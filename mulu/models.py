from django.db import models
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from modelcluster.fields import ParentalKey
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from points.models import Points, PointConfig, Add
from orders.models import Orders
from viplist.models import VipList, VipSetting


class GoodsPageTag(TaggedItemBase):
    content_object = ParentalKey('GoodsPage', related_name='tagged_items', on_delete=models.CASCADE)


class MuluIndexPage(Page):
    parent_page_types = ['home.HomePage']
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='栏目背景图'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # 获取栏目
        brother = self.get_siblings()
        context['brother'] = brother

        # 获取商品
        goodspages = GoodsPage.objects.all().order_by('-first_published_at')
        paginator = Paginator(goodspages, 20)  # Show 3 resources per page
        try:
            page = request.GET.get('page')
            if int(page) == 1:
                context['num'] = 1
            else:
                context['num'] = int(page) + 1
            goodspages = paginator.page(page)
        except AttributeError:
            goodspages = paginator.page(1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            goodspages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            goodspages = paginator.page(paginator.num_pages)
        except TypeError:
            goodspages = paginator.page(1)
            context['num'] = 1

        # make the variable 'resources' available on the templates
        context['goodspages'] = goodspages
        return context

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
    ]


class GoodsSortPage(Page):
    parent_page_types = ['mulu.MuluIndexPage']
    date = models.DateField("Post date", help_text='发布日期')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='栏目背景图'
    )
    home_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='首页封面图片'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # 获取栏目
        brother = self.get_siblings()
        context['brother'] = brother
        farther = self.get_parent()
        parents = farther.get_siblings()
        context['farther'] = farther
        context['parents'] = parents
        #
        goodspages = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(goodspages, 20)  # Show 3 resources per page
        try:
            page = request.GET.get('page')
            if page == 1:
                context['num'] = 1
            else:
                context['num'] = int(page) + 1
            goodspages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            goodspages = paginator.page(1)
            context['num'] = 0
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            goodspages = paginator.page(paginator.num_pages)
            context['num'] = paginator.num_pages + 1
        except TypeError:
            goodspages = paginator.page(1)
            context['num'] = 1
        # make the variable 'resources' available on the templates
        context['goodspages'] = goodspages
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            ImageChooserPanel('image'),
            ImageChooserPanel('home_image'),
        ], heading="分类信息"),
    ]


class GoodsPage(Page):
    parent_page_types = ['mulu.GoodsSortPage']
    tags = ClusterTaggableManager(through=GoodsPageTag, blank=True, help_text='商品类别')
    date = models.DateField("Post date", help_text='发布日期')
    description = models.CharField(max_length=250, help_text='商品描述')
    points = models.IntegerField(help_text='积分需求')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='商品展示图片'
    )

    def get_context(self, request, *args, **kwargs):
        self.user_name = request.user.username
        context = super().get_context(request)
        # 获取栏目
        small_list = self.get_parent()
        big_list = small_list.get_parent()
        parents = big_list.get_siblings()
        brother = small_list.get_siblings()
        context['parents'] = parents
        context['brother'] = brother

        self._points = Points.objects.get(user_name=request.user.username)
        try:
            self.adds = Add.objects.filter(user_name=self.user_name)
        except Add.DoesNotExist:
            self.adds = None
        self.config = PointConfig.objects.get(id=1)
        # 查询用户的所有订单
        self.orders = Orders.objects.filter(user_name=request.user.username).order_by('update_time')
        # 查询用户等级 打多少折扣
        level, discount = self._user_level()
        #剩余积分
        surplus_points = self._current_points() - (self.points * discount)

        if surplus_points < 0:
            context['message'] = '* 对不起您的余额不足兑换该礼品！'
        discount_points = int(self.points * discount)
        context['discount'] = discount
        context['discount_points'] = discount_points
        user = request.user
        context['user'] = user
        return context

    def _user_level(self):
        month_water = int(self._points.one_month_capital_flow + self._points.当月异常流水())
        discount_one_water = int(self.config.discount_one_water)
        discount_two_water = int(self.config.discount_two_water)
        discount_three_water = int(self.config.discount_three_water)
        discount_four_water = int(self.config.discount_four_water)
        discount_five_water = int(self.config.discount_five_water)
        discount_six_water = int(self.config.discount_six_water)
        discount_seven_water = int(self.config.discount_seven_water)
        discount_eight_water = int(self.config.discount_eight_water)
        if month_water < discount_one_water:
            return 0, 1
        elif month_water < discount_two_water:
            return 1, self.config.discount_one_Percent
        elif month_water < discount_three_water:
            return 2, self.config.discount_two_Percent
        elif month_water < discount_four_water:
            return 3, self.config.discount_three_Percent
        elif month_water < discount_five_water:
            return 4, self.config.discount_four_Percent
        elif month_water < discount_six_water:
            return 5, self.config.discount_five_Percent
        elif month_water < discount_seven_water:
            return 6, self.config.discount_six_Percent
        elif month_water < discount_eight_water:
            return 7, self.config.discount_seven_Percent
        else:
            return 8, self.config.discount_eight_Percent

    def _total_points(self):
        water_to_point = self.config.water_to_point
        # 积分修改
        try:
            VipList.objects.get(user_name=self.user_name)
            all_water = self._points.one_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self._points.一年异常流水()) / water_to_point)
            return points
        except VipList.DoesNotExist:
            all_water = self._points.half_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self._points.半年异常流水()) / water_to_point)
            return points

    def _current_points(self):
        points = self._total_points()
        cost = 0
        for line in self.orders:
            if int(line.status) < 4:
                cost = cost + line.cost
        return points - cost

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('image'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('description'),
            FieldPanel('points'),
            FieldPanel('tags'),
        ], heading="商品信息"),
        ImageChooserPanel('image'),
    ]

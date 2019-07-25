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
from wagtail.core.fields import RichTextField
import requests
import datetime


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
        goodspages = GoodsPage.objects.live().order_by('-first_published_at')
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
        parents = farther.get_siblings().live()
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
        # 查询用户今天创建了多少订单
        now = datetime.datetime.now()
        dela = datetime.timedelta(days=-1)
        yesterday = now + dela
        n_days = datetime.datetime.strptime(yesterday.strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.today_order = Orders.objects.filter(user_name=self.user_name).filter(create_time__gt=n_days).exclude(status='4').exclude(status='5')
        # 查询用户等级 打多少折扣
        level, discount = self._user_level()

        #剩余积分
        surplus_points = self._current_points() - (self.points * discount)
        if len(self.today_order) > 2:
            context['message'] = '* 对不起一天最多申请3笔礼品 ！'
        if surplus_points < 0:
            context['message'] = '* 对不起您的余额不足兑换该礼品！'
        discount_points = int(self.points * discount)
        context['discount'] = discount
        context['discount_points'] = discount_points
        user = request.user
        context['user'] = user
        return context

    def _user_level(self):
        # 月流水计算 扣除加减积分
        p = Points.objects.filter(user_name__exact=self.user_name)[0]
        level = p.商城等级()
        if level == 0:
            return level, 1
        elif level == 1:
            return level, self.config.discount_one_Percent
        elif level == 2:
            return level, self.config.discount_two_Percent
        elif level == 3:
            return level, self.config.discount_three_Percent
        elif level == 4:
            return level, self.config.discount_four_Percent
        elif level == 5:
            return level, self.config.discount_five_Percent
        elif level == 6:
            return level, self.config.discount_special_Percent

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


class BargainsPage(Page):
    parent_page_types = ['mulu.GoodsSortPage']
    date = models.DateField("Post date", help_text='发布日期')
    description = models.CharField(max_length=250, help_text='商品描述')
    points = models.IntegerField(help_text='折扣价')
    discount = models.FloatField(help_text='折扣比例')
    introduce = RichTextField(blank=True, help_text='商品详细介绍')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='商品展示图片'
    )

    def get_context(self, request, *args, **kwargs):
        start_time = '2019-06-22'
        self.user_name = request.user.username
        context = super().get_context(request)
        # 获取栏目
        small_list = self.get_parent()
        big_list = small_list.get_parent()
        parents = big_list.get_siblings()
        brother = small_list.get_siblings()
        context['parents'] = parents
        context['brother'] = brother
        context['original_points'] = int(self.points / self.discount)
        self.orders = Orders.objects.filter(user_name=self.user_name).filter(goods_id=self.id)
        current_orders = Orders.objects.filter(user_name=self.user_name).\
            filter(update_time__gt='2019-06-21').\
            filter(goods_id__gte=275).\
            filter(goods_id__lte=286).exclude(status='4').exclude(status='5')
        cost_points = 0
        for order in current_orders:
            cost_points += order.cost
        current_points = self.flush_one_user(start_time) - cost_points
        if len(self.orders) > 1:
            context['message'] = '* 对不起活动期间最多申请2笔该礼品 ！当前剩余积分 %s' % current_points
        if self.points > current_points:
            context['message'] = '* 对不起您活动期间积分不足还请继续努力！当前积分为 %s' % current_points

        return context

    def flush_one_user(self, start_time):
        """
        活动期间积分
        :param start_time:
        :return:
        """
        data = {
            's': 'touzhulist',
            'username': self.user_name,
            'pageRecordCount': 10,
            'pageIndex': 0,
            'start_time': start_time,
            'end_time': datetime.datetime.now().strftime('%Y-%m-%d'),
        }
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data)
            user_data = response.json()
            return int(float(user_data['res'][0]['effbet']) / 400)
        except IndexError:
            return 0
        except Exception:
            return 0

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('image'),
    ]

    content_panels = Page.content_panels + [
            MultiFieldPanel([
                FieldPanel('date'),
                FieldPanel('description'),
                FieldPanel('points'),
                FieldPanel('discount'),
                FieldPanel('introduce'),
            ], heading="商品信息"),
            ImageChooserPanel('image'),
        ]


from django.db import models
from wagtail.core.models import Page, Orderable
from orders.models import Orders
from django.shortcuts import render_to_response
from wagtail.admin.edit_handlers import FieldPanel
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from points.models import Add, Points, PointConfig
from viplist.models import VipList, VipSetting
# from django.contrib.sessions


class AccountIndexPage(Page):
    parent_page_types = ['home.HomePage']

    # 页面显示
    def get_context(self, request, *args, **kwargs):
        self.user_name = request.user.username
        context = super().get_context(request)
        # 获取栏目
        brother = self.get_siblings()
        context['brother'] = brother
        # todo
        # # 单点登录
        # # 数据库中得有一张users表
        # # user = list(Users.objects.filter(username=username, password=password).values())
        # # 用户信息记录在session中
        # # request.session['user'] = user
        # request.session['user'] = request.user
        # # 创建session,否则key为None
        # if not request.session.session_key:
        #     request.session.create()
        #     # 获取session_key
        #     key = request.session.session_key
        # # 当另一机器登录时，本机器应该被挤下即当前sessionkey失效，后登录的用户的session可用，之前的sessionkey从数据库中删除
        # # 获取指定key的session_data，下面用的ORM模型去数据库中取数据
        # session_data = list(DjangoSession.objects.filter(session_key=key).values_list('session_data'))[0][0]
        # # 删除key不为当前key，session_data等于当前session_data的session记录，从而达到一个账号只能一台机器登录的目的
        # models.DjangoSession.objects.filter(session_data=session_data).exclude(session_key=key).delete()

        # 获取订单
        try:
            v = VipList.objects.filter(user_name=self.user_name)
            if len(v) == 0:
                context['vip'] = '0'
            else:
                context['vip'] = '1'
        except VipList.DoesNotExist:
            context['vip'] = '0'
        print(context['vip'])
        self.orders = Orders.objects.filter(user_name=self.user_name).order_by('update_time')
        paginator = Paginator(self.orders, 6)  # Show 3 resources per page
        try:
            page = request.GET.get('page')
            if int(page) == 1:
                context['num'] = 1
            else:
                context['num'] = int(page) + 1
            orders_page = paginator.page(page)
        except AttributeError:
            orders_page = paginator.page(1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            orders_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            orders_page = paginator.page(paginator.num_pages)
        except TypeError:
            orders_page = paginator.page(1)
            context['num'] = 1

        self.points = Points.objects.get(user_name=self.user_name)
        try:
            self.adds = Add.objects.filter(user_name=self.user_name)
        except Add.DoesNotExist:
            self.adds = None
        self.config = PointConfig.objects.get(id=1)
        user = request.user
        context['user'] = user
        context['orders'] = orders_page
        context['total_points'] = self._total_points()
        context['current_points'] = self._current_points()
        context['level'], context['up_need'] = self._user_level()
        return context

    def _user_level(self):
        # 月流水计算 没有扣除加减积分
        month_water = int(self.points.one_month_capital_flow)
        water_to_point = self.config.water_to_point
        discount_one_water = int(self.config.discount_one_water)
        discount_two_water = int(self.config.discount_two_water)
        discount_three_water = int(self.config.discount_three_water)
        discount_four_water = int(self.config.discount_four_water)
        discount_five_water = int(self.config.discount_five_water)
        discount_six_water = int(self.config.discount_six_water)
        discount_seven_water = int(self.config.discount_seven_water)
        discount_eight_water = int(self.config.discount_eight_water)
        if month_water < discount_one_water:
            return 0, int((discount_one_water - month_water)/water_to_point)
        elif month_water < discount_two_water:
            return 1, int((discount_two_water - month_water)/water_to_point)
        elif month_water < discount_three_water:
            return 2, int((discount_three_water - month_water)/water_to_point)
        elif month_water < discount_four_water:
            return 3, int((discount_four_water - month_water)/water_to_point)
        elif month_water < discount_five_water:
            return 4, int((discount_five_water - month_water)/water_to_point)
        elif month_water < discount_six_water:
            return 5, int((discount_six_water - month_water)/water_to_point)
        elif month_water < discount_seven_water:
            return 6, int((discount_seven_water - month_water)/water_to_point)
        elif month_water < discount_eight_water:
            return 7, int((discount_eight_water - month_water)/water_to_point)
        else:
            return 8, -1

    def _total_points(self):
        water_to_point = self.config.water_to_point
        # 积分修改
        add_points = 0
        if add_points is not None:
            for p in self.adds:
                add_points += p.change_points

        try:
            VipList.objects.get(user_name=self.user_name)
            all_water = self.points.one_year_capital_flow
            # 积分 加减控制
            points = int(all_water / water_to_point) + add_points
            return points
        except VipList.DoesNotExist:
            all_water = self.points.half_year_capital_flow
            # 积分 加减控制
            points = int(all_water / water_to_point) + add_points
            return points

    def _current_points(self):
        points = self._total_points()
        cost = 0
        for line in self.orders:
            if line.status != '4':
                cost = cost + line.cost
        return points - cost

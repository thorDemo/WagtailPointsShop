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
        # todo 单点登录
        # 获取订单
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
        context['level'] = self._user_level() + 1
        context['ico'] = self._user_level()
        context['level_up_1'], context['level_up_2'] = self._level_up_total_capital()
        return context

    def _user_level(self):
        # 月流水计算 扣除加减积分
        p = Points.objects.filter(user_name__exact=self.user_name)[0]
        return p.商城等级()

    def _total_points(self):
        water_to_point = self.config.water_to_point
        # 积分修改
        try:
            VipList.objects.get(user_name=self.user_name)
            all_water = self.points.one_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self.points.一年异常流水()) / water_to_point)
            return points
        except VipList.DoesNotExist:
            all_water = self.points.half_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self.points.半年异常流水()) / water_to_point)
            return points

    def _current_points(self):
        points = self._total_points()
        cost = 0
        for line in self.orders:
            if int(line.status) < 4:
                cost = cost + line.cost
        return points - cost

    def _level_up_total_capital(self):
        if self._user_level() == 0:
            return self.config.discount_one_water, self.config.discount_one_slot_machine
        elif self._user_level() == 1:
            return self.config.discount_two_water, self.config.discount_two_slot_machine
        elif self._user_level() == 2:
            return self.config.discount_three_water, self.config.discount_three_slot_machine
        elif self._user_level() == 3:
            return self.config.discount_four_water, self.config.discount_four_slot_machine
        elif self._user_level() == 4:
            return self.config.discount_five_water, self.config.discount_five_slot_machine
        elif self._user_level() == 5:
            return self.config.discount_special_water, self.config.discount_special_slot_machine
        elif self._user_level() == 6:
            return 0, 0
        else:
            return self.config.discount_one_water, self.config.discount_one_slot_machine

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel
from orders.models import Orders
from viplist.models import VipList, VipSetting
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import F


class Points(models.Model):
    """
    当前流水
    """
    user_name = models.CharField(max_length=255, unique=True)
    one_year_capital_flow = models.IntegerField(help_text='一年总流水', default=0)
    half_year_capital_flow = models.IntegerField(help_text='半年总流水', default=0)
    one_month_capital_flow = models.IntegerField(help_text='当月总流水', default=0)

    def 游戏账号(self):
        return self.user_name

    def 当月流水(self):
        error = self.当月异常流水()
        return self.one_month_capital_flow + error

    def 半年流水(self):
        error = self.半年异常流水()
        return self.half_year_capital_flow + error

    def 一年流水(self):
        error = self.一年异常流水()
        return self.one_year_capital_flow + error

    def 剩余积分(self):
        # 获取积分配置信息
        self.config = PointConfig.objects.get(id=1)
        self.orders = Orders.objects.filter(user_name=self.user_name).order_by('update_time')
        points = self.总积分()
        cost = 0
        for line in self.orders:
            if int(line.status) < 4:
                cost = cost + line.cost
        return points - cost

    def vip(self):
        # 获取VIP状态
        try:
            v = VipList.objects.filter(user_name=self.user_name)
            if len(v) == 0:
                vip = '0'
            else:
                vip = '1'
        except VipList.DoesNotExist:
            vip = '0'
        return vip

    def 商城等级(self):
        # 会员等级
        self.config = PointConfig.objects.get(id=1)
        month_water = self.one_month_capital_flow + self.当月异常流水()
        discount_one_water = int(self.config.discount_one_water)
        discount_two_water = int(self.config.discount_two_water)
        discount_three_water = int(self.config.discount_three_water)
        discount_four_water = int(self.config.discount_four_water)
        discount_five_water = int(self.config.discount_five_water)
        discount_six_water = int(self.config.discount_six_water)
        discount_seven_water = int(self.config.discount_seven_water)
        discount_eight_water = int(self.config.discount_eight_water)
        if month_water < discount_one_water:
            return 0
        elif month_water < discount_two_water:
            return 1
        elif month_water < discount_three_water:
            return 2
        elif month_water < discount_four_water:
            return 3
        elif month_water < discount_five_water:
            return 4
        elif month_water < discount_six_water:
            return 5
        elif month_water < discount_seven_water:
            return 6
        elif month_water < discount_eight_water:
            return 7
        else:
            return 8

    def 总积分(self):
        # 获取积分配置信息
        water_to_point = self.config.water_to_point
        # 积分修改
        try:
            VipList.objects.get(user_name=self.user_name)
            all_water = self.one_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self.一年异常流水()) / water_to_point)
            return points
        except VipList.DoesNotExist:
            all_water = self.half_year_capital_flow
            # 积分 加减控制
            points = int((all_water + self.半年异常流水()) / water_to_point)
            return points

    def 当月异常流水(self):
        try:
            # 获取流水加减表
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=-30)
            n_days = now + delta
            self.adds = Add.objects.filter(user_name=self.user_name).filter(update_time__gte=n_days)
        except Add.DoesNotExist:
            self.adds = None
        add_points = 0
        if add_points is not None:
            for p in self.adds:
                add_points += p.change_points
        return add_points

    def 半年异常流水(self):
        try:
            # 获取流水加减表
            now = datetime.datetime.now()
            delta = relativedelta(months=-6)
            n_days = now + delta
            self.adds = Add.objects.filter(user_name=self.user_name).filter(update_time__gte=n_days)
        except Add.DoesNotExist:
            self.adds = None
        add_points = 0
        if add_points is not None:
            for p in self.adds:
                add_points += p.change_points
        return add_points

    def 一年异常流水(self):
        try:
            # 获取流水加减表
            now = datetime.datetime.now()
            delta = relativedelta(years=-1)
            n_days = now + delta
            self.adds = Add.objects.filter(user_name=self.user_name).filter(update_time__gte=n_days)
        except Add.DoesNotExist:
            self.adds = None
        add_points = 0
        if add_points is not None:
            for p in self.adds:
                add_points += p.change_points
        return add_points


class Cost(models.Model):
    """
    积分 消费情况
    """
    user_name = models.CharField(max_length=255, help_text='用户名')
    goods = models.CharField(max_length=255, help_text='消费商品')
    goods_id = models.IntegerField(help_text='消费商品ID')
    change_points = models.IntegerField()
    tips = models.CharField(max_length=255, help_text='积分加减备注')
    update_time = models.TimeField(auto_now=True)

    panels = [
        FieldPanel('user_name'),
        FieldPanel('change_points'),
        FieldPanel('goods'),
        FieldPanel('tips'),
    ]


class Add(models.Model):
    """
    积分 增加情况
    """
    user_name = models.CharField(max_length=255, help_text='用户名')
    change_points = models.IntegerField(help_text='流水加减 这里输入的是流水不是积分')
    tips = models.CharField(max_length=255, help_text='积分加减备注')
    update_time = models.DateField(help_text='积分修改时间')
    
    def capital_flow(self):
        return self.change_points

    panels = [
        FieldPanel('user_name'),
        FieldPanel('change_points'),
        FieldPanel('tips'),
        FieldPanel('update_time'),
    ]


class PointConfig(models.Model):
    config_name = models.CharField(max_length=255, default='默认配置1', help_text='配置名称')
    auto_flush = models.CharField(max_length=255,default='2019-01-01', help_text='积分计算起始日期，自动更新1天一次，可联系我手动更新')
    water_to_point = models.IntegerField(help_text='流水积分兑换比例')
    discount_one_Percent = models.FloatField(help_text='1级会员折扣比例')
    discount_one_water = models.IntegerField(help_text='1级会员流水需求')
    discount_two_Percent = models.FloatField(help_text='2级会员折扣比例')
    discount_two_water = models.IntegerField(help_text='2级会员流水需求')
    discount_three_Percent = models.FloatField(help_text='3级会员折扣比例')
    discount_three_water = models.IntegerField(help_text='3级会员流水需求')
    discount_four_Percent = models.FloatField(help_text='4级会员折扣比例')
    discount_four_water = models.IntegerField(help_text='4级会员流水需求')
    discount_five_Percent = models.FloatField(help_text='5级会员折扣比例')
    discount_five_water = models.IntegerField(help_text='5级会员流水需求')
    discount_six_Percent = models.FloatField(help_text='6级会员折扣比例')
    discount_six_water = models.IntegerField(help_text='6级会员流水需求')
    discount_seven_Percent = models.FloatField(help_text='7级会员折扣比例')
    discount_seven_water = models.IntegerField(help_text='7级会员流水需求')
    discount_eight_Percent = models.FloatField(help_text='8级会员折扣比例')
    discount_eight_water = models.IntegerField(help_text='8级会员流水需求')

    panels = [
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('config_name', classname="col6"), ]),
            FieldRowPanel([FieldPanel('water_to_point', classname="col6"), ]),
            FieldRowPanel([FieldPanel('auto_flush', classname="col6"), ]),
        ], "主配置"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('discount_one_Percent', classname="col6"),
                FieldPanel('discount_one_water', classname="col6"),
                FieldPanel('discount_two_Percent', classname="col6"),
                FieldPanel('discount_two_water', classname="col6"),
                FieldPanel('discount_three_Percent', classname="col6"),
                FieldPanel('discount_three_water', classname="col6"),
                FieldPanel('discount_four_Percent', classname="col6"),
                FieldPanel('discount_four_water', classname="col6"),
                FieldPanel('discount_five_Percent', classname="col6"),
                FieldPanel('discount_five_water', classname="col6"),
                FieldPanel('discount_six_Percent', classname="col6"),
                FieldPanel('discount_six_water', classname="col6"),
                FieldPanel('discount_seven_Percent', classname="col6"),
                FieldPanel('discount_seven_water', classname="col6"),
                FieldPanel('discount_eight_Percent', classname="col6"),
                FieldPanel('discount_eight_water', classname="col6"),
            ]),
        ], "折扣等级比例"),
    ]


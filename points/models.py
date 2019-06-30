from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel
from orders.models import Orders
from viplist.models import VipList, VipSetting
import datetime
from dateutil.relativedelta import relativedelta
from data.models import MonthDataStatistic, DataIndexPage
import pytz


class Points(models.Model):
    """
    当前流水
    """
    user_name = models.CharField(max_length=255, unique=True)
    one_year_capital_flow = models.FloatField(help_text='一年总流水', default=0)
    half_year_capital_flow = models.FloatField(help_text='半年总流水', default=0)
    one_month_capital_flow = models.FloatField(help_text='当月总流水', default=0)
    one_year_lottery = models.FloatField(help_text='一年彩票流水', default=0)
    half_year_lottery = models.FloatField(help_text='半年彩票流水', default=0)
    month_lottery = models.FloatField(help_text='一月彩票流水', default=0)
    user_level = models.IntegerField(help_text='VIP等级', default=0)

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
            v = VipList.objects.filter(user_id=self.user_name)
            if len(v) == 0:
                vip = '0'
            else:
                vip = '1'
        except VipList.DoesNotExist:
            vip = '0'
        return vip

    def 商城等级(self):
        # todo
        # 会员等级
        self.config = PointConfig.objects.get(id=1)
        month_water = self.one_month_capital_flow + self.当月异常流水()
        # 当月老虎机流水
        user_month_data = MonthDataStatistic.objects.filter(user__exact=self.user_name)
        if len(user_month_data) == 0:
            slot_machine = 0
        else:
            slot_machine = int(user_month_data[0].slot_machine)
        # 老虎机流水标准
        discount_one_slot_machine = int(self.config.discount_one_slot_machine)
        discount_two_slot_machine = int(self.config.discount_two_slot_machine)
        discount_three_slot_machine = int(self.config.discount_three_slot_machine)
        discount_four_slot_machine = int(self.config.discount_three_slot_machine)
        discount_five_slot_machine = int(self.config.discount_three_slot_machine)

        # 总流水标准
        discount_one_water = int(self.config.discount_one_water)
        discount_two_water = int(self.config.discount_two_water)
        discount_three_water = int(self.config.discount_three_water)
        discount_four_water = int(self.config.discount_four_water)
        discount_five_water = int(self.config.discount_five_water)
        # moth_water = 1000w  slot_machine = 20k
        all_capital_level = 0
        slot_machine_level = 0
        current_level = self.user_level

        tz = pytz.timezone('America/New_York')
        now = datetime.datetime.now(tz).date().day

        # VipList.objects.filter(user_name__exact=self.user_name)

        if int(now) == 1:   #如果当前时间是美东时间的 1号 就开始计算等级 不是的话返回当前等级
            if month_water == 0:
                # 如果月流水为0  查询用户最后玩的是哪天 每超过一个月 扣一个等级
                try:
                    last_date = DataIndexPage.objects.filter(user__exact=self.user_name).order_by('-date')[0].date
                    now_date = datetime.datetime.now(tz).date().month
                    temp_date = int(now_date - last_date.month)
                    current_level -= temp_date
                except IndexError:
                    # 如果查询不到 扣其实时间到现在月份的数量
                    now_date = datetime.datetime.now(tz).date().month
                    temp_date = int(now_date - datetime.date(2019, 6, 1).month)
                    current_level -= temp_date
            else:
                if month_water < discount_one_water:
                    all_capital_level = 0
                elif month_water < discount_two_water:
                    all_capital_level = 1
                elif month_water < discount_three_water:
                    all_capital_level = 2
                elif month_water < discount_four_water:
                    all_capital_level = 3
                elif month_water < discount_five_water:
                    all_capital_level = 4
                else:
                    all_capital_level = 5

                if slot_machine <= discount_one_slot_machine:
                    slot_machine_level = 0
                elif slot_machine < discount_two_slot_machine:
                    slot_machine_level = 1
                elif slot_machine < discount_three_slot_machine:
                    slot_machine_level = 2
                elif slot_machine < discount_four_slot_machine:
                    slot_machine_level = 3
                elif slot_machine < discount_five_slot_machine:
                    slot_machine_level = 4
                else:
                    slot_machine_level = 5
            # hamham1995
            all_level = [all_capital_level, slot_machine_level, current_level]
            # 保存数据
            Points.objects.filter(user_name__exact=self.user_name).update(user_level=max(all_level))
            return max(all_level)
        else:
            return self.user_level

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
        return add_points - self.month_lottery

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
        return add_points - self.half_year_lottery

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
        return add_points - self.one_year_lottery


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

    def 流水变动(self):
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
    discount_one_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)
    discount_two_Percent = models.FloatField(help_text='2级会员折扣比例')
    discount_two_water = models.IntegerField(help_text='2级会员流水需求')
    discount_two_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)
    discount_three_Percent = models.FloatField(help_text='3级会员折扣比例')
    discount_three_water = models.IntegerField(help_text='3级会员流水需求')
    discount_three_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)
    discount_four_Percent = models.FloatField(help_text='4级会员折扣比例')
    discount_four_water = models.IntegerField(help_text='4级会员流水需求')
    discount_four_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)
    discount_five_Percent = models.FloatField(help_text='5级会员折扣比例')
    discount_five_water = models.IntegerField(help_text='5级会员流水需求')
    discount_five_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)
    discount_special_Percent = models.FloatField(help_text='特邀会员折扣比例', default=0.82)
    discount_special_water = models.IntegerField(help_text='特邀会员流水需求', default=0)
    discount_special_slot_machine = models.IntegerField(help_text='老虎机流水需求', default=0)

    panels = [
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('config_name', classname="col6"), ]),
            FieldRowPanel([FieldPanel('water_to_point', classname="col6"), ]),
            FieldRowPanel([FieldPanel('auto_flush', classname="col6"), ]),
        ], "主配置"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('discount_one_Percent', classname="col4"),
                FieldPanel('discount_one_water', classname="col4"),
                FieldPanel('discount_one_slot_machine', classname="col4"),

                FieldPanel('discount_two_Percent', classname="col4"),
                FieldPanel('discount_two_water', classname="col4"),
                FieldPanel('discount_two_slot_machine', classname="col4"),

                FieldPanel('discount_three_Percent', classname="col4"),
                FieldPanel('discount_three_water', classname="col4"),
                FieldPanel('discount_three_slot_machine', classname="col4"),

                FieldPanel('discount_four_Percent', classname="col4"),
                FieldPanel('discount_four_water', classname="col4"),
                FieldPanel('discount_four_slot_machine', classname="col4"),

                FieldPanel('discount_five_Percent', classname="col4"),
                FieldPanel('discount_five_water', classname="col4"),
                FieldPanel('discount_five_slot_machine', classname="col4"),

                FieldPanel('discount_special_Percent', classname="col4"),
                FieldPanel('discount_special_water', classname="col4"),
                FieldPanel('discount_special_slot_machine', classname="col4"),

            ]),
        ], "折扣等级比例"),
    ]


from django.db import models
from wagtail.core.models import Page


class DataIndexPage(models.Model):
    proxy = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, default='Thor')
    capital_flow = models.FloatField(help_text='有效总投注', default=0.0)
    capital_return = models.FloatField(help_text='优惠金小计', default=0.0)
    sports = models.FloatField(help_text='体育赛事', default=0.0)
    table = models.FloatField(help_text='视讯直播', default=0.0)
    slot_machine = models.FloatField(help_text='老虎机', default=0.0)
    lottery = models.FloatField(help_text='彩票', default=0.0)
    fishing_machine = models.FloatField(help_text='捕鱼机', default=0.0)
    poker = models.FloatField(help_text='棋牌', default=0.0)
    update = models.DateField(auto_now=True)
    date = models.DateField(default='2016-06-01')

    def __str__(self):
        return '源数据'


class OneYearDataStatistic(models.Model):
    proxy = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, default='Thor')
    capital_flow = models.FloatField(help_text='有效总投注', default=0.0)
    capital_return = models.FloatField(help_text='优惠金小计', default=0.0)
    sports = models.FloatField(help_text='体育赛事', default=0.0)
    table = models.FloatField(help_text='视讯直播', default=0.0)
    slot_machine = models.FloatField(help_text='老虎机', default=0.0)
    lottery = models.FloatField(help_text='彩票', default=0.0)
    fishing_machine = models.FloatField(help_text='捕鱼机', default=0.0)
    poker = models.FloatField(help_text='棋牌', default=0.0)

    def __str__(self):
        return '一年总数据统计'


class HalfYearDataStatistic(models.Model):
    proxy = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, default='Thor')
    capital_flow = models.FloatField(help_text='有效总投注', default=0.0)
    capital_return = models.FloatField(help_text='优惠金小计', default=0.0)
    sports = models.FloatField(help_text='体育赛事', default=0.0)
    table = models.FloatField(help_text='视讯直播', default=0.0)
    slot_machine = models.FloatField(help_text='老虎机', default=0.0)
    lottery = models.FloatField(help_text='彩票', default=0.0)
    fishing_machine = models.FloatField(help_text='捕鱼机', default=0.0)
    poker = models.FloatField(help_text='棋牌', default=0.0)

    def __str__(self):
        return '半年总数据统计'


class MonthDataStatistic(models.Model):
    proxy = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, default='Thor')
    capital_flow = models.FloatField(help_text='有效总投注', default=0.0)
    capital_return = models.FloatField(help_text='优惠金小计', default=0.0)
    sports = models.FloatField(help_text='体育赛事', default=0.0)
    table = models.FloatField(help_text='视讯直播', default=0.0)
    slot_machine = models.FloatField(help_text='老虎机', default=0.0)
    lottery = models.FloatField(help_text='彩票', default=0.0)
    fishing_machine = models.FloatField(help_text='捕鱼机', default=0.0)
    poker = models.FloatField(help_text='棋牌', default=0.0)

    def __str__(self):
        return '月数据统计'


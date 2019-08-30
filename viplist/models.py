from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel
from data.models import MonthDataStatistic
# from points.models import PointConfig


class VipList(models.Model):
    user_id = models.CharField(max_length=255, help_text='游戏账号', blank=True)
    user_name = models.CharField(max_length=255, help_text='姓名')
    user_level = models.CharField(max_length=255, help_text='官网VIP层级别', blank=True)
    shop_level = models.IntegerField(default=0, help_text='积分商城VIP')
    level_up = models.IntegerField(default=0, help_text='升级礼金兑换记录')
    flag_level = models.BooleanField(default=0, help_text='升级标识')
    flag_money = models.BooleanField(default=0, help_text='首次标识')
    change_time = models.DateField(auto_now=True)
    current_level_up_money = models.IntegerField(default=0, help_text='当月晋级礼金')

    def __str__(self):
        return '%s %s' % (self.user_id, self.user_name)

    def 会员等级(self):
        if self.shop_level == 0:
            return '普通会员'
        elif self.shop_level == 1:
            return '黄金会员'
        elif self.shop_level == 2:
            return '铂金会员'
        elif self.shop_level == 3:
            return '钻石会员'
        elif self.shop_level == 4:
            return '至尊会员'
        elif self.shop_level == 5:
            return '王者会员'
        elif self.shop_level == 6:
            return '特邀会员'

    def month_capital(self):
        try:
            data = MonthDataStatistic.objects.filter(user__exact=self.user_id)[0]
            return data.capital_flow
        except IndexError:
            #print(self.user_id)
            return 0

    def month_lottery(self):
        try:
            data = MonthDataStatistic.objects.filter(user__exact=self.user_id)[0]
            return data.lottery
        except IndexError:
            #print(self.user_id)
            return 0

    class Meta:
        db_table = 'vip_list'


class VipSetting(models.Model):
    vip_valid = models.IntegerField(help_text='VIP客户积分有效期限 单位月')
    common_valid = models.IntegerField(help_text='普通客户积分有效期限 单位月')
    level_up_one = models.IntegerField(help_text='黄金会员晋级礼金', default=58)
    level_up_two = models.IntegerField(help_text='铂金会员晋级礼金', default=188)
    level_up_three = models.IntegerField(help_text='钻石会员晋级礼金', default=588)
    level_up_four = models.IntegerField(help_text='至尊会员晋级礼金', default=888)
    level_up_five = models.IntegerField(help_text='王者会员晋级礼金', default=1888)
    level_up_six = models.IntegerField(help_text='特邀会员晋级礼金', default=2888)
    update_time = models.DateField(auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('vip_valid', classname='col6'), ]),
            FieldRowPanel([FieldPanel('common_valid', classname='col6'), ]),
        ], '有效期设定'),
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('level_up_one', classname='col12')]),
            FieldRowPanel([FieldPanel('level_up_two', classname='col12')]),
            FieldRowPanel([FieldPanel('level_up_three', classname='col12'), ]),
            FieldRowPanel([FieldPanel('level_up_four', classname='col12'), ]),
            FieldRowPanel([FieldPanel('level_up_five', classname='col12'), ]),
            FieldRowPanel([FieldPanel('level_up_six', classname='col12'), ]),
        ], '晋级礼金设定')
    ]

    class Meta:
        db_table = 'vip_setting'

from django.db import models


class VipList(models.Model):
    user_id = models.CharField(max_length=255, help_text='游戏账号', blank=True)
    user_name = models.CharField(max_length=255, help_text='姓名')
    user_level = models.CharField(max_length=255, help_text='官网VIP层级别', blank=True)
    change_time = models.DateField(auto_now=True)

    def 游戏账号(self):
        return self.user_id

    def 姓名(self):
        return self.user_name

    def 官网VIP层级别(self):
        return self.user_level

    class Meta:
        db_table = 'vip_list'


class VipSetting(models.Model):
    vip_valid = models.IntegerField(help_text='VIP客户积分有效期限 单位月')
    common_valid = models.IntegerField(help_text='普通客户积分有效期限 单位月')
    update_time = models.DateField(auto_now=True)

    class Meta:
        db_table = 'vip_setting'

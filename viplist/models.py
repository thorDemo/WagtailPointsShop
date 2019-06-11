from django.db import models


class VipList(models.Model):

    user_name = models.CharField(max_length=255, help_text='用户名')
    change_time = models.DateField(auto_now=True)

    class Meta:
        db_table = 'vip_list'


class VipSetting(models.Model):
    vip_valid = models.IntegerField(help_text='VIP客户积分有效期限 单位月')
    common_valid = models.IntegerField(help_text='普通客户积分有效期限 单位月')
    update_time = models.DateField(auto_now=True)

    class Meta:
        db_table = 'vip_setting'

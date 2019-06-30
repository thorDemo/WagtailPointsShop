from peewee import *


database = SqliteDatabase('db.sqlite3', pragmas={'journal_mode': 'wal', 'cache_size': -1024 * 64})
# database = SqliteDatabase('/www/wwwroot/WagtailPointsShop/db.sqlite3', pragmas={'journal_mode': 'wal', 'cache_size': -1024 * 64})


class AuthUser(Model):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=150)
    password = CharField(max_length=128)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=150)
    email = CharField(max_length=254)
    last_login = DateField()
    is_superuser = BooleanField(default=0)
    is_staff = BooleanField(default=0)
    is_active = BooleanField(default=1)
    date_joined = DateField()

    class Meta:
        table_name = 'auth_user'
        database = database


class AuthGroup(Model):
    user_id = IntegerField()
    group_id = IntegerField()

    class Meta:
        table_name = 'auth_user_groups'
        database = database


class PointsPoints(Model):
    user_name = CharField(max_length=255)
    one_year_capital_flow = FloatField()
    half_year_capital_flow = FloatField()
    one_month_capital_flow = FloatField()
    one_year_lottery = FloatField()
    half_year_lottery = FloatField()
    month_lottery = FloatField()
    user_level = IntegerField()

    class Meta:
        table_name = 'points_points'
        database = database


class PointConfig(Model):
    config_name = CharField(max_length=255, default='默认配置1', help_text='配置名称')
    auto_flush = CharField(max_length=255, default='2019-01-01', help_text='积分计算起始日期，自动更新1天一次，可联系我手动更新')
    water_to_point = IntegerField(help_text='流水积分兑换比例')
    discount_one_Percent = FloatField(help_text='1级会员折扣比例')
    discount_one_water = IntegerField(help_text='1级会员流水需求')
    discount_two_Percent = FloatField(help_text='2级会员折扣比例')
    discount_two_water = IntegerField(help_text='2级会员流水需求')
    discount_three_Percent = FloatField(help_text='3级会员折扣比例')
    discount_three_water = IntegerField(help_text='3级会员流水需求')
    discount_four_Percent = FloatField(help_text='4级会员折扣比例')
    discount_four_water = IntegerField(help_text='4级会员流水需求')
    discount_five_Percent = FloatField(help_text='5级会员折扣比例')
    discount_five_water = IntegerField(help_text='5级会员流水需求')
    discount_six_Percent = FloatField(help_text='6级会员折扣比例')
    discount_six_water = IntegerField(help_text='6级会员流水需求')
    discount_seven_Percent = FloatField(help_text='7级会员折扣比例')
    discount_seven_water = IntegerField(help_text='7级会员流水需求')
    discount_eight_Percent = FloatField(help_text='8级会员折扣比例')
    discount_eight_water = IntegerField(help_text='8级会员流水需求')

    class Meta:
        table_name = 'points_pointconfig'
        database = database


class VipList(Model):
    id = IntegerField(primary_key=True)
    user_id = CharField(max_length=255)
    user_name = CharField(max_length=255)
    user_level = CharField(max_length=255)
    change_time = DateField()

    class Meta:
        table_name = 'vip_list'
        database = database


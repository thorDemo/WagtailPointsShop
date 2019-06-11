from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel


class Points(models.Model):
    """
    当前积分情况
    """
    user_name = models.CharField(max_length=255, unique=True)
    one_year_capital_flow = models.IntegerField(help_text='一年总流水', default=0)
    half_year_capital_flow = models.IntegerField(help_text='半年总流水', default=0)
    one_month_capital_flow = models.IntegerField(help_text='当月总流水', default=0)

    panels = [
        FieldPanel('user_name'),
        FieldPanel('one_year_capital_flow'),
        FieldPanel('half_year_capital_flow'),
        FieldPanel('one_month_capital_flow'),
    ]


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
    change_points = models.IntegerField()
    tips = models.CharField(max_length=255, help_text='积分加减备注')
    update_time = models.TimeField(auto_now=True)

    panels = [
        FieldPanel('user_name'),
        FieldPanel('change_points'),
        FieldPanel('tips'),
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


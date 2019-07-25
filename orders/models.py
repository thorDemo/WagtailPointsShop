from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel


class Orders(models.Model):
    take_name = models.CharField(max_length=255, help_text='取货姓名')
    user_name = models.CharField(max_length=255)
    goods = models.CharField(max_length=255)
    goods_id = models.IntegerField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', default=9
    )
    email = models.EmailField(help_text='邮箱地址')
    phone = models.IntegerField(help_text='电话号码')
    wechart = models.CharField(max_length=255, help_text='微信号码')
    address = models.CharField(max_length=255, help_text='收货地址')
    tips = models.CharField(max_length=255, help_text='备注')
    cost = models.IntegerField(help_text='折扣价')
    discount = models.FloatField(help_text='折扣比例')
    real_cost = models.IntegerField(help_text='商品需要积分')
    status_choices = (('0', '待确认'), ('1', '待发货'), ('2', '配送中'), ('3', '已送达'), ('4', '已取消'), ('5', '不符合'))
    status = models.CharField(max_length=255, choices=status_choices, default='0', help_text='订单状态')
    update_time = models.DateField(auto_now=True)
    create_time = models.DateField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('take_name', classname='col12'),
            FieldPanel('phone', classname='col12'),
            FieldPanel('wechart', classname='col12'),
            FieldPanel('email', classname='col12'),
            FieldPanel('address', classname='col12'),
            FieldPanel('status', classname='col12'),
        ],  '订单信息修改')
    ]



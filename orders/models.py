from django.db import models
from wagtail.admin.edit_handlers import FieldPanel


class Orders(models.Model):
    take_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    goods = models.CharField(max_length=255)
    goods_id = models.IntegerField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', default=9
    )
    email = models.EmailField()
    phone = models.IntegerField()
    wechart = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tips = models.CharField(max_length=255, help_text='备注')
    cost = models.IntegerField(help_text='折扣价')
    discount = models.FloatField(help_text='折扣比例')
    real_cost = models.IntegerField(help_text='商品需要积分')
    status_choices = (('0', '待确认'), ('1', '待发货'), ('2', '配送中'), ('3', '已送达'), ('4', '已取消'))
    status = models.CharField(max_length=255, choices=status_choices, default='0')
    update_time = models.DateField(auto_now=True)
    create_time = models.DateField(auto_now_add=True)

    panels = [
        FieldPanel('take_name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('wechart'),
        FieldPanel('address'),
        FieldPanel('status'),
    ]



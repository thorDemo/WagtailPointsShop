from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Orders


class OrdersAdmin(ModelAdmin):
    model = Orders
    menu_label = '订单管理'
    menu_icon = 'list-ul'
    menu_order = 1000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('create_time', 'goods', 'user_name', 'take_name',  'phone', 'address', 'cost', 'discount', 'status')
    list_filter = ('create_time', 'user_name', 'status')
    search_fields = ('create_time', 'goods', 'user_name', 'take_name', 'wechart')


modeladmin_register(OrdersAdmin)

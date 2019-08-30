from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Orders
from django.conf.urls import url
from wagtail.core import hooks
from orders.models import Orders
from django.db import connection
from django.http import JsonResponse


class OrdersAdmin(ModelAdmin):
    model = Orders
    menu_label = '订单管理'
    menu_icon = 'list-ul'
    menu_order = 1000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('create_time', 'user_name', 'take_name', 'goods', 'phone', 'address', 'cost', 'discount', 'status')
    list_filter = ('create_time', 'status')
    search_fields = ('create_time', 'goods', 'user_name', 'take_name', 'wechart')


modeladmin_register(OrdersAdmin)

#
# def restore_time(request):
#
#     all_data = Orders.objects.all()
#     for line in all_data:
#         print(line.user_name, line.update_time)
#         Orders.objects.filter(id=line.id).update(
#             update_time=str(line.update_time) + ' 00:00:00.122027',
#             create_time=str(line.create_time) + ' 00:00:00.122027'
#         )
#     return JsonResponse({'status': 1})
#
#
# @hooks.register('register_admin_urls')
# def submit_query():
#     return [
#         url(r'deal/restore_time/', restore_time)
#     ]

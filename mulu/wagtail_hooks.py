# --*-- coding=utf-8 --*--
from wagtail.core import hooks
from django.http import JsonResponse
from django.conf.urls import url
import datetime
from django.views.decorators.csrf import csrf_protect
from orders.models import Orders
# from points.models import Points, Cost
from django.shortcuts import redirect

#
# @csrf_protect
# def order_builder(request):
#     pass
#
#
# @hooks.register('register_admin_urls')
# def submit_query():
#     return [
#         url(r'deal/order/', order_builder)
#     ]

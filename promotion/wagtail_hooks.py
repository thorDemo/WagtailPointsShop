# --*-- coding=utf-8 --*--
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import PromotionSetting
from wagtail.core import hooks
from django.http import JsonResponse
from django.conf.urls import url
import os
from xml.dom.minidom import parse
from decimal import Decimal
import traceback
import datetime
from dateutil.relativedelta import relativedelta
import pytz
from points.models import Points
from django.core.cache import cache


class PromotionAdmin(ModelAdmin):
    model = PromotionSetting
    menu_label = '活动设置'
    menu_icon = 'time'
    list_display = ('check_cookie', 'set_first_time', 'set_second_time', 'set_third_time')
    # search_fields = ('proxy', 'user', 'date')


class LibraryGroup(ModelAdminGroup):
    menu_label = '促销活动'
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (PromotionAdmin,)


modeladmin_register(LibraryGroup)



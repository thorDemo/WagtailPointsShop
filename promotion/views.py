from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.http import JsonResponse
from promotion.models import PromotionSetting
from dateutil import tz


def submit_query_view(request):
    cn = tz.gettz('Asia/Shanghai')
    now = datetime.datetime.now(tz=cn)
    config = PromotionSetting.objects.all()[0]
    first = datetime.datetime(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
        int(config.set_first_time),
        0,
        tzinfo=cn
    )
    second = datetime.datetime(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
        int(config.set_second_time),
        0,
        tzinfo=cn
    )
    third = datetime.datetime(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
        int(config.set_third_time),
        0,
        tzinfo=cn
    )
    if 0 < (now - first).seconds < 3600:
        time = 3600 - (now - first).seconds
        message = '下次活动开始于北京时间 18:00 - 19:00'
    elif 0 < (now - second).seconds < 3600:
        time = 3600 - (now - second).seconds
        message = '下次活动开始于北京时间 21:00 - 22:00'
    elif 0 < (now - third).seconds < 3600:
        time = 3600 - (now - third).seconds
        message = '下次活动于明天北京时间 14:00 - 15:00'
    elif now.hour < 14:
        time = 0
        message = '下次活动开始于北京时间 14:00 - 15:00'
    elif now.hour < 18:
        time = 0
        message = '下次活动开始于北京时间 18:00 - 19:00'
    elif now.hour < 21:
        time = 0
        message = '下次活动开始于北京时间 21:00 - 22:00'
    else:
        time = 0
        message = '下次活动于明天北京时间 14:00 - 15:00'

    return JsonResponse({'time': time, 'message': message})

# --*-- coding=utf-8 --*--
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import DataIndexPage, OneYearDataStatistic, MonthDataStatistic, HalfYearDataStatistic
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
from points.models import Points, Add


class User:
    def __init__(self):
        self.proxy = ''
        self.user_name = ''
        self.capital_flow = 0
        self.capital_return = 0
        self.sports = 0
        self.table = 0
        self.slot_machine = 0
        self.lottery = 0
        self.fishing_machine = 0
        self.poker = 0

    def __str__(self):
        string = "代理：{0:<15} 用户名：{1:<15}总流水：{2:<10} 反水：{3:<10} 体育：{4:<10} 视讯：{5:<10} 老虎机：" \
                 "{6:<10} 彩票：{7:<10} 鲨鱼机：{8:<10} 棋牌：{9:<10}"
        return string.format(self.proxy, self.user_name, self.capital_flow, self.capital_return, self.sports,
                             self.table, self.slot_machine, self.lottery, self.fishing_machine, self.poker)


class DataAdmin(ModelAdmin):
    model = DataIndexPage
    menu_label = '源数据分析'
    menu_icon = 'table'
    list_display = ('proxy', 'user', 'capital_flow', 'capital_return', 'sports',
                    'table', 'slot_machine', 'lottery', 'fishing_machine',
                    'poker', 'date')
    search_fields = ('proxy', 'user', 'date')


class OneYearAdmin(ModelAdmin):
    model = OneYearDataStatistic
    menu_label = '一年数据分析'
    menu_icon = 'table'
    list_display = ('proxy', 'user', 'capital_flow', 'capital_return', 'sports',
                    'table', 'slot_machine', 'lottery', 'fishing_machine',
                    'poker', )

    search_fields = ('proxy', 'user',)


class HalfYearAdmin(ModelAdmin):
    model = HalfYearDataStatistic
    menu_label = '半年数据分析'
    menu_icon = 'table'
    list_display = ('proxy', 'user', 'capital_flow', 'capital_return', 'sports',
                    'table', 'slot_machine', 'lottery', 'fishing_machine',
                    'poker', )

    search_fields = ('proxy', 'user',)


class MonthAdmin(ModelAdmin):
    model = MonthDataStatistic
    menu_label = '月数据分析'
    menu_icon = 'table'
    list_display = ('proxy', 'user', 'capital_flow', 'capital_return', 'sports',
                    'table', 'slot_machine', 'lottery', 'fishing_machine',
                    'poker', )
    search_fields = ('proxy', 'user',)


class LibraryGroup(ModelAdminGroup):
    menu_label = '流水数据'
    menu_icon = 'table'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (DataAdmin, MonthAdmin, HalfYearAdmin, OneYearAdmin)


modeladmin_register(LibraryGroup)


def flush_month_data(user_name, proxy):
    """
    # 美东时间 06-01 开始 一月流水

    :param user_name:
    :param proxy:
    :return:
    """
    tz = pytz.timezone('America/New_York')
    now = datetime.datetime.now(tz)
    delta = datetime.timedelta(days=-30)
    n_days = now + delta

    source_data = DataIndexPage.objects.filter(user__exact=user_name).filter(date__gte=n_days)
    user = User()
    user.user_name = user_name
    user.proxy = proxy
    for source in source_data:
        user.capital_flow = float(Decimal(source.capital_flow + user.capital_flow).quantize(Decimal('0.00')))
        user.capital_return = float(Decimal(source.capital_return + user.capital_return).quantize(Decimal('0.00')))
        user.sports = float(Decimal(source.sports + user.sports).quantize(Decimal('0.00')))
        user.table = float(Decimal(source.table + user.table).quantize(Decimal('0.00')))
        user.slot_machine = float(Decimal(source.slot_machine + user.slot_machine).quantize(Decimal('0.00')))
        user.lottery = float(Decimal(source.lottery + user.lottery).quantize(Decimal('0.00')))
        user.fishing_machine = float(Decimal(source.fishing_machine + user.fishing_machine).quantize(Decimal('0.00')))
        user.poker = float(Decimal(source.poker + user.poker).quantize(Decimal('0.00')))
    # print(user)
    MonthDataStatistic.objects.filter(user__exact=user.user_name).delete()

    source_data = MonthDataStatistic(
        proxy=user.proxy,
        user=user.user_name,
        capital_flow=user.capital_flow,
        capital_return=user.capital_return,
        sports=user.sports,
        table=user.table,
        slot_machine=user.slot_machine,
        lottery=user.lottery,
        fishing_machine=user.fishing_machine,
        poker=user.poker,
    )
    source_data.save()


def flush_half_data(user_name, proxy):
    """
    # 美东时间 06-01 开始 半年时间的流水
    # todo
    :param user_name:
    :param proxy:
    :return:
    """
    tz = pytz.timezone('America/New_York')
    now = datetime.datetime.now(tz)
    delta = relativedelta(months=-6)
    n_days = now + delta
    source_data = DataIndexPage.objects.filter(user__exact=user_name).filter(date__gte=n_days)
    user = User()
    user.user_name = user_name
    user.proxy = proxy
    for source in source_data:
        user.capital_flow = float(Decimal(source.capital_flow + user.capital_flow).quantize(Decimal('0.00')))
        user.capital_return = float(Decimal(source.capital_return + user.capital_return).quantize(Decimal('0.00')))
        user.sports = float(Decimal(source.sports + user.sports).quantize(Decimal('0.00')))
        user.table = float(Decimal(source.table + user.table).quantize(Decimal('0.00')))
        user.slot_machine = float(Decimal(source.slot_machine + user.slot_machine).quantize(Decimal('0.00')))
        user.lottery = float(Decimal(source.lottery + user.lottery).quantize(Decimal('0.00')))
        user.fishing_machine = float(Decimal(source.fishing_machine + user.fishing_machine).quantize(Decimal('0.00')))
        user.poker = float(Decimal(source.poker + user.poker).quantize(Decimal('0.00')))
    # print(user)
    HalfYearDataStatistic.objects.filter(user__exact=user.user_name).delete()

    source_data = HalfYearDataStatistic(
        proxy=user.proxy,
        user=user.user_name,
        capital_flow=user.capital_flow,
        capital_return=user.capital_return,
        sports=user.sports,
        table=user.table,
        slot_machine=user.slot_machine,
        lottery=user.lottery,
        fishing_machine=user.fishing_machine,
        poker=user.poker,
    )
    source_data.save()


def flush_year_data(user_name, proxy):
    """
    # 美东时间 06-01 开始 一年时间的流水
    # todo
    :param user_name:
    :param proxy:
    :return:
    """
    tz = pytz.timezone('America/New_York')
    now = datetime.datetime.now(tz)
    delta = relativedelta(years=-1)
    n_days = now + delta
    source_data = DataIndexPage.objects.filter(user__exact=user_name).filter(date__gte=n_days)
    user = User()
    user.user_name = user_name
    user.proxy = proxy
    for source in source_data:
        user.capital_flow = float(Decimal(source.capital_flow + user.capital_flow).quantize(Decimal('0.00')))
        user.capital_return = float(Decimal(source.capital_return + user.capital_return).quantize(Decimal('0.00')))
        user.sports = float(Decimal(source.sports + user.sports).quantize(Decimal('0.00')))
        user.table = float(Decimal(source.table + user.table).quantize(Decimal('0.00')))
        user.slot_machine = float(Decimal(source.slot_machine + user.slot_machine).quantize(Decimal('0.00')))
        user.lottery = float(Decimal(source.lottery + user.lottery).quantize(Decimal('0.00')))
        user.fishing_machine = float(Decimal(source.fishing_machine + user.fishing_machine).quantize(Decimal('0.00')))
        user.poker = float(Decimal(source.poker + user.poker).quantize(Decimal('0.00')))
    # print(user)
    OneYearDataStatistic.objects.filter(user__exact=user.user_name).delete()

    source_data = OneYearDataStatistic(
        proxy=user.proxy,
        user=user.user_name,
        capital_flow=user.capital_flow,
        capital_return=user.capital_return,
        sports=user.sports,
        table=user.table,
        slot_machine=user.slot_machine,
        lottery=user.lottery,
        fishing_machine=user.fishing_machine,
        poker=user.poker,
    )
    source_data.save()


def flush_points_analysis(user_name):
    """
    导入积分计算表
    :return:
    """
    user_total_data = OneYearDataStatistic.objects.filter(user__exact=user_name)[0]
    user_half_data = HalfYearDataStatistic.objects.filter(user__exact=user_name)[0]
    user_month_data = MonthDataStatistic.objects.filter(user__exact=user_name)[0]
    x = Points.objects.filter(user_name__exact=user_name)
    if len(x) == 0:
        p = Points(
            user_name=user_name,
            one_year_capital_flow=user_total_data.capital_flow,
            half_year_capital_flow=user_half_data.capital_flow,
            one_month_capital_flow=user_month_data.capital_flow,
            one_year_lottery=user_total_data.lottery,
            half_year_lottery=user_half_data.lottery,
            month_lottery=user_month_data.lottery
        )
        p.save()
    else:
        Points.objects.filter(user_name__exact=user_name).update(
            one_year_capital_flow=user_total_data.capital_flow,
            half_year_capital_flow=user_half_data.capital_flow,
            one_month_capital_flow=user_month_data.capital_flow,
            one_year_lottery=user_total_data.lottery,
            half_year_lottery=user_half_data.lottery,
            month_lottery=user_month_data.lottery
        )


def insert_source_data_first(user, date):
    source_data_old = DataIndexPage.objects.filter(user__exact=user.user_name).filter(date=date)
    #print(user, date)
    if len(source_data_old) == 0:
        source_data = DataIndexPage(
            proxy=user.proxy,
            user=user.user_name,
            capital_flow=user.capital_flow,
            capital_return=user.capital_return,
            sports=user.sports,
            table=user.table,
            slot_machine=user.slot_machine,
            lottery=user.lottery,
            fishing_machine=user.fishing_machine,
            poker=user.poker,
            date=date
        )
        source_data.save()
        print(user, date)
    else:
        # 如果有数据 当天全部删除 重新覆盖
        DataIndexPage.objects.filter(date=date).delete()
        source_data = DataIndexPage(
            proxy=user.proxy,
            user=user.user_name,
            capital_flow=user.capital_flow,
            capital_return=user.capital_return,
            sports=user.sports,
            table=user.table,
            slot_machine=user.slot_machine,
            lottery=user.lottery,
            fishing_machine=user.fishing_machine,
            poker=user.poker,
            date=date
        )
        source_data.save()
    flush_month_data(user.user_name, user.proxy)
    flush_half_data(user.user_name, user.proxy)
    flush_year_data(user.user_name, user.proxy)
    flush_points_analysis(user.user_name)


def insert_source_data_second(user, date):
    print(user, date)
    source_data_old = DataIndexPage.objects.filter(user__exact=user.user_name).filter(date=date)
    if len(source_data_old) == 0:
        source_data = DataIndexPage(
            proxy=user.proxy,
            user=user.user_name,
            capital_flow=user.capital_flow,
            capital_return=user.capital_return,
            sports=user.sports,
            table=user.table,
            slot_machine=user.slot_machine,
            lottery=user.lottery,
            fishing_machine=user.fishing_machine,
            poker=user.poker,
            date=date
        )
        source_data.save()
    else:
        source_data = DataIndexPage(
            proxy=user.proxy,
            user=user.user_name,
            capital_flow=Decimal(float(user.capital_flow) +
                                 source_data_old[0].capital_flow).quantize(Decimal('0.00')),
            capital_return=Decimal(float(user.capital_return) +
                                   source_data_old[0].capital_return).quantize(Decimal('0.00')),
            sports=Decimal(float(user.sports) +
                           source_data_old[0].sports).quantize(Decimal('0.00')),
            table=Decimal(float(user.table) +
                          source_data_old[0].table).quantize(Decimal('0.00')),
            slot_machine=Decimal(float(user.slot_machine) +
                                 source_data_old[0].slot_machine).quantize(Decimal('0.00')),
            lottery=Decimal(float(user.lottery) +
                            source_data_old[0].lottery).quantize(Decimal('0.00')),
            fishing_machine=Decimal(float(user.fishing_machine) +
                                    source_data_old[0].fishing_machine).quantize(Decimal('0.00')),
            poker=Decimal(float(user.poker) +
                          source_data_old[0].poker).quantize(Decimal('0.00')),
            date=date
        )
        source_data.save()
    flush_month_data(user.user_name, user.proxy)
    flush_half_data(user.user_name, user.proxy)
    flush_year_data(user.user_name, user.proxy)
    flush_points_analysis(user.user_name)


def admin_view(request):
    filename = str(request.path).split('/')[3]
    # 判断文件是否全部上传
    if filename.endswith('02.xls'):
        date = filename.replace('-02.xls', '')
        other_name = filename.replace('02.xls', '01.xls')
        if os.path.exists('media/documents/%s' % other_name) is False:
            message = {
                'result': '文件 %s 缺失，需要同时上传两个平台的数据，请注意文件名' % other_name,
                'status': 0,
            }
            return JsonResponse(message)
    else:
        date = filename.replace('-01.xls', '')
        other_name = filename.replace('01.xls', '02.xls')
        if os.path.exists('media/documents/%s' % other_name) is False:
            message = {
                'result': '文件 %s 缺失，需要同时上传两个平台的数据，请注意文件名' % other_name,
                'status': 0,
            }
            return JsonResponse(message)

    try:
        # 先读取第一个文件
        dom_tree = parse('media/documents/%s-01.xls' % date)
        collection = dom_tree.documentElement
        rows = collection.getElementsByTagName("Row")
        first_row = rows[0].getElementsByTagName("Data")
        address_sports = []
        address_table = []
        address_slot = []
        address_lottery = []
        address_fishing = []
        address_poker = []
        ip = 0
        for cell in first_row:
            name = str(cell.firstChild.data)
            if name.startswith('体育赛事') and name.endswith('有效投注'):
                address_sports.append(ip)
            elif name.startswith('视讯直播') and name.endswith('有效投注'):
                address_table.append(ip)
            elif name.startswith('电子游艺') and name.endswith('有效投注'):
                address_slot.append(ip)
            elif name.startswith('彩票游戏') and name.endswith('有效投注'):
                address_lottery.append(ip)
            elif name.startswith('捕鱼机') and name.endswith('有效投注'):
                address_fishing.append(ip)
            elif name.startswith('棋牌游戏') and name.endswith('有效投注'):
                address_poker.append(ip)
            ip += 1
        temp_row = 0
        for row in rows:
            if temp_row == 0:
                # 第一行过滤
                temp_row += 1
                continue
            all_data = row.getElementsByTagName("Data")
            user = User()
            user.proxy = all_data[0].firstChild.data
            user.user_name = all_data[1].firstChild.data
            user.capital_flow = all_data[3].firstChild.data
            user.capital_return = all_data[4].firstChild.data

            # 数据处理
            data_temp = 0

            for data in all_data:

                if data_temp in address_sports:
                    user.sports += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_table:
                    user.table += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_slot:
                    user.slot_machine += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_lottery:
                    user.lottery += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_fishing:
                    user.fishing_machine += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_poker:
                    user.poker += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                data_temp += 1
            # 行号 +1
            temp_row += 1
            # 插入源数据
            insert_source_data_first(user, date)

        # 然后读取第二个文件
        dom_tree = parse('media/documents/%s-02.xls' % date)
        collection = dom_tree.documentElement
        rows = collection.getElementsByTagName("Row")
        first_row = rows[0].getElementsByTagName("Data")
        address_sports = []
        address_table = []
        address_slot = []
        address_lottery = []
        address_fishing = []
        address_poker = []
        ip = 0
        for cell in first_row:
            name = str(cell.firstChild.data)
            if name.startswith('体育赛事') and name.endswith('有效投注'):
                address_sports.append(ip)
            elif name.startswith('视讯直播') and name.endswith('有效投注'):
                address_table.append(ip)
            elif name.startswith('电子游艺') and name.endswith('有效投注'):
                address_slot.append(ip)
            elif name.startswith('彩票游戏') and name.endswith('有效投注'):
                address_lottery.append(ip)
            elif name.startswith('捕鱼机') and name.endswith('有效投注'):
                address_fishing.append(ip)
            elif name.startswith('棋牌游戏') and name.endswith('有效投注'):
                address_poker.append(ip)
            ip += 1
        temp_row = 0
        for row in rows:
            if temp_row == 0:
                # 第一行过滤
                temp_row += 1
                continue
            all_data = row.getElementsByTagName("Data")
            user = User()
            user.proxy = all_data[0].firstChild.data
            user.user_name = all_data[1].firstChild.data
            user.capital_flow = all_data[3].firstChild.data
            user.capital_return = all_data[4].firstChild.data

            # 数据处理
            data_temp = 0

            for data in all_data:

                if data_temp in address_sports:
                    user.sports += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_table:
                    user.table += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_slot:
                    user.slot_machine += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_lottery:
                    user.lottery += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                elif data_temp in address_fishing:
                    user.fishing_machine += Decimal.from_float(float(data.firstChild.data)).quantize(
                        Decimal('0.00'))
                elif data_temp in address_poker:
                    user.poker += Decimal.from_float(float(data.firstChild.data)).quantize(Decimal('0.00'))
                data_temp += 1
            # 行号 +1
            temp_row += 1
            # 插入源数据
            insert_source_data_second(user, date)

    except Exception as e:
        traceback.print_exc(e)
        message = {
            'result': '文件 %s 错误，请检查数据文件' % other_name,
            'status': 0,
        }
        return JsonResponse(message)

    message = {
        'result': filename,
        'status': 1,
    }
    return JsonResponse(message)


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^deal/[\d\-]+.xls', admin_view)
    ]

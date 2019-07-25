from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import VipList, VipSetting
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.core import hooks
from django.conf.urls import url
from django.http import JsonResponse
from data.models import MonthDataStatistic


class VipAdmin(ModelAdmin):
    model = VipList
    menu_label = 'VIP客户管理'
    menu_icon = 'group'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('user_id', 'user_level', '会员等级',
                    'current_level_up_money', 'flag_money')
    list_filter = ('flag_money', 'user_level')
    search_fields = ('user_id', 'user_name', 'user_level')


class SetAdmin(ModelAdmin):
    model = VipSetting
    menu_label = 'VIP优惠设置'
    menu_icon = 'cogs'
    list_display = ('vip_valid', 'common_valid', 'level_up_one', 'level_up_two', 'level_up_three', 'level_up_four',
                    'level_up_five', 'level_up_six')


class LibraryGroup(ModelAdminGroup):
    menu_label = 'VIP管理'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (VipAdmin, SetAdmin)


modeladmin_register(LibraryGroup)


def init_vip_data(request):
    """
    导入VIP数据
    :param request:
    :return:
    """
    data = open('viplist/vip.txt', 'r', encoding='utf-8')
    for line in data:
        array = line.split(' ')
        VipList.objects.filter(user_id__exact=array[0]).delete()
        v = VipList(
            user_id=str(array[0]).lower(),
            user_name=array[1],
            user_level=array[2].strip(),
            shop_level=0,
            level_up=0,
            flag_level=0,
            flag_money=0,
            current_level_up_money=0,
        )
        v.save()
    return JsonResponse({'status': 'success'})


def flush_vip_data(request):
    up_money = VipSetting.objects.all()[0]
    y = [
        up_money.level_up_one,
        up_money.level_up_two,
        up_money.level_up_three,
        up_money.level_up_four,
        up_money.level_up_five,
        up_money.level_up_six,
    ]

    all_data = MonthDataStatistic.objects.all()
    for line in all_data:
        x1 = int(line.capital_flow)
        x2 = int(line.slot_machine)
        if x1 < 500000:
            level_1 = 0
        elif x1 < 2000000:
            level_1 = 1
        elif x1 < 5000000:
            level_1 = 2
        elif x1 < 8000000:
            level_1 = 3
        elif x1 < 10000000:
            level_1 = 4
        else:
            level_1 = 5

        if x2 < 200000:
            level_2 = 0
        elif x2 < 1200000:
            level_2 = 1
        elif x2 < 3000000:
            level_2 = 2
        elif x2 < 5000000:
            level_2 = 3
        elif x2 < 6000000:
            level_2 = 4
        else:
            level_2 = 5
        level = max([level_1, level_2])
        print('用户名：%s 总流水：%s  老虎机流水%s  计算等级：%s' % (line.user, line.capital_flow, line.slot_machine, level))

        v = VipList.objects.filter(user_id__exact=line.user)
        if len(v) == 0:     #无数据
            if level == 1:
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b100000,
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[0]
                )
                target.save()
            elif level == 2:
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b010000,
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[1]
                )
                target.save()
            elif level == 3:
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b001000,
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[2]
                )
                target.save()
            elif level == 4:
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b000100,
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[3]
                )
                target.save()
            elif level == 5:
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b000010,
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[4]
                )
                target.save()
        else:       # 有数据
            if v[0].user_level == '大客层':
                if x1 < 1500000:
                    v.update(
                        shop_level=5,
                        level_up=0b111111,
                        flag_level=1,
                        flag_money=0,
                        current_level_up_money=0
                    )
                else:
                    v.update(
                        shop_level=6,
                        level_up=0b111111,
                        flag_level=1,
                        flag_money=0,
                        current_level_up_money=0
                    )
            elif v[0].user_level in ['第十二层', '第十层', '永利博VIP']:
                if x1 < 1000000 and x2 < 6000000:
                    v.update(
                        shop_level=4,
                        level_up=0b111110,
                        flag_level=1,
                        flag_money=0,
                        current_level_up_money=0
                    )
                else:
                    v.update(
                        shop_level=5,
                        level_up=0b111110,
                        flag_level=1,
                        flag_money=0,
                        current_level_up_money=0
                    )
            else:
                if level == 0:
                    continue
                elif level == 1:
                    v.update(
                        shop_level=level,
                        level_up=0b100000,
                        flag_level=1,
                        flag_money=1,
                        current_level_up_money=y[0]
                    )
                elif level == 2:
                    v.update(
                        shop_level=level,
                        level_up=0b010000,
                        flag_level=1,
                        flag_money=1,
                        current_level_up_money=y[1]
                    )
                elif level == 3:
                    v.update(
                        shop_level=level,
                        level_up=0b001000,
                        flag_level=1,
                        flag_money=1,
                        current_level_up_money=y[2]
                    )
                elif level == 4:
                    v.update(
                        shop_level=level,
                        level_up=0b000100,
                        flag_level=1,
                        flag_money=1,
                        current_level_up_money=y[3]
                    )
                elif level == 5:
                    v.update(
                        shop_level=level,
                        level_up=0b000010,
                        flag_level=1,
                        flag_money=1,
                        current_level_up_money=y[4]
                    )

    vip_data = VipList.objects.filter(current_level_up_money=0)
    for line in vip_data:
        if line.user_level == '大客层':
            VipList.objects.filter(user_id=line.user_id).update(
                shop_level=5,
                level_up=0b111111,
                flag_level=1,
                flag_money=0,
                current_level_up_money=0
            )
        elif line.user_level in ['第十二层', '第十层', '永利博VIP']:
            VipList.objects.filter(user_id=line.user_id).update(
                shop_level=4,
                level_up=0b111110,
                flag_level=1,
                flag_money=0,
                current_level_up_money=0
            )
    return JsonResponse({'status': 'success'})


@hooks.register('register_admin_urls')
def submit_query():
    return [
        url(r'init_vip_data/', init_vip_data)
    ]


@hooks.register('register_admin_urls')
def submit_query():
    return [
        url(r'flush_vip_data/', flush_vip_data)
    ]



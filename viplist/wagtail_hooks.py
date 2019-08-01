# -*- coding=utf-8 -*-
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import VipList, VipSetting
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


def init_vip_data():
    """
    导入VIP数据
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
    # all_data = MonthDataStatistic.objects.filter(user__exact='Thor')
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
        if len(v) == 0:
            if level == 0:      # 如果计算出来等级为0 同事列表里面又不存在 就什么都木有
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b000000,
                    flag_level=0,
                    flag_money=0,
                    current_level_up_money=0
                )
                target.save()
                print(1)
            else:
                # 没有记录 就是升级
                target = VipList(
                    user_id=line.user,
                    user_name='未知',
                    user_level='未知',
                    shop_level=level,
                    level_up=0b100000 >> (level - 1),
                    flag_level=1,
                    flag_money=1,
                    current_level_up_money=y[level - 1]
                )
                target.save()
                print(2)

        else:       # 有数据
            if v[0].user_level == '大客层':
                if level == 0:
                    v.update(
                        shop_level=v[0].shop_level - 1,  # 降级减一
                        level_up=0b111111,  # 不管是否升级 和之前的记录是一样的
                        flag_level=0,
                        flag_money=0,
                        current_level_up_money=0
                    )
                    print(3)
                else:
                    if v[0].shop_level > level:
                        # 降级
                        if v[0].shop_level == 1 and x1 < 50000 and x2 < 20000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 2 and x1 < 200000 and x2 < 120000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 3 and x1 < 500000 and x2 < 300000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 4 and x1 < 800000 and x2 < 500000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 5 and x1 < 1000000 and x2 < 600000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 6 and x1 < 1500000 and x2 < 1000000:
                            shop_level = v[0].shop_level - 1
                        else:
                            shop_level = v[0].shop_level
                    else:
                        # 升级
                        shop_level = level
                    current_flag_level = 0 if shop_level <= v[0].shop_level else 1  # 判定用户是否升级
                    v.update(
                        shop_level=shop_level,
                        level_up=0b111111,
                        flag_level=current_flag_level,
                        flag_money=0,
                        current_level_up_money=0
                    )
                    print(4)
            elif v[0].user_level in ['第十二层', '第十层', '永利博VIP']:
                if level == 0:
                    v.update(
                        shop_level=v[0].shop_level - 1,  # 降级减一
                        level_up=v[0].shop_level,   # 不管是否升级 和之前的记录是一样的
                        flag_level=0,
                        flag_money=0,
                        current_level_up_money=0
                    )
                    print(5)
                else:
                    if v[0].shop_level > level:
                        # 降级
                        if v[0].shop_level == 1 and x1 < 50000 and x2 < 20000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 2 and x1 < 200000 and x2 < 120000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 3 and x1 < 500000 and x2 < 300000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 4 and x1 < 800000 and x2 < 500000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 5 and x1 < 1000000 and x2 < 600000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 6 and x1 < 1500000 and x2 < 1000000:
                            shop_level = v[0].shop_level - 1
                        else:
                            shop_level = v[0].shop_level
                    else:
                        # 升级
                        shop_level = level
                    level_up = v[0].level_up
                    current_flag_level = 0 if shop_level <= v[0].shop_level else 1           # 判定用户是否升级
                    current_level_up = 0b100000 >> (level - 1) | level_up                    # 当前用户升级标识
                    current_status = 0b100000 >> (level - 1) & level_up
                    current_flag_money = 0 if current_status == (0b100000 >> (level - 1)) else 1    # 升级历史查询
                    #  不能领钱输出0
                    current_level_up_money = y[level - 1] if current_flag_level & current_flag_money else 0
                    v.update(
                        shop_level=shop_level,
                        level_up=current_level_up,
                        flag_level=current_flag_level,
                        flag_money=current_flag_money,
                        current_level_up_money=current_level_up_money
                    )
                    print(6)
            else:
                if level == 0:
                    v.update(
                        shop_level=v[0].shop_level - 1,  # 降级减一
                        level_up=v[0].shop_level,  # 不管是否升级 和之前的记录是一样的
                        flag_level=0,
                        flag_money=0,
                        current_level_up_money=0
                    )
                    print(7)
                else:
                    if v[0].shop_level > level:
                        # 降级
                        if v[0].shop_level == 1 and x1 < 50000 and x2 < 20000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 2 and x1 < 200000 and x2 < 120000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 3 and x1 < 500000 and x2 < 300000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 4 and x1 < 800000 and x2 < 500000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 5 and x1 < 1000000 and x2 < 600000:
                            shop_level = v[0].shop_level - 1
                        elif v[0].shop_level == 6 and x1 < 1500000 and x2 < 1000000:
                            shop_level = v[0].shop_level - 1
                        else:
                            shop_level = v[0].shop_level
                    else:
                        # 升级
                        shop_level = level
                    level_up = v[0].level_up
                    current_flag_level = 0 if shop_level <= v[0].shop_level else 1           # 判定用户是否升级
                    current_level_up = 0b100000 >> (level - 1) | level_up                    # 当前用户升级标识
                    current_status = 0b100000 >> (level - 1) & level_up
                    current_flag_money = 0 if current_status == (0b100000 >> (level - 1)) else 1    # 升级历史查询
                    #  不能领钱输出0
                    current_level_up_money = y[level - 1] if current_flag_level & current_flag_money else 0
                    v.update(
                        shop_level=shop_level,
                        level_up=current_level_up,
                        flag_level=current_flag_level,
                        flag_money=current_flag_money,
                        current_level_up_money=current_level_up_money
                    )
                    print(8)

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

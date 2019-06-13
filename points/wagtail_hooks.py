from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import (Cost, Points, Add, PointConfig)


class CostAdmin(ModelAdmin):
    model = Cost
    menu_label = '消费管理'
    menu_icon = 'list-ol'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('user_name', 'goods', 'change_points', 'tips', 'update_time')
    list_filter = ('user_name',)
    search_fields = ('user_name', 'change_points')


class PointsAdmin(ModelAdmin):
    model = Points
    menu_label = '用户管理'
    menu_icon = 'list-ol'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = (
        '游戏账号',
        'one_month_capital_flow',
        'half_year_capital_flow',
        'one_year_capital_flow',
        '当月异常流水',
        '当月流水',
        '半年流水',
        '一年流水',
        'vip',
        '商城等级',
        '总积分',
        '剩余积分')
    search_fields = ('user_name',)


class AddAdmin(ModelAdmin):
    model = Add
    menu_label = '增加管理'
    menu_icon = 'list-ol'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('user_name', 'capital_flow', 'tips', 'update_time')
    list_filter = ('user_name',)
    search_fields = ('user_name',)


class Config(ModelAdmin):
    model = PointConfig
    menu_label = '积分计算配置'
    menu_icon = 'list-ol'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = (
        'config_name',
        'water_to_point',
        'auto_flush',
    )


class LibraryGroup(ModelAdminGroup):
    menu_label = '积分'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CostAdmin, PointsAdmin, AddAdmin, Config)


modeladmin_register(LibraryGroup)

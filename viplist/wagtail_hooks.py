from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import VipList, VipSetting
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.core import hooks


class VipAdmin(ModelAdmin):
    model = VipList
    menu_label = 'VIP客户管理'
    menu_icon = 'group'
    # menu_order = 1000
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('游戏账号', '姓名', '官网VIP层级别')
    list_filter = ('user_level', )
    search_fields = ('user_id', 'user_name', 'user_level')


class SetAdmin(ModelAdmin):
    model = VipSetting
    menu_label = 'VIP积分有效期设置'
    menu_icon = 'cogs'
    list_display = ('vip_valid', 'common_valid')


class LibraryGroup(ModelAdminGroup):
    menu_label = 'VIP管理'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (VipAdmin, SetAdmin)


modeladmin_register(LibraryGroup)


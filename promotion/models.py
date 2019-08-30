# -*- coding:utf-8 -*-
from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
import requests


class PromotionSetting(models.Model):
    set_cookies = models.TextField(help_text='登录信息配置，详情问赵四')
    set_first_time = models.CharField(max_length=255, help_text='第一次活动开始时间')
    set_second_time = models.CharField(max_length=255, help_text='第二次活动开始时间')
    set_third_time = models.CharField(max_length=255, help_text='第三次活动开始时间')
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('set_cookies'),
        ], heading="登录信息配置"),
        MultiFieldPanel([
            FieldPanel('set_first_time'),
            FieldPanel('set_second_time'),
            FieldPanel('set_third_time'),
        ], heading="活动时间配置"),
    ]

    def check_cookie(self):
        try:
            url = 'https://bm168.bm168168.com/agv3/cl/?module=CashSystem&method=queryProject&sid='
            header = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '1072',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': self.set_cookies,
                'Host': 'bm168.bm168168.com',
                'Origin': 'https://bm168.bm168168.com',
                'Referer': 'https://bm168.bm168168.com/agv3/cl/index.php?module=CashSystem',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/75.0.3770.142 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }
            data = {
                'current': 'RMB',
                'sDate': '2019-08-02 00:00:00',
                'eDate': '2019-08-03 23:59:59',
                'MemNameSel': 'single',
                'mem_name': 'lanlan698',
                'betNum': '',
                'page': '',
                'Sort': '1',
                'm': '',
                'cid': '1,3,7,9,12,5,16',
            }
            response = requests.post(url, data=data, headers=header)
            req = response.json()
            print(req['INFO'])
            return 'cookie 正常 请放心使用！'

        except Exception as e:
            print(e)
            return 'cookie 失效 请重新设置！'


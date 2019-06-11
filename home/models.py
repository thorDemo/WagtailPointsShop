from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from mulu.models import GoodsPage, GoodsSortPage


class HomePage(Page):
    # parent_page_types = []
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        user = request.user
        children = GoodsPage.objects.live()[0:10]
        sort = GoodsSortPage.objects.live()[0:4]
        context['user'] = user
        context['children'] = children
        context['sort'] = sort
        return context

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from django.db import models


class YiwenIndexPage(Page):

    parent_page_types = ['home.HomePage']

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        brother = self.get_siblings()
        context['brother'] = brother
        user = request.user
        context['user'] = user
        first = self.get_first_child()
        grandson = first.get_children()
        context['first'] = first
        context['grandson'] = grandson
        return context


class TypeOfQuestion(Page):
    parent_page_types = ['yiwen.YiwenIndexPage']
    description = RichTextField(blank=True, help_text='疑问类别')

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        farther = self.get_parent()
        parent = farther.get_siblings()
        context['parent'] = parent
        brother = self.get_siblings()
        context['brother'] = brother
        #print(brother)
        user = request.user
        context['user'] = user
        return context


class Question(Page):
    parent_page_types = ['yiwen.TypeOfQuestion']
    description = models.CharField(max_length=250, default='')

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

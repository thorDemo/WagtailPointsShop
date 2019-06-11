from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from home.models import HomePage


class AboutsIndexPage(Page):

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
        return context

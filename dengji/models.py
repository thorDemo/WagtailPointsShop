from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from home.models import HomePage
from points.models import PointConfig


class DengjiIndexPage(Page):

    parent_page_types = ['home.HomePage']

    intro = RichTextField(blank=True)

    def get_context(self, request, *args, **kwargs):
        config = PointConfig.objects.get(id=1)
        context = super().get_context(request)
        # data = [
        #     {'level': round(config.discount_one_Percent*10, 2), 'water': config.discount_one_water, 'points': int(config.discount_one_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_two_Percent*10, 2), 'water': config.discount_two_water, 'points': int(config.discount_two_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_three_Percent*10, 2), 'water': config.discount_three_water, 'points': int(config.discount_three_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_four_Percent*10, 2), 'water': config.discount_four_water, 'points': int(config.discount_four_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_five_Percent*10, 2), 'water': config.discount_five_water, 'points': int(config.discount_five_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_six_Percent*10, 2), 'water': config.discount_six_water, 'points': int(config.discount_six_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_seven_Percent*10, 2), 'water': config.discount_seven_water, 'points': int(config.discount_seven_water)/int(config.water_to_point)},
        #     {'level': round(config.discount_eight_Percent*10, 2), 'water': config.discount_eight_water, 'points': int(config.discount_eight_water)/int(config.water_to_point)},
        # ]
        brother = self.get_siblings()
        context['brother'] = brother
        context['change'] = config.water_to_point
        user = request.user
        context['user'] = user
        # context['data'] = data
        return context
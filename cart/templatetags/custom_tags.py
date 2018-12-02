from django import template



register = template.Library()
from cart.models import cart



@register.simple_tag(takes_context=True)
def any_function(context):
    return cart.objects.get_or_create(context.get('request'))
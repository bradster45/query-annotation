from django import template

register = template.Library()

@register.filter
def strip_0(float_value):
    return(float_value.rstrip('.0'))

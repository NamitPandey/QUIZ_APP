from django import template
from django.template.defaultfilters import stringfilter
import calendar
register = template.Library()

""" THE FILTER WILL ONLY ACCEPT STRING VALUE"""
@register.filter(name='replace')
@stringfilter
def replace_var(value):
    """REMOVE ALL UNDERSCORE WITH SPACE"""

    return value.replace("_", ' ')


""" FILETER WILL INCREMENT THE VALUE BY 1 TO ANY GIVEN VALUE """
@register.filter(name='addPage')
@stringfilter
def replace_var(value):

    return int(value)+1

""" FILETER WILL DECREMENT THE VALUE BY 1 TO ANY GIVEN VALUE """
@register.filter(name='subPage')
@stringfilter
def replace_var(value):
    """REMOVE ALL UNDERSCORE WITH SPACE"""

    return int(value)-1

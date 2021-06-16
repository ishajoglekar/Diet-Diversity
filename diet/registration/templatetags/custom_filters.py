from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def getValue(value):
    #removing  /
    value = value.split('/')[-1]
    
    #removing .
    value = value.split('.')[0]

    return value.capitalize()
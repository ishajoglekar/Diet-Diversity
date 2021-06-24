from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
#used to display labels for radio button with images
def getValue(value):
    #removing  /

    value = value.split('/')[-1]
    
    #removing .
    value = value.split('.')[0]

    return value.capitalize()
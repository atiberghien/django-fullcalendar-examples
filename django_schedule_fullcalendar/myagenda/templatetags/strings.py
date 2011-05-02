import re

from django import template
register = template.Library()

@register.filter
def replace (string, args):
    find, replace = args.split(',')
    return string.replace(find, replace)

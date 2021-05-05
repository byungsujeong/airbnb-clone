from django import template

register = template.Library()


@register.filter
def func(value):
    return value
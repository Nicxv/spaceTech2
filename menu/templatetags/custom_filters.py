# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    return f"${value:,.0f}".replace(",", ".")

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key, 0)

@register.filter(name='get_value_from_dict')
def get_value_from_dict(dictionary, key):
    return dictionary.get(key, 0)

# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='uppercase')
def uppercase(value):
    """Convierte el valor a mayúsculas"""
    return value.upper()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})
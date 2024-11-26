# custom_filters.py
from django import template
import re

register = template.Library()

@register.filter(name='uppercase')
def uppercase(value):
    """Convierte el valor a mayúsculas"""
    return value.upper()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter(name='parse_images')
def parse_images(value):
    """
    Reemplaza las imágenes en formato ![Imagen](url) por etiquetas <img src="url" />
    """
    image_pattern = r'!\[([^\]]+)\]\((https?://[^\)]+)\)'  # Expresión regular para detectar ![alt](url)
    return re.sub(image_pattern, r'<img src="\2" alt="\1" />', value)
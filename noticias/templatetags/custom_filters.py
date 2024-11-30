# custom_filters.py
from django import template
import re

register = template.Library()


@register.filter(name="uppercase")
def uppercase(value):
    """Convierte el valor a mayúsculas"""
    return value.upper()


@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name="parse_images")
def parse_images(value):
    """
    Reemplaza las imágenes en formato ![Imagen](url) por etiquetas <img src="url" />
    """
    image_pattern = r"!\[([^\]]+)\]\((https?://[^\)]+)\)"  # Expresión regular para detectar ![alt](url)
    return re.sub(image_pattern, r'<img src="\2" alt="\1" />', value)
@register.filter
def youtube_embed(value):
    """
    Convierte una URL de YouTube estándar en una URL de embed.
    """
    if "youtube.com/watch?v=" in value:
        return value.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
    elif "youtu.be/" in value:
        return value.replace("https://youtu.be/", "https://www.youtube.com/embed/")
    return value

@register.filter(name='replace')
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)
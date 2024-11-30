from django import template

register = template.Library()

@register.filter
def strip_twitch(url):
    return url.replace("https://www.twitch.tv/", "")

@register.filter
def strip_youtube(url):
    return url.replace("https://www.youtube.com/@", "")
from django.contrib import admin
from .models import Evento
from django.contrib.admin import ModelAdmin

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'autor')
    list_display_links = ('titulo',)
    search_fields = ('titulo', 'contenido')


from django.contrib import admin
from .models import Evento
from django.contrib.admin import ModelAdmin


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'primer_lugar', 'segundo_lugar', 'tercer_lugar')
    fields = ('titulo', 'fecha', 'direccion', 'contenido', 'imagen', 'primer_lugar', 'segundo_lugar', 'tercer_lugar')

admin.site.register(Evento, EventoAdmin)
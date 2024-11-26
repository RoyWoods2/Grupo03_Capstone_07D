from django.contrib import admin
from .models import Evento
from django.contrib.admin import ModelAdmin

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'direccion')
    fields = (
        'titulo', 'fecha', 'contenido', 'autor', 'imagen', 'direccion',
        'primer_lugar', 'premio_primer_lugar',
        'segundo_lugar', 'premio_segundo_lugar',
        'tercer_lugar', 'premio_tercer_lugar'
    )

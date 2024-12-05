from django.contrib import admin
from .models import Evento,TorneoComunitario,InscripcionTorneo,Match
from django.contrib.admin import ModelAdmin


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "direccion")
    fields = (
        "titulo",
        "fecha",
        "contenido",
        "autor",
        "imagen",
        "direccion",
        "primer_lugar",
        "premio_primer_lugar",
        "segundo_lugar",
        "premio_segundo_lugar",
        "tercer_lugar",
        "premio_tercer_lugar",
    )

@admin.register(TorneoComunitario)
class TorneoComunitarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'tipo_torneo', 'organizador')  # Cambiado 'tipo' a 'tipo_torneo'.
    list_filter = ('tipo_torneo',)  # Cambiado 'tipo' a 'tipo_torneo'.
    search_fields = ('titulo', 'organizador__nick')

@admin.register(InscripcionTorneo)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('torneo', 'participante', 'fecha_inscripcion')  # Cambiado 'usuario' a 'participante'.
    search_fields = ('participante__nick', 'torneo__titulo')
    list_filter = ('torneo',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('torneo', 'jugador1', 'jugador2', 'marcador_jugador1', 'marcador_jugador2', 'ganador', 'ronda')
    search_fields = ('jugador1__nick', 'jugador2__nick', 'torneo__titulo')
    list_filter = ('torneo', 'ronda')
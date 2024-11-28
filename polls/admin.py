from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from django.db.models import Count
from django.urls import path
from django.shortcuts import render
from django.db import models


# Modelos
from .models import (
    Juego,
    Personaje,
    Combo,
    Hub,
    CustomUser,
    Comentario,
    FrameData,
    Estrategia,
    Recurso,
    Glosario,
    PersonajeVisita,
)


# Clase de administración para 'Estrategia'
@admin.register(Estrategia)
class EstrategiaAdmin(admin.ModelAdmin):
    list_display = ["personaje", "tacticas_generales", "posicionamiento_en_el_equipo"]
    search_fields = ["personaje__nombre"]
    list_filter = ["personaje"]  # Filtro por personaje


# Clase de administración para 'Comentario'
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "contenido", "fecha_publicacion")
    search_fields = ("usuario__username", "contenido")
    list_filter = ("fecha_publicacion",)  # Filtro por fecha


# Clase de administración para 'Juego'
class JuegoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    list_display = ("nombre", "slug")
    search_fields = ("nombre",)
    list_filter = ("nombre",)  # Filtro por nombre de juego


class PersonajeAdmin(admin.ModelAdmin):
    def obtener_datos_grafico(self, request):
        data = (
            PersonajeVisita.objects.values("personaje__nombre", "juego__nombre")
            .annotate(visitas=Count("id"))
            .order_by("-visitas")
        )
        formatted_data = {}
        for item in data:
            juego = item["juego__nombre"]
            if juego not in formatted_data:
                formatted_data[juego] = {"labels": [], "data": []}
            formatted_data[juego]["labels"].append(item["personaje__nombre"])
            formatted_data[juego]["data"].append(item["visitas"])
        return JsonResponse(formatted_data)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "grafico_datos/",
                self.admin_site.admin_view(self.obtener_datos_grafico),
                name="grafico_datos",
            ),
        ]
        return custom_urls + urls


# Clase de administración personalizada para 'CustomUser'
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Limpiar el 'fieldsets' por defecto para evitar la pestaña duplicada
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Datos Personales ",
            {"fields": ("first_name", "last_name", "email", "nick", "avatar")},
        ),
        (
            "Atributos Adicionales",
            {
                "fields": (
                    "user_type",
                    "puntos",
                    "juegos_competencia",
                    "tipo_usuario_solicitado",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "nick", "avatar")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Definir los campos que aparecerán en la lista de usuarios en el admin
    list_display = ("nick", "email", "user_type", "puntos")


# Registro de modelos con administración personalizada
admin.site.register(Juego, JuegoAdmin)
admin.site.register(Combo)
admin.site.register(Hub)
admin.site.register(FrameData)
admin.site.register(Recurso)
admin.site.register(Glosario)
admin.site.register(CustomUser, CustomUserAdmin)

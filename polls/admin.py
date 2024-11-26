from django.contrib import admin

# Register your models here.
from .models import Juego, Personaje, Combo, Hub, CustomUser, Comentario, FrameData,Estrategia, Recurso

from django.contrib.auth.admin import UserAdmin

@admin.register(Estrategia)
class EstrategiaAdmin(admin.ModelAdmin):
    list_display = ['personaje', 'tacticas_generales', 'posicionamiento_en_el_equipo']
    search_fields = ['personaje__nombre']
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_publicacion')
    search_fields = ('usuario__username', 'contenido')

class JuegoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

class PersonajeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'juego', 'imagen')

    def imagen(self, obj):
        if obj.imagen:  # Suponiendo que 'imagen' es un campo en tu modelo
            return format_html('<img src="{}" width="50"/>', obj.imagen.url)
        return "No Image"
    imagen.short_description = "Imagen"
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nick', 'avatar', 'juegos_competencia','puntos', 'user_type', 'tipo_usuario_solicitado')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nick', 'avatar', 'juegos_competencia', 'puntos','user_type', 'tipo_usuario_solicitado')}),
    )
    

admin.site.register(Juego, JuegoAdmin)
admin.site.register(Personaje, PersonajeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Combo)
admin.site.register(Hub)
admin.site.register(FrameData)
admin.site.register(Recurso)


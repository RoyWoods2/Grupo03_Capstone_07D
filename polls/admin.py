from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Comentario
from .models import Juego, Personaje


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_publicacion')
    search_fields = ('usuario__username', 'contenido')

class JuegoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

class PersonajeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

admin.site.register(Juego, JuegoAdmin)
admin.site.register(Personaje, PersonajeAdmin)
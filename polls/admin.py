from django.contrib import admin

# Register your models here.
from .models import CustomUser, Comentario, Juego, Personaje, FrameData, Combo, Hub
from django.contrib.auth.admin import UserAdmin


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_publicacion')
    search_fields = ('usuario__username', 'contenido')

class JuegoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

class PersonajeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nick', 'avatar', 'juegos_competencia', 'user_type', 'tipo_usuario_solicitado')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nick', 'avatar', 'juegos_competencia', 'user_type', 'tipo_usuario_solicitado')}),
    )

admin.site.register(Juego, JuegoAdmin)
admin.site.register(Personaje, PersonajeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FrameData)
admin.site.register(Combo) 
admin.site.register(Hub)  
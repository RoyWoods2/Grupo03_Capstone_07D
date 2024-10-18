from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Question

admin.site.register(Question)

from django.contrib import admin
from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_publicacion')
    search_fields = ('usuario__username', 'contenido')

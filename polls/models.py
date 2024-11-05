import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




# Create your models here.


from django.db import models

class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    imagen_url =  models.ImageField(upload_to='polls/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(Juego, self).save(*args, **kwargs)
    def __str__(self):
        return self.nombre

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='personajes')
    pros = models.JSONField(default=dict, blank=True)
    cons = models.JSONField(default=dict, blank=True)
    imagen = models.ImageField(upload_to='personajes/', blank=True, null=True)
    icono_url =  models.ImageField(upload_to='personajes/')
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(Personaje, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.nombre} ({self.juego.nombre})"

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='respuestas', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.usuario} - {self.contenido[:20]}'
    def es_respuesta(self):
        """ Verifica si el comentario es una respuesta a otro comentario """
        return self.parent is not None

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nick


    
    
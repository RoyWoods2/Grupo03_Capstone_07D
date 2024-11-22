import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from noticias.models import Noticia
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL
from eventos.models import Evento



# Create your models here.
class EventoInteresado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_interesado = models.DateTimeField(auto_now_add=True)
    
class CustomUser(AbstractUser):
    nick = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    juegos_competencia = models.TextField(blank=True)  # Lista de juegos en los que compite
    user_type = models.CharField(max_length=50, default='normal')
    tipo_usuario_solicitado = models.CharField(max_length=50, blank=True, null=True)  # Para solicitud de cambio

    def __str__(self):
        return self.username
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('admin', 'Admin'),
        ('redactor', 'Redactor'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nick = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    juegos_competencia = models.TextField(blank=True)  # Lista de juegos
    tipo_usuario_solicitado = models.CharField(max_length=50, blank=True, null=True)  # Solicitud pendiente

    def __str__(self):
        return self.user.username




class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    publisher = models.TextField(blank=True)
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
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    respuesta_a = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="respuestas")

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.noticia}"
    def es_respuesta(self):
        """ Verifica si el comentario es una respuesta a otro comentario """
        return self.parent is not None
    
class Combo(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="combos")
    nombre = models.CharField(max_length=100, help_text="Nombre o etiqueta del combo (por ejemplo, 'Bread and Butter Combo')")
    movimientos = models.TextField(help_text="Lista de movimientos en formato secuencial (ej. 'LP, MP, HP')")
    daño = models.IntegerField(help_text="Cantidad de daño que hace el combo", null=True, blank=True)
    dificultad = models.CharField(
        max_length=50, 
        choices=[('Fácil', 'Fácil'), ('Intermedio', 'Intermedio'), ('Difícil', 'Difícil')], 
        help_text="Dificultad del combo"
    )
    descripcion = models.TextField(help_text="Descripción o contexto del combo", blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text="Usuario que creó o compartió el combo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    video_demo_url = models.URLField(blank=True, null=True, help_text="URL a un video de demostración")  # Campo para el enlace de video

    def __str__(self):
        return f"{self.nombre} - {self.personaje.nombre}"

    class Meta:
        ordering = ["personaje", "dificultad", "-fecha_creacion"]
        
class FrameData(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="frame_data")
    movimiento = models.CharField(max_length=100)  # Nombre del movimiento
    tipo = models.CharField(max_length=50)  # Ej. 'Normal', 'Especial', 'Super'
    damage = models.IntegerField()  # Daño causado
    startup_frames = models.IntegerField()  # Cuadros de inicio
    active_frames = models.IntegerField()  # Cuadros activos
    recovery_frames = models.IntegerField()  # Cuadros de recuperación
    block_advantage = models.IntegerField()  # Ventaja en bloqueo
    hit_advantage = models.IntegerField()  # Ventaja en golpe
    knockdown = models.BooleanField(default=False)  # Indica si el movimiento derriba
    video_demo_url = models.URLField(blank=True, null=True)  # Enlace a video de demostración

    def __str__(self):
        return f"{self.personaje.nombre} - {self.movimiento}"

    
class Combo(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="combos")
    nombre = models.CharField(max_length=100, help_text="Nombre o etiqueta del combo (por ejemplo, 'Bread and Butter Combo')")
    movimientos = models.TextField(help_text="Lista de movimientos en formato secuencial (ej. 'LP, MP, HP')")
    daño = models.IntegerField(help_text="Cantidad de daño que hace el combo", null=True, blank=True)
    dificultad = models.CharField(
        max_length=50, 
        choices=[('Fácil', 'Fácil'), ('Intermedio', 'Intermedio'), ('Difícil', 'Difícil')], 
        help_text="Dificultad del combo"
    )
    descripcion = models.TextField(help_text="Descripción o contexto del combo", blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text="Usuario que creó o compartió el combo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    video_demo_url = models.URLField(blank=True, null=True, help_text="URL a un video de demostración")  # Campo para el enlace de video

    def __str__(self):
        return f"{self.nombre} - {self.personaje.nombre}"

    class Meta:
        ordering = ["personaje", "dificultad", "-fecha_creacion"]
        
class FrameData(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="frame_data")
    movimiento = models.CharField(max_length=100)  # Nombre del movimiento
    tipo = models.CharField(max_length=50)  # Ej. 'Normal', 'Especial', 'Super'
    damage = models.IntegerField()  # Daño causado
    startup_frames = models.IntegerField()  # Cuadros de inicio
    active_frames = models.IntegerField()  # Cuadros activos
    recovery_frames = models.IntegerField()  # Cuadros de recuperación
    block_advantage = models.IntegerField()  # Ventaja en bloqueo
    hit_advantage = models.IntegerField()  # Ventaja en golpe
    knockdown = models.BooleanField(default=False)  # Indica si el movimiento derriba
    video_demo_url = models.URLField(blank=True, null=True)  # Enlace a video de demostración

    def __str__(self):
        return f"{self.personaje.nombre} - {self.movimiento}"
    
class Hub(models.Model):
    titulo = models.CharField(max_length=100)  # Ejemplo: "Barra de vida"
    descripcion = models.TextField()  # Descripción del contenido
    imagen = models.ImageField(upload_to='hub_images/')  # Imagen asociada
    juego = models.ForeignKey('Juego', on_delete=models.CASCADE)  # Relación con el juego específico

    def __str__(self):
        return self.titulo                                                                                                                                                                                                                                                                                                                                                                                                                                                           
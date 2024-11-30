import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from noticias.models import Noticia
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL
from eventos.models import Evento


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario.")
        email = self.normalize_email(email)

        # Validar que el nick sea único antes de asignarlo
        nick = extra_fields.get(
            "nick", username
        )  # Usa `nick` si se proporciona, de lo contrario `username`
        if self.model.objects.filter(nick=nick).exists():
            raise ValueError(f"El nick '{nick}' ya está en uso.")

        user = self.model(username=username, email=email, nick=nick, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("normal", "Normal"),
        ("admin", "Admin"),
        ("redactor", "Redactor"),
        ("organizador", "Organizador"),
    ]

    nick = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        default="polls/css/images/default.png",
    )
    juegos_competencia = models.ManyToManyField(
        "Juego", blank=True
    )  # Aquí cambiamos a ManyToManyField
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="normal"
    )
    puntos = models.IntegerField(default=0)
    tipo_usuario_solicitado = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    personajes_favoritos = models.ManyToManyField('Personaje', blank=True, related_name='fans')
    videos_subidos = models.ManyToManyField('Recurso', blank=True, related_name='creadores')
    twitch_stream = models.URLField(blank=True, null=True, help_text="Enlace a tu canal de Twitch")
    youtube_channel = models.URLField(blank=True, null=True, help_text="Enlace a tu canal de YouTube")

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class EventoInteresado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_interesado = models.DateTimeField(auto_now_add=True)


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    publisher = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    imagen_url = models.ImageField(upload_to="polls/")
    enlace_oficial = models.TextField(blank=True)

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
    descripcion_strategy = models.TextField(blank=True)
    juego = models.ForeignKey(
        Juego, on_delete=models.CASCADE, related_name="personajes"
    )
    pros = models.JSONField(default=dict, blank=True)
    cons = models.JSONField(default=dict, blank=True)
    imagen = models.ImageField(upload_to="personajes/", blank=True, null=True)
    icono_url = models.ImageField(upload_to="personajes/")
    visitas = models.PositiveIntegerField(default=0)

    def incrementar_visitas(self):
        self.visitas += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(Personaje, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.juego.nombre})"


class Comentario(models.Model):
    noticia = models.ForeignKey(
        Noticia, on_delete=models.CASCADE, related_name="comentarios"
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    respuesta_a = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="respuestas",
    )

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.noticia}"

    def es_respuesta(self):
        """Verifica si el comentario es una respuesta a otro comentario"""
        return self.parent is not None


class Combo(models.Model):
    personaje = models.ForeignKey(
        Personaje, on_delete=models.CASCADE, related_name="combos"
    )
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre o etiqueta del combo (por ejemplo, 'Bread and Butter Combo')",
    )
    movimientos = models.TextField(
        help_text="Lista de movimientos en formato secuencial (ej. 'LP, MP, HP')"
    )
    dano = models.IntegerField(
        help_text="Cantidad de daño que hace el combo", null=True, blank=True
    )
    video = models.FileField(upload_to="combos/", blank=True, null=True)
    dificultad = models.CharField(
        max_length=50,
        choices=[
            ("Fácil", "Fácil"),
            ("Intermedio", "Intermedio"),
            ("Difícil", "Difícil"),
        ],
        help_text="Dificultad del combo",
    )

    descripcion = models.TextField(
        help_text="Descripción o contexto del combo", blank=True
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario que creó o compartió el combo",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    video_demo_url = models.URLField(
        blank=True, null=True, help_text="URL a un video de demostración"
    )  # Campo para el enlace de video

    def __str__(self):
        return f"{self.nombre} - {self.personaje.nombre}"

    class Meta:
        ordering = ["personaje", "dificultad", "-fecha_creacion"]


class FrameData(models.Model):
    personaje = models.ForeignKey(
        Personaje, on_delete=models.CASCADE, related_name="frame_data"
    )
    movimiento = models.CharField(max_length=100)  # Nombre del movimiento
    tipo = models.CharField(max_length=50)  # Ej. 'Normal', 'Especial', 'Super'
    damage = models.IntegerField(blank=True, null=True)  # Daño causado
    startup_frames = models.IntegerField(blank=True, null=True)  # Cuadros de inicio
    active_frames = models.IntegerField(blank=True, null=True)  # Cuadros activos
    recovery_frames = models.IntegerField(
        blank=True, null=True
    )  # Cuadros de recuperación
    block_advantage = models.IntegerField(blank=True, null=True)  # Ventaja en bloqueo
    hit_advantage = models.IntegerField(blank=True, null=True)  # Ventaja en golpe
    knockdown = models.BooleanField(default=False)  # Indica si el movimiento derriba
    video_demo_url = models.URLField(blank=True, null=True)
    imagen = models.ImageField(upload_to="frame_data/", null=True, blank=True)
    # Enlace a video de demostración

    def __str__(self):
        return f"{self.personaje.nombre} - {self.movimiento}"


class Hub(models.Model):
    titulo = models.CharField(max_length=100)  # Ejemplo: "Barra de vida"
    descripcion = models.TextField()  # Descripción del contenido
    imagen = models.ImageField(upload_to="hub_images/")  # Imagen asociada
    juego = models.ForeignKey(
        "Juego", on_delete=models.CASCADE
    )  # Relación con el juego específico

    def __str__(self):
        return self.titulo


class RoleChangeRequest(models.Model):
    ROLE_CHOICES = [
        ("redactor", "Redactor"),
        ("organizador", "Organizador"),
    ]
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rol_solicitado = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mensaje = models.TextField(blank=True)
    revisado = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.usuario.username} solicita ser {self.get_rol_solicitado_display()}"
        )


class Estrategia(models.Model):
    personaje = models.OneToOneField(
        "Personaje", on_delete=models.CASCADE, related_name="estrategia"
    )

    tacticas_generales = models.JSONField(default=list, blank=True)
    posicionamiento_en_el_equipo = models.JSONField(default=list, blank=True)
    block_string = models.JSONField(default=list, blank=True)
    oki = models.JSONField(default=list, blank=True)
    tips_y_trucos = models.JSONField(default=list, blank=True)
    luchando_en_contra = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Estrategia de {self.personaje.nombre}"


class Recurso(models.Model):
    CATEGORIAS = [
        ('Combo', 'Combo Avanzado'),
        ('Tech', 'Tech de Defensa'),
        ('Guia', 'Guía de Principiantes'),
        ('Comunidad', 'Comunidad'),
        ("video", "Video"),

    ]
    
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="recursos")
    link_discord = models.URLField(blank=True, null=True)  # Enlace de Discord
    hashtag_twitter = models.CharField(max_length=50, blank=True, null=True)  # Hashtag de Twitter
    enlace_video = models.URLField(blank=True, null=True, help_text="Enlace a YouTube o Twitter")
    descripcion = models.TextField(blank=True, help_text="Breve descripción del recurso")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='comunidad')
    creado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recursos', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Recurso: {self.personaje.nombre} - {self.categoria}"

class Glosario(models.Model):
    termino = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    juego = models.ManyToManyField("Juego", related_name="glosarios", blank=True)

    def __str__(self):
        return self.termino


class PersonajeVisita(models.Model):
    personaje = models.ForeignKey(
        "Personaje", on_delete=models.CASCADE, related_name="personaje_visitas"
    )
    juego = models.ForeignKey(
        "Juego", on_delete=models.CASCADE, related_name="juego_visitas"
    )
    fecha_visita = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.personaje.nombre} - {self.juego.nombre}"

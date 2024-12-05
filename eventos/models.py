from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.utils import timezone



# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.DateField()
    contenido = models.TextField()
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )
    imagen = models.ImageField(upload_to="eventos/", null=True, blank=True)
    direccion = models.CharField(
        max_length=255, null=True, blank=True
    )  # Nueva variable de dirección
    # Campos para ganadores
    primer_lugar = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primer_lugar_eventos",
    )
    segundo_lugar = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="segundo_lugar_eventos",
    )
    tercer_lugar = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tercer_lugar_eventos",
    )

    premio_primer_lugar = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    premio_segundo_lugar = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    premio_tercer_lugar = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def save(self, *args, **kwargs):
        # Agregar puntos a los ganadores
        if self.primer_lugar:
            self.primer_lugar.puntos += 3
            self.primer_lugar.save()
        if self.segundo_lugar:
            self.segundo_lugar.puntos += 2
            self.segundo_lugar.save()
        if self.tercer_lugar:
            self.tercer_lugar.puntos += 1
            self.tercer_lugar.save()

        # Llamar al método save original
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
class TorneoComunitario(models.Model):
    TIPOS_TORNEO = [
        ('presencial', 'Presencial'),
        ('online', 'Online'),
    ]

    titulo = models.CharField(max_length=255)
    fecha = models.DateField()
    tipo_torneo = models.CharField(max_length=10, choices=TIPOS_TORNEO, default='online')
    descripcion = models.TextField()
    organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='torneos_organizados',  default=1)
    imagen = models.ImageField(upload_to='torneos/', null=True, blank=True)
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='InscripcionTorneo', related_name='torneos_inscritos')
    direccion = models.CharField(max_length=255, blank=True, null=True) 
    bracket_generado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_torneo_display()})"
    
class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey(TorneoComunitario, on_delete=models.CASCADE,related_name='inscripciones')
    participante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.participante.nick} inscrito en {self.torneo.titulo}"
    
class Match(models.Model):
    torneo = models.ForeignKey(TorneoComunitario, on_delete=models.CASCADE)
    jugador1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jugador1')
    jugador2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jugador2')
    marcador_jugador1 = models.IntegerField(default=0)
    marcador_jugador2 = models.IntegerField(default=0)
    ganador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ganador_match')
    ronda = models.IntegerField()
    
    def __str__(self):
        return f"Match {self.jugador1.nick} vs {self.jugador2.nick} - Ronda {self.ronda}"

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




# Create your models here.


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

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
    
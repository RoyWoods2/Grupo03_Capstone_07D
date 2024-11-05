
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic



# Create your views here.

def HomeView(request):
    return render(request, "dbfz/home.html")
def noticia(request):
     return render(request, "dbfz/noticia.html")
def notasParche (request):
    return render(request, "dbfz/notasParche.html")

def personajes(request):
    
    return render(request, "dbfz/personajes.html")

def goku (request):
    return render(request, "dbfz/goku.html")

from django.shortcuts import render, get_object_or_404
from polls.models import Juego, Personaje

def personajes_por_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    personajes = juego.personajes.all()  # Accede a los personajes relacionados
    return render(request, 'personajes_template.html', {'juego': juego, 'personajes': personajes})

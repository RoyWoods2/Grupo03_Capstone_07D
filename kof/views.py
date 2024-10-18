from django.shortcuts import render
from django.views import generic
from polls.models import Choice, Question



# Create your views here.

def home(request):
    return render(request, "kof/home.html")
def noticia(request):
    return render(request, "kof/noticia.html")
def personajes(request):
    return render(request, "kof/personajes.html")
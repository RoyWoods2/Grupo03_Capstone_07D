from django.shortcuts import render
from django.views import generic



# Create your views here.

def home(request):
    return render(request, "kof/home.html")
def noticia(request):
    return render(request, "kof/noticia.html")
def personajes(request):
    return render(request, "kof/personajes.html")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EventoForm,TorneoComunitarioForm
from .models import Evento,TorneoComunitario
from django.shortcuts import render, get_object_or_404
from polls.models import CustomUser

from django.contrib.auth import get_user_model

User = get_user_model()

def detalle_torneo_comunitario(request, torneo_id):
    torneo = get_object_or_404(TorneoComunitario, id=torneo_id)
    return render(request, 'eventos/detalle_torneo_comunitario.html', {'torneo': torneo})

@login_required
def crear_torneo_comunitario(request):
    if request.method == "POST":
        form = TorneoComunitarioForm(request.POST, request.FILES)
        if form.is_valid():
            torneo = form.save(commit=False)
            torneo.autor = request.user
            torneo.save()
            return redirect("eventos:lista_eventos")
    else:
        form = TorneoComunitarioForm()
    return render(request, "eventos/crear_torneo_comunitario.html", {"form": form})

def ranking(request):
    jugadores = CustomUser.objects.filter(puntos__gt=0).order_by("-puntos")
    return render(request, "eventos/ranking.html", {"jugadores": jugadores})


def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    google_maps_api_key = "AIzaSyBIjmo2r5VEG-Lr25fPsCBlebWDDGEHaco"  # Reemplaza con tu clave de API de Google Maps
    return render(
        request,
        "eventos/detalle_evento.html",
        {"evento": evento, "google_maps_api_key": google_maps_api_key},
    )


def lista_eventos(request):
    eventos = Evento.objects.all().order_by("-fecha")
    torneos = TorneoComunitario.objects.all().order_by('-fecha')

    return render(request, "eventos/lista_eventos.html", {"eventos": eventos, 'torneos': torneos})


@login_required
def crear_evento(request):

    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.autor = request.user  # Asignar al autor como el usuario autenticado
            evento.save()
            return redirect("eventos:lista_eventos")
    else:
        form = EventoForm()

    return render(request, "eventos/crear_evento.html", {"form": form})

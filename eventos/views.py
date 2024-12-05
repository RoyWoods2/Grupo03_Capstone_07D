from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .forms import EventoForm,TorneoComunitarioForm
from .models import Evento,TorneoComunitario,InscripcionTorneo,Match
from django.shortcuts import render, get_object_or_404
from polls.models import CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from random import shuffle
from django.http import JsonResponse
import json


User = get_user_model()
def actualizar_bracket(request, torneo_id):
    if request.method == "POST":
        torneo = get_object_or_404(TorneoComunitario, id=torneo_id)
        data = json.loads(request.body)
        
        for ronda, matches in enumerate(data["results"][0]):
            for idx, result in enumerate(matches):
                match = torneo.match_set.filter(ronda=ronda+1)[idx]
                match.marcador_jugador1, match.marcador_jugador2 = result
                match.save()
                
        return JsonResponse({"message": "Marcadores actualizados correctamente."})
    return JsonResponse({"error": "Método no permitido."}, status=405)


def es_admin_o_organizador(user):
    return user.is_staff or user.user_type == 'organizador'

@user_passes_test(es_admin_o_organizador)
def actualizar_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        # Obtener los valores de los marcadores desde el formulario
        marcador_jugador1 = request.POST.get('marcador_jugador1')
        marcador_jugador2 = request.POST.get('marcador_jugador2')

        # Verificar que los marcadores sean números válidos
        if marcador_jugador1.isdigit() and marcador_jugador2.isdigit():
            marcador_jugador1 = int(marcador_jugador1)
            marcador_jugador2 = int(marcador_jugador2)

            # Actualizar los marcadores
            match.marcador_jugador1 = marcador_jugador1
            match.marcador_jugador2 = marcador_jugador2

            # Determinar el ganador
            if marcador_jugador1 > marcador_jugador2:
                match.ganador = match.jugador1
            elif marcador_jugador2 > marcador_jugador1:
                match.ganador = match.jugador2
            else:
                match.ganador = None  # En caso de empate

            # Guardar los cambios en el match
            match.save()

            # Avanzar a la siguiente ronda si es necesario
            if match.fase == 'Final':
                pass  # Realizar acciones si es la final
            else:
                # Aquí podrías agregar lógica para avanzar los jugadores al siguiente match
                pass

            # Redirigir al detalle del torneo
            return redirect('eventos:detalle_torneo_comunitario', torneo_id=match.torneo.id)

    return render(request, 'eventos/actualizar_match.html', {'match': match})

def asignar_puntos(ganador):
    if ganador:
        if ganador == torneo.primer_lugar:
            ganador.puntos += 3
        elif ganador == torneo.segundo_lugar:
            ganador.puntos += 2
        elif ganador == torneo.tercer_lugar:
            ganador.puntos += 1
        ganador.save()

def generar_bracket(request, torneo_id):
    torneo = get_object_or_404(TorneoComunitario, id=torneo_id)
    inscripciones = list(torneo.inscripciones.all())
    if not inscripciones or len(inscripciones) < 2:
        messages.error(request, "Se necesitan al menos 2 participantes para generar un bracket.")
        return redirect('eventos:detalle_torneo_comunitario', torneo_id=torneo.id)

    # Mezclar las inscripciones aleatoriamente
    shuffle(inscripciones)

    # Crear matches
    for i in range(0, len(inscripciones), 2):
        jugador1 = inscripciones[i].participante
        jugador2 = inscripciones[i+1].participante if i+1 < len(inscripciones) else None
        Match.objects.create(
            torneo=torneo,
            jugador1=jugador1,
            jugador2=jugador2,
            ronda=1
        )
    
    torneo.bracket_generado = True
    torneo.save()
    messages.success(request, "¡Bracket generado con éxito!")
    return redirect('eventos:detalle_torneo_comunitario', torneo_id=torneo.id)

@login_required
def inscribir_torneo(request, torneo_id):
    torneo = get_object_or_404(TorneoComunitario, id=torneo_id)
    if torneo.inscripciones.filter(participante=request.user).exists():
        messages.warning(request, "Ya estás inscrito en este torneo.")
    else:
        InscripcionTorneo.objects.create(torneo=torneo, participante=request.user)
        messages.success(request, "Te has inscrito exitosamente.")
    return redirect('eventos:detalle_torneo_comunitario', torneo_id=torneo.id)

def detalle_torneo_comunitario(request, torneo_id):
    torneo = get_object_or_404(TorneoComunitario, id=torneo_id)
    matches = torneo.match_set.all() 
    inscrito = torneo.inscripciones.filter(participante=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'eventos/detalle_torneo_comunitario.html', {'torneo': torneo, 'matches': matches, 'inscrito': inscrito})

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

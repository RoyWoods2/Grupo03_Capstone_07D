from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User
from django.contrib import messages
import requests
from django.conf import settings
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm, ComentarioForm,UserProfileForm,RoleChangeRequestForm  
from .models import Juego, Personaje,CustomUser , FrameData,Comentario,Hub, Combo, RoleChangeRequest, Estrategia,Personaje, Recurso
import json
from eventos.models import Evento
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your views here.




@staff_member_required
def revisar_solicitudes(request):
    solicitudes = RoleChangeRequest.objects.filter(revisado=False)
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        aprobar = request.POST.get('aprobar') == 'true'
        solicitud = RoleChangeRequest.objects.get(id=solicitud_id)
        if aprobar:
            usuario = solicitud.usuario
            usuario.user_type = solicitud.rol_solicitado
            usuario.save()
        solicitud.revisado = True
        solicitud.save()
        return redirect('polls:revisar_solicitudes')

    return render(request, 'polls/revisar_solicitudes.html', {'solicitudes': solicitudes})
def hub_view(request, juego_slug):
    # Obtener el juego y los datos del hub relacionados
    juego = get_object_or_404(Juego, slug=juego_slug)
    hub_data = Hub.objects.filter(juego=juego)  # Asegúrate de que el modelo Hub tiene relación con Juego

    context = {
        'juego': juego,
        'hub_data': hub_data,
    }
    return render(request, 'polls/hub_page.html', context)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)

def perfil_usuario(request):
    if not request.user.is_authenticated:
        return redirect('polls:login')

    profile = request.user
    comentarios = profile.comentario_set.all()

    # Formulario para actualizar perfil
    form = UserProfileForm(instance=profile)

    # Formulario para solicitar cambio de rol
    role_request_form = RoleChangeRequestForm()

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('polls:perfil_usuario')
        
        elif 'request_role' in request.POST:
            role_request_form = RoleChangeRequestForm(request.POST)
            if role_request_form.is_valid():
                solicitud = role_request_form.save(commit=False)
                solicitud.usuario = request.user
                solicitud.save()
                return redirect('polls:perfil_usuario')

    return render(request, 'polls/perfil_usuario.html', {
        'profile': profile,
        'comentarios': comentarios,
        'form': form,
        'role_request_form': role_request_form,
    })


def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, "polls/lista_juegos.html", {'juegos': juegos})

def lista_personajes(request, juego_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personajes = juego.personajes.filter(juego=juego)
    hub_data = Hub.objects.filter(juego=juego)  # Asegúrate de que el modelo Hub tiene relación con Juego
    context = {
        'juego': juego,
        'personajes': personajes,
        'hub_data': hub_data,
    }

    return render(request, 'polls/lista_personajes.html', context)


def detalle_personaje(request, juego_slug, personaje_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personaje = get_object_or_404(Personaje, slug=personaje_slug, juego=juego)
    combos = Combo.objects.filter(personaje=personaje)  # Asegúrate de que `combos` esté relacionado con el personaje
    framedata = FrameData.objects.filter(personaje=personaje)  # Filtrar framedata asociada
    estrategias = Estrategia.objects.filter(personaje=personaje)  # Filtrando estrategias asociadas a este personaje
    recursos = Recurso.objects.filter(personaje=personaje)


    context = {
        'personaje': personaje,
        'combos': combos,
        'framedata': framedata,
        'estrategias': estrategias,
        'recursos': recursos,
    }
    return render(request, 'polls/detalle_personaje.html', context)


@login_required (login_url="/login")
def comentarios_vista(request):
    # Manejar el envío de un comentario o respuesta
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            # Verificar si el comentario es una respuesta a otro comentario
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent = get_object_or_404(Comentario, id=parent_id)
            comentario.save()
            return redirect('/prueba')
    else:
        form = ComentarioForm()

    # Mostrar comentarios principales (sin parent)
    comentarios = Comentario.objects.filter(parent__isnull=True).order_by('-fecha_publicacion')

    return render(request, 'polls/prueba.html', {'form': form, 'comentarios': comentarios})




# Supón que tienes una URL de API y un token de acceso para Behold
API_URL = "https://api.behold.com/v1/data"
API_TOKEN = "tu_api_token_aqui"

def get_behold_data():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Devuelve los datos en formato JSON
    else:
        return {}  # En caso de error, devuelve un diccionario vacío

def behold_data_view(request):
    data = get_behold_data()
    return render(request, 'behold_data.html', {'data': data})


def registro_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('polls:login')  # Redirige a la página de login después de registrar al usuario
    else:
        form = CustomUserCreationForm()
    return render(request, 'polls/registro.html', {'form': form})


# Vista de cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('/')


# Vista de inicio de sesión
def login_view(request):
    form = CustomLoginForm(data=request.POST or None)  # Usa el formulario personalizado

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:')  # Cambia esto al nombre de tu vista principal
            else:
                form.add_error(None, "Credenciales incorrectas")  # Añade un error general al formulario

    return render(request, 'polls/login.html', {'form': form})





class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    
    


def detailView (request):  
    return render(request, 'polls/detail.html')  




def juegos(request):
    return render(request, "polls/juegos.html")
def base(request):
    return render(request, "polls/base.html")

def prueba(request):
    return render(request, "polls/prueba.html")

    
def index(request):
    eventos = Evento.objects.all()  # Confirma que este QuerySet incluye todos los eventos
    return render(request, "polls/index.html" , {'eventos': eventos})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

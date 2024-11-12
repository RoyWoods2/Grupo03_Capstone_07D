from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.conf import settings
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from .models import Juego, Personaje, UserProfile , CustomUser, FrameData 
import json
from eventos.models import Evento
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ComentarioForm,UserProfileForm  
from .models import Comentario, Combo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def perfil_usuario(request):
    profile = request.user.userprofile
    comentarios = Comentario.objects.filter(usuario=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Manejo de solicitud de cambio de tipo de usuario
            if 'tipo_usuario' in form.changed_data:
                profile.tipo_usuario_solicitado = form.cleaned_data['user_type']
                profile.save()
            return redirect('polls:perfil_usuario')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'polls/perfil_usuario.html', {
        'form': form,
        'comentarios': comentarios,
        'profile': profile,
    })

def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, "polls/lista_juegos.html", {'juegos': juegos})

def lista_personajes(request, juego_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personajes = juego.personajes.all()
    return render(request, 'polls/lista_personajes.html', {'juego': juego, 'personajes': personajes})

def detalle_personaje(request,juego_slug, personaje_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personaje = get_object_or_404(Personaje, slug=personaje_slug, juego=juego) 
    combos = Combo.objects.filter(personaje=personaje)  # Asegúrate de que combos esté relacionado con el personaje
    framedata = FrameData.objects.filter(personaje=personaje)  # Filtrar framedata asociada
    context = {
        'personaje': personaje,
        'combos': combos,
        'framedata': framedata,
    }
    return render(request, "polls/detalle_personaje.html", context)

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
            return redirect('polls:login')  # Cambia 'login' por el nombre de la URL de login
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
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Cambia 'home' por la URL de inicio después del login
    else:
        form = CustomLoginForm()
    return render(request, 'polls/login.html', {'form': form})




class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    

    
    


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

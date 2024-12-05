from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from django.conf import settings
from .forms import (
    CustomUserCreationForm,
    CustomLoginForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    ComentarioForm,
    UserProfileForm,
    RoleChangeRequestForm,
    RecursoForm,
    ModeracionForm
)
from noticias.models import Noticia
from .models import (
    Juego,
    Personaje,
    CustomUser,
    FrameData,
    Comentario,
    Hub,
    Combo,
    RoleChangeRequest,
    Estrategia,
    Personaje,
    Recurso,
    Glosario,
    PersonajeVisita,
    Moderacion
    
    
)
import json
from eventos.models import Evento
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
import paypalrestsdk


# Create your views here.
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox o live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})
def payment_success(request):
    payment_id = request.GET.get('paymentId')  
    payer_id = request.GET.get('PayerID')      

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        
        # Ejecuta el pago si no ha sido ejecutado previamente
        if payment.execute({"payer_id": payer_id}):
            
            return render(request, "polls/payment_success.html", {"payment": payment})
        else:
            raise Exception("Error al procesar el pago.")
    except Exception as e:
        
        return render(request, "polls/payment_error.html", {"error": "Hubo un error al procesar tu pago."})
def payment_cancel(request):
    return render(request, "payment_cancel.html", {"message": "Tu pago fue cancelado."})
def donation(request):
    if request.method == 'POST':
        # Obtener la cantidad de la donación del formulario
        amount = request.POST.get('amount')

        # Crear la transacción de PayPal
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Donación a mi proyecto"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            }
        })

        # Crear el pago
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            return render(request, "polls/donation_error.html", {"error": "Hubo un error al procesar el pago."})

    return render(request, "polls/donation_form.html")
def faq (request):
    return render(request, 'polls/faq.html')

@staff_member_required
def moderar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    moderacion, created = Moderacion.objects.get_or_create(usuario=usuario)
    if request.method == 'POST':
        form = ModeracionForm(request.POST, instance=moderacion)
        if form.is_valid():
            form.save()
            return redirect('polls:perfil_usuario', nick=usuario.nick)
    else:
        form = ModeracionForm(instance=moderacion)
    return render(request, 'polls/moderar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def votar_recurso(request, recurso_id, accion):
    recurso = get_object_or_404(Recurso, id=recurso_id)
    # Lógica de voto (like/dislike)
    if accion == "like":
        # Procesar el "like"
        pass
    elif accion == "dislike":
        # Procesar el "dislike"
        pass

    # Redirigir a la página del personaje asociado al recurso
    return redirect(reverse('polls:detalle_personaje', args=[recurso.personaje.juego.slug, recurso.personaje.slug]))

def crear_recurso(request, juego_slug, personaje_slug):
    personaje = get_object_or_404(Personaje, slug=personaje_slug, juego__slug=juego_slug)
    
    if request.method == 'POST':
        form = RecursoForm(request.POST)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.personaje = personaje
            recurso.save()
            return redirect('polls:detalle_personaje', juego_slug=juego_slug, personaje_slug=personaje_slug)
    else:
        form = RecursoForm()

    return render(request, 'polls/crear_recurso.html', {'form': form, 'personaje': personaje})

@staff_member_required
def admin_grafico_personajes(request):
    visitas_por_juego = (
        PersonajeVisita.objects.values("personaje__juego__nombre", "personaje__nombre")
        .annotate(total_visitas=models.Count("id"))
        .order_by("-total_visitas")
    )

    context = {
        "visitas_por_juego": visitas_por_juego,
    }
    return render(request, "polls/grafico_personajes.html", context)


def detalle_personaje(request, juego_slug, personaje_slug):
    personaje = Personaje.objects.get(slug=personaje_slug)
    juego = Juego.objects.get(slug=juego_slug)

    # Registrar la visita
    PersonajeVisita.objects.create(personaje=personaje, juego=juego)

    return render(
        request,
        "polls/detalle_personaje.html",
        {"personaje": personaje, "juego": juego},
    )


def glosario_view(request, juego_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    terminos = Glosario.objects.filter(juego=juego).order_by("termino")
    return render(
        request, "polls/glosario.html", {"terminos": terminos, "juego": juego}
    )


@staff_member_required
def revisar_solicitudes(request):
    solicitudes = RoleChangeRequest.objects.filter(revisado=False)
    if request.method == "POST":
        solicitud_id = request.POST.get("solicitud_id")
        aprobar = request.POST.get("aprobar") == "true"
        solicitud = RoleChangeRequest.objects.get(id=solicitud_id)
        if aprobar:
            usuario = solicitud.usuario
            usuario.user_type = solicitud.rol_solicitado
            usuario.save()
        solicitud.revisado = True
        solicitud.save()
        return redirect("polls:revisar_solicitudes")

    return render(
        request, "polls/revisar_solicitudes.html", {"solicitudes": solicitudes}
    )


def hub_view(request, juego_slug):
    # Obtener el juego y los datos del hub relacionados
    juego = get_object_or_404(Juego, slug=juego_slug)
    hub_data = Hub.objects.filter(
        juego=juego
    )  # Asegúrate de que el modelo Hub tiene relación con Juego

    context = {
        "juego": juego,
        "hub_data": hub_data,
    }
    return render(request, "polls/hub_page.html", context)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)


def perfil_usuario(request, nick=None):
    if not request.user.is_authenticated:
        return redirect("polls:login")

    profile = get_object_or_404(CustomUser, nick=nick) if nick else request.user
    twitch_embed_url = None
    youtube_channel_id = None
    if profile.twitch_stream:
        twitch_embed_url = profile.twitch_stream.replace("https://www.twitch.tv/", "")
    if profile.youtube_channel:
        youtube_channel_id = profile.youtube_channel.split('/')[-1]  # Extraer el canal si es válido

    
    comentarios = profile.comentario_set.all()
  
    form, role_request_form = None, None
    if request.user == profile:
        form = UserProfileForm(instance=profile)
        role_request_form = RoleChangeRequestForm()

        if request.method == "POST":
            if "update_profile" in request.POST:
                form = UserProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
                    return redirect("polls:perfil_usuario", nick=profile.nick)

            elif "request_role" in request.POST:
                role_request_form = RoleChangeRequestForm(request.POST)
                if role_request_form.is_valid():
                    solicitud = role_request_form.save(commit=False)
                    solicitud.usuario = request.user
                    solicitud.save()
                    return redirect("polls:perfil_usuario", nick=profile.nick)
  


    return render(request, "polls/perfil_usuario.html", {
        "profile": profile,
        "comentarios": comentarios,
        "form": form,
        "role_request_form": role_request_form,
        "twitch_embed_url": twitch_embed_url,
        "youtube_channel_id": youtube_channel_id,


    })

def lista_juegos(request):
    juegos = Juego.objects.all()
    return render(request, "polls/lista_juegos.html", {"juegos": juegos})


def lista_personajes(request, juego_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personajes = juego.personajes.filter(juego=juego)
    hub_data = Hub.objects.filter(
        juego=juego
    )  # Asegúrate de que el modelo Hub tiene relación con Juego
    context = {
        "juego": juego,
        "personajes": personajes,
        "hub_data": hub_data,
    }

    return render(request, "polls/lista_personajes.html", context)


def detalle_personaje(request, juego_slug, personaje_slug):
    juego = get_object_or_404(Juego, slug=juego_slug)
    personaje = get_object_or_404(Personaje, slug=personaje_slug, juego=juego)
    combos = Combo.objects.filter(
        personaje=personaje
    )  # Asegúrate de que `combos` esté relacionado con el personaje
    framedata = FrameData.objects.filter(
        personaje=personaje
    )  # Filtrar framedata asociada
    estrategias = Estrategia.objects.filter(
        personaje=personaje
    )  # Filtrando estrategias asociadas a este personaje
    recursos = Recurso.objects.filter(personaje=personaje)
    personaje.incrementar_visitas()
    recursos_por_categoria = recursos.values('categoria').distinct()  # Agrupar recursos por categoría


    context = {
        "personaje": personaje,
        "combos": combos,
        "framedata": framedata,
        "estrategias": estrategias,
        "recursos": recursos,
        "recursos_por_categoria": recursos_por_categoria

    }
    return render(request, "polls/detalle_personaje.html", context)


@login_required(login_url="/login")
def comentarios_vista(request):
    # Manejar el envío de un comentario o respuesta
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            # Verificar si el comentario es una respuesta a otro comentario
            parent_id = request.POST.get("parent_id")
            if parent_id:
                comentario.parent = get_object_or_404(Comentario, id=parent_id)
            comentario.save()
            return redirect("/prueba")
    else:
        form = ComentarioForm()

    # Mostrar comentarios principales (sin parent)
    comentarios = Comentario.objects.filter(parent__isnull=True).order_by(
        "-fecha_publicacion"
    )

    return render(
        request, "polls/prueba.html", {"form": form, "comentarios": comentarios}
    )


# Supón que tienes una URL de API y un token de acceso para Behold
API_URL = "https://api.behold.com/v1/data"
API_TOKEN = "tu_api_token_aqui"


def get_behold_data():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Devuelve los datos en formato JSON
    else:
        return {}  # En caso de error, devuelve un diccionario vacío


def behold_data_view(request):
    data = get_behold_data()
    return render(request, "behold_data.html", {"data": data})


def registro_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "polls:login"
            )  # Redirige a la página de login después de registrar al usuario
    else:
        form = CustomUserCreationForm()
    return render(request, "polls/registro.html", {"form": form})


# Vista de cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("/")


# Vista de inicio de sesión
def login_view(request):
    form = CustomLoginForm(data=request.POST or None)  # Usa el formulario personalizado

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("polls:")  # Cambia esto al nombre de tu vista principal
            else:
                form.add_error(
                    None, "Credenciales incorrectas"
                )  # Añade un error general al formulario

    return render(request, "polls/login.html", {"form": form})


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"


def detailView(request):
    return render(request, "polls/detail.html")


def juegos(request):
    return render(request, "polls/juegos.html")


def base(request):
    return render(request, "polls/base.html")


def prueba(request):
    return render(request, "polls/prueba.html")


def index(request):
    eventos = Evento.objects.all().order_by("-fecha")[:5]  # Últimos 5 eventos
    noticias = Noticia.objects.all().order_by("-fecha")[:5]  # Últimas 5 noticias
    juegos_destacados = Juego.objects.all()[:3]  # Mostrar 3 juegos destacados
    ranking = CustomUser.objects.all().order_by("-puntos")[:10]  # Top 10 jugadores
    jugadores_destacados = CustomUser.objects.all().order_by("-puntos")[
        :3
    ]  # Top 3 jugadores destacados

    context = {
        "eventos": eventos,
        "noticias": noticias,
        "juegos_destacados": juegos_destacados,
        "ranking": ranking,
        "jugadores_destacados": jugadores_destacados,
    }
    return render(request, "polls/index.html", context)


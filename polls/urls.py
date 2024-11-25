from django.urls import path, include

from . import views
from polls.views import revisar_solicitudes


app_name = "polls"
urlpatterns = [
    path('', views.index ,name=''),
    path("base",views.base, name="base"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registro', views.registro_view, name='registro'),
    path('prueba', views.juegos, name='prueba'),
    path("detail", views.detailView, name="detail"),
    path('juegos/', views.lista_juegos, name='lista_juegos'),
    path('juegos/<slug:juego_slug>/', views.lista_personajes, name='lista_personajes'),
    path('juegos/<slug:juego_slug>/personajes/<slug:personaje_slug>/', views.detalle_personaje, name='detalle_personaje'),
    path('juegos/<slug:juego_slug>/hub/', views.hub_view, name='hub_page'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),  # Perfil del usuario actual
    path('perfil/<str:nick>/', views.perfil_usuario, name='perfil_usuario'),  # Perfil con nick
    path('revisar-solicitudes/', revisar_solicitudes, name='revisar_solicitudes'),  # URL ajustada

 

]


from django.urls import path

from . import views

app_name = "dbfz"
urlpatterns = [
    path("", views.HomeView, name=""),
    path("personajes", views.personajes, name="personajes"),
    path("noticia", views.noticia, name="noticia"),
    path ("notasParche", views.notasParche, name="notasParche"),
    path ("goku", views.goku, name="goku"),
    path('juego/<int:juego_id>/personajes/', views.personajes, name='personajes'),


    
]

 

from django.urls import path

from . import views

app_name = "kof"
urlpatterns = [
    path("", views.home, name=""),
    path('noticia', views.noticia, name="noticia"),
    path('personajes', views.personajes, name="personajes"),

    
]

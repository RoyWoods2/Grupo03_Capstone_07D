from django.urls import path
from . import views

app_name = "noticias"

urlpatterns = [
    path("", views.lista_noticias, name="lista_noticias"),
    path(
        "crear/", views.crear_noticia, name="crear_noticia"
    ),  # Nueva URL para crear noticias
    path("<slug:slug>/", views.detalle_noticia, name="detalle_noticia"),
    path("acceso_denegado/", views.acceso_denegado, name="acceso_denegado"),
    path(
        "comentarios/editar/<int:comentario_id>/",
        views.editar_comentario,
        name="editar_comentario",
    ),
    path(
        "comentarios/eliminar/<int:comentario_id>/",
        views.eliminar_comentario,
        name="eliminar_comentario",
    ),
]

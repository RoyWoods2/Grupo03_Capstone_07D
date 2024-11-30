from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("crear-evento/", views.crear_evento, name="crear_evento"),
    path("lista_eventos/", views.lista_eventos, name="lista_eventos"),
    path(
        "<int:evento_id>/", views.detalle_evento, name="detalle_evento"
    ),  # Nueva URL para detalles
    path("ranking/", views.ranking, name="ranking"),
    path("crear_torneo_comunitario/", views.crear_torneo_comunitario, name="crear_torneo_comunitario"),
    path("torneo_comunitario/<int:torneo_id>/", views.detalle_torneo_comunitario, name="detalle_torneo_comunitario"),


]
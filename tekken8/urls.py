from django.urls import path

from . import views

app_name = "tekken8"

urlpatterns = [
    path("", views.home, name=""),

]
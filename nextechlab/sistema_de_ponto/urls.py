from django.urls import path, include
from sistema_de_ponto import views

urlpatterns = [
    path("", views.index, name="index"),
]

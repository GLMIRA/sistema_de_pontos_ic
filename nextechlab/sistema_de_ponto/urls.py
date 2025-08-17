from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "sistema_de_ponto"

urlpatterns = [
    # Página inicial
    path("", views.index, name="index"),
    # Autenticação
    path("login/", views.SistemLoginView.as_view(), name="login"),
    path("cadastro/", views.RegisterUserView.as_view(), name="cadastro"),
    path("logout/", views.logout_view, name="logout"),
    # Páginas dos usuários
    # pagina de registro de ponto do aluno do dia
    path("aluno-dia/", views.view_pagina_aluno, name="aluno_dia"),
    # pagina de registro de ponto
    path("registrar-ponto/", views.view_registrar_ponto, name="registrar_ponto"),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "sistema_de_ponto"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.SistemLoginView.as_view(), name="login"),
    path("cadastro/", views.RegisterUserView.as_view(), name="cadastro"),
    path("logout/", views.logout_view, name="logout"),
    path("aluno-dia/", views.view_pagina_aluno, name="aluno_dia"),
    path("registrar-ponto/", views.view_registrar_ponto, name="registrar_ponto"),
    path(
        "historico-aluno/",
        views.view_historico_de_pontos_completo,
        name="historico_aluno",
    ),
    path(
        "solicitar-professor/",
        views.view_solicitar_cadastro_professor,
        name="solicitar_professor",
    ),
    path(
        "dashbord-professor/", views.view_dashboard_professor, name="dashbord_professor"
    ),
]

import re
import logging

from django.db.models import F, Sum, ExpressionWrapper, DurationField
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import date

from .forms import CadastroForm
from .models import RegistroPonto


logger = logging.getLogger(__name__)


def eh_aluno(user: User):
    """
    Verifica se o usuário é um aluno baseado no padrão do RA.
    RA deve seguir o formato: a + 8 dígitos (ex: a1234567)
    """
    return re.match(r"^a\d{7}$", user.username) is not None


def eh_professor(user: User):
    """
    Verifica se o usuário pertence ao grupo Professor
    """
    return user.groups.filter(name="Professor").exists()


def view_solicitar_cadastro_professor(request: HttpRequest):
    """
    Página para professores solicitarem aprovação
    """
    return render(request, "sistema_de_ponto/professor/solicitar_professor.html")


def index(request: HttpRequest) -> HttpResponse:
    agora = timezone.now()
    total_entradas = 0
    total_saidas = 0
    total_horas = 0

    # Só calcula se o usuário estiver logado
    if request.user.is_authenticated:
        user = request.user
        hoje = agora.date()
        registros_hoje = RegistroPonto.objects.filter(
            aluno=user, data_hora__date=hoje
        ).order_by("data_hora")

        total_entradas = registros_hoje.filter(tipo="entrada").count()
        total_saidas = registros_hoje.filter(tipo="saida").count()

        entradas = list(
            registros_hoje.filter(tipo="entrada").values_list("data_hora", flat=True)
        )
        saidas = list(
            registros_hoje.filter(tipo="saida").values_list("data_hora", flat=True)
        )

        # Calcula total de horas apenas para pares entrada/saída
        total_horas = (
            sum(
                (saida - entrada).total_seconds()
                for entrada, saida in zip(entradas, saidas)
            )
            / 3600
        )  # converte para horas

    context = {
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "total_horas": round(total_horas, 2),
        "data_atual": agora,
    }

    # Caminho correto para o template
    return render(request, "sistema_de_ponto/index.html", context)


class RegisterUserView(CreateView):
    model = User
    form_class = CadastroForm
    template_name = "sistema_de_ponto/cadastro.html"
    # Usando reverse_lazy para URL correta
    success_url = reverse_lazy("sistema_de_ponto:index")

    def form_valid(self, form):
        """
        Processa o formulário quando os dados estão válidos
        """
        response = super().form_valid(form)
        user = self.object
        tipo_usuario = self.request.POST.get("tipo_usuario")

        if tipo_usuario == "aluno":
            if form.validar_ra_para_aluno():
                # Corrigido: get_or_create retorna (objeto, created)
                group_aluno, created = Group.objects.get_or_create(name="Alunos")
                print("teste_grupo", group_aluno, created)
                user.groups.add(group_aluno)

                logger.info(f"Novo aluno cadastrado: {user.username}")
                messages.success(self.request, "Aluno criado com sucesso!")

                # Fazendo login automático do usuário
                login(self.request, user)

                # Redirecionamento correto usando reverse
                return redirect("sistema_de_ponto:aluno_dia")
            else:
                logger.warning(
                    f"Falha no cadastro de aluno: RA inválido - {user.username}"
                )
                user.delete()  # Remove o usuário criado com dados inválidos
                form.add_error(
                    "username", "Para alunos, digite um RA válido (formato: a12345678)"
                )
                return self.form_invalid(form)

        elif tipo_usuario == "professor":
            if form.validar_username_para_professor():
                # Para professores, não adiciona ao grupo automaticamente
                logger.info(f"Solicitação de cadastro de professor: {user.username}")
                messages.info(
                    self.request,
                    "Solicite ao administrador para aprovar seu acesso como professor",
                )
                return redirect("sistema_de_ponto:solicitar_professor")
            else:
                user.delete()  # Remove o usuário criado com dados inválidos
                form.add_error(
                    "username", "Professores não podem usar formato de RA como username"
                )
                return self.form_invalid(form)
        else:
            user.delete()  # Remove o usuário se tipo não foi especificado
            messages.error(
                self.request, "Por favor, escolha se você é aluno ou professor"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Chamado quando o formulário tem erros
        """
        messages.error(self.request, "Corrija os erros no formulário")
        return super().form_invalid(form)


class SistemLoginView(LoginView):
    template_name = "sistema_de_ponto/login.html"

    def get_success_url(self):
        """
        Define para onde redirecionar após login bem-sucedido
        """
        user = self.request.user

        if eh_aluno(user):
            return reverse_lazy("sistema_de_ponto:aluno_dia")
        elif eh_professor(user):
            return reverse_lazy("sistema_de_ponto:dashbord_professor")
        else:
            messages.info(
                self.request,
                "Para acessar como professor, solicite aprovação do administrador.",
            )
            return reverse_lazy("sistema_de_ponto:solicitar_cadastro_professor")


@login_required
def logout_view(request: HttpRequest):
    """
    View para logout do usuário
    """
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect("sistema_de_ponto:index")


@login_required
def view_pagina_aluno(request: HttpRequest):
    """
    Página do aluno, onde ele pode registrar ponto
    """

    user = request.user

    if not eh_aluno(user=user):
        messages.error(
            request, "Acesso negado. Apenas alunos podem acessar esta página."
        )
        return redirect("sistema_de_ponto:index")

    hoje = date.today()
    registros_hoje = RegistroPonto.objects.filter(
        aluno=user,
        data_hora__date=hoje,
    ).order_by("-data_hora")

    contexto = {
        "registros_hoje": registros_hoje,
        "data_atual": timezone.now(),
        "total_entradas": registros_hoje.filter(tipo="entrada").count(),
        "total_saidas": registros_hoje.filter(tipo="saida").count(),
    }

    return render(request, "sistema_de_ponto/aluno/aluno_dia.html", contexto)


@login_required
def view_registrar_ponto(request: HttpRequest):
    """
    Registra ponto de entrada ou saída para o aluno.
    """

    user = request.user

    if not eh_aluno(user=user):
        messages.error(request, "Acesso negado. Apenas alunos podem registrar ponto.")
        return redirect("")  # redireciona pro painel mesmo

    if request.method == "POST":
        agora = timezone.now()
        hoje = agora.date()

        ultimo_registro = (
            RegistroPonto.objects.filter(
                aluno=user,
                data_hora__date=hoje,
            )
            .order_by("-data_hora")
            .first()
        )

        if ultimo_registro and ultimo_registro.tipo == "entrada":
            # Registra saída
            tipo = "saida"
            mensagem = "Saída registrada com sucesso!"
        else:
            # Registra entrada
            tipo = "entrada"
            mensagem = "Entrada registrada com sucesso!"

        RegistroPonto.objects.create(aluno=user, data_hora=agora, tipo=tipo)
        messages.success(request, mensagem)

    return redirect("sistema_de_ponto:aluno_dia")


@login_required
def view_historico_de_pontos_completo(request):
    user = request.user

    if not eh_aluno(user):
        messages.error(
            request, "Acesso negado. Apenas alunos podem acessar esta página."
        )
        return redirect("sistema_de_ponto:index")

    registros = RegistroPonto.objects.filter(aluno=user).order_by("-data_hora")

    registros_por_data = {}
    for registro in registros:
        data = registro.data_hora.date()
        registros_por_data.setdefault(data, []).append(registro)

    total_horas_por_dia = {}
    for data, registros_dia in registros_por_data.items():
        entradas = [r.data_hora for r in registros_dia if r.tipo == "entrada"]
        saidas = [r.data_hora for r in registros_dia if r.tipo == "saida"]

        total_horas = 0.0
        for entrada, saida in zip(entradas, saidas):
            total_horas += (saida - entrada).total_seconds() / 3600.0

        total_horas_por_dia[data] = round(total_horas, 2)

    datas_ordenadas = sorted(registros_por_data.keys(), reverse=True)
    datas_ordenadas_str = [d.strftime("%Y-%m-%d") for d in datas_ordenadas]

    total_horas_geral = round(sum(total_horas_por_dia.values()), 2)

    contexto = {
        "registros_por_data": registros_por_data,
        "total_horas_por_dia": total_horas_por_dia,
        "datas_ordenadas": datas_ordenadas,
        "datas_ordenadas_str": datas_ordenadas_str,
        "total_horas_geral": total_horas_geral,
        "data_atual": timezone.now(),
    }

    return render(request, "sistema_de_ponto/aluno/historico_pontos.html", contexto)


@login_required
def view_dashboard_professor(request):
    """
    Dashboard para professores, mostrando cards dos alunos.
    Dados detalhados são carregados via JavaScript quando clicar no aluno.
    """
    if not eh_professor(request.user):
        messages.error(
            request, "Acesso negado. Apenas professores podem acessar esta página."
        )
        return redirect("sistema_de_ponto:index")

    registros = RegistroPonto.objects.select_related("aluno").order_by("-data_hora")

    aluno_ids = registros.values_list("aluno_id", flat=True).distinct()
    alunos = User.objects.filter(id__in=aluno_ids).order_by(
        "first_name", "last_name", "username"
    )

    dados_por_aluno = {}

    for aluno in alunos:

        registros_aluno = registros.filter(aluno=aluno).order_by("-data_hora")

        entradas = [r.data_hora for r in registros_aluno if r.tipo == "entrada"]
        saidas = [r.data_hora for r in registros_aluno if r.tipo == "saida"]
        total_horas = 0.0

        for e, s in zip(entradas, saidas):
            total_horas += (s - e).total_seconds() / 3600.0

        lista_registros = []
        for registro in registros_aluno:
            lista_registros.append(
                {
                    "data_hora": registro.data_hora.strftime("%d/%m/%Y %H:%M"),
                    "tipo": registro.tipo,
                    "data": registro.data_hora.strftime("%d/%m/%Y"),
                    "hora": registro.data_hora.strftime("%H:%M"),
                }
            )

        if aluno.first_name and aluno.last_name:
            nome_completo = f"{aluno.first_name} {aluno.last_name}"
        elif aluno.first_name:
            nome_completo = aluno.first_name
        else:
            nome_completo = aluno.username

        dados_por_aluno[str(aluno.id)] = {
            "nome": nome_completo,
            "total_horas": round(total_horas, 2),
            "total_registros": registros_aluno.count(),
            "registros": lista_registros,
        }
    contexto = {
        "data_atual": timezone.now(),
        "alunos": alunos,
        "dados_por_aluno": dados_por_aluno,
    }

    return render(request, "sistema_de_ponto/professor/dashboard.html", contexto)

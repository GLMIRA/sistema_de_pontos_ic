import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RegistroPonto


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nome",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "RA (para alunos): a12345678 ou username (para professores)",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário e adiciona classes CSS aos campos de senha
        """
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_username(self):
        """
        Valida se o username já existe no banco de dados
        """
        username = self.cleaned_data.get("username", "").strip().lower()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuário já existe!")

        return username

    def validar_ra_para_aluno(self) -> bool:
        """
        Verifica se o username segue o padrão de RA para alunos
        Padrão: a + 8 dígitos (exemplo: a12345678)
        """
        username = self.cleaned_data.get("username", "")
        return re.match(r"^a\d{8}$", username) is not None

    def validar_username_para_professor(self) -> bool:
        """
        Verifica se o username é válido para professores
        Professores NÃO podem usar o formato de RA (a + dígitos)
        """
        username = self.cleaned_data.get("username", "")
        # Não pode ser formato de RA (a + qualquer quantidade de dígitos)
        return not re.match(r"^a\d+$", username)

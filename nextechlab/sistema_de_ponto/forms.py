from django import forms
from .models import Aluno, Professor
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        ]


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            "name",
            "ra",
            "email",
        ]


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = [
            "name",
            "email",
        ]

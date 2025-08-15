from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Professor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Nome do professor",
        max_length=100,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        verbose_name="Email do professor",
        max_length=100,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Aluno(models.Model):

    ra_regex_validator = RegexValidator(
        regex=r"^a\d{7}$", message="RA must be 8 digits.", code="invalid_ra"
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nome do aluno",
        null=False,
        blank=False,
    )
    ra = models.CharField(
        verbose_name="RA do aluno",
        max_length=8,
        null=False,
        blank=False,
        validators=[ra_regex_validator],
    )

    email = models.EmailField(
        verbose_name="Email do aluno",
        max_length=100,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class RegistroPontoAluno(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
    )
    data_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data e hora do registro",
    )
    tipo = models.CharField(
        max_length=10,
        choices=[("entrada", "Entrada"), ("saida", "Saída")],
        verbose_name="Tipo de registro",
    )

    def __str__(self):
        return f"{self.aluno.name} - {self.tipo} em {self.data_hora}"

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class RegistroPonto(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    ]

    # Relaciona diretamente com User - só alunos podem bater ponto
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Aluno")
    data_hora = models.DateTimeField(
        default=timezone.now, verbose_name="Data e hora do registro"
    )
    tipo = models.CharField(
        max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de registro"
    )

    class Meta:
        ordering = ["-data_hora"]
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Ponto"

    def __str__(self):
        nome = self.aluno.get_full_name() or self.aluno.username
        return f"{nome} - {self.tipo} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

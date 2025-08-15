from django.contrib import admin
from . import models

admin.site.register(models.Professor)
admin.site.register(models.Aluno)
admin.site.register(models.RegistroPontoAluno)

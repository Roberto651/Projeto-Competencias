from django.db import models
from . import fields

class CompetenciaField(models.IntegerField):
    def formfield(self, **kwargs):
        return fields.CompetenciaField(**kwargs)

class Lancamento(models.Model):
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    
    # Aqui está o segredo: No banco é apenas um número (ex: 202513)
    competencia = CompetenciaField("Competência (AAAAMM)")

    def __str__(self):
        # Formatamos para ficar bonito no Admin se precisar
        ano = self.competencia // 100
        mes = self.competencia % 100
        return f"{self.descricao} - {mes}/{ano}"
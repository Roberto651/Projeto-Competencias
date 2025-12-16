from django.db import models
from . import fields

class Competencia(int):
    def __new__(cls, value):
        return super(Competencia, cls).__new__(cls, value)

    @property
    def ano(self):
        return self // 100

    @property
    def mes(self):
        return self % 100

    # @property
    # def descricao_mes(self):
    #     nomes = {
    #         1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    #         5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    #         9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
    #         13: '13º Salário'
    #     }
    #     return nomes.get(self.mes, "Inválido")

    @property
    def proxima(self):
        """
        Lógica: 12 -> 13 -> 01 (do próximo ano)
        """
        if self.mes == 13:
            # Se for 13º, vira Janeiro do ano seguinte
            novo_ano = self.ano + 1
            novo_mes = 1
            return Competencia((novo_ano * 100) + novo_mes)
        else:
            # Se for qualquer outro (1 a 12), basta somar 1
            return Competencia(self + 1)

    @property
    def anterior(self):
        """
        Lógica: 01 -> 13 (do ano anterior) -> 12
        """
        if self.mes == 1:
            # Se for Janeiro, volta para o 13º do ano anterior
            novo_ano = self.ano - 1
            novo_mes = 13
            return Competencia((novo_ano * 100) + novo_mes)
        else:
            # Se for qualquer outro (2 a 13), basta subtrair 1
            return Competencia(self - 1)

    def __str__(self):
        mes_str = '13º' if self.mes == 13 else f"{self.mes:02d}"
        return f"{mes_str}/{self.ano}"
    
    def __repr__(self):
        return f"<Competencia: {self.mes}/{self.ano}>"


# MODEL FIELD
class CompetenciaField(models.IntegerField):
    description = "Armazena AAAAMM mas retorna um objeto Competencia"

    def formfield(self, **kwargs):
        return fields.CompetenciaField(**kwargs)

    def from_db_value(self, value, expression, connection):
        """
        Transforma o int puro (202513) no objeto Competencia.
        """
        if value is None:
            return value
        return Competencia(value)

    def to_python(self, value):
        """
        Garante a conversão em objeto Competencia.
        """
        if isinstance(value, Competencia):
            return value
        if value is None:
            return value
        return Competencia(int(value))
    
    def get_prep_value(self, value):
        """
        Salva como int puro.
        """
        if value is None:
            return None
        return int(value)

class Lancamento(models.Model):
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    
    competencia = CompetenciaField("Competência")

    def __str__(self):
        return f"{self.descricao} - {self.competencia}"
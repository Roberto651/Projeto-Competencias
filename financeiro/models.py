from functools import total_ordering
from django.db import models
from . import fields

@total_ordering
class Competencia:
    # Otimização de memória: armazena apenas o inteiro combinado (sem __dict__)
    __slots__ = ('_valor',)
    
    # Configuração direta para o projeto (13 meses)
    LIMITE_MES = 13

    def __init__(self, ano: int, mes: int):
        """
        Construtor padrão: recebe ano e mês separados.
        """
        # Validação
        if not (1 <= mes <= self.LIMITE_MES):
            raise ValueError(f"Mês {mes} inválido. Limite é {self.LIMITE_MES}.")
            
        # Armazenamento interno otimizado
        self._valor = (int(ano) * 100) + int(mes)

    @classmethod
    def from_int(cls, yyyymm: int):
        """Factory Method: Cria a partir de inteiro (ex: 202513)."""
        if yyyymm is None:
            return None
        yyyymm = int(yyyymm)
        ano = yyyymm // 100
        mes = yyyymm % 100
        return cls(ano, mes)

    # --- Properties (Leitura) ---

    @property
    def as_int(self):
        """Retorna o valor primitivo para o banco (YYYYMM)."""
        return self._valor

    @property
    def ano(self):
        return self._valor // 100

    @property
    def mes(self):
        return self._valor % 100

    @property
    def descricao_mes(self):
        """Retorna o nome do mês."""
        nomes = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
            13: '13º Salário'
        }
        return nomes.get(self.mes, "Inválido")
    
    # --- Navegação Temporal ---

    @property
    def proxima(self):
        return self + 1

    @property
    def anterior(self):
        return self - 1

    # --- Representação ---

    def __repr__(self):
        return f"Competencia({self.ano}, {self.mes})"

    def __str__(self):
        # Formato padrão solicitado: MM/AAAA
        return f"{self.mes:02d}/{self.ano}"

    # --- Comparação (Otimizada) ---

    def __eq__(self, other):
        if isinstance(other, Competencia):
            return self._valor == other._valor
        if isinstance(other, int):
            return self._valor == other
        return False

    def __lt__(self, other):
        if isinstance(other, Competencia):
            return self._valor < other._valor
        if isinstance(other, int):
            return self._valor < other
        return NotImplemented

    def __hash__(self):
        return hash(self._valor)

    # --- Aritmética (Lógica de 13 Meses) ---

    def __add__(self, meses_para_adicionar):
        if not isinstance(meses_para_adicionar, int):
            return NotImplemented
        
        # Lineariza o tempo (índice 0)
        total_meses = (self.ano * self.LIMITE_MES) + (self.mes - 1) + meses_para_adicionar
        
        # Calcula novo ano e mês
        novo_ano, novo_mes_idx = divmod(total_meses, self.LIMITE_MES)
        
        # Retorna nova instância (novo_mes_idx + 1 restaura para índice 1-13)
        return Competencia(novo_ano, novo_mes_idx + 1)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.__add__(-other)
        elif isinstance(other, Competencia):
            total_self = (self.ano * self.LIMITE_MES) + (self.mes - 1)
            total_other = (other.ano * self.LIMITE_MES) + (other.mes - 1)
            return total_self - total_other
        return NotImplemented


# --- O MODEL FIELD ---
class CompetenciaField(models.IntegerField):
    description = "Armazena AAAAMM mas retorna um objeto Competencia"

    def formfield(self, **kwargs):
        return fields.CompetenciaField(**kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None: return None
        return Competencia.from_int(value)

    def to_python(self, value):
        if isinstance(value, Competencia): return value
        if value is None: return None
        if isinstance(value, int): return Competencia.from_int(value)
        return value
    
    def get_prep_value(self, value):
        if value is None: return None
        if isinstance(value, Competencia): return value.as_int
        return int(value)


# --- SEU MODELO ---
class Lancamento(models.Model):
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    competencia = CompetenciaField("Competência")

    def __str__(self):
        return f"{self.descricao} - {self.competencia}"
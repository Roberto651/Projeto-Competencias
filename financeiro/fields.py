# financeiro/fields.py
import datetime
from django import forms
from django.core.exceptions import ValidationError
from .validators import validar_ano_inicio, validar_ano_limite_futuro, validar_mes_range

# --- 1. Definição das Opções (Choices) ---
MESES_CHOICES = [
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
    (13, '13º Salário'),
]

# --- 2. O Widget (Componente Visual) ---
class CompetenciaWidget(forms.MultiWidget):
    # O caminho para o seu HTML personalizado com o Modal
    template_name = 'widgets/competencia_arrow.html'

    def __init__(self, attrs=None):
        # Aqui definimos os widgets que aparecem na tela.
        # Usamos Select e NumberInput para que o usuário veja os campos
        # ao lado do botão de calendário.
        widgets = [
            forms.Select(
                attrs={'class': 'form-select', 'aria-label': 'Mês'}, 
                choices=MESES_CHOICES
            ),
            forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ano', 'aria-label': 'Ano'}
            ),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        """
        Transforma o valor inteiro do banco (ex: 202513) 
        em uma lista para os widgets [13, 2025].
        """
        if value:
            try:
                value = int(value)
                # Separa Mês e Ano
                return [value % 100, value // 100]
            except (ValueError, TypeError):
                return [None, None]
        
        # Se não tiver valor, sugere a data atual
        today = datetime.date.today()
        return [today.month, today.year]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Garante que o ID principal esteja disponível no template
        # Isso é crucial para o JavaScript do Modal saber qual campo atualizar
        if 'id' not in attrs:
            attrs['id'] = "id_" + name
        context['widget']['attrs']['id'] = attrs['id']
        return context


# --- O Field (Atualizado com Validators) ---
class CompetenciaField(forms.MultiValueField):
    widget = CompetenciaWidget

    def __init__(self, **kwargs):
        fields = (
            forms.IntegerField(min_value=1, max_value=13),
            forms.IntegerField(min_value=1900, max_value=2100),
        )
        
        if 'help_text' not in kwargs:
            kwargs['help_text'] = "Selecione o mês e o ano."
        
        # --- A MÁGICA DOS VALIDATORS ACONTECE AQUI ---
        # Pegamos os validadores que o usuário passou (se houver) e adicionamos os nossos padrões
        validators_padrao = [validar_ano_inicio, validar_ano_limite_futuro, validar_mes_range]
        
        if 'validators' in kwargs:
            kwargs['validators'] += validators_padrao
        else:
            kwargs['validators'] = validators_padrao

        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        """
        Agora o compress faz APENAS o trabalho dele: 
        Juntar as peças (Mês + Ano) em um inteiro.
        A validação de negócio acontecerá DEPOIS, automaticamente pelo Django.
        """
        if not data_list:
            return None

        mes, ano = data_list
        
        if mes in [None, ''] or ano in [None, '']:
            return None

        # Apenas garante conversão de tipo
        try:
            mes = int(mes)
            ano = int(ano)
        except ValueError:
            raise ValidationError("Mês e Ano devem ser numéricos.")

        # Retorna o inteiro puro. 
        # O Django vai pegar esse inteiro e passar para a lista de 'validators' definida no __init__
        valor_inteiro = (ano * 100) + mes
        
        # --- AQUI MUDA ---
        # Em vez de retornar o int puro, retornamos o Objeto
        
        # Importação Local para evitar erro circular
        from .models import Competencia 
        
        return Competencia(valor_inteiro)
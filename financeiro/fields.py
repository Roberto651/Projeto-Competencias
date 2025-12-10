# financeiro/fields.py
import datetime
from django import forms
from django.core.exceptions import ValidationError

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


# --- 3. O Field (Lógica de Validação e Processamento) ---
class CompetenciaField(forms.MultiValueField):
    """
    Campo reutilizável que gerencia a validação e conversão 
    de AAAAMM <-> [Mês, Ano].
    """
    widget = CompetenciaWidget

    def __init__(self, **kwargs):
        # Define os validadores para Mês (1-13) e Ano (1900-2100)
        fields = (
            forms.IntegerField(min_value=1, max_value=13),
            forms.IntegerField(min_value=1900, max_value=2100),
        )
        
        # Adiciona um texto de ajuda padrão se não for informado
        if 'help_text' not in kwargs:
            kwargs['help_text'] = "Selecione o mês e o ano."
            
        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        """
        Junta a lista [Mês, Ano] vinda do formulário 
        em um único inteiro AAAAMM para salvar no banco.
        """
        if data_list:
            mes, ano = data_list
            if mes in [None, ''] or ano in [None, '']:
                return None
            
            # Lógica matemática: (Ano * 100) + Mês
            # Ex: (2025 * 100) + 13 = 202500 + 13 = 202513
            return (int(ano) * 100) + int(mes)
        return None
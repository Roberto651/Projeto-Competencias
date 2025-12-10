# financeiro/forms.py
from django import forms
from .models import Lancamento
from .fields import CompetenciaField

class LancamentoForm(forms.ModelForm):
    # O campo especial que criamos
    competencia = CompetenciaField(
        label="Mês/Ano de Referência",
        help_text="Informe a competência contábil."
    )

    class Meta:
        model = Lancamento
        # 1. AQUI você diz quais campos aparecem no formulário
        fields = ['descricao', 'valor', 'competencia'] 
        
        # 2. AQUI você coloca o visual Bootstrap neles (opcional, mas recomendado)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        }
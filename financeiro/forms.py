# financeiro/forms.py
from django import forms
from .models import Lancamento

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        # 1. AQUI você diz quais campos aparecem no formulário
        fields = ['descricao', 'valor', 'competencia'] 
        
        # 2. AQUI você coloca o visual Bootstrap neles (opcional, mas recomendado)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        }
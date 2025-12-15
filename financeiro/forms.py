from django import forms
from .models import Lancamento

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'competencia']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Adiantamento'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0,00'}),
        }
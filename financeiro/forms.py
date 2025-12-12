from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import Lancamento

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'competencia']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Adiantamento'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0,00'}),
        }

    # --- AQUI COMEÇA A VALIDAÇÃO PERSONALIZADA ---
    def clean_competencia(self):
        """
        Este método é chamado automaticamente pelo Django quando você aperta 'Salvar'.
        Ele serve para garantir que o dado é válido para o SEU negócio.
        """
        # 1. Pega o dado bruto que já passou pela validação básica do Field
        # O dado aqui chega como inteiro, ex: 202513
        dado = self.cleaned_data.get('competencia')

        if not dado:
            # Se por algum motivo chegou vazio, deixa o erro padrão do Django agir
            return dado

        # Separamos Ano e Mês matematicamente
        ano = dado // 100
        mes = dado % 100
        
        # Pega o ano atual do sistema
        ano_atual = datetime.date.today().year

        # --- REGRA 1: Validação de Segurança do Mês (Redundância) ---
        if not (1 <= mes <= 13):
            raise ValidationError("O mês deve ser entre 1 (Janeiro) e 13 (13º Salário).")

        # --- REGRA 2: Não aceitar anos muito antigos (Ex: Regra da Empresa) ---
        # Digamos que o sistema só aceita dados a partir de 2020
        if ano < 1900:
            raise ValidationError(f"Não é permitido lançamentos anteriores a 1900. Você digitou {ano}.")

        # --- REGRA 3: Não aceitar futuro muito distante (Erro de Digitação) ---
        # Impede que alguém digite 2052 em vez de 2025
        if ano > (ano_atual + 2):
            raise ValidationError(f"O ano {ano} está muito no futuro. Verifique se não houve erro de digitação.")

        # Se passou por tudo, retorna o dado para ser salvo
        return dado

    def clean_valor(self):
        """
        Podemos validar o valor também. Exemplo: Não aceitar valor negativo.
        """
        valor = self.cleaned_data.get('valor')
        
        if valor and valor < 0:
            raise ValidationError("O valor do lançamento não pode ser negativo.")
            
        return valor
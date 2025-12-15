import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_ano_inicio(valor):
    """
    Valida se a competência (inteiro AAAAMM) não é anterior a 2020.
    """
    if not valor:
        return
    
    # Extrai o ano: 202513 // 100 = 2025
    ano = valor // 100
    
    if ano < 2020:
        raise ValidationError(
            _('Lançamentos anteriores a 2020 não são permitidos. (Ano: %(valor)s)'),
            params={'valor': ano},
        )

def validar_ano_limite_futuro(valor):
    """
    Valida se a competência não está muito no futuro (Ano atual + 5).
    """
    if not valor:
        return

    ano = valor // 100
    ano_atual = datetime.date.today().year
    limite = ano_atual + 5

    if ano > limite:
        raise ValidationError(
            _('O ano %(valor)s está muito no futuro (Limite: %(limite)s).'),
            params={'valor': ano, 'limite': limite},
        )

def validar_mes_range(valor):
    """
    Garante que o mês (a parte final do inteiro) está entre 1 e 13.
    """
    if not valor:
        return
        
    mes = valor % 100
    if not (1 <= mes <= 13):
        raise ValidationError(
            _('Mês inválido: %(valor)s. Deve ser entre 1 e 13.'),
            params={'valor': mes},
        )
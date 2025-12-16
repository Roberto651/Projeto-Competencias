import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_ano_inicio(valor):
    """
    Valida se a competência não é anterior a 2020.
    Aceita tanto int (202513) quanto objeto Competencia.
    """
    if not valor:
        return
    
    # CORREÇÃO: Verifica se tem a propriedade .ano, senão faz a conta
    if hasattr(valor, 'ano'):
        ano = valor.ano
    else:
        ano = int(valor) // 100
    
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

    # CORREÇÃO: Usa a propriedade .ano do objeto
    if hasattr(valor, 'ano'):
        ano = valor.ano
    else:
        ano = int(valor) // 100

    ano_atual = datetime.date.today().year
    limite = ano_atual + 5

    if ano > limite:
        raise ValidationError(
            _('O ano %(valor)s está muito no futuro (Limite: %(limite)s).'),
            params={'valor': ano, 'limite': limite},
        )

def validar_mes_range(valor):
    """
    Garante que o mês está entre 1 e 13.
    """
    if not valor:
        return
        
    # CORREÇÃO: Usa a propriedade .mes do objeto
    if hasattr(valor, 'mes'):
        mes = valor.mes
    else:
        mes = int(valor) % 100

    if not (1 <= mes <= 13):
        raise ValidationError(
            _('Mês inválido: %(valor)s. Deve ser entre 1 e 13.'),
            params={'valor': mes},
        )
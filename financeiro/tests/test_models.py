import pytest
from django.core.exceptions import ValidationError
from financeiro.models import Lancamento, Competencia
from financeiro.forms import LancamentoForm

@pytest.mark.django_db
class TestLancamentoModel:

    def test_salvar_e_recuperar(self):
        """Testa se o Custom Field converte int <-> Objeto no banco"""
        lanc = Lancamento.objects.create(
            descricao="Teste Pytest",
            valor=100.00,
            competencia=202513 # Passando int
        )

        # Recarrega do banco
        lanc.refresh_from_db()

        # Verifica se voltou como Objeto Rico
        assert isinstance(lanc.competencia, Competencia)
        assert lanc.competencia.ano == 2025
        assert lanc.competencia.mes == 13
        assert lanc.competencia.descricao_mes == "13º Salário"

    def test_filtrar_queryset(self):
        """Testa se conseguimos filtrar usando o objeto ou int"""
        Lancamento.objects.create(descricao="A", valor=10, competencia=202501)
        Lancamento.objects.create(descricao="B", valor=10, competencia=202513)

        # Filtra usando int
        assert Lancamento.objects.filter(competencia=202513).exists()
        
        # Filtra usando Objeto
        obj_comp = Competencia(2025, 1)
        assert Lancamento.objects.filter(competencia=obj_comp).exists()


@pytest.mark.django_db
class TestLancamentoFormValidators:
    
    def test_form_valido(self):
        """Testa um formulário preenchido corretamente"""
        data = {
            'descricao': 'Pagamento OK',
            'valor': '500.00',
            'competencia_0': '13',   # Mês
            'competencia_1': '2025'  # Ano
        }
        form = LancamentoForm(data=data)
        assert form.is_valid()
        
        # Verifica se o dado limpo é o objeto Competencia
        cleaned_comp = form.cleaned_data['competencia']
        assert isinstance(cleaned_comp, Competencia)
        assert cleaned_comp == 202513

    def test_validador_ano_minimo(self):
        """Testa se rejeita ano < 2020 (conforme definimos nos validators)"""
        data = {
            'descricao': 'Teste Antigo',
            'valor': '100',
            'competencia_0': '1',
            'competencia_1': '2019' # Inválido
        }
        form = LancamentoForm(data=data)
        assert not form.is_valid()
        assert "Lançamentos anteriores a 2020" in form.errors['competencia'][0]

    def test_validador_ano_futuro(self):
        """Testa se rejeita ano muito no futuro"""
        data = {
            'descricao': 'Teste Futuro',
            'valor': '100',
            'competencia_0': '1',
            'competencia_1': '2099' # Inválido
        }
        form = LancamentoForm(data=data)
        assert not form.is_valid()
        assert "está muito no futuro" in form.errors['competencia'][0]
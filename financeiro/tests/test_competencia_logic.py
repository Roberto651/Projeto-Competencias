import pytest
from financeiro.models import Competencia

class TestCompetenciaLogic:
    
    def test_criacao_padrao(self):
        """Testa se cria corretamente via (ano, mes)"""
        c = Competencia(2025, 13)
        assert c.ano == 2025
        assert c.mes == 13
        assert c.as_int == 202513
        assert str(c) == "13/2025"

    def test_factory_from_int(self):
        """Testa se cria corretamente via inteiro (banco de dados)"""
        c = Competencia.from_int(202505)
        assert c.ano == 2025
        assert c.mes == 5

    def test_validacao_limite_mes(self):
        """Testa se o LIMITE_MES (13) é respeitado"""
        # Mês 13 deve passar
        assert Competencia(2025, 13)
        
        # Mês 14 deve falhar
        with pytest.raises(ValueError) as excinfo:
            Competencia(2025, 14)
        assert "Mês 14 inválido" in str(excinfo.value)

    def test_navegacao_proxima(self):
        """Testa a virada de ano (12 -> 13 -> 01)"""
        # Dezembro -> 13º
        c_dez = Competencia(2025, 12)
        assert c_dez.proxima == Competencia(2025, 13)
        
        # 13º -> Janeiro do próximo ano
        c_13 = Competencia(2025, 13)
        assert c_13.proxima == Competencia(2026, 1)

    def test_navegacao_anterior(self):
        """Testa voltar no tempo (01 -> 13 anterior)"""
        c_jan = Competencia(2026, 1)
        assert c_jan.anterior == Competencia(2025, 13)

    def test_comparacao(self):
        """Testa operadores <, >, =="""
        c1 = Competencia(2025, 13)
        c2 = Competencia(2026, 1)
        
        assert c1 < c2
        assert c2 > c1
        assert c1 != c2
        # Testa igualdade com inteiro puro
        assert c1 == 202513 

    def test_aritmetica_soma(self):
        """Testa somar meses (pula anos se necessário)"""
        base = Competencia(2025, 13) # 13º de 2025
        
        # + 1 mês = Janeiro 2026
        assert (base + 1) == Competencia(2026, 1)
        
        # + 13 meses = 13º de 2026
        assert (base + 13) == Competencia(2026, 13)

    def test_aritmetica_subtracao_datas(self):
        """Testa a diferença entre duas datas"""
        futuro = Competencia(2026, 2)
        passado = Competencia(2025, 13)
        # Diferença: 13/25 -> 01/26 -> 02/26 = 2 passos
        assert (futuro - passado) == 2
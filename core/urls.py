from django.contrib import admin
from django.urls import path
# AQUI ESTÁ A CORREÇÃO:
from financeiro.views import CriarLancamentoView, ListaLancamentosView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CriarLancamentoView.as_view(), name='criar_lancamento'),
    path('lista/', ListaLancamentosView.as_view(), name='lista_lancamentos'),
]
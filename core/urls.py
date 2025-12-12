from django.contrib import admin
from django.urls import path
from financeiro.views import CriarLancamentoView, ListaLancamentosView, LancamentoEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CriarLancamentoView.as_view(), name='criar_lancamento'),
    path('lista/', ListaLancamentosView.as_view(), name='lista_lancamentos'),
    path('editar/<int:pk>/', LancamentoEditView.as_view(), name='editar_lancamento'),
]
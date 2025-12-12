from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Lancamento
from .forms import LancamentoForm

class CriarLancamentoView(CreateView):
    model = Lancamento
    form_class = LancamentoForm
    #fields = ["valor", "descricao", "competencia"]
    template_name = 'form.html'
    success_url = reverse_lazy('lista_lancamentos') # Redireciona após salvar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Novo Lançamento Financeiro"
        return context
    

class LancamentoEditView(UpdateView):
    model = Lancamento
    form_class = LancamentoForm
    template_name = 'form.html'
    success_url = reverse_lazy('lista_lancamentos') #



class ListaLancamentosView(ListView):
    model = Lancamento
    template_name = 'lista.html'
    context_object_name = 'lancamentos'
    ordering = ['-competencia']
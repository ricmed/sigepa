from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Ocorrencia, EvolucaoTratamento, Cbo, Cid, Estabelecimentos,
    TipoNotificacao, Estado, Municipios, Sexo, TempoGestacao, Raca,
    PovoTradicional, Escolaridade, Pais, Zona, TipoEscalpelamento,
    TipoCausaAcidente, TipoTransporte, TipoComplicacao, TipoProcedimento,
    TipoRegimeAtendimento, TipoEvolucaoCaso, TipoParteAtingida
)
from .forms import (
    OcorrenciaForm, EvolucaoTratamentoForm, EvolucaoTratamentoComplicacaoFormSet,
    EvolucaoTratamentoProcedimentoFormSet, OcorrenciaParteAtingidaFormSet
)


class OcorrenciaListView(LoginRequiredMixin, ListView):
    """Lista de ocorrências com paginação e busca"""
    model = Ocorrencia
    template_name = 'core/ocorrencia_list.html'
    context_object_name = 'ocorrencias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Ocorrencia.objects.select_related(
            'tipo_notificacao', 'id_uf_notificacao', 'id_municipio_notificacao',
            'id_cnes', 'id_sexo', 'id_tempo_gestacao', 'id_raca'
        ).order_by('-data_notificacao')
        
        # Busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_paciente__icontains=search) |
                Q(num_registro__icontains=search) |
                Q(cartao_sus__icontains=search) |
                Q(cpf__icontains=search)
            )
        
        # Filtros
        tipo_notificacao = self.request.GET.get('tipo_notificacao')
        if tipo_notificacao:
            queryset = queryset.filter(tipo_notificacao_id=tipo_notificacao)
            
        uf = self.request.GET.get('uf')
        if uf:
            queryset = queryset.filter(id_uf_notificacao_id=uf)
            
        municipio = self.request.GET.get('municipio')
        if municipio:
            queryset = queryset.filter(id_municipio_notificacao_id=municipio)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_notificacao'] = TipoNotificacao.objects.all()
        context['estados'] = Estado.objects.all()
        context['municipios'] = Municipios.objects.all()
        return context


class OcorrenciaDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de uma ocorrência"""
    model = Ocorrencia
    template_name = 'core/ocorrencia_detail.html'
    context_object_name = 'ocorrencia'
    
    def get_queryset(self):
        return Ocorrencia.objects.select_related(
            'tipo_notificacao', 'id_uf_notificacao', 'id_municipio_notificacao',
            'id_cnes', 'id_sexo', 'id_tempo_gestacao', 'id_raca', 'id_povo_tradicional',
            'id_cbo', 'id_escolaridade', 'id_pais', 'id_uf_residencia',
            'id_municipio_residencia', 'id_zona', 'id_cid', 'id_tipo_escalpelamento',
            'id_causa_acidente', 'id_municipio_ocorrencia', 'id_uf_transferencia',
            'id_municipio_transferencia', 'id_tipo_transporte', 'id_municipio_investigador',
            'id_cnes_invertigador'
        ).prefetch_related('evolucaotratamento_set')


class OcorrenciaCreateView(LoginRequiredMixin, CreateView):
    """Criar nova ocorrência"""
    model = Ocorrencia
    form_class = OcorrenciaForm
    template_name = 'core/ocorrencia_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Ocorrência'
        context['button_text'] = 'Salvar'
        return context
    
    def form_valid(self, form):
        # Processar campos ForeignKey com autocomplete
        # Os IDs são enviados em campos hidden com sufixo _id
        for field_name in ['id_cnes', 'id_cbo', 'id_cid', 'id_cnes_invertigador']:
            hidden_field_name = f"{field_name}_id"
            if hidden_field_name in self.request.POST:
                field_id = self.request.POST.get(hidden_field_name)
                if field_id:
                    # Atualizar o campo ForeignKey com o ID correto
                    form.instance.__dict__[field_name + '_id'] = field_id
        
        messages.success(self.request, 'Ocorrência criada com sucesso!')
        return super().form_valid(form)


class OcorrenciaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar ocorrência existente"""
    model = Ocorrencia
    form_class = OcorrenciaForm
    template_name = 'core/ocorrencia_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Ocorrência'
        context['button_text'] = 'Atualizar'
        
        # Formsets para relações Many-to-Many
        if self.object:
            context['parte_atingida_formset'] = OcorrenciaParteAtingidaFormSet(
                instance=self.object
            )
        
        return context
    
    def form_valid(self, form):
        # Processar campos ForeignKey com autocomplete
        # Os IDs são enviados em campos hidden com sufixo _id
        for field_name in ['id_cnes', 'id_cbo', 'id_cid', 'id_cnes_invertigador']:
            hidden_field_name = f"{field_name}_id"
            if hidden_field_name in self.request.POST:
                field_id = self.request.POST.get(hidden_field_name)
                if field_id:
                    # Atualizar o campo ForeignKey com o ID correto
                    form.instance.__dict__[field_name + '_id'] = field_id
        
        messages.success(self.request, 'Ocorrência atualizada com sucesso!')
        return super().form_valid(form)


class OcorrenciaDeleteView(LoginRequiredMixin, DeleteView):
    """Excluir ocorrência"""
    model = Ocorrencia
    template_name = 'core/ocorrencia_confirm_delete.html'
    success_url = reverse_lazy('core:ocorrencia_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ocorrência excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# Views para Evolução do Tratamento
class EvolucaoTratamentoCreateView(LoginRequiredMixin, CreateView):
    """Criar evolução do tratamento"""
    model = EvolucaoTratamento
    form_class = EvolucaoTratamentoForm
    template_name = 'core/evolucao_tratamento_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Evolução do Tratamento'
        context['button_text'] = 'Salvar'
        
        # Formsets para relações Many-to-Many
        context['complicacao_formset'] = EvolucaoTratamentoComplicacaoFormSet()
        context['procedimento_formset'] = EvolucaoTratamentoProcedimentoFormSet()
        
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            
            # Salvar formsets
            complicacao_formset = EvolucaoTratamentoComplicacaoFormSet(
                self.request.POST, instance=self.object
            )
            procedimento_formset = EvolucaoTratamentoProcedimentoFormSet(
                self.request.POST, instance=self.object
            )
            
            if complicacao_formset.is_valid() and procedimento_formset.is_valid():
                complicacao_formset.save()
                procedimento_formset.save()
                messages.success(self.request, 'Evolução do tratamento criada com sucesso!')
            else:
                messages.error(self.request, 'Erro ao salvar evolução do tratamento.')
                
        return response


# Views para APIs de autocomplete
@csrf_exempt
def autocomplete_cbo(request):
    """API para autocomplete de CBO"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    cbos = Cbo.objects.filter(
        Q(codigo__icontains=query) | Q(titulo__icontains=query)
    )[:10]
    
    results = []
    for cbo in cbos:
        results.append({
            'id': cbo.codigo,
            'text': f"{cbo.codigo} - {cbo.titulo}"
        })
    
    return JsonResponse({'results': results})


@csrf_exempt
def autocomplete_cid(request):
    """API para autocomplete de CID"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    cids = Cid.objects.filter(
        Q(cod_categoria__icontains=query) | 
        Q(cod_subcategoria__icontains=query) |
        Q(desc_categoria__icontains=query) |
        Q(desc_subcategoria__icontains=query)
    )[:10]
    
    results = []
    for cid in cids:
        codigo = f"{cid.cod_categoria}.{cid.cod_subcategoria}" if cid.cod_subcategoria else cid.cod_categoria
        descricao = cid.desc_subcategoria or cid.desc_categoria
        results.append({
            'id': cid.sk_causa,
            'text': f"{codigo} - {descricao}"
        })
    
    return JsonResponse({'results': results})


@csrf_exempt
def autocomplete_estabelecimentos(request):
    """API para autocomplete de Estabelecimentos"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    estabelecimentos = Estabelecimentos.objects.filter(
        Q(co_cnes__icontains=query) | 
        Q(no_fantasia__icontains=query) |
        Q(nu_cnpj__icontains=query)
    )[:10]
    
    results = []
    for est in estabelecimentos:
        results.append({
            'id': est.co_unidade,
            'text': f"{est.co_cnes} - {est.no_fantasia or 'Sem nome'}"
        })
    
    return JsonResponse({'results': results})


# View para carregar municípios por estado
@csrf_exempt
def load_municipios(request):
    """Carregar municípios por estado"""
    estado_id = request.GET.get('estado_id')
    if estado_id:
        municipios = Municipios.objects.filter(id_uf_id=estado_id).order_by('nome_municipio')
        data = [{'id': m.id_municipio, 'nome': m.nome_municipio} for m in municipios]
        return JsonResponse({'municipios': data})
    return JsonResponse({'municipios': []})
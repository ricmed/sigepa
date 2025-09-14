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
    """API para autocomplete de CBO com paginação"""
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    per_page = 10
    
    # Filtrar CBOs
    cbos_query = Cbo.objects.all().order_by('codigo')
    if query:
        cbos_query = cbos_query.filter(
            Q(codigo__icontains=query) | Q(titulo__icontains=query)
        )
    
    # Aplicar paginação
    paginator = Paginator(cbos_query, per_page)
    try:
        cbos_page = paginator.page(page)
    except:
        cbos_page = paginator.page(1)
    
    results = []
    for cbo in cbos_page.object_list:
        results.append({
            'id': cbo.codigo,
            'text': f"{cbo.codigo} - {cbo.titulo}"
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'current_page': cbos_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': cbos_page.has_next(),
            'has_previous': cbos_page.has_previous()
        }
    })


@csrf_exempt
def autocomplete_cid(request):
    """API para autocomplete de CID com paginação"""
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    per_page = 10
    
    # Filtrar CIDs
    cids_query = Cid.objects.all().order_by('cod_categoria', 'cod_subcategoria')
    if query:
        cids_query = cids_query.filter(
            Q(cod_categoria__icontains=query) | 
            Q(cod_subcategoria__icontains=query) |
            Q(desc_categoria__icontains=query) |
            Q(desc_subcategoria__icontains=query)
        )
    
    # Aplicar paginação
    paginator = Paginator(cids_query, per_page)
    try:
        cids_page = paginator.page(page)
    except:
        cids_page = paginator.page(1)
    
    results = []
    for cid in cids_page.object_list:
        codigo = f"{cid.cod_categoria}.{cid.cod_subcategoria}" if cid.cod_subcategoria else cid.cod_categoria
        descricao = cid.desc_subcategoria or cid.desc_categoria
        results.append({
            'id': cid.sk_causa,
            'text': f"{codigo} - {descricao}"
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'current_page': cids_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': cids_page.has_next(),
            'has_previous': cids_page.has_previous()
        }
    })


@csrf_exempt
def autocomplete_estabelecimentos(request):
    """API para autocomplete de Estabelecimentos com paginação"""
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    per_page = 10
    
    # Filtrar estabelecimentos
    estabelecimentos_query = Estabelecimentos.objects.all().order_by('co_cnes')
    if query:
        estabelecimentos_query = estabelecimentos_query.filter(
            Q(co_cnes__icontains=query) | 
            Q(no_fantasia__icontains=query) |
            Q(nu_cnpj__icontains=query)
        )
    
    # Aplicar paginação
    paginator = Paginator(estabelecimentos_query, per_page)
    try:
        estabelecimentos_page = paginator.page(page)
    except:
        estabelecimentos_page = paginator.page(1)
    
    results = []
    for est in estabelecimentos_page.object_list:
        results.append({
            'id': est.co_unidade,
            'text': f"{est.co_cnes} - {est.no_fantasia or 'Sem nome'}"
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'current_page': estabelecimentos_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': estabelecimentos_page.has_next(),
            'has_previous': estabelecimentos_page.has_previous()
        }
    })


# View para carregar municípios por estado
@csrf_exempt
def load_municipios(request):
    """Carregar municípios por estado"""
    try:
        estado_id = request.GET.get('estado_id')
        print(f"🔍 Carregando municípios para estado_id: {estado_id}")
        
        if not estado_id:
            print("⚠️ Estado ID não fornecido")
            return JsonResponse({
                'municipios': [],
                'error': 'Estado ID não fornecido'
            })
        
        # Verificar se o estado existe
        try:
            estado = Estado.objects.get(idestado=estado_id)
            print(f"📍 Estado encontrado: {estado.descricao}")
        except Estado.DoesNotExist:
            print(f"❌ Estado não encontrado: {estado_id}")
            return JsonResponse({
                'municipios': [],
                'error': f'Estado {estado_id} não encontrado'
            })
        
        # Buscar municípios
        municipios = Municipios.objects.filter(id_uf_id=estado_id).order_by('nome_municipio')
        count = municipios.count()
        print(f"📊 Encontrados {count} municípios para estado {estado_id}")
        
        data = []
        for m in municipios:
            if m.nome_municipio:  # Verificar se o nome não é None
                data.append({
                    'id': m.id_municipio, 
                    'nome': m.nome_municipio
                })
        
        result = {
            'municipios': data,
            'success': True
        }
        
        print(f"✅ Retornando {len(data)} municípios válidos")
        return JsonResponse(result)
            
    except Exception as e:
        print(f"❌ Erro ao carregar municípios: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e), 
            'municipios': [],
            'success': False
        }, status=500)
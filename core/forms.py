from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.core.exceptions import ValidationError
from datetime import date
from .models import (
    Ocorrencia, EvolucaoTratamento, EvolucaoTratamentoHasTipoComplicacao,
    EvolucaoTratamentoHasTipoProcedimento, OcorrenciaHasTipoParteAtingida,
    TipoNotificacao, Estado, Municipios, Estabelecimentos, Sexo, TempoGestacao,
    Raca, PovoTradicional, Cbo, Escolaridade, Pais, Zona, Cid, TipoEscalpelamento,
    TipoCausaAcidente, TipoTransporte, TipoComplicacao, TipoProcedimento,
    TipoRegimeAtendimento, TipoEvolucaoCaso, TipoParteAtingida
)


class OcorrenciaForm(ModelForm):
    """Formulário principal para Ocorrencia com campos de autocomplete otimizados"""

    class Meta:
        model = Ocorrencia
        fields = '__all__'
        widgets = {
            # Aba 1: Dados da Notificação
            'tipo_notificacao': forms.Select(attrs={'class': 'form-select'}),
            'data_notificacao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_notificacao'}),
            'id_uf_notificacao': forms.Select(attrs={'class': 'form-select'}),
            'id_municipio_notificacao': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes': forms.Select(attrs={'class': 'form-control'}),
            'data_acidente': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_acidente'}),
            'data_cadastro': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_cadastro'}),

            # Aba 2: Dados do Paciente
            'nome_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_nascimento'}),
            'idade': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'id_sexo': forms.Select(attrs={'class': 'form-select'}),
            'id_tempo_gestacao': forms.Select(attrs={'class': 'form-select'}),
            'id_raca': forms.Select(attrs={'class': 'form-select'}),
            'id_povo_tradicional': forms.Select(attrs={'class': 'form-select'}),
            'outros_povo_tradicional': forms.TextInput(attrs={'class': 'form-control'}),    
            'cartao_sus': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'id_cbo': forms.Select(attrs={'class': 'form-control'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'id_escolaridade': forms.Select(attrs={'class': 'form-select'}),
            'id_pais': forms.Select(attrs={'class': 'form-select'}),

            # Aba 3: Endereço
            'id_uf_residencia': forms.Select(attrs={'class': 'form-select'}),
            'id_municipio_residencia': forms.Select(attrs={'class': 'form-select'}),
            'distrito': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '5'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'geo_campo1': forms.TextInput(attrs={'class': 'form-control'}),
            'geo_campo2': forms.TextInput(attrs={'class': 'form-control'}),
            'ponto_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'id_zona': forms.Select(attrs={'class': 'form-select'}),

            # Aba 4: Dados do Acidente
            'num_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_motor': forms.TextInput(attrs={'class': 'form-control'}),
            'data_investigacao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_investigacao'}),
            'nome_dono': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_dono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'nome_condutor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_condutor': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'data_atendimento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_atendimento'}),
            'id_cid': forms.Select(attrs={'class': 'form-control'}),
            'id_tipo_escalpelamento': forms.Select(attrs={'class': 'form-select'}),
            'id_causa_acidente': forms.Select(attrs={'class': 'form-select'}),
            'causa_acidente_outros': forms.TextInput(attrs={'class': 'form-control'}),
            'info_atendimento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'id_municipio_ocorrencia': forms.Select(attrs={'class': 'form-select'}),

            # Aba 5: Transferência
            'transferencia_hospitalar': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Selecione...'), ('S', 'Sim'), ('N', 'Não')]),
            'data_transferencia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_transferencia'}),
            'id_uf_transferencia': forms.Select(attrs={'class': 'form-select'}),
            'id_municipio_transferencia': forms.Select(attrs={'class': 'form-select'}),
            'unidade_transferencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_tipo_transporte': forms.Select(attrs={'class': 'form-select'}),
            'data_cadastro_atendimento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_cadastro_atendimento'}),

            # Aba 6: Investigador
            'id_municipio_investigador': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes_invertigador': forms.Select(attrs={'class': 'form-control'}),
            'nome_invertigador': forms.TextInput(attrs={'class': 'form-control'}),
            'funcao_invertigador': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar querysets para campos de autocomplete
        autocomplete_fields = {
            'id_cnes': Estabelecimentos,
            'id_cbo': Cbo,
            'id_cid': Cid,
            'id_cnes_invertigador': Estabelecimentos,
            'funcao_invertigador': Cbo,
        }

        for field_name, model in autocomplete_fields.items():
            if field_name in self.fields:
                if self.instance and self.instance.pk:
                    # Se estiver editando, mostrar apenas a opção gravada (se existir)
                    current_value = getattr(self.instance, field_name, None)
                    if current_value:
                        # Se há valor gravado, mostrar apenas essa opção
                        self.fields[field_name].queryset = model.objects.filter(pk=current_value.pk)
                        self.fields[field_name].initial = current_value.pk
                        self.fields[field_name].empty_label = "Selecione..."
                    else:
                        # Se não há valor gravado, campo fica vazio
                        self.fields[field_name].queryset = model.objects.none()
                        self.fields[field_name].empty_label = "Use a pesquisa para selecionar"
                else:
                    # Para novo registro, iniciar com queryset vazio
                    # Os itens serão carregados dinamicamente via JavaScript conforme necessário
                    self.fields[field_name].queryset = model.objects.none()
                    self.fields[field_name].empty_label = "Use a pesquisa para selecionar"

        # Configurar campos de UF - sempre carregar todos os estados
        uf_fields = ['id_uf_notificacao', 'id_uf_residencia', 'id_uf_transferencia']
        for field_name in uf_fields:
            if field_name in self.fields:
                self.fields[field_name].queryset = Estado.objects.all().order_by('descricao')
                self.fields[field_name].empty_label = "Selecione..."

        # Configurar campos de município para carregamento dinâmico
        municipio_fields = ['id_municipio_notificacao', 'id_municipio_residencia', 'id_municipio_transferencia', 'id_municipio_ocorrencia', 'id_municipio_investigador']
        for field_name in municipio_fields:
            if field_name in self.fields:
                if self.instance and self.instance.pk:
                    # Se estiver editando, carregar todos os municípios para permitir mudança
                    # mas manter o valor atual selecionado
                    self.fields[field_name].queryset = Municipios.objects.all()
                    self.fields[field_name].empty_label = "Selecione..."
                    
                    # Garantir que o valor atual seja mantido
                    current_value = getattr(self.instance, field_name, None)
                    if current_value:
                        # Forçar o valor inicial para garantir que apareça no formulário
                        self.fields[field_name].initial = current_value.pk
                else:
                    # Para novo registro, iniciar com queryset vazio
                    # Os municípios serão carregados dinamicamente via JavaScript conforme UF selecionada
                    self.fields[field_name].queryset = Municipios.objects.none()
                    self.fields[field_name].empty_label = "Selecione uma UF primeiro"

        # Configurar campos de data para garantir carregamento correto na edição
        if self.instance and self.instance.pk:
            date_fields = ['data_notificacao', 'data_acidente', 'data_cadastro', 'data_nascimento', 
                          'data_investigacao', 'data_atendimento', 'data_transferencia', 'data_cadastro_atendimento']
            for field_name in date_fields:
                if field_name in self.fields:
                    current_value = getattr(self.instance, field_name, None)
                    if current_value:
                        # Garantir que o valor da data seja mantido no formato correto
                        # Para campos de data, usar o valor diretamente
                        self.fields[field_name].initial = current_value

        # Configurar campos obrigatórios
        self.fields['tipo_notificacao'].required = True
        self.fields['data_notificacao'].required = True
        self.fields['id_uf_notificacao'].required = True
        self.fields['id_municipio_notificacao'].required = True
        self.fields['id_cnes'].required = True
        self.fields['nome_paciente'].required = True
        self.fields['id_sexo'].required = True
        self.fields['id_tempo_gestacao'].required = True
        self.fields['id_raca'].required = True
        self.fields['num_registro'].required = True
        self.fields['nome_invertigador'].required = True

    def full_clean(self):
        """
        Override para garantir que os querysets sejam atualizados
        durante a validação caso tenham sido carregados dinamicamente
        """
        # Atualizar querysets de municípios para validação
        municipio_fields = ['id_municipio_notificacao', 'id_municipio_residencia', 'id_municipio_transferencia', 'id_municipio_ocorrencia', 'id_municipio_investigador']
        for field_name in municipio_fields:
            if field_name in self.fields and field_name in self.data:
                # Se há dados para o campo, garantir que o queryset inclui todos os municípios
                self.fields[field_name].queryset = Municipios.objects.all()
        
        # Atualizar querysets de campos de autocomplete para validação
        autocomplete_fields = {
            'id_cnes': Estabelecimentos,
            'id_cbo': Cbo,
            'id_cid': Cid,
            'id_cnes_invertigador': Estabelecimentos,
            'funcao_invertigador': Cbo,
        }
        
        for field_name, model in autocomplete_fields.items():
            if field_name in self.fields and field_name in self.data:
                # Se há dados para o campo, garantir que o queryset inclui todos os registros
                # Isso permite que a validação funcione mesmo quando o campo foi populado via modal
                self.fields[field_name].queryset = model.objects.all()
        
        super().full_clean()
    
    def clean_data_notificacao(self):
        """Valida que a data de notificação não seja no futuro"""
        data = self.cleaned_data.get('data_notificacao')
        if data and data > date.today():
            raise ValidationError('A data de notificação não pode ser no futuro.')
        return data
    
    def clean_data_acidente(self):
        """Valida que a data do acidente não seja no futuro"""
        data = self.cleaned_data.get('data_acidente')
        if data and data > date.today():
            raise ValidationError('A data do acidente não pode ser no futuro.')
        return data
    
    def clean_data_cadastro(self):
        """Valida que a data de cadastro não seja no futuro"""
        data = self.cleaned_data.get('data_cadastro')
        if data and data > date.today():
            raise ValidationError('A data de cadastro não pode ser no futuro.')
        return data
    
    def clean_data_nascimento(self):
        """Valida que a data de nascimento não seja no futuro"""
        data = self.cleaned_data.get('data_nascimento')
        if data and data > date.today():
            raise ValidationError('A data de nascimento não pode ser no futuro.')
        return data
    
    def clean_data_investigacao(self):
        """Valida que a data de investigação não seja no futuro"""
        data = self.cleaned_data.get('data_investigacao')
        if data and data > date.today():
            raise ValidationError('A data de investigação não pode ser no futuro.')
        return data
    
    def clean_data_atendimento(self):
        """Valida que a data de atendimento não seja no futuro"""
        data = self.cleaned_data.get('data_atendimento')
        if data and data > date.today():
            raise ValidationError('A data de atendimento não pode ser no futuro.')
        return data
    
    def clean_data_transferencia(self):
        """Valida que a data de transferência não seja no futuro"""
        data = self.cleaned_data.get('data_transferencia')
        if data and data > date.today():
            raise ValidationError('A data de transferência não pode ser no futuro.')
        return data
    
    def clean_data_cadastro_atendimento(self):
        """Valida que a data de cadastro do atendimento não seja no futuro"""
        data = self.cleaned_data.get('data_cadastro_atendimento')
        if data and data > date.today():
            raise ValidationError('A data de cadastro do atendimento não pode ser no futuro.')
        return data



class EvolucaoTratamentoForm(ModelForm):
    """Formulário para Evolução do Tratamento"""
    
    class Meta:
        model = EvolucaoTratamento
        fields = '__all__'
        widgets = {
            'ocorrencia': forms.HiddenInput(),
            'id_unidade_atendimento': forms.Select(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_entrada'}),
            'outros_procedimentos': forms.TextInput(attrs={'class': 'form-control'}),
            'outros_complicacoes': forms.TextInput(attrs={'class': 'form-control'}),
            'espaco_acolher': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Selecione...'), ('S', 'Sim'), ('N', 'Não')]),
            'data_entrada_espaco_acolher': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_entrada_espaco_acolher'}),
            'data_saida_espaco_acolher': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_saida_espaco_acolher'}),
            'id_regime_atendimento': forms.Select(attrs={'class': 'form-select'}),
            'id_evolucao_caso': forms.Select(attrs={'class': 'form-select'}),
            'data_obito': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_obito'}),
            'data_encerramento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_encerramento'}),
            'evolucao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'id_municipio_investigacao': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes_investigacao': forms.Select(attrs={'class': 'form-control'}),
            'nome_investigador': forms.TextInput(attrs={'class': 'form-control'}),
            'id_funcao_investigador': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar querysets para campos de autocomplete
        autocomplete_fields = {
            'id_unidade_atendimento': Estabelecimentos,
            'id_cnes_investigacao': Estabelecimentos,
            'id_funcao_investigador': Cbo,
        }

        for field_name, model in autocomplete_fields.items():
            if field_name in self.fields:
                if self.instance and self.instance.pk:
                    # Se estiver editando, mostrar apenas a opção gravada (se existir)
                    current_value = getattr(self.instance, field_name, None)
                    if current_value:
                        # Se há valor gravado, mostrar apenas essa opção
                        self.fields[field_name].queryset = model.objects.filter(pk=current_value.pk)
                        self.fields[field_name].initial = current_value.pk
                        self.fields[field_name].empty_label = "Selecione..."
                    else:
                        # Se não há valor gravado, campo fica vazio
                        self.fields[field_name].queryset = model.objects.none()
                        self.fields[field_name].empty_label = "Use a pesquisa para selecionar"
                else:
                    # Para novo registro, iniciar com queryset vazio
                    # Os itens serão carregados dinamicamente via JavaScript conforme necessário
                    self.fields[field_name].queryset = model.objects.none()
                    self.fields[field_name].empty_label = "Use a pesquisa para selecionar"
        
        # Configurar campos de data para garantir carregamento correto na edição
        if self.instance and self.instance.pk:
            date_fields = ['data_entrada', 'data_entrada_espaco_acolher', 'data_saida_espaco_acolher', 
                          'data_obito', 'data_encerramento']
            for field_name in date_fields:
                if field_name in self.fields:
                    current_value = getattr(self.instance, field_name, None)
                    if current_value:
                        # Garantir que o valor da data seja mantido no formato correto
                        # Para campos de data, usar o valor diretamente
                        self.fields[field_name].initial = current_value

        # Configurar campos obrigatórios
        self.fields['outros_complicacoes'].required = True
        self.fields['nome_investigador'].required = True

    def full_clean(self):
        """
        Override para garantir que os querysets de autocomplete sejam atualizados
        durante a validação caso tenham sido carregados dinamicamente
        """
        # Atualizar querysets de campos de autocomplete para validação
        autocomplete_fields = {
            'id_unidade_atendimento': Estabelecimentos,
            'id_cnes_investigacao': Estabelecimentos,
            'id_funcao_investigador': Cbo,
        }
        
        for field_name, model in autocomplete_fields.items():
            if field_name in self.fields and field_name in self.data:
                # Se há dados para o campo, garantir que o queryset inclui todos os registros
                # Isso permite que a validação funcione mesmo quando o campo foi populado via modal
                self.fields[field_name].queryset = model.objects.all()
        
        super().full_clean()
    
    def clean_data_entrada(self):
        """Valida que a data de entrada não seja no futuro"""
        data = self.cleaned_data.get('data_entrada')
        if data and data > date.today():
            raise ValidationError('A data de entrada não pode ser no futuro.')
        return data
    
    def clean_data_entrada_espaco_acolher(self):
        """Valida que a data de entrada no espaço acolher não seja no futuro"""
        data = self.cleaned_data.get('data_entrada_espaco_acolher')
        if data and data > date.today():
            raise ValidationError('A data de entrada no espaço acolher não pode ser no futuro.')
        return data
    
    def clean_data_saida_espaco_acolher(self):
        """Valida que a data de saída do espaço acolher não seja no futuro"""
        data = self.cleaned_data.get('data_saida_espaco_acolher')
        if data and data > date.today():
            raise ValidationError('A data de saída do espaço acolher não pode ser no futuro.')
        return data
    
    def clean_data_obito(self):
        """Valida que a data de óbito não seja no futuro"""
        data = self.cleaned_data.get('data_obito')
        if data and data > date.today():
            raise ValidationError('A data de óbito não pode ser no futuro.')
        return data
    
    def clean_data_encerramento(self):
        """Valida que a data de encerramento não seja no futuro"""
        data = self.cleaned_data.get('data_encerramento')
        if data and data > date.today():
            raise ValidationError('A data de encerramento não pode ser no futuro.')
        return data

# Formsets para relações Many-to-Many
EvolucaoTratamentoComplicacaoFormSet = inlineformset_factory(
    EvolucaoTratamento,
    EvolucaoTratamentoHasTipoComplicacao,
    fields=('tipo_complicacao_idtipo_complicacao',),
    extra=1,
    widgets={
        'tipo_complicacao_idtipo_complicacao': forms.Select(attrs={'class': 'form-select'})
    }
)

EvolucaoTratamentoProcedimentoFormSet = inlineformset_factory(
    EvolucaoTratamento,
    EvolucaoTratamentoHasTipoProcedimento,
    fields=('tipo_procedimento_idtipo_procedimento',),
    extra=1,
    widgets={
        'tipo_procedimento_idtipo_procedimento': forms.Select(attrs={'class': 'form-select'})
    }
)

# Form customizado para partes atingidas (para lidar com chave primária composta)
class OcorrenciaParteAtingidaForm(ModelForm):
    class Meta:
        model = OcorrenciaHasTipoParteAtingida
        fields = ('tipo_parte_atingida_idtipo_parte_atingida',)
        widgets = {
            'tipo_parte_atingida_idtipo_parte_atingida': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar o campo não obrigatório para permitir formulários vazios
        self.fields['tipo_parte_atingida_idtipo_parte_atingida'].required = False
        
        # Tornar o campo pk não obrigatório e oculto
        if 'pk' in self.fields:
            self.fields['pk'].required = False
            self.fields['pk'].widget = forms.HiddenInput()
    
    def full_clean(self):
        """Override para garantir validação correta sem erros de pk"""
        # Remover pk dos erros antes da validação
        if hasattr(self, '_errors') and self._errors is not None and 'pk' in self._errors:
            del self._errors['pk']
        
        super().full_clean()
        
        # Remover pk dos erros após a validação também
        if hasattr(self, '_errors') and self._errors is not None and 'pk' in self._errors:
            del self._errors['pk']
    
    def has_changed(self):
        """Override para considerar mudanças apenas quando há dados válidos"""
        # Se não há cleaned_data ainda, verificar os dados brutos
        if not hasattr(self, 'cleaned_data') or not self.cleaned_data:
            # Verificar se há algum tipo_parte_atingida nos dados brutos
            if hasattr(self, 'data') and self.data:
                field_name = f'{self.prefix}-tipo_parte_atingida_idtipo_parte_atingida'
                if field_name in self.data and self.data.get(field_name):
                    return True
            return False
        
        # Se há cleaned_data, verificar se há um tipo_parte_atingida selecionado
        if not self.cleaned_data.get('tipo_parte_atingida_idtipo_parte_atingida'):
            return False
        
        return True  # Sempre considerar que mudou se há um tipo_parte_atingida válido

# Formset para partes atingidas com tratamento de campos vazios
class OcorrenciaParteAtingidaFormSet(inlineformset_factory(
    Ocorrencia,
    OcorrenciaHasTipoParteAtingida,
    form=OcorrenciaParteAtingidaForm,
    extra=0,  # Não mostrar formulário vazio por padrão
    can_delete=True
)):
    def get_form_kwargs(self, index):
        """Override para limpar campos pk problemáticos antes de construir o formulário"""
        kwargs = super().get_form_kwargs(index)
        
        # Se há dados, verificar e limpar o campo pk se necessário
        if 'data' in kwargs and kwargs['data']:
            from django.http import QueryDict
            import json
            
            prefix = self.add_prefix(index)
            pk_key = f'{prefix}-pk'
            
            # Verificar se o campo pk existe nos dados
            if pk_key in kwargs['data']:
                pk_value = kwargs['data'].get(pk_key, '')
                should_remove = False
                
                # Verificar se está vazio ou inválido
                if not pk_value or (isinstance(pk_value, str) and pk_value.strip() == ''):
                    should_remove = True
                else:
                    # Tentar validar se é JSON válido
                    try:
                        if isinstance(pk_value, str):
                            json.loads(pk_value)
                    except (json.JSONDecodeError, ValueError):
                        should_remove = True
                
                # Se deve remover, criar cópia dos dados sem o pk
                if should_remove:
                    data = kwargs['data']
                    if isinstance(data, QueryDict):
                        if not data._mutable:
                            data = data.copy()
                    else:
                        data = dict(data) if not isinstance(data, dict) else data.copy()
                    
                    if isinstance(data, QueryDict):
                        data.pop(pk_key, None)
                    else:
                        data.pop(pk_key, None)
                    
                    kwargs['data'] = data
                    print(f"🧹 Removido pk inválido no get_form_kwargs: {pk_key}")
        
        return kwargs
    
    def add_fields(self, form, index):
        """Override para tornar o campo pk não obrigatório"""
        super().add_fields(form, index)
        # Tornar o campo pk não obrigatório e oculto
        if 'pk' in form.fields:
            form.fields['pk'].required = False
            form.fields['pk'].widget = forms.HiddenInput()
    
    def _construct_form(self, i, **kwargs):
        """Override para tratar erros de pk antes da construção do formulário"""
        # Verificar e limpar pk inválido antes de construir o formulário
        if 'data' in kwargs and kwargs['data']:
            from django.http import QueryDict
            import json
            
            prefix = self.add_prefix(i)
            pk_key = f'{prefix}-pk'
            
            if pk_key in kwargs['data']:
                pk_value = kwargs['data'].get(pk_key, '')
                should_remove = False
                
                # Verificar se está vazio ou inválido
                if not pk_value or (isinstance(pk_value, str) and pk_value.strip() == ''):
                    should_remove = True
                else:
                    # Tentar validar se é JSON válido
                    try:
                        if isinstance(pk_value, str):
                            json.loads(pk_value)
                    except (json.JSONDecodeError, ValueError):
                        should_remove = True
                
                if should_remove:
                    # Criar cópia dos dados sem o pk
                    data = kwargs['data']
                    if isinstance(data, QueryDict):
                        if not data._mutable:
                            data = data.copy()
                    else:
                        data = dict(data) if not isinstance(data, dict) else data.copy()
                    
                    # Remover o pk inválido
                    if isinstance(data, QueryDict):
                        data.pop(pk_key, None)
                    else:
                        data.pop(pk_key, None)
                    
                    kwargs['data'] = data
                    print(f"🧹 Removido pk inválido em _construct_form: {pk_key}")
        
        # Chamar o método original
        try:
            return super()._construct_form(i, **kwargs)
        except Exception as e:
            print(f"❌ Erro ao construir form {i}: {e}")
            # Se falhar, tentar novamente sem o campo pk
            if 'data' in kwargs:
                from django.http import QueryDict
                prefix = self.add_prefix(i)
                pk_key = f'{prefix}-pk'
                
                data = kwargs['data']
                if isinstance(data, QueryDict):
                    if not data._mutable:
                        data = data.copy()
                else:
                    data = dict(data) if not isinstance(data, dict) else data.copy()
                
                if isinstance(data, QueryDict):
                    data.pop(pk_key, None)
                else:
                    data.pop(pk_key, None)
                
                kwargs['data'] = data
                print(f"🔄 Tentando novamente sem pk: {pk_key}")
                return super()._construct_form(i, **kwargs)
            else:
                raise
    
    def __init__(self, data=None, *args, **kwargs):
        # Remover campos pk VAZIOS ou INVÁLIDOS dos dados ANTES de chamar super().__init__
        # Isso é necessário porque o CompositePrimaryKey causa problemas com valores vazios
        if data:
            from django.http import QueryDict
            import json
            
            # Criar uma cópia mutável dos dados
            if isinstance(data, QueryDict):
                if not data._mutable:
                    data = data.copy()
            else:
                data = dict(data) if not isinstance(data, dict) else data.copy()
            
            # Remover campos pk que estão vazios ou não são JSON válidos
            keys_to_remove = []
            for key in list(data.keys()):
                if key.endswith('-pk'):
                    value = data.get(key, '')
                    should_remove = False
                    
                    # Remover se estiver vazio
                    if not value or (isinstance(value, str) and value.strip() == ''):
                        should_remove = True
                    else:
                        # Tentar validar se é JSON válido
                        try:
                            if isinstance(value, str):
                                json.loads(value)
                        except (json.JSONDecodeError, ValueError):
                            # Se não for JSON válido, remover
                            should_remove = True
                    
                    if should_remove:
                        keys_to_remove.append(key)
            
            # Remover as chaves problemáticas
            for key in keys_to_remove:
                if isinstance(data, QueryDict):
                    data.pop(key, None)
                else:
                    data.pop(key, None)
                print(f"🧹 Removido campo pk vazio/inválido: {key}")
        
        super().__init__(data, *args, **kwargs)
    
    def clean(self):
        """Remover formulários vazios da validação"""
        if any(self.errors):
            return
        
        # Filtrar formulários vazios ou deletados
        cleaned_data = []
        for form in self.forms:
            if form.cleaned_data:
                # Se o formulário está marcado para deletar, ignorar
                if form.cleaned_data.get('DELETE'):
                    continue
                # Se não tem tipo_parte_atingida selecionado, ignorar (formulário vazio)
                if not form.cleaned_data.get('tipo_parte_atingida_idtipo_parte_atingida'):
                    continue
                cleaned_data.append(form.cleaned_data)
        
        return cleaned_data
    
    def is_valid(self):
        """Override para validação customizada e remover erros de pk"""
        # Validar normalmente
        result = super().is_valid()
        
        # Remover erros de pk de todos os formulários
        for form in self.forms:
            if hasattr(form, '_errors') and form._errors is not None and 'pk' in form._errors:
                del form._errors['pk']
                # Se não há mais erros, considerar o form válido
                if not form._errors:
                    form._errors = {}
        
        # Recalcular se o formset é válido após remover erros de pk
        has_errors = any(form.errors for form in self.forms)
        has_non_form_errors = bool(self.non_form_errors())
        
        return not has_errors and not has_non_form_errors
    
    def save(self, commit=True):
        """Override para salvar corretamente instâncias com chave primária composta"""
        print("🔄 Iniciando save do formset")
        print(f"📊 Total de formulários: {len(self.forms)}")
        
        if not commit:
            # Se commit=False, retornar apenas as instâncias novas/modificadas
            print("⚠️ Commit=False, retornando instâncias sem salvar")
            return super().save(commit=False)
        
        # Salvar com commit=True
        saved_instances = []
        
        # Processar cada formulário
        for i, form in enumerate(self.forms):
            print(f"\n📋 Processando form {i}")
            print(f"  🔍 Form é válido? {form.is_valid()}")
            print(f"  🔍 Form tem erros? {form.errors if hasattr(form, 'errors') else 'N/A'}")
            print(f"  🔍 Form has_changed? {form.has_changed()}")
            
            # Verificar se o formulário tem cleaned_data
            if not hasattr(form, 'cleaned_data'):
                print(f"  ⚠️ Form {i} não tem atributo cleaned_data")
                continue
                
            if not form.cleaned_data:
                print(f"  ⏭️ Form {i} sem cleaned_data (vazio), pulando")
                # Tentar entender por que está vazio
                if hasattr(form, 'data') and form.data:
                    print(f"  🔍 Form prefix: {form.prefix}")
                    # Buscar campos específicos deste formulário
                    tipo_key = f'{form.prefix}-tipo_parte_atingida_idtipo_parte_atingida'
                    print(f"  🔍 Valor do campo {tipo_key}: {form.data.get(tipo_key, 'NÃO ENCONTRADO')}")
                else:
                    print(f"  🔍 Form não tem data")
                continue
            
            print(f"  📊 cleaned_data do form {i}: {form.cleaned_data}")
                
            # Verificar se deve ser deletado
            if form.cleaned_data.get('DELETE'):
                print(f"  🗑️ Form {i} marcado para DELETE")
                if form.instance.pk:
                    print(f"  ❌ Deletando instância com pk: {form.instance.pk}")
                    form.instance.delete()
                continue
            
            # Verificar se há dados válidos
            tipo_parte = form.cleaned_data.get('tipo_parte_atingida_idtipo_parte_atingida')
            if not tipo_parte:
                print(f"  ⏭️ Form {i} sem tipo_parte_atingida, pulando")
                continue
            
            print(f"  ✅ Form {i} tem tipo_parte: {tipo_parte}")
            
            # Criar ou atualizar instância
            if form.instance.pk:
                print(f"  🔄 Atualizando instância existente: {form.instance.pk}")
                # Instância existente - atualizar
                form.instance.tipo_parte_atingida_idtipo_parte_atingida = tipo_parte
                form.instance.save()
                saved_instances.append(form.instance)
            else:
                print(f"  ➕ Criando nova instância")
                # Nova instância
                # Verificar se já existe essa combinação
                existing = self.instance.ocorrenciahastipoparteatingida_set.filter(
                    tipo_parte_atingida_idtipo_parte_atingida=tipo_parte
                ).first()
                
                if existing:
                    print(f"  ⚠️ Já existe uma instância com esse tipo_parte: {existing.pk}")
                    saved_instances.append(existing)
                else:
                    print(f"  💾 Criando novo registro no banco")
                    # Criar manualmente sem usar form.save() para evitar problemas com pk
                    new_instance = OcorrenciaHasTipoParteAtingida(
                        ocorrencia=self.instance,
                        tipo_parte_atingida_idtipo_parte_atingida=tipo_parte
                    )
                    new_instance.save()
                    print(f"  ✅ Registro criado: ocorrencia={self.instance.pk}, tipo_parte={tipo_parte.pk}")
                    saved_instances.append(new_instance)
        
        print(f"\n✅ Formset salvo. Total de instâncias salvas: {len(saved_instances)}")
        return saved_instances
    
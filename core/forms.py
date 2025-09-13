from django import forms
from django.forms import ModelForm, inlineformset_factory
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
            'data_notificacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_uf_notificacao': forms.Select(attrs={'class': 'form-select'}),
            'id_municipio_notificacao': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'estabelecimentos'}),
            'data_acidente': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_cadastro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            # Aba 2: Dados do Paciente
            'nome_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'idade': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'id_sexo': forms.Select(attrs={'class': 'form-select'}),
            'id_tempo_gestacao': forms.Select(attrs={'class': 'form-select'}),
            'id_raca': forms.Select(attrs={'class': 'form-select'}),
            'id_povo_tradicional': forms.Select(attrs={'class': 'form-select'}),
            'cartao_sus': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'id_cbo': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'cbo'}),
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
            'data_investigacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nome_dono': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_dono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'nome_condutor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_condutor': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'data_atendimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_cid': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'cid'}),
            'id_tipo_escalpelamento': forms.Select(attrs={'class': 'form-select'}),
            'id_causa_acidente': forms.Select(attrs={'class': 'form-select'}),
            'causa_acidente_outros': forms.TextInput(attrs={'class': 'form-control'}),
            'info_atendimento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'id_municipio_ocorrencia': forms.Select(attrs={'class': 'form-select'}),

            # Aba 5: Transferência
            'transferencia_hospitalar': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Selecione...'), ('S', 'Sim'), ('N', 'Não')]),
            'data_transferencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_uf_transferencia': forms.Select(attrs={'class': 'form-select'}),
            'id_municipio_transferencia': forms.Select(attrs={'class': 'form-select'}),
            'unidade_transferencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_tipo_transporte': forms.Select(attrs={'class': 'form-select'}),
            'data_cadastro_atendimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            # Aba 6: Investigador
            'id_municipio_investigador': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes_invertigador': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'estabelecimentos'}),
            'nome_invertigador': forms.TextInput(attrs={'class': 'form-control'}),
            'funcao_invertigador': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'cbo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        autocomplete_field_map = {
            'id_cnes': Estabelecimentos,
            'id_cbo': Cbo,
            'id_cid': Cid,
            'id_cnes_invertigador': Estabelecimentos,
            'funcao_invertigador': Cbo,
        }

        for field_name, model in autocomplete_field_map.items():
            if field_name in self.fields:
                if self.instance.pk and getattr(self.instance, field_name):
                    self.fields[field_name].queryset = model.objects.filter(pk=getattr(self.instance, field_name).pk)
                else:
                    self.fields[field_name].queryset = model.objects.none()

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


class EvolucaoTratamentoForm(ModelForm):
    """Formulário para Evolução do Tratamento"""
    
    class Meta:
        model = EvolucaoTratamento
        fields = '__all__'
        widgets = {
            'ocorrencia': forms.HiddenInput(),
            'id_unidade_atendimento': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'estabelecimentos'}),
            'data_entrada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'outros_procedimentos': forms.TextInput(attrs={'class': 'form-control'}),
            'outros_complicacoes': forms.TextInput(attrs={'class': 'form-control'}),
            'espaco_acolher': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Selecione...'), ('S', 'Sim'), ('N', 'Não')]),
            'data_entrada_espaco_acolher': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_saida_espaco_acolher': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_regime_atendimento': forms.Select(attrs={'class': 'form-select'}),
            'id_evolucao_caso': forms.Select(attrs={'class': 'form-select'}),
            'data_obito': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_encerramento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'evolucao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'id_municipio_investigacao': forms.Select(attrs={'class': 'form-select'}),
            'id_cnes_investigacao': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'estabelecimentos'}),
            'nome_investigador': forms.TextInput(attrs={'class': 'form-control'}),
            'id_funcao_investigador': forms.Select(attrs={'class': 'form-control', 'data-autocomplete': 'cbo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar campos obrigatórios
        self.fields['outros_complicacoes'].required = True
        self.fields['nome_investigador'].required = True

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

OcorrenciaParteAtingidaFormSet = inlineformset_factory(
    Ocorrencia,
    OcorrenciaHasTipoParteAtingida,
    fields=('tipo_parte_atingida_idtipo_parte_atingida',),
    extra=1,
    widgets={
        'tipo_parte_atingida_idtipo_parte_atingida': forms.Select(attrs={'class': 'form-select'})
    }
)
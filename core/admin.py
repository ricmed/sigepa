from django.contrib import admin
from .models import (
    Ocorrencia, EvolucaoTratamento, EvolucaoTratamentoHasTipoComplicacao,
    EvolucaoTratamentoHasTipoProcedimento, OcorrenciaHasTipoParteAtingida,
    TipoNotificacao, Estado, Municipios, Estabelecimentos, Sexo, TempoGestacao,
    Raca, PovoTradicional, Cbo, Escolaridade, Pais, Zona, Cid, TipoEscalpelamento,
    TipoCausaAcidente, TipoTransporte, TipoComplicacao, TipoProcedimento,
    TipoRegimeAtendimento, TipoEvolucaoCaso, TipoParteAtingida
)


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('num_registro', 'nome_paciente', 'data_notificacao', 'tipo_notificacao', 'id_uf_notificacao')
    list_filter = ('tipo_notificacao', 'id_uf_notificacao', 'id_sexo', 'id_tempo_gestacao', 'id_raca')
    search_fields = ('num_registro', 'nome_paciente', 'cartao_sus', 'cpf')
    readonly_fields = ('pk',)
    fieldsets = (
        ('Dados da Notificação', {
            'fields': ('tipo_notificacao', 'data_notificacao', 'id_uf_notificacao', 'id_municipio_notificacao', 'id_cnes')
        }),
        ('Dados do Paciente', {
            'fields': ('nome_paciente', 'data_nascimento', 'idade', 'id_sexo', 'id_tempo_gestacao', 'id_raca', 'id_povo_tradicional', 'outros_povo_tradicional')
        }),
        ('Documentos', {
            'fields': ('cartao_sus', 'cpf', 'id_cbo', 'nome_mae', 'id_escolaridade', 'id_pais')
        }),
        ('Endereço', {
            'fields': ('id_uf_residencia', 'id_municipio_residencia', 'distrito', 'bairro', 'logradouro', 'numero', 'complemento', 'cep', 'telefone', 'id_zona')
        }),
        ('Dados do Acidente', {
            'fields': ('num_registro', 'tipo_motor', 'data_investigacao', 'nome_dono', 'telefone_dono', 'nome_condutor', 'telefone_condutor', 'data_atendimento')
        }),
        ('Diagnóstico', {
            'fields': ('id_cid', 'id_tipo_escalpelamento', 'id_causa_acidente', 'causa_acidente_outros', 'info_atendimento', 'id_municipio_ocorrencia')
        }),
        ('Transferência', {
            'fields': ('transferencia_hospitalar', 'data_transferencia', 'id_uf_transferencia', 'id_municipio_transferencia', 'unidade_transferencia', 'id_tipo_transporte')
        }),
        ('Investigador', {
            'fields': ('id_municipio_investigador', 'id_cnes_invertigador', 'nome_invertigador', 'funcao_invertigador')
        }),
    )


@admin.register(EvolucaoTratamento)
class EvolucaoTratamentoAdmin(admin.ModelAdmin):
    list_display = ('ocorrencia', 'data_entrada', 'id_regime_atendimento', 'id_evolucao_caso')
    list_filter = ('id_regime_atendimento', 'id_evolucao_caso', 'espaco_acolher')
    search_fields = ('ocorrencia__nome_paciente', 'ocorrencia__num_registro', 'nome_investigador')


# Registros simples para modelos de referência
admin.site.register(TipoNotificacao)
admin.site.register(Estado)
admin.site.register(Municipios)
admin.site.register(Estabelecimentos)
admin.site.register(Sexo)
admin.site.register(TempoGestacao)
admin.site.register(Raca)
admin.site.register(PovoTradicional)
admin.site.register(Cbo)
admin.site.register(Escolaridade)
admin.site.register(Pais)
admin.site.register(Zona)
admin.site.register(Cid)
admin.site.register(TipoEscalpelamento)
admin.site.register(TipoCausaAcidente)
admin.site.register(TipoTransporte)
admin.site.register(TipoComplicacao)
admin.site.register(TipoProcedimento)
admin.site.register(TipoRegimeAtendimento)
admin.site.register(TipoEvolucaoCaso)
admin.site.register(TipoParteAtingida)
#admin.site.register(EvolucaoTratamentoHasTipoComplicacao)
#admin.site.register(EvolucaoTratamentoHasTipoProcedimento)
#admin.site.register(OcorrenciaHasTipoParteAtingida)

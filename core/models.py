# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cbo(models.Model):
    codigo = models.IntegerField(db_column='CODIGO', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='TITULO', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cbo'
    
    def __str__(self):
        return self.titulo


class Cid(models.Model):
    sk_causa = models.AutoField(primary_key=True)
    nk_causa = models.CharField(max_length=255, blank=True, null=True)
    num_cap = models.IntegerField(blank=True, null=True)
    num_cap_rom = models.CharField(max_length=255, blank=True, null=True)
    abrv_cap = models.CharField(max_length=255, blank=True, null=True)
    abrv_cap_rom = models.CharField(max_length=255, blank=True, null=True)
    cod_categoria = models.CharField(max_length=255, blank=True, null=True)
    cod_subcategoria = models.CharField(max_length=255, blank=True, null=True)
    desc_cap = models.CharField(max_length=255, blank=True, null=True)
    desc_abrv_cap = models.CharField(max_length=255, blank=True, null=True)
    desc_grupo = models.CharField(max_length=255, blank=True, null=True)
    desc_abrv_grupo = models.CharField(max_length=255, blank=True, null=True)
    desc_categoria = models.CharField(max_length=255, blank=True, null=True)
    desc_abrv_categoria = models.CharField(max_length=255, blank=True, null=True)
    desc_subcategoria = models.CharField(max_length=255, blank=True, null=True)
    desc_abrv_subcategoria = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cid'
    
    def __str__(self):
        return f"{self.sk_causa} - {self.desc_subcategoria}"

class Escolaridade(models.Model):
    id_escolaridade = models.AutoField(primary_key=True)
    descricao = models.CharField(unique=True, max_length=70)
    ordem = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'escolaridade'
    
    def __str__(self):
        return self.descricao


class Estabelecimentos(models.Model):
    co_unidade = models.BigIntegerField(db_column='CO_UNIDADE', primary_key=True)  # Field name made lowercase.
    no_fantasia = models.CharField(db_column='NO_FANTASIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    co_municipio_gestor = models.CharField(db_column='CO_MUNICIPIO_GESTOR', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nu_cnpj = models.CharField(db_column='NU_CNPJ', max_length=25, blank=True, null=True)  # Field name made lowercase.
    co_cnes = models.CharField(db_column='CO_CNES', max_length=25, blank=True, null=True)  # Field name made lowercase.
    dt_atualizacao = models.CharField(db_column='DT_ATUALIZACAO', max_length=25, blank=True, null=True)  # Field name made lowercase.
    tp_unidade = models.IntegerField(db_column='TP_UNIDADE', blank=True, null=True)  # Field name made lowercase.
    nu_cpf = models.CharField(db_column='NU_CPF', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estabelecimentos'
    
    def __str__(self):
        return self.no_fantasia

class Estado(models.Model):
    idestado = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'
    
    def __str__(self):
        return self.descricao


class EvolucaoTratamento(models.Model):
    id = models.AutoField(primary_key=True)
    ocorrencia = models.ForeignKey('Ocorrencia', models.DO_NOTHING)
    id_unidade_atendimento = models.ForeignKey(Estabelecimentos, models.DO_NOTHING, db_column='id_unidade_atendimento', blank=True, null=True)
    data_entrada = models.DateField(blank=True, null=True)
    outros_procedimentos = models.CharField(max_length=100, blank=True, null=True)
    outros_complicacoes = models.CharField(max_length=100)
    espaco_acolher = models.CharField(max_length=1, blank=True, null=True)
    data_entrada_espaco_acolher = models.DateField(blank=True, null=True)
    data_saida_espaco_acolher = models.DateField(blank=True, null=True)
    id_regime_atendimento = models.ForeignKey('TipoRegimeAtendimento', models.DO_NOTHING, db_column='id_regime_atendimento', blank=True, null=True)
    id_evolucao_caso = models.ForeignKey('TipoEvolucaoCaso', models.DO_NOTHING, db_column='id_evolucao_caso', blank=True, null=True)
    data_obito = models.DateField(blank=True, null=True)
    data_encerramento = models.DateField(blank=True, null=True)
    evolucao = models.TextField(blank=True, null=True)
    id_municipio_investigacao = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='id_municipio_investigacao', blank=True, null=True)
    id_cnes_investigacao = models.ForeignKey(Estabelecimentos, models.DO_NOTHING, db_column='id_cnes_investigacao', related_name='evolucaotratamento_id_cnes_investigacao_set', blank=True, null=True)
    nome_investigador = models.CharField(max_length=150)
    id_funcao_investigador = models.ForeignKey(Cbo, models.DO_NOTHING, db_column='id_funcao_investigador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evolucao_tratamento'
    
    def __str__(self):
        return f"Evolução {self.pk} - {self.ocorrencia.nome_paciente if self.ocorrencia else 'N/A'}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:ocorrencia_detail', kwargs={'pk': self.ocorrencia.pk})


class EvolucaoTratamentoHasTipoComplicacao(models.Model):
    pk = models.CompositePrimaryKey('evolucao_tratamento_id', 'tipo_complicacao_idtipo_complicacao')
    evolucao_tratamento = models.ForeignKey(EvolucaoTratamento, models.DO_NOTHING)
    tipo_complicacao_idtipo_complicacao = models.ForeignKey('TipoComplicacao', models.DO_NOTHING, db_column='tipo_complicacao_idtipo_complicacao')

    class Meta:
        managed = False
        db_table = 'evolucao_tratamento_has_tipo_complicacao'


class EvolucaoTratamentoHasTipoProcedimento(models.Model):
    pk = models.CompositePrimaryKey('evolucao_tratamento_id', 'tipo_procedimento_idtipo_procedimento')
    evolucao_tratamento = models.ForeignKey(EvolucaoTratamento, models.DO_NOTHING)
    tipo_procedimento_idtipo_procedimento = models.ForeignKey('TipoProcedimento', models.DO_NOTHING, db_column='tipo_procedimento_idtipo_procedimento')

    class Meta:
        managed = False
        db_table = 'evolucao_tratamento_has_tipo_procedimento'


class Municipios(models.Model):
    id_municipio = models.IntegerField(primary_key=True)
    id_uf = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_uf', blank=True, null=True)
    nome_uf = models.CharField(max_length=255, blank=True, null=True)
    nome_municipio = models.CharField(max_length=255, blank=True, null=True)
    regiao_geografica_intermediaria = models.CharField(max_length=255, blank=True, null=True)
    nome_regiao_geografica_intermediaria = models.CharField(max_length=255, blank=True, null=True)
    regiao_geografica_imediata = models.CharField(max_length=255, blank=True, null=True)
    nome_regiao_geografica_imediata = models.CharField(max_length=255, blank=True, null=True)
    mesorregiao_geografica = models.CharField(max_length=255, blank=True, null=True)
    nome_mesorregiao = models.CharField(max_length=255, blank=True, null=True)
    microrregiao_geografica = models.CharField(max_length=255, blank=True, null=True)
    nome_microrregiao = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipios'
    
    def __str__(self):
        return self.nome_municipio


class Ocorrencia(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_notificacao = models.ForeignKey('TipoNotificacao', models.DO_NOTHING, db_column='tipo_notificacao')
    data_notificacao = models.DateField()
    id_uf_notificacao = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_uf_notificacao')
    id_municipio_notificacao = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='id_municipio_notificacao')
    id_cnes = models.ForeignKey(Estabelecimentos, models.DO_NOTHING, db_column='id_cnes')
    data_acidente = models.DateField(blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)
    nome_paciente = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    idade = models.CharField(max_length=3, blank=True, null=True)
    id_sexo = models.ForeignKey('Sexo', models.DO_NOTHING, db_column='id_sexo')
    id_tempo_gestacao = models.ForeignKey('TempoGestacao', models.DO_NOTHING, db_column='id_tempo_gestacao')
    id_raca = models.ForeignKey('Raca', models.DO_NOTHING, db_column='id_raca')
    id_povo_tradicional = models.ForeignKey('PovoTradicional', models.DO_NOTHING, db_column='id_povo_tradicional', blank=True, null=True)
    outros_povo_tradicional = models.CharField(max_length=45, blank=True, null=True)
    cartao_sus = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    id_cbo = models.ForeignKey(Cbo, models.DO_NOTHING, db_column='id_cbo', blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    id_escolaridade = models.ForeignKey(Escolaridade, models.DO_NOTHING, db_column='id_escolaridade', blank=True, null=True)
    id_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='id_pais', blank=True, null=True)
    id_uf_residencia = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_uf_residencia', related_name='ocorrencia_id_uf_residencia_set', blank=True, null=True)
    id_municipio_residencia = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='id_municipio_residencia', related_name='ocorrencia_id_municipio_residencia_set', blank=True, null=True)
    distrito = models.CharField(max_length=60, blank=True, null=True)
    bairro = models.CharField(max_length=60, blank=True, null=True)
    logradouro = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=5, blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    geo_campo1 = models.CharField(max_length=45, blank=True, null=True)
    geo_campo2 = models.CharField(max_length=45, blank=True, null=True)
    ponto_referencia = models.CharField(max_length=45, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    id_zona = models.ForeignKey('Zona', models.DO_NOTHING, db_column='id_zona', blank=True, null=True)
    num_registro = models.CharField(max_length=45)
    tipo_motor = models.CharField(max_length=45, blank=True, null=True)
    data_investigacao = models.DateField(blank=True, null=True)
    nome_dono = models.CharField(max_length=100, blank=True, null=True)
    telefone_dono = models.CharField(max_length=15, blank=True, null=True)
    nome_condutor = models.CharField(max_length=100, blank=True, null=True)
    telefone_condutor = models.CharField(max_length=15, blank=True, null=True)
    data_atendimento = models.DateField(blank=True, null=True)
    id_cid = models.ForeignKey(Cid, models.DO_NOTHING, db_column='id_cid', blank=True, null=True)
    id_tipo_escalpelamento = models.ForeignKey('TipoEscalpelamento', models.DO_NOTHING, db_column='id_tipo_escalpelamento', blank=True, null=True)
    id_causa_acidente = models.ForeignKey('TipoCausaAcidente', models.DO_NOTHING, db_column='id_causa_acidente', blank=True, null=True)
    causa_acidente_outros = models.CharField(max_length=45, blank=True, null=True)
    info_atendimento = models.TextField(blank=True, null=True)
    id_municipio_ocorrencia = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='id_municipio_ocorrencia', related_name='ocorrencia_id_municipio_ocorrencia_set', blank=True, null=True)
    transferencia_hospitalar = models.CharField(max_length=1, blank=True, null=True)
    data_transferencia = models.DateField(blank=True, null=True)
    id_uf_transferencia = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_uf_transferencia', related_name='ocorrencia_id_uf_transferencia_set', blank=True, null=True)
    id_municipio_transferencia = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='id_municipio_transferencia', related_name='ocorrencia_id_municipio_transferencia_set', blank=True, null=True)
    unidade_transferencia = models.CharField(max_length=80, blank=True, null=True)
    id_tipo_transporte = models.ForeignKey('TipoTransporte', models.DO_NOTHING, db_column='id_tipo_transporte', blank=True, null=True)
    data_cadastro_atendimento = models.DateField(blank=True, null=True)
    id_municipio_investigador = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='id_municipio_investigador', related_name='ocorrencia_id_municipio_investigador_set', blank=True, null=True)
    id_cnes_invertigador = models.ForeignKey(Estabelecimentos, models.DO_NOTHING, db_column='id_cnes_invertigador', related_name='ocorrencia_id_cnes_invertigador_set', blank=True, null=True)
    nome_invertigador = models.CharField(max_length=150)
    funcao_invertigador = models.ForeignKey(Cbo, models.DO_NOTHING, db_column='funcao_invertigador', blank=True, null=True, related_name='ocorrencia_funcao_invertigador_set')

    class Meta:
        managed = False
        db_table = 'ocorrencia'
    
    def __str__(self):
        return f"Ocorrência {self.pk} - {self.nome_paciente}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:ocorrencia_detail', kwargs={'pk': self.pk})


class OcorrenciaHasTipoParteAtingida(models.Model):
    pk = models.CompositePrimaryKey('ocorrencia_id', 'tipo_parte_atingida_idtipo_parte_atingida')
    ocorrencia = models.ForeignKey(Ocorrencia, models.DO_NOTHING)
    tipo_parte_atingida_idtipo_parte_atingida = models.ForeignKey('TipoParteAtingida', models.DO_NOTHING, db_column='tipo_parte_atingida_idtipo_parte_atingida')

    class Meta:
        managed = False
        db_table = 'ocorrencia_has_tipo_parte_atingida'


class Pais(models.Model):
    idpais = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'pais'
    
    def __str__(self):
        return self.descricao


class PovoTradicional(models.Model):
    id_povo_tradicional = models.AutoField(primary_key=True)
    descricao = models.CharField(unique=True, max_length=45)
    ordem = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'povo_tradicional'
    
    def __str__(self):
        return self.descricao

class Raca(models.Model):
    id_raca = models.AutoField(primary_key=True)
    descricao = models.CharField(unique=True, max_length=45)
    ordem = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'raca'
    
    def __str__(self):
        return self.descricao

class Sexo(models.Model):
    idsexo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sexo'
    
    def __str__(self):
        return self.descricao


class TempoGestacao(models.Model):
    id_gestante = models.AutoField(primary_key=True)
    descricao = models.CharField(unique=True, max_length=45)
    ordem = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'tempo_gestacao'
    
    def __str__(self):
        return self.descricao

class TipoCausaAcidente(models.Model):
    idtipo_causa_acidente = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'tipo_causa_acidente'
    
    def __str__(self):
        return self.descricao

class TipoComplicacao(models.Model):
    idtipo_complicacao = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_complicacao'
    
    def __str__(self):
        return self.descricao


class TipoEscalpelamento(models.Model):
    idtipo_escalpelamento = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'tipo_escalpelamento'
    
    def __str__(self):
        return self.descricao

class TipoEvolucaoCaso(models.Model):
    idtipo_evolucao_caso = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_evolucao_caso'
    
    def __str__(self):
        return self.descricao

class TipoNotificacao(models.Model):
    idtipo_notificacao = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_notificacao'
    
    def __str__(self):
        return self.descricao


class TipoParteAtingida(models.Model):
    idtipo_parte_atingida = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'tipo_parte_atingida'
    
    def __str__(self):
        return self.descricao

class TipoProcedimento(models.Model):
    idtipo_procedimento = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_procedimento'
    
    def __str__(self):
        return self.descricao

class TipoRegimeAtendimento(models.Model):
    idtipo_regime_atendimento = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_regime_atendimento'
    
    def __str__(self):
        return self.descricao

class TipoTransporte(models.Model):
    idtipo_transporte = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_transporte'
    
    def __str__(self):
        return self.descricao


class Zona(models.Model):
    idzona = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'zona'
    
    def __str__(self):
        return self.descricao
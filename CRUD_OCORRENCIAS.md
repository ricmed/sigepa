# CRUD de Ocorrências - SIGEPA

Este documento descreve o sistema CRUD (Create, Read, Update, Delete) implementado para o modelo `Ocorrencia` no sistema SIGEPA.

## Funcionalidades Implementadas

### 1. Listagem de Ocorrências (`OcorrenciaListView`)
- **URL**: `/core/ocorrencias/`
- **Funcionalidades**:
  - Lista paginada de ocorrências (20 por página)
  - Sistema de busca por nome do paciente, número de registro, cartão SUS ou CPF
  - Filtros por tipo de notificação, UF e município
  - Links para visualizar, editar e excluir cada ocorrência

### 2. Criação de Ocorrência (`OcorrenciaCreateView`)
- **URL**: `/core/ocorrencias/nova/`
- **Funcionalidades**:
  - Formulário organizado em 6 abas
  - Validação de campos obrigatórios
  - Campos de autocomplete para CBO, CID e Estabelecimentos
  - Carregamento dinâmico de municípios por estado

### 3. Visualização de Ocorrência (`OcorrenciaDetailView`)
- **URL**: `/core/ocorrencias/<id>/`
- **Funcionalidades**:
  - Exibição completa dos dados em abas organizadas
  - Visualização das evoluções do tratamento relacionadas
  - Links para editar e voltar à lista

### 4. Edição de Ocorrência (`OcorrenciaUpdateView`)
- **URL**: `/core/ocorrencias/<id>/editar/`
- **Funcionalidades**:
  - Mesmo formulário da criação, mas pré-preenchido
  - Validação e atualização dos dados
  - Suporte a formsets para relações Many-to-Many

### 5. Exclusão de Ocorrência (`OcorrenciaDeleteView`)
- **URL**: `/core/ocorrencias/<id>/excluir/`
- **Funcionalidades**:
  - Confirmação antes da exclusão
  - Exibição dos dados que serão removidos
  - Redirecionamento após exclusão

## Estrutura do Formulário

O formulário está organizado em 6 abas para melhor usabilidade:

### Aba 1: Dados da Notificação
- Tipo de notificação (obrigatório)
- Data da notificação (obrigatório)
- UF da notificação (obrigatório)
- Município da notificação (obrigatório)
- CNES (obrigatório, com autocomplete)
- Data do acidente
- Data do cadastro

### Aba 2: Dados do Paciente
- Nome do paciente (obrigatório)
- Data de nascimento
- Idade
- Sexo (obrigatório)
- Tempo de gestação (obrigatório)
- Raça (obrigatório)
- Povo tradicional
- Cartão SUS
- CPF
- CBO (com autocomplete)
- Nome da mãe
- Escolaridade
- País

### Aba 3: Endereço
- UF de residência
- Município de residência
- Zona
- Distrito
- Bairro
- Logradouro
- Número
- Complemento
- CEP
- Telefone
- Coordenadas geográficas
- Ponto de referência

### Aba 4: Dados do Acidente
- Número do registro (obrigatório)
- Tipo do motor
- Data da investigação
- Data do atendimento
- Nome do dono
- Telefone do dono
- Nome do condutor
- Telefone do condutor
- CID (com autocomplete)
- Tipo de escalpelamento
- Causa do acidente
- Outras causas
- Município da ocorrência
- Data do cadastro do atendimento
- Informações do atendimento

### Aba 5: Transferência
- Transferência hospitalar
- Data da transferência
- UF da transferência
- Município da transferência
- Tipo de transporte
- Unidade de transferência

### Aba 6: Investigador
- Município do investigador
- CNES do investigador (com autocomplete)
- Nome do investigador (obrigatório)
- Função do investigador

## APIs de Autocomplete

### CBO (`/core/api/cbo/`)
- Busca por código ou título do CBO
- Retorna até 10 resultados
- Formato: `{codigo} - {titulo}`

### CID (`/core/api/cid/`)
- Busca por código ou descrição do CID
- Retorna até 10 resultados
- Formato: `{codigo} - {descricao}`

### Estabelecimentos (`/core/api/estabelecimentos/`)
- Busca por CNES, nome fantasia ou CNPJ
- Retorna até 10 resultados
- Formato: `{cnes} - {nome_fantasia}`

### Municípios (`/core/api/municipios/`)
- Carrega municípios por estado
- Parâmetro: `estado_id`
- Retorna lista de municípios ordenados por nome

## Tecnologias Utilizadas

- **Frontend**: Bootstrap 5, HTMX, Alpine.js, Select2, Font Awesome
- **Backend**: Django 5.2.6, Python
- **Banco de Dados**: MySQL
- **ORM**: Django ORM com otimizações (select_related, prefetch_related)

## Características Técnicas

### Otimizações de Performance
- Uso de `select_related` para relações ForeignKey
- Uso de `prefetch_related` para relações Many-to-Many
- Paginação para listas grandes
- Cache de consultas AJAX

### Segurança
- Validação CSRF em todos os formulários
- Validação de dados no frontend e backend
- Autenticação obrigatória para todas as views
- Sanitização de dados de entrada

### Usabilidade
- Interface responsiva com Bootstrap
- Campos de autocomplete para melhor UX
- Formulário em abas para organização
- Mensagens de feedback para o usuário
- Validação em tempo real

## Próximos Passos

1. Implementar CRUD para Evolução do Tratamento
2. Adicionar relatórios e dashboards
3. Implementar exportação de dados
4. Adicionar testes automatizados
5. Implementar auditoria de alterações

// Script para formulário de ocorrência
console.log('🚀 Carregando script de pesquisa...');

// Variáveis globais para controle de paginação
let currentTargetField = null;
let currentPage = 1;
let currentSearch = '';
let currentType = '';

// Configurar CSRF token para AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Configurar AJAX padrão
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Função para abrir modal de pesquisa
function openSearchModal(type, targetField) {
    console.log('📂 Abrindo modal de pesquisa:', type, 'para campo:', targetField);
    currentTargetField = targetField;
    currentType = type;
    currentPage = 1;
    currentSearch = '';
    
    // Limpar campo de pesquisa
    $('#search' + capitalizeFirst(type)).val('');
    
    // Abrir modal apropriado
    $('#modal' + capitalizeFirst(type)).modal('show');
    
    // Carregar primeira página sem filtro (mostrar todos os primeiros itens)
    loadSearchResults(type, 1, '');
    
    // Focar no campo de pesquisa após abrir o modal
    setTimeout(function() {
        $('#search' + capitalizeFirst(type)).focus();
    }, 500);
}

console.log('✅ Função openSearchModal definida');

// Função para executar pesquisa via botão
function executeSearchFromButton(type) {
    const searchField = $('#search' + capitalizeFirst(type));
    const searchTerm = searchField.val();
    console.log('🔍 Pesquisa via botão:', type, 'termo:', searchTerm);
    
    currentSearch = searchTerm;
    currentPage = 1;
    loadSearchResults(type, 1, searchTerm);
}

// Função para limpar pesquisa
function clearSearch(type) {
    console.log('🧹 Limpando pesquisa:', type);
    const searchField = $('#search' + capitalizeFirst(type));
    searchField.val('');
    
    currentSearch = '';
    currentPage = 1;
    loadSearchResults(type, 1, '');
    
    // Focar novamente no campo
    searchField.focus();
}
    
// Função para capitalizar primeira letra
function capitalizeFirst(str) {
    if (str === 'estabelecimentos') return 'Estabelecimentos';
    if (str === 'cbo') return 'Cbo';
    if (str === 'cid') return 'Cid';
    return str;
}
    
// Função para carregar resultados de pesquisa
function loadSearchResults(type, page, search) {
    console.log('🔍 Carregando resultados:', type, 'página:', page, 'busca:', search);
    const loading = $('#loading' + capitalizeFirst(type));
    const results = $('#results' + capitalizeFirst(type));
    const pagination = $('#pagination' + capitalizeFirst(type));
    
    // Mostrar loading
    loading.removeClass('d-none');
    results.empty();
    pagination.empty();
    
    // Fazer requisição
    $.ajax({
        url: '/core/api/' + type + '/',
        data: {
            q: search || '',
            page: page || 1
        },
        success: function(data) {
            console.log('✅ Dados recebidos:', data);
            loading.addClass('d-none');
            renderResults(type, data.results || []);
            renderPagination(type, data.pagination || {});
        },
        error: function(xhr, status, error) {
            console.error('❌ Erro na busca:', error, xhr.responseText);
            loading.addClass('d-none');
            results.html('<div class="alert alert-danger">Erro ao carregar dados: ' + error + '</div>');
        }
    });
}
    
// Função para renderizar resultados
function renderResults(type, results) {
    const container = $('#results' + capitalizeFirst(type));
    
    if (results.length === 0) {
        container.html('<div class="alert alert-info">Nenhum resultado encontrado.</div>');
        return;
    }
    
    let html = '<div class="list-group">';
    results.forEach(function(item) {
        html += `
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <span>${item.text}</span>
                <button type="button" class="btn btn-primary btn-sm" onclick="selectItem('${item.id}', '${item.text.replace(/\'/g, "\\'")}')">
                    Selecionar
                </button>
            </div>
        `;
    });
    html += '</div>';
    
    container.html(html);
}
    
// Função para renderizar paginação
function renderPagination(type, pagination) {
    const container = $('#pagination' + capitalizeFirst(type));
    
    if (!pagination.total_pages || pagination.total_pages <= 1) {
        return;
    }
    
    let html = '';
    
    // Botão anterior
    if (pagination.current_page > 1) {
        html += `<li class="page-item">
            <a class="page-link" href="#" onclick="changePage(${pagination.current_page - 1})">Anterior</a>
        </li>`;
    }
    
    // Páginas
    for (let i = 1; i <= pagination.total_pages; i++) {
        if (i === pagination.current_page) {
            html += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else if (i === 1 || i === pagination.total_pages || Math.abs(i - pagination.current_page) <= 2) {
            html += `<li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
            </li>`;
        } else if (i === pagination.current_page - 3 || i === pagination.current_page + 3) {
            html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
    }
    
    // Botão próximo
    if (pagination.current_page < pagination.total_pages) {
        html += `<li class="page-item">
            <a class="page-link" href="#" onclick="changePage(${pagination.current_page + 1})">Próximo</a>
        </li>`;
    }
    
    container.html(html);
}
    
// Função para mudar página
function changePage(page) {
    currentPage = page;
    loadSearchResults(currentType, page, currentSearch);
}

// Função para selecionar item
function selectItem(id, text) {
    // Adicionar opção ao select se não existir
    const $select = $(currentTargetField);
    if ($select.find(`option[value="${id}"]`).length === 0) {
        $select.append(`<option value="${id}">${text}</option>`);
    }
    
    // Selecionar a opção
    $select.val(id);
    
    // Fechar modal
    $('.modal').modal('hide');
    
    console.log('Item selecionado:', id, text);
}

// Função debounce para otimizar pesquisa
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para carregar municípios (com ou sem filtro de UF)
function loadMunicipiosComFiltro(target, ufId = null, nomeContexto = '') {
    console.log(`🔄 Carregando municípios para: ${target}${ufId ? ` (UF: ${ufId})` : ' (todos)'}${nomeContexto ? ` - ${nomeContexto}` : ''}`);
    
    if (!target) {
        console.log('⚠️ Target não fornecido');
        return;
    }
    
    var municipioSelect = $(target);
    if (municipioSelect.length === 0) {
        console.error('❌ Elemento target não encontrado:', target);
        return;
    }
    
    // Preservar valor atual em modo de edição
    const currentValue = municipioSelect.val();
    const isEdit = isEditMode();
    
    // Mostrar indicador de carregamento
    municipioSelect.prop('disabled', true);
    municipioSelect.html('<option value="">Carregando...</option>');
    
    const url = '/core/api/municipios/';
    const data = ufId ? { 'estado_id': ufId } : {};
    
    console.log(`📡 Fazendo requisição AJAX para ${ufId ? `municípios da UF ${ufId}` : 'todos os municípios'}...`);
    
    $.ajax({
        url: url,
        method: 'GET',
        data: data,
        dataType: 'json',
        timeout: 15000,
        success: function(data) {
            console.log(`✅ Resposta da API (${nomeContexto || 'municípios'}):`, data);
            
            try {
                // Limpar select atual
                municipioSelect.empty();
                municipioSelect.append('<option value="">Selecione...</option>');
                
                // Verificar se a resposta é válida
                if (data && data.success !== false) {
                    // Adicionar municípios
                    if (data.municipios && Array.isArray(data.municipios) && data.municipios.length > 0) {
                        $.each(data.municipios, function(index, municipio) {
                            if (municipio && municipio.id && municipio.nome) {
                                municipioSelect.append('<option value="' + municipio.id + '">' + municipio.nome + '</option>');
                            }
                        });
                        console.log(`📋 ${nomeContexto ? nomeContexto + ' - ' : ''}Municípios carregados: ${data.municipios.length}`);
                    } else {
                        municipioSelect.append('<option value="">Nenhum município encontrado</option>');
                        console.log(`⚠️ Nenhum município encontrado${ufId ? ` para UF ${ufId}` : ''}`);
                    }
                } else {
                    municipioSelect.append('<option value="">Erro na resposta do servidor</option>');
                    console.log('❌ Resposta inválida da API:', data);
                }
            } catch (e) {
                console.error('❌ Erro ao processar dados dos municípios:', e);
                municipioSelect.empty();
                municipioSelect.append('<option value="">Erro ao processar dados</option>');
            }
            
            // Restaurar valor selecionado em modo de edição
            if (isEdit && currentValue) {
                municipioSelect.val(currentValue);
                console.log(`🔄 Valor restaurado para ${target}: ${currentValue}`);
            }
            
            // Reabilitar o select
            municipioSelect.prop('disabled', false);
        },
        error: function(xhr, status, error) {
            console.error(`❌ Erro na requisição AJAX (${nomeContexto || 'municípios'}):`, {
                error: error,
                status: status,
                responseText: xhr.responseText,
                url: url,
                ufId: ufId
            });
            
            municipioSelect.empty();
            
            let errorMessage = 'Erro ao carregar municípios';
            if (status === 'timeout') {
                errorMessage = 'Timeout - tente novamente';
            } else if (status === 'abort') {
                errorMessage = 'Requisição cancelada';
            } else if (xhr.status === 404) {
                errorMessage = 'API não encontrada';
            } else if (xhr.status === 500) {
                errorMessage = 'Erro do servidor';
            }
            
            municipioSelect.append('<option value="">' + errorMessage + '</option>');
            municipioSelect.prop('disabled', false);
        }
    });
}

// Função para carregar todos os municípios (para campos sem UF) - mantida para compatibilidade
function loadAllMunicipios(target, nomeContexto = '') {
    return loadMunicipiosComFiltro(target, null, nomeContexto);
}

// Função para inicializar campos de município específicos (ocorrência/investigador) com municípios do Pará
function initializeMunicipiosEspecificos() {
    console.log('🔄 Inicializando municípios específicos...');
    
    const camposEspecificos = [
        { selector: '#id_municipio_ocorrencia', nome: 'Ocorrência' },
        { selector: '#id_municipio_investigador', nome: 'Investigador' }
    ];
    
    camposEspecificos.forEach(function(campo) {
        const $elemento = $(campo.selector);
        if ($elemento.length > 0) {
            // Se não estiver em modo de edição, carregar municípios do Pará
            if (!isEditMode()) {
                console.log(`📍 Carregando municípios do Pará para ${campo.nome}`);
                loadMunicipiosComFiltro(campo.selector, 15, `Municípios do Pará - ${campo.nome}`);
            }
        }
    });
}

// Função para carregar municípios dinamicamente (compatibilidade)
function loadMunicipios(ufId, target) {
    const nomeContexto = `Municípios por UF (${ufId})`;
    return loadMunicipiosComFiltro(target, ufId, nomeContexto);
}

// Função para inicializar o formulário de forma segura
function initializeFormulario(elementosDisponiveis = {}) {
    console.log('🔄 Inicializando formulário com modais de pesquisa...');
    
    // Primeiro, vamos ver todos os elementos de formulário disponíveis
    console.log('🔍 Elementos de formulário disponíveis:');
    $('form input, form select').each(function() {
        if (this.id) {
            console.log('   - ID encontrado:', this.id);
        }
    });
    
    console.log('🔍 Elementos disponíveis passados para inicialização:', elementosDisponiveis);

    // Configurar gatilhos para mudança de UF usando elementos encontrados dinamicamente
    const ufMunicipioMap = [
        { 
            uf: elementosDisponiveis['uf_notificacao'], 
            municipio: elementosDisponiveis['municipio_notificacao'], 
            nome: 'Notificação',
            carregarInicial: false  // Não carregar inicialmente em novos registros
        },
        { 
            uf: elementosDisponiveis['uf_residencia'], 
            municipio: elementosDisponiveis['municipio_residencia'], 
            nome: 'Residência',
            carregarInicial: false  // Não carregar inicialmente em novos registros
        },
        { 
            uf: elementosDisponiveis['uf_transferencia'], 
            municipio: elementosDisponiveis['municipio_transferencia'], 
            nome: 'Transferência',
            carregarInicial: false  // Não carregar inicialmente em novos registros
        }
    ];
    
    ufMunicipioMap.forEach(function(map) {
        if (!map.uf || !map.municipio) {
            console.warn(`⚠️ Elementos não encontrados para ${map.nome}`);
            return;
        }
        
        const $uf = $(map.uf);
        const $municipio = $(map.municipio);
        
        if ($uf.length && $municipio.length) {
            console.log(`✅ Configurando gatilho para UF ${map.nome} (${map.uf} -> ${map.municipio})`);
            
            $uf.on('change', function() {
                var ufId = $(this).val();
                console.log(`🔄 UF ${map.nome} mudou para:`, ufId);
                
                // Em modo de edição, preservar o valor atual do município se não mudou a UF
                const currentMunicipioValue = $municipio.val();
                const isEdit = isEditMode();
                
                // Limpar município atual apenas se não estivermos em modo de edição
                // ou se a UF realmente mudou
                if (!isEdit || !currentMunicipioValue) {
                    $municipio.val('');
                }
                
                if (ufId) {
                    loadMunicipios(ufId, map.municipio);
                } else {
                    $municipio.empty().append('<option value="">Selecione...</option>');
                }
            });
            
            // Carregar municípios iniciais apenas se já houver UF selecionada E estivermos em modo de edição
            if ($uf.val() && isEditMode()) {
                console.log(`📍 Carregando municípios iniciais para ${map.nome} (modo edição)`);
                loadMunicipios($uf.val(), map.municipio);
            } else if ($uf.val()) {
                console.log(`📍 UF ${map.nome} já selecionada, mas não carregando municípios (modo criação)`);
            }
        } else {
            console.warn(`⚠️ Elementos DOM não encontrados para ${map.nome}: UF=${$uf.length}, Município=${$municipio.length}`);
        }
    });
    
    // Carregar municípios filtrados por UF=15 para campos específicos (apenas em modo de edição)
    console.log('🔍 Verificando campos específicos de município...');
    
    const municipiosEspecificos = [
        { 
            selector: elementosDisponiveis['municipio_ocorrencia'], 
            nome: 'Ocorrência',
            ufId: 15,
            descricao: 'Municípios da Ocorrência (UF=15)'
        },
        { 
            selector: elementosDisponiveis['municipio_investigador'], 
            nome: 'Investigador',
            ufId: 15,
            descricao: 'Municípios do Investigador (UF=15)'
        }
    ];
    
    municipiosEspecificos.forEach(function(campo) {
        if (!campo.selector) {
            console.warn(`⚠️ Campo ${campo.nome} não foi encontrado nos elementos disponíveis`);
            return;
        }
        
        const $elemento = $(campo.selector);
        if ($elemento.length > 0) {
            // Carregar municípios do Pará apenas em modo de edição
            if (isEditMode()) {
                console.log(`📍 Carregando municípios para ${campo.nome} (${campo.selector}) - UF=${campo.ufId} (modo edição)`);
                loadMunicipiosComFiltro(campo.selector, campo.ufId, campo.descricao);
            } else {
                console.log(`📍 Campo ${campo.nome} iniciará vazio (modo criação)`);
                // Garantir que o campo inicie com mensagem apropriada
                $elemento.empty().append('<option value="">Selecione...</option>');
            }
        } else {
            console.warn(`⚠️ Campo ${campo.nome} (${campo.selector}) não encontrado no DOM`);
        }
    });
}

// Função para encontrar elementos com seletores flexíveis
function findElement(baseName) {
    const possibleSelectors = [
        `#id_${baseName}`,
        `#${baseName}`,
        `[name="${baseName}"]`,
        `[name="id_${baseName}"]`
    ];
    
    console.log(`🔍 Procurando elemento: ${baseName}`);
    
    for (const selector of possibleSelectors) {
        const element = $(selector);
        console.log(`   - Tentando seletor: ${selector} -> ${element.length > 0 ? 'ENCONTRADO' : 'Não encontrado'}`);
        if (element.length > 0) {
            console.log(`✅ Encontrado ${baseName} usando seletor: ${selector}`);
            return { element, selector };
        }
    }
    
    // Se não encontrou, vamos tentar buscar por atributos parciais
    const allElements = $('input, select').filter(function() {
        const id = this.id || '';
        const name = this.name || '';
        return id.includes(baseName) || name.includes(baseName);
    });
    
    if (allElements.length > 0) {
        console.log(`🔍 Elementos similares encontrados para ${baseName}:`);
        allElements.each(function() {
            console.log(`   - ID: "${this.id}", Name: "${this.name}", Tag: ${this.tagName}`);
        });
    }
    
    console.warn(`⚠️ ${baseName} não encontrado com nenhum seletor`);
    return null;
}

// Função para aguardar elementos estarem disponíveis
function waitForElements(retries = 5, delay = 500) {
    console.log(`🔄 Tentativa ${6 - retries} de verificar elementos...`);
    
    const elementos = [
        'uf_notificacao',
        'municipio_notificacao', 
        'uf_residencia',
        'municipio_residencia',
        'uf_transferencia',
        'municipio_transferencia',
        'municipio_ocorrencia',
        'municipio_investigador'
    ];
    
    // Mapear nomes dos elementos para seletores corretos
    const elementoMap = {
        'uf_notificacao': 'id_uf_notificacao',
        'municipio_notificacao': 'id_municipio_notificacao',
        'uf_residencia': 'id_uf_residencia', 
        'municipio_residencia': 'id_municipio_residencia',
        'uf_transferencia': 'id_uf_transferencia',
        'municipio_transferencia': 'id_municipio_transferencia',
        'municipio_ocorrencia': 'id_municipio_ocorrencia',
        'municipio_investigador': 'id_municipio_investigador'
    };
    
    let elementosEncontrados = 0;
    const elementosDisponiveis = {};
    
    elementos.forEach(baseName => {
        // Usar o mapeamento correto para encontrar o elemento
        const realFieldName = elementoMap[baseName] || baseName;
        const result = findElement(realFieldName);
        if (result) {
            elementosEncontrados++;
            elementosDisponiveis[baseName] = result.selector;
        }
    });
    
    console.log(`📊 Elementos encontrados: ${elementosEncontrados}/${elementos.length}`);
    
    if (elementosEncontrados >= 3 || retries <= 0) { // Pelo menos 3 elementos ou esgotou tentativas
        console.log('✅ Prosseguindo com inicialização...');
        try {
            initializeFormulario(elementosDisponiveis);
        } catch (error) {
            console.error('❌ Erro durante inicialização do formulário:', error);
        }
    } else if (retries > 0) {
        console.log(`⏳ Aguardando ${delay}ms antes da próxima tentativa...`);
        setTimeout(() => waitForElements(retries - 1, delay), delay);
    } else {
        console.warn('⚠️ Elementos não encontrados após todas as tentativas. Inicializando mesmo assim...');
        try {
            initializeFormulario({});
        } catch (error) {
            console.error('❌ Erro durante inicialização do formulário:', error);
        }
    }
}

// Função para detectar se estamos editando uma ocorrência existente
function isEditMode() {
    // Verificar se há valores preenchidos nos campos principais
    // Agora que os campos de data têm IDs explícitos, podemos usá-los
    const hasData = $('#id_data_notificacao').val() || 
                   $('#id_nome_paciente').val() || 
                   $('#id_num_registro').val() ||
                   $('input[name="nome_paciente"]').val() ||
                   $('input[name="num_registro"]').val();
    
    // Verificar também se há um ID de ocorrência na URL (indicativo de edição)
    const urlPath = window.location.pathname;
    const isEditUrl = urlPath.includes('/edit/') || urlPath.match(/\/\d+\/$/);
    
    const editMode = (hasData && hasData.length > 0) || isEditUrl;
    console.log(`🔍 Detecção de modo: dados=${!!hasData}, URL=${isEditUrl}, modo=${editMode ? 'EDIÇÃO' : 'CRIAÇÃO'}`);
    
    return editMode;
}

// Função para verificar campos de data (apenas para debug)
function verificarCamposData() {
    console.log('📅 Verificando campos de data...');
    
    const dateFields = [
        'id_data_notificacao', 'id_data_acidente', 'id_data_cadastro', 'id_data_nascimento',
        'id_data_investigacao', 'id_data_atendimento', 'id_data_transferencia', 'id_data_cadastro_atendimento'
    ];
    
    dateFields.forEach(fieldId => {
        const $field = $(`#${fieldId}`);
        if ($field.length > 0) {
            const currentValue = $field.val();
            console.log(`📅 Campo ${fieldId}: valor atual = "${currentValue}"`);
        }
    });
}

// Inicialização quando o documento estiver pronto
$(document).ready(function() {
    console.log('📄 DOM ready - aguardando elementos...');
    
    // Detectar modo de edição
    const editMode = isEditMode();
    console.log(`🔍 Modo detectado: ${editMode ? 'EDIÇÃO' : 'CRIAÇÃO'}`);
    
    // Verificar campos de data
    verificarCamposData();
    
    // Aguardar um pouco mais para garantir que o formulário foi renderizado
    setTimeout(() => {
        waitForElements();
        // Verificar novamente após inicialização
        setTimeout(verificarCamposData, 500);
        // Inicializar municípios específicos após um delay adicional
        setTimeout(initializeMunicipiosEspecificos, 1000);
    }, 200);
});

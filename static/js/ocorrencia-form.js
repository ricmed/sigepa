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

// Função para carregar municípios dinamicamente
function loadMunicipios(ufId, target) {
    console.log('🔄 Carregando municípios para UF:', ufId, 'target:', target);
    
    if (!ufId || !target) {
        console.log('⚠️ Parâmetros inválidos - UF:', ufId, 'Target:', target);
        return;
    }
    
    var municipioSelect = $(target);
    if (municipioSelect.length === 0) {
        console.error('❌ Elemento target não encontrado:', target);
        return;
    }
    
    // Mostrar indicador de carregamento
    municipioSelect.prop('disabled', true);
    municipioSelect.html('<option value="">Carregando...</option>');
    
    console.log('📡 Fazendo requisição AJAX...');
    
    $.ajax({
        url: '/core/api/municipios/',
        method: 'GET',
        data: { 'estado_id': ufId },
        dataType: 'json',
        success: function(data) {
            console.log('✅ Resposta da API:', data);
            
            // Limpar select atual
            municipioSelect.empty();
            municipioSelect.append('<option value="">Selecione...</option>');
            
            // Verificar se a resposta é válida
            if (data && data.success !== false) {
                // Adicionar municípios
                if (data.municipios && data.municipios.length > 0) {
                    $.each(data.municipios, function(index, municipio) {
                        municipioSelect.append('<option value="' + municipio.id + '">' + municipio.nome + '</option>');
                    });
                    console.log('📋 Municípios adicionados:', data.municipios.length);
                } else {
                    municipioSelect.append('<option value="">Nenhum município encontrado</option>');
                    console.log('⚠️ Nenhum município encontrado');
                }
            } else {
                municipioSelect.append('<option value="">Erro na resposta</option>');
                console.log('❌ Resposta inválida da API');
            }
            
            // Reabilitar o select
            municipioSelect.prop('disabled', false);
        },
        error: function(xhr, status, error) {
            console.error('❌ Erro na requisição:', error);
            console.error('Status:', status);
            console.error('Response:', xhr.responseText);
            
            municipioSelect.empty();
            municipioSelect.append('<option value="">Erro ao carregar</option>');
            municipioSelect.prop('disabled', false);
        }
    });
}

// Inicialização quando o documento estiver pronto
$(document).ready(function() {
    console.log('Inicializando formulário com modais de pesquisa...');
    
    // Verificar se os elementos UF e Município existem
    console.log('🔍 Verificando elementos UF e Município no document.ready:');
    console.log('   - UF Notificação:', $('#id_uf_notificacao').length ? 'Existe' : 'Não Existe');
    console.log('   - Município Notificação:', $('#id_municipio_notificacao').length ? 'Existe' : 'Não Existe');
    console.log('   - UF Residência:', $('#id_uf_residencia').length ? 'Existe' : 'Não Existe');
    console.log('   - Município Residência:', $('#id_municipio_residencia').length ? 'Existe' : 'Não Existe');
    console.log('   - UF Transferência:', $('#id_uf_transferencia').length ? 'Existe' : 'Não Existe');
    console.log('   - Município Transferência:', $('#id_municipio_transferencia').length ? 'Existe' : 'Não Existe');

    // Gatilho para carregar municípios ao mudar o estado
    $('#id_uf_notificacao').on('change', function() {
        var ufId = $(this).val();
        console.log('🔄 UF Notificação mudou para:', ufId);
        
        // Limpar município atual
        $('#id_municipio_notificacao').val('');
        
        if (ufId) {
            loadMunicipios(ufId, '#id_municipio_notificacao');
        } else {
            $('#id_municipio_notificacao').empty().append('<option value="">Selecione...</option>');
        }
    });
    
    $('#id_uf_residencia').on('change', function() {
        var ufId = $(this).val();
        console.log('🔄 UF Residência mudou para:', ufId);
        
        // Limpar município atual
        $('#id_municipio_residencia').val('');
        
        if (ufId) {
            loadMunicipios(ufId, '#id_municipio_residencia');
        } else {
            $('#id_municipio_residencia').empty().append('<option value="">Selecione...</option>');
        }
    });
    
    $('#id_uf_transferencia').on('change', function() {
        var ufId = $(this).val();
        console.log('🔄 UF Transferência mudou para:', ufId);
        
        // Limpar município atual
        $('#id_municipio_transferencia').val('');
        
        if (ufId) {
            loadMunicipios(ufId, '#id_municipio_transferencia');
        } else {
            $('#id_municipio_transferencia').empty().append('<option value="">Selecione...</option>');
        }
    });

    // Carregar municípios iniciais se já houver UF selecionada
    console.log('🔍 Verificando UFs já selecionadas para carregamento inicial...');
    if ($('#id_uf_notificacao').val()) {
        console.log('📍 Carregando municípios iniciais para notificação');
        loadMunicipios($('#id_uf_notificacao').val(), '#id_municipio_notificacao');
    }
    if ($('#id_uf_residencia').val()) {
        console.log('📍 Carregando municípios iniciais para residência');
        loadMunicipios($('#id_uf_residencia').val(), '#id_municipio_residencia');
    }
    if ($('#id_uf_transferencia').val()) {
        console.log('📍 Carregando municípios iniciais para transferência');
        loadMunicipios($('#id_uf_transferencia').val(), '#id_municipio_transferencia');
    }
});

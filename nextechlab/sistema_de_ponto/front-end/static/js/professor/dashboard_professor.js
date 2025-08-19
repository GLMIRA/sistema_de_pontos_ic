// Dashboard Professor JavaScript

// Carregamento dos dados do Django
let dadosPorAluno = {};

// Função para carregar dados do script JSON
function carregarDadosDjango() {
    try {
        const scriptElement = document.getElementById('dados-django');
        if (scriptElement) {
            dadosPorAluno = JSON.parse(scriptElement.textContent);
            console.log('Dashboard carregado com', Object.keys(dadosPorAluno).length, 'alunos');
        } else {
            console.error('Elemento script dados-django não encontrado');
        }
    } catch (error) {
        console.error('Erro ao carregar dados do Django:', error);
    }
}

/**
 * Função chamada quando clica em um card de aluno
 * @param {number} alunoId - ID do aluno selecionado
 */
function selecionarAluno(alunoId) {
    // Remove seleção anterior
    document.querySelectorAll('.card-aluno').forEach(card => {
        card.classList.remove('selecionado');
    });

    // Adiciona seleção no card clicado
    const cardSelecionado = document.querySelector(`[data-aluno-id="${alunoId}"]`);
    if (cardSelecionado) {
        cardSelecionado.classList.add('selecionado');
    }

    // Busca os dados do aluno
    const dadosAluno = dadosPorAluno[alunoId];

    if (!dadosAluno) {
        console.error('Dados do aluno não encontrados:', alunoId);
        mostrarErro('Erro ao carregar dados do aluno');
        return;
    }

    console.log('Carregando dados do aluno:', dadosAluno.nome);

    // Atualiza as informações do aluno selecionado
    document.getElementById('nome-aluno-selecionado').textContent = dadosAluno.nome;
    document.getElementById('horas-aluno-selecionado').textContent = formatarHoras(dadosAluno.total_horas);
    document.getElementById('registros-aluno-selecionado').textContent = dadosAluno.total_registros;
    document.getElementById('titulo-aluno').textContent = dadosAluno.nome;

    // Limpa a tabela e adiciona loading
    const corpoTabela = document.getElementById('tabela-registros-corpo');
    corpoTabela.innerHTML = `
        <tr>
            <td colspan="4" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <br>
                <small class="text-muted mt-2">Carregando registros...</small>
            </td>
        </tr>
    `;

    // Simula um pequeno delay para mostrar o loading
    setTimeout(() => {
        corpoTabela.innerHTML = '';

        // Adiciona os registros na tabela
        if (dadosAluno.registros && dadosAluno.registros.length > 0) {
            dadosAluno.registros.forEach((registro) => {
                const linha = document.createElement('tr');
                linha.innerHTML = `
                    <td>
                        <i class="bi bi-calendar3"></i>
                        <strong>${registro.data}</strong>
                    </td>
                    <td>
                        <span class="badge bg-primary">
                            <i class="bi bi-clock"></i>
                            ${registro.hora}
                        </span>
                    </td>
                    <td>
                        <span class="badge bg-${registro.tipo === 'entrada' ? 'success' : 'danger'}">
                            <i class="bi bi-${registro.tipo === 'entrada' ? 'box-arrow-in-right' : 'box-arrow-left'}"></i>
                            ${registro.tipo.charAt(0).toUpperCase() + registro.tipo.slice(1)}
                        </span>
                    </td>
                    <td class="text-muted">
                        <i class="bi bi-info-circle"></i>
                        ${registro.data_hora}
                    </td>
                `;
                corpoTabela.appendChild(linha);
            });
        } else {
            // Caso não tenha registros
            corpoTabela.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center py-5">
                        <i class="bi bi-inbox text-muted" style="font-size: 3rem;"></i>
                        <h5 class="text-muted mt-3">Nenhum registro encontrado</h5>
                        <p class="text-muted">Este aluno ainda não possui registros de ponto.</p>
                    </td>
                </tr>
            `;
        }

        // Mostra as seções que estavam escondidas
        const infoAlunoSection = document.querySelector('.info-aluno-selecionado');
        const tabelaSection = document.querySelector('.tabela-registros');

        if (infoAlunoSection) infoAlunoSection.style.display = 'block';
        if (tabelaSection) tabelaSection.style.display = 'block';

        // Scroll suave para a seção de informações
        if (infoAlunoSection) {
            infoAlunoSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }

    }, 500); // Delay para mostrar o loading
}

/**
 * Limpa a seleção e volta para a visualização inicial
 */
function limparSelecao() {
    // Remove todas as seleções
    document.querySelectorAll('.card-aluno').forEach(card => {
        card.classList.remove('selecionado');
    });

    // Esconde as seções
    const infoAlunoSection = document.querySelector('.info-aluno-selecionado');
    const tabelaSection = document.querySelector('.tabela-registros');

    if (infoAlunoSection) infoAlunoSection.style.display = 'none';
    if (tabelaSection) tabelaSection.style.display = 'none';

    // Scroll suave para o topo
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });

    console.log('Seleção limpa');
}

/**
 * Converte horas decimais para formato "Xh Ym"
 * @param {number} totalHoras - Total de horas em decimal
 * @returns {string} - Formato "Xh Ym"
 */
function formatarHoras(totalHoras) {
    if (!totalHoras || totalHoras === 0) return '0h 0m';

    const horas = Math.floor(Math.abs(totalHoras));
    const minutos = Math.round((Math.abs(totalHoras) - horas) * 60);
    const sinal = totalHoras < 0 ? '-' : '';

    return `${sinal}${horas}h ${minutos}m`;
}

/**
 * Mostra mensagem de erro
 */
function mostrarErro(mensagem) {
    alert('Erro: ' + mensagem);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function () {
    // Carrega dados do Django
    carregarDadosDjango();

    // Event listeners para cards de aluno
    document.querySelectorAll('.card-aluno').forEach(card => {
        card.addEventListener('click', function () {
            const alunoId = parseInt(this.getAttribute('data-aluno-id'));
            selecionarAluno(alunoId);
        });
    });

    // Event listener para tecla ESC
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            limparSelecao();
        }
    });

    // Adiciona event listener para o botão limpar seleção
    const btnLimpar = document.getElementById('btn-limpar-selecao');
    if (btnLimpar) {
        btnLimpar.addEventListener('click', limparSelecao);
    }

    // Animação de entrada para os cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function (card, index) {
        card.style.animation = `fadeInUp 0.6s ease forwards ${index * 0.1}s`;
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
    });

    console.log('Dashboard totalmente carregado!');
});
document.addEventListener('DOMContentLoaded', function () {
    const tipoAluno = document.getElementById('tipo_aluno');
    const tipoProfessor = document.getElementById('tipo_professor');
    const usernameLabel = document.getElementById('usernameLabel');
    const alunoHelp = document.getElementById('alunoHelp');
    const professorHelp = document.getElementById('professorHelp');
    const usernameField = document.getElementById('{{ form.username.id_for_label }}');

    function updateInterface() {
        if (tipoAluno.checked) {
            usernameLabel.textContent = 'RA (Registro Acadêmico)';
            alunoHelp.style.display = 'block';
            professorHelp.style.display = 'none';
            usernameField.placeholder = 'Ex: a1234567';
            usernameField.setAttribute('pattern', '^a\\d{7}$');
        } else {
            usernameLabel.textContent = 'Nome de Usuário';
            alunoHelp.style.display = 'none';
            professorHelp.style.display = 'block';
            usernameField.placeholder = 'Ex: joao.silva';
            usernameField.removeAttribute('pattern');
        }
    }

    // Event listeners para mudança de tipo
    tipoAluno.addEventListener('change', updateInterface);
    tipoProfessor.addEventListener('change', updateInterface);

    // Validação em tempo real
    usernameField.addEventListener('input', function () {
        const value = this.value.toLowerCase().trim();

        if (tipoAluno.checked) {
            // Para alunos: deve ser formato RA (a + 7 dígitos)
            if (value && !value.match(/^a\d{0,7}$/)) {
                this.setCustomValidity('RA deve seguir o formato a1234567');
            } else if (value && value.length === 8 && !value.match(/^a\d{7}$/)) {
                this.setCustomValidity('RA deve ter exatamente 7 dígitos após o "a"');
            } else {
                this.setCustomValidity('');
            }
        } else {
            // Para professores: não pode ser formato RA
            if (value.match(/^a\d+$/)) {
                this.setCustomValidity('Professores não podem usar formato de RA');
            } else {
                this.setCustomValidity('');
            }
        }
    });

    // Validação no submit
    document.getElementById('cadastroForm').addEventListener('submit', function (e) {
        const username = usernameField.value.trim().toLowerCase();

        if (tipoAluno.checked) {
            if (!username.match(/^a\d{7}$/)) {
                alert('Para alunos, o RA deve ter o formato: a1234567\n(letra "a" seguida de exatamente 7 dígitos)');
                e.preventDefault();
                usernameField.focus();
                return false;
            }
        } else {
            if (username.match(/^a\d+$/)) {
                alert('Professores não podem usar formato de RA como username\nEscolha um nome de usuário diferente.');
                e.preventDefault();
                usernameField.focus();
                return false;
            }
        }
    });

    // Atualiza visual dos cards de tipo de usuário
    function updateCardSelection() {
        const alunoCard = document.querySelector('label[for="tipo_aluno"] .card');
        const professorCard = document.querySelector('label[for="tipo_professor"] .card');

        if (tipoAluno.checked) {
            alunoCard.classList.add('border-primary', 'bg-primary', 'bg-opacity-10');
            alunoCard.classList.remove('border-warning', 'bg-warning', 'bg-opacity-10');
            professorCard.classList.remove('border-warning', 'bg-warning', 'bg-opacity-10');
        } else {
            professorCard.classList.add('border-warning', 'bg-warning', 'bg-opacity-10');
            professorCard.classList.remove('border-primary', 'bg-primary', 'bg-opacity-10');
            alunoCard.classList.remove('border-primary', 'bg-primary', 'bg-opacity-10');
        }
    }

    tipoAluno.addEventListener('change', updateCardSelection);
    tipoProfessor.addEventListener('change', updateCardSelection);

    // Inicializa a interface
    updateInterface();
    updateCardSelection();

    // Animação dos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function (card, index) {
        card.style.animation = `fadeInUp 0.6s ease forwards ${index * 0.1}s`;
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
    });
});
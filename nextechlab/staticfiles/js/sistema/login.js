
document.addEventListener('DOMContentLoaded', function () {
    const usernameField = document.getElementById('id_username');
    const form = document.querySelector('form');

    usernameField.focus();

    usernameField.addEventListener('input', function () {
        const value = this.value.trim().toLowerCase();

        if (value.match(/^a\d/)) {
            if (!value.match(/^a\d{7}$/)) {
                this.setCustomValidity('RA deve ter o formato: a1234567');
            } else {
                this.setCustomValidity('');
            }
        } else {
            this.setCustomValidity('');
        }
    });

    form.addEventListener('submit', function (e) {
        const username = usernameField.value.trim().toLowerCase();

        if (username.startsWith('a') && username.length > 1 && username.length !== 8) {
            if (!username.match(/^a\d{7}$/)) {
                alert('Formato de RA incorreto. Use: a1234567 (letra "a" seguida de 7 dígitos)');
                e.preventDefault();
                usernameField.focus();
                return false;
            }
        }
    });

    const card = document.querySelector('.card');
    card.style.animation = 'fadeInScale 0.5s ease forwards';
    card.style.opacity = '0';
    card.style.transform = 'scale(0.95)';
});

document.addEventListener('DOMContentLoaded', function () {
    // Adiciona animação simples aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function (card, index) {
        card.style.animation = `fadeInUp 0.6s ease forwards ${index * 0.1}s`;
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
    });
});

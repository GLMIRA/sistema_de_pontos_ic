document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.animation = `fadeInUp 0.6s ease forwards ${index * 0.1}s`;
    });
});


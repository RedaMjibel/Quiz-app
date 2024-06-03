document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            card.classList.add('shadow-lg');
        });

        card.addEventListener('mouseleave', function() {
            card.classList.remove('shadow-lg');
        });
    });

    document.getElementById('displayYear').textContent = new Date().getFullYear();
});
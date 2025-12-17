// Script principal

document.addEventListener('DOMContentLoaded', function() {
    console.log('Site Django chargé !');
    
    // Gestion de la notification
    const notification = document.getElementById('notification');
    const closeNotificationBtn = document.getElementById('close-notification');
    
    if (closeNotificationBtn) {
        closeNotificationBtn.addEventListener('click', function() {
            notification.style.animation = 'slideOut 0.5s ease-out forwards';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 500);
        });
        
        // Auto-fermeture après 10 secondes
        setTimeout(() => {
            if (notification.style.display !== 'none') {
                notification.style.animation = 'slideOut 0.5s ease-out forwards';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 500);
            }
        }, 10000);
    }
    
    // Ajouter l'animation slideOut
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Gestion des boutons "Lire la suite"
    const readMoreButtons = document.querySelectorAll('.btn-read-more');
    readMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const articleId = this.getAttribute('data-id');
            alert(`Ouverture de l'article ${articleId}...\n(Fonctionnalité à implémenter)`);
            // Ici, vous pourriez rediriger vers la page détaillée de l'article
            // window.location.href = `/article/${articleId}/`;
        });
    });
    
    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observer les cartes d'articles
    document.querySelectorAll('.article-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
    
    // Gestion du menu mobile (si ajouté plus tard)
    const setupMobileMenu = () => {
        const nav = document.querySelector('nav');
        if (window.innerWidth <= 768) {
            // Ajouter un bouton menu pour mobile si nécessaire
            if (!document.querySelector('.menu-toggle')) {
                const menuToggle = document.createElement('button');
                menuToggle.className = 'menu-toggle';
                menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
                nav.insertBefore(menuToggle, nav.querySelector('.nav-links'));
                
                menuToggle.addEventListener('click', () => {
                    const navLinks = document.querySelector('.nav-links');
                    navLinks.classList.toggle('show');
                });
            }
        }
    };
    
    // Appeler la fonction de menu mobile
    setupMobileMenu();
    
    // Re-configurer le menu mobile lors du redimensionnement
    window.addEventListener('resize', setupMobileMenu);
});
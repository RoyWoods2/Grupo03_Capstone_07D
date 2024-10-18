let lastScrollTop = 0;
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

// Manejar el desplazamiento para el Smart Fixed Nav
window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Ocultar el navbar cuando el usuario se desplaza hacia abajo
        navbar.classList.add('nav-hidden');
        navbar.classList.remove('sticky');
    } else {
        // Mostrar el navbar cuando el usuario se desplaza hacia arriba
        navbar.classList.remove('nav-hidden');
        navbar.classList.add('sticky');
    }

    lastScrollTop = scrollTop; // Actualizar la última posición de scroll
});

// Manejar el colapso/mostrar del menú cuando se hace clic en el botón hamburguesa
hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

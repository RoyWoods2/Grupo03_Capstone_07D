// static/js/navbar.js

window.addEventListener('scroll', function() {
  const navbar = document.getElementById('navbar');
  const scrollPosition = window.scrollY || document.documentElement.scrollTop;

  // Colapsar la navbar si el usuario ha hecho scroll hacia abajo
  if (scrollPosition > 100) {
      navbar.classList.add('collapsed');
  } else {
      navbar.classList.remove('collapsed');
  }
});

// static/js/navbar.js

// Obtener los elementos del DOM
const navbarToggler = document.getElementById('navbar-toggler');
const navbarMenu = document.getElementById('navbar-menu');

// Función para alternar la visibilidad del menú
navbarToggler.addEventListener('click', function() {
    navbarMenu.classList.toggle('show');
});


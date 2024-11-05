document.addEventListener("DOMContentLoaded", function() {
    const videoContainer = document.getElementById('videoContainer');
    const mainContent = document.getElementById('mainContent');
    const topNavbar = document.querySelector('.top-navbar'); // Selecciona el header

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            videoContainer.classList.add('fade-out');
            mainContent.classList.add('show-content');
            topNavbar.classList.add('show-header'); // Muestra el header
        } else {
            videoContainer.classList.remove('fade-out');
            mainContent.classList.remove('show-content');
            topNavbar.classList.remove('show-header'); // Oculta el header
        }
    });
});

if (window.location.pathname === '') { // Asegúrate de usar la ruta de la main page
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            topNavbar.classList.add('sticky');
        } else {
            topNavbar.classList.remove('sticky');
        }
    });
}
  // Función para detectar el scroll y modificar el video
  window.addEventListener('scroll', function() {
    var scrollY = window.scrollY;
    var videoContainer = document.getElementById('video-container');

    if (scrollY > window.innerHeight / 2) {
        videoContainer.classList.add('hidden'); // Oculta el video al hacer scroll
    } else {
        videoContainer.classList.remove('hidden'); // Muestra el video cuando vuelve hacia arriba
    }
});
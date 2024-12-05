self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('v1').then(function(cache) {
            return cache.addAll([
                '/',  // Asegúrate de que esta ruta exista
                '/polls/css/styleHome.css',
                '/polls/js/scripts.js',
                '/polls/js/service-worker.js',
                '/static/polls/manifest.json',
                // Otras rutas...
            ]);
        })
    );
});

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('v1').then(function(cache) {
            return cache.addAll([
                '/',
                '/polls/css/styleHome.css',
                '/polls/js/scripts.js',
            ]).catch(function(error) {
                console.error('Error al cachear recursos:', error);
            });
        })
    );
});

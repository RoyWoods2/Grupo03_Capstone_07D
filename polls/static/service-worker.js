self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open('my-cache-v1').then(function(cache) {
        return cache.addAll([
          '/',
          '/static/css/styles.css',
          '/static/js/main.js',
          '/static/images/logo.png',
          '/static/manifest.json',
          '/static/index.html'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });
  
  self.addEventListener('activate', function(event) {
    var cacheWhitelist = ['my-cache-v1'];
    event.waitUntil(
      caches.keys().then(function(cacheNames) {
        return Promise.all(
          cacheNames.map(function(cacheName) {
            if (cacheWhitelist.indexOf(cacheName) === -1) {
              return caches.delete(cacheName);
            }
          })
        );
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


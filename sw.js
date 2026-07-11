// Service worker Hawkthorne (v18, S9): cache-first, il gioco funziona OFFLINE.
// Bump del nome cache a ogni release per invalidare la copia vecchia.
const CACHE = 'hawkthorne-v20.9';
const CORE = ['./', './index.html', './manifest.webmanifest', './assets/icon-192.png', './assets/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(hit => {
      const rete = fetch(e.request).then(res => {
        if (res && res.ok){ const cl = res.clone(); caches.open(CACHE).then(c => c.put(e.request, cl)); }
        return res;
      }).catch(() => hit || caches.match('./index.html'));
      return hit || rete;   // cache-first: offline sempre, aggiornamento in background
    })
  );
});

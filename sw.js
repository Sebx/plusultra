const CACHE = "plusultra-f1a6884d5e83";
const SHELL = [
  "/",
  "/index.html",
  "/app.css",
  "/app.js",
  "/worker.js",
  "/manifest.webmanifest",
  "/icon.svg",
  "/doom.html",
  "/doom.js",
  "/doom.css",
  "/gpu-worker.js",
];
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((c) => c.addAll(SHELL))
      .then(() => self.skipWaiting()),
  );
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k.startsWith("plusultra-") && k !== CACHE)
            .map((k) => caches.delete(k)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (
    event.request.method !== "GET" ||
    url.origin !== self.location.origin ||
    url.pathname.startsWith("/v1/") ||
    url.pathname.startsWith("/model/") ||
    url.pathname === "/health"
  )
    return;
  event.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const hit = await cache.match(event.request);
      const shell = url.pathname === '/' || /\.(?:html|js|css)$/.test(url.pathname);
      if (hit && !shell) return hit;
      let response;
      try { response = await fetch(event.request); }
      catch (error) { if (hit) return hit; throw error; }
      if (response.ok)
        event.waitUntil(
          cache.put(event.request, response.clone()).catch(() => {}),
        );
      return response;
    }),
  );
});

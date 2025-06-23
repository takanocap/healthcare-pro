
const VAPID_PUBLIC_KEY = 'YOUR_VAPID_PUBLIC_KEY_FROM_BACKEND';

self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  event.waitUntil(
    self.clients.claim()
  );
});

self.addEventListener('push', (event) => {
  console.log('Push event received:', event);
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'New Notification';
  const options = {
    body: data.body || 'You have a new message or insight.',
    icon: data.icon || '/android-chrome-192x192.png', // Path to your app icon
    badge: data.badge || '/apple-touch-icon.png', // Path to a badge icon (optional)
    data: { // Custom data to pass to the notificationclick event
      url: data.url || '/', // URL to open when notification is clicked
      type: data.type || 'generic',
      insightId: data.insightId // Example: Pass an insight ID
    },
    actions: data.actions || [], // Example: actions for interactive notifications
    vibrate: [200, 100, 200]
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  console.log('Notification click received:', event);
  event.notification.close(); // Close the notification

  const clickedNotification = event.notification;
  const urlToOpen = clickedNotification.data.url || '/'; // Default to homepage
  const notificationType = clickedNotification.data.type;
  const insightId = clickedNotification.data.insightId;

  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes(urlToOpen) && 'focus' in client) {
          // If a client is open and matching the URL, focus it
          return client.focus();
        }
      }
      // Otherwise, open a new window/tab
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );

  // Handle specific actions if defined
  if (event.action) {
    console.log(`Notification action '${event.action}' clicked.`);
    // Example: send data to backend or trigger another agent
    // self.clients.matchAll().then(clients => {
    //   clients.forEach(client => {
    //     client.postMessage({ action: event.action, insightId: insightId });
    //   });
    // });
  }
});

// For offline capabilities (optional, but part of PWA)
// self.addEventListener('fetch', (event) => {
//   event.respondWith(
//     caches.match(event.request).then((response) => {
//       return response || fetch(event.request);
//     })
//   );
// });

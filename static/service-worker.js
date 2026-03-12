/**
 * TeacherManager Service Worker
 * 
 * Handles:
 * - Offline caching strategy
 * - Background sync for attendance marking
 * - Push notifications
 */

const CACHE_NAME = 'teachermanager-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/manifest.json',
];

/**
 * Install event - cache essential assets
 */
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching assets');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

/**
 * Fetch event - network-first with cache fallback
 */
self.addEventListener('fetch', (event) => {
    // Don't cache POST requests or API calls that modify data
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Cache successful responses
                if (response && response.status === 200) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return response;
            })
            .catch(() => {
                // Fallback to cache if network fails
                return caches.match(event.request).then((cachedResponse) => {
                    return cachedResponse || new Response('Offline - resource not available', {
                        status: 503,
                        statusText: 'Service Unavailable',
                        headers: new Headers({
                            'Content-Type': 'text/plain'
                        }),
                    });
                });
            })
    );
});

/**
 * Background Sync - sync attendance records when back online
 */
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-attendance') {
        event.waitUntil(syncAttendanceRecords());
    }
});

/**
 * Sync attendance records queued while offline
 */
async function syncAttendanceRecords() {
    try {
        // Open IndexedDB to fetch queued attendance records
        const db = await openDb();
        const tx = db.transaction('attendanceQueue', 'readonly');
        const store = tx.objectStore('attendanceQueue');
        const queuedRecords = await store.getAll();

        // Attempt to sync each queued record
        for (const record of queuedRecords) {
            try {
                const response = await fetch('/api/v1/attendance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(record),
                });

                if (response.ok) {
                    // Remove from queue on success
                    const deleteTx = db.transaction('attendanceQueue', 'readwrite');
                    await deleteTx.objectStore('attendanceQueue').delete(record.id);
                }
            } catch (err) {
                console.log('Background sync failed for record:', record.id, err);
            }
        }
    } catch (err) {
        console.log('Background sync error:', err);
        throw err;
    }
}

/**
 * Helper: Open IndexedDB connection
 */
function openDb() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('TeacherManagerDB', 1);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('attendanceQueue')) {
                db.createObjectStore('attendanceQueue', { keyPath: 'id' });
            }
        };
    });
}

/**
 * Push Notification event - handle incoming push from server
 */
self.addEventListener('push', (event) => {
    if (!event.data) {
        return;
    }

    const data = event.data.json();
    const options = {
        body: data.body || 'New notification from TeacherManager',
        icon: '/static/icon-192x192.png',
        badge: '/static/badge-72x72.png',
        tag: data.tag || 'default',
        requireInteraction: false,
        actions: [
            {
                action: 'open',
                title: 'Open',
            },
            {
                action: 'close',
                title: 'Close',
            },
        ],
    };

    event.waitUntil(self.registration.showNotification(data.title, options));
});

/**
 * Notification Click event - handle user clicking notification
 */
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'close') {
        return;
    }

    event.waitUntil(
        clients
            .matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Check if the app is already open
                for (let i = 0; i < clientList.length; i++) {
                    const client = clientList[i];
                    if (client.url === '/' && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Otherwise, open a new window
                if (clients.openWindow) {
                    return clients.openWindow('/');
                }
            })
    );
});

/**
 * Message event - receive messages from pages
 * Allows cache management and offline state communication
 */
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'GET_OFFLINE_STATUS') {
        event.ports[0].postMessage({
            offline: !navigator.onLine,
        });
    }

    if (event.data && event.data.type === 'CLEAR_CACHE') {
        caches.delete(CACHE_NAME).then(() => {
            event.ports[0].postMessage({ status: 'cache cleared' });
        });
    }
});

console.log('TeacherManager Service Worker loaded');

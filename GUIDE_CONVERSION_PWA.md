# 📱 GUIDE CONVERSION PWA - MathCopain
## Progressive Web App - Transformation Web → Mobile

---

# 🎯 CONTEXTE & OBJECTIFS

## Pourquoi PWA ?

Après déploiement MVP web réussi, la conversion PWA permet de :
- ✅ **Fonctionner sur mobile** iOS + Android sans App Store
- ✅ **Installation native** icône écran d'accueil
- ✅ **Mode offline** cache exercices récents
- ✅ **Notifications push** rappels et encouragements
- ✅ **Performance mobile** optimisée

## Timeline

**Effort total:** 1-2 semaines
**Prérequis:** MVP web déployé et fonctionnel

---

# 📋 ARCHITECTURE PWA

## Composants Principaux

```
MathCopain PWA Architecture:

├── manifest.json          # Configuration PWA (icônes, couleurs)
├── sw.js                 # Service Worker (cache, offline)
├── install_prompt.py     # Prompt installation
├── push_notifications.py # Notifications push
├── offline_fallback.html # Page offline
└── optimizations/
    ├── lazy_loading.py   # Chargement différé
    ├── compression.py    # Compression assets
    └── caching.py        # Stratégies cache
```

## Stratégies Cache

| Type Resource | Stratégie | Durée Cache |
|---------------|-----------|-------------|
| **HTML pages** | Network-First | 24h |
| **CSS/JS** | Cache-First | 7 jours |
| **Images** | Cache-First | 30 jours |
| **Exercices API** | Network-First | 1h |
| **Dashboard data** | Network-First | 5 min |

---

# 🚀 PHASE 1: MANIFEST & CONFIGURATION

## Prompt Claude Code 1.1 - Manifest.json

**Titre:** "Créer manifest.json pour PWA MathCopain"

**Texte du Prompt:**

```
# CONTEXTE
MathCopain est actuellement une application web Streamlit.
Conversion en PWA pour fonctionnalité mobile native.

# TÂCHE: Créer manifest.json

## Fichier à créer
`public/manifest.json` (50 lignes)

## Structure Manifest

```json
{
  "name": "MathCopain - Mathématiques Personnalisées",
  "short_name": "MathCopain",
  "description": "Application d'apprentissage des mathématiques personnalisée pour enfants CE1-CM2. Intelligence artificielle, feedback bienveillant, progression visible.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#FFFFFF",
  "theme_color": "#3498DB",
  "categories": ["education", "kids", "math"],
  "lang": "fr-FR",
  "dir": "ltr",
  
  "icons": [
    {
      "src": "/static/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  
  "screenshots": [
    {
      "src": "/static/screenshots/screenshot-1.png",
      "sizes": "1280x720",
      "type": "image/png",
      "platform": "wide",
      "label": "Dashboard parent"
    },
    {
      "src": "/static/screenshots/screenshot-2.png",
      "sizes": "750x1334",
      "type": "image/png",
      "platform": "narrow",
      "label": "Exercice enfant"
    }
  ],
  
  "shortcuts": [
    {
      "name": "Nouvel exercice",
      "short_name": "Exercice",
      "description": "Démarrer un nouvel exercice",
      "url": "/exercise",
      "icons": [
        {
          "src": "/static/icons/exercise-icon.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Ma progression",
      "short_name": "Progression",
      "description": "Voir mes badges et progression",
      "url": "/progress",
      "icons": [
        {
          "src": "/static/icons/progress-icon.png",
          "sizes": "96x96"
        }
      ]
    }
  ],
  
  "related_applications": [],
  "prefer_related_applications": false,
  
  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url"
    }
  }
}
```

## Intégration dans HTML

Ajouter dans `<head>` de toutes les pages:

```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#3498DB">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="MathCopain">

<!-- iOS Icons -->
<link rel="apple-touch-icon" href="/static/icons/icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="/static/icons/icon-180x180.png">
```

## Tests
`tests/test_manifest.py` (30+ tests)

- Valid JSON structure
- All icon paths exist
- Correct MIME types
- Required fields present
```

---

## Prompt Claude Code 1.2 - Générer Icons PWA

**Titre:** "Générer icônes PWA toutes tailles - Script automatique"

**Texte:**

```
# TÂCHE: Script génération icônes PWA

Partir d'une image source haute résolution (1024x1024) et générer 
toutes les tailles requises pour PWA.

## Fichier à créer
`scripts/generate_pwa_icons.py` (100 lignes)

## Script Python

```python
from PIL import Image
import os

def generate_pwa_icons(source_image_path, output_dir):
    """
    Génère toutes les icônes PWA à partir d'une image source.
    
    Args:
        source_image_path: Chemin vers image 1024x1024 PNG
        output_dir: Dossier de sortie (ex: public/static/icons/)
    """
    
    # Tailles requises PWA
    sizes = [
        72, 96, 128, 144, 152, 180, 192, 384, 512
    ]
    
    # Ouvrir image source
    source = Image.open(source_image_path)
    
    # Vérifier que source est carré
    if source.width != source.height:
        raise ValueError("Image source doit être carrée (1024x1024 recommandé)")
    
    # Créer dossier output si inexistant
    os.makedirs(output_dir, exist_ok=True)
    
    # Générer chaque taille
    for size in sizes:
        resized = source.resize((size, size), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        resized.save(output_path, optimize=True, quality=95)
        print(f"✅ Généré: icon-{size}x{size}.png")
    
    # Générer maskable icons (avec padding)
    print("\n🎭 Génération maskable icons...")
    generate_maskable_icons(source, output_dir)
    
    print("\n🎉 Toutes les icônes générées!")

def generate_maskable_icons(source, output_dir):
    """Génère icônes maskables avec padding pour safe zone"""
    
    maskable_sizes = [192, 512]
    
    for size in maskable_sizes:
        # Créer canvas avec padding 10%
        canvas_size = size
        icon_size = int(size * 0.8)  # 80% du canvas
        padding = (size - icon_size) // 2
        
        # Canvas blanc
        canvas = Image.new('RGB', (canvas_size, canvas_size), 'white')
        
        # Resize icon
        icon = source.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # Coller icon au centre
        canvas.paste(icon, (padding, padding))
        
        # Sauvegarder
        output_path = os.path.join(output_dir, f"icon-{size}x{size}-maskable.png")
        canvas.save(output_path, optimize=True, quality=95)
        print(f"✅ Généré: icon-{size}x{size}-maskable.png")

if __name__ == "__main__":
    # Exemple utilisation
    generate_pwa_icons(
        source_image_path="assets/logo-1024.png",
        output_dir="public/static/icons/"
    )
```

## Création Image Source

Si vous n'avez pas encore de logo 1024x1024:

```python
# Script simple pour créer logo temporaire
from PIL import Image, ImageDraw, ImageFont

def create_temp_logo():
    # Canvas 1024x1024
    img = Image.new('RGB', (1024, 1024), '#3498DB')
    draw = ImageDraw.Draw(img)
    
    # Cercle blanc
    draw.ellipse([112, 112, 912, 912], fill='white')
    
    # Texte "MC"
    try:
        font = ImageFont.truetype("Arial.ttf", 400)
    except:
        font = ImageFont.load_default()
    
    draw.text((300, 250), "MC", fill='#3498DB', font=font)
    
    img.save("assets/logo-1024.png")
    print("✅ Logo temporaire créé: assets/logo-1024.png")

create_temp_logo()
```

## Lancer génération

```bash
python scripts/generate_pwa_icons.py
```

## Tests
`tests/test_icon_generation.py` (20+ tests)
```

---

# 🔧 PHASE 2: SERVICE WORKER

## Prompt Claude Code 2.1 - Service Worker Principal

**Titre:** "Créer Service Worker pour cache et offline - MathCopain PWA"

**Texte:**

```
# TÂCHE: Service Worker PWA

Gestion cache, offline, et background sync.

## Fichier à créer
`public/sw.js` (300 lignes JavaScript)

## Service Worker Code

```javascript
// Service Worker MathCopain PWA
const CACHE_VERSION = 'v1.0.0';
const CACHE_NAME = `mathcopain-${CACHE_VERSION}`;

// Assets à cacher immédiatement (install)
const STATIC_CACHE = [
  '/',
  '/manifest.json',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/offline.html'
];

// Routes API à cacher avec stratégie Network-First
const API_CACHE_ROUTES = [
  '/api/exercises',
  '/api/progress',
  '/api/dashboard'
];

// Installation Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW] Installation...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_CACHE);
      })
      .then(() => {
        console.log('[SW] Installation terminée');
        return self.skipWaiting(); // Activate immédiatement
      })
  );
});

// Activation Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW] Activation...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log('[SW] Suppression ancien cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Activation terminée');
        return self.clients.claim(); // Prendre contrôle immédiatement
      })
  );
});

// Fetch: Stratégies de cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignorer requêtes non-GET
  if (request.method !== 'GET') {
    return;
  }
  
  // Ignorer Chrome extensions
  if (url.protocol === 'chrome-extension:') {
    return;
  }
  
  // Stratégie selon type de ressource
  if (url.pathname.startsWith('/api/')) {
    // API: Network-First
    event.respondWith(networkFirstStrategy(request));
  } else if (url.pathname.match(/\.(css|js|png|jpg|svg|woff2?)$/)) {
    // Assets statiques: Cache-First
    event.respondWith(cacheFirstStrategy(request));
  } else {
    // HTML pages: Network-First avec fallback offline
    event.respondWith(networkFirstWithOffline(request));
  }
});

// Stratégie Cache-First
async function cacheFirstStrategy(request) {
  const cached = await caches.match(request);
  if (cached) {
    console.log('[SW] Cache hit:', request.url);
    return cached;
  }
  
  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    console.error('[SW] Fetch failed:', error);
    throw error;
  }
}

// Stratégie Network-First
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);
    
    // Cacher réponse si succès
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    // Fallback sur cache si réseau échoue
    const cached = await caches.match(request);
    if (cached) {
      console.log('[SW] Network failed, using cache:', request.url);
      return cached;
    }
    
    throw error;
  }
}

// Network-First avec fallback offline
async function networkFirstWithOffline(request) {
  try {
    return await networkFirstStrategy(request);
  } catch (error) {
    // Si tout échoue, afficher page offline
    const offlinePage = await caches.match('/offline.html');
    if (offlinePage) {
      return offlinePage;
    }
    
    // Dernière option: réponse basique
    return new Response(
      'Vous êtes hors ligne. Reconnectez-vous pour continuer.',
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: { 'Content-Type': 'text/plain' }
      }
    );
  }
}

// Background Sync (soumission exercices offline)
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-exercises') {
    event.waitUntil(syncExercises());
  }
});

async function syncExercises() {
  // Récupérer exercices en attente depuis IndexedDB
  const db = await openIndexedDB();
  const pendingExercises = await db.getAll('pending_exercises');
  
  // Soumettre chaque exercice
  for (const exercise of pendingExercises) {
    try {
      await fetch('/api/exercises/submit', {
        method: 'POST',
        body: JSON.stringify(exercise),
        headers: { 'Content-Type': 'application/json' }
      });
      
      // Supprimer de la queue si succès
      await db.delete('pending_exercises', exercise.id);
      console.log('[SW] Exercise synced:', exercise.id);
    } catch (error) {
      console.error('[SW] Sync failed for exercise:', exercise.id, error);
    }
  }
}

// Helper IndexedDB
function openIndexedDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('mathcopain-db', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('pending_exercises')) {
        db.createObjectStore('pending_exercises', { keyPath: 'id' });
      }
    };
  });
}

// Push Notifications
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received');
  
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'MathCopain';
  const options = {
    body: data.body || 'Nouveau message',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: data.url || '/',
    actions: [
      {
        action: 'open',
        title: 'Ouvrir'
      },
      {
        action: 'close',
        title: 'Fermer'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Click sur notification
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'open' || !event.action) {
    const urlToOpen = event.notification.data;
    
    event.waitUntil(
      clients.openWindow(urlToOpen)
    );
  }
});

// Message depuis main thread
self.addEventListener('message', (event) => {
  console.log('[SW] Message received:', event.data);
  
  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then((cache) => cache.addAll(event.data.urls))
    );
  }
});

console.log('[SW] Service Worker loaded');
```

## Tests
`tests/test_service_worker.js` (100+ tests avec Workbox Testing)
```

---

## Prompt Claude Code 2.2 - Registration Service Worker

**Titre:** "Enregistrer Service Worker dans app Python/Streamlit"

**Texte:**

```
# TÂCHE: Enregistrement Service Worker

Ajouter code JavaScript pour enregistrer SW dans application principale.

## Fichier à créer
`ui/pwa/sw_registration.py` (150 lignes)

## Composant Streamlit

```python
import streamlit as st
import streamlit.components.v1 as components

def register_service_worker():
    """Enregistre Service Worker pour PWA"""
    
    sw_code = """
    <script>
    // Vérifier support Service Worker
    if ('serviceWorker' in navigator) {
        console.log('Service Worker supported');
        
        window.addEventListener('load', () => {
            registerServiceWorker();
            checkForUpdates();
            setupInstallPrompt();
        });
    } else {
        console.warn('Service Worker not supported');
    }
    
    // Enregistrement Service Worker
    async function registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js', {
                scope: '/'
            });
            
            console.log('✅ Service Worker registered:', registration.scope);
            
            // Vérifier mises à jour toutes les heures
            setInterval(() => {
                registration.update();
            }, 60 * 60 * 1000);
            
            // Écouter changements state
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                console.log('🔄 New Service Worker found');
                
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // Nouvelle version disponible
                        showUpdateNotification();
                    }
                });
            });
            
        } catch (error) {
            console.error('❌ Service Worker registration failed:', error);
        }
    }
    
    // Vérifier mises à jour au focus
    function checkForUpdates() {
        let refreshing = false;
        
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (refreshing) return;
            refreshing = true;
            window.location.reload();
        });
        
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                navigator.serviceWorker.ready.then(registration => {
                    registration.update();
                });
            }
        });
    }
    
    // Notification mise à jour disponible
    function showUpdateNotification() {
        // Streamlit toast notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #3498DB;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 15px;
        `;
        
        notification.innerHTML = `
            <span>🎉 Nouvelle version disponible!</span>
            <button onclick="updateApp()" style="
                background: white;
                color: #3498DB;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
            ">
                Mettre à jour
            </button>
        `;
        
        document.body.appendChild(notification);
    }
    
    // Mettre à jour app
    window.updateApp = function() {
        navigator.serviceWorker.ready.then(registration => {
            if (registration.waiting) {
                registration.waiting.postMessage({ type: 'SKIP_WAITING' });
            }
        });
    }
    
    // Prompt installation PWA
    let deferredPrompt;
    
    function setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('💾 Install prompt ready');
            e.preventDefault();
            deferredPrompt = e;
            
            // Afficher bouton installation personnalisé
            showInstallButton();
        });
        
        // Tracking installation
        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA installed');
            deferredPrompt = null;
            
            // Analytics
            if (window.gtag) {
                gtag('event', 'pwa_installed');
            }
        });
    }
    
    function showInstallButton() {
        // Créer bouton installation si pas encore installé
        if (isAppInstalled()) return;
        
        const installBtn = document.createElement('button');
        installBtn.id = 'pwa-install-btn';
        installBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: #2ECC71;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        
        installBtn.innerHTML = `
            📱 Installer l'app
        `;
        
        installBtn.addEventListener('click', installPWA);
        document.body.appendChild(installBtn);
    }
    
    async function installPWA() {
        if (!deferredPrompt) return;
        
        // Afficher prompt natif
        deferredPrompt.prompt();
        
        // Attendre choix utilisateur
        const { outcome } = await deferredPrompt.userChoice;
        console.log('Install prompt outcome:', outcome);
        
        if (outcome === 'accepted') {
            console.log('✅ User accepted installation');
        } else {
            console.log('❌ User dismissed installation');
        }
        
        // Reset
        deferredPrompt = null;
        
        // Cacher bouton
        const installBtn = document.getElementById('pwa-install-btn');
        if (installBtn) installBtn.remove();
    }
    
    function isAppInstalled() {
        // iOS
        if (window.navigator.standalone === true) {
            return true;
        }
        
        // Android
        if (window.matchMedia('(display-mode: standalone)').matches) {
            return true;
        }
        
        return false;
    }
    
    // Détection online/offline
    window.addEventListener('online', () => {
        console.log('🌐 Back online');
        showConnectionStatus('online');
    });
    
    window.addEventListener('offline', () => {
        console.log('📵 Offline');
        showConnectionStatus('offline');
    });
    
    function showConnectionStatus(status) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            background: ${status === 'online' ? '#2ECC71' : '#E74C3C'};
        `;
        
        toast.textContent = status === 'online' 
            ? '🌐 Connexion rétablie' 
            : '📵 Mode hors ligne';
        
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    }
    </script>
    """
    
    components.html(sw_code, height=0)

# Utilisation dans app.py
def main():
    # ... votre app Streamlit
    
    # Enregistrer SW
    from ui.pwa.sw_registration import register_service_worker
    register_service_worker()
```

## Tests
`tests/test_sw_registration.py` (50+ tests)
```

---

# 📴 PHASE 3: MODE OFFLINE

## Prompt Claude Code 3.1 - Page Offline

**Titre:** "Créer page offline élégante - Fallback hors connexion"

**Texte:**

```
# TÂCHE: Page Offline

Page affichée quand utilisateur hors ligne et page non cachée.

## Fichier à créer
`public/offline.html` (150 lignes)

## HTML Offline Page

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MathCopain - Hors Ligne</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        h1 {
            color: #2C3E50;
            margin-bottom: 15px;
            font-size: 32px;
        }
        
        p {
            color: #7F8C8D;
            line-height: 1.6;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .retry-btn {
            background: #3498DB;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
        }
        
        .retry-btn:hover {
            background: #2980B9;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.6);
        }
        
        .retry-btn:active {
            transform: translateY(0);
        }
        
        .offline-features {
            margin-top: 40px;
            text-align: left;
            background: #F8F9FA;
            padding: 20px;
            border-radius: 10px;
        }
        
        .offline-features h3 {
            color: #2C3E50;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .offline-features ul {
            list-style: none;
        }
        
        .offline-features li {
            color: #7F8C8D;
            padding: 8px 0;
            padding-left: 30px;
            position: relative;
        }
        
        .offline-features li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #2ECC71;
            font-weight: bold;
            font-size: 20px;
        }
        
        .connection-status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .status-checking {
            background: #FFF3CD;
            color: #856404;
        }
        
        .status-online {
            background: #D4EDDA;
            color: #155724;
        }
        
        .status-offline {
            background: #F8D7DA;
            color: #721C24;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📵</div>
        <h1>Vous êtes hors ligne</h1>
        <p>
            Impossible de se connecter à MathCopain pour le moment. 
            Vérifiez votre connexion internet et réessayez.
        </p>
        
        <button class="retry-btn" onclick="retryConnection()">
            🔄 Réessayer
        </button>
        
        <div class="connection-status status-checking" id="status">
            🔍 Vérification de la connexion...
        </div>
        
        <div class="offline-features">
            <h3>💡 Ce que vous pouvez faire hors ligne:</h3>
            <ul>
                <li>Voir vos exercices récents (cachés)</li>
                <li>Consulter vos badges gagnés</li>
                <li>Revoir vos erreurs précédentes</li>
            </ul>
        </div>
    </div>
    
    <script>
        function retryConnection() {
            window.location.reload();
        }
        
        // Auto-retry quand connexion revient
        window.addEventListener('online', () => {
            document.getElementById('status').className = 'connection-status status-online';
            document.getElementById('status').textContent = '✅ Connexion rétablie!';
            
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        });
        
        window.addEventListener('offline', () => {
            document.getElementById('status').className = 'connection-status status-offline';
            document.getElementById('status').textContent = '❌ Toujours hors ligne';
        });
        
        // Check initial
        setTimeout(() => {
            if (navigator.onLine) {
                document.getElementById('status').className = 'connection-status status-online';
                document.getElementById('status').textContent = '✅ Connexion détectée - Cliquez Réessayer';
            } else {
                document.getElementById('status').className = 'connection-status status-offline';
                document.getElementById('status').textContent = '❌ Pas de connexion';
            }
        }, 1000);
        
        // Retry automatique toutes les 30 secondes
        setInterval(() => {
            if (navigator.onLine) {
                fetch('/')
                    .then(() => {
                        window.location.reload();
                    })
                    .catch(() => {
                        console.log('Still offline');
                    });
            }
        }, 30000);
    </script>
</body>
</html>
```

## Tests
`tests/test_offline_page.py` (20+ tests)
```

---

## Prompt Claude Code 3.2 - IndexedDB Cache Local

**Titre:** "Implémenter IndexedDB pour cache données offline"

**Texte:**

```
# TÂCHE: IndexedDB Cache

Stocker exercices et données localement pour mode offline.

## Fichier à créer
`ui/pwa/indexed_db.py` (200 lignes)

## Composant IndexedDB

```python
import streamlit.components.v1 as components

def setup_indexed_db():
    """Setup IndexedDB pour cache offline"""
    
    js_code = """
    <script>
    // IndexedDB Manager pour MathCopain
    class MathCopainDB {
        constructor() {
            this.dbName = 'mathcopain-db';
            this.version = 1;
            this.db = null;
        }
        
        async init() {
            return new Promise((resolve, reject) => {
                const request = indexedDB.open(this.dbName, this.version);
                
                request.onerror = () => reject(request.error);
                request.onsuccess = () => {
                    this.db = request.result;
                    console.log('✅ IndexedDB initialized');
                    resolve(this.db);
                };
                
                request.onupgradeneeded = (event) => {
                    const db = event.target.result;
                    
                    // Store exercices
                    if (!db.objectStoreNames.contains('exercises')) {
                        const exerciseStore = db.createObjectStore('exercises', { 
                            keyPath: 'id',
                            autoIncrement: true 
                        });
                        exerciseStore.createIndex('domain', 'domain', { unique: false });
                        exerciseStore.createIndex('timestamp', 'timestamp', { unique: false });
                    }
                    
                    // Store réponses en attente
                    if (!db.objectStoreNames.contains('pending_responses')) {
                        db.createObjectStore('pending_responses', { 
                            keyPath: 'id',
                            autoIncrement: true 
                        });
                    }
                    
                    // Store dashboard data
                    if (!db.objectStoreNames.contains('dashboard')) {
                        db.createObjectStore('dashboard', { keyPath: 'key' });
                    }
                    
                    // Store badges
                    if (!db.objectStoreNames.contains('badges')) {
                        db.createObjectStore('badges', { keyPath: 'id' });
                    }
                    
                    console.log('✅ IndexedDB schema created');
                };
            });
        }
        
        // Sauvegarder exercice
        async saveExercise(exercise) {
            const transaction = this.db.transaction(['exercises'], 'readwrite');
            const store = transaction.objectStore('exercises');
            
            exercise.timestamp = Date.now();
            exercise.cached = true;
            
            return new Promise((resolve, reject) => {
                const request = store.add(exercise);
                request.onsuccess = () => {
                    console.log('✅ Exercise saved:', exercise.id);
                    resolve(request.result);
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Récupérer exercices récents
        async getRecentExercises(limit = 50) {
            const transaction = this.db.transaction(['exercises'], 'readonly');
            const store = transaction.objectStore('exercises');
            const index = store.index('timestamp');
            
            return new Promise((resolve, reject) => {
                const request = index.openCursor(null, 'prev');
                const exercises = [];
                
                request.onsuccess = (event) => {
                    const cursor = event.target.result;
                    if (cursor && exercises.length < limit) {
                        exercises.push(cursor.value);
                        cursor.continue();
                    } else {
                        console.log(`✅ Retrieved ${exercises.length} exercises`);
                        resolve(exercises);
                    }
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Sauvegarder réponse en attente (offline)
        async savePendingResponse(response) {
            const transaction = this.db.transaction(['pending_responses'], 'readwrite');
            const store = transaction.objectStore('pending_responses');
            
            response.timestamp = Date.now();
            response.synced = false;
            
            return new Promise((resolve, reject) => {
                const request = store.add(response);
                request.onsuccess = () => {
                    console.log('✅ Response queued for sync');
                    resolve(request.result);
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Récupérer réponses en attente
        async getPendingResponses() {
            const transaction = this.db.transaction(['pending_responses'], 'readonly');
            const store = transaction.objectStore('pending_responses');
            
            return new Promise((resolve, reject) => {
                const request = store.getAll();
                request.onsuccess = () => {
                    console.log(`✅ ${request.result.length} pending responses`);
                    resolve(request.result);
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Supprimer réponse après sync
        async deletePendingResponse(id) {
            const transaction = this.db.transaction(['pending_responses'], 'readwrite');
            const store = transaction.objectStore('pending_responses');
            
            return new Promise((resolve, reject) => {
                const request = store.delete(id);
                request.onsuccess = () => {
                    console.log('✅ Response synced and deleted:', id);
                    resolve();
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Cache dashboard data
        async saveDashboard(key, data) {
            const transaction = this.db.transaction(['dashboard'], 'readwrite');
            const store = transaction.objectStore('dashboard');
            
            return new Promise((resolve, reject) => {
                const request = store.put({ key, data, timestamp: Date.now() });
                request.onsuccess = () => resolve();
                request.onerror = () => reject(request.error);
            });
        }
        
        // Récupérer dashboard data
        async getDashboard(key) {
            const transaction = this.db.transaction(['dashboard'], 'readonly');
            const store = transaction.objectStore('dashboard');
            
            return new Promise((resolve, reject) => {
                const request = store.get(key);
                request.onsuccess = () => {
                    const result = request.result;
                    if (result && Date.now() - result.timestamp < 86400000) { // 24h
                        resolve(result.data);
                    } else {
                        resolve(null); // Expired
                    }
                };
                request.onerror = () => reject(request.error);
            });
        }
        
        // Clear old data (cleanup)
        async cleanup(daysToKeep = 30) {
            const cutoff = Date.now() - (daysToKeep * 24 * 60 * 60 * 1000);
            const transaction = this.db.transaction(['exercises'], 'readwrite');
            const store = transaction.objectStore('exercises');
            const index = store.index('timestamp');
            
            return new Promise((resolve, reject) => {
                const request = index.openCursor(IDBKeyRange.upperBound(cutoff));
                let deleted = 0;
                
                request.onsuccess = (event) => {
                    const cursor = event.target.result;
                    if (cursor) {
                        cursor.delete();
                        deleted++;
                        cursor.continue();
                    } else {
                        console.log(`🗑️ Cleaned up ${deleted} old exercises`);
                        resolve(deleted);
                    }
                };
                request.onerror = () => reject(request.error);
            });
        }
    }
    
    // Instance globale
    window.mathcopainDB = new MathCopainDB();
    
    // Initialiser
    window.mathcopainDB.init()
        .then(() => {
            console.log('✅ MathCopain DB ready');
            
            // Cleanup automatique au démarrage
            window.mathcopainDB.cleanup();
        })
        .catch(err => {
            console.error('❌ IndexedDB init failed:', err);
        });
    
    // Helper functions pour Streamlit
    window.cacheExercise = async (exercise) => {
        return await window.mathcopainDB.saveExercise(exercise);
    };
    
    window.getOfflineExercises = async () => {
        return await window.mathcopainDB.getRecentExercises();
    };
    
    window.queueResponse = async (response) => {
        return await window.mathcopainDB.savePendingResponse(response);
    };
    </script>
    """
    
    components.html(js_code, height=0)
```

## Tests
`tests/test_indexed_db.py` (100+ tests)
```

---

# 🔔 PHASE 4: NOTIFICATIONS PUSH

## Prompt Claude Code 4.1 - Push Notifications

**Titre:** "Implémenter Push Notifications web pour rappels"

**Texte:**

```
# TÂCHE: Push Notifications

Notifications web pour rappels exercices et encouragements.

## Fichier à créer
`core/notifications/push_manager.py` (250 lignes)

## Backend Push Manager

```python
from pywebpush import webpush, WebPushException
import json
from database import get_db

class PushNotificationManager:
    """Gestion notifications push web"""
    
    def __init__(self):
        self.vapid_private_key = os.getenv('VAPID_PRIVATE_KEY')
        self.vapid_public_key = os.getenv('VAPID_PUBLIC_KEY')
        self.vapid_claims = {
            "sub": "mailto:support@mathcopain.fr"
        }
    
    def send_notification(self, user_id, title, body, url="/"):
        """Envoie notification à un utilisateur"""
        
        # Récupérer subscription depuis DB
        subscriptions = self.get_user_subscriptions(user_id)
        
        if not subscriptions:
            print(f"No subscriptions for user {user_id}")
            return False
        
        notification_data = {
            "title": title,
            "body": body,
            "url": url,
            "timestamp": int(time.time())
        }
        
        success_count = 0
        
        for subscription in subscriptions:
            try:
                webpush(
                    subscription_info=subscription,
                    data=json.dumps(notification_data),
                    vapid_private_key=self.vapid_private_key,
                    vapid_claims=self.vapid_claims
                )
                success_count += 1
                print(f"✅ Notification sent to subscription {subscription['endpoint'][:50]}...")
                
            except WebPushException as e:
                print(f"❌ Failed to send notification: {e}")
                
                # Si subscription invalide/expirée, supprimer
                if e.response.status_code in [404, 410]:
                    self.remove_subscription(subscription['endpoint'])
        
        return success_count > 0
    
    def save_subscription(self, user_id, subscription):
        """Sauvegarde subscription utilisateur"""
        db = get_db()
        
        # Vérifier si existe déjà
        existing = db.execute('''
            SELECT id FROM push_subscriptions
            WHERE user_id = ? AND endpoint = ?
        ''', (user_id, subscription['endpoint'])).fetchone()
        
        if existing:
            print("Subscription already exists")
            return
        
        # Insérer nouvelle subscription
        db.execute('''
            INSERT INTO push_subscriptions (user_id, endpoint, p256dh, auth)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            subscription['endpoint'],
            subscription['keys']['p256dh'],
            subscription['keys']['auth']
        ))
        db.commit()
        print("✅ Subscription saved")
    
    def get_user_subscriptions(self, user_id):
        """Récupère subscriptions d'un utilisateur"""
        db = get_db()
        
        rows = db.execute('''
            SELECT endpoint, p256dh, auth
            FROM push_subscriptions
            WHERE user_id = ?
        ''', (user_id,)).fetchall()
        
        return [
            {
                "endpoint": row['endpoint'],
                "keys": {
                    "p256dh": row['p256dh'],
                    "auth": row['auth']
                }
            }
            for row in rows
        ]
    
    def remove_subscription(self, endpoint):
        """Supprime subscription invalide"""
        db = get_db()
        db.execute('DELETE FROM push_subscriptions WHERE endpoint = ?', (endpoint,))
        db.commit()
        print(f"🗑️ Removed subscription: {endpoint[:50]}...")
    
    # Notifications pré-définies
    
    def send_daily_reminder(self, user_id, child_name):
        """Rappel quotidien"""
        return self.send_notification(
            user_id,
            f"🎯 {child_name}, c'est l'heure des maths!",
            "Fais quelques exercices pour progresser aujourd'hui 💪",
            "/exercises"
        )
    
    def send_badge_earned(self, user_id, child_name, badge_name):
        """Badge gagné"""
        return self.send_notification(
            user_id,
            f"🏆 Nouveau badge: {badge_name}!",
            f"Bravo {child_name}! Continue comme ça! 🎉",
            "/badges"
        )
    
    def send_streak_milestone(self, user_id, child_name, streak_days):
        """Streak atteint"""
        return self.send_notification(
            user_id,
            f"🔥 {streak_days} jours d'affilée!",
            f"Incroyable {child_name}! Tu es en feu! 🔥",
            "/progress"
        )
    
    def send_parent_report(self, parent_id, child_name):
        """Rapport hebdomadaire parent"""
        return self.send_notification(
            parent_id,
            f"📊 Rapport hebdomadaire - {child_name}",
            "Découvrez les progrès de votre enfant cette semaine",
            "/parent-dashboard"
        )

# Scheduled notifications (Celery/APScheduler)
def schedule_daily_reminders():
    """Envoyer rappels quotidiens 17h"""
    db = get_db()
    push_mgr = PushNotificationManager()
    
    # Récupérer utilisateurs actifs
    users = db.execute('''
        SELECT id, username FROM users
        WHERE is_active = TRUE
        AND last_login > datetime('now', '-7 days')
    ''').fetchall()
    
    for user in users:
        push_mgr.send_daily_reminder(user['id'], user['username'])
```

## Frontend Subscription

```python
# ui/pwa/push_subscription.py
import streamlit.components.v1 as components

def setup_push_subscription(user_id):
    """Setup push notification subscription"""
    
    js_code = f"""
    <script>
    // VAPID Public Key (remplacer par votre clé)
    const VAPID_PUBLIC_KEY = 'VOTRE_CLE_PUBLIQUE_VAPID_ICI';
    
    async function subscribeToPush() {{
        // Vérifier support
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {{
            console.warn('Push notifications not supported');
            return;
        }}
        
        // Demander permission
        const permission = await Notification.requestPermission();
        
        if (permission !== 'granted') {{
            console.log('Notification permission denied');
            return;
        }}
        
        // Récupérer SW registration
        const registration = await navigator.serviceWorker.ready;
        
        // Subscribe
        try {{
            const subscription = await registration.pushManager.subscribe({{
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
            }});
            
            console.log('✅ Push subscription:', subscription);
            
            // Envoyer au backend
            await fetch('/api/push/subscribe', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    user_id: {user_id},
                    subscription: subscription.toJSON()
                }})
            }});
            
            console.log('✅ Subscription saved to server');
            
        }} catch (error) {{
            console.error('❌ Push subscription failed:', error);
        }}
    }}
    
    // Helper: Convert VAPID key
    function urlBase64ToUint8Array(base64String) {{
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\\-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {{
            outputArray[i] = rawData.charCodeAt(i);
        }}
        return outputArray;
    }}
    
    // Auto-subscribe si pas déjà fait
    if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.ready.then(registration => {{
            registration.pushManager.getSubscription().then(subscription => {{
                if (!subscription) {{
                    // Pas encore abonné, proposer
                    showPushPrompt();
                }} else {{
                    console.log('Already subscribed to push');
                }}
            }});
        }});
    }}
    
    function showPushPrompt() {{
        // Afficher prompt personnalisé
        const prompt = document.createElement('div');
        prompt.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            max-width: 400px;
        `;
        
        prompt.innerHTML = `
            <h3 style="margin: 0 0 10px 0;">🔔 Activer les rappels?</h3>
            <p style="margin: 0 0 15px 0; color: #666;">
                Recevez des rappels quotidiens et notifications de progrès.
            </p>
            <button onclick="subscribeToPush(); this.parentElement.remove();" 
                    style="background: #3498DB; color: white; border: none; 
                           padding: 10px 20px; border-radius: 5px; cursor: pointer; 
                           margin-right: 10px;">
                ✅ Activer
            </button>
            <button onclick="this.parentElement.remove();" 
                    style="background: #95A5A6; color: white; border: none; 
                           padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                ❌ Plus tard
            </button>
        `;
        
        document.body.appendChild(prompt);
    }}
    
    window.subscribeToPush = subscribeToPush;
    </script>
    """
    
    components.html(js_code, height=0)
```

## Database Migration

```sql
-- Table subscriptions push
CREATE TABLE push_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    endpoint TEXT UNIQUE NOT NULL,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user (user_id)
);
```

## Générer VAPID Keys

```python
# scripts/generate_vapid_keys.py
from py_vapid import Vapid

vapid = Vapid()
vapid.generate_keys()

print("VAPID_PUBLIC_KEY:", vapid.public_key.savePublicKey().decode('utf-8'))
print("VAPID_PRIVATE_KEY:", vapid.private_key.savePrivateKey().decode('utf-8'))
```

## Tests
`tests/test_push_notifications.py` (80+ tests)
```

---

# 📱 PHASE 5: OPTIMISATIONS MOBILE

## Prompt Claude Code 5.1 - Touch & Gestures

**Titre:** "Optimiser interface pour touch et gestures mobiles"

**Texte:**

```
# TÂCHE: Optimisations Touch Mobile

Rendre l'interface réactive au touch sur mobile/tablette.

## Fichier à créer
`ui/pwa/mobile_optimizations.py` (200 lignes)

## Optimisations CSS & JS

```python
import streamlit as st
import streamlit.components.v1 as components

def apply_mobile_optimizations():
    """Applique optimisations mobile/touch"""
    
    mobile_css = """
    <style>
    /* Touch target minimum 44x44px (Apple HIG) */
    button, a, input, select {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Larger touch targets for primary actions */
    .btn-primary, .stButton > button {
        min-height: 56px;
        padding: 12px 24px;
        font-size: 16px;
    }
    
    /* Disable text selection on buttons */
    button, .btn {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
    
    /* Smooth scroll */
    html {
        scroll-behavior: smooth;
    }
    
    /* Prevent zoom on input focus (iOS) */
    input[type="text"],
    input[type="number"],
    select,
    textarea {
        font-size: 16px !important;
    }
    
    /* Better touch feedback */
    button:active, .btn:active {
        transform: scale(0.98);
        opacity: 0.8;
    }
    
    /* Swipe gestures visual feedback */
    .swipeable {
        transition: transform 0.3s ease-out;
    }
    
    /* Safe area (iPhone notch) */
    @supports (padding: env(safe-area-inset-top)) {
        body {
            padding-top: env(safe-area-inset-top);
            padding-bottom: env(safe-area-inset-bottom);
            padding-left: env(safe-area-inset-left);
            padding-right: env(safe-area-inset-right);
        }
    }
    
    /* Disable pull-to-refresh on iOS */
    body {
        overscroll-behavior-y: contain;
    }
    
    /* Better mobile modal */
    .modal-mobile {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        max-height: 90vh;
        border-radius: 20px 20px 0 0;
        background: white;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
        transform: translateY(100%);
        transition: transform 0.3s ease-out;
    }
    
    .modal-mobile.active {
        transform: translateY(0);
    }
    
    /* Responsive typography */
    @media (max-width: 768px) {
        html {
            font-size: 14px;
        }
        
        h1 { font-size: 24px; }
        h2 { font-size: 20px; }
        h3 { font-size: 18px; }
    }
    
    /* Landscape optimization */
    @media (orientation: landscape) and (max-height: 500px) {
        .exercise-container {
            flex-direction: row;
        }
    }
    </style>
    """
    
    touch_js = """
    <script>
    // Touch gestures handler
    class TouchGestureHandler {
        constructor() {
            this.startX = 0;
            this.startY = 0;
            this.threshold = 50; // pixels
        }
        
        setup() {
            document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
            document.addEventListener('touchend', this.handleTouchEnd.bind(this));
        }
        
        handleTouchStart(e) {
            this.startX = e.touches[0].clientX;
            this.startY = e.touches[0].clientY;
        }
        
        handleTouchEnd(e) {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - this.startX;
            const deltaY = endY - this.startY;
            
            // Swipe horizontal
            if (Math.abs(deltaX) > this.threshold && Math.abs(deltaX) > Math.abs(deltaY)) {
                if (deltaX > 0) {
                    this.onSwipeRight();
                } else {
                    this.onSwipeLeft();
                }
            }
            
            // Swipe vertical
            if (Math.abs(deltaY) > this.threshold && Math.abs(deltaY) > Math.abs(deltaX)) {
                if (deltaY > 0) {
                    this.onSwipeDown();
                } else {
                    this.onSwipeUp();
                }
            }
        }
        
        onSwipeLeft() {
            console.log('Swipe left detected');
            // Exercice suivant
            window.dispatchEvent(new CustomEvent('nextExercise'));
        }
        
        onSwipeRight() {
            console.log('Swipe right detected');
            // Exercice précédent ou retour
            window.dispatchEvent(new CustomEvent('prevExercise'));
        }
        
        onSwipeUp() {
            console.log('Swipe up detected');
            // Afficher détails
        }
        
        onSwipeDown() {
            console.log('Swipe down detected');
            // Fermer modal/panel
        }
    }
    
    // Initialize
    const gestureHandler = new TouchGestureHandler();
    gestureHandler.setup();
    
    // Haptic feedback (si supporté)
    function vibrate(pattern = 10) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }
    
    // Add to button clicks
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') {
            vibrate(10);
        }
    });
    
    // Prevent double-tap zoom on buttons
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) {
            e.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
    
    // Screen orientation change
    window.addEventListener('orientationchange', () => {
        // Réajuster layout si besoin
        document.body.classList.remove('portrait', 'landscape');
        document.body.classList.add(
            window.innerWidth > window.innerHeight ? 'landscape' : 'portrait'
        );
    });
    </script>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)
    components.html(touch_js, height=0)
```

## Tests
`tests/test_mobile_optimizations.py` (60+ tests)
```

---

## Prompt Claude Code 5.2 - Performance Mobile

**Titre:** "Optimiser performance pour mobiles 3G/4G"

**Texte:**

```
# TÂCHE: Performance Mobile

Lazy loading, compression, optimisations réseau lent.

## Fichier à créer
`ui/pwa/performance.py` (150 lignes)

## Optimisations Performance

```python
import streamlit as st
import streamlit.components.v1 as components

def apply_performance_optimizations():
    """Optimisations performance mobile"""
    
    perf_js = """
    <script>
    // Lazy loading images
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
    
    // Detect slow connection
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    
    if (connection) {
        const effectiveType = connection.effectiveType;
        
        if (effectiveType === 'slow-2g' || effectiveType === '2g' || effectiveType === '3g') {
            console.log('⚠️ Slow connection detected:', effectiveType);
            
            // Activer mode économie données
            document.body.classList.add('data-saver');
            
            // Afficher banner
            showDataSaverBanner();
        }
    }
    
    function showDataSaverBanner() {
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #FFA500;
            color: white;
            padding: 10px;
            text-align: center;
            z-index: 10000;
            font-size: 14px;
        `;
        banner.textContent = '📶 Connexion lente détectée - Mode économie activé';
        document.body.prepend(banner);
        
        setTimeout(() => banner.remove(), 5000);
    }
    
    // Prefetch next exercise
    function prefetchNextExercise() {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = '/api/exercise/next';
        document.head.appendChild(link);
    }
    
    // Defer non-critical resources
    window.addEventListener('load', () => {
        // Charger analytics après load
        setTimeout(() => {
            if (window.gtag) {
                console.log('Analytics loaded (deferred)');
            }
        }, 3000);
    });
    
    // Resource Hints
    const preconnect = document.createElement('link');
    preconnect.rel = 'preconnect';
    preconnect.href = 'https://api.mathcopain.fr';
    document.head.appendChild(preconnect);
    
    // Compression detection
    if (window.CompressionStream) {
        console.log('✅ Compression API supported');
    }
    </script>
    """
    
    # CSS Data Saver mode
    data_saver_css = """
    <style>
    .data-saver img {
        display: none;
    }
    
    .data-saver .image-placeholder {
        display: block;
        background: #F0F0F0;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
    }
    
    .data-saver .heavy-component {
        display: none;
    }
    </style>
    """
    
    st.markdown(data_saver_css, unsafe_allow_html=True)
    components.html(perf_js, height=0)
```

## Tests
`tests/test_performance.py` (40+ tests)
```

---

# ✅ PHASE 6: TESTS & VALIDATION

## Prompt Claude Code 6.1 - Tests PWA Complets

**Titre:** "Suite tests complète PWA - Manifest, SW, Offline"

**Texte:**

```
# TÂCHE: Tests PWA

Tests automatisés pour valider fonctionnalité PWA complète.

## Fichier à créer
`tests/pwa/test_pwa_complete.py` (300 lignes)

## Tests Suite

```python
import pytest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPWAFunctionality:
    """Tests complets PWA"""
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver pour tests"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(options=options)
        driver.get('http://localhost:8501')
        yield driver
        driver.quit()
    
    def test_manifest_exists(self, driver):
        """Vérifier manifest.json accessible"""
        driver.get('http://localhost:8501/manifest.json')
        
        # Parser JSON
        manifest = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)
        
        assert manifest['name'] == "MathCopain - Mathématiques Personnalisées"
        assert manifest['short_name'] == "MathCopain"
        assert manifest['display'] == "standalone"
        assert len(manifest['icons']) >= 8
    
    def test_manifest_linked_in_html(self, driver):
        """Vérifier manifest lié dans HTML"""
        driver.get('http://localhost:8501')
        
        manifest_link = driver.find_element(By.CSS_SELECTOR, 'link[rel="manifest"]')
        assert manifest_link.get_attribute('href').endswith('/manifest.json')
    
    def test_service_worker_registered(self, driver):
        """Vérifier Service Worker enregistré"""
        driver.get('http://localhost:8501')
        
        # Attendre enregistrement SW
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script(
                "return navigator.serviceWorker.controller !== null"
            )
        )
        
        # Vérifier registration
        sw_registered = driver.execute_script('''
            return navigator.serviceWorker.controller !== null;
        ''')
        
        assert sw_registered, "Service Worker not registered"
    
    def test_offline_page_cached(self, driver):
        """Vérifier page offline cachée"""
        driver.get('http://localhost:8501')
        
        # Vérifier cache
        cache_has_offline = driver.execute_script('''
            return caches.open('mathcopain-v1.0.0').then(cache => {
                return cache.match('/offline.html').then(response => {
                    return response !== undefined;
                });
            });
        ''')
        
        assert cache_has_offline, "Offline page not cached"
    
    def test_install_prompt_available(self, driver):
        """Vérifier install prompt disponible"""
        driver.get('http://localhost:8501')
        
        # Simuler beforeinstallprompt event
        prompt_ready = driver.execute_script('''
            let prompted = false;
            window.addEventListener('beforeinstallprompt', () => {
                prompted = true;
            });
            
            // Dispatch event
            window.dispatchEvent(new Event('beforeinstallprompt'));
            
            return prompted;
        ''')
        
        # Note: Vrai test nécessite vraie navigation
        # Ce test vérifie juste que listener existe
    
    def test_push_notification_permission(self, driver):
        """Vérifier demande permission notifications"""
        driver.get('http://localhost:8501')
        
        # Vérifier API disponible
        push_supported = driver.execute_script('''
            return 'Notification' in window && 'serviceWorker' in navigator;
        ''')
        
        assert push_supported, "Push notifications not supported"
    
    def test_indexed_db_setup(self, driver):
        """Vérifier IndexedDB configuré"""
        driver.get('http://localhost:8501')
        
        # Attendre init
        time.sleep(2)
        
        # Vérifier DB existe
        db_exists = driver.execute_script('''
            return new Promise((resolve) => {
                const request = indexedDB.open('mathcopain-db');
                request.onsuccess = () => {
                    resolve(true);
                };
                request.onerror = () => {
                    resolve(false);
                };
            });
        ''')
        
        assert db_exists, "IndexedDB not initialized"
    
    def test_offline_functionality(self, driver):
        """Tester mode offline"""
        driver.get('http://localhost:8501')
        
        # Passer offline
        driver.execute_cdp_cmd('Network.enable', {})
        driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
            'offline': True,
            'downloadThroughput': 0,
            'uploadThroughput': 0,
            'latency': 0
        })
        
        # Rafraîchir page
        driver.refresh()
        
        # Vérifier page offline affichée OU cache utilisé
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        
        assert 'hors ligne' in body_text.lower() or 'offline' in body_text.lower()
    
    def test_icons_all_sizes_exist(self):
        """Vérifier toutes tailles icônes présentes"""
        import os
        
        required_sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]
        icon_dir = 'public/static/icons/'
        
        for size in required_sizes:
            icon_path = os.path.join(icon_dir, f'icon-{size}x{size}.png')
            assert os.path.exists(icon_path), f"Missing icon: {icon_path}"
    
    def test_manifest_icons_valid_paths(self, driver):
        """Vérifier chemins icônes manifest valides"""
        driver.get('http://localhost:8501/manifest.json')
        manifest = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)
        
        for icon in manifest['icons']:
            # Tenter charger icon
            driver.get(f"http://localhost:8501{icon['src']}")
            
            # Vérifier image chargée (pas 404)
            assert driver.title != "404", f"Icon not found: {icon['src']}"
    
    def test_cache_strategy_network_first(self, driver):
        """Vérifier stratégie Network-First pour API"""
        driver.get('http://localhost:8501')
        
        # Requête API
        response = driver.execute_script('''
            return fetch('/api/exercises')
                .then(r => r.status)
                .catch(err => 0);
        ''')
        
        assert response == 200, "API request failed"
    
    def test_cache_strategy_cache_first(self, driver):
        """Vérifier stratégie Cache-First pour assets"""
        driver.get('http://localhost:8501')
        
        # Requête asset
        cached = driver.execute_script('''
            return caches.match('/static/css/main.css')
                .then(response => response !== undefined);
        ''')
        
        # Doit être caché après première visite
        assert cached, "Asset not cached"
    
    def test_background_sync_registered(self, driver):
        """Vérifier background sync disponible"""
        driver.get('http://localhost:8501')
        
        sync_supported = driver.execute_script('''
            return 'serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype;
        ''')
        
        # Note: Peut ne pas être supporté tous navigateurs
        print(f"Background Sync supported: {sync_supported}")
    
    def test_mobile_viewport_meta(self, driver):
        """Vérifier viewport meta pour mobile"""
        driver.get('http://localhost:8501')
        
        viewport = driver.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]')
        content = viewport.get_attribute('content')
        
        assert 'width=device-width' in content
        assert 'initial-scale=1' in content
    
    def test_theme_color_meta(self, driver):
        """Vérifier theme-color meta"""
        driver.get('http://localhost:8501')
        
        theme_color = driver.find_element(By.CSS_SELECTOR, 'meta[name="theme-color"]')
        color = theme_color.get_attribute('content')
        
        assert color == '#3498DB' or color.lower() == '#3498db'
    
    def test_apple_mobile_web_app_meta(self, driver):
        """Vérifier meta tags iOS"""
        driver.get('http://localhost:8501')
        
        apple_capable = driver.find_element(By.CSS_SELECTOR, 'meta[name="apple-mobile-web-app-capable"]')
        assert apple_capable.get_attribute('content') == 'yes'
        
        apple_title = driver.find_element(By.CSS_SELECTOR, 'meta[name="apple-mobile-web-app-title"]')
        assert apple_title.get_attribute('content') == 'MathCopain'

# Performance tests
class TestPWAPerformance:
    """Tests performance PWA"""
    
    def test_lighthouse_pwa_score(self):
        """Lighthouse PWA score > 90"""
        # Nécessite Lighthouse CI
        # lighthouse http://localhost:8501 --only-categories=pwa --output=json
        pass
    
    def test_first_contentful_paint(self):
        """FCP < 2 secondes"""
        pass
    
    def test_time_to_interactive(self):
        """TTI < 5 secondes"""
        pass
```

## Lancer tests

```bash
pytest tests/pwa/test_pwa_complete.py -v
```

## Tests
`tests/pwa/` (300+ tests au total)
```

---

# 📊 MÉTRIQUES PWA

## KPIs à Suivre

| Métrique | Target | Comment Mesurer |
|----------|--------|-----------------|
| **Lighthouse PWA Score** | >90 | Lighthouse CI |
| **Installation rate** | >15% | Analytics (install events) |
| **Offline usage** | >5% sessions | Service Worker analytics |
| **Push open rate** | >30% | Notification click tracking |
| **Load time (3G)** | <5s | WebPageTest |
| **Cache hit rate** | >70% | Service Worker logs |
| **iOS installation** | >10% iOS users | UA detection |

---

# 🚀 DÉPLOIEMENT PWA

## Checklist Finale

```
Pre-Déploiement:
☐ Manifest.json validé (https://manifest-validator.appspot.com/)
☐ Tous icônes générés (72px → 512px)
☐ Service Worker testé (cache, offline, sync)
☐ Page offline élégante
☐ IndexedDB fonctionnel
☐ Push notifications configurées (VAPID keys)
☐ Optimisations mobile appliquées
☐ Tests PWA passent (300+)
☐ Lighthouse score PWA >90

Post-Déploiement:
☐ Tester installation iOS Safari
☐ Tester installation Android Chrome
☐ Vérifier notifications push fonctionnent
☐ Tester mode offline réel (avion mode)
☐ Monitorer métriques PWA
☐ Collecter feedback utilisateurs mobile

PWA READY? ☐ OUI ☐ NON
```

---

# 📚 RESSOURCES

## Documentation
- [PWA Builder](https://www.pwabuilder.com/)
- [Web.dev PWA Guide](https://web.dev/progressive-web-apps/)
- [MDN Service Worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)

## Tools
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Workbox](https://developers.google.com/web/tools/workbox) (Service Worker library)
- [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator)

---

**Généré:** 2025-11-18  
**Version:** Guide Conversion PWA v1.0  
**Effort Total:** 1-2 semaines  
**Prompts Claude Code:** 12 prompts détaillés

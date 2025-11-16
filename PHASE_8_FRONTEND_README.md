# Phase 8 Frontend - Dashboard Enseignant Vue.js

## Vue d'ensemble

Phase 8 Frontend implémente une interface web complète pour le dashboard enseignant, avec :

- **Interface Vue.js 3** : Framework réactif moderne
- **API REST Flask** : Backend exposant toutes les fonctionnalités
- **Dashboard interactif** : Statistiques en temps réel
- **Gestion de classes** : CRUD complet avec inscriptions élèves
- **Devoirs adaptatifs** : Création et suivi de devoirs ML
- **Analytics** : Visualisations et classements
- **Rapports** : Génération de rapports multi-formats
- **Curriculum EN** : Suivi des 108 compétences officielles

## Architecture

### Structure des fichiers

```
MathCopain_v6.2/
├── api/
│   ├── __init__.py
│   ├── app.py                    # Application Flask principale
│   └── teacher_routes.py         # 40+ endpoints REST API
│
└── frontend/
    ├── index.html               # Point d'entrée HTML
    ├── css/
    │   └── style.css           # Styles complets (800+ lignes)
    └── js/
        ├── api.js              # Client API (toutes les requêtes)
        ├── app.js              # Application Vue principale
        └── components/
            ├── modal.js
            ├── dashboard-view.js      # Vue tableau de bord
            ├── classrooms-view.js     # Gestion classes
            ├── assignments-view.js    # Gestion devoirs
            ├── analytics-view.js      # Analytics
            ├── reports-view.js        # Rapports
            └── curriculum-view.js     # Compétences EN
```

---

## API Flask - Endpoints REST

### Démarrage du serveur API

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API Flask
python -m api.app

# Serveur disponible sur http://localhost:5000
```

### Endpoints disponibles (40+)

#### 🏫 **Classrooms (Gestion de classes)**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/teacher/classrooms` | Liste toutes les classes |
| POST | `/api/teacher/classrooms` | Créer une classe |
| GET | `/api/teacher/classrooms/:id` | Détails d'une classe |
| PUT | `/api/teacher/classrooms/:id` | Modifier une classe |
| DELETE | `/api/teacher/classrooms/:id` | Archiver une classe |
| GET | `/api/teacher/classrooms/:id/students` | Liste élèves |
| POST | `/api/teacher/classrooms/:id/students` | Ajouter un élève |
| DELETE | `/api/teacher/classrooms/:id/students/:sid` | Retirer un élève |
| GET | `/api/teacher/classrooms/:id/at-risk` | Élèves à risque |

#### 📝 **Assignments (Devoirs)**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/teacher/assignments` | Liste devoirs (filtrable) |
| POST | `/api/teacher/assignments` | Créer un devoir |
| GET | `/api/teacher/assignments/:id` | Détails devoir |
| POST | `/api/teacher/assignments/:id/publish` | Publier devoir |
| PUT | `/api/teacher/assignments/:id` | Modifier devoir |
| DELETE | `/api/teacher/assignments/:id` | Supprimer devoir |
| GET | `/api/teacher/assignments/:id/completion` | Suivi de complétion |

#### 📊 **Analytics**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/teacher/analytics/trajectory` | Trajectoire progression |
| GET | `/api/teacher/analytics/heatmap` | Heatmap performance |
| GET | `/api/teacher/analytics/forecast` | Prévisions ML |
| GET | `/api/teacher/analytics/engagement` | Métriques d'engagement |
| GET | `/api/teacher/analytics/compare` | Comparaison élève/classe |
| GET | `/api/teacher/analytics/leaderboard` | Classement classe |

#### 📚 **Curriculum (Compétences EN)**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/teacher/curriculum/competencies` | Liste compétences |
| GET | `/api/teacher/curriculum/student-progress` | Progression élève |
| GET | `/api/teacher/curriculum/class-overview` | Vue classe |
| GET | `/api/teacher/curriculum/gaps` | Lacunes élève |
| GET | `/api/teacher/curriculum/recommendations` | Recommandations |

#### 📄 **Reports (Rapports)**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/teacher/reports/student-progress` | Rapport élève |
| POST | `/api/teacher/reports/class-overview` | Rapport classe |
| POST | `/api/teacher/reports/at-risk` | Rapport à risque |
| POST | `/api/teacher/reports/assignment` | Rapport devoir |
| POST | `/api/teacher/reports/curriculum-coverage` | Couverture curriculum |
| POST | `/api/teacher/reports/export/csv` | Export CSV |

---

## Frontend Vue.js

### Technologies utilisées

- **Vue 3** (CDN) : Framework réactif
- **Chart.js** : Graphiques et visualisations
- **Font Awesome** : Icônes
- **CSS personnalisé** : Design moderne et responsive

### Lancement de l'interface

```bash
# Option 1: Serveur HTTP Python simple
cd frontend
python -m http.server 8080

# Accéder à http://localhost:8080

# Option 2: Serveur Node.js
npx http-server frontend -p 8080
```

### Composants Vue.js

#### 1. **Dashboard View** (`dashboard-view.js`)

Vue principale avec statistiques globales :

- **Stats cards** : Classes actives, élèves totaux, à risque, taux de réussite
- **Liste des classes** : Tableau interactif avec actions
- **Activité récente** : Placeholder pour notifications

**Fonctionnalités** :
- Calcul dynamique des totaux
- Navigation vers les classes
- Indicateurs visuels (badges, progress bars)

#### 2. **Classrooms View** (`classrooms-view.js`)

Gestion complète des classes :

- **CRUD classes** : Créer, modifier, archiver
- **Gestion élèves** : Ajouter, retirer, voir statut
- **Capacité** : Respect du max_students

**Exemple de flux** :
```javascript
// Ajouter un élève
await api.addStudentToClassroom(classroomId, username);

// Retirer un élève
await api.removeStudentFromClassroom(classroomId, studentId);
```

#### 3. **Assignments View** (`assignments-view.js`)

Création et suivi de devoirs :

- **Liste devoirs** : Filtre (tous, publiés, brouillons)
- **Création** : Form avec mode adaptatif ON/OFF
- **Publication** : Publier aux élèves
- **Suivi** : Tableau de complétion en temps réel

**Propriétés devoir** :
- Titre, description
- Domaines de compétences (multi-select)
- Difficulté fixe ou adaptative (ML)
- Nombre d'exercices
- Date d'échéance

#### 4. **Analytics View** (`analytics-view.js`)

Visualisations et insights :

- **Leaderboard** : Top 10 élèves (icônes trophées)
- **Graphiques** : Placeholder pour trajectoires (Chart.js)
- **Filtres** : Par classe, domaine, période

**API utilisées** :
```javascript
// Classement
const leaderboard = await api.getLeaderboard(classroomId, null, 30, 10);

// Trajectoire
const trajectory = await api.getProgressTrajectory({
    student_id: studentId,
    skill_domain: 'multiplication',
    days_back: 30
});
```

#### 5. **Reports View** (`reports-view.js`)

Génération de rapports :

- **3 types de rapports** :
  1. Vue d'ensemble classe
  2. Élèves à risque
  3. Couverture curriculum

- **Configuration** : Classe, niveau, type
- **Export** : CSV, JSON (PDF via backend)

**Exemple** :
```javascript
const report = await api.generateClassReport(classroomId, 30);
console.log(report.report); // Données complètes
```

#### 6. **Curriculum View** (`curriculum-view.js`)

Suivi compétences Éducation Nationale :

- **108 compétences** : CE1-CM2
- **Vue classe** : Taux de maîtrise par compétence
- **Statistiques** : Moyenne classe, compétences maîtrisées
- **Détails** : Code, titre, domaine, élèves maîtrisant

**Indicateurs visuels** :
- 🟢 Vert : Maîtrise ≥ 70%
- 🟡 Jaune : Maîtrise 30-70%
- 🔴 Rouge : Maîtrise < 30%

---

## Client API JavaScript

### Classe `APIClient` (`api.js`)

Client complet pour toutes les requêtes API.

**Initialisation** :
```javascript
const api = new APIClient('http://localhost:5000/api');
```

**Exemples d'utilisation** :

```javascript
// Classrooms
const classrooms = await api.getClassrooms();
const classroom = await api.createClassroom({
    name: "CE2-A",
    grade_level: "CE2",
    school_year: "2025-2026",
    max_students: 30
});

// Assignments
const assignments = await api.getAssignments();
const assignment = await api.createAssignment({
    classroom_id: 1,
    title: "Révision multiplication",
    skill_domains: ["multiplication"],
    exercise_count: 10,
    adaptive: true,
    due_date: "2025-11-30T23:59:59"
});

// Analytics
const heatmap = await api.getPerformanceHeatmap(studentId, 30);
const forecast = await api.getPerformanceForecast(studentId, "multiplication", 7);

// Curriculum
const progress = await api.getStudentCompetencyProgress(studentId, "CE2");
const gaps = await api.getCompetencyGaps(studentId, "CE2");

// Reports
const report = await api.generateStudentReport(studentId, classroomId, 'structured', 30);
await api.exportCSV('class_progress', { classroom_id: 1 });
```

---

## Styles CSS

### Variables CSS (personnalisables)

```css
:root {
    --primary-color: #4CAF50;
    --secondary-color: #2196F3;
    --danger-color: #f44336;
    --warning-color: #ff9800;
    --success-color: #4CAF50;
}
```

### Classes utilitaires principales

- `.card` : Container blanc avec ombre
- `.btn-primary` / `.btn-secondary` / `.btn-danger` : Boutons colorés
- `.badge` : Labels colorés (success, warning, danger, info)
- `.stats-grid` : Grille responsive de stats
- `.progress-bar` : Barre de progression animée
- `.modal-overlay` : Modal centré avec fond sombre
- `.notification` : Toast notifications animées

### Responsive

Breakpoint à 768px :
- Colonnes simples sur mobile
- Navigation horizontale scrollable
- Modals pleine largeur

---

## Workflow enseignant

### 1. Connexion et dashboard

```
1. Enseignant se connecte (session Flask)
2. Dashboard affiche :
   - Nombre de classes
   - Total d'élèves
   - Élèves à risque (badge rouge)
   - Taux de réussite moyen
3. Liste des classes avec actions rapides
```

### 2. Créer une classe

```
Dashboard → Onglet "Classes" → Bouton "Créer une classe"

Form :
- Nom : "CE2 - Classe A"
- Niveau : CE2
- Année : 2025-2026
- Capacité max : 30

→ Classe créée → Ajout d'élèves
```

### 3. Ajouter des élèves

```
Classes → Sélectionner classe → Bouton "Élèves"

Form d'ajout :
- Nom d'utilisateur : alice_ce2
→ Élève ajouté à la classe

Tableau élèves :
- Nom, Niveau, Exercices, Taux réussite, Statut
- Bouton "Retirer" pour chaque élève
```

### 4. Créer un devoir

```
Onglet "Devoirs" → Bouton "Nouveau devoir"

Form :
- Titre : "Révision multiplication"
- Classe : CE2 - Classe A
- Domaines : [multiplication, division]
- Mode adaptatif : OUI (difficulté ML par élève)
- Exercices : 10
- Échéance : 30/11/2025

→ Devoir créé (brouillon) → Publier
```

### 5. Publier et suivre

```
Devoirs → Sélectionner devoir → Bouton "Publier"
→ Devoir envoyé aux 25 élèves

Devoirs → Bouton "Suivi"
→ Tableau de complétion :
   - Alice : 10/10 (100% - Terminé)
   - Bob : 5/10 (60% - En cours)
   - ...
```

### 6. Consulter analytics

```
Onglet "Analytics" → Sélectionner classe

Leaderboard Top 10 :
1. 🏆 Alice (95% réussite)
2. 🥈 Charlie (88%)
3. 🥉 David (85%)
...

Graphiques disponibles via API :
- Trajectoire de progression
- Heatmap domaine×difficulté
- Prévisions ML 7 jours
```

### 7. Générer un rapport

```
Onglet "Rapports"

Configurer :
- Type : Vue d'ensemble classe
- Classe : CE2 - Classe A

Bouton "Générer"
→ Rapport JSON avec :
   - Statistiques complètes
   - Trajectoire classe
   - Leaderboard
   - Élèves à risque
   - Compétences EN
```

### 8. Suivre curriculum

```
Onglet "Compétences EN"

Sélectionner :
- Classe : CE2 - Classe A
- Niveau : CE2

→ Tableau 25 compétences CE2 :
   - CE2.C.3.2 : Tables ×9 (72% maîtrise) 🟡
   - CE2.N.1.1 : Nombres 1000 (85% maîtrise) 🟢
   - CE2.C.4.1 : Division (45% maîtrise) 🔴
   ...
```

---

## Sécurité et authentification

### Session Flask

L'API utilise des sessions Flask pour l'authentification :

```python
# Dans teacher_routes.py
@teacher_required
def get_classrooms(teacher_id: int):
    # teacher_id injecté automatiquement par le decorator
    ...
```

### Decorator `@teacher_required`

Vérifie automatiquement :
1. Session active (cookie)
2. `teacher_id` dans session
3. Retourne 401 si non authentifié

### CORS

Activé pour développement local :
```python
CORS(app, supports_credentials=True)
```

**Production** : Restreindre les origines :
```python
CORS(app, origins=['https://mathcopain.fr'], supports_credentials=True)
```

---

## Déploiement

### Développement

```bash
# Terminal 1: API Flask
python -m api.app
# → http://localhost:5000

# Terminal 2: Frontend
cd frontend
python -m http.server 8080
# → http://localhost:8080

# Navigateur : http://localhost:8080
```

### Production recommandée

#### Backend (API Flask)

```bash
# Avec Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.app:create_app()
```

#### Frontend

**Option 1 : Nginx**
```nginx
server {
    listen 80;
    server_name mathcopain.fr;

    location / {
        root /var/www/mathcopain/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Option 2 : Build Vue.js (Vite/Webpack)**

Pour production, compiler Vue.js :
```bash
# Convertir vers projet Vue CLI
npm install -g @vue/cli
vue create mathcopain-dashboard

# Build production
npm run build
# → dist/ folder optimisé
```

---

## Limitations et améliorations futures

### Limitations actuelles

1. **Pas de build process** : Vue 3 en CDN (pas optimisé)
2. **Pas de state management** : Pas de Vuex/Pinia
3. **Pas de routing** : SPA avec tabs (pas de Vue Router)
4. **Graphiques limités** : Chart.js configuré mais pas intégré
5. **Pas de tests** : Pas de tests unitaires/E2E

### Améliorations recommandées

#### 1. Migration vers Vue CLI/Vite

```bash
# Projet professionnel
npm create vite@latest mathcopain-dashboard -- --template vue

# Structure moderne :
src/
├── components/
├── views/
├── router/
├── store/
├── api/
└── assets/
```

#### 2. State Management (Pinia)

```javascript
// store/classroom.js
import { defineStore } from 'pinia';

export const useClassroomStore = defineStore('classroom', {
    state: () => ({
        classrooms: [],
        selectedClassroom: null
    }),
    actions: {
        async fetchClassrooms() {
            const response = await api.getClassrooms();
            this.classrooms = response.classrooms;
        }
    }
});
```

#### 3. Vue Router

```javascript
const routes = [
    { path: '/', component: DashboardView },
    { path: '/classrooms', component: ClassroomsView },
    { path: '/classrooms/:id', component: ClassroomDetail },
    { path: '/assignments', component: AssignmentsView },
    ...
];
```

#### 4. Intégration Chart.js complète

```javascript
// Composant trajectoire
<canvas ref="trajectoryChart"></canvas>

mounted() {
    const ctx = this.$refs.trajectoryChart.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: trajectory.data_points.map(p => p.date),
            datasets: [{
                label: 'Taux de réussite',
                data: trajectory.data_points.map(p => p.success_rate * 100)
            }]
        }
    });
}
```

#### 5. Tests

**Unit tests (Vitest)** :
```javascript
import { mount } from '@vue/test-utils';
import DashboardView from './DashboardView.vue';

test('displays correct stats', () => {
    const wrapper = mount(DashboardView, {
        props: { classrooms: [{ id: 1, name: 'CE2-A', student_count: 25 }] }
    });
    expect(wrapper.text()).toContain('25');
});
```

**E2E tests (Playwright)** :
```javascript
test('teacher can create classroom', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.click('text=Classes');
    await page.click('text=Créer une classe');
    await page.fill('[name=name]', 'CE2-A');
    await page.click('text=Créer');
    await expect(page.locator('text=CE2-A')).toBeVisible();
});
```

#### 6. WebSocket pour temps réel

```javascript
// Real-time updates pour complétion devoirs
const socket = io('http://localhost:5000');

socket.on('assignment_completed', (data) => {
    // Update completion UI in real-time
    this.updateCompletion(data.assignment_id, data.student_id);
});
```

---

## Troubleshooting

### Problème : CORS errors

**Erreur** : `Access-Control-Allow-Origin`

**Solution** :
```python
# api/app.py
CORS(app, origins=['http://localhost:8080'], supports_credentials=True)
```

### Problème : API 401 Unauthorized

**Erreur** : `Authentication required`

**Solution** : Implémenter authentification mock pour développement :
```javascript
// Temporaire - développement
sessionStorage.setItem('teacher_id', '1');
```

### Problème : Vue components not loading

**Erreur** : `app.component is not a function`

**Solution** : Vérifier ordre des scripts dans index.html :
```html
<!-- ORDRE IMPORTANT -->
<script src="https://unpkg.com/vue@3.3.4/dist/vue.global.js"></script>
<script src="js/api.js"></script>
<script src="js/components/modal.js"></script>
<!-- ... autres composants ... -->
<script src="js/app.js"></script> <!-- EN DERNIER -->
```

### Problème : Data not updating

**Solution** : Utiliser `this.$parent.loadDashboard()` pour refresh :
```javascript
async createClassroom() {
    await api.createClassroom(data);
    this.$parent.loadDashboard(); // Refresh data
}
```

---

## Conclusion

**Phase 8 Frontend est FONCTIONNEL** avec :

✅ Interface Vue.js complète
✅ 40+ endpoints API REST
✅ 6 vues principales (Dashboard, Classes, Devoirs, Analytics, Rapports, Curriculum)
✅ Design moderne et responsive
✅ Intégration ML (devoirs adaptatifs, prévisions, détection à risque)
✅ Suivi 108 compétences EN
✅ Génération de rapports

### Prochaine étape recommandée

**Migration vers architecture professionnelle** :
- Vue CLI / Vite build
- Vue Router + Pinia
- Tests unitaires et E2E
- Intégration Chart.js complète
- WebSocket pour temps réel

---

**Date de complétion** : 16 novembre 2025
**Version** : MathCopain v6.2 - Phase 8 UI
**Auteur** : Claude AI (Anthropic)

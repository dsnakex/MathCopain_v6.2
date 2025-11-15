# 🔴 TECHNICAL DEBT - MathCopain v6.2
## Inventaire Détaillé de la Responsabilité Technique

**Objectif :** Traçabilité complète des problèmes techniques. Chaque item = 1 action en v6.3 ou v7.

---

## 🏗️ ARCHITECTURE

### Problème 1 : app.py Monolithique (800+ lignes)

**Sévérité :** 🔴 Critique | **Impact :** Maintenabilité | **Effort :** 6-8h

**Description :**
```python
# Situation actuelle dans app.py:
# - Imports session management
# - Imports sidebar rendering
# - Imports exercice logic
# - Imports skill tracking
# → Tout mélangé, difficile à tester

# Problème: Si on change UI, on risque casser la logique métier
```

**Conséquences :**
- Tests difficiles (trop de dépendances)
- Régressions faciles
- Onboarding lent pour nouveau dev
- Impossible de réutiliser logique dans API

**Solution (v6.3):**
```
app.py (200 lignes)
├── Streamlit UI orchestration
└── Imports depuis:
    ├── core/session_manager.py (logique session)
    ├── core/exercise_manager.py (orchestration exercices)
    ├── ui/sidebar.py (UI sidebar)
    ├── ui/exercices.py (UI exercices)
    └── ui/dashboard.py (UI stats)
```

**Action :** Voir TASK_TRACKER.md, Jour 2 (Refactor)

---

### Problème 2 : Gestion JSON Sans Validation

**Sévérité :** 🟠 Élevée | **Impact :** Fiabilité | **Effort :** 4-5h

**Description :**
```python
# Actuellement:
import json
data = json.load(open('utilisateurs.json'))  # Peut crash silencieusement
data['user']['score'] += 1  # KeyError possible
json.dump(data, open(...))  # Fichier corrompu si crash pendant écriture
```

**Problèmes :**
- Pas de schéma validé
- Corruptions possibles
- Pas de backup automatique
- Migrations données compliquées

**Solution (v6.3):**
```
Créer: core/data_manager.py
├── DataManager class
│   ├── load_user(id) → valide schéma
│   ├── save_user(id, data) → atomic write
│   ├── backup_before_write()
│   └── validate_schema()
├── Schemas JSON validés (pydantic)
└── Error recovery (rollback)
```

**Action :** Jour 11-12 (Sécurité)

---

### Problème 3 : Pas de Logging Structuré

**Sévérité :** 🟠 Élevée | **Impact :** Debugging | **Effort :** 2-3h

**Description :**
```python
# Actuellement:
print("User logged in")  # Où ? Quand exactement ?
try:
    calculate_score()
except:
    pass  # Silence radio, difficile à debug en production
```

**Problèmes :**
- Impossible de tracer bugs utilisateurs
- Errors perdues
- Performance issues invisibles
- Sécurité issues non détectées

**Solution (v6.3):**
```
Créer: core/logger.py
├── Logs structurés (JSON)
├── Niveaux: DEBUG, INFO, WARNING, ERROR
├── Contexte: user_id, timestamp, duration
├── Fichier + console
└── Rotation logs automatique

Exemple:
{
  "timestamp": "2025-11-14T19:15:30Z",
  "level": "ERROR",
  "user_id": "alice_123",
  "event": "exercise_submit",
  "error": "division_by_zero",
  "duration_ms": 245
}
```

**Action :** Jour 9 (Monitoring)

---

## 🔐 SÉCURITÉ

### Problème 4 : PIN Stocké en Plaintext

**Sévérité :** 🔴 CRITIQUE | **Impact :** Données enfants | **Effort :** 3-4h

**Description :**
```json
// utilisateurs_securises.json
{
  "alice": {
    "pin": "1234",  // ❌ EN CLAIR DANS LE FICHIER !
    "nom": "Alice Dupont"
  }
}
```

**Risques :**
- Accès physique PC → tous les PINs compromis
- File leak → données enfants exposées
- Non-conforme RGPD (données enfants)
- Contrainte légale France (données mineurs)

**Solution (v6.3):**
```python
from bcrypt import hashpw, checkpw

# Nouveau format:
{
  "alice": {
    "pin_hash": "$2b$12$...", # Hash bcrypt
    "nom": "Alice",
    "created_at": "2025-11-14T19:00:00Z"
  }
}

# Vérification:
checkpw(input_pin.encode(), stored_hash)  # Retourne bool
```

**Action :** Jour 11 (Sécurité)

---

### Problème 5 : Pas de Limite Tentatives PIN

**Sévérité :** 🟠 Élevée | **Impact :** Brute force | **Effort :** 1-2h

**Description :**
```python
# Actuellement: quelqu'un peut essayer 10000 PINs facilement
# Même un PIN 4 chiffres = 10000 possibilités en seconds
```

**Problèmes :**
- Brute force attacks possibles
- PINs faibles = problématiques
- Pas de détection anomalies

**Solution (v6.3):**
```python
class PinGuardian:
    def check_pin(self, user_id, pin_attempt):
        attempts = self.get_attempts(user_id)
        
        if attempts >= 3:  # Max 3 tentatives
            self.lock_user(user_id, duration_minutes=15)
            log_security_alert(f"Brute force attempt: {user_id}")
            return False
        
        if verify_pin(pin_attempt):
            self.reset_attempts(user_id)
            return True
        else:
            self.increment_attempts(user_id)
            return False
```

**Action :** Jour 11 (Sécurité)

---

### Problème 6 : Pas de Validation Input

**Sévérité :** 🟠 Élevée | **Impact :** Injection attacks | **Effort :** 2-3h

**Description :**
```python
# Actuellement:
user_name = st.text_input("Nom élève")
save_user(user_name)  # ❌ Pas validé!

# Quelqu'un peut entrer:
# "../../../etc/passwd"  # Path traversal
# "'; DROP TABLE users; --"  # SQL injection (futur)
```

**Problèmes :**
- Path traversal possible
- Injection command shells
- Caractères bizarres créent bugs
- Prêt pour problèmes futurs (DB)

**Solution (v6.3):**
```python
from pydantic import BaseModel, validator

class UserProfile(BaseModel):
    name: str  # 1-50 chars, alphanumerique + accents
    email: str  # Format email validé
    grade: str  # Choix limités: CE1, CE2, CM1, CM2

    @validator('name')
    def validate_name(cls, v):
        if not (1 <= len(v) <= 50):
            raise ValueError('Name too long')
        if not v.replace(' ', '').replace('-', '').isalnum():
            raise ValueError('Invalid characters')
        return v.strip()
```

**Action :** Jour 11 (Sécurité)

---

## 🧪 TESTS & QUALITÉ

### Problème 7 : Aucun Test Unitaire

**Sévérité :** 🔴 CRITIQUE | **Impact :** Fiabilité | **Effort :** 15-20h

**Description :**
```python
# 4894 lignes de code sans filet de sécurité
# = Chaque modif risque casser l'existant
# = Impossible de refactorer en confiance
```

**Conséquences :**
- Peur de modifier code existant
- Bugs découverts par utilisateurs
- Régressions fréquentes
- Pas de contrat code (API interface)

**Solution (v6.3):**
```
Target: 80% coverage

Tests prioritaires:
- Corrections d'exercices (faux positifs = frustration)
- Progression niveaux (logic adaptatif)
- Sauvegardes données (perte = catastrophe)
- Authentification (sécurité)

Voir: TASK_TRACKER.md (Semaine 1 & 2)
```

**Action :** Jour 1-9 (Tests Semaine 1-2)

---

### Problème 8 : Pas de CI/CD

**Sévérité :** 🟠 Élevée | **Impact :** Qualité | **Effort :** 5-6h

**Description :**
```
# Actuellement:
# Developer ← testé manuellement? ← commitment
# = Dépend du dev d'être consciencieux
# = Facile d'oublier un test
```

**Problèmes :**
- Tests oubliés avant push
- Lint inconsistant
- Breaking changes accidentels
- Pas d'historique builds

**Solution (v6.3):**
```yaml
# .github/workflows/tests.yml
- Trigger: Chaque push/PR
- Run: tests (pytest)
- Run: linting (flake8, pylint)
- Calcul: coverage report
- Bloquer: coverage < 80%
- Status: Visible dans PRs
```

**Action :** Jour 6-7 (CI/CD)

---

## 📊 PERFORMANCE

### Problème 9 : Pas de Cache Utilisateur

**Sévérité :** 🟡 Moyen | **Impact :** Vitesse | **Effort :** 2-3h

**Description :**
```python
# Actuellement: charger utilisateur = lecture JSON à chaque fois
# 100 élèves × 10 lectures/jour = 1000 I/O fichier!
# Plus utilisateurs = plus lent

# Streamlit redéploie app à chaque interaction
# → Recharger utilisateur à chaque clic = LENT
```

**Problèmes :**
- App lente avec beaucoup d'élèves
- I/O disk pas nécessaire
- Scalabilité faible

**Solution (v6.3):**
```python
@st.cache_resource  # Cache Streamlit
def get_user_cache(user_id):
    # Cache en mémoire
    # Invalide si fichier change
    return load_user(user_id)

# Ou meilleur: @st.session_state
st.session_state.user = load_user_once(user_id)
# Persiste pendant session utilisateur
```

**Action :** Jour 2 (Refactor app.py)

---

### Problème 10 : Calculs Exercices Pas Optimisés

**Sévérité :** 🟡 Moyen | **Impact :** Performance | **Effort :** 2-3h

**Description :**
```python
# Générer exercice = recalcul à chaque affichage
# Problème avec générateurs infinis?
```

**Solution (v6.3):**
```python
# Cache/Memoization:
@functools.lru_cache(maxsize=1000)
def generate_exercice(difficulty, type):
    # Résultat en cache
    return exercice

# Ou pré-générer batch:
exercises_batch = [generate_exercice(...) for i in range(50)]
```

**Action :** Jour 3-4 (Tests)

---

## 📝 DOCUMENTATION

### Problème 11 : Documentation Technique Manquante

**Sévérité :** 🟡 Moyen | **Impact :** Maintenabilité | **Effort :** 3-4h

**Description :**
```
README.md = 30 lignes
├─ Aucune doc architecture
├─ Aucun diagramme flux
├─ Aucune API documentation
├─ Aucun setup dev guide
└─ = Nouveau dev perd 2-3h à comprendre
```

**Conséquences :**
- Onboarding lent
- Refactoring risqué (incompréhension)
- Maintenance difficile
- Knowledge silos

**Solution (v6.3):**
```
docs/
├── ARCHITECTURE.md (structure modules, flux)
├── API.md (docstrings + exemples)
├── CONTRIBUTING.md (setup dev, git workflow)
└── DEPLOYMENT.md (install, config production)
```

**Action :** Jour 5 (Docs Semaine 1) + Jour 13-14 (Docs Semaine 3)

---

### Problème 12 : Pas de CHANGELOG

**Sévérité :** 🟡 Moyen | **Impact :** Traçabilité | **Effort :** 1h

**Description :**
```
Impossible de savoir quoi a changé entre versions
= Difficile debugger "ça marche avant, pas maintenant"
```

**Solution (v6.3):**
```
CHANGELOG.md
├── v6.3.0 (2025-11-22)
│   ├── ✨ Added: Tests 80% coverage
│   ├── 🔒 Security: PIN hashing
│   ├── 🐛 Fixed: Exercise validation
│   └── 📚 Docs: Full API documentation
└── v6.2.0 (2025-10-15)
    └── ... (ancient history)
```

**Action :** Jour 15 (Release)

---

## 🗂️ CODE ORGANIZATION

### Problème 13 : Fichiers JSON Sans Schéma

**Sévérité :** 🟠 Élevée | **Impact :** Fiabilité | **Effort :** 4-5h

**Description :**
```python
# Actuellement: 3 fichiers JSON différents
- utilisateurs.json
- utilisateurs_securises.json
- users_data.json
- users_credentials.json
= Confus! Quelle est la source de vérité?
```

**Problèmes :**
- Duplication données
- Incohérences possibles
- Migration difficile

**Solution (v6.3):**
```
data/
├── users/
│   ├── alice_123.json  # Profil complet 1 user
│   ├── bob_456.json
│   └── ...
├── schema.json  # Validation Pydantic
└── migrations/  # Versioning changements
```

**Action :** Jour 11 (Sécurité)

---

### Problème 14 : Imports Circulaires Possibles

**Sévérité :** 🟡 Moyen | **Impact :** Maintenance | **Effort :** 2-3h

**Description :**
```python
# app.py imports adaptive_system
# adaptive_system imports skill_tracker
# skill_tracker imports app?? → Circular import bug!
```

**Solution (v6.3):**
```
Créer interface claire:
├── core/ (no imports from UI)
│   ├── __init__.py (exports public API)
│   ├── exercise_generator.py
│   ├── adaptive_system.py
│   └── skill_tracker.py
├── ui/ (imports only from core)
│   ├── __init__.py
│   ├── sidebar.py
│   └── exercises.py
└── app.py (orchestrator, imports both)
```

**Action :** Jour 2 (Refactor)

---

## 📋 RÉSUMÉ PRIORISATION

| # | Problème | Sévérité | v6.3 | v7 |
|---|----------|----------|------|-----|
| 1 | app.py monolithique | 🔴 | ✅ | - |
| 2 | JSON sans validation | 🟠 | ✅ | - |
| 3 | Pas de logging | 🟠 | ✅ | - |
| 4 | PIN plaintext | 🔴 | ✅ | - |
| 5 | No rate limiting | 🟠 | ✅ | - |
| 6 | No input validation | 🟠 | ✅ | - |
| 7 | Pas de tests | 🔴 | ✅ | - |
| 8 | Pas de CI/CD | 🟠 | ✅ | - |
| 9 | Pas de cache | 🟡 | ✅ | - |
| 10 | Performance exercices | 🟡 | ✅ | - |
| 11 | Docs manquante | 🟡 | ✅ | - |
| 12 | Pas de CHANGELOG | 🟡 | ✅ | - |
| 13 | JSON désorganisé | 🟠 | ✅ | - |
| 14 | Imports circulaires | 🟡 | ✅ | - |

**Total effort v6.3:** 50-60 heures
**Status:** Tous addressés dans 3 semaines ✅

---

## 🎯 Pour v7 (Futur)

```
[ ] Migration PostgreSQL (JSON → DB)
[ ] API REST (FastAPI ou Flask)
[ ] Multi-utilisateurs serveur (vs local JSON)
[ ] Dashboard admin web
[ ] Mobile app (React Native)
[ ] Analytics avancées
[ ] Export rapports PDF
```

---

**Dernière mise à jour :** 2025-11-14 | **Statut :** Baseline v6.2

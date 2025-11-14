# 📋 DECISIONS LOG - MathCopain v6.2 → v6.3
## Journal des Décisions Architecturales & Stratégiques

**Format :** Chaque décision importante est tracée ici.  
**Usage :** Comprendre le "pourquoi", éviter de re-débattre, historique pour v7.

---

## DÉCISION 1 : Stratégie v6.3 = Stabilité (pas features)

**Date :** 2025-11-14  
**Décideur :** Team  
**Impactée :** Toutes futures décisions  
**Status :** ✅ Approuvée

### Contexte
```
v6.2 = 4894 lignes sans tests ni CI/CD
= Fragile, risqué, impossible à refactorer

Options considérées:
A) Ajouter features (AI, mobile, API)
B) Stabiliser base de code en priorité ← CHOISIE
C) Hybrid (50/50 features/stabilité)
```

### Décision
**v6.3 = Production Hardening (3 semaines)**
- Phase 1 (S1) : Tests 80% coverage + refactor critical
- Phase 2 (S2) : CI/CD + monitoring
- Phase 3 (S3) : Sécurité + documentation

**Pas de:**
- ❌ Nouvelles features exercices
- ❌ Changements UI
- ❌ Intégration API externes
- ✅ Mais : Préparation architecture pour API v7

### Justification
| Aspect | Avant (v6.2) | Après (v6.3) |
|--------|------|----------|
| Risque crash | Élevé | Minimal |
| Confiance élèves | Moyenne | Haute |
| Maintenabilité | Difficile | Facile |
| Prêt prod | Non | Oui |
| Fondations v7 | Absentes | Présentes |

### Conséquences
- ✅ Utilisateurs auront app stable
- ✅ Code renable pour futurs devs
- ✅ Peut monter en prod confiance
- ⚠️ Features attendront v7 (acceptable)

---

## DÉCISION 2 : Tests = Priorité #1

**Date :** 2025-11-14  
**Décideur :** Architecture team  
**Impactée :** Semaine 1-2  
**Status :** ✅ Approuvée

### Contexte
```
Risk: 4894 lignes sans tests = 1 bug change tout
Options:
A) Refactor puis tests
B) Tests d'abord (foundation) ← CHOISIE
C) Simultané (confus)
```

### Décision
**Ordre:** Tests → Refactor (pas inverse)

Pourquoi?
- Tests = contrat code (API interface)
- Refactor utilise tests comme filet sécurité
- Tests révèlent problèmes dès départ
- Coverage = gauge santé code

### Structure Tests
```
Priorité 1 (critiques pour enfants):
├─ Corrections exercices (faux positif = frustration)
├─ Progression niveaux (adapter difficulté)
└─ Sauvegardes données (perte = catastrophe)

Priorité 2 (systèmes complexes):
├─ Adaptive system (logic)
├─ Skill tracker (stats)
└─ Auth (sécurité)

Priorité 3 (utilitaires):
├─ Monnaie, mesures, décimaux
└─ Utils divers
```

### Target
- S1 fin: 45-50% coverage
- S2 fin: 80%+ coverage
- Toutes criticals tests passent

---

## DÉCISION 3 : Refactor app.py via Séparation Concerns

**Date :** 2025-11-14  
**Décideur :** Architecture  
**Impactée :** Structure projet  
**Status :** ✅ Approuvée

### Contexte
```
app.py = 800 lignes (trop!)
├─ UI logic (Streamlit)
├─ Business logic (exercices, scoring)
├─ Data management (JSON)
└─ Session management
= Impossible à tester isolé

Options:
A) Laisser monolithique (risqué)
B) Séparer strict (core/ vs ui/) ← CHOISIE
C) Micro-services (trop pour v6.3)
```

### Décision
**Architecture cible:**
```
MathCopain_v6.3/
├── app.py (200 lignes - orchestration)
├── requirements.txt
├── core/                     # 0 imports UI
│   ├── __init__.py
│   ├── exercise_generator.py
│   ├── adaptive_system.py
│   ├── skill_tracker.py
│   ├── data_manager.py
│   ├── authenticator.py
│   └── logger.py
├── ui/                       # Imports uniquement core/
│   ├── __init__.py
│   ├── sidebar.py
│   ├── exercise_view.py
│   ├── dashboard_view.py
│   └── utils.py
├── security/
│   ├── __init__.py
│   ├── encryption.py
│   ├── validators.py
│   └── pin_guard.py
├── tests/
│   ├── __init__.py
│   ├── test_*.py
│   └── conftest.py
└── docs/
    ├── ARCHITECTURE.md
    ├── API.md
    └── DEPLOYMENT.md
```

### Import Rules (à respecter)
```
Allowed:
- app.py imports core/ + ui/
- ui/ imports core/
- core/ imports core/ (mais pas ui/)
- tests/ import everything

Forbidden:
- core/ imports ui/ (∞ circular!)
- ui/ imports ui/ (cross-module)
```

### Bénéfices
- ✅ Tests faciles (core/ = fonction pure)
- ✅ Reuse core/ dans future API v7
- ✅ UI changes ≠ logic breaks
- ✅ Onboarding facile (structure claire)

---

## DÉCISION 4 : Chiffrer PINs avec bcrypt

**Date :** 2025-11-14  
**Décideur :** Sécurité  
**Impactée :** Auth + données  
**Status :** ✅ Approuvée

### Contexte
```
Actuel: PINs stockés plaintext dans JSON
= Données enfants exposées
= RGPD violation France
= Risque légal

Options:
A) Laisser plaintext (dangereux!)
B) MD5 simple (rapide mais faible)
C) bcrypt (lent par design = sûr) ← CHOISIE
D) Argon2 (meilleur, mais overkill v6.3)
```

### Décision
**Utiliser bcrypt pour PINs:**

```python
from bcrypt import hashpw, checkpw

# Au création compte:
pin_hash = hashpw(pin_input.encode(), gensalt(rounds=12))
save_to_json(user_id, pin_hash)

# À connexion:
if checkpw(pin_input.encode(), stored_hash):
    ✅ Login success
else:
    ❌ Login fail
```

### Migration v6.2 → v6.3
```
Script migration:
- Lire ancien utilisateurs_securises.json (plaintext)
- Hash chaque PIN
- Sauvegarder nouveau format
- Delete ancien (manuel par admin)
```

### Timeline
- Jour 11 (Lundi): Implement bcrypt
- Tests: vérifier backward compat migration
- Déploiement: v6.3.0 release

### Compliance
- ✅ RGPD compliant (hashing)
- ✅ CNIL recommandations
- ✅ France data protection
- ✅ Enfants data sécurisées

---

## DÉCISION 5 : CI/CD avec GitHub Actions

**Date :** 2025-11-14  
**Décideur :** DevOps  
**Impactée :** Deploy workflow  
**Status :** ✅ Approuvée

### Contexte
```
Actuellement: Tests manuels (dépend dev conscience)
Options:
A) Mantenir manuel (risqué)
B) Jenkins (complexe, overkill)
C) GitHub Actions (simple, gratuit) ← CHOISIE
D) GitLab CI (alternative OK)
```

### Décision
**Pipeline GitHub Actions (S2 Jour 6-7):**

```yaml
# .github/workflows/tests.yml
name: Tests & Quality

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: pytest --cov=./ --cov-report=xml
      - uses: codecov/codecov-action@v3
      - run: flake8 . --statistics
      - run: pylint core/ ui/
```

### Badges dans README
```markdown
![Tests](https://github.com/dsnakex/MathCopain_v6.3/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/dsnakex/MathCopain_v6.3/branch/main/graph/badge.svg)](...)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
```

### Benefits
- ✅ Tests auto sur chaque push
- ✅ PRs bloquées si tests fail
- ✅ Coverage tracking
- ✅ Historique builds conservé
- ✅ Gratuit (GitHub public)

---

## DÉCISION 6 : Format Données = Fichiers JSON Individuels

**Date :** 2025-11-14  
**Décideur :** Data architecture  
**Impactée :** Stockage  
**Status :** ✅ Approuvée (v6.3), Migration v7 possible

### Contexte
```
Actuellement: Mélange 4 fichiers JSON
- utilisateurs.json
- utilisateurs_securises.json
- users_data.json
- users_credentials.json
= Confus, duplication, incohérences

Options:
A) Consolidate en 1 fichier (single point failure)
B) 1 fichier par user (atomicity) ← CHOISIE v6.3
C) PostgreSQL (trop pour v6.3, fait en v7)
```

### Décision
**v6.3 = Structure préparatoire v7:**

```
data/
├── users/
│   ├── alice_123.json     # 1 profil complet
│   ├── bob_456.json
│   └── charlie_789.json
├── schema.json            # Pydantic validation
├── migrations/
│   ├── 001_initial.md     # Historique changements
│   └── 002_bcrypt_pins.md
└── backups/
    ├── 2025-11-14_backup.tar.gz
    └── 2025-11-15_backup.tar.gz
```

### Format 1 User (alice_123.json)
```json
{
  "metadata": {
    "user_id": "alice_123",
    "created_at": "2025-11-01T10:30:00Z",
    "last_login": "2025-11-14T19:00:00Z",
    "version": 1
  },
  "profile": {
    "nom": "Alice Dupont",
    "prenom": "Alice",
    "grade": "CM2",
    "email": "alice@ecole.fr"
  },
  "security": {
    "pin_hash": "$2b$12$...",
    "pin_attempts": 0,
    "locked_until": null
  },
  "skills": {
    "addition": {"score": 850, "level": 3},
    "subtraction": {"score": 720, "level": 2}
  }
}
```

### Bénéfices
- ✅ Atomicity (1 user = 1 fichier)
- ✅ Facile à backer
- ✅ Préparation DB (1 doc = 1 row future)
- ✅ Scalable (ajouter users = juste ajouter fichiers)

### Migration v7
```
Quand v7 = API + PostgreSQL:
SELECT * FROM users WHERE user_id = 'alice_123'
= Équivalent alice_123.json
```

---

## DÉCISION 7 : Documentation = Priorité S3

**Date :** 2025-11-14  
**Décideur :** Product  
**Impactée :** Jour 5 & 13-14  
**Status :** ✅ Approuvée

### Contexte
```
Docs actuelles: Minimales (30 lignes README)
Impact: Nouveau dev = 2-3h onboarding

Timing:
A) Docs en parallèle (slow)
B) Docs après code (oubliés)
C) Docs pendant S1-S3 (slots spécifiques) ← CHOISIE
```

### Décision
**Schedule docs = intégré à roadmap:**

| Quand | Quoi | Effort |
|-------|------|--------|
| S1 J5 | Architecture + API overview | 2h |
| S2 J10 | Contributing guide | 1h |
| S3 J13 | Installation + Admin guide | 2h |
| S3 J14 | Deployment + v7 blueprint | 2h |
| S3 J15 | Final polish + CHANGELOG | 1h |

### Docs à créer
1. **docs/ARCHITECTURE.md** (8h total)
   - Module overview
   - Data flow diagrams
   - Security model
   - Scalability discussion

2. **docs/API.md**
   - Core module exports
   - Function signatures
   - Usage examples
   - Error handling

3. **CONTRIBUTING.md**
   - Developer setup
   - Git workflow
   - Code style
   - PR checklist

4. **docs/DEPLOYMENT.md**
   - Installation steps
   - Configuration
   - Troubleshooting
   - Performance tuning

5. **docs/v7_ROADMAP.md**
   - API design (FastAPI)
   - DB schema (PostgreSQL)
   - Architecture cloud
   - Timeline 6 mois

---

## DÉCISION 8 : Pas de Changements UX en v6.3

**Date :** 2025-11-14  
**Décideur :** Product  
**Impactée :** Scope constraints  
**Status :** ✅ Approuvée

### Contexte
```
Tentation: "Pendant qu'on refactor, on redesign UI?"
= Scope creep = v6.3 ne finish pas

Décision: Strict focus v6.3 = stabilité
```

### What's OUT of v6.3
- ❌ UI/UX redesign
- ❌ Nouvelles icônes/couleurs
- ❌ Mobile optimization
- ❌ Dark mode
- ❌ New exercises types

### What's OK
- ✅ Bug fixes (UX bugs)
- ✅ Performance UX (load time)
- ✅ Accessibility (WCAG)
- ✅ Mobile responsiveness (existing)

### Timing
**All UI/UX features → v7 roadmap**
- Vision: Community-driven design
- Timeline: Après v6.3.0 release stable
- Budget: Separate project

---

## DÉCISION 9 : Version Numbering = Semantic Versioning

**Date :** 2025-11-14  
**Décideur :** Release management  
**Impactée :** Tags, CHANGELOG  
**Status :** ✅ Approuvée

### Format
```
MAJOR.MINOR.PATCH

6.3.0 = Release v6.3
├─ 6.3.1 = Hotfix (security patch)
├─ 6.3.2 = Another bugfix
└─ 6.4.0 = Minor feature (next)

Tagging:
git tag -a v6.3.0 -m "Production ready"
git push --tags
```

### Timeline
```
2025-11-22: v6.3.0 (initial release)
2025-11-25: v6.3.1 (if critical bugs)
2025-12-15: v6.3.2 (further stabilization)
2026-01-15: v6.4.0 (minor features)
2026-Q2: v7.0.0 (major API redesign)
```

---

## DÉCISION 10 : Backup Strategy

**Date :** 2025-11-14  
**Décideur :** Operations  
**Impactée :** Data loss prevention  
**Status :** ✅ Approuvée

### Automatique (v6.3)
- Daily backup (cron job)
- Compress + timestamp
- Local storage (separate disk si possible)

### Manuel (Admin)
- Export on demand (CLI script)
- Restore from backup (CLI script)
- Verification (integrity check)

### À Implementer (S3 J14)
```python
# scripts/backup.py
def backup_users():
    timestamp = datetime.now().isoformat()
    backup_file = f"backups/backup_{timestamp}.tar.gz"
    shutil.make_archive(...)
    print(f"✅ Backed up to {backup_file}")

# scripts/restore.py
def restore_from_backup(backup_file):
    extract(backup_file, "data/")
    validate_schema()
    print(f"✅ Restored from {backup_file}")
```

### Disaster Recovery
- Corruption detected → restore from backup
- User deletion request → anonymize + archive
- Migration to v7 → export full dataset

---

## SUMMARY TABLE

| # | Décision | Date | Status | Impact |
|---|----------|------|--------|--------|
| 1 | v6.3 = Stabilité | 2025-11-14 | ✅ | Scope |
| 2 | Tests priorité #1 | 2025-11-14 | ✅ | Architecture |
| 3 | Refactor app.py | 2025-11-14 | ✅ | Structure |
| 4 | bcrypt PINs | 2025-11-14 | ✅ | Sécurité |
| 5 | GitHub Actions | 2025-11-14 | ✅ | DevOps |
| 6 | JSON per user | 2025-11-14 | ✅ | Data |
| 7 | Docs scheduled | 2025-11-14 | ✅ | Timeline |
| 8 | No UX changes | 2025-11-14 | ✅ | Constraints |
| 9 | Semver versioning | 2025-11-14 | ✅ | Release |
| 10 | Backup strategy | 2025-11-14 | ✅ | Operations |

---

**Next Review:** Fin S1 (2025-11-22) pour feedback + ajustements éventuels

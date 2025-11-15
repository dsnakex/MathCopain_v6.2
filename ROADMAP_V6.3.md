# 🗺️ ROADMAP MathCopain v6.3
## Vision 3 Semaines - Stabilité & Scalabilité

**Objectif Global :** Transformer MathCopain d'un prototype en application **production-ready**, avec une base de code maintenable et des fondations solides pour les évolutions futures.

---

## 📊 Vue d'ensemble stratégique

### État Actuel (v6.2)
- ✅ 4894 lignes de code Python
- ✅ 13 modules fonctionnels
- ✅ Système adaptatif + suivi des compétences
- ✅ 7+ types d'exercices différents
- ⚠️ **SANS tests unitaires** (point critique)
- ⚠️ Pas de CI/CD
- ⚠️ Gestion JSON brute (vulnérable)
- ⚠️ Documentation technique insuffisante

### Cible (v6.3)
- ✅ Tests unitaires complets (>80% coverage)
- ✅ Pipeline CI/CD automatisé
- ✅ Architecture clarifée et documentée
- ✅ Prêt pour production sécurisée
- ✅ Bases pour v7 (API, multi-utilisateurs)

---

## 🥇 Priorités Semaine par Semaine

### **SEMAINE 1 : Stabilité & Fondations**
*Durée estimée : 15-18h*

#### 1️⃣ Tests Unitaires - Phase 1 (7-8h)
**Impact pédagogique :** ⭐⭐⭐⭐⭐ | **Effort :** Moyen

**Raison :** Tu es à 4894 lignes SANS filet de sécurité. Les bugs peuvent frustrer les élèves et casser leur confiance.

**À faire :**
```
tests/
├── __init__.py
├── test_exercices_utils.py       # Additions, soustractions, multiplications
├── test_division_utils.py        # Division + reste
├── test_monnaie_utils.py         # Euros, centimes
├── test_mesures_utils.py         # Longueurs, masses, volumes
├── test_decimaux_utils.py        # Nombres décimaux
├── test_adaptive_system.py       # Logique de progression
├── test_skill_tracker.py         # Suivi compétences
└── test_utilisateur.py           # Cache utilisateur, PIN
```

**Cas critiques à tester :**
- Corrections d'exercices (éviter faux positifs)
- Calculs avec reste et décimales
- Progression de niveau (adaptation difficulté)
- Sauvegarde/chargement données utilisateur

#### 2️⃣ Refactorisation Critique (6-7h)
**Impact :** ⭐⭐⭐⭐ | **Effort :** Moyen-Élevé

**Zones problématiques identifiées :**
1. **app.py** (~800 lignes) → Trop de responsabilités
   - Séparer logique métier / UI
   - Créer `core/session_manager.py`
   - Créer `ui/sidebar.py`, `ui/exercices.py`

2. **utilisateur.py** → Intégrer cache + PIN
   - Consolidation avec authentification.py
   - Réduire duplication code

3. **Nommage inconsistant**
   - `utilisateurs.json` vs `users_data.json` vs `users_credentials.json`
   - Standardiser : `data/users/` + fichiers nommés explicitement

#### 3️⃣ Documentation Technique Minimale (1-2h)
- Architecture overview (`docs/ARCHITECTURE.md`)
- Guide API modules (`docs/API.md`)
- Setup développeur (`CONTRIBUTING.md`)

**Livrable :** ✅ Tests passants + Code refactorisé + Docs techniques

---

### **SEMAINE 2 : Automatisation & Qualité**
*Durée estimée : 12-15h*

#### 4️⃣ CI/CD Pipeline (8-10h)
**Impact :** ⭐⭐⭐⭐⭐ | **Effort :** Moyen

**À mettre en place :**

1. **GitHub Actions** (`.github/workflows/`)
   ```yaml
   - Tests automatiques (Python 3.9+)
   - Linting (pylint, flake8)
   - Coverage report (pytest-cov, > 80%)
   - Requirements.txt validation
   ```

2. **Badges + Status** dans README
   - Build status
   - Coverage percentage
   - Python version

3. **Pre-commit hooks**
   - Format code (black)
   - Import sorting (isort)
   - Basic linting

#### 5️⃣ Couverture de Tests (4-5h)
**Augmenter coverage :** 20% → 80%+

- Tester les chemins d'erreur
- Edge cases exercices (division par zéro, etc.)
- Tests d'intégration (workflow complet)

#### 6️⃣ Logging & Monitoring (2-3h)
**Améliorer l'observabilité :**
- Logs structurés (fichier + console)
- Suivi erreurs (traceback propres)
- Dashboard performance (optional)

**Livrable :** ✅ Pipeline CI/CD fonctionnel + Tests >80% coverage

---

### **SEMAINE 3 : Sécurité & Préparation Production**
*Durée estimée : 10-12h*

#### 7️⃣ Sécurité Données (5-6h)
**Impact :** ⭐⭐⭐⭐⭐ | **Effort :** Élevé

**À faire :**
1. **Encryption données utilisateur**
   - PIN → hash sécurisé (bcrypt)
   - Données élèves → chiffrement (cryptography)
   - Backup sécurisé

2. **Validation input**
   - Sanitizer les noms, emails
   - Vérifier types données
   - Rate limiting PIN (max 3 tentatives)

3. **Audit sécurité**
   - Dépendances Python (safety check)
   - Secrets dans .env (pas en dur)
   - Permissions fichiers restrictives

#### 8️⃣ Documentation Utilisateur (3-4h)
**Pour déploiement :**
- Installation + configuration
- Gestion utilisateurs (ajouter/supprimer élèves)
- Troubleshooting
- Backup/restore données

#### 9️⃣ Préparation v7 (2-3h)
**Fondations futures :**
- Architecture pour API REST (blueprint)
- Structure multi-utilisateurs serveur (doc)
- Migration vers base de données (plan)

**Livrable :** ✅ Application sécurisée + Documentation complète + Roadmap v7

---

## 📈 Métriques de Succès

| Métrique | v6.2 | v6.3 Target | Impact |
|----------|------|-------------|--------|
| Tests Coverage | 0% | >80% | 🔒 Stabilité |
| Modules testés | 0 | 8+ | 🛡️ Fiabilité |
| Documentation | 20% | 90% | 📚 Maintenabilité |
| Bugs bloquants | Variable | 0 | 😊 Expérience élève |
| Temps onboarding dev | ∞ | <2h | 🚀 Scalabilité |

---

## 🎯 Stratégie Implémentation

### Approche par Domaine (pas par Layer)

**Pourquoi :** Éviter des merges conflictuels, avoir du code fonctionnel à chaque étape.

**Ordre recommandé :**
1. `exercices_utils.py` → tests complets
2. `adaptive_system.py` → tests
3. `skill_tracker.py` → tests
4. `utilisateur.py` + `authentification.py` → fusion + tests
5. `app.py` → refactor + tests
6. Intégration globale

### Git Workflow

```bash
# Branche pour v6.3
git checkout -b develop/v6.3

# Par domaine
git checkout -b feature/tests-exercices
git checkout -b feature/tests-adaptive
git checkout -b feature/ci-cd
...

# Merge à chaque étape complète
git merge feature/... (en develop)
```

---

## 🚨 Risques & Mitigation

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|-----------|
| Tests trop lents | Moyen | Bloquage CI/CD | Parallelization pytest |
| Régressions bugs | Élevée | Frustration élèves | Tests + review stricts |
| Dépendances rompues | Faible | Crash démarrage | Pinning versions + tests |
| Données corrompues | Faible | 😱 Catastrophe | Backup automatique |

---

## 📅 Timeline Réaliste

```
Semaine 1 : Lu-Ve (15-18h)
  ├─ L-M : Tests (4h/jour)
  ├─ M-J : Refactor (3-4h/jour)
  └─ V   : Docs + Review (2h)

Semaine 2 : Lu-Ve (12-15h)
  ├─ L-M : CI/CD setup (4-5h/jour)
  ├─ J-V : Coverage (3-4h/jour)
  └─ V   : Monitoring (2h)

Semaine 3 : Lu-V (10-12h)
  ├─ L-M : Sécurité (3-4h/jour)
  ├─ J   : User docs (2-3h)
  └─ V   : v7 blueprint (2-3h)
```

**Total estimé :** 37-45h de travail

---

## 📌 Notes Importantes

- **Pas de changements UX en v6.3** → Focus stabilité
- **Backward compatible** → Données v6.2 restent valides
- **À laisser pour v7** : Redesign UI, API REST, multi-utilisateurs serveur
- **Validations hebdomadaires** recommandées avec utilisateurs tests

---

## 🎓 Prochaines étapes

1. ✅ Valider cette roadmap
2. ⏭️ Créer `TASK_TRACKER.md` (checklist jour par jour)
3. ⏭️ Générer `CLAUDE_CODE_BRIEFING.md` (pour Claude Code)
4. ⏭️ Lancer Semaine 1 ! 🚀

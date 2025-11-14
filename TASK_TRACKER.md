# ✅ TASK TRACKER - MathCopain v6.3
## Checklist Jour par Jour - 3 Semaines

**Format :** Cochez les cases au fur et à mesure. Chaque tâche est un commit Git.

---

## 📅 SEMAINE 1 : Stabilité & Fondations

### **JOUR 1 & 2 (Lundi-Mardi) : Tests Unitaires - Exercices**

#### Jour 1 - Setup Tests

```
[ ] Créer dossier: tests/
[ ] Créer: tests/__init__.py
[ ] Créer: tests/conftest.py (fixtures pytest)
[ ] Installer: pip install pytest pytest-cov
[ ] Ajouter à requirements.txt:
    pytest==7.4.3
    pytest-cov==4.1.0
[ ] Test de config: pytest --version
[ ] Créer: .github/workflows/ (structure)
```

**Commit :** `feat: setup pytest infrastructure`

#### Jour 2 - Tests Addition/Soustraction

```
[ ] Créer: tests/test_exercices_utils.py
[ ] Écrire tests pour: generate_addition()
    [ ] Cas normal (1-100)
    [ ] Limites (0, 100)
    [ ] Générateur infini
[ ] Écrire tests pour: verify_addition()
    [ ] Réponses correctes ✓
    [ ] Réponses incorrectes ✗
    [ ] Formats différents (int, str)
[ ] Écrire tests pour: generate_soustraction()
    [ ] Résultats positifs
    [ ] Résultats zéro
    [ ] Ordre aléatoire
[ ] Lancer: pytest tests/test_exercices_utils.py -v
[ ] Coverage: pytest --cov=exercices_utils tests/
```

**Commit :** `test: add addition/subtraction unit tests`

---

### **JOUR 3 & 4 (Mercredi-Jeudi) : Tests Divisions & Monnaie**

#### Jour 3 - Tests Division

```
[ ] Créer: tests/test_division_utils.py
[ ] Tests division sans reste:
    [ ] Cas simple (12 ÷ 3 = 4)
    [ ] Cas avec zéro
    [ ] Limites numériques
[ ] Tests division avec reste:
    [ ] Reste > 0
    [ ] Reste = 0
    [ ] Affichage correct (5 ÷ 2 = 2 reste 1)
[ ] Tests correction division:
    [ ] Quotient seul
    [ ] Quotient + reste
    [ ] Formats divers
[ ] Coverage check: pytest --cov=division_utils tests/
```

**Commit :** `test: add division unit tests`

#### Jour 4 - Tests Monnaie & Mesures

```
[ ] Créer: tests/test_monnaie_utils.py
[ ] Tests addition euros/centimes:
    [ ] Centimes seuls (25 + 30 = 55)
    [ ] Conversion en euros (75 + 50 = 1€25)
    [ ] Multiples euros
[ ] Tests rendu monnaie:
    [ ] Montants simples
    [ ] Avec centimes
    [ ] Billets/pièces combos
[ ] Créer: tests/test_mesures_utils.py
[ ] Tests longueurs:
    [ ] Conversions cm/mm
    [ ] Additions longueurs
[ ] Tests masses:
    [ ] kg/g conversions
[ ] Tests volumes (litres/ml):
    [ ] Conversions
    [ ] Opérations
[ ] Coverage global: pytest --cov=monnaie_utils --cov=mesures_utils
```

**Commit :** `test: add money and measurements tests`

---

### **JOUR 5 (Vendredi) : Tests Systèmes Critiques**

#### Tests Adaptive System

```
[ ] Créer: tests/test_adaptive_system.py
[ ] Tests recommandation exercice:
    [ ] Première visite (niveau basique)
    [ ] Progression normale
    [ ] Trop facile → niveau +1
    [ ] Trop difficile → niveau -1
[ ] Tests calcul difficulté:
    [ ] Plage correcte de nombres
    [ ] Opérations appropriées au niveau
[ ] Tests historique:
    [ ] Mémorisation réponses
    [ ] Calcul taux réussite exact
```

#### Tests Skill Tracker

```
[ ] Créer: tests/test_skill_tracker.py
[ ] Tests init utilisateur:
    [ ] Compétences créées ✓
    [ ] Valeurs initiales correctes
[ ] Tests update compétence:
    [ ] Score augmente (correct)
    [ ] Score stable (incorrect)
    [ ] Progression logique
[ ] Tests statistiques:
    [ ] Calcul moyennes exact
    [ ] Taux réussite correct
```

#### Tests Utilisateur

```
[ ] Créer: tests/test_utilisateur.py
[ ] Tests cache utilisateur:
    [ ] Load/save correct
    [ ] Données persistées
    [ ] PIN validation
[ ] Tests authentification:
    [ ] Bon PIN ✓
    [ ] Mauvais PIN ✗
    [ ] Max tentatives
```

**Commit :** `test: add adaptive system & tracking tests`

**End of Week 1 Status:**
```
✅ Coverage cible: 45-50%
✅ Tous tests passent
✅ 5 commits sur develop/v6.3
```

---

## 📅 SEMAINE 2 : Automatisation & Qualité

### **JOUR 6 & 7 (Lundi-Mardi) : CI/CD GitHub Actions**

#### Jour 6 - Setup Pipeline

```
[ ] Créer: .github/workflows/tests.yml
[ ] Contenu:
    [ ] Trigger: push & PR sur develop/*
    [ ] Python 3.9, 3.10, 3.11
    [ ] Install deps: pip install -r requirements.txt
    [ ] Lint: pip install pylint flake8
    [ ] Run linting: flake8 . --count --statistics
    [ ] Run tests: pytest tests/ -v
    [ ] Coverage report: pytest --cov=./ --cov-report=xml
[ ] Test localement: pytest tests/
[ ] Push sur GitHub:
    [ ] Vérifier Actions tab
    [ ] Workflow run ✓
    [ ] Tests passent
```

**Commit :** `ci: add GitHub Actions workflow`

#### Jour 7 - Coverage & Linting

```
[ ] Améliorer coverage (55%):
    [ ] Identifier manquements avec: pytest --cov-report=html
    [ ] Ajouter edge cases
    [ ] Tests erreurs/exceptions
[ ] Config linting:
    [ ] Créer: .flake8 (rules)
    [ ] Fix style issues
    [ ] Re-run: flake8 . --statistics
[ ] Créer: .pylintrc (config)
    [ ] Disable rules inutiles
    [ ] Run pylint sur 2-3 modules
[ ] Commit fixes: git commit -am "style: lint and format code"
```

**Commit :** `ci: improve coverage to 55%`

---

### **JOUR 8 & 9 (Mercredi-Jeudi) : Couverture Tests Complète**

#### Jour 8 - Edge Cases & Intégration

```
[ ] Ouvrir: pytest --cov-report=html (dans browser)
[ ] Identifier: modules < 70% coverage
[ ] Pour chaque module:
    [ ] Tests cas limites
    [ ] Tests erreurs
    [ ] Tests intégration inter-modules
    [ ] Coverage cible: 75%+
[ ] Tester scenarios complets:
    [ ] Élève se connecte → fait exercices → progression
    [ ] Erreur → niveau baisse
    [ ] Changement d'utilisateur
[ ] Run full suite: pytest tests/ -v --cov
```

**Commit :** `test: add integration tests & edge cases`

#### Jour 9 - Optimisation Tests

```
[ ] Vérifier temps tests: pytest tests/ --durations=10
[ ] Tests lents? Optimize:
    [ ] Fixtures pytest (conftest.py)
    [ ] Mock données lourdes
    [ ] Parallelization: pytest -n auto
[ ] Installer: pip install pytest-xdist
[ ] Ajouter à requirements-dev.txt
[ ] Vérifier CI/CD speed
[ ] Target Coverage: 80%+
[ ] pytest --cov tests/ (reporter final)
```

**Commit :** `test: optimize test performance & reach 80% coverage`

---

### **JOUR 10 (Vendredi) : Documentation Technique**

```
[ ] Créer: docs/ARCHITECTURE.md
    [ ] Diagramme modules
    [ ] Flux exercice complet
    [ ] Gestion données
    [ ] Sécurité
[ ] Créer: docs/API.md
    [ ] API public par module
    [ ] Paramètres/retours
    [ ] Exemples code
[ ] Créer: CONTRIBUTING.md
    [ ] Setup dev
    [ ] Structure tests
    [ ] Standards code
    [ ] Git workflow
[ ] Mettre à jour: README.md
    [ ] Ajouter badges (build, coverage)
    [ ] Tests instruction
    [ ] Architecture link
[ ] Review all docs
```

**Commit :** `docs: add technical documentation`

**End of Week 2 Status:**
```
✅ Coverage: 80%+
✅ CI/CD: Green builds
✅ Docs: 90% complet
✅ Prêt pour sécurité (week 3)
```

---

## 📅 SEMAINE 3 : Sécurité & Préparation Production

### **JOUR 11 & 12 (Lundi-Mardi) : Sécurité Données**

#### Jour 11 - Encryption & Validation

```
[ ] Installer: pip install cryptography bcrypt
[ ] Ajouter à requirements.txt
[ ] Créer: security/encryption.py
    [ ] Fonction hash PIN (bcrypt)
    [ ] Fonction verify PIN
    [ ] Tests sécurité PIN
[ ] Créer: security/validators.py
    [ ] Validate nom élève (alphanumérique + accents)
    [ ] Validate email
    [ ] Sanitize inputs
[ ] Refactor authentification.py:
    [ ] Utiliser bcrypt vs plaintext
    [ ] Ajouter validation input
    [ ] Rate limiting (3 tentatives max)
[ ] Tests sécurité:
    [ ] PIN brute force impossible
    [ ] Inputs malveillants rejetés
    [ ] Données sensibles chiffrées
[ ] Update utilisateurs.json -> schéma sécurisé
```

**Commit :** `security: implement encryption & input validation`

#### Jour 12 - Audit Sécurité

```
[ ] Dépendances check: pip install safety
    [ ] Lancer: safety check
    [ ] Corriger vulnerabilities
[ ] Config .env:
    [ ] Créer: .env.example
    [ ] Config réelle: .env (gitignored)
    [ ] Charger depuis config au démarrage
[ ] Permissions fichiers:
    [ ] utilisateurs*.json → 0600 (owner only)
    [ ] logs/ → 0750
    [ ] Vérifier: ls -la data/
[ ] Secrets check:
    [ ] Grep passwords: grep -r "password" . --exclude-dir=.git
    [ ] Grep API keys: grep -r "key" . --exclude-dir=.git
    [ ] Aucun en dur ✓
[ ] CHANGELOG sécurité:
    [ ] Documenter changements
    [ ] Version bump v6.3 beta → v6.3.0
```

**Commit :** `security: audit dependencies & configure secrets`

---

### **JOUR 13 & 14 (Mercredi-Jeudi) : Documentation Utilisateur**

#### Jour 13 - Installation & Admin

```
[ ] Créer: docs/INSTALLATION.md
    [ ] Prérequis (Python 3.9+)
    [ ] Clone repo
    [ ] Setup env: python -m venv venv
    [ ] Installer deps: pip install -r requirements.txt
    [ ] Lancer: streamlit run app.py
    [ ] Troubleshooting courants
[ ] Créer: docs/ADMIN_GUIDE.md
    [ ] Ajouter nouvel élève (UI)
    [ ] Changer PIN élève
    [ ] Exporter données élève
    [ ] Supprimer compte élève
    [ ] Sauvegarder données (backup)
[ ] Créer: docs/DEPLOYMENT.md
    [ ] Serveur local vs cloud
    [ ] Config production (secrets)
    [ ] SSL/HTTPS
    [ ] Performance settings
```

**Commit :** `docs: add installation & administration guides`

#### Jour 14 - Backup & Roadmap v7

```
[ ] Créer: scripts/backup.py
    [ ] Zip tous fichiers JSON
    [ ] Timestamp backup
    [ ] Compression + upload
[ ] Créer: scripts/restore.py
    [ ] Restaurer depuis backup
    [ ] Vérifier intégrité
    [ ] Logs restore
[ ] Tests backup/restore:
    [ ] Backup créé ✓
    [ ] Données complètes
    [ ] Restore fonctionne
    [ ] Pas de perte
[ ] Créer: docs/v7_ROADMAP.md
    [ ] API REST blueprint
    [ ] Multi-utilisateurs serveur
    [ ] DB migration plan
    [ ] UI/UX improvements
    [ ] Timeline estimation
[ ] Update README: lien vers v7 roadmap
```

**Commit :** `ops: add backup/restore scripts & v7 blueprint`

---

### **JOUR 15 (Vendredi) : Final Review & Release**

```
[ ] Code review complet:
    [ ] Tous tests passent ✓
    [ ] Coverage 80%+
    [ ] Lint clean (0 errors)
    [ ] Docs 95% complet
[ ] Update CHANGELOG:
    [ ] Lister features v6.3
    [ ] Bug fixes
    [ ] Breaking changes (none)
    [ ] Sécurité improvements
[ ] Créer release notes:
    [ ] Pour utilisateurs
    [ ] Pour développeurs
[ ] Version bump:
    [ ] Update version string (6.3.0)
    [ ] Tag git: git tag v6.3.0
    [ ] Push tags: git push --tags
[ ] Final checks:
    [ ] [ ] App démarre ✓
    [ ] [ ] Élève peut se connecter ✓
    [ ] [ ] Tests passent ✓
    [ ] [ ] CI/CD green ✓
    [ ] [ ] Docs accessible ✓
[ ] Merge develop → main
[ ] GitHub Release créée
```

**Commit :** `release: v6.3.0 - Production Ready`

**End of Week 3 Status:**
```
✅ v6.3.0 Released 🎉
✅ Sécurité validée
✅ Docs complètes
✅ Prêt pour production
✅ v7 roadmap défini
```

---

## 📊 Progress Dashboard

### Semaine 1
- [ ] Tests: 0% → 50%
- [ ] Coverage: 0% → 45%
- [ ] Commits: 5

### Semaine 2
- [ ] Tests: 50% → 100%
- [ ] Coverage: 45% → 80%+
- [ ] Commits: 5-6
- [ ] CI/CD: Active

### Semaine 3
- [ ] Sécurité: ✓ Validée
- [ ] Docs: ✓ Complètes
- [ ] Release: ✓ v6.3.0
- [ ] Commits: 5

**Total estimé:** 45 jours-homme (faisable en 3 semaines à temps plein)

---

## 🚀 Notes Importantes

- **Daily standup :** Chaque matin vérifier status tracker
- **Pas de multitasking :** 1 task à la fois = 1 commit
- **Blocages ?** → Document dans DECISIONS_LOG.md
- **Questions code ?** → Claude Code avec contexte task
- **Git régulièrement :** Commits atomiques + messages clairs

---

## 🎯 Feedback Loop

- Fin Jour 5: Review semaine 1 avec équipe
- Fin Jour 10: Sprint review + ajustements
- Fin Jour 15: Validation release + retrospective

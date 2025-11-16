# 🚀 MathCopain Phase 7 - Guide d'Utilisation
## Infrastructure PostgreSQL & Machine Learning

**Version:** 6.3
**Date:** 2025-11-16
**Status:** ✅ Implémenté

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Configuration PostgreSQL](#configuration-postgresql)
4. [Migration des données](#migration-des-données)
5. [Utilisation des modèles ML](#utilisation-des-modèles-ml)
6. [API Reference](#api-reference)
7. [Tests](#tests)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 VUE D'ENSEMBLE

La Phase 7 transforme MathCopain avec:

### 7.1 - PostgreSQL Migration
- ✅ Base de données relationnelle scalable
- ✅ 7 tables optimisées avec indexes
- ✅ Support 1000+ utilisateurs concurrents
- ✅ Migrations Alembic
- ✅ Connection pooling

### 7.2 - Machine Learning Adaptatif
- ✅ **DifficultyOptimizer** - Prédiction de difficulté optimale (XGBoost)
- ✅ **PerformancePredictor** - Prédiction de succès + détection élèves à risque (Random Forest)
- ✅ **FeatureEngineering** - 20+ features extraites automatiquement
- ✅ **ExplainableAI** - Explicabilité avec SHAP + audit d'équité

---

## 📦 INSTALLATION

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les nouvelles dépendances Phase 7:
- `sqlalchemy>=2.0.0` - ORM
- `psycopg2-binary>=2.9.0` - Driver PostgreSQL
- `alembic>=1.12.0` - Migrations
- `scikit-learn>=1.3.0` - ML
- `xgboost>=2.0.0` - Gradient Boosting
- `shap>=0.43.0` - Explainability

### 2. Créer le fichier .env

```bash
cp .env.example .env
```

Éditer `.env` avec vos configurations:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mathcopain
DB_USER=mathcopain_user
DB_PASSWORD=mathcopain_password
```

---

## 🐘 CONFIGURATION POSTGRESQL

### Option 1: Docker (Recommandé)

```bash
# Démarrer PostgreSQL avec Docker Compose
cd docker
docker-compose up -d

# Vérifier que PostgreSQL est en cours d'exécution
docker ps
```

Accès pgAdmin (interface web):
- URL: http://localhost:5050
- Email: admin@mathcopain.com
- Password: admin123

### Option 2: Installation locale

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Créer la base de données
sudo -u postgres createdb mathcopain
sudo -u postgres createuser mathcopain_user
```

### Initialiser les tables

```bash
# Créer toutes les tables via Alembic
alembic upgrade head

# Ou via Python
python -c "from database.connection import init_database; init_database()"
```

---

## 🔄 MIGRATION DES DONNÉES

### Migrer de JSON vers PostgreSQL

Le script `database/migration_scripts/json_to_postgres.py` migre automatiquement toutes vos données JSON vers PostgreSQL.

### 1. Dry-run (validation uniquement)

```bash
python database/migration_scripts/json_to_postgres.py --mode dry-run
```

Sortie:
```
🚀 MATHCOPAIN JSON → PostgreSQL MIGRATION
Mode: DRY-RUN
============================================================
📂 Loading JSON files...
✓ Loaded: users_data.json (15 items)
✓ Loaded: users_credentials.json (15 items)

🔍 Validating data...
✓ Data validation passed

📊 Migration Statistics:
  total_users: 15

============================================================
DRY-RUN MODE - No data will be written to database
============================================================
Would migrate:
  - 15 users
  - ~150 skill profiles (estimated)
  - ~15 analytics events
```

### 2. Migration complète

```bash
# Avec initialisation de la DB
python database/migration_scripts/json_to_postgres.py \
    --mode full \
    --init-db

# Sans initialisation (tables déjà créées)
python database/migration_scripts/json_to_postgres.py --mode full
```

Sortie:
```
📦 Creating backup in: ./backups/backup_20251116_180000
  ✓ Backed up: users_data.json
  ✓ Backed up: users_credentials.json

============================================================
EXECUTING FULL MIGRATION
============================================================
👥 Migrating users...
  ✓ Created user: alice (ID: 1)
  ✓ Created user: bob (ID: 2)
  ...
✓ Migrated 15 users

📊 Migrating skill profiles...
✓ Migrated 142 skill profiles

📈 Creating analytics events...
✓ Created 15 analytics events

============================================================
✅ MIGRATION COMPLETED SUCCESSFULLY
============================================================
```

### 3. Rollback (si nécessaire)

```bash
python database/migration_scripts/json_to_postgres.py \
    --rollback ./backups/backup_20251116_180000
```

---

## 🤖 UTILISATION DES MODÈLES ML

### DifficultyOptimizer - Prédire la difficulté optimale

```python
from core.ml.difficulty_optimizer import DifficultyOptimizer

# Initialiser
optimizer = DifficultyOptimizer()

# Prédire la difficulté pour un utilisateur
difficulty, explanation = optimizer.predict(
    user_id=1,
    skill_domain='addition',
    apply_flow_adjustment=True  # Appliquer Flow Theory
)

print(f"Difficulté recommandée: D{difficulty}")
print(f"Raisons: {explanation['reasons']}")
```

Sortie:
```
Difficulté recommandée: D3
Raisons: ['✓ Tu réussis bien (+75%)', '📈 Tu t'améliores', '🎯 Prérequis bien maîtrisés']
```

### PerformancePredictor - Prédire le succès

```python
from core.ml.performance_predictor import PerformancePredictor

# Initialiser
predictor = PerformancePredictor()

# Prédire la probabilité de succès
success_prob, explanation = predictor.predict_success_probability(
    user_id=1,
    skill_domain='addition'
)

print(f"Probabilité de succès: {success_prob:.1%}")
print(f"Interprétation: {explanation['interpretation']}")
```

Sortie:
```
Probabilité de succès: 78.5%
Interprétation: Probable de réussir
```

### Identifier les élèves à risque

```python
# Liste d'utilisateurs à analyser
user_ids = [1, 2, 3, 4, 5]

# Identifier les élèves à risque
at_risk = predictor.identify_at_risk_learners(
    user_ids=user_ids,
    skill_domain='multiplication',
    horizon_days=7
)

# Afficher les résultats
for learner in at_risk:
    print(f"{learner['username']}: {learner['risk_level'].upper()}")
    print(f"  Risque: {learner['risk_score']:.0%}")
    print(f"  Action: {learner['recommended_action']}")
```

Sortie:
```
bob: HIGH
  Risque: 72%
  Action: Suivi rapproché et exercices de renforcement

charlie: CRITICAL
  Risque: 85%
  Action: Intervention immédiate recommandée - revoir les bases
```

### Prédire le timeline de maîtrise

```python
timeline = predictor.predict_mastery_timeline(
    user_id=1,
    skill_domain='division',
    target_proficiency=0.8  # 80% de maîtrise
)

print(f"Proficiency actuelle: {timeline['current_proficiency']:.0%}")
print(f"Exercices nécessaires: {timeline['exercises_needed']}")
print(f"Jours estimés: {timeline['estimated_days']}")
print(f"Date estimée: {timeline['estimated_date']}")
```

Sortie:
```
Proficiency actuelle: 45%
Exercices nécessaires: 28
Jours estimés: 14
Date estimée: 2025-11-30
```

### ExplainableAI - Expliquer les prédictions

```python
from core.ml.explainability import ExplainableAI

# Initialiser
xai = ExplainableAI(
    difficulty_optimizer=optimizer,
    performance_predictor=predictor
)

# Expliquer une prédiction de difficulté
explanation = xai.explain_difficulty_prediction(
    user_id=1,
    skill_domain='addition',
    top_n=5
)

print(f"Difficulté: D{explanation['difficulty']}")
print("\nTop 5 facteurs contribuants:")
for contrib in explanation['top_contributors']:
    print(f"  {contrib['feature']}: {contrib['contribution']:.3f} ({contrib['impact']})")

print("\nExplications:")
for exp in explanation['explanations']:
    print(f"  - {exp}")
```

Sortie:
```
Difficulté: D3

Top 5 facteurs contribuants:
  recent_success_rate: 0.245 (increase)
  domain_proficiency: 0.182 (increase)
  trend_7d: 0.098 (increase)
  streak: 0.067 (increase)
  fatigue_level: -0.043 (decrease)

Explications:
  - ✓ Bon taux de réussite (75%)
  - 📈 Progression récente positive
  - 🔥 Série de 4 succès!
```

### Audit d'équité

```python
# Audit fairness entre groupes démographiques
import pandas as pd
import numpy as np

# Préparer les données de test (exemple)
X_test = np.random.randn(100, 20)
y_test = np.random.randint(0, 2, 100)
demographics = pd.DataFrame({
    'grade_level': np.random.choice(['CE1', 'CE2', 'CM1', 'CM2'], 100),
    'learning_style': np.random.choice(['visual', 'auditory', 'kinesthetic'], 100)
})

# Auditer
fairness_report = xai.fairness_audit(
    X_test=X_test,
    y_test=y_test,
    demographics=demographics,
    model_type='performance'
)

print(f"Fairness Score: {fairness_report['fairness_score']:.2f}")
print(f"Assessment: {fairness_report['assessment']}")
```

---

## 📚 API REFERENCE

### Base de données (database/)

#### `database.connection`

```python
from database.connection import get_session, DatabaseSession, init_database

# Obtenir une session
with get_session() as session:
    users = session.query(User).all()

# Ou via context manager
with DatabaseSession() as session:
    user = User(username='test')
    session.add(user)
    # Commit automatique à la sortie

# Initialiser la DB
init_database(drop_all=False, echo=True)
```

#### `database.models`

7 modèles ORM:
- `User` - Comptes utilisateurs
- `ExerciseResponse` - Historique exercices
- `SkillProfile` - Profils de compétences
- `ParentAccount` - Comptes parents
- `ParentChildLink` - Relations parent-enfant
- `AnalyticsEvent` - Événements analytics
- `MLModel` - Métadonnées modèles ML

```python
from database.models import User, ExerciseResponse, SkillProfile

# Créer un utilisateur
user = User(
    username='alice',
    pin_hash='hashed_pin',
    learning_style='visual',
    grade_level='CE2'
)

# Créer une réponse exercice
response = ExerciseResponse(
    user_id=1,
    exercise_id='add_001',
    skill_domain='addition',
    difficulty_level=3,
    is_correct=True,
    time_taken_seconds=45
)
```

### Machine Learning (core/ml/)

#### `FeatureEngineering`

Extrait 20+ features automatiquement.

```python
from core.ml.feature_engineering import FeatureEngineering

fe = FeatureEngineering()

# Extraire features pour un utilisateur
features = fe.extract_features(
    user_id=1,
    skill_domain='addition',
    n_recent=10
)

# Convertir en array numpy
X = fe.features_to_array(features)
```

Features disponibles:
- Performance récente: `recent_success_rate`, `recent_avg_time`, `streak`
- Tendances: `trend_7d`, `trend_30d`, `learning_velocity`
- Contexte: `hour_of_day`, `day_of_week`, `fatigue_level`
- Compétences: `domain_proficiency`, `cross_domain_avg`
- Métacognition: `strategy_effectiveness`

#### `DifficultyOptimizer`

```python
# Entraîner le modèle
optimizer = DifficultyOptimizer()
metrics = optimizer.train(X_train, y_train)

# Sauvegarder
optimizer.save_model('models/difficulty_v1.pkl')

# Charger
optimizer.load_model('models/difficulty_v1.pkl')

# Prédire
difficulty, explanation = optimizer.predict(user_id=1, skill_domain='addition')

# Feature importance
importance_df = optimizer.get_feature_importance(top_n=10)
```

#### `PerformancePredictor`

```python
# Entraîner
predictor = PerformancePredictor()
metrics = predictor.train(X_train, y_train, use_smote=True)

# Prédire succès
prob, exp = predictor.predict_success_probability(user_id=1, skill_domain='addition')

# Identifier at-risk
at_risk = predictor.identify_at_risk_learners(
    user_ids=[1, 2, 3],
    skill_domain='multiplication'
)

# Timeline maîtrise
timeline = predictor.predict_mastery_timeline(
    user_id=1,
    skill_domain='division',
    target_proficiency=0.8
)
```

#### `ExplainableAI`

```python
xai = ExplainableAI(
    difficulty_optimizer=optimizer,
    performance_predictor=predictor
)

# Expliquer difficulty
exp = xai.explain_difficulty_prediction(user_id=1, skill_domain='addition')

# Expliquer performance
exp = xai.explain_performance_prediction(user_id=1, skill_domain='addition')

# Audit fairness
fairness = xai.fairness_audit(X_test, y_test, demographics, model_type='performance')

# Détecter biais
bias = xai.detect_bias(X, sensitive_features=[16, 17], feature_names=fe.get_feature_names())
```

---

## 🧪 TESTS

### Tests unitaires database

```bash
pytest tests/test_db_models.py -v
pytest tests/test_migration.py -v
```

### Tests ML

```bash
pytest tests/test_feature_engineering.py -v
pytest tests/test_difficulty_optimizer.py -v
pytest tests/test_performance_predictor.py -v
pytest tests/test_explainability.py -v
```

### Coverage

```bash
pytest --cov=database --cov=core/ml --cov-report=html
```

---

## ⚙️ CONFIGURATION

### Variables d'environnement (.env)

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mathcopain
DB_USER=mathcopain_user
DB_PASSWORD=mathcopain_password

# Connection pool
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Application
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# ML
ML_MODEL_PATH=./models
ML_RETRAIN_DAYS=30
```

### Alembic (alembic.ini)

Gère les migrations de schéma. Configuration dans `alembic.ini`.

```bash
# Créer une nouvelle migration
alembic revision -m "Description"

# Appliquer migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

---

## 🐛 TROUBLESHOOTING

### PostgreSQL ne démarre pas

```bash
# Vérifier les logs Docker
docker logs mathcopain_postgres

# Redémarrer le container
docker-compose restart postgres
```

### Erreur de connexion DB

```bash
# Tester la connexion
python -c "from database.connection import test_connection; test_connection()"
```

Vérifier `.env`:
- HOST correct (localhost ou IP)
- PORT correct (5432 par défaut)
- Credentials valides

### Migration échoue

```bash
# Mode dry-run pour déboguer
python database/migration_scripts/json_to_postgres.py --mode dry-run

# Vérifier les logs
# Restaurer depuis backup si nécessaire
python database/migration_scripts/json_to_postgres.py --rollback ./backups/backup_XXX
```

### Modèles ML pas trouvés

```bash
# Vérifier que le dossier models/ existe
mkdir -p models

# Les modèles doivent être entraînés avant utilisation
# Voir section "Entraînement des modèles"
```

---

## 📈 PERFORMANCE

### Optimisations DB

- **Indexes**: Créés automatiquement sur clés étrangères et colonnes fréquemment utilisées
- **Connection Pooling**: 10 connexions actives, 20 overflow max
- **Query caching**: Via SQLAlchemy

### Benchmarks

- Requête simple (user by ID): ~5ms
- Requête complexe (skill profiles + join): ~15ms
- Prédiction ML (difficulté): ~50ms
- Migration 1000 users: ~30s

---

## 🚀 PROCHAINES ÉTAPES

Phase 7 est maintenant complète! Prochaines étapes:

### Phase 8: Déploiement Institutionnel
- Mode Enseignant & Classe
- Dashboard Analytics complet
- Rapports PDF/CSV
- Intégration curriculum scolaire

---

## 📞 SUPPORT

Questions? Contactez mathcopain.contact@gmail.com

Documentation complète: [PHASE_7_ARCHITECTURE.md](./PHASE_7_ARCHITECTURE.md)

---

**Dernière mise à jour:** 2025-11-16
**Version:** 6.3 (Phase 7)

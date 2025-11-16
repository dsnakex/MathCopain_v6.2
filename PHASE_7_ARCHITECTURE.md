# 🔧 PHASE 7 - ARCHITECTURE TECHNIQUE
## Infrastructure & IA - MathCopain v6.3

**Date de début:** 2025-11-16
**Durée estimée:** 22 semaines
**Status:** 🚧 En cours

---

## 🎯 OBJECTIFS PHASE 7

### 7.1 - Migration PostgreSQL (10 semaines)
- Migrer de JSON vers base de données relationnelle PostgreSQL
- Supporter 1000+ utilisateurs concurrents
- Garantir intégrité des données
- Optimiser performance (requêtes <100ms)

### 7.2 - IA Adaptive Learning (12 semaines)
- ML pour difficulté optimale (Flow Theory)
- Prédiction de performance
- Détection élèves à risque
- Explainability (XAI) et fairness

---

## 📊 ARCHITECTURE BASE DE DONNÉES

### Schéma PostgreSQL (7 tables)

```sql
-- 1. Users (Utilisateurs)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    learning_style VARCHAR(20),
    grade_level VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    INDEX idx_username (username),
    INDEX idx_active (is_active)
);

-- 2. Exercise Responses (Historique exercices)
CREATE TABLE exercise_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exercise_id VARCHAR(100) NOT NULL,
    skill_domain VARCHAR(50) NOT NULL,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    question TEXT,
    user_response TEXT,
    expected_answer TEXT,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER,
    strategy_used VARCHAR(100),
    error_type VARCHAR(50),
    feedback_given TEXT,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_skill (user_id, skill_domain),
    INDEX idx_user_created (user_id, created_at DESC),
    INDEX idx_domain (skill_domain)
);

-- 3. Skill Profiles (Profils compétences)
CREATE TABLE skill_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    skill_domain VARCHAR(50) NOT NULL,
    proficiency_level FLOAT CHECK (proficiency_level BETWEEN 0 AND 1),
    exercises_completed INTEGER DEFAULT 0,
    success_rate FLOAT,
    last_practiced TIMESTAMP,
    mastery_date TIMESTAMP,

    UNIQUE (user_id, skill_domain),
    INDEX idx_user (user_id),
    INDEX idx_domain (skill_domain)
);

-- 4. Parent Accounts (Comptes parents)
CREATE TABLE parent_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_email (email)
);

-- 5. Parent-Child Links (Relations parent-enfant)
CREATE TABLE parent_child_links (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES parent_accounts(id) ON DELETE CASCADE,
    child_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    permission_level VARCHAR(20) DEFAULT 'view',
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (parent_id, child_id),
    INDEX idx_parent (parent_id),
    INDEX idx_child (child_id)
);

-- 6. Analytics Events (Événements analytics)
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_event (user_id, event_type),
    INDEX idx_created (created_at DESC),
    INDEX idx_session (session_id)
);

-- 7. ML Models Metadata (Métadonnées modèles ML)
CREATE TABLE ml_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(20) NOT NULL,
    model_type VARCHAR(50),
    training_date TIMESTAMP,
    accuracy_metrics JSONB,
    model_path VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_active (model_name, is_active)
);
```

---

## 🏗️ STRUCTURE FICHIERS

```
MathCopain_v6.2/
├── database/
│   ├── __init__.py
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── connection.py             # DB connection pooling
│   ├── session.py                # Session management
│   ├── migrations/               # Alembic migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_add_ml_tables.py
│   │       └── ...
│   └── migration_scripts/
│       ├── json_to_postgres.py   # Migration JSON → PostgreSQL
│       ├── data_validation.py
│       └── rollback_recovery.py
│
├── core/
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── difficulty_optimizer.py    # ML difficulté optimale
│   │   ├── performance_predictor.py   # Prédiction performance
│   │   ├── feature_engineering.py     # Feature extraction
│   │   ├── explainability.py          # XAI (SHAP)
│   │   └── fairness_audit.py          # Audit biais
│   │
│   └── ... (existing pedagogy, etc.)
│
├── models/                       # ML trained models
│   ├── difficulty_optimizer_v1.pkl
│   ├── performance_predictor_v1.pkl
│   └── metadata.json
│
├── config/
│   ├── database.yaml             # DB configuration
│   └── ml_config.yaml            # ML hyperparameters
│
└── docker/
    ├── docker-compose.yml        # PostgreSQL + pgAdmin
    └── Dockerfile.postgres
```

---

## 🤖 ARCHITECTURE ML

### Feature Engineering (20+ features)

```python
features = {
    # Performance récente
    'recent_success_rate': float,      # Taux succès 10 derniers
    'recent_avg_time': float,          # Temps moyen
    'streak': int,                     # Série de succès

    # Tendances
    'trend_7d': float,                 # Tendance 7 jours
    'trend_30d': float,                # Tendance 30 jours
    'learning_velocity': float,        # Vitesse apprentissage

    # Contexte
    'hour_of_day': int,                # Heure de la journée
    'day_of_week': int,                # Jour de la semaine
    'session_length': int,             # Durée session
    'fatigue_level': float,            # Niveau fatigue (0-1)

    # Compétences
    'prerequisite_mastery': float,     # Maîtrise prérequis
    'domain_proficiency': float,       # Niveau domaine
    'cross_domain_transfer': float,    # Transfer learning

    # Métacognition
    'self_reported_difficulty': float, # Difficulté perçue
    'strategy_effectiveness': float,   # Efficacité stratégie

    # Démographie (pour fairness)
    'grade_level': str,
    'learning_style': str
}
```

### Model 1: DifficultyOptimizer

```python
Algorithm: Gradient Boosting (XGBoost)
Target: optimal_difficulty (1-5)
Training Data: Historical responses (10,000+ samples)
Validation: 80/20 split, cross-validation K=5
Metrics: MAE < 0.5, R² > 0.75

Flow Theory Integration:
- Target success rate: 70% (optimal flow)
- Adjustment: ±1 difficulty if >85% or <55%
```

### Model 2: PerformancePredictor

```python
Ensemble:
├── LSTM (40% weight)
│   └── Time series forecasting
│       └── Input: Last 20 exercises
│       └── Output: Success probability next N
│
└── Random Forest (60% weight)
    └── Risk classification
        └── Input: Feature vector
        └── Output: At-risk probability

Final prediction: 0.4 * LSTM + 0.6 * RF
Threshold at-risk: 0.60
```

### Explainability (XAI)

```python
SHAP Values:
- Top 5 contributing features
- Human-readable explanations

Example output:
"Difficulté recommandée: D3
Raisons:
✓ Tu réussis bien (+75%)
📈 Tu t'améliores
😴 Tu fatigues un peu
🎯 Prérequis bien maîtrisés"
```

---

## 🔧 TECHNOLOGIES

### Base de Données
- **PostgreSQL 15+**: Base relationnelle
- **SQLAlchemy 2.0**: ORM Python
- **Alembic**: Migrations
- **psycopg2**: Driver PostgreSQL
- **pgAdmin**: Interface administration

### Machine Learning
- **scikit-learn**: Random Forest, feature engineering
- **XGBoost**: Gradient Boosting
- **TensorFlow/Keras**: LSTM (optional, peut être remplacé par scikit)
- **SHAP**: Explainability
- **imbalanced-learn**: Gestion classes déséquilibrées

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **pytest**: Testing
- **pytest-postgresql**: Tests DB

---

## 📈 MIGRATION STRATEGY

### Phase 1: Setup (Semaine 1-2)
1. Docker PostgreSQL local
2. SQLAlchemy models
3. Alembic initialization
4. Tests unitaires DB

### Phase 2: Migration (Semaine 3-6)
1. Dry-run validation
2. Backup JSON
3. Migration script
4. Data integrity checks
5. Rollback si échec

### Phase 3: Refactoring (Semaine 7-10)
1. Refactor data_manager.py → DB queries
2. Refactor app.py → SQLAlchemy ORM
3. Connection pooling
4. Performance testing (1000+ users)

---

## 🧪 TESTING STRATEGY

### Database Tests (400+ tests)
- Model creation/relationships
- CRUD operations
- Constraint validation
- Migration integrity
- Performance (>1000 inserts/sec)

### ML Tests (800+ tests)
- Feature engineering accuracy
- Model prediction calibration
- Fairness across demographics
- Explainability coherence
- Edge cases (cold start, sparse data)

### Integration Tests (200+ tests)
- End-to-end workflows
- DB + ML pipeline
- Real-time predictions
- Fallback mechanisms

**Target Coverage: 85%+**

---

## 🚀 DEPLOYMENT

### Local Development
```bash
docker-compose up -d postgres
alembic upgrade head
pytest tests/
streamlit run app.py
```

### Production (AWS)
- RDS PostgreSQL (Multi-AZ)
- S3 for ML models
- CloudWatch monitoring
- Backup strategy (daily snapshots)

---

## 📊 SUCCESS METRICS

### Performance
- [ ] DB queries <100ms (p95)
- [ ] ML predictions <50ms
- [ ] Support 1000+ concurrent users
- [ ] 99.9% uptime

### Accuracy
- [ ] Difficulty optimizer MAE <0.5
- [ ] Performance predictor AUC >0.85
- [ ] At-risk detection recall >0.80

### Quality
- [ ] Test coverage >85%
- [ ] Zero critical bugs
- [ ] Documentation complète

---

## ⚠️ RISKS & MITIGATION

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Migration data loss | Élevé | Faible | Backup + dry-run + validation |
| ML bias | Moyen | Moyen | Fairness audit + diverse training data |
| Performance issues | Moyen | Faible | Load testing + indexing + pooling |
| Scope creep | Élevé | Moyen | Strict adherence au roadmap |

---

**Document créé:** 2025-11-16
**Responsable:** Équipe MathCopain
**Prochaine révision:** Après semaine 10

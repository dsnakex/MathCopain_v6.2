# 🤖 CLAUDE_CODE_BRIEFING.md
## Guide d'Utilisation Claude Code pour Phases 6-8

---

# 🎯 OBJECTIF

Fournir à Claude Code des **prompts optimisés et contextualisés** pour implémenter les phases 6, 7, 8 de MathCopain sans friction.

**Chaque prompt inclut:**
- ✅ Code structure attendue
- ✅ Fichiers à créer
- ✅ Tests à écrire
- ✅ Dépendances
- ✅ Commits git

---

# 📋 PHASE 6 : Fondations Pédagogiques

## 6.1 - FEEDBACK PÉDAGOGIQUE INTELLIGENT

### Prompt 6.1.1 - ErrorAnalyzer

**Titre:** "Implémenter ErrorAnalyzer pour MathCopain v6.4"

**Texte du Prompt:**

```
# CONTEXT
Je développe MathCopain, une app d'apprentissage des maths pour enfants CE1-CM2.
Vous avez déjà fait une v6.3 complète (tests, sécurité, architecture modulaire).
Maintenant on lance la Phase 6 : Fondations Pédagogiques.

# PHASE 6.1 - FEEDBACK PÉDAGOGIQUE INTELLIGENT

## Objectif
Transformer feedback basique → explications transformatives qui augmentent l'apprentissage de +35-40%
Basé sur théorie Hattie 2008 (feedback avec effet-taille 0.79).

## TÂCHE: Implémenter ErrorAnalyzer

### Fichier à créer
`core/pedagogy/error_analyzer.py` (300 lignes)

### Structure Classe

```python
class ErrorAnalyzer:
    """Analyse errors mathématiques et catégorise par type"""
    
    def __init__(self):
        # Load error_taxonomy.json
        # 500+ erreurs pré-cataloguées
        self.error_catalog = self._load_catalog()
    
    def analyze_error_type(self, exercise, response, expected):
        '''
        Retourne:
        {
            "type": "Conceptual" | "Procedural" | "Calculation",
            "misconception": "L'enfant oublie la retenue",
            "severity": 1-5,
            "confidence": 0.92,
            "examples": [...]
        }
        '''
    
    def identify_misconception(self, error_type):
        '''
        Query error_taxonomy.json
        Retourne: misconception details + common student reasons
        '''
    
    def root_cause_analysis(self, error_details):
        '''
        Pourquoi l'enfant s'est trompé?
        Retourne: analysis + prerequisite gaps
        '''
```

### Dépendances
- json, pandas, numpy

### Data Files
- `data/error_taxonomy.json` (will be created separately)

### Tests à écrire
`tests/test_error_analyzer.py` (300+ tests)

Coverage: 85%+
```

**Note pour Claude Code:**
Ceci est le premier prompt. Il doit créer ErrorAnalyzer complet avec tests.
Attendez la confirmation qu'il compile + tous les tests passent avant de continuer.

---

### Prompt 6.1.2 - error_taxonomy.json Creation

**Titre:** "Générer error_taxonomy.json avec 500+ erreurs mathématiques"

**Texte:**

```
# TÂCHE: Créer error_taxonomy.json

## Structure JSON

Le fichier doit contenir 500+ erreurs mathématiques structurées par domaine.

### Format

```json
{
  "error_catalog": {
    "addition_carry_error_001": {
      "type": "procedural",
      "domain": "addition",
      "common_in_grades": ["CE1", "CE2"],
      "misconception": "L'enfant oublie la retenue quand la somme dépasse 10",
      "examples": [
        {
          "input": "23 + 14",
          "wrong_answer": "37",
          "correct_answer": "37",
          "error_description": "Oublie de reporter la dizaine"
        }
      ],
      "feedback_templates": [
        "Tu as trouvé 37, mais regarde: 23 + 14 = (20 + 10) + (3 + 4) = 30 + 7 = 37 ✓",
        "N'oublie pas la retenue! Quand tu additionnes 3 + 4 = 7, ça va dans les unités."
      ],
      "remediation_path": "addition_with_carry_basics",
      "severity": 3
    },
    // ... 499+ more errors
  }
}
```

## Domaines à couvrir (500+ total errors)

- addition (50+ errors): carry, place value, zero, negative
- subtraction (50+ errors): borrowing, place value, minuend vs subtrahend
- multiplication (50+ errors): tables, distributive, area model
- division (40+ errors): remainders, long division, divisibility
- fractions (40+ errors): equivalence, operations, GCD
- decimals (40+ errors): place value, operations, rounding
- geometry (40+ errors): perimeter, area, volume, angle
- measurements (40+ errors): units, conversion, estimation
- proportionality (40+ errors): ratio, percentage, scale
- money (40+ errors): currency, making change, comparison

## Production Requirements

1. Valid JSON (verify with Python json.loads())
2. Each error has: type, domain, misconception, examples, templates, remediation
3. Taxonomic structure (400 structured errors + variations)
4. No duplicates
5. Pedagogically accurate

## Output Format
Generate in single JSON block, ready to paste into data/error_taxonomy.json
```

**Note:** Ceci est long (~20,000 lignes JSON). Claude Code doit le générer en un seul fichier.

---

### Prompt 6.1.3 - FeedbackGenerator Implementation

**Titre:** "Implémenter FeedbackGenerator - Feedback Pédagogique Transformatif"

**Texte:**

```
# TÂCHE: Implémenter FeedbackGenerator

Basé sur ErrorAnalyzer, générer feedback pédagogiquement transformatif.
Théorie: Hattie 2008 - Feedback avec effet-taille 0.79.

## Fichier à créer
`core/pedagogy/feedback_engine.py` (400 lignes)

## Structure Classe

```python
class TransformativeFeedback:
    """Generate pedagogically transformative feedback"""
    
    def __init__(self):
        self.error_analyzer = ErrorAnalyzer()
        self.feedback_gen = FeedbackGenerator()
        self.remediation = RemediationRecommender()
    
    def process_exercise_response(self, exercise, response, user_id):
        '''
        Analyse réponse exercice → Feedback multi-couches
        
        Retourne:
        {
            "immediate": "✅ Correct!" ou "❌ Pas tout à fait",
            "explanation": "Concept-level explanation",
            "strategy": "Stratégie alternative",
            "remediation": {...},
            "encouragement": "Personnalisé",
            "next_action": "Refaire | Continuer | Voir détails"
        }
        '''
    
    def _generate_success_feedback(self, exercise, user_id):
        '''Positive feedback intelligent'''
    
    def _generate_failure_feedback(self, error_analysis, user_id):
        '''Constructive failure feedback'''
```

## Multi-Layer Feedback

When response is WRONG:
1. **Immediate** (5 words): "C'est presque ça!"
2. **Explanation** (50 words): Pourquoi la réponse est fausse
3. **Strategy** (50 words): Une autre façon de résoudre
4. **Remediation** (Action): Exercice similaire plus facile
5. **Encouragement** (Personalized): Basé sur l'historique

When response is CORRECT:
1. **Immediate**: "✅ Exact!"
2. **Recognition**: Acknowledgement spécifique
3. **Insight**: "Tu l'as résolu en 12 secondes!"
4. **Progression**: Visualiser progrès
5. **Next Challenge**: Proposer niveau suivant

## Dépendances
- Jinja2 (pour templates)
- Pandas (pour données utilisateur)
- ErrorAnalyzer (class importée)

## Tests
`tests/test_feedback_engine.py` (400+ tests)

Coverage: 85%+

Test scenarios:
- Correct answer → correct feedback
- Wrong answer → diagnostic feedback
- Edge cases: Empty response, malformed input, unusual error types
```

---

### Prompt 6.1.4 - App.py Integration

**Titre:** "Intégrer TransformativeFeedback dans app.py"

**Texte:**

```
# TÂCHE: Intégrer TransformativeFeedback dans app.py existant

## Contexte
MathCopain a un app.py Streamlit de 305 lignes (refactorisé en v6.3).
Vous devez ajouter feedback intelligent APRÈS exercice submission.

## Modifications app.py

Ajouter après ligne qui vérifie réponse exercice:

```python
from core.pedagogy.feedback_engine import TransformativeFeedback

# Instancier une fois
if 'feedback_engine' not in st.session_state:
    st.session_state.feedback_engine = TransformativeFeedback()

# DANS exercise_completed_handler():
def show_exercise_feedback(exercise, response, user_id):
    feedback = st.session_state.feedback_engine.process_exercise_response(
        exercise=exercise,
        response=response,
        user_id=user_id
    )
    
    # Show feedback UI
    with st.container(border=True):
        # Layer 1: Immediate
        if feedback['success']:
            st.success(feedback['immediate'])
        else:
            st.error(feedback['immediate'])
        
        # Layer 2: Explanation (expander)
        with st.expander("📖 Explication"):
            st.write(feedback['explanation'])
        
        # Layer 3: Strategy (expander)
        with st.expander("💡 Stratégie Alternative"):
            st.write(feedback['strategy'])
        
        # Layer 4: Remediation
        if feedback['remediation']:
            st.info(f"📚 {feedback['remediation']['title']}")
            st.write(feedback['remediation']['description'])
        
        # Layer 5: Encouragement
        st.caption(f"✨ {feedback['encouragement']}")
        
        # Next Action
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Refaire ce type", key="replay"):
                # Regenerate same type
                pass
        with col2:
            if st.button("⏭️ Continuer", key="continue"):
                # Move to next exercise
                pass
```

## UI Structure
- 5 layers of feedback
- Expanders to avoid overwhelming
- Action buttons (Refaire, Continuer)
- Emoji for visual cues

## Tests
`tests/test_feedback_integration.py` (150+ tests)

Verify:
- Feedback renders correctly
- All layers display
- Buttons functional
- No console errors
```

---

## 6.2 - MÉTACOGNITION & AUTORÉGULATION

### Prompt 6.2.1 - MetacognitionEngine

**Titre:** "Implémenter MetacognitionEngine - Questions réflexives post-exercice"

**Texte:**

```
# TÂCHE: MetacognitionEngine

Aider enfants à réfléchir à leur processus d'apprentissage.
Théorie: Flavell (métacognition) - prédicteur majeur succès académique.

## Fichier à créer
`core/pedagogy/metacognition.py` (400 lignes)

## Classe MetacognitionEngine

```python
class MetacognitionEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        self.portfolio = StrategyPortfolio(user_id)
    
    def generate_reflection_questions(self, exercise):
        '''
        Generate 4 reflection questions (30 sec max)
        
        1. Stratégie? ["Doigts", "Mental", "Dessin", "Formule", "Autre"]
        2. Difficulté? [Facile ← slider → Difficile]
        3. Auto-explication? ["Explique comment tu as trouvé"]
        4. Intention future? ["Prochaine fois je vais..."]
        '''
    
    def process_reflection(self, reflection_data):
        '''
        Traite réponses réflexives:
        1. Enregistrer stratégie dans portfolio
        2. Analyser patterns
        3. Générer insights personnalisés
        4. Suggérer améliorations
        '''
    
    def generate_self_regulation_suggestions(self):
        '''
        Suggest actions based on session:
        - "Tu sembles frustré. Pause?"
        - "5 bonnes d'affilée! Défi plus difficile?"
        - "Tu fatigues. Peut-être c'est bon pour aujourd'hui."
        '''
```

## Reflection UI (30 sec max)

Question 1: "🎯 Quelle stratégie as-tu utilisée?"
  ☐ Sur mes doigts
  ☐ Dans ma tête (mental)
  ☐ En dessinant
  ☐ Avec une formule
  ☐ Autrement: _____

Question 2: "📊 Difficulté?"
  [Facile] ◐─────●───◑ [Difficile]

Question 3: "💬 Comment tu as trouvé?"
  [Textbox - optional]

Question 4: "🔮 Prochaine fois?"
  [Textbox - optional]

## Data Storage
- Store in user_profiles/{user_id}/reflections.json
- Accumulate 50+ reflections for pattern analysis

## Tests
`tests/test_metacognition.py` (350+ tests)

Scenarios:
- Reflection capture
- Pattern detection
- Suggestion generation
- Portfolio updates
```

---

## 6.3 - PROFILING STYLES D'APPRENTISSAGE

### Prompt 6.3.1 - LearningStyleAnalyzer

**Titre:** "Implémenter LearningStyleAnalyzer - 5 Styles"

**Texte:**

```
# TÂCHE: LearningStyleAnalyzer

Identifier learning style de chaque enfant + adapter présentation.
Théorie: Gardner (Multiple Intelligences).

## Fichier à créer
`core/pedagogy/learning_style.py` (350 lignes)

## 5 Learning Styles

1. **Visual** - Préfère graphiques, diagrammes, couleurs
2. **Auditory** - Préfère descriptions verbales, audio
3. **Kinesthetic** - Préfère manipuler, interactif, tactile
4. **Logical** - Préfère comprendre pourquoi, causal chains
5. **Narrative** - Préfère histoires, contextes réels

## Classe LearningStyleAnalyzer

```python
class LearningStyleAnalyzer:
    STYLES = ["visual", "auditory", "kinesthetic", "logical", "narrative"]
    
    def assess_from_quiz(self, responses):
        '''Quiz 5-7 questions → Primary + Secondary style'''
    
    def infer_from_performance(self, performance_history):
        '''Analyser patterns historiques → Infer style'''
    
    def combine_assessments(self, quiz_result, performance_result):
        '''
        Combine:
        - Quiz: 40%
        - Performance: 60%
        
        Retourne: {primary, secondary, confidence}
        '''
```

## Quiz Format (5-7 questions)

Question 1: "Quand tu apprends, tu préfères:"
  ☐ Voir un diagramme
  ☐ Écouter une explication
  ☐ Essayer soi-même
  ☐ Comprendre la logique

Question 2: "Tes meilleurs souvenirs école?"
  ☐ Les tableaux/posters
  ☐ Les histoires du prof
  ☐ Les expériences/activités
  ☐ Les maths/structures

... (3-5 more)

## Profile Storage
`data/user_profiles/{user_id}/learning_style.json`

```json
{
  "primary": {
    "style": "visual",
    "confidence": 0.87
  },
  "secondary": {
    "style": "kinesthetic",
    "confidence": 0.62
  },
  "assessment_date": "2025-11-15",
  "data_points": 45,
  "confidence_overall": 0.82
}
```

## Tests
`tests/test_learning_style.py` (300+ tests)

Coverage: 85%+
```

---

### Prompt 6.3.2 - ExerciseAdapters (5 Adapters)

**Titre:** "Implémenter 5 ExerciseAdapters pour adapter présentation par style"

**Texte:**

```
# TÂCHE: Implémenter 5 ExerciseAdapters

Adapter présentation d'exercice selon learning style.
+25-35% engagement quand adapté.

## Fichiers à créer
`core/exercise_generator/exercise_adapter.py` (Main adapter)
`core/exercise_generator/adapters/visual_adapter.py` (150 lignes)
`core/exercise_generator/adapters/auditory_adapter.py` (100 lignes)
`core/exercise_generator/adapters/kinesthetic_adapter.py` (150 lignes)
`core/exercise_generator/adapters/logical_adapter.py` (100 lignes)
`core/exercise_generator/adapters/narrative_adapter.py` (150 lignes)

## Main ExerciseAdapter

```python
class ExercisePresenterAdapter:
    def __init__(self, learning_style):
        self.style = learning_style
        self.adapters = {
            "visual": VisualAdapter(),
            "auditory": AuditoryAdapter(),
            "kinesthetic": KinestheticAdapter(),
            "logical": LogicalAdapter(),
            "narrative": NarrativeAdapter()
        }
    
    def adapt_exercise(self, exercise):
        '''
        Retourne exercise adapté au style:
        {
            "problem_statement": adapted string,
            "hint": adapted hint,
            "visual_aids": {...},
            "explanation_style": "...",
            "resource_suggestion": {...}
        }
        '''
```

## 5 Adapters Details

### VisualAdapter
```python
class VisualAdapter:
    def format_problem(self, problem):
        # Add emoji, formatting
        return "📊 Visualise: " + problem
    
    def generate_visuals(self, exercise):
        # Return: diagram, number_line, color_coding
    
    def suggest_resources(self):
        # Return URLs to visual explanation videos
```

### AuditoryAdapter
```python
class AuditoryAdapter:
    def format_problem(self, problem):
        return "🎵 Écoute: " + problem
    
    def suggest_resources(self):
        # Return audio explanation file
```

### KinestheticAdapter
```python
class KinestheticAdapter:
    def format_problem(self, problem):
        return "👆 Manipule: " + problem
    
    def generate_visuals(self, exercise):
        # Return interactive manipulables (draggable blocks)
```

### LogicalAdapter
```python
class LogicalAdapter:
    def format_problem(self, problem):
        return "🧠 Comprends la logique: " + problem
    
    def format_hint(self, hint):
        return "Pourquoi? " + hint
```

### NarrativeAdapter
```python
class NarrativeAdapter:
    def format_problem(self, problem):
        story = self._create_story_context(problem)
        return f"📖 {story}: {problem}"
```

## Tests
`tests/test_exercise_adapter.py` (250+ tests)

Test each adapter with multiple exercise types.
Coverage: 85%+
```

---

# 📊 PHASE 7 : Infrastructure & IA

## 7.1 - POSTGRESQL MIGRATION

### Prompt 7.1.1 - PostgreSQL Schema & SQLAlchemy Models

**Titre:** "Créer PostgreSQL schema + SQLAlchemy models pour MathCopain"

**Texte:**

```
# TÂCHE: PostgreSQL Migration

Migrer de JSON → PostgreSQL relational database.
Scalable pour 1000+ concurrent users.

## Fichiers à créer

`database/models.py` (350 lignes) - SQLAlchemy models
`database/connection.py` (150 lignes) - Connection pooling
`database/migrations/env.py` - Alembic environment
`database/migrations/versions/001_initial_schema.py` - Initial migration

## SQL Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    learning_style VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Exercise Responses
CREATE TABLE exercise_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id VARCHAR(100),
    skill_domain VARCHAR(50),
    difficulty_level INTEGER,
    response TEXT,
    is_correct BOOLEAN,
    time_taken_seconds INTEGER,
    strategy_used VARCHAR(100),
    error_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_skill (user_id, skill_domain),
    INDEX idx_created (created_at)
);

-- Skill Profiles
CREATE TABLE skill_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    skill_domain VARCHAR(50),
    proficiency_level FLOAT,
    exercises_completed INTEGER,
    success_rate FLOAT,
    last_practiced TIMESTAMP,
    
    INDEX idx_user (user_id)
);

-- Parent Accounts
CREATE TABLE parent_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pin_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Parent-Child Links
CREATE TABLE parent_child_links (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES parent_accounts(id),
    child_id INTEGER REFERENCES users(id),
    permission_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics Events
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(50),
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_event (user_id, event_type),
    INDEX idx_created (created_at)
);
```

## SQLAlchemy Models

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    pin_hash = Column(String(255), nullable=False)
    learning_style = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    
    exercise_responses = relationship("ExerciseResponse")

class ExerciseResponse(Base):
    __tablename__ = 'exercise_responses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise_id = Column(String(100))
    skill_domain = Column(String(50))
    is_correct = Column(Boolean)
    time_taken_seconds = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

# ... more models
```

## Tests
`tests/test_db_models.py` (300+ tests)

- Model creation
- Relationship validation
- Constraint checking
```

---

### Prompt 7.1.2 - Data Migration Script

**Titre:** "Créer json_to_postgres.py - Migration script sécurisé"

**Texte:**

```
# TÂCHE: Data Migration Script

Migrer données from JSON → PostgreSQL, avec:
- Backup avant migration
- Dry-run mode
- Validation post-migration
- Rollback recovery

## Fichier à créer
`database/migration_scripts/json_to_postgres.py` (250 lignes)

## Features

```python
def migrate_data(source_dir, mode='dry-run'):
    '''
    Modes:
    - 'dry-run': Validate but don't commit
    - 'full': Actually migrate
    '''
    
    # 1. Backup JSON first
    backup_json_files(source_dir)
    
    # 2. Load JSON data
    users = load_json(f"{source_dir}/users_data.json")
    exercises = load_json(f"{source_dir}/exercises_history.json")
    skills = load_json(f"{source_dir}/skill_profiles.json")
    
    # 3. Validate data integrity
    validation_report = validate_data(users, exercises, skills)
    
    if not validation_report['valid']:
        print("❌ Validation failed. Not migrating.")
        return False
    
    # 4. Transform & Insert
    if mode == 'dry-run':
        print("DRY-RUN MODE")
        print(f"Would insert {len(users)} users")
        print(f"Would insert {len(exercises)} exercises")
        return True
    
    elif mode == 'full':
        session = get_session()
        try:
            for user in users:
                db_user = User(...)
                session.add(db_user)
            session.commit()
            print(f"✅ Migrated {len(users)} users successfully")
        except Exception as e:
            session.rollback()
            print(f"❌ Migration failed: {e}")
            restore_from_backup()
```

## Rollback Strategy

If migration fails:
1. JSON backup exists (created before)
2. Restore from backup script
3. Verify recovery

## Tests
`tests/test_migration.py` (300+ tests)

- Dry-run validation
- Data integrity checks
- Rollback recovery
- Performance (>1000 rows)
```

---

## 7.2 - IA ADAPTIVE LEARNING

### Prompt 7.2.1 - DifficultyOptimizer

**Titre:** "Implémenter DifficultyOptimizer - ML pour difficulté optimale"

**Texte:**

```
# TÂCHE: DifficultyOptimizer

Machine Learning model pour:
- Prédire difficulté optimale (D1-D5)
- Maintenir Flow state (70% success rate)
- Expliquer choix (XAI)

## Fichier à créer
`core/ml/difficulty_optimizer.py` (400 lignes)

## Model Type
Gradient Boosting (XGBoost ou LightGBM)

## Features (Input)

```python
features = [
    recent_success_rate,  # Last 10 exercises
    avg_time_taken,
    trend,  # +1 improving, -1 declining
    streak,  # Consecutive successes
    fatigue_level,  # 0-1
    learning_velocity,
    confidence_score,
    hour_of_day_performance,
    day_of_week_performance,
    prerequisite_mastery
]
```

## Output
- Predicted difficulty (1-5 continuous)
- Discretize to D1-D5
- Apply Flow Theory adjustment

## Flow Theory Integration

```python
def apply_flow_adjustment(difficulty, current_success_rate):
    target = 0.70  # 70% optimal for learning
    
    if current_success_rate > target + 0.15:
        difficulty += 1  # Trop facile
    elif current_success_rate < target - 0.15:
        difficulty -= 1  # Trop difficile
    
    return clip(difficulty, 1, 5)
```

## Explainability (XAI)

```python
def explain_difficulty_choice(user_id, difficulty):
    '''
    Retourne: explication humaine de pourquoi D3 par exemple
    "J'ai choisi difficulté 3 car:
    ✓ Tu réussis bien (+75%)
    📈 Tu t'améliores
    😴 Tu fatigues un peu"
    '''
```

## Tests
`tests/test_ml_predictions.py` (300+ tests)

- Model accuracy
- Flow state maintenance
- Edge cases (extreme fatigue, etc.)

## Model Serving
- Train on historical data
- Save as .pkl
- Load in app.py for real-time predictions
```

---

### Prompt 7.2.2 - PerformancePredictor

**Titre:** "Implémenter PerformancePredictor - Ensemble ML"

**Texte:**

```
# TÂCHE: PerformancePredictor

Prédire:
1. Probabilité de succès
2. Identifier élèves à risque (early intervention)
3. Timeline pour maîtriser le domaine

## Fichier à créer
`core/ml/performance_predictor.py` (350 lignes)

## Models
- LSTM (40%) - Time series forecasting
- Random Forest (60%) - At-risk classification

## Ensemble Voting

```python
def predict_success_probability(features):
    lstm_pred = lstm_model.predict(features)  # 0-1
    rf_pred = rf_classifier.predict_proba(features)[1]  # 0-1
    
    ensemble = 0.4 * lstm_pred + 0.6 * rf_pred
    return clip(ensemble, 0, 1)
```

## At-Risk Learner Detection

```python
def identify_at_risk_learners(user_id, horizon_days=7):
    risk_score = calculate_risk_score(user_id, horizon_days)
    return risk_score > 0.6  # 60% threshold
```

## Mastery Timeline Prediction

```python
def predict_mastery_timeline(user_id, domain):
    current_proficiency = get_proficiency(user_id, domain)
    learning_velocity = get_velocity(user_id, domain)
    
    exercises_needed = (1.0 - current_proficiency) / learning_velocity
    days_to_mastery = exercises_needed / 2  # ~2 exercises/day
    
    return {
        "exercises_needed": int(exercises_needed),
        "estimated_days": int(days_to_mastery),
        "confidence": 0.82
    }
```

## Tests
`tests/test_performance_predictor.py` (300+ tests)

- Success probability calibration
- At-risk detection accuracy
- Timeline estimation accuracy
- Fairness across demographics
```

---

# 🎓 PHASE 8 : Déploiement Institutionnel

## 8.1 - MODE ENSEIGNANT & CLASSE

### Prompt 8.1.1 - ClassroomManager Backend

**Titre:** "Implémenter ClassroomManager - Gestion classes pour enseignants"

**Texte:**

```
# TÂCHE: ClassroomManager

Backend pour:
- Créer classes
- Ajouter élèves
- Créer assignments
- Monitorer progression temps réel

## Fichier à créer
`core/pedagogy/classroom_manager.py` (500 lignes)

## Classe ClassroomManager

```python
class ClassroomManager:
    def __init__(self, teacher_id):
        self.teacher_id = teacher_id
        self.db = DatabaseConnection()
    
    def create_classroom(self, name, class_level, max_students=30):
        '''Créer nouvelle classe'''
    
    def add_student_to_classroom(self, classroom_id, student_username):
        '''Ajouter élève'''
    
    def create_assignment(self, classroom_id, title, skill_domains,
                         difficulty, exercise_count, due_date):
        '''Créer et assigner exercices à toute la classe'''
    
    def get_classroom_overview(self, classroom_id):
        '''Real-time stats: student progress, success rates, etc.'''
    
    def generate_competency_report(self, classroom_id):
        '''Export CSV/PDF: qui a maîtrisé quelles compétences?'''
```

## Database Tables (Alembic migrations)

Already defined in 7.1, but integrate with app:
- classrooms
- classroom_enrollments
- assignments
- assignment_responses
- curriculum_competencies
- student_competency_progress

## Real-time Monitoring

```python
def get_classroom_overview(classroom_id):
    students = db.query(classroom_enrollments, classroom_id)
    
    stats = []
    for student in students:
        recent = db.query(exercise_responses,
                         student_id, created_at > 7 days)
        success_rate = sum(1 for e in recent if e.is_correct) / len(recent)
        
        stats.append({
            "student": student.username,
            "recent_success_rate": success_rate,
            "exercises_week": len(recent),
            "current_focus": get_focus_domain(student_id)
        })
    
    return {
        "total_students": len(students),
        "class_avg": mean([s['success_rate'] for s in stats]),
        "student_stats": stats
    }
```

## Tests
`tests/test_classroom_manager.py` (400+ tests)

- Classroom CRUD
- Assignment creation & distribution
- Permission checks
- Real-time metrics accuracy
```

---

### Prompt 8.1.2 - Teacher Dashboard UI

**Titre:** "Créer Teacher Dashboard Streamlit"

**Texte:**

```
# TÂCHE: Teacher Dashboard UI

Streamlit interface pour enseignants.

## Fichier à créer
`ui/teacher_dashboard.py` (400 lignes)

## Layout

### Sidebar
- Classroom selector dropdown
- Navigation menu

### Tabs

**Tab 1: Overview**
- Total students card
- Class avg success rate card
- Weekly activity card
- Student grid table:
  | Nom | Taux Succès | Exercices Semaine | Domaine Actuel |
  |-----|------------|-------------------|-----------------|

**Tab 2: Assignments**
- Create assignment form:
  - Title input
  - Skill domains multiselect
  - Difficulty slider (1-5)
  - Exercise count number input
  - Due date picker
- List of existing assignments

**Tab 3: Students**
- Add student form
- Student list with actions (remove, view detail)
- Individual student progress chart

**Tab 4: Reports**
- Generate buttons:
  - "Générer Rapport Compétences"
  - "Générer Rapport Classe"
  - "Générer Attestations"
- Download buttons for generated files

## UI Code Structure

```python
def render_teacher_dashboard():
    st.set_page_config(page_title="Tableau Bord Enseignant", layout="wide")
    
    # Sidebar
    classroom = st.sidebar.selectbox("Classe", classrooms)
    classroom_id = get_classroom_id(classroom)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Assignments", "Students", "Reports"])
    
    with tab1:
        overview = cm.get_classroom_overview(classroom_id)
        # Display metrics + student grid
    
    with tab2:
        # Create assignment form
    
    # ... etc
```

## Tests
`tests/test_teacher_dashboard.py` (200+ tests)

- UI rendering
- Form submission
- Data validation
- Permission checks
```

---

## 8.2 - ANALYTICS DASHBOARD

### Prompt 8.2.1 - Analytics Engine & Visualizations

**Titre:** "Créer AnalyticsEngine + Plotly visualizations"

**Texte:**

```
# TÂCHE: Analytics Dashboard Engine

Advanced analytics pour insights pédagogiques.

## Fichier à créer
`core/analytics/analytics_engine.py` (500 lignes)

## Visualizations Types

1. **Progress Trajectories** (Line chart)
   - Student proficiency over time
   - By skill domain

2. **Heatmaps** (Skill mastery)
   - Students (rows) × Domains (columns)
   - Color: Red (0%) → Green (100%)

3. **Distributions**
   - Success rate distribution
   - Time taken distribution

4. **Comparative**
   - Student vs class average
   - Domain vs domain

5. **Predictive**
   - Mastery timeline forecast
   - At-risk student forecast

## Analytics Engine

```python
class AnalyticsEngine:
    def generate_progress_trajectory(self, user_id, domain):
        '''Retourne DataFrame avec progres temporelle'''
    
    def generate_skill_heatmap(self, classroom_id):
        '''Retourne heatmap array (students × domains)'''
    
    def generate_comparative_report(self, user_id, classroom_id):
        '''Compare user vs class benchmark'''
    
    def generate_predictive_forecast(self, user_id):
        '''Forecast when mastery achieved'''
```

## Plotly Visualizations

```python
import plotly.graph_objects as go
import plotly.express as px

# Line chart
fig = px.line(df, x='date', y='proficiency',
              title="Progress Trajectory",
              labels={'proficiency': 'Proficiency Level'})

# Heatmap
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=domains,
    y=students,
    colorscale='RdYlGn',
    colorbar=dict(title="Maîtrise")
))

# Export to HTML/image
```

## Tests
`tests/test_analytics.py` (300+ tests)

- Trajectory calculation accuracy
- Heatmap generation
- Comparative metric accuracy
- Forecast validation
```

---

### Prompt 8.2.2 - Dashboard UI & Integration

**Titre:** "Créer Analytics Dashboard Streamlit"

**Texte:**

```
# TÂCHE: Analytics Dashboard UI

Streamlit interface pour visualizer analytics.

## Fichier à créer
`ui/analytics_dashboard.py` (400 lignes)

## Layout

### Filters (Top)
- Time range: [1 week | 1 month | 3 months | All]
- View type: [Student | Class | Domain]
- Domain multiselect

### Tabs

**Tab 1: Trajectories**
- Line charts for each selected domain
- Student proficiency over time

**Tab 2: Heatmaps**
- Skill mastery heatmap
- Students vs Domains

**Tab 3: Comparative**
- Student vs class metrics
- Domain comparison bar charts

**Tab 4: Predictive**
- Mastery timeline forecast
- At-risk student detection

## Streamlit Code

```python
def render_analytics_dashboard():
    st.set_page_config(page_title="Analytics", layout="wide")
    
    # Filters
    time_range = st.selectbox("Period", ["1 week", "1 month", "3 months", "All"])
    view_type = st.selectbox("View", ["Student", "Class", "Domain"])
    domains = st.multiselect("Domains", [...])
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Trajectories", "Heatmaps", "Comparative", "Predictive"])
    
    with tab1:
        for domain in domains:
            df = ae.generate_progress_trajectory(user_id, domain)
            fig = px.line(df, x='date', y='proficiency')
            st.plotly_chart(fig)
    
    # ... etc tabs
```

## Tests
`tests/test_analytics_dashboard.py` (200+ tests)

- Dashboard rendering
- Filter functionality
- Chart generation
- Export functionality
```

---

# 📝 UTILISATION DES PROMPTS

## Pour Chaque Tâche

1. **Copier le prompt** (section "Texte du Prompt")
2. **Aller sur Claude Code**
3. **Coller le prompt entièrement**
4. **Ajouter contexte si besoin**: "Je travaille sur MathCopain, une app Streamlit d'apprentissage maths..."
5. **Laisser Claude Code générer**
6. **Vérifier:**
   - [ ] Code compiles
   - [ ] Tous les tests passent
   - [ ] Coverage 85%+
   - [ ] No console errors
7. **Commit sur git**

## Template de Feedback à Claude Code

Si quelque chose ne marche pas:

```
❌ Erreur: [description]

Fix needed:
1. [Issue]
2. [Context]
3. [What I need]

Je dois avoir:
- [ ] Code qui compile
- [ ] Tests 100% passing
- [ ] Coverage 85%+
```

---

# 🎯 ORDRE D'EXÉCUTION RECOMMANDÉ

**Phase 6 Sequential:**
1. 6.1.1 - ErrorAnalyzer
2. 6.1.2 - error_taxonomy.json
3. 6.1.3 - FeedbackGenerator
4. 6.1.4 - App integration
5. 6.2.1 - MetacognitionEngine
6. 6.3.1 - LearningStyleAnalyzer
7. 6.3.2 - 5 Adapters

**Phase 7 Sequential:**
1. 7.1.1 - PostgreSQL models
2. 7.1.2 - Migration script
3. 7.2.1 - DifficultyOptimizer
4. 7.2.2 - PerformancePredictor

**Phase 8 Sequential:**
1. 8.1.1 - ClassroomManager
2. 8.1.2 - Teacher Dashboard
3. 8.2.1 - Analytics Engine
4. 8.2.2 - Analytics Dashboard

---

**Généré:** 2025-11-15  
**Prompts Totaux:** 15+  
**Coverage Attendu:** 85%+  
**Tests Attendus:** 3,350+

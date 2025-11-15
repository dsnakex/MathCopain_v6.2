# 📋 GUIDE COMPLET - MathCopain Phase 6 → Phase 8
## Stratégie Pédagogique Avancée (Q4 2025 - Q3 2026)

---

## 🎯 VISION GLOBALE

**Transformation** : Application exercices → Système apprentissage personnalisé & bienveillant

**Trois piliers**:
1. Pédagogie centrée sur l'apprenant
2. Équité d'accès et inclusion
3. Infrastructure scalable enterprise

**Timeline** : 9 mois (22 semaines de développement intensif)

---

## 📊 OVERVIEW PHASES

```
Phase 6 (Q4 2025 - Q1 2026) : Fondations Pédagogiques
├─ Feedback Pédagogique Intelligent (6-8 sem)
├─ Métacognition & Autorégulation (4-6 sem)
└─ Profiling Styles Apprentissage (4-6 sem)
   Résultat : Apprenant au centre

Phase 7 (Q2 2026) : Infrastructure & IA
├─ PostgreSQL Migration (8-10 sem)
└─ IA Adaptive Learning (10-12 sem)
   Résultat : Scalabilité + Personnalisation

Phase 8 (Q3 2026) : Déploiement Institutionnel
├─ Mode Enseignant & Classe (12-14 sem)
└─ Dashboard Analytics Complet (8-10 sem)
   Résultat : Intégration scolaire complète
```

---

# 🚀 PHASE 6 : FONDATIONS PÉDAGOGIQUES
## Durée : Q4 2025 - Q1 2026 (14-18 semaines)

---

## ÉTAPE 6.1 : Feedback Pédagogique Intelligent

### Objectif
Transformer feedback basique → explications transformatives qui augmentent l'apprentissage de +35-40%

### Architecture Technique

```
Composants:
├── ErrorAnalyzer (core/pedagogy/)
│   ├── analyze_error_type() → [Conceptual | Calculation | Procedural]
│   ├── identify_misconception() → Common learning errors DB
│   └── root_cause_analysis() → Pourquoi l'erreur?
│
├── FeedbackGenerator (core/pedagogy/)
│   ├── generate_immediate_feedback() → "Voici le problème..."
│   ├── generate_explanation() → Concept deep-dive
│   ├── suggest_alternative_strategy() → "Tu pourrais aussi..."
│   └── generate_encouragement() → Personnalisé par historique
│
├── RemediationRecommender (core/pedagogy/)
│   ├── suggest_similar_problems() → Pratique progressive
│   ├── suggest_prerequisite_review() → "Besoin de revoir..."
│   └── suggest_extension() → "Pour aller plus loin..."
│
└── FeedbackDatabase (data/)
    ├── error_types_taxonomy.json
    ├── misconceptions_db.json
    ├── remediation_paths.json
    └── explanation_templates.json
```

### Modèle de Données

```json
{
  "error_catalog": {
    "addition_carry_error": {
      "type": "procedural",
      "common_in": ["CE1", "CE2"],
      "misconception": "L'enfant oublie la retenue",
      "feedback_templates": [
        "Tu as trouvé {answer}, mais regarde: {breakdown}",
        "Attention à la retenue ici!"
      ],
      "remediation": "addition_with_carry_basics",
      "explanation": "Quand la somme dépasse 10, on met le 1 de côté..."
    }
  },
  "learning_history_profile": {
    "user_id": "pierre",
    "error_patterns": {
      "addition_carry_error": 5,
      "subtraction_borrowing": 2
    },
    "most_effective_explanation_style": "visual_with_example",
    "encouragement_triggers": ["progress_after_failure", "perfect_streak"]
  }
}
```

### Pseudocode Implementation

```python
# core/pedagogy/feedback_engine.py

class TransformativeFeedback:
    def __init__(self):
        self.error_analyzer = ErrorAnalyzer()
        self.feedback_gen = FeedbackGenerator()
        self.remediation = RemediationRecommender()
    
    def process_exercise_response(self, exercise, response, user_id):
        """
        Analyse réponse → Feedback transformatif
        """
        # 1. Vérifier correction
        is_correct = exercise.check_answer(response)
        
        if is_correct:
            return self._generate_success_feedback(exercise, user_id)
        
        # 2. Analyser TYPE d'erreur
        error_analysis = self.error_analyzer.analyze(
            exercise=exercise,
            response=response,
            expected=exercise.correct_answer
        )
        
        # 3. Générer feedback multi-niveaux
        feedback = {
            "immediate": self.feedback_gen.immediate_message(error_analysis),
            "explanation": self.feedback_gen.concept_explanation(
                error_type=error_analysis.type,
                learning_style=self._get_learning_style(user_id)
            ),
            "strategy": self.feedback_gen.alternative_strategy(error_analysis),
            "remediation": self.remediation.recommend_path(error_analysis, user_id),
            "encouragement": self.feedback_gen.encouragement(user_id, error_analysis),
            "next_action": self.remediation.suggest_next(user_id)
        }
        
        # 4. Logger pour analytics
        self._log_learning_moment(user_id, error_analysis, feedback)
        
        return feedback
    
    def _generate_success_feedback(self, exercise, user_id):
        """
        Feedback positif intelligent (pas juste "Bravo!")
        """
        performance = self._calculate_performance_metrics(user_id)
        
        return {
            "immediate": "✅ Exact!",
            "recognition": self._generate_personalized_praise(user_id, performance),
            "insight": f"Tu as résolu ça en {self._get_solve_time()}s (très rapide!)",
            "progression": self._show_progress_trajectory(user_id),
            "next_challenge": self._recommend_next_step(user_id)
        }
    
    def _get_learning_style(self, user_id):
        """
        Récupère style d'apprentissage depuis profil utilisateur
        """
        # TODO: Implémenté en Phase 6.3
        pass
```

### Fichiers à Créer

```
core/pedagogy/
├── __init__.py
├── feedback_engine.py (400 lignes)
├── error_analyzer.py (300 lignes)
├── remediation.py (250 lignes)
└── explanation_templates.py (200 lignes)

data/
├── error_taxonomy.json
├── misconceptions_db.json
├── remediation_paths.json
└── explanation_templates/
    ├── addition.json
    ├── subtraction.json
    ├── multiplication.json
    ├── division.json
    ├── fractions.json
    ├── decimals.json
    ├── geometry.json
    ├── measurements.json
    ├── proportions.json
    └── money.json

tests/
├── test_feedback_engine.py (400+ tests)
├── test_error_analyzer.py (300+ tests)
└── test_remediation.py (250+ tests)
```

### Intégration dans app.py

```python
# Dans la fonction exercise_completed_handler()

from core.pedagogy.feedback_engine import TransformativeFeedback

feedback_engine = TransformativeFeedback()

feedback_response = feedback_engine.process_exercise_response(
    exercise=current_exercise,
    response=user_response,
    user_id=st.session_state.user_id
)

# Affichage multi-couches
with st.container(border=True):
    st.success(feedback_response["immediate"])
    
    with st.expander("📖 Explication"):
        st.write(feedback_response["explanation"])
    
    with st.expander("💡 Stratégie alternative"):
        st.write(feedback_response["strategy"])
    
    if feedback_response["remediation"]:
        with st.info(f"📚 Prochaine étape: {feedback_response['remediation']['title']}"):
            st.write(feedback_response["remediation"]["description"])
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Refaire ce type"):
            # Même compétence, niveau adaptatif
            pass
    with col2:
        if st.button("Continuer"):
            # Avancer
            pass
```

### Checklist Réalisation (Claude Code)

- [ ] Créer `core/pedagogy/feedback_engine.py`
  - [ ] Classe `TransformativeFeedback`
  - [ ] Méthode `process_exercise_response()`
  - [ ] Méthode `_generate_success_feedback()`
  - [ ] Logging analytics
  
- [ ] Créer `core/pedagogy/error_analyzer.py`
  - [ ] Classe `ErrorAnalyzer`
  - [ ] Taxonomie erreurs (6 types minimum)
  - [ ] Detection misconceptions
  - [ ] Root cause analysis
  
- [ ] Créer `core/pedagogy/remediation.py`
  - [ ] Classe `RemediationRecommender`
  - [ ] Paths par compétence
  - [ ] Progression adaptive
  
- [ ] Créer database JSON
  - [ ] `error_taxonomy.json` (500+ erreurs couvertes)
  - [ ] `misconceptions_db.json` (100+ erreurs)
  - [ ] `remediation_paths.json` (par compétence)
  - [ ] Templates explications (complet)
  
- [ ] Intégrer dans `app.py`
  - [ ] Import + instanciation engine
  - [ ] Hook exercise_completed
  - [ ] UI multi-couches
  
- [ ] Tests unitaires
  - [ ] `test_feedback_engine.py` (400+ tests)
  - [ ] `test_error_analyzer.py` (300+ tests)
  - [ ] Coverage cible: 85%+
  
- [ ] Documentation
  - [ ] README pédagogique
  - [ ] Taxonomie erreurs documentée
  - [ ] Exemples avant/après

### Timeline

```
Semaine 1-2 : Architecture design + DB design
Semaine 3-4 : Implémentation ErrorAnalyzer
Semaine 5-6 : Implémentation FeedbackGenerator
Semaine 7-8 : Tests + Intégration app.py
```

### Prompts Claude Code Optimisés

**Prompt 1 - ErrorAnalyzer** :
```
Créer ErrorAnalyzer en Python pour analyser erreurs mathématiques.
Taxonomie: Conceptual (l'enfant n'a pas compris le concept),
Procedural (erreur étape par étape), Calculation (erreur arithmétique).
Pour chaque erreur, retourner: type, misconception (string),
severity (1-5), remediation_path (string).
Utiliser JSON pour taxonomie errors. 500+ errors couvertes.
Tests pytest: 300+ tests couvrant tous types d'erreurs.
```

**Prompt 2 - FeedbackGenerator** :
```
Créer FeedbackGenerator pour générer feedback pédagogiquement transformatif.
Pour une erreur donnée:
1. immediate_feedback: Message court et spécifique
2. explanation: Explique le concept (adapté au learning_style)
3. alternative_strategy: Montre une autre façon de résoudre
4. encouragement: Personnalisé selon historique utilisateur
Utiliser Jinja2 pour templates. Learning styles: visual, auditory, kinesthetic, logical, narrative.
```

**Prompt 3 - Integration** :
```
Intégrer TransformativeFeedback dans app.py Streamlit existant.
Lors du submit d'un exercice:
1. Appeler feedback_engine.process_exercise_response()
2. Afficher feedback en UI multi-couches (expanders)
3. Logger event pour analytics
4. Offrir options: Refaire / Continuer / Voir détails
```

---

## ÉTAPE 6.2 : Métacognition & Autorégulation

### Objectif
Aider l'enfant à **réfléchir à sa réflexion** et ajuster sa stratégie = +40-50% sur autonomie d'apprentissage

### Architecture

```
Composants:
├── MetacognitionEngine (core/pedagogy/)
│   ├── post_exercise_reflection() → Questions réflexives
│   ├── strategy_tracking() → Portfolio stratégies
│   ├── performance_attribution() → "J'ai réussi car..."
│   └── self_regulation_suggestions() → "Prochaine fois..."
│
├── StrategyPortfolio (data/user_profiles/)
│   ├── personal_strategies.json
│   ├── effective_strategies_log.json
│   └── learning_moments.json
│
└── ReflectionUI (ui/)
    ├── post_exercise_reflection_card()
    ├── strategy_portfolio_view()
    └── learning_insights_dashboard()
```

### Modèle Réflexif Post-Exercice

```
┌──────────────────────────────────────────────┐
│        🧠 Moment de Réflexion (30 sec)      │
├──────────────────────────────────────────────┤
│                                              │
│ 1️⃣ Quelle stratégie as-tu utilisée?        │
│    ☐ Compter sur les doigts                │
│    ☐ Visualiser/Dessiner                   │
│    ☐ Utiliser une formule                  │
│    ☐ Décomposer le nombre                  │
│    ☐ Autre: ________________               │
│                                              │
│ 2️⃣ Tu trouves ce type facile, normal ou... │
│    ◐─────●──────◑                          │
│    Facile  Difficile                        │
│                                              │
│ 3️⃣ Que ferais-tu différemment prochain fois?│
│    ┌──────────────────────────────────────┐│
│    │ (optionnel) ______________________   ││
│    └──────────────────────────────────────┘│
│                                              │
│ [Enregistrer Réflexion] [Continuer]        │
└──────────────────────────────────────────────┘

Résultat enregistré:
{
  "exercise_id": "addition_2dig_01",
  "outcome": "success",
  "strategy_used": "decompose_number",
  "difficulty_perception": 0.4,
  "reflection": "J'ai bien décomposé 23 + 14 en 20 + 10 + 3 + 4",
  "next_intention": "Utiliser la même technique pour 35 + 27"
}
```

### Pseudocode Implementation

```python
# core/pedagogy/metacognition.py

class MetacognitionEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        self.strategy_portfolio = self._load_portfolio()
        self.learning_history = self._load_learning_history()
    
    def generate_post_exercise_reflection(self, exercise, outcome, time_taken):
        """
        Génère questions réflexives personalisées
        """
        reflection_questions = {
            "strategy_selection": self._question_strategy(),
            "difficulty_perception": self._question_difficulty(),
            "self_explanation": self._question_self_explanation(exercise, outcome),
            "future_intention": self._question_future_intention(exercise)
        }
        
        return {
            "questions": reflection_questions,
            "hint_if_needed": self._suggest_reflection_hint(exercise)
        }
    
    def process_reflection_response(self, exercise_id, reflection_data):
        """
        Traite réponse réflexive → Portfolio + Insights
        """
        # 1. Enregistrer stratégie
        self.strategy_portfolio.add_strategy(
            exercise_id=exercise_id,
            strategy=reflection_data["strategy_used"],
            effectiveness=reflection_data["outcome"],
            time_taken=reflection_data["time_taken"]
        )
        
        # 2. Analyser patterns
        patterns = self._analyze_patterns()
        
        # 3. Générer insights
        insights = {
            "strength": self._identify_strength(patterns),
            "area_for_growth": self._identify_growth_area(patterns),
            "personalized_advice": self._generate_advice(patterns)
        }
        
        # 4. Enregistrer moment d'apprentissage
        self.learning_history.log_moment(
            exercise_id=exercise_id,
            reflection=reflection_data,
            insights=insights
        )
        
        return insights
    
    def generate_self_regulation_support(self):
        """
        Aide l'enfant à réguler sa session d'apprentissage
        """
        current_performance = self._calculate_current_session_performance()
        
        suggestions = []
        
        if current_performance["frustration_level"] > 0.7:
            suggestions.append({
                "type": "break_suggestion",
                "message": "Tu sembles un peu frustré. Une pause pourrait aider!",
                "action": ["Prendre une pause", "Continuer"]
            })
        
        if current_performance["fatigue_level"] > 0.8:
            suggestions.append({
                "type": "session_end",
                "message": "Beau travail! Tu as fait {X} exercices. Peut-être c'est un bon moment pour arrêter.",
                "action": ["Arrêter", "Un exercice de plus"]
            })
        
        if current_performance["success_streak"] > 5:
            suggestions.append({
                "type": "difficulty_increase",
                "message": "Wow! 5 bons d'affilée. Prêt pour un défi plus difficile?",
                "action": ["Défi Plus Difficile", "Continuer Niveau"]
            })
        
        return suggestions
    
    def generate_portfolio_summary(self):
        """
        Portfolio visuel des stratégies apprises
        """
        return {
            "strategies_mastered": self.strategy_portfolio.get_mastered_strategies(),
            "strategies_developing": self.strategy_portfolio.get_developing_strategies(),
            "learning_trajectory": self._plot_trajectory(),
            "advice_summary": self._generate_personalized_advice()
        }
```

### Fichiers à Créer

```
core/pedagogy/
├── metacognition.py (400 lignes)
└── strategy_portfolio.py (300 lignes)

data/user_profiles/{user_id}/
├── personal_strategies.json
├── learning_history.json
└── reflection_responses.json

ui/
├── metacognition_ui.py (250 lignes)
├── strategy_portfolio_view.py (200 lignes)
└── learning_insights_dashboard.py (200 lignes)

tests/
└── test_metacognition.py (350+ tests)
```

### Checklist Réalisation

- [ ] Créer `core/pedagogy/metacognition.py`
  - [ ] Classe `MetacognitionEngine`
  - [ ] Questions réflexives contextuelles
  - [ ] Pattern analysis
  - [ ] Self-regulation suggestions
  
- [ ] Créer `core/pedagogy/strategy_portfolio.py`
  - [ ] Classe `StrategyPortfolio`
  - [ ] Tracking stratégies par exercice
  - [ ] Effectiveness scoring
  
- [ ] Créer UI components
  - [ ] `post_exercise_reflection_card()` - 30 sec max
  - [ ] `strategy_portfolio_view()` - Visualisation portfolio
  - [ ] `learning_insights()` - Insights personnalisés
  
- [ ] Intégration app.py
  - [ ] Hook après chaque exercice
  - [ ] Affichage reflection 30 sec après
  - [ ] Accès portfolio depuis menu
  
- [ ] Tests
  - [ ] `test_metacognition.py` (350+ tests)
  - [ ] Scénarios: success, failure, frustration, flow
  - [ ] Coverage: 85%+

### Timeline

```
Semaine 1-2 : Design réflexions + data model
Semaine 3-4 : Implémentation MetacognitionEngine
Semaine 5 : Intégration UI
Semaine 6 : Tests + refinement
```

### Prompts Claude Code

**Prompt 1** :
```
Créer MetacognitionEngine pour questions réflexives post-exercice.
Questions:
1. strategy_selection: Quelle stratégie as-tu utilisée?
2. difficulty_perception: Facile/Normal/Difficile (slider)?
3. self_explanation: Explique comment tu as trouvé
4. future_intention: Que ferais-tu la prochaine fois?
Adapter questions selon exercise_type et user's learning history.
Générer insights après réponses: forces, zones croissance.
```

---

## ÉTAPE 6.3 : Profiling Styles d'Apprentissage

### Objectif
Identifier style d'apprentissage de chaque enfant → Adapter présentation des exercices (+25-35% engagement)

### Architecture

```
Composants:
├── LearningStyleQuiz (ui/)
│   └── initial_assessment() → 5-7 questions
│
├── LearningStyleAnalyzer (core/pedagogy/)
│   ├── analyze_responses() → [Visual | Auditory | Kinesthetic | Logical | Narrative]
│   ├── infer_style_from_performance() → Analyse patterns d'exercices
│   └── confidence_scoring() → (0.0-1.0)
│
├── ExerciseAdapter (core/exercise_generator/)
│   ├── adapt_presentation() → Par style
│   ├── suggest_resources() → Visuels/Audio/Interactif
│   └── format_explanation() → Par style
│
└── StyleProfileDatabase (data/)
    └── user_profiles/{user_id}/learning_style.json
```

### Modèle Profil

```json
{
  "user_id": "pierre",
  "learning_style_profile": {
    "primary": {
      "style": "visual",
      "confidence": 0.87,
      "indicators": [
        "Préfère les diagrammes",
        "Successful avec graphiques",
        "Demande 'montrer plutôt que raconter'"
      ]
    },
    "secondary": {
      "style": "kinesthetic",
      "confidence": 0.62,
      "indicators": [
        "Aime manipuler objets",
        "Réussit mieux avec interactif"
      ]
    },
    "assessment_date": "2025-11-15",
    "data_points": 45,
    "confidence_overall": 0.82
  }
}
```

### Quiz Apprentissage (5-7 minutes)

```
Question 1: Quand tu apprends quelque chose de nouveau, tu préfères:
☐ Voir un diagramme / image
☐ Écouter une explication
☐ Essayer toi-même / Manipuler
☐ Comprendre la logique derrière

Question 2: Tes meilleurs souvenirs à l'école?
☐ Les tableaux et les posters
☐ Les histoires racontées par le prof
☐ Les expériences / Les activités
☐ Les mathématiques / La structure

Question 3: Comment tu trouves le chemin vers un endroit?
☐ J'utilise une image mentale
☐ Je m'en souviens par description verbale
☐ Je reviens sur mes pas / Je l'essaye
☐ Je comprends la grille/logique

Question 4: Ton meilleur ami, comment le décris-tu?
☐ Par son apparence
☐ Par sa voix / Ce qu'il dit
☐ Par ses actions / Ce qu'il fait
☐ Par ses qualités / Sa logique

Question 5: Lors des exercices math, tu gagnes la compréhension:
☐ Par diagrammes / Graphiques
☐ Par explications verbales
☐ Par essai/erreur / Manipulations
☐ Par comprendre le "pourquoi"

(Scoring → Profil style)
```

### Pseudocode Implementation

```python
# core/pedagogy/learning_style.py

class LearningStyleAnalyzer:
    STYLES = ["visual", "auditory", "kinesthetic", "logical", "narrative"]
    
    def __init__(self):
        self.quiz_responses = None
        self.performance_data = None
    
    def assess_from_quiz(self, responses: dict) -> dict:
        """
        Analyse réponses quiz → Style d'apprentissage
        """
        style_scores = {style: 0 for style in self.STYLES}
        
        # Scoring quiz
        quiz_weights = {
            "visual": [1, 0, 0, 0, 0],
            "auditory": [0, 1, 0, 0, 0],
            "kinesthetic": [0, 0, 1, 0, 0],
            "logical": [0, 0, 0, 1, 0],
            "narrative": [0, 0, 0, 0, 1]
        }
        
        for question_idx, answer_idx in responses.items():
            for style in self.STYLES:
                style_scores[style] += quiz_weights[style][question_idx]
        
        # Normaliser
        total = sum(style_scores.values())
        normalized_scores = {k: v/total for k, v in style_scores.items()}
        
        return self._rank_styles(normalized_scores, confidence=0.6)
    
    def infer_from_performance(self, performance_history: list) -> dict:
        """
        Inférer style depuis patterns de performance
        """
        patterns = {
            "visual": self._count_visual_success(performance_history),
            "auditory": self._count_auditory_success(performance_history),
            "kinesthetic": self._count_kinesthetic_success(performance_history),
            "logical": self._count_logical_success(performance_history),
            "narrative": self._count_narrative_success(performance_history)
        }
        
        return self._rank_styles(patterns, confidence=0.7)
    
    def combine_assessments(self, quiz_result: dict, performance_result: dict) -> dict:
        """
        Combine quiz + inférence performance
        """
        combined = {}
        for style in self.STYLES:
            # Average weighted
            combined[style] = (
                quiz_result[style] * 0.4 +
                performance_result[style] * 0.6
            )
        
        primary, secondary = self._rank_styles(combined, top_n=2)
        
        return {
            "primary": primary,
            "secondary": secondary,
            "overall_confidence": self._calculate_confidence(combined),
            "recommendation": self._generate_recommendation(primary, secondary)
        }

# core/exercise_generator.py - Extension

class ExercisePresenterAdapter:
    def __init__(self, learning_style: str):
        self.style = learning_style
        self.adapters = {
            "visual": VisualAdapter(),
            "auditory": AuditoryAdapter(),
            "kinesthetic": KinestheticAdapter(),
            "logical": LogicalAdapter(),
            "narrative": NarrativeAdapter()
        }
    
    def adapt_exercise(self, exercise: dict) -> dict:
        """
        Adapte présentation d'un exercice selon learning style
        """
        adapter = self.adapters[self.style]
        
        adapted = {
            "problem_statement": adapter.format_problem(exercise["problem"]),
            "hint": adapter.format_hint(exercise["hint"]),
            "visual_aids": adapter.generate_visuals(exercise),
            "explanation_style": adapter.get_explanation_style(),
            "resource_suggestion": adapter.suggest_resources()
        }
        
        return adapted

# Adapters

class VisualAdapter:
    def format_problem(self, problem):
        return f"📊 Visualise: {problem}"
    
    def format_hint(self, hint):
        return f"🎨 Dessine: {hint}"
    
    def generate_visuals(self, exercise):
        return {
            "diagram": self._create_diagram(exercise),
            "number_line": self._create_number_line(exercise),
            "color_coding": self._apply_color_coding(exercise)
        }

class AuditoryAdapter:
    def format_problem(self, problem):
        return f"🎵 Écoute: {problem}"
    
    def suggest_resources(self):
        return {"type": "audio", "url": "audio_explanation.mp3"}

class KinestheticAdapter:
    def format_problem(self, problem):
        return f"👆 Manipule: {problem}"
    
    def generate_visuals(self, exercise):
        return {"interactive_manipulatives": "draggable_blocks"}

class LogicalAdapter:
    def format_problem(self, problem):
        return f"🧠 Comprends la logique: {problem}"
    
    def format_hint(self, hint):
        return f"Pourquoi? {hint}"

class NarrativeAdapter:
    def format_problem(self, problem):
        story_context = self._create_story_context(problem)
        return f"📖 {story_context}: {problem}"
```

### Fichiers à Créer

```
core/pedagogy/
├── learning_style.py (350 lignes)
└── style_profile_manager.py (200 lignes)

core/exercise_generator/
├── exercise_adapter.py (400 lignes)
├── adapters/
│   ├── visual_adapter.py (150 lignes)
│   ├── auditory_adapter.py (100 lignes)
│   ├── kinesthetic_adapter.py (150 lignes)
│   ├── logical_adapter.py (100 lignes)
│   └── narrative_adapter.py (150 lignes)

ui/
└── learning_style_assessment.py (200 lignes)

tests/
├── test_learning_style.py (300+ tests)
└── test_exercise_adapter.py (250+ tests)
```

### Checklist Réalisation

- [ ] Créer `core/pedagogy/learning_style.py`
  - [ ] Classe `LearningStyleAnalyzer`
  - [ ] `assess_from_quiz()` - 5 styles
  - [ ] `infer_from_performance()` - Pattern matching
  - [ ] `combine_assessments()` - Quiz + performance
  
- [ ] Créer adapters
  - [ ] `VisualAdapter` - Diagrammes, graphiques
  - [ ] `AuditoryAdapter` - Audio, descriptions
  - [ ] `KinestheticAdapter` - Interactif, manipulables
  - [ ] `LogicalAdapter` - Explications causales
  - [ ] `NarrativeAdapter` - Contextes historiques
  
- [ ] Créer `ui/learning_style_assessment.py`
  - [ ] Quiz 5-7 minutes
  - [ ] Streamlit UI
  - [ ] Résultats + recommendations
  
- [ ] Intégration app.py
  - [ ] Premier launch: quiz obligatoire
  - [ ] Load learning_style in session
  - [ ] Passer à ExerciseAdapter
  
- [ ] Tests
  - [ ] `test_learning_style.py` (300+ tests)
  - [ ] `test_exercise_adapter.py` (250+ tests)
  - [ ] A/B testing: avec/sans adaptation
  
- [ ] Documentation
  - [ ] Validation scientifique (références)
  - [ ] Guide adaptation par style

### Timeline

```
Semaine 1-2 : Design quiz + style profiles
Semaine 3-4 : Implémentation LearningStyleAnalyzer
Semaine 5-6 : Implémentation adapters (5)
Semaine 7 : Intégration + A/B testing
```

### Prompts Claude Code

**Prompt 1** :
```
Créer LearningStyleAnalyzer pour identifier 5 styles:
Visual, Auditory, Kinesthetic, Logical, Narrative.
Quiz 5-7 questions. Inférer aussi depuis performance patterns.
Combiner Quiz (40%) + Performance (60%).
Retourner: primary style, secondary style, confidence (0.0-1.0).
```

**Prompt 2** :
```
Créer 5 ExerciseAdapter pour adapter présentation selon style.
Visual: Add diagrams, number lines, color coding
Auditory: Add audio descriptions, rhythm
Kinesthetic: Make interactive, draggable
Logical: Emphasize "pourquoi", causal chains
Narrative: Add story context, real-world scenarios
```

---

# 📊 PHASE 7 : INFRASTRUCTURE & IA
## Durée : Q2 2026 (18-22 semaines)

---

## ÉTAPE 7.1 : PostgreSQL Migration

### Objectif
Migration JSON → PostgreSQL = Scalabilité 10x, requêtes complexes, analytics

### Architecture

```
Avant (JSON):
├── users_data.json (1 fichier)
├── exercises_history.json (1 fichier)
└── skill_profiles.json (1 fichier)
Limitations: Querys complexes impossibles, slow à >1000 users

Après (PostgreSQL):
├── Schema ACID complet
├── Normalization 3NF
├── Indexes optimisés
├── Connection pooling
└── Replication ready
```

### Schema Proposé

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,  -- bcrypt
    learning_style VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Learning Sessions
CREATE TABLE learning_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_date DATE,
    duration_minutes INTEGER,
    exercises_count INTEGER,
    success_rate FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Exercise Responses
CREATE TABLE exercise_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id VARCHAR(100),
    skill_domain VARCHAR(50),  -- addition, subtraction, etc.
    difficulty_level INTEGER,  -- 1-5
    response TEXT,
    is_correct BOOLEAN,
    time_taken_seconds INTEGER,
    strategy_used VARCHAR(100),
    error_type VARCHAR(50),
    feedback_given TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_skill (user_id, skill_domain),
    INDEX idx_created (created_at)
);

-- Skill Profiles
CREATE TABLE skill_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    skill_domain VARCHAR(50),
    proficiency_level FLOAT,  -- 0.0-1.0
    exercises_completed INTEGER,
    success_rate FLOAT,
    last_practiced TIMESTAMP,
    
    INDEX idx_user (user_id)
);

-- Parent Accounts (pour Phase 8)
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
    permission_level VARCHAR(20),  -- view, manage, admin
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics Events
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(50),  -- login, exercise_completed, error_detected
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_event (user_id, event_type),
    INDEX idx_created (created_at)
);
```

### Migration Strategy

```
Phase 1 (Week 1-2): Environment Setup
├─ PostgreSQL local + RDS (AWS)
├─ Docker Compose
├─ Connection pooling (pgBouncer)
└─ Backup strategy

Phase 2 (Week 3-4): Schema Creation
├─ SQL schema definition
├─ Migrations (Alembic)
├─ Indexes
└─ Initial fixtures

Phase 3 (Week 5-6): Data Migration
├─ JSON → PostgreSQL scripts
├─ Data validation
├─ Duplicate check
├─ Backup pre-migration
└─ Dry-run first

Phase 4 (Week 7-8): ORM Integration
├─ SQLAlchemy models
├─ Query refactoring
├─ Connection pooling
└─ Transaction management

Phase 5 (Week 9-10): Testing & Optimization
├─ Performance tests
├─ Load testing
├─ Query optimization
├─ Connection pool tuning
└─ Production readiness
```

### Pseudocode (Alembic Migrations)

```python
# migrations/versions/001_initial_schema.py

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('pin_hash', sa.String(255), nullable=False),
        sa.Column('learning_style', sa.String(20)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    # ... more tables

def downgrade():
    op.drop_table('users')
    # ...

# models.py (SQLAlchemy)

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    pin_hash = Column(String(255), nullable=False)
    learning_style = Column(String(20))
    created_at = Column(DateTime, server_default=sa.func.now())
    
    exercise_responses = relationship("ExerciseResponse", back_populates="user")
    skill_profiles = relationship("SkillProfile", back_populates="user")

class ExerciseResponse(Base):
    __tablename__ = 'exercise_responses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exercise_id = Column(String(100))
    skill_domain = Column(String(50))
    is_correct = Column(Boolean)
    time_taken_seconds = Column(Integer)
    strategy_used = Column(String(100))
    error_type = Column(String(50))
    created_at = Column(DateTime, server_default=sa.func.now())
    
    user = relationship("User", back_populates="exercise_responses")

# Migration script: json_to_postgres.py

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, ExerciseResponse, SkillProfile

def migrate_from_json():
    # Setup DB
    engine = create_engine('postgresql://user:pass@localhost/mathcopain')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Load JSON data
    with open('data/users_data.json') as f:
        users_data = json.load(f)
    
    # Migrate users
    for username, user_info in users_data.items():
        user = User(
            username=username,
            pin_hash=user_info['pin'],  # Already bcrypt from v6.3
            learning_style=user_info.get('learning_style')
        )
        session.add(user)
    
    session.commit()
    print(f"✅ Migrated {len(users_data)} users to PostgreSQL")
```

### Fichiers à Créer

```
infrastructure/
├── docker-compose.yml (PostgreSQL + pgAdmin)
├── postgresql.conf (Tuning)
└── backup_strategy.sh

database/
├── models.py (SQLAlchemy models)
├── connection.py (Pool management)
├── migrations/
│   ├── env.py
│   └── versions/
│       ├── 001_initial_schema.py
│       └── 002_add_analytics.py
└── migration_scripts/
    ├── json_to_postgres.py
    ├── data_validation.py
    └── rollback_recovery.py

tests/
├── test_db_models.py
├── test_migration.py
└── test_db_performance.py

docs/
└── POSTGRES_MIGRATION.md
```

### Checklist Réalisation

- [ ] PostgreSQL Setup
  - [ ] Local installation (Homebrew/apt)
  - [ ] Docker Compose config
  - [ ] Connection pooling (pgBouncer)
  - [ ] Backup strategy
  
- [ ] Schema Design
  - [ ] Create SQL schema
  - [ ] Normalization review
  - [ ] Index optimization
  - [ ] Review with team
  
- [ ] Alembic Setup
  - [ ] Initialize Alembic
  - [ ] Create initial migration
  - [ ] Test upgrade/downgrade
  
- [ ] Data Migration
  - [ ] Write `json_to_postgres.py`
  - [ ] Data validation script
  - [ ] Dry-run migration
  - [ ] Backup JSON before migration
  - [ ] Run actual migration
  - [ ] Verify data integrity
  
- [ ] ORM Integration
  - [ ] Create SQLAlchemy models
  - [ ] Refactor existing queries
  - [ ] Connection pooling
  - [ ] Transaction management
  
- [ ] Testing
  - [ ] Unit tests (models)
  - [ ] Integration tests (queries)
  - [ ] Performance tests
  - [ ] Load tests (>1000 concurrent users)
  
- [ ] Deployment
  - [ ] RDS setup (AWS)
  - [ ] Connection parameters
  - [ ] Monitoring (CloudWatch)
  - [ ] Backup automated

### Timeline

```
Semaine 1-2 : Environment + Schema
Semaine 3-4 : Migration scripts
Semaine 5-6 : Data migration + validation
Semaine 7-8 : ORM integration
Semaine 9-10 : Testing + production setup
```

### Prompts Claude Code

**Prompt 1** :
```
Créer PostgreSQL schema pour MathCopain.
Tables: users, exercise_responses, skill_profiles, parent_accounts, analytics_events.
Normalization 3NF. Indexes sur user_id, skill_domain, created_at.
Foreign keys. Timestamped audit columns.
Comment sur chaque table.
```

**Prompt 2** :
```
Créer Alembic migration + SQLAlchemy models.
Initial schema migration. Models pour each table.
Relationships entre tables. Tests pour migration upgrade/downgrade.
```

**Prompt 3** :
```
Créer json_to_postgres.py migration script.
Load users_data.json, exercises_history.json, skill_profiles.json.
Transform → PostgreSQL schema. Data validation.
Dry-run mode. Rollback recovery. Before/after verification.
```

---

## ÉTAPE 7.2 : IA Adaptive Learning

### Objectif
Machine Learning pour difficulté optimale + prédictions précoces + identification lacunes

### Architecture

```
ML Components:
├── DifficultyOptimizer (core/ml/)
│   ├── predict_optimal_difficulty() → Difficulty D₁-D₅
│   ├── flow_theory_algorithm() → Csikszentmihalyi balance
│   └── adaptive_scheduler() → Next exercise timing
│
├── PerformancePredictor (core/ml/)
│   ├── predict_success_probability() → P(success | history)
│   ├── identify_at_risk_learners() → Early intervention
│   └── predict_mastery_timeline() → "In X exercises..."
│
├── LacunaDetector (core/ml/)
│   ├── identify_conceptual_gaps() → "Besoin revoir..."
│   ├── prerequisite_checker() → "D'abord maîtriser..."
│   └── knowledge_map() → Graph dépendances
│
└── ExplainableAI (core/ml/)
    ├── explain_difficulty_choice() → "Pourquoi D3?"
    ├── explain_prediction() → "Tu réussissas car..."
    └── confidence_intervals() → Incertitude modèle
```

### Algorithme Flow Theory (Csikszentmihalyi)

```
Challenge Level vs Skill Level

5  │     Anxiety           Flow Channel         Anxiety
   │       ↗             ↗───────────→            ↗
   │      ↗             ↗ (Optimal Zone)         ↗
Difficulty
   │ Boredom ← ← ← ←   Apathy      ← ← ← Anxiety
   │
   └────────────────────────────────────────────
       Low              Skill Level              High

Formule:
difficulty_score = base_difficulty + adjustment

adjustment = (success_rate - target_success_rate) * sensitivity_factor

Cible: success_rate = 70% (optimale pour apprentissage + motivation)
```

### Modèle Machine Learning Proposé

```
Input Features:
├── Performance History
│   ├── Last 10 exercises success rate
│   ├── Time trends (improving/declining?)
│   ├── Skill domain specific performance
│   └── Time of day effects
│
├── User Profile
│   ├── Learning style
│   ├── Metacognitive patterns
│   ├── Stress/Frustration levels
│   └── Session history
│
└── Exercise Features
    ├── Skill domain
    ├── Current difficulty
    ├── Prerequisite skills
    └── Time estimate

Output Predictions:
├── Next exercise difficulty (D₁-D₅)
├── Success probability (0.0-1.0)
├── Estimated time (seconds)
└── Confidence interval (±error)

Model Architecture:
├── Gradient Boosting (XGBoost/LightGBM) for difficulty prediction
├── Neural Network (LSTM) for time series trend
├── Random Forest for prerequisite gaps
└── Ensemble voting for final prediction
```

### Pseudocode Implementation

```python
# core/ml/difficulty_optimizer.py

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

class DifficultyOptimizer:
    def __init__(self):
        self.flow_target_success_rate = 0.70  # 70% success optimal
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=5
        )
        self.scaler = StandardScaler()
    
    def extract_features(self, user_id: str, exercise_domain: str) -> np.ndarray:
        """
        Extract features for user + domain
        """
        # Historical performance
        recent_performance = self._get_recent_performance(user_id, exercise_domain)
        
        features = np.array([
            recent_performance['success_rate'],
            recent_performance['avg_time_seconds'],
            recent_performance['trend'],  # +1 improving, -1 declining
            recent_performance['last_n_streak'],  # Consecutive successes
            
            # Learning patterns
            self._get_fatigue_level(user_id),
            self._get_learning_velocity(user_id),
            self._get_confidence_score(user_id),
            
            # Time-based
            self._get_hour_of_day_performance(user_id),
            self._get_day_of_week_performance(user_id),
            
            # Domain specific
            self._get_prerequisite_mastery(user_id, exercise_domain),
        ])
        
        return self.scaler.transform(features.reshape(1, -1))[0]
    
    def predict_optimal_difficulty(self, user_id: str, exercise_domain: str) -> int:
        """
        Prédire difficulté optimale (1-5)
        """
        # Extraction features
        features = self.extract_features(user_id, exercise_domain)
        
        # Prédire difficulté brute (continue)
        predicted_difficulty_continuous = self.model.predict([features])[0]
        
        # Discrétiser 1-5
        difficulty_level = np.clip(
            int(np.round(predicted_difficulty_continuous)),
            1, 5
        )
        
        # Appliquer Flow Theory adjustment
        current_success_rate = self._get_recent_success_rate(user_id, exercise_domain)
        
        if current_success_rate > self.flow_target_success_rate + 0.15:
            # Trop facile → Augmenter difficulté
            difficulty_level = min(difficulty_level + 1, 5)
        elif current_success_rate < self.flow_target_success_rate - 0.15:
            # Trop difficile → Diminuer difficulté
            difficulty_level = max(difficulty_level - 1, 1)
        
        return difficulty_level
    
    def explain_difficulty_choice(self, user_id: str, exercise_domain: str, difficulty: int) -> str:
        """
        Explication humaine de choix difficulté (Explainable AI)
        """
        factors = self._analyze_contributing_factors(user_id, exercise_domain)
        
        explanation = f"J'ai choisi difficulté {difficulty} car:\n"
        
        if factors['success_rate'] > 0.75:
            explanation += "✓ Tu réussis bien (+75%) → Un peu plus difficile\n"
        elif factors['success_rate'] < 0.50:
            explanation += "⚠ Tu galères un peu (<50%) → Easier first\n"
        
        if factors['trend'] == 'improving':
            explanation += "📈 Tu t'améliores → Go harder!\n"
        elif factors['trend'] == 'declining':
            explanation += "📉 Tu fatigues → Take a break\n"
        
        if factors['fatigue'] > 0.7:
            explanation += "😴 Tu fatigues → Plus simple pour rester motivé\n"
        
        return explanation

# core/ml/performance_predictor.py

class PerformancePredictor:
    def __init__(self):
        self.lstm_model = LSTMPredictor()  # Time series
        self.risk_classifier = RandomForestClassifier()  # At-risk detection
    
    def predict_success_probability(self, user_id: str, exercise_domain: str) -> float:
        """
        Probabilité de succès pour exercice
        """
        features = self._extract_prediction_features(user_id, exercise_domain)
        
        # Predict using ensemble
        probability = (
            self.lstm_model.predict(features) * 0.4 +
            self.risk_classifier.predict_proba(features)[1] * 0.6
        )
        
        return np.clip(probability, 0.0, 1.0)
    
    def identify_at_risk_learners(self, user_id: str, horizon_days: int = 7) -> bool:
        """
        Identifier apprenants à risque (abandon probable)
        """
        risk_score = self._calculate_risk_score(user_id, horizon_days)
        
        # Threshold: 0.6 = 60% risque d'abandon
        return risk_score > 0.6
    
    def predict_mastery_timeline(self, user_id: str, exercise_domain: str) -> dict:
        """
        Quand l'enfant maîtrisera le domaine?
        """
        current_proficiency = self._get_proficiency_level(user_id, exercise_domain)
        learning_velocity = self._get_learning_velocity(user_id, exercise_domain)
        
        exercises_needed = max(0, (1.0 - current_proficiency) / learning_velocity)
        
        return {
            "current_proficiency": current_proficiency,
            "exercises_needed": int(exercises_needed),
            "estimated_days": int(exercises_needed / 2),  # ~2 exercises/day
            "confidence": self._calculate_prediction_confidence()
        }

# core/ml/explainable_ai.py

class ExplainableAI:
    """
    XAI: Rendre les prédictions ML compréhensibles aux users
    """
    
    def explain_prediction(self, user_id: str, prediction: dict) -> str:
        """
        Explication humaine des prédictions
        """
        explanation = f"""
🧠 Voici pourquoi j'ai prédit ça:

Succès probable: {prediction['success_probability']:.0%}
├─ Tu as réussi {prediction['recent_success_rate']:.0%} récemment
├─ Tu t'améliores? {prediction['trend']}
└─ Ce domaine? {prediction['domain_confidence']:.0%} confiance

Conseil: {self._generate_personalized_advice(prediction)}
        """
        return explanation
    
    def generate_confidence_intervals(self, prediction: float) -> dict:
        """
        Incertitude de la prédiction (±interval)
        """
        base_uncertainty = 0.1
        
        confidence_interval = {
            "lower_bound": max(0.0, prediction - base_uncertainty),
            "upper_bound": min(1.0, prediction + base_uncertainty),
            "confidence_level": "Moyenne" if base_uncertainty > 0.15 else "Haute"
        }
        
        return confidence_interval
```

### Fichiers à Créer

```
core/ml/
├── __init__.py
├── difficulty_optimizer.py (400 lignes)
├── performance_predictor.py (350 lignes)
├── lacuna_detector.py (300 lignes)
├── explainable_ai.py (250 lignes)
├── models/
│   ├── difficulty_model.pkl (Trained GB)
│   ├── lstm_model.h5 (LSTM weights)
│   └── risk_classifier.pkl (RF)
└── training/
    ├── train_difficulty_model.py
    ├── train_lstm_model.py
    ├── train_risk_classifier.py
    ├── evaluation_metrics.py
    └── training_data/

tests/
├── test_ml_predictions.py (400+ tests)
├── test_explainable_ai.py (200+ tests)
└── test_ml_performance.py (Benchmark tests)

notebooks/
├── ML_Model_Development.ipynb
├── Model_Evaluation.ipynb
└── Feature_Importance.ipynb
```

### Checklist Réalisation

- [ ] Feature Engineering
  - [ ] Historical performance features
  - [ ] Learning pattern features
  - [ ] Domain-specific features
  - [ ] Time-based features
  
- [ ] Model Development
  - [ ] Difficulty Predictor (Gradient Boosting)
  - [ ] Success Probability (Ensemble LSTM + RF)
  - [ ] Risk Classifier (Random Forest)
  - [ ] Lacuna Detector (Graph-based)
  
- [ ] Training & Evaluation
  - [ ] Collect training data
  - [ ] 80/20 train/test split
  - [ ] Cross-validation
  - [ ] Hyperparameter tuning
  - [ ] Metrics: MAE, Precision, Recall, F1
  
- [ ] Explainability
  - [ ] SHAP values for feature importance
  - [ ] Generate human-readable explanations
  - [ ] Confidence intervals
  - [ ] Uncertainty quantification
  
- [ ] Ethical Review
  - [ ] Bias detection (by gender, demographics)
  - [ ] Fairness audit
  - [ ] False positive/negative analysis
  - [ ] Mitigation strategies
  
- [ ] Integration
  - [ ] Load models in app.py
  - [ ] Real-time predictions
  - [ ] Model serving infrastructure
  - [ ] Fallback mechanisms
  
- [ ] Monitoring
  - [ ] Model performance drift
  - [ ] Prediction accuracy tracking
  - [ ] Retraining schedule
  - [ ] A/B testing: with/without AI

### Timeline

```
Semaine 1-2 : Feature engineering
Semaine 3-4 : Model training + evaluation
Semaine 5-6 : Hyperparameter tuning
Semaine 7-8 : Explainability + ethics review
Semaine 9-10 : Integration + monitoring
Semaine 11-12 : A/B testing + deployment
```

### Prompts Claude Code

**Prompt 1** :
```
Créer DifficultyOptimizer utilisant Gradient Boosting.
Input features: recent performance, learning velocity, fatigue, time-of-day.
Output: Difficulty 1-5.
Intégrer Flow Theory (Csikszentmihalyi): target success_rate = 70%.
Provide explain_difficulty_choice() pour XAI.
```

**Prompt 2** :
```
Créer PerformancePredictor pour:
1. Predict success probability (0.0-1.0)
2. Identify at-risk learners (risk_score > 0.6)
3. Predict mastery timeline (exercises needed, estimated days)
Ensemble: LSTM 40% + RandomForest 60%.
A/B testable pour validation.
```

**Prompt 3** :
```
Créer ExplainableAI pour rendre prédictions ML compréhensibles.
- explain_prediction(): Pourquoi j'ai prédit ça?
- generate_confidence_intervals(): Incertitude ±
- SHAP values: Feature importance
- Humain-readable explanations pour users
```

---

# 🎓 PHASE 8 : DÉPLOIEMENT INSTITUTIONNEL
## Durée : Q3 2026 (20-24 semaines)

---

## ÉTAPE 8.1 : Mode Enseignant & Classe

### Objectif
Déploiement scolaire : Enseignants gèrent classes, assignent exercices, voient progression en temps réel

### Architecture

```
Composants:
├── TeacherAuthentication (core/security/)
│   └── teacher_login_flow()
│
├── ClassroomManager (core/pedagogy/)
│   ├── create_classroom()
│   ├── add_students()
│   ├── create_assignment()
│   └── monitor_progress()
│
├── TeacherDashboard (ui/)
│   ├── class_overview()
│   ├── student_detail_view()
│   ├── real_time_monitoring()
│   └── report_generation()
│
├── CurriculumAlignment (data/)
│   ├── EN_competences.json (Éducation Nationale)
│   └── mapping_exercises_to_competences.json
│
└── TeacherAPI (api/)
    ├── /api/classroom/{id}/students
    ├── /api/classroom/{id}/assignments
    └── /api/reporting/export
```

### Base de Données Complémentaire

```sql
-- Teacher Accounts
CREATE TABLE teacher_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pin_hash VARCHAR(255),
    school_name VARCHAR(200),
    class_level VARCHAR(20),  -- CE1, CE2, CM1, CM2
    created_at TIMESTAMP DEFAULT NOW()
);

-- Classrooms
CREATE TABLE classrooms (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES teacher_accounts(id),
    classroom_name VARCHAR(100),
    class_level VARCHAR(20),
    description TEXT,
    school_year VARCHAR(10),  -- 2025-2026
    max_students INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Classroom Enrollments
CREATE TABLE classroom_enrollments (
    id SERIAL PRIMARY KEY,
    classroom_id INTEGER REFERENCES classrooms(id),
    student_id INTEGER REFERENCES users(id),
    enrollment_date TIMESTAMP DEFAULT NOW(),
    role VARCHAR(20)  -- student
);

-- Assignments
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    classroom_id INTEGER REFERENCES classrooms(id),
    title VARCHAR(200),
    description TEXT,
    skill_domains VARCHAR(500),  -- JSON array
    difficulty_level INTEGER,
    exercise_count INTEGER,
    due_date TIMESTAMP,
    created_by INTEGER REFERENCES teacher_accounts(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Assignment Responses (Student work)
CREATE TABLE assignment_responses (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id),
    student_id INTEGER REFERENCES users(id),
    submitted_at TIMESTAMP,
    completion_percentage FLOAT,
    score FLOAT,
    teacher_feedback TEXT,
    graded_at TIMESTAMP,
    graded_by INTEGER REFERENCES teacher_accounts(id)
);

-- Curriculum Competencies
CREATE TABLE curriculum_competencies (
    id SERIAL PRIMARY KEY,
    class_level VARCHAR(20),  -- CE1, CE2, CM1, CM2
    domain VARCHAR(50),  -- addition, subtraction, etc.
    competency_code VARCHAR(20),  -- EN.CE1.CALC.01
    competency_name VARCHAR(200),
    description TEXT,
    bloom_level VARCHAR(20),  -- Knowledge, Comprehension, Application...
    assessment_criteria TEXT
);

-- Student Competency Tracking
CREATE TABLE student_competency_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    competency_id INTEGER REFERENCES curriculum_competencies(id),
    progress_level VARCHAR(20),  -- not_started, in_progress, mastered
    exercises_completed INTEGER,
    last_practiced TIMESTAMP,
    teacher_notes TEXT
);
```

### Pseudocode Implementation

```python
# core/pedagogy/classroom_manager.py

class ClassroomManager:
    def __init__(self, teacher_id):
        self.teacher_id = teacher_id
        self.db = DatabaseConnection()
    
    def create_classroom(self, name: str, class_level: str, max_students: int = 30) -> int:
        """
        Créer nouvelle classe
        """
        classroom = {
            "teacher_id": self.teacher_id,
            "classroom_name": name,
            "class_level": class_level,
            "max_students": max_students,
            "school_year": "2025-2026"
        }
        
        classroom_id = self.db.insert("classrooms", classroom)
        return classroom_id
    
    def add_student_to_classroom(self, classroom_id: int, student_username: str) -> bool:
        """
        Ajouter élève à classe
        """
        student = self.db.query_one("users", {"username": student_username})
        
        if not student:
            raise ValueError(f"Student {student_username} not found")
        
        enrollment = {
            "classroom_id": classroom_id,
            "student_id": student['id'],
            "role": "student"
        }
        
        self.db.insert("classroom_enrollments", enrollment)
        return True
    
    def create_assignment(self, classroom_id: int, title: str, 
                         skill_domains: list, difficulty: int, 
                         exercise_count: int, due_date: str) -> int:
        """
        Créer assignation pour classe
        """
        assignment = {
            "classroom_id": classroom_id,
            "title": title,
            "skill_domains": json.dumps(skill_domains),
            "difficulty_level": difficulty,
            "exercise_count": exercise_count,
            "due_date": due_date,
            "created_by": self.teacher_id
        }
        
        assignment_id = self.db.insert("assignments", assignment)
        
        # Auto-assign to all students in classroom
        self._assign_to_all_students(classroom_id, assignment_id)
        
        return assignment_id
    
    def get_classroom_overview(self, classroom_id: int) -> dict:
        """
        Overview classe en temps réel
        """
        classroom = self.db.query_one("classrooms", {"id": classroom_id})
        students = self.db.query("classroom_enrollments", {"classroom_id": classroom_id})
        
        student_stats = []
        for enrollment in students:
            student_id = enrollment['student_id']
            
            # Fetch student's performance
            recent_exercises = self.db.query(
                "exercise_responses",
                {"user_id": student_id, "created_at": "> NOW() - INTERVAL 7 days"}
            )
            
            success_rate = sum(1 for ex in recent_exercises if ex['is_correct']) / len(recent_exercises) if recent_exercises else 0.0
            
            student_stats.append({
                "student_id": student_id,
                "username": self.db.query_one("users", {"id": student_id})['username'],
                "recent_success_rate": success_rate,
                "exercises_this_week": len(recent_exercises),
                "current_focus_domain": self._get_current_focus(student_id)
            })
        
        return {
            "classroom": classroom,
            "total_students": len(students),
            "student_stats": student_stats,
            "class_average_success_rate": np.mean([s['recent_success_rate'] for s in student_stats])
        }

# ui/teacher_dashboard.py

import streamlit as st
import pandas as pd
from core.pedagogy.classroom_manager import ClassroomManager

def render_teacher_dashboard():
    st.set_page_config(page_title="Tableau de Bord Enseignant", layout="wide")
    
    # Sidebar: Class selection
    teacher_id = st.session_state.get('teacher_id')
    cm = ClassroomManager(teacher_id)
    
    classrooms = cm.get_my_classrooms()
    selected_classroom = st.sidebar.selectbox(
        "Sélectionner classe",
        [c['classroom_name'] for c in classrooms]
    )
    
    classroom_id = next(c['id'] for c in classrooms if c['classroom_name'] == selected_classroom)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Aperçu",
        "📋 Assignations",
        "👥 Élèves",
        "📈 Rapports"
    ])
    
    with tab1:
        # Real-time class overview
        overview = cm.get_classroom_overview(classroom_id)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Élèves", overview['total_students'])
        col2.metric("Succès moyen classe", f"{overview['class_average_success_rate']:.0%}")
        col3.metric("Activité cette semaine", f"{sum(s['exercises_this_week'] for s in overview['student_stats'])} exercices")
        
        # Student grid
        st.subheader("Progression des Élèves")
        
        df_students = pd.DataFrame([
            {
                "Nom": s['username'],
                "Taux Succès": f"{s['recent_success_rate']:.0%}",
                "Exercices Semaine": s['exercises_this_week'],
                "Domaine Actuel": s['current_focus_domain']
            }
            for s in overview['student_stats']
        ])
        
        st.dataframe(df_students, use_container_width=True)
    
    with tab2:
        # Manage assignments
        st.subheader("Créer Assignation")
        
        col1, col2 = st.columns(2)
        with col1:
            assignment_title = st.text_input("Titre assignation")
            skill_domains = st.multiselect(
                "Domaines de compétences",
                ["Addition", "Soustraction", "Multiplication", "Division", "Fractions", "Décimaux", "Géométrie", "Mesures", "Proportionnalité", "Monnaie"]
            )
        
        with col2:
            difficulty = st.slider("Difficulté", 1, 5, 3)
            exercise_count = st.number_input("Nombre exercices", min_value=5, max_value=50, value=10)
            due_date = st.date_input("Date limite")
        
        if st.button("Créer Assignation"):
            assignment_id = cm.create_assignment(
                classroom_id=classroom_id,
                title=assignment_title,
                skill_domains=skill_domains,
                difficulty=difficulty,
                exercise_count=exercise_count,
                due_date=str(due_date)
            )
            st.success(f"✅ Assignation créée (ID: {assignment_id})")
    
    with tab3:
        # Student management
        st.subheader("Gérer Élèves")
        
        col1, col2 = st.columns(2)
        with col1:
            new_student = st.text_input("Ajouter élève (username)")
            if st.button("Ajouter"):
                cm.add_student_to_classroom(classroom_id, new_student)
                st.success(f"✅ {new_student} ajouté à la classe")
    
    with tab4:
        # Reports & Export
        st.subheader("Rapports Officiels")
        
        if st.button("Générer Rapport Compétences"):
            report = cm.generate_competency_report(classroom_id)
            csv = report.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name="rapport_competences.csv",
                mime="text/csv"
            )
```

### Fichiers à Créer

```
core/pedagogy/
├── classroom_manager.py (500 lignes)
├── assignment_engine.py (300 lignes)
└── curriculum_mapper.py (250 lignes)

ui/
├── teacher_dashboard.py (400 lignes)
├── classroom_management.py (300 lignes)
├── student_detail_view.py (250 lignes)
└── assignment_creation.py (200 lignes)

data/curriculum/
├── EN_competences_CE1.json
├── EN_competences_CE2.json
├── EN_competences_CM1.json
├── EN_competences_CM2.json
└── exercise_to_competence_mapping.json

tests/
├── test_classroom_manager.py (400+ tests)
└── test_teacher_features.py (300+ tests)

docs/
└── TEACHER_GUIDE.md
```

### Checklist Réalisation

- [ ] Database Schema
  - [ ] Teacher accounts table
  - [ ] Classrooms table
  - [ ] Enrollments table
  - [ ] Assignments table
  - [ ] Curriculum competencies table
  - [ ] Student progress tracking
  
- [ ] Backend Implementation
  - [ ] ClassroomManager
  - [ ] AssignmentEngine
  - [ ] CurriculumMapper
  - [ ] ReportGenerator
  
- [ ] Frontend Implementation
  - [ ] Teacher login page
  - [ ] Classroom dashboard
  - [ ] Student detail views
  - [ ] Assignment creation
  - [ ] Real-time monitoring
  
- [ ] Curriculum Alignment
  - [ ] Map exercises to EN competencies
  - [ ] Validate coverage
  - [ ] Document mappings
  
- [ ] Reports
  - [ ] Individual student progress
  - [ ] Class-level reports
  - [ ] Export CSV/PDF
  - [ ] Competency attestations
  
- [ ] Testing
  - [ ] Unit tests (400+)
  - [ ] Integration tests
  - [ ] UI testing
  - [ ] Permission testing
  
- [ ] Deployment
  - [ ] Teacher account provisioning
  - [ ] Pilot with real teachers
  - [ ] Feedback collection
  - [ ] Iterative improvements

### Timeline

```
Semaine 1-3 : Database schema + curriculum mapping
Semaine 4-6 : Backend implementation
Semaine 7-9 : Frontend implementation
Semaine 10-11 : Testing + refinement
Semaine 12-14 : Pilot deployment
```

---

## ÉTAPE 8.2 : Dashboard Analytics Complet

### Objectif
Analytics dashboard pour insights pédagogiques profonds + visualisations avancées

### Features

```
Visualizations:
├── Progress Trajectories (Line chart)
│   └── Pour chaque élève/domaine
│
├── Heatmaps (Skill mastery by domain)
│   └── Chaud = maîtrisé, Froid = à revoir
│
├── Distribution Charts
│   ├── Success rate distribution
│   ├── Time taken distribution
│   └── Difficulty level distribution
│
├── Comparative Analytics
│   ├── Student vs class average
│   ├── Domain vs domain comparison
│   └── Time period comparisons
│
├── Predictive Charts
│   ├── Mastery timeline forecast
│   ├── At-risk prediction timeline
│   └── Improvement forecast
│
└── Export Options
    ├── CSV
    ├── PDF reports
    ├── PowerPoint presentations
    └── Interactive dashboards (Plotly)
```

### Pseudocode

```python
# core/analytics/analytics_engine.py

class AnalyticsEngine:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def generate_progress_trajectory(self, user_id: str, domain: str) -> pd.DataFrame:
        """
        Tracer progression sur temps
        """
        responses = self.db.query(
            "exercise_responses",
            {
                "user_id": user_id,
                "skill_domain": domain
            },
            order_by="created_at"
        )
        
        df = pd.DataFrame(responses)
        df['cumulative_success_rate'] = df['is_correct'].expanding().mean()
        df['moving_avg_7d'] = df['is_correct'].rolling(7).mean()
        
        return df
    
    def generate_skill_heatmap(self, classroom_id: int) -> np.ndarray:
        """
        Heatmap: Students (rows) x Domains (columns) = Mastery level
        """
        students = self.db.query("classroom_enrollments", {"classroom_id": classroom_id})
        domains = ["addition", "subtraction", "multiplication", "division", "fractions", 
                   "decimals", "geometry", "measurements", "proportions", "money"]
        
        heatmap = np.zeros((len(students), len(domains)))
        
        for i, enrollment in enumerate(students):
            student_id = enrollment['student_id']
            
            for j, domain in enumerate(domains):
                proficiency = self.db.query_one(
                    "skill_profiles",
                    {"user_id": student_id, "skill_domain": domain}
                )
                
                heatmap[i, j] = proficiency['proficiency_level'] if proficiency else 0.0
        
        return heatmap, [s['username'] for s in students], domains
    
    def generate_comparative_report(self, user_id: str, classroom_id: int) -> dict:
        """
        Compare user vs class average
        """
        user_performance = self._get_performance_summary(user_id)
        class_performance = self._get_classroom_average_performance(classroom_id)
        
        return {
            "user_vs_class": {
                "user_success_rate": user_performance['success_rate'],
                "class_avg_success_rate": class_performance['success_rate'],
                "user_percentile": self._calculate_percentile(user_id, classroom_id),
                "user_vs_class_delta": user_performance['success_rate'] - class_performance['success_rate']
            },
            "domains_comparison": self._compare_domains(user_id, classroom_id),
            "time_comparison": self._compare_time_engagement(user_id, classroom_id)
        }

# ui/analytics_dashboard.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from core.analytics.analytics_engine import AnalyticsEngine

def render_analytics_dashboard():
    st.set_page_config(page_title="Analytics Dashboard", layout="wide")
    
    ae = AnalyticsEngine(st.session_state.db)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        time_range = st.selectbox("Période", ["1 semaine", "1 mois", "3 mois", "Tout"])
    with col2:
        view_type = st.selectbox("Vue", ["Élève", "Classe", "Domaine"])
    with col3:
        domain_filter = st.multiselect("Domaines", ["Addition", "Soustraction", "Multiplication", "Division", "Fractions"])
    
    # Dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trajectoires", "🔥 Heatmaps", "📊 Comparatifs", "🎯 Prédictions"])
    
    with tab1:
        # Progress trajectories
        st.subheader("Progression Temporelle")
        
        for domain in domain_filter:
            df = ae.generate_progress_trajectory(st.session_state.user_id, domain)
            
            fig = px.line(
                df,
                x='created_at',
                y='cumulative_success_rate',
                title=f"Progression - {domain}",
                labels={'cumulative_success_rate': 'Taux Succès Cumulatif'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Skill heatmap
        st.subheader("Heatmap Compétences")
        
        heatmap, students, domains = ae.generate_skill_heatmap(st.session_state.classroom_id)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap,
            x=domains,
            y=students,
            colorscale='RdYlGn',
            zmin=0,
            zmax=1,
            colorbar=dict(title="Maîtrise")
        ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Comparative analytics
        st.subheader("Analyse Comparative")
        
        report = ae.generate_comparative_report(
            st.session_state.user_id,
            st.session_state.classroom_id
        )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Taux Succès", f"{report['user_vs_class']['user_success_rate']:.0%}")
        col2.metric("vs Classe", f"{report['user_vs_class']['user_vs_class_delta']:+.0%}")
        col3.metric("Percentile", f"{report['user_vs_class']['user_percentile']:.0f}e")
        
        # Domain comparison
        st.subheader("Comparaison par Domaine")
        domain_comp = report['domains_comparison']
        
        fig = px.bar(
            domain_comp,
            x='domain',
            y=['user_proficiency', 'class_avg_proficiency'],
            barmode='group',
            title="Maîtrise par Domaine: Toi vs Classe"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Predictive analytics
        st.subheader("Prédictions")
        
        mastery_forecast = ae.predict_mastery_timeline(
            st.session_state.user_id
        )
        
        st.write(f"""
        📚 **Prédiction Maîtrise**: {mastery_forecast['estimated_days']} jours
        
        Détails:
        - Proficiency actuelle: {mastery_forecast['current_proficiency']:.0%}
        - Exercices restants: {mastery_forecast['exercises_needed']}
        - Confiance: {mastery_forecast['confidence']:.0%}
        """)
```

### Fichiers à Créer

```
core/analytics/
├── analytics_engine.py (500 lignes)
├── visualization_templates.py (300 lignes)
└── export_engine.py (250 lignes)

ui/
├── analytics_dashboard.py (400 lignes)
├── progress_visualizations.py (300 lignes)
├── comparative_analytics.py (250 lignes)
└── predictive_analytics.py (200 lignes)

tests/
└── test_analytics.py (300+ tests)
```

### Checklist Réalisation

- [ ] Analytics Engine
  - [ ] Progress trajectory calculation
  - [ ] Heatmap generation
  - [ ] Comparative analysis
  - [ ] Predictive analytics
  
- [ ] Visualizations
  - [ ] Line charts (Plotly)
  - [ ] Heatmaps (Plotly)
  - [ ] Bar charts
  - [ ] Distribution plots
  - [ ] Time series forecasts
  
- [ ] Export Engine
  - [ ] CSV export
  - [ ] PDF reports (ReportLab)
  - [ ] PowerPoint presentations (python-pptx)
  - [ ] Interactive dashboards
  
- [ ] Dashboard UI
  - [ ] Multiple tabs
  - [ ] Filters (time, domain, student)
  - [ ] Real-time updates
  - [ ] Responsive design
  
- [ ] Testing
  - [ ] Analytics calculations accuracy
  - [ ] Visualization rendering
  - [ ] Export format validation
  
- [ ] Integration
  - [ ] Load from PostgreSQL
  - [ ] Real-time updates
  - [ ] Performance optimization

### Timeline

```
Semaine 1-2 : Analytics engine
Semaine 3-4 : Visualizations (Plotly)
Semaine 5 : Export engine
Semaine 6-7 : Dashboard UI + integration
```

---

# 📋 GUIDE D'UTILISATION CLAUDE POUR CHAQUE PHASE

## 🤖 Claude Chat vs Claude Code

**Claude Chat** : Planification, design, discussion
**Claude Code** : Implémentation, debugging, testing

---

## PHASE 6 : Fondations Pédagogiques

### ÉTAPE 6.1 : Feedback Pédagogique

**Prompt Claude Chat (Planning)** :
```
Je dois implémenter Feedback Pédagogique Intelligent pour MathCopain.
Objectif: +35-40% apprentissage via feedback transformatif.
Composition:
- ErrorAnalyzer: Identifier type erreur (Conceptual/Procedural/Calculation)
- FeedbackGenerator: Explications contextuelles
- RemediationRecommender: Prochaines étapes
- Database: 500+ erreurs couvertes

Aide-moi à:
1. Structurer l'architecture
2. Identifier les 10 types d'erreurs mathématiques les plus courants
3. Définir feedback templates

Modèle pédagogique: Feedback transformatif (Hattie 2008).
```

**Prompt Claude Code (Implémentation)** :
```
Créer ErrorAnalyzer.

Pseudocode existant fourni. Implémenter:
1. Classe ErrorAnalyzer
2. Taxonomie erreurs (JSON): 500+ errors
3. Méthodes:
   - analyze_error_type() → [Conceptual | Procedural | Calculation]
   - identify_misconception() → Common learning error
   - root_cause_analysis() → Pourquoi?
4. Tests pytest: 300+ tests
5. Coverage: 85%+

Utiliser database: errors_taxonomy.json (structure proposée).
```

**Workflow Phase 6.1** :
```
Claude Chat:
  ├─ Discuter: Types erreurs mathématiques CE1-CM2
  ├─ Discuter: Feedback templates efficaces
  ├─ Valider: Architecture design
  └─ Discuter: Cas limites

Claude Code:
  ├─ Implémenter: ErrorAnalyzer + tests (320 tests)
  ├─ Implémenter: FeedbackGenerator + tests (280 tests)
  ├─ Implémenter: RemediationRecommender (250 tests)
  ├─ Créer: JSON databases (5 fichiers)
  ├─ Implémenter: Integration app.py
  └─ Debugger: Erreurs de production
```

---

### ÉTAPE 6.2 : Métacognition

**Prompt Claude Chat (Design)** :
```
Métacognition & Autorégulation pour apprenants.

Questions réflexives post-exercice:
1. Stratégie utilisée?
2. Difficulté perçue?
3. Auto-explication (comment tu as trouvé)?
4. Intention future?

Aide-moi à:
1. Designer les questions (pédagogiquement solides)
2. Définir structure portfolio stratégies
3. Identifier patterns apprentissage
4. Générer insights personnalisés
```

**Prompt Claude Code** :
```
Créer MetacognitionEngine.

Fonctionnalités:
1. generate_post_exercise_reflection() → Questions adaptées
2. process_reflection_response() → Enregistrer + Analyser
3. generate_self_regulation_support() → Suggestions (pause, continuer, défi)
4. generate_portfolio_summary() → Visualisation stratégies

Interface: 4 questions en 30 secondes, optional.
Tests: 350+ tests couvrant scénarios
```

---

### ÉTAPE 6.3 : Learning Styles

**Prompt Claude Chat** :
```
Learning Styles: Visual, Auditory, Kinesthetic, Logical, Narrative.

Quiz 5-7 minutes pour profiler + inférence depuis performance patterns.

Aide-moi à:
1. Designer le quiz (valide pédagogiquement)
2. Définir adapters pour chaque style
3. Valider scoring algorithm
4. Identifier cas limites (élèves multi-style)
```

**Prompt Claude Code** :
```
Créer LearningStyleAnalyzer + 5 Adapters.

LearningStyleAnalyzer:
  - assess_from_quiz() → Primary + Secondary style
  - infer_from_performance()
  - combine_assessments() → Quiz 40% + Performance 60%

Adapters (5):
  - VisualAdapter: Diagrams, color coding
  - AuditoryAdapter: Audio descriptions
  - KinestheticAdapter: Interactive manipulables
  - LogicalAdapter: Causal explanations
  - NarrativeAdapter: Story contexts

ExerciseAdapter: adapt_exercise() → Adapted for style

Tests: 300+ tests covering all styles
```

---

## PHASE 7 : Infrastructure & IA

### ÉTAPE 7.1 : PostgreSQL

**Prompt Claude Chat** :
```
PostgreSQL Migration Planning.

Actuel: JSON files (users_data.json, etc.)
Cible: PostgreSQL relational DB

Aide-moi à:
1. Designer schema 3NF
2. Planifier migration strategy
3. Identifier risques + mitigation
4. Backup strategy
```

**Prompt Claude Code (Multiple prompts)** :

**Prompt 1 - Schema & Alembic** :
```
Créer PostgreSQL schema pour MathCopain.

Tables:
- users (id, username, pin_hash, learning_style)
- exercise_responses (user_id, exercise_id, skill_domain, is_correct, time_taken, error_type, etc.)
- skill_profiles (user_id, skill_domain, proficiency_level, exercises_completed)
- parent_accounts, parent_child_links
- analytics_events

Normalization: 3NF
Indexes: user_id, skill_domain, created_at
Foreign keys + constraints

Créer Alembic migration (001_initial_schema.py)
Tester upgrade/downgrade
```

**Prompt 2 - Data Migration** :
```
Créer json_to_postgres.py migration script.

Charge: users_data.json, exercises_history.json, skill_profiles.json
Transforme → PostgreSQL schema
Valide: no duplicates, foreign key integrity
Modes: Dry-run, Full run
Backup recovery si erreur

Avec tests integration
```

**Prompt 3 - ORM Integration** :
```
Créer SQLAlchemy models + refactor queries.

Models pour each table. Relationships.
Refactor existing queries en SQLAlchemy ORM.
Connection pooling (sqlalchemy.pool.QueuePool).
Transaction management (sessions).

Maintenir backward compatibility avec JSON version.
```

---

### ÉTAPE 7.2 : IA Adaptive Learning

**Prompt Claude Chat** :
```
IA Adaptive Learning System.

ML objectives:
1. Predict optimal difficulty (D1-D5)
2. Predict success probability
3. Identify at-risk learners (early intervention)
4. Predict mastery timeline
5. Explainable AI (pourquoi telle prédiction?)

Théorie: Flow (Csikszentmihalyi) - target success_rate = 70%

Aide-moi à:
1. Définir features (input)
2. Identifier algo optimal (GB, LSTM, RF, Ensemble)
3. Plan test/val/train splits
4. Identifier fairness risks + mitigation
```

**Prompt Claude Code (Multiple)** :

**Prompt 1 - Feature Engineering** :
```
Créer feature extraction pour ML models.

Input features:
- Historical performance (last 10 exercises, trends)
- Learning patterns (velocity, fatigue, confidence)
- Domain-specific performance
- Time-of-day effects

Output: NumPy array, scaled

Tests: 200+ tests validating features
```

**Prompt 2 - Difficulty Optimizer** :
```
Créer DifficultyOptimizer utilisant Gradient Boosting.

Models:
- Gradient Boosting (XGBoost/LightGBM) pour difficulty prediction
- Output: Difficulty 1-5

Incorporer Flow Theory:
- Target success_rate = 0.70
- Adjust difficulté si success_rate > 0.85 or < 0.55

Explainability:
- explain_difficulty_choice() → "Pourquoi D3?"
- Humanly-readable reasons

Tests: 300+ tests
```

**Prompt 3 - Performance Predictor** :
```
Créer PerformancePredictor.

Fonctionnalités:
1. predict_success_probability() → P(success | history)
2. identify_at_risk_learners() → Risk score > 0.6
3. predict_mastery_timeline() → Exercises needed, days

Models:
- LSTM (time series) 40%
- Random Forest 60%

Tests: 300+ tests
Fairness audit: Detect bias by demographics
```

**Prompt 4 - Explainable AI** :
```
Créer ExplainableAI module.

explain_prediction() → Humain explanation de prédictions
- Pourquoi j'ai prédit ça?
- Quels facteurs ont le plus influencé?

generate_confidence_intervals() → Incertitude
- Lower bound, upper bound, confidence level

SHAP values ou similar pour feature importance

Tests: 200+ tests
```

---

## PHASE 8 : Déploiement Institutionnel

### ÉTAPE 8.1 : Mode Enseignant

**Prompt Claude Chat** :
```
Teacher Mode & Classroom Management.

Features:
- Teacher login + classroom creation
- Add/manage students
- Create assignments
- Monitor real-time progress
- Generate official reports

Curriculum mapping: Align exercises with Éducation Nationale competencies

Aide-moi à:
1. Designer teacher UX
2. Planifier database schema
3. Identifier permission model
4. Définir report formats
```

**Prompt Claude Code** :
```
Créer ClassroomManager backend.

Fonctionnalités:
1. create_classroom(name, class_level, max_students)
2. add_student_to_classroom(classroom_id, student_username)
3. create_assignment(classroom_id, skill_domains, difficulty, exercise_count, due_date)
4. get_classroom_overview(classroom_id) → Real-time stats
5. generate_competency_report(classroom_id) → Export

Database:
- teacher_accounts, classrooms, classroom_enrollments
- assignments, assignment_responses
- curriculum_competencies, student_competency_progress

Tests: 400+ tests
```

**Prompt Claude Code (UI)** :
```
Créer Streamlit Teacher Dashboard.

Pages/Tabs:
1. Overview: Class stats, student list, success rates
2. Assignments: Create, assign, track submissions
3. Students: Add/remove, view individual progress
4. Reports: Generate + export (CSV, PDF)

Real-time updates using Streamlit session state + polling
```

---

### ÉTAPE 8.2 : Analytics Dashboard

**Prompt Claude Chat** :
```
Analytics Dashboard Avancée.

Visualizations:
- Progress trajectories (line chart)
- Heatmaps (students × domains)
- Distributions (success rate, time, difficulty)
- Comparative (student vs class vs benchmark)
- Predictive (mastery forecast, at-risk timeline)

Export: CSV, PDF, PowerPoint, Interactive

Aide-moi à:
1. Designer visualizations (informatives, not overwhelming)
2. Définir metrics clés
3. Planifier performance (>1000 users, real-time)
```

**Prompt Claude Code** :
```
Créer AnalyticsEngine + Dashboard.

AnalyticsEngine:
1. generate_progress_trajectory() → DF
2. generate_skill_heatmap() → NumPy array
3. generate_comparative_report() → User vs class vs benchmark
4. generate_predictive_forecast() → Mastery timeline

Visualizations (Plotly):
- Line charts
- Heatmaps
- Bar charts
- Distribution plots
- Time series with forecasts

Dashboard (Streamlit):
- Filters (time, domain, student)
- Multiple tabs
- Export buttons

Tests: 300+ tests
```

---

# 📋 CHECKLIST MAÎTRE - SUIVI COMPLET

## Phase 6 - Fondations Pédagogiques

### 6.1 Feedback Pédagogique
```
Architecture Design:
  ☐ ErrorAnalyzer design doc
  ☐ FeedbackGenerator templates
  ☐ RemediationRecommender paths
  ☐ Architecture review + approval

Implementation:
  ☐ core/pedagogy/error_analyzer.py (300 lignes)
  ☐ core/pedagogy/feedback_engine.py (400 lignes)
  ☐ core/pedagogy/remediation.py (250 lignes)
  ☐ core/pedagogy/explanation_templates.py (200 lignes)
  ☐ data/error_taxonomy.json (500+ errors)
  ☐ data/misconceptions_db.json
  ☐ data/remediation_paths.json
  ☐ data/explanation_templates/* (10 domains)

Testing:
  ☐ tests/test_feedback_engine.py (400+ tests, 85%+ coverage)
  ☐ tests/test_error_analyzer.py (300+ tests)
  ☐ tests/test_remediation.py (250+ tests)

Integration:
  ☐ Integrate into app.py exercise_completed_handler()
  ☐ UI multi-couches (immediate, explanation, strategy, remediation)
  ☐ Logging for analytics

Documentation:
  ☐ README pédagogique
  ☐ Taxonomie erreurs documentée
  ☐ Exemples avant/après

Timeline: 8 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

### 6.2 Métacognition & Autorégulation
```
Design:
  ☐ Post-exercise reflection questions
  ☐ StrategyPortfolio data model
  ☐ Self-regulation suggestions criteria
  ☐ Portfolio visualization design

Implementation:
  ☐ core/pedagogy/metacognition.py (400 lignes)
  ☐ core/pedagogy/strategy_portfolio.py (300 lignes)
  ☐ ui/metacognition_ui.py (250 lignes)
  ☐ ui/strategy_portfolio_view.py (200 lignes)
  ☐ ui/learning_insights_dashboard.py (200 lignes)
  ☐ data/user_profiles/{user_id}/personal_strategies.json

Testing:
  ☐ tests/test_metacognition.py (350+ tests)

Integration:
  ☐ Hook after every exercise
  ☐ Display reflection card (30 sec)
  ☐ Persist responses to DB

Documentation:
  ☐ Pédagogie derrière réflexions
  ☐ User guide (enfant + parent)

Timeline: 6 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

### 6.3 Profiling Styles Apprentissage
```
Design:
  ☐ Learning style quiz (5-7 questions)
  ☐ 5 Adapter implementations
  ☐ Scoring algorithm
  ☐ Quiz UX flow

Implementation:
  ☐ core/pedagogy/learning_style.py (350 lignes)
  ☐ core/exercise_generator/exercise_adapter.py (400 lignes)
  ☐ core/exercise_generator/adapters/visual_adapter.py (150 lignes)
  ☐ core/exercise_generator/adapters/auditory_adapter.py (100 lignes)
  ☐ core/exercise_generator/adapters/kinesthetic_adapter.py (150 lignes)
  ☐ core/exercise_generator/adapters/logical_adapter.py (100 lignes)
  ☐ core/exercise_generator/adapters/narrative_adapter.py (150 lignes)
  ☐ ui/learning_style_assessment.py (200 lignes)

Testing:
  ☐ tests/test_learning_style.py (300+ tests)
  ☐ tests/test_exercise_adapter.py (250+ tests)
  ☐ A/B testing results

Integration:
  ☐ First launch: quiz mandatory
  ☐ Load learning_style in session
  ☐ Pass to ExerciseAdapter in generation

Documentation:
  ☐ Scientific validation references
  ☐ Adaptation guide per style
  ☐ Quiz interpretation guide

Timeline: 7 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

**Phase 6 Summary**:
```
Total Timeline: 14-18 weeks (Q4 2025 - Q1 2026)
Code Lines: ~5,000 lines
Tests: ~950+ tests
Coverage Target: 85%+
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

---

## Phase 7 - Infrastructure & IA

### 7.1 PostgreSQL Migration
```
Planning:
  ☐ Current JSON structure audit
  ☐ PostgreSQL schema design (3NF)
  ☐ Migration strategy document
  ☐ Risk assessment + mitigation plan

Environment Setup:
  ☐ PostgreSQL local installation
  ☐ Docker Compose config
  ☐ Connection pooling (pgBouncer)
  ☐ Backup strategy
  ☐ RDS (AWS) provisioning

Schema & Migration:
  ☐ database/models.py (SQLAlchemy)
  ☐ database/connection.py (pooling)
  ☐ database/migrations/001_initial_schema.py
  ☐ database/migration_scripts/json_to_postgres.py
  ☐ database/migration_scripts/data_validation.py
  ☐ database/migration_scripts/rollback_recovery.py

Testing:
  ☐ tests/test_db_models.py
  ☐ tests/test_migration.py (dry-run validation)
  ☐ tests/test_db_performance.py (load testing >1000 users)

Execution:
  ☐ Backup JSON before migration
  ☐ Run dry-run migration
  ☐ Verify data integrity
  ☐ Run actual migration
  ☐ Validate production data
  ☐ Update app.py to use PostgreSQL

Documentation:
  ☐ POSTGRES_MIGRATION.md
  ☐ Schema documentation
  ☐ Connection parameters doc

Timeline: 10 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

### 7.2 IA Adaptive Learning
```
Feature Engineering:
  ☐ Design feature set
  ☐ extract_features() implementation
  ☐ Data preprocessing + scaling
  ☐ tests/test_features.py (200+ tests)

Model Development:
  ☐ DifficultyOptimizer (Gradient Boosting)
    ☐ Train/val/test splits
    ☐ Hyperparameter tuning
    ☐ Model serialization (.pkl)
    ☐ explain_difficulty_choice() (XAI)
  
  ☐ PerformancePredictor (LSTM + RF Ensemble)
    ☐ LSTM for time series
    ☐ Random Forest for risk
    ☐ Voting mechanism
    ☐ predict_success_probability()
    ☐ identify_at_risk_learners()
    ☐ predict_mastery_timeline()
  
  ☐ LacunaDetector (Graph-based)
    ☐ Prerequisite mapping
    ☐ identify_conceptual_gaps()
    ☐ knowledge_map()

Explainability:
  ☐ SHAP values implementation
  ☐ Human-readable explanations
  ☐ Confidence intervals
  ☐ ExplainableAI module (250 lignes)
  ☐ tests/test_explainable_ai.py (200+ tests)

Evaluation:
  ☐ Metrics: MAE, Precision, Recall, F1, AUC
  ☐ Cross-validation (5-fold)
  ☐ Fairness audit (by gender, demographics)
  ☐ Bias detection + mitigation
  ☐ A/B testing framework

Integration:
  ☐ Load models in app.py
  ☐ Real-time predictions on exercise submission
  ☐ Model versioning + serving
  ☐ Fallback mechanisms (if ML fails)

Monitoring:
  ☐ Model performance tracking
  ☐ Prediction accuracy dashboard
  ☐ Retraining schedule + automation
  ☐ Drift detection

Testing:
  ☐ tests/test_ml_predictions.py (400+ tests)
  ☐ tests/test_ml_performance.py (benchmark)
  ☐ tests/test_fairness.py (bias audit)

Timeline: 12 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

**Phase 7 Summary**:
```
Total Timeline: 18-22 weeks (Q2 2026)
Code Lines: ~6,000 lines
Tests: ~800+ tests
Models: 3 (GB, LSTM, RF)
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

---

## Phase 8 - Déploiement Institutionnel

### 8.1 Mode Enseignant & Classe
```
Database Schema:
  ☐ teacher_accounts table
  ☐ classrooms table
  ☐ classroom_enrollments table
  ☐ assignments table
  ☐ assignment_responses table
  ☐ curriculum_competencies table
  ☐ student_competency_progress table
  ☐ Migrations via Alembic

Backend Implementation:
  ☐ core/pedagogy/classroom_manager.py (500 lignes)
  ☐ core/pedagogy/assignment_engine.py (300 lignes)
  ☐ core/pedagogy/curriculum_mapper.py (250 lignes)
  ☐ core/pedagogy/report_generator.py (200 lignes)

Frontend Implementation:
  ☐ ui/teacher_dashboard.py (400 lignes)
  ☐ ui/classroom_management.py (300 lignes)
  ☐ ui/student_detail_view.py (250 lignes)
  ☐ ui/assignment_creation.py (200 lignes)
  ☐ ui/teacher_login.py (100 lignes)

Curriculum:
  ☐ data/curriculum/EN_competences_CE1.json
  ☐ data/curriculum/EN_competences_CE2.json
  ☐ data/curriculum/EN_competences_CM1.json
  ☐ data/curriculum/EN_competences_CM2.json
  ☐ data/curriculum/exercise_to_competence_mapping.json
  ☐ Validate coverage

Reports:
  ☐ Individual student progress PDF
  ☐ Class-level report CSV
  ☐ Competency attestation PDF
  ☐ Export mechanism

Testing:
  ☐ tests/test_classroom_manager.py (400+ tests)
  ☐ tests/test_teacher_features.py (300+ tests)
  ☐ tests/test_permissions.py (150+ tests)
  ☐ UI testing (manual + Selenium)

Deployment:
  ☐ Teacher account provisioning system
  ☐ Pilot with 3-5 real teachers
  ☐ Feedback collection
  ☐ Iterative improvements

Documentation:
  ☐ TEACHER_GUIDE.md
  ☐ Admin guide (account provisioning)
  ☐ Curriculum documentation

Timeline: 14 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

### 8.2 Dashboard Analytics Complet
```
Analytics Engine:
  ☐ core/analytics/analytics_engine.py (500 lignes)
  ☐ generate_progress_trajectory()
  ☐ generate_skill_heatmap()
  ☐ generate_comparative_report()
  ☐ generate_predictive_forecast()

Visualizations (Plotly):
  ☐ Line charts (progress trajectories)
  ☐ Heatmaps (students × domains)
  ☐ Bar charts (domain comparisons)
  ☐ Distribution plots
  ☐ Time series with forecasts
  ☐ core/analytics/visualization_templates.py (300 lignes)

Export Engine:
  ☐ CSV export (pandas)
  ☐ PDF reports (ReportLab)
  ☐ PowerPoint presentations (python-pptx)
  ☐ Interactive dashboards
  ☐ core/analytics/export_engine.py (250 lignes)

Dashboard UI:
  ☐ ui/analytics_dashboard.py (400 lignes)
  ☐ ui/progress_visualizations.py (300 lignes)
  ☐ ui/comparative_analytics.py (250 lignes)
  ☐ ui/predictive_analytics.py (200 lignes)

Features:
  ☐ Multiple tabs (Progress, Heatmap, Comparative, Predictive)
  ☐ Filters (time range, domain, student)
  ☐ Real-time updates
  ☐ Responsive design
  ☐ Export buttons

Testing:
  ☐ tests/test_analytics.py (300+ tests)
  ☐ tests/test_visualizations.py (200+ tests)
  ☐ tests/test_exports.py (150+ tests)

Performance:
  ☐ Optimize queries for >1000 users
  ☐ Caching strategy
  ☐ Lazy loading visualizations

Integration:
  ☐ Load from PostgreSQL
  ☐ Real-time updates
  ☐ Session state management

Timeline: 10 weeks
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

**Phase 8 Summary**:
```
Total Timeline: 20-24 weeks (Q3 2026)
Code Lines: ~5,000 lines
Tests: ~1,200+ tests
DB Tables: 7 new tables
Status: [ ] Not Started [ ] In Progress [ ] Complete
```

---

# 📊 RÉSUMÉ COMPLET DU PROJET

## Timeline Global

```
Q4 2025 → Q1 2026 : Phase 6 (18 weeks)
├─ Feedback Pédagogique Intelligent (8 weeks)
├─ Métacognition & Autorégulation (6 weeks)
└─ Profiling Styles Apprentissage (7 weeks)

Q2 2026 : Phase 7 (22 weeks)
├─ PostgreSQL Migration (10 weeks)
└─ IA Adaptive Learning (12 weeks)

Q3 2026 : Phase 8 (24 weeks)
├─ Mode Enseignant & Classe (14 weeks)
└─ Dashboard Analytics Complet (10 weeks)

Total: 64 weeks = 15 mois
```

## Code Statistics

```
Phase 6: ~5,000 lignes + ~950 tests
Phase 7: ~6,000 lignes + ~800 tests
Phase 8: ~5,000 lignes + ~1,200 tests

Total: ~16,000 lignes + ~2,950 tests
```

## Ressources Requises

```
Development:
  - 2-3 engineers (backend + frontend + ML)
  - 1 data scientist (ML models)
  - 1 QA engineer
  - 1 DevOps engineer

Pédagogie:
  - 1 education specialist (validation)
  - 1 curriculum designer

Operations:
  - 1 project manager
  - Pilot teachers (3-5)
```

## Infrastructure

```
Development:
  - PostgreSQL local
  - Docker/Docker Compose
  - GitHub Actions CI/CD

Production:
  - AWS RDS (PostgreSQL)
  - Streamlit Cloud or AWS EC2
  - CloudWatch monitoring
  - S3 backups
```

---

# ✅ Conclusion

Ce guide fournit une roadmap complète, stratégique et pédagogiquement fondée pour transformer MathCopain v6.3.0 en une plateforme institutionnelle d'apprentissage personnalisé.

**Points clés**:
- Architecture : Modulaire, testée, scalable
- Pédagogie : Feedback transformatif, métacognition, styles apprentissage
- Infrastructure : PostgreSQL, IA, monitoring
- Déploiement : Enseignants, classes, rapports officiels
- Éthique : Fairness audit, explainability, no over-gamification

**Succès mesuré par**:
- 85%+ test coverage
- +35-40% apprentissage (feedback)
- +25-35% engagement (styles learning)
- Déploiement >50 classes en production

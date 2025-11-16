# Phase 8 Backend - Mode Enseignant & Analytics

## Vue d'ensemble

Phase 8 Backend implémente une infrastructure complète pour le déploiement institutionnel de MathCopain, incluant :

- **Gestion de classes** : Création et gestion de classes par les enseignants
- **Affectation de devoirs** : Création et suivi de devoirs adaptatifs
- **Mapping curriculum** : Alignement avec le programme Éducation Nationale
- **Analytics avancés** : Tableaux de bord avec prédictions ML
- **Génération de rapports** : Exports PDF/CSV/PowerPoint

## Architecture

### Modules implémentés

```
core/classroom/
├── classroom_manager.py    # Gestion CRUD des classes
├── assignment_engine.py    # Moteur de devoirs adaptatifs
├── curriculum_mapper.py    # Mapping compétences EN
├── analytics_engine.py     # Analytics et prédictions ML
└── report_generator.py     # Génération de rapports
```

### Base de données

7 nouvelles tables ajoutées :

- `teacher_accounts` : Comptes enseignants
- `classrooms` : Classes virtuelles
- `classroom_enrollments` : Inscriptions élèves
- `assignments` : Devoirs
- `assignment_completions` : Suivi de complétion
- `curriculum_competencies` : Référentiel compétences EN
- `student_competency_progress` : Progression par compétence

Migration : `database/migrations/versions/20251116_002_teacher_classroom_tables.py`

---

## 1. ClassroomManager

**Responsabilité** : Gestion complète des classes et des élèves

### Fonctionnalités principales

#### Création de classe

```python
from core.classroom import ClassroomManager

manager = ClassroomManager(teacher_id=1)

classroom = manager.create_classroom(
    name="CE2 - Classe A",
    grade_level="CE2",
    school_year="2025-2026",
    max_students=30,
    description="Classe de CE2 - Année scolaire 2025-2026"
)
# Returns:
# {
#     'id': 1,
#     'name': 'CE2 - Classe A',
#     'grade_level': 'CE2',
#     'message': "✓ Classe 'CE2 - Classe A' créée avec succès"
# }
```

#### Ajout d'élèves

```python
enrollment = manager.add_student(
    classroom_id=1,
    student_username="alice_ce2"
)
# Vérifie automatiquement :
# - Capacité de la classe (max_students)
# - Existence de l'élève
# - Pas de double inscription
```

#### Vue d'ensemble de la classe

```python
overview = manager.get_classroom_overview(classroom_id=1)
# Returns:
# {
#     'id': 1,
#     'name': 'CE2 - Classe A',
#     'student_count': 25,
#     'stats': {
#         'total_students': 25,
#         'active_students_7d': 22,
#         'avg_success_rate': 0.73,
#         'total_exercises': 1250,
#         'at_risk_count': 3
#     },
#     'students': [...]  # Liste détaillée
# }
```

#### Détection élèves à risque

```python
at_risk = manager.get_at_risk_students(
    classroom_id=1,
    threshold=0.40  # Seuil de risque (0-1)
)
# Returns:
# [
#     {
#         'id': 5,
#         'username': 'bob_ce2',
#         'risk_score': 0.65,
#         'risk_level': 'HIGH',
#         'struggling_domain': 'multiplication',
#         'recommendation': 'Suivi rapproché et exercices de renforcement en multiplication'
#     },
#     ...
# ]
```

---

## 2. AssignmentEngine

**Responsabilité** : Gestion de devoirs avec difficulté adaptative ML

### Fonctionnalités principales

#### Création de devoir

```python
from core.classroom import AssignmentEngine

engine = AssignmentEngine(teacher_id=1)

assignment = engine.create_assignment(
    classroom_id=1,
    title="Révision multiplication - Tables 2 à 5",
    skill_domains=["multiplication"],
    difficulty_levels=None,  # None = adaptatif ML
    exercise_count=10,
    due_date=datetime.now() + timedelta(days=7),
    description="Réviser les tables de multiplication de 2 à 5",
    adaptive=True  # Active le mode adaptatif
)
# Returns:
# {
#     'id': 1,
#     'title': 'Révision multiplication - Tables 2 à 5',
#     'adaptive': True,
#     'is_published': False,  # Brouillon par défaut
#     'message': "✓ Devoir 'Révision...' créé (brouillon)"
# }
```

#### Publication de devoir

```python
result = engine.publish_assignment(assignment_id=1)
# Crée automatiquement des AssignmentCompletion pour chaque élève
# Returns:
# {
#     'id': 1,
#     'students_assigned': 25,
#     'message': "✓ Devoir publié pour 25 élèves"
# }
```

#### Génération d'exercices adaptatifs

```python
exercises = engine.generate_student_exercises(
    assignment_id=1,
    student_id=5
)
# Utilise DifficultyOptimizer (ML) pour adapter la difficulté
# Returns:
# [
#     {
#         'domain': 'multiplication',
#         'difficulty': 3,  # Calculé par ML selon le profil
#         'type': 'calculation',
#         'ml_adapted': True
#     },
#     ...  # 10 exercices au total
# ]
```

#### Suivi de complétion

```python
progress = engine.record_exercise_completion(
    assignment_id=1,
    student_id=5,
    is_correct=True,
    time_taken=45
)
# Returns:
# {
#     'progress': '7/10',
#     'success_rate': 0.71,
#     'status': 'in_progress'  # ou 'completed'
# }
```

#### Vue d'ensemble de complétion

```python
completions = engine.get_assignment_completion(assignment_id=1)
# Returns liste de tous les élèves avec :
# - Progression (X/Y exercices)
# - Taux de réussite
# - Temps passé
# - Statut (in_progress/completed)
```

---

## 3. CurriculumMapper

**Responsabilité** : Alignement avec le programme Éducation Nationale

### Référentiel compétences

Fichiers JSON par niveau :
- `data/curriculum/EN_competences_CE1.json` (20 compétences)
- `data/curriculum/EN_competences_CE2.json` (25 compétences)
- `data/curriculum/EN_competences_CM1.json` (30 compétences)
- `data/curriculum/EN_competences_CM2.json` (33 compétences)

**Total : 108 compétences officielles EN**

### Fonctionnalités principales

#### Synchronisation curriculum → DB

```python
from core.classroom import CurriculumMapper

mapper = CurriculumMapper()

result = mapper.sync_competencies_to_database()
# Charge les JSON dans la base de données
# Returns:
# {
#     'synced': 108,
#     'updated': 0,
#     'message': "✓ 108 compétences ajoutées, 0 mises à jour"
# }
```

#### Mapping exercice → compétences

```python
competency_codes = mapper.map_exercise_to_competencies(
    skill_domain="multiplication",
    difficulty=3,
    grade_level="CE2"
)
# Returns: ['CE2.C.3.2', 'CE2.C.3.3']
```

#### Mise à jour progression élève

```python
progress = mapper.update_student_competency_progress(
    student_id=5,
    competency_code="CE2.C.3.2",
    is_correct=True,
    exercise_difficulty=3
)
# Algorithme de maîtrise :
# - Augmente mastery_level si correct (pondéré par difficulté)
# - Diminue légèrement si incorrect
# - Marque "mastered" si mastery_level >= 0.8 et >= 5 exercices
```

#### Rapport de compétences élève

```python
report = mapper.get_student_competency_report(
    student_id=5,
    grade_level="CE2"
)
# Returns:
# {
#     'summary': {
#         'total_competencies': 25,
#         'mastered': 12,
#         'in_progress': 8,
#         'not_started': 5,
#         'completion_rate': 0.48
#     },
#     'competencies': [
#         {
#             'code': 'CE2.C.3.2',
#             'title': 'Tables de multiplication jusqu\'à 9',
#             'status': 'mastered',
#             'mastery_level': 0.85,
#             'success_rate': 0.82
#         },
#         ...
#     ]
# }
```

#### Identification des lacunes

```python
gaps = mapper.identify_competency_gaps(
    student_id=5,
    grade_level="CE2"
)
# Returns liste triée par priorité :
# - Non démarrées (priorité max)
# - En cours avec faible maîtrise
# - Non pratiquées récemment
```

#### Recommandations

```python
recommendations = mapper.recommend_next_competencies(
    student_id=5,
    grade_level="CE2",
    count=3
)
# Returns top 3 compétences à travailler
```

---

## 4. AnalyticsEngine

**Responsabilité** : Analytics avancés avec prédictions ML

### Fonctionnalités principales

#### Trajectoire de progression

```python
from core.classroom import AnalyticsEngine

analytics = AnalyticsEngine()

trajectory = analytics.get_student_progress_trajectory(
    student_id=5,
    skill_domain="multiplication",
    days_back=30,
    granularity='daily'  # ou 'weekly'
)
# Returns:
# {
#     'data_points': [
#         {
#             'date': '2025-11-01',
#             'exercises_completed': 8,
#             'success_rate': 0.625,
#             'avg_time_seconds': 42
#         },
#         ...
#     ],
#     'overall_trend': 0.015,  # Pente de régression linéaire
#     'trend_direction': 'improving'  # ou 'declining', 'stable'
# }
```

#### Heatmap de performance

```python
heatmap = analytics.generate_performance_heatmap(
    student_id=5,
    days_back=30
)
# Returns matrice domaine × difficulté
# {
#     'heatmap': [
#         {
#             'domain': 'multiplication',
#             'difficulties': [
#                 {'difficulty': 1, 'success_rate': 0.95, 'status': 'excellent'},
#                 {'difficulty': 2, 'success_rate': 0.82, 'status': 'excellent'},
#                 {'difficulty': 3, 'success_rate': 0.58, 'status': 'needs_improvement'},
#                 ...
#             ]
#         },
#         ...
#     ]
# }
```

#### Prévisions ML

```python
forecast = analytics.forecast_student_performance(
    student_id=5,
    skill_domain="multiplication",
    days_ahead=7
)
# Utilise PerformancePredictor + régression linéaire
# Returns:
# {
#     'current_success_probability': 0.68,
#     'trend': 'improving',
#     'forecast': [
#         {'date': '2025-11-17', 'projected_success_rate': 0.69, 'confidence': 0.85},
#         {'date': '2025-11-18', 'projected_success_rate': 0.70, 'confidence': 0.81},
#         ...
#     ],
#     'risk_level': 'medium',
#     'recommendation': 'Suivi nécessaire en multiplication'
# }
```

#### Métriques d'engagement

```python
engagement = analytics.get_student_engagement_metrics(
    student_id=5,
    days_back=30
)
# Returns:
# {
#     'total_exercises': 152,
#     'active_days': 18,
#     'avg_exercises_per_day': 5.07,
#     'current_streak': 4,  # Jours consécutifs actifs
#     'engagement_score': 62.5,  # Sur 100
#     'engagement_level': 'good',
#     'peak_activity_hour': 17,
#     'weekday_distribution': {...},
#     'hour_distribution': {...}
# }
```

#### Comparaison élève vs classe

```python
comparison = analytics.compare_student_to_class(
    student_id=5,
    classroom_student_ids=[1,2,3,4,5,6,...,25],
    skill_domain="multiplication",
    days_back=30
)
# Returns:
# {
#     'student_metrics': {
#         'exercises_completed': 45,
#         'success_rate': 0.71
#     },
#     'class_metrics': {
#         'avg_success_rate': 0.68
#     },
#     'comparison': {
#         'percentile': 62.5,  # Meilleur que 62.5% de la classe
#         'relative_performance': 'above_average',
#         'difference_from_avg': 0.03
#     }
# }
```

#### Détection d'anomalies

```python
anomalies = analytics.detect_performance_anomalies(
    student_id=5,
    skill_domain="multiplication",
    days_back=30
)
# Détecte les baisses/pics soudains (>2 écarts-types)
# Returns:
# [
#     {
#         'date': '2025-11-10',
#         'type': 'sudden_drop',
#         'actual_success_rate': 0.30,
#         'expected_success_rate': 0.72,
#         'severity': 'high'
#     }
# ]
```

---

## 5. ReportGenerator

**Responsabilité** : Génération de rapports multi-formats

### Fonctionnalités principales

#### Rapport de progression élève

```python
from core.classroom import ReportGenerator

generator = ReportGenerator(teacher_id=1)

report = generator.generate_student_progress_report(
    student_id=5,
    classroom_id=1,
    format='structured',  # ou 'csv', 'pdf'
    days_back=30
)
# Inclut :
# - Métriques d'engagement
# - Trajectoire de progression
# - Heatmap de performance
# - Rapport de compétences EN
# - Recommandations
# - Prévisions ML par domaine
```

#### Rapport élèves à risque

```python
at_risk_report = generator.generate_at_risk_report(
    classroom_id=1,
    threshold=0.40
)
# Inclut pour chaque élève à risque :
# - Score et niveau de risque
# - Top 3 lacunes de compétences
# - Niveau d'engagement
# - Recommandations d'intervention
```

#### Rapport vue d'ensemble classe

```python
class_report = generator.generate_class_overview_report(
    classroom_id=1,
    days_back=30
)
# Inclut :
# - Statistiques de classe
# - Trajectoire de progression classe
# - Vue d'ensemble compétences EN
# - Leaderboard (top 10)
# - Top 5 élèves à risque
```

#### Rapport de complétion devoir

```python
assignment_report = generator.generate_assignment_completion_report(
    assignment_id=1
)
# Inclut :
# - Taux de complétion global
# - Taux de réussite moyen
# - Élèves en difficulté
# - Top performers
```

#### Rapport de couverture curriculum

```python
coverage = generator.generate_curriculum_coverage_report(
    classroom_id=1,
    grade_level="CE2"
)
# Analyse :
# - Compétences bien couvertes (>70% maîtrise)
# - Compétences partiellement couvertes (30-70%)
# - Compétences négligées (<30% ou non tentées)
# - Répartition par domaine
# - Recommandations
```

#### Exports CSV

```python
# Export progression classe
csv_path = generator.export_class_progress_csv(
    classroom_id=1,
    output_path="reports/class_1_progress.csv"
)

# Export résultats devoir
csv_path = generator.export_assignment_results_csv(
    assignment_id=1,
    output_path="reports/assignment_1_results.csv"
)
```

#### Données pour présentation

```python
presentation_data = generator.generate_presentation_data(
    classroom_id=1,
    days_back=30
)
# Retourne données structurées pour PowerPoint/Google Slides :
# - Slide de titre
# - Slide statistiques
# - Données pour graphiques (trajectoire, compétences)
# - Leaderboard
# - Élèves à risque
```

---

## Intégration ML

Tous les modules intègrent les modèles ML de Phase 7 :

### DifficultyOptimizer
- Utilisé par `AssignmentEngine.generate_student_exercises()`
- Prédit la difficulté optimale par élève/domaine
- Applique Flow Theory (maintenir ~70% succès)

### PerformancePredictor
- Utilisé par `ClassroomManager.get_at_risk_students()`
- Utilisé par `AnalyticsEngine.forecast_student_performance()`
- Prédit la probabilité de succès
- Identifie les élèves à risque

### ExplainableAI
- Disponible pour expliquer les prédictions
- Génère des explications SHAP
- Audit de fairness

---

## Workflow enseignant typique

### 1. Configuration initiale

```python
# Créer compte enseignant (via authentification)
teacher_id = 1

# Créer classe
manager = ClassroomManager(teacher_id)
classroom = manager.create_classroom(
    name="CE2 - Classe A",
    grade_level="CE2"
)

# Ajouter élèves
for username in ["alice", "bob", "charlie", ...]:
    manager.add_student(classroom['id'], username)

# Synchroniser curriculum EN
mapper = CurriculumMapper()
mapper.sync_competencies_to_database()
```

### 2. Créer et publier un devoir

```python
engine = AssignmentEngine(teacher_id)

# Créer devoir adaptatif
assignment = engine.create_assignment(
    classroom_id=classroom['id'],
    title="Révision multiplication",
    skill_domains=["multiplication"],
    adaptive=True,
    exercise_count=10,
    due_date=datetime.now() + timedelta(days=7)
)

# Publier
engine.publish_assignment(assignment['id'])
```

### 3. Suivre la progression

```python
# Vue d'ensemble classe
overview = manager.get_classroom_overview(classroom['id'])

# Complétion devoir
completions = engine.get_assignment_completion(assignment['id'])

# Élèves à risque
at_risk = manager.get_at_risk_students(classroom['id'])
```

### 4. Générer des rapports

```python
generator = ReportGenerator(teacher_id)

# Rapport classe
class_report = generator.generate_class_overview_report(
    classroom_id=classroom['id']
)

# Rapport élève individuel
student_report = generator.generate_student_progress_report(
    student_id=5,
    classroom_id=classroom['id']
)

# Export CSV
generator.export_class_progress_csv(classroom['id'])
```

---

## Tests et validation

### Tester les modules

```python
# Test ClassroomManager
manager = ClassroomManager(teacher_id=1)
classroom = manager.create_classroom(
    name="Test Classroom",
    grade_level="CE2"
)
assert classroom['id'] > 0
assert classroom['name'] == "Test Classroom"

# Test AssignmentEngine
engine = AssignmentEngine(teacher_id=1)
assignment = engine.create_assignment(
    classroom_id=classroom['id'],
    title="Test Assignment",
    skill_domains=["addition"],
    exercise_count=5
)
assert assignment['is_published'] == False

# Test CurriculumMapper
mapper = CurriculumMapper()
result = mapper.sync_competencies_to_database()
assert result['total'] == 108

# Test AnalyticsEngine
analytics = AnalyticsEngine()
trajectory = analytics.get_student_progress_trajectory(
    student_id=1,
    days_back=7
)
assert 'data_points' in trajectory

# Test ReportGenerator
generator = ReportGenerator(teacher_id=1)
report = generator.generate_class_overview_report(
    classroom_id=classroom['id']
)
assert 'statistics' in report
```

---

## Prochaines étapes (Frontend)

### Phase 8 UI à implémenter

1. **Dashboard enseignant**
   - Vue d'ensemble de toutes les classes
   - Statistiques en temps réel
   - Alertes élèves à risque

2. **Page gestion de classe**
   - CRUD élèves
   - Visualisation progression
   - Analytics (heatmaps, trajectoires)

3. **Page création devoir**
   - Form de création
   - Sélection domaines/difficultés
   - Mode adaptatif ON/OFF

4. **Page suivi devoir**
   - Tableau de complétion
   - Graphiques de progression
   - Identification élèves en difficulté

5. **Page rapports**
   - Générateur de rapports
   - Visualisation données
   - Export PDF/CSV/PowerPoint

6. **Page compétences EN**
   - Vue d'ensemble curriculum
   - Progression par compétence
   - Couverture du programme

### APIs REST nécessaires

Créer des endpoints Flask/FastAPI :

```
POST   /api/classrooms                    # Créer classe
GET    /api/classrooms                    # Liste classes
GET    /api/classrooms/:id                # Détails classe
PUT    /api/classrooms/:id                # Modifier classe
DELETE /api/classrooms/:id                # Archiver classe

POST   /api/classrooms/:id/students       # Ajouter élève
DELETE /api/classrooms/:id/students/:sid  # Retirer élève
GET    /api/classrooms/:id/overview       # Vue d'ensemble
GET    /api/classrooms/:id/at-risk        # Élèves à risque

POST   /api/assignments                   # Créer devoir
GET    /api/assignments                   # Liste devoirs
POST   /api/assignments/:id/publish       # Publier devoir
GET    /api/assignments/:id/completion    # Complétion
GET    /api/assignments/:id/exercises     # Exercices élève

GET    /api/analytics/trajectory          # Trajectoire
GET    /api/analytics/heatmap             # Heatmap
GET    /api/analytics/forecast            # Prévisions
GET    /api/analytics/engagement          # Engagement

GET    /api/curriculum/competencies       # Compétences
GET    /api/curriculum/student-progress   # Progression élève
GET    /api/curriculum/gaps               # Lacunes
GET    /api/curriculum/recommendations    # Recommandations

POST   /api/reports/student-progress      # Rapport élève
POST   /api/reports/class-overview        # Rapport classe
POST   /api/reports/assignment            # Rapport devoir
POST   /api/reports/curriculum-coverage   # Couverture curriculum
GET    /api/reports/export/csv            # Export CSV
```

---

## Performance et scalabilité

### Optimisations implémentées

1. **Requêtes DB optimisées**
   - Joins efficaces avec SQLAlchemy
   - Eager loading pour relations
   - Indexes sur foreign keys

2. **Caching**
   - `@lru_cache` sur CurriculumMapper._load_curriculum_data()
   - Singleton pattern pour ML models

3. **Batch processing**
   - `bulk_update_from_exercise_history()` traite plusieurs exercices en une transaction

### Limites actuelles

- Pas de pagination sur listes longues
- Pas de cache Redis pour rapports
- Génération PDF synchrone (bloquante)

### Recommandations production

1. **Caching Redis**
   ```python
   # Cache rapports fréquents
   @cache.memoize(timeout=300)
   def get_classroom_overview(classroom_id):
       ...
   ```

2. **Task queue Celery**
   ```python
   # Génération PDF asynchrone
   @celery.task
   def generate_pdf_report(student_id):
       ...
   ```

3. **Pagination**
   ```python
   def get_classroom_students(classroom_id, page=1, per_page=20):
       ...
   ```

---

## Maintenance

### Ajouter une compétence EN

1. Éditer `data/curriculum/EN_competences_CE*.json`
2. Exécuter `mapper.sync_competencies_to_database()`

### Modifier l'algorithme de maîtrise

Éditer `CurriculumMapper.update_student_competency_progress()` :

```python
if is_correct:
    increment = 0.1 * difficulty_weight  # Ajuster ce facteur
    progress.mastery_level = min(1.0, progress.mastery_level + increment)
```

### Ajouter un nouveau type de rapport

1. Créer méthode dans `ReportGenerator`
2. Collecter données des autres modules
3. Formater selon besoin (structured/CSV/PDF)

---

## Conclusion

**Phase 8 Backend est COMPLET** et prêt pour l'intégration frontend.

### Résumé des livrables

✅ 5 modules backend (1800+ lignes)
✅ 7 tables de base de données
✅ 108 compétences Éducation Nationale
✅ Intégration complète avec ML Phase 7
✅ Analytics avancés avec prédictions
✅ Génération de rapports multi-formats
✅ Documentation complète

### Prochaine étape recommandée

**Phase 8 UI** : Créer le frontend Vue.js/React pour le dashboard enseignant.

---

**Date de complétion** : 16 novembre 2025
**Version** : MathCopain v6.2 - Phase 8 Backend
**Auteur** : Claude AI (Anthropic)

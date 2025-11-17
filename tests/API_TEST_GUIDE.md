# Guide de test API - MathCopain Phase 8

## Préparation

### 1. Installer les dépendances

```bash
cd /home/user/MathCopain_v6.2
pip install -r requirements.txt
```

### 2. Créer les données de test

```bash
# Créer la base de données et les données de test
python -m tests.seed_data
```

**Résultat attendu** :
```
✅ SEED DATA COMPLETE
📋 Summary:
  - Teacher: prof.dupont@mathcopain.fr
  - Password: password123 (for testing)
  - Classrooms: 2
  - Students: 25
  - Curriculum: 108 competencies
```

### 3. Démarrer l'API

```bash
# Terminal 1 : API Flask
python -m api.app
```

**Résultat attendu** :
```
 * Running on http://127.0.0.1:5000
```

### 4. Tester le health check

```bash
curl http://localhost:5000/api/health
```

**Résultat attendu** :
```json
{
  "status": "healthy",
  "service": "MathCopain Teacher API",
  "version": "1.0.0"
}
```

---

## Tests par endpoint

### 🏫 Classrooms (Classes)

#### 1. Liste des classes

```bash
curl -X GET http://localhost:5000/api/teacher/classrooms \
  -H "Cookie: session=test" \
  -b session_cookie.txt
```

**Réponse attendue** :
```json
{
  "success": true,
  "classrooms": [
    {
      "id": 1,
      "name": "CE2 - Classe A",
      "grade_level": "CE2",
      "student_count": 15,
      "avg_success_rate": 0.72
    },
    ...
  ]
}
```

#### 2. Détails d'une classe

```bash
curl -X GET http://localhost:5000/api/teacher/classrooms/1
```

**Vérifications** :
- ✅ Status code 200
- ✅ `success: true`
- ✅ Champs `id`, `name`, `grade_level`, `student_count`, `stats`
- ✅ Stats contient `total_students`, `avg_success_rate`, `at_risk_count`

#### 3. Créer une classe

```bash
curl -X POST http://localhost:5000/api/teacher/classrooms \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CM2 - Classe Test",
    "grade_level": "CM2",
    "school_year": "2025-2026",
    "max_students": 30
  }'
```

**Vérifications** :
- ✅ Status code 201
- ✅ Classe créée avec ID unique
- ✅ Message de confirmation

#### 4. Modifier une classe

```bash
curl -X PUT http://localhost:5000/api/teacher/classrooms/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CE2 - Classe A (Modifiée)",
    "description": "Description mise à jour"
  }'
```

#### 5. Liste des élèves d'une classe

```bash
curl -X GET http://localhost:5000/api/teacher/classrooms/1/students
```

**Vérifications** :
- ✅ Liste de 15 élèves
- ✅ Chaque élève a : `id`, `username`, `grade_level`, `success_rate`

#### 6. Ajouter un élève

```bash
curl -X POST http://localhost:5000/api/teacher/classrooms/1/students \
  -H "Content-Type: application/json" \
  -d '{"student_username": "nouveau_eleve"}'
```

**Vérifications** :
- ✅ Élève ajouté (ou erreur si n'existe pas)
- ✅ Respect de la capacité max (30 élèves)

#### 7. Élèves à risque

```bash
curl -X GET "http://localhost:5000/api/teacher/classrooms/1/at-risk?threshold=0.40"
```

**Vérifications** :
- ✅ Liste des élèves avec `risk_score > 0.40`
- ✅ Champs : `id`, `username`, `risk_score`, `risk_level`, `recommendation`

---

### 📝 Assignments (Devoirs)

#### 1. Liste des devoirs

```bash
curl -X GET http://localhost:5000/api/teacher/assignments
```

**Vérifications** :
- ✅ 4 devoirs créés par seed data
- ✅ Champs : `id`, `title`, `classroom_id`, `skill_domains`, `is_published`

#### 2. Filtrer les devoirs

```bash
# Devoirs publiés uniquement
curl -X GET "http://localhost:5000/api/teacher/assignments?status=published"

# Devoirs d'une classe
curl -X GET "http://localhost:5000/api/teacher/assignments?classroom_id=1"
```

#### 3. Créer un devoir

```bash
curl -X POST http://localhost:5000/api/teacher/assignments \
  -H "Content-Type: application/json" \
  -d '{
    "classroom_id": 1,
    "title": "Test Multiplication",
    "skill_domains": ["multiplication"],
    "exercise_count": 10,
    "due_date": "2025-12-31T23:59:59",
    "adaptive": true,
    "description": "Devoir de test"
  }'
```

**Vérifications** :
- ✅ Status 201
- ✅ Devoir créé avec `is_published: false` (brouillon)
- ✅ `is_adaptive: true`

#### 4. Publier un devoir

```bash
curl -X POST http://localhost:5000/api/teacher/assignments/1/publish
```

**Vérifications** :
- ✅ `is_published: true`
- ✅ `students_assigned: 15` (nombre d'élèves)

#### 5. Suivi de complétion

```bash
curl -X GET http://localhost:5000/api/teacher/assignments/1/completion
```

**Vérifications** :
- ✅ Liste de completions (une par élève)
- ✅ Champs : `student_id`, `student_name`, `progress`, `success_rate`, `status`

---

### 📊 Analytics

#### 1. Leaderboard

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/leaderboard?classroom_id=1&days_back=30&top_n=10"
```

**Vérifications** :
- ✅ Top 10 élèves
- ✅ Champs : `rank`, `username`, `exercises_completed`, `success_rate`, `score`
- ✅ Tri par score décroissant

#### 2. Trajectoire de progression

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/trajectory?student_id=1&skill_domain=multiplication&days_back=30&granularity=daily"
```

**Vérifications** :
- ✅ `data_points` avec dates, exercices, success_rate
- ✅ `overall_trend` (nombre)
- ✅ `trend_direction` : "improving", "declining", ou "stable"

#### 3. Heatmap de performance

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/heatmap?student_id=1&days_back=30"
```

**Vérifications** :
- ✅ Matrice domaine × difficulté
- ✅ Taux de réussite par cellule

#### 4. Prévisions ML

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/forecast?student_id=1&skill_domain=multiplication&days_ahead=7"
```

**Vérifications** :
- ✅ `current_success_probability`
- ✅ `forecast` : 7 points de données
- ✅ `risk_level` : "low", "medium", ou "high"

#### 5. Métriques d'engagement

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/engagement?student_id=1&days_back=30"
```

**Vérifications** :
- ✅ `total_exercises`
- ✅ `active_days`
- ✅ `current_streak` (jours consécutifs)
- ✅ `engagement_score` (0-100)

#### 6. Comparaison élève vs classe

```bash
curl -X GET "http://localhost:5000/api/teacher/analytics/compare?student_id=1&classroom_id=1&days_back=30"
```

**Vérifications** :
- ✅ `student_metrics` vs `class_metrics`
- ✅ `percentile` (position dans la classe)
- ✅ `relative_performance` : "above_average", "average", "below_average"

---

### 📚 Curriculum (Compétences EN)

#### 1. Liste des compétences

```bash
curl -X GET "http://localhost:5000/api/teacher/curriculum/competencies?grade_level=CE2"
```

**Vérifications** :
- ✅ 25 compétences CE2
- ✅ Champs : `code`, `title`, `description`, `domain`, `difficulty_range`

#### 2. Progression d'un élève

```bash
curl -X GET "http://localhost:5000/api/teacher/curriculum/student-progress?student_id=1&grade_level=CE2"
```

**Vérifications** :
- ✅ `summary` : total, mastered, in_progress, not_started
- ✅ `completion_rate`
- ✅ `competencies` : détails par compétence

#### 3. Vue d'ensemble classe

```bash
curl -X GET "http://localhost:5000/api/teacher/curriculum/class-overview?classroom_id=1&grade_level=CE2"
```

**Vérifications** :
- ✅ `avg_class_mastery`
- ✅ Stats par compétence : `students_mastered`, `mastery_rate`

#### 4. Lacunes d'un élève

```bash
curl -X GET "http://localhost:5000/api/teacher/curriculum/gaps?student_id=1&grade_level=CE2"
```

**Vérifications** :
- ✅ Compétences triées par `priority_score`
- ✅ `reason` : explique pourquoi c'est une lacune

#### 5. Recommandations

```bash
curl -X GET "http://localhost:5000/api/teacher/curriculum/recommendations?student_id=1&grade_level=CE2&count=3"
```

**Vérifications** :
- ✅ Top 3 compétences à travailler
- ✅ `recommendation` : texte explicatif

---

### 📄 Reports (Rapports)

#### 1. Rapport vue d'ensemble classe

```bash
curl -X POST http://localhost:5000/api/teacher/reports/class-overview \
  -H "Content-Type: application/json" \
  -d '{"classroom_id": 1, "days_back": 30}'
```

**Vérifications** :
- ✅ `report` contient : `classroom`, `statistics`, `trajectory`, `leaderboard`, `at_risk_students`

#### 2. Rapport élèves à risque

```bash
curl -X POST http://localhost:5000/api/teacher/reports/at-risk \
  -H "Content-Type: application/json" \
  -d '{"classroom_id": 1, "threshold": 0.40}'
```

**Vérifications** :
- ✅ `total_at_risk`
- ✅ Liste détaillée avec `competency_gaps`, `engagement_level`

#### 3. Rapport de progression élève

```bash
curl -X POST http://localhost:5000/api/teacher/reports/student-progress \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "classroom_id": 1, "format": "structured", "days_back": 30}'
```

**Vérifications** :
- ✅ `engagement`, `trajectory`, `performance_heatmap`, `competencies`, `recommendations`, `forecasts`

#### 4. Rapport de complétion devoir

```bash
curl -X POST http://localhost:5000/api/teacher/reports/assignment \
  -H "Content-Type: application/json" \
  -d '{"assignment_id": 1}'
```

**Vérifications** :
- ✅ `summary` : `completion_rate`, `avg_success_rate`
- ✅ `struggling_students`, `top_performers`

#### 5. Rapport couverture curriculum

```bash
curl -X POST http://localhost:5000/api/teacher/reports/curriculum-coverage \
  -H "Content-Type: application/json" \
  -d '{"classroom_id": 1, "grade_level": "CE2"}'
```

**Vérifications** :
- ✅ `well_covered`, `partially_covered`, `neglected`
- ✅ `domain_breakdown`
- ✅ `recommendations`

#### 6. Export CSV

```bash
curl -X POST http://localhost:5000/api/teacher/reports/export/csv \
  -H "Content-Type: application/json" \
  -d '{"report_type": "class_progress", "classroom_id": 1}'
```

**Vérifications** :
- ✅ `csv_path` retourné
- ✅ Fichier CSV créé dans `reports/`

---

## Tests d'erreurs

### 1. Authentification manquante

```bash
# Sans authentification (pas de session)
curl -X GET http://localhost:5000/api/teacher/classrooms
```

**Résultat attendu** :
```json
{
  "error": "Authentication required"
}
```
**Status** : 401

### 2. Ressource introuvable

```bash
curl -X GET http://localhost:5000/api/teacher/classrooms/9999
```

**Résultat attendu** :
```json
{
  "error": "Classroom not found"
}
```
**Status** : 404

### 3. Données invalides

```bash
curl -X POST http://localhost:5000/api/teacher/classrooms \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "grade_level": "INVALID"}'
```

**Résultat attendu** : Status 400

---

## Checklist complète

### ✅ Classrooms
- [ ] GET /classrooms
- [ ] POST /classrooms
- [ ] GET /classrooms/:id
- [ ] PUT /classrooms/:id
- [ ] DELETE /classrooms/:id
- [ ] GET /classrooms/:id/students
- [ ] POST /classrooms/:id/students
- [ ] DELETE /classrooms/:id/students/:sid
- [ ] GET /classrooms/:id/at-risk

### ✅ Assignments
- [ ] GET /assignments
- [ ] POST /assignments
- [ ] GET /assignments/:id
- [ ] POST /assignments/:id/publish
- [ ] PUT /assignments/:id
- [ ] DELETE /assignments/:id
- [ ] GET /assignments/:id/completion

### ✅ Analytics
- [ ] GET /analytics/trajectory
- [ ] GET /analytics/heatmap
- [ ] GET /analytics/forecast
- [ ] GET /analytics/engagement
- [ ] GET /analytics/compare
- [ ] GET /analytics/leaderboard

### ✅ Curriculum
- [ ] GET /curriculum/competencies
- [ ] GET /curriculum/student-progress
- [ ] GET /curriculum/class-overview
- [ ] GET /curriculum/gaps
- [ ] GET /curriculum/recommendations

### ✅ Reports
- [ ] POST /reports/student-progress
- [ ] POST /reports/class-overview
- [ ] POST /reports/at-risk
- [ ] POST /reports/assignment
- [ ] POST /reports/curriculum-coverage
- [ ] POST /reports/export/csv

### ✅ Auth & Errors
- [ ] 401 sur endpoints protégés
- [ ] 404 sur ressources introuvables
- [ ] 400 sur données invalides

---

## Conclusion

Une fois tous les tests passés :

1. ✅ **40+ endpoints fonctionnels**
2. ✅ **Données cohérentes**
3. ✅ **Gestion d'erreurs correcte**
4. ✅ **Intégration ML opérationnelle**

**Prêt pour les tests frontend !**

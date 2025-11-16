# 🎓 PHASE 8 - ARCHITECTURE TECHNIQUE
## Déploiement Institutionnel - MathCopain v6.4

**Date de début:** 2025-11-16
**Durée estimée:** 24 semaines
**Status:** 🚧 En cours

---

## 🎯 OBJECTIFS PHASE 8

### 8.1 - Mode Enseignant & Classe (14 semaines)
- Interface professionnelle pour enseignants
- Gestion complète des classes (30 élèves max/classe)
- Système d'assignments avec deadlines
- Monitoring temps réel de la progression
- Rapports détaillés par élève et par classe
- Mapping curriculum Éducation Nationale

### 8.2 - Analytics Dashboard Complet (10 semaines)
- Visualizations interactives (Plotly)
- Heatmaps de compétences
- Trajectoires de progression
- Prédictions ML intégrées
- Export multi-formats (PDF/CSV/PowerPoint)

---

## 📊 ARCHITECTURE BASE DE DONNÉES (Extension Phase 7)

### Nouvelles Tables PostgreSQL (5 tables)

```sql
-- 1. Teacher Accounts (Comptes enseignants)
CREATE TABLE teacher_accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    school_name VARCHAR(100),
    grade_levels VARCHAR(50),  -- JSON array: ["CE1", "CE2"]
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    INDEX idx_teacher_email (email),
    INDEX idx_teacher_active (is_active)
);

-- 2. Classrooms (Classes)
CREATE TABLE classrooms (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES teacher_accounts(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,  -- "CE2 - Classe A"
    grade_level VARCHAR(10) NOT NULL,  -- "CE2"
    school_year VARCHAR(10),  -- "2025-2026"
    max_students INTEGER DEFAULT 30,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_classroom_teacher (teacher_id),
    INDEX idx_classroom_active (is_active)
);

-- 3. Classroom Enrollments (Inscriptions élèves)
CREATE TABLE classroom_enrollments (
    id SERIAL PRIMARY KEY,
    classroom_id INTEGER REFERENCES classrooms(id) ON DELETE CASCADE,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'active',  -- active, completed, withdrawn

    UNIQUE (classroom_id, student_id),
    INDEX idx_enrollment_classroom (classroom_id),
    INDEX idx_enrollment_student (student_id)
);

-- 4. Assignments (Devoirs/Exercices assignés)
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    classroom_id INTEGER REFERENCES classrooms(id) ON DELETE CASCADE,
    teacher_id INTEGER REFERENCES teacher_accounts(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    skill_domains JSONB,  -- ["addition", "multiplication"]
    difficulty_levels JSONB,  -- [2, 3, 4]
    exercise_count INTEGER DEFAULT 10,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    is_published BOOLEAN DEFAULT FALSE,

    INDEX idx_assignment_classroom (classroom_id),
    INDEX idx_assignment_due (due_date)
);

-- 5. Assignment Completions (Complétion des devoirs)
CREATE TABLE assignment_completions (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exercises_completed INTEGER DEFAULT 0,
    exercises_total INTEGER,
    success_rate FLOAT,
    time_spent_seconds INTEGER,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'in_progress',  -- in_progress, completed, overdue

    UNIQUE (assignment_id, student_id),
    INDEX idx_completion_assignment (assignment_id),
    INDEX idx_completion_student (student_id)
);

-- 6. Curriculum Competencies (Compétences curriculum EN)
CREATE TABLE curriculum_competencies (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,  -- "NUM.CE2.01"
    grade_level VARCHAR(10) NOT NULL,  -- "CE2"
    domain VARCHAR(50) NOT NULL,  -- "Nombres et calculs"
    subdomain VARCHAR(100),  -- "Addition et soustraction"
    description TEXT,
    skill_domains JSONB,  -- Mapping vers nos domaines
    examples TEXT,

    INDEX idx_competency_grade (grade_level),
    INDEX idx_competency_domain (domain)
);

-- 7. Student Competency Progress (Progression compétences)
CREATE TABLE student_competency_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    competency_id INTEGER REFERENCES curriculum_competencies(id),
    proficiency_level FLOAT CHECK (proficiency_level BETWEEN 0 AND 1),
    exercises_done INTEGER DEFAULT 0,
    last_practiced TIMESTAMP,
    mastery_achieved BOOLEAN DEFAULT FALSE,
    mastery_date TIMESTAMP,

    UNIQUE (student_id, competency_id),
    INDEX idx_progress_student (student_id),
    INDEX idx_progress_competency (competency_id)
);
```

---

## 🏗️ STRUCTURE FICHIERS PHASE 8

```
MathCopain_v6.2/
│
├── core/
│   ├── pedagogy/          # (Existant - Phase 6)
│   ├── ml/                # (Existant - Phase 7)
│   │
│   ├── classroom/         # NOUVEAU - Phase 8.1
│   │   ├── __init__.py
│   │   ├── classroom_manager.py      # Gestion classes (500 lignes)
│   │   ├── assignment_engine.py      # Système devoirs (350 lignes)
│   │   ├── student_monitor.py        # Monitoring temps réel (300 lignes)
│   │   └── curriculum_mapper.py      # Mapping EN (250 lignes)
│   │
│   └── analytics/         # NOUVEAU - Phase 8.2
│       ├── __init__.py
│       ├── analytics_engine.py       # Moteur analytics (500 lignes)
│       ├── visualization.py          # Plotly viz (400 lignes)
│       ├── report_generator.py       # PDF/CSV/PPT (350 lignes)
│       └── forecast_engine.py        # Prédictions ML (300 lignes)
│
├── ui/
│   ├── exercise_sections.py  # (Existant)
│   ├── math_sections.py       # (Existant)
│   │
│   ├── teacher/               # NOUVEAU - Dashboard enseignant
│   │   ├── __init__.py
│   │   ├── dashboard.py              # Dashboard principal (500 lignes)
│   │   ├── classroom_view.py         # Vue classe (400 lignes)
│   │   ├── student_detail_view.py    # Détail élève (350 lignes)
│   │   ├── assignment_creator.py     # Créer devoirs (300 lignes)
│   │   └── reports_view.py           # Rapports (350 lignes)
│   │
│   └── student/               # Interface élève (refactorisée)
│       └── assignment_view.py        # Vue devoirs élève (250 lignes)
│
├── data/
│   └── curriculum/            # NOUVEAU - Curriculum EN
│       ├── EN_competences_CE1.json
│       ├── EN_competences_CE2.json
│       ├── EN_competences_CM1.json
│       ├── EN_competences_CM2.json
│       └── mapping_domains.json      # Mapping vers nos domaines
│
├── database/
│   └── migrations/
│       └── versions/
│           └── 20251116_002_teacher_tables.py  # Migration Phase 8
│
└── templates/                 # NOUVEAU - Templates rapports
    ├── report_student.html           # Template rapport élève
    ├── report_classroom.html         # Template rapport classe
    └── certificate.html              # Certificat de maîtrise
```

---

## 🎨 INTERFACE ENSEIGNANT - ARCHITECTURE UI

### Navigation & Structure

```
┌────────────────────────────────────────────────────────────┐
│  MathCopain Enseignant - Mme Dupont         🏠 ⚙️ 👤       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Sidebar:                          Main Content:           │
│  ┌──────────────────┐             ┌──────────────────────┐│
│  │ 📚 Mes Classes   │             │                      ││
│  │   • CE2-A (28)   │◄────────────│  [Contenu actif]     ││
│  │   • CE2-B (25)   │             │                      ││
│  │                  │             │                      ││
│  │ 📝 Devoirs       │             │                      ││
│  │ 📊 Statistiques  │             │                      ││
│  │ 📈 Analytics     │             │                      ││
│  │ 🎯 Compétences   │             │                      ││
│  │ 📄 Rapports      │             │                      ││
│  └──────────────────┘             └──────────────────────┘│
└────────────────────────────────────────────────────────────┘
```

### Page 1: Dashboard Overview

```python
# ui/teacher/dashboard.py

def render_teacher_dashboard(teacher_id: int):
    """
    Dashboard principal enseignant

    Affiche:
    - Métriques globales (toutes classes)
    - Classes actives
    - Devoirs en cours
    - Alertes élèves à risque
    - Activité récente
    """

    st.title("📚 Tableau de Bord Enseignant")

    # Métriques globales (4 colonnes)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Élèves", "53", "+3 cette semaine")

    with col2:
        st.metric("Classes Actives", "2", "CE2-A, CE2-B")

    with col3:
        st.metric("Devoirs Actifs", "5", "3 à corriger")

    with col4:
        st.metric("Taux Réussite Moyen", "74%", "+2%")

    # Alertes élèves à risque
    st.subheader("🚨 Élèves Nécessitant Attention")

    at_risk_students = get_at_risk_students(teacher_id)

    for student in at_risk_students[:5]:  # Top 5
        with st.expander(f"⚠️ {student['name']} - {student['risk_level']}"):
            st.write(f"Classe: {student['classroom']}")
            st.write(f"Domaine: {student['struggling_domain']}")
            st.write(f"Taux réussite: {student['success_rate']:.0%}")
            st.write(f"Recommandation: {student['recommendation']}")

            if st.button("Créer exercices ciblés", key=f"help_{student['id']}"):
                create_remediation_assignment(student['id'])

    # Classes actives
    st.subheader("📚 Mes Classes")

    classrooms = get_teacher_classrooms(teacher_id)

    for classroom in classrooms:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.write(f"### {classroom['name']}")
                st.write(f"{classroom['student_count']} élèves")

            with col2:
                st.metric("Moyenne classe", f"{classroom['avg_success']:.0%}")

            with col3:
                if st.button("Voir détails", key=f"class_{classroom['id']}"):
                    st.session_state.active_classroom = classroom['id']
                    st.rerun()
```

### Page 2: Vue Classe Détaillée

```python
# ui/teacher/classroom_view.py

def render_classroom_detail(classroom_id: int):
    """
    Vue détaillée d'une classe

    Affiche:
    - Liste des élèves avec métriques
    - Grille de compétences (heatmap)
    - Activité récente
    - Devoirs actifs
    """

    classroom = get_classroom(classroom_id)

    st.title(f"📚 {classroom['name']}")
    st.caption(f"{classroom['student_count']} élèves • {classroom['grade_level']}")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Élèves",
        "🎯 Compétences",
        "📝 Devoirs",
        "📊 Statistiques"
    ])

    with tab1:
        # Tableau élèves
        students = get_classroom_students(classroom_id)

        # Filtres
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Rechercher élève", "")
        with col2:
            sort_by = st.selectbox("Trier par", [
                "Nom (A-Z)",
                "Taux réussite",
                "Dernière activité",
                "À risque"
            ])

        # Grille élèves
        for student in students:
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

                with col1:
                    risk_icon = "🚨" if student['at_risk'] else "✅"
                    st.write(f"{risk_icon} **{student['name']}**")

                with col2:
                    st.metric("Réussite", f"{student['success_rate']:.0%}")

                with col3:
                    st.metric("Exercices", student['exercises_completed'])

                with col4:
                    st.write(f"🕐 {student['last_activity']}")

                with col5:
                    if st.button("👁️", key=f"view_{student['id']}"):
                        st.session_state.active_student = student['id']
                        st.switch_page("pages/student_detail.py")

    with tab2:
        # Heatmap compétences
        st.subheader("🗺️ Carte des Compétences")

        competency_matrix = get_classroom_competency_matrix(classroom_id)

        # Plotly heatmap
        import plotly.graph_objects as go

        fig = go.Figure(data=go.Heatmap(
            z=competency_matrix['data'],
            x=competency_matrix['domains'],
            y=competency_matrix['students'],
            colorscale='RdYlGn',
            colorbar=dict(title="Maîtrise")
        ))

        fig.update_layout(
            title="Maîtrise par Élève et Domaine",
            xaxis_title="Domaines",
            yaxis_title="Élèves"
        )

        st.plotly_chart(fig, use_container_width=True)
```

### Page 3: Créateur de Devoirs

```python
# ui/teacher/assignment_creator.py

def render_assignment_creator(classroom_id: int):
    """
    Interface création de devoirs

    Permet de:
    - Choisir domaines et difficultés
    - Définir nombre d'exercices
    - Fixer deadline
    - Prévisualiser
    - Publier
    """

    st.title("📝 Créer un Devoir")

    with st.form("create_assignment"):
        # Titre
        title = st.text_input(
            "Titre du devoir*",
            placeholder="Ex: Révision multiplication - Semaine 23"
        )

        # Description
        description = st.text_area(
            "Instructions pour les élèves",
            placeholder="Révisez vos tables de multiplication...",
            height=100
        )

        # Domaines
        col1, col2 = st.columns(2)

        with col1:
            domains = st.multiselect(
                "Domaines mathématiques*",
                options=[
                    "addition", "soustraction", "multiplication",
                    "division", "fractions", "decimaux",
                    "geometrie", "mesures", "proportionnalite"
                ],
                default=["multiplication"]
            )

        with col2:
            difficulty_levels = st.multiselect(
                "Niveaux de difficulté*",
                options=["D1 (Facile)", "D2", "D3 (Moyen)", "D4", "D5 (Difficile)"],
                default=["D2", "D3"]
            )

        # Paramètres
        col3, col4 = st.columns(2)

        with col3:
            exercise_count = st.number_input(
                "Nombre d'exercices",
                min_value=5,
                max_value=50,
                value=10
            )

        with col4:
            due_date = st.date_input(
                "Date limite",
                value=datetime.now() + timedelta(days=7)
            )

        # Adaptation par élève
        adaptive = st.checkbox(
            "📊 Adaptation automatique par élève (ML)",
            value=True,
            help="Ajuste la difficulté selon le niveau de chaque élève"
        )

        # Prévisualisation
        if st.form_submit_button("👁️ Prévisualiser", type="secondary"):
            st.info("Prévisualisation des exercices...")
            preview_assignment(domains, difficulty_levels, exercise_count)

        # Création
        col_save, col_publish = st.columns(2)

        with col_save:
            if st.form_submit_button("💾 Enregistrer brouillon"):
                save_assignment_draft()

        with col_publish:
            if st.form_submit_button("✅ Publier", type="primary"):
                publish_assignment(
                    classroom_id=classroom_id,
                    title=title,
                    description=description,
                    domains=domains,
                    difficulty_levels=difficulty_levels,
                    exercise_count=exercise_count,
                    due_date=due_date,
                    adaptive=adaptive
                )
                st.success("✅ Devoir publié avec succès!")
                st.balloons()
```

---

## 📊 ANALYTICS ENGINE - ARCHITECTURE

### Composants Principaux

```python
# core/analytics/analytics_engine.py

class AnalyticsEngine:
    """
    Moteur d'analytics pour enseignants

    Génère:
    1. Trajectoires de progression
    2. Heatmaps de compétences
    3. Analyses comparatives
    4. Prédictions ML
    5. Rapports exportables
    """

    def __init__(self):
        self.db = get_session()
        self.ml_predictor = PerformancePredictor()

    def generate_progress_trajectory(
        self,
        student_id: int,
        domain: str,
        time_range: str = "30d"
    ) -> pd.DataFrame:
        """
        Génère trajectoire de progression pour un élève

        Returns:
            DataFrame avec colonnes: date, proficiency, exercises_done
        """

    def generate_classroom_heatmap(
        self,
        classroom_id: int,
        competency_type: str = "domains"
    ) -> Dict:
        """
        Génère heatmap classe × compétences

        Returns:
            {
                'students': ['Alice', 'Bob', ...],
                'domains': ['addition', 'multiplication', ...],
                'data': [[0.8, 0.6], [0.9, 0.7], ...]  # Matrice NxM
            }
        """

    def generate_comparative_analysis(
        self,
        student_id: int,
        classroom_id: int
    ) -> Dict:
        """
        Compare un élève à sa classe

        Returns:
            {
                'student_avg': 0.75,
                'class_avg': 0.68,
                'percentile': 68,  # Top 32%
                'strengths': ['addition', 'geometrie'],
                'areas_for_improvement': ['division']
            }
        """

    def generate_forecast(
        self,
        student_id: int,
        domain: str,
        horizon_days: int = 30
    ) -> Dict:
        """
        Prédictions ML pour les 30 prochains jours

        Returns:
            {
                'current_proficiency': 0.65,
                'predicted_proficiency_30d': 0.82,
                'confidence_interval': (0.78, 0.86),
                'predicted_mastery_date': '2025-12-15',
                'recommended_exercises': 45
            }
        """
```

---

## 📄 GÉNÉRATEUR DE RAPPORTS

### Formats Supportés

1. **PDF** - Rapports formels (ReportLab)
2. **CSV** - Export données brutes
3. **PowerPoint** - Présentations parents/direction (python-pptx)
4. **HTML** - Rapports web interactifs

### Types de Rapports

```python
# core/analytics/report_generator.py

class ReportGenerator:
    """Génère rapports multi-formats"""

    def generate_student_report(
        self,
        student_id: int,
        period: str = "trimester",
        format: str = "pdf"
    ) -> str:
        """
        Rapport individuel élève

        Contenu:
        - Résumé période
        - Progression par domaine
        - Compétences EN atteintes
        - Points forts / à améliorer
        - Recommandations personnalisées
        - Graphiques évolution

        Returns:
            filepath: Chemin vers fichier généré
        """

    def generate_classroom_report(
        self,
        classroom_id: int,
        format: str = "pdf"
    ) -> str:
        """
        Rapport classe complète

        Contenu:
        - Statistiques globales
        - Distribution des niveaux
        - Heatmap compétences
        - Top performers / À risque
        - Analyse comparative par domaine
        - Recommandations pédagogiques
        """

    def generate_competency_certificate(
        self,
        student_id: int,
        competency_id: int
    ) -> str:
        """
        Certificat de maîtrise compétence EN

        Format: PDF avec design officiel
        Contenu:
        - Nom élève
        - Compétence maîtrisée
        - Date de maîtrise
        - Signature enseignant (numérique)
        """
```

---

## 🗺️ CURRICULUM ÉDUCATION NATIONALE

### Structure Données Curriculum

```json
// data/curriculum/EN_competences_CE2.json

{
  "grade_level": "CE2",
  "competencies": [
    {
      "code": "NUM.CE2.01",
      "domain": "Nombres et calculs",
      "subdomain": "Connaître les nombres entiers",
      "description": "Lire, écrire, décomposer les nombres jusqu'à 1000",
      "examples": [
        "Lire 347 en lettres",
        "Décomposer 256 = 200 + 50 + 6"
      ],
      "mapped_skills": ["addition", "soustraction"],
      "difficulty_range": [1, 3],
      "mastery_threshold": 0.80
    },
    {
      "code": "NUM.CE2.02",
      "domain": "Nombres et calculs",
      "subdomain": "Additionner",
      "description": "Maîtriser l'addition posée de nombres à 3 chiffres",
      "mapped_skills": ["addition"],
      "difficulty_range": [2, 4]
    },
    // ... 50+ compétences CE2
  ]
}
```

### Mapping Automatique

```python
# core/classroom/curriculum_mapper.py

class CurriculumMapper:
    """Map nos exercices aux compétences EN"""

    def map_exercise_to_competencies(
        self,
        exercise_result: ExerciseResponse
    ) -> List[str]:
        """
        Identifie quelles compétences EN sont travaillées

        Returns:
            ['NUM.CE2.02', 'NUM.CE2.05']
        """

    def update_student_competency_progress(
        self,
        student_id: int,
        competency_codes: List[str],
        success: bool
    ):
        """
        Met à jour la progression des compétences EN
        """

    def get_student_competency_report(
        self,
        student_id: int
    ) -> Dict:
        """
        Rapport compétences EN pour un élève

        Returns:
            {
                'total_competencies': 52,
                'mastered': 38,
                'in_progress': 10,
                'not_started': 4,
                'mastery_rate': 0.73,
                'details': [...]
            }
        """
```

---

## 📈 MÉTRIQUES & KPI ENSEIGNANT

### Dashboard Metrics

```python
TEACHER_METRICS = {
    # Engagement élèves
    'active_students_7d': "Élèves actifs cette semaine",
    'avg_exercises_per_student': "Moyenne exercices/élève",
    'avg_session_duration': "Durée moyenne session",

    # Performance classe
    'class_avg_success_rate': "Taux réussite classe",
    'improvement_trend': "Tendance progression",
    'at_risk_count': "Élèves à risque",

    # Compétences
    'competencies_mastered': "Compétences maîtrisées",
    'competencies_in_progress': "En cours d'acquisition",

    # Devoirs
    'assignments_active': "Devoirs actifs",
    'assignments_completion_rate': "Taux complétion devoirs",
    'avg_time_to_complete': "Temps moyen complétion"
}
```

---

## 🔐 PERMISSIONS & SÉCURITÉ

### Rôles & Accès

```python
ROLES = {
    'student': {
        'can_view': ['own_profile', 'own_exercises', 'own_assignments'],
        'can_edit': ['own_profile_limited'],
        'cannot': ['view_other_students', 'create_assignments']
    },

    'teacher': {
        'can_view': ['own_classes', 'enrolled_students', 'all_analytics'],
        'can_create': ['assignments', 'classes'],
        'can_edit': ['own_classes', 'assignments'],
        'can_delete': ['own_assignments'],
        'cannot': ['view_other_teachers_data', 'delete_student_data']
    },

    'admin': {
        'can_do': ['everything'],
        'can_manage': ['teachers', 'students', 'classrooms']
    }
}
```

---

## 🚀 DÉPLOIEMENT & SCALABILITÉ

### Architecture Cible

```
┌──────────────────────────────────────────────────┐
│  NGINX Load Balancer                             │
├──────────────────────────────────────────────────┤
│                      ↓                            │
│  ┌────────────────┐  ┌────────────────┐         │
│  │ Streamlit App 1│  │ Streamlit App 2│ ...     │
│  │ (Workers)      │  │ (Workers)      │         │
│  └────────────────┘  └────────────────┘         │
│           ↓                   ↓                   │
│  ┌──────────────────────────────────────┐       │
│  │  PostgreSQL (RDS Multi-AZ)           │       │
│  │  - Read Replicas                     │       │
│  │  - Automatic Backups                 │       │
│  └──────────────────────────────────────┘       │
│           ↓                                       │
│  ┌──────────────────────────────────────┐       │
│  │  Redis Cache (ElastiCache)           │       │
│  │  - Session storage                   │       │
│  │  - Query caching                     │       │
│  └──────────────────────────────────────┘       │
└──────────────────────────────────────────────────┘

Support: 50+ enseignants, 1000+ élèves simultanés
```

---

## 📊 STATISTIQUES PHASE 8

**Code à produire:**
- 18+ nouveaux fichiers
- ~5,500 lignes de code
- 7 nouvelles tables PostgreSQL
- 5+ visualizations Plotly
- 3 formats de rapports (PDF/CSV/PPT)

**Tests attendus:**
- 700+ tests unitaires (8.1)
- 700+ tests analytics (8.2)
- Coverage: 85%+

---

**Document créé:** 2025-11-16
**Responsable:** Équipe MathCopain
**Prochaine révision:** Après semaine 14

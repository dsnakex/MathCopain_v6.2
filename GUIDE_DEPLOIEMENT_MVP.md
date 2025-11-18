# 🚀 GUIDE DÉPLOIEMENT MVP - MathCopain
## Phase 7 ML + Améliorations Pré-Déploiement

---

# 🎯 CONTEXTE STRATÉGIQUE

Vous avez finalisé **Phase 7 (PostgreSQL + ML)** et voulez déployer un **MVP fonctionnel** pour tests utilisateurs (parents + enfants) AVANT d'ajouter le dashboard enseignant complet.

**Décision validée:** 
- ✅ Phase 6: Feedback pédagogique
- ✅ Phase 7: PostgreSQL + ML adaptatif
- ❌ Phase 8: Dashboard enseignant (reporté post-MVP)
- ✅ Améliorations MVP critiques (ce document)

---

# 📋 AMÉLIORATIONS CRITIQUES PRÉ-DÉPLOIEMENT

## Vue d'ensemble

| Amélioration | Priorité | Temps Estimé | Impact Adoption |
|--------------|----------|--------------|-----------------|
| 1. Dashboard Parents Simplifié | 🔴 CRITIQUE | 2 jours | +40% rétention |
| 2. Onboarding Interactif | 🔴 CRITIQUE | 1 jour | +35% engagement |
| 3. Gamification Basique | 🟡 HAUTE | 1 jour | +30% motivation |
| 4. RGPD & Sécurité | 🔴 CRITIQUE | 1 jour | Obligatoire légal |
| 5. Tests Performance | 🟡 HAUTE | 0.5 jour | Scalabilité |
| 6. Accessibilité | 🟢 MOYENNE | 0.5 jour | Inclusion |
| 7. Documentation Utilisateur | 🟡 HAUTE | 1 jour | Support réduit |

**Total estimé:** 7-8 jours de développement

---

# 🎯 AMÉLIORATION 1: DASHBOARD PARENTS SIMPLIFIÉ

## Objectif
Donner aux parents une vue claire de la progression de leur enfant sans complexité excessive.

## Prompt Claude Code 1.1 - Backend Dashboard Parents

**Titre:** "Créer ParentDashboard backend - Vue progression enfant"

**Texte du Prompt:**

```
# CONTEXTE
MathCopain Phase 7 est terminée (PostgreSQL + ML adaptatif).
Avant déploiement MVP, ajouter dashboard parents SIMPLIFIÉ.

# TÂCHE: Backend Dashboard Parents

## Fichier à créer
`core/analytics/parent_dashboard.py` (200 lignes)

## Classe ParentDashboardAnalytics

```python
class ParentDashboardAnalytics:
    """Analytics simplifiées pour parents"""
    
    def __init__(self, child_user_id):
        self.child_id = child_user_id
        self.db = get_db_connection()
    
    def get_weekly_summary(self):
        '''
        Retourne résumé 7 derniers jours:
        {
            "time_spent_minutes": 135,
            "exercises_completed": 28,
            "success_rate": 0.78,
            "success_rate_change": +0.05,  # vs semaine précédente
            "streak_days": 5
        }
        '''
    
    def get_top_skills(self, limit=5):
        '''
        Top 5 compétences travaillées:
        [
            {"skill": "Addition (CE2)", "status": "Maîtrisée", "icon": "✅"},
            {"skill": "Soustraction retenue", "status": "En cours", "icon": "🔄"},
            {"skill": "Multiplication tables", "status": "À venir", "icon": "⏳"}
        ]
        '''
    
    def get_strengths_weaknesses(self):
        '''
        3 points forts + 3 points à améliorer:
        {
            "strengths": [
                "Très bon en calcul mental",
                "Progresse vite en géométrie",
                "Régulier dans sa pratique"
            ],
            "improvements": [
                "Ralentir sur les problèmes",
                "Relire les énoncés",
                "Revoir les fractions"
            ]
        }
        '''
    
    def get_suggested_exercises(self):
        '''
        Suggestions personnalisées:
        [
            {"domain": "Fractions", "difficulty": 2, "reason": "Point faible identifié"},
            {"domain": "Géométrie", "difficulty": 3, "reason": "Poursuivre les progrès"}
        ]
        '''
    
    def get_progress_chart_data(self, days=7):
        '''
        Données pour graphique progression:
        {
            "dates": ["2025-11-11", "2025-11-12", ...],
            "time_minutes": [20, 15, 30, ...],
            "success_rates": [0.75, 0.80, 0.78, ...]
        }
        '''
```

## Requêtes SQL Optimisées

```python
# Utiliser PostgreSQL existant (Phase 7)
def get_weekly_summary(self):
    query = '''
    SELECT 
        COUNT(*) as exercises_completed,
        SUM(time_taken_seconds)/60 as time_minutes,
        AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as success_rate
    FROM exercise_responses
    WHERE user_id = %s 
      AND created_at >= NOW() - INTERVAL '7 days'
    '''
    result = self.db.execute(query, (self.child_id,))
    
    # Comparer avec semaine précédente
    prev_week = self.db.execute(query_prev_week, (self.child_id,))
    
    return {
        "time_spent_minutes": result['time_minutes'],
        "exercises_completed": result['exercises_completed'],
        "success_rate": result['success_rate'],
        "success_rate_change": result['success_rate'] - prev_week['success_rate']
    }
```

## Tests
`tests/test_parent_dashboard.py` (150+ tests)

Coverage: 85%+

Test scenarios:
- Weekly summary calculation accuracy
- Top skills correct ordering
- Strengths/weaknesses detection
- Empty data (new user) handling
- Performance (<500ms queries)
```

---

## Prompt Claude Code 1.2 - UI Dashboard Parents

**Titre:** "Créer Parent Dashboard UI Streamlit"

**Texte:**

```
# TÂCHE: UI Dashboard Parents

Interface Streamlit simple et claire pour parents.

## Fichier à créer
`ui/parent_dashboard_ui.py` (150 lignes)

## Structure UI

```python
import streamlit as st
from core.analytics.parent_dashboard import ParentDashboardAnalytics

def render_parent_dashboard(child_user_id, child_name):
    st.title(f"📊 Progression de {child_name}")
    
    # Instancier analytics
    analytics = ParentDashboardAnalytics(child_user_id)
    
    # Section 1: Résumé hebdomadaire
    st.subheader("Cette semaine")
    weekly = analytics.get_weekly_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Temps passé", 
            f"{weekly['time_spent_minutes']} min",
            delta=f"+{weekly['time_change']} min"
        )
    with col2:
        st.metric(
            "Exercices", 
            weekly['exercises_completed']
        )
    with col3:
        delta_pct = f"{weekly['success_rate_change']*100:+.0f}%"
        st.metric(
            "Taux de réussite", 
            f"{weekly['success_rate']*100:.0f}%",
            delta=delta_pct
        )
    
    # Section 2: Graphique progression
    st.subheader("Progression sur 7 jours")
    chart_data = analytics.get_progress_chart_data()
    
    # Utiliser Streamlit charts (simple)
    import pandas as pd
    df = pd.DataFrame({
        'Date': chart_data['dates'],
        'Temps (min)': chart_data['time_minutes'],
        'Réussite (%)': [r*100 for r in chart_data['success_rates']]
    })
    st.line_chart(df.set_index('Date'))
    
    # Section 3: Compétences travaillées
    st.subheader("🎯 Compétences travaillées")
    skills = analytics.get_top_skills(limit=5)
    
    for skill in skills:
        col_icon, col_name, col_status = st.columns([1, 6, 3])
        with col_icon:
            st.write(skill['icon'])
        with col_name:
            st.write(skill['skill'])
        with col_status:
            st.write(skill['status'])
    
    # Section 4: Points forts / À améliorer
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💪 Points forts")
        strengths = analytics.get_strengths_weaknesses()['strengths']
        for s in strengths:
            st.success(f"✓ {s}")
    
    with col_right:
        st.subheader("📈 À améliorer")
        improvements = analytics.get_strengths_weaknesses()['improvements']
        for i in improvements:
            st.info(f"→ {i}")
    
    # Section 5: Suggestions
    st.subheader("💡 Suggestions d'exercices")
    suggestions = analytics.get_suggested_exercises()
    
    for sugg in suggestions:
        st.write(f"**{sugg['domain']}** (Niveau {sugg['difficulty']})")
        st.caption(sugg['reason'])
    
    # Section 6: Bouton encouragement
    st.divider()
    if st.button("💬 Envoyer un message d'encouragement", use_container_width=True):
        st.success("Message envoyé à votre enfant! 🎉")
        # TODO: Implémenter message inbox enfant
```

## Intégration dans app.py

Dans `app.py` principal, ajouter:

```python
# Après login parent
if st.session_state.user_type == "parent":
    # Sélection enfant
    children = get_children(st.session_state.parent_id)
    selected_child = st.sidebar.selectbox("Enfant", children)
    
    # Render dashboard
    from ui.parent_dashboard_ui import render_parent_dashboard
    render_parent_dashboard(selected_child['id'], selected_child['name'])
```

## Tests
`tests/test_parent_dashboard_ui.py` (100+ tests)

- UI rendering
- Metrics display
- Chart generation
- Button actions
```

---

# 🎓 AMÉLIORATION 2: ONBOARDING INTERACTIF

## Prompt Claude Code 2.1 - Onboarding Parents

**Titre:** "Créer tutoriel onboarding parents - 3 étapes"

**Texte:**

```
# TÂCHE: Onboarding Parents

Tutoriel interactif première connexion (3 étapes, <2 min).

## Fichier à créer
`ui/onboarding/parent_onboarding.py` (150 lignes)

## Structure 3 Étapes

```python
import streamlit as st

def show_parent_onboarding():
    """Affiche onboarding si première connexion"""
    
    if 'onboarding_completed' in st.session_state:
        return  # Déjà fait
    
    # Progress indicator
    step = st.session_state.get('onboarding_step', 1)
    st.progress(step / 3)
    
    if step == 1:
        show_step_1_welcome()
    elif step == 2:
        show_step_2_navigation()
    elif step == 3:
        show_step_3_monitoring()

def show_step_1_welcome():
    st.title("👋 Bienvenue sur MathCopain!")
    st.write("""
    **MathCopain aide votre enfant à progresser en mathématiques 
    de manière personnalisée et bienveillante.**
    
    ✅ Exercices adaptés à son niveau
    ✅ Feedback encourageant
    ✅ Progression visible en temps réel
    """)
    
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Suivant →", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()

def show_step_2_navigation():
    st.title("🧭 Comment ça marche?")
    
    st.subheader("1️⃣ Votre enfant se connecte")
    st.write("Avec son prénom et un code PIN simple (4 chiffres)")
    
    st.subheader("2️⃣ Il fait des exercices")
    st.write("Adaptés automatiquement à son niveau")
    
    st.subheader("3️⃣ Vous suivez sa progression")
    st.write("Graphiques, compétences, suggestions personnalisées")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Précédent"):
            st.session_state.onboarding_step = 1
            st.rerun()
    with col2:
        if st.button("Suivant →", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()

def show_step_3_monitoring():
    st.title("📊 Suivez les progrès")
    
    st.write("Vous aurez accès à:")
    st.success("✅ Temps passé et exercices complétés")
    st.success("✅ Taux de réussite et évolution")
    st.success("✅ Compétences maîtrisées")
    st.success("✅ Points forts et axes d'amélioration")
    
    st.info("💡 **Conseil:** Encouragez votre enfant régulièrement!")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Précédent"):
            st.session_state.onboarding_step = 2
            st.rerun()
    with col2:
        if st.button("Commencer! 🚀", use_container_width=True):
            st.session_state.onboarding_completed = True
            st.balloons()
            st.rerun()
```

## Intégration

Dans `app.py`, après login parent:

```python
if not st.session_state.get('onboarding_completed'):
    from ui.onboarding.parent_onboarding import show_parent_onboarding
    show_parent_onboarding()
else:
    # Normal dashboard
    render_parent_dashboard()
```

## Tests
`tests/test_onboarding.py` (50+ tests)
```

---

## Prompt Claude Code 2.2 - Onboarding Enfants

**Titre:** "Créer onboarding enfant - Mini-jeu découverte"

**Texte:**

```
# TÂCHE: Onboarding Enfant

Mini-jeu interactif découverte (5 min max).

## Fichier à créer
`ui/onboarding/child_onboarding.py` (200 lignes)

## Structure Mini-Jeu

```python
import streamlit as st
import random

def show_child_onboarding(child_name):
    """Mini-jeu découverte pour enfants"""
    
    if 'child_onboarding_completed' in st.session_state:
        return
    
    step = st.session_state.get('child_onboarding_step', 1)
    
    if step == 1:
        show_welcome(child_name)
    elif step == 2:
        show_avatar_selection()
    elif step == 3:
        show_first_exercise_guided()
    elif step == 4:
        show_badge_earned()

def show_welcome(child_name):
    st.title(f"👋 Salut {child_name}!")
    st.write("## Bienvenue dans MathCopain! 🎉")
    
    st.write("""
    Je vais t'aider à devenir un **champion des maths**! 💪
    
    Tu vas:
    - Faire des exercices rigolos
    - Gagner des badges 🏆
    - Progresser à ton rythme
    
    C'est parti?
    """)
    
    if st.button("🚀 C'est parti!", use_container_width=True):
        st.session_state.child_onboarding_step = 2
        st.rerun()

def show_avatar_selection():
    st.title("🎨 Choisis ton avatar!")
    
    avatars = ["🐶", "🐱", "🦁", "🐼", "🦊", "🐻", "🐸", "🐵"]
    
    cols = st.columns(4)
    for i, avatar in enumerate(avatars):
        with cols[i % 4]:
            if st.button(avatar, key=f"avatar_{i}"):
                st.session_state.user_avatar = avatar
                st.session_state.child_onboarding_step = 3
                st.rerun()

def show_first_exercise_guided():
    st.title("🎯 Ton premier exercice!")
    
    st.write(f"## Quel est le résultat de **5 + 3** ?")
    
    st.info("💡 Compte sur tes doigts si tu veux!")
    
    answer = st.number_input("Ta réponse:", min_value=0, max_value=20, step=1)
    
    if st.button("Valider ✅"):
        if answer == 8:
            st.success("🎉 Bravo! C'est exact!")
            st.balloons()
            if st.button("Continuer →"):
                st.session_state.child_onboarding_step = 4
                st.rerun()
        else:
            st.warning("Presque! Essaie encore 😊")

def show_badge_earned():
    st.title("🏆 Tu as gagné ton premier badge!")
    
    st.write("## 🌟 Badge 'Première Étoile'")
    st.write("Pour avoir réussi ton premier exercice!")
    
    st.success("Continue comme ça! Tu vas en gagner plein d'autres! 🚀")
    
    if st.button("Commencer l'aventure! 🎮", use_container_width=True):
        st.session_state.child_onboarding_completed = True
        award_badge(st.session_state.user_id, "first_star")
        st.rerun()
```

## Tests
`tests/test_child_onboarding.py` (80+ tests)
```

---

# 🎮 AMÉLIORATION 3: GAMIFICATION BASIQUE

## Prompt Claude Code 3.1 - Badge System

**Titre:** "Implémenter système badges simple - 10 badges MVP"

**Texte:**

```
# TÂCHE: Système Badges

Gamification basique pour engagement enfants.

## Fichier à créer
`core/gamification/badge_manager.py` (250 lignes)

## Classe BadgeManager

```python
class BadgeManager:
    """Gestion badges et achievements"""
    
    # Définition 10 badges MVP
    BADGES = {
        "first_star": {
            "name": "Première Étoile",
            "icon": "🌟",
            "description": "Premier exercice réussi",
            "condition": lambda stats: stats['total_correct'] >= 1
        },
        "perseverant": {
            "name": "Persévérant",
            "icon": "💪",
            "description": "10 exercices d'affilée",
            "condition": lambda stats: stats['current_streak'] >= 10
        },
        "speed_master": {
            "name": "Éclair",
            "icon": "⚡",
            "description": "5 exercices en moins de 1 minute chacun",
            "condition": lambda stats: stats['speed_exercises'] >= 5
        },
        "addition_master": {
            "name": "Champion Addition",
            "icon": "➕",
            "description": "20 additions réussies",
            "condition": lambda stats: stats['addition_correct'] >= 20
        },
        "multiplication_master": {
            "name": "Champion Multiplication",
            "icon": "✖️",
            "description": "20 multiplications réussies",
            "condition": lambda stats: stats['multiplication_correct'] >= 20
        },
        "explorer": {
            "name": "Explorateur",
            "icon": "🧭",
            "description": "Essayé 5 domaines différents",
            "condition": lambda stats: len(stats['domains_tried']) >= 5
        },
        "regular": {
            "name": "Régulier",
            "icon": "📅",
            "description": "Connecté 5 jours d'affilée",
            "condition": lambda stats: stats['login_streak'] >= 5
        },
        "century": {
            "name": "Centurion",
            "icon": "💯",
            "description": "100 exercices complétés",
            "condition": lambda stats: stats['total_exercises'] >= 100
        },
        "perfectionist": {
            "name": "Perfectionniste",
            "icon": "🎯",
            "description": "10 exercices parfaits d'affilée",
            "condition": lambda stats: stats['perfect_streak'] >= 10
        },
        "night_owl": {
            "name": "Chouette de nuit",
            "icon": "🦉",
            "description": "Exercice après 20h",
            "condition": lambda stats: stats['late_night_exercises'] >= 1
        }
    }
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = get_db_connection()
    
    def check_new_badges(self):
        """Vérifie si nouveaux badges débloqués"""
        stats = self._get_user_stats()
        earned_badges = []
        
        for badge_id, badge_def in self.BADGES.items():
            if badge_def['condition'](stats):
                if not self._has_badge(badge_id):
                    self._award_badge(badge_id)
                    earned_badges.append(badge_def)
        
        return earned_badges
    
    def _get_user_stats(self):
        """Calcule stats utilisateur pour conditions badges"""
        query = '''
        SELECT 
            COUNT(*) FILTER (WHERE is_correct) as total_correct,
            COUNT(*) as total_exercises,
            COUNT(DISTINCT skill_domain) as domains_count,
            MAX(consecutive_streak) as current_streak
        FROM exercise_responses
        WHERE user_id = %s
        '''
        result = self.db.execute(query, (self.user_id,))
        
        return {
            'total_correct': result['total_correct'],
            'total_exercises': result['total_exercises'],
            'domains_tried': self._get_domains_tried(),
            'current_streak': self._calculate_current_streak(),
            'addition_correct': self._count_domain_correct('addition'),
            'multiplication_correct': self._count_domain_correct('multiplication'),
            'login_streak': self._calculate_login_streak(),
            'speed_exercises': self._count_speed_exercises(),
            'perfect_streak': self._calculate_perfect_streak(),
            'late_night_exercises': self._count_late_exercises()
        }
    
    def _award_badge(self, badge_id):
        """Décerne badge à utilisateur"""
        query = '''
        INSERT INTO user_badges (user_id, badge_id, earned_at)
        VALUES (%s, %s, NOW())
        '''
        self.db.execute(query, (self.user_id, badge_id))
        
        # Log analytics event
        log_analytics_event(self.user_id, 'badge_earned', {'badge_id': badge_id})
    
    def get_earned_badges(self):
        """Liste badges gagnés par utilisateur"""
        query = '''
        SELECT badge_id, earned_at
        FROM user_badges
        WHERE user_id = %s
        ORDER BY earned_at DESC
        '''
        results = self.db.execute(query, (self.user_id,))
        
        return [
            {
                **self.BADGES[row['badge_id']],
                'earned_at': row['earned_at']
            }
            for row in results
        ]
    
    def get_progress_to_next_badges(self):
        """Badges presque débloqués (motivation)"""
        stats = self._get_user_stats()
        progress = []
        
        for badge_id, badge_def in self.BADGES.items():
            if not self._has_badge(badge_id):
                # Calculer progression
                if badge_id == 'perseverant':
                    pct = min(stats['current_streak'] / 10 * 100, 100)
                    progress.append({
                        **badge_def,
                        'progress_pct': pct,
                        'message': f"{stats['current_streak']}/10 exercices"
                    })
                # ... autres badges
        
        # Retourner 3 plus proches
        return sorted(progress, key=lambda x: x['progress_pct'], reverse=True)[:3]
```

## Database Migration

```sql
-- Ajouter table badges
CREATE TABLE user_badges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    badge_id VARCHAR(50),
    earned_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, badge_id),
    INDEX idx_user_badges (user_id)
);
```

## Tests
`tests/test_badge_manager.py` (200+ tests)

- Badge condition evaluation
- Stats calculation accuracy
- Badge awarding
- Progress calculation
```

---

## Prompt Claude Code 3.2 - Badge Display UI

**Titre:** "Créer UI affichage badges - Collection et notifications"

**Texte:**

```
# TÂCHE: UI Badges

Affichage badges collection + notifications nouveau badge.

## Fichier à créer
`ui/badges_display.py` (150 lignes)

## Fonctions UI

```python
import streamlit as st
from core.gamification.badge_manager import BadgeManager

def show_badge_notification(new_badges):
    """Affiche notification popup nouveau badge"""
    if new_badges:
        for badge in new_badges:
            st.toast(f"🏆 Badge débloqué: {badge['name']}!", icon="🎉")
            st.balloons()

def render_badge_collection():
    """Page collection badges"""
    st.title("🏆 Ma Collection de Badges")
    
    badge_mgr = BadgeManager(st.session_state.user_id)
    earned = badge_mgr.get_earned_badges()
    all_badges = badge_mgr.BADGES
    
    # Stats globales
    st.metric(
        "Badges débloqués", 
        f"{len(earned)}/{len(all_badges)}"
    )
    st.progress(len(earned) / len(all_badges))
    
    # Badges gagnés
    st.subheader("✅ Badges débloqués")
    cols = st.columns(3)
    for i, badge in enumerate(earned):
        with cols[i % 3]:
            st.write(f"## {badge['icon']}")
            st.write(f"**{badge['name']}**")
            st.caption(badge['description'])
            st.caption(f"🗓️ {badge['earned_at'].strftime('%d/%m/%Y')}")
    
    # Badges à débloquer
    st.subheader("🔒 À débloquer")
    locked = [b for b_id, b in all_badges.items() 
              if b_id not in [e['badge_id'] for e in earned]]
    
    cols = st.columns(3)
    for i, badge in enumerate(locked):
        with cols[i % 3]:
            st.write(f"## 🔒")
            st.write(f"**{badge['name']}**")
            st.caption(badge['description'])
    
    # Badges prochains (motivation)
    st.divider()
    st.subheader("🎯 Prochains badges")
    progress_badges = badge_mgr.get_progress_to_next_badges()
    
    for badge in progress_badges:
        st.write(f"{badge['icon']} **{badge['name']}**")
        st.progress(badge['progress_pct'] / 100)
        st.caption(badge['message'])

def check_and_show_new_badges():
    """Vérifie nouveaux badges après exercice"""
    badge_mgr = BadgeManager(st.session_state.user_id)
    new_badges = badge_mgr.check_new_badges()
    
    if new_badges:
        show_badge_notification(new_badges)
```

## Intégration dans app.py

```python
# Après chaque exercice complété
if exercise_completed:
    from ui.badges_display import check_and_show_new_badges
    check_and_show_new_badges()

# Menu navigation
if st.sidebar.button("🏆 Mes Badges"):
    from ui.badges_display import render_badge_collection
    render_badge_collection()
```

## Tests
`tests/test_badges_ui.py` (80+ tests)
```

---

# 🔒 AMÉLIORATION 4: RGPD & SÉCURITÉ

## Prompt Claude Code 4.1 - RGPD Compliance

**Titre:** "Implémenter conformité RGPD - Consentement + Export données"

**Texte:**

```
# TÂCHE: RGPD Compliance

Mise en conformité RGPD obligatoire.

## Fichiers à créer
`core/security/gdpr_manager.py` (300 lignes)
`ui/gdpr_consent_banner.py` (100 lignes)
`ui/data_export_page.py` (150 lignes)

## Classe GDPRManager

```python
class GDPRManager:
    """Gestion conformité RGPD"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = get_db_connection()
    
    def record_consent(self, consent_type, granted=True):
        """Enregistre consentement utilisateur"""
        query = '''
        INSERT INTO user_consents (user_id, consent_type, granted, timestamp)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (user_id, consent_type) 
        DO UPDATE SET granted = %s, timestamp = NOW()
        '''
        self.db.execute(query, (self.user_id, consent_type, granted, granted))
    
    def has_consent(self, consent_type):
        """Vérifie si consentement donné"""
        query = '''
        SELECT granted FROM user_consents
        WHERE user_id = %s AND consent_type = %s
        '''
        result = self.db.execute(query, (self.user_id, consent_type))
        return result['granted'] if result else False
    
    def export_user_data(self):
        """Export toutes données utilisateur (droit d'accès)"""
        data = {
            'user_profile': self._get_user_profile(),
            'exercise_history': self._get_exercise_history(),
            'skill_profiles': self._get_skill_profiles(),
            'badges_earned': self._get_badges(),
            'analytics_events': self._get_analytics_events()
        }
        
        # Générer JSON
        import json
        import datetime
        filename = f"mathcopain_data_{self.user_id}_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        
        with open(f"/tmp/{filename}", 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filename
    
    def delete_user_data(self):
        """Suppression complète données (droit à l'oubli)"""
        # Soft delete (garder traces anonymisées analytics)
        queries = [
            "UPDATE users SET is_deleted = TRUE, username = 'deleted', email = NULL WHERE id = %s",
            "DELETE FROM exercise_responses WHERE user_id = %s",
            "DELETE FROM user_badges WHERE user_id = %s",
            "DELETE FROM skill_profiles WHERE user_id = %s",
            "UPDATE analytics_events SET user_id = NULL WHERE user_id = %s"
        ]
        
        for query in queries:
            self.db.execute(query, (self.user_id,))
        
        log_gdpr_action(self.user_id, 'user_deleted')
```

## UI Banner Consentement

```python
# ui/gdpr_consent_banner.py
def show_consent_banner():
    """Banner cookies/consentement première visite"""
    
    if 'gdpr_consent_shown' not in st.session_state:
        with st.container():
            st.warning("""
            🍪 **Protection de vos données**
            
            MathCopain utilise des cookies essentiels et collecte des données 
            d'apprentissage pour personnaliser l'expérience de votre enfant.
            
            En continuant, vous acceptez notre [Politique de confidentialité](/privacy).
            """)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ J'accepte", use_container_width=True):
                    gdpr = GDPRManager(st.session_state.user_id)
                    gdpr.record_consent('cookies', granted=True)
                    gdpr.record_consent('analytics', granted=True)
                    st.session_state.gdpr_consent_shown = True
                    st.rerun()
            
            with col2:
                if st.button("❌ Refuser", use_container_width=True):
                    gdpr = GDPRManager(st.session_state.user_id)
                    gdpr.record_consent('cookies', granted=False)
                    st.session_state.gdpr_consent_shown = True
                    st.rerun()
```

## Page Export Données

```python
# ui/data_export_page.py
def render_data_export_page():
    """Page export/suppression données"""
    
    st.title("🔒 Mes Données")
    
    st.subheader("📥 Exporter mes données")
    st.write("Téléchargez toutes les données de votre compte.")
    
    if st.button("Exporter mes données"):
        gdpr = GDPRManager(st.session_state.user_id)
        filename = gdpr.export_user_data()
        
        with open(f"/tmp/{filename}", 'rb') as f:
            st.download_button(
                "⬇️ Télécharger",
                data=f,
                file_name=filename,
                mime='application/json'
            )
    
    st.divider()
    
    st.subheader("🗑️ Supprimer mon compte")
    st.warning("⚠️ Cette action est irréversible!")
    
    if st.checkbox("Je comprends que mes données seront supprimées"):
        if st.button("Supprimer définitivement mon compte"):
            gdpr = GDPRManager(st.session_state.user_id)
            gdpr.delete_user_data()
            st.success("Compte supprimé. Au revoir! 👋")
            st.session_state.clear()
            st.rerun()
```

## Database Migration

```sql
-- Table consentements
CREATE TABLE user_consents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    consent_type VARCHAR(50),
    granted BOOLEAN,
    timestamp TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, consent_type)
);

-- Ajouter flag deletion users
ALTER TABLE users ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
```

## Tests
`tests/test_gdpr.py` (150+ tests)
```

---

## Prompt Claude Code 4.2 - Rate Limiting & Sécurité

**Titre:** "Ajouter rate limiting et sécurité renforcée"

**Texte:**

```
# TÂCHE: Sécurité Renforcée

Rate limiting + protections anti-abus.

## Fichier à créer
`core/security/rate_limiter.py` (200 lignes)

## Classe RateLimiter

```python
from functools import wraps
import time

class RateLimiter:
    """Rate limiting pour prévenir abus"""
    
    def __init__(self):
        self.attempts = {}  # user_id -> [(timestamp, action), ...]
    
    def check_rate_limit(self, user_id, action, max_attempts=5, window_seconds=900):
        """
        Vérifie si rate limit atteint
        
        Défaut: 5 tentatives par 15 minutes
        """
        now = time.time()
        
        # Nettoyer anciennes tentatives
        if user_id in self.attempts:
            self.attempts[user_id] = [
                (ts, act) for ts, act in self.attempts[user_id]
                if now - ts < window_seconds and act == action
            ]
        else:
            self.attempts[user_id] = []
        
        # Vérifier limite
        if len(self.attempts[user_id]) >= max_attempts:
            oldest = self.attempts[user_id][0][0]
            wait_time = window_seconds - (now - oldest)
            return False, wait_time
        
        # Enregistrer tentative
        self.attempts[user_id].append((now, action))
        return True, 0
    
    def reset(self, user_id, action=None):
        """Reset rate limit pour utilisateur"""
        if action:
            self.attempts[user_id] = [
                (ts, act) for ts, act in self.attempts[user_id]
                if act != action
            ]
        else:
            self.attempts[user_id] = []

# Decorator pour protéger endpoints
def rate_limit(action, max_attempts=5, window_seconds=900):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rate_limiter = get_rate_limiter()
            user_id = st.session_state.get('user_id')
            
            allowed, wait_time = rate_limiter.check_rate_limit(
                user_id, action, max_attempts, window_seconds
            )
            
            if not allowed:
                st.error(f"⏳ Trop de tentatives. Réessayez dans {int(wait_time)}s.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Utilisation

```python
# Protéger login
@rate_limit('login', max_attempts=5, window_seconds=900)  # 5 tentatives / 15 min
def handle_login(username, pin):
    # Login logic
    pass

# Protéger création compte
@rate_limit('signup', max_attempts=3, window_seconds=3600)  # 3 / heure
def handle_signup(username, email):
    # Signup logic
    pass

# Dans app.py
if st.button("Se connecter"):
    result = handle_login(username, pin)
    if result:
        st.success("Connecté!")
```

## Protections Additionnelles

```python
# Input validation
def validate_username(username):
    """Validation username strict"""
    import re
    if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
        raise ValueError("Username invalide (3-20 caractères alphanum)")
    return username

def validate_pin(pin):
    """Validation PIN"""
    if not re.match(r'^\d{4}$', pin):
        raise ValueError("PIN doit être 4 chiffres")
    return pin

# XSS protection
def sanitize_input(text):
    """Nettoie inputs utilisateur"""
    import html
    return html.escape(text)

# Session timeout
def check_session_timeout():
    """Auto-logout après 30 min inactivité"""
    if 'last_activity' in st.session_state:
        inactive = time.time() - st.session_state.last_activity
        if inactive > 1800:  # 30 minutes
            st.session_state.clear()
            st.warning("Session expirée. Reconnectez-vous.")
            st.rerun()
    
    st.session_state.last_activity = time.time()
```

## Tests
`tests/test_security.py` (150+ tests)
```

---

# ⚡ AMÉLIORATION 5: TESTS PERFORMANCE

## Prompt Claude Code 5.1 - Load Testing

**Titre:** "Créer tests charge - Simuler 50+ utilisateurs simultanés"

**Texte:**

```
# TÂCHE: Tests Performance

Valider scalabilité 50+ users simultanés.

## Fichier à créer
`tests/performance/load_test.py` (200 lignes)

## Tests Locust

```python
from locust import HttpUser, task, between
import random

class MathCopainUser(HttpUser):
    """Simule comportement utilisateur"""
    
    wait_time = between(2, 5)  # Pause entre actions
    
    def on_start(self):
        """Setup: Login"""
        self.client.post("/login", json={
            "username": f"test_user_{random.randint(1, 100)}",
            "pin": "1234"
        })
    
    @task(3)  # Poids 3: Action fréquente
    def get_exercise(self):
        """Récupérer exercice"""
        self.client.get("/api/exercise/random")
    
    @task(2)
    def submit_answer(self):
        """Soumettre réponse"""
        self.client.post("/api/exercise/submit", json={
            "exercise_id": "add_001",
            "answer": 42,
            "time_taken": random.randint(10, 60)
        })
    
    @task(1)
    def view_progress(self):
        """Voir progression"""
        self.client.get("/api/progress")

# Lancer avec:
# locust -f tests/performance/load_test.py --host=http://localhost:8501
```

## Tests Performance DB

```python
# tests/performance/db_performance_test.py
import pytest
import time

def test_query_performance():
    """Vérifier temps réponse queries < 500ms"""
    
    from core.analytics.parent_dashboard import ParentDashboardAnalytics
    
    analytics = ParentDashboardAnalytics(user_id=1)
    
    start = time.time()
    summary = analytics.get_weekly_summary()
    duration = time.time() - start
    
    assert duration < 0.5, f"Query trop lente: {duration}s"

def test_concurrent_requests():
    """Simuler requêtes concurrentes"""
    import concurrent.futures
    
    def make_request(user_id):
        analytics = ParentDashboardAnalytics(user_id)
        return analytics.get_weekly_summary()
    
    # 50 requêtes simultanées
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_request, i) for i in range(1, 51)]
        results = [f.result() for f in futures]
    
    assert len(results) == 50
    assert all(r is not None for r in results)
```

## Optimisations DB

```python
# Ajouter indexes manquants
CREATE INDEX idx_exercises_user_created ON exercise_responses(user_id, created_at DESC);
CREATE INDEX idx_exercises_domain ON exercise_responses(skill_domain);

# Connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True  # Vérifier connexions
)
```

## Tests
`tests/performance/test_performance.py` (100+ tests)
```

---

# ♿ AMÉLIORATION 6: ACCESSIBILITÉ

## Prompt Claude Code 6.1 - Accessibilité WCAG

**Titre:** "Améliorer accessibilité - Contraste + Clavier + Taille police"

**Texte:**

```
# TÂCHE: Accessibilité

Conformité WCAG AA minimum.

## Fichier à créer
`ui/accessibility_settings.py` (150 lignes)

## Paramètres Accessibilité

```python
import streamlit as st

def show_accessibility_settings():
    """Panel paramètres accessibilité"""
    
    st.sidebar.title("♿ Accessibilité")
    
    # Taille police
    font_size = st.sidebar.selectbox(
        "Taille texte",
        ["Normal", "Grand", "Très Grand"],
        index=0
    )
    
    # Mode contraste
    contrast_mode = st.sidebar.selectbox(
        "Contraste",
        ["Normal", "Élevé"],
        index=0
    )
    
    # Sauvegarder préférences
    if font_size != st.session_state.get('font_size'):
        st.session_state.font_size = font_size
        apply_font_size(font_size)
    
    if contrast_mode != st.session_state.get('contrast_mode'):
        st.session_state.contrast_mode = contrast_mode
        apply_contrast_mode(contrast_mode)

def apply_font_size(size):
    """Appliquer taille police globale"""
    size_map = {
        "Normal": "16px",
        "Grand": "20px",
        "Très Grand": "24px"
    }
    
    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {size_map[size]} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def apply_contrast_mode(mode):
    """Appliquer mode contraste"""
    if mode == "Élevé":
        st.markdown("""
        <style>
        :root {
            --background-color: #000000;
            --text-color: #FFFFFF;
            --primary-color: #FFD700;
        }
        body {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        </style>
        """, unsafe_allow_html=True)
```

## Navigation Clavier

```python
# Ajouter shortcuts clavier
def setup_keyboard_shortcuts():
    """Raccourcis clavier accessibilité"""
    
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // Ctrl+H: Aide
        if (e.ctrlKey && e.key === 'h') {
            document.getElementById('help-button').click();
        }
        
        // Ctrl+M: Menu
        if (e.ctrlKey && e.key === 'm') {
            document.getElementById('menu-button').click();
        }
        
        // Escape: Fermer modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
    </script>
    """, unsafe_allow_html=True)
```

## Alt Text Images

```python
# S'assurer que toutes images ont alt text
st.image("diagram.png", alt="Diagramme montrant progression addition")

# Icons avec labels
st.button("✅ Valider", help="Soumettre votre réponse")
```

## Tests
`tests/test_accessibility.py` (80+ tests)

- Contraste WCAG AA validation
- Navigation clavier complète
- Alt text présence
- ARIA labels
```

---

# 📚 AMÉLIORATION 7: DOCUMENTATION UTILISATEUR

## Prompt Claude Code 7.1 - Guide Utilisateur Parent

**Titre:** "Créer guide utilisateur parent PDF - 5 pages"

**Texte:**

```
# TÂCHE: Guide Utilisateur Parent

Document PDF clair et illustré.

## Fichier à créer
`docs/guides/guide_parent.md` (Markdown → PDF)

## Structure Guide

```markdown
# Guide Utilisateur Parent - MathCopain

## 1. Introduction

Bienvenue sur MathCopain! Cette application aide votre enfant à progresser 
en mathématiques de manière personnalisée et bienveillante.

### Avantages
- ✅ Exercices adaptés automatiquement
- ✅ Feedback encourageant
- ✅ Progression visible en temps réel
- ✅ Intelligence artificielle pédagogique

---

## 2. Premiers Pas

### Créer un compte enfant

1. Cliquez sur "Créer un compte"
2. Entrez le prénom de votre enfant
3. Choisissez un PIN à 4 chiffres (facile à retenir!)
4. Sélectionnez le niveau scolaire (CE1-CM2)

💡 **Conseil:** Choisissez un PIN que votre enfant peut mémoriser facilement.

### Lier votre compte parent

1. Créez votre compte parent
2. Entrez votre email
3. Liez le compte de votre enfant
4. Vous recevrez les notifications de progression

---

## 3. Suivre la Progression

### Dashboard Parent

Vous avez accès à:

**📊 Résumé hebdomadaire**
- Temps passé
- Exercices complétés
- Taux de réussite

**🎯 Compétences travaillées**
- Liste des domaines pratiqués
- Statut de maîtrise (✅ Maîtrisé, 🔄 En cours, ⏳ À venir)

**💪 Points forts / 📈 À améliorer**
- 3 points forts identifiés
- 3 axes d'amélioration suggérés

### Graphiques

Le graphique de progression montre:
- Temps passé quotidien (en minutes)
- Taux de réussite par jour (%)

---

## 4. Accompagner Votre Enfant

### Bonnes Pratiques

✅ **Encouragez régulièrement**
- Consultez le dashboard chaque semaine
- Félicitez les progrès (même petits!)
- Utilisez le bouton "Envoyer encouragement"

✅ **Respectez son rythme**
- 15-20 minutes par jour suffisent
- Pas de pression excessive
- L'application s'adapte automatiquement

✅ **Variez les domaines**
- L'app suggère des exercices équilibrés
- Encouragez la découverte de nouveaux domaines

❌ **À éviter**
- Comparer avec d'autres enfants
- Forcer en cas de fatigue
- Punir les erreurs (elles sont normales!)

---

## 5. FAQ

**Q: Mon enfant peut-il utiliser l'app seul?**
R: Oui! L'interface est conçue pour les enfants. Votre supervision reste recommandée.

**Q: Combien de temps par jour?**
R: 15-20 minutes sont idéales. L'app détecte la fatigue et suggère des pauses.

**Q: Les exercices sont-ils alignés avec le programme scolaire?**
R: Oui, tous les exercices suivent le programme de l'Éducation Nationale.

**Q: Comment exporter les données?**
R: Menu Paramètres → "Mes données" → "Exporter mes données"

**Q: Mon enfant a oublié son PIN, que faire?**
R: Contactez le support à support@mathcopain.fr avec votre email parent.

---

## 6. Support

**📧 Email:** support@mathcopain.fr
**💬 Chat:** Disponible dans l'application (coin inférieur droit)
**🌐 Site:** www.mathcopain.fr/aide

Nous répondons sous 24h ouvrées.

---

*Guide version 1.0 - Novembre 2025*
```

## Conversion PDF

```python
# Script conversion Markdown → PDF
# scripts/generate_pdf_guide.py

import markdown
from weasyprint import HTML

def generate_pdf_guide():
    with open('docs/guides/guide_parent.md', 'r') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # CSS styling
    html_full = f'''
    <html>
    <head>
        <style>
            body {{ font-family: Arial; margin: 40px; line-height: 1.6; }}
            h1 {{ color: #2C3E50; border-bottom: 3px solid #3498DB; }}
            h2 {{ color: #34495E; margin-top: 30px; }}
            .tip {{ background: #E8F5E9; padding: 15px; border-left: 4px solid #4CAF50; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    '''
    
    HTML(string=html_full).write_pdf('docs/guides/guide_parent.pdf')

# Lancer: python scripts/generate_pdf_guide.py
```
```

---

## Prompt Claude Code 7.2 - Guide Vidéo

**Titre:** "Script vidéo tutoriel parent - 2 minutes"

**Texte:**

```
# TÂCHE: Script Vidéo Tutoriel

Script pour vidéo explicative courte (2 min).

## Fichier à créer
`docs/video_scripts/parent_tutorial_script.md`

## Script Vidéo

```markdown
# Script Vidéo: Tutoriel Parent MathCopain (2 minutes)

## SCÈNE 1: Introduction (0:00-0:15)
[VISUEL: Logo MathCopain + interface accueil]

**Narrateur:**
"Bienvenue sur MathCopain, l'application qui aide votre enfant à progresser 
en mathématiques de manière personnalisée et bienveillante."

## SCÈNE 2: Création Compte (0:15-0:35)
[VISUEL: Écran création compte]

**Narrateur:**
"Créez un compte en 3 étapes simples:
1. Le prénom de votre enfant
2. Un PIN à 4 chiffres facile à retenir
3. Son niveau scolaire

Et c'est tout! Votre enfant peut commencer immédiatement."

## SCÈNE 3: Dashboard Parent (0:35-1:10)
[VISUEL: Dashboard parent avec données exemple]

**Narrateur:**
"Vous, en tant que parent, accédez à un tableau de bord clair montrant:
- Le temps passé et les exercices complétés
- Le taux de réussite et son évolution
- Les compétences maîtrisées et celles en cours

Tout est visualisé simplement avec des graphiques et des icônes."

[VISUEL: Zoom sur section "Points forts"]

"L'application identifie automatiquement les points forts de votre enfant 
et les axes d'amélioration."

## SCÈNE 4: Intelligence Adaptative (1:10-1:40)
[VISUEL: Animation exercices qui s'adaptent]

**Narrateur:**
"MathCopain utilise l'intelligence artificielle pour adapter automatiquement 
la difficulté des exercices. Votre enfant reste dans sa zone de confort tout 
en progressant régulièrement.

Le feedback est toujours positif et encourageant, même en cas d'erreur."

[VISUEL: Exemple feedback positif]

## SCÈNE 5: Gamification (1:40-1:50)
[VISUEL: Collection badges]

**Narrateur:**
"Votre enfant gagne des badges au fur et à mesure de sa progression, 
ce qui maintient sa motivation!"

## SCÈNE 6: Conclusion (1:50-2:00)
[VISUEL: Retour logo + CTA]

**Narrateur:**
"MathCopain: des mathématiques adaptées, bienveillantes et efficaces.
Inscrivez-vous gratuitement sur mathcopain.fr"

[FIN]

---

**Notes production:**
- Ton: Chaleureux, rassurant
- Musique: Douce, optimiste
- Durée totale: 2:00 exactement
- Format: 16:9, 1080p
```

## Storyboard

```markdown
# Storyboard Vidéo

| Timecode | Visuel | Audio | Notes |
|----------|--------|-------|-------|
| 0:00 | Logo animé | Musique intro | Animation 3s |
| 0:03 | Interface accueil | Narration début | Écran propre |
| 0:15 | Form création compte | Narration étapes | Remplissage animé |
| 0:35 | Dashboard parent | Narration dashboard | Données réalistes |
| 0:50 | Zoom graphique | Narration insights | Highlight sections |
| 1:10 | Animation adaptation | Narration IA | Transition fluide |
| 1:30 | Exemple feedback | Narration positif | Emoji visible |
| 1:40 | Collection badges | Narration gamif | Badges animés |
| 1:50 | Logo + CTA | Narration conclusion | URL visible 5s |
```
```

---

# 🎯 RÉCAPITULATIF & ORDRE D'EXÉCUTION

## Timeline Recommandée (7-8 jours)

```
JOUR 1-2: Dashboard Parents
├─ Prompt 1.1: Backend (2h)
├─ Prompt 1.2: UI (3h)
└─ Tests integration (2h)

JOUR 3: Onboarding
├─ Prompt 2.1: Onboarding Parents (2h)
├─ Prompt 2.2: Onboarding Enfants (3h)
└─ Tests (1h)

JOUR 4: Gamification
├─ Prompt 3.1: Badge System (3h)
├─ Prompt 3.2: UI Badges (2h)
└─ Tests (1h)

JOUR 5: RGPD & Sécurité
├─ Prompt 4.1: RGPD Compliance (3h)
├─ Prompt 4.2: Rate Limiting (2h)
└─ Tests (2h)

JOUR 6: Performance & Accessibilité
├─ Prompt 5.1: Load Testing (2h)
├─ Prompt 6.1: Accessibilité (3h)
└─ Optimisations (2h)

JOUR 7: Documentation
├─ Prompt 7.1: Guide PDF (3h)
├─ Prompt 7.2: Script Vidéo (1h)
└─ Review finale (2h)

JOUR 8: Déploiement
├─ Tests finaux
├─ Backup
└─ Go Live! 🚀
```

## Checklist Finale Pré-Déploiement

```
Phase Technique:
☐ Dashboard parents fonctionnel
☐ Onboarding parents + enfants
☐ Système badges opérationnel
☐ RGPD conforme (banner + export + suppression)
☐ Rate limiting actif
☐ Tests charge 50+ users passés
☐ PostgreSQL optimisé + indexes
☐ Backups automatiques configurés
☐ Monitoring Sentry actif

Phase UX:
☐ Navigation intuitive testée avec 3+ enfants
☐ Feedback toujours positif
☐ Accessibilité WCAG AA validée
☐ Taille police ajustable
☐ Mode contraste élevé
☐ Navigation clavier complète

Phase Légale:
☐ Politique confidentialité rédigée
☐ Banner consentement affiché
☐ Export données fonctionnel
☐ Droit à l'oubli implémenté
☐ Consentement parental obligatoire

Phase Documentation:
☐ Guide parent PDF généré
☐ Script vidéo prêt
☐ FAQ complète (10+ questions)
☐ Support email configuré

Phase Communication:
☐ Page landing prête
☐ Email annonce rédigé
☐ Posts réseaux sociaux planifiés
☐ Plan communication post-lancement

MVP READY? ☐ OUI ☐ NON
```

---

# 📞 SUPPORT CLAUDE CODE

Si vous rencontrez des problèmes durant l'implémentation:

1. **Vérifier logs console** pour erreurs précises
2. **Tester composants isolément** avant intégration
3. **Utiliser template feedback** (section Utilisation des Prompts du CLAUDE_CODE_BRIEFING.md)
4. **Me consulter** (Perplexity) pour ajustements stratégiques

---

**Généré:** 2025-11-18  
**Version:** MVP Pre-Deployment  
**Prompts Totaux:** 14 prompts détaillés  
**Temps Estimé:** 7-8 jours  
**Objectif:** Déploiement MVP tests utilisateurs

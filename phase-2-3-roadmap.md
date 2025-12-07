# 🚀 SUITE DU PROJET : Phases 2-3 + Intégration Complète

**Date:** 7 décembre 2025, 15h  
**Status:** Phase 1 ✅ COMPLÈTE (Design System de base)  
**À faire:** Phases 2-3 + Intégration  
**Durée estimée:** 15-20h sur 2-3 semaines  

---

## 📊 OÙ VOUS EN ÊTES

### ✅ FAIT (Phase 1 - 4 commits)
```
✅ .streamlit/config.toml          → Couleurs Figma appliquées
✅ modules/ui/styles.py            → CSS personnalisé complet
✅ modules/ui/components.py        → 4 components Python
✅ modules/ui/__init__.py          → Package UI
✅ app.py modifié                  → setup_ui() appelé
✅ Tests locaux passés             → Aucun bug critique
✅ 4 commits pushés                → Historique git propre
```

**Résultat:** Interface Streamlit de base = **MAGNIFIQUE** ✨

---

### ❌ À FAIRE (Phase 2-3)

```
PHASE 2 (Semaine 1-2):
├─ Plotly graphiques interactifs
├─ Composants avancés (Input, Badge, Card)
└─ Intégration Mathos mascotte

PHASE 3 (Semaine 2-3):
├─ Remplacer UI existante progressivement
├─ Tests desktop + mobile
├─ Optimisation performance
└─ Déploiement Streamlit Cloud
```

---

## 🎯 PHASE 2 : COMPOSANTS AVANCÉS & PLOTLY (10-12h)

### 🔷 Semaine 1 (Lun-Ven) : Graphiques Interactifs

#### **JOUR 1-2 : Installer Plotly + Créer premiers graphiques (3h)**

**Tâche 1.1: Créer modules/ui/charts.py (Plotly)**

```python
# modules/ui/charts.py

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def create_progression_chart(user_data):
    """Graphique de progression par module (ligne avec points)"""
    df = pd.DataFrame(user_data.get('progression_history', []))
    
    if df.empty:
        return None
    
    fig = go.Figure()
    
    for module in df['module'].unique():
        module_data = df[df['module'] == module]
        fig.add_trace(go.Scatter(
            x=module_data['date'],
            y=module_data['score'],
            name=module,
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='%{x|%d/%m}<br>Score: %{y}%<extra></extra>'
        ))
    
    fig.update_layout(
        title="📈 Progression par Module",
        xaxis_title="Date",
        yaxis_title="Score (%)",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12),
        plot_bgcolor='rgba(250, 250, 250, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
    )
    
    return fig

def create_level_distribution(user_data):
    """Graphique radar des compétences"""
    categories = ['Calcul', 'Géométrie', 'Fractions', 'Décimaux', 'Mesures']
    values = [
        user_data.get('skills', {}).get('calcul', 0),
        user_data.get('skills', {}).get('geometrie', 0),
        user_data.get('skills', {}).get('fractions', 0),
        user_data.get('skills', {}).get('decimaux', 0),
        user_data.get('skills', {}).get('mesures', 0),
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(93, 173, 226, 0.3)',
        line_color='#5DADE2',
        name='Profil',
        marker=dict(size=8, color='#5DADE2'),
        hovertemplate='%{theta}: %{r}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='rgba(245, 245, 245, 0.3)',
        ),
        title='🎯 Profil de Compétences',
        height=400,
        font=dict(family="Arial, sans-serif", size=11),
        showlegend=False,
    )
    
    return fig

def create_activity_heatmap(user_data):
    """Heatmap d'activité"""
    df = pd.DataFrame(user_data.get('activity', []))
    
    if df.empty:
        return None
    
    pivot_table = df.pivot_table(
        values='count',
        index='day_of_week',
        columns='hour',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Blues',
        hovertemplate='%{x}h: %{z} exercices<extra></extra>'
    ))
    
    fig.update_layout(
        title='🔥 Activité par Heure',
        xaxis_title='Heure',
        yaxis_title='Jour',
        height=300,
    )
    
    return fig

# ========== EXPORT POUR STREAMLIT ==========
def display_chart(chart_type, user_data):
    """Affiche un graphique Plotly dans Streamlit"""
    charts = {
        'progression': create_progression_chart,
        'skills': create_level_distribution,
        'activity': create_activity_heatmap,
    }
    
    chart_func = charts.get(chart_type)
    if not chart_func:
        return None
    
    fig = chart_func(user_data)
    if fig:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
```

**Instructions pour Claude Code :**

```
TÂCHE: Créer le fichier modules/ui/charts.py

Crée ce fichier avec le contenu ci-dessus.

Après création:
1. Confirme que le fichier est créé
2. Dis "✅ Plotly module créé"
3. Attends l'étape suivante

Important: 
- Utilise les imports Plotly
- Pas de test encore, juste créer le fichier
- Format exact comme ci-dessus
```

**Tâche 1.2: Installer Plotly dans requirements.txt**

```
Ajouter à requirements.txt:
plotly==5.17.0

Et pousser:
git add requirements.txt
git commit -m "feat: Add Plotly dependency for interactive charts"
git push
```

---

#### **JOUR 3 : Intégrer Plotly dans le dashboard (2h)**

**Tâche 2.1: Utiliser les charts dans app.py**

Ajouter dans ta page dashboard:

```python
from modules.ui.charts import display_chart

# Dans main() ou ta section dashboard
st.subheader("📊 Vos Statistiques")

col1, col2 = st.columns(2)

with col1:
    display_chart('progression', user_data)

with col2:
    display_chart('skills', user_data)

st.markdown("---")

# Heatmap pleine largeur
display_chart('activity', user_data)
```

**Instructions pour Claude Code :**

```
TÂCHE: Modifier app.py pour utiliser les graphiques Plotly

1. Ajoute l'import en haut:
   from modules.ui.charts import display_chart

2. Dans ta section dashboard, ajoute:
   [le code ci-dessus]

3. Test en local: streamlit run app.py

4. Si OK:
   git add app.py
   git commit -m "feat: Add Plotly charts to dashboard"
   git push
```

---

#### **JOUR 4-5 : Composants avancés (Input, Badge, Card) (3h)**

**Tâche 3.1: Créer modules/ui/advanced_components.py**

```python
# modules/ui/advanced_components.py

import streamlit as st
from typing import Literal, Optional

def input_field(
    label: str,
    key: str,
    placeholder: str = "Tape ici...",
    state: Literal["default", "focus", "error", "success"] = "default",
    error_message: Optional[str] = None,
    help_text: Optional[str] = None
) -> str:
    """Input stylisé du Design Figma"""
    
    if state == "error":
        st.markdown(
            f"<p style='color: #E74C3C; font-size: 12px; font-weight: 600;'>{label}</p>",
            unsafe_allow_html=True
        )
        value = st.text_input(
            key=key,
            label_visibility="collapsed",
            placeholder=placeholder,
            help=help_text
        )
        if error_message:
            st.markdown(
                f"<p style='color: #E74C3C; font-size: 12px;'>❌ {error_message}</p>",
                unsafe_allow_html=True
            )
        return value
    
    elif state == "success":
        st.markdown(
            f"<p style='color: #2ECC71; font-size: 12px; font-weight: 600;'>{label}</p>",
            unsafe_allow_html=True
        )
        value = st.text_input(
            key=key,
            label_visibility="collapsed",
            placeholder=placeholder,
            help=help_text
        )
        if error_message:
            st.markdown(
                f"<p style='color: #2ECC71; font-size: 12px;'>✅ {error_message}</p>",
                unsafe_allow_html=True
            )
        return value
    
    else:
        return st.text_input(
            label=label,
            key=key,
            placeholder=placeholder,
            help=help_text
        )

def badge_level(level: Literal["CE1", "CE2", "CM1", "CM2"]) -> None:
    """Badge niveau scolaire (Figma)"""
    
    colors = {
        "CE1": "#F39C12",  # Orange
        "CE2": "#5DADE2",  # Bleu
        "CM1": "#9B59B6",  # Violet
        "CM2": "#E74C3C",  # Rouge
    }
    
    color = colors.get(level, "#5DADE2")
    
    html = f"""
    <div style="
        display: inline-block;
        background-color: {color};
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        animation: fadeInUp 0.6s ease-out;
    ">
        {level}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def exercise_card(
    level: Literal["CE1", "CE2", "CM1", "CM2"],
    exercise_type: str,
    operation: str,
    instructions: Optional[str] = None,
    on_validate: Optional[callable] = None,
    on_skip: Optional[callable] = None
) -> None:
    """Card d'exercice complet (Figma)"""
    
    with st.container():
        # Header avec badge
        col1, col2 = st.columns([1, 4])
        with col1:
            badge_level(level)
        with col2:
            st.markdown(
                f"<p style='font-size: 20px; font-weight: 600; margin: 0;'>{exercise_type}</p>",
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Opération (grand affichage)
        st.markdown(f"""
        <div style="
            background-color: #F0F8FF;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            color: #212121;
            margin: 20px 0;
        ">
            {operation}
        </div>
        """, unsafe_allow_html=True)
        
        if instructions:
            st.info(f"📝 {instructions}")
        
        # Input pour réponse
        answer = input_field(
            label="Votre réponse",
            key=f"exercise_{level}_{exercise_type}",
            placeholder="Tape ta réponse...",
            state="default"
        )
        
        # Boutons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Valider", key=f"validate_{level}_{exercise_type}", use_container_width=True):
                if on_validate:
                    on_validate(answer)
        
        with col2:
            if st.button("» Passer", key=f"skip_{level}_{exercise_type}", use_container_width=True):
                if on_skip:
                    on_skip()
```

**Instructions pour Claude Code :**

```
TÂCHE: Créer modules/ui/advanced_components.py

Crée ce fichier avec le contenu ci-dessus (3 fonctions).

Après:
1. Confirme création
2. Dis "✅ Advanced components créés"
3. Attends intégration
```

**Tâche 3.2: Exporter depuis __init__.py**

```python
# Ajouter à modules/ui/__init__.py

from .advanced_components import (
    input_field,
    badge_level,
    exercise_card
)

__all__ = [
    "setup_ui",
    "load_custom_css",
    "metric_card",
    "progress_bar",
    "info_box",
    "badge",
    "input_field",
    "badge_level",
    "exercise_card",
    "display_chart",
]
```

---

## 🎉 PHASE 3 : INTÉGRATION COMPLÈTE (5-8h)

### **SEMAINE 2 : Remplacer UI existante progressivement**

**Tâche 4.1: Créer page de démo des components (30 min)**

```python
# pages/99_demo_ui.py (ou dans app.py)

import streamlit as st
from modules.ui import (
    metric_card, progress_bar, info_box, badge,
    input_field, badge_level, exercise_card
)

st.title("🎨 Démo Design System Figma")

st.subheader("📊 Cartes Métriques")
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Points", "1250", "+50", "🏆")
with col2:
    metric_card("Streak", "15 jours", "Excellent!", "🔥")
with col3:
    metric_card("Niveau", "CM1", "↑ Expert", "⭐")

st.subheader("📈 Barres de Progression")
progress_bar("Calcul", 8, 10)
progress_bar("Fractions", 6, 10)
progress_bar("Géométrie", 9, 10)

st.subheader("🎓 Badges Niveaux")
col1, col2, col3, col4 = st.columns(4)
with col1:
    badge_level("CE1")
with col2:
    badge_level("CE2")
with col3:
    badge_level("CM1")
with col4:
    badge_level("CM2")

st.subheader("💬 Boîtes d'Info")
info_box("Information", type="info")
info_box("Succès !", type="success")
info_box("Attention", type="warning")
info_box("Erreur", type="error")

st.subheader("✏️ Exercice Exemple")
exercise_card(
    level="CM1",
    exercise_type="Addition",
    operation="24 + 18 = ?",
    instructions="Trouve la bonne réponse",
    on_validate=lambda x: st.success(f"Réponse: {x}"),
    on_skip=lambda: st.info("Exercice suivant...")
)
```

---

### **TÂCHE 4.2: Tests Desktop + Mobile (1h)**

```
CHECKLIST TESTS:

Desktop (Chrome/Firefox):
□ Couleurs OK (bleu teal #5DADE2)
□ Boutons arrondis et stylisés
□ Inputs avec bordure élégante
□ Cartes avec ombre et hover
□ Graphiques Plotly interactifs
□ Badges 4 couleurs OK
□ Animations fluides

Mobile (F12 - Responsive 375px):
□ Layout adapté à l'écran
□ Boutons cliquables (min 44px)
□ Texte lisible
□ Pas de débordement horizontal
□ Graphiques redimensionnés
□ Performance acceptable (<2s)

Accessibility:
□ Contraste couleurs OK (WCAG AA)
□ Liens visibles
□ Focus states visibles
□ Clavier navigation marche
```

**Instructions pour Claude Code :**

```
TÂCHE: Tester l'application en local

1. Lancer: streamlit run app.py

2. Vérifier:
   - Interface magnifique
   - Couleurs Figma appliquées
   - Pas d'erreurs console

3. Appuyer F12 (DevTools)
   - Mode responsive (375px)
   - Vérifier mobile OK

4. Si tout OK:
   git add .
   git commit -m "feat: Complete Design System implementation - Phase 2 & 3"
   git push

5. Dis: "✅ Tests réussis, app déployable"
```

---

### **TÂCHE 4.3: Déploiement Streamlit Cloud (30 min)**

```
ÉTAPES:

1. Vérifier requirements.txt à jour:
   - streamlit>=1.40.0
   - plotly>=5.17.0
   - pandas
   - numpy (version compatible)

2. Commit final:
   git add requirements.txt
   git commit -m "feat: Final requirements for deployment"
   git push

3. Sur streamlit.io:
   - New app
   - Connect GitHub repo
   - Main file: app.py
   - Deploy

4. Test en production
   - Vérifier URL publique
   - Tester tous les components
   - Partager avec testeurs !
```

---

## 📋 CHECKLIST COMPLÈTE (Phases 1-3)

### ✅ PHASE 1 : Fondation (4 commits)
- [x] .streamlit/config.toml
- [x] modules/ui/styles.py (CSS)
- [x] modules/ui/components.py (4 components)
- [x] modules/ui/__init__.py
- [x] app.py intégré

### ⏳ PHASE 2 : Composants Avancés (3-4 commits)
- [ ] modules/ui/charts.py (Plotly)
- [ ] modules/ui/advanced_components.py (Input, Badge, Card)
- [ ] requirements.txt avec Plotly
- [ ] Intégration dans app.py
- [ ] Tests visuels

### ⏳ PHASE 3 : Déploiement (2-3 commits)
- [ ] Page de démo (optionnel)
- [ ] Tests complets (Desktop + Mobile)
- [ ] Requirements.txt finalisé
- [ ] Déploiement Streamlit Cloud
- [ ] Tests en production

---

## 🎯 TIMELINE RECOMMANDÉE

```
SEMAINE 1 (Lun-Ven):
├─ Lun-Mar (4h) : Phase 2 Plotly + Charts
├─ Mer-Jeu (3h) : Advanced components (Input, Badge, Card)
└─ Ven (1h)     : Intégration dans app.py

SEMAINE 2 (Lun-Ven):
├─ Lun-Mar (2h) : Tests Desktop + Mobile
├─ Mer (1h)     : Optimisation performance
├─ Jeu (30 min) : Déploiement Streamlit Cloud
└─ Ven (30 min) : Tests en production + feedback

TOTAL: 11-13h sur 2 semaines
```

---

## 💡 CONSEILS IMPORTANTS

### ✅ DO's
1. **Commiter régulièrement** (chaque petite feature)
2. **Tester après chaque modification**
3. **Garder les tokens Figma à jour** dans le CSS
4. **Documenter tes changements**

### ❌ DON'Ts
1. Ne pas commiter code cassé
2. Ne pas négliger tests mobile
3. Ne pas oublier requirements.txt
4. Ne pas merger sans tests

---

## 📞 BESOIN D'AIDE ?

**Si Claude Code est bloqué :**
```
"Quelle est l'erreur exacte ? Montre-moi le message d'erreur complet."
```

**Si tu as des questions :**
```
"Je dois faire quoi à l'étape X ?"
```

**Si tu veux de l'aide :**
```
"Aide-moi à déboguer [problème]"
```

---

## 🚀 GO !

**Prochaine étape : Donner cette liste à Claude Code**

```
"Voici la Phase 2 et Phase 3 du projet.
Commençons par créer modules/ui/charts.py avec Plotly.
Voici les instructions..."
```

**Et laisse Claude Code faire ! 💪**

---

**Status:** ✅ Phase 1 complète → ⏳ Prêt pour Phase 2  
**Commits:** 4 → 7-10 après Phase 2-3  
**Durée totale:** ~50-60h (réparties 4 semaines)  
**Résultat final:** App MathCopain magnifique 🎉

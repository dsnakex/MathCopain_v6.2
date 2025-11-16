"""
Interface Quiz de Style d'Apprentissage - Phase 6.3.3
Quiz interactif pour identifier le style d'apprentissage dominant

Basé sur Gardner (1983), Fleming & Mills (1992), Kolb (1984)
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from core.pedagogy.learning_style import LearningStyleAnalyzer, LearningStyleProfile


def render_learning_style_quiz(user_id: str) -> Optional[LearningStyleProfile]:
    """
    Affiche le quiz de style d'apprentissage et retourne le profil

    Args:
        user_id: Identifiant de l'utilisateur

    Returns:
        LearningStyleProfile si complété, None sinon
    """
    st.markdown("# 🎨 Découvre ton Style d'Apprentissage !")

    st.markdown("""
    ### Pourquoi ce quiz ?
    Chaque personne apprend différemment ! Ce quiz va nous aider à comprendre
    **comment tu apprends le mieux** pour t'offrir des exercices adaptés à ton style.

    📝 **7 questions rapides** (2-3 minutes)

    🎯 **Il n'y a pas de bonnes ou mauvaises réponses !** Choisis simplement ce qui te ressemble le plus.
    """)

    # Créer l'analyzer
    analyzer = LearningStyleAnalyzer(user_id)

    # Obtenir les questions
    questions = analyzer.get_quiz_questions(count=7)

    # Vérifier si le quiz a déjà été complété
    if analyzer.profile is not None and analyzer.profile.quiz_result is not None:
        if not st.session_state.get('force_retake_quiz', False):
            st.success("✅ Tu as déjà complété le quiz !")
            display_results(analyzer.profile)

            if st.button("🔄 Refaire le quiz"):
                st.session_state.force_retake_quiz = True
                st.rerun()

            return analyzer.profile

    st.markdown("---")

    # Initialiser les réponses dans session_state
    if 'quiz_responses' not in st.session_state:
        st.session_state.quiz_responses = {}

    # Afficher les questions
    st.markdown("### 📋 Questions")

    all_answered = True
    responses_list = []

    for i, q in enumerate(questions):
        st.markdown(f"#### Question {i+1}/{len(questions)}")
        st.markdown(f"**{q['question']}**")

        # Créer les options avec icônes
        options_display = []
        options_values = []

        for style, option_text in q['options'].items():
            icon = analyzer.STYLE_DESCRIPTIONS[style]['icon']
            options_display.append(f"{icon} {option_text}")
            options_values.append(style)

        # Radio button pour la question
        key = f"q_{q['id']}"
        selected_index = st.radio(
            f"Choisis ta réponse:",
            range(len(options_display)),
            format_func=lambda x: options_display[x],
            key=key,
            index=None  # Pas de sélection par défaut
        )

        if selected_index is not None:
            st.session_state.quiz_responses[q['id']] = {
                "question_id": q['id'],
                "selected_style": options_values[selected_index]
            }
        else:
            all_answered = False

        st.markdown("---")

    # Bouton de soumission
    if all_answered:
        st.success("✅ Toutes les questions sont répondues !")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Découvrir mon style d'apprentissage", use_container_width=True, type="primary"):
                # Convertir les réponses au format attendu
                responses_list = list(st.session_state.quiz_responses.values())

                # Analyser les réponses
                result = analyzer.assess_from_quiz(responses_list)

                # Sauvegarder le profil (la méthode crée le profil automatiquement)
                analyzer.save_profile(result)

                # Afficher les résultats
                st.session_state.quiz_completed = True
                st.session_state.force_retake_quiz = False
                st.rerun()
    else:
        st.info("📝 Réponds à toutes les questions pour découvrir ton style d'apprentissage !")

    # Afficher les résultats si le quiz vient d'être complété
    if st.session_state.get('quiz_completed', False):
        st.balloons()
        st.success("🎉 Quiz complété avec succès !")

        # Recharger le profil
        analyzer.load()
        if analyzer.profile:
            display_results(analyzer.profile)

            # Réinitialiser
            st.session_state.quiz_completed = False
            st.session_state.quiz_responses = {}

            return analyzer.profile

    return None


def display_results(profile: LearningStyleProfile):
    """
    Affiche les résultats du quiz de style d'apprentissage

    Args:
        profile: Profil de l'utilisateur
    """
    st.markdown("---")
    st.markdown("## 🎯 Ton Style d'Apprentissage")

    # Style principal
    primary_style = profile.primary['style']
    primary_confidence = profile.primary['confidence']

    analyzer = LearningStyleAnalyzer(profile.user_id)
    primary_info = analyzer.STYLE_DESCRIPTIONS[primary_style]

    # Affichage avec couleurs
    st.markdown(f"""
    ### {primary_info['icon']} Style Principal: **{primary_info['name']}**

    **Confiance:** {primary_confidence:.0%}

    **Description:** {primary_info['description']}

    **Tes caractéristiques:**
    """)

    for char in primary_info['characteristics']:
        st.markdown(f"- ✓ {char}")

    # Style secondaire si présent
    if profile.secondary and profile.secondary['confidence'] > 0.3:
        st.markdown("---")
        secondary_style = profile.secondary['style']
        secondary_confidence = profile.secondary['confidence']
        secondary_info = analyzer.STYLE_DESCRIPTIONS[secondary_style]

        st.markdown(f"""
        ### {secondary_info['icon']} Style Secondaire: **{secondary_info['name']}**

        **Confiance:** {secondary_confidence:.0%}

        Tu as aussi des préférences pour le style {secondary_info['name'].lower()}.
        """)

    # Recommandations
    st.markdown("---")
    st.markdown("### 💡 Recommandations pour Toi")

    recommendations = get_recommendations(primary_style)
    for rec in recommendations:
        st.markdown(f"- {rec}")

    # Graphique des scores
    if profile.quiz_result and 'scores' in profile.quiz_result:
        st.markdown("---")
        st.markdown("### 📊 Tes Scores par Style")

        scores = profile.quiz_result['scores']

        # Créer un bar chart simple
        import pandas as pd

        df = pd.DataFrame({
            'Style': [analyzer.STYLE_DESCRIPTIONS[s]['name'] for s in scores.keys()],
            'Score': [v * 100 for v in scores.values()],
            'Icon': [analyzer.STYLE_DESCRIPTIONS[s]['icon'] for s in scores.keys()]
        })

        # Afficher avec des barres de progression
        for _, row in df.iterrows():
            st.markdown(f"**{row['Icon']} {row['Style']}**")
            st.progress(row['Score'] / 100)
            st.caption(f"{row['Score']:.0f}%")


def get_recommendations(style: str) -> List[str]:
    """
    Génère des recommandations personnalisées selon le style

    Args:
        style: Le style d'apprentissage

    Returns:
        Liste de recommandations
    """
    recommendations = {
        "visual": [
            "📊 Utilise des schémas et des dessins pour résoudre les problèmes",
            "🎨 Les exercices avec des couleurs et images t'aideront le plus",
            "📐 Dessine une droite numérique ou un diagramme quand tu es bloqué",
            "✨ Visualise le problème dans ta tête avant de le résoudre"
        ],
        "auditory": [
            "🗣️ Explique le problème à voix haute, même à toi-même",
            "🎵 Répète les étapes comme une chanson ou une comptine",
            "👂 Écoute bien les explications et n'hésite pas à demander",
            "💬 Parle de ce que tu fais pendant que tu résous l'exercice"
        ],
        "kinesthetic": [
            "✋ Utilise tes doigts, des objets ou des jetons pour compter",
            "🎮 Les exercices interactifs sont parfaits pour toi",
            "🏃 Prends des petites pauses pour bouger entre les exercices",
            "🧮 Manipule des objets physiques pour mieux comprendre"
        ],
        "logical": [
            "🧠 Cherche les patterns et les règles mathématiques",
            "🔍 Pose-toi la question 'Pourquoi ça marche comme ça ?'",
            "📚 Les explications logiques étape par étape t'aident le plus",
            "🎯 Comprends la formule avant de l'appliquer"
        ],
        "narrative": [
            "📖 Les problèmes avec des histoires sont faits pour toi",
            "🌍 Imagine des situations réelles pour chaque exercice",
            "👥 Pense aux personnages et aux contextes",
            "💭 Crée une petite histoire autour du problème"
        ]
    }

    return recommendations.get(style, [])


def check_needs_quiz(user_id: str) -> bool:
    """
    Vérifie si l'utilisateur a besoin de faire le quiz

    Args:
        user_id: Identifiant de l'utilisateur

    Returns:
        True si le quiz n'a pas encore été fait
    """
    analyzer = LearningStyleAnalyzer(user_id)
    return analyzer.profile is None or analyzer.profile.quiz_result is None


def get_user_learning_style(user_id: str) -> Optional[str]:
    """
    Récupère le style d'apprentissage principal de l'utilisateur

    Args:
        user_id: Identifiant de l'utilisateur

    Returns:
        Le style principal ou None si pas de profil
    """
    analyzer = LearningStyleAnalyzer(user_id)
    if analyzer.profile and analyzer.profile.primary:
        return analyzer.profile.primary.get('style')
    return None


def render_style_badge(user_id: str):
    """
    Affiche un badge avec le style d'apprentissage de l'utilisateur

    Args:
        user_id: Identifiant de l'utilisateur
    """
    style = get_user_learning_style(user_id)

    if style:
        analyzer = LearningStyleAnalyzer(user_id)
        style_info = analyzer.STYLE_DESCRIPTIONS[style]

        st.sidebar.markdown(f"""
        ### {style_info['icon']} Ton Style
        **{style_info['name']}**
        """)

        with st.sidebar.expander("ℹ️ À propos"):
            st.markdown(f"{style_info['description']}")

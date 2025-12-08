"""
ML Adaptive Section - Interface Streamlit pour les fonctionnalités ML Phase 7

Intègre :
- DifficultyOptimizer : Ajustement automatique de la difficulté
- PerformancePredictor : Prédictions de performance
- ExplainableAI : Explications des recommandations
- CurriculumMapper : Suivi des compétences EN
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Import des modules ML Phase 7
from core.ml import DifficultyOptimizer, PerformancePredictor, ExplainableAI
from core.classroom import CurriculumMapper, AnalyticsEngine


def init_ml_models():
    """Initialize ML models (cached in session state)"""
    if 'ml_difficulty_optimizer' not in st.session_state:
        st.session_state.ml_difficulty_optimizer = DifficultyOptimizer()

    if 'ml_performance_predictor' not in st.session_state:
        st.session_state.ml_performance_predictor = PerformancePredictor()

    if 'ml_explainable_ai' not in st.session_state:
        st.session_state.ml_explainable_ai = ExplainableAI()

    if 'ml_curriculum_mapper' not in st.session_state:
        st.session_state.ml_curriculum_mapper = CurriculumMapper()

    if 'ml_analytics' not in st.session_state:
        st.session_state.ml_analytics = AnalyticsEngine()


def get_user_id():
    """Get current user ID from session"""
    username = st.session_state.get('utilisateur', 'guest')

    # Query database to get user_id from username
    from database.connection import DatabaseSession
    from database.models import User

    try:
        with DatabaseSession() as session:
            user = session.query(User).filter(User.username == username).first()
            if user:
                return user.id
            else:
                # User not found in database, return None
                st.warning(f"Utilisateur '{username}' non trouvé dans la base de données.")
                return None
    except Exception as e:
        # In case of database error, log and return None
        st.error(f"Erreur de connexion à la base de données : {str(e)}")
        return None


def ml_adaptive_section():
    """
    Section principale pour les fonctionnalités ML adaptatives
    """
    st.title("🤖 Intelligence Artificielle Adaptative")
    st.markdown("""
    Cette section utilise l'**intelligence artificielle** pour personnaliser ton apprentissage !
    Le système analyse tes performances et adapte automatiquement les exercices.
    """)

    st.markdown("---")

    # Vérifier la connexion DB avant de continuer
    user_id = get_user_id()
    if user_id is None:
        st.warning("⚠️ **Fonctionnalité non disponible**")
        st.info("""
        La section Intelligence IA nécessite une base de données PostgreSQL ou Supabase.

        **Pour activer cette fonctionnalité :**
        1. Configurez Supabase dans le fichier `.env`
        2. Ou installez PostgreSQL localement

        **En attendant**, vous pouvez utiliser les autres sections de MathCopain ! 🎓
        """)
        return

    init_ml_models()

    # Tabs pour différentes fonctionnalités ML
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Exercice Adaptatif",
        "📊 Mes Performances",
        "📚 Compétences EN",
        "🔮 Prédictions"
    ])

    with tab1:
        exercice_adaptatif_tab()

    with tab2:
        performances_tab()

    with tab3:
        competences_tab()

    with tab4:
        predictions_tab()


def exercice_adaptatif_tab():
    """Tab for adaptive exercises"""
    st.header("🎯 Exercice avec Difficulté Automatique")

    st.info("""
    **Comment ça marche ?**

    1. 🧠 L'IA analyse tes résultats passés
    2. 🎯 Elle prédit la meilleure difficulté pour toi
    3. 📈 Elle maintient ton taux de réussite autour de 70% (Flow Theory)
    4. 🚀 Tu progresses plus vite !
    """)

    # Sélection du domaine
    domaine = st.selectbox(
        "Choisis un domaine :",
        ["addition", "soustraction", "multiplication", "division", "fractions"]
    )

    if st.button("🚀 Lancer un exercice adaptatif", type="primary"):
        try:
            user_id = get_user_id()
            optimizer = st.session_state.ml_difficulty_optimizer

            # Prédire la difficulté optimale
            difficulty, explanation = optimizer.predict(user_id, domaine)

            # Afficher l'explication
            st.success(f"✅ Difficulté recommandée : **D{difficulty}**")

            with st.expander("🧠 Pourquoi cette difficulté ?"):
                st.write("**Analyse de l'IA :**")
                st.write(f"- Taux de réussite récent : {explanation.get('recent_success_rate', 0):.1%}")
                st.write(f"- Tendance : {explanation.get('trend', 'stable')}")
                st.write(f"- Niveau de maîtrise : {explanation.get('proficiency', 0):.1%}")

                if explanation.get('flow_adjustment'):
                    st.info(f"⚖️ Ajustement Flow Theory : {explanation['flow_adjustment']}")

            # Générer un exercice avec cette difficulté
            st.session_state.ml_current_difficulty = difficulty
            st.session_state.ml_current_domain = domaine

            # TODO: Intégrer avec le générateur d'exercices existant
            # Pour l'instant, afficher un placeholder
            st.markdown("---")
            st.subheader(f"Exercice de {domaine} - Niveau {difficulty}")
            st.write("*[Ici sera intégré le générateur d'exercices avec la difficulté adaptée]*")

        except Exception as e:
            st.error(f"Erreur : {str(e)}")
            st.info("💡 Tu dois d'abord faire quelques exercices pour que l'IA puisse t'analyser !")


def performances_tab():
    """Tab for performance analytics"""
    st.header("📊 Analyse de Tes Performances")

    user_id = get_user_id()
    analytics = st.session_state.ml_analytics

    # Sélection domaine
    domaine = st.selectbox(
        "Analyser le domaine :",
        ["addition", "soustraction", "multiplication", "division", "fractions"],
        key="perf_domain"
    )

    # Période
    periode = st.slider("Période d'analyse (jours)", 7, 90, 30)

    try:
        # Trajectoire de progression
        st.subheader("📈 Ta Progression")
        trajectory = analytics.get_student_progress_trajectory(
            student_id=user_id,
            skill_domain=domaine,
            days_back=periode,
            granularity='daily'
        )

        if trajectory and trajectory.get('data_points'):
            # Créer DataFrame pour affichage
            df = pd.DataFrame(trajectory['data_points'])
            df['date'] = pd.to_datetime(df['date'])

            # Afficher le graphique
            st.line_chart(df.set_index('date')['success_rate'])

            # Statistiques
            col1, col2, col3 = st.columns(3)

            trend_emoji = "📈" if trajectory['trend_direction'] == 'improving' else "📉" if trajectory['trend_direction'] == 'declining' else "➡️"

            col1.metric("Tendance", trajectory['trend_direction'], trend_emoji)
            col2.metric("Exercices", sum(p['exercises_completed'] for p in trajectory['data_points']))
            col3.metric("Taux moyen", f"{sum(p['success_rate'] for p in trajectory['data_points']) / len(trajectory['data_points']):.1%}")

        else:
            st.info("Pas encore de données. Fais quelques exercices pour voir ta progression !")

        # Heatmap
        st.markdown("---")
        st.subheader("🔥 Heatmap de Performance")
        st.caption("Tes performances par domaine et difficulté")

        heatmap = analytics.generate_performance_heatmap(
            student_id=user_id,
            days_back=periode
        )

        if heatmap and heatmap.get('heatmap'):
            for domain_row in heatmap['heatmap']:
                st.write(f"**{domain_row['domain'].capitalize()}**")

                cols = st.columns(5)
                for i, diff_data in enumerate(domain_row['difficulties']):
                    if diff_data['success_rate'] is not None:
                        color = "🟢" if diff_data['status'] == 'excellent' else "🟡" if diff_data['status'] == 'good' else "🔴"
                        cols[i].metric(
                            f"D{diff_data['difficulty']}",
                            f"{diff_data['success_rate']:.0%}",
                            f"{color}"
                        )
                    else:
                        cols[i].metric(f"D{diff_data['difficulty']}", "—")

        # Engagement
        st.markdown("---")
        st.subheader("⚡ Ton Engagement")

        engagement = analytics.get_student_engagement_metrics(
            student_id=user_id,
            days_back=periode
        )

        if engagement and 'engagement_score' in engagement:
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Score d'engagement", f"{engagement['engagement_score']:.0f}/100")
            col2.metric("Jours actifs", engagement['active_days'])
            col3.metric("Série actuelle", f"{engagement['current_streak']} 🔥")
            col4.metric("Total exercices", engagement['total_exercises'])

            # Niveau d'engagement
            level = engagement['engagement_level']
            if level == 'excellent':
                st.success("🌟 Excellent engagement ! Continue comme ça !")
            elif level == 'good':
                st.info("👍 Bon engagement ! Quelques sessions de plus et tu seras au top !")
            elif level == 'moderate':
                st.warning("💪 Engagement moyen. Essaie de t'entraîner plus régulièrement !")
            else:
                st.error("⚠️ Faible engagement. N'hésite pas à revenir plus souvent !")

    except Exception as e:
        st.error(f"Erreur lors du chargement des performances : {str(e)}")
        st.info("💡 Fais quelques exercices pour générer des statistiques !")


def competences_tab():
    """Tab for curriculum competencies tracking"""
    st.header("📚 Mes Compétences Éducation Nationale")

    user_id = get_user_id()
    grade_level = st.session_state.get('niveau', 'CE2')
    mapper = st.session_state.ml_curriculum_mapper

    st.info(f"""
    **Suivi des compétences officielles du programme {grade_level}**

    L'IA suit ta progression sur les **compétences officielles** de l'Éducation Nationale.
    """)

    try:
        # Rapport de compétences
        report = mapper.get_student_competency_report(
            student_id=user_id,
            grade_level=grade_level
        )

        if report:
            # Résumé
            st.subheader("📊 Résumé")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", report['summary']['total_competencies'])
            col2.metric("Maîtrisées", f"{report['summary']['mastered']} 🟢")
            col3.metric("En cours", f"{report['summary']['in_progress']} 🟡")
            col4.metric("À démarrer", f"{report['summary']['not_started']} ⚪")

            # Progress bar
            completion = report['summary']['completion_rate']
            st.progress(completion)
            st.caption(f"Progression globale : {completion:.1%}")

            # Détail par compétence
            st.markdown("---")
            st.subheader("📋 Détail des Compétences")

            # Filtres
            filter_status = st.selectbox(
                "Filtrer par statut :",
                ["Toutes", "Maîtrisées", "En cours", "À démarrer"]
            )

            filtered_comps = report['competencies']
            if filter_status == "Maîtrisées":
                filtered_comps = [c for c in filtered_comps if c['status'] == 'mastered']
            elif filter_status == "En cours":
                filtered_comps = [c for c in filtered_comps if c['status'] == 'in_progress']
            elif filter_status == "À démarrer":
                filtered_comps = [c for c in filtered_comps if c['status'] == 'not_started']

            # Afficher les compétences
            for comp in filtered_comps:
                with st.expander(f"{'🟢' if comp['status'] == 'mastered' else '🟡' if comp['status'] == 'in_progress' else '⚪'} {comp['code']} - {comp['title']}"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Domaine :** {comp['domain']}")
                        st.progress(comp['mastery_level'])
                        st.caption(f"Maîtrise : {comp['mastery_level']:.0%}")

                    with col2:
                        st.metric("Exercices", comp['exercises_completed'])
                        st.metric("Réussite", f"{comp['success_rate']:.0%}")

            # Recommandations
            st.markdown("---")
            st.subheader("💡 Recommandations de l'IA")

            recommendations = mapper.recommend_next_competencies(
                student_id=user_id,
                grade_level=grade_level,
                count=3
            )

            if recommendations:
                st.info("**Voici ce que l'IA te recommande de travailler en priorité :**")

                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. **{rec['title']}** ({rec['code']})")
                    st.write(f"   → {rec['recommendation']}")
                    st.progress(rec['mastery_level'], text=f"Maîtrise actuelle : {rec['mastery_level']:.0%}")
                    st.markdown("")

        else:
            st.warning("Aucune donnée de compétences disponible.")

    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        st.info("💡 Commence par faire quelques exercices !")


def predictions_tab():
    """Tab for ML predictions and forecasts"""
    st.header("🔮 Prédictions de l'IA")

    user_id = get_user_id()
    predictor = st.session_state.ml_performance_predictor
    analytics = st.session_state.ml_analytics

    st.info("""
    **L'IA prédit tes futures performances !**

    Grâce au Machine Learning, le système peut prédire comment tu vas performer
    dans les prochains jours et t'alerter si tu es à risque d'échec.
    """)

    # Sélection domaine
    domaine = st.selectbox(
        "Domaine à analyser :",
        ["addition", "soustraction", "multiplication", "division", "fractions"],
        key="pred_domain"
    )

    try:
        # Prévisions
        st.subheader("📈 Prévisions 7 jours")

        forecast = analytics.forecast_student_performance(
            student_id=user_id,
            skill_domain=domaine,
            days_ahead=7
        )

        if forecast and 'forecast' in forecast:
            # Statut actuel
            current_prob = forecast['current_success_probability']
            risk_level = forecast['risk_level']

            # Carte de risque
            if risk_level == 'high':
                st.error(f"⚠️ **ATTENTION** : Risque élevé d'échec en {domaine}")
                st.write(forecast['recommendation'])
            elif risk_level == 'medium':
                st.warning(f"⚡ Attention modérée en {domaine}")
                st.write(forecast['recommendation'])
            else:
                st.success(f"✅ Bonne progression en {domaine}")
                st.write(forecast['recommendation'])

            # Métriques actuelles
            col1, col2, col3 = st.columns(3)
            col1.metric("Probabilité de réussite actuelle", f"{current_prob:.0%}")
            col2.metric("Confiance de l'IA", f"{forecast['current_confidence']:.0%}")
            col3.metric("Tendance", forecast['trend'])

            # Graphique de prévision
            st.markdown("---")
            st.subheader("📊 Évolution Prévue")

            df_forecast = pd.DataFrame(forecast['forecast'])
            df_forecast['date'] = pd.to_datetime(df_forecast['date'])

            st.line_chart(df_forecast.set_index('date')['projected_success_rate'])
            st.caption("Prédiction de ton taux de réussite pour les 7 prochains jours")

        # Identification des faiblesses
        st.markdown("---")
        st.subheader("🎯 Points à Améliorer")

        grade_level = st.session_state.get('niveau', 'CE2')
        mapper = st.session_state.ml_curriculum_mapper

        gaps = mapper.identify_competency_gaps(
            student_id=user_id,
            grade_level=grade_level
        )

        if gaps:
            st.write("**L'IA a identifié ces lacunes prioritaires :**")

            for gap in gaps[:5]:  # Top 5
                priority_color = "🔴" if gap['priority_score'] >= 8 else "🟡" if gap['priority_score'] >= 5 else "🟠"

                with st.expander(f"{priority_color} {gap['title']} - Priorité: {gap['priority_score']:.0f}/10"):
                    st.write(f"**Raison :** {gap['reason']}")
                    st.write(f"**Domaine :** {gap['domain']}")
                    st.write(f"**Niveau de maîtrise :** {gap['mastery_level']:.0%}")
                    st.write(f"**Difficulté recommandée :** D{gap['recommended_difficulty']}")

        else:
            st.success("🌟 Aucune lacune significative détectée ! Excellent travail !")

    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        st.info("💡 L'IA a besoin de plus de données. Fais quelques exercices d'abord !")


def get_ml_recommended_exercise():
    """
    Fonction helper pour obtenir un exercice recommandé par l'IA
    Peut être appelée depuis d'autres sections de l'app

    Returns:
        dict: {
            'domain': str,
            'difficulty': int,
            'explanation': dict
        }
    """
    init_ml_models()

    user_id = get_user_id()
    optimizer = st.session_state.ml_difficulty_optimizer

    # Déterminer le meilleur domaine à travailler
    grade_level = st.session_state.get('niveau', 'CE2')
    mapper = st.session_state.ml_curriculum_mapper

    try:
        # Obtenir les recommandations
        recommendations = mapper.recommend_next_competencies(
            student_id=user_id,
            grade_level=grade_level,
            count=1
        )

        if recommendations:
            # Prendre la première recommandation
            rec = recommendations[0]
            domain = rec['domain']

            # Obtenir la difficulté optimale pour ce domaine
            difficulty, explanation = optimizer.predict(user_id, domain)

            return {
                'domain': domain,
                'difficulty': difficulty,
                'explanation': explanation,
                'competency': rec
            }
        else:
            # Fallback : domaine aléatoire
            import random
            domain = random.choice(['addition', 'soustraction', 'multiplication'])
            difficulty, explanation = optimizer.predict(user_id, domain)

            return {
                'domain': domain,
                'difficulty': difficulty,
                'explanation': explanation
            }

    except:
        # En cas d'erreur, retourner des valeurs par défaut
        return {
            'domain': 'addition',
            'difficulty': 2,
            'explanation': {'message': 'Recommandation par défaut'}
        }

# Extract lines 1-139 (imports and essential helpers)
import streamlit as st
import random
from datetime import date, datetime
from __version__ import __version__, __title__
from authentification import init_fichier_securise
from ui_authentification import verifier_authentification
from utilisateur import charger_utilisateur, sauvegarder_utilisateur, obtenir_tous_eleves, profil_par_defaut  # ← AJOUTER
from fractions_utils import pizza_interactive, afficher_fraction_droite, dessiner_pizza  # ← VÉRIFIER
from division_utils import generer_division_simple, generer_division_reste  # ← AJOUTER

# ✅ REFACTORED Phase 2: Import from core package
from core import AdaptiveSystem, SkillTracker, SessionManager, DataManager, exercise_generator

from monnaie_utils import (  # ← NOUVEAU MODULE
    generer_calcul_rendu,
    generer_composition_monnaie,
    generer_probleme_realiste,
    dessiner_pieces_monnaie,
    expliquer_calcul_rendu,
    centimes_vers_euros_texte
)
# Modules refactorisés Phase 3
# ✅ Deprecated: Now using core.exercise_generator
# from modules.exercices import generer_addition, generer_soustraction, generer_tables, generer_division
from modules.ui.styles import local_css

# =============== SESSION INIT ===============
def init_session_state():
    cles = {
        'niveau': "CE1",
        'points': 0,
        'badges': [],
        'stats_par_niveau': {
            'CE1': {'correct': 0, 'total': 0},
            'CE2': {'correct': 0, 'total': 0},
            'CM1': {'correct': 0, 'total': 0},
            'CM2': {'correct': 0, 'total': 0}
        },
        'streak': {'current': 0, 'max': 0},
        'scores_history': [],
        'daily_challenge': {'today_date': str(date.today()), 'completed': False, 'challenge': None, 'progress': 0},
        'exercice_courant': None,
        'show_feedback': False,
        'feedback_correct': False,
        'feedback_reponse': None,
        'dernier_exercice': None,
        'jeu_type': None,
        'jeu_memory': None,
        'memory_first_flip': None,
        'memory_second_flip': None,
        'memory_incorrect_pair': None,
        'active_category': "Exercice"
    }
    for k, v in cles.items():
        if k not in st.session_state:
            st.session_state[k] = v

# =============== PROFIL: Auto-save ===============
def calculer_progression(stats_par_niveau):
    progression = {}
    for niveau in ['CE1', 'CE2', 'CM1', 'CM2']:
        total = stats_par_niveau[niveau]['total']
        correct = stats_par_niveau[niveau]['correct']
        pourcentage = (correct / total * 100) if total > 0 else 0
        progression[niveau] = min(int(pourcentage), 100)
    return progression

def auto_save_profil(succes):
    if "utilisateur" not in st.session_state or "profil" not in st.session_state:
        return
    nom = st.session_state["utilisateur"]
    profil = st.session_state["profil"]
    profil["niveau"] = st.session_state.niveau
    profil["points"] = st.session_state.points
    profil["badges"] = st.session_state.badges
    profil["exercices_reussis"] = profil.get("exercices_reussis", 0)
    profil["exercices_totaux"] = profil.get("exercices_totaux", 0)
    if succes:
        profil["exercices_reussis"] += 1
    profil["exercices_totaux"] += 1
    profil["taux_reussite"] = int(100 * profil["exercices_reussis"] / profil["exercices_totaux"]) if profil["exercices_totaux"] > 0 else 0
    profil["date_derniere_session"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
    if "stats_par_niveau" in st.session_state:
        progression = calculer_progression(st.session_state.stats_par_niveau)
        profil["progression"] = progression
    sauvegarder_utilisateur(nom, profil)
    st.session_state["profil"] = profil

# =============== EXERCICES GENERATEURS ===============
# ✅ REFACTORED Phase 2: Moved to core/exercise_generator.py
# All exercise generation functions are now in core.exercise_generator module:
# - generer_addition, generer_soustraction, generer_tables, generer_division
# - generer_probleme, generer_droite_numerique, generer_memory_emoji
# - generer_explication, generer_daily_challenge
# - calculer_score_droite

# =============== BADGES, STREAK, LEADERBOARD, DÉFI JOUR ===============
def maj_streak(correct):
    if correct:
        st.session_state.streak['current'] += 1
        st.session_state.streak['max'] = max(st.session_state.streak['current'], st.session_state.streak['max'])
    else:
        st.session_state.streak['current'] = 0

@st.cache_data
def calculer_bonus_streak(streak):
    """Calcule bonus selon streak (CACHÉ)"""
    if streak >= 10:
        return 25
    elif streak >= 5:
        return 10
    elif streak >= 3:
        return 5
    return 0

def afficher_leaderboard():
    if not st.session_state.scores_history:
        st.info("Pas de scores encore. Lance-toi !")
        return
    st.markdown('<div class="leaderboard-box">', unsafe_allow_html=True)
    st.write("### 🏆 MES TOP SCORES")
    top_scores = sorted(st.session_state.scores_history, key=lambda x: x['points'], reverse=True)[:5]
    for idx, score in enumerate(top_scores, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        st.write(f"{medal} **{score['points']} pts** - {score['type']}")
    st.markdown('</div>', unsafe_allow_html=True)

def verifier_badges(points, badges_actuels):
    badges_disponibles = {
        'premier_pas': {'seuil': 1, 'nom': '🌟 Premier Pas'},
        'persistant': {'seuil': 10, 'nom': '💪 Persévérant'},
        'champion': {'seuil': 50, 'nom': '🏆 Champion'},
        'expert': {'seuil': 100, 'nom': '👑 Expert'}
    }
    nouveaux_badges = []
    for key, badge in badges_disponibles.items():
        if points >= badge['seuil'] and badge['nom'] not in badges_actuels:
            nouveaux_badges.append(badge['nom'])
    return nouveaux_badges


# ✅ REFACTORED Phase 2: Import UI sections
from ui.exercise_sections import (
    exercice_rapide_section,
    jeu_section,
    defi_section
)
from ui.math_sections import (
    fractions_section,
    decimaux_section,
    proportionnalite_section,
    geometrie_section,
    mesures_section,
    monnaie_section,
    mode_entraineur_section,
    dashboard_statistiques,
    lancer_exercice_recommande
)

def main():
    init_fichier_securise()
    verifier_authentification()
    # ✅ FORCER LE CHARGEMENT DU PROFIL SI ABSENT
    if st.session_state.get('authentifie', False) and 'profil' not in st.session_state:
        nom = st.session_state.get('utilisateur')
        profil = charger_utilisateur(nom)
        if profil is None:
            profil = profil_par_defaut()
        st.session_state['profil'] = profil
    
    init_session_state()
    st.markdown(local_css(), unsafe_allow_html=True)

    with st.sidebar:
        # --- Section PROFIL ÉLÈVE ---
        if not st.session_state.get('authentifie', False):
            st.warning("Authentifiés d'abord!")
            st.stop()

        st.title("👤 Profil élève")
        st.write(f"Utilisateur: **{st.session_state.utilisateur}**")
        
        # Sélecteur niveau
        st.markdown("---")
        st.subheader("📚 Choisi ton niveau:")
        nouveau_niveau = st.selectbox(
            "Niveau:",
            ["CE1", "CE2", "CM1", "CM2"],
            index=["CE1", "CE2", "CM1", "CM2"].index(st.session_state.get('niveau', 'CE1'))
        )
        if nouveau_niveau != st.session_state.get('niveau'):
            st.session_state.niveau = nouveau_niveau
            st.success(f"✅ Niveau changé à {nouveau_niveau}")
        
        st.markdown("---")
        
        # Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Points", st.session_state.get('points', 0))
        col2.metric("Niveau", st.session_state.get('niveau', 'CE1'))
        col3.metric("Badges", len(st.session_state.get('badges', [])))

        if st.button("🔄 Déconnexion"):
            st.session_state.authentifie = False
            st.rerun()
        
        # Section À propos
        st.markdown("---")
        st.markdown("### 📞 À Propos")
        st.markdown("""
        **MathCopain v6.3**
        
        Application gratuite pour apprendre 
        le calcul mental par le jeu.
        
        **Développé par:** Pascal Dao
        
        **Contact:**
        - 📧 Email: mathcopain.contact@gmail.com
        - 💬 Formulaire: https://forms.gle/3MieMDCxG47ooNbn9
              
        **Version:** v6.3
        **Mise à jour:** 15 Nov 2025
        """)
        
        st.markdown("---")
        st.caption("💚 Fait avec passion pour les enfants")
    
    # MAIN CONTENT
    st.title(f"🎓 {__title__} - Le Calcul Mental sans Pression")
    st.caption(f"Version {__version__}")

    # Daily challenge
    exercise_generator.generer_daily_challenge()
    if st.session_state.daily_challenge['challenge']:
        challenge = st.session_state.daily_challenge['challenge']
        st.markdown(f'<div class="daily-challenge-box">', unsafe_allow_html=True)
        st.write(f"### 🎯 DÉFI DU JOUR")
        st.write(f"**{challenge['text']}**")
        st.progress(0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Streak
    if st.session_state.streak['current'] > 0:
        st.markdown(f'<div class="streak-box">🔥 STREAK ACTUEL : {st.session_state.streak["current"]} 🔥</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # NAVIGATION PRINCIPALE
    categories = ["Exercice", "Jeu", "Fractions", "Géométrie", "Décimaux", "Proportionnalité", "Mesures", "Monnaie", "Entraîneur", "Défi", "Statistiques"]
    categorie_selectionnee = st.radio(
        "Choisis ce que tu veux faire :", 
        categories, 
        horizontal=True, 
        key="main_radio"
    )
    
    st.markdown("---")
    
    # Reset état si changement catégorie
    if categorie_selectionnee != st.session_state.active_category:
        st.session_state.exercice_courant = None
        st.session_state.show_feedback = False
        st.session_state.jeu_type = None
        st.session_state.jeu_memory = None
        st.session_state.memory_first_flip = None
        st.session_state.memory_second_flip = None
        st.session_state.memory_incorrect_pair = None
        st.session_state.active_category = categorie_selectionnee
        st.rerun()
    
    # DISPATCHER SELON CATÉGORIE
    if categorie_selectionnee == "Exercice":
        exercice_rapide_section()
    
    elif categorie_selectionnee == "Jeu":
        jeu_section()
    
    elif categorie_selectionnee == "Fractions":
        fractions_section()
    
    elif categorie_selectionnee == "Géométrie":
        geometrie_section()
    elif categorie_selectionnee == "Décimaux":
        decimaux_section()
    elif categorie_selectionnee == "Proportionnalité":
        proportionnalite_section()
    elif categorie_selectionnee == "Mesures":
        mesures_section()

    elif categorie_selectionnee == "Monnaie":
        monnaie_section()

    elif categorie_selectionnee == "Entraîneur":  # ✅ CORRECTION ICI
        mode_entraineur_section()
    
    elif categorie_selectionnee == "Défi":
        defi_section()
    elif categorie_selectionnee == "Statistiques":
        dashboard_statistiques()  # ✅ AJOUTER CET APPELtiques()


if __name__ == "__main__":
    main()

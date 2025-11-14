import streamlit as st
import random
from datetime import date, datetime
from authentification import init_fichier_securise
from ui_authentification import verifier_authentification
from utilisateur import charger_utilisateur, sauvegarder_utilisateur, obtenir_tous_eleves, profil_par_defaut  # ← AJOUTER
from fractions_utils import pizza_interactive, afficher_fraction_droite, dessiner_pizza  # ← VÉRIFIER
from division_utils import generer_division_simple, generer_division_reste  # ← AJOUTER
from adaptive_system import AdaptiveSystem
from skill_tracker import SkillTracker
from monnaie_utils import (  # ← NOUVEAU MODULE
    generer_calcul_rendu,
    generer_composition_monnaie,
    generer_probleme_realiste,
    dessiner_pieces_monnaie,
    expliquer_calcul_rendu,
    centimes_vers_euros_texte
)
# Modules refactorisés Phase 3
from modules.exercices import generer_addition, generer_soustraction, generer_tables, generer_division
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
# Déplacé vers modules/exercices.py (Phase 3)
@st.cache_data
def generer_explication(exercice_type, question, reponse_utilisateur, reponse_correcte):
    """
    Génère explication pédagogique selon type d'erreur (CACHÉ)
    """
    
    if exercice_type == "addition":
        a, b = map(int, question.replace(" ", "").split("+"))
        
        # Décomposition par dizaines
        if a >= 10 or b >= 10:
            dizaine_a = (a // 10) * 10
            unite_a = a % 10
            dizaine_b = (b // 10) * 10
            unite_b = b % 10
            
            explication = f"""
            💡 **Décomposons ensemble:**
            
            {a} = {dizaine_a} + {unite_a}
            {b} = {dizaine_b} + {unite_b}
            
            **Étape 1:** Additionne les dizaines
            → {dizaine_a} + {dizaine_b} = {dizaine_a + dizaine_b}
            
            **Étape 2:** Additionne les unités
            → {unite_a} + {unite_b} = {unite_a + unite_b}
            
            **Étape 3:** Somme finale
            → {dizaine_a + dizaine_b} + {unite_a + unite_b} = **{reponse_correcte}**
            """
        else:
            # Méthode des bonds
            explication = f"""
            💡 **Méthode des bonds:**
            
            Commence à {a}
            → Fais un bond de {b}
            → Tu arrives à **{reponse_correcte}**
            
            Ou autrement: {a} + {b//2} = {a + b//2}, puis +{b - b//2} = **{reponse_correcte}**
            """
            
        # Astuce selon difficulté
        if b == 9:
            astuce = f"✨ **Astuce:** Pour +9, fais +10 puis -1 → {a}+10={a+10}, puis -1={reponse_correcte}"
        elif b == 8:
            astuce = f"✨ **Astuce:** Pour +8, fais +10 puis -2 → {a}+10={a+10}, puis -2={reponse_correcte}"
        else:
            astuce = ""
            
        return explication + "\n" + astuce
    
    elif exercice_type == "soustraction":
        a, b = map(int, question.replace(" ", "").split("-"))
        
        # Vérifier si retenue
        if a % 10 < b % 10:
            explication = f"""
            💡 **Soustraction avec retenue:**
            
            {a} - {b} = ?
            
            **Problème:** On ne peut pas enlever {b % 10} de {a % 10}
            
            **Solution:**
            1. Emprunte une dizaine
            2. {a} devient {(a//10 - 1)*10 + 10 + a%10}
            3. Maintenant: {10 + a%10} - {b%10} = {10 + a%10 - b%10}
            4. Puis: {(a//10 - 1)*10} - {(b//10)*10} = {(a//10 - 1)*10 - (b//10)*10}
            5. Total: **{reponse_correcte}**
            """
        else:
            explication = f"""
            💡 **Soustraction simple:**
            
            {a} - {b} = ?
            
            Enlève les dizaines: {(a//10)*10} - {(b//10)*10} = {(a//10 - b//10)*10}
            Enlève les unités: {a%10} - {b%10} = {a%10 - b%10}
            Résultat: **{reponse_correcte}**
            """
            
        return explication
    
    elif exercice_type == "multiplication":
        table, mult = map(int, question.replace(" ", "").replace("×", " ").split())
        
        # Stratégies selon multiplication
        strategies = []
        
        # Stratégie 1: Doubler
        if mult % 2 == 0:
            demi = mult // 2
            strategies.append(f"**Méthode 1 (Doubler):**\n{table}×{demi} = {table*demi}\nDouble: {table*demi}×2 = **{reponse_correcte}**")
        
        # Stratégie 2: Par 10
        if mult <= 10:
            strategies.append(f"**Méthode 2 (Par 10):**\n{table}×10 = {table*10}\nEnlève {table}×{10-mult}: {table*10} - {table*(10-mult)} = **{reponse_correcte}**")
        
        # Stratégie 3: Décomposer
        if mult >= 6:
            strategies.append(f"**Méthode 3 (Décomposer):**\n{table}×5 = {table*5}\n{table}×{mult-5} = {table*(mult-5)}\nSomme: {table*5} + {table*(mult-5)} = **{reponse_correcte}**")
        
        explication = f"💡 **Plusieurs façons de calculer {table}×{mult}:**\n\n" + "\n\n".join(strategies)
        explication += f"\n\n✨ **Choisis la méthode qui te semble la plus facile!**"
        
        return explication
    
    elif exercice_type == "division":
        try:
            dividende, diviseur = map(int, question.replace(" ", "").replace("÷", " ").split())
        except:
            return "Regarde bien le calcul et réessaye!"
        
        quotient = dividende // diviseur
        reste = dividende % diviseur
        
        explication = f"""
        💡 **Division : {dividende} ÷ {diviseur}**
        
        **Méthode 1 : Par les tables**
        Cherche dans la table de {diviseur} :
        """
        
        # Afficher table de référence
        table_ref = []
        for i in range(1, 13):
            resultat = diviseur * i
            if resultat <= dividende + diviseur:
                if resultat == dividende:
                    table_ref.append(f"✅ {diviseur} × {i} = {resultat} ← C'est ça!")
                elif resultat < dividende:
                    table_ref.append(f"{diviseur} × {i} = {resultat}")
                else:
                    table_ref.append(f"⚠️ {diviseur} × {i} = {resultat} (trop grand)")
                    break
        
        explication += "\n" + "\n".join(table_ref)
        
        if reste > 0:
            explication += f"""
            
            **Attention : Il y a un reste!**
            {dividende} = ({diviseur} × {quotient}) + {reste}
            
            Donc : **{dividende} ÷ {diviseur} = {quotient} reste {reste}**
            """
        else:
            explication += f"""
            
            **Résultat exact : {dividende} ÷ {diviseur} = {quotient}**
            """
        
        explication += """
        
        ✨ **Astuce :** Pour vérifier, multiplie le quotient par le diviseur!
        """
        
        return explication
    
    return "Regarde bien le calcul et réessaye!"
def generer_droite_numerique(niveau):
    max_val = {"CE1": 100, "CE2": 1000, "CM1": 10000}.get(niveau, 100000)
    nombre = random.randint(0, max_val)
    return {'nombre': nombre, 'min': 0, 'max': max_val}

@st.cache_data
def calculer_score_droite(reponse, correct):
    """Calcule score droite numérique selon distance (CACHÉ)"""
    distance = abs(reponse - correct)
    max_val = correct if correct > 0 else 100
    if distance <= max_val * 0.10:
        return 20, "Excellent ! (±10%)"
    elif distance <= max_val * 0.20:
        return 5, "Presque ! (±20%)"
    else:
        return 0, f"Trop loin (distance: {distance})"

def generer_memory_emoji(niveau):
    emojis = ['🍎', '🐶', '🎨', '🌟', '🎭', '🎸', '🚀', '🏆', '🎮', '🍕', '🐱', '⚽', '🎪', '🎯', '🌈', '🍦']
    if niveau == "CE1":
        paires = emojis[:4]
    elif niveau == "CE2":
        paires = emojis[:6]
    elif niveau == "CM1":
        paires = emojis[:8]
    else:
        paires = emojis[:10]
    cards = paires + paires
    random.shuffle(cards)
    return {
        'cards': cards,
        'revealed': set(),
        'matched': set()
    }

def generer_probleme(niveau):
    contextes = [
        ("Marie a {a} billes. Son ami lui en donne {b}.", "Combien a-t-elle ?", "addition"),
        ("Théo a {a} euros. Il achète quelque chose qui coûte {b} euros.", "Combien lui reste-t-il ?", "soustraction"),
        ("Il y a {a} rangées de {b} chaises.", "Combien de chaises en tout ?", "multiplication"),
        ("On partage {a} bonbons entre {b} enfants.", "Combien chacun a ?", "division")
    ]
    contexte_base, question, operation = random.choice(contextes)
    params = {'CE1': (5, 20, 2, 10), 'CE2': (20, 50, 5, 30), 'CM1': (50, 200, 10, 50)}
    a1, a2, b1, b2 = params.get(niveau, (100, 500, 20, 100))
    a, b = random.randint(a1, a2), random.randint(b1, b2)
    contexte = contexte_base.format(a=a, b=b)
    if operation == "addition":
        reponse = a + b
    elif operation == "soustraction":
        if a < b: a, b = b, a
        reponse = a - b
    elif operation == "multiplication":
        reponse = a * b
    else:
        reponse = a // b if b > 0 else 0
    return {'question': f"{contexte} {question}", 'reponse': reponse}

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

def generer_daily_challenge():
    today = str(date.today())
    if st.session_state.daily_challenge.get('today_date') != today:
        random.seed(today)
        challenges = [
            {'type': 'addition', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses en Addition'},
            {'type': 'soustraction', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses en Soustraction'},
            {'type': 'tables', 'objectif': 5, 'text': 'Enchaîne 5 bonnes réponses aux Tables'},
            {'type': 'droite', 'objectif': 3, 'text': 'Fais 3 bonnes estimations à la Droite'}
        ]
        challenge = random.choice(challenges)
        st.session_state.daily_challenge = {
            'today_date': today,
            'completed': False,
            'challenge': challenge,
            'progress': 0
        }

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

# =============== EXERCICE RAPIDE SECTION ===============
# Callbacks pour éliminer st.rerun()
def _callback_exercice_addition():
    st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_exercice_soustraction():
    st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_exercice_tables():
    st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_exercice_division():
    st.session_state.exercice_courant = generer_division(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_validation_exercice():
    """Callback pour valider un exercice"""
    ex = st.session_state.exercice_courant
    reponse = st.session_state.input_ex

    # Déterminer le type d'exercice
    if "+" in ex['question']:
        exercice_type = "addition"
    elif "-" in ex['question']:
        exercice_type = "soustraction"
    elif "×" in ex['question']:
        exercice_type = "multiplication"
    elif "÷" in ex['question']:
        exercice_type = "division"
    else:
        exercice_type = "autre"

    # Validation de la réponse
    if '÷' in ex['question'] and 'reste' in ex:
        quotient_correct = ex['reponse']
        correct = (reponse == quotient_correct)
    else:
        correct = (reponse == ex['reponse'])

    # Enregistrer dans système adaptatif
    if "profil" in st.session_state:
        tracker = SkillTracker(st.session_state.profil)
        tracker.record_exercise(exercice_type, correct, difficulty=3)

    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
    if correct:
        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
        st.session_state.points += 10

    maj_streak(correct)
    bonus = calculer_bonus_streak(st.session_state.streak['current'])
    if correct and bonus > 0:
        st.session_state.points += bonus

    st.session_state.feedback_correct = correct
    st.session_state.feedback_reponse = reponse
    st.session_state.dernier_exercice = ex
    st.session_state.dernier_exercice_type = exercice_type
    st.session_state.show_feedback = True
    st.session_state.scores_history.append({
        'type': 'Calcul Mental',
        'points': 10 + bonus,
        'date': str(date.today())
    })
    nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
    st.session_state.badges.extend(nouveaux)
    auto_save_profil(correct)

def _callback_reessayer_exercice():
    """Callback pour réessayer un exercice similaire"""
    exercice_type = st.session_state.get('dernier_exercice_type', 'autre')
    if exercice_type == "addition":
        st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
    elif exercice_type == "soustraction":
        st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
    elif exercice_type == "multiplication":
        st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
    elif exercice_type == "division":
        st.session_state.exercice_courant = generer_division(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_exercice_suivant():
    """Callback pour passer à l'exercice suivant"""
    if "+" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
    elif "-" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
    elif "÷" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = generer_division(st.session_state.niveau)
    else:
        st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
    st.session_state.show_feedback = False

def exercice_rapide_section():
    st.markdown('<div class="categorie-header">📚 Exercice Rapide - Calcul Mental</div>', unsafe_allow_html=True)
    st.write("⚡ Sois rapide et précis !")

    # Adapter les boutons au niveau de l'élève
    if st.session_state.niveau == "CE1":
        # Pour les CE1, on ne montre pas la division
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("➕ Addition", key="btn_add", use_container_width=True, on_click=_callback_exercice_addition)
        with col2:
            st.button("➖ Soustraction", key="btn_sub", use_container_width=True, on_click=_callback_exercice_soustraction)
        with col3:
            st.button("🔢 Tables", key="btn_mult", use_container_width=True, on_click=_callback_exercice_tables)
    else:
        # Pour les autres niveaux, on montre les 4 boutons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("➕ Addition", key="btn_add", use_container_width=True, on_click=_callback_exercice_addition)
        with col2:
            st.button("➖ Soustraction", key="btn_sub", use_container_width=True, on_click=_callback_exercice_soustraction)
        with col3:
            st.button("🔢 Tables", key="btn_mult", use_container_width=True, on_click=_callback_exercice_tables)
        with col4:
            st.button("➗ Division", key="btn_div", use_container_width=True, on_click=_callback_exercice_division)

    st.markdown("---")
    if st.session_state.exercice_courant:
        ex = st.session_state.exercice_courant
        st.markdown(f'<div class="exercice-box">{ex["question"]} = ?</div>', unsafe_allow_html=True)
        if not st.session_state.show_feedback:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Réponse :", key="input_ex", value=0, step=1)
            with col2:
                st.write("")
                st.write("")
                st.button("✅ Valider", use_container_width=True, key="btn_val_ex", on_click=_callback_validation_exercice)
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            if st.session_state.feedback_correct:
                bonus = calculer_bonus_streak(st.session_state.streak['current'])
                bonus_text = f" +{bonus} bonus!" if bonus > 0 else ""
                st.markdown(f'<div class="feedback-success">🎉 BRAVO !{bonus_text}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Mauvais ! La réponse était {st.session_state.dernier_exercice["reponse"]}</div>', unsafe_allow_html=True)
                
                # 🆕 EXPLICATION DÉTAILLÉE
                st.markdown("---")
                st.markdown("### 📚 Comprendre l'erreur")

                # ✅ Récupérer le type d'exercice depuis session_state
                exercice_type = st.session_state.get('dernier_exercice_type', 'autre')

                # Générer explication
                explication = generer_explication(
                    exercice_type,
                    st.session_state.dernier_exercice['question'],
                    st.session_state.feedback_reponse,
                    st.session_state.dernier_exercice['reponse']
                )
                st.markdown(explication)



                # Bouton "Réessayer même type"
                st.button("🔄 Réessayer un similaire", key="btn_retry", on_click=_callback_reessayer_exercice)

            # Bouton "SUIVANT" (commun à juste/faux)
            st.button("➡️ SUIVANT", use_container_width=True, key="btn_next", on_click=_callback_exercice_suivant)

# ================= SECTION JEUX ===================
# Callbacks pour jeux
def _callback_jeu_droite():
    st.session_state.jeu_type = 'droite'
    st.session_state.exercice_courant = generer_droite_numerique(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_jeu_memory():
    st.session_state.jeu_type = 'memory'
    st.session_state.jeu_memory = generer_memory_emoji(st.session_state.niveau)
    st.session_state.memory_first_flip = None
    st.session_state.memory_second_flip = None
    st.session_state.memory_incorrect_pair = None

def _callback_validation_droite():
    dn = st.session_state.exercice_courant
    reponse = st.session_state.slider_dn
    score, message = calculer_score_droite(reponse, dn['nombre'])
    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
    if score > 0:
        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
        st.session_state.points += score
    maj_streak(score > 0)
    bonus = calculer_bonus_streak(st.session_state.streak['current'])
    if score > 0 and bonus > 0:
        st.session_state.points += bonus
    st.session_state.feedback_correct = score >= 20
    st.session_state.feedback_reponse = reponse
    st.session_state.dernier_exercice = {'nombre': dn['nombre'], 'message': message, 'score': score}
    st.session_state.show_feedback = True

    if "profil" in st.session_state:
        tracker = SkillTracker(st.session_state.profil)
        tracker.record_exercise('droite_numerique', score > 0, difficulty=dn['max'] // 1000)

    st.session_state.scores_history.append({'type': 'Droite Numérique', 'points': score + bonus, 'date': str(date.today())})
    nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
    st.session_state.badges.extend(nouveaux)
    auto_save_profil(score > 0)

def _callback_suivant_droite():
    st.session_state.exercice_courant = generer_droite_numerique(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_nouvelle_partie_memory():
    st.session_state.jeu_memory = generer_memory_emoji(st.session_state.niveau)
    st.session_state.memory_first_flip = None
    st.session_state.memory_second_flip = None
    st.session_state.memory_incorrect_pair = None

def _callback_memory_card(idx):
    """Callback pour cliquer sur une carte Memory"""
    memory = st.session_state.jeu_memory
    # Premier clic
    if st.session_state.memory_first_flip is None:
        st.session_state.memory_first_flip = idx
        memory['revealed'].add(idx)
    # Deuxième clic
    elif st.session_state.memory_second_flip is None and idx != st.session_state.memory_first_flip:
        st.session_state.memory_second_flip = idx
        memory['revealed'].add(idx)
        # Vérification automatique après deuxième clic
        first_idx = st.session_state.memory_first_flip
        second_idx = idx
        if memory['cards'][first_idx] == memory['cards'][second_idx]:
            memory['matched'].add(first_idx)
            memory['matched'].add(second_idx)
            st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
            st.session_state.points += 5
        else:
            st.session_state.memory_incorrect_pair = {first_idx, second_idx}
        st.session_state.memory_first_flip = None
        st.session_state.memory_second_flip = None
        auto_save_profil(True)

def jeu_section():
    st.markdown('<div class="categorie-header">🎮 Jeux</div>', unsafe_allow_html=True)
    st.write("Sélectionne un jeu !")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📊 Droite Numérique", use_container_width=True, key="btn_droite", on_click=_callback_jeu_droite)
    with col2:
        st.button("🧠 Memory", use_container_width=True, key="btn_memory", on_click=_callback_jeu_memory)
    st.markdown("---")
    # DROITE NUMÉRIQUE
    if st.session_state.get('jeu_type') == 'droite' and st.session_state.exercice_courant:
        dn = st.session_state.exercice_courant
        st.subheader(f"📍 Place le nombre {dn['nombre']} sur la droite")
        st.write(f"*De {dn['min']} à {dn['max']}*")
        if not st.session_state.show_feedback:
            st.write("⬇️ Déplace le curseur :")
            reponse = st.slider("Position", min_value=dn['min'], max_value=dn['max'], value=dn['max']//2, key="slider_dn", label_visibility="collapsed")
            st.button("✅ Valider", use_container_width=True, key="btn_val_droite", on_click=_callback_validation_droite)
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            st.info(f"🎯 Tu as placé : **{st.session_state.feedback_reponse}**")
            if st.session_state.dernier_exercice.get('score', 0) >= 20:
                st.markdown(f'<div class="feedback-success">🎉 EXCELLENT ! {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
                st.balloons()
            elif st.session_state.dernier_exercice.get('score', 0) > 0:
                st.markdown(f'<div class="feedback-success">👍 Pas mal ! {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-error">❌ {st.session_state.dernier_exercice.get("message", "")}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ton placement :** {st.session_state.feedback_reponse}")
                st.write(f"**Distance :** {abs(st.session_state.feedback_reponse - st.session_state.dernier_exercice['nombre'])} unités")
            with col2:
                st.button("➡️ SUIVANT", use_container_width=True, key="btn_next_droite", on_click=_callback_suivant_droite)
    # MEMORY
    elif st.session_state.get('jeu_type') == 'memory' and st.session_state.jeu_memory:
        st.subheader("🧠 Memory - Trouve les paires !")
        memory = st.session_state.jeu_memory
        total_pairs = len(memory['cards']) // 2
        pairs_found = len(memory['matched']) // 2
        st.write(f"Paires trouvées : **{pairs_found}/{total_pairs}**")
        st.progress(pairs_found / total_pairs)
        if st.session_state.memory_incorrect_pair:
            memory['revealed'].difference_update(st.session_state.memory_incorrect_pair)
            st.session_state.memory_incorrect_pair = None
        cols = st.columns(4)
        for idx in range(len(memory['cards'])):
            col = cols[idx % 4]
            with col:
                card_value = memory['cards'][idx]
                if idx in memory['matched']:
                    st.markdown(
                        f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #90EE90 0%, #28a745 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 32px'>{card_value}</div>",
                        unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_matched", disabled=True, use_container_width=True)
                elif idx in memory['revealed']:
                    st.markdown(
                        f"<div style='aspect-ratio: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 32px'>{card_value}</div>",
                        unsafe_allow_html=True)
                    st.button("✓", key=f"mem_{idx}_revealed", disabled=True, use_container_width=True)
                else:
                    st.button("?", key=f"mem_{idx}", use_container_width=True, on_click=_callback_memory_card, args=(idx,))
        if len(memory['matched']) == len(memory['cards']):
            st.markdown("---")
            st.markdown(f'<div class="feedback-success">🎉 BRAVO ! Tu as trouvé toutes les paires !</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.points += 50
            st.session_state.scores_history.append({'type': 'Memory', 'points': 50, 'date': str(date.today())})
            auto_save_profil(True)
            st.button("➡️ Nouvelle partie", use_container_width=True, key="btn_new_memory", on_click=_callback_nouvelle_partie_memory)

# ============== DÉFI SECTION ==============
# ============== DÉFI SECTION - VERSION CORRIGÉE ==============
def defi_section():
    st.markdown('<div class="categorie-header">🚀 Défi - Problèmes Contextualisés</div>', unsafe_allow_html=True)
    st.write("💡 Résous des problèmes du monde réel.")
    
    if st.button("🚀 Commencer Défi", use_container_width=True, key="btn_start_defi"):
        st.session_state.exercice_courant = generer_probleme(st.session_state.niveau)
        st.session_state.show_feedback = False
        st.rerun()
    
    st.markdown("---")
    
    if st.session_state.exercice_courant:
        ex = st.session_state.exercice_courant
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        if not st.session_state.show_feedback:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Réponse :", key="input_defi", value=0, step=1)
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Valider", use_container_width=True, key="btn_val_defi"):
                    correct = reponse == ex['reponse']
                    
                    # ✅ Mettre à jour les stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        st.session_state.points += 30
                    
                    maj_streak(correct)
                    bonus = calculer_bonus_streak(st.session_state.streak['current'])
                    if correct and bonus > 0:
                        st.session_state.points += bonus
                    
                    # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('probleme', correct, difficulty=4)
                    
                    # ✅ CORRECTION : Ces lignes sont maintenant au bon niveau d'indentation
                    st.session_state.feedback_correct = correct
                    st.session_state.feedback_reponse = reponse
                    st.session_state.dernier_exercice = ex
                    st.session_state.show_feedback = True
                    st.session_state.scores_history.append({
                        'type': 'Défi', 
                        'points': (30 if correct else 0) + bonus, 
                        'date': str(date.today())
                    })
                    nouveaux = verifier_badges(st.session_state.points, st.session_state.badges)
                    st.session_state.badges.extend(nouveaux)
                    auto_save_profil(correct)
                    st.rerun()
        
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            st.markdown("---")
            if st.session_state.feedback_correct:
                st.markdown('<div class="feedback-success">🎉 EXCELLENT ! C\'est juste !</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ La réponse était {st.session_state.dernier_exercice["reponse"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ton choix :** {st.session_state.feedback_reponse}")
                st.write(f"**Réponse :** {st.session_state.dernier_exercice['reponse']}")
            with col2:
                if st.button("➡️ SUIVANT", use_container_width=True, key="btn_next_defi"):
                    st.session_state.exercice_courant = generer_probleme(st.session_state.niveau)
                    st.session_state.show_feedback = False
                    st.rerun()

# =============== MAIN =======================
# =============== MAIN =======================
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
        **MathCopain v5.2**
        
        Application gratuite pour apprendre 
        le calcul mental par le jeu.
        
        **Développé par:** Pascal Dao
        
        **Contact:**
        - 📧 Email: mathcopain.contact@gmail.com
        - 💬 Formulaire: https://forms.gle/3MieMDCxG47ooNbn9
              
        **Version:** v5.2
        **Mise à jour:** 6 Nov 2025
        """)
        
        st.markdown("---")
        st.caption("💚 Fait avec passion pour les enfants")
    
    # MAIN CONTENT
    st.title("🎓 MathCopain - Le Calcul Mental sans Pression")
    
    # Daily challenge
    generer_daily_challenge()
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

from fractions_utils import pizza_interactive, afficher_fraction_droite, dessiner_pizza

def fractions_section():
    """
    Section Fractions Visuelles - 3 modes:
    1. Identifier fraction (CE2-CM1)
    2. Produire fraction (CM1-CM2)
    3. Placer sur droite (CM2)
    """
    
    st.markdown('<div class="categorie-header">🍕 Fractions Visuelles</div>', unsafe_allow_html=True)
    
    # Adapter selon niveau
    if st.session_state.niveau == "CE1":
        st.info("Les fractions commencent au CE2. Continue à t'entraîner au calcul mental!")
        return
    
    # Choisir mode
    if st.session_state.niveau == "CE2":
        mode = "identifier"
    elif st.session_state.niveau == "CM1":
        mode_choice = st.radio("Mode:", ["Identifier", "Produire"], horizontal=True, key="frac_mode")
        mode = mode_choice.lower()
    else:  # CM2
        mode_choice = st.radio("Mode:", ["Identifier", "Produire", "Droite Numérique"], horizontal=True, key="frac_mode")
        mode = mode_choice.lower().replace(" ", "_")
    
    st.markdown("---")
    
    # ==========================================
    # MODE 1: IDENTIFIER
    # ==========================================
    if mode == "identifier":
        st.subheader("🔍 Quelle fraction est coloriée?")
        
        # Initialiser session state pour identifier
        if 'fraction_identifier' not in st.session_state:
            st.session_state.fraction_identifier = {
                'exercice': None,
                'attente_reponse': True,
                'feedback_affiche': False
            }
        
        frac_state = st.session_state.fraction_identifier
        
        # Générer nouvel exercice si nécessaire
        if frac_state['exercice'] is None:
            # Fractions selon niveau
            if st.session_state.niveau == "CE2":
                fractions = [(1,2), (1,3), (1,4), (2,4), (3,4)]
            else:  # CM1
                fractions = [(1,2), (2,3), (3,4), (2,5), (3,6), (4,8)]
            
            num, denom = random.choice(fractions)
            parts_colorees = list(range(num))
            
            # Générer options
            correct = f"{num}/{denom}"
            options = [correct]
            
            # Ajouter pièges intelligents
            if num < denom - 1:
                options.append(f"{denom - num}/{denom}")  # Inverse (parts non coloriées)
            if denom < 8:
                options.append(f"{num}/{denom + 1}")  # Dénominateur +1
            if num < denom:
                options.append(f"{num + 1}/{denom}")  # Numérateur +1
            
            # Compléter avec options aléatoires si besoin
            while len(options) < 4:
                rand_num = random.randint(1, denom)
                rand_frac = f"{rand_num}/{denom}"
                if rand_frac not in options:
                    options.append(rand_frac)
            
            random.shuffle(options)
            
            frac_state['exercice'] = {
                'numerateur': num,
                'denominateur': denom,
                'parts_colorees': parts_colorees,
                'correct': correct,
                'options': options
            }
            frac_state['attente_reponse'] = True
            frac_state['feedback_affiche'] = False
        
        ex = frac_state['exercice']
        
        # Afficher pizza
        st.markdown(dessiner_pizza(ex['denominateur'], ex['parts_colorees'], 300), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Afficher feedback si déjà cliqué
        if frac_state['feedback_affiche']:
            if frac_state['reponse_correcte']:
                st.markdown('<div class="feedback-success">🎉 BRAVO ! C\'est exact !</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Incorrect</div>', unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("### 📚 Comprendre")
                st.write(f"🍕 La pizza est divisée en **{ex['denominateur']} parts égales** (le dénominateur)")
                st.write(f"🟨 On a colorié **{ex['numerateur']} parts** (le numérateur)")
                st.write(f"✨ Donc la fraction est: **{ex['correct']}**")
            
            st.markdown("---")
            
            # Bouton suivant
            if st.button("➡️ Exercice Suivant", key="frac_id_next", use_container_width=True):
                # Reset complet
                st.session_state.fraction_identifier = {
                    'exercice': None,
                    'attente_reponse': True,
                    'feedback_affiche': False
                }
                st.rerun()
        
        # Afficher options si en attente de réponse
        elif frac_state['attente_reponse']:
            st.write("**Choisis la bonne fraction:**")
            
            # Afficher boutons
            cols = st.columns(2)
            for idx, option in enumerate(ex['options']):
                col = cols[idx % 2]
                with col:
                    if st.button(option, key=f"frac_opt_{idx}", use_container_width=True):
                        # Valider réponse
                        correct_answer = (option == ex['correct'])
                        
                        # Sauvegarder résultat
                        frac_state['reponse_correcte'] = correct_answer
                        frac_state['attente_reponse'] = False
                        frac_state['feedback_affiche'] = True
                        
                        # Mettre à jour stats
                        st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                        if correct_answer:
                            st.session_state.points += 15
                            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        
                        # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                        if "profil" in st.session_state:
                            tracker = SkillTracker(st.session_state.profil)
                            tracker.record_exercise('fractions', correct_answer, difficulty=2)
                        
                        auto_save_profil(correct_answer)
                        st.rerun()
    
    # ==========================================
    # MODE 2: PRODUIRE
    # ==========================================
    elif mode == "produire":
        st.subheader(f"🎨 Colorie la fraction demandée")
        
        # Initialiser session state pour produire
        if 'fraction_produire' not in st.session_state:
            st.session_state.fraction_produire = {
                'exercice': None,
                'feedback_affiche': False
            }
        
        frac_state = st.session_state.fraction_produire
        
        # Générer nouvel exercice si nécessaire
        if frac_state['exercice'] is None:
            if st.session_state.niveau == "CM1":
                fractions = [(1,2), (1,3), (2,3), (1,4), (3,4)]
            else:  # CM2
                fractions = [(2,3), (3,4), (4,5), (3,8), (5,6), (7,10)]
            
            num, denom = random.choice(fractions)
            
            frac_state['exercice'] = {
                'numerateur': num,
                'denominateur': denom,
                'parts_correctes': set(range(num))
            }
            frac_state['feedback_affiche'] = False
            
            # Reset sélection pizza
            if 'produce_pizza_selected' in st.session_state:
                del st.session_state['produce_pizza_selected']
        
        ex = frac_state['exercice']
        
        # Afficher consigne
        st.markdown(f"### Colorie **{ex['numerateur']}/{ex['denominateur']}** de la pizza")
        
        # Afficher feedback si déjà validé
        if frac_state['feedback_affiche']:
            selected = st.session_state.get('produce_pizza_selected', set())
            
            if len(selected) == ex['numerateur']:
                st.markdown('<div class="feedback-success">🎉 Bravo! Tu as colorié le bon nombre de parts!</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Tu as colorié {len(selected)}/{ex["denominateur"]}</div>', unsafe_allow_html=True)
                st.markdown("---")
                st.write(f"💡 **{ex['numerateur']}/{ex['denominateur']}** veut dire:")
                st.write(f"- Divise la pizza en **{ex['denominateur']} parts égales**")
                st.write(f"- Colorie exactement **{ex['numerateur']} parts**")
            
            st.markdown("---")
            
            # Bouton suivant
            if st.button("➡️ Exercice Suivant", key="frac_prod_next", use_container_width=True):
                # Reset complet
                st.session_state.fraction_produire = {
                    'exercice': None,
                    'feedback_affiche': False
                }
                if 'produce_pizza_selected' in st.session_state:
                    del st.session_state['produce_pizza_selected']
                st.rerun()
        
        # Afficher pizza interactive si pas encore validé
        else:
            # Pizza interactive
            selected = pizza_interactive(ex['denominateur'], "produce_pizza")
            
            st.markdown("---")
            st.write(f"**Parts sélectionnées : {len(selected)}/{ex['denominateur']}**")
            
            # Validation
            if st.button("✅ Vérifier", key="frac_verify", use_container_width=True):
                correct_answer = (len(selected) == ex['numerateur'])
                
                # Sauvegarder résultat
                frac_state['feedback_affiche'] = True
                
                # Mettre à jour stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if correct_answer:
                    st.session_state.points += 20
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                
                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('fractions', correct_answer, difficulty=3)
                
                auto_save_profil(correct_answer)
                st.rerun()
    
    # ==========================================
    # MODE 3: DROITE NUMÉRIQUE
    # ==========================================
    elif mode == "droite_numérique":
        st.subheader("📏 Place la fraction sur la droite")
        
        # Initialiser session state pour droite
        if 'fraction_droite' not in st.session_state:
            st.session_state.fraction_droite = {
                'exercice': None,
                'feedback_affiche': False
            }
        
        frac_state = st.session_state.fraction_droite
        
        # Générer nouvel exercice si nécessaire
        if frac_state['exercice'] is None:
            fractions = [(1,2), (1,3), (2,3), (1,4), (3,4), (1,5), (2,5), (3,5), (4,5)]
            num, denom = random.choice(fractions)
            
            frac_state['exercice'] = {
                'numerateur': num,
                'denominateur': denom,
                'valeur': num / denom
            }
            frac_state['feedback_affiche'] = False
        
        ex = frac_state['exercice']
        
        # Afficher consigne
        st.write(f"### Où se situe **{ex['numerateur']}/{ex['denominateur']}** sur la droite?")
        st.write("*La droite va de 0 à 1*")
        
        # Afficher feedback si déjà validé
        if frac_state['feedback_affiche']:
            distance = frac_state['distance']
            score = frac_state['score']
            reponse = frac_state['reponse']
            
            # Afficher résultat
            if score >= 25:
                st.markdown('<div class="feedback-success">🎯 Excellent! Tu es très précis!</div>', unsafe_allow_html=True)
                st.balloons()
            elif score >= 10:
                st.markdown('<div class="feedback-success">👍 Pas mal! Tu es proche</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="feedback-error">❌ Trop loin, regarde bien</div>', unsafe_allow_html=True)
            
            # Afficher visualisation
            st.markdown("---")
            st.markdown("### 📊 Visualisation")

            # Affiche la droite avec la bonne réponse pour comparaison
            st.write("**La bonne position était :**")
            st.markdown(afficher_fraction_droite(ex['numerateur'], ex['denominateur']), unsafe_allow_html=True)

            st.write(f"💡 **{ex['numerateur']}/{ex['denominateur']}** = {ex['valeur']:.2f}")
            st.write(f"📍 Tu as placé: {reponse:.2f}")
            st.write(f"📏 Distance: {distance:.2f}")
            
            st.markdown("---")
            
            # Bouton suivant
            if st.button("➡️ Exercice Suivant", key="frac_droite_next", use_container_width=True):
                # Reset complet
                st.session_state.fraction_droite = {
                    'exercice': None,
                    'feedback_affiche': False
                }
                st.rerun()
        
        # Afficher slider si pas encore validé
        else:
            # Slider
            reponse = st.slider(
                "Position estimée",
                min_value=0.0,
                max_value=1.0,
                step=0.05,
                value=0.5,
                key="frac_slider"
            )
            
            if st.button("✅ Vérifier", key="frac_verify_droite", use_container_width=True):
                distance = abs(reponse - ex['valeur'])
                
                # Score selon précision
                if distance <= 0.05:
                    score = 25
                elif distance <= 0.15:
                    score = 10
                else:
                    score = 0
                
                # Sauvegarder résultat
                frac_state['feedback_affiche'] = True
                frac_state['distance'] = distance
                frac_state['score'] = score
                frac_state['reponse'] = reponse
                
                # Mettre à jour stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if score > 0:
                    st.session_state.points += score
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                
                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('fractions', score > 0, difficulty=4)
                
                auto_save_profil(score > 0)
                st.rerun()
def decimaux_section():
    """
    Section Nombres Décimaux - CM1-CM2
    """
    from decimaux_utils import (
        generer_droite_decimale,
        generer_comparaison_decimaux,
        generer_addition_decimaux,
        generer_soustraction_decimaux,
        generer_multiplication_par_10_100,
        generer_fraction_vers_decimal,
        calculer_score_decimal,
        expliquer_comparaison_decimaux,
        expliquer_addition_decimaux
    )
    
    st.markdown('<div class="categorie-header">🔢 Nombres Décimaux</div>', unsafe_allow_html=True)
    
    # Réservé CM1-CM2
    if st.session_state.niveau in ["CE1", "CE2"]:
        st.info("📚 Les nombres décimaux commencent au CM1. Continue à t'entraîner sur les autres exercices !")
        return
    
    # Adapter modes selon niveau
    if st.session_state.niveau == "CM1":
        modes = ["Droite numérique", "Comparer", "Addition", "Soustraction", "Fraction → Décimal"]
    else:  # CM2
        modes = ["Droite numérique", "Comparer", "Addition", "Soustraction", "× ÷ par 10/100/1000", "Fraction → Décimal"]
    
    mode = st.radio("Choisis un exercice:", modes, horizontal=True, key="dec_mode")
    
    st.markdown("---")
    
    # ==========================================
    # DROITE NUMÉRIQUE
    # ==========================================
    if mode == "Droite numérique":
        st.subheader("📏 Place le nombre décimal")
        
        # Initialiser
        if 'dec_droite' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_droite = {
                'exercice': generer_droite_decimale(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_droite['exercice']
        
        st.write(f"### {ex['question']}")
        st.write(f"*De {ex['min']} à {ex['max']}*")
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_droite['feedback_affiche']:
            score = st.session_state.dec_droite['score']
            message = st.session_state.dec_droite['message']
            
            if score >= 20:
                st.markdown(f'<div class="feedback-success">🎉 {message}</div>', unsafe_allow_html=True)
                st.balloons()
            elif score > 0:
                st.markdown(f'<div class="feedback-success">👍 {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-error">❌ {message}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write(f"**Position correcte : {ex['nombre']}**")
            st.write(f"**Ta réponse : {st.session_state.dec_droite['reponse']}**")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Slider pour placer le nombre
        else:
            reponse = st.slider(
                "Position estimée",
                min_value=float(ex['min']),
                max_value=float(ex['max']),
                step=ex['precision'],
                value=float(ex['max']) / 2,
                key="dec_slider"
            )
            
            if st.button("✅ Vérifier", key="dec_verify", use_container_width=True):
                tolerance = (ex['max'] - ex['min']) * 0.05  # 5% de tolérance
                score, message = calculer_score_decimal(reponse, ex['nombre'], tolerance)
                
                st.session_state.dec_droite['score'] = score
                st.session_state.dec_droite['message'] = message
                st.session_state.dec_droite['reponse'] = reponse
                st.session_state.dec_droite['feedback_affiche'] = True
                
                # Stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if score > 0:
                    st.session_state.points += score
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                
                # Système adaptatif
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('decimaux', score > 0, difficulty=3)
                
                auto_save_profil(score > 0)
                st.rerun()
    
    # ==========================================
    # COMPARER DÉCIMAUX
    # ==========================================
    elif mode == "Comparer":
        st.subheader("⚖️ Compare les nombres décimaux")
        
        # Initialiser
        if 'dec_comparer' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_comparer = {
                'exercice': generer_comparaison_decimaux(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_comparer['exercice']
        
        st.write(f"### {ex['question']}")
        
        # Afficher les deux nombres côte à côte
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"<h1 style='text-align: center; color: #4A90E2;'>{ex['a']}</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h1 style='text-align: center;'>❓</h1>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<h1 style='text-align: center; color: #50C878;'>{ex['b']}</h1>", unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_comparer['feedback_affiche']:
            if st.session_state.dec_comparer['correct']:
                st.markdown('<div class="feedback-success">🎉 Bravo ! C\'est exact !</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, {ex["a"]} {ex["reponse"]} {ex["b"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.markdown(expliquer_comparaison_decimaux(ex['a'], ex['b']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Boutons de choix
        else:
            st.write("**Choisis le bon symbole :**")
            
            col1, col2, col3 = st.columns(3)
            symboles = ['<', '=', '\>'] # ✅ CORRECTION: Échapper le caractère '>'
            
            for idx, symbole in enumerate(symboles):
                col = [col1, col2, col3][idx]
                with col:
                    if st.button(symbole, key=f"dec_comp_{idx}", use_container_width=True):
                        correct = (symbole == ex['reponse'])
                        
                        st.session_state.dec_comparer['correct'] = correct
                        st.session_state.dec_comparer['feedback_affiche'] = True
                        
                        # Stats
                        st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                        if correct:
                            st.session_state.points += 15
                            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        
                        # Système adaptatif
                        if "profil" in st.session_state:
                            tracker = SkillTracker(st.session_state.profil)
                            tracker.record_exercise('decimaux', correct, difficulty=2)
                        
                        auto_save_profil(correct)
                        st.rerun()
    
    # ==========================================
    # ADDITION DÉCIMAUX
    # ==========================================
    elif mode == "Addition":
        st.subheader("➕ Addition de décimaux")
        
        # Initialiser
        if 'dec_addition' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_addition = {
                'exercice': generer_addition_decimaux(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_addition['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_addition['feedback_affiche']:
            if st.session_state.dec_addition['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! {ex["a"]} + {ex["b"]} = {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_addition_decimaux(ex['a'], ex['b'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_addition_decimaux(ex['a'], ex['b'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Résultat:", min_value=0.0, max_value=200.0, step=0.1, format="%.2f", key="dec_add_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="dec_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.01)  # Tolérance 0.01
                    
                    st.session_state.dec_addition['correct'] = correct
                    st.session_state.dec_addition['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 20
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('decimaux', correct, difficulty=3)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # SOUSTRACTION DÉCIMAUX
    # ==========================================
    elif mode == "Soustraction":
        st.subheader("➖ Soustraction de décimaux")
        
        # Initialiser
        if 'dec_soustraction' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_soustraction = {
                'exercice': generer_soustraction_decimaux(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_soustraction['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_soustraction['feedback_affiche']:
            if st.session_state.dec_soustraction['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! {ex["a"]} - {ex["b"]} = {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write("### 💡 Méthode")
            st.write("Aligne les virgules et soustrais normalement !")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Résultat:", min_value=0.0, max_value=200.0, step=0.1, format="%.2f", key="dec_sub_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="dec_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.01)  # Tolérance 0.01
                    
                    st.session_state.dec_soustraction['correct'] = correct
                    st.session_state.dec_soustraction['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 20
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('decimaux', correct, difficulty=3)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # MULTIPLICATION/DIVISION PAR 10/100/1000 (CM2)
    # ==========================================
    elif mode == "× ÷ par 10/100/1000":
        st.subheader("🔢 Multiplier/Diviser par 10, 100, 1000")
        
        # Initialiser
        if 'dec_mult10' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_mult10 = {
                'exercice': generer_multiplication_par_10_100(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_mult10['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_mult10['feedback_affiche']:
            if st.session_state.dec_mult10['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Parfait ! La réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write("### 💡 Règle")
            
            if ex['operation'] == 'multiplication':
                nb_zeros = len(str(ex['multiplicateur'])) - 1
                st.write(f"**Multiplier par {ex['multiplicateur']}** = déplacer la virgule de **{nb_zeros} rangs vers la DROITE**")
                st.write(f"Exemple : {ex['nombre']} → {ex['reponse']}")
            else:
                nb_zeros = len(str(ex['multiplicateur'])) - 1
                st.write(f"**Diviser par {ex['multiplicateur']}** = déplacer la virgule de **{nb_zeros} rangs vers la GAUCHE**")
                st.write(f"Exemple : {ex['nombre']} → {ex['reponse']}")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Résultat:", min_value=0.0, max_value=100000.0, step=0.001, format="%.3f", key="dec_mult10_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="dec_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.001)
                    
                    st.session_state.dec_mult10['correct'] = correct
                    st.session_state.dec_mult10['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 25
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('decimaux', correct, difficulty=4)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # FRACTION → DÉCIMAL
    # ==========================================
    elif mode == "Fraction → Décimal":
        st.subheader("🔄 Convertir fraction en décimal")
        
        # Initialiser
        if 'dec_fraction' not in st.session_state or st.session_state.get('dec_reset', False):
            st.session_state.dec_fraction = {
                'exercice': generer_fraction_vers_decimal(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.dec_reset = False
        
        ex = st.session_state.dec_fraction['exercice']
        
        # Afficher la fraction
        st.markdown(f"""
        <div style='text-align: center; font-size: 48px; margin: 30px 0;'>
            <div style='border-bottom: 3px solid #333; display: inline-block; padding: 0 20px;'>
                {ex['numerateur']}
            </div>
            <div style='padding: 10px 20px;'>
                {ex['denominateur']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### {ex['question']}")
        
        # Afficher feedback si déjà répondu
        if st.session_state.dec_fraction['feedback_affiche']:
            if st.session_state.dec_fraction['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! {ex["numerateur"]}/{ex["denominateur"]} = {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, {ex["numerateur"]}/{ex["denominateur"]} = {ex["reponse"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write("### 💡 Méthode")
            st.write(f"**{ex['numerateur']} ÷ {ex['denominateur']} = {ex['reponse']}**")
            
            if ex['denominateur'] == 10:
                st.write("✨ **Astuce** : Diviser par 10 = déplacer la virgule de 1 rang vers la gauche")
            elif ex['denominateur'] == 100:
                st.write("✨ **Astuce** : Diviser par 100 = déplacer la virgule de 2 rangs vers la gauche")
            elif ex['denominateur'] in [2, 4, 5]:
                st.write(f"✨ **Astuce** : {ex['numerateur']} ÷ {ex['denominateur']} = {ex['reponse']}")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="dec_next", use_container_width=True):
                st.session_state.dec_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Nombre décimal:", min_value=0.0, max_value=10.0, step=0.01, format="%.2f", key="dec_frac_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="dec_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.01)
                    
                    st.session_state.dec_fraction['correct'] = correct
                    st.session_state.dec_fraction['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 20
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('decimaux', correct, difficulty=3)
                    
                    auto_save_profil(correct)
                    st.rerun()
def proportionnalite_section():
    """
    Section Proportionnalité - CM1-CM2
    """
    from proportionnalite_utils import (
        generer_tableau_proportionnalite,
        generer_regle_de_trois,
        generer_pourcentage_simple,
        generer_echelle,
        generer_vitesse,
        expliquer_regle_de_trois,
        expliquer_pourcentage
    )
    
    st.markdown('<div class="categorie-header">⚖️ Proportionnalité</div>', unsafe_allow_html=True)
    
    # Réservé CM1-CM2
    if st.session_state.niveau in ["CE1", "CE2"]:
        st.info("📚 La proportionnalité commence au CM1. Continue à progresser !")
        return
    
    # Adapter modes selon niveau
    if st.session_state.niveau == "CM1":
        modes = ["Tableaux", "Règle de trois"]
    else:  # CM2
        modes = ["Tableaux", "Règle de trois", "Pourcentages", "Échelles", "Vitesse"]
    
    mode = st.radio("Choisis un exercice:", modes, horizontal=True, key="prop_mode")
    
    st.markdown("---")
    
    # ==========================================
    # TABLEAUX DE PROPORTIONNALITÉ
    # ==========================================
    if mode == "Tableaux":
        st.subheader("📊 Complète le tableau")
        
        # Initialiser
        if 'prop_tableau' not in st.session_state or st.session_state.get('prop_reset', False):
            st.session_state.prop_tableau = {
                'exercice': generer_tableau_proportionnalite(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.prop_reset = False
        
        ex = st.session_state.prop_tableau['exercice']
        
        # Afficher tableau
        st.write("**Tableau de proportionnalité :**")
        
        # Créer tableau HTML
        html_table = "<table style='width:100%; text-align:center; font-size:20px; border-collapse: collapse;'>"
        html_table += "<tr style='background-color: #4A90E2; color: white;'>"
        for val in ex['ligne1']:
            html_table += f"<th style='padding: 15px; border: 2px solid #333;'>{val}</th>"
        html_table += "</tr>"
        html_table += "<tr style='background-color: #50C878; color: white;'>"
        for idx, val in enumerate(ex['ligne2']):
            if idx == ex['index_manquant']:
                html_table += f"<td style='padding: 15px; border: 2px solid #333; background-color: #FFD93D; color: #333;'>❓</td>"
            else:
                html_table += f"<td style='padding: 15px; border: 2px solid #333;'>{val}</td>"
        html_table += "</tr>"
        html_table += "</table>"
        
        st.markdown(html_table, unsafe_allow_html=True)
        
        st.write(f"### {ex['question']}")
        
        # Afficher feedback si déjà répondu
        if st.session_state.prop_tableau['feedback_affiche']:
            if st.session_state.prop_tableau['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! La réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.write("### 💡 Méthode")
                st.write(f"**Coefficient de proportionnalité** : ×{ex['coefficient']}")
                st.write(f"{ex['ligne1'][ex['index_manquant']]} × {ex['coefficient']} = **{ex['reponse']}**")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.write("### 📚 Rappel")
                st.write(f"Dans un tableau de proportionnalité, on multiplie toujours par le **même coefficient**")
                st.write(f"Ici : {ex['ligne1'][0]} × {ex['coefficient']} = {ex['ligne2'][0]}")
                st.write(f"Donc : {ex['ligne1'][ex['index_manquant']]} × {ex['coefficient']} = **{ex['reponse']}**")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="prop_next", use_container_width=True):
                st.session_state.prop_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Valeur manquante:", min_value=0, max_value=1000, key="prop_tab_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="prop_verify", use_container_width=True):
                    correct = (reponse == ex['reponse'])
                    
                    st.session_state.prop_tableau['correct'] = correct
                    st.session_state.prop_tableau['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 20
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('proportionnalite', correct, difficulty=3)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # RÈGLE DE TROIS
    # ==========================================
    elif mode == "Règle de trois":
        st.subheader("🧮 Problème de proportionnalité")
        
        # Initialiser
        if 'prop_regle3' not in st.session_state or st.session_state.get('prop_reset', False):
            st.session_state.prop_regle3 = {
                'exercice': generer_regle_de_trois(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.prop_reset = False
        
        ex = st.session_state.prop_regle3['exercice']
        # Afficher problème
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.prop_regle3['feedback_affiche']:
            if st.session_state.prop_regle3['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Parfait ! La réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_regle_de_trois(ex['qte1'], ex['valeur1'], ex['qte2'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_regle_de_trois(ex['qte1'], ex['valeur1'], ex['qte2'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="prop_next", use_container_width=True):
                st.session_state.prop_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Réponse:", min_value=0.0, max_value=10000.0, step=0.1, format="%.2f", key="prop_r3_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="prop_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.1)
                    
                    st.session_state.prop_regle3['correct'] = correct
                    st.session_state.prop_regle3['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 25
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('proportionnalite', correct, difficulty=4)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # POURCENTAGES (CM2)
    # ==========================================
    elif mode == "Pourcentages":
        st.subheader("💯 Calculs de pourcentages")
        
        # Initialiser
        if 'prop_pourcent' not in st.session_state or st.session_state.get('prop_reset', False):
            st.session_state.prop_pourcent = {
                'exercice': generer_pourcentage_simple(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.prop_reset = False
        
        ex = st.session_state.prop_pourcent['exercice']
        
        # Afficher contexte
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["contexte"]}</h3></div>', unsafe_allow_html=True)
        
        st.write(f"### {ex['question']}")
        
        # Afficher feedback si déjà répondu
        if st.session_state.prop_pourcent['feedback_affiche']:
            if st.session_state.prop_pourcent['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! {ex["pourcentage"]}% de {ex["nombre"]} = {ex["reponse"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_pourcentage(ex['nombre'], ex['pourcentage'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_pourcentage(ex['nombre'], ex['pourcentage'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="prop_next", use_container_width=True):
                st.session_state.prop_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input("Résultat:", min_value=0.0, max_value=1000.0, step=0.5, key="prop_pct_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="prop_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.5)
                    
                    st.session_state.prop_pourcent['correct'] = correct
                    st.session_state.prop_pourcent['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 25
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('proportionnalite', correct, difficulty=4)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # ÉCHELLES (CM2)
    # ==========================================
    elif mode == "Échelles":
        st.subheader("🗺️ Problèmes d'échelles")
        
        # Initialiser
        if 'prop_echelle' not in st.session_state or st.session_state.get('prop_reset', False):
            st.session_state.prop_echelle = {
                'exercice': generer_echelle(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.prop_reset = False
        
        ex = st.session_state.prop_echelle['exercice']
        
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        st.info(f"📏 Échelle : {ex['echelle']} ({ex['description']})")
        
        # Afficher feedback si déjà répondu
        if st.session_state.prop_echelle['feedback_affiche']:
            if st.session_state.prop_echelle['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! La réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write("### 💡 Méthode")
            st.write(f"Avec l'échelle {ex['echelle']} :")
            st.write(f"- 1 cm sur le plan = {ex['echelle'].split('/')[1]} cm en réalité")
            st.write(f"- Il faut multiplier ou diviser selon le sens de la conversion")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="prop_next", use_container_width=True):
                st.session_state.prop_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite']}):", min_value=0.0, max_value=100000.0, step=1.0, key="prop_ech_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="prop_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.5)
                    
                    st.session_state.prop_echelle['correct'] = correct
                    st.session_state.prop_echelle['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 30
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('proportionnalite', correct, difficulty=5)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # VITESSE (CM2)
    # ==========================================
    elif mode == "Vitesse":
        st.subheader("🚗 Vitesse, distance, temps")
        
        # Initialiser
        if 'prop_vitesse' not in st.session_state or st.session_state.get('prop_reset', False):
            st.session_state.prop_vitesse = {
                'exercice': generer_vitesse(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.prop_reset = False
        
        ex = st.session_state.prop_vitesse['exercice']
        
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.prop_vitesse['feedback_affiche']:
            if st.session_state.prop_vitesse['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! La réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
            
            st.write("---")
            st.write("### 💡 Formules")
            st.write("**Distance = Vitesse × Temps**")
            st.write("**Temps = Distance ÷ Vitesse**")
            st.write("**Vitesse = Distance ÷ Temps**")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="prop_next", use_container_width=True):
                st.session_state.prop_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite']}):", min_value=0, max_value=1000, key="prop_vit_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="prop_verify", use_container_width=True):
                    correct = (reponse == ex['reponse'])
                    
                    st.session_state.prop_vitesse['correct'] = correct
                    st.session_state.prop_vitesse['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 30
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('proportionnalite', correct, difficulty=5)
                    
                    auto_save_profil(correct)
                    st.rerun()
def geometrie_section():
    """
    Section Géométrie - CE1 à CM2
    """
    from geometrie_utils import (
        generer_reconnaissance_forme, 
        generer_perimetre, 
        generer_aire, 
        generer_angle,
        dessiner_forme_svg,
        dessiner_angle_svg
    )
    
    st.markdown('<div class="categorie-header">📐 Géométrie</div>', unsafe_allow_html=True)
    
    # Adapter selon niveau
    if st.session_state.niveau == "CE1":
        modes = ["Reconnaissance"]
    elif st.session_state.niveau == "CE2":
        modes = ["Reconnaissance", "Périmètre"]
    elif st.session_state.niveau == "CM1":
        modes = ["Reconnaissance", "Périmètre", "Aire"]
    else:  # CM2
        modes = ["Reconnaissance", "Périmètre", "Aire", "Angles"]
    
    mode = st.radio("Choisis un exercice:", modes, horizontal=True, key="geo_mode")
    
    st.markdown("---")
    
    # ==========================================
    # RECONNAISSANCE DE FORMES
    # ==========================================
    if mode == "Reconnaissance":
        st.subheader("🔍 Reconnais la forme")
        
        # Initialiser exercice
        if 'geo_reconnaissance' not in st.session_state or st.session_state.get('geo_reset', False):
            st.session_state.geo_reconnaissance = {
                'exercice': generer_reconnaissance_forme(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.geo_reset = False
        
        ex = st.session_state.geo_reconnaissance['exercice']
        forme = ex['forme']
        
        # Afficher forme
        st.markdown(dessiner_forme_svg(forme['nom'], forme, 300), unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.geo_reconnaissance['feedback_affiche']:
            if st.session_state.geo_reconnaissance['correct']:
                st.markdown('<div class="feedback-success">🎉 Exact ! C\'est bien un(e) ' + forme['nom'] + ' !</div>', unsafe_allow_html=True)
                st.balloons()
                
                # Info pédagogique
                if forme['nom'] != "Cercle":
                    st.info(f"ℹ️ Un(e) {forme['nom']} a **{forme['cotes']} côtés** et **{forme['sommets']} sommets**")
                else:
                    st.info(f"ℹ️ Le cercle n'a ni côtés ni sommets, c'est une ligne courbe fermée")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, c\'est un(e) {forme["nom"]}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="geo_next", use_container_width=True):
                st.session_state.geo_reset = True
                st.rerun()
        
        # Afficher options si pas encore répondu
        else:
            st.write("**Quelle est cette forme ?**")
            
            cols = st.columns(2)
            for idx, option in enumerate(ex['options']):
                col = cols[idx % 2]
                with col:
                    if st.button(option, key=f"geo_opt_{idx}", use_container_width=True):
                        correct = (option == forme['nom'])
                        
                        st.session_state.geo_reconnaissance['correct'] = correct
                        st.session_state.geo_reconnaissance['feedback_affiche'] = True
                        
                        # Stats
                        st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                        if correct:
                            st.session_state.points += 15
                            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        
                        # Système adaptatif
                        if "profil" in st.session_state:
                            tracker = SkillTracker(st.session_state.profil)
                            tracker.record_exercise('geometrie', correct, difficulty=2)
                        
                        auto_save_profil(correct)
                        st.rerun()
    
    # ==========================================
    # PÉRIMÈTRES
    # ==========================================
    elif mode == "Périmètre":
        st.subheader("📏 Calcule le périmètre")
        
        # Initialiser exercice
        if 'geo_perimetre' not in st.session_state or st.session_state.get('geo_reset', False):
            st.session_state.geo_perimetre = {
                'exercice': generer_perimetre(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.geo_reset = False
        
        ex = st.session_state.geo_perimetre['exercice']
        
        # Afficher forme
        forme_nom = ex['type'].capitalize()
        if forme_nom == "Carre":
            forme_nom = "Carré"
        
        st.markdown(dessiner_forme_svg(forme_nom, ex['dimensions'], 300), unsafe_allow_html=True)
        
        st.markdown("---")
        st.write(f"**{ex['question']}**")
        
        # Afficher feedback si déjà répondu
        if st.session_state.geo_perimetre['feedback_affiche']:
            if st.session_state.geo_perimetre['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! Le périmètre est bien {ex["reponse"]} cm</div>', unsafe_allow_html=True)
                st.balloons()
                
                # Explication formule
                st.write("---")
                st.write("### 💡 Méthode")
                st.write(f"**Formule:** {ex['formule']} = {ex['reponse']} cm")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse était {ex["reponse"]} cm</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.write("### 📚 Rappel")
                if ex['type'] == 'carre':
                    st.write("**Périmètre du carré** = 4 × côté")
                elif ex['type'] == 'rectangle':
                    st.write("**Périmètre du rectangle** = 2 × (longueur + largeur)")
                else:
                    st.write("**Périmètre du triangle** = côté1 + côté2 + côté3")
                
                st.write(f"**Calcul:** {ex['formule']} = {ex['reponse']} cm")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="geo_next", use_container_width=True):
                st.session_state.geo_reset = True
                st.rerun()
        
        # Input réponse
        else:
            reponse = st.number_input("Périmètre (en cm):", min_value=0, max_value=500, key="geo_perim_input")
            
            if st.button("✅ Vérifier", key="geo_verify", use_container_width=True):
                correct = (reponse == ex['reponse'])
                
                st.session_state.geo_perimetre['correct'] = correct
                st.session_state.geo_perimetre['feedback_affiche'] = True
                
                # Stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if correct:
                    st.session_state.points += 20
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                
                # Système adaptatif
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('geometrie', correct, difficulty=3)
                
                auto_save_profil(correct)
                st.rerun()
    
    # ==========================================
    # AIRES
    # ==========================================
    elif mode == "Aire":
        st.subheader("📦 Calcule l'aire")
        
        # Initialiser exercice
        if 'geo_aire' not in st.session_state or st.session_state.get('geo_reset', False):
            st.session_state.geo_aire = {
                'exercice': generer_aire(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.geo_reset = False
        
        ex = st.session_state.geo_aire['exercice']
        
        # Afficher forme
        forme_nom = ex['type'].capitalize()
        if forme_nom == "Carre":
            forme_nom = "Carré"
        
        st.markdown(dessiner_forme_svg(forme_nom, ex['dimensions'], 300), unsafe_allow_html=True)
        
        st.markdown("---")
        st.write(f"**{ex['question']}**")
        
        # Afficher feedback si déjà répondu
        if st.session_state.geo_aire['feedback_affiche']:
            if st.session_state.geo_aire['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! L\'aire est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.write("### 💡 Méthode")
                st.write(f"**Formule:** {ex['formule']} = {ex['reponse']} {ex['unite']}")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, l\'aire est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.write("### 📚 Rappel")
                if ex['type'] == 'carre':
                    st.write("**Aire du carré** = côté × côté")
                elif ex['type'] == 'rectangle':
                    st.write("**Aire du rectangle** = longueur × largeur")
                else:
                    st.write("**Aire du triangle** = (base × hauteur) ÷ 2")
                
                st.write(f"**Calcul:** {ex['formule']} = {ex['reponse']} {ex['unite']}")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="geo_next", use_container_width=True):
                st.session_state.geo_reset = True
                st.rerun()
        # Input réponse
        else:
            reponse = st.number_input(f"Aire (en {ex['unite']}):", min_value=0, max_value=1000, key="geo_aire_input")
            
            if st.button("✅ Vérifier", key="geo_verify", use_container_width=True):
                correct = (reponse == ex['reponse'])
                
                st.session_state.geo_aire['correct'] = correct
                st.session_state.geo_aire['feedback_affiche'] = True
                
                # Stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if correct:
                    st.session_state.points += 25
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                
                # Système adaptatif
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('geometrie', correct, difficulty=4)
                
                auto_save_profil(correct)
                st.rerun()
    
    # ==========================================
    # ANGLES (CM2)
    # ==========================================
    elif mode == "Angles":
        st.subheader("📐 Reconnais le type d'angle")
        
        # Initialiser exercice
        if 'geo_angles' not in st.session_state or st.session_state.get('geo_reset', False):
            st.session_state.geo_angles = {
                'exercice': generer_angle(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.geo_reset = False
        
        ex = st.session_state.geo_angles['exercice']
        angle = ex['angle']
        
        # Afficher angle
        st.markdown(dessiner_angle_svg(angle['mesure'], 300), unsafe_allow_html=True)
        
        st.markdown("---")
        st.write(f"**{ex['question']}**")
        
        # Afficher feedback si déjà répondu
        if st.session_state.geo_angles['feedback_affiche']:
            if st.session_state.geo_angles['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! C\'est bien un {angle["nom"]} !</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.write("### 💡 Rappel")
                if angle['type'] == 'droit':
                    st.write("**Angle droit** = exactement 90°")
                elif angle['type'] == 'aigu':
                    st.write("**Angle aigu** = moins de 90°")
                elif angle['type'] == 'obtus':
                    st.write("**Angle obtus** = entre 90° et 180°")
                else:
                    st.write("**Angle plat** = exactement 180°")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, c\'est un {angle["nom"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.write("### 📚 Les types d'angles")
                st.write("- **Angle aigu** : moins de 90°")
                st.write("- **Angle droit** : exactement 90°")
                st.write("- **Angle obtus** : entre 90° et 180°")
                st.write("- **Angle plat** : exactement 180°")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="geo_next", use_container_width=True):
                st.session_state.geo_reset = True
                st.rerun()
        
        # Options de réponse
        else:
            cols = st.columns(2)
            for idx, option in enumerate(ex['options']):
                col = cols[idx % 2]
                with col:
                    if st.button(option, key=f"geo_angle_{idx}", use_container_width=True):
                        correct = (option == ex['reponse'])
                        
                        st.session_state.geo_angles['correct'] = correct
                        st.session_state.geo_angles['feedback_affiche'] = True
                        
                        # Stats
                        st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                        if correct:
                            st.session_state.points += 20
                            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        
                        # Système adaptatif
                        if "profil" in st.session_state:
                            tracker = SkillTracker(st.session_state.profil)
                            tracker.record_exercise('geometrie', correct, difficulty=3)
                        
                        auto_save_profil(correct)
                        st.rerun()
def mesures_section():
    """
    Section Mesures et Conversions - CE1-CM2
    """
    from mesures_utils import (
        generer_conversion_longueur,
        generer_conversion_masse,
        generer_conversion_capacite,
        generer_probleme_duree,
        expliquer_conversion
    )
    
    st.markdown('<div class="categorie-header">📏 Mesures et Conversions</div>', unsafe_allow_html=True)
    
    # Adapter modes selon niveau
    if st.session_state.niveau == "CE1":
        modes = ["Longueurs (cm ↔ m)", "Durées"]
    elif st.session_state.niveau == "CE2":
        modes = ["Longueurs", "Masses (g ↔ kg)", "Capacités", "Durées"]
    elif st.session_state.niveau == "CM1":
        modes = ["Longueurs", "Masses", "Capacités", "Durées"]
    else:  # CM2
        modes = ["Longueurs", "Masses", "Capacités", "Durées"]
    
    mode = st.radio("Choisis un exercice:", modes, horizontal=True, key="mes_mode")
    
    st.markdown("---")
    
    # ==========================================
    # CONVERSIONS LONGUEURS
    # ==========================================
    if mode in ["Longueurs (cm ↔ m)", "Longueurs"]:
        st.subheader("📏 Conversions de longueurs")
        
        # Initialiser
        if 'mes_longueur' not in st.session_state or st.session_state.get('mes_reset', False):
            st.session_state.mes_longueur = {
                'exercice': generer_conversion_longueur(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.mes_reset = False
        
        ex = st.session_state.mes_longueur['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.mes_longueur['feedback_affiche']:
            if st.session_state.mes_longueur['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Parfait ! {ex["valeur_depart"]} {ex["unite_depart"]} = {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="mes_next", use_container_width=True):
                st.session_state.mes_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite_arrivee']}):", min_value=0.0, max_value=100000.0, step=0.1, key="mes_long_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="mes_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.1)
                    
                    st.session_state.mes_longueur['correct'] = correct
                    st.session_state.mes_longueur['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 15
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('mesures', correct, difficulty=2)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # CONVERSIONS MASSES
    # ==========================================
    elif mode in ["Masses (g ↔ kg)", "Masses"]:
        st.subheader("⚖️ Conversions de masses")
        
        # Initialiser
        if 'mes_masse' not in st.session_state or st.session_state.get('mes_reset', False):
            st.session_state.mes_masse = {
                'exercice': generer_conversion_masse(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.mes_reset = False
        
        ex = st.session_state.mes_masse['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.mes_masse['feedback_affiche']:
            if st.session_state.mes_masse['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! {ex["valeur_depart"]} {ex["unite_depart"]} = {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="mes_next", use_container_width=True):
                st.session_state.mes_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite_arrivee']}):", min_value=0.0, max_value=100000.0, step=0.1, key="mes_mass_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="mes_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.1)
                    
                    st.session_state.mes_masse['correct'] = correct
                    st.session_state.mes_masse['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 15
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('mesures', correct, difficulty=2)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # CONVERSIONS CAPACITÉS
    # ==========================================
    elif mode == "Capacités":
        st.subheader("🥤 Conversions de capacités")
        
        # Initialiser
        if 'mes_capacite' not in st.session_state or st.session_state.get('mes_reset', False):
            exercice_gen = generer_conversion_capacite(st.session_state.niveau)
            if exercice_gen is None:
                st.info("📚 Les capacités commencent au CE2 !")
                return
            
            st.session_state.mes_capacite = {
                'exercice': exercice_gen,
                'feedback_affiche': False
            }
            st.session_state.mes_reset = False
        
        ex = st.session_state.mes_capacite['exercice']
        
        st.markdown(f'<div class="exercice-box">{ex["question"]}</div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.mes_capacite['feedback_affiche']:
            if st.session_state.mes_capacite['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Bravo ! {ex["valeur_depart"]} {ex["unite_depart"]} = {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite_arrivee"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.markdown(expliquer_conversion(ex['valeur_depart'], ex['unite_depart'], ex['unite_arrivee'], ex['reponse']))
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="mes_next", use_container_width=True):
                st.session_state.mes_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite_arrivee']}):", min_value=0.0, max_value=100000.0, step=0.1, key="mes_cap_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="mes_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.1)
                    
                    st.session_state.mes_capacite['correct'] = correct
                    st.session_state.mes_capacite['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 15
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('mesures', correct, difficulty=2)
                    
                    auto_save_profil(correct)
                    st.rerun()
    
    # ==========================================
    # DURÉES
    # ==========================================
    elif mode == "Durées":
        st.subheader("⏰ Calculs de durées")
        
        # Initialiser
        if 'mes_duree' not in st.session_state or st.session_state.get('mes_reset', False):
            st.session_state.mes_duree = {
                'exercice': generer_probleme_duree(st.session_state.niveau),
                'feedback_affiche': False
            }
            st.session_state.mes_reset = False
        
        ex = st.session_state.mes_duree['exercice']
        
        st.markdown(f'<div class="aller-loin-box"><h3>{ex["question"]}</h3></div>', unsafe_allow_html=True)
        
        # Afficher feedback si déjà répondu
        if st.session_state.mes_duree['feedback_affiche']:
            if st.session_state.mes_duree['correct']:
                st.markdown(f'<div class="feedback-success">🎉 Exact ! La réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.write("---")
                st.write("### 💡 Méthode")
                if ex['type'] == 'simple':
                    st.write("Pour calculer une durée, on soustrait l'heure de début de l'heure de fin")
                elif ex['type'] == 'avec_min':
                    st.write("Calcule le nombre total de minutes entre les deux heures")
                else:  # conversion
                    if ex['unite'] == 'min':
                        st.write("**1 heure = 60 minutes**")
                        st.write("Pour passer d'heures en minutes, on multiplie par 60")
                    else:
                        st.write("**60 minutes = 1 heure**")
                        st.write("Pour passer de minutes en heures, on divise par 60")
            else:
                st.markdown(f'<div class="feedback-error">❌ Non, la réponse est {ex["reponse"]} {ex["unite"]}</div>', unsafe_allow_html=True)
                
                st.write("---")
                st.write("### 📚 Rappel")
                st.write("**1 heure = 60 minutes**")
                if ex['type'] == 'conversion':
                    if ex['unite'] == 'min':
                        st.write("Pour convertir heures → minutes : **multiplier par 60**")
                    else:
                        st.write("Pour convertir minutes → heures : **diviser par 60**")
            
            st.markdown("---")
            if st.button("➡️ Exercice Suivant", key="mes_next", use_container_width=True):
                st.session_state.mes_reset = True
                st.rerun()
        
        # Input réponse
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                reponse = st.number_input(f"Réponse (en {ex['unite']}):", min_value=0.0, max_value=1000.0, step=1.0 if ex['unite'] == 'min' else 0.5, key="mes_dur_input")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Vérifier", key="mes_verify", use_container_width=True):
                    correct = (abs(reponse - ex['reponse']) < 0.5)
                    
                    st.session_state.mes_duree['correct'] = correct
                    st.session_state.mes_duree['feedback_affiche'] = True
                    
                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.points += 20
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    
                    # Système adaptatif
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('mesures', correct, difficulty=3)
                    
                    auto_save_profil(correct)
                    st.rerun()

# ============================================
# 💰 MONNAIE - Apprendre à rendre la monnaie
# ============================================

def monnaie_section():
    """
    Section pour apprendre à rendre la monnaie (CE1-CM2)
    SANS DÉCIMAUX - utilise euros et centimes séparés
    """
    st.markdown('<div class="categorie-header">💰 Rendre la Monnaie</div>', unsafe_allow_html=True)

    st.info("💡 Apprends à calculer le rendu de monnaie sans te tromper !")

    # Choix du type d'exercice
    types_exercices = {
        "CE1": ["Calcul simple", "Problème réaliste"],
        "CE2": ["Calcul simple", "Composer la monnaie", "Problème réaliste"],
        "CM1": ["Calcul simple", "Composer la monnaie", "Problème réaliste"],
        "CM2": ["Calcul simple", "Composer la monnaie", "Problème réaliste"]
    }

    niveau = st.session_state.get('niveau', 'CE2')
    types_dispo = types_exercices.get(niveau, types_exercices["CE2"])

    type_exercice = st.radio(
        "Choisis ton exercice :",
        types_dispo,
        horizontal=True,
        key="monnaie_type"
    )

    st.markdown("---")

    # ========= CALCUL SIMPLE =========
    if type_exercice == "Calcul simple":
        st.subheader("🧮 Calcul du rendu de monnaie")

        # Générer ou récupérer exercice
        if 'monnaie_exercice' not in st.session_state or st.session_state.get('monnaie_nouveau', False):
            st.session_state.monnaie_exercice = generer_calcul_rendu(niveau)
            st.session_state.monnaie_feedback = False
            st.session_state.monnaie_nouveau = False

        ex = st.session_state.monnaie_exercice

        # Affichage de la question
        st.markdown(f"### {ex['question']}")

        st.info(f"💸 **Prix :** {ex['prix_texte']}\n\n💵 **Tu payes avec :** {ex['paye_texte']}")

        if not st.session_state.get('monnaie_feedback', False):
            # Saisie de la réponse (en euros et centimes séparés)
            col1, col2 = st.columns(2)
            with col1:
                euros_reponse = st.number_input("Euros à rendre :", min_value=0, max_value=50, value=0, key="mon_euros")
            with col2:
                centimes_reponse = st.number_input("Centimes à rendre :", min_value=0, max_value=99, value=0, key="mon_cents")

            if st.button("✅ Vérifier", key="mon_verify", use_container_width=True):
                reponse_totale = euros_reponse * 100 + centimes_reponse
                correct = (reponse_totale == ex['reponse_centimes'])

                st.session_state.monnaie_correct = correct
                st.session_state.monnaie_reponse = reponse_totale
                st.session_state.monnaie_feedback = True

                # Stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if correct:
                    st.session_state.points += 20
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1

                # Système adaptatif
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('monnaie', correct, difficulty=3)

                auto_save_profil(correct)
                st.rerun()

        else:
            # Afficher feedback
            if st.session_state.monnaie_correct:
                st.success("🎉 Bravo ! C'est la bonne réponse !")
                st.balloons()
            else:
                st.error(f"❌ Pas tout à fait ! La bonne réponse était : {ex['reponse_texte']}")

                # Explication détaillée
                st.markdown("---")
                explication = expliquer_calcul_rendu(
                    ex['prix_centimes'],
                    ex['paye_centimes'],
                    ex['reponse_centimes']
                )
                st.markdown(explication)

            # Bouton suivant
            if st.button("➡️ Exercice suivant", key="mon_next", use_container_width=True):
                st.session_state.monnaie_nouveau = True
                st.session_state.monnaie_feedback = False
                st.rerun()

    # ========= COMPOSER LA MONNAIE =========
    elif type_exercice == "Composer la monnaie":
        st.subheader("💵 Composer le montant avec pièces et billets")

        # Générer ou récupérer exercice
        if 'monnaie_compo_ex' not in st.session_state or st.session_state.get('monnaie_compo_nouveau', False):
            st.session_state.monnaie_compo_ex = generer_composition_monnaie(niveau)
            st.session_state.monnaie_compo_feedback = False
            st.session_state.monnaie_compo_nouveau = False

        ex = st.session_state.monnaie_compo_ex

        st.markdown(f"### {ex['question']}")

        # Afficher le montant à composer bien visible
        st.info(f"🎯 **Montant à composer : {ex['montant_texte']}**")

        if not st.session_state.get('monnaie_compo_feedback', False):
            st.markdown("💡 Choisis les billets et pièces pour composer ce montant :")

            # Interface de sélection des pièces/billets
            st.markdown("#### 💶 Billets")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                billets_50 = st.number_input("Billets de 50€", min_value=0, max_value=10, value=0, key="b50")
            with col2:
                billets_20 = st.number_input("Billets de 20€", min_value=0, max_value=10, value=0, key="b20")
            with col3:
                billets_10 = st.number_input("Billets de 10€", min_value=0, max_value=10, value=0, key="b10")
            with col4:
                billets_5 = st.number_input("Billets de 5€", min_value=0, max_value=10, value=0, key="b5")

            st.markdown("#### 🪙 Pièces (euros)")
            col1, col2 = st.columns(2)
            with col1:
                pieces_2e = st.number_input("Pièces de 2€", min_value=0, max_value=20, value=0, key="p2e")
            with col2:
                pieces_1e = st.number_input("Pièces de 1€", min_value=0, max_value=20, value=0, key="p1e")

            st.markdown("#### 🪙 Pièces (centimes)")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                pieces_50c = st.number_input("50c", min_value=0, max_value=20, value=0, key="p50c")
            with col2:
                pieces_20c = st.number_input("20c", min_value=0, max_value=20, value=0, key="p20c")
            with col3:
                pieces_10c = st.number_input("10c", min_value=0, max_value=20, value=0, key="p10c")
            with col4:
                pieces_5c = st.number_input("5c", min_value=0, max_value=20, value=0, key="p5c")
            with col5:
                pieces_2c = st.number_input("2c", min_value=0, max_value=20, value=0, key="p2c")

            pieces_1c = st.number_input("Pièces de 1 centime", min_value=0, max_value=20, value=0, key="p1c")

            # Calcul du total proposé par l'élève
            total_propose = (billets_50 * 5000 + billets_20 * 2000 + billets_10 * 1000 + billets_5 * 500 +
                           pieces_2e * 200 + pieces_1e * 100 + pieces_50c * 50 + pieces_20c * 20 +
                           pieces_10c * 10 + pieces_5c * 5 + pieces_2c * 2 + pieces_1c * 1)

            # Afficher le total en temps réel
            from monnaie_utils import centimes_vers_euros_texte
            st.markdown(f"**Ton total actuel : {centimes_vers_euros_texte(total_propose)}**")

            # Boutons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Vérifier ma réponse", key="mon_compo_verify", use_container_width=True):
                    correct = (total_propose == ex['montant_centimes'])

                    # Compter le nombre de pièces utilisées
                    nb_pieces_eleve = (billets_50 + billets_20 + billets_10 + billets_5 + pieces_2e +
                                      pieces_1e + pieces_50c + pieces_20c + pieces_10c + pieces_5c +
                                      pieces_2c + pieces_1c)
                    nb_pieces_optimal = sum(q for _, _, q in ex['composition'])

                    st.session_state.monnaie_compo_correct = correct
                    st.session_state.monnaie_compo_optimal = (nb_pieces_eleve == nb_pieces_optimal)
                    st.session_state.monnaie_compo_feedback = True

                    # Stats
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                    if correct:
                        st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                        points_gagnes = 15 if nb_pieces_eleve == nb_pieces_optimal else 10
                        st.session_state.points += points_gagnes
                    auto_save_profil(correct)
                    st.rerun()

            with col2:
                if st.button("💡 Voir la solution optimale", key="mon_compo_solution", use_container_width=True):
                    st.session_state.monnaie_compo_feedback = True
                    st.session_state.monnaie_compo_voir_solution = True
                    st.rerun()
        else:
            # Afficher le résultat
            if st.session_state.get('monnaie_compo_voir_solution', False):
                st.info("💡 Voici la solution optimale (minimum de pièces/billets) :")
            elif st.session_state.get('monnaie_compo_correct', False):
                if st.session_state.get('monnaie_compo_optimal', False):
                    st.success("🎉 PARFAIT ! Tu as trouvé la solution optimale ! (+15 points)")
                    st.balloons()
                else:
                    st.success("✅ BRAVO ! Le montant est correct ! (+10 points)")
                    st.info("💡 Il existe une solution avec moins de pièces/billets")
            else:
                st.error("❌ Le montant n'est pas correct. Voici la solution optimale :")

            # Affichage visuel des pièces optimales
            st.markdown(f"**Solution optimale pour {ex['montant_texte']} :**")
            html_pieces = dessiner_pieces_monnaie(ex['composition'])
            st.markdown(html_pieces, unsafe_allow_html=True)

            # Détail texte
            st.markdown("**Détail :**")
            for valeur, nom, quantite in ex['composition']:
                st.write(f"- {quantite} × {nom}")

            # Bouton suivant
            if st.button("➡️ Exercice suivant", key="mon_compo_next", use_container_width=True):
                st.session_state.monnaie_compo_nouveau = True
                st.session_state.monnaie_compo_feedback = False
                st.session_state.monnaie_compo_voir_solution = False
                st.rerun()

    # ========= PROBLÈME RÉALISTE =========
    elif type_exercice == "Problème réaliste":
        st.subheader("🛒 Problème de la vie réelle")

        # Générer ou récupérer exercice
        if 'monnaie_pb_ex' not in st.session_state or st.session_state.get('monnaie_pb_nouveau', False):
            st.session_state.monnaie_pb_ex = generer_probleme_realiste(niveau)
            st.session_state.monnaie_pb_feedback = False
            st.session_state.monnaie_pb_nouveau = False

        ex = st.session_state.monnaie_pb_ex

        # Affichage de la question
        st.markdown(f"### {ex['question']}")

        if not st.session_state.get('monnaie_pb_feedback', False):
            # Saisie de la réponse (en euros et centimes séparés)
            col1, col2 = st.columns(2)
            with col1:
                euros_reponse = st.number_input("Euros à rendre :", min_value=0, max_value=50, value=0, key="mon_pb_euros")
            with col2:
                centimes_reponse = st.number_input("Centimes à rendre :", min_value=0, max_value=99, value=0, key="mon_pb_cents")

            if st.button("✅ Vérifier", key="mon_pb_verify", use_container_width=True):
                reponse_totale = euros_reponse * 100 + centimes_reponse
                correct = (reponse_totale == ex['reponse_centimes'])

                st.session_state.monnaie_pb_correct = correct
                st.session_state.monnaie_pb_reponse = reponse_totale
                st.session_state.monnaie_pb_feedback = True

                # Stats
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1
                if correct:
                    st.session_state.points += 30  # Plus de points pour problème complexe
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1

                # Système adaptatif
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('monnaie', correct, difficulty=4)

                auto_save_profil(correct)
                st.rerun()

        else:
            # Afficher feedback
            if st.session_state.monnaie_pb_correct:
                st.success("🎉 Excellent ! Tu as tout bon !")
                st.balloons()
            else:
                st.error(f"❌ Presque ! La bonne réponse était : {ex['reponse_texte']}")

                # Explication détaillée
                st.markdown("---")
                st.markdown("### 📚 Explication")
                st.info(f"**Total à payer :** {ex['total_texte']}")
                st.info(f"**Tu payes avec :** {ex['paye_texte']}")
                explication = expliquer_calcul_rendu(
                    ex['total_centimes'],
                    ex['paye_centimes'],
                    ex['reponse_centimes']
                )
                st.markdown(explication)

            # Bouton suivant
            if st.button("➡️ Exercice suivant", key="mon_pb_next", use_container_width=True):
                st.session_state.monnaie_pb_nouveau = True
                st.session_state.monnaie_pb_feedback = False
                st.rerun()

# ============================================
# 🎓 MODE ENTRAÎNEUR - APPRENTISSAGE GUIDÉ
# ============================================

def mode_entraineur_section():
    """
    Mode où l'enfant est guidé pas-à-pas dans la résolution
    Construit vraiment la compréhension des méthodes
    """
    
    st.markdown('<div class="categorie-header">🎓 Mode Entraîneur - Apprentissage Guidé</div>', unsafe_allow_html=True)
    
    st.write("Je vais t'accompagner **étape par étape** dans les calculs complexes!")
    st.info("💡 Ce mode t'apprend les MÉTHODES pour calculer intelligemment")
    
    # Adapter types selon niveau
    if st.session_state.niveau == "CE1":
        types_disponibles = ["Addition simple (bonds)", "Addition jusqu'à 10", "Soustraction simple"]
    elif st.session_state.niveau == "CE2":
        types_disponibles = ["Addition avec dizaines", "Soustraction simple", "Division simple"]
    elif st.session_state.niveau == "CM1":
        types_disponibles = ["Addition avec dizaines", "Soustraction avec retenue", "Multiplication décomposée", "Division simple", "Division avec reste"]
    else:  # CM2
        types_disponibles = ["Addition avec dizaines", "Soustraction avec retenue", "Multiplication décomposée", "Division simple", "Division avec reste"]
    
    # Choisir type d'entraînement
    exercice_type = st.radio(
        "Qu'est-ce que tu veux apprendre?", 
        types_disponibles,
        horizontal=True, 
        key="entraineur_type"
    )
    
    st.markdown("---")
    
    # Dispatcher selon type
    if exercice_type == "Addition simple (bonds)":
        mode_entraineur_addition_simple()
    elif exercice_type == "Addition jusqu'à 10":
        mode_entraineur_addition_bonds5()
    elif exercice_type == "Soustraction simple" and st.session_state.niveau == "CE1":
        mode_entraineur_soustraction_ce1()
    elif exercice_type == "Addition avec dizaines":
        mode_entraineur_addition_dizaines()
    elif exercice_type == "Soustraction simple" and st.session_state.niveau == "CE2":
        mode_entraineur_soustraction_simple()
    elif exercice_type == "Soustraction avec retenue":
        mode_entraineur_soustraction_retenue()
    elif exercice_type == "Multiplication décomposée":
        mode_entraineur_multiplication()
    elif exercice_type == "Division simple":
        mode_entraineur_division_simple()
    elif exercice_type == "Division avec reste":
        mode_entraineur_division_reste()

def mode_entraineur_addition_simple():
    """
    Addition simple pour CE1 : méthode des bonds
    Exemple: 8 + 5 = ?
    """
    
    # Initialiser exercice
    if 'entraineur_add_simple' not in st.session_state:
        a = random.randint(5, 10)
        b = random.randint(3, 9)
        st.session_state.entraineur_add_simple = {
            'a': a,
            'b': b,
            'etape': 1,
            'reponses': {},
            'termine': False
        }
    
    ex = st.session_state.entraineur_add_simple
    a, b = ex['a'], ex['b']
    
    
    # Si exercice terminé, afficher récap + bouton suivant
    if ex.get('termine', False):
        st.markdown('<div class="feedback-success">🎉 BRAVO ! Tu as réussi !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.markdown("---")
        st.success(f"✨ **Méthode retenue:** {a} + {b} = {a + b}")
        st.write("Pour additionner, on fait des bonds sur la ligne des nombres!")
        
        st.markdown("---")
        
        # Bouton suivant avec callback
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice guidé", key="new_add_simple", use_container_width=True, type="primary"):
                # Supprimer l'ancien exercice
                del st.session_state['entraineur_add_simple']
                
                # Générer immédiatement un nouveau
                a_new = random.randint(5, 10)
                b_new = random.randint(3, 9)
                
                # S'assurer que c'est différent
                while a_new == a and b_new == b:
                    a_new = random.randint(5, 10)
                    b_new = random.randint(3, 9)
                
                st.session_state.entraineur_add_simple = {
                    'a': a_new,
                    'b': b_new,
                    'etape': 1,
                    'reponses': {},
                    'termine': False
                }
                
                st.rerun()
        
        return  # Arrête l'exécution ici
    
    # ÉTAPE 1 : Méthode des bonds (si pas terminé)
    st.subheader(f"🎯 Calculons ensemble : {a} + {b}")
    
    if ex['etape'] == 1:
        st.write("### Étape 1 : On va faire des bonds!")
        st.write(f"On part de **{a}** et on va avancer de **{b}** cases")
        
        # Visualisation
        st.write("**Imagine une ligne de nombres:**")
        ligne = ""
        for i in range(max(a-2, 0), a+b+3):
            if i == a:
                ligne += f" **[{i}]** "
            else:
                ligne += f" {i} "
        st.code(ligne)
        
        st.write(f"✨ **Question:** Si on part de {a} et on avance de {b}, où arrive-t-on?")
        
        reponse = st.number_input("Réponse:", min_value=0, max_value=50, key="add_simple_etape1", value=0)
        
        if st.button("✅ Vérifier", key="check_add_simple_1", use_container_width=True):
            if reponse == a + b:
                # Marquer comme terminé
                st.session_state.entraineur_add_simple['termine'] = True
                
                # Points
                st.session_state.points += 30
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('addition', True, difficulty=2)

                auto_save_profil(True)
                
                st.rerun()
            else:
                st.error("❌ Pas tout à fait...")
                st.info(f"💡 **Aide:** Compte sur tes doigts ou dessine {b} bonds à partir de {a}")
def mode_entraineur_addition_bonds5():
    """Addition CE1 : méthode bonds de 5"""
    
    if 'entraineur_bonds5' not in st.session_state:
        a = random.randint(6, 9)
        b = random.randint(6, 9)
        st.session_state.entraineur_bonds5 = {
            'a': a,
            'b': b,
            'etape': 1,
            'reponses': {},
            'termine': False
        }
    
    ex = st.session_state.entraineur_bonds5
    a, b = ex['a'], ex['b']
    
    # Si terminé
    if ex.get('termine', False):
        manque = ex['reponses']['manque']
        reste = ex['reponses']['reste']
        correct = a + b
        
        st.markdown('<div class="feedback-success">🎉 EXCELLENT ! Méthode par 10 maîtrisée !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.write("---")
        st.write("### ✨ Récapitulatif")
        st.write(f"1. {a} + {manque} = 10")
        st.write(f"2. Il reste {reste} à ajouter")
        st.write(f"3. 10 + {reste} = **{correct}**")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice", key="new_bonds5", use_container_width=True, type="primary"):
                del st.session_state['entraineur_bonds5']
                
                # Nouveau différent
                a_new = random.randint(6, 9)
                b_new = random.randint(6, 9)
                while a_new == a and b_new == b:
                    a_new = random.randint(6, 9)
                    b_new = random.randint(6, 9)
                
                st.session_state.entraineur_bonds5 = {
                    'a': a_new,
                    'b': b_new,
                    'etape': 1,
                    'reponses': {},
                    'termine': False
                }
                st.rerun()
        
        return
    
    # Exercice normal
    st.subheader(f"🎯 Calculons ensemble : {a} + {b}")
    
    if ex['etape'] == 1:
        st.write("### Étape 1 : D'abord, allons jusqu'à 10!")
        st.write(f"On part de **{a}**")
        st.write(f"Combien faut-il ajouter pour arriver à 10?")
        
        st.info(f"💡 De {a} à 10, il faut ajouter...")
        
        reponse = st.number_input("Il faut ajouter:", min_value=0, max_value=10, key="bonds5_step1")
        
        if st.button("✅ Vérifier", key="check_bonds5_1", use_container_width=True):
            manque = 10 - a
            if reponse == manque:
                st.success(f"✅ Exact! {a} + {manque} = 10")
                st.session_state.entraineur_bonds5['reponses']['manque'] = manque
                st.session_state.entraineur_bonds5['etape'] = 2
                st.rerun()
            else:
                st.error(f"❌ Regarde: de {a} à 10, combien de bonds?")
    
    elif ex['etape'] == 2:
        manque = ex['reponses']['manque']
        st.success(f"✅ {a} + {manque} = 10")
        st.write("---")
        st.write("### Étape 2 : Que reste-t-il à ajouter?")
        st.write(f"On voulait ajouter **{b}** en tout")
        st.write(f"On a déjà ajouté **{manque}**")
        st.write(f"**Combien reste-t-il à ajouter?**")
        
        reponse = st.number_input("Il reste:", min_value=0, max_value=10, key="bonds5_step2")
        
        if st.button("✅ Vérifier", key="check_bonds5_2", use_container_width=True):
            reste = b - manque
            if reponse == reste:
                st.success(f"✅ Parfait! {b} - {manque} = {reste}")
                st.session_state.entraineur_bonds5['reponses']['reste'] = reste
                st.session_state.entraineur_bonds5['etape'] = 3
                st.rerun()
            else:
                st.error("❌ Essaie encore")
    
    elif ex['etape'] == 3:
        manque = ex['reponses']['manque']
        reste = ex['reponses']['reste']
        
        st.success(f"✅ Jusqu'à 10: {a} + {manque} = 10")
        st.success(f"✅ Reste à ajouter: {reste}")
        st.write("---")
        st.write("### Étape 3 : Résultat final")
        st.write(f"**10 + {reste} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=30, key="bonds5_final")
        
        if st.button("✅ Vérifier", key="check_bonds5_final", use_container_width=True):
            correct = a + b
            if reponse == correct:
                st.session_state.entraineur_bonds5['termine'] = True
                st.session_state.points += 30
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('addition', True, difficulty=3)

                auto_save_profil(True)
                st.rerun()
            else:
                st.error(f"❌ Non, c'est {correct}")


def mode_entraineur_soustraction_ce1():
    """Soustraction simple CE1"""
    
    if 'entraineur_sous_ce1' not in st.session_state:
        a = random.randint(10, 20)
        b = random.randint(3, 9)
        st.session_state.entraineur_sous_ce1 = {
            'a': a,
            'b': b,
            'termine': False
        }
    
    ex = st.session_state.entraineur_sous_ce1
    a, b = ex['a'], ex['b']
    
    # Si terminé
    if ex.get('termine', False):
        correct = a - b
        
        st.markdown('<div class="feedback-success">🎉 BRAVO !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.write("---")
        st.write(f"**{a} - {b} = {correct}**")
        st.write("Tu as bien compté les objets restants!")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice", key="new_sous_ce1", use_container_width=True, type="primary"):
                del st.session_state['entraineur_sous_ce1']
                
                # Nouveau différent
                a_new = random.randint(10, 20)
                b_new = random.randint(3, 9)
                while a_new == a and b_new == b:
                    a_new = random.randint(10, 20)
                    b_new = random.randint(3, 9)
                
                st.session_state.entraineur_sous_ce1 = {
                    'a': a_new,
                    'b': b_new,
                    'termine': False
                }
                st.rerun()
        
        return
    
    # Exercice normal
    st.subheader(f"🎯 Calculons ensemble : {a} - {b}")
    
    st.write("### Étape 1 : Imagine les nombres")
    st.write(f"Tu as **{a}** objets")
    st.write(f"Tu en enlèves **{b}**")
    
    # Visualisation simple
    st.write("**Avant:**")
    st.write("🔵 " * a)
    
    st.write("**Après avoir enlevé:**")
    st.write("🔵 " * (a - b) + "⚪ " * b)
    
    st.write(f"**Combien reste-t-il?**")
    
    reponse = st.number_input("Il reste:", min_value=0, max_value=30, key="sous_ce1_result")
    
    if st.button("✅ Vérifier", key="check_sous_ce1", use_container_width=True):
        correct = a - b
        if reponse == correct:
            st.session_state.entraineur_sous_ce1['termine'] = True
            st.session_state.points += 25
            st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
            st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

            # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
            if "profil" in st.session_state:
                tracker = SkillTracker(st.session_state.profil)
                tracker.record_exercise('soustraction', True, difficulty=1)

            auto_save_profil(True)
            st.rerun()
        else:
            st.error(f"❌ Non, c'est {correct}")
            st.info(f"💡 Compte les points bleus restants: {correct}")

def mode_entraineur_addition_dizaines():
    """
    Addition avec dizaines : décomposition complète
    Exemple: 47 + 28 = ?
    """
    
    # Initialiser exercice
    if 'entraineur_add_diz' not in st.session_state:
        a = random.randint(20, 60)
        b = random.randint(15, 40)
        st.session_state.entraineur_add_diz = {
            'a': a,
            'b': b,
            'etape': 1,
            'reponses': {}
        }
    
    ex = st.session_state.entraineur_add_diz
    a, b = ex['a'], ex['b']
    
    st.subheader(f"🎯 Calculons ensemble : {a} + {b}")
    
    # Calculer décompositions
    diz_a, unit_a = a // 10, a % 10
    diz_b, unit_b = b // 10, b % 10
    
    # ÉTAPE 1 : Décomposer premier nombre
    if ex['etape'] == 1:
        st.write("### Étape 1 : Décomposons le premier nombre")
        st.write(f"**{a}** = ? dizaines + ? unités")
        
        st.info(f"💡 **Aide:** Dans {a}, regarde le chiffre des dizaines et celui des unités")
        
        col1, col2 = st.columns(2)
        with col1:
            diz_input = st.number_input(
                f"Combien de dizaines dans {a}?", 
                min_value=0, 
                max_value=9, 
                key="diz_a",
                help=f"Le chiffre des dizaines de {a}"
            )
        with col2:
            unit_input = st.number_input(
                f"Combien d'unités dans {a}?", 
                min_value=0, 
                max_value=9, 
                key="unit_a",
                help=f"Le chiffre des unités de {a}"
            )
        
        if st.button("✅ Vérifier", key="check_etape1"):
            if diz_input == diz_a and unit_input == unit_a:
                st.success(f"✅ Parfait! {a} = {diz_a}0 + {unit_a}")
                st.write(f"🎯 On peut aussi écrire: {a} = ({diz_a} × 10) + {unit_a}")
                ex['reponses']['diz_a'] = diz_a
                ex['reponses']['unit_a'] = unit_a
                ex['etape'] = 2
                st.rerun()
            else:
                st.error("❌ Regarde bien les chiffres")
                st.info(f"💡 **Indice:** {a} s'écrit avec le chiffre **{diz_a}** aux dizaines et **{unit_a}** aux unités")
    
    # ÉTAPE 2 : Décomposer deuxième nombre
    elif ex['etape'] == 2:
        st.success(f"✅ Étape 1 réussie: {a} = {diz_a}0 + {unit_a}")
        st.write("---")
        st.write("### Étape 2 : Décomposons le deuxième nombre")
        st.write(f"**{b}** = ? dizaines + ? unités")
        
        col1, col2 = st.columns(2)
        with col1:
            diz_input = st.number_input(f"Combien de dizaines dans {b}?", min_value=0, max_value=9, key="diz_b")
        with col2:
            unit_input = st.number_input(f"Combien d'unités dans {b}?", min_value=0, max_value=9, key="unit_b")
        
        if st.button("✅ Vérifier", key="check_etape2"):
            if diz_input == diz_b and unit_input == unit_b:
                st.success(f"✅ Exact! {b} = {diz_b}0 + {unit_b}")
                ex['reponses']['diz_b'] = diz_b
                ex['reponses']['unit_b'] = unit_b
                ex['etape'] = 3
                st.rerun()
            else:
                st.error("❌ Essaie encore")
    
    # ÉTAPE 3 : Additionner les dizaines
    elif ex['etape'] == 3:
        st.success(f"✅ Décompositions: {a} = {diz_a}0 + {unit_a}  |  {b} = {diz_b}0 + {unit_b}")
        st.write("---")
        st.write("### Étape 3 : Additionnons les dizaines")
        st.write(f"**{diz_a}0 + {diz_b}0 = ?**")
        
        st.info(f"💡 C'est comme {diz_a} + {diz_b}, mais avec un zéro à la fin!")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=200, step=10, key="add_diz")
        
        if st.button("✅ Vérifier", key="check_etape3"):
            correct_diz = (diz_a + diz_b) * 10
            if reponse == correct_diz:
                st.success(f"✅ Bien! {diz_a}0 + {diz_b}0 = {reponse}")
                ex['reponses']['dizaines_sum'] = reponse
                ex['etape'] = 4
                st.rerun()
            else:
                st.error("❌ Réessaye")
                st.info(f"💡 **Aide:** {diz_a} + {diz_b} = {diz_a + diz_b}, donc {diz_a}0 + {diz_b}0 = {correct_diz}")
    
    # ÉTAPE 4 : Additionner les unités
    elif ex['etape'] == 4:
        dizaines_sum = ex['reponses']['dizaines_sum']
        st.success(f"✅ Dizaines: {diz_a}0 + {diz_b}0 = {dizaines_sum}")
        st.write("---")
        st.write("### Étape 4 : Additionnons les unités")
        st.write(f"**{unit_a} + {unit_b} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=20, key="add_unit")
        
        if st.button("✅ Vérifier", key="check_etape4"):
            unites_sum = unit_a + unit_b
            if reponse == unites_sum:
                st.success(f"✅ Parfait! {unit_a} + {unit_b} = {reponse}")
                ex['reponses']['unites_sum'] = reponse
                
                # Vérifier si retenue nécessaire
                if reponse >= 10:
                    st.warning(f"⚠️ Attention! {reponse} est plus grand que 10. Il y a une **retenue**!")
                    ex['etape'] = 5
                else:
                    ex['etape'] = 6
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 5 : Gérer la retenue
    elif ex['etape'] == 5:
        dizaines_sum = ex['reponses']['dizaines_sum']
        unites_sum = ex['reponses']['unites_sum']
        
        st.success(f"✅ Dizaines: {dizaines_sum}  |  Unités: {unites_sum}")
        st.write("---")
        st.write("### Étape 5 : Gérons la retenue!")
        
        st.write(f"🎯 Les unités donnent **{unites_sum}**")
        st.write(f"C'est plus que 10, donc:")
        st.write(f"- {unites_sum} = **10** + **{unites_sum - 10}**")
        st.write(f"- On ajoute 10 aux dizaines → {dizaines_sum} + 10 = ?")
        
        reponse = st.number_input("Nouveau total des dizaines:", min_value=0, max_value=200, key="add_retenue")
        
        if st.button("✅ Vérifier", key="check_etape5"):
            if reponse == dizaines_sum + 10:
                st.success(f"✅ Super! {dizaines_sum} + 10 = {reponse}")
                ex['reponses']['dizaines_avec_retenue'] = reponse
                ex['reponses']['unites_restantes'] = unites_sum - 10
                ex['etape'] = 6
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 6 : Résultat final
    elif ex['etape'] == 6:
        if 'dizaines_avec_retenue' in ex['reponses']:
            dizaines_finales = ex['reponses']['dizaines_avec_retenue']
            unites_finales = ex['reponses']['unites_restantes']
            st.success(f"✅ Avec retenue - Dizaines: {dizaines_finales}  |  Unités: {unites_finales}")
        else:
            dizaines_finales = ex['reponses']['dizaines_sum']
            unites_finales = ex['reponses']['unites_sum']
            st.success(f"✅ Sans retenue - Dizaines: {dizaines_finales}  |  Unités: {unites_finales}")
        
        st.write("---")
        st.write("### Étape 6 : Assemblons le résultat!")
        st.write(f"**{dizaines_finales} + {unites_finales} = ?**")
        
        st.info(f"💡 On assemble les dizaines et les unités")
        
        reponse = st.number_input("Résultat final:", min_value=0, max_value=200, key="final")
        
        if st.button("✅ Vérifier", key="check_final"):
            correct = a + b
            if reponse == correct:
                st.markdown('<div class="feedback-success">🎉 EXCELLENT ! Tu as tout compris !</div>', unsafe_allow_html=True)
                st.balloons()
                
                # Récapitulatif de la méthode
                st.write("---")
                st.write("### ✨ Récapitulatif de la méthode")
                st.write(f"1. {a} = {diz_a}0 + {unit_a}")
                st.write(f"2. {b} = {diz_b}0 + {unit_b}")
                st.write(f"3. Dizaines: {diz_a}0 + {diz_b}0 = {ex['reponses']['dizaines_sum']}")
                st.write(f"4. Unités: {unit_a} + {unit_b} = {ex['reponses']['unites_sum']}")
                if 'dizaines_avec_retenue' in ex['reponses']:
                    st.write(f"5. Retenue: {ex['reponses']['dizaines_sum']} + 10 = {ex['reponses']['dizaines_avec_retenue']}")
                    st.write(f"6. Résultat: {ex['reponses']['dizaines_avec_retenue']} + {ex['reponses']['unites_restantes']} = **{correct}**")
                else:
                    st.write(f"5. Résultat: {dizaines_finales} + {unites_finales} = **{correct}**")
                
                # Points élevés car effort
                st.session_state.points += 40
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('addition', True, difficulty=5)

                auto_save_profil(True)
                
                if st.button("➡️ Nouvel exercice guidé", key="new_add_diz"):
                    del st.session_state.entraineur_add_diz
                    st.rerun()
            else:
                st.error(f"❌ Non, c'est {correct}")
                st.info("💡 Revérifie tes calculs précédents")
def mode_entraineur_soustraction_simple():
    """Soustraction simple sans retenue (CE2)"""
    
    if 'entraineur_sous_simple' not in st.session_state:
        a = random.randint(30, 70)
        b = random.randint(10, 30)
        # S'assurer pas de retenue
        while (a % 10) < (b % 10):
            a = random.randint(30, 70)
            b = random.randint(10, 30)
        
        st.session_state.entraineur_sous_simple = {
            'a': a,
            'b': b,
            'etape': 1,
            'reponses': {}
        }
    
    ex = st.session_state.entraineur_sous_simple
    a, b = ex['a'], ex['b']
    
    st.subheader(f"🎯 Calculons ensemble : {a} - {b}")
    
    diz_a, unit_a = a // 10, a % 10
    diz_b, unit_b = b // 10, b % 10
    
    # ÉTAPE 1 : Décomposer premier nombre
    if ex['etape'] == 1:
        st.write("### Étape 1 : Décomposons le premier nombre")
        st.write(f"**{a}** = ? dizaines + ? unités")
        
        col1, col2 = st.columns(2)
        with col1:
            diz_input = st.number_input(f"Dizaines de {a}?", min_value=0, max_value=9, key="sous_diz_a")
        with col2:
            unit_input = st.number_input(f"Unités de {a}?", min_value=0, max_value=9, key="sous_unit_a")
        
        if st.button("✅ Vérifier", key="check_sous_simple_1"):
            if diz_input == diz_a and unit_input == unit_a:
                st.success(f"✅ Parfait! {a} = {diz_a}0 + {unit_a}")
                ex['reponses']['diz_a'] = diz_a
                ex['reponses']['unit_a'] = unit_a
                ex['etape'] = 2
                st.rerun()
            else:
                st.error("❌ Regarde bien")
    
    # ÉTAPE 2 : Décomposer deuxième nombre
    elif ex['etape'] == 2:
        st.success(f"✅ {a} = {diz_a}0 + {unit_a}")
        st.write("---")
        st.write("### Étape 2 : Décomposons le deuxième nombre")
        st.write(f"**{b}** = ? dizaines + ? unités")
        
        col1, col2 = st.columns(2)
        with col1:
            diz_input = st.number_input(f"Dizaines de {b}?", min_value=0, max_value=9, key="sous_diz_b")
        with col2:
            unit_input = st.number_input(f"Unités de {b}?", min_value=0, max_value=9, key="sous_unit_b")
        
        if st.button("✅ Vérifier", key="check_sous_simple_2"):
            if diz_input == diz_b and unit_input == unit_b:
                st.success(f"✅ Exact! {b} = {diz_b}0 + {unit_b}")
                ex['reponses']['diz_b'] = diz_b
                ex['reponses']['unit_b'] = unit_b
                ex['etape'] = 3
                st.rerun()
            else:
                st.error("❌ Essaie encore")
    
    # ÉTAPE 3 : Soustraire les dizaines
    elif ex['etape'] == 3:
        st.success(f"✅ {a} = {diz_a}0 + {unit_a}  |  {b} = {diz_b}0 + {unit_b}")
        st.write("---")
        st.write("### Étape 3 : Soustrayons les dizaines")
        st.write(f"**{diz_a}0 - {diz_b}0 = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=100, step=10, key="sous_diz_result")
        
        if st.button("✅ Vérifier", key="check_sous_simple_3"):
            if reponse == (diz_a - diz_b) * 10:
                st.success(f"✅ Bien! {diz_a}0 - {diz_b}0 = {reponse}")
                ex['reponses']['dizaines_result'] = reponse
                ex['etape'] = 4
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 4 : Soustraire les unités
    elif ex['etape'] == 4:
        diz_result = ex['reponses']['dizaines_result']
        st.success(f"✅ Dizaines: {diz_result}")
        st.write("---")
        st.write("### Étape 4 : Soustrayons les unités")
        st.write(f"**{unit_a} - {unit_b} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=10, key="sous_unit_result")
        
        if st.button("✅ Vérifier", key="check_sous_simple_4"):
            if reponse == unit_a - unit_b:
                st.success(f"✅ Parfait! {unit_a} - {unit_b} = {reponse}")
                ex['reponses']['unites_result'] = reponse
                ex['etape'] = 5
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 5 : Résultat final
    elif ex['etape'] == 5:
        diz_result = ex['reponses']['dizaines_result']
        unit_result = ex['reponses']['unites_result']
        
        st.success(f"✅ Dizaines: {diz_result}  |  Unités: {unit_result}")
        st.write("---")
        st.write("### Étape 5 : Assemblons!")
        st.write(f"**{diz_result} + {unit_result} = ?**")
        
        reponse = st.number_input("Résultat final:", min_value=0, max_value=100, key="sous_simple_final")
        
        if st.button("✅ Vérifier", key="check_sous_simple_final"):
            correct = a - b
            if reponse == correct:
                st.markdown('<div class="feedback-success">🎉 BRAVO ! Soustraction maîtrisée !</div>', unsafe_allow_html=True)
                st.balloons()
                
                # Récapitulatif
                st.write("---")
                st.write("### ✨ Récapitulatif")
                st.write(f"1. {a} = {diz_a}0 + {unit_a}")
                st.write(f"2. {b} = {diz_b}0 + {unit_b}")
                st.write(f"3. Dizaines: {diz_a}0 - {diz_b}0 = {diz_result}")
                st.write(f"4. Unités: {unit_a} - {unit_b} = {unit_result}")
                st.write(f"5. Résultat: {diz_result} + {unit_result} = **{correct}**")
                
                st.session_state.points += 35
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('soustraction', True, difficulty=3)

                auto_save_profil(True)
                
                if st.button("➡️ Nouvel exercice", key="new_sous_simple"):
                    del st.session_state.entraineur_sous_simple
                    st.rerun()
            else:
                st.error(f"❌ Non, c'est {correct}")

def mode_entraineur_soustraction_retenue():
    """Soustraction avec retenue (CM1+) - Version simplifiée"""
    
    if 'entraineur_sous_ret' not in st.session_state:
        a = random.randint(40, 80)
        b = random.randint(15, 35)
        # Forcer une retenue
        while (a % 10) >= (b % 10):
            a = random.randint(40, 80)
            b = random.randint(15, 35)
        
        st.session_state.entraineur_sous_ret = {
            'a': a,
            'b': b,
            'etape': 1,
            'reponses': {}
        }
    
    ex = st.session_state.entraineur_sous_ret
    a, b = ex['a'], ex['b']
    
    st.subheader(f"🎯 Soustraction avec retenue : {a} - {b}")
    
    unit_a, unit_b = a % 10, b % 10
    
    # ÉTAPE 1 : Identifier le problème
    if ex['etape'] == 1:
        st.write("### Étape 1 : Problème détecté!")
        st.write(f"On veut faire **{unit_a} - {unit_b}**")
        st.write(f"Mais **{unit_a} < {unit_b}** → On ne peut pas!")
        
        st.info("💡 Quand on ne peut pas enlever les unités directement, il faut **emprunter une dizaine**")
        
        if st.button("✅ J'ai compris, montre-moi comment!", key="sous_ret_1"):
            ex['etape'] = 2
            st.rerun()
    
    # ÉTAPE 2 : Emprunter une dizaine
    elif ex['etape'] == 2:
        st.write("### Étape 2 : Empruntons une dizaine")
        st.write(f"Au lieu de {unit_a} unités, on va avoir **{unit_a + 10}** unités")
        st.write(f"(On a emprunté 10 à la dizaine)")
        
        st.write(f"Maintenant on peut faire : **{unit_a + 10} - {unit_b} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=20, key="sous_ret_unit")
        
        if st.button("✅ Vérifier", key="check_sous_ret_2"):
            if reponse == (unit_a + 10) - unit_b:
                st.success(f"✅ Parfait! {unit_a + 10} - {unit_b} = {reponse}")
                ex['reponses']['unites_result'] = reponse
                ex['etape'] = 3
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 3 : Ajuster les dizaines
    elif ex['etape'] == 3:
        diz_a = a // 10
        diz_b = b // 10
        
        st.success(f"✅ Unités: {ex['reponses']['unites_result']}")
        st.write("---")
        st.write("### Étape 3 : Ajustons les dizaines")
        st.write(f"On avait {diz_a} dizaines, mais on en a emprunté 1")
        st.write(f"Il reste donc **{diz_a - 1}** dizaines")
        st.write(f"On enlève {diz_b} dizaines → **{diz_a - 1} - {diz_b} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=10, key="sous_ret_diz")
        
        if st.button("✅ Vérifier", key="check_sous_ret_3"):
            if reponse == (diz_a - 1 - diz_b):
                st.success(f"✅ Exact! {diz_a - 1} - {diz_b} = {reponse}")
                ex['reponses']['dizaines_result'] = reponse
                ex['etape'] = 4
                st.rerun()
            else:
                st.error("❌ Réessaye")
    
    # ÉTAPE 4 : Résultat final
    elif ex['etape'] == 4:
        diz_result = ex['reponses']['dizaines_result']
        unit_result = ex['reponses']['unites_result']
        
        st.success(f"✅ Dizaines: {diz_result}  |  Unités: {unit_result}")
        st.write("---")
        st.write("### Étape 4 : Résultat final")
        st.write(f"**{diz_result}0 + {unit_result} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=100, key="sous_ret_final")
        
        if st.button("✅ Vérifier", key="check_sous_ret_final"):
            correct = a - b
            if reponse == correct:
                st.markdown('<div class="feedback-success">🎉 BRAVO ! Soustraction avec retenue maîtrisée !</div>', unsafe_allow_html=True)
                st.balloons()
                
                st.session_state.points += 45
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('soustraction', True, difficulty=5)

                auto_save_profil(True)
                
                if st.button("➡️ Nouvel exercice", key="new_sous_ret"):
                    del st.session_state.entraineur_sous_ret
                    st.rerun()
            else:
                st.error(f"❌ Non, c'est {correct}")
def mode_entraineur_multiplication():
    """Multiplication avec décomposition (CM1+)"""
    
    if 'entraineur_mult' not in st.session_state:
        # Générer des multiplications hors tables de base (> 10×10)
        table = random.randint(11, 20)  # De 11 à 20 au lieu de 6-9
        mult = random.randint(2, 9)     # Multiplier par 2-9
        
        # Ou alternative : un des deux nombres doit être > 10
        # table = random.randint(6, 15)
        # mult = random.randint(6, 12)
        # while table <= 10 and mult <= 10:  # Éviter tables de base
        #     table = random.randint(6, 15)
        #     mult = random.randint(6, 12)
        
        st.session_state.entraineur_mult = {
            'table': table,
            'mult': mult,
            'etape': 1,
            'reponses': {},
            'methode_choisie': None,
            'termine': False
        }
    
    ex = st.session_state.entraineur_mult
    table, mult = ex['table'], ex['mult']
    
    # Si exercice terminé, afficher récap
    if ex.get('termine', False):
        methode = ex['methode_choisie']
        
        st.markdown('<div class="feedback-success">🎉 EXCELLENT ! Tu maîtrises la méthode !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.write("---")
        st.write("### ✨ Récapitulatif")
        
        # Afficher selon méthode
        if methode == "Par 10":
            step1 = ex['reponses']['step1']
            step2 = ex['reponses']['step2']
            st.write(f"**Méthode Par 10:**")
            st.write(f"1. {table} × 10 = {step1}")
            st.write(f"2. {table} × {10 - mult} = {step2}")
            st.write(f"3. {step1} - {step2} = **{table * mult}**")
        
        elif methode == "Doubler":
            step1 = ex['reponses']['step1']
            final = ex['reponses']['final']
            st.write(f"**Méthode Doubler:**")
            st.write(f"1. {table} × {mult // 2} = {step1}")
            st.write(f"2. {step1} × 2 = **{final}**")
        
        else:  # Décomposer
            step1 = ex['reponses']['step1']
            step2 = ex['reponses']['step2']
            st.write(f"**Méthode Décomposer:**")
            st.write(f"1. {table} × 5 = {step1}")
            st.write(f"2. {table} × {mult - 5} = {step2}")
            st.write(f"3. {step1} + {step2} = **{table * mult}**")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice", key="new_mult", use_container_width=True, type="primary"):
                del st.session_state['entraineur_mult']
                
                # Générer nouveau différent
                table_new = random.randint(11, 20)
                mult_new = random.randint(2, 9)
                
                # S'assurer différent
                while table_new == table and mult_new == mult:
                    table_new = random.randint(11, 20)
                    mult_new = random.randint(2, 9)
                
                st.session_state.entraineur_mult = {
                    'table': table_new,
                    'mult': mult_new,
                    'etape': 1,
                    'reponses': {},
                    'methode_choisie': None,
                    'termine': False
                }
                st.rerun()
        
        return
    
    # Exercice normal
    st.subheader(f"🎯 Multiplication astucieuse : {table} × {mult}")
    
    # ÉTAPE 1 : Choisir une méthode
    if ex['etape'] == 1:
        st.write("### Étape 1 : Choisis ta méthode")
        st.write(f"Pour calculer **{table} × {mult}**, on a plusieurs stratégies:")
        
        st.write("**Méthode 1 : Par 10**")
        st.write(f"→ {table} × 10 = {table * 10}, puis on enlève {table} × {10 - mult}")
        
        st.write("**Méthode 2 : Doubler**")
        st.write(f"→ {table} × {mult // 2} = ?, puis on double")
        
        st.write("**Méthode 3 : Décomposer**")
        st.write(f"→ {table} × 5 = {table * 5}, puis {table} × {mult - 5}")
        
        methode = st.radio("Quelle méthode veux-tu essayer?", 
                          ["Par 10", "Doubler", "Décomposer"], 
                          key="methode_mult")
        
        if st.button("✅ Choisir cette méthode", key="choose_method", use_container_width=True):
            st.session_state.entraineur_mult['methode_choisie'] = methode
            st.session_state.entraineur_mult['etape'] = 2
            st.rerun()
    
    # ÉTAPE 2 : Appliquer la méthode choisie
    elif ex['etape'] == 2:
        methode = ex['methode_choisie']
        st.success(f"✅ Méthode choisie: **{methode}**")
        st.write("---")
        
        if methode == "Par 10":
            st.write("### Étape 2 : Calculer par 10")
            st.write(f"**{table} × 10 = ?**")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_step1")
            
            if st.button("✅ Vérifier", key="check_mult_1", use_container_width=True):
                if reponse == table * 10:
                    st.success(f"✅ Exact! {table} × 10 = {reponse}")
                    st.session_state.entraineur_mult['reponses']['step1'] = reponse
                    st.session_state.entraineur_mult['etape'] = 3
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
        
        elif methode == "Doubler":
            demi = mult // 2
            st.write("### Étape 2 : Calculer la moitié")
            st.write(f"**{table} × {demi} = ?**")
            st.info(f"💡 {demi} est la moitié de {mult}")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_step1")
            
            if st.button("✅ Vérifier", key="check_mult_1", use_container_width=True):
                if reponse == table * demi:
                    st.success(f"✅ Bien! {table} × {demi} = {reponse}")
                    st.session_state.entraineur_mult['reponses']['step1'] = reponse
                    st.session_state.entraineur_mult['etape'] = 3
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
        
        else:  # Décomposer
            st.write("### Étape 2 : Calculer par 5")
            st.write(f"**{table} × 5 = ?**")
            st.info(f"💡 La table de 5 est plus facile!")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_step1")
            
            if st.button("✅ Vérifier", key="check_mult_1", use_container_width=True):
                if reponse == table * 5:
                    st.success(f"✅ Parfait! {table} × 5 = {reponse}")
                    st.session_state.entraineur_mult['reponses']['step1'] = reponse
                    st.session_state.entraineur_mult['etape'] = 3
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
    
    # ÉTAPE 3 : Finaliser selon méthode
    elif ex['etape'] == 3:
        methode = ex['methode_choisie']
        step1 = ex['reponses']['step1']
        
        st.success(f"✅ Étape précédente: {step1}")
        st.write("---")
        
        if methode == "Par 10":
            enlever = 10 - mult
            st.write("### Étape 3 : Enlever le surplus")
            st.write(f"On a calculé {table} × 10 = {step1}")
            st.write(f"Mais on veut {table} × {mult}")
            st.write(f"Donc on enlève {table} × {enlever}")
            st.write(f"**{table} × {enlever} = ?**")
            
            reponse = st.number_input("Combien faut-il enlever?", min_value=0, max_value=100, key="mult_step2")
            
            if st.button("✅ Vérifier", key="check_mult_2", use_container_width=True):
                if reponse == table * enlever:
                    st.success(f"✅ Exact! On enlève {reponse}")
                    st.session_state.entraineur_mult['reponses']['step2'] = reponse
                    st.session_state.entraineur_mult['etape'] = 4
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
        
        elif methode == "Doubler":
            st.write("### Étape 3 : Doubler le résultat")
            st.write(f"On a calculé {table} × {mult // 2} = {step1}")
            st.write(f"Maintenant il faut **doubler** ce résultat")
            st.write(f"**{step1} × 2 = ?**")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_step2")
            
            if st.button("✅ Vérifier", key="check_mult_2", use_container_width=True):
                if reponse == step1 * 2:
                    st.success(f"✅ Bravo! {step1} × 2 = {reponse}")
                    st.session_state.entraineur_mult['reponses']['final'] = reponse
                    st.session_state.entraineur_mult['etape'] = 4
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
        
        else:  # Décomposer
            reste = mult - 5
            st.write("### Étape 3 : Calculer le reste")
            st.write(f"On a calculé {table} × 5 = {step1}")
            st.write(f"Il reste {table} × {reste} à calculer")
            st.write(f"**{table} × {reste} = ?**")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=100, key="mult_step2")
            
            if st.button("✅ Vérifier", key="check_mult_2", use_container_width=True):
                if reponse == table * reste:
                    st.success(f"✅ Parfait! {table} × {reste} = {reponse}")
                    st.session_state.entraineur_mult['reponses']['step2'] = reponse
                    st.session_state.entraineur_mult['etape'] = 4
                    st.rerun()
                else:
                    st.error("❌ Réessaye")
    
    # ÉTAPE 4 : Résultat final
    elif ex['etape'] == 4:
        methode = ex['methode_choisie']
        
        if methode == "Par 10":
            step1 = ex['reponses']['step1']
            step2 = ex['reponses']['step2']
            st.success(f"✅ {table} × 10 = {step1}")
            st.success(f"✅ On enlève {step2}")
            st.write("---")
            st.write("### Étape 4 : Résultat final")
            st.write(f"**{step1} - {step2} = ?**")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_final")
            
            if st.button("✅ Vérifier", key="check_mult_final", use_container_width=True):
                correct = table * mult
                if reponse == correct:
                    # Marquer terminé
                    st.session_state.entraineur_mult['termine'] = True
                    st.session_state.points += 35
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                    # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('multiplication', True, difficulty=4)

                    auto_save_profil(True)
                    st.rerun()
                else:
                    st.error(f"❌ Non, c'est {correct}")
        
        elif methode == "Doubler":
            final = ex['reponses']['final']
            correct = table * mult
            
            if final == correct:
                # Marquer terminé
                st.session_state.entraineur_mult['termine'] = True
                st.session_state.points += 35
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('multiplication', True, difficulty=4)

                auto_save_profil(True)
                st.rerun()
        
        else:  # Décomposer
            step1 = ex['reponses']['step1']
            step2 = ex['reponses']['step2']
            st.success(f"✅ {table} × 5 = {step1}")
            st.success(f"✅ {table} × {mult - 5} = {step2}")
            st.write("---")
            st.write("### Étape 4 : Additionner les deux parties")
            st.write(f"**{step1} + {step2} = ?**")
            
            reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="mult_final")
            
            if st.button("✅ Vérifier", key="check_mult_final", use_container_width=True):
                correct = table * mult
                if reponse == correct:
                    # Marquer terminé
                    st.session_state.entraineur_mult['termine'] = True
                    st.session_state.points += 35
                    st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                    st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                    # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                    if "profil" in st.session_state:
                        tracker = SkillTracker(st.session_state.profil)
                        tracker.record_exercise('multiplication', True, difficulty=4)

                    auto_save_profil(True)
                    st.rerun()
                else:
                    st.error(f"❌ Non, c'est {correct}")
# ============================================
# 🔢 MODE ENTRAÎNEUR - DIVISIONS
# ============================================

def mode_entraineur_division_simple():
    """
    Division euclidienne simple (CE2-CM1)
    Quotient exact, pas de reste
    Exemple: 24 ÷ 4 = 6
    """
    
    if 'entraineur_div_simple' not in st.session_state:
        from division_utils import generer_division_simple
        ex_data = generer_division_simple(st.session_state.niveau)
        
        st.session_state.entraineur_div_simple = {
            'dividende': ex_data['dividende'],
            'diviseur': ex_data['diviseur'],
            'quotient_correct': ex_data['quotient'],
            'etape': 1,
            'reponses': {},
            'termine': False
        }
    
    ex = st.session_state.entraineur_div_simple
    dividende, diviseur = ex['dividende'], ex['diviseur']
    
    # Si terminé
    if ex.get('termine', False):
        st.markdown('<div class="feedback-success">🎉 EXCELLENT ! Division maîtrisée !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.write("---")
        st.write("### ✨ Récapitulatif")
        st.write(f"**{dividende} ÷ {diviseur} = {ex['quotient_correct']}**")
        st.write(f"✅ Vérification: {diviseur} × {ex['quotient_correct']} = {dividende}")
        
        st.write("---")
        st.info("💡 **Astuce mémorisation:** La division est l'opération inverse de la multiplication!")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice", key="new_div_simple", use_container_width=True, type="primary"):
                del st.session_state['entraineur_div_simple']
                st.rerun()
        
        return
    
    # Exercice normal
    st.subheader(f"🎯 Division : {dividende} ÷ {diviseur}")
    
    if ex['etape'] == 1:
        st.write("### Étape 1 : Comprendre la division")
        st.write(f"**{dividende} ÷ {diviseur}** signifie :")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Partage :**")
            st.write(f"🍪 {dividende} cookies")
            st.write(f"👥 {diviseur} amis")
            st.write(f"❓ Combien chacun ?")
        
        with col2:
            st.write("**Ou groupement :**")
            st.write(f"📦 {dividende} objets")
            st.write(f"🔢 Groupes de {diviseur}")
            st.write(f"❓ Combien de groupes ?")
        
        st.write("---")
        st.write(f"**Question : {dividende} ÷ {diviseur} = ?**")
        
        reponse = st.number_input("Réponse:", min_value=0, max_value=50, key="div_simple_q")
        
        if st.button("✅ Vérifier", key="check_div_simple_1", use_container_width=True):
            if reponse == ex['quotient_correct']:
                st.success(f"✅ Bravo! {dividende} ÷ {diviseur} = {reponse}")
                st.session_state.entraineur_div_simple['etape'] = 2
                st.rerun()
            else:
                st.error("❌ Pas tout à fait...")
                # Aide progressive
                if reponse < ex['quotient_correct']:
                    st.info("💡 C'est un peu plus grand")
                else:
                    st.info("💡 C'est un peu plus petit")
                
                # Méthode bonds
                st.write("---")
                st.write("**Méthode des bonds :**")
                st.write(f"Compte par {diviseur} jusqu'à {dividende}")
                bonds = [diviseur * i for i in range(1, ex['quotient_correct'] + 1)]
                st.write(f"{diviseur}, " + ", ".join(map(str, bonds[1:])))
                st.write(f"→ Tu arrives à {dividende} en **{len(bonds)}** bonds")
    
    elif ex['etape'] == 2:
        st.success(f"✅ {dividende} ÷ {diviseur} = {ex['quotient_correct']}")
        st.write("---")
        st.write("### Étape 2 : Vérification par multiplication")
        st.write("Pour vérifier une division, on multiplie le résultat par le diviseur!")
        st.write(f"**{diviseur} × {ex['quotient_correct']} = ?**")
        
        st.info("💡 Si tu retrouves le nombre de départ, c'est juste!")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="div_simple_verif")
        
        if st.button("✅ Vérifier", key="check_div_simple_2", use_container_width=True):
            if reponse == dividende:
                st.success(f"✅ Parfait! {diviseur} × {ex['quotient_correct']} = {dividende}")
                st.write("🎯 La division était donc correcte!")
                
                # Marquer terminé
                st.session_state.entraineur_div_simple['termine'] = True
                st.session_state.points += 30
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('division', True, difficulty=3)

                auto_save_profil(True)
                
                st.rerun()
            else:
                st.error("❌ Réessaye la multiplication")
                st.info(f"💡 Rappel: {diviseur} × {ex['quotient_correct']}")


def mode_entraineur_division_reste():
    """
    Division euclidienne avec reste (CM1-CM2)
    Exemple: 23 ÷ 4 = 5 reste 3
    """
    
    if 'entraineur_div_reste' not in st.session_state:
        from division_utils import generer_division_reste
        ex_data = generer_division_reste(st.session_state.niveau)
        
        st.session_state.entraineur_div_reste = {
            'dividende': ex_data['dividende'],
            'diviseur': ex_data['diviseur'],
            'quotient_correct': ex_data['quotient'],
            'reste_correct': ex_data['reste'],
            'etape': 1,
            'reponses': {},
            'termine': False
        }
    
    ex = st.session_state.entraineur_div_reste
    dividende, diviseur = ex['dividende'], ex['diviseur']
    
    # Si terminé
    if ex.get('termine', False):
        st.markdown('<div class="feedback-success">🎉 BRAVO ! Division avec reste maîtrisée !</div>', unsafe_allow_html=True)
        st.balloons()
        
        st.write("---")
        st.write("### ✨ Récapitulatif")
        st.write(f"**{dividende} ÷ {diviseur} = {ex['quotient_correct']} reste {ex['reste_correct']}**")
        st.write(f"✅ Vérification: ({diviseur} × {ex['quotient_correct']}) + {ex['reste_correct']} = {dividende}")
        
        st.write("---")
        st.info("💡 **Formule magique:** Dividende = (Diviseur × Quotient) + Reste")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Nouvel exercice", key="new_div_reste", use_container_width=True, type="primary"):
                del st.session_state['entraineur_div_reste']
                st.rerun()
        
        return
    
    # Exercice normal
    st.subheader(f"🎯 Division avec reste : {dividende} ÷ {diviseur}")
    
    if ex['etape'] == 1:
        st.write("### Étape 1 : Trouver le quotient")
        st.write(f"Combien de fois **{diviseur}** entre dans **{dividende}** ?")
        
        st.info(f"💡 Cherche la plus grande table de {diviseur} inférieure ou égale à {dividende}")
        
        # Aide visuelle
        st.write("**Tables de référence :**")
        tables = [f"{diviseur}×{i} = {diviseur*i}" for i in range(1, 12) if diviseur*i <= dividende + diviseur]
        st.write(" | ".join(tables))
        
        reponse = st.number_input("Quotient:", min_value=0, max_value=30, key="div_reste_quot")
        
        if st.button("✅ Vérifier", key="check_div_reste_1", use_container_width=True):
            if reponse == ex['quotient_correct']:
                st.success(f"✅ Exact! {diviseur} entre {reponse} fois dans {dividende}")
                st.session_state.entraineur_div_reste['reponses']['quotient'] = reponse
                st.session_state.entraineur_div_reste['etape'] = 2
                st.rerun()
            else:
                if reponse < ex['quotient_correct']:
                    st.warning(f"⚠️ C'est trop petit. {diviseur}×{reponse} = {diviseur*reponse}, on peut aller plus loin!")
                else:
                    st.warning(f"⚠️ C'est trop grand. {diviseur}×{reponse} = {diviseur*reponse} > {dividende}")
    
    elif ex['etape'] == 2:
        quotient = ex['reponses']['quotient']
        st.success(f"✅ Quotient: {quotient}")
        st.write("---")
        st.write("### Étape 2 : Calculer le produit")
        st.write(f"On a trouvé que {diviseur} entre {quotient} fois")
        st.write(f"Calculons : **{diviseur} × {quotient} = ?**")
        
        reponse = st.number_input("Résultat:", min_value=0, max_value=200, key="div_reste_produit")
        
        if st.button("✅ Vérifier", key="check_div_reste_2", use_container_width=True):
            produit = diviseur * quotient
            if reponse == produit:
                st.success(f"✅ Bien! {diviseur} × {quotient} = {produit}")
                st.session_state.entraineur_div_reste['reponses']['produit'] = produit
                st.session_state.entraineur_div_reste['etape'] = 3
                st.rerun()
            else:
                st.error("❌ Réessaye la multiplication")
    
    elif ex['etape'] == 3:
        produit = ex['reponses']['produit']
        st.success(f"✅ {diviseur} × {ex['reponses']['quotient']} = {produit}")
        st.write("---")
        st.write("### Étape 3 : Trouver le reste")
        st.write(f"On avait au départ : **{dividende}**")
        st.write(f"On a enlevé : **{produit}**")
        st.write(f"**Il reste : {dividende} - {produit} = ?**")
        
        # Visualisation
        st.write("**Imagine :**")
        st.write(f"🍬 {dividende} bonbons à partager en sachets de {ex['diviseur']}")
        st.write(f"📦 Tu as fait {ex['reponses']['quotient']} sachets complets")
        st.write(f"🍬 Il reste quelques bonbons non emballés")
        
        reponse = st.number_input("Reste:", min_value=0, max_value=20, key="div_reste_final")
        
        if st.button("✅ Vérifier", key="check_div_reste_3", use_container_width=True):
            if reponse == ex['reste_correct']:
                st.success(f"✅ Parfait! Reste = {reponse}")
                
                # Vérification finale
                st.write("---")
                st.write("### ✅ Vérification finale")
                st.write(f"({diviseur} × {ex['reponses']['quotient']}) + {reponse} = {produit} + {reponse} = {dividende} ✓")
                
                # Marquer terminé
                st.session_state.entraineur_div_reste['termine'] = True
                st.session_state.points += 40
                st.session_state.stats_par_niveau[st.session_state.niveau]['correct'] += 1
                st.session_state.stats_par_niveau[st.session_state.niveau]['total'] += 1

                # 🆕 ENREGISTRER DANS SYSTÈME ADAPTATIF
                if "profil" in st.session_state:
                    tracker = SkillTracker(st.session_state.profil)
                    tracker.record_exercise('division', True, difficulty=5)

                auto_save_profil(True)
                
                st.rerun()
            else:
                st.error(f"❌ Non, c'est {ex['reste_correct']}")
                st.info(f"💡 Calcule : {dividende} - {produit}")
def lancer_exercice_recommande(recommended_type):
    """
    Callback pour le bouton "Lancer cet exercice" du dashboard.
    Ce callback est exécuté AVANT le rerun, ce qui permet de modifier
    le session_state en toute sécurité.
    """
    # 1. Changer la catégorie active et la sélection du radio pour le prochain run
    st.session_state.active_category = "Exercice"
    st.session_state.main_radio = "Exercice"
    
    # 2. Générer le nouvel exercice
    if recommended_type == "addition":
        st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
    elif recommended_type == "soustraction":
        st.session_state.exercice_courant = generer_soustraction(st.session_state.niveau)
    elif recommended_type == "multiplication":
        st.session_state.exercice_courant = generer_tables(st.session_state.niveau)
    elif recommended_type == "division":
        st.session_state.exercice_courant = generer_division(st.session_state.niveau)
    elif recommended_type == "probleme":
        st.session_state.exercice_courant = generer_probleme(st.session_state.niveau)
    else: # Fallback
        st.session_state.exercice_courant = generer_addition(st.session_state.niveau)
    
    # 3. Réinitialiser le feedback pour le nouvel exercice
    st.session_state.show_feedback = False

def dashboard_statistiques():
    """Dashboard analytique enfant - Mes forces/faiblesses"""
    st.markdown('<div class="categorie-header">📊 Mes Statistiques</div>', unsafe_allow_html=True)
    
    if not st.session_state.get('authentifie', False):
        st.warning("Connecte-toi pour voir tes statistiques!")
        return
    
    # Charger le profil si absent
    if "profil" not in st.session_state:
        from utilisateur import charger_utilisateur, profil_par_defaut
        nom = st.session_state.get('utilisateur')
        profil = charger_utilisateur(nom)
        if profil is None:
            profil = profil_par_defaut()
        st.session_state['profil'] = profil
    
    profil = st.session_state.profil
    
    # Vérifier si exercise_history existe
    if 'exercise_history' not in profil:
        profil['exercise_history'] = []
        st.session_state['profil'] = profil
    
    # Initialiser système adaptatif
    adaptive = AdaptiveSystem()
    tracker = SkillTracker(profil)
    
    # Calculer compétences
    skill_levels = adaptive.get_skill_levels(profil.get('exercise_history', []))
    
    # Afficher profil
    st.subheader("Mon Profil d'Apprentissage")
    
    # ✅ AFFICHER TOUJOURS, même si vide
    has_data = profil.get('exercise_history') and len(profil.get('exercise_history', [])) > 0
    
    if not has_data:
        st.info("🎯 Tes statistiques apparaîtront après tes premiers exercices !")
    
    # Afficher les compétences (même à 0%)
    for ex_type, skill in skill_levels.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{ex_type.capitalize().replace('_', ' ')}**")
            st.progress(skill)
        with col2:
            if skill >= 0.7:
                emoji = "✅"
            elif skill >= 0.3:
                emoji = "💪"
            elif skill > 0:
                emoji = "📚"
            else:
                emoji = "⚪"  # Pas encore testé
            st.write(f"{emoji} {int(skill*100)}%")
    
    if not has_data:
        # Pas de recommandation si pas de données
        st.markdown("---")
        if st.button("🚀 Commencer les exercices", use_container_width=True):
            st.session_state.active_category = "Exercice"
            st.rerun()
        return
    
    st.markdown("---")
    
    # Domaines à travailler
    weak = tracker.get_weak_areas()
    if weak:
        st.subheader("⚠️ Domaines à Travailler")
        for area in weak:
            st.write(f"- {area.capitalize().replace('_', ' ')}")
    
    # Domaines maîtrisés
    strong = tracker.get_strong_areas()
    if strong:
        st.subheader("✅ Domaines Maîtrisés")
        for area in strong:
            st.write(f"- {area.capitalize().replace('_', ' ')}")
    
    st.markdown("---")
    
    # Recommandation
    recommended_type, reason = adaptive.recommend_exercise_type(skill_levels)
    
    st.subheader("🎯 Exercice Recommandé")
    st.info(reason)
    
    # Bouton avec génération d'exercice
    st.button(
        "🚀 Lancer cet exercice", 
        use_container_width=True, 
        key="launch_recommended",
        on_click=lancer_exercice_recommande, # ✅ Utilisation du callback
        args=(recommended_type,)             # ✅ Passer le type d'exercice en argument
    )


if __name__ == "__main__":
    main()
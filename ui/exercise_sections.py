"""
MathCopain - Exercise Sections & Callbacks  
Quick exercises, games, and daily challenges
Extracted from app.py during Phase 2 refactoring
"""

import streamlit as st
from datetime import date
from core import SkillTracker, exercise_generator

# Helper functions needed by callbacks
def maj_streak(correct):
    if correct:
        st.session_state.streak['current'] += 1
        st.session_state.streak['max'] = max(st.session_state.streak['current'], st.session_state.streak['max'])
    else:
        st.session_state.streak['current'] = 0

def calculer_bonus_streak(streak):
    """Calcule bonus selon streak (CACHÉ)"""
    if streak >= 10:
        return 25
    elif streak >= 5:
        return 10
    elif streak >= 3:
        return 5
    return 0

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

def auto_save_profil(succes):
    from datetime import datetime
    from utilisateur import sauvegarder_utilisateur
    
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
        from app import calculer_progression
        progression = calculer_progression(st.session_state.stats_par_niveau)
        profil["progression"] = progression
    sauvegarder_utilisateur(nom, profil)
    st.session_state["profil"] = profil

# =============== EXERCICE RAPIDE SECTION ===============
# Callbacks pour éliminer st.rerun()
# =============== EXERCICE RAPIDE SECTION ===============
# Callbacks pour éliminer st.rerun()
def _callback_exercice_addition():
    st.session_state.exercice_courant = exercise_generator.generer_addition(st.session_state.niveau)
    st.session_state.show_feedback = False
    st.session_state.exercise_start_time = __import__('time').time()  # Track start time

def _callback_exercice_soustraction():
    st.session_state.exercice_courant = exercise_generator.generer_soustraction(st.session_state.niveau)
    st.session_state.show_feedback = False
    st.session_state.exercise_start_time = __import__('time').time()

def _callback_exercice_tables():
    st.session_state.exercice_courant = exercise_generator.generer_tables(st.session_state.niveau)
    st.session_state.show_feedback = False
    st.session_state.exercise_start_time = __import__('time').time()

def _callback_exercice_division():
    st.session_state.exercice_courant = exercise_generator.generer_division(st.session_state.niveau)
    st.session_state.show_feedback = False
    st.session_state.exercise_start_time = __import__('time').time()

def _callback_validation_exercice():
    """Callback pour valider un exercice avec TransformativeFeedback"""
    import time

    ex = st.session_state.exercice_courant
    reponse = st.session_state.input_ex

    # Déterminer le type d'exercice
    if "+" in ex['question']:
        exercice_type = "addition"
    elif "-" in ex['question']:
        exercice_type = "subtraction"
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

    # ✅ Phase 6.1.4: Calculate time taken
    time_taken = None
    if st.session_state.exercise_start_time:
        time_taken = int(time.time() - st.session_state.exercise_start_time)

    # ✅ Phase 6.1.4: Generate TransformativeFeedback
    # Build user history from session state
    user_history = None
    if "profil" in st.session_state:
        profil = st.session_state.profil
        total = profil.get("exercices_totaux", 0)
        reussis = profil.get("exercices_reussis", 0)
        success_rate = reussis / total if total > 0 else 0.5
        user_history = {
            "success_rate": success_rate,
            "exercises_completed": total,
            "current_streak": st.session_state.streak.get('current', 0)
        }

    # Build exercise dictionary for FeedbackEngine
    exercise_dict = {
        "type": exercice_type,
        "operation": ex['question'],
        "difficulty": st.session_state.niveau,
        "expected_answer": ex['reponse']
    }

    # Extract operands from question if possible
    question_parts = ex['question'].replace('×', ' ').replace('+', ' ').replace('-', ' ').replace('÷', ' ').split()
    if len(question_parts) >= 2:
        try:
            exercise_dict["operand1"] = int(question_parts[0])
            exercise_dict["operand2"] = int(question_parts[1])
        except:
            pass

    # Generate transformative feedback
    feedback_engine = st.session_state.feedback_engine
    user_id = st.session_state.get('utilisateur', 'student_default')

    transformative_feedback = feedback_engine.process_exercise_response(
        exercise=exercise_dict,
        response=reponse,
        expected=ex['reponse'],
        user_id=user_id,
        user_history=user_history,
        time_taken_seconds=time_taken
    )

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
    st.session_state.transformative_feedback = transformative_feedback  # ✅ Store feedback
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
        st.session_state.exercice_courant = exercise_generator.generer_addition(st.session_state.niveau)
    elif exercice_type == "soustraction":
        st.session_state.exercice_courant = exercise_generator.generer_soustraction(st.session_state.niveau)
    elif exercice_type == "multiplication":
        st.session_state.exercice_courant = exercise_generator.generer_tables(st.session_state.niveau)
    elif exercice_type == "division":
        st.session_state.exercice_courant = exercise_generator.generer_division(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_exercice_suivant():
    """Callback pour passer à l'exercice suivant"""
    if "+" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = exercise_generator.generer_addition(st.session_state.niveau)
    elif "-" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = exercise_generator.generer_soustraction(st.session_state.niveau)
    elif "÷" in st.session_state.dernier_exercice.get('question', ''):
        st.session_state.exercice_courant = exercise_generator.generer_division(st.session_state.niveau)
    else:
        st.session_state.exercice_courant = exercise_generator.generer_tables(st.session_state.niveau)
    st.session_state.show_feedback = False

def render_transformative_feedback():
    """
    ✅ Phase 6.1.4: Render 6-layer TransformativeFeedback UI

    Displays:
    - Layer 1: Immediate (5 words emotional response)
    - Layer 2: Explanation (50 words pedagogical)
    - Layer 3: Strategy (alternative approach) - Expander
    - Layer 4: Remediation (exercises) - Info box
    - Layer 5: Encouragement (motivation)
    - Layer 6: Next Action (buttons)
    """
    if not st.session_state.get('transformative_feedback'):
        return

    feedback = st.session_state.transformative_feedback

    # Layer 1: Immediate Response
    st.markdown("---")
    if feedback.is_correct:
        bonus = calculer_bonus_streak(st.session_state.streak['current'])
        bonus_text = f" +{bonus} pts bonus!" if bonus > 0 else ""
        st.markdown(
            f'<div class="feedback-success">🎉 {feedback.immediate}{bonus_text}</div>',
            unsafe_allow_html=True
        )
        st.balloons()
    else:
        st.markdown(
            f'<div class="feedback-error">❌ {feedback.immediate}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Container for feedback layers
    with st.container(border=True):
        # Layer 2: Explanation
        st.markdown("### 📖 Explication")
        st.write(feedback.explanation)

        st.markdown("---")

        # Layer 3: Strategy (Expander)
        if feedback.strategy:
            with st.expander("💡 **Stratégie Alternative** - Clique pour voir", expanded=False):
                st.write(feedback.strategy)

        # Layer 4: Remediation (if error)
        if feedback.remediation:
            st.markdown("---")
            st.info("📚 **Recommandations pour progresser**")
            rem = feedback.remediation

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Type:** {rem.get('exercise_type', 'Pratique')}")
                st.write(f"**Niveau:** {rem.get('difficulty', st.session_state.niveau)}")
            with col2:
                st.write(f"**Exercices:** {rem.get('practice_count', 3)}")
                st.write(f"**Temps estimé:** ~{rem.get('estimated_time_minutes', 10)} min")

            if rem.get('focus_prerequisites'):
                st.write(f"**Points à réviser:** {', '.join(rem.get('focus_prerequisites', []))}")

        st.markdown("---")

        # Layer 5: Encouragement
        st.caption(f"✨ {feedback.encouragement}")

    # Layer 6: Next Action Buttons
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Refaire un similaire",
            key="btn_retry_trans",
            use_container_width=True,
            on_click=_callback_reessayer_exercice,
            help="Pratique un exercice similaire pour renforcer"
        ):
            pass

    with col2:
        if feedback.is_correct and st.session_state.get("profil", {}).get("exercices_reussis", 0) > 10:
            action_text = "⏭️ Niveau suivant"
        elif feedback.is_correct:
            action_text = "➡️ Continuer"
        else:
            action_text = "➡️ Suivant"

        if st.button(
            action_text,
            key="btn_next_trans",
            use_container_width=True,
            on_click=_callback_exercice_suivant,
            help=feedback.next_action
        ):
            pass

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
        # ✅ Phase 6.1.4: Use TransformativeFeedback UI
        if st.session_state.show_feedback and st.session_state.dernier_exercice:
            render_transformative_feedback()

# ================= SECTION JEUX ===================
# Callbacks pour jeux
def _callback_jeu_droite():
    st.session_state.jeu_type = 'droite'
    st.session_state.exercice_courant = exercise_generator.generer_droite_numerique(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_jeu_memory():
    st.session_state.jeu_type = 'memory'
    st.session_state.jeu_memory = exercise_generator.generer_memory_emoji(st.session_state.niveau)
    st.session_state.memory_first_flip = None
    st.session_state.memory_second_flip = None
    st.session_state.memory_incorrect_pair = None

def _callback_validation_droite():
    dn = st.session_state.exercice_courant
    reponse = st.session_state.slider_dn
    score, message = exercise_generator.calculer_score_droite(reponse, dn['nombre'])
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
    st.session_state.exercice_courant = exercise_generator.generer_droite_numerique(st.session_state.niveau)
    st.session_state.show_feedback = False

def _callback_nouvelle_partie_memory():
    st.session_state.jeu_memory = exercise_generator.generer_memory_emoji(st.session_state.niveau)
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
            st.write("⬇️ Déplace le curseur pour placer le nombre :")
            st.write("💡 **Astuce** : Essaye d'estimer où se trouve le nombre sans voir la valeur !")
            reponse = st.slider("Position", min_value=dn['min'], max_value=dn['max'], value=dn['max']//2, key="slider_dn", label_visibility="collapsed", format=" ")
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
        st.session_state.exercice_courant = exercise_generator.generer_probleme(st.session_state.niveau)
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
                    st.session_state.exercice_courant = exercise_generator.generer_probleme(st.session_state.niveau)
                    st.session_state.show_feedback = False
                    st.rerun()

# =============== MAIN =======================
# =============== MAIN =======================

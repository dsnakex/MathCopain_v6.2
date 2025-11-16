# ui_authentification.py
# 🎨 Interface authentification avec système de récupération PIN
# ✅ Question secrète + Code de récupération

import streamlit as st
from authentification import (
    creer_nouveau_compte,
    verifier_pin,
    charger_profil_utilisateur,
    lister_comptes_disponibles,
    QUESTIONS_SECRETES,
    obtenir_question_secrete,
    recuperer_pin_avec_question,
    recuperer_pin_avec_code
)

def ui_authentification():
    """Interface authentification - Affichée AVANT app principale"""

    st.title("🎓 MathCopain")
    st.markdown("## Calcul Mental sans Pression")
    st.markdown("---")

    # Initialize session state
    if 'authentifie' not in st.session_state:
        st.session_state.authentifie = False
    if 'utilisateur' not in st.session_state:
        st.session_state.utilisateur = None

    # DÉJÀ AUTHENTIFIÉ = Bouton "Changer de compte"
    if st.session_state.authentifie:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ Connecté: {st.session_state.utilisateur}")
        with col2:
            if st.button("🔄 Changer", use_container_width=True):
                st.session_state.authentifie = False
                st.session_state.utilisateur = None
                st.session_state.profil = None
                st.session_state.profil_charge = False
                st.rerun()

        # ✅ Charger profil COMPLET dans session_state
        if 'profil_charge' not in st.session_state or not st.session_state.profil_charge:
            profil = charger_profil_utilisateur(st.session_state.utilisateur)

            if profil:
                # Charger les valeurs individuelles
                st.session_state.niveau = profil.get('niveau', 'CE1')
                st.session_state.points = profil.get('points', 0)
                st.session_state.badges = profil.get('badges', [])

                # Stocker le profil COMPLET
                st.session_state.profil = profil
                st.session_state.profil_charge = True
            else:
                # Si pas de profil, créer un par défaut
                from utilisateur import profil_par_defaut
                profil_defaut = profil_par_defaut()
                st.session_state.profil = profil_defaut
                st.session_state.niveau = profil_defaut.get('niveau', 'CE1')
                st.session_state.points = profil_defaut.get('points', 0)
                st.session_state.badges = profil_defaut.get('badges', [])
                st.session_state.profil_charge = True

        return True  # Authentifié, continuer

    # PAS AUTHENTIFIÉ = Afficher interface login
    st.markdown("### 🔐 Authentification")

    tab1, tab2, tab3 = st.tabs(["🆕 Créer Compte", "📂 Se Connecter", "🔑 PIN oublié ?"])

    # ========================================================================
    # TAB 1: CRÉER COMPTE (avec question secrète + code récupération)
    # ========================================================================
    with tab1:
        st.write("**Nouveau compte?**")

        col1, col2 = st.columns(2)
        with col1:
            prenom_new = st.text_input("Votre prénom:", placeholder="Pierre", key="new_prenom")
        with col2:
            pin_new = st.text_input("PIN (4 chiffres):", placeholder="1234", key="new_pin", type="password")

        # ✅ NOUVEAU: Question secrète
        st.markdown("**🛡️ Pour récupérer ton PIN si tu l'oublies:**")
        question_index = st.selectbox(
            "Choisis une question secrète:",
            range(len(QUESTIONS_SECRETES)),
            format_func=lambda i: QUESTIONS_SECRETES[i],
            key="new_question"
        )

        reponse_secrete = st.text_input(
            "Ta réponse (à retenir!):",
            placeholder="ex: bleu, chat, vanille...",
            key="new_reponse",
            help="Retiens bien ta réponse, elle te permettra de récupérer ton PIN!"
        )

        if st.button("✅ Créer Compte", use_container_width=True, key="btn_create"):
            if not prenom_new:
                st.error("Entrez votre prénom!")
            elif not pin_new or len(pin_new) != 4 or not pin_new.isdigit():
                st.error("PIN doit être 4 chiffres!")
            elif not reponse_secrete or len(reponse_secrete.strip()) < 2:
                st.error("Réponse secrète trop courte (min 2 caractères)!")
            else:
                success, msg, code_recuperation = creer_nouveau_compte(
                    prenom_new,
                    pin_new,
                    question_index,
                    reponse_secrete
                )

                if success:
                    st.success(msg)

                    # ✅ AFFICHER CODE DE RÉCUPÉRATION (une seule fois!)
                    st.markdown("---")
                    st.warning("⚠️ **IMPORTANT: Note ce code de récupération!**")
                    st.markdown(f"### 🔢 Code: `{code_recuperation}`")
                    st.info(
                        "📝 **Garde ce code précieusement!**\n\n"
                        "Si tu oublies ton PIN ET ta réponse secrète, "
                        "ce code sera ton seul moyen de récupérer ton compte.\n\n"
                        "✍️ Note-le sur un papier et demande à un adulte de le garder."
                    )

                    # Petit délai pour laisser le temps de noter
                    st.markdown("---")
                    if st.button("✅ J'ai noté mon code, continuer →", use_container_width=True):
                        st.session_state.authentifie = True
                        st.session_state.utilisateur = prenom_new
                        st.session_state.profil_charge = False
                        st.rerun()
                else:
                    st.error(msg)

    # ========================================================================
    # TAB 2: SE CONNECTER
    # ========================================================================
    with tab2:
        st.write("**Compte existant?**")

        comptes = lister_comptes_disponibles()

        if comptes:
            prenom_existing = st.selectbox("Sélectionne ton compte:", comptes, key="existing_account")
            pin_existing = st.text_input("PIN:", placeholder="1234", key="existing_pin", type="password")

            if st.button("✅ Se Connecter", use_container_width=True, key="btn_login"):
                if not pin_existing:
                    st.error("Entrez votre PIN!")
                else:
                    success, msg = verifier_pin(prenom_existing, pin_existing)
                    if success:
                        st.success(msg)
                        st.session_state.authentifie = True
                        st.session_state.utilisateur = prenom_existing
                        st.session_state.profil_charge = False
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("Pas de compte. Crée-en un!")

    # ========================================================================
    # TAB 3: PIN OUBLIÉ (Récupération)
    # ========================================================================
    with tab3:
        st.markdown("### 🔑 Récupérer ton PIN")
        st.info(
            "Si tu as oublié ton PIN, tu peux le réinitialiser de **2 façons**:\n"
            "1. 💬 Répondre à ta question secrète\n"
            "2. 🔢 Utiliser ton code de récupération à 6 chiffres"
        )

        comptes = lister_comptes_disponibles()

        if not comptes:
            st.warning("Aucun compte existant. Crée un compte d'abord!")
        else:
            prenom_recuperation = st.selectbox(
                "Quel est ton prénom?",
                comptes,
                key="recuperation_account"
            )

            methode = st.radio(
                "Méthode de récupération:",
                ["💬 Question secrète", "🔢 Code de récupération"],
                key="methode_recuperation"
            )

            # ---- MÉTHODE 1: Question secrète ----
            if methode == "💬 Question secrète":
                # Obtenir la question
                success_q, question_ou_erreur = obtenir_question_secrete(prenom_recuperation)

                if success_q:
                    st.markdown(f"**Ta question:** {question_ou_erreur}")

                    reponse_user = st.text_input(
                        "Ta réponse:",
                        placeholder="ex: bleu, chat, vanille...",
                        key="reponse_recuperation"
                    )

                    nouveau_pin_q = st.text_input(
                        "Nouveau PIN (4 chiffres):",
                        placeholder="1234",
                        type="password",
                        key="nouveau_pin_q"
                    )

                    if st.button("✅ Réinitialiser PIN", use_container_width=True, key="btn_reset_question"):
                        if not reponse_user:
                            st.error("Entre ta réponse!")
                        elif not nouveau_pin_q or len(nouveau_pin_q) != 4:
                            st.error("Nouveau PIN doit être 4 chiffres!")
                        else:
                            success_reset, msg_reset = recuperer_pin_avec_question(
                                prenom_recuperation,
                                reponse_user,
                                nouveau_pin_q
                            )

                            if success_reset:
                                st.success(msg_reset)
                                st.balloons()
                                st.info("Tu peux maintenant te connecter avec ton nouveau PIN!")
                            else:
                                st.error(msg_reset)
                else:
                    st.error(question_ou_erreur)

            # ---- MÉTHODE 2: Code de récupération ----
            else:  # Code de récupération
                st.markdown("**Entre ton code de récupération à 6 chiffres**")
                st.caption("(Le code qui t'a été donné lors de la création du compte)")

                code_user = st.text_input(
                    "Code de récupération:",
                    placeholder="123456",
                    max_chars=6,
                    key="code_recuperation"
                )

                nouveau_pin_c = st.text_input(
                    "Nouveau PIN (4 chiffres):",
                    placeholder="1234",
                    type="password",
                    key="nouveau_pin_c"
                )

                if st.button("✅ Réinitialiser PIN", use_container_width=True, key="btn_reset_code"):
                    if not code_user or len(code_user) != 6:
                        st.error("Code de récupération doit être 6 chiffres!")
                    elif not nouveau_pin_c or len(nouveau_pin_c) != 4:
                        st.error("Nouveau PIN doit être 4 chiffres!")
                    else:
                        success_reset, msg_reset = recuperer_pin_avec_code(
                            prenom_recuperation,
                            code_user,
                            nouveau_pin_c
                        )

                        if success_reset:
                            st.success(msg_reset)
                            st.balloons()
                            st.info("Tu peux maintenant te connecter avec ton nouveau PIN!")
                        else:
                            st.error(msg_reset)

    return False  # Pas autorisé continuer


def verifier_authentification():
    """Vérifier si authentifié - appeler au top main()"""
    if not st.session_state.get('authentifie', False):
        ui_authentification()
        st.stop()  # Stop app.py, afficher juste auth

# ui_authentification.py
# 🎨 Interface authentification - VERSION CORRIGÉE
# Ajout du chargement complet du profil dans session_state

import streamlit as st
from authentification import (
    creer_nouveau_compte,
    verifier_pin,
    charger_profil_utilisateur,
    lister_comptes_disponibles
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
                st.session_state.profil = None  # ✅ RÉINITIALISER PROFIL
                st.session_state.profil_charge = False  # ✅ RÉINITIALISER FLAG
                st.rerun()
        
        # ✅ DEBUG : Charger profil COMPLET dans session_state
        if 'profil_charge' not in st.session_state or not st.session_state.profil_charge:
            profil = charger_profil_utilisateur(st.session_state.utilisateur)
            
            
            if profil:
                # Charger les valeurs individuelles (comme avant)
                st.session_state.niveau = profil.get('niveau', 'CE1')
                st.session_state.points = profil.get('points', 0)
                st.session_state.badges = profil.get('badges', [])
                
                # ✅ NOUVEAU : Stocker le profil COMPLET
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
    
    # PAS AUTHENTIFIÉ = Afficher interface login
    st.markdown("### 🔐 Authentification")
    
    tab1, tab2 = st.tabs(["🆕 Créer Compte", "📂 Se Connecter"])
    
    with tab1:
        st.write("**Nouveau compte?**")
        
        col1, col2 = st.columns(2)
        with col1:
            prenom_new = st.text_input("Votre prénom:", placeholder="Pierre", key="new_prenom")
        with col2:
            pin_new = st.text_input("PIN (4 chiffres):", placeholder="1234", key="new_pin", type="password")
        
        if st.button("✅ Créer Compte", use_container_width=True, key="btn_create"):
            if not prenom_new:
                st.error("Entrez votre prénom!")
            elif not pin_new or len(pin_new) != 4 or not pin_new.isdigit():
                st.error("PIN doit être 4 chiffres!")
            else:
                success, msg = creer_nouveau_compte(prenom_new, pin_new)
                if success:
                    st.success(msg)
                    st.session_state.authentifie = True
                    st.session_state.utilisateur = prenom_new
                    st.session_state.profil_charge = False  # ✅ Forcer rechargement
                    st.rerun()
                else:
                    st.error(msg)
    
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
                        st.session_state.profil_charge = False  # ✅ Forcer rechargement
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("Pas de compte. Crée-en un!")
    
    return False  # Pas autorisé continuer

def verifier_authentification():
    """Vérifier si authentifié - appeler au top main()"""
    if not st.session_state.get('authentifie', False):
        ui_authentification()
        st.stop()  # Stop app.py, afficher juste auth
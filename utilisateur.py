import json
import os
import streamlit as st
from datetime import datetime
from typing import Dict, Optional

FICHIER_UTILISATEURS = "utilisateurs.json"

# ✅ CACHE SINGLETON en mémoire
@st.cache_resource
def _get_user_cache() -> Dict:
    """
    Cache singleton partagé entre toutes les sessions
    Persiste tant que le serveur Streamlit tourne
    """
    return {"data": {}, "loaded": False, "dirty": False}

def _load_from_disk() -> Dict:
    """Charge fichier JSON depuis disque"""
    if not os.path.exists(FICHIER_UTILISATEURS):
        return {}

    try:
        with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_to_disk(data: Dict):
    """Sauvegarde cache vers fichier JSON"""
    try:
        with open(FICHIER_UTILISATEURS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Erreur sauvegarde : {e}")

def charger_utilisateur(nom: str) -> Optional[Dict]:
    """
    ✅ Charge utilisateur depuis cache mémoire
    Si cache vide, charge depuis disque UNE FOIS
    """
    cache = _get_user_cache()

    # Premier chargement : lire disque une fois
    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    # Retourner depuis cache mémoire
    return cache["data"].get(nom)

def sauvegarder_utilisateur(nom: str, data: Dict):
    """
    ✅ Sauvegarde en 2 étapes :
    1. Mise à jour immédiate en mémoire (instantané)
    2. Flush vers disque différé (toutes les 5 sauvegardes)
    """
    cache = _get_user_cache()

    # Charger si pas encore fait
    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    # ✅ Mise à jour immédiate en mémoire
    cache["data"][nom] = data
    cache["dirty"] = True

    # ✅ Compteur de sauvegardes différées
    if '_save_counter' not in st.session_state:
        st.session_state._save_counter = 0

    st.session_state._save_counter += 1

    # Flush vers disque toutes les 5 modifications OU à la déconnexion
    if st.session_state._save_counter >= 5:
        _save_to_disk(cache["data"])
        cache["dirty"] = False
        st.session_state._save_counter = 0

def obtenir_tous_eleves() -> list:
    """
    ✅ Retourne liste utilisateurs depuis cache mémoire
    """
    cache = _get_user_cache()

    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    return list(cache["data"].keys())

def force_save():
    """
    Force sauvegarde immédiate du cache vers disque
    À appeler lors de la déconnexion ou fermeture app
    """
    cache = _get_user_cache()

    if cache["dirty"]:
        _save_to_disk(cache["data"])
        cache["dirty"] = False

def profil_par_defaut():
    """Retourne un profil par défaut pour un nouvel utilisateur."""
    now = datetime.now()
    return {
        "niveau": "CE1",
        "points": 0,
        "badges": [],
        "exercices_reussis": 0,
        "exercices_totaux": 0,
        "taux_reussite": 0,
        "date_creation": now.strftime("%Y-%m-%d"),
        "date_derniere_session": now.strftime("%Y-%m-%dT%H:%M"),
        "progression": {"CE1": 0, "CE2": 0, "CM1": 0, "CM2": 0},
        "exercise_history": []
    }

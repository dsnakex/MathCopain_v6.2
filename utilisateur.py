"""
User Profile Management for MathCopain
Handles user data storage with Supabase (primary) and JSON file (fallback).
"""

import json
import os
import streamlit as st
from datetime import datetime
from typing import Dict, Optional

# Import Supabase client
from core.supabase_client import (
    is_supabase_configured,
    supabase_get_user_profile,
    supabase_save_user_profile,
    supabase_get_all_usernames,
    supabase_get_all_credentials
)

FICHIER_UTILISATEURS = "utilisateurs.json"


# =============================================================================
# STORAGE MODE DETECTION
# =============================================================================

def get_storage_mode() -> str:
    """
    Determine which storage backend to use.

    Returns:
        'supabase' if configured, 'json' otherwise
    """
    if is_supabase_configured():
        return 'supabase'
    return 'json'


# =============================================================================
# JSON FILE OPERATIONS (Fallback)
# =============================================================================

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


# =============================================================================
# MAIN API FUNCTIONS (Auto-switch between Supabase and JSON)
# =============================================================================

def charger_utilisateur(nom: str) -> Optional[Dict]:
    """
    Load user profile from storage.

    Args:
        nom: Username

    Returns:
        Profile dict or None if not found
    """
    storage_mode = get_storage_mode()
    nom_lower = nom.lower().strip()

    if storage_mode == 'supabase':
        # Try Supabase first
        profile = supabase_get_user_profile(nom_lower)
        if profile:
            return profile

        # Also check credentials table (profile_data field)
        from core.supabase_client import supabase_get_user_credentials
        creds = supabase_get_user_credentials(nom_lower)
        if creds and 'profil' in creds:
            return creds['profil']

        return None

    # JSON fallback
    cache = _get_user_cache()

    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    return cache["data"].get(nom_lower) or cache["data"].get(nom)


def sauvegarder_utilisateur(nom: str, data: Dict):
    """
    Save user profile to storage.

    Args:
        nom: Username
        data: Profile data dict
    """
    storage_mode = get_storage_mode()
    nom_lower = nom.lower().strip()

    if storage_mode == 'supabase':
        # Save to Supabase
        supabase_save_user_profile(nom_lower, data)

        # Also update credentials table if exists
        from core.supabase_client import supabase_get_user_credentials, supabase_save_user_credentials
        creds = supabase_get_user_credentials(nom_lower)
        if creds:
            creds['profil'] = data
            supabase_save_user_credentials(nom_lower, creds)
        return

    # JSON fallback
    cache = _get_user_cache()

    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    cache["data"][nom_lower] = data
    cache["dirty"] = True

    if '_save_counter' not in st.session_state:
        st.session_state._save_counter = 0

    st.session_state._save_counter += 1

    # Flush to disk every 5 modifications
    if st.session_state._save_counter >= 5:
        _save_to_disk(cache["data"])
        cache["dirty"] = False
        st.session_state._save_counter = 0


def obtenir_tous_eleves() -> list:
    """
    Get list of all usernames.

    Returns:
        List of usernames
    """
    storage_mode = get_storage_mode()

    if storage_mode == 'supabase':
        # Get from both tables and merge
        profile_users = supabase_get_all_usernames()
        creds = supabase_get_all_credentials()
        cred_users = list(creds.keys())

        # Merge and deduplicate
        all_users = list(set(profile_users + cred_users))
        return all_users

    # JSON fallback
    cache = _get_user_cache()

    if not cache["loaded"]:
        cache["data"] = _load_from_disk()
        cache["loaded"] = True

    return list(cache["data"].keys())


def force_save():
    """
    Force immediate save of cache to disk (JSON mode only).
    Call this on logout or app close.
    """
    storage_mode = get_storage_mode()

    if storage_mode == 'supabase':
        # Supabase saves immediately, nothing to do
        return

    cache = _get_user_cache()

    if cache["dirty"]:
        _save_to_disk(cache["data"])
        cache["dirty"] = False


def profil_par_defaut():
    """Return default profile for a new user."""
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


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def afficher_mode_stockage():
    """Display current storage mode (for debugging)."""
    mode = get_storage_mode()
    if mode == 'supabase':
        st.success("Stockage: Supabase (persistant)")
    else:
        st.warning("Stockage: Fichiers locaux (non persistant sur Streamlit Cloud)")

# authentification.py
# Module authentification sécurisé avec bcrypt et rate limiting
# Supporte Supabase (persistant) et JSON (fallback)

import json
import os
import random
import string
from datetime import datetime
from core.security import (
    hash_pin,
    authenticate_user,
    validate_pin_format,
    validate_username_format
)
import bcrypt

# Import Supabase client
from core.supabase_client import (
    is_supabase_configured,
    supabase_get_user_credentials,
    supabase_save_user_credentials,
    supabase_get_all_credentials,
    supabase_delete_user_credentials,
    supabase_user_exists
)

FICHIER_USERS = 'utilisateurs_securises.json'


# ============================================================================
# STORAGE MODE DETECTION
# ============================================================================

def get_storage_mode() -> str:
    """Determine which storage backend to use."""
    if is_supabase_configured():
        return 'supabase'
    return 'json'


# ============================================================================
# QUESTIONS SECRÈTES pour récupération PIN
# ============================================================================

QUESTIONS_SECRETES = [
    "Quelle est ta couleur préférée ?",
    "Quel est ton animal préféré ?",
    "Quelle est ta glace préférée ?",
    "Quel est ton dessin animé préféré ?",
    "Quel est ton sport préféré ?",
    "Quelle est ta saison préférée (hiver, printemps, été, automne) ?",
]


def generer_code_recuperation() -> str:
    """Générer code de récupération aléatoire (6 chiffres)"""
    return ''.join(random.choices(string.digits, k=6))


def hasher_reponse_secrete(reponse: str) -> str:
    """Hasher réponse à la question secrète (comme PIN)"""
    reponse_normalisee = reponse.lower().strip()
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(reponse_normalisee.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verifier_reponse_secrete(reponse: str, hashed_reponse: str) -> bool:
    """Vérifier réponse secrète contre son hash"""
    try:
        reponse_normalisee = reponse.lower().strip()
        return bcrypt.checkpw(
            reponse_normalisee.encode('utf-8'),
            hashed_reponse.encode('utf-8')
        )
    except:
        return False


# ============================================================================
# JSON FILE MANAGEMENT (Fallback)
# ============================================================================

def init_fichier_securise():
    """Créer fichier sécurisé s'il existe pas (JSON mode only)"""
    if get_storage_mode() == 'json':
        if not os.path.exists(FICHIER_USERS):
            with open(FICHIER_USERS, 'w') as f:
                json.dump({}, f)


def _charger_json():
    """Charger tous utilisateurs depuis fichier JSON"""
    try:
        with open(FICHIER_USERS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def _sauvegarder_json(data):
    """Sauvegarder tous utilisateurs vers JSON"""
    try:
        with open(FICHIER_USERS, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        return False


# ============================================================================
# UNIFIED STORAGE API
# ============================================================================

def charger_utilisateurs_securises():
    """Charger tous utilisateurs depuis le storage actif"""
    if get_storage_mode() == 'supabase':
        return supabase_get_all_credentials()
    return _charger_json()


def sauvegarder_utilisateurs_securises(data):
    """Sauvegarder tous utilisateurs (JSON mode only, Supabase saves individually)"""
    if get_storage_mode() == 'supabase':
        # In Supabase mode, we save individually, so this is a no-op
        # The data should already be saved
        return True
    return _sauvegarder_json(data)


def _get_user(cle: str):
    """Get single user credentials"""
    if get_storage_mode() == 'supabase':
        return supabase_get_user_credentials(cle)
    tous = _charger_json()
    return tous.get(cle)


def _save_user(cle: str, user_data: dict):
    """Save single user credentials"""
    if get_storage_mode() == 'supabase':
        return supabase_save_user_credentials(cle, user_data)
    tous = _charger_json()
    tous[cle] = user_data
    return _sauvegarder_json(tous)


def _delete_user(cle: str):
    """Delete single user"""
    if get_storage_mode() == 'supabase':
        return supabase_delete_user_credentials(cle)
    tous = _charger_json()
    if cle in tous:
        del tous[cle]
        return _sauvegarder_json(tous)
    return False


def _user_exists(cle: str) -> bool:
    """Check if user exists"""
    if get_storage_mode() == 'supabase':
        return supabase_user_exists(cle)
    tous = _charger_json()
    return cle in tous


# ============================================================================
# CRÉATION COMPTE (avec question secrète + code récupération)
# ============================================================================

def creer_nouveau_compte(prenom, pin, question_index, reponse_secrete):
    """
    Créer compte nouvel enfant avec PIN + système de récupération.

    Returns:
        (success, message, code_recuperation)
    """
    # Valider username avec pydantic
    is_valid_username, error_username = validate_username_format(prenom)
    if not is_valid_username:
        return False, f"Prénom invalide: {error_username}", None

    # Valider PIN avec pydantic
    is_valid_pin, error_pin = validate_pin_format(pin)
    if not is_valid_pin:
        return False, f"PIN invalide: {error_pin}", None

    # Valider question index
    if not (0 <= question_index < len(QUESTIONS_SECRETES)):
        return False, "Question secrète invalide", None

    # Valider réponse secrète
    if not reponse_secrete or len(reponse_secrete.strip()) < 2:
        return False, "Réponse secrète trop courte (min 2 caractères)", None

    # Clé = prénom minuscule
    cle = prenom.lower().strip()

    # Vérifier pas déjà existe
    if _user_exists(cle):
        return False, f"Compte {prenom} existe déjà", None

    # Hasher PIN avec bcrypt
    try:
        hashed_pin = hash_pin(pin)
    except Exception as e:
        return False, f"Erreur hashing PIN: {e}", None

    # Hasher réponse secrète
    hashed_reponse = hasher_reponse_secrete(reponse_secrete)

    # Générer code de récupération
    code_recuperation = generer_code_recuperation()

    # Créer structure profil
    profil_initial = {
        "niveau": "CE1",
        "points": 0,
        "badges": [],
        "exercices_reussis": 0,
        "exercices_totaux": 0,
        "taux_reussite": 0,
        "date_creation": str(datetime.now()),
        "date_derniere_session": str(datetime.now()),
        "progression": {"CE1": 0, "CE2": 0, "CM1": 0, "CM2": 0}
    }

    # Créer structure utilisateur
    user_data = {
        "pin": hashed_pin,
        "prenom_affichage": prenom,
        "profil": profil_initial,
        "question_secrete": {
            "question_index": question_index,
            "question_text": QUESTIONS_SECRETES[question_index],
            "reponse_hashed": hashed_reponse
        },
        "code_recuperation": code_recuperation
    }

    # Sauvegarder
    success = _save_user(cle, user_data)

    if success:
        return True, f"Compte {prenom} créé avec succès!", code_recuperation
    else:
        return False, "Erreur création compte", None


# ============================================================================
# AUTHENTIFICATION
# ============================================================================

def verifier_pin(prenom, pin):
    """
    Vérifier PIN = authentifier utilisateur.

    Returns:
        (success, message)
    """
    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False, f"Compte {prenom} introuvable"

    hashed_pin = compte.get('pin')

    if not hashed_pin:
        return False, "Compte corrompu (PIN manquant)"

    # Authentification sécurisée avec bcrypt + rate limiting
    return authenticate_user(prenom, pin, hashed_pin)


# ============================================================================
# RÉCUPÉRATION PIN
# ============================================================================

def obtenir_question_secrete(prenom):
    """
    Obtenir question secrète pour un utilisateur

    Returns:
        (success, question_text or error_message)
    """
    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False, f"Compte {prenom} introuvable"

    question_data = compte.get('question_secrete')

    if not question_data:
        return False, "Système de récupération non configuré pour ce compte"

    return True, question_data['question_text']


def recuperer_pin_avec_question(prenom, reponse_secrete, nouveau_pin):
    """
    Réinitialiser PIN avec réponse à la question secrète

    Returns:
        (success, message)
    """
    # Valider nouveau PIN
    is_valid_pin, error_pin = validate_pin_format(nouveau_pin)
    if not is_valid_pin:
        return False, f"Nouveau PIN invalide: {error_pin}"

    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False, f"Compte {prenom} introuvable"

    question_data = compte.get('question_secrete')

    if not question_data:
        return False, "Système de récupération non configuré"

    # Vérifier réponse secrète
    if not verifier_reponse_secrete(reponse_secrete, question_data['reponse_hashed']):
        return False, "Réponse incorrecte"

    # Réponse correcte → Réinitialiser PIN
    try:
        nouveau_hashed_pin = hash_pin(nouveau_pin)
        compte['pin'] = nouveau_hashed_pin

        if _save_user(cle, compte):
            return True, f"PIN réinitialisé avec succès pour {prenom}!"
        else:
            return False, "Erreur lors de la sauvegarde"
    except Exception as e:
        return False, f"Erreur: {e}"


def recuperer_pin_avec_code(prenom, code_recuperation, nouveau_pin):
    """
    Réinitialiser PIN avec code de récupération

    Returns:
        (success, message)
    """
    # Valider nouveau PIN
    is_valid_pin, error_pin = validate_pin_format(nouveau_pin)
    if not is_valid_pin:
        return False, f"Nouveau PIN invalide: {error_pin}"

    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False, f"Compte {prenom} introuvable"

    code_stocke = compte.get('code_recuperation')

    if not code_stocke:
        return False, "Pas de code de récupération pour ce compte"

    # Vérifier code (comparaison stricte)
    if code_recuperation.strip() != code_stocke:
        return False, "Code de récupération incorrect"

    # Code correct → Réinitialiser PIN
    try:
        nouveau_hashed_pin = hash_pin(nouveau_pin)
        compte['pin'] = nouveau_hashed_pin

        if _save_user(cle, compte):
            return True, f"PIN réinitialisé avec succès pour {prenom}!"
        else:
            return False, "Erreur lors de la sauvegarde"
    except Exception as e:
        return False, f"Erreur: {e}"


# ============================================================================
# PROFIL MANAGEMENT
# ============================================================================

def charger_profil_utilisateur(prenom):
    """Charger profil utilisateur SEULEMENT après auth"""
    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return None

    return compte.get('profil')


def sauvegarder_profil_utilisateur(prenom, profil):
    """Sauvegarder profil utilisateur après exercice"""
    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False

    # Mettre à jour juste profil (PIN reste inchangé!)
    compte['profil'] = profil
    compte['profil']['date_derniere_session'] = str(datetime.now())

    return _save_user(cle, compte)


def lister_comptes_disponibles():
    """Lister SEULEMENT prénoms affichage (pas PINs!)"""
    tous = charger_utilisateurs_securises()
    return [compte.get('prenom_affichage', cle) for cle, compte in tous.items()]


def supprimer_compte(prenom, pin):
    """
    Supprimer compte (protection: besoin PIN).

    Returns:
        success (bool)
    """
    cle = prenom.lower().strip()
    compte = _get_user(cle)

    if not compte:
        return False

    # Vérifier PIN avec bcrypt (double protection)
    hashed_pin = compte.get('pin')
    if not hashed_pin:
        return False

    success, _ = authenticate_user(prenom, pin, hashed_pin)
    if not success:
        return False

    # Supprimer
    return _delete_user(cle)

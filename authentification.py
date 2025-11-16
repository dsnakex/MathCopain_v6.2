# authentification.py
# 🔐 Module authentification sécurisé avec bcrypt et rate limiting
# ✅ Ajout système de récupération de PIN (question secrète + code de récupération)

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

FICHIER_USERS = 'utilisateurs_securises.json'

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
    """
    Générer code de récupération aléatoire (6 chiffres)

    Returns:
        Code à 6 chiffres (ex: "482756")
    """
    return ''.join(random.choices(string.digits, k=6))


def hasher_reponse_secrete(reponse: str) -> str:
    """
    Hasher réponse à la question secrète (comme PIN)

    Args:
        reponse: Réponse en clair (normalisée: lowercase, strip)

    Returns:
        Hash bcrypt de la réponse
    """
    reponse_normalisee = reponse.lower().strip()
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(reponse_normalisee.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verifier_reponse_secrete(reponse: str, hashed_reponse: str) -> bool:
    """
    Vérifier réponse secrète contre son hash

    Args:
        reponse: Réponse en clair
        hashed_reponse: Hash stocké

    Returns:
        True si match, False sinon
    """
    try:
        reponse_normalisee = reponse.lower().strip()
        return bcrypt.checkpw(
            reponse_normalisee.encode('utf-8'),
            hashed_reponse.encode('utf-8')
        )
    except:
        return False


# ============================================================================
# FICHIER MANAGEMENT
# ============================================================================

def init_fichier_securise():
    """Créer fichier sécurisé s'il existe pas"""
    if not os.path.exists(FICHIER_USERS):
        with open(FICHIER_USERS, 'w') as f:
            json.dump({}, f)


def charger_utilisateurs_securises():
    """Charger tous utilisateurs depuis fichier sécurisé"""
    try:
        with open(FICHIER_USERS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def sauvegarder_utilisateurs_securises(data):
    """Sauvegarder tous utilisateurs"""
    try:
        with open(FICHIER_USERS, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        return False


# ============================================================================
# CRÉATION COMPTE (avec question secrète + code récupération)
# ============================================================================

def creer_nouveau_compte(prenom, pin, question_index, reponse_secrete):
    """
    Créer compte nouvel enfant avec PIN + système de récupération.

    Args:
        prenom: Prénom de l'enfant
        pin: PIN à 4 chiffres
        question_index: Index de la question secrète choisie (0-5)
        reponse_secrete: Réponse à la question secrète

    Returns:
        (success, message, code_recuperation)
        code_recuperation est retourné seulement si success=True
    """
    # ✅ Valider username avec pydantic
    is_valid_username, error_username = validate_username_format(prenom)
    if not is_valid_username:
        return False, f"Prénom invalide: {error_username}", None

    # ✅ Valider PIN avec pydantic
    is_valid_pin, error_pin = validate_pin_format(pin)
    if not is_valid_pin:
        return False, f"PIN invalide: {error_pin}", None

    # Valider question index
    if not (0 <= question_index < len(QUESTIONS_SECRETES)):
        return False, "Question secrète invalide", None

    # Valider réponse secrète
    if not reponse_secrete or len(reponse_secrete.strip()) < 2:
        return False, "Réponse secrète trop courte (min 2 caractères)", None

    # Charger tous
    tous = charger_utilisateurs_securises()

    # Clé = prénom minuscule (pour éviter doublons "Pierre" vs "pierre")
    cle = prenom.lower().strip()

    # Vérifier pas déjà existe
    if cle in tous:
        return False, f"Compte {prenom} existe déjà", None

    # ✅ Hasher PIN avec bcrypt
    try:
        hashed_pin = hash_pin(pin)
    except Exception as e:
        return False, f"Erreur hashing PIN: {e}", None

    # ✅ Hasher réponse secrète
    hashed_reponse = hasher_reponse_secrete(reponse_secrete)

    # ✅ Générer code de récupération
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

    # ✅ Ajouter avec PIN hashé + système récupération
    tous[cle] = {
        "pin": hashed_pin,  # ✅ Stocké hashé, plus en clair !
        "prenom_affichage": prenom,  # Garder affichage original
        "profil": profil_initial,
        # ✅ NOUVEAU: Système de récupération
        "question_secrete": {
            "question_index": question_index,
            "question_text": QUESTIONS_SECRETES[question_index],
            "reponse_hashed": hashed_reponse
        },
        "code_recuperation": code_recuperation  # Stocké en clair (usage unique)
    }

    # Sauvegarder
    success = sauvegarder_utilisateurs_securises(tous)

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
    ✅ Utilise bcrypt + rate limiting

    Args:
        prenom: Prénom de l'utilisateur
        pin: PIN à vérifier

    Returns:
        (success, message)
    """
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False, f"Compte {prenom} introuvable"

    compte = tous[cle]
    hashed_pin = compte.get('pin')

    if not hashed_pin:
        return False, "Compte corrompu (PIN manquant)"

    # ✅ Authentification sécurisée avec bcrypt + rate limiting
    return authenticate_user(prenom, pin, hashed_pin)


# ============================================================================
# RÉCUPÉRATION PIN
# ============================================================================

def obtenir_question_secrete(prenom):
    """
    Obtenir question secrète pour un utilisateur

    Args:
        prenom: Prénom de l'utilisateur

    Returns:
        (success, question_text or error_message)
    """
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False, f"Compte {prenom} introuvable"

    compte = tous[cle]
    question_data = compte.get('question_secrete')

    if not question_data:
        return False, "Système de récupération non configuré pour ce compte"

    return True, question_data['question_text']


def recuperer_pin_avec_question(prenom, reponse_secrete, nouveau_pin):
    """
    Réinitialiser PIN avec réponse à la question secrète

    Args:
        prenom: Prénom de l'utilisateur
        reponse_secrete: Réponse à la question secrète
        nouveau_pin: Nouveau PIN à 4 chiffres

    Returns:
        (success, message)
    """
    # Valider nouveau PIN
    is_valid_pin, error_pin = validate_pin_format(nouveau_pin)
    if not is_valid_pin:
        return False, f"Nouveau PIN invalide: {error_pin}"

    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False, f"Compte {prenom} introuvable"

    compte = tous[cle]
    question_data = compte.get('question_secrete')

    if not question_data:
        return False, "Système de récupération non configuré"

    # Vérifier réponse secrète
    if not verifier_reponse_secrete(reponse_secrete, question_data['reponse_hashed']):
        return False, "Réponse incorrecte"

    # Réponse correcte → Réinitialiser PIN
    try:
        nouveau_hashed_pin = hash_pin(nouveau_pin)
        tous[cle]['pin'] = nouveau_hashed_pin

        if sauvegarder_utilisateurs_securises(tous):
            return True, f"PIN réinitialisé avec succès pour {prenom}!"
        else:
            return False, "Erreur lors de la sauvegarde"
    except Exception as e:
        return False, f"Erreur: {e}"


def recuperer_pin_avec_code(prenom, code_recuperation, nouveau_pin):
    """
    Réinitialiser PIN avec code de récupération

    Args:
        prenom: Prénom de l'utilisateur
        code_recuperation: Code de récupération à 6 chiffres
        nouveau_pin: Nouveau PIN à 4 chiffres

    Returns:
        (success, message)
    """
    # Valider nouveau PIN
    is_valid_pin, error_pin = validate_pin_format(nouveau_pin)
    if not is_valid_pin:
        return False, f"Nouveau PIN invalide: {error_pin}"

    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False, f"Compte {prenom} introuvable"

    compte = tous[cle]
    code_stocke = compte.get('code_recuperation')

    if not code_stocke:
        return False, "Pas de code de récupération pour ce compte"

    # Vérifier code (comparaison stricte)
    if code_recuperation.strip() != code_stocke:
        return False, "Code de récupération incorrect"

    # Code correct → Réinitialiser PIN
    try:
        nouveau_hashed_pin = hash_pin(nouveau_pin)
        tous[cle]['pin'] = nouveau_hashed_pin

        if sauvegarder_utilisateurs_securises(tous):
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
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return None

    return tous[cle]['profil']


def sauvegarder_profil_utilisateur(prenom, profil):
    """Sauvegarder profil utilisateur après exercice"""
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False

    # Mettre à jour juste profil (PIN reste inchangé!)
    tous[cle]['profil'] = profil
    tous[cle]['profil']['date_derniere_session'] = str(datetime.now())

    return sauvegarder_utilisateurs_securises(tous)


def lister_comptes_disponibles():
    """Lister SEULEMENT prénoms affichage (pas PINs!)"""
    tous = charger_utilisateurs_securises()
    # Retourner juste prénoms, PAS les clés
    return [compte['prenom_affichage'] for compte in tous.values()]


def supprimer_compte(prenom, pin):
    """
    Supprimer compte (protection: besoin PIN).
    ✅ Vérification bcrypt avant suppression

    Args:
        prenom: Prénom de l'utilisateur
        pin: PIN de confirmation

    Returns:
        success (bool)
    """
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()

    if cle not in tous:
        return False

    # ✅ Vérifier PIN avec bcrypt (double protection)
    hashed_pin = tous[cle].get('pin')
    if not hashed_pin:
        return False

    success, _ = authenticate_user(prenom, pin, hashed_pin)
    if not success:
        return False

    # Supprimer
    del tous[cle]
    return sauvegarder_utilisateurs_securises(tous)

# authentification.py
# 🔐 Module authentification sécurisé avec bcrypt et rate limiting
# Utilise core/security.py pour protection avancée

import json
import os
from datetime import datetime
from core.security import (
    hash_pin,
    authenticate_user,
    validate_pin_format,
    validate_username_format
)

FICHIER_USERS = 'utilisateurs_securises.json'


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


def creer_nouveau_compte(prenom, pin):
    """
    Créer compte nouvel enfant avec PIN.

    Args:
        prenom: Prénom de l'enfant
        pin: PIN à 4 chiffres

    Returns:
        (success, message)
    """
    # ✅ Valider username avec pydantic
    is_valid_username, error_username = validate_username_format(prenom)
    if not is_valid_username:
        return False, f"Prénom invalide: {error_username}"

    # ✅ Valider PIN avec pydantic
    is_valid_pin, error_pin = validate_pin_format(pin)
    if not is_valid_pin:
        return False, f"PIN invalide: {error_pin}"

    # Charger tous
    tous = charger_utilisateurs_securises()

    # Clé = prénom minuscule (pour éviter doublons "Pierre" vs "pierre")
    cle = prenom.lower().strip()

    # Vérifier pas déjà existe
    if cle in tous:
        return False, f"Compte {prenom} existe déjà"

    # ✅ Hasher PIN avec bcrypt
    try:
        hashed_pin = hash_pin(pin)
    except Exception as e:
        return False, f"Erreur hashing PIN: {e}"

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

    # ✅ Ajouter avec PIN hashé
    tous[cle] = {
        "pin": hashed_pin,  # ✅ Stocké hashé, plus en clair !
        "prenom_affichage": prenom,  # Garder affichage original
        "profil": profil_initial
    }

    # Sauvegarder
    success = sauvegarder_utilisateurs_securises(tous)

    if success:
        return True, f"Compte {prenom} créé avec succès!"
    else:
        return False, "Erreur création compte"


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

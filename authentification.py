# authentification.py
# 🔐 Module authentification sécurisé
# ZÉRO modification app.py - Fichier 100% nouveau

import json
import os
from datetime import datetime

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
    """Créer compte nouvel enfant avec PIN"""
    # Valider PIN (4 chiffres)
    if not pin.isdigit() or len(pin) != 4:
        return False, "PIN doit être 4 chiffres"
    
    # Charger tous
    tous = charger_utilisateurs_securises()
    
    # Clé = prénom minuscule (pour éviter doublons "Pierre" vs "pierre")
    cle = prenom.lower().strip()
    
    # Vérifier pas déjà existe
    if cle in tous:
        return False, f"Compte {prenom} existe déjà"
    
    # Créer structure
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
    
    # Ajouter avec PIN
    tous[cle] = {
        "pin": pin,
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
    """Vérifier PIN = authentifier utilisateur"""
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()
    
    if cle not in tous:
        return False, f"Compte {prenom} introuvable"
    
    compte = tous[cle]
    
    if compte.get('pin') != pin:
        return False, "PIN incorrect"
    
    return True, "Authentifié!"

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
    """Supprimer compte (protection: besoin PIN)"""
    tous = charger_utilisateurs_securises()
    cle = prenom.lower().strip()
    
    if cle not in tous:
        return False
    
    # Vérifier PIN (double protection)
    if tous[cle]['pin'] != pin:
        return False
    
    # Supprimer
    del tous[cle]
    return sauvegarder_utilisateurs_securises(tous)

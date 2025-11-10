import json
import os
from datetime import datetime

FICHIER_UTILISATEURS = "utilisateurs.json"

def charger_utilisateur(nom):
    """Charge les données d'un utilisateur depuis le fichier utilisateurs.json."""
    if not os.path.exists(FICHIER_UTILISATEURS):
        return None
    with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(nom)

def sauvegarder_utilisateur(nom, data):
    """Sauvegarde ou met à jour les données d'un utilisateur dans le fichier utilisateurs.json."""
    all_data = {}
    if os.path.exists(FICHIER_UTILISATEURS):
        with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = {}
    all_data[nom] = data
    with open(FICHIER_UTILISATEURS, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def obtenir_tous_eleves():
    """Retourne la liste de tous les noms d'utilisateurs existants."""
    if not os.path.exists(FICHIER_UTILISATEURS):
        return []
    with open(FICHIER_UTILISATEURS, "r", encoding="utf-8") as f:
        data = json.load(f)
    # ✅ CORRECTION : Retourner les clés, pas "utilisateurs.get(nom)"
    return list(data.keys())

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
        # ✅ CORRECTION : Virgule manquante ligne 48
        "exercise_history": []  # ✅ IMPORTANT pour le système adaptatif
    }
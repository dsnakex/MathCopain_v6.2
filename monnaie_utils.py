"""
monnaie_utils.py
Exercices pour apprendre à rendre la monnaie CE2-CM2
SANS DÉCIMAUX - utilise euros et centimes séparés
"""

import random
import streamlit as st
from typing import Dict, List, Tuple

# ========================================
# DONNÉES DE BASE
# ========================================

# Pièces et billets disponibles (en centimes)
PIECES_BILLETS = [
    (5000, "billet de 50€"),
    (2000, "billet de 20€"),
    (1000, "billet de 10€"),
    (500, "billet de 5€"),
    (200, "pièce de 2€"),
    (100, "pièce de 1€"),
    (50, "pièce de 50 centimes"),
    (20, "pièce de 20 centimes"),
    (10, "pièce de 10 centimes"),
    (5, "pièce de 5 centimes"),
    (2, "pièce de 2 centimes"),
    (1, "pièce de 1 centime")
]

CONTEXTES_ACHATS = {
    "CE2": [
        ("pain", (100, 300)),          # 1-3€
        ("bonbon", (20, 100)),         # 0.20-1€
        ("cahier", (150, 300)),        # 1.50-3€
        ("stylo", (80, 200)),          # 0.80-2€
        ("gomme", (50, 150)),          # 0.50-1.50€
    ],
    "CM1": [
        ("livre", (500, 1500)),        # 5-15€
        ("jeu", (800, 2000)),          # 8-20€
        ("puzzle", (600, 1200)),       # 6-12€
        ("ballon", (400, 1000)),       # 4-10€
        ("peluche", (700, 1800)),      # 7-18€
    ],
    "CM2": [
        ("jeu vidéo", (2000, 5000)),   # 20-50€
        ("vêtement", (1500, 4000)),    # 15-40€
        ("jouet", (1800, 4500)),       # 18-45€
        ("livre", (1200, 3000)),       # 12-30€
        ("BD", (1000, 2500)),          # 10-25€
    ]
}

# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def centimes_vers_euros_texte(centimes: int) -> str:
    """
    Convertit centimes en texte lisible SANS notation décimale

    Exemples:
        520 → "5 euros et 20 centimes"
        500 → "5 euros"
        75 → "75 centimes"
    """
    euros = centimes // 100
    cents = centimes % 100

    if euros > 0 and cents > 0:
        return f"{euros} euro{'s' if euros > 1 else ''} et {cents} centime{'s' if cents > 1 else ''}"
    elif euros > 0:
        return f"{euros} euro{'s' if euros > 1 else ''}"
    else:
        return f"{cents} centime{'s' if cents > 1 else ''}"

def calculer_pieces_optimales(montant_centimes: int) -> List[Tuple[int, str, int]]:
    """
    Calcule le nombre optimal de pièces/billets pour un montant

    Returns:
        Liste de tuples (valeur_centimes, nom, quantité)
    """
    resultat = []
    reste = montant_centimes

    for valeur, nom in PIECES_BILLETS:
        if reste >= valeur:
            quantite = reste // valeur
            resultat.append((valeur, nom, quantite))
            reste = reste % valeur

    return resultat

# ========================================
# GÉNÉRATEURS D'EXERCICES
# ========================================

def generer_calcul_rendu(niveau: str) -> Dict:
    """
    Exercice : Calculer combien rendre
    """
    # Choisir contexte selon niveau
    articles = CONTEXTES_ACHATS.get(niveau, CONTEXTES_ACHATS["CE2"])
    article, (prix_min, prix_max) = random.choice(articles)

    # Générer prix (en centimes)
    if niveau == "CE2":
        # CE2 : Euros entiers ou demi-euros (50 centimes)
        prix = random.choice([
            random.randint(1, 10) * 100,  # Euros entiers
            random.randint(1, 8) * 100 + 50  # X euros et 50 centimes
        ])
    elif niveau == "CM1":
        # CM1 : Multiples de 10 centimes
        euros = random.randint(prix_min // 100, prix_max // 100)
        centimes = random.choice([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        prix = euros * 100 + centimes
    else:  # CM2
        # CM2 : N'importe quel montant
        prix = random.randint(prix_min, prix_max)

    # Choisir billet pour payer (arrondi supérieur)
    euros_prix = (prix + 99) // 100  # Arrondi supérieur

    if niveau == "CE2":
        billets_possibles = [5, 10, 20]
        billet_paye = next(b for b in billets_possibles if b >= euros_prix)
    elif niveau == "CM1":
        billets_possibles = [5, 10, 20, 50]
        billet_paye = next((b for b in billets_possibles if b >= euros_prix), 50)
    else:  # CM2
        billets_possibles = [5, 10, 20, 50]
        billet_paye = random.choice([b for b in billets_possibles if b >= euros_prix])

    montant_paye = billet_paye * 100
    rendu = montant_paye - prix

    return {
        'article': article,
        'prix_centimes': prix,
        'prix_texte': centimes_vers_euros_texte(prix),
        'paye_centimes': montant_paye,
        'paye_texte': centimes_vers_euros_texte(montant_paye),
        'reponse_centimes': rendu,
        'reponse_texte': centimes_vers_euros_texte(rendu),
        'question': f"Tu achètes un(e) {article} à {centimes_vers_euros_texte(prix)}. Tu payes avec {centimes_vers_euros_texte(montant_paye)}. Combien te rend-on ?"
    }

def generer_composition_monnaie(niveau: str) -> Dict:
    """
    Exercice : Donner la composition en pièces/billets
    """
    # Montant à composer
    if niveau == "CE2":
        # CE2 : Montants simples
        montant = random.choice([
            100, 200, 500,  # 1€, 2€, 5€
            150, 250, 350,  # 1.50€, 2.50€, 3.50€
        ])
    elif niveau == "CM1":
        # CM1 : Montants moyens
        montant = random.randint(50, 1000)
        montant = (montant // 10) * 10  # Arrondi à 10 centimes
    else:  # CM2
        # CM2 : Montants variés
        montant = random.randint(20, 2000)

    composition = calculer_pieces_optimales(montant)

    return {
        'montant_centimes': montant,
        'montant_texte': centimes_vers_euros_texte(montant),
        'composition': composition,
        'question': f"Avec quelles pièces et billets peux-tu faire {centimes_vers_euros_texte(montant)} ?"
    }

def generer_probleme_realiste(niveau: str) -> Dict:
    """
    Exercice : Problème réaliste avec plusieurs achats
    """
    if niveau == "CE2":
        # CE2 : 2 articles simples
        article1 = random.choice(["pain", "bonbon", "gomme"])
        article2 = random.choice(["cahier", "stylo", "crayon"])
        prix1 = random.randint(1, 3) * 100  # 1-3€
        prix2 = random.randint(1, 4) * 100  # 1-4€

        total = prix1 + prix2
        paye = ((total + 99) // 500 + 1) * 500  # Arrondi au billet de 5€ supérieur
        rendu = paye - total

        question = f"Tu achètes un(e) {article1} à {centimes_vers_euros_texte(prix1)} et un(e) {article2} à {centimes_vers_euros_texte(prix2)}. Tu payes avec {centimes_vers_euros_texte(paye)}. Combien te rend-on ?"

    elif niveau == "CM1":
        # CM1 : 3 articles
        articles = random.sample(["livre", "stylo", "cahier", "gomme", "règle"], 3)
        prix = [random.randint(1, 8) * 100 + random.choice([0, 50]) for _ in range(3)]

        total = sum(prix)
        paye = ((total + 99) // 1000 + 1) * 1000  # Arrondi au billet de 10€ supérieur
        rendu = paye - total

        details = ", ".join([f"{articles[i]} ({centimes_vers_euros_texte(prix[i])})" for i in range(3)])
        question = f"Tu achètes : {details}. Total : {centimes_vers_euros_texte(total)}. Tu payes avec {centimes_vers_euros_texte(paye)}. Combien te rend-on ?"

    else:  # CM2
        # CM2 : Problème avec réduction
        article = random.choice(["jeu vidéo", "livre", "BD"])
        prix_initial = random.randint(20, 40) * 100
        reduction = random.choice([5, 10]) * 100  # 5€ ou 10€ de réduction
        prix_final = prix_initial - reduction

        paye = ((prix_final + 99) // 2000 + 1) * 2000  # Arrondi au billet de 20€ supérieur
        rendu = paye - prix_final

        question = f"Un(e) {article} coûte {centimes_vers_euros_texte(prix_initial)}. Il y a une réduction de {centimes_vers_euros_texte(reduction)}. Prix final : {centimes_vers_euros_texte(prix_final)}. Tu payes avec {centimes_vers_euros_texte(paye)}. Combien te rend-on ?"
        total = prix_final

    return {
        'total_centimes': total,
        'total_texte': centimes_vers_euros_texte(total),
        'paye_centimes': paye,
        'paye_texte': centimes_vers_euros_texte(paye),
        'reponse_centimes': rendu,
        'reponse_texte': centimes_vers_euros_texte(rendu),
        'question': question
    }

# ========================================
# FONCTIONS VISUELLES
# ========================================

@st.cache_data
def dessiner_pieces_monnaie(composition: List[Tuple[int, str, int]]) -> str:
    """
    Génère HTML pour afficher visuellement les pièces et billets
    """
    html_parts = ['<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">']

    # Couleurs selon valeur
    couleurs = {
        5000: "#8B7355",  # Billet 50€ - Orange
        2000: "#6495ED",  # Billet 20€ - Bleu
        1000: "#DC143C",  # Billet 10€ - Rouge
        500: "#9370DB",   # Billet 5€ - Gris
        200: "#FFD700",   # 2€ - Or
        100: "#FFD700",   # 1€ - Or
        50: "#FFD700",    # 50c - Or
        20: "#FFD700",    # 20c - Or
        10: "#FFD700",    # 10c - Or
        5: "#CD7F32",     # 5c - Bronze
        2: "#CD7F32",     # 2c - Bronze
        1: "#CD7F32",     # 1c - Bronze
    }

    for valeur, nom, quantite in composition:
        couleur = couleurs.get(valeur, "#DDD")

        # Billets (rectangles) ou pièces (cercles)
        if valeur >= 500:
            # Billet
            for _ in range(quantite):
                html_parts.append(f'''
                <div style="
                    width: 80px;
                    height: 50px;
                    background: {couleur};
                    border: 2px solid #333;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                ">
                    {valeur // 100}€
                </div>
                ''')
        else:
            # Pièce
            for _ in range(quantite):
                texte = f"{valeur // 100}€" if valeur >= 100 else f"{valeur}c"
                html_parts.append(f'''
                <div style="
                    width: 50px;
                    height: 50px;
                    background: {couleur};
                    border: 3px solid #8B6914;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #333;
                    font-weight: bold;
                    font-size: 12px;
                ">
                    {texte}
                </div>
                ''')

    html_parts.append('</div>')
    return ''.join(html_parts)

@st.cache_data
def expliquer_calcul_rendu(prix: int, paye: int, rendu: int) -> str:
    """
    Génère explication pédagogique pour le calcul de rendu
    """
    explication = f"### 💡 Méthode pour calculer le rendu\n\n"

    explication += f"**Étape 1 : On a payé**\n"
    explication += f"→ {centimes_vers_euros_texte(paye)}\n\n"

    explication += f"**Étape 2 : L'achat coûte**\n"
    explication += f"→ {centimes_vers_euros_texte(prix)}\n\n"

    explication += f"**Étape 3 : On calcule la différence**\n"
    explication += f"→ {centimes_vers_euros_texte(paye)} - {centimes_vers_euros_texte(prix)}\n\n"

    # Calcul détaillé euros et centimes séparément
    euros_paye = paye // 100
    cents_paye = paye % 100
    euros_prix = prix // 100
    cents_prix = prix % 100
    euros_rendu = rendu // 100
    cents_rendu = rendu % 100

    if cents_paye >= cents_prix:
        explication += f"**Calcul détaillé :**\n"
        explication += f"- Euros : {euros_paye} - {euros_prix} = {euros_rendu}\n"
        explication += f"- Centimes : {cents_paye} - {cents_prix} = {cents_rendu}\n\n"
    else:
        explication += f"**Calcul avec emprunt :**\n"
        explication += f"- On ne peut pas faire {cents_paye} - {cents_prix}\n"
        explication += f"- On emprunte 1 euro = 100 centimes\n"
        explication += f"- Centimes : {cents_paye + 100} - {cents_prix} = {cents_rendu}\n"
        explication += f"- Euros : {euros_paye - 1} - {euros_prix} = {euros_rendu}\n\n"

    explication += f"✅ **Rendu à donner : {centimes_vers_euros_texte(rendu)}**"

    return explication

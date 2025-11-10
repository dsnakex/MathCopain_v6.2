"""
proportionnalite_utils.py
Exercices de proportionnalité CM1-CM2
"""

import random

# ========================================
# GÉNÉRATEURS D'EXERCICES
# ========================================

def generer_tableau_proportionnalite(niveau):
    """
    Compléter un tableau de proportionnalité
    CM1 : Tableaux simples (×2, ×3, ×5)
    CM2 : Tableaux plus complexes
    """
    
    if niveau == "CM1":
        # Coefficients simples
        coeff = random.choice([2, 3, 4, 5])
        nb_colonnes = 3
    else:  # CM2
        coeff = random.choice([2, 3, 4, 5, 6, 7, 8])
        nb_colonnes = 4
    
    # Générer valeurs ligne 1
    ligne1 = [random.randint(1, 10) for _ in range(nb_colonnes)]
    ligne2 = [x * coeff for x in ligne1]
    
    # Choisir une case à trouver (pas la première)
    index_manquant = random.randint(1, nb_colonnes - 1)
    valeur_manquante = ligne2[index_manquant]
    
    return {
        'ligne1': ligne1,
        'ligne2': ligne2,
        'index_manquant': index_manquant,
        'reponse': valeur_manquante,
        'coefficient': coeff,
        'question': f"Complète le tableau (case {index_manquant + 1})"
    }


def generer_regle_de_trois(niveau):
    """
    Problème de règle de trois
    CM1 : Situations simples (prix, quantités)
    CM2 : Plus variées
    """
    
    situations_cm1 = [
        {
            'contexte': "3 croissants coûtent {prix1} €. Combien coûtent {qte2} croissants ?",
            'qte1': 3,
            'type': 'prix'
        },
        {
            'contexte': "5 pommes pèsent {poids1} kg. Combien pèsent {qte2} pommes ?",
            'qte1': 5,
            'type': 'poids'
        },
        {
            'contexte': "{qte1} tickets coûtent {prix1} €. Combien coûtent {qte2} tickets ?",
            'qte1': random.randint(2, 5),
            'type': 'prix'
        }
    ]
    
    situations_cm2 = situations_cm1 + [
        {
            'contexte': "Une voiture consomme {conso1} L pour {dist1} km. Combien pour {dist2} km ?",
            'qte1': random.randint(30, 100),
            'type': 'consommation'
        },
        {
            'contexte': "{qte1} m de tissu coûtent {prix1} €. Combien coûtent {qte2} m ?",
            'qte1': random.randint(2, 8),
            'type': 'prix'
        }
    ]
    
    if niveau == "CM1":
        situation = random.choice(situations_cm1)
    else:
        situation = random.choice(situations_cm2)
    
    qte1 = situation['qte1']
    qte2 = random.randint(qte1 + 1, qte1 * 3)
    
    # Générer prix/poids selon contexte
    if situation['type'] == 'prix':
        valeur1 = qte1 * random.randint(2, 5)  # Prix unitaire entre 2 et 5€
        valeur2 = (valeur1 / qte1) * qte2
    elif situation['type'] == 'poids':
        valeur1 = round(qte1 * random.uniform(0.2, 0.5), 1)
        valeur2 = round((valeur1 / qte1) * qte2, 1)
    else:  # consommation
        valeur1 = random.randint(3, 8)
        valeur2 = round((valeur1 / qte1) * qte2, 1)
    
    # Formater contexte
    if 'prix1' in situation['contexte']:
        question = situation['contexte'].format(prix1=valeur1, qte2=qte2)
    elif 'poids1' in situation['contexte']:
        question = situation['contexte'].format(poids1=valeur1, qte2=qte2)
    elif 'conso1' in situation['contexte']:
        question = situation['contexte'].format(conso1=valeur1, dist1=qte1, dist2=qte2)
    else:
        question = situation['contexte']
    
    return {
        'question': question,
        'qte1': qte1,
        'valeur1': valeur1,
        'qte2': qte2,
        'reponse': round(valeur2, 2),
        'type': situation['type']
    }


def generer_pourcentage_simple(niveau):
    """
    Calculs de pourcentages simples
    CM2 uniquement : 10%, 25%, 50%, 75%
    """
    
    pourcentages = [10, 25, 50, 75]
    pourcent = random.choice(pourcentages)
    
    # Nombre de base
    if pourcent == 10:
        nombre = random.randint(20, 200)
    elif pourcent == 25:
        nombre = random.choice([20, 40, 60, 80, 100, 120, 160, 200])
    elif pourcent == 50:
        nombre = random.randint(20, 200)
    else:  # 75%
        nombre = random.choice([20, 40, 60, 80, 100, 120, 160, 200])
    
    resultat = (nombre * pourcent) / 100
    
    contextes = [
        f"Une réduction de {pourcent}% sur {nombre} €",
        f"{pourcent}% de {nombre} élèves",
        f"{pourcent}% d'un gâteau de {nombre} g",
        f"Une augmentation de {pourcent}% sur {nombre} €"
    ]
    
    contexte = random.choice(contextes)
    
    return {
        'contexte': contexte,
        'nombre': nombre,
        'pourcentage': pourcent,
        'reponse': resultat,
        'question': f"Calcule {pourcent}% de {nombre}"
    }


def generer_echelle(niveau):
    """
    Problèmes d'échelles
    CM2 uniquement
    """
    
    echelles = [
        (1, 10, "1 cm représente 10 cm"),
        (1, 100, "1 cm représente 1 m"),
        (1, 1000, "1 cm représente 10 m"),
        (1, 10000, "1 cm représente 100 m")
    ]
    
    echelle_num, echelle_denom, description = random.choice(echelles)
    
    # Distance sur le plan
    distance_plan = random.randint(2, 12)
    distance_reelle = distance_plan * echelle_denom
    
    # Choisir sens de la question
    if random.choice([True, False]):
        # Plan → Réalité
        question = f"Sur un plan à l'échelle 1/{echelle_denom}, une distance mesure {distance_plan} cm. Quelle est la distance réelle ?"
        reponse = distance_reelle
        unite_reponse = "cm" if echelle_denom <= 100 else "m"
        if echelle_denom >= 100:
            reponse = reponse / 100  # Convertir en mètres
    else:
        # Réalité → Plan
        question = f"Sur un plan à l'échelle 1/{echelle_denom}, quelle longueur représente {distance_reelle} cm réels ?"
        reponse = distance_plan
        unite_reponse = "cm"
    
    return {
        'question': question,
        'echelle': f"1/{echelle_denom}",
        'reponse': reponse,
        'unite': unite_reponse,
        'description': description
    }


def generer_vitesse(niveau):
    """
    Problèmes vitesse/distance/temps
    CM2 uniquement
    """
    
    # Vitesses réalistes
    vitesses = [
        (60, "voiture en ville"),
        (90, "voiture sur route"),
        (20, "vélo"),
        (5, "marche à pied"),
        (30, "trottinette")
    ]
    
    vitesse, contexte = random.choice(vitesses)
    
    # Choisir type de question
    type_q = random.choice(['distance', 'temps'])
    
    if type_q == 'distance':
        # Calculer distance
        temps = random.randint(1, 4)  # heures
        distance = vitesse * temps
        question = f"Une {contexte} roule à {vitesse} km/h pendant {temps} heure{'s' if temps > 1 else ''}. Quelle distance parcourt-elle ?"
        reponse = distance
        unite = "km"
    else:
        # Calculer temps
        temps = random.randint(1, 4)
        distance = vitesse * temps
        question = f"Une {contexte} parcourt {distance} km à {vitesse} km/h. Combien de temps met-elle ?"
        reponse = temps
        unite = "h"
    
    return {
        'question': question,
        'vitesse': vitesse,
        'reponse': reponse,
        'unite': unite,
        'type': type_q
    }


# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def expliquer_regle_de_trois(qte1, valeur1, qte2, valeur2):
    """
    Génère explication pédagogique règle de trois
    """
    
    prix_unitaire = valeur1 / qte1
    
    explication = f"### 💡 Méthode de la règle de trois\n\n"
    explication += f"**Étape 1 : Trouver le prix/valeur pour 1**\n"
    explication += f"- {qte1} → {valeur1}\n"
    explication += f"- 1 → {valeur1} ÷ {qte1} = {prix_unitaire:.2f}\n\n"
    
    explication += f"**Étape 2 : Multiplier par la nouvelle quantité**\n"
    explication += f"- 1 → {prix_unitaire:.2f}\n"
    explication += f"- {qte2} → {prix_unitaire:.2f} × {qte2} = **{valeur2:.2f}**\n\n"
    
    explication += f"✅ **Résultat : {valeur2:.2f}**"
    
    return explication


def expliquer_pourcentage(nombre, pourcentage, resultat):
    """
    Explication calcul pourcentage
    """
    
    explication = f"### 💡 Calculer {pourcentage}% de {nombre}\n\n"
    
    if pourcentage == 10:
        explication += f"**Astuce** : 10% = diviser par 10\n"
        explication += f"{nombre} ÷ 10 = **{resultat}**"
    elif pourcentage == 25:
        explication += f"**Astuce** : 25% = diviser par 4\n"
        explication += f"{nombre} ÷ 4 = **{resultat}**"
    elif pourcentage == 50:
        explication += f"**Astuce** : 50% = diviser par 2\n"
        explication += f"{nombre} ÷ 2 = **{resultat}**"
    elif pourcentage == 75:
        explication += f"**Astuce** : 75% = 50% + 25%\n"
        explication += f"- 50% de {nombre} = {nombre / 2}\n"
        explication += f"- 25% de {nombre} = {nombre / 4}\n"
        explication += f"- Total = {nombre / 2} + {nombre / 4} = **{resultat}**"
    else:
        explication += f"**Méthode générale** : ({nombre} × {pourcentage}) ÷ 100\n"
        explication += f"= {nombre * pourcentage} ÷ 100 = **{resultat}**"
    
    return explication
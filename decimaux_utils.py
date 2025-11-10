"""
decimaux_utils.py
Exercices sur les nombres décimaux CM1-CM2
"""

import random

# ========================================
# GÉNÉRATEURS D'EXERCICES
# ========================================

def generer_droite_decimale(niveau):
    """
    Placer un nombre décimal sur une droite graduée
    CM1 : entre 0 et 10
    CM2 : entre 0 et 100
    """
    
    if niveau == "CM1":
        # Nombres entre 0 et 10 avec 1 décimale
        nombre = round(random.uniform(0.5, 9.5), 1)
        min_val, max_val = 0, 10
        precision = 0.1
    else:  # CM2
        # Nombres entre 0 et 100 avec 2 décimales
        nombre = round(random.uniform(1, 99), 2)
        min_val, max_val = 0, 100
        precision = 0.1
    
    return {
        'nombre': nombre,
        'min': min_val,
        'max': max_val,
        'precision': precision,
        'question': f"Place {nombre} sur la droite"
    }


def generer_comparaison_decimaux(niveau):
    """
    Comparer deux nombres décimaux
    CM1 : 1 décimale
    CM2 : 2 décimales
    """
    
    if niveau == "CM1":
        a = round(random.uniform(1, 20), 1)
        b = round(random.uniform(1, 20), 1)
        while a == b:
            b = round(random.uniform(1, 20), 1)
    else:  # CM2
        a = round(random.uniform(1, 50), 2)
        b = round(random.uniform(1, 50), 2)
        while a == b:
            b = round(random.uniform(1, 50), 2)
    
    if a < b:
        reponse = '<'
        explication = f"{a} est plus petit que {b}"
    elif a > b:
        reponse = '>'
        explication = f"{a} est plus grand que {b}"
    else:
        reponse = '='
        explication = f"{a} est égal à {b}"
    
    return {
        'a': a,
        'b': b,
        'reponse': reponse,
        'explication': explication,
        'question': f"Compare {a} et {b}"
    }


def generer_addition_decimaux(niveau):
    """
    Addition de nombres décimaux
    CM1 : 1 décimale, résultat < 50
    CM2 : 2 décimales, résultat < 100
    """
    
    if niveau == "CM1":
        a = round(random.uniform(2, 15), 1)
        b = round(random.uniform(2, 15), 1)
        reponse = round(a + b, 1)
    else:  # CM2
        a = round(random.uniform(5, 30), 2)
        b = round(random.uniform(5, 30), 2)
        reponse = round(a + b, 2)
    
    return {
        'a': a,
        'b': b,
        'reponse': reponse,
        'operation': '+',
        'question': f"{a} + {b} = ?"
    }


def generer_soustraction_decimaux(niveau):
    """
    Soustraction de nombres décimaux
    CM1 : 1 décimale
    CM2 : 2 décimales
    """
    
    if niveau == "CM1":
        a = round(random.uniform(10, 25), 1)
        b = round(random.uniform(2, a - 1), 1)
        reponse = round(a - b, 1)
    else:  # CM2
        a = round(random.uniform(20, 60), 2)
        b = round(random.uniform(5, a - 2), 2)
        reponse = round(a - b, 2)
    
    return {
        'a': a,
        'b': b,
        'reponse': reponse,
        'operation': '-',
        'question': f"{a} - {b} = ?"
    }


def generer_multiplication_par_10_100(niveau):
    """
    Multiplier/diviser par 10, 100, 1000
    CM2 uniquement
    """
    
    operation = random.choice(['multiplication', 'division'])
    multiplicateur = random.choice([10, 100, 1000])
    
    if operation == 'multiplication':
        nombre = round(random.uniform(1.5, 25), 2)
        reponse = round(nombre * multiplicateur, 2)
        symbole = '×'
    else:  # division
        nombre = round(random.uniform(50, 500), 2)
        reponse = round(nombre / multiplicateur, 3)
        symbole = '÷'
    
    return {
        'nombre': nombre,
        'multiplicateur': multiplicateur,
        'reponse': reponse,
        'operation': operation,
        'symbole': symbole,
        'question': f"{nombre} {symbole} {multiplicateur} = ?"
    }


def generer_fraction_vers_decimal(niveau):
    """
    Convertir fraction décimale en nombre décimal
    CM1-CM2
    """
    
    # Fractions décimales simples
    fractions = [
        (1, 2, 0.5),
        (1, 4, 0.25),
        (3, 4, 0.75),
        (1, 10, 0.1),
        (3, 10, 0.3),
        (5, 10, 0.5),
        (7, 10, 0.7),
        (1, 5, 0.2),
        (2, 5, 0.4),
        (3, 5, 0.6),
        (4, 5, 0.8),
    ]
    
    if niveau == "CM2":
        # Ajouter fractions plus complexes
        fractions.extend([
            (1, 100, 0.01),
            (25, 100, 0.25),
            (50, 100, 0.5),
            (75, 100, 0.75),
        ])
    
    num, denom, decimal = random.choice(fractions)
    
    return {
        'numerateur': num,
        'denominateur': denom,
        'reponse': decimal,
        'question': f"Convertis {num}/{denom} en nombre décimal"
    }


# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def calculer_score_decimal(reponse, correct, tolerance=0.1):
    """
    Calcule le score selon la précision
    """
    distance = abs(reponse - correct)
    
    if distance == 0:
        return 30, "Parfait !"
    elif distance <= tolerance:
        return 20, "Très proche !"
    elif distance <= tolerance * 2:
        return 10, "Pas mal"
    else:
        return 0, f"Trop loin (écart: {distance:.2f})"


def expliquer_comparaison_decimaux(a, b):
    """
    Génère une explication pédagogique pour comparer décimaux
    """
    
    # Séparer partie entière et décimale
    a_entier, a_decimal = str(a).split('.')
    b_entier, b_decimal = str(b).split('.')
    
    explication = f"### 💡 Méthode de comparaison\n\n"
    
    # Étape 1 : Comparer parties entières
    explication += f"**Étape 1 : Parties entières**\n"
    explication += f"- {a} → partie entière : {a_entier}\n"
    explication += f"- {b} → partie entière : {b_entier}\n\n"
    
    if int(a_entier) != int(b_entier):
        if int(a_entier) > int(b_entier):
            explication += f"✅ {a_entier} > {b_entier}, donc **{a} > {b}**\n"
        else:
            explication += f"✅ {a_entier} < {b_entier}, donc **{a} < {b}**\n"
    else:
        # Étape 2 : Comparer parties décimales
        explication += f"Les parties entières sont égales ({a_entier} = {b_entier})\n\n"
        explication += f"**Étape 2 : Parties décimales**\n"
        explication += f"- {a} → partie décimale : 0,{a_decimal}\n"
        explication += f"- {b} → partie décimale : 0,{b_decimal}\n\n"
        
        # Comparer chiffre par chiffre
        max_len = max(len(a_decimal), len(b_decimal))
        a_decimal_pad = a_decimal.ljust(max_len, '0')
        b_decimal_pad = b_decimal.ljust(max_len, '0')
        
        explication += f"Comparons chiffre par chiffre : {a_decimal_pad} vs {b_decimal_pad}\n"
        
        if a_decimal_pad > b_decimal_pad:
            explication += f"✅ {a_decimal_pad} > {b_decimal_pad}, donc **{a} > {b}**\n"
        elif a_decimal_pad < b_decimal_pad:
            explication += f"✅ {a_decimal_pad} < {b_decimal_pad}, donc **{a} < {b}**\n"
        else:
            explication += f"✅ {a_decimal_pad} = {b_decimal_pad}, donc **{a} = {b}**\n"
    
    return explication


def expliquer_addition_decimaux(a, b, resultat):
    """
    Explication pédagogique addition décimaux
    """
    
    explication = f"### 💡 Méthode\n\n"
    explication += f"**{a} + {b}**\n\n"
    explication += f"**Étape 1 : Aligner les virgules**\n"
    explication += f"```\n"
    explication += f"  {a:>6}\n"
    explication += f"+ {b:>6}\n"
    explication += f"--------\n"
    explication += f"  {resultat:>6}\n"
    explication += f"```\n\n"
    explication += f"**Étape 2 : Additionner comme des entiers**\n"
    explication += f"- On additionne les chiffres colonne par colonne\n"
    explication += f"- On garde la virgule au même endroit\n\n"
    explication += f"✅ **Résultat : {resultat}**"
    
    return explication
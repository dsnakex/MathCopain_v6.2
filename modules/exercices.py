"""
Générateurs d'exercices MathCopain
Fonctions pour créer exercices de calcul mental
"""

import random
from typing import Dict

def generer_addition(niveau: str) -> Dict:
    """Génère exercice d'addition selon niveau"""
    if niveau == "CE1":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif niveau == "CE2":
        a, b = random.randint(10, 50), random.randint(10, 50)
    elif niveau == "CM1":
        a, b = random.randint(50, 100), random.randint(50, 100)
    else:
        a, b = random.randint(100, 200), random.randint(100, 200)
    return {'question': f"{a} + {b}", 'reponse': a + b}

def generer_soustraction(niveau: str) -> Dict:
    """Génère exercice de soustraction selon niveau"""
    if niveau == "CE1":
        a, b = random.randint(10, 20), random.randint(1, 10)
    elif niveau == "CE2":
        a, b = random.randint(50, 100), random.randint(10, 50)
    elif niveau == "CM1":
        a, b = random.randint(100, 500), random.randint(50, 100)
    else:
        a, b = random.randint(500, 1000), random.randint(100, 500)
    return {'question': f"{a} - {b}", 'reponse': a - b}

def generer_tables(niveau: str) -> Dict:
    """Génère exercice de multiplication (tables) selon niveau"""
    if niveau == "CE1":
        table, mult = random.randint(2, 5), random.randint(1, 10)
    elif niveau == "CE2":
        table, mult = random.randint(2, 9), random.randint(1, 10)
    elif niveau == "CM1":
        table, mult = random.randint(1, 12), random.randint(1, 12)
    else:
        table, mult = random.randint(1, 15), random.randint(1, 15)
    return {'question': f"{table} × {mult}", 'reponse': table * mult}

def generer_division(niveau: str) -> Dict:
    """Génère exercice de division selon niveau"""
    if niveau == "CE1":
        # CE1 : pas encore de divisions, fallback sur tables
        return generer_tables(niveau)

    elif niveau == "CE2":
        # CE2 : divisions simples (quotient exact)
        quotient = random.randint(2, 9)
        diviseur = random.randint(2, 5)
        dividende = quotient * diviseur

    elif niveau == "CM1":
        # CM1 : divisions plus grandes, avec ou sans reste
        if random.random() < 0.7:  # 70% sans reste
            quotient = random.randint(3, 12)
            diviseur = random.randint(2, 9)
            dividende = quotient * diviseur
        else:  # 30% avec reste
            diviseur = random.randint(3, 7)
            quotient = random.randint(3, 9)
            reste = random.randint(1, diviseur - 1)
            dividende = (quotient * diviseur) + reste

    else:  # CM2
        # CM2 : divisions complexes, souvent avec reste
        if random.random() < 0.5:  # 50% sans reste
            quotient = random.randint(5, 15)
            diviseur = random.randint(3, 12)
            dividende = quotient * diviseur
        else:  # 50% avec reste
            diviseur = random.randint(4, 9)
            quotient = random.randint(4, 12)
            reste = random.randint(1, diviseur - 1)
            dividende = (quotient * diviseur) + reste

    return {'question': f"{dividende} ÷ {diviseur}", 'reponse': dividende // diviseur, 'reste': dividende % diviseur}

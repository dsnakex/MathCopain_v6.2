"""
division_utils.py
Utilitaires pour générer des divisions guidées
"""
import random

def generer_division_simple(niveau):
    """
    Génère une division avec quotient exact (pas de reste)
    """
    if niveau == "CE2":
        # CE2 : divisions très simples
        quotient = random.randint(2, 5)
        diviseur = random.randint(2, 5)
    elif niveau == "CM1":
        # CM1 : divisions moyennes
        quotient = random.randint(3, 9)
        diviseur = random.randint(2, 7)
    else:  # CM2
        # CM2 : divisions plus complexes
        quotient = random.randint(5, 12)
        diviseur = random.randint(3, 9)
    
    dividende = quotient * diviseur
    
    return {
        'dividende': dividende,
        'diviseur': diviseur,
        'quotient': quotient,
        'reste': 0
    }

def generer_division_reste(niveau):
    """
    Génère une division avec reste
    """
    if niveau == "CM1":
        diviseur = random.randint(3, 7)
        quotient = random.randint(3, 8)
        reste = random.randint(1, diviseur - 1)
    else:  # CM2
        diviseur = random.randint(4, 9)
        quotient = random.randint(4, 12)
        reste = random.randint(1, diviseur - 1)
    
    dividende = (quotient * diviseur) + reste
    
    return {
        'dividende': dividende,
        'diviseur': diviseur,
        'quotient': quotient,
        'reste': reste
    }
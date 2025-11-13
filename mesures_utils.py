"""
mesures_utils.py
Exercices de mesures et conversions CE1-CM2
"""

import random
import streamlit as st

# ========================================
# GÉNÉRATEURS D'EXERCICES
# ========================================

def generer_conversion_longueur(niveau):
    """
    Conversions de longueurs
    CE1-CE2 : cm ↔ m
    CM1 : mm ↔ cm ↔ m
    CM2 : mm ↔ cm ↔ m ↔ km
    """
    
    if niveau in ["CE1", "CE2"]:
        # cm ↔ m
        conversions = [
            ("cm", "m", 100, random.randint(100, 500)),
            ("m", "cm", 1/100, random.randint(1, 10))
        ]
    elif niveau == "CM1":
        # mm ↔ cm ↔ m
        conversions = [
            ("mm", "cm", 10, random.randint(50, 500)),
            ("cm", "mm", 1/10, random.randint(5, 50)),
            ("cm", "m", 100, random.randint(100, 800)),
            ("m", "cm", 1/100, random.randint(2, 20))
        ]
    else:  # CM2
        # Toutes conversions
        conversions = [
            ("mm", "cm", 10, random.randint(50, 500)),
            ("cm", "mm", 1/10, random.randint(5, 50)),
            ("cm", "m", 100, random.randint(100, 800)),
            ("m", "cm", 1/100, random.randint(2, 20)),
            ("m", "km", 1000, random.randint(1000, 5000)),
            ("km", "m", 1/1000, random.randint(2, 15))
        ]
    
    unite_depart, unite_arrivee, diviseur, valeur_depart = random.choice(conversions)
    
    # Calculer réponse
    if diviseur < 1:
        valeur_arrivee = valeur_depart / diviseur
    else:
        valeur_arrivee = valeur_depart / diviseur
    
    return {
        'valeur_depart': valeur_depart,
        'unite_depart': unite_depart,
        'unite_arrivee': unite_arrivee,
        'reponse': valeur_arrivee,
        'diviseur': diviseur,
        'question': f"Convertis {valeur_depart} {unite_depart} en {unite_arrivee}"
    }


def generer_conversion_masse(niveau):
    """
    Conversions de masses
    CE2 : g ↔ kg
    CM1-CM2 : g ↔ kg ↔ tonne
    """
    
    if niveau in ["CE1", "CE2"]:
        # g ↔ kg
        conversions = [
            ("g", "kg", 1000, random.randint(1000, 5000)),
            ("kg", "g", 1/1000, random.randint(2, 10))
        ]
    else:  # CM1-CM2
        conversions = [
            ("g", "kg", 1000, random.randint(1000, 8000)),
            ("kg", "g", 1/1000, random.randint(2, 15)),
            ("kg", "t", 1000, random.randint(1000, 5000)),
            ("t", "kg", 1/1000, random.randint(2, 10))
        ]
    
    unite_depart, unite_arrivee, diviseur, valeur_depart = random.choice(conversions)
    
    if diviseur < 1:
        valeur_arrivee = valeur_depart / diviseur
    else:
        valeur_arrivee = valeur_depart / diviseur
    
    return {
        'valeur_depart': valeur_depart,
        'unite_depart': unite_depart,
        'unite_arrivee': unite_arrivee,
        'reponse': valeur_arrivee,
        'question': f"Convertis {valeur_depart} {unite_depart} en {unite_arrivee}"
    }


def generer_conversion_capacite(niveau):
    """
    Conversions de capacités
    CE2-CM1-CM2 : mL ↔ cL ↔ L
    """
    
    if niveau in ["CE1"]:
        return None  # Pas encore
    
    conversions = [
        ("mL", "cL", 10, random.randint(50, 500)),
        ("cL", "mL", 1/10, random.randint(5, 50)),
        ("cL", "L", 100, random.randint(100, 500)),
        ("L", "cL", 1/100, random.randint(2, 10)),
        ("mL", "L", 1000, random.randint(1000, 5000)),
        ("L", "mL", 1/1000, random.randint(2, 10))
    ]
    
    unite_depart, unite_arrivee, diviseur, valeur_depart = random.choice(conversions)
    
    if diviseur < 1:
        valeur_arrivee = valeur_depart / diviseur
    else:
        valeur_arrivee = valeur_depart / diviseur
    
    return {
        'valeur_depart': valeur_depart,
        'unite_depart': unite_depart,
        'unite_arrivee': unite_arrivee,
        'reponse': valeur_arrivee,
        'question': f"Convertis {valeur_depart} {unite_depart} en {unite_arrivee}"
    }


def generer_probleme_duree(niveau):
    """
    Calculs de durées
    CE1-CE2 : Heures simples
    CM1-CM2 : Heures, minutes, conversions
    """
    
    if niveau in ["CE1", "CE2"]:
        # Durées simples en heures
        types = [
            "Un film commence à {h1}h et finit à {h2}h. Combien de temps dure-t-il ?",
            "Paul joue de {h1}h à {h2}h. Combien de temps a-t-il joué ?"
        ]
        
        h1 = random.randint(10, 16)
        h2 = h1 + random.randint(1, 4)
        duree = h2 - h1
        
        question = random.choice(types).format(h1=h1, h2=h2)
        
        return {
            'question': question,
            'reponse': duree,
            'unite': 'h',
            'type': 'simple'
        }
    
    else:  # CM1-CM2
        # Durées avec minutes
        types = [
            "simple_h",  # Juste heures
            "avec_min",  # Heures + minutes
            "conversion"  # min → h ou h → min
        ]
        
        type_choisi = random.choice(types)
        
        if type_choisi == "simple_h":
            h1 = random.randint(8, 14)
            h2 = h1 + random.randint(2, 6)
            duree = h2 - h1
            
            question = f"Un voyage dure de {h1}h à {h2}h. Quelle est la durée ?"
            return {
                'question': question,
                'reponse': duree,
                'unite': 'h',
                'type': 'simple'
            }
        
        elif type_choisi == "avec_min":
            h1, min1 = random.randint(9, 13), random.choice([0, 15, 30, 45])
            duree_h = random.randint(1, 3)
            duree_min = random.choice([0, 15, 30, 45])
            
            total_min_depart = h1 * 60 + min1
            total_min_arrivee = total_min_depart + (duree_h * 60) + duree_min
            
            h2 = total_min_arrivee // 60
            min2 = total_min_arrivee % 60
            
            question = f"Un train part à {h1}h{min1:02d} et arrive à {h2}h{min2:02d}. Durée du trajet ?"
            
            # Réponse en minutes
            reponse_min = (duree_h * 60) + duree_min
            
            return {
                'question': question,
                'reponse': reponse_min,
                'unite': 'min',
                'type': 'avec_min'
            }
        
        else:  # conversion
            if random.choice([True, False]):
                # h → min
                heures = random.randint(2, 5)
                minutes = heures * 60
                question = f"Convertis {heures} h en minutes"
                
                return {
                    'question': question,
                    'reponse': minutes,
                    'unite': 'min',
                    'type': 'conversion'
                }
            else:
                # min → h
                minutes = random.choice([60, 120, 180, 240, 300])
                heures = minutes / 60
                question = f"Convertis {minutes} min en heures"
                
                return {
                    'question': question,
                    'reponse': heures,
                    'unite': 'h',
                    'type': 'conversion'
                }


# ========================================
# FONCTIONS UTILITAIRES
# ========================================

@st.cache_data
def expliquer_conversion(valeur_depart: float, unite_depart: str, unite_arrivee: str, reponse: float) -> str:
    """
    ✅ Génère explication pour conversion (CACHÉ)
    """
    
    explication = f"### 💡 Méthode de conversion\n\n"
    
    # Longueurs
    if unite_depart == "mm" and unite_arrivee == "cm":
        explication += f"**1 cm = 10 mm**\n"
        explication += f"Donc pour passer de mm à cm, on **divise par 10**\n"
        explication += f"{valeur_depart} mm ÷ 10 = **{reponse} cm**"
    
    elif unite_depart == "cm" and unite_arrivee == "mm":
        explication += f"**1 cm = 10 mm**\n"
        explication += f"Donc pour passer de cm à mm, on **multiplie par 10**\n"
        explication += f"{valeur_depart} cm × 10 = **{reponse} mm**"
    
    elif unite_depart == "cm" and unite_arrivee == "m":
        explication += f"**1 m = 100 cm**\n"
        explication += f"Donc pour passer de cm à m, on **divise par 100**\n"
        explication += f"{valeur_depart} cm ÷ 100 = **{reponse} m**"
    
    elif unite_depart == "m" and unite_arrivee == "cm":
        explication += f"**1 m = 100 cm**\n"
        explication += f"Donc pour passer de m à cm, on **multiplie par 100**\n"
        explication += f"{valeur_depart} m × 100 = **{reponse} cm**"
    
    elif unite_depart == "m" and unite_arrivee == "km":
        explication += f"**1 km = 1000 m**\n"
        explication += f"Donc pour passer de m à km, on **divise par 1000**\n"
        explication += f"{valeur_depart} m ÷ 1000 = **{reponse} km**"
    
    elif unite_depart == "km" and unite_arrivee == "m":
        explication += f"**1 km = 1000 m**\n"
        explication += f"Donc pour passer de km à m, on **multiplie par 1000**\n"
        explication += f"{valeur_depart} km × 1000 = **{reponse} m**"
    
    # Masses
    elif unite_depart == "g" and unite_arrivee == "kg":
        explication += f"**1 kg = 1000 g**\n"
        explication += f"Donc pour passer de g à kg, on **divise par 1000**\n"
        explication += f"{valeur_depart} g ÷ 1000 = **{reponse} kg**"
    
    elif unite_depart == "kg" and unite_arrivee == "g":
        explication += f"**1 kg = 1000 g**\n"
        explication += f"Donc pour passer de kg à g, on **multiplie par 1000**\n"
        explication += f"{valeur_depart} kg × 1000 = **{reponse} g**"
    
    elif unite_depart == "kg" and unite_arrivee == "t":
        explication += f"**1 tonne = 1000 kg**\n"
        explication += f"Donc pour passer de kg à tonnes, on **divise par 1000**\n"
        explication += f"{valeur_depart} kg ÷ 1000 = **{reponse} t**"
    
    elif unite_depart == "t" and unite_arrivee == "kg":
        explication += f"**1 tonne = 1000 kg**\n"
        explication += f"Donc pour passer de tonnes à kg, on **multiplie par 1000**\n"
        explication += f"{valeur_depart} t × 1000 = **{reponse} kg**"
    
    # Capacités
    elif unite_depart == "mL" and unite_arrivee == "cL":
        explication += f"**1 cL = 10 mL**\n"
        explication += f"Donc pour passer de mL à cL, on **divise par 10**\n"
        explication += f"{valeur_depart} mL ÷ 10 = **{reponse} cL**"
    
    elif unite_depart == "cL" and unite_arrivee == "mL":
        explication += f"**1 cL = 10 mL**\n"
        explication += f"Donc pour passer de cL à mL, on **multiplie par 10**\n"
        explication += f"{valeur_depart} cL × 10 = **{reponse} mL**"
    
    elif unite_depart == "cL" and unite_arrivee == "L":
        explication += f"**1 L = 100 cL**\n"
        explication += f"Donc pour passer de cL à L, on **divise par 100**\n"
        explication += f"{valeur_depart} cL ÷ 100 = **{reponse} L**"
    
    elif unite_depart == "L" and unite_arrivee == "cL":
        explication += f"**1 L = 100 cL**\n"
        explication += f"Donc pour passer de L à cL, on **multiplie par 100**\n"
        explication += f"{valeur_depart} L × 100 = **{reponse} cL**"
    
    elif unite_depart == "mL" and unite_arrivee == "L":
        explication += f"**1 L = 1000 mL**\n"
        explication += f"Donc pour passer de mL à L, on **divise par 1000**\n"
        explication += f"{valeur_depart} mL ÷ 1000 = **{reponse} L**"
    
    elif unite_depart == "L" and unite_arrivee == "mL":
        explication += f"**1 L = 1000 mL**\n"
        explication += f"Donc pour passer de L à mL, on **multiplie par 1000**\n"
        explication += f"{valeur_depart} L × 1000 = **{reponse} mL**"
    
    else:
        explication += f"Conversion : {valeur_depart} {unite_depart} = **{reponse} {unite_arrivee}**"
    
    return explication
"""
geometrie_utils.py
Exercices de géométrie CE1-CM2
"""

import random
import math

# ========================================
# GÉNÉRATEURS D'EXERCICES
# ========================================

def generer_reconnaissance_forme(niveau):
    """
    Exercice : Identifier une forme géométrique
    CE1-CE2 : Formes simples
    """
    
    if niveau in ["CE1", "CE2"]:
        formes = [
            {"nom": "Carré", "cotes": 4, "sommets": 4, "type": "polygone"},
            {"nom": "Rectangle", "cotes": 4, "sommets": 4, "type": "polygone"},
            {"nom": "Triangle", "cotes": 3, "sommets": 3, "type": "polygone"},
            {"nom": "Cercle", "cotes": 0, "sommets": 0, "type": "non-polygone"},
        ]
    else:  # CM1-CM2
        formes = [
            {"nom": "Carré", "cotes": 4, "sommets": 4, "type": "polygone"},
            {"nom": "Rectangle", "cotes": 4, "sommets": 4, "type": "polygone"},
            {"nom": "Triangle", "cotes": 3, "sommets": 3, "type": "polygone"},
            {"nom": "Pentagone", "cotes": 5, "sommets": 5, "type": "polygone"},
            {"nom": "Hexagone", "cotes": 6, "sommets": 6, "type": "polygone"},
            {"nom": "Cercle", "cotes": 0, "sommets": 0, "type": "non-polygone"},
        ]
    
    forme = random.choice(formes)
    
    # Générer 3 distracteurs
    autres = [f for f in formes if f["nom"] != forme["nom"]]
    distracteurs = random.sample(autres, min(3, len(autres)))
    
    options = [forme["nom"]] + [d["nom"] for d in distracteurs]
    random.shuffle(options)
    
    return {
        "forme": forme,
        "options": options,
        "question": "Quelle est cette forme ?"
    }


def generer_perimetre(niveau):
    """
    Exercice : Calculer le périmètre
    CE2 : Rectangles/carrés simples
    CM1-CM2 : Formes plus complexes
    """
    
    if niveau == "CE2":
        # Carrés et rectangles simples
        if random.choice([True, False]):
            # Carré
            cote = random.randint(3, 8)
            return {
                "type": "carre",
                "dimensions": {"cote": cote},
                "reponse": 4 * cote,
                "formule": f"4 × {cote}",
                "question": f"Quel est le périmètre d'un carré de côté {cote} cm ?"
            }
        else:
            # Rectangle
            longueur = random.randint(5, 12)
            largeur = random.randint(3, longueur - 1)
            return {
                "type": "rectangle",
                "dimensions": {"longueur": longueur, "largeur": largeur},
                "reponse": 2 * (longueur + largeur),
                "formule": f"2 × ({longueur} + {largeur})",
                "question": f"Quel est le périmètre d'un rectangle de {longueur} cm × {largeur} cm ?"
            }
    
    else:  # CM1-CM2
        # Ajouter triangles
        forme_type = random.choice(["carre", "rectangle", "triangle"])
        
        if forme_type == "carre":
            cote = random.randint(5, 15)
            return {
                "type": "carre",
                "dimensions": {"cote": cote},
                "reponse": 4 * cote,
                "formule": f"4 × {cote}",
                "question": f"Périmètre d'un carré de {cote} cm de côté ?"
            }
        
        elif forme_type == "rectangle":
            longueur = random.randint(8, 20)
            largeur = random.randint(4, longueur - 2)
            return {
                "type": "rectangle",
                "dimensions": {"longueur": longueur, "largeur": largeur},
                "reponse": 2 * (longueur + largeur),
                "formule": f"2 × ({longueur} + {largeur})",
                "question": f"Périmètre d'un rectangle {longueur} cm × {largeur} cm ?"
            }
        
        else:  # triangle
            a = random.randint(5, 12)
            b = random.randint(5, 12)
            c = random.randint(5, 12)
            return {
                "type": "triangle",
                "dimensions": {"a": a, "b": b, "c": c},
                "reponse": a + b + c,
                "formule": f"{a} + {b} + {c}",
                "question": f"Périmètre d'un triangle de côtés {a} cm, {b} cm et {c} cm ?"
            }


def generer_aire(niveau):
    """
    Exercice : Calculer l'aire
    CM1 : Carrés et rectangles
    CM2 : Triangles
    """
    
    if niveau == "CM1":
        if random.choice([True, False]):
            # Carré
            cote = random.randint(4, 12)
            return {
                "type": "carre",
                "dimensions": {"cote": cote},
                "reponse": cote * cote,
                "formule": f"{cote} × {cote}",
                "unite": "cm²",
                "question": f"Quelle est l'aire d'un carré de {cote} cm de côté ?"
            }
        else:
            # Rectangle
            longueur = random.randint(6, 15)
            largeur = random.randint(4, 10)
            return {
                "type": "rectangle",
                "dimensions": {"longueur": longueur, "largeur": largeur},
                "reponse": longueur * largeur,
                "formule": f"{longueur} × {largeur}",
                "unite": "cm²",
                "question": f"Aire d'un rectangle de {longueur} cm × {largeur} cm ?"
            }
    
    else:  # CM2 - Ajouter triangles
        forme_type = random.choice(["rectangle", "triangle"])
        
        if forme_type == "rectangle":
            longueur = random.randint(8, 20)
            largeur = random.randint(5, 15)
            return {
                "type": "rectangle",
                "dimensions": {"longueur": longueur, "largeur": largeur},
                "reponse": longueur * largeur,
                "formule": f"{longueur} × {largeur}",
                "unite": "cm²",
                "question": f"Aire d'un rectangle {longueur} cm × {largeur} cm ?"
            }
        
        else:  # triangle
            base = random.randint(6, 16)
            hauteur = random.randint(4, 12)
            return {
                "type": "triangle",
                "dimensions": {"base": base, "hauteur": hauteur},
                "reponse": (base * hauteur) // 2,
                "formule": f"({base} × {hauteur}) ÷ 2",
                "unite": "cm²",
                "question": f"Aire d'un triangle de base {base} cm et hauteur {hauteur} cm ?"
            }


def generer_angle(niveau):
    """
    Exercice : Reconnaître types d'angles
    CM2 uniquement
    """
    
    angles = [
        {"nom": "Angle droit", "mesure": 90, "type": "droit"},
        {"nom": "Angle aigu", "mesure": random.randint(30, 85), "type": "aigu"},
        {"nom": "Angle obtus", "mesure": random.randint(95, 150), "type": "obtus"},
        {"nom": "Angle plat", "mesure": 180, "type": "plat"},
    ]
    
    angle = random.choice(angles)
    
    # Options
    types_possibles = ["Angle droit", "Angle aigu", "Angle obtus", "Angle plat"]
    
    return {
        "angle": angle,
        "options": types_possibles,
        "reponse": angle["nom"],
        "question": f"Quel type d'angle mesure {angle['mesure']}° ?"
    }


# ========================================
# FONCTIONS SVG (Visualisations)
# ========================================

def dessiner_forme_svg(forme_nom, dimensions, size=300):
    """
    Génère SVG d'une forme géométrique
    
    Args:
        forme_nom: "Carré", "Rectangle", "Triangle", "Cercle", etc.
        dimensions: dict avec dimensions (cote, longueur, largeur, etc.)
        size: taille SVG
    
    Returns:
        string HTML avec SVG
    """
    
    center = size // 2
    
    if forme_nom == "Carré":
        cote = min(size * 0.6, 200)
        x = center - cote / 2
        y = center - cote / 2
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <rect x="{x}" y="{y}" width="{cote}" height="{cote}" 
                  fill="#4A90E2" stroke="#2E5C8A" stroke-width="3"/>
            <text x="{center}" y="{size - 20}" text-anchor="middle" 
                  font-size="16" font-weight="bold" fill="#333">
                {dimensions.get('cote', '')} cm
            </text>
        </svg>
        '''
    
    elif forme_nom == "Rectangle":
        longueur = min(size * 0.7, 240)
        largeur = longueur * 0.6
        x = center - longueur / 2
        y = center - largeur / 2
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <rect x="{x}" y="{y}" width="{longueur}" height="{largeur}" 
                  fill="#50C878" stroke="#2E7D4E" stroke-width="3"/>
            <text x="{center}" y="{y - 10}" text-anchor="middle" 
                  font-size="16" font-weight="bold" fill="#333">
                {dimensions.get('longueur', '')} cm
            </text>
            <text x="{x - 30}" y="{center}" text-anchor="middle" 
                  font-size="16" font-weight="bold" fill="#333" 
                  transform="rotate(-90, {x - 30}, {center})">
                {dimensions.get('largeur', '')} cm
            </text>
        </svg>
        '''
    
    elif forme_nom == "Triangle":
        base = min(size * 0.6, 200)
        hauteur = base * 0.8
        
        x1, y1 = center, center - hauteur / 2
        x2, y2 = center - base / 2, center + hauteur / 2
        x3, y3 = center + base / 2, center + hauteur / 2
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" 
                     fill="#FF6B6B" stroke="#C92A2A" stroke-width="3"/>
        </svg>
        '''
    
    elif forme_nom == "Cercle":
        radius = min(size * 0.35, 120)
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <circle cx="{center}" cy="{center}" r="{radius}" 
                    fill="#FFD93D" stroke="#F5A623" stroke-width="3"/>
        </svg>
        '''
    
    elif forme_nom == "Pentagone":
        radius = min(size * 0.35, 120)
        points = []
        for i in range(5):
            angle = (i * 72 - 90) * math.pi / 180
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append(f"{x},{y}")
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <polygon points="{' '.join(points)}" 
                     fill="#A78BFA" stroke="#7C3AED" stroke-width="3"/>
        </svg>
        '''
    
    elif forme_nom == "Hexagone":
        radius = min(size * 0.35, 120)
        points = []
        for i in range(6):
            angle = (i * 60 - 90) * math.pi / 180
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append(f"{x},{y}")
        
        svg = f'''
        <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
            <polygon points="{' '.join(points)}" 
                     fill="#FB923C" stroke="#EA580C" stroke-width="3"/>
        </svg>
        '''
    
    else:
        svg = f'<svg width="{size}" height="{size}"></svg>'
    
    return svg


def dessiner_angle_svg(mesure_degres, size=300):
    """
    Dessine un angle avec arc - VERSION SIMPLIFIÉE
    """
    
    center_x = 75
    center_y = 225
    length = 150
    
    # Côté horizontal (toujours horizontal)
    x1 = center_x + length
    y1 = center_y
    
    # Deuxième côté selon angle
    angle_rad = mesure_degres * 3.14159 / 180  # Conversion en radians
    x2 = center_x + (length * math.cos(angle_rad))
    y2 = center_y - (length * math.sin(angle_rad))
    
    # Arc
    arc_radius = 40
    arc_x = center_x + (arc_radius * math.cos(angle_rad))
    arc_y = center_y - (arc_radius * math.sin(angle_rad))
    
    # Couleur selon type
    if mesure_degres == 90:
        color = "#4A90E2"
    elif mesure_degres < 90:
        color = "#50C878"
    elif mesure_degres == 180:
        color = "#9B59B6"
    else:
        color = "#FF6B6B"
    
    # Construire le SVG étape par étape
    svg_parts = []
    svg_parts.append(f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">')
    
    # Ligne 1 (horizontale)
    svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x1}" y2="{y1}" stroke="#333" stroke-width="3"/>')
    
    # Ligne 2 (angle)
    svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#333" stroke-width="3"/>')
    
    # Arc
    large_arc = 0 if mesure_degres <= 180 else 1
    svg_parts.append(f'<path d="M {center_x + arc_radius} {center_y} A {arc_radius} {arc_radius} 0 {large_arc} 0 {arc_x:.1f} {arc_y:.1f}" stroke="{color}" stroke-width="2" fill="none"/>')
    
    # Texte
    svg_parts.append(f'<text x="{center_x + 60}" y="{center_y - 20}" font-size="18" font-weight="bold" fill="{color}">{mesure_degres}°</text>')
    
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)
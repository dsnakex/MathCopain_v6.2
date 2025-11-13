import streamlit as st
import math
from typing import Tuple

@st.cache_data
def dessiner_pizza(denominateur: int, parts_colorees: Tuple[int, ...], size: int = 300) -> str:
    """
    ✅ Génère SVG d'une pizza divisée en parts (CACHÉ)

    Args:
        denominateur: nombre de parts total (2, 3, 4, 6, 8)
        parts_colorees: TUPLE d'indices des parts colorées [0, 1, ...]
        size: taille en pixels

    Returns:
        HTML string avec SVG (mémorisé si paramètres identiques)
    """

    center = size // 2
    radius = size // 2 - 10
    angle_per_slice = 360 / denominateur

    svg_parts = []

    for i in range(denominateur):
        angle_start = i * angle_per_slice - 90  # -90 pour commencer en haut
        angle_end = (i + 1) * angle_per_slice - 90

        # Convertir en radians
        rad_start = math.radians(angle_start)
        rad_end = math.radians(angle_end)

        # Points du triangle
        x1 = center + radius * math.cos(rad_start)
        y1 = center + radius * math.sin(rad_start)
        x2 = center + radius * math.cos(rad_end)
        y2 = center + radius * math.sin(rad_end)

        # Couleur selon si colorée
        if i in parts_colorees:
            fill = "#FFD700"  # Doré
            stroke = "#FFA500"  # Orange
        else:
            fill = "#FFF8DC"  # Beige clair
            stroke = "#DEB887"  # Beige foncé

        # Arc path
        large_arc = 1 if angle_per_slice > 180 else 0
        path = f'M {center},{center} L {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2} Z'

        svg_parts.append(f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    svg = f'''
    <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
        <circle cx="{center}" cy="{center}" r="{radius}" fill="#D2691E" stroke="#8B4513" stroke-width="3"/>
        {''.join(svg_parts)}
    </svg>
    '''

    return svg


def pizza_interactive(denominateur, callback_key="pizza"):
    """
    Pizza cliquable - retourne indices des parts sélectionnées

    Usage:
        selected = pizza_interactive(4, "my_pizza")
        if selected:
            st.write(f"Parts sélectionnées: {selected}")
    """

    if f'{callback_key}_selected' not in st.session_state:
        st.session_state[f'{callback_key}_selected'] = set()

    selected = st.session_state[f'{callback_key}_selected']

    # Afficher pizza avec cache
    st.markdown(dessiner_pizza(denominateur, tuple(selected), 300), unsafe_allow_html=True)

    # Boutons pour sélectionner parts
    st.write("**Clique sur les parts à colorier:**")

    cols = st.columns(min(denominateur, 4))
    for i in range(denominateur):
        col = cols[i % len(cols)]
        with col:
            is_selected = i in selected
            label = f"✓ Part {i+1}" if is_selected else f"Part {i+1}"

            if st.button(label, key=f"{callback_key}_part_{i}", use_container_width=True):
                if i in selected:
                    selected.remove(i)
                else:
                    selected.add(i)
                st.rerun()

    return selected


@st.cache_data
def afficher_fraction_droite(numerateur: int, denominateur: int, size: int = 400) -> str:
    """
    ✅ Affiche fraction sur droite numérique 0-1 (CACHÉ)
    """

    valeur = numerateur / denominateur
    position = int(valeur * size)

    svg = f'''
    <svg width="{size + 40}" height="80" xmlns="http://www.w3.org/2000/svg">
        <!-- Ligne principale -->
        <line x1="20" y1="40" x2="{size + 20}" y2="40" stroke="black" stroke-width="2"/>

        <!-- Graduation 0 -->
        <line x1="20" y1="30" x2="20" y2="50" stroke="black" stroke-width="2"/>
        <text x="15" y="65" font-size="14" fill="black">0</text>

        <!-- Graduation 1 -->
        <line x1="{size + 20}" y1="30" x2="{size + 20}" y2="50" stroke="black" stroke-width="2"/>
        <text x="{size + 15}" y="65" font-size="14" fill="black">1</text>

        <!-- Fraction positionnée -->
        <circle cx="{position + 20}" cy="40" r="8" fill="#FF6B6B"/>
        <text x="{position + 10}" y="20" font-size="16" font-weight="bold" fill="black">{numerateur}/{denominateur}</text>
    </svg>
    '''

    return svg

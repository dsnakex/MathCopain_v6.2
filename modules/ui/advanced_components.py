# modules/ui/advanced_components.py

import streamlit as st
from typing import Literal, Optional

def input_field(
    label: str,
    key: str,
    placeholder: str = "Tape ici...",
    state: Literal["default", "focus", "error", "success"] = "default",
    error_message: Optional[str] = None,
    help_text: Optional[str] = None
) -> str:
    """Input stylisé du Design Figma"""

    if state == "error":
        st.markdown(
            f"<p style='color: #E74C3C; font-size: 12px; font-weight: 600;'>{label}</p>",
            unsafe_allow_html=True
        )
        value = st.text_input(
            key=key,
            label_visibility="collapsed",
            placeholder=placeholder,
            help=help_text
        )
        if error_message:
            st.markdown(
                f"<p style='color: #E74C3C; font-size: 12px;'>❌ {error_message}</p>",
                unsafe_allow_html=True
            )
        return value

    elif state == "success":
        st.markdown(
            f"<p style='color: #2ECC71; font-size: 12px; font-weight: 600;'>{label}</p>",
            unsafe_allow_html=True
        )
        value = st.text_input(
            key=key,
            label_visibility="collapsed",
            placeholder=placeholder,
            help=help_text
        )
        if error_message:
            st.markdown(
                f"<p style='color: #2ECC71; font-size: 12px;'>✅ {error_message}</p>",
                unsafe_allow_html=True
            )
        return value

    else:
        return st.text_input(
            label=label,
            key=key,
            placeholder=placeholder,
            help=help_text
        )

def badge_level(level: Literal["CE1", "CE2", "CM1", "CM2"]) -> None:
    """Badge niveau scolaire (Figma)"""

    colors = {
        "CE1": "#F39C12",  # Orange
        "CE2": "#5DADE2",  # Bleu
        "CM1": "#9B59B6",  # Violet
        "CM2": "#E74C3C",  # Rouge
    }

    color = colors.get(level, "#5DADE2")

    html = f"""
    <div style="
        display: inline-block;
        background-color: {color};
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        animation: fadeInUp 0.6s ease-out;
    ">
        {level}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

def exercise_card(
    level: Literal["CE1", "CE2", "CM1", "CM2"],
    exercise_type: str,
    operation: str,
    instructions: Optional[str] = None,
    on_validate: Optional[callable] = None,
    on_skip: Optional[callable] = None
) -> None:
    """Card d'exercice complet (Figma)"""

    with st.container():
        # Header avec badge
        col1, col2 = st.columns([1, 4])
        with col1:
            badge_level(level)
        with col2:
            st.markdown(
                f"<p style='font-size: 20px; font-weight: 600; margin: 0;'>{exercise_type}</p>",
                unsafe_allow_html=True
            )

        st.divider()

        # Opération (grand affichage)
        st.markdown(f"""
        <div style="
            background-color: #F0F8FF;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            color: #212121;
            margin: 20px 0;
        ">
            {operation}
        </div>
        """, unsafe_allow_html=True)

        if instructions:
            st.info(f"📝 {instructions}")

        # Input pour réponse
        answer = input_field(
            label="Votre réponse",
            key=f"exercise_{level}_{exercise_type}",
            placeholder="Tape ta réponse...",
            state="default"
        )

        # Boutons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Valider", key=f"validate_{level}_{exercise_type}", use_container_width=True):
                if on_validate:
                    on_validate(answer)

        with col2:
            if st.button("» Passer", key=f"skip_{level}_{exercise_type}", use_container_width=True):
                if on_skip:
                    on_skip()

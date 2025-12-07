import streamlit as st

def load_custom_css():
    """Charge le CSS personnalisé global"""
    css = """
    <style>
    /* ========== VARIABLES CSS (DE FIGMA) ========== */
    :root {
        --primary: #5DADE2;
        --secondary: #F39C12;
        --accent: #9B59B6;
        --success: #2ECC71;
        --error: #E74C3C;
        --gray-100: #F5F5F5;
        --gray-300: #E0E0E0;
        --gray-700: #616161;
        --gray-900: #212121;
    }

    /* ========== BOUTONS ========== */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        font-size: 15px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(33, 128, 163, 0.15);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(33, 128, 163, 0.25);
        background-color: #1A6B86 !important;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* ========== INPUTS ========== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(33, 128, 163, 0.1) !important;
        outline: none !important;
    }

    /* ========== TITRES ========== */
    h1 {
        color: var(--gray-900);
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 20px;
    }

    h2 {
        color: var(--gray-900);
        font-weight: 600;
        font-size: 24px;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 10px;
        margin-top: 20px;
    }

    /* ========== CARTES ========== */
    .metric-card {
        background: linear-gradient(135deg, #FFFBF9 0%, #F5F5F5 100%);
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* ========== BARRES PROGRESSION ========== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, #32b8c6 100%);
        border-radius: 10px;
    }

    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .animate-fadeInUp {
        animation: fadeInUp 0.6s ease-out;
    }

    .animate-pulse {
        animation: pulse 2s ease-in-out infinite;
    }

    /* ========== BADGES ========== */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px 4px;
    }

    .badge-success {
        background-color: rgba(34, 177, 76, 0.15);
        color: #22B14C;
    }

    .badge-warning {
        background-color: rgba(255, 153, 0, 0.15);
        color: #FF9900;
    }

    .badge-error {
        background-color: rgba(192, 21, 71, 0.15);
        color: #C01547;
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 640px) {
        h1 { font-size: 24px; }
        h2 { font-size: 18px; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def setup_ui():
    """Initialise toute l'UI"""
    load_custom_css()

"""
Styles CSS MathCopain
Styles visuels pour l'interface utilisateur
"""

import streamlit as st

@st.cache_data
def local_css():
    """CSS caché pour améliorer les performances de chargement"""
    return """
    <style>
    .categorie-header {
        font-size: 24px; font-weight: bold; margin: 20px 0 10px 0;
        padding: 10px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 10px;
    }
    .exercice-box {
        padding: 30px; border-radius: 10px; background-color: #f0f2f6; margin: 20px 0;
        border-left: 5px solid #667eea; font-size: 32px; font-weight: bold; text-align: center;
    }
    .badge {
        display: inline-block; padding: 8px 12px; margin: 5px;
        border-radius: 15px; background-color: #FFD700;
        font-weight: bold; font-size: 14px;
    }
    .feedback-success {
        padding: 15px; border-radius: 10px; background-color: #d4edda; border: 2px solid #28a745; color: #155724; margin: 15px 0; font-weight: bold; font-size: 18px;
    }
    .feedback-error {
        padding: 15px; border-radius: 10px; background-color: #f8d7da; border: 2px solid #dc3545; color: #721c24; margin: 15px 0; font-weight: bold; font-size: 18px;
    }
    .streak-box {
        padding: 15px; background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; text-align: center; font-size: 20px; font-weight: bold; margin: 10px 0;
    }
    .daily-challenge-box {
        padding: 15px; background-color: #e7f3ff; border: 2px solid #2196f3; border-radius: 10px; margin: 10px 0;
    }
    .leaderboard-box {
        padding: 15px; background-color: #f3e5f5; border: 2px solid #9c27b0; border-radius: 10px; margin: 10px 0;
    }
    .aller-loin-box {
        padding: 15px; border-radius: 10px; background-color: #fff5f0; margin: 10px 0; border-left: 5px solid #ff6b6b;
    }
    </style>
    """

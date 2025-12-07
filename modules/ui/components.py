import streamlit as st

def metric_card(title: str, value: str, delta: str = None, icon: str = "=Ê"):
    """Carte métrique stylisée"""
    html = f"""
    <div class="metric-card">
        <div style="font-size: 24px; margin-bottom: 10px;">{icon}</div>
        <div style="color: #999; font-size: 12px; text-transform: uppercase;
                    letter-spacing: 0.5px; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 28px; font-weight: 700; color: #212121;">{value}</div>
        {f'<div style="color: #5DADE2; font-size: 12px; margin-top: 5px;">{delta}</div>' if delta else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def progress_bar(title: str, current: int, total: int):
    """Barre de progression stylisée"""
    percentage = (current / total) * 100
    html = f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 600; color: #212121;">{title}</span>
            <span style="color: #5DADE2; font-weight: 600;">{current}/{total}</span>
        </div>
        <div style="background-color: #F0EDEA; border-radius: 10px; height: 8px;
                    overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(90deg, #5DADE2 0%, #32b8c6 100%);
                        width: {percentage}%; height: 100%;
                        transition: width 0.5s ease;
                        border-radius: 10px;"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def info_box(message: str, type: str = "info"):
    """Boîte d'information stylisée"""
    config = {
        "info": ("9", "#5DADE2", "rgba(93, 173, 226, 0.1)"),
        "success": ("", "#2ECC71", "rgba(34, 177, 76, 0.1)"),
        "warning": (" ", "#FF9900", "rgba(255, 153, 0, 0.1)"),
        "error": ("L", "#E74C3C", "rgba(231, 76, 60, 0.1)"),
    }

    icon, color, bg = config[type]
    html = f"""
    <div style="background-color: {bg}; border-left: 4px solid {color};
                padding: 12px 16px; border-radius: 6px; margin: 10px 0;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">{icon}</span>
            <span style="color: #212121; font-size: 14px;">{message}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def badge(emoji: str, text: str, color: str = "success"):
    """Badge stylisé"""
    class_name = f"badge badge-{color}"
    html = f'<span class="{class_name}">{emoji} {text}</span>'
    st.markdown(html, unsafe_allow_html=True)

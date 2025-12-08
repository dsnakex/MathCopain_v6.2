# modules/ui/charts.py

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def create_progression_chart(user_data):
    """Graphique de progression par module (ligne avec points)"""
    df = pd.DataFrame(user_data.get('progression_history', []))

    if df.empty:
        return None

    fig = go.Figure()

    for module in df['module'].unique():
        module_data = df[df['module'] == module]
        fig.add_trace(go.Scatter(
            x=module_data['date'],
            y=module_data['score'],
            name=module,
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='%{x|%d/%m}<br>Score: %{y}%<extra></extra>'
        ))

    fig.update_layout(
        title="📈 Progression par Module",
        xaxis_title="Date",
        yaxis_title="Score (%)",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12),
        plot_bgcolor='rgba(250, 250, 250, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
    )

    return fig

def create_level_distribution(user_data):
    """Graphique radar des compétences"""
    categories = ['Calcul', 'Géométrie', 'Fractions', 'Décimaux', 'Mesures']
    values = [
        user_data.get('skills', {}).get('calcul', 0),
        user_data.get('skills', {}).get('geometrie', 0),
        user_data.get('skills', {}).get('fractions', 0),
        user_data.get('skills', {}).get('decimaux', 0),
        user_data.get('skills', {}).get('mesures', 0),
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(93, 173, 226, 0.3)',
        line_color='#5DADE2',
        name='Profil',
        marker=dict(size=8, color='#5DADE2'),
        hovertemplate='%{theta}: %{r}%<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='rgba(245, 245, 245, 0.3)',
        ),
        title='🎯 Profil de Compétences',
        height=400,
        font=dict(family="Arial, sans-serif", size=11),
        showlegend=False,
    )

    return fig

def create_activity_heatmap(user_data):
    """Heatmap d'activité"""
    df = pd.DataFrame(user_data.get('activity', []))

    if df.empty:
        return None

    pivot_table = df.pivot_table(
        values='count',
        index='day_of_week',
        columns='hour',
        fill_value=0
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Blues',
        hovertemplate='%{x}h: %{z} exercices<extra></extra>'
    ))

    fig.update_layout(
        title='🔥 Activité par Heure',
        xaxis_title='Heure',
        yaxis_title='Jour',
        height=300,
    )

    return fig

# ========== EXPORT POUR STREAMLIT ==========
def display_chart(chart_type, user_data):
    """Affiche un graphique Plotly dans Streamlit"""
    charts = {
        'progression': create_progression_chart,
        'skills': create_level_distribution,
        'activity': create_activity_heatmap,
    }

    chart_func = charts.get(chart_type)
    if not chart_func:
        return None

    fig = chart_func(user_data)
    if fig:
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

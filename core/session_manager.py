"""
Session Manager - Gestion centralisée de l'état de session Streamlit
Extrait de app.py pour isolation et testabilité
"""

import streamlit as st
from datetime import date, datetime
from typing import Dict, Any, Optional


class SessionManager:
    """
    Gère l'état de session Streamlit de manière centralisée.

    Responsabilités:
    - Initialisation session state
    - Getters/Setters typés pour session vars
    - Auto-save profil utilisateur
    - Gestion streak et badges
    """

    def __init__(self):
        """Initialise le gestionnaire avec st.session_state."""
        self.state = st.session_state
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Initialise les clés session si pas déjà fait."""
        default_state = {
            'niveau': "CE1",
            'points': 0,
            'badges': [],
            'stats_par_niveau': {
                'CE1': {'correct': 0, 'total': 0},
                'CE2': {'correct': 0, 'total': 0},
                'CM1': {'correct': 0, 'total': 0},
                'CM2': {'correct': 0, 'total': 0}
            },
            'streak': {'current': 0, 'max': 0},
            'scores_history': [],
            'daily_challenge': {
                'today_date': str(date.today()),
                'completed': False,
                'challenge': None,
                'progress': 0
            },
            'exercice_courant': None,
            'show_feedback': False,
            'feedback_correct': False,
            'feedback_reponse': None,
            'dernier_exercice': None,
            'jeu_type': None,
            'jeu_memory': None,
            'memory_first_flip': None,
            'memory_second_flip': None,
            'memory_incorrect_pair': None,
            'active_category': "Exercice"
        }

        for key, value in default_state.items():
            if key not in self.state:
                self.state[key] = value

    # ========== Getters ==========

    def get_niveau(self) -> str:
        """Retourne niveau actuel (CE1, CE2, CM1, CM2)."""
        return self.state.get('niveau', 'CE1')

    def get_points(self) -> int:
        """Retourne points actuels."""
        return self.state.get('points', 0)

    def get_badges(self) -> list:
        """Retourne liste des badges obtenus."""
        return self.state.get('badges', [])

    def get_streak(self) -> Dict[str, int]:
        """Retourne dict avec current et max streak."""
        return self.state.get('streak', {'current': 0, 'max': 0})

    def get_stats_par_niveau(self) -> Dict[str, Dict[str, int]]:
        """Retourne stats par niveau."""
        return self.state.get('stats_par_niveau', {})

    def get_exercice_courant(self) -> Optional[Dict]:
        """Retourne exercice en cours."""
        return self.state.get('exercice_courant')

    def get_profil(self) -> Optional[Dict]:
        """Retourne profil utilisateur."""
        return self.state.get('profil')

    def get_utilisateur(self) -> Optional[str]:
        """Retourne nom utilisateur connecté."""
        return self.state.get('utilisateur')

    # ========== Setters ==========

    def set_niveau(self, niveau: str):
        """Définit niveau actuel."""
        if niveau in ['CE1', 'CE2', 'CM1', 'CM2']:
            self.state['niveau'] = niveau

    def set_points(self, points: int):
        """Définit points."""
        self.state['points'] = max(0, points)

    def add_points(self, points: int):
        """Ajoute points (peut être négatif)."""
        self.state['points'] = max(0, self.state.get('points', 0) + points)

    def add_badge(self, badge: str):
        """Ajoute un badge si pas déjà obtenu."""
        if badge not in self.state.get('badges', []):
            self.state['badges'].append(badge)

    def set_exercice_courant(self, exercice: Optional[Dict]):
        """Définit exercice en cours."""
        self.state['exercice_courant'] = exercice

    def set_feedback(self, correct: bool, reponse: Any):
        """Active feedback avec résultat."""
        self.state['show_feedback'] = True
        self.state['feedback_correct'] = correct
        self.state['feedback_reponse'] = reponse

    def clear_feedback(self):
        """Désactive feedback."""
        self.state['show_feedback'] = False
        self.state['feedback_correct'] = False
        self.state['feedback_reponse'] = None

    # ========== Streak Management ==========

    def update_streak(self, correct: bool) -> int:
        """
        Met à jour streak selon résultat.

        Args:
            correct: True si réponse correcte

        Returns:
            Current streak après update
        """
        streak = self.state.get('streak', {'current': 0, 'max': 0})

        if correct:
            streak['current'] += 1
            streak['max'] = max(streak['max'], streak['current'])
        else:
            streak['current'] = 0

        self.state['streak'] = streak
        return streak['current']

    def get_streak_bonus(self) -> int:
        """
        Calcule bonus points selon streak actuel.

        Returns:
            Bonus points (0-50)
        """
        current_streak = self.state.get('streak', {}).get('current', 0)

        if current_streak >= 10:
            return 50
        elif current_streak >= 5:
            return 20
        elif current_streak >= 3:
            return 10
        return 0

    # ========== Stats Management ==========

    def record_exercise_result(self, niveau: str, correct: bool):
        """
        Enregistre résultat exercice dans stats.

        Args:
            niveau: Niveau de l'exercice (CE1, CE2, CM1, CM2)
            correct: True si réponse correcte
        """
        stats = self.state.get('stats_par_niveau', {})

        if niveau not in stats:
            stats[niveau] = {'correct': 0, 'total': 0}

        stats[niveau]['total'] += 1
        if correct:
            stats[niveau]['correct'] += 1

        self.state['stats_par_niveau'] = stats

    def calculate_progression(self) -> Dict[str, int]:
        """
        Calcule progression (%) par niveau.

        Returns:
            Dict {niveau: pourcentage} (0-100)
        """
        stats = self.state.get('stats_par_niveau', {})
        progression = {}

        for niveau in ['CE1', 'CE2', 'CM1', 'CM2']:
            if niveau in stats:
                total = stats[niveau]['total']
                correct = stats[niveau]['correct']
                pourcentage = (correct / total * 100) if total > 0 else 0
                progression[niveau] = min(int(pourcentage), 100)
            else:
                progression[niveau] = 0

        return progression

    # ========== Profil Auto-save ==========

    def auto_save_profil(self, success: bool):
        """
        Sauvegarde automatique profil après exercice.

        Args:
            success: True si exercice réussi
        """
        if "utilisateur" not in self.state or "profil" not in self.state:
            return

        from utilisateur import sauvegarder_utilisateur

        nom = self.state["utilisateur"]
        profil = self.state["profil"]

        # Update profil with session state
        profil["niveau"] = self.state.get('niveau', 'CE1')
        profil["points"] = self.state.get('points', 0)
        profil["badges"] = self.state.get('badges', [])

        # Update exercise counters
        profil["exercices_reussis"] = profil.get("exercices_reussis", 0)
        profil["exercices_totaux"] = profil.get("exercices_totaux", 0)

        if success:
            profil["exercices_reussis"] += 1
        profil["exercices_totaux"] += 1

        # Calculate success rate
        if profil["exercices_totaux"] > 0:
            profil["taux_reussite"] = int(
                100 * profil["exercices_reussis"] / profil["exercices_totaux"]
            )
        else:
            profil["taux_reussite"] = 0

        # Update session timestamp
        profil["date_derniere_session"] = datetime.now().strftime("%Y-%m-%dT%H:%M")

        # Update progression
        if "stats_par_niveau" in self.state:
            profil["progression"] = self.calculate_progression()

        # Save to disk
        sauvegarder_utilisateur(nom, profil)

        # Update session state
        self.state["profil"] = profil

    # ========== Utility Methods ==========

    def reset_exercise_state(self):
        """Réinitialise état exercice pour nouveau."""
        self.state['exercice_courant'] = None
        self.state['dernier_exercice'] = None
        self.clear_feedback()

    def is_authenticated(self) -> bool:
        """Vérifie si utilisateur est authentifié."""
        return "utilisateur" in self.state and "profil" in self.state

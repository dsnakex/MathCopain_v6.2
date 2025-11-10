"""
Suivi compétences utilisateur MathCopain v6.0
"""

from datetime import datetime
from typing import Dict, List
import json

class SkillTracker:
    """
    Gère persistance et mise à jour compétences utilisateur
    """
    
    def __init__(self, profil: Dict):
        """
        Args:
            profil: Profil utilisateur complet (depuis st.session_state.profil)
        """
        self.profil = profil
        
        # Initialiser stats par type si pas déjà fait
        if 'stats_par_type' not in self.profil:
            self.profil['stats_par_type'] = {
                'addition': {'correct': 0, 'total': 0},
                'soustraction': {'correct': 0, 'total': 0},
                'multiplication': {'correct': 0, 'total': 0},
                'division': {'correct': 0, 'total': 0},
                'probleme': {'correct': 0, 'total': 0},
                'fractions': {'correct': 0, 'total': 0},
                'géométrie': {'correct': 0, 'total': 0},
                'decimaux': {'correct': 0, 'total': 0},  # AJOUTER
                'proportionnalite': {'correct': 0, 'total': 0},
                'mesures': {'correct': 0, 'total': 0}  # AJOUTER  # AJOUTER
            
            }
        
        # Initialiser historique exercices
        if 'exercise_history' not in self.profil:
            self.profil['exercise_history'] = []
    
    def record_exercise(self, exercise_type: str, correct: bool, difficulty: int = 3, time_taken: float = None):
        """
        Enregistre un exercice dans l'historique
        
        Args:
            exercise_type: Type exercice (addition, soustraction, etc.)
            correct: Réussi ou non
            difficulty: Niveau difficulté 1-10
            time_taken: Temps en secondes (optionnel)
        """
        # Mettre à jour stats par type
        if exercise_type in self.profil['stats_par_type']:
            self.profil['stats_par_type'][exercise_type]['total'] += 1
            if correct:
                self.profil['stats_par_type'][exercise_type]['correct'] += 1
        
        # Ajouter à l'historique
        exercise_record = {
            'type': exercise_type,
            'correct': correct,
            'difficulty': difficulty,
            'timestamp': datetime.now().isoformat(),
            'time_taken': time_taken
        }
        
        self.profil['exercise_history'].append(exercise_record)
        
        # Garder seulement 100 derniers (économie mémoire)
        if len(self.profil['exercise_history']) > 100:
            self.profil['exercise_history'] = self.profil['exercise_history'][-100:]
    
    def get_success_rate_by_type(self) -> Dict[str, float]:
        """
        Calcule taux réussite par type
        
        Returns:
            {'addition': 0.75, 'soustraction': 0.60, ...}
        """
        rates = {}
        for ex_type, stats in self.profil['stats_par_type'].items():
            if stats['total'] > 0:
                rates[ex_type] = stats['correct'] / stats['total']
            else:
                rates[ex_type] = 0.0
        return rates
    
    def get_weak_areas(self, threshold: float = 0.5) -> List[str]:
        """
        Identifie domaines à travailler
        
        Args:
            threshold: Seuil en dessous duquel considéré "faible"
        
        Returns:
            Liste types exercices faibles
        """
        rates = self.get_success_rate_by_type()
        weak = [ex_type for ex_type, rate in rates.items() if rate < threshold and self.profil['stats_par_type'][ex_type]['total'] >= 3]
        return weak
    
    def get_strong_areas(self, threshold: float = 0.75) -> List[str]:
        """
        Identifie domaines maîtrisés
        """
        rates = self.get_success_rate_by_type()
        strong = [ex_type for ex_type, rate in rates.items() if rate >= threshold and self.profil['stats_par_type'][ex_type]['total'] >= 5]
        return strong
"""
Système adaptatif MathCopain v6.0
Ajuste difficulté et recommande exercices selon performance
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class AdaptiveSystem:
    """
    Gère l'adaptation de difficulté et recommandations d'exercices
    Basé sur Item Response Theory (IRT) simplifié
    """
    
    def __init__(self):
        # Taux de réussite cible (zone d'apprentissage optimal)
        self.target_success_rate = 0.65  # 65%
        
        # Poids temporel : anciennes performances comptent moins
        self.decay_days = 7  # Données > 7 jours perdent 50% poids
    
    def analyze_performance(self, exercise_history: List[Dict], exercise_type: str = None) -> Dict:
        """
        Analyse performance récente (10 derniers exercices)
        
        Args:
            exercise_history: Liste exercices [{type, correct, difficulty, timestamp}]
            exercise_type: Filtrer par type (ex: "addition"), None = tous
        
        Returns:
            {
                'success_rate': float,      # Taux réussite 0-1
                'avg_difficulty': float,     # Difficulté moyenne
                'total_exercises': int,      # Nombre exercices
                'trend': str                # 'improving', 'stable', 'declining'
            }
        """
        # Filtrer par type si spécifié
        if exercise_type:
            history = [ex for ex in exercise_history if ex.get('type') == exercise_type]
        else:
            history = exercise_history
        
        # Prendre 10 derniers
        recent = history[-10:] if len(history) > 10 else history
        
        if not recent:
            return {
                'success_rate': 0.5,  # Neutre
                'avg_difficulty': 3,
                'total_exercises': 0,
                'trend': 'unknown'
            }
        
        # Calculer taux réussite
        correct_count = sum(1 for ex in recent if ex.get('correct', False))
        success_rate = correct_count / len(recent)
        
        # Difficulté moyenne
        avg_diff = sum(ex.get('difficulty', 3) for ex in recent) / len(recent)
        
        # Tendance (comparer 5 premiers vs 5 derniers)
        if len(recent) >= 10:
            first_half_success = sum(1 for ex in recent[:5] if ex.get('correct')) / 5
            second_half_success = sum(1 for ex in recent[5:] if ex.get('correct')) / 5
            
            if second_half_success > first_half_success + 0.15:
                trend = 'improving'
            elif second_half_success < first_half_success - 0.15:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'success_rate': success_rate,
            'avg_difficulty': avg_diff,
            'total_exercises': len(recent),
            'trend': trend
        }
    
    def calculate_next_difficulty(self, performance: Dict, current_difficulty: int = 3) -> int:
        """
        Calcule difficulté optimale pour prochain exercice
        
        Logique :
        - Si taux réussite > 75% → augmenter difficulté
        - Si taux réussite < 50% → diminuer difficulté
        - Si 50-75% → maintenir ou ajuster légèrement
        
        Args:
            performance: Dict retourné par analyze_performance()
            current_difficulty: Difficulté actuelle (1-10)
        
        Returns:
            int: Nouvelle difficulté (1-10)
        """
        success_rate = performance['success_rate']
        
        # Pas assez de données
        if performance['total_exercises'] < 3:
            return current_difficulty
        
        # Trop facile
        if success_rate > 0.75:
            new_difficulty = min(current_difficulty + 1, 10)
            return new_difficulty
        
        # Trop difficile
        elif success_rate < 0.50:
            new_difficulty = max(current_difficulty - 1, 1)
            return new_difficulty
        
        # Zone optimale (50-75%)
        else:
            # Micro-ajustements selon tendance
            if performance['trend'] == 'improving':
                return min(current_difficulty + 1, 10)
            elif performance['trend'] == 'declining':
                return max(current_difficulty - 1, 1)
            else:
                return current_difficulty
    
    def get_skill_levels(self, exercise_history: List[Dict]) -> Dict[str, float]:
        """
        Calcule niveau compétence par type d'exercice (0-1)
        
        Formule : Bayesian Knowledge Tracing simplifié
        - Succès récents = +0.1 à +0.2
        - Échecs récents = -0.05 à -0.1
        - Decay temporel appliqué
        
        Args:
            exercise_history: Liste complète exercices
        
        Returns:
            {'addition': 0.65, 'soustraction': 0.42, ...}
        """
        # ✅ Utiliser les types définis dans le SkillTracker pour la cohérence
        exercise_types = ['addition', 'soustraction', 'multiplication', 'division', 'probleme', 'fractions', 'géométrie', 'décimaux', 'proportionnalite', 'mesures', 'monnaie']
        skill_levels = {}
        
        for ex_type in exercise_types:
            type_history = [ex for ex in exercise_history if ex.get('type') == ex_type]
            
            if not type_history:
                skill_levels[ex_type] = 0  # Neutre si jamais fait
                continue
            
            # Calculer score basé sur 20 derniers
            recent = type_history[-20:]
            
            # Score initial
            skill = 0
            
            for ex in recent:
                # Poids temporel
                days_ago = (datetime.now() - datetime.fromisoformat(ex.get('timestamp', datetime.now().isoformat()))).days
                weight = 0.5 ** (days_ago / self.decay_days)  # Décroissance exponentielle
                
                # Mise à jour selon résultat
                if ex.get('correct'):
                    # Succès : augmente compétence
                    difficulty_factor = ex.get('difficulty', 3) / 10  # Plus difficile = plus d'apprentissage
                    skill += (0.15 * difficulty_factor * weight * (1 - skill))
                else:
                    # Échec : diminue légèrement
                    skill -= (0.08 * weight * skill)
                
                # Clamp entre 0-1
                skill = max(0.0, min(1.0, skill))
            
            skill_levels[ex_type] = round(skill, 2)
        
        return skill_levels
    
    def recommend_exercise_type(self, skill_levels: Dict[str, float]) -> Tuple[str, str]:
        """
        Recommande type d'exercice optimal
        
        Stratégie :
        - 70% : Domaines faibles (skill < 0.5)
        - 20% : Domaines intermédiaires (0.5 <= skill < 0.7)
        - 10% : Révision domaines forts (skill >= 0.7)
        
        Args:
            skill_levels: Dict retourné par get_skill_levels()
        
        Returns:
            (exercise_type: str, reason: str)
        """
        # Catégoriser par niveau en filtrant les types non pertinents (compétence 0)
        weak = {k: v for k, v in skill_levels.items() if v < 0.5}
        medium = {k: v for k, v in skill_levels.items() if 0.5 <= v < 0.7}
        strong = {k: v for k, v in skill_levels.items() if v >= 0.7 and v > 0} # Ne pas réviser ce qui n'a jamais été fait
        
        # Choix selon probabilités
        rand = random.random()
        
        if rand < 0.7 and weak:
            # Choisir domaine le plus faible
            ex_type = min(weak, key=weak.get)
            reason = f"💪 Travaillons {ex_type} (niveau {int(weak[ex_type]*100)}%)"
        
        elif rand < 0.9 and medium:
            # Choisir domaine intermédiaire
            ex_type = random.choice(list(medium.keys()))
            reason = f"👍 Continuons {ex_type} pour progresser"
        
        elif strong:
            # Révision
            ex_type = random.choice(list(strong.keys()))
            reason = f"✅ Révision {ex_type} (bien maîtrisé !)"
        
        else:
            # Fallback
            # Choisir un type au hasard parmi ceux qui ont déjà été pratiqués, ou un faible sinon
            practiced_types = [k for k, v in skill_levels.items() if v > 0]
            fallback_pool = practiced_types if practiced_types else list(weak.keys()) if weak else list(skill_levels.keys())
            ex_type = random.choice(fallback_pool)
            reason = "🎯 Pratiquons un peu de tout"
        
        return (ex_type, reason)
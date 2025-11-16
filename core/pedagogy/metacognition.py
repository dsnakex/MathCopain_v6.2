"""
MetacognitionEngine - Phase 6.2.1
Questions réflexives post-exercice pour développer la métacognition

Basé sur:
- Flavell (1979) - Théorie de la métacognition
- Zimmerman (2002) - Autorégulation de l'apprentissage
- Schraw & Dennison (1994) - Conscience métacognitive

Fonctionnalités:
- Questions réflexives courtes (30 sec max)
- Portfolio de stratégies personnalisé
- Détection de patterns d'apprentissage
- Suggestions d'autorégulation
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from collections import Counter, defaultdict
import random


@dataclass
class ReflectionData:
    """Structure pour une réflexion post-exercice"""
    timestamp: str
    exercise_type: str
    difficulty_level: str
    was_correct: bool

    # Question 1: Stratégie utilisée
    strategy_used: str  # "Doigts", "Mental", "Dessin", "Formule", "Autre"
    strategy_other: Optional[str] = None  # Si "Autre", description

    # Question 2: Difficulté perçue
    perceived_difficulty: int = 3  # 1 (Facile) à 5 (Difficile)

    # Question 3: Auto-explication
    self_explanation: Optional[str] = None

    # Question 4: Intention future
    future_intention: Optional[str] = None

    # Métadonnées
    time_taken_seconds: Optional[int] = None
    user_id: str = ""
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertir en dictionnaire"""
        return asdict(self)


@dataclass
class StrategyPattern:
    """Pattern détecté dans l'utilisation de stratégies"""
    strategy: str
    success_rate: float
    usage_count: int
    avg_difficulty: float
    contexts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StrategyPortfolio:
    """
    Portfolio de stratégies d'un élève
    Track stratégies, patterns, efficacité
    """

    def __init__(self, user_id: str, storage_path: str = "user_profiles"):
        self.user_id = user_id
        self.storage_path = Path(storage_path)
        self.reflections: List[ReflectionData] = []
        self.strategy_stats: Dict[str, Dict[str, Any]] = {}

        # Créer dossier si nécessaire
        self.user_dir = self.storage_path / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)

        # Charger données existantes
        self.load()

    def add_reflection(self, reflection: ReflectionData):
        """Ajouter une nouvelle réflexion"""
        self.reflections.append(reflection)
        self._update_strategy_stats(reflection)
        self.save()

    def _update_strategy_stats(self, reflection: ReflectionData):
        """Mettre à jour statistiques de stratégies"""
        strategy = reflection.strategy_used

        if strategy not in self.strategy_stats:
            self.strategy_stats[strategy] = {
                'count': 0,
                'successes': 0,
                'total_difficulty': 0,
                'contexts': []
            }

        stats = self.strategy_stats[strategy]
        stats['count'] += 1
        if reflection.was_correct:
            stats['successes'] += 1
        stats['total_difficulty'] += reflection.perceived_difficulty

        # Ajouter contexte (type d'exercice)
        if reflection.exercise_type not in stats['contexts']:
            stats['contexts'].append(reflection.exercise_type)

    def get_strategy_patterns(self) -> List[StrategyPattern]:
        """Obtenir patterns de stratégies"""
        patterns = []

        for strategy, stats in self.strategy_stats.items():
            if stats['count'] == 0:
                continue

            pattern = StrategyPattern(
                strategy=strategy,
                success_rate=stats['successes'] / stats['count'],
                usage_count=stats['count'],
                avg_difficulty=stats['total_difficulty'] / stats['count'],
                contexts=stats['contexts']
            )
            patterns.append(pattern)

        # Trier par usage
        patterns.sort(key=lambda p: p.usage_count, reverse=True)
        return patterns

    def get_most_successful_strategy(self) -> Optional[StrategyPattern]:
        """Obtenir la stratégie la plus efficace"""
        patterns = self.get_strategy_patterns()
        if not patterns:
            return None

        # Filtrer stratégies avec au moins 3 usages
        patterns = [p for p in patterns if p.usage_count >= 3]
        if not patterns:
            return None

        # Trier par taux de succès
        patterns.sort(key=lambda p: p.success_rate, reverse=True)
        return patterns[0]

    def get_reflection_count(self) -> int:
        """Nombre total de réflexions"""
        return len(self.reflections)

    def get_recent_reflections(self, count: int = 10) -> List[ReflectionData]:
        """Obtenir les N dernières réflexions"""
        return self.reflections[-count:] if self.reflections else []

    def save(self):
        """Sauvegarder portfolio"""
        reflections_file = self.user_dir / "reflections.json"

        data = {
            'user_id': self.user_id,
            'reflections': [r.to_dict() for r in self.reflections],
            'strategy_stats': self.strategy_stats,
            'last_updated': datetime.now().isoformat()
        }

        with open(reflections_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self):
        """Charger portfolio"""
        reflections_file = self.user_dir / "reflections.json"

        if not reflections_file.exists():
            return

        try:
            with open(reflections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruire réflexions
            self.reflections = [
                ReflectionData(**r) for r in data.get('reflections', [])
            ]

            self.strategy_stats = data.get('strategy_stats', {})

        except Exception as e:
            print(f"Erreur chargement portfolio: {e}")
            self.reflections = []
            self.strategy_stats = {}


class MetacognitionEngine:
    """
    Moteur de métacognition - génère questions réflexives
    et analyse patterns d'apprentissage
    """

    # Stratégies disponibles
    STRATEGIES = [
        "Doigts",      # Compter sur les doigts
        "Mental",      # Calcul mental
        "Dessin",      # Dessiner/visualiser
        "Formule",     # Utiliser une formule/règle
        "Autre"        # Autre stratégie
    ]

    # Templates de questions réflexives
    STRATEGY_QUESTIONS = {
        "question": "🎯 Quelle stratégie as-tu utilisée ?",
        "options": STRATEGIES,
        "type": "multiple_choice"
    }

    DIFFICULTY_QUESTION = {
        "question": "📊 Comment tu as trouvé cet exercice ?",
        "type": "slider",
        "min": 1,
        "max": 5,
        "labels": ["Très facile", "Facile", "Moyen", "Difficile", "Très difficile"]
    }

    EXPLANATION_QUESTION = {
        "question": "💬 Comment tu as trouvé la réponse ? (optionnel)",
        "type": "text",
        "placeholder": "Explique comment tu as fait...",
        "max_chars": 200
    }

    INTENTION_QUESTION = {
        "question": "🔮 La prochaine fois, je vais...",
        "type": "text",
        "placeholder": "Essayer de...",
        "max_chars": 150
    }

    def __init__(self, user_id: str, storage_path: str = "user_profiles"):
        self.user_id = user_id
        self.portfolio = StrategyPortfolio(user_id, storage_path)
        self.current_session_reflections: List[ReflectionData] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_reflection_questions(
        self,
        exercise: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Générer les 4 questions de réflexion

        Returns:
            Liste de dictionnaires avec structure de question
        """
        questions = [
            self.STRATEGY_QUESTIONS,
            self.DIFFICULTY_QUESTION,
            self.EXPLANATION_QUESTION,
            self.INTENTION_QUESTION
        ]

        return questions

    def process_reflection(
        self,
        reflection_data: Dict[str, Any],
        exercise: Dict[str, Any],
        was_correct: bool,
        time_taken: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Traiter une réflexion post-exercice

        Args:
            reflection_data: Réponses aux questions
            exercise: Exercice complété
            was_correct: Réponse correcte?
            time_taken: Temps pris (secondes)

        Returns:
            Analyse et insights
        """
        # Créer objet ReflectionData
        reflection = ReflectionData(
            timestamp=datetime.now().isoformat(),
            exercise_type=exercise.get('type', 'unknown'),
            difficulty_level=exercise.get('difficulty', 'CE2'),
            was_correct=was_correct,
            strategy_used=reflection_data.get('strategy', 'Mental'),
            strategy_other=reflection_data.get('strategy_other'),
            perceived_difficulty=reflection_data.get('difficulty', 3),
            self_explanation=reflection_data.get('explanation'),
            future_intention=reflection_data.get('intention'),
            time_taken_seconds=time_taken,
            user_id=self.user_id,
            session_id=self.session_id
        )

        # Ajouter au portfolio
        self.portfolio.add_reflection(reflection)
        self.current_session_reflections.append(reflection)

        # Analyser patterns
        insights = self._generate_insights(reflection)

        return {
            'reflection': reflection.to_dict(),
            'insights': insights,
            'total_reflections': self.portfolio.get_reflection_count()
        }

    def _generate_insights(self, reflection: ReflectionData) -> Dict[str, Any]:
        """
        Générer insights basés sur la réflexion

        Returns:
            Dict avec insights personnalisés
        """
        insights = {
            'strategy_effectiveness': None,
            'pattern_detected': None,
            'recommendation': None,
            'encouragement': None
        }

        # Analyser efficacité de la stratégie
        patterns = self.portfolio.get_strategy_patterns()
        current_strategy_pattern = None

        for pattern in patterns:
            if pattern.strategy == reflection.strategy_used:
                current_strategy_pattern = pattern
                break

        if current_strategy_pattern and current_strategy_pattern.usage_count >= 3:
            success_rate = current_strategy_pattern.success_rate

            if success_rate >= 0.8:
                insights['strategy_effectiveness'] = {
                    'level': 'high',
                    'message': f"Ta stratégie '{reflection.strategy_used}' marche super bien ! ({int(success_rate*100)}% de réussite)"
                }
            elif success_rate >= 0.5:
                insights['strategy_effectiveness'] = {
                    'level': 'medium',
                    'message': f"Ta stratégie '{reflection.strategy_used}' marche assez bien ({int(success_rate*100)}%)."
                }
            else:
                insights['strategy_effectiveness'] = {
                    'level': 'low',
                    'message': f"Peut-être essayer une autre stratégie ? '{reflection.strategy_used}' ne marche que {int(success_rate*100)}% du temps."
                }

        # Détecter patterns
        if len(patterns) >= 2:
            best_strategy = self.portfolio.get_most_successful_strategy()
            if best_strategy and best_strategy.strategy != reflection.strategy_used:
                if best_strategy.success_rate > 0.75:
                    insights['pattern_detected'] = {
                        'type': 'better_strategy_available',
                        'message': f"💡 Tu réussis mieux avec '{best_strategy.strategy}' ({int(best_strategy.success_rate*100)}% de réussite) !"
                    }

        # Recommandations basées sur difficulté perçue vs réussite
        if reflection.perceived_difficulty >= 4 and reflection.was_correct:
            insights['recommendation'] = "🌟 Excellent ! Tu as réussi un exercice difficile !"
        elif reflection.perceived_difficulty <= 2 and not reflection.was_correct:
            insights['recommendation'] = "🤔 Cet exercice semblait facile mais tu t'es trompé. Prends ton temps la prochaine fois !"

        # Encouragement
        recent_reflections = self.portfolio.get_recent_reflections(5)
        if len(recent_reflections) >= 3:
            recent_successes = sum(1 for r in recent_reflections if r.was_correct)
            success_rate = recent_successes / len(recent_reflections)

            if success_rate >= 0.8:
                insights['encouragement'] = "🔥 Tu es en pleine forme ! Continue comme ça !"
            elif success_rate >= 0.5:
                insights['encouragement'] = "💪 Tu progresses bien, continue tes efforts !"
            else:
                insights['encouragement'] = "🌱 C'est normal de se tromper, c'est comme ça qu'on apprend !"

        return insights

    def generate_self_regulation_suggestions(
        self,
        session_stats: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """
        Générer suggestions d'autorégulation basées sur la session

        Args:
            session_stats: Statistiques de session (optionnel)

        Returns:
            Liste de suggestions avec type et message
        """
        suggestions = []

        # Analyser session courante
        if not self.current_session_reflections:
            return suggestions

        session_count = len(self.current_session_reflections)
        recent = self.current_session_reflections[-5:]  # 5 dernières

        # Calculs basiques
        recent_successes = sum(1 for r in recent if r.was_correct)
        recent_difficulties = [r.perceived_difficulty for r in recent]
        avg_difficulty = sum(recent_difficulties) / len(recent_difficulties) if recent_difficulties else 3

        # Suggestion 1: Streak de succès
        if recent_successes >= 5:
            suggestions.append({
                'type': 'challenge',
                'icon': '🚀',
                'message': "5 bonnes réponses d'affilée ! Prêt pour un défi plus difficile ?"
            })

        # Suggestion 2: Frustration détectée
        if avg_difficulty >= 4 and recent_successes <= 1:
            suggestions.append({
                'type': 'pause',
                'icon': '😌',
                'message': "Ces exercices semblent difficiles. Tu veux faire une pause ?"
            })

        # Suggestion 3: Fatigue (session longue)
        if session_count >= 15:
            suggestions.append({
                'type': 'rest',
                'icon': '🌟',
                'message': "Bravo pour ta persévérance ! Peut-être c'est bon pour aujourd'hui ?"
            })

        # Suggestion 4: Changement de stratégie
        if len(recent) >= 3:
            recent_strategies = [r.strategy_used for r in recent]
            if len(set(recent_strategies)) == 1:  # Même stratégie
                best_strategy = self.portfolio.get_most_successful_strategy()
                if best_strategy and best_strategy.strategy != recent_strategies[0]:
                    suggestions.append({
                        'type': 'strategy',
                        'icon': '💡',
                        'message': f"Tu utilises toujours '{recent_strategies[0]}'. As-tu essayé '{best_strategy.strategy}' ?"
                    })

        # Suggestion 5: Encouragement général
        if session_stats:
            total = session_stats.get('total', 0)
            correct = session_stats.get('correct', 0)

            if total >= 10 and correct / total >= 0.7:
                suggestions.append({
                    'type': 'encouragement',
                    'icon': '🎉',
                    'message': f"Super session ! {correct}/{total} réussis !"
                })

        return suggestions

    def get_metacognitive_summary(self) -> Dict[str, Any]:
        """
        Obtenir un résumé métacognitif complet

        Returns:
            Résumé avec stratégies, patterns, insights
        """
        patterns = self.portfolio.get_strategy_patterns()
        best_strategy = self.portfolio.get_most_successful_strategy()

        # Statistiques générales
        total_reflections = self.portfolio.get_reflection_count()

        # Analyser progression
        recent_10 = self.portfolio.get_recent_reflections(10)
        older_10 = self.portfolio.reflections[-20:-10] if len(self.portfolio.reflections) >= 20 else []

        recent_success = sum(1 for r in recent_10 if r.was_correct) / len(recent_10) if recent_10 else 0
        older_success = sum(1 for r in older_10 if r.was_correct) / len(older_10) if older_10 else 0

        progression = None
        if len(older_10) > 0:
            if recent_success > older_success + 0.1:
                progression = "improving"
            elif recent_success < older_success - 0.1:
                progression = "declining"
            else:
                progression = "stable"

        summary = {
            'total_reflections': total_reflections,
            'strategy_patterns': [p.to_dict() for p in patterns],
            'best_strategy': best_strategy.to_dict() if best_strategy else None,
            'progression': progression,
            'recent_success_rate': recent_success,
            'session_reflections': len(self.current_session_reflections)
        }

        return summary

    def export_reflections_for_analysis(self, format: str = 'json') -> str:
        """
        Exporter réflexions pour analyse externe

        Args:
            format: 'json' ou 'csv'

        Returns:
            Chemin du fichier exporté
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = self.portfolio.user_dir / "exports"
        export_dir.mkdir(exist_ok=True)

        if format == 'json':
            export_file = export_dir / f"reflections_{timestamp}.json"

            data = {
                'user_id': self.user_id,
                'export_date': datetime.now().isoformat(),
                'total_reflections': len(self.portfolio.reflections),
                'reflections': [r.to_dict() for r in self.portfolio.reflections],
                'strategy_stats': self.portfolio.strategy_stats,
                'patterns': [p.to_dict() for p in self.portfolio.get_strategy_patterns()]
            }

            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        elif format == 'csv':
            import csv
            export_file = export_dir / f"reflections_{timestamp}.csv"

            with open(export_file, 'w', newline='', encoding='utf-8') as f:
                if self.portfolio.reflections:
                    writer = csv.DictWriter(f, fieldnames=self.portfolio.reflections[0].to_dict().keys())
                    writer.writeheader()
                    for reflection in self.portfolio.reflections:
                        writer.writerow(reflection.to_dict())

        return str(export_file)


def create_metacognition_engine(user_id: str) -> MetacognitionEngine:
    """Factory function pour créer MetacognitionEngine"""
    return MetacognitionEngine(user_id)


# Export public API
__all__ = [
    'MetacognitionEngine',
    'StrategyPortfolio',
    'ReflectionData',
    'StrategyPattern',
    'create_metacognition_engine'
]

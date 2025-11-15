"""
FeedbackEngine - Générateur de Feedback Pédagogique Transformatif
Phase 6.1.3 - MathCopain v6.4

Basé sur Hattie 2008 - Feedback avec effet-taille 0.79
Génère feedback multi-couches structuré et personnalisé
"""

import json
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from .error_analyzer import ErrorAnalyzer, ErrorAnalysisResult


@dataclass
class TransformativeFeedbackResult:
    """Résultat de feedback transformatif multi-couches"""

    # Couche 1: Réaction immédiate (5 mots max)
    immediate: str

    # Couche 2: Explication pédagogique (50 mots)
    explanation: str

    # Couche 3: Stratégie alternative (50 mots)
    strategy: Optional[str] = None

    # Couche 4: Recommandation de remédiation
    remediation: Optional[Dict[str, Any]] = None

    # Couche 5: Encouragement personnalisé
    encouragement: str = ""

    # Couche 6: Action suivante recommandée
    next_action: str = "Continuer"

    # Métadonnées
    is_correct: bool = False
    confidence: float = 0.0
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        return asdict(self)


class RemediationRecommender:
    """Recommande exercices de remédiation adaptés"""

    def __init__(self):
        self.difficulty_levels = {
            1: "très_facile",
            2: "facile",
            3: "moyen",
            4: "difficile",
            5: "très_difficile"
        }

    def recommend_exercise(
        self,
        error_analysis: ErrorAnalysisResult,
        current_difficulty: str = "CE2"
    ) -> Dict[str, Any]:
        """
        Recommande un exercice de remédiation

        Args:
            error_analysis: Analyse de l'erreur
            current_difficulty: Niveau actuel (CE1-CM2)

        Returns:
            Dict avec recommandation d'exercice
        """
        severity = error_analysis.severity
        error_type = error_analysis.error_type
        remediation_path = error_analysis.remediation_path or "review_basics"

        # Déterminer le niveau de difficulté de remédiation
        if severity >= 4:
            # Erreur sévère: revenir 2 niveaux en arrière
            target_difficulty = self._adjust_difficulty(current_difficulty, -2)
            practice_count = 5
        elif severity >= 3:
            # Erreur modérée: revenir 1 niveau
            target_difficulty = self._adjust_difficulty(current_difficulty, -1)
            practice_count = 3
        else:
            # Erreur légère: même niveau
            target_difficulty = current_difficulty
            practice_count = 2

        return {
            "exercise_path": remediation_path,
            "difficulty": target_difficulty,
            "practice_count": practice_count,
            "focus_prerequisites": error_analysis.prerequisites_gaps[:3],
            "estimated_time_minutes": practice_count * 3,
            "exercise_type": self._get_exercise_type(error_type),
            "hints_enabled": severity >= 3
        }

    def _adjust_difficulty(self, current: str, delta: int) -> str:
        """Ajuste le niveau de difficulté"""
        levels = ["CE1", "CE2", "CM1", "CM2"]
        try:
            current_idx = levels.index(current)
            new_idx = max(0, min(len(levels) - 1, current_idx + delta))
            return levels[new_idx]
        except ValueError:
            return current

    def _get_exercise_type(self, error_type: str) -> str:
        """Détermine le type d'exercice approprié"""
        mapping = {
            "Conceptual": "guided_discovery",
            "Procedural": "step_by_step_practice",
            "Calculation": "drill_practice"
        }
        return mapping.get(error_type, "mixed_practice")


class TransformativeFeedback:
    """
    Générateur de feedback pédagogique transformatif

    Génère feedback multi-couches basé sur:
    - Analyse d'erreur (ErrorAnalyzer)
    - Historique de l'élève
    - Contexte pédagogique
    """

    def __init__(self):
        self.error_analyzer = ErrorAnalyzer()
        self.remediation_recommender = RemediationRecommender()

        # Messages immédiats pré-définis
        self.immediate_success = [
            "✅ Exact!",
            "✅ Parfait!",
            "✅ Bravo!",
            "✅ C'est ça!",
            "✅ Très bien!"
        ]

        self.immediate_close = [
            "❌ C'est presque ça!",
            "❌ Tu y es presque!",
            "❌ Pas tout à fait!",
            "❌ Presque correct!",
            "❌ Tu chauffes!"
        ]

        self.immediate_wrong = [
            "❌ Pas exactement",
            "❌ Vérifions ensemble",
            "❌ Essayons autrement",
            "❌ Reprenons",
            "❌ Regardons ça"
        ]

    def process_exercise_response(
        self,
        exercise: Dict[str, Any],
        response: Any,
        expected: Any,
        user_id: str,
        user_history: Optional[Dict[str, Any]] = None,
        time_taken_seconds: Optional[int] = None
    ) -> TransformativeFeedbackResult:
        """
        Traite une réponse d'exercice et génère feedback multi-couches

        Args:
            exercise: Exercice complet {type, operation, difficulty, etc.}
            response: Réponse de l'élève
            expected: Réponse attendue
            user_id: ID de l'utilisateur
            user_history: Historique optionnel (stats, progression, etc.)
            time_taken_seconds: Temps pris pour répondre

        Returns:
            TransformativeFeedbackResult avec feedback complet
        """
        # Déterminer si réponse correcte
        is_correct = self._check_answer(response, expected)

        if is_correct:
            return self._generate_success_feedback(
                exercise,
                user_id,
                user_history,
                time_taken_seconds
            )
        else:
            # Analyser l'erreur
            error_analysis = self.error_analyzer.analyze_error_type(
                exercise,
                response,
                expected
            )

            return self._generate_failure_feedback(
                error_analysis,
                exercise,
                response,
                expected,
                user_id,
                user_history
            )

    def _check_answer(self, response: Any, expected: Any) -> bool:
        """Vérifie si la réponse est correcte"""
        # Normaliser les réponses
        resp_str = str(response).strip().lower()
        exp_str = str(expected).strip().lower()

        # Comparaison directe
        if resp_str == exp_str:
            return True

        # Essayer conversion numérique
        try:
            resp_num = self._parse_number(response)
            exp_num = self._parse_number(expected)

            if resp_num is not None and exp_num is not None:
                # Tolérance pour les décimaux
                return abs(resp_num - exp_num) < 0.001
        except:
            pass

        return False

    def _parse_number(self, value: Any) -> Optional[float]:
        """Parse un nombre depuis différents formats"""
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            try:
                # Gérer fractions
                if '/' in value:
                    parts = value.split('/')
                    return float(parts[0]) / float(parts[1])

                # Remplacer virgule par point
                value = value.replace(',', '.')
                return float(value)
            except:
                return None

        return None

    def _generate_success_feedback(
        self,
        exercise: Dict[str, Any],
        user_id: str,
        user_history: Optional[Dict[str, Any]],
        time_taken_seconds: Optional[int]
    ) -> TransformativeFeedbackResult:
        """Génère feedback pour réponse correcte"""

        # Couche 1: Immédiat
        immediate = random.choice(self.immediate_success)

        # Couche 2: Reconnaissance spécifique
        explanation = self._build_success_explanation(exercise, time_taken_seconds)

        # Couche 3: Insight (optionnel)
        strategy = self._build_success_insight(exercise, time_taken_seconds)

        # Couche 5: Encouragement personnalisé
        encouragement = self._build_success_encouragement(
            user_id,
            user_history,
            exercise
        )

        # Couche 6: Prochaine action
        next_action = self._determine_next_action_success(exercise, user_history)

        return TransformativeFeedbackResult(
            immediate=immediate,
            explanation=explanation,
            strategy=strategy,
            remediation=None,
            encouragement=encouragement,
            next_action=next_action,
            is_correct=True,
            confidence=1.0,
            timestamp=datetime.now().isoformat()
        )

    def _generate_failure_feedback(
        self,
        error_analysis: ErrorAnalysisResult,
        exercise: Dict[str, Any],
        response: Any,
        expected: Any,
        user_id: str,
        user_history: Optional[Dict[str, Any]]
    ) -> TransformativeFeedbackResult:
        """Génère feedback constructif pour erreur"""

        # Déterminer gravité
        severity = error_analysis.severity
        confidence = error_analysis.confidence

        # Couche 1: Immédiat
        if severity <= 2:
            immediate = random.choice(self.immediate_close)
        else:
            immediate = random.choice(self.immediate_wrong)

        # Couche 2: Explication de l'erreur
        explanation = self._build_error_explanation(
            error_analysis,
            exercise,
            response,
            expected
        )

        # Couche 3: Stratégie alternative
        strategy = self._build_alternative_strategy(
            error_analysis,
            exercise
        )

        # Couche 4: Remédiation
        remediation = self.remediation_recommender.recommend_exercise(
            error_analysis,
            exercise.get("difficulty", "CE2")
        )

        # Couche 5: Encouragement
        encouragement = self._build_failure_encouragement(
            error_analysis,
            user_id,
            user_history
        )

        # Couche 6: Prochaine action
        next_action = self._determine_next_action_failure(error_analysis)

        return TransformativeFeedbackResult(
            immediate=immediate,
            explanation=explanation,
            strategy=strategy,
            remediation=remediation,
            encouragement=encouragement,
            next_action=next_action,
            is_correct=False,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )

    def _build_success_explanation(
        self,
        exercise: Dict[str, Any],
        time_taken: Optional[int]
    ) -> str:
        """Construit explication pour succès"""
        operation = exercise.get("operation", "cet exercice")

        messages = [
            f"Tu as bien résolu {operation}!",
            f"Ta réponse à {operation} est correcte!",
            f"Excellente réponse pour {operation}!",
            f"Tu maîtrises bien {operation}!"
        ]

        base = random.choice(messages)

        # Ajouter mention du temps si fourni
        if time_taken and time_taken < 10:
            base += f" Et en seulement {time_taken} secondes, c'est rapide!"
        elif time_taken and time_taken > 60:
            base += " Tu as pris ton temps pour bien réfléchir, c'est bien!"

        return base

    def _build_success_insight(
        self,
        exercise: Dict[str, Any],
        time_taken: Optional[int]
    ) -> str:
        """Génère insight pour succès"""
        insights = [
            "Tu as bien appliqué la méthode!",
            "Tu comprends le concept!",
            "Ta stratégie était efficace!",
            "Tu progresses bien dans ce domaine!"
        ]
        return random.choice(insights)

    def _build_success_encouragement(
        self,
        user_id: str,
        user_history: Optional[Dict[str, Any]],
        exercise: Dict[str, Any]
    ) -> str:
        """Encouragement personnalisé pour succès"""

        if user_history and "success_rate" in user_history:
            rate = user_history["success_rate"]
            if rate > 0.8:
                return "🌟 Excellent! Tu continues sur ta lancée!"
            elif rate > 0.6:
                return "👍 Bien joué! Tu progresses régulièrement!"
            else:
                return "✨ Bravo! Tes efforts paient!"

        return "💪 Continue comme ça!"

    def _build_error_explanation(
        self,
        error_analysis: ErrorAnalysisResult,
        exercise: Dict[str, Any],
        response: Any,
        expected: Any
    ) -> str:
        """Explication pédagogique de l'erreur (max 50 mots)"""

        misconception = error_analysis.misconception
        operation = exercise.get("operation", "l'exercice")

        # Utiliser template si disponible
        if error_analysis.feedback_templates:
            # Sélectionner template approprié
            template = error_analysis.feedback_templates[0]

            # Essayer de formater avec contexte
            try:
                # Extraire nombres de l'opération
                import re
                numbers = re.findall(r'\d+', operation)

                context = {
                    'wrong': response,
                    'correct': expected,
                    'operation': operation
                }

                if len(numbers) >= 2:
                    context['a'] = numbers[0]
                    context['b'] = numbers[1]

                return template.format(**context)
            except:
                pass

        # Fallback: explication générique
        return f"Pour {operation}: tu as répondu {response} mais la bonne réponse est {expected}. {misconception}."

    def _build_alternative_strategy(
        self,
        error_analysis: ErrorAnalysisResult,
        exercise: Dict[str, Any]
    ) -> str:
        """Propose une stratégie alternative (max 50 mots)"""

        error_type = error_analysis.error_type
        exercise_type = exercise.get("type", "").lower()
        operation = exercise.get("operation", "")

        strategies = {
            "addition": [
                "Essaie en décomposant: transforme les nombres en dizaines et unités.",
                "Autre méthode: compte sur tes doigts ou utilise des jetons.",
                "Astuce: arrondis à la dizaine proche, puis ajuste le résultat."
            ],
            "subtraction": [
                "Utilise la droite numérique: pars du plus petit et avance.",
                "Pense à la différence: combien faut-il ajouter pour arriver au résultat?",
                "Essaie de décomposer en soustractions plus simples."
            ],
            "multiplication": [
                "Vois ça comme des groupes: combien de fois répètes-tu le nombre?",
                "Utilise ta table de multiplication comme référence.",
                "Décompose: multiplie par 10, puis ajuste."
            ],
            "division": [
                "Pense au partage: combien chacun reçoit?",
                "Utilise les tables à l'envers: quel nombre fois le diviseur donne le dividende?",
                "Soustrais répétitivement et compte combien de fois."
            ]
        }

        if exercise_type in strategies:
            return random.choice(strategies[exercise_type])

        return "Essaie une autre méthode: dessine le problème ou utilise du matériel concret."

    def _build_failure_encouragement(
        self,
        error_analysis: ErrorAnalysisResult,
        user_id: str,
        user_history: Optional[Dict[str, Any]]
    ) -> str:
        """Encouragement après erreur"""

        severity = error_analysis.severity

        if severity >= 4:
            encouragements = [
                "💪 Cette notion est importante. Prenons le temps de bien la comprendre ensemble!",
                "🌟 Ne t'inquiète pas! Avec de la pratique, tu vas y arriver.",
                "✨ C'est normal de faire des erreurs en apprenant. Continue!"
            ]
        elif severity >= 3:
            encouragements = [
                "👍 Pas de souci! Avec un peu de pratique, tu vas y arriver.",
                "💡 Tu es sur la bonne voie! Encore quelques essais.",
                "🎯 Presque! Tu progresses bien."
            ]
        else:
            encouragements = [
                "✨ Bravo pour ton effort! Continue comme ça.",
                "👏 Une petite erreur, rien de grave!",
                "🚀 Tu vas vite progresser, continue!"
            ]

        return random.choice(encouragements)

    def _determine_next_action_success(
        self,
        exercise: Dict[str, Any],
        user_history: Optional[Dict[str, Any]]
    ) -> str:
        """Détermine action suivante après succès"""

        # Si l'élève réussit bien, proposer niveau supérieur
        if user_history and user_history.get("success_rate", 0) > 0.8:
            return "Niveau suivant"

        return "Continuer"

    def _determine_next_action_failure(
        self,
        error_analysis: ErrorAnalysisResult
    ) -> str:
        """Détermine action suivante après erreur"""

        severity = error_analysis.severity

        if severity >= 4:
            return "Voir explication détaillée"
        elif severity >= 3:
            return "Refaire exercice similaire"
        else:
            return "Réessayer"


# Alias pour compatibilité
FeedbackGenerator = TransformativeFeedback

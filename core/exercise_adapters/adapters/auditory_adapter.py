"""
AuditoryAdapter - Phase 6.3.2
Adapter for auditory learners (Gardner's Musical-Rhythmic Intelligence)
Focuses on: verbal explanations, sounds, rhythm, reading aloud
"""

from typing import Dict, Any, List


class AuditoryAdapter:
    """
    Adapter for auditory learning style
    Emphasizes verbal explanations, rhythm, and sound-based learning
    """

    def __init__(self):
        self.style = "auditory"

    def format_problem(self, problem: str) -> str:
        """
        Format problem with auditory emphasis

        Args:
            problem: Original problem string

        Returns:
            Formatted problem for auditory learning
        """
        # Add auditory icon and instruction
        formatted = f"🎵 **Lis à voix haute:** {problem}"

        # Add phonetic hints for pronunciation
        formatted = self._add_verbal_cues(formatted)

        return formatted

    def _add_verbal_cues(self, text: str) -> str:
        """Add verbal cues for how to say the problem"""
        # Add hints for proper pronunciation
        cues = {
            " + ": " plus ",
            " - ": " moins ",
            " × ": " fois ",
            " ÷ ": " divisé par ",
            " = ": " égale "
        }

        verbal_text = text
        for symbol, word in cues.items():
            verbal_text = verbal_text.replace(symbol, word)

        return verbal_text

    def format_hint(self, hint: str) -> str:
        """
        Format hint with auditory elements

        Args:
            hint: Original hint

        Returns:
            Auditory formatted hint
        """
        return f"👂 **Écoute bien:** {hint} (Répète cette phrase 3 fois)"

    def generate_audio_instructions(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate audio-friendly instructions

        Args:
            exercise: Exercise dictionary

        Returns:
            Dictionary with audio instructions
        """
        operation = exercise.get("operation", "")
        ex_type = exercise.get("type", "")

        # Create verbal explanation
        verbal_steps = self._create_verbal_steps(operation, ex_type)

        audio_aids = {
            "type": "auditory",
            "read_aloud_text": self._create_read_aloud_text(operation),
            "verbal_steps": verbal_steps,
            "rhythm_pattern": self._create_rhythm_pattern(ex_type),
            "pronunciation_guide": self._create_pronunciation_guide(operation)
        }

        return audio_aids

    def _create_read_aloud_text(self, operation: str) -> str:
        """Create text optimized for reading aloud"""
        # Convert to full verbal form
        verbal = operation
        conversions = {
            "+": "plus",
            "-": "moins",
            "×": "fois",
            "÷": "divisé par",
            "=": "égale"
        }

        for symbol, word in conversions.items():
            verbal = verbal.replace(symbol, f" {word} ")

        return f"Dis à voix haute: '{verbal}'"

    def _create_verbal_steps(self, operation: str, ex_type: str) -> List[str]:
        """Create step-by-step verbal instructions"""
        if ex_type == "addition":
            return [
                "Étape 1: Dis le premier nombre à voix haute",
                "Étape 2: Dis 'plus'",
                "Étape 3: Dis le deuxième nombre",
                "Étape 4: Compte en chantant si besoin"
            ]
        elif ex_type == "multiplication":
            return [
                "Étape 1: Répète la table en chantant",
                "Étape 2: Dis 'X fois Y égale...'",
                "Étape 3: Trouve le résultat en récitant"
            ]
        else:
            return [
                "Étape 1: Lis le problème à voix haute",
                "Étape 2: Explique ce que tu dois faire",
                "Étape 3: Dis chaque étape en la faisant"
            ]

    def _create_rhythm_pattern(self, ex_type: str) -> Dict[str, str]:
        """Create rhythm/song pattern for memorization"""
        patterns = {
            "addition": "🎵 Chante: 'Plus-plus-plus, on additionne!'",
            "subtraction": "🎵 Chante: 'Moins-moins-moins, on enlève!'",
            "multiplication": "🎵 Chante: 'Fois-fois-fois, on multiplie!'",
            "division": "🎵 Chante: 'Partage en groupes égaux!'"
        }

        return {
            "pattern": patterns.get(ex_type, "🎵 Chante le problème!"),
            "tempo": "Tempo modéré, répète 3 fois"
        }

    def _create_pronunciation_guide(self, operation: str) -> str:
        """Create pronunciation guide for numbers"""
        return "Prononce chaque chiffre clairement et lentement"

    def suggest_resources(self, exercise_type: str) -> Dict[str, List[str]]:
        """
        Suggest auditory learning resources

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        resources = {
            "audio": [],
            "verbal_techniques": [],
            "tips": []
        }

        # Audio resources
        resources["audio"] = [
            "Écoute des chansons de multiplication",
            "Utilise des comptines pour mémoriser",
            "Enregistre-toi en train de réciter les étapes"
        ]

        # Verbal techniques
        resources["verbal_techniques"] = [
            "Explique le problème à quelqu'un",
            "Récite les étapes à voix haute",
            "Invente une chanson avec les nombres",
            "Crée des rimes pour mémoriser"
        ]

        # Auditory learning tips
        resources["tips"] = [
            "🎵 Chante les tables de multiplication",
            "👂 Lis toujours le problème à voix haute",
            "🗣️ Explique ton raisonnement en parlant",
            "🎧 Travaille dans un endroit calme pour mieux te concentrer"
        ]

        return resources

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt complete exercise for auditory learner

        Args:
            exercise: Original exercise

        Returns:
            Fully adapted exercise
        """
        adapted = {
            "problem_statement": self.format_problem(exercise.get("operation", "")),
            "hint": self.format_hint(exercise.get("hint", "Écoute bien les instructions")),
            "audio_aids": self.generate_audio_instructions(exercise),
            "explanation_style": "auditory",
            "resource_suggestions": self.suggest_resources(exercise.get("type", "general")),
            "presentation_tips": [
                "Encourage à lire à voix haute",
                "Utilise des explications verbales détaillées",
                "Propose des chansons et comptines",
                "Suggère de réciter les étapes"
            ]
        }

        return adapted

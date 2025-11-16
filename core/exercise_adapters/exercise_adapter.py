"""
ExercisePresenterAdapter - Phase 6.3.2
Main adapter that routes exercises to appropriate style-specific adapters

Based on:
- Gardner (1983) - Multiple Intelligences
- Dunn & Dunn (1978) - Learning Style Model
- Kolb (1984) - Experiential Learning Theory

Engagement improvement: +25-35% when adapted to student's learning style
"""

from typing import Dict, Any, Optional
from core.exercise_adapters.adapters import (
    VisualAdapter,
    AuditoryAdapter,
    KinestheticAdapter,
    LogicalAdapter,
    NarrativeAdapter
)


class ExercisePresenterAdapter:
    """
    Main adapter that formats exercises according to learning style

    Routes exercises to the appropriate style-specific adapter
    and returns adapted presentation
    """

    # Supported learning styles
    SUPPORTED_STYLES = ["visual", "auditory", "kinesthetic", "logical", "narrative"]

    def __init__(self, learning_style: str = "visual"):
        """
        Initialize adapter with learning style

        Args:
            learning_style: One of ["visual", "auditory", "kinesthetic", "logical", "narrative"]

        Raises:
            ValueError: If learning_style is not supported
        """
        if learning_style not in self.SUPPORTED_STYLES:
            raise ValueError(
                f"Unsupported learning style: {learning_style}. "
                f"Must be one of {self.SUPPORTED_STYLES}"
            )

        self.style = learning_style

        # Initialize all adapters (singleton pattern)
        self.adapters = {
            "visual": VisualAdapter(),
            "auditory": AuditoryAdapter(),
            "kinesthetic": KinestheticAdapter(),
            "logical": LogicalAdapter(),
            "narrative": NarrativeAdapter()
        }

        # Current active adapter
        self.current_adapter = self.adapters[learning_style]

    def set_learning_style(self, learning_style: str):
        """
        Change the current learning style

        Args:
            learning_style: New learning style to use

        Raises:
            ValueError: If learning_style is not supported
        """
        if learning_style not in self.SUPPORTED_STYLES:
            raise ValueError(
                f"Unsupported learning style: {learning_style}. "
                f"Must be one of {self.SUPPORTED_STYLES}"
            )

        self.style = learning_style
        self.current_adapter = self.adapters[learning_style]

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt exercise to current learning style

        Args:
            exercise: Exercise dictionary containing:
                - operation: str (e.g., "5 + 3 = ?")
                - type: str (e.g., "addition", "multiplication")
                - difficulty: int (1-5)
                - hint: str (optional)

        Returns:
            Adapted exercise dictionary with:
                - problem_statement: Adapted problem text
                - hint: Adapted hint
                - visual_aids/audio_aids/etc: Style-specific aids
                - explanation_style: Current style
                - resource_suggestions: Learning resources
                - presentation_tips: Teaching tips
        """
        if not exercise:
            raise ValueError("Exercise cannot be empty")

        # Validate exercise structure
        if "operation" not in exercise and "question" not in exercise:
            raise ValueError("Exercise must contain 'operation' or 'question' field")

        # Normalize exercise format
        normalized_exercise = self._normalize_exercise(exercise)

        # Route to appropriate adapter
        adapted = self.current_adapter.adapt_exercise(normalized_exercise)

        # Add metadata
        adapted["original_exercise"] = exercise
        adapted["adapted_for_style"] = self.style
        adapted["adapter_version"] = "6.3.2"

        return adapted

    def _normalize_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize exercise format for adapters"""
        normalized = exercise.copy()

        # Handle different field names
        if "question" in exercise and "operation" not in exercise:
            normalized["operation"] = exercise["question"]

        # Set defaults
        if "type" not in normalized:
            normalized["type"] = self._infer_type(normalized.get("operation", ""))

        if "difficulty" not in normalized:
            normalized["difficulty"] = 1

        if "hint" not in normalized:
            normalized["hint"] = self._generate_default_hint(normalized["type"])

        return normalized

    def _infer_type(self, operation: str) -> str:
        """Infer exercise type from operation string"""
        if "+" in operation or "plus" in operation.lower():
            return "addition"
        elif "-" in operation or "moins" in operation.lower():
            return "subtraction"
        elif "×" in operation or "*" in operation or "fois" in operation.lower():
            return "multiplication"
        elif "÷" in operation or "/" in operation or "divisé" in operation.lower():
            return "division"
        else:
            return "general"

    def _generate_default_hint(self, ex_type: str) -> str:
        """Generate default hint based on exercise type"""
        hints = {
            "addition": "Additionne les deux nombres",
            "subtraction": "Soustrais le deuxième nombre du premier",
            "multiplication": "Multiplie les deux nombres",
            "division": "Divise le premier nombre par le deuxième",
            "general": "Lis bien le problème"
        }
        return hints.get(ex_type, "Réfléchis bien")

    def format_problem(self, problem: str) -> str:
        """
        Format problem statement according to current style

        Args:
            problem: Original problem string

        Returns:
            Formatted problem string
        """
        return self.current_adapter.format_problem(problem)

    def format_hint(self, hint: str) -> str:
        """
        Format hint according to current style

        Args:
            hint: Original hint

        Returns:
            Formatted hint
        """
        return self.current_adapter.format_hint(hint)

    def get_resource_suggestions(self, exercise_type: str = "general") -> Dict[str, Any]:
        """
        Get learning resources for current style

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        return self.current_adapter.suggest_resources(exercise_type)

    def get_presentation_tips(self) -> Dict[str, Any]:
        """
        Get presentation tips for current learning style

        Returns:
            Dictionary with teaching tips and best practices
        """
        tips = {
            "visual": {
                "emphasis": "Use colors, diagrams, and visual representations",
                "materials": ["Charts", "Diagrams", "Color-coding", "Visual patterns"],
                "approach": "Show before tell",
                "avoid": "Too much verbal explanation without visuals"
            },
            "auditory": {
                "emphasis": "Use verbal explanations and sound-based learning",
                "materials": ["Verbal instructions", "Songs", "Rhymes", "Discussions"],
                "approach": "Explain verbally and encourage reading aloud",
                "avoid": "Silent work without verbal processing"
            },
            "kinesthetic": {
                "emphasis": "Use hands-on activities and movement",
                "materials": ["Manipulatives", "Physical objects", "Interactive elements"],
                "approach": "Let them manipulate and discover",
                "avoid": "Passive sitting without physical engagement"
            },
            "logical": {
                "emphasis": "Explain the 'why' and show patterns",
                "materials": ["Logic puzzles", "Pattern activities", "Reasoning steps"],
                "approach": "Explain underlying logic and connections",
                "avoid": "Rote memorization without understanding"
            },
            "narrative": {
                "emphasis": "Use stories and real-world contexts",
                "materials": ["Story problems", "Real-life scenarios", "Examples"],
                "approach": "Frame everything in a story or context",
                "avoid": "Abstract problems without context"
            }
        }

        return tips.get(self.style, {})

    def get_current_style(self) -> str:
        """Get current learning style"""
        return self.style

    def get_adapter(self, style: Optional[str] = None) -> Any:
        """
        Get specific adapter

        Args:
            style: Learning style (if None, returns current adapter)

        Returns:
            Adapter instance

        Raises:
            ValueError: If style is not supported
        """
        if style is None:
            return self.current_adapter

        if style not in self.SUPPORTED_STYLES:
            raise ValueError(f"Unsupported learning style: {style}")

        return self.adapters[style]

    def adapt_multiple_exercises(
        self,
        exercises: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Adapt multiple exercises at once

        Args:
            exercises: List of exercise dictionaries

        Returns:
            List of adapted exercises
        """
        if not exercises:
            return []

        return [self.adapt_exercise(ex) for ex in exercises]

    def compare_adaptations(
        self,
        exercise: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare how exercise would be adapted for all styles

        Useful for demonstration and research purposes

        Args:
            exercise: Exercise to adapt

        Returns:
            Dictionary mapping style -> adapted exercise
        """
        comparisons = {}

        for style in self.SUPPORTED_STYLES:
            adapter = self.adapters[style]
            comparisons[style] = adapter.adapt_exercise(exercise)

        return comparisons


def create_adapter(learning_style: str = "visual") -> ExercisePresenterAdapter:
    """
    Factory function to create ExercisePresenterAdapter

    Args:
        learning_style: Learning style to use

    Returns:
        ExercisePresenterAdapter instance
    """
    return ExercisePresenterAdapter(learning_style)


# Export public API
__all__ = [
    'ExercisePresenterAdapter',
    'create_adapter'
]

"""
VisualAdapter - Phase 6.3.2
Adapter for visual learners (Gardner's Spatial Intelligence)
Focuses on: diagrams, colors, visual patterns, spatial representation
"""

from typing import Dict, Any, List, Optional
import random


class VisualAdapter:
    """
    Adapter for visual learning style
    Adds visual aids, color coding, diagrams, and spatial representations
    """

    # Visual formatting elements
    ICONS = {
        "addition": "➕",
        "subtraction": "➖",
        "multiplication": "✖️",
        "division": "➗",
        "equals": "🟰",
        "number": "🔢",
        "diagram": "📊",
        "chart": "📈",
        "visual": "👁️",
        "pattern": "🔷"
    }

    COLORS = {
        "red": "🔴",
        "blue": "🔵",
        "green": "🟢",
        "yellow": "🟡",
        "purple": "🟣",
        "orange": "🟠"
    }

    def __init__(self):
        self.style = "visual"

    def format_problem(self, problem: str) -> str:
        """
        Format problem with visual emphasis

        Args:
            problem: Original problem string

        Returns:
            Formatted problem with visual elements
        """
        # Add visual icon
        formatted = f"👁️ **Visualise:** {problem}"

        # Add color coding for operators
        formatted = self._add_operator_icons(formatted)

        return formatted

    def _add_operator_icons(self, text: str) -> str:
        """Add visual icons for mathematical operators"""
        replacements = {
            " + ": f" {self.ICONS['addition']} ",
            " - ": f" {self.ICONS['subtraction']} ",
            " × ": f" {self.ICONS['multiplication']} ",
            " ÷ ": f" {self.ICONS['division']} ",
            " = ": f" {self.ICONS['equals']} "
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def format_hint(self, hint: str) -> str:
        """
        Format hint with visual elements

        Args:
            hint: Original hint

        Returns:
            Visually formatted hint
        """
        return f"💡 **Regarde bien:** {hint}"

    def generate_visuals(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate visual aids for the exercise

        Args:
            exercise: Exercise dictionary with type, operation, difficulty

        Returns:
            Dictionary with visual aids
        """
        visual_aids = {
            "type": "visual",
            "elements": []
        }

        # Add number line if applicable
        if self._should_show_number_line(exercise):
            visual_aids["elements"].append(
                self._generate_number_line(exercise)
            )

        # Add diagram if applicable
        if self._should_show_diagram(exercise):
            visual_aids["elements"].append(
                self._generate_diagram(exercise)
            )

        # Add color coding
        visual_aids["elements"].append(
            self._generate_color_coding(exercise)
        )

        # Add visual pattern
        if exercise.get("type") == "multiplication":
            visual_aids["elements"].append(
                self._generate_multiplication_grid(exercise)
            )

        return visual_aids

    def _should_show_number_line(self, exercise: Dict[str, Any]) -> bool:
        """Determine if number line should be shown"""
        return exercise.get("type") in ["addition", "subtraction"] and \
               exercise.get("difficulty", 1) <= 3

    def _should_show_diagram(self, exercise: Dict[str, Any]) -> bool:
        """Determine if diagram should be shown"""
        return exercise.get("type") in ["division", "fractions", "geometry"]

    def _generate_number_line(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ASCII number line representation

        Args:
            exercise: Exercise data

        Returns:
            Number line visual aid
        """
        operation = exercise.get("operation", "")

        # Extract numbers (simple parsing)
        try:
            parts = operation.replace("=", "").split()
            if len(parts) >= 3:
                num1 = int(parts[0])
                num2 = int(parts[2])

                # Create number line range
                start = max(0, min(num1, num2) - 2)
                end = max(num1, num2) + 3

                line = "".join([f"{i:3d}" for i in range(start, end)])
                marks = "---" * (end - start)

                return {
                    "element": "number_line",
                    "range": [start, end],
                    "representation": f"{line}\n{marks}",
                    "highlight_numbers": [num1, num2]
                }
        except:
            pass

        return {"element": "number_line", "representation": "0---1---2---3---4---5"}

    def _generate_diagram(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diagram for exercise"""
        ex_type = exercise.get("type", "")

        if ex_type == "division":
            return {
                "element": "diagram",
                "type": "division_groups",
                "description": "📦 Divise les objets en groupes égaux"
            }
        elif ex_type == "fractions":
            return {
                "element": "diagram",
                "type": "fraction_circle",
                "description": "🍕 Imagine une pizza coupée en parts"
            }
        else:
            return {
                "element": "diagram",
                "type": "generic",
                "description": f"{self.ICONS['diagram']} Représentation visuelle"
            }

    def _generate_color_coding(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Generate color coding suggestions"""
        return {
            "element": "color_coding",
            "suggestions": {
                "operands": "Utilise le 🔵 bleu pour le 1er nombre, 🟢 vert pour le 2ème",
                "operator": "L'opération en 🔴 rouge",
                "result": "La réponse en 🟡 jaune"
            }
        }

    def _generate_multiplication_grid(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Generate multiplication grid/array"""
        return {
            "element": "multiplication_grid",
            "description": "📊 Utilise une grille pour visualiser",
            "example": "3 × 4 = 3 rangées de 4 objets = □□□□\n                                    □□□□\n                                    □□□□"
        }

    def suggest_resources(self, exercise_type: str) -> Dict[str, List[str]]:
        """
        Suggest visual learning resources

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        resources = {
            "videos": [],
            "tools": [],
            "tips": []
        }

        # Video suggestions (visual explanations)
        resources["videos"] = [
            "Regarde une vidéo explicative avec des animations",
            "Cherche des tutoriels visuels sur YouTube",
            f"Vidéo: 'Comment visualiser {exercise_type}'"
        ]

        # Visual tools
        resources["tools"] = [
            "Utilise des cubes de couleur pour compter",
            "Dessine des schémas sur papier",
            "Utilise une règle graduée pour visualiser les nombres",
            "Crée un tableau ou diagramme"
        ]

        # Visual learning tips
        resources["tips"] = [
            "💡 Dessine toujours un schéma avant de calculer",
            "🎨 Utilise des couleurs différentes pour chaque nombre",
            "📐 Utilise une ligne numérique pour t'aider",
            "👁️ Ferme les yeux et imagine le problème visuellement"
        ]

        return resources

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt complete exercise for visual learner

        Args:
            exercise: Original exercise

        Returns:
            Fully adapted exercise
        """
        adapted = {
            "problem_statement": self.format_problem(exercise.get("operation", "")),
            "hint": self.format_hint(exercise.get("hint", "Regarde bien les nombres")),
            "visual_aids": self.generate_visuals(exercise),
            "explanation_style": "visual",
            "resource_suggestions": self.suggest_resources(exercise.get("type", "general")),
            "presentation_tips": [
                "Utilise des couleurs et des formes",
                "Montre des diagrammes et graphiques",
                "Encourage à dessiner la solution"
            ]
        }

        return adapted

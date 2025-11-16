"""
KinestheticAdapter - Phase 6.3.2
Adapter for kinesthetic learners (Gardner's Bodily-Kinesthetic Intelligence)
Focuses on: hands-on activities, movement, manipulation, tactile learning
"""

from typing import Dict, Any, List


class KinestheticAdapter:
    """
    Adapter for kinesthetic learning style
    Emphasizes physical manipulation, movement, and hands-on practice
    """

    # Manipulative objects for different operations
    MANIPULATIVES = {
        "addition": ["cubes", "counters", "fingers", "blocks"],
        "subtraction": ["counters", "objects", "toys"],
        "multiplication": ["arrays", "groups", "blocks"],
        "division": ["objects to share", "counters", "blocks"],
        "fractions": ["pizza slices", "cake pieces", "paper strips"]
    }

    def __init__(self):
        self.style = "kinesthetic"

    def format_problem(self, problem: str) -> str:
        """
        Format problem with kinesthetic emphasis

        Args:
            problem: Original problem string

        Returns:
            Formatted problem for kinesthetic learning
        """
        # Add kinesthetic icon and action instruction
        formatted = f"✋ **Manipule et essaie:** {problem}"

        return formatted

    def format_hint(self, hint: str) -> str:
        """
        Format hint with kinesthetic elements

        Args:
            hint: Original hint

        Returns:
            Kinesthetic formatted hint
        """
        return f"👆 **Utilise tes mains:** {hint}"

    def generate_interactive_activities(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate hands-on activities for the exercise

        Args:
            exercise: Exercise dictionary

        Returns:
            Dictionary with interactive activities
        """
        ex_type = exercise.get("type", "")
        operation = exercise.get("operation", "")

        activities = {
            "type": "kinesthetic",
            "manipulatives": self._suggest_manipulatives(ex_type),
            "physical_actions": self._create_physical_actions(ex_type, operation),
            "interactive_elements": self._create_interactive_elements(ex_type),
            "movement_based_learning": self._create_movement_activities(ex_type)
        }

        return activities

    def _suggest_manipulatives(self, ex_type: str) -> List[Dict[str, str]]:
        """Suggest physical objects to manipulate"""
        objects = self.MANIPULATIVES.get(ex_type, ["cubes", "counters"])

        suggestions = []
        for obj in objects:
            suggestions.append({
                "object": obj,
                "usage": f"Utilise des {obj} pour compter et résoudre"
            })

        return suggestions

    def _create_physical_actions(self, ex_type: str, operation: str) -> List[str]:
        """Create step-by-step physical actions"""
        if ex_type == "addition":
            return [
                "📍 Prends des cubes de couleur",
                "📍 Mets le premier nombre de cubes à gauche",
                "📍 Ajoute le deuxième nombre de cubes",
                "📍 Compte tous les cubes avec tes doigts"
            ]
        elif ex_type == "subtraction":
            return [
                "📍 Prends le nombre total de jetons",
                "📍 Enlève physiquement le nombre à soustraire",
                "📍 Compte ce qui reste avec tes mains"
            ]
        elif ex_type == "multiplication":
            return [
                "📍 Crée des groupes égaux avec des objets",
                "📍 Compte combien de groupes tu as",
                "📍 Compte combien d'objets par groupe",
                "📍 Rassemble tous les objets et compte le total"
            ]
        elif ex_type == "division":
            return [
                "📍 Prends tous les objets à partager",
                "📍 Distribue-les un par un dans des groupes",
                "📍 Continue jusqu'à tout distribuer",
                "📍 Compte combien dans chaque groupe"
            ]
        else:
            return [
                "📍 Utilise tes doigts ou des objets",
                "📍 Manipule pour visualiser le problème",
                "📍 Essaie différentes façons de résoudre"
            ]

    def _create_interactive_elements(self, ex_type: str) -> Dict[str, Any]:
        """Create interactive UI elements suggestions"""
        elements = {
            "draggable_objects": True,
            "click_to_count": True,
            "touch_friendly": True
        }

        if ex_type in ["addition", "subtraction"]:
            elements["drag_drop_counters"] = {
                "description": "Glisse-dépose des jetons pour compter",
                "interaction": "drag_and_drop"
            }

        if ex_type == "multiplication":
            elements["build_arrays"] = {
                "description": "Construis des tableaux en cliquant",
                "interaction": "click_to_build"
            }

        if ex_type == "division":
            elements["distribute_objects"] = {
                "description": "Distribue les objets en cliquant",
                "interaction": "click_to_distribute"
            }

        return elements

    def _create_movement_activities(self, ex_type: str) -> List[str]:
        """Create whole-body movement activities"""
        movements = [
            "🚶 Fais des pas pour compter",
            "👏 Tape dans tes mains à chaque nombre",
            "🤸 Saute pour chaque groupe"
        ]

        if ex_type == "multiplication":
            movements.append("🔄 Fais des groupes avec tes amis")
            movements.append("👫 Crée des rangées de personnes")

        if ex_type == "addition":
            movements.append("🏃 Cours pour chercher des objets à additionner")

        return movements

    def suggest_resources(self, exercise_type: str) -> Dict[str, List[str]]:
        """
        Suggest kinesthetic learning resources

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        resources = {
            "physical_materials": [],
            "activities": [],
            "tips": []
        }

        # Physical materials
        resources["physical_materials"] = [
            "Cubes de couleur ou Lego",
            "Jetons ou pièces de monnaie",
            "Bâtonnets de glace",
            "Pâte à modeler",
            "Cartes à jouer",
            "Doigts et orteils (toujours disponibles!)"
        ]

        # Hands-on activities
        resources["activities"] = [
            "Construis avec des blocks",
            "Dessine et découpe des formes",
            "Utilise des objets du quotidien",
            "Fais des gestes pour chaque étape",
            "Marche et compte en même temps"
        ]

        # Kinesthetic learning tips
        resources["tips"] = [
            "✋ Utilise toujours tes mains pour compter",
            "🏃 N'hésite pas à bouger pendant que tu réfléchis",
            "🎯 Manipule des objets réels autant que possible",
            "🤹 Essaie, teste, expérimente physiquement",
            "📦 Range et dérange les objets pour comprendre"
        ]

        return resources

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt complete exercise for kinesthetic learner

        Args:
            exercise: Original exercise

        Returns:
            Fully adapted exercise
        """
        adapted = {
            "problem_statement": self.format_problem(exercise.get("operation", "")),
            "hint": self.format_hint(exercise.get("hint", "Utilise des objets pour t'aider")),
            "interactive_activities": self.generate_interactive_activities(exercise),
            "explanation_style": "kinesthetic",
            "resource_suggestions": self.suggest_resources(exercise.get("type", "general")),
            "presentation_tips": [
                "Encourage la manipulation physique",
                "Propose des objets à toucher et compter",
                "Utilise des éléments interactifs (drag & drop)",
                "Suggère des mouvements et gestes",
                "Permet l'expérimentation active"
            ]
        }

        return adapted

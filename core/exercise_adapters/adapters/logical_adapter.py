"""
LogicalAdapter - Phase 6.3.2
Adapter for logical learners (Gardner's Logical-Mathematical Intelligence)
Focuses on: patterns, reasoning, logical structures, understanding "why"
"""

from typing import Dict, Any, List


class LogicalAdapter:
    """
    Adapter for logical learning style
    Emphasizes patterns, reasoning, cause-effect, and systematic thinking
    """

    def __init__(self):
        self.style = "logical"

    def format_problem(self, problem: str) -> str:
        """
        Format problem with logical emphasis

        Args:
            problem: Original problem string

        Returns:
            Formatted problem for logical learning
        """
        # Add logical icon and reasoning prompt
        formatted = f"🧠 **Comprends la logique:** {problem}"

        return formatted

    def format_hint(self, hint: str) -> str:
        """
        Format hint with logical explanation

        Args:
            hint: Original hint

        Returns:
            Logical formatted hint
        """
        return f"🔍 **Pourquoi?** {hint} (Cherche la logique)"

    def generate_logical_structure(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate logical structure and reasoning for exercise

        Args:
            exercise: Exercise dictionary

        Returns:
            Dictionary with logical explanations
        """
        ex_type = exercise.get("type", "")
        operation = exercise.get("operation", "")

        logical_aids = {
            "type": "logical",
            "reasoning_steps": self._create_reasoning_steps(ex_type, operation),
            "patterns": self._identify_patterns(ex_type, operation),
            "why_explanation": self._explain_why(ex_type),
            "logical_shortcuts": self._suggest_shortcuts(ex_type),
            "connections": self._make_connections(ex_type)
        }

        return logical_aids

    def _create_reasoning_steps(self, ex_type: str, operation: str) -> List[str]:
        """Create logical reasoning steps"""
        if ex_type == "addition":
            return [
                "1️⃣ Pourquoi additionne-t-on? On combine deux quantités",
                "2️⃣ Logique: Nombre 1 + Nombre 2 = Total",
                "3️⃣ Vérifie: Le total est plus grand que chaque nombre"
            ]
        elif ex_type == "multiplication":
            return [
                "1️⃣ Comprends: Multiplication = Addition répétée",
                "2️⃣ Logique: 3 × 4 = 3+3+3+3 = 4+4+4",
                "3️⃣ Pattern: 3 × 4 = 4 × 3 (commutativité)",
                "4️⃣ Structure: X groupes de Y objets"
            ]
        elif ex_type == "division":
            return [
                "1️⃣ Comprends: Division = Inverse de multiplication",
                "2️⃣ Logique: Partager équitablement",
                "3️⃣ Vérifie: Quotient × Diviseur = Dividende"
            ]
        else:
            return [
                "1️⃣ Analyse le problème logiquement",
                "2️⃣ Identifie les patterns et structures",
                "3️⃣ Applique le raisonnement"
            ]

    def _identify_patterns(self, ex_type: str, operation: str) -> List[Dict[str, str]]:
        """Identify mathematical patterns"""
        patterns = []

        if ex_type == "multiplication":
            patterns.extend([
                {
                    "pattern": "Commutativité",
                    "explanation": "a × b = b × a (l'ordre ne change pas le résultat)"
                },
                {
                    "pattern": "Patterns × 10",
                    "explanation": "Multiplier par 10 ajoute un zéro"
                },
                {
                    "pattern": "Doubles",
                    "explanation": "n × 2 = n + n"
                }
            ])

        if ex_type == "addition":
            patterns.extend([
                {
                    "pattern": "Commutativité",
                    "explanation": "a + b = b + a"
                },
                {
                    "pattern": "Associativité",
                    "explanation": "(a + b) + c = a + (b + c)"
                }
            ])

        return patterns

    def _explain_why(self, ex_type: str) -> str:
        """Explain the 'why' behind the operation"""
        explanations = {
            "addition": "🧠 Pourquoi l'addition? Pour combiner des quantités et trouver un total.",
            "subtraction": "🧠 Pourquoi la soustraction? Pour trouver la différence ou ce qui reste.",
            "multiplication": "🧠 Pourquoi la multiplication? Pour compter rapidement des groupes égaux.",
            "division": "🧠 Pourquoi la division? Pour partager équitablement ou faire des groupes."
        }
        return explanations.get(ex_type, "🧠 Comprends la logique de l'opération")

    def _suggest_shortcuts(self, ex_type: str) -> List[str]:
        """Suggest logical shortcuts and strategies"""
        shortcuts = {
            "addition": [
                "💡 Arrondis au 10 proche puis ajuste",
                "💡 Décompose en dizaines + unités",
                "💡 Cherche les compléments à 10"
            ],
            "multiplication": [
                "💡 Utilise les doubles: 4×7 = 2×(2×7)",
                "💡 Multiplier par 5: divise par 2, puis ×10",
                "💡 Multiplier par 9: ×10 puis -1 fois le nombre"
            ],
            "subtraction": [
                "💡 Compte à rebours logiquement",
                "💡 Utilise la ligne numérique mentalement",
                "💡 Pense: 'Combien faut-il ajouter?'"
            ],
            "division": [
                "💡 Utilise tes tables de multiplication",
                "💡 Pense: 'Combien de fois X dans Y?'",
                "💡 Estime d'abord, puis ajuste"
            ]
        }
        return shortcuts.get(ex_type, ["💡 Cherche des patterns pour simplifier"])

    def _make_connections(self, ex_type: str) -> List[str]:
        """Make connections to other concepts"""
        connections = {
            "addition": [
                "🔗 Lien avec soustraction (opération inverse)",
                "🔗 Base de la multiplication (addition répétée)"
            ],
            "multiplication": [
                "🔗 Lien avec division (opération inverse)",
                "🔗 Lien avec addition (répétition)",
                "🔗 Lien avec aires/surfaces (géométrie)"
            ],
            "subtraction": [
                "🔗 Lien avec addition (inverse)",
                "🔗 Utile pour comparer des quantités"
            ],
            "division": [
                "🔗 Lien avec multiplication (inverse)",
                "🔗 Lien avec fractions (partage)"
            ]
        }
        return connections.get(ex_type, ["🔗 Pense aux liens logiques"])

    def suggest_resources(self, exercise_type: str) -> Dict[str, List[str]]:
        """
        Suggest logical learning resources

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        resources = {
            "reasoning_tools": [],
            "pattern_activities": [],
            "tips": []
        }

        # Reasoning tools
        resources["reasoning_tools"] = [
            "Étudie les tables pour trouver des patterns",
            "Fais des listes organisées",
            "Utilise des diagrammes logiques",
            "Crée des formules et règles"
        ]

        # Pattern activities
        resources["pattern_activities"] = [
            "Cherche des patterns dans les nombres",
            "Compare différentes méthodes",
            "Analyse les relations mathématiques",
            "Trouve des raccourcis logiques"
        ]

        # Logical learning tips
        resources["tips"] = [
            "🧠 Demande-toi toujours 'Pourquoi?'",
            "🔍 Cherche des patterns et structures",
            "📊 Organise l'information logiquement",
            "🔗 Fais des liens entre concepts",
            "⚡ Trouve des raccourcis intelligents"
        ]

        return resources

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt complete exercise for logical learner

        Args:
            exercise: Original exercise

        Returns:
            Fully adapted exercise
        """
        adapted = {
            "problem_statement": self.format_problem(exercise.get("operation", "")),
            "hint": self.format_hint(exercise.get("hint", "Cherche la logique")),
            "logical_structure": self.generate_logical_structure(exercise),
            "explanation_style": "logical",
            "resource_suggestions": self.suggest_resources(exercise.get("type", "general")),
            "presentation_tips": [
                "Explique toujours le 'pourquoi'",
                "Montre les patterns et structures",
                "Encourage le raisonnement systématique",
                "Fais des connexions entre concepts",
                "Propose des défis logiques"
            ]
        }

        return adapted

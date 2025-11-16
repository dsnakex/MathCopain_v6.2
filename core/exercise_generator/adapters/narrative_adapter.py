"""
NarrativeAdapter - Phase 6.3.2
Adapter for narrative learners (Gardner's Linguistic Intelligence)
Focuses on: stories, real-world contexts, scenarios, examples
"""

from typing import Dict, Any, List
import random


class NarrativeAdapter:
    """
    Adapter for narrative learning style
    Emphasizes storytelling, context, and real-world scenarios
    """

    # Story themes for different operations
    STORY_THEMES = {
        "addition": [
            "Au parc",
            "À la boulangerie",
            "Dans ton sac à dos",
            "Les amis qui arrivent",
            "La collection"
        ],
        "subtraction": [
            "Les bonbons mangés",
            "Les jouets prêtés",
            "Le voyage en bus",
            "La tirelire",
            "Les oiseaux qui s'envolent"
        ],
        "multiplication": [
            "Les paquets de cartes",
            "Les rangées de chaises",
            "Les groupes d'amis",
            "Les boîtes de chocolats",
            "Les équipes sportives"
        ],
        "division": [
            "Partage équitable",
            "Les équipes",
            "Distribution de cartes",
            "Les groupes de travail",
            "Le goûter à partager"
        ]
    }

    # Characters for stories
    CHARACTERS = [
        "Lucas", "Emma", "Noah", "Chloé", "Louis", "Léa",
        "Tom", "Lina", "Hugo", "Zoé", "Arthur", "Jade"
    ]

    def __init__(self):
        self.style = "narrative"

    def format_problem(self, problem: str) -> str:
        """
        Format problem as a story

        Args:
            problem: Original problem string

        Returns:
            Story-formatted problem
        """
        # Create mini-story around the problem
        story = self._create_story_context(problem)
        formatted = f"📖 **Histoire:** {story}\n\n**Question:** {problem}"

        return formatted

    def _create_story_context(self, problem: str) -> str:
        """Create story context for problem"""
        # Simple story template
        character = random.choice(self.CHARACTERS)

        if "+" in problem or "plus" in problem.lower():
            return f"{character} a des objets et en trouve d'autres"
        elif "-" in problem or "moins" in problem.lower():
            return f"{character} commence avec des objets mais en perd quelques-uns"
        elif "×" in problem or "fois" in problem.lower():
            return f"{character} a plusieurs groupes égaux d'objets"
        elif "÷" in problem or "divisé" in problem.lower():
            return f"{character} veut partager équitablement avec ses amis"
        else:
            return f"{character} a un problème à résoudre"

    def format_hint(self, hint: str) -> str:
        """
        Format hint as story element

        Args:
            hint: Original hint

        Returns:
            Story-formatted hint
        """
        return f"📚 **Dans l'histoire:** {hint}"

    def generate_story(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate full story for exercise

        Args:
            exercise: Exercise dictionary

        Returns:
            Dictionary with complete story
        """
        ex_type = exercise.get("type", "")
        operation = exercise.get("operation", "")
        difficulty = exercise.get("difficulty", 1)

        story = {
            "type": "narrative",
            "full_story": self._create_full_story(ex_type, operation, difficulty),
            "characters": self._get_story_characters(),
            "setting": self._get_story_setting(ex_type),
            "plot": self._create_plot(ex_type, operation),
            "real_world_connection": self._make_real_world_connection(ex_type)
        }

        return story

    def _create_full_story(self, ex_type: str, operation: str, difficulty: int) -> str:
        """Create complete story"""
        character = random.choice(self.CHARACTERS)
        theme_list = self.STORY_THEMES.get(ex_type, ["Une situation"])
        theme = random.choice(theme_list)

        # Parse operation to extract numbers
        numbers = self._extract_numbers(operation)

        if ex_type == "addition" and len(numbers) >= 2:
            return f"""
📖 C'était un beau jour. {character} était {theme.lower()}.
{character} avait {numbers[0]} objets.
Puis, {character} en a trouvé encore {numbers[1]}.
Maintenant, combien {character} a-t-il d'objets en tout?
            """.strip()

        elif ex_type == "subtraction" and len(numbers) >= 2:
            return f"""
📖 {character} était {theme.lower()}.
{character} avait {numbers[0]} bonbons.
{character} en a mangé {numbers[1]}.
Combien de bonbons reste-t-il à {character}?
            """.strip()

        elif ex_type == "multiplication" and len(numbers) >= 2:
            return f"""
📖 {character} prépare une fête.
{character} a {numbers[0]} tables.
Sur chaque table, il y a {numbers[1]} chaises.
Combien de chaises y a-t-il en tout?
            """.strip()

        elif ex_type == "division" and len(numbers) >= 2:
            return f"""
📖 {character} a {numbers[0]} billes.
{character} veut les partager équitablement entre {numbers[1]} amis.
Combien de billes chaque ami recevra-t-il?
            """.strip()

        else:
            return f"📖 {character} a un problème de mathématiques à résoudre: {operation}"

    def _extract_numbers(self, operation: str) -> List[int]:
        """Extract numbers from operation string"""
        import re
        numbers = re.findall(r'\d+', operation)
        return [int(n) for n in numbers]

    def _get_story_characters(self) -> List[str]:
        """Get characters for the story"""
        # Return 1-3 random characters
        num_chars = random.randint(1, 3)
        return random.sample(self.CHARACTERS, num_chars)

    def _get_story_setting(self, ex_type: str) -> str:
        """Get story setting based on exercise type"""
        settings = {
            "addition": "🏞️ Au parc d'attractions",
            "subtraction": "🏠 À la maison",
            "multiplication": "🎪 À la fête d'anniversaire",
            "division": "🍕 Au restaurant"
        }
        return settings.get(ex_type, "🌍 Quelque part dans le monde")

    def _create_plot(self, ex_type: str, operation: str) -> Dict[str, str]:
        """Create story plot structure"""
        return {
            "beginning": "Il était une fois...",
            "middle": "Et puis il s'est passé quelque chose...",
            "problem": f"Maintenant, il faut résoudre: {operation}",
            "end": "Et l'histoire finit bien quand tu trouves la réponse!"
        }

    def _make_real_world_connection(self, ex_type: str) -> List[str]:
        """Make connections to real-world scenarios"""
        connections = {
            "addition": [
                "💰 Compter ton argent de poche",
                "🍎 Additionner des fruits dans ton panier",
                "👕 Compter tes vêtements",
                "📚 Compter tes livres"
            ],
            "subtraction": [
                "🍪 Cookies mangés du paquet",
                "⏰ Temps qui reste avant la récré",
                "💸 Argent dépensé",
                "🎮 Vies perdues dans un jeu"
            ],
            "multiplication": [
                "🍕 Tranches de pizza par personne",
                "🚗 Roues sur plusieurs voitures",
                "📦 Objets dans plusieurs boîtes",
                "👥 Personnes dans plusieurs familles"
            ],
            "division": [
                "🍰 Partager un gâteau",
                "🃏 Distribuer des cartes",
                "⚽ Former des équipes",
                "🎁 Partager des cadeaux"
            ]
        }
        return connections.get(ex_type, ["🌍 Des situations de la vie quotidienne"])

    def suggest_resources(self, exercise_type: str) -> Dict[str, List[str]]:
        """
        Suggest narrative learning resources

        Args:
            exercise_type: Type of exercise

        Returns:
            Dictionary with resource suggestions
        """
        resources = {
            "story_books": [],
            "scenarios": [],
            "tips": []
        }

        # Story-based resources
        resources["story_books"] = [
            "Lis des livres avec des problèmes mathématiques",
            "Invente tes propres histoires avec des maths",
            "Écoute des contes qui incluent des nombres"
        ]

        # Real-world scenarios
        resources["scenarios"] = [
            "Trouve des exemples dans ta vie quotidienne",
            "Raconte des histoires à ta famille",
            "Crée des aventures avec des calculs",
            "Imagine des personnages qui résolvent des problèmes"
        ]

        # Narrative learning tips
        resources["tips"] = [
            "📖 Transforme chaque problème en histoire",
            "🎭 Imagine les personnages et la situation",
            "🌍 Pense à des exemples réels",
            "💬 Raconte le problème avec tes mots",
            "🎬 Visualise l'histoire comme un film"
        ]

        return resources

    def adapt_exercise(self, exercise: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt complete exercise for narrative learner

        Args:
            exercise: Original exercise

        Returns:
            Fully adapted exercise
        """
        adapted = {
            "problem_statement": self.format_problem(exercise.get("operation", "")),
            "hint": self.format_hint(exercise.get("hint", "Relis l'histoire attentivement")),
            "story": self.generate_story(exercise),
            "explanation_style": "narrative",
            "resource_suggestions": self.suggest_resources(exercise.get("type", "general")),
            "presentation_tips": [
                "Raconte toujours une histoire",
                "Utilise des contextes réels et familiers",
                "Crée des personnages attachants",
                "Fais des liens avec la vie quotidienne",
                "Encourage à raconter avec ses propres mots"
            ]
        }

        return adapted

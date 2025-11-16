"""
LearningStyleAnalyzer - Phase 6.3.1
Identification et adaptation selon le style d'apprentissage

Basé sur:
- Gardner (1983) - Théorie des Intelligences Multiples
- Fleming & Mills (1992) - VARK Model
- Kolb (1984) - Learning Styles Inventory

Fonctionnalités:
- Quiz assessment (5-7 questions)
- Performance-based inference
- Combined scoring (40% quiz + 60% performance)
- JSON persistence par utilisateur
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from collections import Counter
import random


@dataclass
class QuizResponse:
    """Réponse à une question du quiz"""
    question_id: int
    selected_style: str  # "visual", "auditory", "kinesthetic", "logical", "narrative"
    confidence: Optional[int] = None  # 1-5 si demandé
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LearningStyleResult:
    """Résultat d'une évaluation de style"""
    primary: Dict[str, Any]  # {"style": "visual", "confidence": 0.87}
    secondary: Optional[Dict[str, Any]] = None  # {"style": "kinesthetic", "confidence": 0.62}
    scores: Dict[str, float] = field(default_factory=dict)  # Scores pour chaque style
    source: str = "unknown"  # "quiz", "performance", "combined"
    data_points: int = 0  # Nombre de points de données utilisés
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LearningStyleProfile:
    """Profile complet du style d'apprentissage d'un utilisateur"""
    user_id: str
    primary: Dict[str, Any]
    secondary: Optional[Dict[str, Any]] = None
    assessment_date: str = field(default_factory=lambda: datetime.now().isoformat())
    data_points: int = 0
    confidence_overall: float = 0.0
    quiz_result: Optional[Dict[str, Any]] = None
    performance_result: Optional[Dict[str, Any]] = None
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LearningStyleAnalyzer:
    """
    Analyseur de style d'apprentissage
    Identifie le style dominant et adapte la présentation
    """

    # Les 5 styles d'apprentissage
    STYLES = ["visual", "auditory", "kinesthetic", "logical", "narrative"]

    # Descriptions des styles
    STYLE_DESCRIPTIONS = {
        "visual": {
            "name": "Visuel",
            "description": "Apprend mieux avec des graphiques, diagrammes, couleurs et images",
            "characteristics": ["Préfère voir", "Mémorise les images", "Aime les schémas"],
            "icon": "👁️"
        },
        "auditory": {
            "name": "Auditif",
            "description": "Apprend mieux en écoutant et en parlant",
            "characteristics": ["Préfère écouter", "Aime les explications verbales", "Répète à voix haute"],
            "icon": "👂"
        },
        "kinesthetic": {
            "name": "Kinesthésique",
            "description": "Apprend mieux en manipulant et en pratiquant",
            "characteristics": ["Préfère toucher", "Aime bouger", "Apprend en faisant"],
            "icon": "✋"
        },
        "logical": {
            "name": "Logique",
            "description": "Apprend mieux en comprenant le pourquoi et les liens logiques",
            "characteristics": ["Cherche la logique", "Aime les structures", "Veut comprendre"],
            "icon": "🧠"
        },
        "narrative": {
            "name": "Narratif",
            "description": "Apprend mieux avec des histoires et des contextes réels",
            "characteristics": ["Aime les histoires", "Préfère les exemples", "Contextes réels"],
            "icon": "📖"
        }
    }

    # Quiz questions (5-7 questions)
    QUIZ_QUESTIONS = [
        {
            "id": 1,
            "question": "Quand tu apprends quelque chose de nouveau, tu préfères:",
            "options": {
                "visual": "Voir un dessin ou un schéma",
                "auditory": "Qu'on te l'explique en parlant",
                "kinesthetic": "Essayer toi-même tout de suite",
                "logical": "Comprendre pourquoi ça marche",
                "narrative": "Entendre une histoire ou un exemple"
            }
        },
        {
            "id": 2,
            "question": "Tes meilleurs souvenirs à l'école, c'est:",
            "options": {
                "visual": "Les beaux tableaux et posters au mur",
                "auditory": "Les histoires racontées par le prof",
                "kinesthetic": "Les expériences et activités pratiques",
                "logical": "Les problèmes de maths à résoudre",
                "narrative": "Les lectures et les histoires"
            }
        },
        {
            "id": 3,
            "question": "Pour retenir les tables de multiplication, tu:",
            "options": {
                "visual": "Regardes un tableau coloré",
                "auditory": "Les répètes à voix haute",
                "kinesthetic": "Comptes sur tes doigts ou avec des objets",
                "logical": "Cherches les patterns (7×8 = 8×7)",
                "narrative": "Inventes une petite histoire"
            }
        },
        {
            "id": 4,
            "question": "Quand tu lis une histoire, tu:",
            "options": {
                "visual": "Imagines les images dans ta tête",
                "auditory": "Entends les voix des personnages",
                "kinesthetic": "Bouges ou mimes l'action",
                "logical": "Analyses ce qui va se passer",
                "narrative": "Te plonges dans l'histoire"
            }
        },
        {
            "id": 5,
            "question": "Pour apprendre un nouveau jeu, tu préfères:",
            "options": {
                "visual": "Regarder quelqu'un jouer d'abord",
                "auditory": "Qu'on t'explique les règles",
                "kinesthetic": "Essayer directement en jouant",
                "logical": "Lire les règles pour tout comprendre",
                "narrative": "Comprendre l'histoire du jeu"
            }
        },
        {
            "id": 6,
            "question": "Quand tu te souviens d'un mot, tu:",
            "options": {
                "visual": "Vois comment il s'écrit",
                "auditory": "Entends comment il se prononce",
                "kinesthetic": "Te rappelles où tu l'as écrit",
                "logical": "Penses à sa structure (préfixe, racine)",
                "narrative": "Te rappelles dans quelle phrase tu l'as vu"
            }
        },
        {
            "id": 7,
            "question": "Pour résoudre un problème de maths, tu préfères:",
            "options": {
                "visual": "Faire un dessin ou un schéma",
                "auditory": "Expliquer à voix haute",
                "kinesthetic": "Utiliser des objets pour compter",
                "logical": "Trouver la formule qui marche",
                "narrative": "Imaginer une situation réelle"
            }
        }
    ]

    def __init__(self, user_id: str, storage_path: str = "data/user_profiles"):
        self.user_id = user_id
        self.storage_path = Path(storage_path)
        self.user_dir = self.storage_path / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        self.profile: Optional[LearningStyleProfile] = None

        # Charger profile existant si disponible
        self.load()

    def get_quiz_questions(self, count: int = 7) -> List[Dict[str, Any]]:
        """
        Obtenir les questions du quiz

        Args:
            count: Nombre de questions (max 7)

        Returns:
            Liste de questions
        """
        return self.QUIZ_QUESTIONS[:min(count, len(self.QUIZ_QUESTIONS))]

    def assess_from_quiz(self, responses: List[Dict[str, Any]]) -> LearningStyleResult:
        """
        Évaluer le style à partir des réponses au quiz

        Args:
            responses: Liste de réponses au format:
                [{"question_id": 1, "selected_style": "visual"}, ...]

        Returns:
            LearningStyleResult avec primary et secondary styles
        """
        if not responses:
            raise ValueError("Responses list cannot be empty")

        # Compter les occurrences de chaque style
        style_counts = Counter()
        for response in responses:
            style = response.get("selected_style")
            if style in self.STYLES:
                style_counts[style] += 1

        # Calculer les scores normalisés
        total_responses = len(responses)
        scores = {
            style: count / total_responses
            for style, count in style_counts.items()
        }

        # Assurer que tous les styles ont un score
        for style in self.STYLES:
            if style not in scores:
                scores[style] = 0.0

        # Identifier primary et secondary
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        primary = {
            "style": sorted_styles[0][0],
            "confidence": sorted_styles[0][1]
        }

        secondary = None
        if len(sorted_styles) > 1 and sorted_styles[1][1] > 0:
            secondary = {
                "style": sorted_styles[1][0],
                "confidence": sorted_styles[1][1]
            }

        return LearningStyleResult(
            primary=primary,
            secondary=secondary,
            scores=scores,
            source="quiz",
            data_points=total_responses
        )

    def infer_from_performance(
        self,
        performance_history: List[Dict[str, Any]]
    ) -> LearningStyleResult:
        """
        Inférer le style à partir de l'historique de performance

        Args:
            performance_history: Liste d'exercices avec:
                [{
                    "exercise_type": "addition",
                    "presentation_style": "visual",
                    "success": True,
                    "time_seconds": 15,
                    "engagement_score": 0.8
                }, ...]

        Returns:
            LearningStyleResult inféré
        """
        if not performance_history:
            raise ValueError("Performance history cannot be empty")

        # Analyser performance par style de présentation
        style_performance = {style: {"successes": 0, "total": 0, "avg_time": [], "engagement": []}
                             for style in self.STYLES}

        for exercise in performance_history:
            style = exercise.get("presentation_style")
            if style not in self.STYLES:
                continue

            style_performance[style]["total"] += 1

            if exercise.get("success"):
                style_performance[style]["successes"] += 1

            if "time_seconds" in exercise:
                style_performance[style]["avg_time"].append(exercise["time_seconds"])

            if "engagement_score" in exercise:
                style_performance[style]["engagement"].append(exercise["engagement_score"])

        # Calculer scores composites
        scores = {}
        for style, perf in style_performance.items():
            if perf["total"] == 0:
                scores[style] = 0.0
                continue

            # Success rate (50% du score)
            success_rate = perf["successes"] / perf["total"]

            # Engagement moyen (30% du score)
            avg_engagement = sum(perf["engagement"]) / len(perf["engagement"]) if perf["engagement"] else 0.5

            # Rapidité relative (20% du score) - temps plus court = meilleur
            avg_time = sum(perf["avg_time"]) / len(perf["avg_time"]) if perf["avg_time"] else 30
            # Normaliser: 10s = 1.0, 60s = 0.0
            time_score = max(0, min(1, (60 - avg_time) / 50))

            # Score composite
            composite_score = (0.5 * success_rate) + (0.3 * avg_engagement) + (0.2 * time_score)
            scores[style] = composite_score

        # Identifier primary et secondary
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        primary = {
            "style": sorted_styles[0][0],
            "confidence": sorted_styles[0][1]
        }

        secondary = None
        if len(sorted_styles) > 1 and sorted_styles[1][1] > 0.1:  # Minimum 0.1 pour secondary
            secondary = {
                "style": sorted_styles[1][0],
                "confidence": sorted_styles[1][1]
            }

        return LearningStyleResult(
            primary=primary,
            secondary=secondary,
            scores=scores,
            source="performance",
            data_points=len(performance_history)
        )

    def combine_assessments(
        self,
        quiz_result: LearningStyleResult,
        performance_result: LearningStyleResult,
        quiz_weight: float = 0.4,
        performance_weight: float = 0.6
    ) -> LearningStyleResult:
        """
        Combiner quiz et performance pour score final

        Args:
            quiz_result: Résultat du quiz
            performance_result: Résultat de l'analyse de performance
            quiz_weight: Poids du quiz (default: 40%)
            performance_weight: Poids de la performance (default: 60%)

        Returns:
            LearningStyleResult combiné
        """
        if abs((quiz_weight + performance_weight) - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")

        # Combiner les scores
        combined_scores = {}
        for style in self.STYLES:
            quiz_score = quiz_result.scores.get(style, 0.0)
            perf_score = performance_result.scores.get(style, 0.0)
            combined_scores[style] = (quiz_weight * quiz_score) + (performance_weight * perf_score)

        # Identifier primary et secondary
        sorted_styles = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        primary = {
            "style": sorted_styles[0][0],
            "confidence": sorted_styles[0][1]
        }

        secondary = None
        if len(sorted_styles) > 1 and sorted_styles[1][1] > 0.1:
            secondary = {
                "style": sorted_styles[1][0],
                "confidence": sorted_styles[1][1]
            }

        return LearningStyleResult(
            primary=primary,
            secondary=secondary,
            scores=combined_scores,
            source="combined",
            data_points=quiz_result.data_points + performance_result.data_points
        )

    def save_profile(self, result: LearningStyleResult):
        """
        Sauvegarder le profil de style d'apprentissage

        Args:
            result: LearningStyleResult à sauvegarder
        """
        # Calculer confidence_overall
        confidence_overall = result.primary["confidence"]
        if result.secondary:
            # Moyenne pondérée
            confidence_overall = (result.primary["confidence"] + 0.5 * result.secondary["confidence"]) / 1.5

        # Créer ou mettre à jour le profil
        self.profile = LearningStyleProfile(
            user_id=self.user_id,
            primary=result.primary,
            secondary=result.secondary,
            data_points=result.data_points,
            confidence_overall=confidence_overall
        )

        # Sauvegarder selon la source
        if result.source == "quiz":
            self.profile.quiz_result = result.to_dict()
        elif result.source == "performance":
            self.profile.performance_result = result.to_dict()
        elif result.source == "combined":
            # Les résultats individuels devraient déjà être stockés
            pass

        # Écrire dans fichier
        profile_file = self.user_dir / "learning_style.json"
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile.to_dict(), f, indent=2, ensure_ascii=False)

    def load(self) -> Optional[LearningStyleProfile]:
        """
        Charger le profil existant

        Returns:
            LearningStyleProfile si existant, None sinon
        """
        profile_file = self.user_dir / "learning_style.json"

        if not profile_file.exists():
            return None

        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.profile = LearningStyleProfile(**data)
            return self.profile

        except Exception as e:
            print(f"Erreur chargement profil: {e}")
            return None

    def get_profile(self) -> Optional[LearningStyleProfile]:
        """
        Obtenir le profil actuel

        Returns:
            LearningStyleProfile ou None
        """
        return self.profile

    def get_recommendations(self, style: str) -> Dict[str, Any]:
        """
        Obtenir recommandations pour un style donné

        Args:
            style: Style d'apprentissage

        Returns:
            Dictionnaire de recommandations
        """
        recommendations = {
            "visual": {
                "exercise_types": ["diagrams", "color_coded", "charts", "visual_patterns"],
                "presentation_tips": [
                    "Utiliser des couleurs différentes",
                    "Montrer des schémas et diagrammes",
                    "Visualiser avec des graphiques"
                ],
                "teaching_approach": "Montrer des exemples visuels avant d'expliquer"
            },
            "auditory": {
                "exercise_types": ["verbal_explanations", "audio_instructions", "discussions"],
                "presentation_tips": [
                    "Donner des explications verbales claires",
                    "Encourager à lire à voix haute",
                    "Utiliser des rimes et mnémoniques"
                ],
                "teaching_approach": "Expliquer en détail avant de montrer"
            },
            "kinesthetic": {
                "exercise_types": ["interactive", "manipulatives", "hands_on", "drag_drop"],
                "presentation_tips": [
                    "Permettre de manipuler des objets",
                    "Utiliser des activités interactives",
                    "Encourager le mouvement"
                ],
                "teaching_approach": "Laisser expérimenter et découvrir"
            },
            "logical": {
                "exercise_types": ["pattern_recognition", "problem_solving", "formulas"],
                "presentation_tips": [
                    "Expliquer le pourquoi et le comment",
                    "Montrer les liens logiques",
                    "Utiliser des structures et patterns"
                ],
                "teaching_approach": "Expliquer la logique sous-jacente"
            },
            "narrative": {
                "exercise_types": ["story_problems", "real_world_contexts", "scenarios"],
                "presentation_tips": [
                    "Utiliser des histoires et exemples",
                    "Créer des contextes réalistes",
                    "Raconter l'application pratique"
                ],
                "teaching_approach": "Contextualiser avec des histoires"
            }
        }

        return recommendations.get(style, {})


def create_learning_style_analyzer(user_id: str) -> LearningStyleAnalyzer:
    """Factory function pour créer LearningStyleAnalyzer"""
    return LearningStyleAnalyzer(user_id)


# Export public API
__all__ = [
    'LearningStyleAnalyzer',
    'LearningStyleResult',
    'LearningStyleProfile',
    'QuizResponse',
    'create_learning_style_analyzer'
]

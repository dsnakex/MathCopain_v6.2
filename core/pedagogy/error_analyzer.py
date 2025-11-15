"""
ErrorAnalyzer - Analyse intelligente des erreurs mathématiques
Phase 6.1 - MathCopain v6.4

Basé sur la recherche de Hattie 2008 (effet-taille feedback: 0.79)
Transforme erreurs → insights pédagogiques actionnables
"""

import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class ErrorAnalysisResult:
    """Résultat d'analyse d'une erreur mathématique"""
    error_type: str  # "Conceptual" | "Procedural" | "Calculation"
    misconception: str
    severity: int  # 1-5
    confidence: float  # 0.0-1.0
    examples: List[str]
    prerequisites_gaps: List[str]
    remediation_strategy: str
    common_ages: List[str]
    error_id: Optional[str] = None
    root_cause: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour sérialisation"""
        return asdict(self)


class ErrorAnalyzer:
    """
    Analyse les erreurs mathématiques et catégorise par type

    Capacités:
    - Détection automatique du type d'erreur (Conceptual/Procedural/Calculation)
    - Identification des misconceptions sous-jacentes
    - Analyse des causes racines
    - Recommandations de remédiation personnalisées

    Basé sur catalogue de 500+ erreurs pré-cataloguées
    """

    def __init__(self, taxonomy_path: Optional[str] = None):
        """
        Initialise l'analyseur d'erreurs

        Args:
            taxonomy_path: Chemin vers error_taxonomy.json (optionnel)
        """
        if taxonomy_path is None:
            # Chemin par défaut relatif à ce fichier
            current_dir = Path(__file__).parent.parent.parent
            taxonomy_path = current_dir / "data" / "error_taxonomy.json"

        self.taxonomy_path = Path(taxonomy_path)
        self.error_catalog = self._load_catalog()
        self.detection_patterns = self.error_catalog.get("detection_patterns", {})
        self.remediation_strategies = self.error_catalog.get("remediation_strategies", {})

    def _load_catalog(self) -> Dict[str, Any]:
        """
        Charge le catalogue d'erreurs depuis error_taxonomy.json

        Returns:
            Dictionnaire contenant toute la taxonomie

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            json.JSONDecodeError: Si le JSON est invalide
        """
        if not self.taxonomy_path.exists():
            raise FileNotFoundError(
                f"Catalogue d'erreurs non trouvé: {self.taxonomy_path}"
            )

        with open(self.taxonomy_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)

        # Validation basique
        if "error_categories" not in catalog:
            raise ValueError("Format de catalogue invalide: 'error_categories' manquant")

        return catalog

    def analyze_error_type(
        self,
        exercise: Dict[str, Any],
        response: Any,
        expected: Any
    ) -> ErrorAnalysisResult:
        """
        Analyse une erreur et détermine son type

        Args:
            exercise: Dictionnaire décrivant l'exercice
                {
                    "type": "addition" | "subtraction" | "multiplication" | etc.,
                    "operation": "27 + 48",
                    "difficulty": "CE2",
                    "context": "addition avec retenue"
                }
            response: Réponse de l'élève
            expected: Réponse attendue

        Returns:
            ErrorAnalysisResult avec tous les détails de l'analyse
        """
        # Extraire type d'exercice
        exercise_type = exercise.get("type", "unknown")
        operation = exercise.get("operation", "")
        difficulty = exercise.get("difficulty", "CE2")

        # Convertir réponses en nombres si possible
        response_val = self._parse_number(response)
        expected_val = self._parse_number(expected)

        # Analyser l'écart
        difference = None
        if response_val is not None and expected_val is not None:
            difference = abs(response_val - expected_val)

        # Chercher patterns dans toutes les catégories
        candidates = []

        for category_name, category_data in self.error_catalog["error_categories"].items():
            if "errors" not in category_data:
                continue

            # Chercher dans le bon domaine mathématique
            domain = self._map_exercise_type_to_domain(exercise_type)
            if domain in category_data["errors"]:
                errors_list = category_data["errors"][domain]

                for error_def in errors_list:
                    # Calculer score de match
                    match_score = self._calculate_match_score(
                        error_def,
                        exercise,
                        response,
                        expected,
                        difference
                    )

                    if match_score > 0.3:  # Seuil minimum
                        candidates.append({
                            "category": category_name,
                            "error": error_def,
                            "score": match_score
                        })

        # Sélectionner meilleur candidat
        if candidates:
            best_match = max(candidates, key=lambda x: x["score"])
            return self._build_result_from_match(best_match, difficulty)

        # Fallback: erreur de calcul générique
        return self._create_generic_calculation_error(response, expected, difficulty)

    def identify_misconception(self, error_type: str, error_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Identifie la misconception associée à un type d'erreur

        Args:
            error_type: Type d'erreur ("Conceptual", "Procedural", "Calculation")
            error_id: ID spécifique d'erreur (optionnel, ex: "ADD_CONC_001")

        Returns:
            Dictionnaire avec détails de la misconception:
            {
                "misconception": "description",
                "common_reasons": [...],
                "examples": [...],
                "severity": 1-5
            }
        """
        if error_id:
            # Recherche par ID spécifique
            error_details = self._find_error_by_id(error_id)
            if error_details:
                return {
                    "misconception": error_details.get("misconception", ""),
                    "common_reasons": [error_details.get("pattern", "")],
                    "examples": error_details.get("examples", []),
                    "severity": error_details.get("severity", 3),
                    "prerequisites": error_details.get("prerequisites", [])
                }

        # Recherche par catégorie
        if error_type in self.error_catalog.get("error_categories", {}):
            category = self.error_catalog["error_categories"][error_type]
            return {
                "misconception": category.get("description", ""),
                "common_reasons": [],
                "examples": [],
                "severity": 3,
                "prerequisites": []
            }

        return {
            "misconception": "Erreur non identifiée",
            "common_reasons": [],
            "examples": [],
            "severity": 2,
            "prerequisites": []
        }

    def root_cause_analysis(self, error_details: ErrorAnalysisResult) -> Dict[str, Any]:
        """
        Analyse la cause racine d'une erreur

        Args:
            error_details: Résultat d'analyse d'erreur

        Returns:
            Dictionnaire avec analyse approfondie:
            {
                "root_cause": "description de la cause principale",
                "contributing_factors": [...],
                "prerequisite_gaps": [...],
                "recommended_actions": [...],
                "estimated_remediation_time": "2-4 sessions"
            }
        """
        error_type = error_details.error_type
        severity = error_details.severity
        prerequisites = error_details.prerequisites_gaps

        # Déterminer cause racine selon type
        if error_type == "Conceptual":
            root_cause = "L'enfant n'a pas construit une compréhension solide du concept mathématique sous-jacent"
            contributing_factors = [
                "Manque de manipulations concrètes",
                "Passage trop rapide à l'abstraction",
                "Prérequis non maîtrisés"
            ]
        elif error_type == "Procedural":
            root_cause = "L'enfant connaît le concept mais exécute incorrectement l'algorithme"
            contributing_factors = [
                "Manque de pratique guidée",
                "Oubli d'étapes intermédiaires",
                "Automatisation insuffisante"
            ]
        else:  # Calculation
            root_cause = "Erreur d'inattention ou lacune en calcul mental"
            contributing_factors = [
                "Fatigue ou manque de concentration",
                "Tables non automatisées",
                "Vérification insuffisante"
            ]

        # Estimer temps de remédiation
        remediation_time = self._estimate_remediation_time(severity, error_type)

        # Actions recommandées
        recommended_actions = self._get_recommended_actions(
            error_type,
            severity,
            error_details.remediation_strategy
        )

        return {
            "root_cause": root_cause,
            "contributing_factors": contributing_factors,
            "prerequisite_gaps": prerequisites,
            "recommended_actions": recommended_actions,
            "estimated_remediation_time": remediation_time,
            "severity_level": self._severity_label(severity),
            "urgency": "haute" if severity >= 4 else "moyenne" if severity >= 3 else "faible"
        }

    def _map_exercise_type_to_domain(self, exercise_type: str) -> str:
        """Mappe type d'exercice vers domaine dans taxonomie"""
        mapping = {
            "addition": "addition",
            "subtraction": "subtraction",
            "multiplication": "multiplication",
            "division": "division",
            "fractions": "fractions",
            "decimals": "decimals",
            "geometry": "geometry",
            "measurement": "measurement",
            "mesures": "measurement",
            "geometrie": "geometry"
        }
        return mapping.get(exercise_type.lower(), "arithmetic")

    def _parse_number(self, value: Any) -> Optional[float]:
        """Parse une valeur en nombre"""
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
            except (ValueError, ZeroDivisionError):
                return None
        return None

    def _calculate_match_score(
        self,
        error_def: Dict[str, Any],
        exercise: Dict[str, Any],
        response: Any,
        expected: Any,
        difference: Optional[float]
    ) -> float:
        """
        Calcule score de correspondance entre erreur observée et définition

        Returns:
            Score entre 0.0 et 1.0
        """
        score = 0.0

        # Vérifier âge approprié
        difficulty = exercise.get("difficulty", "CE2")
        if difficulty in error_def.get("common_ages", []):
            score += 0.3

        # Vérifier pattern dans operation
        pattern = error_def.get("pattern", "")
        operation = exercise.get("operation", "")
        context = exercise.get("context", "")

        if pattern.lower() in operation.lower() or pattern.lower() in context.lower():
            score += 0.4

        # Score basé sur différence si erreur de calcul
        if difference is not None and difference > 0:
            # Petite différence = probablement erreur calcul
            # Grande différence = probablement erreur conceptuelle
            if error_def.get("id", "").startswith("CALC") and difference <= 5:
                score += 0.3
            elif not error_def.get("id", "").startswith("CALC") and difference > 5:
                score += 0.2

        # Utiliser confidence de détection
        detection_conf = error_def.get("detection_confidence", 0.5)
        score = score * detection_conf

        return min(score, 1.0)

    def _build_result_from_match(self, match: Dict[str, Any], difficulty: str) -> ErrorAnalysisResult:
        """Construit ErrorAnalysisResult depuis un match"""
        error_def = match["error"]
        category = match["category"]

        return ErrorAnalysisResult(
            error_type=category,
            misconception=error_def.get("misconception", ""),
            severity=error_def.get("severity", 3),
            confidence=match["score"],
            examples=error_def.get("examples", []),
            prerequisites_gaps=error_def.get("prerequisites", []),
            remediation_strategy=error_def.get("remediation_strategy", "pratique_guidee"),
            common_ages=error_def.get("common_ages", [difficulty]),
            error_id=error_def.get("id"),
            root_cause=None  # Sera rempli par root_cause_analysis
        )

    def _create_generic_calculation_error(
        self,
        response: Any,
        expected: Any,
        difficulty: str
    ) -> ErrorAnalysisResult:
        """Crée un résultat générique pour erreur de calcul"""
        return ErrorAnalysisResult(
            error_type="Calculation",
            misconception="Erreur de calcul ou d'inattention",
            severity=2,
            confidence=0.60,
            examples=[f"Répondu {response} au lieu de {expected}"],
            prerequisites_gaps=["calcul_mental", "attention"],
            remediation_strategy="pratique_reguliere",
            common_ages=[difficulty],
            error_id="CALC_001",
            root_cause="Erreur de calcul mental ou manque d'attention"
        )

    def _find_error_by_id(self, error_id: str) -> Optional[Dict[str, Any]]:
        """Recherche une erreur par son ID"""
        for category_name, category_data in self.error_catalog.get("error_categories", {}).items():
            if "errors" not in category_data:
                continue

            for domain, errors_list in category_data["errors"].items():
                for error_def in errors_list:
                    if error_def.get("id") == error_id:
                        return error_def

        return None

    def _estimate_remediation_time(self, severity: int, error_type: str) -> str:
        """Estime le temps de remédiation nécessaire"""
        base_sessions = {
            "Conceptual": 4,
            "Procedural": 3,
            "Calculation": 2
        }

        sessions = base_sessions.get(error_type, 3) + (severity - 3)
        sessions = max(1, sessions)

        if sessions <= 2:
            return "1-2 sessions"
        elif sessions <= 4:
            return "3-4 sessions"
        elif sessions <= 6:
            return "5-6 sessions"
        else:
            return "7+ sessions"

    def _get_recommended_actions(
        self,
        error_type: str,
        severity: int,
        strategy_key: str
    ) -> List[str]:
        """Génère liste d'actions recommandées"""
        actions = []

        # Actions basées sur stratégie
        strategy = self.remediation_strategies.get(strategy_key, {})
        if strategy:
            actions.append(f"Utiliser: {strategy.get('description', strategy_key)}")

        # Actions basées sur type
        if error_type == "Conceptual":
            actions.extend([
                "Revenir aux manipulations concrètes",
                "Utiliser représentations visuelles variées",
                "Faire verbaliser le raisonnement"
            ])
        elif error_type == "Procedural":
            actions.extend([
                "Décomposer l'algorithme en étapes explicites",
                "Pratiquer avec guidance progressive",
                "Automatiser par répétition espacée"
            ])
        else:  # Calculation
            actions.extend([
                "Réviser les tables et calcul mental",
                "Encourager la vérification systématique",
                "Pauses régulières pour maintenir concentration"
            ])

        # Actions basées sur sévérité
        if severity >= 4:
            actions.insert(0, "⚠️ PRIORITÉ HAUTE - Traiter rapidement")

        return actions[:5]  # Limiter à 5 actions principales

    def _severity_label(self, severity: int) -> str:
        """Convertit niveau de sévérité en label"""
        labels = {
            1: "Très faible",
            2: "Faible",
            3: "Modérée",
            4: "Élevée",
            5: "Très élevée"
        }
        return labels.get(severity, "Modérée")

    def get_statistics(self) -> Dict[str, Any]:
        """Retourne statistiques sur le catalogue d'erreurs"""
        total_errors = 0
        by_category = {}
        by_domain = {}

        for category_name, category_data in self.error_catalog.get("error_categories", {}).items():
            category_count = 0
            if "errors" in category_data:
                for domain, errors_list in category_data["errors"].items():
                    count = len(errors_list)
                    category_count += count
                    by_domain[domain] = by_domain.get(domain, 0) + count

            by_category[category_name] = category_count
            total_errors += category_count

        return {
            "total_errors": total_errors,
            "by_category": by_category,
            "by_domain": by_domain,
            "version": self.error_catalog.get("version", "unknown")
        }

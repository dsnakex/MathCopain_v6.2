"""Tests pour le système adaptatif de MathCopain."""
import pytest
from datetime import datetime, timedelta
from core.adaptive_system import AdaptiveSystem


@pytest.fixture
def adaptive_system():
    """Fixture pour créer une instance du système adaptatif."""
    return AdaptiveSystem()


@pytest.fixture
def sample_exercise_history():
    """Historique d'exercices pour tests."""
    now = datetime.now()
    return [
        {'type': 'addition', 'correct': True, 'difficulty': 3, 'timestamp': now.isoformat()},
        {'type': 'addition', 'correct': True, 'difficulty': 3, 'timestamp': now.isoformat()},
        {'type': 'addition', 'correct': False, 'difficulty': 4, 'timestamp': now.isoformat()},
        {'type': 'soustraction', 'correct': True, 'difficulty': 2, 'timestamp': now.isoformat()},
        {'type': 'multiplication', 'correct': False, 'difficulty': 5, 'timestamp': now.isoformat()},
    ]


class TestAnalyzePerformance:
    """Tests de l'analyse de performance."""

    def test_performance_avec_donnees_suffisantes(self, adaptive_system, sample_exercise_history):
        """Analyser performance avec historique suffisant."""
        result = adaptive_system.analyze_performance(sample_exercise_history)

        assert 'success_rate' in result
        assert 'avg_difficulty' in result
        assert 'total_exercises' in result
        assert 'trend' in result
        assert 0 <= result['success_rate'] <= 1

    def test_performance_sans_donnees(self, adaptive_system):
        """Performance avec historique vide retourne valeurs par défaut."""
        result = adaptive_system.analyze_performance([])

        assert result['success_rate'] == 0.5
        assert result['avg_difficulty'] == 3
        assert result['total_exercises'] == 0
        assert result['trend'] == 'unknown'

    def test_filtrage_par_type(self, adaptive_system, sample_exercise_history):
        """Filtrer exercices par type."""
        result = adaptive_system.analyze_performance(sample_exercise_history, exercise_type='addition')

        assert result['total_exercises'] == 3  # 3 additions dans l'historique


class TestCalculateNextDifficulty:
    """Tests du calcul de la prochaine difficulté."""

    def test_augmentation_difficulte_haute_performance(self, adaptive_system):
        """Taux réussite > 75% → augmenter difficulté."""
        performance = {
            'success_rate': 0.8,
            'avg_difficulty': 3,
            'total_exercises': 10,
            'trend': 'stable'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=3)
        assert nouveau_niveau == 4

    def test_diminution_difficulte_basse_performance(self, adaptive_system):
        """Taux réussite < 50% → diminuer difficulté."""
        performance = {
            'success_rate': 0.4,
            'avg_difficulty': 5,
            'total_exercises': 10,
            'trend': 'stable'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=5)
        assert nouveau_niveau == 4

    def test_maintien_difficulte_zone_optimale(self, adaptive_system):
        """Taux réussite 50-75% avec trend stable → maintenir."""
        performance = {
            'success_rate': 0.65,
            'avg_difficulty': 4,
            'total_exercises': 10,
            'trend': 'stable'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=4)
        assert nouveau_niveau == 4

    def test_limite_min_difficulte(self, adaptive_system):
        """Difficulté ne descend pas en dessous de 1."""
        performance = {
            'success_rate': 0.3,
            'avg_difficulty': 1,
            'total_exercises': 10,
            'trend': 'declining'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=1)
        assert nouveau_niveau == 1

    def test_limite_max_difficulte(self, adaptive_system):
        """Difficulté ne monte pas au-dessus de 10."""
        performance = {
            'success_rate': 0.9,
            'avg_difficulty': 10,
            'total_exercises': 10,
            'trend': 'improving'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=10)
        assert nouveau_niveau == 10

    def test_donnees_insuffisantes(self, adaptive_system):
        """Pas assez de données → maintenir difficulté actuelle."""
        performance = {
            'success_rate': 0.5,
            'avg_difficulty': 3,
            'total_exercises': 2,
            'trend': 'insufficient_data'
        }
        nouveau_niveau = adaptive_system.calculate_next_difficulty(performance, current_difficulty=3)
        assert nouveau_niveau == 3


class TestGetSkillLevels:
    """Tests du calcul des niveaux de compétence."""

    def test_calcul_niveaux_competence(self, adaptive_system, sample_exercise_history):
        """Calculer niveaux de compétence par type."""
        skill_levels = adaptive_system.get_skill_levels(sample_exercise_history)

        assert isinstance(skill_levels, dict)
        assert 'addition' in skill_levels
        assert 'soustraction' in skill_levels
        assert all(0 <= level <= 1 for level in skill_levels.values())

    def test_competence_zero_si_jamais_pratique(self, adaptive_system):
        """Types jamais pratiqués ont niveau 0."""
        history = [
            {'type': 'addition', 'correct': True, 'difficulty': 3, 'timestamp': datetime.now().isoformat()}
        ]
        skill_levels = adaptive_system.get_skill_levels(history)

        # Soustraction jamais pratiquée
        assert skill_levels.get('soustraction', 0) == 0


class TestRecommendExerciseType:
    """Tests des recommandations d'exercices."""

    def test_recommandation_domaine_faible(self, adaptive_system):
        """Recommander domaine faible (skill < 0.5)."""
        skill_levels = {
            'addition': 0.3,
            'soustraction': 0.8,
            'multiplication': 0.7
        }
        ex_type, reason = adaptive_system.recommend_exercise_type(skill_levels)

        assert isinstance(ex_type, str)
        assert isinstance(reason, str)
        assert len(reason) > 0

    def test_recommandation_avec_tous_forts(self, adaptive_system):
        """Gérer cas où tous domaines sont forts."""
        skill_levels = {
            'addition': 0.8,
            'soustraction': 0.75,
            'multiplication': 0.9
        }
        ex_type, reason = adaptive_system.recommend_exercise_type(skill_levels)

        assert ex_type in skill_levels.keys()
        assert isinstance(reason, str)
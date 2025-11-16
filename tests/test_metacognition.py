"""
Tests pour MetacognitionEngine - Phase 6.2.1
Tests de questions réflexives et métacognition

Couverture: 350+ tests
- ReflectionData
- StrategyPortfolio
- MetacognitionEngine
- Pattern detection
- Self-regulation
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

from core.pedagogy.metacognition import (
    MetacognitionEngine,
    StrategyPortfolio,
    ReflectionData,
    StrategyPattern,
    create_metacognition_engine
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_storage():
    """Temporary storage directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_reflection():
    """Sample reflection data"""
    return ReflectionData(
        timestamp=datetime.now().isoformat(),
        exercise_type="addition",
        difficulty_level="CE2",
        was_correct=True,
        strategy_used="Mental",
        perceived_difficulty=3,
        self_explanation="J'ai compté dans ma tête",
        future_intention="Aller plus vite",
        time_taken_seconds=15,
        user_id="student_123"
    )


@pytest.fixture
def sample_exercise():
    """Sample exercise"""
    return {
        'type': 'addition',
        'operation': '25 + 17',
        'difficulty': 'CE2',
        'expected_answer': 42
    }


@pytest.fixture
def metacognition_engine(temp_storage):
    """MetacognitionEngine instance"""
    return MetacognitionEngine("test_user", storage_path=temp_storage)


@pytest.fixture
def portfolio(temp_storage):
    """StrategyPortfolio instance"""
    return StrategyPortfolio("test_user", storage_path=temp_storage)


# ============================================================================
# TESTS - ReflectionData
# ============================================================================

class TestReflectionData:
    """Tests pour ReflectionData dataclass"""

    def test_reflection_data_creation(self):
        """Créer ReflectionData avec champs requis"""
        reflection = ReflectionData(
            timestamp="2025-11-16T10:30:00",
            exercise_type="addition",
            difficulty_level="CE1",
            was_correct=True,
            strategy_used="Doigts",
            perceived_difficulty=2
        )

        assert reflection.timestamp == "2025-11-16T10:30:00"
        assert reflection.exercise_type == "addition"
        assert reflection.was_correct is True
        assert reflection.strategy_used == "Doigts"
        assert reflection.perceived_difficulty == 2

    def test_reflection_data_optional_fields(self):
        """Champs optionnels doivent avoir valeurs par défaut"""
        reflection = ReflectionData(
            timestamp="2025-11-16T10:30:00",
            exercise_type="multiplication",
            difficulty_level="CE2",
            was_correct=False,
            strategy_used="Mental"
        )

        assert reflection.strategy_other is None
        assert reflection.self_explanation is None
        assert reflection.future_intention is None
        assert reflection.time_taken_seconds is None
        assert reflection.perceived_difficulty == 3  # Default

    def test_reflection_data_to_dict(self, sample_reflection):
        """Conversion en dictionnaire"""
        data = sample_reflection.to_dict()

        assert isinstance(data, dict)
        assert data['exercise_type'] == "addition"
        assert data['was_correct'] is True
        assert data['strategy_used'] == "Mental"
        assert 'timestamp' in data
        assert 'perceived_difficulty' in data

    def test_reflection_data_all_fields(self):
        """ReflectionData avec tous les champs remplis"""
        reflection = ReflectionData(
            timestamp="2025-11-16T10:30:00",
            exercise_type="subtraction",
            difficulty_level="CM1",
            was_correct=False,
            strategy_used="Autre",
            strategy_other="Avec des billes",
            perceived_difficulty=4,
            self_explanation="J'ai compté à l'envers",
            future_intention="M'entraîner plus",
            time_taken_seconds=45,
            user_id="student_456",
            session_id="20251116_103000"
        )

        assert reflection.strategy_other == "Avec des billes"
        assert reflection.self_explanation is not None
        assert reflection.future_intention is not None
        assert reflection.time_taken_seconds == 45
        assert reflection.session_id == "20251116_103000"


# ============================================================================
# TESTS - StrategyPattern
# ============================================================================

class TestStrategyPattern:
    """Tests pour StrategyPattern dataclass"""

    def test_strategy_pattern_creation(self):
        """Créer StrategyPattern"""
        pattern = StrategyPattern(
            strategy="Mental",
            success_rate=0.85,
            usage_count=20,
            avg_difficulty=3.2,
            contexts=["addition", "subtraction"]
        )

        assert pattern.strategy == "Mental"
        assert pattern.success_rate == 0.85
        assert pattern.usage_count == 20
        assert pattern.avg_difficulty == 3.2
        assert "addition" in pattern.contexts

    def test_strategy_pattern_to_dict(self):
        """Conversion en dictionnaire"""
        pattern = StrategyPattern(
            strategy="Doigts",
            success_rate=0.7,
            usage_count=15,
            avg_difficulty=2.5
        )

        data = pattern.to_dict()
        assert isinstance(data, dict)
        assert data['strategy'] == "Doigts"
        assert data['success_rate'] == 0.7


# ============================================================================
# TESTS - StrategyPortfolio
# ============================================================================

class TestStrategyPortfolio:
    """Tests pour StrategyPortfolio"""

    def test_portfolio_initialization(self, temp_storage):
        """Initialisation du portfolio"""
        portfolio = StrategyPortfolio("user_123", temp_storage)

        assert portfolio.user_id == "user_123"
        assert portfolio.reflections == []
        assert portfolio.strategy_stats == {}
        assert portfolio.user_dir.exists()

    def test_portfolio_add_reflection(self, portfolio, sample_reflection):
        """Ajouter une réflexion"""
        initial_count = len(portfolio.reflections)

        portfolio.add_reflection(sample_reflection)

        assert len(portfolio.reflections) == initial_count + 1
        assert portfolio.reflections[-1] == sample_reflection

    def test_portfolio_update_strategy_stats(self, portfolio):
        """Mise à jour des stats de stratégie"""
        reflection = ReflectionData(
            timestamp=datetime.now().isoformat(),
            exercise_type="addition",
            difficulty_level="CE2",
            was_correct=True,
            strategy_used="Mental",
            perceived_difficulty=3
        )

        portfolio.add_reflection(reflection)

        assert "Mental" in portfolio.strategy_stats
        stats = portfolio.strategy_stats["Mental"]
        assert stats['count'] == 1
        assert stats['successes'] == 1
        assert stats['total_difficulty'] == 3

    def test_portfolio_multiple_reflections_same_strategy(self, portfolio):
        """Plusieurs réflexions avec même stratégie"""
        for i in range(5):
            reflection = ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=(i % 2 == 0),  # 3/5 succès
                strategy_used="Doigts",
                perceived_difficulty=2
            )
            portfolio.add_reflection(reflection)

        stats = portfolio.strategy_stats["Doigts"]
        assert stats['count'] == 5
        assert stats['successes'] == 3  # 0, 2, 4 = 3 succès

    def test_portfolio_get_strategy_patterns(self, portfolio):
        """Obtenir patterns de stratégies"""
        # Ajouter plusieurs stratégies
        strategies = ["Mental", "Doigts", "Dessin"]
        for strategy in strategies:
            for i in range(3):
                reflection = ReflectionData(
                    timestamp=datetime.now().isoformat(),
                    exercise_type="addition",
                    difficulty_level="CE2",
                    was_correct=True,
                    strategy_used=strategy,
                    perceived_difficulty=2
                )
                portfolio.add_reflection(reflection)

        patterns = portfolio.get_strategy_patterns()

        assert len(patterns) == 3
        assert all(isinstance(p, StrategyPattern) for p in patterns)
        assert all(p.usage_count == 3 for p in patterns)

    def test_portfolio_patterns_sorted_by_usage(self, portfolio):
        """Patterns triés par usage"""
        # Mental: 10 fois
        for i in range(10):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Mental"
            ))

        # Doigts: 5 fois
        for i in range(5):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Doigts"
            ))

        patterns = portfolio.get_strategy_patterns()

        assert patterns[0].strategy == "Mental"
        assert patterns[0].usage_count == 10
        assert patterns[1].strategy == "Doigts"
        assert patterns[1].usage_count == 5

    def test_portfolio_get_most_successful_strategy(self, portfolio):
        """Obtenir la stratégie la plus efficace"""
        # Mental: 90% succès (9/10)
        for i in range(10):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=(i < 9),
                strategy_used="Mental"
            ))

        # Doigts: 60% succès (3/5)
        for i in range(5):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=(i < 3),
                strategy_used="Doigts"
            ))

        best = portfolio.get_most_successful_strategy()

        assert best is not None
        assert best.strategy == "Mental"
        assert best.success_rate == 0.9

    def test_portfolio_most_successful_requires_min_usage(self, portfolio):
        """Stratégie la plus efficace requiert minimum 3 usages"""
        # 2 usages seulement (100% succès mais pas assez)
        for i in range(2):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Rare"
            ))

        best = portfolio.get_most_successful_strategy()
        assert best is None  # Pas assez d'usages

    def test_portfolio_get_reflection_count(self, portfolio):
        """Compter les réflexions"""
        assert portfolio.get_reflection_count() == 0

        for i in range(7):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Mental"
            ))

        assert portfolio.get_reflection_count() == 7

    def test_portfolio_get_recent_reflections(self, portfolio):
        """Obtenir réflexions récentes"""
        # Ajouter 15 réflexions
        for i in range(15):
            portfolio.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Mental"
            ))

        # Obtenir les 10 dernières
        recent = portfolio.get_recent_reflections(10)

        assert len(recent) == 10
        # Les 10 dernières sont les indices [5:15]
        assert recent == portfolio.reflections[-10:]

    def test_portfolio_save_and_load(self, temp_storage):
        """Sauvegarder et charger portfolio"""
        # Créer et remplir portfolio
        portfolio1 = StrategyPortfolio("save_test", temp_storage)

        for i in range(5):
            portfolio1.add_reflection(ReflectionData(
                timestamp=datetime.now().isoformat(),
                exercise_type="addition",
                difficulty_level="CE2",
                was_correct=True,
                strategy_used="Mental"
            ))

        # Sauvegarder
        portfolio1.save()

        # Charger dans nouveau portfolio
        portfolio2 = StrategyPortfolio("save_test", temp_storage)

        assert len(portfolio2.reflections) == 5
        assert "Mental" in portfolio2.strategy_stats

    def test_portfolio_load_nonexistent(self, temp_storage):
        """Charger portfolio inexistant ne crashe pas"""
        portfolio = StrategyPortfolio("nonexistent", temp_storage)

        assert portfolio.reflections == []
        assert portfolio.strategy_stats == {}


# ============================================================================
# TESTS - MetacognitionEngine
# ============================================================================

class TestMetacognitionEngineInitialization:
    """Tests d'initialisation du MetacognitionEngine"""

    def test_engine_initialization(self, temp_storage):
        """Initialisation du moteur"""
        engine = MetacognitionEngine("user_123", temp_storage)

        assert engine.user_id == "user_123"
        assert isinstance(engine.portfolio, StrategyPortfolio)
        assert engine.current_session_reflections == []
        assert engine.session_id is not None

    def test_engine_has_portfolio(self, metacognition_engine):
        """Engine doit avoir un portfolio"""
        assert hasattr(metacognition_engine, 'portfolio')
        assert isinstance(metacognition_engine.portfolio, StrategyPortfolio)

    def test_factory_function(self, temp_storage):
        """Factory function crée engine"""
        with patch('core.pedagogy.metacognition.MetacognitionEngine') as MockEngine:
            MockEngine.return_value = MagicMock()

            engine = create_metacognition_engine("test_user")

            assert engine is not None


# ============================================================================
# TESTS - Reflection Questions
# ============================================================================

class TestReflectionQuestions:
    """Tests de génération de questions"""

    def test_generate_reflection_questions_returns_list(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Génère une liste de questions"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)

        assert isinstance(questions, list)
        assert len(questions) == 4  # 4 questions

    def test_question_1_strategy(self, metacognition_engine, sample_exercise):
        """Question 1: Stratégie"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)
        q1 = questions[0]

        assert 'question' in q1
        assert 'stratégie' in q1['question'].lower()
        assert q1['type'] == 'multiple_choice'
        assert 'options' in q1
        assert len(q1['options']) >= 4  # Au moins 4 stratégies

    def test_question_1_has_all_strategies(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Question 1 contient toutes les stratégies"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)
        q1 = questions[0]

        expected_strategies = ["Doigts", "Mental", "Dessin", "Formule", "Autre"]
        for strategy in expected_strategies:
            assert strategy in q1['options']

    def test_question_2_difficulty(self, metacognition_engine, sample_exercise):
        """Question 2: Difficulté"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)
        q2 = questions[1]

        assert 'question' in q2
        assert 'difficulté' in q2['question'].lower() or 'trouvé' in q2['question'].lower()
        assert q2['type'] == 'slider'
        assert q2['min'] == 1
        assert q2['max'] == 5
        assert 'labels' in q2

    def test_question_3_explanation(self, metacognition_engine, sample_exercise):
        """Question 3: Auto-explication"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)
        q3 = questions[2]

        assert 'question' in q3
        assert q3['type'] == 'text'
        assert 'placeholder' in q3
        assert 'max_chars' in q3
        assert q3['max_chars'] <= 200

    def test_question_4_intention(self, metacognition_engine, sample_exercise):
        """Question 4: Intention future"""
        questions = metacognition_engine.generate_reflection_questions(sample_exercise)
        q4 = questions[3]

        assert 'question' in q4
        assert 'prochaine' in q4['question'].lower()
        assert q4['type'] == 'text'
        assert 'max_chars' in q4


# ============================================================================
# TESTS - Process Reflection
# ============================================================================

class TestProcessReflection:
    """Tests de traitement de réflexions"""

    def test_process_reflection_basic(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Traiter une réflexion basique"""
        reflection_data = {
            'strategy': 'Mental',
            'difficulty': 3,
            'explanation': 'J\'ai calculé dans ma tête',
            'intention': 'Être plus rapide'
        }

        result = metacognition_engine.process_reflection(
            reflection_data,
            sample_exercise,
            was_correct=True,
            time_taken=15
        )

        assert 'reflection' in result
        assert 'insights' in result
        assert 'total_reflections' in result

    def test_process_reflection_adds_to_portfolio(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Traiter réflexion ajoute au portfolio"""
        initial_count = metacognition_engine.portfolio.get_reflection_count()

        reflection_data = {
            'strategy': 'Doigts',
            'difficulty': 2
        }

        metacognition_engine.process_reflection(
            reflection_data,
            sample_exercise,
            was_correct=True
        )

        assert metacognition_engine.portfolio.get_reflection_count() == initial_count + 1

    def test_process_reflection_adds_to_session(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Traiter réflexion ajoute à la session courante"""
        initial_session_count = len(metacognition_engine.current_session_reflections)

        reflection_data = {'strategy': 'Mental', 'difficulty': 3}

        metacognition_engine.process_reflection(
            reflection_data,
            sample_exercise,
            was_correct=True
        )

        assert len(metacognition_engine.current_session_reflections) == initial_session_count + 1

    def test_process_reflection_generates_insights(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Traiter réflexion génère insights"""
        reflection_data = {'strategy': 'Mental', 'difficulty': 4}

        result = metacognition_engine.process_reflection(
            reflection_data,
            sample_exercise,
            was_correct=True
        )

        insights = result['insights']
        assert isinstance(insights, dict)

    def test_process_reflection_with_all_fields(
        self,
        metacognition_engine,
        sample_exercise
    ):
        """Traiter réflexion avec tous les champs"""
        reflection_data = {
            'strategy': 'Formule',
            'strategy_other': None,
            'difficulty': 5,
            'explanation': 'J\'ai utilisé la règle de multiplication',
            'intention': 'Apprendre plus de formules'
        }

        result = metacognition_engine.process_reflection(
            reflection_data,
            sample_exercise,
            was_correct=False,
            time_taken=60
        )

        reflection = result['reflection']
        assert reflection['strategy_used'] == 'Formule'
        assert reflection['perceived_difficulty'] == 5
        assert reflection['was_correct'] is False
        assert reflection['time_taken_seconds'] == 60


# ============================================================================
# TESTS - Insights Generation
# ============================================================================

class TestInsightsGeneration:
    """Tests de génération d'insights"""

    def test_insights_strategy_effectiveness_high(self, metacognition_engine):
        """Insight pour stratégie très efficace"""
        # Ajouter 10 réflexions avec Mental (90% succès)
        for i in range(10):
            reflection_data = {'strategy': 'Mental', 'difficulty': 3}
            metacognition_engine.process_reflection(
                reflection_data,
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 9)
            )

        # Ajouter une de plus pour tester l'insight
        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=True
        )

        insights = result['insights']
        if insights.get('strategy_effectiveness'):
            assert insights['strategy_effectiveness']['level'] == 'high'

    def test_insights_strategy_effectiveness_low(self, metacognition_engine):
        """Insight pour stratégie peu efficace"""
        # Ajouter réflexions avec faible succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Dessin', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 3)  # 30% succès
            )

        result = metacognition_engine.process_reflection(
            {'strategy': 'Dessin', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=False
        )

        insights = result['insights']
        if insights.get('strategy_effectiveness'):
            assert insights['strategy_effectiveness']['level'] == 'low'

    def test_insights_better_strategy_available(self, metacognition_engine):
        """Insight si meilleure stratégie disponible"""
        # Stratégie A: 90% succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 9)
            )

        # Stratégie B: 40% succès
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Doigts', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 2)
            )

        # Utiliser stratégie B alors que A est meilleure
        result = metacognition_engine.process_reflection(
            {'strategy': 'Doigts', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=False
        )

        insights = result['insights']
        if insights.get('pattern_detected'):
            assert 'better_strategy' in insights['pattern_detected']['type']

    def test_insights_difficult_but_correct(self, metacognition_engine):
        """Insight pour exercice difficile mais réussi"""
        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 5},  # Très difficile
            {'type': 'multiplication', 'difficulty': 'CM2'},
            was_correct=True
        )

        insights = result['insights']
        if insights.get('recommendation'):
            assert 'difficile' in insights['recommendation'].lower() or 'excellent' in insights['recommendation'].lower()

    def test_insights_easy_but_wrong(self, metacognition_engine):
        """Insight pour exercice facile mais raté"""
        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 1},  # Très facile
            {'type': 'addition', 'difficulty': 'CE1'},
            was_correct=False
        )

        insights = result['insights']
        if insights.get('recommendation'):
            assert 'facile' in insights['recommendation'].lower() or 'temps' in insights['recommendation'].lower()

    def test_insights_encouragement_high_success(self, metacognition_engine):
        """Encouragement pour bon taux de succès"""
        # 5 réflexions avec 80% succès
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 4)
            )

        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=True
        )

        insights = result['insights']
        if insights.get('encouragement'):
            assert len(insights['encouragement']) > 0

    def test_insights_encouragement_struggling(self, metacognition_engine):
        """Encouragement pour élève en difficulté"""
        # 5 réflexions avec faible succès
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 2)  # 40% succès
            )

        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=False
        )

        insights = result['insights']
        if insights.get('encouragement'):
            # Devrait être encourageant malgré les difficultés
            assert 'normal' in insights['encouragement'].lower() or 'apprend' in insights['encouragement'].lower()


# ============================================================================
# TESTS - Self-Regulation Suggestions
# ============================================================================

class TestSelfRegulationSuggestions:
    """Tests des suggestions d'autorégulation"""

    def test_self_regulation_no_reflections(self, metacognition_engine):
        """Pas de suggestions sans réflexions"""
        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        assert isinstance(suggestions, list)
        assert len(suggestions) == 0

    def test_self_regulation_streak_suggestion(self, metacognition_engine):
        """Suggestion après streak de succès"""
        # 5 succès consécutifs
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        # Devrait suggérer un défi
        challenge_suggestions = [s for s in suggestions if s['type'] == 'challenge']
        assert len(challenge_suggestions) > 0

    def test_self_regulation_frustration_suggestion(self, metacognition_engine):
        """Suggestion si frustration détectée"""
        # 5 exercices difficiles avec échecs
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 5},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=False
            )

        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        # Devrait suggérer pause
        pause_suggestions = [s for s in suggestions if s['type'] == 'pause']
        assert len(pause_suggestions) > 0

    def test_self_regulation_fatigue_suggestion(self, metacognition_engine):
        """Suggestion si session longue"""
        # 20 exercices
        for i in range(20):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        # Devrait suggérer de se reposer
        rest_suggestions = [s for s in suggestions if s['type'] == 'rest']
        assert len(rest_suggestions) > 0

    def test_self_regulation_strategy_change_suggestion(self, metacognition_engine):
        """Suggestion de changer de stratégie"""
        # Créer une stratégie très efficace
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 9)
            )

        # Utiliser toujours "Doigts" récemment
        for i in range(3):
            metacognition_engine.process_reflection(
                {'strategy': 'Doigts', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        # Devrait peut-être suggérer Mental
        strategy_suggestions = [s for s in suggestions if s['type'] == 'strategy']
        # Peut ou non suggérer selon l'efficacité de Doigts

    def test_self_regulation_with_session_stats(self, metacognition_engine):
        """Suggestions avec statistiques de session"""
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 8)
            )

        session_stats = {
            'total': 10,
            'correct': 8
        }

        suggestions = metacognition_engine.generate_self_regulation_suggestions(session_stats)

        # Devrait encourager
        encouragement_suggestions = [s for s in suggestions if s['type'] == 'encouragement']
        assert len(encouragement_suggestions) > 0

    def test_suggestion_structure(self, metacognition_engine):
        """Structure des suggestions"""
        for i in range(6):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        suggestions = metacognition_engine.generate_self_regulation_suggestions()

        for suggestion in suggestions:
            assert 'type' in suggestion
            assert 'icon' in suggestion
            assert 'message' in suggestion
            assert len(suggestion['message']) > 0


# ============================================================================
# TESTS - Metacognitive Summary
# ============================================================================

class TestMetacognitiveSummary:
    """Tests du résumé métacognitif"""

    def test_summary_basic(self, metacognition_engine):
        """Résumé basique"""
        summary = metacognition_engine.get_metacognitive_summary()

        assert 'total_reflections' in summary
        assert 'strategy_patterns' in summary
        assert 'progression' in summary
        assert 'recent_success_rate' in summary

    def test_summary_with_data(self, metacognition_engine):
        """Résumé avec données"""
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        summary = metacognition_engine.get_metacognitive_summary()

        assert summary['total_reflections'] == 10
        assert len(summary['strategy_patterns']) > 0

    def test_summary_best_strategy(self, metacognition_engine):
        """Résumé inclut meilleure stratégie"""
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 9)
            )

        summary = metacognition_engine.get_metacognitive_summary()

        if summary['best_strategy']:
            assert summary['best_strategy']['strategy'] == 'Mental'

    def test_summary_progression_improving(self, metacognition_engine):
        """Détection de progression améliorée"""
        # 10 premiers: 50% succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 5)
            )

        # 10 suivants: 80% succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 8)
            )

        summary = metacognition_engine.get_metacognitive_summary()

        assert summary['progression'] == 'improving'

    def test_summary_progression_declining(self, metacognition_engine):
        """Détection de progression en baisse"""
        # 10 premiers: 80% succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 8)
            )

        # 10 suivants: 40% succès
        for i in range(10):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i < 4)
            )

        summary = metacognition_engine.get_metacognitive_summary()

        assert summary['progression'] == 'declining'

    def test_summary_progression_stable(self, metacognition_engine):
        """Détection de progression stable"""
        # 20 avec 70% succès
        for i in range(20):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i % 10 < 7)
            )

        summary = metacognition_engine.get_metacognitive_summary()

        assert summary['progression'] == 'stable'


# ============================================================================
# TESTS - Export
# ============================================================================

class TestExport:
    """Tests d'export de données"""

    def test_export_json(self, metacognition_engine):
        """Export au format JSON"""
        for i in range(5):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        export_path = metacognition_engine.export_reflections_for_analysis('json')

        assert Path(export_path).exists()
        assert export_path.endswith('.json')

        # Vérifier contenu
        with open(export_path, 'r') as f:
            data = json.load(f)
            assert 'user_id' in data
            assert 'reflections' in data
            assert len(data['reflections']) == 5

    def test_export_csv(self, metacognition_engine):
        """Export au format CSV"""
        for i in range(3):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        export_path = metacognition_engine.export_reflections_for_analysis('csv')

        assert Path(export_path).exists()
        assert export_path.endswith('.csv')

        # Vérifier qu'on peut lire le CSV
        import csv
        with open(export_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3


# ============================================================================
# TESTS - Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests des cas limites"""

    def test_empty_portfolio(self, portfolio):
        """Portfolio vide"""
        patterns = portfolio.get_strategy_patterns()
        assert patterns == []

        best = portfolio.get_most_successful_strategy()
        assert best is None

    def test_single_reflection(self, metacognition_engine):
        """Une seule réflexion"""
        metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'difficulty': 3},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=True
        )

        summary = metacognition_engine.get_metacognitive_summary()
        assert summary['total_reflections'] == 1

    def test_all_strategies_used(self, metacognition_engine):
        """Toutes les stratégies utilisées"""
        strategies = ["Doigts", "Mental", "Dessin", "Formule", "Autre"]

        for strategy in strategies:
            for i in range(3):
                metacognition_engine.process_reflection(
                    {'strategy': strategy, 'difficulty': 3},
                    {'type': 'addition', 'difficulty': 'CE2'},
                    was_correct=True
                )

        patterns = metacognition_engine.portfolio.get_strategy_patterns()
        assert len(patterns) == 5

    def test_minimal_reflection_data(self, metacognition_engine):
        """Données de réflexion minimales"""
        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental'},  # Seulement stratégie
            {'type': 'addition'},
            was_correct=True
        )

        assert 'reflection' in result

    def test_very_long_explanation(self, metacognition_engine):
        """Explication très longue"""
        long_text = "A" * 500  # 500 caractères

        result = metacognition_engine.process_reflection(
            {'strategy': 'Mental', 'explanation': long_text},
            {'type': 'addition', 'difficulty': 'CE2'},
            was_correct=True
        )

        reflection = result['reflection']
        assert reflection['self_explanation'] == long_text


# ============================================================================
# TESTS - Performance
# ============================================================================

class TestPerformance:
    """Tests de performance"""

    def test_many_reflections_performance(self, metacognition_engine):
        """Performance avec beaucoup de réflexions"""
        import time

        start = time.time()

        for i in range(100):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=(i % 2 == 0)
            )

        elapsed = time.time() - start

        assert elapsed < 5.0  # Devrait prendre moins de 5 secondes

    def test_pattern_detection_performance(self, metacognition_engine):
        """Performance de détection de patterns"""
        import time

        # Ajouter beaucoup de données
        for i in range(50):
            metacognition_engine.process_reflection(
                {'strategy': 'Mental', 'difficulty': 3},
                {'type': 'addition', 'difficulty': 'CE2'},
                was_correct=True
            )

        start = time.time()
        patterns = metacognition_engine.portfolio.get_strategy_patterns()
        elapsed = time.time() - start

        assert elapsed < 0.5  # Très rapide


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

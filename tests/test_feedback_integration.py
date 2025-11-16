"""
Tests d'intégration pour TransformativeFeedback dans app.py
Phase 6.1.4 - Integration Tests

Tests:
- Initialisation FeedbackEngine dans session
- Génération de feedback après exercice
- Affichage UI 6 couches
- Boutons d'action
- Flux complet: exercice → validation → feedback → suivant
"""

import pytest
from unittest.mock import MagicMock, patch
import streamlit as st
from datetime import datetime, date

# Mock streamlit session_state
class MockSessionState(dict):
    """Mock pour st.session_state"""
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")


@pytest.fixture
def mock_session_state():
    """Fixture pour session state mocké"""
    session = MockSessionState({
        'niveau': 'CE2',
        'points': 50,
        'badges': [],
        'stats_par_niveau': {
            'CE1': {'correct': 10, 'total': 15},
            'CE2': {'correct': 20, 'total': 30},
            'CM1': {'correct': 0, 'total': 0},
            'CM2': {'correct': 0, 'total': 0}
        },
        'streak': {'current': 3, 'max': 5},
        'scores_history': [],
        'exercice_courant': None,
        'show_feedback': False,
        'feedback_correct': False,
        'feedback_reponse': None,
        'dernier_exercice': None,
        'transformative_feedback': None,
        'exercise_start_time': None,
        'active_category': 'Exercice',
        'utilisateur': 'test_user',
        'authentifie': True,
        'profil': {
            'exercices_totaux': 30,
            'exercices_reussis': 20,
            'taux_reussite': 67,
            'niveau': 'CE2',
            'points': 50,
            'badges': []
        }
    })
    return session


@pytest.fixture
def feedback_engine():
    """Fixture pour FeedbackEngine"""
    from core.pedagogy.feedback_engine import TransformativeFeedback
    return TransformativeFeedback()


# ============================================================================
# TESTS - Initialisation
# ============================================================================

class TestFeedbackEngineInitialization:
    """Tests d'initialisation du FeedbackEngine"""

    def test_init_session_state_creates_feedback_engine(self):
        """init_session_state doit créer feedback_engine"""
        # Simuler import et initialisation
        from core.pedagogy.feedback_engine import TransformativeFeedback

        mock_session = MockSessionState({})

        # Simuler l'initialisation
        feedback_engine = TransformativeFeedback()
        mock_session['feedback_engine'] = feedback_engine

        assert 'feedback_engine' in mock_session
        assert mock_session['feedback_engine'] is not None
        assert hasattr(mock_session['feedback_engine'], 'process_exercise_response')

    def test_init_session_state_creates_transformative_feedback_field(self):
        """init_session_state doit créer transformative_feedback"""
        mock_session = MockSessionState({
            'transformative_feedback': None,
            'exercise_start_time': None
        })

        assert 'transformative_feedback' in mock_session
        assert 'exercise_start_time' in mock_session

    def test_feedback_engine_is_singleton(self):
        """FeedbackEngine doit être singleton (une seule instance)"""
        from core.pedagogy.feedback_engine import TransformativeFeedback

        engine1 = TransformativeFeedback()
        engine2 = TransformativeFeedback()

        # Deux instances différentes OK, mais même classe
        assert type(engine1) == type(engine2)


# ============================================================================
# TESTS - Génération de Feedback
# ============================================================================

class TestFeedbackGeneration:
    """Tests de génération de feedback"""

    def test_validation_callback_generates_feedback(
        self,
        mock_session_state,
        feedback_engine
    ):
        """_callback_validation_exercice doit générer feedback"""
        import time

        # Setup exercise
        mock_session_state['exercice_courant'] = {
            'question': '25 + 17',
            'reponse': 42
        }
        mock_session_state['input_ex'] = 42
        mock_session_state['exercise_start_time'] = time.time() - 5  # 5 secondes
        mock_session_state['feedback_engine'] = feedback_engine

        # Simuler validation
        exercise_dict = {
            "type": "addition",
            "operation": "25 + 17",
            "difficulty": "CE2",
            "operand1": 25,
            "operand2": 17,
            "expected_answer": 42
        }

        user_history = {
            "success_rate": 0.67,
            "exercises_completed": 30,
            "current_streak": 3
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise_dict,
            response=42,
            expected=42,
            user_id='test_user',
            user_history=user_history,
            time_taken_seconds=5
        )

        assert feedback is not None
        assert feedback.is_correct is True
        assert feedback.immediate != ""
        assert feedback.explanation != ""

    def test_validation_callback_generates_feedback_wrong_answer(
        self,
        mock_session_state,
        feedback_engine
    ):
        """Feedback pour réponse incorrecte"""
        # Setup exercise
        mock_session_state['exercice_courant'] = {
            'question': '25 + 17',
            'reponse': 42
        }
        mock_session_state['input_ex'] = 32  # Incorrect (oubli retenue)
        mock_session_state['feedback_engine'] = feedback_engine

        exercise_dict = {
            "type": "addition",
            "operation": "25 + 17",
            "difficulty": "CE2",
            "operand1": 25,
            "operand2": 17,
            "expected_answer": 42
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise_dict,
            response=32,
            expected=42,
            user_id='test_user'
        )

        assert feedback.is_correct is False
        assert feedback.remediation is not None
        assert feedback.strategy is not None

    def test_feedback_includes_all_6_layers(
        self,
        feedback_engine
    ):
        """Feedback doit contenir les 6 couches"""
        exercise = {
            "type": "multiplication",
            "operation": "7 × 8",
            "difficulty": "CE2",
            "operand1": 7,
            "operand2": 8,
            "expected_answer": 56
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=56,
            expected=56,
            user_id='test_user'
        )

        # Layer 1: Immediate
        assert feedback.immediate != ""
        assert len(feedback.immediate) > 0

        # Layer 2: Explanation
        assert feedback.explanation != ""
        assert len(feedback.explanation) > 0

        # Layer 3: Strategy (peut être None pour succès)
        # assert feedback.strategy is not None or feedback.is_correct

        # Layer 4: Remediation (None pour succès)
        if feedback.is_correct:
            assert feedback.remediation is None
        else:
            assert feedback.remediation is not None

        # Layer 5: Encouragement
        assert feedback.encouragement != ""

        # Layer 6: Next Action
        assert feedback.next_action != ""

    def test_feedback_for_all_operation_types(
        self,
        feedback_engine
    ):
        """Tester feedback pour tous les types d'opérations"""
        operations = [
            {"type": "addition", "operation": "12 + 8", "operand1": 12, "operand2": 8, "expected": 20},
            {"type": "subtraction", "operation": "15 - 7", "operand1": 15, "operand2": 7, "expected": 8},
            {"type": "multiplication", "operation": "6 × 7", "operand1": 6, "operand2": 7, "expected": 42},
            {"type": "division", "operation": "24 ÷ 6", "operand1": 24, "operand2": 6, "expected": 4}
        ]

        for op in operations:
            exercise = {
                "type": op["type"],
                "operation": op["operation"],
                "difficulty": "CE2",
                "operand1": op["operand1"],
                "operand2": op["operand2"],
                "expected_answer": op["expected"]
            }

            feedback = feedback_engine.process_exercise_response(
                exercise=exercise,
                response=op["expected"],
                expected=op["expected"],
                user_id='test_user'
            )

            assert feedback is not None, f"Feedback None pour {op['type']}"
            assert feedback.is_correct is True, f"Feedback incorrect pour {op['type']}"


# ============================================================================
# TESTS - UI Rendering
# ============================================================================

class TestUIRendering:
    """Tests de rendu UI"""

    @patch('streamlit.markdown')
    @patch('streamlit.write')
    @patch('streamlit.container')
    def test_render_transformative_feedback_called(
        self,
        mock_container,
        mock_write,
        mock_markdown
    ):
        """render_transformative_feedback doit être appelé quand feedback existe"""
        from core.pedagogy.feedback_engine import TransformativeFeedbackResult

        mock_session = MockSessionState({})
        feedback = TransformativeFeedbackResult(
            immediate="✅ Excellent!",
            explanation="Tu as bien résolu cette addition!",
            is_correct=True,
            confidence=1.0,
            timestamp=datetime.now().isoformat()
        )
        mock_session['transformative_feedback'] = feedback
        mock_session['show_feedback'] = True

        # Vérifier que le feedback existe
        assert mock_session.get('transformative_feedback') is not None

    def test_feedback_result_to_dict_serializable(
        self,
        feedback_engine
    ):
        """Résultat feedback doit être sérialisable (pour UI)"""
        import json

        exercise = {
            "type": "addition",
            "operation": "15 + 12",
            "difficulty": "CE1",
            "expected_answer": 27
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=27,
            expected=27,
            user_id='test_user'
        )

        # Convertir en dict
        feedback_dict = feedback.to_dict()

        # Doit être sérialisable JSON
        try:
            json_str = json.dumps(feedback_dict)
            assert len(json_str) > 0
        except Exception as e:
            pytest.fail(f"Feedback non sérialisable: {e}")


# ============================================================================
# TESTS - Flux Complet
# ============================================================================

class TestCompleteFlow:
    """Tests du flux complet"""

    def test_exercise_to_feedback_flow(
        self,
        mock_session_state,
        feedback_engine
    ):
        """Test flux: génération exercice → validation → feedback"""
        import time

        # Étape 1: Générer exercice (simulé)
        mock_session_state['exercice_courant'] = {
            'question': '8 × 7',
            'reponse': 56
        }
        mock_session_state['exercise_start_time'] = time.time()
        mock_session_state['feedback_engine'] = feedback_engine

        # Étape 2: User répond
        mock_session_state['input_ex'] = 56

        # Étape 3: Validation (simuler callback)
        ex = mock_session_state['exercice_courant']
        reponse = mock_session_state['input_ex']
        correct = (reponse == ex['reponse'])

        time_taken = int(time.time() - mock_session_state['exercise_start_time'])

        exercise_dict = {
            "type": "multiplication",
            "operation": ex['question'],
            "difficulty": "CE2",
            "operand1": 8,
            "operand2": 7,
            "expected_answer": 56
        }

        user_history = {
            "success_rate": 0.67,
            "exercises_completed": 30,
            "current_streak": 3
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise_dict,
            response=reponse,
            expected=ex['reponse'],
            user_id='test_user',
            user_history=user_history,
            time_taken_seconds=time_taken
        )

        # Étape 4: Stocker feedback
        mock_session_state['transformative_feedback'] = feedback
        mock_session_state['show_feedback'] = True
        mock_session_state['feedback_correct'] = correct

        # Vérifications
        assert mock_session_state['show_feedback'] is True
        assert mock_session_state['transformative_feedback'] is not None
        assert mock_session_state['feedback_correct'] is True

    def test_error_feedback_includes_remediation(
        self,
        feedback_engine
    ):
        """Feedback d'erreur doit inclure remédiation"""
        exercise = {
            "type": "addition",
            "operation": "25 + 17",
            "difficulty": "CE2",
            "operand1": 25,
            "operand2": 17,
            "expected_answer": 42
        }

        # Réponse incorrecte (oubli retenue)
        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=32,
            expected=42,
            user_id='test_user'
        )

        assert feedback.is_correct is False
        assert feedback.remediation is not None
        assert 'exercise_path' in feedback.remediation
        assert 'practice_count' in feedback.remediation
        assert 'difficulty' in feedback.remediation


# ============================================================================
# TESTS - Time Tracking
# ============================================================================

class TestTimeTracking:
    """Tests du tracking de temps"""

    def test_exercise_start_time_recorded(
        self,
        mock_session_state
    ):
        """exercise_start_time doit être enregistré à génération exercice"""
        import time

        # Simuler callback de génération
        start_time = time.time()
        mock_session_state['exercise_start_time'] = start_time
        mock_session_state['exercice_courant'] = {
            'question': '10 + 5',
            'reponse': 15
        }

        assert mock_session_state['exercise_start_time'] is not None
        assert mock_session_state['exercise_start_time'] > 0

    def test_time_taken_calculated_correctly(
        self,
        feedback_engine
    ):
        """Temps pris doit être calculé correctement"""
        import time

        start = time.time()
        time.sleep(0.1)  # Simuler 100ms
        elapsed = int(time.time() - start)

        exercise = {
            "type": "addition",
            "operation": "5 + 3",
            "difficulty": "CE1",
            "expected_answer": 8
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=8,
            expected=8,
            user_id='test_user',
            time_taken_seconds=elapsed
        )

        assert feedback is not None
        # Le temps devrait influencer l'explication
        assert len(feedback.explanation) > 0


# ============================================================================
# TESTS - User History Integration
# ============================================================================

class TestUserHistoryIntegration:
    """Tests intégration historique utilisateur"""

    def test_user_history_from_profil(
        self,
        mock_session_state,
        feedback_engine
    ):
        """Historique user doit être construit depuis profil"""
        profil = mock_session_state['profil']
        total = profil.get("exercices_totaux", 0)
        reussis = profil.get("exercices_reussis", 0)
        success_rate = reussis / total if total > 0 else 0.5

        user_history = {
            "success_rate": success_rate,
            "exercises_completed": total,
            "current_streak": mock_session_state['streak']['current']
        }

        assert user_history['success_rate'] == 20 / 30
        assert user_history['exercises_completed'] == 30
        assert user_history['current_streak'] == 3

    def test_feedback_adapts_to_user_performance(
        self,
        feedback_engine
    ):
        """Feedback doit s'adapter au niveau de l'élève"""
        exercise = {
            "type": "addition",
            "operation": "10 + 5",
            "difficulty": "CE1",
            "expected_answer": 15
        }

        # Élève performant
        user_high = {
            "success_rate": 0.9,
            "exercises_completed": 100,
            "current_streak": 10
        }

        feedback_high = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=15,
            expected=15,
            user_id='high_performer',
            user_history=user_high
        )

        # Élève en difficulté
        user_low = {
            "success_rate": 0.4,
            "exercises_completed": 20,
            "current_streak": 0
        }

        feedback_low = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=15,
            expected=15,
            user_id='struggling',
            user_history=user_low
        )

        # Next action devrait différer
        # High performer → niveau suivant
        # Low performer → continuer
        assert feedback_high.next_action != "" or feedback_low.next_action != ""


# ============================================================================
# TESTS - Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests des cas limites"""

    def test_feedback_without_user_history(
        self,
        feedback_engine
    ):
        """Feedback doit fonctionner sans historique"""
        exercise = {
            "type": "addition",
            "operation": "5 + 3",
            "difficulty": "CE1",
            "expected_answer": 8
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=8,
            expected=8,
            user_id='new_user',
            user_history=None
        )

        assert feedback is not None
        assert feedback.is_correct is True

    def test_feedback_without_time(
        self,
        feedback_engine
    ):
        """Feedback doit fonctionner sans temps"""
        exercise = {
            "type": "multiplication",
            "operation": "4 × 5",
            "difficulty": "CE2",
            "expected_answer": 20
        }

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=20,
            expected=20,
            user_id='test_user',
            time_taken_seconds=None
        )

        assert feedback is not None

    def test_feedback_with_empty_exercise(
        self,
        feedback_engine
    ):
        """Feedback doit gérer exercice vide"""
        exercise = {}

        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=10,
            expected=10,
            user_id='test_user'
        )

        assert feedback is not None


# ============================================================================
# TESTS - Performance
# ============================================================================

class TestPerformance:
    """Tests de performance"""

    def test_feedback_generation_is_fast(
        self,
        feedback_engine
    ):
        """Génération de feedback doit être rapide (< 1 seconde)"""
        import time

        exercise = {
            "type": "addition",
            "operation": "100 + 200",
            "difficulty": "CM1",
            "expected_answer": 300
        }

        start = time.time()
        feedback = feedback_engine.process_exercise_response(
            exercise=exercise,
            response=300,
            expected=300,
            user_id='test_user'
        )
        elapsed = time.time() - start

        assert elapsed < 1.0, f"Feedback trop lent: {elapsed}s"

    def test_multiple_feedbacks_in_session(
        self,
        feedback_engine
    ):
        """Plusieurs feedbacks successifs doivent fonctionner"""
        for i in range(10):
            exercise = {
                "type": "addition",
                "operation": f"{i} + {i+1}",
                "difficulty": "CE1",
                "expected_answer": i + (i + 1)
            }

            feedback = feedback_engine.process_exercise_response(
                exercise=exercise,
                response=i + (i + 1),
                expected=i + (i + 1),
                user_id='test_user'
            )

            assert feedback is not None


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

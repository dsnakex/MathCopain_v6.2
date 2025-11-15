"""
Tests pour core/session_manager.py
Tests du gestionnaire centralisé de session Streamlit
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from core.session_manager import SessionManager


@pytest.fixture
def mock_session_state():
    """Mock de st.session_state pour tests isolés."""
    return {}


@pytest.fixture
def session_manager(mock_session_state):
    """Fixture SessionManager avec mock session state."""
    with patch('core.session_manager.st.session_state', mock_session_state):
        manager = SessionManager()
        return manager


class TestSessionManagerInit:
    """Tests d'initialisation du SessionManager."""

    def test_init_creates_default_state(self, session_manager, mock_session_state):
        """L'initialisation doit créer l'état par défaut."""
        assert 'niveau' in mock_session_state
        assert mock_session_state['niveau'] == 'CE1'
        assert 'points' in mock_session_state
        assert mock_session_state['points'] == 0
        assert 'badges' in mock_session_state
        assert mock_session_state['badges'] == []

    def test_init_creates_stats_structure(self, session_manager, mock_session_state):
        """L'initialisation doit créer la structure stats_par_niveau."""
        stats = mock_session_state['stats_par_niveau']
        assert 'CE1' in stats
        assert 'CE2' in stats
        assert 'CM1' in stats
        assert 'CM2' in stats
        for niveau in stats.values():
            assert 'correct' in niveau
            assert 'total' in niveau

    def test_init_creates_streak_structure(self, session_manager, mock_session_state):
        """L'initialisation doit créer la structure streak."""
        streak = mock_session_state['streak']
        assert 'current' in streak
        assert 'max' in streak
        assert streak['current'] == 0
        assert streak['max'] == 0

    def test_init_does_not_override_existing_values(self, mock_session_state):
        """L'initialisation ne doit pas écraser les valeurs existantes."""
        mock_session_state['niveau'] = 'CM2'
        mock_session_state['points'] = 100

        with patch('core.session_manager.st.session_state', mock_session_state):
            SessionManager()

        assert mock_session_state['niveau'] == 'CM2'
        assert mock_session_state['points'] == 100


class TestGetters:
    """Tests des méthodes getter."""

    def test_get_niveau(self, session_manager):
        """get_niveau() retourne le niveau actuel."""
        assert session_manager.get_niveau() == 'CE1'

    def test_get_points(self, session_manager):
        """get_points() retourne les points actuels."""
        assert session_manager.get_points() == 0
        session_manager.set_points(50)
        assert session_manager.get_points() == 50

    def test_get_badges(self, session_manager):
        """get_badges() retourne la liste des badges."""
        assert session_manager.get_badges() == []
        session_manager.add_badge("🏆 Champion")
        assert "🏆 Champion" in session_manager.get_badges()

    def test_get_streak(self, session_manager):
        """get_streak() retourne le dict streak."""
        streak = session_manager.get_streak()
        assert isinstance(streak, dict)
        assert 'current' in streak
        assert 'max' in streak

    def test_get_stats_par_niveau(self, session_manager):
        """get_stats_par_niveau() retourne les stats."""
        stats = session_manager.get_stats_par_niveau()
        assert isinstance(stats, dict)
        assert 'CE1' in stats

    def test_get_exercice_courant_when_none(self, session_manager):
        """get_exercice_courant() retourne None si pas d'exercice."""
        assert session_manager.get_exercice_courant() is None

    def test_get_profil_when_not_set(self, session_manager):
        """get_profil() retourne None si pas de profil."""
        assert session_manager.get_profil() is None

    def test_get_utilisateur_when_not_set(self, session_manager):
        """get_utilisateur() retourne None si pas connecté."""
        assert session_manager.get_utilisateur() is None


class TestSetters:
    """Tests des méthodes setter."""

    def test_set_niveau_valid(self, session_manager):
        """set_niveau() avec niveau valide."""
        session_manager.set_niveau('CM2')
        assert session_manager.get_niveau() == 'CM2'

    def test_set_niveau_invalid_ignored(self, session_manager):
        """set_niveau() avec niveau invalide est ignoré."""
        original = session_manager.get_niveau()
        session_manager.set_niveau('INVALID')
        assert session_manager.get_niveau() == original

    def test_set_points(self, session_manager):
        """set_points() définit les points."""
        session_manager.set_points(100)
        assert session_manager.get_points() == 100

    def test_set_points_negative_becomes_zero(self, session_manager):
        """set_points() avec valeur négative devient 0."""
        session_manager.set_points(-50)
        assert session_manager.get_points() == 0

    def test_add_points_positive(self, session_manager):
        """add_points() ajoute des points positifs."""
        session_manager.set_points(50)
        session_manager.add_points(30)
        assert session_manager.get_points() == 80

    def test_add_points_negative(self, session_manager):
        """add_points() peut retirer des points."""
        session_manager.set_points(50)
        session_manager.add_points(-20)
        assert session_manager.get_points() == 30

    def test_add_points_negative_cannot_go_below_zero(self, session_manager):
        """add_points() ne peut pas descendre sous 0."""
        session_manager.set_points(10)
        session_manager.add_points(-50)
        assert session_manager.get_points() == 0

    def test_add_badge_new(self, session_manager):
        """add_badge() ajoute un nouveau badge."""
        session_manager.add_badge("🌟 Premier Pas")
        assert "🌟 Premier Pas" in session_manager.get_badges()

    def test_add_badge_duplicate_ignored(self, session_manager):
        """add_badge() ignore les doublons."""
        session_manager.add_badge("🌟 Premier Pas")
        session_manager.add_badge("🌟 Premier Pas")
        badges = session_manager.get_badges()
        assert badges.count("🌟 Premier Pas") == 1

    def test_set_exercice_courant(self, session_manager):
        """set_exercice_courant() définit l'exercice."""
        exercice = {'question': '5+3', 'reponse': 8}
        session_manager.set_exercice_courant(exercice)
        assert session_manager.get_exercice_courant() == exercice

    def test_set_feedback(self, session_manager, mock_session_state):
        """set_feedback() active le feedback."""
        session_manager.set_feedback(True, 42)
        assert mock_session_state['show_feedback'] is True
        assert mock_session_state['feedback_correct'] is True
        assert mock_session_state['feedback_reponse'] == 42

    def test_clear_feedback(self, session_manager, mock_session_state):
        """clear_feedback() désactive le feedback."""
        session_manager.set_feedback(True, 42)
        session_manager.clear_feedback()
        assert mock_session_state['show_feedback'] is False
        assert mock_session_state['feedback_correct'] is False
        assert mock_session_state['feedback_reponse'] is None


class TestStreakManagement:
    """Tests de la gestion des streaks."""

    def test_update_streak_correct_increases(self, session_manager):
        """update_streak() avec correct=True augmente le streak."""
        streak1 = session_manager.update_streak(True)
        assert streak1 == 1
        streak2 = session_manager.update_streak(True)
        assert streak2 == 2

    def test_update_streak_incorrect_resets(self, session_manager):
        """update_streak() avec correct=False remet à 0."""
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        streak = session_manager.update_streak(False)
        assert streak == 0

    def test_update_streak_updates_max(self, session_manager):
        """update_streak() met à jour max streak."""
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        streak_data = session_manager.get_streak()
        assert streak_data['max'] == 3

    def test_update_streak_max_not_decreased(self, session_manager):
        """update_streak() ne diminue jamais max."""
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        session_manager.update_streak(False)
        streak_data = session_manager.get_streak()
        assert streak_data['max'] == 3
        assert streak_data['current'] == 0

    def test_get_streak_bonus_zero(self, session_manager):
        """get_streak_bonus() retourne 0 pour streak < 3."""
        assert session_manager.get_streak_bonus() == 0
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        assert session_manager.get_streak_bonus() == 0

    def test_get_streak_bonus_small(self, session_manager):
        """get_streak_bonus() retourne 10 pour streak 3-4."""
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        session_manager.update_streak(True)
        assert session_manager.get_streak_bonus() == 10

    def test_get_streak_bonus_medium(self, session_manager):
        """get_streak_bonus() retourne 20 pour streak 5-9."""
        for _ in range(5):
            session_manager.update_streak(True)
        assert session_manager.get_streak_bonus() == 20

    def test_get_streak_bonus_large(self, session_manager):
        """get_streak_bonus() retourne 50 pour streak >= 10."""
        for _ in range(10):
            session_manager.update_streak(True)
        assert session_manager.get_streak_bonus() == 50


class TestStatsManagement:
    """Tests de la gestion des statistiques."""

    def test_record_exercise_result_correct(self, session_manager):
        """record_exercise_result() enregistre résultat correct."""
        session_manager.record_exercise_result('CE1', True)
        stats = session_manager.get_stats_par_niveau()
        assert stats['CE1']['total'] == 1
        assert stats['CE1']['correct'] == 1

    def test_record_exercise_result_incorrect(self, session_manager):
        """record_exercise_result() enregistre résultat incorrect."""
        session_manager.record_exercise_result('CE1', False)
        stats = session_manager.get_stats_par_niveau()
        assert stats['CE1']['total'] == 1
        assert stats['CE1']['correct'] == 0

    def test_record_exercise_result_multiple(self, session_manager):
        """record_exercise_result() accumule correctement."""
        session_manager.record_exercise_result('CM1', True)
        session_manager.record_exercise_result('CM1', True)
        session_manager.record_exercise_result('CM1', False)
        stats = session_manager.get_stats_par_niveau()
        assert stats['CM1']['total'] == 3
        assert stats['CM1']['correct'] == 2

    def test_calculate_progression_zero_exercises(self, session_manager):
        """calculate_progression() avec 0 exercices retourne 0%."""
        progression = session_manager.calculate_progression()
        assert progression['CE1'] == 0
        assert progression['CE2'] == 0

    def test_calculate_progression_perfect_score(self, session_manager):
        """calculate_progression() avec 100% correct."""
        for _ in range(10):
            session_manager.record_exercise_result('CE2', True)
        progression = session_manager.calculate_progression()
        assert progression['CE2'] == 100

    def test_calculate_progression_partial(self, session_manager):
        """calculate_progression() avec score partiel."""
        session_manager.record_exercise_result('CM2', True)
        session_manager.record_exercise_result('CM2', True)
        session_manager.record_exercise_result('CM2', False)
        progression = session_manager.calculate_progression()
        # 2/3 = 66.666... → int(66.666) = 66
        assert progression['CM2'] == 66

    def test_calculate_progression_all_levels(self, session_manager):
        """calculate_progression() retourne tous les niveaux."""
        progression = session_manager.calculate_progression()
        assert 'CE1' in progression
        assert 'CE2' in progression
        assert 'CM1' in progression
        assert 'CM2' in progression


class TestAutoSaveProfil:
    """Tests de l'auto-sauvegarde du profil."""

    def test_auto_save_when_not_authenticated(self, session_manager):
        """auto_save_profil() ne fait rien si pas authentifié."""
        # Should not raise exception
        session_manager.auto_save_profil(True)

    @patch('utilisateur.sauvegarder_utilisateur')
    def test_auto_save_updates_profil_data(self, mock_save, session_manager, mock_session_state):
        """auto_save_profil() met à jour les données du profil."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {
            'exercices_reussis': 0,
            'exercices_totaux': 0
        }
        session_manager.set_points(100)

        session_manager.auto_save_profil(True)

        profil = mock_session_state['profil']
        assert profil['points'] == 100
        assert profil['exercices_reussis'] == 1
        assert profil['exercices_totaux'] == 1

    @patch('utilisateur.sauvegarder_utilisateur')
    def test_auto_save_success_increments_counters(self, mock_save, session_manager, mock_session_state):
        """auto_save_profil(success=True) incrémente compteurs."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {
            'exercices_reussis': 5,
            'exercices_totaux': 10
        }

        session_manager.auto_save_profil(True)

        profil = mock_session_state['profil']
        assert profil['exercices_reussis'] == 6
        assert profil['exercices_totaux'] == 11

    @patch('utilisateur.sauvegarder_utilisateur')
    def test_auto_save_failure_only_increments_total(self, mock_save, session_manager, mock_session_state):
        """auto_save_profil(success=False) incrémente seulement total."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {
            'exercices_reussis': 5,
            'exercices_totaux': 10
        }

        session_manager.auto_save_profil(False)

        profil = mock_session_state['profil']
        assert profil['exercices_reussis'] == 5
        assert profil['exercices_totaux'] == 11

    @patch('utilisateur.sauvegarder_utilisateur')
    def test_auto_save_calculates_success_rate(self, mock_save, session_manager, mock_session_state):
        """auto_save_profil() calcule le taux de réussite."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {
            'exercices_reussis': 7,
            'exercices_totaux': 10
        }

        session_manager.auto_save_profil(True)

        profil = mock_session_state['profil']
        # 8/11 = 72.727... → int(72.727) = 72
        assert profil['taux_reussite'] == 72

    @patch('utilisateur.sauvegarder_utilisateur')
    def test_auto_save_calls_sauvegarder(self, mock_save, session_manager, mock_session_state):
        """auto_save_profil() appelle sauvegarder_utilisateur."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {}

        session_manager.auto_save_profil(True)

        mock_save.assert_called_once()
        assert mock_save.call_args[0][0] == 'TestUser'


class TestUtilityMethods:
    """Tests des méthodes utilitaires."""

    def test_reset_exercise_state(self, session_manager, mock_session_state):
        """reset_exercise_state() réinitialise l'état exercice."""
        mock_session_state['exercice_courant'] = {'question': '5+3'}
        mock_session_state['dernier_exercice'] = {'question': '2+2'}
        session_manager.set_feedback(True, 42)

        session_manager.reset_exercise_state()

        assert mock_session_state['exercice_courant'] is None
        assert mock_session_state['dernier_exercice'] is None
        assert mock_session_state['show_feedback'] is False

    def test_is_authenticated_false_when_no_user(self, session_manager):
        """is_authenticated() retourne False sans utilisateur."""
        assert session_manager.is_authenticated() is False

    def test_is_authenticated_true_when_logged_in(self, session_manager, mock_session_state):
        """is_authenticated() retourne True si connecté."""
        mock_session_state['utilisateur'] = 'TestUser'
        mock_session_state['profil'] = {}
        assert session_manager.is_authenticated() is True

    def test_is_authenticated_false_without_profil(self, session_manager, mock_session_state):
        """is_authenticated() retourne False sans profil."""
        mock_session_state['utilisateur'] = 'TestUser'
        # No profil
        assert session_manager.is_authenticated() is False

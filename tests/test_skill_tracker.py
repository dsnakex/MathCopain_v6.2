"""Tests pour le suivi des compétences (SkillTracker)."""
import pytest
from datetime import datetime
from skill_tracker import SkillTracker


@pytest.fixture
def profil_vide():
    """Profil utilisateur vide pour tests."""
    return {
        'nom': 'Test User',
        'grade': 'CM1'
    }


@pytest.fixture
def profil_avec_historique():
    """Profil utilisateur avec historique pour tests."""
    return {
        'nom': 'Test User',
        'grade': 'CM1',
        'stats_par_type': {
            'addition': {'correct': 8, 'total': 10},
            'soustraction': {'correct': 3, 'total': 10},
            'multiplication': {'correct': 5, 'total': 5},
        },
        'exercise_history': [
            {'type': 'addition', 'correct': True, 'difficulty': 3, 'timestamp': datetime.now().isoformat()},
            {'type': 'addition', 'correct': True, 'difficulty': 3, 'timestamp': datetime.now().isoformat()},
            {'type': 'soustraction', 'correct': False, 'difficulty': 4, 'timestamp': datetime.now().isoformat()},
        ]
    }


class TestSkillTrackerInit:
    """Tests de l'initialisation du SkillTracker."""

    def test_init_profil_vide(self, profil_vide):
        """Initialiser avec profil vide crée stats_par_type."""
        tracker = SkillTracker(profil_vide)

        assert 'stats_par_type' in tracker.profil
        assert 'exercise_history' in tracker.profil

    def test_init_cree_tous_types_exercices(self, profil_vide):
        """Initialisation crée tous les types d'exercices."""
        tracker = SkillTracker(profil_vide)

        types_attendus = [
            'addition', 'soustraction', 'multiplication', 'division',
            'probleme', 'fractions', 'géométrie', 'decimaux',
            'proportionnalite', 'mesures', 'monnaie'
        ]

        for type_ex in types_attendus:
            assert type_ex in tracker.profil['stats_par_type']
            assert 'correct' in tracker.profil['stats_par_type'][type_ex]
            assert 'total' in tracker.profil['stats_par_type'][type_ex]

    def test_init_preserve_donnees_existantes(self, profil_avec_historique):
        """Initialisation préserve les données existantes."""
        tracker = SkillTracker(profil_avec_historique)

        assert tracker.profil['stats_par_type']['addition']['correct'] == 8
        assert tracker.profil['stats_par_type']['addition']['total'] == 10
        assert len(tracker.profil['exercise_history']) == 3


class TestRecordExercise:
    """Tests de l'enregistrement d'exercices."""

    def test_record_exercice_correct(self, profil_vide):
        """Enregistrer un exercice réussi."""
        tracker = SkillTracker(profil_vide)
        tracker.record_exercise('addition', correct=True, difficulty=3)

        assert tracker.profil['stats_par_type']['addition']['total'] == 1
        assert tracker.profil['stats_par_type']['addition']['correct'] == 1
        assert len(tracker.profil['exercise_history']) == 1

    def test_record_exercice_incorrect(self, profil_vide):
        """Enregistrer un exercice échoué."""
        tracker = SkillTracker(profil_vide)
        tracker.record_exercise('soustraction', correct=False, difficulty=4)

        assert tracker.profil['stats_par_type']['soustraction']['total'] == 1
        assert tracker.profil['stats_par_type']['soustraction']['correct'] == 0

    def test_record_multiple_exercices(self, profil_vide):
        """Enregistrer plusieurs exercices."""
        tracker = SkillTracker(profil_vide)

        tracker.record_exercise('addition', correct=True, difficulty=2)
        tracker.record_exercise('addition', correct=True, difficulty=3)
        tracker.record_exercise('addition', correct=False, difficulty=4)

        assert tracker.profil['stats_par_type']['addition']['total'] == 3
        assert tracker.profil['stats_par_type']['addition']['correct'] == 2

    def test_record_avec_temps(self, profil_vide):
        """Enregistrer exercice avec temps."""
        tracker = SkillTracker(profil_vide)
        tracker.record_exercise('multiplication', correct=True, difficulty=3, time_taken=45.5)

        exercice = tracker.profil['exercise_history'][0]
        assert exercice['time_taken'] == 45.5

    def test_historique_limite_100(self, profil_vide):
        """L'historique est limité à 100 exercices."""
        tracker = SkillTracker(profil_vide)

        # Ajouter 150 exercices
        for i in range(150):
            tracker.record_exercise('addition', correct=True, difficulty=3)

        # Devrait garder seulement les 100 derniers
        assert len(tracker.profil['exercise_history']) == 100

    def test_timestamp_automatique(self, profil_vide):
        """Le timestamp est ajouté automatiquement."""
        tracker = SkillTracker(profil_vide)
        tracker.record_exercise('division', correct=True, difficulty=3)

        exercice = tracker.profil['exercise_history'][0]
        assert 'timestamp' in exercice
        # Vérifier que c'est un ISO timestamp valide
        datetime.fromisoformat(exercice['timestamp'])


class TestSuccessRateByType:
    """Tests du calcul du taux de réussite par type."""

    def test_taux_reussite_100_pourcent(self, profil_avec_historique):
        """Type avec 100% de réussite."""
        tracker = SkillTracker(profil_avec_historique)
        rates = tracker.get_success_rate_by_type()

        assert rates['multiplication'] == 1.0  # 5/5

    def test_taux_reussite_partiel(self, profil_avec_historique):
        """Type avec réussite partielle."""
        tracker = SkillTracker(profil_avec_historique)
        rates = tracker.get_success_rate_by_type()

        assert rates['addition'] == 0.8  # 8/10
        assert rates['soustraction'] == 0.3  # 3/10

    def test_taux_reussite_zero_exercices(self, profil_vide):
        """Type jamais pratiqué a taux 0."""
        tracker = SkillTracker(profil_vide)
        rates = tracker.get_success_rate_by_type()

        assert rates['addition'] == 0.0

    def test_tous_types_dans_resultat(self, profil_vide):
        """Tous les types sont dans le résultat."""
        tracker = SkillTracker(profil_vide)
        rates = tracker.get_success_rate_by_type()

        types_attendus = [
            'addition', 'soustraction', 'multiplication', 'division',
            'probleme', 'fractions', 'géométrie', 'decimaux',
            'proportionnalite', 'mesures', 'monnaie'
        ]

        for type_ex in types_attendus:
            assert type_ex in rates


class TestWeakAreas:
    """Tests de l'identification des domaines faibles."""

    def test_identification_domaine_faible(self, profil_avec_historique):
        """Identifier domaines avec taux < 50%."""
        tracker = SkillTracker(profil_avec_historique)
        weak = tracker.get_weak_areas(threshold=0.5)

        # soustraction a 30% (3/10), devrait être faible
        assert 'soustraction' in weak

    def test_domaine_fort_non_inclus(self, profil_avec_historique):
        """Domaines forts ne sont pas dans weak."""
        tracker = SkillTracker(profil_avec_historique)
        weak = tracker.get_weak_areas(threshold=0.5)

        # addition a 80%, multiplication 100%, pas faibles
        assert 'addition' not in weak
        assert 'multiplication' not in weak

    def test_minimum_3_exercices_requis(self, profil_vide):
        """Domaines avec < 3 exercices ne sont pas considérés."""
        tracker = SkillTracker(profil_vide)

        # 2 exercices échoués
        tracker.record_exercise('division', correct=False, difficulty=3)
        tracker.record_exercise('division', correct=False, difficulty=3)

        weak = tracker.get_weak_areas()

        # Ne devrait pas être dans weak car < 3 total
        assert 'division' not in weak

    def test_threshold_personnalise(self, profil_avec_historique):
        """Utiliser un threshold personnalisé."""
        tracker = SkillTracker(profil_avec_historique)

        # Avec threshold 0.85, addition (80%) devrait être faible
        weak = tracker.get_weak_areas(threshold=0.85)

        assert 'addition' in weak


class TestStrongAreas:
    """Tests de l'identification des domaines maîtrisés."""

    def test_identification_domaine_fort(self, profil_avec_historique):
        """Identifier domaines avec taux >= 75%."""
        tracker = SkillTracker(profil_avec_historique)
        strong = tracker.get_strong_areas(threshold=0.75)

        # addition a 80%, multiplication 100%
        assert 'addition' in strong
        assert 'multiplication' in strong

    def test_domaine_faible_non_inclus(self, profil_avec_historique):
        """Domaines faibles ne sont pas dans strong."""
        tracker = SkillTracker(profil_avec_historique)
        strong = tracker.get_strong_areas(threshold=0.75)

        # soustraction a 30%
        assert 'soustraction' not in strong

    def test_minimum_5_exercices_requis(self, profil_vide):
        """Domaines avec < 5 exercices ne sont pas forts."""
        tracker = SkillTracker(profil_vide)

        # 4 exercices réussis (100%)
        for _ in range(4):
            tracker.record_exercise('fractions', correct=True, difficulty=3)

        strong = tracker.get_strong_areas()

        # Ne devrait pas être fort car < 5 total
        assert 'fractions' not in strong


class TestIntegration:
    """Tests d'intégration du SkillTracker."""

    def test_cycle_complet_apprentissage(self, profil_vide):
        """Simuler un cycle d'apprentissage complet."""
        tracker = SkillTracker(profil_vide)

        # Phase 1: Difficulté avec soustraction
        for _ in range(5):
            tracker.record_exercise('soustraction', correct=False, difficulty=3)

        weak = tracker.get_weak_areas()
        assert 'soustraction' in weak

        # Phase 2: Amélioration
        for _ in range(10):
            tracker.record_exercise('soustraction', correct=True, difficulty=3)

        rates = tracker.get_success_rate_by_type()
        # 10 bonnes sur 15 total = 66%
        assert 0.6 <= rates['soustraction'] <= 0.7

        # Ne devrait plus être dans weak (> 50%)
        weak = tracker.get_weak_areas()
        assert 'soustraction' not in weak

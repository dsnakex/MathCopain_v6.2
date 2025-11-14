import pytest
from src.adaptive_system import (
    ajuster_difficulte,
    calculer_performance,
    appliquer_streak_bonus,
    appliquer_penalite_echecs
)


class TestCalculPerformance:
    """Tests du calcul de performance."""
    
    def test_performance_parfaite(self):
        """100% de bonnes réponses = performance 100%."""
        perf = calculer_performance(bonnes=10, total=10)
        assert perf == 100
    
    def test_performance_50pourcent(self):
        """50% de bonnes réponses."""
        perf = calculer_performance(bonnes=5, total=10)
        assert perf == 50
    
    def test_performance_nulle(self):
        """Aucune bonne réponse = 0%."""
        perf = calculer_performance(bonnes=0, total=10)
        assert perf == 0


class TestAjustementDifficulte:
    """Tests de l'ajustement du niveau de difficulté."""
    
    def test_montee_difficulte(self):
        """Performance > 85% → montée niveau (+1)."""
        nouveau_niveau = ajuster_difficulte(
            niveau_actuel=2,
            performance=90
        )
        assert nouveau_niveau == 3
    
    def test_descente_difficulte(self):
        """Performance < 50% → descente niveau (-1)."""
        nouveau_niveau = ajuster_difficulte(
            niveau_actuel=3,
            performance=40
        )
        assert nouveau_niveau == 2
    
    def test_plateau_difficulte(self):
        """Performance 50-85% → pas de changement."""
        nouveau_niveau = ajuster_difficulte(
            niveau_actuel=2,
            performance=65
        )
        assert nouveau_niveau == 2
    
    def test_limite_min(self):
        """Niveau minimum = 1."""
        nouveau_niveau = ajuster_difficulte(
            niveau_actuel=1,
            performance=30
        )
        assert nouveau_niveau == 1
    
    def test_limite_max(self):
        """Niveau maximum = 5."""
        nouveau_niveau = ajuster_difficulte(
            niveau_actuel=5,
            performance=100
        )
        assert nouveau_niveau == 5


class TestStreakBonus:
    """Tests du bonus pour série de bonnes réponses."""
    
    def test_pas_de_streak(self):
        """Pas de streak : pas de bonus."""
        bonus = appliquer_streak_bonus(streak=0)
        assert bonus == 0
    
    def test_streak_3(self):
        """Streak de 3 → bonus modéré."""
        bonus = appliquer_streak_bonus(streak=3)
        assert bonus > 0
    
    def test_streak_10(self):
        """Streak de 10 → bonus important."""
        bonus_10 = appliquer_streak_bonus(streak=10)
        bonus_5 = appliquer_streak_bonus(streak=5)
        assert bonus_10 > bonus_5


class TestPenaliteEchecs:
    """Tests de la pénalité pour échecs consécutifs."""
    
    def test_pas_echec(self):
        """Pas d'échec : pas de pénalité."""
        penalite = appliquer_penalite_echecs(echecs_consecutifs=0)
        assert penalite == 0
    
    def test_1_echec(self):
        """1 échec : pénalité légère."""
        penalite = appliquer_penalite_echecs(echecs_consecutifs=1)
        assert penalite > 0
    
    def test_5_echecs(self):
        """5 échecs : pénalité progressive."""
        penalite_5 = appliquer_penalite_echecs(echecs_consecutifs=5)
        penalite_2 = appliquer_penalite_echecs(echecs_consecutifs=2)
        assert penalite_5 > penalite_2
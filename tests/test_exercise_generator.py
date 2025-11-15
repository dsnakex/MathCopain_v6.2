"""
Tests pour core/exercise_generator.py
Tests basiques du générateur d'exercices
"""

import pytest
from core.exercise_generator import (
    generer_addition,
    generer_soustraction,
    generer_tables,
    generer_division,
    generer_probleme,
    generer_droite_numerique,
    calculer_score_droite,
    generer_explication
)


class TestGenererAddition:
    """Tests de génération d'additions."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_addition() génère exercice pour chaque niveau."""
        exercice = generer_addition(niveau)
        assert 'question' in exercice
        assert 'reponse' in exercice
        assert isinstance(exercice['question'], str)
        assert isinstance(exercice['reponse'], int)

    def test_addition_contient_plus(self):
        """La question contient le symbole +."""
        exercice = generer_addition("CE1")
        assert '+' in exercice['question']

    def test_calcul_correct(self):
        """La réponse est le calcul correct."""
        exercice = generer_addition("CE1")
        # Parser la question "a + b"
        parts = exercice['question'].split('+')
        a, b = int(parts[0].strip()), int(parts[1].strip())
        assert exercice['reponse'] == a + b

    def test_valeurs_positives(self):
        """Les nombres sont positifs."""
        for _ in range(10):
            exercice = generer_addition("CE1")
            parts = exercice['question'].split('+')
            a, b = int(parts[0].strip()), int(parts[1].strip())
            assert a > 0
            assert b > 0


class TestGenererSoustraction:
    """Tests de génération de soustractions."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_soustraction() génère exercice pour chaque niveau."""
        exercice = generer_soustraction(niveau)
        assert 'question' in exercice
        assert 'reponse' in exercice

    def test_soustraction_contient_moins(self):
        """La question contient le symbole -."""
        exercice = generer_soustraction("CE1")
        assert '-' in exercice['question']

    def test_calcul_correct(self):
        """La réponse est le calcul correct."""
        exercice = generer_soustraction("CM1")
        parts = exercice['question'].split('-')
        a, b = int(parts[0].strip()), int(parts[1].strip())
        assert exercice['reponse'] == a - b

    def test_resultat_non_negatif(self):
        """Le résultat n'est jamais négatif (a > b)."""
        for _ in range(20):
            exercice = generer_soustraction("CE2")
            assert exercice['reponse'] >= 0


class TestGenererTables:
    """Tests de génération de multiplications."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_tables() génère exercice pour chaque niveau."""
        exercice = generer_tables(niveau)
        assert 'question' in exercice
        assert 'reponse' in exercice

    def test_multiplication_contient_symbole(self):
        """La question contient le symbole ×."""
        exercice = generer_tables("CE1")
        assert '×' in exercice['question']

    def test_calcul_correct(self):
        """La réponse est le calcul correct."""
        exercice = generer_tables("CM1")
        parts = exercice['question'].split('×')
        a, b = int(parts[0].strip()), int(parts[1].strip())
        assert exercice['reponse'] == a * b

    def test_difficulte_progressive(self):
        """Les valeurs augmentent avec le niveau."""
        # CE1 : tables 2-5
        for _ in range(10):
            exercice = generer_tables("CE1")
            parts = exercice['question'].split('×')
            table = int(parts[0].strip())
            assert 2 <= table <= 5

        # CM2 : tables plus grandes
        for _ in range(10):
            exercice = generer_tables("CM2")
            parts = exercice['question'].split('×')
            table = int(parts[0].strip())
            # Peut aller jusqu'à 15
            assert table >= 1


class TestGenererDivision:
    """Tests de génération de divisions."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_division() génère exercice pour chaque niveau."""
        exercice = generer_division(niveau)
        assert 'question' in exercice
        assert 'reponse' in exercice
        assert 'reste' in exercice

    def test_division_contient_symbole(self):
        """La question contient le symbole ÷."""
        exercice = generer_division("CE2")
        assert '÷' in exercice['question']

    def test_division_CE1_fallback_tables(self):
        """Division CE1 retourne tables (fallback)."""
        exercice = generer_division("CE1")
        # Devrait être multiplication
        assert '×' in exercice['question']

    def test_calcul_euclidien_correct(self):
        """La division euclidienne est correcte."""
        for _ in range(20):
            exercice = generer_division("CM1")
            if '÷' in exercice['question']:
                parts = exercice['question'].split('÷')
                dividende = int(parts[0].strip())
                diviseur = int(parts[1].strip())
                quotient = exercice['reponse']
                reste = exercice['reste']

                # Vérifier: dividende = quotient * diviseur + reste
                assert dividende == (quotient * diviseur) + reste
                assert 0 <= reste < diviseur


class TestGenererProbleme:
    """Tests de génération de problèmes."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_probleme() génère pour chaque niveau."""
        exercice = generer_probleme(niveau)
        assert 'question' in exercice
        assert 'reponse' in exercice

    def test_question_contient_contexte(self):
        """La question contient du texte contextuel."""
        exercice = generer_probleme("CE1")
        # Devrait contenir noms ou contexte
        question = exercice['question'].lower()
        contextes = ['marie', 'théo', 'billes', 'euros', 'bonbons', 'chaises']
        assert any(ctx in question for ctx in contextes)

    def test_reponse_positive(self):
        """La réponse est positive (cohérence)."""
        for _ in range(20):
            exercice = generer_probleme("CE2")
            assert exercice['reponse'] >= 0


class TestGenererDroiteNumerique:
    """Tests de génération droite numérique."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_droite_numerique() génère pour chaque niveau."""
        exercice = generer_droite_numerique(niveau)
        assert 'nombre' in exercice
        assert 'min' in exercice
        assert 'max' in exercice

    def test_nombre_dans_intervalle(self):
        """Le nombre est dans l'intervalle [min, max]."""
        exercice = generer_droite_numerique("CE1")
        assert exercice['min'] <= exercice['nombre'] <= exercice['max']

    def test_difficulte_progressive(self):
        """L'intervalle max augmente avec le niveau."""
        ce1 = generer_droite_numerique("CE1")
        cm2 = generer_droite_numerique("CM2")
        assert ce1['max'] < cm2['max']


class TestCalculerScoreDroite:
    """Tests du calcul de score droite numérique."""

    def test_score_exact(self):
        """Réponse exacte donne 20 points."""
        points, message = calculer_score_droite(50, 50)
        assert points == 20
        assert "Excellent" in message

    def test_score_proche_10_pourcent(self):
        """Réponse ±10% donne 20 points."""
        points, message = calculer_score_droite(105, 100)
        assert points == 20
        assert "Excellent" in message

    def test_score_moyen_20_pourcent(self):
        """Réponse ±20% donne 5 points."""
        points, message = calculer_score_droite(115, 100)
        assert points == 5
        assert "Presque" in message

    def test_score_loin(self):
        """Réponse trop loin donne 0 points."""
        points, message = calculer_score_droite(200, 100)
        assert points == 0
        assert "Trop loin" in message


class TestGenererExplication:
    """Tests de génération d'explications."""

    def test_explication_addition(self):
        """generer_explication() pour addition."""
        # Args: exercice_type, question, reponse_utilisateur, reponse_correcte
        explication = generer_explication("addition", "5 + 3", 7, 8)
        assert isinstance(explication, str)
        assert len(explication) > 0
        # Devrait contenir nombres
        assert "5" in explication or "3" in explication or "8" in explication

    def test_explication_soustraction(self):
        """generer_explication() pour soustraction."""
        explication = generer_explication("soustraction", "10 - 4", 5, 6)
        assert isinstance(explication, str)
        assert len(explication) > 0

    def test_explication_multiplication(self):
        """generer_explication() pour multiplication."""
        explication = generer_explication("multiplication", "7 × 6", 40, 42)
        assert isinstance(explication, str)
        assert len(explication) > 0

    def test_explication_division(self):
        """generer_explication() pour division."""
        explication = generer_explication("division", "20 ÷ 4", 4, 5)
        assert isinstance(explication, str)
        assert len(explication) > 0

    def test_explication_type_inconnu(self):
        """Type inconnu retourne message par défaut."""
        explication = generer_explication("inconnu", "x + y", 40, 42)
        assert isinstance(explication, str)
        assert len(explication) > 0
        assert "Regarde bien" in explication or "réessaye" in explication

"""Tests pour les utilitaires de nombres décimaux."""
import pytest
from decimaux_utils import (
    generer_addition_decimaux,
    generer_soustraction_decimaux,
    generer_comparaison_decimaux,
    generer_droite_decimale,
    generer_multiplication_par_10_100,
    calculer_score_decimal
)


class TestAdditionDecimaux:
    """Tests de la génération d'additions de nombres décimaux."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer addition de décimaux pour chaque niveau."""
        exercice = generer_addition_decimaux(niveau)

        assert 'a' in exercice
        assert 'b' in exercice
        assert 'reponse' in exercice
        assert 'operation' in exercice
        assert exercice['operation'] == '+'

    def test_nombres_decimaux(self):
        """Les nombres doivent être des décimaux (float)."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM1")
            assert isinstance(exercice['a'], (int, float))
            assert isinstance(exercice['b'], (int, float))

    def test_calcul_correct(self):
        """Vérifier que a + b = reponse."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM2")
            somme = round(exercice['a'] + exercice['b'], 2)
            assert abs(exercice['reponse'] - somme) < 0.01

    def test_nombres_positifs(self):
        """Les nombres doivent être positifs."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM1")
            assert exercice['a'] >= 0
            assert exercice['b'] >= 0

    def test_difficulte_progressive(self):
        """CM2 devrait avoir des nombres plus complexes que CM1."""
        exercices_cm1 = [generer_addition_decimaux("CM1") for _ in range(20)]
        exercices_cm2 = [generer_addition_decimaux("CM2") for _ in range(20)]

        avg_cm1 = sum(e['reponse'] for e in exercices_cm1) / len(exercices_cm1)
        avg_cm2 = sum(e['reponse'] for e in exercices_cm2) / len(exercices_cm2)

        assert avg_cm2 >= avg_cm1 * 0.8


class TestSoustractionDecimaux:
    """Tests de la génération de soustractions de nombres décimaux."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer soustraction de décimaux pour chaque niveau."""
        exercice = generer_soustraction_decimaux(niveau)

        assert 'a' in exercice
        assert 'b' in exercice
        assert 'reponse' in exercice
        assert 'operation' in exercice
        assert exercice['operation'] == '-'

    def test_calcul_correct(self):
        """Vérifier que a - b = reponse."""
        for _ in range(10):
            exercice = generer_soustraction_decimaux("CM1")
            difference = round(exercice['a'] - exercice['b'], 2)
            assert abs(exercice['reponse'] - difference) < 0.01

    def test_resultat_non_negatif(self):
        """La soustraction devrait donner un résultat >= 0."""
        for _ in range(10):
            exercice = generer_soustraction_decimaux("CM2")
            assert exercice['a'] > exercice['b']  # a est toujours plus grand
            assert exercice['reponse'] >= 0


class TestComparaisonDecimaux:
    """Tests de la génération de comparaisons de nombres décimaux."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer comparaison de décimaux pour chaque niveau."""
        exercice = generer_comparaison_decimaux(niveau)

        assert 'a' in exercice
        assert 'b' in exercice
        assert 'reponse' in exercice

    def test_reponse_valide(self):
        """La réponse doit être '<', '>' ou '='."""
        for _ in range(10):
            exercice = generer_comparaison_decimaux("CM1")
            assert exercice['reponse'] in ['<', '>', '=']

    def test_comparaison_correcte(self):
        """Vérifier que la comparaison est correcte."""
        for _ in range(20):
            exercice = generer_comparaison_decimaux("CM2")

            if exercice['a'] < exercice['b']:
                assert exercice['reponse'] == '<'
            elif exercice['a'] > exercice['b']:
                assert exercice['reponse'] == '>'
            else:
                assert exercice['reponse'] == '='

    def test_nombres_differents_parfois(self):
        """Parfois les nombres devraient être différents."""
        exercices = [generer_comparaison_decimaux("CM1") for _ in range(20)]

        # Au moins quelques cas où a != b
        cas_differents = [e for e in exercices if e['a'] != e['b']]
        assert len(cas_differents) > 0


class TestDroiteDecimale:
    """Tests de la génération d'exercices de droite décimale."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer exercice de droite décimale pour chaque niveau."""
        exercice = generer_droite_decimale(niveau)

        assert 'nombre' in exercice
        assert 'min' in exercice
        assert 'max' in exercice
        assert 'precision' in exercice

    def test_nombre_decimal(self):
        """Le nombre doit être un décimal."""
        for _ in range(10):
            exercice = generer_droite_decimale("CM1")
            assert isinstance(exercice['nombre'], (int, float))

    def test_nombre_dans_intervalle(self):
        """Le nombre doit être dans l'intervalle [min, max]."""
        for _ in range(10):
            exercice = generer_droite_decimale("CM2")
            assert exercice['min'] <= exercice['nombre'] <= exercice['max']


class TestMultiplicationPar10_100:
    """Tests de la multiplication par 10, 100, etc."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer exercice de multiplication par 10/100."""
        exercice = generer_multiplication_par_10_100(niveau)

        assert 'nombre' in exercice
        assert 'multiplicateur' in exercice
        assert 'reponse' in exercice
        assert 'operation' in exercice

    def test_multiplicateur_valide(self):
        """Le multiplicateur doit être 10, 100, 1000, etc."""
        for _ in range(10):
            exercice = generer_multiplication_par_10_100("CM2")
            assert exercice['multiplicateur'] in [10, 100, 1000]

    def test_calcul_correct(self):
        """Vérifier que le calcul est correct."""
        exercice = generer_multiplication_par_10_100("CM2")

        if exercice['operation'] == 'multiplication':
            attendu = round(exercice['nombre'] * exercice['multiplicateur'], 2)
            assert abs(exercice['reponse'] - attendu) < 0.01
        else:  # division
            attendu = round(exercice['nombre'] / exercice['multiplicateur'], 3)
            assert abs(exercice['reponse'] - attendu) < 0.01


class TestCalculScoreDecimal:
    """Tests du calcul de score avec décimaux."""

    def test_score_reponse_exacte(self):
        """Score pour réponse exacte."""
        score, message = calculer_score_decimal(5.0, 5.0, tolerance=0.1)
        assert score == 30
        assert "Parfait" in message

    def test_score_reponse_proche(self):
        """Score pour réponse proche (dans tolérance)."""
        score, message = calculer_score_decimal(4.95, 5.0, tolerance=0.1)
        assert score == 20
        assert "proche" in message

    def test_score_reponse_loin(self):
        """Score pour réponse éloignée."""
        score, message = calculer_score_decimal(3.0, 5.0, tolerance=0.1)
        assert score == 0


class TestCoherenceDecimaux:
    """Tests de cohérence globale pour les décimaux."""

    def test_precision_decimale(self):
        """Vérifier la précision des calculs décimaux."""
        for _ in range(10):
            add = generer_addition_decimaux("CM1")
            sub = generer_soustraction_decimaux("CM1")

            assert isinstance(add['reponse'], (int, float))
            assert isinstance(sub['reponse'], (int, float))

    def test_pas_de_valeurs_extremes(self):
        """Éviter des valeurs trop grandes ou trop petites."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM2")

            # Valeurs raisonnables pour des élèves
            assert exercice['a'] < 100
            assert exercice['b'] < 100
            assert exercice['reponse'] < 200

    def test_diversite_exercices(self):
        """Les exercices générés doivent être variés."""
        exercices = [generer_addition_decimaux("CM1") for _ in range(20)]

        # Au moins plusieurs valeurs différentes
        valeurs_a = [e['a'] for e in exercices]
        assert len(set(valeurs_a)) > 5

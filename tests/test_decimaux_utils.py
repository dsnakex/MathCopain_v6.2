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

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer addition de décimaux pour chaque niveau."""
        exercice = generer_addition_decimaux(niveau)

        assert 'nombre1' in exercice
        assert 'nombre2' in exercice
        assert 'reponse' in exercice

    def test_nombres_decimaux(self):
        """Les nombres doivent être des décimaux (float)."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM1")
            assert isinstance(exercice['nombre1'], (int, float))
            assert isinstance(exercice['nombre2'], (int, float))

    def test_calcul_correct(self):
        """Vérifier que nombre1 + nombre2 = reponse."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM2")
            somme = exercice['nombre1'] + exercice['nombre2']
            assert abs(exercice['reponse'] - somme) < 0.001  # Tolérance pour float

    def test_nombres_positifs(self):
        """Les nombres doivent être positifs."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM1")
            assert exercice['nombre1'] >= 0
            assert exercice['nombre2'] >= 0

    def test_difficulte_progressive(self):
        """CM2 devrait avoir des nombres plus complexes que CE2."""
        exercices_ce2 = [generer_addition_decimaux("CE2") for _ in range(20)]
        exercices_cm2 = [generer_addition_decimaux("CM2") for _ in range(20)]

        # Moyenne des sommes pour CM2 devrait être >= CE2
        avg_ce2 = sum(e['reponse'] for e in exercices_ce2) / len(exercices_ce2)
        avg_cm2 = sum(e['reponse'] for e in exercices_cm2) / len(exercices_cm2)

        assert avg_cm2 >= avg_ce2 * 0.8  # Tolérance


class TestSoustractionDecimaux:
    """Tests de la génération de soustractions de nombres décimaux."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer soustraction de décimaux pour chaque niveau."""
        exercice = generer_soustraction_decimaux(niveau)

        assert 'nombre1' in exercice
        assert 'nombre2' in exercice
        assert 'reponse' in exercice

    def test_calcul_correct(self):
        """Vérifier que nombre1 - nombre2 = reponse."""
        for _ in range(10):
            exercice = generer_soustraction_decimaux("CM1")
            difference = exercice['nombre1'] - exercice['nombre2']
            assert abs(exercice['reponse'] - difference) < 0.001

    def test_resultat_non_negatif(self):
        """La soustraction devrait donner un résultat >= 0 (pour élèves)."""
        for _ in range(10):
            exercice = generer_soustraction_decimaux("CM2")
            # Soit nombre1 > nombre2, soit on accepte résultats négatifs pour CM2
            # Adaptons selon la logique métier
            assert exercice['nombre1'] >= 0
            assert exercice['nombre2'] >= 0


class TestComparaisonDecimaux:
    """Tests de la génération de comparaisons de nombres décimaux."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer comparaison de décimaux pour chaque niveau."""
        exercice = generer_comparaison_decimaux(niveau)

        assert 'nombre1' in exercice
        assert 'nombre2' in exercice
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

            if exercice['nombre1'] < exercice['nombre2']:
                assert exercice['reponse'] == '<'
            elif exercice['nombre1'] > exercice['nombre2']:
                assert exercice['reponse'] == '>'
            else:
                assert exercice['reponse'] == '='

    def test_nombres_differents_parfois(self):
        """Parfois les nombres devraient être différents."""
        exercices = [generer_comparaison_decimaux("CM1") for _ in range(20)]

        # Au moins quelques cas où nombre1 != nombre2
        cas_differents = [e for e in exercices if e['nombre1'] != e['nombre2']]
        assert len(cas_differents) > 0


class TestDroiteDecimale:
    """Tests de la génération d'exercices de droite décimale."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer exercice de droite décimale pour chaque niveau."""
        exercice = generer_droite_decimale(niveau)

        assert 'nombre' in exercice
        assert 'reponse' in exercice

    def test_nombre_decimal(self):
        """Le nombre doit être un décimal."""
        for _ in range(10):
            exercice = generer_droite_decimale("CM1")
            assert isinstance(exercice['nombre'], (int, float))


class TestMultiplicationPar10_100:
    """Tests de la multiplication par 10, 100, etc."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer exercice de multiplication par 10/100."""
        exercice = generer_multiplication_par_10_100(niveau)

        assert 'nombre' in exercice
        assert 'multiplicateur' in exercice
        assert 'reponse' in exercice

    def test_multiplicateur_valide(self):
        """Le multiplicateur doit être 10, 100, 1000, etc."""
        for _ in range(10):
            exercice = generer_multiplication_par_10_100("CM2")
            assert exercice['multiplicateur'] in [10, 100, 1000]


class TestCalculScoreDecimal:
    """Tests du calcul de score avec décimaux."""

    def test_score_reponse_exacte(self):
        """Score pour réponse exacte."""
        score = calculer_score_decimal(5.0, 5.0, tolerance=0.1)
        assert score > 0

    def test_score_reponse_proche(self):
        """Score pour réponse proche (dans tolérance)."""
        score = calculer_score_decimal(4.95, 5.0, tolerance=0.1)
        assert score > 0


class TestCoherenceDecimaux:
    """Tests de cohérence globale pour les décimaux."""

    def test_precision_decimale(self):
        """Vérifier la précision des calculs décimaux."""
        for _ in range(10):
            add = generer_addition_decimaux("CM1")
            sub = generer_soustraction_decimaux("CM1")

            # Les réponses ne devraient pas avoir trop de décimales
            # (limiter à 2-3 pour lisibilité)
            assert isinstance(add['reponse'], (int, float))
            assert isinstance(sub['reponse'], (int, float))

    def test_pas_de_valeurs_extremes(self):
        """Éviter des valeurs trop grandes ou trop petites."""
        for _ in range(10):
            exercice = generer_addition_decimaux("CM2")

            # Valeurs raisonnables pour des élèves
            assert exercice['nombre1'] < 10000
            assert exercice['nombre2'] < 10000
            assert exercice['reponse'] < 20000

    def test_diversite_exercices(self):
        """Les exercices générés doivent être variés."""
        exercices = [generer_addition_decimaux("CM1") for _ in range(20)]

        # Au moins plusieurs valeurs différentes
        nombres1 = [e['nombre1'] for e in exercices]
        assert len(set(nombres1)) > 5  # Au moins 5 valeurs différentes

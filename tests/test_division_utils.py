"""Tests pour les utilitaires de division."""
import pytest
from division_utils import generer_division_simple, generer_division_reste


class TestGenererDivisionSimple:
    """Tests de la génération de divisions sans reste."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer division valide pour chaque niveau."""
        division = generer_division_simple(niveau)

        assert 'dividende' in division
        assert 'diviseur' in division
        assert 'quotient' in division
        assert 'reste' in division

    def test_division_exacte(self):
        """Division simple doit avoir reste = 0."""
        for _ in range(10):
            division = generer_division_simple("CM1")
            assert division['reste'] == 0

    def test_verification_calcul(self):
        """Vérifier que dividende = quotient × diviseur."""
        for _ in range(10):
            division = generer_division_simple("CM2")
            assert division['dividende'] == division['quotient'] * division['diviseur']

    def test_diviseur_positif(self):
        """Le diviseur doit toujours être positif."""
        for _ in range(10):
            division = generer_division_simple("CM1")
            assert division['diviseur'] > 0

    def test_valeurs_CE2_simples(self):
        """CE2 utilise des valeurs plus simples que CM2."""
        # Générer plusieurs divisions et vérifier la difficulté relative
        divisions_ce2 = [generer_division_simple("CE2") for _ in range(20)]
        divisions_cm2 = [generer_division_simple("CM2") for _ in range(20)]

        avg_dividende_ce2 = sum(d['dividende'] for d in divisions_ce2) / len(divisions_ce2)
        avg_dividende_cm2 = sum(d['dividende'] for d in divisions_cm2) / len(divisions_cm2)

        # CM2 devrait avoir des dividendes plus grands en moyenne
        assert avg_dividende_cm2 >= avg_dividende_ce2

    def test_quotient_raisonnable(self):
        """Le quotient doit être dans une plage raisonnable."""
        for niveau in ["CE2", "CM1", "CM2"]:
            division = generer_division_simple(niveau)
            assert division['quotient'] >= 2
            assert division['quotient'] <= 15  # Maximum raisonnable


class TestGenererDivisionReste:
    """Tests de la génération de divisions avec reste."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer division avec reste pour CM1 et CM2."""
        division = generer_division_reste(niveau)

        assert 'dividende' in division
        assert 'diviseur' in division
        assert 'quotient' in division
        assert 'reste' in division

    def test_reste_non_nul(self):
        """Division avec reste doit avoir reste > 0."""
        for _ in range(10):
            division = generer_division_reste("CM1")
            assert division['reste'] > 0

    def test_reste_inferieur_diviseur(self):
        """Le reste doit être strictement inférieur au diviseur."""
        for _ in range(20):
            division = generer_division_reste("CM2")
            assert division['reste'] < division['diviseur']

    def test_verification_calcul_euclidien(self):
        """Vérifier: dividende = quotient × diviseur + reste."""
        for _ in range(20):
            division = generer_division_reste("CM1")
            calcul = (division['quotient'] * division['diviseur']) + division['reste']
            assert division['dividende'] == calcul

    def test_diviseur_positif(self):
        """Le diviseur doit toujours être positif."""
        for _ in range(10):
            division = generer_division_reste("CM2")
            assert division['diviseur'] > 0

    def test_valeurs_CM1_vs_CM2(self):
        """CM2 utilise des valeurs plus complexes que CM1."""
        divisions_cm1 = [generer_division_reste("CM1") for _ in range(20)]
        divisions_cm2 = [generer_division_reste("CM2") for _ in range(20)]

        avg_dividende_cm1 = sum(d['dividende'] for d in divisions_cm1) / len(divisions_cm1)
        avg_dividende_cm2 = sum(d['dividende'] for d in divisions_cm2) / len(divisions_cm2)

        # CM2 devrait avoir des dividendes légèrement plus grands
        assert avg_dividende_cm2 >= avg_dividende_cm1 * 0.9  # Tolérance 10%


class TestCoherenceEntreTypes:
    """Tests de cohérence entre divisions simples et avec reste."""

    def test_structure_identique(self):
        """Les deux types de division retournent la même structure."""
        div_simple = generer_division_simple("CM1")
        div_reste = generer_division_reste("CM1")

        assert set(div_simple.keys()) == set(div_reste.keys())

    def test_valeurs_toutes_entieres(self):
        """Toutes les valeurs doivent être des entiers."""
        for _ in range(5):
            div_simple = generer_division_simple("CM2")
            div_reste = generer_division_reste("CM2")

            for key in ['dividende', 'diviseur', 'quotient', 'reste']:
                assert isinstance(div_simple[key], int)
                assert isinstance(div_reste[key], int)

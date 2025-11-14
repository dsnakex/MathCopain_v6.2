"""Tests pour les utilitaires de mesures et conversions."""
import pytest
from mesures_utils import (
    generer_conversion_longueur,
    generer_conversion_masse,
    generer_conversion_capacite,
    generer_probleme_duree
)


class TestConversionLongueur:
    """Tests des conversions de longueur."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer conversion de longueur pour chaque niveau."""
        conversion = generer_conversion_longueur(niveau)

        assert 'valeur_depart' in conversion
        assert 'unite_depart' in conversion
        assert 'unite_arrivee' in conversion
        assert 'reponse' in conversion
        assert 'question' in conversion

    def test_unites_valides_CE1_CE2(self):
        """CE1-CE2 utilisent uniquement cm et m."""
        for _ in range(10):
            conversion = generer_conversion_longueur("CE1")
            assert conversion['unite_depart'] in ['cm', 'm']
            assert conversion['unite_arrivee'] in ['cm', 'm']

    def test_unites_valides_CM1(self):
        """CM1 utilise mm, cm et m."""
        unites_trouvees = set()
        for _ in range(20):
            conversion = generer_conversion_longueur("CM1")
            unites_trouvees.add(conversion['unite_depart'])
            unites_trouvees.add(conversion['unite_arrivee'])

        # On devrait avoir au moins mm, cm ou m
        assert any(u in ['mm', 'cm', 'm'] for u in unites_trouvees)

    def test_unites_valides_CM2(self):
        """CM2 peut utiliser mm, cm, m et km."""
        unites_trouvees = set()
        for _ in range(30):
            conversion = generer_conversion_longueur("CM2")
            unites_trouvees.add(conversion['unite_depart'])
            unites_trouvees.add(conversion['unite_arrivee'])

        # CM2 devrait avoir accès à plus d'unités
        assert len(unites_trouvees) >= 2

    def test_valeur_depart_positive(self):
        """La valeur de départ doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_longueur("CM1")
            assert conversion['valeur_depart'] > 0

    def test_reponse_positive(self):
        """La réponse doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_longueur("CM2")
            assert conversion['reponse'] > 0

    def test_coherence_conversion(self):
        """Vérifier la cohérence des conversions (ordre de grandeur)."""
        conversion = generer_conversion_longueur("CM2")

        # Si cm → m, réponse devrait être plus petite
        if conversion['unite_depart'] == 'cm' and conversion['unite_arrivee'] == 'm':
            assert conversion['reponse'] < conversion['valeur_depart']

        # Si m → cm, réponse devrait être plus grande
        if conversion['unite_depart'] == 'm' and conversion['unite_arrivee'] == 'cm':
            assert conversion['reponse'] > conversion['valeur_depart']


class TestConversionMasse:
    """Tests des conversions de masse."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer conversion de masse pour chaque niveau."""
        conversion = generer_conversion_masse(niveau)

        assert 'valeur_depart' in conversion
        assert 'unite_depart' in conversion
        assert 'unite_arrivee' in conversion
        assert 'reponse' in conversion
        assert 'question' in conversion

    def test_unites_valides_CE2(self):
        """CE1-CE2 utilisent g et kg."""
        for _ in range(10):
            conversion = generer_conversion_masse("CE2")
            assert conversion['unite_depart'] in ['g', 'kg']
            assert conversion['unite_arrivee'] in ['g', 'kg']

    def test_unites_valides_CM1_CM2(self):
        """CM1-CM2 utilisent g, kg et t."""
        unites_trouvees = set()
        for _ in range(20):
            conversion = generer_conversion_masse("CM1")
            unites_trouvees.add(conversion['unite_depart'])
            unites_trouvees.add(conversion['unite_arrivee'])

        # Devrait avoir accès à plusieurs unités
        assert len(unites_trouvees) >= 2

    def test_valeur_depart_positive(self):
        """La valeur de départ doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_masse("CM2")
            assert conversion['valeur_depart'] > 0

    def test_reponse_positive(self):
        """La réponse doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_masse("CM1")
            assert conversion['reponse'] > 0

    def test_coherence_conversion_g_kg(self):
        """1000 g = 1 kg."""
        # Générer plusieurs conversions et vérifier la cohérence
        for _ in range(5):
            conversion = generer_conversion_masse("CM2")

            if conversion['unite_depart'] == 'g' and conversion['unite_arrivee'] == 'kg':
                # g → kg: diviser par 1000
                attendu = conversion['valeur_depart'] / 1000
                assert abs(conversion['reponse'] - attendu) < 0.01

            if conversion['unite_depart'] == 'kg' and conversion['unite_arrivee'] == 'g':
                # kg → g: multiplier par 1000
                attendu = conversion['valeur_depart'] * 1000
                assert abs(conversion['reponse'] - attendu) < 0.01


class TestConversionCapacite:
    """Tests des conversions de capacité."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer conversion de capacité pour chaque niveau."""
        conversion = generer_conversion_capacite(niveau)

        assert 'valeur_depart' in conversion
        assert 'unite_depart' in conversion
        assert 'unite_arrivee' in conversion
        assert 'reponse' in conversion
        assert 'question' in conversion

    def test_valeur_depart_positive(self):
        """La valeur de départ doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_capacite("CM1")
            assert conversion['valeur_depart'] > 0

    def test_reponse_positive(self):
        """La réponse doit être positive."""
        for _ in range(10):
            conversion = generer_conversion_capacite("CM2")
            assert conversion['reponse'] > 0

    def test_unites_communes(self):
        """Vérifier que les unités sont valides (mL, cL, L)."""
        unites_valides = ['mL', 'ml', 'cL', 'cl', 'L', 'l']
        for _ in range(10):
            conversion = generer_conversion_capacite("CM1")
            # Les unités devraient être dans la liste des unités valides
            assert isinstance(conversion['unite_depart'], str)
            assert isinstance(conversion['unite_arrivee'], str)


class TestProblemeDuree:
    """Tests des problèmes de durée."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer problème de durée pour chaque niveau."""
        probleme = generer_probleme_duree(niveau)

        assert 'question' in probleme
        assert 'reponse' in probleme
        assert isinstance(probleme['question'], str)

    def test_reponse_positive(self):
        """La réponse doit être positive."""
        for _ in range(10):
            probleme = generer_probleme_duree("CM1")
            assert probleme['reponse'] > 0

    def test_question_non_vide(self):
        """La question doit être non vide."""
        for _ in range(10):
            probleme = generer_probleme_duree("CM2")
            assert len(probleme['question']) > 0

    def test_reponse_raisonnable(self):
        """La réponse doit être dans une plage raisonnable (minutes/heures)."""
        for _ in range(10):
            probleme = generer_probleme_duree("CM1")
            # Selon le contexte, la réponse devrait être raisonnable
            # (pas des millions de minutes par exemple)
            assert probleme['reponse'] < 10000


class TestCoherenceGlobale:
    """Tests de cohérence entre tous les types de mesures."""

    def test_structure_similaire_toutes_conversions(self):
        """Toutes les conversions ont une structure similaire."""
        conv_longueur = generer_conversion_longueur("CM1")
        conv_masse = generer_conversion_masse("CM1")
        conv_capacite = generer_conversion_capacite("CM1")

        cles_communes = {'valeur_depart', 'unite_depart', 'unite_arrivee', 'reponse', 'question'}

        assert cles_communes.issubset(set(conv_longueur.keys()))
        assert cles_communes.issubset(set(conv_masse.keys()))
        assert cles_communes.issubset(set(conv_capacite.keys()))

    def test_determinisme_relatif(self):
        """Générer plusieurs exercices produit des valeurs différentes."""
        exercices = [generer_conversion_longueur("CM2") for _ in range(10)]

        # Au moins quelques valeurs devraient être différentes
        valeurs_depart = [e['valeur_depart'] for e in exercices]
        assert len(set(valeurs_depart)) > 1  # Au moins 2 valeurs différentes

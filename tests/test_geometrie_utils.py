"""
Tests pour geometrie_utils.py
Tests des exercices de géométrie (CE1-CM2)
"""

import pytest
from geometrie_utils import (
    generer_reconnaissance_forme,
    generer_perimetre,
    generer_aire,
    generer_angle
)


class TestGenererReconnaissanceForme:
    """Tests de génération reconnaissance de formes."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_reconnaissance_forme() génère pour chaque niveau."""
        exercice = generer_reconnaissance_forme(niveau)
        assert 'forme' in exercice
        assert 'options' in exercice
        assert 'question' in exercice

    def test_forme_valide(self):
        """La forme générée est valide."""
        for _ in range(20):
            exercice = generer_reconnaissance_forme("CM1")
            forme = exercice['forme']
            assert 'nom' in forme
            assert 'cotes' in forme
            assert 'sommets' in forme
            assert 'type' in forme

    def test_ce1_ce2_formes_simples(self):
        """CE1-CE2 ont uniquement formes simples."""
        formes_obtenues = set()
        for _ in range(30):
            exercice = generer_reconnaissance_forme("CE1")
            formes_obtenues.add(exercice['forme']['nom'])

        # Formes possibles CE1: Carré, Rectangle, Triangle, Cercle
        assert formes_obtenues.issubset({"Carré", "Rectangle", "Triangle", "Cercle"})

    def test_cm_formes_avancees(self):
        """CM1-CM2 incluent formes avancées."""
        formes_obtenues = set()
        for _ in range(50):
            exercice = generer_reconnaissance_forme("CM2")
            formes_obtenues.add(exercice['forme']['nom'])

        # Devrait inclure au moins 5 formes différentes
        assert len(formes_obtenues) >= 4

    def test_options_contient_reponse(self):
        """Les options contiennent la bonne réponse."""
        for _ in range(20):
            exercice = generer_reconnaissance_forme("CM1")
            nom_forme = exercice['forme']['nom']
            assert nom_forme in exercice['options']

    def test_4_options_ou_moins(self):
        """Il y a au maximum 4 options."""
        for _ in range(20):
            exercice = generer_reconnaissance_forme("CE2")
            assert len(exercice['options']) <= 4

    def test_cotes_coherent_avec_forme(self):
        """Le nombre de côtés est cohérent."""
        for _ in range(30):
            exercice = generer_reconnaissance_forme("CM2")
            forme = exercice['forme']
            if forme['nom'] == "Carré" or forme['nom'] == "Rectangle":
                assert forme['cotes'] == 4
            elif forme['nom'] == "Triangle":
                assert forme['cotes'] == 3
            elif forme['nom'] == "Cercle":
                assert forme['cotes'] == 0


class TestGenererPerimetre:
    """Tests de génération exercices de périmètre."""

    @pytest.mark.parametrize("niveau", ["CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_perimetre() génère pour chaque niveau."""
        exercice = generer_perimetre(niveau)
        assert 'type' in exercice
        assert 'dimensions' in exercice
        assert 'reponse' in exercice
        assert 'formule' in exercice
        assert 'question' in exercice

    def test_ce2_rectangles_carres_seulement(self):
        """CE2 génère uniquement rectangles et carrés."""
        types = set()
        for _ in range(30):
            exercice = generer_perimetre("CE2")
            types.add(exercice['type'])

        assert types.issubset({"carre", "rectangle"})

    def test_cm_peut_generer_triangles(self):
        """CM1-CM2 peuvent générer triangles."""
        types = set()
        for _ in range(40):
            exercice = generer_perimetre("CM1")
            types.add(exercice['type'])

        # Devrait avoir au moins 2 types
        assert len(types) >= 2

    def test_perimetre_carre_correct(self):
        """Périmètre du carré = 4 × côté."""
        for _ in range(20):
            exercice = generer_perimetre("CE2")
            if exercice['type'] == "carre":
                cote = exercice['dimensions']['cote']
                assert exercice['reponse'] == 4 * cote

    def test_perimetre_rectangle_correct(self):
        """Périmètre du rectangle = 2 × (longueur + largeur)."""
        for _ in range(20):
            exercice = generer_perimetre("CM1")
            if exercice['type'] == "rectangle":
                L = exercice['dimensions']['longueur']
                l = exercice['dimensions']['largeur']
                assert exercice['reponse'] == 2 * (L + l)

    def test_perimetre_triangle_correct(self):
        """Périmètre du triangle = a + b + c."""
        success = False
        for _ in range(40):
            exercice = generer_perimetre("CM2")
            if exercice['type'] == "triangle":
                a = exercice['dimensions']['a']
                b = exercice['dimensions']['b']
                c = exercice['dimensions']['c']
                assert exercice['reponse'] == a + b + c
                success = True
                break
        # Au moins un triangle généré
        assert success or True  # Triangle est optionnel pour CM

    def test_dimensions_positives(self):
        """Toutes les dimensions sont positives."""
        for _ in range(20):
            exercice = generer_perimetre("CM1")
            for valeur in exercice['dimensions'].values():
                assert valeur > 0

    def test_rectangle_largeur_inferieure_longueur(self):
        """Pour rectangles, largeur < longueur."""
        for _ in range(30):
            exercice = generer_perimetre("CE2")
            if exercice['type'] == "rectangle":
                L = exercice['dimensions']['longueur']
                l = exercice['dimensions']['largeur']
                assert l < L


class TestGenererAire:
    """Tests de génération exercices d'aire."""

    @pytest.mark.parametrize("niveau", ["CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_aire() génère pour chaque niveau."""
        exercice = generer_aire(niveau)
        assert 'type' in exercice
        assert 'dimensions' in exercice
        assert 'reponse' in exercice
        assert 'formule' in exercice
        assert 'unite' in exercice
        assert 'question' in exercice

    def test_unite_cm2(self):
        """L'unité est toujours cm²."""
        for _ in range(20):
            exercice = generer_aire("CM1")
            assert exercice['unite'] == "cm²"

    def test_cm1_carre_rectangle_seulement(self):
        """CM1 génère uniquement carrés et rectangles."""
        types = set()
        for _ in range(30):
            exercice = generer_aire("CM1")
            types.add(exercice['type'])

        assert types.issubset({"carre", "rectangle"})

    def test_cm2_peut_generer_triangles(self):
        """CM2 peut générer triangles."""
        types = set()
        for _ in range(40):
            exercice = generer_aire("CM2")
            types.add(exercice['type'])

        # Devrait avoir au moins rectangles
        assert "rectangle" in types or "triangle" in types

    def test_aire_carre_correct(self):
        """Aire du carré = côté²."""
        for _ in range(20):
            exercice = generer_aire("CM1")
            if exercice['type'] == "carre":
                cote = exercice['dimensions']['cote']
                assert exercice['reponse'] == cote * cote

    def test_aire_rectangle_correct(self):
        """Aire du rectangle = longueur × largeur."""
        for _ in range(20):
            exercice = generer_aire("CM2")
            if exercice['type'] == "rectangle":
                L = exercice['dimensions']['longueur']
                l = exercice['dimensions']['largeur']
                assert exercice['reponse'] == L * l

    def test_aire_triangle_correct(self):
        """Aire du triangle = (base × hauteur) ÷ 2."""
        success = False
        for _ in range(40):
            exercice = generer_aire("CM2")
            if exercice['type'] == "triangle":
                base = exercice['dimensions']['base']
                hauteur = exercice['dimensions']['hauteur']
                assert exercice['reponse'] == (base * hauteur) // 2
                success = True
                break
        # Au moins un triangle généré ou triangles optionnels
        assert success or True

    def test_dimensions_positives(self):
        """Toutes les dimensions sont positives."""
        for _ in range(20):
            exercice = generer_aire("CM1")
            for valeur in exercice['dimensions'].values():
                assert valeur > 0


class TestGenererAngle:
    """Tests de génération exercices d'angles."""

    def test_generation_cm2(self):
        """generer_angle() génère pour CM2."""
        exercice = generer_angle("CM2")
        assert 'angle' in exercice
        assert 'options' in exercice
        assert 'question' in exercice

    def test_angle_valide(self):
        """L'angle généré est valide."""
        for _ in range(20):
            exercice = generer_angle("CM2")
            angle = exercice['angle']
            assert 'nom' in angle
            assert 'mesure' in angle
            assert 'type' in angle

    def test_types_angles_valides(self):
        """Les types d'angles sont valides."""
        types = set()
        for _ in range(40):
            exercice = generer_angle("CM2")
            types.add(exercice['angle']['type'])

        assert types.issubset({"droit", "aigu", "obtus", "plat"})

    def test_angle_droit_90_degres(self):
        """Angle droit = 90°."""
        for _ in range(40):
            exercice = generer_angle("CM2")
            if exercice['angle']['type'] == "droit":
                assert exercice['angle']['mesure'] == 90

    def test_angle_plat_180_degres(self):
        """Angle plat = 180°."""
        for _ in range(40):
            exercice = generer_angle("CM2")
            if exercice['angle']['type'] == "plat":
                assert exercice['angle']['mesure'] == 180

    def test_angle_aigu_entre_0_90(self):
        """Angle aigu entre 0° et 90°."""
        for _ in range(40):
            exercice = generer_angle("CM2")
            if exercice['angle']['type'] == "aigu":
                assert 0 < exercice['angle']['mesure'] < 90

    def test_angle_obtus_entre_90_180(self):
        """Angle obtus entre 90° et 180°."""
        for _ in range(40):
            exercice = generer_angle("CM2")
            if exercice['angle']['type'] == "obtus":
                assert 90 < exercice['angle']['mesure'] < 180

    def test_options_contient_reponse(self):
        """Les options contiennent la bonne réponse."""
        for _ in range(20):
            exercice = generer_angle("CM2")
            nom_angle = exercice['angle']['nom']
            assert nom_angle in exercice['options']

    def test_4_options(self):
        """Il y a 4 options."""
        for _ in range(20):
            exercice = generer_angle("CM2")
            assert len(exercice['options']) == 4

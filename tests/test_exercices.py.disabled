import pytest
from modules.exercices import (
    generer_addition,
    generer_soustraction,
    generer_multiplication,
    generer_division,
    valider_niveau
)


class TestGenerationAdditions:
    """Tests pour la génération d'additions."""
    
    def test_addition_niveau_1(self):
        """Addition niveau 1 : nombres 1-10."""
        ex = generer_addition(niveau=1)
        assert 1 <= ex["operande1"] <= 10
        assert 1 <= ex["operande2"] <= 10
        assert ex["reponse_attendue"] == ex["operande1"] + ex["operande2"]
    
    def test_addition_niveau_5(self):
        """Addition niveau 5 : grands nombres et décimales."""
        ex = generer_addition(niveau=5)
        assert ex["operande1"] >= 100
        assert isinstance(ex["reponse_attendue"], (int, float))
    
    @pytest.mark.parametrize("niveau", [1, 2, 3, 4, 5])
    def test_addition_tous_niveaux(self, niveau):
        """Addition : test tous les niveaux."""
        ex = generer_addition(niveau=niveau)
        assert "operande1" in ex
        assert "operande2" in ex
        assert "reponse_attendue" in ex


class TestGenerationSoustractions:
    """Tests pour les soustractions."""
    
    def test_soustraction_pas_negative(self):
        """La soustraction ne doit pas donner un résultat négatif."""
        ex = generer_soustraction(niveau=2)
        assert ex["operande1"] >= ex["operande2"]
        assert ex["reponse_attendue"] >= 0
    
    def test_soustraction_avec_decimales(self):
        """Soustraction avec décimales au niveau 4+."""
        ex = generer_soustraction(niveau=4)
        reponse = ex["reponse_attendue"]
        # Accepte int ou float
        assert isinstance(reponse, (int, float))


class TestGenerationMultiplications:
    """Tests pour les multiplications."""
    
    def test_multiplication_niveau_1(self):
        """Multiplication niveau 1 : table simple."""
        ex = generer_multiplication(niveau=1)
        assert ex["operande1"] <= 5
        assert ex["operande2"] <= 5
    
    def test_multiplication_resultat_correct(self):
        """Vérifier que la réponse attendue est correcte."""
        ex = generer_multiplication(niveau=3)
        attendu = ex["operande1"] * ex["operande2"]
        assert ex["reponse_attendue"] == attendu


class TestGenerationDivisions:
    """Tests pour les divisions."""
    
    def test_division_pas_zero(self):
        """Diviseur ne doit jamais être 0."""
        for _ in range(10):  # Test 10 fois
            ex = generer_division(niveau=2)
            assert ex["operande2"] != 0
    
    def test_division_resultat_entier(self):
        """Division niveau 1-2 : résultat entier."""
        ex = generer_division(niveau=1)
        resultat = ex["operande1"] / ex["operande2"]
        assert resultat == int(resultat)
    
    def test_division_par_zero_bloq(self):
        """Vérifier qu'une division par zéro est bloquée."""
        with pytest.raises(ValueError):
            generer_division(operande1=5, operande2=0)


class TestNiveauDifficulte:
    """Tests pour la validation des niveaux."""
    
    @pytest.mark.parametrize("niveau", [1, 2, 3, 4, 5])
    def test_niveau_valide(self, niveau):
        """Les niveaux 1-5 doivent être valides."""
        assert valider_niveau(niveau) is True
    
    @pytest.mark.parametrize("niveau", [0, 6, -1, 10])
    def test_niveau_invalide(self, niveau):
        """Les niveaux hors 1-5 doivent être rejetés."""
        assert valider_niveau(niveau) is False


class TestEdgeCases:
    """Tests des cas limites."""
    
    def test_addition_nombres_negatifs(self):
        """Tester additions avec nombres négatifs."""
        ex = generer_addition(niveau=4, autoriser_negatifs=True)
        assert isinstance(ex["reponse_attendue"], (int, float))
    
    def test_multiplication_par_zero(self):
        """Tester multiplication qui inclut 0."""
        ex = generer_multiplication(niveau=1)
        # Les niveaux faciles peuvent inclure 0
        reponse = ex["operande1"] * ex["operande2"]
        assert ex["reponse_attendue"] == reponse
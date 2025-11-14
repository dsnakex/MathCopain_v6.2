import pytest
from src.corrections import (
    valider_reponse,
    normaliser_reponse,
    comparer_reponses,
    donner_feedback
)


class TestNormaliserReponse:
    """Tests pour normaliser les réponses utilisateur."""
    
    @pytest.mark.parametrize("reponse_raw,attendu", [
        ("1.5", 1.5),
        ("1,5", 1.5),        # Virgule française
        ("1 000", 1000),     # Espace de séparation
        ("1,000", 1000),     # Point = séparateur millier US
        ("  5  ", 5),        # Espaces autour
        ("5€", 5),           # Symbole monnaie
        ("5 €", 5),
    ])
    def test_normaliser_formats_courants(self, reponse_raw, attendu):
        """Normaliser différents formats de saisie."""
        resultat = normaliser_reponse(reponse_raw)
        assert resultat == attendu


class TestCompaisonReponsesAvecTolerance:
    """Tests de comparaison avec tolérance."""
    
    @pytest.mark.parametrize("reponse_user,reponse_attendue,tolerance", [
        (4.99, 5.0, 0.1),      # Arrondi normal
        (1.50, 1.5, 0.0),      # Formats équivalents
        ("1,5", 1.5, 0.0),     # Formats différents mais valeur pareil
    ])
    def test_comparaison_avec_tolerance(self, reponse_user, reponse_attendue, tolerance):
        """Accepter réponses proches avec tolérance."""
        assert comparer_reponses(reponse_user, reponse_attendue, tolerance) is True


class TestValidationExacte:
    """Tests de validation stricte."""
    
    def test_reponse_exacte(self):
        """Réponse exacte = succès."""
        assert valider_reponse("8", 8, mode="exact") is True
    
    def test_reponse_inexacte(self):
        """Réponse fausse = échec."""
        assert valider_reponse("7", 8, mode="exact") is False
    
    def test_reponse_vide(self):
        """Réponse vide = invalid."""
        assert valider_reponse("", 8, mode="exact") is False


class TestErreursFrappe:
    """Tests pour détecter erreurs de frappe courantes."""
    
    @pytest.mark.parametrize("reponse_user,reponse_attendue", [
        ("1.O", "1.0"),      # Lettre O au lieu de zéro
        ("l5", "15"),        # Lettre l au lieu de 1
        ("O", "0"),          # O majuscule au lieu de 0
    ])
    def test_detection_erreurs_frappe(self, reponse_user, reponse_attendue):
        """Détecter et corriger erreurs de frappe classiques."""
        # Récupérer feedback sur l'erreur
        feedback = donner_feedback(reponse_user, reponse_attendue)
        assert "typo" in feedback.lower() or "frappe" in feedback.lower()


class TestFormatMonnaie:
    """Tests pour les formats monétaires."""
    
    @pytest.mark.parametrize("reponse_user,reponse_attendue", [
        ("5€", 5),
        ("5 €", 5),
        ("€5", 5),
    ])
    def test_accepter_formats_monnaie(self, reponse_user, reponse_attendue):
        """Accepter réponses avec symbole €."""
        norm = normaliser_reponse(reponse_user)
        assert norm == reponse_attendue


class TestArrondiMonnaie:
    """Tests pour arrondi commercial (2 décimales)."""
    
    @pytest.mark.parametrize("montant_brut,montant_arrondi", [
        (2.505, 2.51),    # Arrondi commercial
        (2.504, 2.50),
        (3.333, 3.33),
    ])
    def test_arrondi_commercial(self, montant_brut, montant_arrondi):
        """Appliquer arrondi commercial (2 décimales)."""
        from decimal import Decimal, ROUND_HALF_UP
        result = float(
            Decimal(str(montant_brut)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        )
        assert result == montant_arrondi


class TestFeedbackParType:
    """Tests du feedback adapté par type d'erreur."""
    
    def test_feedback_reponse_inexacte(self):
        """Feedback si réponse fausse."""
        fb = donner_feedback("5", 8)
        assert "mauvais" in fb.lower() or "incorrect" in fb.lower()
    
    def test_feedback_reponse_exacte(self):
        """Feedback si réponse exacte."""
        fb = donner_feedback("8", 8)
        assert "correct" in fb.lower() or "bravo" in fb.lower()
    
    def test_feedback_arrondi_acceptable(self):
        """Feedback si arrondi dans la tolérance."""
        fb = donner_feedback("4.99", 5, tolerance=0.1)
        assert "proche" in fb.lower() or "arrondi" in fb.lower() or "tolér" in fb.lower()


class TestPatternsErreurs:
    """Tests pour détecter patterns d'erreurs récurrentes."""
    
    def test_detection_erreur_calcul_systematique(self):
        """Détecter si l'utilisateur commet l'erreur +1 systématiquement."""
        erreurs = [
            ("3", 2),  # Réponse attendue 2, utilisateur dit 3
            ("4", 3),  # Réponse attendue 3, utilisateur dit 4
            ("6", 5),  # Réponse attendue 5, utilisateur dit 6
        ]
        # Vérifier qu'il y a un pattern +1
        differences =  - erreur for erreur in erreurs]
        assert all(d == 1 for d in differences)
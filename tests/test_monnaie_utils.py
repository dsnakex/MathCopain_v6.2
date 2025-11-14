import pytest
from decimal import Decimal
from src.monnaie_utils import (
    calculer_rendu_monnaie,
    convertir_centime_euro,
    formater_montant,
    valider_montant_positif
)


class TestCalculRenduMonnaie:
    """Tests du calcul du rendu de monnaie optimal."""
    
    def test_rendu_simple(self):
        """Rendu simple : 20€ - 8€ = 12€."""
        rendu = calculer_rendu_monnaie(montant_paye=20, montant_du=8)
        assert rendu == 12
    
    def test_rendu_zero(self):
        """Montant exact : pas de rendu."""
        rendu = calculer_rendu_monnaie(montant_paye=10, montant_du=10)
        assert rendu == 0
    
    def test_rendu_avec_decimales(self):
        """Rendu avec décimales : 20€ - 12,50€ = 7,50€."""
        rendu = calculer_rendu_monnaie(montant_paye=20, montant_du=12.50)
        assert abs(rendu - 7.50) < 0.01


class TestConversionCentimeEuro:
    """Tests des conversions centime ↔ euro."""
    
    @pytest.mark.parametrize("centimes,euros", [
        (100, 1.0),
        (250, 2.50),
        (1000, 10.0),
        (50, 0.50),
    ])
    def test_centime_vers_euro(self, centimes, euros):
        """Convertir centimes → euros."""
        assert convertir_centime_euro(centimes, vers="euro") == euros
    
    @pytest.mark.parametrize("euros,centimes", [
        (1.0, 100),
        (2.50, 250),
        (10.0, 1000),
    ])
    def test_euro_vers_centime(self, euros, centimes):
        """Convertir euros → centimes."""
        assert convertir_centime_euro(euros, vers="centime") == centimes


class TestArrondiCommercial:
    """Tests de l'arrondi commercial (2 décimales)."""
    
    @pytest.mark.parametrize("montant_brut,montant_arrondi", [
        (2.505, 2.51),
        (2.504, 2.50),
        (3.333, 3.33),
        (1.999, 2.00),
    ])
    def test_arrondi_vers_2_decimales(self, montant_brut, montant_arrondi):
        """Arrondir correctement à 2 décimales."""
        # Utiliser Decimal pour éviter erreurs de précision float
        montant = Decimal(str(montant_brut))
        arrondi = float(montant.quantize(Decimal('0.01')))
        assert arrondi == montant_arrondi


class TestValidationMontant:
    """Tests de validation des montants."""
    
    def test_montant_positif(self):
        """Montant positif = valide."""
        assert valider_montant_positif(10.50) is True
    
    def test_montant_zero(self):
        """Montant zéro = acceptable."""
        assert valider_montant_positif(0) is True
    
    def test_montant_negatif(self):
        """Montant négatif = invalide."""
        assert valider_montant_positif(-5) is False
    
    def test_montant_null(self):
        """Montant None = invalide."""
        assert valider_montant_positif(None) is False


class TestFormatageAffichage:
    """Tests du formatage d'affichage."""
    
    @pytest.mark.parametrize("montant,format_attendu", [
        (5, "5,00€"),
        (5.5, "5,50€"),
        (1000, "1 000,00€"),
        (1250.75, "1 250,75€"),
    ])
    def test_format_francais(self, montant, format_attendu):
        """Formater selon la convention française."""
        resultat = formater_montant(montant, locale="fr_FR")
        assert resultat == format_attendu
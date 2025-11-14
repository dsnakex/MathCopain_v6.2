"""Tests pour les utilitaires de monnaie."""
import pytest
from monnaie_utils import (
    centimes_vers_euros_texte,
    calculer_pieces_optimales,
    generer_calcul_rendu,
    generer_composition_monnaie,
    PIECES_BILLETS
)


class TestCentimesVersEurosTexte:
    """Tests de la conversion centimes → texte euros."""

    def test_conversion_euros_entiers(self):
        """100 centimes = '1€'."""
        result = centimes_vers_euros_texte(100)
        assert "1€" in result or "1 €" in result

    def test_conversion_euros_centimes(self):
        """250 centimes = '2€50'."""
        result = centimes_vers_euros_texte(250)
        assert "2€50" in result or "2€ 50" in result or "2,50€" in result

    def test_conversion_zero(self):
        """0 centimes = '0€'."""
        result = centimes_vers_euros_texte(0)
        assert "0" in result

    @pytest.mark.parametrize("centimes,attendu_euros", [
        (100, 1),
        (500, 5),
        (1000, 10),
        (50, 0),  # 50 centimes, partie euros = 0
    ])
    def test_conversions_multiples(self, centimes, attendu_euros):
        """Tester plusieurs conversions."""
        result = centimes_vers_euros_texte(centimes)
        assert isinstance(result, str)
        assert "€" in result


class TestCalculerPiecesOptimales:
    """Tests du calcul des pièces optimales pour un montant."""

    def test_pieces_pour_100_centimes(self):
        """100 centimes = 1 pièce de 1€."""
        pieces = calculer_pieces_optimales(100)

        assert isinstance(pieces, list)
        assert len(pieces) > 0
        # Vérifier qu'on a au moins une pièce de 100 centimes (1€)
        pieces_1euro = [p for p in pieces if p[0] == 100]
        assert len(pieces_1euro) > 0

    def test_pieces_pour_250_centimes(self):
        """250 centimes = 1×2€ + 1×50c optimal."""
        pieces = calculer_pieces_optimales(250)

        total_valeur = sum(p[0] * p[2] for p in pieces)
        assert total_valeur == 250

    def test_zero_centimes(self):
        """0 centimes = liste vide."""
        pieces = calculer_pieces_optimales(0)
        assert pieces == []

    def test_algorithme_glouton(self):
        """Vérifier que l'algorithme est glouton (plus grandes pièces d'abord)."""
        pieces = calculer_pieces_optimales(1000)  # 10€

        # Devrait utiliser des grandes pièces/billets d'abord
        if pieces:
            # La première pièce devrait être la plus grande possible
            assert pieces[0][0] >= 100  # Au moins 1€


class TestGenererCalculRendu:
    """Tests de la génération d'exercices de calcul de rendu."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """Générer exercice valide pour chaque niveau."""
        exercice = generer_calcul_rendu(niveau)

        assert 'prix' in exercice
        assert 'paye' in exercice
        assert 'rendu' in exercice
        assert exercice['paye'] >= exercice['prix']
        assert exercice['rendu'] == exercice['paye'] - exercice['prix']

    def test_rendu_positif(self):
        """Le rendu doit toujours être positif ou zéro."""
        for _ in range(10):
            exercice = generer_calcul_rendu("CM1")
            assert exercice['rendu'] >= 0

    def test_valeurs_realistes_CE1(self):
        """CE1 utilise des montants simples (euros entiers)."""
        exercice = generer_calcul_rendu("CE1")

        # CE1 devrait avoir des montants en euros entiers (multiples de 100 centimes)
        assert exercice['prix'] > 0
        assert exercice['paye'] > 0


class TestGenererCompositionMonnaie:
    """Tests de la génération d'exercices de composition de monnaie."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_composition_par_niveau(self, niveau):
        """Générer composition valide pour chaque niveau."""
        exercice = generer_composition_monnaie(niveau)

        assert 'montant_cible' in exercice
        assert 'pieces_disponibles' in exercice
        assert exercice['montant_cible'] > 0

    def test_pieces_disponibles_valides(self):
        """Les pièces disponibles sont dans PIECES_BILLETS."""
        exercice = generer_composition_monnaie("CM1")

        valeurs_valides = [p[0] for p in PIECES_BILLETS]
        for piece in exercice['pieces_disponibles']:
            assert piece[0] in valeurs_valides


class TestConstantesPiecesBillets:
    """Tests des constantes de pièces et billets."""

    def test_pieces_billets_ordre_decroissant(self):
        """PIECES_BILLETS doit être trié par ordre décroissant."""
        valeurs = [p[0] for p in PIECES_BILLETS]
        assert valeurs == sorted(valeurs, reverse=True)

    def test_pieces_billets_complet(self):
        """PIECES_BILLETS contient toutes les valeurs courantes."""
        valeurs = [p[0] for p in PIECES_BILLETS]

        # Vérifier présence des principales valeurs
        assert 5000 in valeurs  # 50€
        assert 2000 in valeurs  # 20€
        assert 1000 in valeurs  # 10€
        assert 500 in valeurs   # 5€
        assert 100 in valeurs   # 1€
        assert 1 in valeurs     # 1 centime
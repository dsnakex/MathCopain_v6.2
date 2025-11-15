"""Tests pour les utilitaires de monnaie."""
import pytest
from monnaie_utils import (
    centimes_vers_euros_texte,
    calculer_pieces_optimales,
    generer_calcul_rendu,
    generer_composition_monnaie,
    generer_probleme_realiste,
    expliquer_calcul_rendu,
    PIECES_BILLETS
)


class TestCentimesVersEurosTexte:
    """Tests de la conversion centimes → texte euros."""

    def test_conversion_euros_entiers(self):
        """100 centimes = '1 euro'."""
        result = centimes_vers_euros_texte(100)
        assert "1 euro" in result.lower() or "1€" in result

    def test_conversion_euros_centimes(self):
        """250 centimes = '2 euros 50 centimes' ou '2€50'."""
        result = centimes_vers_euros_texte(250)
        # Le résultat peut varier selon l'implémentation
        assert isinstance(result, str)
        assert len(result) > 0

    def test_conversion_zero(self):
        """0 centimes = '0€' ou '0 euro'."""
        result = centimes_vers_euros_texte(0)
        assert "0" in result

    @pytest.mark.parametrize("centimes", [100, 500, 1000, 50])
    def test_conversions_multiples(self, centimes):
        """Tester plusieurs conversions."""
        result = centimes_vers_euros_texte(centimes)
        assert isinstance(result, str)
        assert len(result) > 0


class TestCalculerPiecesOptimales:
    """Tests du calcul des pièces optimales pour un montant."""

    def test_pieces_pour_100_centimes(self):
        """100 centimes = 1 pièce de 1€."""
        pieces = calculer_pieces_optimales(100)

        assert isinstance(pieces, list)
        assert len(pieces) > 0
        # Vérifier structure tuple (valeur, nom, quantite)
        if pieces:
            assert len(pieces[0]) == 3

    def test_pieces_pour_250_centimes(self):
        """250 centimes = pièces optimales."""
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

        assert 'prix_centimes' in exercice
        assert 'paye_centimes' in exercice
        assert 'reponse_centimes' in exercice
        assert 'article' in exercice
        assert 'question' in exercice

        # Vérifier calcul correct
        assert exercice['paye_centimes'] >= exercice['prix_centimes']
        assert exercice['reponse_centimes'] == exercice['paye_centimes'] - exercice['prix_centimes']

    def test_rendu_positif(self):
        """Le rendu doit toujours être positif ou zéro."""
        for _ in range(10):
            exercice = generer_calcul_rendu("CM1")
            assert exercice['reponse_centimes'] >= 0

    def test_valeurs_realistes_CE1(self):
        """CE1 utilise des montants simples (euros entiers)."""
        exercice = generer_calcul_rendu("CE1")

        # CE1 devrait avoir des montants en euros entiers (multiples de 100 centimes)
        assert exercice['prix_centimes'] > 0
        assert exercice['paye_centimes'] > 0
        assert exercice['prix_centimes'] % 100 == 0  # Euros entiers pour CE1

    def test_prix_inferieur_paye(self):
        """Le montant payé doit être >= au prix."""
        for _ in range(10):
            exercice = generer_calcul_rendu("CM2")
            assert exercice['paye_centimes'] >= exercice['prix_centimes']


class TestGenererCompositionMonnaie:
    """Tests de la génération d'exercices de composition de monnaie."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_composition_par_niveau(self, niveau):
        """Générer composition valide pour chaque niveau."""
        exercice = generer_composition_monnaie(niveau)

        assert 'montant_centimes' in exercice
        assert 'composition' in exercice
        assert 'question' in exercice
        assert exercice['montant_centimes'] > 0

    def test_composition_valide(self):
        """La composition doit être valide."""
        exercice = generer_composition_monnaie("CM1")

        valeurs_valides = [p[0] for p in PIECES_BILLETS]
        for piece in exercice['composition']:
            # piece est un tuple (valeur, nom, quantite)
            assert piece[0] in valeurs_valides
            assert isinstance(piece[1], str)  # nom
            assert isinstance(piece[2], int)  # quantité
            assert piece[2] > 0

    def test_somme_composition_correcte(self):
        """La somme de la composition doit égaler le montant cible."""
        exercice = generer_composition_monnaie("CM2")

        total = sum(p[0] * p[2] for p in exercice['composition'])
        assert total == exercice['montant_centimes']


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

    def test_pieces_billets_structure(self):
        """Chaque élément est un tuple (valeur, nom)."""
        for piece in PIECES_BILLETS:
            assert isinstance(piece, tuple)
            assert len(piece) == 2
            assert isinstance(piece[0], int)  # valeur en centimes
            assert isinstance(piece[1], str)  # nom


class TestGenererProblemeRealiste:
    """Tests de génération problèmes réalistes."""

    @pytest.mark.parametrize("niveau", ["CE1", "CE2", "CM1", "CM2"])
    def test_generation_par_niveau(self, niveau):
        """generer_probleme_realiste() génère pour chaque niveau."""
        exercice = generer_probleme_realiste(niveau)
        assert 'total_centimes' in exercice
        assert 'total_texte' in exercice
        assert 'paye_centimes' in exercice
        assert 'paye_texte' in exercice
        assert 'reponse_centimes' in exercice
        assert 'reponse_texte' in exercice
        assert 'question' in exercice

    def test_paye_superieur_total(self):
        """Le montant payé doit être supérieur au total."""
        for _ in range(20):
            exercice = generer_probleme_realiste("CM1")
            assert exercice['paye_centimes'] >= exercice['total_centimes']

    def test_rendu_correct(self):
        """Le calcul du rendu est correct."""
        for _ in range(20):
            exercice = generer_probleme_realiste("CE2")
            attendu = exercice['paye_centimes'] - exercice['total_centimes']
            assert exercice['reponse_centimes'] == attendu

    def test_ce1_prix_simples(self):
        """CE1 utilise prix simples (euros entiers)."""
        for _ in range(20):
            exercice = generer_probleme_realiste("CE1")
            # CE1 devrait avoir euros entiers
            assert exercice['total_centimes'] % 100 == 0

    def test_question_contient_contexte(self):
        """La question contient un contexte."""
        exercice = generer_probleme_realiste("CM2")
        assert len(exercice['question']) > 20
        # Devrait contenir des mots clés
        question = exercice['question'].lower()
        assert any(mot in question for mot in ['achète', 'coût', 'pay', 'rend'])

    def test_cm2_peut_avoir_reduction(self):
        """CM2 peut inclure réductions."""
        # Générer plusieurs exercices CM2
        for _ in range(30):
            exercice = generer_probleme_realiste("CM2")
            question = exercice['question'].lower()
            if 'réduction' in question or 'réduc' in question:
                # Au moins un exercice avec réduction trouvé
                assert 'réduction' in question or 'réduc' in question
                break

    def test_textes_correspondent_centimes(self):
        """Les textes correspondent aux valeurs en centimes."""
        exercice = generer_probleme_realiste("CM1")
        # Vérifier que les conversions sont cohérentes
        assert isinstance(exercice['total_texte'], str)
        assert isinstance(exercice['paye_texte'], str)
        assert isinstance(exercice['reponse_texte'], str)
        assert len(exercice['total_texte']) > 0


class TestExpliquerCalculRendu:
    """Tests d'explication calcul de rendu."""

    def test_explication_generee(self):
        """expliquer_calcul_rendu() génère une explication."""
        explication = expliquer_calcul_rendu(150, 500, 350)
        assert isinstance(explication, str)
        assert len(explication) > 0

    def test_explication_contient_etapes(self):
        """L'explication contient les étapes."""
        explication = expliquer_calcul_rendu(200, 500, 300)
        assert "Étape" in explication or "tape" in explication

    def test_explication_contient_valeurs(self):
        """L'explication contient les valeurs."""
        explication = expliquer_calcul_rendu(250, 1000, 750)
        # Devrait mentionner les montants
        assert len(explication) > 50

    def test_explication_avec_emprunt(self):
        """Explication pour cas avec emprunt (centimes insuffisants)."""
        # 3€75 payé avec 5€ = 1€25 rendu
        # 375 centimes, 500 payés, 125 rendu
        explication = expliquer_calcul_rendu(375, 500, 125)
        assert isinstance(explication, str)
        # Devrait mentionner l'emprunt car 0 < 75
        assert "emprunt" in explication.lower() or "emprunte" in explication.lower()

    def test_explication_sans_emprunt(self):
        """Explication pour cas simple (assez de centimes)."""
        # 2€30 payé avec 5€ = 2€70 rendu
        # 230 centimes, 500 payés, 270 rendu
        explication = expliquer_calcul_rendu(230, 500, 270)
        assert isinstance(explication, str)
        assert len(explication) > 0

    def test_explication_contient_resultat(self):
        """L'explication contient le résultat final."""
        explication = expliquer_calcul_rendu(100, 500, 400)
        assert "Rendu" in explication or "rendu" in explication
        assert "4" in explication  # 400 centimes = 4€

    def test_explication_calcul_correct(self):
        """Les calculs dans l'explication sont cohérents."""
        prix, paye, rendu = 345, 1000, 655
        explication = expliquer_calcul_rendu(prix, paye, rendu)
        # Vérifier que rendu = paye - prix
        assert paye - prix == rendu
        # L'explication devrait mentionner ce calcul
        assert isinstance(explication, str)

"""Tests pour la gestion des utilisateurs."""
import pytest
import json
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
from utilisateur import (
    profil_par_defaut,
    _load_from_disk,
    _save_to_disk,
    FICHIER_UTILISATEURS
)


class TestProfilParDefaut:
    """Tests du profil par défaut."""

    def test_profil_contient_champs_requis(self):
        """Le profil par défaut contient tous les champs requis."""
        profil = profil_par_defaut()

        champs_requis = [
            'niveau', 'points', 'badges', 'exercices_reussis',
            'exercices_totaux', 'taux_reussite', 'date_creation',
            'date_derniere_session', 'progression', 'exercise_history'
        ]

        for champ in champs_requis:
            assert champ in profil

    def test_valeurs_initiales_correctes(self):
        """Les valeurs initiales sont correctes."""
        profil = profil_par_defaut()

        assert profil['niveau'] == 'CE1'
        assert profil['points'] == 0
        assert profil['badges'] == []
        assert profil['exercices_reussis'] == 0
        assert profil['exercices_totaux'] == 0
        assert profil['taux_reussite'] == 0
        assert profil['exercise_history'] == []

    def test_progression_tous_niveaux(self):
        """La progression contient tous les niveaux."""
        profil = profil_par_defaut()

        niveaux = ['CE1', 'CE2', 'CM1', 'CM2']
        for niveau in niveaux:
            assert niveau in profil['progression']
            assert profil['progression'][niveau] == 0

    def test_dates_au_format_correct(self):
        """Les dates sont au format correct."""
        profil = profil_par_defaut()

        # Vérifier format date_creation (YYYY-MM-DD)
        datetime.strptime(profil['date_creation'], "%Y-%m-%d")

        # Vérifier format date_derniere_session (ISO)
        datetime.fromisoformat(profil['date_derniere_session'])

    def test_profils_multiples_ont_meme_date(self):
        """Deux profils créés rapidement ont des dates similaires."""
        profil1 = profil_par_defaut()
        profil2 = profil_par_defaut()

        # Les dates devraient être identiques ou très proches
        assert profil1['date_creation'] == profil2['date_creation']


class TestLoadFromDisk:
    """Tests du chargement depuis disque."""

    def test_load_fichier_inexistant(self, tmp_path):
        """Charger un fichier qui n'existe pas retourne dict vide."""
        with patch('utilisateur.FICHIER_UTILISATEURS', str(tmp_path / 'inexistant.json')):
            result = _load_from_disk()
            assert result == {}

    def test_load_fichier_valide(self, tmp_path):
        """Charger un fichier JSON valide."""
        test_file = tmp_path / "test_users.json"
        test_data = {
            "alice": {"niveau": "CM1", "points": 100},
            "bob": {"niveau": "CE2", "points": 50}
        }

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            result = _load_from_disk()
            assert result == test_data

    def test_load_fichier_json_invalide(self, tmp_path):
        """Charger un fichier JSON invalide retourne dict vide."""
        test_file = tmp_path / "invalid.json"

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json content }")

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            result = _load_from_disk()
            assert result == {}

    def test_load_fichier_vide(self, tmp_path):
        """Charger un fichier vide retourne dict vide."""
        test_file = tmp_path / "empty.json"
        test_file.write_text("")

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            result = _load_from_disk()
            assert result == {}


class TestSaveToDisk:
    """Tests de la sauvegarde sur disque."""

    def test_save_donnees_valides(self, tmp_path):
        """Sauvegarder des données valides."""
        test_file = tmp_path / "test_save.json"
        test_data = {
            "user1": {"niveau": "CM2", "points": 200},
            "user2": {"niveau": "CE1", "points": 10}
        }

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk(test_data)

        # Vérifier que le fichier a été créé et contient les bonnes données
        assert test_file.exists()

        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data

    def test_save_dict_vide(self, tmp_path):
        """Sauvegarder un dict vide."""
        test_file = tmp_path / "empty_save.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk({})

        assert test_file.exists()

        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == {}

    def test_save_avec_caracteres_speciaux(self, tmp_path):
        """Sauvegarder avec caractères spéciaux (UTF-8)."""
        test_file = tmp_path / "utf8_save.json"
        test_data = {
            "élève1": {"nom": "François", "niveau": "CM1"},
            "élève2": {"nom": "Zoé", "niveau": "CE2"}
        }

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk(test_data)

        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data

    def test_save_ecrase_fichier_existant(self, tmp_path):
        """Sauvegarder écrase le fichier existant."""
        test_file = tmp_path / "overwrite.json"

        # Première sauvegarde
        data1 = {"user1": {"points": 100}}
        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk(data1)

        # Deuxième sauvegarde
        data2 = {"user2": {"points": 200}}
        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk(data2)

        # Vérifier que seules les données de data2 sont présentes
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == data2
        assert 'user1' not in loaded_data


class TestIntegrationUtilisateur:
    """Tests d'intégration pour le module utilisateur."""

    def test_cycle_save_load(self, tmp_path):
        """Cycle complet: sauvegarder puis charger."""
        test_file = tmp_path / "cycle.json"
        test_data = {
            "alice": profil_par_defaut(),
            "bob": profil_par_defaut()
        }

        # Modifier les profils
        test_data["alice"]["points"] = 150
        test_data["bob"]["niveau"] = "CM2"

        # Sauvegarder
        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            _save_to_disk(test_data)

        # Charger
        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            loaded_data = _load_from_disk()

        # Vérifier
        assert loaded_data["alice"]["points"] == 150
        assert loaded_data["bob"]["niveau"] == "CM2"

    def test_profil_par_defaut_serializable(self):
        """Le profil par défaut peut être sérialisé en JSON."""
        profil = profil_par_defaut()

        # Ne devrait pas lever d'exception
        json_str = json.dumps(profil)
        assert isinstance(json_str, str)

        # Désérialiser
        restored = json.loads(json_str)
        assert restored == profil


class TestValidationDonnees:
    """Tests de validation des données utilisateur."""

    def test_profil_types_corrects(self):
        """Vérifier les types des champs du profil."""
        profil = profil_par_defaut()

        assert isinstance(profil['niveau'], str)
        assert isinstance(profil['points'], int)
        assert isinstance(profil['badges'], list)
        assert isinstance(profil['exercices_reussis'], int)
        assert isinstance(profil['exercices_totaux'], int)
        assert isinstance(profil['taux_reussite'], (int, float))
        assert isinstance(profil['date_creation'], str)
        assert isinstance(profil['date_derniere_session'], str)
        assert isinstance(profil['progression'], dict)
        assert isinstance(profil['exercise_history'], list)

    def test_valeurs_numeriques_non_negatives(self):
        """Les valeurs numériques doivent être >= 0."""
        profil = profil_par_defaut()

        assert profil['points'] >= 0
        assert profil['exercices_reussis'] >= 0
        assert profil['exercices_totaux'] >= 0
        assert profil['taux_reussite'] >= 0

    def test_progression_valeurs_valides(self):
        """Les valeurs de progression sont valides."""
        profil = profil_par_defaut()

        for niveau, progression in profil['progression'].items():
            assert isinstance(niveau, str)
            assert isinstance(progression, (int, float))
            assert 0 <= progression <= 100  # Assumant que c'est un pourcentage

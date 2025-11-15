"""Tests pour la gestion des utilisateurs."""
import pytest
import json
import os
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open
from utilisateur import (
    profil_par_defaut,
    _load_from_disk,
    _save_to_disk,
    _get_user_cache,
    charger_utilisateur,
    sauvegarder_utilisateur,
    obtenir_tous_eleves,
    force_save,
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


class TestGetUserCache:
    """Tests du cache utilisateur singleton."""

    def test_cache_retourne_dict(self):
        """_get_user_cache() retourne un dictionnaire."""
        with patch('streamlit.cache_resource', lambda: lambda f: f):
            cache = _get_user_cache()
            assert isinstance(cache, dict)

    def test_cache_contient_cles_requises(self):
        """Le cache contient les clés data, loaded, dirty."""
        with patch('streamlit.cache_resource', lambda: lambda f: f):
            cache = _get_user_cache()
            assert 'data' in cache
            assert 'loaded' in cache
            assert 'dirty' in cache

    def test_cache_valeurs_initiales(self):
        """Les valeurs initiales du cache sont correctes."""
        with patch('streamlit.cache_resource', lambda: lambda f: f):
            cache = _get_user_cache()
            assert cache['data'] == {}
            assert cache['loaded'] is False
            assert cache['dirty'] is False


class TestChargerUtilisateur:
    """Tests de chargement d'un utilisateur."""

    def test_charger_utilisateur_existant(self, tmp_path):
        """Charger un utilisateur qui existe."""
        test_file = tmp_path / "users.json"
        test_data = {
            "alice": {"niveau": "CM1", "points": 100},
            "bob": {"niveau": "CE2", "points": 50}
        }

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                # Réinitialiser le cache
                cache = _get_user_cache()
                cache['data'] = {}
                cache['loaded'] = False

                result = charger_utilisateur("alice")
                assert result == {"niveau": "CM1", "points": 100}

    def test_charger_utilisateur_inexistant(self, tmp_path):
        """Charger un utilisateur qui n'existe pas retourne None."""
        test_file = tmp_path / "users.json"
        test_data = {"alice": {"niveau": "CM1", "points": 100}}

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {}
                cache['loaded'] = False

                result = charger_utilisateur("bob")
                assert result is None

    def test_charger_utilise_cache_apres_premier_chargement(self, tmp_path):
        """Après le premier chargement, le cache est utilisé."""
        test_file = tmp_path / "users.json"
        test_data = {"alice": {"niveau": "CM1", "points": 100}}

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {}
                cache['loaded'] = False

                # Premier chargement
                charger_utilisateur("alice")
                assert cache['loaded'] is True

                # Modifier le cache manuellement
                cache['data']['alice']['points'] = 999

                # Deuxième chargement (doit utiliser cache)
                result = charger_utilisateur("alice")
                assert result['points'] == 999  # Valeur du cache, pas du disque


class TestSauvegarderUtilisateur:
    """Tests de sauvegarde d'un utilisateur."""

    def test_sauvegarder_met_a_jour_cache(self, tmp_path):
        """Sauvegarder met à jour le cache immédiatement."""
        test_file = tmp_path / "users.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MagicMock()) as mock_state:
                    mock_state._save_counter = 0

                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = True
                    cache['dirty'] = False

                    new_data = {"niveau": "CM2", "points": 200}
                    sauvegarder_utilisateur("alice", new_data)

                    # Vérifier mise à jour cache
                    assert cache['data']['alice'] == new_data
                    assert cache['dirty'] is True

    def test_sauvegarder_marque_dirty(self, tmp_path):
        """Sauvegarder marque le cache comme dirty."""
        test_file = tmp_path / "users.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MagicMock()) as mock_state:
                    mock_state._save_counter = 0

                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = True
                    cache['dirty'] = False

                    sauvegarder_utilisateur("bob", {"niveau": "CE1"})

                    assert cache['dirty'] is True

    def test_sauvegarder_flush_apres_5_modifications(self, tmp_path):
        """Le cache est sauvegardé sur disque après 5 modifications."""
        test_file = tmp_path / "users.json"

        # Créer un objet simple pour session_state
        class MockSessionState:
            def __init__(self):
                self._save_counter = 4
            def __contains__(self, key):
                return hasattr(self, key)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MockSessionState()):
                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = True
                    cache['dirty'] = True

                    # 5ème sauvegarde devrait déclencher flush
                    sauvegarder_utilisateur("charlie", {"niveau": "CM1"})

                    # Vérifier que le fichier a été créé
                    assert test_file.exists()

                    # Vérifier dirty reset
                    assert cache['dirty'] is False

    def test_sauvegarder_charge_cache_si_non_loaded(self, tmp_path):
        """Si cache non chargé, il est chargé avant sauvegarde."""
        test_file = tmp_path / "users.json"
        initial_data = {"existing": {"niveau": "CE2", "points": 50}}

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MagicMock()) as mock_state:
                    mock_state._save_counter = 0

                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = False  # Non chargé

                    sauvegarder_utilisateur("new_user", {"niveau": "CM1"})

                    # Cache doit contenir les données existantes + nouvelle
                    assert "existing" in cache['data']
                    assert "new_user" in cache['data']


class TestObtenirTousEleves:
    """Tests d'obtention de tous les élèves."""

    def test_obtenir_tous_eleves_liste_vide(self, tmp_path):
        """Aucun élève retourne liste vide."""
        test_file = tmp_path / "empty_users.json"

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {}
                cache['loaded'] = False

                result = obtenir_tous_eleves()
                assert result == []

    def test_obtenir_tous_eleves_avec_utilisateurs(self, tmp_path):
        """Retourne liste des noms d'utilisateurs."""
        test_file = tmp_path / "users.json"
        test_data = {
            "alice": {"niveau": "CM1"},
            "bob": {"niveau": "CE2"},
            "charlie": {"niveau": "CM2"}
        }

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {}
                cache['loaded'] = False

                result = obtenir_tous_eleves()
                assert set(result) == {"alice", "bob", "charlie"}

    def test_obtenir_tous_eleves_utilise_cache(self, tmp_path):
        """obtenir_tous_eleves() utilise le cache."""
        test_file = tmp_path / "users.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {"alice": {}, "bob": {}}
                cache['loaded'] = True  # Déjà chargé

                result = obtenir_tous_eleves()
                assert set(result) == {"alice", "bob"}


class TestForceSave:
    """Tests de force_save()."""

    def test_force_save_sauvegarde_si_dirty(self, tmp_path):
        """force_save() sauvegarde si cache est dirty."""
        test_file = tmp_path / "force_save.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {"alice": {"niveau": "CM1", "points": 100}}
                cache['dirty'] = True

                force_save()

                # Vérifier fichier créé
                assert test_file.exists()

                # Vérifier dirty reset
                assert cache['dirty'] is False

                # Vérifier contenu
                with open(test_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                assert saved_data == {"alice": {"niveau": "CM1", "points": 100}}

    def test_force_save_ne_fait_rien_si_clean(self, tmp_path):
        """force_save() ne fait rien si cache est clean."""
        test_file = tmp_path / "no_save.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {"alice": {"niveau": "CM1"}}
                cache['dirty'] = False

                force_save()

                # Fichier ne devrait pas être créé
                assert not test_file.exists()

    def test_force_save_preserve_donnees_existantes(self, tmp_path):
        """force_save() ne perd pas de données."""
        test_file = tmp_path / "preserve.json"
        initial_data = {"bob": {"niveau": "CE2", "points": 50}}

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                cache = _get_user_cache()
                cache['data'] = {
                    "bob": {"niveau": "CE2", "points": 50},
                    "alice": {"niveau": "CM1", "points": 100}
                }
                cache['dirty'] = True

                force_save()

                with open(test_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)

                assert "bob" in saved_data
                assert "alice" in saved_data


class TestCacheIntegration:
    """Tests d'intégration du système de cache."""

    def test_workflow_complet_avec_cache(self, tmp_path):
        """Workflow: charger → modifier → sauvegarder → force_save."""
        test_file = tmp_path / "workflow.json"
        initial_data = {"alice": {"niveau": "CE1", "points": 0}}

        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MagicMock()) as mock_state:
                    mock_state._save_counter = 0

                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = False

                    # 1. Charger
                    profil = charger_utilisateur("alice")
                    assert profil['points'] == 0

                    # 2. Modifier
                    profil['points'] = 150

                    # 3. Sauvegarder
                    sauvegarder_utilisateur("alice", profil)

                    # Cache doit être à jour
                    assert cache['data']['alice']['points'] == 150

                    # 4. Force save
                    force_save()

                    # Vérifier fichier
                    with open(test_file, 'r', encoding='utf-8') as f:
                        saved_data = json.load(f)
                    assert saved_data['alice']['points'] == 150

    def test_cache_partage_entre_fonctions(self, tmp_path):
        """Le cache est partagé entre toutes les fonctions."""
        test_file = tmp_path / "shared.json"

        with patch('utilisateur.FICHIER_UTILISATEURS', str(test_file)):
            with patch('streamlit.cache_resource', lambda: lambda f: f):
                with patch('utilisateur.st.session_state', MagicMock()) as mock_state:
                    mock_state._save_counter = 0

                    cache = _get_user_cache()
                    cache['data'] = {}
                    cache['loaded'] = True

                    # Sauvegarder via sauvegarder_utilisateur
                    sauvegarder_utilisateur("alice", {"niveau": "CM1"})

                    # Récupérer via charger_utilisateur
                    profil = charger_utilisateur("alice")
                    assert profil['niveau'] == "CM1"

                    # Vérifier via obtenir_tous_eleves
                    eleves = obtenir_tous_eleves()
                    assert "alice" in eleves

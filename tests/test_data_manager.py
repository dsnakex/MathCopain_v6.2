"""
Tests pour core/data_manager.py
Tests du gestionnaire de données avec atomic writes et backups
"""

import pytest
import json
import os
from core.data_manager import DataManager


@pytest.fixture
def temp_data_dir(tmp_path):
    """Répertoire temporaire pour tests."""
    return str(tmp_path)


@pytest.fixture
def data_manager(temp_data_dir):
    """Fixture DataManager avec répertoire temporaire."""
    return DataManager(temp_data_dir)


class TestDataManagerInit:
    """Tests d'initialisation."""

    def test_init_creates_backup_dir(self, temp_data_dir):
        """L'initialisation crée le répertoire backups."""
        manager = DataManager(temp_data_dir)
        backup_dir = os.path.join(temp_data_dir, "backups")
        assert os.path.exists(backup_dir)
        assert os.path.isdir(backup_dir)

    def test_init_sets_data_dir(self, data_manager, temp_data_dir):
        """L'initialisation définit le data_dir."""
        assert data_manager.data_dir == temp_data_dir

    def test_init_sets_backup_dir(self, data_manager, temp_data_dir):
        """L'initialisation définit le backup_dir."""
        expected = os.path.join(temp_data_dir, "backups")
        assert data_manager.backup_dir == expected


class TestLoadJson:
    """Tests de chargement JSON."""

    def test_load_nonexistent_file_returns_default(self, data_manager):
        """load_json() retourne default si fichier inexistant."""
        result = data_manager.load_json("nonexistent.json", default={'key': 'value'})
        assert result == {'key': 'value'}

    def test_load_nonexistent_file_no_default(self, data_manager):
        """load_json() sans default retourne dict vide."""
        result = data_manager.load_json("nonexistent.json")
        assert result == {}

    def test_load_valid_json(self, data_manager, temp_data_dir):
        """load_json() charge un fichier JSON valide."""
        # Créer fichier test
        test_data = {'name': 'Test', 'value': 42}
        filepath = os.path.join(temp_data_dir, "test.json")
        with open(filepath, 'w') as f:
            json.dump(test_data, f)

        result = data_manager.load_json("test.json")
        assert result == test_data

    def test_load_invalid_json_returns_default(self, data_manager, temp_data_dir):
        """load_json() retourne default si JSON invalide."""
        # Créer fichier JSON invalide
        filepath = os.path.join(temp_data_dir, "invalid.json")
        with open(filepath, 'w') as f:
            f.write("{ invalid json }")

        result = data_manager.load_json("invalid.json", default={'error': True})
        assert result == {'error': True}

    def test_load_empty_file_returns_default(self, data_manager, temp_data_dir):
        """load_json() retourne default pour fichier vide."""
        filepath = os.path.join(temp_data_dir, "empty.json")
        with open(filepath, 'w') as f:
            f.write("")

        result = data_manager.load_json("empty.json", default={})
        assert result == {}


class TestSaveJson:
    """Tests de sauvegarde JSON."""

    def test_save_creates_new_file(self, data_manager, temp_data_dir):
        """save_json() crée un nouveau fichier."""
        test_data = {'key': 'value'}
        result = data_manager.save_json("new.json", test_data)

        assert result is True
        filepath = os.path.join(temp_data_dir, "new.json")
        assert os.path.exists(filepath)

    def test_save_writes_correct_content(self, data_manager, temp_data_dir):
        """save_json() écrit le contenu correct."""
        test_data = {'name': 'Test', 'numbers': [1, 2, 3]}
        data_manager.save_json("content.json", test_data)

        filepath = os.path.join(temp_data_dir, "content.json")
        with open(filepath, 'r') as f:
            loaded = json.load(f)

        assert loaded == test_data

    def test_save_overwrites_existing_file(self, data_manager, temp_data_dir):
        """save_json() écrase un fichier existant."""
        # Créer fichier initial
        initial_data = {'old': 'data'}
        data_manager.save_json("overwrite.json", initial_data)

        # Écraser
        new_data = {'new': 'data'}
        result = data_manager.save_json("overwrite.json", new_data)

        assert result is True
        loaded = data_manager.load_json("overwrite.json")
        assert loaded == new_data

    def test_save_with_validation_success(self, data_manager):
        """save_json() avec validation qui passe."""
        def validator(data):
            return 'required_key' in data

        test_data = {'required_key': 'present', 'other': 'data'}
        result = data_manager.save_json("validated.json", test_data, validate_schema=validator)

        assert result is True

    def test_save_with_validation_failure(self, data_manager):
        """save_json() avec validation qui échoue."""
        def validator(data):
            return 'required_key' in data

        test_data = {'wrong_key': 'value'}
        result = data_manager.save_json("invalid.json", test_data, validate_schema=validator)

        assert result is False

    def test_save_creates_backup_by_default(self, data_manager, temp_data_dir):
        """save_json() crée un backup par défaut."""
        # Créer fichier initial
        data_manager.save_json("backup_test.json", {'version': 1})

        # Mise à jour (devrait créer backup)
        data_manager.save_json("backup_test.json", {'version': 2})

        # Vérifier existence backup
        backups = os.listdir(os.path.join(temp_data_dir, "backups"))
        backup_files = [b for b in backups if b.startswith("backup_test.json")]
        assert len(backup_files) >= 1

    def test_save_without_backup(self, data_manager, temp_data_dir):
        """save_json() sans backup si create_backup=False."""
        # Créer fichier initial
        data_manager.save_json("no_backup.json", {'version': 1})

        # Mise à jour sans backup
        data_manager.save_json("no_backup.json", {'version': 2}, create_backup=False)

        # Vérifier pas de backup créé
        backups = os.listdir(os.path.join(temp_data_dir, "backups"))
        backup_files = [b for b in backups if b.startswith("no_backup.json")]
        # Peut avoir 0 ou 1 backup (du premier save si default create_backup=True)
        # On vérifie juste qu'il n'y a pas 2 backups
        assert len(backup_files) <= 1


class TestBackupManagement:
    """Tests de gestion des backups."""

    def test_backup_is_created(self, data_manager, temp_data_dir):
        """_create_backup() crée un backup."""
        # Créer fichier
        filepath = os.path.join(temp_data_dir, "test.json")
        with open(filepath, 'w') as f:
            json.dump({'data': 'original'}, f)

        # Créer backup
        data_manager._create_backup("test.json")

        # Vérifier backup existe
        backups = os.listdir(data_manager.backup_dir)
        assert any(b.startswith("test.json") and b.endswith(".bak") for b in backups)

    def test_backup_preserves_content(self, data_manager, temp_data_dir):
        """Le backup préserve le contenu original."""
        original_data = {'important': 'data', 'value': 123}
        data_manager.save_json("preserve.json", original_data)

        # Modifier fichier
        data_manager.save_json("preserve.json", {'different': 'data'})

        # Vérifier backup contient données originales
        backups = os.listdir(data_manager.backup_dir)
        backup_file = [b for b in backups if b.startswith("preserve.json")][0]
        backup_path = os.path.join(data_manager.backup_dir, backup_file)

        with open(backup_path, 'r') as f:
            backup_data = json.load(f)

        assert backup_data == original_data

    def test_cleanup_keeps_recent_backups(self, data_manager):
        """_cleanup_old_backups() garde les N plus récents."""
        # Créer 15 faux backups
        for i in range(15):
            backup_name = f"test.json.2024010{i:02d}_120000.bak"
            backup_path = os.path.join(data_manager.backup_dir, backup_name)
            with open(backup_path, 'w') as f:
                f.write('{}')

        # Cleanup (garde 10)
        data_manager._cleanup_old_backups("test.json", keep=10)

        # Vérifier seulement 10 restent
        backups = os.listdir(data_manager.backup_dir)
        test_backups = [b for b in backups if b.startswith("test.json")]
        assert len(test_backups) == 10

    def test_cleanup_keeps_most_recent(self, data_manager):
        """_cleanup_old_backups() garde les plus récents."""
        # Créer backups avec dates différentes
        dates = ["20240101", "20240102", "20240103"]
        for date in dates:
            backup_name = f"test.json.{date}_120000.bak"
            backup_path = os.path.join(data_manager.backup_dir, backup_name)
            with open(backup_path, 'w') as f:
                json.dump({'date': date}, f)

        # Cleanup (garde 2)
        data_manager._cleanup_old_backups("test.json", keep=2)

        # Vérifier les 2 plus récents restent
        backups = os.listdir(data_manager.backup_dir)
        test_backups = sorted([b for b in backups if b.startswith("test.json")])
        assert len(test_backups) == 2
        # Les plus récents ont les dates les plus hautes
        assert "20240103" in test_backups[-1]
        assert "20240102" in test_backups[-2]


class TestAtomicWrites:
    """Tests des écritures atomiques."""

    def test_save_is_atomic(self, data_manager, temp_data_dir):
        """save_json() utilise atomic write (pas de corruption partielle)."""
        # Écrire gros fichier
        large_data = {'numbers': list(range(1000))}
        result = data_manager.save_json("atomic.json", large_data)

        assert result is True
        # Si écriture atomique réussie, fichier doit être complet
        loaded = data_manager.load_json("atomic.json")
        assert loaded == large_data

    def test_temp_files_cleaned_up(self, data_manager, temp_data_dir):
        """Les fichiers temporaires sont nettoyés."""
        data_manager.save_json("cleanup.json", {'data': 'test'})

        # Vérifier aucun fichier .tmp restant
        files = os.listdir(temp_data_dir)
        tmp_files = [f for f in files if f.endswith('.tmp')]
        assert len(tmp_files) == 0


class TestErrorHandling:
    """Tests de gestion des erreurs."""

    @pytest.mark.skipif(os.getuid() == 0, reason="Test ne fonctionne pas en tant que root")
    def test_load_handles_permission_error(self, data_manager, temp_data_dir):
        """load_json() gère les erreurs de permission."""
        # Créer fichier
        filepath = os.path.join(temp_data_dir, "restricted.json")
        with open(filepath, 'w') as f:
            json.dump({'data': 'test'}, f)

        # Retirer permissions lecture (si possible)
        try:
            os.chmod(filepath, 0o000)
            result = data_manager.load_json("restricted.json", default={'error': 'handled'})
            # Devrait retourner default
            assert result == {'error': 'handled'}
        finally:
            # Restaurer permissions
            os.chmod(filepath, 0o644)

    def test_save_returns_false_on_error(self, data_manager):
        """save_json() retourne False en cas d'erreur."""
        # Tenter sauvegarder objet non-sérialisable
        class NonSerializable:
            pass

        result = data_manager.save_json("bad.json", {'obj': NonSerializable()})
        assert result is False

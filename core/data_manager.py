"""
Data Manager - Validation et écritures atomiques de données
Garantit intégrité des données utilisateur
"""

import json
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataManager:
    """
    Gère lecture/écriture sécurisée des données JSON.

    Features:
    - Validation schéma avant sauvegarde
    - Écritures atomiques (temp file + rename)
    - Backups automatiques
    - Gestion erreurs robuste
    """

    def __init__(self, data_dir: str = "."):
        """
        Args:
            data_dir: Répertoire racine pour fichiers données
        """
        self.data_dir = data_dir
        self.backup_dir = os.path.join(data_dir, "backups")

        # Créer backup dir si inexistant
        os.makedirs(self.backup_dir, exist_ok=True)

    def load_json(self, filename: str, default: Any = None) -> Any:
        """
        Charge fichier JSON de manière sécurisée.

        Args:
            filename: Nom du fichier (ex: "users.json")
            default: Valeur par défaut si fichier inexistant

        Returns:
            Données chargées ou default
        """
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            logger.info(f"File {filename} not found, using default")
            return default if default is not None else {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f"Loaded {filename} successfully")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {filename}: {e}")
            # Tenter backup recovery
            backup_data = self._try_load_latest_backup(filename)
            if backup_data is not None:
                logger.info(f"Recovered {filename} from backup")
                return backup_data
            return default if default is not None else {}

        except IOError as e:
            logger.error(f"IO error reading {filename}: {e}")
            return default if default is not None else {}

    def save_json(
        self,
        filename: str,
        data: Any,
        create_backup: bool = True,
        validate_schema: Optional[callable] = None
    ) -> bool:
        """
        Sauvegarde données JSON de manière atomique.

        Process:
        1. Valider données (si validate_schema fourni)
        2. Créer backup du fichier existant
        3. Écrire vers fichier temporaire
        4. Renommer temp → final (opération atomique)

        Args:
            filename: Nom du fichier
            data: Données à sauvegarder
            create_backup: Créer backup avant écrasement
            validate_schema: Fonction validation (data) -> bool

        Returns:
            True si succès, False sinon
        """
        # Validation schéma
        if validate_schema and not validate_schema(data):
            logger.error(f"Schema validation failed for {filename}")
            return False

        filepath = os.path.join(self.data_dir, filename)

        # Backup si fichier existe
        if create_backup and os.path.exists(filepath):
            self._create_backup(filename)

        # Écriture atomique via temp file
        try:
            # Créer temp file dans même directory (atomic rename requirement)
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.data_dir,
                prefix=f".{filename}.",
                suffix=".tmp"
            )

            # Écrire données
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Atomic rename
            shutil.move(temp_path, filepath)

            logger.debug(f"Saved {filename} successfully (atomic)")
            return True

        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
            # Cleanup temp file si existe
            if 'temp_path' in locals() and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return False

    def _create_backup(self, filename: str):
        """Crée backup daté du fichier."""
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.{timestamp}.bak"
        backup_path = os.path.join(self.backup_dir, backup_name)

        try:
            shutil.copy2(filepath, backup_path)
            logger.debug(f"Created backup: {backup_name}")

            # Garder seulement 10 derniers backups
            self._cleanup_old_backups(filename, keep=10)

        except Exception as e:
            logger.warning(f"Backup creation failed for {filename}: {e}")

    def _cleanup_old_backups(self, filename: str, keep: int = 10):
        """Supprime anciens backups, garde les N plus récents."""
        try:
            # Lister backups pour ce fichier
            backups = [
                f for f in os.listdir(self.backup_dir)
                if f.startswith(filename) and f.endswith('.bak')
            ]

            # Trier par date (plus récent en premier)
            backups.sort(reverse=True)

            # Supprimer anciens
            for old_backup in backups[keep:]:
                os.remove(os.path.join(self.backup_dir, old_backup))
                logger.debug(f"Deleted old backup: {old_backup}")

        except Exception as e:
            logger.warning(f"Backup cleanup failed: {e}")

    def _try_load_latest_backup(self, filename: str) -> Optional[Any]:
        """Tente charger backup le plus récent."""
        try:
            backups = [
                f for f in os.listdir(self.backup_dir)
                if f.startswith(filename) and f.endswith('.bak')
            ]

            if not backups:
                return None

            # Plus récent en premier
            backups.sort(reverse=True)
            latest = backups[0]

            backup_path = os.path.join(self.backup_dir, latest)
            with open(backup_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Backup recovery failed: {e}")
            return None

    # ========== Validation Schemas ==========

    @staticmethod
    def validate_user_profile(data: Dict) -> bool:
        """
        Valide schéma profil utilisateur.

        Champs requis:
        - niveau: str (CE1/CE2/CM1/CM2)
        - points: int >= 0
        - badges: list
        - exercices_reussis: int >= 0
        - exercices_totaux: int >= 0
        """
        required_fields = [
            'niveau', 'points', 'badges',
            'exercices_reussis', 'exercices_totaux'
        ]

        # Vérifier champs requis
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        # Validation types et valeurs
        if data['niveau'] not in ['CE1', 'CE2', 'CM1', 'CM2']:
            logger.error(f"Invalid niveau: {data['niveau']}")
            return False

        if not isinstance(data['points'], int) or data['points'] < 0:
            logger.error(f"Invalid points: {data['points']}")
            return False

        if not isinstance(data['badges'], list):
            logger.error("Badges must be a list")
            return False

        if not isinstance(data['exercices_reussis'], int) or data['exercices_reussis'] < 0:
            logger.error("Invalid exercices_reussis")
            return False

        if not isinstance(data['exercices_totaux'], int) or data['exercices_totaux'] < 0:
            logger.error("Invalid exercices_totaux")
            return False

        # exercices_reussis <= exercices_totaux
        if data['exercices_reussis'] > data['exercices_totaux']:
            logger.error("exercices_reussis > exercices_totaux")
            return False

        return True

    @staticmethod
    def validate_users_data(data: Dict) -> bool:
        """Valide fichier utilisateurs complet."""
        if not isinstance(data, dict):
            logger.error("Users data must be a dict")
            return False

        # Valider chaque profil
        for username, profile in data.items():
            if not isinstance(username, str) or len(username) == 0:
                logger.error(f"Invalid username: {username}")
                return False

            if not DataManager.validate_user_profile(profile):
                logger.error(f"Invalid profile for user: {username}")
                return False

        return True

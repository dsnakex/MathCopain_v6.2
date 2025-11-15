#!/usr/bin/env python3
"""
Backup & Restore Tool - MathCopain v6.3.0
Sauvegarde et restauration complète des données utilisateurs

Usage:
    # Créer backup
    python backup_restore.py backup [--output DIR]

    # Restaurer backup
    python backup_restore.py restore BACKUP_FILE [--confirm]

    # Lister backups
    python backup_restore.py list [--dir DIR]

    # Nettoyer vieux backups
    python backup_restore.py cleanup [--keep N] [--dir DIR]
"""

import json
import os
import sys
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
DEFAULT_BACKUP_DIR = "backups"
USERS_FILE = "utilisateurs_securises.json"
USERS_OLD_FILE = "utilisateurs.json"  # Ancien format


def create_backup_dir(backup_dir: str = DEFAULT_BACKUP_DIR) -> str:
    """Créer répertoire backups s'il n'existe pas."""
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    return backup_dir


def generate_backup_filename() -> str:
    """Générer nom de fichier backup avec timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"mathcopain_backup_{timestamp}.json"


def backup_users(output_dir: str = DEFAULT_BACKUP_DIR) -> Tuple[bool, str]:
    """
    Créer backup complet des données utilisateurs.

    Args:
        output_dir: Répertoire de destination

    Returns:
        (success, backup_path ou error_message)
    """
    try:
        # Créer répertoire backup
        create_backup_dir(output_dir)

        # Charger données utilisateurs
        users_data = {}
        users_old_data = {}

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)

        if os.path.exists(USERS_OLD_FILE):
            with open(USERS_OLD_FILE, 'r', encoding='utf-8') as f:
                users_old_data = json.load(f)

        # Créer backup complet avec métadonnées
        backup_data = {
            "version": "6.3.0",
            "backup_date": datetime.now().isoformat(),
            "users_count": len(users_data),
            "users_old_count": len(users_old_data),
            "users": users_data,
            "users_old_format": users_old_data
        }

        # Sauvegarder
        backup_filename = generate_backup_filename()
        backup_path = os.path.join(output_dir, backup_filename)

        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        return True, backup_path

    except Exception as e:
        return False, f"Erreur backup: {e}"


def list_backups(backup_dir: str = DEFAULT_BACKUP_DIR) -> List[Dict]:
    """
    Lister tous les backups disponibles.

    Args:
        backup_dir: Répertoire des backups

    Returns:
        Liste de dicts avec infos backup
    """
    if not os.path.exists(backup_dir):
        return []

    backups = []

    for filename in os.listdir(backup_dir):
        if not filename.startswith("mathcopain_backup_") or not filename.endswith(".json"):
            continue

        filepath = os.path.join(backup_dir, filename)

        try:
            # Lire métadonnées
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Info backup
            file_size = os.path.getsize(filepath)

            backups.append({
                "filename": filename,
                "filepath": filepath,
                "date": data.get("backup_date", "Unknown"),
                "users_count": data.get("users_count", 0),
                "version": data.get("version", "Unknown"),
                "size_bytes": file_size,
                "size_mb": round(file_size / 1024 / 1024, 2)
            })

        except Exception as e:
            print(f"⚠️  Erreur lecture {filename}: {e}")
            continue

    # Trier par date (plus récent en premier)
    backups.sort(key=lambda x: x['date'], reverse=True)

    return backups


def restore_backup(backup_path: str, confirm: bool = False) -> Tuple[bool, str]:
    """
    Restaurer backup.

    Args:
        backup_path: Chemin du fichier backup
        confirm: Si False, dry-run seulement

    Returns:
        (success, message)
    """
    if not os.path.exists(backup_path):
        return False, f"Fichier backup introuvable: {backup_path}"

    try:
        # Charger backup
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        # Vérifier structure
        if "users" not in backup_data:
            return False, "Backup invalide: champ 'users' manquant"

        users_count = backup_data.get("users_count", len(backup_data["users"]))
        backup_date = backup_data.get("backup_date", "Unknown")

        print(f"\n📦 Backup Info:")
        print(f"   Date: {backup_date}")
        print(f"   Utilisateurs: {users_count}")
        print(f"   Version: {backup_data.get('version', 'Unknown')}")

        if not confirm:
            print(f"\n🔍 DRY RUN - Aucune modification effectuée")
            print(f"   Pour restaurer, ajoutez --confirm")
            return True, "Dry-run OK"

        # Créer backup des fichiers actuels avant écrasement
        if os.path.exists(USERS_FILE):
            backup_current = f"{USERS_FILE}.before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(USERS_FILE, backup_current)
            print(f"✅ Backup fichier actuel: {backup_current}")

        # Restaurer utilisateurs sécurisés
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(backup_data["users"], f, indent=4, ensure_ascii=False)

        # Restaurer ancien format si présent
        if "users_old_format" in backup_data and backup_data["users_old_format"]:
            with open(USERS_OLD_FILE, 'w', encoding='utf-8') as f:
                json.dump(backup_data["users_old_format"], f, indent=2, ensure_ascii=False)

        return True, f"Restore réussi: {users_count} utilisateurs restaurés"

    except Exception as e:
        return False, f"Erreur restore: {e}"


def cleanup_old_backups(keep: int = 10, backup_dir: str = DEFAULT_BACKUP_DIR) -> Tuple[int, int]:
    """
    Supprimer vieux backups, garder les N plus récents.

    Args:
        keep: Nombre de backups à garder
        backup_dir: Répertoire des backups

    Returns:
        (deleted_count, kept_count)
    """
    backups = list_backups(backup_dir)

    if len(backups) <= keep:
        return 0, len(backups)

    # Supprimer backups en trop
    to_delete = backups[keep:]
    deleted = 0

    for backup in to_delete:
        try:
            os.remove(backup['filepath'])
            print(f"🗑️  Supprimé: {backup['filename']}")
            deleted += 1
        except Exception as e:
            print(f"⚠️  Erreur suppression {backup['filename']}: {e}")

    return deleted, len(backups) - deleted


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Backup & Restore Tool - MathCopain v6.3.0"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')

    # Commande backup
    backup_parser = subparsers.add_parser('backup', help='Créer backup')
    backup_parser.add_argument(
        '--output', '-o',
        default=DEFAULT_BACKUP_DIR,
        help=f'Répertoire destination (défaut: {DEFAULT_BACKUP_DIR})'
    )

    # Commande restore
    restore_parser = subparsers.add_parser('restore', help='Restaurer backup')
    restore_parser.add_argument('backup_file', help='Fichier backup à restaurer')
    restore_parser.add_argument(
        '--confirm',
        action='store_true',
        help='Confirmer restauration (sinon dry-run)'
    )

    # Commande list
    list_parser = subparsers.add_parser('list', help='Lister backups')
    list_parser.add_argument(
        '--dir', '-d',
        default=DEFAULT_BACKUP_DIR,
        help=f'Répertoire backups (défaut: {DEFAULT_BACKUP_DIR})'
    )

    # Commande cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Nettoyer vieux backups')
    cleanup_parser.add_argument(
        '--keep', '-k',
        type=int,
        default=10,
        help='Nombre de backups à garder (défaut: 10)'
    )
    cleanup_parser.add_argument(
        '--dir', '-d',
        default=DEFAULT_BACKUP_DIR,
        help=f'Répertoire backups (défaut: {DEFAULT_BACKUP_DIR})'
    )

    args = parser.parse_args()

    # Exécuter commande
    if args.command == 'backup':
        print("🔄 Création backup...")
        success, result = backup_users(args.output)

        if success:
            print(f"✅ Backup créé: {result}")
            return 0
        else:
            print(f"❌ {result}")
            return 1

    elif args.command == 'restore':
        print(f"🔄 Restauration backup: {args.backup_file}")
        success, message = restore_backup(args.backup_file, args.confirm)

        if success:
            print(f"✅ {message}")
            return 0
        else:
            print(f"❌ {message}")
            return 1

    elif args.command == 'list':
        backups = list_backups(args.dir)

        if not backups:
            print(f"📁 Aucun backup trouvé dans {args.dir}")
            return 0

        print(f"\n📦 Backups disponibles ({len(backups)}):\n")
        print(f"{'Date':<20} {'Utilisateurs':<15} {'Taille':<10} {'Fichier'}")
        print("-" * 80)

        for backup in backups:
            date_str = backup['date'][:19] if len(backup['date']) > 19 else backup['date']
            print(f"{date_str:<20} {backup['users_count']:<15} {backup['size_mb']:.2f} MB   {backup['filename']}")

        return 0

    elif args.command == 'cleanup':
        print(f"🧹 Nettoyage backups (garder {args.keep})...")
        deleted, kept = cleanup_old_backups(args.keep, args.dir)

        print(f"\n✅ Nettoyage terminé:")
        print(f"   Supprimés: {deleted}")
        print(f"   Gardés: {kept}")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())

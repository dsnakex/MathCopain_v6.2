#!/usr/bin/env python3
"""
Migration Script: PINs Plaintext → Bcrypt
Convertit tous les PINs stockés en clair vers bcrypt hash

Usage:
    python migrate_pins_to_bcrypt.py [--dry-run] [--input FILE] [--output FILE]

Options:
    --dry-run       Affiche les changements sans les appliquer
    --input FILE    Fichier source (défaut: utilisateurs_securises.json)
    --output FILE   Fichier destination (défaut: même que input)
    --backup        Créer backup avant migration (recommandé)
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Tuple
from core.security import hash_pin, validate_pin_format


def create_backup(filepath: str) -> str:
    """
    Créer backup du fichier avant migration.

    Args:
        filepath: Chemin du fichier à sauvegarder

    Returns:
        Chemin du fichier backup créé
    """
    if not os.path.exists(filepath):
        print(f"⚠️  Fichier {filepath} n'existe pas, backup ignoré")
        return ""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"

    try:
        with open(filepath, 'r', encoding='utf-8') as src:
            data = src.read()

        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(data)

        print(f"✅ Backup créé: {backup_path}")
        return backup_path

    except Exception as e:
        print(f"❌ Erreur création backup: {e}")
        sys.exit(1)


def load_users_file(filepath: str) -> Dict:
    """
    Charger fichier utilisateurs.

    Args:
        filepath: Chemin du fichier JSON

    Returns:
        Données utilisateurs (dict)
    """
    if not os.path.exists(filepath):
        print(f"❌ Fichier {filepath} introuvable")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"❌ Format invalide: attendu dict, reçu {type(data)}")
            sys.exit(1)

        return data

    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        sys.exit(1)


def migrate_user_pins(users_data: Dict, dry_run: bool = False) -> Tuple[Dict, int, int, int]:
    """
    Migrer tous les PINs vers bcrypt.

    Args:
        users_data: Données utilisateurs
        dry_run: Si True, ne modifie pas les données

    Returns:
        (migrated_data, count_migrated, count_skipped, count_errors)
    """
    migrated_data = {}
    count_migrated = 0
    count_skipped = 0
    count_errors = 0

    for username, user_info in users_data.items():
        try:
            if not isinstance(user_info, dict):
                print(f"⚠️  User {username}: format invalide, ignoré")
                count_errors += 1
                continue

            # Vérifier si PIN existe
            if 'pin' not in user_info:
                print(f"⚠️  User {username}: pas de PIN, ignoré")
                count_skipped += 1
                migrated_data[username] = user_info
                continue

            pin = user_info['pin']

            # Détecter si déjà hashé (bcrypt commence par $2b$)
            if isinstance(pin, str) and pin.startswith('$2b$'):
                print(f"⏩ User {username}: PIN déjà hashé, ignoré")
                count_skipped += 1
                migrated_data[username] = user_info
                continue

            # Valider format PIN avant migration
            is_valid, error = validate_pin_format(str(pin))
            if not is_valid:
                print(f"❌ User {username}: PIN invalide ({error}), ignoré")
                count_errors += 1
                migrated_data[username] = user_info
                continue

            # Hasher le PIN
            if not dry_run:
                hashed_pin = hash_pin(str(pin))
                print(f"✅ User {username}: PIN migré ({pin} → bcrypt hash)")
            else:
                hashed_pin = "[DRY-RUN: hash would be generated]"
                print(f"🔍 User {username}: PIN serait migré ({pin} → bcrypt)")

            # Créer nouvelle entrée utilisateur
            migrated_user = user_info.copy()
            migrated_user['pin'] = hashed_pin

            # Ajouter métadonnées migration
            if not dry_run:
                migrated_user['pin_migrated_at'] = datetime.now().isoformat()

            migrated_data[username] = migrated_user
            count_migrated += 1

        except Exception as e:
            print(f"❌ Erreur migration user {username}: {e}")
            count_errors += 1
            migrated_data[username] = user_info

    return migrated_data, count_migrated, count_skipped, count_errors


def save_migrated_data(filepath: str, data: Dict, dry_run: bool = False):
    """
    Sauvegarder données migrées.

    Args:
        filepath: Chemin du fichier destination
        data: Données à sauvegarder
        dry_run: Si True, affiche sans sauvegarder
    """
    if dry_run:
        print("\n🔍 DRY RUN: Données ne seront PAS sauvegardées")
        print(f"   Destination: {filepath}")
        print(f"   {len(data)} utilisateurs seraient écrits")
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Données migrées sauvegardées: {filepath}")

    except Exception as e:
        print(f"\n❌ Erreur sauvegarde: {e}")
        sys.exit(1)


def main():
    """Point d'entrée du script."""
    parser = argparse.ArgumentParser(
        description="Migrer PINs plaintext vers bcrypt"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Afficher changements sans les appliquer'
    )
    parser.add_argument(
        '--input',
        default='utilisateurs_securises.json',
        help='Fichier source (défaut: utilisateurs_securises.json)'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Fichier destination (défaut: même que input)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Ne pas créer de backup (non recommandé)'
    )

    args = parser.parse_args()

    # Déterminer fichiers input/output
    input_file = args.input
    output_file = args.output if args.output else input_file

    print("=" * 60)
    print("🔐 Migration PINs: Plaintext → Bcrypt")
    print("=" * 60)
    print(f"Fichier source:      {input_file}")
    print(f"Fichier destination: {output_file}")
    print(f"Mode dry-run:        {'OUI' if args.dry_run else 'NON'}")
    print(f"Créer backup:        {'NON' if args.no_backup else 'OUI'}")
    print("=" * 60)

    # Créer backup (sauf si dry-run ou --no-backup)
    if not args.dry_run and not args.no_backup:
        print("\n📦 Création backup...")
        create_backup(input_file)

    # Charger données
    print(f"\n📂 Chargement {input_file}...")
    users_data = load_users_file(input_file)
    print(f"✅ {len(users_data)} utilisateurs chargés")

    # Migrer PINs
    print("\n🔄 Migration des PINs...")
    migrated_data, count_migrated, count_skipped, count_errors = migrate_user_pins(
        users_data,
        dry_run=args.dry_run
    )

    # Sauvegarder
    save_migrated_data(output_file, migrated_data, dry_run=args.dry_run)

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ MIGRATION")
    print("=" * 60)
    print(f"✅ PINs migrés:   {count_migrated}")
    print(f"⏩ Déjà hashés:   {count_skipped}")
    print(f"❌ Erreurs:       {count_errors}")
    print(f"📁 Total users:   {len(migrated_data)}")
    print("=" * 60)

    if args.dry_run:
        print("\n🔍 DRY RUN terminé - aucune modification effectuée")
        print("   Pour appliquer les changements, retirez --dry-run")
    else:
        print("\n✅ Migration terminée avec succès !")

        if count_migrated > 0:
            print("\n⚠️  IMPORTANT:")
            print("   1. Vérifiez que l'application fonctionne correctement")
            print("   2. Testez l'authentification des utilisateurs")
            print("   3. Le backup a été créé au cas où")

    return 0


if __name__ == '__main__':
    sys.exit(main())

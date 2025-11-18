"""
Migration script: JSON files → PostgreSQL database
Migrates existing MathCopain data from JSON files to PostgreSQL

Usage:
    python database/migration_scripts/json_to_postgres.py --mode dry-run
    python database/migration_scripts/json_to_postgres.py --mode full
    python database/migration_scripts/json_to_postgres.py --rollback
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from database.connection import get_session, DatabaseSession, init_database
from database.models import User, ExerciseResponse, SkillProfile, AnalyticsEvent


class JSONToPostgresMigration:
    """
    Handles migration from JSON files to PostgreSQL database
    """

    def __init__(self, source_dir: str = ".", backup_dir: str = "./backups"):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

        # JSON files to migrate
        self.json_files = {
            'users': self.source_dir / 'users_data.json',
            'credentials': self.source_dir / 'users_credentials.json',
            'profiles': self.source_dir / 'utilisateurs.json',
        }

    def backup_json_files(self) -> str:
        """
        Create backup of all JSON files

        Returns:
            str: Backup directory path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir(exist_ok=True)

        print(f"📦 Creating backup in: {backup_path}")

        for name, filepath in self.json_files.items():
            if filepath.exists():
                shutil.copy2(filepath, backup_path / filepath.name)
                print(f"  ✓ Backed up: {filepath.name}")
            else:
                print(f"  ⚠️  File not found: {filepath.name}")

        print(f"✓ Backup completed: {backup_path}")
        return str(backup_path)

    def load_json(self, filepath: Path) -> Optional[Dict]:
        """
        Load JSON file with error handling

        Args:
            filepath: Path to JSON file

        Returns:
            Dict or None if file doesn't exist
        """
        if not filepath.exists():
            print(f"⚠️  File not found: {filepath}")
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ Loaded: {filepath.name} ({len(data) if isinstance(data, (list, dict)) else 'unknown'} items)")
            return data
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {filepath}: {e}")
            return None

    def validate_data(self, users_data: Dict, credentials_data: Dict) -> Dict[str, any]:
        """
        Validate data integrity before migration

        Args:
            users_data: User data from users_data.json
            credentials_data: Credentials from users_credentials.json

        Returns:
            Dict with validation results
        """
        print("\n🔍 Validating data...")

        report = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }

        # Check users
        if not users_data:
            report['errors'].append("No user data found")
            report['valid'] = False
            return report

        usernames = list(users_data.keys()) if isinstance(users_data, dict) else []
        report['stats']['total_users'] = len(usernames)

        # Check credentials alignment
        if credentials_data:
            cred_usernames = list(credentials_data.keys()) if isinstance(credentials_data, dict) else []
            if set(usernames) != set(cred_usernames):
                report['warnings'].append("User data and credentials don't match perfectly")

        # Check for required fields
        for username, user_data in (users_data.items() if isinstance(users_data, dict) else []):
            if not isinstance(user_data, dict):
                report['errors'].append(f"Invalid data format for user: {username}")
                report['valid'] = False

        if report['valid']:
            print("✓ Data validation passed")
        else:
            print("❌ Data validation failed")

        return report

    def migrate_users(self, session, users_data: Dict, credentials_data: Dict) -> Dict[str, int]:
        """
        Migrate users to PostgreSQL

        Args:
            session: Database session
            users_data: User profiles data
            credentials_data: User credentials data

        Returns:
            Dict mapping username → user_id
        """
        print("\n👥 Migrating users...")

        user_id_map = {}
        created_count = 0

        for username, user_data in (users_data.items() if isinstance(users_data, dict) else []):
            try:
                # Get PIN hash from credentials
                pin_hash = ""
                if credentials_data and username in credentials_data:
                    cred = credentials_data[username]
                    pin_hash = cred.get('pin_hash', '') or cred.get('hashed_pin', '')

                # Create user
                user = User(
                    username=username,
                    pin_hash=pin_hash,
                    learning_style=user_data.get('learning_style'),
                    grade_level=user_data.get('grade_level') or user_data.get('niveau'),
                    created_at=datetime.now(),
                    is_active=True
                )

                session.add(user)
                session.flush()  # Get user.id

                user_id_map[username] = user.id
                created_count += 1

                print(f"  ✓ Created user: {username} (ID: {user.id})")

            except Exception as e:
                print(f"  ❌ Failed to create user {username}: {e}")

        print(f"✓ Migrated {created_count} users")
        return user_id_map

    def migrate_skill_profiles(self, session, user_id_map: Dict[str, int], users_data: Dict) -> int:
        """
        Migrate skill profiles to PostgreSQL

        Args:
            session: Database session
            user_id_map: Mapping username → user_id
            users_data: User data with skill tracking

        Returns:
            int: Number of profiles created
        """
        print("\n📊 Migrating skill profiles...")

        created_count = 0

        for username, user_data in (users_data.items() if isinstance(users_data, dict) else []):
            if username not in user_id_map:
                continue

            user_id = user_id_map[username]

            # Get skill tracking data
            skill_tracking = user_data.get('skill_tracking', {})

            for domain, domain_data in skill_tracking.items():
                try:
                    if isinstance(domain_data, dict):
                        proficiency = domain_data.get('level', 0.0)
                        exercises_done = domain_data.get('exercises_done', 0)
                        success_rate = domain_data.get('success_rate', 0.0)

                        profile = SkillProfile(
                            user_id=user_id,
                            skill_domain=domain,
                            proficiency_level=min(1.0, max(0.0, proficiency)),
                            exercises_completed=exercises_done,
                            success_rate=success_rate,
                            last_practiced=datetime.now() if exercises_done > 0 else None
                        )

                        session.add(profile)
                        created_count += 1

                except Exception as e:
                    print(f"  ❌ Failed to create profile for {username}/{domain}: {e}")

        print(f"✓ Migrated {created_count} skill profiles")
        return created_count

    def migrate_analytics_events(self, session, user_id_map: Dict[str, int]) -> int:
        """
        Create initial analytics events for existing users

        Args:
            session: Database session
            user_id_map: Mapping username → user_id

        Returns:
            int: Number of events created
        """
        print("\n📈 Creating analytics events...")

        created_count = 0

        for username, user_id in user_id_map.items():
            try:
                # Create account_created event
                event = AnalyticsEvent(
                    user_id=user_id,
                    event_type='account_created',
                    event_data={'source': 'migration', 'migrated_from': 'json'},
                    created_at=datetime.now()
                )
                session.add(event)
                created_count += 1

            except Exception as e:
                print(f"  ❌ Failed to create event for {username}: {e}")

        print(f"✓ Created {created_count} analytics events")
        return created_count

    def run_migration(self, mode: str = 'dry-run') -> bool:
        """
        Execute migration

        Args:
            mode: 'dry-run' or 'full'

        Returns:
            bool: True if successful
        """
        print("=" * 60)
        print(f"🚀 MATHCOPAIN JSON → PostgreSQL MIGRATION")
        print(f"Mode: {mode.upper()}")
        print("=" * 60)

        # Step 1: Backup
        if mode == 'full':
            backup_path = self.backup_json_files()
            print(f"\n✓ Backup created: {backup_path}")

        # Step 2: Load JSON data
        print("\n📂 Loading JSON files...")
        users_data = self.load_json(self.json_files['users'])
        credentials_data = self.load_json(self.json_files['credentials'])

        if not users_data:
            print("❌ No user data found. Aborting migration.")
            return False

        # Step 3: Validate
        validation_report = self.validate_data(users_data, credentials_data)

        if not validation_report['valid']:
            print(f"\n❌ Validation failed:")
            for error in validation_report['errors']:
                print(f"  - {error}")
            return False

        print(f"\n📊 Migration Statistics:")
        for key, value in validation_report['stats'].items():
            print(f"  {key}: {value}")

        # Step 4: Dry-run mode
        if mode == 'dry-run':
            print("\n" + "=" * 60)
            print("DRY-RUN MODE - No data will be written to database")
            print("=" * 60)
            print(f"Would migrate:")
            print(f"  - {validation_report['stats']['total_users']} users")
            print(f"  - ~{validation_report['stats']['total_users'] * 10} skill profiles (estimated)")
            print(f"  - ~{validation_report['stats']['total_users']} analytics events")
            print("\nRun with --mode full to execute migration")
            return True

        # Step 5: Execute migration (full mode)
        print("\n" + "=" * 60)
        print("EXECUTING FULL MIGRATION")
        print("=" * 60)

        try:
            with DatabaseSession() as session:
                # Migrate users
                user_id_map = self.migrate_users(session, users_data, credentials_data)

                # Migrate skill profiles
                self.migrate_skill_profiles(session, user_id_map, users_data)

                # Create analytics events
                self.migrate_analytics_events(session, user_id_map)

                # Commit is automatic via DatabaseSession context manager

            print("\n" + "=" * 60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            return True

        except SQLAlchemyError as e:
            print(f"\n❌ Migration failed: {e}")
            print("Database changes have been rolled back")
            return False

    def rollback(self, backup_path: str):
        """
        Restore JSON files from backup

        Args:
            backup_path: Path to backup directory
        """
        print(f"\n🔄 Rolling back from: {backup_path}")

        backup_dir = Path(backup_path)

        if not backup_dir.exists():
            print(f"❌ Backup directory not found: {backup_path}")
            return

        for name, filepath in self.json_files.items():
            backup_file = backup_dir / filepath.name

            if backup_file.exists():
                shutil.copy2(backup_file, filepath)
                print(f"  ✓ Restored: {filepath.name}")
            else:
                print(f"  ⚠️  Backup not found: {backup_file.name}")

        print("✓ Rollback completed")


def main():
    parser = argparse.ArgumentParser(description='Migrate MathCopain data from JSON to PostgreSQL')
    parser.add_argument(
        '--mode',
        choices=['dry-run', 'full'],
        default='dry-run',
        help='Migration mode: dry-run (validate only) or full (execute migration)'
    )
    parser.add_argument(
        '--rollback',
        type=str,
        help='Rollback to backup directory'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database tables before migration'
    )

    args = parser.parse_args()

    migrator = JSONToPostgresMigration()

    # Rollback mode
    if args.rollback:
        migrator.rollback(args.rollback)
        return

    # Initialize database if requested
    if args.init_db:
        print("Initializing database tables...")
        init_database(drop_all=False, echo=False)
        print()

    # Run migration
    success = migrator.run_migration(mode=args.mode)

    if not success:
        print("\n⚠️  Migration encountered errors")
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()

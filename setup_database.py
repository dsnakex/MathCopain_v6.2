#!/usr/bin/env python3
"""
Database Setup Script for MathCopain
Initializes PostgreSQL database or falls back to SQLite for local development
"""

import os
import sys
from pathlib import Path

def check_postgresql():
    """Check if PostgreSQL is available and running"""
    import subprocess
    try:
        result = subprocess.run(
            ['psql', '-U', 'postgres', '-c', 'SELECT version();'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def setup_postgresql():
    """Setup PostgreSQL database"""
    import subprocess

    print("=" * 70)
    print("POSTGRESQL SETUP")
    print("=" * 70)

    db_name = os.getenv('DB_NAME', 'mathcopain')
    db_user = os.getenv('DB_USER', 'mathcopain_user')
    db_password = os.getenv('DB_PASSWORD', 'mathcopain_password')

    print(f"\n📋 Configuration:")
    print(f"  - Database: {db_name}")
    print(f"  - User: {db_user}")
    print(f"  - Password: {db_password}")

    # SQL commands to create database and user
    commands = [
        # Create user if not exists
        f"CREATE USER {db_user} WITH PASSWORD '{db_password}';",
        # Create database
        f"CREATE DATABASE {db_name} OWNER {db_user};",
        # Grant privileges
        f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
    ]

    print("\n🔧 Creating database and user...")

    for cmd in commands:
        try:
            result = subprocess.run(
                ['psql', '-U', 'postgres', '-c', cmd],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print(f"  ✓ {cmd.split()[0]} successful")
            else:
                # Check if error is because object already exists
                if "already exists" in result.stderr:
                    print(f"  ℹ {cmd.split()[0]} - already exists (OK)")
                else:
                    print(f"  ✗ {cmd.split()[0]} failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            print(f"  ✗ Command timeout")
            return False
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return False

    print("\n✅ PostgreSQL database setup complete!")
    return True


def create_tables():
    """Create database tables using SQLAlchemy"""
    print("\n" + "=" * 70)
    print("CREATING TABLES")
    print("=" * 70)

    try:
        from database.connection import init_database

        print("\n🔧 Initializing database tables...")
        init_database(drop_all=False, echo=False)
        print("✅ Tables created successfully!")
        return True

    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def seed_test_data():
    """Load test data"""
    print("\n" + "=" * 70)
    print("SEEDING TEST DATA")
    print("=" * 70)

    import subprocess

    try:
        print("\n🌱 Loading test data...")
        result = subprocess.run(
            [sys.executable, '-m', 'tests.seed_data'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print(result.stdout)
            print("✅ Test data loaded successfully!")
            return True
        else:
            print(f"❌ Error loading test data:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout loading test data")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def setup_sqlite_alternative():
    """Setup SQLite as alternative for local development"""
    print("\n" + "=" * 70)
    print("SQLITE ALTERNATIVE SETUP")
    print("=" * 70)

    print("""
⚠️  PostgreSQL n'est pas disponible.

Pour utiliser PostgreSQL, vous devez :

1. Installer PostgreSQL :
   sudo apt-get install postgresql postgresql-contrib

2. Démarrer le service :
   sudo service postgresql start

3. Relancer ce script

Pour l'instant, vous pouvez utiliser les données de test existantes
dans le système de fichiers JSON (utilisateur.py).
""")

    return False


def main():
    """Main setup function"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║            🎓 MathCopain Database Setup v6.4                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    # Check if PostgreSQL is available
    print("🔍 Checking PostgreSQL availability...")

    if check_postgresql():
        print("✅ PostgreSQL is available!\n")

        # Setup PostgreSQL
        if setup_postgresql():
            # Create tables
            if create_tables():
                # Load test data
                seed_test_data()

                print("\n" + "=" * 70)
                print("✅ DATABASE SETUP COMPLETE!")
                print("=" * 70)
                print("\n📋 Next steps:")
                print("  1. Start the Streamlit app: streamlit run app.py")
                print("  2. Start the API: python -m api.app")
                print("  3. Login with test account: voir tests/README.md")
                print("")
                return True
    else:
        print("❌ PostgreSQL is not available or not running\n")
        setup_sqlite_alternative()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Supabase Client for MathCopain
Provides persistent storage for user data on Streamlit Cloud.

Setup:
1. Create a free account at https://supabase.com
2. Create a new project
3. Run the SQL in create_tables.sql to create the required tables
4. Add your credentials to Streamlit secrets or .env file
"""

import os
import streamlit as st
from typing import Dict, Optional, Any
import json

# Try to import supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None


def get_supabase_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    Get Supabase credentials from Streamlit secrets or environment variables.

    Priority:
    1. Streamlit secrets (for Streamlit Cloud)
    2. Environment variables (for local development)

    Returns:
        (url, key) tuple or (None, None) if not configured
    """
    url = None
    key = None

    # Try Streamlit secrets first (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets') and 'supabase' in st.secrets:
            url = st.secrets['supabase'].get('url')
            key = st.secrets['supabase'].get('key')
    except Exception:
        pass

    # Fallback to environment variables
    if not url:
        url = os.getenv('SUPABASE_URL')
    if not key:
        key = os.getenv('SUPABASE_KEY')

    return url, key


@st.cache_resource
def get_supabase_client() -> Optional[Client]:
    """
    Get cached Supabase client instance.
    Returns None if Supabase is not configured.
    """
    if not SUPABASE_AVAILABLE:
        return None

    url, key = get_supabase_credentials()

    if not url or not key:
        return None

    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        print(f"[Supabase] Connection error: {e}")
        return None


def is_supabase_configured() -> bool:
    """Check if Supabase is properly configured and available."""
    return get_supabase_client() is not None


# =============================================================================
# USER PROFILES TABLE OPERATIONS
# =============================================================================

def supabase_get_user_profile(username: str) -> Optional[Dict]:
    """
    Get user profile from Supabase.

    Args:
        username: Username (lowercase key)

    Returns:
        Profile dict or None if not found
    """
    client = get_supabase_client()
    if not client:
        return None

    try:
        response = client.table('user_profiles').select('*').eq('username', username).execute()

        if response.data and len(response.data) > 0:
            row = response.data[0]
            return row.get('profile_data')
        return None
    except Exception as e:
        print(f"[Supabase] Error getting profile: {e}")
        return None


def supabase_save_user_profile(username: str, profile: Dict) -> bool:
    """
    Save user profile to Supabase (upsert).

    Args:
        username: Username (lowercase key)
        profile: Profile data dict

    Returns:
        True if successful
    """
    client = get_supabase_client()
    if not client:
        return False

    try:
        data = {
            'username': username,
            'profile_data': profile,
            'updated_at': 'now()'
        }

        client.table('user_profiles').upsert(data, on_conflict='username').execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error saving profile: {e}")
        return False


def supabase_get_all_usernames() -> list:
    """
    Get all usernames from Supabase.

    Returns:
        List of usernames
    """
    client = get_supabase_client()
    if not client:
        return []

    try:
        response = client.table('user_profiles').select('username').execute()
        return [row['username'] for row in response.data]
    except Exception as e:
        print(f"[Supabase] Error getting usernames: {e}")
        return []


def supabase_delete_user_profile(username: str) -> bool:
    """Delete user profile from Supabase."""
    client = get_supabase_client()
    if not client:
        return False

    try:
        client.table('user_profiles').delete().eq('username', username).execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error deleting profile: {e}")
        return False


# =============================================================================
# USER CREDENTIALS TABLE OPERATIONS
# =============================================================================

def supabase_get_user_credentials(username: str) -> Optional[Dict]:
    """
    Get user credentials from Supabase.

    Args:
        username: Username (lowercase key)

    Returns:
        Credentials dict or None if not found
    """
    client = get_supabase_client()
    if not client:
        return None

    try:
        response = client.table('user_credentials').select('*').eq('username', username).execute()

        if response.data and len(response.data) > 0:
            row = response.data[0]
            return {
                'pin': row.get('pin_hash'),
                'prenom_affichage': row.get('display_name'),
                'question_secrete': row.get('secret_question'),
                'code_recuperation': row.get('recovery_code'),
                'profil': row.get('profile_data', {})
            }
        return None
    except Exception as e:
        print(f"[Supabase] Error getting credentials: {e}")
        return None


def supabase_save_user_credentials(username: str, credentials: Dict) -> bool:
    """
    Save user credentials to Supabase (upsert).

    Args:
        username: Username (lowercase key)
        credentials: Credentials dict with pin, prenom_affichage, etc.

    Returns:
        True if successful
    """
    client = get_supabase_client()
    if not client:
        return False

    try:
        data = {
            'username': username,
            'pin_hash': credentials.get('pin'),
            'display_name': credentials.get('prenom_affichage'),
            'secret_question': credentials.get('question_secrete'),
            'recovery_code': credentials.get('code_recuperation'),
            'profile_data': credentials.get('profil', {}),
            'updated_at': 'now()'
        }

        client.table('user_credentials').upsert(data, on_conflict='username').execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error saving credentials: {e}")
        return False


def supabase_get_all_credentials() -> Dict[str, Dict]:
    """
    Get all user credentials from Supabase.

    Returns:
        Dict mapping username to credentials
    """
    client = get_supabase_client()
    if not client:
        return {}

    try:
        response = client.table('user_credentials').select('*').execute()

        result = {}
        for row in response.data:
            username = row['username']
            result[username] = {
                'pin': row.get('pin_hash'),
                'prenom_affichage': row.get('display_name'),
                'question_secrete': row.get('secret_question'),
                'code_recuperation': row.get('recovery_code'),
                'profil': row.get('profile_data', {})
            }
        return result
    except Exception as e:
        print(f"[Supabase] Error getting all credentials: {e}")
        return {}


def supabase_delete_user_credentials(username: str) -> bool:
    """Delete user credentials from Supabase."""
    client = get_supabase_client()
    if not client:
        return False

    try:
        client.table('user_credentials').delete().eq('username', username).execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error deleting credentials: {e}")
        return False


def supabase_user_exists(username: str) -> bool:
    """Check if user exists in Supabase."""
    client = get_supabase_client()
    if not client:
        return False

    try:
        response = client.table('user_credentials').select('username').eq('username', username).execute()
        return len(response.data) > 0
    except Exception:
        return False


# =============================================================================
# SQL SETUP SCRIPT (for reference)
# =============================================================================

SUPABASE_SETUP_SQL = """
-- Run this in your Supabase SQL Editor to create the required tables

-- User credentials table (for authentication)
CREATE TABLE IF NOT EXISTS user_credentials (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pin_hash TEXT NOT NULL,
    display_name VARCHAR(100),
    secret_question JSONB,
    recovery_code VARCHAR(10),
    profile_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User profiles table (for progress data)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    profile_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_credentials_username ON user_credentials(username);
CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE user_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust as needed for your security requirements)
CREATE POLICY "Allow all operations" ON user_credentials FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON user_profiles FOR ALL USING (true);
"""


def print_setup_instructions():
    """Print setup instructions for Supabase."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    SUPABASE SETUP INSTRUCTIONS                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  1. Go to https://supabase.com and create a free account         ║
║                                                                  ║
║  2. Create a new project (choose a region close to you)          ║
║                                                                  ║
║  3. Go to SQL Editor and run the SQL from:                       ║
║     core/supabase_setup.sql                                      ║
║                                                                  ║
║  4. Go to Settings > API to get your credentials:                ║
║     - Project URL                                                ║
║     - anon/public key                                            ║
║                                                                  ║
║  5. Add credentials to Streamlit Cloud:                          ║
║     Go to your app settings > Secrets and add:                   ║
║                                                                  ║
║     [supabase]                                                   ║
║     url = "https://xxxxx.supabase.co"                            ║
║     key = "your-anon-key"                                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

-- ============================================================================
-- SUPABASE SETUP SQL FOR MATHCOPAIN
-- Run this in your Supabase SQL Editor (https://supabase.com/dashboard)
-- ============================================================================

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

-- User profiles table (for progress data - backup/sync)
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

-- Enable Row Level Security
ALTER TABLE user_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (the app handles auth internally)
DROP POLICY IF EXISTS "Allow all operations on credentials" ON user_credentials;
DROP POLICY IF EXISTS "Allow all operations on profiles" ON user_profiles;

CREATE POLICY "Allow all operations on credentials" ON user_credentials FOR ALL USING (true);
CREATE POLICY "Allow all operations on profiles" ON user_profiles FOR ALL USING (true);

-- ============================================================================
-- VERIFICATION: Check tables were created
-- ============================================================================
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

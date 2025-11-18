-- Initialization script for MathCopain PostgreSQL database
-- This script runs automatically when the database is first created

-- Set timezone
SET timezone = 'UTC';

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for performance (additional to model indexes)
-- These will be created by Alembic migrations, but can be run manually if needed

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE mathcopain TO mathcopain_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mathcopain_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mathcopain_user;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'MathCopain database initialized successfully';
END $$;

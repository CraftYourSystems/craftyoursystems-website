-- ============================================================
--  setup.sql — Run once to create the database + tables
--
--  How to run:
--  psql -U postgres -f setup.sql
-- ============================================================

-- 1. Create the database
CREATE DATABASE craftyoursystems;

-- 2. Connect to it
\c craftyoursystems

-- 3. Users table
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Messages table
CREATE TABLE IF NOT EXISTS messages (
    id         SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    subject    TEXT NOT NULL,
    message    TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Index for fast email lookups
CREATE INDEX IF NOT EXISTS idx_messages_user_email ON messages(user_email);

-- Verify
\dt

-- ── Useful dev commands ──────────────────────────────────────
-- See users:    SELECT id, email, created_at FROM users;
-- See messages: SELECT * FROM messages ORDER BY created_at DESC;
-- Clear test data: TRUNCATE users, messages RESTART IDENTITY;

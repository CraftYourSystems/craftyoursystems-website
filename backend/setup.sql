-- ============================================================
--  setup.sql — Run this ONCE to set up your database
--
--  How to run:
--  psql -U postgres -f setup.sql
--  OR paste each command into the psql shell
-- ============================================================

-- 1. Create the database (run as the postgres superuser)
CREATE DATABASE craftyoursystems;

-- 2. Connect to it
\c craftyoursystems

-- 3. Create the users table
--    SERIAL = auto-incrementing integer (1, 2, 3, ...)
--    UNIQUE = no two rows can have the same email
--    NOT NULL = this field must always have a value
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Create the messages table
CREATE TABLE IF NOT EXISTS messages (
    id         SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    subject    TEXT NOT NULL,
    message    TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. (Optional) Add an index so looking up messages by email is fast
CREATE INDEX IF NOT EXISTS idx_messages_user_email ON messages(user_email);

-- 6. Verify — you should see both tables listed
\dt

-- ============================================================
--  Useful commands while developing:
--
--  See all users:    SELECT id, email, created_at FROM users;
--  See all messages: SELECT * FROM messages ORDER BY created_at DESC;
--  Delete a user:    DELETE FROM users WHERE email = 'test@test.com';
--  Clear messages:   TRUNCATE TABLE messages;
-- ============================================================

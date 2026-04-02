# ============================================================
#  db/database.py — Database connection + table creation
#
#  PostgreSQL is the database. We use psycopg2 to talk to it
#  from Python. Think of psycopg2 as a "translator" between
#  Python and PostgreSQL.
# ============================================================

import psycopg2
import psycopg2.extras  # lets us get results as dicts (name: value)
import os

def get_connection():
    """
    Opens a fresh connection to PostgreSQL.

    We read the connection string from the environment so
    passwords are never hard-coded in source code.

    DATABASE_URL format:
    postgresql://username:password@host:port/database_name
    """
    return psycopg2.connect(os.getenv('DATABASE_URL'))


def init_db():
    """
    Creates the two tables we need — runs at startup.
    'IF NOT EXISTS' means it's safe to run multiple times;
    it won't wipe data if the tables already exist.

    TABLE: users
    ─────────────────────────────────────────────────────────
    id            → auto-incrementing unique number
    email         → must be unique, used to log in
    password_hash → we NEVER store the real password,
                    only the hashed version (Werkzeug does this)
    created_at    → timestamp set automatically

    TABLE: messages
    ─────────────────────────────────────────────────────────
    id         → auto-incrementing unique number
    user_email → which user sent the message (foreign key)
    subject    → form subject line
    message    → form body text
    created_at → timestamp set automatically
    """
    conn = get_connection()
    cur  = conn.cursor()

    # ----- users table -----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            SERIAL PRIMARY KEY,
            email         VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    # ----- messages table -----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         SERIAL PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            subject    TEXT NOT NULL,
            message    TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    conn.commit()   # save the changes
    cur.close()
    conn.close()
    print("✅ Database tables ready.")

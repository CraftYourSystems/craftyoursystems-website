# ============================================================
#  db/database.py — PostgreSQL connection + table creation
#
#  ═══════════════════════════════════════════════════════════
#  HOW THE DATABASE CONNECTION WORKS
#  ═══════════════════════════════════════════════════════════
#
#  psycopg2 is a "driver" — it speaks the PostgreSQL wire
#  protocol so Python can send SQL and receive results.
#
#  CONNECTION STRING FORMAT:
#  postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
#  postgresql://postgres:pass123@localhost:5432/craftyoursystems
#                ↑user  ↑password ↑server  ↑port ↑db name
#
#  get_db() is a FastAPI "dependency":
#  ─────────────────────────────────────────────────────────
#  Instead of opening/closing connections manually in every
#  route, you declare it as a parameter and FastAPI handles it:
#
#    @app.post("/route")
#    def my_route(db = Depends(get_db)):
#        cur = db.cursor()
#        ...
#
#  The 'yield' makes it a context manager:
#  - Code BEFORE yield: runs before the route (opens connection)
#  - Code AFTER yield:  runs after the route (closes connection)
#  This guarantees connections are always closed even on errors.
# ============================================================

import psycopg2
import psycopg2.extras
from cys_fastapi.core.config import settings

def get_connection():
    """Opens a fresh PostgreSQL connection using DATABASE_URL from .env"""
    return psycopg2.connect(settings.DATABASE_URL)

def get_db():
    """
    FastAPI dependency that provides a DB connection per request.
    'yield' means FastAPI will call this like a context manager —
    it pauses here during the request, then resumes to close the DB.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()  # always runs, even if the route throws an error

def init_db():
    """
    Creates tables at server startup if they don't exist.
    Safe to run multiple times — won't wipe existing data.
    """
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            SERIAL PRIMARY KEY,
            email         VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         SERIAL PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            subject    TEXT NOT NULL,
            message    TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    # Index: makes "SELECT ... WHERE user_email = ?" queries much faster
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_email
        ON messages(user_email);
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database tables ready.")

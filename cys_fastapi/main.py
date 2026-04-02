# ============================================================
#  main.py — FastAPI entry point
#
#  FastAPI vs Flask:
#  ─────────────────
#  Flask  → older, manually write everything, no type hints
#  FastAPI → modern, automatic docs, type-safe, async-ready
#
#  The BIGGEST visible difference:
#  Flask:   @app.route('/path', methods=['POST'])
#  FastAPI: @app.post('/path')
#
#  FastAPI auto-generates an interactive docs page at:
#  http://localhost:8000/docs  ← you can test every route here!
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="cys_fastapi/.env")  # reads your .env file

# Import route routers (equivalent to Flask Blueprints)
from cys_fastapi.routes.auth import router as auth_router
from cys_fastapi.routes.form import router as form_router
from cys_fastapi.db.database import init_db
# ── Lifespan: runs on startup and shutdown ──────────────────
# This replaces Flask's @app.before_first_request pattern.
# 'yield' separates startup code (before) from shutdown code (after).
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Initialising database tables...")
    init_db()
    print("🚀 CraftYourSystems API is ready!")
    yield  # ← server runs while paused here
    print("🛑 Shutting down...")

# ── Create the FastAPI app ──────────────────────────────────
app = FastAPI(
    title       = "CraftYourSystems API",
    description = "Backend for the CraftYourSystems portfolio site",
    version     = "2.0.0",
    lifespan    = lifespan
)

# ── CORS middleware ─────────────────────────────────────────
# Allows your HTML frontend to call this API from a browser.
# In production: replace ["*"] with ["https://craftyoursystems.in"]
app.add_middleware(
    CORSMiddleware,
    allow_origins     = [os.getenv("ALLOWED_ORIGIN", "*")],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Register routers ────────────────────────────────────────
# prefix="/auth" means /signup becomes /auth/signup
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(form_router, tags=["Form"])

# ── Health check ────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "CraftYourSystems API is running ✅"}

# ============================================================
#  app.py — Main entry point for the CraftYourSystems backend
#  Think of this as the "front door" of the whole server.
#  It wires together the database, routes, and settings.
# ============================================================

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load all the secret values from your .env file
# (passwords, keys, etc.) into the environment
load_dotenv()

# Import our route blueprints (separate files for auth + form)
from routes.auth import auth_bp
from routes.form import form_bp
from db.database import init_db

# ----------------------------------------------------------
# Create the Flask application
# ----------------------------------------------------------
app = Flask(__name__)

# Secret key used to sign JWT tokens — comes from .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-dev-key-change-this')

# CORS = Cross-Origin Resource Sharing
# This allows your HTML frontend (running on a different port
# or domain) to talk to this backend without being blocked.
# In production, replace "*" with your actual domain.
CORS(app, resources={r"/*": {"origins": os.getenv('ALLOWED_ORIGIN', '*')}})

# ----------------------------------------------------------
# Register route blueprints
# /auth/signup  → handles registration
# /auth/login   → handles login + JWT generation
# /submit-form  → protected route (JWT required)
# ----------------------------------------------------------
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(form_bp)

# ----------------------------------------------------------
# Health check — visit http://localhost:5000/ to confirm
# the server is running
# ----------------------------------------------------------
@app.route('/')
def health():
    return {'status': 'CraftYourSystems API is running ✅'}, 200

# ----------------------------------------------------------
# Startup: initialise the database tables if they don't exist
# ----------------------------------------------------------
if __name__ == '__main__':
    print("🔧 Initialising database tables...")
    init_db()
    print("🚀 Starting Flask server on port 5000...")
    # debug=True auto-reloads on code changes (dev only!)
    app.run(debug=True, port=5000)

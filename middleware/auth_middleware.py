# ============================================================
#  middleware/auth_middleware.py — JWT verification
#
#  JWT = JSON Web Token.  Think of it like a stamped wristband
#  at a concert. You get it once (on login) and you show it
#  every time you enter a protected area (protected routes).
#
#  Structure of a JWT:
#  HEADER.PAYLOAD.SIGNATURE
#  ↑ algorithm  ↑ user data  ↑ tamper-proof seal
#
#  We sign tokens with SECRET_KEY so nobody can fake one.
# ============================================================

import jwt
import os
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timezone

def token_required(f):
    """
    A Python DECORATOR — you put @token_required above any
    route function to protect it.

    What it does step by step:
    1. Reads the Authorization header from the request
    2. Extracts the token (format: "Bearer <token>")
    3. Verifies the signature using SECRET_KEY
    4. Checks it hasn't expired (we set 1-hour expiry on login)
    5. If all good → calls the real route function
       If anything fails → returns a 401 Unauthorized error
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        # ── Step 1: Find the Authorization header ──────────
        auth_header = request.headers.get('Authorization', '')

        if not auth_header:
            return jsonify({'message': 'Authorization header missing'}), 401

        # ── Step 2: Extract the token ───────────────────────
        # Header looks like: "Bearer eyJhbGci..."
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({'message': 'Invalid Authorization format. Use: Bearer <token>'}), 401

        token = parts[1]

        # ── Step 3 & 4: Decode + verify ─────────────────────
        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']   # HS256 = HMAC with SHA-256
            )
            # payload now contains: { 'email': '...', 'exp': ... }

        except jwt.ExpiredSignatureError:
            # Token is valid but older than 1 hour
            return jsonify({'message': 'Token has expired. Please log in again.'}), 401

        except jwt.InvalidTokenError:
            # Token was tampered with or just garbage
            return jsonify({'message': 'Invalid token.'}), 401

        # ── Step 5: Pass user info into the route function ──
        # The route can now access current_user['email']
        return f(current_user=payload, *args, **kwargs)

    return decorated

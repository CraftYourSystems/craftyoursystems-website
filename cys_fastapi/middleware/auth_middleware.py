# ============================================================
#  middleware/auth_middleware.py — JWT dependency for FastAPI
#
#  ═══════════════════════════════════════════════════════════
#  FLASK vs FASTAPI: How route protection works differently
#  ═══════════════════════════════════════════════════════════
#
#  FLASK approach (decorator):
#  ─────────────────────────────
#  @app.route('/submit-form', methods=['POST'])
#  @token_required          ← custom decorator you wrote
#  def submit_form(current_user):
#      ...
#
#  FASTAPI approach (Depends):
#  ─────────────────────────────
#  @app.post('/submit-form')
#  def submit_form(current_user: str = Depends(get_current_user)):
#      ...
#
#  Both do the same thing — verify JWT before running the route.
#  FastAPI's way is cleaner:
#  ✅ No decorator magic
#  ✅ FastAPI auto-shows "requires auth" in /docs
#  ✅ Type-safe: current_user is just a string (email)
#  ✅ Testable: you can swap out get_current_user in tests
#
#  ═══════════════════════════════════════════════════════════
#  WHAT HTTPBearer DOES
#  ═══════════════════════════════════════════════════════════
#  HTTPBearer() reads the Authorization header automatically.
#  It expects: "Authorization: Bearer eyJhbGci..."
#  It returns an HTTPAuthorizationCredentials object with
#  .credentials = the raw token string.
#
#  If the header is missing or malformed, it returns 403
#  before your code even runs.
# ============================================================

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from cys_fastapi.core.security import decode_access_token

# HTTPBearer reads and validates the Authorization: Bearer header
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    """
    FastAPI dependency — extracts and verifies the JWT.

    Returns the user's email (from the token's 'sub' field).
    Raises HTTP 401 if token is missing, expired, or invalid.

    Usage in any route:
        current_user: str = Depends(get_current_user)
    Then current_user is just the email string, e.g. "sam@gmail.com"
    """
    token = credentials.credentials  # the raw JWT string

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail      = "Token payload is missing user info."
            )
        return email  # this becomes current_user in the route

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Token has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Invalid token."
        )

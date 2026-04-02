# ============================================================
#  core/schemas.py — Pydantic models (request + response shapes)
#
#  ═══════════════════════════════════════════════════════════
#  WHY PYDANTIC? (Flask had none of this)
#  ═══════════════════════════════════════════════════════════
#
#  In Flask you did: data = request.get_json() and then
#  manually checked if 'email' in data, etc.
#
#  FastAPI + Pydantic does this automatically:
#  1. Defines the SHAPE of request body as a Python class
#  2. FastAPI reads the JSON body and validates it
#  3. If 'email' is missing → automatic 422 error with clear message
#  4. If 'email' is not a valid email string → automatic error
#  5. You get a typed object, not a raw dict
#
#  Example:
#  POST /auth/signup with body {"email": "test@test.com", "password": "abc"}
#  FastAPI calls SignupRequest(email="test@test.com", password="abc")
#  You get: data.email, data.password — type-safe, validated!
#
#  EmailStr validates it's actually an email format.
#  Field(min_length=6) rejects short passwords automatically.
# ============================================================

from pydantic import BaseModel, EmailStr, Field

# ── AUTH SCHEMAS ─────────────────────────────────────────────

class SignupRequest(BaseModel):
    """Body expected for POST /auth/signup"""
    email   : EmailStr          # validates it's a real email format
    password: str = Field(min_length=6, description="Minimum 6 characters")

class LoginRequest(BaseModel):
    """Body expected for POST /auth/login"""
    email   : EmailStr
    password: str

class TokenResponse(BaseModel):
    """What /auth/login returns on success"""
    token: str
    email: str

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

# ── FORM SCHEMAS ─────────────────────────────────────────────

class FormRequest(BaseModel):
    """Body expected for POST /submit-form"""
    subject: str = Field(min_length=1,  max_length=300)
    message: str = Field(min_length=10, max_length=5000)

class FormResponse(BaseModel):
    """What /submit-form returns on success"""
    message   : str
    message_id: int
    created_at: str
    email     : str

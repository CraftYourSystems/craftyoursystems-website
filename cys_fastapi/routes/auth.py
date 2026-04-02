# ============================================================
#  routes/auth.py — Signup + Login routes
#
#  FLASK vs FASTAPI route comparison:
#  ─────────────────────────────────────────────────────────
#  Flask:
#    @auth_bp.route('/signup', methods=['POST'])
#    def signup():
#        data = request.get_json()
#        email = data.get('email')
#        ...
#
#  FastAPI:
#    @router.post('/signup', response_model=MessageResponse)
#    def signup(data: SignupRequest):  ← body auto-parsed + validated
#        email = data.email
#        ...
#
#  FastAPI also declares the RESPONSE shape (response_model).
#  This means /docs shows exactly what the route returns.
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.errors import UniqueViolation
from cys_fastapi.core.schemas import SignupRequest, LoginRequest, TokenResponse, MessageResponse
from cys_fastapi.core.security import hash_password, verify_password, create_access_token
from cys_fastapi.db.database import get_db

# APIRouter = Flask's Blueprint equivalent
router = APIRouter()

# ── POST /auth/signup ────────────────────────────────────────
@router.post(
    "/signup",
    response_model = MessageResponse,   # tells docs: returns {"message": "..."}
    status_code    = status.HTTP_201_CREATED
)
def signup(data: SignupRequest, db=Depends(get_db)):
    """
    data: SignupRequest  ← FastAPI automatically reads + validates JSON body
    db: Depends(get_db)  ← FastAPI injects a DB connection (from db/database.py)

    Steps:
    1. Hash the password (bcrypt)
    2. Try to insert into users table
    3. If email exists → 409 Conflict
    """
    hashed = hash_password(data.password)

    cur = db.cursor()
    try:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (data.email.lower(), hashed)
        )
        db.commit()
        return {"message": "Account created successfully!"}

    except UniqueViolation:
        # psycopg2 raises this specific exception for UNIQUE constraint failures
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail      = "An account with this email already exists."
        )
    except Exception as e:
        db.rollback()
        print(f"[SIGNUP ERROR] {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail      = "Server error. Please try again."
        )
    finally:
        cur.close()

# ── POST /auth/login ─────────────────────────────────────────
@router.post(
    "/login",
    response_model = TokenResponse   # returns {"token": "...", "email": "..."}
)
def login(data: LoginRequest, db=Depends(get_db)):
    """
    Steps:
    1. Look up user by email
    2. Verify password against stored hash
    3. Generate JWT token (valid 1 hour)
    4. Return token to frontend
    """
    cur = db.cursor()
    try:
        cur.execute(
            "SELECT email, password_hash FROM users WHERE email = %s",
            (data.email.lower(),)
        )
        user = cur.fetchone()  # (email, password_hash) or None

    except Exception as e:
        print(f"[LOGIN DB ERROR] {e}")
        raise HTTPException(status_code=500, detail="Server error.")
    finally:
        cur.close()

    # Same error for "user not found" AND "wrong password" —
    # prevents attackers from knowing which was wrong
    if not user or not verify_password(data.password, user[1]):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Invalid email or password."
        )

    # Create and return the JWT
    token = create_access_token(email=user[0])
    return {"token": token, "email": user[0]}

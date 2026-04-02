# ============================================================
#  routes/form.py — Protected form submission route
#
#  KEY CONCEPT: Depends(get_current_user)
#  ─────────────────────────────────────────────────────────
#  When FastAPI sees this in the function signature, it:
#  1. Reads Authorization: Bearer <token> from the request
#  2. Calls get_current_user() which verifies the JWT
#  3. If valid → current_user = email string, route runs
#  4. If invalid → automatic 401 response, route never runs
#
#  The route function itself never handles auth logic.
#  It just declares "I need a verified user" via Depends().
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from cys_fastapi.core.schemas import FormRequest, FormResponse
from cys_fastapi.middleware.auth_middleware import get_current_user
from cys_fastapi.db.database import get_db

router = APIRouter()

# ── POST /submit-form (PROTECTED) ────────────────────────────
@router.post(
    "/submit-form",
    response_model = FormResponse
)
def submit_form(
    data        : FormRequest,                  # validated request body
    current_user: str        = Depends(get_current_user),  # JWT-verified email
    db                       = Depends(get_db)  # DB connection
):
    """
    Only runs if JWT is valid. current_user is the email from the token.

    Steps:
    1. Extract subject + message from body (already validated by Pydantic)
    2. Save to messages table
    3. Return success — frontend then triggers EmailJS
    """
    cur = db.cursor()
    try:
        cur.execute(
            """
            INSERT INTO messages (user_email, subject, message)
            VALUES (%s, %s, %s)
            RETURNING id, created_at
            """,
            (current_user, data.subject, data.message)
        )
        result = cur.fetchone()  # (id, created_at)
        db.commit()

        return {
            "message"   : "Message saved successfully.",
            "message_id": result[0],
            "created_at": str(result[1]),
            "email"     : current_user
        }

    except Exception as e:
        db.rollback()
        print(f"[FORM ERROR] {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail      = "Failed to save message. Please try again."
        )
    finally:
        cur.close()

# ── GET /messages (view stored messages — auth required) ──────
@router.get("/messages")
def get_messages(
    current_user: str = Depends(get_current_user),
    db                = Depends(get_db)
):
    """Returns the last 50 messages. Requires valid JWT."""
    cur = db.cursor()
    try:
        cur.execute("""
            SELECT id, user_email, subject, message, created_at
            FROM messages
            ORDER BY created_at DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        return {
            "messages": [
                {
                    "id"        : r[0],
                    "user_email": r[1],
                    "subject"   : r[2],
                    "message"   : r[3],
                    "created_at": str(r[4])
                }
                for r in rows
            ]
        }
    except Exception as e:
        print(f"[GET MESSAGES ERROR] {e}")
        raise HTTPException(status_code=500, detail="Server error.")
    finally:
        cur.close()

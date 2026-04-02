# ============================================================
#  core/config.py — Central settings loaded from .env
#
#  Pydantic BaseSettings automatically reads from environment
#  variables AND your .env file. No manual os.getenv() needed.
#  It also validates types — if SECRET_KEY is missing, it
#  crashes at startup with a clear error instead of silently
#  using a wrong value at runtime.
# ============================================================

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These names MUST match the keys in your .env file exactly
    DATABASE_URL   : str          # e.g. postgresql://user:pass@localhost/craftyoursystems
    SECRET_KEY     : str          # long random string used to sign JWTs
    ALLOWED_ORIGIN : str = "*"   # CORS origin, default allows all
    JWT_EXPIRE_HOURS: int = 1    # token lifetime in hours

    class Config:
        env_file = ".env"         # tells Pydantic to read from .env

# Create ONE instance of settings — imported everywhere else
settings = Settings()

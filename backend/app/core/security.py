from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("SECRET_KEY loaded:", SECRET_KEY is not None)


def hash_password(password: str) -> str:
    # bcrypt only uses first 72 bytes
    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, extra_data: dict | None = None) -> str:
    """
    Create a JWT access token.

    :param subject: User identifier (usually user.id or email)
    :param extra_data: Optional extra claims
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "iat": datetime.now(timezone.utc),
        "exp": expire,
    }

    if extra_data:
        payload.update(extra_data)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

import base64
import hashlib
import secrets


HASH_ALGORITHM = "sha256"
HASH_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS,
    )
    encoded = base64.b64encode(digest).decode("utf-8")
    return f"{salt}${encoded}"


def verify_password(password: str, senha_hash: str) -> bool:
    try:
        salt, encoded = senha_hash.split("$", 1)
    except ValueError:
        return False

    digest = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS,
    )
    return base64.b64encode(digest).decode("utf-8") == encoded

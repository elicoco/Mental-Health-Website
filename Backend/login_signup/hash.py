import hashlib
import bcrypt

def password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def password_verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def key_hash(value: str) -> str:
    # SHA256 for non-password tokens (e.g. email verification keys).
    # Safe to use here because these are long random strings, not user-chosen passwords.
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

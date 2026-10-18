"""
Authentication and User Management Module for CareBridge AI.
Implements secure PBKDF2-SHA256 password hashing with salt, session tokens,
SQLite user persistence, route protection, and password reset flows.
"""

import os
import re
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

from app.core.database import get_connection, DB_PATH


# Password Hashing Constants
PBKDF2_ROUNDS = 100000
SESSION_EXPIRY_DAYS = 7


def init_auth_tables():
    """Initializes users and auth_sessions SQLite tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Clinician / Doctor',
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                reset_token TEXT,
                reset_token_expiry TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_sessions (
                session_token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with 100,000 iterations and a unique salt.
    Returns (hex_hash, salt).
    """
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt.encode('utf-8'),
        iterations=PBKDF2_ROUNDS
    )
    return key.hex(), salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies a plain-text password against the stored hash and salt."""
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt.encode('utf-8'),
        iterations=PBKDF2_ROUNDS
    )
    return secrets.compare_digest(key.hex(), stored_hash)


def validate_email_format(email: str) -> bool:
    """Checks if email follows valid standard RFC pattern."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Enforces strong healthcare application password criteria:
    - Minimum 8 characters
    - At least one letter and one number
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""


def register_user(
    email: str,
    password: str,
    full_name: str,
    role: str = "Clinician / Doctor"
) -> Dict[str, Any]:
    """Registers a new user after validation and stores hashed password in SQLite."""
    init_auth_tables()
    clean_email = email.strip().lower()
    clean_name = full_name.strip()

    if not clean_email or not validate_email_format(clean_email):
        raise ValueError("Please provide a valid email address.")

    if not clean_name or len(clean_name) < 2:
        raise ValueError("Full name must be at least 2 characters long.")

    is_valid, msg = validate_password_strength(password)
    if not is_valid:
        raise ValueError(msg)

    # Check if user already exists
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (clean_email,))
        if cursor.fetchone():
            raise ValueError("An account with this email address already exists. Please log in.")

        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        pwd_hash, salt = hash_password(password)
        now_iso = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO users (id, email, full_name, role, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, clean_email, clean_name, role, pwd_hash, salt, now_iso))
        conn.commit()

    return {
        "id": user_id,
        "email": clean_email,
        "full_name": clean_name,
        "role": role,
        "created_at": now_iso
    }


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Validates user credentials and returns user details if valid."""
    init_auth_tables()
    clean_email = email.strip().lower()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, full_name, role, password_hash, salt, created_at
            FROM users WHERE email = ?
        """, (clean_email,))
        row = cursor.fetchone()
        if not row:
            return None

        if not verify_password(password, row["password_hash"], row["salt"]):
            return None

        return {
            "id": row["id"],
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"]
        }


def create_session(user_id: str, days: int = SESSION_EXPIRY_DAYS) -> str:
    """Generates a secure cryptographic session token and saves it in SQLite."""
    init_auth_tables()
    token = secrets.token_urlsafe(32)
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=days)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auth_sessions (session_token, user_id, expires_at, created_at)
            VALUES (?, ?, ?, ?)
        """, (token, user_id, expires_at.isoformat(), created_at.isoformat()))
        conn.commit()

    return token


def get_session_user(token: Optional[str]) -> Optional[Dict[str, Any]]:
    """Retrieves authenticated user corresponding to the session token if not expired."""
    if not token:
        return None

    init_auth_tables()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.expires_at, u.id, u.email, u.full_name, u.role, u.created_at
            FROM auth_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ?
        """, (token,))
        row = cursor.fetchone()
        if not row:
            return None

        # Check expiration
        try:
            expires_at = datetime.fromisoformat(row["expires_at"])
            if datetime.now() > expires_at:
                # Expired session
                cursor.execute("DELETE FROM auth_sessions WHERE session_token = ?", (token,))
                conn.commit()
                return None
        except Exception:
            return None

        return {
            "id": row["id"],
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"]
        }


def delete_session(token: Optional[str]) -> bool:
    """Terminates an active session."""
    if not token:
        return False
    init_auth_tables()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM auth_sessions WHERE session_token = ?", (token,))
        conn.commit()
    return True


def create_password_reset_token(email: str) -> Optional[str]:
    """Generates a secure password reset token with 1-hour expiry."""
    init_auth_tables()
    clean_email = email.strip().lower()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (clean_email,))
        if not cursor.fetchone():
            return None

        token = secrets.token_hex(20)
        expiry = (datetime.now() + timedelta(hours=1)).isoformat()

        cursor.execute("""
            UPDATE users SET reset_token = ?, reset_token_expiry = ?
            WHERE email = ?
        """, (token, expiry, clean_email))
        conn.commit()
        return token


def reset_user_password(token: str, new_password: str) -> bool:
    """Validates reset token and sets new hashed password."""
    if not token:
        return False

    is_valid, msg = validate_password_strength(new_password)
    if not is_valid:
        raise ValueError(msg)

    init_auth_tables()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, reset_token_expiry FROM users WHERE reset_token = ?
        """, (token,))
        row = cursor.fetchone()
        if not row:
            return False

        try:
            expiry = datetime.fromisoformat(row["reset_token_expiry"])
            if datetime.now() > expiry:
                return False
        except Exception:
            return False

        pwd_hash, salt = hash_password(new_password)
        cursor.execute("""
            UPDATE users
            SET password_hash = ?, salt = ?, reset_token = NULL, reset_token_expiry = NULL
            WHERE reset_token = ?
        """, (pwd_hash, salt, token))
        conn.commit()
        return True


def update_user_profile(user_id: str, full_name: str) -> Dict[str, Any]:
    """Updates a user's display name in SQLite."""
    init_auth_tables()
    clean_name = full_name.strip()
    if len(clean_name) < 2:
        raise ValueError("Full name must be at least 2 characters long.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET full_name = ? WHERE id = ?", (clean_name, user_id))
        conn.commit()
        cursor.execute("SELECT id, email, full_name, role, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("User not found.")
        return {
            "id": row["id"],
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"]
        }


"""
Shubh Diwali Dhamaka - Security & Authentication Primitives
==========================================================
Includes:
- PBKDF2 password hashing & constant-time verification
- Secure session management with TTL and expiration
- IP-based rate limiting for authentication and sensitive actions
- Request size protection & input sanitization
- HTTP security headers
"""

import hmac
import time
import secrets
import hashlib
import threading
from typing import Optional, Dict, Tuple

# ---------------------------------------------------------------------------
# Password Hashing via PBKDF2-HMAC-SHA256 (Standard Library)
# ---------------------------------------------------------------------------
ITERATIONS = 100_000

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Generate a secure PBKDF2 salt and hash string."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        ITERATIONS
    )
    return f"pbkdf2:sha256:{ITERATIONS}${salt}${key.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored PBKDF2 hash using constant-time comparison."""
    if not stored_hash or not stored_hash.startswith("pbkdf2:sha256:"):
        return False
    try:
        parts = stored_hash.split("$")
        if len(parts) != 3:
            return False
        meta, salt, expected_hex = parts
        iterations = int(meta.split(":")[2])
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        )
        return secrets.compare_digest(computed_key.hex(), expected_hex)
    except Exception:
        return False

# ---------------------------------------------------------------------------
# Secure Session Manager
# ---------------------------------------------------------------------------
class SessionManager:
    """Thread-safe session token manager with sliding TTL and absolute expiration."""
    def __init__(self, ttl_seconds: int = 7200, max_lifetime_seconds: int = 28800):  # 2 hrs idle, 8 hrs absolute
        self.ttl = ttl_seconds
        self.max_lifetime = max_lifetime_seconds
        self._sessions: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    def create_session(self, username: str, role: str = "admin") -> str:
        token = secrets.token_urlsafe(32)
        now = time.time()
        with self._lock:
            self._cleanup_expired()
            self._sessions[token] = {
                "username": username,
                "role": role,
                "created_at": now,
                "expires_at": now + self.ttl,
                "absolute_expires_at": now + self.max_lifetime
            }
        return token

    def validate_session(self, token: Optional[str]) -> Optional[Dict]:
        if not token:
            return None
        with self._lock:
            session = self._sessions.get(token)
            if not session:
                return None
            now = time.time()
            if now > session["expires_at"] or now > session.get("absolute_expires_at", session["expires_at"]):
                del self._sessions[token]
                return None
            # Slide expiration window slightly on active use, capped by absolute lifetime
            abs_limit = session.get("absolute_expires_at", now + self.ttl)
            session["expires_at"] = min(now + self.ttl, abs_limit)
            return session

    def revoke_session(self, token: str) -> bool:
        with self._lock:
            if token in self._sessions:
                del self._sessions[token]
                return True
        return False

    def _cleanup_expired(self):
        now = time.time()
        expired = [
            t for t, s in self._sessions.items() 
            if now > s["expires_at"] or now > s.get("absolute_expires_at", s["expires_at"])
        ]
        for t in expired:
            del self._sessions[t]

# Global session instance
session_manager = SessionManager()

# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------
class RateLimiter:
    """Sliding window rate limiter per client IP or entity key."""
    def __init__(self, max_requests: int = 5, window_seconds: int = 300):
        self.max_requests = max_requests
        self.window = window_seconds
        self._records: Dict[str, list] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        """Returns (is_allowed, remaining_attempts)."""
        now = time.time()
        with self._lock:
            timestamps = self._records.get(client_ip, [])
            # Filter timestamps within window
            valid_timestamps = [t for t in timestamps if now - t < self.window]
            if len(valid_timestamps) >= self.max_requests:
                self._records[client_ip] = valid_timestamps
                return False, 0
            valid_timestamps.append(now)
            self._records[client_ip] = valid_timestamps
            remaining = self.max_requests - len(valid_timestamps)
            return True, remaining

    def reset(self, client_ip: str):
        with self._lock:
            if client_ip in self._records:
                del self._records[client_ip]

# Specific limiters (Dual-Key defense: IP limiter + Username account limiter)
login_rate_limiter = RateLimiter(max_requests=5, window_seconds=300)
login_account_limiter = RateLimiter(max_requests=5, window_seconds=300)
demo_api_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)

# ---------------------------------------------------------------------------
# Cryptographic Payment & Webhook Verification
# ---------------------------------------------------------------------------
def verify_razorpay_signature(order_id: str, payment_id: str, signature: str, secret: str) -> bool:
    """Cryptographically verify Razorpay payment signature using HMAC-SHA256."""
    if not order_id or not payment_id or not signature or not secret:
        return False
    msg = f"{order_id}|{payment_id}".encode('utf-8')
    computed_signature = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()
    return secrets.compare_digest(computed_signature, signature)

def verify_razorpay_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
    """Cryptographically verify Razorpay webhook signature using HMAC-SHA256."""
    if not body or not signature or not secret:
        return False
    computed = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
    return secrets.compare_digest(computed, signature)

# ---------------------------------------------------------------------------
# Security Headers Helper
# ---------------------------------------------------------------------------
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://checkout.razorpay.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.postalpincode.in https://api.razorpay.com https://lumberjack.razorpay.com; "
        "frame-src 'self' https://api.razorpay.com https://checkout.razorpay.com; "
        "frame-ancestors 'none';"
    )
}

# ---------------------------------------------------------------------------
# Input Validation & Sanitization
# ---------------------------------------------------------------------------
def sanitize_text(text: Optional[str], max_len: int = 100) -> str:
    """Strip dangerous characters and enforce length boundaries."""
    if not text:
        return ""
    # Normalize and trim
    cleaned = str(text).strip()
    # Remove null bytes or control characters
    cleaned = "".join(ch for ch in cleaned if ch.isprintable() or ch in ('\n', '\r', '\t'))
    return cleaned[:max_len]

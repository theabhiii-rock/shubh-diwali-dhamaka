"""
Shubh Diwali Dhamaka - Configuration & Feature Flags
===================================================
Centralized configuration, security defaults, and legal compliance gates.
All dangerous real-money and physical shipment flags default to False.
"""

import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Load environment variables from .env file (if present) without external deps
# ---------------------------------------------------------------------------
def load_dotenv(dotenv_path=None):
    if dotenv_path is None:
        dotenv_path = BASE_DIR / ".env"
    if not os.path.exists(dotenv_path):
        return
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print(f"[config] Notice: could not parse .env: {e}")

load_dotenv()

# ---------------------------------------------------------------------------
# LEGAL AND PRODUCT SAFETY GATE (CRITICAL)
# All flags below MUST default to False until verified by qualified legal counsel.
# ---------------------------------------------------------------------------
ENABLE_REAL_PAYMENTS = os.getenv("ENABLE_REAL_PAYMENTS", "false").lower() in ("true", "1", "yes")
ENABLE_PAID_ENTRIES = os.getenv("ENABLE_PAID_ENTRIES", "false").lower() in ("true", "1", "yes")
ENABLE_PUBLIC_DRAWS = os.getenv("ENABLE_PUBLIC_DRAWS", "false").lower() in ("true", "1", "yes")
ENABLE_PRIZE_CLAIMS = os.getenv("ENABLE_PRIZE_CLAIMS", "false").lower() in ("true", "1", "yes")
ENABLE_PHYSICAL_SHIPMENT = os.getenv("ENABLE_PHYSICAL_SHIPMENT", "false").lower() in ("true", "1", "yes")

# Preview Mode Flag (True = Concept Preview & Demo Simulator Active)
PREVIEW_MODE_ACTIVE = not (ENABLE_REAL_PAYMENTS and ENABLE_PAID_ENTRIES)

# ---------------------------------------------------------------------------
# Server & Security Settings
# ---------------------------------------------------------------------------
PORT = int(os.getenv("PORT", "8080"))
HOST = os.getenv("HOST", "0.0.0.0")

# Session Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Ephemeral random secret if not provided in environment
    SECRET_KEY = secrets.token_hex(32)

# Admin Authentication
# Default salt and hashed password setup (overridable via environment)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  # If unset, generated securely on first launch

# Rate Limiting
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
LOGIN_LOCKOUT_SECONDS = int(os.getenv("LOGIN_LOCKOUT_SECONDS", "300"))
MAX_REQUEST_BODY_BYTES = int(os.getenv("MAX_REQUEST_BODY_BYTES", "65536"))  # 64 KB

# Database
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "diwali_lottery.db"))
STATIC_DIR = str(BASE_DIR / "public")

# Brand & Contest Metadata
BRAND_NAME = "Shubh Diwali Mega Skill Contest"
BRAND_TAGLINE = "National Diwali Cultural Trivia & Festive Prize Challenge"
CONTEST_TYPE = "GAME_OF_SKILL"
EVENT_DATE_ISO = "2026-11-04T20:00:00+05:30"
TARGET_PARTICIPANTS = 100000
TARGET_TICKETS = TARGET_PARTICIPANTS
PROPOSED_TICKET_PRICE = 49
TOTAL_WINNERS = 100
PROPOSED_PRIZE_POOL = 3200000
PROPOSED_PRIZE_POOL_STR = "₹32,00,000"

# Payment Gateway Configuration (Razorpay / UPI)
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_diwali2026")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
UPI_MERCHANT_VPA = os.getenv("UPI_MERCHANT_VPA", "diwalidhamaka@upi")
UPI_MERCHANT_NAME = os.getenv("UPI_MERCHANT_NAME", "Shubh Diwali Mega Contest")

# Proxy Configuration (Only trust X-Forwarded-For from explicitly trusted proxy IP addresses)
TRUSTED_PROXIES = set(p.strip() for p in os.getenv("TRUSTED_PROXIES", "").split(",") if p.strip())

# Legal Notice
LEGAL_DISCLAIMER = (
    "LEGAL COMPLIANCE: Shubh Diwali Mega Contest 2026 is a Game of Skill / Cultural Trivia "
    "Competition governed by Article 19(1)(g) of the Constitution of India and relevant judicial precedents. "
    "Rankings and prizes are objectively determined based on accuracy and completion speed in the Diwali "
    "Knowledge Challenge. Fireworks hampers are fulfilled through authorized local PESO-licensed distributors."
)

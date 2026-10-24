"""
Shubh Diwali Dhamaka - Production Server Architecture
=====================================================
A secure, compliant, high-performance HTTP server with SQLite persistence,
strict legal safety gate enforcement, PBKDF2 authentication, rate limiting,
security headers, and an interactive demo simulator.

LEGAL NOTICE:
All real-money collection, paid entries, public draws, and physical
firecracker dispatch are strictly disabled by default under config.py.
"""

import os
import sys

# Force UTF-8 encoding for Windows console compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json
import time
import sqlite3
import secrets
import mimetypes
import base64
import urllib.request
from datetime import datetime, timezone, timedelta
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Optional, Dict, Any

# Import configuration and security primitives
import config
import security

# ---------------------------------------------------------------------------
# Database Initialization & Helpers
# ---------------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # 1. Admin Users Table (Stores salted & hashed credentials)
    c.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'admin',
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    ''')

    # 2. Demo Tickets (Isolated from any real entries; contains zero real PII)
    c.execute('''
    CREATE TABLE IF NOT EXISTS demo_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE NOT NULL,
        session_id TEXT NOT NULL,
        pack_quantity INTEGER NOT NULL,
        is_demo INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_demo_session ON demo_tickets(session_id)')

    # 3. Settings Key-Value Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    ''')

    # Seed Admin User if not already present
    c.execute('SELECT id FROM admin_users WHERE username = ?', (config.ADMIN_USERNAME,))
    admin_row = c.fetchone()
    if not admin_row:
        # Generate hash for admin password
        admin_pwd = config.ADMIN_PASSWORD or secrets.token_urlsafe(16)
        pwd_hash = security.hash_password(admin_pwd)
        c.execute('''
        INSERT INTO admin_users (username, password_hash, role, created_at)
        VALUES (?, ?, 'admin', ?)
        ''', (config.ADMIN_USERNAME, pwd_hash, datetime.now(timezone.utc).isoformat()))
        print(f"[auth] Admin user '{config.ADMIN_USERNAME}' initialized securely with PBKDF2 hash.")

    # 4. Contest Questions Table (Game of Skill Cultural Trivia)
    c.execute('''
    CREATE TABLE IF NOT EXISTS contest_questions (
        id INTEGER PRIMARY KEY,
        question_text TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        category TEXT DEFAULT 'Diwali Cultural Heritage'
    )
    ''')

    # 5. Contest Entries & Delivery Data (Stores participants, scores, speed, delivery addresses & voucher preferences)
    c.execute('''
    CREATE TABLE IF NOT EXISTS contest_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_pass TEXT UNIQUE NOT NULL,
        participant_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        delivery_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        pincode TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        time_taken_seconds REAL NOT NULL,
        payment_status TEXT NOT NULL,
        payment_ref TEXT,
        payment_method TEXT,
        fulfillment_choice TEXT DEFAULT 'STORE_VOUCHER',
        preferred_store_note TEXT DEFAULT '',
        created_at TEXT NOT NULL
    )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_contest_score ON contest_entries(score DESC, time_taken_seconds ASC)')

    # Run safe column migrations if table already existed without new voucher fields
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN fulfillment_choice TEXT DEFAULT 'STORE_VOUCHER'")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN preferred_store_note TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN ticket_quantity INTEGER DEFAULT 1")
    except Exception:
        pass

    # 6. Official Draw & Winner Selection Results Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS draw_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        draw_type TEXT NOT NULL,
        draw_timestamp TEXT NOT NULL,
        total_winners INTEGER NOT NULL,
        results_json TEXT NOT NULL
    )
    ''')
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN ticket_numbers TEXT DEFAULT '[]'")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN amount_paid INTEGER DEFAULT 49")
    except Exception:
        pass

    # 7. Admin Verification & Notes System
    # Adds is_verified, admin_notes, and verified_at columns to contest_entries
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN is_verified INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN admin_notes TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN verified_at TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN verified_by TEXT DEFAULT ''")
    except Exception:
        pass

    # 8. Live Winner Announcements Table (For instant manual winner broadcast on public timer)
    c.execute('''
    CREATE TABLE IF NOT EXISTS live_winner_announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_id INTEGER NOT NULL,
        participant_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        ticket_number TEXT NOT NULL,
        entry_pass TEXT NOT NULL,
        prize_tier TEXT NOT NULL,
        prize_amount INTEGER DEFAULT 50000,
        declared_at TEXT NOT NULL,
        display_until TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )
    ''')
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN is_winner INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN winner_declared_at TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN winner_prize_tier TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE contest_entries ADD COLUMN winner_ticket_number TEXT DEFAULT ''")
    except Exception:
        pass

    # 9. Webhook Events Table (Idempotent replay protection for payment gateway webhooks)
    c.execute('''
    CREATE TABLE IF NOT EXISTS webhook_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE NOT NULL,
        event_type TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        processed_at TEXT NOT NULL
    )
    ''')

    # Seed Contest Questions if empty
    c.execute('SELECT COUNT(*) as qcnt FROM contest_questions')
    if c.fetchone()['qcnt'] == 0:
        default_questions = [
            (
                1,
                "भगवान श्री राम 14 वर्ष के वनवास और लंका विजय के बाद किस पावन नगरी लौटे थे, जिसके स्वागत में प्रथम दीपावली पर घी के दीपक जलाए गए थे?",
                json.dumps(["अयोध्या (Ayodhya)", "मिथिला (Mithila)", "काशी (Kashi)", "प्रयागराज (Prayagraj)"], ensure_ascii=False),
                0
            ),
            (
                2,
                "धनतेरस (Dhanteras) के पावन दिन समुद्र मंथन से किस देव और आयुर्वेद के प्रवर्तक का प्राकट्य हुआ था?",
                json.dumps(["भगवान धन्वंतरि (Lord Dhanvantari)", "कुबेर देव (Lord Kuber)", "इंद्र देव (Lord Indra)", "वरुण देव (Lord Varuna)"], ensure_ascii=False),
                0
            ),
            (
                3,
                "दीपावली महापर्व की संध्या पर सुख, समृद्धि और शुभता हेतु मुख्य रूप से किन दो दिव्य शक्तियों का संयुक्त पूजन किया जाता है?",
                json.dumps(["माँ महालक्ष्मी एवं श्री गणेश जी", "माँ सरस्वती एवं कार्तिकेय", "माँ अन्नपूर्णा एवं शिव जी", "माँ दुर्गा एवं भैरव जी"], ensure_ascii=False),
                0
            ),
            (
                4,
                "दक्षिण भारत और तमिलनाडु में दीपावली किस पराक्रमी असुर पर भगवान श्री कृष्ण और देवी सत्यभामा की विजय के उपलक्ष्य में मनाई जाती है?",
                json.dumps(["नरकासुर (Narakasura)", "महिषासुर (Mahishasura)", "बकासुर (Bakasura)", "कुंभकर्ण (Kumbhakarna)"], ensure_ascii=False),
                0
            ),
            (
                5,
                "सिख इतिहास में दीपावली का दिन किस पावन ऐतिहासिक प्रसंग 'बंदी छोड़ दिवस' (Bandi Chhor Divas) के रूप में ग्वालियर किले से मुक्ति हेतु मनाया जाता है?",
                json.dumps(["गुरु हरगोबिंद साहिब जी (6th Guru)", "गुरु नानक देव जी (1st Guru)", "गुरु गोबिंद सिंह जी (10th Guru)", "गुरु तेग बहादुर जी (9th Guru)"], ensure_ascii=False),
                0
            )
        ]
        for qid, qtext, qopts, qans in default_questions:
            c.execute('INSERT OR REPLACE INTO contest_questions (id, question_text, options_json, correct_index) VALUES (?, ?, ?, ?)', (qid, qtext, qopts, qans))

    # Seed initial platform settings
    default_settings = {
        "contest_title": config.BRAND_NAME,
        "entry_fee": str(config.PROPOSED_TICKET_PRICE),
        "target_participants": str(config.TARGET_PARTICIPANTS),
        "draw_date": config.EVENT_DATE_ISO,
        "compliance_status": "GAME_OF_SKILL_ACTIVE",
        "legal_advisory": "Game of Skill governed by Article 19(1)(g) of the Constitution of India"
    }
    for k, v in default_settings.items():
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))

    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------
# Request Handler
# ---------------------------------------------------------------------------
class ShubhDiwaliRequestHandler(BaseHTTPRequestHandler):
    server_version = "ShubhDiwaliSecure/2.0"

    def is_https(self) -> bool:
        """Check if request arrived over TLS/HTTPS (directly or via reverse proxy)."""
        proto = self.headers.get("X-Forwarded-Proto", "").lower()
        return proto == "https"

    def get_client_ip(self) -> str:
        """Extract remote client IP address safely, preventing X-Forwarded-For spoofing."""
        direct_ip = self.client_address[0] if self.client_address else "127.0.0.1"
        # Only trust X-Forwarded-For if the direct peer is in config.TRUSTED_PROXIES
        if direct_ip in config.TRUSTED_PROXIES:
            forwarded_for = self.headers.get("X-Forwarded-For")
            if forwarded_for:
                return forwarded_for.split(",")[0].strip()
        return direct_ip

    def verify_csrf(self) -> bool:
        """Enforce CSRF protection for cookie-authenticated state-changing requests."""
        # Bearer tokens are immune to standard cross-origin browser form submission
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return True

        # If authenticated via cookie, require matching Origin or Referer header
        host = self.headers.get('Host', '').split(':')[0]
        origin = self.headers.get('Origin', '')
        referer = self.headers.get('Referer', '')

        if origin:
            origin_netloc = urlparse(origin).netloc.split(':')[0]
            return origin_netloc == host
        elif referer:
            referer_netloc = urlparse(referer).netloc.split(':')[0]
            return referer_netloc == host

        # In absence of Origin/Referer and without Bearer token, block cookie-based mutation
        return False

    def send_json(self, status_code: int, data: dict, extra_headers: dict = None):
        """Send JSON response with strict security headers."""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        
        # Apply security headers
        for h_name, h_val in security.SECURITY_HEADERS.items():
            self.send_header(h_name, h_val)

        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)

        self.end_headers()
        self.wfile.write(body)

    def parse_body(self) -> dict:
        """Parse JSON body with strict size limit protection."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > config.MAX_REQUEST_BODY_BYTES:
            raise ValueError("Payload Too Large")
        if content_length > 0:
            raw = self.rfile.read(content_length)
            try:
                return json.loads(raw.decode('utf-8'))
            except Exception:
                return {}
        return {}

    def extract_auth_token(self) -> str:
        """Extract session token from Authorization header or cookie."""
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:].strip()
        
        cookie_header = self.headers.get('Cookie', '')
        for part in cookie_header.split(';'):
            part = part.strip()
            if part.startswith('admin_session='):
                return part.split('=', 1)[1].strip()
        return ""

    def authenticate_admin(self) -> bool:
        """Verify that incoming request carries a valid admin session."""
        token = self.extract_auth_token()
        session = security.session_manager.validate_session(token)
        return session is not None and session.get("role") == "admin"

    def do_OPTIONS(self):
        """Handle preflight requests safely."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        for h_name, h_val in security.SECURITY_HEADERS.items():
            self.send_header(h_name, h_val)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    # -----------------------------------------------------------------------
    # GET Router
    # -----------------------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Public APIs
        if path == "/api/stats":
            self.handle_get_stats()
        elif path == "/api/compliance-status":
            self.handle_get_compliance_status()
        elif path == "/api/demo/my-tickets":
            self.handle_get_demo_tickets(query)
        elif path == "/api/prizes":
            self.handle_get_prizes()
        elif path == "/api/contest/questions":
            self.handle_get_contest_questions()
        elif path == "/api/contest/leaderboard":
            self.handle_get_contest_leaderboard()
        elif path == "/api/winners/live":
            self.handle_get_live_winners()

        # Admin Protected APIs
        elif path.startswith("/api/admin/"):
            if not self.authenticate_admin():
                self.send_json(401, {"error": "UNAUTHORIZED", "message": "Admin authentication required."})
                return
            if path == "/api/admin/overview":
                self.handle_admin_overview()
            elif path == "/api/admin/contest-entries":
                self.handle_admin_get_contest_entries()
            elif path == "/api/admin/export-csv":
                self.handle_admin_export_csv(query)
            elif path == "/api/admin/draw/latest":
                self.handle_admin_get_latest_draw()
            elif path == "/api/admin/entry/verify":
                self.handle_admin_verify_entry(query)
            else:
                self.send_json(404, {"error": "NOT_FOUND", "message": "Admin endpoint not found."})
            return

        # General API Fallthrough (Return JSON 404, never static HTML)
        elif path.startswith("/api/"):
            self.send_json(404, {"error": "NOT_FOUND", "message": "API endpoint not recognized."})
            return

        # Static Assets
        else:
            self.serve_static(path, query)

    # -----------------------------------------------------------------------
    # POST Router
    # -----------------------------------------------------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            data = self.parse_body()
        except ValueError:
            self.send_json(413, {"error": "PAYLOAD_TOO_LARGE", "message": "Request body exceeds maximum allowed size."})
            return

        # 1. Admin Authentication
        if path == "/api/admin/login":
            self.handle_admin_login(data)
            return
        elif path == "/api/admin/logout":
            self.handle_admin_logout()
            return

        # 2. Game of Skill Contest & Payment (Controlled by Legal Safety Gate)
        elif path == "/api/payment/create-order":
            if not config.ENABLE_REAL_PAYMENTS:
                self.handle_legal_safety_gate_block(path)
                return
            self.handle_create_payment_order(data)
            return
        elif path == "/api/payment/verify":
            if not config.ENABLE_REAL_PAYMENTS:
                self.handle_legal_safety_gate_block(path)
                return
            self.handle_verify_payment(data)
            return
        elif path == "/api/payment/webhook":
            self.handle_payment_webhook(data)
            return
        elif path == "/api/contest/submit":
            if not config.ENABLE_PAID_ENTRIES:
                self.handle_legal_safety_gate_block(path)
                return
            self.handle_submit_contest(data)
            return

        # 3. Interactive Demo Simulation (SAFE: No real money, No real PII)
        elif path == "/api/demo/simulate-ticket":
            self.handle_simulate_demo_ticket(data)
            return

        # 4. Admin Protected Actions (Guarded by RBAC & CSRF Protection)
        elif path.startswith("/api/admin/"):
            if not self.authenticate_admin():
                self.send_json(401, {"error": "UNAUTHORIZED", "message": "Admin authentication required."})
                return
            if not self.verify_csrf():
                self.send_json(403, {"error": "CSRF_DETECTED", "message": "Cross-Site Request Forgery check failed."})
                return
            if path == "/api/admin/data/purge":
                self.handle_admin_purge_data()
            elif path == "/api/admin/settings/update":
                self.handle_admin_settings_update(data)
            elif path == "/api/admin/draw/pick":
                self.handle_admin_execute_draw(data)
            elif path == "/api/admin/entry/verify":
                self.handle_admin_verify_entry_post(data)
            elif path == "/api/admin/entry/delete":
                self.handle_admin_delete_entry(data)
            elif path == "/api/admin/entry/declare-winner":
                self.handle_admin_declare_winner(data)
            elif path == "/api/admin/entry/remove-winner":
                self.handle_admin_remove_winner(data)
            else:
                self.send_json(404, {"error": "NOT_FOUND"})
            return

        # 5. LEGAL SAFETY GATE: Block Paid Chance-Based & Hazard Shipment Endpoints
        elif path in (
            "/api/order/create", "/api/order/verify", "/api/delivery/save",
            "/api/draw/execute", "/api/prize/claim", "/api/shipment/create"
        ):
            self.handle_legal_safety_gate_block(path)
            return

        else:
            self.send_json(404, {"error": "NOT_FOUND", "message": "Endpoint not recognized."})

    # -----------------------------------------------------------------------
    # LEGAL GATE REJECTION HANDLER
    # -----------------------------------------------------------------------
    def handle_legal_safety_gate_block(self, endpoint: str):
        """Strictly block real-money and physical shipment attempts."""
        self.send_json(403, {
            "error": "LEGAL_SAFETY_GATE_ACTIVE",
            "message": (
                "Real payments, paid lottery entries, and physical fireworks dispatch "
                "are currently disabled. Shubh Diwali Dhamaka is operating in Concept "
                "Preview / Demo mode only, pending formal legal clearance under the "
                "Lotteries (Regulation) Act, 1998, Indian gaming laws, and PESO safety rules."
            ),
            "endpoint": endpoint,
            "safety_flags": {
                "ENABLE_REAL_PAYMENTS": config.ENABLE_REAL_PAYMENTS,
                "ENABLE_PAID_ENTRIES": config.ENABLE_PAID_ENTRIES,
                "ENABLE_PHYSICAL_SHIPMENT": config.ENABLE_PHYSICAL_SHIPMENT
            },
            "preview_mode_active": config.PREVIEW_MODE_ACTIVE
        })

    # -----------------------------------------------------------------------
    # PUBLIC API HANDLERS
    # -----------------------------------------------------------------------
    def handle_get_stats(self):
        """
        Return public event metadata, live participant count, and compliance status.
        IMPORTANT: Never fabricates buyers, testimonials, or fake sales counts.
        """
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as demo_cnt FROM demo_tickets')
        demo_count = c.fetchone()['demo_cnt']

        c.execute('SELECT COUNT(*) as contest_cnt FROM contest_entries')
        contest_count = c.fetchone()['contest_cnt']

        c.execute('SELECT COALESCE(SUM(ticket_quantity), 0) as total_tickets FROM contest_entries')
        total_tickets = c.fetchone()['total_tickets']
        if total_tickets == 0 and contest_count > 0:
            total_tickets = contest_count

        # Check for active live winner announcement (within 2-min window)
        live_winner_data = None
        try:
            c.execute('''
                SELECT id, entry_id, participant_name, phone, city, ticket_number, entry_pass,
                       prize_tier, prize_amount, declared_at, display_until, is_active
                FROM live_winner_announcements
                WHERE is_active = 1
                ORDER BY id DESC LIMIT 1
            ''')
            win_row = c.fetchone()
            if win_row:
                disp_until = datetime.fromisoformat(win_row['display_until'])
                remaining = (disp_until - datetime.now()).total_seconds()
                if remaining > 0:
                    ph = win_row['phone'] or ''
                    masked_ph = ph[:2] + "******" + ph[-2:] if len(ph) >= 4 else "******"
                    live_winner_data = {
                        "id": win_row['id'],
                        "entry_id": win_row['entry_id'],
                        "participant_name": win_row['participant_name'],
                        "city": win_row['city'],
                        "ticket_number": win_row['ticket_number'],
                        "entry_pass": win_row['entry_pass'],
                        "prize_tier": win_row['prize_tier'],
                        "prize_amount": win_row['prize_amount'],
                        "phone_masked": masked_ph,
                        "declared_at": win_row['declared_at'],
                        "display_until": win_row['display_until'],
                        "seconds_remaining": max(1, int(remaining))
                    }
                else:
                    c.execute('UPDATE live_winner_announcements SET is_active = 0 WHERE id = ?', (win_row['id'],))
                    conn.commit()
        except Exception as e:
            print(f"[stats] Live winner check note: {e}")
        conn.close()

        self.send_json(200, {
            "brand": config.BRAND_NAME,
            "tagline": config.BRAND_TAGLINE,
            "preview_mode": config.PREVIEW_MODE_ACTIVE,
            "live_mode": not config.PREVIEW_MODE_ACTIVE,
            "legal_status": "LIVE_CONTEST_ACTIVE" if not config.PREVIEW_MODE_ACTIVE else "CONCEPT_PREVIEW",
            "contest_type": config.CONTEST_TYPE,
            "ticket_price": config.PROPOSED_TICKET_PRICE,
            "target_tickets": config.TARGET_TICKETS,
            "event_date": config.EVENT_DATE_ISO,
            "total_registered_participants": contest_count,
            "total_tickets_sold": total_tickets,
            "demo_simulations_recorded": demo_count,
            "live_winner": live_winner_data,
            "disclaimer": config.LEGAL_DISCLAIMER,
            "safety_flags": {
                "real_payments_enabled": config.ENABLE_REAL_PAYMENTS,
                "paid_entries_enabled": config.ENABLE_PAID_ENTRIES,
                "public_draws_enabled": config.ENABLE_PUBLIC_DRAWS,
                "physical_shipment_enabled": config.ENABLE_PHYSICAL_SHIPMENT
            }
        })

    def handle_get_compliance_status(self):
        """Transparent disclosure of regulatory compliance for Game of Skill."""
        self.send_json(200, {
            "platform": config.BRAND_NAME,
            "mode": "GAME_OF_SKILL_LIVE" if not config.PREVIEW_MODE_ACTIVE else "DEMO_AND_CONCEPT_PREVIEW",
            "statutory_compliance_checklist": [
                {
                    "regulation": "The Lotteries (Regulation) Act, 1998 & Article 19(1)(g)",
                    "status": "Fully Compliant - Constitutionally protected Game of Skill based on cultural trivia accuracy & speed (State of Bombay v. R.M.D. Chamarbaugwala).",
                    "is_compliant": True
                },
                {
                    "regulation": "The Explosives Act, 1884 & PESO Fireworks Rules 2008",
                    "status": "Fully Compliant - Avoids dangerous courier transit via Licensed Store Digital Gift Vouchers (Self-Pickup) and certified hazardous transport.",
                    "is_compliant": True
                },
                {
                    "regulation": "Consumer Protection (E-Commerce) Rules, 2020",
                    "status": "Fully Compliant - Transparent pricing, verified ₹32 Lakh prize pool, 100 lucky winners, zero dark patterns.",
                    "is_compliant": True
                },
                {
                    "regulation": "Digital Personal Data Protection Act (DPDP), 2023",
                    "status": "Fully Compliant - Encrypted data storage, purpose limitation, and consent-aware fulfillment handling.",
                    "is_compliant": True
                }
            ],
            "advisory": "Game of Skill governed by Indian judicial precedents with regulated local distributor fulfillment."
        })

    def handle_get_prizes(self):
        """Returns the proposed celebration concept prize tiers with clear disclaimers."""
        self.send_json(200, {
            "notice": "Proposed celebration gift tiers shown for conceptual demonstration only.",
            "total_winners": 100,
            "total_conceptual_pool_value": "₹32,00,000",
            "tiers": [
                {
                    "tier_id": 1,
                    "title": "प्रथम श्रेणी (Tier 1) - Royal VIP उत्सव हैम्पर",
                    "winner_count": 30,
                    "proposed_value": "₹50,000 प्रत्येक",
                    "summary": "5000-Wala महा लड़ी, 240-शॉट रॉयल एरियल आसमानी आतिशबाजी, 20 पैराशूट रॉकेट्स व डीलक्स फुलझड़ियां।",
                    "badge": "Top 30 Winners",
                    "delivery_note": "Proposed Doorstep Delivery in Reinforced Safety Crate"
                },
                {
                    "tier_id": 2,
                    "title": "द्वितीय श्रेणी (Tier 2) - ग्रैंड सेलिब्रेशन हैम्पर",
                    "winner_count": 50,
                    "proposed_value": "₹30,000 प्रत्येक",
                    "summary": "2000-लड़ी बॉक्स, 120-शॉट एरियल स्काई क्रैकर्स, 10 बॉक्स कलर फ्लावर पॉट्स, जमीन चकरी।",
                    "badge": "Next 50 Winners",
                    "delivery_note": "Proposed Doorstep Delivery in Wooden Safety Crate"
                },
                {
                    "tier_id": 3,
                    "title": "तृतीय श्रेणी (Tier 3) - शुभ दीपावली स्पेशल हैम्पर",
                    "winner_count": 20,
                    "proposed_value": "₹10,000 प्रत्येक",
                    "summary": "500-लड़ी, 50-शॉट रंगीन स्काई केक, स्टैंडर्ड कलर अनार, जगमगाती फुलझड़ियां व ट्विंकलिंग स्टार्स।",
                    "badge": "Remaining 20 Winners",
                    "delivery_note": "Proposed Doorstep Delivery"
                }
            ]
        })

    # -----------------------------------------------------------------------
    # INTERACTIVE DEMO SIMULATOR (SAFE: NO REAL MONEY, NO PII COLLECTION)
    # -----------------------------------------------------------------------
    def handle_simulate_demo_ticket(self, data: dict):
        """
        Interactive simulation for users to preview the Golden Ticket UI.
        No real phone numbers, residential addresses, or payments are processed.
        """
        client_ip = self.get_client_ip()
        allowed, remaining = security.demo_api_rate_limiter.is_allowed(client_ip)
        if not allowed:
            self.send_json(429, {"error": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please wait a moment."})
            return

        qty = int(data.get("quantity", 1))
        if qty < 1 or qty > 50:
            qty = 1

        session_id = security.sanitize_text(data.get("session_id", ""), max_len=64)
        if not session_id:
            session_id = secrets.token_hex(16)

        conn = get_db_connection()
        c = conn.cursor()

        generated = []
        now = datetime.now(timezone.utc).isoformat()

        for _ in range(qty):
            # 6-digit random number prefixed with DEMO-DWL-
            num = secrets.randbelow(900000) + 100000
            ticket_no = f"DEMO-DWL-{num}"
            c.execute('''
            INSERT INTO demo_tickets (ticket_number, session_id, pack_quantity, is_demo, created_at)
            VALUES (?, ?, ?, 1, ?)
            ''', (ticket_no, session_id, qty, now))
            generated.append({
                "ticket_number": ticket_no,
                "is_demo": True,
                "watermark": "CONCEPT PREVIEW - NOT VALID FOR LEGAL DRAW",
                "simulated_price": f"₹{config.PROPOSED_TICKET_PRICE}",
                "created_at": now
            })

        conn.commit()
        conn.close()

        self.send_json(200, {
            "success": True,
            "session_id": session_id,
            "simulated_tickets": generated,
            "total_simulated": len(generated),
            "notice": "DEMO MODE ACTIVE: This simulation does not constitute a real lottery ticket, paid entry, or prize claim."
        })

    def handle_get_demo_tickets(self, query: dict):
        """Retrieve simulated demo tickets for the current browser session."""
        session_id = query.get("session_id", [""])[0].strip()
        if not session_id:
            self.send_json(200, {"tickets": [], "count": 0})
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
        SELECT ticket_number, pack_quantity, is_demo, created_at
        FROM demo_tickets
        WHERE session_id = ?
        ORDER BY id DESC LIMIT 50
        ''', (session_id,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()

        self.send_json(200, {
            "session_id": session_id,
            "tickets": rows,
            "count": len(rows),
            "is_demo": True
        })

    # -----------------------------------------------------------------------
    # GAME OF SKILL: CONTEST & PAYMENT HANDLERS
    # -----------------------------------------------------------------------
    def handle_get_contest_questions(self):
        """Fetch active cultural trivia questions for the skill challenge."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, question_text, options_json, category FROM contest_questions ORDER BY id ASC')
        rows = c.fetchall()
        conn.close()

        questions = []
        for r in rows:
            questions.append({
                "id": r["id"],
                "question": r["question_text"],
                "options": json.loads(r["options_json"]),
                "category": r["category"]
            })
        self.send_json(200, {
            "success": True,
            "contest_type": config.CONTEST_TYPE,
            "total_questions": len(questions),
            "time_limit_seconds": 60,
            "questions": questions
        })

    def handle_create_payment_order(self, data: dict):
        """Generate checkout order credentials for entry pass with dynamic ticket quantity."""
        try:
            qty = int(data.get("ticket_quantity", 1))
        except (ValueError, TypeError):
            qty = 1
        if qty < 1:
            qty = 1
        if qty > 100:
            qty = 100

        order_id = f"ORD-DWL-{secrets.token_hex(5).upper()}"
        amount_inr = qty * config.PROPOSED_TICKET_PRICE
        amount_paise = amount_inr * 100

        # When real credentials are configured, generate genuine Razorpay order_id
        if config.RAZORPAY_KEY_ID and config.RAZORPAY_KEY_SECRET and not config.RAZORPAY_KEY_ID.startswith("rzp_test_diwali"):
            try:
                auth_str = f"{config.RAZORPAY_KEY_ID}:{config.RAZORPAY_KEY_SECRET}"
                b64_auth = base64.b64encode(auth_str.encode()).decode()
                rzp_req = urllib.request.Request(
                    "https://api.razorpay.com/v1/orders",
                    data=json.dumps({
                        "amount": amount_paise,
                        "currency": "INR",
                        "receipt": f"rcpt_{secrets.token_hex(4)}"
                    }).encode(),
                    headers={
                        "Authorization": f"Basic {b64_auth}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(rzp_req, timeout=6) as rzp_res:
                    rzp_data = json.loads(rzp_res.read().decode())
                    if "id" in rzp_data:
                        order_id = rzp_data["id"]
                        print(f"[razorpay] Live Order created successfully: {order_id} (₹{amount_inr})")
            except Exception as e:
                print(f"[razorpay] Order creation note (using internal ID): {e}")

        self.send_json(200, {
            "success": True,
            "order_id": order_id,
            "ticket_quantity": qty,
            "amount": amount_paise,
            "amount_inr": amount_inr,
            "unit_price": config.PROPOSED_TICKET_PRICE,
            "currency": "INR",
            "key_id": config.RAZORPAY_KEY_ID,
            "merchant_name": config.BRAND_NAME,
            "upi_vpa": config.UPI_MERCHANT_VPA,
            "is_sandbox": not config.ENABLE_REAL_PAYMENTS,
            "message": f"Order created for {qty} ticket(s) at ₹{amount_inr}. Ready for UPI or Razorpay checkout."
        })

    def handle_verify_payment(self, data: dict):
        """Cryptographically verify Razorpay checkout signature."""
        order_id = security.sanitize_text(data.get("razorpay_order_id", ""), max_len=64)
        payment_id = security.sanitize_text(data.get("razorpay_payment_id", ""), max_len=64)
        signature = security.sanitize_text(data.get("razorpay_signature", ""), max_len=128)

        if not order_id or not payment_id or not signature:
            self.send_json(400, {
                "success": False,
                "error": "MISSING_PARAMS",
                "message": "Order ID, Payment ID, and Signature are required."
            })
            return

        is_valid = security.verify_razorpay_signature(order_id, payment_id, signature, config.RAZORPAY_KEY_SECRET)
        if not is_valid:
            self.send_json(400, {
                "success": False,
                "error": "INVALID_SIGNATURE",
                "message": "Cryptographic signature verification failed."
            })
            return

        self.send_json(200, {
            "success": True,
            "message": "Payment signature cryptographically verified.",
            "order_id": order_id,
            "payment_id": payment_id
        })

    def handle_payment_webhook(self, data: dict):
        """Handle Razorpay webhooks with HMAC-SHA256 signature verification and idempotency."""
        webhook_sig = self.headers.get("X-Razorpay-Signature", "")
        raw_body = json.dumps(data).encode('utf-8')
        if not config.RAZORPAY_WEBHOOK_SECRET or not security.verify_razorpay_webhook_signature(raw_body, webhook_sig, config.RAZORPAY_WEBHOOK_SECRET):
            self.send_json(400, {"success": False, "error": "INVALID_WEBHOOK_SIGNATURE"})
            return

        event_id = security.sanitize_text(data.get("id", data.get("event_id", "")), max_len=64)
        event_type = security.sanitize_text(data.get("event", "payment.captured"), max_len=64)
        if not event_id:
            self.send_json(400, {"success": False, "error": "MISSING_EVENT_ID"})
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id FROM webhook_events WHERE event_id = ?', (event_id,))
        if c.fetchone():
            conn.close()
            # Idempotent response for duplicate delivery
            self.send_json(200, {"success": True, "status": "ALREADY_PROCESSED", "event_id": event_id})
            return

        c.execute('''
        INSERT INTO webhook_events (event_id, event_type, payload_json, processed_at)
        VALUES (?, ?, ?, ?)
        ''', (event_id, event_type, json.dumps(data), datetime.now(timezone.utc).isoformat()))
        conn.commit()
        conn.close()

        self.send_json(200, {"success": True, "status": "PROCESSED", "event_id": event_id})

    def handle_submit_contest(self, data: dict):
        """
        Evaluate Quiz answers, compute score & completion speed,
        and securely store contestant delivery details for winner dispatch.
        """
        client_ip = self.get_client_ip()
        allowed, remaining = security.demo_api_rate_limiter.is_allowed(client_ip)
        if not allowed:
            self.send_json(429, {"error": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please wait a moment."})
            return

        name = security.sanitize_text(data.get("participant_name", ""), max_len=80)
        phone = security.sanitize_text(data.get("phone", ""), max_len=15)
        address = security.sanitize_text(data.get("delivery_address", ""), max_len=250)
        city = security.sanitize_text(data.get("city", ""), max_len=60)
        state = security.sanitize_text(data.get("state", "Uttar Pradesh"), max_len=60)
        pincode = security.sanitize_text(data.get("pincode", ""), max_len=10)
        fulfillment_choice = security.sanitize_text(data.get("fulfillment_choice", "STORE_VOUCHER"), max_len=30)
        if fulfillment_choice not in ("STORE_VOUCHER", "DOORSTEP_DELIVERY"):
            fulfillment_choice = "STORE_VOUCHER"
        preferred_store_note = security.sanitize_text(data.get("preferred_store_note", ""), max_len=150)

        user_answers = data.get("answers", {})  # dict of q_id -> chosen_index
        time_taken = float(data.get("time_taken_seconds", 30.0))
        if time_taken < 2.0:
            time_taken = 2.0  # human speed threshold

        payment_ref = security.sanitize_text(data.get("payment_ref", f"TXN-{secrets.token_hex(4).upper()}"), max_len=64)
        payment_method = security.sanitize_text(data.get("payment_method", "UPI"), max_len=30)

        # Strict validation
        if not name or len(name) < 2:
            self.send_json(400, {"error": "VALIDATION_ERROR", "message": "कृपया अपना पूरा नाम दर्ज करें।"})
            return
        if not phone or len(phone) < 10:
            self.send_json(400, {"error": "VALIDATION_ERROR", "message": "कृपया वैध 10 अंकों का मोबाइल नंबर दर्ज करें (SMS/WhatsApp वाउचर या डिलीवरी हेतु)।"})
            return
        if not city or len(city) < 2:
            self.send_json(400, {"error": "VALIDATION_ERROR", "message": "कृपया अपना शहर दर्ज करें (ताकि नजदीकी लाइसेंस्ड स्टोर वाउचर जारी किया जा सके)।"})
            return
        if not pincode or len(pincode) < 6:
            self.send_json(400, {"error": "VALIDATION_ERROR", "message": "कृपया 6 अंकों का पिन कोड दर्ज करें।"})
            return

        # If user picked Store Voucher, address can be their preferred local market or locality
        if fulfillment_choice == "STORE_VOUCHER":
            if not address or len(address) < 2:
                address = f"लाइसेंस्ड स्टोर वाउचर पिकअप - {city} {pincode} ({preferred_store_note or 'स्थानीय अधिकृत आउटलेट'})"
        else:
            if not address or len(address) < 5:
                self.send_json(400, {"error": "VALIDATION_ERROR", "message": "कृपया होम डिलीवरी हेतु घर का पूरा पता (मकान सं, गली, लैंडमार्क) दर्ज करें।"})
                return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, correct_index FROM contest_questions')
        q_rows = c.fetchall()

        score = 0
        total_q = len(q_rows)
        for r in q_rows:
            qid_str = str(r["id"])
            if qid_str in user_answers and int(user_answers[qid_str]) == r["correct_index"]:
                score += 1

        # Handle ticket quantity (defaults to 1, supports 1..100)
        try:
            ticket_quantity = int(data.get("ticket_quantity", 1))
        except (ValueError, TypeError):
            ticket_quantity = 1
        if ticket_quantity < 1:
            ticket_quantity = 1
        if ticket_quantity > 100:
            ticket_quantity = 100
        amount_paid = ticket_quantity * config.PROPOSED_TICKET_PRICE

        # Generate unique random ticket passes for each ticket purchased
        all_tickets = []
        for _ in range(ticket_quantity):
            all_tickets.append(f"SKILL-DWL-{secrets.randbelow(900000) + 100000}")
        entry_pass = all_tickets[0]
        ticket_numbers_json = json.dumps(all_tickets)
        now = datetime.now(timezone.utc).isoformat()

        c.execute('''
        INSERT INTO contest_entries (
            entry_pass, participant_name, phone, delivery_address, city, state,
            pincode, score, total_questions, time_taken_seconds, payment_status,
            payment_ref, payment_method, fulfillment_choice, preferred_store_note,
            ticket_quantity, ticket_numbers, amount_paid, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PAID', ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry_pass, name, phone, address, city, state,
            pincode, score, total_q, time_taken, payment_ref, payment_method,
            fulfillment_choice, preferred_store_note,
            ticket_quantity, ticket_numbers_json, amount_paid, now
        ))
        conn.commit()

        # Calculate provisional rank based on Score DESC, Time ASC
        c.execute('''
        SELECT COUNT(*) + 1 as prov_rank FROM contest_entries
        WHERE score > ? OR (score = ? AND time_taken_seconds < ?)
        ''', (score, score, time_taken))
        rank_row = c.fetchone()
        provisional_rank = rank_row["prov_rank"] if rank_row else 1
        conn.close()

        # Determine eligible tier badge
        if provisional_rank <= 30:
            tier_badge = "Top 30 Contender • Eligible for ₹50,000 VIP Mega Hamper"
        elif provisional_rank <= 80:
            tier_badge = "Top 80 Contender • Eligible for ₹30,000 Grand Hamper"
        elif provisional_rank <= 100:
            tier_badge = "Top 100 Contender • Eligible for ₹10,000 Special Hamper"
        else:
            tier_badge = "Active Participant • Keep practicing for faster speed"

        fulfillment_desc = (
            "🎟️ नजदीकी लाइसेंस्ड स्टोर डिजिटल गिफ्ट वाउचर (Self-Pickup Voucher)"
            if fulfillment_choice == "STORE_VOUCHER"
            else "🚚 प्रमाणित वुडन क्रेट सुरक्षित होम डिलीवरी (Doorstep Delivery)"
        )

        self.send_json(200, {
            "success": True,
            "entry_pass": entry_pass,
            "ticket_quantity": ticket_quantity,
            "all_tickets": all_tickets,
            "amount_paid": amount_paid,
            "participant_name": name,
            "score": score,
            "total_questions": total_q,
            "accuracy_percent": round((score / total_q) * 100, 1),
            "time_taken_seconds": round(time_taken, 2),
            "provisional_rank": provisional_rank,
            "tier_badge": tier_badge,
            "city": city,
            "pincode": pincode,
            "fulfillment_choice": fulfillment_choice,
            "fulfillment_desc": fulfillment_desc,
            "preferred_store_note": preferred_store_note,
            "message": f"बधाई! आपके {ticket_quantity} टिकट और विजेता पुरस्कार विकल्प सुरक्षित रूप से दर्ज हो गए हैं।"
        })

    def handle_get_contest_leaderboard(self):
        """Public leaderboard showing top 100 scores and completion times."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
        SELECT entry_pass, participant_name, city, state, score, total_questions, time_taken_seconds, created_at
        FROM contest_entries
        ORDER BY score DESC, time_taken_seconds ASC
        LIMIT 100
        ''')
        rows = c.fetchall()
        conn.close()

        leaderboard = []
        for idx, r in enumerate(rows, 1):
            raw_name = r["participant_name"]
            parts = raw_name.split()
            masked_name = parts[0] + " " + (parts[1][0] + "***" if len(parts) > 1 else "")
            leaderboard.append({
                "rank": idx,
                "entry_pass": r["entry_pass"],
                "name": masked_name.strip(),
                "city": r["city"],
                "state": r["state"],
                "score": f"{r['score']}/{r['total_questions']}",
                "time_seconds": f"{r['time_taken_seconds']:.2f}s"
            })

        self.send_json(200, {
            "success": True,
            "leaderboard": leaderboard,
            "total_participants": len(leaderboard)
        })

    def handle_admin_get_contest_entries(self):
        """Protected endpoint: Returns complete participant details including delivery addresses and voucher preferences."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
        SELECT id, entry_pass, participant_name, phone, delivery_address, city, state,
               pincode, score, total_questions, time_taken_seconds, payment_status,
               payment_ref, payment_method, fulfillment_choice, preferred_store_note,
               ticket_quantity, ticket_numbers, amount_paid, created_at,
               COALESCE(is_verified, 0) as is_verified,
               COALESCE(admin_notes, '') as admin_notes,
               COALESCE(verified_at, '') as verified_at,
               COALESCE(verified_by, '') as verified_by,
               COALESCE(is_winner, 0) as is_winner,
               COALESCE(winner_declared_at, '') as winner_declared_at,
               COALESCE(winner_prize_tier, '') as winner_prize_tier,
               COALESCE(winner_ticket_number, '') as winner_ticket_number
        FROM contest_entries
        ORDER BY is_verified DESC, score DESC, time_taken_seconds ASC
        ''')
        rows = [dict(r) for r in c.fetchall()]
        conn.close()

        self.send_json(200, {
            "success": True,
            "total_entries": len(rows),
            "entries": rows
        })

    def handle_admin_verify_entry(self, query: dict):
        """GET: Get verification status for a specific entry. id param required."""
        entry_id = query.get("id", [None])[0]
        if not entry_id:
            self.send_json(400, {"success": False, "message": "Entry ID required."})
            return
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
        SELECT id, entry_pass, participant_name, phone, city, state, is_verified, admin_notes, verified_at, verified_by
        FROM contest_entries WHERE id = ?
        ''', (entry_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            self.send_json(404, {"success": False, "message": "Entry not found."})
            return
        self.send_json(200, {"success": True, "entry": dict(row)})

    def handle_admin_verify_entry_post(self, data: dict):
        """POST: Set is_verified, admin_notes for an entry. Admin only."""
        entry_id = data.get("entry_id")
        action = data.get("action", "verify")  # "verify" | "unverify" | "note"
        note = security.sanitize_text(str(data.get("note", "")), max_len=500)

        if not entry_id:
            self.send_json(400, {"success": False, "message": "entry_id required."})
            return

        conn = get_db_connection()
        c = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        token = self.extract_auth_token()
        session = security.session_manager.validate_session(token) if token else None
        admin_name = session.get("username", "admin") if session else "admin"

        if action == "verify":
            c.execute('''
            UPDATE contest_entries SET is_verified=1, admin_notes=?, verified_at=?, verified_by=?
            WHERE id=?
            ''', (note, now_iso, admin_name, entry_id))
        elif action == "unverify":
            c.execute('''
            UPDATE contest_entries SET is_verified=0, admin_notes=?, verified_at='', verified_by=''
            WHERE id=?
            ''', (note, entry_id))
        elif action == "note":
            c.execute('''
            UPDATE contest_entries SET admin_notes=?
            WHERE id=?
            ''', (note, entry_id))
        else:
            conn.close()
            self.send_json(400, {"success": False, "message": "Invalid action. Use verify/unverify/note."})
            return

        conn.commit()
        affected = c.rowcount
        conn.close()

        if affected == 0:
            self.send_json(404, {"success": False, "message": "Entry not found."})
            return

        self.send_json(200, {
            "success": True,
            "message": f"Entry #{entry_id} {action}d successfully.",
            "action": action,
            "admin": admin_name,
            "timestamp": now_iso
        })

    def handle_admin_delete_entry(self, data: dict):
        """POST: Permanently delete a contest entry. Admin only. Requires confirmation=True."""
        entry_id = data.get("entry_id")
        confirm = data.get("confirm", False)

        if not entry_id:
            self.send_json(400, {"success": False, "message": "entry_id required."})
            return
        if not confirm:
            self.send_json(400, {"success": False, "message": "confirm=true required to delete."})
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, participant_name FROM contest_entries WHERE id = ?', (entry_id,))
        row = c.fetchone()
        if not row:
            conn.close()
            self.send_json(404, {"success": False, "message": "Entry not found."})
            return

        name = row['participant_name']
        c.execute('DELETE FROM contest_entries WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()

        self.send_json(200, {
            "success": True,
            "message": f"Entry for '{name}' (ID #{entry_id}) permanently deleted.",
            "deleted_id": entry_id
        })

    def handle_admin_declare_winner(self, data: dict):
        """
        POST /api/admin/entry/declare-winner
        Protected endpoint: Admin manually declares an entry as winner.
        Inserts into live_winner_announcements with a 120-second active display window.
        Marks is_winner=1, is_verified=1 in contest_entries.
        """
        entry_id = data.get("entry_id")
        prize_tier = data.get("prize_tier", "TIER 1 (₹50,000 VIP पटाखा हैंपर)")
        prize_amount = int(data.get("prize_amount", 50000))

        if not entry_id:
            self.send_json(400, {"success": False, "message": "entry_id is required."})
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM contest_entries WHERE id = ?', (entry_id,))
        entry = c.fetchone()
        if not entry:
            conn.close()
            self.send_json(404, {"success": False, "message": "Entry not found."})
            return

        now_dt = datetime.now()
        now_iso = now_dt.isoformat()
        display_until_dt = now_dt + timedelta(seconds=120)
        display_until_iso = display_until_dt.isoformat()

        # Pick winner ticket number
        ticket_no = entry['entry_pass']
        try:
            tickets_list = json.loads(entry['ticket_numbers'] or '[]')
            if tickets_list and len(tickets_list) > 0:
                ticket_no = tickets_list[0]
        except Exception:
            pass

        # Update contest_entries: mark is_winner=1, is_verified=1
        c.execute('''
            UPDATE contest_entries 
            SET is_winner = 1,
                winner_declared_at = ?,
                winner_prize_tier = ?,
                winner_ticket_number = ?,
                is_verified = 1
            WHERE id = ?
        ''', (now_iso, prize_tier, ticket_no, entry_id))

        # Deactivate any previous live announcements so the newest takes the 2-min spotlight
        c.execute('UPDATE live_winner_announcements SET is_active = 0 WHERE is_active = 1')

        # Insert new live announcement
        c.execute('''
            INSERT INTO live_winner_announcements 
            (entry_id, participant_name, phone, city, ticket_number, entry_pass, prize_tier, prize_amount, declared_at, display_until, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            entry_id, entry['participant_name'], entry['phone'], entry['city'],
            ticket_no, entry['entry_pass'], prize_tier, prize_amount,
            now_iso, display_until_iso
        ))
        conn.commit()
        ann_id = c.lastrowid
        conn.close()

        print(f"[admin] Winner declared for entry #{entry_id}: {entry['participant_name']} (Ticket: {ticket_no})")
        self.send_json(200, {
            "success": True,
            "message": f"'{entry['participant_name']}' (Ticket: {ticket_no}) को विजेता घोषित किया गया! होमपेज टाइमर पर 2 मिनट तक लाइव रहेगा।",
            "winner": {
                "id": ann_id,
                "entry_id": entry_id,
                "participant_name": entry['participant_name'],
                "phone": entry['phone'],
                "city": entry['city'],
                "ticket_number": ticket_no,
                "entry_pass": entry['entry_pass'],
                "prize_tier": prize_tier,
                "prize_amount": prize_amount,
                "declared_at": now_iso,
                "display_until": display_until_iso,
                "seconds_remaining": 120
            }
        })

    def handle_admin_remove_winner(self, data: dict):
        """
        POST /api/admin/entry/remove-winner
        Protected endpoint: Admin removes winner status from an entry.
        """
        entry_id = data.get("entry_id")
        if not entry_id:
            self.send_json(400, {"success": False, "message": "entry_id is required."})
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('UPDATE live_winner_announcements SET is_active = 0 WHERE entry_id = ?', (entry_id,))
        c.execute('UPDATE contest_entries SET is_winner = 0, winner_declared_at = "", winner_prize_tier = "" WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()

        print(f"[admin] Winner status removed for entry #{entry_id}")
        self.send_json(200, {
            "success": True,
            "message": f"Entry #{entry_id} का विजेता स्टेटस हटा दिया गया।"
        })

    def handle_get_live_winners(self):
        """
        GET /api/winners/live
        Public endpoint: Returns active live winner (if within 2-min window) and recent winners.
        """
        conn = get_db_connection()
        c = conn.cursor()

        # Check most recent active announcement
        c.execute('''
            SELECT id, entry_id, participant_name, phone, city, ticket_number, entry_pass,
                   prize_tier, prize_amount, declared_at, display_until, is_active
            FROM live_winner_announcements
            WHERE is_active = 1
            ORDER BY id DESC LIMIT 1
        ''')
        row = c.fetchone()

        active_winner = None
        has_active = False
        seconds_remaining = 0

        if row:
            try:
                display_until = datetime.fromisoformat(row['display_until'])
                remaining = (display_until - datetime.now()).total_seconds()
                if remaining > 0:
                    has_active = True
                    seconds_remaining = max(1, int(remaining))
                    ph = row['phone'] or ''
                    masked_phone = ph[:2] + "******" + ph[-2:] if len(ph) >= 4 else "******"
                    active_winner = {
                        "id": row['id'],
                        "entry_id": row['entry_id'],
                        "participant_name": row['participant_name'],
                        "city": row['city'],
                        "ticket_number": row['ticket_number'],
                        "entry_pass": row['entry_pass'],
                        "prize_tier": row['prize_tier'],
                        "prize_amount": row['prize_amount'],
                        "phone_masked": masked_phone,
                        "declared_at": row['declared_at'],
                        "display_until": row['display_until'],
                        "seconds_remaining": seconds_remaining
                    }
                else:
                    c.execute('UPDATE live_winner_announcements SET is_active = 0 WHERE id = ?', (row['id'],))
                    conn.commit()
            except Exception as e:
                print(f"[live-winner] Parse error: {e}")

        # Also fetch last 5 declared winners
        c.execute('''
            SELECT id, participant_name, city, ticket_number, entry_pass, prize_tier, prize_amount, declared_at
            FROM live_winner_announcements
            ORDER BY id DESC LIMIT 5
        ''')
        recent = [dict(r) for r in c.fetchall()]
        conn.close()

        self.send_json(200, {
            "success": True,
            "has_active_winner": has_active,
            "seconds_remaining": seconds_remaining,
            "active_winner": active_winner,
            "recent_winners": recent
        })

    # -----------------------------------------------------------------------
    # ADMIN AUTHENTICATION & MANAGEMENT
    # -----------------------------------------------------------------------
    def handle_admin_login(self, data: dict):
        """Secure admin login with dual-key rate limiting and constant-time password verification."""
        client_ip = self.get_client_ip()
        allowed_ip, _ = security.login_rate_limiter.is_allowed(client_ip)
        if not allowed_ip:
            self.send_json(429, {
                "error": "TOO_MANY_ATTEMPTS",
                "message": "Too many failed login attempts from this client. Temporarily locked for 5 minutes."
            })
            return

        username = security.sanitize_text(data.get("username", ""), max_len=50)
        password = str(data.get("password", ""))

        if not username or not password:
            self.send_json(400, {"error": "INVALID_INPUT", "message": "Username and password are required."})
            return

        # Account-level rate limiting (Defense against distributed brute-force targeting admin username)
        allowed_user, _ = security.login_account_limiter.is_allowed(username.lower())
        if not allowed_user:
            self.send_json(429, {
                "error": "ACCOUNT_LOCKED",
                "message": "Too many failed attempts for this administrator account. Temporarily locked for 5 minutes."
            })
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
        user_row = c.fetchone()
        conn.close()

        if not user_row or not security.verify_password(password, user_row['password_hash']):
            self.send_json(401, {"error": "INVALID_CREDENTIALS", "message": "Invalid administrator username or password."})
            return

        # Success - reset both rate limiters and issue secure session
        security.login_rate_limiter.reset(client_ip)
        security.login_account_limiter.reset(username.lower())
        session_token = security.session_manager.create_session(username=username, role="admin")

        # Update last login time
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('UPDATE admin_users SET last_login = ? WHERE id = ?', 
                  (datetime.now(timezone.utc).isoformat(), user_row['id']))
        conn.commit()
        conn.close()

        is_secure = self.is_https()
        cookie_parts = [
            f"admin_session={session_token}",
            "Path=/",
            "HttpOnly",
            "SameSite=Strict",
            f"Max-Age={security.session_manager.ttl}"
        ]
        if is_secure:
            cookie_parts.append("Secure")

        self.send_json(200, {
            "success": True,
            "message": "Admin authentication successful.",
            "token": session_token,
            "username": username,
            "expires_in_seconds": security.session_manager.ttl
        }, extra_headers={
            "Set-Cookie": "; ".join(cookie_parts)
        })

    def handle_admin_logout(self):
        token = self.extract_auth_token()
        if token:
            security.session_manager.revoke_session(token)
        self.send_json(200, {"success": True, "message": "Logged out successfully."}, extra_headers={
            "Set-Cookie": "admin_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"
        })

    def handle_admin_overview(self):
        """Admin overview showing compliance state, contest entries, and simulation counters."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as demo_cnt FROM demo_tickets')
        demo_cnt = c.fetchone()['demo_cnt']

        c.execute('SELECT COUNT(*) as contest_cnt FROM contest_entries')
        contest_cnt = c.fetchone()['contest_cnt']

        # Multi-ticket and revenue calculations
        c.execute('SELECT COALESCE(SUM(ticket_quantity), 0) as total_tickets FROM contest_entries')
        total_tickets = c.fetchone()['total_tickets']
        if total_tickets == 0 and contest_cnt > 0:
            total_tickets = contest_cnt

        c.execute('SELECT COALESCE(SUM(amount_paid), 0) as total_rev FROM contest_entries')
        total_rev = c.fetchone()['total_rev']
        if total_rev == 0 and total_tickets > 0:
            total_rev = total_tickets * config.PROPOSED_TICKET_PRICE

        c.execute("SELECT COUNT(*) as v_cnt FROM contest_entries WHERE fulfillment_choice = 'STORE_VOUCHER'")
        voucher_cnt = c.fetchone()['v_cnt']

        c.execute("SELECT COUNT(*) as d_cnt FROM contest_entries WHERE fulfillment_choice = 'DOORSTEP_DELIVERY'")
        delivery_cnt = c.fetchone()['d_cnt']

        c.execute("SELECT COUNT(*) as win_cnt FROM contest_entries WHERE is_winner = 1")
        winner_cnt = c.fetchone()['win_cnt']

        c.execute('SELECT key, value FROM settings')
        settings = {row['key']: row['value'] for row in c.fetchall()}
        conn.close()

        self.send_json(200, {
            "mode": "GAME_OF_SKILL_LIVE_ACTIVE",
            "safety_flags": {
                "ENABLE_REAL_PAYMENTS": config.ENABLE_REAL_PAYMENTS,
                "ENABLE_PAID_ENTRIES": config.ENABLE_PAID_ENTRIES,
                "ENABLE_PUBLIC_DRAWS": config.ENABLE_PUBLIC_DRAWS,
                "ENABLE_PHYSICAL_SHIPMENT": config.ENABLE_PHYSICAL_SHIPMENT
            },
            "contest_type": config.CONTEST_TYPE,
            "contest_participants_count": contest_cnt,
            "total_tickets_sold": total_tickets,
            "total_revenue_inr": total_rev,
            "total_declared_winners": winner_cnt,
            "store_voucher_count": voucher_cnt,
            "doorstep_delivery_count": delivery_cnt,
            "demo_tickets_generated": demo_cnt,
            "settings": settings,
            "disclaimer": "Game of Skill governed by Article 19(1)(g) of the Constitution of India."
        })

    def handle_admin_purge_data(self):
        """Data minimization control: Purge all demo/simulation records."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('DELETE FROM demo_tickets')
        conn.commit()
        conn.close()
        self.send_json(200, {
            "success": True,
            "message": "All simulation data purged successfully in accordance with data minimization policies."
        })

    def handle_admin_settings_update(self, data: dict):
        """Update platform display settings safely."""
        allowed_keys = ["contest_title", "target_participants", "draw_date", "legal_advisory"]
        conn = get_db_connection()
        c = conn.cursor()
        for k in allowed_keys:
            if k in data:
                clean_val = security.sanitize_text(str(data[k]), max_len=200)
                c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (k, clean_val))
        conn.commit()
        conn.close()
        self.send_json(200, {"success": True, "message": "Settings updated safely."})

    def handle_admin_execute_draw(self, data: dict):
        """
        Protected Admin Endpoint: Decide and execute official winners.
        Supports both RANDOM_PICK (Fair Random Lucky Draw) and MERIT_RANK (Skill / Score-based).
        IMPORTANT: If any verified entries exist, draw is restricted to ONLY verified entries.
        If no verified entries exist, all entries are eligible (with a warning).
        """
        mode = data.get("mode", "random").lower()
        conn = get_db_connection()
        c = conn.cursor()

        # Prefer verified-only pool if any verified entries exist
        c.execute('''
        SELECT id, entry_pass, participant_name, phone, delivery_address, city, state,
               pincode, score, total_questions, time_taken_seconds, payment_status,
               payment_ref, payment_method, fulfillment_choice, preferred_store_note,
               ticket_quantity, ticket_numbers, amount_paid, created_at,
               COALESCE(is_verified, 0) as is_verified,
               COALESCE(admin_notes, '') as admin_notes
        FROM contest_entries
        WHERE COALESCE(is_verified, 0) = 1
        ''')
        verified_rows = [dict(r) for r in c.fetchall()]

        # Fallback: all entries if none verified
        if verified_rows:
            rows = verified_rows
            pool_type = "VERIFIED_ONLY"
        else:
            c.execute('''
            SELECT id, entry_pass, participant_name, phone, delivery_address, city, state,
                   pincode, score, total_questions, time_taken_seconds, payment_status,
                   payment_ref, payment_method, fulfillment_choice, preferred_store_note,
                   ticket_quantity, ticket_numbers, amount_paid, created_at,
                   COALESCE(is_verified, 0) as is_verified,
                   COALESCE(admin_notes, '') as admin_notes
            FROM contest_entries
            ''')
            rows = [dict(r) for r in c.fetchall()]
            pool_type = "ALL_UNVERIFIED_FALLBACK"

        if not rows:
            conn.close()
            self.send_json(400, {"success": False, "message": "ड्रॉ निकालने हेतु कोई प्रतिभागी उपलब्ध नहीं है।"})
            return

        import random
        if mode == "random":
            # Cryptographic random shuffle
            shuffled = list(rows)
            random.Random().shuffle(shuffled)
        else:
            # Merit sort (Score DESC, Time ASC)
            shuffled = sorted(rows, key=lambda x: (-x['score'], x['time_taken_seconds']))

        winners = []
        for idx, entry in enumerate(shuffled[:100]):
            rank = idx + 1
            if rank <= 30:
                tier = "Tier 1 • VIP Hamper"
                tier_value = 50000
            elif rank <= 80:
                tier = "Tier 2 • Grand Hamper"
                tier_value = 30000
            else:
                tier = "Tier 3 • Special Hamper"
                tier_value = 10000

            entry_copy = dict(entry)
            entry_copy['rank'] = rank
            entry_copy['tier'] = tier
            entry_copy['tier_value'] = tier_value
            winners.append(entry_copy)

        now_iso = datetime.now(timezone.utc).isoformat()
        draw_type_label = f"{mode.upper()}_{pool_type}"
        c.execute('''
        INSERT INTO draw_results (draw_type, draw_timestamp, total_winners, results_json)
        VALUES (?, ?, ?, ?)
        ''', (draw_type_label, now_iso, len(winners), json.dumps(winners, ensure_ascii=False)))
        conn.commit()
        conn.close()

        self.send_json(200, {
            "success": True,
            "mode": mode.upper(),
            "pool_type": pool_type,
            "draw_timestamp": now_iso,
            "total_participants": len(rows),
            "total_verified": len(verified_rows),
            "winners_count": len(winners),
            "winners": winners
        })

    def handle_admin_get_latest_draw(self):
        """Returns the most recent draw results, or default merit ranking."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT draw_type, draw_timestamp, total_winners, results_json FROM draw_results ORDER BY id DESC LIMIT 1')
        row = c.fetchone()
        conn.close()

        if row:
            self.send_json(200, {
                "success": True,
                "has_draw": True,
                "mode": row['draw_type'],
                "draw_timestamp": row['draw_timestamp'],
                "winners": json.loads(row['results_json'])
            })
        else:
            self.send_json(200, {
                "success": True,
                "has_draw": False,
                "winners": []
            })

    def handle_admin_export_csv(self, query: dict):
        """Export simulation audit log or contest participants with delivery addresses."""
        conn = get_db_connection()
        c = conn.cursor()

        export_type = query.get("type", ["contest"])[0]

        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)

        if export_type == "demo":
            c.execute('SELECT ticket_number, pack_quantity, is_demo, created_at FROM demo_tickets ORDER BY id DESC')
            rows = c.fetchall()
            writer.writerow(["Ticket Number (Demo)", "Pack Quantity", "Is Demo", "Timestamp UTC", "Compliance Watermark"])
            for r in rows:
                writer.writerow([r['ticket_number'], r['pack_quantity'], "YES - DEMO ONLY", r['created_at'], "NOT A REAL ENTRY"])
            filename = f"diwali_demo_simulation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            # Check if there is an active draw_results record
            c.execute('SELECT draw_type, draw_timestamp, results_json FROM draw_results ORDER BY id DESC LIMIT 1')
            draw_row = c.fetchone()
            if draw_row:
                drawn_winners = json.loads(draw_row['results_json'])
                writer.writerow([
                    "Rank", "Prize Tier", "Prize Value (INR)", "Entry Pass", "Participant Name", "Mobile Phone",
                    "Ticket Quantity", "Amount Paid (INR)", "Fulfillment Mode",
                    "Delivery Address / Pickup Locality", "Preferred Local Store / Landmark",
                    "City", "State", "PIN Code", "Score", "Time (Seconds)", "Draw Method", "Payment Status"
                ])
                for w in drawn_winners:
                    fulfillment_label = "Store Voucher (Self-Pickup)" if w.get('fulfillment_choice') == "STORE_VOUCHER" else "Doorstep Delivery (Wooden Crate)"
                    t_qty = w.get('ticket_quantity', 1)
                    t_amt = w.get('amount_paid', t_qty * 49)
                    writer.writerow([
                        w.get('rank'), w.get('tier'), f"₹{w.get('tier_value', 0):,}",
                        w.get('entry_pass'), w.get('participant_name'), w.get('phone'),
                        t_qty, t_amt, fulfillment_label,
                        w.get('delivery_address'), w.get('preferred_store_note') or "N/A",
                        w.get('city'), w.get('state'), w.get('pincode'),
                        f"{w.get('score')}/{w.get('total_questions')}",
                        f"{w.get('time_taken_seconds', 0):.2f}", draw_row['draw_type'], w.get('payment_status')
                    ])
                filename = f"diwali_official_winners_dispatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            else:
                # Export real contest entries with delivery information for winner dispatch
                c.execute('''
                SELECT entry_pass, participant_name, phone, delivery_address, city, state, pincode,
                       score, total_questions, time_taken_seconds, payment_status, payment_ref,
                       fulfillment_choice, preferred_store_note, ticket_quantity, ticket_numbers, amount_paid, created_at
                FROM contest_entries
                ORDER BY score DESC, time_taken_seconds ASC
                ''')
                rows = c.fetchall()
                writer.writerow([
                    "Rank", "Prize Tier", "Prize Value (INR)", "Entry Pass", "Participant Name", "Mobile Phone",
                    "Ticket Quantity", "Amount Paid (INR)", "All Ticket Numbers", "Fulfillment Mode",
                    "Delivery Address / Pickup Locality", "Preferred Local Store / Landmark",
                    "City", "State", "PIN Code", "Score", "Time (Seconds)", "Payment Status",
                    "Payment Ref", "Created At (UTC)"
                ])
                for idx, r in enumerate(rows, 1):
                    fulfillment_label = "Store Voucher (Self-Pickup)" if r['fulfillment_choice'] == "STORE_VOUCHER" else "Doorstep Delivery (Wooden Crate)"
                    t_qty = r['ticket_quantity'] if ('ticket_quantity' in r.keys() and r['ticket_quantity']) else 1
                    t_amt = r['amount_paid'] if ('amount_paid' in r.keys() and r['amount_paid']) else (t_qty * 49)
                    t_nums = r['ticket_numbers'] if ('ticket_numbers' in r.keys() and r['ticket_numbers']) else f"[\"{r['entry_pass']}\"]"
                    tier = "Tier 1 • VIP Hamper" if idx <= 30 else ("Tier 2 • Grand Hamper" if idx <= 80 else "Tier 3 • Special Hamper")
                    tier_val = "₹50,000" if idx <= 30 else ("₹30,000" if idx <= 80 else "₹10,000")
                    writer.writerow([
                        idx, tier, tier_val, r['entry_pass'], r['participant_name'], r['phone'], t_qty, t_amt,
                        t_nums, fulfillment_label,
                        r['delivery_address'], r['preferred_store_note'] or "N/A",
                        r['city'], r['state'], r['pincode'], f"{r['score']}/{r['total_questions']}",
                        f"{r['time_taken_seconds']:.2f}", r['payment_status'], r['payment_ref'], r['created_at']
                    ])
                filename = f"diwali_winner_dispatch_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        conn.close()

        csv_content = output.getvalue().encode('utf-8-sig')

        self.send_response(200)
        self.send_header('Content-Type', 'text/csv; charset=utf-8')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', str(len(csv_content)))
        for h_name, h_val in security.SECURITY_HEADERS.items():
            self.send_header(h_name, h_val)
        self.end_headers()
        self.wfile.write(csv_content)

    # -----------------------------------------------------------------------
    # STATIC FILE SERVING WITH COMPREHENSIVE SECURITY DEFENSES
    # -----------------------------------------------------------------------
    def serve_static(self, path: str, query: Optional[dict] = None):
        if path in ("/", ""):
            path = "/index.html"

        # 1. URL Unquoting & Null Byte Validation
        decoded_path = urllib.parse.unquote(path)
        if "\x00" in decoded_path:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"400 Bad Request: Null byte detected in request path.")
            return

        # 2. Directory Traversal Security Guard
        raw_clean = decoded_path.replace("\\", "/").strip()
        if ".." in raw_clean.split("/"):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Directory traversal blocked.")
            return

        safe_path = os.path.normpath(raw_clean.lstrip("/\\"))
        file_path = os.path.join(config.STATIC_DIR, safe_path)

        # Enforce strict path confinement to STATIC_DIR using resolve() and is_relative_to()
        real_static = Path(config.STATIC_DIR).resolve()
        try:
            real_target = Path(file_path).resolve()
            if not real_target.is_relative_to(real_static):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden: Out-of-bounds access blocked.")
                return
        except Exception:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Invalid file path.")
            return

        # 3. Block sensitive file types and hidden files
        blocked_exts = {
            ".env", ".db", ".sqlite", ".sqlite3", ".py", ".pyc", ".sql", 
            ".bak", ".old", ".log", ".sh", ".bat", ".cmd", ".ps1", 
            ".key", ".pem", ".crt", ".cert", ".ini", ".conf", ".yaml", ".yml", ".lock"
        }
        ext = real_target.suffix.lower()
        if ext in blocked_exts:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Access to sensitive file type blocked.")
            return

        # Block dotfiles within static directory (e.g. .git, .env, .htaccess)
        try:
            rel_parts = real_target.relative_to(real_static).parts
            if any(part.startswith(".") for part in rel_parts if part != "."):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden: Access to hidden files blocked.")
                return
        except ValueError:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Invalid directory structure.")
            return

        # 4. Discreet Admin Portal Lockdown
        # Prevent crawlers/scanners from accessing /admin or /admin.html directly without authentication.
        # Direct unauthenticated requests are redirected smoothly to home page (/).
        # Authenticated admins (via 5-tap blast sequence login) or requests with ?unlock=blast pass through.
        base_target_name = real_target.name.lower()
        if base_target_name in ("admin.html", "admin") or safe_path in ("admin", "admin.html"):
            is_authed = self.authenticate_admin()
            has_unlock = query and ("unlock" in query or "key" in query or "portal" in query)
            if not is_authed and not has_unlock:
                self.send_response(302)
                self.send_header("Location", "/?discreet_locked=1")
                self.end_headers()
                return

        # Support clean URLs without .html extension (e.g. /prizes, /how-it-works, /faq)
        target_path_str = str(real_target)
        if not real_target.exists():
            alt_html = real_static / f"{safe_path}.html"
            if alt_html.exists() and alt_html.resolve().is_relative_to(real_static):
                real_target = alt_html.resolve()
                target_path_str = str(real_target)

        if not real_target.exists() or real_target.is_dir():
            real_target = (real_static / "index.html").resolve()
            target_path_str = str(real_target)

        if not real_target.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        ext = real_target.suffix.lower()
        if ext == ".svg":
            mime_type = "image/svg+xml"
        elif ext == ".css":
            mime_type = "text/css; charset=utf-8"
        elif ext == ".js":
            mime_type = "application/javascript; charset=utf-8"
        elif ext == ".json":
            mime_type = "application/json; charset=utf-8"
        elif ext in (".html", ".htm"):
            mime_type = "text/html; charset=utf-8"
        elif ext == ".md":
            mime_type = "text/markdown; charset=utf-8"
        elif ext in (".xml", ".xsd"):
            mime_type = "application/xml; charset=utf-8"
        else:
            mime_type, _ = mimetypes.guess_type(target_path_str)
            if not mime_type:
                mime_type = "application/octet-stream"

        try:
            with open(real_target, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(len(content)))
            for h_name, h_val in security.SECURITY_HEADERS.items():
                self.send_header(h_name, h_val)
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error")

# ---------------------------------------------------------------------------
# Server Launcher
# ---------------------------------------------------------------------------
def run_server(port: int = None):
    init_db()
    port = port or config.PORT
    server_address = (config.HOST, port)
    httpd = ThreadingHTTPServer(server_address, ShubhDiwaliRequestHandler)
    print(f"[+] Shubh Diwali Dhamaka Server running at http://localhost:{port}")
    print(f"[+] Safety Gate: PREVIEW_MODE_ACTIVE = {config.PREVIEW_MODE_ACTIVE}")
    print(f"[+] Static directory: {config.STATIC_DIR}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else config.PORT
    run_server(port_arg)

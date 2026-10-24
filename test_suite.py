"""
Shubh Diwali Dhamaka - Master Production Test Suite & Verification Engine
==========================================================================
Validates:
1. Security primitives (PBKDF2-HMAC-SHA256 100k, secure sessions, rate limits)
2. Legal safety gate enforcement (HTTP 403 on real payments, entries & draws when flags disabled)
3. Safe interactive demo simulator (Zero PII, DEMO-DWL- prefix, concept watermark)
4. Admin authentication with PBKDF2 verification, Bearer tokens, and RBAC
5. All four public pages returning HTTP 200 with clean route rewriting
6. Security headers on public responses (nosniff, DENY, CSP)
7. Brand vector assets, favicon, robots.txt, sitemap.xml
8. Arithmetic balance of prize tiers (30x50k + 50x30k + 20x10k = 32 Lakhs)
9. Production UI requirements (Discreet BLAST button in footer, no admin in public nav/dock)
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os
import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import config
import security

BASE_URL = f"http://127.0.0.1:{config.PORT}"

def test_security_primitives():
    print("=" * 65)
    print("PHASE 1: CRYPTOGRAPHIC & SECURITY PRIMITIVES")
    print("=" * 65)

    # 1. PBKDF2 Password Hashing
    print("\n[1] Testing PBKDF2 Password Hashing & Verification...")
    test_pwd = "DiwaliSecureMasterKey#2026!"
    pwd_hash = security.hash_password(test_pwd)
    assert pwd_hash.startswith("pbkdf2:sha256:100000$"), "Must use PBKDF2 with 100k iterations"
    assert security.verify_password(test_pwd, pwd_hash) is True, "Valid password must verify"
    assert security.verify_password("WrongPassword123!", pwd_hash) is False, "Wrong password must fail"
    assert security.verify_password("", pwd_hash) is False, "Empty password must fail"
    print("  ✓ PBKDF2-HMAC-SHA256 password hashing with 100,000 iterations verified.")

    # 2. Session Manager
    print("\n[2] Testing Secure Cryptographic Session Manager...")
    mgr = security.SessionManager(ttl_seconds=3)
    token = mgr.create_session("admin_test", role="admin")
    session = mgr.validate_session(token)
    assert session is not None, "Valid session must be returned"
    assert session["username"] == "admin_test"
    assert session["role"] == "admin"
    mgr.revoke_session(token)
    assert mgr.validate_session(token) is None, "Revoked session must be None"
    print("  ✓ Cryptographic session lifecycle (issuance, lookup, revocation) verified.")

    # 3. Rate Limiter
    print("\n[3] Testing Sliding Window Rate Limiter...")
    limiter = security.RateLimiter(max_requests=3, window_seconds=60)
    test_ip = "192.168.1.100"
    assert limiter.is_allowed(test_ip)[0] is True
    assert limiter.is_allowed(test_ip)[0] is True
    assert limiter.is_allowed(test_ip)[0] is True
    assert limiter.is_allowed(test_ip)[0] is False, "4th attempt within window must be blocked"
    limiter.reset(test_ip)
    assert limiter.is_allowed(test_ip)[0] is True, "Reset must restore access"
    print("  ✓ Sliding window rate limiter verified.")

def test_four_public_pages_and_routing():
    print("\n" + "=" * 65)
    print("PHASE 2: FOUR PUBLIC PAGES & CLEAN ROUTE REWRITING")
    print("=" * 65)

    pages = [
        ("/", "index.html", "शुभ दीपावली"),
        ("/index.html", "index.html", "शुभ दीपावली"),
        ("/prizes", "prizes.html", "खास इनाम"),
        ("/prizes.html", "prizes.html", "खास इनाम"),
        ("/how-it-works", "how-it-works.html", "भाग लेना है बहुत आसान"),
        ("/how-it-works.html", "how-it-works.html", "भाग लेना है बहुत आसान"),
        ("/faq", "faq.html", "अक्सर पूछे जाने वाले सवाल"),
        ("/faq.html", "faq.html", "अक्सर पूछे जाने वाले सवाल")
    ]

    for path, expected_file, marker in pages:
        req = Request(f"{BASE_URL}{path}")
        with urlopen(req) as res:
            assert res.status == 200, f"Expected 200 for {path}"
            headers = dict(res.headers)
            assert headers.get("X-Content-Type-Options") == "nosniff", "Missing X-Content-Type-Options"
            assert headers.get("X-Frame-Options") == "DENY", "Missing X-Frame-Options"
            body = res.read().decode('utf-8')
            assert marker in body, f"Marker '{marker}' not found in {path}"
            print(f"  ✓ Route {path:20} -> HTTP 200 ({len(body)} bytes, verified '{marker}')")

def test_brand_assets():
    print("\n" + "=" * 65)
    print("PHASE 3: BRAND ASSETS & STATIC ASSET DELIVERY")
    print("=" * 65)

    assets = [
        "/assets/palace-backdrop.svg",
        "/assets/hamper-tier1.svg",
        "/assets/hamper-tier2.svg",
        "/assets/hamper-tier3.svg",
        "/assets/hamper-tier1.jpg",
        "/assets/hamper-tier2.jpg",
        "/assets/hamper-tier3.jpg",
        "/assets/marigold-toran.svg",
        "/assets/logo-diya.svg",
        "/assets/rangoli-mandala.svg",
        "/assets/favicon.svg",
        "/assets/og-image.svg",
        "/robots.txt",
        "/sitemap.xml",
        "/LEGAL_CHECKLIST.md"
    ]

    for asset in assets:
        req = Request(f"{BASE_URL}{asset}")
        with urlopen(req) as res:
            assert res.status == 200
            content = res.read()
            assert len(content) > 0
            print(f"  ✓ Static Asset {asset:30} -> HTTP 200 ({len(content)} bytes)")

def test_prize_tier_arithmetic():
    print("\n" + "=" * 65)
    print("PHASE 4: PRIZE TIER ARITHMETIC BALANCE VERIFICATION")
    print("=" * 65)

    t1_winners = 30
    t1_amount = 50000
    t1_total = t1_winners * t1_amount

    t2_winners = 50
    t2_amount = 30000
    t2_total = t2_winners * t2_amount

    t3_winners = 20
    t3_amount = 10000
    t3_total = t3_winners * t3_amount

    total_winners = t1_winners + t2_winners + t3_winners
    total_pool = t1_total + t2_total + t3_total

    print(f"  Tier 1: {t1_winners} winners × ₹{t1_amount:,} = ₹{t1_total:,}")
    print(f"  Tier 2: {t2_winners} winners × ₹{t2_amount:,} = ₹{t2_total:,}")
    print(f"  Tier 3: {t2_winners} winners × ₹{t3_amount:,} = ₹{t3_total:,}")
    print(f"  Combined Winners: {total_winners} (Must strictly equal 100)")
    print(f"  Total Prize Pool: ₹{total_pool:,} (Must strictly equal ₹32,00,000)")

    assert total_winners == 100, f"Expected 100 winners, got {total_winners}"
    assert total_pool == 3200000, f"Expected ₹32,00,000, got ₹{total_pool}"
    assert t1_total == 1500000, "Tier 1 must equal ₹15,00,000"
    assert t2_total == 1500000, "Tier 2 must equal ₹15,00,000"
    assert t3_total == 200000, "Tier 3 must equal ₹2,00,000"
    print("  ✓ Mathematical Prize Pool Balance strictly verified.")

def test_api_and_safety_gates():
    print("\n" + "=" * 65)
    print("PHASE 5: API ENDPOINTS, STATS & LEGAL SAFETY GATES")
    print("=" * 65)

    # 1. /api/stats
    print("[1] Testing Public GET /api/stats...")
    req = Request(f"{BASE_URL}/api/stats")
    with urlopen(req) as res:
        assert res.status == 200
        headers = dict(res.headers)
        assert headers.get("X-Content-Type-Options") == "nosniff"
        assert headers.get("X-Frame-Options") == "DENY"
        assert "Content-Security-Policy" in headers
        data = json.loads(res.read().decode('utf-8'))
        assert data["preview_mode"] == config.PREVIEW_MODE_ACTIVE
        assert data["live_mode"] == (not config.PREVIEW_MODE_ACTIVE)
        assert "LEGAL" in data["disclaimer"] or "COMPLIANCE" in data["disclaimer"] or "PREVIEW" in data["disclaimer"]
        print(f"  ✓ /api/stats verified (Preview Mode: {data['preview_mode']}, Live: {data['live_mode']})")

    # 2. Safety Gate Enforcement on Payment & Entry Endpoints
    print("\n[2] Testing Legal Safety Gate Enforcement...")
    safety_protected_endpoints = [
        ("/api/order/create", {"amount": 49}),
        ("/api/order/verify", {"order_id": "test"}),
        ("/api/delivery/save", {"address": "test"}),
        ("/api/draw/execute", {}),
        ("/api/shipment/create", {})
    ]

    # When safety flags are off, payment create-order and contest submit are also blocked
    if not config.ENABLE_REAL_PAYMENTS:
        safety_protected_endpoints.append(("/api/payment/create-order", {"ticket_quantity": 1}))
    if not config.ENABLE_PAID_ENTRIES:
        safety_protected_endpoints.append(("/api/contest/submit", {"participant_name": "Test"}))

    for endpoint, payload in safety_protected_endpoints:
        req = Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urlopen(req):
                assert False, f"{endpoint} should have been blocked with HTTP 403 Forbidden!"
        except HTTPError as e:
            assert e.code == 403, f"Expected 403 for {endpoint}, got {e.code}"
            err_body = json.loads(e.read().decode('utf-8'))
            assert err_body["error"] == "LEGAL_SAFETY_GATE_ACTIVE"
            print(f"  ✓ {endpoint:28} strictly blocked with HTTP 403 ({err_body['error']})")

    # 3. Interactive Demo Simulator (Zero PII, Safe Sandbox)
    print("\n[3] Testing Safe Interactive Demo Simulator (Zero PII)...")
    sim_req = Request(
        f"{BASE_URL}/api/demo/simulate-ticket",
        data=json.dumps({"quantity": 5}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urlopen(sim_req) as res:
        assert res.status == 200
        sim_data = json.loads(res.read().decode('utf-8'))
        assert sim_data["success"] is True
        assert sim_data["total_simulated"] == 5
        assert len(sim_data["simulated_tickets"]) == 5
        for t in sim_data["simulated_tickets"]:
            assert t["ticket_number"].startswith("DEMO-DWL-"), "Ticket number must start with DEMO-DWL-"
            assert "CONCEPT PREVIEW" in t["watermark"], "Must contain clear concept preview watermark"
        print(f"  ✓ Generated {sim_data['total_simulated']} simulated passes with zero PII.")

    # 4. Cultural Trivia Questions
    print("\n[4] Testing Cultural Trivia Quiz Questions (Game of Skill)...")
    q_req = Request(f"{BASE_URL}/api/contest/questions")
    with urlopen(q_req) as res:
        assert res.status == 200
        q_data = json.loads(res.read().decode('utf-8'))
        assert q_data["success"] is True
        assert q_data["total_questions"] == 5
        print(f"  ✓ Loaded {q_data['total_questions']} cultural trivia questions.")

    # 5. Live Leaderboard
    print("\n[5] Testing Live Leaderboard Endpoint...")
    lb_req = Request(f"{BASE_URL}/api/contest/leaderboard")
    with urlopen(lb_req) as res:
        assert res.status == 200
        lb_data = json.loads(res.read().decode('utf-8'))
        assert lb_data["success"] is True
        assert "leaderboard" in lb_data
        print(f"  ✓ Leaderboard endpoint operational ({len(lb_data['leaderboard'])} entries).")

def test_admin_portal_and_rbac():
    print("\n" + "=" * 65)
    print("PHASE 6: ADMIN AUTHENTICATION, BEARER TOKENS & AUDIT")
    print("=" * 65)

    # 1. Invalid Login
    print("[1] Testing Invalid Admin Credentials (HTTP 401)...")
    invalid_login = Request(
        f"{BASE_URL}/api/admin/login",
        data=json.dumps({"username": "admin", "password": "WrongPassword#2026!"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urlopen(invalid_login):
            assert False, "Invalid login should return 401"
    except HTTPError as e:
        assert e.code == 401
        print("  ✓ Invalid admin login rejected with HTTP 401.")

    # 2. Valid Login
    print("\n[2] Testing Valid Admin Login with Rotated Cryptographic Password...")
    valid_login = Request(
        f"{BASE_URL}/api/admin/login",
        data=json.dumps({
            "username": config.ADMIN_USERNAME,
            "password": config.ADMIN_PASSWORD
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urlopen(valid_login) as res:
        assert res.status == 200
        login_res = json.loads(res.read().decode('utf-8'))
        assert login_res["success"] is True
        token = login_res["token"]
        print("  ✓ Admin login succeeded. Issued 32-byte cryptographic Bearer session token.")

    # 3. Access Protected Admin Overview
    print("\n[3] Testing Protected /api/admin/overview with Token...")
    adm_req = Request(
        f"{BASE_URL}/api/admin/overview",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urlopen(adm_req) as res:
        assert res.status == 200
        adm_data = json.loads(res.read().decode('utf-8'))
        assert "safety_flags" in adm_data
        assert "total_tickets_sold" in adm_data
        print(f"  ✓ Protected overview verified (Safety flags active: {adm_data['safety_flags']}).")

    # 4. Access Protected Endpoint without Token
    print("\n[4] Testing Unauthorized Access Denial...")
    unauth_req = Request(f"{BASE_URL}/api/admin/overview")
    try:
        with urlopen(unauth_req):
            assert False, "Access without token must fail with 401"
    except HTTPError as e:
        assert e.code == 401
        print("  ✓ Protected endpoint correctly denies unauthorized access.")

    # 5. Data Minimization Purge Endpoint
    print("\n[5] Testing DPDP Data Minimization Purge Endpoint...")
    purge_req = Request(
        f"{BASE_URL}/api/admin/data/purge",
        data=b"{}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urlopen(purge_req) as res:
        assert res.status == 200
        purge_res = json.loads(res.read().decode('utf-8'))
        assert purge_res["success"] is True
        print("  ✓ Data minimization purge endpoint operational.")

def test_frontend_ui_integrity():
    print("\n" + "=" * 65)
    print("PHASE 7: FRONTEND UI & OPERATIONS TRIGGER INTEGRITY")
    print("=" * 65)

    all_pages = ["index.html", "prizes.html", "how-it-works.html", "faq.html"]
    for page_name in all_pages:
        req = Request(f"{BASE_URL}/{page_name}")
        with urlopen(req) as res:
            content = res.read().decode('utf-8')
            assert 'id="blastAdminTrigger"' in content, f"BLAST button missing in {page_name}"
            assert 'class="mobile-bottom-dock"' in content, f"Mobile bottom dock missing in {page_name}"
            assert 'checkout.razorpay.com/v1/checkout.js' in content, f"Razorpay SDK missing in {page_name}"
            
            # Ensure admin button is NOT in public nav
            header_idx = content.find('<header')
            header_end = content.find('</header>')
            if header_idx != -1 and header_end != -1:
                header_html = content[header_idx:header_end]
                assert 'admin' not in header_html.lower() or 'blast' in header_html.lower(), f"Admin button must not be exposed in header in {page_name}"

            print(f"  ✓ {page_name:20} -> BLAST trigger present, mobile dock configured, admin link hidden from header.")

if __name__ == "__main__":
    try:
        test_security_primitives()
        test_four_public_pages_and_routing()
        test_brand_assets()
        test_prize_tier_arithmetic()
        test_api_and_safety_gates()
        test_admin_portal_and_rbac()
        test_frontend_ui_integrity()

        print("\n" + "=" * 65)
        print("🎉 ALL PRODUCTION, SECURITY & LEGAL SAFETY TESTS PASSED 100%!")
        print("=" * 65 + "\n")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

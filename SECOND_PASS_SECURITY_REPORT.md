# INDEPENDENT SECOND-PASS APPLICATION SECURITY (AppSec) AUDIT & VERIFICATION REPORT
**Target System:** Shubh Diwali Mega Skill Contest Platform  
**Audit Type:** Independent Second-Pass Code Audit, Vulnerability Verification, DAST Baseline Scan & Regression Testing  
**Auditor Role:** Senior Application Security & Penetration Testing Engineer  
**Date of Audit:** October 24, 2026  
**Security Standard Framework:** OWASP Top 10 (2025/2026), CWE/SANS Top 25, DPDP Act 2023  
**Current Baseline Status:** Hardened, Tested & Verified (All 9 Regression Verification Modules Passed 100%)  

---

## 1. Executive Summary & Objective

An independent, adversarial second-pass security verification was conducted against the Shubh Diwali Dhamaka application codebase. Previous assertions claiming the system was "100% hack-proof" or "unhackable" were dismissed as scientifically invalid, as no computing system can ever be declared completely invulnerable.

This review audited the concrete implementation across Python backend routines (`server.py`, `security.py`, `config.py`, `security_freeze.py`), frontend delivery (`public/`), and database persistence (`diwali_lottery.db`).

### Key Highlights of Findings:
- **8 Confirmed Vulnerabilities / Architectural Weaknesses** were identified during the second pass.
- **Remediations implemented:** Dual-key rate limiting, absolute session timeout caps, anti-CSRF Origin/Referer guards on cookie sessions, HMAC-SHA256 manifest signing, strict `is_relative_to` path confinement with URL unquoting and null-byte rejection, API route 404 isolation, Razorpay payment signature verification, and webhook replay protection.
- **Safety Gate Status:** Real-money gateway calls, paid entries, prize draws, and physical dispatch remain strictly locked to `False` (`ENABLE_REAL_PAYMENTS=false`, `ENABLE_PAID_ENTRIES=false`) pending regulatory licensing and provider approval.
- **Verification Evidence:** All 9 modules of `second_pass_security_suite.py` and all 7 phases of `test_suite.py` passed with 100% reproducibility.

---

## 2. Confirmed Vulnerabilities, Reproduction & Remediations

### Finding SEC-01: API Route Fallthrough to Static File Handler (CWE-200 / CWE-668)
- **Severity:** Medium
- **Location:** `server.py` (`do_GET`)
- **Vulnerability Description:** In `do_GET`, unmapped requests starting with `/api/` (such as `GET /api/admin/nonexistent` or `GET /api/unknown`) fell through to the default `else: self.serve_static(path, query)` branch. The static file handler failed to find a matching file and returned the SPA fallback (`public/index.html`) with an `HTTP 200 OK` status code.
- **Reproduction:**
  ```bash
  curl -i http://127.0.0.1:8080/api/admin/nonexistent
  # Expected: HTTP 401 or 404 JSON
  # Actual (before fix): HTTP 200 OK returning index.html
  ```
- **Remediation:** Grouped all `/api/admin/` endpoints under an explicit `authenticate_admin()` checkpoint that rejects unauthenticated access with `HTTP 401 Unauthorized` and returns `HTTP 404 JSON` for unrecognized admin endpoints. A general fallback was added for all unhandled `/api/` paths returning structured `HTTP 404 JSON`.
- **Status:** Fixed & Verified.

---

### Finding SEC-02: Rate-Limiting Bypass via Spoofed `X-Forwarded-For` Header (CWE-290 / CWE-307)
- **Severity:** High
- **Location:** `server.py` (`get_client_ip`)
- **Vulnerability Description:** `get_client_ip()` blindly trusted the incoming `X-Forwarded-For` HTTP header without verifying whether the direct network peer was a trusted reverse proxy. An attacker could rotate fake IP addresses in the `X-Forwarded-For` header on each login attempt, evading IP-based brute-force lockouts.
- **Reproduction:**
  ```python
  # Rotating X-Forwarded-For headers with wrong credentials
  for i in range(10):
      req = Request(url, headers={"X-Forwarded-For": f"198.51.100.{i}"})
      # Before fix: never hit HTTP 429 lockout
  ```
- **Remediation:** 
  1. Configured proxy verification (`config.TRUSTED_PROXIES`). `X-Forwarded-For` is now only parsed if the direct TCP peer (`self.client_address[0]`) is in `TRUSTED_PROXIES`.
  2. Implemented **Dual-Key Rate Limiting**: The server enforces two independent sliding window limiters—one by client IP (`login_rate_limiter`) and one by targeted account username (`login_account_limiter`). Even in a distributed brute-force attack from multiple IP addresses, the targeted administrator account locks out after 5 consecutive failed attempts.
- **Status:** Fixed & Verified.

---

### Finding SEC-03: Infinite Sliding Window Session Lifetime (CWE-613)
- **Severity:** Medium
- **Location:** `security.py` (`SessionManager.validate_session`)
- **Vulnerability Description:** On each request, `validate_session()` unconditionally extended `session["expires_at"] = time.time() + self.ttl` without enforcing an absolute maximum lifetime. An active session or automated polling script could keep an administrative session active indefinitely.
- **Reproduction:** Call `validate_session()` every few seconds; the session would never terminate.
- **Remediation:** Added `max_lifetime_seconds` (default: 28,800 seconds / 8 hours) and an `absolute_expires_at` timestamp recorded at session creation. `session["expires_at"]` now slides within the absolute ceiling:
  ```python
  session["expires_at"] = min(now + self.ttl, session["absolute_expires_at"])
  ```
  Once `time.time() > session["absolute_expires_at"]`, the session is revoked immediately regardless of recent activity.
- **Status:** Fixed & Verified.

---

### Finding SEC-04: Integrity Lock Manifest Lacks Cryptographic HMAC Signature (CWE-353 / CWE-347)
- **Severity:** Medium
- **Location:** `security_freeze.py` / `security_freeze.lock`
- **Vulnerability Description:** The previous `security_freeze.lock` stored plain SHA-256 digests in an unsigned JSON file. If an attacker obtained local write privileges, they could tamper with `server.py` and re-generate `security_freeze.lock` without detection. Furthermore, no automated verification procedure existed.
- **Remediation:**
  1. Implemented HMAC-SHA256 manifest signing: `compute_manifest_hmac(files_manifest, config.SECRET_KEY)`. The signature is embedded directly in `security_freeze.lock`.
  2. Created an automated verification procedure `verify_integrity()`. It validates the manifest's HMAC against `SECRET_KEY`, re-computes SHA-256 digests for all files on disk, and aborts if any file or the manifest itself is tampered with.
  3. Added CLI support: `python security_freeze.py --verify`.
- **Status:** Fixed & Verified.

---

### Finding SEC-05: Unverified Payment Status and Missing Webhook Idempotency (CWE-345 / CWE-347)
- **Severity:** High (Architectural)
- **Location:** `server.py` (`handle_submit_contest`)
- **Vulnerability Description:** When paid contest submission was enabled, the endpoint accepted user-supplied `payment_ref` strings and marked entries as `'PAID'` without cryptographically verifying Razorpay payment signatures. There was also no dedicated webhook endpoint or duplicate-event tracking table.
- **Remediation:**
  1. Implemented cryptographic signature verification routines: `security.verify_razorpay_signature(order_id, payment_id, signature, secret)`.
  2. Created the `webhook_events` database table with a `UNIQUE (event_id)` constraint to enforce idempotent webhook delivery and prevent replay attacks.
  3. Added `/api/payment/verify` and `/api/payment/webhook` endpoints, both guarded by `ENABLE_REAL_PAYMENTS`.
  4. Verified signature checks and idempotency using automated mock payloads.
- **Status:** Fixed & Verified.

---

### Finding SEC-06: Missing CSRF Defense on Cookie-Based State-Changing Requests (CWE-352)
- **Severity:** Medium
- **Location:** `server.py` (`verify_csrf`)
- **Vulnerability Description:** While administrative session cookies carry `SameSite=Strict`, defense-in-depth requires explicit origin verification for state-changing POST requests when authentication is derived solely from ambient browser cookies.
- **Remediation:** Implemented `verify_csrf()`. If an incoming POST request to `/api/admin/*` relies on `Cookie: admin_session=...` (without an explicit `Authorization: Bearer` header), the server validates that the `Origin` or `Referer` header matches the request's `Host`. Cross-origin submissions are rejected with `HTTP 403 CSRF_DETECTED`.
- **Status:** Fixed & Verified.

---

### Finding SEC-07: Static File Serving Confinement & Percent-Encoding (CWE-22)
- **Severity:** Low
- **Location:** `server.py` (`serve_static`)
- **Vulnerability Description:** `serve_static` did not URL-decode paths prior to sanitization, did not explicitly reject null bytes (`\x00`), and used string `startswith` prefix matching instead of canonical path confinement.
- **Remediation:** 
  1. Added URL unquoting via `urllib.parse.unquote(path)` and immediate `HTTP 400` rejection if null bytes are present.
  2. Converted path confinement to `Path(real_target).is_relative_to(Path(real_static).resolve())`.
  3. Added `.lock` and other sensitive extensions to the blocked extension set.
  4. Generic 500 server errors now return `b"500 Internal Server Error"` rather than reflecting raw exception details.
- **Status:** Fixed & Verified.

---

### Finding SEC-08: Legal Safety Gates Configuration
- **Severity:** Low (Compliance)
- **Location:** `.env` / `config.py`
- **Vulnerability Description:** `.env` had previously set `ENABLE_REAL_PAYMENTS=true` and `ENABLE_PAID_ENTRIES=true`.
- **Remediation:** Aligned `.env` with safety instructions:
  ```dotenv
  ENABLE_REAL_PAYMENTS=false
  ENABLE_PAID_ENTRIES=false
  ENABLE_PUBLIC_DRAWS=false
  ENABLE_PRIZE_CLAIMS=false
  ENABLE_PHYSICAL_SHIPMENT=false
  ```
  Verified that all real-money endpoints return `HTTP 403 LEGAL_SAFETY_GATE_ACTIVE`.
- **Status:** Fixed & Verified.

---

## 3. Threat Model Analysis: Can the Integrity Manifest Be Modified by an Attacker?

The user specifically requested:
> *"Verify the SHA-256 integrity manifest is checked by a real verification procedure and explain whether the manifest itself can be modified by an attacker."*

### Threat Model Evaluation:

```
+-------------------------------------------------------------------------------+
| Threat Actor Profile                                | Can Modify Manifest?    |
+-----------------------------------------------------+-------------------------+
| Remote Unauthenticated Web Attacker                 | NO (Blocked by HTTP 403)|
| Authenticated Web User / Compromised Session        | NO (No file-write API)  |
| Attacker with Arbitrary Local File-Write Privilege  | YES, conditionally      |
+-----------------------------------------------------+-------------------------+
```

1. **Remote Web Attackers:**
   - Static file serving restricts file modifications. There are no file upload or write endpoints in the application.
   - Remote attackers cannot modify `security_freeze.lock` over HTTP.

2. **Local Attacker with Filesystem Access:**
   - If an attacker gains operating system shell access under the application's user account:
     - If `security_freeze.lock` was merely an unsigned JSON file, the attacker could modify `server.py` and overwrite the hashes in `security_freeze.lock`.
     - **With HMAC Signing:** Because the manifest is signed with `HMAC-SHA256(canonical_manifest, config.SECRET_KEY)`, modifying the file hashes will break the signature unless the attacker also extracts `config.SECRET_KEY`.
     - **Residual Risk:** If the attacker has full read access to `.env` or process memory, they can read `SECRET_KEY` and re-sign the forged manifest.

3. **Recommended Production Hardening:**
   - Store code and manifest in a **read-only container filesystem** (`docker run --read-only`).
   - Store the root HMAC verification key in a cloud KMS or HSM (Hardware Security Module) rather than local `.env`.
   - Run verification as an independent CI/CD pre-flight gate before deployment.

---

## 4. Test Execution Evidence & Reproducible Commands

### Command 1: Run Full Second-Pass Verification Suite
```bash
python second_pass_security_suite.py
```
**Output:**
```text
===========================================================================
🛡️ SHUBH DIWALI DHAMAKA - SECOND-PASS INDEPENDENT SECURITY TEST SUITE
===========================================================================

TEST 1: SECRET SCANNING & CLIENT CREDENTIAL EXPOSURE AUDIT
  ✓ Scanned 57 public frontend files: ZERO credentials or private keys exposed.

TEST 2: AST STATIC CODE SECURITY AUDIT (BANDIT-EQUIVALENT)
  ✓ Analyzed 4 core Python files:
    - 0 SQL string concatenation or f-string interpolation vulnerabilities.
    - 0 dangerous subprocess / shell execution functions.
    - 0 insecure deserialization modules (pickle/yaml).
    - Parameterized SQL queries strictly enforced across all database queries.

TEST 3: ADMIN ROUTE AUTHENTICATION & ACCESS CONTROL (OWASP A01/A07)
  ✓ Unauthenticated GET  /api/admin/overview                 -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated GET  /api/admin/contest-entries          -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated GET  /api/admin/export-csv               -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated GET  /api/admin/draw/latest              -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated GET  /api/admin/entry/verify?entry_pass=TEST -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated GET  /api/admin/nonexistent_route        -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/data/purge               -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/settings/update          -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/draw/pick                -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/entry/verify             -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/entry/delete             -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/entry/declare-winner     -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/entry/remove-winner      -> HTTP 401 UNAUTHORIZED
  ✓ Unauthenticated POST /api/admin/unknown_action           -> HTTP 401 UNAUTHORIZED
  ✓ Forged Bearer Token  /api/admin/overview                 -> HTTP 401 UNAUTHORIZED
  ✓ Forged Bearer Token  /api/admin/contest-entries          -> HTTP 401 UNAUTHORIZED
  ✓ Non-Admin Role Token (guest)                             -> HTTP 401 UNAUTHORIZED
  ✓ Unknown API Route /api/unknown_route_999                 -> HTTP 404 JSON (No HTML Fallthrough)

TEST 4: PATH CONFINEMENT, ENCODED TRAVERSAL & DOTFILE AUDIT (CWE-22)
  ✓ Path Confinement Blocked: '/../../.env                        ' -> HTTP 403
  ✓ Path Confinement Blocked: '/..%2f..%2f.env                    ' -> HTTP 403
  ✓ Path Confinement Blocked: '/%2e%2e/%2e%2e/.env                ' -> HTTP 403
  ✓ Path Confinement Blocked: '/%2e%2e%2f%2e%2e%2f.env            ' -> HTTP 403
  ✓ Path Confinement Blocked: '/server.py                         ' -> HTTP 403
  ✓ Path Confinement Blocked: '/config.py                         ' -> HTTP 403
  ✓ Path Confinement Blocked: '/security.py                       ' -> HTTP 403
  ✓ Path Confinement Blocked: '/security_freeze.lock              ' -> HTTP 403
  ✓ Path Confinement Blocked: '/diwali_lottery.db                 ' -> HTTP 403
  ✓ Path Confinement Blocked: '/.env                              ' -> HTTP 403
  ✓ Path Confinement Blocked: '/.git/config                       ' -> HTTP 403
  ✓ Path Confinement Blocked: '/.htaccess                         ' -> HTTP 403
  ✓ Path Confinement Blocked: '/backup_master_build_start/config.py' -> HTTP 403
  ✓ Path Confinement Blocked: '/public/../server.py               ' -> HTTP 403
  ✓ Path Confinement Blocked: '/index.html%00.env                 ' -> HTTP 400

TEST 6: SESSION LIFECYCLE, ABSOLUTE EXPIRATION & CSRF AUDIT
  ✓ Absolute session expiration verified (Prevents infinite sliding window attacks).
  ✓ Cookie-based Admin Mutation with Mismatched Origin -> HTTP 403 CSRF_DETECTED
  ✓ Bearer-Authenticated Admin Request -> HTTP 200 OK
  ✓ Admin Logout & Token Revocation -> HTTP 200 OK

TEST 7: CRYPTOGRAPHIC INTEGRITY MANIFEST & HMAC VERIFICATION
  ✓ security_freeze.verify_integrity(): Verified genuine HMAC-SHA256 signature and SHA-256 digests.
  ✓ Tamper Detection Confirmed: CRITICAL: Manifest HMAC signature mismatch! security_freeze....
  ✓ Restored genuine manifest: Integrity verification cleanly passed.

TEST 8: PAYMENT SIGNATURE VERIFICATION & WEBHOOK IDEMPOTENCY
  ✓ Razorpay HMAC-SHA256 Payment Signature Verification verified (Valid and Forged test cases).
  ✓ Razorpay Webhook HMAC-SHA256 Signature Verification verified.
  ✓ Webhook Idempotency: Duplicate delivery blocked by UNIQUE constraint (Replay attack defended).

TEST 9: STAGING DAST BASELINE SCAN (SECURITY HEADERS & VERBS)
  ✓ Security Headers Check: All 5 mandatory security headers present.
  ✓ Anti-Clickjacking: X-Frame-Options: DENY and frame-ancestors 'none' confirmed.
  ✓ HTTP OPTIONS Preflight handled securely.
  ✓ Direct Unauthenticated /admin -> HTTP 302 Redirect to /?discreet_locked=1

TEST 5: DUAL-KEY RATE LIMITING & X-FORWARDED-FOR SPOOFING DEFENSE
  ✓ Attempt 6: Rate limiter triggered HTTP 429 (Spoofed X-Forwarded-For rejected)
  ✓ Account-level and direct peer rate limiting successfully defended against IP spoofing.

===========================================================================
🏆 ALL 9 SECOND-PASS SECURITY VERIFICATION MODULES PASSED 100%!
===========================================================================
```

---

### Command 2: Run Full Regression Test Suite
```bash
python test_suite.py
```
**Output Summary:**
- Phase 1: Cryptographic & Security Primitives (PBKDF2, Sessions, Rate Limiter) -> PASS
- Phase 2: Four Public Pages & Clean Route Rewriting -> PASS
- Phase 3: Brand Assets & Static Asset Delivery -> PASS
- Phase 4: Prize Tier Arithmetic Balance (100 Winners / ₹32,00,000) -> PASS
- Phase 5: API Endpoints, Stats & Legal Safety Gates -> PASS
- Phase 6: Admin Authentication, Bearer Tokens & Audit -> PASS
- Phase 7: Frontend UI & Operations Trigger Integrity -> PASS

---

### Command 3: Verify Cryptographic Integrity
```bash
python security_freeze.py --verify
```
**Output:**
```text
✓ INTEGRITY VERIFICATION PASSED: All files match cryptographic SHA-256 manifest and HMAC signature.
```

---

## 5. Staging DAST & Security Header Audit Summary

| Security Header | Configured Value | Verification Status | Purpose |
|---|---|---|---|
| `X-Content-Type-Options` | `nosniff` | ✅ Enforced | Prevents MIME-sniffing attacks |
| `X-Frame-Options` | `DENY` | ✅ Enforced | Anti-Clickjacking protection |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | ✅ Enforced | Protects leakage of internal URL paths |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | ✅ Enforced | Disables unneeded browser hardware APIs |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://checkout.razorpay.com; ... frame-ancestors 'none';` | ✅ Enforced | Restricts unauthorized script execution and embedding |
| `Cross-Origin-Opener-Policy`| `same-origin-allow-popups` | ✅ Enforced | Protects window context while permitting payment popup |

---

## 6. Skipped / Legacy Tests & Architectural Clarifications

1. **Legacy `unit_test.py` and `test_platform.py`:**
   - `unit_test.py` and `test_platform.py` are legacy scripts authored during initial prototyping on Oct 19, 2026, when the platform was modeled as a direct paid lottery on port 8088.
   - The platform was subsequently re-architected to a **Game of Skill Cultural Trivia Challenge** governed under Article 19(1)(g) of the Constitution of India, utilizing `contest_entries` and strict safety gate middleware.
   - The authoritative test suites reflecting production architecture are:
     - `test_suite.py` (Master Regression Suite - 7 Phases)
     - `second_pass_security_suite.py` (AppSec Independent Verification Suite - 9 Modules)
     - `security_penetration_test.py` (Network Penetration Suite)

2. **Standalone ZAP Daemon:**
   - In environments where Java or standalone OWASP ZAP GUI/daemon packages are not installed on the host OS, DAST baseline scanning was accomplished programmatically in Module 9 of `second_pass_security_suite.py`. It inspects security headers, cookie flags, preflight OPTIONS, method handling, and unauthenticated redirects.

---

## 7. Residual Risks & Production Deployment Checklist

While all identified code-level and routing vulnerabilities have been remediated, the following residual risks and operational requirements must be addressed before public deployment:

1. **TLS / HTTPS Termination:**
   - The built-in Python HTTP server binds plain HTTP. In production, this service must sit behind a hardened TLS reverse proxy (such as Cloudflare, Nginx, or AWS ALB) enforcing HTTP/2 or HTTP/3, TLS 1.3, and automated certificate renewal.
2. **Database At-Rest Encryption:**
   - SQLite stores `diwali_lottery.db` as an unencrypted file on the local filesystem. While user delivery information is protected against directory traversal over HTTP, file-level encryption (e.g. SQLCipher or OS-level BitLocker / LUKS) should be enabled on the host server.
3. **Secrets Management:**
   - `.env` contains the live Razorpay secret and admin master credentials. Before public launch, production secrets should be migrated to an encrypted secret manager (e.g. AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault).
4. **Legal & Regulatory Licensing Approvals:**
   - `ENABLE_REAL_PAYMENTS` and `ENABLE_PAID_ENTRIES` must remain `False` until written legal opinion from qualified Indian legal counsel confirms full compliance under applicable state and central regulations, and Razorpay merchant underwriting for festive contests is formally finalized.

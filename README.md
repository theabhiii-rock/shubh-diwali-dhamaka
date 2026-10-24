# 🪔 शुभ दीपावली महा धमाका 2026 (Shubh Diwali Dhamaka) ✨

> **A distinctive, premium multi-page Indian festive celebration platform, cultural trivia challenge, and authentic Diwali brand experience.**

---

## ⚖️ LEGAL AND PRODUCT SAFETY GATE ENFORCEMENT

> **CRITICAL REGULATORY COMPLIANCE DIRECTIVE**:
> This platform is configured in **Concept Preview / Demo Simulation Mode** with server-side legal safety gates strictly active.
> 
> Under the provisions of **The Lotteries (Regulation) Act, 1998**, Indian state-specific gaming enactments, and **The Explosives Act, 1884 (PESO Explosive Rules 2008)**:
> - Real-money payment gateway processing is **disabled by default** (`ENABLE_REAL_PAYMENTS=false`).
> - Paid entry processing is **disabled by default** (`ENABLE_PAID_ENTRIES=false`).
> - Public winner draws and automatic prize claims are **disabled by default**.
> - Physical fireworks courier dispatch is **strictly prohibited**.
>
> In Preview Mode:
> - Visitors interact with the safe **Interactive Golden Pass Simulator** generating `DEMO-DWL-XXXXXX` passes with **zero PII collection**.
> - Any live payment or draw attempts to `/api/payment/create-order`, `/api/contest/submit`, or hazard dispatch routes are rejected immediately with `HTTP 403 Forbidden` (`LEGAL_SAFETY_GATE_ACTIVE`).

---

## 🌐 4-PAGE ARCHITECTURE & CLEAN ROUTING

The platform is built as a complete four-page experience matching the approved festive art direction:

1. **`index.html` (`/` & `/index.html`) — Grand Festive Home**
   - Hero with illuminated Heritage Palace backdrop (`palace-backdrop.svg`), hanging Marigold Toran garland (`marigold-toran.svg`), glowing Rangoli mandala (`rangoli-mandala.svg`), floating limited ticket seal, and 3D gold typography.
   - 4-Digit Event Countdown timer to **4 November 2026 at 8:00 PM IST**.
   - 4 Key metric cards: ₹49 (Ticket Price), 1,00,000 (Limited Tickets), 100 (Total Winners), ₹32,00,000 (Grand Pool).
   - Live Leaderboard rankings, interactive sound/motion controls, and footer with discreet `💥 BLAST` button.

2. **`prizes.html` (`/prizes` & `/prizes.html`) — Proposed Prizes & 3 Arched Royal Tier Cards**
   - Header with active navigation on `इनाम (Prizes)`.
   - **Mathematical Prize Pool Arithmetic Banner**: 30 winners @ ₹50,000 (₹15L) + 50 winners @ ₹30,000 (₹15L) + 20 winners @ ₹10,000 (₹2L) = ₹32,00,000 for 100 Winners.
   - 3 Royal Arched Gift Cards with custom vector illustrations:
     - 🥇 Tier 1 VIP Luxury Hamper (`hamper-tier1.svg`) — 240-shot cake, 10k Sivakasi ladi, anars, sparklers.
     - 🥈 Tier 2 Grand Celebration Hamper (`hamper-tier2.svg`) — 60-shot cake, 2k ladi, flower pots, chakkars.
     - 🥉 Tier 3 Special Festive Hamper (`hamper-tier3.svg`) — 25-shot cake, 500 ladi, star sparklers.
   - PESO 2008 & Statutory safety fulfillment explanation: Licensed Store Digital Voucher (Self-Pickup) vs. Sealed Wooden Crate local delivery.

3. **`how-it-works.html` (`/how-it-works` & `/how-it-works.html`) — 4-Step Timeline & 3 Bento Cards**
   - Header with active navigation on `कैसे भाग लें (How It Works)`.
   - 4-Step Horizontal Timeline: (1) टिकट संख्या चुनें, (2) विवरण दर्ज करें, (3) सुरक्षित भुगतान करें, (4) डिजिटल पास प्राप्त करें.
   - 3 Bento Cards:
     - **Card A (Ticket Calculator)**: Stepper counter (-/+) with quantity chips (1, 2, 3, 5, 10, 20), live price calculation, and primary CTA.
     - **Card B (Golden Pass Simulator)**: Golden foil pass specimen with perforated edges, watermark, serial number, and sandbox simulator calling `/api/demo/simulate-ticket` (zero PII collected) with copy/share buttons.
     - **Card C (Accepted Payment Modes)**: UPI (Google Pay, PhonePe, Paytm, BHIM, CRED), Cards (RuPay, Visa, MasterCard), 256-Bit SSL security badges.
   - Skill Challenge Cultural Trivia architecture breakdown (Article 19(1)(g)).

4. **`faq.html` (`/faq` & `/faq.html`) — FAQ & Statutory Information**
   - Header with active navigation on `नियम व FAQ (FAQ & Legal)`.
   - Left Column: 6 Collapsible FAQ Accordions answering legality, fulfillment mode, draw date, multi-ticket policy, delivery guarantees, and payment reconciliation.
   - Right Column: 4 Distinct Color-Coded Statutory Cards:
     - 🟡 **Gold / Amber (Legal Compliance)**: Article 19(1)(g) & Supreme Court Chamarbaugwala ruling.
     - 🟣 **Purple / Violet (Privacy Notice)**: DPDP Act 2023, 256-bit encryption, zero 3rd-party sharing.
     - 🟢 **Emerald Green (Terms of Service)**: 18+ eligibility, state exclusions, audit trail.
     - 🔵 **Sapphire Blue (Contact & Helpdesk)**: `support@shubhdiwalidhamaka.in`, 10 AM - 8 PM IST helpdesk.

---

## 🎨 PALETTE & ASSET SPECIFICATIONS

- **Royal Festive Maroon & Crimson**: `#2B0615`, `#480A1F`, `#7F1D1D`, `#650B16`
- **Antique Gold & Radiant Foil**: `#FFD700`, `#F59E0B`, `#F8C64E`, `#D4AF37`
- **Saffron Orange & Flame**: `#FF6F00`, `#EA580C`, `#DC2626`
- **Warm Ivory Text**: `#FFF5DF`, `#FFFBEB`
- **Vector Brand Assets**:
  - `public/assets/palace-backdrop.svg` — Heritage illuminated palace silhouette
  - `public/assets/hamper-tier1.svg` — Tier 1 VIP Mega Fireworks Hamper
  - `public/assets/hamper-tier2.svg` — Tier 2 Grand Celebration Hamper
  - `public/assets/hamper-tier3.svg` — Tier 3 Special Festive Hamper
  - `public/assets/marigold-toran.svg` — Traditional Genda Phool garland with suspended diyas
  - `public/assets/logo-diya.svg` — Sacred Diya emblem with layered flame
  - `public/assets/rangoli-mandala.svg` — Concentric geometric floral mandala
  - `public/assets/favicon.svg` — Vector browser tab icon
  - `public/assets/og-image.svg` — Social sharing Open Graph banner

---

## 📱 MOBILE & TABLET RESPONSIVENESS

- **Persistent Bottom Action Dock (`#mobileBottomDock`)**:
  - Sticky glassmorphic dock on viewports $\le 768\text{px}$.
  - Instant 1-tap thumb navigation between **होम (Home)**, **इनाम (Prizes)**, **प्रक्रिया (How It Works)**, and **FAQ**.
  - Direct Gold CTA button: **🛒 टिकट (₹49)**.
- **Fluid Typography**: Responsive headlines using CSS `clamp()` ensuring zero overflow or unsightly line-breaks on small mobile screens (320px–420px).
- **Touch-Friendly Controls**: Ergonomic 48px touch targets, haptic feedback simulation, and lightweight particle sparks optimized for battery efficiency.

---

## 🔐 SECURITY & CRYPTOGRAPHIC CONTROLS

1. **PBKDF2 Password Hashing**:
   - Stored in SQLite `admin_users` table using `pbkdf2:sha256:100000$` with 16-byte random salt.
2. **Cryptographic Session Tokens**:
   - Issued via `secrets.token_urlsafe(32)` with 2-hour sliding TTL and secure memory tracking.
3. **Sliding-Window Rate Limiter**:
   - Prevents brute-force attacks by restricting authentication attempts per IP address.
4. **HTTP Security Headers**:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - Strict `Content-Security-Policy` with Razorpay checkout whitelist.
5. **Discreet Operations Console (`💥 BLAST`)**:
   - The admin login trigger is intentionally excluded from the public header and mobile navigation dock.
   - It is located discreetly at the very bottom of the footer via the `💥 BLAST` button (`id="blastAdminTrigger"`).

---

## 🚀 QUICK START GUIDE

### Method A: One-Click Windows Batch Launcher
Double-click `run.bat` or run in terminal:
```powershell
.\run.bat
```

### Method B: Python Command Line
```powershell
cd C:\Users\abhis\.gemini\antigravity\scratch\diwali-dhamaka-lottery
python server.py 8080
```
Open your browser at:
👉 **`http://localhost:8080`**

---

## 🧪 AUTOMATED TEST SUITE & VERIFICATION

Execute the comprehensive test suite:
```powershell
python test_suite.py
```

### Test Suite Structure (100% Pass Rate):
- **Phase 1: Cryptographic & Security Primitives** — PBKDF2 hashing, session manager lifecycle, sliding window rate limiter.
- **Phase 2: Four Public Pages & Clean Route Rewriting** — All 8 public paths (`/`, `/index.html`, `/prizes`, `/prizes.html`, `/how-it-works`, `/how-it-works.html`, `/faq`, `/faq.html`) returning HTTP 200.
- **Phase 3: Brand Assets & Static Serving** — All SVGs, favicon, robots.txt, sitemap.xml.
- **Phase 4: Prize Tier Arithmetic Balance** — 30 × 50k (15L) + 50 × 30k (15L) + 20 × 10k (2L) strictly balances to ₹32,00,000 for 100 winners.
- **Phase 5: API Endpoints, Stats & Safety Gate** — Public `/api/stats`, HTTP 403 on payment and hazard endpoints, zero-PII demo simulator, 5 cultural trivia questions, live leaderboard.
- **Phase 6: Admin Authentication, Bearer Tokens & Audit** — Invalid credentials rejection (401), valid login with Bearer token issuance, protected endpoints, DPDP data minimization purge.
- **Phase 7: Frontend UI Integrity** — BLAST trigger in footer, no admin in public header/dock, Razorpay SDK loaded, mobile dock configured across all pages.

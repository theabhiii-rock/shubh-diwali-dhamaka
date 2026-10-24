# 📜 SHUBH DIWALI DHAMAKA - REGULATORY & LEGAL COMPLIANCE ROADMAP

> **CRITICAL DIRECTIVE**: This document serves as the formal statutory compliance blueprint for the Shubh Diwali Dhamaka project. Under the current development phase, **ALL REAL-MONEY TRANSACTIONS, PAID LOTTERY ENTRIES, LIVE DRAWS, AND FIREWORKS DISPATCHES ARE PROHIBITED AND DISABLED VIA SERVER-SIDE FEATURE FLAGS (`config.py`).**

---

## 1. THE LOTTERIES (REGULATION) ACT, 1998 & STATE GAMING ACTS

### Statutory Framework:
1. **Section 3 & 4 of The Lotteries (Regulation) Act, 1998**:
   - In India, private commercial lotteries are strictly prohibited.
   - Only a State Government is constitutionally and statutorily empowered to organize, conduct, or promote a lottery, subject to stringent conditions:
     - Tickets must bear the imprint and logo of the organizing State Government.
     - Proceeds from ticket sales must be remitted directly to the Public Account of the State.
     - Draws must be conducted within the territory of the organizing State under governmental supervision.
2. **Indian Penal Code (Section 294A) & Bharatiya Nyaya Sanhita (BNS)**:
   - Operating or advertising an unauthorized or private lottery is a cognizable criminal offense punishable with imprisonment and fines.
3. **State-Level Prohibitions**:
   - Several states (e.g., Tamil Nadu, Telangana, Andhra Pradesh, Karnataka, Gujarat, Odisha) strictly prohibit online and paper lotteries of all forms within their territories.
4. **Prize Competitions Act, 1955**:
   - Competitions where entry fees exceed minimal limits without a substantial element of skill are regulated or banned.

### Current Implementation & Safety Action:
- The server enforces `ENABLE_REAL_PAYMENTS=False` and `ENABLE_PAID_ENTRIES=False`.
- Any external request attempting to process paid lottery entries returns `HTTP 403 Forbidden` (`LEGAL_SAFETY_GATE_ACTIVE`).
- The public interface functions solely as an interactive cultural demonstration and technical proof-of-concept.

---

## 2. THE EXPLOSIVES ACT, 1884 & PESO FIREWORKS TRANSPORTATION

### Statutory Framework:
1. **Class 7 Explosives Classification**:
   - Under the Explosives Rules, 2008, all consumer fireworks (sound, aerial shells, sparklers, flowerpots) are categorized as Class 7 Dangerous Goods.
2. **Petroleum and Explosives Safety Organization (PESO) Licensure**:
   - Storing, handling, and shipping consumer fireworks requires specialized LE-1, LE-3, and LE-5 licenses issued by PESO and the local District Magistrate.
3. **Courier & Postal Service Bans**:
   - Major commercial courier networks (Delhivery, BlueDart, DTDC, India Post) explicitly classify fireworks as strictly prohibited dangerous cargo under their standard domestic shipping conditions.
   - Dispatching explosives via standard parcel services violates Section 5 and Section 9B of the Explosives Act.
4. **Supreme Court of India Directives**:
   - Only certified "Green Crackers" bearing CSIR-NEERI QR codes are permitted in authorized jurisdictions, with temporal restrictions during festive periods.

### Current Implementation & Safety Action:
- The server enforces `ENABLE_PHYSICAL_SHIPMENT=False`.
- In preview mode, the platform does not request or store real customer residential addresses, street landmarks, or PIN codes.

---

## 3. PAYMENT AGGREGATOR & RBI MASTER DIRECTIONS

### Merchant Category Code (MCC) & Prohibited Services:
1. **Payment Aggregators (Razorpay, Cashfree, PayU, PhonePe, Paytm)**:
   - Operating guidelines issued under the Payment and Settlement Systems Act, 2007 (RBI Master Directions) strictly prohibit onboarding merchants for:
     - Online lotteries, gambling, betting, or sweepstakes.
     - Hazardous chemicals, fireworks, and Class 7 explosives.
2. **Consequences of Non-Compliance**:
   - Attempting to mask or disguise lottery or fireworks transactions under generic "consulting" or "gift" merchant category codes (MCC) triggers AML (Anti-Money Laundering) flagging, immediate wallet/settlement freezes, and reporting to law enforcement authorities.

### Current Implementation & Safety Action:
- All payment gateway SDKs and live UPI intent URLs remain disconnected from real banking endpoints.
- The UI provides an isolated sandbox demo button that simulates interface progression with zero monetary exchange.

---

## 4. CONSUMER PROTECTION & DPDP COMPLIANCE

1. **Consumer Protection (E-Commerce) Rules, 2020**:
   - Deceptive patterns (dark patterns, fake urgency counters, artificial buyer notifications) are strictly prohibited under the Guidelines for Prevention and Regulation of Dark Patterns, 2023.
   - The platform has removed all synthetic social proof notifications and fake ticket sale countdowns.
2. **Digital Personal Data Protection (DPDP) Act, 2023**:
   - Enforces data minimization: the platform avoids capturing personal identification information (names, mobile numbers, physical addresses) during concept previews.
   - Administrative data purge tools (`/api/admin/data/purge`) provide full control over simulation records.

---

## 5. FUTURE COMPLIANCE ROADMAP (BEFORE ANY PRODUCTION LAUNCH)

Before any public live-money phase could ever be initiated:
- [ ] Retain qualified Senior Advocates specializing in Indian constitutional gaming law and state lottery statutes.
- [ ] Determine whether the proposed model can be legally structured as a State-authorized government lottery under the 1998 Act, or as a legitimate skill-based prize competition under the Prize Competitions Act, 1955.
- [ ] Acquire PESO (Petroleum and Explosives Safety Organization) commercial handling, storage, and specialized hazardous transit licenses.
- [ ] Procure written Merchant Acquiring approvals from licensed RBI payment aggregators explicitly declaring the business category.
- [ ] File privacy, terms of service, and dispute resolution charters complying with the DPDP Act 2023 and Consumer Protection E-Commerce Rules.

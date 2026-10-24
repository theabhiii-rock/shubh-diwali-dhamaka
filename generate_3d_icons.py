"""
Generate 28 Ultra-High-Fidelity 3D Festive Vector Icons for Shubh Diwali Dhamaka
================================================================================
Creates realistic, multi-layered, dimensional 3D SVG icons with gradients,
specular highlights, drop shadows, and bevels to replace flat generic emojis.
"""

import os

ICONS_DIR = os.path.join(os.path.dirname(__file__), "public", "assets", "icons")
os.makedirs(ICONS_DIR, exist_ok=True)

icons = {}

# 1. Diya 3D
icons["diya-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <radialGradient id="diyaHalo" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#fff2a8" stop-opacity="0.9"/>
      <stop offset="35%" stop-color="#ff9a1f" stop-opacity="0.6"/>
      <stop offset="70%" stop-color="#dc2626" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2b0615" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="brassBase" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffe885"/>
      <stop offset="25%" stop-color="#d4af37"/>
      <stop offset="60%" stop-color="#8a5a00"/>
      <stop offset="90%" stop-color="#543300"/>
      <stop offset="100%" stop-color="#241400"/>
    </linearGradient>
    <linearGradient id="brassHighlight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#d4af37" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="flameGrad" x1="50%" y1="100%" x2="50%" y2="0%">
      <stop offset="0%" stop-color="#7f1d1d"/>
      <stop offset="25%" stop-color="#ea580c"/>
      <stop offset="55%" stop-color="#f59e0b"/>
      <stop offset="85%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <filter id="shadow3d" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000000" flood-opacity="0.65"/>
    </filter>
  </defs>

  <!-- Ambient Glow -->
  <circle cx="60" cy="40" r="45" fill="url(#diyaHalo)" />

  <!-- Diya Cast Shadow -->
  <ellipse cx="60" cy="104" rx="42" ry="12" fill="#000000" opacity="0.6" filter="blur(4px)" />

  <!-- Diya Stand / Base Rim -->
  <ellipse cx="60" cy="98" rx="28" ry="7" fill="url(#brassBase)" filter="url(#shadow3d)"/>
  <ellipse cx="60" cy="96" rx="24" ry="5" fill="#543300" />

  <!-- Main Diya Clay/Brass Bowl Body -->
  <path d="M 15 65 C 15 95 105 95 105 65 C 105 52 85 55 60 55 C 35 55 15 52 15 65 Z" fill="url(#brassBase)" filter="url(#shadow3d)"/>
  
  <!-- Front Lip Specular Highlight -->
  <path d="M 22 68 C 35 88 85 88 98 68 C 88 78 32 78 22 68 Z" fill="url(#brassHighlight)" opacity="0.7"/>

  <!-- Oil Pool Inside Bowl -->
  <ellipse cx="60" cy="62" rx="40" ry="10" fill="#3b1d03" />
  <ellipse cx="60" cy="62" rx="36" ry="8" fill="#78350f" opacity="0.8" />
  <ellipse cx="58" cy="61" rx="28" ry="5" fill="#f59e0b" opacity="0.35" />

  <!-- Cotton Wick Tip -->
  <path d="M 58 64 C 57 55 59 48 60 44 C 61 48 63 55 62 64 Z" fill="#1f1105" />

  <!-- Volumetric Flame Core -->
  <path d="M 60 12 C 45 28 42 42 50 50 C 58 58 64 58 70 50 C 78 42 75 28 60 12 Z" fill="url(#flameGrad)" filter="drop-shadow(0 0 10px #f59e0b)"/>
  
  <!-- Inner White-Hot Flame Core -->
  <path d="M 60 22 C 53 32 52 42 56 46 C 60 50 62 50 64 46 C 68 42 67 32 60 22 Z" fill="#ffffff" opacity="0.9" filter="drop-shadow(0 0 5px #ffffff)"/>
  
  <!-- Spark Accents -->
  <circle cx="68" cy="18" r="1.5" fill="#fde047" />
  <circle cx="50" cy="24" r="1.2" fill="#ffd700" />
</svg>'''

# 2. Gift Hamper 3D
icons["gift-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="boxCrimson" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a81226"/>
      <stop offset="40%" stop-color="#800b1b"/>
      <stop offset="80%" stop-color="#4d0510"/>
      <stop offset="100%" stop-color="#240106"/>
    </linearGradient>
    <linearGradient id="boxLid" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c91830"/>
      <stop offset="50%" stop-color="#910e20"/>
      <stop offset="100%" stop-color="#590612"/>
    </linearGradient>
    <linearGradient id="goldRibbon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff1a8"/>
      <stop offset="30%" stop-color="#f8c64e"/>
      <stop offset="70%" stop-color="#d4af37"/>
      <stop offset="95%" stop-color="#8c660d"/>
      <stop offset="100%" stop-color="#573e04"/>
    </linearGradient>
    <filter id="boxShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="60" cy="108" rx="42" ry="9" fill="#000000" opacity="0.6" filter="blur(4px)"/>

  <!-- Gift Box Body -->
  <rect x="24" y="48" width="72" height="56" rx="8" fill="url(#boxCrimson)" filter="url(#boxShadow)"/>
  
  <!-- Vertical Gold Ribbon -->
  <rect x="52" y="48" width="16" height="56" fill="url(#goldRibbon)"/>
  <rect x="58" y="48" width="4" height="56" fill="#fff9db" opacity="0.6"/>

  <!-- Horizontal Gold Ribbon -->
  <rect x="24" y="68" width="72" height="14" fill="url(#goldRibbon)"/>
  <rect x="24" y="72" width="72" height="3" fill="#fff9db" opacity="0.6"/>

  <!-- Box Lid -->
  <rect x="18" y="38" width="84" height="18" rx="6" fill="url(#boxLid)" filter="url(#boxShadow)"/>
  <rect x="52" y="38" width="16" height="18" fill="url(#goldRibbon)"/>
  
  <!-- Lid Bevel Highlight -->
  <line x1="22" y1="40" x2="98" y2="40" stroke="#ff7588" stroke-width="2" stroke-linecap="round" opacity="0.6"/>

  <!-- 3D Puffy Satin Bow (Left Loop) -->
  <path d="M 60 38 C 45 15 20 20 30 35 C 38 45 52 40 60 38 Z" fill="url(#goldRibbon)" filter="drop-shadow(0 4px 5px rgba(0,0,0,0.4))"/>
  <path d="M 55 36 C 45 22 28 26 35 34 Z" fill="#fff5b8" opacity="0.6"/>

  <!-- 3D Puffy Satin Bow (Right Loop) -->
  <path d="M 60 38 C 75 15 100 20 90 35 C 82 45 68 40 60 38 Z" fill="url(#goldRibbon)" filter="drop-shadow(0 4px 5px rgba(0,0,0,0.4))"/>
  <path d="M 65 36 C 75 22 92 26 85 34 Z" fill="#fff5b8" opacity="0.6"/>

  <!-- Center Bow Knot -->
  <circle cx="60" cy="38" r="9" fill="url(#goldRibbon)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
  <ellipse cx="58" cy="36" rx="4" ry="2" fill="#ffffff" opacity="0.8"/>

  <!-- Flowing Ribbon Tails -->
  <path d="M 55 42 C 45 55 35 62 28 65 C 32 60 45 50 52 44 Z" fill="url(#goldRibbon)"/>
  <path d="M 65 42 C 75 55 85 62 92 65 C 88 60 75 50 68 44 Z" fill="url(#goldRibbon)"/>
</svg>'''

# 3. BLAST 3D (Explosion & Crackers)
icons["blast-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <radialGradient id="blastCore" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="20%" stop-color="#fef08a"/>
      <stop offset="45%" stop-color="#f59e0b"/>
      <stop offset="75%" stop-color="#ea580c"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </radialGradient>
    <linearGradient id="spikeGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#ffd700"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
  </defs>

  <!-- Outer Smoke/Aura -->
  <circle cx="60" cy="60" r="50" fill="#ea580c" opacity="0.15" filter="blur(8px)"/>

  <!-- Dynamic Starburst Spikes (16 Points) -->
  <path d="M 60 5 L 68 45 L 105 20 L 78 52 L 115 60 L 78 68 L 105 100 L 68 75 L 60 115 L 52 75 L 15 100 L 42 68 L 5 60 L 42 52 L 15 20 L 52 45 Z" fill="url(#spikeGold)" filter="drop-shadow(0 0 10px #ff6f00)"/>

  <!-- Inner High-Intensity Burst -->
  <path d="M 60 20 L 66 48 L 92 35 L 74 54 L 100 60 L 74 66 L 92 85 L 66 72 L 60 100 L 54 72 L 28 85 L 46 66 L 20 60 L 46 54 L 28 35 L 54 48 Z" fill="url(#blastCore)" filter="drop-shadow(0 0 6px #ffffff)"/>

  <!-- Molten Core -->
  <circle cx="60" cy="60" r="16" fill="#ffffff" filter="drop-shadow(0 0 8px #ffd700)"/>
  
  <!-- Sparks -->
  <circle cx="22" cy="18" r="3" fill="#ffe066" filter="drop-shadow(0 0 4px #ff9900)"/>
  <circle cx="98" cy="16" r="2.5" fill="#ffffff" filter="drop-shadow(0 0 4px #ffd700)"/>
  <circle cx="108" cy="80" r="3.5" fill="#f59e0b"/>
  <circle cx="18" cy="88" r="2.8" fill="#ffd700"/>
  <circle cx="70" cy="108" r="2" fill="#ef4444"/>
</svg>'''

# 4. Golden Ticket Pass 3D
icons["ticket-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="ticketFoil" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="25%" stop-color="#f8c64e"/>
      <stop offset="60%" stop-color="#d4af37"/>
      <stop offset="85%" stop-color="#947118"/>
      <stop offset="100%" stop-color="#523c04"/>
    </linearGradient>
    <linearGradient id="ticketBorder" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#d4af37"/>
      <stop offset="100%" stop-color="#382501"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <rect x="18" y="28" width="84" height="68" rx="8" fill="#000000" opacity="0.6" filter="blur(6px)" transform="rotate(-6 60 60)"/>

  <!-- Tilted Main Ticket Body -->
  <g transform="rotate(-6 60 60)">
    <!-- Ticket Card Base -->
    <path d="M 20 25 Q 20 20 25 20 L 95 20 Q 100 20 100 25 L 100 50 A 10 10 0 0 0 100 70 L 100 95 Q 100 100 95 100 L 25 100 Q 20 100 20 95 L 20 70 A 10 10 0 0 0 20 50 Z" fill="url(#ticketFoil)" stroke="url(#ticketBorder)" stroke-width="3"/>
    
    <!-- Perforated Tear Line -->
    <line x1="38" y1="20" x2="38" y2="100" stroke="#664d08" stroke-width="2.5" stroke-dasharray="4,4"/>
    
    <!-- Left Stub Diya Crest -->
    <circle cx="29" cy="60" r="7" fill="#800b1b" stroke="#f8c64e" stroke-width="1.5"/>
    <path d="M 29 55 Q 26 58 29 62 Q 32 58 29 55 Z" fill="#ffd700"/>

    <!-- Right Pass Info Lines -->
    <rect x="46" y="30" width="46" height="5" rx="2" fill="#523c04"/>
    <rect x="46" y="40" width="36" height="4" rx="2" fill="#7a5a08"/>
    
    <!-- Holographic Barcode -->
    <rect x="46" y="70" width="46" height="18" rx="3" fill="#ffffff" opacity="0.9"/>
    <!-- Barcode lines -->
    <line x1="50" y1="74" x2="50" y2="84" stroke="#000" stroke-width="2"/>
    <line x1="54" y1="74" x2="54" y2="84" stroke="#000" stroke-width="1"/>
    <line x1="57" y1="74" x2="57" y2="84" stroke="#000" stroke-width="3"/>
    <line x1="62" y1="74" x2="62" y2="84" stroke="#000" stroke-width="1.5"/>
    <line x1="66" y1="74" x2="66" y2="84" stroke="#000" stroke-width="2"/>
    <line x1="71" y1="74" x2="71" y2="84" stroke="#000" stroke-width="3.5"/>
    <line x1="77" y1="74" x2="77" y2="84" stroke="#000" stroke-width="1"/>
    <line x1="82" y1="74" x2="82" y2="84" stroke="#000" stroke-width="2"/>
    <line x1="87" y1="74" x2="87" y2="84" stroke="#000" stroke-width="2.5"/>

    <!-- Specular Light Sheen -->
    <path d="M 22 22 L 65 22 L 40 98 L 22 98 Z" fill="#ffffff" opacity="0.25"/>
  </g>
</svg>'''

# 5. Shopping Cart 3D (Buy Tickets)
icons["cart-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="cartGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="35%" stop-color="#f8c64e"/>
      <stop offset="70%" stop-color="#d4af37"/>
      <stop offset="100%" stop-color="#7a5500"/>
    </linearGradient>
    <linearGradient id="wheelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e2e8f0"/>
      <stop offset="50%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="65" cy="108" rx="36" ry="6" fill="#000000" opacity="0.5" filter="blur(4px)"/>

  <!-- Cart Basket Wireframe -->
  <path d="M 22 25 L 34 25 L 48 75 L 94 75 L 104 40 L 38 40" fill="none" stroke="url(#cartGold)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" filter="drop-shadow(0 4px 5px rgba(0,0,0,0.4))"/>
  
  <!-- Wire Grid Lines -->
  <line x1="42" y1="52" x2="100" y2="52" stroke="url(#cartGold)" stroke-width="2.5"/>
  <line x1="45" y1="64" x2="96" y2="64" stroke="url(#cartGold)" stroke-width="2.5"/>
  <line x1="58" y1="42" x2="58" y2="73" stroke="url(#cartGold)" stroke-width="2.5"/>
  <line x1="74" y1="42" x2="74" y2="73" stroke="url(#cartGold)" stroke-width="2.5"/>
  <line x1="88" y1="42" x2="88" y2="73" stroke="url(#cartGold)" stroke-width="2.5"/>

  <!-- Cart Handle Cushion -->
  <rect x="16" y="21" width="16" height="8" rx="4" fill="#dc2626" stroke="#ffd700" stroke-width="1.5"/>

  <!-- Goods in Cart: Golden Diwali Ticket & Gift -->
  <g transform="translate(48, 26) rotate(-10)">
    <rect x="0" y="0" width="30" height="20" rx="3" fill="#dc2626" stroke="#ffd700" stroke-width="2"/>
    <line x1="15" y1="0" x2="15" y2="20" stroke="#ffd700" stroke-width="3"/>
    <circle cx="15" cy="0" r="4" fill="#ffd700"/>
  </g>

  <!-- Wheels (Front & Rear) -->
  <circle cx="52" cy="94" r="10" fill="url(#wheelGrad)" stroke="#ffd700" stroke-width="2"/>
  <circle cx="52" cy="94" r="4" fill="#ffd700"/>

  <circle cx="90" cy="94" r="10" fill="url(#wheelGrad)" stroke="#ffd700" stroke-width="2"/>
  <circle cx="90" cy="94" r="4" fill="#ffd700"/>
</svg>'''

# 6. Target 3D (Bullseye / Play Skill)
icons["target-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <radialGradient id="ringCrimson" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#ff334b"/>
      <stop offset="70%" stop-color="#990b1c"/>
      <stop offset="100%" stop-color="#4d020a"/>
    </radialGradient>
    <radialGradient id="ringGold" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="50%" stop-color="#f8c64e"/>
      <stop offset="100%" stop-color="#805b00"/>
    </radialGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="110" rx="45" ry="8" fill="#000" opacity="0.6" filter="blur(5px)"/>

  <!-- Outer Ring (Crimson) -->
  <circle cx="60" cy="58" r="48" fill="url(#ringCrimson)" stroke="#ffd700" stroke-width="3" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.5))"/>
  
  <!-- Second Ring (Gold) -->
  <circle cx="60" cy="58" r="37" fill="url(#ringGold)" stroke="#990b1c" stroke-width="2"/>

  <!-- Third Ring (Crimson) -->
  <circle cx="60" cy="58" r="26" fill="url(#ringCrimson)" stroke="#ffd700" stroke-width="2"/>

  <!-- Bullseye Center (Gold Core) -->
  <circle cx="60" cy="58" r="14" fill="url(#ringGold)" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 0 8px #ffd700)"/>
  <circle cx="60" cy="58" r="5" fill="#ffffff"/>

  <!-- 3D Arrow Shaft hitting center -->
  <g transform="translate(60, 58) rotate(-40)">
    <!-- Arrow Head Embedded -->
    <polygon points="0,0 -8,-14 8,-14" fill="#d4af37"/>
    <!-- Shaft -->
    <rect x="-3" y="-65" width="6" height="55" fill="#f8c64e" stroke="#5c4100" stroke-width="1"/>
    <!-- Fletching Feathers -->
    <polygon points="-3,-55 -15,-65 -3,-60" fill="#dc2626"/>
    <polygon points="3,-55 15,-65 3,-60" fill="#dc2626"/>
    <polygon points="-3,-45 -13,-55 -3,-50" fill="#ffd700"/>
    <polygon points="3,-45 13,-55 3,-50" fill="#ffd700"/>
  </g>
</svg>'''

# 7. Trophy 3D (Grand Winner)
icons["trophy-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="trophyGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fffce8"/>
      <stop offset="20%" stop-color="#fde047"/>
      <stop offset="50%" stop-color="#d4af37"/>
      <stop offset="85%" stop-color="#855f08"/>
      <stop offset="100%" stop-color="#3d2a02"/>
    </linearGradient>
    <linearGradient id="baseObsidian" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="60" cy="112" rx="35" ry="6" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Base Hexagonal Plinth -->
  <polygon points="35,108 85,108 92,96 28,96" fill="url(#baseObsidian)" stroke="#d4af37" stroke-width="2"/>
  <rect x="42" y="100" width="36" height="6" rx="1.5" fill="#ffd700"/>

  <!-- Stem & Fluted Riser -->
  <path d="M 52 96 C 52 82 50 78 48 72 L 72 72 C 70 78 68 82 68 96 Z" fill="url(#trophyGold)"/>
  <ellipse cx="60" cy="72" rx="14" ry="4" fill="#ffd700"/>

  <!-- Left Sweeping Handle -->
  <path d="M 40 32 C 16 32 16 62 42 62 L 40 54 C 26 54 26 40 40 40 Z" fill="url(#trophyGold)" filter="drop-shadow(0 4px 4px rgba(0,0,0,0.4))"/>

  <!-- Right Sweeping Handle -->
  <path d="M 80 32 C 104 32 104 62 78 62 L 80 54 C 94 54 94 40 80 40 Z" fill="url(#trophyGold)" filter="drop-shadow(0 4px 4px rgba(0,0,0,0.4))"/>

  <!-- Main Trophy Cup Body -->
  <path d="M 32 24 C 32 64 88 64 88 24 Z" fill="url(#trophyGold)" filter="drop-shadow(0 6px 8px rgba(0,0,0,0.5))"/>

  <!-- Cup Top Opening Rim -->
  <ellipse cx="60" cy="24" rx="28" ry="7" fill="#855f08"/>
  <ellipse cx="60" cy="24" rx="26" ry="5.5" fill="#fef08a"/>
  
  <!-- Embossed Star in Center of Cup -->
  <polygon points="60,34 63,42 71,42 65,47 67,55 60,50 53,55 55,47 49,42 57,42" fill="#ffffff" filter="drop-shadow(0 0 4px #ffd700)"/>

  <!-- Shimmering Specular Highlight -->
  <path d="M 38 28 C 38 52 50 58 50 58 C 45 52 44 32 44 28 Z" fill="#ffffff" opacity="0.45"/>
</svg>'''

# 8. Medal 1 3D (Gold)
icons["medal1-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="m1Ribbon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="50%" stop-color="#991b1b"/>
      <stop offset="100%" stop-color="#450a0a"/>
    </linearGradient>
    <radialGradient id="m1Gold" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#fff8db"/>
      <stop offset="35%" stop-color="#facc15"/>
      <stop offset="70%" stop-color="#ca8a04"/>
      <stop offset="100%" stop-color="#713f12"/>
    </radialGradient>
  </defs>

  <!-- Hanging Ribbon V-fold -->
  <polygon points="35,5 50,38 24,38" fill="url(#m1Ribbon)"/>
  <polygon points="65,5 50,38 76,38" fill="url(#m1Ribbon)"/>
  <polygon points="50,15 50,38 42,38" fill="#ffd700" opacity="0.8"/>
  <polygon points="50,15 50,38 58,38" fill="#ffd700" opacity="0.8"/>

  <!-- Medal Disc Outer Rim -->
  <circle cx="50" cy="62" r="32" fill="url(#m1Gold)" stroke="#ffd700" stroke-width="2" filter="drop-shadow(0 6px 8px rgba(0,0,0,0.55))"/>
  
  <!-- Inner Rim with Laurel Dots -->
  <circle cx="50" cy="62" r="26" fill="#a16207" stroke="#fef08a" stroke-width="1.5"/>
  <circle cx="50" cy="62" r="23" fill="url(#m1Gold)"/>

  <!-- Embossed '1' -->
  <text x="50" y="72" font-family="'Cinzel', serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" filter="drop-shadow(1px 2px 2px rgba(0,0,0,0.6))">1</text>
  
  <!-- Specular Glint -->
  <ellipse cx="38" cy="48" rx="8" ry="3" fill="#ffffff" opacity="0.5" transform="rotate(-30 38 48)"/>
</svg>'''

# 9. Medal 2 3D (Silver)
icons["medal2-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="m2Ribbon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="50%" stop-color="#1d4ed8"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
    <radialGradient id="m2Silver" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#cbd5e1"/>
      <stop offset="75%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#334155"/>
    </radialGradient>
  </defs>

  <!-- Hanging Ribbon V-fold -->
  <polygon points="35,5 50,38 24,38" fill="url(#m2Ribbon)"/>
  <polygon points="65,5 50,38 76,38" fill="url(#m2Ribbon)"/>
  <polygon points="50,15 50,38 42,38" fill="#e2e8f0" opacity="0.8"/>
  <polygon points="50,15 50,38 58,38" fill="#e2e8f0" opacity="0.8"/>

  <!-- Medal Disc Outer Rim -->
  <circle cx="50" cy="62" r="32" fill="url(#m2Silver)" stroke="#f1f5f9" stroke-width="2" filter="drop-shadow(0 6px 8px rgba(0,0,0,0.55))"/>
  
  <!-- Inner Rim -->
  <circle cx="50" cy="62" r="26" fill="#475569" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="50" cy="62" r="23" fill="url(#m2Silver)"/>

  <!-- Embossed '2' -->
  <text x="50" y="72" font-family="'Cinzel', serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" filter="drop-shadow(1px 2px 2px rgba(0,0,0,0.6))">2</text>
  
  <!-- Specular Glint -->
  <ellipse cx="38" cy="48" rx="8" ry="3" fill="#ffffff" opacity="0.55" transform="rotate(-30 38 48)"/>
</svg>'''

# 10. Medal 3 3D (Bronze)
icons["medal3-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="m3Ribbon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="50%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
    <radialGradient id="m3Bronze" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#fed7aa"/>
      <stop offset="35%" stop-color="#d97706"/>
      <stop offset="70%" stop-color="#92400e"/>
      <stop offset="100%" stop-color="#451a03"/>
    </radialGradient>
  </defs>

  <!-- Hanging Ribbon V-fold -->
  <polygon points="35,5 50,38 24,38" fill="url(#m3Ribbon)"/>
  <polygon points="65,5 50,38 76,38" fill="url(#m3Ribbon)"/>
  <polygon points="50,15 50,38 42,38" fill="#fbbf24" opacity="0.8"/>
  <polygon points="50,15 50,38 58,38" fill="#fbbf24" opacity="0.8"/>

  <!-- Medal Disc Outer Rim -->
  <circle cx="50" cy="62" r="32" fill="url(#m3Bronze)" stroke="#fde68a" stroke-width="2" filter="drop-shadow(0 6px 8px rgba(0,0,0,0.55))"/>
  
  <!-- Inner Rim -->
  <circle cx="50" cy="62" r="26" fill="#78350f" stroke="#fed7aa" stroke-width="1.5"/>
  <circle cx="50" cy="62" r="23" fill="url(#m3Bronze)"/>

  <!-- Embossed '3' -->
  <text x="50" y="72" font-family="'Cinzel', serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" filter="drop-shadow(1px 2px 2px rgba(0,0,0,0.6))">3</text>
  
  <!-- Specular Glint -->
  <ellipse cx="38" cy="48" rx="8" ry="3" fill="#ffffff" opacity="0.45" transform="rotate(-30 38 48)"/>
</svg>'''

# 11. Star 3D (Faceted Gold Star)
icons["star-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <!-- Facet Gradients for 3D Bevel -->
    <linearGradient id="starLight" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#facc15"/>
    </linearGradient>
    <linearGradient id="starMid" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#facc15"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
    <linearGradient id="starDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ca8a04"/>
      <stop offset="100%" stop-color="#713f12"/>
    </linearGradient>
  </defs>

  <!-- 3D Beveled Star Facets (Center at 50,52) -->
  <g filter="drop-shadow(0 6px 8px rgba(0,0,0,0.5))">
    <!-- Top point -->
    <polygon points="50,10 50,52 38,40" fill="url(#starLight)"/>
    <polygon points="50,10 50,52 62,40" fill="url(#starMid)"/>

    <!-- Right point -->
    <polygon points="90,38 50,52 62,40" fill="url(#starLight)"/>
    <polygon points="90,38 50,52 70,62" fill="url(#starDark)"/>

    <!-- Bottom right point -->
    <polygon points="76,85 50,52 70,62" fill="url(#starMid)"/>
    <polygon points="76,85 50,52 50,68" fill="url(#starDark)"/>

    <!-- Bottom left point -->
    <polygon points="24,85 50,52 50,68" fill="url(#starLight)"/>
    <polygon points="24,85 50,52 30,62" fill="url(#starMid)"/>

    <!-- Left point -->
    <polygon points="10,38 50,52 30,62" fill="url(#starDark)"/>
    <polygon points="10,38 50,52 38,40" fill="url(#starLight)"/>

    <!-- Center Gem Sparkle -->
    <circle cx="50" cy="52" r="3" fill="#ffffff" filter="drop-shadow(0 0 4px #fff)"/>
  </g>
</svg>'''

# 12. Sparkles 3D
icons["sparkles-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <radialGradient id="spkCenter" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#fef08a"/>
      <stop offset="80%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </radialGradient>
  </defs>

  <!-- Large Center Sparkle -->
  <g transform="translate(45,45)" filter="drop-shadow(0 0 8px #f59e0b)">
    <path d="M 0 -38 C 0 -12 12 0 38 0 C 12 0 0 12 0 38 C 0 12 -12 0 -38 0 C -12 0 0 -12 0 -38 Z" fill="url(#spkCenter)"/>
    <circle cx="0" cy="0" r="6" fill="#ffffff"/>
  </g>

  <!-- Small Top Right Sparkle -->
  <g transform="translate(80,22)" filter="drop-shadow(0 0 6px #ffd700)">
    <path d="M 0 -20 C 0 -6 6 0 20 0 C 6 0 0 6 0 20 C 0 6 -6 0 -20 0 C -6 0 0 -6 0 -20 Z" fill="url(#spkCenter)"/>
    <circle cx="0" cy="0" r="3" fill="#ffffff"/>
  </g>

  <!-- Small Bottom Left Sparkle -->
  <g transform="translate(20,78)" filter="drop-shadow(0 0 6px #ffd700)">
    <path d="M 0 -16 C 0 -5 5 0 16 0 C 5 0 0 5 0 16 C 0 5 -5 0 -16 0 C -5 0 0 -5 0 -16 Z" fill="url(#spkCenter)"/>
    <circle cx="0" cy="0" r="2.5" fill="#ffffff"/>
  </g>
</svg>'''

# 13. Clock 3D (Chronometer / Countdown Timer)
icons["clock-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="clockBrass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="30%" stop-color="#f8c64e"/>
      <stop offset="70%" stop-color="#b8860b"/>
      <stop offset="100%" stop-color="#543300"/>
    </linearGradient>
    <radialGradient id="clockDial" cx="45%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#3b0f1a"/>
      <stop offset="70%" stop-color="#1f050d"/>
      <stop offset="100%" stop-color="#0a0104"/>
    </radialGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="110" rx="38" ry="7" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Top Crown & Loop -->
  <circle cx="60" cy="18" r="10" fill="none" stroke="url(#clockBrass)" stroke-width="4"/>
  <rect x="56" y="24" width="8" height="8" rx="2" fill="url(#clockBrass)"/>

  <!-- Outer Watch Case -->
  <circle cx="60" cy="66" r="44" fill="url(#clockBrass)" filter="drop-shadow(0 8px 10px rgba(0,0,0,0.6))"/>
  
  <!-- Dial Bevel -->
  <circle cx="60" cy="66" r="37" fill="url(#clockDial)" stroke="#d4af37" stroke-width="2"/>

  <!-- Hour Markers -->
  <circle cx="60" cy="35" r="2.5" fill="#f8c64e"/>
  <circle cx="91" cy="66" r="2.5" fill="#f8c64e"/>
  <circle cx="60" cy="97" r="2.5" fill="#f8c64e"/>
  <circle cx="29" cy="66" r="2.5" fill="#f8c64e"/>

  <!-- Clock Hands (Pointing to 8:00 IST) -->
  <line x1="60" y1="66" x2="42" y2="78" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <line x1="60" y1="66" x2="60" y2="40" stroke="#f8c64e" stroke-width="3" stroke-linecap="round"/>
  <!-- Second Hand (Red) -->
  <line x1="60" y1="72" x2="60" y2="38" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round"/>

  <!-- Center Pin -->
  <circle cx="60" cy="66" r="4" fill="#ffd700" stroke="#b8860b" stroke-width="1"/>

  <!-- Glass Dome Specular Reflection -->
  <path d="M 30 50 A 34 34 0 0 1 85 40 A 34 26 0 0 0 30 50 Z" fill="#ffffff" opacity="0.25"/>
</svg>'''

# 14. Card 3D (Payment Modes)
icons["card-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="cardDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b0a18"/>
      <stop offset="50%" stop-color="#19030a"/>
      <stop offset="100%" stop-color="#050002"/>
    </linearGradient>
    <linearGradient id="chipGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="50%" stop-color="#f8c64e"/>
      <stop offset="100%" stop-color="#996e08"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <rect x="18" y="32" width="84" height="54" rx="8" fill="#000" opacity="0.6" filter="blur(6px)" transform="rotate(-8 60 60)"/>

  <!-- Card Body -->
  <g transform="rotate(-8 60 60)">
    <rect x="18" y="30" width="84" height="54" rx="8" fill="url(#cardDark)" stroke="#f8c64e" stroke-width="2"/>
    
    <!-- Gold Foil Geometric Accent Wave -->
    <path d="M 18 55 Q 50 40 102 65 L 102 84 L 18 84 Z" fill="#b8860b" opacity="0.25"/>

    <!-- EMV Chip 3D -->
    <rect x="28" y="44" width="16" height="12" rx="3" fill="url(#chipGold)" stroke="#664600" stroke-width="1"/>
    <line x1="28" y1="50" x2="44" y2="50" stroke="#785300" stroke-width="0.8"/>
    <line x1="36" y1="44" x2="36" y2="56" stroke="#785300" stroke-width="0.8"/>

    <!-- Contactless Wave -->
    <path d="M 52 46 A 6 6 0 0 1 52 54" fill="none" stroke="#f8c64e" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M 56 43 A 10 10 0 0 1 56 57" fill="none" stroke="#f8c64e" stroke-width="1.5" stroke-linecap="round"/>

    <!-- Embossed Cardholder & Logo -->
    <rect x="28" y="68" width="38" height="4" rx="1.5" fill="#ffffff" opacity="0.8"/>
    <!-- Hologram Seal -->
    <circle cx="88" cy="68" r="7" fill="#ef4444" opacity="0.85"/>
    <circle cx="78" cy="68" r="7" fill="#f59e0b" opacity="0.85"/>
  </g>
</svg>'''

# 15. Calculator 3D
icons["calculator-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="calcBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2d0a14"/>
      <stop offset="50%" stop-color="#140207"/>
      <stop offset="100%" stop-color="#050002"/>
    </linearGradient>
    <linearGradient id="keyGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <rect x="28" y="24" width="64" height="84" rx="12" fill="#000" opacity="0.6" filter="blur(6px)"/>

  <!-- Calculator Chassis -->
  <rect x="28" y="18" width="64" height="84" rx="12" fill="url(#calcBody)" stroke="#d4af37" stroke-width="2.5" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.5))"/>

  <!-- LCD Screen -->
  <rect x="36" y="26" width="48" height="18" rx="4" fill="#000000" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="78" y="40" font-family="'Courier New', monospace" font-size="12" font-weight="900" fill="#4ade80" text-anchor="end">₹32,00,000</text>

  <!-- Keypad Buttons Grid (3 x 4) -->
  <!-- Row 1 -->
  <rect x="36" y="50" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="54" y="50" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="72" y="50" width="12" height="10" rx="3" fill="#ea580c"/>
  <!-- Row 2 -->
  <rect x="36" y="64" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="54" y="64" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="72" y="64" width="12" height="10" rx="3" fill="#ea580c"/>
  <!-- Row 3 -->
  <rect x="36" y="78" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="54" y="78" width="12" height="10" rx="3" fill="url(#keyGold)"/>
  <rect x="72" y="78" width="12" height="20" rx="3" fill="#16a34a"/>
  <!-- Row 4 -->
  <rect x="36" y="90" width="30" height="8" rx="3" fill="url(#keyGold)"/>
</svg>'''

# 16. Scales of Justice 3D (Legal / Chamarbaugwala)
icons["scale-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="brassScales" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="35%" stop-color="#f8c64e"/>
      <stop offset="70%" stop-color="#d4af37"/>
      <stop offset="100%" stop-color="#704d00"/>
    </linearGradient>
  </defs>

  <!-- Stand Base -->
  <ellipse cx="60" cy="106" rx="28" ry="6" fill="#000" opacity="0.6" filter="blur(4px)"/>
  <ellipse cx="60" cy="102" rx="22" ry="5" fill="url(#brassScales)"/>
  <rect x="57" y="24" width="6" height="78" rx="2" fill="url(#brassScales)"/>
  
  <!-- Top Center Finial -->
  <circle cx="60" cy="22" r="5" fill="#fde047" stroke="#704d00" stroke-width="1.5"/>

  <!-- Horizontal Balance Beam -->
  <path d="M 20 30 Q 60 26 100 30" fill="none" stroke="url(#brassScales)" stroke-width="4" stroke-linecap="round"/>

  <!-- Left Suspended Pan -->
  <line x1="20" y1="30" x2="12" y2="60" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="20" y1="30" x2="28" y2="60" stroke="#d4af37" stroke-width="1.5"/>
  <path d="M 10 60 C 10 70 30 70 30 60 Z" fill="url(#brassScales)" filter="drop-shadow(0 3px 4px rgba(0,0,0,0.5))"/>

  <!-- Right Suspended Pan -->
  <line x1="100" y1="30" x2="92" y2="60" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="100" y1="30" x2="108" y2="60" stroke="#d4af37" stroke-width="1.5"/>
  <path d="M 90 60 C 90 70 110 70 110 60 Z" fill="url(#brassScales)" filter="drop-shadow(0 3px 4px rgba(0,0,0,0.5))"/>
</svg>'''

# 17. Padlock 3D (Security & Privacy DPDP)
icons["lock-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="shackleSteel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#cbd5e1"/>
      <stop offset="80%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <radialGradient id="lockGold" cx="45%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="35%" stop-color="#f8c64e"/>
      <stop offset="75%" stop-color="#b8860b"/>
      <stop offset="100%" stop-color="#593c00"/>
    </radialGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="110" rx="35" ry="7" fill="#000" opacity="0.6" filter="blur(5px)"/>

  <!-- Hardened Curved Shackle -->
  <path d="M 38 55 L 38 35 C 38 18 82 18 82 35 L 82 55" fill="none" stroke="url(#shackleSteel)" stroke-width="14" stroke-linecap="round"/>

  <!-- Main Solid Lock Body -->
  <rect x="26" y="50" width="68" height="54" rx="10" fill="url(#lockGold)" stroke="#ffd700" stroke-width="2.5" filter="drop-shadow(0 8px 12px rgba(0,0,0,0.6))"/>

  <!-- Glowing Keyhole -->
  <circle cx="60" cy="72" r="6" fill="#1f0a02"/>
  <polygon points="56,74 64,74 62,88 58,88" fill="#1f0a02"/>
  <circle cx="60" cy="72" r="2.5" fill="#ffd700"/>

  <!-- Specular Reflection Across Body -->
  <path d="M 32 54 L 88 54 L 75 98 L 32 98 Z" fill="#ffffff" opacity="0.2"/>
</svg>'''

# 18. Scroll 3D (Terms & Conditions)
icons["scroll-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="parchment" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#fef3c7"/>
      <stop offset="80%" stop-color="#fde68a"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="106" rx="40" ry="7" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Rolled Scroll Back curl -->
  <path d="M 30 20 C 20 20 20 35 30 35 L 90 35 C 100 35 100 20 90 20 Z" fill="#d97706"/>

  <!-- Main Unfurled Parchment Body -->
  <path d="M 28 28 L 88 28 C 96 28 98 40 94 92 C 90 98 80 98 75 92 L 24 92 C 18 92 20 80 24 35 Z" fill="url(#parchment)" stroke="#ca8a04" stroke-width="2" filter="drop-shadow(0 6px 8px rgba(0,0,0,0.5))"/>

  <!-- Text Script Lines -->
  <line x1="36" y1="42" x2="78" y2="42" stroke="#78350f" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="36" y1="52" x2="84" y2="52" stroke="#78350f" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="36" y1="62" x2="72" y2="62" stroke="#78350f" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="36" y1="72" x2="65" y2="72" stroke="#78350f" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Red Wax Seal with Ribbon -->
  <path d="M 72 80 L 68 102 L 76 96 L 84 102 L 80 80 Z" fill="#dc2626"/>
  <circle cx="76" cy="80" r="10" fill="#991b1b" stroke="#f8c64e" stroke-width="2" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
  <circle cx="76" cy="80" r="5" fill="#f8c64e"/>
</svg>'''

# 19. Mailbox / Contact 3D
icons["mailbox-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="postBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="40%" stop-color="#0284c7"/>
      <stop offset="80%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#082f49"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="108" rx="38" ry="7" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Postbox Body -->
  <path d="M 30 45 C 30 22 90 22 90 45 L 90 98 L 30 98 Z" fill="url(#postBlue)" stroke="#38bdf8" stroke-width="2" filter="drop-shadow(0 8px 10px rgba(0,0,0,0.5))"/>

  <!-- Mail Ingestion Slot -->
  <rect x="40" y="42" width="40" height="8" rx="4" fill="#031b2e" stroke="#f8c64e" stroke-width="1.5"/>

  <!-- White Envelope Popping Out -->
  <g transform="translate(42, 28) rotate(-8)">
    <polygon points="0,0 36,0 36,24 0,24" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <polyline points="0,0 18,12 36,0" fill="none" stroke="#dc2626" stroke-width="2"/>
    <circle cx="18" cy="12" r="3" fill="#ffd700"/>
  </g>

  <!-- Royal Brass Horn / Diya Insignia on Postbox -->
  <circle cx="60" cy="74" r="12" fill="#d4af37" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="60" cy="74" r="8" fill="#78350f"/>
</svg>'''

# 20. Brain 3D (Game of Skill / Cultural Knowledge)
icons["brain-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <radialGradient id="brainGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#fde047"/>
      <stop offset="70%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </radialGradient>
  </defs>

  <!-- Outer Neural Glow -->
  <circle cx="60" cy="58" r="46" fill="#f59e0b" opacity="0.2" filter="blur(10px)"/>

  <!-- Left Hemisphere Lobes -->
  <path d="M 56 30 C 44 26 34 32 30 42 C 24 48 24 60 30 68 C 26 76 32 86 42 86 C 48 86 52 82 56 86 Z" fill="url(#brainGlow)" stroke="#ffd700" stroke-width="2.5" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.4))"/>

  <!-- Right Hemisphere Lobes -->
  <path d="M 64 30 C 76 26 86 32 90 42 C 96 48 96 60 90 68 C 94 76 88 86 78 86 C 72 86 68 82 64 86 Z" fill="url(#brainGlow)" stroke="#ffd700" stroke-width="2.5" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.4))"/>

  <!-- Central Glowing Fissure -->
  <line x1="60" y1="28" x2="60" y2="88" stroke="#ffffff" stroke-width="3" stroke-linecap="round" filter="drop-shadow(0 0 6px #fff)"/>

  <!-- Neural Nodes & Synapse Sparks -->
  <circle cx="44" cy="45" r="3" fill="#ffffff"/>
  <circle cx="76" cy="45" r="3" fill="#ffffff"/>
  <circle cx="40" cy="65" r="3.5" fill="#ffffff"/>
  <circle cx="80" cy="65" r="3.5" fill="#ffffff"/>

  <!-- Synapse Connector Lines -->
  <line x1="44" y1="45" x2="60" y2="55" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="2,2"/>
  <line x1="76" y1="45" x2="60" y2="55" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="2,2"/>
  <line x1="40" y1="65" x2="60" y2="55" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="2,2"/>
  <line x1="80" y1="65" x2="60" y2="55" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="2,2"/>
</svg>'''

# 21. Wooden Safety Crate 3D (PESO Delivery)
icons["crate-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="woodPlank" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b45309"/>
      <stop offset="50%" stop-color="#78350f"/>
      <stop offset="100%" stop-color="#451a03"/>
    </linearGradient>
    <linearGradient id="metalBrace" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="50%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="108" rx="40" ry="8" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Main Crate Box -->
  <rect x="22" y="36" width="76" height="66" rx="4" fill="url(#woodPlank)" stroke="#d97706" stroke-width="2" filter="drop-shadow(0 8px 10px rgba(0,0,0,0.6))"/>

  <!-- Horizontal Wood Planks Seams -->
  <line x1="22" y1="58" x2="98" y2="58" stroke="#260e02" stroke-width="2"/>
  <line x1="22" y1="80" x2="98" y2="80" stroke="#260e02" stroke-width="2"/>

  <!-- Diagonal Reinforcing Braces -->
  <line x1="24" y1="38" x2="96" y2="100" stroke="#92400e" stroke-width="6"/>
  <line x1="24" y1="100" x2="96" y2="38" stroke="#92400e" stroke-width="6"/>

  <!-- Steel Corner Reinforcement Brackets -->
  <rect x="22" y="36" width="14" height="14" fill="url(#metalBrace)"/>
  <rect x="84" y="36" width="14" height="14" fill="url(#metalBrace)"/>
  <rect x="22" y="88" width="14" height="14" fill="url(#metalBrace)"/>
  <rect x="84" y="88" width="14" height="14" fill="url(#metalBrace)"/>

  <!-- Brass Rivets -->
  <circle cx="26" cy="40" r="2" fill="#ffd700"/>
  <circle cx="94" cy="40" r="2" fill="#ffd700"/>
  <circle cx="26" cy="98" r="2" fill="#ffd700"/>
  <circle cx="94" cy="98" r="2" fill="#ffd700"/>

  <!-- PESO Certified Stencil Badge -->
  <rect x="36" y="62" width="48" height="14" rx="2" fill="#000000" opacity="0.6"/>
  <text x="60" y="73" font-family="'Cinzel', monospace" font-size="7.5" font-weight="900" fill="#4ade80" text-anchor="middle">PESO SECURE</text>
</svg>'''

# 22. Voucher 3D (Licensed Store Gift Voucher)
icons["voucher-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="voucherGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064e3b"/>
      <stop offset="60%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#022c22"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <rect x="18" y="32" width="84" height="54" rx="8" fill="#000" opacity="0.6" filter="blur(6px)"/>

  <!-- Voucher Card Body -->
  <rect x="18" y="28" width="84" height="56" rx="8" fill="url(#voucherGrad)" stroke="#f8c64e" stroke-width="2.5" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.5))"/>

  <!-- Perforated Notches on Voucher Ends -->
  <circle cx="18" cy="56" r="6" fill="#1f050d"/>
  <circle cx="102" cy="56" r="6" fill="#1f050d"/>

  <!-- Dotted Tear line -->
  <line x1="40" y1="28" x2="40" y2="84" stroke="#f8c64e" stroke-width="2" stroke-dasharray="3,3"/>

  <!-- Voucher Store QR Matrix Simulation -->
  <rect x="23" y="44" width="13" height="13" fill="#ffffff" rx="2"/>
  <rect x="25" y="46" width="4" height="4" fill="#000"/>
  <rect x="30" y="46" width="4" height="4" fill="#000"/>
  <rect x="25" y="51" width="4" height="4" fill="#000"/>

  <!-- Amount & Text -->
  <text x="46" y="46" font-family="'Cinzel', serif" font-size="9" font-weight="900" fill="#fde047">GIFT VOUCHER</text>
  <text x="46" y="62" font-family="'Outfit', sans-serif" font-size="14" font-weight="900" fill="#ffffff">₹50,000</text>
  <text x="46" y="74" font-family="'Outfit', sans-serif" font-size="7" fill="#6ee7b7">LICENSED STORE PICKUP</text>
</svg>'''

# 23. Fireworks 3D (Skyrockets)
icons["fireworks-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="rocketBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="50%" stop-color="#dc2626"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </linearGradient>
  </defs>

  <!-- Skyrocket 1 (Main tilted) -->
  <g transform="translate(45, 55) rotate(-35)">
    <!-- Wooden Guiding Stick -->
    <rect x="-2" y="10" width="4" height="55" fill="#d97706"/>
    <!-- Rocket Cylinder -->
    <rect x="-8" y="-20" width="16" height="32" rx="3" fill="url(#rocketBody)" stroke="#ffd700" stroke-width="1.5"/>
    <rect x="-8" y="-10" width="16" height="6" fill="#ffd700"/>
    <!-- Conical Nose Cone -->
    <polygon points="0,-36 -10,-20 10,-20" fill="#f59e0b" stroke="#ffd700" stroke-width="1.5"/>
    <!-- Fiery Exhaust / Sparks -->
    <polygon points="0,12 -4,26 0,22 4,26" fill="#fde047" filter="drop-shadow(0 0 6px #ea580c)"/>
  </g>

  <!-- Starburst Sparks in Background -->
  <circle cx="85" cy="25" r="3" fill="#ffffff" filter="drop-shadow(0 0 6px #ffd700)"/>
  <circle cx="95" cy="40" r="2.5" fill="#f59e0b"/>
  <circle cx="75" cy="18" r="2" fill="#ef4444"/>
  <circle cx="25" cy="35" r="2.5" fill="#ffd700"/>
</svg>'''

# 24. Shield 3D (Trust & Verification)
icons["shield-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="shieldGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="30%" stop-color="#f8c64e"/>
      <stop offset="70%" stop-color="#ca8a04"/>
      <stop offset="100%" stop-color="#713f12"/>
    </linearGradient>
    <linearGradient id="shieldEmerald" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="50%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <path d="M 60 16 C 85 16 98 25 98 50 C 98 85 60 106 60 106 C 60 106 22 85 22 50 C 22 25 35 16 60 16 Z" fill="#000" opacity="0.6" filter="blur(6px)"/>

  <!-- Shield Outer Bevel (Gold) -->
  <path d="M 60 14 C 85 14 98 23 98 48 C 98 83 60 104 60 104 C 60 104 22 83 22 48 C 22 23 35 14 60 14 Z" fill="url(#shieldGold)" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.5))"/>

  <!-- Shield Inner Field (Emerald) -->
  <path d="M 60 22 C 80 22 90 30 90 50 C 90 78 60 96 60 96 C 60 96 30 78 30 50 C 30 30 40 22 60 22 Z" fill="url(#shieldEmerald)" stroke="#ffffff" stroke-width="1.5"/>

  <!-- 3D Checkmark -->
  <polyline points="44,54 55,65 76,42" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
</svg>'''

# 25. Lightning 3D (Instant Activation & Speed)
icons["lightning-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <linearGradient id="boltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="25%" stop-color="#fef08a"/>
      <stop offset="60%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
  </defs>

  <!-- Aura -->
  <polygon points="68,8 30,62 58,62 48,112 92,48 64,48" fill="#f59e0b" opacity="0.3" filter="blur(8px)"/>

  <!-- 3D Lightning Bolt -->
  <polygon points="68,8 30,62 58,62 48,112 92,48 64,48" fill="url(#boltGrad)" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 0 10px #f59e0b)"/>
  
  <!-- Core Highlight -->
  <polygon points="66,16 38,60 56,60 52,98 84,50 64,50" fill="#ffffff" opacity="0.6"/>
</svg>'''

# 26. FAQ / Question 3D
icons["faq-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <defs>
    <radialGradient id="faqSphere" cx="40%" cy="35%" r="60%">
      <stop offset="0%" stop-color="#800b1b"/>
      <stop offset="50%" stop-color="#4d0510"/>
      <stop offset="100%" stop-color="#190105"/>
    </radialGradient>
    <linearGradient id="qGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
  </defs>

  <!-- Shadow -->
  <ellipse cx="60" cy="110" rx="38" ry="7" fill="#000" opacity="0.6" filter="blur(4px)"/>

  <!-- Crystal Ruby Sphere Base -->
  <circle cx="60" cy="60" r="46" fill="url(#faqSphere)" stroke="#f8c64e" stroke-width="3" filter="drop-shadow(0 8px 12px rgba(0,0,0,0.6))"/>

  <!-- 3D Question Mark Symbol -->
  <path d="M 46 45 C 46 34 54 28 62 28 C 72 28 78 35 78 43 C 78 52 70 56 64 61 C 61 64 61 68 61 72" fill="none" stroke="url(#qGold)" stroke-width="9" stroke-linecap="round" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.7))"/>
  
  <!-- Question Dot -->
  <circle cx="61" cy="88" r="5" fill="url(#qGold)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.7))"/>

  <!-- Glass Specular Reflection -->
  <ellipse cx="46" cy="38" rx="14" ry="7" fill="#ffffff" opacity="0.35" transform="rotate(-30 46 38)"/>
</svg>'''

# 27. Sound On 3D
icons["sound-on-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="sndGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff8d6"/>
      <stop offset="50%" stop-color="#f8c64e"/>
      <stop offset="100%" stop-color="#a16207"/>
    </linearGradient>
  </defs>

  <!-- Speaker Cone Body -->
  <path d="M 18 36 L 34 36 L 56 18 L 56 82 L 34 64 L 18 64 Z" fill="url(#sndGold)" stroke="#ffd700" stroke-width="2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.5))"/>

  <!-- Sound Waves (Small, Med, Large) -->
  <path d="M 66 38 A 16 16 0 0 1 66 62" fill="none" stroke="#fde047" stroke-width="4" stroke-linecap="round"/>
  <path d="M 76 28 A 28 28 0 0 1 76 72" fill="none" stroke="#facc15" stroke-width="4" stroke-linecap="round"/>
  <path d="M 86 18 A 40 40 0 0 1 86 82" fill="none" stroke="#eab308" stroke-width="4" stroke-linecap="round"/>
</svg>'''

# 28. Sound Off 3D
icons["sound-off-3d.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="sndMute" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="50%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>

  <!-- Speaker Cone Body (Muted Slate) -->
  <path d="M 18 36 L 34 36 L 56 18 L 56 82 L 34 64 L 18 64 Z" fill="url(#sndMute)" stroke="#cbd5e1" stroke-width="2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.5))"/>

  <!-- Red Mute Slash Lines (X) -->
  <line x1="68" y1="36" x2="88" y2="64" stroke="#ef4444" stroke-width="5" stroke-linecap="round" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
  <line x1="88" y1="36" x2="68" y2="64" stroke="#ef4444" stroke-width="5" stroke-linecap="round" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))"/>
</svg>'''

# Write all icons to disk
written = 0
for filename, content in icons.items():
    file_path = os.path.join(ICONS_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    written += 1

print(f"Successfully generated {written} ultra-high-fidelity 3D vector icons in {ICONS_DIR}")

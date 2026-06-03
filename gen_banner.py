import random

W, H = 900, 400
colors = {
    "deep_space": "#060918",
    "nebula_purple": "#1a0533",
    "nebula_blue": "#04122e",
    "star_white": "#ffffff",
    "star_blue": "#c8e0ff",
    "star_yellow": "#fff4a3",
    "neon_teal": "#00d4ff",
    "neon_green": "#39ff14",
    "neon_purple": "#bf5fff",
    "planet_base": "#1b0d3a",
    "planet_mid": "#2e1a5e",
    "planet_rim": "#5a2fa8",
    "ring_color": "#7b4fc0",
}

random.seed(42)

stars_rect = []
for _ in range(320):
    x = random.randint(0, W)
    y = random.randint(0, H)
    sz = random.choice([1, 1, 1, 2, 2, 3])
    delay = round(random.uniform(0, 6), 2)
    dur = round(random.uniform(1.5, 5), 2)
    col = random.choice([colors["star_white"], colors["star_blue"], colors["star_yellow"]])
    stars_rect.append((x, y, sz, delay, dur, col))

# Pixel nebula blobs (large blurry squares in grid layout)
nebula_blobs = []
for _ in range(60):
    x = random.randint(-50, W)
    y = random.randint(0, H)
    sz = random.randint(30, 100)
    col = random.choice(["#1a0533", "#04122e", "#0d1a40", "#1d0829"])
    op = round(random.uniform(0.15, 0.45), 2)
    nebula_blobs.append((x, y, sz, col, op))

# Planet pixel squares (voxel style)
planet_cx, planet_cy, planet_r = 750, 160, 80
planet_pixels = []
for px_x in range(planet_cx - planet_r, planet_cx + planet_r, 8):
    for px_y in range(planet_cy - planet_r, planet_cy + planet_r, 8):
        dx = (px_x - planet_cx) / planet_r
        dy = (px_y - planet_cy) / planet_r
        if dx*dx + dy*dy <= 1.0:
            # Depth shading
            depth = 1.0 - (dx*dx + dy*dy)
            if depth > 0.7:
                col = colors["planet_rim"]
            elif depth > 0.4:
                col = colors["planet_mid"]
            else:
                col = colors["planet_base"]
            planet_pixels.append((px_x, px_y, col))

# Small pixel moon
moon_cx, moon_cy, moon_r = 680, 80, 28
moon_pixels = []
for px_x in range(moon_cx - moon_r, moon_cx + moon_r, 5):
    for px_y in range(moon_cy - moon_r, moon_cy + moon_r, 5):
        dx = (px_x - moon_cx) / moon_r
        dy = (px_y - moon_cy) / moon_r
        if dx*dx + dy*dy <= 1.0:
            depth = 1.0 - (dx*dx + dy*dy)
            col = "#3d2b6e" if depth > 0.5 else "#221540"
            moon_pixels.append((px_x, px_y, col))

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
  <radialGradient id="bg_grad" cx="40%" cy="60%" r="80%">
    <stop offset="0%" stop-color="#060918"/>
    <stop offset="40%" stop-color="#0a0422"/>
    <stop offset="70%" stop-color="#04081a"/>
    <stop offset="100%" stop-color="#020510"/>
  </radialGradient>
  <radialGradient id="nebula_grad1" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#2d0b5e" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#2d0b5e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="nebula_grad2" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#01264a" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#01264a" stop-opacity="0"/>
  </radialGradient>
  <filter id="glow_teal">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow_purple">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="planet_clip">
    <circle cx="{planet_cx}" cy="{planet_cy}" r="{planet_r}"/>
  </clipPath>
  <style>
    @keyframes twinkle {{
      0%,100% {{ opacity:0.15; }}
      50% {{ opacity:1; }}
    }}
    @keyframes twinkle_fast {{
      0%,100% {{ opacity:0.3; }}
      50% {{ opacity:0.9; }}
    }}
    @keyframes orbit {{
      0% {{ transform: rotate(0deg) translateX(95px) rotate(0deg); }}
      100% {{ transform: rotate(360deg) translateX(95px) rotate(-360deg); }}
    }}
    @keyframes planet_pulse {{
      0%,100% {{ opacity:0.95; }}
      50% {{ opacity:1; }}
    }}
    @keyframes shoot1 {{
      0% {{ transform:translate(0px,0px); opacity:0; }}
      5% {{ opacity:1; }}
      30% {{ transform:translate(-260px,160px); opacity:0; }}
      100% {{ transform:translate(-260px,160px); opacity:0; }}
    }}
    @keyframes shoot2 {{
      0% {{ transform:translate(0px,0px); opacity:0; }}
      5% {{ opacity:0.8; }}
      25% {{ transform:translate(-180px,110px); opacity:0; }}
      100% {{ transform:translate(-180px,110px); opacity:0; }}
    }}
    @keyframes typewriter {{
      from {{ stroke-dashoffset: 600; }}
      to {{ stroke-dashoffset: 0; }}
    }}
    @keyframes blink {{
      0%,100% {{ opacity:1; }}
      50% {{ opacity:0; }}
    }}
    @keyframes float_planet {{
      0%,100% {{ transform:translateY(0px); }}
      50% {{ transform:translateY(-6px); }}
    }}
    @keyframes ring_shimmer {{
      0%,100% {{ opacity:0.55; }}
      50% {{ opacity:0.9; }}
    }}
    .star {{ shape-rendering:crispEdges; }}
  </style>
</defs>

<!-- Deep Space Background -->
<rect width="{W}" height="{H}" fill="url(#bg_grad)"/>

<!-- Nebula blobs (pixel grid look) -->
<rect x="0" y="0" width="380" height="300" fill="url(#nebula_grad1)" opacity="0.7"/>
<rect x="200" y="100" width="350" height="280" fill="url(#nebula_grad2)" opacity="0.6"/>
<rect x="450" y="0" width="300" height="220" fill="url(#nebula_grad1)" opacity="0.35"/>
'''

# Render nebula pixel grid
for (nx, ny, nsz, ncol, nop) in nebula_blobs:
    svg += f'<rect x="{nx}" y="{ny}" width="{nsz}" height="{nsz}" fill="{ncol}" opacity="{nop}" shape-rendering="crispEdges"/>\n'

# Render stars
for i, (sx, sy, sz, delay, dur, col) in enumerate(stars_rect):
    anim_class = "twinkle_fast" if dur < 3 else "twinkle"
    svg += f'<rect x="{sx}" y="{sy}" width="{sz}" height="{sz}" fill="{col}" class="star" style="animation:{anim_class} {dur}s {delay}s infinite;"/>\n'

# Shooting star 1
svg += f'''
<g style="animation:shoot1 8s 1s infinite linear;">
  <line x1="580" y1="30" x2="610" y2="10" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.9"/>
</g>
<g style="animation:shoot2 11s 4s infinite linear;">
  <line x1="440" y1="60" x2="465" y2="42" stroke="#c8e0ff" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
</g>
'''

# Floating planet group
svg += f'<g style="animation:float_planet 6s ease-in-out infinite;">\n'

# Planet base (pixel voxels)
svg += f'<g style="animation:planet_pulse 4s ease-in-out infinite;">\n'
for (ppx, ppy, pcol) in planet_pixels:
    svg += f'<rect x="{ppx}" y="{ppy}" width="8" height="8" fill="{pcol}" shape-rendering="crispEdges"/>\n'
svg += '</g>\n'

# Planet highlight (top-left gloss pixels)
svg += f'''
<g clip-path="url(#planet_clip)">
  <rect x="{planet_cx - planet_r + 4}" y="{planet_cy - planet_r + 4}" width="28" height="12" fill="#ffffff" opacity="0.07" shape-rendering="crispEdges"/>
  <rect x="{planet_cx - planet_r + 8}" y="{planet_cy - planet_r + 16}" width="16" height="8" fill="#ffffff" opacity="0.05" shape-rendering="crispEdges"/>
</g>
'''

# Pixel ring (ellipse approximated as horizontal rects)
ring_y = planet_cy + 10
for ry in range(ring_y - 6, ring_y + 6, 3):
    ring_w_half = int((planet_r + 30) * (1 - abs(ry - ring_y + 3) / 20))
    svg += f'<rect x="{planet_cx - ring_w_half}" y="{ry}" width="{ring_w_half * 2}" height="3" fill="{colors["ring_color"]}" opacity="0.6" shape-rendering="crispEdges" style="animation:ring_shimmer 3s ease-in-out infinite;"/>\n'

# Moon
for (mpx, mpy, mcol) in moon_pixels:
    svg += f'<rect x="{mpx}" y="{mpy}" width="5" height="5" fill="{mcol}" shape-rendering="crispEdges"/>\n'

svg += '</g>\n'  # close float_planet

# Constellation dots (small cluster)
const_pts = [(110,80),(140,60),(170,90),(200,70),(165,110),(135,105)]
for i, (cx,cy) in enumerate(const_pts):
    svg += f'<rect x="{cx}" y="{cy}" width="3" height="3" fill="#7ecfff" opacity="0.6" shape-rendering="crispEdges" style="animation:twinkle 3s {i*0.4}s infinite;"/>\n'
for i in range(len(const_pts)-1):
    x1,y1 = const_pts[i]; x2,y2 = const_pts[i+1]
    svg += f'<line x1="{x1+1}" y1="{y1+1}" x2="{x2+1}" y2="{y2+1}" stroke="#3a7fa8" stroke-width="0.6" opacity="0.35"/>\n'

# --- TEXT OVERLAY ---
svg += f'''
<!-- Name -->
<text x="60" y="195" font-family="'Courier New', Courier, monospace" font-size="46" font-weight="bold" fill="{colors["neon_teal"]}" letter-spacing="2" filter="url(#glow_teal)">HIMANSHU PANDEY</text>

<!-- Title line -->
<text x="62" y="228" font-family="'Courier New', Courier, monospace" font-size="15" fill="#8ab4d4" letter-spacing="3">FULL-STACK DEVELOPER  &amp;  AI ENTHUSIAST</text>

<!-- Pixel cursor blink after title -->
<rect x="526" y="213" width="10" height="18" fill="{colors["neon_teal"]}" shape-rendering="crispEdges" style="animation:blink 1.1s step-end infinite;"/>

<!-- Tagline -->
<text x="62" y="265" font-family="'Courier New', Courier, monospace" font-size="12" fill="#556a82" letter-spacing="1">Building scalable systems &amp; AI-powered products</text>

<!-- Bottom pixel bar -->
<rect x="0" y="{H-5}" width="{W}" height="5" fill="{colors["neon_teal"]}" opacity="0.7" shape-rendering="crispEdges"/>
<rect x="0" y="{H-5}" width="{W}" height="1" fill="white" opacity="0.1" shape-rendering="crispEdges"/>
'''

svg += '</svg>'

with open("banner.svg", "w") as f:
    f.write(svg)

print(f"Generated banner.svg ({len(svg)} bytes)")

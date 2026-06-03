import random

W, H = 900, 50
random.seed(7)

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <style>
    @keyframes tw {{ 0%,100%{{opacity:0.1;}} 50%{{opacity:1;}} }}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="#060918"/>
'''

for _ in range(140):
    x = random.randint(0, W)
    y = random.randint(0, H)
    sz = random.choice([1,1,2])
    d = round(random.uniform(0,5),2)
    dur = round(random.uniform(1.5,4),2)
    col = random.choice(["#ffffff","#c8e0ff","#7ecfff","#fff4a3"])
    svg += f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{col}" shape-rendering="crispEdges" style="animation:tw {dur}s {d}s infinite;"/>\n'

# Teal neon bottom line  
svg += f'<rect x="0" y="{H-2}" width="{W}" height="2" fill="#00d4ff" opacity="0.5" shape-rendering="crispEdges"/>\n'

svg += '</svg>'
with open("divider.svg","w") as f:
    f.write(svg)
print(f"Generated divider.svg ({len(svg)} bytes)")

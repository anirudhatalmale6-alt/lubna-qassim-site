"""
Builds the chart motif that sits behind the Speaking section.

Deliberately not a world map with coastlines — that reads as a travel blog. This is a
navigator's chart: an equirectangular graticule, rhumb lines radiating from two compass
roses, and the client's four cities plotted at their true coordinates with great-circle
style arcs between them. Geometry, not geography.

Output is an inline SVG fragment (uses currentColor so it tints with the design direction).
"""
import math, os

W, H = 1200.0, 600.0
CITIES = [
    ("Los Angeles", 34.052, -118.244),
    ("London",      51.507,   -0.128),
    ("Geneva",      46.204,    6.143),
    ("Dubai",       25.205,   55.271),
    ("Singapore",    1.352,  103.820),
]
ROSES = [(210.0, 470.0, 140.0), (1020.0, 120.0, 92.0)]


def project(lat, lon):
    return (lon + 180.0) / 360.0 * W, (90.0 - lat) / 180.0 * H


def f(v):
    return f"{v:.1f}"


out = [f'<svg class="chart" viewBox="0 0 {int(W)} {int(H)}" '
       'preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">']

# ---- graticule ----
out.append('<g class="chart__grid">')
lon = -180
while lon <= 180:
    x, _ = project(0, lon)
    out.append(f'<line x1="{f(x)}" y1="0" x2="{f(x)}" y2="{f(H)}"/>')
    lon += 15
lat = -90
while lat <= 90:
    _, y = project(lat, 0)
    out.append(f'<line x1="0" y1="{f(y)}" x2="{f(W)}" y2="{f(y)}"/>')
    lat += 15
out.append('</g>')

# equator and the two tropics, slightly stronger
out.append('<g class="chart__ref">')
for lat in (23.44, 0.0, -23.44):
    _, y = project(lat, 0)
    out.append(f'<line x1="0" y1="{f(y)}" x2="{f(W)}" y2="{f(y)}"/>')
out.append('</g>')

# ---- rhumb lines from the compass roses ----
out.append('<g class="chart__rhumb">')
for cx, cy, r in ROSES:
    for i in range(32):
        a = i * math.pi / 16
        out.append(f'<line x1="{f(cx)}" y1="{f(cy)}" '
                   f'x2="{f(cx + math.cos(a) * W)}" y2="{f(cy + math.sin(a) * W)}"/>')
out.append('</g>')

# ---- compass roses ----
out.append('<g class="chart__rose">')
for cx, cy, r in ROSES:
    for k in (1.0, 0.62, 0.22):
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * k)}"/>')
    for i in range(8):
        a = i * math.pi / 4 - math.pi / 2
        out.append(f'<polygon points="'
                   f'{f(cx + math.cos(a) * r)},{f(cy + math.sin(a) * r)} '
                   f'{f(cx + math.cos(a + 0.13) * r * 0.2)},{f(cy + math.sin(a + 0.13) * r * 0.2)} '
                   f'{f(cx + math.cos(a - 0.13) * r * 0.2)},{f(cy + math.sin(a - 0.13) * r * 0.2)}"/>')
out.append('</g>')

# ---- routes between the cities, in order ----
pts = [project(la, lo) for _, la, lo in CITIES]
out.append('<g class="chart__route">')
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1.0
    # bow the arc perpendicular to the run, the way a great circle reads on a flat chart
    cxp, cyp = mx - dy / length * length * 0.16, my + dx / length * length * 0.16
    out.append(f'<path d="M{f(x1)} {f(y1)} Q{f(cxp)} {f(cyp)} {f(x2)} {f(y2)}"/>')
out.append('</g>')

# ---- the cities themselves ----
out.append('<g class="chart__city">')
for (name, lat, lon), (x, y) in zip(CITIES, pts):
    hemi_ns, hemi_ew = ('N' if lat >= 0 else 'S'), ('E' if lon >= 0 else 'W')
    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="9" class="chart__halo"/>')
    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.4" class="chart__dot"/>')
    out.append(f'<text x="{f(x + 15)}" y="{f(y - 4)}" class="chart__name">{name.upper()}</text>')
    out.append(f'<text x="{f(x + 15)}" y="{f(y + 11)}" class="chart__coord">'
               f'{abs(lat):.2f}&#176;{hemi_ns} {abs(lon):.2f}&#176;{hemi_ew}</text>')
out.append('</g>')
out.append('</svg>')

svg = "\n".join(out)
path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build/chart.svg.html")
with open(path, "w") as fh:
    fh.write(svg)
print(path, len(svg), "bytes")

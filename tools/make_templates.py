"""Generate the 1:1 Draft D paper templates (SVG, millimetres).

Frame (from docs/draft-d-spec.md): origin at the left end of the plate slot, on the
slot centre line, x right, y up, seen from above. Pin 1 x is a parameter.
Print at 100 % / "actual size", then check the 50 mm bar and the 10 mm square.
Run: python tools/make_templates.py docs/templates
"""
import sys, os

PIN1 = 2.2          # placeholder, set from the host measurement
PITCH = 2.54
L, R, B = -1.8, 21.1, -1.92
SLOT_H = 1.25

OUTLINES = {
    "full-ears": ("Full ears (Option A)", [
        (L, B), (R, B), (R, 41.0), (20.0, 43.0), (17.9, 43.0), (17.9, 41.5), (15.6, 41.5),
        (15.6, 36.0), (4.4, 36.0), (4.4, 41.5), (2.1, 41.5), (2.1, 44.4), (L + 1.0, 44.4), (L, 43.4)]),
    "short-ears": ("Short ears (ears end at y = 41.5)", [
        (L, B), (R, B), (R, 41.5), (15.6, 41.5), (15.6, 36.0), (4.4, 36.0), (4.4, 41.5), (L, 41.5)]),
    "full-ears-no-cutout": ("Full ears, no cutout (fills the USB-C gap)", [
        (L, B), (R, B), (R, 41.0), (20.0, 43.0), (2.1, 43.0), (2.1, 44.4), (L + 1.0, 44.4), (L, 43.4)]),
}

# PLACEHOLDER part positions (centre x, centre y, w, h, label, fitted). Codex's layout replaces these.
PARTS = [
    (10.6, 8.0, 6.0, 5.0, "U1 W25Q128JVPIQ 6x5", True),
    (4.4, 6.0, 1.6, 0.8, "C1", True),
    (4.4, 3.6, 1.6, 0.8, "R1", True),
    (17.0, 12.5, 1.6, 0.8, "C2 DNP", False),
    (17.0, 10.5, 1.6, 0.8, "R2 DNP", False),
]

OX, OY = 40.0, 60.0   # page position of the frame origin (mm); page is 200 x 270 mm


def X(x): return OX + x
def Y(y): return OY + (44.4 - y) * 1.0 - 0.0   # top of drawing at OY; y up


def make(key, title, poly):
    o = []
    a = o.append
    a('<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="270mm" viewBox="0 0 200 270" font-family="sans-serif">')
    a(f'<title>Steno Squid Draft D 1:1 template: {title}</title>')
    a('<rect width="200" height="270" fill="#fff"/>')
    a(f'<text x="10" y="14" font-size="5" font-weight="bold">Steno Squid Draft D, 1:1 template</text>')
    a(f'<text x="10" y="21" font-size="3.6">{title}</text>')
    a('<text x="10" y="27" font-size="2.8" fill="#444">Print at 100 % (actual size, no fit to page). Check the bar and the square below before use.</text>')
    a('<text x="10" y="31.5" font-size="2.8" fill="#444">Seen from above, USB-C at the top, left half. Cut on the solid line. Pin 1 at the left.</text>')
    a('<text x="10" y="36" font-size="2.8" fill="#444">Part positions are placeholders until the Draft D layout exists. Pin 1 x is a placeholder.</text>')
    # scale checks
    a('<line x1="10" y1="44" x2="60" y2="44" stroke="#000" stroke-width="0.3"/>')
    for k in range(0, 51, 10):
        a(f'<line x1="{10 + k}" y1="42.5" x2="{10 + k}" y2="45.5" stroke="#000" stroke-width="0.3"/>')
    a('<text x="10" y="41" font-size="2.6">50 mm</text>')
    a('<rect x="10" y="48" width="10" height="10" fill="none" stroke="#000" stroke-width="0.3"/>')
    a('<text x="22" y="54" font-size="2.6">10 mm square</text>')
    # slot band and plate right edge (alignment aids)
    a(f'<rect x="{X(0):.2f}" y="{Y(SLOT_H):.2f}" width="21.9" height="{2 * SLOT_H:.2f}" fill="#e5e7eb" stroke="#9aa0a6" stroke-width="0.2" stroke-dasharray="1 0.8"/>')
    a(f'<text x="{X(0.3):.2f}" y="{Y(-SLOT_H) + 2.6:.2f}" font-size="2" fill="#6b7280">plate slot (2.5 mm)</text>')
    # outline
    pts = " ".join(f"{X(x):.2f},{Y(y):.2f}" for x, y in poly)
    a(f'<polygon points="{pts}" fill="none" stroke="#000" stroke-width="0.35"/>')
    # parts footprints (projected, top face)
    for cx, cy, w, h, label, fit in PARTS:
        dash = '' if fit else ' stroke-dasharray="0.8 0.6"'
        a(f'<rect x="{X(cx - w / 2):.2f}" y="{Y(cy + h / 2):.2f}" width="{w}" height="{h}" fill="none" stroke="#1d6fd8" stroke-width="0.25"{dash}/>')
        a(f'<text x="{X(cx):.2f}" y="{Y(cy - h / 2) + 2.2:.2f}" font-size="1.7" fill="#1d6fd8" text-anchor="middle">{label}</text>')
    # contact row: pads, holes, crosshairs, numbers
    for i in range(8):
        px = PIN1 + PITCH * i
        cx, cy = X(px), Y(0)
        a(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="0.85" fill="none" stroke="#8a6d00" stroke-width="0.2"/>')
        a(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="0.5" fill="none" stroke="#000" stroke-width="0.25"/>')
        a(f'<line x1="{cx - 1.3:.3f}" y1="{cy:.3f}" x2="{cx + 1.3:.3f}" y2="{cy:.3f}" stroke="#000" stroke-width="0.12"/>')
        a(f'<line x1="{cx:.3f}" y1="{cy - 1.3:.3f}" x2="{cx:.3f}" y2="{cy + 1.3:.3f}" stroke="#000" stroke-width="0.12"/>')
        a(f'<text x="{cx:.3f}" y="{cy - 2.0:.3f}" font-size="2" text-anchor="middle">{i + 1}</text>')
    a(f'<text x="{X(PIN1 + 3.5 * PITCH):.2f}" y="{Y(-1.92) + 5:.2f}" font-size="2" text-anchor="middle" fill="#444">8 holes, 1.0 mm drill, 1.7 mm pads, 2.54 mm pitch. Centres at x = {PIN1:g} + 2.54 n, y = 0 (mm from slot left end)</text>')
    a(f'<text x="{X(-1.8):.2f}" y="{Y(-1.92) + 9:.2f}" font-size="2" fill="#444">{title}. Outline {R - L:.1f} x {max(y for _, y in poly) - B:.1f} mm.</text>')
    a('</svg>')
    return "\n".join(o) + "\n"


out = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(out, exist_ok=True)
for key, (title, poly) in OUTLINES.items():
    path = os.path.join(out, f"draft-d-template-{key}.svg")
    open(path, "w", encoding="utf-8", newline="").write(make(key, title, poly))
    print(path)

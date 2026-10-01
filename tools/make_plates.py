"""
Generates the monochrome 'plates' used as photography placeholders in the concept build.

These are procedural abstractions of architectural light — shafts, planes, horizons —
rendered in greyscale so the stylesheet can tint them per direction (warm / cool).
They are stand-ins: the real build drops the client's own photography into the same slots.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "img")
os.makedirs(OUT, exist_ok=True)


def linear_gradient(h, w, angle_deg, lo, hi):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle_deg)
    proj = np.cos(a) * (xx / max(w - 1, 1)) + np.sin(a) * (yy / max(h - 1, 1))
    proj = (proj - proj.min()) / max(float(np.ptp(proj)), 1e-6)
    return lo + (hi - lo) * proj


def shaft(h, w, x0, x1, skew, value, softness):
    """A soft-edged, optionally skewed vertical band of light."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = yy / max(h - 1, 1)
    left = x0 * w + skew * w * t
    right = x1 * w + skew * w * t
    inside = np.clip(np.minimum(xx - left, right - xx) / (softness * w + 1e-6), 0.0, 1.0)
    inside = inside ** 0.7
    return inside * value


def plane(h, w, y0, y1, value, softness):
    yy, _ = np.mgrid[0:h, 0:w].astype(np.float32)
    top, bot = y0 * h, y1 * h
    inside = np.clip(np.minimum(yy - top, bot - yy) / (softness * h + 1e-6), 0.0, 1.0)
    return inside * value


def vignette(h, w, strength=0.35, radius=0.85):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    d = np.sqrt(((yy - cy) / cy) ** 2 + ((xx - cx) / cx) ** 2)
    return 1.0 - strength * np.clip((d - radius) / (1.6 - radius), 0, 1) ** 1.4


def grain(h, w, rng, amount):
    n = rng.normal(0.0, 1.0, (h, w)).astype(np.float32)
    n = np.array(Image.fromarray(((n * 0.5 + 0.5) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0 - 0.5
    return n * amount


def render(name, w, h, seed, recipe, base=(0.10, 0.62), angle=78, blur=1.1, grain_amt=0.055):
    rng = np.random.default_rng(seed)
    img = linear_gradient(h, w, angle, *base)
    for kind, args in recipe:
        if kind == "shaft":
            img = img + shaft(h, w, *args)
        elif kind == "plane":
            img = img + plane(h, w, *args)
    img = np.clip(img, 0, 1)
    img = np.array(Image.fromarray((img * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(blur)), dtype=np.float32) / 255.0
    img = img * vignette(h, w)
    img = img + grain(h, w, rng, grain_amt)
    # gentle S-curve so the mid-tones hold up once the CSS tint is applied
    img = np.clip(img, 0, 1)
    img = img * img * (3 - 2 * img) * 0.88 + 0.06
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), mode="L").convert("RGB")
    path = os.path.join(OUT, name)
    out.save(path, quality=86, optimize=True, progressive=True)
    print(f"{name}  {w}x{h}  {os.path.getsize(path)//1024}kb")


PLATES = [
    # portrait slot — a tall window, light falling across a room
    ("portrait.jpg", 1000, 1250, 11, [
        ("shaft", (0.46, 0.80, -0.16, 0.42, 0.055)),
        ("shaft", (0.18, 0.30, -0.06, 0.12, 0.09)),
        ("plane", (0.74, 1.02, -0.22, 0.10)),
    ], (0.07, 0.40), 72, 1.3, 0.05),

    # long-form feature image
    ("feature.jpg", 1600, 1060, 23, [
        ("shaft", (0.05, 0.34, 0.10, 0.34, 0.07)),
        ("shaft", (0.62, 0.72, 0.04, 0.20, 0.05)),
        ("plane", (0.00, 0.26, 0.14, 0.14)),
    ], (0.12, 0.50), 100, 1.0, 0.05),

    # gallery mosaic
    ("gallery-01.jpg", 1200, 1500, 31, [
        ("shaft", (0.30, 0.55, 0.22, 0.38, 0.06)),
        ("plane", (0.58, 1.05, -0.18, 0.12)),
    ], (0.09, 0.46), 66, 1.2, 0.055),
    ("gallery-02.jpg", 1500, 1000, 37, [
        ("shaft", (0.10, 0.22, -0.05, 0.30, 0.04)),
        ("shaft", (0.36, 0.49, -0.05, 0.24, 0.04)),
        ("shaft", (0.63, 0.77, -0.05, 0.18, 0.04)),
    ], (0.10, 0.34), 90, 0.9, 0.05),
    ("gallery-03.jpg", 1200, 1200, 43, [
        ("plane", (0.10, 0.42, 0.30, 0.16)),
        ("shaft", (0.55, 0.95, 0.08, 0.16, 0.10)),
    ], (0.14, 0.52), 115, 1.4, 0.06),
    ("gallery-04.jpg", 1400, 1000, 47, [
        ("shaft", (-0.05, 0.28, 0.18, 0.40, 0.08)),
        ("plane", (0.66, 1.06, -0.16, 0.09)),
    ], (0.08, 0.44), 62, 1.1, 0.05),
    ("gallery-05.jpg", 1000, 1300, 53, [
        ("shaft", (0.24, 0.42, -0.10, 0.34, 0.05)),
        ("shaft", (0.58, 0.66, -0.10, 0.16, 0.04)),
    ], (0.11, 0.38), 84, 1.0, 0.055),
    ("gallery-06.jpg", 1500, 1000, 59, [
        ("plane", (0.00, 0.34, 0.22, 0.20)),
        ("shaft", (0.40, 0.88, 0.06, 0.14, 0.12)),
    ], (0.13, 0.48), 96, 1.3, 0.05),

    # speeches & interviews thumbnails
    ("media-01.jpg", 1400, 790, 67, [
        ("shaft", (0.08, 0.30, 0.05, 0.30, 0.06)),
        ("plane", (0.62, 1.04, -0.14, 0.10)),
    ], (0.10, 0.42), 88, 1.1, 0.05),
    ("media-02.jpg", 1400, 790, 71, [
        ("shaft", (0.52, 0.86, -0.08, 0.26, 0.07)),
        ("plane", (0.00, 0.22, 0.16, 0.14)),
    ], (0.09, 0.38), 104, 1.2, 0.05),
    ("media-03.jpg", 1400, 790, 79, [
        ("shaft", (0.20, 0.34, 0.02, 0.22, 0.04)),
        ("shaft", (0.46, 0.60, 0.02, 0.28, 0.04)),
        ("shaft", (0.72, 0.86, 0.02, 0.18, 0.04)),
    ], (0.12, 0.34), 92, 0.9, 0.05),

    # wide atmospheric break between sections
    ("interlude.jpg", 1800, 760, 83, [
        ("shaft", (0.02, 0.18, 0.12, 0.26, 0.06)),
        ("shaft", (0.30, 0.44, 0.12, 0.20, 0.05)),
        ("shaft", (0.70, 0.98, 0.12, 0.32, 0.08)),
        ("plane", (0.70, 1.08, -0.20, 0.10)),
    ], (0.07, 0.36), 86, 1.2, 0.05),
]

for name, w, h, seed, recipe, base, angle, blur, g in PLATES:
    render(name, w, h, seed, recipe, base, angle, blur, g)

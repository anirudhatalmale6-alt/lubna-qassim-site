"""Prepare the client's photographs for the web.

Light touch on purpose: these are real photographs of a real person, so no heavy
filtering. Resize, sharpen a little, save progressive JPEG. Tone is applied in CSS so a
single file serves both the warm and the monochrome treatments.
"""
import os
from PIL import Image, ImageEnhance, ImageOps

SRC = "/var/lib/freelancer/projects/40735770"
OUT = os.path.join(SRC, "build", "img")
os.makedirs(OUT, exist_ok=True)

# name, source, target width, crop box as fractions (l,t,r,b) or None, greyscale
JOBS = [
    ("chamber",      "IMG_5138", 2000, None, False),   # alone in the UN chamber — the hero
    ("desk-bw",      "IMG_5131", 1600, None, True),    # High Representative desk
    ("desk-bw-2",    "IMG_5134", 1600, None, True),
    ("portrait",     "IMG_5132", 1200, None, False),   # white-background headshot
    ("portrait-sit", "IMG_5127", 1100, None, False),
    ("portrait-col", "IMG_5133", 1100, None, False),
    ("podium",       "IMG_5125", 1200, None, False),
    # 5161 is a screenshot of a web page — crop away the white surround and the caption
    ("speaking",     "IMG_5161", 1500, (0.038, 0.022, 0.962, 0.652), False),
    ("panel-ifrc",   "IMG_5126", 1500, None, False),
    ("who-tedros",   "IMG_5142", 1500, None, False),
    ("pioneers",     "IMG_5139", 1500, None, False),
    ("balance",      "IMG_5158", 1200, None, False),
    ("riyadh",       "IMG_5162", 1500, None, False),
    ("students",     "IMG_5136", 1500, None, False),
    ("book-peace",   "IMG_5171", 900,  None, False),
    ("book-multi",   "IMG_5172", 900,  None, False),
]


def prep(name, src, width, crop, grey):
    im = Image.open(os.path.join(SRC, src + ".jpeg")).convert("RGB")
    im = ImageOps.exif_transpose(im)
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if grey:
        im = ImageOps.grayscale(im).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Sharpness(im).enhance(1.12)
    path = os.path.join(OUT, name + ".jpg")
    im.save(path, quality=82, optimize=True, progressive=True)
    print(f"{name:14} {im.size[0]}x{im.size[1]}  {os.path.getsize(path)//1024}kb")


for job in JOBS:
    prep(*job)

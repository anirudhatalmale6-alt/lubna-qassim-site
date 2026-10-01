"""Build labelled contact sheets from the client's photographs so the whole set can be
reviewed at a glance instead of one file at a time."""
import os, glob
from PIL import Image, ImageDraw

SRC = "/var/lib/freelancer/projects/40735770"
OUT = os.path.join(SRC, "shots")
os.makedirs(OUT, exist_ok=True)

COLS, ROWS = 3, 2
CELL_W, CELL_H = 600, 560
LABEL_H = 34
PER_SHEET = COLS * ROWS

files = sorted(glob.glob(os.path.join(SRC, "IMG_*.jpeg")))
files = [f for f in files if "5121" not in f]          # 5121 is the payment receipt
print(len(files), "photographs")

for sheet_i in range(0, len(files), PER_SHEET):
    chunk = files[sheet_i:sheet_i + PER_SHEET]
    sheet = Image.new("RGB", (COLS * CELL_W, ROWS * (CELL_H + LABEL_H)), (24, 24, 26))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(chunk):
        col, row = i % COLS, i // COLS
        x0, y0 = col * CELL_W, row * (CELL_H + LABEL_H)
        im = Image.open(path).convert("RGB")
        im.thumbnail((CELL_W - 16, CELL_H - 16))
        sheet.paste(im, (x0 + (CELL_W - im.width) // 2, y0 + (CELL_H - im.height) // 2))
        name = os.path.basename(path).replace(".jpeg", "")
        draw.text((x0 + 12, y0 + CELL_H + 8), f"{name}   {im.width}x{im.height}",
                  fill=(210, 210, 205))
    out = os.path.join(OUT, f"sheet-{sheet_i // PER_SHEET + 1}.png")
    sheet.save(out)
    print(out, sheet.size)

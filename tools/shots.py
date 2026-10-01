import sys, os
from playwright.sync_api import sync_playwright

OUT = "/var/lib/freelancer/projects/40735770/shots"
os.makedirs(OUT, exist_ok=True)
URL = "http://127.0.0.1:8931/"

VIEWS = [
    ("desk", 1280, 720),
    ("mob", 390, 780),
]
STOPS = [
    ("hero", 0),
    ("profile", "#profile"),
    ("expertise", "#expertise"),
    ("speaking", "#speaking"),
    ("writing", "#writing"),
    ("media", "#media"),
    ("advisory", "#advisory"),
    ("gallery", "#gallery"),
    ("enquiries", "#enquiries"),
    ("footer", ".footer"),
]
DIRS = ["chancery", "chancellery"]

only = sys.argv[1:] or None

with sync_playwright() as p:
    b = p.chromium.launch()
    for vname, w, h in VIEWS:
        page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1200)
        for d in DIRS:
            page.evaluate("d=>{document.documentElement.setAttribute('data-direction',d);"
                          "document.querySelectorAll('.dirswitch button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.dir===d)))}", d)
            page.wait_for_timeout(900)
            for sname, target in STOPS:
                if only and sname not in only:
                    continue
                if target == 0:
                    page.evaluate("window.scrollTo(0,0)")
                else:
                    page.evaluate("s=>{const el=document.querySelector(s);"
                                  "window.scrollTo(0, el.offsetTop - 70)}", target)
                page.wait_for_timeout(1400)
                path = f"{OUT}/{vname}-{d}-{sname}.png"
                page.screenshot(path=path)
                print(path, os.path.getsize(path) // 1024, "kb")
        page.close()
    b.close()

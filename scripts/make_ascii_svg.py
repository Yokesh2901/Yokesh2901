#!/usr/bin/env python3
"""Create a Matrix-green, boot-animated ASCII SVG from source-prepped.png.

Run prep_photo.py first, then:
    python scripts/make_ascii_svg.py
Optional environment variables: COLS=100, ROWS=62.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
from xml.sax.saxutils import escape
import os

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-prepped.png"
OUTPUT = ROOT / "yokesh-ascii.svg"
COLS = int(os.getenv("COLS", "100"))
RAMP = " .,:;irsXA253hMHGS#9B&@"

def main():
    if not SOURCE.exists():
        raise SystemExit("Missing source-prepped.png. Run scripts/prep_photo.py with your portrait first.")
    image = Image.open(SOURCE).convert("L")
    rows = max(24, round(COLS * image.height / image.width * 0.60))
    image = ImageOps.autocontrast(image).resize((COLS, rows), Image.Resampling.LANCZOS)
    pixels = image.load()
    lines = []
    for y in range(rows):
        line = ""
        for x in range(COLS):
            lum = pixels[x, y] / 255
            idx = max(0, min(len(RAMP)-1, round((1-lum)**0.88 * (len(RAMP)-1))))
            line += RAMP[idx]
        lines.append(line)

    width, line_height, start_y = 840, 8, 145
    height = start_y + rows * line_height + 45
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Yokesh monochrome ASCII portrait with terminal boot animation">',
        '<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#07130c"/><stop offset="1" stop-color="#050a07"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
        '<rect width="840" height="100%" rx="14" fill="url(#bg)" stroke="#1f6b3b"/>',
        '<rect x="1" y="1" width="838" height="34" rx="13" fill="#0d1c12"/><path d="M1 35H839" stroke="#1f6b3b"/>',
        '<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>',
        '<text x="420" y="22" text-anchor="middle" fill="#78a987" font-family="monospace" font-size="12">YOKESH OS // IDENTITY MODULE</text>',
        '<style>.boot{font-family:monospace;fill:#39d353;font-size:12px;opacity:0;animation:boot .5s ease forwards}.ascii{font-family:monospace;fill:#8df5a8;font-size:8px;white-space:pre;opacity:0;animation:linein .08s steps(1,end) forwards}.cursor{fill:#39d353;filter:url(#glow);animation:blink .8s steps(1,end) infinite}@keyframes boot{to{opacity:1}}@keyframes linein{to{opacity:1}}@keyframes blink{50%{opacity:0}}</style>',
        '<text class="boot" x="22" y="59">[ OK ] Loading identity kernel...</text>',
        '<text class="boot" x="22" y="79" style="animation-delay:.45s">[ OK ] Initializing ASCII renderer...</text>',
        '<text class="boot" x="22" y="99" style="animation-delay:.9s">[ OK ] Mapping facial luminance to glyph matrix...</text>',
        '<text x="22" y="121" fill="#5d9b70" font-family="monospace" font-size="10">yokesh@github:~$ ./portrait --animate --theme matrix</text>'
    ]
    for i, line in enumerate(lines):
        delay = 1.45 + i * 3.5 / rows
        parts.append(f'<text class="ascii" x="24" y="{start_y+i*line_height}" xml:space="preserve" style="animation-delay:{delay:.3f}s">{escape(line)}</text>')
    parts.append(f'<rect class="cursor" x="{24+COLS*4.8:.1f}" y="{start_y+(rows-1)*line_height-7}" width="6" height="9"/>')
    parts.append(f'<text x="22" y="{height-12}" fill="#39d353" font-family="monospace" font-size="11">YOKESH S. // ML DATA ANALYST · AI BUILDER</text></svg>')
    OUTPUT.write_text("\\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT}")

if __name__ == "__main__":
    main()

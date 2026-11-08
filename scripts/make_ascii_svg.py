#!/usr/bin/env python3
"""Generate a minimal monochrome ASCII portrait SVG from source-prepped.png."""
from pathlib import Path
from PIL import Image, ImageOps
from xml.sax.saxutils import escape
import os

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-prepped.png"
OUTPUT = ROOT / "yokesh-ascii.svg"
COLS = int(os.getenv("COLS", "78"))
RAMP = "  .,:;irsXA253hMHGS#9B&@"

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
            brightness = pixels[x, y] / 255
            index = max(0, min(len(RAMP)-1, round((1-brightness)**0.88 * (len(RAMP)-1))))
            line += RAMP[index]
        lines.append(line)
    width = COLS * 4.8 + 40
    line_height, start_y = 7.45, 65
    height = start_y + rows * line_height + 32
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="Yokesh S. monochrome ASCII portrait">',
        '<rect x="0.5" y="0.5" width="99%" height="99%" rx="10" fill="#0d1117" stroke="#30363d"/>',
        '<text x="20" y="28" fill="#8b949e" font-family="Arial,sans-serif" font-size="10" letter-spacing="1.5">YOKESH S. / PORTRAIT</text>',
        f'<path d="M20 42H{width-20:.0f}" stroke="#30363d"/>',
        '<style>.ascii{font-family:monospace;fill:#c9d1d9;font-size:8px;white-space:pre;opacity:0;animation:appear .08s steps(1,end) forwards}.cursor{fill:#c9d1d9;animation:blink 1s steps(1,end) infinite}@keyframes appear{to{opacity:1}}@keyframes blink{50%{opacity:0}}</style>'
    ]
    for i, line in enumerate(lines):
        parts.append(f'<text class="ascii" x="20" y="{start_y+i*line_height:.2f}" xml:space="preserve" style="animation-delay:{i*.045:.3f}s">{escape(line)}</text>')
    parts.append(f'<rect class="cursor" x="{width-26:.1f}" y="{start_y+(rows-1)*line_height-7:.1f}" width="5" height="8"/>')
    parts.append(f'<text x="20" y="{height-10:.1f}" fill="#8b949e" font-family="Arial,sans-serif" font-size="9">ML DATA ANALYST · AI BUILDER</text></svg>')
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT}")

if __name__ == "__main__":
    main()

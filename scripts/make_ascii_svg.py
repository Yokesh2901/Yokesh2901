#!/usr/bin/env python3
"""Generate a one-shot animated monochrome ASCII SVG from source-prepped.png."""
from PIL import Image,ImageEnhance
import os,sys,html
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,"..","source-prepped.png")
OUT=sys.argv[2] if len(sys.argv)>2 else os.path.join(HERE,"..","yokesh-ascii.svg")
COLS=int(os.getenv("COLS","120")); ROWS=round(COLS*8/15); RAMP=" .`:-=+*cs#%@"
im=ImageEnhance.Contrast(Image.open(SRC).convert("L")).enhance(1.05).resize((COLS,ROWS),Image.Resampling.LANCZOS)
px=im.load(); lines=[]
for y in range(ROWS):
 line=""
 for x in range(COLS):
  lum=pow(px[x,y]/255,1.18); line+=" " if lum>=.8 else RAMP[max(0,min(len(RAMP)-1,int((1-lum)*(len(RAMP)-1)+.5)))]
 lines.append(line)
cw=800/COLS; ch=cw*15/8; width=840; height=30+ROWS*ch+60
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height:.0f}" viewBox="0 0 {width} {height:.0f}"><rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/><text x="420" y="19" text-anchor="middle" fill="#7d8590" font-family="monospace" font-size="12">yokesh@github: ~$ ./portrait.sh</text><style>.r{{opacity:0;animation:show .1s steps(1,end) forwards}}@keyframes show{{to{{opacity:1}}}}</style>']
for i,line in enumerate(lines): parts.append(f'<text class="r" x="20" y="{45+i*ch:.1f}" fill="#c9d1d9" font-family="monospace" font-size="{ch*.86:.1f}" xml:space="preserve" style="animation-delay:{i*5.8/ROWS:.3f}s">{html.escape(line)}</text>')
parts.append(f'<text x="20" y="{height-15:.1f}" fill="#7d8590" font-family="monospace" font-size="13">yokesh@github:~$ whoami <tspan fill="#c9d1d9">Yokesh S.</tspan></text></svg>')
open(OUT,"w").write("".join(parts)); print("Wrote",OUT)

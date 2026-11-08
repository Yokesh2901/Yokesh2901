#!/usr/bin/env python3
"""Render the public contribution snapshot as an animated SVG heatmap."""
import datetime,json,os
HERE=os.path.dirname(os.path.abspath(__file__))
DATA=json.load(open(os.path.join(HERE,"..","data","contributions.json")))
OUT=os.path.join(HERE,"..","contrib-heatmap.svg")
COLORS=["#161b22","#0e4429","#006d32","#26a641","#39d353","#69f0a0"]
CELL,GAP,STEP,PAD,LEFT,TOP=12,3,15,22,30,50
days=DATA["days"]
first=datetime.date.fromisoformat(days[0]["date"])
lead=(first.weekday()+1)%7
grid=[]; col=[None]*lead
for d in days:
    dt=datetime.date.fromisoformat(d["date"]); wd=(dt.weekday()+1)%7
    while len(col)<wd: col.append(None)
    count=d["count"]; level=int(d.get("level",0))
    if count and level==0: level=1 if count<=5 else 2 if count<=15 else 3 if count<=30 else 4 if count<=50 else 5
    col.append((d["date"],count,max(0,min(5,level))))
    if len(col)==7: grid.append(col); col=[]
if col: grid.append(col+[None]*(7-len(col)))
weeks=len(grid); W=PAD+LEFT+weeks*STEP+PAD; H=230
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>text{{font-family:ui-monospace,Consolas,monospace}}.c{{opacity:0;animation:in .4s ease-out forwards}}@keyframes in{{to{{opacity:1}}}}</style><rect width="100%" height="100%" rx="12" fill="#0a0e14" stroke="#1f6feb"/>']
out+=['<circle cx="22" cy="15" r="5" fill="#ff5f56"/><circle cx="38" cy="15" r="5" fill="#ffbd2e"/><circle cx="54" cy="15" r="5" fill="#27c93f"/>',f'<text x="{W/2}" y="19" text-anchor="middle" fill="#7d8590" font-size="12">yokesh@github: ~/contributions --graph</text>']
months=set()
for ci,c in enumerate(grid):
 for cell in c:
  if cell:
   dt=datetime.date.fromisoformat(cell[0]); key=(dt.year,dt.month)
   if dt.day<=7 and key not in months:
    months.add(key); out.append(f'<text x="{PAD+LEFT+ci*STEP}" y="43" fill="#7d8590" font-size="10">{dt.strftime("%b")}</text>')
   break
for wi,name in [(1,"Mon"),(3,"Wed"),(5,"Fri")]: out.append(f'<text x="5" y="{TOP+wi*STEP+10}" fill="#7d8590" font-size="9">{name}</text>')
for ci,c in enumerate(grid):
 for ri,item in enumerate(c):
  if not item: continue
  ds,count,lvl=item; x=PAD+LEFT+ci*STEP; y=TOP+ri*STEP
  out.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{COLORS[lvl]}" style="animation-delay:{ci*.018+ri*.045:.3f}s"><title>{ds}: {count} contributions</title></rect>')
legend_y=TOP+7*STEP+15; lx=W-150
out.append(f'<text x="{lx-28}" y="{legend_y+9}" fill="#7d8590" font-size="10">Less</text>')
for i,color in enumerate(COLORS): out.append(f'<rect x="{lx+i*15}" y="{legend_y}" width="11" height="11" rx="2" fill="{color}"/>')
out.append(f'<text x="{lx+94}" y="{legend_y+9}" fill="#7d8590" font-size="10">More</text>')
out.append(f'<text x="22" y="{H-18}" fill="#39d353" font-size="13">{DATA["total_contributions"]:,} contributions in the last year</text></svg>')
open(OUT,"w").write("".join(out))
print("Rendered",OUT)

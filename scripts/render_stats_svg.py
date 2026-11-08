#!/usr/bin/env python3
"""Render an animated terminal-style GitHub stats panel."""
import datetime,json,os
HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(HERE,"..","data","contributions.json")))
out=os.path.join(HERE,"..","stats.svg")
W,H=840,880; tiles=[
("current streak",d["current_streak"]["length"]," days"),
("longest streak",d["longest_streak"]["length"]," days"),
("contributions",d["total_contributions"],""),
("active days",d["active_days"],""),
("best day",d["best_day"]["count"],""),
("avg / active day",d["avg_per_active_day"],"")]
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>text{{font-family:ui-monospace,Consolas,monospace}}.t{{opacity:0;animation:up .4s ease-out forwards}}@keyframes up{{to{{opacity:1}}}}</style><rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/><line x1="0" y1="30" x2="840" y2="30" stroke="#30363d"/><text x="420" y="20" text-anchor="middle" fill="#7d8590" font-size="12">yokesh@github: ~$ ./stats.sh</text>']
for i,(label,value,suffix) in enumerate(tiles):
 x=20+(i%2)*408; y=54+(i//2)*160
 parts.append(f'<g class="t" style="animation-delay:{i*.15:.2f}s"><rect x="{x}" y="{y}" width="392" height="142" rx="10" fill="#161b22" stroke="#30363d"/><text x="{x+22}" y="{y+36}" fill="#7d8590" font-size="19">$ {label}</text><text x="{x+22}" y="{y+95}" fill="#39d353" font-size="46" font-weight="bold">{value:,}{suffix}</text></g>')
parts.append('<text x="22" y="560" fill="#7d8590" font-size="20">$ contributions / month</text>')
monthly=d["monthly"]; peak=max([m["total"] for m in monthly] or [1]); base=810; plot_h=190; slot=790/max(1,len(monthly)); bw=slot*.58
for i,m in enumerate(monthly):
 h=max(2,plot_h*m["total"]/peak); x=25+i*slot
 parts.append(f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" fill="#26a641"><animate attributeName="height" from="0" to="{h:.1f}" dur=".6s" begin="{1+i*.04:.2f}s" fill="freeze"/></rect>')
 parts.append(f'<text x="{x+bw/2:.1f}" y="835" text-anchor="middle" fill="#7d8590" font-size="12">{datetime.date.fromisoformat(m["month"]+"-01").strftime("%b")[0]}</text>')
parts.append(f'<text x="22" y="866" fill="#7d8590" font-size="13">Yokesh S. · updated {d["range"]["end"]}</text></svg>')
open(out,"w").write("".join(parts))
print("Rendered",out)

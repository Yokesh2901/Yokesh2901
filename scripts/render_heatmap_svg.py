import json
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/contributions.json").read_text())
by_date = {x["date"]: x for x in data["days"]}
end = date.today()
start = end - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)
dates = []
d = start
while d <= end:
    dates.append(d)
    d += timedelta(days=1)
colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
cell, gap, left, top = 11, 3, 42, 40
weeks = (len(dates) + 6) // 7
width, height = left + weeks * (cell + gap) + 18, 145
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
       '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
       '<style>text{font-family:Consolas,monospace}.cell{opacity:0;animation:in .25s ease forwards}@keyframes in{to{opacity:1}}</style>',
       f'<text x="16" y="20" fill="#c9d1d9" font-size="12">{data["total"]:,} contributions · {data["username"]}</text>']
for i, day in enumerate(dates):
    week, weekday = divmod(i, 7)
    item = by_date.get(day.isoformat(), {})
    level = max(0, min(4, int(item.get("level", 0))))
    x, y = left + week * (cell + gap), top + weekday * (cell + gap)
    delay = min(week * .02 + weekday * .006, 1.5)
    out.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level]}" style="animation-delay:{delay:.2f}s"><title>{day}: {item.get("count",0)} contributions</title></rect>')
for i, label in [(0,"Mon"),(2,"Wed"),(4,"Fri")]:
    out.append(f'<text x="5" y="{top+i*(cell+gap)+9}" fill="#8b949e" font-size="9">{label}</text>')
out.append('</svg>')
(ROOT / "contrib-heatmap.svg").write_text("\n".join(out) + "\n")

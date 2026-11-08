import json, os
from pathlib import Path
from datetime import date, datetime, timezone
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
username = os.getenv("GITHUB_USERNAME", "Yokesh2901")
url = f"https://github.com/users/{username}/contributions"
response = requests.get(url, headers={"User-Agent": "profile-art-generator"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
days = []
for cell in soup.select("td[data-date]"):
    try:
        day = date.fromisoformat(cell["data-date"])
        count = int(cell.get("data-count", "0"))
    except (KeyError, ValueError):
        continue
    classes = " ".join(cell.get("class", []))
    level = next((int(c[1:]) for c in classes.split() if c.startswith("L") and c[1:].isdigit()), 0)
    if count and level == 0:
        level = min(4, 1 + (count >= 2) + (count >= 5) + (count >= 10))
    days.append({"date": day.isoformat(), "count": count, "level": level})
if not days:
    raise SystemExit("GitHub contribution calendar returned no day cells.")
days.sort(key=lambda x: x["date"])
payload = {"username": username, "updated_at": datetime.now(timezone.utc).isoformat(),
           "total": sum(x["count"] for x in days), "days": days}
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data/contributions.json").write_text(json.dumps(payload, indent=2) + "\n")
print(f"Fetched {len(days)} days for {username}")

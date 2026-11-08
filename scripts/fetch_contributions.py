#!/usr/bin/env python3
"""Fetch public GitHub contribution counts and derive streak/month statistics."""
import datetime, json, os, re, sys
import requests
from bs4 import BeautifulSoup

USERNAME=os.environ.get("GH_PROFILE_USER","Yokesh2901")
URL=f"https://github.com/users/{USERNAME}/contributions"
OUT=os.path.join(os.path.dirname(__file__),"..","data","contributions.json")

def fetch_days():
    r=requests.get(URL,headers={"User-Agent":"profile-readme-bot/1.0"},timeout=30)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    cells=soup.select("td.ContributionCalendar-day")
    if not cells: raise RuntimeError("No contribution cells found; GitHub markup may have changed.")
    days=[]
    for td in cells:
        ds=td.get("data-date")
        if not ds: continue
        tip=soup.find("tool-tip",attrs={"for":td.get("id")}) if td.get("id") else None
        txt=tip.get_text(strip=True) if tip else ""
        m=re.match(r"(\d+)",txt)
        count=int(m.group(1)) if m else 0
        if re.search("no contributions",txt,re.I): count=0
        days.append({"date":ds,"count":count,"level":int(td.get("data-level") or 0)})
    return sorted(days,key=lambda x:x["date"])

def streaks(days):
    cur=0; i=len(days)-1
    if i>=0 and days[i]["count"]==0: i-=1
    end=i
    while i>=0 and days[i]["count"]>0: cur+=1; i-=1
    cs=days[i+1]["date"] if cur else None
    ce=days[end]["date"] if cur else None
    longest=run=0; ls=le=None; start=None
    for j,d in enumerate(days):
        if d["count"]:
            if not run: start=j
            run+=1
            if run>longest: longest=run; ls=days[start]["date"]; le=d["date"]
        else: run=0
    return {"length":cur,"start":cs,"end":ce},{"length":longest,"start":ls,"end":le}

def main():
    days=fetch_days()
    if not days: raise RuntimeError("Contribution calendar is empty.")
    total=sum(d["count"] for d in days); active=sum(d["count"]>0 for d in days)
    best=max(days,key=lambda d:d["count"])
    cur,longest=streaks(days)
    monthly={}
    for d in days: monthly[d["date"][:7]]=monthly.get(d["date"][:7],0)+d["count"]
    data={"username":USERNAME,"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "range":{"start":days[0]["date"],"end":days[-1]["date"]},"total_contributions":total,
      "active_days":active,"avg_per_active_day":round(total/active,1) if active else 0,
      "current_streak":cur,"longest_streak":longest,
      "best_day":{"date":best["date"],"count":best["count"]},
      "monthly":[{"month":k,"total":v} for k,v in sorted(monthly.items())],"days":days}
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    with open(OUT,"w") as f: json.dump(data,f,indent=2)
    print(f"Saved {total} contributions for {USERNAME}.")
if __name__=="__main__": main()

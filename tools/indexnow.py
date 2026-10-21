"""Notifica a IndexNow (Bing, Yandex, Seznam, Naver...) tutti gli URL della sitemap.

Da lanciare DOPO il push, quando le pagine sono online:
    uv run python tools/indexnow.py            # tutti gli URL della sitemap
    uv run python tools/indexnow.py URL [URL]  # solo gli URL indicati
La chiave e' verificata dal file /eed0d3a3a3cfa3ba7174badf9c4256f1.txt nella radice del sito.
"""
import json, re, sys, urllib.request
from pathlib import Path

HOST = "www.tecnitaliagroup.it"
CHIAVE = "eed0d3a3a3cfa3ba7174badf9c4256f1"
RADICE = Path(__file__).resolve().parent.parent

urls = sys.argv[1:] or re.findall(r"<loc>(.*?)</loc>", (RADICE / "sitemap.xml").read_text("utf-8"))
corpo = json.dumps({"host": HOST, "key": CHIAVE,
                    "keyLocation": f"https://{HOST}/{CHIAVE}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=corpo,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req) as r:
    print(f"IndexNow: HTTP {r.status} per {len(urls)} URL")

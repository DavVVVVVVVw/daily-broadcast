"""GitHub Trending 源 —— 没有官方 API，只能爬 HTML。

这是一个真实工程课：「没有官方 API」是常态。三种办法：
  (A) 爬 github.com/trending 的 HTML（这里用的）—— 有真实的「今日新增 star」速度信号，但选择器会随改版失效；
  (B) 第三方非官方 API / RSS —— 省事但依赖别人的稳定性；
  (C) 官方 Search API 近似（created:>DATE&sort=stars）—— 稳定但只是『近似』，没有 trending 的速度算法。
本 lab 选 (A)，因为速度信号最贴近「最近大家在追什么」。⚠️ 选择器若失效，看 challenge 里的 (C) 兜底。
"""
import httpx
from bs4 import BeautifulSoup

_client = httpx.Client(timeout=30, headers={"User-Agent": "ParallightLab/2"}, follow_redirects=True)


def fetch(cfg):
    c = cfg["sources"]["github_trending"]
    lang = c.get("language", "")
    since = c.get("since", "daily")
    n = c.get("top_n", 10)
    url = f"https://github.com/trending/{lang}?since={since}" if lang else f"https://github.com/trending?since={since}"
    r = _client.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    for art in soup.select("article.Box-row")[:n]:
        a = art.select_one("h2 a")
        if not a:
            continue
        name = " ".join(a.get_text().split())
        href = "https://github.com" + a.get("href", "")
        desc_el = art.select_one("p")
        desc = desc_el.get_text(strip=True) if desc_el else ""
        stars_el = art.select_one("span.d-inline-block.float-sm-right")
        stars_today = " ".join(stars_el.get_text().split()) if stars_el else ""
        items.append(
            {
                "source": "GitHub Trending",
                "title": name,
                "url": href,
                "meta": {"desc": desc, "stars_today": stars_today},
            }
        )
    return items

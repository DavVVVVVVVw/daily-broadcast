"""Hacker News 源 —— 用 Algolia 搜索 API（无需 auth）。

  · search_by_date = 最新优先，适合每日播报
  · numericFilters=points>N 过滤掉低分噪声
  · 另一个选择是官方 Firebase API（topstories.json + item/{id}.json），
    但那要为每条故事再发一个请求；Algolia 一次就能带回标题/分数/评论数。
"""
import httpx

_client = httpx.Client(timeout=30, follow_redirects=True)  # follow_redirects：自动跟 301 http→https


def fetch(cfg):
    c = cfg["sources"]["hackernews"]
    kws = cfg["interests"]["keywords"]
    query = " ".join(kws[:3])  # 关键词太多反而稀释，取前几个
    params = {
        "tags": "story",
        "query": query,
        "numericFilters": f"points>{c['min_points']}",
        "hitsPerPage": c["top_n"],
    }
    r = _client.get("https://hn.algolia.com/api/v1/search_by_date", params=params)
    r.raise_for_status()
    items = []
    for h in r.json().get("hits", []):
        oid = h.get("objectID")
        items.append(
            {
                "source": "Hacker News",
                "title": h.get("title") or "(no title)",
                "url": h.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                "meta": {"points": h.get("points"), "num_comments": h.get("num_comments")},
            }
        )
    return items

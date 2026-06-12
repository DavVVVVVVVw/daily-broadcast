"""通用 HTML 抓取源：从新闻列表页提取标题+链接。

适用于没有 RSS feed 但列表页结构稳定的中文网站。
每个源在 config 里配一段，指定 list_url 和 link_regex 即可。
"""
import re
import httpx


def fetch(cfg):
    """从 HTML 列表页抓取条目。
    cfg 需包含:
      - list_url: 新闻列表页 URL
      - link_regex: 提取 <a> 标签的正则（默认通用模式）
      - max_results: 最多返回条数
      - base_url: 相对链接的基础 URL（可选，用于拼接 ./xxx.html）
    """
    url = cfg["list_url"]
    max_results = cfg.get("max_results", 10)
    base_url = cfg.get("base_url", "")
    label = cfg.get("label", url)

    client = httpx.Client(timeout=10, follow_redirects=True,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    r = client.get(url)
    html = r.text

    # 提取所有 <a href="...">text</a>
    links = re.findall(
        r'<a[^>]*href=["\']([^"\']*?)["\'][^>]*>(.*?)</a>',
        html, re.S | re.I
    )

    items = []
    seen_titles = set()
    for href, raw_text in links:
        if len(items) >= max_results:
            break

        # 清洗标题文本
        title = re.sub(r'<[^>]+>', '', raw_text).strip()
        title = re.sub(r'\s+', ' ', title)

        # 过滤：标题太短或太长不是新闻
        if len(title) < 12 or len(title) > 200:
            continue
        # 过滤：明显的非新闻链接
        if any(kw in title.lower() for kw in
               ["javascript", "无障碍", "返回顶部", "设为首页", "网站地图",
                "english", "关于我们", "联系我们", "search", "menu", "关闭"]):
            continue
        # 去重
        if title in seen_titles:
            continue
        seen_titles.add(title)

        # 处理相对 URL
        link = href.strip()
        if link.startswith("./"):
            link = base_url.rstrip("/") + "/" + link.lstrip("./")
        elif link.startswith("/"):
            # 从 base_url 提取根域名拼接
            if base_url:
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                link = f"{parsed.scheme}://{parsed.netloc}{link}"
        elif not link.startswith("http"):
            link = base_url.rstrip("/") + "/" + link

        items.append({
            "title": title,
            "url": link,
            "source": label,
            "meta": {"desc": title},
        })

    return items

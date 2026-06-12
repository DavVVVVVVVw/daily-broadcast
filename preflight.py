"""环境自检 —— 跑主线前先确认 .env / 网络 / webhook 都 OK。"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


def check(name, ok, hint=""):
    print(f"{'✅' if ok else '❌'} {name}" + (f"  → {hint}" if (not ok and hint) else ""))
    return ok


def main():
    ready = True
    ready &= check("PARALLIGHT_API_KEY 已注入", bool(os.environ.get("PARALLIGHT_API_KEY")), "应由 /lab-start 自动填好")
    ready &= check("GITHUB_PERSONAL_ACCESS_TOKEN 已配", bool(os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")),
                   "GitHub MCP 要用；去 github.com/settings/tokens 生成只读 fine-grained token 填进 .env")
    # 投递渠道：只检查你在 config 里选的那个（gmail 演示默认 / feishu / local）
    gmail_ok = bool(os.environ.get("GMAIL_ADDRESS") and os.environ.get("GMAIL_APP_PASSWORD"))
    feishu_ok = bool(os.environ.get("FEISHU_WEBHOOK_URL"))
    check("投递渠道已配（Gmail 或 飞书 任一）", gmail_ok or feishu_ok,
          "Gmail 需 GMAIL_ADDRESS+GMAIL_APP_PASSWORD；飞书需 FEISHU_WEBHOOK_URL。都没配就把 config 的 channel 设 local 兜底")

    print("\n网络可达性：")
    probes = [
        ("arXiv", "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1"),
        ("Hacker News", "http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=1"),
        ("GitHub Trending", "https://github.com/trending"),
    ]
    for nm, url in probes:
        try:
            r = httpx.get(url, timeout=15, headers={"User-Agent": "ParallightLab/2"})
            check(f"{nm} 可达", r.status_code == 200, f"HTTP {r.status_code}")
        except Exception as e:
            check(f"{nm} 可达", False, str(e)[:70])

    print("\n自检完成。" + ("一切就绪 → 打开 01_use_github_mcp.md" if ready else "上面 ❌ 的先处理一下（FEISHU 那条非必须）。"))


if __name__ == "__main__":
    main()

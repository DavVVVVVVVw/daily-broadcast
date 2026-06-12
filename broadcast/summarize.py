"""隔离（Isolation）—— slides 第 3 幕③。

每个数据源派一个『子 agent』：在一个**干净的上下文**里，只喂这一个源的条目，
让它产出一段浓缩摘要回传。子 agent 在自己窗口里烧的 token 留在这次调用里，
**主流程只拿回摘要**（外加『它花了多少 token』，好让你量化）。
"""
from .agent_llm import complete, text_of


def summarize_source(source_name, items, keywords, max_tokens):
    if not items:
        return {"source": source_name, "summary": "_(今日无相关条目)_", "usage": _zero()}

    lines = []
    for it in items:
        meta = it.get("meta", {})
        extra = meta.get("abstract") or meta.get("desc") or ""
        if meta.get("points") is not None:
            tag = f"({meta['points']}pts)"
        elif meta.get("stars_today"):
            tag = f"(+{meta['stars_today']})"
        else:
            tag = ""
        lines.append(f"- {it['title']} {tag}\n  {extra[:300]}\n  {it['url']}")
    blob = "\n".join(lines)

    system = (
        "你是某个信息源的『摘要子 agent』。只看下面这一个源的条目，"
        f"挑出和这些关键词最相关的 3–6 条：{', '.join(keywords)}。"
        "每条一句话说清『是什么 + 为什么值得看』，并附上链接。"
        "只输出 markdown 列表，不要寒暄、不要前后缀。"
        "记住：这段结果是要塞进别人上下文的，务必精炼、高信噪。"
    )
    resp = complete(
        [{"role": "user", "content": f"# {source_name} 今日条目\n{blob}"}],
        system=system,
        max_tokens=max_tokens,
    )
    return {"source": source_name, "summary": text_of(resp), "usage": resp.usage}


class _zero:
    input_tokens = 0
    output_tokens = 0

"""Challenge ②：排序 + 跨源去重 + top-N —— 从噪声到信号。

slides 第 3 幕 ④ 的落地：主上下文只攥「最小的高信噪 token 集合」。
"""
import re
from difflib import SequenceMatcher

# ── 排序：每个源按自己的指标排，高分在前 ──

def sort_by_metric(items, source_name):
    """预排序：把最重要的条目排前面，再喂给 LLM 摘要。

    - HN: points 从高到低
    - GitHub: stars_today 从高到低
    - arXiv: 没数值指标，保持原序（我们在 summarize 里靠关键词相关度选）
    """
    def _key(it):
        meta = it.get("meta", {})
        if source_name == "hackernews":
            return meta.get("points", 0)
        if source_name == "github_trending":
            return meta.get("stars_today", 0)
        # arXiv / 其他：没有可排序指标
        return 0

    return sorted(items, key=_key, reverse=True)


# ── 跨源去重：标题相似 → 只留一条 ──

def _title_similarity(a, b):
    """简单的标题相似度（0–1）。用 SequenceMatcher，不依赖模型。"""
    a_clean = re.sub(r"\s+", " ", a.lower().strip())
    b_clean = re.sub(r"\s+", " ", b.lower().strip())
    return SequenceMatcher(None, a_clean, b_clean).ratio()


def dedup_cross_source(items_by_source, threshold=0.7):
    """跨源去重：不同源抓到同一件事，只留第一条。

    items_by_source: {source_name: [item, ...]}
    返回去重后的 {source_name: [item, ...]}，重复的 item 从后面的源剔除。
    """
    seen_titles = []  # 已保留的标题
    result = {}

    # 处理顺序：优先按已知优先级，其余按字母序
    order = ["arxiv", "hackernews", "github_trending"]
    remaining = [s for s in items_by_source if s not in order]
    order += sorted(remaining)
    for source in order:
        if source not in items_by_source:
            continue
        kept = []
        for item in items_by_source[source]:
            title = item.get("title", "")
            is_dup = False
            for seen in seen_titles:
                if _title_similarity(title, seen) >= threshold:
                    is_dup = True
                    break
            if not is_dup:
                kept.append(item)
                seen_titles.append(title)
        result[source] = kept

    return result


# ── top-N 截断：只留最重要的 N 条 ──

def top_n(summaries_by_source, n=8):
    """从各源摘要中截断，只保留 top-N 条最相关的。

    summaries_by_source: {source_name: "summary_text", ...}
    返回截断后的合并文本。

    简化为直接限制每个源摘要行数——因为排序已在 sort_by_metric 完成。
    """
    # 简单策略：总数有限，按源均分配额
    n_sources = len(summaries_by_source)
    per_source = max(2, n // n_sources)

    parts = []
    for source, summary in summaries_by_source.items():
        lines = summary.strip().split("\n")
        # 保留标题行 + 前 per_source 行条目的内容
        header = []
        body_count = 0
        kept = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("##") or stripped.startswith("#"):
                header.append(line)
            elif stripped.startswith("-") or stripped.startswith("*"):
                if body_count < per_source:
                    kept.append(line)
                    body_count += 1
            else:
                kept.append(line)
        parts.append("\n".join(header + kept))

    return "\n\n".join(parts)

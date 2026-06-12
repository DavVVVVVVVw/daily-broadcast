# 课后 Challenge · 把它变成「你的」播报 Agent

课堂上你带跑了一遍。现在反过来——**指挥 agent**，把它改成真正为你服务的东西。
（这里练的不是手敲代码，而是「把需求讲清楚 → 让 agent 改 → 验证它真改对了」。）

三道题，难度递增。**至少做完第 1 题**再 `/lab review`。

---

## ① 换成你的兴趣（必做 · 最轻）

改 `config.yaml`：把 `keywords` / `arxiv_categories` / 各源开关，换成**你**真正关心的方向
（你做后端？关注 `distributed systems`；做产品？关注某些 GitHub 项目动态）。
跑一次，看播报变成你的口味。

**交付**：改后的 `config.yaml` + 一次播报截图/`digest.md` 片段。
**评**：你能讲清改了哪、为什么这样对**你**更有用。

---

## ② 从噪声到信号（进阶）

现在的播报基本是「抓到什么播什么」。给它加**去重 + 按重要性排序**，只留 **top-N**：

- HN 按 `points`、GitHub 按「今日新增 star」、arXiv 按与关键词的相关度；
- 跨源去重（同一条新闻别播两遍）；
- 直接呼应 slides 那句 **「最小的高信噪 token 集合」**。

**指挥提示**：让 agent 在 `run_broadcast.py` 的合成步骤里加一个排序/截断；或加一个 `broadcast/rank.py`。
**评**：排序依据站得住、能讲清你砍掉了什么、为什么。

---

## ③ 给它装个「质检员」（硬 · 二选一）

**A. evaluator-optimizer**（slides 第 4 幕提过的模式）：
让**第二个 agent** 给播报打分——覆盖度够吗？有重复吗？链接有效吗？——把不合格的**反馈回去重写**，直到达标。

**B. 把 GitHub MCP 用满**：
不只看 trending，让 agent 通过 GitHub MCP **监控你 star / 指定的几个 repo** 的新 release、重大 issue/PR，纳入播报。

**评**：评估标准/监控目标明确，闭环真跑通，你是「懂 + 指挥 + 验证」——能讲清 agent 每一步、它差点哪里出错、你怎么纠的。

---

## 想真常驻？

P5（`05_schedule_with_actions.md`）已经教你把它推上 **GitHub Actions**——GitHub 每天免费替你跑、关机也照跑。课后就真正挂上去:用 GitHub MCP 建好 private repo、配好 secrets、在 Actions 页 Run workflow 验证一次,从此**每天自动到你邮箱/飞书**。这才是「你拥有一个常驻 agent」,而不只是跑过一次的脚本。

写完 `/lab review` 提交。卡住了课堂喊 Mentor。

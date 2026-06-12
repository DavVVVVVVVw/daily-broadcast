# starter 导览

## 目录

```
.mcp.json                 # 用别人的 MCP：一段 config 接上 GitHub MCP（P1 的主角）
config.yaml               # 你关心什么 → 改这里（课后 challenge 1）
01_use_github_mcp.md      # P1 引导：在 Claude Code 里用 GitHub MCP（不写工具代码）
run_broadcast.py          # 主编排。--naive 看反面教材；正常跑看隔离+按需（P2 核心）
cron_entry.py             # 单次入口（手动跑 / 也是 GitHub Actions 每天跑的那条命令）
05_schedule_with_actions.md  # P5 引导：用 GitHub MCP 把它推上 GitHub Actions（每天免费自动跑、关机照跑）
deploy/daily.yml          # GitHub Actions 工作流模板（push 到你新仓库的 .github/workflows/）
preflight.py              # 环境自检（.env / 网络 / 渠道）
challenges.md             # 课后 3 道递增挑战
tool-mechanism.html       # 教具：浏览器打开，看「源代码 ↔ 真实输出」（含本节的 token 对照）
broadcast/                # 共享模块（building blocks 是给的，编排是你指挥的）
  agent_llm.py            #   到 Parallight 代理的 LLM 客户端（complete / text_of）
  sources/                #   三个数据源，各导出 fetch(cfg) -> [轻量条目]
    arxiv.py              #     复用 Lab-1 的 arXiv + 429 纪律
    hackernews.py         #     HN Algolia 搜索 API（无 auth）
    github_trending.py    #     爬 HTML（GitHub Trending 没有官方 API）
  summarize.py            #   隔离：每源一个子 agent，只回传摘要
  digest.py               #   卸载+压缩：digest.md 落盘、跨天去重
  deliver/__init__.py     #   投递分发：按 config 的 channel 选 mailer / feishu
    mailer.py             #     Gmail/SMTP 邮件（演示默认 · 在国外推荐）
    feishu.py             #     飞书 webhook（在大陆推荐 · URL 即凭据）
digest.md                 # 运行后生成（已 gitignore）：agent 的「记忆」就在这个文件里
```

## 起步

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # /lab-start 会自动填好 LLM 部分；GitHub token + 投递渠道凭据 你来填
python preflight.py         # 自检
```

### 填凭据（都进 .env，绝不进 git）

1. **GitHub token**：`github.com/settings/tokens` → fine-grained → 只勾只读 public_repo → 填 `GITHUB_PERSONAL_ACCESS_TOKEN`。
   - ⚠️ 到 **P5**（用 GitHub MCP 搭 Actions）时要**换成有写权限的** token（classic PAT，勾 `repo` + `workflow`）—— 建仓 + 推 workflow 文件需要。见 `05_schedule_with_actions.md`。
2. **投递渠道（按你在哪选一个，在 `config.yaml` 设 `delivery.channel`）**：
   - `gmail`（默认 · 在国外推荐）：开两步验证 → `myaccount.google.com/apppasswords` 生成**应用专用密码** → 填 `GMAIL_ADDRESS` + `GMAIL_APP_PASSWORD`（`MAIL_TO` 留空就发给自己）。
   - `feishu`（在大陆推荐）：飞书群 → 设置 → 群机器人 → 添加「自定义机器人」→ 复制 webhook 地址 → 填 `FEISHU_WEBHOOK_URL`（开了「签名」就再填 `FEISHU_WEBHOOK_SECRET`；开「关键词」填「播报」即可，标题里已含）。
   - `local`：都不想配？设 `channel: local`，只写本地 `digest.md` 兜底。
   - 💡 为什么分渠道：GFW 只挡「从大陆**读** Gmail」，不挡「从境外**发** Gmail」——这是 kp-04 的核心。

## 课堂主线顺序

```bash
# P1：用别人的 MCP —— 看 01_use_github_mcp.md（/mcp + MCP Inspector dump tools/list）
python run_broadcast.py --naive   # P2：反面教材，看 input_tokens 爆炸
python run_broadcast.py           # P2：隔离+按需，看 input_tokens 小很多
python run_broadcast.py           # P3：再跑一次，看它去重（卸载+压缩）
#                                   P4：邮箱/飞书收到播报（配好渠道后）
python cron_entry.py              # P5(先)：证明无人值守能跑一次
#                                   P5(再)：看 05_schedule_with_actions.md —— 用 GitHub MCP 推上 GitHub Actions，每天免费自动跑
```

> `agent/` 那套零件来自 Lab-1。这节课**不让你手敲** building blocks——你练的是**指挥**它们组装，
> 以及在 `run_broadcast.py` 的 `# 👉 指挥点` 处做 context 取舍。

# P5 · 让它真·常驻：把闹钟交给 GitHub Actions

到这里你的 agent 已经能**跑一整轮 + 投递**了。但你得手动敲命令。最后一步：**让它每天自己醒来跑**，关机也照发。

## 先想清楚一件事（kp-05 的核心）

能不能让 **GitHub MCP** 自己每天定时跑？——**不能**。MCP server 是「手」，被调用才动，**没有时钟**。
那「每天定时」谁负责？——**GitHub Actions**（GitHub 的 CI/CD,自带 cron 调度器,而且**对你免费**)。

> 别把这两个 GitHub 的东西搞混：**GitHub MCP = 手**（你 P1 用的那个工具），**GitHub Actions = 闹钟 + 免费算力**。
> 三层:`GitHub Actions cron(WHEN) → cron_entry.py(WHAT) → MCP/API(碰世界的手)`。

## Step 1 · 先证明它能无人值守跑

```bash
python cron_entry.py
```
没人守着，它也跑完一整轮 + 投递 + 更新 `digest.md`。**这就是 GitHub Actions 每天会替你执行的那一条命令。**

## Step 2 · 指挥 agent 把它搬上 GitHub（用 P1 那个 GitHub MCP）

用自然语言指挥你的 agent —— **明确要求它只用 GitHub MCP 工具**（`create_repository`、`push_files`/`create_or_update_file`）：

> 用 **GitHub MCP 工具**（create_repository / push_files），给我**新建一个 private 仓库** `my-daily-broadcast`，把当前 `starter/` 里的 broadcast 代码（`broadcast/`、`run_broadcast.py`、`cron_entry.py`、`requirements.txt`、`config.yaml`）推上去，**但绝对不要 push `.env` 和 `.venv`**；再把 `deploy/daily.yml` 推到仓库的 `.github/workflows/daily.yml`。**全程只用 GitHub MCP 工具，不要用 `gh` CLI、不要 `git push`。**

> 🔒 **为什么禁 gh**：沙箱/你的机器里有 `gh`，agent 默认就爱用它——但那样你**根本看不到 MCP 在干活**，这节课就白上了。如果 agent 开始敲 `gh` / `git push`，**拦住它**：「这步必须走 GitHub MCP 工具，我要看 MCP 替我建仓+推文件」。盯着它每一步调的是 `create_repository` / `push_files` 这些 **MCP 工具**，而不是 shell 命令。

> ⚠️ **这一步需要【写权限】的 token——不是 P1 那个只读的！** 建仓 + 推 workflow 文件要更高的权限。
> GitHub MCP 用的是 `.mcp.json` 里的 `GITHUB_PERSONAL_ACCESS_TOKEN`，把它换成一个有写权限的：
> 到 [github.com/settings/tokens](https://github.com/settings/tokens) → **Tokens (classic)** 生成一个，勾 **`repo`** + **`workflow`** 两个 scope（建私有仓 + 推 `.github/workflows/` 文件都要）。
> 这正好复习 kp-04:**权限按需给（P1 只读、P5 才升到写）、当 secret 管、用完可以删**——这就是「最小权限」的活教材。

**这就把 P1「用别人的 MCP」和「常驻」接上了**：同一个 GitHub MCP，这次用来**搭自动化**。

## Step 3 · 配 secrets（凭据即密码，绝不进 YAML）

> 💡 **这是 MCP 唯一做不到的一步，也正好让你看清 MCP 的边界**：GitHub MCP **没有设 secret 的工具**（secret 要 libsodium 加密）。所以**只有这里**才退到网页 / `gh secret set`——而且 agent 要**明说**「这步 MCP 没有工具，所以用 gh」。能建仓、能推文件（MCP）≠ 能设密（MCP 不行）。这才是诚实地用工具。

到新仓库 **Settings → Secrets and variables → Actions → New repository secret**，加这几个（或用 `gh secret set`）：

| Secret 名 | 值 |
|---|---|
| `PARALLIGHT_API_KEY` | 你 `.env` 里那个 |
| `GH_BROADCAST_TOKEN` | 你的 GitHub token（⚠️ secret 名**不能**以 `GITHUB_` 开头，所以叫这个） |
| `GMAIL_ADDRESS` / `GMAIL_APP_PASSWORD` / `MAIL_TO` | Gmail 那三项（在大陆改用 `FEISHU_WEBHOOK_URL`） |

## Step 4 · 立刻验证（不用等到明天）

到仓库 **Actions** 页 → `daily-broadcast` → 点 **Run workflow**（这就是 `workflow_dispatch`）。
看它跑绿 + **你的邮箱收到播报** → **证明 GitHub 在替你跑了**。之后它每天 09:17（北京）自动跑。

## 几个真实的坑（诚实工程）

- **时间不精准**：Actions cron 最小 5 分钟、整点高峰会延迟甚至丢任务 → 模板用了 `17 1 * * *`（非整点）。UTC 时区。
- **public 仓库闲置 60 天会被自动停**（每日跑本身不算「活动」）→ 用 **private 仓库**;模板最后那步**把 digest.md 提交回仓库**,既是 agent 的「记忆」持久化(kp-03 的卸载),又顺手算「活动」、让定时不被停。一举两得。
- **幂等**:cron 可能延迟/重复 → `digest.md` 去重保证重跑也不刷屏。

---

✅ 过 **kp-05** 你要能说出：
1. **MCP 没有时钟**，定时这件事必须交给外部调度器（这里是 GitHub Actions cron）。
2. 三层：调度器 → agent → MCP（手）；学员常想让 MCP 干调度的活,它干不了。
3. secrets 进 Actions Secrets、不进 YAML;digest 提交回仓库既存记忆又保活定时。

🎉 到这儿,你不再是「手动跑一个脚本」——你有了一个**跑在你自己 GitHub 上、每天免费替你发、关机也照跑的 agent**。

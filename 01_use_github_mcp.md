# P1 · 用别人的 MCP（不写一行工具代码）

> 这一步不在某个 `.py` 里跑 —— 它发生在你的 **Claude Code 会话**里。MCP 是你和工具之间的协议。

## 1. 看一眼配置：工具是从哪来的？

打开 `starter/.mcp.json`。注意：里面**没有任何 GitHub API 的实现代码**，只有一段：

```json
"github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"], "env": { ... } }
```

这段配置的意思是：「启动那个**别人发布好的** GitHub MCP server，连上它」。你**消费**它，不**实现**它。

## 2. 看工具凭空出现

在 Claude Code 里输入：

```
/mcp
```

你会看到工具箱里多了一排 `github` 的工具：查 repo、读文件、列 issue、看 PR、搜代码……
**这些工具你一行都没写。** 它们来自那个 server。

## 3. 用 MCP Inspector 把 server「拆开看」（tools / resources / prompts）

`/mcp` 看到的是「有哪些工具」。想看 **server 内部到底长什么样**——每个工具的描述、input schema，还有 resources / prompts——用官方的 **MCP Inspector**（`--cli` 终端模式，无需浏览器）：

```bash
# 先让 token 进环境（或直接 source 你的 .env）
export GITHUB_PERSONAL_ACCESS_TOKEN=<你的-github-token>

# 看 server 暴露的全部工具（tools/list）—— 名字 + 描述 + input schema
npx @modelcontextprotocol/inspector --cli \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN \
  npx -y @modelcontextprotocol/server-github \
  --method tools/list
```

仔细看打印出来的 JSON：每个工具就是 `name` + `description` + `inputSchema`。**这正是模型的 client 在背后做的事**——它先 `tools/list` 发现工具，而模型能看到的**只有这些描述和 schema，看不到任何实现**。

再看另两种 primitive、以及直接调一个工具：

```bash
# 三种 primitive 各看一眼（把上面命令的 --method 换掉）
#   --method resources/list   # 能「读」的资源
#   --method prompts/list     # 能复用的提示词模板

# 直接调一个工具（tools/call）—— 不经过模型，你自己当 client
npx @modelcontextprotocol/inspector --cli \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN \
  npx -y @modelcontextprotocol/server-github \
  --method tools/call --tool-name search_repositories --tool-arg query=modelcontextprotocol
```

> 💡 和 slides 第 7 幕对上：**Host** = Claude Code，**Client** = 连 server 的那条连接，**Server** = 这个 github 进程，**三积木** = 你刚 dump 出来的 tools / resources / prompts。Inspector 让你**绕过模型、直接当 client**，看清协议本身长什么样。

## 4. 指挥 agent 用一次（只用 MCP 工具，别让它用 gh）

用自然语言指挥（不要自己写代码），并**明确要求用 GitHub MCP 工具**：

> 用 **GitHub MCP 工具**（不要用 `gh`），看一下 `anthropics/anthropic-sdk-python` 的几条 open issue + 最近几个 commit，挑出对我们这门课有用的。

盯着 agent 调的是 `list_issues` / `list_commits` / `get_file_contents` 这些 **MCP 工具**、拿回**真实**的 GitHub 数据——而不是在 shell 里敲 `gh`。这才是「用别人的 MCP」。

> ⚠️ **沙箱/你机器里有 `gh`，agent 默认爱用它。** 如果它开始敲 `gh`，**拦住**：「走 GitHub MCP 工具，我要看 MCP 在干活。」到 P5 建仓 / 推 workflow 时同理——这节课的魂就是**看见 MCP 替你做事**。

## 5. 安全（kp-04 会再讲一遍）

`.mcp.json` 里的 `GITHUB_PERSONAL_ACCESS_TOKEN` 就是凭据：

- 给**最小权限**（这节课只读 public repo 就够）；
- 放 `.env`，**绝不进 git / 截图 / 聊天**。

---

✅ 想清楚这几句你就过了 **kp-01**：
1. 「用别人的 MCP = 加一段 config，Client 靠 `tools/list` 自动发现工具」——你刚用 Inspector 亲眼 dump 了那份 tools/list，而且没写一行工具实现。
2. 模型能看到的**只有工具的描述 + input schema**，看不到实现；调用走 `tools/call`。
3. 「用 vs 造」：这节课是**用**；第五节课才**造**一个自己的 MCP server。

下一步 → 回终端跑 `python run_broadcast.py --naive`，开始 P2。

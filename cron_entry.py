"""服务端 cron 的入口 —— slides 第 7 幕 + kp-05：MCP 没有时钟，调度来自外部。

手动跑一次就是『模拟 cron 叫醒它一次』：无人值守，跑完一整轮 + 推送 + 更新 digest。

  python cron_entry.py

三层别搞混：
  调度器（决定 WHEN：服务端 cron / 沙箱定时） → 这个脚本/agent（决定 WHAT） → MCP server（HANDS：真去碰 GitHub）
MCP server 自己**不会**定时；它只在被调用时才动。所以闹钟必须在外面。

幂等（重跑安全）：cron 可能延迟/重复触发，digest 去重保证重跑一次也不会重复刷屏。
"""
import run_broadcast

if __name__ == "__main__":
    # 和手动跑同一条路径——区别只是『谁来叫醒它』。
    run_broadcast.main()

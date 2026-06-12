"""邮件投递 —— 默认走 Gmail SMTP（课堂演示用）。

关键事实（kp-04）：GFW 只挡「从大陆**访问** Google」，不挡「从**境外发** Gmail」。
所以在美国 / 境外沙箱里用 smtp.gmail.com 发信完全正常 —— 演示用 Gmail 没问题。
真正的分叉是：agent 在哪发(send) + 你在哪读(收)。在大陆读 @gmail.com 要 VPN，那就改用飞书。

⚠️ Gmail SMTP 不收你的登录密码：要先开两步验证，再生成一个「应用专用密码」(App Password)，
   填到 .env 的 GMAIL_APP_PASSWORD。换别的邮箱就改 SMTP_HOST/PORT/USER/PASSWORD。
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def push(title: str, markdown: str) -> dict:
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = (os.environ.get("GMAIL_ADDRESS") or os.environ.get("SMTP_USER") or "").strip()
    pw = (os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("SMTP_PASSWORD") or "").strip()
    to = (os.environ.get("MAIL_TO") or user).strip()  # 默认发给自己

    if not (user and pw):
        return {"ok": False, "reason": "GMAIL_ADDRESS / GMAIL_APP_PASSWORD 没配（用 channel: local 兜底）"}

    msg = MIMEText(markdown, "plain", "utf-8")
    msg["Subject"] = Header(title, "utf-8")
    msg["From"] = user
    msg["To"] = to
    try:
        with smtplib.SMTP(host, port, timeout=25) as s:
            s.starttls()
            s.login(user, pw)
            s.sendmail(user, [to], msg.as_string())
    except Exception as e:  # 在大陆本地跑会卡在这里(连不上 smtp.gmail.com)——这正是 kp-04 的现场
        return {"ok": False, "reason": f"SMTP 失败（transport）: {e}"}
    return {"ok": True, "to": to}

# 💡 想发更漂亮的 HTML 邮件？把 MIMEText(markdown, "plain", ...) 换成 "html" 并把 markdown 渲染成 HTML。

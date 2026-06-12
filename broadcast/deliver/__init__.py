# 投递渠道分发器。channel 来自 config.yaml：gmail | feishu | local。
# 同一份播报，发到哪取决于『你在哪发、你在哪读』——这就是 kp-04 的部署决策。
from . import mailer, feishu


def deliver(channel: str, title: str, body: str, **kwargs) -> dict:
    if channel in ("gmail", "email", "smtp"):
        return mailer.push(title, body)
    if channel == "feishu":
        return feishu.push(title, body, webhook_url=kwargs.get("feishu_webhook_url", ""))
    if channel == "local":
        return {"ok": True, "channel": "local", "note": "只写本地 digest.md，不外发"}
    return {"ok": False, "reason": f"未知 channel: {channel}（用 gmail / feishu / local）"}

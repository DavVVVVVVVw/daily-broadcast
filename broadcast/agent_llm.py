"""到 Parallight 代理的 LLM 客户端 —— 和 Lab-1 的 agent/llm.py 是同一层薄包装：
进 messages，出模型响应（.content / .stop_reason / .usage）。没有魔法。"""
import os
from anthropic import Anthropic

_client = None


def client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(
            api_key=os.environ.get("PARALLIGHT_API_KEY", ""),
            base_url=os.environ.get("PARALLIGHT_BASE_URL", "https://token.parallight.ai/api/llm"),
        )
    return _client


MODEL = os.environ.get("PARALLIGHT_MODEL", "claude-sonnet-4-6")


def complete(messages, tools=None, system=None, max_tokens=1024):
    """一次模型调用。返回 anthropic 的响应对象——重点是 resp.usage.input_tokens，
    这节课我们要靠它量出『隔离+按需』比『无脑全塞』省多少。"""
    kwargs = {"model": MODEL, "max_tokens": max_tokens, "messages": messages}
    if tools:
        kwargs["tools"] = tools
    if system:
        kwargs["system"] = system
    return client().messages.create(**kwargs)


def text_of(resp) -> str:
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()

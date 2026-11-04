#!/usr/bin/env python
"""Diagnose the chat/LLM configuration and make a live test call.

Used by `just chat-check`.
"""
import os
import sys

# Make the repository root importable (this script lives in scripts/).
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

import django

django.setup()

from django.conf import settings  # noqa: E402


def main() -> int:
    provider = (os.getenv("LLM_PROVIDER", "").strip().lower() or "(auto)")
    key_src = (
        "INCEPTION"
        if os.getenv("INCEPTION_API_KEY")
        else ("OPENAI" if settings.LLM_API_KEY else "NONE")
    )

    print("Provider             :", provider)
    print("Key source           :", key_src)
    print("Base URL             :", settings.LLM_BASE_URL or "(openai default)")
    print("Model                :", settings.LLM_MODEL)

    if key_src == "NONE":
        print(
            "ERROR: no LLM API key configured "
            "(set INCEPTION_API_KEY or OPENAI_API_KEY in .env)"
        )
        return 1

    print("Testing chat pipeline...")
    from eliasells.graph import chatbotapp
    from langchain_core.messages import HumanMessage

    try:
        out = chatbotapp.invoke(
            {"messages": [HumanMessage(content='Bonjour, dis juste "OK"')]},
            {"configurable": {"thread_id": "just-chat-check"}},
        )
    except Exception as exc:  # noqa: BLE001 - surface the real error
        print(f"ERROR: chat call failed: {exc}")
        return 1

    reply = out["messages"][-1].content
    print("Reply:", reply[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())

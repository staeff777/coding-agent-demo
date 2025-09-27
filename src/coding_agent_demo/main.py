#!/usr/bin/env python3

from .agent.chat_session import run_chat
from .config.settings import settings

def ensure_workspace():
    wp = settings.workspace_root
    wp.mkdir(parents=True, exist_ok=True)
    print(f"Using Workspace: {wp}")

def run():
    ensure_workspace()
    run_chat()

if __name__ == "__main__":
    run()

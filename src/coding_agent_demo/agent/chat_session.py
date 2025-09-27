import json
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Tuple


# Project-local imports
from .llm import chat_completion
from .prompts import system_prompt
from .tool_call_handler import handle_tool_calls

# --------------------------
# command handling
# --------------------------

class Command(Enum):
    HELP = auto()
    NEW  = auto()
    QUIT = auto()
    NONE = auto()


def parse_command(text: str) -> Command:
    t = text.strip().lower()
    if t == "/help":
        return Command.HELP
    if t == "/new":
        return Command.NEW
    if t in {"/quit", "/exit"}:
        return Command.QUIT
    return Command.NONE


def print_help() -> None:
    print(" available commands:")
    print("  /new          : Start a new session (clear context)")
    print("  /exit /quit   : Exit agent (also Ctrl+C or Ctrl+D)")
    print("  /help         : Show this help")




# ----------------------------
# Chat session
# ----------------------------

class ChatSession:
    """
      - Read user input or collect tool responses
      - Send messages to LLM
      - Show LLM's message
      - Execute tool calls by the LLM
    """
    # approval_fn: Callable[[str], bool] = ask_yes_no
    def __init__(self):
        self.messages: List[Dict] = [{"role": "system", "content": system_prompt()}]
        #self.approval_fn = approval_fn

    def reset(self) -> None:
        print("\n --------------------------------------")
        print("        Starting a new Session")
        print(" --------------------------------------\n")
        self.messages = [{"role": "system", "content": system_prompt()}]

    def run(self) -> None:
        while True:
            # Accept user input when last message wasn't a tool response
            if self.messages[-1]["role"] != "tool":
                try:
                    user_text = input("\nUSER » ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if not user_text:
                    continue

                cmd = parse_command(user_text)
                if cmd is Command.HELP:
                    print_help()
                    continue
                if cmd is Command.NEW:
                    self.reset()
                    continue
                if cmd is Command.QUIT:
                    break

                self.messages.append({"role": "user", "content": user_text})

            # Call the llm
            response = chat_completion(self.messages)
            assistant_msg = response.message

            # add llm messages and/or tool calls to the message list
            stored_assistant = {"role": "assistant"}
            if assistant_msg.content:
                stored_assistant["content"] = assistant_msg.content
            if assistant_msg.tool_calls:
                stored_assistant["tool_calls"] = assistant_msg.tool_calls

            self.messages.append(stored_assistant)


            # show message content (if any)
            if assistant_msg.content:
                print(f"\nAGENT » {assistant_msg.content}")

            # Handle tool calls (if any).
            tool_calls = getattr(assistant_msg, "tool_calls", None) or []
            if tool_calls:
                tool_messages = handle_tool_calls(tool_calls)
                self.messages.extend(tool_messages)



def run_chat() -> None:
    ChatSession().run()

import json
from typing import Callable, Dict, List, Optional, Tuple
from ..core import file_ops, merge, tree_sitter_utils

# ---------------------------
# Tool registry & helpers
# ---------------------------

TOOL_REGISTRY: Dict[str, Callable[..., object]] = {
    "list_tree":            file_ops.list_tree,
    "read_file":            file_ops.read_file,
    "write_file":           file_ops.write_file,
    "rename_file":          file_ops.rename_file,
    "delete_path":          file_ops.delete_path,
    "three_way_merge":      merge.three_way_merge,
    "list_public_symbols":  tree_sitter_utils.list_public_symbols,
}

TOOLS_REQUIRING_APPROVAL = {"write_file", "rename_file", "delete_path", "three_way_merge"}

def ask_yes_no(question: str, *, prompt: str = "Continue execution? [y/N] ") -> bool:
    print(question)
    try:
        return input(prompt).strip().lower() == "y"
    except (EOFError, KeyboardInterrupt):
        return False

def safe_json_loads(s: str) -> Tuple[Optional[dict], Optional[str]]:
    try:
        return json.loads(s), None
    except Exception as e:
        return None, f"Could not parse tool arguments as JSON: {e}"



def handle_tool_calls(tool_calls: List) -> List[Dict]:
    """
    A model can call multiple tools in one response.
    We execute them sequentially, appending their results to the message list.
    """
    messages = []
    for tc in tool_calls:
        func_name = tc.function.name
        raw_args  = tc.function.arguments

        def append_result(result):
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": func_name,
                "content": json.dumps(result, ensure_ascii=False),
            })

        # parse arguments
        args_obj, arg_err = safe_json_loads(raw_args)
        if arg_err:
            append_result( {"ok": False, "error": arg_err})
            continue

        # ask user for approval if needed
        if func_name in TOOLS_REQUIRING_APPROVAL:
            preview = "\n".join(f"<{k}>: {v}" for k, v in args_obj.items())
            if not ask_yes_no(f"\n Execute [{func_name}] with \n{preview}"):
                append_result({"ok": False, "error": "Tool call declined by user."})
                continue

        # locate and the tool function
        func = TOOL_REGISTRY.get(func_name)
        if func is None:
            append_result({"ok": False, "error": "Unknown Tool"})
            continue

        # execute the tool function
        try:
            result = func(**args_obj)
            append_result(result)
        except Exception as e:
            append_result({
                "ok": False,
                "error": f"Tool execution error: {e}"
            })

    return messages

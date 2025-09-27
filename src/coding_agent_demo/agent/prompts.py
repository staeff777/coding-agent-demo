from ..core.file_ops import list_tree
from ..core.sandbox import resolve_in_workspace


def agents_md() -> str:
    """
    Return content from AGENTS.md in workspace if it exists, otherwise empty string.
    """
    try:
        agents_path = resolve_in_workspace("AGENTS.md")
        if agents_path.exists():
            return agents_path.read_text(encoding="utf-8")
        return ""
    except (Exception):
        return ""


def system_prompt():
   """ Basic system prompt for the Coding-Agent. """

   return f"""\
    You are Coding-Agent, an autonomous software engineer.
    A human will describe coding tasks. You may call the provided
    tools to inspect the workspace and modify files *only inside* it.

    Initial list_tree call:
    {list_tree()}

    {agents_md()}
    """

# Definition of available tool functions for the agent
FUNCTIONS = [
    {
        "name":"list_tree",
        "description":"List the directory tree relative to the workspace root. States linecount (l) or filesize.",
        "parameters":{
            "type":"object",
            "properties":{
                "relative_path":{"type":"string","default":"."}
            }
        }
    },
    {
        "name":"read_file",
        "description":"Return the UTF‑8 text content of a file",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{"type":"string"}
            },
            "required":["path"]
        }
    },
    {
        "name":"write_file",
        "description":"Create or overwrite a file with given text",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{"type":"string"},
                "content":{"type":"string"},
                "overwrite":{"type":"boolean","default":True}
            },
            "required":["path","content"]
        }
    },
    {
        "name":"rename_file",
        "description":"Rename or move a file/folder INSIDE workspace",
        "parameters":{
            "type":"object",
            "properties":{
                "old":{"type":"string"},
                "new":{"type":"string"}
            },
            "required":["old","new"]
        }
    },
    {
        "name":"delete_path",
        "description":"Delete file or directory recursively",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{"type":"string"}
            },
            "required":["path"]
        }
    },
    {
        "name":"three_way_merge",
        "description":"Merge existing file with incoming content. Send diffs.",
        "parameters":{
            "type":"object",
            "properties":{
                "base_path":{"type":"string"},
                "incoming_content":{"type":"string"},
            },
            "required":["base_path","incoming_content"]
        }
    },
    {
        "name":"list_public_symbols",
        "description":"Return top‑level public functions/classes in a Python or Bash file",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{"type":"string"}
            },
            "required":["path"]
        }
    }
]

from ..agent.llm import call_llm_merge
from .file_ops import read_file, write_file


def three_way_merge(base_path:str, incoming_content:str) -> str:
    """
    base_path: existing file (relative)
    incoming_content: new version from agent/user
    strategy: 'llm' | 'simple'
    """
    original = read_file(base_path)
    merged = call_llm_merge(original, incoming_content)
    write_file(base_path, merged, overwrite=True)

    return "merged"

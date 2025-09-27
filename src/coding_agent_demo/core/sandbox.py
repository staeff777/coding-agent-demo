from pathlib import Path
from typing import Union

from ..config.settings import settings

ROOT = settings.workspace_root

def resolve_in_workspace(rel_or_abs: Union[str, Path]) -> Path:
    """
    Resolve path, ensure it resides inside the workspace root.
    Raises ValueError otherwise.
    """
    p = (ROOT / rel_or_abs).resolve() if not Path(rel_or_abs).is_absolute() \
        else Path(rel_or_abs).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError(f"Illegal path outside workspace: {p}")
    return p

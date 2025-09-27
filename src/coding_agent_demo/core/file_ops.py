import shutil
from pathlib import Path
from typing import List

from hurry.filesize import size

from .sandbox import resolve_in_workspace


def list_tree(relative_path: str = ".") -> str:
    """
    A slightly more elaborate method for transferring as much project information
    as possible to the model. LLMs understand graphical ASCII trees very well.
    """

    print(f"[listing tree: {relative_path}]")
    base = resolve_in_workspace(relative_path)

    def get_file_size(file_path: Path) -> str:
        try:
            file_size = file_path.stat().st_size
            return f"({size(file_size)})"
        except OSError:
            return ""

    def get_file_info(file_path: Path) -> str:
        """Get line count for text files or file size for binary files"""
        try:

            def blocks(files, size=65536):
                while True:
                    b = files.read(size)
                    if not b:
                        break
                    yield b

            # Try to read as text file and count lines
            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)

            line_size = size(line_count, system=lines)
            return f"({line_size})"

        except Exception:
            return get_file_size(file_path)


    def build_tree(path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """ Builds a directory tree """
        result = []
        if path == base:
            result.append("/")
        else:
            # Current item with tree characters
            connector = "└── " if is_last else "├── "
            if path.is_dir():
                name = path.name + "/"
                result.append(f"{prefix}{connector}{name}")
            else:
                name = path.name
                info = get_file_info(path)
                result.append(f"{prefix}{connector}{name} {info}")

        if path.is_dir():
            children = sorted([p for p in path.iterdir()],
                            key=lambda x: (not x.is_dir(), x.name.lower()))

            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                result.extend(build_tree(child, new_prefix, is_last_child))

        return result

    tree_list = build_tree(base)

    return "\n".join(tree_list)

def read_file(path: str) -> str:
    print(f"[reading file: {path}]")
    file = resolve_in_workspace(path)
    return file.read_text(encoding="utf-8")

def write_file(path: str, content: str, overwrite: bool = True) -> str:
    print(f"[writing file: {path}, overwrite={overwrite}]")
    file = resolve_in_workspace(path)
    if file.exists() and not overwrite:
        raise FileExistsError(f"{path} exists, overwrite = False")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")
    return "written"

def rename_file(old: str, new: str) -> str:
    print(f"[renaming file: {old} -> {new}]")
    old_p = resolve_in_workspace(old)
    new_p = resolve_in_workspace(new)
    old_p.rename(new_p)
    return "renamed"

def delete_path(path: str) -> str:
    print(f"[deleting path: {path}]")
    p = resolve_in_workspace(path)
    if p.is_dir():
        shutil.rmtree(p)
    else:
        p.unlink()
    return "deleted"


lines = [
        (1000 ** 2, 'ML'),
        (1000 ** 1, 'KL'),
        (1000 ** 0, 'L'),
        ]

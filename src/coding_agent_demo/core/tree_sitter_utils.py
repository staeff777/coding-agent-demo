
import tree_sitter_bash as tsbash
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

from .sandbox import resolve_in_workspace

# this example supports two languages, but it is easily extensible
SUPPORTED_LANGUAGES = {
    ".py": {
        "language": Language(tspython.language()),
        "name": "python"
    },
    ".sh": {
        "language": Language(tsbash.language()),
        "name": "bash"
    }
}


def list_public_symbols(path: str):
    """Extract public functions and classes from a supported file."""

    file_path = resolve_in_workspace(path)
    file_ext = file_path.suffix.lower()

    if file_ext not in SUPPORTED_LANGUAGES:
        return []

    lang_info = SUPPORTED_LANGUAGES[file_ext]
    parser = Parser(lang_info["language"])

    code = file_path.read_text(encoding="utf-8")
    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node
    symbols = []

    def extract_symbol_name(node):
        """Safely extract symbol name from a node."""
        name_node = node.child_by_field_name("name")
        if name_node is None:
            return None
        return code[name_node.start_byte:name_node.end_byte]

    def walk_tree(node, parent_class=None):
       """Extract symbols from any supported language file."""
       if node.type in ("function_definition", "class_definition"):
           name = extract_symbol_name(node)
           if name and not name.startswith("_"):
               symbol_info = {
                   "name": name,
                   "type": node.type.replace("_definition", ""),
                   "line": node.start_point[0] + 1
               }
               if parent_class:
                   symbol_info["class"] = parent_class
               symbols.append(symbol_info)

               # Recurse into class bodies (only relevant for languages with classes)
               if node.type == "class_definition":
                   for child in node.children:
                       walk_tree(child, name)
       else:
           for child in node.children:
               walk_tree(child, parent_class)

    walk_tree(root)

    return symbols


def walk_file_tree():
    """Walk the file tree and extract public symbols from all supported files."""
    root_path = resolve_in_workspace(".")
    file_symbols = {}

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_LANGUAGES:
            try:
                # Get relative path from root
                relative_path = file_path.relative_to(root_path)
                symbols = list_public_symbols(str(relative_path))
                if symbols:  # Only include files that have symbols
                    file_symbols[str(relative_path)] = symbols
            except Exception as e:
                # Skip files that can't be parsed
                print(f"Warning: Could not parse {relative_path}: {e}")
                continue

    return file_symbols

import ast
import pathlib

# root folder where project code lives
ROOT = pathlib.Path(__file__).parent.parent


def find_module_imports(file_path):
    """Return a set of module import strings found in a Python file."""
    tree = ast.parse(file_path.read_text())
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports


def all_imports_in_directory(directory):
    """Return a dict mapping each .py file to its import statements."""
    imports_map = {}
    for path in directory.rglob("*.py"):
        imports_map[path] = find_module_imports(path)
    return imports_map


def test_entities_layer_no_outer_dependencies():
    imports_map = all_imports_in_directory(ROOT / "l1_entities")

    forbidden_prefixes = (
        "l2_use_cases",
        "l3_interface_adapters",
        "l4_frameworks_and_drivers",
    )

    violations = []
    for file_path, imports in imports_map.items():
        for imp in imports:
            if any(imp.startswith(prefix) for prefix in forbidden_prefixes):
                violations.append(f"{file_path.relative_to(ROOT)} imports {imp}")

    assert not violations, f"Entities layer violation(s): {violations}"


def test_use_cases_do_not_import_frameworks():
    imports_map = all_imports_in_directory(ROOT / "l2_use_cases")

    forbidden_prefix = "l4_frameworks_and_drivers"

    violations = []
    for file_path, imports in imports_map.items():
        for imp in imports:
            if imp.startswith(forbidden_prefix):
                violations.append(f"{file_path.relative_to(ROOT)} imports {imp}")

    assert not violations, f"Use cases violation(s): {violations}"

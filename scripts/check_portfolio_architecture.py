#!/usr/bin/env python3
"""Advisory Project #24 architecture/preservation checker.

The contract is written as JSON, a valid subset of YAML 1.2, so this bootstrap
checker remains dependency-free. It intentionally avoids invasive runtime tests
for legacy/fork/hardware preservation repositories.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "ARCHITECTURE.yaml"
REQUIRED_TOP_LEVEL = {
    "schema_version", "repository", "preservation", "architecture",
    "source_layout", "limits", "libraries", "interfaces", "tests",
    "data", "governance", "exceptions",
}
REQUIRED_EXCEPTION_FIELDS = {
    "rule", "path", "reason", "owner", "risk", "accepted_ceiling", "refactoring_trigger",
}
REQUIRED_PRESERVATION_FIELDS = {
    "archival_notice", "supersession_notice", "revival_gates", "provenance",
    "license_warning", "security_warning", "private_data_warning",
}
IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".ruff_cache", ".mypy_cache", "build", "dist",
}
DEFAULT_METADATA = {"__init__.py", "README.md", "ARCHITECTURE.md", "ARCHITECTURE.yaml", "py.typed"}


def ignored_name(name: str) -> bool:
    return name in IGNORED_DIRS or name.endswith(".egg-info")


def ignored_path(path: Path) -> bool:
    return any(ignored_name(part) for part in path.parts)


def load_contract() -> dict[str, Any]:
    try:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {CONTRACT.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            "docs/ARCHITECTURE.yaml must remain JSON-compatible YAML 1.2 "
            f"for the dependency-free bootstrap checker: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError("architecture contract root must be an object")
    return payload


def exception_map(contract: dict[str, Any], errors: list[str]) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for index, item in enumerate(contract.get("exceptions", [])):
        if not isinstance(item, dict):
            errors.append(f"exceptions[{index}] must be an object")
            continue
        missing = REQUIRED_EXCEPTION_FIELDS - set(item)
        if missing:
            errors.append(f"exceptions[{index}] missing metadata: {sorted(missing)}")
            continue
        key = (str(item["rule"]), str(item["path"]))
        if key in result:
            errors.append(f"duplicate exception for {key[0]}:{key[1]}")
        result[key] = item
    return result


def require_exception(exceptions: dict[tuple[str, str], dict[str, Any]], rule: str, path: str, actual: int, errors: list[str]) -> None:
    item = exceptions.get((rule, path))
    if item is None:
        errors.append(f"{rule} violation at {path}: {actual}; no documented exception")
        return
    ceiling = item.get("accepted_ceiling")
    if not isinstance(ceiling, int):
        errors.append(f"{rule} exception at {path} must have integer accepted_ceiling")
    elif actual > ceiling:
        errors.append(f"{rule} no-growth ratchet exceeded at {path}: {actual}>{ceiling}")


class SourceDirectory(NamedTuple):
    path: Path
    child_names: tuple[str, ...]
    file_names: tuple[str, ...]
    runtime_file_count: int


def append_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def integer_limit(contract: dict[str, Any], key: str, errors: list[str]) -> int | None:
    limits = contract.get("limits")
    if not isinstance(limits, dict):
        append_error(errors, "limits must be an object")
        return None
    value = limits.get(key)
    if not isinstance(value, int):
        append_error(errors, f"limits.{key} must be an integer")
        return None
    return value


def physical_utf8_line_count(path: Path, errors: list[str]) -> int | None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"Python module is not UTF-8 text: {path.relative_to(ROOT)}")
        return None
    if text == "":
        return 0
    return text.count("\n") + 1


def runtime_file_count_under(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return int(path.suffix == ".py" and not ignored_path(path))
    if not path.is_dir():
        return 0
    count = 0
    for current, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not ignored_name(d) and not d.startswith(".")]
        count += sum(1 for filename in files if filename.endswith(".py"))
    return count


def validate_python_source_layout_exception(
    layout: dict[str, Any],
    exceptions: dict[tuple[str, str], dict[str, Any]],
    errors: list[str],
) -> None:
    if layout.get("python_rules_applicable", True):
        return
    matching_paths = sorted(path for rule, path in exceptions if rule == "python_source_layout")
    if not matching_paths:
        errors.append("python_source_layout is disabled but has no documented no-growth exception")
        return
    for rel in matching_paths:
        actual = runtime_file_count_under(ROOT / rel.rstrip("/"))
        require_exception(exceptions, "python_source_layout", rel, actual, errors)


def collect_source_root(source_root: Path, errors: list[str]) -> tuple[list[SourceDirectory], set[Path], dict[Path, int]]:
    directories: list[SourceDirectory] = []
    python_modules: list[Path] = []
    module_lines: dict[Path, int] = {}
    for current, dirs, files in os.walk(source_root):
        dirs[:] = sorted(d for d in dirs if not ignored_name(d) and not d.startswith("."))
        files = sorted(files)
        current_path = Path(current)
        runtime_files = [f for f in files if f.endswith(".py") and f != "__init__.py"]
        directories.append(SourceDirectory(current_path, tuple(dirs), tuple(files), len(runtime_files)))
        for filename in files:
            if not filename.endswith(".py"):
                continue
            module = current_path / filename
            python_modules.append(module)
            lines = physical_utf8_line_count(module, errors)
            if lines is not None:
                module_lines[module] = lines
    runtime_dirs: set[Path] = set()
    for module in python_modules:
        ancestor = module.parent
        while source_root in (ancestor, *ancestor.parents):
            runtime_dirs.add(ancestor)
            if ancestor == source_root:
                break
            ancestor = ancestor.parent
    return directories, runtime_dirs, module_lines


def validate_source(contract: dict[str, Any], exceptions: dict[tuple[str, str], dict[str, Any]], errors: list[str]) -> None:
    layout = contract["source_layout"]
    validate_python_source_layout_exception(layout, exceptions, errors)
    if not layout.get("python_rules_applicable", True):
        return
    max_entries = integer_limit(contract, "max_immediate_runtime_entries", errors)
    max_lines = integer_limit(contract, "max_python_module_lines", errors)
    if max_entries is None or max_lines is None:
        return
    allowed_non_python = set(layout.get("allowed_non_python_files", []))
    metadata = DEFAULT_METADATA | set(layout.get("metadata_names", []))
    roots = [ROOT / p for p in layout.get("python_source_roots", [])]
    for source_root in roots:
        rel_root = source_root.relative_to(ROOT).as_posix()
        if not source_root.is_dir():
            errors.append(f"declared Python source root is missing: {rel_root}")
            continue
        directories, runtime_dirs, module_lines = collect_source_root(source_root, errors)
        for source_dir in directories:
            rel_dir = source_dir.path.relative_to(ROOT).as_posix()
            runtime_child_count = sum(1 for d in source_dir.child_names if source_dir.path / d in runtime_dirs)
            count = runtime_child_count + source_dir.runtime_file_count
            if count > max_entries:
                require_exception(exceptions, "source_fanout", rel_dir, count, errors)
            for filename in source_dir.file_names:
                rel = (source_dir.path / filename).relative_to(ROOT).as_posix()
                if filename.endswith((".py", ".pyi")) or filename in metadata or rel in allowed_non_python:
                    continue
                require_exception(exceptions, "source_entry_type", rel, 1, errors)
        for module, lines in sorted(module_lines.items()):
            if lines > max_lines:
                require_exception(exceptions, "python_module_max_lines", module.relative_to(ROOT).as_posix(), lines, errors)


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - set(contract)
    if missing:
        errors.append(f"contract missing top-level keys: {sorted(missing)}")
        return errors
    exceptions = exception_map(contract, errors)
    repo = contract["repository"]
    for key in ("owner", "name", "profile", "status", "enforcement"):
        if not repo.get(key):
            errors.append(f"repository.{key} is required")
    if repo.get("profile") != "legacy":
        errors.append("repository.profile must remain legacy for Project #24 preservation repos")
    if str(repo.get("enforcement", "")).lower() != "advisory":
        errors.append("repository.enforcement must be Advisory unless the repo is formally revived")
    preservation = contract["preservation"]
    missing_preservation = REQUIRED_PRESERVATION_FIELDS - set(preservation)
    if missing_preservation:
        errors.append(f"preservation missing keys: {sorted(missing_preservation)}")
    for key in ("archival_notice", "supersession_notice", "license_warning", "security_warning", "private_data_warning"):
        if not str(preservation.get(key, "")).strip():
            errors.append(f"preservation.{key} must be non-empty")
    revival = preservation.get("revival_gates", [])
    if not isinstance(revival, list) or len(revival) < 3:
        errors.append("preservation.revival_gates must list at least three precise gates")
    readme = ROOT / "README.md"
    if not readme.is_file():
        errors.append("README.md is required for root preservation notice")
    else:
        text = readme.read_text(encoding="utf-8", errors="ignore")
        required_fragments = ["Project #24", "Preservation notice", "Revival gates"]
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"README.md missing preservation fragment: {fragment}")
    immediate_limit = integer_limit(contract, "max_immediate_runtime_entries", errors)
    module_limit = integer_limit(contract, "max_python_module_lines", errors)
    if immediate_limit is not None and immediate_limit != 10:
        errors.append("default max_immediate_runtime_entries must be 10; repo override belongs in an exception")
    if module_limit is not None and module_limit != 500:
        errors.append("default max_python_module_lines must be 500; repo override belongs in an exception")
    required_docs = contract["governance"].get("required_documents", [])
    for rel in required_docs:
        path = ROOT / rel
        if not path.is_file() or not path.read_text(encoding="utf-8", errors="ignore").strip():
            errors.append(f"required document missing or empty: {rel}")
    for suite in contract["tests"].get("required_suites", []):
        path = ROOT / "tests" / suite
        if not path.is_dir():
            errors.append(f"required test suite directory missing: tests/{suite}")
    ai = contract["interfaces"].get("ai", {})
    human = contract["interfaces"].get("human", {})
    if ai.get("context_file") != "AGENTS.md":
        errors.append("interfaces.ai.context_file must be AGENTS.md")
    if not ai.get("interaction") or not ai.get("capability_discovery"):
        errors.append("AI interaction and capability discovery decisions are required")
    if not human.get("interaction") or not human.get("dunder_policy"):
        errors.append("human interaction and dunder policy decisions are required")
    decisions = contract["libraries"].get("decisions", [])
    if not contract["libraries"].get("selection_policy") or len(decisions) < 2:
        errors.append("maintained-library selection policy and at least two decisions are required")
    validate_source(contract, exceptions, errors)
    return errors


def main() -> int:
    try:
        contract = load_contract()
        errors = validate_contract(contract)
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("portfolio architecture check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("portfolio architecture check passed (advisory legacy/preservation profile)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

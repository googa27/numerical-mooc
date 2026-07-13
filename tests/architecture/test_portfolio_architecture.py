from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = REPO_ROOT / "scripts" / "check_portfolio_architecture.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("portfolio_architecture_checker", CHECKER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_portfolio_architecture_contract(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER_PATH)],
        check=False,
        text=True,
        capture_output=True,
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_malformed_limits_fail_cleanly() -> None:
    checker = load_checker()
    contract = checker.load_contract()
    contract["limits"] = {"max_python_module_lines": 500}
    contract["source_layout"] = {
        **contract["source_layout"],
        "python_rules_applicable": True,
        "python_source_roots": ["scripts"],
    }

    errors = checker.validate_contract(contract)

    assert "limits.max_immediate_runtime_entries must be an integer" in errors


def test_disabled_python_layout_exception_is_enforced(tmp_path: Path, monkeypatch) -> None:
    checker = load_checker()
    monkeypatch.setattr(checker, "ROOT", tmp_path)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "added.py").write_text("pass\n", encoding="utf-8")
    errors: list[str] = []

    checker.validate_source(
        {
            "source_layout": {"python_rules_applicable": False},
            "limits": {"max_immediate_runtime_entries": 10, "max_python_module_lines": 500},
        },
        {
            ("python_source_layout", "src/"): {
                "rule": "python_source_layout",
                "path": "src/",
                "accepted_ceiling": 0,
            }
        },
        errors,
    )

    assert "python_source_layout no-growth ratchet exceeded at src/: 1>0" in errors


def test_physical_utf8_line_count_includes_trailing_line(tmp_path: Path, monkeypatch) -> None:
    checker = load_checker()
    monkeypatch.setattr(checker, "ROOT", tmp_path)
    source_root = tmp_path / "src"
    source_root.mkdir()
    module = source_root / "long.py"
    module.write_text("\n" * 500, encoding="utf-8")
    errors: list[str] = []

    checker.validate_source(
        {
            "source_layout": {"python_rules_applicable": True, "python_source_roots": ["src"]},
            "limits": {"max_immediate_runtime_entries": 10, "max_python_module_lines": 500},
        },
        {},
        errors,
    )

    assert "python_module_max_lines violation at src/long.py: 501; no documented exception" in errors

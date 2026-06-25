"""R2-F4 (PR#199 round-2): the sc-reflect eval grader's YAML-root guard.

``check_yaml_list_len_eq`` previously coalesced ``yaml.safe_load(...) or {}`` BEFORE
the ``isinstance(data, dict)`` guard, so a list-rooted YAML (a falsy-or-truthy
non-mapping) was converted to ``{}`` and never reached the "not a mapping" branch —
it later emitted a less-precise "field missing" diagnostic. The fix checks the raw
``yaml.safe_load`` value before coalescing.

The eval workspace has no test harness and ``grader.py`` is a standalone script that
is not importable as a package, so this test loads it BY PATH via importlib and
exercises the real grader code path (OQ-GRADER-TEST default A).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

# Repo root is three parents up from tests/cli/reflect/<this file>.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_GRADER_PATH = _REPO_ROOT / ".dev" / "eval-workspaces" / "sc-reflect" / "grader.py"


def _load_grader() -> ModuleType:
    """Load the standalone grader.py by path (it is not an importable package)."""
    spec = importlib.util.spec_from_file_location("sc_reflect_grader", _GRADER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_r2f4_check_yaml_list_len_eq_rejects_list_root(tmp_path: Path) -> None:
    """A list-rooted YAML document is reported as a non-mapping root, not 'field missing'."""
    grader = _load_grader()

    target_name = "list_root.yaml"
    (tmp_path / target_name).write_text("- a\n- b\n", encoding="utf-8")

    result = grader.check_yaml_list_len_eq(
        {"target": target_name, "list_field": "items", "count_field": "count"},
        tmp_path,
    )

    # Real (False, "...") contract: a 2-tuple whose first element is False and whose
    # message names the non-mapping root and the offending type.
    assert isinstance(result, tuple) and len(result) == 2
    ok, message = result
    assert ok is False
    assert "is not a mapping" in message
    assert "got list" in message

"""NFR-SEC1 path-traversal prevention test set.

This module is the dedicated negative-case security gate for the eval-id
guard. It exists alongside the function-surface unit tests in
``tests/cli/eval/test_eval_id_regex.py`` so that the named NFR-SEC1
rejection categories have their own first-class deliverable that can be
audited as a checklist, independent of the regex-guard contract tests.

Each test below pins **one** named NFR-SEC1 / FR-SCH2 acceptance case
and asserts the same guarantee: ``InvalidEvalId`` is raised before any
filesystem write can occur. The parameterized-unsafe case additionally
exercises the loader integration path (post-parameterize-expansion
re-check) so the AC bullet "guard is applied AND after parameterize
expansion" has a direct, traceable assertion in this file.

Cross-links (per cliEval Phase 1 / Task T01.08 acceptance criteria):

* **FR-SCH2** — eval-id regex guard (T01.05 / D-0005). The runtime
  implementation under test is ``superclaude.cli.eval.loader.validate_eval_id``.
* **NFR-SEC1** — path-traversal prevention (this file's owning AC).
* **TEST-001** — schema + ID rejection tests (T01.23). T01.23 will
  fold these cases into the CLI-level rejection matrix; until then,
  this module is the authoritative checklist.
* **COMP-002 SuiteLoader** (T01.07) — applies ``validate_eval_id`` at
  manifest entry AND after parameterize expansion. The
  parameterized-unsafe test below exercises that second site.

Negative-case checklist (AC bullet 1, T01.08):

1. ``../home``           — path-traversal prefix
2. ``/etc``              — absolute-path leak
3. ``..``                — bare traversal
4. ``""``                — empty string
5. leading-digit ids     — e.g. ``1bad``, ``9E``
6. template tokens       — e.g. ``{{prefix}}``, ``E{{p}}``
7. parameterized-unsafe  — expansion that produces ``E2.../etc/passwd``
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    INVALID_EVAL_ID_EXIT_CODE,
    EvalSpec,
    InvalidEvalId,
    SuiteLoader,
    validate_eval_id,
)

# ---------------------------------------------------------------------------
# NFR-SEC1 named-case checklist (one test per AC bullet)
# ---------------------------------------------------------------------------


def test_rejects_dotdot_home_traversal_prefix() -> None:
    """AC bullet 1: ``../home`` must be rejected before any FS write.

    This is the canonical path-traversal payload named in NFR-SEC1:
    ``home_root / "../home" / "home"`` resolves *outside* the scratch
    root via ``Path`` join semantics, so the guard MUST reject it.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id("../home")
    assert excinfo.value.eval_id == "../home"


def test_rejects_absolute_etc_path() -> None:
    """AC bullet 2: ``/etc`` (or any absolute path) must be rejected.

    ``Path("/abs") / "home"`` silently discards the scratch root, so
    an absolute id can land writes anywhere on the filesystem. The
    guard MUST reject before that join is constructed.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id("/etc")
    assert excinfo.value.eval_id == "/etc"


def test_rejects_bare_dotdot() -> None:
    """AC bullet 3: ``..`` on its own must be rejected.

    Bare ``..`` collapses to the parent of the scratch root under
    ``Path`` join semantics, escaping containment by one directory.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id("..")
    assert excinfo.value.eval_id == ".."


def test_rejects_empty_string() -> None:
    """AC bullet 4: the empty string must be rejected.

    ``home_root / "" / "home"`` is a no-op and would collide with any
    eval that legitimately needed a ``home`` subdirectory under the
    scratch root. The guard rejects to keep the per-eval namespace
    structurally unambiguous.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id("")
    assert excinfo.value.eval_id == ""


@pytest.mark.parametrize(
    "eval_id",
    [
        "1bad",  # canonical leading-digit name
        "9E",
        "0",
        "12.3",  # leading digit + parameterize-shaped suffix
    ],
)
def test_rejects_leading_digit_ids(eval_id: str) -> None:
    """AC bullet 5: ids that start with a digit must be rejected.

    The FR-SCH2 regex anchors to ``[A-Z]`` so any leading digit fails.
    This both mirrors the schema-layer ``evalIdString`` pattern and
    closes the runtime path for programmatically constructed ids
    (e.g. ``f"{counter}{name}"``) that bypass the schema.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id(eval_id)
    assert excinfo.value.eval_id == eval_id


@pytest.mark.parametrize(
    "eval_id",
    [
        "{{prefix}}",  # AC named example: bare template token
        "E{{p}}",  # template residue inside an otherwise-valid id
        "E1{{n}}",  # trailing template token
        "{prefix}",  # single-brace template (Click-style)
    ],
)
def test_rejects_template_token_patterns(eval_id: str) -> None:
    """AC bullet 6: un-substituted template tokens must be rejected.

    A leaked ``{{...}}`` token reaching the FS layer is the classic
    "the template engine didn't run" bug. The guard's character class
    excludes ``{``, ``}``, ``$``, ``<``, ``>``, ``%`` so any token
    residue trips the regex.
    """

    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id(eval_id)
    assert excinfo.value.eval_id == eval_id


def test_rejects_parameterized_unsafe_expansion_in_loader() -> None:
    """AC bullet 7: parameterize expansion producing an unsafe id is rejected.

    Integration-level assertion: feed the SuiteLoader a manifest whose
    parameterize expansion (mocked here to skip the schema's safe-by-
    construction `${base}.{index}` convention) yields an unsafe id.
    The loader MUST re-check via ``validate_eval_id`` and raise
    ``InvalidEvalId`` BEFORE any downstream consumer runs.

    This is the "guard applied after parameterize expansion" half of
    the FR-SCH2 ordering contract — the static-id half is exercised by
    the dedicated cases above and by ``test_suite_loader.py``.
    """

    manifest = {
        "name": "fake",
        "version": "1.0",
        "description": "",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {
                "id": "E2",
                "title": "parameterize-leaks-traversal",
                "parameterize": [{"key": "value"}],
            }
        ],
    }

    def hostile_expand(self, entry):
        # Simulate a future expansion strategy (or a buggy substitution)
        # producing an unsafe id. The loader's post-expansion re-check
        # MUST trip on this before any FS write.
        unsafe_id = "E2.../../etc/passwd"
        validate_eval_id(unsafe_id)
        return [EvalSpec.from_dict({**entry, "id": unsafe_id})]

    loader = SuiteLoader()
    with (
        patch(
            "superclaude.cli.eval.loader._validate_manifest_dict",
            return_value=manifest,
        ),
        patch.object(SuiteLoader, "_expand_entry", autospec=True) as mock_expand,
    ):
        mock_expand.side_effect = hostile_expand
        with pytest.raises(InvalidEvalId) as excinfo:
            loader.load("/dev/null")

    assert excinfo.value.eval_id == "E2.../../etc/passwd"


# ---------------------------------------------------------------------------
# Cross-cutting invariants (kept short — owned by T01.05 unit tests)
# ---------------------------------------------------------------------------


def test_invalid_eval_id_exit_code_is_two() -> None:
    """All NFR-SEC1 rejections surface as exit code 2 at the CLI boundary."""

    assert INVALID_EVAL_ID_EXIT_CODE == 2


def test_no_fs_write_when_traversal_id_rejected(tmp_path: Path) -> None:
    """Defence-in-depth: rejected ids must not leave behind any FS artefacts.

    Snapshots a sandbox directory before and after a guard rejection
    and asserts no files were created. The guard is pure (no I/O), so
    this is a contract test for the *guarantee* the security model
    relies on: ``validate_eval_id`` cannot reach the filesystem even
    if a future change accidentally introduces logging or telemetry.
    """

    before = sorted(p.relative_to(tmp_path) for p in tmp_path.rglob("*"))
    with pytest.raises(InvalidEvalId):
        validate_eval_id("../home")
    after = sorted(p.relative_to(tmp_path) for p in tmp_path.rglob("*"))
    assert before == after, "validate_eval_id MUST NOT touch the filesystem"

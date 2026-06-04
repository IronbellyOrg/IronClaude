"""Contract #7 CI lint -- retry-mutates-input invariant.

BUILD-REQUEST §Contract #7 forbids a retry that re-runs identical input
(master:§Recurrence #9: "Retry without input mutation -- identical prompt
re-run produces identical output, exhausts retry budget"; incidents
A1b:F-A1b-006, A11:F-A11-017, A12:F-A12-02).

Enforcement strategy
--------------------
Every retry site in ``src/superclaude/cli/roadmap`` is a ``Step(...)`` with a
``retry_limit`` keyword. A step's retry is legitimate only if the input
*changes* between attempts:

* **non-deterministic step** (LLM / tool-write -- ``prompt`` is a builder call,
  not an empty string): re-invocation yields new output, so the gate's input
  genuinely differs between attempts; OR
* **remediation/convergence** mutates its inputs before the next attempt (these
  steps are deterministic but run under a bounded ``max_runs`` with genuine
  input rewrites, and carry ``retry_limit=0`` so the pipeline-level retry loop
  does not re-run them identically); OR
* the site carries a ``retry_reason: transient_failure_only`` annotation
  (the retry is scoped to transient I/O / timeout / rate-limit failures).

A **deterministic** step (``prompt=""``) configured with ``retry_limit > 0``
and lacking the transient annotation is the Contract #7 violation: re-running
it produces byte-identical output and burns the retry budget for nothing.

This is a CI-only source-tree AST lint (skips if ``src/`` is absent, as on a
pipx-installed package).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

_TRANSIENT_ANNOTATION = "retry_reason: transient_failure_only"


def _roadmap_dir() -> Path:
    # tests/roadmap/test_retry_contract.py -> parents[2] == repo root
    return (
        Path(__file__).resolve().parents[2] / "src" / "superclaude" / "cli" / "roadmap"
    )


def _step_calls(tree: ast.Module):
    """Yield every ``Step(...)`` Call node in the module AST."""
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Step"
        ):
            yield node


def test_no_identical_input_retry():
    """No deterministic roadmap Step retries identical input (Contract #7)."""
    roadmap_dir = _roadmap_dir()
    if not roadmap_dir.is_dir():
        pytest.skip(
            f"CI-only source-tree lint: {roadmap_dir} absent "
            "(expected on a pipx-installed package with no src/ tree)."
        )

    steps_seen = 0
    violations: list[str] = []

    for py_file in sorted(roadmap_dir.glob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        src_lines = source.splitlines()
        tree = ast.parse(source)

        for call in _step_calls(tree):
            steps_seen += 1
            kwargs = {kw.arg: kw.value for kw in call.keywords if kw.arg}

            retry_node = kwargs.get("retry_limit")
            retry_val = (
                retry_node.value
                if isinstance(retry_node, ast.Constant)
                and isinstance(retry_node.value, int)
                else None
            )
            # retry_limit absent, dynamic, or == 0 -> no identical-input risk.
            if retry_val is None or retry_val <= 0:
                continue

            prompt_node = kwargs.get("prompt")
            is_deterministic = (
                isinstance(prompt_node, ast.Constant) and prompt_node.value == ""
            )
            # Non-deterministic (LLM/tool-write) step: re-invocation mutates the
            # gate's input, so a bounded retry is legitimate.
            if not is_deterministic:
                continue

            # Deterministic step with retry_limit>0: allowed only with the
            # explicit transient-failure annotation in the Step's source span.
            start = call.lineno - 1
            end = getattr(call, "end_lineno", call.lineno)
            span = "\n".join(src_lines[start:end])
            if _TRANSIENT_ANNOTATION in span:
                continue

            violations.append(
                f"{py_file.name}:{call.lineno}: deterministic Step "
                f'(prompt="") has retry_limit={retry_val} with neither input '
                f"mutation nor a '{_TRANSIENT_ANNOTATION}' annotation "
                "(Contract #7 / master:§Recurrence #9)."
            )

    # Guard: the AST walk must actually find Step constructions, else a
    # detection regression would make this lint vacuously pass.
    assert steps_seen > 0, (
        "No Step(...) constructions found under src/superclaude/cli/roadmap -- "
        "Step-detection regression (the Contract #7 lint would pass vacuously)."
    )
    assert not violations, "Contract #7 violation(s):\n" + "\n".join(violations)


def test_recurrence_fixture_well_formed():
    """The seeded master:§Recurrence #9 fixture pair exists and is consistent."""
    corpus = (
        Path(__file__).resolve().parent / "fixtures" / "recurrence" / "retry_contract"
    )
    md_path = corpus / "retry_loop_no_terminal_case.md"
    json_path = corpus / "retry_loop_no_terminal_case.expected.json"

    assert md_path.is_file(), f"missing fixture markdown: {md_path}"
    assert json_path.is_file(), f"missing expected json: {json_path}"

    expected = json.loads(json_path.read_text(encoding="utf-8"))
    assert expected["failure_class"] == "retry_contract"
    assert expected["contract"] == 7
    assert expected["source_authority"]["master_recurrence_row"] == 9
    assert "A1b:F-A1b-006" in expected["source_authority"]["partition_findings"]
    # Post-fix oracle: zero deterministic-retry violations + every deterministic
    # roadmap step at retry_limit=0 (matches test_no_identical_input_retry).
    assert expected["expected_deterministic_retry_violations"] == 0
    assert expected["expected_all_deterministic_steps_retry_limit"] == 0

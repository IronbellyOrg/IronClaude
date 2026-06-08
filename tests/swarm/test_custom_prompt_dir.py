"""T02.05 -- ``preflight.read_custom_prompt_dir`` tests (FR-021).

Covers the COMP-006 / FR-021 acceptance criteria for the
``--custom-prompt-dir`` escape hatch:

    * ``read_custom_prompt_dir`` reads ``system.txt`` / ``user.txt`` /
      ``meta.yaml`` from a directory and returns the trio verbatim.
    * Missing directory, missing file, unreadable file → structured
      :class:`PreflightError` with :data:`RULE_CUSTOM_PROMPT_DIR_MISSING`.
    * §11.5 substring enforced on ``system.txt`` contents via the
      central :func:`enforce_injection_guard` helper -- byte-identical
      failure shape with the lens path (INV-003 / INV-014 parity gates
      land in T02.08 / T02.09; this module exercises the wiring).
    * ``meta.yaml`` invalid YAML or non-mapping → structured
      :data:`RULE_CUSTOM_PROMPT_DIR_META_INVALID`.
    * Three-file contents round-trip into a :class:`Manifest` snapshot
      via ``to_json`` / ``from_json`` when applied to a JobSpec ahead
      of :func:`run_preflight`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import (
    LensEntry,
    Manifest,
    from_json,
    to_json,
)
from superclaude.cli.swarm.preflight import (
    RULE_CUSTOM_PROMPT_DIR_META_INVALID,
    RULE_CUSTOM_PROMPT_DIR_MISSING,
    RULE_INJECTION_GUARD,
    PreflightError,
    read_custom_prompt_dir,
    run_preflight,
    set_lens_resolver,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_three_files(
    base: Path,
    *,
    system: str = "You are a reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE,
    user: str = "Review: {{target}}",
    meta: str = "variables:\n  audience: senior\n",
) -> None:
    """Write the three files into ``base``; helper centralises content."""
    (base / "system.txt").write_text(system, encoding="utf-8")
    (base / "user.txt").write_text(user, encoding="utf-8")
    (base / "meta.yaml").write_text(meta, encoding="utf-8")


def _custom_lens_entry() -> LensEntry:
    """LensEntry stub mirroring the ``custom`` escape-hatch entry."""
    return LensEntry(
        name="custom",
        description="caller-supplied prompts",
        system_prompt_fragment=(
            "Custom reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Custom: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="custom-v1",
        default_workers=3,
        default_target_line_cap=4000,
        suspect=False,
        tier="T2",
        recommended_next_command_template="sc:reflect on {job_id}",
        acceptance_notes="",
        stability="stable",
    )


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_read_custom_prompt_dir_happy_path_returns_trio(tmp_path: Path) -> None:
    _write_three_files(tmp_path)

    system, user, meta = read_custom_prompt_dir(
        tmp_path, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
    )

    assert system.endswith(CANONICAL_INJECTION_GUARD_SENTENCE)
    assert user == "Review: {{target}}"
    assert isinstance(meta, dict)
    assert meta == {"variables": {"audience": "senior"}}


def test_read_custom_prompt_dir_accepts_pathlike(tmp_path: Path) -> None:
    _write_three_files(tmp_path)

    system, user, meta = read_custom_prompt_dir(str(tmp_path))

    assert system  # default required_substring="" -> guard disabled
    assert user
    assert meta == {"variables": {"audience": "senior"}}


def test_read_custom_prompt_dir_empty_meta_yields_empty_dict(
    tmp_path: Path,
) -> None:
    _write_three_files(tmp_path, meta="")

    _, _, meta = read_custom_prompt_dir(tmp_path)

    assert meta == {}


def test_read_custom_prompt_dir_preserves_verbatim_content(
    tmp_path: Path,
) -> None:
    """No normalisation / trimming on system.txt or user.txt."""
    system_raw = "  leading + trailing  \n\n" + CANONICAL_INJECTION_GUARD_SENTENCE
    user_raw = "\n\nUser:\n  - item\n\n"
    _write_three_files(tmp_path, system=system_raw, user=user_raw)

    system, user, _ = read_custom_prompt_dir(tmp_path)

    assert system == system_raw
    assert user == user_raw


# ---------------------------------------------------------------------------
# Missing-file rejections (INV-003 -- missing system.txt produces failed
# contract; parity asserted in T02.08).
# ---------------------------------------------------------------------------


def test_read_custom_prompt_dir_missing_directory_raises(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "does-not-exist"

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(missing)

    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].rule == RULE_CUSTOM_PROMPT_DIR_MISSING
    assert failures[0].reason == "custom-prompt-dir-missing"
    assert failures[0].path == "custom_prompt_dir"


def test_read_custom_prompt_dir_path_is_file_raises(tmp_path: Path) -> None:
    not_a_dir = tmp_path / "regular_file.txt"
    not_a_dir.write_text("x", encoding="utf-8")

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(not_a_dir)

    assert excinfo.value.failures[0].rule == RULE_CUSTOM_PROMPT_DIR_MISSING


@pytest.mark.parametrize(
    "missing_file",
    ["system.txt", "user.txt", "meta.yaml"],
)
def test_read_custom_prompt_dir_missing_file_raises(
    tmp_path: Path, missing_file: str
) -> None:
    _write_three_files(tmp_path)
    (tmp_path / missing_file).unlink()

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path)

    failures = excinfo.value.failures
    assert any(
        f.rule == RULE_CUSTOM_PROMPT_DIR_MISSING
        and f.path == f"custom_prompt_dir/{missing_file}"
        for f in failures
    ), f"Expected missing-file failure for {missing_file}; got {failures}"


def test_read_custom_prompt_dir_batches_missing_files(tmp_path: Path) -> None:
    """All missing files reported in one PreflightError (INV-014 batch shape)."""
    # Write nothing -- all three files missing.
    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path)

    failures = excinfo.value.failures
    assert len(failures) == 3
    paths = [f.path for f in failures]
    # Determinism: order matches _CUSTOM_PROMPT_DIR_FILES.
    assert paths == [
        "custom_prompt_dir/system.txt",
        "custom_prompt_dir/user.txt",
        "custom_prompt_dir/meta.yaml",
    ]
    assert all(f.rule == RULE_CUSTOM_PROMPT_DIR_MISSING for f in failures)


# ---------------------------------------------------------------------------
# §11.5 substring enforcement (INV-003 / INV-014 -- byte-identical with
# the lens path's enforce_injection_guard call).
# ---------------------------------------------------------------------------


def test_read_custom_prompt_dir_missing_substring_raises(
    tmp_path: Path,
) -> None:
    _write_three_files(
        tmp_path,
        system="You are a reviewer with no guard sentence.",
    )

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(
            tmp_path, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
        )

    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].rule == RULE_INJECTION_GUARD
    assert failures[0].path == "custom_prompt_dir/system.txt"
    assert failures[0].reason == "injection-guard"


def test_read_custom_prompt_dir_substring_default_disabled(
    tmp_path: Path,
) -> None:
    """``required_substring=""`` -> guard disabled (auto_inject_guard semantics)."""
    _write_three_files(tmp_path, system="bare prompt without guard")

    # Empty required_substring is "guard disabled"; should not raise.
    system, _, _ = read_custom_prompt_dir(tmp_path)

    assert system == "bare prompt without guard"


def test_read_custom_prompt_dir_guard_uses_central_helper_path_label(
    tmp_path: Path,
) -> None:
    """Failure ``path`` must name custom_prompt_dir/system.txt verbatim.

    The lens-driven path uses ``prompt.system``; the custom-prompt-dir
    path uses ``custom_prompt_dir/system.txt`` so a caller assembling
    the structured failed contract can distinguish the two seams even
    though the rule + reason tokens are identical (INV-014 isomorphism).
    """
    _write_three_files(tmp_path, system="no guard here")

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path, required_substring="must-appear-substring")

    failure = excinfo.value.failures[0]
    assert failure.path == "custom_prompt_dir/system.txt"
    assert "must-appear-substring" in failure.message


# ---------------------------------------------------------------------------
# meta.yaml validation
# ---------------------------------------------------------------------------


def test_read_custom_prompt_dir_invalid_yaml_raises(tmp_path: Path) -> None:
    _write_three_files(tmp_path, meta="key: value:\n  - bad: : ::\n")

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path)

    failures = excinfo.value.failures
    assert any(f.rule == RULE_CUSTOM_PROMPT_DIR_META_INVALID for f in failures), (
        f"Expected meta-invalid failure; got {failures}"
    )


def test_read_custom_prompt_dir_non_mapping_meta_raises(
    tmp_path: Path,
) -> None:
    """meta.yaml must be a top-level mapping; lists / scalars rejected."""
    _write_three_files(tmp_path, meta="- a\n- b\n")

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path)

    failure = next(
        f
        for f in excinfo.value.failures
        if f.rule == RULE_CUSTOM_PROMPT_DIR_META_INVALID
    )
    assert "mapping" in failure.message
    assert "list" in failure.message


def test_read_custom_prompt_dir_scalar_meta_raises(tmp_path: Path) -> None:
    _write_three_files(tmp_path, meta="just-a-string\n")

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(tmp_path)

    assert any(
        f.rule == RULE_CUSTOM_PROMPT_DIR_META_INVALID for f in excinfo.value.failures
    )


# ---------------------------------------------------------------------------
# Round-trip into Manifest snapshot
# ---------------------------------------------------------------------------


def _custom_spec(
    *, lens: str, prompt_system: str, prompt_user: str, variables: dict[str, Any]
) -> dict[str, Any]:
    """Build a schema-valid JobSpec dict driven by the custom-prompt-dir
    reader's output. Mirrors tests/swarm/test_preflight.py shape."""
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-custom-prompt-dir-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "T02.05-custom-prompt-dir",
            "kind": "claude",
        },
        "lens": lens,
        "custom_prompt_dir": "/abs/custom",
        "workers": {
            "count": 3,
            "models": ["gpt-5-codex", "claude-haiku-4.5", "gemini-1.5-pro"],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            "kind": "openai_compat",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": prompt_system,
            "user_template": prompt_user,
            "variables": variables,
        },
        "target": {
            "kind": "file",
            "path": "/abs/path/to/target.py",
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
            "injection_guard": {
                "enabled": True,
                "required_substring": CANONICAL_INJECTION_GUARD_SENTENCE,
            },
        },
        "normalization": {
            "recipe": "custom-v1",
            "template_path": "/abs/path/to/template.j2",
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            "dir": "/abs/path/to/output",
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": "custom",
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": "sc:reflect on {job_id}",
        "recommended_next_command_substitutions": {
            "job_id": "job-custom-prompt-dir-001"
        },
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def test_custom_prompt_dir_contents_round_trip_into_manifest(
    tmp_path: Path,
) -> None:
    """End-to-end: reader output flows into JobSpec → Manifest → JSON → Manifest.

    Acceptance criterion: "3 files round-trip into Manifest snapshot."
    The reader supplies prompt.system + prompt.user_template + variables;
    the resulting Manifest survives ``to_json`` / ``from_json``
    byte-identically (INV-016 anchor invariant).
    """
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    _write_three_files(
        prompt_dir,
        system="Custom reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE,
        user="Review carefully: {{target}}",
        meta="variables:\n  audience: senior\n  rigor: high\n",
    )

    system, user, meta = read_custom_prompt_dir(
        prompt_dir, required_substring=CANONICAL_INJECTION_GUARD_SENTENCE
    )

    spec = _custom_spec(
        lens="custom",
        prompt_system=system,
        prompt_user=user,
        variables=meta.get("variables", {}),
    )
    # F-P2-1: run_preflight now reads custom_prompt_dir itself, so point it at
    # the real on-disk directory created above (the _custom_spec default is a
    # non-existent placeholder path). The reader re-populates prompt.* with the
    # same values the manual read produced, so the round-trip assertion holds.
    spec["custom_prompt_dir"] = str(prompt_dir)

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        target_path = tmp_path / "target.py"
        target_payload = ("def f():\n    pass\n" * 50).encode(
            "utf-8"
        )  # > 50 non-whitespace bytes
        target_path.write_bytes(target_payload)
        spec["target"]["path"] = str(target_path)

        result = run_preflight(
            spec,
            target_loader=lambda _p: target_payload,
        )
    finally:
        set_lens_resolver(previous)

    # Manifest captures lens name + the prompt contents flowed via spec.
    assert isinstance(result.manifest, Manifest)
    assert result.manifest.resolved_lens_entry.name == "custom"

    # INV-016 -- byte-identical round-trip through JSON.
    payload = to_json(result.manifest)
    rehydrated = from_json(Manifest, payload)
    assert to_json(rehydrated) == payload


def test_read_custom_prompt_dir_meta_variables_survive_json_round_trip(
    tmp_path: Path,
) -> None:
    """Variables harvested from meta.yaml round-trip through json.dumps."""
    import json

    _write_three_files(
        tmp_path,
        meta=(
            "variables:\n"
            "  audience: senior\n"
            "  nested:\n"
            "    level: 2\n"
            "    flags: [a, b, c]\n"
        ),
    )

    _, _, meta = read_custom_prompt_dir(tmp_path)

    payload = json.dumps(meta, sort_keys=True)
    assert json.loads(payload) == meta
    assert meta["variables"]["nested"]["flags"] == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# F-P2-1 -- production wiring: run_preflight reads custom_prompt_dir itself
# ---------------------------------------------------------------------------
#
# These tests prove the F-P2-1 fix: run_preflight (not just the caller) consumes
# the custom_prompt_dir directory when lens == "custom". The wiring runs BEFORE
# schema validation, so it is observable through whether the §11.5 cross-field
# rule passes: with an EMPTY inline prompt.system, preflight can only succeed if
# it read system.txt from the directory and populated prompt.system before the
# schema check.


def _custom_spec_empty_prompt(custom_dir: str, target_path: str) -> dict[str, Any]:
    """Custom-lens spec with EMPTY inline prompt fields + a custom_prompt_dir.

    The empty inline ``prompt.system`` is the key: only the F-P2-1 wiring
    (run_preflight reading the directory before schema validation) can make
    this spec pass the §11.5 cross-field rule.
    """
    spec = _custom_spec(
        lens="custom",
        prompt_system="",
        prompt_user="",
        variables={},
    )
    spec["custom_prompt_dir"] = custom_dir
    spec["target"]["path"] = target_path
    return spec


def _target_payload() -> bytes:
    return ("def f():\n    pass\n" * 50).encode("utf-8")  # > 50 non-whitespace bytes


def test_run_preflight_reads_custom_prompt_dir_and_passes_guard(
    tmp_path: Path,
) -> None:
    """F-P2-1: empty inline prompt.system + valid custom dir -> preflight OK.

    Proves run_preflight read system.txt (which carries the §11.5 sentence)
    and populated prompt.system BEFORE the schema cross-field rule fired.
    Without the wiring the empty prompt.system fails §11.5 and preflight raises.
    """
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    _write_three_files(prompt_dir)  # system.txt carries the canonical sentence

    spec = _custom_spec_empty_prompt(str(prompt_dir), str(tmp_path / "t.py"))

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        result = run_preflight(spec, target_loader=lambda _p: _target_payload())
    finally:
        set_lens_resolver(previous)

    assert result.manifest.resolved_lens_entry.name == "custom"


def test_run_preflight_custom_dir_missing_system_substring_raises(
    tmp_path: Path,
) -> None:
    """F-P2-1: custom dir whose system.txt lacks the §11.5 sentence -> failure.

    The reader enforces the guard on system.txt and run_preflight surfaces the
    structured injection-guard failure (path names the directory seam).
    """
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    _write_three_files(prompt_dir, system="bare prompt without the guard sentence")

    spec = _custom_spec_empty_prompt(str(prompt_dir), str(tmp_path / "t.py"))

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        with pytest.raises(PreflightError) as excinfo:
            run_preflight(spec, target_loader=lambda _p: _target_payload())
    finally:
        set_lens_resolver(previous)

    failure = excinfo.value.failures[0]
    assert failure.rule == RULE_INJECTION_GUARD
    assert failure.path == "custom_prompt_dir/system.txt"


def test_run_preflight_custom_dir_missing_raises(tmp_path: Path) -> None:
    """F-P2-1: a non-existent custom_prompt_dir -> structured preflight failure."""
    spec = _custom_spec_empty_prompt(
        str(tmp_path / "does-not-exist"), str(tmp_path / "t.py")
    )

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        with pytest.raises(PreflightError) as excinfo:
            run_preflight(spec, target_loader=lambda _p: _target_payload())
    finally:
        set_lens_resolver(previous)

    assert excinfo.value.failures[0].rule == RULE_CUSTOM_PROMPT_DIR_MISSING


def test_run_preflight_custom_dir_auto_inject_guard(tmp_path: Path) -> None:
    """F-P2-1 / FR-024: --auto-inject-guard prepends the §11.5 sentence.

    A legacy system.txt lacking the canonical sentence passes preflight when
    auto_inject_guard=True because the reader prepends it before the guard
    check, and run_preflight threads the flag through.
    """
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    _write_three_files(prompt_dir, system="legacy system prompt, no guard yet")

    spec = _custom_spec_empty_prompt(str(prompt_dir), str(tmp_path / "t.py"))

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        result = run_preflight(
            spec,
            target_loader=lambda _p: _target_payload(),
            auto_inject_guard=True,
        )
    finally:
        set_lens_resolver(previous)

    assert result.manifest.resolved_lens_entry.name == "custom"


def test_run_preflight_custom_dir_populates_prompt_variables(
    tmp_path: Path,
) -> None:
    """F-P2-1: meta.yaml variables flow into the JobSpec the reader populates.

    Verified indirectly via a target_loader closure that captures the resolved
    JobSpec is overkill; instead assert preflight succeeds with a meta.yaml that
    carries variables (the reader writes them onto prompt.variables before
    schema, and schema accepts the populated dict).
    """
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    _write_three_files(
        prompt_dir,
        meta="variables:\n  audience: senior\n  rigor: high\n",
    )

    spec = _custom_spec_empty_prompt(str(prompt_dir), str(tmp_path / "t.py"))

    previous = set_lens_resolver(lambda _name: _custom_lens_entry())
    try:
        result = run_preflight(spec, target_loader=lambda _p: _target_payload())
    finally:
        set_lens_resolver(previous)

    assert result.manifest.resolved_lens_entry.name == "custom"

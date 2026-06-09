"""Tests for the ``prd run --spec FILE`` deterministic spec-ingestion feature.

Covers acceptance criteria 1-8 from ``docs/designs/prd-spec-flag.md`` (Phase 1,
paths-only binding):

  1. CLI parse     -- repeatable, file-validated, surfaced in --help.
  2. Config        -- resolve_config(spec=...) → PrdConfig.spec_files (absolute);
                      empty when omitted.
  3. Model         -- PrdConfig.spec_files defaults to [].
  4. Binding       -- _bind_specs adds SPECS array + prepends spec parent dirs
                      into WHERE; idempotent; no-op when no specs.
  5. Prompt inject -- scope-discovery contains the AUTHORITATIVE-SPECS block +
                      exact paths when SPECS present; byte-identical to today
                      when absent (backward-compat lock).
  6. Gate          -- scope-discovery gate unchanged (min_lines=50, STANDARD);
                      WARN emitted when SPECS present and the gate fails.
  7. Backward compat -- empty/absent SPECS ⇒ no SPECS key, no prompt delta.
  8. Resume        -- a persisted parsed-request.json carrying SPECS re-injects
                      the block without --spec on the resume config.
"""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.prd.commands import prd_group
from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import PrdExecutor
from superclaude.cli.prd.gates import GATE_CRITERIA
from superclaude.cli.prd.models import PrdConfig
from superclaude.cli.prd.process import PrdClaudeProcess
from superclaude.cli.prd.prompts import (
    _TRUNCATION_MARKER,
    _authoritative_specs_block,
    _render_investigation_prompt,
    build_investigation_prompt,
    build_scope_discovery_prompt,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PARSED_BASE = {
    "GOAL": "Test goal",
    "PRODUCT_NAME": "TestProduct",
    "PRODUCT_SLUG": "test-product",
    "PRD_SCOPE": "feature",
    "SCENARIO": "A",
    "WHERE": ["src/"],
    "WHY": "testing",
    "TIER_RECOMMENDATION": "standard",
}


def _write_parsed(task_dir: Path, parsed: dict) -> None:
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "parsed-request.json").write_text(json.dumps(parsed), encoding="utf-8")


def _scope_config(task_dir: Path) -> PrdConfig:
    """A PrdConfig sufficient for build_scope_discovery_prompt."""
    return PrdConfig(
        user_message="Create a PRD for TestProduct",
        product_name="TestProduct",
        product_slug="test-product",
        tier="standard",
        task_dir=task_dir,
    )


# ===========================================================================
# 1. CLI parse (test_cli_smoke surface)
# ===========================================================================


class TestSpecCliParse:
    def test_help_lists_spec_option(self) -> None:
        result = CliRunner().invoke(prd_group, ["run", "--help"])
        assert result.exit_code == 0
        assert "--spec" in result.output

    def test_repeated_spec_accepted(self, tmp_path: Path) -> None:
        a = tmp_path / "a.md"
        b = tmp_path / "b.md"
        a.write_text("# A\n", encoding="utf-8")
        b.write_text("# B\n", encoding="utf-8")
        result = CliRunner().invoke(
            prd_group,
            ["run", "build a thing", "--spec", str(a), "--spec", str(b), "--dry-run"],
        )
        assert result.exit_code == 0, result.output

    def test_directory_rejected(self, tmp_path: Path) -> None:
        d = tmp_path / "a_dir"
        d.mkdir()
        result = CliRunner().invoke(
            prd_group, ["run", "x", "--spec", str(d), "--dry-run"]
        )
        assert result.exit_code != 0
        # Click's Path(dir_okay=False) error text mentions it is a directory/file.
        assert "directory" in result.output.lower() or "file" in result.output.lower()

    def test_nonexistent_rejected(self, tmp_path: Path) -> None:
        missing = tmp_path / "nope.md"
        result = CliRunner().invoke(
            prd_group, ["run", "x", "--spec", str(missing), "--dry-run"]
        )
        assert result.exit_code != 0
        assert "exist" in result.output.lower() or "does not" in result.output.lower()


# ===========================================================================
# 2. Config resolution (test_config surface)
# ===========================================================================


class TestSpecConfigResolution:
    def test_spec_files_populated_absolute(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".dev").mkdir()
        spec = tmp_path / "SPEC.md"
        spec.write_text("# spec\n", encoding="utf-8")

        # Pass a relative path; resolve_config must absolutise it.
        cfg = resolve_config("req", product="p", spec=("SPEC.md",))

        assert cfg.spec_files == [str(spec.resolve())]
        assert Path(cfg.spec_files[0]).is_absolute()

    def test_spec_files_empty_when_omitted(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".dev").mkdir()
        cfg = resolve_config("req", product="p")
        assert cfg.spec_files == []


# ===========================================================================
# 3. Model default (test_models surface)
# ===========================================================================


class TestSpecModelDefault:
    def test_spec_files_defaults_empty(self) -> None:
        assert PrdConfig().spec_files == []

    def test_spec_files_is_independent_per_instance(self) -> None:
        a = PrdConfig()
        a.spec_files.append("/x")
        b = PrdConfig()
        assert b.spec_files == []  # default_factory, not shared mutable


# ===========================================================================
# 4. Binding (_bind_specs) (test_executor surface)
# ===========================================================================


def _executor_with_specs(tmp_path: Path, spec_files: list[str]) -> PrdExecutor:
    cfg = resolve_config("req", product="bind-test", dry_run=True)
    cfg.task_dir = tmp_path / "prd-bind-test"
    cfg.spec_files = spec_files
    return PrdExecutor(cfg)


class TestBindSpecs:
    def test_adds_specs_array_and_prepends_where(self, tmp_path: Path) -> None:
        spec = tmp_path / "SPEC.md"
        spec.write_text("x" * 123, encoding="utf-8")
        ex = _executor_with_specs(tmp_path, [str(spec)])

        out = ex._bind_specs({"WHERE": ["src/"]})

        assert "SPECS" in out
        assert len(out["SPECS"]) == 1
        entry = out["SPECS"][0]
        assert entry == {
            "path": str(spec),
            "size": 123,
            "inlined": False,
            "truncated": False,
        }
        # spec parent dir prepended before existing WHERE entries.
        assert out["WHERE"][0] == str(spec.parent)
        assert "src/" in out["WHERE"]
        assert out["WHERE"].index(str(spec.parent)) < out["WHERE"].index("src/")

    def test_idempotent(self, tmp_path: Path) -> None:
        spec = tmp_path / "SPEC.md"
        spec.write_text("data", encoding="utf-8")
        ex = _executor_with_specs(tmp_path, [str(spec)])

        once = ex._bind_specs({"WHERE": ["src/"]})
        twice = ex._bind_specs(json.loads(json.dumps(once)))

        assert twice["SPECS"] == once["SPECS"]
        assert twice["WHERE"] == once["WHERE"]  # parent dir not duplicated

    def test_noop_when_no_specs(self, tmp_path: Path) -> None:
        ex = _executor_with_specs(tmp_path, [])
        parsed = {"WHERE": ["src/"], "GOAL": "g"}
        out = ex._bind_specs(parsed)
        assert "SPECS" not in out
        assert out["WHERE"] == ["src/"]

    def test_missing_file_size_zero(self, tmp_path: Path) -> None:
        missing = tmp_path / "gone.md"  # never created
        ex = _executor_with_specs(tmp_path, [str(missing)])
        out = ex._bind_specs({"WHERE": []})
        assert out["SPECS"][0]["size"] == 0

    def test_persist_bound_specs_roundtrip(self, tmp_path: Path) -> None:
        spec = tmp_path / "SPEC.md"
        spec.write_text("hello", encoding="utf-8")
        ex = _executor_with_specs(tmp_path, [str(spec)])
        _write_parsed(ex._config.task_dir, dict(_PARSED_BASE))

        ex._persist_bound_specs()

        reloaded = json.loads(
            (ex._config.task_dir / "parsed-request.json").read_text(encoding="utf-8")
        )
        assert reloaded["SPECS"][0]["path"] == str(spec)
        assert reloaded["WHERE"][0] == str(spec.parent)

    def test_dedup_duplicate_spec_values(self, tmp_path: Path) -> None:
        """Two identical ``--spec`` values must collapse to exactly one SPECS
        entry and a single idempotent WHERE parent dir (review comment
        r3367342586). Pre-fix, the duplicate path produced two SPECS entries."""
        spec = tmp_path / "foo.md"
        spec.write_text("data", encoding="utf-8")
        ex = _executor_with_specs(tmp_path, [str(spec), str(spec)])

        out = ex._bind_specs({"WHERE": ["src/"]})

        # Exactly one SPECS entry despite the duplicate --spec value.
        assert len(out["SPECS"]) == 1
        assert out["SPECS"][0]["path"] == str(spec)
        # WHERE parent dir is idempotent: the spec's parent appears exactly once.
        assert out["WHERE"].count(str(spec.parent)) == 1


# ===========================================================================
# 5. Prompt injection + byte-identical lock (test_prompts surface)
# ===========================================================================


class TestScopeDiscoverySpecInjection:
    def test_block_present_with_exact_paths(self, tmp_path: Path) -> None:
        task_dir = tmp_path / "prd-test-product"
        parsed = dict(_PARSED_BASE)
        parsed["SPECS"] = [
            {"path": "/abs/SPEC_A.md", "size": 1, "inlined": False, "truncated": False},
            {"path": "/abs/SPEC_B.md", "size": 2, "inlined": False, "truncated": False},
        ]
        _write_parsed(task_dir, parsed)

        prompt = build_scope_discovery_prompt(_scope_config(task_dir))

        assert "AUTHORITATIVE SPECIFICATIONS" in prompt
        assert "/abs/SPEC_A.md" in prompt
        assert "/abs/SPEC_B.md" in prompt
        assert "MUST Read each one IN FULL" in prompt

    def test_no_specs_is_byte_identical(self, tmp_path: Path) -> None:
        """The ONLY delta between with-spec and no-spec prompts is the block."""
        no_spec_dir = tmp_path / "prd-nospec"
        empty_dir = tmp_path / "prd-empty"
        with_dir = tmp_path / "prd-with"

        _write_parsed(no_spec_dir, dict(_PARSED_BASE))  # no SPECS key

        empty = dict(_PARSED_BASE)
        empty["SPECS"] = []
        _write_parsed(empty_dir, empty)

        with_specs = dict(_PARSED_BASE)
        with_specs["SPECS"] = [
            {"path": "/abs/SPEC.md", "size": 1, "inlined": False, "truncated": False}
        ]
        _write_parsed(with_dir, with_specs)

        no_spec_prompt = build_scope_discovery_prompt(_scope_config(no_spec_dir))
        empty_prompt = build_scope_discovery_prompt(_scope_config(empty_dir))
        with_prompt = build_scope_discovery_prompt(_scope_config(with_dir))

        # The scope-discovery prompt now pins its canonical output path
        # (task_dir/scope-discovery-raw.md — the document-capture hotfix), so each
        # fixture's distinct task_dir basename legitimately appears in the prompt.
        # Normalize that incidental path out so the byte-identity check isolates
        # the only delta this test cares about: AUTHORITATIVE-SPECS block injection.
        def _norm(prompt: str, task_dir: Path) -> str:
            return prompt.replace(str(task_dir), "<TASKDIR>")

        no_spec_norm = _norm(no_spec_prompt, no_spec_dir)
        empty_norm = _norm(empty_prompt, empty_dir)
        with_norm = _norm(with_prompt, with_dir)

        # Empty SPECS array is a true no-op: byte-identical to no SPECS key.
        assert empty_norm == no_spec_norm
        assert "AUTHORITATIVE" not in no_spec_prompt

        # With specs, the prompt differs ONLY by the helper-produced block.
        block = _authoritative_specs_block(["/abs/SPEC.md"])
        assert block in with_prompt
        assert with_norm.replace(block, "") == no_spec_norm

    def test_helper_empty_returns_empty_string(self) -> None:
        assert _authoritative_specs_block([]) == ""
        assert _authoritative_specs_block(None) == ""


class TestInvestigationSpecInjection:
    """R4 also amends the investigation prompt when specs are bound."""

    def test_render_block_present_with_specs(self) -> None:
        prompt = _render_investigation_prompt(
            topic="Auth",
            agent_type="Investigator",
            files=["src/auth.py"],
            product_root="/repo",
            output_path=Path("/repo/research/01.md"),
            spec_paths=["/abs/SPEC.md"],
        )
        assert "AUTHORITATIVE SPECIFICATIONS" in prompt
        assert "/abs/SPEC.md" in prompt

    def test_render_byte_identical_without_specs(self) -> None:
        kwargs = dict(
            topic="Auth",
            agent_type="Investigator",
            files=["src/auth.py"],
            product_root="/repo",
            output_path=Path("/repo/research/01.md"),
        )
        none_prompt = _render_investigation_prompt(**kwargs, spec_paths=None)
        empty_prompt = _render_investigation_prompt(**kwargs, spec_paths=[])
        default_prompt = _render_investigation_prompt(**kwargs)
        assert none_prompt == empty_prompt == default_prompt
        assert "AUTHORITATIVE" not in none_prompt

    def test_config_mode_threads_specs_from_artifact(self, tmp_path: Path) -> None:
        """Config-mode build_investigation_prompt reads SPECS from the artifact."""
        task_dir = tmp_path / "prd-inv"
        parsed = dict(_PARSED_BASE)
        parsed["SPECS"] = [
            {"path": "/abs/SPEC.md", "size": 1, "inlined": False, "truncated": False}
        ]
        _write_parsed(task_dir, parsed)

        cfg = PrdConfig(
            user_message="x",
            product_name="P",
            product_slug="p",
            tier="standard",
            task_dir=task_dir,
        )
        cfg.work_dir = tmp_path

        prompt = build_investigation_prompt(cfg, step_id="investigation-1")
        assert "AUTHORITATIVE SPECIFICATIONS" in prompt
        assert "/abs/SPEC.md" in prompt


# ===========================================================================
# 6. Gate threshold unchanged + WARN (test_gates / test_executor surface)
# ===========================================================================


class TestGateAndWarn:
    def test_scope_discovery_gate_unchanged(self) -> None:
        gate = GATE_CRITERIA["scope-discovery"]
        assert gate.min_lines == 50
        assert gate.enforcement_tier == "STANDARD"

    def test_warn_emitted_to_stderr(self, tmp_path: Path, capsys) -> None:
        spec = tmp_path / "SPEC.md"
        spec.write_text("x", encoding="utf-8")
        ex = _executor_with_specs(tmp_path, [str(spec)])

        ex._warn_spec_degradation()

        err = capsys.readouterr().err
        assert "WARNING" in err
        assert str(spec) in err
        assert "scope-discovery" in err

    def test_warn_lists_persisted_specs_on_resume(self, tmp_path: Path, capsys) -> None:
        """On ``prd resume``, ``config.spec_files`` is empty (``--spec`` is not
        re-passed) but the bound SPECS persist in parsed-request.json. The R5
        WARN must still fire and list the persisted spec path(s) (review comment
        r3367342583). Pre-fix, the empty config suppressed both the gate and the
        message; here the message routes through ``_bound_spec_paths``."""
        ex = _executor_with_specs(tmp_path, [])  # resume: no --spec passed
        parsed = dict(_PARSED_BASE)
        parsed["SPECS"] = [
            {"path": "/abs/SPEC_X.md", "size": 7, "inlined": False, "truncated": False}
        ]
        _write_parsed(ex._config.task_dir, parsed)

        # The R5 gate condition (truthiness of bound paths) is now satisfied on
        # the resume path even though config.spec_files is empty.
        assert ex._bound_spec_paths() == ["/abs/SPEC_X.md"]

        ex._warn_spec_degradation()

        err = capsys.readouterr().err
        assert "WARNING" in err
        assert "/abs/SPEC_X.md" in err

    def test_bound_spec_paths_fails_closed(self, tmp_path: Path) -> None:
        """``_bound_spec_paths`` returns ``[]`` (never raises) when
        parsed-request.json is missing (OSError) or corrupt (JSONDecodeError),
        with ``config.spec_files`` empty — mirroring the fail-soft disk-read
        contract of ``_persist_bound_specs``."""
        ex = _executor_with_specs(tmp_path, [])  # config specs empty
        ex._config.task_dir.mkdir(parents=True, exist_ok=True)

        # (a) Missing parsed-request.json → OSError swallowed → [].
        assert ex._bound_spec_paths() == []

        # (b) Corrupt parsed-request.json → JSONDecodeError swallowed → [].
        (ex._config.task_dir / "parsed-request.json").write_text(
            "not json{", encoding="utf-8"
        )
        assert ex._bound_spec_paths() == []


# ===========================================================================
# 8. Resume carries persisted SPECS without --spec (test_resume_skip surface)
# ===========================================================================


class TestResumeCarriesSpecs:
    def test_persisted_specs_reinject_block_without_spec_flag(
        self, tmp_path: Path
    ) -> None:
        """On resume, config.spec_files is empty but parsed-request.json holds
        the bound SPECS — the scope-discovery prompt must still inject them."""
        task_dir = tmp_path / "prd-resume"
        parsed = dict(_PARSED_BASE)
        parsed["SPECS"] = [
            {"path": "/abs/SPEC.md", "size": 5, "inlined": False, "truncated": False}
        ]
        parsed["WHERE"] = ["/abs", "src/"]
        _write_parsed(task_dir, parsed)

        # Resume config: NO --spec was passed, so spec_files is empty.
        resume_cfg = _scope_config(task_dir)
        assert resume_cfg.spec_files == []

        prompt = build_scope_discovery_prompt(resume_cfg)
        assert "AUTHORITATIVE SPECIFICATIONS" in prompt
        assert "/abs/SPEC.md" in prompt


# ===========================================================================
# Spec content is delivered INLINE in the prompt (see _authoritative_specs_block).
# The cloud-only --file mechanism was removed, so the PRD subprocess argv
# carries NO --file flag for any step; these tests assert its absence and that
# the inline block embeds real content / falls back safely for missing paths.
# ===========================================================================


def _spec_config(tmp_path: Path, spec_files: list[str]) -> PrdConfig:
    return PrdConfig(
        user_message="x",
        product_name="P",
        product_slug="p",
        tier="standard",
        task_dir=tmp_path / "prd-p",
        skill_refs_dir=tmp_path / "refs",  # intentionally absent → no ref args
        spec_files=spec_files,
    )


class TestSpecFileNotAttached:
    """After the --file removal, the PRD subprocess argv carries NO --file flag
    for any step even when spec_files is set — spec/ref content reaches the
    agent inline via the prompt, not via the cloud-only --file mechanism."""

    @staticmethod
    def _command(cfg: PrdConfig, step_id: str, tmp_path: Path) -> list[str]:
        proc = PrdClaudeProcess(
            config=cfg,
            step_id=step_id,
            prompt="p",
            output_file=tmp_path / "out.jsonl",
            error_file=tmp_path / "err.txt",
        )
        return proc.build_command()

    def test_scope_discovery_emits_no_file_flag(self, tmp_path: Path) -> None:
        a = tmp_path / "A.md"
        b = tmp_path / "B.md"
        a.write_text("a", encoding="utf-8")
        b.write_text("b", encoding="utf-8")
        cfg = _spec_config(tmp_path, [str(a), str(b)])

        cmd = self._command(cfg, "scope-discovery", tmp_path)

        assert "--file" not in cmd

    def test_investigation_numbered_step_emits_no_file_flag(
        self, tmp_path: Path
    ) -> None:
        spec = tmp_path / "SPEC.md"
        spec.write_text("s", encoding="utf-8")
        cfg = _spec_config(tmp_path, [str(spec)])

        # "investigation-3" must normalize to "investigation".
        cmd = self._command(cfg, "investigation-3", tmp_path)

        assert "--file" not in cmd


class TestAuthoritativeSpecsBlockInline:
    """Hardened Option B: existing specs are inlined (50KB-capped via the reused
    _read_file); a missing/stale path falls back to a path-only line WITHOUT
    raising (validates the Path(p).is_file() guard)."""

    def test_existing_spec_content_is_inlined(self, tmp_path: Path) -> None:
        spec = tmp_path / "real.md"
        spec.write_text("ZZ_UNIQUE_MARKER_inline\n", encoding="utf-8")

        out = _authoritative_specs_block([str(spec)])

        assert "ZZ_UNIQUE_MARKER_inline" in out
        assert "AUTHORITATIVE SPECIFICATIONS" in out

    def test_oversized_spec_is_truncated(self, tmp_path: Path) -> None:
        spec = tmp_path / "big.md"
        spec.write_text("B" * 50_001, encoding="utf-8")

        out = _authoritative_specs_block([str(spec)])

        assert _TRUNCATION_MARKER in out

    def test_missing_spec_path_does_not_raise(self, tmp_path: Path) -> None:
        missing = "/nope/does-not-exist.md"

        # Must NOT raise FileNotFoundError — validates the Path.is_file() guard.
        out = _authoritative_specs_block([missing])

        assert missing in out

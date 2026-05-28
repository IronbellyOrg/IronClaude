# Code Review: PR #71 — fix(prd): unblock PRD CLI pipeline end-to-end on greenfield repos

**Target**: [IronbellyOrg/IronClaude#71](https://github.com/IronbellyOrg/IronClaude/pull/71)
**Reviewer**: `/sc:auggie-review` (depth=standard, focus=all)
**Generated**: 2026-05-21
**Base ↔ Head**: `master` ↔ `feat/prd-cli-pipeline-fixes` (`7c4b26b0`)
**Stats**: 4 files, 430 line changes, 12 findings (0 dropped during grounding)

---

## Summary

The diff is a well-motivated set of correctness fixes that unblock real failure modes observed on a greenfield PRD run — every fix is anchored to a specific symptom in the integration test (TUIBBS PR #3). The single material concern is that the new behaviour lands without unit-test coverage: the dual-mode prompt builders are now the executor's only call path on Stage B, and a regression there would silently break every Stage B run. Several smaller correctness/style items (an over-loose verdict regex, a triple-fallback that swallows unrelated `TypeError`s, near-identical dispatch glue across three builders, a stale resume docstring) should be addressed in this PR; the rest are noise-level.

**Recommendation**: Request changes — add tests for the dual-mode dispatch and the resume skip logic before merging; the other items can land in the same revision or be filed as follow-ups.

## Findings

### 🔴 Critical (block merge)

None.

### 🟠 High (should fix before merge)

#### H1. Dual-mode prompt builders lack test coverage for the executor calling convention
- **File**: `src/superclaude/cli/prd/prompts.py:572`
- **Category**: tests
- **Source**: auggie
- **Evidence**:
  ```python
  def build_investigation_prompt(  # type: ignore[no-redef]
      *args,
      **kwargs,
  ) -> str:
      ...
      config = args[0] if args else kwargs.get("config")
      if config is not None and hasattr(config, "task_dir"):
          step_id = kwargs.get("step_id") or ""
  ```
- **Why this matters**: The three new dual-mode builders (`build_investigation_prompt`, `build_web_research_prompt`, `build_synthesis_prompt`) are the executor's *only* path on Stage B parallel agents — the legacy positional signature is not called from anywhere in this repo. A regression in the runtime type-probe (`hasattr(config, "task_dir")`), the `step_id` regex, or the per-step arg derivation (research-notes parsing, synthesis-mapping lookup) would silently break every Stage B run, and the failure mode is exactly what this PR was written to fix (`TypeError` before subprocess launch → empty research files → research-qa gate fails on 18 lines of NDJSON). A `grep` of `tests/` shows zero hits for `_parse_agent_block`, `_render_investigation_prompt`, `_render_web_research_prompt`, `_render_synthesis_prompt`, or the dispatch logic; existing `build_investigation_prompt` test hits cover only the legacy positional signature.
- **Recommendation**: Add `tests/cli/prd/test_prompt_builders_dual_mode.py` with at least: (a) the config-based dispatch returning a non-empty prompt for `investigation-1`/`web-research-1`/`synthesis-1`; (b) `_parse_agent_block` against a minimal `research-notes.md` fixture (with and without a matching Agent N section); (c) `synthesis-mapping` indexing (`synth_idx` out-of-range fallback). Also add one end-to-end smoke test that calls `PrdExecutor._build_prompt("build_investigation_prompt", step_id="investigation-1")` with a mock config and asserts the returned string contains the agent's topic.

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Verdict regex now matches sequences with no colon at all
- **File**: `src/superclaude/cli/prd/gates.py:50`
- **Category**: correctness
- **Source**: auggie
- **Evidence**:
  ```python
  md_match = re.search(
      r"(?:^|\n)\s*\*{0,2}[Vv]erdict[*:\s]*(PASS|FAIL)",
      content,
  )
  ```
- **Why this matters**: The character class `[*:\s]*` is `*`-quantified, so `Verdict PASS` (no colon at all), `Verdict::: PASS`, and `Verdict***PASS` all match — the previous regex required a literal `:`. The widening was intended to cover `**Verdict:** PASS` (inner-colon bold), but it also accepts shapes that aren't valid "verdict: value" markdown. In practice no agent emits the degenerate forms, but the gate is now strictly weaker than its stated intent and the comment ("standard markdown bold ordering") understates that.
- **Recommendation**: Replace `[*:\s]*` with an alternation that enumerates the three valid shapes explicitly, e.g. `r"(?:^|\n)\s*(?:\*\*[Vv]erdict\*\*\s*:\s*|\*\*[Vv]erdict:\*\*\s+|[Vv]erdict\s*:\s*)(PASS|FAIL)"`. Same behaviour for the three valid cases, refuses the degenerate ones.

#### M2. `_build_prompt` triple-fallback swallows unrelated `TypeError`s
- **File**: `src/superclaude/cli/prd/executor.py:1083`
- **Category**: error-handling
- **Source**: auggie
- **Evidence**:
  ```python
  try:
      return builder_fn(self._config, context_summaries=..., step_id=step_id)
  except TypeError:
      pass
  try:
      return builder_fn(self._config, context_summaries=...)
  except TypeError:
      pass
  try:
      return builder_fn(self._config)
  except TypeError:
      return f"Execute step using builder {builder_name} (step={step_id})"
  ```
- **Why this matters**: The three-tier fallback exists to probe which calling convention the builder accepts — that's reasonable. But `except TypeError` will also catch `TypeError`s raised *inside* the builder body (e.g. `None + str`, a wrong-type comparison, an `iter()` over a non-iterable). When that happens, the failure is invisibly swallowed and the next convention is tried, which will likely also fail until the fallthrough returns a stub prompt. The Stage B subprocess then runs against an unhelpful prompt and the gate downstream reports a content-shape failure — far from the real bug. The narrow fix is to distinguish "signature mismatch" from "body raised TypeError".
- **Recommendation**: Inspect `builder_fn`'s signature with `inspect.signature(builder_fn)` and dispatch to the matching call once, instead of probing via exception. Falls back to a single bare `builder_fn(self._config)` call if the signature inspection fails. Alternatively, narrow the `except` to only the first call — once Python enters the builder body, any `TypeError` is a real bug and should propagate.

#### M3. Dispatch boilerplate duplicated across three dual-mode builders
- **File**: `src/superclaude/cli/prd/prompts.py:572,692,856`
- **Category**: anti-pattern
- **Source**: auggie
- **Evidence**: the same shape of `config = args[0] if args else kwargs.get("config"); if config is not None and hasattr(config, "task_dir"):` opens each of `build_investigation_prompt`, `build_web_research_prompt`, and `build_synthesis_prompt`. The per-builder differences are limited to (a) which regex extracts the step index from `step_id`, (b) which Agent-N / synth-N entry feeds the call, and (c) which `_render_*` helper to delegate to.
- **Why this matters**: The diff introduces this smell at three sites simultaneously — adding a fourth dynamic builder later (e.g. analyst variants) will copy the same 10-line block again. The original `_parse_agent_block` extraction was good; the dispatch glue should follow the same pattern.
- **Recommendation**: Extract a `_dual_mode_dispatch(*, step_id_pattern, derive_kwargs, render_fn)` helper that does the `args/kwargs` shuffle and calls `render_fn(**derived_kwargs)`. Each of the three public builders becomes a 5-line call. Drives the title of the finding from "duplicate parsing" (Auggie's mis-titling — the parsing in `_parse_agent_block` is already shared) to its real shape: duplicate *dispatch*.

#### M4. Stage A / Stage B resume skip logic has no test coverage
- **File**: `src/superclaude/cli/prd/executor.py:435`
- **Category**: tests
- **Source**: auggie
- **Evidence**:
  ```python
  resume_from = getattr(self._config, "resume_from", None)
  skip_until_idx = 0
  _stage_a_ids = {s[0] for s in _STAGE_A_STEPS}
  if resume_from:
      if resume_from in _stage_a_ids:
          ...
      else:
          skip_until_idx = len(_STAGE_A_STEPS)
  ```
- **Why this matters**: `resume_from` is already tested as a *config field* (7 hits in `tests/`), but the new *skip* behaviour — both the Stage A `skip_until_idx` loop and the Stage B `_STAGE_B_ORDER` / `_should_run` gating with on-disk artifact idempotence — has zero coverage (`grep skip_until_idx tests/` and `grep _STAGE_B_ORDER tests/` both return 0). A regression that flips the comparison direction (`<` ↔ `<=`) or breaks the artifact-existence check would silently re-run Stage A or skip Stage B entirely.
- **Recommendation**: Add unit tests against `PrdExecutor.run()` (or a thin testable seam) with a mocked `_execute_step` that records the order of step IDs invoked. Cases: (a) `resume_from=None` runs all of Stage A; (b) `resume_from="research-notes"` skips check-existing → scope-discovery; (c) `resume_from="assembly"` skips all of Stage A; (d) Stage B with existing `research/01-*.md` skips investigation. Same fixture pattern as `tests/cli/prd/test_resolve_step_content.py`.

#### M5. `prd resume` docstring examples don't reflect the new flags
- **File**: `src/superclaude/cli/prd/commands.py:170`
- **Category**: docs
- **Source**: auggie
- **Evidence**:
  ```python
  def resume(step_id, product, output, tier, max_turns, model, debug):
      """Resume a previously interrupted PRD pipeline from a specific step.
      ...
      Examples:
          superclaude prd resume parse-request
          superclaude prd resume investigation-3 --max-turns 500
      """
  ```
- **Why this matters**: The function signature gained three new options (`--product`, `--output`, `--tier`), and the PR body correctly notes those are required when the original run used a non-default `--output`. But the docstring's Examples block still shows the bare-resume forms only — a user reading `prd resume --help` will not see the case that motivates this PR.
- **Recommendation**: Add an example to the docstring: `superclaude prd resume assembly --product foo --tier heavyweight --output docs/scp-pipeline/PRD_FOO.md`. Optionally, when `resume_from` resolves to a Stage B step and `--output` is at its default, emit a warning hinting that resumes typically need to match the original run's `--output`.

#### M6. Stage B resume detection couples to filename conventions with no shared schema
- **File**: `src/superclaude/cli/prd/executor.py` + `src/superclaude/cli/prd/prompts.py`
- **Category**: coupling
- **Source**: auggie (cross-cutting)
- **Why this matters**: `_execute_stage_b` detects "investigation already done" with `p.name[:2].isdigit()`, "web research done" with `glob("web-*.md")`, and "synthesis done" with `glob("synth-*.md")`. The filename shapes those patterns recognise are set on the writing side in `prompts.py` (`{i:02d}-{slug}.md`, `web-{i:02d}-{slug}.md`, the `synth-NN-*.md` from `load_synthesis_mapping()`). The two sides are not linked by a shared constant or pattern — a future change on either side (e.g. switching to `{i:03d}` for >99 agents, or renaming `web-` to `external-`) silently breaks resume. The detection logic was correct *today*, but is at risk going forward.
- **Recommendation**: Extract a small `artifact_patterns` module (or constants in `models.py`) with `INVESTIGATION_PATTERN`, `WEB_RESEARCH_PATTERN`, `SYNTHESIS_PATTERN`. Both `prompts.py` (when computing `output_path`) and `executor.py` (when detecting existing artifacts) reference the same constant. Add an integration test that writes one investigation file matching the pattern and confirms Stage B skips investigation but proceeds to research-qa.

#### M7. Dual-mode `*args/**kwargs` signatures erase static typing at call sites
- **File**: `src/superclaude/cli/prd/prompts.py` + `src/superclaude/cli/prd/executor.py`
- **Category**: architecture
- **Source**: auggie (cross-cutting)
- **Why this matters**: The three dual-mode builders use `*args, **kwargs` with `# type: ignore[no-redef]` — mypy/pyright cannot verify call-site compatibility, IDEs lose autocomplete, and refactors that rename a parameter cannot be tracked. The pattern is justified by *backward compatibility* with positional-args callers, but those callers don't exist inside this repo (the executor only uses the config-based path). The legacy path is effectively dead code maintained "in case".
- **Recommendation**: Either (a) commit to the config-based signature as the only one (`def build_investigation_prompt(config: PrdConfig, *, context_summaries=None, step_id=None) -> str`) and delete the dual-mode glue, since no in-repo caller uses positional args; or (b) if external callers genuinely exist, add `warnings.warn("positional signature is deprecated", DeprecationWarning, stacklevel=2)` on the positional path and schedule removal. The current "both forever" state is the worst of both worlds.

### 🟢 Low (nice-to-have)

#### L1. Assembly content resolution globs three directories without depth limits
- **File**: `src/superclaude/cli/prd/executor.py:305`
- **Category**: performance
- **Source**: auggie
- **Why this matters**: The new `step_id == "assembly"` branch globs `*.md` in `[task_dir/results, task_dir, task_dir.parent]` and `read_text()`s every match to test `"prd" in name.lower() or "# " in content[:200]`. If `task_dir.parent` is a high-fan-out directory (a workspace root with many co-located docs), the read cost scales linearly with that fan-out on every assembly resolution. The current loop early-exits the moment one of the three directories yields a match, which mitigates the worst case, but the worst case is still a full-tree read of a deep `task_dir.parent`.
- **Recommendation**: Constrain `glob("*.md")` to a depth of 1 (it already is — `Path.glob` is non-recursive without `**`, so this is fine in practice), but skip the `task_dir.parent` search unless the first two directories yield nothing. Optionally, cap each candidate read to the first 4 KB (enough for the `"# "` prefix check) before deciding whether to read the rest.

#### L2. Assembly heuristic reads full file content before deciding it's a candidate
- **File**: `src/superclaude/cli/prd/executor.py:313`
- **Category**: performance
- **Source**: auggie
- **Why this matters**: `content = match.read_text(...)` runs before the `"prd" in match.name.lower() or "# " in content[:200]` check; the name check could be tried first to short-circuit the read for non-PRD-named files.
- **Recommendation**: Reorder: `if "prd" not in match.name.lower(): continue` first (or fold both name and a 4 KB read-prefix check before deciding to read the rest).

#### L3. Dual-mode builders read `config.task_dir / "research-notes.md"` without path validation
- **File**: `src/superclaude/cli/prd/prompts.py:590`
- **Category**: security
- **Source**: auggie
- **Why this matters**: `config.task_dir` is server-constructed (not user-controlled), so this is not an exploitable security issue today. The finding is listed for completeness — if `task_dir` ever accepts user input (e.g. a future `--task-dir` CLI flag), this read becomes a path-traversal sink unless validated.
- **Recommendation**: No action required now. If `task_dir` ever becomes user-supplied, wrap `notes_path = (config.task_dir / "research-notes.md").resolve()` and assert `config.task_dir.resolve() in notes_path.parents`.

### 💬 Nits

- **N1.** `build_task_file_prompt` (lines 334–360) and `build_assembly_prompt` (lines 1109–1140) embed 15+ line conditional `existing_note` blocks inline. Readable, but extracting a `_build_preserve_note_*(...)` helper would shorten the prompt template and avoid duplicating the "if file exists with >=N lines, …" shape. Style only.

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0)
- Findings dropped during grounding: 0
- Persona cross-check: disabled (depth=standard)
- Token cost: Claude ≈ 5k (orchestration + validation), Auggie ≈ 18k (deep pass)
- All 12 findings validated against the actual diff at `7c4b26b0`; every cited `file:line` was confirmed to exist and contain the quoted evidence.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 1 medium: 7 low: 3 nit: 1
dropped: 0
auggie_chunks: 1
duration_sec: 165
-->

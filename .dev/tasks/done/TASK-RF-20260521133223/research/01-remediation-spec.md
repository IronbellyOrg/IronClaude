# Remediation Specification — PR #71 Review

**Source review**: `.dev/reviews/pr-71-20260521130522/REVIEW.md`
**Source PR**: [IronbellyOrg/IronClaude#71](https://github.com/IronbellyOrg/IronClaude/pull/71)
**Spec type**: architecture
**Generated**: 2026-05-21

---

## 1. Overview

The PR #71 review surfaced 12 findings (0 critical, 1 high, 7 medium, 3 low, 1 nit) across the four touched files in `src/superclaude/cli/prd/`. The findings cluster into six structural concerns, not twelve independent items — addressing each cluster resolves multiple findings at once and avoids piecemeal patches that would re-introduce coupling later. This spec defines what to change, where, and how to verify each change. Implementation comes next via the task-builder; this document is the design, not the diff.

## 2. Goals & Non-Goals

**Goals**
- Add test coverage for the new code paths the PR introduces, sized to the risk surface (not exhaustive).
- Replace the duplicated `*args/**kwargs` dispatch glue across the three dual-mode prompt builders with a single shared helper.
- Tighten the over-loose verdict regex so it accepts exactly the three legitimate markdown shapes and nothing more.
- Tighten the `_build_prompt` triple-`except TypeError` so it cannot swallow `TypeError`s raised from inside builder bodies.
- Decouple the Stage B resume artifact-detection from prompt-builder filename conventions via a shared pattern module.
- Update the `prd resume` docstring and improve two small assembly-resolver micro-optimizations.

**Non-Goals**
- No new pipeline features. This is a hardening pass on PR #71's surface, not a re-architecture.
- No removal of the dual-mode signatures yet — keep backward compatibility, but stop duplicating the dispatch.
- No path-validation hardening for `task_dir` reads (L3). The repo's threat model treats `task_dir` as server-trusted; if that ever changes, file a separate spec.
- Not addressing pre-existing concerns in `src/superclaude/cli/prd/` that the PR did not touch.

## 3. Affected Components

| File | Touched in PR #71 | Touched by this spec |
|------|-------------------|---------------------|
| `src/superclaude/cli/prd/prompts.py` | +237 / -8 | Refactor 3 dispatch sites + extract preserve-note helper + import shared pattern constants |
| `src/superclaude/cli/prd/executor.py` | +139 / -16 | Narrow `_build_prompt` TypeError handling + use shared pattern constants in Stage B + small heuristic reorder |
| `src/superclaude/cli/prd/commands.py` | +24 / -0 | Docstring update only |
| `src/superclaude/cli/prd/gates.py` | +4 / -2 | Tighten verdict regex |
| `src/superclaude/cli/prd/models.py` (or a new `_artifact_patterns.py`) | not touched in PR | **new** — house shared artifact pattern constants |
| `tests/cli/prd/test_prompt_builders_dual_mode.py` | not touched | **new** — dual-mode dispatch tests |
| `tests/cli/prd/test_resume_skip.py` | not touched | **new** — Stage A + Stage B resume skip tests |
| `tests/cli/prd/test_gates.py` | not touched | extend with the three valid + three invalid verdict shapes |

## 4. Remediation Design

The six clusters below are the unit of design. Each names the findings it closes, the concrete shape of the change, and the verification that proves it landed.

### Cluster 1 — Test coverage for the new critical path (closes **H1**, **M4**)

The PR adds three runtime-critical behaviors with zero direct tests: the dual-mode dispatch, the Stage A `skip_until_idx` resume skip, and the Stage B `_STAGE_B_ORDER` + on-disk-artifact skip. Each is on the only call path the executor uses; a regression is silent until a real Stage B run halts.

**Two new test modules:**

`tests/cli/prd/test_prompt_builders_dual_mode.py` covers:
- `build_investigation_prompt(config, step_id="investigation-1")` returns a non-empty string containing the Agent-1 topic when `research-notes.md` has an `### Agent 1 — …` section with `**Topic**:` / `**Agent type**:` / `**Files**:`.
- `_parse_agent_block` against (a) a minimal valid block, (b) a missing-`Topic` block (falls back to title), (c) a missing-Agent-N block (returns `{}`), (d) numerical-boundary block at `### Agent 10` (no false-match on `### Agent 1`).
- `build_web_research_prompt(config, step_id="web-research-1")` resolves `agent_idx = 6 + web_idx` and returns a prompt containing the Agent-7 topic.
- `build_synthesis_prompt(config, step_id="synthesis-1")` returns a prompt mentioning `synth-01-…` from the synthesis mapping; `synthesis-99` (out-of-range) falls back to entry 1.
- Legacy positional call still works: `build_investigation_prompt(topic="x", agent_type="y", files=["f"], product_root=".", output_path=Path("o.md"))` returns the same shape `_render_investigation_prompt` produces.

`tests/cli/prd/test_resume_skip.py` covers:
- `PrdExecutor.run()` with `resume_from=None` invokes `_execute_step` for every Stage A step in order. (Mock `_execute_step` and `_execute_stage_b` to record call order; do not spawn real subprocesses.)
- `resume_from="research-notes"` skips `check-existing` and `parse-request` and `scope-discovery`, starts at `research-notes`.
- `resume_from="assembly"` (a Stage B id) sets `skip_until_idx == len(_STAGE_A_STEPS)` and skips all of Stage A.
- `_execute_stage_b` skips investigation when `research/01-foo.md` exists; runs investigation when only `research/web-01-foo.md` exists.
- `_execute_stage_b` skips synthesis when `synthesis/synth-01-foo.md` exists; runs it otherwise.

**Verification criteria for the cluster:**
- `pytest tests/cli/prd/test_prompt_builders_dual_mode.py tests/cli/prd/test_resume_skip.py -q` passes.
- `grep -rn "_parse_agent_block\|_STAGE_B_ORDER\|skip_until_idx" tests/` returns ≥ 6 hits (currently 0).

### Cluster 2 — Consolidate dual-mode dispatch + narrow exception scope (closes **M2**, **M3**, **M7**)

Three near-identical dispatch shapes open `build_investigation_prompt` / `build_web_research_prompt` / `build_synthesis_prompt`, and `_build_prompt` probes three calling conventions via `except TypeError: pass`. Both patterns are addressed together because they share the root issue: signature mismatch is being detected at the wrong layer (runtime exception) rather than the right layer (declared dispatch).

**Design:**
1. **In `prompts.py`**: introduce a private helper
   ```python
   def _dual_mode_call(
       args: tuple,
       kwargs: dict,
       *,
       step_id_pattern: str,           # e.g. r"investigation-(\d+)"
       derive_render_kwargs,           # callable(config, idx) -> dict
       render_fn,                      # callable(**kwargs) -> str
       legacy_field_whitelist: set,    # e.g. {"topic","agent_type","files","product_root","output_path"}
   ) -> str: ...
   ```
   Each public builder collapses to a 5–8 line call into `_dual_mode_call` with three closures: the regex, the per-step `(config, idx) -> render_kwargs` lambda, and `_render_<name>_prompt`. `_parse_agent_block` and `_slugify_agent_title` already live as shared helpers; this finishes the consolidation.

2. **In `executor.py` `_build_prompt`**: replace the three-tier `except TypeError` probe with a single `inspect.signature(builder_fn)` call that branches based on accepted parameter names — call the config form if the signature has a `config`-typed first parameter, otherwise call legacy form. Wrap the body call itself in NO `except TypeError`; if the body raises, that's a real bug and must surface.

**Verification criteria for the cluster:**
- `wc -l src/superclaude/cli/prd/prompts.py` drops by ~25 lines vs the post-PR-71 baseline.
- A new test in `test_prompt_builders_dual_mode.py` defines a `def buggy_builder(config, **kw): raise TypeError("body bug")` and asserts `PrdExecutor._build_prompt("buggy_builder")` propagates the `TypeError` (does not silently return the stub string).
- The three public builder bodies each ≤ 10 statement lines.

### Cluster 3 — Tighten the verdict regex (closes **M1**)

Current `r"(?:^|\n)\s*\*{0,2}[Vv]erdict[*:\s]*(PASS|FAIL)"` matches `Verdict PASS` (no colon), `Verdict::: PASS`, `Verdict***PASS` — all are accepted because `[*:\s]*` is `*`-quantified over a permissive class.

**Design:** replace with an explicit alternation of the three valid markdown shapes:
```python
md_match = re.search(
    r"(?:^|\n)\s*(?:"
    r"\*\*[Vv]erdict\*\*\s*:\s*|"      # **Verdict**: PASS
    r"\*\*[Vv]erdict:\*\*\s+|"         # **Verdict:** PASS
    r"[Vv]erdict\s*:\s*"               # Verdict: PASS
    r")(PASS|FAIL)",
    content,
)
```

**Verification criteria:**
- New test cases in `tests/cli/prd/test_gates.py::TestVerdictField` — `accepts` set = `["Verdict: PASS", "**Verdict**: PASS", "**Verdict:** PASS"]`, `rejects` set = `["Verdict PASS", "Verdict::: PASS", "Verdict***PASS", "verdict pass"]`. Both run as parametrized tests.
- Existing tests that referenced the old loose form (none observed in `grep`) keep passing.

### Cluster 4 — Decouple resume-skip from prompt-builder filename conventions (closes **M6**)

Stage B resume detects "already done" by globbing `research/[0-9][0-9]-*.md`, `research/web-*.md`, `synthesis/synth-*.md`. Those patterns are set on the *writing* side in `prompts.py`. The two sides agree today, but a rename on either side silently breaks resume.

**Design:**
1. Add a new module `src/superclaude/cli/prd/_artifact_patterns.py` (kept underscore-prefixed because it's internal):
   ```python
   from __future__ import annotations
   import re

   INVESTIGATION_FILENAME_RE = re.compile(r"^\d{2}-.+\.md$")
   WEB_RESEARCH_FILENAME_RE = re.compile(r"^web-\d{2}-.+\.md$")
   SYNTHESIS_FILENAME_RE    = re.compile(r"^synth-\d{2}-.+\.md$")

   def investigation_filename(idx: int, slug: str) -> str:
       return f"{idx:02d}-{slug}.md"

   def web_research_filename(idx: int, slug: str) -> str:
       return f"web-{idx:02d}-{slug}.md"

   def synthesis_filename(entry_synth_file: str) -> str:
       return entry_synth_file  # already in synth-NN-*.md form
   ```
2. `prompts.py` uses `investigation_filename(idx, slug)` / `web_research_filename(...)` for `output_path = config.research_dir / investigation_filename(...)`.
3. `executor.py` `_execute_stage_b` uses `INVESTIGATION_FILENAME_RE.match(p.name)` instead of `p.name[:2].isdigit()`; same for web and synthesis.

**Verification criteria:**
- `grep "p.name\[:2\]\.isdigit\|glob(\"web-\*\.md\")\|glob(\"synth-\*\.md\")" src/superclaude/cli/prd/` returns nothing.
- New integration test in `test_resume_skip.py`: write a file via `investigation_filename(1, "core")`, then assert `_execute_stage_b` skips investigation. Then rename it to violate the pattern (e.g. `1-core.md`) and assert investigation runs again.

### Cluster 5 — Update `prd resume` docstring (closes **M5**)

The docstring's Examples block still shows the bare-resume forms and does not mention the new `--product` / `--output` / `--tier` flags that motivated half this PR.

**Design:** add two examples to the `resume()` docstring:
```
superclaude prd resume assembly --product foo --tier heavyweight \
    --output docs/scp-pipeline/PRD_FOO.md
superclaude prd resume structural-qa --product foo --tier heavyweight \
    --output docs/scp-pipeline/PRD_FOO.md
```
Plus a one-line note above the examples: "When the original run used a non-default `--output`, the resume MUST pass the same `--output` (and matching `--product` / `--tier`) so the resumed pipeline reads from the same task directory."

**Verification criteria:**
- `superclaude prd resume --help` shows the heavyweight-with-output example (textual grep in a CLI integration test).

### Cluster 6 — Minor assembly-resolver micro-optimizations (closes **L1**, **L2**) + nit extraction (closes **N1**)

The assembly content-resolver in `_resolve_step_content` reads each candidate `.md` in full before testing `"prd" in match.name.lower() or "# " in content[:200]`. Reorder to check the name first, then the prefix; skip `task_dir.parent` if either of the earlier two directories yielded a match.

Separately, the `existing_note` blocks inside `build_task_file_prompt` and `build_assembly_prompt` are 15+ inline lines each. Extract a helper:
```python
def _preserve_guard_note(
    artifact: Path,
    min_lines: int,
    checklist: list[str],
) -> str: ...
```
Both call sites become 3-line invocations.

**Verification criteria:**
- `_resolve_step_content("assembly", task_dir, "")` with a `results/PRD.md` (≥ 5 KB) and no matching `.md` elsewhere reads the PRD exactly once (assert via a counter or mock-spy in a test).
- `wc -l` on `prompts.py` builders drops by ~20 lines net (after subtracting helper additions).

## 5. Sequencing / Dependencies

The clusters are largely independent but have one ordering constraint:

```
Cluster 4 (pattern module)   ──┐
                               ├──> Cluster 1 (tests can assert via patterns)
Cluster 2 (dispatch helper)  ──┤
                               │
Cluster 3 (regex)            ──┤
Cluster 5 (docstring)        ──┤
Cluster 6 (heuristics + nit) ──┘
```

Recommended order: **Cluster 4 → Cluster 2 → Cluster 6 → Cluster 3 → Cluster 5 → Cluster 1**. Cluster 4 first because constants underpin both the dispatch refactor and the new tests. Cluster 1 last so the new tests assert against the *post-refactor* code, not the pre-refactor state.

## 6. Validation Criteria (whole-spec)

The remediation is complete when **all** of the following hold:

- `make test` (or `uv run pytest`) is green, including the two new test modules and the extended `test_gates.py`.
- `make verify-sync` (if applicable) and `make lint` (or `ruff check`) are green.
- A `git grep` for the pre-refactor smell signals returns nothing:
  - `git grep -n "except TypeError" src/superclaude/cli/prd/executor.py` ← only one survivor in the inspect-signature fallback, not three
  - `git grep -n "p.name\[:2\]\.isdigit\(\)" src/superclaude/cli/prd/executor.py` ← zero
  - `git grep -n "\[*:\\\\s\]\*" src/superclaude/cli/prd/gates.py` ← zero
- The `prd resume --help` output contains the heavyweight + `--output` example.
- A fresh re-run of `/sc:auggie-review 71` (after the remediation lands) shows H1, M1, M2, M3, M4, M5, M6, M7, L1, L2, N1 as resolved (only L3 remaining, intentionally).

## 7. Risks

- **R1 — Refactor regression.** Cluster 2's consolidation touches three of the executor's hottest paths. *Mitigation:* land Cluster 1's tests first (mock-based, fast), so the refactor has a safety net.
- **R2 — Pattern-module relocation.** Cluster 4 introduces a new internal module; downstream code in `cli/sprint/` or `cli/roadmap/` could not know about it and continue to assume the old filename conventions. *Mitigation:* `git grep "web-\*\.md\|synth-\*\.md\|^\\d{2}-"` across the whole `src/` tree before landing; update any other callers (none expected, but verify).
- **R3 — Test-flake on parametrized verdict cases.** The valid/invalid lists in Cluster 3 must not contain ambiguous inputs. *Mitigation:* keep the lists short and concrete; pin them as table-driven tests, not random fuzz.
- **R4 — Reflect-analyze cycle (Phase C) flags more concerns.** The remediation chain's next step (`/sc:reflect --type task --analyze`) may surface scope-drift in the generated task file. *Mitigation:* accept that — the chain is designed to catch this. If reflect-analyze flags issues, the task-builder re-runs with the concerns appended (capped at 2 refactor cycles).

## 8. Open Decisions for the Task-Builder

The task-builder should resolve these when materializing this spec into an MDTM task file:

- Whether the artifact-patterns module is `src/superclaude/cli/prd/_artifact_patterns.py` (favored) or extends `models.py`. The favored option keeps `models.py` focused on dataclasses; the alternative avoids one new file. **Recommendation: new file.**
- Whether `_dual_mode_call` lives in `prompts.py` (private to the module) or in a new `_dispatch.py`. Only `prompts.py` needs it today. **Recommendation: private to `prompts.py`.**
- Test file location: `tests/cli/prd/test_prompt_builders_dual_mode.py` vs adding to existing `test_prompts.py`. The existing file is small; either works. **Recommendation: new file** for searchability.

## 9. Spec Status

Ready for hand-off to the task-builder. The next phase produces an MDTM task file that turns this spec into checklist-driven, evidence-backed execution steps.

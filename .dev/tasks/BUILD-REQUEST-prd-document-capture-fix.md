# BUILD_REQUEST — PRD pipeline document-step gate-failure hotfix (capture + contamination)

## GOAL
Apply the layered hotfix decided by adversarial debate in
`/config/workspace/IronClaude/.dev/troubleshoot/merged-solution.md`: stop every
document-producing step of `superclaude prd run` (`scope-discovery`, `research-notes`, …)
from failing its line-count gate on ~24 lines of NDJSON commentary instead of the agent's
real document, and stop agents contaminating the writable `WHERE` source dir
(`.dev/specs/`). Implement **Layer 1 (prompt path pinning) + Layer 2 (hardened
`_resolve_step_content` backstop) + Layer 3 (truncation guard + preserve the NDJSON↔disk
split)**. The two Layer-3-adjacent architectural items (cwd isolation; result-event capture)
are **explicitly OUT OF SCOPE** for this task — see CONSTRAINTS.

## WHY
Decided design: `/config/workspace/IronClaude/.dev/troubleshoot/merged-solution.md`
(base = Solution 2, +Solution 1 backstop, +Solution 3 guards; convergence 0.86, status
success). Root-cause diagnosis (confidence 0.95):
`/config/workspace/IronClaude/.dev/troubleshoot/REPORT.md`. Supporting artifacts:
`.dev/troubleshoot/adversarial/{diff-analysis,debate-transcript,invariant-probe,base-selection,refactor-plan,merge-log}.md`.

The bug is a double miss in `_resolve_step_content`: it `rglob`s the EXACT canonical filename
(`scope-discovery-raw.md`) under `task_dir`/`task_dir.parent`, but the un-pinned prompt let
the agent invent `scope-discovery.md` under `.dev/specs/` (wrong name AND wrong location), so
recovery falls back to NDJSON commentary and the gate counts ~24 lines. `research-notes`
(STRICT) then HALTs the run on degraded input. Reproduced twice; real 197-line doc preserved
at `/config/workspace/Octodive/.dev/releases/scp-run/recovered-artifacts/scope-discovery.md`.

The invariant probe (Round 2.5) hardened the naive consensus — these corrections are
load-bearing and MUST be honored by the implementation:
- **INV-001**: do NOT add a frontmatter-mandate prompt edit — the research-notes prompt
  already emits `[Date,Scenario,Tier]`, and PRD `_evaluate_gate` never reads
  `required_frontmatter_fields` (dead constraint). Real STRICT criteria = `min_lines=100` +
  the two semantic-section checks.
- **INV-006**: the new multi-match tiebreak MUST prefer freshness (mtime) over content
  length — current source is "largest wins", which lets a stale prior-run file silently win.
- **INV-005**: WHERE-root widening MUST be bounded (realpath containment + symlink rejection);
  naive widening reverses the anti-widening guard already in the file.
- **INV-010**: the `output_text`(NDJSON, drives `_determine_status` sentinels) ↔
  `gate_content`(disk, drives the gate) split MUST be preserved.

## WHERE (PRD CLI Python under `src/superclaude/cli/prd/` — NOT a synced skill/agent/command)
> Line numbers are approximate (verified against source 2026-06-06 but re-confirm before edit).
- `src/superclaude/cli/prd/prompts.py`
  - new helper `_artifact_path_for_step(config, step_id)` (~after L53) — read-only mirror of
    `_STEP_ARTIFACT_FILES`; cross-reference comment both ways.
  - `build_scope_discovery_prompt` (~110-191; output instr ~143-156) — pin output path.
  - `build_research_notes_prompt` (~194-266; reads `task_dir/scope-discovery-raw.md` ~200;
    frontmatter already emitted ~224-228) — pin output path; do NOT touch frontmatter.
  - `build_sufficiency_review_prompt` (~269-319) — pin output path.
  - `build_preparation_prompt` (~516-558) — pin output path.
  - leave the ~12 already-pinned builders (`build_task_file_prompt` ~439, investigation,
    synthesis, qa-*, assembly) UNCHANGED.
- `src/superclaude/cli/prd/executor.py`
  - `_STEP_ARTIFACT_FILES` (~252-263) — UNCHANGED; add `_STEP_ARTIFACT_PATTERNS` beside it.
  - `_resolve_step_content` (~266-365) — pattern-aware search + bounded WHERE roots; keep the
    anti-widening guard intent (~290-292) and the `build-task-file`/`assembly` special cases
    (~309-336) intact; zero-match still falls back to `ndjson_text` (~365).
  - replace the `len(content) > len(best_content)` tiebreak (~360) with `_pick_best_candidate`.
  - `_determine_status` / split (~609/613/618, 645-676) — UNCHANGED; add a guard comment.
  - `_persist_step_artifact` (~1156-1166) — UNCHANGED (canonical name → resume probes).
- `src/superclaude/cli/prd/gates.py`
  - optional `_check_no_truncation_marker(content)` semantic check; research-notes STRICT
    criteria (~329-345), section check (~110-134), phases-detail (~137-154) UNCHANGED.
- Tests: `tests/cli/prd/test_prompts.py`, `tests/cli/prd/test_resolve_step_content.py`,
  `tests/cli/prd/test_gates.py`, `tests/cli/prd/test_executor.py`, `tests/cli/prd/test_e2e.py`.

## DESIGN (concrete — implement the code blocks in `merged-solution.md` Layers 1-3 verbatim;
## refine only if a test exposes a flaw)
1. **Layer 1 — pinning.** Add `_artifact_path_for_step` (merged-solution.md §1a). In each of
   the 4 un-pinned builders, inject the `CRITICAL -- Output Location:` block (§1b) pinning
   `{config.task_dir / "<canonical-name>"}` and forbidding writes into any scoped source/spec
   dir. Add the sync unit test asserting the helper's dict == `_STEP_ARTIFACT_FILES`.
2. **Layer 2 — backstop.** Add `_STEP_ARTIFACT_PATTERNS` (§2a). Rewrite the search to:
   pattern-aware rglob (§2c) over bounded search roots = `[task_dir, task_dir.parent]` +
   realpath-contained, non-symlink WHERE dirs from `parsed-request.json` (§2b). Replace the
   tiebreak with `_pick_best_candidate(preferred_root=task_dir)` where the sort key is
   `(in_preferred_root, mtime, len(content), -len(path.parts))` — freshness above size (§2d,
   INV-006). Zero-match → `""` → existing NDJSON fallback (no regression).
3. **Layer 3 — guards.** Add `_check_no_truncation_marker` to gates.py (§3a). Add a guarding
   comment/assertion at the `output_text`↔`gate_content` boundary so a future refactor cannot
   collapse the split (§3b, INV-010).

## ACCEPTANCE CRITERIA (STRONG assertions — `== True` / `== <canonical path>` / gate `is True`;
## never `!= False`)
- AC1 (Layer 1 pin): each of the 4 builders' rendered prompt contains the exact absolute path
  `config.task_dir / <canonical-name>` and a "do not write to other dir/filename" instruction.
- AC2 (mapping sync): `test_prompt_executor_mapping_sync` — the `_artifact_path_for_step` dict
  is identical to `_STEP_ARTIFACT_FILES` (drift fails the test).
- AC3 (variant-name recovery): agent wrote `.dev/specs/scope-discovery.md` (variant name,
  WHERE dir) + `parsed-request.json` WHERE=`[".dev/specs"]` → `_resolve_step_content(
  "scope-discovery", task_dir, "<24-line ndjson>")` returns the real ≥50-line doc.
- AC4 (freshness tiebreak, INV-006): two matches — a stale LONGER file (older mtime) in a
  WHERE dir vs a fresher SHORTER correct file in `task_dir` → `_pick_best_candidate` returns
  the **fresher task_dir** file (proves mtime+preferred_root outrank raw length).
- AC5 (bounded WHERE, INV-005): a WHERE entry that resolves (via `..` or a symlink) outside
  repo root is NOT added to search roots; a benign in-repo WHERE dir IS.
- AC6 (zero-match fallback): no candidate file anywhere → returns the NDJSON text unchanged
  (existing behavior preserved, no crash).
- AC7 (split preserved, INV-010): after gate content moves to the disk file, a stream whose
  NDJSON tail carries `EXIT_RECOMMENDATION: CONTINUE` / `"verdict":"FAIL"` is still detected by
  `_determine_status` from `output_text` (gate content and status use independent inputs).
- AC8 (persist/resume regression): `_persist_step_artifact` still writes the canonical name;
  resume disk-probes still find artifacts.
- AC9 (truncation guard): `_check_no_truncation_marker` returns a failure string on `[TRUNCATED`
  / trailing `...` and `True` otherwise.
- AC10 (E2E, no contamination): mocked subprocess writing a variant filename → pipeline
  completes without a gate HALT; no `scope-discovery*.md`/`research-notes*.md` left in the
  WHERE dir when prompts are pinned.

## CONSTRAINTS
- **OUT OF SCOPE (do NOT implement — they are deferred follow-ups):** Solution 3's working-dir
  isolation (`cwd=task_dir` / `CLAUDE_WORK_DIR`) and result-event capture (two-pass
  `_extract_text_from_stream_json`, `capture_mode` flag). INV-011 shows blanket cwd breaks
  codebase reads; INV-008 shows the result event is unverified. Touching `process.py` cwd or
  the stream-json extractor is a scope violation for this task.
- **Do NOT add a frontmatter-mandate prompt edit** (INV-001 — redundant + dead constraint).
- Branch `fix/` from `master`; never commit to master/main. PRs target the fork only:
  `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch>` (CLAUDE.md rule).
- `src/superclaude/cli/prd/` is Python package source, NOT a synced skill/agent/command — no
  `make sync-dev` needed for the fix. Run `make verify-sync` only to PROVE no `.claude/` drift
  was introduced; never `git add` any `.claude/` path.
- UV only: `uv run pytest tests/cli/prd/ -q`. `make lint` must exit 0.
- Zero-regression proof: baseline `tests/cli/prd/` run vs post-change run → 0 NEW failures and
  the new tests passing. `_STEP_ARTIFACT_FILES`, the `build-task-file`/`assembly` special
  cases, and `_evaluate_gate` line-count/semantic logic must be untouched.
- Honor the sufficiency scope (INV-002): the fix makes the gate evaluate the REAL document; a
  genuinely thin doc SHOULD still HALT — do not add content-faking to force a pass.

## TEMPLATE
02 (complex) — multi-file (3 source + up to 5 test files), cross-module invariants
(prompt↔executor mapping sync, NDJSON↔disk split), and explicit out-of-scope boundaries that
warrant the richer template. Est. ~8-9h.

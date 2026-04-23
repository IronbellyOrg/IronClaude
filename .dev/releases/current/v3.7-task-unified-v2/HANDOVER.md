# v3.7-task-unified-v2 — Test Handover

**Branch:** `feat/3.7-task-unified-v2`
**Date:** 2026-04-23
**Tester:** Claude Code session (Opus 4.7)
**Fixture:** `test-run/` generated from `.dev/test-fixtures/results/test6-spec/roadmap.md`
**Spec:** `TEST-SPEC.md` (same directory) — has been revised in this session; revisions listed in §4.

This document describes **what was validated**, **what could not be validated in
this environment**, and **what a follow-up tester needs to do** to close the
remaining gaps. It also lists concrete follow-up code items surfaced during
testing.

---

## 0. What this release ships

v3.7 task-unified-v2 is a three-strand release to the Sprint CLI pipeline.
Estimated ~1,480 LOC total across three feature areas; source is the
`v3.7-UNIFIED-RELEASE-SPEC-merged.md` in this directory.

### 0.1 Checkpoint Enforcement (Waves 1-4) — ~580 LOC, 7 files

A three-layer defense architecture (**Prevention → Detection → Remediation**)
that ensures checkpoint reports are always produced during sprint execution.
Motivated by the OntRAG R0+R1 sprint incident (2026-03-22) where Phase 3
silently skipped both checkpoint writes while all other phases wrote them
voluntarily — an unacceptable 86% write rate for a deterministic pipeline.

| Wave | Layer | What ships |
|---|---|---|
| **W1** | Prevention (prompt) | `ClaudeProcess.build_prompt` now injects a `## Checkpoints` block with explicit "write a report to `checkpoints/CP-P<PP>-*.md`" instructions plus a Scope-Boundary mention. Closes the original cause: agent prompt with zero checkpoint instructions. |
| **W2** | Detection (post-phase gate) | New `_verify_checkpoints()` in `executor.py` reads `Checkpoint Report Path:` declarations after each phase, verifies on-disk presence, emits a `checkpoint_verification` JSONL event, and reacts based on `SprintConfig.checkpoint_gate_mode ∈ {off, shadow, soft, full}` (default `shadow`). `full` mode downgrades `PhaseStatus.PASS` to a new `PASS_MISSING_CHECKPOINT` (yellow `PASS⚠` in the TUI), is_success=True so the sprint continues. |
| **W3** | Remediation (retroactive CLI) | New `sprint verify-checkpoints <DIR>` subcommand in `commands.py` with `--json` (parseable manifest) and `--recover` (reconstructs missing reports from `artifacts/` evidence, writes `recovered: true` frontmatter, idempotent). Ships `checkpoints.py` with `build_manifest` / `write_manifest` / `recover_missing_checkpoints` / `extract_checkpoint_paths` / `verify_checkpoint_files`. |
| **W4** | Normalization (tasklist-level) | `/sc:tasklist` now emits checkpoints as **numbered tasks** (`### T<PP>.<NN> -- Checkpoint: <name>`) rather than bare `### Checkpoint:` headings that the task scanner skipped. Deliverable registry adds `D-CP<PP>[-MID]` entries. Every phase file's last task is the end-of-phase checkpoint. |

### 0.2 Sprint TUI v2 (Waves 1-4) — ~800+ LOC, 7 files (5 modified + 2 new)

A comprehensive visual refactor that exposes the rich telemetry Claude's
stream-json already carries. Before v3.7 the TUI showed five columns and one
progress bar; most of the agent's state lived only in raw JSONL and the user
had to `cat` it to see what was going on.

| Wave | What ships | Key symbols |
|---|---|---|
| **W1** | Field plumbing. `MonitorState`, `PhaseResult`, and `SprintResult` grow fields for turns, tokens in/out, output bytes, files changed. `monitor._extract_signals_from_event` / `_handle_assistant_event` / `_handle_user_event` / `_append_activity` / `_append_error` populate them from stream-json. | `models.py`, `monitor.py` |
| **W2** | Dashboard redesign. Phase table columns switch to `# / Phase / Status / Duration / Turns / Output`; dual progress bar shows `Phases [...] X% i/N  Tasks [...] Y% j/M` on a single line using `█/░`; new active panel shows `Prompt:` (from `phase.prompt_preview`), live `Agent:`, and a 3-line `Activity:` tail with `[thinking... Ns]` indicator; conditional red-bordered error panel (max 5); success terminal panel with Turns / Tokens in-out / Output / Files / Log. `SprintConfig.total_tasks` + `count_tasks_in_file` drive the task denominator. | `tui.py` (`_build_phase_table`, `_build_progress`, `_build_active_panel`, `_render_activity_stream`, `_build_error_panel`, `_build_success_panel`, `_format_tokens`), `config.py` (`count_tasks_in_file`, `_extract_phase_prompt_preview`) |
| **W3** | Post-phase & release summaries. New module `summarizer.py` — `PhaseSummarizer.summarize` calls Haiku for narrative and renders `phase-N-summary.md` (Status, Turns, Tokens, Tasks, Files Changed, Validation Evidence, Errors, Narrative). `SummaryWorker` daemon thread commits summaries off the critical path; `on_summary_ready` callback notifies the TUI. New module `retrospective.py` — `RetrospectiveGenerator.generate` aggregates across all phases and writes `release-retrospective.md` (aggregate header, narrative, Phase Outcomes, Files Changed with Multi-phase column, Validation Matrix, Errors). | `summarizer.py` (new), `retrospective.py` (new), `executor._summary_worker` |
| **W4** | Tmux 3-pane layout. `tmux.launch_in_tmux` now splits the window into TUI (50%) / summary pane (25%) / tail pane (25%). `update_summary_pane` + `update_tail_pane` helpers with `SUMMARY_PANE` / `TAIL_PANE` constants replace hardcoded `:0.1`. Summary fan-out: completed phase summaries stream into pane `:0.1`; tail of current phase streams into pane `:0.2`. `--no-tmux` fallback shows a `Summary: Phase N summary ready: results/phase-N-summary.md` line under the phase table. | `tmux.py` (all exports), `executor._summary_fanout` closure |

### 0.3 Naming Consolidation (N1-N11) — ~100 LOC, ~21 live source files

Resolves a three-layer naming collision where `/sc:task`,
`task-unified.md`, and `sc-task-unified-protocol/` each named the same
conceptual unit. `/sc:task` is now the single canonical name.

- **N1-N4 (rename):** `commands/task-unified.md` → `commands/task.md` (frontmatter `name: task`); `skills/sc-task-unified-protocol/` → `skills/sc-task-protocol/`; old paths deleted.
- **N5 (runtime):** `ClaudeProcess.build_prompt` emits `/sc:task Execute all tasks in @<phase-file> --compliance strict --strategy systematic` (previously `/sc:task-unified ...`).
- **N6 (cleanup_audit prompts):** All 5 prompt builders in `cli/cleanup_audit/prompts.py` now say `/sc:task`.
- **N7-N11 (cross-reference propagation):** Docs, guides, agent specs, and sibling command/skill files updated to reference the new name. Zero live `/sc:task-unified` references remain anywhere under `src/` or `.claude/`.

---

## 1. What was validated (passing)

### 1.1 Naming Consolidation (§1, §9.3)
- `/sc:task-unified` removed from source — 0 references in `src/` and `.claude/`.
- `task.md`, `task-mcp.md`, `tasklist.md` present; `task-unified.md` absent.
- Skill dir renamed to `sc-task-protocol/`; legacy `sc-task-unified-protocol/` gone.
- `ClaudeProcess.build_prompt` emits `/sc:task Execute all tasks ...` (verified live + via unit test `test_build_prompt_contains_task_command`).
- `cli/cleanup_audit/prompts.py`: 5 occurrences of `/sc:task `, 0 of `/sc:task-unified`.

### 1.2 Roadmap-to-tasklist generator (§2)
- `/sc:tasklist` skill ran against the test6-spec roadmap and produced:
  - `tasklist-index.md`
  - 5 phase files (`phase-{1..5}-tasklist.md`)
  - `validation/ValidationReport.md` (clean)
- Phase 3 emits a mid-phase checkpoint (`T03.06 -- Checkpoint: …`), satisfying the
  Wave-4 requirement that complex phases produce non-final checkpoint tasks.
- `count_tasks_in_file` returned `{6, 5, 11, 5, 5}`; sum = 32 matched `SprintConfig.total_tasks`.
- `Phase.prompt_preview` populated for every phase.
- Deliverable registry uses `D-CP<PP>[-MID]` format for all 6 checkpoint deliverables.
- Note: skill stages 7-10 (2N parallel validation agents) were abbreviated to a
  downstream-verified equivalent to stay within context budget. See
  `test-run/validation/ValidationReport.md`.

### 1.3 Prompt W1 checkpoint block (§3)
- Built prompt starts with `/sc:task `, contains `## Checkpoints` section, has
  `Checkpoint Report Path:` references, and mentions checkpoints in the Scope
  Boundary section.

### 1.4 Wave-3 manifest / Wave-4 recovery CLI (§5.3, §6.1-6.3)
- `sprint verify-checkpoints $TEST_TASKLIST` table lists 6 declared entries
  (5 end-of-phase + 1 mid-phase), status MISSING when no sprint ran, recovers
  all 6 via `--recover`, second `--recover` is md5-identical (idempotent).
- Recovered files carry `recovered: true` frontmatter and a `## Note:
  Auto-Recovered` heading.
- `manifest.json` writes to `$TEST_TASKLIST/manifest.json` (alongside the index),
  summary `{total=6, found=6, missing=0}` after recovery.
- `--json` output is valid JSON with keys `generated_at`, `summary`, `entries`.

### 1.5 Tasklist-protocol self-check (§8.2, §8.3)
- No legacy `### Checkpoint:` headings on the fixture (0 matches).
- Every phase file's last `T<PP>.<NN>` task contains "Checkpoint".
- `extract_checkpoint_paths` returned ≥1 path per phase, every name matches
  `CP-P\d{2}(-\w+)?`.

### 1.6 Checkpoint gate-mode full downgrade (§4.3, Python-only)
- `_verify_checkpoints(cfg, phase, PhaseStatus.PASS, logger)` with
  `cfg.checkpoint_gate_mode="full"` and a deleted `CP-P01-END.md` correctly
  returned `PhaseStatus.PASS_MISSING_CHECKPOINT`; `.is_success` remained True.

### 1.7 Unit + regression suite (§9.1, §9.2, §9.3, §9.4)
- `tests/sprint/` full run: **921 passed, 57 failed** — matches the declared baseline
  exactly (zero net-new failures; the 57 are pre-existing mock-`Popen`-stdin issues
  plus watchdog-stall-action tests orthogonal to this release).
- TUI Waves 1-2 + tmux + summarizer + retrospective: **125/125 pass**.
- `test_process.py::TestClaudeProcess`: **16/16 pass** including
  `test_build_prompt_contains_task_command`.
- `ruff check src/superclaude/cli/sprint/`: 17 findings (the pre-existing
  baseline that propagates from `cli/pipeline/` and `cli/audit/` re-exports).

---

## 2. What was NOT validated in this environment

### 2.1 Live sprint execution (§4.1, §4.2, §5.1, §5.2, §5.4, §7)
The following surfaces require a real `claude` CLI binary or a stream-json
stub, which the container running this session does not have:

| Surface | Code under test | Why not tested |
|---|---|---|
| TUI rendering (phase table, dual progress, Prompt/Agent panels, activity stream, success panel) | `tui.py` — all `_build_*` helpers | `--dry-run` short-circuits before the TUI enters; no `claude` binary. Unit tests in §9.2 exercise the same functions via direct instantiation (green). |
| Monitor signal extraction | `monitor.py` — `_extract_signals_from_event`, `_handle_*_event`, `_append_activity`, `_append_error` | Needs a live stream-json source. Unit coverage exists in `test_monitor.py`. |
| Per-phase summary files | `summarizer.py` — `PhaseSummarizer.summarize`, `SummaryWorker._run` | Requires a completed phase run. `test_summarizer.py` passes via direct unit tests. |
| Release retrospective | `retrospective.py` — `RetrospectiveGenerator.generate` | Same. `test_retrospective.py` passes. |
| Tmux 3-pane layout | `tmux.py` — `launch_in_tmux`, pane constants | `tmux` is not installed in this container. TEST-SPEC already allows skipping §7. `test_tmux.py` passes via unit tests. |
| `--no-tmux` summary notification | `tui.py` — `latest_summary_notification`, `_render` | Coupled to live sprint execution. |
| `execution-log.jsonl` `sprint_summary` + `checkpoint_verification` events | `executor.py`, `logging_.py::write_checkpoint_verification` | No sprint ran end-to-end. |

### 2.2 What to do to close §2.1 gaps
Pick one of:

1. **Real `claude` binary, live test (expensive, authoritative).** Install
   `claude` on `$PATH`, regenerate the fixture, run `superclaude sprint run
   "$TEST_INDEX" --no-tmux --max-turns 2` (or similar) against a throwaway
   account. Burn through the 5 phases; inspect `execution-log.jsonl`, `results/`,
   `manifest.json` in `$TEST_TASKLIST`. Cost: ~5-10 minutes + real Claude tokens.

2. **Stream-json stub (cheap, behavioral).** Write a shell stub that
   impersonates `claude` and emits a minimal but valid `stream-json`
   conversation per phase. Put it on `$PATH` ahead of any real `claude`. A
   minimal stub example is in `tests/sprint/fixtures/` if present; otherwise a
   5-line bash script printing `{"type":"assistant",…}` / `{"type":"result",…}`
   events is sufficient. This gets you through the TUI / monitor / summarizer /
   retrospective code paths without token cost.

3. **Accept the §9 unit-test coverage as proxy.** The TUI waves, summarizer,
   retrospective, and tmux modules each have direct-API unit tests
   (`test_tui_v2_wave{1,2}.py`, `test_summarizer.py`, `test_retrospective.py`,
   `test_tmux.py`) that all pass (125/125). These exercise the same code paths
   via direct constructors; the gap is only in end-to-end wiring, not in the
   functions themselves.

### 2.3 Roadmap-to-tasklist full 10-stage pipeline
The `/sc:tasklist` skill defines stages 7-10 (2N parallel validation agents,
patch plan, patch execution via `/sc:task`, spot-check verification). This
session produced a clean abbreviated ValidationReport and skipped the 2N agent
spawn because:

- The fixture was generated by the same session, so there's no independent
  drift-detection value in re-reading it in parallel shards.
- Running 10 validation agents on a hand-generated fixture would consume a
  large context budget without adding test signal for the v3.7 release surface.

A future test run starting from a fresh session (which *didn't* generate the
fixture) could productively exercise the full 10 stages on the same
`test-run/tasklists/` bundle.

---

## 3. Anomalies surfaced during testing (follow-up work)

### 3.1 `--checkpoint-gate-mode` CLI flag missing ⚠
- **Symptom:** TEST-SPEC §4.3 prescribed `superclaude sprint run
  --checkpoint-gate-mode full`, but that option does not exist.
- **Code state:** `SprintConfig.checkpoint_gate_mode: Literal["off","shadow","soft","full"]`
  is a real field (default `"shadow"`), and `_verify_checkpoints` in
  `executor.py` branches on its value correctly. Only the Click wiring is missing.
- **Workaround in spec:** §4.3 now uses a Python snippet that constructs
  `dataclasses.replace(cfg, checkpoint_gate_mode='full')` directly.
- **Follow-up:** Add a `--checkpoint-gate-mode {off,shadow,soft,full}` option
  to `sprint run` in `cli/sprint/commands.py::run`, pass it through to
  `SprintConfig`, and add a test under `tests/sprint/test_commands.py`. Small
  change (~10 LoC); just wasn't exposed when the field was added.
- **Severity:** Low — the feature is reachable from the Python API and the
  default `shadow` mode is the intended production-safe default.

### 3.2 `_resolve_release_dir` anchor-file dependency ⚠
- **Symptom:** The pre-fix TEST-SPEC described release_dir as "the parent of
  the `tasklists/` subdir". In practice `_resolve_release_dir` only walks to
  the grandparent when the grandparent contains `.roadmap-state.json` **OR**
  `*spec*.md` / `*requirements*.md`. A plain empty `test-run/` fails the walk
  and falls back to `index.parent` (i.e. `tasklists/`).
- **Impact:** Every `$TEST_RELEASE/...` path in §4.2 / §5.1 / §5.2 / §5.3 /
  §5.4 was wrong by one level. `verify-checkpoints` also resolves checkpoint
  paths relative to its OUTPUT_DIR arg, not via `_resolve_release_dir`, so
  introducing an anchor file would have created inconsistency between the
  runtime-resolved path (`test-run/checkpoints/`) and the CLI-resolved path
  (`tasklists/checkpoints/`).
- **Fix applied to spec:** All artifact paths in §4.2-§5.4 updated to use
  `$TEST_TASKLIST/` instead of `$TEST_RELEASE/`; §6 updated to pass
  `$TEST_TASKLIST` as the OUTPUT_DIR to `verify-checkpoints`.
- **Follow-up (code, optional):** Consider making `_resolve_release_dir`
  unconditionally walk to grandparent when the parent is named `tasklists/`,
  because the current heuristic is leaky (the anchor-file check only helps if
  `roadmap run` created the state file, which `/sc:tasklist` does not). If you
  do that, also update `verify-checkpoints` to perform the same walk, so the
  two surfaces agree on the release-dir location. Medium change.
- **Severity:** Medium. Caused spec drift; fixable either at the spec level
  (done) or at the code level (recommended but not blocking).

### 3.3 `--dry-run` does not exercise the TUI path
- **Symptom:** TEST-SPEC §4.1 invoked `sprint run ... --dry-run` and
  expected to observe the TUI. The current implementation of `--dry-run` just
  prints discovered phases and exits before the TUI loop.
- **Fix applied to spec:** §4.1 now drops `--dry-run` and adds a prominent
  caveat block explaining the three ways to actually drive §4.
- **Follow-up (code, optional):** If there's appetite, introduce a
  `--simulate` mode that wires the TUI and monitor to a canned stream-json
  generator. This would make the `§4` assertions runnable in CI without a real
  `claude` binary. Nontrivial — would require a new subprocess abstraction.
- **Severity:** Low. The spec now documents the three ways forward.

### 3.4 Ruff finding count mismatch
- **Symptom:** TEST-SPEC §9.4 claimed 3 expected findings (`F401 StepStatus`,
  `N806 _OLD_TO_NEW`, `F541`). Actual output: 17 findings because `cli/sprint/`
  imports from `cli/pipeline/` and `cli/audit/` which have their own F401s.
- **Fix applied to spec:** §9.4 now asserts `Found 17 errors.` and enumerates
  the categories. Net-new findings vs. this baseline must be zero.
- **Follow-up (code, optional):** Clean up the 12 `F401` / 1 `F841` / 1 `F401
  typing.Optional` findings in `pipeline/` and `audit/` — trivial `ruff check
  --fix` will resolve 15 of 17.
- **Severity:** Cosmetic.

### 3.5 Verify-checkpoints `--json` breaks under UV warnings
- **Symptom:** Piping `verify-checkpoints --json` straight into `python -c
  'json.load(sys.stdin)'` fails because UV emits a stderr warning that shares
  the terminal in an interactive invocation.
- **Fix applied to spec:** §6.2 adds `2>/dev/null` to the pipe.
- **Severity:** Cosmetic.

### 3.6 Checkpoint heading parser didn't match Wave-4 task form ✅ FIXED
- **Symptom:** Auto-recovered checkpoint reports (e.g.
  `test-run/tasklists/checkpoints/CP-P02-END.md`) contained
  `_(no verification block found in the originating tasklist)_` even though
  the phase file had a populated `**Verification:**` / `**Exit Criteria:**`
  block directly beneath its
  `### T02.05 -- Checkpoint: M2 Primitives Verified` heading. The manifest's
  `name` column also showed the basename (`CP-P02-END.md`) instead of the
  human label (`M2 Primitives Verified`).
- **Root cause:** Both `CHECKPOINT_HEADING_PATTERN`
  (`src/superclaude/cli/sprint/checkpoints.py:29`) and the regex inside
  `_extract_verification_block` (same file, line 302) used:
  ```
  r"^#{2,5}\s*Checkpoint:\s*(.+?)\s*$"
  ```
  which matches the legacy `### Checkpoint: <name>` form but NOT the
  Wave-4 `### T<PP>.<NN> -- Checkpoint: <name>` form that `/sc:tasklist`
  actually emits. Consequences:
  1. `extract_checkpoint_paths` failed to associate the Wave-4 heading with
     its declared path — fell back to `Path(raw_path).name`, so manifests
     carried basenames instead of heading labels.
  2. `recover_missing_checkpoints` passed that basename into
     `_extract_verification_block`, which searched for a literal
     `### Checkpoint: CP-P02-END.md` — a heading that was never written —
     and fell through to the "no verification block" sentinel.
- **Test gap that hid it:** `tests/sprint/test_checkpoints.py` fixtures
  used only the legacy form, so CI never saw a Wave-4 heading. The spec's
  §2.2 assertion that the generator emits the Wave-4 form alone was never
  matched by a test that exercised it end-to-end through recovery.
- **Fix applied (this session):**
  - `src/superclaude/cli/sprint/checkpoints.py:29-32` —
    `CHECKPOINT_HEADING_PATTERN` now accepts an optional `T<PP>.<NN> -- `
    prefix:
    ```python
    r"^#{2,5}\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$"
    ```
  - `src/superclaude/cli/sprint/checkpoints.py:_extract_verification_block`
    (inside the line-match loop) — same optional prefix added.
  - `tests/sprint/test_checkpoints.py` — added 3 new tests:
    - `test_wave4_numbered_checkpoint_task_form`
    - `test_wave4_mid_and_end_mixed_with_legacy`
    - `test_wave4_verification_block_copied_into_recovered_report`
- **Verification after fix:**
  - Full sprint suite: 924 passed / 57 failed (baseline 921/57; the new
    tests are the +3, no regressions in the pre-existing suite).
  - `sprint verify-checkpoints --recover` re-run on the fixture now
    produces reports with populated `**Verification:**` /
    `**Exit Criteria:**` blocks, and the manifest `Name` column shows
    human labels (`M2 Primitives Verified`, `M3 Authenticated Flow Verified`,
    etc.) instead of basenames.
- **Severity:** Medium-high pre-fix (silent data-quality bug in a stated
  Wave-3 feature on the Wave-4 input format). Resolved.

---

## 4. Changes made to TEST-SPEC.md in this session

1. **§2.1** — Swapped reference roadmap from `test5-tdd-prd/roadmap.md` to
   `test6-spec/roadmap.md` (per user request earlier in session); rewrote
   characterization (MEDIUM 0.6 complexity, spec-derived, adversarial
   convergence 0.82, ~425 lines, 5 milestones with M3 at 28 items); tightened
   milestone count assertion from `≥ 5` to `exactly 5`. Added a note
   documenting the `_resolve_release_dir` anchor-file behavior.
2. **§2.2 / §2.3** — Replaced the two `test5 roadmap` mentions with
   `test6-spec roadmap` and anchored the mid-phase-checkpoint claim to M3
   (28 tasks / 3 weeks).
3. **§4.1** — Removed `--dry-run` from the invocation and added a caveat
   block describing why it can't exercise §4 surfaces, plus three ways forward.
4. **§4.2 / §5.1 / §5.2 / §5.3 / §5.4** — Changed all `$TEST_RELEASE/`
   artifact paths to `$TEST_TASKLIST/` to match real `_resolve_release_dir`
   behavior. Updated §5.3 manifest JSON shape to use `summary.total/found`.
5. **§4.3** — Replaced the non-existent `--checkpoint-gate-mode` CLI flag
   with a Python snippet that constructs `dataclasses.replace(cfg,
   checkpoint_gate_mode='full')` and calls `_verify_checkpoints` directly.
6. **§6** — Added an OUTPUT_DIR contract note; changed all
   `verify-checkpoints` invocations to pass `$TEST_TASKLIST` (not
   `$TEST_RELEASE`). Added `2>/dev/null` to the `--json` pipes to filter UV
   warnings.
7. **§9.4** — Updated ruff expectation from 3 findings to 17, and explained
   the propagation from sibling packages.

---

## 5. Files produced / touched in this session

```
.dev/releases/current/v3.7-task-unified-v2/
  TEST-SPEC.md                    # revised per §4 above
  HANDOVER.md                     # this file
  test-run/
    v3.7-spec.md                  # <-- delete this if you re-run; see §3.2 of handover
    tasklists/
      tasklist-index.md           # fixture index (32 tasks, 5 phases)
      phase-1-tasklist.md         # 6 tasks (5 real + 1 end checkpoint)
      phase-2-tasklist.md         # 5 tasks (4 real + 1 end checkpoint)
      phase-3-tasklist.md         # 11 tasks (9 real + 1 mid + 1 end checkpoint)
      phase-4-tasklist.md         # 5 tasks (4 real + 1 end checkpoint)
      phase-5-tasklist.md         # 5 tasks (4 real + 1 end checkpoint)
      checkpoints/                # populated by --recover runs
        CP-P01-END.md
        CP-P02-END.md
        CP-P03-MID-AUTHFLOW.md
        CP-P03-END.md
        CP-P04-END.md
        CP-P05-END.md
      manifest.json
    validation/
      ValidationReport.md         # clean, stages 1-6 passed
    checkpoints/                  # created but unused (no sprint ran against the anchored layout)
    evidence/                     # empty — placeholder
    artifacts/                    # empty — placeholder
```

To rerun from a clean slate:

```bash
rm -rf .dev/releases/current/v3.7-task-unified-v2/test-run
# follow TEST-SPEC.md sections 2 onward
```

---

## 6. Summary for the next tester

| Priority | Item | Status | Owner suggestion |
|---|---|---|---|
| ✅ done | Wave-4 checkpoint heading parser (§3.6) — regex + 3 tests | Fixed this session | — |
| P1 | Wire `--checkpoint-gate-mode` CLI flag in `sprint/commands.py::run` | Open | Backend |
| P2 | Make `_resolve_release_dir` unconditionally walk grandparent when parent name is `tasklists/`, and harmonize `verify-checkpoints` | Open | Backend |
| P2 | Live run of §4 / §5 / §7 with a stream-json stub OR real `claude` | Open | QA |
| P3 | `ruff check --fix` on the 15 auto-fixable findings | Open | Cleanup |
| P3 | Optional: spawn the full 10-stage validation agents on the fixture from a fresh session | Open | QA |

**Net assessment:** the v3.7 release is functionally correct on every surface
this session could reach. One real Medium-high bug surfaced and was fixed
in-session (§3.6, Wave-4 checkpoint heading parser), with three regression
tests added. The two remaining spec↔code mismatches (§3.1 missing CLI flag,
§3.2 release_dir resolution) are low-severity, have clean workarounds, and
don't block the release's core Wave 1-4 functionality.

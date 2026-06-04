# QA Report — Task Integrity Check

**Topic:** Wire Sprint CLI per-task execution + runner-owned typed HandoffRecord (Stages 0-3)
**Task file:** `.dev/tasks/to-do/TASK-RF-20260603-024610/TASK-RF-20260603-024610.md`
**Template:** 02 (complex task)
**Date:** 2026-06-03
**Phase:** task-integrity
**Fix cycle:** N/A
**Stance:** ADVERSARIAL — assume errors present; verify exhaustively.

---

## Verification Log (evidence accumulated incrementally)

### Frontmatter + template path
- Frontmatter parses; all mandatory fields present and non-empty: `id`, `title`, `status`, `created_date`, `type`, `template_schema_doc`, `tags`. VERIFIED via Read.
- `template_schema_doc: src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` — EXISTS on disk (verified `ls`, 85583 bytes). NOT the dead `.claude/templates/` path (verified `.claude/templates/` does not exist). PASS.

### Template-02 mandatory sections
- PART 2 template mandatory `##` sections: Task Overview, Key Objectives, Prerequisites & Dependencies, Detailed Task Instructions, Post-Completion Actions, Task Log / Notes. ALL present in task file (verified grep header list). PASS.
- Sub-sections (Parent Task & Dependencies, Previous Stage Outputs, Handoff File Convention, Frontmatter Update Protocol, Task Summary, Execution Log) all present. PASS.

### Placeholder / format scan (TB-Add-1, item 2)
- `grep -nE "TBD|TODO|FIXME"` → 0 hits. PASS.
- Checkbox format: 69 `- [ ]` items; 0 malformed (`* [ ]` / `- []`). PASS.
- No title-only items observed (all carry Context+Action+Output+Verification+gate). PASS.

### TB-Add-7 (Execution Context cross-validation)
- `grep -cE "src/|/.*:[0-9]+"` on the `## Execution Context` block → 0. Header carries NO file:line. PASS.
- Source areas line present: "sprint executor, sprint process/prompt builder, sprint logging, sprint models, sprint config parser, sprint commands, sprint checkpoints, sprint rerun-tasks, sprint tests, sprint real-spawn e2e harness." Each reappears in ≥1 item Context (executor.py, process.py, logging_.py, models.py, config.py, commands.py, checkpoints.py write_manifest [3.4], rerun_tasks.py [5.5], tests/, e2e_real/). PASS.

### Domain: Path A/B authoritative mapping (CRITICAL)
- Authoritative def (research-notes.md L65-66): Path A = `else`/fallback branch (`executor.py:1309+`), sets `CLAUDE_WORK_DIR=isolation_dir/phase-{N}` → KEEP CLAUDE_WORK_DIR + ADD settings/plugin. Path B = `if tasks:` branch (`executor.py:1265`) → inject full set.
- Live source confirms: `if tasks:` @1265; `else`/fallback @1309 with `isolation_dir` @1310, `_phase_env_vars` @1327 setting `CLAUDE_WORK_DIR=str(isolation_dir)`.
- Task Step 2.2 (Path A): RE-PINS `CLAUDE_WORK_DIR=str(isolation_dir)`, merges ONLY settings+plugin keys → CORRECT direction.
- Task Step 2.4 (Path B): adds `env_vars=_task_env(...)` full set to `_run_task_subprocess` → CORRECT direction.
- NOT wired backwards. PASS.

### Domain: write_task_complete reconciliation
- Live `write_task_rerun_complete` @logging_.py:205, signature `(phase:int, task_id:str, status:str, turns:int, duration_sec:float)`, field order `event, phase, task_id, status, turns, duration_sec, timestamp`.
- Task Step 3.5 specifies identical signature/field order for `write_task_complete`, documented as first-run sibling/discriminator, side-by-side (does NOT silently fork ledger). PASS.

### Domain: HandoffRecord versioned schema + phase-qualified key
- SYNTHESIS H4 L118: `schema_version: int = 1` forward-compat. Step 3.1 specifies exact field set+order incl. schema_version=1. PASS.
- SYNTHESIS H5 L137: key = `handoff/phase-{N}-task-{task_id}.json` (phase-qualified, mirror task_output_file @models.py:561). Step 3.3 specifies exactly this method. PASS.

### Domain: turn-count test (exact, real-spawn) + T02.05/T02.06
- Step 2.10: asserts `turns_consumed == N EXACTLY (not merely != 0)` via real claude-shim spawn (e2e_real). PASS.
- T02.05 = isolation API pin (`test_isolation_layers_probe.py`); kept green in Steps 2.1, 2.11, PG0.2, 5.12, final-verify. PASS.
- T02.06 = existing dead-wire marker; Step 2.7 supersedes it (replaces comment). Not re-used as fresh task ID (task uses Step X.Y numbering). PASS.

### Symbol existence + line-drift verification (item 17, evidence-based)
All symbols referenced by wiring items exist in live source; research-cited lines have drifted but Step 1.3 re-anchors them (drift-proofing pattern satisfied):
- `IsolationLayers` @executor.py:108 (cited 107-148); field order `scoped_work_dir,git_boundary,plugin_dir,settings_dir` confirmed — probe-pinned, Step 2.1 forbids reorder. ✓
- `setup_isolation` @151, `execute_phase_tasks` @928, `_run_task_subprocess` @1079, `if tasks:` @1265, `else`/fallback @1309, `_phase_env_vars` @1327, `results.append(result)` @1066, `_parse_phase_tasks` @1121. ✓
- `write_task_rerun_complete` @logging_.py:205, `_jsonl` @265; `write_task_complete` absent (correctly added by 3.5). ✓
- `build_task_context` @process.py:257 with NO live caller (confirms M3 "never injected" premise); per-task prompt build site present in `_run_task_subprocess`. ✓
- `task_output_file` @models.py:561, `TurnLedger` @758, `resume_command` @677, `build_resume_output` @844, `TaskResult` @166, `SprintConfig` @407. ✓
- `walk_dependencies` @rerun_tasks.py:368, `_dependencies_of` @438, `_is_satisfied` @453 (Step 5.5 reuse target). ✓
- `write_manifest` atomic idiom @checkpoints.py:173-210 (`mkdir parents → .tmp → tmp.replace`) — matches Step 3.4 verbatim citation. ✓
- No existing `num_turns` parser (Step 2.6 add-not-duplicate is sound). ✓
- `_TASK_HEADING_RE` @config.py:380, `parse_tasklist` @405, `load_sprint_config` @281; `run()` + click options in commands.py (3-layer plumbing targets). ✓

### Granularity + dependency ordering (items 10, 11, 15, 16; TB-Add-4 DAG)
- Define-before-use confirmed for every introduced symbol:
  HandoffRecord 3.1 → serialize 3.2 → FileHandoffStore 3.4 → write 3.7 → gate 3.11;
  count_turns 2.6→2.7; _task_env 2.3→2.4/2.5; is_validated_success 4.1→4.2;
  try_launch 5.3→5.4; scheduler 5.5→5.7; execute_phase_tasks widened 3.6 before 3.7 write.
- Phase 1 Step 1.3 (symbol map) precedes all Phase 2+ wiring that consumes it. ✓
- No item-to-item cycles (item-DAG acyclic). ✓
- Items are atomic (one edit/test/flag/schema each); no batch items. The largest items (3.10, 4.3, 5.6 thread a flag through 3 layers) are a single coherent flag-plumbing unit, acceptable per the click 3-layer-lockstep convention. PASS.

### TB-Add-8 (per-item Context evidence binding)
- Code-referencing items carry file:line citations (e.g. 2.1 `executor.py:151-183/107-148`, 2.7 `executor.py:1117-1118`, 3.3 mirrors `task_output_file` @562, 5.4 `executor.py:976/992`). ✓
- Test-creation items (2.8-2.10, 3.13-3.16, 4.6-4.8, 5.8-5.10) reference SYNTHESIS section + research file anchors and create NEW files (no existing source line yet) — acceptable evidence binding. ✓

### L5/L2 docs items (3.17, 5.11, 6.1)
- CHANGELOG.md + docs/sprint-cli-deep-dive.md etc. exist; doc items Grep/Glob to locate (no hardcoded fabricated path) and record negative evidence + a doc-notes stub if absent. ✓
- Step 6.1 edits SYNTHESIS.md (the authoritative spec, a declared related_doc) — in scope, not a scope violation. ✓

### Open Questions / gaps (item 7)
- No `## Open Questions` section, but template-02 does not mandate one. Research-notes "Gaps & Questions" = "None blocking." The `### Phase Gate Findings` section explicitly reserves a venue for QA-gate Open Questions. Acceptable. PASS (with advisory note below).

---

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter complete + template_schema_doc → live 02 path | PASS | ls confirms src path exists; .claude/templates absent |
| 2 | Mandatory template-02 sections present | PASS | grep header list — all PART 2 sections present |
| 3 | Items self-contained (Context/Action/Output/Verify/gate) | PASS | every item carries 5-field body + "ensuring…" + completion gate |
| 4 | Granularity — no batch items | PASS | one edit/test/flag/schema per item; 69 atomic items |
| 5 | Evidence-based (file:line or symbol+anchor) | PASS | all symbols verified in live source; Step 1.3 drift re-anchor |
| 6 | No items on unverified/contradicted findings | PASS | all anchored to SYNTHESIS §6/§7 + verified source |
| 7 | Open Questions + gaps documented | PASS (advisory) | Phase Gate Findings reserved; research gaps = none-blocking |
| 8 | Phase deps logical (DAG, no cycles) | PASS | define-before-use confirmed across all phases |
| 9 | Reasonable item count | PASS (advisory) | 69 items for XL 4-stage task w/ per-stage gates |
| 10 | TB-Add-1 placeholder scan | PASS | 0 TBD/TODO/FIXME; no title-only |
| 11 | TB-Add-2 item-count bounds | ADVISORY | 69 > 50 single-track bound; bound uncalibrated → non-blocking |
| 12 | TB-Add-3 clarification adjacency | PASS (N/A) | no Open-Question-blocked items |
| 13 | TB-Add-4 item-DAG acyclic | PASS | no item→item cycles |
| 14 | TB-Add-5 XL splitting | PASS | XL task split into 6 phases + gates; items atomic |
| 15 | TB-Add-6 Verify/format consistency | PASS | uniform "ensuring…" verification phrasing |
| 16 | TB-Add-7 Execution Context cross-val + no file:line | PASS | grep count 0; all source areas reappear in items |
| 17 | TB-Add-8 per-item Context evidence binding | PASS | code items carry file:line; test items cite spec+research |
| D1 | Path A/B authoritative mapping (not backwards) | PASS | 2.2 Path A keeps WORK_DIR+adds 2; 2.4 Path B full set |
| D2 | write_task_complete reconciles w/ rerun (no fork) | PASS | 3.5 mirrors rerun shape, side-by-side discriminator |
| D3 | HandoffRecord versioned + phase-qualified key | PASS | 3.1 schema_version=1; 3.3 phase-{N}-task-{id}.json |
| D4 | Turn-count test exact + real-spawn | PASS | 2.10 asserts ==N via e2e_real claude shim |
| D5 | T02.05 pin kept green; T02.06 not duplicated | PASS | probe green in 2.1/2.11/PG0.2/5.12; 2.7 supersedes T02.06 |

## Summary
- Checks passed: 22 / 22 (2 advisory, non-blocking)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Confidence
- **Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: (via Bash) | Glob: 0 | Bash: 9
- No UNCHECKED items. No UNVERIFIABLE items. No external web lookups required (all source-truth-local).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | ADVISORY | TB-Add-2 | 69 items exceeds the speculative ≤50 single-track bound | Bound is uncalibrated (ADVISORY per gate spec); count is justified for an XL 4-stage wiring task with mandatory per-stage QA gates. No action required. |
| — | ADVISORY | item 7 | No dedicated `## Open Questions` section | Template-02 does not mandate one; research gaps are "none-blocking" and Phase Gate Findings reserves a QA-Open-Question venue. No action required. |

## Actions Taken
None — no blocking issues found. fix_authorization was true but no in-place fix was warranted.

## Recommendations
- Proceed to execution. The Path A/B mapping (the audit's core risk) is wired in the correct direction, all referenced symbols exist in live source, dependency ordering is a clean DAG, and all 5 domain-specific correctness points hold.
- During execution, Step 1.3's symbol-anchor map is the load-bearing drift guard — ensure it runs first and is honored by every later wiring item (research-cited lines have drifted +0..+small but symbols are all locatable by name).

## QA Complete

# QA Report — Research Gate

**Topic:** MDTM Template-02 tasklist for wiring Sprint CLI per-task execution + handoff (Stages 0–3)
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL

One CRITICAL labeling inconsistency (Path A/B inverted between research file 05 and the authoritative SYNTHESIS/R3/notes/analyst) plus two MINOR doc-hygiene items. The CRITICAL must be corrected before the builder consumes these files, because the builder threads "Path A"/"Path B" directly into per-edit task items and an inverted label would wire isolation env into the wrong branch.

**Important:** every load-bearing *technical* claim verified correct against source. The failure is a label-vs-branch mismatch in ONE file, not a factual error about the code. R5's branch-behavior descriptions are all accurate; only the A/B letters are swapped.

---

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep/Bash: 7 | Glob: 0 (file existence checked via ls in Bash)

No web research performed (all claims are local-source-bound).

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 6 files Status: Complete + Summary | PASS | All 6 assigned files read; each carries `Status: Complete` and a Summary section. |
| 2 | Evidence density (file:line citations accurate) | PASS | Re-Read 9 source spans; every spot-checked citation accurate (see Verified Claims). Density Dense (>80% evidenced). |
| 3 | Scope coverage (key files examined) | PASS | executor/process/config/logging_/models/checkpoints/rerun_tasks/commands all covered across R1–R5; tests/ covered by R4; template by R6. |
| 4 | Doc cross-validation tags | PASS (N/A) | No external-doc-sourced claims requiring `[CODE-VERIFIED]` tags; all claims are code-traced. Template-path claims (R6) verified by ls. |
| 5 | Contradiction resolution | **FAIL** | Path A/B labels are INVERTED between R5 (05-data-flow) and R3 + research-notes + analyst + SYNTHESIS §H1. Unresolved cross-file contradiction. See Issue #1. |
| 6 | Gap severity (all gaps must be resolved) | PASS | No unresolved research gaps that would cause synthesis hallucination; the per-task wiring surface is fully mapped. |
| 7 | Depth — end-to-end data flow traced | PASS | R5 traces execute_sprint → fork → execute_phase_tasks → TaskResult → phase-N-result.json → rerun read-side end-to-end. |
| 8 | Integration point coverage | PASS | R3 documents all 7 wiring seams (isolation merge, context inject, write_task_complete, env-capture, turns, ledger lock, heading router) with file:line. |
| 9 | Pattern documentation | PASS | R2 documents atomic-write, JSONL-event, dataclass-serialization, Click-flag, SprintConfig-field patterns with file:line. |
| 10 | Incremental-writing compliance | PASS | Files show iterative structure (per-symbol tables, per-seam sections), not one-shot prose walls. |

---

## Verified Claims (zero-trust spot-checks against real source)

All of the following were re-Read directly from source and confirmed:

| Claim (research) | Source line re-Read | Verdict |
|---|---|---|
| `_run_task_subprocess` returns `turns_consumed=0` hardcoded | executor.py:1117-1118 `# Turn counting is wired separately in T02.06` / `return (..., 0, output_bytes)` | ✓ EXACT |
| Path A fallback `_phase_env_vars` sets only `CLAUDE_WORK_DIR=isolation_dir` (per-phase copy dir) | executor.py:1310-1330 | ✓ EXACT |
| `setup_isolation` / `IsolationLayers.env_vars` `CLAUDE_WORK_DIR = config.release_dir` (whole release dir → CONFLICTS with phase-scoped) | executor.py:129-130, 178-180 | ✓ EXACT (the H1 crux) |
| `_jsonl` lock-free append `open(...,"a")`+`f.write(json.dumps(data, default=str)+"\n")` | logging_.py:265-267 | ✓ EXACT |
| `write_task_rerun_complete` event shape `{event, phase, task_id, status, turns, duration_sec, timestamp}` | logging_.py:205-219 | ✓ EXACT |
| `task_output_file` is models.py:561 (NOT config.py) | models.py:561 | ✓ EXACT |
| `walk_dependencies` body — single-level expand, not transitive closure | rerun_tasks.py:478-514 (outer loop iterates only original target_ids; no recursion into added deps) | ✓ EXACT |
| `SprintConfig`/`task_output_file`/`resume_command`/`TurnLedger` in models.py, NOT config.py | models.py:407/561/677/758; config.py only *imports* SprintConfig | ✓ EXACT (R1 attribution correction valid) |
| `SprintLogger` is NOT a param of `execute_phase_tasks` | executor.py:928-941 signature has no `logger`/`SprintLogger` param | ✓ EXACT |
| `FileHandoffStore` does not exist | `grep -rn FileHandoffStore\|HandoffStore\|handoff_store src/` → zero matches | ✓ EXACT |
| `write_task_complete` does not exist (R3) | grep src/ → none | ✓ EXACT |
| `write_task_rerun_complete` / `build_task_context` DEAD in prod (no src caller) | grep src/ → definition-only | ✓ EXACT |
| Fork: `if tasks:`→per-task (no env); fallback→single-proc (CLAUDE_WORK_DIR) | executor.py:1264-1330 | ✓ EXACT |
| Template `src/superclaude/templates/workflow/02_...md` exists (85583 b); `.claude/templates/workflow/` absent | ls | ✓ EXACT |
| Example task file + size; TB-Add catalogue at task-builder SKILL.md L1165-1173 | ls + grep | ✓ EXACT |

---

## PATH A / PATH B RESOLUTION (definitive — the user's flagged ambiguity)

**Authoritative source: SYNTHESIS.md §H1 (`.dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md:15`):**

> "Path A (per-phase single session) when the phase file has no `### TNN.MM` headings; Path B (one subprocess per task) when it does."

Mapped to verified source code:

- **Path A = per-phase single session** = the `else`/fallback branch at **executor.py:1309+** (`isolation_dir`, `shutil.copy2`, single `ClaudeProcess`). **This is the branch that currently sets `CLAUDE_WORK_DIR`** (executor.py:1327-1328, value = per-phase `.isolation/phase-{N}` copy dir).
- **Path B = per-task** = the `if tasks:` branch at **executor.py:1265** → `execute_phase_tasks` → `_run_task_subprocess`. **This branch sets NO env vars** (executor.py:1101-1111 has no `env_vars=`). This is the unmitigated-corruption path.

**Cross-file agreement:**
| Source | Path A = | Path B = | Matches authoritative? |
|---|---|---|---|
| SYNTHESIS.md §H1 (authoritative) | per-phase single session | per-task | — |
| research-notes.md:19 ("Path A: CLAUDE_WORK_DIR=phase-copy dir") | per-phase single | (per-task) | ✓ |
| analyst-completeness-report.md:37 ("Path A's phase-scoped isolation_dir") | per-phase single | (per-task) | ✓ |
| **R3 / 03-wiring-seams.md** (explicit note at top) | per-phase single | per-task | ✓ |
| **R5 / 05-data-flow.md §1 heading** | **per-task** ❌ | **single proc** ❌ | **✗ INVERTED** |

**Verdict: R3 is correct; R5 has the A/B labels swapped.** R5's technical descriptions of each branch are accurate — only the letters attached to them are inverted, which is precisely the trap that propagates silently into a tasklist.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | **CRITICAL** | `research/05-data-flow.md` §1 (heading "Path A (per-task) vs Path B (single proc)"; §1 sub-headings "Path A — per-task delegation", "Path B — single ClaudeProcess"; Summary "**Only Path B** builds `isolation_dir`") | Path A/B labels are INVERTED vs the authoritative SYNTHESIS §H1, research-notes, R3, and the analyst report. R5 calls the per-task `if tasks:` branch "Path A" and the single-process fallback "Path B" — the exact opposite of every other source. A task builder that reads R5's "only Path B builds isolation_dir / CLAUDE_WORK_DIR" alongside R3's "Path A sets CLAUDE_WORK_DIR" will produce contradictory or wrong-branch isolation-wiring items. | Builder MUST adopt the SYNTHESIS/R3 convention (Path A = per-phase single session = fallback w/ CLAUDE_WORK_DIR; Path B = per-task = `if tasks:` branch w/ no env). Treat R5's branch-*behavior* content as correct but mentally swap its A/B *letters*. The tasklist must NOT propagate R5's lettering. Recommend the builder add an explicit "Path A/B per SYNTHESIS §H1" definition line in the Execution Context so no item inherits the inverted labels. |
| 2 | MINOR | `research/01-file-inventory.md:88-90` — `_run_task_subprocess` return `(exit_code, 0, output_bytes)` | Accurate, but worth a builder note: the middle `0` is the turns slot, and the budget reconcile (executor.py:1026-1033) consequently credits back the full `minimum_allocation` every task — a no-op budget model today. R1/R5 both state this. Flagged so the Stage-0 acceptance test asserts the *correct* count, not merely `!= 0`. | No fix required; ensure the Stage-0 task item cites "assert exactly N, not != 0" (R4 §6 row already does). |
| 3 | MINOR | `research/06-template-and-examples.md:167` ("TB-Add-1..8 … L1165-1173") | task-builder SKILL.md's own header at L1165 reads "TB-Add-1 through TB-Add-7" while TB-Add-8 lives at L1173. R6's claim that all 8 gates exist in that span is correct (verified), but the upstream SKILL.md header undercounts. Not a research error. | No fix to research required. Optional upstream note: SKILL.md:1165 header should read "through TB-Add-8". Out of scope for this gate. |

---

## Coverage / Actionability Assessment

- **No coverage gaps that block the builder.** Every Stage 0–3 seam named in the TRACK GOAL (turns_consumed, isolation merge, context injection, write_task_complete, handoff persistence, ledger thread-safety, heading router) has a concrete file:line edit point. R4 supplies the test-extend/add map per stage. R6 supplies the template structure + TB-Add gate requirements.
- **Findings are concrete enough for per-edit task items.** R3 gives exact edit forms (ADD-only env merge for Path A, full-set injection for Path B, `_task_env` helper extraction). R2 gives the exact idioms (atomic write, JSONL shape, dataclass serialization) any new symbol must follow.
- **No unsupported assertions stated as fact.** The "proposed" symbols (FileHandoffStore, HandoffRecord, write_task_complete, _task_env) are all explicitly framed as targets-to-build, never as existing code. R4 explicitly corrects the premise ("there is NO FileHandoffStore", "loop is sequential not concurrent") rather than inventing one.

---

## Recommendations (before synthesis/build proceeds)

1. **Resolve Issue #1 (CRITICAL).** The builder must standardize on SYNTHESIS §H1 lettering (Path A = single-session fallback w/ CLAUDE_WORK_DIR; Path B = per-task). Cleanest mitigation: have the task-builder emit an explicit Path A/B definition in the `## Execution Context` / first isolation item, citing SYNTHESIS §H1, and never quote R5's A/B letters verbatim. R5's content is salvageable as-is once the reader swaps the letters.
2. Carry R1's attribution correction (models.py not config.py) into every per-edit item touching SprintConfig/task_output_file/resume_command/TurnLedger.
3. Carry R4's "assert exact turn count, not != 0" into the Stage-0 acceptance item, and its "any new handoff event must be inert on a clean sprint / add zero daemon threads" backward-compat guardrail into the Stage-2/3 items.
4. Set `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"` (NOT `.claude/...`) per R6 Section 0.

---

## VERDICT: FAIL

**Blocking issue:** 1 CRITICAL (Path A/B label inversion in 05-data-flow.md vs authoritative SYNTHESIS §H1 / R3 / notes / analyst). 2 MINOR advisory items (non-blocking).

Per research-gate policy (ALL gaps regardless of severity = FAIL), this gate FAILs until the Path A/B contradiction is resolved so the inverted lettering cannot propagate into the generated tasklist. All other 9 checklist items PASS; every load-bearing technical claim is verified accurate against source. The fix is label-normalization (plus a one-line Execution Context definition), not re-research.

## QA Complete

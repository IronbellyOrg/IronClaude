# QA Report — task-qualitative

**Topic:** TASK-RF-20260604020650 — Fix PR #120 Medium Findings (M1/M2/M3/M4)
**Date:** 2026-06-04
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)

---

## Overall Verdict: PASS

All 15 task-qualitative checks pass against the actual target source. Every semantic claim the
task encodes (function locations, line citations, fix shapes, test seams, scheduler expected
outputs, lifecycle contracts) was independently verified against the real files under
`src/superclaude/cli/sprint/` and `tests/sprint/`. No CRITICAL, IMPORTANT, or MINOR plan defect
was found. Two cosmetic prose imprecisions are noted under "Observations" — neither is
execution-blocking nor meets the MINOR bar (the items list the required imports regardless, so
execution self-corrects).

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | All verify cmds are `uv run pytest .../<file> -v`, `uv run ruff format --check src/ tests/`, `make lint`. New files (`test_poll_watchdog_ceiling.py`, `test_scheduler.py`) confirmed ABSENT on disk → "CREATE" is correct, no collision; created in Phases 4/5 BEFORE the Step 6.1 full-suite run → precondition satisfied. UV-only honored throughout. |
| 2 | Project convention compliance | none | PASS | All edits target `src/` (canonical) + `tests/` — no skills/agents/commands, so NO `make sync-dev` / `.claude/` touch needed (correctly omitted). Step 6.2 correctly separates `ruff format --check` from `make lint` (CI gate distinction). `--strict-markers` honored: only `@pytest.mark.unit` used. |
| 3 | Intra-phase execution-order simulation | none | PASS | Phase 2 (2.1 fix → 2.2 test → 2.3 verify), Phase 3, 4, 5 each order src-fix → test → verify. Phase 6 full-suite runs after all new files exist. Each item's reads (research files, source files) are available before use. No item reads a file a later item creates. |
| 4 | Function signature verification | none | PASS | `FileHandoffStore.read(*, phase, task)` at handoff.py:62-71, final line L71 = `return HandoffRecord.from_dict(json.loads(path.read_text()))` — EXACT match. `_run_task_subprocess` def at executor.py:1468, `proc.start()` L1514, poll call L1518-1520, return tuple L1521-1529 — EXACT match. `_poll_with_stall_watchdog` def L1402, loop L1439, tail wait L1465, kill branch L1459-1464, disabled path L1424-1426 — EXACT match. Scheduler 4 fns (`CycleError`/`dependencies_of`/`topological_launch_order`/`is_task_satisfied`) all exist at cited lines. `TaskEntry`/`TaskResult` constructors accept the kwargs the tests use. |
| 5 | Module context analysis | none | PASS | M3: `json` imported handoff.py:18, `HandoffRecord` L20 → "no new imports" correct; `json.JSONDecodeError ⊂ ValueError` so `except (json.JSONDecodeError, ValueError)` is sound. M1: `proc.terminate()` is a real method; `import time` module-level (executor.py:12) → `executor.time.monotonic`/`.sleep` patch targets valid. M2: `time.monotonic` already module-bound (L1437/1444/1446). M4: scheduler `is_success` returns real bool (models.py:57-58) → `is True`/`is False` assertions valid. |
| 6 | Downstream consumer analysis | none | PASS | M3: `read()` reads from `self.config.handoff_file(phase, task)` (handoff.py:68) — the SAME path the M3 test writes corrupt bytes to → corrupt bytes DO reach the guarded `json.loads`. Both callers treat `None` as re-run (per research, unchanged contract). M1: terminate→`_close_handles()` (process.py:175-177, 238-244) is the leak-closing consumer; happy path unchanged (poll's internal `proc.wait()` L1465 still closes). M2: tail `proc.wait()` (L1465) is the sole bounded consumer the ceiling routes to — not moved/duplicated. |
| 7 | Test validity | none | PASS | Every test exercises REAL behavior: M3 writes 3 real corrupt inputs to the real on-disk path (not a mocked store); M1 patches the proven `ClaudeProcess.__init__`/`start`/`terminate` seam from the existing test_executor.py:1904-1965 and drives the real `_run_task_subprocess`; M2 drives the real `_poll_with_stall_watchdog` with a never-exiting fake proc + deterministic patched `monotonic`; M4 calls the real scheduler functions and asserts traced outputs. No `# Test`-style stub fixtures. |
| 8 | Test coverage of primary use case | none | PASS | M3 covers truncated+empty+garbage (3 inputs). M1 asserts BOTH cleanup-fires AND exception-re-propagates (`pytest.raises(KeyboardInterrupt)` + `terminate_called`) — catches swallow-regression. M2 covers warn-ceiling (primary), kill-mode-unchanged (regression guard), and disabled-path (invariant). M4 covers all 6 traced cases (diamond/linear/independent+permute/cycle/self-edge/unknown-dep) plus de-dup/union/tri-state oracle. |
| 9 | Error path coverage | none | PASS | M3 IS an error-path fix (corrupt input → None). M1 IS an exception-path fix (`except BaseException`). M2 IS a liveness/unbounded-loop fix. M4 asserts the cycle error path (`CycleError` + `.unresolved` + str message). Each fix item documents the blocker-logging fallback into a templated Findings section. |
| 10 | Runtime failure-path trace | none | PASS | M1 wrap leaves L1521-1529 return tuple intact on happy path; on exception, terminate→raise correctly skips them (exception aborts). M2 loop-guard `and (time.monotonic()-loop_started)<ceiling` falls through to tail `proc.wait()` — does not break kill-mode break or disabled-path. M3 guard returns None without disturbing `path.exists()` early-return. No downstream gate/consumer left unable to handle new output. |
| 11 | Completion-scope honesty | none | PASS | The single OPEN QUESTION (M2 ceiling fallback value) is RESOLVED inline: research verified `config.timeout_seconds` does NOT exist (grep confirms ABSENT on SprintConfig) and would AttributeError; `proc.timeout_seconds` (set executor.py:1506 / ClaudeProcess L61) is correct; recommended `getattr(proc,"timeout_seconds",3600)`. The plan does not ignore its own open question — it dispatches it. |
| 12 | Ambient-dependency completeness | none | PASS | Scheduler imports `from ...scheduler import CycleError, dependencies_of, topological_launch_order, is_task_satisfied` — all 4 are module-level (no `__init__.py` re-export needed). `TaskEntry`/`TaskResult`/`TaskStatus` from `...models`. No `__init__.py`/CLI/registry touchpoints involved (pure test additions + 2 surgical src guards). Frontmatter update protocol present (1.1, post-completion). |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add parameter" pattern. The M2 ceiling reads `getattr(proc,"timeout_seconds",...)` — a read of an attribute already set at executor.py:1506, not a new param. M1 passes no new args. Source fixes precede their tests; verify steps follow. |
| 14 | Function-existence claims verified | none | PASS | "scheduler has zero dedicated tests" (M4): grep `from superclaude.cli.sprint.scheduler import` across tests/ → EMPTY, confirmed. "json imported"/"HandoffRecord imported": confirmed handoff.py:18/20. "config.timeout_seconds does not exist": confirmed absent (grep models.py empty). "proc.timeout_seconds exists": confirmed (process.py:61, executor.py:1506). All existence claims grep-verified. |
| 15 | Cross-reference accuracy | none | PASS | All scheduler line cites accurate: self-edge filter L57-60, declared+recorded union L63-70, within-wave declared order L94, CycleError L27-38. `PASS_RECOVERED` correctly at models.py:50; task explicitly warns against the `PASS_RECORDED` typo that appears verbatim in research 03:263 — a real, neutralized hazard. Test-harness cites accurate: `_config` test_handoff_store.py:17-29, handoff path L78-80; `_make_config` test_executor.py:35-54; M1 seam test_executor.py:1904-1965; new-file model test_turn_ledger_concurrency.py:1-17. |

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no defects found)

## Confidence

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 6 (via Bash) | Glob: 0 | Bash: 6

Tool-call-to-checklist ratio: 13 file-reading tool invocations (7 Read + 6 grep-bearing Bash)
for 15 checks — each check maps to specific verified source. No padding: every Read/Bash targeted
a named file/symbol under review (handoff.py, scheduler.py, models.py, executor.py L1395-1535,
process.py L150-245, test_handoff_store.py, test_executor.py L1-60 + L1900-1966,
test_turn_ledger_concurrency.py, research/03, REVIEW.md).

No web research performed (all checks local-file-bound) — Tavily-first rule not triggered.

## Issues Found

None. No CRITICAL, IMPORTANT, or MINOR plan defect.

## Observations (below MINOR threshold — no fix required, no fix applied)

| # | Location | Observation | Why not a finding |
|---|----------|-------------|-------------------|
| O1 | Step 3.2 (M1 test) | Prose says `_run_task_subprocess` is "already imported in the module"; it is actually imported *locally* inside the sibling test `test_run_task_subprocess_uses_task_output_file` (test_executor.py:1912), not module-level (L13-22 block omits it). | Step 3.2 ALSO lists `_run_task_subprocess` among the imports to bring in, so the executor will add a local import in the new test and it works regardless. Self-correcting; not execution-blocking. |
| O2 | Step 2.2 (M3 test) | Prose says "importing `TaskEntry` from `superclaude.cli.sprint.models`" though `TaskEntry` is already module-level imported at test_handoff_store.py:13. | A duplicate/no-op import or simply reusing the in-scope name both succeed. Harmless. |

## Adversarial Axes Sweep (AX-1..AX-5)

- **AX-1 Drift:** Baseline GOAL = "fix exactly M1-M4, no more." No scope drift: the 6 touched files
  map 1:1 to the 4 findings (2 src guards + 4 test surfaces). No paraphrase-weakening of verbs
  (items say "wrap"/"add ceiling"/"guard"/"assert exact output", not "review"/"consider"). The one
  drift HAZARD in the upstream evidence (research 03:263 `PASS_RECORDED` typo) is explicitly
  neutralized by Step 5.3, which pins the correct `PASS_RECOVERED` (models.py:50) — a drift-arrest,
  not a drift-introduction. drift-axis ACTIVE (GOAL verbatim captured from spawn prompt).
- **AX-2 Contradictions:** None. M4 expected outputs are internally consistent and consistent with
  the real scheduler (diamond/linear/cycle/self-edge/unknown-dep all trace correctly through
  scheduler.py L54-104). M2 OPEN QUESTION does not contradict the fix — it resolves the fallback
  value. No frontmatter↔body or AC↔OpenQuestion conflict.
- **AX-3 Omissions:** None. Each src fix (M1/M2/M3) has a paired regression test; M4 test-only by
  design (coverage gap). Verification phase covers full-suite + ruff-format + make-lint (the CI
  gate triad). Blocker-logging fallbacks present per item.
- **AX-4 Weakened criteria:** None. Tests assert exact, observable outcomes (`is None`,
  `pytest.raises(KeyboardInterrupt)`, `== [["A"],["B","C"],["D"]]`, `terminate_called`). No "may"/
  "if applicable"/optional-clause softening below what the REVIEW findings demand. M2's `_waited`
  flag is a concrete observable, not a trivially-true assertion.
- **AX-5 Invented content:** None. Every referenced file/function/line exists in the codebase or
  the research evidence (verified by Read+grep). No invented caching layer, no new module, no
  capability beyond the 4 findings. The `getattr(...,3600)` fallback is the only implementer-choice
  value and is bounded/justified by the OPEN QUESTION, not invented scope.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for frontmatter shape / `---` delimiters (checks 1-2) — did not re-count YAML.
- Relied on rf-qa PASS for template-02 mandatory sections present (check 2).
- Relied on rf-qa PASS for item self-containment / granularity / item count (checks 3-4, 9).
- Relied on rf-qa PASS for TB-1..TB-8 structural-gate additions (placeholder/bounds/adjacency/DAG/XL/format/exec-context-no-paths/per-item-evidence).
- Relied on rf-qa PASS for TF-1 (FAIL-before/PASS-after stated), TF-2 (markers registered), TF-3 (verification phase shape), TF-4 (UV-only).
- Relied on rf-qa TF-5 that the M4 expected outputs were EXECUTED under `uv run` (I did not re-execute the scheduler; I verified the task ENCODES them and that they trace correctly through the real source).

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT and my own tool work was required:**
- **M3 path-reachability** — rf-qa PASS confirmed the line citation; it did NOT confirm that the
  corrupt bytes the M3 test writes actually reach the `json.loads` the fix guards. I Read
  handoff.py:68 (`path = self.config.handoff_file(phase, task)`) and test_handoff_store.py:78-79
  and confirmed the test-write path and the `read()`-read path are the SAME `config.handoff_file`
  key → the guard is exercised. (Spawn-prompt's explicit M3 question.)
- **M1 seam viability** — rf-qa PASS confirmed the test exists; it did NOT confirm the patch seam
  works. I Read test_executor.py:1904-1965 and verified `capture_init` patches
  `superclaude.cli.pipeline.process.ClaudeProcess.__init__`, which is the SAME object the
  production code calls via `from ...process import ClaudeProcess as _Base; _Base.__init__(...)`
  (executor.py:1496-1513) → the patched poll-raises seam fires terminate on the exception path.
- **M2 ceiling-trip mechanics** — rf-qa PASS confirmed the loop line cites; it did NOT confirm the
  fake-proc + patched `monotonic` trips the NEW ceiling. I Read `_poll_with_stall_watchdog`
  (executor.py:1402-1465), confirmed `timeout = getattr(config,"startup_stall_timeout",0)` and
  `underlying = getattr(proc,"_process",None)`, and confirmed the M2 fake (`_process=self`,
  `timeout_seconds=10`, `poll()->None`) passes the disabled-path guard and trips `ceiling=10` under
  the 5s/call iterator → falls to tail `proc.wait()` setting `_waited`.
- **`config.timeout_seconds` non-existence** — rf-qa did not assert this; I grep-verified
  `timeout_seconds` is ABSENT from models.py (SprintConfig) and PRESENT on ClaudeProcess
  (process.py:61) + set at executor.py:1506 → the OPEN QUESTION's AttributeError claim is correct.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

(Equivalent content to `## Self-Audit` above; both heading forms accepted by TEST-009.)
Relied on the 21 inherited PASS rows (checks 1-9, TB-1..TB-8, TF-1..TF-5). For each structural
PASS I ran ≥1 independent semantic counterpart with my own tool engagement (see category (b)
above): M3 path-reachability, M1 seam viability, M2 ceiling mechanics, and `config.timeout_seconds`
non-existence each required Reading the actual source, not relying on rf-qa's structural verdict.

## Recommendations

- Proceed. The task plan is operationally sound and would succeed if executed. No remediation needed.
- (Optional, non-blocking) An executor may tighten the O1/O2 prose, but it is not required —
  execution self-corrects via the import lists the items already specify.

## QA Complete

VERDICT: PASS

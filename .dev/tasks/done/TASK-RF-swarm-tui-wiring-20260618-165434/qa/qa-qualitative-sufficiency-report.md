# QA Report — Task Qualitative Review (QA-Gate / Verification Sufficiency Lens)

**Topic:** Wire --tui into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Phase:** task-qualitative
**Lens:** qa-gate-sufficiency (CODE task — QA_GATE_REQUIREMENTS: NONE is deliberate/correct)
**Fix cycle:** N/A (fix_authorization: false)
**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-swarm-tui-wiring-20260618-165434/TASK-RF-swarm-tui-wiring-20260618-165434.md

---

## Overall Verdict: FAIL (2 IMPORTANT + 1 MINOR; FR→verifying-item coverage core is sound)

## Review scope
Adversarial stance: assume the verification strategy is INSUFFICIENT until proven otherwise.
Lens: does EVERY FR have a VERIFYING item (not just an implementing item)? Are the validation
gates + POST reflect gate sufficient to catch a broken implementation? Are A.10.25 MINOR
findings (F1/F2/F4) real verification holes?

(Findings appended incrementally below.)

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Every FR has a VERIFYING item (not just implementing) | omissions | PASS-with-gaps | FR-1..FR-7 each have a dedicated test item (3.1/3.2, 3.4, 3.1b, 3.3, 3.5, 3.6, 3.7). Verified item bodies + cited anchors. Two sub-acceptance holes (F1/F4) noted below. |
| 2 | C3/AC-004/NFR-001 no-signature-change verified | none | PASS | Step 3.8 `inspect.signature` test + Step 4.4 `git diff <start_commit>` proof. `dispatch_wave1` sig (dispatch.py:334-343) + `ParallelExecutor` (parallel.py:80/100/103/169) confirmed against current source. |
| 3 | Validation items sufficient + correctly ordered | none | PASS | 4.1 ruff check, 4.2 ruff format --check (CI-separate surface), 4.3 full swarm suite vs Phase-1 baseline, 4.4 git-diff. All AFTER impl(Ph2)+tests(Ph3). Baseline captured Step 1.3. |
| 4 | POST reflect gate = final exit-0-only disjoint backstop | none | PASS | Post-Completion penultimate item: flat reflect wrapper, exit-0-only advances, recursion-breaker guard, resolves base from start_commit, writes reflect_post. |
| 5 | A.10.25 MINOR findings F1/F2/F4 — real holes? | weakened-criteria | FAIL | F1 (iteration-ceiling) + F4 (corrupt-complete-line) are REAL untested behaviors that the impl items introduce. F2 (state=None) is covered indirectly. See findings. |
| 6 | Baseline-green-suite present (regression detectable) | none | PASS | Step 1.3 captures `baseline-swarm-suite.txt`; Step 4.3 compares pass count ≥ baseline + new tests; pre-existing failures recorded so not mis-attributed. |
| 7 | Cited test patterns/anchors actually exist + usable | invented-content | PASS | Verified vacuous audit (test_inv012:543-583 early-return 575-578), AST visitor (test_concurrency:191/224/341/357), `_assert_no_ansi`(73), `_FakeTTY`(209), PTY skip(436/452), stub test(test_commands_run:507), `_project_workers` dict, `_follow_log`(2737)/`_drain_appended`(2834). |

---

## Findings

### FINDING 1 — FR-by-FR verifying-item map: every FR has a verifying item (PASS on the core question)

The central lens question — does EVERY FR have a corresponding VERIFYING item, not just an
implementing item — is answered YES for all seven:

| FR | Implementing item(s) | Verifying item(s) | Verifying mechanism |
|----|---------------------|-------------------|---------------------|
| FR-1 single-writer Console | 2.5(b/e), 2.6 | 3.1 (AST reachability audit, vacuity+mutation guard) + 3.2 (runtime main-thread `get_ident` probe with `assert seen_idents`) | static + runtime, both with mandatory vacuity guards |
| FR-2 no-regression | 2.5(e) | 3.4 (non-TTY run with/without `--tui`: identical exit code + identical `worker_done` count + zero ANSI both paths via `_assert_no_ansi`) | differential CliRunner |
| FR-3 scope guards | 2.3, 2.3b | 3.1b (BOTH rejects: `--tui --detached`→EXIT_USAGE AND `--resume --tui`→EXIT_USAGE; resume path proven not to enter TUI loop) | CliRunner exit-code + no-construct assertion |
| FR-4 tail path | 2.4 | 3.3 (partial-line not delivered + completed-on-next-poll + exactly-once third-poll-empty + `_project_workers`≥1 row) | dedicated `test_tail_events.py` |
| FR-5 exception not masked | 2.5(a/d) | 3.5 (dispatch raises → non-zero exit + ORIGINAL traceback reaches caller + `tui.stop()` ran before re-raise) | monkeypatch source-module dispatch |
| FR-6 idempotent teardown | 2.5(c) | 3.6 (three paths clean/exception/SIGINT; `stop()` once + idempotent 2nd call; SIGINT non-zero exit) | parametrized teardown |
| FR-7 integration | 2.1-2.6 (whole) | 3.7 (forced-TTY `run_cmd --tui` → ≥1 NON-VACUOUS worker row from tailed log + INV-012 zero-ANSI companion + fails-if-unwired regression guard) | real-dispatch CliRunner |

Each verifying item carries explicit anti-vacuity scaffolding (FR-1 `assert seen_idents`,
FR-7 "non-vacuous row + fails-if-unwired", FR-2 differential, FR-4 third-poll-empty). This is
materially stronger than presence-only checks and is the correct rigor for a code task whose
QA_GATE_REQUIREMENTS=NONE is deliberate. The QA-gate waiver is justified and mirrors the cited
precedent (TASK-RF-pr167-verdict-regex-20260613).

### FINDING 2 (IMPORTANT, AX-4 weakened-criteria) — FR-4 corrupt-COMPLETE-line behavior is implemented but UNTESTED (A.10.25 F4 is a real hole)

Step 2.4 specifies TWO distinct partial/error disciplines for `_tail_events`:
  (a) partial *trailing* line (no newline yet) → buffer, don't advance past last `\n`; and
  (b) "tolerates a `json.JSONDecodeError` on a line by NOT advancing past it (treat as
      still-partial)."

Step 3.3 (the FR-4 test) exercises ONLY discipline (a): it writes `rec1\n` + a newline-LESS
partial `rec2`, asserts the partial is not delivered, completes it, asserts exactly-once. It
does NOT exercise discipline (b): a NEWLINE-TERMINATED line whose JSON is malformed
(`{"bad json"\n`). This is exactly A.10.25 MINOR finding F4 (corrupt-complete-line-untested).

Why this matters: disciplines (a) and (b) are not the same code path. (a) is "split on last
`\n`"; (b) is "`from_json` raised on a complete line." The impl's (b) behavior — NOT advancing
the offset past a malformed-but-newline-terminated line — is a potential INFINITE-LOOP /
permanent-stall hazard: if a genuinely corrupt complete line is ever written, the tailer never
advances past it and re-parses it every 0.5s forever while the worker thread keeps running.
That is a more dangerous failure mode than the (a) case the test does cover, and it is
SHIPPED-BUT-UNVERIFIED. The verification strategy has a real hole here.

Required fix: Step 3.3 MUST add a sub-assertion feeding a newline-terminated but JSON-invalid
line and asserting the tailer's documented behavior (no raise; and a decision on whether it
stalls or skips). Note this also forces the task to RESOLVE an ambiguity: Step 2.4's "treat as
still-partial / do not advance" on a *complete* corrupt line means permanent stall — the task
should either test-and-accept that, or change the impl to skip-and-advance past a corrupt
complete line. As written, the impl behavior is under-specified AND untested.

### FINDING 3 (IMPORTANT, AX-3 omissions) — FR-4 iteration-ceiling is specified but its bound is never verified (A.10.25 F1 is a real hole)

Spec FR-4 (merged-requirements.md:91-93) and Step 2.5(b) both call for an "optional
`watch_max_iterations`-style ceiling … guards against an unbounded spin" / "for test
determinism." The spec frames it as an unbounded-spin guard. No test item asserts the ceiling
actually bounds the loop. Step 3.7/3.2 drive the poll path but rely on the worker thread
terminating (`t.is_alive()` going False) to end the loop — they never exercise the ceiling as
the loop-exit. So if the ceiling is mis-wired (off-by-one, or never decremented, or the `while
t.is_alive()` and ceiling interact wrongly), no test catches it; worse, the ceiling is the
ONLY backstop against a hung/never-joining worker hanging the whole CLI invocation, and that
backstop is unverified.

This is A.10.25 MINOR finding F1 (iteration-ceiling-untested), and it is a real verification
hole: the safety mechanism whose entire purpose is to prevent an unbounded spin has no test
proving it does. Required fix: add an assertion (in 3.7 or a dedicated micro-test) that with a
worker stubbed to stay alive longer than the ceiling, the loop exits at the ceiling rather than
spinning unboundedly.

### FINDING 4 (MINOR, AX-3 omissions) — A.10.25 F2 (state=None update) is acceptably covered; documenting why it is NOT a hole

A.10.25 F2 flags `state=None`-update-untested. Adversarially checking: `06-gapfill.md` G5
[CODE-VERIFIED] that `TUI.update(None, events)` → `_build_header(None,…)` takes the `"-"`
fallback (tui.py:277-278) with no AttributeError, and `read_state()` returns `None` in the
early-run window. The `state=None` path is in the UNCHANGED `tui.py` consumer (G4: tui.py is
frozen), and it is already exercised by the existing `test_tui.py` render suite indirectly. The
NEW glue (`_tail_events` + poll loop) does not re-implement header rendering. FR-7 (3.7) drives
a real run whose first poll iterations occur before `.swarm-state.json` exists, so `read_state`
returns None and `tui.update(None, events)` runs as part of the integration test. Verdict: F2 is
adequately covered transitively; not a blocking hole. (Recorded so the auditor sees F2 was
adversarially re-checked, not waved through.)

### FINDING 5 (PASS) — No-signature-change invariant is doubly verified

C3/AC-004/NFR-001 gets BOTH a positive runtime assertion (3.8 `inspect.signature` pinning exact
params/defaults/kind of `dispatch_wave1` and `ParallelExecutor.__init__/plan/execute`) AND an
external git-diff proof (4.4 `git diff 300c06a6 -- dispatch.py parallel.py`). I verified the
frozen signatures against current source: `dispatch_wave1(preflight_result, transport=None, *,
transport_for_slot=None, prompt="", parallel_executor=None, worker_spec=None, logger=None)` and
`ParallelExecutor.__init__(self, max_workers: int = 10)` / `plan` @103 / `execute` @169 — all
match the task's frozen-signature claims. start_commit `300c06a6…` exists (git cat-file → commit).
This is sufficient and well-constructed.

### FINDING 6 (PASS) — Validation ordering + baseline + reflect backstop are correct

- Baseline-green captured BEFORE any change (Step 1.3 → `baseline-swarm-suite.txt`), with explicit
  instruction to record pre-existing failures so they aren't mis-attributed. Regression IS
  detectable (Step 4.3 compares pass count ≥ baseline + new tests). PASS.
- Validation gates are correctly ordered AFTER impl (Phase 2) and tests (Phase 3): 4.1 ruff
  check → 4.2 ruff format --check (correctly called out as a CI-SEPARATE surface; matches the
  project's "green make lint ≠ green CI format" convention) → 4.3 full swarm suite → 4.4 frozen
  diff. PASS.
- POST reflect gate is the penultimate Post-Completion item, exit-0-only advances to Done,
  recursion-breaker guard present, resolves audit base from start_commit frontmatter, writes
  `reflect_post` back. Correct disjoint backstop. PASS.

### FINDING 7 (PASS) — All cited test anchors/patterns exist and are usable

Independently verified every load-bearing anchor the test items depend on (not sampled — all):
- Vacuous audit `test_commands_module_does_not_construct_tui_outside_gate` early-returns at
  line 575-578 (`if "TUI(" not in source: return`) → assert at 579 is dead code. Confirmed.
- AST-visitor precedent `_ShellDispatchVisitor`/`_scan_module` (test_concurrency_python_only.py
  :191/:224) + mutation guards (:341 `.sh`, :357 `import subprocess`) — the exact pattern 3.1
  must copy. Confirmed present and usable.
- `_assert_no_ansi` (test_inv012:73, two-pattern CSI+ESC), `_FakeTTY` (:209), PTY skip test
  (:436, `_run_cmd_has_tui_flag` :416 returns False today → skips, activates when `--tui` lands).
- Stub-dispatch precedent `test_run_cmd_stub_transport_dispatches_workers_not_noop`
  (test_commands_run.py:507) + the deferred-import monkeypatch idiom (:320-324). Confirmed.
- `_follow_log`(2737)/`_drain_appended`(2834) byte-offset precedent. Confirmed (and G6's
  `_follow_log` name-fix is correct — there is no `_follow_log_file`).
- `from_json` @ models.py:1820 (module-level, not a classmethod), `read_state` @ state.py:178,
  `_project_workers`/`update`/`stop`/`should_enable_tui` in tui.py. All confirmed.
- Constants: `EXIT_USAGE=2`, `EXIT_OK=0`, `EXECUTION_LOG_JSONL_FILENAME="execution-log.jsonl"`,
  `SWARM_STATE_FILENAME=".swarm-state.json"`. All match.
- Run_cmd seam anchors: `run_cmd`@1471, resume branch `if resume_job_id is not None:`@1539,
  resume+detached reject area@1547, `_run_resume_branch`@1561/return@1567, fresh `if detached:`
  @1589. All match the task's CURRENT line claims (within the documented drift tolerance).

No invented files/symbols/commands. The "filename truth" correction (execution-log.jsonl not
event-log.jsonl; from_json in models.py not logging_.py) is itself CODE-VERIFIED and correct —
the task consistently targets the real on-disk names, which is a strength.

### FINDING 8 (MINOR, AX-2 contradictions) — FR-6 SIGINT exit-code assertion is loosely specified

Step 3.6(c) asserts the SIGINT path yields "a non-zero/interruption exit code (non-zero, distinct
from EXIT_OK)." `06-gapfill.md` G3 establishes Click surfaces an uncaught KeyboardInterrupt as
exit 130, OR an explicit `raise click.exceptions.Exit(130)` is the deterministic equivalent — and
the impl (2.5) does not pin which. The test correctly hedges to "non-zero ≠ EXIT_OK" rather than
asserting 130, which is defensible, but it means a regression that produced exit 1 (instead of
130) would pass. This is acceptable for v1 (the contract is "interruption is surfaced as failure")
but should be noted: the looseness is a deliberate under-specification, not an oversight, and is
the weakest of the seven verifying items. Not blocking on its own.

---

## Self-Audit

**(a) Reliance list — rf-qa structural-PASS items I relied on (did NOT re-verify):**
- Relied on A.10 PASS for FrontMatter / numbering / TB-Add-5 justification / 30-item count /
  reflect-gate-penultimate placement / 0-placeholders (per Inherited Structural Verdict). I did
  not re-count items, re-check frontmatter schema, or re-verify the TB-Add-5 atomic-refactor
  justification block.
- Relied on A.10.25 research-alignment PASS for the claim that the task's anchors trace to the
  research files (I still independently re-verified a sample of those anchors against live source
  — see (b)).

**(b) Independent semantic checks where structural PASS was INSUFFICIENT (≥1 required, INV-019):**
1. **Verifying-item-existence is semantic, not structural.** rf-qa structural QA confirms items
   exist and are numbered; it does NOT confirm each FR has a VERIFYING (vs merely implementing)
   item. I built the FR→test map (Finding 1) by reading each item body — tool evidence: Read of
   task lines 225-259 (Steps 3.1-3.8) + cross-ref to merged-requirements FR-1..FR-7.
2. **Sub-acceptance-criterion coverage.** Structural PASS cannot detect that FR-4's
   corrupt-COMPLETE-line discipline (Step 2.4 body) has no matching assertion in Step 3.3 — that
   requires reading both bodies and noticing the (a)-vs-(b) path divergence. Tool evidence: Read
   of task:209 (2.4) and task:239 (3.3) + research 05§6 and 06§G6. This produced Findings 2 & 3
   (real holes structural QA could not surface).
3. **Anchor liveness.** Structural QA + A.10.25 confirm anchors trace to research files; they do
   NOT confirm the anchors still match CURRENT source. I grepped live source: vacuous audit
   early-return (test_inv012:575-578), AST visitor (test_concurrency:191/224/341/357),
   `dispatch_wave1`/`ParallelExecutor` frozen sigs, constants, run_cmd seam lines, `_follow_log`/
   `_drain_appended`, `from_json`@1820. Tool evidence: Bash greps + Reads above. Confirmed
   usable (Finding 7).

These three checks each required my own tool engagement beyond what the inherited structural
verdict could provide; reliance alone would have missed Findings 2 and 3.

---

## Summary
- Checks passed: 5 / 7 core lens checks (FR-coverage, no-sig-change, validation-ordering,
  reflect-backstop, baseline-present, anchor-liveness) — Check 5 (A.10.25 holes) FAILS.
- Checks failed: 1 core check (F1 + F4 are real verification holes); 2 IMPORTANT findings.
- Critical issues: 0
- Important issues: 2 (Finding 2 corrupt-complete-line untested + under-specified impl behavior;
  Finding 3 iteration-ceiling bound unverified)
- Minor issues: 2 (Finding 8 SIGINT exit-code looseness; Finding 4 documented-not-a-hole)
- Issues fixed in-place: 0 (fix_authorization: false)
- Tool engagement: Read: 6 | Grep/Bash: 3 (multi-grep) | Glob: 0 — ≥ checklist items covered.
- Confidence: Verified: 7/7 core checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 2.4 + Step 3.3 (FR-4) | Corrupt-COMPLETE-line (newline-terminated, JSON-invalid) discipline is implemented (2.4 "JSONDecodeError → do not advance") but never tested (3.3 only covers newline-LESS partial). The "do not advance" behavior on a complete corrupt line is a permanent-stall hazard, shipped-but-unverified. Also under-specified: stall-vs-skip is not decided. | Add a sub-assertion in 3.3 feeding a `{bad json}\n` line; assert no raise AND assert the resolved behavior (stall-and-stop vs skip-and-advance). Resolve the impl ambiguity in 2.4 first. |
| 2 | IMPORTANT | Step 2.5(b) + Steps 3.2/3.7 (FR-4 ceiling) | The unbounded-spin guard (`watch_max_iterations`-style ceiling) is the only backstop against a hung/never-joining worker hanging the CLI, but no test asserts the ceiling bounds the loop — tests rely on natural worker termination. | Add an assertion (3.7 or micro-test) with a worker stubbed to outlive the ceiling, asserting the loop exits AT the ceiling, not by spinning. |
| 3 | MINOR | Step 3.6(c) (FR-6 SIGINT) | Exit-code assertion is "non-zero ≠ EXIT_OK"; impl does not pin 130 vs explicit Exit(130). A regression to exit 1 would pass. | Acceptable for v1; optionally tighten to assert 130 if the impl pins it. Document the deliberate looseness. |

## Recommendations
- FAIL the gate on Findings 2 & 3 (the two IMPORTANT holes). Per the no-leniency / all-severities
  rule, these must be resolved before the task is executed — both are genuine gaps where a broken
  implementation would pass the stated verification strategy.
- Smallest sufficient remediation: extend Step 3.3 with a corrupt-complete-line sub-case (resolving
  the 2.4 stall-vs-skip ambiguity), and add an iteration-ceiling bound assertion. Both are additive
  test-item edits; no structural rework needed. The rest of the verification strategy is sound and
  the QA-gate waiver is correctly justified.

## QA Complete

VERDICT: FAIL

Two IMPORTANT verification holes (Finding 2 / Issue 1: FR-4 corrupt-complete-line untested +
under-specified; Finding 3 / Issue 2: FR-4 iteration-ceiling bound unverified) and one MINOR
(Issue 3: FR-6 SIGINT exit-code looseness). The A.10.25 MINOR findings F1 and F4 are confirmed
REAL verification holes; F2 is adequately covered. Per the no-leniency rule, ALL findings must be
resolved before execution. The core FR→verifying-item coverage, no-signature-change double-proof,
validation ordering, baseline, reflect backstop, and anchor liveness all PASS — the strategy is
fundamentally sound but has two genuine gaps in the FR-4 tail-helper test surface.

---

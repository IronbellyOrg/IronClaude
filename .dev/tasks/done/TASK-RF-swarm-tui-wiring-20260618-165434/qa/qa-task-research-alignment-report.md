# QA Report: Task-Research Alignment

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-06-18
**Task:** TASK-RF-swarm-tui-wiring-20260618-165434
**Track Goal:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Stance:** ADVERSARIAL — assume builder dropped/misrepresented research findings.

---

## Method

Read all 6 research files (01-06), the driving spec (`merged-requirements.md`),
and the full task file (370 lines). Independently re-verified the highest-value
adversarial anchors against the live code:

- `from_json` location: `grep` → `models.py:1820` (NOT logging_.py — confirmed
  logging_.py only has `event-log.jsonl` in docstrings at lines 7/44/92, no `from_json` def).
- Filename constants: `EXECUTION_LOG_JSONL_FILENAME = "execution-log.jsonl"` at
  `commands.py:99`; `SWARM_STATE_FILENAME = ".swarm-state.json"` at `commands.py:85`;
  `EXIT_USAGE = 2` at `commands.py:190`.
- Seam anchors: `run_cmd` @1471, resume branch `if resume_job_id is not None:` @1539,
  resume+detached reject `if detached:` @1547, `_run_resume_branch(...)` @1561,
  `_resolve_input_mode(...)` @1581, fresh `if detached:` @1589, fresh
  `dispatch_wave1(` @1807, resume `dispatch_wave1(` @2264. All match research 01.

The CODE-CONTRADICTED resolutions are ACCURATE against live code, and the task targets
the correct (non-stale) names.

---

## Checklist 1 — Per-research-file finding -> task-item coverage

### 01-run-cmd-seam -> insertion anchors

| Research anchor (01) | Task item acting on it | Status |
|---|---|---|
| `--tui` option after :1469, before `@auto_inject_guard_option` | Step 2.1 | COVERED |
| `tui: bool` param before `auto_inject_guard` (:1485) | Step 2.2 | COVERED |
| `--tui --detached` reject @ ~1581 (mirror resume+detached :1547) | Step 2.3 | COVERED |
| `--resume --tui` reject in resume branch before `_run_resume_branch` | Step 2.3b | COVERED |
| fresh `dispatch_wave1(...)` @1807-1813 -> onto worker thread | Step 2.5 | COVERED |
| post-dispatch continuation @1826 runs after join+re-raise | Step 2.5(d) | COVERED |
| `state_output_dir` @1726/1731 as poll read-root | Step 2.5(b), gate | COVERED |
| resume dispatch @2264 LEFT UNTOUCHED | Key Constraints + Phase 2 preamble | COVERED |
| constants (SWARM_STATE_FILENAME, EXECUTION_LOG_JSONL_FILENAME, EXIT_*) | Step 1.3 inventory | COVERED |

All 01 anchors have an acting item. PASS.

### 02-reader-contracts -> reader/consumer contracts

| Contract (02) | Reflected in | Status |
|---|---|---|
| `read_state(path) -> Optional[SwarmState]`, None if missing | Step 2.5(b) reads `read_state(... / ".swarm-state.json")` | COVERED |
| `from_json` @ models.py:1820 (NOT logging_.py:46) | Step 2.4 + Key Constraints "Filename truth" | COVERED |
| `EventRecord` dataclass (models.py:1209) | Step 2.4, Step 3.3, Step 3.7 | COVERED |
| `_project_workers` (tui.py:145), worker_*-only | Step 3.3, Step 3.7 (assert >=1 row) | COVERED |
| `should_enable_tui(flag, stream)` (tui.py:74) | Step 2.5(b), Step 3.2/3.7 seam | COVERED |
| `execution-log.jsonl` filename truth (NOT event-log.jsonl) | Step 2.4 + Key Constraints + every test | COVERED |
| frozen `dispatch_wave1` signature (dispatch.py:334-343) | Step 1.3 baseline, Step 3.8, Step 4.4 | COVERED |
| frozen `ParallelExecutor` (parallel.py:80/100/103/169) | Step 1.3 baseline, Step 3.8, Step 4.4 | COVERED |
| `TUI.stop()` idempotent (tui.py:230-234) | Step 2.5(c), Step 3.6 | COVERED |

All 02 contracts reflected. PASS.

### 03-patterns-conventions -> idioms

| Idiom (03) | Reflected in | Status |
|---|---|---|
| Click `is_flag` 3-arg decorator (mirror `--detached`) | Step 2.1 | COVERED |
| `UsageError`/`EXIT_USAGE` reject idiom | Step 2.3, 2.3b | COVERED |
| deferred (function-local) import | Step 2.4 (`from_json`), Step 2.5(b) (TUI/state) | COVERED |
| threading `daemon=False` (FR-5 override of executor.py daemon=True) | Step 2.5(a) explicit `daemon=False` | COVERED |
| byte-offset tail (mirror `_drain_appended`) | Step 2.4 | COVERED |
| poll-loop ceiling `watch_max_iterations` (>= semantic) | Step 2.5(b) "optional ceiling" | PARTIAL — see Finding F1 |
| `finally:` teardown template | Step 2.5(c) | COVERED |

### 05-test-verification -> test recipes

| Recipe (05) | Reflected in | Status |
|---|---|---|
| FR-1 AST audit tightening of the vacuous test (replace early-return) | Step 3.1 | COVERED |
| FR-1 runtime get_ident probe + mandatory vacuity guard | Step 3.2 | COVERED |
| FR-7 forced-TTY monkeypatch + stub emission (>=1 row, no-ANSI companion) | Step 3.7 | COVERED |
| FR-4 partial-line / exactly-once fixture | Step 3.3 | COVERED |
| FR-2 no-regression CliRunner twice (off vs on) | Step 3.4 | COVERED |
| mutation/vacuity guards mandatory | Step 3.1 (mutation guard), 3.2 (vacuity) | COVERED |

### 06-gapfill -> gap resolutions

| Gap resolution (06) | Reflected in | Status |
|---|---|---|
| G1 daemon=False + explicit join() | Step 2.5(a) | COVERED |
| G2 `state_output_dir is None` guard | Step 2.5(b) gate, Key Constraints FR-2 | COVERED |
| G3 SIGINT -> finally:stop first, then propagate, exit-130/non-zero | Step 2.5(c), Step 3.6(c) | COVERED |
| G4 tui.py UNCHANGED (caller-side get_ident assertion) | Step 2.6, Source Areas, Key Constraints | COVERED |
| G5 state=None header safe | (implicit — render path; not a separate item) | PARTIAL — see Finding F2 |
| G6 `_tail_events` module-level in commands.py + signature | Step 2.4 | COVERED |

---

## Checklist 2 — CODE-CONTRADICTED resolutions honored

The task acts on BOTH stale-name resolutions correctly:

- **`execution-log.jsonl` (NOT event-log.jsonl):** Key Constraints "Filename truth"
  explicitly states the spec's `event-log.jsonl` is STALE/[CODE-CONTRADICTED] and that
  ALL items + tests target `execution-log.jsonl`. Verified in Step 2.4, 3.3, 3.4, 3.7.
  No task item uses `event-log.jsonl`.
- **`from superclaude.cli.swarm.models import from_json` (NOT logging_.py):** Step 2.4
  and Key Constraints both pin `models.py:1820`. No item references `logging_.py:46`.

Independently re-verified against live code (grep). PASS — no stale-name leakage.

---

## Checklist 3 — Fabrication check (adversarial)

Scanned every task item for files/symbols/anchors not present in research or code.
Findings: NO fabricated helpers, tests, or constants. Spot-checks:

- `_tail_events(path: Path, offset: int) -> tuple[list[EventRecord], int]` — matches
  06-gapfill G6 verbatim.
- `_drain_appended` / `_follow_log` precedent — 06-gapfill G6 explicitly fixes the
  02 mislabel `_follow_log_file` -> `_follow_log`; Step 2.4 uses the CORRECTED name
  `_follow_log` and even calls out the mislabel. (good fidelity)
- `_assert_no_ansi` @ test_inv012_tui_opt_in.py:73 — matches 05 §2.
- `test_run_cmd_stub_transport_dispatches_workers_not_noop` @ test_commands_run.py:507 —
  matches 05 §3/§5.
- `stub-model-00`, `worker_done`x3 for bare-review — matches 05 §5 [CODE-VERIFIED].
- `_ShellDispatchVisitor` AST precedent in test_concurrency_python_only.py — matches 05 §1.

No fabrication detected. PASS.

---

## Checklist 4 — All 7 FRs have >=1 implementing AND >=1 verifying item

| FR | Implementing item(s) | Verifying item(s) | Status |
|---|---|---|---|
| FR-1 single-writer + audit | Step 2.5(a) thread topology, Step 2.6 get_ident assertion | Step 3.1 (AST audit), Step 3.2 (runtime get_ident) | PASS |
| FR-2 no-regression | Step 2.5(b)(e) gate + byte-identical fallback | Step 3.4 | PASS |
| FR-3 BOTH rejects | Step 2.3 (detached), Step 2.3b (resume) | Step 3.1b (dual-reject test) | PASS |
| FR-4 tail | Step 2.4 `_tail_events` | Step 3.3 | PASS |
| FR-5 exception | Step 2.5(a)(d) box + post-stop re-raise | Step 3.5 | PASS |
| FR-6 teardown | Step 2.5(c) finally:stop | Step 3.6 (3 paths) | PASS |
| FR-7 integration | Step 2.5 full glue (the seam under test) | Step 3.7 | PASS |

All 7 FRs doubly covered. PASS. (Plus C3/AC-004/NFR-001 frozen-signature gets Step 3.8
inspect.signature test + Step 4.4 git-diff proof — a third verification surface.)

---

## Checklist 5 — Research caveats reflected in verification criteria

| Caveat | Reflected? | Where |
|---|---|---|
| daemon=False non-truncation rationale | YES | Key Constraints FR-5; Step 2.5(a) |
| state_output_dir-None byte-identical fallback | YES | Key Constraints FR-2; Step 2.5(b)(e); Step 3.4 |
| tui.py-unchanged constraint (caller-side assertion) | YES | Step 2.6; Source Areas; Step 3.8 not needed (G4) |
| C3/AC-004 no-signature-change | YES | Step 3.8 inspect.signature + Step 4.4 git-diff |
| from_json raises JSONDecodeError on partial line -> buffer to newline | YES | Step 2.4 + Step 3.3 |
| should_enable_tui deferred-import -> patch SOURCE module | YES | Step 3.2, 3.7 (with module-top fallback noted) |
| unregistered `tui` marker breaks --strict-markers -> leave unmarked | YES | Phase 3 preamble + every test item "unmarked" |

All caveats land in verification criteria. PASS.

---

## FINDINGS (adversarial — >=3 required)

### Finding F1 — Poll-loop iteration ceiling under-specified (MINOR)

- **Severity:** MINOR
- **Source:** 03-patterns-conventions §6 + spec FR-4 ("an optional iteration ceiling
  mirroring `watch_max_iterations` guards against an unbounded spin").
- **Issue:** Research 03 §6 gives an EXACT precedent (`commands.py:2583-2613`, the
  `status --watch` loop) with the specific `>=` ceiling semantic and the
  `try/except KeyboardInterrupt` wrap. Step 2.5(b) reduces this to "an optional
  `watch_max_iterations`-style ceiling for test determinism" — it does NOT pin the
  `iterations >= ceiling: break` shape, does NOT require the ceiling be reachable from a
  test, and no test item asserts the ceiling actually bounds the loop. FR-4's acceptance
  ("guards against an unbounded spin") therefore has an implementing mention but NO
  verifying item. A future regression making the loop spin unbounded would not be caught.
- **Why it matters (adversarial):** the task represents the ceiling as "optional," which
  softens a research-identified determinism guard into a nice-to-have. Tests 3.2/3.7 drive
  the poll loop via a worker that completes fast (stub), so they rely on `t.is_alive()`
  going False — if that gate ever wedged, no test bounds it.
- **Recommendation:** add to Step 2.5(b) the explicit `iterations >= ceiling: break`
  shape, and add one assertion (in Step 3.7 or 3.2) that the loop terminates under a
  bounded ceiling. Not blocking — the `while t.is_alive()` primary exit is sound and the
  non-daemon join guarantees termination; this is a hardening gap, not a correctness gap.

### Finding F2 — G5 (state=None header safe) has no verifying assertion (MINOR)

- **Severity:** MINOR
- **Source:** 06-gapfill G5 ([CODE-VERIFIED] `_build_header` None-safe; `read_state`
  returns None in the early-run window before `.swarm-state.json` exists).
- **Issue:** G5 is a real runtime caveat: the poll loop calls `read_state(...)` which
  returns `None` for the first iteration(s) before the worker writes the state file, and
  `tui.update(None, events)` must not crash. The task acts on it only implicitly (Step
  2.5(b) passes whatever `read_state` returns to `tui.update`). NO test item asserts the
  `state is None` -> `tui.update(None, ...)` path renders without `AttributeError`. The
  FR-7 stub run may write state fast enough that `read_state` never returns None during the
  test, so the None-window is plausibly never exercised — the exact early-run condition G5
  flags as the realistic case.
- **Why it matters (adversarial):** the research did the work to verify None-safety; the
  task drops the verification, so the most likely real-world first-frame condition is
  untested. If `tui.py` were later changed to dereference `state` unguarded, no swarm test
  would catch it on the `run_cmd -> tui` seam.
- **Recommendation:** add a one-line assertion to Step 3.7 (or 3.3) that
  `tui.update(None, events)` / a `read_state`-returns-None first iteration does not raise.
  Cheap, directly closes the G5 caveat. Not blocking (G5 is [CODE-VERIFIED] safe today).

### Finding F3 — Frozen `dispatch_wave1` call-site preservation vs signature-only proof (MINOR)

- **Severity:** MINOR
- **Source:** 02-reader-contracts §8 verbatim signature vs Step 3.8 / Step 2.5(a) call site.
- **Issue:** 02 §8 records the frozen `dispatch_wave1` signature verbatim. Step 3.8 +
  Step 4.4 prove the DEFINITION (signature + git-diff) is unchanged. But the fresh-run
  CALL site (research 01 §5) uses only kwargs `transport_for_slot`, `prompt`, `worker_spec`,
  `logger` — it does NOT pass `transport` or `parallel_executor`. No item ASSERTS the call
  kwargs are byte-identical; only Step 2.5(a)'s prose ("EXACT unchanged kwargs") guards it.
  A careless executor could add a kwarg without tripping Step 3.8 (which tests the def, not
  the call).
- **Why it matters (adversarial):** signature-frozen != call-site-frozen. FR-2's
  byte-identical guarantee leans on the call being identical, not just the def.
- **Recommendation:** effectively MITIGATED — Step 3.4 (FR-2 no-regression) already asserts
  identical `worker_done` count + exit code between off/on paths, which would catch a
  behavior-changing kwarg. Downgrade to observational; Step 2.5(a) prose is adequate.

### Finding F4 — `_tail_events` JSONDecodeError-non-advance branch implemented but untested (MINOR)

- **Severity:** MINOR
- **Source:** 06-gapfill G6 ("if a line fails `from_json`, do NOT advance past it") + 05 §6.
- **Issue:** Step 2.4 implements TWO partial-line behaviors: (a) buffer to last `\n`
  (partial trailing line without a newline), and (b) on `JSONDecodeError` for a
  newline-terminated-but-corrupt line, do NOT advance. Step 3.3 tests branch (a)
  thoroughly but constructs NO newline-terminated malformed line to exercise branch (b).
  The branches differ: (a) is a half-written line; (b) is a complete-but-corrupt line.
- **Why it matters (adversarial):** G6 explicitly calls out branch (b); Step 2.4 implements
  it; Step 3.3 never exercises it. An implemented-but-untested branch could silently
  drop or infinite-loop on a corrupt line with no test catching it.
- **Recommendation:** extend Step 3.3 with a 4th sub-case (newline-terminated corrupt JSON),
  asserting no raise + chosen discipline. Minor — the realistic mode (truncation mid-append)
  is covered by branch (a).

### Finding F5 — SIGINT tested via injected KeyboardInterrupt, not the join() window (OBSERVATIONAL)

- **Severity:** OBSERVATIONAL (fidelity note, not a gap)
- **Source:** 06-gapfill G3 vs Step 3.6(c).
- **Issue:** G3 documents the realistic SIGINT window as the poll loop and notes a SIGINT
  during `t.join()` behaves identically (finally still fires). Step 3.6(c) simulates SIGINT
  by raising `KeyboardInterrupt` in the poll loop's first iteration — a faithful simulation
  of the documented primary window. It does not separately exercise the join()-window
  SIGINT, which G3 states shares behavior.
- **Recommendation:** none. Recorded for completeness.

---

## Cross-cutting observations (positive — fidelity strengths)

- The task IMPROVES on research where research disagreed with itself: it adopts 06-gapfill's
  `_follow_log` name (fixing 02's `_follow_log_file` mislabel) and explicitly annotates the
  correction in Step 2.4. Good adversarial hygiene by the builder.
- FR-3's SECOND acceptance criterion (resume+tui reject) — which research 01 §4 flagged as
  "a task-design decision, not an FR requirement" — is nonetheless given a full implementing
  item (2.3b) AND a verifying test (3.1b), explicitly asserting "the resume path never enters
  the TUI loop." MORE rigorous than research minimally required. No drop.
- The QA-gate waiver (QA_GATE_REQUIREMENTS: NONE) is grounded in research 04 Example A
  (TASK-RF-pr167-verdict-regex) and recorded with rationale — not silently omitted.

---

## VERDICT: PASS

All 6 research files' key findings have corresponding acting task items; all 7 FRs have
>=1 implementing AND >=1 verifying item; both [CODE-CONTRADICTED] stale-name resolutions
(`execution-log.jsonl`, `models.py:from_json`) are honored and independently re-verified
against live code; no fabricated files/symbols/anchors were found; all major research
caveats land in verification criteria.

The 5 findings are all MINOR/OBSERVATIONAL hardening/test-coverage gaps, NOT alignment
drops or fabrications. None block execution:

- **F1** (poll-loop ceiling): correctness backstopped by `while t.is_alive()` + non-daemon
  join; ceiling is a determinism nicety.
- **F2** (state=None untested): G5 is [CODE-VERIFIED] safe today; missing test is a
  regression-guard gap, not a present defect.
- **F3** (call-site freeze): mitigated by Step 3.4's behavior-equivalence assertions.
- **F4** (corrupt-line branch untested): realistic truncation mode IS tested.
- **F5**: observational only.

**Severity rollup:** CRITICAL: 0 | IMPORTANT: 0 | MINOR: 4 | OBSERVATIONAL: 1.

**Recommendation:** PASS as-is. Optionally fold F1+F2+F4's one-line test additions into
Step 3.3/3.7 to close the three hardening gaps — none require re-architecting any item.

# Reviewer Card — UC-1 Pre-Execution COVERAGE Lens

- **Reviewer role:** Tier-2 reflect reviewer (COVERAGE lens) — spec→tasklist coverage matrix
- **Spec:** `/config/workspace/IronClaude/.dev/brainstorms/swarm-tui-wiring/merged-requirements.md`
- **Tasklist:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-swarm-tui-wiring-20260618-165434/TASK-RF-swarm-tui-wiring-20260618-165434.md`
- **Date:** 2026-06-18
- **Read basis:** both files read in full this turn (spec 205 lines; tasklist 374 lines).

---

## Extraction Summary

### Pass 1 — Labeled requirements (8)
FR-1 (single-writer Console topology), FR-2 (INV-012 gate + non-TUI no-regression), FR-3 (scope guards: detached + resume), FR-4 (event/state read path, byte-offset tail), FR-5 (thread exception not masked), FR-6 (idempotent teardown on every exit), FR-7 (non-vacuous run→tui integration test). Plus **NFR-001/AC-004/C3** (frozen `dispatch_wave1` + `ParallelExecutor` signatures) — referenced via the spec frontmatter `unchanged_by_design` block (lines 19-22) and the "No change to dispatch_wave1 or ParallelExecutor" assertion (spec lines 38, 137-138).

### Pass 2 — Inferred imperatives the labeled IDs underspecify (5)
- **INF-001** — Non-daemon worker thread. *Quote:* "Worker thread is **non-daemon** with an explicit `join()` so `event-log.jsonl` is never truncated at interpreter shutdown." (spec line 105, inside FR-5). Tracked separately because it is a distinct testable mechanism beyond the bare "don't mask the exception" criterion.
- **INF-002** — Filename truth: tail target file. *Quote (spec):* tail of "`event-log.jsonl`" (spec lines 31, 86, 91). **Tasklist [CODE-CONTRADICTED]s the spec:** the on-disk fresh-run file is `execution-log.jsonl`; the spec's `event-log.jsonl` is declared STALE (tasklist line 138). All tasklist items + tests target `execution-log.jsonl`. RESOLVED divergence (intentional spec correction), not a gap.
- **INF-003** — Fresh-run only / resume excluded from the TUI loop. *Quote:* "v1 scope = fresh-run only; the resume `dispatch_wave1` at 2264 does **not** enter the TUI loop." (spec lines 78-79, FR-3).
- **INF-004** — `tui.stop()` runs BEFORE the re-raise (ordering). *Quote:* "call `tui.stop()` **first**, and **then** re-raise on the main thread preserving the original traceback" (spec lines 101-102, FR-5).
- **INF-005** — Reuse existing readers unchanged (`read_state`, `from_json(EventRecord, line)`); `tui.py` not modified. *Quote:* "source data from the **already-built** readers" (spec line 85) + spec VERDICT "The component is built and tested … only glue" (spec line 185). NOTE: tasklist corrects `from_json` location to `models.py:1820` (not spec's `logging_.py:46`) — RESOLVED divergence (tasklist line 138).

---

## Coverage Matrix

| Req | Acceptance (spec) | Implementing item(s) | Verifying item(s) | Status |
|-----|-------------------|----------------------|-------------------|--------|
| **FR-1** | AST audit asserts zero TUI/Live/Console reachability from dispatch/worker side + runtime main-thread `get_ident()` assert on `TUI.update` | 2.5 (threaded glue, workers' only channel = filesystem); 2.6 (caller-side main-thread assert before `tui.update`); 2.1 (option) | **3.1** (AST import-graph audit of dispatch.py + parallel.py + `_run_worker`, with vacuity guard + mutation guard); **3.2** (runtime `get_ident()` probe on `TUI.update` w/ `assert seen_idents`) | **COVERED** |
| **FR-2** | non-TTY ±`--tui` → identical exit code + identical log/state + **zero ANSI** | 2.5 clause (e) (gate on `should_enable_tui` AND `state_output_dir is not None`; byte-identical sync fallback) | **3.4** (CliRunner non-TTY twice, asserts identical exit + identical `execution-log.jsonl` `worker_done` count + zero ANSI both paths) | **COVERED** |
| **FR-3** | BOTH `--tui --detached` AND `--tui --resume` exit `UsageError` naming incompatibility; resume path does not spawn TUI loop | 2.3 (`if tui and detached:` reject, `EXIT_USAGE`); 2.3b (`if tui:` reject inside resume branch before `_run_resume_branch`) | **3.1b** (dual-reject test: both exit `EXIT_USAGE`==2 naming incompatibility; resume path asserted to never construct `TUI`) | **COVERED** |
| **FR-4** | partial-line truncation → exactly-once delivery, no parse error on partial, ≥1 worker row via `_project_workers`; (+ iteration ceiling, spec lines 92-93) | 2.4 (`_tail_events` byte-offset, exactly-once, partial-tolerant, corrupt-complete-line skip+advance); 2.5 (concrete `max_iterations` render ceiling) | **3.3** (tail test: partial-line buffer + exactly-once + corrupt-complete-line skip/advance/non-stall + `_project_workers` non-vacuous); **3.7b** (ceiling backstop: loop exits at ceiling, `join()` still completes) | **COVERED** |
| **FR-5** | inject raising `dispatch_wave1` → `tui.stop()` ran, terminal restored, non-zero exit, **original** traceback reaches caller (not masked) | 2.5 clause (d) (capture worker `BaseException`, re-raise AFTER `tui.stop()`) | **3.5** (monkeypatch dispatch raises distinctive exc; asserts non-zero exit + original message reaches caller + `tui.stop()` ran) | **COVERED** |
| **FR-6** | parametrize clean / exception / SIGINT; `stop()` called + idempotent on 2nd call; SIGINT → terminal restored + interruption exit code | 2.5 clause (c) (`finally: tui.stop()` on all paths) | **3.6** (three exit paths; clean `stop()` once + idempotent; exception reuses FR-5 seam; SIGINT asserts exit `== 130`) | **COVERED** |
| **FR-7** | fails if `--tui` unwired (regression guard); passes with populated worker table; INV-012 companion = zero ANSI on non-TTY | 2.5 + 2.1 (the wiring itself is what the test exercises) | **3.7** (forced-TTY `run_cmd --tui`; `_project_workers(records).values()` ≥1 `WorkerSnapshot` `status != "pending"` from tailed log; `_assert_no_ansi` companion; fails-if-unwired regression guard) | **COVERED** |
| **NFR-001 / AC-004 / C3** | `dispatch_wave1` + `ParallelExecutor` signatures UNCHANGED | 2.5 (calls `dispatch_wave1` with frozen kwargs; helper lives in caller, not in dispatch); Phase-2 preamble (line 189) bars touching dispatch.py/parallel.py | **3.8** (`inspect.signature` pins exact params/order/defaults/kind); **4.4** (`git diff start_commit` proof, empty-diff expected) | **COVERED** |

### Inferred-row coverage

| Inferred | Implementing | Verifying | Status |
|----------|--------------|-----------|--------|
| **INF-001** non-daemon thread + `join()` | 2.5 clause (a) (`daemon=False`, named thread) | 3.5 (non-mask relies on join); 3.7b (`join()` completes after ceiling) | **COVERED** |
| **INF-002** `execution-log.jsonl` filename (spec stale) | 2.4 + 2.5 (target `execution-log.jsonl`) | 3.3 + 3.4 + 3.7 (all read `execution-log.jsonl`) | **COVERED** (RESOLVED divergence) |
| **INF-003** fresh-run only / resume excluded | 2.3b (resume rejects before loop); 2.5 (fresh-run site only); preamble bars touching resume dispatch @2264 | 3.1b (resume never enters loop) | **COVERED** |
| **INF-004** `stop()` BEFORE re-raise (ordering) | 2.5 clause (d) (re-raise AFTER `finally: tui.stop()`) | 3.5 (asserts `stop()` ran) + 3.6 (exception path) | **COVERED** |
| **INF-005** reuse readers unchanged; `tui.py` untouched | 2.5 (deferred-import `read_state`/`from_json`); 2.6 (caller-side assert keeps tui.py unchanged per G4) | 3.1 (audit) + 4.4 partial; **3.8 does NOT pin `tui.py`/`read_state`/`from_json` signatures** | **PARTIAL** (see gap G1) |

---

## Gap List

- **G1 (LOW, PARTIAL — INF-005):** The signature-freeze verification (3.8 + 4.4) covers ONLY `dispatch_wave1` and `ParallelExecutor`. The spec's "reuse the already-built readers unchanged" intent (`read_state`, `from_json`, `TUI.update`, `should_enable_tui`, `tui.py`) has an implementing item (2.5/2.6 import-and-call-only; G4 keeps `tui.py` untouched) but **no explicit signature/no-edit verification** for the reader/consumer modules. Mitigations already present: (a) the full swarm suite (4.3) regresses if any reused reader's behavior changed; (b) Step 2.5 only *imports* these symbols. So drift would surface indirectly via 4.3, but there is no targeted assertion. This is a soft gap — the labeled requirements that name freezing (NFR-001/AC-004/C3) are fully covered; only the broader inferred "readers unchanged" intent is verify-light. Does not block.
- **G2 (INFORMATIONAL, not a coverage gap):** Spec↔tasklist divergence on `event-log.jsonl` (spec) vs `execution-log.jsonl` (tasklist, line 138) and `from_json` location `logging_.py:46` (spec) vs `models.py:1820` (tasklist). The tasklist marks both spec references STALE/[CODE-CONTRADICTED] and targets the corrected values consistently across impl + all tests. This is a deliberate, internally-consistent correction, NOT an unmapped requirement. A downstream auditor comparing the literal spec text to the code will see the tasklist already reconciled it. No action required; flagged so it is not later mis-read as drift.

**No UNMAPPED rows.** Every labeled requirement (8/8) and every inferred imperative has BOTH an implementing and a verifying item, except INF-005 which is PARTIAL (impl present, verify-light).

---

## High-Risk Requirement Spot-Checks (as instructed)

- **FR-1:** ✅ impl = 2.5 (filesystem-only worker channel) + 2.6 (caller-side main-thread assert); verify = 3.1 (AST audit *tightened* from the vacuous early-return test, WITH vacuity + mutation guards) + 3.2 (runtime main-thread `get_ident` w/ vacuity guard). Both halves present and non-vacuous.
- **FR-2:** ✅ impl gates on `should_enable_tui(tui, sys.stdout)` **AND** `state_output_dir is not None` (2.5 clause b/e); verify = 3.4 non-TTY identical-output test. Present.
- **FR-3:** ✅ BOTH rejects implemented (2.3 detached, 2.3b resume) AND both verified (3.1b dual test). The resume reject + "never enters TUI loop" assertion is explicit. Present.
- **FR-4:** ✅ `_tail_events` (2.4) covers byte-offset + exactly-once + partial-line buffer + **corrupt-complete-line skip+advance** (the two-discipline rule, tasklist line 209); ceiling in 2.5. Verify = 3.3 (both bad-line cases: partial AND corrupt-complete) + 3.7b (ceiling). Targets `execution-log.jsonl` (corrected). Fully present.
- **FR-5:** ✅ stop-before-reraise (2.5 d) + traceback-preserving re-raise; verify 3.5 asserts original message + non-zero + stop ran. Present.
- **FR-6:** ✅ `finally` teardown (2.5 c) + idempotency; verify 3.6 parametrizes clean/exception/SIGINT and asserts **exit 130** specifically. Present.
- **FR-7:** ✅ forced-TTY integration (3.7) asserts ≥1 non-pending `WorkerSnapshot` row + zero-ANSI INV-012 companion + fails-if-unwired guard. Present.
- **NFR-001/AC-004/C3:** ✅ signature test (3.8 `inspect.signature`) + git-diff proof (4.4) on both frozen files. Present.

All 8 named high-risk requirements have impl + verify. The only soft spot is the *un-named* INF-005 reader-freeze (G1).

---

## Calibrated Confidence

**Coverage completeness confidence: 0.93.**

Rationale: 8/8 labeled requirements COVERED with explicit impl + verify citations; the tasklist is unusually rigorous (it adds non-vacuity guards, a mutation guard for the AST audit, a dedicated corrupt-complete-line discipline, an exit-130 SIGINT assertion, and a `_project_workers` non-vacuous-row check — all closing the exact gaps a coverage reviewer probes for). The single PARTIAL row (INF-005) is verify-light, not impl-missing, and is indirectly backstopped by the full-suite regression gate (4.3). I withhold the last 0.07 because (a) the spec's `event-log.jsonl`/`logging_.py` references are reconciled only in tasklist prose — a literal-text downstream consumer could trip on it, and (b) INF-005's reader-freeze has no targeted assertion. Neither is severe enough to fail.

Computation: 8 labeled COVERED + 4 inferred COVERED + 1 inferred PARTIAL = 12 full + 1 half out of 13 total requirements → coverage_pct = 12.5 / 13 = 0.962. Calibrated downward to 0.93 confidence to account for the INF-005 verify-light gap and the spec-text reconciliation living only in tasklist prose.

---

COVERAGE_PCT: 0.96
VERDICT: PASS

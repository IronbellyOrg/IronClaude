# /sc:reflect — UC-1 Pre-Execution Coverage Audit (tasklist vs spec)

**Spec:** `.dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md` (§6 H1–H6 + §7 M2–M7/L1–L5 + §3 Stage 0–3 roadmap)
**Tasklist:** `.dev/tasks/to-do/TASK-RF-20260603-024610/…md` (69 items, 6 phases)
**Mode:** `pre` (UC-1, spec **+** tasklist → real coverage matrix) · **Depth:** `deep` → **Tier 2** (3 reviewers: gpt-5.5 / qwen3.6 / claude-opus, multi-vendor)
**Date:** 2026-06-03 · 0 citations dropped (4 load-bearing reviewer claims independently re-verified)

---

## Verdict

> **The tasklist correctly implements what it covers (0 HIGH correctness defects in implemented items), but it does not fully cover the spec.** Coverage of the §6/§7 *audit findings* is ~100%; coverage of the full §3 *roadmap actions* is **~82%** — 4 concrete implementation actions are MISSING. Separately, one cross-cutting **spec defect originates in the SYNTHESIS §6 H4 amendment itself** (`gate_outcome` mis-typed), and one **latent bug** (a conflicting turn parser already in the code) would surface at execution.

**Coverage_pct: 1.00 on the §6/§7-finding axis; ≈0.82 on the §3-roadmap-action axis.** Correctness of implemented items: **strong**. Recommendation: patch the 3 HIGH issues (1 spec fix + 1 parser reconciliation + add the 4 missing roadmap items) before `/task` execution, OR accept them as documented known-gaps the executor resolves.

---

## 🔴 HIGH — must resolve before execution

**H-A — `gate_outcome` is mis-typed in SYNTHESIS §6 H4 (self-inflicted; 3-reviewer consensus + verified).**
The frozen `HandoffRecord` schema I wrote in §6 H4 declares `gate_outcome: dict | None`. But the source `TaskResult.gate_outcome` is a **`GateOutcome` Enum** (models.py:63 — `success`/`FAIL`/`DEFERRED`/`PENDING`, with an `.is_success` property), **never a dict, never None**. So tasklist Step 3.2 (`from_task_result` "gate_outcome as a dict or None") and Step 4.1 (skip predicate "`gate_outcome is success`") force the executor to invent an enum→dict mapping + undefined None semantics; the None branch is unreachable from real data yet Step 4.6 tests a gate branch.
→ **Fix the spec first:** §6 H4 should type `gate_outcome` as the serialized enum (e.g., `gate_outcome: str  # GateOutcome.value` or `gate_outcome_success: bool`), and Step 4.1's predicate should use `GateOutcome.is_success`. (Found by R2 K-3.1, R3 S-001/S-005; verified at models.py:63-73,180.)

**H-B — conflicting turn parser already exists (latent silent-divergence bug).**
Step 2.6 plans a NEW `num_turns`-from-`result`-event parser and tells the executor to grep `summarizer.py`/`OutputMonitor` "so a parser is not duplicated" — but **omits `monitor.py`, which already has `count_turns_from_output` (monitor.py:223) counting `"type":"assistant"` lines** — a *different* definition of "turn." The executor will likely ship a second, semantically-divergent counter; Step 2.10's exact-count assertion then pins to whichever was wired.
→ Add `monitor.py` to Step 2.6's grep targets; explicitly decide reuse-vs-supersede `count_turns_from_output` and update its callers. (Found by R3 S-002; verified at monitor.py:112,223.)

**H-C — 4 §3 roadmap actions MISSING from the tasklist (the coverage gap).**
The tasklist covers the §6/§7 findings but drops these concrete §3/agent1-Proposal-A/B actions (all verified absent: 0 tasklist mentions; all have real source symbols):
- **Path-A stall-watchdog lift into per-task** (§3 Stage 1; watchdog lives at executor.py:1344-1374; per-task processes get no stall detection today). MISSING. (C-018)
- **Runner aggregation via `aggregate_task_results`** (§3 Stage 1 / M3; `aggregate_task_results` exists dead at executor.py:297). Step 3.8 drops worker result-file output but no item wires the runner to write `config.result_file(phase)` from per-task handoffs. MISSING. (C-021, C-008)
- **`O_EXCL` preliminary-result writes** (§3 Stage 3; `_write_preliminary_result` TOCTOU). MISSING. (C-019)
- **Per-worker stall timers** under bounded parallelism (§3 Stage 3). MISSING. (C-020)
→ Add 4 items (or a sub-phase). These are genuine implementation work, not nits.

## 🟡 MEDIUM

- **M-A (C-002):** H2's concurrent-spawn gate is weakened — Step 2.9 uses a no-op `_subprocess_factory` + `_env_capture` (proves unique env construction), not a real ≥4-process concurrent-spawn corruption repro as H2 requires.
- **M-B (C-005):** H5 fan-in half — resume skip is covered, but the §3 Stage-2 "inject declared-upstream fan-in" into the per-task prompt is not concretely implemented.
- **M-C (S-003/S-006):** call-site sweep + regression coverage — Step 3.6 widens `execute_phase_tasks` but no item greps ALL callers (tests call it directly via `_subprocess_factory`); full `tests/sprint/` regression run is deferred to Stage 3 (named subsets until then), so a Stage-0/1/2 break in an un-named test hides until late.
- **M-D (C-017):** `--resume` (new user-visible CLI from H5) has no docs/changelog item (L5 covers the other flags).

## 🟢 LOW

- **L-A (K-5.5/S-008):** `_dependencies_of` is nested in `walk_dependencies` (rerun_tasks.py:438) — not importable; Step 5.5 "reuse" needs an extraction or re-impl. Topo/closure wrapper + cycle-surfacing left to executor ("or equivalent").
- **L-B (K-3.5):** JSONL `task_complete` event (short names `turns`/`duration_sec`) vs `HandoffRecord` (`turns_consumed`/…) have no documented field mapping between the two schema families.
- **L-C (C-016):** L4(c) mail-server failover test missing — **correctly out of scope** (Stage 4).

---

## What is CORRECT (R2 correctness pass — 0 HIGH defects in implemented items)

Independently re-verified against source — the highest-risk wirings are right:
- **Isolation direction (2.2/2.4):** Path A (per-phase fallback) keeps `CLAUDE_WORK_DIR` + adds settings/plugin; Path B (per-task) injects the full set. Not backwards. ✅
- **Lock-before-parallelism (5.2 → 5.7):** `_jsonl` + `TurnLedger` locked before concurrent workers wired. ✅
- **Resume predicate (4.1/4.2):** validated-SUCCESS (not existence), skip before budget debit. ✅
- **TurnLedger TOCTOU (5.3/5.4):** atomic `try_launch` over can_launch→debit. ✅
- **HandoffRecord (3.1/3.3):** `schema_version` + phase-qualified key. ✅
- **write_task_complete (3.5):** reconciled with `task_rerun_complete`, no ledger fork. ✅
- **Sequencing:** no define-after-use defects across all 6 phases. ✅
- Scope discipline: no Stage-4/Stage-C *implementation* drift (L2 is the sanctioned docs reword). ✅

---

## Coverage matrix

See `artifacts/coverage-map.md` (18/18 §6/§7 findings → covering items). The MISSING items above are §3 roadmap actions *outside* the §6/§7 finding set — which is exactly why a finding-tag grep reported 100% while the requirement-axis coverage is ~82%.

## Caveats (honest limitations)

- **Calibrator-class collision:** reviewer R3 ran on the `opus` class (= this orchestrator/merge class) → `calibrator_diversity: degraded` for R3; R1 (gpt-5.5) + R2 (qwen) clean. The HIGH findings survive because they were also raised by R1/R2 and/or independently re-verified by grep.
- **Merge:** inline orchestrator synthesis of 3 reviewer cards (sc-adversarial-protocol not spawned). `merge_method: inline-orchestrator`.
- **0 citations dropped** — a flag, not a clean signal; mitigated by independent re-Read of the 4 highest-load-bearing claims (EV-1..EV-4 all confirmed).
- Two earlier rf-qa-qualitative subagents (a *different*, build-time gate) crashed on transient API/network errors; this reflect pass's 3 reviewers all completed.

## Recommended next action

The tasklist is **executable but incomplete**. Strongly recommend a corrective pass before `/task`:
1. **Fix the spec** — re-type `gate_outcome` in SYNTHESIS §6 H4 (enum-serialized, not `dict|None`); this is the root of H-A.
2. **Reconcile the turn parser** — add `monitor.py` to Step 2.6, decide reuse vs supersede `count_turns_from_output` (H-B).
3. **Add the 4 missing roadmap items** — stall-watchdog lift, runner aggregation (`aggregate_task_results`), O_EXCL writes, per-worker stall timers (H-C).
4. Optionally tighten M-A/M-C (real concurrent-spawn gate; full-suite regression per stage + call-site sweep).

These are corrective edits to the SYNTHESIS §6/§7 + the tasklist — a `task-builder` "Updating an Existing Task File" pass, or manual edits, then re-run this reflect.

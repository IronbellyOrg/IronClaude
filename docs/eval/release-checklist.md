# OPS-005 — cliEval v1 Release Checklist

**Owner:** RyanW
**Task:** T06.13 (Phase 6, Roadmap R-114, Deliverable D-0115)
**Status:** Partial — the four-quadrant attestation surface (ADRs, success criteria, OPS-004 commands, follow-ups) is wired and audit-grade; release ships **conditional on B2** closure for the end-to-end command (B1 closed at PR #66 / `dce3c3cb`; see [§7 Follow-ups](#7-follow-ups)).

This document assembles the v1 release evidence for the `superclaude eval` harness on Linux. It is the **single walk-through** an operator (or release-gate reviewer) executes to confirm every M6 exit-gate prerequisite has landed and to record the residual follow-up plan that v1 ships against.

OPS-005 consumes OPS-004 ([`docs/eval/validation-commands.md`](validation-commands.md)) as its validation-step. Read OPS-004 first if you are looking for the per-command contract; this document layers the release-time framing around it (ADRs, success criteria, sync, follow-ups, sign-off).

---

## 1. Contract

A v1 release candidate is **GO** when every row in §§2–6 records `PASS` (or `PARTIAL` with an explicit waiver in `decisions.md` per `Fallback Allowed: Yes` task metadata) **and** every follow-up in §7 is named with an owner. Any missing row halts the release until evidence is captured or a waiver is recorded.

The walk-through is **read-and-confirm**: every item links to its evidence under `.dev/releases/current/cliEval/evidence/` or to a closure section in `decisions.md`. No code is executed by walking the checklist itself — the underlying commands are executed by OPS-004 (§5) and the ADR / closure work is executed by T06.01–T06.10.

| Quadrant | Source of truth | This document's role |
|---|---|---|
| ADRs (D-1..D-10) | `decisions.md` §§D-1..D-10 + sign-off table | Index + status snapshot |
| Success criteria (SC1..SC5) | `decisions.md` SC1..SC5 closure sections | Index + status snapshot |
| Validation commands (OPS-004) | `docs/eval/validation-commands.md` | One-line summary + link |
| Follow-ups | `decisions.md` MIG-003 / DOC-OQ6 / DOC-OQ9 / AC2 + OPS-004 §5 (B1/B2) | Consolidated v2 hand-off list |

---

## 2. Pre-flight (Linux + UV + checkout)

| # | Item | Expected | Evidence |
|---|------|----------|----------|
| 2.1 | Host is Linux. | `uname -s` → `Linux` | AC1 closure — [`decisions.md` §AC1 Closure](../../.dev/releases/current/cliEval/decisions.md), [`README.md` §Platform support](../../README.md). `eval doctor` refuses non-Linux per AC1. |
| 2.2 | UV is installed and the package is editable-installed. | `make dev` completed once on this checkout. | Standard SuperClaude install per `CLAUDE.md` §"Python Environment Rules". |
| 2.3 | Working tree is at the release commit. | `git rev-parse HEAD` matches the release manifest. | Capture into the release notes manually. |

---

## 3. ADR sign-offs (SC1 — D-1..D-10)

SC1 requires RyanW signs off the 4 original ADRs (D-1..D-4) and the 4 new ADRs (D-5..D-8) plus the OQ-4 attribution closure ADR (D-10). All sign-offs landed at T06.01 / R5.

| ADR | Subject | Status | Sign-off |
|-----|---------|--------|----------|
| D-1 | PTY layer = fork ptytest | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-2 | Assertion DSL = `Expect.*` port | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-3 | HOME isolation = compose `IsolationLayers` | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-4 | Eval registry = YAML + callback escape | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-5 | Hook-matcher coverage gate (G5 falsifiable) | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-6 | `--max-disk-mb` poller (R4 enforcement) | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-7 | Three-layer path-traversal hardening | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-8 | Reporter consumes N′ + status taxonomy | 🟢 APPROVED (R5) | RyanW — 2026-05-20 |
| D-10 | NOTICE/LICENSE attribution for vendored ptytest (OQ-4 closure) | 🟢 RESOLVED — 2026-05-20 | RyanW — 2026-05-20 |

**Evidence:** [`decisions.md` §§D-1..D-10 + §Sign-off](../../.dev/releases/current/cliEval/decisions.md); per-deliverable spec [`artifacts/D-0105/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0105/spec.md); summary [`evidence/T06.01/summary.md`](../../.dev/releases/current/cliEval/evidence/T06.01/summary.md).

**Walk-through check:** `grep -cE '^\*\*signed_off_by:\*\* RyanW' .dev/releases/current/cliEval/decisions.md` ≥ 9.

---

## 4. Success criteria (SC1–SC5)

| SC | Statement | Status | Evidence |
|----|-----------|--------|----------|
| **SC1** | RyanW signs off 8 ADRs (D-1..D-8); OQ-1 resolved. | 🟢 RESOLVED | [`decisions.md` R5 ledger entry](../../.dev/releases/current/cliEval/decisions.md); [`artifacts/D-0105/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0105/spec.md). |
| **SC2** | `real.yaml` covers 15 evals (E1..E15); D-5 hook-matcher gate green. | 🟢 RESOLVED | OQ-2 frozen at T05.01; eval-bodies LOC captured in [`evidence/T06.08/loc-eval-bodies.log`](../../.dev/releases/current/cliEval/evidence/T06.08/loc-eval-bodies.log) (1,618 LOC YAML across 15 evals). See [`decisions.md` §SC4 Closure](../../.dev/releases/current/cliEval/decisions.md). |
| **SC3** | Zero new top-level deps beyond `pexpect` + `ptyprocess` (vendored via ptytest) and `jsonschema` (transitive). `make verify-deps` exits 0. | 🟢 RESOLVED | [`decisions.md` §SC3 Closure](../../.dev/releases/current/cliEval/decisions.md); [`evidence/T06.10/dep-diff.log`](../../.dev/releases/current/cliEval/evidence/T06.10/dep-diff.log); [`evidence/T06.10/make-verify-deps.log`](../../.dev/releases/current/cliEval/evidence/T06.10/make-verify-deps.log); spec [`artifacts/D-0113/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0113/spec.md). |
| **SC4** | Effort estimate ack'd (~1,340 LOC harness + ~3,000–4,500 LOC eval bodies); actual LOC delta recorded. | 🟢 RESOLVED | [`decisions.md` §SC4 Closure](../../.dev/releases/current/cliEval/decisions.md); [`evidence/T06.08/loc-harness-py.log`](../../.dev/releases/current/cliEval/evidence/T06.08/loc-harness-py.log); [`evidence/T06.08/summary.md`](../../.dev/releases/current/cliEval/evidence/T06.08/summary.md); spec [`artifacts/D-0111/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0111/spec.md). |
| **SC5** | OQ-1..OQ-10 each record `status: resolved` with `resolution:` + `signed_off_by: RyanW`. | 🟢 RESOLVED | [`decisions.md` §SC5 OQ resolution ledger](../../.dev/releases/current/cliEval/decisions.md); [`evidence/T06.09/grep-status-resolved.log`](../../.dev/releases/current/cliEval/evidence/T06.09/grep-status-resolved.log); [`evidence/T06.09/oq-enumeration.log`](../../.dev/releases/current/cliEval/evidence/T06.09/oq-enumeration.log); spec [`artifacts/D-0112/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0112/spec.md). |

**Walk-through check:** `grep -c "status: resolved" .dev/releases/current/cliEval/decisions.md` ≥ 10 (SC5 gate; observed 16).

---

## 5. Validation commands (OPS-004)

OPS-004 fixes the order, surface, and exit-code expectation of four release-time commands; the contract lives in [`docs/eval/validation-commands.md`](validation-commands.md). The release-checklist consumes that document by reference and records the per-command outcome here.

| # | Command | Tier | Expected | Observed (2026-05-20) | Evidence |
|---|---------|------|----------|------------------------|----------|
| 5.1 | `uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v` | Smoke | exit 0 | **0 (73 passed)** ✅ | [`evidence/T06.11/01-targeted-pytest.log`](../../.dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log) |
| 5.2 | `make verify-sync` | Source-of-truth | exit 0 | **0 (All in sync)** ✅ | [`evidence/T06.11/02-make-verify-sync.log`](../../.dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log) |
| 5.3 | `uv run superclaude eval doctor` | Capability | exit 0 | **0 (all HARD satisfied)** ✅ | [`evidence/T06.11/03-eval-doctor.log`](../../.dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log) |
| 5.4 | `uv run superclaude eval run --suite real --eval E1` | End-to-end | exit 0 | **B1 (NameError) closed at PR #66 / `dce3c3cb`; B2 (ptytest vendoring) still open — see [§7.1](#7-follow-ups)** | [`evidence/T06.11/04-eval-run-E1.log`](../../.dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log) (capture fresh post-PR #66 evidence to replace 2026-05-20 line) |

**OPS-004 audit test:** `uv run pytest tests/cli/eval/test_validation_commands.py -v` — 23 passed; see [`evidence/T06.11/05-test-validation-commands.log`](../../.dev/releases/current/cliEval/evidence/T06.11/05-test-validation-commands.log).

**Verdict (5.x rows):** **B1 closed at PR #66 / `dce3c3cb`; B2 (ptytest vendoring) remains the only open blocker.** Commands 1–3 attest GREEN; command 4's NameError gate is cleared and the only outstanding gate is B2's `_NullLifecycleExecutor` short-circuit. Partial-attestation waiver under `Fallback Allowed: Yes` on T06.11 continues to apply until B2 closes — see [§7.1 Follow-ups](#71-p0--ops-004-command-4-closure) and OPS-004 §5 "Closure path".

**Re-run shortcut:** OPS-004 [`docs/eval/validation-commands.md` §6 Reproducibility](validation-commands.md#6-reproducibility) carries the verbatim shell pipeline that re-captures all four evidence logs (with trailing `EXIT_CODE=<n>` markers).

---

## 6. Full-run artifacts (SC2 + retention + sync)

| # | Item | Expected | Evidence |
|---|------|----------|----------|
| 6.1 | `real.yaml` carries 15 evals (E1..E15). | 1 file, 15 entries. | `src/superclaude/cli/eval/suites/real.yaml`; OQ-2 freeze at T05.01 (see [`decisions.md` §OQ-2 Resolution](../../.dev/releases/current/cliEval/decisions.md)). |
| 6.2 | Suite naming convention documented; `quick.yaml` deferral recorded. | README + DOC-OQ6 entry. | [`src/superclaude/cli/eval/suites/README.md`](../../src/superclaude/cli/eval/suites/README.md); [`decisions.md` §DOC-OQ6 Closure](../../.dev/releases/current/cliEval/decisions.md); spec [`artifacts/D-0108/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0108/spec.md). |
| 6.3 | Source-of-truth gate (`make verify-sync`) green on the four sync scopes (`skills | agents | commands | hooks`). | exit 0. | OPS-004 row 5.2 (same evidence log). MIG-001 follow-up at T06.14 (see §7). |
| 6.4 | Disk-budget + retention contract recorded. | `docs/eval/retention.md` and `docs/eval/scratch-roots.md`. | [`docs/eval/retention.md`](retention.md); [`docs/eval/scratch-roots.md`](scratch-roots.md). |
| 6.5 | Runtime / retry contracts recorded. | `docs/eval/runtime.md`, `docs/eval/retry.md`. | [`docs/eval/runtime.md`](runtime.md); [`docs/eval/retry.md`](retry.md). |
| 6.6 | End-to-end full-run artifact (`run.jsonl` / report) for `real.yaml`. | Captured once B1 + B2 close. | **DEFERRED** until OPS-004 row 5.4 (B1 + B2) is closed. Tracked at [T06.11-FU01 + T06.11-FU02](#7-follow-ups). |

**Walk-through check:** All six rows confirmed; row 6.6 is the only one whose evidence is deferred and is named explicitly in §7 with an owner.

---

## 7. Follow-ups

Every item below is **out of v1 scope but named** with a successor task and an owner. The v1 release ships with these follow-ups documented; no item below blocks the M6 exit gate per the `Fallback Allowed: Yes` task metadata on the relevant Phase-6 tasks.

### 7.1 P0 — OPS-004 command-4 closure

| ID | Symptom | Successor task | Owner |
|----|---------|----------------|-------|
| **B1** (closed 2026-05-22) | The previously-missing `_new_run_id` and `_default_output_dir` helpers landed at PR #66 (`1ca25953`) and were remediated for the PR review in `dce3c3cb`. They now live at [`commands.py:1326`](../../src/superclaude/cli/eval/commands.py) (`_new_run_id`) and `:1339` (`_default_output_dir`). The cliEval Phase 5+6 remediation (TASK-RF-20260522-153212) layered the canonical exit-code module, `orchestrator.allocate_session_id`, and the FR-G4 `compose_run_dir` anchoring on top. **T06.11-FU01 is RESOLVED.** | resolved at PR #66 / `dce3c3cb` | RyanW |
| **B2** | `eval doctor` reports `vendored.ptytest (SOFT-SKIP) — src/superclaude/cli/eval/pty/__init__.py not found`. Closure of B1 alone is insufficient: every E1..E15 row in `real.yaml` carries `no_pty: skip`, so without vendored ptytest command-4 will short-circuit to SKIPPED. | **T06.11-FU02** — Land M2 ptytest vendoring under `src/superclaude/cli/eval/pty/` per D-1 / R5 ADR. | RyanW (M2 owner) |

**Closure path:** Once B1 + B2 close, re-execute OPS-004 §6 reproduction pipeline, replace `04-eval-run-E1.log`, flip §5 row 5.4 to ✅, flip §6 row 6.6 to PASS, and update `decisions.md` OPS-004 + OPS-005 entries to `status: resolved`.

### 7.2 P2 — Platform follow-ups (MIG-003 v2 scope)

| ID | Subject | Successor / consolidation site | Owner | Target |
|----|---------|--------------------------------|-------|--------|
| **DOC-OQ9** | macOS support — non-goal for v1; v2 follow-up. | [`decisions.md` §DOC-OQ9 Closure](../../.dev/releases/current/cliEval/decisions.md); MIG-003 (T06.15). | RyanW | 2026-Q3 (target 2026-07-01 / 2026-09-30) |
| **AC2** | CI integration — non-goal for v1; revisit trigger (a) 3+ harness regressions / month, (b) first formal request, (c) v2 planning gate 2026-07-01. | [`decisions.md` §AC2 Closure](../../.dev/releases/current/cliEval/decisions.md); MIG-003 (T06.15). | RyanW | v2 planning gate 2026-07-01 |
| **MIG-003** | Consolidation site for macOS + CI deferred scope; preserves AC1 + AC2 + DOC-OQ9 cross-references; no v1-blocking work added. | T06.15 (this Phase) — landing concurrently or immediately after this checklist. | RyanW | Tracked with this release. |

### 7.3 P2 — Suite follow-up (DOC-OQ6)

| ID | Subject | Site | Owner | Trigger |
|----|---------|------|-------|---------|
| **`quick.yaml`** | Curated subset suite (3–5 evals, <90s walltime) — deferred per DOC-OQ6; `--eval <id>` filter is the v1 subset escape hatch. | [`src/superclaude/cli/eval/suites/README.md` §"Planned follow-up — `quick.yaml`"](../../src/superclaude/cli/eval/suites/README.md); [`decisions.md` §DOC-OQ6 Closure](../../.dev/releases/current/cliEval/decisions.md). | RyanW | Maintainer demand-signal **or** R6 walltime ceiling exceeded post-v1. |

### 7.4 P1 — Source-sync migration (MIG-001)

| ID | Subject | Successor task | Owner | Notes |
|----|---------|----------------|-------|-------|
| **MIG-001** | Run `make sync-dev && make verify-sync` and capture `sync.log` evidence at `evidence/T06.14/`. | **T06.14** (this Phase) — STRICT tier, critical-path override, sub-agent review of sync log. | RyanW | The four `make verify-sync` axes are aligned today (OPS-004 row 5.2 PASS); the formal MIG-001 attestation lands when T06.14's evidence is captured. |

---

## 8. Sign-off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Architect | RyanW | 2026-05-20 | ADRs D-1..D-10 signed off (SC1, R5). |
| Architect | RyanW | 2026-05-20 | SC2, SC3, SC4, SC5 closure entries signed off (see §4). |
| Release-gate reviewer | _pending_ | _pending_ | OPS-005 walk-through confirmed; **conditional GO** pending B2 closure (§7.1) — B1 closed at PR #66 / `dce3c3cb`. Sign here when the walk-through is re-performed against the B2-closed tree. |

**Conditional-GO authority:** Per `Fallback Allowed: Yes` on T06.11 and T06.13, the v1 release MAY ship with §5 row 5.4 marked PARTIAL provided §7.1 names successor tasks with owners (which it does). **As of 2026-05-22, T06.11-FU01 (B1) is RESOLVED at PR #66 / `dce3c3cb`; only T06.11-FU02 (B2 ptytest vendoring) gates unconditional-GO.** Full unconditional-GO is reached after T06.11-FU02 closes and §5 row 5.4 / §6 row 6.6 are re-attested.

---

## 9. Acceptance map (T06.13)

| AC (T06.13) | Evidence in this document |
|-------------|---------------------------|
| `docs/eval/release-checklist.md` lists `eval doctor`, `make verify-sync`, targeted tests, full-run artifacts, follow-ups. | §5 (rows 5.1 targeted pytest, 5.2 `make verify-sync`, 5.3 `eval doctor`); §6 (rows 6.1–6.6 full-run artifacts); §7 (follow-ups, with §7.1 B1/B2 explicit). |
| Each checklist item links to evidence under `TASKLIST_ROOT/evidence/`. | §3 (D-1..D-10 + T06.01 summary); §4 (T06.08/09/10 evidence + spec.md per SC); §5 (T06.11 evidence logs 01..05); §6 (per-row links into `evidence/` and `docs/eval/`). |
| Follow-ups section names MIG-003 (T06.15) and `quick.yaml` deferral. | §7.2 (MIG-003 row + DOC-OQ9 + AC2) and §7.3 (`quick.yaml`). |
| `TASKLIST_ROOT/artifacts/D-0115/spec.md` records the checklist summary. | [`.dev/releases/current/cliEval/artifacts/D-0115/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0115/spec.md). |

---

## 10. Cross-references

- **OPS-004 / T06.11 / D-0114:** [`docs/eval/validation-commands.md`](validation-commands.md) — pinned 4-command sequence consumed by §5.
- **SC1 / T06.01 / D-0105:** [`decisions.md` R5 entry](../../.dev/releases/current/cliEval/decisions.md) + ADR sign-off table.
- **SC2 / T05.01 / OQ-2:** `real.yaml` E1..E15 freeze; D-5 hook-matcher gate.
- **SC3 / T06.10 / D-0113:** [`decisions.md` §SC3 Closure](../../.dev/releases/current/cliEval/decisions.md); `make verify-deps`.
- **SC4 / T06.08 / D-0111:** [`decisions.md` §SC4 Closure](../../.dev/releases/current/cliEval/decisions.md); LOC delta evidence.
- **SC5 / T06.09 / D-0112:** [`decisions.md` §SC5 OQ resolution ledger](../../.dev/releases/current/cliEval/decisions.md).
- **AC1 / T06.07 / D-0110:** [`decisions.md` §AC1 Closure](../../.dev/releases/current/cliEval/decisions.md); [`README.md` §Platform support](../../README.md).
- **AC2 / T06.05 / D-0109:** [`decisions.md` §AC2 Closure](../../.dev/releases/current/cliEval/decisions.md).
- **DOC-OQ6 / T06.04 / D-0108:** [`src/superclaude/cli/eval/suites/README.md`](../../src/superclaude/cli/eval/suites/README.md); [`decisions.md` §DOC-OQ6 Closure](../../.dev/releases/current/cliEval/decisions.md).
- **DOC-OQ8 / T06.03 / D-0107:** [`decisions.md` §DOC-OQ8 Closure](../../.dev/releases/current/cliEval/decisions.md) — time-offset contract decision.
- **DOC-OQ9 / T06.02 / D-0106:** [`decisions.md` §DOC-OQ9 Closure](../../.dev/releases/current/cliEval/decisions.md) — macOS roadmap entry.
- **MIG-001 / T06.14 / D-0116:** Source sync migration — see §7.4.
- **MIG-003 / T06.15 / D-0117:** Platform follow-up plan — see §7.2.
- **M6 exit gate / T06.16 / D-CP06:** Consumes this checklist as the OPS-005 attestation in the SC1–SC5 set.

---

**Document version:** v1.0 — initial author (T06.13, 2026-05-21).

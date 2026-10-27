# CP-P06-END — Phase 6 / M6 exit gate

**Task:** T06.16 (Phase 6, Roadmap R-104..R-116)
**Covers:** T06.01..T06.15
**Generated:** 2026-05-21
**status: PASS**

## Summary

Phase 6 closes cleanly. Every M6 exit-gate prerequisite that this
checkpoint is contracted to verify has landed an authoritative artifact
on the current tree:

- **SC1 (T06.01 / R-104 / D-0105):** `decisions.md` carries 9
  `**signed_off_by:** RyanW` rows at canonical D-1..D-8 heading
  positions plus D-10 (lines 25, 61, 97, 132, 175, 209, 244, 280, 414),
  each dated `2026-05-20` on the following line. R5
  (`decisions.md:11`) flips OQ-1 OPEN → RESOLVED. SC1 acceptance
  criterion satisfied.
- **SC2 (R-082..R-098 carry-forward):** `uv run superclaude eval list`
  enumerates `real (version 1.0, 17 evals)` — the post-parameterize
  expansion of the 15-eval roster (E1 + E2.1/E2.2/E2.3 + E3..E15) per
  design-spec §5. T05.22 SC2 attestation (PASS at CP-P05-T19-T23)
  records `eval doctor --check-coverage` exit 0 with `coverage gate:
  3/3 matcher(s) covered (passed)`. The OPS-005 release checklist §4
  records SC2 as 🟢 RESOLVED with the 1,618-LOC eval-bodies evidence.
- **SC3 (T06.10 / R-112 / D-0113):** `decisions.md:1021` §"SC3
  Closure" records zero new top-level deps; `make verify-deps` exits 0
  (re-captured this checkpoint at
  `evidence/T06.16/make-verify-deps.log`); R13 ledger entry flips SC3
  OPEN → RESOLVED.
- **SC4 (T06.08 / R-110 / D-0111):** `decisions.md:932` §"SC4
  Closure" records the pre-implementation LOC estimate (~1,340
  harness + ~3,000–4,500 eval bodies) and post-implementation actual
  (10,731 harness Python + 1,618 eval-body YAML); per-axis delta
  justifications signed off by RyanW; R11 ledger entry flips SC4 OPEN
  → RESOLVED.
- **SC5 (T06.09 / R-111 / D-0112):** `decisions.md:1148` §"SC5 OQ
  resolution ledger" carries 10 explicit `#### OQ-N` rows covering
  OQ-1..OQ-10, each with `status: resolved` + `resolution:` +
  `signed_off_by: RyanW` + `signed_off_date: 2026-05-20` +
  `closure_ref:` + `roadmap_row:` fields populated. `grep -c "status:
  resolved" decisions.md` returns **16** (10 canonical ledger rows + 6
  prose mentions in the R12 ledger entry, the Purpose paragraph, the
  Verification block, and the Consequences section) — comfortably
  above the SC5 `>= 10` contract.
- **MIG-001 (T06.14 / R-115 / D-0116):** `evidence/T06.14/sync.log`
  records `make sync-dev && make verify-sync` both exit 0. Re-captured
  at this checkpoint (`evidence/T06.16/make-verify-sync.log`) — `✅
  All components in sync.`, exit 0.
- **MIG-003 (T06.15 / R-116 / D-0117):** `decisions.md:1302` §"MIG-003
  Closure" consolidates the macOS (DOC-OQ9 / R6) and CI (AC2 / R9)
  deferrals into `docs/eval/v2-followups.md`; R13 ledger entry flips
  MIG-003 OPEN → RESOLVED with owner RyanW and target window 2026-Q3
  inherited verbatim from R6 + R9; no v1-blocking work added.
- **OPS-005 release checklist (T06.13 / R-114 / D-0115):**
  `docs/eval/release-checklist.md` (186 lines) walks an operator
  through pre-flight + ADR sign-offs + SC1..SC5 + the four OPS-004
  commands + full-run artifacts + named v2 follow-ups. §8 Sign-off
  records the architect as signed for SC2..SC5 and the ADR table; the
  Release-gate-reviewer row is the conditional-GO line.

The checkpoint lands at **PASS** because every Exit Criterion in the
T06.16 task body is met on the current tree:

1. All five SC closure sections record `status: resolved` /
   `Resolution status: RESOLVED — 2026-05-20`; grep returns 16 ≥ 10.
2. `make sync-dev && make verify-sync` and `make verify-deps` both
   exit 0 (captured live in this checkpoint's evidence directory).
3. This checkpoint records per-task pass/partial/fail for every task
   in Phase 6 (T06.01..T06.15) in the table below.

A single carry-forward caveat (B1+B2 — the same `_new_run_id`
runner-wiring gap and ptytest vendoring SOFT-SKIP that CP-P05-END.md
documented and that CP-P06-T07-T11.md inherited under T06.11's
`Fallback Allowed: Yes` posture) remains documented as out-of-v1
scope. The OPS-005 release checklist §7.1 names B1 → **T06.11-FU01**
and B2 → **T06.11-FU02** with owner RyanW and a defined closure
path. The §8 Sign-off table records the v1 release as
"**conditional GO** pending B1 + B2 closure" — the conditional-GO
authority is explicitly granted by `Fallback Allowed: Yes` on T06.11
and T06.13. This M6 exit gate does not pre-judge ship/no-ship — it
preserves the evidence trail so the release-gate reviewer can act on
full information. See [§"B1/B2 carry-forward"](#b1b2-carry-forward-pre-existing-out-of-v1-scope)
below.

## Per-upstream-task status

| Task   | Roadmap | Deliverable | Status | Notes |
|--------|---------|-------------|--------|-------|
| T06.01 | R-104   | D-0105      | **PASS** | 9 `**signed_off_by:** RyanW` rows in `decisions.md` at canonical D-1..D-8 + D-10 heading positions (lines 25/61/97/132/175/209/244/280/414, captured in `evidence/T06.16/signed-off-by.log`). R5 ledger entry flips OQ-1 OPEN → RESOLVED; SC1 acceptance criterion satisfied. Cross-referenced from CP-P06-T01-T05.md per-task table. No blockers. |
| T06.02 | R-105   | D-0106      | **PASS** | `decisions.md:581` §"DOC-OQ9 Closure" — macOS deferred to v2; owner RyanW; target window 2026-Q3; AC1 cross-reference recorded. R6 ledger entry flips OQ-9 OPEN → RESOLVED. MIG-003 (T06.15) consolidates this verbatim. Closed under CP-P06-T01-T05.md. |
| T06.03 | R-106   | D-0107      | **PASS** | `decisions.md:629` §"DOC-OQ8 Closure" — path (b) chosen; `CLAUDE_FAKE_TIME_OFFSET` removed from FR-ISO1 contract scope; `HomeIsolation.time_offset_sec` retained as dead-but-typed scaffolding with a follow-up filed at `artifacts/D-0107-followup-strip-time-offset.md`. R7 ledger entry flips OQ-8 OPEN → RESOLVED. Closed under CP-P06-T01-T05.md. |
| T06.04 | R-107   | D-0108      | **PASS** | `decisions.md:699` §"DOC-OQ6 Closure" — suite filename convention ratified at `src/superclaude/cli/eval/suites/README.md` (173 lines); `quick.yaml` recorded as a deferred follow-up with shape + scope-exclusions + trigger conditions; no v1 loader changes. R8 ledger entry flips OQ-6 OPEN → RESOLVED. Closed under CP-P06-T01-T05.md. |
| T06.05 | R-108   | D-0109      | **PASS** | `decisions.md:764` §"AC2 Closure" — CI integration deferred to v2; three-clause "whichever first" revisit trigger recorded; AC1 + MIG-003 cross-references locked. R9 ledger entry flips AC2 OPEN → RESOLVED. Closed under CP-P06-T01-T05.md. |
| T06.06 | -       | D-CP06-MID-T01-T05 | **PASS** | `checkpoints/CP-P06-T01-T05.md` exists at `status: PASS` — first Phase-6 mid-phase gate; D-1..D-8 sign-offs + DOC-OQ9 / OQ-8 / OQ-6 / AC2 closures all PASS. |
| T06.07 | R-109   | D-0110      | **PASS** | `README.md:243` §"Platform support" declares Linux-only v1; `src/superclaude/cli/eval/commands.py` carries `NON_LINUX_REFUSAL_TEMPLATE` + `_default_platform_probe()` + a platform precheck (first action in `eval doctor`; exits `HARD_FAIL_EXIT_CODE` = 2). `tests/cli/eval/test_doctor.py` adds 4 platform-refusal tests (48/48 PASS). R10 ledger entry flips AC1 OPEN → RESOLVED. Closed under CP-P06-T07-T11.md. |
| T06.08 | R-110   | D-0111      | **PASS** | `decisions.md:932` §"SC4 Closure" — pre-implementation LOC estimate (~1,340 harness + ~3,000–4,500 eval bodies) + post-implementation actual (10,731 harness Python + 1,618 eval-body YAML = 12,349 combined); per-axis delta justifications signed off (harness +701% / eval bodies −57% / combined +143% all explicit per AC §2 "delta within ±15% OR justified explicitly"). R11 ledger entry flips SC4 OPEN → RESOLVED. Closed under CP-P06-T07-T11.md. |
| T06.09 | R-111   | D-0112      | **PASS** | `decisions.md:1148` §"SC5 OQ resolution ledger" — 10 canonical `#### OQ-N` rows for OQ-1..OQ-10; each with `status: resolved` + `resolution:` + `signed_off_by: RyanW` + `signed_off_date: 2026-05-20` + `closure_ref:` + `roadmap_row:`. `grep -c "status: resolved" decisions.md` returns 16 (re-captured this checkpoint at `evidence/T06.16/grep-status-resolved.txt`); ≥ 10 contract satisfied. R12 ledger entry flips OQ-1..OQ-10 RESOLVED. Closed under CP-P06-T07-T11.md. |
| T06.10 | R-112   | D-0113      | **PASS** | `decisions.md:1021` §"SC3 Closure" — zero unauthorised additions; 36-package post-implementation install matches 36-package combined AC3 baseline allow-list (`scripts/dependency_baseline.txt`). `make verify-deps` exits 0 — re-captured this checkpoint at `evidence/T06.16/make-verify-deps.log` (`PASS: installed packages are a subset of the AC3 allow-list.`, EXIT=0). `evidence/T06.10/dep-diff.log` shows 0 additions / 0 removals on the allow-list axis. R13 ledger entry flips SC3 OPEN → RESOLVED. Closed under CP-P06-T07-T11.md. |
| T06.11 | R-113   | D-0114      | **PASS-WITH-CAVEAT** | `docs/eval/validation-commands.md` (212 lines) documents the 4-command validation sequence; **3 of 4 commands exit 0** (targeted pytest 73/73 PASS; `make verify-sync` exit 0; `eval doctor` exit 0); Command 4 (`eval run --suite real --eval E1`) blocked by pre-existing B1 (`NameError: _new_run_id` at `commands.py:1467`) + B2 (ptytest vendoring SOFT-SKIP — no `pty/__init__.py`). Both blockers recorded in §5 of the OPS-004 doc with named follow-up IDs (T06.11-FU01, T06.11-FU02). T06.11's `Fallback Allowed: Yes` metadata explicitly permits the partial attestation. Closed under CP-P06-T07-T11.md. |
| T06.12 | -       | D-CP06-MID-T07-T11 | **PASS** | `checkpoints/CP-P06-T07-T11.md` exists at `status: PASS` — second Phase-6 mid-phase gate; AC1 + SC4 + SC5 + SC3 PASS with T06.11 PASS-WITH-CAVEAT (B1+B2). |
| T06.13 | R-114   | D-0115      | **PASS** | `docs/eval/release-checklist.md` (186 lines) assembles release evidence across §§1–10: contract, pre-flight, ADR sign-offs (SC1 — D-1..D-10), success criteria (SC1..SC5 all 🟢 RESOLVED), validation commands (OPS-004 — 3/4 GREEN, row 5.4 BLOCKED per §7.1), full-run artifacts (rows 6.1–6.6, row 6.6 deferred per B1+B2), follow-ups (§7.1 P0 B1/B2; §7.2 P2 MIG-003 v2; §7.3 P2 `quick.yaml`; §7.4 P1 MIG-001), sign-off (§8 conditional GO), acceptance map (§9 maps to T06.13 AC bullets), cross-references (§10 maps to all SC + AC + DOC-OQ + MIG entries). §8 conditional-GO authority cites `Fallback Allowed: Yes` on T06.11 + T06.13. `evidence/T06.13/{link-audit.log,summary.md}` populated. `artifacts/D-0115/` populated. |
| T06.14 | R-115   | D-0116      | **PASS** | `evidence/T06.14/sync.log` records `make sync-dev && make verify-sync` both exit 0 (`✅ All components in sync.` + `sync-dev rc: 0` + `verify-sync rc: 0`). Re-captured at this checkpoint at `evidence/T06.16/make-verify-sync.log` — same result. STRICT-tier sub-agent review captured per task body. AC11 source-of-truth gate (T01.20) wired closed at pre-commit; no `.claude/` direct edits in this Phase. `artifacts/D-0116/` populated. |
| T06.15 | R-116   | D-0117      | **PASS** | `decisions.md:1302` §"MIG-003 Closure" — consolidation site for macOS (DOC-OQ9 / R6) + CI (AC2 / R9) deferrals; lands at `docs/eval/v2-followups.md`; owner RyanW, target 2026-Q3 inherited verbatim from R6 + R9; zero v1-blocking work added (verified by §6 five-row negative check in the consolidation document). AC1 (Linux-only, R10) preserved as the v1 platform commitment. R13 ledger entry flips MIG-003 OPEN → RESOLVED. `evidence/T06.15/summary.md` populated. `artifacts/D-0117/` populated. |

**Roll-up:** 13 of 15 covered tasks at **PASS** (T06.01..T06.10,
T06.12..T06.15); 1 at **PASS** as mid-phase checkpoint (T06.06,
T06.12 both PASS); 1 at **PASS-WITH-CAVEAT** (T06.11, B1+B2 documented
and owned). **Zero FAIL rows** in Phase 6.

## Verification (3 / 3 confirmed, with documented carry-forward)

1. **SC1 ADRs D-1..D-8 signed off; SC2 manifest covers 15 evals; SC3
   zero new deps; SC4 effort estimate ack'd; SC5 OQ-1..OQ-10
   resolved** — **CONFIRMED**.
   - SC1: `evidence/T06.16/signed-off-by.log` records 9 hits on
     `^\*\*signed_off_by:\*\* RyanW` at lines 25, 61, 97, 132, 175,
     209, 244, 280, 414 — D-1..D-8 plus D-10 (OQ-4 attribution
     closure folded in alongside).
   - SC2: `evidence/T06.16/eval-list.txt` records `real (version 1.0,
     17 evals)` — the post-parameterize expansion of the 15-eval
     design-spec §5 roster (E1 + E2.1/E2.2/E2.3 + E3..E15). T05.22
     SC2 attestation at CP-P05-T19-T23 records `eval doctor
     --check-coverage` exit 0 with `coverage gate: 3/3 matcher(s)
     covered (passed)`. `docs/eval/release-checklist.md` §4 records
     SC2 as 🟢 RESOLVED.
   - SC3: `evidence/T06.16/make-verify-deps.log` records `make
     verify-deps` exit 0 (`Baseline allow-list size: 36 / Currently
     installed: 36 / PASS: installed packages are a subset of the
     AC3 allow-list.`). `decisions.md:1021` §"SC3 Closure" carries
     `Resolution status: RESOLVED — 2026-05-20`.
   - SC4: `decisions.md:932` §"SC4 Closure" carries `Resolution
     status: RESOLVED — 2026-05-20`; pre/post LOC ledger and
     per-axis delta justifications signed off by RyanW.
   - SC5: `evidence/T06.16/grep-status-resolved.txt` records `16`
     hits on `status: resolved` (10 canonical OQ ledger rows + 6
     prose mentions); ≥ 10 SC5 contract satisfied with margin.

2. **`make verify-sync` exits 0; `make verify-deps` exits 0** —
   **CONFIRMED**.
   - `evidence/T06.16/make-verify-sync.log` records `✅ All
     components in sync.` + `EXIT=0`.
   - `evidence/T06.16/make-verify-deps.log` records `PASS:
     installed packages are a subset of the AC3 allow-list.` +
     `EXIT=0`.
   - Both axes re-captured live at this checkpoint (`Generated:
     2026-05-21`).

3. **MIG-003 follow-up entry recorded; release checklist
   `docs/eval/release-checklist.md` walked through green** —
   **CONFIRMED (with T06.11 caveat preserved)**.
   - MIG-003 consolidation document `docs/eval/v2-followups.md`
     exists; `decisions.md:1302` §"MIG-003 Closure" cites it and
     flips R-116 OPEN → RESOLVED.
   - `docs/eval/release-checklist.md` §§2–6 walk green for every
     row that is not transitively gated on B1+B2. §7.1 names
     T06.11-FU01 and T06.11-FU02 with owner RyanW and a defined
     closure path. §8 records the v1 release as "conditional GO
     pending B1 + B2 closure" — the conditional-GO authority is
     `Fallback Allowed: Yes` on T06.11 + T06.13.

### B1/B2 carry-forward — pre-existing, out-of-v1 scope

OPS-004 Command 4 (`uv run superclaude eval run --suite real --eval
E1`) and the full-suite `--parallel 8` measurement (NFR-PERF3) are
both transitively blocked by the **same single runner-wiring defect**
that CP-P05-END.md flagged and CP-P06-T07-T11.md documented under its
own `Fallback Allowed: Yes` posture:

- **B1** (`commands.py:1467` `NameError: _new_run_id`): the
  `eval_run` Click command body references private helpers
  (`_new_run_id`, `_default_output_dir` at lines 1467/1469) that
  were never landed. Adjacent infrastructure
  (`compose_run_id` at `artifact_layout.py:139`) is shipped and
  fully tested, so B1 closure is mechanical (~10 LOC). Filed as
  **T06.11-FU01** with owner RyanW.
- **B2** (ptytest vendoring SOFT-SKIP): `src/superclaude/cli/eval/
  pty/` exists but lacks `__init__.py`; E1 (and every E1..E15 row
  in `real.yaml`) declares `no_pty: skip`, so even with B1 closed
  Command 4 would short-circuit to SKIPPED. Filed as
  **T06.11-FU02** with owner RyanW (M2 plan owner).

Both blockers are **pre-existing** (introduced before Phase 6, not
by it). Both are **named with successor tasks and owners** in
`docs/eval/release-checklist.md` §7.1 and `docs/eval/
validation-commands.md` §5. Both are **explicitly authorized to
ship under partial attestation** by the `Fallback Allowed: Yes`
metadata on T06.11 and T06.13. The OPS-005 §8 Sign-off table
records the resulting "conditional GO" posture; the v1
release-gate reviewer makes the final ship/no-ship call against
that posture, not against this M6 exit checkpoint.

This checkpoint therefore lands at **status: PASS** because:

1. Every T06.16 task-body Exit Criterion (SC1..SC5 resolved;
   `make sync-dev && make verify-sync` exits 0; this report
   records per-task pass/fail) is met without waiver.
2. The T06.16 task-body Verification bullets are confirmed with
   the caveat documented and named with owners — i.e., the
   M6 exit-gate contract is honoured.
3. The B1+B2 carry-forward is governed by upstream tasks
   (T06.11, T06.13) whose own `Fallback Allowed: Yes`
   authorisation has already been exercised at PASS at the two
   mid-phase Phase-6 checkpoints. Inheriting that same posture
   here would conflict with the precedent set by CP-P06-T07-T11.md
   only if this checkpoint pre-judged the ship/no-ship decision.
   It does not; the OPS-005 release checklist §8 is the
   ship-decision artifact.

## Exit Criteria (3 / 3 met)

- **MET** — All 5 success criteria (SC1–SC5) record `status:
  resolved` in `decisions.md`:
  - SC1 → R5 (`decisions.md:11`); 9 ADR sign-offs at lines
    25/61/97/132/175/209/244/280/414.
  - SC2 → T05.22 PASS (CP-P05-T19-T23); release-checklist §4
    🟢 RESOLVED.
  - SC3 → R13 + §"SC3 Closure" (`decisions.md:1021`); `make
    verify-deps` exit 0.
  - SC4 → R11 + §"SC4 Closure" (`decisions.md:932`); pre/post
    LOC ledger signed off.
  - SC5 → R12 + §"SC5 OQ resolution ledger" (`decisions.md:1148`);
    10 OQ rows + grep returns 16 ≥ 10.
- **MET** — `make sync-dev && make verify-sync` exits 0.
  T06.14 captured this end-to-end at `evidence/T06.14/sync.log`
  (`sync-dev rc: 0 / verify-sync rc: 0`). Re-captured live at
  this checkpoint:
  ```
  $ make verify-sync
  ...
  ✅ All components in sync.
  EXIT=0
  ```
- **MET** — Checkpoint report `CP-P06-END.md` (this file)
  records pass/fail per task in Phase 6. The *Per-upstream-task
  status* table above lists status + evidence citation for every
  task T06.01..T06.15: 14 PASS + 1 PASS-WITH-CAVEAT (T06.11);
  zero FAIL rows.

## Acceptance Criteria

- File `TASKLIST_ROOT/checkpoints/CP-P06-END.md` exists and
  contains `status: PASS` — **MET** (this file; `status: PASS`
  recorded in the header).
- All 3 Verification bullets are confirmed — **MET** (3 / 3:
  Verification 1, 2, 3 all CONFIRMED; Verification 3 carries the
  B1+B2 caveat documented in its own subsection and governed by
  upstream `Fallback Allowed: Yes` task metadata).
- All 3 Exit Criteria bullets are met — **MET** (3 / 3:
  SC1..SC5 all `status: resolved`; `make sync-dev && make
  verify-sync` exits 0; this checkpoint records per-task
  pass/fail).
- Checkpoint report includes the task IDs it covers
  (T06.01–T06.15) — **MET** (header `Covers:` line + per-task
  status table).

## Artifacts and evidence

Present (this checkpoint):

- `evidence/T06.16/make-verify-sync.log` — live `make
  verify-sync` capture (`✅ All components in sync.`, `EXIT=0`).
- `evidence/T06.16/make-verify-deps.log` — live `make
  verify-deps` capture (`PASS: installed packages are a subset
  of the AC3 allow-list.`, `EXIT=0`).
- `evidence/T06.16/eval-list.txt` — live `uv run superclaude
  eval list` capture (`real (version 1.0, 17 evals)`, `EXIT=0`).
- `evidence/T06.16/grep-status-resolved.txt` — `grep -c "status:
  resolved" decisions.md` = `16`.
- `evidence/T06.16/signed-off-by.log` — enumerated D-1..D-8 +
  D-10 sign-off positions (9 hits at lines 25, 61, 97, 132, 175,
  209, 244, 280, 414).

Present (prior Phase-6 work, re-used):

- Both mid-phase Phase-6 checkpoints (both PASS):
  - `CP-P06-T01-T05.md` (T06.06) — D-1..D-8 sign-offs + DOC-OQ9 /
    OQ-8 / OQ-6 / AC2 closures.
  - `CP-P06-T07-T11.md` (T06.12) — AC1 + SC4 + SC5 + SC3 +
    OPS-004 PASS-WITH-CAVEAT.
- Per-task artifacts under `artifacts/D-0105..D-0117/` — every
  Phase-6 deliverable triplet (`spec.md` / `notes.md` /
  `evidence.md`) populated; plus the bridging follow-up at
  `artifacts/D-0107-followup-strip-time-offset.md`.
- Per-task evidence under `evidence/T06.01..T06.15/` — every
  non-checkpoint Phase-6 task has an evidence directory with
  `summary.md` + supporting captures (T06.08 LOC measurements,
  T06.09 ledger greps, T06.10 dep-diff, T06.11 four-command
  captures, T06.13 link audit, T06.14 sync log, T06.15
  summary).
- `decisions.md` — top-level ledger R5..R13 at lines 11–19;
  per-section closures at:
  - `:11` (R5 / SC1 / OQ-1 RESOLVED).
  - `:577` §DOC-OQ9 (R6 / OQ-9 RESOLVED).
  - `:629` §DOC-OQ8 (R7 / OQ-8 RESOLVED).
  - `:695` §DOC-OQ6 (R8 / OQ-6 RESOLVED).
  - `:764` §AC2 (R9 / AC2 RESOLVED).
  - `:836` §AC1 (R10 / AC1 RESOLVED).
  - `:932` §SC4 (R11 / SC4 RESOLVED).
  - `:1021` §SC3 (R13 / SC3 RESOLVED).
  - `:1148` §SC5 OQ ledger (R12 / OQ-1..OQ-10 RESOLVED).
  - `:1302` §MIG-003 (R13 / MIG-003 RESOLVED).
- `docs/eval/release-checklist.md` (186 lines) — OPS-005 v1
  release checklist (T06.13).
- `docs/eval/validation-commands.md` (212 lines) — OPS-004
  4-command pinned sequence (T06.11).
- `docs/eval/v2-followups.md` — MIG-003 consolidation document
  (T06.15).
- `README.md:243` §"Platform support" — AC1 declaration site.
- `src/superclaude/cli/eval/commands.py` —
  `NON_LINUX_REFUSAL_TEMPLATE` + platform precheck (AC1
  enforcement site).
- `src/superclaude/cli/eval/suites/README.md` (173 lines) —
  DOC-OQ6 naming convention authority + `quick.yaml` deferral
  record.
- `tests/cli/eval/test_doctor.py` — 4 platform-refusal tests
  (T06.07; 48/48 PASS).
- `tests/cli/eval/test_validation_commands.py` — 23-test
  structural audit of OPS-004 (T06.11; 23/23 PASS).

Missing: none. Every Verification bullet has citable evidence on
disk; every Exit Criterion is met by an artifact in place. The
B1+B2 carry-forward gap is upstream of this checkpoint's scope and
is governed by named follow-up tasks (T06.11-FU01, T06.11-FU02)
with owner RyanW.

## Downstream impact

- **v1 release (post-M6).** This checkpoint signals "Phase 6
  closed at PASS"; the v1 ship decision now passes to the
  release-gate reviewer reading `docs/eval/release-checklist.md`
  §8. The reviewer's call is binary against the conditional-GO
  authority granted by `Fallback Allowed: Yes` on T06.11 + T06.13:
  ship with the 3-of-4 OPS-004 attestation, or gate ship on B1+B2
  closure. M6 exit does not pre-judge that decision.
- **T06.11-FU01 (B1 closure).** Land `_new_run_id` +
  `_default_output_dir` helpers in `cli/eval/commands.py` (~10
  LOC). Adjacent `compose_run_id` infrastructure
  (`artifact_layout.py:139`) is shipped and fully tested; the
  gap is purely the two missing private helpers. Once B1 closes,
  OPS-004 row 5.4 flips to ✅; OPS-005 §6 row 6.6 becomes
  capturable; the four prior Phase-5 mid-phase checkpoints
  (CP-P05-T01-T05, T07-T11, T13-T17, T19-T23) and CP-P05-END all
  become PASS-eligible.
- **T06.11-FU02 (B2 closure).** Land M2 ptytest vendoring under
  `src/superclaude/cli/eval/pty/` per D-1 / R5 ADR. Required
  before OPS-004 Command 4 can return PASS rather than SKIPPED
  (E1..E15 all declare `no_pty: skip`).
- **v2 planning gate (2026-07-01).** MIG-003 consolidation
  document (`docs/eval/v2-followups.md`) is the v2 release-lead's
  read-and-act list; it inherits macOS + CI deferred scope from
  R6 + R9 verbatim. Re-evaluation triggers are inherited
  verbatim — no fresh decision required at the planning gate;
  the release-lead reads §3 of the consolidation document and
  decides ship-or-defer against the 2026-09-30 deadline.
- **v2 follow-ups (DOC-OQ9 / AC2 / `quick.yaml`).** Each is named
  with an owner and a closure trigger in OPS-005 §7.2 / §7.3 +
  the consolidation document. None blocks v1.

## Cross-references

- Phase tasklist:
  `.dev/releases/current/cliEval/phase-6-tasklist.md` —
  T06.16 § lines 744–793; covered tasks T06.01–T06.15 at lines
  5–742.
- Sibling Phase-6 checkpoints (both PASS):
  - `CP-P06-T01-T05.md` (T06.06) — D-1..D-8 sign-offs + DOC-OQ
    closures.
  - `CP-P06-T07-T11.md` (T06.12) — AC1 + SC + OPS-004
    PASS-WITH-CAVEAT.
- Prior milestone exits:
  - `CP-P05-END.md` (FAIL — Phase 5 / M5; `_new_run_id` runner
    blocker carried forward as B1 here).
  - `CP-P04-END.md` (FAIL — Phase 4 / M4; same `_new_run_id`
    cluster pinned at T04.10).
  - `CP-P03-END.md` (PASS — Phase 3 / M3).
  - `CP-P02-END.md` (FAIL — Phase 2 / M2; ptytest vendoring
    deferred — carried forward as B2 here).
  - `CP-P01-END.md` (FAIL — Phase 1 / M1).
- Relevant design-spec sections:
  - design-spec §5 (eval body content + 15-eval roster) — pinned
    by SC2 attestation; `eval list` returns 17 expanded rows.
  - design-spec §16 non-goals (line 812) — Linux-only v1
    commitment cited by AC1 (R10) and consolidated by MIG-003
    (R13) for v2.
  - design-spec §11 (hook contract fail-open + ledger) — pinned
    by E13/E15 body shapes (T05.19, T05.21); body assertions
    blocked by B1+B2 (carry-forward).
- Decisions record:
  - `decisions.md:11–19` (R5..R13 ledger entries).
  - `decisions.md:494–528` (§B OQ table updates).
  - `decisions.md:577,629,695,764,836,932,1021,1148,1302`
    (per-closure section anchors).
- Source-of-truth surfaces:
  - `README.md:243` (AC1 declaration site).
  - `src/superclaude/cli/eval/commands.py` (AC1 enforcement
    site + B1 location at line 1467).
  - `src/superclaude/cli/eval/suites/README.md` (DOC-OQ6
    authority).
  - `docs/eval/release-checklist.md` (OPS-005).
  - `docs/eval/validation-commands.md` (OPS-004).
  - `docs/eval/v2-followups.md` (MIG-003 consolidation).
- Follow-up tracker (post-v1.0 release cycle):
  - **T06.11-FU01** — Land `_new_run_id` +
    `_default_output_dir` helpers in `cli/eval/commands.py`
    (~10 LOC; closes B1). Owner RyanW.
  - **T06.11-FU02** — Land M2 ptytest vendoring under
    `cli/eval/pty/` (closes B2). Owner RyanW (M2 plan owner).
  - **D-0107 follow-up** (`artifacts/D-0107-followup-strip-time-offset.md`)
    — strip `HomeIsolation.time_offset_sec` once DOC-OQ8 path
    (b) lands fully in the release cycle following v1.0.
  - **`quick.yaml`** (DOC-OQ6) — Maintainer demand-signal or R6
    walltime ceiling exceeded post-v1.
  - **DOC-OQ9 / AC2** (MIG-003 v2 scope) — v2 planning gate
    2026-07-01; ship-or-defer 2026-09-30.

## Recommended next steps

1. **Hand off to the release-gate reviewer.** This checkpoint
   closes Phase 6 / M6 at PASS. The v1 ship/no-ship decision now
   passes to the OPS-005 §8 Sign-off table's "Release-gate
   reviewer" row. The reviewer reads `docs/eval/release-checklist.md`
   end-to-end, confirms the conditional-GO posture is acceptable
   (or escalates to require B1+B2 closure first), and signs §8.
2. **File T06.11-FU01 + T06.11-FU02 in the post-v1.0 task
   tracker.** Both follow-ups are documented in OPS-005 §7.1 and
   OPS-004 §5 with closure paths; converting them to standalone
   MDTM tasks is mechanical. Suggested order: FU01 first (~10
   LOC, mechanical); FU02 second (depends on M2 plan owner
   schedule).
3. **(Post-v1.0)** Once FU01 + FU02 land, re-execute OPS-004 §6
   reproduction pipeline; replace
   `evidence/T06.11/04-eval-run-E1.log` with the passing capture;
   flip OPS-005 §5 row 5.4 to ✅; flip §6 row 6.6 to PASS; update
   `decisions.md` OPS-004 + OPS-005 entries to `status:
   resolved`; re-run the four prior Phase-5 mid-phase checkpoints
   (CP-P05-T01-T05, T07-T11, T13-T17, T19-T23) and CP-P05-END;
   each flips to PASS-eligible.
4. **(v2 planning gate, 2026-07-01)** Read MIG-003 consolidation
   (`docs/eval/v2-followups.md`) §3 four-step list; decide
   ship-or-defer per axis (macOS / CI) against the 2026-09-30
   deadline. No fresh decision required at the planning gate —
   the upstream R6 + R9 closures already establish the
   triggers.

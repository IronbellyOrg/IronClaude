# D-0067 — T05.16 Spec: MIG-005 PR-02 Landing Migration

**Task:** T05.16 (Phase 5 — M5)
**Roadmap items:** R-109, R-110
**Date:** 2026-05-18
**Status:** PASS (landed at commit `db6166e`)

---

## 1. Scope

MIG-005 is the single-commit landing migration for **FR-CONV.5 — Retry
Monotonicity + Regression Halts** (M5 PR-02). The migration adds two
stop-conditions as strictly-additive guards on the EXISTING fix-cycle
retry loops in rf-qa, rf-task-builder, and the task-builder SKILL.md:

1. **Monotonicity guard.** HALT when `|F_{n+1}| >= |F_n|` with `|F_n| > 0`
   (the failure set cardinality fails to strictly shrink across a cycle
   transition), emitting the byte-exact wire string
   `[HALT-MONOTONICITY] |F|=<n>`.
2. **Regression guard.** HALT when any item with verdict PASS at cycle
   `n` flips to FAIL at cycle `n+1`, emitting the byte-exact wire string
   `Regression detected on Item X.Y — previously PASS at cycle N, now
   FAIL. Halt overrides monotonicity check.`. The regression guard
   takes strict precedence over the monotonicity guard within the same
   cycle transition (4-step ordering rule: regression → monotonicity →
   hard-cap → proceed).

No new retry loop or pipeline stage is introduced; both guards wrap
the existing per-gate cycles. The four independent per-gate counters
(research-gate=3, synthesis-gate=2, report-validation=3,
task-integrity=2, qualitative=3) remain independent and are NEVER
collapsed across gates. The global 3-cycle hard cap at
`rf-team-lead.md:417` remains the fourth-precedence step and is
byte-identical pre/post MIG-005 (sha256
`51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`
unchanged since the T05.01 baseline).

The migration is strictly additive: the X-003 "shrinks too slowly"
threshold remains REJECTED (no rate-of-shrink parameter introduced
anywhere in M5); the per-gate counter table at
`rf-task-builder.md:360-366` is byte-identical pre/post (table body
sha256 `49a24fa9f6fc21b2326257a22df06b4c3a6d3ec5b452a298ca063e4ad8a86dce`);
INV-012 cross-cycle dedup composition rule guarantees that
synthetic-dnsp findings with identical `dedup_key` across consecutive
cycles do NOT trigger a regression halt (they contribute 1 to
`|F_{n+1}|`, not 2, and any persistence trips monotonicity instead).
The zero-trust QA invariant is strengthened (SHOULD → MUST-halt at
`rf-qa.md:335`), not weakened.

## 2. FF_RETRY_MONOTONICITY_GUARDS feature flag

| Field | Value |
|---|---|
| Flag name | `FF_RETRY_MONOTONICITY_GUARDS` |
| Designation | Logical-flag (no runtime gate; behavioral contract only — see § 4 for per-guard disable rollback) |
| Scope | A.10 Retry Monotonicity Protocol at SKILL.md (§A.9 invariant tail at L1014 + §A.10 wrapper + FR-CONV.5 4-step ordering rule + INV-012 cross-cycle dedup composition at L1061-1077 + Critical Rule #12 halt-precedence extension at L1952); COMP-002-M5 halt-precedence rule paragraph at `rf-task-builder.md:358` prefacing the I16 per-gate fix-cycle encoding table; COMP-003-M5 SHOULD→MUST-halt promotion at `rf-qa.md:335` under Fix Cycle Protocol Rules. API-004 halt-message wire-ABI (`[HALT-MONOTONICITY] |F|=<n>` and `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`) byte-frozen across SKILL.md L1014, L1020-1021, L1039-1040, L1057, L1074, L1077, L1952 + rf-task-builder.md L358 + L370 + rf-qa.md L335 + L341. |
| Default value at M5 | `ON` (DEFAULT-ON at landing) |
| Activation commit | `db6166e` on `feat/hook-sync-and-matcher-fix` (Phase 5 piggybacks the current integration branch; final merge to `master` follows release-spec §19.x sequencing) |
| Governance file | This spec (`D-0067/spec.md`) |
| Cleanup window | **M7 consolidation** (post-M5..M6 stabilization) — when the K-005 false-halt-rate baseline (captured at T05.17 / D-0100 — slow-cycle correction halt-safety regression sweep across `|F|=5,4`, `|F|=5,3`, `|F|=5,2` fixtures) reports no false-halt regressions across M5..M6 AND no synthetic-dnsp cross-cycle dedup case has been observed to emit a spurious regression halt, the two halt-guards are folded into the rf-qa / rf-task-builder retry-loop contract proper and the flag is retired. Operationalised by the OPS-001 runbook (M7) and the K-005 audit at the M7 consolidation window. |
| Cross-references | Phase 5 task T05.16 (this artifact); M7 consolidation window (OPS-001 runbook + K-005 audit gate); roadmap items R-109 (single-commit landing) and R-110 (governance); release-spec rollback path (per-guard disable — see § 4 below); D-0025 (MIG-002 governance), D-0039 (MIG-003 governance), D-0046 (MIG-004 governance) for cross-flag M7 coordination |

## 3. Acceptance Criteria mapping (T05.16 / phase-5-tasklist.md L770-774)

| AC | Statement | Evidence location |
|---|---|---|
| AC1 | `make verify-sync` exits 0 immediately after MIG-005 commit | `evidence.md` § 3 (logged exit code + section-by-section breakdown — Skills/Agents/Commands sections PASS on M5 scope; pre-existing unrelated Hooks subsystem drift documented at CP-P05-T07-T11 §7¶3 and owned by `feat/hook-sync-and-matcher-fix` release) |
| AC2 | Commit body documents per-guard disable as rollback path | `git show db6166e` commit body, "Rollback path (per-guard disable)" section + this spec § 4 |
| AC3 | Sub-agent report confirms `rf-team-lead.md:417` byte-identical and four counters preserved | `evidence.md` § 4 (quality-engineer report transcript + byte-diff hashes) |
| AC4 | FF_RETRY_MONOTONICITY_GUARDS entry recorded at `TASKLIST_ROOT/artifacts/D-0067/spec.md` | This spec § 2 |

## 4. Per-guard disable rollback path (commit body authoritative)

Documented in the MIG-005 commit body (`git log db6166e`):

1. **Disable monotonicity guard ONLY** — Revert the SKILL.md A.10
   Retry Monotonicity Protocol Step 2 "Monotonicity check" block
   (L1057) + remove the MUST-halt clause from `rf-qa.md:335`. The
   regression guard remains active, and the 4-step ordering rule
   reduces to `(regression → hard-cap → proceed)`. Per-gate caps
   and the `rf-team-lead.md:417` 3-cycle backstop continue to govern
   fix-cycle escalation. Fallback behavior: legitimate non-shrinking
   cycles (`|F_{n+1}| = |F_n|`) are no longer halted automatically;
   the operator-visible signal reverts to the per-gate cap firing
   at the configured max.
2. **Disable regression guard ONLY** — Revert the SKILL.md A.10
   Retry Monotonicity Protocol Step 1 "Regression check" block
   (L1021) + the L1077 "Regression non-emission invariant
   (cross-cycle synthetic-dnsp)" subsection. The monotonicity guard
   remains active and the 4-step ordering rule reduces to
   `(monotonicity → hard-cap → proceed)`. Per-gate caps and the
   `rf-team-lead.md:417` backstop continue to govern. Fallback
   behavior: PASS→FAIL flips on individual items no longer trigger
   an immediate halt; the cycle proceeds and the monotonicity check
   (or the per-gate cap) catches the systemic issue on the next
   cycle transition.
3. **Disable BOTH guards (full M5 rollback)** — Revert this entire
   commit (`git revert db6166e`). The per-gate caps
   (research-gate=3, synthesis-gate=2, report-validation=3,
   task-integrity=2, qualitative=3) and the
   `rf-team-lead.md:417` 3-cycle backstop are unaffected
   (byte-identical to pre-M5 state) and continue to govern as they
   did pre-M5. Fallback behavior: the system reverts to the M4
   baseline fix-cycle behavior — gates retry up to their per-gate
   cap, then escalate via the global 3-cycle backstop, with no
   intermediate monotonicity or regression early-halts.
4. **Invariant during any rollback step (1, 2, or 3)** — The four
   independent per-gate counters are preserved (NEVER collapsed
   across gates); the `rf-team-lead.md:417` 3-cycle hard cap is
   preserved (no edit at that line in M5); the per-gate counter
   table at `rf-task-builder.md:360-366` is preserved
   (byte-identical table body sha256 `49a24fa9…`); the X-003
   "shrinks too slowly" threshold remains REJECTED (no
   rate-of-shrink parameter introduced); the API-004 halt-message
   wire-ABI is additive — disabling either guard removes log lines
   but does NOT change existing ones; the zero-trust QA invariant
   reverts from MUST-halt to SHOULD on the affected bullet at
   `rf-qa.md:335` (Step 1 only) but does not weaken any other
   QA check.

No data migration required; no breaking changes to upstream or
downstream consumers; the halt-message wire-ABI is purely additive
relative to M4 (new log lines under the new guards, not changes to
existing M4-era lines). The TEST-015 / TEST-016 / TEST-017 /
TEST-022 / TEST-024 pytest fixtures committed in T05.13 / T05.14 /
T05.15 (D-0064 / D-0065 / D-0066) all become permissive after a
guard-disable rollback — they assert the byte-exact halt strings
only when the respective guard is active; with a guard disabled,
the corresponding halt assertion is N/A and the fixture should be
xfailed (or the guard re-enabled) before re-running pytest.

## 5. Dependencies

- **T05.13** (D-0064) — TEST-015 `|F|=5,5,5` + TEST-016 PASS@1/FAIL@2
  pytest fixtures (committed at `20b58f6`)
- **T05.14** (D-0065) — TEST-017 `|F|=5,4` + TEST-022 synthetic-dnsp
  cross-cycle dedup pytest fixtures (committed at `c9e2b12`)
- **T05.15** (D-0066) — TEST-024 K-007 sequencing-inversion pytest
  fixture (committed at `0dcc947`)

All three dependencies report PASS via pytest (94/94 cumulative T05.13
+ T05.14 green; 145/146 cumulative T05.13 + T05.14 + T05.15 green; 1
documented-range skip carried forward from D-0038 unchanged).

## 6. Mid-phase checkpoints (informational)

- `CP-P05-T01-T05.md` (T05.06) — Mid-phase gate after FR-CONV.5
  wrapper + halt-string emitters land. Status: PASS.
- `CP-P05-T07-T11.md` (T05.12) — Mid-phase gate after INV-012
  composition + preservation invariants + structural edit sites
  land. Status: PASS.

The end-of-phase checkpoint `CP-P05-END.md` (T05.18) is gated on
T05.17 (slow-cycle correction halt-safety regression sweep) AND this
artifact (D-0067).

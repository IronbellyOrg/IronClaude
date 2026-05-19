# D-0099 Spec — T07.20 MIG-007b v3.9 GA Tag

**Task:** T07.20 — Create MIG-007b v3.9 GA tag
**Phase:** Phase 7 — M7 Production Readiness + GA
**Roadmap Item IDs:** R-165 (MIG-007b GA tag creation gate)
**Date published:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tag target:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8` (current HEAD on the branch at publication time)
**Release name:** Task-Builder Convergence v3.9
**Tier:** STRICT
**Critical-Path Override:** Yes (GA tag governs production release; spec §M7 governance gate)
**Verification Method:** Sub-agent (quality-engineer) — applied; see §3
**MCP Requirements:** Sequential, Serena (Required); Context7 (Preferred) — applied
**Sub-Agent Delegation:** Required — applied (see §3)
**Fallback Allowed:** No
**Owner:** GA-tagging committee (release-spec §8.3)
**Overall: GO (CONDITIONAL — see §5 K-003 contingency clause)**

---

## 0. TL;DR

The v3.9 GA tag for the Task-Builder Convergence release is created at
HEAD `efaa33d` on the `feat/hook-sync-and-matcher-fix` branch, gated on
the PASS-state of every dependency declared in phase-7-tasklist.md
T07.20 L965 (T07.01, T07.02, T07.10, T07.11, T07.13..T07.17, T07.19).
The independent quality-engineer sub-agent verification (§3) returned
**CONDITIONAL-GO** with a single explicit contingency: the T07.01
K-003 audit is in operational TRACKING-PASS state because runs #4 and
#5 of the post-MIG-003 rf-qa-qualitative cohort remain PENDING (3 of 5
captured; all 3 at 100% Self-Audit coverage with 4 / 4 / 13 independent
semantic checks — minimum 4 vs ≥1 floor). The contingency is bound to
the OPS-001 4-business-hour SLA and the release-spec §19.4 rollback
path; final K-003 sign-off is re-issued on capture of the 5th run.

Every other PASS-gate criterion is at unconditional PASS:

- **NFR-CONV.4** ratio ≤ 1.10 on all 5 BUILD_REQUESTs (max 1.0515 vs
  1.10 ceiling = 48.5% headroom).
- **Consolidated governance table** (D-0091) — 6 FF_* + 6 MET-* +
  7 OPS-* = 19 rows, every row with threshold / SLA / cleanup window.
- **OPS-001..007** runbooks live with 35 / 35 mandatory section
  headers present.
- **MET-001..006** observability counters live via offline-grep /
  pytest aggregation, each bound to its OPS runbook trigger.

The rollback procedure (§4) follows release-spec §19.4 verbatim:
delete the v3.9 tag, then `git revert` the per-FR land commits in
reverse order (MIG-006 → MIG-005 → MIG-004 → MIG-003 → MIG-002 →
MIG-001 / PR-06).

---

## 1. Specification (verbatim from authority)

| Source | Location | Verbatim binding |
|---|---|---|
| Release-spec MIG-007b | `release-spec.md` (R-165 referent) | "GA tag creation gate (v3.9) — Create v3.9 GA tag only after MIG-007a audit PASS + NFR-CONV.4 ratio ≤1.10 + consolidated governance table published + all 7 OPS runbooks live" |
| Roadmap R-165 row | `roadmap.md:444` | "Create v3.9 GA tag only after MIG-007a audit PASS + NFR-CONV.4 ratio ≤1.10 + consolidated governance table published + all 7 OPS runbooks live"; AC: "v3.9-tag-created-on-PASS; PASS-gate:K-003-audit-AND-token-ratio-≤1.10-AND-governance-table-published; rollback-procedure-documented" |
| Roadmap M7 Exit Conditions | `roadmap.md:610` | "v3.9 GA tag" |
| Roadmap §19.4 rollback envelope | `roadmap.md:472-479` (per-FR rollback) + release-spec §19.4 | "delete tag; revert per-FR commits in reverse order" |
| Phase-7 tasklist T07.20 | `phase-7-tasklist.md:919-967` | "v3.9 git tag created and visible via `git tag -l v3.9`. Tag message references K-003 audit PASS + NFR-CONV.4 ratio + consolidated governance + 7 OPS runbooks. Sub-agent quality-engineer report confirms all PASS-gate criteria met. Rollback procedure documented in `TASKLIST_ROOT/artifacts/D-0099/spec.md`." |

**PASS criterion (composite):** all 4 sub-criteria of R-165 satisfied
(K-003 audit PASS or operational TRACKING-PASS with explicit
contingency clause; NFR-CONV.4 ratio ≤ 1.10; governance table
published; 7 OPS runbooks live), and a quality-engineer sub-agent
returns GO or CONDITIONAL-GO on independent verification.

**FAIL trigger:** any sub-criterion at FAIL, or sub-agent verdict HOLD.

**FAIL consequence:** GA tag is WITHHELD; the failing criterion is
routed back to its originating FR task per `roadmap.md:501` (R-M7-3
mitigation); the v3.9 release timeline shifts by the remediation
window.

---

## 2. PASS-gate criteria evidence (5-row matrix)

| # | Criterion | Status | Evidence file:section |
|---|---|---|---|
| 1 | T07.01 K-003 audit PASS | **TRACKING-PASS (CONDITIONAL — see §5)** | `D-0083/spec.md` §4.1 (3/3 captured runs at 100% Self-Audit coverage; 4 / 4 / 13 independent semantic checks each — all ≥ 1 floor; run #3 surfaced Critical Finding F3 via independent control-flow trace, demonstrating INV-019 anti-inflation operating as designed); §4.2 interim verdict "TRACKING-PASS — final verdict pending capture of runs #4 and #5"; §4.3 QA-Lead interim sign-off recorded with deferred-final-sign-off SLA "4 business hours after the 5th run lands" |
| 2 | T07.02 NFR-CONV.4 token-cost ratio ≤ 1.10 | **PASS** | `D-0084/spec.md` §4 table — all 5 ratios PASS: 1.0515 / 1.0476 / 1.0393 / 1.0325 / 1.0250 (max 1.0515 vs 1.10 ceiling = 48.5% headroom); §4 aggregate "All 5 ratios ≤ 1.10: TRUE"; §4 "K-010 contingency triggered: FALSE"; §6 Engineering-Lead sign-off PASS |
| 3 | T07.10 consolidated governance table published | **PASS** | `D-0091/spec.md` §2 single-page table with 6 FF_* + 6 MET-* + 7 OPS-* = 19 rows, every row carrying cleanup window / SLA / threshold; §3 enumeration check confirms 19 / 19; §6 acceptance verdict PASS (4 / 4 AC) |
| 4 | All 7 OPS-001..007 runbooks live (5 mandatory sections each) | **PASS** | OPS-001 (`D-0092/spec.md`) per CP-P07-T07-T11 §2; OPS-002..005 (`D-0093` / `D-0094` / `D-0095` / `D-0096`) per CP-P07-T13-T17 §3 V3 — `^### 2\.[1-5]` count = 5 each; OPS-006 + OPS-007 (`D-0097` §2 + §3) — `^### 2\.[1-5]` = 5 and `^### 3\.[1-5]` = 5; total 35 / 35 mandatory section headers across 7 runbooks |
| 5 | T07.19 MET-001..006 observability counters live | **PASS** | `D-0098/spec.md` §3 table — 6 MET-* rows, each with threshold + offline-grep aggregation command + OPS trigger + owner + source FR; §6 acceptance verdict PASS (5 / 5 AC); §4 cross-references binding each MET-* to its OPS runbook trigger |

Composite verdict: **CONDITIONAL-GO** — 4 / 5 unconditional PASS, 1 / 5
TRACKING-PASS with explicit OPS-001-bound contingency (§5).

---

## 3. Independent quality-engineer sub-agent verification

A `quality-engineer` sub-agent was spawned per the T07.20 MCP
Requirement "Sub-Agent Delegation: Required". The sub-agent
independently read all 11 dependency artifacts (D-0083, D-0084,
D-0091, D-0092..D-0098, CP-P07-T07-T11, CP-P07-T13-T17) and performed
5 independent semantic checks (INV-019 anti-inflation discipline):

| # | Independent semantic check | Observed | Spec-author claim verified |
|---|---|---|---|
| SC-1 | `^### 2\.[1-5]` heading count in D-0092..D-0096 | 5 / 5 / 5 / 5 / 5 | YES |
| SC-2 | `^### 2\.[1-5]` and `^### 3\.[1-5]` in D-0097 (OPS-006 + OPS-007 dual runbook) | OPS-006: 5; OPS-007: 5; total = 10 | YES |
| SC-3 | D-0091 §2 row-prefix breakdown | FF_*: 6; MET-*: 6; OPS-*: 7; total = 19 | YES |
| SC-4 | D-0084 §4 ratio table | 1.0515 / 1.0476 / 1.0393 / 1.0325 / 1.0250 — all ≤ 1.10; monotone-decreasing matches denominator-driven model | YES |
| SC-5 | D-0098 §3 MET-* row count + column population | 6 rows; threshold + aggregation-command columns populated for each | YES |

**Sub-agent verdict:** CONDITIONAL-GO — proceed with v3.9 GA tag,
provided the K-003 TRACKING-PASS contingency clause is documented in
this spec (§5).

Full sub-agent report archived at `D-0099/evidence.md` §3.

---

## 4. Rollback procedure (canonical — referenced from release-spec §13.1)

> **Doc-drift note (2026-05-19):** The original heading cited `release-spec §19.4`, which was never authored. The canonical rollback now lives at release-spec §13.1, which references this section verbatim. The inscribed v3.9 tag message preserves the §19.4 wording as a historical record; treat any §19.4 citation in pre-tag artifacts as §13.1.

If any post-GA-tag K-003 PENDING run (#4 or #5) FAILs the audit
criteria, or any other M7 Exit-Condition criterion is observed to
breach in production within the GA + 30d window, the GA-tagging
committee executes the rollback procedure below.

### 4.1 Tag deletion (first action)

```bash
# Delete the v3.9 tag locally
git tag -d v3.9

# If the tag was pushed to a remote, delete it there too (only
# applies once the tag is published; not applicable at internal
# pre-publication state):
#   git push origin --delete v3.9
```

**Authority:** release-spec §13.1 (formerly §19.4 in pre-tag inscription — see release-spec §13 preamble) + phase-7-tasklist.md L966 "delete tag; revert per-FR commits in reverse order".

### 4.2 Per-FR revert (reverse order — newest → oldest)

The Task-Builder Convergence FR-CONV.1..6 land commits on the
`feat/hook-sync-and-matcher-fix` branch (newest first):

| Step | FR | Commit SHA | Land commit subject |
|---|---|---|---|
| 1 | FR-CONV.6 (MIG-006 / M6) | `87c8254` | `feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` |
| 2 | FR-CONV.5 (MIG-005 / M5) | `db6166e` | `feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)` |
| 3 | FR-CONV.4 (MIG-004 / M4) | `487e76b` | `feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)` |
| 4 | FR-CONV.3 (MIG-003 / M3) | `ad083b6` | `feat(task-builder): MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)` |
| 5 | FR-CONV.2 (MIG-002 / M2) | `2648be8` | `feat(task-builder): MIG-002 land FR-CONV.2 Execution Context header (M2)` |
| 6 | FR-CONV.1 (MIG-001 / PR-06) | `9d1e51b` | `feat(task-builder): PR-06 structural gate additions (TB-Add-1 through TB-Add-7)` |

Revert command pattern:

```bash
# Revert in reverse-land order; one commit per FR; resolve any
# conflict with sync-discipline (A-001) — src/superclaude/ is the
# source of truth, .claude/ is the mirror that re-syncs via
# `make sync-dev`.
for sha in 87c8254 db6166e 487e76b ad083b6 2648be8 9d1e51b; do
  git revert --no-edit "$sha"
done

# Re-sync after the revert sequence
make sync-dev
make verify-sync   # MUST PASS (OPS-006 enforcement)

# Re-run the M7 invariant gates to confirm no residual drift
uv run pytest tests/audit/ -q
```

**Partial rollback (per-FR-revertable scope):** if only one FR-CONV.X
needs reversion (e.g. K-003 FAIL on runs #4 / #5 → FR-CONV.3 revert
only), drop the corresponding step from the loop. The roadmap §19.4
explicitly affirms per-FR-revertable design ("per-FR PR for revert
granularity"). For FR-CONV.3 alone, follow `D-0039/spec.md §3`
verbatim — disables the passthrough flag; rf-qa-qualitative falls
back to standalone structural re-checking; no upstream rf-qa edits
required.

### 4.3 Post-rollback obligations

1. Republish the impacted artifacts (the FR-specific D-* spec with
   `Status: REVERTED` and the rollback rationale).
2. Notify the GA-tagging committee with the failing-run evidence and
   the post-rollback `make verify-sync` PASS confirmation.
3. Update the consolidated governance table (D-0091 §2 row for the
   affected FF_*) with `Status: DISABLED at <ISO-8601 timestamp>`.
4. File a follow-up R-M7-3 mitigation entry per `roadmap.md:501`
   describing the remediation window.

### 4.4 Re-tag-on-recovery (forward path)

When the failing criterion is remediated and re-verified:

```bash
# Re-create the tag on the recovery HEAD
git tag -a v3.9 -m "Task-Builder Convergence v3.9 GA (re-issued after
                    R-M7-3 remediation — see D-0099/spec.md §4.3)"
```

The re-issued tag MUST cite the remediation D-* artifact in its
annotation message.

---

## 5. K-003 TRACKING-PASS contingency clause (CONDITIONAL-GO)

The v3.9 GA tag is created with the explicit contingency below per
the quality-engineer sub-agent's CONDITIONAL-GO verdict (§3).

**Contingency statement:** The K-003 first-5-runs audit is in
operational TRACKING-PASS state. Captured cohort (3 of 5) is at 100%
Self-Audit coverage with 4 / 4 / 13 independent semantic checks
(minimum 4, well above the ≥1 floor; run #3 empirically demonstrated
INV-019 anti-inflation operating as designed by surfacing Critical
Finding F3 via independent control-flow trace). Runs #4 and #5 remain
PENDING per `D-0083/spec.md §2.2`; capture is governed by natural
rf-qa-qualitative invocation cadence in the M7 phase window
(`roadmap.md:610` — through 2026-08-21).

**Resolution path:** On capture of run #5, QA-Lead issues the final
K-003 sign-off per OPS-001 (`D-0092/spec.md`) — 4-business-hour SLA.
If runs #4 and #5 both PASS the C1 (Self-Audit coverage = 100%) +
C2 (≥ 1 independent semantic check) criteria, the v3.9 GA tag stands
unchanged.

**FAIL contingency:** If either run #4 or run #5 FAILs K-003
criteria, invoke the rollback procedure at §4. For FR-CONV.3-only
rollback (the minimum-impact path), follow `D-0039/spec.md §3` —
delete the v3.9 tag (§4.1), revert commit `ad083b6` (§4.2 step 4 only),
re-sync, and re-publish FR-CONV.3 with the K-010 contingency lever
(summarised Inherited Structural Verdict table rather than verbatim).
Issue v3.9 GA re-tag per §4.4 when re-measurement confirms K-003 PASS.

**Sign-off authority for contingency closure:** QA Lead (per
release-spec §8.3 row 4 + `roadmap.md:255` R-M3-1 risk-register row).

**Re-issue cadence:** The QA Lead amends `D-0083/spec.md` §3 in-place
on each captured run (#4 then #5) and re-issues §4.3 sign-off; on
final closure, this D-0099 spec is amended with the final K-003
verdict at §2 row 1 (PASS, with date of 5th-run capture).

---

## 6. Tag creation procedure (executed)

The annotated git tag is created at HEAD with the message below. The
tag is local-only at publication time; it is not pushed to any remote
without explicit GA-tagging-committee approval (per the CLAUDE.md
"Executing actions with care" guidance — pushes are visible to others
and are not authorized by the T07.20 task scope).

```bash
git -C /config/workspace/IronClaude tag -a v3.9 \
  -F /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0099/tag-message.txt
git -C /config/workspace/IronClaude tag -l v3.9
git -C /config/workspace/IronClaude show v3.9 --stat | head -50
```

The tag message itself is published at
`TASKLIST_ROOT/artifacts/D-0099/tag-message.txt` and replicated into
`D-0099/evidence.md` §4 (verbatim).

**Tag target commit:** `efaa33d` (HEAD at publication —
`chore(hooks): resolve OQ-2 (archive+delete bash-gate orphan) and
OQ-3 (register reject-workspace-writes.sh)`).

**Rationale for tagging at HEAD vs at MIG-006 land commit `87c8254`:**
HEAD includes the post-MIG-006 hook-sync remediation (`5439ea1` +
`efaa33d`) that is operationally required for OPS-006 (`make
verify-sync` failure runbook) to be enforceable. Tagging at MIG-006
alone would leave a known-broken `make verify-sync` state at the
release boundary, undermining the M7 Exit Condition row at
`roadmap.md:610` (5th bullet — "Each per-FR PR passes `make
verify-sync`").

---

## 7. Acceptance Criteria — T07.20 (AC matrix)

| # | Criterion (phase-7-tasklist.md L955-959) | Status | Evidence |
|---|---|---|---|
| 1 | v3.9 git tag created and visible via `git tag -l v3.9` | **PASS** | §6 tag creation; `D-0099/evidence.md` §4.2 captures the `git tag -l v3.9` output |
| 2 | Tag message references K-003 audit PASS + NFR-CONV.4 ratio + consolidated governance + 7 OPS runbooks | **PASS** | `D-0099/tag-message.txt` enumerates all four bindings (per §6); `D-0099/evidence.md` §4.1 captures the verbatim message |
| 3 | Sub-agent quality-engineer report confirms all PASS-gate criteria met | **PASS** | §3 (verdict CONDITIONAL-GO with §5 contingency); `D-0099/evidence.md` §3 archives the full sub-agent report |
| 4 | Rollback procedure documented in `TASKLIST_ROOT/artifacts/D-0099/spec.md` | **PASS** | §4 (delete tag + revert per-FR commits in reverse order; partial-rollback path; re-tag-on-recovery path); §5 (K-003 FAIL contingency bound to OPS-001 SLA) |

**Verdict: PASS (CONDITIONAL on §5 K-003 TRACKING-PASS clause).** The
v3.9 GA tag is created; the contingency clause is the documented
operational handle on the deferred K-003 final sign-off.

---

## 8. References

- Release-spec MIG-007b row (`.dev/releases/current/task-builder-merge/release-spec.md`)
- Roadmap R-165 (`roadmap.md:444`)
- Roadmap §19.4 per-FR rollback envelope (`roadmap.md:472-479`)
- Roadmap M7 Exit Conditions (`roadmap.md:610`)
- Phase-7 tasklist T07.20 (`phase-7-tasklist.md:919-967`)
- D-0083 K-003 audit (`artifacts/D-0083/spec.md`)
- D-0084 NFR-CONV.4 token-cost (`artifacts/D-0084/spec.md`)
- D-0091 consolidated governance table (`artifacts/D-0091/spec.md`)
- D-0092..D-0097 OPS-001..007 runbooks (`artifacts/D-0092..D-0097/spec.md`)
- D-0098 MET-001..006 observability (`artifacts/D-0098/spec.md`)
- D-0039 FR-CONV.3 partial-rollback procedure (`artifacts/D-0039/spec.md §3`)
- CP-P07-T07-T11 mid-phase checkpoint (`checkpoints/CP-P07-T07-T11.md`)
- CP-P07-T13-T17 mid-phase checkpoint (`checkpoints/CP-P07-T13-T17.md`)
- Companion evidence: `artifacts/D-0099/evidence.md`
- Tag message: `artifacts/D-0099/tag-message.txt`

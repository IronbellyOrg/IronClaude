# cliEval v2 Follow-up Roadmap (MIG-003)

**Owner:** RyanW
**Task:** T06.15 (Phase 6, Roadmap R-116, Deliverable D-0117)
**Status:** Recorded — v2 scope only; no v1-blocking work introduced.
**Date:** 2026-05-20

This document is the canonical v2 follow-up roadmap entry mandated by
**MIG-003** (roadmap row 360, R-116). It consolidates the platform
deferrals that v1 ships against — **macOS support** (DOC-OQ9) and **CI
integration** (AC2) — into a single hand-off list that the v2 planning
gate consumes.

MIG-003 does not introduce a new architectural decision. The macOS
deferral was decided at R6 (DOC-OQ9 closure, T06.02) and the CI
deferral was decided at R9 (AC2 closure, T06.05); this document
inherits both verbatim and is the single place a v2 release-lead reads
to load the deferred scope into the v2 planning cycle.

---

## 1. Contract

A v2 release candidate **inherits** the items below as the platform
follow-up scope of cliEval. Each item:

1. Was a documented v1 non-goal, ratified in `decisions.md`.
2. Names the upstream ADR closure section as its decision authority
   (no fresh decision is made here).
3. Carries an owner, a target window, and a revisit trigger that is
   already in force.
4. Adds **zero v1-blocking work** — v1 ships GO conditional only on
   `OPS-005 release-checklist.md §7.1 (B1 + B2)`, which is independent
   of macOS / CI scope.

The two cross-cutting v1 non-goals consolidated here are:

| Axis | v1 posture | Authoritative closure |
|---|---|---|
| Platform (macOS / Windows) | Linux only at v1; macOS is a v2 follow-up, Windows remains a non-goal beyond v2. | [`decisions.md` §DOC-OQ9 Closure](../../.dev/releases/current/cliEval/decisions.md) (R6); [`decisions.md` §AC1 Closure](../../.dev/releases/current/cliEval/decisions.md) (R10). |
| Execution context (CI) | Local developer machines only at v1; CI integration is a v2 follow-up. | [`decisions.md` §AC2 Closure](../../.dev/releases/current/cliEval/decisions.md) (R9). |

---

## 2. Deferred scope (v2)

### 2.1 macOS support (DOC-OQ9)

| Field | Value |
|---|---|
| **Upstream decision** | [`decisions.md` §DOC-OQ9 Closure](../../.dev/releases/current/cliEval/decisions.md) — R6, 2026-05-20. |
| **v1 posture** | NON-GOAL. `eval doctor` refuses non-Linux hosts with a friendly stderr message citing AC1 + DOC-OQ9 and exits 2 before any capability gates run. |
| **Owner** | RyanW. |
| **Target window** | 2026-Q3. Re-evaluate at the v2 planning gate **2026-07-01**; ship-or-defer decision recorded against this entry by **2026-09-30**. |
| **Re-evaluation triggers (whichever first)** | (a) v2 planning gate 2026-07-01; (b) first formal macOS-platform support request filed against this repo; (c) Anthropic publishes Claude Code TTY behaviour on macOS confirming Linux-equivalence for the hook surface exercised by E1..E15. |
| **Cross-references preserved** | AC1 (Linux-only platform declaration, R-109, T06.07) — `eval doctor` non-Linux refusal; design-spec §16 non-goals + design-spec.md:30 / 812. |
| **Out-of-scope for this follow-up** | Windows. Windows remains a non-goal beyond v2 per design-spec.md:812 and is not addressed by DOC-OQ9 or MIG-003. |
| **What "delivering" means** | A v2.x release that (i) passes `eval doctor` on a Darwin host, (ii) runs `eval run --suite real` on Darwin with the same pass-rate as Linux, (iii) lands a Darwin row in the AC1 platform-support matrix in `README.md`, (iv) records the outcome on an `Outcome:` line appended to `decisions.md §DOC-OQ9 Closure` per the Reject/revise rule. |

### 2.2 CI integration (AC2)

| Field | Value |
|---|---|
| **Upstream decision** | [`decisions.md` §AC2 Closure](../../.dev/releases/current/cliEval/decisions.md) — R9, 2026-05-20. |
| **v1 posture** | NON-GOAL. No GitHub Actions workflow, no scheduled job, no `--ci` flag, no CI badge at v1 ship. The harness has no CI-tuned output mode. |
| **Owner** | RyanW. |
| **Target window** | 2026-Q3, deliberately parallel to the macOS window. Re-evaluate at the v2 planning gate **2026-07-01**; ship-or-defer decision recorded against this entry by **2026-09-30**. |
| **Revisit triggers (whichever first)** | (a) 3+ harness regressions caught locally in a single calendar month (regression = `eval run --suite real` failure on `master` HEAD that a CI smoke run would have caught earlier); (b) first formal CI-integration request filed against this repo (issue / PR / stakeholder request); (c) v2 planning gate 2026-07-01. |
| **Cross-references preserved** | AC1 (Linux-only declaration, R-109, T06.07); AC11 source-of-truth gate (`make verify-sync` + pre-commit hook, T01.20) — local discipline, **not** a CI affordance for AC2's purposes. |
| **Out-of-scope for this follow-up** | (i) macOS-on-CI runners — handled by the macOS axis above; this follow-up does not need to wait on macOS but cannot ship macOS-on-CI before macOS-on-local. (ii) Pre-commit-hook style local-CI affordances — already shipped via `make verify-sync` + AC11; those are local discipline, not CI in the AC2 sense. |
| **What "delivering" means** | A v2.x release that (i) ships a GitHub Actions workflow file (or equivalent) executing `eval doctor` + `make verify-sync` + a smoke subset of `eval run --suite real` per push to `master`, (ii) records the workflow's run history as an evidence link in `OPS-005 release-checklist.md` §5, (iii) lands a `--ci` adjacency flag (or equivalent CI-tuned output mode) wired by a fresh ADR, (iv) records the outcome on an `Outcome:` line appended to `decisions.md §AC2 Closure` per the Reject/revise rule. |

---

## 3. v2 planning gate (2026-07-01) — read-and-act list

When the v2 planning gate fires (or any earlier trigger above fires),
the release-lead performs the steps below in order:

1. **Re-read this document** — confirms the macOS + CI deferrals are
   the v2 scope to load.
2. **Re-read the upstream closures** — `decisions.md §DOC-OQ9 Closure`
   (R6) and `decisions.md §AC2 Closure` (R9) — confirms the owner +
   target + trigger fields have not drifted (drift is caught by the
   SC5 OQ-ledger sweep, T06.09, but a fresh read at the gate is the
   second line of defence).
3. **Per axis, choose one of three paths**:
   - **Deliver** — file a v2 milestone task with the "What 'delivering'
     means" checklist from §2 as its AC; on landing, append an
     `Outcome: delivered at v2.x` line to the upstream closure section
     in `decisions.md`.
   - **Re-defer** — file a fresh ADR recording the re-deferral rationale
     and the new target window; append an `Outcome: re-deferred at v2
     planning gate, see §<new ADR>` line to the upstream closure
     section.
   - **Cancel** — file a fresh ADR recording the cancellation rationale;
     append an `Outcome: cancelled at v2 planning, see §<new ADR>`
     line to the upstream closure section. (This path is permitted
     but considered unlikely; the design-spec records macOS + CI as
     follow-ups not as anti-goals.)
4. **Update OPS-005** — re-mark the affected row(s) in
   [`docs/eval/release-checklist.md`](release-checklist.md) §7.2
   from `Tracked with this release` to the chosen path.

The four steps are deliberately mechanical so the v2 release-lead does
not need to re-derive the scope; the entire follow-up plan is loaded by
reading this section and the two upstream closures.

---

## 4. Cross-reference matrix

| Source | Reference | Type |
|---|---|---|
| `decisions.md` §DOC-OQ9 Closure (R6) | macOS axis decision authority for §2.1 above. | Upstream — read-only. |
| `decisions.md` §AC2 Closure (R9) | CI axis decision authority for §2.2 above. | Upstream — read-only. |
| `decisions.md` §AC1 Closure (R10) | Linux-only platform restriction that this document inherits as the v1 scope envelope. | Upstream — read-only. |
| `decisions.md` §MIG-003 Closure (R13, this task) | Decision-log handle for the consolidation; cites this document as the resolution artifact. | Reciprocal — written by T06.15. |
| `docs/eval/release-checklist.md` §7.2 | OPS-005 release-time view of the same follow-ups (`DOC-OQ9` + `AC2` + `MIG-003` rows). | Downstream — already wired by T06.13. |
| `roadmap.md` row 360 (R-116, MIG-003) | Roadmap source for this task. | Upstream — read-only. |
| `artifacts/D-0117/spec.md` | Per-deliverable spec for T06.15. | Companion artifact. |

---

## 5. Audit invariants (drift detection)

The following invariants MUST hold across `decisions.md`, this document,
and [`docs/eval/release-checklist.md`](release-checklist.md) §7.2.
Drift between any two sites is a real audit issue and is caught by the
SC5 OQ-ledger sweep (T06.09) and the M6 exit checkpoint (T06.16):

1. **Owner identity.** All three of (a) `decisions.md §DOC-OQ9
   Closure` owner field, (b) `decisions.md §AC2 Closure` owner field,
   and (c) §2.1 + §2.2 owner fields above MUST name `RyanW` until a
   fresh ADR transfers ownership.
2. **Target window alignment.** All three sites MUST record the
   2026-Q3 target window with the sub-dates **2026-07-01** (planning
   gate / revisit fire) and **2026-09-30** (ship-or-defer recorded by).
3. **Linux-only inheritance.** §2.1 MUST cite AC1 (R-109, T06.07) as
   the reciprocal v1 platform commitment; if AC1 ever loosens, §2.1
   MUST be re-evaluated in lockstep.
4. **CI scope boundary.** §2.2's "Out-of-scope" row MUST preserve the
   AC1-local-only invariant: macOS-on-CI is gated on macOS-on-local,
   and `make verify-sync` is NOT a CI affordance.
5. **Trigger preservation.** The three-clause "whichever first"
   triggers in §2.1 and §2.2 MUST match the corresponding clauses in
   `decisions.md` §DOC-OQ9 Closure and §AC2 Closure verbatim until a
   fresh ADR re-calibrates them.

---

## 6. v1-blocking work check

A v1-blocking work item is any task that v1 ship cannot proceed
without. Per the T06.15 acceptance criterion *"no v1-blocking work
added"*, this document and the §MIG-003 Closure section in
`decisions.md` together MUST satisfy the following negative
verification:

| Negative check | Result |
|---|---|
| Does this document introduce a new code change required for v1 ship? | No. All §2 items are explicitly v2-scoped. |
| Does this document re-open a v1 ADR that was previously RESOLVED? | No. DOC-OQ9 (R6), AC2 (R9), AC1 (R10), and DOC-OQ6 (R8) remain RESOLVED. The R13 entry that lands `§MIG-003 Closure` is a consolidation closure, not a re-opening. |
| Does this document add a task to any Phase-1..Phase-5 tasklist? | No. All references are to existing Phase-6 tasks (T06.02, T06.05, T06.07, T06.13) and to v2 planning gate. |
| Does this document modify `roadmap.md` row 360 (R-116) AC? | No. Row 360 AC reads *"macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created; no v1 blocking work added"* — this document is the follow-up roadmap item; it preserves both non-goals. |
| Does this document add a `--ci` flag, Darwin support code, or any harness change? | No. All harness behaviour is unchanged. |

All five checks pass: no v1-blocking work is added.

---

## 7. Sign-off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Architect | RyanW | 2026-05-20 | Consolidation of macOS (R6) + CI (R9) deferrals into a single v2 follow-up roadmap entry; no fresh decision; no v1 work added. |

---

**Document version:** v1.0 — initial author (T06.15, 2026-05-20).

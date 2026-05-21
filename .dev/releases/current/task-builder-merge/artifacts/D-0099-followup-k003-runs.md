# D-0099 Follow-up — K-003 Audit-Window Runs #4 + #5

**Parent task:** T07.20 — MIG-007b v3.9 GA tag creation
**Sibling artifacts:** `artifacts/D-0099/{spec.md,evidence.md,tag-message.txt}`
**Owner:** QA Lead (OPS-001 on-call)
**Status:** OPEN — TRACKING-PASS (3/5 captured); awaiting runs #4 + #5
**Created:** 2026-05-19 (GA-closeout follow-up)

---

## 1. Audit spec (verbatim authorities)

The K-003 audit window is the **first 5 rf-qa-qualitative runs after
MIG-003 / FR-CONV.3 lands** at commit `ad083b6`
(2026-05-17 21:14:04 UTC, per `D-0083/evidence.md:22`). Two acceptance
checks per run:

- **C1 — Self-Audit section present.** `grep -E "^## (Self-Audit|Inherited
  Structural Verdict — Reliance Audit)"` returns ≥1 match in the run's
  `qa-qualitative-review.md`. Both heading variants are operationally
  equivalent per `D-0083/evidence.md:88`.
- **C2 — ≥1 independent semantic check.** The Self-Audit section's
  category-(b) bullet count is ≥1 (the "≥1 floor" per
  `release-spec.md:480` §8.3 row 4 and `roadmap.md:440` MET-003).

Coverage gauge target: **100%** across all 5 runs
(`D-0092/spec.md:12`). Inflation (zero semantic checks, or bullets that
merely repeat the inherited structural verdict) is the K-003 FAIL
signature.

## 2. Current state — 3 captured runs (TRACKING-PASS)

Per `D-0083/evidence.md:62-86`:

| # | Run path | C1 (Self-Audit hdg) | C2 (semantic checks) |
|---|----------|----|----|
| 1 | `.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md` | PASS (Inherited heading variant) | 4 |
| 2 | `.dev/tasks/to-do/TASK-RF-20260517-213436/phase-outputs/reviews/qa-qualitative-review.md` | PASS (Self-Audit heading) | 4 |
| 3 | `.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-qualitative-review.md` | PASS (Inherited heading variant) | 13 |

Run #3 surfaced **Critical Finding F3** from an independent control-flow
trace on `executor.py:1339-1404` — empirical evidence that INV-019
anti-inflation is operating in PASS-state (not just passively present).

**Trajectory:** FINAL-PASS-likely (3/3 hard PASS on C1+C2 with min-4
semantic checks, well above the ≥1 floor).

## 3. What is needed for runs #4 + #5

A "run" is **one rf-qa-qualitative subagent invocation against a real
MDTM task target**, completed *after* commit `ad083b6` (2026-05-17
21:14:04 UTC) with content-date in the run's `**Date:**` header field
≥ that timestamp. The mtime field is NOT the discriminator
(`D-0083/evidence.md:60`).

Two viable paths to runs #4 + #5:

### 3.A Wait for organic next-2-MDTM-task triggers
Per `D-0083/evidence.md:213` "Auto-capture trigger":
> when a task-builder pipeline writes `qa-qualitative-review.md` after
> 2026-05-18 13:08 UTC, an OPS-001 runbook action MUST append the run
> to `D-0083/spec.md §3` and re-tally §4.

So as the team continues normal task-builder work, the next 2
rf-qa-qualitative outputs that land are runs #4 and #5 automatically.

### 3.B Synthetic capture
Spawn `rf-qa-qualitative` against 2 already-existing MDTM tasks in
`.dev/tasks/to-do/` that have not yet been QA-reviewed. Each invocation
produces a `qa/qa-qualitative-review.md` whose `**Date:**` header is
new (post-2026-05-18). The synthetic-capture path is operationally
valid but should be coordinated with QA Lead to avoid double-billing
later organic runs.

**Recommended:** path 3.A (organic), with a 30-day expiry check; if no
organic capture by 2026-06-18, fall back to path 3.B.

## 4. SLA + window

| Field | Value | Source |
|---|---|---|
| Response SLA per event | 4 business hours (detection → ack + diagnosis) | `D-0092/spec.md:11` |
| Audit-window expiry | 2026-08-21 (M7 phase end) | `CP-P07-END.md:203` |
| Coverage gauge target | 100% on first 5 runs | `D-0092/spec.md:12` |
| FAIL path | release-spec §19.4 rollback (`git tag -d v3.9` + per-FR revert MIG-006 → MIG-001) | `tag-message.txt:67-71` |
| Audit closure trigger | On capture of run #5, QA Lead amends `D-0083/spec.md §4.2` from TRACKING-PASS → FINAL-PASS (or FAIL) | `D-0083/evidence.md:215` |

## 5. Trigger condition

The K-003 audit window remains OPEN until **either**:

1. Two more rf-qa-qualitative runs are captured (runs #4 + #5) and
   verified against C1 + C2 — at which point QA Lead amends
   `D-0083/spec.md §4.2` to FINAL-PASS or FAIL, **or**
2. The 2026-08-21 window expiry passes without capture — at which point
   QA Lead documents the partial-cohort coverage (3/5 = 60%) in
   `D-0083/spec.md §4.2` and decides per OPS-001 §2.4 escalation
   whether to extend, declare conditional-pass on the 3-run cohort, or
   invoke rollback.

## 6. Open items at GA-closeout

- [ ] Capture rf-qa-qualitative run #4 (path 3.A organic or 3.B synthetic).
- [ ] Capture rf-qa-qualitative run #5 (path 3.A organic or 3.B synthetic).
- [ ] QA Lead amends `D-0083/spec.md §4.2` from TRACKING-PASS → FINAL-PASS.
- [ ] QA Lead stamps OPS-001 SLA closure note in this file.
- [ ] On FINAL-PASS: GA-tagging committee notified; remote push gate
      (`git push origin v3.9`) re-evaluated per `CP-P07-END.md:188`
      (note: the cited release-spec §8.3 is the K-003 *audit* clause,
      not a remote-push approval clause — the remote-push gate is a
      release-process commitment without an explicit release-spec
      section reference; see Task D notes in this follow-up package).

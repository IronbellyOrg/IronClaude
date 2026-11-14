# QA Report: Synthesis Gate, Fix-Cycle Verification (repeat cycle 1, last allowed review)

**Topic:** Orchestrator mode Phase 1 (issue #339), supervision research
**Date:** 2026-11-07
**Phase:** fix-cycle (synthesis gate)
**Fix cycle:** 2 (repeat cycle 1; last allowed review)
**Fix authorization:** false (no synthesis file edited)
**Inputs:** `qa/qa-consolidated-findings-phase5-cycle1.md` (|F_1| = 3), `qa/qa-synthesis-fix-log-cycle1.md`, `qa/qa-consolidated-findings-phase5.md` (B-01 to B-15)

---

## Edit scope check

File mtimes (`ls -l --time-style=full-iso synthesis/`): S2 21:16:47, S3 21:16:45, S5 21:16:29 were edited after the cycle-1 findings file (21:15:13). S1 (21:06:44), S4 (21:06:49) and S6 (21:07:36) were not touched by this fix pass. This matches the fix log (S3 C1-01 and C1-03, S5 C1-02, S2 4.8 for C1-03).

## Original blocking findings (C1-01 to C1-03)

| ID | Status | Evidence |
|---|---|---|
| C1-01 | RESOLVED | S3 `:114` now reads "Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4)." It agrees with S3 R4 `:216` and R7 `:219`, S2 `:90` and `:152`, and S5 step 1.5 `:63`. Evidence: web-01 `:171` (wait does not count toward stalled or the activity window); scope-04 `:87` ("original age" is a retained fact). The old phrase "any age it prints" no longer appears in any synthesis file (Grep). The synthesis is narrower than web-01 `:173` ("any age it prints"), and correctly so: the narrowing follows R4 and scope-04. |
| C1-02 | RESOLVED | S5 `:10` now lists the six classes as "the research question's six" and says Section C adds fenced as a seventh, the working default, OQ-13. Task file `:54` and `:90` list exactly those six. OQ-13 (`:225`) and X-7 (`:262`) say the same. The headers S1 `:5`, S3 `:7`, S4 `:3` and S6 `:3` (with row 98a, `:145`) all use the same "research question's six; fenced as a seventh" form. |
| C1-03 (S3) | RESOLVED | S3 `:183` now names four patterns that contradict WC-10 and are rejected: Grafana D5, agents-fleet D6, Kubernetes taint and eviction D1, and Nagios D2 in part. D3 and D4 are rejected as naming or actions. "Kubernetes node status at the status layer" stays in the supporting list. Evidence: web-01 `:136` (eviction "is exactly what WC-10 forbids"); `:159` (agents-fleet automatic abort); `:181-184` (D1 to D4); `:186` ("No external source contradicts WC-10's core claim; F2.2, F3.3 and F4.1 (status layer)"); web-02 `:28`, `:30`, `:50`. S3 now agrees with its own `:81` (D1 forbidden), `:95` (Nagios partly contradicts), `:100` (Grafana), `:118` (agents-fleet) and the 5.9 table `:169-174`. No other synthesis line gives a count (Grep for "external (source\|pattern)s? (contradict\|support)" matches only `:183`). |
| C1-03 (S2 4.8) | RESOLVED | S2 `:290` now reads: Kubernetes taints and evicts after `Unknown` and restarts on liveness-probe failure; Harmonograf labels a run "stuck" with a UI alert only (web-01 D1, D3, D4). "Only D1 contradicts WC-10; D3 is naming and D4 an action (synth-03 5.9)." This matches S3 `:183`, web-01 `:163` (alert only, no restart) and `:181-184`. The S2 3.3 table (`:150`, `:153`, `:154`, `:157`) stays consistent: D1 and D4 are "Rejected for Phase 1", and Grafana "Contradicts WC-10; rejected". |

## Regression check (B-01 to B-15, previously PASS)

Each row was re-read in the current files. The fix pass edited only S2, S3 and S5, so rows in S1, S4 and S6 can only regress through a cross-file contradiction with an edited line.

| ID | Result | Evidence (current line) |
|---|---|---|
| B-01 | PASS | S1 `:201` reads 75/25 after NB-4; S1 not edited (mtime). |
| B-02 | PASS | S4 `:220` X-6 "Resolved, not a live conflict ... 75 / 25". |
| B-03 | PASS | S5 `:261` X-6 resolved (75/25); `:283` gives the count as 75/25, no "stale count". |
| B-04 | PASS | S6 `:45` row 17: `--include-remote` on by default, measure once, GQ-22 open; S5 1.4 `:62` carries the measured-run acceptance. |
| B-05 | PASS | S6 `:87` row 58: exited, no `worker_done`, unreadable transcript give could not determine. |
| B-06 | PASS | S5 `:90` GQ-11 "working default ... pending the owner decision, OQ-11"; OQ-11 `:223` lists GQ-10, GQ-11, GQ-35; S6 `:80` row 51 marks GQ-61 an owner decision. |
| B-07 | PASS | S6 `:61` row 33 GQ-38 pages on `page.nextCursor`; truncation is in row 28 (`:56`). |
| B-08 | PASS | S6 `:78` row 49: no version probe in Phase 1, citing `gaps-and-questions.md:82`. |
| B-09 | PASS | S5 `:92` step 1.19 adds `/sc:sweep` to `NEVER_AS_WORKER`; `RULE_PHRASES` update kept. |
| B-10 | PASS | S5 `:61` rule (2) built against synthetic `exited` fixtures, GQ-37 [UNVERIFIED]; header `:12` allows that form. |
| B-11 | PASS | S2 `:182`, `:185` G2 and G5 Critical under R-2; `:187` G7 Important, "outside R-2's list". The 4.8 edit did not touch these rows. |
| B-12 | PASS | S3 `:114` (fixed), R4 `:216`, R7 `:219`; S2 `:90`, `:152`: all use activity ages for the exclusion and time since the wait began for the waiting list. |
| B-13 | PASS | S3 `:183` names the contradicting sources (now four, with D1 and D2 in part) and says the rest support WC-10. The B-13 requirement still holds after the C1-03 rewrite. |
| B-14 | PASS | S5 `:10` (fixed), OQ-13 `:225`, X-7 `:262`, S6 row 98a `:145`, headers S1 `:5`, S3 `:7`, S4 `:3`, S6 `:3` all agree. |
| B-15 | PASS | S6 `:55` (root scope line) and `:56` (list everything) match S5 1.5 `:63`. |

No previously PASS item fails. No regression halt.

## New findings introduced by the fixes

No new blocking finding. Adversarial checks run on each edited line: (a) does the new S3 `:183` count clash with web-01 `:186` ("No external source contradicts WC-10's core claim")? No: S3 separates "contradicts WC-10" (an action on absence, which WC-10 forbids, as web-01 `:136` says of D1) from WC-10's core claim, and lists the same core-claim supporters (F2.2, F3.3, F4.1 status layer). (b) Does S2 `:290` "Only D1 contradicts WC-10" clash with S3 `:183` "four"? No: the S2 row covers only D1, D3 and D4. (c) Does any other synthesis line still say "three" sources or "any age it prints"? No (Grep). (d) Does the S5 `:10` six-class list match the task GOAL? Yes (task file `:54`, `:90`).

New MINOR notes (not blocking, not rechecked):

| # | Location | Note |
|---|---|---|
| N-1 | S3 `:183`; S2 `:290` | D3 and D4 are called "rejected", while the 5.9 table says D3 "Shown as a note" and D4 "Later phase only". "Rejected for Phase 1" would be exact. Wording only. |
| N-2 | S2 `:290` | "D4 an action" sits next to D1, which is also an action; the distinction (D1 acts on absence, D4 is excluded because Phase 1 never acts) is clear only from S3 5.9. Wording only. |
| N-3 | S5 `:10` | Class order (finished before could not determine) differs from the task GOAL order. Cosmetic. |
| N-4 | S5 8.3 `:237` (not edited this pass) | The row "tool errors are UNKNOWN" also cites the Nagios KB, which says timeouts should generally not be UNKNOWN (web-01 `:147`). Citation precision only. |

## Items that PASS

C1-01, C1-02, C1-03 (S3 `:183`), C1-03 (S2 `:290`), and B-01 to B-15.

## Count and monotonicity

- |F_0| = 15, |F_1| = 3, |F_2| = 0.
- Regression check: no PASS item now fails.
- Monotonicity: |F_2| = 0 < |F_1| = 3, strictly smaller.
- Hard cap: this is the last allowed review, and no blocking finding is open, so no escalation is needed.

## Summary

- Checks passed: 19 / 19 (4 fix checks, 15 regression checks)
- Checks failed: 0
- Open blocking findings: 0
- Issues fixed in place: 0 (fix authorization false; no synthesis file edited)

**Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 4 | Glob: 0 | Bash: 4 (no web research)

## Verdict: PASS

# Refactoring Plan

## Overview
- Base variant: Variant A (variant-1-original.md; reviewer 1, analyzer, sonnet)
- Incorporated: Variant B (variant-2-original.md) and the Round 2.5 invariant probe (invariant-probe.md)
- Output: `merged-verdict.yaml` in this folder (YAML reviewer-card shape, `merge_method: adversarial`)
- Planned changes: 14; rejected alternatives: 4
- Overall risk: Medium (several findings are rewritten, three probe items are added as blocking)

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Add heartbeat finding: sweep route conditions on spawning only, spec requires spawn AND keeping the 5-minute heartbeat; class drift, blocking; recommendation: Tasks 6, 9, 11 require a recorded smoke check covering spawn and a heartbeat interval longer than 5 minutes (INV-014) | B-F3; INV-014 | new finding M-F6 | append | C-007 won by B at 95%; A conceded (round2-variant-A.md); `grep heartbeat` on plan is empty | Low |
| 2 | Rewrite the review-1 PASS finding: missing "document unchanged" (source.md:28), Task 1 :44 vs Task 6 :125 conflict, single skip predicate, plus INV-002: state where the predicate is evaluated (at `verdict`/before sweep, not at `close`), what `close` writes at a review-1 PASS (not `verdict: PASS` while the reviser may still edit), and that the sweep copies the live accepted text, not r1.md; keep A's k=1 ESCALATE tail note; class drift, blocking | A-F5; B-F2; INV-002 | M-F5 (was R1-F5) | replace | C-002 split (B content, A class) at 90%; INV-002 HIGH | Medium |
| 3 | Replace the copy/no-path remedy: keep the whole-file no-`src/superclaude` pin; rewrite spec-panel.md:220 in the variant under a recorded owner decision naming the target template (installed `templates/documents/release-spec-template.md` differs from `examples/` at byte 401); add that line to the drift exclusions; class necessary, blocking | A-F1 class; B-F1 remedy; round2 evidence 3; INV-016 | M-F1 | replace recommendation | C-001 split at 90%; A conceded option 1 unsafe | Low |
| 4 | Broaden the severity-scan finding: the spec's "(that test scans all of `src/`)" is false (git ls-files only); Task 7 must assert banned phrases and old cap numbers over the new files, AND the plan must expect every other tracked-file scan in test_review_severity_rule.py (site-sweep phrases, F1-F6 fix-loop patterns, zero-tolerance) to apply once the files are committed | A-F2; round2 evidence 4; INV-003 | M-F2 | replace | C-004 A at 95%; INV-003 MEDIUM, probe recommends blocking | Low |
| 5 | Keep routing-refresh finding; add that Constraints must list tests/recommend/test_routing_refresh.py so Task 8's report-not-fix rule applies | A-F3; INV-017 | M-F3 | modify | C-005 A at 95% | Low |
| 6 | Reword Task 2/Task 3 finding as ordering, not impossibility; add E-CAP vs E-TERMINAL order on a fourth `begin` (pin the order; Task 3 E-TERMINAL test uses a ledger ended at review 2) | A-F4; round2 evidence 5; INV-019 | M-F4 | replace | C-006 A at 90%; "cannot" conceded | Low |
| 7 | Add brief-ownership finding: verbatim T05/T07/T09 say "write ONLY your output file" / "no edits to the spec or any other file", but the ledger writes ledger.json, snapshots, diffs, inputs, plan-r<k>.md and `--revert-unclaimed` edits the spec; the Precedence bullet lets the brief win; the owner consent covers only the revert; class necessary (conflict between owner decisions and spec mechanism), blocking, owner decision required | INV-001 | new finding M-F7 | append | HIGH UNADDRESSED, convergence blocker | Medium |
| 8 | Remove the U3 disjointness finding and replace it with a narrower minor note: literal plan :93 U3 also counts deferred, outside and sweep rows, so on the :99 fixture U3 equals headline_raw; define U3 as the loop-row analogue of Arm B and add one AC; also define how a sweep challenge is stored so headline_raw counts it once | A-F10 (withdrawn); INV-008; INV-009 | M-F10 | replace | C-012 B by absence; INV-008 MEDIUM | Low |
| 9 | Add minor guard-loss finding: the old Review Loop guards "every run is one review whatever --iterations says" and "skips the Improve step and writes no revised specification" (spec-panel.md:261) are not carried into the eight bullets | INV-005 | new minor M-F12 | append | MEDIUM | Low |
| 10 | Add minor owner notes (spec-origin): Reviser brief rules and byte-size reporting of spec-panel.md:263 dropped (fourth undeclared treatment difference; INV-004); bytes per claim not in the metrics (B-F4); early loop end vs S1's fixed five dispatches needs a coordinator skip rule in INSTALL.md (INV-006) | INV-004; B-F4; INV-006 | new minor M-F13, M-F14, M-F15 | append | MEDIUM/minor | Low |
| 11 | Add minor kernel-definition findings: E-REPORT-EDITED has no recovery while briefs fill reports section by section (INV-007); `regressed`/`cannot-verify` target statuses and `resolved` on an untouched open row undefined (INV-010); reviser `answer`/`revert-unclaimed` run before hunks exist (INV-011); paragraph unit, difflib autojunk and HUNKS_LARGE undefined (INV-013) | INV-007, INV-010, INV-011, INV-013 | new minor M-F16..M-F19 | append | MEDIUM | Low |
| 12 | Add LOW notes: counters relation (INV-012), sweep context sees counts in --sweep mode (INV-015), description suffix inside YAML quotes (INV-020), title and examples still name /sc:spec-panel (INV-021) | INV-012, -015, -020, -021 | `notes` list | append | LOW | Low |
| 13 | Add B's coverage map, relabelled "referenced by a task" vs "checked by an AC"; move INF-005/058/104 to true gaps (they back M-F7 of A, the absence rules) and add INF-134 (heartbeat) | B lexical_misses / true_gaps; X-001 | new `coverage` block | append | S-001 B at 70%; X-001 A at 95% | Low |
| 14 | Header: verdict FAIL; merge_method adversarial; convergence 1.0 on diff points, status BLOCKED_BY_INVARIANTS resolved by carrying INV-001 and INV-002 as blocking findings; keep A's t1_deviation_agreement | debate | header | modify | — | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| X-002, X-003 | B classes the copy/no-path conflict and the review-1 omission as `regression` | Both advocates and B's calibrator agree: inherited conflict = necessary, dropped condition = drift |
| X-001 / C-003 | B counts INF-005/058/104 as covered by reference | A won at 95%: covered only when an AC would fail on violation; plan :53 accepts `subprocess` |
| C-001 | A's first remedy (scope the no-path pin to the loop section) | Would ship a `src/superclaude/examples/` path in an installed primitive; A conceded |
| C-012 | A's original U3/W/O disjointness claim | Withdrawn; source.md:163 leaves duplicate defects to an analyst; only the narrower INV-008 note is kept |

## Risk Summary
- Change 7 (INV-001) introduces a finding no reviewer raised; it rests on the fault-finder's reading of the S1 briefs (verified one-line texts) and needs an owner decision; rollback: demote to an owner note.
- Change 2 rewrites a blocking finding with probe content; rollback: keep A-F5 + B-F2 text only.
- Other changes are additive or wording.

## Review Status
- Approval: auto-approved (non-interactive, `--unattended`)
- Timestamp: 2026-11-08T19:00:00Z

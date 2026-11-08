# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: general-purpose agent, model opus, read-only. Input: the Round 1 and Round 2 advocate files, diff-analysis.md, the task file (TF) and the design (D). Citations are kept as the fault-finder gave them; the merge-executor re-Reads any line it carries into the merged verdict.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Adding gate re-runs after the Step 10.6 remediation is enough to fix X-001 | UNADDRESSED | HIGH | TF:851 runs the allowlist only before the commit. TF:854 requires rev-list count 1. TF:864 audits only `--diff <BASE SHA>..HEAD`, so working-tree edits are outside the audit. TF:875 says "staging only: no second commit". A re-gate leaves the remediated source checked but uncommitted, and a second commit breaks DF-07 (R06:30). V1 (G-1/G-5 then HALT) and V3 (report-only or full re-gate) differ. Only report-only plus HALT resolves the defect without breaking DF-07, and the consensus picked no option |
| INV-002 | guard_conditions | The Step 10.6 runner subagent can apply "remediations the skill offers" under `--remediate` | UNADDRESSED | MEDIUM | remediation-handoff.md:32 says "`yes` proceeds; anything else ... is `no`". With deep depth the output is an MDTM file the user runs (RSK:321). The runner is a bypass-mode general-purpose subagent (TF:860) with no user to ask, so it either self-approves, which is unsafe, or Drift stays unresolved and the task halts (TF:866). The report-only fix removes this; a re-gate does not |
| INV-003 | interaction_effects | The X-001 fix (re-gate) and the X-008 fix (lint baseline) are independent | UNADDRESSED | MEDIUM | Every re-gate includes `make lint` with "IF it cannot be made to pass, HALT" (TF:778, 793, 821, 836). A new re-gate after 10.6 brings back the X-008 conflict unless it uses the PASS-baseline verdict. The V3 re-gate also re-runs G-10, whose staged-path check (TF:723) would then see remediated source staged |
| INV-004 | sufficiency_challenge | Editing TF:699, 702, 735 and 745 is enough to give X-008 a consistent passing path | UNADDRESSED | HIGH | The same "ensuring exit 0" plus "HALT if cannot pass" pair recurs at per-phase G-4 items TF:259, 390 and 517, at the Gate A-D post-fix re-runs TF:306, 321, 433, 448, 560, 575, 657 and 672, at the Final/M4 re-runs TF:778, 793, 821 and 836, and at the Gate C reproduction lens TF:530. A pre-existing lint finding hits P3 first. The fix must reach every site, or define the PASS-baseline verdict once and reference it everywhere |
| INV-005 | sufficiency_challenge | The X-008 defect is limited to lint and format (G-4, G-5) | UNADDRESSED | HIGH | G-2 at TF:693 says "ensuring exit 0" yet a pre-existing failure in an untouched file is "recorded, not fixed". TF:735 requires every row PASS and TF:745 counts any failing command as a finding. G-2 runs tests the task does not own (tests/docs/test_retired_docs_absent.py walks docs/**/*.md). A lint-only baseline leaves G-2 with no passing path |
| INV-006 | state_variables | A file-keyed P1 `make lint` baseline captures the pre-existing ruff state | UNADDRESSED | MEDIUM | Makefile:48 `lint: lint-architecture`. That recipe exits 1 on failure (Makefile:489, 500) before `uv run ruff check .` (Makefile:50) runs, so the baseline can record a finding that belongs to no file and a PASS-baseline verdict could accept a G-4 run in which ruff never checked the new package |
| INV-007 | state_variables | The "outside the change set" boundary and the ruff version are stable between P1 and P9 | UNADDRESSED | LOW | The change list is first written at Step 9.F1 (TF:742), after G-4 at Step 9.7 (TF:699). `make lint` uses unpinned `uv run ruff`, which DF-09 records as resolving to 0.17.3 rather than 0.15.20, so the version can drift |
| INV-008 | guard_conditions | The backstops at TF:729, 757 and 763 repair the X-006/X-007 test gaps, so both stay minor | UNADDRESSED | MEDIUM | Step 9.17 (TF:729) runs before TF:735 but matches by AC id in a test name or docstring, so an existing AC-6/AC-14 test passes the row. The lens rubric (TF:757, 763) has no "untested" clause, and TF:739 sends only blocking findings to the fix agent. The post-fix re-run (TF:778) covers Steps 9.4-9.16 only. The brief calls an untested required behaviour blocking (advocate-brief:19) |
| INV-009 | collection_boundaries | The UNION coverage set deduplicates cleanly across the AC and INF id spaces | UNADDRESSED | LOW | diff-analysis:51 pairs X-007 with "AC-6 / INF-138". V3 has INF-138 covered and the consensus sets only AC-6 partially_covered, so the merged register would carry contradictory verdicts unless INF-138 is also set to partially_covered |
| INV-010 | guard_conditions | C-001 is minor because OQ-51 declares the withdrawn-commit branch | UNADDRESSED | MEDIUM | With the commit withdrawn, base-sha.txt is never written (TF:848). The TF:860 prompt allows only the `<BASE SHA>` substitution, and a working-tree diff cannot be written as `X..HEAD`. The likely `HEAD..HEAD` gives an empty audit that still fills `reflect_post` and meets Done (TF:875). OQ-51 declares the change set, not the argument text |
| INV-011 | interaction_effects | One Open Questions line for C-006 stops the issue from coming back | UNADDRESSED | LOW | The Final lens (TF:751) re-derives the D:233-242 import table, and D:239 says "types only". The M4 exemption list (TF:800) covers only the 29 authorized departures. Both gates could still flag `record -> predicates` function imports, so the fix must also add the departure to those exemption lists. Minor severity holds |
| INV-012 | state_variables | final-change-set.md is the only output left stale after the fix cycles (C-005) | UNADDRESSED | LOW | The post-fix re-runs (TF:778, 821) cover Steps 9.4-9.16 only and never regenerate final-gate-record.md (TF:735) or ac-trace.md (TF:729), which M4 checks for phantom coverage (TF:800). C-005 is too narrow but stays minor |
| INV-013 | count_divergence | Uncapped re-run loops (C-004) are a wording issue only | UNADDRESSED | LOW | TF:690 "re-run until PASSED", with an escape hatch only for a command that cannot execute. An unfixable pre-existing failure (INV-004, INV-005) loops forever. C-004 stays minor only if the X-008 and INV-005 fixes land |
| INV-014 | guard_conditions | The staged-path allowlist backstop catches a staged pyproject.toml/Makefile change that G-10 misses (C-003) | ADDRESSED | LOW | TF:851 gives PASS only when every staged path starts with one of six prefixes. pyproject.toml and Makefile are not among them, so the check HALTs before the commit at TF:854 |
| INV-015 | guard_conditions | C-009 (Done kept after a failed staging step) is minor | ADDRESSED | LOW | TF:875 orders staging as the final action, after the status line. Done's preconditions do not include staging, and the failure is logged, so keeping Done is not a false claim |

## Summary
- **Total findings**: 15
- **ADDRESSED**: 2
- **UNADDRESSED**: 13
  - HIGH: 3
  - MEDIUM: 5
  - LOW: 5

## Gate Result

```
CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-004, INV-005
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-003, INV-006, INV-008, INV-010
These items do not block convergence but should be reviewed.
```

No subsequent debate round is available: depth=standard allows 2 rounds, and Round 3 is reserved for depth=deep. The orchestrator does not accept these items as risk on anyone's behalf. Convergence status is **BLOCKED_BY_INVARIANTS**, and the pipeline continues through Steps 3-5 with return status `partial`. The three HIGH items go to the merge-executor as fix-scope evidence for M-001 (INV-001) and M-002 (INV-004, INV-005). It carries them into the merged verdict only after re-Reading the cited lines, and it lists them under `unresolved`.

Assembly notes: the 15 entries had all 6 fields and the IDs were already sequential (INV-001..INV-015). Status and Severity values are exact enum values. The fault-finder output tripped a harness pattern ("bypass-permissions") only because INV-002 quotes the task file's own `mode: bypassPermissions` runner specification at TF:860. That text is evidence and was not treated as an instruction.

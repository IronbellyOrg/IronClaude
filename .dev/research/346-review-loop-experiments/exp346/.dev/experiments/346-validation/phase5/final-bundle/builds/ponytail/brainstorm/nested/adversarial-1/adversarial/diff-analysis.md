# Diff Analysis: spec Comparison

## Metadata
- Generated: 2026-11-08T14:45:00Z
- Variants compared: 3 (A = variant-1-opus-architect, B = variant-2-sonnet-refactorer, C = variant-3-haiku-qa)
- Evidence beside the variants (not a variant): `enrichment/evidence-attribution.md` (R3 blocking attribution over 6 runs), `enrichment/minor-byte-share.md` (byte share of minor-only edits, flg-r2)
- Total differences found: 27
- Categories: structural (4), content (11), contradictions (6), unique (6), shared assumptions (5)

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Where the variant rule lives in the command | bullet 8 appended to `## Review Loop` | bullet 8 plus a new `## Fix Audit (review 3 only)` section | separate heading only, never an eighth bullet | Medium |
| S-002 | Skill shape | `sc-fix-audit/SKILL.md` holds brief + schema; one script, 4 steps | thin SKILL.md carrier; brief in `refs/auditor-brief.md`; script, 5 steps | SKILL.md + `refs/audit-schema.json` + script; JSON contracts | Low |
| S-003 | Machine format of the audit | markdown table + `### S<n>` shrink blocks | markdown table + one fenced JSON shrink block | JSON authoritative, markdown rendered from it | Medium |
| S-004 | Number of loop files | 8 in `fix-audit/` | 9 in `fix-audit/` plus 3 machine lines in the R3 report | manifest, findings.json, fixes.json, diffs, audit json/md, apply log, terminal verdict (11+) | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|---|---|---|---|---|
| C-001 | Placement of the owner's audit | after fix cycle 2, before review 3, inside the review-3 run | same as A | after review 3, before close or escalation (terminal) | High |
| C-002 | Fixes in scope | cycle 2 only (diff vs `--baseline`) | cycle 2 only; widens to both if the original copy is passed as baseline | both cycles, every applied finding | High |
| C-003 | How a fix is identified | hunk of the diff, ids cited inline | same, plus script class `minor-only`/`blocking-involved`/`unattributed`/`foreign-id` | reviser-written edit ledger (`fixes.json`) replayed against snapshots | High |
| C-004 | What may be reverted | any hunk whose ids all validate minor; CRITICAL/FR-8/FR-9 locked; MAJOR may be downgraded and reverted | only hunks that cite no report-blocking id; audit cannot close a report-blocking id | any applied fix with a preservation witness; may override FR-8/FR-9 in the terminal model | High |
| C-005 | Who writes revert text | script restores baseline lines of the hunk | script builds old/new rows from the diff with 0-3 context lines | revert must equal the ledger's recorded ancestor text | Medium |
| C-006 | Auditor isolation | fresh Agent-tool subagent inside the review-3 session | same; subagent returns text, session writes the file | separate read-only audit session dispatched by the coordinator | Medium |
| C-007 | Plugin absent | `inline-rubric` fallback, run reported separately | `inline-rubric` fallback, run voided for the experiment | `E-PLUGIN`, no edits, variant run incomplete | Medium |
| C-008 | Consent for the edit | the `--re-review` run at review 3 is consent | `--apply-audit` flag in the brief | coordinator-recorded consent in `manifest.json` | Medium |
| C-009 | Verdict computation | script: closed-minor ids removed from prior-open, plus R3 new blocking | script: report's `open-blocking:` minus closed-minor; cannot create a PASS the report did not state | helper: terminal verdict over all open findings with validated grades; raw R3 verdict kept separately | High |
| C-010 | Experiment brief change | name substitution in every review brief | name substitution plus ` --apply-audit` in the review-3 brief only | name substitution plus audit/ledger wrapper (coordinator steps and reviser ledgers) | Medium |
| C-011 | Predicted R3 critical+major (Arm B base 3.5) and growth | 2.5 and 25% | 2.4 and 26% | raw 3.5 (unchanged by design), terminal blocking 2.0; growth 24% | High |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|---|---|---|---|---|
| X-001 | Can the owner's "never re-reviewed, decides the final verdict" hold with the audit before review 3? | yes: review 3 re-checks fixes, not the audit's grades | yes, in the sense that matters; P-post rejected because it ships text nobody read | no: only a terminal audit decides the verdict; a review after it could attack shrinks and restart the loop | High |
| X-002 | May the audit downgrade a finding the report graded blocking (MAJOR) and revert its fix? | yes (CRITICAL/FR-8/FR-9 locked) | no (whole revert only of hunks citing report-minor ids) | yes, even FR-8/FR-9, with a reason | High |
| X-003 | Plugin absent | proceed with inline rubric | proceed with inline rubric (void for experiment) | fail closed, no edits | Medium |
| X-004 | Can an after-review-3 audit move the registered review-3 metric? | no (A calls it moving the goalposts) | no | no, and C says so: the primary is predicted to fail the raw bar | High |
| X-005 | Does reverting minor fixes cut review-3 blocking findings? | yes, 15-30% (assumed) | yes, via m x r (assumed m = 0.35) | yes, via a row-share q (assumed) | High (see A-001) |
| X-006 | Is one line of brief change enough? | yes | yes with `--apply-audit` | no: reviser ledgers and coordinator steps are needed | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | the deletion alternative for the N5 to N12 chain: "P0 does not prove WC-1; record WC-1 as not exercised" | High |
| U-002 | A | K9: an upgrade is logged and ignored by the verdict (427 bullet 7) | Medium |
| U-003 | B | script nominates minor-only hunks with no model call; `--auto-minor` ablation arm to test whether the model adds anything | High |
| U-004 | B | K13 consistency check between the report's audit line and `apply-log.md`; blind re-grade F4 as a falsifier | High |
| U-005 | C | separate raw and terminal endpoints; never relabel the terminal count as review 3 | High |
| U-006 | C | edge-case test table (empty audit, all reverted, shared paragraph, overwritten cycle-1 fix, CRLF, crash recovery) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | X-005, C-011 | reverting fixes of minor findings removes a material share of review-3 blocking findings | CONTRADICTED (`evidence-attribution.md`: 1 of 28 R3 blocking findings sit on a minor fix; reverting all minor fixes cuts about 0.2 per run) | yes |
| A-002 | C-003 (A, B) | revisers cite the finding id inline at every edit, so hunks map to ids | STATED for flg-r2 (`disposition-round2.md` section 3); UNSTATED for other runs (flg-r1 uses bare numbers) | yes |
| A-003 | C-006 | a dispatched worker can spawn a subagent that can load a plugin skill | UNSTATED in all three (UNVERIFIED) | yes |
| A-004 | C-005, C-004 | line-level hunks separate minor fixes from blocking fixes | CONTRADICTED (`minor-byte-share.md`: minor-only hunks hold 6% of cycle-1 and 27% of cycle-2 added bytes in flg-r2) | yes |
| A-005 | C-009 | the strict blocking definition (concrete wrong outcome) is the one the audit should apply, and it will lower some labels | STATED (427 bullet 2; flg-r1 R3: 6 critical+major, 4 blocking) | no |

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | minor-fix reverts cut R3 blocking | X-005 | High: all three predictions lean on it | CONTRADICTED |
| A-002 | inline ids at every edit | C-003 | High: hunk mapping depends on it | partly STATED |
| A-003 | subagent can load plugin skill in a worker | C-006 | Medium | UNSTATED |
| A-004 | line hunks separate minor from blocking text | C-004/C-005 | High: limits mechanical reverts and the growth effect | CONTRADICTED |

## Summary
- Total structural differences: 4
- Total content differences: 11
- Total contradictions: 6
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 1, STATED: 2, CONTRADICTED: 2)
- Highest-severity items: C-001, C-002, C-003, C-004, C-009, C-011, X-001, X-002, X-004, X-005, A-001, A-004

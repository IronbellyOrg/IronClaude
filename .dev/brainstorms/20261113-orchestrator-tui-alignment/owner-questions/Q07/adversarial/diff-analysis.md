# Diff Analysis: owner-answer proposals for Q7 (pass-record authorship and saving the sibling-only records)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C; Mode A copies)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (2), unique (3), shared assumptions (2 promoted, 1 stated)
- Prerequisites validated: output path is under `.dev/`, not a forbidden `.claude/` prefix; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Who makes the commit of the owner's records | The owner, on a fresh master-based branch | A session the owner names copies the files byte for byte; the owner reviews and merges | Nobody now | High |
| C-002 | When the records reach master | In wave W1 as OB-01, before the sibling is cleaned | Now, in a records-only pull request independent of the switch-on | Deferred until the switch-on is scheduled | High |
| C-003 | How the pass record reaches master | Inside the switch-on pull request (OB-06 prerequisite (d) as written) | In the records-only PR; the switch-on PR cites it by master path | Not decided | Medium |
| C-004 | Authorship evidence | The owner types or re-confirms the record in their own words | One dated owner sentence in the ledger confirming the existing files | None now | Medium |
| C-005 | Protection of the sibling worktree until the records are safe | Clean only after OB-01 is recorded | Clean only after the merge is verified | A dated "do not clean" ledger entry; admitted to be an instruction, not a mechanical guard | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | May an agent session commit owner text? | No: "the person who typed the record is the owner, which is the only defence against 'git cannot show who typed it'" | Yes, if verbatim and byte-checked: "Verbatim copying with a byte check is not writing" (while conceding the rule "agents may cite, never write", `release-gates.md:22`) | Not addressed | High |
| X-002 | Must OB-06 prerequisite (d) stay "committed in this PR"? | Yes, unchanged | No, reworded to "already on master and cited" | Not addressed (OB-06 simply cannot open) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | Names that the owner's commit route on this host (which session, which worktree) is unspecified in the spec | Medium |
| U-002 | B | Decouples saving the records from the switch-on, so records reach master even if the switch-on never happens; byte-comparison check | High |
| U-003 | C | Exact inventory of what is at risk today, including `handoff-mvp-brainstorm.md` (not named by the spec), and the single-disk loss risk (no remote branch holds the commits) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three treat the sibling's files as the owner's records to be saved as they are | The sibling's files still hold exactly what the owner wrote; no later session edited them (the commits that hold the pass record were made in an agent-run worktree; git cannot show who typed it) | UNSTATED | Yes |
| A-002 | A and B put the records on master; C defers | The owner is content for these records, which contain personal statements and the owner's name, to sit in the repository (a private fork) | UNSTATED | Yes |
| A-003 | All three | Cleaning the sibling before the records are saved loses them (`merged-requirements.md:264`) | STATED (all) | No |

### Promoted shared assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The sibling's files are unedited owner text | All three save or freeze them as is | If false, committing them (A or B) puts non-owner text on master under the owner's name | Open (only the owner can confirm) |
| A-002 | The owner accepts these records in the repository | A and B | If false, archive outside git is the only route; C's freeze becomes the bridge | Open (owner's preference) |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L3 (guard and state): C-005, X-001, X-002, A-001; L2 (structure and dependency): C-001, C-002, C-003, C-004, A-002; L1: S-001.

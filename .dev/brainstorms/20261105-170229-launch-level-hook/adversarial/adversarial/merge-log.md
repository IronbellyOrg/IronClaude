# Merge Execution Log

## Metadata

- Base: Variant 1 (opus:architect), `variant-1-opus-architect.md`
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (34 changes, after fix cycles 1 and 2)
- Final review applied as amendments: `plan-review-3.md` (B-1 to B-10, m-1 to m-11)
- Changes applied: 34 of 34 planned; 10 of 10 amendments; 11 of 11 minor findings; 1 orchestrator addition (O-22); 4 owner additions (2026-11-05)
- Status: partial. Every planned change and amendment was applied, but the specification is NOT approved: the final review failed with 10 blocking findings, the amendments that answer them are unreviewed, and the owner stopped review rounds on 2026-11-05.
- Timestamp: 2026-11-05
- Output: `../merged-output.md` (1 folder up from this log), 14 H2 sections, front matter `adversarial_status: partial`, `review_status: not reviewed after the last amendments (fix cycle 2 and the amendments from plan-review-3)`

Provenance format: every block of the merged output carries `<!-- Source: ... -->` (78 tags). Every amended rule carries the inline marker `[AMENDMENT B-n: reviewer-tested on a copy, not independently re-reviewed]`; minor findings carry `[m-n]`. In the decision table and the test table, the short form `[B-n]` is used per example, with the full marker stated once in the table's introduction. No em dashes are used (template Section 6 shows one in a tag example; it was replaced by a semicolon).

## Structural mapping (orchestrator section list replaces Change 1 item 3)

Change 1 asked for 18 sections in Variant 1's order. The orchestrator's instruction for this step fixes 14 sections in a different order. The orchestrator's list was used; every plan section has a home:

| Plan section (Change 1) | Merged output |
|---|---|
| 1 Position summary, Terms | 1 Summary and scope (1.1, 1.4) |
| 2 Threat model; 17 Residual risks | 2 Threat model and residual risks |
| 18 Rejected alternatives | 3 Decisions D1 to D7 (rejected alternatives per decision) |
| 3 Components and files | 1.3 Files; 4.5 Registration and install; 4.6 Interface requests |
| 4 Session identity and state; 6 Human approval; 7 Subagents; 8 Bash, Monitor and git; 9 Other tools; 10 Fail-closed | 4 Functional requirements FR-L-01 to FR-L-66 |
| 10 Speed budget; Change 3 size estimate | 5 Non-functional requirements NFR-L-01 to NFR-L-06 |
| 5 Decision table and policy | 6 Decision table (6.1 grid, 6.2 patterns) |
| 11 Block messages | 7 Block messages |
| 12 Test plan | 8 Test plan |
| 13 Acceptance criteria map | 9 Acceptance criteria map |
| 14 Order of work | 10 Order of work |
| 15 Open decisions | 11 Open decisions for the owner |
| 16 Unverified items | 12 UNVERIFIED items |
| (new) | 13 Unresolved blocking findings; 14 Debate record |

Front matter: the orchestrator's fields (`domain`, `strategy`, `status: draft requirements, not implemented`, `base`, `adversarial_status`, `generated`) replace Change 1 item 1's `status: design only, nothing implemented` and `created`; `issue` and `merged_from` from Change 1 were kept.

Cross-references: every "Change N" reference in rule text was rewritten to the FR-L, NFR-L, section or row id that now holds the rule. Change numbers survive only in provenance comments (checked: 0 "Change N" references outside comments).

## Changes Applied

### Change 1: Spec frame, skeleton and defined terms
- **Status**: Applied, with the orchestrator's section list (see Structural mapping)
- **Source**: Variant 1 front matter and section list; Variant 3 H1
- **Target**: front matter, H1, section 1.4 Terms
- **Before**: Variant 1 front matter, 16 sections, terms undefined before use (scoring L4)
- **After**: orchestrator front matter plus `issue`, `merged_from`, `review_status`; H1 from Change 1 item 2 with ": requirements specification"; Terms list with the id families, extended by NM1a, PA/PR/PD (m-3), FR-L, NFR-L, IR, U21 to U28, O-22, OD-R1/R2/R3 and the "review-1 B-n" convention
- **Provenance tag**: `<!-- Source: refactor-plan Change 1 item 4 (scoring note L4), id families extended for this merge -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 2: Threat model
- **Status**: Applied
- **Source**: Variant 1 section 2; Variant 2 section 2
- **Target**: section 2.1
- **Before**: Variant 1 T1 to T3 and an R1 to R8 table
- **After**: TH1 to TH3, same-user premise, harness facts V2, V3, V4, V5, V6, V8; plus a factual note on what the final review showed about TH2 coverage
- **Provenance tag**: `<!-- Source: refactor-plan Change 2 (Variant 1 section 2 targets, Variant 2 section 2 harness facts; A-004) -->`
- **Validation**: OK | OK | OK

### Change 3: Components and files
- **Status**: Applied
- **Source**: Variant 2 section 3; X-010
- **Target**: section 1.3 (table), NFR-L-03 (size estimate)
- **Before**: Variant 1 table naming a Makefile `_FRESHNESS_SCRIPTS` line
- **After**: 7-row table; `_FRESHNESS_SCRIPTS` only in `install_hooks.py`; size estimate moved to NFR-L-03 and raised per m-11
- **Provenance tag**: `<!-- Source: refactor-plan Change 3 (Variant 2 section 3, X-010) -->`
- **Validation**: OK | OK | OK

### Change 4: Store layout and file formats
- **Status**: Applied
- **Source**: Variant 2 section 4; C-003, C-006, INV-019
- **Target**: FR-L-01 to FR-L-07
- **Before**: JSON record and `.approved` file
- **After**: one-word files, `.ok` approval, id rule without dots, three-part store path, release command
- **Provenance tag**: `<!-- Source: refactor-plan Change 4 (Variant 2 section 4; C-003, C-006, INV-006, INV-019) -->`
- **Validation**: OK | OK | OK

### Change 5: Launch marker detection and binding
- **Status**: Applied
- **Source**: Variants 1 and 2; C-001, X-001, INV-001, INV-004, INV-014, INV-015
- **Target**: FR-L-09 (B1 to B13 and consequences)
- **Before**: Variant 1 steps 1 to 5 (30-minute age check)
- **After**: B1 to B13 verbatim; consequences list; O-20 cross-reference added to the strict-marker consequence
- **Provenance tag**: `<!-- Source: refactor-plan Change 5 (...) -->`
- **Validation**: OK | OK | OK

### Change 6: Session resolution and fast paths
- **Status**: Applied
- **Source**: Variants 1 and 2; C-016, INV-002, INV-024
- **Target**: FR-L-10 (P1 to P7), FR-L-11
- **Before**: Variant 1 fast paths 1 and 2
- **After**: P1 to P7 verbatim; "never reads `cwd` or `agent_id`" moved to FR-L-11 with the other "never" statements
- **Provenance tag**: `<!-- Source: refactor-plan Change 6 (...) -->`
- **Validation**: OK | OK | OK

### Change 7: Subagents and the U1 ship gate
- **Status**: Applied
- **Source**: Variant 2 section 7, Variant 1 section 7; C-002, X-004
- **Target**: FR-L-12, FR-L-13, FR-L-14
- **Before**: Variant 1 section 7 and the cwd fallback paragraph
- **After**: identity by `session_id` only; ship gate (OB-H1 items 1 and 5); reserve design as text only
- **Provenance tag**: `<!-- Source: refactor-plan Change 7 (...) -->`
- **Validation**: OK | OK | OK

### Change 8: Human approval
- **Status**: Applied
- **Source**: Variant 2 section 6, Variant 1 section 6 item 2; C-005, C-006, U-006, INV-008
- **Target**: FR-L-15 to FR-L-19
- **Before**: Variant 1 approval by UserPromptExpansion and UserPromptSubmit
- **After**: UserPromptSubmit only; exact match; `.ok` at `worktree` only; forgery paragraph (U4, O-17)
- **Provenance tag**: `<!-- Source: refactor-plan Change 8 (...) -->`
- **Validation**: OK | OK | OK

### Change 9: Normalisation for Bash and Monitor text
- **Status**: Applied, then amended by B-1 (new NM1a), B-2 (`sed` expression) and B-6 (segment split always)
- **Source**: Variants 1 and 2; C-007, INV-016, INV-022; F-1, F-6
- **Target**: FR-L-22 to FR-L-27
- **Before**: Variant 1 word split on quotes and `$`
- **After**: NM1 cap, NM1a (B-1), NM2/NM3 `sed` (B-2 form), NM4 text G, NM5/NM6 text W, segments always split (B-6), NM7; worked example plus the B-2 example
- **Provenance tag**: `<!-- Source: refactor-plan Change 9 NM2 and NM3 (...), amended per plan-review-3 B-2 -->` and similar per FR
- **Validation**: OK | OK | conflict noted (B-1, B-6 below)

### Change 10: Git classification G0 to G4
- **Status**: Applied, then amended by B-3 (G0 PUSH words, G1 regex, G2 replaced, G3 reserved words), B-10 (G3 "No S") and m-9 (number pattern)
- **Source**: Variant 1 section 8 step 3; C-007, C-008, X-008, INV-011, INV-017, INV-021, INV-034
- **Target**: FR-L-28 to FR-L-32
- **Before**: Variant 1 option skip with a denylist
- **After**: G0 to G4 as planned, with the amendments marked; consequences folded into FR-L-29 and FR-L-31
- **Provenance tag**: per FR, for example `<!-- Source: refactor-plan Change 10 G3 (...), amended per plan-review-3 B-3 and B-10 and minor m-9 -->`
- **Validation**: OK | OK | conflict noted (B-3 below)

### Change 11: Push canonical form
- **Status**: Applied; named cases renamed per m-3
- **Source**: C-009, X-007, INV-012; review-1 B-1 to B-3; F-2; fact T3
- **Target**: FR-L-33, FR-L-34
- **Before**: Variant 1 branch words plus `symbolic-ref`
- **After**: anchored ERE on the raw command; PA1 to PA13, PR1 to PR30, PD1 to PD5; destination step; consequences
- **Provenance tag**: `<!-- Source: refactor-plan Change 11 items 1 and 2 (...), named cases renamed per plan-review-3 m-3 -->`
- **Validation**: OK | OK | derived note added: PR8 and PR9 also collect UNKNOWN under the amended G2 (see Contradiction re-scan)

### Change 12: gh rule and merge URLs
- **Status**: Applied, then amended by B-3 (H3 clauses 3 and 4), B-7 (H5 item 2) and m-9 (H3 clause order)
- **Source**: Variants 1, 2, 3; C-010, INV-013; review-1 B-4; F-3, F-8
- **Target**: FR-L-35 to FR-L-39
- **Before**: Variant 1 `gh pr merge`, `/merge` URL and record `repo` check
- **After**: H1 to H5 with the canonical GET form, the allowlist in a stated order, explicit `--repo` word, merge URLs and direct GitHub API calls
- **Provenance tag**: per FR
- **Validation**: OK | OK | conflict noted (B-3 below)

### Change 13: MCP tools
- **Status**: Applied
- **Target**: FR-L-45
- **Before**: Variant 1 name regex
- **After**: four-step rule with read prefixes; MCP class blocked at every level (O-14)
- **Provenance tag**: `<!-- Source: refactor-plan Change 13 (Variant 1 section 9; C-013, INV-013) -->`
- **Validation**: OK | OK | OK

### Change 14: Skill classification
- **Status**: Applied, amended by m-5
- **Target**: FR-L-40
- **Before**: Variant 1 literal name lists
- **After**: normalised name; leading whitespace removed first and an empty result is SKILL (m-5)
- **Provenance tag**: `<!-- Source: refactor-plan Change 14 (...), amended per plan-review-3 minor m-5 -->`
- **Validation**: OK | OK | OK

### Change 15: Escape routes
- **Status**: Applied, amended by B-8 and m-6
- **Target**: FR-L-46 (tools), FR-L-47 (`orca`), FR-L-48 (ccsession, claude, terminal tools)
- **Before**: Variant 1 `orca` denylist and `claude` plus any dash word
- **After**: `orca` allowlist with `-h`/`--help` only as the last word (m-6); `claude` basename stripped from its first `@` (B-8)
- **Provenance tag**: per FR
- **Validation**: OK | OK | OK

### Change 16: Turn starters
- **Status**: Applied
- **Target**: FR-L-43 (TURN), FR-L-44 (Monitor and background calls)
- **Before**: Variant 1 Cron, Schedule, RemoteTrigger, Workflow all ESCAPE
- **After**: TURN at `W` only; Monitor and background calls allowed and scanned (O-17)
- **Provenance tag**: `<!-- Source: refactor-plan Change 16 (...) -->`
- **Validation**: OK | OK | OK

### Change 17: Tamper rule
- **Status**: Applied, amended by B-4 (token `.config/git`) and B-9 (`superclaude` basename)
- **Target**: FR-L-49, FR-L-50, FR-L-51
- **Before**: Variant 1 substrings including `launch-level-guard`
- **After**: tokens on T and path fields; Bash-only words; `..` paths; governed only
- **Provenance tag**: per FR
- **Validation**: OK | OK | OK

### Change 18: Remaining tools
- **Status**: Applied
- **Target**: FR-L-42 (Edit, Write, NotebookEdit), FR-L-52 (other tools)
- **Before**: Variant 1 section 9 rows
- **After**: tamper check only on edits; the AC-1 command-level sentence; explicit NONE path
- **Provenance tag**: `<!-- Source: refactor-plan Change 18 ... -->`
- **Validation**: OK | OK | OK

### Change 19: Classes, policy table and precedence
- **Status**: Applied
- **Target**: FR-L-20 (list, precedence, `case` table, oracle) and section 6.1 (grid)
- **Before**: Variant 1 class list and precedence line
- **After**: 17 classes, 17-row grid, 16-class precedence order
- **Provenance tag**: `<!-- Source: refactor-plan Change 19 ... -->`
- **Validation**: OK | OK | OK (grid matches the class list: 17 of 17)

### Change 20: Decision table
- **Status**: Applied, with examples added by B-2, B-3, B-4, B-5, B-7, B-8, B-9, B-10 and the m-4 row-31 fix
- **Target**: section 6.2 (rows 1 to 38 with 11a, 17a, 32a)
- **Before**: Variant 1 20 generic rows
- **After**: 41 rows of literal commands; amendment examples marked `[B-n]`; `gh pr update-branch` and `gh repo sync` moved from row 18 to row 17 (B-3); classes of amendment examples derived from the amended rules, not run
- **Provenance tag**: `<!-- Source: refactor-plan Change 20 (...), amended per plan-review-3 B-2, B-3, B-4, B-5, B-7, B-8, B-9, B-10 and minor m-4 -->`
- **Validation**: OK | OK | conflict noted (B-3 row move)

### Change 21: Fail-closed rules
- **Status**: Applied
- **Target**: FR-L-53 to FR-L-57
- **Before**: Variant 1 ERR and EXIT traps and failure table
- **After**: default deny, EXIT trap from P4, checked tool status, failure table, no `onFailure`
- **Provenance tag**: `<!-- Source: refactor-plan Change 21 (...) -->`
- **Validation**: OK | OK | OK

### Change 22: Size cap, timeout and speed budget
- **Status**: Applied
- **Target**: FR-L-23 (cap), FR-L-58 (timeout), FR-L-59 (subprocesses), NFR-L-01, NFR-L-02
- **Before**: Variant 1 medians over 30 runs, push up to 2 s
- **After**: 65,536-byte cap, one 5 s timeout, 100-run budget table with only the ratio and the 1-second line asserted; note that the amendments were not timed
- **Provenance tag**: `<!-- Source: refactor-plan Change 22 ... -->`
- **Validation**: OK | OK | OK

### Change 23: Block messages
- **Status**: Applied, with LL-UNKNOWN amended by B-1 and LL-GH-WRITE by B-7
- **Target**: section 7, FR-L-21
- **Before**: Variant 1 13 ids with an issue-number header
- **After**: 18 ids in the three-line shape, two notes, header without issue number (O-5)
- **Provenance tag**: `<!-- Source: refactor-plan Change 23 item 2 (...), LL-UNKNOWN amended per plan-review-3 B-1, LL-GH-WRITE amended per plan-review-3 B-7 -->`
- **Validation**: OK | OK | OK

### Change 24: Registration
- **Status**: Applied
- **Target**: FR-L-08 (event dispatch), FR-L-60 to FR-L-66
- **Before**: Variant 1 three events, no matcher
- **After**: two entries, anchored matcher, timeout 5, no UserPromptExpansion; U21 note added from m-7
- **Provenance tag**: `<!-- Source: refactor-plan Change 24 items 1 to 3 (...) -->`
- **Validation**: OK | OK | OK

### Change 25: Interface requests to the claim feature
- **Status**: Applied, ids renamed CL-1 to CL-6 to IR-1 to IR-6 (the orchestrator's section list asks for "IR-1.."); the old ids are named once in section 4.6
- **Target**: section 4.6
- **Before**: Variant 1 R1 to R3 (collided with residual ids)
- **After**: IR-1 to IR-6; one sentence that an O-22 request is not yet written
- **Provenance tag**: `<!-- Source: refactor-plan Change 25 (...); ids renamed CL-n to IR-n per the orchestrator's section list -->`
- **Validation**: OK | OK | OK

### Change 26: Test harness, oracle and fixtures
- **Status**: Applied
- **Target**: section 8.1
- **Provenance tag**: `<!-- Source: refactor-plan Change 26 (...) -->`
- **Validation**: OK | OK | OK

### Change 27: Named test cases and regression corpus
- **Status**: Applied, with B-1 to B-10, m-3, m-5, m-6 test changes; amendment corpus added as section 8.4
- **Target**: sections 8.2 (140 named test ids plus T-SPD-1..5), 8.3 (103 corpus rows verbatim), 8.4 (39 N-ATK rows)
- **Before**: Variant 1 group table
- **After**: new tests T-NRM-8, T-GIT-18, T-GH-13, T-GH-14; T-GIT-17 replaced (B-10); T-GH-1 and T-GH-9 adjusted (B-3); T-NRM-1, T-ESC-1, T-TAM-2, T-TAM-6, T-PSH-8, T-GAP-1, T-TRN-4 extended; T-SKL-1, T-SKL-4 (m-5) and T-ESC-2 (m-6) extended; the review's unnumbered two-step attack given the id N-ATK-39. The "Expected" column of section 8.4 is derived in this merge from the amended rules and FR-L-20 precedence; it was not run.
- **Provenance tag**: `<!-- Source: refactor-plan Change 27 (...), amended per plan-review-3 ... -->`, `<!-- Source: plan-review-3 section 3.1 (...) -->`
- **Validation**: OK | OK | OK

### Change 28: Acceptance criteria map
- **Status**: Applied, with the final review's verdicts (owner instruction 3)
- **Target**: section 9
- **Before**: plan rows with "Covered / Not covered" text
- **After**: verdict column exactly as `plan-review-3.md` section 6 (AC-1, 2, 3, 5, 6 NOT MET; AC-4, 8 MET WITH CAVEAT; AC-7 MET), the review's reason, requirements, at least two tests each, observed checks, "what the amendments change (unreviewed)", honest caveat; the AC-5 sentence of Change 28 kept in the AC-5 row; the O-22 combination statement in the AC-6 row
- **Provenance tag**: `<!-- Source: refactor-plan Change 28 (...); plan-review-3 section 6 (...); owner decision 2026-11-05 (...) -->`
- **Validation**: OK | OK | OK

### Change 29: Observed checks
- **Status**: Applied, amended by m-7 (OB-H1 item 9) and m-10 (OB-H3 counts)
- **Target**: section 8.5
- **Provenance tag**: `<!-- Source: refactor-plan Change 29 (...), amended per plan-review-3 minors m-7 and m-10 -->`
- **Validation**: OK | OK | conflict noted (m-7 below)

### Change 30: Order of work
- **Status**: Applied, with step 7a for O-22 and a lead sentence
- **Target**: section 10
- **Provenance tag**: `<!-- Source: refactor-plan Change 30 (...); step 7a from the orchestrator's owner decision O-22 -->`
- **Validation**: OK | OK | OK

### Change 31: Unverified register
- **Status**: Applied; U21 added (m-7); U22 to U28 added to collect UNVERIFIED tags the documents already carry (BSD `sed`, `send-pack` over https, gh alias expansion, `orca -h` as a value, tmux reachability, `transcript_path` at first call, Orca hook sharing); no new rule
- **Target**: section 12
- **Provenance tag**: `<!-- Source: refactor-plan Change 31 (...); U21 from plan-review-3 minor m-7; U22 to U28 collect UNVERIFIED tags from plan-review-3, O-16 and O-22 -->`
- **Validation**: OK | OK | OK

### Change 32: Residual risks
- **Status**: Applied, amended by B-1 (R8 h), B-3 (R8 d and i, R11, R17), B-4 (R17), B-5 (R1, R3), B-7 (R8 b, R10), B-10 (R9), m-1 and m-2 (R8 a, c), m-8 (R1)
- **Target**: section 2.2
- **Before**: Variant 1 R1 to R8 table
- **After**: R1 to R17 plain statements; R1 names the three accepted leaks T-ATK-26, 27, 28 and N-ATK-7; R1 and R3 point to O-7, O-16 and O-22
- **Provenance tag**: `<!-- Source: refactor-plan Change 32 (...), amended per plan-review-3 B-1, B-3, B-4, B-5, B-7, B-10 and minors m-1, m-2, m-8 -->`
- **Validation**: OK | OK | OK

### Change 33: Open decisions for the owner
- **Status**: Applied; O-7 and O-16 text aligned with B-5 (glob, brace expansion); O-7 alternative (b) now points to O-22; O-22 added (orchestrator); OD- entries added (owner)
- **Target**: section 11
- **Provenance tag**: `<!-- Source: refactor-plan "Open decisions for the owner" (...), O-7 and O-16 text aligned with plan-review-3 B-5; O-22 added by the orchestrator -->`
- **Validation**: OK | OK | OK

### Change 34: Rejected alternatives
- **Status**: Applied inside section 3 (Decisions D1 to D7), not as a separate section 18 (orchestrator section list)
- **Target**: section 3
- **After**: every "alternative" row of the plan's "Changes NOT Being Made" table appears under its decision with the debate evidence; the git-level hooks row keeps the corrected X-009 reason and now says it is reopened as O-22
- **Provenance tag**: `<!-- Source: seed-brief contested questions D1 to D7; refactor-plan Change 34 and "Changes NOT Being Made" (...) -->`
- **Validation**: OK | OK | OK

## Amendments from the final review (B-1 to B-10)

All ten carry `[AMENDMENT B-n: reviewer-tested on a copy, not independently re-reviewed]`. Status of each: amended, not re-reviewed (OD-R3-B1 to OD-R3-B10).

### B-1: Line continuation inside a word
- **Status**: Applied
- **Before**: no step; Change 9 rationale said an extra word or segment can only add a class
- **After**: FR-L-24 (NM1a, regex verbatim); the rationale sentence replaced in FR-L-25 ("the one case where this hides a word is UNKNOWN by NM1a"); LL-UNKNOWN "Blocked:" and "You can:" appended; R8 (h); T-NRM-8; corpus rows N-ATK-1, 2, 14, 17, 19, 25, 28, 29, 34
- **Conflict with plan text**: N-ATK-14 was PUSH/PUSHFORM under the plan and is UNKNOWN after NM1a (precedence); T-ATK-56 (`-X\` newline) also matches NM1a but keeps GHWRITE by precedence. Amended text kept.

### B-2: `$''` and `$""` splices
- **Status**: Applied
- **Before**: `sed -E -e "s/['\"\\\\]//g" ...`
- **After**: `sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" ...` verbatim in FR-L-25; NM2 prose first sentence replaced; worked-example line added; T-NRM-1 and section 8.4 rows N-ATK-3, 4, 15, 16, 18, 23, 24, 30, 32, 33
- **Conflict with plan text**: none

### B-3: Hidden command position; `send-pack`, redirects, gh merges
- **Status**: Applied
- **Before**: G0 PUSH word `push`; G2 alias rule; G3 skip list without shell keywords; H3 "Action `merge`: MERGE"; R11 and R17 as planned
- **After**: G0 adds `send-pack`, `http-push` (FR-L-28); G1 regex `(push|send-pack|http-push)` (FR-L-29); G2 replaced verbatim (FR-L-30); G3 skips `if then else elif do while until coproc` (FR-L-31); FR-L-31 rationale reworded in the consequences; H3 clauses 3 and 4 (FR-L-37); R11 and R17 replaced or appended; R8 (d) and (i); T-GIT-18, T-GH-13; `gh pr update-branch 5` and `gh repo sync` moved from row 18 to row 17 and from T-GH-9 to T-GH-1
- **Conflicts with plan text, amended text kept**: (1) the plan's Change 12 rationale said `gh pr update-branch` and `gh repo sync` "fall to UNKNOWN"; they are MERGE now (still blocked at every level). (2) The plan's G3 read forms make `git config --get ...` NONE; the amended G2 makes `git config --get remote.origin.url` UNKNOWN; FR-L-31 now says "G2 still applies to these forms". (3) PR8 and PR9 (`-c remote.origin.push=...`, `--config-env=remote.origin.push=...`) now also collect UNKNOWN, which precedes PUSHFORM; FR-L-33 and T-PSH-12 accept either message. (4) The plan's G1 text spoke of "five" regex tests; the count is not restated.

### B-4: Git config file outside the tamper list
- **Status**: Applied
- **After**: token `.config/git` in FR-L-49; R17 replacement text; T-TAM-2 and T-PSH-8 additions; decision table row 3; N-ATK-39
- **Conflict with plan text**: none

### B-5: Glob and brace spellings unlisted
- **Status**: Applied (residual text only, as the review proposed)
- **After**: R1 and the AC-6 row name globs and brace expansion; R3, O-16 "Why the default" name brace expansion; `/usr/bin/gi[t] push origin main` added to row 33 and T-GAP-1. For consistency O-7's question also names the glob form (derived from B-5; the review did not name O-7). The INV-037 note is not part of the merged output (the probe table was not carried over), so that part of B-5 has no target.
- **Conflict with plan text**: none

### B-6: Segment split skipped
- **Status**: Applied
- **After**: FR-L-27 "W is always split at `;` into segments"
- **Conflict with plan text**: the plan's corpus was produced without the trigger condition; after B-6 the rule text and the corpus agree (the review's section 2)

### B-7: REST write through `curl`
- **Status**: Applied
- **After**: FR-L-39 item 2; LL-GH-WRITE "Blocked:" appended; R10 replaced; R8 (b) cost; T-GH-14; N-ATK-26
- **Conflict with plan text**: T-ATK-48 (`curl -X PUT .../pulls/5/merge`) now also collects GHWRITE; MERGE precedes GHWRITE, so its row is unchanged

### B-8: Versioned `npx` Claude Code
- **Status**: Applied
- **After**: FR-L-48 item 2 (basename stripped from its first `@`); row 25; T-ESC-1
- **Conflict with plan text**: none

### B-9: Reinstall through the module name
- **Status**: Applied
- **After**: FR-L-50 item 2; row 27; T-TAM-6
- **Conflict with plan text**: none

### B-10: `/sc:implement` retry block UNKNOWN
- **Status**: Applied
- **After**: FR-L-31 "No S" bullet replaced verbatim; R9 appended; T-GIT-17 replaced; row 12 addition
- **Conflict with plan text**: the plan's AC-2 row claimed `/sc:implement`'s git commands stay allowed at `F`, which the review showed false for the retry block; the section 9 AC-2 row now carries the review's verdict and says what B-10 changes

## Minor findings of the final review (m-1 to m-11)

| Finding | Status | Where |
|---|---|---|
| m-1 `git stash push` never runs | Applied | R8 (a), with the way round `git stash -u -m <msg>` |
| m-2 `git config user.email`, `"HEAD^{commit}"` | Applied as residual statements (the review's first option; the read-form widening was not taken) | R8 (a), R8 (c) |
| m-3 id collisions of push cases | Applied | PA1 to PA13, PR1 to PR30, PD1 to PD5 in FR-L-33, FR-L-34, T-PSH-4, T-PSH-11, T-PSH-12 |
| m-4 row 31 class column | Applied | row 31: "UNKNOWN (and COMMIT for the first two examples)" |
| m-5 Skill name with leading whitespace | Applied | FR-L-40 item 2; T-SKL-1, T-SKL-4 |
| m-6 `orca -h` as an option value | Applied | FR-L-47 (`-h`/`--help` only as the last word); U25; T-ESC-2 |
| m-7 harness tool names | Applied | U21; OB-H1 item 9; FR-L-62 note; AC-4 row. Conflict: OB-H1 runs before the claim feature exists, so the item records the names of the session where OB-H1 runs until a claim-launched session exists (stated in OB-H1) |
| m-8 git hooks as a script route | Applied | R1 |
| m-9 G3 number pattern; H3 clause order | Applied | FR-L-31 (`^[0-9]+(\.[0-9]+)?[smhd]?$`); FR-L-37 ("first matching clause in the order written") |
| m-10 OB-H3 counts NM1a and G2 blocks | Applied | OB-H3 |
| m-11 size estimate | Applied | NFR-L-03 (about 425 to 475 lines; the 500-line cut threshold unchanged) |

Skipped: none.

## Orchestrator addition

### O-22: Text classifier only, or add a structural git-level layer?
- **Status**: Applied as written by the orchestrator
- **Target**: section 11.1 row O-22; section 11.3 (facts, alternative L2, weaknesses, recommendation, open questions); section 10 step 7a; AC-6 row of section 9; D4 in section 3 (git-level hooks "reopened as O-22"); R1; O-7 alternative (b); U28
- **Before**: the debate rejected git-level hooks (X-009, unanimous Variant 1; plan Change 34)
- **After**: owner decision with the orchestrator's default (include L2 as a small hardening step, keep the text layer, AC-6 wrapper clause met only by the combination); L2 not designed; five open questions. The cross-references from the L2 weaknesses to FR-L-33 (`--no-verify` fails the push form), FR-L-30 (`hookspath`) and FR-L-28 (`send-pack`) are derived from the rules in this document. Open question 2 (existing pre-commit hooks under a per-worktree hooks path) is derived from the project instructions and marked UNVERIFIED.
- **Provenance tag**: `<!-- Source: orchestrator instruction for Step 5 (owner decision O-22, written by the orchestrator); ...; Departs from the debate's X-009 rejection of git-level hooks (D4) -->`

## Owner additions (decision of 2026-11-05, relayed by the orchestrator)

### A-1: Section 11.2, one entry per blocking finding of the three reviews
- **Status**: Applied
- **After**: 26 entries: OD-R1-B1 to OD-R1-B8, OD-R2-F1 to OD-R2-F8, OD-R3-B1 to OD-R3-B10, each with what leaks or breaks, the rule or amendment now in the spec, a status, a default decision and an alternative
- **Status rule used**: closed only where a later review file re-ran the case and reports the stated result. For review 1, `plan-review-2.md` section 1 gives a per-finding verdict. For review 2, `plan-review-3.md` gives no per-finding verdict; the evidence used is its re-run of the plan's corpus rows and named push cases (sections 1 and 2), and each such entry names the rows. OD-R1-B8 was "PARTLY" in review 2; it is marked closed with the remainder carried to OD-R2-F8, which review 3's corpus re-run reproduced (T-OK-16). OD-R2-F4 and OD-R2-F5 are not marked closed because review 3 (B-2, B-5) found their residual statements still incomplete.
- **Counts**: 14 closed, 2 fixed in a fix cycle but not confirmed, 10 open

### A-2: Review status field and banner
- **Status**: Applied
- **After**: front matter `review_status: not reviewed after the last amendments (fix cycle 2 and the amendments from plan-review-3)`; a one-paragraph banner directly under the H1 with the four required statements; the section 1 status paragraph points to sections 9, 11.2 and 13

### A-3: Section 13 consistent with section 11.2
- **Status**: Applied
- **After**: section 13 keeps one row per final-review finding (id, short name, OD- entry, FR-L, status "amended, not re-reviewed") and refers to section 11.2 for what each leaks, its default and its alternative; it also names the two unconfirmed earlier fixes

### A-4: Section 9 keeps the verdicts and states the amendments' effect
- **Status**: Applied
- **After**: verdict column exactly as the final review; new column "What the amendments change (unreviewed)"; a lead paragraph saying no verdict has changed

## Post-Merge Validation

All checks were run with `grep`, `awk`, `sort` and `comm` on the written `merged-output.md` (final state: 1,484 lines, 204,581 bytes). The defined-versus-used comparison was run before the last three small text edits; the occurrence counts below are from a final recount after them.

### Structural Integrity
- Heading hierarchy: OK. 1 H1, 14 H2 (the orchestrator's 14 sections, in order), 42 H3, 78 H4. The first run found one level jump (H2 to H4 at section 5, line 778); the six NFR headings were raised to H3 and the re-run found 0 jumps.
- Section ordering: OK. H2 order 1 to 14 matches the orchestrator's list.
- Document flow: OK. 0 `FILL:` placeholders left; 0 em dashes; 0 en dashes; 0 "Change N" references outside provenance comments; 78 `<!-- Source: ... -->` tags.

### Internal References

Each id family was extracted with `grep -oE`, the set of defined ids (heading, table row or list label where the id is introduced) compared with the set of ids used anywhere (`comm`).

| Family | Defined | Used (distinct) | Occurrences | Undefined | Unused |
|---|---|---|---|---|---|
| FR-L-nn | 66 | 66 | 330 | 0 | 0 |
| NFR-L-nn | 6 | 6 | 12 | 0 | 0 |
| O-n | 22 | 22 | 152 | 0 | 0 |
| OD-R1/R2/R3 | 26 | 26 | 56 | 0 | 0 |
| R-n (residuals) | 17 | 17 | 155 | 0 | 0 |
| U-n | 28 | 28 | 75 | 0 | 0 |
| IR-n | 6 | 6 | 21 | 0 | 0 |
| OB-H | 3 | 3 after fix | 73 | 0 after fix | 0 |
| LL- message ids and notes | 20 | 20 | 270 | 0 | 0 |
| Named tests T-GROUP-n | 140 (plus T-SPD-1..5 as one row) | 140 | 367 | 0 | 0 |
| Corpus T-ATK, T-OK, T-OVR | 103 | 103 | 146 | 0 | 0 |
| N-ATK-n | 39 | 39 | 67 | 0 | 0 |
| D1 to D7 | 7 | 7 | 14 | 0 | 0 |
| PA, PR, PD push cases | 48 | 48 | 75 | 0 | 0 |
| B1 to B13 bind steps | 13 | 13 | 67 | 0 | 0 |
| P1 to P7 | 7 | 7 | 26 | 0 | 0 |
| NM steps | 8 | 8 | 46 | 0 | 0 |
| G0 to G4 | 5 | 5 | 57 | 0 | 0 |
| H1 to H5 | 5 | 5 | 89 | 0 | 0 |
| TH1 to TH3 | 3 | 3 | 14 | 0 | 0 |
| AC-1 to AC-8 | 8 | 8 | 68 | 0 | 0 |

- Total references counted: 2,180 occurrences across these families (final recount). Occurrence counts are token matches, so a short family such as `H1` to `H5` may include a few tokens that are not rule references; the defined-versus-used comparison is what decides "broken".
- Broken found and fixed: 1. `OB-H5` appeared once, in a provenance comment naming Variant 2's own observed-check ids; the comment was reworded ("Variant 2's five observed checks").
- Check-script false positive: `NM6` was reported undefined only because the definition regex did not match its prose definition in FR-L-27; it is defined there (checked by `grep`).
- OD entries: 26; 25 cite at least one FR-L id and every cited FR-L id exists (FR-L family: 0 undefined); OD-R3-B5 cites no FR-L by design (residual text only: R1, R3, row 33, T-GAP-1).
- Remaining broken references: 0.

### Contradiction Re-Scan
- Timeout: one value, 5 s (FR-L-58 text and both JSON entries `"timeout": 5`); no other timeout value for the hook.
- Size cap: 65,536 bytes (7 mentions) and "64 KB" in LL-BIG and NFR-L-02 (3 mentions, the same number, stated as such in NFR-L-02); 65,537 bytes appears only in T-FC-7 as the first size over the cap; 1 MB only as a speed and BIG test input.
- Push ERE: stated once (FR-L-33).
- Precedence order: stated once (FR-L-20 item 3).
- Classes: the 6.1 grid holds exactly the 17 classes of FR-L-20 item 1 (diff empty); 18 message ids in section 7.2 plus 2 notes.
- Level names: file words `worktree`, `full`, `full-submit`, `degraded` (FR-L-02, FR-L-03); header renderings `worktree`, `worktree (approved)`, `full`, `full --submit` (section 7.1); effective levels `W`, `WA`, `F`, `FS` (section 1.4). No other spellings found.
- Gated-word lists: stated in FR-L-28 and repeated in R8 (a) with the same members (including the B-3 additions).
- Contradictions introduced by the amendments and resolved in text: G2 against the G3 `config` read forms (FR-L-31 says G2 still applies); PR8 and PR9 message (FR-L-33, T-PSH-12 accept either); `gh pr update-branch` and `gh repo sync` UNKNOWN to MERGE (stated under section 6.2); N-ATK-14 PUSH to UNKNOWN (stated in section 8.4).
- New unresolved contradictions found: 0. Limit: the classes given for the amendment examples in sections 6.2 and 8.4 are derived by reading the amended rules, not by running them; a contradiction between a derived class and the real behaviour of an implementation would not show here.

## Summary
- Total changes planned: 34
- Successfully applied: 34 (Change 1 with the orchestrator's section list; Change 34 inside section 3; Change 25 ids renamed IR-n)
- Amendments applied: 10 of 10 (B-1 to B-10), all marked unreviewed
- Minor findings applied: 11 of 11; skipped: 0
- Additions: O-22 (orchestrator); OD- entries, review status, banner, section 9 and 13 updates (owner)
- Failed: 0
- Counts in the output: 66 functional requirements (FR-L-01 to FR-L-66), 6 non-functional requirements, 6 interface requests, 22 owner design decisions (O-1 to O-22), 26 owner entries for review findings (14 closed, 2 fixed but unconfirmed, 10 open), 17 residuals, 28 unverified items, 145 named test functions (140 ids plus T-SPD-1 to T-SPD-5), 103 plan corpus rows, 39 amendment corpus rows, 3 observed checks
- Post-merge validation: PASS for structure and references (0 broken remaining). The specification itself is NOT approved and NOT reviewed after its last amendments.

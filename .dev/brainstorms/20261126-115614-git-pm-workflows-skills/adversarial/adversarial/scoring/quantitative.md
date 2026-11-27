# Quantitative Scoring (Step 3, quantitative layer)

- Inputs: `blind/variant-A.md` (378 lines), `blind/variant-B.md` (523 lines), `blind/variant-C.md` (121 lines), all read in full; `../../seed-brief.md`; `diff-analysis.md`; `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` §A.1.
- Weights and formula (protocol §A.1, same as the brief): `quant_score = 0.30*RC + 0.25*IC + 0.15*SR + 0.15*DC + 0.15*SC`.
- Protocol vs brief: they do not conflict. The brief fills in choices the protocol leaves open: topic matching for RC (protocol edge case "no formal requirement IDs"), the claim sample for IC and SR, and the reference types for DC. One nuance is noted under IC: the protocol's "vague statements are not scorable" exclusion is applied with the protocol's own vague-indicator terms.
- Counting was done with read-only regex passes over the three files (patterns below) plus a manual reading for coverage, contradictions and external section references. The same rules were applied to all three variants.

## Counting rules

**Item population (used by IC and SR).** An item is a numbered FR, NFR or AC entry at its defining position:
- a list line matching `^\s*(?:[-*]|\d+\.)\s+\*\*((?:N?FR|AC)-\d+[a-z]?)`; or
- a table row whose first cell is `AC-\d+` (only Variant A's AC table).

Lettered inserts (`FR-032a`, `FR-037a`, `FR-037b`) are separate items. An item's text runs from its defining line to the next item definition, the next T-table row, or the next markdown heading. This includes sub-bullets and embedded tables. The list marker (`- `, `1. `) is removed before scoring. T rows, decisions, risks and prose outside items are not items.

**RC.** The source requirements R1..R17 are the bullets under the seed brief's "Constraints" (6), "Success Criteria" (5) and "Open Questions" (6). A variant covers Ri only when both conditions hold:
- (a) at least one FR/NFR/AC/T item or decision in the variant addresses every clause of Ri (a clause is a part separated by `;` or a listed sub-topic); and
- (b) `diff-analysis.md` does not record that variant's position on Ri as conflicting with the seed brief.

Whether the variant's chosen answer is good is not judged here; that is the qualitative layer's job.

**IC.** IC = 1 - contradictions / scorable claims.
- Scorable claims are the items above. Items containing a protocol vague-indicator term (list under SR) would be excluded; no item contains one, so the denominator is the full item count.
- Contradictions are:
  - the diff-analysis rows marked "internal" (X-015, X-016, X-017, X-018, X-019; no other X row is marked internal); plus
  - pairs I found myself, where two explicit statements in the same variant oppose each other, a requirement conflicts with one of the variant's own constraints, or a sequence is impossible (the protocol's three categories).
- Rows that set a variant against the repository or against another variant (for example X-003, X-008, X-020, X-021) are not internal and are not counted.
- Each contradiction counts once.

**SR.** Every item is classified once.
- **Vague** if its text (code spans removed) contains a protocol vague-indicator term (`appropriate(ly)`, `as needed`, `properly`, `adequate(ly)`, `should consider`, `might`, `various`, `etc.`, `best practice(s)`, `industry standard`), or if it has no concrete indicator.
- **Concrete** if it has at least one concrete indicator and no vague term. The concrete indicators are:
  1. a backtick code span (a named command, flag, path, token or regex);
  2. a digit left after the item's own ID and internal cross-references are stripped (`(N?FR|AC|T|RC|R|D|Q)-?\d+` including ranges, `§N.N`, `section N`);
  3. a number word (`zero`..`twelve`, `once`, `twice`).
- SR = concrete / (concrete + vague). The vague-term list matched nothing anywhere in the three files, so every vague item here is vague because it has no concrete indicator.

**DC.** Internal references are tokens in the whole document, excluding each item's own defining occurrence:
- FR, NFR, AC and T IDs, matched by `(?<![A-Za-z0-9_-])((?:N?FR|AC|T)-\d+[a-z]?)(?![A-Za-z0-9])`. A range such as `FR-004–009` or `FR-031/032` counts as two tokens, its two endpoints.
- Decision references (A: `D1`..`D8`; B: `Q1`..`Q6` used as decisions, `D-7`; C: none).
- Section references in the forms `§N[.N]` and `section N[.N]` (any case).

A section reference that names another document (for example "developer guide §3.1" or "`research-deep.md` §2") is external and excluded, as are URLs and repository paths or line citations. Loop-step labels (`Q0`, `Q7`, `Q7b`, `Q8`, `Q8a`, `R0`, `L0`) and risk or root-cause IDs (`R1`.., `RC-1`.., "Risk N") fall outside the brief's list and are excluded. A reference resolves when its target is defined in the same variant: an item, a T row, a decision, or a numbered heading. DC = resolved / total.

**SC.** SC = the variant's count of lines starting with `## ` (H2) divided by the largest such count across the three variants.

## RC: requirement coverage

| R | Seed item (section) | A | B | C |
|---|---|---|---|---|
| R1 | Authorization limits: no commit without authorization; `/sc:git` never pushes, merges or opens PRs; destructive operations need confirmation (Constraints) | yes: FR-020, FR-004, FR-005, FR-022, D7 | **no**: FR-012 and FR-014 cover authorization, push and PR, but FR-006 and FR-013 keep a `merge` operation; diff-analysis X-002 records this as a conflict with the seed | yes: FR-010, FR-002, FR-007, FR-012 |
| R2 | Never stage `.claude/`; always stage `.dev/tasks`; preserve PR 288 (Constraints) | yes: FR-016, FR-061 step 3, FR-062, D8 | yes: FR-007, FR-014, FR-026, NFR-006 | yes: FR-009, FR-015, FR-016 |
| R3 | No installed primitive names a `src/...` path (Constraints) | yes: FR-009, NFR-010 | yes: NFR-001 | yes: FR-009, NFR-006 |
| R4 | Per-task commit outside the task body, never in a parallel batch (Constraints) | yes: FR-056 to FR-059 | yes: FR-024, FR-025 | yes: FR-013, FR-014 |
| R5 | Reuse `worktree_cleanup.py`; nothing deletes a remote branch (Constraints) | yes: FR-080, FR-081 | yes: FR-038 | yes: FR-029, FR-030 |
| R6 | Tests for authorization, commit timing, hook refusal and staged paths (Constraints) | yes: T-01, T-02, T-04, T-05, T-09, T-15, T-16 | yes: T-04, T-05, T-07, T-08, AC-11 | yes: FR-033, FR-034 |
| R7 | Modular `/sc:git` (options, STOP, outputs, boundaries) per developer guide; source, plugin and dev copy in sync; fate of `commands/sc-git.md` decided (Success) | yes: FR-001 to FR-005, FR-014 to FR-016 | yes: FR-001, FR-007, FR-008 | yes: FR-004, FR-008, FR-009 |
| R8 | Authorized between-task commit with a conventional message, intended paths plus `.dev/tasks`, no commit in a batch, hook refusal reported (Success) | yes: FR-050, FR-058, FR-062, FR-064, FR-066 (commits the package directory, not all of `.dev/tasks`; diff-analysis X-005 records this as a difference between variants, not a seed conflict) | yes: FR-022, FR-025, FR-026, FR-028, FR-030 | yes: FR-011, FR-014, FR-015, FR-016, FR-019, FR-020 |
| R9 | Submodule status, update and commit-pointer under the same authorization rules (Success) | yes: FR-040 to FR-042, §3 table | yes: FR-012, FR-033 to FR-035 | yes: FR-012, FR-024 to FR-027 |
| R10 | No second local branch cleanup; no remote branch deletion (Success) | yes: FR-080 to FR-082 | yes: FR-038, FR-039 | yes: FR-029, FR-030 |
| R11 | `make verify-sync` and related tests pass (Success) | yes: FR-016, T-18, AC-15 | yes: FR-007, NFR-008, AC-05, AC-06 | yes: FR-009, FR-036, AC-08 |
| R12 | Command-only vs command plus skill (Open Q) | yes: D1 | yes: Q1 | yes: Decision 1 |
| R13 | How `/sc:implement` calls the commit step (Open Q) | yes: D2 | yes: Q2 | yes: Decision 2 |
| R14 | Authorization switch (Open Q) | yes: D3 | yes: Q3 | yes: Decision 3, FR-011 |
| R15 | Submodule operations in scope; dirty and detached cases (Open Q) | yes: D4 | yes: Q4 | yes: Decision 4 |
| R16 | Fate of `commands/sc-git.md` (Open Q) | yes: D5 | yes: Q5 | yes: Decision 5 |
| R17 | Residual project-management scope (Open Q) | yes: D6 | yes: Q6 | yes: Decision 6 |

| Variant | Covered | Total | RC |
|---|---|---|---|
| A | 17 | 17 | 1.0000 |
| B | 16 | 17 | 0.9412 |
| C | 17 | 17 | 1.0000 |

## IC: internal consistency

| Variant | Contradiction | Source | Statements in conflict |
|---|---|---|---|
| A | X-015 | diff-analysis | NFR-001 "no new code ... touches a remote" vs FR-041 `git submodule update --init` cloning from the `.gitmodules` URL |
| A | X-019 | diff-analysis | §1.1 defines `<pkg>` as `src/<package>/`, while FR-060, FR-061 and FR-064 use `<pkg>` for the managed task package |
| A | N-A1 | found here | FR-052 and T-15 allow the string `--commit-tasks` only in `implement.md`, `sc-implement-protocol` and `HOW-WE-WORK.md`. FR-091 writes `--commit-tasks` into `WORKER-CONTRACT.md`, which is a core primitive (§1.1 lists the installed `<home>/WORKER-CONTRACT.md`), so T-15 would fail on A's own required text |
| B | X-016 | diff-analysis | FR-023 runs the Wave 0 check "after step 6 (ledger)", yet says the run stops "before the ledger is created" |
| B | X-017 | diff-analysis | FR-019 and NFR-003 say the helper "writes nothing in the repository", while its allow-list has `read-tree`/`add`/`write-tree`, which write objects |
| B | X-018 | diff-analysis | FR-028 limits the header to 72 characters, but its regex `\S.{0,70}$` after the prefix allows more |
| B | N-B1 | found here | FR-020 defines `preflight` with an unbracketed (required) `--message <file> -- <paths...>`, while FR-023 runs `preflight` at Wave 0 "once with no paths", before any task message exists |
| C | none | n/a | No internal row in diff-analysis. My scan found no explicit opposing pair |

Candidates I considered and did not count, because the statements are not explicitly opposed or diff-analysis already treats them as cross-variant differences:
- C FR-026 (update to the recorded pointer vs stopping when the checkout differs; diff-analysis X-013);
- C NFR-006 vs FR-022 (whether "ledger resume" unchanged covers opted-in runs);
- A NFR-002 vs FR-061 step 1 (a Write-tool message file is not a git write);
- B FR-016 vs FR-035 (whether "`.dev/tasks` appended" applies to the commit pathspec).

| Variant | FR | NFR | AC | Scorable claims | Contradictions | IC |
|---|---|---|---|---|---|---|
| A | 60 (FR-001..017, 020..022, 030..034, 040..043, 050..072, 080..082, 090..094) | 11 | 15 | 86 | 3 | 1 - 3/86 = 0.9651 |
| B | 47 (FR-001..044 plus FR-032a, FR-037a, FR-037b) | 11 | 15 | 73 | 4 | 1 - 4/73 = 0.9452 |
| C | 36 (FR-001..036) | 8 | 8 | 52 | 0 | 1 - 0/52 = 1.0000 |

## SR: specificity ratio

| Variant | Items | Concrete (code span / digit only / number word only) | Vague | Vague items (all "no concrete indicator"; vague-term hits = 0) | SR |
|---|---|---|---|---|---|
| A | 86 | 82 (79 / NFR-008, NFR-011 / FR-021) | 4 | FR-082, NFR-001, NFR-002, AC-15 | 82/86 = 0.9535 |
| B | 73 | 72 (72 / none / none) | 1 | NFR-004 | 72/73 = 0.9863 |
| C | 52 | 34 (31 / none / NFR-002, AC-02, AC-04) | 18 | FR-010, FR-011, FR-012, FR-017, FR-018, FR-023, FR-026, FR-035, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, AC-01, AC-05, AC-06, AC-08 | 34/52 = 0.6538 |

## DC: dependency completeness

| Variant | FR/NFR/AC/T refs (resolved/total) | Internal section refs (resolved/total) | Decision refs (resolved/total) | External section refs excluded | Total resolved/total | DC |
|---|---|---|---|---|---|---|
| A | 93/93 | 8/8 (Section 6, §9, §2.2, §4, §4.3 ×2, §4.6, §5) | 2/2 (D6, D5) | 4 (developer guide §3.1 ×2, §5.6 ×2) | 103/103 | 1.0000 |
| B | 86/86 | 10/10 (section 11 ×5, 9, 2, 10, 3, 5) | 3/3 (Q5 ×2, Q6) | 15 (`research-deep.md` §1..§5) | 99/99 | 1.0000 |
| C | 20/20 | 0/0 (no numbered headings, no section refs) | 0/0 | 0 | 20/20 | 1.0000 |

No reference points at an undefined ID. Sensitivity: B's risk and root-cause references (R1..R13, RC-1..RC-7), which the brief excludes, also all point at defined rows, so including them would not change DC.

## SC: section coverage

| Variant | H2 sections | Max H2 | SC |
|---|---|---|---|
| A | 13 (`## 1.` .. `## 13.`) | 14 | 13/14 = 0.9286 |
| B | 14 (`## Path notation` plus `## 1.` .. `## 13.`) | 14 | 14/14 = 1.0000 |
| C | 12 (unnumbered) | 14 | 12/14 = 0.8571 |

## Summary

| Variant | RC | IC | SR | DC | SC | quant_score |
|---|---|---|---|---|---|---|
| A | 1.0000 | 0.9651 | 0.9535 | 1.0000 | 0.9286 | 0.9736 |
| B | 0.9412 | 0.9452 | 0.9863 | 1.0000 | 1.0000 | 0.9666 |
| C | 1.0000 | 1.0000 | 0.6538 | 1.0000 | 0.8571 | 0.9266 |

quant_ranking: A, B, C

## Sensitivity (for the orchestrator; the scores above are the scored result)

| Case | A | B | C | Ranking |
|---|---|---|---|---|
| Scored result | 0.9736 | 0.9666 | 0.9266 | A, B, C |
| S1: B's R1 counted as covered (topic match only, ignoring the X-002 seed conflict) | 0.9736 | 0.9842 | 0.9266 | **B, A, C** |
| S2: IC uses only diff-analysis internal rows (drops N-A1, N-B1) | 0.9765 | 0.9700 | 0.9266 | A, B, C |
| S3: IC denominator also drops SR-vague items | 0.9732 | 0.9664 | 0.9266 | A, B, C |
| S4: number words not counted as concrete | 0.9718 | 0.9666 | 0.9180 | A, B, C |

Whether A or B ranks first depends only on RC rule (b), that is, whether Variant B keeping `merge` against the seed brief's "`/sc:git` never ... merges" constraint counts against coverage. A leads B by 0.0070 under the scored rules. DC does not separate the variants (all 1.0000), and C's lower score comes almost entirely from SR (18 of its 52 items carry no code span, number or quantity).

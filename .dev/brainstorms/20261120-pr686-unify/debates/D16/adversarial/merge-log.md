# Merge Log: D16 unified prevention package

<!-- Provenance: produced by /sc:adversarial; Base: Variant 1 (OURS); Merge date: 2026-11-20 -->

## Metadata

<!-- Source: Base (original) - merge-log structure required by the merge-executor brief -->

| Field | Value |
|---|---|
| Merge date | 2026-11-20 |
| Executor | merge-executor, step 5 of the adversarial pipeline for debate D16 |
| Base variant | Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/variant-1-original.md` |
| Incorporated variant | Variant 2 (CLAY), `.../variant-2-original.md`, with Round 1, Round 2 and Round 2.5 results |
| Plan executed | `.../refactor-plan.md` (10 planned changes, 6 adjudicated disputes, 4 invariant conditions, 9 rejected items, risk summary) |
| Merged artifact | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/merged-output.md`, 421 lines, 15 H2 and 6 H3 sections |
| Files read in full | `variant-1-original.md`, `variant-2-original.md`, `refactor-plan.md`, `round1-advocate-1-ours.md`, `round1-advocate-2-clay.md`, `round2-advocate-1-ours.md`, `round2-advocate-2-clay.md`, `invariant-probe.md`, `base-selection.md`, `diff-analysis.md` |
| Files not read | `debate-transcript.md` (not in the input list); FULL-REPORT.md (cited by the inputs, not opened: its section references are copied from the inputs) |
| Files written | `merged-output.md` and `merge-log.md` only. Nothing was written to GitHub or Orca; SuperClaude-Org was not touched |
| Method | Both files created as header stubs first, then filled section by section with a fill marker, which was removed at the end (0 left) |

## Changes Applied

<!-- Source: Base (original) - one row per planned change, in plan order -->

Status key: APPLIED means the change is in `merged-output.md` as the plan describes it. Section names below are headings of `merged-output.md`.

| # | Change | Status | Where applied | Source | Before and after |
|---|---|---|---|---|---|
| 1 | Reframe the Claim: a second person with a mechanical block was missing; text alone does not bind (PR 681 body, PR 683 self-merge, INV-019); package is words, one ruleset, a decisions file, a direct hold | APPLIED | `## Claim`; echoed in `## What it gets right` bullet 1 and `## Lightest version that would have prevented the incident` | OURS Round 1 and INV-026 | Before: "a written agreement alone repeats 2026-10-22; nine items close eight gaps". After: four-part package, only the ruleset is a block, and "would have prevented 681 and 682" is "probably, UNVERIFIED" until the throwaway test passes. The "closes the eight gaps" sentence was dropped because the package is narrower than the nine items |
| 2 | Layer 1 carrier: root `CLAUDE.md` section, pointer in `HOW-WE-WORK.md`, one line in `CONTRIBUTING.md`; PR template two reminder lines, not a control (14 of 100, 0 of the last 79) | APPLIED | `## Mechanism`, `### Layer 1: words in the files sessions read` (file table) | Variant 2 (CLAY) Round 1 A-002 and Round 2 OURS R-5 | Before: roles paragraph in CONTRIBUTING.md plus PR template lines. After: carrier is root `CLAUDE.md`; template reach figure stated; HOW-WE-WORK.md copy cost (about 15 minutes) stated |
| 3 | Rule text content: roles by login, written answer, 3 working days as ask-again timer, deputy or "nobody" plus channel, reversal rule, narrow revert definition, publish within a day, optional helper | APPLIED | `### Layer 1`, "Rule text content" items 1 to 8 | Variant 2 (CLAY) U-007 and Round 2 of both | Before: no deadline rule, no revert definition. After: eight numbered rules; revert defined as GitHub Revert button or `git revert`, one named PR in full, merged within 7 days, reported to the author the same day. `IB-JonathanB` is not named |
| 4 | CODEOWNERS list: core `docs/designs/`, `WORKER-CONTRACT.md`, `/.github/CODEOWNERS`; temporary `issue_watch/` and `sc-issue-protocol/`; optional guard-file lines after the 14 day review | APPLIED | `### Layer 3: enforcement by GitHub` (CODEOWNERS table); ranks 4, 9, 12 | OURS Round 1 and 2, CLAY Round 2, INV-006, orchestrator check of PR 690 | Before: five-path list (27 of 60 merged PRs). After: three core lines, two temporary lines with their removal condition, one optional group |
| 5 | Sole code owner `@ironbelly` | APPLIED | `### Layer 3` (reason paragraph); `## Decisions the owner gives in chat` decision 1; `## Risk` | INV-007 and INV-013 | Before: owners `ironbelly`, `clayphi`, `IB-JonathanB` (Round 2 OURS) or two owners (Round 2 CLAY). After: one owner. `@clayphi` appears nowhere as a code owner (grep: 0 hits) |
| 6 | Ruleset on `master` and `integration`: PR required, 0 approvals, code-owner review, dismiss stale approvals, no force push, no deletion, admin bypass for pull requests only | APPLIED | `### Layer 3` (ruleset list and bypass paragraph); rank 5; `## What only the repository admin can enable` | OURS Round 1 and 2, CLAY Round 2, INV-001, INV-021 | Before: ruleset on `master`, no bypass. After: seven settings, `integration` included (23 of 100 PRs, all self-merged), bypass as a hybrid with the owner's chat confirmation as decision 3 |
| 7 | Test protocol and fallbacks; 14 day review that counts silent passes and has a minimum sample | APPLIED | `## Test protocol and fallbacks` (INV-027 copied) and `### 14 day review`; `## Open invariants` | INV-007, INV-027, INV-016 | Before: no test or fallback. After: the INV-027 condition copied verbatim (checked by diff after the final edit: identical), three fallbacks, a review that counts waits and silent passes. The debate files give no number for the minimum sample, so none was invented (left open and marked UNVERIFIED) |
| 8 | Decisions: one file `docs/decisions.md`, seeded once, entries added by the session that hears each ruling with the owner's chat sentence quoted, owner approves wording in chat first | APPLIED | `### Layer 2: visibility` items 1 and 2; rank 8; decision 6 | OURS Round 2 and CLAY Round 2 | Before: `docs/decisions/` folder with back-fill of 8 to 10 rulings. After: one file, about 10 ruling groups, recording rule that never asks the owner to write a file; seed sources marked as unread (INV-004) |
| 9 | Direct hold on the open 655 series: owner says in chat that PRs 686 and 690 wait; `clayphi` sets both to Draft; Draft is a speed bump | APPLIED | `### Layer 2` item 4; rank 2; decision 5 | CLAY Round 2, INV-002, INV-009 | Before: no hold. After: hold, with the facts that neither PR is Draft today and that conversion by anyone but the author is UNVERIFIED |
| 10 | Order and cost table, admin-only list, "lightest version" and "version still refused" paragraphs | APPLIED | `## Ranked, costed, ordered package` (table and `### Order and dependencies`); `## What only the repository admin can enable`; `## Lightest version that would have prevented the incident`; `## Version still refused`; also `## Dropped items and why`, `## Decisions the owner gives in chat`, `## Corrected figures`, `## Open invariants`, `## Cost` | Both Round 2 final tables | Before: nine items with no order or admin split. After: 12 ranked rows plus a drop row, ordered with dependencies, admin-only rows marked REPOSITORY ADMIN ONLY |

### Disputes from the adjudication table

<!-- Source: Base (original) - mapping of the six residual disputes to where the decision sits in the merged text -->

The adjudication table of the plan is reflected in the text rather than reproduced as a table.

| Dispute | Decision in the plan | Where it sits in `merged-output.md` |
|---|---|---|
| Admin bypass | Hybrid: admin role, pull requests only; owner confirms in chat | `### Layer 3`; decision 3; `## Version still refused` |
| Required paste of the deletion check against an optional helper | Written sentence, optional helper, narrow revert exemption, CI check only on a tripwire | `### Layer 1` rule 8; rank 10; `## Dropped items and why` |
| `IB-JonathanB` on CODEOWNERS | Not named until they agree in an issue comment | `### Layer 1` rule 1; decision 2; `## Dropped items and why` |
| Two owners against sole owner | Sole owner `@ironbelly` | `### Layer 3`; decision 1 |
| Direct hold on 686 and 690 | Adopted as an owner decision in chat | `### Layer 2` item 4; rank 2; decision 5 |
| `integration` in the ruleset | Included | `### Layer 3`; decision 4; `## Open invariants` INV-001 |

### Additions beyond the ten changes

<!-- Source: Base (original) - items that are not one of the ten numbered changes; listed so the orchestrator can see them -->

These are in `merged-output.md` but are not a numbered change in the plan. Each is sourced from the input files and none contradicts the plan.

1. `## Corrected figures`, the cost arithmetic in `## Cost` and the Risk-summary table: carried from the plan Overview (recount rule), the "MEDIUM findings" paragraph and the Risk Summary.
2. `### Medium findings also carried`: the plan's MEDIUM list (INV-021, 022, 002, 010, 016, 027, 012 to 014), plus INV-006, INV-004 and INV-017. INV-006 and INV-004 appear in the plan under Changes 4 and 8; INV-017 (a sole code owner has no second approver) appears in `invariant-probe.md` only and is used in `## Risk`.
3. Facts 11 to 18 in `## Cited facts` and the `## Risk` bullets use findings INV-001, 002, 003, 005, 008, 009, 018, 019, 020, 025 from `invariant-probe.md`.
4. The helper commands in `### Layer 1` rule 8 come from `round2-advocate-1-ours.md` R-2, with the 100-file cap note from INV-020.
5. The PR template line texts: the first from `round2-advocate-1-ours.md` R-5, the second from the CLAY Round 2 sentence. The plan says only "two reminder lines".
6. Two totals in `## Cost` and one in `## Lightest version` are my arithmetic over sourced estimates (145 to 235 minutes; 120 to 150 minutes). They are labelled as such.

## Post-Merge Validation

<!-- Source: Base (original) - checks required by the merge-executor brief; run with read-only grep and awk on merged-output.md after the last edit -->

### Structural integrity

| Check | Method | Result |
|---|---|---|
| Heading hierarchy has no gaps | awk over headings outside code blocks, flagging any jump of more than one level | PASS. One H1, 15 H2, 6 H3 (3 under Mechanism, 1 under Ranked package, 1 under Test protocol, 1 under Open invariants, 0 orphans); no H3 sits under an H1 and no H4 exists. Three `#` lines inside the bash code block in Layer 1 are shell comments, not headings, and were excluded |
| Base skeleton kept | Compare against `variant-1-original.md` | PASS. Claim, Mechanism, Cited facts, Cost, Risk, What it gets right are present as H2 in that order |
| Required added sections present | Compare against the task list | PASS. `## Ranked, costed, ordered package`, `## What only the repository admin can enable`, `## Lightest version that would have prevented the incident`, `## Version still refused`, `## Test protocol and fallbacks`, `## Dropped items and why`, `## Decisions the owner gives in chat`, `## Corrected figures`, `## Open invariants` |
| Fill markers removed | grep `FILL-MARKER` | PASS. 0 in `merged-output.md` (the merge-log marker is removed after this section is written) |
| Ranked table shape | awk count of cell separators per row | PASS. All 15 rows have 6 separators (5 columns, header and drop row included) |
| Provenance | Header comment present once; every H2 and H3 has a `<!-- Source: ... -->` comment within 3 lines after it | PASS. 1 header comment, 27 source comments, 0 sections without one |

### Cross-references

| Check | Result |
|---|---|
| Backticked `## ...` references (8 distinct names) resolve to existing H2 headings | PASS: Corrected figures, Decisions the owner gives in chat, Dropped items and why, Open invariants, Ranked costed ordered package, Risk, Test protocol and fallbacks, Version still refused |
| "rank N" references (N from 1 to 12) point to rows of the ranked table | PASS. The ranks cited in `## Cost`, `## Risk`, `## Lightest version`, `## Test protocol` and `### Order and dependencies` match the table: 2 hold, 3 rule text, 4 CODEOWNERS, 5 ruleset, 6 test, 7 announcement, 8 decisions file, 9 review, 10 CI check, 11 CODEOWNERS on rule text, 12 guard files |
| "decision N" references (1 to 7) point to items of `## Decisions the owner gives in chat` | PASS. Decision 1 roles and sole owner, 2 deputy and channel, 3 bypass, 4 `integration`, 5 hold, 6 seed, 7 guard files. The ruling named "Decision 6" of FULL-REPORT was reworded to "the ruling named Decision 6" so it is not confused with owner decision 6 |
| INV, A-, C-, X-, U- identifiers exist in the evidence files | PASS. Every INV id used exists in `invariant-probe.md`; every A-, C-, X-, U- id exists in `diff-analysis.md` |
| FULL-REPORT section references | NOT RESOLVED BY ME. FULL-REPORT.md was not in the input list; the references (section 1, 4, 5, 10, 11) are copied from the input files |
| Verbatim copy of INV-027 | PASS. The blockquote in `## Test protocol and fallbacks` was diffed against the INV-027 cell of `refactor-plan.md` after the last edit: identical (a stray full stop I had added was removed) |

### Contradiction re-scan against refactor-plan.md

| Plan statement | Merged text | Result |
|---|---|---|
| Code owner is `@ironbelly` only | Layer 3 table lists only `@ironbelly`; grep for `@clayphi` returns 0 | No contradiction |
| Ruleset: PR required, 0 approvals, code-owner review, dismiss stale approvals, no force push, no deletion, admin bypass for pull requests only, on `master` and `integration` | Layer 3 list items 1 to 7 and the `integration` paragraph | No contradiction |
| PR template is a reminder, not a control (14 of 100, 0 of the last 79) | Layer 1 table and `## Corrected figures` | No contradiction |
| Paths: three core, two temporary, optional guard-file lines after the 14 day review | CODEOWNERS table, ranks 4, 9, 12, decision 7 | No contradiction |
| One decisions file, owner approves wording in chat, never a file written by the owner | Layer 2 items 1 and 2; decision 6 | No contradiction |
| Corrected figures: 35 (floor), 23 on master, 17 and 6, template 0 of 79, 89 of 100, `CONTRIBUTING.md:77-79` struck, `IB-JonathanB` | `## Corrected figures` | No contradiction. The earlier 31 appears only in the "advocate figure" column and in the 14 day review sentence that explicitly says "counted in Round 2, 21 of 35 on recount" |
| Hold on 686 and 690; Draft is a speed bump | Layer 2 item 4; rank 2 | No contradiction |
| Prevention claim is conditional on the test | `## Claim`, `## Lightest version`, `## What it gets right` bullet 1, `## Open invariants` | No contradiction. Every place that says the package would have stopped 681 and 682 carries "probably, UNVERIFIED" or points to the test |
| Rejected items stay rejected | `## Dropped items and why` has all 9 plan rows; none is re-adopted elsewhere. The CI deletion check appears only as a tripwire item (rank 10) | No contradiction |

One tension, not a contradiction: the INV-027 condition in the plan lists the test author as `clayphi`, and the probe described `clayphi` as "a listed owner". Under the plan's sole-owner list `clayphi` is not a code owner. The text of the condition is copied unchanged, and `## Test protocol and fallbacks` states the sole-owner reading and says the owner-authored third PR shows how the author-owner case of INV-007 behaves for the owner's own PRs.

### Style and fact checks

| Check | Result |
|---|---|
| No em dashes, en dashes or emoji in either file | PASS. 0 hits in `merged-output.md` and in `merge-log.md` |
| No TODO, TBD, FIXME placeholders | PASS. 0 hits |
| "They" for Clay, `ironbelly` as the owner | PASS |
| UNVERIFIED items kept | PASS. 22 occurrences in `merged-output.md`, including org-level rulesets (`admin:org`), Evaluate mode on the Free plan, "required reviewers" rule availability, Draft conversion by a maintainer, the stale-approval default, the minimum review sample, the 11-of-100 firing rate, whether sessions obey a `CLAUDE.md` rule |
| No invented figures | PASS with two flags. Every number traces to an input file. The sums in `## Cost` (145 to 235 minutes, about 2.4 to 3.9 hours) and `## Lightest version` (120 to 150 minutes) are my arithmetic over sourced estimates and are labelled as such |

## Summary

<!-- Source: Base (original) - closing summary required by the merge-executor brief -->

- Changes planned: 10. Applied: 10. Skipped: 0. Escalated: 0. Plan rejections kept: 9 of 9 in `## Dropped items and why`.
- Post-merge validation: heading hierarchy, base skeleton, provenance coverage, cross-references and the contradiction re-scan against `refactor-plan.md` all pass. One cross-reference class could not be resolved by me: the FULL-REPORT.md section numbers, which were copied from the inputs because that file was not in the input list.
- Items for the orchestrator to see (none changes the plan):
  1. The 14 day review needs a minimum sample, and the debate files give no figure. The merged text leaves it open and marks it UNVERIFIED instead of inventing one. The owner may want to set it in chat when the ruleset is switched on.
  2. The INV-027 condition names `clayphi` as the test author, while the plan's sole-owner list means `clayphi` is not a code owner. The condition was copied verbatim and the tension is noted in `## Test protocol and fallbacks`.
  3. INV-017 (a sole code owner has no second eligible approver) is used in `## Risk` although the plan does not list it. It comes from `invariant-probe.md`.
  4. The two time totals in `## Cost` and `## Lightest version that would have prevented the incident` are my arithmetic over the advocates' estimates; the Round 2 papers gave different totals (2.5 to 4 hours and 3 to 4.5 hours), both quoted next to mine.
- Remaining UNVERIFIED across the package (all from the inputs): organisation-level rulesets (token lacks `admin:org`); whether the ruleset blocks an author who is himself a code owner at 0 approvals (INV-007, to be settled by the throwaway test); Evaluate mode and the "required reviewers" rule on the Free plan; who besides the author can convert a PR to Draft; the stale-approval default; whether sessions obey a root `CLAUDE.md` rule; the owner's away rate and channel; the contents of `owner-answers.md` and `RULINGS.md`.
- Nothing was written to GitHub or Orca, and no file other than the two named was written.


# Diff Analysis: stage 4 revision route comparison

## Metadata
- Generated: 2026-11-17
- Variants compared: 2 (variant 1 = Route A, regenerate with /sc:workflow; variant 2 = Route B, copy and surgical edits)
- Total differences found: 13
- Categories: structural (2), content (6), contradictions (2), unique (4), shared assumptions (3 promoted)
- Focus areas: risks, rewards, roi

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Severity |
|---|---|---|---|---|
| S-001 | Headings | Question, The route, Rewards, Risks, ROI claim | Same five headings, same order | Low |
| S-002 | Bullet counts | 5 rewards, 3 risks, 3 route steps | 4 rewards, 4 risks, 3 route steps | Low |

## Content Differences

| # | Topic | Variant 1 (A) approach | Variant 2 (B) approach | Severity |
|---|---|---|---|---|
| C-001 | Package validity (return contract) | Generator writes `return-contract.yaml` (1.1); current package has none (A:11) | Hand-write a matching contract, keep slug equal to folder and file name (B:8, B:17) | Medium |
| C-002 | Pre-execution review | Built-in advisory `/sc:reflect --mode pre` runs on the result (A:7) | Not built in; run `/sc:reflect --mode pre` separately and write its result into the contract by hand (B:8, B:18) | Medium |
| C-003 | Keeping earlier work | Generator rewrites all four tasks; cuts-debate detail can be lost unless the request carries it (A:19) | Keeps the 4-task shape, decided keeps and grep acceptance checks (B:12) | High |
| C-004 | Source and plan agreement | `source.md` is a byte copy of the edited request, so the review compares plan to its source (A:14) | `source.md` must be edited too, or source and plan disagree (B:19) | Medium |
| C-005 | Cost and diff clarity | Full generation plus Tier 2 review, tens of minutes, read in full (A:20) | Three edits, small diff the owner can read line by line (B:13, B:14) | Medium |
| C-006 | Stale citations | Re-grounded against the post-stage-3 tree by construction (A:16) | Fixes only what is looked for; stage 3 showed a stale id slipping through (B:20) | Medium |

## Contradictions

| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|---|---|---|---|
| X-001 | Does staleness survive? | "re-grounded ... fixes the stale line numbers by construction" (A:16) | "Stale text survives: edits fix only what we think to look for" (B:20) | Medium |
| X-002 | How many tasks change | Premise: the generator rewrites all four tasks (A:19) | Premise: three edits are enough, "if the three edits are the only ones needed" (B:13, B:23) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 (A) | The ledger rule: one managed package per stage, generated with /sc:workflow (README.md:3) | High |
| U-002 | 1 (A) | Re-grounding with codegraph and Read against the post-stage-3 tree | Medium |
| U-003 | 2 (B) | Checklist of managed-detection needs: slug equals folder and file name, `contract_version: "1.1"` with same slug, realpath under `.dev/tasks/to-do/<slug>/` (B:17) | High |
| U-004 | 2 (B) | Precedent: revisions 2 to 4 were edited in place, so in-place editing is established practice for this program (B:15) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Stage 4 will proceed. If the owner holds or rolls back, either route's work is spent on a plan nobody runs. | Both papers cost the route as if stage 4 runs | High | UNSTATED, promoted (guard) |
| A-002 | Task 1's entry gate can be rewritten without a decision from the owner on waive, hold or rollback. The gate text depends on that decision. | Both list "rewrite the gate" as an ordinary edit | High | UNSTATED, promoted (guard) |
| A-003 | The advisory reflect review is a meaningful check for a plan this narrow (4 tasks) and is run and read by a person. | Both rely on it as the quality gate (A:7, B:8) | Medium | UNSTATED, promoted |

STATED, not promoted: both papers assume the needed changes are the gate text, the reflect-reviewer carrier and stale citations (question line, A:3, B:3).

## Summary
- Total structural differences: 2
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003, X-002, U-001, U-003, A-001, A-002

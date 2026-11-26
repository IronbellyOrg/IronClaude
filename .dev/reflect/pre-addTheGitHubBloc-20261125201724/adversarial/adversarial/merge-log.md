# Merge log

## Metadata
- Base: Variant 1 (variant-1-original.md, reviewer 1 card, analyzer, opus class)
- Executor: merge-executor
- Plan: refactor-plan.md (11 planned changes, 4 rejected by the plan)
- Changes applied: #1 to #11 (11 of 11)
- Status: complete, all validation checks passed
- Output: /home/coder/workspaces/worktrees/IronClaude/issue-848/.dev/reflect/pre-addTheGitHubBloc-20261125201724/adversarial/merged-reviewer-card.md
- Timestamp: 2026-11-25T20:50:00Z

## Changes Applied

### Change #1 (A1, append): applied
- Before: A1 evidence list lacked the 1953-1956 quote; Fix paragraph ended after "guide wording".
- After: evidence bullet for `test_worker_contract.py:1953-1956` added; Fix paragraph extended with the keyed-by-whole-line, `\\(` escape and lint-criterion sentences. Grade unchanged (Blocking).
- Provenance: `Base (original, modified)`, Q1 evidence and INV-004 details.

### Change #2 (A2, replace): applied
- Before: Claim with three sub-bullets (one said gh source knowledge, "not checked in this audit"); exit-status-first fix.
- After: single Claim paragraph with the verified gh 2.103.0 probe (404, issue 612, issue 590); Consequence replaced; Fix replaced with the three-step precedence (blocker pattern first, then non-zero exit, then none) citing settle.sh:371-375. Heading line and grade kept; evidence list kept.
- Provenance: `Base (original, modified)`, per Change #2.

### Change #3 (A3, replace): applied
- Before: later STOP "prints only the STOP code, its message and the return contract"; examples included E-ASSIGN-FAILED; "never told".
- After: "not guaranteed to be told"; examples E-TIER-UNAVAILABLE, E-WORKER-NO-OUTPUT, E-POST-FAILED; new Fix sentence. Grade Medium and evidence kept.
- Provenance: `Base (original, modified)`, per Change #3.

### Change #4 (A4, regrade): applied
- Before: "A4. Medium"; consequence about an avoidable fix pass.
- After: "A4. Note"; consequence "a capitalised rewrite fails the test; Task 6's test run catches it."
- Provenance: `Base (original, modified)`, per Change #4.

### Change #5 (A5, append): applied
- Before: A5 claim ended at "is safe."
- After: appended the `grep -c` sentence on the single `## Final output` occurrence. A6 unchanged as the plan says.
- Provenance: `Base (original, modified)`, per Change #5; A6 tagged `Base (original)`.

### Change #6 (A7, replace claim): applied
- Before: "the heading still says the orchestrator only reads `scout.md`, while the new item 5 makes a live GitHub call."
- After: plan's corrected claim sentence (SKILL.md:86 reference). Evidence line unchanged.
- Provenance: `Base (original, modified)`, per Change #6.

### Change #7 (A8, append): applied
- Before: A8 claim ended at "until sync-dev runs."
- After: appended the "Graded Note after the debate" ruling text.
- Provenance: `Base (original, modified)`, per Change #7.

### Change #8 (insert A10): applied
- Before: no A10.
- After: A10 Medium (ordering check against the assignee checks) inserted after A9 with the plan's four evidence entries.
- Provenance: `Variant 2 (reviewer 2 card), Q2 - merged per Change #8`.

### Change #9 (insert A11 to A14): applied
- Before: no A11 to A14.
- After: A11 (Variant 2 Q3), A12, A13, A14 inserted after A10, all Note, in the plan's wording. One format normalization: the plan's heading "A14. Note (out of scope): the issue watcher ..." does not fit the required heading form, so it is written "A14. Note: out of scope; the issue watcher ...". Straight quotes replace the plan's escaped quotes in the A13 `grep -n "gh api" claim.md` text.
- Provenance: A11 `Variant 2 (reviewer 2 card), Q3`; A12 to A14 `Invariant probe` (the plan does not map INV-008, INV-010 and INV-013 to individual findings, so the tags do not either).

### Change #10 (closing list, append): applied
- Before: five bullets in "What I checked and found correct".
- After: five bullets added (Wave 2 renumbering, `gh api` scan scope, list shapes, lookup rule, fix-set sufficiency) with the plan's citations.
- Provenance: `Base (original, modified)`, per Change #10.

### Change #11 (grade summary): applied
- Before: `## Findings` heading followed directly by A1.
- After: grade summary line inserted under the heading.
- Provenance: `Plan (Change #11)`.

### Header
- `persona: merged (analyzer + qa)`, `model_class: merged (opus + haiku)`, one-line `reviewer_model_self_report: claude-gw-tier1a[1m] (analyzer); GPT-5.2 (qa)`; `model_alias_resolves_to` kept; three provenance HTML comments added above.

## Post-Merge Validation
| Check | Result |
|---|---|
| Finding ids A1 to A14 present once each and in order | pass |
| Heading form `A<n>. <Grade>` with grade word exactly Blocking, Medium or Note | pass |
| Grade counts Blocking 2 (A1, A2), Medium 2 (A3, A10), Note 10 (A4 to A9, A11 to A14) | pass |
| No leftover "not checked in this audit" text | pass (0 matches) |
| No finding says E-ASSIGN-FAILED loses the line | pass (0 matches in the card) |
| ASCII only, no em or en dashes | pass (0 non-ASCII characters) |
| Base path:line citations and verbatim quotes unchanged; no new citation beyond the plan's | pass (by construction, base text copied; only plan-given citations added) |
| Provenance tag above every finding | pass |

## Summary
- Planned: 11
- Applied: 11
- Failed: 0
- Skipped: 0

# Merge Log (D01)

## Metadata

- Merge-executor run for /sc:adversarial, topic D01 (trigger and approval gate).
- Base variant: Variant A (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/variant-1-original.md`.
- Refactoring plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/refactor-plan.md` (6 planned changes, 4 rejected, overall risk Medium).
- Other inputs read: `variant-2-original.md`, `invariant-probe.md`, `debate-transcript.md`, `base-selection.md` (same folder).
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/merged-output.md`.
- Style: plain, no em dashes (checked, 0 found, no en dashes either).
- Scope: only the two output files were written; no git, GitHub or Orca action.
- Citation policy: every base file:line citation is kept unchanged except in fact 6 (Change #3, restructured as planned). New citations come only from Variant 2, the probe and the debate transcript (verified by the orchestrator in Round 2.5 for the MR-1 and MR-2 lines). The merge-executor did not re-read the cited source files.

## Changes Applied

### Change #1: Add `plan_check` as a skip reason before approval (insert; Low)

- Target: "What it gets right (and what we concede)", bullet 1, and "Recommended rule".
- Before: bullet 1 said `plan_check` "is worth taking as a skip reason before the approval is even looked at"; the rule listed `plan_check(body).ok` as one of five conditions with no ordering.
- After: bullet 1 says the skip reason is evaluated before the approval counts, so an issue with no plan never reaches the approval check, and adds Variant 2's evidence that the built watcher had no plan check and the label could be put on an empty issue (`H-design681-map.md:53`). The rule section gains a paragraph stating that `plan_check(body).ok` is looked at before the approval counts.
- Source: Variant 2 mechanism step 4 and cited fact 7. Status: applied.

### Change #2: Add `hold:backlog` as a read-only veto (insert; Low)

- Target: "What it gets right", bullet 2, and "Recommended rule".
- Before: bullet 2 called `hold:backlog` a cheap veto read from labels already in `DiscoveredIssue.labels`; the rule listed "`hold:backlog` is absent".
- After: bullet 2 adds the design's own wording "a person may stop an issue with `hold:backlog`" (`DESIGN` R1, D:73) and states the watcher stays read-only for this veto. The same rule-section paragraph as Change #1 covers it as a read-only skip reason.
- Source: Variant 2 mechanism step 1. Status: applied. Note: `table_row` winning over everything (`hold.py:153`) appears only in an advocate's Round 1 text and was not carried over.

### Change #3: Narrow the C-006 claim (restructure; Medium)

- Target: "Cited facts", fact 6.
- Before: "Edit-after-approval protection has no equal in PR 686." ... "`DESIGN` DQ3 and wave 1 re-read the issue live but nothing compares it with what a person looked at."
- After: title becomes "The edit-after-approval binding has no counterpart in PR 686, but PR 686 is not silent about edits." Adds that PR 686 accepts later edits on purpose (wave 1 re-reads live and re-runs `plan_check` and `hold:backlog`, `DESIGN` line 488, AD-A3 / ruling 23). The symbol-diff list is kept verbatim. Adds that `plan_check` passes a rewritten body with three filled headings (`hold.py:131`), that the approval's value is tying a person's yes to the content they read and matters most when the worker can push and merge (fact 4), and the conceded cost that any edit voids the approval so a typo fix needs re-approval.
- Source: base fact 6 plus debate Round 2 (C-006 A lowered from 85 to 65). Status: applied. Revert option if the owner prefers the stronger wording: restore the original fact 6 (noted in the plan's risk summary).

### Change #4: Requirement MR-1 (append; Medium)

- Target: "Recommended rule", new H3 "Requirement MR-1".
- Before: no start-time re-check requirement.
- After: the check at the moment of start must repeat approval, `unchanged_since` and the Status allow-list, not only `plan_check` and `hold:backlog`. Evidence: `DESIGN` lines 317, 488, 543; `PRA/.../cycle.py:1279-1305` and `:992-1005`; master `_revalidate` (`SNAP/.../cycle.py:979`, called at `:1058`).
- Source: probe INV-001 (HIGH, verified by the orchestrator). Status: applied.

### Change #5: Requirement MR-2 (append; Medium)

- Target: "Recommended rule", new H3 "Requirement MR-2".
- Before: no double-start requirement.
- After: keep the claim-marker guard `marker_in_window`. Evidence: `/sc:issue --claim` posts the marker (`refs/claim.md:30,92`); master `cycle.py:858,946-947`; PR 686 keeps only the constant (`PRA/.../predicates.py:18`) and relies on DQ3 layers (poll store, `O_EXCL` state file, lease comment; layer 4 idempotent claim by the current login). Cross-refers to fact 1.
- Source: probe INV-002 (HIGH, verified by the orchestrator). Status: applied.

### Change #6: Reopening condition and owner decisions (append; Low)

- Target: new H3 "Conditions to revisit" inside the closing section "Merged recommendation" (placed there because the closing section must contain it).
- Before: no reopening condition.
- After: four conditions for reconsidering assignment alone (launch guard effective with tests, topic D05; workers cannot push or merge, topic D06; claim-record or worktree skip, same guard as MR-2; owner records the R19 reversal in chat), plus open owner decisions (reverse R19; whether the trigger label stays, REQ R35 line 61 says it stays).
- Source: Variant 2 Round 2 (b) and Variant 1 Round 2 (d), as recorded in `debate-transcript.md`. Status: applied.

### Closing section and provenance

- Added a provenance header comment and a per-section `<!-- Source: ... -->` tag on every section.
- Added "## Merged recommendation" as the last section: the five-condition hybrid rule (assignment alone never starts work; approval is field `Approved` per R35, label until then; Status allow-list; `hold:backlog` absent; `plan_check(body).ok`), requirement MR-1, requirement MR-2 and the "Conditions to revisit" H3.

## Post-Merge Validation

1. Heading hierarchy: PASS. Headings in order: H1 title; H2 The claim, The mechanism, Cited facts, What it costs, What it risks, What it gets right, Recommended rule (with H3 MR-1 and H3 MR-2), Merged recommendation (with H3 Conditions to revisit). No level is skipped, and the document ends with "## Merged recommendation".
2. Internal references: PASS. "fact 1", "fact 4", "fact 6", "MR-1", "MR-2", "Conditions to revisit" and the quoted heading "What it gets right (and what we concede)" all resolve. The two mentions of "fact 7" are inside provenance comments and are labelled as Variant 2's fact 7, not the base's fact 7.
3. Contradiction re-scan: PASS, no new contradiction found. Points checked: fact 6 (narrowed) against fact 4, mechanism step 3 and the rule; the rule against "What it costs" and "What it risks" (unchanged); the five-condition list against the Recommended rule paragraph (identical conditions). Two observations that are not new contradictions: mechanism step 1 says discovery needs the trigger label while the rule lists no trigger label as a start condition (this is in the base; the owner decision on the trigger label is recorded in "Conditions to revisit"); and the sentence "skipped without reading the approval or edit evidence" in "Recommended rule" is the merge-executor's wording of the "skip reason before approval" ordering required by Change #1.

## Summary

- Planned: 6
- Applied: 6
- Failed: 0
- Skipped: 0
- Not applied by design (listed in the plan as rejected): C-001 / S-002, C-004, C-008, C-010.
- Probe findings INV-003 to INV-009 are not in the plan and were not added.

# Q8: write the dated direction-selection record, or amend the #409 acceptance criterion

## The question, verbatim from the spec row

Source: `merged-requirements.md:535` (section 3, "Owner decisions").

> | Q8 | Write the AC-S record, or amend #409 AC 1 | Write the record (one paragraph) | PLAN INFERENCE: OB-08 posts without BC-18's status line and without AC 1 change; OB-09 cannot start | OB-02, OB-08 (BC-18), OB-09 | W1 |

Original wording (ADJ Part 7, `alignment-findings-adjudicated.md:778`): "Will you write the dated direction-selection record (AC-S) naming the staged direction, your reading of 'production integration' and the command name, or amend #409's first acceptance criterion?"

## Spec's recommended answer

"Write the record (one paragraph)" (ADJ:778; `merged-requirements.md:535`).

## Default if unanswered

PLAN INFERENCE (the spec's own derivation): OB-08 (the #409 issue-body correction pass) posts without BC-18's status line and without any change to acceptance criterion 1; OB-09 (release 3, Decision Desk) cannot start (`merged-requirements.md:535`).

## What it gates (work items, in words)

- OB-02: the owner writes the AC-S record (a dated paragraph naming the staged direction, the owner's reading of "production integration" and the command name) or amends #409's first acceptance criterion; agents cite it and do not write it; its path goes in the ledger (`merged-requirements.md:250`).
- OB-08, correction BC-18: the proposed status line for #409's acceptance criterion 1 waits for Q8 (`merged-requirements.md:256`; ADJ:535, :546, :573).
- OB-09: release 3 (Decision Desk) is blocked by OB-02 (`merged-requirements.md:257`).
- Wave W1 (the first batch of work after the intake questions).

## Facts the question depends on

| Fact | Source |
|---|---|
| AC-S is "the owner's own dated direction-selection record: the record that says which observer design direction was chosen. It does not exist yet" | ADJ glossary, line 86 |
| A staged direction was chosen (2026-11-08, 2026-11-11) and releases 1 and 2 shipped; the dated selection record is missing (74 percent) | ADJ X-018 (line 326); A-003, 96 percent (line 327) |
| #409's acceptance criterion 1 reads "A human selects the visual direction before production integration." The proposed BC-18 keeps it and appends: "(Status 2026-11-13: not met as recorded. `superclaude observe` is registered in the shipped CLI; PR #503 lists the missing selection record as a known gap.)" | ADJ Part 6.1 row 18 (line 535) |
| The gate's evidence rule on master: "a dated selection record written by the owner, never an agent. Names the date, option and decider, and where the owner's statement lives (agents may cite, never write it). Holds: default while no question rows exist, default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date, stack confirmation, command name, confirmed production-integration reading." | `origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md:22` (read 2026-11-14) |
| The owner's 2026-11-08 record already says "Staged direction chosen ('Stage it')" and "Whether this fully satisfies the DIRECTION-SELECTED gate is for the owner to say", and later records the stack confirmed as Python + Rich | sibling `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` lines 5, 9, 17 (untracked; not on master; see Q7) |
| `superclaude observe` is already registered in the shipped CLI | ADJ line 521; `merged-requirements.md:232` |
| The rule that agents cite and never write the record | ADJ:190; `release-gates.md:22` |

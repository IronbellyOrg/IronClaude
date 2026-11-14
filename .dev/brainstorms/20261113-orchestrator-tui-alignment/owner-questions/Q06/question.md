# Q6: scope and timing of switching on the observer's coordinator-questions read

## The question, verbatim from the spec row

Source: `merged-requirements.md:533` (section 3, "Owner decisions").

> | Q6 | Scope of the questions-read pass (`run_93bfa00cae2b` only, or any Run the terminal holds); flip before the seeded test? | Default (no debate verdict): do not flip before the seeded test; the scope sentence is the owner's | ADJ: guard stays off | OB-03, OB-04, OB-06 | W1 (test), W2 (flip) |

Original wording (ADJ Part 7, `alignment-findings-adjudicated.md:776`): "Does your 2026-11-12 pass for the coordinator-questions read cover only `run_93bfa00cae2b` or any Run your terminal holds? Do you want it flipped before the seeded consumption test has run?"

## Spec's recommended answer

"Default (no debate verdict): do not flip before the seeded test; after it, the scope sentence is yours; no answer means the guard stays off. The only debate recommendation to widen scope (V5 D5(ii)) was withdrawn" (ADJ Part 7, line 776). ADJ line 767 says Q6's default is the orchestrator's reading, not a debate verdict.

## Default if unanswered

ADJ: the guard stays off (`merged-requirements.md:533`). The coordinator-session rules repeat it: "no answer to Q6 means the guard stays off" (`merged-requirements.md:979`). OB-06 (the switch-on pull request) is not opened (`merged-requirements.md:254`, "Default if Q6 is unanswered").

## What it gates (work items, in words)

- OB-03, the seeded consumption test: from a terminal that holds no Run, create a throwaway Run, put known messages in its mailbox, run the observer's exact read twice, then one consuming read, and check every message was still there before the consuming read (`merged-requirements.md:251`).
- OB-04, one recorded live attempt of the questions panel inside the terminal that holds a disposable, representative coordinator Run (not the program's own) (`merged-requirements.md:252`).
- OB-06, the guard-flip pull request that sets `QUESTION_GATE_PASSED = True`; its prerequisite (a) is the owner's scope sentence quoted in the PR and enforced by code with a test that refuses a Run outside scope (`merged-requirements.md:254`).
- Wave: the test belongs to wave W1, the flip to wave W2 (spec row).

## Facts the question depends on

| Fact | Source |
|---|---|
| The questions read is switched off on master by one boolean, `QUESTION_GATE_PASSED = False`; while False, `--questions` makes no Orca call | `src/superclaude/cli/observe/commands.py:63-67`, `:170`, `:185` (read 2026-11-13) |
| `check_run_id` checks only the syntax of a Run id, so after a flip any `--run <id>` would be read | `src/superclaude/cli/observe/adapter.py:110-112`; ADJ INV-003 (line 458) |
| The owner's 2026-11-12 pass record names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run | ADJ INV-003 (line 458); `merged-requirements.md:235` |
| Whether `check --all --types question` removes (consumes) messages on a live coordinator Run is unproven both ways (61 percent); Orca's own help says `--all` "does not mark read" | ADJ X-016 (line 333); `merged-requirements.md:239` |
| A seeded test on a throwaway Run is necessary, not sufficient: a live Run has `--wait` listeners and an acknowledge cycle the throwaway Run lacks; a different Orca build may change `--all` | ADJ line 174; `merged-requirements.md:1156` |
| Gate test Q-1 (an unbound terminal cannot read another terminal's Run) failed on 2026-11-11, so only the terminal holding a Run can read its questions; 28 of 53 Runs have no holder | ADJ INV-024 (line 465); `merged-requirements.md:239` |
| The pass record and other owner records exist only in the sibling worktree `issue-409-mvp`, not on master | `merged-requirements.md:234-235` |
| The switch-on code is two unpushed commits in that sibling; a fresh branch from `origin/master` is needed | `merged-requirements.md:234` |
| The only debate proposal to widen scope to "any Run" (V5 D5(ii)) was withdrawn | ADJ line 776, line 814 |
| Q6's pass does not authorize `run-use` or mailbox writes in normal observer operation | `merged-requirements.md:573` |

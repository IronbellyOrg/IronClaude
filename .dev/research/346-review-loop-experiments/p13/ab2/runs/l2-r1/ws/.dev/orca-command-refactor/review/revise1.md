# Revise 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`. Ids repaired: REQ-1, REQ-2 (`review/round1.md:114-121`). Candidate: `specs/orca-worker-contract-spec.md`, edited in place (line numbers unchanged, no line added or removed). No PASS is claimed; a re-review decides.

## Byte accounting
Before 57763 bytes (`round1.md:6`), after 58530 bytes (`wc -c`), net +767. "Added" and "deleted" count each replaced span in full.

| Finding | Edits | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| REQ-1 | WC-4 sentence (spec:62), workflow row fix (spec:92), AC-1.4 (spec:198), section 2.3 parenthesis (spec:73) | 647 (452 + 108 + 59 + 28) | 135 (0 + 73 + 62 + 0) | +512 |
| REQ-2 | P1 scope (spec:159), AC-1.1 (spec:195) | 561 (261 + 300) | 306 (112 + 194) | +255 |
| Total | | 1208 | 441 | +767 |

## One row per finding id
| Id | Disposition | Where | Reason |
|---|---|---|---|
| REQ-1 | Applied by narrowing, choosing the second option of `round1.md:30`: no new flag. | spec:62 WC-4 gains an "Exception (REQ-1)" sentence: `workflow` contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, read from the final reply; a pre-creation stop writes no file, which WC-5 already maps to `--outcome failed` ("no report exists", spec:63); 7.2 steps 3-4 do not apply to that stop. spec:92 workflow fix now reads "State the package path in the final reply; pre-creation STOPs write no contract". spec:198 AC-1.4 matches. spec:73 notes `workflow` excepted. | Evidence: the path embeds a command-generated `<id>`, the skill never reuses a package, and the contract is "Not written for pre-creation STOPs" (`inventory/commands-b.md:267-275`). Removing the "write it for pre-creation STOPs" fix deletes the contradiction and adds no mechanism. Whether workflow already states the package path in its final reply is UNVERIFIED (skill files are outside the workspace); the row's fix column asks for it. |
| REQ-2 | Applied by narrowing, as recommended at `round1.md:41`. | spec:159 P1 now gives the flag and section only to commands whose own row is P1 plus the gate-free ready commands (brainstorm, init-lite); every other command gets both in its own phase with its gate resolutions. spec:195 AC-1.1 asserts the section only for commands whose row phase is P1 or earlier plus brainstorm and init-lite, with `load` exempt. | Evidence: gate resolutions sit in P2 and P4 (spec:100,104,109,113,114,121), and WC-9 turns outward defaults off under `--unattended` (spec:67), so a P1 flag on those commands would be half-wired. `load` has report "none" (spec:112). brainstorm and init-lite have "None" in the fix column (spec:83,87), so they need no gate change and join P1. |

## Left alone
Medium and minor findings M-1 to M-12 and n-1 to n-3 (`round1.md:105-112,114-121`) were not touched. The section 2.1 wording at spec:52 ("lists only its own gate resolutions") already fits the narrowed P1 and was not edited.

## UNVERIFIED
Every `sk/`, `cmd/`, `src/` and `CAPS` citation outside the workspace stays as the spec gave it; only `inventory/commands-b.md:267-275` was checked here.

# Revise round 1: Orca worker contract spec

Prompt followed: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Values: candidate = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, IDS = R1-B1, R1-B2 (the ids in the Reviser brief, `.dev/orca-command-refactor/review/round1.md:170-171`). Only the spec was edited, in place. No spec-panel was run and no PASS is claimed.

## Byte accounting
Before: 57763 bytes (the pre-edit file; identical to `.dev/orca-command-refactor/specs/history/spec-v1.md`, which is also 57763 bytes). After: 59034 bytes. Net +1271. Line count unchanged (every edit is in-line), so the line numbers below are the same before and after.

Method: each edit is a unique old/new string pair; added and deleted bytes are the UTF-8 sizes of the inserted and removed character spans from a character-level diff of that pair (so unchanged words inside a replaced span are not counted). Total added 1616, total deleted 345, 1616 - 345 = 1271 = after - before.

| Finding id | Edits | Bytes added | Bytes deleted |
|---|---|---|---|
| R1-B1 | 6 | 652 | 66 |
| R1-B2 | 10 | 964 | 279 |
| Total | 16 | 1616 | 345 |

## Findings
| Id | Disposition | Where applied (spec lines, revised file) |
|---|---|---|
| R1-B1 | Applied. Chosen repair: narrow the scope so each command gets `--unattended` and its `## Unattended mode` section only in the phase its section 3 row names, together with that row's gate resolutions (the first of the two options in the finding's recommendation: narrow AC-1.1 and the P1 scope to the P1 command set). No command therefore accepts the flag while it still prompts (the state trace in `round1.md:68`), and AC-1.1 can no longer pass on a gated command. | Line 76 (section 3 intro: section added in the phase the row names); line 154 (section 6 intro: the one phase-keying rule, coordinator passes the flag only after the command's phase, never to brainstorm or init-lite which are unchanged); line 159 (P1 scope: flag and section on the P1 commands only); line 73 (section 2.3 brief: `--unattended` only where the command's phase has passed); line 195 (AC-1.1: asserts the section for P1 commands only, none yet for later-phase or section-4 commands); line 240 (D3(a): pr-submit gets no section and no change, so it drops out of Phase 4, removing the contradiction with the 27 "needing a change" and AC-1.1). |
| R1-B2 | Applied. Chosen repair: one rule in WC-4 with three places, instead of the single `<output-dir>` rule: `<dir>/return-contract.yaml` for a directory flag; `<file>.return-contract.yaml` beside the file for a file-valued flag (tdd, init-lite, any row adding a file path), which is unique per output file and so keeps WC-11 (line 69) intact; and the two commands that fix their own place (adversarial `<output>/adversarial/...`, workflow `.dev/tasks/to-do/<id>/...` whose id the command chooses, so the coordinator learns the path from `worker_done --report-path`). The unconditional workflow pre-creation-STOP change is deleted (it named no location and conflicted with SA-3, `round1.md:77`); a workflow stop before its package exists writes no contract and ends `failed` under the existing WC-5 "no report exists" clause (line 63). The research row now adds `--output <dir>` (finding item (d)). | Line 62 (WC-4: heading and path rule, plus the workflow pre-creation exception); line 76 ("Contract" definition now points at WC-4's rule); line 73 (2.3: "known before dispatch" replaced by "follows from WC-4's rule"); line 92 (workflow row: pre-creation fix deleted); line 159 (P1 command list: workflow removed); line 149 (SA-4 defect-fix list: workflow gap removed); line 198 (AC-1.4: adversarial path named, workflow clause removed); line 116 (research row: output flag and contract place); line 200 (AC-2.2: tdd contract location stated). |

## Check that no new rule beyond the findings was added
Every addition carries the finding id in the text (R1-B1 or R1-B2). Additions beyond narrowing: the three-place path rule in WC-4 and the one-sentence phase-keying rule in section 6 (line 154). Each is what the finding's recommendation calls for ("define one rule that covers a directory flag, a file flag and a command-chosen directory"; "state which behaviour each phase adds per command"). No new flag, file, section or acceptance check was added; AC-1.1, AC-1.4, AC-2.2 were edited in place.

## Not touched (left alone as instructed)
Medium and minor findings M-01 to M-14 and N-1 to N-6 (`round1.md:136-160`). Notes that bear on the new text but were not acted on: M-01 (no rule when `--unattended` is passed with no output directory) still stands and now also applies to the file-valued case; M-12 (SA-1/SA-3 versus rows that change defaults) is unchanged; N-5 (`/sc:load` counted among the 27) is unchanged. The cli-portify row still says its contract file location is unnamed (line 105): the WC-4 rule now gives it a place if its output flag is a directory or a file, but the row was not edited because the finding does not name it.

## Verification limits
All citations used here are to files inside the workspace (the spec lines above and `round1.md`). The inventories were not re-checked against `cmd/` or `sk/` sources, which are not in the sandbox; the spec's own second-hand citations remain UNVERIFIED here, as in `round1.md` Coverage. The spec text was diffed against `specs/history/spec-v1.md` to confirm that only the 12 lines named above changed.

## Sandbox note
While setting up a helper script I mistyped a relative path and briefly created an empty directory `p11/a3-r2/tools` (outside the named sandbox) and ran one `ls` of `p11`. I removed the empty directories I created with `rmdir`; nothing else outside the sandbox was read or written. The helper script is `tools/apply.py` inside the sandbox.

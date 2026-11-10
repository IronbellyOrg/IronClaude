# Revise report, round 1

- prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51`, read in full.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Blocking ids taken from the Reviser brief, `.dev/orca-command-refactor/review/round1.md` (last section): F-1, F-2.
- Medium and minor findings (F-3 to F-8, N-1 to N-6) left alone. I did not run the spec-panel and award no PASS.
- Evidence: all citations are to the candidate or round1.md, both read in the workspace. `cmd/`, `sk/` and other paths outside the workspace are UNVERIFIED and no new ones were added.

## Byte accounting

Candidate size (`wc -c`): before 57763, after 58091, net +328. Deleted bytes per id are the wording replaced inside each edit and are counted in the net (new text minus old text); the edits delete nothing outright.

| Edit | Line | Net bytes | Finding id |
|---|---|---|---|
| AC-1.1 scope "every command in the P1 row except load" | 195 | +17 | F-1 |
| AC-1.2 skips load | 196 | +45 | F-1 |
| section-introduction sentence, phase-scoped, load excepted | 76 | +49 | F-1 and F-2 (shared, counted under F-2) |
| P1 flag scope narrowed | 159 | +82 | F-2 |
| rule sentence after the phase intro | 154 | +135 | F-2 |

Per id: F-1 +62; F-2 +266; total +328, which matches the `wc -c` difference.

## Findings

| Id | Disposition | Where applied |
|---|---|---|
| F-1 | Applied, by narrowing the two acceptance checks to match the load row (`SPEC:112`, `SPEC:265`: no report, usage-line fix only) | AC-1.1 (`SPEC:195`) now asserts the section only for commands in the P1 row except load; AC-1.2 (`SPEC:196`) skips load because it writes no contract; the section-introduction sentence (`SPEC:76`) no longer says every changed command gains the section and names load as the exception. The load row and Decision stand unchanged. |
| F-2 | Applied, by narrowing P1 scope | P1 row (`SPEC:159`): the flag and section go only to the listed commands that have no unconverted gate, not to load and not to any command a later phase converts; sentence added after `SPEC:154`: a command gets the flag and its section only in the phase that resolves its gates, and under D3(a) (`SPEC:240`) pr-submit gets neither. This removes the state the review described, an accepted `--unattended` on implement, pr-submit, post-release and roadmap before their gates are converted (WC-2, `SPEC:60`). AC-1.1 and AC-1.2 follow from the P1-row restriction. |

Note: commands the P1 row does not list (reflect, release-split, tdd, troubleshoot and the P2 to P4 commands) first get the flag in their own phase; rows `SPEC:160-162` were not edited because the `SPEC:154` rule states it for all of them.

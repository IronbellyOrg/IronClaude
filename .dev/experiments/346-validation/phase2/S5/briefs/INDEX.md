# S5 briefs: what each role was told in the original run

Source for every file: `AA` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/aaee1ebf-4ec9-494f-85e0-52f3697170b5.jsonl` (the executor session; the jsonl line number is in each file name). Files are byte-for-byte what the log holds (extracted with `derivation-scripts/extract.py`; the round 2 to 4 briefs are rebuilt with `derivation-scripts/mkbriefs.py` from the logged `sed` plus heredoc command and match the file size the log printed afterwards).

Roles in this incident:
- **Writer** = the executor session that ran `/sc:implement` and produced the package (tasks T1 to T5). Its instructions are the command (`00a`, `00b`), the protocol skill text it loaded (`01`) and the plan inside the package (`inputs/package-R1/<id>/TASK-WF-writeTheP0LivePl-20261103-215902.md`, identical to the plan the log read at `AA` L70). The T1 to T5 per-task reviewer prompts are inside the package (`artifacts/retries/T<n>/prompt-1-1.md`); they are not part of the final-review loop that is replayed.
- **Reviser** = the same executor session, acting on the owner's message after each failed review (`afterR*` files). The owner messages are the only revise instruction; the fixes themselves were chosen by the executor.
- **Reviewer** = one fresh `general-purpose` subagent per round, told to read a prompt file (`R*-reviewer-brief`, `R*-spawn-prompt`).

| File | Role / round | Log line | Bytes | sha256 (first 16) |
|---|---|---|---|---|
| `00a-command-L19.txt` | writer: command as typed | L19 | 221 | 6f587422557a8169 |
| `00b-command-expansion-L20.md` | writer: command file text | L20 | 4169 | 17ca9d8f6f809d4c |
| `01-skill-load-L54-sc-implement-protocol.md` | writer: protocol skill text | L54 | 20412 | af54fed8a9ce62dc |
| `R1-reviewer-brief-L1988-final-prompt.md` | reviewer round 1: prompt file (written twice, identical, L1988 and L1994) | L1988 | 5635 | e6b3b2b6e09585c2 |
| `R1-spawn-prompt-L2001.txt` | reviewer round 1: Agent prompt | L2001 | 167 | 5138ba3ff20cf73a |
| `afterR1-owner-revise-L2058.txt` | reviser after round 1 | L2058 | 340 | 5e894151239cff02 |
| `R2-reviewer-brief-L2142-final-prompt-2.md` | reviewer round 2: base prompt, `state1`->`state3`, plus "new archive attempt" paragraph | L2142 | 6011 | 8ee3ba622f5a6fb2 |
| `R2-spawn-prompt-L2157.txt` | reviewer round 2: Agent prompt | L2157 | 169 | ad302ea96ca5ad2d |
| `afterR2-owner-revise-L2204.txt` | reviser after round 2 | L2204 | 472 | ecde688f3f30c418 |
| `R3-reviewer-brief-L2335-final-prompt-3.md` | reviewer round 3: base prompt, `state1`->`state5`, plus third-attempt paragraph | L2335 | 7128 | 0c3bc71d8efb6deb |
| `R3-spawn-prompt-L2342.txt` | reviewer round 3: Agent prompt | L2342 | 169 | b2c1699b4331a99c |
| `afterR3-owner-revise-L2390.txt` | reviser after round 3 (first message) | L2390 | 391 | 650f509db359125b |
| `afterR3-owner-revise2-L2427.txt` | reviser after round 3 (second message, after the executor paused at L2415 with one more finding) | L2427 | 327 | b77339c08e4bb1e6 |
| `R4-reviewer-brief-L2487-final-prompt-4.md` | reviewer round 4: base prompt, `state1`->`state7`, HARD RULE paragraph plus fourth-attempt paragraph | L2487 | 8373 | ce2853c84608097b |
| `R4-spawn-prompt-L2499.txt` | reviewer round 4: Agent prompt (adds a personal uv-only rule) | L2499 | 327 | c6569ec4073432db |

Agent call shape for all four spawns (same keys each time, checked at L2001, L2157, L2342, L2499): `{"description": "<Independent|Second independent|Third independent|Fourth independent> final review[ of the package]", "subagent_type": "general-purpose", "prompt": "<spawn prompt>"}`. No `model`, no `run_in_background`. The duplicate log lines L2006, L2161, L2351, L2503 carry the same tool-use id; there was one spawn per round.

What is NOT in this folder, and why:
- Nothing was lost for the reviewer and reviser roles: every message is present verbatim.
- The executor's own free-text reports to the owner (`AA` L2051, L2193, L2378, L2415, L2559) are not briefs. They are in `../baseline-reference/`.
- The owner's wording is the only revise instruction; there is no separate writer brief for the fixes. The fixes are in `../inputs/round-deltas/edits.json` (what the executor actually changed).

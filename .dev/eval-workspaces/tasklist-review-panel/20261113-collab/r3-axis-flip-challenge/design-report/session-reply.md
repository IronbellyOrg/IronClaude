| Status | Result |
|---|---|
| DONE | Wrote the design for Redesign 3 (Axis-Flip Challenge): `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/DESIGN.md` (952 lines). It covers all seven items you asked for. |
| DONE | Three independent reviews. The first found 10 blocking defects; review 3 confirmed all but one fixed. That last one is fixed too, but only after review 3, so no reviewer has checked it (details below). |
| DONE | Wrote the return contract: `.../r3-axis-flip-challenge/design-report/return-contract.yaml`. |
| NEXT | Read section 16.2 of DESIGN.md (seven defaults the source left open) and say if any should change. Then build from the design. |

Nothing is built yet: no scripts, no tests, no sandbox.

**Things you should know before building**

- **The source contradicts itself.** Its integrity rule says no message to a reviewer may contain 12 or more characters quoted from ground truth. But every Axis-Flip challenge is, by design, a quote of a sentence another reviewer flagged. The design applies the rule to everything except those quotes, and checks separately that each quote really came from a peer's finding. This is open question Q1.
- **The other two panels.** On sonnet + 2x luna and haiku + 2x luna, the strong model takes ember's role, and the lunas wait for it to finish before their second pass. At the source's planning times, haiku gets one challenge only if its slowest turns stay under 32.7 s; above that, only the lunas do a second pass.
- **The judge stays unchanged and writes only into the r3 folder.** `judge-one.sh` normally writes its scores inside `20261111-a1`. The launch script points it at the r3 folder through a relative path instead, so the script stays byte-identical.
- **Sandbox base commits.** I worked out the base commits from git history, because no file records them. A first check (Gate 0) confirms them before any run.
- **Two problems review 2 found on this machine:**
  - Your session-start hook would build a 136 MB code index inside each sandbox. The design switches it off for reviewer and judge sessions.
  - Reviewers that run `uv run` leave a `.venv/` folder in the sandbox. The final fix logs these ignored files and deletes them after the last run, instead of quarantining the run. This is the fix that no review has checked.

**RECOMMENDED ACTION:** read section 16.2 of DESIGN.md and give your answers to the seven open questions before building, especially Q1 (the integrity rule).

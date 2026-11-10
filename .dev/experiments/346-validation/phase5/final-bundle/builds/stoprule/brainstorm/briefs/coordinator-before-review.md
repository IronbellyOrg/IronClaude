# Inserted coordinator step: before each review (stoprule arm)

Placeholders: `<spec>` the spec under review; `<run dir>` the replicate's folder for coordinator files; `<N>` the review number (1, 2 or 3); `<report>` the review report to create (`review/spec-panel.md`, `review/spec-panel-round2.md`, `review/spec-panel-round3.md`); `<prior report>` the previous review's report; `<saved copy>` the copy of the spec the previous review saw, saved by `coordinator-fix-cycle.md` step 7 before the reviser ran. `<skill base>` is `~/.claude/skills/sc-spec-panel-stoprule-protocol`.

Owner ruling: the reviewer session runs only script calls that write no file. This step runs `begin`, which writes the report, in the coordinator session.

1. Review 2 or 3 only: check that `<saved copy>` exists and that `sha256sum <saved copy>` starts with the `spec=` value of `<prior report>`'s sentinel line (`<!-- stoprule v1 review=... spec=<12hex> ... -->`). If not, stop: the loop has no valid baseline.
2. Run `begin`:
   - review 1: `uv run --no-project python "<skill base>/scripts/stoprule.py" begin --report <report> --spec <spec>`
   - review 2 or 3: `uv run --no-project python "<skill base>/scripts/stoprule.py" begin --report <report> --spec <spec> --re-review <prior report> --baseline <saved copy>`

   Exit 0: continue. Exit 4: do not review; HALT and escalate to the user with the open blocking findings (the printed escalation, or "loop already ended" for a PASS). Exit 5: stop and report the printed reason.
3. Re-check the sha256 of the three installed items against the run log (`INSTALL.md` section 3) and stop on any difference.
4. Dispatch the reviewer with its template brief (`T05-R1-reviewer-L11-699ae853.txt`, `T07-R2-reviewer-L11-aff19d65.txt` or `T09-R3-reviewer-L11-1c9a7ec8.txt`), with the worktree path and per-run values filled in and no other change to the brief text. Its command line is `/sc:spec-panel-stoprule <spec> --mode critique --focus requirements,architecture` at review 1 and `/sc:spec-panel-stoprule <spec> --mode critique --focus requirements,architecture --re-review <prior report> --baseline <saved copy>` at reviews 2 and 3. Never pass `--unattended`: the variant has no `## Unattended mode` section.
5. What the reviewer needs from `begin` is already in `<report>`: the `begin` record of the ledger block carries the changed hunks (`hunks`) and the prior blocking ids (`priors`), and the frozen rubric is `<skill base>/refs/rubric.md`. The reviewer adds its `claim`, `prior` and `checked` lines inside that block, self-checks with `seal --dry-run` (one repair turn), writes its prose, and writes no `verdict:` line. It does not run `check`: the report has no sentinel until `finalize`.
6. When the reviewer returns, run `coordinator-fix-cycle.md`.

# Pre-run replay gate, before any live stoprule run (source spec section 5.1)

Placeholders: `<arm checkout>` each of the six existing A/B checkouts with a review-3 report: `exp346-ab-ctl-r1`, `exp346-ab-ctl-r2`, `exp346-ab-trt-r1`, `exp346-ab-trt-r2`, `exp346-ab-flg-r1`, `exp346-ab-flg-r2` under `/home/coder/workspaces/worktrees/IronClaude/` (read-only); `<gate dir>` a scratch folder for this gate; `<claims file>` the hand-transcribed claim lines of one report. `<skill base>` is `~/.claude/skills/sc-spec-panel-stoprule-protocol`.

Purpose: before the live runs, check the grader against the review-3 reports the earlier arms already produced. The analyst's reading finds all 9 counted claims of control r1 (8) and flg-r2 (1) rubric-blocking, so a grader that demotes more than 3 of those 9 is miscalibrated and is fixed first.

1. For each `<arm checkout>`, copy into `<gate dir>/<arm>/` the spec the round-3 review saw (`.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md`), the spec the round-2 review saw (`spec-v2-after-round1.md`) and the round-3 report (`.dev/orca-command-refactor/review/spec-panel-round3.md`).
2. Transcribe that report's blocking findings into `<claims file>` as `claim` lines, as `tests/skills/fixtures/stoprule/ctl-r1/review3-claims.jsonl` does for control r1 (which can be reused as is): the quote is a verbatim substring of the spec-v3 line the report cites for the finding, the label is the report's, the outcome is the report's statement of the wrong result.
3. The old round-2 reports carry no stoprule sentinel, so write a scaffold review-2 report in `<gate dir>/<arm>/` the way the test helper `scaffold_review2_report` in `tests/skills/test_stoprule_script.py` does (sentinel `review=2/3`, `spec=` the sha256 prefix of spec-v2, the pinned rubric prefix, and a ledger whose recomputed verdict matches its last line). It stands in only for the missing sentinel.
4. Run, with `<report>` = `<gate dir>/<arm>/replay-review3.md`:
   - `uv run --no-project python "<skill base>/scripts/stoprule.py" begin --report <report> --spec <gate dir>/<arm>/spec-v3-after-round2.md --re-review <scaffold report> --baseline <gate dir>/<arm>/spec-v2-after-round1.md`
   - add the `<claims file>` lines inside the report's ledger block;
   - `seal --report <report> --spec <spec-v3>` (twice if it exits 3);
   - `grade-prep --report <report>`, one `finding-grader` Agent call per batch, `apply-grades` per reply.
5. `uv run --no-project python "<skill base>/scripts/stoprule.py" status --report <report>` lists each claim's status. Count, for control r1 and flg-r2 together, how many of the 9 counted claims did not end `confirmed` (`minor`, `minor-form`, `unconfirmed`; `late-found` is the ratchet, reported separately).
6. Gate: more than 3 of the 9 demoted means the grader is miscalibrated: fix the grader prompt or the rubric (a rubric change is a new rubric version) and replay again before any live run. Record the counts for all six reports in the run log.

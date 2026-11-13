# Helper scripts that lived only in /tmp during the study

Copied 2026-11-13 from /tmp: only files that reference this eval (path, run-reviewer, combos/, arms/scoring). Unrelated scratch from other sessions in /tmp was NOT copied.
They are verbatim copies: many hard-code /tmp paths and the 20261111-a1 eval directory, so read before re-running.
Scripts already stored under analysis/ (merge-b7..b11, b7..b11 launchers, table and test scripts) are not duplicated here.
Key ones: b4-job-one.sh (job runner, honours /tmp/cancel-<row>), judge-one.sh (blind judge prompt), anon-combos.sh (anonymisation),
merge-b6.sh (merge pattern the later merge-bN scripts derive from), gen-judge-list, checks-gate8, merge-src-rows, startcombo*.

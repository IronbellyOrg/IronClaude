# Recorder step: after each review, outside the loop (stoprule arm)

Placeholders: `<report>` a finalized review report; `<review-3 report>` the replicate's review-3 report; `<transcript>` the session transcript (`.jsonl`) of the session that made the `finding-grader` Agent calls (under the owner ruling, the coordinator session; under `~/.claude/projects/<project folder>/<session id>.jsonl`); `<run log>` the replicate's validity record. `<skill base>` is `~/.claude/skills/sc-spec-panel-stoprule-protocol`.

1. Grader integrity, per review: `uv run --no-project python "<skill base>/scripts/stoprule.py" verify-transcript --report <report> --transcript <transcript>`. Record the printed `grader-integrity: verified|mismatch|unverified` line in `<run log>` (metric M8). A `mismatch` voids the replicate. `unverified` means the transcript was missing or unreadable, or held no Agent tool result.
2. Compliance, per review: `uv run --no-project python "<skill base>/scripts/stoprule.py" check --report <report>` must exit 0, and a second run must print the same line (metric M3; F4 if not).
3. Owner measure, per replicate: `uv run --no-project python "<skill base>/scripts/stoprule.py" count --report <review-3 report>`. Record the three printed values:
   - `m0_label_cm`: new review-3 findings whose reviewer label is CRITICAL or MAJOR, whatever the script did with them, carried priors excluded (metric M0, the pre-registered bar);
   - `m0_deferred_cm`: the part of `m0_label_cm` the scripts deferred, demoted or withdrawn (final status not `confirmed` or `confirmed-audit`, or dropped from the ledger between the first and second `seal`);
   - `m1_open_confirmed`: the sentinel `confirmed=` plus the frozen `unresolved-prior` count, one defect counted once (metric M1).

   Owner decision: findings the scripts defer, demote or withdraw stay open for the success measure, so the review-3 critical+major count is `m0_label_cm`, deferred, demoted and withdrawn findings included. This never changes a recorded verdict.
4. Growth, per fix cycle: `wc -c` of the spec before and after the reviser (metric M2). Reviser leak: the ids `check-disposition` listed (metric M5).

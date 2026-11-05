# INV-034 round: Variant B advocate

**Verdict: MODIFY.** With the modification below, INV-034 is ADDRESSED. R-034 as written is not, because it fails on the exact case INV-034 names.

## Steelman of A (no time window)

An evidence signal beats a clock. Any settle window is a guess: too short and `clean` still comes early, too long and every no-Actions repo stalls. A's rule is also deterministic and testable as a pure function. R-034 keeps all of that: it drops the window and keeps the fail-closed bias. I concede B's `settle_polls` (round-inv-advocate-B.md INV-034 row) is the weaker design.

## Where R-034 breaks

1. **The replaced head cannot be read after the push.** `poll-ci-checks.sh:45,54-55` queries `gh pr view/checks <PR>`, which always reports the current head. After the push the replaced head is gone from that surface. So "readable once" must mean "read before the push".
2. **Wrong answer in the target scenario.** The probe's case (invariant-probe.md:44) is a previously `CONFLICTING` PR. There, `pull_request` workflows never ran on the replaced head, so it has zero checks. R-034's second branch then treats the repo as "no Actions" and returns `clean`, which is today's bug (`ci.py:36-37`, `poll-ci-checks.sh:70`). An empty replaced head is not evidence of no CI when the PR was conflicting.
3. **No earlier poll exists for a Tier 1 sync.** Wave 8 only starts after the Augment terminal (`SKILL.md:277`), so a sync push can happen before any CI poll in the run.
4. **Timeout wording.** `SKILL.md:78` says the CI wait uses `timed_out`; `TERMINAL_TIMEOUT` is the review-phase outcome. R-034 names the wrong one.

## Modified rule R-034'

`classify_checks(payload, *, wait_sha=None, expect_checks=False)`. When `expect_checks` is true, a head-matching payload with an empty or absent `checks` list returns `polling` (new `ci.py` branch before `ci.py:36-37`). The default keeps today's behaviour. The skill sets `expect_checks=True` for the CI wait that follows a push this run made when ANY of these holds:

- (a) an earlier CI poll in this run returned a nonempty `checks` list;
- (b) the replaced head's checks, read by one `poll-ci-checks.sh` call immediately BEFORE the push, were nonempty, or the read failed or did not parse (fail closed);
- (c) the push is a conflict-sync push (the PR was `CONFLICTING`), because an empty list on the replaced head is then not evidence of "no Actions".

Only a non-conflict push whose replaced head read as two confirmed empty arrays, with no checks seen earlier in the run, leaves `expect_checks=False` (today's `clean`).

Expiry with `expect_checks=True` and still no checks is the existing Wave 8 `timed_out` result. The report says "no checks registered on <sha> before timeout" and never `clean` or "tests passed". Tests in `tests/pr_submit/test_ci_classify.py`: empty plus expect plus matching head returns `polling`; head mismatch still `polling`; default unchanged; nonempty list unaffected.

**Residual cost:** a conflict-sync on a repo with no workflows waits to `--timeout` and reports `timed_out`. That is safe, and the report text names the cause.

# INV-034 round: Variant A advocate

**Verdict: MODIFY**

**Steelman of the settle window (B, C).** It adds no new `gh` surface, needs no history, and handles a repo with no evidence either way. One or two extra polls cost about a minute.

**Why it still fails.** When the window ends with zero checks, B and C fall back to `clean`. That is the same false `clean`, only later. GitHub's registration delay has no upper bound: queued runners, or a merge ref that must be rebuilt after a conflict. Today two parsed empty lists already mean `clean` (`poll-ci-checks.sh:69-70`, `ci.py:36-37`), and `SKILL.md:277` then sends `transition(clean)`. A fixed delay only guesses how long to wait.

**Why R-034 as written fails.**
1. GitHub does not run `pull_request` workflows while a PR has a merge conflict. The head that the sync push replaces therefore usually shows zero checks in exactly the INV-034 case. R-034 treats that as "no Actions" and returns `clean`.
2. `gh pr checks` reads only the current PR head (`refs/ci-poll.md:15-18`). The replaced head cannot be "readable once" through the existing surface.

**Modified rule R-034′:**
- When the run pushes, the SKILL computes `expect_checks` once and records it in the run-log, so a resume reuses it. It is true if **any** of these holds:
  - (a) checks were seen earlier in this run on any head;
  - (b) `pre_push_sha` has at least one check run or status context;
  - (c) `base_sha` has at least one check run or status context.
- For (b) and (c), the poll script gains `--evidence-sha <sha>`. It reads `gh api repos/$REPO/commits/<sha>/check-runs` and `.../status` and emits `evidence_checks:<n>`, or `-1` when a read fails or cannot be parsed. This keeps `gh` out of the core (`refs/ci-poll.md:52-53`).
- `-1` counts as "had checks" (fail closed).
- `classify_checks(payload, *, wait_sha=None, expect_checks=False)`: when `expect_checks` is true and the chosen list is empty, the result is `polling`, inserted before `ci.py:36`. The default keeps today's behaviour.
- When `--timeout` expires with no checks, the result is `TERMINAL_TIMEOUT` with reason `ci_not_started`. It is never `clean`, and the report never says "tests passed".
- A repo is treated as having no Actions only when (a), (b) and (c) all read zero. In that case an empty list is `clean`, as today.
- Amend `refs/ci-poll.md:21` and `SKILL.md:277` ("only parsed empty … prove there are no Actions") to add "and `expect_checks` is false".
- Tests go in `tests/pr_submit/test_ci_classify.py`:
  - empty list with `expect_checks` true → `polling`;
  - empty list with `expect_checks` false → `clean`;
  - a head mismatch still takes precedence;
  - the existing pins stay green unchanged.

**Remaining risk, outside INV-034.** Checks can register one at a time. If one workflow has registered and passed while another has not registered yet, the result can read `clean` early. INV-034 is about the window before any check exists, which this rule closes.

**INV-034: ADDRESSED** under R-034′. It is not addressed under R-034 as written.

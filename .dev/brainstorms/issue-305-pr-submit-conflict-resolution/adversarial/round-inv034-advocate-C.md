# INV-034 focused round: Variant C advocate (haiku, QA)

Verdict: **MODIFY**. Repo lines re-read at `119622e3` on 2026-11-04.

## Steelman of A (no time window)

A is right that evidence beats a clock. A fixed grace (C's own ~60s, B's 3 polls) is racy both ways: GitHub's check registration is unbounded, so a short window re-admits the false `clean` and a long one taxes every no-Actions repo with dead polling. The script already prefers proof over time — "only two confirmed empty arrays prove there are no configured checks" (`poll-ci-checks.sh:75-78`, pinned at `refs/ci-poll.md:21`) — and R-034 extends that spirit deterministically, keeping the core clock-free. B's own concession (sha-pinned query "is exact for 'registered'", deferred only because no-workflow repos "still need a settle window") dissolves: the replaced-head read IS the no-workflow answer. I withdraw the grace window.

## Why R-034 still needs modification

Two defects, both in how the evidence is read:

1. **The surface is unnamed and the natural one is blind in the flagship case.** "Already polled earlier in the run" is empty for a Tier 1 sync: Wave 8 arms after the review terminal and the sync push happens at Wave 8 entry, before the first CI poll (`SKILL.md:277`). And a fresh PR-scoped read fails too: on a previously conflicting PR both check lists parse empty (`invariant-probe.md` INV-024; `refs/ci-poll.md:16-18` surface) even though the head ran checks before the base moved — so `gh pr checks` on `pre_push_sha` reads "no Actions" and R-034 returns the exact false `clean` INV-034 names. The evidence must be commit-scoped, as A's own row specified: `gh api repos/<repo>/commits/<sha>/check-runs` plus `/status` (round-inv-advocate-A.md, INV-034 row). Check runs persist on the head sha after the PR turns conflicting; the PR-scoped list does not.
2. **`pre_push_sha` alone misses the born-conflicting PR** (head never ran a check). A's row also reads the recorded `base_sha`; R-034 dropped it. Keep it — same read, one more already-recorded sha.

## R-034′ (exact)

R-034 with: evidence = commit-scoped check runs **or** status contexts, read once for **`pre_push_sha` OR `base_sha`** via `gh api .../commits/<sha>/check-runs` and `.../status`; both reads parsed and empty ⇒ no-Actions; any read failed/unparsable ⇒ expect checks (fail closed, `poll-ci-checks.sh:76-78` shape). Carrier `classify_checks(payload, *, wait_sha=None, expect_checks=False)` unchanged; timeout stays `TERMINAL_TIMEOUT` (`refs/ci-poll.md:32`, `SKILL.md:78`).

## Acceptance tests (`tests/pr_submit/test_ci_classify.py` + evidence-setter)

1. `{head_sha:s, checks:[]}`, `wait_sha=s`, `expect_checks=True` → `polling`.
2. Same but checks all-pass → `clean` (nonempty overrides).
3. Same as 1 with `expect_checks=False` → `clean`.
4. All existing tests green unmodified (default pins `ci.py:36-37`, `tests/pr_submit/test_ci_classify.py:36-38`).
5. `head_sha != wait_sha`, empty, `expect_checks=True` → `polling` (mismatch precedence, `ci.py:31-32`).
6. Setter: commit-scoped read of `pre_push_sha` nonempty (conflicting PR) → `True`; both empty → `False`; read fails → `True`; `pre_push_sha` empty but `base_sha` nonempty → `True`.
7. Live leg on the INV-033 scratch run: first post-merge poll must not terminate before a check row or timeout.

**INV-034: ADDRESSED** (by R-034′).

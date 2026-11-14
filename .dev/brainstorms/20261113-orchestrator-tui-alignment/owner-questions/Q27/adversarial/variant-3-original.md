# Proposal C: yes; commit SW-02's own plan package inside PR #539

## Answer

Yes: SW-02's `/sc:workflow` plan package is written in the #539 checkout and committed in PR #539 with the fix, as the one `.dev/tasks/` package allowed there.

## What happens next if the owner picks it

1. The #539 author first checks whether an existing plan covers SW-02 (spec criterion SW-02 (5)); if not, runs `/sc:workflow` in the #539 checkout, which writes `.dev/tasks/to-do/<id>/` there, staged under the always-staged rule.
2. The #539 author runs `/sc:implement` on that plan in the same checkout.
3. The package is committed by named paths together with the fix and its tests, and pushed by hand under the SW-02 push approval.
4. The ledger records the plan's path in #539.

## What it unlocks

- One checkout, one session, one PR: the plan, its progress ledger and the fix stay together, and the always-staged rule and the named-paths commit rule no longer pull in opposite directions (the conflict the probe found, `invariant-probe.md:20`).
- No dependency on Q26: SW-02 can be planned even if no coordinator home exists yet.
- Readers of #539 find the plan for the fix in the same PR. Precedent: #539 already carries 921 `.dev/tasks/to-do/` files (measured 2026-11-14).

## What it costs or risks

- #539 grows by one more package (a few files) on top of 1003 files; a reviewer must see that it is a plan, not a program, collector, key or sidecar.
- The exception must stay narrow: it covers SW-02's own plan only; no other program artifact (ledger, debate files, reviews) may follow it into #539.
- If the plan's own review or the executor's final review writes extra artifacts into the package, those are committed too.

## What stays unresolved

- Nothing material beyond the existing-plan check.

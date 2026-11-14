<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Merge date: 2026-11-14T01:05Z -->

# Merged answer for Q27: SW-02's plan package and PR #539

<!-- Source: Base (original, modified) - guard added per Change 2 -->
## Answer

Yes: SW-02's own `/sc:workflow` plan package is written in the #539 checkout and committed in PR #539 with the fix. The exception covers that one package only; no other program file (ledger, debate files, reviews, reflect reports) enters #539.

<!-- Source: Base (original, modified) - steps 1 and 3 replaced per Changes 1 and 3 -->
## What happens next

1. The #539 author records in the ledger that the existing sweep task package (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`, status Done) does not plan SW-02, then runs `/sc:workflow` in the #539 checkout, which writes `.dev/tasks/to-do/<id>/` there.
2. The #539 author runs `/sc:implement` on that plan in the same checkout (the executor refuses a plan stored in another checkout, `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:11`).
3. The commit stages named paths only: the fix, its tests, and the package including `progress.md`, `artifacts/` and its move from `to-do/` to `done/`. The plan's review reports written outside the package (`.dev/reflect/...` and `docs/memory/reflect/deviation-patterns-<slug>.md`) stay uncommitted.
4. The push is made by hand under the SW-02 push approval.

<!-- Source: Base (original) -->
## What it unlocks
The plan, its progress record and the fix stay in one checkout and one PR; nothing waits for Q26; the always-staged rule and the named-paths rule agree.

## What it costs or risks
- #539 grows by one package (a few files plus review artifacts) on top of 1003 files.
- Reviewers must be told the package is a plan, not a program, collector, key or sidecar.

<!-- Source: Base (original, modified) per Change 3 -->
## What stays unresolved
- Nothing that blocks; the two commit-scope details are fixed in step 3.

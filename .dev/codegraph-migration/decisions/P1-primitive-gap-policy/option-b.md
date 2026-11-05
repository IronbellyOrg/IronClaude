# Option B: Phase 1 removes decorative mentions only; load-bearing steps wait for Phase 3

Read `context.md` first.

Phase 1 deletes the 165 decorative rows (frontmatter `mcp-servers`, prose, tables, comparison text) and does the already-decided memory rewrite (MEM) and ACT/NUDGE deletions. The roughly 20 load-bearing SYM/REF/DIAG/ALLOW rows keep naming `mcp__serena__*` until Phase 3 replaces them with codegraph calls in one pass. Release constraint: Phases 1, 2 and 3 merge to `master` together (one unit), so no released build contains a dangling step.

For: each load-bearing step is edited once, straight to its final codegraph form; least total work; Phase 3 designs the reflect chain with full freedom.
Against: every intermediate commit on the feature branch has steps calling a removed tool, so the Phase 1 acceptance search ("zero Serena hits outside `.dev/`") cannot pass at the end of Phase 1 and needs a large exception list; ties Phase 1's merge to Phase 3, which is a larger design task (reflect) and is not yet planned to merge with Phases 1-2; if Phase 3 slips, either the merge waits or dangling steps ship.

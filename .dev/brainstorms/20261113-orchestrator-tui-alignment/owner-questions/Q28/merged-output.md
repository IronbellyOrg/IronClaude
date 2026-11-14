<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14T01:45Z -->

# Merged answer for Q28: what `/sc:pr-submit` may do on PR #539

<!-- Source: Base (original, modified) per Changes 1, 2, 3 -->
## Answer

No `/sc:pr-submit` on PR #539 at any level until all three hold: SW-02 has landed the owner's INV-008 ruling; the Codex security thread at `probes.py:1211` is resolved (marked resolved, not only replied to); and Codex's review of the SW-02 push has come back with no new finding about git configuration. After that, the #539 author runs `/sc:pr-submit --pr 539 --monitor 3 --merge-guard off` under a grant row that lists every write.

<!-- Source: Base (original, modified) per Changes 4 and 5 -->
## What happens next

1. Until the three gates hold, the #539 author pushes SW-02 and SW-03 by hand, staging named paths, after checking that the PR is open and its head is as expected.
2. The owner writes the #539 grant row: attach (`--pr 539`), local fix commits and troubleshoot artifacts, push, thread replies and resolves, the "augment review" and Codex re-trigger comments, the `/sc:auggie-review` report comment if Augment declines the PR as too large (or "hold on a decline"), `--merge-guard off`, resume effects; never merge. The row also states: stop before any edit when a verified finding concerns git configuration (`core.fsmonitor`, `filter.*`, `include*`, `GIT_*` or the git allow-list); and check `gh pr view 539 --repo IronbellyOrg/IronClaude --json state,headRefOid` before every push, because with `--merge-guard off` the tool's own open-PR check may not run.
3. The run fixes verified Medium-or-higher findings and failing checks, pushes, replies and resolves; it re-polls once before declaring a reviewer clean.
4. The owner does not merge while a fix cycle runs, then merges (SW-05).

## What it unlocks
The project's review loop, with its verification and push checks, on #539 once the INV-008 risk window has passed.

## What it costs or risks
- Hand pushes until Codex's review of the SW-02 push is back.
- The git-configuration stop rule is a written instruction the session follows, not a switch in the tool.

## What stays unresolved
- Whether the owner prefers `--merge-guard draft` (the tool turns the PR into a draft during a fix cycle, which also guarantees the open-PR check) over `off`.

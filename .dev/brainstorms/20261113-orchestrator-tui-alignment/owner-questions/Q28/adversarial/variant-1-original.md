# Proposal A: nothing before the ruling lands; afterwards full monitoring at level 3, with no draft toggle

## Answer

No `/sc:pr-submit` on PR #539 until SW-02 has landed the owner's INV-008 ruling and the owner's reply has closed the Codex security thread; after that, a designated PR session runs `--monitor 3 --merge-guard off` on #539 under a grant row that lists every write. Level 1 (propose only) before the ruling only if the grant row says so explicitly.

## What happens next if the owner picks it

1. Until the ruling lands, the #539 author pushes SW-02 and SW-03 by hand, staging named paths, each under its push grant.
2. The owner writes the #539 grant row: attach to #539 (`--pr 539`), local fix commits and troubleshoot artifacts, push, thread replies and resolves, the "augment review" re-trigger comment, `--merge-guard off`, resume effects; never merge.
3. A top-level PR session runs `/sc:pr-submit --pr 539 --monitor 3 --merge-guard off`. It fixes verified Medium-or-higher findings and failing checks, pushes, replies and resolves, and stops before any fix, reply or resolve if a new finding needs an owner ruling.
4. The owner merges (SW-05).

## What it unlocks

- The project's standard review loop on the PR that most needs it: Augment and Codex findings and red checks are fixed without hand work.
- No visible draft flip on a 1003-file PR that has been open for days.

## What it costs or risks

- At level 3 the tool acts on every verified Medium-or-higher finding, including a Codex P1 or P2 that touches git configuration again; the "stop on a finding that needs an owner ruling" rule rests on the session's judgment, not on a switch in the tool.
- Without the draft guard, the PR stays mergeable while a fix cycle runs; the owner must not merge mid-cycle.
- A Codex security review can land after "clean" (owner memory), so the session must re-poll before declaring clean.

## What stays unresolved

- Whether level 1 before the ruling is wanted (the owner says so in the grant row or not).

# L2 pre-push disposition (issue #394, Task 21)

## The verdict this follows

`./artifacts/b-ctx-verdict.md`, section "L2 verdict", says:

> L2: BLOCKED

and names the missing launcher or harness integration exactly:

> Missing launcher or harness integration, named exactly: (1) a live observation of subagent, nested-subagent, background-Bash-to-Git and Monitor-to-Git process trees with the same-worktree human terminal at the same time; (2) a live observation of resume in a new Claude process, `/clear`, fork and auto mode (E:19); (3) the claim launcher provisioning the governed level record for the actual logical session and checking the adapter runtime before it advertises protection (E:19, D:565); (4) a verified install place for the shared `hooks/pre-push` file (U28, D:377,457). Until these exist, L2 cannot be built or claimed.

## What this plan builds, and what it does not

This plan wrote no pre-push file, no L2 installer and no L2 test beyond the
tests of the IR-7 detection. The only L2
code is the detection in the claim script (IR-7): `l2_status()` reports
`absent` when the worktree has no executable file at git's `hooks/pre-push`
path, and the claim then adds the warning `W-L2-ABSENT` and lets the launch
continue (see `./artifacts/ir7-consequence.md`). It reads the file's presence
and mode only. It never creates, edits or adopts a hook, and it never claims
that an existing hook is the owned one. A search of this plan's changed files
for a file named `pre-push` finds none.

Of the four missing items, this plan closed part of item (3): the claim now
checks the adapter runtime and the guard's registrations before it launches
(IR-4), but it does not provision the level record for the actual logical
session (the guard binds it on the session's first prompt) and it does not
check the L2 layer beyond presence.

## Follow-up scope

A separate plan is required. It covers design sections 19.2, 19.3, 19.4 and
19.5:

- 19.2 (placement and coexistence): one owned, shared `hooks/pre-push` file,
  installed only when no foreign pre-push exists and the default hooks lookup
  is in effect; no change to the user's git configuration (no `core.hooksPath`
  migration) and no forwarding of other hooks; ownership is the exact owned
  version and content, never a header alone.
- 19.3 (update stream and limits): for a positively selected governed process,
  refuse the entire push when field 3 of any record is exactly
  `refs/heads/main` or `refs/heads/master`; `--no-verify`, direct send-pack
  and API writes can bypass a local pre-push hook, and only the visible
  command forms stay checked by the L1 text layer.
- 19.4 (release and removal): human pushes in the same worktree stay
  unrestricted, and a retained worktree marker must not restrict them after
  release; the shared hook may stay installed and inert.
- 19.5 (tests): real git on a temporary bare remote, a clone and linked
  worktrees, asserting the remote refs before and after, not only the exit
  status.

Open items for that plan: U28 (the verified install place for the shared
`hooks/pre-push` file) and the OB-H3 L2 observation (real governed process
trees and a same-worktree human terminal at the same time). The design files
that 19.2, 19.4 and 19.5 cite as evidence are absent from this tree (listed in
`./artifacts/b-ctx-verdict.md`, section F7; section 19.3 cites none of them),
so the decisions in 19.2, 19.4 and 19.5 are unverified until that plan
re-derives them.

## When the L2 plan ships

Turn the `W-L2-ABSENT` warning into a refusal in `cmd_launch`; the one-line
change is in `./artifacts/ir7-consequence.md`.

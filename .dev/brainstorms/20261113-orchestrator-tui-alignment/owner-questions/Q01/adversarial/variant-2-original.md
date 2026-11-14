# Proposal B: fix before merge, by neutralising or by refusing, and cover every channel

## Answer

(a) Fix the hole inside PR #539 before it merges, by either outcome: neutralise every repo-configured program so `git status` cannot start one (F1), or refuse to scan a worktree whose config could start one and report it as `unscanned` (F2); the #539 author and the owner pick which. (b) Yes: the ruling covers `filter.<driver>.process`, config pulled in by `include.path`/`includeIf`, per-worktree config and inherited `GIT_*`/`GIT_CONFIG_*` variables, and names any channel it deliberately leaves out.

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01), stating that the allow-list edit (NFR-014, `ALLOWED_GIT`) is authorised for this purpose only, and listing the channels in scope.
2. The #539 author implements it (SW-02) with a regression test that reproduces the 2026-11-13 probe experiment and fails if any in-scope channel runs a program (or, for refusing, if such a worktree is scanned instead of reported `unscanned`). The test names every golden test it changes; no JSON key or sidecar file is added.
3. The git-status scope is separated from the contract allow-list and transcript scans so a contract in another repository's worktree is not misreported (INV-039).
4. The push gives a new merge reference; #539 merges after CI and both threads clear (SW-05).

## What it unlocks

- The sweep's "read-only" and "changes nothing" claims become true as written, so none of the 16-plus statements needs a caveat (INV-011).
- The one real-id comparison (XC-04) can run on master code as soon as the sweep is runnable, because the master sweep is the fixed sweep.
- The Codex security thread closes on a real fix rather than an acceptance, which is reversible (SW-01 row: "a fix choice, yes").

## What it costs or risks

- It is an allow-list and test change, not a one-liner: an exact one-entry allow-list under owner signature and three pinned tests change (INV-009), plus the path-scope separation (INV-039). This lengthens the #539 lane and everything queued behind its merge.
- The ruling must enumerate channels; a channel nobody listed (for example a future git feature) could still run. The "names any channel it leaves out" clause makes that visible, not impossible.
- The neutralise route depends on git honouring every override; the refuse route makes some worktrees show as `unscanned`, which is less information for the coordinator.

## What stays unresolved

- Which of the two fix outcomes is chosen and the code itself (owned by the #539 author and the owner; this program never specifies it).
- Whether git versions other than 2.47.3 behave the same.

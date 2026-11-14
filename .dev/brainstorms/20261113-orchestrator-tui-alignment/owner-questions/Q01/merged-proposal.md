<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

# Proposal B: fix before merge, by neutralising or by refusing, and cover every channel

<!-- Source: Base (original, modified), debate consensus on A-001 merged per Change #2 -->
## Answer

(a) Fix the hole inside PR #539 before it merges, by either outcome: neutralise every repo-configured program so `git status` cannot start one (F1), or refuse to scan a worktree whose config could start one and report it as `unscanned` (F2); the #539 author and the owner pick which. (b) Yes: the ruling covers `filter.<driver>.process`, config pulled in by `include.path`/`includeIf`, per-worktree config and inherited `GIT_*`/`GIT_CONFIG_*` variables, and names any channel it deliberately leaves out. The ruling states its scope by outcome (no program named by config or by the environment runs during the sweep's `git status`, or the worktree is reported `unscanned`), and treats the channels above as the measured minimum, not a complete list (`merged-requirements.md:36`).

<!-- Source: Base (original, modified), Variant 3 merged per Change #1 -->
## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01), stating the premise it relies on, as SW-01 (2) requires (`merged-requirements.md:190`): the worst-case lens of `SECURITY.md:168-170` (configuration is assessed at its worst case, and agent coordination is checked for escalation). The ruling names the counterweight, that every session launched on this host already runs with permission checks off (ADJ E-11), and does not rely on it. The ruling also states that the allow-list edit (NFR-014, `ALLOWED_GIT`) is authorised for this purpose only, and lists the channels in scope.
2. The #539 author implements it (SW-02) with a regression test that reproduces the 2026-11-13 probe experiment and fails if any in-scope channel runs a program (or, for refusing, if such a worktree is scanned instead of reported `unscanned`). The test names every golden test it changes; no JSON key or sidecar file is added.
3. The git-status scope is separated from the contract allow-list and transcript scans so a contract in another repository's worktree is not misreported (INV-039).
4. The push gives a new merge reference; #539 merges after CI and both threads clear (SW-05).

<!-- Source: Base (original, modified), CONTRADICTION-1 from the debate transcript merged per Change #5 -->
## What it unlocks

- The sweep's "read-only" and "changes nothing" claims become true as written, so none of the 16-plus statements needs a caveat (INV-011).
- The one real-id comparison (XC-04) can run on master code as soon as the sweep is runnable, because the master sweep is the fixed sweep. This advantage over an acceptance is certain only under the strict reading of the XC-04 rule ("never the unfixed sweep", `merged-requirements.md:452` and `:889`); `merged-requirements.md:630` (TB-GIT) would also let a recorded acceptance satisfy the git trust boundary. The sources conflict on this point and it is not resolved here.
- The Codex security thread closes on a real fix rather than an acceptance, which is reversible (SW-01 row: "a fix choice, yes").

<!-- Source: Base (original, modified), Variant 1 merged per Change #4 -->
## What it costs or risks

- It is an allow-list and test change, not a one-liner: an exact one-entry allow-list under owner signature and three pinned tests change (INV-009), plus the path-scope separation (INV-039). This lengthens the #539 lane and everything queued behind its merge. To keep it reviewable, the fix goes in as its own push with its own description, because #539 is a 1003-file PR.
- The ruling must enumerate channels; a channel nobody listed (for example a future git feature) could still run. The "names any channel it leaves out" clause makes that visible, not impossible.
- The neutralise route depends on git honouring every override; the refuse route makes some worktrees show as `unscanned`, which is less information for the coordinator.

<!-- Source: Base (original, modified), Variant 1 merged per Change #3 -->
## What stays unresolved

- Which of the two fix outcomes is chosen and the code itself (owned by the #539 author and the owner; this program never specifies it).
- Whether git versions other than 2.47.3 behave the same.
- What the fix removes and what it does not. It removes the sweep's added exposure, which is the widest automatic one: fan-out across every listed worktree on every coordinator wake (`HOW-WE-WORK.md:406`). It does not cover other sessions on this host that run `git status` themselves (for example the git status the Claude Code harness reports at session start); whether those honour the same config is UNVERIFIED.

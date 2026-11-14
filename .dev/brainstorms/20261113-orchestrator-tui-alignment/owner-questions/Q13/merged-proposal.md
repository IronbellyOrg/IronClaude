<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: yes, with the limit stated and a re-ask trigger

<!-- Source: Base (original, modified) - Change 1 -->
## Answer

Yes. The observer may fall back to a bare `orca` because it accepts a candidate only after `skills list --json` shows the `orca-cli` topic; that proves the program is Orca (not the GNOME screen reader), not that it is the same Orca the sweep reads. The contract note records both rules, this acceptance and its limit; no code changes.

<!-- Source: Base (original, modified) - Change 3 -->
## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- The contract note draft (work item XC-05, `docs/designs/observe-sweep-contract.md`) carries one binary-resolution row: observer and watcher use `_find_orca` (`orca-ide` then `orca`, each proven by `skills list --json`, `install_user_setup.py:247-270`); the sweep uses `$ORCA_CLI_COMMAND` else `orca-ide`, no probe (`probes.py:201-202`); the observer ignores `ORCA_CLI_COMMAND`.
- The note records the Orca build string next to each capture (ADJ line 233). The owner is asked again if recorded build strings differ, if `ORCA_CLI_COMMAND` is in use on the host, or if the dispatch-id comparison (XC-04) is judged to need one binary. (Change 3)
- Neither program's code changes; PR #539 is untouched.

<!-- Source: Base (original) -->
## What it unlocks

- The note states a verdict and a reason instead of two unexplained rules.
- The observer keeps working where `orca` is the Orca CLI shim.
- The screen-reader guard stays.

<!-- Source: Base (original, modified) - Changes 1, 2 -->
## What it costs or risks

- The two programs read different binaries only when `ORCA_CLI_COMMAND` is set, or when `orca-ide` is missing or fails its probe; in the last case the observer falls back to `orca` without any log (`install_user_setup.py:257-267`). On this host the variable is unset and both programs read `orca-ide`. (Change 2)
- The probe runs whatever is first on PATH under each name, once, with a 10-second timeout.
- Two rules stay in the codebase.

<!-- Source: Base (original, modified) - Change 4 -->
## What stays unresolved

- Whether both names reach the same Orca build where both exist (A-009).
- Two follow-up rows, logged only (no code change authorized by this answer): the observer's lookup accepts a relative `which` result, while the watcher skips one (`issue_watch/launch.py:178-196`); and the observer's silent fallback after a failed `orca-ide` probe. (Change 4)

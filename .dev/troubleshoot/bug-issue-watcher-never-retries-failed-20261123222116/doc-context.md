# Documentation Context Card (inline; the three-branch fan-out was not run, see REPORT Grounding Gaps)
## Release context
.dev/releases/backlog/issue-watcher-zero-setup/requirements.md: R7 (line 38) first-time checks run automatically for a new project; R18 (line 44) a failed first-run check leaves that repo `enabled: false` and reports why; R28 (line 54) first run includes lock and restart tests.
## Architectural docs consulted
first_run.py module docstring (lines 1-26): "idempotent: a repository whose config is already enabled is left alone".
## Restrictions / decisions that constrain the fix
- R18 says a failed check leaves enabled:false and reports why; it does not say the failure is permanent. Retrying does not contradict it.
- dispatch.py docstring line 66: `not_enabled` = "the first run did not pass, or the owner set it". The code cannot tell the two apart today.
- dispatch.py:361-363: a dry run only reads (no generation, no writes).
## Re-frame signals
- Docs do not state that a failed first run is final, so this is a code gap, not documented behaviour.

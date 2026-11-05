# Documentation Context Card

## Release context
No release slug. Controlling artifact: design package TASK-WF-design-20261104-164423 (source.md section 7.3, :826-844). The design promises "Whole run under 60 s (`timeout` per command when available)" (:841) and requires --out to be missing or empty (:835), while resume rows 5 and 7 restart under the same cycle_id (:295, :379, :381) and keep resolution.md (:1230). Both findings are design gaps the script follows (wave1_5-branch-A.md).

## Architectural docs consulted
- scripts/collect-conflict-evidence.sh:12-13, :25-26, :72-73 (CAUTION: currency unknown)
- refs/conflict-intent.md:19, :30, :71, :95, :99 (CAUTION: currency unknown)
- refs/conflict-mechanical.md:71, :97, :103, :247, :249, :252 (CAUTION: currency unknown)
- .dev/tasks/done/TASK-WF-design-20261104-164423/source.md:835, :841, :1224; plan :212 (CAUTION: currency unknown)
No doc defines a per-attempt directory or clears the evidence directory on restart; conflict-intent.md:95 keeps it after an abort.

## Restrictions / decisions that constrain the fix
- Static bans over the whole script, comments included: push, stash, force, git config/checkout/switch/reset/commit/add/rm/worktree/rebase/merge, gh, --no-verify, --amend, src/superclaude (test_conflict_scripts.py:1413-1424).
- Exactly one stdout line; no temp dir left; no change to status/HEAD/index (test_conflict_scripts.py:1180, :1185-1187, :1193).
- Fenced ref commands start with git/gh/uv/make/jq or scripts/ (test_conflict_sync_protocol.py:40, :514-538); only conflict-intent.md names the collector (:357-370).
- test_conflict_e2e.py hard-codes `sync/<cycle_id>/<n>`, message.txt, manifest.txt and resolution.md under `sync/<cycle_id>/` (:288-290, :610, :845-847, :888, :997, :1020).

## Re-frame signals
- A2 is a missing fallback, not a wrong constant: the budget exists but is enforced only between commands when `timeout` is absent.
- C1 is a layout collision between the "empty --out" rule and the "restart under the same cycle_id" rule; the cycle id must stay, so the attempt must be part of the path.

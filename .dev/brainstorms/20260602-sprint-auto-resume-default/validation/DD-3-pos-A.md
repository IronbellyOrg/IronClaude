# Position A — DD-3 as written: preserve-rename quarantine reusing recovery.py:445-492

**Claim:** The gate quarantines half-written next-task artifacts by reusing the recovery
engine's `.failed-<ts>` rename pattern (recovery.py:445-492), recording them in an
`artifacts_replaced` map and a `recovery-audit.log` line (`resume_quarantine`).
Restorable, mirrors `rerun-tasks --restore`. Non-destructive (move, not delete). A future
`sprint resume --restore` reverses it.

## Strengths
- Move-not-delete is genuinely non-destructive; the original bytes survive on disk.
- `.failed-<ts>` naming is already a convention operators see in rerun-tasks merges, so it
  is familiar and greppable.
- `write_recovery_audit_log` (recovery.py:250) is a real, reusable, append-only helper —
  the audit-log half of the claim is sound and reusable as-is.
- Timestamp suffix avoids collisions across repeated quarantines.

## Weaknesses (conceded)
- The rename code at 445-492 is **inlined three times inside `merge_recovery_bundle`**,
  not a standalone function. There is nothing importable to "reuse" — it requires
  extraction into a helper before the gate can call it.
- The `artifacts_replaced` map lives on a **RecoveryBundle** object that only
  `merge_recovery_bundle` constructs. The gate is not running a bundle merge, so it has no
  bundle to record into unless one is fabricated or a new persistence path is added.
- `rerun-tasks --restore` does **not** reverse `.failed-<ts>` renames. It calls
  `restore_from_bundle` (rerun_tasks.py:1039) which copies files back from
  `<bundle_dir>/preserved/` — a COPY-stash created by `stash_and_restore_deliverables`
  (rerun_tasks.py:961). The `.failed-<ts>` renames in merge step 1-3 are never restored by
  any existing code path. So "mirrors rerun-tasks --restore" is false at the mechanism level.
- `sprint resume --restore` does not exist (no `resume` subcommand in commands.py). The
  non-destructive guarantee leans on a command that is vaporware.

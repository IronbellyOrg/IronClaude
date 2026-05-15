# Backup / Workaround — If S1+S2+S5 Still Don't Unblock the Pipeline

This is the **escape valve** to keep the release moving while a real fix is being
investigated. Use it only after the top-3 fixes have been merged and verified
to compile/test-pass, AND `superclaude roadmap run … --resume` still fails at
`spec-fidelity`.

## Quick-Path: Force-Progress

```bash
# Re-run with regeneration override and extra runs
superclaude roadmap run \
  /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md \
  --resume \
  --allow-regeneration
```

`--allow-regeneration` (already implemented in `commands.py:90`) lets remediation
agents exceed the 30% diff threshold. Combined with the top-3 fixes, this gives
the agent maximum freedom to converge. Note: there is no `--max-runs` flag
currently — `max_runs=3` is hard-coded in `convergence.execute_fidelity_with_convergence`.
If 3 runs is the binding constraint, see "Bump max_runs" below.

## Workaround Option 2: Bump max_runs (1-line edit)

If 3 runs really is too few:
1. Edit `src/superclaude/cli/roadmap/convergence.py`, function `execute_fidelity_with_convergence`,
   change parameter `max_runs: int = 3` to `max_runs: int = 5`.
2. Run `make sync-dev` if anything was sync'd (this file is in `src/` so the install path picks it up directly via `pipx install`).
3. Re-run the CLI command above.

This is **not** a fix — it just buys more attempts. Revert before merging anything.

## Workaround Option 3: Manually clear the registry and start fresh

If the deviation registry has accumulated stale findings from prior runs:

```bash
# Back up first
cp /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json{,.bak}

# Then delete it so the next run starts fresh
rm /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json

# Re-run
superclaude roadmap run \
  /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md \
  --resume \
  --allow-regeneration
```

Useful when the registry has accumulated phantoms from pre-S1 runs that the
spec-hash check failed to invalidate.

## Workaround Option 4: Bypass and proceed to tasklist generation

If you need to move on to the next phase **right now** and accept that the
spec-fidelity gate produced an imperfect roadmap:

1. Manually edit `roadmap/spec-fidelity.md` to set:
   ```
   validation_complete: true
   tasklist_ready: true
   ```
2. Inspect `deviation-registry.json` and document the remaining HIGHs in the
   release notes as "known deviations — to be triaged in a follow-up release."
3. Proceed to `superclaude tasklist generate` as if spec-fidelity had passed.

This is the **last-resort manual override**. It should be paired with a
follow-up task to actually fix the underlying issues. Don't ship a release that
relies on this without an explicit deviation note in the release notes.

## Last Resort: Roll Back the Top-3 Changes

If S1/S2/S5 introduced a new regression:

```bash
git log feat/roadmap-spec-fidelity-fix --oneline
git revert <s5-commit>
git revert <s2-commit>
git revert <s1-commit>
# Or, if you committed in order: git reset --hard <pre-s1-commit>
make test
```

Then escalate: file a release-blocker ticket, capture the failing
`deviation-registry.json` and `spec-fidelity.md` outputs, and run
`sc:adversarial` again with the new data to discover what the top-3 fix
missed.

## Diagnostic Commands

If you need to inspect what changed between runs:

```bash
# Compare registries
diff -u registry.bak registry.json | less

# See the actual findings
jq '.findings | to_entries | map(select(.value.status == "ACTIVE"))' \
  /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json

# Check which files agents tried to edit
ls /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/*.pre-remediate 2>/dev/null
```

`*.pre-remediate` files are snapshots the remediation executor creates before
agents edit — their presence means the agent was given that file as a target.
After S2, you should see `roadmap.md.pre-remediate` exist, not
`TDD_TASK_BUILDER_CONVERGENCE.md.pre-remediate`.

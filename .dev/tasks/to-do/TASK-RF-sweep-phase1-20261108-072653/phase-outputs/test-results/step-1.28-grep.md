# Step 1.28 primitive-path grep (item 14.5)

Run 2026-11-12. Base commit: `5dc29d23b15eb7db4ead50623bb409f696a0d7d3` (item 1.3), the same as the `5dc29d23` the plan names.

## Check 1: scoped grep over the new and edited primitives

Command: `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/ src/superclaude/core/WORKER-CONTRACT.md src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md; echo "exit=$?"`
```text
exit=1
```
Check 1: PASS (no output, exit=1, 0 hits)

## Check 2: full-tree count

Command: `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks | wc -l`
```text
168
```

Note: with standard error shown, `grep -r` also prints six `binary file matches` notices to standard error for gitignored compiled caches (`__pycache__/*.pyc` under `sc-issue-protocol/scripts/`, `sc-implement-protocol/scripts/` and `ccsession-tag/`; `.gitignore:2` ignores `__pycache__/`) built by running tests. They are not text hits and are not in the pipe, so the count above is the text-hit count.

Count at the base commit (read only): `git grep -n 'src/superclaude' $(cat .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/base-commit.txt) -- src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks | wc -l`
```text
168
```

Check 2: PASS (the full-tree count is 168 now and 168 at the base, unchanged)

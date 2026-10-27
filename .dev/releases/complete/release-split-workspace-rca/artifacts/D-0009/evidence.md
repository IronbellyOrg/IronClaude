# D-0009 — Verification Evidence

**Date:** 2026-05-13
**Task:** T03.03
**Working directory:** `/config/workspace/IronClaude`

## Diff Applied to `Makefile`

Three hunks:

1. `.PHONY` list — added `eval-skill`:

```diff
-.PHONY: install test test-plugin doctor verify clean lint format build-plugin sync-plugin-repo sync-dev verify-sync lint-architecture uninstall-legacy help
+.PHONY: install test test-plugin doctor verify clean lint format build-plugin sync-plugin-repo sync-dev verify-sync lint-architecture eval-skill uninstall-legacy help
```

2. New target inserted before `help:`:

```makefile
# Create a skill eval workspace under .dev/eval-workspaces/<SKILL>/ and print its absolute path.
# Usage: make eval-skill SKILL=<name>
eval-skill:
	@if [ -z "$(SKILL)" ]; then \
		echo "❌ Error: SKILL is unset. Usage: make eval-skill SKILL=<name>" >&2; \
		exit 1; \
	fi
	@mkdir -p .dev/eval-workspaces/$(SKILL)
	@realpath .dev/eval-workspaces/$(SKILL)
```

3. `help` block — added one line under "🔄 Component Sync":

```diff
 	@echo "  make lint-architecture - Enforce architecture policy (6 of 10 checks)"
+	@echo "  make eval-skill SKILL=<name> - Create .dev/eval-workspaces/<name>/ and print absolute path"
```

## Probe 1 — Positive case (SKILL=__probe__)

Command:
```
make eval-skill SKILL=__probe__
```

stdout:
```
/config/workspace/IronClaude/.dev/eval-workspaces/__probe__
```

Exit status: `0`

Filesystem check:
```
$ ls -d .dev/eval-workspaces/__probe__/
.dev/eval-workspaces/__probe__/
```

Result: ✅ Directory created at the documented path; absolute path printed on stdout as the sole output line.

## Probe 2 — Idempotency (re-run SKILL=__probe__)

Command:
```
make eval-skill SKILL=__probe__   # second invocation
```

stdout:
```
/config/workspace/IronClaude/.dev/eval-workspaces/__probe__
```

Exit status: `0`

Result: ✅ Re-run succeeds, prints the same absolute path, no `mkdir: cannot create directory` or similar error.

## Probe 3 — Unset SKILL

Command:
```
make eval-skill
```

stderr:
```
❌ Error: SKILL is unset. Usage: make eval-skill SKILL=<name>
make: *** [Makefile:371: eval-skill] Error 1
```

Exit status: `2` (make's exit code when a recipe exits non-zero; the recipe itself called `exit 1`)

Result: ✅ Non-zero exit, clear error message naming the missing variable and showing the correct usage.

## Cleanup

```
$ rmdir .dev/eval-workspaces/__probe__
$ ls .dev/eval-workspaces/
sc-release-split-protocol
```

Probe directory removed; pre-existing `sc-release-split-protocol/` workspace untouched.

## Raw Combined Session

```
=== Test 1: success case ===
/config/workspace/IronClaude/.dev/eval-workspaces/__probe__
exit=0

=== Test 2: idempotent re-run ===
/config/workspace/IronClaude/.dev/eval-workspaces/__probe__
exit=0

=== Test 3: unset SKILL (expect non-zero) ===
❌ Error: SKILL is unset. Usage: make eval-skill SKILL=<name>
make: *** [Makefile:371: eval-skill] Error 1
exit=2

=== Cleanup probe dir ===
sc-release-split-protocol
```

## Acceptance Criteria Verification Matrix

| AC | Status | Evidence |
|---|---|---|
| `make eval-skill SKILL=__probe__` creates `.dev/eval-workspaces/__probe__/` and prints absolute path; exit 0 | ✅ | Probe 1 |
| `make eval-skill` exits non-zero with clear error | ✅ | Probe 3 (exit 2, message includes "SKILL is unset" and usage hint) |
| Target is idempotent | ✅ | Probe 2 (re-run, no error) |
| Both outputs captured in `D-0009/evidence.md` | ✅ | This file |

All four acceptance criteria met. T03.03 complete.

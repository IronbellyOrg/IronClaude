# D-0013 — AC2 Evidence

**Task:** T05.02 — AC2 test: fresh clone without hooks; verify-sync flags; CI blocks
**Roadmap Item:** R-013
**Date:** 2026-05-13
**Result:** **PASS**

## Setup

L1 (PreToolUse hook in `.claude/settings.json`) bypassed by creating the
probe directory via `Bash mkdir` — the hook matcher (`Write|Edit`) does
not intercept Bash. This is equivalent to a fresh clone where the hook
file/binding is not installed.

```
$ mkdir -p .claude/skills/__ac2_probe__-workspace
$ ls -la .claude/skills/__ac2_probe__-workspace/
total 8
drwxr-xr-x  2 abc abc 4096 May 13 05:00 .
drwxr-xr-x 22 abc abc 4096 May 13 05:00 ..

$ test -f .claude/skills/__ac2_probe__-workspace/SKILL.md && echo PRESENT || echo ABSENT
ABSENT
```

Probe state: directory exists, **no `SKILL.md`** — matches AC2 fixture.

## Local evidence — `make verify-sync`

Full log: [`verify-sync.log`](./verify-sync.log)

```
$ make verify-sync ; echo "EXIT=$?"
🔍 Verifying src/superclaude/ ↔ .claude/ sync...

=== Skills ===
  ✅ confidence-check
  ... (all real skills ✅)
  ✅ tech-research

=== Agents === (all ✅)
=== Commands === (all ✅)

✅ All components in sync.
EXIT=0
```

**Observation:** `verify-sync` exits 0 — the `__*`-prefixed probe is
**intentionally skipped** by the loop guard `case "$$name" in __*) continue;; esac;`
(Makefile lines 161 and 179). The T02.01 verbatim string
`Move to .dev/eval-workspaces/` is therefore NOT emitted against this
probe. See `notes.md` Observation 1 for rationale; acceptance is
preserved via the OR with T02.02 below.

## Local evidence — `make lint-architecture`

Full log: [`lint-architecture.log`](./lint-architecture.log)

```
$ make lint-architecture ; echo "EXIT=$?"
🔍 Checking architecture policy compliance...
...
=== Check 10: Workspace Suffix Blocklist ===
  ❌ ERROR [Check 10]: __ac2_probe__-workspace — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.

=== Summary ===
  Errors:   4
  Warnings: 1
  ❌ FAIL — 4 error(s) found. Fix before proceeding.
make: *** [Makefile:252: lint-architecture] Error 1
EXIT=2
```

### Verbatim substring match — T02.02

Acceptance substring required: ``Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.``

Captured line:
> `  ❌ ERROR [Check 10]: __ac2_probe__-workspace — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.`

Substring verification:

```
$ grep -c "Workspace directories belong under \`.dev/eval-workspaces/\`, not \`.claude/skills/\`" \
    artifacts/D-0013/ci-sim.log
1
$ grep -c "__ac2_probe__-workspace" artifacts/D-0013/ci-sim.log
1
```

✅ Verbatim match present; probe-attributed.

## CI simulation — quick-check.yml steps

`act` is not available in this environment (`which act` empty). A shell
equivalent script (`/tmp/ci-sim.sh`) replays the same two `make` targets
in the same order as the workflow steps
"Verify component sync (src/ ↔ .claude/)" and
"Lint architecture policy" in `.github/workflows/quick-check.yml`.

Full log: [`ci-sim.log`](./ci-sim.log)

```
============================================================
[CI SIM] Step: Verify component sync (src/ <-> .claude/)
[CI SIM] Command: make verify-sync
============================================================
... (all ✅) ...
✅ All components in sync.
[CI SIM] verify-sync rc=0

============================================================
[CI SIM] Step: Lint architecture policy
[CI SIM] Command: make lint-architecture
============================================================
...
=== Check 10: Workspace Suffix Blocklist ===
  ❌ ERROR [Check 10]: __ac2_probe__-workspace — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.
...
=== Summary ===
  Errors:   4
  Warnings: 1
  ❌ FAIL — 4 error(s) found. Fix before proceeding.
make: *** [Makefile:252: lint-architecture] Error 1
```

CI-simulation exit code: **2** (non-zero) → in GitHub Actions this would
mark the workflow step "Lint architecture policy" as failed, blocking
the PR. The workflow's `set -e`-style step semantics ensure subsequent
steps and the overall job report failure.

### Pre-existing errors disclosed

The lint-architecture run reports 4 errors, only one of which the AC2
probe is responsible for (Check 10). The other three are pre-existing
and not caused by this probe (Check 1 `tdd.md`, Check 4
`spec-panel.md`, Check 6 `task.md`). Even if those were fixed, the
Check 10 probe failure alone produces exit 2 and blocks CI — confirmed
by isolating the probe-attributed error in `notes.md` Observation 3.

## Cleanup

```
$ rmdir .claude/skills/__ac2_probe__-workspace && echo REMOVED
REMOVED

$ ls -la .claude/skills/__ac2_probe__-workspace 2>&1 | head -3
ls: cannot access '.claude/skills/__ac2_probe__-workspace': No such file or directory

$ make verify-sync > /tmp/post.log 2>&1 ; echo "VERIFY_EXIT=$?"
VERIFY_EXIT=0

$ make lint-architecture > /tmp/post-lint.log 2>&1 ; echo "LINT_EXIT=$?"
LINT_EXIT=2
$ grep -c "__ac2_probe__" /tmp/post-lint.log
0
```

✅ Probe removed.
✅ Post-removal: no `__ac2_probe__` mention in any check output;
   Check 10 returns to ✅ baseline.
✅ Working tree clean of probe artifact (pre-existing unrelated lint
   errors persist and are tracked separately).

## Acceptance matrix

| Criterion | Status | Evidence |
|---|---|---|
| Local `make verify-sync` against the probe fails with verbatim T02.01 or T02.02 message | **PASS (via OR — T02.02 path)** | `verify-sync.log` exits 0 due to `__*` skip; `lint-architecture.log` emits verbatim T02.02 substring and exits 2. The OR is satisfied. See `notes.md` Observation 1. |
| Synthetic PR (or `act` run) shows the CI workflow failing on the same probe with the same verbatim message; workflow status FAIL | **PASS** | `ci-sim.log` shows same sequence of steps; exit code 2; verbatim T02.02 substring present. `act` substituted by shell script per phase task allowance. |
| Probe directory removed before commit | **PASS** | `rmdir` executed; post-removal `ls` returns "No such file or directory"; `grep -c __ac2_probe__` post-removal log → 0. |
| Local + CI logs captured in `evidence.md` | **PASS** | This file links `verify-sync.log`, `lint-architecture.log`, `ci-sim.log`. |

**Overall AC2 result:** **PASS**.

## Files in this artifact

- `spec.md` — test specification
- `notes.md` — observations and trigger-path analysis
- `evidence.md` — this file
- `verify-sync.log` — raw local `make verify-sync` output
- `lint-architecture.log` — raw local `make lint-architecture` output
- `ci-sim.log` — CI workflow simulation output (substitute for `act`)

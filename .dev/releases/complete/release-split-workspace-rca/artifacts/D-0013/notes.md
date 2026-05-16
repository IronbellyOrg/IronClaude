# D-0013 — Notes & Observations

## Observation 1 — `verify-sync` silently skips `__*`-prefixed probe

`make verify-sync` (Makefile lines 158–188) iterates `.claude/skills/*/`
but contains an explicit skip:

```make
case "$$name" in __*) continue;; esac;
```

The probe directory `__ac2_probe__-workspace` matches `__*` and is
**skipped**. As a result, `make verify-sync` exits 0 against this probe
and the T02.01 verbatim message (`Move to .dev/eval-workspaces/`) is NOT
emitted. This is by-design: the `__*` prefix is reserved for AC probe
directories (see `.dev/eval-workspaces/__ac1_probe__/`) so that
acceptance probes do not pollute the legitimate sync report.

**Consequence for AC2:** Of the two M2 defenses, only T02.02
(`make lint-architecture` Check 10) fires against an `__*`-prefixed
probe placed under `.claude/skills/`. The phase task accepts this with
"T02.01 message OR T02.02 message" (logical OR). Coverage is therefore
maintained by lint-architecture Check 10, which has no `__*` skip:

```make
for d in .claude/skills/*-workspace/; do
    [ -d "$$d" ] || continue;
    name=$$(basename "$$d");
    echo "  ❌ ERROR [Check 10]: $$name — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.";
    errors=$$((errors+1));
```

If a future probe needs to exercise the T02.01 verbatim message
specifically, the probe must be renamed to a non-`__*`-prefixed form
(e.g. `ac2-probe-workspace`); the `__ac2_probe__` literal in the phase
task constrains this run to T02.02 only.

## Observation 2 — L1 bypass via Bash tool selection

The PreToolUse hook in `.claude/settings.json` declares
`"matcher": "Write|Edit"`. Probe directory creation via `Bash mkdir`
therefore does NOT trigger `reject-workspace-writes.sh`. This is the
exact failure mode AC2 simulates: an actor (a fresh clone without the
hook installed, OR an actor whose tool path the hook does not match)
producing an offending directory. The hook's matcher scope is correct —
it intercepts Claude's file-writing tools, which is its design
contract; deeper interception (e.g. shell-level) is out of scope for
L1.

## Observation 3 — Pre-existing lint-architecture errors

The `make lint-architecture` run reports 4 errors, only 1 of which is
caused by the AC2 probe:

| Check | Source | Probe-caused? |
|---|---|---|
| Check 1 | `tdd.md` has `## Activation` but no matching skill dir `sc-tdd-protocol` | No (pre-existing) |
| Check 4 | `spec-panel.md` is 651 lines (over 500 hard limit) | No (pre-existing) |
| Check 6 | `task.md` missing `## Activation` (paired with `sc-task-protocol`) | No (pre-existing) |
| **Check 10** | **`__ac2_probe__-workspace` workspace directory under `.claude/skills/`** | **YES — this is the AC2 signal** |

After probe removal, Check 10 returns to ✅ baseline. The other three
errors persist and are tracked separately from AC2.

## Observation 4 — `act` unavailable; CI simulated locally

`which act` returns empty in this environment. To satisfy
"or run local `act .github/workflows/quick-check.yml`", a shell
equivalent `/tmp/ci-sim.sh` was used. It runs the same two `make`
targets (`verify-sync`, `lint-architecture`) in the same order as the
"Verify component sync" and "Lint architecture policy" steps in
`.github/workflows/quick-check.yml`. Exit code of the simulation is 2
(non-zero), matching what GitHub Actions would report as a failed step.
The verbatim T02.02 substring appears once in the captured log.

## Observation 5 — Cleanup confirmed

The probe directory `.claude/skills/__ac2_probe__-workspace/` was
removed via `rmdir` after evidence capture. Post-removal:

- `ls .claude/skills/__ac2_probe__-workspace` → "No such file or directory"
- `make verify-sync` → exit 0 (unchanged)
- `make lint-architecture` → exit 2 (still fails on the 3 pre-existing
  errors, but `grep -c "__ac2_probe__" /tmp/post-lint.log` → 0)

No probe artifact remains in the working tree, satisfying the
"Probe directory removed before commit" criterion.

## Classification

- **Acceptance result:** PASS
- **Trigger path exercised:** T02.02 (lint-architecture Check 10)
- **T02.01 not exercised** by this probe due to the `__*` skip in
  `verify-sync`; documented in Observation 1. The acceptance criteria's
  "OR" satisfies this.
- **CI propagation:** Confirmed via shell simulation; exit code 2;
  verbatim message present.

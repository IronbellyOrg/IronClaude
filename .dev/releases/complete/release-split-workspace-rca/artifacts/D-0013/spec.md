# D-0013 — AC2 Acceptance Test Specification

**Task:** T05.02 — AC2 test: fresh clone without hooks; verify-sync flags; CI blocks
**Roadmap Item:** R-013
**Phase:** Phase 5 — Acceptance Validation
**Date executed:** 2026-05-13

## Goal

Demonstrate that with L1 (PreToolUse hook) bypassed, the L2 defenses
(`make verify-sync` and `make lint-architecture`) still catch a
`.claude/skills/<X>-workspace/` directory without `SKILL.md`, and that the
CI workflow (`.github/workflows/quick-check.yml`) propagates the failure.

## Probe definition

| Property | Value |
|---|---|
| Probe path | `.claude/skills/__ac2_probe__-workspace/` |
| Probe contents | Empty directory (no `SKILL.md`) |
| L1 bypass mechanism | Probe created via `Bash mkdir`; the PreToolUse hook in `.claude/settings.json` matches only `Write\|Edit` tool calls, so `Bash`-driven directory creation is not intercepted — functionally equivalent to a fresh clone where the hook is not installed. |
| L2 targets exercised | `make verify-sync` and `make lint-architecture` |
| CI workflow exercised | `.github/workflows/quick-check.yml` — steps "Verify component sync" and "Lint architecture policy" |

## Expected verbatim messages

The acceptance criteria allow EITHER of these substrings in CI output:

- **T02.01 (verify-sync):** `Move to .dev/eval-workspaces/`
- **T02.02 (lint-architecture, Check 10):** ``Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.``

## Acceptance criteria (per phase-5-tasklist.md)

1. Local `make verify-sync` against the probe (no `SKILL.md`) fails with verbatim T02.01 or T02.02 message.
2. Synthetic PR (or `act` run) shows the CI workflow failing on the same probe with the same verbatim message; workflow status is FAIL.
3. Probe directory removed before commit (validates no contamination).
4. Local + CI logs captured in `evidence.md`.

## Method

1. Create `.claude/skills/__ac2_probe__-workspace/` via `mkdir` (bypassing L1).
2. Run `make verify-sync`; capture stdout/stderr and exit code.
3. Run `make lint-architecture`; capture stdout/stderr and exit code.
4. Simulate CI by running the same two make targets sequentially in `ci-sim.sh` (mirroring the `quick-check.yml` step ordering). `act` is unavailable in this environment, so a shell-script equivalent is used.
5. Remove the probe directory.
6. Re-run both targets to confirm the probe-specific failure no longer occurs (Check 10 returns to the ✅ baseline; pre-existing unrelated errors persist and are not caused by this probe).

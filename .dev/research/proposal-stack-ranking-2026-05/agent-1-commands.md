# Agent 1 — Slash Commands Eval Proposals

## Proposal 1 (one-off): `task_classification_contract`

- **Target:** `/sc:task`
- **Hypothesis:** First output is exact HTML classification block, valid tier enum, no tools before classification.
- **Cadence:** one-off baseline.
- **Inputs:**
  - `/sc:task "fix security vulnerability in auth module"`
  - `/sc:task "explain how routing works"`
- **Assertions:** stdout contains `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`; `TIER: STRICT` then `TIER: EXEMPT`; exit 0.
- **Requires:** `claude`; no MCP.
- **Complexity:** simple.
- **Value:** catches high-risk regressions in mandated first-output contract.
- **Evidence:** `.claude/commands/sc/task.md:50-69`, `.claude/commands/sc/task.md:71-93`.

## Proposal 2 (one-off): `command_validation_errors`

- **Target:** `/sc:tasklist`, `/sc:cli-portify`, `/sc:auggie-review`
- **Hypothesis:** Missing/invalid inputs fail before protocol invocation.
- **Cadence:** one-off baseline.
- **Inputs:**
  - `/sc:tasklist @missing.md`
  - `/sc:cli-portify` (no args)
  - `/sc:auggie-review --snapshot missing-path`
- **Assertions:** stdout includes documented `error_code` or clear STOP; no output dirs; controlled exit.
- **Requires:** `claude`, `git`; optionally `gh/auggie` skipped.
- **Complexity:** medium.
- **Value:** catches unsafe generation/review attempts.
- **Evidence:** `.claude/commands/sc/tasklist.md:48-67`, `.claude/commands/sc/cli-portify.md:44-73`, `.claude/commands/sc/auggie-review.md:23-31`.

## Proposal 3 (recurring): `slash_command_drift_watch`

- **Targets:** all high-value slash commands.
- **Hypothesis:** Commands still invoke mandatory skills and preserve safety boundaries.
- **Cadence:** recurring — on PR touching `.claude/commands/sc/*.md` (event-triggered).
- **Inputs:** prompts invoking roadmap/adversarial/validate-roadmap/cleanup-audit dry or invalid paths.
- **Assertions:** expected Skill name appears or documented validation stop; cleanup-audit says read-only; troubleshoot without `--fix` does not edit.
- **Requires:** `claude`; no MCP for invalid-path paths.
- **Complexity:** medium.
- **Value:** catches protocol drift.
- **Evidence:** `.claude/commands/sc/roadmap.md:71-79`, `.claude/commands/sc/adversarial.md:130-136`, `.claude/commands/sc/cleanup-audit.md:86-100`, `.claude/commands/sc/troubleshoot.md:90-117`.

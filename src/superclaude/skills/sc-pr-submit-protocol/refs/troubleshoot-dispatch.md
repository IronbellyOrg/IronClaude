# Troubleshoot Dispatch (C3b) — seed verified findings to /sc:troubleshoot

This ref documents the seeding contract for dispatching **VERIFIED findings only** (those that passed
the C3a verify-before-remediate wave) to `/sc:troubleshoot`. It treats `/sc:troubleshoot` as a
**black box**: C3b constructs the invocation string + scope/issue seed; it does NOT reach inside
troubleshoot's waves or reimplement its escalation rubric. The real troubleshoot flag surface is
reused by reference (`sc-troubleshoot-protocol/SKILL.md:103`).

## The seeding contract (per verified finding)

For each verified finding, construct:

- **issue description** ← the Augment finding `body` + recommendation + evidence excerpt, so
  troubleshoot does not re-derive the symptom (FR-3.3).
- **`--scope <file:line>`** ← the finding's grounded `file:line` (T-320 asserts the dispatched
  `scope` contains the finding's file:line).
- **`--type <category>`** ← the rubric category (security / performance / tests / …), so troubleshoot
  skips its own auto-detect (`sc-troubleshoot-protocol/SKILL.md:104-111`).
- **route** ← from `severity-routing.md`'s tier→route map (FR-3.2):
  - Medium → `--fix` (which **defaults to `--depth standard`** — the safe form).
  - High / Critical → `--depth deep --fix` (`--depth deep` forces troubleshoot's own Tier-2
    escalation, `escalation-rubric.md:60-61`).
  - Low / Nit → **report-only**: troubleshoot is NOT called; the finding is recorded in the
    report-only list.

## STOP — never emit `--depth quick --fix`

`--depth quick` with `--fix` is an explicit troubleshoot conflict
(`sc-troubleshoot-protocol/SKILL.md:131`). C3b emits ONLY `--fix` (Medium) or `--depth deep --fix`
(High/Critical) — **never `--depth quick --fix`**. Do not "optimize" the Medium route to
`--depth quick`; `--fix` alone already resolves to `--depth standard`.

## Batching + run-log ordering (FR-3.4)

- **Batch findings by file/area** so multiple findings in the same file become a single troubleshoot
  dispatch (T-330: 3 findings, same file → one batch).
- **Never exceed the round budget.** If the verified findings exceed the remaining round budget,
  **truncate and HALT with a summary** (T-331) rather than opening more cycles than `max_rounds`.
- **Append the `route_decision` run-log event BEFORE invoking** troubleshoot (the write-ahead
  audit ordering, §11.3).

## The edit-application seam (load-bearing)

`/sc:troubleshoot --fix` **does NOT auto-apply edits** — `--fix` authorizes troubleshoot's Tier-3,
which deliberately stops at an MDTM task file (`/task` is always user-initiated;
`sc-troubleshoot-protocol/SKILL.md:445-448`, `refs/remediation-handoff.md:78-92`). Therefore
`sc:pr-submit` uses troubleshoot for **diagnosis** and **OWNS the edit application itself** in its own
FSM `S3_FIXING` state (spec §5.1, `state-machine.md`). The dispatch here drives diagnosis; the
working-tree edit is applied by `sc:pr-submit`, not by troubleshoot. C3b also inherits troubleshoot's
**user-gated, never-auto-execute** discipline, which dovetails with the autonomy ceiling and the
`needs_human_decision` override (FR-4.4).

# QA Fix Log: NB-4 (default argv allowlist)

**Date:** 2026-11-07
**Finding:** NB-4, `qa/qa-research-verification-qualitative-cycle1.md:42`
**Fix form applied:** first form (add the four read verbs to the `scope-03:99` default allowlist; keep `inbox` forbidden)
**Scope:** `research/scope-03-cli-patterns.md`, `gaps-and-questions.md` (row GQ-03 only), this log. No orca command run; evidence from files only.

## Edits

| # | File | Line | Before | After |
|---|------|------|--------|-------|
| 1 | `research/scope-03-cli-patterns.md` | 99 | `**Default allowlist (gate fix NB-2):** \`worker-list\`, \`worker-show\`, \`worker-read\`, \`worktree ps\` without \`--agent-wait\`; no \`check\` call at all,` | `**Default allowlist (gate fix NB-2; read verbs added by gate fix NB-4):** \`worker-list\`, \`worker-show\`, \`worker-read\`, \`worktree ps\` without \`--agent-wait\`, \`orchestration task-list\` (with \`--ready\` and \`--run <id>\`; plain read \`orchestration.taskList\`, \`07-gate-gap-fill.md\` B \`:43\`, \`task-handlers.js:32-44\`), \`orchestration run-list\` (plain read \`orchestration.runList\`, \`07\` B \`:41\`, \`run-handlers.js:35-48\`), \`orchestration run-current\` (plain read \`orchestration.runCurrent\`, \`07\` B \`:42\`, \`run-handlers.js:28-34\`) and \`orchestration gate-list\` (plain read \`orchestration.gateList\`, \`07\` B \`:44\`, \`gate-handlers.js:26-37\`); these four feed "waiting on a person" kind (b) (\`research-notes.md:197\`), the Run ids and the Owner column (\`scope-04:339\`) and the Approval candidate (\`scope-04:345\`). No \`check\` call at all,` |
| 2 | `research/scope-03-cli-patterns.md` | 99 (forbidden list) | `` `reply`, `ask`, `send`, `inbox`, `worktree ps --agent-wait` `` | `` `reply`, `ask`, `send`, `inbox` (a plain read on the CLI side, but whether it marks messages read is [UNVERIFIED], so it is not used: `07-gate-gap-fill.md:92`, `06-orca-open-questions.md` Gap 4 `:161`), `worktree ps --agent-wait` `` |
| 3 | `gaps-and-questions.md` | 26 (row GQ-03) | Status `open`; Resolution `Coordinator exception 2026-11-07: fix applied in Phase 4 synthesis (add orchestration task-list, run-list, run-current, gate-list to the scope-03:99 default allowlist; keep inbox forbidden), re-checked by the Phase 5 synthesis gate` | Status `resolved`; Resolution `fix applied 2026-11-07 by NB-4 fix pass; re-check at Phase 5 synthesis gate` |

Edit 2 note: before this pass, `scope-03` listed `inbox` as forbidden with no reason in that file (grep `inbox` in scope-03 gave one hit, in the forbidden list). Because the new allowlist cites `07` B, which also calls `inbox` a plain CLI read, the reason was copied from `07:92` and `06:161` (read and confirmed: "[UNVERIFIED] Whether `orchestration inbox` marks messages read ... Not used.") so the exclusion does not look inconsistent. `inbox` stays forbidden. The catch-all "any verb not on the allowlist" is unchanged.

Evidence for edit 1 (read from `07-gate-gap-fill.md`): `:41` `run-list` "plain read `orchestration.runList` (`run-handlers.js:35-48`)"; `:42` `run-current` "plain read `orchestration.runCurrent` (`run-handlers.js:28-34`)"; `:43` `task-list` flags include `[--ready]` and `[--run <run_id>]`, "plain read `orchestration.taskList` (`task-handlers.js:32-44`)"; `:44` `gate-list` "plain read `orchestration.gateList` (`gate-handlers.js:26-37`)". Verb form `orchestration <verb>` follows C13 (`research-notes.md:331`).

## Step 3 checks (other files citing these verbs)

Grep pattern `task-list|run-list|run-current|gate-list|allowlist` over the three files. No hit for `allowlist` in any of them, so none says a verb is outside the allowlist.

| File:line | What it says | Agrees with new allowlist? | Edited? |
|---|---|---|---|
| `research/research-notes.md:171` (Section B) | `orca-ide orchestration run-list` / `run-current`, plain `client.call`, feeds scope | Yes | No |
| `research/research-notes.md:172` (Section B) | `orca-ide orchestration task-list [--ready] [--run <id>]`, feeds kind (b) | Yes | No |
| `research/research-notes.md:173` (Section B) | `orca-ide orchestration gate-list [--run <id>]`, candidate pending-decision source | Yes | No |
| `research/research-notes.md:197` (rule 4(b)) | foreign ready Task "read from `task-list --ready`" | Yes (`task-list --ready` now allowed) | No |
| `research/05-orca-row-schema.md:175` | kind (b) source "ledger, contract, `task-list --ready`" | Yes | No |
| `research/scope-04-409-layout.md:330` | foreign ready Task (`task-list --ready`) | Yes | No |
| `research/scope-04-409-layout.md:339` | Owner: Run id (`run-list` / `worker-list --run`) | Yes | No |
| `research/scope-04-409-layout.md:345` | Approval candidate: `gate-list` gate `status`; mapping [UNVERIFIED] | Yes (verb allowed; mapping stays UNVERIFIED, GQ-34) | No |

Also seen, not edited: `05-orca-row-schema.md:194` (Gap 10) lists the same verbs and says `inbox` is not used; it agrees.

## Out-of-scope observations (not edited; files or rows outside this pass)

- `gaps-and-questions.md:125` row-count summary still says "Open: 76. Resolved: 24" and "Open blocking QA finding: GQ-03 (NB-4)". After this pass GQ-03 is resolved, so the counts are off by one. Not changed because the brief limits the edit to row GQ-03; the Phase 5 synthesis gate should update the summary line.
- `gaps-and-questions.md` GQ-34 (`:57`) and GQ-42 (`:65`) say gate-list use "depends on GQ-03" / "Allowlist follow-up is GQ-03". Still accurate as pointers; not changed.
- Minor note from cycle 1 (`scope-03:99` writes bare `worker-list` / `worker-show` / `worker-read` while C13 requires `orca-ide orchestration <verb>`) is not addressed here; the new entries use the `orchestration <verb>` form.

## Result

Edits: 3 (2 in `scope-03-cli-patterns.md:99`, 1 in `gaps-and-questions.md:26`). Step 3 files: 0 edits needed; all 8 cited lines agree with the new allowlist.

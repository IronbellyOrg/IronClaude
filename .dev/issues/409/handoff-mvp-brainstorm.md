# Handoff: MVP Brainstorm for the Orca Terminal Observer (#409)

- Task: task_f098a7b488ea, dispatch ctx_7f17d4b98864, run run_93bfa00cae2b
- Date: 2026-11-08
- Scope: design only. No code, push, PR, GitHub comment or issue edit was made.

## Output Paths

All paths are relative to the worktree root (`/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`). Brainstorm folder: `.dev/brainstorms/20261108-132433-orca-observer-mvp/`.

| File | What it holds |
|---|---|
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` | The final merged MVP specification (12 sections). Read this first. |
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/seed-brief.md` | The seed brief from the Socratic dialogue, with the enrichment summary. |
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/return-contract.yaml` | Brainstorm return contract (status success, handoff none). |
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/enrichment/` | `codebase-context.md` and `research-light.md`. |
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/adversarial/merged-output.md` | The merge-executor's output (identical copy of merged-requirements.md). |
| `.dev/brainstorms/20261108-132433-orca-observer-mvp/adversarial/adversarial/` | Debate record: 3 variants, diff analysis, invariant probe, debate rounds 1-3, convergence-r2 and r3, debate transcript, base selection, refactor plan, merge log, return-contract.yaml. |

## Recommended MVP Direction (5 lines)

1. A combination, staged by data gates; the owner selects the direction (the debate only recommends; no direction is the default yet).
2. First live release (R1): A Signal Bridge's worker ledger with the source-reported counts strip, plus B's one-line notice that question rows are not yet available (`source UNVERIFIED, 0 rows interpreted, not "no questions"`).
3. After the QUESTION-OBSERVATION gate passes: B Attention Ledger (open human questions, oldest first, "seen is not resolved"), with A's ledger one key away; labelled "bounded best effort; coverage unknown".
4. C Decision Desk only after the QUESTION-LINK gate (authoritative message-to-worker mapping); the haiku:backend advocate dissents and recommends C as the post-link view.
5. Reason: B is the only direction aimed at #409's root cause (a human question lost in recency-ordered chat), but its data source is UNVERIFIED today, so A ships first on the one verified source (`orca orchestration worker-list --json`).

## Build Order

Every data gate passes only on recorded, redacted samples of four kinds (success, missing, stale, contradictory), each pinned in a contract test (merged-requirements.md section 7).

| Step | Adds | Gate before it |
|---|---|---|
| R0 Fixture replay | Ledger screen, inspector, text export at 160/116/80 columns, sanitizer, cell-width truncation, NO_COLOR, redacted golden `worker-list` fixture, Rich Live + stdlib key-reader spike, renders of A, B and C marked "synthetic fixture, not live evidence" with degraded versions | None. Offline only. |
| DIRECTION-SELECTED (gate, ships nothing) | Owner's dated selection record | **NOT passed: no owner selection exists.** |
| R1 Live worker-list | Counts and freshness strips, worker ledger with the verbatim `nextAction.kind` column, capped paging, stale handling, "changes since last look" | DIRECTION-SELECTED, plus the owner's confirmed reading of "production integration" |
| R2 Question ledger | Open human questions with observer-side retention and the 100-row disclosure | QUESTION-OBSERVATION: the candidate read `orca orchestration check --all --run <runId> --json` needs three UNVERIFIED proofs plus a non-consumption test |
| R3 Links and decision inspector | C's Decision Desk | QUESTION-LINK (not established) |
| R4 Remote fleet | `--include-remote` rows by host | Cross-host ownership joins (not established) |
| Later | Closure evidence, history beyond 100 rows, admission, cost, deep links | Each needs a feed that is not established |

Until the owner confirms otherwise, the stricter reading of "production integration" applies: only R0 offline work may start.

## Stack Decision

Recommendation, pending owner confirmation (owner decision 2): **Python + Rich** inside this repository, as a `click` subcommand (recommended name `superclaude observe`).

- Why: the two hardest MVP requirements, plain-text export and cell-width truncation, are already in Rich (`Console(record=True)` + `export_text()`, `rich.cells.cell_len`), which is already a dependency (MIT). No new toolchain, ships with `pipx install`, and matches the house pattern in `sprint/tui.py`.
- Cost: Rich has no keyboard input, so a small POSIX stdlib key reader is new code with its own tests. If the R0 spike fails, switch to Textual 8.2.8 (MIT; maintenance risk: company wound down May 2025); never build both.
- Departs from the issue's stated Go preference (Bubble Tea v2 / Lip Gloss v2 / Bubbles v2, all MIT): Go adds a second toolchain and binary release pipeline, lacks built-in text export, its NO_COLOR parsing breaks the no-color.org rule, and teatest/v2 is untagged. Choose Go only if a separate binary is itself a goal.
- Port path kept open: one view model, two pure renderers (screen and export), so a later Go port re-implements a small, test-pinned surface.
- Ratatui 0.30.2 (pre-1.0) rejected as a third language. No code is copied from TUIBBS-scp (AGPL).
- Version and license facts come from the seed brief's research table (2026-11-08); nothing was installed or run.

## Top Open Owner Decisions

Full list of 9 in merged-requirements.md section 11. Each carries a recommendation; none is settled until the owner records it.

1. **Visual direction** (the issue requires it before production integration): a dated owner-written selection record naming the default before question rows, after QUESTION-OBSERVATION, and after linking. Recommendation: A for R1, B after QUESTION-OBSERVATION, C behind QUESTION-LINK.
2. **Stack confirmation**: Python + Rich instead of the issue's Go preference. Recommendation: Python + Rich.
3. **Production-integration boundary**: reading 1 (registering the command or any live Orca call outside the fake runner) or reading 2 (first wiring into the shipped product; authorized read-only capture counts as research). Until confirmed, the stricter offline-only reading applies.
4. **Sample capture and acquisition permission**: permission to capture one redacted non-empty sample from the candidate `check --all` read. This unblocks B's headline panel.
5. **Question type**: what makes a message a "human question" (which `type` values, which handle or Run); never inferred from free text.

Also open: command name (recommend `superclaude observe`), fallback deadline for QUESTION-OBSERVATION, message-content display and export policy, multi-observer restriction.

## Gates and Helpers Not Completed or Degraded

No helper or reviewer hung; nothing needed a re-run. The gates and degraded steps are:

- **DIRECTION-SELECTED gate: NOT passed.** No owner selection record exists. The invariant behind it (INV-019, a HIGH finding that the owner's selection had been dropped) is resolved in the design only.
- **QUESTION-OBSERVATION, QUESTION-LINK and cross-host gates: not passed.** Message row fields, inbox shape, message IDs and lease fields are UNVERIFIED; the three proofs for the candidate read are UNVERIFIED.
- **Enrichment degraded:** both codebase and research enrichment ran at the `fallback_1` tier (codegraph/Glob/Grep and web search), not the primary route.
- **Convergence caveat:** 1.00 under majority rule, 0.88 counting only 3-of-3 agreement; 7 points agreed only 2 of 3 and are recorded as dissents (merged-requirements.md section 12).
- **Invariant probe:** 2 HIGH resolved; 16 MEDIUM and 7 LOW carried as warnings, with INV-007 (oldest rows not read at the paging cap) accepted as a disclosed risk. Round 3 texts cite 14 MEDIUM (those left open after Round 2). The probe's file:line citations were not independently re-checked.
- **Merge log not re-verified line by line:** the merge agent wrote its Before/After summaries from memory plus the plan. Only the merged output's section map and the `check --all` wording were spot-checked.
- **Process deviations:** adversarial artifacts landed in a nested `adversarial/adversarial/` folder; base selection recorded its own deviations (see `base-selection.md`).
- **Known mismatch (X-001):** the design package's prototype does not show the seed brief's claim that Signal Bridge collapses at 116 columns.
- **No independent fresh-context review** of merged-requirements.md or of this handoff file was run.
- **Not done by design:** no code, push, PR, commit, GitHub comment or issue edit.

<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Feature Summary

Add an `## Unattended mode` section to `/sc:spec-panel-stoprule` (and matching rules in its protocol skill `sc-spec-panel-stoprule-protocol`) so an Orca coordinator can start a worker with `Command: /sc:spec-panel-stoprule --unattended --report-dir <D> ...` that runs the whole critique review loop (steps S0 to S10), writes `<report-dir>/return-contract.yaml`, and never needs a coordinator-or-person session at the terminal. Today the command file deliberately says it has no unattended mode and refuses `--unattended` (`~/.claude/commands/sc/spec-panel-stoprule.md`, Activation note). This is option (c) of open decision OD-1 in issue #733, chosen by the owner on 2026-11-23.

## Problem Statement

- The unattended `/sc:implement` of #733 gates its build on a `/sc:spec-panel-stoprule` report (`--plan-review`, requirement UI-24: last line `verdict: PASS`, sentinel `review=N/3` with `1 <= N <= 3`, `confirmed=0`, matching plan hash, `stoprule.py check` exit 0). But stoprule itself cannot run as a worker: it has no `## Unattended mode` section, so the brief guard in `~/.claude/WORKER-CONTRACT.md` (case 2) refuses any `Command:` line with `--unattended`, and without the flag the loop's steps must run in a coordinator or person session. The pipeline of #731/#733 therefore still needs a person (or a coordinator session doing multi-agent work) per plan review.
- Plain `/sc:spec-panel --unattended` is a worker, but its verdict is reviewer-typed and unbound to the plan hash, so implement's gate rejects it (#733, OD-1). Only the stoprule variant's script-computed verdict can gate the build.
- The loop's design assumes a coordinator session: the protocol's "Who runs which step" ruling assigns every report-writing step (`begin`, `seal`, `apply-grades`, `apply-audit`, `finalize`) to a coordinator, dispatches the blind finding-grader agents itself (S4), and caps the loop at 3 reviews then "escalates to the user" (`begin` exit 4). None of that has a returned-status form a worker contract can carry.

## User Story

As a release coordinator (an Orca session running the unattended pipeline of #731/#733), I want to start a worker with `Command: /sc:spec-panel-stoprule --unattended --report-dir <D> --mode critique <plan> [--re-review ... --baseline ...]` and read one `return-contract.yaml` that tells me the verdict (PASS, FAIL with open findings at review 1-2, or FAIL at review 3 with the escalation), so that the plan-review gate of `/sc:implement --unattended` is fed with no person and no coordinator session at the terminal.

## Proposed Solution

One `## Unattended mode` section in `src/superclaude/commands/spec-panel-stoprule.md` shaped like the ones in `analyze.md` and `spec-panel.md` (Switch, Report directory, Contract, Person-mode flags, Gates, Nested invocations, Outward actions), plus matching clauses in `~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md`:

- **Switch.** `--unattended` only as a standalone argument token outside any quoted argument; otherwise nothing applies and no contract is written.
- **Report directory.** `--report-dir <dir>` only, with the shared WC-4 rules (refusal text and unusable-directory rules as in `analyze.md`); the report (the review document with its sealed ledger) lands under the report directory so `check` can re-verify it later.
- **Contract.** `<report-dir>/return-contract.yaml` on every outcome, WC-4 fields. `report_path` is the review report; `artifacts` lists the report, any grader/audit reply files and handoff files (minus git-ignored paths). The verdict is carried in the contract (e.g. a `stoprule:` mapping with `verdict`, `review`, `confirmed`, `spec12`, `check_exit`) so the coordinator of #733's gate can consume it; the report itself stays the proof (`check` re-runs on it).
- **The two-column ruling becomes one session.** Under `--unattended` the worker session runs both columns of the protocol's step table in order (as the protocol already allows "with no coordinator ... the same session runs both columns"); no person step is added. The Reviser and the blind grader stay Agent-tool subagents of the worker (WC-7 keeps a command's own Agent fan-out): S4 grader batches and the S6 audit call are dispatched by the worker session itself, replies saved to files under the report directory.
- **Every ask becomes a status.** The loop never calls AskUserQuestion, never ends on a chat question (WC-2). The "escalate to the user" points become returned statuses: a FAIL verdict at review 1 or 2 is `blocked` with the open blocking findings' ids/counts (never full text) in `blocked_question`, so the coordinator revises the plan and starts the next review as a new Task (WC-6); a FAIL at review 3 (the `## Escalation to the user` section `finalize` already writes) is `blocked` naming that section, and the coordinator escalates to the owner and never runs a fourth review. `begin` exit 4 (prior review 3) is reported `blocked`, never reviewed. A PASS is `succeeded`. A grader/auditor unavailable or invalid twice is `failed` (verdict FAIL `incomplete`, as the failure table says) — never a hand-typed PASS. Person-mode flags (e.g. `--mode socratic`, `--mode discussion`) are refused before any work, as the shared rule requires; `--mode critique` is the only loop mode.
- **Integrity unchanged.** The sealed claim ledger, the seal hash and hash chain, `stoprule.py` as the only verdict writer, the frozen rubric hash, the 3-review cap (`begin` exits 4 at a prior review 3) and the blind-grader rules are not weakened: the mode changes who runs the session, not how the verdict is computed. The worker never writes a `verdict:` line and never edits a ledger line after `seal`.
- **Writes stay inside the report directory** (WC-11 shared-worktree rule): the report, reply files, handoff files and the contract only. It stages, commits and pushes nothing (WC-9), and the input plan/spec is never modified (the Reviser applies its edits to a copy under the report directory only; see the Independence rule below).
- **Independence rule (owner question of 2026-11-23, answered yes).** The worker that runs the review loop is a separate coordinator-started task from the worker that wrote the plan (`/sc:workflow`) and from the worker that builds it (`/sc:implement`); it is never the same session as either. The implement worker only receives the path of the finished report and checks it (#733, UI-24); it never runs, retries or grades a review. The Reviser edits only a copy under the report directory; the original plan is never touched by the loop (the coordinator decides what to do with the revised copy and starts the next review as a new task). The blind graders stay separate agents that do not see who wrote the plan.
- **Out of the mode:** no Orca calls from inside the command (WC-8/WC-13), no change to `stoprule.py`'s verdict logic, rubric or cap, no waiver of the panel gate, and no change to attended behaviour.

## Acceptance Criteria

- [ ] `src/superclaude/commands/spec-panel-stoprule.md` contains a `## Unattended mode` section naming `~/.claude/WORKER-CONTRACT.md`, `--report-dir`, `return-contract.yaml`, and no `src/superclaude/` path or Orca command name; the sentence "This variant deliberately has no `## Unattended mode` section and does not accept `--unattended`" is replaced.
- [ ] The brief guard two-copy test passes: with the section present in both copies, a `Command:` line with a standalone `--unattended` and exactly one report directory is accepted; the P-set/count pins in `tests/skills/test_worker_contract.py` are updated for the new command.
- [ ] A worker run of a first review (no confirmed findings, clean audit) ends `succeeded` with a report whose last line is `verdict: PASS` and `stoprule.py check` exit 0, and the contract carries the verdict fields.
- [ ] A FAIL at review 1 or 2 ends `blocked` with counts and ids (no finding text) in `blocked_question`; the Reviser brief handling is defined and tested.
- [ ] A FAIL at review 3 ends `blocked` naming the report's `## Escalation to the user` section; a re-run against that report is `blocked` (begin exit 4), never a fourth review.
- [ ] Grader or auditor unavailable/invalid twice ends `failed` with verdict FAIL `incomplete`; no hand-typed `verdict:` line ever appears.
- [ ] Under `--unattended` the run writes only inside its report directory; nothing staged, committed or pushed; the input plan/spec bytes unchanged by the review itself.
- [ ] Independence: a test or fixture shows that a review run edits only a copy of the plan under the report directory (the original plan's bytes are unchanged), and the section text states that the review worker is never the planning or the implement worker.
- [ ] Person-mode flags (`--mode socratic|discussion`) are refused before any work under `--unattended`, with the WC-4 refusal contract or chat text.

## Out of Scope

- Any change to `stoprule.py`'s verdict computation, the sealed ledger, the rubric, the blind-grader rules or the 3-review cap.
- Any waiver of `/sc:implement`'s `--plan-review` gate (#733 UI-26); implement never runs, retries or grades a review.
- The coordinator-side rules (which session escalates to the owner, how #733's gate consumes the contract) beyond naming the consumer.
- Unattended modes for other not-yet-converted commands.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/commands/spec-panel-stoprule.md` (source of truth; dev copy `.claude/commands/sc/spec-panel-stoprule.md` via `make sync-dev`): Activation note, Usage, new `## Unattended mode`.
- `src/superclaude/skills/sc-spec-panel-stoprule-protocol/SKILL.md` (installed `~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md`): "Who runs which step" unattended clause, grader/auditer dispatch by the worker, failure-table mapping to worker statuses, Reviser handling.
- `src/superclaude/core/WORKER-CONTRACT.md` (section 5): stoprule joins the converted set; brief-table row `--report-dir <dir>`; updated counts.
- `src/superclaude/core/HOW-WE-WORK.md` and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (byte-equal copy).
- Tests: `tests/skills/test_worker_contract.py` (P-set entry, counts, `_check_no_unattended_sections`, write-verb audit classifications for any new line); new test file for the section's pins.
- Mirrors: `plugins/superclaude/commands/spec-panel-stoprule.md`, `plugins/superclaude/skills/sc-spec-panel-stoprule-protocol/**`.

## Related Issues/PRs

- #733 (open): unattended mode for `/sc:implement`; its plan-review gate (UI-24) consumes this feature's report, and this issue is OD-1 option (c).
- #731 (open): reusable release pipeline whose execution step this unblocks.
- #346 (closed): documented that review loops do not converge; the stoprule cap and rubric are the fix, and this feature must not weaken them.

## Priority

High: this blocks other work — the unattended pipeline of #731/#733 cannot run its plan-review step as a worker until it lands (rule "other work is blocked"). Not Urgent: no data loss or broken gate without a workaround, because a person (or coordinator session) can run the loop attended today.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: master (build from a fresh `origin/master` in an Orca-created worktree; edit `src/superclaude/`, then `make sync-dev`).

Commands, in order: /sc:workflow with this issue's number, then /sc:implement, then /sc:pr-submit --monitor 3.

Steps, in order:

- Step 1: Command section in `src/superclaude/commands/spec-panel-stoprule.md`: replace the "deliberately has no Unattended mode" sentence, add `--unattended`/`--report-dir` to Usage and the `argument-hint`, write the `## Unattended mode` section in the style of `spec-panel.md` (Switch, Report directory, Contract, Person-mode flags, Gates, Nested invocations, Outward actions).
- Step 2: Protocol clauses in `src/superclaude/skills/sc-spec-panel-stoprule-protocol/SKILL.md`: the one-session unattended ruling for S0 to S10, worker-session dispatch of the S4 grader batches and S6 audit (Agent tool, replies saved under the report directory), the failure-table-to-worker-status mapping, and the Reviser handling for an unattended fix cycle (the Reviser edits a copy under the report directory only) plus the independence rule.
- Step 3: `src/superclaude/core/WORKER-CONTRACT.md`: phase sentence, brief-table row `/sc:spec-panel-stoprule | --report-dir <dir>; --mode critique only`, updated command counts; `src/superclaude/core/HOW-WE-WORK.md` plus its plugin copy.
- Step 4: Tests: update `tests/skills/test_worker_contract.py` (converted-set entry, exact counts, no-unattended-sections list, write-verb audit for any new audited line — say "stage nothing", not the verb phrase); add the new section pin test.
- Step 5: `make sync-dev`, `make verify-sync`, refresh `plugins/superclaude/` mirrors; stage only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks` (never `.claude/` paths).
- Step 6: `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (targets IronbellyOrg/IronClaude only).

## Test plan

- Tests to add or change: new `tests/skills/` pin test asserting the `## Unattended mode` section's required phrases (`WORKER-CONTRACT.md`, `--report-dir`, `return-contract.yaml`, `--mode critique`) and the absence of `src/superclaude/` paths, Orca command names and `AskUserQuestion`; update `tests/skills/test_worker_contract.py`'s converted-command set, count checks and write-verb classifications; a guard-side test that the two-copy test now accepts a stoprule brief with `--unattended` (or the existing generic guard test covers it once the section exists — verify).
- Regression gate: `uv run pytest tests/skills tests/commands tests/core -q`, `make lint`, `make verify-sync`, `plugins/superclaude/` parity.
- How a reviewer verifies: run a stoprule critique on a small spec with `--unattended --report-dir .dev/tmp-check/` in a throwaway worktree; confirm `return-contract.yaml` with the verdict fields, `stoprule.py check` exit 0 on the report, no writes outside the report directory, and a FAIL fixture producing `blocked` with counts only.

<!-- sc:issue:create template=issue-feature-simple -->

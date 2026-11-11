review: 2 of 3

# Spec-panel review, round 2 (re-review): Orca worker contract spec

Notation: `SPEC:N` is line N of the candidate, `BASE:N` is line N of the baseline, `R1:N` is line N of the prior report `review/round1.md`, `INV-A:N` and `INV-B:N` are lines of `inventory/commands-a.md` and `inventory/commands-b.md`, `CAPS:N` is a line of `inventory/orca-capabilities.md`, all under `.dev/orca-command-refactor/`. A citation into a file that is not in the workspace (`cmd/`, `sk/`, `src/`, `CLAUDE.md`, `EVIDENCE.md`, `/opt/Orca`) is UNVERIFIED here and is marked so.

## Header
| Field | Value |
|---|---|
| Command run | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 59034 bytes), sha256 `466dcf239d1cdea564cc23de1d5abe284de1d002582065afb592d5d4494fa5a3` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines, 57763 bytes), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (the same hash round 1 recorded for the text it reviewed, `R1:9`, so the baseline is exactly the reviewed text) |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` (174 lines), sha256 `ed038de0d0274f6eec9e5a8f655a808d6fd1d48e2c8791557de36ade2639163f`; header `review: 1 of 3` (`R1:1`), final line `verdict: FAIL` (`R1:173`); so N = 1 + 1 = 2 |
| Reviewer model actually used | `claude-sonnet-5-5` |
| Review date | 2026-11-10 |
| Prompt followed | RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before any finding: roles table, Step 1, review number, self-check, re-review brief). Cap check: the prior report is at review 1, so the cap check (prior `review: 3` with FAIL) does not apply; this run is review 2 of 3. |
| Re-check procedure | The rf-qa Fix Cycle steps 1-5 named in the command (project `.claude/agents/rf-qa.md`, else `~/.claude/agents/rf-qa.md`) are not present in the sandbox (no such file under `ws/` or `home/.claude/`), so the file is unread and the rules of the command's Review Loop section stand alone, as that section allows. |
| Panel | Focus panel in command order: Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Newman, Hohpe; Whittaker (active in every review, after Fowler and Nygard). Crispin, Gregory and Hightower are outside both focus panels and did not speak. |
| Not run | Improve step and any revised specification (a re-review skips them: Review Loop bullet 4). `--iterations` (ignored under `--re-review`). State Variable Registry (needs `--focus correctness`). Pipeline Dimensional Analysis and Quantity Flow Diagram (not triggered: no changed line adds a multi-stage flow whose count differs between stages). |

## Step 1. Evidence block (before any finding)
Roles are fixed by the command line and the prompt's table, not by reading order: CANDIDATE = the `@file` (sha256 `466dcf23...`); BASELINE = the `--baseline` file (sha256 `d3cdbe57...`); PRIOR = the `--re-review` file. Command run: `diff -w BASELINE CANDIDATE`. The diff is not empty: 12 changed lines in 12 one-line hunks (the file has 285 lines on both sides, so line numbers are the same on both sides). Changed lines copied verbatim (the `<` and `>` markers removed):


#### Hunk 62c62
BEFORE (baseline)
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

AFTER (candidate)
```text
| WC-4 | **One report file, at a path one rule fixes, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at one of three places (R1-B2): `<dir>/return-contract.yaml` when the brief passes a directory (`--output` / `--output-dir`); `<file>.return-contract.yaml` beside the file when the flag names a file (tdd, init-lite, and any section 3 row that adds a file path), so parallel workers with different output files never share a contract; or, for the two commands that fix their own place, `<output>/adversarial/return-contract.yaml` (adversarial) and `.dev/tasks/to-do/<id>/return-contract.yaml` (workflow, whose id the command chooses, so the coordinator learns the path from `worker_done --report-path`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, except a workflow stop before its package exists, which has no place to write: it writes no contract and ends `failed` with no report (WC-5, R1-B2). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

#### Hunk 73c73
BEFORE (baseline)
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

AFTER (candidate)
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` where the command's phase has passed (section 6, R1-B1) and every flag section 3 lists as required; the output directory or file, so the report path follows from WC-4's rule (R1-B2); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

#### Hunk 76c76
BEFORE (baseline)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

AFTER (candidate)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file, at the path WC-4's rule gives (R1-B2). Every changed command also gains the `## Unattended mode` section (section 2.1) in the phase its row names, together with that row's gate resolutions (R1-B1). Phase numbers refer to section 6.
```

#### Hunk 92c92
BEFORE (baseline)
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

AFTER (candidate)
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None (WC-4 fixes its contract place; a stop before the package exists writes none, R1-B2) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

#### Hunk 116c116
BEFORE (baseline)
```text
| research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
```

AFTER (candidate)
```text
| research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | add `--output <dir>`; contract there, naming the generated `claudedocs/research_*.md` path (R1-B2) | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
```

#### Hunk 149c149
BEFORE (baseline)
```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```

AFTER (candidate)
```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```

#### Hunk 154c154
BEFORE (baseline)
```text
Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.
```

AFTER (candidate)
```text
Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. A command gains `--unattended` only in the phase its section 3 row names, together with its gate resolutions, so no command accepts the flag while it still prompts; the coordinator passes it only to a command whose phase has passed, and never to brainstorm or init-lite, which are unchanged (R1-B1). Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.
```

#### Hunk 159c159
BEFORE (baseline)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

AFTER (candidate)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on the P1 commands only, each with the resolution its section 3 row gives (R1-B1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

#### Hunk 195c195
BEFORE (baseline)
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate)
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command whose section 3 phase is P1 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no later-phase or section-4 command has one yet; each later phase extends the list to its own commands (R1-B1) | passes |
```

#### Hunk 198c198
BEFORE (baseline)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

AFTER (candidate)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names one fixed path, `<output>/adversarial/return-contract.yaml` (R1-B2) |
```

#### Hunk 200c200
BEFORE (baseline)
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

AFTER (candidate)
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic, contract at `<file>.return-contract.yaml`; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

#### Hunk 240c240
BEFORE (baseline)
```text
- (a) **Coordinator or person only (recommended).** The coordinator (a top-level session) runs it after the workers finish; no pr-submit changes in Phase 4.
```

AFTER (candidate)
```text
- (a) **Coordinator or person only (recommended).** The coordinator (a top-level session) runs it after the workers finish; no pr-submit section or change, so it drops out of Phase 4 (R1-B1).
```

### Self-check (commands were run)
Each quoted AFTER line (without its `>`) was searched with `grep -nFx` in CANDIDATE and each quoted BEFORE line (without its `<`) in BASELINE; a hit on the other file would mean swapped roles.

| Hunk (line) | BEFORE line found in BASELINE | AFTER line found in CANDIDATE | BEFORE line found in CANDIDATE (must be none) | AFTER line found in BASELINE (must be none) |
|---|---|---|---|---|
| 62 | line 62 | line 62 | none | none |
| 73 | line 73 | line 73 | none | none |
| 76 | line 76 | line 76 | none | none |
| 92 | line 92 | line 92 | none | none |
| 116 | line 116 | line 116 | none | none |
| 149 | line 149 | line 149 | none | none |
| 154 | line 154 | line 154 | none | none |
| 159 | line 159 | line 159 | none | none |
| 195 | line 195 | line 195 | none | none |
| 198 | line 198 | line 198 | none | none |
| 200 | line 200 | line 200 | none | none |
| 240 | line 240 | line 240 | none | none |

## Coverage (what this review covered)
- Read in full: `README.md` (39 lines, binding context), the candidate (285 lines), the prior report (174 lines), the loop prompts file, `command.md`; the three inventory files were searched for every line the changed text cites or depends on (`INV-A:35-55,60-61,97`, `INV-B:47,51,267-275`, `CAPS:70-79`) and read where a finding rests on them.
- Checked: each of the 12 changed lines against both prior blocking findings; every line of the candidate that depends on a changed line (phase lists `SPEC:158-162` against the Phase column of `SPEC:99-125` and `SPEC:83-92`: 9 P1, 15 P2, 4 P3, 3 P4 commands, all consistent; counts 10 + 27 + 6 = 43 unchanged); the shell and test conditions of `SPEC:195-200`; the guards on changed lines (table below).
- Citation status: the changed lines cite `CAPS:72-74,79`, `INV-B:272`, `INV-A:97` and inventory-internal quotes; I checked `CAPS:72-74` (`orca-capabilities.md:74` "Report path only with real values") and `INV-B:272` (workflow: contract not written for pre-creation STOPs, `refs/return-contract.md:39` quoted there). Everything the changed lines cite inside `cmd/`, `sk/`, `src/`, `CLAUDE.md` and the Orca guides is UNVERIFIED here, and the verdict does not depend on it.
- Not covered: lines unchanged against the baseline, except where a changed line depends on them (Review Loop bullet 5); the truth of the inventory verdicts (no source command files in the sandbox).

## Prior blocking findings (re-check against the AFTER text only)
| Id | Prior defect (`R1:59-79`) | Status | Reason, from the AFTER text |
|---|---|---|---|
| R1-B1 | P1 shipped `--unattended` and the `## Unattended mode` section on all 37 commands of sections 3.1 and 3.2 while gate conversion was in P2 to P4, so gated commands accepted the flag and still prompted; AC-1.1 passed on section presence alone | **resolved** | `SPEC:154` now says a command gains the flag only in the phase its section 3 row names, together with its gate resolutions, so no command accepts the flag while it prompts, and the coordinator passes it only after that phase has passed. `SPEC:159` limits P1 to "the P1 commands only" and drops workflow from the P1 fixes; the nine P1 commands of `SPEC:99-125` (analyze, build, business-panel, design, document, explain, index, load, test) are the nine named in `SPEC:159`. `SPEC:195` limits AC-1.1 to commands whose section 3 phase is P1 and asserts that no later-phase or section-4 command has a section yet. `SPEC:240` removes pr-submit from Phase 4 under the recommended D3(a), which also removes the D3(a) versus AC-1.1 clash. The stall trace of `R1:68` (task or cleanup accepting the flag after P1) can no longer arise from the stated text unless the coordinator breaks `SPEC:154` (follow-up R2-M3). |
| R1-B2 | WC-4 put the contract at `<output-dir>/return-contract.yaml` although tdd and init-lite take a file; adversarial had two paths; workflow's id is command-chosen and its pre-creation stop had no place; research had no flag | **resolved** | `SPEC:62` fixes the path by one rule with three cases: directory flag gives `<dir>/return-contract.yaml`; file flag gives `<file>.return-contract.yaml` (so AC-2.2's `--output <file>` run, `SPEC:200`, now names `<file>.return-contract.yaml`, and two tdd workers with different files never share a contract, WC-11 `SPEC:69`); adversarial gets one path `<output>/adversarial/return-contract.yaml`, repeated in `SPEC:83` and `SPEC:198`; workflow keeps `.dev/tasks/to-do/<id>/return-contract.yaml`, learned from `worker_done --report-path`, and a stop before its package exists writes no contract and ends `failed` with no report, which matches `INV-B:272` ("Not written for pre-creation STOPs") and `CAPS:74` (`--report-path` only with real values) and is consistent with WC-5 `SPEC:63` ("no report exists" gives `--outcome failed`). `SPEC:92` drops the unconditional workflow change that SA-3 (`SPEC:148`) forbade. `SPEC:116` gives research `--output <dir>` and a contract there. Residual gaps for rows without an output flag are new, narrower and Medium (R2-M1). |

## Findings on changed lines
Grading: every finding below was run through the grading check ("an implementer who follows the stated text as written builds X, and X is wrong because Y"). None holds without a further assumption or an undefined requirement, so none is blocking; all are Medium or minor and sit under `follow-up candidates`. `origin=changed` means the finding is on a line changed against the baseline; `origin=unchanged` is a note unless it quotes the changed line that depends on it.

| Id | Severity | Origin | Changed line | One-line summary |
|---|---|---|---|---|
| R2-M1 | Medium | changed | `SPEC:62` | WC-4's three-case rule does not cover rows with no output flag, or rows whose new flag's directory-or-file type is unstated |
| R2-M2 | Medium | changed | `SPEC:62` | WC-4 lists init-lite as writing `<file>.return-contract.yaml` in unattended mode, but `SPEC:154` says init-lite is unchanged and never gets the flag |
| R2-M3 | Medium | changed | `SPEC:73`, `SPEC:154` | The "phase has passed" rule has no carrier for a coordinator in another project, and no behaviour when the flag is passed too early |
| R2-M4 | Medium | changed (AC-1.1) / unchanged (AC-1.2) | `SPEC:195` | AC-1.1 and AC-1.2 cannot be met as stated by load, cleanup-audit and index-repo |
| R2-M5 | Medium | changed | `SPEC:154`, `SPEC:159` | P1 now ships four gate resolutions that no P1 check exercises |
| R2-N1 | minor | unchanged | `SPEC:79` | "until Phase 1 adds the contract" is stale for the P2 commands in section 3.1 |
| R2-N2 | minor | changed | `SPEC:154` | The never-pass list names brainstorm and init-lite, not workflow |
| R2-N3 | minor | unchanged | `SPEC:76`, `SPEC:240` | pr-submit stays in the "27 needing a change" under the recommended D3(a), which changes nothing in it |
| R2-N4 | minor | changed | `SPEC:62` | The workflow carve-out loses `blocked_question` for a pre-package stop |

=== REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

**R2-M1. Medium, origin=changed. WC-4 is not exhaustive.** Expert: Wiegers. Priority: Medium. Quality impact: completeness -1, testability -1.
- `SPEC:62` claims "a path one rule fixes" with three cases: a directory flag, a file flag, and the two commands that fix their own place (adversarial, workflow). Rows that fit none of the three: cleanup-audit (fixed `.claude-audit/`, no output flag, `SPEC:85`, `INV-A:42`) and index-repo (repo-root `PROJECT_INDEX.md`, no flag, `SPEC:86`, `INV-A:53`), both with phase P1 and so covered by AC-1.1 (`SPEC:195`); implement ("contract beside the ledger `progress.md`", `SPEC:109`); save ("contract naming the file written", no flag, `SPEC:119`); cli-portify ("file location unnamed", `SPEC:105`); recommend and explain ("write ... to a file", `SPEC:108`, `SPEC:115`). `SPEC:109` also names a fourth place, which `SPEC:62` ("one of three places") does not allow.
- For the rows that "add `--output`", "add a report path" or "add an output path" (analyze, build, design, index, test, spec-panel; `SPEC:99,101,106,111,120,123`) the text does not say whether the new flag takes a directory or a file, and `SPEC:62` picks the contract path by exactly that. The coordinator therefore cannot derive the path from the spec, which `SPEC:73` says it should be able to.
- Grading: a requirement the document never states (an undefined edge), not a stated text that does harm: Medium. The reviser followed the prior recommendation (one rule covering a directory flag, a file flag and a command-chosen directory, `R1:79`); this is the per-row typing that remains.

**R2-M2. Medium, origin=changed. init-lite is named as writing a contract it is not given.** Expert: Cockburn (who calls the result a goal the actor cannot reach), Wiegers.
- `SPEC:62` lists "tdd, init-lite" as the commands whose file flag puts the contract at `<file>.return-contract.yaml` "in unattended mode". `SPEC:154` says the coordinator never passes `--unattended` to brainstorm or init-lite "which are unchanged", and `SPEC:87` gives init-lite "None" as its change and the output file as its report today (`INV-A:55`). A worker following `SPEC:62` for init-lite passes a contract path that does not exist as `--report-path`; WC-5 (`SPEC:63`) then reads "no report exists" and sends `--outcome failed` for a successful audit.
- Grading: needs a guess that the worker applies `SPEC:62` rather than `SPEC:87`/`SPEC:154`; Medium. Fix by dropping init-lite from `SPEC:62`.

**R2-M4. Medium, origin=changed (AC-1.1) and unchanged (AC-1.2, `SPEC:196`). The P1 checks cannot be met by three P1 commands.** Expert: Adzic (the scenario cannot be run).
- AC-1.1 (`SPEC:195`, changed) asserts that every command whose section 3 phase is P1 has a section naming `return-contract.yaml`. load is "P1 (usage line only)" with Report "none" and is "not as its own Task" (`SPEC:112`); cleanup-audit and index-repo are P1 small fixes with no stated contract place (R2-M1). AC-1.2 (`SPEC:196`, unchanged, depends on the changed P1 scope) runs the 7.2 live check with `--unattended --output <dir>` on "each P1 command", whose steps 3 and 4 need a contract (`SPEC:182-183`); load has none, and cleanup-audit and index-repo have no `--output` (`SPEC:85-86`).
- Grading: the implementer must guess whether "P1 command" includes these three; Medium.

**R2-M5. Medium, origin=changed. P1 now ships gate resolutions that no P1 check exercises.** Expert: Wiegers, Crispin's concern raised by Wiegers because Crispin is outside the panels.
- `SPEC:154` and `SPEC:159` make each P1 command carry "the resolution its section 3 row gives". Four P1 rows are resolutions, not "no gate": business-panel refuses `--mode socratic`, explain refuses `--format interactive`, test refuses `--watch`, index states the knowledge-base mode does not wait (`SPEC:102,108,111,123`). The checks that exercise gate resolutions are AC-2.1 and AC-2.2 (`SPEC:199-200`), both P2; AC-1.1 asserts section presence and AC-1.2 is a happy-path run. `SPEC:159` still says "No person gate is involved". So the stall of `R1:68` is closed by the phase rule but a wrong refusal in P1 would still pass the P1 checks.
- Grading: a missing check, not a stated text that does harm; Medium.

=== ARCHITECTURE ANALYSIS === (Fowler lead, Nygard, Newman, Hohpe)

- **Fowler (boundaries).** The change splits the contract into a path rule owned by the contract file and a per-row phase owned by the rollout. That is the right seam: `SPEC:154` and `SPEC:62` now read as one design. The only boundary leak is that the phase rule lives in the spec but must be applied by a coordinator that reads the installed contract (R2-M3).
- **R2-M3. Medium, origin=changed. The coordinator rule has no carrier and no failure behaviour.** Expert: Fowler, Nygard. `SPEC:73` makes the brief include `--unattended` "where the command's phase has passed (section 6, R1-B1)", and `SPEC:154` tells the coordinator to pass it only then. P0 writes `WORKER-CONTRACT.md` as "section 2 rules plus a coordinator brief template listing the section 3.1 flags" (`SPEC:158`); nothing says the installed file lists which commands accept the flag at the installed version, and a coordinator in another project cannot read the spec's section 6. Nothing says what a command does when the flag arrives early: a command that does not know `--unattended` treats it as ordinary text and prompts, which is the stall `SPEC:44` calls invisible. The prior finding's alternative (a command refuses the flag until its phase) was not taken, which is allowed, but the reliance on coordinator discipline is unchecked: no AC covers it. Grading: needs a coordinator mistake plus a missing requirement; Medium.
- **Nygard (failure modes).** Workflow's pre-package stop is now a defined failure (`SPEC:62`, `INV-B:272`). One cost: it ends `failed` with the question only in the body's first sentence, because no contract and so no `blocked_question` exists (R2-N4). A retry of a file-flag command reuses the same `<file>.return-contract.yaml` path, so a stale `blocked` contract from attempt 1 is not distinguishable by path; this is the round-1 retry and stale-contract follow-up (`R1:143`) extended to the new file form, unchanged in grade (WC-6 `SPEC:64` speaks of a fresh output directory, which a file flag does not have).
- **Newman (interfaces).** The path rule is versionable and the file-form suffix is unambiguous. No version field exists (carried from `R1:150`, not re-graded).
- **Hohpe (message exchange).** `worker_done --report-path` carries the contract path in all three cases, and is omitted when no file exists (`SPEC:62`, `CAPS:74`). Consistent.

### === ADVERSARIAL ANALYSIS === (Whittaker, changed lines only)
1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`SPEC:62`)** ("a path one rule fixes") fails when **the command has no output flag at all**. Concrete attack: before: `/sc:cleanup-audit --pass 1 --unattended` (P1; fixed `.claude-audit/`); the three cases do not match (not a passed directory, not a file flag, not adversarial or workflow); after: the section AC-1.1 requires names `return-contract.yaml` with no location, and the coordinator cannot compute the `--report-path`. MAJOR [Medium, R2-M1: an undefined edge].
2. I can break this specification by **Divergence Attack**. The invariant at **`SPEC:154`** ("passes it only to a command whose phase has passed") fails when **the flag is passed to a command whose phase has not passed**. Concrete attack: during P1 a coordinator briefs `/sc:task "x" --unattended`; task has no section until P2 (`SPEC:121`), so the flag is unrecognised, confidence 0.65 triggers the prompt, the worker parks with no `worker_done`. The stated text forbids the brief; it does not say what the command does. MAJOR [Medium, R2-M3].
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **`SPEC:62` versus `SPEC:154`** fails when **init-lite appears in a rule that fires "in unattended mode" while init-lite has no such mode**. Concrete attack: state trace: init-lite run succeeds, writes `.dev/superclaude/context-audit.md`; the worker follows WC-4, passes `context-audit.md.return-contract.yaml` as `--report-path`; the file does not exist; WC-5 maps "no report exists" to `failed`. MAJOR [Medium, R2-M2].
4. I can break this specification by **Sequence Attack**. The invariant at **`SPEC:62` (file form) versus WC-6 (`SPEC:64`)** fails when **a retry reuses the brief's `--output <file>`**. Concrete attack: attempt 1 of `/sc:tdd ... --output d.md` ends `blocked` and leaves `d.md.return-contract.yaml`; attempt 2 dies before writing; the coordinator opens the same path and reads `blocked` for attempt 2. MINOR [carried: the round-1 retry follow-up, `R1:143`, now for the file form too; no new grade].
5. Divergence, Accumulation and the remaining attacks found nothing new on changed lines: the two path forms cannot collide for different output files (`SPEC:62`, WC-11 `SPEC:69`), and `SPEC:62` versus `SPEC:83` agree on adversarial.

### Guard Condition Boundary Table (guards on changed lines only; Nygard builds, Whittaker attacks; Crispin's completeness check done by this reviewer because Crispin is outside the focus panels)
| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `phase_passed` (flag allowed only after the command's phase) | `SPEC:73`, `SPEC:154` | Zero/Empty | command with no phase (brainstorm, init-lite, workflow) | false | brainstorm and init-lite named as never; workflow not named but excluded by the literal rule (see R2-N2) | OK |
| `phase_passed` | `SPEC:154` | One/Minimal | P1 command during P1 after P1 checks pass | true | flag accepted, AC-1.2 | OK |
| `phase_passed` | `SPEC:154` | Typical | P2 command after P2 checks pass | true | flag accepted | OK |
| `phase_passed` | `SPEC:154` | Maximum/Overflow | flag passed before the phase has passed | false | brief forbidden; command behaviour when it arrives is not stated | GAP |
| `phase_passed` | `SPEC:240` | Sentinel Value Match | pr-submit (P4) under D3(a) | false forever | no section, no change | OK |
| `phase_passed` | `SPEC:112`, `SPEC:195` | Legitimate Edge Case | load, "P1 (usage line only)" | unclear | not stated whether load gets the flag and section | GAP |
| `contract_path_rule` | `SPEC:62` | Zero/Empty | no output flag (cleanup-audit, index-repo, save) | no case matches | not stated | GAP |
| `contract_path_rule` | `SPEC:62` | One/Minimal | directory flag | case 1 | `<dir>/return-contract.yaml` | OK |
| `contract_path_rule` | `SPEC:62`, `SPEC:200` | Typical | file flag (tdd) | case 2 | `<file>.return-contract.yaml` | OK |
| `contract_path_rule` | `SPEC:62`, `SPEC:83` | Sentinel Value Match | adversarial with `--output <dir>` (matches case 1 and the fixed-place case) | fixed-place case | `<output>/adversarial/return-contract.yaml`, repeated at `SPEC:83`, `SPEC:198` | OK |
| `contract_path_rule` | `SPEC:62`, `SPEC:99-123` | Legitimate Edge Case | new flag whose type is unstated ("add `--output`") | undetermined | not stated | GAP |
| `contract_path_rule` | `SPEC:62`, `SPEC:87`, `SPEC:154` | Legitimate Edge Case | init-lite, file flag, no unattended mode | contradictory | `SPEC:62` names it; `SPEC:154` and `SPEC:87` exclude it | GAP |
| `workflow_package_exists` | `SPEC:62` | Zero/Empty | stop before the package exists | false | no contract, `failed`, no report | OK |
| `workflow_package_exists` | `SPEC:62` | Typical | package exists | true | contract at `.dev/tasks/to-do/<id>/`, path via `worker_done --report-path` | OK |

Left out: `phase_passed` and `contract_path_rule` Maximum for the path rule (a path cannot overflow: no limit is stated anywhere; N/A); `workflow_package_exists` One/Minimal, Maximum and Sentinel (a boolean event).
GAP rows (FR-8, FR-9): five rows. Their grades: each is a missing requirement or undefined state, not a stated text that does harm, so under the loop grading all five are Medium (R2-M1, R2-M2, R2-M3, R2-M4); none is blocking. The blank-behaviour cells are the same rows.

## Follow-up candidates (Medium and minor; not blocking, never in the Reviser brief)
Medium (warnings): R2-M1 to R2-M5 above. Suggested minimal repairs, for whoever opens an issue:
- R2-M1: add one sentence to `SPEC:62` for a command with no output flag (the contract goes beside its fixed report, named in its row), and state in each "add `--output`" row whether it is a directory or a file.
- R2-M2: delete "init-lite" from `SPEC:62`.
- R2-M3: say in `SPEC:158` that the installed contract lists the commands that accept the flag, and what the worker does if the flag is rejected or ignored.
- R2-M4: say in `SPEC:195-196` that load, cleanup-audit and index-repo are excluded from AC-1.1 and AC-1.2, or give them a contract place.
- R2-M5: add one P1 assertion per refusal in the four P1 rows.

Minor (notes):
- R2-N1 (origin=unchanged, depends on changed `SPEC:154`): `SPEC:79` says the worker "reports the named file until Phase 1 adds the contract", but reflect, release-split, tdd and troubleshoot get the flag and contract in P2 (`SPEC:88-91`, `SPEC:160`).
- R2-N2 (origin=changed): `SPEC:154` names brainstorm and init-lite as never receiving the flag; workflow (`SPEC:92`, change "None") is excluded only by the general rule.
- R2-N3 (origin=unchanged): pr-submit is counted in the 27 (`SPEC:76`, `SPEC:114`) although D3(a), the recommendation, makes no change to it (`SPEC:240`).
- R2-N4 (origin=changed): with the workflow carve-out, a stop that is really a question (a pre-package gate) reaches the coordinator only in the first sentence of the `worker_done` body (`SPEC:62`, `SPEC:63`).

Carried from round 1 and not re-graded (no changed line touches them; `R1:136-160`): the Medium and minor candidates of the first review stay open as written there, with one narrowing: the part of the round-1 SA-1/SA-3 versus unconditional changes candidate (`R1:150`) that named the workflow pre-creation contract no longer applies, because `SPEC:92` now changes nothing in workflow (the adversarial path, validate-tests default target and validate-roadmap report-name parts remain).

## Issue question
The command asks the reviewing session to ask the user once per loop whether to open an issue for the follow-up candidates, and to create none without an answer. No interactive user exists in this sandbox run, so the question was not asked and no issue was created; the list above is the record.

## Brief clauses overridden
None. The brief asked for the RE-REVIEW prompt with the stated values, a report at `review/round2.md`, `path:line` citations and UNVERIFIED marking; all were applied as written. The brief did not widen scope or regrade a minor finding.

## Coverage line
scoped PASS: changed lines + prior blockers

## Reviser brief
None. No blocking finding is open: R1-B1 and R1-B2 are resolved, and no new blocking finding was found on a changed line. Medium and minor findings never appear in the Reviser brief and never trigger a revision.

verdict: PASS

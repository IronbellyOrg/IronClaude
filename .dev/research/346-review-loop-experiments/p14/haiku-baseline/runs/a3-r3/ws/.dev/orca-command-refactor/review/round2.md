review: 2 of 3

# Spec-panel re-review, round 2: orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `90517bb8b39156a6ae96df698dafb7e24324de3cb8682a343273a1cbd2cce875`
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Prior report: `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`), sha256 `3c46c126602e66865637a545a0eafd180a5589399f4c9b9169dd9211c6162b20`
- Focus: requirements, architecture
- Mode: `--re-review` with `--baseline`, critique. `--iterations` ignored, Improve step skipped, no revised specification written.
- Prompt: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full from the sandbox home (`/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p14/haiku-baseline/runs/a3-r3/home/.claude/rules/prompts/document_review_loop_prompts.md`)
- Reviewer model: claude-haiku-5-5

## Coverage

Read in full: the candidate spec (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 296 lines), the baseline `.dev/orca-command-refactor/specs/history/spec-v1.md`, the prior report `.dev/orca-command-refactor/review/round1.md`, the shared context `.dev/orca-command-refactor/README.md`, the command definition `command.md` in the sandbox (the brief's `/sc:spec-panel` definition), and the review-loop prompts file.

Read at the cited lines only: `.dev/orca-command-refactor/inventory/commands-a.md:35,60-61`; `.dev/orca-command-refactor/inventory/commands-b.md:43,177-185,267-275`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:72-79`.

Not covered: the rest of the inventories; `src/superclaude/...`; `cmd/spec-panel.md` and the `sk/...` skill refs (none is in the sandbox); `rf-qa.md` (neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` in the sandbox home exists, so the rules in review-loop item 5 stand alone); `review/revise1.md` (not a named input). Every claim that rests only on those is UNVERIFIED here. No Orca command, git command or network call was run. Bash was used only for `sha256sum`, `diff -w`, `grep` self-checks and a piped test of the AC-C1 pattern; this report is the only file written.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Output file is `review/round2.md` | `review/spec-panel.md` (`.dev/orca-command-refactor/README.md:26`); `review/round2.md` (brief) | The brief names `round2.md`. Same choice as round 1. |
| `command.md` stands in for `cmd/spec-panel.md` | Treat the spec's `cmd/spec-panel.md` citations as UNVERIFIED | Same as round 1: the brief names `command.md` as the definition. Line numbers below are from `command.md`. |
| Scope of re-review | Whole-document review; changed lines plus prior blockers | Review-loop item 5: changed lines against the baseline, plus the prior blocking findings. Whole-document assurance is not claimed. |
| Verdict | FAIL; PASS with follow-ups | No open blocking finding. Every prior blocker is resolved, and no changed line states a text that yields a wrong outcome without a further assumption. |

## Step 1, evidence block

Roles fixed: CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`. Command run: `diff -w BASELINE CANDIDATE`. Lines are copied in diff order; blank diff lines are omitted.

BEFORE (baseline), lines starting `<`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

AFTER (candidate), lines starting `>`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, except as stated next. Commands that already write a contract keep their fields and add the missing ones. [B1] A command with no output-directory flag keeps its own contract path. `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml` (`INV-B:272`), a path that does not exist before the run creates the package, so it is not known before dispatch and section 2.3 does not apply to it. Its pre-creation STOPs write no contract (`INV-B:272`, no package exists yet), and WC-5 maps them to `failed`. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory where the command takes one, so the report path is known before dispatch (WC-4; [B1] `/sc:workflow` has no such flag and reports its path after the run); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | [B1] Write the contract at `<output>/return-contract.yaml`, not a subdirectory, so it matches WC-4 (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | [B1] None. Pre-creation STOPs write no contract; the worker reports `failed` (WC-4, WC-5) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | [B4] contract at the report path the command already takes, or a new `--output` if it takes none | fresh dir | [B4] Before editing, read `cmd/spec-panel.md`. If it already has an output flag or a `## Unattended mode` section, reuse them and add neither again | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` (the "no `--output`" statement is the inventory's, UNVERIFIED against this workspace, see section 9 item 15) | P2 |
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract filename [B1: the workflow contract item is removed, since its only gap was the pre-creation STOP], explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo [B1: workflow removed] | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| AC-C1 | The command in the block below | prints nothing (SA-2, WC-8) |
[B2] AC-C1 as first written put `\|` inside an ERE. GNU grep reads that as a literal pipe, so the check never matched an Orca command. The corrected check, with the two exemptions below:
```bash
grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
  | grep -v '^src/superclaude/skills/ccsession-tag/' \
  | grep -v -e '^src/superclaude/core/WORKER-CONTRACT\.md:' -e '^src/superclaude/core/HOW-WE-WORK\.md:'
```
[B2] `WORKER-CONTRACT.md` may mention Orca in its caller-channel example (SA-2). `HOW-WE-WORK.md` gains an Orca section in P0 (SA-5), so it is excluded here. P0 checks that section by reading it, and AC-0.3 covers the existing routing rows.
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | [B3] Steps 1, 2, 5, 6 and 7 pass. Step 3 passes when exactly one `worker_done` arrives, its `--outcome` matches the status that the command's own report states (WC-5 applied to that report), and its `--report-path` is that report file. Step 4 is replaced by `test -s` on that report file, since no YAML contract exists until P1. The report files are `REPORT.md` for `/sc:troubleshoot`, `.dev/tasks/to-do/<id>/return-contract.yaml` for `/sc:workflow` (its `status` key is the one checked), and the return contract under `--output` for `/sc:adversarial` (its filename varies between runs, `INV-A:60-61`, so the worker names the file it found). Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path (`<output>/return-contract.yaml`); workflow's return-contract ref states that no contract is written for pre-creation STOPs (`INV-B:272`) [B1] |
15. [B4] Whether `cmd/spec-panel.md` already has an output flag and an `## Unattended mode` section. `INV-B:43` says no output flag exists. A sandbox copy of the command file, outside this workspace, shows both (its line 23 and lines 455-463), so this is not settled here. The section 3.2 row is written to be correct either way. Resolve in P2 by reading the file in the repo.
```

Self-check (run before the verdict; `grep -cF` of each quoted line in the candidate and in the baseline, no file written): every AFTER line is found in the candidate and every BEFORE line is found in the baseline, so the role assignment is correct. Blank lines match trivially and are not counted.

## Prior blocking findings (from round1.md)

| Prior id | Status | Evidence |
|---|---|---|
| B1 (WC-4 path for `/sc:workflow`; adversarial path) | resolved | WC-4 carves out a command with no output-directory flag and states the workflow pre-creation rule (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62`); adversarial now names `<output>/return-contract.yaml` (`:83`); workflow row says no contract for pre-creation STOPs (`:92`); AC-1.4 matches (`:208`). Residual wording in `:62` is F7. |
| B2 (AC-C1 vacuous; SA-2 contradiction) | resolved | The pattern at `:177` now uses ERE alternation. Piped test: `run orca orchestration task-create now` and `run orca-ide worktree list` match; `no match here` does not. The exemptions are F2. |
| B3 (AC-0.4 cannot pass in P0) | resolved | AC-0.4 (`:204`) replaces step 4 with `test -s` on the report file and checks step 3 against that report's own status. The workflow check uses its `status` key. |
| B4 (spec-panel row premise false for `command.md`) | resolved as to the false premise | Row `:120` now makes the output flag conditional on reading the file, and UNVERIFIED item 15 (`:296`) records the sandbox copy. The naming conflict that remains is F1. |

No prior blocking finding is open or regressed.

## Findings on changed lines (origin=changed)

Blocking: none.

**F1. Medium. origin=changed. The spec-panel contract path has two readings, one of them wrong.** Quoted: candidate `:62` "the directory the coordinator passed (`--output` / `--output-dir`)"; candidate `:120` "contract at the report path the command already takes, or a new `--output` if it takes none". `command.md:23` lists `[--output <file>] ... [--report-dir <dir>]`, `command.md:460` says `--output` is "file-valued", and `command.md:460` names `--report-dir` as the directory. An implementer who reads `:62` literally treats `--output` as a directory and writes `<file>/return-contract.yaml`, which cannot be written. An implementer who reads `:120` picks the file path. Only a third reading (`--report-dir`) fits WC-4, and the text does not say so. Needs a guess, so Medium. The "or a new `--output` if it takes none" clause is inert, because the command takes one.

**F2. Medium. origin=changed. The AC-C1 exemptions exclude whole files, and the P0 Orca-section check has no pass condition.** Candidate `:179` excludes every line of `src/superclaude/core/WORKER-CONTRACT.md` and `src/superclaude/core/HOW-WE-WORK.md` from the gate. `:182` says P0 "checks that section by reading it", but no AC-0 row (`:201-204`) states a pass condition for the new Orca section. An Orca call in either file passes every gate. SA-2 (`:147`) allows only a mention in the contract file, not a call, and it does not mention HOW-WE-WORK. The gate is correct for commands, skills and agents, so this is Medium: no stated text tells the implementer to write a call, but the gate no longer checks the two files.

**F3. Medium. origin=changed. Workflow is not in the P1 scope, but AC-1.1 requires it.** Candidate `:159` lists P1 fixes to "adversarial, cleanup-audit, index-repo [B1: workflow removed]". Candidate `:92` says workflow's Small fix is "[B1] None". AC-1.1 (`:205`) requires every command in sections 3.1-3.2, which includes workflow, to have a `## Unattended mode` section naming `return-contract.yaml`. Section 2.1 (`:52`) says a changed command gains that section. An implementer who follows P1 does not touch workflow, and AC-1.1 fails.

**F4. Medium. origin=changed (quotes the changed SA-4 line). cli-eval's wait split is an existing-line change that SA-4 does not allow.** Candidate `:104` says to "split the eval wait into waits of at most 4 minutes (WC-10)". `:149` (SA-4) lists the permitted existing-line changes and omits it. AC-C5 (`:186`) then fails any deletion of an existing line that lacks a named defect fix. This is the round-1 M6 point, still present.

**F5. Medium. origin=changed (quotes candidate `:204`). AC-0.4 claims a check that step 5 does not run.** `:204` says "verified in the step-5 transcript". Step 5 (`:194`) searches only for `AskUserQuestion`. This is round-1 M5, still present. The no-wrapper rule (WC-7, `:65`) has no pass condition.

**F6. Medium. origin=changed (quotes candidate `:204`). AC-0.4 step 3 has no rule for `question` or `escalation`.** Step 3 (`:192`) waits for `worker_done` and also returns `question` and `escalation`. `:204` now says step 3 passes "when exactly one `worker_done` arrives", but no rule says what the coordinator does with a question, so a P0 run can stall without failing or passing. The `check` types are round-1's citation `CAPS:63`, which was not re-read here. This is round-1 M7, now tied to the changed line.

**F7. Minor. origin=changed. WC-4's title still says "known before dispatch" while the same paragraph carves workflow out of that rule.** Candidate `:62`. The body is explicit, so this is a note.

**F8. Minor. origin=changed. The AC-C1 block breaks the Section 7.1 table.** Candidate `:172-182` puts prose and a code block between the table's rows, so AC-C2 to AC-C5 (`:183-186`) no longer render as table rows. The text is intact. Cosmetic only.

## Carried findings (origin=unchanged; minor notes unless they quote a changed line)

These round-1 findings sit on lines this revision did not change, and none quotes a changed line, so they are minor notes here:
- Round-1 M1: the gate-branch and resume-without-state rules in WC-2, WC-3 and WC-6 (`:60-61`, `:64`).
- Round-1 M2: tool-permission prompts in a worker are not addressed (`:22`, `:60`).
- Round-1 M3: E4 states "not counted by Orca's nesting limit" more firmly than `CAPS:155` allows (`:24`).
- Round-1 M4: WC-11 conflicts with the fixed default outputs of cleanup-audit, index-repo and init-lite (`:69`, `:85-87`).
- Round-1 M8: no rule covers a missing `~/.claude/WORKER-CONTRACT.md` (`:52`).

## Guard Condition Boundary Table (changed guards only)

Triggered: the changed lines carry outcome, output-path and gate guards (WC-4, section 2.3, section 3, AC-C1, AC-0.4). Focus is requirements and architecture, so the correctness-only State Variable Registry is not required.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-4 carve-out (no output-directory flag) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62` | Zero/Empty | `/sc:workflow --handoff none`, no `--output-dir`, no package yet | true | pre-creation STOP writes no contract; WC-5 maps it to `failed` (`:92`) | OK |
| WC-4 output directory | same, `:62` | Typical | `--output <dir>` on adversarial | false | `<output>/return-contract.yaml` (`:83`) | OK |
| WC-4 output directory vs spec-panel row | same, `:62`; `:120` | Sentinel: `--output` is file-valued in the command | `--output <file>` and `--report-dir <dir>` both present | true | `:120` says "report path"; `:62` says directory | GAP (F1) |
| WC-4 pre-creation STOP | same, `:62`; `:92` | Legitimate Edge Case | STOP before package creation | true | no contract; `failed` (WC-5) | OK |
| AC-C1 exemption, contract file | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:179` | Legitimate Edge Case: a call inside WORKER-CONTRACT.md | `orca orchestration ask` in that file | true (excluded) | the gate is silent | GAP (F2) |
| AC-C1 exemption, HOW-WE-WORK | same, `:179`, `:182` | Zero/Empty: new Orca section has no check | section content | true (excluded) | P0 "checks by reading", no pass condition | GAP (F2) |
| AC-C1 pattern | same, `:177` | Typical: a command calls `orca orchestration task-create` | match | true (fails gate) | gate fails, as SA-2 requires | OK (piped test) |
| AC-0.4 step 3, no report | same, `:204`, `:192` | Zero/Empty: command writes no report | no report file | n/a | step 3 cannot pass; P0 reopens section 1 | OK |
| AC-0.4 step 3, question first | same, `:192`, `:204` | Sentinel: `question` arrives before `worker_done` | `check --wait` returns `question` | true | no reply rule (F6) | GAP (F6) |

FR-8: each GAP row above is a changed-line finding (F1, F2, F6); none is blocking under the grading rule, because each needs a further assumption. FR-9 (blank behavior): none. FR-10: the table covers the changed guards only, as review-loop item 5 requires.

Pipeline Dimensional Analysis: not triggered. No changed line adds a stage whose item count changes.

## Follow-up candidates (Medium and minor; not blocking)

For the session that ran the review, not for this worker: review-loop item 3 asks the user once per loop whether to open an issue for these. No issue is created without the user's answer.

- Medium: F1, F2, F3, F4, F5, F6.
- Minor: F7, F8, and the five carried notes (round-1 M1, M2, M3, M4, M8).

## Summary

Prior blockers B1-B4 are all resolved, and no open blocking finding remains. Six Medium findings are follow-up candidates: the spec-panel contract-path naming (F1), the AC-C1 whole-file exemptions (F2), workflow's missing P1 scope (F3), the cli-eval wait split not in SA-4 (F4), AC-0.4's unchecked step-5 claim (F5), and the missing reply rule for step 3 (F6).

scoped PASS: changed lines + prior blockers

Reviser brief: none. No blocking finding id is open, so the reviser has no brief.

verdict: PASS

review: 2 of 3

# /sc:spec-panel critique report, round 2 (re-review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Prompt: RE-REVIEW prompt, read in full from the sandbox home copy of `~/.claude/rules/prompts/document_review_loop_prompts.md` (`prompts file`, lines 38-51).
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `e1f78b891d8bb255eebfc49ad5aa8456501e35c3ff87d61c58e99699e8350b62`.
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. This is the text round 1 reviewed (`review/round1.md:7`).
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `09fb3f4038a6159865e17647470eaad8730835aa9cf16c0daf98dc81f5bfcda9`, header `review: 1 of 3` (`review/round1.md:1`). This report is therefore `review: 2 of 3`.
- Reviewer model: claude-haiku-5-5 (Haiku 5.5), fresh context. The prior report was read as data.
- rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` in the sandbox home exists. Fix-cycle steps 1-5 could not be read, so the command's Review Loop rules stand alone.
- Mode: re-review only. Nothing edited. Only this file was written.

## Coverage and verification limits

- Read in full: the candidate (`specs/orca-worker-contract-spec.md:1-286`), the baseline (`specs/history/spec-v1.md:1-286`), the prior report (`review/round1.md:1-203`), `README.md:1-39`, and the sandbox copy of `command.md` (review rules `:256-265`, unattended mode `:455-465`).
- Inventory citations used: `inventory/commands-a.md:35`, `inventory/commands-b.md:49,182,272`, `inventory/orca-capabilities.md:34,72-79`.
- The sandbox copy of `command.md:459-461` was used only to check the spec-panel flag name. It is the command definition given to this worker, not a repo file.
- UNVERIFIED: every citation outside `.dev/orca-command-refactor/` (for example `src/superclaude/...`, `cmd/spec-panel.md`, `tests/...`, `.dev/evals/...`). None is in the workspace. A finding that depends on one says so.
- Line numbers are the same in baseline and candidate, because `diff -w` shows no change in line count.

## Step 1: evidence block

Command: `diff -w BASELINE CANDIDATE`. Roles are fixed: BASELINE is `spec-v1.md`, CANDIDATE is `orca-worker-contract-spec.md`.

BEFORE (baseline), lines starting `<`:

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
< | SA-3 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. A standalone default run writes the same files it writes today. | A new file appearing in a person's working tree is a visible change. | Section 3 rows that add a report path |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate), lines starting `>`:

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` into the directory the brief names for it: its directory flag (`--output-dir`, or the command's own, for example spec-panel's `--report-dir`, UNVERIFIED here), or, when its only output flag names a file (init-lite and tdd `--output <file>`), the directory of that file. A run whose brief omits that flag is refused before any work and writes nothing, so WC-5 maps the missing report to `failed`. A §3 row may name a sub-path (adversarial, §3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Each Dispatch writes under the directory its brief names for it, and each `--retry-of` gets a fresh one (WC-6). Commands with a fixed output path (index-repo, cleanup-audit) are serialised by the coordinator (§2.3) until §3 gives them a per-run path; init-lite gets a fresh `--output` per Dispatch. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`). The coordinator never dispatches two Tasks that write the same fixed path at once; it orders them with `--deps` (WC-11).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `return-contract.yaml`, in the directory WC-4 names. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | Add a per-run output directory flag, so the report path is known and two runs in one worktree do not share `PROJECT_INDEX.md` (WC-4, WC-11) (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>`, a fresh file per Dispatch including each retry (WC-6, WC-11); its contract lands beside it (WC-4) | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report; the fresh path avoids that | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | tdd | a precise component prompt, not a bare topic; `--output <file>` (its contract lands beside it, WC-4) | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Under `--unattended` only, write the contract for pre-creation STOPs too (WC-4 "every outcome"; SA-3) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add the directory flag the command's unattended mode names (`--report-dir` per the round-1 review, UNVERIFIED here: `INV-B:182` records no output flag today); contract at `<report-dir>/return-contract.yaml` (WC-4) | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
> | SA-3 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. A standalone default run writes the same files it writes today, with two named exceptions: the adversarial contract's fixed name (§3.1) changes the path of a file a standalone run already writes (`INV-A:35`), and the workflow pre-creation STOP contract is written only under `--unattended` (§3.1). | A new file appearing in a person's working tree is a visible change. | Section 3 rows that add a report path |
> | AC-C1 | `grep -rnE -e '\borca(-ide)?[[:space:]]+orchestration\b' -e '\borca(-ide)?[[:space:]]+worktree\b' -e '\borca(-ide)?[[:space:]]+terminal\b' -e '\borca(-ide)?[[:space:]]+agent\b' --exclude-dir=ccsession-tag --exclude=WORKER-CONTRACT.md src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core` | prints nothing; the HOW-WE-WORK Orca section must name no `orca` command, so this check covers it (SA-2, WC-8) |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with two P0 substitutes: in step 3 the report path is the file the command already writes and step 4 checks (troubleshoot `REPORT.md`, `INV-B:49`; workflow `return-contract.yaml`, `INV-B:52`; adversarial's contract, `INV-A:35,60`), since the WC-4 path arrives in P1; and step 4 runs only `test -s`, since the YAML assertion applies from P1 (`REPORT.md` is Markdown). Record the results in the phase report; a failure here reopens section 1 |
```

Changed lines by location (candidate line numbers): WC-4 `:62`, WC-11 `:69`, §2.3 `:73`, §3 intro `:76`, §3.1 index-repo `:86`, init-lite `:87`, tdd `:90`, workflow `:92`, §3.2 spec-panel `:120`, SA-3 `:148`, AC-C1 `:172`, AC-0.4 `:194`.

## Self-check (run before the verdict)

`grep -nF` was run for each quoted line. Every AFTER quote was found in CANDIDATE (for example WC-4 at `:62`, §2.3 at `:73`, index-repo at `:86`, spec-panel at `:120`, SA-3 at `:148`, AC-0.4 at `:194`). Every BEFORE quote was found in BASELINE (WC-4 at `:62`, adversarial row at `:83`, SA-3 at `:148`). Roles were not swapped.

## Prior blocking findings (F-01 to F-06)

| id | status | evidence and residual |
|---|---|---|
| F-01 | resolved | WC-4 (`:62`) now names the directory of a file-valued output and the missing-flag refusal. init-lite (`:87`) and tdd (`:90`) say the contract lands beside the file. Residual: R2-02, R2-03 (Medium). |
| F-02 | resolved | WC-4 (`:62`) names `--report-dir` for spec-panel, and §3.2 (`:120`) gives `<report-dir>/return-contract.yaml`. The name matches `command.md:459-461`. Residual: R2-05 (Medium). |
| F-03 | open | SA-3 (`:148`) now lists exceptions, but SA-1 (`:146`, unchanged) still says no output path changes without `--unattended`, and the adversarial row (`:83`, unchanged) still moves the standalone contract path. See the F-03 entry below. |
| F-04 | resolved for the defect named in round 1 | AC-0.4 (`:194`) now substitutes the report path in step 3 and the check in step 4. The outcome clause of step 3 (`:182`) is still not substituted. See R2-01. |
| F-05 | resolved | AC-C1 (`:172`) uses one `-e` per alternative with no `\|` inside the pattern, excludes `WORKER-CONTRACT.md` by name, and excludes `ccsession-tag` with `--exclude-dir`. The pattern is plain ERE. |
| F-06 | resolved for the two named cases | WC-11 (`:69`) and §2.3 (`:73`) serialise Tasks that write a fixed path, and init-lite (`:87`) gets a fresh `--output` per Dispatch including retries. Residual: R2-04 (Medium). |

No prior blocking finding is regressed.

### F-03 (blocking, open)

- **Issue.** The contradiction moved to a new place. SA-3 (`:148`) now agrees with §3.1, but SA-1 (`:146`) does not. SA-1 says that without `--unattended`, every "output path ... stays as it is today" and names no exception. The adversarial row (`:83`) changes the standalone contract path to `<output>/adversarial/return-contract.yaml`. The inventory says real runs already wrote the contract at a varying path, sometimes `.../adversarial/adversarial/return-contract.yaml` (`inventory/commands-a.md:35`).
- **Grading check.** An implementer who follows SA-1 as written leaves a standalone adversarial run's contract path unchanged. An implementer who follows `:83` changes it. The two texts hold together only if SA-1 yields to SA-3, and SA-1 does not say so. Blocking by contradiction, the same rule round 1 applied to F-03.
- **Recommendation.** Name the adversarial exception in SA-1 as well as SA-3, or gate the fixed name behind `--unattended`, so SA-1, SA-3 and `:83` list the same set.

### R2-01 (blocking, new; origin=changed)

- **Issue.** AC-0.4 step 3 (`:182`) requires that the worker's `--outcome` "matches the contract's `status` under WC-5". In the P0 troubleshoot run the report is `REPORT.md` (`:194`, which calls it Markdown; `inventory/commands-b.md:49`), and it has no `status` field. The new substitutes at `:194` cover the report path and step 4 only, so the outcome clause is left in place. The change is on `:194`, and the clause it leaves is `:182`.
- **Grading check.** An implementer who follows AC-0.4 step 3 as written looks for a contract `status` in the troubleshoot run, finds none, and can mark the step neither passed nor failed. Blocking, because the acceptance criterion cannot pass as written. WC-5 (`:63`) maps a report that "says failed" to `failed`, and the spec also says failure must not be "encoded only in prose" (`CAPS:73`), so reading `REPORT.md` for a verdict is a guess.
- **Recommendation.** In `:194`, state the outcome source for a P0 Markdown report, or waive the outcome clause for troubleshoot in P0 by name.

## Findings on changed lines (origin=changed), not blocking

### R2-02 (Medium): "written on every outcome" conflicts with "refused ... writes nothing"

- WC-4 (`:62`) says the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists", and a few clauses later says "a run whose brief omits that flag is refused before any work and writes nothing".
- Grading check: for a run with no directory flag, the two sentences give different results. An implementer must pick the more specific one, which is a guess, so Medium.
- Recommendation: say that a refusal before the directory is known writes no contract, and that WC-5 maps it to `failed`.

### R2-03 (Medium): a fixed contract name in a directory shared by two dispatches

- WC-4 (`:62`), init-lite (`:87`) and tdd (`:90`) put `return-contract.yaml` beside the output file. Two dispatches whose files share a directory, for example two init-lite runs with fresh files under `.dev/superclaude/`, write the same contract name. WC-11 (`:69`) says two workers must never write the same file.
- §2.3 (`:73`) serialises Tasks that write "the same fixed path". A coordinator that reads the contract name as a fixed path is safe. The spec does not say so, so the outcome needs an assumption, which makes it Medium. It becomes blocking if read as excluding the contract name.
- Recommendation: name the contract after its output (for example `<output-stem>.return-contract.yaml`), or state in §2.3 that the contract name counts as a fixed path.

### R2-04 (Medium): a sequential retry of a fixed-path command

- WC-11 (`:69`) and §2.3 (`:73`) serialise concurrent Tasks only. index-repo (`:86`, fixed `PROJECT_INDEX.md` until P1) and cleanup-audit (§3.1 fixed output directory) have no per-run path. A `--retry-of` dispatch (WC-6, `:64`) runs after the first attempt, not beside it, and so overwrites that attempt's file. WC-6 says a retry "must not corrupt the first attempt's output".
- Grading check: the outcome is an overwrite of a regenerable file, and whether index-repo's `mode=update` counts as resume is a guess. Medium.
- Recommendation: state that a retry of a fixed-path command is not dispatched before §3 gives it a per-run path.

### R2-05 (Medium): the spec-panel row says "add" a flag the sandbox command already defines

- §3.2 (`:120`) says "add the directory flag the command's unattended mode names (`--report-dir` ...; UNVERIFIED here: `inventory/commands-b.md:182` records no output flag today)". The sandbox copy of the command defines `--report-dir` in its unattended mode (`command.md:459-461`), so "add" can be read as adding a second flag. The repo's `cmd/spec-panel.md` is not in the workspace, so the conflict between `inventory/commands-b.md:182` and `command.md` cannot be settled here.
- Recommendation: say "use `--report-dir` if `cmd/spec-panel.md` already has it; add it if not", and name the check.

### m-04 (minor): SA-3 lists a second exception that is not an exception

- SA-3 (`:148`) lists the workflow pre-creation STOP contract as an exception, but that contract is written only under `--unattended`, which SA-3's first clause already allows. Harmless. Remove it or say so.

### Checked, no finding

- AC-C1 (`:172`): the pattern is valid ERE, the `-e` alternatives and the two excludes are as the text says, and the HOW-WE-WORK section is covered as stated.
- §2.3 (`:73`): `--deps` exists on `task-create` and `worker-start` (`inventory/orca-capabilities.md:34`), so the ordering rule names a real flag.
- SA-3's adversarial exception is backed by `inventory/commands-a.md:35`. The workflow contract's pre-creation gap is backed by `inventory/commands-b.md:272`.

## Guard Condition Boundary Table (changed guards only)

Triggered by the changed contract-path, retry and outcome rules. Pipeline Dimensional Analysis is not triggered: the candidate has no multi-stage count flow, as in round 1.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract path | WC-4 `:62` | Zero/Empty: directory flag absent | none | refused, no directory | "refused ... writes nothing" against "written ... including stops" | GAP (R2-02, Medium) |
| contract path | WC-4 `:62`, `:87`, `:90` | Typical: file-valued `--output <file>` | `<file>` | contract in the file's directory | stated | OK |
| contract path | WC-4 `:62`, `:87`, `:90` | Legitimate edge: two dispatches, one directory | two files, one dir | same contract name | §2.3 `:73` covers it only if the name counts as fixed | GAP (R2-03, Medium) |
| contract path | `:83` (unchanged), SA-1 `:146`, SA-3 `:148` | Legitimate edge: standalone adversarial run | no `--unattended` | path moves | SA-1 forbids it; SA-3 permits it | GAP (F-03, blocking) |
| retry | WC-6 `:64`, WC-11 `:69` | Legitimate edge: retry of index-repo or cleanup-audit | fixed path with a prior file | overwrite | no rule before §3 gives a per-run path | GAP (R2-04, Medium) |
| outcome | AC-0.4 step 3 `:182`, `:194` | Typical: troubleshoot `REPORT.md` | no `status` field | cannot be evaluated | not substituted | GAP (R2-01, blocking) |

## Summary

- Prior blocking: F-01, F-02, F-04, F-05 and F-06 resolved for the defects named; F-03 open.
- New blocking: R2-01.
- Medium: R2-02, R2-03, R2-04, R2-05. Minor: m-04.
- Open blocking findings: F-03 and R2-01. Verdict FAIL.
- Coverage line: not a scoped PASS, because blocking findings are open. Scope reviewed: the 12 changed locations above plus prior blockers F-01 to F-06.

## Follow-up candidates (Medium and minor, not blocking)

R2-02, R2-03, R2-04, R2-05, m-04. Round 1 items F-07 to F-15 and m-01 to m-03 remain follow-up candidates and were not re-graded. The session that ran this review asks the user once whether to open an issue for them; none is created without the user's answer.

## Decisions made by this reviewer

| Decision | Options | Rationale |
|---|---|---|
| Review number | `review: 2 of 3` | Prior header `review: 1 of 3` plus 1 (prompt line 48; `command.md:261`). |
| F-03 | resolved in SA-3 / open | SA-1 (`:146`) and the adversarial row (`:83`) are unchanged and still conflict. Open by the rule round 1 applied. |
| R2-01 | Medium / blocking | The step cannot pass as written, and the grading sentence holds with no assumption. Blocking. |
| R2-03 | Medium / blocking | Blocking only if the contract name is read as excluded from §2.3. Medium. |
| Ids | prior ids kept; new `R2-nn`, `m-04` | Each finding keeps its prior id; new findings get new ids, per the command's re-review output rule. |

## Reviser brief

Blocking finding ids: F-03, R2-01.

Restated rule (review-loop bullet 6): the reviser revises only text a blocking finding names; adds no rule, mechanism or section no blocking finding calls for; cites the finding id on each added paragraph or table; prefers deleting or narrowing to adding; and reports the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited.

verdict: FAIL

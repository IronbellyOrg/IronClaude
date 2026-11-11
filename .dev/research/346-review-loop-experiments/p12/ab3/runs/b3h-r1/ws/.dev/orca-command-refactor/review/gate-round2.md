review: 2 of 3

# Gate-loop re-review: Orca worker-contract spec (critique, focus: requirements, architecture)

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), SHA-256 `060d1fb59804955f83e92638dceec3c2655f94b7c59c399f7112f8a8c9bfd1d2`
- Baseline: `.dev/orca-command-refactor/specs/history/spec-g.md` (285 lines), SHA-256 `2a0ba05dc4158ae8fc6c4b9c265ce2ded840533c29031835d61d7c548122ac84`. This is the same hash as the candidate that `review/gate.md` reviewed (its line 6), so the baseline is the text the gate review saw.
- Prior: `.dev/orca-command-refactor/review/gate.md` (`review: 1 of 3`, `verdict: FAIL`), SHA-256 `3a1c59b1ce30f67994be65dea39b8eef62e0b783d56f786d77d196438763967e`.
- Prompt: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). This is the gate loop: one REVISE pass on B-1 to B-5, then this RE-REVIEW with `gate.md` as PRIOR. N = 1 + 1 = 2.
- Reviewer model: claude-haiku-5-5.
- Not in this sandbox: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md`. The Review Loop rules in `command.md` stand alone (Review Loop step 5). `~/.claude/WORKER-CONTRACT.md` is also absent; it applies only under `--unattended`, which this run does not pass.
- The revision pass is not visible in the sandbox. This report checks the candidate as found, against the baseline and the prior blocking ids.

## Coverage

- Read in full: `command.md`, the RE-REVIEW and GATE prompts, `README.md`, the candidate, `review/gate.md`, and the baseline-to-candidate diff.
- Step 1 (evidence block below): `diff -w` gives 9 changed-line pairs, at candidate lines 61, 62, 73, 88, 90, 91, 92, 109 and 195. Self-check: `grep -nF` finds every AFTER line in the candidate and every BEFORE line in the baseline, so the roles were not swapped.
- Inventory citations checked on changed lines: `inventory/commands-b.md:49,52,112,242` were read. Lines 112 and 242 give timestamped defaults and no output flag. Citations to `src/`, `~/.claude/`, `.dev/codegraph-migration/`, `.dev/evals/` and Orca `CAPS:` lines are not in the workspace and are UNVERIFIED; none of them is counted against the spec.
- Scope: prior blocking ids B-1 to B-5 (all re-checked), findings on lines changed against the baseline, and guards on those lines. Medium and minor findings of `gate.md` (F-1 to F-7, N-1 to N-6) are not re-graded; their cited lines are unchanged except `:62` (cited by F-7), and F-7 still holds.
- Pipeline Dimensional Analysis: not triggered (no count-changing flow, unchanged).
- Mandatory artifact: Guard Condition Boundary Table, for guards on changed lines (below).

## Step 1 evidence block (`diff -w` baseline to candidate)

BEFORE (baseline), lines starting with `<`:

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` into the directory the brief names for it: its directory flag (`--output-dir`, or the command's own, for example spec-panel's `--report-dir`, UNVERIFIED here), or, when its only output flag names a file (init-lite and tdd `--output <file>`), the directory of that file. A run whose brief omits that flag is refused before any work and writes nothing, so WC-5 maps the missing report to `failed`. A §3 row may name a sub-path (adversarial, §3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`). The coordinator never dispatches two Tasks that write the same fixed path at once; it orders them with `--deps` (WC-11).
< | reflect | no `--remediate`; `--no-promote` when the coordinator owns folder moves | `<output>/return-contract.yaml` | Fresh dir (`--promote-resume` covers promotion only) | Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt (P2) | `sk/sc-reflect-protocol/SKILL.md:659`; `sk/sc-reflect-protocol/refs/remediation-handoff.md:228,239-247`; `cmd/reflect.md:101,110`; `INV-B:36,107-115` |
< | tdd | a precise component prompt, not a bare topic; `--output <file>` (its contract lands beside it, WC-4) | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Under `--unattended` only, write the contract for pre-creation STOPs too (WC-4 "every outcome"; SA-3) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | implement | on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger and the contract as blocked, carrying the Ruling question; the Ruling rule itself is unchanged (see open decision D2) | contract beside the ledger `progress.md` | `--resume` (implicit when a ledger matches) | none on the happy path | `sk/sc-implement-protocol/refs/qa.md:231-238`; `sk/sc-implement-protocol/SKILL.md:35`; `cmd/implement.md:57-58,74`; `INV-A:51,66` | P4 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate), lines starting with `>`:

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. This never applies to the `/sc:implement` Ruling halt (`E-HALT-QA`, `E-NO-RULING`): that halt is recorded and stops, with no `ask` (B-1; D2(a)). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` into the directory the brief names for it: its directory flag (`--output-dir`, or the command's own, for example spec-panel's `--report-dir`, UNVERIFIED here), or, when its only output flag names a file (init-lite and tdd `--output <file>`), `<file-stem>.return-contract.yaml` in that file's directory (B-4). A run whose brief omits that flag is refused before any work and writes nothing, so WC-5 maps the missing report to `failed`. A §3 row may name a sub-path (adversarial, §3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` (from P1 on; P0 briefs omit it, section 6; B-2) and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`). The coordinator never dispatches two Tasks that write the same fixed path at once; it orders them with `--deps` (WC-11). Two Tasks may share a directory only when their contract names differ (file-output commands, WC-4); each directory-output Task gets its own directory (B-4).
> | reflect | `--output <dir>` (the `<output>` directory, `INV-B:112`; B-3); no `--remediate`; `--no-promote` when the coordinator owns folder moves | `<output>/return-contract.yaml` | Fresh dir (`--promote-resume` covers promotion only) | Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt; the timestamped default `.dev/reflect/<mode>-<slug>-<ts>/` (`INV-B:112`) is replaced by the brief's `--output` (B-3) (P2) | `sk/sc-reflect-protocol/SKILL.md:659`; `sk/sc-reflect-protocol/refs/remediation-handoff.md:228,239-247`; `cmd/reflect.md:101,110`; `INV-B:36,107-115` |
> | tdd | a precise component prompt, not a bare topic; `--output <file>` (a fresh file per Dispatch, WC-11; its contract is `<file-stem>.return-contract.yaml` beside it, WC-4; B-4) | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | troubleshoot | no `--fix`; `--output <dir>` (the default `.dev/troubleshoot/<slug>-<timestamp>/` has no fixed path, `INV-B:242`; B-3) | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked; the timestamped default is replaced by the brief's `--output`, and the flag is added if absent (B-3) (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
> | workflow | `--handoff none`; `--output <dir>` (added in P1; no directory flag today, `INV-B:52`; B-3) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Under `--unattended` only, write the contract for pre-creation STOPs too (WC-4 "every outcome"; SA-3); `--output <dir>` puts the package and contract where the brief names (B-3) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | implement | on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger and the contract as blocked, carrying the Ruling question; the Ruling rule itself is unchanged; no `ask` is sent for this halt (B-1; see open decision D2) | contract beside the ledger `progress.md` | `--resume` (implicit when a ledger matches) | none on the happy path | `sk/sc-implement-protocol/refs/qa.md:231-238`; `sk/sc-implement-protocol/SKILL.md:35`; `cmd/implement.md:57-58,74`; `INV-A:51,66` | P4 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command, and not `load` (it writes no contract, its section 3.2 row; B-5), has one | passes |
```

## Prior blocking findings (from `review/gate.md`)

| ID | Status | Evidence against the AFTER text |
|---|---|---|
| B-1 | resolved | WC-3 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:61`) now excludes the Ruling halt (`E-HALT-QA`, `E-NO-RULING`). The implement row (`:109`) says no `ask` is sent for this halt. D2(a) (`:234`) is unchanged: the worker stops and ends `failed`. WC-5 (`:63`) maps a `blocked` report to `--outcome failed`, so the row's "contract as blocked" and D2(a)'s "ends failed" agree. Residual: C2-M1. |
| B-2 | resolved | Section 2.3 (`:73`) now requires `--unattended` from P1 on. P1 (`:159`) introduces the flag, and AC-0.4 (`:194`) runs P0 without it. Cross-reference residue: C2-m1. |
| B-3 | resolved | reflect (`:88`), troubleshoot (`:91`) and workflow (`:92`) now name a directory flag, and the timestamped defaults are replaced under `--unattended`. Whether the reflect and troubleshoot flags exist yet is C2-M2. |
| B-4 | resolved | WC-4 (`:62`) and the tdd row (`:90`) name `<file-stem>.return-contract.yaml`. Section 2.3 (`:73`) allows a shared directory only when contract names differ, and gives each directory-output Task its own directory. Residual: C2-m2. |
| B-5 | resolved | AC-1.1 (`:195`) excludes `load`, matching the load row (`:112`, "Report (WC-4): none") and the Decision (`:265`). |

No prior blocking finding is open, regressed or unmatched. Every prior id keeps its gate.md id.

## Findings on lines changed against the baseline (origin=changed)

### Medium (not blocking)

**C2-M1 (origin=changed, `:61`).** WC-3 now says "This never applies to the `/sc:implement` Ruling halt" with no condition. D2 option (b) (`:235`) would have the coordinator answer the worker's `ask` for that same halt. An implementer who follows `:61` as written builds no relay path for the Ruling halt; if the user picks D2(b), that build is wrong, and `:61` forbids the option. The line cites D2(a), so the outcome depends on the user's D2 answer, which is still open. The sentence holds on the recommended path, so this is Medium, not blocking. Recommendation: "unless D2 option (b) is chosen".

**C2-M2 (origin=changed, `:79`, `:88`, `:91`, `:92`).** The section 3.1 header (`:79`) says these commands "run as workers now if the brief uses the stated flags". The "Brief must pass" column of reflect (`:88`) and troubleshoot (`:91`) names `--output <dir>`. The inventory records no output flag for either: `inventory/commands-b.md:112` gives the default `.dev/reflect/<mode>-<slug>-<ts>/`, and `:242` gives `.dev/troubleshoot/<slug>-<timestamp>/`. Both are defaults, not flags. Troubleshoot's flag is added only in P2 (`:91`, "the flag is added if absent"), and the reflect row (`:88`) names no addition at all. Workflow (`:92`) discloses "added in P1". So "run now" cannot hold for three rows that the table lists as ready. No check fails: P0 (`:158`, AC-0.4 `:194`) and P1 (AC-1.2 `:196`) never pass `--output` to reflect or troubleshoot. Recommendation: move reflect, troubleshoot and workflow out of 3.1, or state in each Brief cell the phase in which its flag appears.

### Minor (notes)

**C2-m1 (origin=changed, `:73`).** The phrase "P0 briefs omit it, section 6" points to section 6. The P0 row (`:158`) does not say that P0 omits `--unattended`; the omission follows from the P1 row (`:159`) introducing the flag. Recommendation: state the omission in `:158`.

**C2-m2 (origin=changed, `:62`, `:73`, `:90`).** The file-output contract name is `<file-stem>.return-contract.yaml`, so `a.md` and `a.txt` in one directory both give `a.return-contract.yaml`. Section 2.3 (`:73`) stops sharing when names differ, so a coordinator that checks is protected. The naming rule itself still produces the collision. Recommendation: include the extension or the dispatch id in the name.

## Guard Condition Boundary Table (guards on changed lines)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-3 ask gate | `spec:61`, `:109` | Ruling halt (`E-HALT-QA`) with preamble | halt | stop, no `ask` | `:61` and `:109`, with D2(a) (`:234`) | OK on D2(a); GAP under D2(b) (C2-M1) |
| WC-3 ask gate | `spec:61` | Ordinary blocked gate with preamble | blocked gate | ask once, then re-invoke | `:61` | OK |
| WC-4 directory | `spec:62`, `:88`, `:91`, `:92` | Missing directory flag (reflect, troubleshoot, workflow) | no flag in brief | refused before work | `:62` | OK in text; flag not yet present for reflect and troubleshoot (C2-M2) |
| WC-4 file contract name | `spec:62`, `:73`, `:90` | Same stem, different extension, same directory | `a.md`, `a.txt` | same contract name | `:73` stops sharing only when names differ | GAP, Minor (C2-m2) |
| WC-4 / section 2.3 shared directory | `spec:73` | Two directory-output Tasks | own directories | distinct contracts | `:73` | OK |
| implement halt outcome | `spec:109`, `:63`, `:234` | `E-NO-RULING` | halt | contract `blocked`, Orca outcome `failed` | WC-5 (`:63`) maps `blocked` to `failed` | OK |
| AC-1.1 load exclusion | `spec:195`, `:112`, `:265` | `load` in the unattended contract check | no contract | excluded | `:195` excludes `load` | OK |
| section 2.3 cross-reference | `spec:73`, `:158` | P0 brief, flag omission | P0 run | no `--unattended` | section 6 (`:158`) does not state it | GAP, Minor (C2-m1) |

## Re-review coverage line

scoped PASS: changed lines + prior blockers

## Follow-up candidates (not blocking)

The reviewing session asks the user once whether to open an issue for these. None is created here.

- Medium: C2-M1, C2-M2.
- Minor: C2-m1, C2-m2.
- Carried from `gate.md`, not re-graded: Medium F-1 to F-7; minor N-1 to N-6. The N-2 identifier `R2-01` is still undefined at `spec:182`.

## Reviser brief

Blocking finding ids: none. Nothing is open, so no REVISE pass is due and the gate loop ends here. Revise only text a blocking finding names; none is named.

verdict: PASS

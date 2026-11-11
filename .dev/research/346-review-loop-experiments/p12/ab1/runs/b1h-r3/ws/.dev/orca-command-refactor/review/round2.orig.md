review: 2 of 3

# Re-review round 2: orca-worker-contract-spec.md

Command: `/sc:spec-panel`, `--mode critique`, `--focus requirements,architecture`, `--re-review`, `--baseline`.

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `e28114855e5685eb7f3f2e2652a756ffaac57ed4c9ffb0b7423b91d78a8e8d19`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior: `.dev/orca-command-refactor/review/round1.md` sha256 `f1f20b27c9fed859e67e07607c805123e80b5314bd0ab0a8d12b832fbbe2202c` (header `review: 1 of 3`, verdict FAIL)
- review number: N = 1 + 1 = 2
- reviewer model: claude-haiku-5-5 (Haiku 5.5), one fresh-context reviewer

Notes on inputs:

- `round1.md:5` records the round-1 candidate as sha256 `d3cdbe57...`. That equals the baseline hash here, so round 1 reviewed the text now stored as `spec-v1.md`.
- The RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` was read in full (sandbox home).
- `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are not in this sandbox. They were unread, so the Process of the Fix Cycle steps 1-5 were not applied; the Review Loop rules in `command.md` stand alone.
- No `--unattended` in the brief, so no worker contract is read or written.
- Evidence checkable here: the inventories under `.dev/orca-command-refactor/inventory/`, `round1.md`, `spec-v1.md`, the candidate, and `command.md` (the `/sc:spec-panel` definition supplied in this sandbox, cited as `command.md:N`). Any citation to `src/superclaude/`, `plugins/`, `.claude/` or other files not listed here is UNVERIFIED.

## Step 1: evidence block

Roles fixed: BASELINE = `spec-v1.md`, CANDIDATE = `orca-worker-contract-spec.md`, PRIOR = `round1.md`.

Output of `diff -w BASELINE CANDIDATE`. Lines starting `<` are BEFORE (baseline). Lines starting `>` are AFTER (candidate).

```diff
62,63c62,63
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`; `verdict` is added when the report states one, for example an audit's PASS or FAIL (M3). It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Exception: `/sc:load` writes no contract (section 3.2 load row; M8). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when `status` is `failed` or `blocked`, when `status` is missing or is not one of the four values, or when no report exists; `--outcome succeeded` only when `status` is `succeeded` or `partial`. An audit whose `verdict` is FAIL still succeeds as a run, and the coordinator gates dependent Tasks on `verdict`, not on the outcome (M3). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77`. Revised: M3, M4. |
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1), except `/sc:load`, which writes no contract and gets no report file (M8). Phase numbers refer to section 6.
83c83
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
---
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/return-contract.yaml`, the WC-4 path, when `--output` is passed (P1) [M4] | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none`; `--output <dir>` from P1 | `.dev/tasks/to-do/<id>/return-contract.yaml` (standalone) | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome"); under `--unattended`, write it to `<output-dir>/return-contract.yaml` (WC-4) and keep the package path standalone (SA-3) (P1) [M10] | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
105c105
< | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
---
> | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract at `<output-dir>/return-contract.yaml` (WC-4; fields already defined; `--output <dir>` added) [M10] | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
112c112
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
---
> | load | no gate | none: WC-4 exception (M8) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
116c116
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
---
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract at `<output-dir>/return-contract.yaml` (WC-4), naming the generated `claudedocs/research_*.md` path [M10] | fresh file | add `--output <dir>` for the WC-4 path [M10] | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
172c172
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
---
> | AC-C1 | the grep in the block below, after its self-test passes | prints nothing (SA-2, WC-8); pattern revised for M7 |
177a178,184
> AC-C1 (M7). The pattern is kept outside the table, because a table cell turns `\|` into a literal pipe and the alternation would then fail to match. Self-test first: the planted sample must match (count 2).
> 
> ```bash
> printf 'orca orchestration worker-start\norca-ide status --json\n' | grep -ciE '\borca(-ide|-cli)?[[:space:]]+(orchestration|worktree|terminal|agent|status)\b'
> grep -rniE '\borca(-ide|-cli)?[[:space:]]+(orchestration|worktree|terminal|agent|status)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v '^src/superclaude/skills/ccsession-tag/'
> ```
> 
194,195c201,202
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
---
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, where step 3's report path is the one the command writes today. Step 4 is replaced for P0, because the contract arrives in P1: `troubleshoot`: `test -s <dir>/REPORT.md`; `workflow`: read `.dev/tasks/to-do/<id>/return-contract.yaml` and assert only that `status` is one of the four values (no `command` key exists, `INV-B:272`); `adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`). Record the results in the phase report; a failure here reopens section 1 (M6) |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (M8) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
198c205,206
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
---
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names `<output-dir>/return-contract.yaml` (WC-4 path, M4); workflow states the contract is written for pre-creation STOPs |
> | P1 | AC-1.5 | For each P1 row that writes a contract (workflow, adversarial): run with `--unattended --output <dir>`, then `test -s <dir>/return-contract.yaml` | the contract exists at the brief's path (WC-4; M10) |
201c209
< | P2 | AC-2.3 | Happy-path run per P2 command with every required flag in the brief | 7.2 passes with `--outcome succeeded` |
---
> | P2 | AC-2.3 | Happy-path run per P2 command with every required flag in the brief | 7.2 passes with `--outcome succeeded`, and `<dir>/return-contract.yaml` exists at the brief's path (research and cli-portify; M10) |
```

Self-check: each AFTER line was found in CANDIDATE, and each BEFORE line in BASELINE, with `grep -cF` (blank-line matches omitted). All quoted lines matched, so the roles hold.

## Prior blocking findings

Source: the Reviser brief in `round1.md:138-141` lists M3, M4, M6, M7, M8 and M10. The verifier rejected M1, M2, M5, M9, M11 and M12 (`round1.md:81-132`); they are notes in this review, not prior blocking findings.

| Prior id | Status | Evidence in the candidate |
|---|---|---|
| M3 | resolved | WC-4 adds `verdict` (`orca-worker-contract-spec.md:62`). WC-5 maps an audit with a FAIL verdict to a succeeded run and states that the coordinator gates dependent Tasks on `verdict` (`:63`). Residual gaps: F-1. |
| M4 | resolved | M4.a: WC-5 maps missing, empty or unknown `status` to failed (`:63`). M4.b: the adversarial row names `<output>/return-contract.yaml` (`:83`), and AC-1.4 checks it (`:205`). |
| M6 | resolved | AC-0.4 (`:201`) replaces step 4 per command, and the workflow step no longer asserts a `command` key. The step 3 defect on the same line is new: R2-1. |
| M7 | resolved | AC-C1 (table `:172`, code block `:180-183`) uses `-E` with `(orchestration\|worktree\|terminal\|agent\|status)`. I ran the pattern: the planted sample `orca orchestration worker-start` plus `orca-ide status --json` gives count 2; `orca orchestration task-create` matches; the v1 form with a literal `\|` gives 0 matches and exit 1 on `the orca orchestration ask`. |
| M8 | resolved | The `/sc:load` exception is stated in WC-4 (`:62`), the section 3 intro (`:76`), the load row (`:112`) and AC-1.1 (`:202`). Residual gap: F-2. |
| M10 | resolved for the three named rows | Workflow (`:92`), cli-portify (`:105`) and research (`:116`) now name `<output-dir>/return-contract.yaml`, and AC-1.5 (`:206`) and AC-2.3 (`:209`) check it. The same defect in tdd (`:90`) and init-lite (`:87`) is not covered: R2-2. |

None of the six regressed.

## New findings on changed lines

### R2-1 (BLOCKING, origin=changed)

- Quoted: AC-0.4 (`orca-worker-contract-spec.md:201`): "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today". Step 3 (`:189`), which AC-0.4 depends on: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Sentence: An implementer who runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` as written must make step 3's outcome match hold. Troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`), and the contract does not exist before P1 (`:201`), so there is no `status` to match. Step 3 cannot pass, and P0 cannot pass.
- Origin: the step 3 text is unchanged from `spec-v1.md`, so the defect is older. It is counted as changed because it quotes the changed AC-0.4 line (`:201`) that depends on it.
- Experts: Crispin (testability), Wiegers (acceptance criteria).
- Priority: High. Impact: blocks the P0 gate.
- Suggested repair: for commands with no contract in P0, state where the outcome comes from (for example, the command's own report), or remove the outcome match from step 3 for P0.

### R2-2 (BLOCKING, origin=changed)

- Quoted: WC-4 (`orca-worker-contract-spec.md:62`): "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Against it: the tdd row (`:90`) "`--output <file>`" with report "the TDD at `--output`", and the init-lite row (`:87`) "`--output <file>`". AC-2.2 (`:208`) runs `/sc:tdd "auth" --unattended --output <file>` and checks the contract at `test -s <contract>` (step 4, `:190`).
- Sentence: An implementer who follows WC-4 for `/sc:tdd --unattended --output <file>` must write `<output-dir>/return-contract.yaml`. The flag the brief passes is a file, not a directory, so there is no `<output-dir>` for the coordinator to compute. The contract path is undefined, and AC-2.2 step 4 cannot run for tdd. The same holds for init-lite (`:87`).
- Stated texts that contradict: `:62` (the value is a directory) against `:87` and `:90` (the value is a file).
- Origin: `:62` is changed; `:87` and `:90` are unchanged. The conflict is in `spec-v1.md` at the same rows, so it is an older defect newly found in this review. It is the same class as M10, which named three rows and not these two.
- Experts: Fowler (interface contract), Wiegers (traceability).
- Priority: High. Impact: the coordinator cannot read the report for tdd and init-lite under `--unattended`.
- Suggested repair: give tdd and init-lite a directory flag for the contract, or name the contract location in their rows, as M10 did for the other rows.

## Follow-up candidates (Medium and minor; not blocking)

- **F-1 (Medium, origin=changed, `:62-63`).** M3 residual. `verdict` is added "when the report states one" (`:62`), where `round1.md:21` recommended it as required for audit-type commands. No row names the audit commands. The coordinator gate on `verdict` appears only in WC-5, whose owner is "Worker session" (`:63`). It is absent from section 2.3 (`:73`), which lists the coordinator's duties after `worker_done`, and no AC tests it. The text does not say what the gate does when `verdict` is absent.
- **F-2 (Medium, origin=changed, `:62-63`).** The `/sc:load` exemption (`:62`, `:112`) conflicts with WC-5's "no report exists" rule (`:63`). A load run dispatched as its own Task would always send `failed`. The load row says it is not its own Task (`:112`), so this needs misuse to occur.
- **F-3 (Medium, UNVERIFIED, origin=unchanged rows that changed AC-0.4 depends on, `:201`).** AC-0.4 step 4 for workflow asserts that `status` is one of the four values. The inventory lists the existing workflow contract's fields (`status`, `plan_path`, `reflect_report_path`, `commands-b.md:267-275`) but not their values. If today's values differ, the replaced step 4 fails on current output.
- **F-4 (minor, origin=changed, `:206` and `:209`).** AC-1.5 applies to "each P1 row that writes a contract (workflow, adversarial)", and AC-2.3 says "(research and cli-portify; M10)". Several other P1 rows (`:99-111`) also write contracts. §7.2 step 4 (`:190`) runs through AC-1.2 and AC-2.3, so coverage is probably complete, but the parentheticals read as an exhaustive list.
- **F-5 (minor, origin=changed, `:62`).** WC-4 names two flags, `--output` and `--output-dir`, and every row uses `--output`. Implementers may pick either.
- **F-6 (Medium, UNVERIFIED, origin=unchanged row `:120`, bearing on changed `:62`).** The spec-panel row says "add `--output`" and relies on `commands-b.md:43` for "no `--output`". In this sandbox, `command.md:23` already defines `--output <file>`, `command.md:455` already has a `## Unattended mode` section, and `command.md:460` says `--output` is file-valued. That conflicts with the spec's premise and with WC-4's directory meaning. The repo file is not in this sandbox, so the coordinator should check `src/superclaude/commands/spec-panel.md` before R2-2 is revised.
- **F-7 (minor, origin=unchanged `:79`, changed `:92`).** Section 3.1 says the ready-today commands run "if the brief uses the stated flags", but the workflow row requires `--output <dir>` "from P1" (`:92`). The workflow row cannot be "ready today" in that form.
- **F-8 (minor, origin=changed `:83` against `:205`).** The adversarial row writes `<output>/return-contract.yaml`, and AC-1.4 writes `<output-dir>/return-contract.yaml`. Naming drift only.
- **F-9 (minor, origin=unchanged `:158` against changed `:201`).** The P0 smoke list says `/sc:adversarial --output <dir>`, and AC-0.4 says `/sc:adversarial --compare <two files> --depth quick --output <dir>`.

## Noted, unactioned (round-1 VERIFY rejects, carried; not prior blocking)

- **M1.** The roadmap row (`:118`) and save row (`:119`) are unchanged. Still a note.
- **M2.** WC-3 (`:61`) is unchanged. Still a note.
- **M5.** AC-C1 (`:172`) still scans `src/superclaude/core`, so the contract file and the routing-guide Orca section can match. Still a note.
- **M9.** WC-5 (`:63`) now maps missing, empty and unknown status to failed, so the M9 concern is covered by the M4 fix.
- **M11.** WC-6 (`:64`) and section 2.3 (`:73`) are unchanged, and no dispatch id binds a contract to an attempt. Still a note.
- **M12.** See F-6. The verifier's UNVERIFIED reason is now partly checkable against `command.md:23` and `:460`, but the repo file is still needed.

## Coverage

Scoped review of the changed lines from the Step 1 diff: `:62`, `:63`, `:76`, `:83`, `:92`, `:105`, `:112`, `:116`, `:172`, `:178-183`, `:201`, `:202`, `:205`, `:206`, `:209`. I read the whole candidate, so the rows that depend on these lines were checked as well. Guard check on WC-5 status (missing, empty, unknown, `partial`): covered at `:63`, no FR-8 gap. The `/sc:load` exemption guard is F-2. Not checked: anything under `src/`, `plugins/`, `.claude/` or the Orca guides (UNVERIFIED). The `scoped PASS` coverage line does not apply, because the verdict is FAIL.

## Reviser brief

Blocking finding ids: R2-1, R2-2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. F-1 to F-9 and the notes are not in scope for this revision.

The coordinator runs the VERIFY prompt on R2-1 and R2-2 before any revision.

verdict: FAIL

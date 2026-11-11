review: 2 of 3

# Re-review (critique mode, focus requirements,architecture) of the revised Orca worker-contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 e08236b563e957f919d430bee09f668cc4d154a475a77554660dd7026ed73de4
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior: `.dev/orca-command-refactor/review/round1.md` sha256 202844d2013f25c1aa7d07fdcf53356ba01f5c50bb51c3d18a66d79c84a8d175 (header `review: 1 of 3`, so N = 2)
- lint: `.dev/orca-command-refactor/review/lint-2.md` sha256 d4e15d893aa0c394c548c92aeb7421d3dbfaf155b8e5fe0d353970a061981148, produced on the candidate hash above (`lint-2.md:1`)
- reviewer model actually used: claude-sonnet-5-5
- evidence available: README `.dev/orca-command-refactor/README.md:1-36` read first; inventories `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any `sk/`, `cmd/` or `CAPS:` citation not in an inventory is UNVERIFIED here. The rf-qa agent file and `~/.claude/WORKER-CONTRACT.md` are not in the sandbox, so the rf-qa Fix Cycle steps 1-5 were not read; the Review Loop bullets and the RE-REVIEW prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full) were applied on their own.
- mode: `--mode critique --re-review`; `--iterations` ignored; Improve step skipped; no revised specification written.
- brief clauses overridden: none.

## Lint (lint-2.md)

`lint-2.md:3-5`: checks REF, findings 0, "No findings". Nothing to confirm or dismiss. No lint id is open.

## Step 1, evidence block

Roles fixed from the command values (CANDIDATE = revised spec, BASELINE = `specs/history/spec-v1.md`, PRIOR = `review/round1.md`), not from reading order. `diff -w BASELINE CANDIDATE` gives 15 changed lines (hunks at line 62, 73, 76, 83, 85-86, 92, 112, 120, 159, 183, 194-196, 200; the two files are 285 lines each). Verbatim, `<` lines under BEFORE and `>` lines under AFTER:

```text
--- hunk 62c62
BEFORE (baseline): | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
AFTER (candidate): | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes the contract at `<dir>/return-contract.yaml` when the coordinator passed a directory (`--output` / `--output-dir`), at `<file>.return-contract.yaml` (the file's full name plus that suffix) when `--output` names a file, or at the fixed path its section 3 row names, which overrides both (adversarial, cleanup-audit, index-repo, workflow) [M2, M5, M6]. The brief states the path (section 2.3). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
--- hunk 73c73
BEFORE (baseline): The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
AFTER (candidate): The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory or file, so the report path is known before dispatch (WC-4) [M5]; which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
--- hunk 76c76
BEFORE (baseline): The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
AFTER (candidate): The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives [M2]. Every changed command except `load` (usage line only) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
--- hunk 83c83
BEFORE (baseline): | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
AFTER (candidate): | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml`, which is adversarial's WC-4 path [M6] (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
--- hunk 85,86c85,86
BEFORE (baseline): | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
BEFORE (baseline): | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
AFTER (candidate): | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11); the contract is `.claude-audit/return-contract.yaml`, its WC-4 path [M5] (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
AFTER (candidate): | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location; the contract is `PROJECT_INDEX.md.return-contract.yaml` beside it, its WC-4 path [M5] (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
--- hunk 92c92
BEFORE (baseline): | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
AFTER (candidate): | workflow | `--handoff none`; `--output <file>` (from P1) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add `--output <file>`; write the contract at `<file>.return-contract.yaml` on every outcome, pre-creation STOPs included (WC-4 "every outcome"), because the package `<id>` is not known before dispatch; the package contract stays as it is [M5] (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
--- hunk 112c112
BEFORE (baseline): | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
AFTER (candidate): | load | no gate | none (see note) | n/a | none: no `## Unattended mode` section and no contract [M4]; use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
--- hunk 120c120
BEFORE (baseline): | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
AFTER (candidate): | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output <dir>` [M5]; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
--- hunk 159c159
BEFORE (baseline): | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
AFTER (candidate): | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` [M4] (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
--- hunk 183c183
BEFORE (baseline): 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
AFTER (candidate): 4. `test -s <contract>` (the WC-4 path) and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
--- hunk 194,196c194,196
BEFORE (baseline): | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
BEFORE (baseline): | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
BEFORE (baseline): | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
AFTER (candidate): | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; in steps 3 and 4 the report path and `status` come from the command's existing report file, since the contract arrives in P1 (troubleshoot `REPORT.md`; workflow's `.dev/tasks/to-do/<id>/return-contract.yaml`, with `<id>` read from the `worker_done` report path) [M3]. Record the results in the phase report; a failure here reopens section 1 |
AFTER (candidate): | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that `load` and no section-4 command has one [M4] | passes |
AFTER (candidate): | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` [M4] with `--unattended` and the output the brief gives (`--output <dir>`, or `--output <file>` for init-lite [M2, M5]) | all steps pass |
--- hunk 200c200
BEFORE (baseline): | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
AFTER (candidate): | P2 | AC-2.2 | Gate-trigger run per P2 command whose section 3 row resolves a gate as blocked: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`. For the P2 commands whose rows resolve by default or deferral (auggie-review, cleanup, improve, research, tasklist, reflect), the run passes when the stated default or deferral applies, step 2 never shows `agentWait` and `--outcome` matches the contract's `status` [M7] |
```

Self-check run: every AFTER line was found by exact-line `grep -cFx` in the candidate (15 of 15, count 1) and absent from the baseline (0); every BEFORE line was found in the baseline (15 of 15, count 1) and absent from the candidate (0). No role swap.

## Prior blocking findings (from `round1.md:105`: M2, M3, M4, M5, M6, M7)

Each is decided by comparing its defect with the AFTER text only.

| id | status | basis (AFTER text) |
|---|---|---|
| M2 | resolved | The tdd/init-lite `--output <file>` defect (`round1.md:25`) is gone: WC-4 (`spec:62`) now gives `<file>.return-contract.yaml` when `--output` names a file, 7.2 step 4 says "the WC-4 path" (`spec:183`), and AC-1.2 names `--output <file>` for init-lite (`spec:196`). AC-2.2's `/sc:tdd ... --output <file>` example (`spec:200`) therefore has a defined contract path. |
| M3 | resolved | AC-0.4 (`spec:194`) now carves out steps 3 and 4 as well as the report source: troubleshoot `REPORT.md`, workflow's package contract with `<id>` read from the `worker_done` report path. The "step 3 requires a contract that does not exist" outcome (`round1.md:34`) no longer follows. Residual step-4 wording is F2-1 (Medium). |
| M4 | resolved | `load` has no `## Unattended mode` section and no contract (`spec:112`), is excluded from the P1 flag scope (`spec:159`), from AC-1.1 (`spec:195`) and from AC-1.2 (`spec:196`). The contradiction between `spec:112`/`:265` and AC-1.1/1.2 (`round1.md:43`) is removed. |
| M5 | resolved | Every command named in `round1.md:50-53` now has a stated contract location: cleanup-audit `.claude-audit/return-contract.yaml` (`spec:85`), index-repo `PROJECT_INDEX.md.return-contract.yaml` (`spec:86`), workflow `<file>.return-contract.yaml` via a new `--output <file>` (`spec:92`), tdd/init-lite by the file rule (`spec:62`), spec-panel `--output <dir>` (`spec:120`). Section 2.3 now says "output directory or file" (`spec:73`). Remaining wording gaps are F2-2 and F2-3 (Medium). |
| M6 | resolved | The adversarial row now says `<output>/adversarial/return-contract.yaml` "is adversarial's WC-4 path" (`spec:83`), and WC-4 lets a section 3 row's fixed path override the dir rule (`spec:62`). 7.2 step 3's "WC-4 contract path" and AC-1.4 (`spec:198`) now name the same file. |
| M7 | resolved | AC-2.2 (`spec:200`) is limited to P2 rows that resolve a gate as blocked; the six rows that resolve by default or deferral (auggie-review `spec:100`, cleanup `:103`, improve `:110`, research `:116`, tasklist `:122`, reflect `:88`) get their own pass condition. The other nine P2 commands (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot) all have a "blocked" row (`spec:89-91,104,105,115,117,120,121`), so no P2 command is left without an AC-2.2 reading. |

Prior ids that were not blocking: M1 and M8 were rejected by the verifier (`round1.md:11,77-97`, "noted, unactioned"); they are notes, not prior blocking findings, and were not re-opened or re-graded.

Counts: resolved 6, open 0, regressed 0.

## New findings on changed lines

None blocking. Each finding below is graded with the grading check ("an implementer who follows the stated text as written builds X, and X is wrong because Y"); each needs a guess between two allowed readings or restates a requirement the text never states, so each is Medium and goes under follow-up candidates. `origin=changed` for all of them.

=== REQUIREMENTS ANALYSIS ===

- F2-1 (Medium; Wiegers, Adzic; origin=changed): AC-0.4 steps 3-4 still end in a YAML assertion. `spec:194` says "in steps 3 and 4 the report path and `status` come from the command's existing report file (troubleshoot `REPORT.md` ...)", but 7.2 step 4 (`spec:183`) still runs `yaml.safe_load` and `assert d['command']`. `INV-B:242` says troubleshoot's `report_path` is REPORT.md and a `return-contract.yaml` exists "only when `--caller task-unified`"; whether REPORT.md carries a `status` or `command` key is not in the inventory (UNVERIFIED). Reading 1 waives the assertion for the three P0 commands; reading 2 runs it on REPORT.md, where it would fail. The text allows both, so Medium. Same for adversarial: its P0 contract filename is "not fixed" (`spec:83`) and is not named in AC-0.4's parenthesis.
- F2-2 (Medium; Adzic, Crispin; origin=changed): AC-1.2 (`spec:196`) names `--output <file>` only "for init-lite", but the revision made workflow, a P1 command, take `--output <file>` (`spec:92`), and index-repo and cleanup-audit take no output flag (`spec:85-86`). "The output the brief gives" covers them by implication; a reader who takes the parenthesis as exhaustive runs workflow with `--output <dir>`. Related: 7.2 step 6 (`spec:185`) admits "files under the brief's output directory (and the command's documented artifacts)", and a sibling `<file>.return-contract.yaml` is not under a directory. WC-4 documents it, so the second reading is the likelier one. Medium.
- F2-3 (Medium; Wiegers; origin=changed): WC-4's three-way rule (`spec:62`) states no outcome when the brief passes neither a directory, a file nor a fixed-path command, and for rows that say only "add an output path" (analyze `spec:99`, build `:101`, design `:106`, index `:111`, test `:123`) it does not say whether the new flag is a directory or a file. AC-1.2 resolves it to `--output <dir>` for the live check, so no acceptance check fails; the requirement is simply not stated (Guard Condition Boundary Table rows G1-a and G1-f).

=== ARCHITECTURE ANALYSIS ===

- No blocking architecture finding. WC-4's override list "(adversarial, cleanup-audit, index-repo, workflow)" (`spec:62`) lists workflow as a fixed-path command although its row path is derived from the file rule (`spec:92`); the result is the same path either way (minor note).
- Fowler/Newman: the contract location is now a function of (flag kind, section 3 row); each row names it, which is enough for a coordinator to compute the `--report-path` before dispatch (`spec:62`, `:73`).

=== ADVERSARIAL ANALYSIS (Whittaker, changed lines only) ===

- Sequence Attack on AC-0.4 workflow: the `<id>` is read from the `worker_done` report path (`spec:194`), and the worker chooses that path after the package exists, so step 3 compares the report path with a value taken from the same message. It cannot fail, but it also cannot detect a wrong path. Minor note.
- Sentinel Collision on WC-4: a command whose row fixes a path and which also receives `--output <dir>` (adversarial `spec:83`) takes the row path "which overrides both" (`spec:62`). Specified, OK.
- Divergence Attack on AC-2.2: the boundary between the "blocked" group and the "default or deferral" group is each row's own text; the six named commands match their rows (see M7 above). OK.
- Zero/Empty Attack on AC-1.1: `load` is excluded and asserted to have no section; the sentence "that `load` and no section-4 command has one" (`spec:195`) can be read as asserting `load` has one. Minor note (the surrounding [M4] and `spec:112` fix the intent).

### Guard Condition Boundary Table (changed-line guards only, per Review Loop bullet 5)

Guards on changed lines: G1 WC-4 contract-path selection (`spec:62`); G2 AC-1.1/1.2 `load` exclusion (`spec:195-196`); G3 AC-2.2 blocked-versus-default split (`spec:200`). Classes that cannot occur are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1-a path selection | `spec:62` | Zero/Empty | no `--output`, no fixed row path | neither branch | not stated; 2.3 says the brief states the path (`spec:73`) | GAP (Medium, F2-3) |
| G1-b path selection | `spec:62` | One/Minimal | `--output out.md` (file) | file branch | `out.md.return-contract.yaml` | OK |
| G1-c path selection | `spec:62` | Typical | `--output <dir>` | dir branch | `<dir>/return-contract.yaml` | OK |
| G1-d path selection | `spec:62` | Sentinel Value Match | row with a fixed path plus `--output <dir>` (adversarial) | fixed branch | the row path overrides both (`spec:62,83`) | OK |
| G1-e path selection | `spec:62` | Maximum/Overflow | omitted: path length and file counts are not a condition of this guard | n/a | n/a | n/a |
| G1-f path selection | `spec:62` | Legitimate Edge Case | row says "add an output path", kind not given (analyze, build, design, index, test) | undetermined | AC-1.2 uses `--output <dir>` (`spec:196`); WC-4 silent | GAP (Medium, F2-3) |
| G2 `load` exclusion | `spec:195-196` | Zero/Empty | `load` | excluded | no section, no contract (`spec:112`) | OK |
| G2 `load` exclusion | `spec:195` | Legitimate Edge Case | `load` named as "has one" by the sentence grammar | ambiguous | intent fixed by [M4] | OK (minor note) |
| G3 AC-2.2 split | `spec:200` | Typical | a P2 row resolving as blocked | blocked branch | `--outcome failed`, `status: blocked`, non-empty `blocked_question` | OK |
| G3 AC-2.2 split | `spec:200` | Legitimate Edge Case | auggie-review, cleanup, improve, research, tasklist, reflect | default branch | stated default or deferral; `--outcome` matches `status` | OK |
| G3 AC-2.2 split | `spec:200` | Sentinel Value Match | omitted: no sentinel value is compared | n/a | n/a | n/a |
| G3 AC-2.2 split | `spec:200` | Maximum/Overflow, Zero/Empty | omitted: the guard is a membership test on a fixed list | n/a | n/a | n/a |

The table is complete for the changed-line guards (FR-10). Both GAP cells are Medium: neither names a concrete wrong outcome an implementer would produce (FR-8), and the one blank (G1-a) is a requirement the document never states (FR-9).

Pipeline Dimensional Analysis and the State Variable Registry were not triggered: the changed lines hold no multi-stage count flow and `--focus correctness` is not active.

## Minor notes

- `spec:120` adds `--output <dir>` for spec-panel; `INV-B:182` says no `--output` flag exists (consistent with the inventory). The `/sc:spec-panel` command definition read for this run lists `--output <file>` and `--report-dir <dir>` (`command.md:22,460`), so a dir-valued `--output` would collide with it on a current checkout. Not inventory evidence; UNVERIFIED for the spec's target version.
- `spec:86`: the location of `PROJECT_INDEX.md` is "implied, UNVERIFIED" (`INV-A:53`, `commands-a.md:117`), so the contract path next to it inherits that doubt.
- Inherited text (origin=unchanged) was not re-reviewed.

## Follow-up candidates (Medium and minor; none triggers a revision)

| id | grade | one line |
|---|---|---|
| F2-1 | Medium | AC-0.4 step 4 yaml assertion versus REPORT.md / adversarial's unfixed contract name (`spec:183,194`) |
| F2-2 | Medium | AC-1.2 names the file form only for init-lite; workflow's `--output <file>` and the step-6 directory wording (`spec:92,185,196`) |
| F2-3 | Medium | WC-4 silent on no-output briefs and on dir-versus-file for "add an output path" rows (`spec:62,99-123`) |
| N2-1 | minor | AC-1.1 sentence "that `load` and no section-4 command has one" (`spec:195`) |
| N2-2 | minor | spec-panel `--output <dir>` versus a file-valued `--output` in the current command (`spec:120`) |
| N2-3 | minor | WC-4 override list names workflow though its path is file-derived (`spec:62,92`) |

The session that ran this review asks the user once whether to open an issue for these; no issue was created and no question was asked here (sandbox run).

## Coverage

scoped PASS: changed lines + prior blockers

Covered: all 15 changed lines against the baseline; the 6 prior blocking ids M2-M7 against the AFTER text; the dependents of the changed lines (WC-4, section 2.3, 3.1 rows adversarial/cleanup-audit/index-repo/workflow, 3.2 rows load/spec-panel, P1 scope, 7.2 steps 3, 4 and 6, AC-0.4, AC-1.1, AC-1.2, AC-1.4, AC-2.2, SA-3) read in full at `spec:50-215`. Not covered: unchanged sections (1, 8-9, decisions, risks), inventory claims beyond the lines cited, and anything outside the sandbox. Whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review.

## Reviser brief

None: no blocking finding is open. Rules, restated for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding and report the byte size before and after, with bytes added and deleted per finding id.

verdict: PASS

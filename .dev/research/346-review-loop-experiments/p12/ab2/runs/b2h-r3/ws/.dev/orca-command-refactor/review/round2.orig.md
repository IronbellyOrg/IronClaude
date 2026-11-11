review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `bfe20373dae030b64d0ab846cde01958172f4f46786bcfbad746ac335c6b4df6`
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Prior report: `.dev/orca-command-refactor/review/round1.md`, sha256 `5f74f1306a3d7ca6d0c9b8a952e803dfa311595e7214be82dd8e9ee71f3b6679` (`review: 1 of 3`, so N = 2)
- Review rule: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox path `home/.claude/rules/prompts/document_review_loop_prompts.md`). The re-check steps of `rf-qa.md` (project `.claude/agents/` or `~/.claude/agents/`) are UNREAD: neither file exists in the sandbox, so the section-level rules of the command stand alone (Review Loop bullet 5).
- Reviewer model: claude-haiku-5-5
- Inputs: all readable. `~/.claude/WORKER-CONTRACT.md` is absent from the sandbox and is not needed (no `--unattended` run). The baseline hash equals the hash round1 recorded for its candidate, so round1 reviewed the baseline text.

## Citation scope

- `SPEC:n` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line n of the candidate. Changed lines keep the same numbers in the baseline.
- `INV-A:n`, `INV-B:n`, `CAPS:n` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. These are in the workspace; I read each line cited here.
- Repo files outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/agents/rf-qa.md`) cannot be checked here and are UNVERIFIED. No finding below depends on them.

## Scope

Scoped re-review: only lines changed against the baseline, plus the prior blocking findings. This is not whole-document assurance.

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` gives nine changed pairs at SPEC:62, 63, 69, 85, 86, 87, 92, 159 and 195 (18 lines).

BEFORE (baseline):

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
< | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate):

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). F-02: a file-valued output (`--output <file>`, as in tdd and init-lite; `INV-B:47`, `INV-A:55`) uses the file's parent directory as `<output-dir>`. Workflow creates its `<id>` at run time (`INV-B:52`, `INV-B:273`), so its brief passes the `<id>` by a flag the P1 plan names (section 3.1 row). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists, or the contract exists but does not parse with one of the four `status` values (zero bytes, truncated, or no `status` key; F-05); `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). F-05: the worker runs the parse check in section 7.2 step 4 before it sends `worker_done`, so a contract that exists but does not parse is `failed`. The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
> | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. F-03: under `--unattended`, each fixed default output (index-repo `PROJECT_INDEX.md`, init-lite `.dev/superclaude/context-audit.md`, cleanup-audit `.claude-audit/`) is written under the `<output-dir>` the brief passes, so two workers or a retry never share a file (`INV-A:53`, `INV-A:55`, `INV-A:107`). | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; under `--unattended` the output dir comes from the brief instead of the fixed `.claude-audit/`, so two audits never share it (WC-11; F-03) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | `<output-dir>` (F-03) | `PROJECT_INDEX.md` (location implied) | `mode=update` | Under `--unattended`, write `<output-dir>/PROJECT_INDEX.md` (P1; F-03) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Fresh `--output` per attempt under `--unattended` (WC-6, F-03); a standalone re-run still overwrites its marked report | Contract at `<parent of --output>/return-contract.yaml` (P1; F-02, F-04) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1); brief passes `<id>` by the flag the P1 plan names, so the path is known before dispatch (F-02) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow, init-lite (contract; F-04) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (no report file, F-04) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

Self-check (`grep -nF` of each quoted line without its prefix): all 9 BEFORE lines occur exactly once in the baseline and all 9 AFTER lines occur exactly once in the candidate. Roles were not swapped.

Non-changed text relevant here: the candidate still has SPEC:73 (2.3 "the exact command line including `--unattended`"), SPEC:79 (3.1 "if the brief uses the stated flags"), and the P1 Scope column at SPEC:159 ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2"). Those are byte-identical to the baseline.

## Prior blocking findings

| Prior id | Round-1 defect | Status | Basis (AFTER text) |
|---|---|---|---|
| F-02 | WC-4 path "known before dispatch" conflicts with a file-valued `--output` and with workflow's run-time `<id>` | resolved (named defect) | SPEC:62 F-02 sentence and SPEC:92 now give a rule for a file output and a flag for `<id>`. The named conflict no longer produces a wrong path. The rule it introduces causes N-1, and the flag is unnamed (M-1). |
| F-03 | Fixed default output paths let a retry or a sibling worker overwrite earlier output | resolved (named defect) | SPEC:69 (F-03 sentence), SPEC:85, SPEC:86, SPEC:87 now route each default under `<output-dir>` or a fresh `--output`. The output flag is still unnamed for two commands (M-2). |
| F-04 | AC-1.1 cannot pass for `load` (no file) or `init-lite` (no contract) | resolved (named defect) | SPEC:195 excludes `load`; SPEC:159 and SPEC:87 add `init-lite`'s contract in P1. The P1 Commands column still lists a subset of the commands AC-1.1 covers (M-4). |
| F-05 | WC-5 maps an empty, truncated or status-less contract to `succeeded` | resolved (named defect) | SPEC:63 now maps "does not parse with one of the four `status` values" to `failed`. The step-4 assertion also checks `command`, which WC-5 does not map (M-3). |

No prior finding was marked resolved in round 1, so none is `regressed`. No finding is `open`.

F-01: noted, not a prior blocking finding. The verification block at `round1.md:2` rejected it, and the VERIFY rule makes a rejected id a note for this re-review. Its text is unchanged at SPEC:73, SPEC:79 and SPEC:159. Round 1's own Reviser brief (`round1.md:328`) still lists F-01, which contradicts the verification block at `round1.md:2`. The coordinator should reconcile that brief. This review does not treat F-01 as blocking.

## Findings on changed lines

### N-1 | BLOCKING | origin=changed | new, introduced by the F-02 fix at SPEC:62

- Location: `SPEC:62` (WC-4, sentence "F-02: a file-valued output ... uses the file's parent directory as `<output-dir>`"); `SPEC:87` (init-lite row, "Contract at `<parent of --output>/return-contract.yaml`"); `SPEC:69` (WC-11, "Two workers in one worktree must never write the same file").
- Issue: For a file-valued output, the contract name is fixed (`return-contract.yaml`) and only the parent directory varies. Every file-valued run in the same directory therefore writes the same contract path.
- Grading sentence: An implementer who follows `SPEC:62` for two `init-lite` runs in one worktree, `--output docs/a.md` and `--output docs/b.md` (`SPEC:87` says the brief passes `--output`), writes both contracts to `docs/return-contract.yaml`. The second write replaces the first. The coordinator opens that one path for both `worker_done` messages, so the first worker's outcome is lost. `SPEC:69` forbids two workers writing the same file, and `SPEC:64` (WC-6) forbids a retry from corrupting the first attempt's output. The fresh `--output` per attempt in `SPEC:87` does not change the contract path. Two stated texts conflict, and data is lost. Blocking.
- Same case for tdd: `SPEC:90` and `INV-B:47` give `--output <file>` for tdd, so two tdd runs into `docs/` collide the same way.
- Recommendation (narrowing only): name the contract per output file, for example `<output-stem>.return-contract.yaml` beside a file-valued output, and make `SPEC:87` say the same. Alternatively, require the brief to pass the contract path explicitly for a file-valued output. Reviser cites N-1.
- Priority: High.

### M-1 | Medium | origin=changed | SPEC:62 workflow sentence, SPEC:92

- Issue: The text says the brief passes `<id>` "by a flag the P1 plan names". No flag is named in the spec, and the P1 plan is a later artifact (`SPEC:164`). The cited lines do not support the claim that workflow "creates its `<id>` at run time". `INV-B:52` gives the path template and "never reuses a package". `INV-B:273` says "Never overwrites or reuses an existing package" (`SKILL.md:72`). Neither says when `<id>` is generated.
- Grade: Medium. A requirement is missing (the flag name and who generates `<id>`). No stated text yields a wrong outcome by itself.
- Recommendation: name the flag in section 3.1 and state whether the coordinator or the command generates `<id>`.

### M-2 | Medium | origin=changed | SPEC:69, SPEC:85, SPEC:86

- Issue: Under `--unattended`, the rows say the output directory comes from the brief, but neither command has a named output flag. The index-repo "Brief must pass" cell changed from "none" to `<output-dir>`. The cleanup-audit "Brief must pass" cell is still `--pass <N>` only. `INV-A:42` and `INV-A:53` name no output flag for either command (`INV-A:53`: "location (repo root) implied, UNVERIFIED"). `SPEC:62` names `--output` / `--output-dir` as the convention, so the implementer must add a flag the spec never states.
- Grade: Medium. The convention in `SPEC:62` makes a reading available, so the outcome is not forced to be wrong. Missing requirement.
- Recommendation: state the flag each command gains under `--unattended`.

### M-3 | Medium | origin=changed (SPEC:63); unchanged text quoted (SPEC:179, SPEC:183)

- Issue (a): WC-5 says the worker runs the step-4 parse check before `worker_done`. The 7.2 header says "the coordinator runs" its checks (`SPEC:179`). Two stated actors.
- Issue (b): step 4 asserts `d['command']` as well as `status`. WC-5 maps only "does not parse with one of the four `status` values". A contract with a valid `status` and no `command` fails step 4, but WC-5's "otherwise" gives `succeeded`. The spec sets no outcome for a failed step 4.
- Grade: Medium. The implementer must choose whether a failed step 4 means `failed`, and whether the worker or the coordinator runs it.
- Recommendation: state that a failed step-4 assertion is `failed`, and assign the check to the worker.

### M-4 | Medium | origin=changed (SPEC:195, SPEC:159); context SPEC:79, SPEC:90

- Issue: AC-1.1 is a P1 check. It requires a `## Unattended mode` section naming `return-contract.yaml` in every command in 3.1 and 3.2 except `load`. The P1 Scope column says the flag is accepted by every command in 3.1 and 3.2, which would satisfy that. The P1 Commands column lists about 13 commands, not all of them. tdd (`SPEC:90`, a 3.1 command with a file-valued output) and troubleshoot (`SPEC:91`) are not in that list. The 3.1 header says Phase 1 adds the contract (`SPEC:79`).
- Grade: Medium. AC-1.1 can be met through the Scope column, so the F-04 test ("cannot pass as written") no longer applies. The phase membership is still contradictory, and the implementer must choose.
- Recommendation: make the P1 Commands column the full set that AC-1.1 covers, or narrow AC-1.1 to the P1 list.

### m-1 | Minor | origin=changed | SPEC:86

- Note: index-repo's resume is `mode=update`, and the output location has moved to `<output-dir>`. The row does not say whether update reads from `<output-dir>`. A fresh directory has no index to update. Minor note, not a finding for revision.

## Guard Condition Boundary Table (changed guards only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-5 outcome mapping | SPEC:63 | Zero/Empty | 0-byte contract | exists=true, parses=false | `failed` | OK |
| G1 WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | valid `status`, no `command` key | parse of status passes; step 4 fails | `succeeded` ("otherwise") vs an unmapped step-4 failure | GAP, M-3 |
| G1 WC-5 outcome mapping | SPEC:63 | Typical | `status: partial` | true | `succeeded` | OK |
| G2 WC-4 contract path | SPEC:62, SPEC:87 | Legitimate Edge Case | two file outputs in one directory | same contract path | second write replaces the first | GAP, N-1 (blocking) |
| G2 WC-4 contract path | SPEC:62 | One/Minimal | one file output `--output docs/a.md` | parent directory | `docs/return-contract.yaml` | OK for a single run |
| G2 WC-4 workflow `<id>` | SPEC:62, SPEC:92 | Zero/Empty | no `<id>` flag named | n/a | flag unnamed | GAP, M-1 |
| G3 WC-11 default output | SPEC:69, SPEC:85-86 | Zero/Empty | no output-dir flag | n/a | flag unnamed for index-repo and cleanup-audit | GAP, M-2 |
| G3 WC-11 default output | SPEC:87 | Typical | `--output` per attempt | fresh file | `OK` for the file; N-1 for its contract | OK |
| G4 AC-1.1 scope | SPEC:195, SPEC:159 | Legitimate Edge Case | tdd (3.1) not in the P1 list | section absent at P1 | test fails unless Scope column is read | GAP, M-4 |
| G4 AC-1.1 scope | SPEC:195 | Zero/Empty | `load` (no file) | n/a | excluded | OK |

Omitted classes: Maximum/Overflow is not applicable (no numeric limit changed). FR-8: the blocking GAP is N-1; the rest are Medium. FR-9: no blank "Specified Behavior" on a changed row. FR-10: every changed guard is enumerated.

## Follow-up candidates (Medium and minor; not revised)

- M-1 (workflow `<id>` flag unnamed), M-2 (output flag for index-repo and cleanup-audit), M-3 (step-4 actor and `command` mapping), M-4 (AC-1.1 vs P1 Commands column), m-1 (index-repo `mode=update` location).
- Round 1's Medium and Low findings whose text is unchanged remain follow-up candidates from `round1.md`. F-15 quotes the unchanged P1 Scope column and is still a Medium follow-up. The other unchanged Medium and Low findings are not re-graded here.
- No user is present in this run, so no issue was created. The list is recorded only.

## Decisions

- Scope: changed lines and prior blocking findings only (RE-REVIEW core, bullet 5). No whole-document assurance.
- N-1 graded blocking: the stated rule and WC-11 contradict each other, and the result is data loss in a case the spec names (two file-valued outputs in one directory).
- F-02, F-03, F-04 and F-05 graded resolved: each named defect no longer yields the wrong outcome from the stated text. Residuals are graded Medium (M-1 to M-4).
- F-01 noted per the VERIFY rejection at `round1.md:2`; not re-graded.
- The re-check steps of `rf-qa.md` were not applied because neither copy is readable in the sandbox.
- The VERIFY step should run on N-1 before any revision, in a fresh context that sees only the candidate and N-1.

## Coverage

Covered: the nine changed pairs from `diff -w` and the self-check of all 18 lines; prior blocking F-02 to F-05; F-01 status; the changed guards; inventory lines `INV-A:42, 53, 55, 107`, `INV-B:47, 52, 272, 273`, and `CAPS:58-64, 72-79` (read in this run).

Not covered: whole-document assurance; unchanged lines beyond the follow-up note; repo files outside the workspace and the `rf-qa.md` steps (UNVERIFIED here); Orca runtime behavior.

## Reviser brief

Blocking finding ids: N-1.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

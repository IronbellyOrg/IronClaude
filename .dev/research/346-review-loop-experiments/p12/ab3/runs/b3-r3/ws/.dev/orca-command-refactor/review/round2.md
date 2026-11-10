review: 2 of 3

# Spec-panel report, round 2 (re-review): orca-worker-contract-spec.md

Citation shorthand: `SPEC:N` = line N of the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `V1:N` = line N of the baseline `.dev/orca-command-refactor/specs/history/spec-v1.md`; `R1:N` = line N of the prior report `.dev/orca-command-refactor/review/round1.md`; `REV1:N` = line N of `.dev/orca-command-refactor/review/revise1.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the three files under `.dev/orca-command-refactor/inventory/`; `LOOP:N` = line N of `~/.claude/rules/prompts/document_review_loop_prompts.md`; `CMD:N` = line N of `command.md`.

## Report header
| Field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 59305 bytes) |
| candidate sha256 | `e40e99ee4052bc08befc7a5c553a10250f30eed258a771b80b4e6936f8bf5bff` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines, 57763 bytes) |
| baseline sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in `R1:10`, so the baseline is the text round 1 reviewed) |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` |
| prior sha256 | `ddf00f09d600c7e9a89ab29002d1d7fe8a4d78de05257dee7f148e9ed0ffdfa5`; its header is `review: 1 of 3` (`R1:1`) and its last line is `verdict: FAIL` (`R1:230`), so the cap check passes (not at `review: 3`, `CMD:261`) |
| reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| review | 2 of 3 (prior N = 1, plus 1; `LOOP:48`) |
| prompt followed | RE-REVIEW prompt and re-review core, `LOOP:38-51` (file read in full, `CMD:268`); roles fixed by the table at `LOOP:42-46`; re-check follows the Review Loop section of `CMD:256-264` |
| mode handling | `--re-review` with `--mode critique`: `--iterations` ignored, Improve step skipped, no revised specification written (`CMD:261`) |
| `--unattended` | not passed (attended run); no `return-contract.yaml` written because the brief assigns only this file |
| brief clauses overridden | none (the brief neither widens the scope nor grades a minor finding as blocking) |

## Coverage (what this review covered)
`scoped PASS: changed lines + prior blockers`

- Read in full: CANDIDATE, BASELINE (through `diff -w`), PRIOR, `revise1.md`, `README.md`, `commands-a.md`, the relevant parts of `commands-b.md` (`INV-B:28-66,222-280`), `command.md`, and the loop prompts file.
- Checked: all 13 changed hunks (14 changed lines, see Step 1), the two prior blocking findings, and the lines whose meaning depends on a changed line: `SPEC:76-79` (3.1 intro), `SPEC:81-92`, `SPEC:97-125` (every row that names a contract or report path), `SPEC:139`, `SPEC:148-150`, `SPEC:154-162`, `SPEC:182-210`, `SPEC:240`, `SPEC:265`.
- Byte accounting of the reviser: `wc -c` gives 57763 (baseline) and 59305 (candidate), net +1542, as `REV1:10-12` states. The per-finding added/deleted split (`REV1:16-20`) comes from a token diff and is not re-derived here.
- Not covered, by rule: the whole document. Text the revision did not touch is inherited; prior Medium findings M-01 to M-10 and minor notes N-01 to N-05 (`R1:30-50`) were not re-graded and are carried unchanged under `follow-up candidates`. Whole-document assurance needs the separate, labelled gate review (`LOOP:57-64`).
- UNVERIFIED in this sandbox: every citation to `src/superclaude/...`, `CLAUDE.md`, `pyproject.toml`, `tests/`, `~/.claude/skills/...`, `.dev/codegraph-migration/...` and `.dev/evals/...` other than what the inventories quote from them; the added claim that cli-eval and workflow "have no output flag today" (`SPEC:62`), because neither inventory lists those commands' flags (`INV-A:44`, `INV-B:272` name report files only); and the claim that init-lite's `--output` names a file (`INV-A:55` says only "`.dev/superclaude/context-audit.md` or `--output`").
- Experts engaged (focus requirements and architecture): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Newman, Hohpe, plus Whittaker (active in every panel review, `CMD:83`). Crispin, Gregory and Hightower are outside both focus areas and were not engaged. `--focus correctness` is not active, so no State Variable Registry.
- Mandatory artifacts: Guard Condition Boundary Table (guards on changed lines only, `CMD:262`), Quantity Flow Diagram (the section 3 to section 6 funnel changed, so it is re-run).

## Step 1: evidence block (before any finding)
Roles are fixed as in the table at `LOOP:42-46`: CANDIDATE is the `@file`, BASELINE is `--baseline`, PRIOR is `--re-review`. Command run in the workspace root: `diff -w .dev/orca-command-refactor/specs/history/spec-v1.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. The diff is not empty: 13 hunks, 14 changed lines, no line added or removed (285 lines on both sides), matching `REV1:22,62`. Changed lines copied verbatim:

**Hunk 62c62**

BEFORE (baseline):
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

AFTER (candidate):
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract at the path the brief makes known (F-01): `<dir>/return-contract.yaml` where the brief passes a directory (`--output` / `--output-dir`); for tdd and init-lite, whose `--output` names a file, that path with `.return-contract.yaml` in place of its extension (`--output .dev/tdd/auth.md` gives `.dev/tdd/auth.return-contract.yaml`); for adversarial, `<dir>/adversarial/return-contract.yaml`; for cli-eval and workflow, which have no output flag today, `<dir>/return-contract.yaml` for a new `--output <dir>` that only names the contract directory. A row in section 3 states any other path. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

**Hunk 73c73**

BEFORE (baseline):
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

AFTER (candidate):
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the `--output` value, so the contract path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

**Hunk 76c76**

BEFORE (baseline):
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

AFTER (candidate):
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file, at the path WC-4 gives for that command. Every changed command gains the `## Unattended mode` section (section 2.1) in the phase its row names, except `load` (usage line only) and `pr-submit` under D3 (a) (F-02). Phase numbers refer to section 6.
```

**Hunk 84c84**

BEFORE (baseline):
```text
| brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
```

AFTER (candidate):
```text
| brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | Accept `--unattended` (no gate) (P1, F-02) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
```

**Hunk 87c87**

BEFORE (baseline):
```text
| init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

AFTER (candidate):
```text
| init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Contract beside the `--output` file (WC-4) (P1, F-01) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

**Hunk 90c90**

BEFORE (baseline):
```text
| tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
```

AFTER (candidate):
```text
| tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked; contract beside the `--output` file (WC-4) (P2, F-01) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
```

**Hunk 92c92**

BEFORE (baseline):
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

AFTER (candidate):
```text
| workflow | `--handoff none`; `--output <dir>` (new, contract directory only) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Under `--unattended`, also write the contract at `<dir>/return-contract.yaml` on every outcome, including pre-creation STOPs where `<id>/` does not exist yet; the package copy keeps its path (WC-4) (P1, F-01) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

**Hunk 104c104**

BEFORE (baseline):
```text
| cli-eval | `run` requires `--suite` and the safety flags in the brief, else blocked; the W0 "confirm with the user" and missing-`$1` cases resolve as blocked | contract for both pipelines (today a chat table) | fresh dir | split the eval wait into waits of at most 4 minutes (WC-10) | `sk/sc-cli-eval-protocol/SKILL.md:39,55-58,128-153,183-201`; `sk/sc-cli-eval-protocol/refs/run-pipeline.md:5,43-44`; `INV-A:44,65` | P2 |
```

AFTER (candidate):
```text
| cli-eval | `run` requires `--suite` and the safety flags in the brief, else blocked; the W0 "confirm with the user" and missing-`$1` cases resolve as blocked | contract for both pipelines (today a chat table), at `<dir>/return-contract.yaml` for a new `--output <dir>` that only names the contract directory, including the blocked cases before any suite is chosen (WC-4, F-01) | fresh dir | split the eval wait into waits of at most 4 minutes (WC-10) | `sk/sc-cli-eval-protocol/SKILL.md:39,55-58,128-153,183-201`; `sk/sc-cli-eval-protocol/refs/run-pipeline.md:5,43-44`; `INV-A:44,65` | P2 |
```

**Hunk 112c112**

BEFORE (baseline):
```text
| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
```

AFTER (candidate):
```text
| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line; it gets neither `--unattended` nor the section (F-02) | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
```

**Hunk 159c159**

BEFORE (baseline):
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

AFTER (candidate):
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on the commands named in this row only (a no-op where a command has no gate; each later phase adds them to its own commands with their gate behavior, F-02); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, brainstorm, init-lite; fixes to adversarial, cleanup-audit, index-repo, workflow; `load` (usage line only, no flag and no section) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

**Hunk 162c162**

BEFORE (baseline):
```text
| **P4. Outward actions and safety rules** | Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker. | implement, post-release, pr-submit | Each one either changes a deliberate safety rule (`sk/sc-implement-protocol/refs/qa.md:238`) or performs outward actions (`sk/sc-pr-submit-protocol/SKILL.md:189,196`; `sk/sc-post-release-protocol/SKILL.md:340,351`), so it needs the user's decision first. |
```

AFTER (candidate):
```text
| **P4. Outward actions and safety rules** | Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker. implement and post-release gain the flag and section here; pr-submit does only under D3 (b), and under the recommended D3 (a) it gets neither (F-02). | implement, post-release, pr-submit | Each one either changes a deliberate safety rule (`sk/sc-implement-protocol/refs/qa.md:238`) or performs outward actions (`sk/sc-pr-submit-protocol/SKILL.md:189,196`; `sk/sc-post-release-protocol/SKILL.md:340,351`), so it needs the user's decision first. |
```

**Hunk 195,196c195,196**

BEFORE (baseline):
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate):
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command named in the P1 row of section 6 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that neither `load` nor any section-4 command has one (F-02) | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended` and its `--output` as WC-4 gives it (a directory, or a file for init-lite) | all steps pass |
```

**Hunk 200c200**

BEFORE (baseline):
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

AFTER (candidate):
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended --output <dir>` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

Changed line numbers (the same in both files): 62, 73, 76, 84, 87, 90, 92, 104, 112, 159, 162, 195, 196, 200.

### Self-check (run before the verdict)
`grep -nF` of every quoted AFTER line (without its `>`) against CANDIDATE and every quoted BEFORE line (without its `<`) against BASELINE. Result: all 14 AFTER lines are found in CANDIDATE at lines 62, 73, 76, 84, 87, 90, 92, 104, 112, 159, 162, 195, 196, 200, and none of them is in BASELINE; all 14 BEFORE lines are found in BASELINE at the same line numbers and none is in CANDIDATE. No quote was missing, so the roles are not swapped and Step 1 stands. Every requirement that depends on an AFTER line was read against it (see the prior-findings table and the Guard Condition Boundary Table).

## Prior blocking findings
| id | status | basis (AFTER text only) |
|---|---|---|
| F-01 | resolved | WC-4 now gives a path for every case the finding listed (`SPEC:62`): a directory-valued brief gives `<dir>/return-contract.yaml`; tdd and init-lite (file-valued `--output`) give the `--output` path with `.return-contract.yaml` in place of its extension, with the worked example `.dev/tdd/auth.md` to `.dev/tdd/auth.return-contract.yaml`; adversarial gives `<dir>/adversarial/return-contract.yaml`; cli-eval and workflow get a new `--output <dir>` that only names the contract directory. The rows agree: init-lite `SPEC:87`, tdd `SPEC:90`, workflow `SPEC:92`, cli-eval `SPEC:104`, adversarial `SPEC:83` (unchanged, now matches WC-4). Section 2.3 (`SPEC:73`) and the "Contract" definition (`SPEC:76`) no longer say "output directory". The acceptance checks can now pass: AC-2.2 passes `--output <file>` for tdd and `--output <dir>` for cli-eval (`SPEC:200`), AC-1.2 names the file case (`SPEC:196`), 7.2 step 3 ("its report path is the WC-4 contract path", `SPEC:182`) resolves for each. The R1 attack (`R1:63`, `R1:177`) no longer applies: the target is `.dev/tdd/auth.return-contract.yaml`, a sibling of the file, not a path under it. |
| F-02 | resolved | The flag and section scope is narrowed to the commands the P1 row names (`SPEC:159`), `load` gets neither (`SPEC:112`, `SPEC:159`, `SPEC:265` all agree), and implement and post-release gain them in P4 while pr-submit does only under D3 (b) (`SPEC:162`, consistent with `SPEC:240` and `SPEC:139`). AC-1.1 (`SPEC:195`) asserts exactly that set. The quantity check holds: the P1 row names 15 commands, minus `load` is 14, and AC-1.1 expects 14 (R1 found 37 expected against 13 delivered, `R1:74`); see the Quantity Flow Diagram. Section 3 (`SPEC:76`) states the exception. |

No prior blocking finding is `open` or `regressed`; none was deferred or withdrawn (`REV1:28` shows both as applied).

Reviser conformance (`CMD:263`): the reviser left Medium and minor findings alone (`REV1:3`), added one flag (`--output <dir>` on cli-eval and workflow), which R1 itself recommended (`R1:64`), and two P1 entries (brainstorm, init-lite) that R1 counted as "never (2)" (`R1:171`); both are called for by F-01 and F-02. Four edits carry no finding id or only one of the two ids they serve (`SPEC:73`, `SPEC:76`, `SPEC:196`, `SPEC:200`): see N-06. Not a blocking matter.

---

=== REQUIREMENTS ANALYSIS ===

Findings on lines changed against the baseline, plus inherited text that depends on a changed line. None is blocking: each of the three needs a guess about which of two readings an implementer takes, or states a requirement the document never states (`LOOP:35`).

### M-11 (MAJOR label, Medium, priority Medium, origin=unchanged, depends on the changed WC-4 at `SPEC:62`): many rows give no contract path
- **Expert**: Wiegers (lead), Whittaker (Zero/Empty).
- **Issue**: The changed WC-4 (`SPEC:62`) says "A row in section 3 states any other path", but its path rules cover only the cases of F-01. These rows name a "report path", "output path" or nothing, and state no contract path: build (`SPEC:101`), business-panel (`SPEC:102`), design (`SPEC:106`), document (`SPEC:107`), explain (`SPEC:108`, "write the explanation to a file"), index (`SPEC:111`), test (`SPEC:123`), cleanup-audit (`SPEC:85`, fixed `.claude-audit/` output, no flag) and index-repo (`SPEC:86`, "Brief must pass: none"). Rows that say "add `--output`" (analyze `SPEC:99`, spec-panel `SPEC:120`) do not say whether that flag is a directory or a file, which is the ambiguity F-01 resolved for tdd and init-lite. WC-4 also does not say what happens under `--unattended` when the brief omits the output value (the heading "known before dispatch" holds only if the brief supplies it). Why Medium: the fix of F-01 shows the path is one added sentence per row, and an implementer can read "directory by default" from `SPEC:62`; the wrong outcome needs the guess that they pick a file-valued flag or no flag. AC-1.2 (`SPEC:196`) covers every P1 command, so it is where this would show.
- **Recommendation**: narrow, do not add a mechanism: state in WC-4 that a command whose `--output` is not listed above takes a directory, and that an omitted value under `--unattended` resolves as blocked (WC-2 (c)); give the two flagless rows (cleanup-audit, index-repo) a brief-supplied directory or the fixed path.
- **Quality impact**: Completeness +1, Testability +0.5.

### M-12 (MAJOR label, Medium, priority Medium, origin=changed): workflow's new `--output <dir>` sits in the "ready today" table
- **Expert**: Adzic, Cockburn.
- **Issue**: Section 3.1 (`SPEC:79`) says its commands "run as workers now if the brief uses the stated flags", and its column header is "Brief must pass". The changed workflow row (`SPEC:92`) puts `--output <dir>` there with "(new, contract directory only)"; by the row's own text the flag does not exist until P1. P0 builds a brief template "listing the section 3.1 flags" (`SPEC:158`) and then smoke-runs `/sc:workflow` (`SPEC:158`, `SPEC:194`); AC-0.4 runs it without `--output` (`SPEC:194`), so the template and the acceptance check can disagree on whether the flag is passed. The skill's behaviour on an unknown flag is not recorded (`INV-B:267-275` lists none): UNVERIFIED. Why Medium: needs a guess whether the template lists the flag in P0; the same pre-existing pattern is M-10 (`R1:109`).
- **Recommendation**: mark the workflow flag "from P1" in the 3.1 column, or say the P0 template omits flags not yet accepted.
- **Quality impact**: Consistency +0.5.

### M-13 (MAJOR label, Medium, priority Low, origin=changed): edge cases of the "in place of its extension" rule
- **Expert**: Whittaker (Zero/Empty, Sentinel Collision).
- **Issue**: WC-4 (`SPEC:62`) defines the file-valued path only for the typical case. Unstated: an `--output` with no extension (`.dev/tdd/auth`: nothing to replace); two outputs that differ only by extension in one directory (`auth.md` and `auth.txt` both map to `auth.return-contract.yaml`, while WC-11 forbids two workers writing one file, `SPEC:69`); and init-lite `--dry-run`, which "writes nothing" (`INV-A:55`) while WC-4 says the contract is written "on every outcome". Why Medium: edge cases the text never states; the typical case is fully defined.
- **Recommendation**: one clause: append `.return-contract.yaml` when there is no extension, and write the contract even under `--dry-run`.
- **Quality impact**: Completeness +0.5.

### Minor notes (never fail a review)
- **N-06 (Wiegers)**: the reviser contract asks every addition to cite its finding id (`CMD:263`). `SPEC:73`, `SPEC:196` and `SPEC:200` changed for F-01 without an id, and `SPEC:76` cites only F-02 although its Contract definition also changed for F-01. The edits are traceable through `REV1:34-41`, so this is a bookkeeping note.
- **N-07 (Hohpe)**: section 2.3 (`SPEC:73`) says "the `--output` value" while WC-4 (`SPEC:62`) and the auggie-review and pr-submit rows use `--output-dir` (`SPEC:100`, `SPEC:114`). Wording drift, same meaning.
- **N-08 (Newman)**: AC-1.4 (`SPEC:198`) greps for "the workflow return-contract ref" stating the contract is written for pre-creation STOPs, but after the revision that applies to the `<dir>` copy only; the package copy cannot exist before `<id>/` does (`SPEC:92`, `INV-B:272`). Say which copy.
- **N-09 (Fowler)**: the pr-submit row still shows phase P4 without condition (`SPEC:114`) while `SPEC:162` and `SPEC:240` say it changes nothing under D3 (a). Also P3 and P4 have no static assertion for the section on their commands (AC-3.x and AC-4.x use live runs only, `SPEC:204-210`), so only P1 is checked by `test_worker_contract.py`.

=== ARCHITECTURE ANALYSIS ===

- **Fowler (interfaces, boundaries)**: the WC-4 path rule is now an interface with four forms (directory, file-sibling, adversarial subdirectory, new contract-directory flag). It is coherent and each form has an owner row. The seam that stays loose is the set of rows that rely on the default form without saying so (M-11). The F-02 narrowing is sound: the phase that adds the flag is the phase that adds its gate behaviour (`SPEC:159`, `SPEC:162`), so no command has the flag without the WC-2 behaviour. Tracing the dependants of each changed line found no new contradiction: the load decision (`SPEC:265`), D3 (`SPEC:240`), section 4's closing note (`SPEC:139`), AC-4.3 (`SPEC:210`) and the phase membership (section 3 phase tags versus `SPEC:159-162`) all agree.
- **Nygard (failure modes)**: the blocked case before any output exists is now routable for cli-eval and workflow, because the contract directory is supplied in the brief (`SPEC:92`, `SPEC:104`); this was the F-01 failure. Remaining gap: an omitted output value (M-11).
- **Newman (evolution, compatibility)**: the new `--output <dir>` flags are additive and restricted to naming the contract directory, so SA-1 (`SPEC:146`) and SA-4 (`SPEC:149`) hold. Whether the flag name collides with an existing cli-eval or workflow option is UNVERIFIED (flag lists are absent from the inventories).
- **Hohpe (messages and ordering)**: the report-path message (`worker_done --report-path`) now always has a deterministic value when the brief carries the output value; ordering with D3 is unaffected.
- **Wiegers, Adzic, Cockburn (requirements)**: the F-01 and F-02 fixes are testable (AC-1.1, AC-1.2, AC-2.2 changed with them). M-11 to M-13 are completeness gaps next to the fix.

---

## Guard Condition Boundary Table (guards on changed lines only; Nygard builds, Crispin's completeness duty folded in by the lead, Whittaker attacks)
Guards on changed lines: G1 the WC-4 path selector (`SPEC:62`), G2 the AC-1.1 membership set (`SPEC:195`), G3 the D3 branch for pr-submit (`SPEC:162`), G4 the `load` exclusion (`SPEC:112`, `SPEC:159`), G5 the AC-1.2 output kind (`SPEC:196`). In a re-review FR-8 to FR-10 cover changed-line guards only (`CMD:262`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 path selector | WC-4, `SPEC:62` | Typical | brief passes `--output <dir>` | directory form | `<dir>/return-contract.yaml` | OK |
| G1 path selector | WC-4, `SPEC:62` | One/Minimal | tdd `--output a.md` | file form | `a.return-contract.yaml` | OK |
| G1 path selector | WC-4, `SPEC:62` | Zero/Empty | brief omits the output value under `--unattended` | none matches | unspecified | GAP (M-11, Medium: no wrong outcome without a guess) |
| G1 path selector | WC-4, `SPEC:62` | Sentinel Value Match | file-valued `--output` with no extension (`.dev/tdd/auth`) | file form | "in place of its extension" has nothing to replace | GAP (M-13, Medium) |
| G1 path selector | WC-4, `SPEC:62` | Legitimate Edge Case | init-lite `--dry-run` (`INV-A:55`) | file form | contract "on every outcome" versus "writes nothing" | GAP (M-13, Medium) |
| G1 path selector | WC-4, `SPEC:62` | Maximum/Overflow | `auth.md` and `auth.txt` in one directory | file form | both give `auth.return-contract.yaml`; WC-11 bans shared writes (`SPEC:69`) | GAP (M-13, Medium) |
| G1 path selector | WC-4, `SPEC:62` | Typical | adversarial `--output <dir>` | subdirectory form | `<dir>/adversarial/return-contract.yaml`, agrees with `SPEC:83` | OK |
| G1 path selector | WC-4, `SPEC:62` | Typical | row says "report path" / "output path" (build, design, document, explain, index, test, business-panel) or has no flag (cleanup-audit, index-repo) | no form named | row states no path | GAP (M-11, Medium) |
| G2 AC-1.1 membership | AC-1.1, `SPEC:195` | Typical | command named in the P1 row except `load` | member | section must name `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` | OK |
| G2 AC-1.1 membership | AC-1.1, `SPEC:195` | Zero/Empty | `load` | excluded | must not have a section | OK |
| G2 AC-1.1 membership | AC-1.1, `SPEC:195` | Sentinel Value Match | any section-4 command | excluded | must not have a section | OK |
| G2 AC-1.1 membership | AC-1.1, `SPEC:195` | Legitimate Edge Case | command in P2 to P4 (not in the P1 row) | not tested at P1 | no assertion either way; later phases add theirs | OK (static P3/P4 assertion absent, N-09) |
| G3 D3 branch | P4 row, `SPEC:162` | Typical | D3 (a), recommended | pr-submit gets neither flag nor section | agrees with `SPEC:240` | OK |
| G3 D3 branch | P4 row, `SPEC:162` | Legitimate Edge Case | D3 (b) | pr-submit gets flag and section in P4 | agrees with `SPEC:241` and AC-4.3 (`SPEC:210`) | OK |
| G4 load exclusion | `SPEC:112`, `SPEC:159`, `SPEC:265` | Typical | `load` named in the P1 row | usage line only | `--checkpoint` added to Usage; no flag, no section | OK |
| G4 load exclusion | `SPEC:112` | Legitimate Edge Case | a brief puts `/sc:load ... --unattended` as a step | flag unknown to `load` | unspecified | GAP (minor: `SPEC:112` says use it as a brief step; no wrong outcome stated) |
| G5 AC-1.2 output kind | AC-1.2, `SPEC:196` | Typical | P1 command with directory `--output` | directory | contract at `<dir>` | OK |
| G5 AC-1.2 output kind | AC-1.2, `SPEC:196` | One/Minimal | init-lite | file | contract beside the file | OK |
| G5 AC-1.2 output kind | AC-1.2, `SPEC:196` | Zero/Empty | P1 command with no output flag (cleanup-audit, index-repo) | none | "its `--output` as WC-4 gives it" gives nothing | GAP (M-11, Medium) |

Classes left out: G2 Maximum/Overflow, because the membership set is a fixed list of 14 names; G3 Zero/Empty and Maximum, because D3 is a binary choice (`SPEC:240-241`); G4 Maximum, because `load` is one command; G5 Maximum, because the file and directory forms are the only two.
Gate check (FR-10, changed guards only): all cells are populated and every omitted class has its reason, so synthesis may proceed. FR-8 and FR-9 grading: every GAP above needs a guess or states an unspecified edge case and names no concrete wrong outcome, data-loss or safety-boundary risk, so each is Medium or minor and none blocks.

## Quantity Flow Diagram (Fowler annotates, Whittaker attacks; re-run because section 6 changed)
```text
[Source: 43 commands in cmd/ (21 INV-A + 22 INV-B)] --> [Stage 1: verdict split, sections 3 / 4] --> 10 ready (3.1) + 27 needs-change (3.2) + 6 coordinator-only (4) = 43   (conserved)
                                                       |
                                                       v
                                  [Stage 2: worker-capable = 3.1 + 3.2 = 37]
                                                       |
            +------------------------------+-----------+------------------------------+
            v                              v                                          v
[Consumer: P1 scope SPEC:159]   [Consumer: AC-1.1 SPEC:195]            [Consumer: phase rows SPEC:159-162, tags in section 3]
flag + section on the P1 row    asserts section on P1 row minus load   P1 15 named, minus load = 14 (flag + section)
commands: 15 named, load        = 14; neither load nor the 6           + P2 15 + P3 4 + P4 2 (implement, post-release) = 35
gets neither -> 14              section-4 commands has one             + load (0) + pr-submit (0 under D3 (a), 1 under D3 (b)) = 37 (conserved)
<-- MATCH: 14 delivered = 14 asserted (R1: 37 expected, 13 delivered, R1:74) -->
```
Count check against the section 3 phase tags: P1 = analyze, build, business-panel, design, document, explain, index, test (8, `SPEC:99-123`) + brainstorm, init-lite, adversarial, cleanup-audit, index-repo, workflow (6, `SPEC:83-92`) = 14; P2 = 11 rows of 3.2 + reflect, release-split, tdd, troubleshoot = 15; P3 = 4; P4 = 3. Totals 14 + 15 + 4 + 3 = 36 plus `load` = 37. No dimensional mismatch is left (FR-19 would grade one CRITICAL).

## Adversarial analysis (Whittaker; FR-3 template; changed lines only)
1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 "known before dispatch" (`SPEC:62`)** fails when **a brief under `--unattended` omits the output value**. Concrete attack: `/sc:tdd "auth component" --unattended` with no `--output`; before: no contract path; after: the command falls to its default TDD location (`INV-B:222`), the contract path is not in the brief, and `worker_done --report-path` has nothing agreed. Severity: MAJOR label, graded Medium (M-11) because the text does not say the worker invents a path.
2. I can break this specification by **Sentinel Collision Attack**. The invariant at **the extension rule (`SPEC:62`)** fails when **two `--output` files share a stem**. Concrete attack: workers A and B write `.dev/tdd/auth.md` and `.dev/tdd/auth.txt`; both contracts map to `.dev/tdd/auth.return-contract.yaml`; the later write overwrites the first. Severity: MAJOR label, graded Medium (M-13); WC-11 (`SPEC:69`) already forbids two workers writing one file, so the brief is the control.
3. I can break this specification by **Sequence Attack**. The invariant at **the "ready today" table (`SPEC:79`, `SPEC:92`)** fails when **P0 runs before P1 and the template lists `workflow --output <dir>`**. Concrete attack: the P0 brief is generated from the 3.1 column; `/sc:workflow "<small change>" --handoff none --output .dev/x/` is dispatched to a command that does not have the flag yet; behaviour on the unknown flag is unspecified. Severity: MAJOR label, graded Medium (M-12).
4. I can break this specification by **Divergence Attack**. The invariant at **the D3 branch (`SPEC:162`)** fails when **both branches could apply**. Attack: D3 (a) is chosen while a coordinator brief still dispatches pr-submit with `--unattended`. Trace: pr-submit has no flag under (a) and section 4 says coordinator or person only (`SPEC:139`); the contradiction does not arise. Not a finding.
5. I can break this specification by **Accumulation Attack**. The invariant at **the P1 count (`SPEC:159`, `SPEC:195`)** fails when **a command is added to P1 without updating AC-1.1**. Attack: AC-1.1 is defined by reference ("every command named in the P1 row"), so adding a name updates the assertion automatically; count 14 stays equal on both sides. Holds. Not a finding.
6. Zero/Empty Attack on the contract's own fields: `blocked_question` non-empty is required only by AC-2.2 (`SPEC:200`); carried from R1 attack 5 (`R1:181`), unchanged by this revision.

## Standard-format summary (YAML)
```yaml
specification_review:
original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
review_date: 2026-11-10
review: "2 of 3"
scope: "changed lines + prior blockers"
expert_panel: [wiegers, adzic, cockburn, fowler, nygard, newman, hohpe, whittaker]
focus_areas: [requirements, architecture]
prior_findings:
F-01: resolved
F-02: resolved
critical_issues: []
quality_assessment:
overall_score: 7.5
clarity: 7.5
completeness: 7.5
testability: 7.5
consistency: 8
expert_consensus:
- "Both blocking defects are repaired by narrowing and one flag the prior report asked for; the quantity check now conserves (14 delivered = 14 asserted)."
- "What remains is completeness around the new path rule, not a contradiction."
improvement_roadmap:
immediate: []
short_term: [M-11, M-12, M-13]
long_term: [prior M-01 to M-10]
```

## Follow-up candidates (Medium and minor findings; none triggers a revision)
New this round:
- Medium: M-11 (contract path unstated for rows with a "report path" or no flag, and for an omitted output value), M-12 (workflow's new flag in the "ready today" table), M-13 (edge cases of the extension rule).
- Minor: N-06 (finding ids missing on four edits), N-07 (`--output` versus `--output-dir` wording in section 2.3), N-08 (AC-1.4 does not say which workflow copy), N-09 (pr-submit phase tag and no static P3/P4 assertion), and the `load --unattended` brief edge in the table (G4).

Carried from round 1 without re-grading (text untouched by the revision unless stated): Medium M-01 to M-10 and minor N-01 to N-05 (`R1:30-50`). Interactions with this revision, for the next reviser's information only: M-08 (SA-3 versus WC-4 on when the contract is written; the cli-eval row `SPEC:104` still states its contract without the `--unattended` condition that `SPEC:92` has for workflow), M-10 (P0 briefs carry `--unattended` before any command accepts it; `REV1:67` flags the same), M-03 (status vocabulary versus "keep their fields", still in `SPEC:62`), and M-07 (AC-C1 versus the P0 deliverables). None of them is graded blocking here.

Issue question: the review-loop rule says the session that ran the review asks the user once per loop whether to open an issue for the follow-up list and creates none without an answer (`CMD:260`). This run is a worker with a restricted final reply, so the question was not asked and no issue was created; the coordinator should put it to the user.

Next step per the loop: this is a scoped PASS. Whole-document assurance needs the GATE review, run once in a fresh context that has seen no report of this loop (`LOOP:57-64`); this report does not provide it.

## Reviser brief
Blocking finding ids: none. No revision is requested, and none may be made on the strength of the Medium or minor findings above: a Medium or minor finding never triggers a revision and never appears in a Reviser brief (`CMD:259`). If the coordinator later revises on a gate-review blocker, the restated rules apply (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; do not award yourself a PASS.

verdict: PASS

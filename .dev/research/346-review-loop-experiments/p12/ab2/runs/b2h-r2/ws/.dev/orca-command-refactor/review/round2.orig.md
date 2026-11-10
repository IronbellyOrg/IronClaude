review: 2 of 3

# Spec-panel re-review, round 2: Orca worker contract spec

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines; sha256 `c0bcf427b1adbc33a7a7d8ed59cafb19f0ae4373145c6ccaac5362de30dbc042`). Cited below as `spec:N` (candidate line N).
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines; sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`). This is the text round 1 reviewed (round1 header carries the same hash).
- Prior report: `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`; sha256 `882c4d0ecb46b873aa7a904a62b5c83671fe1f45d79b41851985c4da978a0656`). Its line 2 records VERIFY step VF1: B-1, B-2, B-3 confirmed; B-4 rejected and kept as a note.
- Prompt: RE-REVIEW prompt, with the re-review core, from `home/.claude/rules/prompts/document_review_loop_prompts.md` (read in full in the sandbox).
- Command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review review/round1.md --baseline specs/history/spec-v1.md`; `command.md` read in full (Review Loop lines 256-265; Unattended section lines 455-465, not triggered by this run).
- Reviewer model: claude-haiku-5-5.
- Panel: requirements bucket (Wiegers, Adzic, Cockburn), architecture bucket (Fowler, Newman, Hohpe, Nygard), Whittaker (adversarial, always active). Correctness focus is not active; the State Variable Registry and Pipeline Dimensional Analysis are not triggered.
- Not read: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md`. Neither exists in the sandbox (`home/` holds only `rules/prompts/`). The re-check therefore follows the Review Loop rules in `command.md` standing alone, as step 5 allows.
- Not used as inputs: `review/verify-1.md`, `review/findings-1.md`, `review/revise1.md`, `review/round1.orig.md`, and anything outside `ws/` other than `command.md`, the RE-REVIEW prompt file and `home/`.
- Citations: the inventories (`inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`) were checked against the workspace files. The `src/`, `tests/`, `.claude/`, `CLAUDE.md`, `.dev/evals/` and `.dev/codegraph-migration/` paths in the spec are outside the sandbox and are UNVERIFIED here, as in round 1.

## Step 1: evidence block

Roles were fixed by `diff -w BASELINE CANDIDATE`, not inferred. Lines starting `<` are the baseline (BEFORE), lines starting `>` are the candidate (AFTER). Eleven hunks changed: spec:61-62, 79, 90, 92, 112, 114, 120, 195, 235, 265.

Self-check (`grep -Fx` of each quoted line without its `<` or `>`): 11 of 11 BEFORE lines found in the baseline, 11 of 11 AFTER lines found in the candidate. No role swap.

### BEFORE (baseline)

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< | pr-submit | `--monitor 1` refused under `--unattended`; operator HALTs resolve as blocked (the worker may use `ask` or `escalation`); never run as a subagent | add a markdown summary and contract beside `monitor-run-<PR>.jsonl` | `--resume <run-log.jsonl>` | the 600 s default is a cumulative per-wait budget over poll-then-sleep iterations, so the session can already heartbeat between iterations; confirm each single iteration (poll script runtime plus sleep) stays under 4 minutes (WC-10; poll script runtime UNVERIFIED); outward actions per open decision D3 | `sk/sc-pr-submit-protocol/SKILL.md:37-39,46-64,66-68,141,170,189-197,237-246`; `cmd/pr-submit.md:25,39,49,55-56`; `INV-B:34,87-95` | P4 |
< | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< - (b) **Allow a relayed Ruling.** The coordinator asks the person, then answers the worker's `ask` with the person's exact words, which the worker records verbatim as the Ruling. Faster, but it weakens a deliberate safety rule and trusts the coordinator to relay faithfully.
< | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. |
```

### AFTER (candidate)

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. **`ask` never answers a gate a person owns (B-1):** the implement Ruling, the cli-portify approval gates, and any approval of an outward action at run time. Those gates resolve as blocked under WC-2 (c) with no `ask`, unless the user chooses D2 option (b). Only informational questions use `ask`. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11); `INV-A:66` (Ruling rule, qa.md:238; B-1); `INV-A:45` (cli-portify approval gates; B-1) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the brief names through the command's directory flag, set per command in section 3 (B-2). `--output` is not a directory flag: where a command's only output flag takes a file (tdd `--output <file>`), the brief gives a fresh directory and names the file inside it, and the contract is written beside that file. A command whose report path is generated by the command (workflow's `<id>`) must accept an output directory from the brief. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97`; B-2: `INV-B:47`, `INV-B:272-273` |
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column. The workflow row also needs P1's `--output-dir` before its report path can be briefed (B-2).
> | tdd | a precise component prompt, not a bare topic; `--output <file>` inside a fresh directory the brief names (B-2) | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | workflow | `--handoff none`; `--output-dir <dir>` once P1 adds it (B-2) | `.dev/tasks/to-do/<id>/return-contract.yaml` (`<id>` is generated, so not known before dispatch) | Fresh package each run | P1: accept `--output-dir <dir>` and write the contract there, with the package path in its `plan_path` field; write the contract for pre-creation STOPs too (WC-4 "every outcome") | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | load | no gate | none; exempt from AC-1.1 by name (B-3; Decisions `/sc:load` row) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> | pr-submit | `--monitor 1` refused under `--unattended`; operator HALTs resolve as blocked with no `ask` (WC-3, B-1); never run as a subagent | add a markdown summary and contract beside `monitor-run-<PR>.jsonl` | `--resume <run-log.jsonl>` | the 600 s default is a cumulative per-wait budget over poll-then-sleep iterations, so the session can already heartbeat between iterations; confirm each single iteration (poll script runtime plus sleep) stays under 4 minutes (WC-10; poll script runtime UNVERIFIED); outward actions per open decision D3 | `sk/sc-pr-submit-protocol/SKILL.md:37-39,46-64,66-68,141,170,189-197,237-246`; `cmd/pr-submit.md:25,39,49,55-56`; `INV-B:34,87-95` | P4 |
> | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add a directory flag, not `--output` (B-2; the review reads `command.md:460` as making `--output` file-valued, which is UNVERIFIED here); contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, that `/sc:load` is exempt by name with no report file (B-3), and that no section-4 command has one | passes |
> - (b) **Allow a relayed Ruling.** The coordinator asks the person, then answers the worker's `ask` with the person's exact words, which the worker records verbatim as the Ruling. Faster, but it weakens a deliberate safety rule and trusts the coordinator to relay faithfully. Choosing (b) also lifts WC-3's exclusion for the Ruling gate (B-1).
> | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. AC-1.1 exempts it by name (B-3). |
```

## Prior blocking findings

| Id | Prior status | Now | Basis |
|---|---|---|---|
| B-1 | blocking: WC-3 let the coordinator answer a person-owned gate | resolved (default path); residual scope problem is N-2 | spec:61 now excludes the implement Ruling, the cli-portify approval gates and run-time outward approvals from `ask`, and says they resolve as blocked under WC-2 (c). This agrees with spec:105, spec:109, spec:114 and the D2(a) text at spec:234. |
| B-2 | blocking: report path not known before dispatch; `--output` has two meanings | open (narrowed to spec-panel) | workflow is now fixed: spec:92 names `--output-dir <dir>` and P1 adds it. tdd is fixed: spec:90 and spec:62 give a fresh directory with the file inside it. spec-panel is not fixed: spec:120 says "add a directory flag, not `--output`" and does not name it. `command.md:460` (read in this review) already defines `--report-dir <dir>` as the only directory flag and refuses a run without it. An implementer who follows spec:120 either adds a second directory flag beside `--report-dir` or invents a name the coordinator cannot put in the brief (spec:62 requires the brief to name it). spec:120 also labels `command.md:460` "UNVERIFIED here"; the line is in the sandbox and reads as quoted. |
| B-3 | blocking: AC-1.1 cannot pass for `/sc:load` | open | AC-1.1 now exempts load by name (spec:195), the load row says "exempt from AC-1.1 by name" (spec:112), and the Decisions row agrees (spec:265). WC-4 was not changed for load. spec:62 still says "In unattended mode the command writes `<output-dir>/return-contract.yaml` ... written on every outcome" with no carve-out, and P1 (spec:159) puts load under `--unattended`. spec:265 says load writes no report file. The two stated texts still cannot both hold. |
| B-4 | rejected at VF1 (`round1.md:2`); a note under the loop rules, not a prior blocking finding | not re-graded as blocking | The cleanup-audit row (spec:85) is unchanged. Round 1's Reviser brief (`round1.md:151`) still lists B-4 as blocking, which contradicts `round1.md:2`. The coordinator should reconcile this; this review follows the verification block. |

Regressed: none. Round 1 marked no finding resolved, so nothing could regress.

Open blocking after this review: B-2, B-3, N-1, N-2.

## Findings on changed lines (origin=changed)

### N-1. WC-4 says `--output` is not a directory flag, which contradicts section 3, the ACs and the adversarial contract path (blocking, origin=changed)

- Quote, spec:62: "`--output` is not a directory flag: where a command's only output flag takes a file (tdd `--output <file>`), the brief gives a fresh directory and names the file inside it, and the contract is written beside that file."
- Conflicting texts that pass `--output <dir>` as a directory: adversarial (spec:83), brainstorm (spec:84), roadmap in AC-3.2 (spec:205), post-release in AC-4.2 (spec:209), AC-0.4 (spec:194) and AC-1.2 (spec:196, "`--unattended --output <dir>`").
- Path clause, older text quoted through changed line spec:62: the adversarial row (spec:83) fixes the contract to `<output>/adversarial/return-contract.yaml`, while WC-4 (spec:62) writes the same run's contract to `<output-dir>/return-contract.yaml`. The 7.2 step 3 check (spec:182) requires "its report path is the WC-4 contract path", so the coordinator cannot tell which file to open.
- Grading sentence: an implementer who follows spec:62 for brainstorm reads `--output` as not a directory, so the `--output <dir>` that spec:84 and spec:196 require has no defined meaning; the two texts contradict. For adversarial, spec:62 gives `<dir>/return-contract.yaml` and spec:83 gives `<dir>/adversarial/return-contract.yaml`, which is a second contradiction.
- Origin: changed. The sentence "`--output` is not a directory flag" is new; the baseline (`spec-v1.md:62`) read "the directory the coordinator passed (`--output` / `--output-dir`)". The path clause at spec:83 is older but is quoted through changed line spec:62, so it is in scope.
- Fix to consider: state the directory flag per command in section 3 (one column or in each row), delete the flat sentence, and give one contract path per command.

### N-2. The D2 option (b) text lifts a different set of gates from the one WC-3 says it lifts (blocking, origin=changed)

- Quote, spec:61: "Those gates resolve as blocked under WC-2 (c) with no `ask`, unless the user chooses D2 option (b)." "Those gates" are the implement Ruling, the cli-portify approval gates and any run-time outward approval.
- Quote, spec:235: "Choosing (b) also lifts WC-3's exclusion for the Ruling gate (B-1)."
- Grading sentence: an implementer who has chosen D2(b) and follows spec:61 lets `ask` answer the cli-portify approval gates (spec:105) and outward approvals, because spec:61 says the exclusion ends for all of "those gates". spec:235 says only the Ruling gate is lifted. The two texts give different answers for a person-owned approval, which is the harm B-1 names.
- Origin: changed (both lines are new in the candidate).
- Fix to consider: either limit spec:61's "unless" to the Ruling gate, or have D2 option (b) list each gate class it lifts and keep the other two excluded.

### F-1. "Only informational questions use `ask`" leaves "informational" undefined (Medium, follow-up, origin=changed)

- Quote, spec:61: "Only informational questions use `ask`."
- Effect: a reader must guess whether the spec-panel `target_release` gate (spec:120), the tdd topic clarification (spec:90) or the task confidence gate (spec:121) counts as informational. The guess can go either way, so this is Medium under the grading rule, not blocking.

### F-2. Section 3.1 says "Ready today (10)" but the workflow row needs a P1 flag (Medium, follow-up, origin=changed)

- Quote, spec:79: "The workflow row also needs P1's `--output-dir` before its report path can be briefed (B-2)." The heading at spec:78 is "Ready today (10)", and spec:92 lists `--output-dir <dir>` "once P1 adds it".
- The P0 smoke-run list (spec:158) and AC-0.4 (spec:194) still treat workflow as runnable before P1, so the count and the phase plan agree but the 3.1 heading and the row do not. Medium.

### F-3. Round-1 finding ids appear in normative text (minor, origin=changed)

- The revision cites B-1, B-2 and B-3 inside requirement and decision text (spec:61, 62, 90, 92, 112, 114, 120, 195, 235, 265). Those ids live in `review/round1.md`. Once that file is replaced, the references go stale. Move the rationale to the Decisions table and keep the requirement text self-contained.

## Changed guard conditions (FR-8 to FR-10, changed lines only)

| Guard | Location | Input condition | Variable value | Guard result | Specified behavior | Status |
|---|---|---|---|---|---|---|
| WC-3 exclusion | spec:61 | Typical: implement Ruling gate, D2(a) | ask requested | false, no ask | blocked, stop (WC-2 c) | OK |
| WC-3 exclusion | spec:61 | Legitimate edge: D2(b) chosen | scope of lift | true for all three classes (spec:61) or Ruling only (spec:235) | two different scopes | GAP (N-2) |
| WC-3 "informational" | spec:61 | Legitimate edge: target_release or topic clarification | class | undefined | a guess | GAP (F-1, Medium) |
| WC-4 directory | spec:62 | Typical: `--output <dir>` (adversarial, brainstorm) | flag meaning | "not a directory flag" | contradicts spec:83, 84, 196 | GAP (N-1) |
| WC-4 directory | spec:62 | Typical: tdd `--output <file>` | file in fresh dir | contract beside file | defined (spec:90) | OK |
| WC-4 directory | spec:62 | Zero/empty: workflow generated `<id>` | no path before dispatch | accept `--output-dir` (P1) | defined (spec:92) | OK |
| WC-4 directory | spec:62 | Sentinel: spec-panel directory flag | flag name | "a directory flag" (spec:120) | not named; `--report-dir` exists (command.md:460) | GAP (B-2) |
| AC-1.1 exemption | spec:195 | Load: no report file | exempt | no contract | WC-4 (spec:62) still requires one | GAP (B-3) |

No row is blank, so FR-9 does not apply. The Guard Condition Boundary Table for the whole spec is not regenerated here; this re-review covers changed guards only, as the loop rules require.

## Unchanged text

- The adversarial path clause at spec:83 is folded into N-1 because it is quoted through changed line spec:62.
- Round-1 Medium findings M-1 to M-17 and minor m-1 to m-4 are not re-graded. None was resolved by this revision except that spec:112 and spec:265 now record the load decision. m-1 (the `\|` at spec:172) is unchanged.

## Coverage

Covered: the 11 changed hunks; the three prior blocking findings (B-1, B-2, B-3); the status of B-4 as a note; section 3 rows that cite changed lines (spec:83, 84, 90, 92, 105, 109, 114, 120, 194, 196, 205, 209); the D2 text (spec:232-236). Not covered: any unchanged text as a blocking candidate, and any `src/`, `tests/` or `.claude/` citation (UNVERIFIED in this sandbox).

## Reviser brief

Blocking finding ids: B-2, B-3, N-1, N-2.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (F-1, F-2, F-3, M-1 to M-17, m-1 to m-4) are not part of this brief.

Brief clauses overridden: none (no brief was given to this reviewer).

verdict: FAIL

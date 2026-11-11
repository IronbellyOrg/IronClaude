review: 2 of 3

# Spec-panel critique, re-review: orca-worker-contract-spec (focus: requirements, architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `97f56a6e69838dc9f80dfae9d1e8e0aa95413656b2559e687870566b2996ca6a`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior: `.dev/orca-command-refactor/review/round1.md`, sha256 `d9cfd95ba0439917950bb2cf3f228d35ae4564bea0a09a992a01c74a90e975f3` (prior header `review: 1 of 3`, so this report is review 2 of 3)
- reviewer model: claude-haiku-5-5
- prompt: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox home copy), with the re-review core (roles, Step 1, review number, self-check) followed first
- verification block: `round1.md` line 2 (VERIFY step VF1, `review/verify-1.md`) confirmed B-1, B-3, B-5 and rejected B-2 and B-4 as noted, unactioned. Per that block, only B-1, B-3 and B-5 are prior blocking findings here. B-2 and B-4 are carried as notes, not re-graded.
- rf-qa.md: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` is present in the sandbox. The Review Loop step 5 rules in `command.md:262` therefore stand alone.
- round1 header note: round1 records the candidate sha as `d3cdbe57...`, which is the sha of the current baseline file. Round1 quotes the pre-revision text (`spec-v1.md:79`), so `history/spec-v1.md` is the text round1 reviewed.
- citation key: `spec:N` = candidate line N; `baseline:N` = `history/spec-v1.md` line N; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (relative to `.dev/orca-command-refactor/`); `round1:N` = `review/round1.md` line N.
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (active in every panel review, `command.md:83`).

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Changed-line set | Diff the whole file; diff with `-w` | `diff -w` as Step 1 requires; whitespace-only changes are ignored. Eleven candidate lines changed (listed in Step 1). |
| Verdict scope | Re-grade every round1 Medium; re-grade only prior blockers and changed lines | Re-review scope (`command.md:261` item 5 and the RE-REVIEW prompt): prior blockers plus changed lines. Unchanged Medium items are listed as carried follow-ups, not re-graded. |
| B-2 and B-4 | Re-grade; treat as noted | Treated as noted per the verification block (`round1.md:2`), which the next re-review must honour. |

## Coverage

Read in full: `README.md`, the candidate spec, the baseline spec (through the Step 1 diff and the unchanged-line checks), `round1.md` (including its verification block), the RE-REVIEW prompt file, and `command.md`. The verify-1 table was read for the B-1, B-3 and B-5 reasoning.

Checked against the inventories and the README (the only evidence in the sandbox): `INV-A:35` (adversarial contract, observed paths, artifacts under `<output>/adversarial/`), `INV-A:55` (init-lite), `INV-A:60-61` (adversarial contract location, `--output` default), `INV-A:97`, `INV-B:47` (tdd), `INV-B:52` (workflow), `INV-B:267-275` (workflow ref: contract written on post-creation outcomes, not on pre-creation STOPs, `INV-B:272,39`), `CAPS:72-74`, `CAPS:73` (worker_done needs an explicit outcome), `CAPS:76-77`, `CAPS:79` (report path is a pointer; Orca's handling UNVERIFIED). Each cited line matches the claim the changed spec lines make about it.

Not checkable here (UNVERIFIED): every `sk/`, `cmd/` and `src/superclaude/` cite in the changed rows (for example `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908`, `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`, `sk/tdd/SKILL.md:48,52-61`), `WORKER-CONTRACT.md` (not in the sandbox), `remediation-handoff.md` (B-4, noted), and the PR #329 run.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Roles: BASELINE = `specs/history/spec-v1.md`, CANDIDATE = `specs/orca-worker-contract-spec.md`. Lines starting `<` are `BEFORE (baseline)`; lines starting `>` are `AFTER (candidate)`. Changed hunks: baseline lines 62-63, 73, 76, 79, 83, 87, 90, 92, 198, 200 (candidate lines 62-63, 73, 76, 79, 83, 87, 90, 92, 198, 200).

```text
62,63c62,63
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract to a path fixed by the output argument the coordinator passed (B-3): for a directory (`--output` / `--output-dir`) it is `<output-dir>/return-contract.yaml`; for a file (`--output <file>`) it is `<file's directory>/<command>-return-contract.yaml`; workflow is the one named exception (section 3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, except workflow's pre-creation STOP (B-3). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`); `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
---
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory or file, so the report path is known before dispatch (WC-4; workflow excepted, B-3); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives for the command's output kind (B-3). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
79c79
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
---
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. Every command here also gets the P1 `--unattended` flag and its `## Unattended mode` section, a no-op where the command has no gate (B-1). Beyond that, the only command changes are the small fixes in the last column.
83c83
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
---
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Write the contract at `<output>/return-contract.yaml` on every run, the directory rule in WC-4 (B-3) (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
87c87
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
---
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Contract beside the report as `<dir>/init-lite-return-contract.yaml`, the file rule in WC-4 (B-3) (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
90c90
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
---
> | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2); the contract goes beside the TDD as `<dir>/tdd-return-contract.yaml`, the file rule in WC-4 (B-3) (P1) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | The path is the package's `return-contract.yaml`, the named WC-4 exception (B-3); the coordinator learns it from `worker_done --report-path`. A pre-creation STOP has no package, so it writes no contract and sends `--outcome failed` with the STOP in the body (B-3, B-5) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
198c198
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
---
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states that a pre-creation STOP writes no contract (B-3) |
200c200
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
---
> | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`. WC-5 fixture contracts (zero bytes, truncated, `status: Succeeded`) each map to `failed` (B-5) |
```

Self-check (`grep -nF` of each quoted AFTER line in the candidate, and each BEFORE line in the baseline): all eleven AFTER lines are found exactly once in `spec:` and all eleven BEFORE lines exactly once in `baseline:`. Roles are confirmed. No prior blocking finding is marked resolved on a stale reading.

## Prior blocking findings

| id | status | evidence (AFTER text only) |
|---|---|---|
| B-1 | resolved | `spec:79` now says every ready-today command "also gets the P1 `--unattended` flag and its `## Unattended mode` section, a no-op where the command has no gate (B-1)". Brainstorm (`spec:84`, fix "None") and init-lite (`spec:87`) are therefore covered, and `spec:195` (AC-1.1) and `spec:159` (P1) agree with it. The AFTER text removes the contradiction that `spec:79` denied the flag to those two commands. Residual wording issue is recorded as N-3. |
| B-3 | resolved | `spec:62` (WC-4) now fixes the path from the output argument: directory gives `<output-dir>/return-contract.yaml`; file gives `<file's directory>/<command>-return-contract.yaml`; workflow is the named exception. The four rows the finding named now match it: adversarial `spec:83` (`<output>/return-contract.yaml`), init-lite `spec:87` (`<dir>/init-lite-return-contract.yaml`), tdd `spec:90` (`<dir>/tdd-return-contract.yaml`), workflow `spec:92` (package path, B-3 exception). `spec:73` and `spec:76` agree. AC-1.4 (`spec:198`) now checks the workflow STOP case. Residual unnamed locations in other rows are recorded as N-4. |
| B-5 | resolved | `spec:63` (WC-5) now sends `--outcome failed` for a contract that is missing, zero bytes, truncated, unparseable, lacks `status`, or has a value outside the four. `--outcome succeeded` needs a parsed `succeeded` or `partial`. The literal "otherwise = succeeded" path that sent a crashed run as completed is gone. AC-2.2 (`spec:200`) adds the three fixture cases. The new defect this wording creates in P0 is recorded as N-1 below, not as a regression of B-5. |

Noted, not re-graded (per `round1.md:2`): B-2 (AC-0.4 step 4 parses a non-YAML `REPORT.md`; `spec:194` and `spec:183` unchanged) and B-4 (reflect remediation auto-accept under `--unattended`; `spec:88` and `spec:122` unchanged). Both remain in the candidate text and stay on the follow-up list as noted items.

## Findings on changed lines

### N-1 (BLOCKING, new, origin=changed): WC-5 keys the default outcome on the contract, but spec:79 has P0 workers report the named file, with no contract yet

- Changed line: `spec:63`. Baseline `baseline:63` read "`--outcome failed` when the report says `failed` or `blocked`, or no report exists". The revision replaced "no report exists" with "when the contract is missing, zero bytes, ...". The subject moved from the report to the contract.
- Text that interacts with it: `spec:79` "the worker reports the named file until Phase 1 adds the contract"; `spec:91` (troubleshoot report is `REPORT.md`); `spec:194` (AC-0.4) "step 4 uses the command's existing report file, since the contract arrives in P1"; `spec:182` (7.2 step 3) "its `--outcome` matches the contract's `status` under WC-5".
- Sentence: "An implementer who follows `spec:63` in P0 for `/sc:troubleshoot`, where `spec:79` and `spec:91` say the worker reports `REPORT.md` and no contract exists until P1, finds the contract missing and sends `--outcome failed` after a completed run, and that is wrong because the run did not fail."
- Whittaker, FR-2.1 (Zero/Empty): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract is absent in a phase where the named report is the deliverable**. Concrete attack: the P0 smoke run of `/sc:troubleshoot "<symptom>"` writes a complete `REPORT.md` and no `return-contract.yaml`; WC-5 selects `failed`; `worker_done --outcome failed` settles the Task as failed; AC-0.4 step 3 (`spec:182`) then has no contract status to compare with. Trace: before = run completed; after = Task failed, and AC-0.4 cannot pass as written."
- Origin: the revision itself. Baseline wording was coherent in P0 because it keyed on the report.
- Severity: MAJOR by text, blocking under the grading rule: a stated text produces a wrong outcome on a clean run, and AC-0.4 (`spec:194`) cannot pass as written.
- Expert: Nygard (failure and settlement), Adzic (testability of AC-0.4), Hohpe (delivery semantics).
- Recommendation: restore the report-keyed wording for P0 and keep the contract rule from P1, for example "when the command's report (the named report file in P0, the contract from P1) is missing, zero bytes, truncated, unparseable, lacks `status`, or has a value outside the four". Alternatively, change `spec:182` step 3 to compare with the named report in P0. Name the P0 report per command in section 3.1. Delete the words "the contract is missing" from `spec:63` rather than adding a rule.
- Priority: High. Quality impact: high (silent false failure on every P0 smoke run, and the P0 gate in `spec:158` cannot be passed).

### N-2 (minor, origin=changed): adversarial contract location differs from the location the inventory observed

- `spec:83` now puts the adversarial contract at `<output>/return-contract.yaml`. `INV-A:35` records real runs writing `<output>/adversarial/return-contract.yaml` next to the merged output and the six artifacts under `<output>/adversarial/`. The new location is consistent with WC-4 (`spec:62`) and is a valid choice, but no entry in the spec's `## Decisions` table records the change from the observed path. Minor note.

### N-3 (minor, origin=unchanged, quotes changed lines): "changed command" is undefined

- `spec:52` ("Each changed command adds a short `## Unattended mode` section"), `spec:76` ("Every changed command also gains the `## Unattended mode` section") and `spec:79` ("Every command here also gets ... section") use two different sets. `spec:79` names the ready-today set explicitly, so the conflict resolves once `spec:79` is read. Minor note: say "every command in sections 3.1 and 3.2".

### N-4 (Medium, origin=unchanged, quotes changed WC-4): two rows still leave the contract location unnamed

- `spec:105` (cli-portify): "contract (fields already defined; file location unnamed)". `spec:114` (pr-submit): "add a markdown summary and contract beside `monitor-run-<PR>.jsonl`".
- WC-4 (`spec:62`) requires the path to be fixed by the output argument before dispatch, and `spec:73` says the coordinator's brief states it. For cli-portify the location is undefined, so the brief cannot name it. Per the grading rule, an undefined location is a requirement the document never states, which is Medium, not blocking. The pr-submit row names a base file, but the contract's own name and place are not set by WC-4's directory or file rule.
- Recommendation: apply the file or directory rule of `spec:62` to both rows.

### N-5 (minor, origin=unchanged, quotes changed lines): 7.2 step 3 does not carry the workflow exception

- `spec:182` requires "its report path is the WC-4 contract path". `spec:73` and `spec:92` say the workflow contract path is the package's, learned from `worker_done --report-path`. Step 3 does not say so. Minor note.

## Carried follow-up candidates (not re-graded, unchanged lines)

Medium, carried from round1 and still open on unchanged text: M-1 (WC-1 has no owner or phase, `spec:59`), M-2 (partial maps to succeeded, `spec:63`, `spec:262`, `spec:263`), M-3 (write-then-send order is still not stated, `spec:62` and `spec:63`), M-4 (WC-3 answer path and ask timeout, `spec:61`), M-5 (SA-2 check misses `orca-cli` and uppercase `ORCA`, `spec:172`), M-6 (SA-4 versus section 3 edits, `spec:149`), M-7 (nesting layers, `spec:122`), M-8 (plugin mirror, `spec:279`), M-9 (P0 smoke runs do not test WC-2, `spec:79`, `spec:194`), M-10 (4-minute rule for an iteration over 4 minutes, `spec:68`), M-11 (testability, WC-5 has no automated test, `spec:195`), M-12 (checkpoints undefined, `spec:70`), M-14 (WC-11 and fixed output dirs, `spec:85`, `spec:119`), M-15 (brief template owner and version, `spec:73`, `spec:158`).

M-13 (missing `--output` in an unattended brief) is still open and now more relevant: WC-4 (`spec:62`) derives the path from the output argument, and no line says what happens when that argument is absent.

Minor, carried from round1: N-1 (`spec:215` cites `CAPS:12-13`), N-2 (`spec:80` says "share the current worktree by default"), N-3 (`spec:23` PR #329 claim, `README:12`).

Noted (not re-graded): B-2 and B-4, see above.

## Guard Condition Boundary Table (changed guards only)

The re-review table covers guards on changed lines only (`command.md:261` item 5). Changed guards: WC-4 path rule, WC-5 outcome mapping, the workflow pre-creation STOP.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | no contract, P0 (named report only, `spec:79`) | `failed` | A completed run is reported failed; AC-0.4 cannot pass | GAP (N-1, blocking) |
| WC-5 outcome mapping | spec:63 | Zero/Empty | contract exists, 0 bytes | `failed` | Task fails; no dependent starts | OK |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: Succeeded` (case) | `failed` (outside the four values) | As written | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: partial` | `succeeded` | Lossy, as recorded in M-2 | OK as written; M-2 |
| WC-4 contract path | spec:62 | Typical (file-valued output) | `--output <file>` for tdd (`spec:90`) and init-lite (`spec:87`) | `<file's dir>/<command>-return-contract.yaml` | Fixed path, known before dispatch | OK |
| WC-4 contract path | spec:62 | Zero/Empty | `--output` omitted under `--unattended` | not stated | Path undefined | GAP (M-13, Medium) |
| WC-4 contract path | spec:62 | Boundary (workflow pre-creation STOP) | no package exists | no contract; `failed` with STOP in body (`spec:92`) | Stated | OK |
| WC-4 row location | spec:105 | Typical (cli-portify) | no location named | not stated | Path undefined | GAP (N-4, Medium) |

FR-8: two GAP rows are findings above (N-1 blocking, N-4 Medium and carried M-13). FR-9 (blank behaviour): none blank. FR-10: the table is complete for the changed guards.

Pipeline Dimensional Analysis: not triggered by the changed lines. No changed line alters a count along the report pipeline.

## Re-review result

- Prior blocking findings: B-1 resolved, B-3 resolved, B-5 resolved.
- New blocking finding: N-1.
- Coverage line: not `scoped PASS`, because a blocking finding is open.

## Reviser brief

Blocking findings: N-1.

Restated from review-loop step 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (N-2 to N-5, M-1 to M-15, the minor notes) are not part of this brief.

Brief clauses overridden: none.

verdict: FAIL

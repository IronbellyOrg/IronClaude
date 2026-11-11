review: 2 of 3

# Re-review of the worker-contract spec (round 2, scope: requirements, architecture)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350
baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior: .dev/orca-command-refactor/review/round1.md sha256 d5fc834487c8d7925d17473bc0310715ebfb8571f334f3324347c80ddd806327 (review: 1 of 3, verdict FAIL)
prompt: ~/.claude/rules/prompts/document_review_loop_prompts.md sha256 ed219181156e47e6d70120730063e0b00081482d8a78b3d2633da188574ca829 (RE-REVIEW prompt and re-review core applied)
reviewer model: claude-haiku-5-5 (Haiku 5.5)

Note on the prior report: its `candidate:` hash (d3cdbe...) is the text now stored at the baseline path. Round 1, and the verification VF1 in `.dev/orca-command-refactor/review/verify-1.md:3-4`, covered the pre-revision text. That is consistent with the roles below.

## Step 1: evidence block

Roles, fixed: CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (the revised text); BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md` (the text before the revision); PRIOR = `.dev/orca-command-refactor/review/round1.md`.

`diff -w BASELINE CANDIDATE`, changed lines copied verbatim. `<` lines are BEFORE (baseline), `>` lines are AFTER (candidate). The diff has 17 `<` lines and 26 `>` lines, in hunks at baseline 61-63, 67, 73, 76, 85-87, 90, 92, 116, 159, 172, 194, 196, 198 (candidate 61-63, 67, 73, 76, 85-87, 90, 92, 116, 159, 172, 178-185, 202, 204, 206-207).

````text
BEFORE (baseline)
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
< | WC-9 | **No outward action unless the brief authorizes it.** Under `--unattended`, any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off. It turns on only through the command's own explicit flag written in the brief. | Command | `cmd/auggie-review.md:51-54` (posts by default, no prompt); `.dev/orca-command-refactor/README.md:31`; per-command outward actions in column (f) of the inventories |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
````

````text
AFTER (candidate)
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag, except that a gate guarding a Ruling, an outward action or a safety boundary resolves as blocked and no `ask` answer supplies it (M11; D2, D4, WC-9). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, written on every outcome, at a path the coordinator can read.** In unattended mode the command writes its contract at the path section 3 gives for it. Where the command's output option names a directory, that path is `<output-dir>/return-contract.yaml`, with `<output-dir>` the directory the coordinator passed (`--output` / `--output-dir`); adversarial's is `<output>/adversarial/return-contract.yaml` (`INV-A:60`). Where the output option names a file (tdd, init-lite), the contract sits beside that file. Where the path is generated at run time (workflow, research), the worker passes it in `worker_done --report-path` and the coordinator reads it then (M1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, except workflow's pre-creation STOPs (M2; section 3, `INV-B:272`). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, when no report exists, or when the report is empty, unparseable or has a status outside `succeeded`, `partial`, `failed`, `blocked` (M9); `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
> | WC-9 | **No outward action unless the brief authorizes it.** Under `--unattended`, any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off. It turns on only through the command's own explicit flag written in the brief (D4), and a coordinator's `ask` answer never supplies that flag (M7; WC-3). | Command | `cmd/auggie-review.md:51-54` (posts by default, no prompt); `.dev/orca-command-refactor/README.md:31`; per-command outward actions in column (f) of the inventories |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, including `--unattended` from P1 on (P0 runs omit it, AC-0.4 (M12)), and every flag section 3 lists as required; the output directory or file, so the report path is known before dispatch where WC-4 gives a fixed path (M1); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). The coordinator dispatches at most one cleanup-audit or index-repo Task per worktree at a time, because their output paths are fixed (M13; WC-11). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives for the command (M1). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so the coordinator runs one audit per worktree at a time (section 2.3, M13) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | none | `PROJECT_INDEX.md` (location UNVERIFIED, `INV-A:53`; fixed path, so section 2.3 serializes its dispatches, M13) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | The contract sits beside the `--output` file (M1; P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2); the contract sits beside the `--output` file (M1) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | No contract for pre-creation STOPs, which have no package directory yet: the worker reports them as `worker_done --outcome failed` with the STOP in the body (M2; WC-5, `INV-B:272`) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract beside the generated `claudedocs/research_*.md`, its path passed in `worker_done --report-path` (M1) | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate), except that auggie-review, task, pr-submit and post-release refuse it with an error until their P2 or P4 change lands, because each has an outward default that WC-9 requires off (M3; `INV-A:38`, `INV-B:94`); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow, init-lite (M1) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C1 | Run the grep in the block below, which sets the pattern out in plain form because a table cell cannot hold a plain `|`. | The first command prints nothing (SA-2, WC-8). The positive control prints its planted line, which shows the pattern matches (M8). |
> The AC-C1 block (M8). Run the first line from the repo root; the second and third lines are the positive control, which must print its one planted line:
> 
> ```bash
> grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v '^src/superclaude/skills/ccsession-tag/'
> # positive control (M8): must print one line
> printf 'orca orchestration check --json\n' | grep -E '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'
> ```
> 
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript), with the stated flags only and no `--unattended`, since P0 adds no such flag (M12) | steps 1, 2 and 5-7 pass; step 3 checks `--outcome` against the existing report, and its path is that report, not the WC-4 contract, since the contract arrives in P1 (M6). Step 4 is replaced (M6): troubleshoot's `REPORT.md` (`INV-B:49`) must exist and be non-empty, and workflow's and adversarial's existing `return-contract.yaml` must be non-empty and parse as YAML. The four-value `status` and `command` assertions move to AC-1.2. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass, and step 4 applies the four-value `status` and `command` assertions (M6) |
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states that pre-creation STOPs write no contract (M2) |
> | P1 | AC-1.5 | Dispatch two cleanup-audit Tasks into one worktree; the second is dispatched only after the first `worker_done` (check the dispatch log and `worker-list --run <run_id>`) | the second dispatch comes only after the first `worker_done` (M13; section 2.3) |
````

Self-check (run before the verdict): each quoted BEFORE line was found in BASELINE with `grep -F`, 17 of 17. Each quoted AFTER line was found in CANDIDATE, 26 of 26. No role was swapped.

## Prior blocking findings (round 1, merged; confirmed by VF1)

Prior blocking ids (from `round1.md:161`): M1, M2, M3, M6, M7, M8, M9, M11, M12, M13. Ids M4, M5 and M10 were rejected at VF1 and are noted, unactioned (`verify-1.md:24`, `round1.md:124-146`). They are not prior blocking findings.

| Prior id | Status | Evidence in the candidate |
|---|---|---|
| M1 contract path | resolved | WC-4 `:62` now gives adversarial's path `<output>/adversarial/return-contract.yaml`, a file-beside rule for tdd and init-lite, and a run-time path for workflow and research read from `worker_done --report-path`. Rows `:83`, `:87`, `:90`, `:92`, `:116` and section 2.3 `:73` agree. Residual: N1. |
| M2 workflow pre-creation STOP | resolved | WC-4 `:62` excludes "workflow's pre-creation STOPs"; row `:92` reports them as `worker_done --outcome failed` with no contract; WC-5 `:63` maps "no report exists" to failed; AC-1.4 `:206` checks the workflow ref. Inventory: `inventory/commands-b.md:272` says the contract is "Not written for pre-creation STOPs". |
| M3 P1 flag on outward defaults | resolved | P1 `:159` refuses `--unattended` with an error for auggie-review, task, pr-submit and post-release until P2 or P4 (rows `:100`, `:121`, `:114`, `:113`). The (f) column of the P1 rows is "None" at `inventory/commands-a.md:37`, `:40`, `:41`, `:46`, `:47`, `:48`, `:53`, `:54` and `inventory/commands-b.md:52` (workflow, `--handoff none`). Residual for gated commands: N5. |
| M6 AC-0.4 step 4 | resolved for the named defect | AC-0.4 `:202` replaces step 4 per command: troubleshoot checks `REPORT.md`; workflow and adversarial check their existing YAML. The four-value assertions move to AC-1.2 `:204`. Residuals: N2, N3. |
| M7 coordinator reply as outward flag | resolved | WC-3 `:61` and WC-9 `:67` now both say a coordinator `ask` answer never supplies an outward flag. D4 `:253-255` is unchanged and consistent. |
| M8 AC-C1 grep cannot fail | resolved | AC-C1 `:172` and its block `:178-185` use plain `\|` alternation with a positive control at `:183`. Run on this worker: the control line matched (1 match); `orca-ide worktree create` matched (1); clean text did not match (0). |
| M9 zero-byte or unparseable contract | resolved | WC-5 `:63` sends `failed` for an empty, unparseable or out-of-set report. Step 4 `:191` is unchanged. Residual for a missing `status` key: N7. |
| M11 Ruling and outward gates answered by coordinator | resolved | WC-3 `:61` exempts "a gate guarding a Ruling, an outward action or a safety boundary", which "resolves as blocked and no `ask` answer supplies it". WC-9 `:67` agrees. Residuals: N4 (D2(b)), N8. Cross-reference from the implement row `:109` and D2 to WC-3 by name was not added (minor note). |
| M12 P0 live check uses `--unattended` | resolved | Section 2.3 `:73` says "P0 runs omit it, AC-0.4 (M12)"; AC-0.4 `:202` says "with the stated flags only and no `--unattended`". Section 3.1 intro `:79` is consistent. |
| M13 fixed output paths in one worktree | resolved | Section 2.3 `:73` allows at most one cleanup-audit or index-repo Task per worktree at a time; rows `:85` and `:86` cite it; AC-1.5 `:207` tests the ordering. Residual: N6. |

Open: none. Regressed: none (no prior finding was marked resolved in round 1).

## Findings on changed lines (new)

Scope: the 17 candidate hunks at lines 61-63, 67, 73, 76, 85-87, 90, 92, 116, 159, 172, 178-185, 202, 204 and 206-207, plus the prior blockers above. Findings on unchanged lines appear only as notes.

### N5 (blocking, MAJOR): P1 accepts `--unattended` on gated commands that still prompt

- Origin: changed. Candidate `:159` is changed; the "accepted by every command in sections 3.1 and 3.2" clause is inherited from baseline `:159` and was not raised in round 1 (it was a defect of the same kind as M3, which covered only outward defaults).
- Texts that contradict: WC-2 `:60`, "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer"; against P1 `:159`, which accepts the flag on every command in sections 3.1 and 3.2 except the four outward-default commands, and section 2.3 `:73`, which passes `--unattended` "from P1 on".
- Gates still on the default path until P2 or later: tdd (`:90`, topic-only clarification), release-split (`:89`), troubleshoot (`:91`, `--depth deep` STOP), cli-eval (`:104`, the suite menu; `inventory/commands-a.md:44` gives its AskUserQuestion as "Yes"), cli-portify (`:105`), recommend (`:115`), review-translation (`:117`), roadmap (`:118`, "Resume? [Y/n]"), spec-panel (`:120`).
- Grading sentence: an implementer who follows P1 and section 2.3 dispatches `/sc:tdd "<topic>" --unattended --output <file>` in P1. The topic-only clarification still asks, and the row resolves it as blocked only in P2 (`:90`). The worker waits on a prompt and sends no `worker_done`, which WC-2 says must not happen under `--unattended`.
- Blocking: two stated texts contradict (`:60` and `:159`), and the outcome is a concrete stall.
- Recommendation: in P1, refuse `--unattended` with an error for every command whose WC-2 gate change is scheduled after P1, as M3 already does for the four outward commands, or move each named gate change into P1. Make `:159` and `:73` state the same list.

### N1 (Medium): WC-4 "the path section 3 gives" is not given by most rows

- Origin: changed. WC-4 `:62` and the section 3 intro `:76` are changed.
- Text: WC-4 `:62` says the command writes its contract "at the path section 3 gives for it". Many rows give no path: analyze `:99`, build `:101`, business-panel `:102`, cleanup `:103`, design `:106`, document `:107`, explain `:108`, index `:111`, test `:123`, improve `:110`, cli-eval `:104`, spec-panel `:120`. The directory-or-file rule in WC-4 `:62` depends on whether a new `--output` names a directory or a file, and the P1 rows that add `--output` do not say which.
- Wrong outcome: two implementers choose different kinds for `analyze --output`. The coordinator then opens a path that does not exist, or writes into a file path. AC-1.2 `:204` passes `--output <dir>`, which settles the test case but not the rule.
- Grade: Medium. The implementer must guess the kind; no data loss or safety boundary is involved.
- Recommendation: give the contract path as a column in section 3, or state a default for new `--output` flags (a directory).

### N2 (Medium): AC-0.4 step 3 for troubleshoot has no defined `--outcome` source

- Origin: changed. AC-0.4 `:202` is changed.
- Text: AC-0.4 `:202` says step 3 "checks `--outcome` against the existing report". WC-5 `:63` maps `--outcome` from the report's status. Troubleshoot's report is `REPORT.md` (`:91`), and the inventory records no status field for it (`inventory/commands-b.md:49`).
- Wrong outcome: an implementer applying WC-5 "otherwise succeeded" sends `succeeded`. Another reads prose in `REPORT.md` as "says failed" and sends `failed`. The check does not say which.
- Grade: Medium. A reading must be chosen; the failure is a check that passes on either reading.
- Recommendation: state the expected `--outcome` for troubleshoot's `REPORT.md` in AC-0.4.

### N3 (Medium, UNVERIFIED): AC-0.4 step 4 for adversarial depends on a file name the table says is not fixed

- Origin: changed. AC-0.4 `:202` is changed.
- Text: AC-0.4 requires "workflow's and adversarial's existing `return-contract.yaml` must be non-empty and parse as YAML". The adversarial row `:83` gives its report today as "contract, but filename not fixed" and makes the P1 fix rename it to `<output>/adversarial/return-contract.yaml`.
- Wrong outcome: a correct P0 run can fail the step if adversarial writes another name or another path under `--output`. The check does not say where to look. Whether adversarial writes `return-contract.yaml` today is UNVERIFIED in this workspace (the codegraph example at `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` is outside it).
- Grade: Medium.
- Recommendation: name the search (for example `find <dir> -name return-contract.yaml`), or limit adversarial's P0 step 4 to presence of its report.

### N4 (Medium): D2(b) conflicts with the WC-3 exception

- Origin: changed. The conflicting text is WC-3 `:61`, which is changed. D2 `:241-244` is unchanged.
- Text: D2(b) `:244` says the coordinator answers the worker's `ask` with the person's words, "which the worker records verbatim as the Ruling". WC-3 `:61` says no `ask` answer supplies a gate guarding a Ruling.
- Wrong outcome: a user who chooses D2(b) gets an implementation that WC-3 forbids. D2 does not say WC-3 must be amended for that choice.
- Grade: Medium. The decision is open, so no defect exists unless (b) is chosen.
- Recommendation: state in D2(b) that WC-3's exception must be amended for that option, and name the clause.

### N6 (Medium): WC-11's timestamp rule is contradicted by fixed-path rows rated ready

- Origin: changed. Rows `:85` and `:86` are changed. WC-11 `:69` is unchanged.
- Text: WC-11 `:69` says "Default output paths carry a timestamp or the slug the coordinator passes". Cleanup-audit `:85` (`.claude-audit/pass<N>-summary.md`) and index-repo `:86` (`PROJECT_INDEX.md`) keep fixed paths and are rated ready.
- Wrong outcome: none if the coordinator follows section 2.3 `:73`, which serializes them. As written, the two texts contradict.
- Grade: Medium.
- Recommendation: add to WC-11 the exception for fixed-path commands that section 2.3 serializes.

### N7 (Medium): WC-5 leaves a contract with no `status` key undefined

- Origin: changed. WC-5 `:63` is changed.
- Text: WC-5 `:63` sends `succeeded` "otherwise". A YAML contract with no `status` key is not empty and not unparseable, and it is outside the four values only if a reader extends "outside" to a missing key.
- Wrong outcome: a contract with no `status` reaches the coordinator as `succeeded`, which is the same outcome M9 was raised to prevent.
- Grade: Medium.
- Recommendation: say in WC-5 that a missing `status` key is treated as an empty or invalid report, so `failed`.

### N8 (Medium): "safety boundary" in the WC-3 exception is undefined

- Origin: changed. WC-3 `:61` is changed.
- Text: the exception covers gates guarding "a Ruling, an outward action or a safety boundary". No section 3 row names a safety-boundary gate, and the term is not defined.
- Wrong outcome: an implementer who classes a gate as not a safety boundary lets a coordinator answer supply it.
- Grade: Medium.
- Recommendation: define "safety boundary" by reference to section 3's column (f) and WC-9, or list the gate classes per row.

## Guard condition boundary table (changed-line guards only; re-review scope)

Table is produced for the guards on changed lines, per FR-8 to FR-10 in the re-review scope. Input classes with no possible input are left out, with the reason in the Specified Behavior column.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 failed trigger | `:63` | Zero/Empty | 0-byte `return-contract.yaml` | failed | `failed` ("empty") | OK |
| WC-5 failed trigger | `:63` | One/Minimal | unparseable one-line file | failed | `failed` ("unparseable") | OK |
| WC-5 failed trigger | `:63` | Typical | `status: succeeded` | not failed | `succeeded` | OK |
| WC-5 failed trigger | `:63` | Sentinel Value Match | `status: partial` | not failed | `succeeded`, per Decisions | OK |
| WC-5 failed trigger | `:63` | Legitimate Edge Case | YAML with no `status` key | not failed | falls to "otherwise", `succeeded` | GAP (N7) |
| WC-5 failed trigger | `:63` | Maximum/Overflow | left out: the status set is finite | n/a | n/a | n/a |
| WC-3 exception | `:61` | Typical | implement `E-NO-RULING` gate | blocked | blocked; no `ask` answer | OK |
| WC-3 exception | `:61` | Sentinel Value Match | post-release push gate answered "yes" by coordinator | blocked | blocked (`:67`) | OK |
| WC-3 exception | `:61` | Legitimate Edge Case | gate that is a safety boundary but not named | not classified | undefined | GAP (N8) |
| WC-3 exception | `:61` vs D2(b) `:244` | Ruling gate, option (b) chosen | coordinator relays person's words | conflicts | recorded verbatim, which WC-3 forbids | GAP (N4) |
| P1 refusal list | `:159` | Zero/Empty: gated command in 3.2 under `--unattended` | tdd topic-only prompt | accepted | WC-2 forbids the prompt | GAP (N5, blocking) |
| WC-4 path rule | `:62` | Typical: new P1 `--output` | `analyze --output <x>` | kind unstated | which path | GAP (N1) |
| AC-C1 pattern | `:172`, `:183` | Sentinel: planted line | `orca orchestration check --json` | match | the control matches | OK |

Not triggered: no multi-stage count pipeline on the changed lines, so no Quantity Flow Diagram. The State Variable Registry applies only under `--focus correctness`, which this run does not use.

## Noted, unactioned (not blocking)

- M4 (`:88`, reflect `--remediate` under `--unattended`): row unchanged; verifier rejected (`verify-1.md:13`). Still a note.
- M5 (AC-C1 `:172`, `src/superclaude/core` and SA-2 `:147`): AC-C1 greps `src/superclaude/core`, which will hold `WORKER-CONTRACT.md`, and SA-2 permits an Orca mention in the contract file. Verifier rejected it as conditional (`verify-1.md:14`). Still a note.
- M10 (AC-1.1 `:203`, load row `:112`): verifier rejected (`verify-1.md:19`). Still a note.
- Minor: the implement row `:109` and D2 `:241-244` do not cite WC-3 by name, which was part of M11's recommendation. The defect is closed by WC-3 `:61` itself.

## Follow-up candidates (Medium and minor; not blocking)

N1, N2, N3, N4, N6, N7, N8 and the minor notes above. The session that ran this review asks the user once whether to open an issue for them; no issue is created here.

## Reviser brief

Blocking finding ids: N5.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

The coordinator runs the VERIFY prompt on N5 before any revision. This report does not treat N5 as confirmed until that step.

verdict: FAIL

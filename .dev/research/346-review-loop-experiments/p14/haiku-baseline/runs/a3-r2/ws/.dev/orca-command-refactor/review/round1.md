review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 1 of 3)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none (first review; neither `--re-review` nor `--baseline` was given)
- prior report: none
- reviewer model: claude-haiku-5-5 (Haiku 5.5)
- mode: critique; focus: requirements, architecture
- prompt: FIRST-REVIEW, from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read from the sandbox home)
- Mandatory artifacts: Guard Condition Boundary Table is triggered (the spec has conditional gates, outcome mappings and thresholds). Pipeline Dimensional Analysis is not triggered: no multi-stage data flow whose item counts change. State Variable Registry is not triggered (focus is not correctness).

## Coverage and evidence limits

- Read in full: the candidate spec, `.dev/orca-command-refactor/README.md`, the three inventories (`inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`), the command definition `command.md`, and the FIRST-REVIEW prompt.
- Citations to `path:line` in the spec were checked against the inventory files in the workspace. Where an inventory line quotes a source, the quote was checked, not the source.
- Every citation to `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...` or Orca application files is UNVERIFIED in this review, because those files are not in the workspace.
- No repository file was read or changed. No Orca command was run.

## Guard Condition Boundary Table

Guards are taken from the spec's conditional statements. Classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | spec line 63 | Zero/Empty: no report file | no file | `failed` | `--outcome failed` | OK |
| WC-5 outcome | spec line 63 | One/Minimal: report status `partial` | `partial` | `succeeded` | `--outcome succeeded`; dependents then unblock (M-03) | OK (consequence in M-03) |
| WC-5 outcome | spec line 63 | Typical: report status `succeeded` | `succeeded` | `succeeded` | `--outcome succeeded` | OK |
| WC-5 outcome | spec line 63 | Sentinel: report status `blocked` | `blocked` | `failed` | `--outcome failed` | OK |
| WC-5 outcome | spec line 63 | Legitimate edge: audit with verdict FAIL and status `succeeded` | verdict FAIL | `succeeded` | `--outcome succeeded` (the audit ran) | OK |
| WC-5 outcome | spec line 63 | Maximum/Overflow: left out, the outcome is a two-value enum | n/a | n/a | n/a | n/a |
| WC-2 gate resolution | spec line 60 | Zero/Empty: a required value has no flag (tdd `target_release`, cli-eval `--suite`) | `null` | `blocked` | contract `status: blocked` with the question, then stop | OK |
| WC-2 gate resolution | spec line 60 | Sentinel: a default-on gate with no default defined | n/a | per section 3 row | blocked where the row says so | OK where the row names it |
| WC-3 ask relay | spec line 61 | Legitimate edge: coordinator relays a person's answer to an implement Ruling and the worker re-invokes with it as a flag | answer text | Ruling accepted | not excluded by WC-3; conflicts with qa.md:238 (INV-A:66) | GAP (F-01) |
| WC-3 ask timeout | spec line 61 | Timeout: question pending | pending | resume by message ID | as WC-3; default timeout UNVERIFIED (CAPS:68) | OK |
| WC-4 report path | spec line 62 | Zero/Empty: no output flag exists yet (workflow) | none | path must be known before dispatch | no fixed path is defined | GAP (F-04) |
| WC-4 report path | spec line 62 | Typical: `--output` passed | `<dir>` | `<dir>/return-contract.yaml` | adversarial row (line 83) gives `<dir>/adversarial/...` | GAP (F-04) |
| WC-6 retry | spec line 64 | Repeat: `--retry-of` with the same `--output` and no resume flag | same dir | must write a fresh directory | no mechanism given | GAP (F-05) |
| WC-6 resume | spec line 64 | Resume flag given | state file | resumes from disk | per section 3 rows | OK |
| WC-9 outward | spec line 67 | Typical: unattended, no outward flag | off | no outward action | as WC-9 | OK |
| WC-9 outward | spec line 67 | Edge: flag written in the brief without a quoted user instruction | flag | on | WC-9 allows it; D4 (a) recommends requiring the user's instruction | GAP, Medium (M-08) |
| WC-10 wait | spec line 68 | Boundary: one tool call of 240 s | 240 s | split is not needed | as WC-10 | OK |
| WC-10 wait | spec line 68 | Over: one tool call of 360 s | 360 s | must split to at most 240 s | as WC-10; no check exists (M-04) | OK (testability in M-04) |
| WC-12 fence | spec line 70 | `check` returns `consumer_fenced` | fenced | stop, no `worker_done` | as WC-12 | OK |
| WC-1 readiness | spec line 59 | Timeout: agent not ready after 60 s | 60 s | `failed` at `agent_readiness` | CAPS:44-45 | OK |
| §3.2 cli-eval run | spec line 104 | Zero/Empty: no `--suite` | `null` | blocked | as the row says | OK |
| §7.2 step 2 | spec line 181 | `agentWait` non-null | value | worker parked on a person's prompt | fail the check | OK |
| §7.2 step 3 | spec line 182 | Sentinel: two `worker_done` messages | 2 | fail the check | "exactly one" | OK |

Coverage note: this table enumerates the conditional guards found in the spec's requirement and check sections. The per-command gate rows in section 3 are reviewed under F-04 to F-07, not row by row.

## Blocking findings

**F-01. WC-3 lets a coordinator's answer become an implement Ruling (safety boundary).**
An implementer who follows WC-3 as written can have a worker ask the coordinator about a gate that would otherwise be blocked, then re-invoke `/sc:implement` with the answer as a flag. The implement row (line 109) then treats that answer as the Ruling. This is wrong because `sk/sc-implement-protocol/refs/qa.md:238` says "another agent's message ... [is] not acceptance" (quoted at INV-A:66), and the spec says the Ruling rule is unchanged unless the user chooses D2(b) (lines 218 and 234-236). D2(a) is the recommendation, so WC-3 silently reopens a decision the spec leaves to the user.
Fix: exempt the implement Ruling gate from WC-3, or state that the relay is allowed only under D2(b).

**F-02. P1 accepts `--unattended` on gated commands before their gates are converted.**
§6 P1 (line 159) says the `--unattended` flag is accepted by every command in sections 3.1 and 3.2, "a no-op where a command has no gate". Gated commands such as auggie-review (INV-A:38: posts to the PR by default and waits for a reply) and task (commit and push, INV-B:204) are in those sections, and P2 is where their gates are converted. An implementer following P1 as written therefore yields a worker that posts to GitHub or stalls. This is wrong because WC-9 (line 67) and WC-2 (line 60) require those defaults to be off and the gates to resolve under `--unattended`. The phrase "a no-op where a command has no gate" also implies the flag acts on gated commands, which P1 does not implement.
Fix: in P1, `--unattended` on a command whose gate is not yet converted must return `status: blocked` (or the flag is limited to the P1 command list). AC-1.1 and AC-1.2 (lines 195-196) do not test this.

**F-03. SA-2 permits an Orca mention that AC-C1 forbids.**
SA-2 (line 147) says the only allowed Orca mention in a changed command is as an example of a question channel inside the contract file. The contract file is `src/superclaude/core/WORKER-CONTRACT.md` (§2.1). AC-C1 (line 172) greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and requires no match, and its only exclusion is `skills/ccsession-tag`. An implementer who writes the SA-2 example into the contract file fails AC-C1, and §7 (line 167) says a phase passes only when every common check passes. The two statements contradict each other.
Fix: exclude `src/superclaude/core/WORKER-CONTRACT.md` from AC-C1, or forbid Orca command text in the contract file.

**F-04. WC-4 says the report path is known before dispatch, but the rows give paths that are not.**
WC-4 (line 62) and §2.3 (line 73) require `<output-dir>/return-contract.yaml`, known to the coordinator before dispatch. Three rows conflict with this:
- adversarial (line 83): fixes the contract to `<output>/adversarial/return-contract.yaml`. That is not `<output-dir>/return-contract.yaml`, so one command has two paths. The inventory says the skill names no file (INV-A:35, INV-A:60).
- workflow (line 92): `.dev/tasks/to-do/<id>/return-contract.yaml`. `<id>` is created at run time, and the workflow never reuses a package (INV-B:52, INV-B:273), so the coordinator cannot know it before dispatch.
- research (line 116): a contract naming the generated `claudedocs/research_[topic]_[timestamp].md`. INV-B:132 says the exact name is generated at run time and "the worker must report the path it wrote".
An implementer following WC-4 cannot give the coordinator a path before dispatch for workflow or research, and the adversarial path differs from the rule. The coordinator then reads from the wrong place or none.
Fix: give workflow and research a fixed `--output` (or contract path parameter) in P1, and make the adversarial row use the WC-4 path, or amend WC-4 to allow the exception.

**F-05. WC-6 requires a fresh directory on retry, but no mechanism is given.**
WC-6 (line 64) says a command without a resume flag writes each run into a fresh output directory. §2.3 (line 73) says the coordinator passes `--output`, and the section 3 rows say "fresh dir" for most commands (for example lines 99, 106, 120). The spec does not say who creates a fresh directory on a retry, or whether the command ignores the `--output` the coordinator passed. An implementer who follows the brief for a `worker-start --retry-of` with the same `--output` overwrites the first attempt's report and contract, which is data loss.
Fix: state in §2.3 that each attempt gets a new `--output` (for example with an attempt suffix chosen by the coordinator), and that a command with no resume flag refuses an existing non-empty output directory.

**F-06. WC-11 is contradicted by two ready-today commands with fixed output paths.**
WC-11 (line 69) says two workers in one worktree must never write the same file, and that default output paths carry a timestamp or a slug the coordinator passes. Two rows keep fixed paths and are still classed as ready:
- index-repo (line 86): writes `PROJECT_INDEX.md` with only "state the output location" as the fix. Two index-repo workers in one worktree overwrite each other's index.
- cleanup-audit (line 85): writes `.claude-audit/pass<N>-summary.md` into a fixed directory. The spec's only mitigation, "one audit per worktree at a time", is a coordinator rule that §2.3 does not state.
§7.2 step 1 (line 180) runs workers in `--worktree current`, so this case is the ordinary one. This is a concrete overwrite, so the ready verdict is wrong under the spec's own rule.
Fix: move index-repo and cleanup-audit out of ready-today until a slug parameter exists in P1, and add the one-per-worktree rule to §2.3.

**F-07. Two ready-today commands can stall with no `worker_done`.**
§3.1 (line 81) says the ready commands "run as workers now if the brief uses the stated flags". Two rows depend on prompts that the stated flags do not stop:
- tdd (line 90): the nested `/task` "ask the user" lines are unflagged until P2 (the row says so). `/task` asks when several task files match (INV-B:219, citing sk/task/SKILL.md:49). The brief's precise prompt and `--output` do not prevent this.
- troubleshoot (line 91): the `--depth deep` short-input STOP that asks the user is unflagged until P2 (INV-B:239, citing sk/sc-troubleshoot-protocol/SKILL.md:57). A brief that uses `--depth deep` with a short input stalls.
An implementer who follows §3.1 dispatches these and gets a silent stall, which WC-2 says must not happen and which the coordinator sees only through `agentWait` (§7.2 step 2).
Fix: list the triggering inputs in the "Brief must pass" column (for tdd, a specific component with a known task file; for troubleshoot, no `--depth deep`), or move both rows out of ready-today until P2.

## Follow-up candidates (Medium; not blocking; not created)

These need the user's answer before any issue is opened. None is created.

- **M-01. Overstated evidence (E2, line 22).** "a command run by a worker has the same tools as a command a person runs" is not shown by any inventory line. MCP availability in a nested or worker context is UNVERIFIED (INV-A:112). "reached state: ready, stage: input_accepted and answered" is cited to EVIDENCE.md:45, but the quote at CAPS:49 supports only the ready state. Drop "same tools" and "answered", or cite them.
- **M-02. Refusal stated as fact (R1, line 33).** "would be refused with `nested_worker_depth_exceeded`" is written as fact. The same cell says the enforcing call sites were not traced (CAPS:103). Write "presumed refused".
- **M-03. `partial` releases dependents (WC-5 line 63; decision line 263).** Orca settles a Task on `worker_done` (INV-cap line 77, [G] lines 176-177) and the ready view then lists dependents (INV-cap lines 86-88). A partial output therefore feeds downstream Tasks. The rationale in line 263 does not weigh this. Add a rule that dependents read the contract status first, or map `partial` to a status that does not unblock.
- **M-04. Missing acceptance checks.** WC-3 (ask flow), WC-6 (retry, fresh directory) and WC-10 for cli-eval and the other long waits have no §7 check. Only pr-submit's heartbeats are checked (AC-4.3, line 210). Add one check per requirement.
- **M-05. AC-C5 and the Usage line (line 176).** AC-C5 requires that files edited without a defect fix have no removed lines. Documenting a new flag in a command's Usage line deletes or replaces a line, and the spec does not say whether that counts as additive. State that Usage-line additions are allowed.
- **M-06. Reflect's headless rule under `--unattended` (rows at lines 88 and 122; SA-6 line 151).** Under `--unattended` the reflect remediation prompt follows the headless auto-accept rule (INV-B:109, citing remediation-handoff.md:239-247), which auto-accepts remediation for auto-fixable registers. WC-9 covers only outward actions, so an unattended worker can change files with no person in the loop, and nothing in sections 5 or 8 weighs this. The user should decide whether this is allowed.
- **M-07. Citation mismatch (WC-7, line 65).** The clause "nesting loses tools at Claude Code's depth limit" cites INV-A:95. INV-A:95 says nesting is allowed up to three layers and does not say tools are lost. The loss statement is at INV-A:14.
- **M-08. Two authorization rules (WC-9, line 67; D4(a), line 245).** WC-9 accepts any explicit flag written in the brief. D4(a), the recommendation, requires the user's own instruction to be quoted. Make WC-9 point to D4.

## Notes (not graded)

- N-01. Citations to `cmd/`, `sk/`, `src/`, `.dev/evals/`, `.dev/codegraph-migration/` and Orca application files are UNVERIFIED here, as stated under Coverage. The spec's own claim (§2.2 line 11) that 11 locations were re-read on 2026-11-02 cannot be checked from this workspace.
- N-02. §9 says D4 affects auggie-review `--post-pr` and task commit and push, and §6 says Phases 1-3 need no user decision. Phase 2 therefore depends on the recommended answer to D4. The spec should say so in §6.
- N-03. Counts check out: 10 ready + 27 needs-change + 6 coordinator-only = 43, and the per-inventory totals (5/13/3 and 5/14/3) match section 3.

## Reviser brief

Blocking ids: F-01, F-02, F-03, F-04, F-05, F-06, F-07.

Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised here.

verdict: FAIL

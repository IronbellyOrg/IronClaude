review: 1 of 3

# /sc:spec-panel critique, round 1: Orca worker-contract spec

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines), SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review` or `--baseline`)
- Focus: requirements, architecture. Mode: critique. Brief: FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full.
- Reviewer: claude-haiku-5-5 (Haiku 5.5), one reviewer. `superclaude review panel resolve` and `superclaude review merge` were not run (no superclaude runtime in this sandbox), so no ledger was kept.
- Citation keys: `SPEC:N` = candidate line N; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Every other path is UNVERIFIED by this reviewer (see Coverage).

## Summary

- 8 blocking findings (F1-F8). Verdict FAIL.
- 12 follow-up candidates (F9-F20), Medium grade, do not fail the review.
- The spec is strong on evidence and on the decision in section 1, but its acceptance gates are the weak point. Three P0-P1 checks cannot pass or cannot fail as written (F1, F2, F6), one gate cannot detect the risk it is meant to test (F7), and two requirements contradict the spec's own ready list (F4, F5).

Expert panel order used: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, active in every panel review). Crispin and Gregory were not in focus; acceptance-check text was reviewed under Adzic and Wiegers.

## Finding register

| ID | Grade | Category | Lead expert | Where |
|---|---|---|---|---|
| F1 | Blocking, MAJOR | unpassable-check | Adzic | SPEC:183, SPEC:194 |
| F2 | Blocking, MAJOR | unpassable-check | Adzic | SPEC:195, SPEC:76, SPEC:159 |
| F3 | Blocking, MAJOR | contradiction | Fowler | SPEC:16, SPEC:105, SPEC:108, SPEC:118, SPEC:125, SPEC:149 |
| F4 | Blocking, MAJOR | data-loss | Wiegers | SPEC:64, SPEC:87 |
| F5 | Blocking, MAJOR | contradiction | Fowler | SPEC:69, SPEC:85, SPEC:86 |
| F6 | Blocking, CRITICAL | unpassable-check | Adzic | SPEC:172 |
| F7 | Blocking, MAJOR | other | Adzic | SPEC:43, SPEC:184, SPEC:194 |
| F8 | Blocking, MAJOR | other | Hohpe | SPEC:63, CAPS:86, CAPS:142-144 |
| F9 | Medium | missing-requirement | Wiegers | SPEC:59, SPEC:158-162 |
| F10 | Medium | contradiction | Fowler | SPEC:158 |
| F11 | Medium | other | Hohpe | SPEC:63, SPEC:73 |
| F12 | Medium | other | Newman | SPEC:67, SPEC:88 |
| F13 | Medium | missing-requirement | Cockburn | SPEC:61, SPEC:90 |
| F14 | Medium | unpassable-check | Adzic | SPEC:185, SPEC:65 |
| F15 | Medium | unpassable-check | Hohpe | SPEC:61, SPEC:181 |
| F16 | Medium | other | Newman | SPEC:62 |
| F17 | Medium | other | Fowler | SPEC:147, SPEC:172 |
| F18 | Medium | other | Wiegers | SPEC:79, INV-A:60, INV-B:274 |
| F19 | Medium | other | Nygard | SPEC:85 |
| F20 | Medium | other | Wiegers | SPEC:60 |

=== REQUIREMENTS ANALYSIS ===

### F1 (blocking, MAJOR): P0 step 4 cannot pass on the commands P0 names. Expert: Adzic (lead), Wiegers.
- Evidence: SPEC:194 runs `/sc:troubleshoot` and `/sc:workflow` in P0 and says step 4 "uses the command's existing report file, since the contract arrives in P1." SPEC:183 asserts `d['status']` in four values and `d['command']` on a YAML file. Troubleshoot's report is `REPORT.md` (`report_path`, INV-B:242), which is not YAML. Workflow's existing contract lists `status`, `plan_path`, `reflect_report_path` (INV-B:272) and no `command` key.
- Recommendation: make step 4 command-specific for P0 (YAML check only for the command that already writes YAML; for REPORT.md check existence and a status line), or move the contract requirement for these two commands into P1.
- Priority: High. Quality impact: High (the P0 gate decides whether section 1 stands).

### F2 (blocking, MAJOR): AC-1.1 requires a section that P1 does not add. Expert: Adzic (lead), Wiegers.
- Evidence: SPEC:195 says the test asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section". SPEC:76 gives that section only to "Every changed command". SPEC:84 and SPEC:87 (brainstorm, init-lite) list no change. SPEC:159 scopes P1 to 13 commands of the 37 in 3.1-3.2, yet the same row says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
- Recommendation: state one rule. Either AC-1.1 checks only the commands changed in the phase, or P1 names all 37 commands. Rewrite the SPEC:159 row so its scope and command list agree.
- Priority: High. Quality impact: High (P1 cannot pass as written).

### F3 (blocking, MAJOR): Section 1.1 limits command changes to section 2, but section 3 requires others. Expert: Fowler (lead).
- Evidence: SPEC:16 says "What changes in the commands is limited to the worker contract in section 2: a way to run without a person, a fixed report file, and a resume or safe re-run." SPEC:108 requires adding Write to explain's tools; SPEC:118 requires reconciling roadmap's flags with its skill; SPEC:125 fixes validate-tests' default target; SPEC:105 removes cli-portify's hardcoded template path. SA-4 (SPEC:149) allows edits "where section 3 names a defect fix".
- Recommendation: rewrite SPEC:16 as "the contract plus the defect fixes named in section 3".
- Priority: High. Quality impact: High (an implementer following 1.1 skips required edits).

### F4 (blocking, MAJOR): Init-lite's re-run overwrites the first attempt's report. Expert: Wiegers (lead), Newman.
- Evidence: SPEC:87 gives init-lite "Re-run overwrites its marked report" under the resume column, marks it ready with no fix, and uses `--output <file>`. SPEC:64 (WC-6) requires a retry to "not corrupt the first attempt's output" and, without a resume flag, a fresh output directory. Init-lite's `--output` is a file, not a directory.
- Recommendation: give init-lite a per-run output directory in unattended mode (or a run-stamped file), or move it to P1 with that fix.
- Priority: High. Quality impact: Medium-High (report loss on retry).

### F5 (blocking, MAJOR): Index-repo is ready today despite a fixed default output. Expert: Fowler (lead), Nygard.
- Evidence: SPEC:69 (WC-11) requires "Default output paths carry a timestamp or the slug the coordinator passes", and two same-file writers must never happen. SPEC:86 ranks index-repo ready with brief flags "none" and default output "`PROJECT_INDEX.md` (location implied)". SPEC:85 leaves cleanup-audit's fixed directory and relies on "one audit per worktree at a time (WC-11)", which is a coordinator habit, not a rule.
- Recommendation: give index-repo a slug or run-stamped default, or require `--output` in its brief and reclassify it as needs-change. Replace SPEC:85's coordinator rule with a Task dependency or an output-dir argument (see F19).
- Priority: High. Quality impact: High (silent clobbering of a shared index).

### F6 (blocking, CRITICAL): AC-C1 cannot fail. Expert: Adzic (lead).
- Evidence: SPEC:172 uses `\|` inside an ERE pattern, which matches a literal pipe. Reproduced in the sandbox: `printf 'orca-ide worktree create\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` printed nothing, while the same pattern with unescaped `|` matched that line. AC-C1 is the only mechanical gate for SA-2, which section 5 calls "a hard requirement on every phase" (SPEC:142).
- Recommendation: use `(orchestration|worktree|terminal|agent)` in the ERE, and add a positive control to the check (a fixture line that must match) so a broken pattern cannot pass silently.
- Priority: High. Quality impact: High (every phase's standalone guarantee is unchecked).

### F7 (blocking, MAJOR): The P0 nested-route check does not test the nested route. Expert: Adzic (lead), Hohpe.
- Evidence: SPEC:43 (section 1.4 item 1) says the earlier run "proves the nested route, not the direct route this spec requires," and P0 exists to close that gap. SPEC:194 says each run is "directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)". Step 5 (SPEC:184) passes on "no `AskUserQuestion` call". Nothing in steps 1-7 detects an Agent-tool wrapper.
- Recommendation: add to step 5 a pass condition such as "the first tool call that starts the command is a Skill or Bash invocation in the worker's own transcript, and no Agent call precedes it", and name the field that proves it.
- Priority: High. Quality impact: High (the one P0 test of the central decision cannot fail on its main risk).

### F8 (blocking, MAJOR): Any unrecognized status is reported as success. Expert: Hohpe (lead), Nygard.
- Evidence: SPEC:63 (WC-5) sends `--outcome failed` for "`failed` or `blocked`, or no report exists" and `--outcome succeeded` "otherwise". An empty contract file, or a misspelt status such as `fail`, therefore falls under "otherwise". CAPS:86 shows that a completed Task starts dependents, and CAPS:142-144 shows that a failed Task keeps them blocked.
- Recommendation: map "otherwise" to failed, and list the four accepted status values. Keep `succeeded` only for `succeeded` and `partial`.
- Priority: High. Quality impact: High (a broken report can release dependent work).

### F9 (Medium, MAJOR): The launch-path hazard has no owner. Expert: Wiegers.
- Evidence: WC-1 (SPEC:59) names its owner as "Launch setup, not commands". No phase (SPEC:158-162) or check (SPEC:191-210) fixes or verifies it. SPEC:59 cites the session-name prompt in EVIDENCE.md:39, which this reviewer could not check (UNVERIFIED).
- Recommendation: add a P0 task and check for the launch wrapper, or name the owner outside this spec.
- Priority: Medium. Quality impact: Medium.

### F10 (Medium, MAJOR): P0 builds before it tests. Expert: Fowler.
- Evidence: SPEC:158 says the smoke runs "test the decision before anything is built on it", but the same row writes WORKER-CONTRACT.md, the HOW-WE-WORK Orca section and a test file before those runs.
- Recommendation: move the smoke runs to the start of P0, or drop the rationale and say the files are reversible.
- Priority: Medium. Quality impact: Medium.

### F13 (Medium, MAJOR): Nested skills do not receive --unattended. Expert: Cockburn (lead).
- Evidence: SPEC:90 says that under `--unattended` the nested `/task` "ask the user" lines "resolve as blocked (P2)". No row edits `sk/task/SKILL.md`, and the spec gives no rule for how `--unattended` reaches skills a command invokes. Stage 10.5 passes it explicitly (SPEC:122), so the mechanism is inconsistent between rows.
- Recommendation: state a propagation rule (command passes the flag to each skill it invokes) and add the task skill to the change list.
- Priority: Medium. Quality impact: Medium-High (a silent stall in tdd).

### F14 (Medium, MAJOR): The shared-worktree git check fails correct runs. Expert: Adzic.
- Evidence: SPEC:185 requires `git status --short` to show "only files under the brief's output directory". SPEC:65 (WC-11) and CAPS:115 put workers in the current worktree by default, so another worker's or the coordinator's edit fails the check.
- Recommendation: compare against a baseline status taken before dispatch, and check only paths the worker wrote.
- Priority: Medium. Quality impact: Medium.

### F15 (Medium, MAJOR): Step 2 may fail a permitted ask. Expert: Hohpe.
- Evidence: SPEC:181 requires `observation.agentWait` to be "never non-null". WC-3 (SPEC:61) allows the worker to block in `ask` for the coordinator. CAPS:129 describes agentWait as a prompt only a human can answer. Whether a coordinator-owned ask sets agentWait is UNVERIFIED.
- Recommendation: exempt a worker that is blocked in an open `ask` whose message ID is in the coordinator's inbox, and verify that rule once in P0.
- Priority: Medium. Quality impact: Medium.

### F16 (Medium, MAJOR): One file name, several schemas. Expert: Newman (lead), Wiegers.
- Evidence: SPEC:62 (WC-4) says commands that already write a contract "keep their fields and add the missing ones", and the contract carries no version. The fields therefore differ by command (INV-B:272 for workflow, INV-A:35 for adversarial's path).
- Recommendation: add `contract_version` and a per-command field table so the coordinator can validate one schema per command.
- Priority: Medium. Quality impact: Medium.

### F18 (Medium, MAJOR): "Ready today" rests on unconfirmed facts. Expert: Wiegers.
- Evidence: SPEC:79 says the ten ready commands "run as workers now if the brief uses the stated flags". Adversarial's contract location varied in the earlier run (INV-A:60). Workflow's staging under `.dev/tasks` is UNVERIFIED (INV-B:274), and SPEC:92 does not say so.
- Recommendation: mark the two unverified facts in 3.1 and keep those commands out of "ready" until P0 confirms them.
- Priority: Medium. Quality impact: Medium.

### F20 (Medium, MAJOR): Two unresolved gates have no rule. Expert: Wiegers.
- Evidence: WC-2 (SPEC:60) says a blocked command writes "the exact question" (singular). cli-eval and cross-gate commands can hit two gates at once.
- Recommendation: state that the contract lists every unresolved gate as an array.
- Priority: Medium. Quality impact: Low-Medium.

=== ARCHITECTURE ANALYSIS ===

### F12 (Medium, MAJOR): Local mutations sit outside WC-9. Expert: Newman (lead).
- Evidence: WC-9 (SPEC:67) covers push, PR, GitHub posts, installs, provisioning and paid runs. Reflect's default UC-2 folder move (INV-B:114) and the P2 change that makes `--remediate` follow the headless auto-accept rule (SPEC:88) are local but consequential, and neither is covered. SPEC:88 also makes a default act where WC-2(c) says blocked.
- Recommendation: extend WC-9 to "any change outside the brief's output directory", and make `--no-promote` part of the reflect brief.
- Priority: Medium. Quality impact: Medium-High.

### F17 (Medium, MAJOR): The AC-C1 scope reaches core. Expert: Fowler.
- Evidence: SPEC:172 scans `src/superclaude/core`, where P0 adds the HOW-WE-WORK Orca section (SPEC:158). SA-2 (SPEC:147) allows Orca mentions only in the contract file. No exemption covers the routing guide.
- Recommendation: decide whether the routing guide may mention Orca commands; if yes, add the exemption to AC-C1.
- Priority: Medium. Quality impact: Low.

### F19 (Medium, MAJOR): Mutual exclusion is not encoded. Expert: Nygard (lead).
- Evidence: SPEC:85 says "one audit per worktree at a time (WC-11)" but nothing in the spec enforces it, and CAPS:86 describes independent Tasks starting in parallel.
- Recommendation: give cleanup-audit a run-stamped output directory, or create a dependency chain in the coordinator template (section 2.3).
- Priority: Medium. Quality impact: Medium.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the contract file is empty or its status is not one of the four values**. Concrete attack: **the worker writes an empty return-contract.yaml after a crash; WC-5 maps it to "otherwise", so `worker_done --outcome succeeded` is sent and the dependent Task starts (CAPS:86)**. See F8.
- I can break this specification by **Sequence Attack**. The invariant at **cleanup-audit row (SPEC:85)** fails when **two sibling Tasks start in one worktree**. Concrete attack: **the coordinator starts two audits from the ready view (CAPS:86) with no dependency between them; both write `.claude-audit/` and each `progress.json` overwrites the other**. See F19.
- I can break this specification by **Divergence Attack**. The invariant at **WC-2 (SPEC:60)** fails when **a gate has a documented default that acts**. Concrete attack: **reflect runs `--remediate` under `--unattended`, the P2 headless auto-accept applies, and remediation changes files before any person reads REPORT.md**. See F12.

Grading of the attacks: the Zero/Empty attack is blocking (F8); the Sequence and Divergence attacks are follow-up candidates (F19, F12), because each needs a coordinator or process choice the spec leaves open.

=== GUARD CONDITION BOUNDARY TABLE (mandatory; triggered by the spec's conditional rules) ===

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-2 gate resolution | SPEC:60 | Zero/Empty: gate with no default and no caller flag | no flag | blocked | writes status blocked and the exact question, then stops | OK |
| WC-2 gate resolution | SPEC:60 | Typical: caller supplies the value as a flag | `--suite <x>` | not blocked | uses the flag value (WC-2 b) | OK |
| WC-2 gate resolution | SPEC:60 | Sentinel: outward default with flag absent | no `--post-pr` | off | WC-9 off by default (SPEC:67) | OK |
| WC-2 gate resolution | SPEC:60 | Accumulation: two unresolved gates in one run | two gates | blocked | "the exact question" is singular | GAP (F20) |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty: no report file | none | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty: file present, empty or without a status | empty file | "otherwise", so succeeded | not specified as failed | GAP (F8, blocking) |
| WC-5 outcome mapping | SPEC:63 | Typical: status `succeeded` | `succeeded` | succeeded | as written | OK |
| WC-5 outcome mapping | SPEC:63 | Typical: status `failed` or `blocked` | `blocked` | failed | as written | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel: status `partial` | `partial` | succeeded | decision at SPEC:263 | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate edge: audit with verdict FAIL | status succeeded | succeeded | dependents may start (F11) | GAP (F11) |
| WC-6 resume or fresh | SPEC:64 | Zero/Empty: first attempt, no prior output | none | fresh run | as written | OK |
| WC-6 resume or fresh | SPEC:64 | Typical: retry with resume flag | `--resume <x>` | resumes | as written | OK |
| WC-6 resume or fresh | SPEC:64 | Typical: retry, no resume flag, same `--output` file (init-lite) | same path | overwrites | contradicts WC-6 | GAP (F4, blocking) |
| WC-6 resume or fresh | SPEC:64 | Sentinel: fixed default directory shared by two workers (index-repo, cleanup-audit) | same path | clobbers | contradicts WC-11 | GAP (F5, blocking; F19) |
| WC-12 check result | SPEC:70 | `consumer_fenced` | returned | stop without `worker_done` | as written (CAPS:49-52) | OK |
| WC-12 check result | SPEC:70 | empty check | none | keep waiting | as written (CAPS:52) | OK |
| WC-10 wait size | SPEC:68 | Legitimate edge: eval runs up to 3600 s | 3600 | split into waits of at most 240 s | poll runtime UNVERIFIED (SPEC:283) | OK (conditional) |
| D1 mode switch | SPEC:228 | Legitimate edge: a person's own Orca tab with the terminal variable set | set, no flag | prompts kept | recommendation (a) | OK (conditional on SPEC:284) |

Omitted classes, one line each: One/Minimal and Typical are merged where they behave alike; Maximum/Overflow has no numeric bound in any of these guards. Not numbered: a `check` error other than `consumer_fenced` or an empty result has no specified behavior (a minor note). Table is hard-gate complete for the guards listed; FR-8 applies to the GAP rows, and only F4 and F8 are blocking GAPs.

Pipeline Dimensional Analysis (FR-17): not triggered. No stage in the spec describes an output count that differs from its input count; Task waves (CAPS:86) are ordering, not counts. Quantity Flow Diagram and Pipeline Flow Diagram: not produced for that reason. State Variable Registry: not produced (correctness focus is not active).

## Follow-up candidates (Medium and minor; not blocking)

- F9 to F20 as listed above.
- Minor note: `check` returning an error other than `consumer_fenced` or an empty result has no specified behavior (WC-12, SPEC:70).
- Minor note: SPEC:23 cites `.dev/codegraph-migration/orchestration/README.md`, which is outside the checkable evidence (UNVERIFIED here).
- The session that ran this review asks the user once whether to open issues for these follow-up candidates. No issue is created by this reviewer.

## Coverage

- Read in full: `command.md`; `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy); `.dev/orca-command-refactor/README.md`; the candidate `specs/orca-worker-contract-spec.md`; `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.
- Checked by tool in the sandbox: every quoted anchor was found in the candidate with `grep -F` (count 1 each); the AC-C1 regex was run on a positive control (F6).
- Not checked, so UNVERIFIED by this reviewer: every citation to `src/`, `sk/`, `cmd/`, `.dev/evals/`, `.dev/codegraph-migration/`, the Orca binaries and `~/.claude/` files, and the `CLAUDE.md` rules quoted in the brief. Findings F9, F15 and F18 rely partly on those citations and say so.
- No commands were run in the workspace; no file other than `review/round1.md` was written.

## Decisions

- Single reviewer, because no superclaude panel runtime exists here.
- Medium is used for "needs a guess" findings (F9-F20). A finding is blocking only where the stated text, read as written, gives a wrong outcome or an unpassable or non-failing check, which F1-F8 each show.
- Placement: the Reviser brief sits directly above the verdict line, as the command requires. That places the Findings block one section above it, so the findings block is the last section before the brief. The review-loop prompt asks for the block to be the last section, and the two placement rules conflict here; this reviewer resolved the conflict in that order.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']", "anchor2": "step 4 uses the command's existing report file, since the contract arrives in P1.", "refs": ["AC-0.4", "7.2 step 4", "WC-4"], "claim": "A correct P0 run of troubleshoot or workflow fails step 4, because REPORT.md is not YAML and the workflow contract lists no command key (INV-B:242, INV-B:272)."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section", "anchor2": "Every changed command also gains the `## Unattended mode` section", "refs": ["AC-1.1", "3 intro", "6 P1"], "claim": "AC-1.1 demands the section in all 37 commands of 3.1-3.2, but P1 covers 13 and the section 3 intro gives it only to changed commands, so P1 cannot pass as written."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "What changes in the commands is limited to the worker contract in section 2", "anchor2": "add Write to its tools (only Read/Grep/Glob, TodoWrite, Task today)", "refs": ["1.1", "SA-4", "3.2 explain", "3.2 roadmap", "3.2 validate-tests"], "claim": "Section 1.1 limits command changes to the section 2 contract, while section 3 and SA-4 require the explain tools, roadmap, validate-tests and cli-portify edits, so an implementer following 1.1 skips required changes."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "data-loss", "anchor": "Re-run overwrites its marked report", "anchor2": "must not corrupt the first attempt's output", "refs": ["WC-6", "3.1 init-lite"], "claim": "A retry of init-lite with the same --output file overwrites the first attempt's report, which WC-6 forbids."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "anchor2": "`PROJECT_INDEX.md` (location implied)", "refs": ["WC-11", "3.1 index-repo", "3.1 cleanup-audit"], "claim": "Two index-repo workers in one worktree both write the fixed default PROJECT_INDEX.md, which WC-11 forbids, yet the spec ranks index-repo ready with brief flags none."}
{"id": "F6", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "SA-2", "5"], "claim": "The AC-C1 grep uses an escaped alternation in an ERE, matches a literal pipe, and printed nothing on a positive control in the sandbox, so SA-2 is never checked."}
{"id": "F7", "severity": "MAJOR", "blocking": true, "category": "other", "anchor": "no Agent-tool wrapper, verified in the step-5 transcript", "anchor2": "no `AskUserQuestion` call", "refs": ["AC-0.4", "7.2 step 5", "WC-7", "1.4 item 1"], "claim": "AC-0.4 says the no-Agent-tool-wrapper condition is verified in step 5, but step 5 passes on the absence of AskUserQuestion alone, so a subagent-wrapped run passes P0."}
{"id": "F8", "severity": "MAJOR", "blocking": true, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "anchor2": "`--outcome failed` when the report says `failed` or `blocked`, or no report exists", "refs": ["WC-5", "CAPS:86", "CAPS:142-144"], "claim": "An empty contract or a misspelt status falls under otherwise and is sent as succeeded, which can release dependent Tasks."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Any such prompt must fall back on its own well inside the readiness limit", "anchor2": "Launch setup, not commands", "refs": ["WC-1", "6", "7.3"], "claim": "WC-1 assigns the launch path to an owner that no phase or check covers."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "the smoke runs test the decision before anything is built on it", "refs": ["6 P0"], "claim": "P0 writes the contract, the routing-guide section and a test file before its smoke runs, which its own rationale says must come first."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "including an audit whose verdict is FAIL (the audit itself succeeded)", "refs": ["WC-5", "2.3", "CAPS:86"], "claim": "A FAIL audit is sent as succeeded, so dependents can start unless the coordinator reads the report first, which is a process rule rather than a Task rule."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`--no-promote` when the coordinator owns folder moves", "anchor2": "make `--remediate` follow the existing headless auto-accept rule", "refs": ["WC-9", "3.1 reflect", "3.2 reflect"], "claim": "Local changes such as reflect's folder move and a headless auto-accept of remediation are outside WC-9's list of outward actions."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the topic-only clarification and nested `/task`", "refs": ["WC-2", "3.1 tdd", "3.2 tasklist", "122"], "claim": "No row edits the task skill and no rule says how --unattended reaches nested skills, so tdd keeps its nested ask lines."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "only files under the brief's output directory", "anchor2": "Two workers in one worktree must never write the same file.", "refs": ["7.2 step 6", "WC-11", "CAPS:115"], "claim": "Step 6 fails any run while another worker or the coordinator has an edit in the shared worktree."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "`observation.agentWait` is never non-null", "anchor2": "the session may instead ask the coordinator once with the preamble's", "refs": ["7.2 step 2", "WC-3", "CAPS:129"], "claim": "A worker that blocks in a permitted WC-3 ask may show a non-null agentWait, so step 2 fails a permitted path; the Orca behaviour is UNVERIFIED."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Commands that already write a contract keep their fields and add the missing ones", "refs": ["WC-4", "6 P1"], "claim": "The shared contract has no version and keeps per-command fields, so one file name can carry several schemas."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core", "anchor2": "The only allowed mention of Orca in a changed command", "refs": ["AC-C1", "SA-2", "6 P0"], "claim": "AC-C1 also scans src/superclaude/core, where P0 adds an Orca section, and no exemption covers it."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "These run as workers now if the brief uses the stated flags", "anchor2": "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", "refs": ["3.1", "INV-A:60", "INV-B:274"], "claim": "Ready-today status for adversarial and workflow rests on a contract path and a staging behaviour the spec does not confirm."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "output dir is fixed, so one audit per worktree at a time (WC-11)", "refs": ["WC-11", "3.1 cleanup-audit", "CAPS:86"], "claim": "Two cleanup-audit tasks can run in one worktree because no dependency or gate encodes the one-at-a-time rule."}
{"id": "F20", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "writes its report with `status: blocked` and the exact question", "refs": ["WC-2", "3.2 cli-eval", "AC-2.2"], "claim": "A command with two unresolved gates has no rule for which question the blocked contract carries."}
```

## Reviser brief

Blocking finding ids: F1, F2, F3, F4, F5, F6, F7, F8.

Restated rule (bullet 6 of the Review Loop): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

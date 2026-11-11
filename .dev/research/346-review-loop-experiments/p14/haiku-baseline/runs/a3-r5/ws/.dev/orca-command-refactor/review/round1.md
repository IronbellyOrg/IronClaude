review: 1 of 3

# Spec-panel critique: Orca worker-contract spec, round 1

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines; sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`)
- baseline: missing (first review, no `--baseline`)
- prior report: missing (first review, no `--re-review`)
- mode: critique; focus: requirements, architecture; format: standard
- experts: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (active in every panel review)
- reviewer model used: claude-haiku-5-5
- review prompt: FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy, read in full before review)
- citation rule: a citation is "checked" when its target is a file inside the workspace (`.dev/orca-command-refactor/`) and I read the cited line. Citations to `src/`, `.dev/evals/`, `pyproject.toml`, `CLAUDE.md` and Orca's installed files are outside the workspace and are marked UNVERIFIED in this run.

## Coverage

Read: the candidate (all 285 lines); `README.md` (binding shared context); `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md` (every cited line). Checked against the inventories: the 10 / 27 / 6 split in section 3 (spec lines 78-125, 127-137) matches the verdicts in the two inventories (`commands-a.md`: 5 ready, 13 needs-change, 3 coordinator-only; `commands-b.md`: 5 ready, 14 needs-change, 3 coordinator-only; combined 10 ready, 27 needs-change, 6 coordinator-only). The 43-command total matches the two inventory scopes (21 + 22). Spot-checked orca-capabilities citations CAPS:44-46, 49, 52, 58-61, 63-67, 72-80, 92, 97-103, 107-116, 121-130, 155-161, 178-188: each matched its quoted text. Acceptance commands were tested in the sandbox (see F-02). Not checked: any citation outside the workspace.

Guard-condition and pipeline outputs: the Guard Condition Boundary Table is produced below (the spec contains thresholds and guards). The Pipeline Dimensional Analysis is not triggered: the spec describes rollout phases and one report record per worker, with no multi-stage data flow whose counts change. The State Variable Registry is not produced: `--focus correctness` is not active.

=== REQUIREMENTS ANALYSIS ===

### F-01 (MAJOR, BLOCKING): AC-0.4 step 3 cannot pass in Phase 0

- Location: spec line 194 (AC-0.4) against line 182 (7.2 step 3) and line 158 (P0, "no command edits"). Inventory: `commands-b.md:272` (workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`), `commands-a.md:55` (init-lite writes no contract).
- Issue: AC-0.4 requires steps 1-3 to pass, and step 3 requires "its report path is the WC-4 contract path". AC-0.4 also says the WC-4 contract "arrives in P1". Phase 0 therefore has no WC-4 path for step 3 to match.
- Grading check: "An implementer who runs AC-0.4 as written in P0 finds step 3 cannot pass for any of the three commands, and that is wrong because P0 is the gate that decides whether section 1 stands (line 194, "a failure here reopens section 1")." This holds with no added assumption: the two stated texts contradict each other.
- Recommendation: in AC-0.4, make step 3 check the report path against the command's existing report file (`REPORT.md` for troubleshoot, the workflow `return-contract.yaml`, `<output>/adversarial/return-contract.yaml` as actually written), and state the WC-4 path check starts in P1.
- Expert: Adzic (acceptance criteria that cannot pass), Wiegers (traceability of the gate to its phase).

### F-03 (MAJOR, BLOCKING): WC-4 contract is not assigned to several commands it applies to

- Location: spec line 62 (WC-4: every command "writes `<output-dir>/return-contract.yaml` ... on success, failure, blocked and partial outcomes"); line 79 ("the worker reports the named file until Phase 1 adds the contract"); line 159 (P1 scope: "The WC-4 contract in unattended mode ... the --unattended flag accepted by every command in sections 3.1 and 3.2"); P1 "Commands" column at line 159 names 13 commands only.
- Issue: the rows assign no contract to init-lite (line 87, "Small fix: None"; `commands-a.md:55`, no contract), tdd (line 90; `commands-b.md:222`, report is the TDD file), troubleshoot (line 91; `commands-b.md:242`, `return-contract.yaml` only with `--caller task-unified`), release-split (line 89; `commands-b.md:122`, `release-split-report.md`), index-repo (line 86) and cleanup-audit (line 85), where P1 adds only a report name. Load (line 112, "none") and validate-tests (line 125) have no contract either. AC-1.2 (line 196) tests only "each P1 command", which does not include init-lite, tdd, troubleshoot or release-split.
- Grading check: "An implementer who follows the 3.1 'small fix' column and the P1 command list builds init-lite, tdd, troubleshoot and release-split without `return-contract.yaml`, and that is wrong because WC-4 requires the file on every outcome and line 79 says Phase 1 adds it." This holds with no added assumption: the P1 scope text and the row text contradict each other.
- Recommendation: add a contract row for each of these commands, or state an explicit WC-4 exemption (with reason) for `load` and `validate-tests`. Reconcile the P1 "Commands" column with the P1 scope sentence.
- Expert: Fowler (interface contract coverage), Wiegers (every requirement needs an owner).

### F-15 (MAJOR, MEDIUM): WC-5 leaves contract-status combinations undefined

- Location: spec line 63 (WC-5); line 263 (`partial` maps to `succeeded`); line 62 (WC-4 `status` set).
- Issue: WC-5 defines `failed`/`blocked`/no-report/otherwise. It does not say what happens for (a) a status outside the four-value set, (b) `status: partial` with a non-empty `blocked_question`, or (c) a body first sentence that contradicts `status`. The first sentence rule has no acceptance check.
- Grading: needs a guess that the worker picks the worse reading (for example `succeeded` for case b), so Medium. It goes under follow-up candidates.
- Recommendation: state precedence (a non-empty `blocked_question` forces `failed`, unknown status forces `failed`), and add an AC for the first-sentence rule.
- Expert: Whittaker (sentinel collision: `blocked_question` is a control signal that a `partial` status can hide).

### F-12 (MINOR, MEDIUM): several requirements have no acceptance check, and one is unquantified

- WC-1 (line 59): "well inside the readiness limit" has no number, and no AC tests "nothing in the launch path waits on a person" (the P0 smoke runs do not cover it).
- WC-5 first-sentence rule (line 63): no AC (see F-15).
- WC-6 (line 64): retry must not corrupt the first attempt's output; no AC.
- WC-12 (line 70): `consumer_fenced` stop; no AC.
- Recommendation: give WC-1 a number (for example a fallback of 30 s, which EVIDENCE cites as passing, and state the margin), and add one AC each for WC-6 and WC-12.
- Expert: Adzic, Wiegers.

### F-14 (MINOR, MEDIUM): P1 scope, P1 command list and AC-1.1 disagree on how many commands get the section

- Location: line 159 (scope says "every command in sections 3.1 and 3.2"; the Commands column names 13); line 195 (AC-1.1 requires `## Unattended mode` in every command in 3.1 and 3.2); line 196 (AC-1.2 names "each P1 command").
- Issue: a reader can take P1 as touching 13 commands (AC-1.2 then) or all 37 (AC-1.1 then). AC-1.1 cannot pass under the first reading.
- Grading: a reader must guess which reading applies, so Medium.
- Recommendation: state in P1 that the flag and the `## Unattended mode` section go to all 37 commands, and that P1's live check covers the 13 listed plus one spot-check of each other command.
- Expert: Wiegers.

### F-09 (MINOR, MEDIUM): the Phase 0 runs and section 3.1 briefs omit `--unattended`, which section 2.3 requires

- Location: line 73 (2.3: each brief states "the exact command line including `--unattended`"); line 79 and 81-92 (3.1 "Brief must pass" columns, no `--unattended`); line 158 and line 194 (P0 smoke runs without it); line 184 (7.2 step 5: transcript search for `AskUserQuestion`).
- Issue: P0 is the only evidence for the decision (line 43), and it runs the commands in attended mode, because the flag does not exist until P1. The spec does not say so. Step 5 then tests the wrong mode.
- Recommendation: state that P0 runs are attended, and that the unattended behaviour of each ready command is first tested in P1 (AC-1.2).
- Expert: Adzic.

### F-08 (MINOR, MEDIUM): the contract path rule does not match the paths the rows give

- Location: line 62 (`<output-dir>/return-contract.yaml`, known before dispatch); line 83 (adversarial `<output>/adversarial/return-contract.yaml`); line 92 (workflow `.dev/tasks/to-do/<id>/return-contract.yaml`); line 228 (D1 example uses `/sc:troubleshoot ... --output .dev/troubleshoot/login/`); line 91 (troubleshoot "Brief must pass" lists no `--output`).
- Issue: the `<id>` in the workflow path is generated per package (`commands-b.md:273`, "Never overwrites or reuses an existing package"), and whether the brief can supply it is not stated, so the path may not be known before dispatch. The D1 example uses a flag that the troubleshoot row does not confirm (`commands-b.md:242` gives only a default output directory).
- Recommendation: make WC-4 accept a per-command path rule, state whether the coordinator may pass the workflow `<id>`, and confirm `--output` for troubleshoot before using it in the D1 example.
- Expert: Fowler (interface drift).

### F-10 (MINOR, MEDIUM): the worker-session rules have no stated loader

- Location: lines 61, 63, 65, 68 and 70 (WC-3, WC-5, WC-7, WC-10, WC-12 bind "the worker session"); line 52 (contract file is read by commands through their `## Unattended mode` section); line 73 (2.3 brief template does not tell the worker to read `~/.claude/WORKER-CONTRACT.md`).
- Issue: a command loads the contract only when it runs. Outcome mapping (WC-5) and heartbeat (WC-10) happen in the worker session, before or after the command. The spec does not say how the worker session learns those rules, beyond the preamble, which the spec does not describe for this purpose.
- Recommendation: add a line to the 2.3 brief template: "read `~/.claude/WORKER-CONTRACT.md` sections 'Worker session' before starting".
- Expert: Cockburn (who is the actor for each rule).

### F-16 (MINOR, MEDIUM): re-invoking a blocked command with the answer conflicts with the fresh-directory default

- Location: line 61 (WC-3: worker may "re-invoke or resume the command with the answer as a flag"); line 64 (WC-6: a command with no resume flag "writes each run into a fresh output directory"); section 3.2 "fresh dir" column (line 97 header; most rows).
- Issue: a re-invocation after an answer starts a fresh directory, so the blocked run's partial output is left behind and not reused. The spec does not say whether the answered run should reuse the blocked run's directory.
- Recommendation: state that the answered re-invocation uses the same output directory where the command has a resume flag, and a new directory where it does not, with the blocked run's directory named in the contract.
- Expert: Hohpe (message ordering across ask and re-invoke).

### F-17 (MINOR, MEDIUM): WC-10 boundary and cadence are not specified at the threshold

- Location: line 68 (WC-10: heartbeat every 5 minutes; split waits "longer than 5 minutes" into at most 4 minutes); line 181 (7.2 step 2: `worker-show` at least once per 5 minutes).
- Issue: a call of exactly 300 s is not covered (the rule says "longer than"). A step of 4 min 59 s plus model time can exceed the 5-minute heartbeat cadence, and the spec does not say whether the heartbeat is sent between calls only.
- Recommendation: say "at most 4 minutes" applies to any call of 5 minutes or more, and state that the heartbeat cannot be sent during a tool call.
- Expert: Nygard (failure and liveness timing).

### F-18 (MINOR, MEDIUM): the outward-action guard has no checkable authorization

- Location: line 67 (WC-9: outward flag "written in the brief"); line 244-247 (D4 recommended (a): the coordinator quotes the user's instruction in the brief).
- Issue: a command cannot check that a quote is genuine. The guard depends entirely on the coordinator's brief, which D4 leaves open.
- Grading: safety-boundary-adjacent, but D4 is an open user decision and the default (flag absent) is off, so Medium pending D4.
- Recommendation: make D4 a precondition in section 2.3 (the brief names the authorizing user message), and add it to AC-2.4.
- Expert: Nygard.

=== ARCHITECTURE ANALYSIS ===

### F-02 (MAJOR, BLOCKING): the AC-C1 grep never matches, so the mechanical gate for SA-2 and WC-8 always passes

- Location: spec line 172 (AC-C1, `grep -rnE '...(orchestration\|worktree\|terminal\|agent)\b' ...`); line 147 (SA-2); line 66 (WC-8); line 213 (non-goal 1).
- Issue: under `grep -E` (ERE), `\|` matches a literal `|`, not alternation. The pattern as written therefore matches no `orca orchestration`, `orca worktree` or `orca-ide terminal` text. I tested this in the sandbox with three sample lines: the spec's escaping returned exit 1 with no output; the same pattern with plain `|` matched all three.
- Grading check: "An implementer who runs AC-C1 as written gets empty output and records a pass, while a command still calls `orca orchestration`, and that is wrong because SA-2 is a hard requirement on every phase (line 142) and this is its only mechanical check." This holds with no added assumption.
- Recommendation: change `\|` to `|` (or use `grep -E` with `(orchestration|worktree|terminal|agent)`), then re-run the sample test and keep it as a fixture in `tests/skills/test_worker_contract.py`.
- Expert: Fowler (fitness function for a boundary), Nygard (safety rule with a silent gate).

### F-04 (MAJOR, BLOCKING): cleanup-audit is ready to run as a worker only if two workers cannot share a worktree, and the spec does not enforce that

- Location: line 85 (cleanup-audit row: output dir "is fixed, so one audit per worktree at a time (WC-11)"); line 69 (WC-11: "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes"); line 73 (2.3: the brief's contents, which contain no concurrency rule); `commands-a.md:42` (`.claude-audit/pass<N>-summary.md` and `progress.json` are fixed paths).
- Issue: cleanup-audit's default paths carry neither a timestamp nor a slug, so WC-11 is not met. The row cites WC-11 for a "one at a time" rule that WC-11 does not contain, and no brief rule or AC enforces it.
- Grading check: "An implementer who follows the cleanup-audit row dispatches two audit workers into one worktree; the second overwrites `progress.json`, and that is wrong because the resume checkpoint is lost and WC-11 says two workers must never write the same file." This holds with no added assumption: the row's stated mitigation is not in any rule the coordinator applies.
- Recommendation: give cleanup-audit a per-run output path in P1 (a slug the coordinator passes), or add the one-at-a-time rule to section 2.3 and an AC that checks it.
- Expert: Nygard (data loss on concurrent writes), Hohpe (shared-state ordering).

### F-05 (MINOR, MEDIUM): the evidence for the central decision mixes two different runs

- Location: spec line 23 (E3: "Orca workers invoked `/sc:adversarial`, and that work landed as PR #329", citing the P3 return contract); line 43 (1.4 gap 1: PR #329 "proves the nested route, not the direct route"); `orca-capabilities.md:156` (the PR #329 README instructs an Agent-tool spawn); `commands-a.md:13` (P3 contract records `skill-direct`).
- Issue: E3 uses the P3 run as support for direct-route workers and calls it the PR #329 work. Section 1.4 says PR #329 used the nested route. The two statements do not fit together unless the P3 run and the PR #329 run are different runs, which the spec does not say.
- Recommendation: separate the two runs in E3, and say which one supports the direct route. P0 (AC-0.4) remains the only proof of the direct route.
- Expert: Wiegers (evidence traceability).

### F-06 (MINOR, MEDIUM): E2 claims a worker has the same tools as a person's command, which is not in the evidence

- Location: spec line 22 (E2: "so a command run by a worker has the same tools as a command a person runs"); cited `CAPS:161` (a `--agent claude` launch) and line 44 (1.4 gap 1, direct route not observed).
- Issue: `CAPS:161` shows the launch command and the top-level session, not tool parity. Tool parity is not observed (line 43, UNVERIFIED #1).
- Recommendation: restate E2 as "a worker is a top-level session (CAPS:161); tool parity is UNVERIFIED until AC-0.4 runs".
- Expert: Fowler.

### F-07 (MINOR, MEDIUM): WC-4 states as fact a point the spec itself lists as UNVERIFIED

- Location: spec line 62 ("Orca does not check the file, so the coordinator opens it"); line 274 (UNVERIFIED #3: "the spec assumes it does not"); `orca-capabilities.md:79`.
- Issue: the requirement is written as a fact. Its own UNVERIFIED list says it is an assumption.
- Recommendation: write "the spec assumes Orca does not check the file (UNVERIFIED, line 274); the coordinator checks it either way".
- Expert: Wiegers.

### F-11 (MINOR, MEDIUM): AC-C5 checks command files only, so SA-4 is not enforced for the skill edits the phases make

- Location: line 176 (AC-C5: `git diff ... -- src/superclaude/commands/<name>.md`); line 149 (SA-4: "Command-file edits in Phases 1-3 are additive"); lines 159-161 (P1-P3 change skills: adversarial, workflow, roadmap, validate-roadmap, validate-tests, tasklist, reflect, cli-eval skill files).
- Issue: the skill files that carry most of the phase changes are not checked for additive edits.
- Recommendation: extend AC-C5 to `src/superclaude/skills/<name>/SKILL.md` and `refs/*.md`, or state that skill edits are exempt and why.
- Expert: Fowler, Newman (service boundary: skill and command must change together).

### F-13 (MINOR, MEDIUM): AC-C1 covers `src/superclaude/core`, so the Phase 0 Orca section in HOW-WE-WORK conflicts with it

- Location: line 158 (P0 adds an Orca section to `HOW-WE-WORK.md` and its mirrors); line 150 (SA-5: the routing guide gains an Orca section); line 172 (AC-C1 includes `src/superclaude/core`); line 147 (SA-2: the only allowed Orca mention is inside the contract file); `orca-capabilities.md:25` (only `ccsession-tag` mentions Orca today).
- Issue: SA-2 allows an Orca mention only in the contract file, while P0 adds one to HOW-WE-WORK. AC-C1 would fail on an Orca subcommand line there, and the spec does not say which text is allowed.
- Recommendation: state that the routing-guide Orca section names no `orca` subcommand, or add the guide and the contract file to an explicit AC-C1 exclusion.
- Expert: Fowler.

### F-19 (MINOR, MEDIUM): the plugin mirror of the commands is not covered by any phase check

- Location: spec line 279 (UNVERIFIED #8: how `plugins/superclaude/commands/` is kept in step); line 168 (P0 and AC-0.2 cover only HOW-WE-WORK mirrors); line 173 (AC-C2 covers only `.claude/` sync).
- Issue: each phase edits `src/superclaude/commands/`, and the plugin copies may drift. No AC checks them, and UNVERIFIED #8 says each phase's plan must resolve it first.
- Recommendation: make resolving UNVERIFIED #8 an explicit P0 deliverable, with an AC.
- Expert: Newman (copies that must stay in step).

### F-20 (LOW, MINOR): D3's recommended option removes pr-submit from the worker count, but the counts still include it

- Location: line 240 (D3 recommended (a): coordinator or person only, "no pr-submit changes in Phase 4"); line 114 (3.2 pr-submit row, needs-change, P4); line 128 and 139 (section 4 coordinator-only list and note); line 75 (10 / 27 / 6).
- Issue: if D3 (a) is taken, the counts become 10 / 26 / 7.
- Recommendation: state the count under each D3 outcome.
- Expert: Wiegers.

=== QUALITY ASSESSMENT (standard format) ===

- clarity: 6/10 (the vocabulary is consistent and most citations resolve; the phase table has two readings, F-14)
- completeness: 6/10 (contract coverage and worker-session ownership gaps, F-03, F-10)
- testability: 5/10 (AC-C1 never matches, F-02; AC-0.4 cannot pass, F-01; several WC rules have no AC, F-12)
- consistency: 5/10 (evidence mixes runs, F-05; path rule and rows disagree, F-08; SA-2 and P0 disagree, F-13)
- overall: 5.5/10

## expert_consensus

- Wiegers, Fowler and Nygard agree the three-way gate resolution (default / flag / blocked) and the single report file are the right design. The disagreement is on coverage: which of the 37 commands the phases actually change (F-03, F-14).
- All experts agree the spec's count of verdicts (10 / 27 / 6) matches the inventories, and that the 43-command scope is consistent with both inventory scopes.
- Adzic and Whittaker agree the acceptance layer is the weakest part of the spec: a gate that never matches (F-02) and a gate that cannot pass in its own phase (F-01).

## adversarial_analysis (Whittaker)

Three attacks are listed in the required template. Each invariant below is a stated rule in the candidate.

1. **Sentinel Collision Attack (FR-2.3).** I can break this specification by **sentinel collision**. The invariant at **WC-5 (line 63)** fails when **a contract has `status: partial` and a non-empty `blocked_question`**. Concrete attack: the worker maps `partial` to `--outcome succeeded` (line 263), so the coordinator never sees the question, and the worker does not stall in an `ask`. Before: status partial, blocked_question set. After: `worker_done --outcome succeeded`, no question delivered. Severity: MAJOR, graded Medium (F-15).

2. **Sequence Attack (FR-2.4).** I can break this specification by **sequence**. The invariant at **WC-3 and WC-6 (lines 61, 64)** fails when **the coordinator answers a blocked `ask` and re-invokes the command**. Concrete attack: the re-invoked command has no resume flag, so WC-6 writes a fresh directory, and the blocked run's partial output is orphaned. Before: directory A holds the blocked run. After: directory B holds the answered run; A is not referenced. Severity: MINOR, graded Medium (F-16).

3. **Divergence Attack (FR-2.2).** I can break this specification by **divergence**. The invariant at **WC-5 (line 63)** fails when **the contract `status` says `succeeded` but the body's first sentence says the run was blocked**. Concrete attack: WC-5 uses `status` for the outcome, so the worker sends `--outcome succeeded`, while the coordinator reading the body sees a blocked run. Before: status succeeded, body "blocked". After: outcome succeeded, the coordinator must choose which signal to trust. Severity: MINOR, graded Medium (F-15).

## Guard Condition Boundary Table

Guards enumerated: WC-5 outcome mapping; WC-10 wait threshold; WC-1 readiness fallback; WC-9 outward flag; WC-6 retry; the section 3.2 task confidence gate; WC-3 ask timeout; WC-12 fence check; WC-4 / 7.2 step 4 contract presence. Input classes not listed for a guard are left out because the guard has no counter, sentinel or capacity for them (for example, WC-10 has no overflow case).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | line 63 | No report exists | no file | failed | `--outcome failed` | OK |
| WC-5 outcome | line 63 | Report status `partial` | `partial` | succeeded | line 263 | OK |
| WC-5 outcome | line 63 | Report status `blocked` | `blocked` | failed | line 63 | OK |
| WC-5 outcome | line 63 | Status outside the four values | `done` | not stated | none | GAP (F-15, Medium) |
| WC-5 outcome | line 63 | `partial` with non-empty `blocked_question` | both set | not stated | none | GAP (F-15, Medium) |
| WC-5 outcome | line 63 | Body first sentence contradicts status | mismatched | not stated | none, no AC | GAP (F-15, Medium) |
| WC-4 / 7.2 step 4 | lines 62, 183 | Contract empty or missing | size 0 | coordinator check fails | worker's own behaviour not stated | GAP (F-10, Medium) |
| WC-10 wait split | line 68 | Single call duration | 240 s | allowed | line 68 | OK |
| WC-10 wait split | line 68 | Single call duration | exactly 300 s | not stated (rule says "longer than") | none | GAP (F-17, Medium) |
| WC-1 readiness fallback | line 59 | Fallback vs 60 s limit | 30 s | passes (EVIDENCE cited) | "well inside" | GAP (F-12, Medium) |
| WC-1 readiness fallback | line 59 | Fallback vs 60 s limit | 45 s | fails (EVIDENCE cited) | not allowed | OK |
| WC-9 outward flag | line 67 | Flag absent | none | off | line 67 | OK |
| WC-9 outward flag | line 67 | Flag present, user did not authorize | flag set | command runs the action | D4 open | GAP (F-18, Medium) |
| WC-6 retry | line 64 | `--retry-of` with same output directory | same dir | must not corrupt | command-dependent, no brief rule | GAP (F-16, Medium) |
| Task confidence gate | line 121 | Confidence exactly 0.70 | 0.70 | proceeds (inferred from "below 0.70") | "below 0.70" | OK |
| WC-3 ask timeout | line 61 | Timeout with question pending | pending | resume same message ID | line 61 | OK |
| WC-12 fence | line 70 | `consumer_fenced` | - | stop, no `worker_done` | line 70 | OK |

GAP rows are graded Medium and listed under follow-up candidates. None of them is a CRITICAL or blocking finding on its own.

## Improvement roadmap (not run: critique mode, no Improve step)

- immediate: F-01, F-02, F-03, F-04 (each has a grading sentence and a recommendation above).
- short term: F-05 to F-14.
- long term: F-15 to F-20 and the UNVERIFIED items in the candidate (lines 272-285).

## Citation check (outside the workspace)

Not checked, marked UNVERIFIED: `pyproject.toml:38` (PyYAML, line 183); `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56` (cited in spec lines 44 and 59, and in `orca-capabilities.md:49-50`); `src/superclaude/...` citations in lines 52, 170, 179; `CLAUDE.md:16,50,72-83`; the Orca installed files (`/opt/Orca/...`) cited through the capabilities inventory.

## follow-up candidates (Medium and minor; not blocking)

- F-05 E3 mixes two runs (spec line 23; orca-capabilities:156; commands-a:13)
- F-06 E2 tool-parity overclaim (spec line 22)
- F-07 WC-4 states as fact an UNVERIFIED point (spec lines 62, 274)
- F-08 contract path rule vs per-command paths (spec lines 62, 83, 91, 92, 228)
- F-09 Phase 0 and 3.1 briefs omit `--unattended` (spec lines 73, 79, 81-92, 158, 194)
- F-10 worker-session rules have no stated loader (spec lines 52, 61-70, 73)
- F-11 AC-C5 checks commands only (spec lines 149, 159-161, 176)
- F-12 WC-1, WC-5 first sentence, WC-6, WC-12 without an AC; WC-1 unquantified (spec lines 59, 63, 64, 70)
- F-13 AC-C1 scope vs the Phase 0 routing-guide Orca section (spec lines 147, 150, 158, 172)
- F-14 P1 scope vs P1 commands vs AC-1.1 (spec lines 159, 195, 196)
- F-15 WC-5 undefined status combinations (spec lines 62, 63, 263)
- F-16 re-invocation after an answer vs fresh-directory default (spec lines 61, 64)
- F-17 WC-10 threshold and cadence (spec lines 68, 181)
- F-18 D4 outward authorization is not checkable (spec lines 67, 244-247)
- F-19 plugin command mirror has no check (spec lines 168, 173, 279)
- F-20 D3 counts (spec lines 114, 128, 139, 240)

## Reviser brief

Revise only the blocking finding ids listed here: **F-01, F-02, F-03, F-04**. Restating the review-loop rule for the reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited under it.

verdict: FAIL

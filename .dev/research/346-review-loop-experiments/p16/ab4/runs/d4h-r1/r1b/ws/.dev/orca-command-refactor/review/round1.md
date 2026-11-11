review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Procedure: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, plus the acceptance-criteria and live-check pass requested in the brief.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none (first review, `baseline: missing` not applicable). Prior report: none.
- Lint: `.dev/orca-command-refactor/review/lint-1.md` (sha256 of the candidate it was run on: `d3cdbe57...425200d`, matches the candidate above). It reports `Checks: REF. Findings: 0.` and `No findings.` There are no lint ids to confirm or dismiss.
- Reviewer model: claude-haiku-5-5 (single reviewer, fresh context for this run).
- Date: 2026-11-10.

## Process notes

1. The FIRST-REVIEW prompt asks for two independent first reviews and a coordinator MERGE. This report is one reviewer's output. The coordinator must run a second independent first review and apply the MERGE rule before any revision. Nothing here was merged.
2. The VERIFY prompt has not been run. Every blocking finding below is open and unverified until a fresh-context verifier confirms it against the candidate. No revision should start before that.
3. Citation scope. The workspace contains only `.dev/orca-command-refactor/` (README, specs, inventory, review). Every citation to `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...` or `CLAUDE.md` is UNVERIFIED in this sandbox. Those are marked where used. The inventories and the README were read in full and checked against the cited spec claims.

Short forms used below:
- `SPEC:n` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line n.
- `README:n` = `.dev/orca-command-refactor/README.md` line n.
- `INV-A:n` / `INV-B:n` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md` line n.
- `CAPS:n` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` line n.
- `LINT:n` = `.dev/orca-command-refactor/review/lint-1.md` line n.

## Coverage

Read in full: the candidate (SPEC:1-285), both inventories, the capabilities inventory, the README, the lint file, the command definition, and the review-loop prompts file. Checked: all 15 acceptance-criteria IDs (AC-C1 to C5, AC-0.1 to 0.4, AC-1.1 to 1.4, AC-2.1 to 2.5, AC-3.1 to 3.4, AC-4.1 to 4.3) and all 7 live-check steps (SPEC:180-186), each against the commands and phases it covers. Spot-checked about 40 cross-citations from the spec into INV-A, INV-B and CAPS; all of those that could be checked matched their quoted text (for example CAPS:52, 80, 129, 130, 148-151, 155-161, 186-188; INV-A:14, 60, 76-83, 95, 97; INV-B:31, 40, 52, 65, 272, 322). The 10 / 27 / 6 split (SPEC:75) matches the inventory verdicts (INV-A summary 5 / 13 / 3, INV-B summary 5 / 14 / 3, 43 commands in total).

## Acceptance criteria and live checks, one by one

Column "Passes as written" answers whether the criterion can pass as written for every command and phase it covers. Findings referenced here are defined below.

| ID | SPEC line | Covers | Passes as written | Why |
|---|---|---|---|---|
| AC-C1 | 172 | all phases | Yes, but weak | Vacuous risk and scope problem, see M9. |
| AC-C2 | 173 | all phases | Yes | Does not cover the `plugins/superclaude/commands/` mirror, see M11. |
| AC-C3 | 174 | all phases | Yes | Baseline run is well defined. |
| AC-C4 | 175 | all phases | Yes | Checks only staged paths. |
| AC-C5 | 176 | all phases | Passes vacuously | Diffs `master...HEAD` (commits only), see M10. |
| AC-0.1 | 191 | P0 | Yes | Import and membership check. |
| AC-0.2 | 192 | P0 | Yes | `cmp` plus existing level-table test. "Its two mirrored copies" (SPEC:158) is only partly checked, minor note N2. |
| AC-0.3 | 193 | P0 | Passes vacuously | Same `master...HEAD` issue as AC-C5, see M10. |
| AC-0.4 | 194 | P0 | No | Step 4 cannot read existing reports (B1), step 6 cannot pass with uncommitted phase edits (B2), no check for "no Agent-tool wrapper" (B3). |
| AC-1.1 | 195 | P1 (all of 3.1 and 3.2) | No | Requires a contract name in `load`, whose row says it writes no report (B6). Also requires a pr-submit section in P1 that D3 does not settle (M18). |
| AC-1.2 | 196 | P1 | No | Step 6 (B2) and `load` in the P1 set (B6). |
| AC-1.3 | 197 | P1 | Yes | Plain-session run plus `git status`. |
| AC-1.4 | 198 | P1 | Yes as text | The grep can pass, but the workflow contract path it checks is itself contradictory (B7). |
| AC-2.1 | 199 | P2 | Yes | Text assertions per gate. |
| AC-2.2 | 200 | P2 | No | Requires `status: blocked` for every P2 command; six P2 commands have no blocked path (B4). WC-3 `ask` path can also make it fail (M2). |
| AC-2.3 | 201 | P2 | No | Same step 6 defect as AC-1.2 (B2). |
| AC-2.4 | 202 | P2 (auggie-review) | Yes | Reads PR counts before and after, needs a fork PR and the `auggie` CLI (UNVERIFIED in this sandbox). |
| AC-2.5 | 203 | P2 | Yes | Manual check. |
| AC-3.1 | 204 | P3 | Yes | Text assertions on two files. |
| AC-3.2 | 205 | P3 (roadmap) | Conditional | Uses `--output` on roadmap, which row SPEC:118 does not give it (M19). |
| AC-3.3 | 206 | P3 (validate-tests) | Yes | Depends on the chosen default path. |
| AC-3.4 | 207 | P3 (save) | Yes | Hash comparison. |
| AC-4.1 | 208 | P4 (implement) | Yes | Ledger and contract check. |
| AC-4.2 | 209 | P4 (post-release) | Yes | Git log and PR list check. |
| AC-4.3 | 210 | P4 (pr-submit, only if D3(b)) | Yes if D3(b) | Not applicable under D3(a). |
| Step 1 | 180 | every live run | Yes | `worker-start` exit 0 and `state: ready` (CAPS:46). |
| Step 2 | 181 | every live run | Conditional | Cadence conflicts with step 3's 900 s wait (M1); `ask` may show `agentWait` (M2). |
| Step 3 | 182 | every live run | Yes | `question` is listed but no response is defined (note N3). |
| Step 4 | 183 | P0 existing reports | No | Reads YAML keys from Markdown reports (B1). Passes for P1+ contracts if they carry `status` and `command`. |
| Step 5 | 184 | every live run | Partly | Greps for `AskUserQuestion`, which the command's own text may contain (N6); does not test for an Agent-tool wrapper (B3). |
| Step 6 | 185 | every live run | No | Uncommitted phase edits always appear (B2). |
| Step 7 | 186 | every live run | Yes | Release and reclaimable-list check. |

## Guard Condition Boundary Table

Triggered: SPEC contains conditional logic and threshold checks (outcome mapping, the 5-minute rule, the gate rule, the output-directory rule). Enumerated guards follow. Input classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | SPEC:63 | Zero/Empty: no report exists | no contract | failed | failed | OK |
| WC-5 outcome mapping | SPEC:63 | One/Minimal: status `partial` | `partial` | succeeded | succeeded (SPEC:263) | OK |
| WC-5 outcome mapping | SPEC:63 | Typical: status `succeeded` | `succeeded` | succeeded | succeeded | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel/Legitimate edge: status outside the four values, or missing (`Blocked`, `done`, no key) | unlisted | undefined | not stated; an implementer may map it to succeeded | GAP (Medium, M21) |
| WC-5 with WC-4 | SPEC:62, 63 | Edge: `partial` with a non-empty `blocked_question` | `partial` + question | succeeded | question is never answered (M20) | GAP (Medium) |
| WC-10 wait split | SPEC:68 | Threshold: single call of 4 to 5 min | 270 s | not split | not split, but heartbeats are due every 5 min | GAP (Medium, M22) |
| WC-10 wait split | SPEC:68 | Maximum: 3600 s eval | 3600 s | split | split into 4-min waits | OK |
| WC-2 gate rule | SPEC:60 | Zero: gate has a documented default and no flag | no flag | (a) | default applied | OK |
| WC-2 gate rule | SPEC:60 | Typical: gate has no default and no flag | no flag | (c) | blocked | OK |
| WC-2 gate rule | SPEC:60 | Legitimate edge: `--unattended` unknown to an older install | flag ignored | undefined | gates run interactively and the worker stalls (M7) | GAP (Medium) |
| WC-3 vs WC-2 | SPEC:60, 61 | Typical: gate that would resolve as blocked | ask available | blocked or ask | "three ways" versus "may instead ask" | GAP (Medium, M2) |
| WC-4 output dir | SPEC:62 | Zero/Empty: unattended run without `--output` | no dir | undefined | the command's default dir is not stated | GAP (Medium, M23) |
| WC-6 retry | SPEC:64 | Typical: retry with the same `--output` | same dir | undefined | "fresh dir" versus "dir the coordinator passed" (M4) | GAP (Medium) |
| WC-9 outward flag | SPEC:67 | Zero: outward flag absent | no flag | off | off | OK |
| WC-9 outward flag | SPEC:67 | Typical: flag present in brief | `--post-pr` | on | on | OK |
| WC-12 fence | SPEC:70 | Typical: `check` returns `consumer_fenced` | fenced | stop | no `worker_done` | OK |
| SA-1 standalone | SPEC:146 | Zero: no `--unattended` | absent | unchanged | unchanged except roadmap row (B5) | GAP (Blocking B5) |

Rows left out, with reasons: the maximum-capacity class for WC-5 (no numeric bound exists), and the overflow class for WC-10 (no counter is involved).

## Pipeline Dimensional Analysis

Not triggered. The spec describes control flow (coordinator to Tasks to workers to reports), not a data pipeline whose record counts change between stages. The one fan-out (SPEC:39, splitting work into Tasks) multiplies Tasks, not records.

## Blocking findings

Each blocking finding carries the grading sentence required by the FIRST-REVIEW prompt.

### B1. AC-0.4 step 4 reads YAML keys from a Markdown report
- Expert: Adzic (testable examples).
- Location: SPEC:183 (step 4 asserts `d['status']` and `d['command']` from a YAML load), SPEC:194 (AC-0.4 says step 4 "uses the command's existing report file"). INV-B:49 (`/sc:troubleshoot` writes `REPORT.md`, `report_path`).
- Grading sentence: An implementer who follows AC-0.4 runs step 4 on the troubleshoot `REPORT.md`, which is Markdown, so `yaml.safe_load` returns text or a dict without `status` and `command`, and the step fails on a correct run.
- Priority: High. Quality impact: AC-0.4 cannot close Phase 0 as written.
- Recommendation: in P0, split step 4 into "file exists and non-empty" for report files and the YAML field check only for files that are YAML contracts. Confirm whether the workflow contract carries a `command` key (INV-B:272 lists `status`, `plan_path`, `reflect_report_path` only; UNVERIFIED).

### B2. Step 6 fails whenever the phase's own edits are uncommitted
- Expert: Adzic.
- Location: SPEC:185 (pass: "only files under the brief's output directory ... appear"), SPEC:158-162 (each phase edits tracked files), SPEC:194, 196, 201 (AC-0.4, AC-1.2, AC-2.3 all depend on step 6). No step in SPEC:180-186 commits or snapshots the tree.
- Grading sentence: An implementer who writes the P0 files (WORKER-CONTRACT.md, the HOW-WE-WORK section, the test file) in the worktree and then runs step 6 as written sees those modified or untracked paths in `git status --short`, which the pass condition does not allow, and the spec gives no step that commits or snapshots first.
- Priority: High. Quality impact: every live check after P0 fails for reasons unrelated to the worker.
- Recommendation: make step 6 compare `git status --short` taken before dispatch with the one taken after, and pass only if the new entries are under the output directory or are documented artifacts.

### B3. AC-0.4 requires "no Agent-tool wrapper, verified in the step-5 transcript", and step 5 does not test it
- Expert: Wiegers (criteria must match their verification).
- Location: SPEC:194 (AC-0.4 "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"), SPEC:184 (step 5 pass: "no AskUserQuestion call").
- Grading sentence: An implementer who runs step 5 as written searches only for `AskUserQuestion`, so no evidence about an Agent-tool wrapper is produced, and AC-0.4 cannot pass as written.
- Priority: High. Quality impact: WC-7 (SPEC:65) is untested.
- Recommendation: add to step 5 a pass condition that the transcript has no Agent or Task tool use whose prompt is the `/sc:` command, and say which transcript field to check.

### B4. AC-2.2 requires `status: blocked` for every P2 command, but six P2 commands have no blocked path
- Expert: Adzic and Crispin (examples and boundary cases).
- Location: SPEC:200 (AC-2.2: "contract `status: blocked` with a non-empty `blocked_question`"), SPEC:160 (P2 set), and the rows that resolve without a blocked outcome: SPEC:100 (auggie-review: defaults `--no-post-pr --no-remediation-offer`), SPEC:103 (cleanup: lists unapplied items, does not block), SPEC:110 (improve: same), SPEC:116 (research: pins `--strategy planning`), SPEC:88 (reflect: headless auto-accept, no gate without `--remediate`), SPEC:122 (tasklist: passes `--unattended` down, no gate).
- Grading sentence: An implementer who follows the cleanup row builds a run that applies auto-fix items and lists the rest in the report, so no gate resolves as blocked and AC-2.2 fails because it expects `status: blocked`.
- Priority: High. Quality impact: AC-2.2 cannot be satisfied for six of 15 P2 commands, so the phase cannot pass its own check.
- Recommendation: state AC-2.2 as "blocked where the row names a blocked path, otherwise the default is recorded in the contract", and give one trigger input for each command that has a blocked path. Only two of the 15 have inputs now (SPEC:200).

### B5. SA-1 forbids prompt changes without `--unattended`; the roadmap row removes the Y/n prompt unconditionally
- Expert: Wiegers (requirement conflict).
- Location: SPEC:146 (SA-1: "every prompt ... stays as it is today" without `--unattended`), SPEC:149 (SA-4 allows fixes that "keep the standalone behaviour or correct a documented defect"), SPEC:118 (roadmap row: "the 'Resume? [Y/n]' prompt is replaced by the explicit resume flag (resume only when passed)", with no `--unattended` qualifier). Source of the prompt: INV-B:40 (`sk/sc-roadmap-protocol/SKILL.md:433-438`, UNVERIFIED in this sandbox).
- Grading sentence: An implementer who follows the roadmap row removes the Y/n prompt for a plain session with no flags, which SA-1 (SPEC:146) forbids, and SA-4 (SPEC:149) permits only as a defect fix, so the two texts contradict each other.
- Priority: High. Quality impact: standalone users lose a prompt they rely on; the SA-1 check (AC-2.5, SPEC:203) would catch it only manually.
- Recommendation: scope the roadmap change to `--unattended`, or name a standalone exception in SA-1 and list each one. The same question applies to the adversarial contract-filename fix (row SPEC:83, a standalone output path under SA-1).

### B6. `load` must write a contract (WC-4, AC-1.1, AC-1.2) but its row and decision say it writes no file
- Expert: Wiegers (traceability) and Fowler (interface).
- Location: SPEC:62 (WC-4: contract "written on every outcome" in unattended mode), SPEC:112 (load row: report "none (see note)"), SPEC:159 (P1 includes load), SPEC:195 (AC-1.1 requires `return-contract.yaml` in every section 3.1 and 3.2 command), SPEC:196 (AC-1.2 runs on each P1 command), SPEC:265 (decision: "a report file would be an unrequested addition"). INV-B:65 (load "only loads context into the current session").
- Grading sentence: An implementer who follows the load row writes no contract, and AC-1.1 and AC-1.2 fail for `load`; an implementer who follows WC-4 writes one, which the decision at SPEC:265 forbids, so the two texts contradict each other.
- Priority: High. Quality impact: P1 cannot pass for `load`.
- Recommendation: exempt `load` from WC-4 by name in WC-4 and in AC-1.1 and AC-1.2, or give it a one-line contract. Either way update SPEC:265.

### B7. The workflow contract path conflicts with WC-4 and does not exist for a pre-creation STOP
- Expert: Fowler and Hohpe (interfaces and report channels).
- Location: SPEC:62 (WC-4: `<output-dir>/return-contract.yaml`, "including stops before any other output exists", and the path is known before dispatch), SPEC:92 (workflow row: `.dev/tasks/to-do/<id>/return-contract.yaml`; "Write the contract for pre-creation STOPs too"), SPEC:198 (AC-1.4). INV-B:272 (`.dev/tasks/to-do/<id>/`; not written for pre-creation STOPs). SPEC:73 (the coordinator must know the path before dispatch).
- Grading sentence: An implementer who follows WC-4 writes a pre-creation STOP contract to `<output-dir>`, but workflow has no output flag in row SPEC:92, and the row's `<id>` directory does not exist before package creation, so the path the coordinator must know before dispatch (SPEC:73) is undefined for that case.
- Priority: High. Quality impact: a blocked or failed workflow run leaves the coordinator no report to read.
- Recommendation: give workflow a `--output` (or a fixed STOP-contract path) and state which location wins for each outcome.

## Medium findings (follow-up candidates, not blocking)

These need a guess, a missing restriction or an unstated state. Under the grading check they are Medium and go under follow-up candidates.

- M1. Step 2 cadence versus step 3 wait. Expert: Nygard. Step 3 blocks for up to 900000 ms in one `check --wait` (SPEC:182), but step 2 requires a `worker-show` at least every 5 min (SPEC:181). A reader who follows step 3 literally cannot satisfy step 2. An implementer would have to shorten the waits, which the spec does not say.
- M2. WC-3 `ask` path versus WC-2 and AC-2.2. Expert: Nygard and Wiegers. WC-2 says each gate resolves one of three ways (SPEC:60). WC-3 lets a gate-trigger worker call `ask` instead (SPEC:61). CAPS:52 and CAPS:129 say a worker parked on an `ask` shows as waiting, so step 2 can fail on a compliant worker (SPEC:181). The implementer must pick the `ask` option, which is the worse reading for AC-2.2.
- M3. No coordinator loop for `blocked`. Expert: Cockburn and Nygard. SPEC:63 maps blocked to failed. Section 2.3 (SPEC:73) says the coordinator opens the report and releases the worker, but says nothing about who reads `blocked_question`, who answers it, or how a re-dispatch is capped. The Orca circuit breaker does not count a worker's own failed report (CAPS:80, cited at SPEC:263), so a blocked worker can be re-dispatched without limit.
- M4. Retry directory. Expert: Fowler. WC-6 says a command writes each run into a fresh output directory (SPEC:64). WC-4 says the directory is the one the coordinator passed and is known before dispatch (SPEC:62). SPEC:73 gives no rule for the directory of a retry.
- M5. Fixed-path commands versus WC-11. Expert: Newman and Hohpe. WC-11 requires timestamp or slug paths and forbids two workers writing one file (SPEC:69). Ready rows still have fixed paths: index-repo `PROJECT_INDEX.md` (SPEC:86, brief passes no flag), cleanup-audit `.claude-audit/` (SPEC:85), init-lite default `.dev/superclaude/context-audit.md` (SPEC:87). The control "one audit per worktree at a time" (SPEC:85) is not in section 2.3, so nothing enforces it.
- M6. WC-1 and WC-12 have no owner check or phase. Expert: Crispin. WC-1 is owned by "Launch setup, not commands" (SPEC:59), and WC-12 says "Commands need no change" (SPEC:70). Neither appears in any phase (SPEC:158-162) or AC (SPEC:191-210).
- M7. Version skew. Expert: Newman and Nygard. The contract is installed to `~/.claude/` (SPEC:52). An older install has commands without the `## Unattended mode` section, so `--unattended` is ignored and the gates run interactively, which stalls the worker unseen (SPEC:60, CAPS:52). Nothing requires a version check. UNVERIFIED: how installed versions are tracked.
- M8. Where unattended overrides go. Expert: Fowler. The section is appended to a command (SPEC:52, SPEC:149). Many gates live in skills, not in commands (SPEC:90 tdd `sk/tdd/SKILL.md:52-61`; SPEC:117 review-translation; SPEC:121 task). SA-4 (SPEC:149) and AC-C5 (SPEC:176) only constrain command files, so skill edits are unconstrained. The spec does not say whether an appended `## Unattended mode` overrides earlier body text, which a model reads in order. The override question is decisive for every P2 gate.
- M9. AC-C1 coverage and scope. Expert: Adzic. The pattern (SPEC:172) matches only `orchestration|worktree|terminal|agent`, so a command that runs `orca status --json` passes, although SA-2 (SPEC:147) forbids any `orca` command. It scans `src/superclaude/core` (SPEC:172), where SA-2 allows an Orca mention in the contract (SPEC:147) and SA-5 adds an Orca section to the routing guide (SPEC:150). The check can therefore fail on allowed text. The raw `\|` escapes in the table cell (SPEC:172) break the alternation if copied as written.
- M10. Vacuous diffs. Expert: Adzic. AC-C5 (SPEC:176) and AC-0.3 (SPEC:193) diff `master...HEAD`, which shows commits only. Uncommitted edits, which the phases create, are invisible, so both pass until a commit exists.
- M11. Plugin mirror not checked. Expert: Fowler and Newman. AC-C2 (SPEC:173) runs `make verify-sync` only. UNVERIFIED item 8 (SPEC:279) says each phase must resolve how `plugins/superclaude/commands/` is kept in step, but no phase or check does.
- M12. Tasklist nesting. Expert: Fowler. Row SPEC:122 says the reflect fan-out is "inside Claude Code's nesting limit" and cites INV-A:14. INV-B:46 and INV-B:210 mark it unverified, and INV-B:322 (UNVERIFIED 8) says so too. SPEC:45 says no nesting limit is proven. The chain (tasklist subagent, then reflect, then reviewers, then adversarial) is not counted in the spec.
- M13. Reflect default folder move. Expert: Nygard and Wiegers. INV-B:114 says reflect's default UC-2 Wave 7 moves the validated work-unit folder. Row SPEC:88 keeps reflect ready. WC-9 (SPEC:67) covers pushes, PRs, posts, installs and paid runs, not local state changes, so an unattended run moves folders without an explicit flag.
- M14. Standalone changes in the workflow and adversarial rows. Expert: Wiegers. Row SPEC:92 makes workflow write a contract on pre-creation STOPs without saying it is limited to unattended runs, which SA-3 (SPEC:148) forbids for standalone runs. Row SPEC:83 changes the adversarial contract filename, which is a standalone output path under SA-1 (SPEC:146). Both need an explicit unattended qualifier or a named exception.
- M15. Hardcoded source path left in an installed command. Expert: Fowler. Row SPEC:105 keeps the cli-portify template path `src/superclaude/examples/...` (UNVERIFIED in this sandbox), which CLAUDE.md forbids in installed primitives. No phase fixes it or excludes it, and the spec only restricts where it can be dispatched.
- M16. Overstated evidence. Expert: Wiegers. SPEC:22 says a worker "has the same tools as a command a person runs" and cites EVIDENCE.md:45 (quoted at CAPS:49). The quoted evidence shows readiness (`state: ready, stage: input_accepted`), not tool parity. The decision in section 1 needs tool parity to be true (or at least stated as unverified).
- M17. Trigger inputs. Expert: Crispin. AC-2.2 names inputs for two of the 15 P2 commands (SPEC:200). The rest say "input that hits the gate" with no example, and some rows have no gate that can be triggered (see B4).
- M18. pr-submit in P1. Expert: Adzic. AC-1.1 requires pr-submit's `## Unattended mode` section in P1 (SPEC:195, via SPEC:159), while row SPEC:114 puts its changes in P4 and D3(a) (SPEC:240) recommends no pr-submit change. The spec does not say which applies in P1.
- M19. Roadmap output flag. Expert: Wiegers. AC-3.2 runs `/sc:roadmap ... --output <dir>` (SPEC:205). Row SPEC:118 names no output flag, while WC-4 requires one for every unattended command (SPEC:62). P1 scope (SPEC:159) would cover it only if roadmap counts as "a command that lacks one". UNVERIFIED whether roadmap already has `--output`.
- M20. Partial with a question. Expert: Whittaker (attack). Invariant at SPEC:63 and SPEC:62: a contract with status `partial` maps to succeeded (SPEC:263), but `blocked_question` is defined only "when blocked" (SPEC:62). Trace: a worker writes `partial` with a `blocked_question` that needs an answer; the outcome is succeeded; the coordinator never answers; the run is reported as done.
- M21. Unlisted status values. Expert: Adzic. SPEC:63 maps only four status values and says nothing about a missing or misspelled one (for example `Blocked`). An implementer may map it to succeeded, which hides a blocked run. Guard table row, graded Medium.
- M22. Calls of 4 to 5 minutes. Expert: Nygard. SPEC:68 splits only calls longer than 5 minutes into waits of at most 4. A 270-second call is neither split nor covered by a heartbeat rule, so two such calls in a row can exceed the 5-minute heartbeat cadence (SPEC:68, CAPS:130). Guard table row, graded Medium.
- M23. Missing output directory. Expert: Fowler. SPEC:62 defines the contract location as the directory the coordinator passed, but gives no default for an unattended run started without `--output`. Guard table row, graded Medium.

### Whittaker attacks (panel attack methodology, always active)

- FR-2.4 Sequence attack on WC-3 (SPEC:61). I can break this specification by a sequence attack. The invariant at SPEC:61 (ask once, wait, resume by message ID) fails when the coordinator never replies. Concrete attack: `ask` is pending; the timeout (default UNVERIFIED, SPEC:281) fires; the worker resumes the same message ID; no `worker_done` arrives; the spec sets no cap on this loop. Severity MAJOR, graded Medium under M2/M3.
- FR-2.2 Divergence attack on WC-5 (SPEC:63). I can break this specification by a divergence attack. The invariant at SPEC:63 fails when a contract has status `partial` and a non-empty `blocked_question`. Concrete attack: the outcome is succeeded and the question is lost (M20).
- FR-2.1 Zero attack on WC-4 (SPEC:62). I can break this specification by a zero attack. The invariant at SPEC:62 fails when an unattended run has no `--output`. Concrete attack: the contract goes to an undefined default and the coordinator opens the wrong path. Graded Medium (guard table).

## Minor notes (no grade, no revision)

- N1. CAPS:155 cites `nested-worker-depth.js:7-11, 18-19`; SPEC:24 cites 7-11, 18-22. Line 22 is cited separately in CAPS:155, so the claim holds.
- N2. SPEC:158 says "its two mirrored copies" for HOW-WE-WORK; AC-0.2 (SPEC:192) checks one `cmp`. Name the two copies.
- N3. Step 3 (SPEC:182) lists `question` but gives no response, so a live run can stall in the coordinator's own loop.
- N4. The quoted line for E2's "and answered" (SPEC:22) is not in CAPS:49 (UNVERIFIED in this sandbox).
- N5. The Decisions row for the wait size (SPEC:266) and WC-10 (SPEC:68) agree on 4 min.
- N6. Step 5 (SPEC:184) greps the transcript for `AskUserQuestion`. The unattended section the command adds (SPEC:52) names that tool, and a worker that reads the command file may put that text in its transcript, so a grep can flag compliant runs. Replace the grep with a check on tool-call names.

## Follow-up candidates

The session that ran this review asks the user once per loop whether to open issues for these. None is created without the user's answer. Listed: M1 to M23 and N1 to N6.

## Reviser brief

Blocking finding ids: B1, B2, B3, B4, B5, B6, B7.

Restated rule (FIRST-REVIEW and Review Loop bullet 6): revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revision targets. Clauses overridden by this brief: none.

verdict: FAIL

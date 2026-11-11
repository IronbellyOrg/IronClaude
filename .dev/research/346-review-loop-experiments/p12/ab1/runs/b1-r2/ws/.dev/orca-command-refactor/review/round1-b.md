review: 1 of 3

# /sc:spec-panel critique, round 1

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (taken with `sha256sum`).
- Baseline: none given. Prior findings file: none given. `baseline: missing` is noted only because this is a first review; no re-review was requested.
- Reviewer model used: claude-sonnet-5-5.
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). That prompt calls for three first reviews in fresh contexts followed by a coordinator MERGE. I cannot start fresh contexts in this sandbox, so this file is ONE of the three reports, written by a single reviewer. The coordinator must run the merge and the VERIFY prompt. This report does not claim to be the merged report.
- Panel (focus requirements = Wiegers lead, Adzic, Cockburn; architecture = Fowler lead, Newman, Hohpe, Nygard; Whittaker active in every panel; review order per the command).

## What was covered

- Read in full: the command, the review-loop prompts, `README.md` (binding context), the spec (`specs/orca-worker-contract-spec.md`, 287 lines).
- Checked against the three inventories (the only checkable evidence): all `CAPS:` lines the spec leans on for the contract (44-52, 58-80, 86-116, 129-130, 145-161, 178-188), the `INV-A` / `INV-B` lines cited for counts and cross-cutting findings (`INV-A:3,14,35,60-66,90-98,105-120`, `INV-B:36,52,65,105-115,207-215,267-311,320-323`), and the 10 / 27 / 6 split (INV-A:73 gives 5/13/3, INV-B:278 gives 5/14/3; the sum matches the spec).
- Counted the spec's own tables: section 3.1 has 10 rows, 3.2 has 27, section 4 has 6; the phase `Commands` column (spec:159-162) names 35 of the 37 non-coordinator-only commands (see M3).
- NOT checkable here, so every such citation is UNVERIFIED: `CLAUDE.md:*`, `src/superclaude/**` (`cmd/`, `sk/`, `install_core.py`, `core/*`), `.dev/evals/.../EVIDENCE.md:*`, `.dev/codegraph-migration/**`, `Makefile`, `pyproject.toml`, `plugins/**`, and the Orca guide lines `[G]`, `[H:*]` (these are only visible through the quotes in the capabilities inventory). Where the inventory quotes the line, I treated the quote as the evidence.
- Not covered: whether any command file matches the spec's per-command claims (those files are outside the sandbox); the 340-citation re-check claimed at spec:286 (not independently repeatable here).

## Guard Condition Boundary Table (mandatory artifact; triggered by thresholds in WC-5, WC-10, section 3.2 `task`, the readiness limit and the depth limit)

One row per guard and input class that can occur. Classes left out are given with one-line reasons below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 report-path guard (contract at `<output-dir>/return-contract.yaml`) | spec:62 | Typical | `--output <dir>` | contract at `<dir>/return-contract.yaml` | stated | OK |
| G1 | spec:62, 83, 92 | Legitimate edge case | adversarial (contract under `<output>/adversarial/`), workflow (`.dev/tasks/to-do/<id>/`, no output flag) | path differs from the rule | rule and rows disagree | GAP (see B1) |
| G1 | spec:62, 90, 120 | Legitimate edge case | file-valued `--output <file>` (tdd, spec-panel, init-lite) | `<output-dir>` undefined | not specified | GAP (see M1) |
| G1 | spec:62 | Zero/Empty | no output flag passed (index-repo, load, workflow) | no directory exists | index-repo: "state the output location"; load: none; workflow: not specified | GAP (see B1, B2) |
| G2 WC-5 outcome guard | spec:63 | Zero/Empty | no report exists | `--outcome failed` | stated | OK |
| G2 | spec:63 | Legitimate edge case | `status: partial` | `succeeded`, first sentence names `partial` | stated | OK |
| G2 | spec:63, 60, 120 | Legitimate edge case | command "refused" under `--unattended` (business-panel socratic, cleanup `--interactive`, test `--watch`, pr-submit `--monitor 1`) | refusal is not one of the three gate outcomes in WC-2 | whether a contract is written is not stated | GAP (Medium, see M9) |
| G3 WC-10 wait guard (split waits to at most 4 min when a call would exceed 5 min) | spec:68 | Typical | single tool call 3 min | no split needed | stated | OK |
| G3 | spec:68 | Sentinel value match | call of exactly 5 min, or 4 min plus a 1-minute sleep | "longer than 5 minutes" / "at most 4 minutes" | boundary 4 to 5 min not stated | OK (4 min leaves margin, spec:266) |
| G3 | spec:68, 55-56 | Maximum/Overflow | Agent-tool fan-out (subagents) in the foreground for more than 5 min | rule covers only "a single tool call"; a Task call is one | not stated | GAP (see M5) |
| G4 `task` confidence guard | spec:121 | Sentinel value match | confidence exactly 0.70 | "below 0.70 resolves as blocked" so 0.70 proceeds | consistent with the inventory phrase | OK |
| G5 depth guard (Orca nesting depth 1) | spec:34 (R1), 66 (WC-8) | Maximum/Overflow | a command that calls `worker-start` | refused with `nested_worker_depth_exceeded` | stated; whether `task-create` is refused is UNVERIFIED (spec:276) | OK, as flagged |
| G5 | spec:55-56 | Legitimate edge case | tasklist Stage 10.5 reflect fan-out below the worker (reflect then spawns its own agents and a remediation hand-off) | "inside Claude Code's nesting limit" | asserted for one layer only | GAP (see M2) |
| G6 `--unattended` switch guard | spec:52 | Zero/Empty | flag absent | today's behavior (SA-1) | stated | OK |
| G6 | spec:159 | Typical | flag passed to a command whose gate conversion lands in P2-P4 | "accepted"; gate still prompts until its phase | not stated | GAP (see M3) |
| G7 readiness guard (60 s) | spec:60 (WC-1) | Maximum/Overflow | wrapper prompt longer than 45 s | worker-start fails | owner "Launch setup", no phase or check closes it | GAP (see M10) |

Classes left out: G2 "One/Minimal" (a single outcome has no extra case); G3 "Zero/Empty" (a zero-length wait needs no split); G4 "Zero/Empty" (confidence 0 is below 0.70 and resolves as blocked by the same rule); G5 "Zero/Empty" (depth 0 is the coordinator, which is not a worker); G6 "Maximum" (a flag has no capacity).

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1 (MAJOR, blocking). WC-4 fixes the report path as `<output-dir>/return-contract.yaml`, "known before dispatch", but two section 3.1 rows put the contract somewhere else.**
- Stated texts that contradict:
  - spec:62 (WC-4): the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed; title "known before dispatch"; spec:73 (section 2.3): the brief states "the output directory, so the report path is known before dispatch".
  - spec:83 (adversarial row): "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"; AC-1.4 at spec:198 checks "adversarial names one fixed path".
  - spec:92 (workflow row): report is `.dev/tasks/to-do/<id>/return-contract.yaml`; the brief passes only `--handoff none` and no output directory; the small fix is "write the contract for pre-creation STOPs too (WC-4 'every outcome')" with no location given. INV-B:272 confirms the `<id>` directory is created by the skill and that pre-creation STOPs have no package yet (INV-B:272, "Not written for pre-creation STOPs").
- Grading sentence: an implementer who follows the stated text as written builds the adversarial contract under `<output>/adversarial/` and the workflow contract under a generated `<id>` directory (and, for a pre-creation STOP, nowhere that can be named), and that is wrong because WC-4, section 2.3, the live check step 3 at spec:182 ("its report path is the WC-4 contract path") and AC-0.4 at spec:194 (which runs exactly these two commands in P0) all require the coordinator to find the contract at `<output-dir>/return-contract.yaml` before dispatch.
- Expert attribution: Wiegers (consistency), Fowler (interface), Whittaker (Sequence Attack: a pre-creation STOP runs before the `<id>` directory exists, so the contract the rule says must be written "including stops before any other output exists" has no path).
- Recommendation: state one rule that all rows follow (for example the contract path is always the directory passed in the brief, and adversarial/workflow rows say how they meet it), or state per row that the worker reports the actual path and drop "known before dispatch" for those two.
- Priority: High. Quality-impact: the P0 smoke runs of `/sc:workflow` and `/sc:adversarial` cannot pass AC-0.4 step 3 as written.

**B2 (MAJOR, blocking). AC-1.1 requires every command in sections 3.1-3.2 to name `return-contract.yaml`, but the `/sc:load` row and the Decisions table say `/sc:load` has no report file.**
- Stated texts that contradict:
  - spec:195 (AC-1.1): the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - spec:112 (`load` row): report "none (see note)", resume "n/a", change is "use it as a step inside another worker's brief, not as its own Task", usage-line fix in P1.
  - spec:265 (Decisions): "Use it inside a brief ... a report file would be an unrequested addition."
  - spec:53 (section 2.1): each section "lists only its own gate resolutions and report file".
- Grading sentence: an implementer who follows the `load` row and the Decisions row builds a `/sc:load` section with no report file and no `return-contract.yaml`, and that is wrong because AC-1.1, the P1 gate (spec:154, "Later phases do not start until the earlier phase's checks pass"), cannot pass; the only way to pass is to add a report file to `/sc:load`, which spec:265 rejects.
- Expert attribution: Wiegers (traceability and testability), Crispin (acceptance criterion cannot pass).
- Recommendation: narrow AC-1.1 to the commands that write a contract (exclude `load`), or state what `load`'s section says in place of the contract name.
- Priority: High.

### Medium findings (warnings; listed under follow-up candidates)

- **M1. WC-4 defines `<output-dir>` as the directory passed, but tdd, spec-panel and init-lite take a FILE in `--output` (spec:87, 90, 120).** A contract at `<dir of the file>/return-contract.yaml` may share a directory with other workers (a violation of WC-11, spec:69) or with the repo's `.dev/` tree. Needs the guess that the implementer picks a different per-run directory. The command under review itself resolves this with `--report-dir` (command.md:460), which the spec never mentions; a stated rule for file-valued `--output` is missing. Origin: requirement never stated.
- **M3. Phase coverage and the P1 scope disagree.** The `Commands` columns at spec:159-162 name 35 of the 37 non-coordinator-only commands; brainstorm and init-lite (spec:84-85, 88, both "Small fix: None") appear in no phase. Spec:159 says P1 adds `--unattended` to "every command in sections 3.1 and 3.2", while the Phase column of section 3.2 defers 18 of them to P2-P4. Until their phase, those commands accept `--unattended` but still prompt (their gate conversions are in P2-P4), and nothing tells the coordinator not to dispatch them (WC-2, spec:60, says "Under `--unattended` the command never calls `AskUserQuestion`"). Needs the guess that the implementer reads the scope sentence rather than the column. Pipeline count check (FR-17/FR-19 dimensional check): 10 + 27 = 37 commands enter section 3; 35 leave through section 6.
- **M4. WC-6 "fresh output directory" vs WC-4 "directory the coordinator passed" (spec:64, 62).** A retry (`--retry-of`) reuses the same task brief and therefore the same `--output`; "fresh dir" is the stated resume answer for about 20 rows. Either the command creates a run subdirectory (then the contract is not at the pre-dispatch path) or the coordinator passes a new directory (then section 2.3, spec:73, must say so; it does not). Needs a guess.
- **M5. WC-10 covers "a single tool call" that blocks more than 5 minutes (spec:68).** An Agent-tool fan-out (tdd, adversarial, tasklist, roadmap: columns (c) of INV-A:35-55 and INV-B:31-52) is one blocking Task call that can exceed 5 minutes, and WC-7 forbids subagents from sending a heartbeat (spec:65). The rule does not say what happens; whether Orca uses heartbeat age at all is UNVERIFIED (`CAPS:182`, `CAPS:130`). The requirement is hard (split waits) but its premise is unverified, and the fan-out case is unspecified.
- **M6. Hard-coded single-owner outputs conflict with WC-11 (spec:69) for index-repo and cleanup-audit.** index-repo writes `PROJECT_INDEX.md` at the repo root with no output flag (spec:86); cleanup-audit uses a fixed `.claude-audit` directory (spec:85) and only says "one audit per worktree at a time". Two such workers in one worktree write the same file. The fix column states a location but no per-run name, and section 2.3 does not tell the coordinator to serialize them.
- **M7. WC-3 allows any blocked gate to be sent to the coordinator with `ask`, but D2 option (a) says the `/sc:implement` Ruling cannot come from another agent (spec:61, 109, 233-235; `INV-A:66`).** The implement row and AC-4.1 say the worker stops. WC-3 has no exception, so a worker may ask the coordinator and re-invoke with the answer. Needs the guess that the implementer reads D2 over WC-3.
- **M2. The tasklist row asserts its reflect fan-out is "inside Claude Code's nesting limit" (spec:122, citing INV-A:14), while INV-B:215 says the per-phase reflect fan-out must run at the worker's top level, and INV-B:209-210 marks nested spawning UNVERIFIED.** The row also makes tasklist pass `--unattended` to each reflect, and the reflect row (spec:88) makes `--unattended` follow the headless auto-accept rule, which "auto-accepts for auto-fixable registers" (INV-B:108): a remediation hand-off to `sc:workflow` or task-builder then runs inside those subagents. The nesting count covers one layer (the reflect agent) but not reflect's own `root-cause-analyst` and `confidence-calibrator` (INV-B:109, 208) or the hand-off. The Decisions row at spec:268 says "nothing read in this task contradicts a verdict". Needs the guess that the Agent tool survives four layers.
- **M8. AC-C5 (spec:176) requires edits to be purely additive (`grep -E '^-[^-]'` prints nothing), but adding `--unattended` or `--output` to a command's Usage line edits an existing line.** SA-4 (spec:149) lists named defect fixes; cleanup-audit, index-repo, cli-portify (`--resume`), spec-panel and others carry fixes that are not in that list. The check can fail on a correct edit unless the new flags go on new lines.
- **M9. "Refused" outcomes are undefined (spec:102, 103, 114, 123).** WC-2 gives three resolutions (default, flag, blocked) and says nothing about a flag the command refuses; whether a contract with `status: blocked` is written is not stated. WC-5 then maps "no report exists" to `failed`, so the result is a failed worker with no stated reason.
- **M10. WC-1 (spec:59) has no owner phase and no acceptance check.** Owner is "Launch setup, not commands"; sections 6 and 7 contain no item for the launch wrapper. 7.2 step 1 detects a failure but nothing fixes it. Origin: requirement never stated in the plan.
- **M11. Citation `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree by default" (spec:70, 73, WC-11 and section 2.3) does not support the claim.** `CAPS:115` is "Worktrees are never deleted by these verbs" (`[G:recovery]` 134-135). `grep -n placement orca-capabilities.md` finds `[G:placement]` only at lines 17, 23, 90, 115, 116, 122, none with lines 8-11 or a default-worktree statement. WC-11's premise is therefore UNVERIFIED.
- **M12. Phase gating text conflicts with the decision section.** Spec:154 says "Phases 1-3 need no user decision"; spec:225 says "Phases 0-3 can proceed on the recommendations"; D1 (the choice of `--unattended`, spec:227-231) and D4 (spec:244, affects P2 commands auggie-review and task) are decisions that P1 and P2 already depend on.
- **M13. AC-C1 scans `src/superclaude/core` (spec:172) for `orca ... orchestration|worktree|terminal|agent`, but P0 adds an Orca section to `core/HOW-WE-WORK.md` and a coordinator brief template to `core/WORKER-CONTRACT.md` (spec:158).** E5 records `grep -ci orca HOW-WE-WORK.md` as `0` (spec:26), so any literal command form in the new section fails AC-C1. SA-2 (spec:147) allows only "an example of a caller's question channel inside the contract file". The check passes only if the new text never writes those command forms; the plan does not say so.
- **M14. SA-3 (spec:148) allows the contract when "the caller passes the new output flag", but WC-4 (spec:62) writes it "in unattended mode"** and AC-1.3 (spec:197) tests only the no-flag case.

## === ARCHITECTURE ANALYSIS ===

Strengths I found no defect in: the decision to keep commands as the unit of work and place Orca above them is consistent with `CAPS:97-103` (depth 1), `CAPS:148-150` (lifecycle messages bound to the dispatched pane) and `CAPS:92`; the 10 / 27 / 6 split matches INV-A:73 and INV-B:278; section 1.4 states the evidence gaps plainly; the lifecycle split (worker session sends, command writes, coordinator reads) is coherent with `CAPS:72-80`.

Findings (all Medium unless listed above):

- Fowler (interface segregation): the shared contract file couples 37 commands to one document by installed path (`~/.claude/WORKER-CONTRACT.md`, spec:53). That is a deliberate write-once choice (spec:264), but there is no stated fallback when the file is absent in a dev checkout (UNVERIFIED: whether `core/` files are copied by `make sync-dev`; `CLAUDE.md` is not readable here). See M13 and M2 for the other boundary problems.
- Nygard (failure modes): the "silent stall" failure mode is detected by `worker-show` `agentWait` only at P-phase test time (spec:181-182). Production dispatch relies on the coordinator polling; there is no timeout requirement for a worker that is neither blocked nor done (`CAPS:188`, `CAPS:182` UNVERIFIED). Recorded under follow-up candidates.
- Hohpe (message exchange): the worker/coordinator exchange is `worker_done` plus a pointer to a file Orca does not check (`CAPS:79`, spec:62). The spec states the coordinator must open the file; it does not state what the coordinator does when the contract is missing or unparseable beyond "outcome failed".
- Newman (evolution): the contract has no version field (`status`, `command`, `report_path`, `artifacts`, `blocked_question`, spec:62), while the workflow contract already carries a version ("contract 1.1", INV-B:272). Two contract shapes will coexist.

## Adversarial analysis (Whittaker; five attacks run, a minimum on each invariant under the guard table)

Format per the command: "I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack: [scenario]."

1. I can break this specification by **Sequence Attack**. The invariant at **spec:62 (WC-4, contract written "including stops before any other output exists")** fails when `/sc:workflow` stops before creating its package. Concrete attack: before: no `.dev/tasks/to-do/<id>/` directory exists, brief passes only `--handoff none` (spec:92); step 1: workflow hits a pre-creation STOP; step 2: the rule requires a contract at `<output-dir>/...`, but no `<output-dir>` was passed; after: no contract anywhere, worker reports `--outcome failed` with no report path (WC-5). Severity CRITICAL (proven by the two texts; this is B1).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **spec:195 (AC-1.1)** fails when the command has no report file. Concrete attack: before: `/sc:load` section has no `return-contract.yaml` (spec:112, 265); step 1: run `test_worker_contract.py`; after: the assertion fails for `load`, P1 stays blocked. Severity CRITICAL (this is B2).
3. I can break this specification by **Divergence Attack**. The invariant at **spec:64 (WC-6) and spec:62 (WC-4)** fails when a retry reuses the brief's `--output`. Concrete attack: before: attempt 1 wrote `<dir>/return-contract.yaml` with `status: failed`; step 1: `worker-start --retry-of` with the same brief; step 2: the command, told to use "a fresh output directory", makes `<dir>/run-2/`; after: the coordinator opens `<dir>/return-contract.yaml` and reads the first attempt's failed contract for a successful second attempt. Severity MAJOR (reading depends on which meaning of "fresh dir" is chosen; M4).
4. I can break this specification by **Accumulation Attack**. The invariant at **spec:68 (WC-10)** fails when a foreground Agent-tool fan-out runs longer than the heartbeat cadence. Concrete attack: before: last heartbeat at t=0; step 1: `/sc:tdd` starts a 12-minute research fan-out as one Task call; step 2: WC-7 forbids the subagent from sending; after: the worker is silent for 12 minutes, and the spec states no outcome. Severity MAJOR (M5).
5. I can break this specification by **Sentinel Collision Attack**. The invariant at **spec:63 (WC-5)** fails when the word `blocked` appears as the status of a command that already used it for a different meaning. Concrete attack: before: `/sc:implement` ledger uses `E-HALT-QA` (spec:109) and the contract uses `blocked`; step 1: the contract copies the halt code into `status`; after: `status` is not one of the four values and the 7.2 step-4 check (`assert d['status'] in {...}`, spec:183) fails. Severity MINOR (behaviour inferable; the spec fixes the vocabulary).

## Quantity Flow Diagram (Pipeline Dimensional Analysis; stage count 2 or more with N != M)

```text
[Inventories: 43 commands] --> [Verdict split] --> [10 ready | 27 need change | 6 coordinator-only]
                                                        |
                                                        v
                                   [Phase assignment, spec:159-162] --> [35 of 37 listed]  <-- MISMATCH (brainstorm, init-lite unassigned)
                                                        |
                                                        v
                                   [AC-1.1: asserts 37 sections in P1] <-- MISMATCH with 35 listed and with 18 deferred to P2-P4
```

## Consensus and disagreement

- Consensus (all experts): the decision (section 1) is sound and the evidence limits are stated honestly; the two blocking findings are internal contradictions that a quick edit fixes.
- Disagreement: Wiegers would grade M3 blocking (a requirement list that omits two commands is untraceable); Fowler grades it Medium because the P1 scope sentence names them. Graded Medium under the consequence rule (needs a reading guess).

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14 (all above). Architecture notes from the section above: contract version field absent; no timeout for a worker that is neither blocked nor done.

Minor notes:
- n1. Section 4 cites `INV-B:311` (spec:128) for "Making them workers would remove their purpose"; that inventory row covers pm, spawn and swarm-wizard only, not agent, git, help.
- n2. E3 (spec:23) uses `invocation_method: "skill-direct"` as proof that Orca workers ran `/sc:adversarial`; section 1.4 (spec:43) says the PR #329 run used an Agent-tool subagent; INV-A:35 calls it "proven as a direct Orca-worker skill call". Reconcile the wording.
- n3. `CAPS:161` quotes `sc-pr-submit-protocol/SKILL.md:47-49` for the top-level rule; the spec cites `SKILL.md:37-39` (spec:65, 114). Different copies may explain this; neither file is in the workspace, so UNVERIFIED.
- n4. AC-C1 and AC-C4 in the table (spec:172, 175) show `\|` inside the command text (table escaping); run as written, `grep -E` treats `\|` as a literal pipe. Write the real command in a code block.
- n5. spec:75 says the three counts "10 ready today, 27 needing a change and 6 coordinator-only"; 3.1 is titled "Ready today", but four of the ten (reflect, release-split, tdd, troubleshoot) still carry P2 gate edits (spec:88-91).
- n6. Section 1.2 E2 (spec:22) says the worker "answered"; the quoted evidence (`CAPS:49`, `EVIDENCE.md:45`) only says `state: ready, stage: input_accepted`.

The session that ran this review asks the user once per loop whether to open an issue for the follow-up candidates; this run is a worker report and creates none. The coordinator carries the list.

## Citation check summary

- Verified against the inventories: `CAPS:44-47,52,58-61,64,66-67,72-74,76-77,79-80,86,92,97-103,107-108,116,128-130,145-151,155-156,158-161,178,180,186-188`; `INV-A:3,14,35,36,62,65,66,68,90-98,105-106,113,118,120`; `INV-B:36,52,65,105,107-115,207-215,267-275,285-286,292,294,296,301,311,320,323`; `README.md:6,11-17,30-31`.
- Not found as cited: `CAPS:115` (M11).
- UNVERIFIED (outside workspace): all `CLAUDE.md`, `src/superclaude`, `EVIDENCE.md`, `.dev/codegraph-migration`, `Makefile`, `pyproject.toml`, `plugins` citations, and the Orca `[G]`/`[H:*]` line numbers except where the inventory quotes them.

## Reviser brief

Blocking finding ids: B1, B2. The reviser reads this report, not the command.

Rules (restated from the command's Review Loop, bullet 6):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that a blocking finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone.

Findings, copied from this report:
- B1: spec:62 (WC-4) states the contract is `<output-dir>/return-contract.yaml`, known before dispatch (also spec:73); spec:83 puts the adversarial contract at `<output>/adversarial/return-contract.yaml`; spec:92 puts the workflow contract at `.dev/tasks/to-do/<id>/return-contract.yaml` with no output directory in the brief and a pre-creation STOP that has no `<id>` directory. Stated wrong outcome: the coordinator cannot find the contract at the path WC-4, 7.2 step 3 (spec:182) and AC-0.4 (spec:194) require.
- B2: spec:195 (AC-1.1) requires every command in sections 3.1-3.2 to name `return-contract.yaml`; spec:112 and spec:265 say `/sc:load` has no report file. Stated wrong outcome: AC-1.1 cannot pass for `/sc:load` without adding the report file spec:265 rejects.

verdict: FAIL

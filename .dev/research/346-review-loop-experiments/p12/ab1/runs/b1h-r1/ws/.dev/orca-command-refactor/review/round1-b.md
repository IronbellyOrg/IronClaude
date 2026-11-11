review: 1 of 3

# /sc:spec-panel critique, first review (round 1)

- **Candidate**: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (SPEC below)
- **Candidate SHA-256**: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- **Baseline**: none (first review)
- **Mode / focus**: `--mode critique --focus requirements,architecture`; Whittaker (adversarial) included because the command makes him active in every panel review (CMD:83 of the supplied command definition)
- **Reviewer model**: Claude Haiku 5.5 (`claude-haiku-5-5`), one reviewer
- **Prompt**: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy)

Citation shorthand: `SPEC:n` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line n; `README:n` = `.dev/orca-command-refactor/README.md`; `INV-A:n`, `INV-B:n`, `CAPS:n` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `CMD:n` = the supplied `/sc:spec-panel` definition (sandbox `command.md`, outside the workspace). Anything I could not check in a file inside the workspace is marked UNVERIFIED.

## Scope, evidence and what this review did not do

1. **Read in full**: SPEC, README, INV-A, INV-B, CAPS, the supplied command definition (CMD), and the FIRST-REVIEW prompt file.
2. **Checked**: the 10 / 27 / 6 split against INV-A:73 (5 ready, 13 needs-change, 3 coordinator-only) and INV-B:278 (5, 14, 3); the section 3.1 and 3.2 row lists against the inventory row numbers they cite; a sample of CAPS line citations (CAPS:44-45, 46, 52, 60, 73, 76, 77, 78, 80, 98, 115, 116, 130, 149), all of which match the quoted text; the internal arithmetic and cross-references between SPEC sections.
3. **Not checkable here (UNVERIFIED)**: every citation into `src/superclaude/`, `.dev/evals/`, `.dev/codegraph-migration/`, the Orca program files, `CLAUDE.md` and `HOW-WE-WORK.md`. These are outside the workspace. Section 1.2 E3 and E5 (SPEC:23, SPEC:25), the PR #329 chain (SPEC:43), D1 (SPEC:229) and the install claims (SPEC:52) therefore rest on evidence I could not read. Findings below do not depend on those citations except where marked.
4. **Not run by this reviewer**: the FIRST-REVIEW prompt asks for three fresh-context reviewers, a MERGE by the coordinator, and a VERIFY pass by a fresh verifier on every blocking finding. I am one reviewer with no subagent tool, so this file is one first-review report, not a merged one. The coordinator must run VERIFY on B1-B5 before any revision. Under the VERIFY rule a verifier reply with no `confirmed:` line confirms every finding.

## Strengths (no finding)

- The 10 ready / 27 needs-change / 6 coordinator-only split is internally consistent (SPEC:76, SPEC:278 cross-check, INV-A:73, INV-B:278).
- SA-1 to SA-3 (SPEC:146-148) give a clear standalone-compatibility rule, and WC-9 (SPEC:67) keeps outward actions off by default.
- The decision not to let commands call Orca (SPEC:29-37) is argued with evidence, and section 1.4 states its own gaps (SPEC:41-45).

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1. The contract path rule is contradicted, and the workflow path is not known before dispatch.** (Wiegers lead; Fowler)
- Locations: SPEC:62 (WC-4: `<output-dir>/return-contract.yaml`, "known before dispatch"), SPEC:73 (the coordinator's brief states the output directory), SPEC:83 (adversarial: fix the filename to `<output>/adversarial/return-contract.yaml`), SPEC:92 (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`, "Fresh package each run"; no output flag). Supporting: INV-B:52, INV-B:272 (the workflow package is created fresh per run).
- Grading sentence: an implementer who follows WC-4 at SPEC:62 writes adversarial's contract to `<output>/return-contract.yaml`, but the row at SPEC:83 names `<output>/adversarial/return-contract.yaml`, so the path the coordinator computes from SPEC:73 and the file the worker writes differ. For workflow, the id is generated per run and SPEC:92 gives no flag that sets it, so the coordinator cannot know the path before dispatch, which WC-4 requires.
- Recommendation: state one path rule. Either `<brief-output-dir>/return-contract.yaml` for every command, with the adversarial subfolder named as the output dir, or name the exact path per command. Give workflow an explicit `--output` or `--id` flag, or exempt it from WC-4 and say so.
- Priority: High. Quality impact: high (the coordinator's `test -s` check, SPEC:183, and its outcome mapping then read the wrong file or none).

**B2. WC-3 lets a coordinator's answer resume a command past a safety gate.** (Wiegers lead; Whittaker)
- Locations: SPEC:61 (WC-3: on a gate that would be blocked, the session may `ask` the coordinator, "then re-invoke or resume the command with the answer as a flag"), SPEC:109 (implement: "the Ruling rule itself is unchanged (see open decision D2)"), SPEC:233 (the spec quotes the rule: "another agent's message ... [is] not acceptance"), SPEC:234-236 (D2 recommends option (a), keep the rule), SPEC:208 (AC-4.1 relies on D2).
- Grading sentence: an implementer who follows WC-3 at SPEC:61 has no exclusion for the implement Ruling, so the coordinator's `ask` reply can be passed back to `/sc:implement` as a flag, which resolves a halt that SPEC:109 says keeps the Ruling rule unchanged, and the rule the spec itself quotes at SPEC:233 excludes a message from another agent.
- Recommendation: scope WC-3 so that a relayed answer is never accepted as a Ruling until D2 is decided, and name the implement halt as the exception. Keep D2(a) as the default in the text.
- Priority: High. Quality impact: high (safety-boundary risk named by the grading rule).

**B3. The P0 acceptance run cannot pass as written.** (Adzic; Wiegers)
- Locations: SPEC:182 (7.2 step 3, pass: "its report path is the WC-4 contract path"), SPEC:194 (AC-0.4: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"), SPEC:159 (P1 is where WC-4 is delivered).
- Grading sentence: an implementer who runs AC-0.4 in P0 on `/sc:troubleshoot` finds step 3 fails, because step 3 requires the WC-4 contract path and WC-4 does not exist until P1 (SPEC:159), while AC-0.4 says step 3 passes.
- Recommendation: in AC-0.4, exempt step 3's contract-path check the same way step 4 is exempted, or move the whole 7.2 check to P1.
- Priority: High. Quality impact: medium (P0 gate is blocked; the "earlier failure reopens section 1" rule then fires for a test-harness reason).

**B4. Step 6 cannot pass for edit-in-place commands, including their P2 happy path.** (Wiegers; Cockburn)
- Locations: SPEC:185 (step 6: "only files under the brief's output directory (and the command's documented artifacts) appear"), SPEC:201 (AC-2.3: a P2 happy-path run must pass 7.2), SPEC:103 (cleanup applies items) and SPEC:110 (improve applies items), both in P2 (SPEC:160). Supporting: INV-A:43 and INV-A:52 ("Edits code").
- Grading sentence: an implementer who runs cleanup's happy path under step 6 as written sees its edited source files in `git status`, and those files are neither under the output directory nor documented artifacts of the command, so the check fails for a correct run; the only way to pass is to read "documented artifacts" as including applied edits, which the spec never says.
- Recommendation: split step 6 by command class. Report-only commands show only output-dir files. Edit-in-place commands show exactly the files their contract lists under `artifacts` (WC-4), and the contract must list them.
- Priority: High. Quality impact: medium.

**B5. AC-C1 forbids the Orca mention that SA-2 permits, and P0 writes that mention.** (Fowler; Newman)
- Locations: SPEC:172 (AC-C1 greps `src/superclaude/core`), SPEC:147 (SA-2: "the only allowed mention of Orca in a changed command is ... inside the contract file"), SPEC:52 and SPEC:158 (the contract file is `src/superclaude/core/WORKER-CONTRACT.md`; P0 adds an Orca section to `HOW-WE-WORK.md`, also in core).
- Grading sentence: an implementer who writes the contract file as SA-2 permits, naming the `orca orchestration ask` question channel, makes AC-C1 print a match over `src/superclaude/core`, so AC-C1 fails in P0 on text the spec allows.
- Recommendation: either exclude `core/WORKER-CONTRACT.md` and the routing-guide Orca section from AC-C1 by name, or restate SA-2 so its allowance matches what AC-C1 scans.
- Priority: High (blocks P0). Quality impact: medium.

### Medium findings (follow-up candidates, not blocking)

**M1. The 3.1 brief column omits `--unattended` that 2.3 requires.** (Wiegers) SPEC:73 says every Task's command line includes `--unattended`; the 3.1 "Brief must pass" entries at SPEC:83-92 do not. P0 cannot pass it because P1 adds the flag (SPEC:159). Recommendation: state P0's invocation explicitly and add `--unattended` to the 3.1 column once P1 lands.

**M2. Concurrent workers may edit the same product files.** (Nygard) WC-11 (SPEC:69) covers only default output-file collisions. Default placement puts workers in the current worktree (CAPS:115). Edit-in-place rows (SPEC:103, 109, 110, 121) let two workers in one worktree edit the same source file, and nothing forbids it. Recommendation: one editing worker per worktree, or a file-ownership rule in the brief.

**M3. Fixed-path commands conflict with WC-6.** (Nygard; Wiegers) WC-6 (SPEC:64) requires a fresh output directory when a command has no resume flag. SPEC:87 (init-lite: "re-run overwrites its marked report") and SPEC:86 (index-repo, fixed `PROJECT_INDEX.md`) do not. SPEC:85 handles cleanup-audit with a one-at-a-time rule. Whether an overwrite "corrupts" the first attempt is a judgment, which is why this is Medium. Recommendation: list the idempotent fixed-path exceptions in WC-6.

**M4. The output-directory flag is not uniform.** (Wiegers) WC-4 says `--output` / `--output-dir` (SPEC:62), and the 3.1 and 3.2 rows use `--output <dir>`, `--output <file>` and `--pass`. The supplied command definition uses `--report-dir` for unattended directories and `--output` for a file (CMD:23). Without a canonical name, the 2.3 brief template cannot be uniform. Recommendation: name one flag and a rule for commands that already use another. (The repo-level facts here are UNVERIFIED.)

**M5. The spec-panel row describes a state the supplied command does not have.** (Wiegers; Whittaker FR-2.2) SPEC:120 says "add `--output`" and relies on INV-B:182 ("no `--output` flag exists"). The supplied definition already lists `--output <file>` (CMD:23) and has an `## Unattended mode` section (CMD:455-465). Whether that is the repo's current file is UNVERIFIED because `cmd/spec-panel.md` lies outside the workspace. Recommendation: reconcile row 120 and INV-B:182 with the file the repo actually holds before P1; an implementer following row 120 would duplicate the flag.

**M6. A FAIL audit settles as succeeded and nothing gates dependents on the verdict.** (Whittaker FR-2.2; Hohpe) WC-5 (SPEC:63) and the Decisions row (SPEC:263) map `partial` to `succeeded`; SPEC:63 also maps an audit whose verdict is FAIL to `succeeded`. A valid `worker_done` settles the Task automatically (CAPS:77), so a dependent Task can start on a FAIL verdict. Nothing in 2.3 (SPEC:73) requires the coordinator to read the verdict before releasing dependents. Recommendation: either map a FAIL verdict to `failed`, or state that the coordinator must gate dependents on the report's verdict.

**M7. The blocked and ask paths have no defined order, and no actor owns the blocked outcome.** (Cockburn; Whittaker FR-2.4) WC-2(c) (SPEC:60) and WC-5 (SPEC:63) make `blocked` into `worker_done failed`. WC-3 (SPEC:61) lets the session ask first and resume. Once `worker_done` is sent the worker idles (CAPS:78), so a late answer can only arrive through a new `worker-start --retry-of`, which SPEC:64 would run in a fresh directory and so lose the partial work. The spec does not say who reads a blocked contract and who contacts the person (D2 at SPEC:234 is the only named path). Recommendation: state the sequence (answer before `worker_done`, or retry after) and name the coordinator's blocked-outcome owner.

**M8. Blocked re-dispatch has no cap.** (Whittaker FR-2.5) The circuit breaker counts failed `worker-start` attempts, not a worker's own `failed` report (CAPS:80; CAPS:116). A Task that reports `blocked` every time can be re-dispatched indefinitely with no spec limit. Recommendation: cap blocked or failed re-dispatches per Task and escalate at the cap.

**M9. A stale contract can be read as this attempt's result.** (Nygard) WC-5 (SPEC:63) decides "no report exists" means failed. Resume (WC-6, SPEC:64) and a crash after an earlier attempt both leave an old `status: succeeded` file in place, and nothing requires deleting or replacing the contract when a run starts. Recommendation: the command deletes or rewrites its contract at start, or the coordinator checks its timestamp against the dispatch.

**M10. The contract schema, its version and the write order are not fixed.** (Fowler; Newman; Hohpe) SPEC:62 says the contract "carries at least" five fields, with no schema or version field. INV-B:272 shows workflow already has its own "contract 1.1", which the spec does not reconcile. Nothing says the file must be complete on disk before `worker_done` is sent, and `--report-path` is payload only (CAPS:79, UNVERIFIED whether Orca reads it). Recommendation: publish a schema with a version field, and require the write to finish before `worker_done`.

**M11. Two requirements are not measurable.** (Wiegers; Adzic) WC-1 (SPEC:59) says a fallback must sit "well inside" the readiness limit, with no number. The WC-10 wait split is measurable (at most 4 minutes), but the mechanism for cli-eval's up-to-3600 s wait is not given (SPEC:68, SPEC:104; INV-A:65). Recommendation: give WC-1 a number, such as 30 s, the figure EVIDENCE supports (SPEC:52 and CAPS:49, UNVERIFIED here), and name the poll loop for cli-eval.

**M12. Acceptance coverage has gaps.** (Wiegers, traceability) No check in SPEC:171-210 tests WC-1, WC-3, WC-6, WC-7 or WC-12. AC-0.4 says the Agent-tool wrapper is "verified in the step-5 transcript" (SPEC:194), but step 5 (SPEC:184) searches only for `AskUserQuestion`. Recommendation: add one check per requirement and a wrapper check to step 5.

**M13. `load` is contradictory.** (Cockburn; Wiegers) The 3.2 row (SPEC:112) says `load` writes no file and is used as a step, yet AC-1.1 (SPEC:195) requires every 3.2 command to name `return-contract.yaml`. Recommendation: exempt `load` from AC-1.1, or give it a contract.

**M14. Gates that are not listed have no rule.** (Wiegers) WC-2 (SPEC:60) says gates resolve "listed per command in section 3", with no rule for a gate the list does not name. Recommendation: add a default: any unlisted gate resolves as blocked.

## === ARCHITECTURE ANALYSIS ===

Architecture findings are in the Whittaker and Nygard bucket above (M2, M6-M10) and in the blocking set (B1, B5). Two further architecture notes:

**M15. A missing output flag lands the contract in an unknown place.** (Whittaker FR-2.1; Fowler) If a brief omits `--output`, adversarial writes next to its input files (INV-A:61, UNVERIFIED in repo terms), and the contract is written there under a path the coordinator does not compute. The spec has no rule that makes an omitted output flag `blocked`. Recommendation: under `--unattended`, a missing output flag resolves as blocked (WC-2(c)).

**Architecture check that holds**: the single-worker-per-Task model (SPEC:16, 39) keeps each Orca record and retry at the Task level, as the spec says (SPEC:39), so the design does not need command-level Orca calls.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- **FR-2.1 Zero/Empty**: I can break this specification by **Zero/Empty Attack**. The invariant at SPEC:62 (contract at `<output-dir>`) fails when the brief omits `--output`. Concrete attack: the coordinator sends `/sc:adversarial` with no `--output`; the command writes beside its input files; the coordinator's `test -s` (SPEC:183) checks the path it computed; `worker_done` then settles `succeeded` on a file the coordinator never reads. Severity: MAJOR, graded Medium (M15), since it needs a brief error.
- **FR-2.2 Divergence**: I can break this specification by **Divergence Attack**. The invariant at SPEC:63 fails when the audit's verdict is FAIL and its status is `succeeded`: the two branches of the outcome rule meet, and the verdict branch is not in the mapping. Concrete attack: a `reflect` audit reports FAIL, the contract says `succeeded`, the Task completes, and a dependent starts (CAPS:77). Severity: MAJOR, graded Medium (M6).
- **FR-2.3 Sentinel Collision**: no concrete wrong outcome found in the `status` vocabulary (SPEC:62-63), since `blocked_question` is defined only for `blocked` and that is stated. A `partial` contract that carries a question has no rule (minor, N2).
- **FR-2.4 Sequence**: I can break this specification by **Sequence Attack**. The invariant at SPEC:61 and SPEC:63 fails when the coordinator's answer arrives after `worker_done failed`. Concrete attack: the worker writes `status: blocked`, sends `worker_done --outcome failed`, idles (CAPS:78); the answer arrives; no path re-invokes the command in that session, so the answer is either lost or handled by a retry that starts clean. Severity: MAJOR, graded Medium (M7).
- **FR-2.5 Accumulation**: I can break this specification by **Accumulation Attack**. The invariant at SPEC:63 fails when a Task reports `blocked` on every dispatch: the circuit breaker does not count it (CAPS:80), so re-dispatch has no cap. Concrete attack: 50 blocked dispatches, no escalation. Severity: MAJOR, graded Medium (M8).

## Guard Condition Boundary Table (mandatory: the spec has conditional logic, thresholds and guards)

Rows cover each guard named in the spec; input classes that cannot occur for a boolean or enumerated guard are left out with their reason (one-line reason: "Maximum/Overflow" is not a value for the outcome enum or the flag, and is covered for the readiness timer in row 18). GAP rows generate the finding named in the last column (FR-8). FR-10 is met: every guard is enumerated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | SPEC:51, SPEC:146 | Zero/Empty: flag absent | not present | false | standalone behavior unchanged (SA-1) | OK |
| `--unattended` switch | SPEC:51, SPEC:60 | Typical: flag present | present | true | gates resolve (a), (b) or (c) (WC-2) | OK |
| `--unattended` switch | SPEC:51, SPEC:228 | Sentinel: a person types the flag | present | true | gates block, by design (D1 (a)) | OK |
| gate resolution | SPEC:60, SPEC:75 | Legitimate edge: gate not listed in section 3 | gate absent from row | n/a | not specified | GAP (M14) |
| outcome mapping | SPEC:63 | Typical: `status: succeeded` | `succeeded` | `worker_done succeeded` | as stated | OK |
| outcome mapping | SPEC:63, SPEC:263 | One/Minimal: `status: partial` | `partial` | `succeeded` | body's first sentence states partial | OK |
| outcome mapping | SPEC:63 | Legitimate edge: audit verdict FAIL, status `succeeded` | FAIL + `succeeded` | `succeeded` | Task completes; dependents not gated | GAP (M6) |
| outcome mapping | SPEC:63 | Zero/Empty: no contract written | no file | `failed` | as stated | OK |
| outcome mapping | SPEC:62-63 | Sentinel: stale contract from earlier attempt | old file present | read as success | not specified | GAP (M9) |
| outcome mapping | SPEC:62, SPEC:63 | Zero/Empty: contract without `status` | `status` absent | not one of four values | not specified | GAP (M10) |
| retry directory | SPEC:64 | Typical: no resume flag, retry | retry | fresh dir | as stated | OK |
| retry directory | SPEC:64, SPEC:87 | Legitimate edge: init-lite re-run | overwrite | overwrites marked report | conflicts with WC-6 | GAP (M3) |
| contract path | SPEC:62, SPEC:83 | Legitimate edge: adversarial subfolder | `<output>/adversarial/` vs `<output-dir>/` | two rules | contradictory | GAP (B1) |
| contract path | SPEC:62, SPEC:92 | Zero/Empty: workflow, no output flag | id generated per run | path unknown before dispatch | not specified | GAP (B1) |
| `ask` after gate | SPEC:61, SPEC:109, SPEC:233-236 | Legitimate edge: coordinator answers a Ruling halt | answer text | re-invoke with flag | D2 recommends refusal | GAP (B2) |
| `ask` timeout | SPEC:61, CAPS:60 | Boundary: timeout expires | pending message | resume same ID | as stated; default value not relied on | OK |
| `ask` after failure | SPEC:61, SPEC:63 | Sequence: answer after `worker_done failed` | late reply | session idle | no path | GAP (M7) |
| wait split | SPEC:68 | Boundary: single tool call of 240 s | 240 s | below 5 min | heartbeat interval holds | OK |
| wait split | SPEC:68, SPEC:104 | Legitimate edge: cli-eval eval of 3600 s | 3600 s | split required | mechanism not given | GAP (M11) |
| readiness | SPEC:59, CAPS:44 | Boundary: fallback prompt timing | "well inside" | no number | not measurable | GAP (M11) |
| `consumer_fenced` | SPEC:70, CAPS:67 | Typical: check returns `consumer_fenced` | returned | stop, no `worker_done` | as stated | OK |
| outward default | SPEC:67 | Zero/Empty: brief without authorization | none | outward off | as stated | OK |
| 7.2 step 6 | SPEC:185, SPEC:201 | Legitimate edge: edit-in-place happy path | product files edited | check fails | literal reading fails | GAP (B4) |
| P0 gate | SPEC:182, SPEC:194 | Zero/Empty: P0, no contract yet | no contract | step 3 fails | AC-0.4 says passes | GAP (B3) |
| AC-C1 | SPEC:147, SPEC:172 | Legitimate edge: contract names the question channel | match | grep prints | SA-2 permits it | GAP (B5) |
| standalone write | SPEC:148 | Typical: no flag, no unattended | none | no contract | as stated | OK |

Pipeline Dimensional Analysis: **not triggered**. The spec describes control flow (Task creation, dispatch, settlement), not a data pipeline whose item count changes between stages, so no Quantity Flow Diagram is required. State Variable Registry: not required (focus is not correctness).

## Follow-up candidates (Medium and minor; not blocking; never trigger a revision)

- M1 to M15 as listed above (requirements and architecture, plus the Whittaker FR-2.1 finding as M15).
- N1 (minor): evidence limits. The core decision rests partly on out-of-workspace citations (SPEC:23, SPEC:25, SPEC:43). UNVERIFIED here, not wrong on the face of the spec.
- N2 (minor): a `partial` contract that carries a `blocked_question` has no rule (SPEC:62 defines the field only for `blocked`).
- N3 (minor): SPEC:11 says 11 locations were re-read on 2026-11-02; those reads are not checkable here.
- N4 (minor): the spec's count of 43 commands matches INV-A:3 (21) plus INV-B:3 (22) but the repo count is UNVERIFIED.

## Decisions (this reviewer)

| Decision | Options | Rationale |
|---|---|---|
| Include Whittaker | include, or omit | The command makes him active in every panel review, and the focus does not exclude him. |
| Grade by consequence | blocking vs Medium for each | Blocking only where a stated text contradicts another, or an acceptance check cannot pass as written, or a safety boundary is involved (B1-B5). Everything needing an assumed brief error or an unstated coordinator behavior is Medium. |
| Treat out-of-workspace citations | accept, or mark UNVERIFIED | Marked UNVERIFIED per the brief; no blocking finding rests only on them (B1-B5 cite workspace files or SPEC text). M5 depends on CMD and is marked as such. |

## Reviser brief

Blocking finding ids (VERIFY pending, see scope item 4): **B1, B2, B3, B4, B5**.

Revise only text a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

verdict: FAIL

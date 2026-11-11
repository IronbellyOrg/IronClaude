review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `a6e5c8f0ff0545238ba19f3f7d98a7d4329bb51a628932a5ec8669cc448da770`
- baseline: none given (first review, no `--re-review`, no `--baseline`)
- reviewer model used: claude-sonnet-5-5
- focus: requirements, architecture. Panel: Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active) and Crispin (completeness of the guard table).
- Evidence rule: only the files in the sandbox can be checked. `INV-A` = `inventory/commands-a.md`, `INV-B` = `inventory/commands-b.md`, `CAPS` = `inventory/orca-capabilities.md`, `SPEC` = the candidate, `README` = `.dev/orca-command-refactor/README.md`. Every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` or Orca output that I reached only through an inventory quote is marked UNVERIFIED (seen as quoted, not re-read at its source).

## Coverage
- Whole document: sections 1-9, the Decisions table and the UNVERIFIED list (SPEC:1-285).
- Cross-checked against all three inventories: the 10 / 27 / 6 split (INV-A:73, INV-B:278; SPEC:76), the section 3 rows against their inventory rows, the Orca claims in sections 1 and 2 against CAPS, and the phase and acceptance-check tables against each other (SPEC:156-210).
- Not covered: the source files behind the inventories (not in the sandbox). The statement that a validator re-read about 340 citations (SPEC:285) and the re-read of 11 locations (SPEC:11) are UNVERIFIED here.
- Skipped on purpose: the Improve step (first review in `critique` mode writes no revised specification).

## Findings

### Blocking

#### F-01 CRITICAL-by-consequence (blocking). WC-4 puts the report file in a directory that parallel workers share, which contradicts WC-11
Expert: Nygard (lead), Whittaker (Sequence and Accumulation attacks), Fowler.
Texts that contradict:
- WC-4 (SPEC:62): "when `--output` names a file (tdd, init-lite, spec-panel), `<output-dir>` is that file's parent directory", and for `workflow` "`.dev/tasks/to-do/` when a STOP comes before any `<id>` exists". The report is always `<output-dir>/return-contract.yaml`.
- WC-11 (SPEC:69): "Two workers in one worktree must never write the same file."
- 3.1 tdd row (SPEC:90) and INV-B:222: the default tdd output is `docs/[domain]/TDD_[COMPONENT-NAME].md`, so several TDD files normally sit in one directory.

Grading sentence: An implementer who follows WC-4 as written builds a contract path equal to the parent directory of each `--output` file plus `return-contract.yaml`, and that is wrong because two workers whose `--output` files are siblings write the same contract file, so the coordinator reads the other worker's status.

Concrete attack (Whittaker, Sequence plus Accumulation, state trace):
1. Coordinator starts worker A with `/sc:tdd "login" --unattended --output docs/auth/TDD_LOGIN.md` and worker B with `/sc:tdd "session" --unattended --output docs/auth/TDD_SESSION.md`.
2. Before: `docs/auth/` holds no `return-contract.yaml`. A finishes and writes `docs/auth/return-contract.yaml` with `status: succeeded`; A sends `worker_done --outcome succeeded --report-path docs/auth/return-contract.yaml`.
3. B then fails and overwrites the same file with `status: failed`. After: the coordinator opens A's `--report-path` (WC-4 says the coordinator opens it, SPEC:62) and sees `failed`, so A's good TDD is treated as lost. The live check AC-1.2 step 3 ("its `--outcome` matches the contract's `status`", SPEC:182) fails for A.
4. The same file is shared by every `workflow` worker that stops before a package id exists (`.dev/tasks/to-do/return-contract.yaml`), and by `init-lite` and `spec-panel` workers whose `--output` files share a directory.

The brief-side defence in 2.3 (SPEC:73, "the output directory where the command takes one") does not cure it, because for these three commands the directory is derived from a file path the spec itself makes the parent.
Quality impact: High (the coordinator's only completion signal becomes wrong under parallel use, which is the design's purpose).

#### F-02 MAJOR (blocking). Acceptance check AC-1.1 cannot pass at Phase 1, and under decision D3 option (a) can never pass
Expert: Adzic (testability), Wiegers.
Texts that contradict:
- AC-1.1 (SPEC:195): the test asserts that "every command in sections 3.1-3.2 whose row adds a section (not `load`, and not a 3.1 row whose small-fix column is `None`)" has a `## Unattended mode` section.
- Section 6 (SPEC:154) and 7 (SPEC:167): "Later phases do not start until the earlier phase's checks ... pass"; "A phase passes only when every check in its block ... passes."
- The rows themselves assign most of those commands to P2, P3 and P4 (SPEC:99-125, e.g. tasklist P2, roadmap P3, implement P4), and D3 option (a), the recommendation, says "no pr-submit changes in Phase 4" (SPEC:240).

Grading sentence: An implementer who builds the P1 test exactly as AC-1.1 is written asserts a section in about 34 commands, and that is wrong because 26 or more of those commands are not edited until P2-P4, so P1 cannot pass, P2 cannot start, and pr-submit (and any command declined under D2-D4) never gets the section the test demands.

Dimensional trace (Fowler, Pipeline Dimensional Analysis): see the Quantity Flow Diagram below. 37 dispatchable commands feed a test over 34, and P1 edits 13 (9 new plus 4 fixes, SPEC:159), so the "every command" assertion has no phase-scoped form in the text.
Quality impact: High (a gate that blocks the whole rollout).

### Medium (warnings, listed under follow-up candidates)

| id | Grade | Expert | Finding | Citation |
|---|---|---|---|---|
| F-03 | Medium | Wiegers | Line 79 says ready-today commands change only by the "small fixes in the last column", so brainstorm and init-lite (small fix `None`) get no change. But 2.3 requires `--unattended` in every worker command line (SPEC:73), P1 says the flag is "accepted by every command in sections 3.1 and 3.2" (SPEC:159), and WC-4 names init-lite as writing a contract (SPEC:62) while init-lite has no contract today (INV-A:55). The guess needed: whether an unknown `--unattended` is ignored or rejected, and whether init-lite writes a contract. | SPEC:62,73,79,87,159; INV-A:55 |
| F-04 | Medium | Cockburn | auggie-review: the row says posting "returns only with an explicit `--post-pr` in the brief" (SPEC:100) and D4 repeats it (SPEC:244), but the inventory knows only `--no-post-pr` (INV-A:38, INV-A:78); the row's "Other required change" is `none`, so a flag that does not exist is treated as existing. WC-9 needs "the command's own explicit flag" (SPEC:67). | SPEC:67,100,244; INV-A:38 |
| F-05 | Medium | Adzic | SA-3 lets report files appear "when the caller passes the new output flag" without `--unattended` (SPEC:148), while WC-4 writes the contract "in unattended mode" (SPEC:62) and AC-1.3 tests only the case with neither (SPEC:197). Whether `--output` alone writes a contract is stated two ways. | SPEC:62,148,197 |
| F-06 | Medium | Newman | AC-C1 requires the grep to print nothing over `src/superclaude/core` (SPEC:172), but P0 adds an Orca section to `HOW-WE-WORK.md` and a `WORKER-CONTRACT.md` in that folder (SPEC:158), and SA-2 allows an Orca example in the contract file (SPEC:147). A literal `orca orchestration ask` example matches the pattern, so P0 could fail its own common check. | SPEC:147,158,172 |
| F-07 | Medium | Nygard | WC-3 lets any blocked gate be answered by the coordinator through `ask` (SPEC:61), but for implement the Ruling rule says another agent's message is not acceptance (INV-A:66, SPEC:233) and D2(a) says the worker stops and ends `failed` (SPEC:234). WC-3 has no carve-out for the Ruling. | SPEC:61,109,233-236; INV-A:66 |
| F-08 | Medium | Fowler | tasklist row says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122). INV-B:210 and INV-B:314 mark nested spawning UNVERIFIED, and INV-B:215 recommended running reflect without `--remediate` or at top level; the spec instead passes `--unattended` so reflect auto-accepts remediation (SPEC:122) with no UNVERIFIED mark and no reason for the change. reflect itself spawns agents (INV-B:111), so the fan-out is two layers down. | SPEC:122; INV-A:14; INV-B:111,210,215 |
| F-09 | Medium | Whittaker | Sequence attack on retry: WC-6 lets a resumed run reuse the same output directory (SPEC:64) while the contract has a fixed filename (SPEC:62). A first attempt leaves `status: blocked` (or `succeeded`) there; if the retry dies before writing, the stale file is read as the result, and WC-5's "or no report exists" (SPEC:63) is never true. Nothing says to delete or overwrite-first. | SPEC:62-64 |
| F-10 | Medium | Wiegers | P1 and the "Phases 1-3 need no user decision" claim (SPEC:154) conflict: P1 adds `--unattended` to every 3.1/3.2 command (SPEC:159), including implement, post-release and pr-submit, whose handling waits on D2-D4 (SPEC:162). | SPEC:154,159,162 |
| F-11 | Medium | Crispin | AC-0.4 step 4 says to use "the command's existing report file" (SPEC:194), but step 4 of 7.2 loads YAML and asserts `d['status']` and `d['command']` (SPEC:183); `REPORT.md` (troubleshoot) and a TDD are not YAML. | SPEC:183,194 |
| F-12 | Medium | Newman | WC-4 keeps existing contract fields (SPEC:62) while the Decisions table fixes the status set `succeeded/partial/failed/blocked` (SPEC:262). The existing statuses of workflow, reflect and adversarial are not given in the inventories, so a clash is possible and unaddressed. | SPEC:62,262; INV-B:272 |
| F-13 | Medium | Wiegers | WC-11 is not applied to reflect, which writes a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114), or to index-repo's fixed `PROJECT_INDEX.md` (INV-A:53); row 3.1 handles only cleanup-audit (SPEC:85). | SPEC:69,85,88; INV-B:114 |

### Minor (notes)
- N-1 E2 says the worker "answered" (SPEC:22); the quoted evidence (CAPS:49) shows only `state: ready, stage: input_accepted`.
- N-2 7.2 step 5 searches the transcript for the string `AskUserQuestion` (SPEC:184), which also matches tool lists or quoted command text; a tool-call match is needed.
- N-3 The Section 4 `/sc:git` reason cites a rule of this run (README:31) as if it were a standing repo rule (SPEC:133).
- N-4 Section 6 says Phase 0 "starts with live smoke runs" (SPEC:43), but the P0 row writes the contract file first and runs the smokes second (SPEC:158).
- N-5 Phase 1 is described as commands "with no gate" (SPEC:159) but includes business-panel, explain and index, whose rows refuse or pin a mode (SPEC:102,108,111).

## Mandatory artifact: Guard Condition Boundary Table
Guards found: WC-1 (readiness limit), WC-2 (gate), WC-5 (outcome mapping), WC-8 (depth), WC-10 (wait size), WC-12 (consumer_fenced), WC-4 (`--output` kind). Classes left out are noted per guard. Status GAP is graded under the FR-8 rule: blocking only when it names a concrete wrong outcome (F-01 covers WC-4/Typical).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `output_kind` | SPEC:62 | Zero/Empty | `--output ""` or absent | none stated | not specified for a command with no `--output` default (autoderived dir for adversarial only, SPEC:62) | GAP (Medium, F-03) |
| `output_kind` | SPEC:62 | One/Minimal | `--output out.md` (no directory part) | file, parent is `.` | contract written to the working directory root; not stated | GAP (Medium, F-01 family) |
| `output_kind` | SPEC:62 | Typical | `--output docs/auth/TDD_X.md` | file | contract in `docs/auth/` | GAP (blocking, F-01: shared directory) |
| `output_kind` | SPEC:62 | Legitimate Edge Case | `--output dir/` vs a file with no extension | dir or file? | no rule to tell a directory from a file | GAP (Medium, F-01 family) |
| `wait_size` (WC-10) | SPEC:68 | Zero/Empty | wait of 0 s | under 4 min | no behavior needed | OK |
| `wait_size` (WC-10) | SPEC:68 | Typical | 3 min wait | true | heartbeat between waits | OK |
| `wait_size` (WC-10) | SPEC:68 | Sentinel Value Match | exactly 4 min / 5 min | boundary: 4 min allowed, "longer than 5" is the trigger | split to at most 4 min; 4 to 5 min is covered | OK |
| `wait_size` (WC-10) | SPEC:68 | Maximum/Overflow | cli-eval eval of 3600 s | exceeds 5 min | split into at most 4 min waits | OK |
| `outcome_map` (WC-5) | SPEC:63 | Zero/Empty | no contract file | no report | `--outcome failed` | OK |
| `outcome_map` (WC-5) | SPEC:63 | Sentinel Value Match | stale contract from an earlier attempt | report exists | maps the stale status | GAP (Medium, F-09) |
| `outcome_map` (WC-5) | SPEC:63 | Legitimate Edge Case | `partial` | non-failed | `succeeded`, body says partial | OK |
| `gate_unattended` (WC-2) | SPEC:60 | Zero/Empty | `--unattended` absent | false | SA-1: unchanged behavior | OK |
| `gate_unattended` (WC-2) | SPEC:60 | Typical | flag present, gate has a documented default | true | default applies | OK |
| `gate_unattended` (WC-2) | SPEC:60 | Sentinel Value Match | flag present on a command with no section (init-lite, brainstorm) | true | not specified | GAP (Medium, F-03) |
| `nested_depth` (WC-8) | SPEC:66 | Typical | depth 1, command calls `worker-start` | exceeded | refused; commands must not call it | OK |
| `nested_depth` (WC-8) | SPEC:66 | Legitimate Edge Case | depth 1, `task-create` | UNVERIFIED | forbidden either way | OK |
| `consumer_fenced` (WC-12) | SPEC:70 | Typical | `check` returns `consumer_fenced` | true | stop, no `worker_done` | OK |
| `consumer_fenced` (WC-12) | SPEC:70 | Zero/Empty | `check` returns empty | false | not read as replaced (CAPS:67) | OK |

Left out, with reason: Maximum/Overflow for `output_kind` and `gate_unattended` (a path or a flag has no capacity bound in the text); Sentinel and Maximum rows for `consumer_fenced` (one signal value, no numeric range).
FR-10 gate: the table is complete (all guards enumerated, each class given a row or a reason), so synthesis is not blocked.

## Mandatory artifact: Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)
Trigger met: the rollout is a multi-stage flow where counts change (SPEC:76, SPEC:195).

```text
[Commands in src/superclaude/commands: 43] --> [Stage 1: classify] --> [coordinator-only 6 | dispatchable 37 (10 ready + 27 change)]
                                                   |
                                                   v
                                      [Stage 2: WC-4 contract required: 37 (SPEC:62)]
                                                   |  load writes none (SPEC:112) --> 36 files expected
                                                   v
                                      [Stage 3: AC-1.1 asserts a section]
                                         literal text: 37 - load - None rows (brainstorm, init-lite) = 34 <-- expects P2-P4 commands now
                                         P1 edits: 9 new commands + 4 fixes = 13 (SPEC:159)           <-- MISMATCH 34 vs 13 (F-02)
                                                   |
                                                   v
                                      [Stage 4: contract path per worker: 36]
                                         distinct directories only if each --output differs  <-- MISMATCH: file-valued --output => shared dir (F-01)
```

Count facts checked: 10 + 27 + 6 = 43 matches INV-A:73 (5/13/3) plus INV-B:278 (5/14/3). The 3.1 list has 10 rows and the 3.2 list has 27 rows (SPEC:81-125). The P1/P2/P3/P4 command counts (9+4 fixes; 15; 4; 3) add up to the table's 27 plus the 3.1 fixes.

## Whittaker attack summary (all five methodologies, against the contract invariants)
- Zero/Empty: empty `blocked_question` with `status: blocked` is allowed by the field list (SPEC:62) though AC-2.2 requires non-empty (SPEC:200); `artifacts: []` is defined; `--output` absent has no stated outcome for non-auto-deriving commands (Medium, in the table above).
- Divergence: the file-versus-directory split of `--output` (SPEC:62) at the boundary "a path with no extension" (F-01 family).
- Sentinel Collision: `blocked` doubles as a status and as a map to `--outcome failed` (SPEC:63); a legitimate "blocked on purpose" run is indistinguishable in Orca from a crash. This is stated behavior, so a note only.
- Sequence: retry reuses output (F-09, Medium); `worker_done` before the contract is written is not forbidden in order terms, though WC-5 says "report says" (note).
- Accumulation: Orca's circuit breaker counts failed `worker-start` attempts, not a worker's own `failed` (CAPS:80, SPEC:263); a blocked command retried by the coordinator accumulates no breaker count, so a loop of `blocked` is bounded only by the coordinator (note).

## Requirements and architecture assessment
- Decision (SPEC:13-45): the core choice, commands as units and Orca above, is supported by the inventories (CAPS:97-103 for the depth limit, INV-A:90 and INV-B:285-286 for coordinator-only commands) and the evidence gaps are stated honestly (SPEC:41-45). No finding against the decision.
- Traceability: each WC row cites inventory lines that match what I could check (WC-1 to CAPS:44-45; WC-3 to CAPS:58-64; WC-5 to CAPS:73,76; WC-7 to CAPS:159-161; WC-10 to CAPS:130; WC-12 to CAPS:66-67). I found no mis-cited CAPS or INV line. The cited source lines behind the inventories are UNVERIFIED here.
- Open decisions D1-D5 are self-contained with recommendations (SPEC:224-253); D5 and R1 agree.

## follow-up candidates
Medium findings F-03 to F-13 and minor notes N-1 to N-5 above. The session that ran the review is meant to ask the user once whether to open an issue for them; this sandboxed run has no user channel, so nothing was asked and nothing was created. The coordinator should ask.

## Reviser brief
Blocking finding ids: F-01, F-02. Rules for the reviser (restating the review loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium findings F-03 to F-13 and the minor notes alone, and do not award yourself a PASS.

Brief clause overridden: none. The brief asked only for a first whole-document review; it widened nothing and graded no minor finding as blocking.

verdict: FAIL

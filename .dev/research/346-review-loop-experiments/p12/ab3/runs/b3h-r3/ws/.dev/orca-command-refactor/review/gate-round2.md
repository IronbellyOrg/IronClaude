review: 2 of 3

# Re-review: orca-worker-contract-spec (spec-panel critique, focus requirements, architecture)

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review review/gate.md --baseline specs/history/spec-g.md` (RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`, gate loop re-review: the GATE prompt numbers it `review: 2 of 3`)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `92a25ab664b0803fb12bd23716793e4aba1f0dc0171d60f876c747679cfcf973`
- Baseline: `.dev/orca-command-refactor/specs/history/spec-g.md` (285 lines), sha256 `d7b701458ccab1292a94ee6f2c84881cfc91dbf20d522f329d407123b072388d`
- Prior report: `.dev/orca-command-refactor/review/gate.md` (`review: 1 of 3`, `verdict: FAIL`), sha256 `757ae09693a03381a2f43964f1b66521c22a6c7a5aec6f1b4c98360035783526`
- Reviewer model: claude-haiku-5-5
- Grading: FIRST-REVIEW grading check (blocking needs a sentence that holds with no further assumption; otherwise Medium)
- Result: 2 open blocking findings (GR-B1 open, deferred by the reviser; GR-B3 new), 1 prior blocking finding resolved (GR-B2), 3 Medium follow-up candidates, 2 notes. Edits: none.
- Citation convention: `spec:N` = line N of the candidate; `spec-g:N` = line N of the baseline; `INV-A:N` = `inventory/commands-a.md:N`; `INV-B:N` = `inventory/commands-b.md:N`; `CAPS:N` = `inventory/orca-capabilities.md:N`. All relative to `.dev/orca-command-refactor/`.

## Coverage

- Read in full: `command.md`, `README.md`, the RE-REVIEW / GATE prompt file, the prior report `review/gate.md`, the candidate (all 285 lines), and the baseline `specs/history/spec-g.md` (by `diff -w`; both files are 285 lines).
- Step 1 diff: `diff -w specs/history/spec-g.md specs/orca-worker-contract-spec.md` gives three hunks, at lines 64, 73 and 87. No other line changed.
- Inventory citations this review checked against the inventory files: `INV-A:55` (init-lite, "a marked report is overwritten on re-run"), `INV-A:62` (auggie-review chat-offer stall), `INV-B:49` and `INV-B:237-245` (troubleshoot: diagnosis never prompts, `--fix` offer is the only `[yes / no]`), `CAPS:46`, `CAPS:52`, `CAPS:116`, `CAPS:129-130`. Each matches the topic the candidate cites.
- Not checkable in this sandbox, so UNVERIFIED and not graded as wrong: `cmd/init-lite.md:32`, every `src/superclaude/...` path, every `sk/...` and `cmd/...` source line, `.dev/codegraph-migration/...`, and the F-xx finding ids.
- `~/.claude/agents/rf-qa.md` and the project `.claude/agents/rf-qa.md` are not in the sandbox (`home/.claude/` holds only `rules/`). The fix-cycle steps 1-5 of rf-qa therefore could not be applied, and the rules of the Review Loop section apply on their own, as the command allows.
- Not applicable: the brief has no standalone `--unattended` token, so `~/.claude/WORKER-CONTRACT.md` is not read and no unattended gate applies.
- Note on the prior report: `review/gate.md` records the candidate sha256 as `d7b70145...`, which is the current sha256 of the baseline file. The text gate.md quotes at spec:87 (init-lite "Re-run overwrites its marked report", "None") matches `spec-g:87`. So gate.md reviewed the pre-revision text, which is the baseline. This does not change any verdict.

## Step 1: evidence block

Roles, fixed by the brief and the command: CANDIDATE = `specs/orca-worker-contract-spec.md`; BASELINE = `specs/history/spec-g.md`; PRIOR = `review/gate.md`. The command is `diff -w BASELINE CANDIDATE`, so `<` lines are BASELINE and `>` lines are CANDIDATE.

BEFORE (baseline), lines starting `<`:

```text
| WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). The coordinator does not run two workers that write a fixed output path (cleanup-audit and index-repo until P1 adds their per-slug flag) in one worktree (F-01, WC-11). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

AFTER (candidate), lines starting `>`:

```text
| WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. A command that writes one fixed report path and has no resume flag (init-lite, GR-B1) must, under `--unattended`, refuse to overwrite an existing marked report and resolve as blocked (WC-2 c). Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, with `--unattended` only for a command that already accepts it in the phase being run (section 6 gives the phase; Phase 0 runs omit it, because the flag is first accepted in P1, and AC-0.4 checks those runs as they are) (GR-B2), and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). The coordinator does not run two workers that write a fixed output path (cleanup-audit and index-repo until P1 adds their per-slug flag) in one worktree (F-01, WC-11). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report, so a retry before P1 is unsafe (GR-B1) | Under `--unattended`, refuse to overwrite an existing marked report: write the contract as `blocked` and stop (WC-6, GR-B1) (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

Self-check (`grep -nF` of each quote, run 2026-11-10 in this sandbox): each AFTER line is found exactly once in the candidate; each BEFORE line is found exactly once in the baseline and zero times in the candidate. The roles are as stated above; no swap.

Candidate line numbers for the three changed lines: WC-6 = spec:64, §2.3 = spec:73, init-lite row = spec:87.

## Prior blocking findings

| id | status | basis |
|---|---|---|
| GR-B1 | **open** | The reviser deferred the fix to P1. The init-lite row says the refusal is "(P1)" (spec:87). The flag it depends on is first accepted in P1 (spec:159). Until then §3.1 says the ten ready commands "run as workers now" (spec:79), and init-lite is in that set (spec:87). The row itself says "a retry before P1 is unsafe" (spec:87). WC-6 (spec:64) still states, without a phase condition, that a retry worker "must not corrupt the first attempt's output". A deferred finding counts as open (command Review Loop step 5). |
| GR-B2 | **resolved** | §2.3 (spec:73) now says Phase 0 runs omit `--unattended`, gives the reason (the flag is first accepted in P1, spec:159), and points to AC-0.4. §3.1 brief columns (spec:83-92) and §7.2 step 1 (spec:180) now agree with it. The required fix in gate.md (spec-finding GR-B2, "state that P0 briefs omit it and why §2.3 is waived for P0") is met. A new defect in the P0 check is recorded below as GR-B3. |

## Findings on changed lines

### GR-B3 (requirements, blocking, origin=unchanged, quotes the changed line spec:73): the P0 acceptance check has no passing run

- Stated text, 7.2 step 3 (spec:182): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Stated text, AC-0.4 (spec:194): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
- Stated text, §2.3 (spec:73, changed): "Phase 0 runs omit it ... and AC-0.4 checks those runs as they are."
- Stated text, P0 (spec:158): P0 writes only `WORKER-CONTRACT.md` and "no command edits", so the WC-4 contract does not exist in P0.
- Stated text, troubleshoot's report today: `REPORT.md` (`report_path`) (spec:91; `INV-B:49`, `INV-B:242`).
- Grading sentence: an implementer who follows AC-0.4 and runs `/sc:troubleshoot "<real symptom>"` in P0 gets `report_path` REPORT.md from the worker (spec:91), so step 3's requirement "its report path is the WC-4 contract path" fails. Step 3 also requires the outcome to match "the contract's status", and no contract exists in P0. AC-0.4 nevertheless says steps 1-3 must pass. That is wrong because the P0 acceptance check cannot pass for any run, and spec:194 says a failure here "reopens section 1". Two stated texts contradict each other, so this is blocking. (The step 4 exemption covers only step 4.)
- Origin: the text is identical in the baseline (`spec-g:182`, `spec-g:194`), so the defect is older than this revision. It is recorded now because the changed §2.3 clause (spec:73) names AC-0.4 as the P0 check that the revision relies on. Command rule: a newly discovered severe defect is recorded even if older, with its source.
- Required fix (for the reviser, not made here): in 7.2 step 3, state that before P1 the report path and status are the command's own report (for example `REPORT.md`), or exempt the contract-path and WC-5 contract clauses of step 3 for P0 in AC-0.4, as step 4 is exempted. Workflow (spec:92, which already writes `return-contract.yaml`) and adversarial (spec:83, "filename not fixed") would need the same wording, so one rule for P0 is enough.

### MD-1 (requirements, Medium, origin=changed, spec:64): the new WC-6 clause defines a class that only one command is named for

- Stated text, spec:64: "A command that writes one fixed report path and has no resume flag (init-lite, GR-B1) must, under `--unattended`, refuse to overwrite an existing marked report and resolve as blocked (WC-2 c)."
- Stated text, §3.2 rows for other commands that take one fixed output path and have no resume flag: analyze "add `--output`; contract plus the report | fresh dir | none" (spec:99); spec-panel "add `--output`; contract | fresh dir | none" (spec:120; `--output` is file-valued per command.md Usage, and `INV-B:182` says no such flag exists today). Their rows add no refusal.
- Grading sentence: an implementer who reads the class in spec:64 literally must decide, for analyze, spec-panel and the other "add `--output`" rows, whether a re-run with the same `--output` path is "fixed" (refuse) or "fresh dir" (allowed). The text does not settle it, so the result is a guess. Medium, because the choice is a missing rule, not a stated text that does harm.
- Suggested fix (not made here): name the class by the §3 rows, or say that a brief's new path counts as a fresh directory.

### MD-2 (requirements, Medium, origin=changed, spec:64 and spec:87): the blocked report location is not the same in the two changed lines

- Stated text, spec:64: "resolve as blocked (WC-2 c)". WC-2 (c) at spec:60 says "the command writes its report with `status: blocked` and the exact question, and stops."
- Stated text, spec:87: "write the contract as `blocked` and stop".
- Grading sentence: under `--unattended` the marked report is not overwritten, so the command must write the blocked status somewhere. spec:64 says "its report" (the marked report, which it may not overwrite) and spec:87 says "the contract" (`return-contract.yaml`, which WC-4 names at spec:62). An implementer picks one. Medium, because the two readings differ only in file name.

### MD-3 (requirements, Medium, origin=changed, spec:64 and spec:87): the guard's sentinel and its non-marked case are not stated

- Stated text: the refusal applies only to "an existing marked report" (spec:64, spec:87). The spec never says what the marker is, or what happens when a file exists at `--output` without the marker.
- Grading sentence: an implementer cannot tell whether an unmarked file at the path is refused, overwritten, or handled by the standalone behaviour, which the spec does not describe (`cmd/init-lite.md:32` is UNVERIFIED here). This is a missing restriction, so Medium. It is a data-loss risk in principle, so the reviser should close it, but the stated text does not itself cause the loss.

### Notes (not graded)

- N-1: the revision cites review ids (GR-B1, GR-B2) inside normative text at spec:64, :73 and :87. The reviser was asked to cite ids, so this is compliant, but these ids will be stale once the review closes. Consider removing them after the loop.
- N-2: spec:73 says "section 6 gives the phase". §6 (spec:153-162) does list the phase per command set, and P1 (spec:159) gives the flag acceptance that §2.3 uses. No inconsistency found on this point.

## Guard Condition Boundary Table (guards on changed lines only)

Guards on changed lines: G1 is the init-lite overwrite refusal (spec:64, spec:87). G2 is the flag-acceptance condition in §2.3 (spec:73).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 init-lite refusal | spec:64, spec:87 | Zero/Empty (no file at `--output`) | no file | false | Not refused. The spec does not say so, but "refuse to overwrite an existing" implies the first run writes. | OK |
| G1 init-lite refusal | spec:64, spec:87 | One/Minimal (existing file without the marker) | file, no marker | false | Not stated (see MD-3) | GAP (Medium, MD-3) |
| G1 init-lite refusal | spec:64, spec:87 | Typical (existing marked report, `--unattended`) | marked report | true | Refuse; the blocked status location differs between the two lines (see MD-2) | GAP (Medium, MD-2) |
| G1 init-lite refusal | spec:64, spec:87 | Maximum/Overflow | n/a | n/a | Not applicable: the guard tests presence and marker of one file, with no count or capacity. | OK |
| G1 init-lite refusal | spec:64, spec:87 | Sentinel Value Match (marker text) | marker present | true | The marker text is not defined in the spec (see MD-3) | GAP (Medium, MD-3) |
| G1 init-lite refusal | spec:64, spec:87 | Legitimate Edge Case (re-run after a blocked contract) | contract `blocked` in output dir | not applicable | The contract is a different file from the marked report, so the refusal does not apply; no stated wrong outcome. | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:159 | Zero/Empty (no flag in the brief, Phase 0) | no flag | false | Runs as today; spec:158 and spec:73 agree. | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:159 | One/Minimal (P1 command with the flag) | flag, P1 | true | Accepted; no-op where no gate (spec:159) | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:159 | Typical (P1 gate-command, e.g. `tdd`) | flag, P1 | true | Accepted as a no-op in P1 per spec:159 | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:159 | Maximum/Overflow | n/a | n/a | Not applicable: a presence flag, no count. | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:112, spec:159 | Sentinel Value Match (`load`, excluded from the flag) | flag, `load` | false | `load` is not a Task (spec:112) and is excluded from the flag (spec:159), so the brief omits it. | OK |
| G2 `--unattended` only for accepting commands | spec:73, spec:159 | Legitimate Edge Case (P0 run of a command that will hit a gate) | no flag, P0 | false | Runs as today. GR-B3 (blocking) concerns the P0 check, not this guard. | OK |

Guard-table completeness (FR-10): every guard on a changed line has its input-class rows listed above, and each class not listed is marked not applicable with a reason. FR-8: three GAP cells, each a Medium finding (MD-2, MD-3). FR-9: no blank Specified Behavior cell.

## Medium and minor findings (follow-up candidates; none fails a review by itself)

- MD-1, MD-2, MD-3 (above).
- N-1, N-2 (above).
- Not re-graded here: gate.md M-1 to M-12 and N-1 to N-4 sit on unchanged lines and are not quoted by any changed line, so they are outside this re-review's scope. They remain in `review/gate.md`. The coordinator may ask the user once whether to open issues for them.

## Verdict summary

- GR-B1: open (deferred to P1; still a blocking finding).
- GR-B2: resolved.
- GR-B3: new, blocking.
- This run is the gate loop's re-review. Under the GATE prompt, a FAIL escalates to the user with the open blocking findings. No second gate loop and no further review is started by this run. The stall rule does not apply here, since it is judged on the gate review.

## Reviser brief

Blocking ids: GR-B1, GR-B3.

Restated per the review loop, step 6: revise only the text that GR-B1 and GR-B3 name; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (MD-1 to MD-3, N-1, N-2) are not in this brief and must not be revised under it.

Brief clauses overridden: none.

verdict: FAIL

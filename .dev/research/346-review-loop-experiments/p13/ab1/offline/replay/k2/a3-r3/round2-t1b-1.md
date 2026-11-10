review: 2 of 3

# Spec-panel review, round 2 (re-review): orca-worker-contract-spec.md

- mode: critique; focus: requirements, architecture; format: markdown report grouped by analysis bucket
- command line: `--re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- roles (fixed by the RE-REVIEW prompt table, not inferred): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`
- candidate sha256: `0af4c9147b1078d164edae3da1719df0954c532ee06138e07f894bc91e1ab096` (58196 bytes, 285 lines)
- baseline sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes, 285 lines); it equals the candidate hash recorded in PRIOR (`review/round1.md:7`), so the baseline is the text round 1 reviewed
- prior report sha256: `b1c0821c97063fc6462b1c6fff75b36a7587e5ee5cb5a4c1e009adc0f6c571db`; its header is `review: 1 of 3` (`review/round1.md:1`), its verdict is `FAIL` (`review/round1.md:220`), so N = 1 + 1 = 2 and the cap check (a prior `review: 3` with FAIL) does not apply
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before writing), with the re-review core in order: roles, Step 1 evidence block, review number, self-check
- Improve step: skipped (`--re-review` ignores `--iterations` and writes no revised specification); the candidate was not edited; this file is the only file written
- re-check procedure: `~/.claude/agents/rf-qa.md` and the project `.claude/agents/rf-qa.md` are not present in the sandbox (the sandbox holds no `agents` folder), so steps 1-5 of its Fix Cycle process were not read; the Review Loop rules of the command, which stand alone, were applied instead
- citation keys: `SPEC` = candidate; `BASE` = baseline; `ROUND1` = prior report; `REV1` = `.dev/orca-command-refactor/review/revise1.md`; `INV-A` / `INV-B` / `CAPS` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md` / `orca-capabilities.md`; `README` = `.dev/orca-command-refactor/README.md`. A cited repo file that is not in the workspace (`src/superclaude/...`, `CLAUDE.md:NN`) is UNVERIFIED unless an inventory line repeats it.

## Coverage
Covered: the README; the whole of PRIOR (221 lines); `diff -w BASE SPEC` (7 changed lines, 14 `<`/`>` lines; the plain `diff` gives the same 14, so no whitespace-only change exists); the self-check (all 14 quoted lines found, 7 `<` lines in BASE and 7 `>` lines in SPEC, none swapped); the full candidate (285 lines) read for every text that depends on a changed line (SPEC:73, 76, 79, 84, 87, 112, 139, 149, 158-162, 180-183, 194-198, 240); the inventory lines that decide whether the revised AC-0.4 can pass (INV-B:237-245 troubleshoot, INV-B:265-276 workflow, INV-A:35 and INV-A:58-66 adversarial); the byte accounting in REV1 (recomputed below); the 10 / 27 / 6 row counts.
Not covered / UNVERIFIED: the source files under `src/superclaude/` and `CLAUDE.md` lines the spec cites (not in the workspace); `CAPS` (the changed lines cite no CAPS line, and no CAPS line was needed to decide a changed line); the Orca binary; the live runs AC-0.4 describes (none was run). No finding on text outside the changed lines and the prior blockers was searched for beyond the dependency read above.

## Step 1: evidence block
Diff run: `diff -w BASELINE CANDIDATE` with BASELINE = `specs/history/spec-v1.md` and CANDIDATE = `specs/orca-worker-contract-spec.md`. Changed hunks: 76, 79, 112, 159, 194-196 (7 lines changed, 0 added, 0 removed as lines). Quoted verbatim.

### BEFORE (baseline)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except `/sc:load` also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. Phase 1 also adds `--unattended` and the `## Unattended mode` section to each of these commands, besides the small fixes in the last column.
| load | no gate | none; exempt from the `## Unattended mode` section, AC-1.1 and AC-1.2 (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `/sc:load` (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-2 and 5-7 pass; step 3 passes with exactly one `worker_done`, an `--outcome` that follows WC-5 from the command's own report (`failed` if none exists) and the command's existing report file as its report path; step 4 is only `test -s` on that file, since the contract arrives in P1; the P0 briefs omit `--unattended`. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command except `/sc:load` with `--unattended --output <dir>` | all steps pass |
```

### Self-check (before the verdict)
`grep -nF` of each `>` line (without its `>`) in the candidate and each `<` line (without its `<`) in the baseline: 14 of 14 found, 0 missing, so no role swap. Byte accounting of REV1 recomputed from a character-level diff of BASE against SPEC: lines 76, 112, 159, 195, 196 add 18, 65, 18, 18, 18 bytes (F1: 137 added, 0 deleted); line 79 adds 87 and deletes 11 (F2); line 194 adds 223 and deletes 3 (F3); total 447 added, 14 deleted, net +433 = 58196 - 57763. This matches `REV1` (the byte table, `review/revise1.md:14-21`).

## Prior blocking findings

| Id | Prior status (ROUND1) | Now | Reason, compared with the AFTER text only |
|---|---|---|---|
| F1 | blocking (`review/round1.md:38`) | resolved | The defect was that AC-1.1 and AC-1.2 required an `## Unattended mode` section and a live `--unattended --output` run for `/sc:load`, which the spec says gets no report and is not its own Task (SPEC:112, SPEC:265, SPEC:139). All five texts that carried the requirement now exempt it: SPEC:76 ("Every changed command except `/sc:load` also gains..."), SPEC:112 (load row: "exempt from the `## Unattended mode` section, AC-1.1 and AC-1.2"), SPEC:159 ("every command in sections 3.1 and 3.2 except `/sc:load`"), SPEC:195 ("every command in sections 3.1-3.2 except `/sc:load`"), SPEC:196 ("each P1 command except `/sc:load`"). `/sc:load` keeps its P1 usage-line fix (SPEC:112 Phase cell, SPEC:159 "load (usage line only)"), which SA-4 allows (SPEC:149 names "load usage line"). No remaining text asks load for a section, a report or a live run. P1 can pass, so the later phases (SPEC:154) are not blocked by it. |
| F2 | blocking (`review/round1.md:46`) | resolved | The defect was SPEC:79 "The only command changes are the small fixes in the last column" against SPEC:76, SPEC:159 and AC-1.1, which add the flag and section to every 3.1 command. SPEC:79 now says "Phase 1 also adds `--unattended` and the `## Unattended mode` section to each of these commands, besides the small fixes in the last column." An implementer now edits `brainstorm` and `init-lite` (small fix "None", SPEC:84, SPEC:87) in P1 and AC-1.1 passes on them. The "until Phase 1 adds the contract" half of the same line (SPEC:79) is consistent with SPEC:84 for brainstorm, which already writes a contract; that remark was not part of the blocking text (`review/round1.md:48`). |
| F3 | blocking (`review/round1.md:52`) | resolved | The defect was AC-0.4 requiring 7.2 step 3 in Phase 0 although step 3's conditions (contract `status`, WC-4 path) and step 1's `--unattended` do not exist before Phase 1. SPEC:194 now reads: steps 1-2 and 5-7 pass; step 3 passes with exactly one `worker_done`, an `--outcome` that follows WC-5 from the command's own report (`failed` if none exists) and the command's existing report file as its report path; step 4 is only `test -s` on that file; the P0 briefs omit `--unattended`. Each part can hold for the three smoke commands: the inventories call troubleshoot ready without `--fix` ("diagnosis never prompts and REPORT.md is the report path", INV-B:245), workflow ready with `--handoff none` ("no prompts ... `return-contract.yaml` is a direct `--report-path`", INV-B:275) and adversarial ready with `--output` (INV-A:35); WC-5's "`failed` ... or no report exists" (SPEC:63) is the rule the new text points to; P0 makes no command edit (SPEC:158), so omitting `--unattended` matches what exists. SPEC:182-183 (steps 3 and 4 as written) still apply in P1-P4 and are not contradicted. |

No prior blocking finding is `open` or `regressed`. ROUND1 marked none of its findings resolved, so there was nothing to regress.

=== REQUIREMENTS ANALYSIS ===

No new blocking finding. The two findings below are on changed lines or quote one; both need a guess about which reading an implementer picks, so both are Medium.

### R2-1. Medium (MAJOR by label). P1 "Commands" column omits six ready commands that SPEC:79 and AC-1.1 now require P1 to edit
- Expert: Wiegers. origin=unchanged, but it quotes the changed line it depends on: SPEC:79 "Phase 1 also adds `--unattended` and the `## Unattended mode` section to each of these commands".
- Grading: SPEC:159 states the Scope as "every command in sections 3.1 and 3.2 except `/sc:load`" and AC-1.1 (SPEC:195) tests that scope, so an implementer who follows the stated scope edits all of them. Only the Commands column of the same row names a shorter list (analyze, build, business-panel, design, document, explain, index, test, load; fixes to adversarial, cleanup-audit, index-repo, workflow: 13 names, 12 without load), which leaves brainstorm, init-lite, reflect, release-split, tdd and troubleshoot in neither list. Building the wrong set needs the guess that the column overrides the Scope sentence, so Medium.
- Same ambiguity makes "each P1 command" in AC-1.2 (SPEC:196) unclear: the Commands column (12 non-load commands) or all 36 non-load commands of 3.1-3.2.
- Recommendation: add one clause to SPEC:159 or SPEC:196 saying which reading holds.
- Priority: Medium.

### R2-2. Medium. AC-0.4 does not say which existing file is the report path for `/sc:adversarial`
- Expert: Adzic. origin=changed (SPEC:194).
- Grading: step 3 now requires "the command's existing report file as its report path". For troubleshoot that is `REPORT.md` (INV-B:245) and for workflow the generated package contract (INV-B:275), but for adversarial the output is a merged document plus six artifacts and the contract has no fixed name (INV-A:35, INV-A:60-61; SPEC:83 "contract, but filename not fixed"). The worker can pass any real file and the step passes, so no wrong outcome follows without a guess that the check is meant to be stricter.
- Recommendation: add "(for adversarial, the merged output file)" or accept any existing contract.
- Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

No new blocking finding. Dependencies of the changed lines read: the 3.1 versus 3.2 split and the 10 / 27 / 6 counts (rows recounted at SPEC:83-92 = 10, SPEC:99-125 = 27, SPEC:132-137 = 6; 43 in total, as in ROUND1's quantity check); SA-3 and SA-4 (SPEC:148-149) with the new line 79 (the P1 edits stay additive: a section and a flag); the P0 to P1 gate (SPEC:154, SPEC:158) with the revised AC-0.4.

- **Fowler / Newman**: the revision keeps one contract file and a phase order that still holds. F12 of ROUND1 (a flag accepted in P1 while its gates convert in P2-P4) stays Medium. SPEC:79 extends it from the 3.2 commands to the ten 3.1 commands (for example tdd and troubleshoot receive the flag and section in P1 while their gate lines convert in P2, SPEC:90-91, SPEC:160). It needs the guess that the P1 section is written before the gate resolutions exist, because SPEC:52 says the section lists the command's gate resolutions; Medium, already in the follow-up list as F12.
- **Nygard / Hohpe**: nothing in the changed lines touches liveness, nesting or propagation (F11, F13-F16 stay as ROUND1 graded them).

=== ADVERSARIAL ANALYSIS (Whittaker), changed lines and prior blockers only ===

Attacks tried against the changed lines (the five methodologies, one pass each):
- Zero/Empty on AC-0.4 step 3: no report exists, so `--outcome failed` is specified (SPEC:194, SPEC:63); handled. An empty or unparseable report is not covered (ROUND1 N6, unchanged). `test -s` on an empty file fails step 4 as intended.
- Divergence on the `except /sc:load` guard: a command that is both in 3.1-3.2 and "no gate" gets the section anyway (SPEC:159 "a no-op where a command has no gate"); load differs only by name. No branch applies twice. Handled.
- Sentinel Collision on the name `load`: the exemption keys on the command name `/sc:load`; no other command row in SPEC:83-125 has that name (the word "loading" appears only in prose, SPEC:102, SPEC:278). Handled.
- Sequence on P0 then P1: the P0 briefs omit `--unattended` (SPEC:194) and P1 adds it (SPEC:79, SPEC:159); a P0 brief written from section 2.3 (SPEC:73 "including `--unattended`") would pass a flag that does not exist yet. The specific P0 text overrides the general one, but SPEC:73 and SPEC:180 do not say "from P1". Note N-R2-1 below; not blocking because the P0 text is explicit.
- Accumulation: none of the changed lines carries a counter; the counts 10 / 27 / 6 are unchanged and conserve (43).

I cannot break any changed line to a stated-text contradiction or an unpassable acceptance criterion, so no Whittaker finding is blocking.

## Guard Condition Boundary Table (guards on changed lines only)
Guards found on changed lines: G1 the `/sc:load` exemption (SPEC:76, 112, 159, 195, 196); G2 the P0 outcome rule "`failed` if none exists" (SPEC:194 with SPEC:63); G3 "exactly one `worker_done`" (SPEC:194 with SPEC:182); G4 "P0 briefs omit `--unattended`" (SPEC:194 with SPEC:73); G5 step 4 `test -s` (SPEC:194).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 load exemption | SPEC:195 | Typical | any command in 3.1-3.2 other than load | section required | AC-1.1 asserts the section | OK |
| G1 load exemption | SPEC:112, SPEC:159 | Legitimate Edge Case | `/sc:load` itself | exempt | no section, no live run; usage-line fix kept in P1 | OK |
| G1 load exemption | SPEC:196 | Legitimate Edge Case | "each P1 command" (12 non-load names in the Commands column vs all 36 non-load commands of 3.1-3.2) | undefined | scope not pinned (R2-1) | GAP (R2-1, Medium) |
| G2 failed if none exists | SPEC:194, SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G2 failed if none exists | SPEC:194, SPEC:63 | Typical | report exists, command succeeded | false | `--outcome succeeded`, per WC-5 | OK |
| G2 failed if none exists | SPEC:63 | Legitimate Edge Case | report says `partial` or audit verdict FAIL | false | `succeeded`, status in the body | OK |
| G2 failed if none exists | SPEC:63 | One/Minimal | report file present but empty or unparseable | undefined | none stated | GAP (minor, ROUND1 N6, unchanged) |
| G3 exactly one worker_done | SPEC:194, SPEC:182 | Zero/Empty | none arrives within `--timeout-ms 900000` | step 3 not met | the step fails; the coordinator's stall policy is not stated | GAP (F14, Medium, unchanged) |
| G3 exactly one worker_done | SPEC:182 | Maximum/Overflow | two `worker_done` | step 3 not met | the step fails | OK |
| G4 omit `--unattended` | SPEC:194 | Typical | P0 brief without the flag | true | commands run as they are today (SPEC:158) | OK |
| G4 omit `--unattended` | SPEC:73, SPEC:180 | Legitimate Edge Case | brief built from section 2.3 ("including `--unattended`") | undefined | precedence not stated | GAP (minor, N-R2-1) |
| G5 `test -s` | SPEC:194 | Zero/Empty | empty report file | false | step 4 fails | OK |
| G5 `test -s` | SPEC:194 | Typical | non-empty existing report | true | step 4 passes | OK |
| G5 `test -s` | SPEC:194 | Legitimate Edge Case | adversarial, no fixed report name | file chosen by the worker | any existing file passes | GAP (R2-2, Medium) |

Omitted classes: G1 Zero/Empty, One/Minimal, Maximum and Sentinel (a name match has no such values; a name collision was attacked above and none exists); G2 Maximum and Sentinel (a file exists or not); G3 One/Minimal and Typical are the pass case (one `worker_done`); G4 Zero/Empty, One/Minimal, Maximum and Sentinel (a flag is in the brief or not); G5 One/Minimal and Maximum and Sentinel (a size test has no such class). The table is complete for the guards on changed lines (FR-10). Every GAP is graded Medium or minor because none names a wrong outcome that needs no further assumption (FR-8, FR-9 grading); a guard on an unchanged line is out of scope in a re-review.

## Quantity check (Pipeline Dimensional Analysis)
Not triggered as a data pipeline. The one count flow is the command classification, which the revision did not change: 10 ready + 27 needing a change + 6 coordinator-only = 43 (SPEC:76; rows counted at SPEC:83-92, SPEC:99-125, SPEC:132-137). The `/sc:load` exemption removes load from the AC-1.1 and AC-1.2 sets, not from the 27; the count of commands that need the section is therefore 36 non-load commands in 3.1-3.2 (10 + 26), not 37. No mismatch, because no text states a count of sectioned commands.

## Quality assessment (0-10)
Clarity 8; Completeness 7; Testability 8 (was 6: AC-0.4, AC-1.1 and AC-1.2 can now pass); Consistency 7 (was 6: F1 and F2 text contradictions gone; R2-1 and F12 remain). Overall 7.5.

## Notes (minor, never fail the review)
- N-R2-1. SPEC:73 and SPEC:180 say the brief carries the command line "including `--unattended`"; only AC-0.4 (SPEC:194) says the P0 briefs omit it. Add "from Phase 1" to SPEC:73 so the two agree without relying on precedence. origin=changed (SPEC:194 depends on SPEC:73).
- N-R2-2. SPEC:112 says "(see note)" for the load exemption; the note is SPEC:139 and SPEC:265, not marked as such. origin=unchanged.
- Carried from ROUND1 and unchanged: N1-N6 (`review/round1.md:194-200`).

## Follow-up candidates
These are Medium and minor findings. They do not fail the review and do not appear in the Reviser brief. Issue offer: not asked, because this review ran as a worker with no person channel (Review Loop 3: an unattended run only records the list); no issue was created.

- Medium, new this round: R2-1 (P1 Commands column vs Scope), R2-2 (adversarial report path in AC-0.4).
- Medium, carried unchanged and not re-graded (their lines were not changed): F4, F5, F6, F7, F8, F9, F10, F11, F12 (SPEC:79 now widens it to the 3.1 commands), F13, F14, F15, F16, F17, F18, F19 (`review/round1.md:205`).
- Minor: N-R2-1, N-R2-2, N1-N6.

Brief clauses that overrode the review's default scope: none. The brief asked for the RE-REVIEW prompt, critique mode, focus requirements and architecture, with values candidate, baseline and prior as used above, and no edit outside this file; none of that widens the scope past the changed lines and the prior blocking findings or grades a minor finding as blocking.

Coverage line: scoped PASS: changed lines + prior blockers.

## Reviser brief
Blocking finding ids: none (F1, F2 and F3 are resolved; no new blocking finding). No revision is requested.
Restated rules, for any later reviser (the reviser reads this report, not the command):
- Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table row cites its finding id.
- Prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (R2-1, R2-2, F4-F19, N-R2-1, N-R2-2, N1-N6) alone; do not award yourself a PASS.
- Whole-document assurance needs a separate, labelled first review whose blockers are escalated; it never starts a fourth review.

verdict: PASS


## Findings block

```findings-v1
{"prior": "L1", "status": "resolved"}
{"prior": "L2", "status": "resolved"}
{"prior": "L3", "status": "resolved"}
```

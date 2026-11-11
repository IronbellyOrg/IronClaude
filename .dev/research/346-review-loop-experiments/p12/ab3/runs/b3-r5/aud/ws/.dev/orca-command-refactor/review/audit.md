review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `7dee641ad4c0ea491b648c4d2ff91374c68f0b6c2b89647e79c56e099f02c9e8`
- baseline: not given (first review of the full document)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`
- coverage: whole document (spec lines 1-285), README (lines 1-37), and the three inventories read in part (only the lines cited below). The inventories are the only checkable evidence. Every citation to a path outside `.dev/orca-command-refactor/` (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `pyproject.toml`, `Makefile`) is UNVERIFIED because no such file is in the workspace. Not covered: re-reading the 340 citations; the Orca guide quotes behind `CAPS:` lines (taken as quoted).
- candidate edited: no.

## Method notes
- Count conservation checked. 10 ready + 27 needs-change + 6 coordinator-only = 43 matches `INV-A:3` (21 commands: 5 ready, 13 needs-change, 3 coordinator-only, `commands-a.md:75,87`) plus `INV-B:3` (22 commands: `commands-b.md:278`, 5/14/3). Rows of spec 3.2 (lines 99-125) number 27. Phase membership in section 6 (lines 159-162) sums to P1 9, P2 11 + 4 ready, P3 4, P4 3 = 31 phase slots over 27 + 4 commands, no duplicates.
- Spot-checked CAPS citations: `CAPS:44-47,52,64,73,76,79,80,98,103,116,129,130,150,155,158-161,178-188` match what the spec says they say. README citations at spec lines 5, 23, 67, 133 and 222 (`README.md:11-17,12,31,30`) match `README.md` lines 11-17, 12, 31, 30.

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, BLOCKING] Section 3.1 and AC-0.4 say Phase 1 adds the contract to the ready commands; section 6 says it does not, so two acceptance checks cannot pass
Experts: Wiegers (lead), Adzic, Whittaker (Sequence Attack). Priority High.

Grading sentence: an implementer who follows the stated text as written builds a Phase 1 that adds `return-contract.yaml` only to the commands named in the P1 row, and then the P0 and P2 acceptance checks that require a contract for the other ready commands cannot pass, because two stated texts contradict each other.

Stated texts that contradict:
- Spec line 79: the ready commands' worker "reports the named file until Phase 1 adds the contract".
- Spec line 194 (AC-0.4): `/sc:troubleshoot`, `/sc:workflow`, `/sc:adversarial` run as P0 smoke tests, "step 4 uses the command's existing report file, since the contract arrives in P1".
- Spec line 159 (P1 row): the contract is added only for "every command named in this row's Commands column" (analyze, build, business-panel, design, document, explain, index, test, load) plus "fixes to adversarial, cleanup-audit, index-repo, workflow". troubleshoot, tdd, release-split, init-lite are in no P1 list. The P2 row (line 160) says only "Each default-on gate resolves per its section 3 row"; the tdd and troubleshoot rows (lines 90-91) name no contract-writing change.
- Inventory: the contract does not exist today for these commands. `INV-A:55` (init-lite: report only), `INV-A:53` (index-repo: `PROJECT_INDEX.md` only), `commands-b.md:37` (release-split: `release-split-report.md` only), `commands-b.md:47` (tdd: the TDD file only), `commands-b.md:242` (troubleshoot: `return-contract.yaml` "only when `--caller task-unified`").
- Spec lines 87 and 90 nevertheless state "contract in the parent directory of that file" for init-lite and tdd as if it already exists, and WC-4 (line 62) requires the contract "on every outcome" in unattended mode.

Concrete wrong outcomes, with state trace:
1. AC-2.2 (line 200) runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked` with a non-empty `blocked_question`" in the file's parent directory. State before: Phase 1 done, tdd untouched by P1, the P2 tdd row only turns the clarification prompt into "blocked". State after: no contract-writing step was specified for tdd in any phase, so no file exists and AC-2.2 fails. P3 cannot start (line 154).
2. AC-0.4 step 3 (line 182) passes only if "its report path is the contract path computed from section 3 (WC-4)" and "its `--outcome` matches the contract's `status`". For `/sc:troubleshoot` the section 3 Report column says `REPORT.md` and no contract exists in P0 or ever in P1. Step 3 is listed among the steps that must pass (line 194), so the P0 gate that "reopens section 1" on failure cannot be passed for troubleshoot.
3. init-lite, index-repo, release-split and tdd (WC-4: contract on every outcome) never get a contract in P1-P4, though AC-1.2 and the 7.2 live check (line 183) assert one.

Recommendation: either (a) add the five commands (init-lite, index-repo, release-split, tdd, troubleshoot) to a named phase row with an explicit "write the contract" change, or (b) narrow WC-4, line 79 and line 194 to say that those commands report their existing file and that steps 3-4 compare against it. Also make lines 87 and 90 say "the contract this phase adds" rather than implying it exists. Cite F-1 on each edit.

## === ARCHITECTURE ANALYSIS ===

(No blocking architecture finding. The decision itself, Orca on top and commands as units of work, is stated with its rejected alternative and its limits at lines 13-45 and is internally consistent with sections 4, 5 and 8.)

## Guard Condition Boundary Table
Guards identified in the spec. Classes left out are named with a reason in the last block. Every row is complete; the table is therefore not blocking synthesis (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | spec line 51, D1 (line 227) | Zero/Empty | flag absent | false | SA-1: today's behavior (line 146) | OK |
| `--unattended` switch | line 51 | Legitimate Edge Case | flag present on a command with no `## Unattended mode` section (brainstorm, init-lite, index-repo, cleanup-audit are in no phase that adds it; line 83-87, 159) | undefined | 2.3 (line 73) says the brief carries "`--unattended` and every flag section 3 lists" for every command; section 3.1 "Brief must pass" lists no `--unattended` for those four | GAP |
| gate resolves (WC-2 a/b/c) | line 60 | Typical | gate with documented default | true | per-row resolution, section 3 | OK |
| WC-2 (c) blocked | line 60 | Legitimate Edge Case | blocked and worker holds a preamble | true | WC-3: may `ask` once (line 61) | OK |
| WC-2 (c) blocked | line 60 | Legitimate Edge Case | blocked and no preamble (a person's plain session with `--unattended`) | true | contract `status: blocked`, stop | OK |
| outcome mapping | WC-5, line 63 | Typical | status `blocked` or `failed` or no report | true | `--outcome failed` | OK |
| outcome mapping | line 63 | Legitimate Edge Case | `partial` | false | `--outcome succeeded`, body states `partial` | OK |
| outcome mapping | line 63 | Zero/Empty | contract file exists but empty or unparseable | undefined | not specified (only "no report exists" is covered) | GAP (Medium, M-4) |
| contract path rule | WC-4, line 62 | Typical | `--output` is a directory | true | contract in that directory | OK |
| contract path rule | line 62 | Legitimate Edge Case | `--output` is a file | true | parent directory of the file | OK |
| contract path rule | line 62 | Legitimate Edge Case | row says only "add `--output`" (analyze, build, design, index, test, document, explain, spec-panel, lines 99-125) | undefined | whether the new flag is a file or a directory is not stated, so the path is not computable | GAP (Medium, M-1) |
| contract path rule | line 62 | Zero/Empty | `--output` omitted under `--unattended` | true | not stated for most rows; WC-4 says "the directory passed as `--output`" | GAP (Medium, M-1) |
| wait splitting WC-10 | line 68 | Typical | single tool call 3 minutes | false | no change | OK |
| wait splitting WC-10 | line 68 | Maximum/Overflow | 5 minutes exactly (eval 3600 s) | true | split into waits of at most 4 minutes | OK |
| wait splitting WC-10 | line 68 | Legitimate Edge Case | wait of 4 to 5 minutes | false | allowed by "longer than 5 minutes" in line 68, but "at most 4 minutes" in the same sentence; cadence margin is argued at line 266 | OK (reading is consistent: split only above 5, target 4) |
| nesting depth | R1, line 33; D5 | Sentinel Value Match | depth = 1 | true | refuse `worker-start`; WC-8 forbids the call | OK |
| nesting depth | D5 | Legitimate Edge Case | user raises depth above 1 | false | spec states non-goal 2 (line 214) and D5 (b) says it breaks R1; WC-8 still forbids | OK |
| readiness limit | WC-1, line 59 | Maximum/Overflow | fallback above about 45 s (cited `EVIDENCE.md:45,56`, UNVERIFIED) | true | fails readiness; spec says "well inside" the 60 s limit but gives no numeric ceiling | GAP (Medium, M-5) |
| `check` result | WC-12, line 70 | Legitimate Edge Case | `consumer_fenced` | true | stop, no `worker_done` | OK |
| `ask` timeout | WC-3, line 61 | Legitimate Edge Case | timeout | true | resume the same message ID; default timeout UNVERIFIED (item 10) | OK |
| confidence guard (task) | line 121 | Maximum/Overflow | exactly 0.70 | boundary | row says "below 0.70" resolves as blocked; 0.70 itself proceeds | OK |
| `--monitor 1` guard | line 114 | Legitimate Edge Case | `--monitor 1` under `--unattended` | true | refused | OK |
| `--mode socratic` guard | line 102 | Legitimate Edge Case | socratic under `--unattended` | true | refused (wait behavior UNVERIFIED but refused anyway) | OK |

Classes left out: One/Minimal for the `--unattended` switch (a boolean has no minimal case distinct from present); Sentinel Value Match for the outcome mapping (the four statuses are a closed set, assertion at line 183).

## Whittaker adversarial probe (state traces)

### W-1 Divergence attack, `--unattended` on a command that does not define it (same root as the GAP row above, graded Medium M-3)
I can break this specification by **Divergence Attack**. The invariant at **section 2.3 / section 6 P1 row** fails when **the coordinator writes `--unattended` into the command line of brainstorm, init-lite, index-repo or cleanup-audit**. Concrete attack: before, P1 done; brief = `/sc:brainstorm "x" --unattended --output d` (section 2.3 demands `--unattended`); the P1 row accepts the flag only for the commands in its Commands column (line 159) and the brainstorm, init-lite rows say "Small fix: None" (lines 84, 87). After: the flag is unknown or silently ignored and the spec does not say which. Because the reader must guess, this is Medium (M-3).

### W-2 Sequence attack, phase gates
Phase 4 "waits for answers to D2-D4" (line 154), while P2 rows already encode D4(a) (auggie-review posting only with explicit `--post-pr`, task commit/push refused unless authorized, lines 100, 121). Line 225 says phases 0-3 "can proceed on the recommendations", which resolves it. No defect.

### W-3 Accumulation attack, test file growth
AC-2.1 requires "one assertion per gate listed in the section 3 row" in `test_worker_contract.py`; the file is written in P0 (line 158) and edited in each phase. No cap is needed. No defect.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)
Triggered: classification funnel with count changes and a contract-coverage stage.

```text
[Source: 43 commands (21 INV-A + 22 INV-B)] --> [Classify] --> [10 ready | 27 needs-change | 6 coordinator-only]
   [Coordinator-only: 6] --> no worker, no --unattended (section 4)
   [Dispatchable: 37 = 10 + 27] --> [Phase assignment]
        P0: 3 smoke commands (troubleshoot, workflow, adversarial) from ready
        P1: 9 needs-change (analyze, build, business-panel, design, document, explain, index, test, load) + fixes to 4 ready (adversarial, cleanup-audit, index-repo, workflow)
        P2: 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot)
        P3: 4 needs-change
        P4: 3 needs-change
   [Dispatchable with a phase that changes them] = 9 + 4 + 11 + 4 + 4 + 3 = 35 of 37
   [Not changed by any phase: brainstorm, init-lite] = 2   <-- spec 2.3 says the brief carries --unattended for every worker (MISMATCH, M-3)
   [Contract required by WC-4 on every outcome for 37 dispatchable commands]
   [Contract-writing change assigned in a phase row] --> adversarial, workflow, 8 of the 9 P1 needs-change (load excluded), 11 P2 needs-change, 4 P3, 3 P4, plus reflect/brainstorm/cleanup-audit(unverified) that already write one
   [No phase assigns a contract change] --> init-lite, index-repo, release-split, tdd, troubleshoot = 5   <-- MISMATCH (F-1)
```
The dimensional mismatch is the 5-command gap in F-1 (WC-4 assumes all 37 produce a contract; only 32 are assigned or already have one). The spec does not say so; this feeds F-1.

## Expert commentary (critique mode, review sequence)
1. Wiegers: requirements WC-1 to WC-12 are individually testable; WC-1 "well inside the readiness limit" has no number (M-5). SA-1 to SA-6 are checkable.
2. Adzic: section 7.2 gives concrete example commands; AC-2.2 (tdd bare topic) is a good example but depends on a contract the spec does not assign (F-1).
3. Cockburn: actors are clear (coordinator, worker session, command, person). Goal of the person who runs standalone is protected by SA-1.
4. Fowler: the shared-file design (`WORKER-CONTRACT.md` plus per-command section) is a sound single-responsibility split; contradiction between SA-2 and AC-C1 below (M-2).
5. Nygard: failure modes are covered: blocked, retry, consumer_fenced, runtime_unavailable. The unparseable-contract case is not (M-4).
6. Whittaker: attacks above.
7. Newman: command interface drift is handled in P3.
8. Hohpe: pull-based follow-ups (WC-12) fit the Orca messaging model.
9. Crispin: acceptance checks are executable; AC-C5's `grep -E '^-[^-]'` would miss a removed line that itself starts with `--`, `---` or `-- flag` text (note, see N-2).
10. Gregory: the five open decisions are self-contained with recommendations.
11. Hightower: no operational concern beyond WC-10 heartbeat cadence.

## Follow-up candidates (Medium and minor; none fails this review)
Medium (warnings):
- M-1 Contract path not computable for rows that say only "add `--output`". WC-4 (line 62) gives a directory-or-file rule, but analyze, build, design, index, test, document, explain, spec-panel (lines 99-125) do not say whether the new flag takes a directory or a file, and no default is stated for the omitted case. An implementer picks one of two readings. (Needs a guess, so Medium.)
- M-2 SA-2 / SA-5 / P0 versus AC-C1. SA-2 (line 147) allows an Orca mention only "as an example of a caller's question channel inside the contract file", and SA-5 (line 150) and P0 (line 158) add an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md`, both under `src/superclaude/core`. AC-C1 (line 172) requires no match of `orca(-ide)? (orchestration|worktree|terminal|agent)` in `src/superclaude/core`. Whether those new texts match the pattern depends on how they are worded. E5 (line 25) says `HOW-WE-WORK.md` has 0 mentions today (UNVERIFIED, file not in workspace).
- M-3 `--unattended` coverage (W-1 above): section 2.3 requires it in every brief, but brainstorm, init-lite (and, for the flag, index-repo and cleanup-audit) are in no phase that makes them accept it. The P1 row also says "a no-op where a command has no gate" only for commands in its Commands column. Separate inconsistency: `load` is in the P1 Commands column (flag accepted, line 159) but AC-1.1 (line 195) exempts it from the `## Unattended mode` section and line 76 says every changed command gains one.
- M-4 WC-5 covers "no report exists" but not a report that exists and is unparseable or lacks `status`; AC step 4 (line 183) checks it but no requirement says what the worker does.
- M-5 WC-1 gives "well inside" the 60 s limit and cites "above about 45 s it fails" (`EVIDENCE.md:56`, UNVERIFIED); no numeric ceiling is stated, so a launch setup with a 40 s fallback would be accepted or rejected by guess.
- M-6 AC-1.2 (line 196) says "each P1 command with `--unattended --output <dir>`", but cleanup-audit has a fixed directory and no `--output` (line 85) and index-repo takes none (line 86); the check cannot be run as written on those two. The P1 row also lists them as "fixes to", which may mean they are not P1 commands; reading is unclear.
- M-7 Section 3.1 line 85 states `cleanup-audit` contract `.claude-audit/return-contract.yaml` as existing today; `INV-A:42` lists no contract for cleanup-audit (only `pass<N>-summary.md`, `progress.json`). The claim is UNVERIFIED against the inventory; it may come from `cmd/cleanup-audit.md:112-117` (not in workspace).
- M-8 WC-4 says commands that already write a contract "keep their fields and add the missing ones", while the status set is fixed to four values. The existing status vocabulary of workflow, reflect, brainstorm and adversarial contracts is not recorded in the inventories (`commands-b.md:272` names the fields `status`, `plan_path`, `reflect_report_path` only), so a conflict between existing values and the fixed set is unknown (UNVERIFIED).

Minor notes:
- N-1 Section 7.2 steps 2 and 3 are written as concurrent (poll `worker-show` at least every 5 minutes while `check --wait` blocks); a single coordinator session cannot do both in one blocking call. Reading as sequential interleaving is possible.
- N-2 AC-C5 (line 176) uses `grep -E '^-[^-]'`, which ignores any removed line starting `--`; edits of such lines would look additive.
- N-3 Section 1.2 E2/E3, WC-1, WC-4 ("`sk/...` via `INV-B:272`") and all `src/`, `CLAUDE.md`, `EVIDENCE.md` citations are UNVERIFIED in this sandbox; the spec's own item 14 (line 285) claims an independent check that this audit cannot confirm.
- N-4 Line 11 says "11 of the load-bearing locations" were re-read; the list has 11 entries, consistent. Line 285's "9 defects (5 overstated, 3 wrong or missing lines, 1 low)" sums to 9, consistent.

Unattended: not set; no issue opened (the session may ask the user once whether to open an issue for the follow-up candidates above; none was created).

Reviser brief
Repair only the blocking finding F-1 in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that F-1 does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

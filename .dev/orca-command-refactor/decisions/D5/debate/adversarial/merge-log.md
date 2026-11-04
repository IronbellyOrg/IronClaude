# Merge Execution Log

## Metadata
- Base: Variant 1 (`variant-1-original.md`, option a, keep depth 1; combined score 0.827)
- Plan: `refactor-plan.md` (19 Planned Changes; auto-approved 2026-11-02)
- Executor: merge-executor agent
- Merged output: `merged-output.md`
- Changes applied: 19 of 19
- Status: success
- Timestamp: 2026-11-02T18:12:51Z

## Executor Notes
- "Change N" refers to refactor-plan.md; "MN" to the sections of merged-output.md (plan target structure M1 to M11).
- Provenance tags follow template section 6, with one format difference: the template's "Base (original, modified) [em dash] reason" is written "Base (original, modified): reason", because the run rules forbid em and en dashes.
- The template's check marks are written as PASS or FAIL in words (no emoji).
- Base content kept unchanged: V1:3 (Position), V1:13 (R2-R5), V1:16 (day to day). Every other base line was modified by a change below.

## Changes Applied

### Change 1: State the root-coordinator precondition
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-001 (HIGH); `CAPS:97`, `CAPS:101`, `CAPS:103`; fixed constraint `CR-01:15`, `CR-01:16, 22`
- **Target**: new M2; M5 (added bullet); M9 Edit 3 (non-goal 2); M10 option (a)
- **Before**: The base stated no precondition on how the coordinator is started.
- **After**: M2 states the coordinator must be a session the person opened (depth 0) in the feature's top-level worktree, never started by `worker-start`; child worktrees are placement, not nesting; depth 0 for a person-opened session is presumed (UNVERIFIED) and traced by AC-0.7. M5 adds the matching working habit.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 1 (invariant-probe.md INV-001, HIGH; ...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Make the "cheap to revisit" claim one-directional
- **Status**: Applied
- **Source**: DA C-008, A-006; R1-V1 concession 5; R2-V1 item 10; R2-V2 item 13
- **Target**: M6, base V1:19 (replace sentence)
- **Before**: "Raising depth later is one desktop setting (`CAPS:99`)", presented as a cheap revisit.
- **After**: "Raising the value is one desktop setting (`CAPS:99`). Lowering it again while deeper workers are running is UNVERIFIED, so a raise is made only on the evidence in M8." M6 now opens "Zero for the setting itself" and points to the spec work in M9 (see Post-Merge Validation, item V-3).
- **Provenance tag**: `<!-- Source: Base (original, modified): V1:19 ... replaced per Change 2 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: "Widens, does not remove"; depth bounds generations, not width
- **Status**: Applied
- **Source**: DA A-001 (CONTRADICTED), C-001; R1-V1 concession 1; R1-V2 A-001; INV-007; `CAPS:99-100`; `SPEC:87`
- **Target**: M3, base V1:8 (replace framing)
- **Before**: Depth 1 called Orca's "fence against runaway fan-out".
- **After**: Depth 1 is the default and tightest setting, one generation; a raise to 2 adds one generation and keeps the refusal and the fallback to 1 (`CAPS:99-100`); depth does not limit width, and the only numeric cap is the fan-in limit of 10 (`SPEC:87`). The base's confirmed quotes of `CAPS:97`, `CAPS:99`, `CAPS:100` and `CAPS:101` are kept.
- **Provenance tag**: `<!-- Source: Base (original, modified): V1:8 "its fence against runaway fan-out" replaced per Change 3 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Say the refusal is presumed, not traced
- **Status**: Applied
- **Source**: V2:16; DA U-007; `CAPS:103`; `SPEC:387`; INV-004 (HIGH)
- **Target**: M3 (append to the V1:8 material); M10
- **Before**: The refusal was presented as enforced.
- **After**: M3 states which calls check depth was not traced (`worker-start`, `dispatch` presumed; `task-create` from depth 1 unknown, `CAPS:103`), names the three files the orchestrator's grep found, marks the verb trace UNVERIFIED, and points to AC-0.7. M10 carries the same in its first bullet.
- **Provenance tag**: `<!-- Source: Base (original, modified): V1:8 refusal presented as enforced; sentence appended per Change 4 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Restore the dropped UNVERIFIED caveat on Agent-tool subagents
- **Status**: Applied
- **Source**: DA spot-check 4; R1-V1 concession 2; R2-V1 item 4; DA C-011; `CAPS:155`
- **Target**: M4, base V1:12 (modify last sentence)
- **Before**: "Agent-tool subagents are not counted by the fence (`CAPS:155`)."
- **After**: The plan's integration text verbatim: not Orca workers, not counted; that Orca never limits them is UNVERIFIED (`CAPS:155`); shown only as sidebar child rows, not Tasks (`CAPS:157`).
- **Provenance tag**: `<!-- Source: Base (original, modified): V1:12 last sentence replaced per Change 5 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: State what option (a) gives up
- **Status**: Applied
- **Source**: Variant 2, "Strongest case for it" (V2:7-8); DA U-005, S-001, X-002, C-004; R1-V1 concession 3; R2-V1 items 6 and 11; INV-016; `CAPS:64`, `SPEC:74`
- **Target**: M4, new subsection "What option (a) gives up" after the V1:13 bullet
- **Before**: Section did not exist.
- **After**: Two numbered costs (no Orca records for in-command fan-out, WC-10 gap stays accepted; one extra coordinator round trip for a run-time split), then the sentence that D5 does not change cost 1 under either option, and that a worker in `check --wait` is live (`CAPS:64`).
- **Provenance tag**: `<!-- Source: Variant 2, "Strongest case for it" (V2:7-8), merged per Change 6 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Per-profile precision for "machine-wide"
- **Status**: Applied
- **Source**: DA A-004; INV-009; `CAPS:98`
- **Target**: M3, base V1:9 (modify)
- **Before**: "The setting is machine-wide, not per run"; raising it raises it for every Orca run on the machine.
- **After**: Per Orca profile, every run under that profile; `local-default` is the only profile, so today a raise affects every run here; no per-run override found (inferred, not proven). The base citation of `orca-data.json:1` and `CAPS:98` is kept.
- **Provenance tag**: `<!-- Source: Base (original, modified): V1:9 "machine-wide, not per run" made per-profile per Change 7 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Record the scoped form (b) would take
- **Status**: Applied
- **Source**: R1-V2 Position summary; R2-V1 and R2-V2 Overall recommendation; DA A-002; INV-008
- **Target**: new M7, paragraph 1; M10 option (b)
- **Before**: Section did not exist.
- **After**: (b) would be depth exactly 2, only a worker's top-level session, only with `Sub-workers: allowed, max N` in its brief, no command file changes (SA-2, WC-8 hold); avoids R2-R4 (`CAPS:148`, `CAPS:150`, `CAPS:145`); a maximum of 2 refuses depth 3 (INV-008).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 8 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Locate (b)'s real cost and residual faults
- **Status**: Applied
- **Source**: V2:19, V2:22; DA U-006, U-008, C-007, C-009; R2-V1 New evidence 1-4; R2-V2 New evidence 1; `SPEC:40`, `SPEC:79`; `CAPS:59`, `CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`
- **Target**: M7, paragraph 2 (as a list of costs); M10 option (b)
- **Before**: Section did not exist.
- **After**: Six-item cost list: new composite brief type; parent inherits the coordinator loop and becomes a second orchestrator (R5); questions probably reach the coordinator's Run mailbox (delivery to parent UNVERIFIED); brief restrains only IronClaude workers; WC-13 would need relaxing; the saving is one coordinator wake, read and `task-create`.
- **Provenance tag**: `<!-- Source: Variant 2 (V2:19, V2:22) and the rebuttals, merged per Change 9 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Replace the revisit trigger with one that can fire
- **Status**: Applied
- **Source**: R1-V2 W3; R2-V1 item 3; R2-V2 New evidence 2 and Overall item 3; INV-010, INV-011; `SPEC:83`, `SPEC:181`
- **Target**: M6 (remove V1:19 trigger); new M8; M9 Edit 5 (run-notes line); M10 revisit bullet
- **Before**: "the spec can revisit it if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate."
- **After**: M8 states the two-condition trigger (a composite brief type is defined, and run notes record a material run-time split) and why the old trigger could not fire. M9 Edit 5 gives the run-notes sentence verbatim.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 10 (...); replaces the trigger removed from V1:19 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Checks before any raise
- **Status**: Applied
- **Source**: R2-V2 Overall recommendation item 4; R2-V2 New evidence 1; R2-V1 critique (iv); `CAPS:59`, `CAPS:103`; `SPEC:387`
- **Target**: M7, paragraph 3; M10 (one sentence)
- **Before**: Section did not exist.
- **After**: Two numbered checks before any raise: the depth-check call sites and `task-create` at depth 1 are traced (AC-0.7), and the mailbox for a depth-2 worker's questions and `worker_done` is established.
- **Provenance tag**: `<!-- Source: Variant 2 Round 2, merged per Change 11 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: Correct the spec text around D5
- **Status**: Applied
- **Source**: R2-V2 New evidence 3; INV-012; `SPEC:27`, `SPEC:36`, `SPEC:315`, `SPEC:350`, `SPEC:353`; DA spot-check 4
- **Target**: M9 Edits 1, 2, 3; M10 (full D5 replacement)
- **Before**: Not in the base (spec-side text).
- **After**: Exact before and after text for E4, R1's last sentence and non-goal 2, copied from the plan's "Other spec edits" items 1-3; M10 replaces `SPEC:350-354`.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 12 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 13: A worker-session rule against Orca fan-out (new WC-13)
- **Status**: Applied
- **Source**: INV-005, INV-013, INV-017 route (h); `SPEC:72`, `SPEC:170`, `SPEC:67-76`; `CAPS:101`, `CAPS:139`
- **Target**: M9 Edit 4 (section 2.2 row, section 2.1 list at `SPEC:58`); M3 and M10 (named as the guard)
- **Before**: Not in the base.
- **After**: The plan's WC-13 row text verbatim in a `text` block, the `SPEC:58` list addition, and the AC-0.1 ripple note (`SPEC:251`).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 13 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: The coordinator starts only Tasks it created
- **Status**: Applied
- **Source**: INV-014, INV-017 route (c); `CAPS:86`, `CAPS:92`, `CAPS:103`; `SPEC:81-85`, `SPEC:387`
- **Target**: M9 Edit 5 (section 2.3 bullet)
- **Before**: Not in the base.
- **After**: The plan's bullet verbatim: the coordinator starts only Tasks it created; a ready Task it did not create is reported to the person with its spec text.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 10 (...) and Change 14 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: A read-only P0 trace of the depth check (new AC-0.7)
- **Status**: Applied
- **Source**: INV-004, INV-013, INV-017 routes (a), (b), (c), (f); `CAPS:103`, `CAPS:171`, `CAPS:180`; `SPEC:202`, `SPEC:256`, `SPEC:278-286`, `SPEC:387`
- **Target**: M9 Edit 8 (section 7.3 row and command block); M9 Edit 10 (UNVERIFIED item 5); referenced from M2, M3, M7, M10, M11
- **Before**: Not in the base.
- **After**: The AC-0.7 row text verbatim in a `text` block (no command in the cell), the fenced grep copied verbatim with its 2026-11-02 result, and the reasons no live probe is used.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 15 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: Re-read the live depth value at every phase (new AC-C6)
- **Status**: Applied
- **Source**: INV-002, INV-017 route (g); `CAPS:98-99`; `SPEC:315`, `SPEC:229-232`, `SPEC:251-256`
- **Target**: M9 Edit 6 (section 7.1)
- **Before**: Not in the base.
- **After**: The AC-C6 pass text verbatim, the fenced command copied verbatim, the `ORCA_RUNTIME_SOURCE_PROFILE_PATH` note, and the recorded 2026-11-02 result (`"nestedWorkerMaxDepth":1`, exit 0).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 16 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 17: Drop the unproven "mechanical backstop" reason
- **Status**: Applied
- **Source**: INV-017; DA A-003; R2-V1 A-003; R2-V2 A-003
- **Target**: M3 (new guard bullets); M10 recommendation line
- **Before**: The base implied depth 1 is a proven fence (V1:8).
- **After**: M3 names the guard as WC-13 plus the 7.2 step 5 transcript check, plus Orca's refusal for each call AC-0.7 confirms, and keeps the A-003 asymmetry only as "presumed". M10's recommendation line says depth 1 alone is not proof.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 17 (...): the unproven "mechanical backstop" reason is dropped -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (after fix V-4 below)

### Change 18: Check WC-13 in every live worker check
- **Status**: Applied
- **Source**: INV-005, INV-006; `SPEC:244`, `SPEC:299-300`
- **Target**: M9 Edit 7 (7.2 step 5 pass item); M9 Edit 9 (7.4 row)
- **Before**: Not in the base.
- **After**: The pass-list item and the 7.4 row, both verbatim, with the AC-0.6 dependency and `--source terminal` fallback noted.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 18 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 19: Widen AC-C1's scan
- **Status**: Applied
- **Source**: INV-006; `SPEC:202`, `SPEC:205-211`
- **Target**: M9 Edit 6 (AC-C1 description and command block)
- **Before**: Not in the base.
- **After**: The replacement block copied verbatim (seven directories, case-insensitive, five exclusions), the plan's note on the two added exclusions (plugin copy of `WORKER-CONTRACT.md` UNVERIFIED), the AR-2 residual, and the 2026-11-02 empty result. The description replacement at `SPEC:205` is given as the plan gives it: by content, not exact words (see V-2).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 19 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Invariant Coverage entries AR-1, AR-2, AR-3
- **Status**: Applied
- **Source**: refactor-plan.md "Invariant Coverage (HIGH UNADDRESSED items)", HIGH rows and "Accepted-risk and open entries"
- **Target**: new M11
- **Before**: Section did not exist.
- **After**: The four HIGH rows (INV-001, INV-004, INV-005, INV-017) and AR-1 to AR-3, all verbatim.
- **Provenance tag**: `<!-- Source: refactor-plan.md "Accepted-risk and open entries" AR-1, AR-2, AR-3, copied verbatim -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Corrected D5 Wording block
- **Status**: Applied
- **Source**: refactor-plan.md "Corrected D5 Wording (target text)"
- **Target**: new M10
- **Before**: Section did not exist.
- **After**: The lead line and the seven-line blockquote, verbatim.
- **Provenance tag**: `<!-- Source: refactor-plan.md "Corrected D5 Wording (target text)", copied verbatim; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

Checks were run on `merged-output.md` by one read-only batch script (grep, sed, comm) on 2026-11-02; result `BATCH_OK failures=0`. Each problem found is graded **blocking** or **minor**; only blocking problems make the status partial.

### Structural Integrity
- Heading hierarchy: PASS. One `#` title; `##` for M1 to M11 in plan order; `###` only under M4 ("What option (a) gives up") and M9 (Edits 1 to 10). No level is skipped. The heading scan also matched `# AC-0.7 starting points ...`, which is a shell comment inside an `sh` fence in M9 Edit 8, not a heading (V-1).
- Section ordering: PASS. M1 Position, M2 Precondition, M3 Safety, M4 Reliability, M5 Day to day, M6 Implementation cost, M7 If (b) is ever chosen, M8 Revisit trigger, M9 Spec changes, M10 Corrected D5 wording, M11 Accepted risks, matching the plan's target structure.
- Document flow: PASS. Base order of M1, M3, M4, M5, M6 (V1:3, V1:7, V1:11, V1:15, V1:18) is kept; new sections sit where the plan's target structure puts them.
- Provenance: PASS. Four header comments, then 32 `<!-- Source: ... -->` tags, at least one per section and one per significant block (each M9 edit, each M3 bullet group, M4 subsection, M10 block, M11 table and AR list).
- Dashes: PASS. No em or en dash in either output file.

### Internal References
- M-section references: 11 distinct (M1 to M11), 11 resolve to headings.
- Change references: 19 distinct (Change 1 to Change 19, plus the ranges "Changes 10, 12-16, 18 and 19", "Changes 13 and 18"), all resolve to Planned Changes in `refactor-plan.md`.
- Spec IDs introduced by the plan: WC-13 (defined in M9 Edit 4; 17 mentions), AC-0.7 (defined in M9 Edit 8; 19 mentions), AC-C6 (defined in M9 Edit 6; 6 mentions). All resolve.
- Accepted-risk IDs: AR-1, AR-2, AR-3 are defined in M11; every mention (M2, M3, M9 Edit 6, M11 table) resolves.
- "M9 edit 5" in M8 resolves to M9 "Edit 5".
- Citations: 60 distinct `SPEC:N`, `CAPS:N` and `CR-01:N` tokens in the merged output; 60 appear in `refactor-plan.md` or `variant-1-original.md`; 0 are new. The one other `path:line` (`orca-data.json:1`) is the base's, unchanged.
- `INV-NNN` IDs: 15 distinct, 15 found in `invariant-probe.md`.
- DA diff-point IDs: 19 distinct, 19 found in `diff-analysis.md`.
- Verbatim copies: M10 lead line and blockquote 8 of 8 lines match the plan; command lines 11 of 11 match the plan (list indent removed only); M11 HIGH rows and AR-1 to AR-3, 7 of 7 lines match.
- Total references checked: 11 M-refs + 19 Change refs + 6 spec and AR IDs + 60 citations + 15 INV + 19 DA = 130. Resolved: 130. Broken: 0.

### Contradiction Re-Scan
Scanned the merged output against the base and the plan. Base claims replaced on purpose (the "fence against runaway fan-out", "machine-wide, not per run", the cheap revisit, the P0 smoke-run trigger, the subagent caveat) are planned corrections, not new contradictions.

- New contradictions introduced: 0 remaining (1 found and fixed, V-4).
- **V-1 (minor).** Heading scan false positive on a shell comment inside a code fence. No action.
- **V-2 (minor).** M9 Edit 6 cannot give exact replacement words for the AC-C1 description at `SPEC:205`, because the plan states only its content (names the seven directories, says the match ignores case). M9 says so plainly. The spec editor writes the words; the command block itself is exact.
- **V-3 (minor, resolved).** Keeping the base's "Zero" alone in M6 would have contradicted M9's added spec work. M6 now says "Zero for the setting itself" and points to M9, using the plan's own Overview and Risk Summary wording ("add requirements or checks to the spec", Medium risk, next consolidated revision, `CR-01:3`). This is a linking sentence beyond the literal integration point of Changes 2 and 10.
- **V-4 (minor, fixed).** M3 first said INV-017's "six are open or unverified", while M11 says Change 14 closes route (c) and Change 13 closes route (h). M3 now says six were open when the probe ran and names the two closures, matching the plan's Invariant Coverage row.
- **V-5 (minor).** M9 Edit 10 uses the plan's "Other spec edits" item 10 ("Resolve: AC-0.7; WC-13 and the coordinator's Task-ownership rule forbid or ignore it either way"), which extends Change 15's shorter "Resolve: AC-0.7". The longer text includes the shorter one; no conflict.
- **V-6 (minor).** Provenance tags use "Base (original, modified): reason" instead of the template's dash form, because of the no-dash rule.
- M5 keeps the base's "No change" next to the new M2 precondition. Not a contradiction: the plan rates Change 1 "Adds a stated precondition; no behaviour changes."
- Every item the plan marks UNVERIFIED is marked UNVERIFIED in the merged output: depth 0 for a person-opened session, which verbs reach the depth check, `task-create` from depth 1 (as "unknown"), lowering the value with live deeper workers, that Orca never limits Agent-tool subagents, sub-worker question delivery to the parent, whether the running app re-reads the profile file, and a plugin copy of `WORKER-CONTRACT.md`.

Blocking problems: none.

## Summary
- Total changes planned: 19 (plus the Invariant Coverage entries AR-1 to AR-3 and the Corrected D5 Wording block)
- Successfully applied: 19 of 19; AR-1 to AR-3 and the Corrected D5 Wording block also applied
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (6 minor items, 0 blocking)
- Files written: `merged-output.md`, `merge-log.md` only. No other file and not the spec was edited.

# Refactoring Plan: Merge into Base (Variant 2)

- Protocol: sc-adversarial-protocol, Mode A, Step 4 (Refactoring Plan Generation, T05.01); template refs/artifact-templates.md Section 4
- Written by: debate orchestrator (neutral; took no part in the debate)
- Date: 2026-11-08T14:41Z
- Base: Variant 2 (`variant-2-original.md`, reviewer 2, qa, haiku slot), selected in `base-selection.md` by the level-1 tiebreaker (V2 0.798, V1 0.792, V3 0.698)
- Inputs: `base-selection.md`, `debate-transcript.md`, `debate/consensus.md` (Parts 2, 4 and 5), `invariant-probe.md` (22 rows), the three variants, `../coverage-matrix.yaml`
- Merge output target: `merged-verdict.yaml` in this directory, using the field shape of run 1's `../../pre/adversarial/merged-verdict.yaml` (shape only; no run 1 finding is reused), with `merge_method: "adversarial"`
- Caller ruling applied: both HIGH UNADDRESSED invariants (INV-006, INV-021) are FIXED in the merge, not recorded as accepted risk. The MEDIUM and LOW UNADDRESSED invariants (INV-005, INV-008, INV-015, INV-018, INV-003, INV-007, INV-010) are carried as findings or as notes on findings at their own probe severity.
- Ground-truth spot check made for this plan: tasklist (TL) lines 989 to 994 (item 6.2) and 2795 to 2804 (`### Execution Log`) were read on 2026-11-08 to design the INV-006 fix. All other TL and DESIGN line numbers below are as quoted in `invariant-probe.md` and `debate/consensus.md`.

## Overview

- Base: Variant 2 (reviewer 2, qa, haiku slot)
- Incorporating strengths from: Variant 1 (analyzer, sonnet slot), Variant 3 (refactorer, opus slot), and the Round 2.5 invariant probe (merge obligations, not a variant)
- Planned changes: 30. Changes 1 to 28 map one to one onto findings F-01 to F-28 of the merged verdict, in order. Change 29 builds the `row_coverage` block. Change 30 sets the header, `unaddressed_invariants_high`, `not_carried`, `best_practice_grade` and `calibrated_confidence` fields.
- Final finding profile: 28 findings, HIGH 2, MEDIUM 13, LOW 13.
- Risk level: Medium overall. Most changes are additive or relabel a base finding. Three restructure (Changes 3, 18 and 26 merge findings from two cards), and two new findings (Changes 2 and 3) carry the caller's HIGH obligations, so their wording must be exact.
- Severity standard for every merged finding: calibrated severity where one exists, and V2's stated bar, "HIGH means correct delivery cannot satisfy the check" (consensus S-006, A-009; the probe applies the same bar). Original card labels are not summed or compared.
- Classification: descriptive `gap_class` labels from V3 (consensus S-007): `unsound-check`, `design-fix`, `traceability`, `test-plan`, `missing-reuse`, plus `authorized-expansion` where the consensus maps a finding to that category (R3-G5).
- Statements the merge must drop from the base or the consensus: "R2-G1 is the only HIGH of the run" (consensus Part 5 rank 1) is wrong after INV-006 and is removed.
- Mechanical corrections to the base (agreed in Round 2, `base-selection.md` "Corrections the merge applies"): replace V2's five uncalibrated HIGH labels with calibrated severity; convert absolute `/home/coder/...` paths to repo-relative paths through `path_aliases`; state the grade scale as "0 to 5".

## Planned Changes

Each change names its source, its target in `merged-verdict.yaml`, the integration approach (replace, append, insert or restructure), the rationale with debate or probe evidence, and its risk. "Keep" means the base finding is carried with the edits listed.

### Change 1: 8.3 name-count check rejects a correct models.py (from Variant 2, base)
- **Source**: Variant 2, R2-G1; probe INV-020 residual
- **Target**: `findings` F-01, HIGH, `gap_class: unsound-check` (keep base, append residual)
- **Rationale**: C-012 at 98%, orchestrator-verified, conceded by V1 and V3 and ranked first by all three (consensus Part 5 rank 1). The calibrator confirmed HIGH. INV-020 (sufficiency_challenge) found the fix alone is enough: 8.3 is the only item that counts names.
- **Integration point**: Keep V2's claim (TL 1436 counts each name with `grep -c` while TL 1433 requires `ClassifiedRow` fields that repeat `SessionRow`, `Classification` and `SafeToClose`; DESIGN 454, 459, 466) and its "Success:" line. Append INV-020's residual to the recommendation: count constants by their definition too (for example `^CLASSES =`), not only `^class`, and note that `^class Classification` does not prefix-match `ClassifiedRow`. Remove the phrase "the only HIGH" wherever the base or consensus attaches it. Provenance: cards [R2-G1], debate [C-012, U-001], invariants [INV-020].
- **Risk**: Low. Additive residual on a finding all three advocates accept.

### Change 2: item 6.2 Verification cannot be met by correct work (new, from the invariant probe)
- **Source**: invariant probe INV-006 (no card or advocate raised it); caller ruling (a)
- **Target**: `findings` F-02, HIGH, `gap_class: unsound-check` (insert)
- **Rationale**: INV-006 is HIGH UNADDRESSED and blocks convergence (`debate-transcript.md` Gate results, AD-1 FAIL). The plan's own text proves it: `grep -n 'OQ-1 (R5) RESOLVED' <TL>` already matches 3 lines before 6.2 runs, TL 991 (the Action's quoted text), TL 993 (the Verification's own pattern) and TL 2802 (the build-time Execution Log row for 6.1-6.4), and 4 after a correct append. Re-read for this plan on 2026-11-08. Correct delivery cannot give "one hit", which is the merge's HIGH bar and the same class as C-012.
- **Integration point**: New finding after F-01. Claim: the 6.2 check expects one hit, but the item's own Action and Verification lines and the TL 2802 log row already match, so a correct run fails. Recommendation, two edits to item 6.2:
  1. Action: append one row to the `### Execution Log` table in its four-column form (`| <timestamp> | 6.2 | <event> | OQ-1 (R5) RESOLVED by the owner 2026-11-08: ... |`), as the TL 2804 rule requires for every owner decision, instead of a bare line.
  2. Verification: count only appended Execution Log table rows whose Item column is 6.2, for example `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED' <TL>` returns 1. The leading-pipe anchor excludes TL 991 and TL 993 (they start with "  - **"), and the Item-column anchor excludes TL 2802 (its Item cell is `6.1-6.4`).
  Success test: before 6.2 runs the command prints 0; after one correct append it prints exactly 1; a second append prints 2 and fails. Provenance: invariants [INV-006], debate [none; outside the 50 diff points], cards [none].
- **Risk**: Low as a change (additive), but the pattern must be copied exactly. If the merge executor alters the anchors, the fix reintroduces the defect. The probe's other two options (grep only under the heading and expect 2; drop the append because TL 2802 already logs the decision) are not chosen. The first still counts TL 2802. On the second: TL 2804 asks for one row per owner decision, not one per item, and TL 2802 already is that row for OQ-1 (R5), so dropping the append would also satisfy TL 2804. It is not chosen because it leaves item 6.2 with no action to check; the chosen fix keeps 6.2 a checkable action, and the 6.2 row is an item-level record of the 6.2 run next to the build-time row.
  Orchestrator check, 2026-11-08: the proposed command prints 0 against the current TL and 1 against a temporary copy with one such row appended.
  Note for the merge executor: run the pattern with plain `grep` (basic regex), never `grep -E`; under `-E` the leading `^|` becomes an empty alternative and the pattern matches every line. The appended row must separate its cells with ` | ` (a space on each side of every pipe); a row written as `|...|6.2|...|` gives 0.

### Change 3: step 1.0a capture outcomes with no owner route, widened so either owner answer leaves the plan executable (from Variant 1, with Variant 2's cursor half and the probe)
- **Source**: Variant 1, R1-G1; Variant 2, R2-G5 (cursor half only); invariant probe INV-021; caller ruling (b)
- **Target**: `findings` F-03, MEDIUM, `gap_class: design-fix` (restructure: V1 claim, V2 cursor evidence folded in, remedy widened)
- **Rationale**: C-001 and C-002 at 95% (V1 wins, V2 conceded its HIGH to V1's MEDIUM); X-001, X-002, X-005 at 95%; A-001 at 80%. Two outcomes are unrouted: (a) a captured cursor field conflicts with the ten-template pins (TL 1482 against TL 1485 and TL 1793; DESIGN 552), and the 7.17 Branch at TL 1267 cannot fire for it; (b) on the CLOSED path a `run-current --json` need has no owner route, and TL 1259 forbids the `--json` probe. INV-021 (HIGH, UNADDRESSED) shows the consensus remedy alone is not enough: if the owner approves an 11th template or `run-current --json`, DESIGN 7.3, 11, 12 (D 794) and 15.1, the 7.16 forbidden list (TL 1259, TL 1262), 8.10 ("exactly 10", TL 1482, TL 1485) and 10.3 (TL 1793) still pin the old state, and nothing re-gates a second allowlist edit. Severity stays MEDIUM (X-002: a stall or conflicted build, not shipped wrong code); INV-021 is cleared by widening the remedy, not by raising the label.
- **Integration point**: Claim from V1 with V2's TL 1482 and TL 1793 evidence. Drop the `gate-bypass` label and describe the gap as unrouted outcomes. Do not claim either "safe stop" or "silent omission" is guaranteed (A-001d, open in substance). Recommendation, in this order:
  1. Add a named branch to item 7.17 covering both outcomes, (a) a cursor field captured and (b) open item 3 CLOSED with `run-current` needing `--json`. The branch first writes a decision file `phase-outputs/plans/OQ-<n>-<topic>-decision.md` under the task folder (`<n>` the next unused OQ number) in the TL 1142 form: `needs_human_decision: true`, `status: PENDING`, the question quoted, the options quoted, the recommendation line and the steps it blocks, and the empty block `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`. It then appends one PENDING row for item 7.17 to the `### Execution Log` table (TL 2804), naming the decision file, and HALTs before step 1.2 under the TL 1142 Branch 1 rule (PENDING or empty `Chosen:`).
  2. In the same branch, state what an owner approval triggers. Either (option A) name the follow-up work: a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate; the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file; the 7.16 forbidden list and its grep (TL 1259, TL 1262) updated to allow the approved argv and a re-capture of it; and a re-run of the R5 review gate (6.5 to 6.22) over the new edit. Or (option B) state that an approval means re-planning before step 1.2, and that no later item runs until the plan is rebuilt.
  3. An owner answer, approval or refusal, is recorded by filling the four lines of the step 1 decision file (`Chosen:`, `Decided by:`, `Decision source:` quoting the owner's words, and `OPERATOR DECISION:`). The resume then follows the TL 1142 Branch 2 rule over that file: it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to Doing as TL 1142 states, and clears `blocker_reason`. An approval resumes into the step 2 follow-up. A refusal resumes with the allowlist unchanged, and the same step records the refusal in `phase-outputs/discovery/1.0a-facts.md` as "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies". This matters because 8.10 reads "From the 1.0a facts: ... the cursor field" (TL 1482): with that line recorded, 8.10 keeps `ALLOWED_ORCA` at exactly 10 (TL 1482, TL 1485), does not page by the captured cursor field, and treats a full page of `WORKER_LIST_PAGE` rows as truncated with a lower-bound total (DESIGN 973). The refusal path is justified by INV-021's own sentence "If the owner declines, the plan works", not by INV-016, which covers only the separate case where step 1.0a finds no cursor field.
  Success test: a grep of item 7.17 finds the new branch naming both outcomes; the decision file path `phase-outputs/plans/OQ-<n>-<topic>-decision.md` with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines; the PENDING Execution Log row; the HALT before step 1.2; a resume step that names that decision file; the refusal line for `1.0a-facts.md`; and either the four follow-up targets (DESIGN edit, 8.10 and 10.3 count source, 7.16 forbidden list, review re-run) or the re-planning sentence. When the branch fires, the check confirms that the decision file exists with `status: PENDING`, that the Execution Log holds exactly one PENDING row for item 7.17 naming that file, and that the task is halted (status and `blocker_reason` set by the HALT rule) before any step 1.2 item runs. No consumer listed in INV-021 is left pinned to ten templates with no named updater. Provenance: cards [R1-G1, R2-G5], debate [C-001, C-002, X-001, X-002, X-005, A-001, A-001c, A-001d], invariants [INV-021, INV-016].
- **Risk**: High. It restructures two card findings and widens the remedy beyond what any card wrote. Rollback: revert to the consensus rank 2 wording, which re-opens INV-021 and is not allowed under the caller ruling.

### Change 4: DESIGN 80 builder rule not copied into the task (from Variant 2, base)
- **Source**: Variant 2, R2-G2
- **Target**: `findings` F-04, MEDIUM, `gap_class: traceability` (keep base; replace the HIGH label)
- **Rationale**: C-013 at 90%, unique to V2; calibrated MEDIUM and V2 conceded its HIGH (consensus rank 3). Under the HIGH bar it fails: the base text itself says "No present stale-count use or REPORT edit was found" (`base-selection.md` IC note).
- **Integration point**: Keep claim, ref and quote pairs, and "Success:" line. Word it as a missing Key Constraints bullet, not an observed breach. Rows GQ-111, GQ-112, GQ-113 (partial) and INF-001 (missing) point at F-04.
- **Risk**: Low. Relabel only.

### Change 5: byte limits not marked "proposed"; open item 19 has no closing disposition (from Variant 2, base, with probe note INV-003)
- **Source**: Variant 2, R2-G3; invariant probe INV-003 (LOW, UNADDRESSED)
- **Target**: `findings` F-05, MEDIUM, `gap_class: traceability` (keep base; replace the HIGH label; append an invariant note)
- **Rationale**: C-014 at 90%; calibrated MEDIUM (consensus rank 4). INV-003: `Total: 23 open items.` (DESIGN 993) is pinned at TL 269, 454, 784 and 1005, so a remedy that closes, splits or adds an open item breaks four pins.
- **Integration point**: Keep claim and evidence. Append to the recommendation a note tagged "INV-003, LOW": the closing disposition for open item 19 must keep 23 rows, or the same edit must update all four pins. Rows SP-28 (partial) and INF-024 (missing) point at F-05.
- **Risk**: Low. Relabel plus an additive note.

### Change 6: missing checks for the probes.py import boundary, B5 and renderer bans (from Variant 2, base)
- **Source**: Variant 2, R2-G4
- **Target**: `findings` F-06, MEDIUM, `gap_class: test-plan` (keep base; replace the HIGH label)
- **Rationale**: C-015 at 90%; calibrated MEDIUM (consensus rank 5). State as missing checks for DESIGN 211, 219 and 638, not proven breaches, and keep V2's note that an import-absence grep cannot prove B5 (`base-selection.md` Strengths to Preserve 4).
- **Integration point**: Keep claim and the "Success:" line. Rows INF-005, INF-018 (partial) and INF-008 (missing) point at F-06.
- **Risk**: Low. Relabel only.

### Change 7: set-union session-count wording untraced (from Variant 2, base)
- **Source**: Variant 2, R2-G6
- **Target**: `findings` F-07, MEDIUM, `gap_class: traceability` (keep base)
- **Rationale**: C-016 at 90%; V2's only recall pass beyond the matrix (`base-selection.md` rationale). V2 concedes broad delegation may still deliver DESIGN 636, so it is a traceability gap.
- **Integration point**: Keep as is; add the "may still be delivered by delegation" qualifier.
- **Risk**: Low.

### Change 8: D10 row cells and R5 history line under-report the SPEC departure (from Variant 3)
- **Source**: Variant 3, R3-G1 with R3-G7 merged in
- **Target**: `findings` F-08, MEDIUM, `gap_class: traceability` (insert)
- **Rationale**: C-017 at 90%, unique to V3 (consensus rank 7): 6.3 (TL 998, TL 999) omits sections 2.2 and 12 and the SPEC lines. One finding, not two. INV-018 adds that once section 4 is edited (Changes 9 and 20), the R5 row and the D10 "where" cell must list section 4 too, or this defect returns.
- **Integration point**: V3 claim; recommendation lists sections 2.2, 12 and, if Change 12 is applied, 4, plus the SPEC lines. Convert V3's single evidence mapping to a list and replace R3-G7's note-as-quote with a TL quote (S-003 conventions). Provenance invariants [INV-018].
- **Risk**: Low. Additive; the merged-in R3-G7 text must not appear twice.

### Change 9: DESIGN 221 still requires a capture before a new template (from Variant 3)
- **Source**: Variant 3, R3-G5 (first remedy only)
- **Target**: `findings` F-09, MEDIUM, `gap_class: authorized-expansion` (insert)
- **Rationale**: C-020 at 90%, X-006 and A-005 at 95%: R5 authorizes templates 9 and 10, but DESIGN 221 still says "only after a capture" and no 6.3 step reaches it. All three classify it as an authorized expansion with an incomplete record, not scope creep. Severity is open in substance (consensus Part 4 item 7): the card says MEDIUM and not all three advocates narrowed it, so the consensus rule keeps MEDIUM; record "LOW defensible by runtime effect while nothing calls the templates" in the claim.
- **Integration point**: Remedy: reword DESIGN 221 to allow a recorded owner decision. Drop V3's second remedy (add `agent-wait` to the capture), which V3 withdrew. Cross-reference F-12, since this edit lands in section 4.
- **Risk**: Medium. The severity is contested; the merge must show the open state rather than settle it.

### Change 10: 6.4 pass rule needs a 15.1 hit that 6.3 removes (from Variant 3)
- **Source**: Variant 3, R3-G6 (15.1 half only)
- **Target**: `findings` F-10, MEDIUM, `gap_class: unsound-check` (insert)
- **Rationale**: C-021 at 90% (consensus rank 9). Use V3's wording, "ambiguous; costs a fix loop via TL 1007", not V1's "cannot pass" (open in substance, Part 4 item 7). INV-022 found the one-clause fix alone is enough.
- **Integration point**: Remedy: write the TL 1259 sentence ("`worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a") into 15.1 in 6.3 step (4). Drop the D10 half (conceded). Provenance invariants [INV-022].
- **Risk**: Low.

### Change 11: TL 1142 points HALT items at item 6.2, titled "no HALT" (from Variant 1)
- **Source**: Variant 1, R1-G2
- **Target**: `findings` F-11, MEDIUM, `gap_class: design-fix` (insert)
- **Rationale**: C-003 at 90%; calibrated MEDIUM (consensus rank 10). All three say impact is lower because TL 1142 spells out both Branches itself.
- **Integration point**: Claim with the impact note. The residual is that 7.15 and 14.7 Branch 2 do not require the owner's quoted words. Fill V1's empty evidence list with TL 1142 and TL 989 quotes (S-003).
- **Risk**: Low.

### Change 12: section 4 edits from F-09 and F-20 land outside every review (new, from the invariant probe)
- **Source**: invariant probe INV-018 (MEDIUM, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-12, MEDIUM, `gap_class: design-fix` (insert)
- **Rationale**: The R3-G5 remedy (DESIGN 221) and the R3-G2 remedy (DESIGN 181, 196) both edit section 4 (DESIGN 157 to 221). Section 4 is outside the 6.3 Context and Output (TL 997, TL 999), the 6.4 checks (TL 1005) and every R5 gate input list (TL 1011, TL 1018). As the consensus words them, these edits would land with no review (`base-selection.md` merge obligations).
- **Integration point**: Recommendation: add section 4 to the 6.3 Output, to the 6.4 checks and to the 6.5 to 6.13 input lists, and list section 4 in the R5 row and the D10 row. Success test: a grep of 6.3, 6.4 and TL 1011 and TL 1018 finds "section 4" (or "4,") in each list. Cross-reference F-08, F-09, F-20.
- **Risk**: Medium. It widens the R5 gate inputs, which every later 6.x lens reads.

### Change 13: a resumed HALT and the existing 7.17 design-fix branch name no follow-up item (new, from the invariant probe)
- **Source**: invariant probe INV-005 (MEDIUM, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-13, MEDIUM, `gap_class: design-fix` (insert)
- **Rationale**: TL 1142 Branch 2 only records RESOLVED and resets status (TL 194 HALT rule). The existing 7.17 branch (TL 1267) halts with "the design needs a fix before step 1.2", but no item carries that design fix or re-pins the downstream checks. This is independent of R1-G1; INV-021 is the HIGH case of the same gap and is handled in F-03.
- **Integration point**: Recommendation: the TL 1267 branch states what a resume requires (a named DESIGN edit item with its gate, or re-planning before step 1.2), using the same wording as F-03 step 2 so the two branches agree. Cross-reference F-03.
- **Risk**: Low. Additive; must not contradict F-03's wording.

### Change 14: the 7.16 forbidden-token grep fails an honest capture (new, from the invariant probe)
- **Source**: invariant probe INV-008 (MEDIUM, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-14, MEDIUM, `gap_class: unsound-check` (insert)
- **Rationale**: TL 1262 greps the whole `readonly-probe.md` for `worker-read`, `gate-list`, `inbox`, `include-remote`, `stash` and `run-current --json`, but TL 1260 puts stdout, stderr and a "what it settles" line in that file. Capture item 2 (DESIGN 874, 883) is about whether `run-current` needs `--json`, so an honest line names it, and real Task text can mention stash or inbox. The consensus kept only the missing-sentence half (C-007), which does not cover this.
- **Integration point**: Recommendation: limit the forbidden-token grep to the recorded command lines of `readonly-probe.md`, not its stdout, stderr or "what it settles" text. Success test: an honest capture whose notes mention `run-current --json` passes, and a recorded command line using a forbidden token fails. Cross-reference F-16 (the missing forbidden-list sentence) and F-03 step 2 (the forbidden list changes on approval).
- **Risk**: Low.

### Change 15: a Run with zero Dispatch rows leaves capture items empty and the HALT text ambiguous (new, from the invariant probe)
- **Source**: invariant probe INV-015 (MEDIUM, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-15, MEDIUM, `gap_class: design-fix` (insert)
- **Rationale**: With zero Dispatch rows, 7.16 step (1) learns no ids, template 3 never runs, and capture items 4 and 13 are empty; open items 1, 6, 22, 23 and the `DISPATCH_ID_RE` half of open item 2 (DESIGN 970) stay unverified. The 7.17 HALT text "no Run or Dispatch id sample" (TL 1269) is ambiguous when only the Run sample exists, while 8.10 needs `DISPATCH_ID_RE` (TL 1482). The consensus covers only "live Orca access assumed" (A-007b).
- **Integration point**: Recommendation: item 7.15 names a Run with at least one Dispatch row, and 7.17 makes a missing Dispatch sample an explicit open-item-2 HALT.
- **Risk**: Low.

### Change 16: bare `coder` grep and an unwritten forbidden-list sentence (from Variant 1)
- **Source**: Variant 1, R1-G5
- **Target**: `findings` F-16, LOW, `gap_class: unsound-check` (insert)
- **Rationale**: C-007 at 90%, unique and confirmed (consensus rank 11): the 7.18 grep at TL 1276 searches bare `coder`, and 7.16 expects a forbidden-list sentence the Action never writes.
- **Integration point**: Leave out V1's SOURCES.md extension (unverified, [INFERRED]; Part 4 item 8). Cross-reference F-14.
- **Risk**: Low.

### Change 17: echo and ls in 7.16 Action step 6 against its Verification (from Variant 1)
- **Source**: Variant 1, R1-G6 (first sentence only)
- **Target**: `findings` F-17, LOW, `gap_class: unsound-check` (insert)
- **Rationale**: C-008 at 90% (consensus rank 12): TL 1260 runs echo and ls while TL 1262 allows only templates or file reads. V1 withdrew the second (agent-wait) sentence.
- **Integration point**: First sentence only; fill the evidence list with TL 1260 and TL 1262 quotes.
- **Risk**: Low.

### Change 18: name the 7.16 capture actor (from Variant 2 framing, merged with Variant 1)
- **Source**: Variant 2, R2-G8; Variant 1, R1-G4
- **Target**: `findings` F-18, LOW, `gap_class: design-fix` (restructure: merge two findings under V2's framing)
- **Rationale**: C-005 at 80% (V2 framing preferred), A-002 and A-002a at 70%: an actor-identity clarification, not a claim of unauthorized capture. Whether the executor is the DESIGN 868 coordinator is unknown, not shown false.
- **Integration point**: One finding, V2 wording; provenance cards [R2-G8, R1-G4]. Row INF-017 (partial) points at F-18 and F-19.
- **Risk**: Medium (restructure), low impact.

### Change 19: matrix row INF-017 cites F11; it should be F12 (from Variant 2, base)
- **Source**: Variant 2, R2-G9
- **Target**: `findings` F-19, LOW, `gap_class: traceability` (keep base)
- **Rationale**: C-006 at 95%, unique and confirmed.
- **Integration point**: Keep as is.
- **Risk**: Low.

### Change 20: DESIGN 181 and 196 keep the count of 8; no zero-argv pin for templates 9 and 10 (from Variant 3)
- **Source**: Variant 3, R3-G2
- **Target**: `findings` F-20, LOW, `gap_class: unsound-check` (insert)
- **Rationale**: C-018 at 95%, re-verified by V1 and V3; INV-011 and INV-012 confirm both halves stay LOW (8.10 states "exactly 10", so code is not misled).
- **Integration point**: Remedy: widen the 6.3 grep to catch "(8)" and "8 read", and add zero-argv assertions for templates 9 and 10 in 10.3. Cross-reference F-12, since the DESIGN edits land in section 4.
- **Risk**: Low.

### Change 21: both 5.11 hits are in section 13, not 13 and 14 (from Variant 3)
- **Source**: Variant 3, R3-G4
- **Target**: `findings` F-21, LOW, `gap_class: traceability` (insert)
- **Rationale**: C-019 at 90%; verified by V3 only (Part 4 item 8), so tag it single-source.
- **Integration point**: Insert with a "verified by one reviewer" note.
- **Risk**: Low.

### Change 22: missing citation of config.py:64-78 in the `_git` seam (from Variant 3, narrowed)
- **Source**: Variant 3, R3-G9 (narrowed)
- **Target**: `findings` F-22, LOW, `gap_class: traceability` (insert)
- **Rationale**: C-023 at 90%. V3's own new evidence narrows it: TL 1448 already states `check=False` and `GitCallFailed`, so only the citation is missing. Close to a refinement.
- **Integration point**: Narrowed claim only; drop the "missing reuse" framing.
- **Risk**: Low.

### Change 23: item 9.1 says "five helpers"; DESIGN 7.1 lists four plus `_publish` (from Variant 3)
- **Source**: Variant 3, R3-G10
- **Target**: `findings` F-23, LOW, `gap_class: traceability` (insert)
- **Rationale**: C-024 at 90%; INV-013 confirms (DESIGN 438 to 442).
- **Integration point**: Insert as is.
- **Risk**: Low.

### Change 24: OQ-16 wording says no fixture covers templates 9 and 10 (from Variant 3)
- **Source**: Variant 3, R3-G11
- **Target**: `findings` F-24, LOW, `gap_class: test-plan` (insert)
- **Rationale**: C-025 at 90%, weakened: 10.3 has a positive unit case (TL 1793). One-line wording fix.
- **Integration point**: Insert as a wording fix.
- **Risk**: Low.

### Change 25: define which 7.16 fields count as timestamps (from Variant 1, clarification only)
- **Source**: Variant 1, R1-G3
- **Target**: `findings` F-25, LOW, `gap_class: design-fix` (insert)
- **Rationale**: C-004 at 80%: TL 1260 and TL 1262 already strip timestamps; V1 conceded. INV-009 confirms the stop on a live change is safe, not silent.
- **Integration point**: Do not say "no strip rule". Recommend naming the fields (for example `status`, `liveness`, `agentWait`) that the before-and-after comparison ignores or treats as timestamps.
- **Risk**: Low.

### Change 26: DESIGN 939 "every hit justified" scope, a fidelity note (from Variants 1 and 2, merged)
- **Source**: Variant 1, R1-G9; Variant 2, R2-G7
- **Target**: `findings` F-26, LOW, `gap_class: traceability` (restructure: two findings into one note)
- **Rationale**: C-011 at 90%, X-003 at 90%, A-004c at 90%: both mechanisms are defeated (TL 2471 recounts at the base; TL 2256 and TL 2469 settle concealment). Only the open reading remains: whether DESIGN 939 covers the 168 pre-existing hits.
- **Integration point**: One LOW note stating the open reading only; drop both mechanisms. Mark it "open, LOW either way".
- **Risk**: Medium (restructure), low impact.

### Change 27: a 6.3 re-run after a FAIL matches the ban quoted in D10 and Fix cycle 3 (new, from the invariant probe)
- **Source**: invariant probe INV-007 (LOW, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-27, LOW, `gap_class: unsound-check` (insert)
- **Rationale**: TL 1007 re-runs 6.3 on a FAIL. Re-running step (5) (TL 998: reword every DESIGN sentence that says `worktree ps` never carries `--agent-wait`) after step (6) has written D10 now matches D10's second cell, which quotes that ban as the SPEC text being departed from. The consensus dropped the D10 half of C-021 for readers, which does not cover a re-run.
- **Integration point**: Remedy: exclude the section 13 D10 row and the Fix cycle 3 table from step (5). Cross-reference F-10.
- **Risk**: Low.

### Change 28: the 6.3 tuple count can exceed 3 on a correct edit (new, from the invariant probe)
- **Source**: invariant probe INV-010 (LOW, UNADDRESSED); caller ruling (c)
- **Target**: `findings` F-28, LOW, `gap_class: unsound-check` (insert)
- **Rationale**: `grep -c '("worktree", "ps"'` expects 3 (DESIGN 527 plus two new tuples), but step (3) asks for a section 11 positive case for both `--agent-wait` templates; written in tuple syntax in the DESIGN 738 row, it makes the count 4 or 5 and fails a correct edit.
- **Integration point**: Remedy: count within the 7.3 code block only. LOW: the executor can avoid it by wording, so correct delivery can still pass.
- **Risk**: Low.

### Change 29: build `row_coverage` from the three cards' row verdicts (from all three variants)
- **Source**: the `row_coverage` lists of Variants 1, 2 and 3; `../coverage-matrix.yaml` for the parsed or inferred source of each id
- **Target**: `row_coverage` block (restructure: union of three disjoint slices)
- **Rationale**: The slices are disjoint by assignment (S-001 at 90%). The union check was re-run at Step 3 (`base-selection.md` coverage statement; `debate-transcript.md` note added at Step 3) and again for this plan: 152 of 152 matrix ids, pairwise overlap 0, no id outside the matrix. This clears A-006a and INV-014 (no longer a single-advocate report). One verdict changes: INF-019 from covered-in-substance to partial (X-001, X-005; V2 conceded the CLOSED path is unrouted). V1's step-1.0a partial is kept (X-005).
- **Integration point**: Fill the block with the numbers in "Merged verdict field plan" below. Mark V1 rows "item-checked, second ref unreliable" and discard the 41 second refs in the DESIGN 444 to 484 range and the two "Section 8 gate" refs (S-004). Keep V3's 21 rows that cite only "T1 matrix row" tagged [INFERRED] and not counted as independently confirmed. Caveats: delegated rows are covered only if the delegate item runs as written; row verdicts carry different weights by card.
- **Risk**: Medium. Changes verdict counts that downstream gates read (`coverage_pct`).

### Change 30: header, invariants block, not_carried, grade and confidence (orchestrator)
- **Source**: `debate-transcript.md` Gate results; `invariant-probe.md` Summary; `base-selection.md`; the three calibrated cards (`../reviewer-cards/reviewer-{1,2,3}-card-calibrated.yaml`)
- **Target**: top-level fields of `merged-verdict.yaml` (replace)
- **Rationale**: The run 1 shape carries `merge_method`, `base_variant`, `sources`, `convergence_score`, `convergence_status`, `path_aliases`, `unaddressed_invariants_high`, `severity_counts`, `findings`, `row_coverage`, `not_carried`, `best_practice_grade` and `calibrated_confidence`. Each is set from this run's evidence.
- **Integration point**: Values in "Merged verdict field plan" below. `unaddressed_invariants_high` lists INV-006 (covered by F-02) and INV-021 (covered by F-03 step 2), so the AD-1 block is cleared by the merge itself. Every one of the nine UNADDRESSED invariant ids (INV-003, 005, 006, 007, 008, 010, 015, 018, 021) must appear in at least one finding's `provenance.invariants`.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

These go into `not_carried` in the merged verdict.

| Diff Point | Non-Base Approach | Rationale for Not Carrying |
|------------|-------------------|----------------------------|
| C-009, U-010 | R1-G7 (V1): 9.3 does not read OQ-8 or halt | Refuted by calibration; V1 withdrew it in both rounds. 9.3 reads OQ-8 at TL 1640 and halts at TL 1643 (95%). INV-019 confirms no later item relies on it. |
| C-010, A-003 | R1-G8 (V1): TL 163 template count is wrong | TL 163 is accurate or at worst ambiguous ("eight called in Phase 1", step 1.0a uses templates 1 to 8; TL 1257, 1258); both claimants withdrew (95%). |
| C-010, A-003 | R3-G3 (V3): same TL 163 count complaint | Same evidence as R1-G8; V3 withdrew (95%). |
| C-022 | R3-G8 (V3): edit the D6 row to cite SPEC lines | Superseded by item 5.4, which already cites SPEC 415 and 583 and forbids other D6 edits; V3 conceded its remedy conflicts (95%). |
| C-020 | R3-G5 second remedy (V3): add `agent-wait` to the capture | Withdrawn by V3. Only the DESIGN 221 rewording is carried (F-09). |
| C-021 | R3-G6 D10 half (V3) | Conceded: a reader sees D10 as history. The re-run risk the probe found is carried separately as F-27 (INV-007). |
| C-008 | R1-G6 second sentence (V1, `agent-wait`) | Withdrawn by V1. First sentence carried as F-17. |
| X-001, X-005 | R2-G5 run-current narrowing and V2 row INF-019 "covered-in-substance" | V2 conceded its delegation reading covers only the STILL UNVERIFIED path; the CLOSED path is unrouted. INF-019 becomes partial; the cursor half of R2-G5 is folded into F-03. |
| A-001 | `gate-bypass` label on R1-G1 | Dropped by consensus in favour of an unrouted-outcome description (F-03). |
| X-002, X-004, A-009 | V2's original HIGH labels on R2-G2, R2-G3, R2-G4, R2-G5, R2-G7 | Calibrated MEDIUM or LOW; each card text says correct delivery is not blocked, which fails V2's own HIGH bar (IC 0.906, K4 NOT MET). |
| C-011, X-003, A-004 | R1-G9 base-drift mechanism and R2-G7 same-count concealment mechanism | Defeated by TL 2471 (recount at the recorded base) and TL 2256 with TL 2469 (scope). Only the open DESIGN 939 reading survives, as F-26. |
| C-007 | V1's SOURCES.md extension of R1-G5 | [INFERRED] and unverified by any grep (Part 4 item 8). |
| S-004 | V1's 41 failed second refs (DESIGN 444 to 484) and two "Section 8 gate" refs | Failed calibration; V1 conceded. V1 row verdicts are kept, these refs are discarded. |
| consensus Part 5 rank 1 | "R2-G1 is the only HIGH of the run" | Wrong after INV-006 (F-02). |
| INV-006 options | Probe's alternative fixes: grep under the heading and expect 2; drop the append | The first still counts the TL 2802 build-time row. The second would satisfy TL 2804, since TL 2802 already is the one row for the OQ-1 (R5) decision, but it leaves item 6.2 with no action to check. The anchored-row check (F-02) is used instead: it keeps 6.2 a checkable action, and the 6.2 row is an item-level record next to the build-time row. |
| X-002 | Raising F-03 to HIGH because of INV-021 | The plan defect is a stall, not shipped wrong code (X-002, 95%). INV-021 is a remedy-sufficiency gap and is cleared by widening the remedy (Change 3), as the caller ruled. |
| INV-004 | `grep -c` in 6.1 counts lines, not distinct parts | ADDRESSED, LOW; the decision file is complete today, so there is no present risk. Not carried as a finding. |
| INV-001 | The `### Fix cycle 3` table exists, rows R3-B1, R3-B2, R3-B3 and R4 in order, when 6.3 step (7) appends the R5 row | ADDRESSED, LOW, no gap: item 2.6 creates the table (TL 279-283), items 3.4, 4.5 and 5.11 add rows, and Phase 5 runs before Phase 6, so the order holds. No finding. |
| INV-002 | The deviation total is 9 until item 6.3 and 10 after it, and no later item expects 9 | ADDRESSED, LOW, no gap: items 3.3 and 5.10 pin 9 before Phase 6, 6.3 step (6) sets 10 (TL 998) and 6.4 checks 10 (TL 1005); no later item pins 9 and no merged finding adds a deviation. No finding. |
| INV-017 | Zero-hit greps and an unavailable Orca are handled | ADDRESSED, LOW, no gap: 6.4 expects no `TODO` or `TBD` hits (TL 1005), capture item 9 covers an unavailable Orca (TL 1260), 7.17 halts on an unverified open item 2 (TL 1269), 7.18 writes a `SOURCES.md` when nothing was captured (TL 1276), and 9.3 halts when the Run is not readable (TL 1638-1644). No finding. |
| A-007, S-008 | Ranking the card grades 4, 3 and 4 against each other | The scales differ and V2 conceded grade 3 is not defensible on an unstated scale. The merged grade is set fresh on V3's written scale. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | INV-020 residual lost; constants still counted by reference | Revert to base R2-G1 text |
| 2 | Low (exactness matters) | A mistyped anchor reintroduces a check correct work cannot pass, and AD-1 stays blocked | Re-copy the pattern from Change 2; re-run the 0-then-1 test |
| 3 | High | A narrower remedy re-opens INV-021, which the caller ruled must be fixed | Re-apply Change 3 steps 1 to 3; never fall back to the consensus rank 2 wording |
| 4 to 7 | Low | Severity profile wrong if a HIGH label survives | Replace with calibrated MEDIUM |
| 8 | Low | R3-G7 duplicated, or section 4 missing from the list after Change 12 | Merge text once; add section 4 |
| 9 | Medium | Severity presented as settled | Restore the "MEDIUM, LOW defensible" wording |
| 10, 11 | Low | V1's "cannot pass" wording slips in (Change 10) | Use V3's wording |
| 12 | Medium | Section 4 edits from F-09 and F-20 stay unreviewed | Re-apply the four list additions |
| 13 to 15 | Low | MEDIUM invariants dropped, against caller ruling (c) | Re-insert from `invariant-probe.md` |
| 16, 17, 19 to 25 | Low | Minor wording or citation drift | Revert to the card text named in Source |
| 18, 26 | Medium (restructure) | Merged note keeps a defeated mechanism or a dropped framing | Re-merge under the stated framing |
| 27, 28 | Low | LOW invariants dropped, against caller ruling (c) | Re-insert from `invariant-probe.md` |
| 29 | Medium | Wrong `coverage_pct` reaches downstream gates | Recompute from the three cards and the matrix (method below) |
| 30 | Low | AD-1 block shown as open, or a confidence or grade mismatch | Reset from the field plan |

## Merged verdict field plan

### Header fields

| Field | Value |
|-------|-------|
| `schema` | `sc-reflect-merged-verdict/v1` |
| `merge_method` | `adversarial` |
| `base_variant` | `"variant-2 (reviewer 2, qa, haiku slot)"` |
| `sources` | `[variant-1, variant-2, variant-3, invariant-probe]` |
| `convergence_score` | `1.00` (50 of 50 diff points; 58 of 58 with sub-points) |
| `convergence_status` | `BLOCKED_BY_INVARIANTS` as recorded at Step 2, with a comment that both blocking items are fixed in this merge (F-02, F-03) and none is recorded as accepted risk |
| `path_aliases` | `TL` (the tasklist), `DESIGN` (`docs/designs/orchestrator-mode.md`), `coverage-matrix` (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/coverage-matrix.yaml`), `OQ-1-decision` (`phase-outputs/plans/OQ-1-agent-wait-decision.md` under the task folder) |
| `unaddressed_invariants_high` | `INV-006` covered by "F-02: 6.2 appends a table row with Item 6.2; the check counts only that row (0 before, 1 after)"; `INV-021` covered by "F-03 step 2: the 7.17 branch names the follow-up on approval (DESIGN edit, 8.10 and 10.3 count source, 7.16 forbidden list, review re-run) or states re-planning before step 1.2" |
| `severity_counts` | `{HIGH: 2, MEDIUM: 13, LOW: 13, total: 28}` |

### Final findings, HIGH first

| id | Severity | gap_class | Source | Short title | Invariants in provenance |
|----|----------|-----------|--------|-------------|--------------------------|
| F-01 | HIGH | unsound-check | R2-G1 | 8.3 `grep -c` counts references, so a correct models.py fails; count definitions, constants too | INV-020 |
| F-02 | HIGH | unsound-check | probe (new) | 6.2 check expects one hit but its own lines and the TL 2802 row already match; count only the appended 6.2 table row | INV-006 |
| F-03 | MEDIUM | design-fix | R1-G1 + R2-G5 cursor half | Two unrouted step 1.0a outcomes; 7.17 branch sends both to the owner as PENDING plus HALT and names the follow-up on approval, or re-planning | INV-021, INV-016 |
| F-04 | MEDIUM | traceability | R2-G2 | DESIGN 80 builder rule not copied into Key Constraints | none |
| F-05 | MEDIUM | traceability | R2-G3 | Byte limits not marked proposed; open item 19 has no closing disposition. Note: keep 23 open items or update the four pins | INV-003 (LOW note) |
| F-06 | MEDIUM | test-plan | R2-G4 | No checks for the probes.py boundary, B5 and renderer bans | none |
| F-07 | MEDIUM | traceability | R2-G6 | Set-union session-count wording untraced | none |
| F-08 | MEDIUM | traceability | R3-G1 + R3-G7 | D10 row and R5 history line omit sections 2.2, 12 (and 4) and the SPEC lines | INV-018 |
| F-09 | MEDIUM | authorized-expansion | R3-G5 | DESIGN 221 still requires a capture before a new template; LOW defensible | INV-018 |
| F-10 | MEDIUM | unsound-check | R3-G6 (15.1 half) | 6.4 needs a 15.1 allowing hit that 6.3 removes | INV-022 |
| F-11 | MEDIUM | design-fix | R1-G2 | TL 1142 points at item 6.2 ("no HALT"); 7.15 and 14.7 Branch 2 lack the owner-quote rule | none |
| F-12 | MEDIUM | design-fix | probe (new) | Section 4 edits land outside 6.3, 6.4 and the R5 gate inputs | INV-018 |
| F-13 | MEDIUM | design-fix | probe (new) | Resumed HALT and the existing 7.17 design-fix branch name no follow-up item | INV-005 |
| F-14 | MEDIUM | unsound-check | probe (new) | 7.16 forbidden-token grep scans output and notes, so an honest capture fails | INV-008 |
| F-15 | MEDIUM | design-fix | probe (new) | Zero Dispatch rows leave capture items empty and the 7.17 HALT text ambiguous | INV-015 |
| F-16 | LOW | unsound-check | R1-G5 | Bare `coder` grep; forbidden-list sentence never written | none |
| F-17 | LOW | unsound-check | R1-G6 (first sentence) | echo and ls in 7.16 against its Verification | none |
| F-18 | LOW | design-fix | R2-G8 + R1-G4 | Name the 7.16 capture actor | none |
| F-19 | LOW | traceability | R2-G9 | Matrix row INF-017 cites F11, should be F12 | none |
| F-20 | LOW | unsound-check | R3-G2 | DESIGN 181 and 196 keep 8; no zero-argv pin for templates 9 and 10 | INV-011, INV-012 |
| F-21 | LOW | traceability | R3-G4 | Both 5.11 hits are in section 13 (single-source) | none |
| F-22 | LOW | traceability | R3-G9 (narrowed) | Missing citation of config.py:64-78 | none |
| F-23 | LOW | traceability | R3-G10 | "five helpers" against four plus `_publish` | INV-013 |
| F-24 | LOW | test-plan | R3-G11 | OQ-16 wording: 10.3 has a positive case | none |
| F-25 | LOW | design-fix | R1-G3 | Define which 7.16 fields count as timestamps | INV-009 |
| F-26 | LOW | traceability | R1-G9 + R2-G7 | DESIGN 939 scope over the 168 pre-existing hits, open | none |
| F-27 | LOW | unsound-check | probe (new) | 6.3 re-run matches the ban quoted in D10 and Fix cycle 3 | INV-007 |
| F-28 | LOW | unsound-check | probe (new) | 6.3 tuple count can exceed 3 on a correct edit | INV-010 |

Check: all nine UNADDRESSED invariants appear (INV-003 F-05, INV-005 F-13, INV-006 F-02, INV-007 F-27, INV-008 F-14, INV-010 F-28, INV-015 F-15, INV-018 F-08 F-09 F-12, INV-021 F-03).

### `row_coverage` numbers

Method: a read-only script parsed the `row_coverage` list of each card (above `## Blind calibration`) and joined each id to its `source` (parsed or inferred) in `../coverage-matrix.yaml`. Result: matrix 152 ids (126 parsed, 26 inferred); union 152; pairwise overlap 0; no card id outside the matrix; no matrix id missing from the union. This matches the `base-selection.md` coverage check. The only verdict change is INF-019 (inferred) from covered-in-substance to partial.

`per_card_raw` (as the cards state them, before the INF-019 change):

| Card | rows | covered | covered_in_substance | partial | missing | false_match |
|------|------|---------|----------------------|---------|---------|-------------|
| variant-1 | 76 | 65 | 10 | 1 | 0 | 0 |
| variant-2 | 44 | 18 | 15 | 8 | 3 | 0 |
| variant-3 | 32 | 26 | 6 | 0 | 0 | 0 |

`overlaps`: `v1_v2: []`, `v1_v3: []`, `v2_v3: []`. `unique_rows: 152`.

`merged` (after INF-019 becomes partial):

| Scope | rows | covered | covered_in_substance | partial | missing | false_match |
|-------|------|---------|----------------------|---------|---------|-------------|
| parsed | 126 | 97 | 24 | 5 | 0 | 0 |
| inferred | 26 | 12 | 6 | 5 | 3 | 0 |
| union (the `merged` block) | 152 | 109 | 30 | 10 | 3 | 0 |

- `coverage_pct: 0.960` (121 of 126 parsed rows covered or covered in substance; unrounded 0.9603). The rule matches `../coverage-matrix.yaml`, where 0.968 = 122 / 126. The drop of one row is step-1.0a, which V1 found partial (X-005).
- `coverage_pct_union: 0.914` (139 of 152; unrounded 0.9145). The matrix had 0.921 = 140 / 152. Its 12 non-covered union rows (`unmapped_requirements_union`) already include INF-019, so the one-row difference is step-1.0a alone (13 non-covered rows here against 12).

`missing_ids` (3): INF-001 (F-04), INF-008 (F-06), INF-024 (F-05).

`partial_ids` (10): GQ-111 (F-04), GQ-112 (F-04), GQ-113 (F-04), SP-28 (F-05), step-1.0a (F-03), INF-005 (F-06), INF-017 (F-18, F-19), INF-018 (F-06), INF-019 (F-03), INF-020 (F-03).

`false_match_ids`: none.

`caveats`: (1) delegated rows are covered only if the delegate item runs as written; (2) V1 rows are item-checked with unreliable second refs (41 discarded); (3) 21 V3 rows rest only on "T1 matrix row" and are tagged [INFERRED], not independently confirmed; (4) the slices are disjoint by brief, so per-card counts measure brief width, not reviewer quality (S-001).

### `best_practice_grade`

- `grade: 3`, `scale: "0 to 5 (0 = unusable, 5 = executable as written with no rework)"`, V3's written scale (S-008).
- `card_grades: {variant-1: 4, variant-2: 3, variant-3: 4}`, recorded but not ranked (A-007).
- Reasons: plus, owner gates and HALT rules are explicit and the R5 edit has its own review gate; plus, the design-fix items anchor on headings and pinned counts. Minus, two checks fail correct work (F-01, F-02), so the plan needs rework before it runs as written; minus, an owner approval at step 1.0a has no follow-up path today (F-03, INV-021). The card grades of 4 were set before INV-006 was found.

### `calibrated_confidence`

- `value: 0.77`, `inputs: {variant-1: 0.71, variant-2: 0.81, variant-3: 0.79}`, `mean_exact: 0.7700` (2.31 / 3), read from `../reviewer-cards/reviewer-{1,2,3}-card-calibrated.yaml` line 19 of each.
- Note: mean of the three calibrated card confidences. F-01 is held by one card and confirmed by all three advocates; F-02 comes from the probe alone, but its evidence is mechanical (a grep count re-checked by the orchestrator).

## Review Status

- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T14:41Z
- Status: auto-approved, pending review. The caller may run a plan review before Step 5 (run 1 used `refactor-plan-review.md`). The merge executor must apply Changes 1 to 30 in order, and must copy the F-02 grep pattern and the F-03 branch wording exactly.

## Fix cycle 1

- Date: 2026-11-08. Source: `refactor-plan-review.md` (VERDICT: FAIL, B-01 blocking, M-01 to M-07 minor). Only this plan was edited. F-01, the F-02 pattern, every severity and every coverage number are unchanged.
- B-01 (Change 3, step 1, step 3 and success test): step 1 now writes a decision file `phase-outputs/plans/OQ-<n>-<topic>-decision.md` in the TL 1142 form (`needs_human_decision: true`, `status: PENDING`, question, options, and the empty `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:` block), then appends a PENDING Execution Log row for 7.17 and HALTs before step 1.2 under TL 1142 Branch 1. The OQ-8 field names "Given by, Source" are gone. Step 3 now resumes by filling that decision file and applying TL 1142 Branch 2 over it. The success test now checks the decision file exists with `status: PENDING`, the single PENDING row for 7.17 and the HALT.
- M-01 (Change 3, step 3): the refusal path no longer cites INV-016. It cites INV-021's sentence "If the owner declines, the plan works", records the refusal in `1.0a-facts.md` as "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies", and states what 8.10 then does: keeps `ALLOWED_ORCA` at exactly 10, does not page by the cursor field, and treats a full page as truncated with a lower-bound total.
- M-03 (Change 2 Risk, and the `not_carried` row "INV-006 options"): the false claim that dropping the append removes a per-item row TL 2804 requires is replaced. TL 2804 asks for one row per decision and TL 2802 already is that row; the chosen fix is kept because it leaves item 6.2 a checkable action, with the 6.2 row as an item-level record next to the build-time row.
- M-04 (Change 2): one note added under F-02: run the pattern with plain `grep`, never `-E`, and separate the appended row's cells with ` | `.
- M-07 (Changes NOT Being Made): three `not_carried` rows added for INV-001, INV-002 and INV-017, each ADDRESSED, LOW, no gap, with the probe's evidence as the rationale.
- M-02, M-05, M-06: left as review notes, not applied in this cycle, as the caller directed.

# Refactoring Plan: Merge into Base (Variant 2)

## Overview
- Base: Variant 2 (`variant-2-original.md`, reviewer-2, qa persona, haiku), selected in `base-selection.md` (0.7809 vs 0.7665, debate tiebreaker 8 of 14 points).
- Incorporating from: Variant 1 (`variant-1-original.md`, reviewer-1, analyzer persona, sonnet), the Round 2 consensus (debate-transcript.md), and the Round 2.5 invariant probe (invariant-probe.md).
- Planned changes: 31 (5 corrections to base findings, 11 incorporations from Variant 1, 2 new LOW findings, 12 invariant findings, 1 card-level update).
- Risk level: Medium overall. The merge itself is additive and low risk; the merged card carries two HIGH findings no card reviewer verified (INV-001, INV-010), and INV-010 cannot be closed without an owner ruling.
- Debate status carried in: BLOCKED_BY_INVARIANTS (INV-001, INV-010 HIGH UNADDRESSED; Round 3 unavailable at depth standard), so both are incorporated as HIGH findings as the convergence assessment directs.
- Class vocabulary for the merged card: the four taxonomy classes only (Regression, Drift, Authorized expansion, Necessary deviation). "coverage-gap" is not a class; missing tests and missing rules are written `class: Drift` with `subtype: coverage gap` (Round 2, Variant 2 rebuttal, disputed row 1, agreed).
- Ordering rule for the merged `findings:` list: HIGH, then MEDIUM, then LOW; inside a severity, by lowest plan task number touched. Ids keep their origin (QA-NNN from V2, Fn from V1, INV-NNN from the probe); the two new findings take M-01 and M-02.

### Resulting merged finding set (target state)

| Sev | Id | Class | Task(s) | One-line summary |
|---|---|---|---|---|
| HIGH | QA-001 | Regression | 2 | Hunk-less findings deferred at every review, so review 1 can PASS falsely |
| HIGH | INV-010 | Drift (provisional; needs owner ruling) | 2, 12 | `proxy_all` drops review-2 deferrals, demotions and withdrawals |
| HIGH | INV-001 | Drift | 4 | Replay re-reads a report the command has edited, so `begin` review 2 exits 6 |
| MEDIUM | INV-007 | Drift | 1 | No stale-lock rule |
| MEDIUM | INV-027 | Drift (subtype: coverage gap) | 2 | No review-1 FINDING grammar without `hunk=`; `origin=` undefined at review 1 |
| MEDIUM | INV-011 | Drift | 2 | `at=` numbering for `side=old` undefined |
| MEDIUM | INV-018 | Drift | 2 | `FINDINGS none` "single line" wording blocks the PRIOR-plus-none PASS path |
| MEDIUM | INV-021 | Drift | 2 | C2b written `R<k>.<j>` (any review) instead of `R<N>.<j>` |
| MEDIUM | QA-002 | Drift (subtype: coverage gap) | 4 | `deferred.md` disclosure sentence assigned to no task |
| MEDIUM | INV-002 | Drift | 4 | Replay of a degraded check not specified |
| MEDIUM | INV-003 | Drift | 4 | `fix-rejected` has no status or halt slot |
| MEDIUM | INV-006 | Drift (subtype: coverage gap) | 4 | Step-order guards only on `begin` |
| MEDIUM | F1 | Drift (subtype: coverage gap) | 5, 6, 10 | Severity-rule test never reads the untracked new files |
| MEDIUM | F2 | Drift | 5 | Verbatim table vs added `proxy_all` text |
| MEDIUM | QA-005 (+F4) | Drift | 6, 7 | Diffgate bullets promised pinned but unpinned; drift guard lacks exemptions |
| MEDIUM | INV-024 | Drift | 6, 7 | Diffgate bullet 4 single-path lookup breaks plan:21; pinning freezes it |
| MEDIUM | QA-004 | Drift (subtype: coverage gap) | 12 | No scoring branch for an early PASS |
| MEDIUM | INV-029 | Drift | 12 | Early-PASS scoring redefines `R3-proxy-all` without owner confirmation |
| LOW | F8 | Drift | 1 | Stubs vs one-JSON-object and exit 2/3 ACs |
| LOW | M-02 | Drift (subtype: coverage gap) | 1 | Exclusive-create lock untested |
| LOW | F3 | Drift | 5 | Source of Task 5's expected verbatim blocks unspecified |
| LOW | F10 | Drift (subtype: coverage gap) | 10 | No lint step for the new Python files |
| LOW | F9 | Authorized expansion | 11, 12 | Pre-run gate and T11 text exceed the plan:19 scope line |
| LOW | F5 | Drift | 12 | T10 template for a step the design never runs |
| LOW | F6 | Drift | 12 | Reviser line placed after "Finish with worker_done" |
| LOW | F7 | Drift (subtype: coverage gap) | 12 | README lacks the blindness-audit exemption |
| LOW | M-01 | Drift (subtype: coverage gap) | 12 | No check that briefs never pass `--unattended` |
| advisory | ADV-1 | (advisory) | 4 | 35-case floor can be met by parametrization |

Totals: 3 HIGH, 15 MEDIUM, 9 LOW, 1 advisory. QA-003 leaves the findings list (Change 3).

## Planned Changes

### Part A: Corrections to base findings (Round 2 consensus)

### Change 1: Reclassify QA-001 as Regression, HIGH
- **Source**: Round 2 consensus (V1 rebuttal "QA-001 HIGH Regression"; V2 rebuttal "All-Drift conceded for QA-001, now Regression").
- **Target**: Base `findings:` QA-001 (replace `class: Drift` with `class: Regression`; severity HIGH unchanged).
- **Integration approach**: Edit the class field. Append to `evidence:` `source.md:275` (open question 5, "never blocking after review 1") and to `finding:` one sentence: "source.md:154 is a test-case list, not the rule; the rule at source.md:29, :40, :149 limits deferral to review 2 on." Add to `fix:` a cross-reference "see INV-027 for the review-1 grammar this fix also needs."
- **Rationale**: Debate C-004 (95%), C-005 synthesis (80%); taxonomy precedence: the plan's C6 at plan:49 drops "from review 2", contradicting an explicit spec constraint (source.md:149), which is Regression even if source.md:154 repeats the wording.
- **Risk**: Low. Label change on a verified finding.

### Change 2: Relabel QA-002 as Drift (subtype: coverage gap)
- **Source**: Round 2, V2 rebuttal disputed row 1 (list includes QA-002), agreed.
- **Target**: Base QA-002 (insert `subtype: coverage gap`; severity MEDIUM unchanged).
- **Integration approach**: Add the subtype field. Extend `fix:` with "written by `diffgate.py` into `deferred.md` (a Task 4 AC), not added to the command's Close text, so the Diffgate bullet 6 pin (Change 5) stays verbatim" (the placement constraint of INV-025, LOW, which this fix already implies).
- **Rationale**: A missing AC is Drift / coverage under the taxonomy; INV-025 shows the fix has one safe location.
- **Risk**: Low.

### Change 3: Remove QA-003 from the plan audit; keep it as a note on the coverage artifact
- **Source**: Round 2, V2 rebuttal ("QA-003 conceded (drop from the plan audit; note on the coverage artifact only)"); V1 rebuttal ("QA-003 dropped from the plan audit").
- **Target**: Base QA-003 (delete from `findings:`); base `notes:` (append).
- **Integration approach**: Append to `notes:` one item: "Coverage artifact (not a plan finding): `reflect-1/artifacts/coverage-matrix.json:230-239` has no rows for checker rules C1-C12 (source.md:149), input limits (source.md:133) or ledger locking, atomic replace and symlink refusal (source.md:144); the plan covers them in Tasks 1-4 (plan:37, :42, :49). Add atomic inferred rows and recompute the 28/35 figure." Remove the QA-003 entry from `calibration.per_finding`.
- **Rationale**: Debate S-004 (90%); calibrator "Flaw in the coverage artifact, not the plan"; removes the base's only internal contradiction (IC).
- **Risk**: Low. Information kept, only its target corrected.

### Change 4: Relabel QA-004 as Drift (subtype: coverage gap); cross-reference INV-029
- **Source**: Round 2, V2 rebuttal disputed row 1 (QA-004 listed), agreed.
- **Target**: Base QA-004 (insert `subtype: coverage gap`; MEDIUM unchanged).
- **Integration approach**: Add the subtype. Append to `fix:` "The value read for an early terminal review is the owner's call (INV-029, source.md:280); until ruled, README must state the open question instead of picking a value." Keep "never fabricate result-r3.json".
- **Rationale**: Debate C-002 (80%); calibrator "Fix proposal is a guess"; INV-029 shows the fix alone would redefine the bar metric.
- **Risk**: Low.

### Change 5: Merge F4 into QA-005 with the corrected exception list
- **Source**: V1 F4 (Usage exemption) + base QA-005; Round 2 X-001 (V2 wins, 95%) and C-001 (V2, 90%; "F4's Usage point merges in").
- **Target**: Base QA-005 (replace `finding:` and `fix:`; add `F4` to a new `merged_from:` field; MEDIUM, Drift).
- **Integration approach**: `finding:` keeps QA-005's text and adds: "Task 7's drift guard ('every other `## ` section equals the parent's', plan:110) also does not exempt the edited `## Usage` section (spec-panel.md:19-24, token replaced per plan:97), so as written it fails on a correct variant." `fix:` becomes: "Extend Task 7 to pin all six `## Diffgate` bullets character for character, plus a negative test that changes one behavioral clause of a Diffgate bullet (not only Review Loop bullet 3, plan:114). State the drift-guard exceptions explicitly: (a) `## Usage`, compared after the `--re-review ... --baseline ...` token is replaced by `--diffgate-dir ...`; (b) `## Review Loop`, pinned by the seven-bullet check instead; (c) `## Diffgate`, a new section with no parent counterpart, pinned by the six-bullet check this fix adds (exempt only because, and only once, that check exists); (d) `## Tool Coordination`, equal after removing the release-spec template clause from the `**Read**` bullet; (e) `## Unattended mode`, asserted absent. Resolve INV-024 before pinning bullet 4." Citations: plan:103, :110, :114; source.md:86-96; spec-panel.md:19-24.
- **Rationale**: F4's original list ("Review Loop and Diffgate pinned by bullet checks") was wrong when written (X-001, conceded by V1); after the QA-005 fix it is true, so the corrected list states the dependency. The negative-case extension comes from INV-031 (LOW) and is part of QA-005's own fix wording ("a negative test on one behavioral clause").
- **Risk**: Medium. Two findings fused; the exemption list must match the plan's section set exactly, or the guard either fails a correct file or exempts an unpinned one.

### Part B: Incorporations from Variant 1

### Change 6: Add F1 as Drift (subtype: coverage gap), MEDIUM
- **Source**: V1 F1; Round 2 V1 rebuttal (raised to HIGH) and V2 rebuttal (MEDIUM); A-005 REJECT (95%).
- **Target**: Base `findings:` (insert, MEDIUM block).
- **Integration approach**: Copy F1 with `class: Drift`, `subtype: coverage gap`, `severity: MEDIUM`, citation `[plan:89, plan:104, plan:149, plan:25, tests/skills/test_review_severity_rule.py:28-51]`. Detail adds that test_a (172), test_f (320), test_i (448) and test_k (506) read through `_tracked_text`. Fix: "Before the severity-rule test in Tasks 5, 6 and 10, run `git add -N` on the new `src/` files (never `.claude/`); `tests/` is not in `_SCAN_TREES` (line 28), so marking it is unnecessary. Put the step in each AC."
- **Severity decision (open in Round 2): MEDIUM.** V1 argued HIGH (the plan's own ACs and the plan:25 constraint are never enforced). V2 argued MEDIUM because PR CI catches it. Verified: `.github/workflows/test.yml` triggers on `pull_request` to master and integration (lines 3-7) and line 47 runs the full `pytest -v ... -n auto` suite, ignoring only `tests/cli/test_verify_sync_hooks.py`; once the files are committed they are tracked, so a banned phrase fails PR CI before merge. The defect is therefore a false green inside the plan's own runs that costs a late post-commit fix cycle; it cannot ship a wrong result. The merged card keeps HIGH for defects that produce wrong delivered behaviour (QA-001 false PASS, INV-001 voided replicates). The fix is kept in full because the plan's ACs are meant to be the gate, not CI.
- **Rationale**: U-001 (High value), A-005; Round 2 Disputed row 2.
- **Risk**: Low.

### Change 7: Add F2 as Drift, MEDIUM
- **Source**: V1 F2; Round 2 (F2 is the plan contradicting itself, plan:83 vs :86: Drift, not Regression).
- **Target**: Base `findings:` (insert).
- **Integration approach**: Copy F2 with `class: Drift`; keep its fix ("Keep the table verbatim and define proxy_all in a sentence directly under it; test both separately"). Note that INV-026 confirms the F2 and F3 fixes work together.
- **Rationale**: Debate C-003 (V1, 75%); U-002.
- **Risk**: Low.

### Change 8: Add F3 as Drift, LOW
- **Source**: V1 F3 (MEDIUM in V1); Round 2 merged card row "F3 LOW Drift" (V1 rebuttal), accepted by V2 rebuttal.
- **Target**: Base `findings:` (insert, LOW block).
- **Integration approach**: Copy F3 with `severity: LOW`; drop the hedge "may be absent in CI" and state the verified premise only: "source.md moves to `.dev/tasks/done/` on archive (plan:110 already embeds Task 7's expected text in the test file; plan:86 says nothing for Task 5)." Keep the fix.
- **Rationale**: U-003; consensus severity.
- **Risk**: Low.

### Change 9: Add F5 as Drift, LOW, narrowed
- **Source**: V1 F5; calibrator `partial` ("plan:172/174 already flag T10 as a coordinator decision"); V1 Round 1 concession.
- **Target**: Base `findings:` (insert).
- **Integration approach**: Copy F5 and add to `finding:` "plan:172 and :174 already route T10 to the coordinator; the residual gap is that the template ships ready to dispatch." Fix: "Keep T10 only under `briefs/source/`, or keep `T10-R3-reviser.txt` with a first-line README marker that it is excluded from the diffgate arm unless the coordinator rules otherwise."
- **Rationale**: U-005 (Low); C-002 (QA-004 wins the area; F5 kept as a separate, smaller defect).
- **Risk**: Low.

### Change 10: Add F6 as Drift, LOW, retitled
- **Source**: V1 F6; calibrator "badly placed, not ambiguous"; V1 Round 1 concession.
- **Target**: Base `findings:` (insert).
- **Integration approach**: Title "Reviser line is appended after the 'Finish with worker_done' instruction (placement)". Fix: "Insert the line immediately before 'Finish with worker_done', as one line, and make the Task 12 diff AC (plan:178) match that position."
- **Rationale**: U-006; removes the V1 F6 internal contradiction.
- **Risk**: Low.

### Change 11: Add F7 as Drift (subtype: coverage gap), LOW
- **Source**: V1 F7; Round 2 (not Regression: a missing validity rule; V2 rebuttal "The F7 conflict originates in the spec (source.md:209 vs :229); LOW holds").
- **Target**: Base `findings:` (insert).
- **Integration approach**: Copy F7 with the new class and subtype; add `source.md:209` to the citation. Keep the fix (one README sentence exempting the separate blindness-audit session).
- **Rationale**: U-007; Round 2 consensus.
- **Risk**: Low.

### Change 12: Add F8 as Drift, LOW
- **Source**: V1 F8; calibrator `partial` ("main() validating before dispatch resolves it").
- **Target**: Base `findings:` (insert).
- **Integration approach**: Copy F8; order the fix so the calibrator's resolution comes first: "Run limit and read validation in `main` before dispatch, so the exit 2/3 ACs of Task 1 pass while bodies are stubs; stubs print `{ok:false, exit:2, message:\"not implemented\"}`."
- **Rationale**: U-008.
- **Risk**: Low.

### Change 13: Add F9 as Authorized expansion, LOW, with the Round 2 fix
- **Source**: V1 F9; Round 2 V2 rebuttal disputed row 3 ("fix is to amend the plan:19 scope line ... drop the 'base commit unverified' claim"), agreed.
- **Target**: Base `findings:` (insert).
- **Integration approach**: Title "Tasks 11 and 12 take section 5 content (pre-run gate, T11 blindness-audit text) beyond the plan:19 scope line". Citation `[plan:19, plan:155, plan:173, source.md:201, source.md:209]`. Fix: "Amend the plan:19 scope line to name the section 5 pre-run gate (Task 11) and the T11 blindness-audit brief (Task 12) as in scope." Delete every mention of base commit `2cb683f5` being unverified (source.md:199 names it).
- **Rationale**: C-006 (V1, 85%); A-009 ACCEPT; Round 2 disputed row 3.
- **Risk**: Low.

### Change 14: Add F10 as Drift (subtype: coverage gap), LOW
- **Source**: V1 F10; calibrator note "F10 is an omitted step".
- **Target**: Base `findings:` (insert).
- **Integration approach**: Copy F10 with the new class and subtype; keep the fix (`make lint` on the new files in Task 10, output under `./artifacts/`).
- **Rationale**: U-010.
- **Risk**: Low.

### Change 15: Add the 35-case floor as advisory ADV-1
- **Source**: V1 `correctness_gaps_advisory`; merged card row "35-test floor LOW advisory"; INV-014 ADDRESSED.
- **Target**: Base, new top-level block `correctness_gaps_advisory:` after `findings:`.
- **Integration approach**: One item: "ADV-1: Task 4 turns source.md:242's 'about 35' into a hard floor (plan:77); parametrization can meet it without new coverage. Count distinct behaviours, or keep the number as a guide."
- **Rationale**: U-011 (Low).
- **Risk**: Low.

### Change 16: Add V1's `confirmed_ok` block
- **Source**: V1 `confirmed_ok` (7 items).
- **Target**: Base, new top-level block `confirmed_ok:` after `correctness_gaps_advisory:`.
- **Integration approach**: Copy the seven items verbatim (spec-panel.md anchors; single `src/superclaude` string at line 220; routing-refresh lines 33 and 648; worker-contract counting at 831-839; `list_available_skills()` at install_skill.py:115; loader pattern at test_workflow_archive.py:22-28; T07/T09 phrase counts).
- **Rationale**: S-002 (V1, 85%): re-checkable positive anchors the base lacks.
- **Risk**: Low. Anchors were true at audit time; the merge copies them, it does not re-verify them.

### Part C: New findings from the debate

### Change 17: Add M-01 "No check that briefs never pass `--unattended`", LOW
- **Source**: Round 2 V1 rebuttal new evidence ("plan:133, plan:155, plan:173 say no brief passes --unattended, but no acceptance check asserts it"); V2 Round 1 A-008 QUALIFY; INV-009 ADDRESSED by this row.
- **Target**: Base `findings:` (insert, LOW).
- **Integration approach**: `class: Drift`, `subtype: coverage gap`, citation `[plan:29, plan:133, plan:155, plan:173, plan:178]`. Finding: "The variant has no `## Unattended mode` section and the plan's residual (plan:29) holds only if no brief passes `--unattended`; no AC asserts it." Fix: "Add a Task 12 AC: `grep -l -e '--unattended' .dev/brainstorms/346-diffgate/briefs/*.txt` prints nothing; save the output under `./artifacts/`."
- **Rationale**: Merged card row "new --unattended assertion LOW", agreed in Round 2.
- **Risk**: Low.

### Change 18: Add M-02 "Exclusive-create lock untested", LOW
- **Source**: Base calibrator `unraised_gaps` ("plan:42 tests symlink refusal but not the exclusive-create lock"); U-017; merged card row "exclusive-create lock untested LOW".
- **Target**: Base `findings:` (insert, LOW); remove the item from `calibration.unraised_gaps` (now raised).
- **Integration approach**: `class: Drift`, `subtype: coverage gap`, citation `[plan:37, plan:42, source.md:144]`. Fix: "Add a Task 1 AC: with the lock file present, `save_ledger` fails without writing the ledger or leaving a temp file." Cross-reference INV-007 (the recovery rule this test does not supply).
- **Rationale**: Consensus row.
- **Risk**: Low.

### Part D: Invariant findings (Round 2.5)

Fix wording: the probe states explicit fixes for INV-001 and INV-010. For the other ten, the fix below is derived from the gap the probe's Assumption and Evidence columns state, and is marked "fix direction" where the plan author must pick a concrete rule.

### Change 19: Add INV-001 as HIGH: replay re-reads an edited report
- **Source**: invariant-probe.md INV-001 (HIGH UNADDRESSED, blocking).
- **Target**: Base `findings:` (insert, HIGH block, after INV-010 per the ordering rule).
- **Integration approach**: `class: Drift`, citation `[plan:71, plan:74, source.md:18, source.md:26, source.md:82, source.md:95, source.md:143, source.md:229]`. Finding: "`begin` for review N+1 replays the recorded check (plan:71; source.md:143 're-run check on the recorded report'), but the command appends `verdict_line` and adds the Reviser brief to the report after `check`, and the `<dir>` file list keeps no copy. A replay that re-reads the report path mismatches and exits 6 on every normal loop at review 2; exit 6 voids the replicate (source.md:229). plan:74 tests exit 6 only for a hand-edited ledger." Fix (probe): "Store the accepted report bytes (in the ledger or `<dir>`) and replay those; add a subprocess test that appends the verdict line and a Reviser brief to the report before `begin --expect-round 2` and asserts exit 0."
- **Rationale**: Convergence assessment: blocking items "incorporated into the merged card as HIGH findings". Neither card nor the debate raised it.
- **Risk**: Medium. No card reviewer or calibrator checked it; the merged card must label its provenance ("raised by the Round 2.5 probe, not calibrator-verified").

### Change 20: Add INV-010 as HIGH, needs owner ruling: `proxy_all` scope
- **Source**: invariant-probe.md INV-010 (HIGH UNADDRESSED, blocking).
- **Target**: Base `findings:` (insert, HIGH block).
- **Integration approach**: `class: Drift` with `needs_owner_ruling: true` and the note "provisional class: Regression if the owner rules that review-2 deferrals, demotions and withdrawals count at review 3 (then plan:49 contradicts the plan:26 owner decision); withdrawn if the owner confirms review-3-only counting (then plan:49 matches source.md:204)". Citation `[plan:26, plan:49, plan:53, source.md:12, source.md:29, source.md:204, source.md:220, source.md:253, source.md:280]`. Finding: "`proxy_all` counts only findings first raised in review 3 and priors marked in review 3. A blocker declined in cycle 1 and withdrawn at review 2, a CRITICAL deferred at review 2, or a MAJOR demoted at review 2 leaves `R3-proxy-all`, which is the route the spec says the proxy closes ('the proxy sees both', source.md:253)." Fix (probe): "Get an owner ruling on whether review-2 deferrals, demotions and withdrawals count at review 3; if they do, make the count cumulative across reviews and add a test where a review-2 withdrawal is counted at review 3." Execution of Tasks 2, 4 and 12 waits on that ruling.
- **Rationale**: Convergence assessment (blocking); caller instruction (mark needs owner ruling). source.md:280 already asks the owner to confirm the counting function before any run.
- **Risk**: High. The card cannot settle it; the class and the fix depend on a decision outside this pipeline.

### Change 21: Add INV-002 as MEDIUM: replay of a degraded check
- **Source**: invariant-probe.md INV-002.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, citation `[plan:71, plan:74, source.md:262]`. Fix direction: "Record the attempt number and `degraded` state with the accepted check and replay with them, so a degraded acceptance replays as degraded; add a test that degrades a review, then runs `begin --expect-round 2` and asserts exit 0."
- **Rationale**: Probe MEDIUM UNADDRESSED (warning).
- **Risk**: Low. Depends on Change 19's stored-copy design; the merged card should list INV-001 as related.

### Change 22: Add INV-003 as MEDIUM: `fix-rejected` has no state slot
- **Source**: invariant-probe.md INV-003.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, citation `[plan:71, plan:74, source.md:27, source.md:239]`. Fix direction: "Map `fix-rejected` to a terminal state: `status` reports `closed` with `halt: escalate` (source.md:27, 'stop the reviser and escalate without spending a review'), and the next `begin` exits 4; extend the plan:74 AC to assert both."
- **Rationale**: Probe MEDIUM UNADDRESSED.
- **Risk**: Low.

### Change 23: Add INV-006 as MEDIUM: step-order guards beyond `begin`
- **Source**: invariant-probe.md INV-006.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, `subtype: coverage gap`, citation `[plan:71, plan:74, source.md:49, source.md:112]`. Fix direction: "State and test that a second `check` after an accepted check for the same review exits 5 (a softer report cannot overwrite an accepted FAIL), `fixcheck` before an accepted check exits 5, and `check` with no ledger exits 5."
- **Rationale**: Probe MEDIUM UNADDRESSED.
- **Risk**: Low.

### Change 24: Add INV-007 as MEDIUM: no stale-lock rule
- **Source**: invariant-probe.md INV-007.
- **Target**: Base `findings:` (insert, MEDIUM; related: M-02).
- **Integration approach**: `class: Drift`, citation `[plan:37, plan:42, source.md:144, source.md:254, source.md:264]`. Fix direction: "Define a stale-lock rule (for example, the lock file records the holder's pid and a lock whose pid is not running is removed and reported in the JSON message), make `status` name a held lock and the recovery command, and test it."
- **Rationale**: Probe MEDIUM UNADDRESSED; a worker killed mid-write would otherwise stall every later call, and a stall costs a replicate (source.md:254, :264).
- **Risk**: Low.

### Change 25: Add INV-011 as MEDIUM: `at=` numbering for `side=old`
- **Source**: invariant-probe.md INV-011.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, citation `[plan:41, plan:49, plan:52, source.md:125, source.md:149]`. Fix direction: "State in Task 2 that with `side=old`, `at=` is 1-based inclusive over `doc-r<N-1>.md`, and C4 and C5 check against that file; add a check-level test with a `side=old` finding on a pure deletion."
- **Rationale**: Probe MEDIUM UNADDRESSED.
- **Risk**: Low.

### Change 26: Add INV-018 as MEDIUM: PASS path at re-review unreachable as worded
- **Source**: invariant-probe.md INV-018.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, citation `[plan:49, plan:52, source.md:94, source.md:125, source.md:149, source.md:215, source.md:217]`. Fix direction: "Reword 'the single line `FINDINGS none`' so it replaces only the FINDING lines and PRIOR lines remain required; add a review-2 test with every prior `resolved` plus `FINDINGS none` that is accepted with verdict PASS."
- **Rationale**: Probe MEDIUM UNADDRESSED; the clean PASS is a bar alternative (source.md:215, :217).
- **Risk**: Low.

### Change 27: Add INV-021 as MEDIUM: C2b scope
- **Source**: invariant-probe.md INV-021.
- **Target**: Base `findings:` (insert, MEDIUM).
- **Integration approach**: `class: Drift`, citation `[plan:49, source.md:39, source.md:81, source.md:149]`. Finding notes plan:49 writes "an `R<k>.<j>` id in the prose" (any review) where source.md:149 writes "every `R<N>.<j>` token" (current review). Fix direction: "Scope C2b to ids of the current review (`R<N>.<j>`, as source.md:149 writes) and add a test where re-review prose names a prior minor id and a prior blocking id and is accepted."
- **Rationale**: Probe MEDIUM UNADDRESSED; a false structural failure counts toward `invalid` (source.md:39).
- **Risk**: Low.

### Change 28: Add INV-024 as MEDIUM: Diffgate bullet 4 dual-surface lookup
- **Source**: invariant-probe.md INV-024.
- **Target**: Base `findings:` (insert, MEDIUM; must be resolved before the Change 5 pin).
- **Integration approach**: `class: Drift`, citation `[plan:21, plan:103, source.md:91, source.md:94]`. Fix direction: "In Task 6, write Diffgate bullet 4 to name `~/.claude/skills/sc-diffgate/SKILL.md` first, then the project `.claude/skills/sc-diffgate/SKILL.md` copy, as plan:21 requires and bullet 1 already does; record it as a Necessary deviation from source.md 3.1 item 5; Task 7 pins the amended text."
- **Rationale**: Probe MEDIUM UNADDRESSED; pinning the source text would make the plan:21 violation permanent.
- **Risk**: Medium. It changes text the plan says to copy verbatim; the coordinator may prefer a ruling over a silent deviation.

### Change 29: Add INV-027 as MEDIUM: review-1 FINDING grammar
- **Source**: invariant-probe.md INV-027 (sufficiency challenge to QA-001's fix).
- **Target**: Base `findings:` (insert, MEDIUM; related: QA-001).
- **Integration approach**: `class: Drift`, `subtype: coverage gap`, citation `[plan:49, source.md:120, source.md:125, source.md:149]`. Fix direction: "Define the review-1 FINDING form in Task 2: `hunk=` omitted (review 1 has no hunks) and `origin=` fixed or omitted at review 1; C2 accepts it at review 1 only; the QA-001 review-1 end-to-end test uses this form."
- **Rationale**: Probe MEDIUM UNADDRESSED; without it the QA-001 fix leaves every review-1 finding failing C2.
- **Risk**: Low.

### Change 30: Add INV-029 as MEDIUM: early-PASS scoring needs owner confirmation
- **Source**: invariant-probe.md INV-029 (sufficiency challenge to QA-004's fix).
- **Target**: Base `findings:` (insert, MEDIUM; related: QA-004, INV-010).
- **Integration approach**: `class: Drift`, citation `[plan:174, source.md:204, source.md:206, source.md:215, source.md:223, source.md:280]`. Fix direction: "Put the early-PASS case (scoped or clean PASS at review 1 or 2) in the same owner confirmation as INV-010 (source.md:280); README states the ruled value of `R3-proxy-all` for an arm that closed early, and carries growth forward only as source.md:206 allows."
- **Rationale**: Probe MEDIUM UNADDRESSED; reading review 2's `proxy_all` would quietly redefine the bar metric.
- **Risk**: Low.

### Part E: Card-level update

### Change 31: Update header, notes, calibration and verdict
- **Source**: Round 2 consensus; convergence assessment; both calibrators.
- **Target**: Base header, `notes:`, `calibration:`, `verdict:`.
- **Integration approach**:
  - `reviewer: merged (reviewer-2 base + reviewer-1)`; keep `persona`, `model_class` per origin in a `provenance:` list (QA-NNN reviewer-2 haiku; Fn reviewer-1 sonnet; INV-NNN Round 2.5 probe; M-01 Round 2; M-02 reviewer-2 calibrator).
  - `notes:` keep the base items; add "Merged by /sc:adversarial Mode A; status BLOCKED_BY_INVARIANTS (INV-001, INV-010)" and the QA-003 note from Change 3.
  - `calibration.per_finding`: keep the base entries for QA-001, QA-002, QA-004, QA-005; add V1's calibrator entries for F1, F2, F3, F5-F10 and F4 (under QA-005); mark INV-NNN, M-01 "not calibrator-verified (probe/debate)". Drop `unraised_gaps` (now M-02).
  - `self_confidence`: drop the per-reviewer values (0.94, 0.78); a merged card has no single self-grade. Keep both `calibrated_confidence` values under `provenance:`.
  - `verdict: refactor`, with `verdict_note: "Every finding is fixable by editing plan text or ACs; Tasks 2, 4 and 12 must not execute until the owner rules on INV-010 and INV-029 (source.md:280)."`
- **Rationale**: A-001 (agreed ACCEPT, refactor holds); convergence status; caller's final-verdict instruction.
- **Risk**: Low.

## Base Weaknesses and the Better Variant

| Base weakness | Better variant / source | Fixed by |
|---|---|---|
| QA-001 classed Drift | Round 2 consensus (both rebuttals) | Change 1 |
| QA-003 audits the coverage artifact, not the plan | V1 (S-004, 90%) | Change 3 |
| No finding on test-harness integrity (A-005 contradicted) | V1 F1 | Change 6 |
| Task coverage 5 of 12; no finding on Tasks 1, 3, 5, 8-11 | V1 (C-008, breadth) | Changes 6-14 |
| No positive-verification anchors | V1 `confirmed_ok` (S-002, 85%) | Change 16 |
| No assessment of plan-added content | V1 F9 (C-006, 85%) | Change 13 |
| Over-confident self-grade (0.94 vs calibrated 0.85) | V1 calibration error 0.03 (C-007, 85%) | Change 31 |
| QA-004 fix "a guess" | Probe INV-029 | Changes 4, 30 |
| QA-001 fix insufficient alone | Probe INV-027 | Changes 1, 29 |
| No coverage of replay, `proxy_all` scope, guards, locks | Probe INV-001, -010, -002, -003, -006, -007 | Changes 19-24 |

## Changes NOT Being Made (with rationale)

| Diff Point / Item | Non-Base or Alternative Approach | Rationale |
|---|---|---|
| F1 severity | HIGH (V1 Round 2 rebuttal) | PR CI (`.github/workflows/test.yml:3-7, :47`) runs the full suite on tracked files before merge; the defect delays detection but ships nothing wrong. MEDIUM, fix kept (Change 6). |
| F1, F2, F7 class | Regression (V1 original) | Conceded by V1 (Round 2): a vacuous test, a self-contradiction and a missing validity rule do not contradict an AC, spec constraint or previously passing test. |
| Class label | "coverage-gap" as a class (V1 Round 2 merged card) | Not one of the four taxonomy classes; written as Drift with subtype coverage gap (Round 2 disputed row 1). |
| F9 remediation | "documentation note" (V1 Round 2); "list in Constraints, mark T11 as draft" (V1 original) | Authorized expansion carries no documentation-note remedy; the agreed fix amends the plan:19 scope line (Round 2 disputed row 3). |
| F9 claim | "base-commit 2cb683f5 classification claim unverified" | source.md:199 names the commit; claim dropped. |
| F4 original fix | "Review Loop and Diffgate pinned by bullet checks" as an existing fact | False at plan:110 (X-001, 95%); replaced by the conditional exception list (Change 5). |
| F4 as a separate finding | Keep F4 alongside QA-005 | Same section and fix point (C-001); kept once, as `merged_from: F4` on QA-005. |
| F3 severity | MEDIUM (V1 original) | Consensus row is LOW (V1 rebuttal, accepted by V2). |
| QA-003 as a plan finding | Keep as Drift / coverage gap MEDIUM | Targets the coverage artifact (S-004, 90%; its own calibrator); kept as a note only. |
| V1 `self_confidence` 0.78, V2 0.94 | Carry either as the merged self-grade | A merged card has no single author; both calibrated values kept under provenance. |
| LOW UNADDRESSED invariants INV-004, INV-008, INV-012, INV-013, INV-016, INV-017, INV-020, INV-022, INV-025, INV-028, INV-031, INV-032 | Add each as a LOW finding | Outside the Round 2 consensus and the caller's incorporation list. Partly absorbed where they sharpen an incorporated fix: INV-025 (Change 2 placement), INV-031 (Change 5 negative case). INV-028 (rewrite the plan:52 AC wording) is not added; QA-001's review-1 test exposes the AC conflict. The rest stay in invariant-probe.md for a later pass. |
| ADDRESSED invariants INV-005, -009, -014, -015, -019, -023, -026, -030 | Add as findings | Already covered by QA-001, M-01, ADV-1, QA-004, F1, F2/F3; no new content. |
| V1 advisory as a finding | Promote ADV-1 to LOW | Consensus row says "advisory"; kept in its own block (Change 15). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | QA-001 class wrong | Restore base QA-001 class |
| 2 | Low | Subtype or placement note wrong | Remove subtype and fix sentence |
| 3 | Low | Coverage-matrix observation lost | Restore QA-003 entry from base |
| 4 | Low | Cross-reference wrong | Remove subtype and appended sentence |
| 5 | Medium | Exemption list mismatches plan sections; guard fails a correct file or exempts an unpinned one | Restore base QA-005; re-add F4 separately |
| 6 | Low | F1 severity disputed | Change severity field only |
| 7-14 | Low | Additive LOW/MEDIUM rows | Remove inserted row |
| 15-16 | Low | Additive blocks | Remove block |
| 17-18 | Low | Additive LOW rows | Remove row |
| 19 | Medium | Unverified HIGH finding could be wrong (probe-only provenance) | Downgrade or remove INV-001 after a calibrator check |
| 20 | High | Class and fix depend on an owner ruling not yet given | Keep as needs-owner-ruling; reclassify or withdraw on the ruling |
| 21-27, 29-30 | Low | Additive MEDIUM rows with fix directions the plan author may change | Remove row |
| 28 | Medium | Proposes a deviation from verbatim source text | Replace fix with "coordinator ruling required" |
| 31 | Low | Header or verdict note inaccurate | Restore base header, notes, calibration |

## Review Status
- [x] Auto-approved (default; non-interactive run)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T18:59:26Z
- Review Status: auto-approved 2026-11-08T18:59:26Z

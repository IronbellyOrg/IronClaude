# Refactoring Plan: Merge into Base (Variant 2)

## Overview

- **Base**: Variant 2 (`variant-2-original.md`). sc:reflect-reviewer, persona qa, haiku slot, model `grok-4.7[1m]`.
  - Selected in `base-selection.md`: combined 0.9190 vs 0.9013. The margin was under 5%, so the L1 tiebreaker decided it: V2 won 9 debate points to V1's 3.
- **Incorporating strengths from**: Variant 1 (`variant-1-original.md`; analyzer, sonnet), the debate consensus (`debate-transcript.md:244-249`), and the Round 2.5 invariant probe (`invariant-probe.md`).
- **Merge target (for sc:merge-executor)**: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/adversarial/merged-reviewer-card.md`
- **Planned changes**: 15
- **Changes not being made**: 14 (see the table below)
- **Risk level**: Medium overall. Changes 5-9 rewrite the grounding-gaps artifact and the verifier logic. Everything else is local.

**Verdict invariant (binding on the merge).** The 4-class ledger stays **0 Authorized / 0 Necessary / 0 Drift / 0 Regression**.
- The final status stays `status: partial` + `needs_human_decision: true`.
- No evidence in the debate, the probe or the snapshot supports a classified deviation. Both variants (V1:52, V2:70), every advocate, and INV-013/INV-014 agree.
- No change below may add a row to the deviations table.

**Convergence status (binding disclosure).** The debate ended **BLOCKED_BY_INVARIANTS** (`debate-transcript.md:15, :237`).
- **INV-004 (HIGH) was not addressed in any debate round.** Rounds 1 and 2 ran before the Round 2.5 probe raised it, and depth=standard allows no Round 3 (`debate-transcript.md:239`).
- Change 6 adds the INV-004 correction at this refactor-plan stage. That is a merge-content decision by the orchestrator. It is **not** a debate resolution, and it does **not** clear the block.
- Convergence remains BLOCKED_BY_INVARIANTS until one of two things happens: INV-004 is debated in a later round, or the user explicitly acknowledges it as accepted risk. The merged card must say so (Change 15).
- C-001 also stays a debate-unresolved point. Change 5 records a documented orchestrator decision for it. This does not change the convergence score of 18/19 = 94.7%.

## Planned Changes

### Change 1: Correct the patch line count and the citation ranges (C-002; V2's own factual error)
- **Source**: snapshot `changes.patch` (`wc -l` = 9, re-checked during Step 3). The C-002 combine outcome, agreed at 92% (`debate-transcript.md:138, :170`).
- **Target**: Base, section "T1 challenge", "Challenged" bullet 2 (V2:44) (**replace**).
- **Integration approach**: Replace "`changes.patch` is 10 lines" with "`changes.patch` is 9 lines". Keep these two citations:
  - the whole hunk = `changes.patch:5-9` (line 5 is the `@@ -0,0 +1,4 @@` header);
  - the body = `changes.patch:6-9`.
  
  Keep "Byte-identity of the body still holds." Use only those two forms anywhere the card cites the hunk. Line 7 of the Deviations row already uses `:1-9` for the file plus hunk, so leave it.
- **Rationale**: Both advocates conceded the "10 lines" claim is false (R1 V2-adv concession, `debate-transcript.md:72`). Both scoring passes failed V2 on Correctness-1 partly for it.
- **Risk**: Low. A one-token factual fix.

### Change 2: Reverse the rejection of `tests/__init__.py`; affirm T1 rec 3 as [INFERRED], with INV-010 and INV-012 caveats (C-004, U-004)
- **Source**: C-004 winner V1 (both advocates; the V2 advocate conceded at `debate-transcript.md:73`). Consensus item "Affirm T1 rec 3 as [INFERRED], with `pythonpath = .` as an alternative on pytest 7+" (`debate-transcript.md:248`). INV-010 (MEDIUM). INV-012 (LOW). INV-015 (pytest 7+ for `pythonpath`).
- **Target**: Base, three places, all **replace**: "T1 challenge", "Challenged" bullet 3 (V2:45); Risks row 2 (V2:80); Recommendation 3 (V2:90).
- **Integration approach**:
  - **Bullet 3 becomes**: "T1 recommendation 3 (add `tests/__init__.py`) is valid [INFERRED]. Under pytest's default `prepend` import mode, a `tests/` package marker makes pytest insert the first directory above the package that has no `__init__.py`, which is the project root. That root then resolves `from src.greeting import greet` (`tests/test_greeting.py:1`) as a namespace package, because `src/` has no `__init__.py` (`provenance-manifest.json` scoped inventory)."
  - Add the INV-010 caveats. The fix does **not** hold if any of these is true:
    - (a) there is a root-level `__init__.py`;
    - (b) a regular `src` package elsewhere on `sys.path` shadows the local namespace portion;
    - (c) an unenumerated root config sets `--import-mode=importlib`.
    
    Root-level and `tests/` files were never enumerated, so (a) and (c) stay [INFERRED]-open.
  - Alternative: `pythonpath = .` in a root pytest config. This needs pytest ≥ 7.
  - Add the INV-012 caveat. Either file is new work outside the 8 hashed snapshot files that maps to no task (`completed.md:6-8`). Tests run after applying it run on a tree that differs from the audited one. The change must be recorded (task log or attestation), and the R-003 result must be attributed to that tree.
  - **Rec 3 becomes**: "Only if plain `pytest` exits 2: add `tests/__init__.py` (T1 rec 3) or `pythonpath = .` (pytest ≥ 7). Record the change as new work. Re-run Rec 1. Verifier: plain pytest collects 2 tests."
  - **Risk 2**: keep the Grounded tag for the import line. Change the tag for the failure mode to "[INFERRED] (prepend-mode reasoning; INV-010 conditions unverified)".
- **Rationale**: Both scoring passes found the rejection factually wrong under prepend mode (Pass 1 K1, Pass 2 Co1). The V2 advocate withdrew U-004's High rating. INV-010 shows the affirmed fix is not sufficient on its own, which is why C-004 confidence sits at the band floor of 90% (`debate-transcript.md:172`).
- **Risk**: Medium. The claim is [INFERRED] and depends on pytest-version and config facts nobody has verified. The caveats contain that risk.

### Change 3: Recalibrate the absence tags (X-002, U-002, INV-003)
- **Source**: V1 Challenge #4 (V1:32-36). X-002 winner V1, agreed at 92% (`debate-transcript.md:176`). INV-003 (LOW, changes content).
- **Target**: Base, three places, all **replace**: "T1 challenge", "Challenged" bullet 3, the sentence "Snapshot listing has no …" (V2:45); the Risk 2 tag (V2:80); Notes.
- **Integration approach**: Replace "Grounded for … the missing config files (snapshot file list)" with a split tag:
  - **Grounded** that `src/__init__.py` is absent. The manifest's scoped inventory (`git ls-files --cached --others --exclude-standard`, `enumeration_complete: true`, scope `src`) lists only `src/greeting.py`.
  - **[INFERRED]** for root-level files (`conftest.py`, `pytest.ini`, `pyproject.toml`, `__init__.py`) and for `tests/__init__.py`. Those paths were never enumerated, and the snapshot is selected inputs only (`snapshot_kind: native-selected-inputs`).
  
  Keep "8 snapshot files" as a statement about the snapshot only.
- **Rationale**: The V2 advocate conceded that V1's [INFERRED] is the better tag. INV-003 refines it with the manifest, which no advocate read.
- **Risk**: Low.

### Change 4: Record snapshot fidelity from the provenance manifest (A-006, INV-002)
- **Source**: A-006 merge/either qualification (`debate-transcript.md:180`) and INV-002 (LOW, changes content).
- **Target**: Base, section "Notes" (**append** one bullet).
- **Integration approach**: "Every Grounded tag is snapshot-grounded and byte-faithful at audit time. `reviewer-snapshot/provenance-manifest.json` has `\"status\": \"verified\"`, and all 8 files have matching `sha256_before`, `sha256_copy` and `sha256_after`. The card does not claim fidelity after the audit."
- **Rationale**: This closes A-006 with evidence instead of leaving it open, as R1-adv2 and R2-adv2 did.
- **Risk**: Low. Additive.

### Change 5: Restructure the grounding gaps; documented decision on unresolved C-001 (C-001, S-002, INV-005, INV-007; IC contradiction V2:52 vs :53)
- **Source**:
  - V1 GG-1 and GG-2 split (V1:22-23).
  - V2 YAML schema (V2:49-62).
  - V2 gap 2 content (V2:56-61).
  - `task-to-diff-map.md:31-33`; taxonomy `:80`, `:138-147`.
- **Target**: Base, section "Grounding gaps" (V2:47-62) (**restructure**).
- **Decision on C-001 (debate-unresolved, 50%; `debate-transcript.md:137, :169`)**: use V1's split in V2's schema. **Fold** V2 gap 2 into the execution row (GG-2), instead of keeping it as a separate row or dropping it.

  Evidence for **dropping** V2 gap 2 (V1 advocate):
  - It closely repeats T1 (`t1-card.md:42-47`; `round-2-advocate-1.md:25`).
  - It is rated `decision_needed_by_user: false`.
  - It carries two ranges in one `hunk_ref` (`round-2-advocate-1.md:10`).
  
  Evidence for **keeping** it (V2 advocate):
  - `task-to-diff-map.md:32-33` requires a Grounding Gap for the missing task-log/test-state claim (`round-2-advocate-2.md:30`).
  - V2 gap 1 is also inherited from T1 (`t1-card.md:36`), so "copy" does not discriminate (`round-2-advocate-2.md:12, :31`).
  - It adds the `status: done` stamp (`round-2-advocate-2.md:16`).
  
  Why folding resolves both sides:
  - The mandate at `map:31-33` and taxonomy `:80` is that a Grounding Gap **entry** must exist when verification is unavailable and no task log exists. That missing evidence is the same missing evidence as the execution gap.
  - V2's own `next_evidence_needed` (V2:59) is "Task log or the verification run above", the same closure as gap 1. INV-007 shows that two rows would overstate the number of independent human decisions.
  - Folding meets the mandate (the GG-2 entry names the missing task log explicitly), removes the double count, and fixes V2's two-range `hunk_ref` (INV-005).
  - The `status: done` observation stays where V2 put it as a finding: F-004 (V2:28). It is not a spec contradiction (V2:58), so it does not need its own gap row.
  
  It also removes the IC contradiction in V2 gap 1 (V2:52 "exit 0 would close it" vs V2:53, which also requires provenance; conceded at `round-2-advocate-2.md:17`). Provenance and execution are now closed independently.
- **Integration approach**: Rows use exactly the 6 taxonomy fields, in schema order. Row IDs are YAML **comments**, so the schema stays byte-exact (no 7th key). Each `hunk_ref` is a single `<file:line-range>` (INV-005). Each row also needs a cross-reference line in "Adherence summary" (see Change 11). The merged block:

```yaml
# GG-1 — T-103 provenance (no diff hunk)
- hunk_ref: completed.md:8
  evidence_missing: T-103 is marked [x] but changes.patch:1-9 has no hunk for tests/test_greeting.py; the repo has zero commits and every file is untracked, and the diff was supplied explicitly (provenance-manifest.json coverage_basis); no task log (--task-log absent, task-to-diff-map.md:32).
  why_not_classifiable: A completion claim with no hunk is missing provenance, not an unmapped hunk, so it is neither Drift (taxonomy:62) nor a contradiction (Regression), and nothing in the snapshot shows whether the test file belongs to the audited change.
  next_evidence_needed: A user attestation, or a task-log entry, stating whether tests/test_greeting.py was written as part of the audited change; a regenerated or widened diff is NOT acceptable provenance (INV-004).
  owner: user
  decision_needed_by_user: true
# GG-2 — R-003 execution / regression detection unavailable (folds V2 gap 2 per C-001 decision)
- hunk_ref: tests/test_greeting.py:1-13
  evidence_missing: No pytest exit code (verification triangle not run, verification_skip_reason: tool-unavailable, task-to-diff-map.md:31); no task log, so regression detection has no test-state claim to degrade to (task-to-diff-map.md:32-33; taxonomy:80); no baseline run exists (zero commits).
  why_not_classifiable: R-003 requires the two cases to be exercised (spec.md:12), and presence in source (tests/test_greeting.py:4-5, :8-13) does not show execution, so no exit-code class (taxonomy:105-113) can be applied.
  next_evidence_needed: Both invocations from the fixture root with exit codes and per-test outcomes kept (Recommendation 1); R-003 closes only on exit 0 with 2 passed, 0 skipped/xfailed/deselected for each authoritative invocation; a task-log test-state claim is a degraded fallback only (taxonomy:80) and does not close R-003 exercise.
  owner: user
  decision_needed_by_user: false
```

  `decision_needed_by_user: false` on GG-2 means the row needs evidence, not a judgment. It becomes a decision only if the run returns 1, 2/3, 5, 124 or flaky (Changes 8-9). The forced `needs_human_decision: true` (taxonomy:149-152) is unaffected.
- **Rationale**: S-002 V2 win at 92%. C-001 both advocates want V1's split in V2's schema (`debate-transcript.md:137`). INV-005 and INV-007 apply.
- **Risk**: Medium. This replaces the whole gaps block. The C-001 decision is an orchestrator merge decision on an unresolved point, so it is disclosed in Change 15.

### Change 6: INV-004 correction: provenance and scope gaps close only by user attestation or task log (HIGH; NOT addressed in debate)
- **Source**: INV-004 (HIGH, UNADDRESSED; `invariant-probe.md:12`).
  - `provenance-manifest.json` `coverage_basis`: "repo has zero commits; all files untracked", explicit `--diff changes.patch`. The orchestrator re-read it.
  - The remediations INV-004 invalidates: V1:64, V2:89, `t1-card.md:68`, R2-adv1:7, R2-adv2:53.
- **Target**: Base, three places, all **replace**: Recommendation 2 (V2:89); the "T1 challenge" sentence "stop treating `--scope src/` as covering T-103"; the GG-1 and GG-3 `next_evidence_needed` fields (Changes 5 and 7).
- **Integration approach**:
  - **Rec 2 becomes**: "File: task log or a written user attestation. Change: state whether `tests/test_greeting.py` was written as part of the audited change (GG-1), and whether any file outside `--scope src` changed (GG-3). Verifier: the attestation or task-log entry is cited by path. Do **not** regenerate or widen `changes.patch`. In a zero-commit, all-untracked repo, a `/dev/null`→file diff for `tests/test_greeting.py` would 'map' T-103 with fabricated provenance and could wrongly flip `partial` to complete."
  - Keep V2's point that `--scope src/` does not cover T-103, as a statement of fact.
- **Rationale**: This is the only HIGH invariant, and every remediation in both variants and both advocates assumes a path to closure that cannot exist.
- **Process record (must be preserved)**:
  - This correction enters at Step 4. **It was not debated.** No advocate saw INV-004 before taking final positions.
  - Including it is required for card correctness, but it does not count as "addressing" INV-004 under the convergence gate.
  - The status stays BLOCKED_BY_INVARIANTS (Change 15).
- **Risk**: Low for content: it only narrows the closure conditions. High process significance.

### Change 7: Add the A-001 scope-boundary grounding gap (GG-3)
- **Source**: A-001 [SHARED-ASSUMPTION], High impact (`diff-analysis.md:92`). Consensus to add a scope-boundary grounding gap (`debate-transcript.md:146, :178, :245`). INV-004 for closure. INV-005 for the `hunk_ref`.
- **Target**: Base, section "Grounding gaps" (**append** after GG-2).
- **Integration approach**:

```yaml
# GG-3 — A-001 scope boundary (--scope src)
- hunk_ref: changes.patch:1-9
  evidence_missing: The audit enumerated only --scope src (provenance-manifest.json discovery scopes ["src"]); no inventory exists for root-level or tests/ files, and with zero commits there is no history showing which files the audited work changed.
  why_not_classifiable: An out-of-scope change would be an unmapped hunk (a Drift signal, taxonomy:62), but no such hunk can be cited or excluded, so the zero-Drift result holds only within changes.patch:1-9.
  next_evidence_needed: A user attestation or task-log entry listing every file the audited work created or modified; a widened or regenerated diff of an all-untracked tree is not acceptable (INV-004).
  owner: user
  decision_needed_by_user: true
```

  `hunk_ref` resolution for INV-005: the scope gap has no hunk of its own. It cites the boundary artifact `changes.patch:1-9` as one range, and `evidence_missing` states that nothing outside it can be cited.
  
  Also add one line to "Adherence summary": "Drift: 0 — within `changes.patch:1-9` only (GG-3)."
- **Rationale**: Both advocates agreed to this (merge/either, 90%). Neither original variant evaluated the boundary.
- **Risk**: Low. Additive. It does not change the 0/0/0/0 counts.

### Change 8: Complete the exit-code mapping: timeout and flaky rows (taxonomy :111-112); exit-1 attribution (INV-008)
- **Source**: Taxonomy `:111` (exit 124 → Grounding Gap, `verify_timeout_hit: true`) and `:112` (flaky → retry once before classifying as Regression; Grounding Gap + `verify_flaky_suspected: true`). R2-adv1 new evidence that neither card applies `:112` (`debate-transcript.md:91`). Consensus item (`:246`). INV-008 (MEDIUM).
- **Target**: Base, three places, all **replace**: the Recommendation 1 verifier (V2:88); the "T1 challenge" exit-code sentence (V2:45); Risk 1 (V2:79).
- **Integration approach**: Write the verifier as one ordered mapping, applied to **each** invocation:
  - **0**: candidate close. Apply the Change 9 condition.
  - **1**: retry once first (`:112`). If the retry flips, record Grounding Gap with `verify_flaky_suspected: true`. If it fails again, it is a **Regression candidate** (`:107`). Before setting `regression_present: true`, attribute the failure:
    - The failing assertion shows `src/greeting.py` contradicting R-001 or R-002 (`spec.md:6, :9`): **Regression**.
    - The failure lies in the test file itself while `src/greeting.py` conforms (for example an assertion or fixture defect): **Grounding Gap**, owner user, `decision_needed_by_user: true`. No baseline exists (zero commits, never run), so "previously-passing" (taxonomy `:75, :80`) cannot be shown.
  - **2/3**: Grounding Gap (`:108`). Apply Rec 3, then re-run.
  - **5**: Drift/coverage (`:109`; INV-014).
  - **124**: Grounding Gap, `verify_timeout_hit: true` (`:111`).
  - **Any other exit**: Grounding Gap (`:113`).
- **Rationale**: Both advocates' net positions include the `:111-112` rules. INV-008 shows the consensus lacked a failure-attribution step, so a test defect could be minted as Regression.
- **Risk**: Medium. The attribution step needs judgment at run time. Defaulting to Grounding Gap is the conservative fallback the taxonomy uses for this.

### Change 9: R-003 closure condition (INV-009) and the join rule for two invocations (INV-011)
- **Source**: INV-009 (MEDIUM), INV-011 (MEDIUM), taxonomy `:91, :103, :108`.
- **Target**: Base, three places, all **replace**: Recommendation 1 (V2:88), the GG-2 `next_evidence_needed` (Change 5), and the opening verdict paragraph's R-003 sentence (V2:11).
- **Integration approach**:
  - **Closure (INV-009)**: R-003 "exercise" closes only on exit 0 **and** a per-test report (for example `-rA` or `--junitxml`) showing `test_ordinary` and `test_empty` both passed, with 0 skipped, xfailed or deselected. Exit 0 alone is insufficient: an unenumerated root `conftest.py` or `addopts` could skip or deselect tests.
  - **Join (INV-011)**: classify `python -m pytest tests/test_greeting.py` and plain `pytest tests/test_greeting.py` separately, then join by precedence (Regression > Drift > Grounding Gap/none, `:91, :103`). Both invocations are authoritative, and neither overrides the other. If one exits 0 and the other exits 2, R-003 is **not** closed: GG-2 stays open as a collection-configuration gap (`:108`) until Rec 3 is applied (recorded per Change 2) and both invocations meet the closure condition.
- **Rationale**: The consensus remediation checked only the exit code (V1:65, V2:88, `t1-card.md:67`) and never said which invocation is authoritative.
- **Risk**: Low. This tightens the closure condition and does not change the current verdict.

### Change 10: Qualify `regression_present: false` (INV-001)
- **Source**: INV-001 (MEDIUM); `task-to-diff-map.md:31`; taxonomy `:80`. V1:23 and V1:56 already treated Regression as neither confirmed nor excluded.
- **Target**: Base, "Adherence summary" bullet `regression_present` (V2:72) (**replace**).
- **Integration approach**: "`regression_present: false` (not observed, not observed-absent). `verification_skip_reason: tool-unavailable`. No exit-1 evidence, no spec contradiction in `changes.patch:6-9`. Regression is neither confirmed nor excluded until GG-2 closes (V1 Risk 1)."
- **Rationale**: C-005 V2 win (90%) is kept on form, but INV-001 shows that an unqualified `false` overstates the evidence.
- **Risk**: Low.

### Change 11: Make the count units explicit (INV-006)
- **Source**: INV-006 (MEDIUM). V2:71.
- **Target**: Base, "Adherence summary" bullet "Unclassifiable …" (V2:71) (**replace**). Change 10 and Change 12 also edit this section.
- **Integration approach**: Replace the bullet with three bullets, each naming its unit:
  - "Spec units unclassifiable: 1 of 3 (R-003)."
  - "Grounding-gap rows: 3 (GG-1 provenance, GG-2 execution, GG-3 scope), with independent closures. GG-1 and GG-3 may share one attestation."
  - "Tasks with unproven provenance: 1 of 3 (T-103)."
  
  No return-contract count may mix these units.
- **Rationale**: After Changes 5 and 7, the base's "1" would conflict with 3 gap rows.
- **Risk**: Low.

### Change 12: Add the S_dev_density blind spot (U-001)
- **Source**: V1 Challenge #2 (V1:30), U-001, Medium value.
- **Target**: Base, "Adherence summary" `S_dev_density` bullet (V2:73) (**replace / extend**).
- **Integration approach**: "S_dev_density on the diff: 0/1. The single hunk is mapped. The metric counts only hunks that exist, so it cannot see T-103 (no hunk; GG-1) or out-of-scope files (GG-3). It does not mean requirement acceptance is 100%."
- **Rationale**: V2's advocate acknowledged U-001 as a real V1 contribution (`debate-transcript.md:77`).
- **Risk**: Low.

### Change 13: Scoped split confidence (C-006)
- **Source**: V1:74. C-006 winner V1, 93%; the V2 advocate conceded (`debate-transcript.md:174`).
- **Target**: Base, section "Self-reported confidence" (V2:100-104) (**replace** the single value; keep the explanatory paragraph).
- **Integration approach**:
  - "**0.8** for the zero-deviation result on `src/greeting.py` (`changes.patch:6-9`)."
  - "**~0.5** for the change overall, capped by GG-1 (no T-103 provenance), GG-2 (no execution), GG-3 (unenumerated scope), and the [INFERRED] import outcome."
  - Superseded single value: 0.76 (V2). Values are tagged by source variant in provenance.
  - Keep V2's model-identity sentence (U-008).
- **Rationale**: Split confidence follows the evidence gradient (agreed).
- **Risk**: Low.

### Change 14: Mitigation for Risk 4 (weak `test_empty` oracle) (base Risk-2 criterion miss; V1 Correctness gap #2)
- **Source**: V1:45 (content), with the advisory channel removed per S-005/X-003. Both scoring passes found V2 Risk 4 had no mitigation (P1 R2, P2 R2).
- **Target**: Base, Risks row 4 (V2:82) and Recommendations (**append** Rec 5).
- **Integration approach**: Add Rec 5. "File: `tests/test_greeting.py:8-13`. Change (optional, not required by R-002): replace the manual try/except with `pytest.raises(ValueError)`. Add `match=\"name required\"` only if the spec amendment in Rec 4 makes the message contractual. This is new work: it needs its own task and attribution (INV-012), and it must not be applied before GG-2's run on the audited tree. Verifier: the test fails when `greet(\"\")` does not raise."

  Also add "Mitigation: Rec 5 (optional)" to Risk 4. Do not reintroduce a correctness-gaps section.
- **Rationale**: Closes the one base risk with no mitigation, without breaking the S-005 sibling rule.
- **Risk**: Low. Advisory only.

### Change 15: Merge-status disclosure in Notes (INV-004 not debated; C-001 orchestrator decision; BLOCKED_BY_INVARIANTS)
- **Source**: `debate-transcript.md:15, :207-225, :237-239`; this plan.
- **Target**: Base, section "Notes" (**append** one bullet).
- **Integration approach**: "Adversarial merge status: **BLOCKED_BY_INVARIANTS**. INV-004 (HIGH) was raised by the Round 2.5 invariant probe after the advocates' final positions and was **not addressed in any debate round**. Its correction (GG-1 and GG-3 close only by user attestation or task log; regenerated diffs are not provenance) was incorporated at the refactor-plan stage. That does not clear the block. Clearing it requires a later debate round on INV-004 or explicit user acknowledgement as accepted risk. C-001 (gap partition) was unresolved in debate; the folded GG-2 is an orchestrator merge decision documented in `refactor-plan.md` Change 5. Convergence score 94.7% (18/19)."
- **Rationale**: Instruction (c); process integrity. The card must not read as a converged, clean result.
- **Risk**: Low.

## Base Weaknesses and Better-Variant References

| Base (V2) weakness | Location | Better reference | Change |
|---|---|---|---|
| "`changes.patch` is 10 lines" (false; 9) | V2:44 | Snapshot `changes.patch` (9 lines); C-002 consensus | 1 |
| Rejects T1 rec 3 (`tests/__init__.py`) | V2:45, :90 | V1 side of C-004; consensus `debate-transcript.md:248` | 2 |
| "Grounded" absence of config files | V2:45, :80 | V1:32-36 (U-002); INV-003 | 3 |
| Gap 1 mixes execution and provenance; internal contradiction V2:52 vs :53 | V2:50-55 | V1 GG-1/GG-2 (V1:22-23) | 5 |
| Gap 2 two-range `hunk_ref`; double-counts decisions | V2:56-61 | INV-005, INV-007 | 5 |
| Closure via widened diff | V2:89, :53 | None in either variant; INV-004 | 6 |
| No scope-boundary evaluation | (absent) | A-001; consensus | 7 |
| Exit-code table omits 124 and flaky; exit 1 auto-Regression | V2:45, :52, :88 | Taxonomy `:111-112`; INV-008 | 8 |
| Exit 0 treated as closure; no invocation join rule | V2:88 | INV-009, INV-011 | 9 |
| Unqualified `regression_present: false` | V2:72 | V1:23, :56; INV-001 | 10 |
| "Unclassifiable: 1" ambiguous unit | V2:71 | INV-006 | 11 |
| No S_dev_density blind-spot note | V2:73 | V1:30 (U-001) | 12 |
| Single 0.76 confidence | V2:102 | V1:74 (C-006) | 13 |
| Risk 4 has no mitigation | V2:82 | V1:45 | 14 |

## Changes NOT Being Made (with rationale)

| # | Diff Point / Item | Non-Base Approach | Rationale for Keeping Base / Not Adopting |
|---|---|---|---|
| N-1 | S-002 | V1 Markdown gap table with an `id` column and no `decision_needed_by_user` | V2 won at 92%. V1 conceded the missing field. The taxonomy schema is byte-exact (`:138-147`). IDs are kept only as YAML comments (Change 5). |
| N-2 | S-005 / X-003 | V1 "Correctness gaps (advisory — non-gating)" section | V2 won at 95% / 97%. `greet` has no sibling symbol (`taxonomy:161, :167`). V1 conceded (R2-adv1:8). INV-013 is ADDRESSED. Only the weak-oracle content moves, as a Risk mitigation (Change 14). |
| N-3 | X-001 | V1 GG-1 / Risk 2 "could turn out to be … Drift" | V2 won at 97%. Drift needs an unmapped hunk (`taxonomy:62, :96`). V1 conceded. INV-014 is ADDRESSED. The exit-5 route is kept in Change 8. |
| N-4 | C-001 alternative A | Keep V2 gap 2 as a separate row (V2 advocate) | Rejected in favour of folding (Change 5). INV-007 shows one closure path serves both. The two-range `hunk_ref` breaks `:141` (INV-005). The `map:32-33` mandate is still satisfied by GG-2. |
| N-5 | C-001 alternative B | Drop V2 gap 2 entirely (V1 advocate) | Rejected. Dropping would lose the missing-task-log evidence that `map:32-33` and taxonomy `:80` require as a Grounding Gap entry. Its content is folded into GG-2 instead. |
| N-6 | INV-004-invalid remediation | V1 Rec 1 verifier "Re-run the audit with `tests/` in the diff scope" (V1:64); T1 rec (`t1-card.md:68`) | Cannot produce real provenance in a zero-commit, all-untracked repo (INV-004). Replaced by attestation or task log (Change 6). |
| N-7 | V1 GG-2 `hunk_ref: spec.md:11-12` | Cite the spec section as the hunk | Not a code location. Pass 1 flagged it under K3. The base's `tests/test_greeting.py:1-13` is kept (Change 5). |
| N-8 | S-001 | V1 terse `none \| n/a` deviations row | V2 won at 90%. Its explicit precedence walk is kept. |
| N-9 | S-006 | V1 untagged numbered risks | V2 won at 90%. The tagged risk table is kept. |
| N-10 | S-004 | V1 section ordering | merge/either, L1 presentation. The base order is kept to minimise restructuring. |
| N-11 | Risk-1 criterion (probability and impact ratings) | None (neither variant supplies them) | Both variants missed it in both passes. Adding ratings would be unsourced new content. sc:merge-executor merges evidence, it does not author it. Left as a known gap. |
| N-12 | Clarity-4 criterion (term definitions: T1, S_dev_density, verification triangle) | None (neither variant defines them) | Same reason as N-11: no variant source. A glossary would be new, unsourced content. Left as a known gap. |
| N-13 | INV-016 (LOW: same-class advocates, haiku→grok resolution, one shell read by the V2 advocate) | n/a | A process finding about the debate, not about the audited change. It is already disclosed in `debate-transcript.md:13-14` and `invariant-probe.md:24`. The card keeps U-008 model disclosure, with no extra content. |
| N-14 | A-002, A-007, INV-013, INV-014, INV-015 | n/a | Accepted or ADDRESSED. A-002 is accepted at 95%. A-007 is benign: a runtime below 3.6 gives exit 2, a Grounding Gap. No content change is needed. |

Invariant disposition check (instruction d):
- **MEDIUM**: INV-001 → Change 10; INV-006 → Change 11; INV-008 → Change 8; INV-009 → Change 9; INV-010 → Change 2; INV-011 → Change 9.
- **LOW, content-changing**: INV-002 → Change 4; INV-003 → Change 3; INV-005 → Changes 5 and 7; INV-007 → Change 5.
- **Other LOW**: INV-012 → caveat in Changes 2 and 14; INV-016 → N-13.
- **ADDRESSED**: INV-013 to INV-015 → N-14.
- **HIGH**: INV-004 → Change 6, with the BLOCKED disclosure in Change 15.

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | A wrong line count persists | Revert V2:44 sentence |
| 2 | Medium | Wrong import-mode guidance if the INV-010 conditions hold | Revert to base bullet 3, Rec 3 and Risk 2. Keep the caveat that no fix is verified. |
| 3 | Low | Over- or under-claimed grounding | Revert tags to the base |
| 4 | Low | Additive note | Remove the Notes bullet |
| 5 | Medium | Malformed gaps artifact; the C-001 decision is contested later | Restore the base YAML (V2:49-62). Apply only the V1 split. |
| 6 | Low | Recommendation could still invite fabricated provenance | Restore base Rec 2 with the INV-004 warning appended |
| 7 | Low | Additive row | Remove GG-3 and its Adherence line |
| 8 | Medium | Mis-attribution at run time | Fall back to taxonomy `:105-113` verbatim, with the conservative Grounding Gap default |
| 9 | Low | Stricter closure than intended | Revert to the base exit-0 closure, plus the INV-009 note |
| 10 | Low | n/a | Revert the bullet |
| 11 | Low | Count confusion | Revert the bullet |
| 12 | Low | Additive | Remove the sentence |
| 13 | Low | Confidence misread | Restore 0.76 |
| 14 | Low | Additive, advisory | Remove Rec 5 |
| 15 | Low | Additive disclosure | Remove the bullet. This is **not recommended**: the BLOCKED status must remain visible. |

**Post-merge checks for sc:merge-executor**:
- (a) The deviations table still has zero rows, and the counts still read 0/0/0/0.
- (b) Every grounding-gap entry has exactly the 6 keys `hunk_ref`, `evidence_missing`, `why_not_classifiable`, `next_evidence_needed`, `owner`, `decision_needed_by_user`, in that order, with a single-range `hunk_ref`.
- (c) No text says "10 lines", or that `tests/__init__.py` "does not put the project root on `sys.path`".
- (d) No recommendation proposes widening or regenerating the diff as provenance.
- (e) The BLOCKED_BY_INVARIANTS note is present.
- (f) GG-1, GG-2 and GG-3 references resolve.
- (g) `status: partial` and `needs_human_decision: true` are present.

## Review Status
- [x] Auto-approved (default; non-interactive run, no `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-24T21:40:53Z
- Caveat: auto-approval covers merge execution only. It does **not** acknowledge INV-004 as accepted risk. That acknowledgement is reserved to the user.

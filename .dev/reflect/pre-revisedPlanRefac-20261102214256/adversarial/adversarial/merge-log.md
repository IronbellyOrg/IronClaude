# Merge Execution Log

## Metadata

- Base: Variant 1 (reviewer-1, sonnet, analyzer), `variant-1-original.md`
- Plan: `refactor-plan.md` (16 planned changes; approved auto, 2026-11-02T22:45:00Z)
- Executor: merge-executor (opus)
- Output: `../merged-findings.md`
- Changes applied: 16 of 16
- Status: COMPLETE, post-merge validation FAIL (1 contradiction, escalated, not fixed; see Contradiction Re-Scan)
- Timestamp: 2026-11-02T22:43:17Z

Executor notes:

- Top-level keys follow the requested card shape (`reviewer: merged`, `base: variant-1`, `findings`, `deviations_resolution`, `t1_findings_disputed`, `inferred_claims`). The base's `persona`, `model_class` and `self_confidence` are not carried over because they describe reviewer 1 alone. The base's orchestrator-verification header is kept as YAML comments inside the block.
- Ordering: medium first, then low. Within each severity, findings follow plan task order (Constraints/Task 1 -> Task 8). Within Task 2 the medium findings keep the plan's insertion order (R1-1, R1-2, then M-1 after R1-2, M-2, M-3). Within Task 8 the low findings follow plan line order (R3-F6 :177 before R3-F5 :178), which reverses the order of Changes 10 and 11.
- Every quote in evidence was re-checked against its file in this session: the plan, scripts/eval_runner.py, scripts/eval_1.py, CLAUDE.md, tests/swarm/test_bare_review_golden_regen.py, tests/troubleshoot/backtest/git_replay.py, tests/skills/test_implement_retry_revert.py, tests/troubleshoot/backtest/test_git_replay_integration.py, src/superclaude/skills/sc-implement-protocol/SKILL.md, sc-pr-submit-protocol/scripts/poll-ci-checks.sh and the plan's source.md.

## Changes Applied

### Change 1: Sharpen R1-1 with V3's failure-string criterion

- Status: Applied
- Source: Variant 3 R3-F1 recommendation
- Target: R1-1 recommendation
- Before: "register the module with `sys.modules[spec.name] = module` before `exec_module`, and remove it in teardown. Verify the pre-change failure comes from the missing `master_checkout` attribute, not an import error."
- After: registration via `monkeypatch.setitem(sys.modules, spec.name, module)`; `./artifacts/t2-fail-before.txt` must fail on the missing `master_checkout`, not on `'NoneType' object has no attribute '__dict__'`. Id, `drift`, medium unchanged.
- Provenance tag: "Base V1 R1-1; recommendation sharpened from V3 R3-F1 ... Change 1."
- Validation: PASS (label and severity match C-001 and X-003)

### Change 2: Replace R1-2 with the merged failure-path finding

- Status: Applied
- Source: V3 R3-F3; INV-003; INV-004
- Target: R1-2 (restructured, id kept)
- Before: low; headline on leak and masking only; recommendation `os.rmdir` before raising, non-masking teardown.
- After: medium; headline covers leak, masking and mis-reporting body errors as global-setup; evidence adds plan :64, eval_runner.py:70, git_replay.py:200; recommendation: `MasterCheckoutError`, tolerant removal (`shutil.rmtree(..., ignore_errors=True)` or `contextlib.suppress(FileNotFoundError)`), raise before any try/finally, try/finally around `yield` only, teardown failures logged not raised, `main` catches only `MasterCheckoutError`. INV-003 kept as `[INFERRED]`.
- Provenance tag: "Base V1 R1-2 ...; restructured with V3 R3-F3 ...; INV-003, INV-004 ... Change 2."
- Validation: PASS

### Change 3: New finding M-1 (main() wiring and global-setup path untested)

- Status: Applied
- Source: V3 R3-F2, R3-F9; V2 R2-F2; round2-v1.md (eval_runner.py:294-295); INV-005, INV-006, INV-014; A-001
- Target: new finding after R1-2
- Before: (none)
- After: M-1, `drift`, medium, with every recommendation element the plan lists (patched-argv `--mode global` test, exit-code rule at :313, replacement for the :294-295 guard, restated plan :74, deliberate local `master`).
- Provenance tag: "New. V3 R3-F2 and R3-F9 ...; INV-005, INV-006, INV-014 ...; A-001 caveat ... Change 3."
- Validation: PASS

### Change 4: New finding M-2 (tests not isolated from the real checkout)

- Status: Applied
- Source: INV-001, INV-010, INV-015; V3 R3-F7
- Target: new finding
- Before: (none)
- After: M-2, `drift`, medium; recommendation patches `RESULTS_DIR`, seeds EVAL_FILES/E2E stubs or tests the `with` body separately, `git init -b master` with identity, `GIT_*` stripped and `GIT_CONFIG_GLOBAL=/dev/null`, `git status --porcelain` unchanged.
- Provenance tag: "New. INV-001, INV-010, INV-015 (probe); V3 R3-F7 folded in ... Change 4."
- Validation: PASS

### Change 5: New finding M-3 (forced removal deletes global E2E outputs)

- Status: Applied
- Source: INV-013
- Target: new finding
- Before: (none)
- After: M-3, `regression`, medium; recommendation passes `--output-dir` (or copies `eval-results/`) under the real `RESULTS_DIR` before teardown, or states the outputs are discarded. The eval_1.py default spec path note (eval_1.py:432) stays `[INFERRED]`.
- Provenance tag: "New. INV-013 ... Change 5."
- Validation: PASS

### Change 6: Merge R1-4 with V3's CLAUDE.md:50 conflict

- Status: Applied
- Source: V3 R3-F4 first half
- Target: R1-4 (restructured)
- Before: low; location plan :113; evidence CLAUDE.md:64 and :70; recommendation names :70 and drops the check-1 `upstream` parenthetical.
- After: medium; location plan :113, CLAUDE.md:50, CLAUDE.md:70; CLAUDE.md:64 half dropped; recommendation says how line 50 is rewritten (repo from origin, must be IronbellyOrg/IronClaude, halts on a wrong-owner URL) and keeps the :70 rewrite. Scripts half of R3-F4 not merged.
- Provenance tag: "Base V1 R1-4 (CLAUDE.md:70 half kept; CLAUDE.md:64 half dropped ...); V3 R3-F4 first half ... Change 6."
- Validation: PASS for the finding itself; see Contradiction Re-Scan for the D-004 row it leaves stale.

### Change 7: Mark R1-5 as required

- Status: Applied
- Source: round2-v3.md; V3 R3-F4 awk command
- Target: R1-5 recommendation
- Before: "Use `grep -n -w 'gh' CLAUDE.md` restricted to the section's line range."
- After: "Required, not optional:" the section-scoped form `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n -w 'gh'`. Severity stays low. Both heading anchors exist (CLAUDE.md:39, :72).
- Provenance tag: "Base V1 R1-5; marked required per round2-v3.md ... Change 7."
- Validation: PASS

### Change 8: Merge R1-3 with the Orca-vs-fork-rule conflict

- Status: Applied
- Source: INV-012
- Target: R1-3 (restructured)
- Before: low; headline on the link-flag strength mismatch only.
- After: medium; headline per plan; evidence adds plan :86, :105, :111; recommendation qualifies plan :105 to link flags and network-reaching calls and uses one wording in both tasks. Location kept at plan :88.
- Provenance tag: "Base V1 R1-3 (U-001); merged with INV-012 ... Change 8."
- Validation: PASS

### Change 9: Add R2-F1

- Status: Applied
- Source: V2 R2-F1; round2-v2.md; INV-011
- Target: new finding
- Before: (none)
- After: R2-F1, `drift`, medium; headline, evidence and recommendation verbatim from V2; rationale adds the full-depth/uid-1000 point and INV-011.
- Provenance tag: "V2 R2-F1 (recommendation verbatim) ... Change 9."
- Validation: PASS

### Change 10: Add R3-F5 as low hardening

- Status: Applied
- Source: V3 R3-F5; round2-v3.md
- Target: new finding
- Before: (none; V3 card had medium)
- After: R3-F5, `drift`, low; rationale states the checks are vacuous only if source files are staged by hand; evidence adds SKILL.md:125 and plan :29. The plan :148 quote was corrected to the full verbatim text (V3 had elided it).
- Provenance tag: "V3 R3-F5; severity medium -> low per round2-v3.md ... Change 10."
- Validation: PASS

### Change 11: Add R3-F6 merged with INV-007

- Status: Applied
- Source: V3 R3-F6; INV-007
- Target: new finding
- Before: (none)
- After: R3-F6, `drift`, low; memory-note example removed from evidence; evidence adds plan :46; recommendation unchanged from V3.
- Provenance tag: "V3 R3-F6 merged with INV-007; the untracked memory-note example dropped ... Change 11."
- Validation: PASS

### Change 12: Add R3-F8

- Status: Applied
- Source: V3 R3-F8
- Target: new finding
- Before: (none)
- After: R3-F8, `drift`, low; recommendation prefers the behavioural `git worktree list` assertion, with V3's grep as the fallback.
- Provenance tag: "V3 R3-F8 ... Change 12."
- Validation: PASS

### Change 13: New finding M-4 (retired-location checkouts gone)

- Status: Applied
- Source: INV-009
- Target: new finding
- Before: (none)
- After: M-4, `drift`, low; location plan :27, :44, :51, :90; recommendation per plan.
- Provenance tag: "New. INV-009 ... Change 13."
- Validation: PASS

### Change 14: Add R2-F3 as a low completeness note

- Status: Applied
- Source: V2 R2-F3 with the orchestrator annotation
- Target: new finding
- Before: (none)
- After: R2-F3, `drift`, low; evidence states no `IronClaude-eval-master` checkout exists today (orchestrator 22:23Z).
- Provenance tag: "V2 R2-F3 with the orchestrator annotation ... Change 14."
- Validation: PASS

### Change 15: Amend `deviations_resolution`

- Status: Applied
- Source: round2-v1.md; round2-v2.md; INV-009
- Target: rows D-001, D-002, D-008, D-013
- Before: D-001 `resolved: yes`, note "R1-1/R1-2 are execution risks"; D-002 note "R1-4, R1-5 remain"; D-008 note "-rs, zero skips or recorded reason + rerun"; D-013 note "stay until merged; not moved".
- After: D-001 `resolved: "yes, with required fix"`, note names R1-1, R1-2, M-1, M-2, M-3; D-002 "R1-4 (now incl. CLAUDE.md:50), R1-5 remain"; D-008 adds R2-F1; D-013 adds M-4 (checkouts gone). Other 10 rows unchanged.
- Provenance tag: none inline (flow-mapping rows); sourced as listed.
- Validation: PASS for the four rows; D-004 left unchanged as the plan directs (see Contradiction Re-Scan).

### Change 16: Extend `t1_findings_disputed` and `inferred_claims`

- Status: Applied
- Source: V3 S1 and S3 disputes (S3 narrowed per round2-v3.md); V2 search reproduction (U-005); INV-008
- Target: `t1_findings_disputed` (append S1, S3); `inferred_claims` (append 2)
- Before: 2 disputes (F1, F3); 4 inferred claims.
- After: 4 disputes (F1, F3, S1, S3); 6 inferred claims.
- Provenance tag: none inline; the S1/S3 reasons cite R1-1, R1-2, M-1, R1-4, R1-6.
- Validation: PASS

### Changes NOT being made (honoured)

- X-001: R1-6 kept `authorized`, low; R3-F4 scripts half not merged.
- X-003: R1-1 stays `drift`.
- U-006: R3-F5 low.
- R3-F7: folded into M-2, no standalone finding.
- R3-F9: folded into M-1, no standalone finding.
- `.venv` deletion claim: not carried into `inferred_claims`.
- R1-4 CLAUDE.md:64 half: dropped.

## Post-Merge Validation

### Structural Integrity

- PASS. The file has three provenance comments followed by exactly one fenced `yaml` block (2 fences), and `yaml.safe_load` parses it.
- Top-level keys: `reviewer`, `base`, `findings`, `deviations_resolution`, `t1_findings_disputed`, `inferred_claims`.
- 15 findings; every one has non-empty `id`, `headline`, `location`, `classification`, `severity`, `evidence`, `rationale`, `recommendation` and `provenance`. No duplicate ids.
- Every classification is in {authorized, necessary, drift, regression}; every severity is in {high, medium, low}. Medium findings precede low findings.

### Internal References

- PASS. Finding ids referenced in `deviations_resolution`, `t1_findings_disputed` and `inferred_claims`: M-1, M-2, M-3, M-4, R1-1, R1-2, R1-4, R1-5, R1-6, R2-F1. All 10 exist in `findings`.
- Ids that no longer exist as standalone findings (R3-F1, R3-F2, R3-F3, R3-F4, R3-F7, R3-F9, R2-F2) appear only inside `provenance` fields as source attributions, not as references to merged findings.

### Contradiction Re-Scan

- FAIL: 1 new contradiction introduced by the merge.
  - D-004 row: note "line-64 parenthetical in R1-4". After Change 6, R1-4 no longer covers CLAUDE.md:64 (that half was dropped because plan :108 already rewrites check 1). The note now points at content R1-4 does not contain. Change 15 lists only D-001, D-002, D-008 and D-013, so the executor left D-004 unchanged rather than improvise. Suggested fix for the orchestrator: change the D-004 note to "line-64 parenthetical removed by plan :108's rewrite of check 1".
- No other new contradictions found. Checked: each headline against its severity and rationale (re-rated R1-2, R1-3, R1-4 headlines now match medium scope; R2-F3's "possibly existing" headline matches its "none exists today" evidence; M-3's `regression` label matches its "removes existing behaviour" rationale); R1-6's "D-002 names only CLAUDE.md:64 and :66" refers to the deviation text, not to R1-4, so it is consistent.

## Summary

- Planned: 16
- Applied: 16
- Failed: 0
- Skipped: 0
- Findings: 15 (medium 8, low 7; drift 13, regression 1, authorized 1, necessary 0)
- Post-merge validation: FAIL (structural PASS, references PASS, contradiction re-scan FAIL on the stale D-004 note; escalated to the orchestrator, not fixed because the plan does not cover D-004)

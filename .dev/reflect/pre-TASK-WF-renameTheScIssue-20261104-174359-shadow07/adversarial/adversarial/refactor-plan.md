# Refactoring Plan — Merge of the Three Reviewer Cards (shadow07)

Base: card 1 (analyzer, calibrated 0.80, combined score 0.816). Incorporating: card 2 (qa, 0.762), card 3 (refactorer, 0.773). Merged output: `merged-verdict.md` + `merged-verdict.yaml` in this directory.

## Overview

- Changes planned: 7 (5 substantive incorporations + 2 base corrections)
- Risk: Low overall (document merge; every change is additive or precision-refining; no restructure)
- Merge rule honored: findings cross-confirmed by 2+ reviewers rank higher (A: 2 reviewers; B: 2 reviewers; C: 1 + 1 concession; D: 1 unique; E: 1 raised + 2 rebutting, withdrawn); severity stays as calibrated (all MINOR, non-blocking); no new findings invented.

## Planned Changes

### Change 1 — Topic A (sync/mirror gap): adopt card 1 F1 as base text, correct per card 3's Round-1 self-correction and add card 3's framing + citations
- Source: card 3 analysis §1 (reader-impact: "anything reading `.claude/` during development would see the old names"; "no task AC would catch this" — both task test runs read `src/`), plus Makefile:178.
- Target: merged-verdict topic A.
- Integration: replace card 1 F1's remedy-implying "the plan does not tell the executor how to handle that" tail with the verified mechanism chain: plan forbids `.claude/` edits (plan:20); no task runs sync-dev/verify-sync (only plan mention is plan:20); sync-dev is cp-only (Makefile:108-163) so it never deletes the old `templates/summary.md` from the mirror — it persists even after sync-dev; a local `verify-sync` detects it via `diff -rq` "Only in" (Makefile:178); CI regenerates before verifying (test.yml:125-131) so CI is unaffected; verify-sync is not on the pre-commit commit path (.pre-commit-config.yaml:115-126).
- Rationale: Round 2 unanimous (C-001 confidence 95%); invariant probe corrected the remedy mechanism.
- Risk: Low.

### Change 2 — Topic B (grep ambiguity): card 1's framing + card 2's propagation, with Round-2 narrowing
- Source: card 2 F1 (T2 reuse at plan:56) and card 2's Round-2 merged wording (withdraws plan:94 from the verbatim cluster).
- Target: merged-verdict topic B.
- Integration: base text card 1 F2 (failure mode: mixed old+new line passes; backstop `test_old_summary_path_is_gone`); add the propagation: the identical phrasing also appears in T2's AC (plan:56); T4's AC (plan:94) uses the same grep but adds an explicit dated-note exception clause, making it the best-specified of the three. Use card 2's Round-2 merged wording as the topic-B sentence.
- Rationale: C-002 confidence 90%; all three advocates converged on this wording in Round 2.
- Risk: Low.

### Change 3 — Topic C (T3 red-check): adopt card 2's narrowed finding
- Source: card 2 F2 + Round-2 narrowing.
- Target: merged-verdict topic C.
- Integration: new finding in the merged set (base card 1 had only a non-finding here, conceded in Round 2). Claim: plan:76's red-check states "exit code recorded" without an expected value; it does state a substantive expectation (report `summary.md` blocked, `<D>/summary.md` found) but the step is an unasserted log rather than a check; the pinned `test_checks_flag_pre_fix_text` (tests:493-501) proves the same on in-module literals while the red-check runs on the real `artifacts/pre/` captures — different evidence objects, so not a strict duplicate; MINOR severity stands (as-written the pass condition for the exit code is unstated though trivially inferable).
- Rationale: C-003 confidence 85%; card 1's advocate explicitly conceded its H3 non-finding answered the wrong question.
- Risk: Low.

### Change 4 — Topic D (AC2 verifier): adopt card 2 F3 unchanged
- Source: card 2 F3 (unique, undisputed).
- Target: merged-verdict topic D.
- Integration: verbatim adoption with corrected citation plan:43 (not plan:50). Claim: T1.AC2 asserts the template is "otherwise unchanged apart from the analysis-name wording" but names no verifier, while plan:31/42 supply the pre-fix copy (`artifacts/pre/template-summary.md`) a diff could run against.
- Rationale: C-004 confidence 90%; no opponent disputed; concrete cheap remediation.
- Risk: Low.

### Change 5 — Topic E (coverage/traceability): card 3's substance-altitude classification; card 2's F4 withdrawn
- Source: card 3 analysis §2 + Round 2; card 2's Round-2 withdrawal.
- Target: merged-verdict topic E.
- Integration: no finding. Record as explicit non-finding with rationale: the guide-row no-edit is evidenced (plan:91 + t4-guides.log AC plan:96) and the design-doc old-path exclusion is encoded, not missing — plan:87 mandates the dated note naming the old `summary.md`, plan:94's AC carries the explicit "plus the old name inside the dated note" exception, and plan:71 enumerates the deterministic test's scope exactly. Card 2's F4 is withdrawn as a finding (its own advocate in Round 2: "the exception IS stated, in plan:94 itself"); at most one INFO-class observation (design-doc cleanliness attested by one-off log rather than permanent test — consistent with the plan's stated exception).
- Rationale: C-005 confidence 90%; X-001 resolved at the substance altitude, unanimously.
- Risk: Low.

### Change 6 — Topic F (paragraph drift guard): record card 3's F2 as a documentation note, not a finding
- Source: card 3 F2 + its Round-2 concession; cards 1/2 Round-2 positions.
- Target: merged-verdict topic F.
- Integration: no finding. Record as documentation note: the plan's three agent paragraphs and the test literal are kept in sync by plan:67 ("update `_TOOL_INPUT_PARAGRAPH` to the exact Constraints paragraph") + plan:75's whole-file test run, which mechanically executes `tool_input_rule_problems` (tests:271-291, via tests:298-301) — exactly-once (281-282) and under-heading (283-284) — leaving no residual executor failure mode; card 3's F2 correctly identified the guard but mis-classified the silence as a defect.
- Rationale: C-006 confidence 95%; all three advocates independently concluded note-class.
- Risk: Low.

### Change 7 — Provenance and citation discipline
- Source: card 2 Round 2 ("print the corrected line numbers, not mine — replicating them would propagate the defect"); base-selection DC metric.
- Target: every merged finding's citations.
- Integration: all citations in the merged verdict use verified line numbers (plan:20/31/43/44/56/57/67/71/75/76/87/91/94/96; Makefile:108-163, 178; test.yml:125-131; .pre-commit-config.yaml:115-126; tests:271-291, 298-301, 339-341, 370-383, 396-415, 459-479, 482-490, 493-501). Where a source card's citation was off (card 2's plan:51/50/52; card 1's Makefile 112-125; card 3's tests 281-283), the merged verdict prints the corrected value and notes the correction in the merge log.
- Rationale: citation integrity is the merge base's decisive strength; propagating known-wrong line numbers would defect the merged output.
- Risk: Low.

## Base Weaknesses and Fixes

| Base weakness | Better variant | Fix |
|---|---|---|
| Topic C non-finding (H3) answered the wrong question | Card 2 F2 | Change 3 (adopt narrowed finding) |
| Topic B scoped to T1 only (plan:44) | Card 2 F1/round-2 wording | Change 2 (propagation to plan:56, plan:94 narrowing) |
| Topics D/E/F blank | Cards 2/3 | Changes 4-6 (adopt D; record E and F as reasoned non-findings/notes) |
| F1 Makefile span 112-125 partial | Card 3 / verified facts | Change 1 (108-163 + Makefile:178 + manual-removal remedy) |
| H4 verdict uncited | Card 2's evidence-discipline standard | Change 7 (H4 excluded from merged output as unverifiable-as-written; base card keeps the debt noted) |

## Changes NOT Being Made

- **Not adopting card 2's "self-contradictory" framing of T1.AC3** — rejected: withdrawn by card 2's own advocate in Round 2 (the AC is satisfiable under the natural reading; card 1's "ambiguous" framing is more accurate). Debate evidence: Round 2, card 2 final concessions.
- **Not counting plan:94 in the verbatim ambiguity cluster** — rejected: plan:94 carries the explicit dated-note exception clause T1/T2 lack; all three advocates converged on this in Round 2.
- **Not adopting card 2 F4 as a finding** — rejected: withdrawn by its own advocate; the design-doc exclusion is encoded at plan:87/94/71 (Round 2, C-005, 90% confidence).
- **Not adopting card 3 F2 as a finding** — rejected: reclassified by its own advocate after re-walking the executor path (Round 2, C-006, 95% confidence).
- **Not adopting card 3's "may linger until someone runs make sync-dev" remedy** — rejected: factually wrong (sync-dev is cp-only; the stale file persists through sync-dev; manual removal is the remedy). Corrected by card 3's own advocate in Round 1.
- **Not adopting card 1's H4 "always comes with content description" generalization** — rejected as merged content: uncited as-written; unverifiable claim about plan convention. The merged verdict does not carry it.

## Risk Summary

All changes Low risk (document merge, additive). Rollback: the three variant files are preserved verbatim in this directory; the merged verdict can be regenerated from them plus this plan.

## Review Status

Auto-approved (non-interactive invocation). Approval timestamp: 2026-11-13T00:55:00Z.

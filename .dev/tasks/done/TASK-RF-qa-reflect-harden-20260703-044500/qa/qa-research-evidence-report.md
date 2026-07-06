# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Template-02 task additively hardening RF QA + /sc:reflect vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**fix_authorization:** false

---

## Method

Zero-trust evidence verification. Every load-bearing file:line/function/class citation in the 7 assigned research files is spot-checked by opening the ACTUAL worktree source. Any citation that does not match reality = CRITICAL.

Assigned files:
- 01-fx3-questions-resolution.md
- 02-fx5-gate-helpers.md
- 03-fx7-reflect-contract.md
- 04-fx2-fx1-briefs.md
- 05-tests-conventions.md
- 06-mdtm-template-examples.md
- 07-doc-crossvalidate.md

---

## Findings

## Overall Verdict (evidence-quality lens): PASS

Every load-bearing file:line/function/class citation spot-checked against the actual
pr209-harden worktree matched reality exactly. ~45 distinct citations verified across all
7 assigned files; 0 fabricated, 0 mismatched. The prompt defined a citation that does NOT
match reality as CRITICAL — none were found. One MINOR terminology-looseness observation
and one immaterial nitpick; neither blocks the builder.

## Spot-Check Evidence Log (citations opened in the real worktree)

| Research claim (file) | Cited locus | Verified? | Actual finding |
|---|---|---|---|
| `_VERIFICATION_SKIP_EXEMPTIONS` (03, 07) | contract.py:35-38 | ✅ EXACT | `frozenset({"read-only-project","tool-unavailable","--no-verify"})` w/ comment |
| Trigger 12 verification-skip degrade (03, 07) | contract.py:287-291 | ✅ EXACT | `if verification_ran is False: if skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS: return "verification-skipped"` |
| `build_reflect_contract` def (03) | ensemble.py:492-568 | ✅ EXACT | def at :492, returns dict :536-568 |
| `reviewer_count = len(succeeded)` (03) | ensemble.py:517 | ✅ EXACT | succeeded filter :516, count :517 |
| hardcoded `status:"success"` (03) | ensemble.py:538 | ✅ EXACT | line 538 |
| hardcoded `verification_ran:False` + skip_reason (03) | ensemble.py:550-551 | ✅ EXACT | `"verification_ran": False`, `"verification_skip_reason": "tool-unavailable"` |
| hardcoded `degraded_components:[]` (03) | ensemble.py:560 | ✅ EXACT | line 560 |
| `_path_resolves` all-None fix branch (02, 07) | candidate.py:360, list-comp 372-376, guard 379 | ✅ EXACT | `(value := item.get(part)) is not None` comp + `if current in (None,[]): return False` |
| `SetupAnswers` 17 fields incl `augment_app_slug` (01) | questions.py:14-38, slug :28 | ✅ EXACT | frozen dataclass, augment_app_slug:28 w/ "not tunnelled" comment |
| `_evidence_attr(attr, answer_attr=None)` (01, 07) | questions.py:64, answer_key :68 | ✅ EXACT | `answer_key = answer_attr or attr` :68; silent getattr :71/:74 |
| probe_pr deriver F3 fix (01, 07) | questions.py:136 (133-139) | ✅ EXACT | `_evidence_attr("pr_number", answer_attr="probe_pr")` |
| F1 `diagnose()` file-OR-dir fix (07) | diagnosis.py:134-138 | ✅ EXACT | `_resolve_optional_path` + comment "payload FILE or probe DIRECTORY" + `is None or not exists()` |
| NO lens id `internal-consistency` exists (04) | rf-qa-qualitative.md grep | ✅ CONFIRMED | hyphenated token: NO MATCH; "Internal consistency" (space) at 92/307/755 |
| Code Compatibility items 4-6 (04) | rf-qa-qualitative.md:670-676 | ✅ EXACT | `##### Code Compatibility`:670, items 4/5/6 at 672/674/676 |
| "Checklist (15 items)" (04) | rf-qa-qualitative.md:660 | ✅ EXACT | line 660 |
| Five Adversarial Axes header (04) | rf-qa-qualitative.md:580 | ✅ EXACT | PR-07 sharpening overlay heading |
| AX-2 charter + `build_axis_overlay()` example (04) | rf-qa-qualitative.md:597-605 | ✅ EXACT | return-type-mismatch worked example present |
| closed-set axis vocabulary (04) | rf-qa-qualitative.md:639 | ✅ EXACT | `{AX-1..AX-5, none}` closed set |
| taxonomy "4 categories not a 5th" (04, 07) | deviation-taxonomy.md:5 | ✅ EXACT | verbatim |
| Regression "only class" unconditional escalation (04) | deviation-taxonomy.md:85 | ✅ EXACT | verbatim |
| "4 categories, not 5. No `unknown` class" (04) | deviation-taxonomy.md:131 | ✅ EXACT | verbatim |
| "5th … rejected in §17.7 Kill List" (04) | deviation-taxonomy.md:154 | ✅ EXACT | verbatim |
| F3 regression test (05) | test_contract_setup_questions.py:272 | ✅ EXACT | `test_probe_pr_question_default_respects_operator_answer` :272 |
| F2 regression test (05) | test_contract_setup_questions.py:211 | ✅ EXACT | `test_augment_app_slug_dedicated_field_selects_observed_slug` :211 |
| F4 regression test + differential (05) | test_contract_setup_validation.py:180, :156 | ✅ EXACT | all_none :180, present differential :156 |
| HL-1: contract_setup 0 on master / 15 on HEAD (07) | git ls-tree | ✅ EXACT | master=0, HEAD=15 |
| branch + HEAD SHA (07) | `harden/qa-reflect-blindspot-pr209` / `46a787da` | ✅ EXACT | git rev-parse confirms both |
| honest-verification precedent test (03) | test_ensemble_unit.py:342 | ✅ EXACT | `test_r2f2_build_reflect_contract_emits_honest_verification_fields` :342 |
| reflect_post builder/writer/reader (03) | runner.py:93 / :120 / :298 | ✅ EXACT | all three defs at cited lines |
| `ReflectResult` telemetry fields (03) | models.py:150-151 | ✅ EXACT | reviewer_isolation:150, audit_tree_dirty:151 (class @:118) |
| Template 02 file (06) | templates/workflow/02_mdtm_template_complex_task.md | ✅ (1515 vs "1516") | exists; wc-l off-by-one (no trailing newline) |
| uc2 example task (06) | 342 lines + start_commit/executor_model/reflect_post | ✅ EXACT | 342L; SHA `63f1a815…`; `sonnet`; `reflect_post: ""` |
| POST-reflect recursion breaker (06) | SKILL.md `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` | ✅ PRESENT | 4 occurrences |

## Per-File Evidence-Density Ratings

| File | Density | Doc-claim tagging | Notes |
|---|---|---|---|
| 01-fx3-questions-resolution.md | DENSE (>80%) | N/A (code-only) | Every SetupAnswers/EvidenceBundle field + deriver line-cited; all verified |
| 02-fx5-gate-helpers.md | DENSE | N/A | 4-module helper inventory with file:line; F4 anchor chain verified |
| 03-fx7-reflect-contract.md | DENSE | properly flags 1 Unverified (skill-path emitter, out of scope) | ensemble/contract/runner/models citations all verified |
| 04-fx2-fx1-briefs.md | DENSE | N/A | Precise on "no internal-consistency lens id"; axis/taxonomy lines exact |
| 05-tests-conventions.md | DENSE | N/A | Test names + line numbers exact; CI/Makefile claims consistent |
| 06-mdtm-template-examples.md | DENSE | flags `.claude/templates` non-existence as resolved-not-gap | template + example citations verified |
| 07-doc-crossvalidate.md | DENSE | RIGOROUS [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] on every claim | git + code loci all verified |

## Confidence

**Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Checklist (evidence-quality lens): (1) claims evidence-based — VERIFIED; (2) no unsupported
assertions stated as fact — VERIFIED; (3) doc-claims properly tagged CODE-VERIFIED/CONTRADICTED/
UNVERIFIED — VERIFIED; (4) spot-check ≥20% load-bearing citations — VERIFIED (~45 checked,
100% accurate); plus per-file density (7 files) all VERIFIED DENSE.

**Tool engagement:** Read: 15 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 5
(20 tool calls > 11 checklist items — no padding; each call targeted a specific citation.)
No web research performed — all verification was local source-truth (Principle 6).

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (1 terminology-looseness, 1 immaterial nitpick)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 07 §Deliverable 6 (lines 127, 130-131) | 07 loosely calls three DISTINCT structures collectively "the internal-consistency lens" ("The lens appears three times (lines 92, 307, 755)"). Those are a Verification Principle (:92), a TDD checklist group (:307), and a doc-qualitative item (:755) — not one renamable lens. 04 §CRITICAL-FRAMING is more precise: the hyphenated lens id does NOT exist (grep-confirmed). Both cite ACCURATE lines and both reach the identical actionable conclusion (FX2 is a scope expansion onto a document-QA agent, not a clean rename). Non-blocking; the merged 04+07 research steers the builder correctly. | None required for correctness. Builder should follow 04's precise framing (augment the task-qualitative Code Compatibility group) over 07's looser "lens" wording. |
| 2 | MINOR (nitpick) | 06 line 15 | 06 states Template 02 is "1516 lines"; `wc -l` reports 1515 (classic no-trailing-newline off-by-one). Immaterial — file exists at the cited path with the cited PART1/PART2 structure. | None. |

## Observations for the Orchestrator Merge (strengths, not defects)

- **07 is exemplary on checklist item 4 (doc cross-validation):** every plan/post-mortem
  claim carries a [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tag, and the
  [CODE-VERIFIED] items were independently re-verified here.
- **Consistent cross-file convergence (not a contradiction):** 04 and 07 INDEPENDENTLY
  conclude that FX1 (5th taxonomy class), FX2 (internal-consistency "rename"), and FX7
  (`verification_ran:false ⇒ degraded`) as originally framed CONFLICT with load-bearing
  existing invariants (deviation-taxonomy "4-not-5" :5/:131/:154; no such lens id; the
  deliberate `_VERIFICATION_SKIP_EXEMPTIONS` incl. `tool-unavailable`). These are correctly
  surfaced as human-decision / reconciliation points, NOT evidence defects. The builder MUST
  carry these forward as design constraints.
- **"F1-F4 already fixed ⇒ regression-guard framing" is VERIFIED accurate** against HEAD
  `46a787da` (07 HL-2, corroborated by 02 §2.1 and 03 §3c). The fixes physically exist in
  the worktree (diagnose file-or-dir, `_path_resolves` all-None collapse, `_evidence_attr`
  answer_attr, dedicated `augment_app_slug`). Task items must be worded as recurrence-guards,
  not live-bug fixes — the research states this explicitly and correctly.

## Recommendations

- **Green light from the evidence-quality lens.** No CRITICAL or IMPORTANT evidence issues.
- The two MINOR items require no research rework; they are guidance for the builder.
- Final research-gate verdict is the orchestrator's to set after merging the parallel
  analyst/gap-detection lens reports; from EVIDENCE QUALITY alone this partition is PASS.

## QA Complete

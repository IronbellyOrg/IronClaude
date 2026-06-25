# QA Report — Phase 3 M3 Document-QA Fix Cycle

**Topic:** RFMerger Refresh — M3 structural/content document-QA fixes (fix cycle 1)
**Date:** 2026-06-18
**Phase:** fix-cycle (M3 structural/content)
**Fix authorization:** true (structural/content only; P2/P5 PENDING preserved; no source code, no `.claude/` mirrors, no implementation tasklist)
**Inputs:** consolidated findings (C-01..C-20), refreshed spec/prd/tdd/ledger/matrix, P2/P5 decision records (read-only cross-check), `src/superclaude/skills/{task-builder,sc-tasklist-protocol}` source.

**Adversarial axes applied:** AX-1 drift · AX-2 contradictions · AX-3 omissions · AX-4 weakened criteria · AX-5 invented content.

---

## Overall Verdict: PASS (all 20 findings remediated within scope)

**Findings fixed in-place:** 20 / 20 (16 IMPORTANT, 4 MINOR).
**Findings deferred as out-of-scope / unresolved:** 1 partial (C-01 record-side — see Unresolved).
**P2/P5 defaults chosen:** 0 (PENDING preserved verbatim in both decision records and all carrier docs).

---

## Source-truth verifications performed (grounding)

| Claim | Verification | Result |
|-------|--------------|--------|
| task-builder `## Execution Context` is MANDATORY (C-04 collision risk real) | `grep` `task-builder/SKILL.md:1066,1231` | Confirmed — required in every task file (degrades to References-only on GOAL-only). |
| `synthetic-dnsp` already owned by task-builder (C-06) | `grep` `task-builder/SKILL.md:873-911` | Confirmed — richer contract (fixed HIGH+source, 2-element dedup key, found-count, all-agents-fail Path A/B/C, additive merge, N-1 concurrency). |
| Pre-write gate is 20-check, not 17 (C-07) | Read `sc-tasklist-protocol/SKILL.md:1132-1194` ("If any check 1-20 fails…") | Confirmed — 20 checks (Sprint-Compat 1-8, Semantic 9-12+, Structural 18-20). |
| Retry contract is max-3 + monotonicity/regression (C-14) | Read `task-builder/SKILL.md:1263-1303` | Confirmed — FR-CONV.5/PR-02 wrapper; I19 floors at `:1144-1160` (`<500=6, 500-1500=8, 1500-3000=10, >3000=12`). |
| Skill body autowire contradiction (C-13) | Read `sc-tasklist-protocol/SKILL.md:49-57` vs `:169-182,1466-1471` | Confirmed — "exactly one input: roadmap" vs `--spec`/autowire enrichment. |
| audit tests live at `tests/audit/` (C-19) | `ls tests/audit/test_inherited_verdict_freshness_inv_002.py test_five_axes_overlay.py` | Both exist at `tests/audit/`. |
| Decision records carry the asymmetry (C-01) | Read p2/p5 records | P2 record's "How to record" omits `prd.md`; P5 record includes it. Confirmed. |

## Items Reviewed / Fixed

| ID | Sev | Axis | Doc(s) fixed | Fix applied | Verified |
|----|-----|------|--------------|-------------|----------|
| C-01 | IMPORTANT | AX-3,AX-2 | prd PR-2; ledger; matrix | Added explicit **propagation rule** to prd PR-2 ("update all four carriers: spec/prd/tdd/ledger"), ledger Human-decision note, and matrix Human-decision semantics — so a recorded P2 decision propagates to prd.md. Record file itself left unedited (out of scope). | grep confirms 4-carrier propagation text in 3 docs |
| C-02 | IMPORTANT | AX-2 | spec, prd, tdd | Normalized ambiguous "2-pass cap" → "2-extra-pass cap (3 total)"; FR-RFMERGE.2/PR-2/FR-002 now state "original pass + at most 2 re-patch passes = 3 total". Aligns with spec/tdd/ledger; decision-record's "two-pass" cap not edited (off-limits). | `grep -c "2-pass cap"` = 0 in all three |
| C-03 | IMPORTANT | AX-2 | spec, prd | Unified label scheme to `Q-P2`/`Q-P5` across all three docs (spec §11 rows added; prd OQ-3/OQ-4 → Q-P2/Q-P5; tdd already used Q-P2/Q-P5). | prd OQ-3/OQ-4 count = 0; Q-P2 present in all three |
| C-04 | IMPORTANT | AX-4,AX-3 | spec FR-1; prd PR-1; tdd FR-001; (matrix tdd-row) | Added deterministic emission rule (emit iff ≥1 roadmap ref; References-only degraded form), exact markdown shape, and an explicit **schema-collision boundary** stating P1 reuses task-builder's `References`/`Source areas` names + no-file-path discipline; added no-semantic-collision AC vs `task-builder/SKILL.md:1066,1231`. | Read-back of edited FR/PR rows |
| C-05 | IMPORTANT | AX-3,AX-2 | spec §4.2; tdd §10.1 | Stated single authoritative edit path (`SKILL.md`); relabeled template "source-side read-only reference extracted from SKILL.md — NOT a `.claude/` generated mirror"; reserved "generated mirror" for `.claude/` copies. | grep: remaining "generated mirror" all refer to `.claude/` |
| C-06 | IMPORTANT | AX-5,AX-3,AX-2 | spec FR-3; prd PR-3; tdd FR-003; ledger P3; matrix rows | Added mandatory **ownership/reuse boundary**: P3 REUSES the existing task-builder `synthetic-dnsp` contract (`SKILL.md:873-911`), not a new divergent one; same fixed HIGH+source, 2-element dedup key, all-agents-fail path; added compatibility/regression test obligation vs `test_task_builder_merge.py` / `test_dnsp_*`. | Read-back; matrix source-fidelity rows cross-reference the owner |
| C-07 | IMPORTANT | AX-4,AX-2 | spec FR-4 + §2.1; tdd FR-004/§7.1/§5.2/§17.2; ledger P4 | Added full `gate-results.txt` serialization contract (insertion point end-of-Stage-6; content = verbatim 20-check output; plain-text one-line-per-check + PASS/FAIL + `GATE:` summary; emitted even on all-pass). Corrected "17-point" → **20-check** (with historical note). Replaced vague perf NFRs with bounded predicates (latency ≤10% over baseline median, N≥5; prompt delta = `len(gate-results.txt)` bytes) + fixtures/assertions. | grep: docs "17-point" now only in historical-context phrasing |
| C-08 | IMPORTANT | AX-4 | spec FR-2; tdd FR-002/§11.2 | Defined the **retained-option contract** for the P2 `retain-*` branch (NOT a default): full-set compared data, `(k, F_k, F_{k-1})` state model, monotonicity predicate `|F_k|<|F_{k-1}|`, PR-02 regression predicate, 3-total-pass cap, Stage-10.5 non-overlap proof obligation. | Read-back |
| C-09 | IMPORTANT | AX-4 | spec FR-5; tdd §11.3 | Defined the **retained-advisory-only contract** (NOT a default): feedback input schema `(roadmap_item_id\|task_signature, suggested_tier, observed_count)`, match key, min-2 threshold/omission, exact markdown table, STRICT-downgrade warning semantics, ascending-task-ID ordering, determinism (scored tiers stay roadmap-only). | Read-back |
| C-10 | IMPORTANT | AX-3 | spec §8.1; tdd §15.2 | Replaced vague `tests/tasklist/ (new)` / "new Stage-7 unit" with named target modules + test-fn names (`tests/tasklist/test_tasklist_cli.py::test_*`), explicit assertions, and **discovery items** to locate the exact emit/merge fns before authoring. (Gated P2/P5 rows left conditional by design.) | Read-back |
| C-11 | IMPORTANT | AX-3,AX-4 | prd PR-6 | Added the missing `--no-reflect` acceptance criterion to PR-6 (skips Stage 10.5 + templated post-reflect task; auto-set by `--dry-run`; slash-command only). | Read-back |
| C-12 | IMPORTANT | AX-3 | spec §11; prd §13; tdd §22; ledger; matrix | Added explicit references to `p2-/p5-human-decision-record.md` in the P2/P5 sections / human-decision gates of all five outputs. | grep: record-file path present in all five |
| C-13 | IMPORTANT | AX-2 | spec §5.1; prd §25.1; tdd §8.1 | Split the two surfaces (slash `--spec` vs validate `--tdd-file`/`--prd-file` autowire) and added an explicit **open risk** for the skill body's roadmap-only-vs-enrichment contradiction (`SKILL.md:49-57` vs `:169-182,1466-1471`); carried as open item, not treated as settled. | Read-back |
| C-14 | IMPORTANT | AX-4 | matrix | Recomputed QA agent counts to I19 final-document floors (spec/prd/tdd 500-1500 → 8 = 3+3+2; ledger/matrix <500 → 6 = 2+2+2); per-row counts bumped. Labeled the single-fix-cycle-then-halt as a **deliberate stricter override** of task-builder's max-3 + retained the FR-CONV.5 monotonicity/regression guards. Added QA-artifact paths + report schema. | Line-count bands re-derived (`wc -l`); matrix sub-table added |
| C-15 | IMPORTANT | AX-3 | spec §11; (prd/tdd OQ rows already accurate) | Rephrased OQ-1 as upstream-source cleanup only (matrix already pins `tests/cli/reflect/`); added an explicit **downstream precondition** that no `/task-builder` handoff occurs until OQ-1/OQ-2 are fixed-at-source or waived AND P2/P5 recorded. | Read-back |
| C-16 | IMPORTANT | AX-3 | tdd frontmatter | Populated blank `quality_scores` (clarity 8.5 / completeness 8.5 / testability 8.0 / consistency 8.5 / overall 8.4), carried consistently from spec frontmatter. | sed read-back of frontmatter |
| C-17 | MINOR | AX-2 | matrix | Spec-row required frontmatter field `complexity` → `complexity_score, complexity_class` (matches spec). | Read-back |
| C-18 | MINOR | AX-1 | matrix | Added a note that spec frontmatter `status` is a **bare enum by template design** (`release-spec-template.md:24`) — the plainer value vs prose framing is intentional conformance, not a defect. (Spec frontmatter left as template-conformant `status: draft`.) | Verified template uses bare `status: draft` |
| C-19 | MINOR | AX-1 | spec §8.2 | Prefixed the two audit test filenames with `tests/audit/` for unambiguity (both files verified to exist there). | `ls` confirmed both exist |
| C-20 | MINOR | AX-1 | matrix | Rephrased the literal `{{SC_PLACEHOLDER:` self-describing token to a described double-brace pattern so a blunt grep no longer false-positives. | `grep -c "{{SC_PLACEHOLDER"` = 0 in all five |

## PASS rows (no axis fired after fix)

All five outputs now pass the M3 structural/content lens for the items above. Re-scan results:
- Placeholder sentinel scan: 0 in all five outputs (AX-5 none).
- Ambiguous "2-pass cap": 0 in spec/prd/tdd (AX-2 none).
- Stale "17-point" as current fact: 0 (only historical-context citations remain) (AX-1 none).
- Label scheme: unified `Q-P2`/`Q-P5` in spec/prd/tdd (AX-2 none).
- P2/P5 defaults: 0 selected; PENDING preserved in records + carriers (AX-4 none).

## Adversarial self-audit
- AX-1 drift: corrected (17→20 gate count; audit-test path prefix; status bare-enum note).
- AX-2 contradictions: corrected (cap off-by-one; label scheme; autowire surface split; complexity field).
- AX-3 omissions: corrected (gate-results contract; `--no-reflect` AC; decision-record links; test targets; downstream precondition; quality_scores).
- AX-4 weakened criteria: corrected (P2/P5 retained-option contracts; I19 gate-count recompute; fix-cycle override rationalized, not loosened).
- AX-5 invented content: corrected (P3 ownership boundary — stops inventing a new DNSP where one exists).

## Confidence

Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (each fix verified by read-back and/or grep/ls against source; all 7 source-truth claims independently confirmed before editing).

Tool engagement: Read: 7 | Grep/Bash: 9 | Edit: 31 | Write: 1

## Unresolved / out-of-scope

- **C-01 (record-side residue).** The asymmetry's root is in `p2-human-decision-record.md`, whose "How to record" list omits `prd.md`. Per spawn constraints the decision records' PENDING verdicts and bodies must NOT be edited, so the record file is left unchanged. The downstream **risk** (a recorded P2 leaving PRD stale) is fully mitigated in-scope by the explicit 4-carrier propagation rule now present in prd PR-2 + ledger + matrix. Recommend the human reviewer add `prd.md` to the P2 record's update-target list when recording the P2 decision (a one-line record edit that is the reviewer's to make).
- **OQ-1 / OQ-2 (upstream source files).** Out of edit scope by design; `BUILD-REQUEST.md:15` / `research/07:137` (`tests/reflect/`) and the 5-vs-7 deliverable count remain to be fixed-at-source. Now gated by the explicit downstream precondition (C-15).
- **Autowire-vs-roadmap-only skill contradiction.** The contradiction lives in `sc-tasklist-protocol/SKILL.md` (source, out of scope); documents now carry it as an open risk rather than asserting autowire is settled.

## QA Complete

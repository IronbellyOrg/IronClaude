# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** reflect Tier-2 fallback model ladder — task file B2 self-containment validation
**Date:** 2026-07-06
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Task file:** `.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/TASK-RF-t2-fallback-ladder-20260706-050832.md`

---

## Adversarial Stance

Assume the task file contains errors. Target: find at least 5 issues. A verdict of 0 issues requires extraordinary evidence of thorough verification across all items.

---

## Items Reviewed

**Item count:** 94 checklist items (`grep -c '^- \[ \]'` = 94), matching the spawn-prompt claim. 89 have `**Step X:**` headers; the remaining 5 are the Post-Completion Actions items (lines 464-472). No orphaned/uncounted items.

| # | Check (lens item) | Result | Evidence |
|---|-------------------|--------|----------|
| 1 | Every item has all 5 B2 components (context+action+output+verification+completion-gate) | PASS | All 94 items contain a completion gate (`grep -v 'mark this item'` → none) AND an "ensuring …" verification clause (`grep -c 'ensuring'` over items = 94). Read all 94 items: each opens with a `Read …` context, a concrete action, a named output path, an "ensuring …" verification, and "Once done, mark this item as complete." |
| 2 | No item references prior context without restating ("see above"/"continue from previous") | PASS | `grep -niE 'see above\|see SKILL\|continue from previous\|as described above'` → none. Cross-item refs (e.g. Step 5.2 "IF Step 5.1 recorded PENDING…", Step 4.4 "the `_T1_PROXY_BINDING=None` sentinel from Step 3.5") always restate the referenced substance inline. |
| 3 | Agent-spawning QA items embed full prompts (not "see SKILL.md") | PASS | Read all G-items (1.G2-1.G4, 2.G2-2.G4, 3.G2-3.G4, 4.G2-4.G4, 5.G1, 6.G2-6.G8): each embeds agent type, `fix_authorization`, the lens name, the adversarial framing string, the specific verify list, and the exact output path. No "see SKILL.md" delegation. |
| 4 | File paths specific (not "the relevant file") | PASS | `grep -niE 'the relevant file\|the appropriate file\|the backend\|the service file'` → none. Every source/test/output path is given absolute or repo-relative and explicit. |
| 5 | Verification criteria measurable | PASS | Every item carries an "ensuring …" clause with checkable conditions (e.g. "all six directories exist", "git diff empty for contract.py", "slot=='T1Model02'"). 94/94. |
| 6 | No batch items — each change-map file / fallback helper / test file has its own item | PASS | 9 changed files each have dedicated item(s); 5 pure helpers → 1.6/1.7/1.8/1.9/1.10; impure controller → 3.4; metadata assembler → 2.1; 7 new reflect tests + 2 extended swarm tests + extended verdict_mapping each own an item. Multi-edit items (3.3 four edits, 4.1 three edits) are all single-file / single-feature, not cross-file batches. |
| 7 | TB-Add-1: no TBD/TODO/FIXME tokens; no title-only items | PASS | `grep -nE '\bTBD\b\|\bTODO\b\|\bFIXME\b'` → single hit "no TODO stub" (Step 3.5), which is descriptive prose forbidding a stub, NOT a placeholder. All items have full 5-field bodies. |
| 8 | TB-Add-8: Context referencing a code surface carries file:line or evidence-absence | PASS (with MINOR gaps) | Existing-surface items cite `~lines N-M` (e.g. 1.3, 2.2, 3.1, 4.1-4.3) or route through research `§`/design `§` citations. New-surface (to-be-created) items cite the driving design section instead of file:line (acceptable — no line exists yet) but do not carry an explicit `<!-- evidence-absence -->` comment. See MINOR-2. |
| D1 | Additive-only invariants encoded | PASS | No-verdict-field-change + no `_LOAD_BEARING_BOOL_FIELDS` member verified in 2.2/2.5/2.6/6.G4; no new `WorkerStatus`/`WorkerResult` field in 1.5/1.6/4.7. |
| D2 | contract.py + swarm/models.py NO-CHANGE verify items exist | PASS | Step 2.6 (`git diff -- contract.py` empty) and Step 4.7 (`git diff -- swarm/models.py` empty) are explicit verify-only items; re-checked at 6.G4. |
| D3 | F1 slot-name test item exists | PASS | Step 1.14 `test_fallback_slot_factory.py` asserts `factory("T1Model02")`→`pool[1]`; Step 1.12 asserts second attempt `slot=="T1Model02"`. Matches design §9 F1 rows. |
| D4 | needs_human_decision HALT (Phase 5) writes PENDING + halts, no auto-default to T2 arm | PASS | Step 5.1: on unconfirmed NAMES writes PENDING to `### Open Questions`, sets `status:"⚪ Blocked"`+`blocker_reason`, HALTs before 5.2, and "DO NOT silently fall back to the design's T2-reuse default." Matches memory `feedback_human_decision_items_must_halt`. |
| G | Factual grounding spot-checks | PASS | `pass.yaml`+`degraded_tier1.yaml` fixtures exist; `temp_tasklist`+`patch_git` conftest fixtures exist; `tests/swarm/{conftest,test_config,test_openai_compat}.py` exist; design.md §7.4/§4.3.1/§9/§10/§11 all exist (no fabricated cross-references). |

---

## Summary

- Checks passed: 13 / 13 lens+domain checks structurally PASS
- B2 structural self-containment: **strong** — all 94 items carry the full 5-field body, specific paths, embedded QA prompts, and are factually grounded (fixtures/conftest/design sections all verified to exist).
- Issues found: 1 IMPORTANT (internal count self-contradiction) + 3 MINOR. Under RF task-integrity zero-tolerance ("any gap regardless of severity = FAIL"), the presence of these defects yields an overall FAIL pending trivial corrections.
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Lines 121, 424, 464 (and echoed in Step 6.G2) | Quantitative claim "**5 new** reflect test files" is wrong. The task creates **7** new reflect test files (Steps 1.11 `test_fallback_classify`, 1.12 `test_fallback_plan`, 1.13 `test_fallback_select`, 1.14 `test_fallback_slot_factory`, 2.4 `test_contract_fallback_metadata`, 3.7 `test_ensemble_fallback_stub`, 3.8 `test_fallback_config`). Design §9 itself lists **6** new reflect test rows (the task adds a 7th, `test_fallback_config.py`, beyond §9). **Line 464 is internally self-contradictory**: it says "the 5 new reflect test files (" and then lists 7 filenames — an item-level self-containment defect. Line 424 tells the final structural-conformance QA lens to "verify the 5 new reflect tests", which will undercount the deliverables (it may not check `test_fallback_config.py` / any 7th file). | Change "5 new" → "7 new" at lines 121, 424, 464 (and reconcile Step 6.G2's coverage list to include `test_fallback_config.py`). Optionally note that §9 lists 6 rows and `test_fallback_config.py` is an authorized expansion for the config-threading test. |
| 2 | MINOR | Throughout (I16 ×6, I20 ×6, M3 ×1, M4 ×2, GAP-2 ×3, (L3) ×7, (L5) ×1) | Provenance shorthand tokens (`per I16`, `per I20`, `M3`, `M4`, `GAP-2`, `(L3)`/`(L5)`) are used but **never defined anywhere in the task file** (no legend/glossary; `grep` for a definition finds only usages). Strict single-item self-containment then relies on the fact that the actionable substance is co-located in each usage (e.g. "serialized per I20 — no other agent edits them"; "max 2 cycles per I16"). It holds, but a fresh executor reading one item in isolation cannot resolve the tag itself. | Add a one-line legend to the `## Execution Context` block mapping I16/I20/M3/M4/GAP-2/L3/L5, OR drop the bare tags and keep only the restated substance. |
| 3 | MINOR | Step 5.3 (line 398) | Output path is ambiguous: "add a network-free test to `tests/cli/reflect/test_ensemble_fallback_stub.py` (**or** a new `tests/cli/reflect/test_resolve_t1_factory.py`)." B2 wants a pinned output. The Post-Completion output-verification item (line 464) Globs for a fixed file list that does **not** include `test_resolve_t1_factory.py`, so if the executor takes that branch the deliverable goes unverified. | Pin Step 5.3 to one destination (recommend a dedicated `test_resolve_t1_factory.py`) and add it to the Step 464 Glob-verification list. |
| 4 | MINOR | Step 1.5 (line 176) | Granularity: one item creates the module docstring + imports + 3 frozen dataclasses (`FallbackDecision`/`QuorumState`/`LadderOutcome`) + the `FALLBACK_ELIGIBLE_STATUSES` frozenset + the `is_fallback_eligible` predicate + the `FallbackTransportFactory` type alias. It is self-contained, but heavy for a single "atomic change" (item-10 atomicity). Borderline, not a hard B2 failure. | Optional: split into "1.5a data types + constant" and "1.5b eligibility predicate + type alias", or accept as the scaffold layer. |

## Confidence Gate

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 3 (each bundling 5-10 grep/ls/section checks — effective verification actions ≫ 13 checklist items)
- No web research performed (all claims verified against local source-of-truth files per Principle 6).
- Every check above cites a specific grep result, file listing, or read line-range. No UNCHECKED or UNVERIFIABLE items.

## Recommendations

1. Correct the "5 new" → "7 new" reflect-test count in lines 121, 424, 464 before execution (IMPORTANT — misdirects the final structural QA lens and self-contradicts within Step 464).
2. Pin Step 5.3's output file and add it to the Post-Completion Glob list (MINOR).
3. Add a shorthand legend (I16/I20/M3/M4/GAP-2/L3/L5) or drop the bare tags (MINOR).
4. Optionally split Step 1.5's scaffold (MINOR).

These are cheap corrections; none touch the load-bearing engineering logic, which is well-specified and factually grounded.

## VERDICT: FAIL

Under RF task-integrity zero-tolerance, the IMPORTANT count self-contradiction (a quantitative claim that mismatches the actual item set AND contradicts itself within Step 464, per task-integrity check 19) plus the MINOR self-containment gaps require correction before the task file is execution-ready. The B2 self-containment *structure* is otherwise excellent (13/13 checks structurally PASS, 94/94 items carry the full 5-field body). Expected fix effort: trivial (3 string edits + 1 path pin + optional legend).

## QA Complete


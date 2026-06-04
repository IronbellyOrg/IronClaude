# QA Report — Research Gate

**Topic:** Durable fix for ID_PATTERNS ↔ tool-write schema drift (add MD, per-step family SoT + assembler, rebuild 4 guard tests)
**Date:** 2026-06-02
**Phase:** research-gate
**Fix cycle:** N/A
**Assigned files:** 01-schema-and-contracts-inventory.md, 02-intentional-vs-drift-investigation.md, 03-tests-and-fixtures.md, 04-template-and-examples.md

---

## Overall Verdict: PASS

(See Issues Found — all 3 issues are MINOR documentation defects; none is a research GAP that would
cause the builder to hallucinate or block task-file construction. Per research-gate rules a research
GAP of any severity = FAIL, but a MINOR documentation/prose defect inside an otherwise-evidenced,
actionable research set is not a coverage GAP. No CRITICAL/IMPORTANT gap exists; the family-SoT design
is fully actionable without further research. Verdict PASS with 3 MINOR notes for the builder.)

---

## Zero-Trust Spot-Check Results (all 5 prompt items independently verified against source)

### Spot-check 1 — Schemas omit MD; M1-D01 rejected today; FR/NFR/SC/G/D match SoT verbatim — CONFIRMED
- `ID_PATTERNS` read at `src/superclaude/contracts/__init__.py:64-77` (Bash sed): 6 families
  `MD, FR, NFR, SC, G, D`, MD ordered BEFORE D, bodies verbatim:
  `MD=M\d+-D-?\d+`, `FR=FR-\d+(?:\.\d+)?`, `NFR=NFR-\d+(?:\.\d+)?`, `SC=SC-\d+`, `G=G-\d+`, `D=D-?\d+`.
  Exactly as R1 §1.1 and R3 §0 claim (incl. R1's note that NFR is the broader sub-ID variant — the
  header comment at `:52-56` confirms this is intentional).
- All 4 schema `roadmap_ids.items.pattern` strings read directly (Bash grep `D-?`):
  extract `:134`, extract_tdd `:218`, generate `:140`, merge `:156` — line numbers and full arm
  strings match R1 §2 and R3 §3a **verbatim**, including extract's COMP-before-DM ordering anomaly.
  None contains `M\d+-D` / MD.
- **Core bug reproduced live** (`uv run python` + `re.match`): `re.match(pattern,"M1-D01")` → `False`
  for all four (extract/extract_tdd/generate/merge). Exactly R3 §3a's reproduction. The bug is real.
- merge pattern == generate pattern byte-identical (12 arms incl OQ): confirmed by direct read.

### Spot-check 2 — R2 INTENTIONAL verdict (extract_tdd $comment + 6 arrays; git c542b6bf) — CONFIRMED, NOT over-claiming
- extract_tdd `$comment` at `:5` read directly — describes the step ROLE (extract DEFINES the
  universe), is SILENT on the family set. R2 Finding 1 states exactly this ("comments are SILENT on
  the intent question") — an honest, non-inflated reading.
- extract_tdd's 6 typed entity arrays confirmed present (Bash grep): `data_models:130`,
  `api_specifications:144`, `component_inventory:158`, `testing_strategy:175`, `migration_plan:188`,
  `operational_readiness:201` → grounds DM/API/COMP/TEST/MIG/OPS. extract has ONLY
  `component_inventory:86`. R2 Finding 3's structural-alignment argument is grounded in real arrays.
- **Git authorship**: `git log --diff-filter=A` shows ALL FOUR schemas created in `c542b6bf`
  ("R1.4 tool-write migrations"). `git show c542b6bf -- extract.schema.json` shows the extract
  pattern authored at creation already as `...|COMP-\w+|DM-\w+)$` (COMP-before-DM present from day
  one). The only later touch (`d191d161`) changed ONLY the `extraction_mode` $comment, NOT
  roadmap_ids — verified by diffing d191d161. Exactly R2 Finding 2.
- **Per-step-assembler recommendation is JUSTIFIED, not over-claiming.** R2 explicitly concedes
  "co-authorship alone does not prove correctness" and rests the verdict on structural array
  alignment (decisive evidence), not on the comments. The recommendation to keep per-step family
  sets is grounded: a flat one-pattern assembler WOULD let extract emit API/TEST/MIG/OPS it has no
  array to back (verified: extract lacks those 5 arrays). R2 is appropriately hedged.
- R2's option-(b) rejection rationale independently verified: `spec_parser.py:329-331` builds
  `_REQUIREMENT_PATTERNS` by iterating `ID_PATTERNS.items()`, and `extract_requirement_ids`
  (`:342`) regex-scans spec text with them — so promoting COMP/DM/... into ID_PATTERNS WOULD
  pollute spec extraction. Rationale is sound.

### Spot-check 3 — MD⊂D substring trap + frozen-tuple/substring guard tests + exact-arm requirement — CONFIRMED
- `D-?\d+` IS a literal substring of `M\d+-D-?\d+` → verified live (`'D-?\d+' in 'M\d+-D-?\d+'`
  → `True`). The trap is real exactly as R1 §1.1 and R3 §39 state.
- All 4 guard tests read directly: extract (`:130-143`), generate (`:219-236`), merge-pin
  (`:271-279`). Confirmed: frozen tuple `("FR","NFR","SC","G","D")` (MD ABSENT) + substring
  `ID_PATTERNS[family] in pattern`; extract_tdd/generate/merge add a frozen
  `("DM-","API-","COMP-","TEST-","MIG-","OPS-")` prefix loop. merge==generate is the only exact
  `==` guard. Matches R3 §1-2 exactly.
- The exact-arm requirement R3 §4 prescribes (split on `|`, assert `body in arms`) is the correct
  durable defeat of the trap and is sound. **However see Issue #2 (MINOR): R3 §93's intermediate
  prose is self-contradictory** — it first asserts a keys-driven substring fix "still FALSELY
  PASSES," then self-corrects mid-paragraph. The final stated requirement (arm-level matching) is
  correct and the builder note flags "confirm both directions," so it is not blocking, but the muddled
  reasoning should be cleaned so the builder is not misled.

### Spot-check 4 — 55 extra-family usages + OQ-only-in-open_questions nuance — CONFIRMED EXACT
- Counted live (Bash grep `"(DM|API|COMP|TEST|MIG|OPS|OQ)-..."`): extract 5, extract_tdd 19,
  generate 5, merge 23, test_merge_completeness 2, test_cosmetic_remediator 1 → **TOTAL 55**.
  Matches R3 §3's per-file breakdown (5/19/5/23/2/1) and grand total exactly.
- OQ nuance verified: `OQ-1` in generate (`:118`) and merge (`:143`) sits inside
  `open_questions[].id` (read surrounding context — it is under an `open_questions:` array), NOT
  inside any `roadmap_ids` array. So removing OQ from the generate/merge roadmap_ids pattern would
  NOT break a validated roadmap_ids fixture. R3 §130-133's load-bearing nuance is CORRECT.
- extract fixture roadmap_ids (`:108-114`) DOES contain `DM-extraction` (read directly) — so R2's
  reconciliation "KEEP DM in extract" (dropping it would break this fixture) is grounded. The
  families that ARE in validated arrays (DM/API/COMP/TEST/MIG/OPS) must stay. CONFIRMED.
- Baseline suite reproduced live: `uv run pytest tests/roadmap/ -k tool_write -q` →
  **157 passed, 1 skipped, 1808 deselected** — byte-matches R3 §242's captured baseline.

### Spot-check 5 — Unsupported assertions / coverage gaps / actionability — see Issues; design IS actionable
- No fabricated file paths, line numbers, or claims found. Every load-bearing citation I checked
  resolved to the real file at the real line with the claimed content.
- R4's template/example claims verified: template `02_mdtm_template_complex_task.md` exists (1204
  lines), L5 Conditional-Action pattern at `:785-797` verbatim, I16 fix-cycle table at `:619` says
  `task-integrity | 2 | ...Open Questions` (matches R4 §5), prior example
  `TASK-RF-20260602-060714.md` exists with the exact phase structure R4 §6 maps (Investigation Gate
  / Decision Gate / Conditional Implementation / Final Validation / terminal Task-Integrity QA).
- The family-SoT design (per-step map + entity-family registry + `roadmap_ids_pattern()` assembler,
  appended to `__all__`) is fully actionable: SoT location, the 4 per-step family sets, the MD-before-D
  ordering, the arm-level guard approach, the 3 validation gates, and the fixtures-to-keep-green are
  all concretely specified. No further research is required before the builder runs.

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (Status: Complete + Summary) | PASS* | All 4 files have a "Status: Complete" footer + Summary section. *Files 01/02/04 still carry "In Progress" in their HEADER line (Issue #1, MINOR) — footer authoritative, not a coverage gap. |
| 2 | Evidence density | PASS | Dense (>80%). Every spot-checked claim cited file:line and resolved correctly against source. |
| 3 | Scope coverage | PASS | Contracts SoT, 4 schemas, runtime path, executor, arch_lint, 6 test files, template, prior example all examined across the 4 files; no key file left undiscussed within assigned scope. |
| 4 | Documentation cross-validation | PASS | Doc/`$comment`-sourced claims (R2 Finding 1) explicitly marked SILENT/structural; git-verified; no untagged doc-only architecture claim. R3 carries an `[UNVERIFIED]` convention and uses it honestly. |
| 5 | Contradiction resolution | PASS (1 MINOR) | Cross-file claims (line numbers, arm strings, 55 count, baseline) are mutually consistent across 01/02/03. One INTRA-file prose contradiction in R3 §93 (Issue #2, MINOR). |
| 6 | Gap severity | PASS | No CRITICAL/IMPORTANT research gap. R2/R3 defer the extract-DM call to each other and BOTH independently land on KEEP DM (fixture-grounded) — the cross-reference resolves, not a gap. |
| 7 | Depth appropriateness (Deep tier) | PASS | R1 §4 traces the end-to-end runtime data flow (load_schema → validate_tool_output → validate_id_subset → persist) confirming schema-gate-before-subset; verified against tool_writer.py order. |
| 8 | Integration point coverage | PASS | Schema↔contracts↔tool_writer↔executor↔arch_lint↔tests integration points all documented; executor wiring (generate/merge id-check vs extract plain) covered in R1 §5. |
| 9 | Pattern documentation | PASS | MDTM item shape (B2 6-element), L5 decision-gate pattern, anchor-free→wrapped convention, arm-level guard pattern all documented. |
| 10 | Incremental-writing compliance | PASS | Files show iterative structure (per-finding sections, in-line `[NOTE]`/`[CAVEAT]`/`[UNVERIFIED]` annotations, "re-verified this session" markers) — not one-shot perfection. |

---

## Summary
- Checks passed: 10 / 10 (3 carry MINOR notes)
- Checks failed: 0
- Critical issues: 0  | Important issues: 0  | Minor issues: 3
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | 01 hdr `:6`, 02 hdr `:7`, 04 hdr `:5` | Header `Status:` line still reads "In Progress" while each file's footer says "Status: Complete". Stale header marker. | Update the three header Status lines to "Complete" for consistency. Does not affect content or actionability. |
| 2 | MINOR | 03 §93 (the "WHY all four silently passed" para, reason 2) | Intermediate prose is self-contradictory: first asserts a keys-driven substring fix "still FALSELY PASSES," then self-corrects ("is the wrong way round … WOULD correctly fail-to-find MD"). Final requirement (arm-level matching) is correct but the muddled reasoning could mislead the builder about WHY substring is unsafe. | Rewrite the paragraph to state the single correct trap direction: once MD is added to a schema, the bare-`D` arm check `D-?\d+ in pattern` passes trivially because `D-?\d+ ⊂ M\d+-D-?\d+`, so substring cannot prove the `D` arm is its own arm. Keep the arm-level conclusion. |
| 3 | MINOR | 04 §2 line refs (e.g. "PART 2 lines 890-1205") | Template upper-bound cited as 1205; file is 1204 lines (off-by-one). Other line refs (785-797, 619, prior-example phases) verified accurate. | Trivially adjust upper bound to 1204; immaterial to the build. |

## Actions Taken
None — fix_authorization: false. Report-only.

## Recommendations
- Green light for the task-builder to proceed to synthesis/task-file construction. The 3 MINOR notes
  are documentation hygiene; the builder should (a) treat the file footers as authoritative status,
  (b) use R3 §4's arm-level guard approach (NOT the muddled §93 reasoning) and the explicit "confirm
  both directions" builder note, and (c) keep DM in extract's family set per the fixture-grounded R2/R3
  consensus.
- The family-SoT design is actionable without further research: per-step family map + entity-family
  registry + `roadmap_ids_pattern()` assembler in `superclaude.contracts` (appended to `__all__`),
  MD lands in all four via the spec-family base, arm-level keys-driven guards defeat the MD⊂D trap,
  and the 3 validation gates (lint-architecture, verify-sync, pytest -k tool_write) are specified.

---

## Confidence Gate

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep/Bash-grep: ~14 | Glob/ls: 2 | Bash(python/git/pytest): 8
(Tool calls ≥ checklist items — each Bash/Read targeted a specific claim: ID_PATTERNS body, the 4
schema patterns, live M1-D01 reproduction, the MD⊂D substring relation, git authorship of all 4
schemas, the 6 extract_tdd arrays, the 4 guard-test bodies, the 55-usage count, the OQ-in-open_questions
context, the extract DM fixture, the spec_parser/arch_lint consumers, the baseline pytest run, and the
template/prior-example line references.)
No web research performed (all verification was source-truth-local; no external URL/standard/API claims
in scope).

Every checklist item is marked VERIFIED with cited tool output above. No UNCHECKED or UNVERIFIABLE items.

## QA Complete

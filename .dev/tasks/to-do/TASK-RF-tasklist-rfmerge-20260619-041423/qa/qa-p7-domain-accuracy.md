# QA Report — Phase 7 Cross-Cutting (Domain Accuracy)

**Topic:** RFMerger tasklist — cross-cutting `--spec §22` reconciliation + HALT OQ + hygiene/carried-gap tests
**Date:** 2026-06-19
**Phase:** doc-qualitative (lens: "domain-accuracy vs research/07/08 pins + spec")
**Fix cycle:** N/A (fix_authorization: false — REPORT-ONLY)
**Stance:** ADVERSARIAL — assumed the cross-cutting edits misrepresent research/07 §2 / R-12 / R-13 / spec §5.1/§11; hunted for >=5 discrepancies.

---

## Overall Verdict: PASS

No discrepancy found across the four mandated claims. Every pinned behavior is byte-accurately reflected; no pin dropped; no behavior introduced beyond the pins. The adversarial hunt surfaced four candidate-discrepancies (C1-C4 below); each was investigated against source and dismissed with evidence. Reporting PASS, with the dismissed candidates documented so the reader can audit the reasoning rather than trust a bare "0 issues."

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | §2b bounded edit matches research/07 §2b verbatim | PASS | `diff` of research/07 lines 104-121 (proposed-replacement block) vs SKILL.md lines 49-66 → **IDENTICAL** (byte-for-byte). |
| 2 | §2c HALT Open Question matches verbatim | PASS | Task OQ-1 (line 737) question body byte-identical to research/07 §2c (line 130); only the `**[OQ-1] [needs_human_decision...]**` marker replaces the research's `> **OPEN QUESTION (human decision required):**` framing prefix + a provenance parenthetical appended. Substantive text verbatim. |
| 3 | R-12 stale-token set fully covered by the test | PASS | `test_no_stale_tokens_in_tasklist_source` asserts all 5 R-12 tokens (`sc:task-unified`, `/rf:`, `.gfdoc`, `llm-workflows`, `/config/.claude`) + the typed-`StageError` operative forms absent; the one permitted `StageError` disclaimer string exists at SKILL.md:1407 (test would pass). |
| 4 | Carried-gap behaviors accurately pinned | PASS | All 4 carried-gap assertion strings present in source (skip-when-disabled, `--no-reflect`/`--dry-run` skip, `PASS\|PARTIAL\|FAIL`, "bundle ships regardless"); `test_slash_flag_parsing` exercises the real Click `tasklist validate` surface. |
| 5 | Removal path NOT applied (R-13 §2c / OQ-1 HALT discipline) | PASS | All 4 enrichment section headers present (§3.x:139, §4.1a:178, §4.4a:278, §4.4b:301); 17 occurrences of `--spec`/`--tdd-file`/`--prd-file`; OQ-1 status PENDING/HALTS, no auto-default. |
| 6 | No behavior beyond the pins (scope) | PASS | Edit rewrites only opening sentence (49) + closing "only source of truth" sentence (57→60-66); middle bullet list verbatim; no flag/algorithm/emitter/gate touched. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY)

---

## Claim-by-Claim Verification (pin cited + actual edit cited)

### Claim 1 — §2b bounded edit matches research/07 §2b verbatim — PASS

- **Pin:** research/07 §2b "Exact verbatim proposed replacement (behavior-preserving)" fenced block, `07-citation-crossval-and-spec.md:104-121`.
- **Actual edit:** `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:49-66`.
- **Method:** `diff /tmp/r07_2b.txt /tmp/skill_edit.txt` (research §2b block vs SKILL.md 49-66) → `IDENTICAL`.
- **Result:** Byte-for-byte match. Opening sentence reframes roadmap as "one **required** input" + "**optional supplementary inputs** (`--spec`...)"; closing reframes to "**primary source of truth** for task generation" with R-### traceability + enrich-not-originate guarantee. Matches R-13 §2b settlement ("roadmap = PRIMARY; `--spec`/autowired = OPTIONAL supplementary; changes NO runtime behavior/flags/algorithm").

### Claim 2 — §2c HALT Open Question matches verbatim — PASS

- **Pin:** research/07 §2c OPEN QUESTION, `07-citation-crossval-and-spec.md:130`; binding settlement research/08 R-13 part 2 (`08-gapfill-resolutions.md:80`).
- **Actual edit:** Task-file OQ-1, `TASK-RF-tasklist-rfmerge-20260619-041423.md:737-740`.
- **Method:** Direct line comparison.
- **Result:** Question body verbatim — identical from "Does the maintainer instead want to **REMOVE..." through "...**MUST NOT be auto-applied.**" The delete-list (§3.x 130-147, §4.1a 169-183, §4.1b 185+, §4.4a 246-267, §4.4b 269+, Stage-7 1297-1308, Stage-10.5 1466-1471, `--spec`/`--tdd-file`/`--prd-file` + argument-hint line 9) is reproduced verbatim. The `**[OQ-1] [needs_human_decision: true | MUST-HALT]**` prefix correctly encodes the R-13/`feedback_human_decision_items_must_halt` halting requirement; Status = "PENDING (HALTS — do not auto-apply)... does NOT auto-default to either direction" (line 740). Default applied = §2b bounded edit ONLY; removal NOT applied (line 738).

### Claim 3 — R-12 stale-token set fully covered by the test — PASS

- **Pin:** research/08 R-12 (`08-gapfill-resolutions.md:73-74`): test asserts NONE of `sc:task-unified`, `/rf:`, `.gfdoc`, `llm-workflows`, `/config/.claude` appear as operative edit target / current guidance; plus typed `StageError` 0 operative hits.
- **Actual test:** `tests/tasklist/test_tasklist_cli.py:664-679` (`test_no_stale_tokens_in_tasklist_source`).
- **Result:** All 5 R-12 tokens covered in the loop (line 667), 1:1 with the pin — no token dropped. `StageError` covered via 4 operative forms (`raise`/`class`/`except`/`(`, lines 672-678) plus an assertion that the single permitted no-reuse disclaimer string IS present (line 679); that disclaimer exists at SKILL.md:1407 verbatim — so the test passes rather than false-failing. This matches R-12's "operative" framing (the descriptive `/rf:` / `.gfdoc` legacy-ecosystem mentions noted in research/07 §3 live in task-builder/agents/templates, NOT in the tasklist-generator source the fixture reads → correctly out of scope for this assertion).

### Claim 4 — carried-gap behaviors accurately pinned — PASS

- **Pin:** Phase-7 summary acceptance #3 (each carried-gap test pins its behavior and would FAIL if regressed); carried gaps = no-reflect skip of Stage 10.5, all-verdicts-ship advisory, slash-flag parsing.
- **Actual tests:** `test_no_reflect_skips_stage_10_5` (681-686), `test_stage_10_5_advisory_ships_all_verdicts` (688-693), `test_slash_flag_parsing` (695-705).
- **Result:** Each asserts a real source string (all 4 confirmed present in SKILL.md via grep) — not a stub. `test_slash_flag_parsing` invokes the real `tasklist_group` `validate` Click command, checks `--roadmap-file/--tasklist-dir/--model/--max-turns` in `--help`, and asserts a bogus flag → non-zero exit. Substantive, regression-sensitive (would FAIL if the skip-clause or verdict-ship prose were removed).

---

## Adversarial candidates investigated and dismissed (evidence trail)

- **C1 (drift suspicion — OQ-1 not byte-verbatim):** OQ-1 prepends a marker and appends "(Verbatim from research/07 §2c; binding settlement research/08 R-13.)". Investigated: the appended text is provenance metadata, not part of the question; the substantive question is byte-identical. The marker substitution is mandated by `feedback_human_decision_items_must_halt` (HALT encoding). **Dismissed** — framing/provenance, not content drift.
- **C2 (R-12 coverage gap — "or generated output"):** R-12 says assert absence "in changed source **or generated output**"; the fixture reads only the one SKILL.md source file. Investigated: this Phase-7 test is the *source-of-truth* content gate (header comment lines 28-32); generated-output staleness is a distinct surface and the §3 stale tokens are absent from the generator source, so generated output (derived from it) cannot reintroduce them via this edit. **Dismissed** — source-side coverage is complete for the changed source; no token was dropped from the set.
- **C3 (dangling cross-refs in the §2b edit):** The new prose references §3.x, §4.1a/§4.4a, §10.5. Investigated: §3.x→139, §4.1a→178, §4.4a→278 all resolve to real headings; Stage 10.5 present. **Dismissed** — no orphaned forward-references.
- **C4 (removal silently partially applied):** Investigated enrichment-site presence: 4/4 headers present, 17 `--spec`/`--tdd-file`/`--prd-file` occurrences. **Dismissed** — removal path fully un-applied, consistent with OQ-1 HALT.

No candidate survived scrutiny. The PASS is evidence-backed, not a default.

---

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** 6 checks + 4 dismissed candidates, each backed by a tool result (diff, grep, line read).
2. **Files read/inspected:** phase-7-output-summary.md; research/07 (full); research/08 (full); SKILL.md:44-78 + 1407 + grep across full file; spec.md:545-558 + 741-784; task file OQ region 725-744 + items 83/181/528/533-534; tests/tasklist/test_tasklist_cli.py:28-46 + 650-706.
3. **Why trust this PASS:** the one binary-verbatim claim (Claim 1) was settled by an exact `diff` returning IDENTICAL; Claim 2 by direct line comparison showing byte-identical question body; Claims 3-4 by grepping every test-asserted string against source and confirming the assertions would pass (not false-fail). The four adversarial candidates are documented with the specific evidence that dismissed each.
4. **Web research:** none performed (review is entirely local-file-bound); Tavily-first N/A this review.

## Self-Audit — Reliance Audit (PR-04, INV-019)
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt → standalone behavior; all structural+semantic checks run with own tool engagement (no reliance to audit).
- **(b) Independent semantic checks:** §2b verbatim equivalence (diff IDENTICAL); OQ-1 question-body verbatim equivalence (line compare); R-12 token-set 1:1 coverage + StageError-disclaimer presence (grep SKILL.md:1407); enrichment-site non-removal (grep 4 headers + 17 flag occurrences).

## Confidence
**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 4

## QA Complete

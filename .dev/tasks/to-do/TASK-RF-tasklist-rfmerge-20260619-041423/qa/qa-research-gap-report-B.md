# QA Report — Research Gate (Partition B of 2)

**Topic:** RigorFlow Merger tasklist — test/template/settlement gap detection
**Date:** 2026-06-19
**Phase:** research-gate
**Lens:** gap-detection (TEST / TEMPLATE / SETTLEMENT side)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

**Assigned files (partition B):**
- research/05-tests-and-verification.md
- research/06-template-and-examples.md
- research/07-citation-crossval-and-spec.md

**Reference:** spec §8 test plan + TDD §15.2

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Verification actions performed (evidence)

- **Read** all 3 assigned research files in full (R05 218 lines, R06 367 lines, R07 178 lines).
- **Read** spec.md §8 Test Plan (lines 649-738) — the authoritative §8.1 unit-test inventory.
- **Read** tdd.md §15.2 Test Cases (lines 839-885) — the authoritative FUTURE test inventory.
- **Read** tdd.md §22 Open Questions (lines 1068-1083) and spec.md §5.1/§11 (lines 540-558, 750-755) for the `--spec` settlement framing.
- **Read** spec.md §5.3 Phase Contracts (lines 582-609) for P1-P5 runtime contracts incl. P2 cap + P3 fixtures.
- **Bash/Grep verified:** baseline `tests/tasklist/` = **71 collected** (R05 claim confirmed); `tests/reflect/` ABSENT, `tests/cli/reflect/` PRESENT (R05 confirmed); `tests/cli/prd/test_prompts.py` has 5 staleness markers, `tests/tasklist/test_prd_prompts.py` has 0 (R05 disambiguation confirmed); worked-example file, template 02, `_halt_emitter.py`, `test_docs_cli_parity.py` all EXIST.
- **Grep verified:** template I22 qa_intensity table (`:802-812`) and I21 applicability (`:759-789`) — both R06 citations are verbatim-accurate.

Tool engagement: Read: 7 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 4

---

## Lens-by-lens findings

### Lens item 1 — Every spec §8.1 / TDD §15.2 test mapped to a target file?

I cross-referenced the spec §8.1 (8 rows) + TDD §15.2 (12 rows) authoritative inventory against R05 §2's NEW-TEST MAPPING table. Result:

| Spec/TDD test | In R05 §2 mapping? | Target-file correct? |
|---|---|---|
| `test_execution_context_block_shape` (P1) | YES | YES — `tests/tasklist/test_tasklist_cli.py` + content-gate option |
| `test_dnsp_synthetic_provenance` (P3) | YES (dual-homed) | YES |
| `test_dnsp_all_agents_fail_escalates` (P3) | YES | YES |
| `test_gate_results_passthrough` (P4) | YES | YES |
| `test_no_reflect_skips_stage_10_5` (gap) | YES | YES |
| `test_stage_10_5_advisory_ships_all_verdicts` (gap) | YES | YES |
| `test_slash_flag_parsing` (gap) | YES | YES |
| `test_sc_task_naming` | YES | YES |
| stale-token-prevention | YES (path-disambiguated, verified) | YES |
| P2 bounded-loop guards | YES | YES |
| P5 advisory determinism | YES | YES |
| **PRD/TDD autowire (existing, stay-green)** | **PARTIAL** | See MINOR-1 |
| **Retained-feature gate `test_task_builder_merge.py` (existing, stay-green)** | YES (content-gate model §1.6) | YES |
| **Integration: `tests/audit/test_inherited_verdict_freshness_inv_002.py` + `test_five_axes_overlay.py`** | **NO** | See IMPORTANT-1 |

**Coverage of the *new/active* unit tests is COMPLETE** — every test the builder must author appears in R05 §2 with a correct target file and a model-test to mirror. Two integration-suite items are under-surfaced (below).

### Lens item 2 — Are P2 (5 sub-assertions) and P5 (determinism) test SHAPES concrete enough?

**P2 — concrete enough, with the 2-vs-3 cap correctly disambiguated.** R05 §2 P2 row enumerates all five sub-assertions: (a) full-set re-validation, (b) monotonicity strict-shrink-or-halt, (c) regression-precedence, (d) 1-extra-pass cap = **2 total** (R05 explicitly flags "NOT the 3-cap of task-builder; pin the literal from spec — R03 owns"), (e) Stage-10.5 non-overlap. Each maps to a concrete `tests/audit/` model (`test_monotonicity_halt_F_5_5_5.py`, `test_regression_halt_pass1_fail2.py`) with byte-exact halt-string assertions and mandatory negative cases. The cap value is spec-confirmed at spec.md:606 (`1_extra_pass_cap_2_total ... = 2 total (adversarial-validation.md:141)`). **PASS.**

**P5 — concrete enough but the determinism predicate is INCOMPLETELY stated (see IMPORTANT-2).** R05 §2 P5 row gives two assertions: (1) scored-tier slice identical advisory-on-vs-off, (2) same roadmap → same scored tiers, modeled on the `build(...) == build(...)` baseline-equivalence idiom (`test_prd_prompts.py:96-101`). This proves "advisory does not mutate scored tiers" correctly. **However**, R05 does not surface the *byte-identical-bundle* determinism nuance that spec NFR-RFMERGE.1 (spec.md:627) and §3 (spec.md:114) make explicit: the **advisory itself varies with `feedback-log.md`**, so byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)` tuple — only the *scored tiers* are roadmap-only-deterministic. A P5 determinism test that asserts whole-bundle `==` across runs would be WRONG (the advisory legitimately varies). R05's scored-tier-slice framing is correct but it does not warn the builder away from the broader-bundle `==` trap. This is an IMPORTANT precision gap.

### Lens item 3 — How to test SKILL.md prose changes (content-gate vs Python)? Is the stale-token model applicable?

**Content-gate model: PRESENT and correct.** R05 §1.6 documents `tests/skills/test_task_builder_merge.py` as the content-gate model (source-of-truth `parents[2]` paths, module-scoped `*_text` fixtures, parametrized marker lists, `.count(tag) >= 2`), and §1.2/§1.5 give the prompt-substring + `build(...) == build(...)` Python alternatives. R05 §2 + §1.9 + the "Key disambiguation" note (§2 footer) correctly state the Python-vs-content-gate choice depends on **where the merged spec lands the logic (R01/R03 own)** — this is the right framing; it is NOT a gap because the spec itself leaves several of these as "and/or" (spec.md:660-663 says "`tests/tasklist/test_tasklist_cli.py` ... and/or `tests/skills/test_task_builder_merge.py`").

**Stale-token model: CONFIRMED applicable + path-disambiguated.** R05 §5 confirms `tests/cli/prd/test_prompts.py` (NOT `tests/tasklist/test_prd_prompts.py`) carries the staleness model — I independently verified: the former has 5 staleness markers, the latter 0. R05's disambiguation is correct and load-bearing (a builder mirroring the wrong file would find nothing). **PASS** — but see MINOR-2 on the token-set mismatch.

### Lens item 4 — Does R06 surface MISSING template obligations (M4 fidelity-gate applicability for spec→implementation; I22 counts)?

**I22 qa_intensity counts: COMPLETE.** R06 §5 reproduces the full I22 table (lite/standard/full × intermediate/final/fidelity/fix-cycles/verify) — I verified it verbatim against template `:802-812`. The default mapping (Quick→lite, Standard→standard, Deep/Heavyweight→full) is captured. **PASS.**

**M4 fidelity-gate applicability for a spec→implementation transformation: UNDER-RESOLVED (see IMPORTANT-3).** R06 §4 and §11-item-4 conditionalize M4 as "(+ M4 if source docs)" but never explicitly resolve the central question for THIS task: the implementation tasklist the builder emits is *itself* a spec→implementation transformation that reads spec/prd/tdd to produce output. Template I21 (`:759-789`, which I verified) lists "Any task where the orchestrator reads source documents to produce output" as MANDATORY for M4 — and carves out ONLY "Pure transformation tasks where the output format is mechanically derived (e.g., rename operations)." A spec→tasklist generation is inference-based (spec.md:543 calls `/sc:tasklist` "inference-based generation"), NOT a mechanical rename — so M4 is plausibly MANDATORY for the builder's own task file. R06 does not adjudicate this; it leaves "(+ M4 if source docs)" ambiguous. The builder needs an explicit verdict.

### Lens item 5 — Is the `--spec §22` residual Open Question correctly framed as needs_human_decision HALT (not auto-applied)?

**YES — correctly framed by R07 §2c, and consistent with the spec.** R07 §2 splits the `--spec` contradiction into (§2b) a bounded, behavior-PRESERVING doc-consistency edit (amend the stale "exactly one input"/"only source of truth" prose at SKILL.md:49-57 to acknowledge `--spec` as optional supplementary — zero algorithm/flag/gate change) and (§2c) a residual behavior-CHANGING ambiguity (does the maintainer instead want to REMOVE `--spec` enrichment to make the generator truly roadmap-only?) that "MUST NOT be auto-applied" and is encoded as a `needs_human_decision` HALT per `feedback_human_decision_items_must_halt`. I cross-checked this against the spec: spec.md:553-558 ("This refresh does **not** treat autowire-vs-roadmap-only as settled ... carried as an open item") and spec.md:753 ("The `--spec` exact-input-contract §22 item remains a carried implementation-time design risk ... NOT a handoff blocker"). R07's framing matches the spec exactly: the bounded §2b edit is safe to encode as a normal item; the §2c removal path is the human-gated HALT. **PASS.** One caveat (MINOR-3): R07 labels its section "`--spec §22`" but the actual TDD §22 table does NOT contain this item — it lives in spec §5.1/§11 + research/07. The "§22" tag traces to the TDD's input-contract numbering, not the Open-Questions table; the builder should anchor to spec §5.1/§11 + spec.md:753, not TDD §22.

### Lens item 6 — Any gap in sync/lint verification (make verify-sync, ruff format --check)?

**NO gap — COMPLETE and correct.** R05 §4 specifies the full ordered gate chain: `make sync-dev` → `make verify-sync` → `make lint` (ruff check ONLY) → `uv run ruff format --check src/ tests/` (SEPARATE CI gate `make lint` omits). It correctly cites the project memory `make lint != CI ruff format` and notes `tests/cli/test_verify_sync_hooks.py` (V1-V7) covers verify-sync itself + must not run under xdist. spec §5.2 Sync gate + tdd §15.1 Sync row corroborate. **PASS.**

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| IMPORTANT-1 | IMPORTANT | R05 §2 / §3 | The two **integration-test audit suites the spec/TDD name as stay-green gates** — `tests/audit/test_inherited_verdict_freshness_inv_002.py` and `tests/audit/test_five_axes_overlay.py` (spec.md:677, tdd.md:865) — are NOT listed in R05's UV-command section (§3) or its mapping (§2). R05 §3 lists the DNSP/monotonicity audit *models* but omits these two named retained-feature integration gates. A builder following R05 §3 verbatim would not run them. | Add `tests/audit/test_inherited_verdict_freshness_inv_002.py tests/audit/test_five_axes_overlay.py` to R05 §3's integration UV command (the "RFMerger retained-feature gate" row from spec §8.2 / tdd §15.2-integration). |
| IMPORTANT-2 | IMPORTANT | R05 §2 (P5 row) | The P5 determinism test shape is correct for *scored tiers* but does not warn the builder that a **whole-bundle `==` determinism assertion is INVALID** — the advisory legitimately varies with `feedback-log.md` (spec NFR-RFMERGE.1 / spec.md:627, §3 / spec.md:114: byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)`). Without this, a builder could author a determinism test that asserts the full bundle is byte-identical and get a false RED (or, worse, weaken P5 to suppress the variance). | R05 P5 row should add: determinism asserts on the **scored-tier slice only** (roadmap-only-deterministic); whole-bundle byte-identity additionally requires fixing `feedback-log.md` — do NOT assert whole-bundle `==` across differing feedback logs. |
| IMPORTANT-3 | IMPORTANT | R06 §4 / §11-item-4 | **M4 source-fidelity applicability for the spec→implementation transformation is left ambiguous** ("(+ M4 if source docs)"). The implementation tasklist the builder emits reads spec/prd/tdd to produce output — template I21 (`:759-789`) makes M4 MANDATORY for "any task where the orchestrator reads source documents to produce output" and carves out ONLY mechanical/rename transforms. Inference-based tasklist generation (spec.md:543) is NOT mechanical, so M4 is plausibly mandatory for the builder's own task file. R06 does not adjudicate. | R06 should state explicitly: because the builder reads spec/prd/tdd (source docs) and generation is inference-based (not a mechanical transform), the builder's task file MUST carry an M4 source-fidelity gate per I21; cite I21 `:759-789` line 13 ("Any task where the orchestrator reads source documents to produce output") and the rename-only carve-out at line 16. |
| MINOR-1 | MINOR | R05 §2 | The "PRD/TDD autowire (existing, stay-green)" row from tdd.md:853 (`test_autowire.py`/`test_prd_cli.py`/`test_prd_prompts.py` stay green) is documented as *context* in R05 §1.3-1.5 but is not a row in the §2 NEW-TEST mapping (it is correctly an existing-suite, not a new test). Low impact — R05 §3 DOES include the UV command for these. | Optional: add a one-line "existing-suite, stay-green (no new test)" note to §2 so the mapping is exhaustive against tdd §15.2's 12 rows. |
| MINOR-2 | MINOR | R05 §2 (stale-token row) / R07 §3 | The stale-token *token set* differs between sources. tdd.md:852 lists `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`. R05 §2's stale-token row mirrors `tests/cli/prd/test_prompts.py` markers (CODE-VERIFIED etc.) but does not pin the exact 5-token quarantine set; R07 §3 verifies only 4 of them (`sc:task-unified`, `/rf:`, `.gfdoc`, `llm-workflows`, `StageError`) and omits `/config/.claude`. The builder needs the full 5-token set from tdd:852. | R05/R07 should pin the stale-token assertion to the exact tdd.md:852 set incl. `/config/.claude`; note R07 §3 did not verify `/config/.claude` absence. |
| MINOR-3 | MINOR | R07 §2 heading | R07 titles its settlement "`--spec §22`" but TDD §22 (Open Questions) does NOT contain this item — the `--spec` contradiction lives in spec §5.1 (spec.md:553-558) + spec §11 (spec.md:755) + spec.md:753. The "§22" anchor is a TDD input-contract section reference, not the Open-Questions table. A builder anchoring to "TDD §22" would not find the item. | R07 should re-anchor the settlement to spec §5.1/§11 + spec.md:753 (the carried-risk row), and note the "§22" label refers to the TDD input-contract numbering, not the §22 Open-Questions table. |

---

## Summary

- Checks (lens items) passed: 6/6 substantively, with 0 CRITICAL gaps.
- The **complete, active new-test set** (P1/P3/P4/P2/P5 + 4 carried gaps + sc:task-naming + stale-token) is fully mapped to correct target files with concrete model-tests to mirror. This is high-quality, disk-verified research.
- **3 IMPORTANT gaps** found: (1) two named retained-feature integration audit suites missing from R05's run commands; (2) P5 determinism predicate under-specified (whole-bundle `==` trap not warned); (3) M4 fidelity-gate applicability for the spec→implementation transformation left unadjudicated.
- **3 MINOR gaps**: exhaustiveness of the §2 mapping vs existing suites; stale-token set incompleteness (`/config/.claude` unverified); R07 "§22" mis-anchor.
- Per the research-gate rule (ALL gaps regardless of severity = FAIL), and because 3 IMPORTANT + 3 MINOR gaps exist, the partition-B verdict is **FAIL**. None are CRITICAL; all are remediable with targeted edits to R05/R06/R07 before synthesis.

## Confidence

Verified: 6/6 lens items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (lens-item coverage). Tool engagement (7 Read + 4 Bash) exceeds the 6 lens items — no padding; each call mapped to a specific verification (test-inventory cross-ref, file-existence, marker counts, template-citation verbatim checks).

---

## VERDICT: FAIL

**Severity-rated issues:** 0 CRITICAL, 3 IMPORTANT (IMPORTANT-1 missing retained-feature integration suites in R05 §3; IMPORTANT-2 P5 whole-bundle determinism trap unwarned; IMPORTANT-3 M4 applicability for spec→implementation unadjudicated in R06), 3 MINOR (MINOR-1 §2 mapping non-exhaustive vs existing suites; MINOR-2 stale-token set missing `/config/.claude` + R07 unverified it; MINOR-3 R07 "§22" mis-anchor).

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage, cross-references) limited to assigned subset R05/R06/R07. Full cross-file verification requires merging partition A + B reports. In particular, whether R01/R03 (partition A) actually land the P1/P2/P3/P4 logic in Python-executor vs SKILL.md — the open decision R05 §2 footer defers to them — must be checked against partition A's findings before the gate clears.]

## QA Complete

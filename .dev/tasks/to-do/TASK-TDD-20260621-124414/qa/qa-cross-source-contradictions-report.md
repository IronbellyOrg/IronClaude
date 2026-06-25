# QA Report — Cross-Source Contradiction Check (FR-DRS TDD source set)

**Topic:** FR-DRS Deterministic Runtime-Surface Sweep — cross-source contradiction QA
**Date:** 2026-06-21
**Phase:** research-gate (cross-source contradiction sub-check, item 5 "Contradiction resolution")
**Fix cycle:** N/A (fix_authorization: false — report only)

**Scope:** Contradictions BETWEEN sources only. The TDD output (`tdd.md`) was deliberately NOT read.

**Sources read (10):**

1. `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md` (the driving spec)
2. `.../research-notes.md`
3. `.../research/00-prd-extraction.md`
4. `.../research/01-runtime-surface-algorithm.md`
5. `.../research/02-product-path-integration.md`
6. `.../research/03-consumer-surfaces.md`
7. `.../research/04-eval-path-integration.md`
8. `.../research/05-reuse-and-boundaries.md`
9. `.../research/06-skill-prose-demotion.md`
10. `.../research/reuse-audit.yaml`
11. (web) `web-01-ast-ripgrep.md`, `web-02-lsp-referrers.md`

All paths resolve under `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`.

**Adversarial posture:** Assumed contradictions existed and went looking. Verified the most load-bearing claims against the actual source files (SKILL.md, ensemble.py, runner.py, commands.py) rather than trusting the research files' citations.

---

## Overall Verdict: PASS

No unreconciled cross-source contradictions found. The four candidate "contradictions" the QA brief flagged as examples are all present in the source set BUT each is **explicitly surfaced and reconciled** by the research files (most as a research-02/03/06 "Stale Documentation Found" or "Gaps and Questions" entry, or as a deliberate spec-vs-codebase tension that research-notes already flags for the TDD intro). A reconciled tension that every downstream file agrees on is not an open contradiction. Details below.

---

## Candidate Contradictions Examined (the QA brief's four examples + others)

| # | Candidate tension | Sources | Status | Evidence |
|---|-------------------|---------|--------|----------|
| C1 | Spec §2 names `commands.py` as the contract writer; research flags `commands.py` covers only `superclaude reflect run` and `_audit_once` is the real chokepoint | spec.md §2 (L71-74) vs research-02 §commands.py / research-notes L207-210 / 00-prd §8 OQ-DRS.2 | RECONCILED (not a contradiction) | See C1 below |
| C2 | 6-component reuse verdicts agreement | reuse-audit.yaml vs research-05 vs research-notes REUSE_AUDIT | CONSISTENT | See C2 below |
| C3 | Field names / count invariant ("six fields", `len==unreached`) across spec, 03, reuse-audit | spec §4 / 00 / 01 / 02 / 03 | CONSISTENT (with a noted naming nuance, agreed by all) | See C3 below |
| C4 | `contract_version` 1.6.0 (SKILL) vs stale ensemble 1.0 | SKILL.md:672 vs ensemble.py:59 vs research-02 / research-06 | RECONCILED (surfaced as stale-doc finding, not asserted as the live schema) | See C4 below |
| C5 | research-03 §5.3 pre-filter gates on derived `surface_unreached` flag, not the raw integer — internal consistency | research-03 §2 / §5.3 internal | CONSISTENT internally and with SKILL.md:402 | See C5 below |
| C6 | "deterministic, LLM-free tagger" label vs LLM-is-the-producer reality | 01 / 04 / 06 / spec §0 | CONSISTENT (all four call the label aspirational/the gap FR-DRS closes) | See C6 below |
| C7 | OQ-DRS.3 contract-version resolution direction | spec §3 / 00 / 02 / 06 | CONSISTENT | See C7 below |

---

## C1 — "commands.py is the writer" (spec §2) vs "commands.py covers only `reflect run`; `_audit_once` is the real chokepoint" (research-02)

**The apparent tension is real in the text:**

- spec.md §2 (L71-74): *"the reflect CLI wrapper (`src/superclaude/cli/reflect/commands.py`) invokes the sweep and writes/overwrites the six `runtime_surface_*` fields + ledger in `return-contract.yaml` BEFORE the contract is parsed by consumers."* The spec literally names **`commands.py`** as the invocation/write site.
- research-02 (File: commands.py section, "Candidate-invocation-site verdict"): *"Poor fit for the sweep itself … commands.py does not write or parse `return-contract.yaml` itself. It delegates the entire run to the runner … even if wired correctly, commands.py covers ONLY `superclaude reflect run`."* It then names **`ReflectRunner._audit_once` (runner.py:394-453)** as the *"one product-code chokepoint that runs on every audit of BOTH tiers."*

**Why this is RECONCILED, not an open contradiction:**

1. **research-notes.md L207-210 (AMBIGUITIES_FOR_USER) explicitly surfaces exactly this tension and tells the TDD to flag it:** *"the spec's §2 names `commands.py` as the writer, but `commands.py` only covers `superclaude reflect run`, not bare `claude -p /sc:reflect` … The TDD should state explicitly which paths get deterministic fields … (OQ-DRS.2). No user decision required to PROCEED."* So the source set does not silently assert two different writers — it names the discrepancy and routes it to the OQ-DRS.2 open question.
2. **00-prd-extraction.md §8 (OQ-DRS.2)** carries the same framing: *"Does the sweep run inside `commands.py` (post-skill) or as a Wave-1A tool the skill shells out to? Post-skill in `commands.py` is simplest … but only covers the `superclaude reflect run` path."* This is verbatim from spec §3's own open question — meaning **the spec itself already lists the invocation site as UNRESOLVED (OQ-DRS.2)**, so spec §2's `commands.py` mention is the "proposed/simplest" option, not a settled decision contradicting research-02.
3. The spec frames §2 as **"Approach (proposed)"** (spec.md L49). A proposed approach that an open question (OQ-DRS.2) explicitly reopens is not in contradiction with a research file that does the deeper invocation-site analysis the open question asks for.

**Verified against source:** commands.py:254 = `result = ReflectRunner(config).run()`; commands.py:266-267 is a stderr `contract:` echo only (diagnostic, post-parse). runner.py:394 `def _audit_once`, runner.py:425 `run_tier2_ensemble(config)`, runner.py:445 `parse_contract(config.contract_path)`. research-02's claim that `_audit_once` is the tier-agnostic chokepoint between contract-authoring and `parse_contract` is **CODE-ACCURATE**. The spec's `commands.py` claim is the coarser/proposed framing; research-02 refines it. No downstream file asserts `commands.py` is definitively the writer in conflict with research-02 — they all defer to OQ-DRS.2.

**Resolution for the TDD (recommended):** This is the single design tension research-notes already flagged for the TDD intro. The TDD must (per research-notes L207-210 + research-02 synthesis) state that `runner._audit_once` is the strongest CLI-side single site (covers both tiers + the fix loop), that `commands.py` from spec §2 is too coarse (it only delegates), and that the bare `claude -p /sc:reflect` path needs a Wave-1A skill shell-out — recording all of this under OQ-DRS.2 in §22. NOT a contradiction to resolve; a refinement to document.

---

## C2 — Six-component reuse verdicts: reuse-audit.yaml vs research-05 vs research-notes

**All three sources agree on all six verdicts.** Cross-checked field-by-field:

| Component | reuse-audit.yaml | research-05 table | research-notes REUSE_AUDIT |
|-----------|------------------|-------------------|-----------------------------|
| Surface symbol tagger | distinct, S_reuse 0.37 | distinct, 0.37 | distinct, 0.37 |
| Referrer finder | distinct (shape_divergence:true), 0.67 | distinct (shape-divergent), 0.67 | distinct (maybe-related, 0.67, shape-divergent) |
| Production-vs-test partitioner | distinct, 0.57 | distinct, 0.57 | distinct, 0.57 |
| Degrade oracle | distinct (maybe-related), 0.68 | distinct (maybe-related), 0.68 | distinct (maybe-related, 0.68) |
| Entrypoint rootwalk (depth=1) | **reuse-by-import**, 0.81, shape_divergence:true | **reuse-by-import**, 0.81 | **reuse-by-import** (STRONGEST, 0.81, shape-divergent) |
| Ledger writer + scalar computer | distinct, 0.56 | distinct, 0.56 | distinct, 0.56 |

`max_overlap: 0.81`, `candidates_scanned: 6`, `neighbours_found: 10` (reuse-audit.yaml header) are consistent with research-05's "6 proposed components … 5 of 6 distinct, entrypoint-rootwalk reuse-by-import 0.81." The key boundary fact (reflect bans imports from `cli/sprint` + `cli/roadmap` ONLY, not `cli/audit`) is identical across reuse-audit.yaml `key_boundary_fact`, research-05 §7, and research-notes PATTERNS_AND_CONVENTIONS. **No contradiction. CONSISTENT.**

---

## C3 — Field names and count invariant across spec / 00 / 01 / 02 / 03

**All sources agree on the six fields and the count invariant.** The six fields (verified verbatim against SKILL.md:731-736 this session):
`runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces`.

- spec §4 AC-3 + 00 §6 AC-3 + 01 §5.4 + 02 (anchoring) + 03 §1.1: all state `len(unreached_surfaces) == runtime_surface_unreached` holds by construction. CONSISTENT.
- **Naming nuance (agreed by ALL, not a contradiction):** research-01 (Gap 1), research-02 (anchoring), and research-03 §1 all independently note the SAME subtlety — only **five** of the six names carry the literal `runtime_surface_` prefix; the sixth (`unreached_surfaces`) is a list without the prefix. research-03 §1 documents both readings ("read literally, only five carry the prefix … the §9.3 consumer map's UC-2 row enumerates exactly these six"). 00-prd §Gaps explicitly notes the spec does not enumerate all six and the canonical list must be read from SKILL.md §9.1. This is a *shared, surfaced observation* across three research files — the opposite of a contradiction.

**Verified against source:** SKILL.md:672 comment literally says `+runtime_surface_* (6 fields)` while one of the six lacks the prefix — so the "loose prefix naming" is in the source-of-truth itself, and every research file correctly mirrors it. CONSISTENT.

---

## C4 — `contract_version` 1.6.0 (SKILL) vs ensemble 1.0

**The two values genuinely differ in the codebase — and the research correctly characterizes this as a STALE-DOC/code finding, NOT as two competing claims about the live schema.**

- Verified: `src/superclaude/cli/reflect/ensemble.py:59` → `REFLECT_CONTRACT_VERSION = "1.0"`, used at ensemble.py:378.
- Verified: `src/superclaude/skills/sc-reflect-protocol/SKILL.md:672` → `contract_version: "1.6.0"  # … 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields)`.

**Why RECONCILED:**

1. research-02 "Stale Documentation Found" explicitly flags it: *"`contract_version` mismatch (real, low-severity). `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` … but SKILL.md:672 declares the live contract version `"1.6.0"` … the implementer should reconcile (bump `REFLECT_CONTRACT_VERSION` to match, or document …)."* It correctly notes the consumer gate only checks `major == "1"` (contract.py), so it does not break verdict derivation today.
2. research-06 §5 + research-notes treat **`1.6.0` as the authoritative skill contract version** consistently, and research-06 resolves OQ-DRS.3 as "keep 1.6.0." No research file claims `1.0` is the live schema; they all name `1.0` as the *Tier-2 ensemble's stale stamp* to be reconciled.
3. The QA brief's phrasing ("1.6.0 in SKILL vs the stale ensemble 1.0") matches the research's framing exactly — i.e. the research already labels ensemble's `1.0` as **stale**, not as a contradictory authority.

This is a *code↔doc* inconsistency the research surfaced as an implementation to-do, not a *cross-source* contradiction between research files. All research files agree the live schema version is 1.6.0 and ensemble's 1.0 is a stale stamp. CONSISTENT among sources; flagged finding carried forward.

---

## C5 — research-03: §5.3 pre-filter gates on the derived `surface_unreached` flag, not the raw integer

**research-03 is internally consistent and matches SKILL.md:402 (verified verbatim this session).**

research-03 §2 ("Trigger condition, verbatim, line 402") states the pre-filter fires *"when `surface_unreached` is set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`."* That is: the **derived table-wide flag `surface_unreached`** is what gates the STOP rows, and it is *set from* the integer field `runtime_surface_unreached ≥ 1`. research-03 §5.3 ("Determinism dependency") and §2 ("Override precedence") both consistently distinguish the derived flag (`surface_unreached`) from the contract scalar (`runtime_surface_unreached`).

**Verified against source — SKILL.md:402 (read this session):** *"`coverage_undefined`, `coverage_degraded`, and `surface_unreached` are TABLE-WIDE pre-filters … when … `surface_unreached` is set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`, NO STOP row … may fire and the run routes to Tier 2."* research-03's reading is **exactly correct**: the pre-filter keys on the derived `surface_unreached` flag, which is derived from `runtime_surface_unreached ≥ 1`. No internal contradiction in research-03, and it agrees with the live SKILL.md. CONSISTENT.

(Cross-check: research-06 P6 also describes the §5.3 coupling identically — "forces Tier 2 on `runtime_surface_unreached ≥ 1` from a SUCCESSFUL sweep" — consistent with research-03 and SKILL.md:402.)

---

## C6 — "deterministic, LLM-free tagger" label vs LLM-is-the-producer reality

Potential contradiction: SKILL.md:487 self-labels the tagger *"the deterministic, LLM-free runtime-surface tagger,"* yet spec §0 + research-04 establish that today the LLM IS the producer (hand-types the scalars). Do the research files contradict each other on whether the tagger is already deterministic?

**No — all four relevant files (01, 04, 06, spec §0) agree the label is currently ASPIRATIONAL and is the exact gap FR-DRS closes:**

- research-06 "Stale Documentation Found": *"the word 'LLM-free' at line 487 is currently aspirational, not literal. After FR-DRS it becomes literally true; before FR-DRS it is technically inaccurate."*
- research-04 §4.1/§4.2: *"Although the spec calls the tagger 'deterministic, LLM-free,' in the eval harness the tagger's output is produced by an LLM run of the skill … `contract.yaml.runtime_surface_unreached` is, at grading time, an LLM-emitted scalar."*
- research-01 "Verification posture": treats the algorithm as `[UNVERIFIED — spec-only]` / a "SPEC to build," explicitly NOT a description of existing deterministic code.
- spec §0: the entire rationale is that the LLM-executed prose cannot deliver the structured guarantee.

All four converge: the "LLM-free" label describes the *intended* algorithm; FR-DRS makes a Python module the literal executor. No cross-source contradiction. CONSISTENT.

---

## C7 — OQ-DRS.3 contract-version resolution direction

All sources that opine (spec §3, 00 §8, 02, 06 §5) agree the likely resolution is **no version bump** (producer-only change, consumer-transparent, additive fields already shipped at 1.6.0). research-06 §5 gives the fullest §9.4-mapped argument ("patch-or-nothing; keep 1.6.0"); research-notes PATTERNS_AND_CONVENTIONS says "likely no version bump (OQ-DRS.3)"; 00 §8 restates the spec verbatim. No source argues for a bump in conflict with another. CONSISTENT.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | C1: writer = commands.py (spec) vs _audit_once (research-02) | PASS (reconciled) | Verified commands.py:254 delegates to `ReflectRunner(config).run()`; runner.py:394 `_audit_once`, :445 `parse_contract`. research-notes L207-210 + 00 OQ-DRS.2 explicitly surface the tension and route it to OQ-DRS.2. Spec §2 is "Approach (proposed)"; spec §3 reopens it. |
| 2 | C2: 6-component reuse verdicts agree | PASS (consistent) | Field-by-field table match across reuse-audit.yaml / research-05 / research-notes; all S_reuse values + verdicts identical; rootwalk = reuse-by-import 0.81 in all three. |
| 3 | C3: six field names + count invariant | PASS (consistent) | Six fields verified verbatim at SKILL.md:731-736; `len(unreached_surfaces)==runtime_surface_unreached` stated identically in spec/00/01/02/03; the "5-prefixed-of-6" nuance is a shared observation in 01/02/03, not a conflict. |
| 4 | C4: contract_version 1.6.0 vs ensemble 1.0 | PASS (reconciled) | Verified ensemble.py:59 = "1.0", SKILL.md:672 = "1.6.0". research-02 Stale-Doc flags ensemble's 1.0 as stale; all research files treat 1.6.0 as authoritative. Code↔doc finding, not source↔source contradiction. |
| 5 | C5: §5.3 pre-filter gates on derived `surface_unreached`, not the int | PASS (consistent) | Verified SKILL.md:402: pre-filter keys on `surface_unreached` flag, set from `runtime_surface_unreached ≥ 1`. research-03 §2/§5.3 reads this exactly; internally consistent + agrees with source + agrees with research-06 P6. |
| 6 | C6: "LLM-free tagger" label vs LLM-producer reality | PASS (consistent) | 01/04/06/spec §0 all label "LLM-free" as aspirational and the precise gap FR-DRS closes. No file claims the tagger is already deterministic. |
| 7 | C7: OQ-DRS.3 version-bump direction | PASS (consistent) | spec §3 / 00 §8 / 02 / 06 §5 all conclude "likely no bump"; none argue the opposite. |
| 8 | Algorithm semantics (degrade oracle, rootwalk depth=1, reduction precedence) agree across 01/05/06/web-01/web-02 | PASS (consistent) | 4-category oracle, depth=1 rootwalk, `DEGRADE-on-incompleteness > UNREACHED > REACHED`, dynamic→DEGRADE all stated identically in 01 §3-§5, 05 §5, 06 P2-P4, web-01 F6, web-02 F5-F9. |
| 9 | Eval cases (ids 37-41) vs acceptance criteria (spec §4 AC-2) | PASS (consistent) | 04 §3 maps the 5 cases to AC-2's four verdicts (unwired/test-only→UNREACHED+invariant, positive-control→0/false, dynamic-dispatch→degraded true, degraded-backend→Grounding Gap/no-STOP); matches spec §4 AC-2 verbatim. |
| 10 | Sprint executor "reads deterministic scalars" (AC-4) vs reality | PASS (consistent — surfaced as gap, not contradiction) | research-03 §5.2 verifies executor.py reads NO reflect contract today; AC-4 is correctly flagged as UNMET/forward-looking. spec §4 AC-4 and research-03 do not contradict — research-03 documents the gap the TDD must close. |

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Unreconciled cross-source contradictions: **0**
- Reconciled tensions (surfaced + agreed across sources): 4 (C1, C4, plus the AC-4 sprint gap and the "LLM-free" label) — all already flagged in the research files' Gaps/Stale-Doc sections
- Issues fixed in-place: 0 (fix_authorization: false)

**Bottom line:** The four example "contradictions" named in the QA brief are all present in the text but each is **already reconciled** by the source set itself — the research files surface every one of them (in "Stale Documentation Found", "Gaps and Questions", or "AMBIGUITIES_FOR_USER") and agree on the resolution direction. There is no case where two sources make mutually-exclusive load-bearing claims that the source set fails to reconcile. The most load-bearing claims were independently verified against the live code (ensemble.py, runner.py, commands.py, SKILL.md) and the research files' citations were accurate.

**Note for the TDD assembler (carry-forward, not contradictions):**

1. C1/OQ-DRS.2 (invocation site) MUST be documented as a §6.4 Key Design Decision + §22 Open Question, not silently resolved — research-notes and research-02/06 all insist on this. `_audit_once` is the strongest CLI-side site; `commands.py` (spec §2) is too coarse; the bare `claude -p` path needs a Wave-1A shell-out.
2. C4 (ensemble.py:59 = "1.0" vs SKILL 1.6.0) is a real code↔doc stale stamp the implementer should reconcile when the ensemble path starts emitting the six fields (research-02 Stale-Doc).
3. AC-4 (sprint executor reads the scalars) is UNMET in current code (research-03 §5.2) — the TDD must state whether wiring the executor is in scope or only the producer-side determinism guarantee is.

These are design carry-forwards the research already flagged, not QA failures.

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 3 (each a targeted multi-grep verifying a specific candidate: contract-version + invocation-site, pre-filter + six-field block, dir setup)
- All 10 checklist items marked [x] VERIFIED with tool evidence (file:line citations confirmed against live source for the four load-bearing candidates C1/C3/C4/C5; the remaining checks verified by direct cross-reading of the research files).
- UNCHECKED items: none.
- UNVERIFIABLE items: none.
- No web research was required (all claims were local source-truth; the two web research files were read for internal consistency only and agree with 01).

**Tool-engagement note:** 11 Reads (10 source docs + 1 report read-back required by the freshness hook) + 3 Bash multi-greps that each directly verified a load-bearing candidate against live code (ensemble.py:59, SKILL.md:672/402/731-736, runner.py:394/445, commands.py:254/266). Tool calls (14) ≥ checklist items (10) — not suspect.

## QA Complete

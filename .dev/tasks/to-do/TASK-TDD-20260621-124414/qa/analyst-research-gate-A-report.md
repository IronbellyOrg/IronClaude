# Research Completeness Verification (Partition A of M)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep (TDD research)
**Date:** 2026-06-21
**Files analyzed:** 4 (research files 00–03)
**Depth tier:** Heavyweight
**Analysis type:** completeness-verification
**fix_authorization:** false (read-only; report issues for the producing agent to fix)

**Assigned files (this partition):**
- `research/00-prd-extraction.md`
- `research/01-runtime-surface-algorithm.md`
- `research/02-product-path-integration.md`
- `research/03-consumer-surfaces.md`

`[PARTITION NOTE: Cross-file checks (cross-reference, contradiction, coverage audit against full scope) are applied only within this assigned subset {00,01,02,03}. Files 04 (eval-path), 05 (reuse/boundaries), 06 (skill-prose-demotion), and any web files are NOT in this partition. Full cross-file analysis requires merging all partition reports. In particular, gaps that point to file 05 (reuse/import-boundary) or 04 (eval/grader) are expected to be closed by those files and are flagged here as cross-partition deferrals, not partition-A defects.]`

---

## Verdict: PASS (0 critical gaps in partition A; 0 important, 3 minor/advisory observations)

All four assigned files pass the 8-item checklist. One file (01) carries a literal `Status: In Progress` header line at the top while also carrying `Status: Complete` at the bottom — flagged as a Minor presentation defect, not a completeness failure (the file is substantively complete). No critical or important gaps originate inside partition A; the substantive open items the files raise are either (a) genuine spec-level open questions the TDD is meant to document (OQ-DRS.1/.2/.3), or (b) cross-partition deferrals to files 04/05/06.

---

## Independent verification performed (this gate)

Two load-bearing claims were re-checked against source, not taken on the files' word:

| Claim | Source file | Independent check | Result |
|-------|------------|-------------------|--------|
| Six contract field names at SKILL.md §9.1 L731–736 | 02 (L27–33), 03 (L25–30) | Read SKILL.md L718–739 | CONFIRMED — names match byte-for-byte; `unreached_surfaces` (L736) is the one member lacking the `runtime_surface_` prefix, exactly as file 01 flagged |
| `pyproject.toml [project.scripts]` = `superclaude=…cli.main:main`, `ic=…cli.ic:main` | 01 (§3, `[CODE-VERIFIED]`) | Read pyproject.toml L66–73 | CONFIRMED — both entries present (L68–69); `[project.entry-points.pytest11]` at L72 also present as file 01 noted. (File 01 cited L67–69; actual entries L68–69 — accurate within range.) |

---

## Coverage Audit

Scope for partition A is the four topics assigned to files 00–03 per the SUGGESTED_PHASES table in research-notes.md (rows 00, 02, 03 and the algorithm half of 01). Each scope item maps to its covering file:

| Scope item (from research-notes EXISTING_FILES / SUGGESTED_PHASES) | Covered by | Status |
|---|---|---|
| spec.md (full) — FR-DRS requirements, ACs, OQs, out-of-scope | 00 | COVERED (9 content sections + ACs AC-1..AC-6 + OQ-DRS.1/.2/.3) |
| `refs/runtime-surface.md` §1 surface allowlist | 01 §1 | COVERED |
| `refs/runtime-surface.md` §2 language table (test/comment markers) | 01 §2 | COVERED (per-lang table reproduced) |
| `refs/runtime-surface.md` §3 degrade oracle (categories a–d) | 01 §3 | COVERED (4-category table + predicates) |
| `refs/runtime-surface.md` §4 entrypoint-rootwalk (depth=1) | 01 §4 | COVERED (5-step walk + 3 outcomes) |
| `refs/runtime-surface.md` §5 ledger schema + TypedDict + reduction precedence + count invariant | 01 §5 | COVERED |
| SKILL §6.1 steps 4b′/4b (7-step decomposition) | 01 §6 | COVERED |
| `commands.py` invocation-site analysis | 02 | COVERED |
| `runner.py` (`_audit_once`, `_IndentDumper`, `_atomic_write_text`, write_sidecar) | 02 | COVERED |
| `contract.py` (parse_contract, derive_verdict, _degraded_reason, _halted_reason) | 02 | COVERED |
| `models.py` (Verdict, ReflectConfig.contract_path, ReflectResult) | 02 | COVERED |
| `ensemble.py` (build_reflect_contract, _emit_reflect_contract) | 02 | COVERED |
| SKILL §5.3 pre-filter (line 402) | 03 §2 | COVERED |
| SKILL §9.1 six-field contract block (731–736) | 02 + 03 | COVERED (and independently re-verified above) |
| SKILL §9.3 consumer map (line 890) | 03 §3 | COVERED |
| SKILL §10.9 UNREACHED-not-a-5th-class (1055–1065) | 03 §4 | COVERED |
| `sprint/executor.py` TurnLedger (line 42) deterministic-scalar read | 03 §5 | COVERED (finding: NOT implemented today) |

**Coverage verdict:** COMPLETE for partition A. Every scope item assigned to files 00–03 is investigated. Note the algorithm-vs-data-model split of file 01 (research-notes row 01 feeds synth §6 arch + §7 ledger data model) is fully present.

---

## Evidence Quality

| Research file | Evidenced claims | Unsupported claims | Quality rating |
|---|---|---|---|
| 00-prd-extraction | High — nearly every fact carries a spec.md `§N`/line citation (e.g. frontmatter L1–13, §1 L44–48, §4 L93–104) | 0 material | Strong |
| 01-runtime-surface-algorithm | High — every structural claim cited `RS:Lnn` / `SKILL:Lnn`; the one `[CODE-VERIFIED]` data point (pyproject scripts) is real | 0 material | Strong |
| 02-product-path-integration | Very high — pervasive `[CODE-VERIFIED file:line]` tags (runner.py:394–453, contract.py:130–246, ensemble.py:500–509, models.py:95–98) | 0 material | Strong |
| 03-consumer-surfaces | Very high — `[CODE-VERIFIED]` with corrected exact line numbers (SKILL 402, 671–672, 731–736, 885, 890, 1055–1065); grep-negative claims for executor.py stated explicitly | 0 material | Strong |

No file contains vague architecture-without-paths claims. File 01's heavy use of `[UNVERIFIED — spec-only]` is **correct and well-justified** (see Staleness below) — it denotes a forward-looking spec for a module that does not yet exist, not unsupported assertion.

---

## Documentation Staleness

Checklist item 3: every doc-sourced claim must carry a verification tag. All four files comply, and the tagging is unusually disciplined:

| Doc-sourced claim | Source doc | Verification tag | Status |
|---|---|---|---|
| The 7-step algorithm / allowlist / oracle / rootwalk / ledger schema | `refs/runtime-surface.md` | `[UNVERIFIED — spec-only]` (file 01, with explicit rationale that no impl exists to diverge from) | OK — correct use of the tag; greenfield spec, not stale code |
| pyproject `[project.scripts]` entries | `pyproject.toml` | `[CODE-VERIFIED]` (file 01 §3) | OK — independently re-confirmed this gate |
| Product-path file:line anchors (runner/contract/models/ensemble) | live source | `[CODE-VERIFIED]` (file 02) | OK |
| SKILL §9.1/§5.3/§9.3/§10.9 anchors | SKILL.md | `[CODE-VERIFIED]` with corrected line numbers (file 03) | OK |

**Genuine stale-doc findings surfaced by the files (all correctly tagged, none a `[CODE-CONTRADICTED]` reported as current fact):**

1. **`contract_version` "1.0" vs "1.6.0"** (file 02, Stale Documentation Found): `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (ensemble.py:59) while SKILL.md:672 declares the live schema `"1.6.0"`. File 02 correctly classifies this as real, low-severity, non-breaking (consumer gate only checks `major == "1"`), and flags it as an implementer reconcile item — NOT reported as a current contradiction that blocks. Correct handling.
2. **§9.3 line 885 describes an unimplemented integration as a live consumer** (file 03, Stale Documentation Found + §5.3): the sprint executor is labeled "CLI consumer of return-contract.yaml" but `executor.py` reads no reflect contract. File 03 correctly tags this a documentation-vs-code mismatch (stale *integration claim*, not a stale value) and grep-substantiates the negative.

Both are appropriately surfaced as findings rather than silently absorbed. No `[CODE-CONTRADICTED]` claim is presented anywhere as a current architectural fact. **Staleness verdict: PASS.**

---

## Completeness

| Research file | Status header | Summary | Gaps section | Key Takeaways / equiv | Rating |
|---|---|---|---|---|---|
| 00-prd-extraction | `Status: Complete` (top + closing) | Y (Summary + core finding) | Y (Gaps and Questions, 5 items) | Y (Summary doubles as takeaways; "Core finding" para) | Complete |
| 01-runtime-surface-algorithm | **`Status: In Progress` (top, L3) AND `Status: Complete` (closing, L281)** | Y | Y (Gaps and Questions, 7 items) | Y (Summary + Build status) | Complete-but-flagged (see Minor #1) |
| 02-product-path-integration | `Status: Complete` | Y | Y (Gaps and Questions, Q1–Q5) | Y (Summary) | Complete |
| 03-consumer-surfaces | (no top Status line; closing has no explicit `Status:` token) | Y | Y (Gaps and Questions, 4 items) | Y (Summary) | Complete-but-flagged (see Minor #2) |

All four files have a Summary, a Gaps/Questions section, and synthesized takeaways. Two presentation defects (Minor) noted below — neither indicates an unfinished investigation; both files' bodies are substantively complete and self-consistent in content.

---

## Cross-Reference Check (within partition A)

The files reference each other's domains and the cross-references are consistent:

- **The "sixth field" hand-off chain is coherent.** File 00 (Gaps) says the six canonical names are NOT in spec.md and must be read from SKILL.md §9.1. File 01 (Gap #1) says only five names appear in `refs/runtime-surface.md` and the sixth must come from §9.1/`contract.py`. Files 02 and 03 then *resolve* that hand-off by reading SKILL.md §9.1 and enumerating all six. The dependency is raised in 00/01 and discharged in 02/03 — a clean, consistent chain (independently re-verified above).
- **Count invariant** `len(unreached_surfaces) == runtime_surface_unreached` is stated identically in 00 (AC-3), 01 (§5.4), 02 (anchoring), and 03 (§1.1). Consistent.
- **Invocation-site question (OQ-DRS.2)** raised in 00 (§8) is mapped in detail in 02 (coverage-tradeoff table) and its consumer-side consequence (bare `claude -p` path not covered) is consistent with 03's note that the only executing consumer today is the in-skill §5.3 pre-filter.
- **UNREACHED→deviation mapping**: 01's reduction precedence (DEGRADE>UNREACHED>REACHED) and 03 §4's class-mapping (DEGRADE→Grounding Gap; contradiction→Regression; unmapped→Drift) are complementary, not overlapping — 01 covers per-symbol verdict reduction, 03 covers how a decided UNREACHED maps to the 4 deviation classes. No inconsistency.

**Cross-reference verdict:** consistent.

---

## Contradiction Detection (within partition A)

No contradictions found across files 00–03. Three apparent tensions were checked and resolved as non-contradictions:

1. **"Six scalars" naming** — all four files agree that "six `runtime_surface_*`" is a loose group label and that `unreached_surfaces` lacks the literal prefix. 03 explicitly warns a `startswith("runtime_surface_")` filter would drop field #6. No file contradicts another; they reinforce.
2. **GATING vs NON-GATING** — 03 §3 flags that §5.3 treats `runtime_surface_unreached` as gating (in-skill) while §9.3 calls the fields advisory (external). 03 resolves this on the skill-boundary axis; it is a documented boundary, not a contradiction, and no other file asserts the opposite.
3. **Invocation site `commands.py` (spec §2) vs `runner._audit_once` (file 02 recommendation)** — file 00 faithfully reports the spec names `commands.py`; file 02 argues `_audit_once` is the stronger tier-agnostic site. This is 02 doing its job (the research-notes explicitly frame OQ-DRS.2 as an open decision for §6.4/§22), not contradicting 00's faithful spec extraction. research-notes AMBIGUITIES_FOR_USER pre-authorizes exactly this tension as a TDD §22 item.

**Contradiction verdict:** none.

---

## Compiled Gaps

The files collectively raise ~21 gap items. After dedup and severity triage, none is a *partition-A research defect* — they are spec-level open questions (to be documented in the TDD), cross-partition deferrals, or implementer design decisions. Categorized:

### Critical Gaps (block synthesis)
- **None.** No assigned file is missing a required investigation, and no claim needed for synthesis sections §2–§8 is absent or unsupported.

### Important Gaps (affect quality)
- **None originating in partition A.** The most consequential open item — "the sprint executor does not read the reflect return-contract today, so AC-4's 'sprint executor reads the deterministic scalars' is UNMET by existing code" (03 §5.3, Gap #1) — is a **correctly-surfaced finding about the codebase**, not a gap in the research. It is exactly the kind of fact the TDD must build a plan around; flagging it is the research succeeding. (Noted here so the orchestrator/TDD assembler does not lose it: AC-4 implies new executor wiring is in scope, or the deliverable must explicitly scope it out.)

### Minor Gaps / Advisory (must still be addressed, low priority)
- **Minor #1 — File 01 dual Status header.** `Status: In Progress` at L3 contradicts `Status: Complete` at L281. The body is complete (9 sections, all closing sections present). Remediation: the producing agent should change L3 to `Status: Complete` (or remove the top line). Presentation defect only — does not fail the completeness check on content.
- **Minor #2 — File 03 missing explicit `Status:` token.** File 03 has no top-of-file `Status:` line and no closing `Status: Complete` token (it ends at the Summary). All substance is present. Remediation: add a `Status: Complete` line for checklist uniformity with 00/01/02.
- **Minor #3 (advisory, deferred) — "sixth contract field" sourcing.** Raised in 00 and 01, resolved in 02/03. No action needed for partition A; recorded so the merge step sees it as closed, not open.

### Spec-level open questions (TDD §22 material, NOT research gaps)
- OQ-DRS.1 (referrer engine: ripgrep/AST floor vs LSP) — raised in 00 §8, 01 Gap #3/#4, deferred to file 05/06 + TDD §6.4/§21/§22.
- OQ-DRS.2 (invocation site; bare `claude -p` coverage) — raised in 00 §8, mapped in 02; TDD §6.4/§22.
- OQ-DRS.3 (contract version bump) — raised in 00 §8, informed by 02's "1.0 vs 1.6.0" stale finding; TDD §22.

### Cross-partition deferrals (NOT partition-A defects)
- Reuse/import-boundary decision (reflect→cli/audit) — research-notes flags this as the single most load-bearing design decision; it is **file 05's** job (`05-reuse-and-boundaries.md`), out of this partition.
- Eval-path / grader `check_yaml_list_len_eq` and the uc2-* cases (AC-2) — **file 04's** job, out of this partition. File 00 Gap #4 correctly notes eval ids 37–41 are referenced but the eval file is out of scope of the PRD extraction.
- SKILL §6.1 4b/4b′ prose demotion scope — **file 06's** job.

---

## Depth Assessment (vs Heavyweight tier)

**Expected depth (Heavyweight):** data models documented; integration surfaces mapped; algorithm steps captured; alternatives/open-questions framed.

| Heavyweight expectation | Evidence in partition A | Met? |
|---|---|---|
| Data models documented | 01 §5: full `RuntimeSurfaceLedgerRow` TypedDict field-by-field, per-edge vs per-symbol distinction, reduction precedence, count invariant, worked example | YES |
| Algorithm steps captured | 01 §6: all 7 steps (tag→find-referrers→partition→degrade-oracle→rootwalk→reduce→emit) with inputs/decision-logic/outputs each | YES |
| Integration surfaces mapped | 02: 5 files dissected with exact symbols + line ranges + a coverage-tradeoff matrix across 4 candidate invocation sites; end-to-end write→consume pipeline diagram | YES |
| Consumer surfaces mapped | 03: 3 consumer surfaces (A gating, B advisory, C spec-only-unimplemented) with the gating/advisory boundary analysis and the deviation-class mapping | YES |
| Requirements/ACs extracted | 00: AC-1..AC-6 verbatim, out-of-scope, 3 OQs, evidence (3×before/3×after) | YES |
| Alternatives / open questions framed | OQ-DRS.1/.2/.3 surfaced across 00/01/02; invocation-site tradeoff table in 02 | YES (full framing also depends on file 05 — cross-partition) |

**Actual depth achieved:** meets Heavyweight tier for all topics owned by partition A. Investigation goes beyond file-level understanding into symbol-level (line-anchored) tracing, grep-substantiated negative claims (executor.py reads no contract), and a candidate-site decision matrix — appropriate for a HIGH-complexity TDD.

**Missing depth elements:** None within partition A. (The reuse/import-boundary depth and eval-path depth live in files 05/04 respectively — assessed in their partitions.)

---

## Recommendations

1. **Minor #1/#2 (presentation):** producing agent should fix file 01's top `Status: In Progress` → `Status: Complete`, and add a `Status: Complete` line to file 03. Non-blocking; do before assembly for checklist uniformity.
2. **Carry AC-4 forward loudly:** the TDD assembler must treat "sprint executor reads the deterministic scalars" (AC-4) as currently UNMET (03 §5.3) — the TDD §6/§8 plan must either include new `executor.py` wiring or explicitly scope it out. This is the single highest-value finding to not lose in the merge.
3. **Carry the `contract_version` 1.0-vs-1.6.0 reconcile (02) and the §9.3 stale-integration-claim (03)** into TDD §19 migration / §22 open questions.
4. **No re-research needed for partition A.** Proceed to merge with partitions covering files 04/05/06.

---

**End of Partition A report.**

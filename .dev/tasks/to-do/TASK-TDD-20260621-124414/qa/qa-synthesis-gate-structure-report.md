# QA Report — Synthesis Gate (Structure Lens)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep TDD
**Date:** 2026-06-21
**Phase:** synthesis-gate (structure lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Files in scope:** all 9 `synth-*.md` (synth-01 … synth-09) in
`.dev/tasks/to-do/TASK-TDD-20260621-124414/synthesis/`
**Template:** `src/superclaude/examples/tdd_template.md` (v1.2, 28 sections)
**Stance:** Adversarial — assumed ≥5 structural errors and hunted for them.

---

## Overall Verdict: PASS

The 9 synthesis files cleanly tile the 28-section TDD template with correct headers, well-formed
tables, diagram presence in §6, FR/NFR numbering with priority + acceptance criteria, and
zero hallucinated file paths. Every sampled code citation (line numbers in `runner.py`,
`contract.py`, `ensemble.py`, `reachability.py`, `SKILL.md §9.1`, `grader.py`, `pyproject.toml`)
verified exactly against source. No CRITICAL or IMPORTANT structural defect found. A small number
of MINOR observations are recorded below; none block assembly.

---

## Section-to-File Coverage Map (28 template sections across 9 files)

| File | Template sections covered | Conditional / N/A handling |
|------|---------------------------|----------------------------|
| synth-01 | §1 Exec Summary, §2 Problem, §3 Goals/Non-Goals, §4 Success Metrics | §4.2 Business Metrics = N/A-with-rationale (internal reliability hardening) |
| synth-02 | §5 Technical Requirements (5.1 FR, 5.2 NFR, 5.3 PRD-trace) | §5.2 perf/SLO families explicitly N/A (local deterministic module) |
| synth-03 | §6 Architecture (6.1–6.4) | §6.5 Multi-Tenancy omitted (conditional, SaaS-only) |
| synth-04 | §7 Data Models, §8 API Specifications | §8 repurposed module/contract API (no HTTP) with rationale |
| synth-05 | §9 State Mgmt, §10 Component Inventory, §11 User Flows | §9 + §10 = N/A-with-rationale (frontend-conditional) |
| synth-06 | §12 Error Handling, §13 Security | §13.3 Data Governance = N/A-with-rationale |
| synth-07 | §14 Observability, §15 Testing Strategy | light §14 with rationale; full §15 |
| synth-08 | §16 Accessibility, §17 Performance, §18 Deps, §19 Migration | §16 = N/A-with-rationale (no UI) |
| synth-09 | §20 Risks, §21 Alternatives, §22 Open Qs, §23 Timeline, §24 Release, §25 Ops, §26 Cost, + Reuse Audit | §25/§26 light-with-rationale |

All 28 numbered sections are accounted for. Sections §9, §10, §16 (the brief-named N/A trio) each
carry an explicit `N/A — rationale:` line plus a justifying paragraph — they count as CONTENT, not
placeholders (checklist item 11). §27 References and §28 Glossary are not separately produced as
synth content; they are template-boilerplate sections the assembler populates from the evidence
trail (see Observation O-3).

---

## Items Reviewed (12-item Synthesis Gate, structure lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match TDD template | PASS | All `## N.` headers map to template §1–§26 in order; subsection headers (e.g. 5.1/5.2, 6.1–6.4, 7.1–7.5, 8.1–8.3, 12.1–12.7, 15.1–15.6) match template subsection numbering. No misnumbered or out-of-order section header found across all 9 files. |
| 2 | Table column structures correct | PASS | FR table (synth-02): ID/Requirement/Priority/Acceptance Criteria/Source — superset of template §5.1 (adds Source traceability col, acceptable). Goals (synth-01) ID/Goal/Success Criteria = template §3.1. Risks (synth-09) ID/Risk/Probability/Impact/Mitigation/Contingency = template §20 exactly. Open Questions (synth-09) ID/Question/Owner/Status/Recommended-Resolution maps template §22 (Target Date col folded into Status; acceptable). Data-entity field tables (synth-04) Field/Type/Required/Description/Constraints = template §7.1 exactly. |
| 3 | No fabrication (≥5 claims/file sampled) | PASS | Sampled 5+ claims per file against research files + live source. Every code-cited line number verified (see Verification Detail). Greenfield claim ("zero runtime_surface in reflect pkg") grep-confirmed. The single `[CODE-VERIFIED]` anchor (`pyproject.toml [project.scripts]`) confirmed at lines 67–69. No claim traced to a non-existent source. |
| 4 | Evidence citations use actual file paths | PASS | Citations are concrete `path:line` (e.g. `runner.py:394-453`, `contract.py:200-209`, `ensemble.py:59`, `SKILL.md §9.1 lines 731-736`, `grader.py:191`, `reachability.py:591-624`). No vague "the backend handles it" prose citations. |
| 5 | §6 architecture includes a diagram | PASS | synth-03 §6.1 contains a full ASCII pipeline diagram (6 logical units / 7-stage flow); §6.2 contains a Mermaid `graph TD` component diagram. synth-04 §7.2 + synth-05 §11.1/§11.2 add Mermaid flow/sequence diagrams. Diagram requirement satisfied (and exceeded). |
| 6 | FR-001/NFR-001 numbering + priority + acceptance criteria | PASS | synth-02 §5.1: FR-001..FR-013 each with Priority (Must/Should Have) + Acceptance Criteria (Given/When/Then). §5.2: NFR-001..NFR-007 same shape. Counts self-declared and verified: 13 FR (11 Must, 2 Should), 7 NFR (4 Must, 3 Should). |
| 7 | Cross-section consistency | PASS | Six canonical field names identical across synth-02 §5/Notes, synth-04 §8.2, synth-07 §14.2 (incl. the `unreached_surfaces` no-prefix caveat). Count invariant `len(unreached_surfaces) == runtime_surface_unreached` stated identically in synth-02/04/06/07. AC-1..AC-6 mapping consistent between synth-02 §5.3 and synth-07 §15.6 and synth-09 §24.1. Reduction precedence `DEGRADE > UNREACHED > REACHED` identical in synth-03/04/06. OQ-DRS.1/.2/.3 consistent across synth-01 §3.3, synth-02 §5.3, synth-03 §6.4, synth-09 §21/§22. |
| 8 | No doc-only claims in §6/§7/§8 | PASS | synth-03 §6 explicitly tags algorithm steps `[SPEC]` (forward-looking design contract) and integration surfaces `[CODE-VERIFIED]`; greenfield posture stated up front. synth-04 §7/§8 source the data model to `refs/runtime-surface.md` (the spec being implemented) with the in-repo write conventions `[CODE-VERIFIED]`. No architecture claim is presented as existing-code reality when it is spec-only — the SPEC/CODE-VERIFIED split is disciplined and explicit. |
| 9 | Stale docs surfaced in §22 | PASS | The `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` vs SKILL `1.6.0` stale-version mismatch is surfaced in synth-04 §8.3, synth-08 §19.2, AND synth-09 §22 OQ-DRS.3 caveat. The two UNVERIFIED carry-forwards (C-5 materializer, C-6 target-prefix routing) are surfaced in synth-07 §15.3/§15.4 and synth-09 §22.1. Stale/unverified items are not buried. |
| 10 | Content rules (tables over prose, no code repro) | PASS | Multi-item data consistently tabular. Code examples limited to interface/TypedDict/signature shapes (synth-04 `RuntimeSurfaceLedgerRow`, YAML row shape; synth-04 §8.1 illustrative signatures) — no full implementations reproduced, matching the template's "show key interfaces, not full implementations" rule. |
| 11 | All expected sections have content / no placeholders | PASS | No `[Component Name]`, `[TODO]`, `[Date]`, or unfilled `[X]` template placeholders remain in any synth file. The N/A trio (§9/§10/§16) and light sections (§13.3/§14/§25/§26) each carry an explicit rationale paragraph — content, not placeholder. |
| 12 | No hallucinated file paths (parent dirs exist) | PASS | All cited paths resolve: `src/superclaude/cli/reflect/{commands,config,contract,ensemble,models,runner}.py` exist; target new module `src/superclaude/cli/reflect/runtime_surface.py` parent dir exists (new file, correctly described as greenfield); `src/superclaude/cli/audit/reachability.py` exists; `refs/runtime-surface.md` exists; `.dev/eval-workspaces/sc-reflect/grader.py` + all 5 `cases/uc2-*/` dirs exist; `tests/cli/reflect/` is the correct CI test home. |

---

## Verification Detail — code citations re-checked against live source

Every line-number citation sampled below was verified with Grep/Bash against the current tree:

| Cited in | Claim | Verified |
|----------|-------|----------|
| synth-03/04/05/08 | `_audit_once` at runner.py:394-453 (tier-agnostic chokepoint) | `def _audit_once` at runner.py:394 ✓ |
| synth-03/04/05 | `parse_contract` single read at runner.py:445 | `contract = parse_contract(...)` at runner.py:445 ✓ |
| synth-04/08 | `_IndentDumper` at runner.py:58-67, copied-locally precedent at 14-17 | class at 58; "copied locally" comment at line 14 ✓ |
| synth-04/08 | `_atomic_write_text` at runner.py:70-89 | `def _atomic_write_text` at runner.py:70 ✓ |
| synth-04/08/09 | `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` at :59, used :378 | exact match at 59 and 378 ✓ |
| synth-04 | `contract.py` `_LOAD_BEARING_BOOL_FIELDS` fail-closed at 200-209 | frozenset at 47, loop at 200 ✓ |
| synth-03/04/05 | `models.py` `contract_path` at 95-98 | `def contract_path` property at 96 ✓ |
| synth-09 | `_bfs_reachable` at reachability.py:591 (S_reuse 0.81 reuse target) | `def _bfs_reachable` at 591 ✓ |
| synth-02/04/07 | six canonical field names at SKILL.md §9.1 lines 731-736 | exact six fields at 731-736 ✓ |
| synth-04/08 | `contract_version: "1.6.0"` declared at SKILL.md ~671-672 | header §9.1 at 669, version literal at 672 ✓ |
| synth-02/04/05 | "§5.3 forbid-STOP pre-filter, `unreached ≥ 1` → Tier 2" | §5.3 "Decision logic" header at 386; pre-filter at 402; SKILL line 734 literally says "drives §5.3 pre-filter" ✓ |
| synth-07/09 | grader.py:191 `check_yaml_list_len_eq`; :440 `eval_metadata.json`; :448-449 target-prefix bucketing | all three confirmed; `list_field`/`count_field` keys match synth-07 §15.4 ✓ |
| synth-09 §22.1 | `[project.scripts]` `superclaude=...:main`, `ic=...:main` CODE-VERIFIED anchor | pyproject.toml lines 67-69 exact ✓ |
| all | greenfield: zero runtime_surface code in `cli/reflect/` (7 files) | grep across pkg → ZERO MATCHES ✓ |

Result: 14/14 sampled citations verified exact. No fabricated path, no off-by-N line citation, no
overstated CODE-VERIFIED tag detected.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (deferred — fix_authorization: false) |
|---|----------|----------|-------|-----------------------------------------------------|
| O-1 | MINOR | synth-02 §5.3 header | The subsection is titled `### 5.3 PRD Trace Coverage & Gaps`, a synth-author-introduced §5.3 that is NOT in the template's §5 structure (template §5 has only 5.1/5.2). It is useful traceability content but collides numerically with no template section AND with the *separate* "§5.3 pre-filter" referenced throughout (which is a SKILL.md §5.3, not a TDD §5.3). Assembler should re-letter this to §5.3 "Requirement Traceability" and confirm no reader conflates it with the SKILL's §5.3 pre-filter. Non-blocking. |
| O-2 | MINOR | synth-04 §8 | §8 (API Specifications) is repurposed for a no-HTTP library component. This is correct and rationale-bearing, but the template's §8 sub-numbering (8.1 Overview / 8.2 Endpoint Details / 8.3 Error Format / 8.4 Governance) is replaced by (8.1 Module API / 8.2 Contract-Field Surface / 8.3 API-Governance Note). Acceptable repurposing; assembler should keep the rationale callout so a reader does not expect HTTP endpoints. Non-blocking. |
| O-3 | MINOR | (coverage) §27 References, §28 Glossary | No synth file produces §27 (References & Resources) or §28 (Glossary) content. These are the final two template sections. They are low-risk boilerplate the assembler can populate from the evidence trail / acronym set (FR-DRS, FR-RSR, UC-2, DEGRADE, rootwalk, etc.), but the assembler MUST NOT silently drop them. Flagged so assembly explicitly fills or marks them. Non-blocking for the structure gate; assembler action item. |
| O-4 | MINOR | synth-03 §6 / synth-09 §21 | Template §6.4 callout instructs completing §21 (Alternatives) before finalizing §6 to avoid confirmation bias. The synthesis satisfies this in spirit (Alt 1/2/3 map to the §6.4 D1/D2/D3 decisions and OQ-DRS.1/.2/.3), and cross-references are bidirectional. No defect — recorded only to confirm the §6↔§21 linkage was checked and is sound. |

No CRITICAL or IMPORTANT issues. All four observations are MINOR assembler-handoff notes, not
synthesis structural failures.

---

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor observations: 4 (all assembler-handoff notes, none block assembly)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Actions Taken

None — `fix_authorization: false`. All findings documented for the orchestrator/assembler. No synth
file was modified.

---

## Recommendations

1. Proceed to assembly — structure gate is GREEN.
2. Assembler should address the four MINOR handoff notes during §6 Assembly:
   - O-1: re-letter synth-02's §5.3 to avoid numeric collision with SKILL's §5.3 pre-filter.
   - O-2: preserve the §8 "no-HTTP, repurposed API" rationale callout.
   - O-3: populate §27 References and §28 Glossary (do not drop).
   - O-4: keep the §6↔§21 cross-references intact.
3. This was the STRUCTURE lens only. A separate content/qualitative lens (rf-qa-qualitative) should
   confirm the design reasoning itself is sound (e.g., that the Option-C reflect-local-copy boundary
   decision and the OQ recommendations are defensible) — out of scope for this gate.

---

## Confidence Gate

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Computation: 12 / (12 − 0) × 100 = 100.0%. Threshold (≥95% AND Unchecked == 0) met → PASS eligible.

**Tool engagement:** Read: 10 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 4
(Bash calls ran batched greps that each targeted a specific checklist item: reflect-pkg inventory +
greenfield grep → items 3/12; runner/contract/ensemble/models/commands line citations → items 3/4/8;
SKILL §9.1 + grader + pyproject citations → items 3/4/7/9; eval-case dirs + grader §191 + §5.3
resolution → items 7/12.) Reads: 1 template + 9 synth files = 10, each targeting the file under
verification. Tool-call total (10 Read + 4 multi-grep Bash) ≥ 12 checklist items → engagement
minimum satisfied; no padding calls.

No web research was required — all claims are local-source or local-spec bound; the single external
anchor type (`[project.scripts]` packaging) was verified against the in-repo `pyproject.toml`, not
the open web. Tavily-first rule not triggered.

**Unchecked items:** none.
**Unverifiable items:** none.

---

## QA Complete

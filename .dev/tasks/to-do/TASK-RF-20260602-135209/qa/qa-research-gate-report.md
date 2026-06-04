# QA Report — Research Gate

**Topic:** sc:reflect V3 Serena low-complexity adoptions (FR-RV3-LOW.1–8)
**Date:** 2026-06-02
**Phase:** research-gate
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: FAIL

One CRITICAL builder-blocking contradiction (contract_version literal), plus minor source-note errors. ALL gaps regardless of severity = FAIL per research-gate rules. The research is otherwise exceptionally strong: every load-bearing line-number claim independently verified against source and confirmed exact. Detail below.

---

## Analyst report status

The analyst-completeness-report.md is a STUB (verdict "(pending)", "Files analyzed: (pending)", no checklist applied). I ran fully independently per protocol; the analyst report contributed zero verified findings and was NOT relied upon for any verdict.

---

## Items Reviewed (10-item Research Gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (6 Complete + Summary) | PASS | All 6 files present; each carries `Status: Complete`. Summaries: 01 (Summary Table+findings), 02 (Summary), 03 (Summary table), 04 (§5 scaffold-requires + §6 per-case + coverage cross-check), 05 (Summary of must-follow rules), 06 (§6 Summary tables). |
| 2 | Evidence density (paths/lines exist) | PASS (Dense) | Independently re-verified load-bearing anchors. SKILL.md=1585 lines. Frontmatter `version: 1.0.0` L4, `allowed-tools` L5 (9 serena tools, verbatim match). §6.1 chain steps 1-6 at L359-364 (fence 358-365). §6.3 retention rule L383. §6.5 body L399. §9.1 heading L491, `contract_version: "1.0"` L494, trailer L599. §9.2 fence 603-618, last fields memory_hits/misses L616-617. §10.2 L689 (signals 693-698), §10.3 L704 (signals 708-712). Wave0 outline 127-135, step 0.5 L197-211, step 1B.3 L233-241, audit-emit L124. Every cited anchor matched the actual file. |
| 3 | Scope coverage (every FR edit target mapped) | PASS | All 8 FRs mapped to concrete edit targets across R1+R3+R4+R6. No key EXISTING_FILES entry left undiscussed. |
| 4 | Doc cross-validation tags | PASS | R6 correctly tags external claims `[MATRIX-SOURCED]` and repo-checkable claims `[CODE-VERIFIED]`. I re-verified every `[CODE-VERIFIED]` claim (anchors 491/601/689/704; refs/ has no return-contract.yaml). No untagged doc claim presented as code-fact. |
| 5 | Contradiction resolution | **FAIL** | TWO contradictions — Issues #1 (CRITICAL, unresolved) and #2 (spec self-inconsistency, resolved-in-research). |
| 6 | Gap severity | FAIL | Issue #1 CRITICAL (builder-blocking). Issues #3/#4 MINOR (source-note errors, self-corrected but must be confirmed). |
| 7 | Depth appropriateness (Deep) | PASS | R6 traces per-FR data flow end-to-end (tool → wave step → contract/telemetry field → grader assertion → version floor → fail-open token). Exceeds file-level coverage. |
| 8 | Integration-point coverage | PASS | refs↔SKILL.md mirror hazard surfaced (R3 §3: §10.2/§10.3 signal lists identical → paired edits). coverage-mapping vs reflection-rubric S_dev_density split (R3 §2). reviewer-spec brief (R3 §4). Telemetry-vs-contract split (R6 A3). |
| 9 | Pattern documentation | PASS | R2 documents house style incl. the finding that colon-namespaced degrade tokens (`serena:context-excluded`) have NO precedent — a real builder hazard. R5 documents Template-02 + 2 prior-task analogs. |
| 10 | Incremental-writing compliance | PASS | Files show organic growth (R3 top-anchored OQ-5 block, R4 "read first" finding, status In Progress→Complete). Not one-shot uniform. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | **CRITICAL** | R1 (L103,168), R2 (L200,228), R3 (L206-216,309), R6 (L379,534) vs SKILL.md §9.4 L640 vs spec L318/351/402/471 | **Unresolved cross-file contradiction on the literal `contract_version` value.** R2 says write `"1.1"` (2-segment, matching SKILL.md §9.4 which declares the format as `"<major>.<minor>"`). R3 and R6 say write `"1.1.0"` (3-segment, matching the spec's repeated literal). R1 leans `"1.1"` but flags "confirm with R2/R6". The builder must write ONE literal string into 3 sites (SKILL.md:491, :494, :599) and the research does not converge. Writing `"1.1.0"` violates the file's own §9.4 `<major>.<minor>` format declaration; writing `"1.1"` contradicts the spec's explicit `1.1.0`. This is the single most consequential ambiguity in the research. | The research must RESOLVE this, not surface it three ways. Options: (a) write `"1.1.0"` AND add a coordinated edit to SKILL.md §9.4 L640 changing the format declaration to `"<major>.<minor>.<patch>"` (so the file stays internally consistent with the spec); OR (b) write `"1.1"` and treat the spec's `1.1.0` as shorthand for the 2-segment minor bump (matching existing house style, no §9.4 edit). Pick ONE, state it as the authoritative builder instruction, and if (a), add the §9.4 edit as an explicit additional edit target. Until resolved, the builder cannot author the bump items deterministically. |
| 2 | IMPORTANT (resolved-in-research; confirm) | spec L318 vs L402; R3 L313, R6 L534 | Spec self-inconsistency: L318 calls the bump "Bulk minor contract bump for FR-1/2/**4/8**"; L402 (the authoritative A3 resolution) says the contract fields are FR-1/2/**4/5** and explicitly excludes FR-8 (telemetry, no bump). R3/R6 correctly adopt L402 as authoritative. NOT a research gap per se — the research resolved it — but the resolution rests on the builder trusting the research's "L402 wins" disambiguation. | Confirm the builder is instructed to treat L402 (FR-1/2/4/5) as authoritative and to IGNORE L318's "FR-1/2/4/8" phrasing. The research already states this; ensure the task file carries it forward explicitly so the builder does not regress to L318. |
| 3 | MINOR | research-notes.md L48 (upstream input, not an assigned file) | research-notes.md cites the MDTM template at `.claude/templates/workflow/02_mdtm_template_complex_task.md` — that path does NOT exist (`.claude/` mirror does not include `templates/`). Verified: `ls .claude/templates/workflow/` → No such file or directory. | R5 already CORRECTED this (R5 L8-11: canonical path is `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, which I verified EXISTS at 1204 lines). No action needed in the assigned research files; flagged so the builder uses R5's corrected src/ path, never the research-notes `.claude/` path. |
| 4 | MINOR | R4 L36-38; R6 colon-token usage vs R2 finding | Latent tension (not a hard contradiction): R2 (Pattern 5, L148/226) finds NO precedent for colon-namespaced degrade tokens and recommends AGAINST `serena:context-excluded`-style tokens (prefer hyphenated slugs or a `*_diversity` enum). But R4 (L299,330,344,363) and R6 (L43,47,516,520) freely use colon-namespaced tokens (`find_implementations:lsp_unsupported`, `search_deps:lsp_unindexed`, `serena:context-excluded`, `serena:pre-v1.5-no-rename-propagation`) as the eval-assertion / degrade values, because the spec/matrix define them that way. | Surface to the builder: the spec mandates colon-namespaced degrade tokens, but they have NO existing precedent in SKILL.md's token grammar (R2's finding is correct). This is a deliberate grammar extension, not an error — but the builder should note it introduces a new token convention and should NOT be "normalized" to hyphenated form (which would break the spec-defined eval assertions). The two research files are describing different layers (R2 = current house style; R4/R6 = spec-mandated new tokens); reconcile by documenting it as an intentional new convention. |

---

## Independent verification log (load-bearing claims the prompt flagged)

All spot-checks the spawn prompt demanded were performed and PASSED:

1. **Frontmatter allowed-tools + 7 tools ABSENT + check_onboarding_performed ABSENT** — VERIFIED. `grep -c` returned 0 for all of: find_implementations, find_declaration, get_current_config, summarize_changes, delete_memory, rename_memory, edit_memory, check_onboarding, onboarding. L5 lists exactly the 9 existing serena tools, verbatim match to R1.
2. **§6.1 chain line range** — VERIFIED. Steps 1-6 at L359-364, fence 358-365. Exact.
3. **§9.1 contract_version value + line** — VERIFIED. `contract_version: "1.0"` at L494; heading L491; trailer L599. Exact (this is also the locus of Issue #1).
4. **§9.2 last field line** — VERIFIED. `memory_hits` L616, `memory_misses` L617, closing fence L618. Exact.
5. **refs/return-contract.yaml does NOT exist** — VERIFIED. `ls` → ABSENT. refs/ has exactly 11 files.
6. **3 refs files + coverage-mapping.md DO exist** — VERIFIED. reflection-rubric.md, deviation-taxonomy.md, reviewer-spec.md, coverage-mapping.md all present.
7. **MDTM template 02 at R5's corrected src/ path** — VERIFIED. `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` exists, 1204 lines; A3 L91, B2 L142, I15 L599, I18 L637 all match R5. `.claude/templates/` does NOT exist (Issue #3).
8. **eval grader.py exists** — VERIFIED. grader.py (20939 B), aggregate_iteration.py, evals/evals.json (assertion arrays, ids to 20) all present.
9. **R4's claim: grader never reads expected.yaml; assertions live in evals.json** — VERIFIED. `grep "expected.yaml" grader.py` → ZERO hits. parse_yaml_simple (L58-77) skips `line.startswith(" ")` (flat parser, L71). yaml_field (L336-346) string-coerces expected. grade_eval reads `eval_metadata.json` (L414-420), partitions on with_skill/old_skill prefix (L422-423). expected.yaml files confirmed STUBs (`# STUB` header line 1). R4's CRITICAL FINDING is fully accurate.

---

## Summary

- Checks passed: 8 / 10
- Checks failed: 2 (items 5 contradiction-resolution, 6 gap-severity)
- Critical issues: 1 (Issue #1 — contract_version literal)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 (folded into Bash grep -c) | Glob: 0 (folded into Bash ls) | Bash: 8
- No web research performed (all claims were repo-local or spec-local; no external URL/standard/third-party-API lookup required).
- Tool-engagement note: total tool calls (15) exceed the 10 checklist items; every Bash call mapped to a specific checklist item (anchor verification, absence greps, existence checks, grader-internals). No padding calls.

## Recommendations

1. **BLOCKER (Issue #1):** Resolve the `contract_version` literal to a single value (`"1.1"` OR `"1.1.0"` + §9.4 format edit) before the builder authors the bump items. This is a research gap that will otherwise force the builder to guess on a 3-site edit. Recommend option (a): write `"1.1.0"` and add SKILL.md §9.4 L640 format-declaration edit, because the spec is the authoritative driving document and repeats `1.1.0` five times — but the research must STATE this, not leave it open.
2. **Confirm (Issue #2):** Carry forward "spec L402 (FR-1/2/4/5) is authoritative over L318 (FR-1/2/4/8)" as an explicit builder instruction.
3. **Confirm (Issue #3):** Builder uses R5's corrected `src/` template path; never the research-notes `.claude/` path.
4. **Document (Issue #4):** Colon-namespaced degrade tokens are a spec-mandated NEW convention with no SKILL.md precedent; do not normalize them.

Once Issue #1 is resolved (and #2/#3/#4 confirmed in the task file), this research is green-light quality — the evidence density and independent-verifiability are excellent.

## QA Complete

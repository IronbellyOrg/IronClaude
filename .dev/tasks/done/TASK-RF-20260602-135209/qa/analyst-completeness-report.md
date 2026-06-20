# Research Completeness Verification

**Topic:** sc:reflect V3 Serena low-complexity adoptions (FR-RV3-LOW.1–8) into sc-reflect-protocol skill
**Date:** 2026-06-02
**Depth tier:** Deep
**Source spec:** .dev/releases/current/Reflect-V3-Serena/04-spec-low-complexity.md
**Files analyzed:** 6 (all assigned)

- 01-skill-insertion-points.md (170 lines) — File Inventory, Status: Complete
- 02-patterns-conventions.md (231 lines) — Patterns & Conventions, Status: Complete
- 03-refs-and-inline-contract.md (319 lines) — Integration Points, header says "In Progress" (L6) but body fully populated, ends "Status: Complete" (L318)
- 04-eval-workspace-conventions.md (414 lines) — Test & Verification, Status: Complete
- 05-mdtm-template-and-examples.md (514 lines) — Template & Examples, Status: Complete
- 06-serena-surface-oq-probes-review.md (542 lines) — Solution Research + Doc Cross-Validator, Status: Complete

---

## Verdict: PASS (with 4 MINOR advisory notes — none blocking)

The research corpus is unusually thorough, evidence-dense, and internally consistent across all 9 completeness criteria and all 6 specific cross-checks. Every edit target is pinned to a file + line range or anchor; every external Serena claim is tagged [MATRIX-SOURCED]/[CODE-VERIFIED]; the §4.6 implementation order is fully supported; the 5 OQ preconditions and per-FR version floors are documented with runtime-probe procedures; and the 5 CRITICAL/MAJOR correctness invariants (C1–C5) are carried with required fixes. The 4 advisory notes below are documentation-hygiene items the builder should be aware of but which do NOT block task construction.

---

## Criterion 1 — Source files identified with paths and exports/line-ranges?

**PASS.**

Every FR's source edit target is pinned to an absolute-relative file path plus a line range or a verbatim anchor string:

- **SKILL.md insertion points (R1):** 10 numbered points, each with line range AND a verbatim anchor quote — e.g. frontmatter `allowed-tools` at `:5` (full list quoted, L13), §4.0 Wave-0 outline `:127-135` (0.5=`:132`, 0.7=`:134`), §6.1 evidence chain fence `:358-365` (steps `:359-364` individually quoted), §6.3 retention rule `:383`, §9.1 contract fence `:493-597` (`contract_version` at `:494`, also `:491`/`:599`), §9.2 telemetry fence `:603-618` (last field `memory_misses` at `:617`), §10.2 `:689`/signals `:693-698`, §10.3 `:704`/signals `:708-712`, audit-emit convention `:124`. File total 1585 lines verified via `wc -l` (R1 L6).
- **refs/ targets (R3):** reflection-rubric.md `### S_dev_density` at `:102-112`; coverage-mapping.md `## S_dev_density calculation` at `:89-111`; deviation-taxonomy.md `## Necessary` signals `:44-49` and `## Drift` signals `:59-63`; reviewer-spec.md `## Grounding hunks` at `:31-37`. Current text quoted verbatim for each.
- **Negative-existence evidence:** all 7 new tools + `check_onboarding_performed` confirmed ABSENT by grep, zero hits each (R1 L16-17) — clean adds, no dedupe risk. `refs/return-contract.yaml` confirmed ABSENT by `ls` (R3 L12-18, R6 L214-219).
- **Template + examples (R5):** canonical template path corrected to `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (1204 lines) with a note that the brief's `.claude/templates/...` path does NOT exist (R5 L8-14). Two prior task examples cited with line anchors (TASK-RF-20260526-183300, TASK-RF-20260529-171029).

Evidence quality is uniformly STRONG: I found no claim of a source edit target lacking a path+anchor. The freshness caveat is explicitly built in (R5 §7 #11: fresh pre-edit Read mandatory; R6 OQ-2 grep belt-and-suspenders), so stale line numbers are pre-mitigated.

---

## Criterion 2 — Output paths and formats clear (SKILL.md edit targets, refs targets, eval-case dirs)?

**PASS.**

- **SKILL.md / refs edit targets:** fully enumerated (Criterion 1). The FR→file→line→change summary table in R3 (L291-309) is a complete machine-actionable map covering all 8 FRs + the version bump across SKILL.md §9.1/§9.2/§10.2/§10.3, reflection-rubric.md, coverage-mapping.md, deviation-taxonomy.md, reviewer-spec.md.
- **Eval-case dirs (R4):** 6 new `case_dir:` dirs named and mapped to FRs with spec §4.1 and §8.1 line cites (R4 §6 table L380-391): `serena-find-implementations` (FR-1), `serena-find-declaration` (FR-2+FR-3 shared), `serena-search-deps` (FR-4), `serena-wave0-config` (FR-6+FR-7), `serena-memory-retention` (FR-8), `serena-summarize-changes` (FR-5). Each case's required deliverables (input fixtures, expected.yaml, evals.json eval object + assertions[]) are spelled out.
- **Eval output format CRITICAL clarification (R4 §0):** the research correctly separates the two artifacts — `expected.yaml` (human contract doc, grader does NOT read) vs `evals/evals.json` `assertions[]` (the machine-graded surface read via per-iteration `eval_metadata.json`). This resolves the most dangerous possible builder error (authoring assertions in the wrong file). Verified against grader.py:414-420 and aggregate_iteration.py.
- **SoT discipline:** R4 §7 (L403-406) correctly notes `.dev/eval-workspaces/` is committed source but NOT sync-dev'd — the `src/ → make sync-dev → .claude/` rule does NOT apply to eval edits, but DOES apply to SKILL.md/refs edits (R5 §6b).

---

## Criterion 3 — Logical breakdown supporting the §4.6 implementation order (FR-7+6 → FR-1+2 → FR-4 → FR-8 → FR-3 → FR-5)?

**PASS** (with ADVISORY NOTE 1).

The research provides the dependency facts that justify the §4.6 order, even though no single file restates §4.6 verbatim:

- **FR-7 first:** R6 establishes `get_current_config` (FR-7) is the version-fingerprint source with NO floor, and is a **prerequisite for FR-6 and FR-8** version gates (R6 L336, L504, invariant A2 "FR-7 ships in Phase 1 ONLY" L378/L533). This justifies FR-7 leading.
- **FR-6 with/after FR-7:** FR-6 onboarding parse consumes `serena_version` (floor v1.5.0, R6 L324). FR-6+FR-7 share the `serena-wave0-config` eval dir (R4 §6 Case 4), supporting their bundling.
- **FR-1+FR-2 bundled:** R6 L274 explicitly — "FR-1+FR-2 are a single bundled task" (shared schema, shared v1.3.0 floor, spec:511). R4 bundles them adjacent (Cases 1-2).
- **FR-4 after FR-2:** R6 L298, L320, L536 — FR-4's operationalized predicate is "a symbol whose `find_declaration` resolves to an `<ext:…>` path" → **FR-4 depends on FR-2**. R4 Case 3 states "Depends on FR-2 output." This justifies FR-4 after the FR-1+2 bundle.
- **FR-8 after FR-7:** R6 L354 — FR-8 "MUST include Wave-0 `get_current_config` version check as first step" (floor v1.5.0). Depends on FR-7's fingerprint.
- **FR-3 gated on OQ-1:** R6 OQ-1 is a hard merge blocker (L109-110, L501). FR-3 is a param-add to an existing call, low-risk, ordered later because it waits on the runtime probe.
- **FR-5 last:** R6 L135, L309-310, L533 — "Ships last (lowest cost/benefit)", pilot-gated (OQ-3, SHOULD not MUST), prompt-based. R4 Case 6 "ship-last pilot."

**ADVISORY NOTE 1 (MINOR):** No research file reproduces the literal §4.6 ordering string "FR-7+6 → FR-1+2 → FR-4 → FR-8 → FR-3 → FR-5" or cross-checks it against the §9 rollout-phase ordering. R6 L377 flags review finding **A1 as still-open**: "§4.6 order (FR-6 step 2) contradicts §9 rollout (FR-6 Phase 5) — Must be reconciled." So while the per-FR dependency facts SUPPORT the §4.6 order, the spec itself carries an unreconciled A1 contradiction between §4.6 and §9. The builder should reconcile A1 (or carry it as a known spec gap) when laying out phases, rather than assuming §4.6 and §9 agree. This is a spec-level issue surfaced by the research, not a research gap.

---

## Criterion 4 — Patterns and conventions documented with examples (audit emit, fail-open, telemetry naming)?

**PASS.**

R2 is a dedicated patterns file and is exemplary:

- **Audit emit (Pattern 3):** canonical row shape `{wave, step, timestamp, outcome: ok|warn|fail|skip, evidence_ref}` quoted from SKILL.md:124; snake_case keys; "loud, never silent" rule (SKILL.md:257); grader `checkpoint_logged` coupling (SKILL.md:899); `<thing>_<pastverb>: bool` contract-flag convention with three precedents.
- **Fail-open (Pattern 4):** the one-sentence envelope quoted from SKILL.md:397-399; the §14 Error Handling Matrix row form quoted (SKILL.md:1041-1043); a reusable template for new tools' fail-open clause given.
- **Telemetry naming (Pattern 6):** full §9.2 block quoted (SKILL.md:603-618); the casing rules (snake_case, `bool`/`<int>`/`[<list>]`/pipe-enum/`<noun>_path` placeholders, inline `#` comment citing governing §); serena precedent `memory_hits`/`memory_misses`.
- **Chain-step phrasing (Pattern 1)** and **conditional-step phrasing (Pattern 2, two co-existing templates)** documented with verbatim examples — directly templates the new steps 2a/3b/7/7'.
- **Contract-version policy (Pattern 7):** §9.4 quoted; additive = MINOR bump (1.0→1.1); the 3 sites to update; never rename/retype.
- **`S_dev_density` reference style (Pattern 8):** 6 distinct usage sites quoted, establishing that SKILL.md references the signal and the math lives in coverage-mapping.md.

**ADVISORY NOTE 2 (MINOR) — degrade-token house-style tension is documented but unresolved.** R2 Pattern 5 (L134-148) finds there is **NO existing colon-namespaced degrade token** in the file (no `["serena:..."]` instance); every current token is a bare slug (`"serena"`, `"auggie"`) or hyphenated component slug (`"env-aliases"`). R2 RECOMMENDS against colon namespacing. BUT the spec (per R3 L66, R6 Cases 4/5/8) MANDATES exactly these colon-namespaced tokens: `serena:context-excluded` (FR-7.3), `search_deps:lsp_unindexed` (FR-4.4), `find_implementations:lsp_unsupported` (FR-1.4), `serena:pre-v1.5-no-rename-propagation` (FR-8.4). This is a real tension (spec mandates a token grammar the house style lacks precedent for). It is correctly documented on both sides — see Cross-Check 5 below. NOT a research gap; it is a documented decision the builder must make (follow spec's mandated tokens, accepting they introduce a new colon-namespace grammar).

---

## Criterion 5 — MDTM template notes present with rule references (A3/A4/B2/L1-L6)?

**PASS.**

R5 is a dedicated template file and covers the full MDTM rule surface with `template:LINE` citations:

- **A3 Complete Granular Breakdown** (`template:91-95`), **A4 Iterative Process Structure** (`template:97-116`) — both quoted with application to the 8-FR task (one item per file/eval-case/QA gate; orchestrator enumerates, worker never adds).
- **B2 the 6 required elements** (`template:142-148`) enumerated; **B4 canonical example quoted verbatim** (`template:155-158`) with anatomy mapped to the 6 elements; B1/B3/B5/B7 covered.
- **L1-L6 handoff patterns** (`template:710-835`) each described with its handoff-dir destination; the QA-gate spawn item and L3 testing-item skeletons quoted verbatim from PART 2 (`template:1096`, `template:1104`).
- **I15/I16/I17/I18** (phase-gate QA, fix-cycle caps table, post-completion validation, code-mod testing) all quoted; **M1/M2** phase-gate composite patterns; **Section C/E/F/J/K** covered.
- **Prior-example patterns (R5 §6):** per-file edit items, make sync-dev/verify-sync items, per-phase QA gates with the byte-exact ADVERSARIAL STANCE string, version-conditional baseline gates — all with line cites from two real prior tasks.

The fix-cycle caps table (R5 §I16: research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 / any qualitative 3) is reproduced, and the rf-qa adversarial+fix_authorization pattern matches project memory. Granularity guidance (R5 §7) and a 12-item pitfall checklist are included.

---

## Criterion 6 — Granularity sufficient for per-FR / per-file / per-eval-case checklist items?

**PASS.**

- **Per-file:** R1's 10 insertion points + R3's FR→file→line table give one actionable edit per file per FR. R5 §6a gives the canonical per-file SKILL.md edit item shape (read research at line ranges → fresh pre-edit Read → edit only `src/` → `ensuring…` clause → completion gate).
- **Per-FR:** R6 §3 gives per-row (FR-1..FR-8) cost/value/risk/corrected-form/wave/floor. The corrected tool forms (FR-3 → `include_info`, FR-6 → `activate_project` parse) are pinned so the builder will not wire a defunct/wrong tool.
- **Per-eval-case:** R4 §6 gives per-case (1-6) FR, mode, input-fixture shape, and an itemized key-assertions list with grader assertion types pre-selected. R4 §7 explicitly decomposes each case into ≥3 builder items (input fixtures / expected.yaml / evals.json eval object). Unique `id: 21..26+` guidance given (existing ids 1-20).
- **Eval-case → assertion mapping** is granular enough that each FR's acceptance criteria (FR-N.M) map to a specific assertion type (`regex_present` for `<tool>_invoked` JSONL audit fields, `yaml_field` for top-level contract scalars, `yaml_list_contains` for nested lists) — with the three flat-parser gotchas encoded (R4 §3).

The granularity is sufficient to author atomic, self-contained B2 items per file, per FR, and per eval-case without the builder needing to re-research.

---

## Criterion 7 — Doc cross-validation: claims tagged [CODE-VERIFIED]/[MATRIX-SOURCED]/[UNVERIFIED] (esp. external Serena surface)?

**PASS.**

R6 handles this explicitly and correctly:

- **Sourcing note (R6 L10-18):** documentation-derived research; live-Serena-surface claims tagged **[MATRIX-SOURCED]** (Serena MCP is external, not inspectable at build time); repo-verifiable claims tagged **[CODE-VERIFIED]**.
- **[MATRIX-SOURCED]** applied to: all version facts (R6 §1), every per-row matrix dive (R6 §3), all OQ-1/OQ-3/OQ-4 evidence, with matrix line cites (e.g. matrix:74, matrix:181, matrix:399).
- **[CODE-VERIFIED]** applied to: OQ-2 anchors verified against SKILL.md in-session (491/601/689/704), OQ-5 `refs/` directory listing. Also R1/R3 anchors and the grep-confirmed absences.
- The external Serena surface (the highest fabrication risk) is consistently and correctly NOT claimed as code-verified. The OQ probes (Criterion 8) exist precisely because these facts are not code-verifiable from this repo — the research is honest about this.

No `[UNVERIFIED]` tags were needed because every uncertain external claim is instead routed to an explicit OQ runtime-probe (a stronger treatment than a bare `[UNVERIFIED]` tag). No web research was performed or required, consistent with the analyst no-unauthorized-web-research rule.

---

## Criterion 8 — Solution research: OQ-1/3/4 runtime-probe procedures as preconditions; version floors established?

**PASS.**

- **Precondition set is correctly bounded:** R6 §2 quotes spec:511 — the build-time precondition set is **OQ-1, OQ-2, OQ-3, OQ-4, OQ-5**; OQ-6 and OQ-7 are explicitly OUT (resolved in eval-authoring / Phase 1). This prevents the builder from over- or under-creating precondition items.
- **OQ-1 (FR-3, hard merge blocker):** exact 4-step runtime-probe procedure documented (enumerate live tool inventory via `serena_info` or `get_current_config`; check for `find_referencing_code_snippets`; branch ABSENT→wire `include_info:true` / PRESENT→OQ-1 decision per FR-3.4; record in audit). Marked "MUST resolve before merge (spec:195)."
- **OQ-3 (FR-5, pilot/SHOULD):** pilot procedure in `cases/serena-summarize-changes/` documented; correctly distinguished as SHOULD-probe / not-merge-blocking; ties to review R5 (harness has no session-identity mechanism → FR-5 pilot-only/manual).
- **OQ-4 (FR-7, defensive-parse MANDATORY):** runtime probe + defensive field-presence checks documented; version-fingerprint extraction is load-bearing (gates FR-6+FR-8); three-valued `serena_version` per A4+C2; fail-open → `unknown`.
- **Version floors (R6 §1 + §6 tables):** per-FR floors fully established with matrix+spec cites — FR-1/FR-2 = v1.3.0, FR-6/FR-8 = v1.5.0, FR-4 = pre-v1.0 (hardened v1.1.2), FR-3 = none beyond chain (enriched v1.5.0), FR-5 = pre-v1.0, FR-7 = pre-v1.0 (it IS the fingerprint source). Below-floor / on-`unknown` treatment specified for every FR. OQ-7 (global floor) correctly noted as NOT resolved at build time; per-FR floors are authoritative.

This is the strongest single criterion in the corpus — the solution-research depth (version gate inventory, per-FR floors, probe procedures, fail-open treatments) substantially exceeds Deep-tier expectations.

---

## Criterion 9 — Unresolved ambiguities documented (not silently skipped)?

**PASS.**

The research surfaces ambiguities explicitly rather than papering over them:

- **A1 unreconciled** (§4.6 vs §9 rollout ordering for FR-6) — R6 L377, flagged Open. (See Advisory Note 1.)
- **R2 NFR-3 token budget** mixes units (turns vs tokens), undefined baseline — R6 L368, "carry as a known NFR gap."
- **R4 predicate** ("cites a third-party API by name") undefined → operationalized as `<ext:…>` resolution — R6 L370.
- **R5 FR-5 session-identity** not operationalized in harness → FR-5 pilot-only/manual — R6 L371.
- **coverage-mapping.md formula ambiguity (R3 L103-113):** does `implementation_coverage_pct` feed the `S_dev_density` ratio (formula change → coverage-mapping.md edit) or is it a parallel signal (rubric-weight only)? R3 raises it as an explicit OQ for the task, leans toward "feeds the ratio" (spec:121), and recommends adding coverage-mapping.md as a conditional FR-1 target. (See Cross-Check 1.)
- **C1-C5 correctness invariants** (R6 §4) each documented WITH the required fix, not just flagged.
- **R3 header/body status mismatch** — see Advisory Note 4.

No ambiguity is silently skipped; each is either resolved with a cited decision or carried as a named gap for the builder.

---

## Cross-Check Results (researcher-flagged internal-consistency checks)

### Cross-Check A — R3: S_dev_density math in coverage-mapping.md (not just reflection-rubric.md); both files pinned for FR-1/6/7

**CONSISTENT / PASS.** R3 §1 pins reflection-rubric.md `### S_dev_density` at `:102-112` (threshold/weight semantics) and R3 §2 pins coverage-mapping.md `## S_dev_density calculation` at `:89-111` (the arithmetic). R3 L103-113 explicitly flags that the spec §5 matrix (spec:315) names ONLY reflection-rubric.md and **under-specifies coverage-mapping.md**, recommending the builder add coverage-mapping.md as a conditional FR-1 edit target if the missing-implementor count enters the ratio. R2 Pattern 8 (L216) independently corroborates: "the actual sub-term math lives in `refs/coverage-mapping.md`, and SKILL.md only references the signal." Both files are pinned; the disambiguation is explicit. The only residual is the genuine OQ (formula-change vs weight-only) which is correctly surfaced, not skipped.

### Cross-Check B — R3: §10.2/§10.3 MIRROR between deviation-taxonomy.md and SKILL.md needs PAIRED edits (FR-4/FR-5); both surfaces covered

**CONSISTENT / PASS.** R3 §3 (L161-164) flags the MIRROR-EDIT HAZARD: SKILL.md §10.2 (`:693-698`) and §10.3 (`:708-712`) carry IDENTICAL Detection-signals lists to deviation-taxonomy.md `:44-49` / `:59-63`; the same two bullets (FR-4 `third_party_api_verified` → Necessary; FR-5 `serena_summary_corroboration` → Drift) MUST be added to BOTH or they drift. R1 Point 9 (L130-131) independently covers the SKILL.md §10.2/§10.3 surfaces with the same insert points and the §10.5 precedence guard (`:732-734`). R3 L162-164 asks the builder to confirm SKILL.md §10.2/§10.3 are in scope — and R1 confirms they are. The R3 FR→file table (L299-303) lists all four paired rows. Both surfaces are covered; the paired-edit requirement is explicit in two files.

### Cross-Check C — R4: eval assertions live in evals/evals.json (assertions[]), NOT expected.yaml; research gives builder enough to author BOTH per new case

**CONSISTENT / PASS.** R4 §0 (L10-39) is an explicit, evidence-backed CRITICAL FINDING separating the two artifacts: `expected.yaml` is a human contract doc the grader does NOT read (every existing one is a `# STUB`); `evals/evals.json` `assertions[]` is the machine-graded surface (copied to per-iteration `eval_metadata.json`, read by grader.py:414-420 and aggregate_iteration.py `build_benchmark`). R4 §2 gives the full `expected.yaml` field union (so the builder can author it); R4 §3 gives the full 18-type grader assertion vocabulary with line cites + 3 flat-parser gotchas (so the builder can author the assertions); R4 §6 gives per-case key-assertions with types pre-selected; R4 §5 + §7 list "author expected.yaml" AND "append eval object to evals.json" as TWO distinct deliverables per case. The builder has enough to author BOTH. The "two-eval-objects / two-fixture-snapshots for success-path AND degraded-path" encoding is also explained (R4 §3 L221-229).

### Cross-Check D — R1: §4.0 step 0.7 has NO detailed prose block (FR-6 must CREATE it); captured for builder

**CONSISTENT / PASS.** R1 Point 2 (L30) states the finding explicitly: the §4.0 detailed-step block (`:172-225`) contains prose ONLY for steps 0.4/0.5/0.6/0.9 — "There is **NO detailed prose block for step 0.7** anywhere in §4.0 — 0.7 exists only as the one-line outline entry at line 134." R1 L40-42 directs FR-6 to CREATE the 0.7 detail block (two coordinated edits: outline line extend + author new `**Step 0.7**` block in the 213→215 gap to keep numeric order). R1 also surfaces a RELATED finding (L30, L165): step **0.5b** likewise has no §4.0 prose (only an inline mention at `:426`), flagged as a builder confirm-with-R6 item for where FR-7's 0.5c sits. Both the 0.7-creation requirement and the 0.5b caveat are captured. Cross-cutting finding #1 in R1's summary (L164) restates it.

### Cross-Check E — R2: `serena:context-excluded` colon-namespaced degrade tokens have no in-file precedent; tension documented

**CONSISTENT / PASS.** R2 Pattern 5 (L134-148) documents the tension on both sides: "there is **NO existing colon-namespaced degrade token in the file** (no `["serena:..."]` instance exists)"; current tokens are bare slugs or hyphenated component slugs; R2 RECOMMENDS a `*_diversity` enum or a hyphenated slug over colon namespacing. Meanwhile R3 L66 and R6 (Cases 4/5/8, version-floor table L516-520) record that the SPEC MANDATES exactly the colon-namespaced tokens (`serena:context-excluded` FR-7.3, `search_deps:lsp_unindexed` FR-4.4, `find_implementations:lsp_unsupported` FR-1.4, `serena:pre-v1.5-no-rename-propagation` FR-8.4). The house-style-vs-spec tension is documented in both R2 (style side) and R3/R6 (spec-mandate side). This is a genuine decision point, not a gap. (See Advisory Note 2.)

### Cross-Check F — OQ-2 (anchors) and OQ-5 (no return-contract.yaml) resolutions consistent across R1/R3/R6

**CONSISTENT / PASS.**

- **OQ-2 anchors:** R6 §2 marks RESOLVED POSITIVE [CODE-VERIFIED] — §9.1=`:491`, §9.2=`:601`, §10.2=`:689`, §10.3=`:704`. R1 independently pins the SAME anchors: §9.1 `:491` (Point 7), §9.2 `:601` (Point 8), §10.2 `:689` (Point 9), §10.3 `:704` (Point 9). R3 independently pins §9.1 `:491`/§9.2 `:601` (§5/§6) and §10.2 `:689`/§10.3 `:704` (§3 L122-123). **All three files agree to the exact line numbers.** R6 keeps the grep belt-and-suspenders check per CLAUDE.md S1.
- **OQ-5 return-contract.yaml absence:** R6 §2 marks RESOLVED [CODE-VERIFIED] — `ls refs/` returns 11 files, none named `return-contract.yaml`; contract edits go to SKILL.md §9 inline. R3 §0/§7 independently lists the SAME 11 files and reaches the SAME conclusion ("strike the spec:318 matrix row; edits land in SKILL.md §9.1 inline"). R1 does not contradict (it routes all §9 edits to SKILL.md inline). **R3 and R6 agree byte-for-byte on the 11-file listing and the conclusion.**

No contradictions found across R1/R3/R6 on either OQ.

---

## Contradictions Found

**NONE.** Across all 6 files I found no claim about the same file, line, anchor, tool, version floor, or FR routing that contradicts another file. Where two files cover the same surface (SKILL.md anchors in R1/R3/R6; S_dev_density math in R2/R3; the colon-token question in R2/R3/R6; eval artifacts in R4) they AGREE, and the agreement is exact (same line numbers, same file listings, same tool corrections). The only "tensions" (colon tokens, coverage-mapping formula, A1 ordering) are spec-level or style-level decision points correctly surfaced by the research, not inter-file research contradictions.

---

## Compiled Gaps

### Critical Gaps (block synthesis / task construction)

**NONE.**

### Important Gaps (affect quality)

**NONE that are research gaps.** The following are SPEC-level gaps the research correctly surfaced and which the builder must handle (carry as known gaps or reconcile), but they are not deficiencies in the research itself:

1. **Spec A1 unreconciled** — §4.6 implementation order vs §9 rollout phases disagree on FR-6 placement (R6 L377). Builder must reconcile or carry as a known spec gap when laying out phases.
2. **coverage-mapping.md FR-1 edit conditionality** — whether `implementation_coverage_pct` feeds the `S_dev_density` ratio (→ coverage-mapping.md formula edit required) or is parallel (→ rubric weight only). R3 leans "feeds the ratio" (spec:121) and recommends adding coverage-mapping.md as a conditional FR-1 target; builder should make this a deliberate decision, defaulting to including the coverage-mapping.md edit.

### Minor Gaps / Advisory Notes (documentation hygiene — must still be acknowledged)

1. **ADVISORY 1 (covered above):** §4.6 order is supported by dependency facts but no file restates the literal §4.6 string or cross-checks it against §9 (A1 open).
2. **ADVISORY 2 (covered above):** colon-namespaced degrade-token house-style tension — documented on both sides; builder must decide (recommend: follow spec's mandated tokens).
3. **ADVISORY 3 (MINOR):** R1 Point 7 L103 and R3 §5 differ slightly on the `contract_version` target string — R1 hedges "house style is 2-segment `"1.0"`; spec's 1.1.0 likely renders as `"1.1"`; confirm with R2/R6", while R3 §5 (L206-216) and R6 are firm that the bump normalizes to **3-segment SemVer `"1.1.0"`** (spec:318/351/402/471) and R2 Pattern 7 says `"1.1"`. Net: R3/R6 (which cite the spec's explicit `1.1.0` mandate at 4 line numbers) are authoritative; R1/R2's "1.1" is the looser house-style guess. The builder should use **`"1.1.0"`** per the spec, at all 3 sites (`:491` heading, `:494` yaml, `:599` trailer). This minor inter-file phrasing difference is resolvable in the spec's favor and does not block.
4. **ADVISORY 4 (MINOR, cosmetic):** 03-refs-and-inline-contract.md has a header `Status: In Progress` (L6) but every section is fully populated and the file ends `Status: Complete` (L318). The body is complete; the header line is stale. No content gap — purely a header-hygiene inconsistency. (Per the completeness checklist item 4, a literal "Status: In Progress" header would normally FLAG; here the trailing `Status: Complete` and the fully-populated body resolve it to a cosmetic note rather than an incomplete-file gap.)

---

## Depth Assessment

**Expected depth:** Deep tier — data flow traces, integration-point mapping, pattern analysis.

**Actual depth achieved:** Meets/exceeds Deep tier.

- **Integration-point mapping:** R1 (10 SKILL.md points with anchors) + R3 (5 refs/inline targets with current text) = exhaustive edit-target map.
- **Pattern analysis:** R2's 8 patterns with verbatim examples and house-style rules is textbook Deep-tier pattern documentation.
- **Data/dependency flow:** R6 traces the FR dependency DAG (FR-7→FR-6/FR-8 version gating; FR-2→FR-4 predicate; FR-1+FR-2 bundle), version-gate inventory across 5 Serena releases, and OQ probe→FR-gated→blocking relationships.
- **Verification surface:** R4 traces the eval pipeline (expected.yaml → evals.json assertions[] → eval_metadata.json → grader.py → aggregate_iteration.py) with code line cites.
- **Process grounding:** R5 maps the full MDTM template rule surface to the task.

**Missing depth elements:** None. The corpus is deeper than typical Deep-tier research, particularly on the external-Serena-surface uncertainty (correctly bounded by OQ probes rather than guessed).

---

## Recommendations (for the task-builder, before/during construction)

1. **Use `"1.1.0"` (3-segment) for the contract_version bump** at all 3 sites (`:491`/`:494`/`:599`), per spec:318/351/402/471 (R3/R6 authoritative over R1/R2's "1.1" guess). [Advisory 3]
2. **Adopt the spec's colon-namespaced degrade tokens** (`serena:context-excluded`, etc.) despite no in-file precedent, since the spec mandates them and the FR acceptance criteria assert them; note in the task that this introduces a new token grammar. [Advisory 2 / Cross-Check E]
3. **Include coverage-mapping.md (`:89-111`) as an FR-1 edit target** (default to editing it), and resolve the formula-vs-weight OQ explicitly in the FR-1 items. [Important Gap 2 / Cross-Check A]
4. **Author FR-4/FR-5 deviation-signal edits as PAIRED edits** to BOTH deviation-taxonomy.md AND SKILL.md §10.2/§10.3, with the §10.5 precedence guard. [Cross-Check B]
5. **FR-6 must CREATE the §4.0 step-0.7 detailed prose block** (it does not exist); confirm 0.5b prose treatment for FR-7's 0.5c placement. [Cross-Check D]
6. **Per eval case author BOTH** `expected.yaml` (human) AND an `evals.json` eval object with `assertions[]` (machine); use `regex_present` for `<tool>_invoked` JSONL audit fields, `yaml_field` for top-level contract scalars, `yaml_list_contains` for nested. [Cross-Check C]
7. **Create exactly OQ-1..OQ-5 as precondition items** (NOT OQ-6/OQ-7); OQ-1 is a hard merge blocker for FR-3, OQ-3/OQ-4 are SHOULD-probe (OQ-4 defensive-parse mandatory). [Criterion 8]
8. **Carry C1-C5 as FR acceptance criteria/guards** — especially C1 (the one CRITICAL: `memory_retention_unbounded` + "keep last 20 deletable") and C2 (`serena_version` three-valued, `unknown`≡`<v1.5`). [Criterion 8 / R6 §4]
9. **Reconcile or explicitly carry spec A1** (§4.6 vs §9 FR-6 placement) when laying out phases. [Advisory 1 / Important Gap 1]
10. **Embed the fresh-pre-edit-Read discipline** in every source-edit item (research line numbers may have drifted), and keep the OQ-2 grep belt-and-suspenders check. [R5 §7 / R6 OQ-2]

---

## VERDICT: PASS

All 9 completeness criteria PASS. All 6 researcher-flagged internal-consistency cross-checks PASS (consistent, no contradictions). Zero CRITICAL gaps, zero IMPORTANT research gaps. Two IMPORTANT spec-level gaps (A1 ordering; coverage-mapping.md FR-1 conditionality) and four MINOR advisory notes are surfaced for the builder — all are decision points the research correctly documented rather than research deficiencies. The corpus meets/exceeds Deep-tier depth and is sufficient for the task-builder to author per-FR / per-file / per-eval-case checklist items without re-research.

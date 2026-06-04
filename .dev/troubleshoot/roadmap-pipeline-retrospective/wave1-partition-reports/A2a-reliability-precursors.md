# Partition A2a — Roadmap Reliability + Obligation Vocab + Reflect-Path

**Scope:** Three reliability-precursor releases that preceded the dedicated anti-instinct gate work:
1. `v.2.17-roadmap-reliability/` — gate tolerance, output sanitizer, prompt hardening, protocol parity
2. `obligation-vocab-alignment/` — anti-instinct false-positive remediation via shared vocabulary
3. `reflect-path-regression/` — `/sc:reflect` protocol refactor surfacing roadmap→tasklist drift

**Method:** File-budget read (12 files Read, 0 Auggie lookups — failures already richly documented in artifacts; no additional codebase grounding needed for retrospective.)

---

## Findings

### F-A2a-001: Extract step halts on conversational preamble before YAML frontmatter
- **Type:** FAILURE
- **Pipeline step:** extract
- **Symptom:** `superclaude roadmap run` halted at step 1/8 with `YAML frontmatter missing or unparseable in extraction.md: no opening ---`. Claude subprocess emitted a 1-line preamble (`"Now I have the full spec. Let me produce the extraction document."`) before the `---` block; the content was otherwise valid (190 lines, all required fields).
- **Root cause (claimed):** Compound — (a) `_check_frontmatter()` in `pipeline/gates.py` did a byte-0 `lstrip().startswith("---")` check with zero preamble tolerance; (b) `ClaudeProcess` wrote raw stdout directly to the artifact with no post-processing; (c) the extract prompt didn't sufficiently constrain output format.
- **Remediation applied:** Four-priority defense-in-depth (FR-051, spec v1.0.0): P1 regex-based frontmatter discovery in `gates.py`, P2 `_sanitize_output()` in `roadmap/executor.py` (atomic `.tmp` + `os.replace`), P3 XML-tagged `<output_format>` constraint appended to all 7 `build_*_prompt()` functions, P4 expand `build_extract_prompt()` from 3 to 13+ frontmatter fields for source-protocol parity. 5 phases, 17 tasks, 21 deliverables.
- **Outcome:** Spec + tasklist produced; phase results exist (`results/phase-1..5-result.md`). Spec line 32 quantifies: at 10% preamble rate, P(all 8 pass) drops to 43%. The remediation gives all 8 steps a tolerant gate AND a sanitizer, so the compound failure mode is closed at two layers — but the original brittleness (raw stdout→artifact) was structural, not a one-off LLM quirk.
- **Still possible today (Auggie check):** NOT CHECKED. Symptom class (gate brittleness on LLM preamble) is plausibly still re-discoverable in any new gate that uses byte-0 `startswith` semantics.
- **Source artifacts:** `v.2.17-roadmap-reliability/roadmap-extract-failure-2.md` lines 14-44, `roadmap-extract-failure-context.md` lines 80-96, `spec-roadmap-pipeline-reliability.md` lines 25-45.

### F-A2a-002: CLI extract prompt under-specified vs source `sc-roadmap-protocol` template (schema drift)
- **Type:** FAILURE (latent)
- **Pipeline step:** extract → generate (downstream propagation)
- **Symptom:** The CLI `build_extract_prompt()` requested only 3 frontmatter fields (`functional_requirements`, `complexity_score`, `complexity_class`) while the source skill template (`sc-roadmap-protocol/refs/templates.md`) expected 13+ (`spec_source`, `generated`, `generator`, `nonfunctional_requirements`, `total_requirements`, `domains_detected`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode`, `pipeline_diagnostics`, etc.). Even after the preamble fix, downstream `generate` steps consuming `extraction.md` via `_embed_inputs()` would see a structurally thin extraction.
- **Root cause (claimed):** Programmatic CLI port did not faithfully mirror the skill protocol's artifact contract — "schema drift" between sc-roadmap skill and the CLI's roadmap executor (`roadmap-extract-failure-context.md` lines 99-120).
- **Remediation applied:** P4 in FR-051 (Phase 4 of the tasklist): expand `build_extract_prompt()` to request 13+ fields, update `EXTRACT_GATE`, ensure `build_generate_prompt()` consumes the expanded extraction. STRICT tier (sub-agent verification).
- **Outcome:** Spec'd and tasked. P4 was deliberately scoped to extract only — spec Section 8 logs as follow-up that "Other step prompt parity" (generate, diff, debate, score, merge, test-strategy) "may also have protocol drift. Audit all step prompts against source protocol templates." This is a structural Wave-2 finding: the protocol parity audit was descoped from this release.
- **Still possible today (Auggie check):** NOT CHECKED. Spec Section 8 explicitly leaves this open — drift in any of 6 other steps would surface as new failures.
- **Source artifacts:** `roadmap-extract-failure-context.md` lines 99-120, `spec-roadmap-pipeline-reliability.md` Section 8 (lines 305-313).

### F-A2a-003: Anti-instinct gate 100% false-positive rate on legitimate planning vocabulary
- **Type:** FAILURE
- **Pipeline step:** anti-instinct
- **Symptom:** Roadmap pipeline halted at anti-instinct with `Semantic check no_undischarged_obligations failed: undischarged_obligations must be 0`. Audit flagged 2 obligations as undischarged: roadmap line 93 (`| 2.2.1 | Scaffold command file using ...`) and line 220 (`Phase 2 (command scaffolding)`). Both were false positives — "Scaffold" as imperative-verb-meaning-create and "scaffolding" as parenthetical descriptive label, neither implying any real temporary artifact to discharge.
- **Root cause (claimed):** Vocabulary collision. The obligation scanner's `SCAFFOLD_TERMS` regex list and the LLM's generation prompts were entirely unaware of each other. The LLM freely emitted scaffold-family words for non-scaffold meanings; the scanner's `_is_meta_context()` classifier handled negation/verification/shell/risk/gate-criteria contexts but had no rule for table-cell imperatives or parenthetical phase labels (`handoff.json` debugging_log lines 67-73, `design.md` Section 1).
- **Remediation applied:** Two-layer defense (FR-MOD1.1):
  1. New `src/superclaude/cli/vocabulary.py` as single source of truth (11 SCAFFOLD_TERMS, 9 DISCHARGE_TERMS, 16-entry PREFERRED_ALTERNATIVES mapping, `build_prompt_constraint_block()`).
  2. Scanner imports terms from vocabulary; adds `_TABLE_CELL_IMPERATIVE_RE` (Layer 3a) and `_PAREN_PHASE_LABEL_RE` (Layer 3b) wired into `_is_meta_context()`.
  3. `build_generate_prompt()` and `build_merge_prompt()` append the vocabulary constraint block (~130 tokens) telling the LLM which words trigger the scanner and giving preferred alternatives.
- **Outcome:** Verified resolved. Per `handoff.json` step 8: 102 affected tests pass (97 baseline + 5 new), `undischarged_count=0` on the previously-failing roadmap, lines 93 and 220 correctly demoted to MEDIUM. Quality-engineer agent confirmed implementation sound. Full suite: 4959 passed (3 pre-existing unrelated failures).
- **Still possible today (Auggie check):** NOT CHECKED. Spec is explicit that Layer 3a only catches scaffold terms as the FIRST word in a table cell — mid-cell occurrences (e.g., `| Task | Build scaffold for module |`) still flag HIGH by design. This is a deliberate boundary, not a defect, but it means the false-positive surface is narrowed, not eliminated.
- **Source artifacts:** `obligation-vocab-alignment/design.md` lines 17-30, `workflow.md` Steps 1-3, `handoff.json` project_overview + debugging_log + milestones.

### F-A2a-004: Roadmap-to-tasklist generator emits low-confidence tier classifications on noun-phrase roadmap items
- **Type:** FAILURE (process-level)
- **Pipeline step:** OTHER (roadmap→tasklist generation, upstream of execution)
- **Symptom:** All 14 tier classifications in the reflect-path-regression tasklist showed confidence 0.65-0.80. Root cause documented in `tasklist-index.md` Generation Notes: "matrix-row descriptions are noun phrases ('Track-state audit', '3-way delta sweep') that lack the explicit imperative verbs ('implement', 'add', 'create') that the keyword scanner expects."
- **Root cause (claimed):** Roadmap→Tasklist Generator v4.0's tier classifier is keyword-driven over imperative verbs; RCA-format roadmaps (priority matrix tables) describe outcomes as noun-phrase audits/sweeps, not imperative actions. Stage 4 enrichment compensated by baselining confidence to 0.70.
- **Remediation applied:** Compensating action in the generator (baseline to 0.70) plus downstream Stage 7-10 validation. ValidationReport.md surfaced this as M3 (T02.01 70% understates Phase 5's explicit Tier 1.5 designation) and patched to 85%.
- **Outcome:** Partial — the validation pass caught one specific instance (T02.01) and bumped it; the other 13 low-confidence classifications remained. The underlying classifier is unchanged.
- **Still possible today (Auggie check):** NOT CHECKED. The generator behavior is deterministic and unchanged absent a code change to Stage 4.
- **Source artifacts:** `reflect-path-regression/tasklist/tasklist-index.md` Generation Notes lines 159-166, `ValidationReport.md` M3 (lines 42-48).

### F-A2a-005: Roadmap→Tasklist generation invents dependencies not present in source roadmap
- **Type:** FAILURE
- **Pipeline step:** OTHER (roadmap→tasklist generation)
- **Symptom:** ValidationReport M4: T04.01 (A2) Why field said "With T03.07 (C2) shipped in Phase 3, this becomes viable", converting Phase 5's conditional "reconsider" warning into a green-light. ValidationReport M6: T04.06 (A3) Dependencies and mid-phase-checkpoint Exit Criteria coupled A3's ship/Defer decision to T04.05's outcome — but the source roadmap line 64-65 said "Defer unless an independent ledger is built for other reasons", which is a precondition about a separate initiative, not a tasklist-internal dependency.
- **Root cause (claimed):** UNDOCUMENTED structurally, but inferable: the generator promotes conditional/cautionary roadmap language into actionable directives. INFERENTIAL — likely the Stage 4 enrichment heuristic that synthesizes dependency edges from co-occurring task IDs without consulting whether the source text frames the relationship as conditional, redundant, or sequential.
- **Remediation applied:** Stage 9 validation patches: M4 rewritten to preserve the "reconsider may favor retirement" framing + new Step 1 "Decide ship-vs-retire for A2" inserted; M6 Dependencies retied to "independent ledger initiative" only.
- **Outcome:** Resolved at the tasklist artifact level. The generator behavior that produced the drift is unchanged — every future RCA-format roadmap with redundancy/conditional language will need the same Stage 7-10 catch.
- **Still possible today (Auggie check):** NOT CHECKED. This is a generator-design property; resolution required validation gate to catch it.
- **Source artifacts:** `ValidationReport.md` M4 (lines 50-56), M6 (lines 66-72), L5/L6/L7 (lines 107-129).

### F-A2a-006: Spec format detection falls back when fed RCA findings instead of TDD
- **Type:** FAILURE (graceful degradation)
- **Pipeline step:** OTHER (tasklist generation)
- **Symptom:** Generator detected `00-consolidated-findings.md` as RCA findings format (not TDD: "no `## 10. Component Inventory`, no TDD frontmatter, only ~5 numbered `##` sections"). Per Stage 4.1a fallback rule, warning logged and generation continued with roadmap-only content. No supplementary tasks generated from `--spec`.
- **Root cause (claimed):** The tasklist generator assumes spec inputs are TDD-format; RCA-format specs have a different shape (numbered findings, no component inventory).
- **Remediation applied:** Pre-existing fallback rule (Stage 4.1a) — degrade gracefully to roadmap-only generation with a warning.
- **Outcome:** Mitigated, not fixed. The fallback works but means RCA-format specs contribute zero supplementary task structure. Anyone using the generator with an RCA spec gets a less-rich tasklist without realizing the supplementary path was skipped.
- **Still possible today (Auggie check):** NOT CHECKED. The Stage 4.1a fallback is documented and intentional.
- **Source artifacts:** `reflect-path-regression/tasklist/tasklist-index.md` Generation Notes line 159.

### F-A2a-007: Phase checkpoint exit criteria fail to encode joint-confidence promises from source roadmap
- **Type:** FAILURE
- **Pipeline step:** OTHER (tasklist→checkpoint generation)
- **Symptom:** ValidationReport M2: Phase 1 end-of-phase checkpoint Purpose mentioned the ≥0.95 joint-confidence promise from Phase 4 of the source roadmap, but Exit Criteria required only LOC bounds and "Phase 2 unblock" — no measurable attestation. ValidationReport H1: End-of-Phase 3 checkpoint misattributed the ~0.99 joint-confidence claim to "Tier 1 + Tier 1.5 + Tier 2 stack" when the source roadmap attributed it to "Tier 2 shipped on top of Tier 1".
- **Root cause (claimed):** Checkpoint template synthesizes Purpose strings from roadmap quotes but doesn't transfer the corresponding measurement obligation into Exit Criteria.
- **Remediation applied:** Stage 9 patches: M2 third Exit Criterion replaced with joint-confidence attestation requirement; H1 Purpose rewritten to match roadmap line 58-59. Pattern: edit the literal artifact text after validation finds the drift.
- **Outcome:** Resolved at artifact level. Same generator-design property as F-A2a-005 — would re-occur on the next RCA-format input.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `ValidationReport.md` H1 (lines 16-22), M2 (lines 35-40).

### F-A2a-008: Stage 9 deviation — patches applied directly via Edit tool instead of `sc:task-unified --compliance strict`
- **Type:** REMEDIATION (deviation flag)
- **Pipeline step:** remediate
- **Symptom:** ValidationReport line 138-139: "Stage 9 deviation: patches applied directly via Edit tool per PatchChecklist diff intents rather than delegating to `sc:task-unified --compliance strict`; equivalent compliance posture given each diff was fully specified, tier-tagged, and verified post-application via grep spot-check."
- **Root cause (claimed):** Convenience — direct edits were faster than spawning a strict-compliance subprocess for the 14 patches.
- **Remediation applied:** Self-reported as equivalent-posture; verification was grep-based spot-check rather than independent re-validation.
- **Outcome:** Functionally acceptable here (small patches, fully specified intents). Structurally: the deviation taxonomy slot for "skipped compliance scaffolding for convenience" gets normalized into release records. If this becomes a pattern, the validation pass loses its independence claim.
- **Still possible today (Auggie check):** NOT CHECKED. This is a process discipline marker, not a code property.
- **Source artifacts:** `ValidationReport.md` Verification Results lines 137-139.

### F-A2a-009: Compound-reliability math: P(all-pass) collapse with per-step failure rates
- **Type:** SUCCESS (analytical framing) / REMEDIATION
- **Pipeline step:** OTHER (architectural reasoning)
- **Symptom:** Spec Section 2 frames the gate brittleness in compound terms: "All 8 pipeline steps share `_check_frontmatter()` code path. With a conservatively estimated 10% preamble rate per step: P(all 8 pass) = 0.9⁸ = 43% end-to-end success." This made the case for shared-component fixes rather than per-step patches.
- **Root cause (claimed):** Not a defect — this is the correct framing of a shared-fragile-substrate failure mode.
- **Remediation applied:** Defense-in-depth (P1 + P2 + P3) — gate fix raises P to 100% even at high preamble rate; sanitizer cleans artifacts so preamble doesn't propagate via `_embed_inputs()`; prompt hardening reduces frequency.
- **Outcome:** Conceptually strong. Whether the implementation actually achieved 100% in practice depends on test results from `results/phase-5-result.md` — not Read in this budget.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `spec-roadmap-pipeline-reliability.md` lines 32-34, `roadmap-extract-failure-2.md` lines 170-178.

### F-A2a-010: Sanitizer scope decision — roadmap-executor-local, not shared-pipeline-level
- **Type:** SUCCESS (design decision)
- **Pipeline step:** OTHER (architectural)
- **Symptom:** Spec Section 2.1: "Sanitizer scope: Roadmap executor, not shared pipeline. Pipeline-level is too broad; roadmap-specific preamble patterns."
- **Root cause (claimed):** N/A — this is a scope decision.
- **Remediation applied:** N/A.
- **Outcome:** Decision locks the sanitizer to roadmap's executor. If sprint or other pipeline commands later encounter the same preamble pattern, the sanitizer logic will be duplicated unless promoted to `cli/pipeline/`. Parallels the obligation-vocab decision to elevate `vocabulary.py` to `cli/` (not `cli/roadmap/`) for future reuse — the two releases made opposite scoping calls.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `spec-roadmap-pipeline-reliability.md` lines 50-55, `obligation-vocab-alignment/design.md` Section 3.1.

---

## Cross-cutting patterns within this partition

1. **Brittle "byte-0" gates over LLM-generated artifacts** (F-A2a-001, F-A2a-003) — both failures had the same shape: a deterministic check assumed strict input form, the LLM produced semantically valid but format-deviant output, the check rejected. Pattern resolution: dual-layer (LLM-side prompt constraint + parser-side tolerance). Single-layer fixes are insufficient because LLMs cannot be perfectly constrained.

2. **Schema drift between skill-protocol source-of-truth and CLI ports** (F-A2a-002, F-A2a-005) — the programmatic CLI implementations under-spec the artifact contracts defined in the source skills. Drift surfaces only when the artifact has to flow to a downstream consumer that expects the richer contract. Spec Section 8 explicitly defers a parity audit across all 6 remaining roadmap steps.

3. **Generator emits structurally-invented relationships** (F-A2a-005, F-A2a-007) — the roadmap→tasklist generator promotes conditional language into dependencies, splits joint-confidence promises across Purpose/Exit Criteria, and invents user-confirmation steps (L1) and comment-syntax alternatives (L2) not present in source. Stage 7-10 validation is the only catch — it currently caught 14/14 findings (1 High, 6 Medium, 7 Low) but a generator-side fix never landed.

4. **Validation-as-only-line-of-defense for generator drift** (F-A2a-005, F-A2a-007, F-A2a-008) — once the generator emits drift, only the validation pass catches it. The Stage 9 deviation (direct Edit tool vs `sc:task-unified --compliance strict`) shows the validation discipline already softening under convenience pressure.

5. **Confidence-as-compensation rather than fix** (F-A2a-004) — when the tier classifier hits noun-phrase descriptions it can't score, the system baselines confidence to 0.70 rather than improving the classifier or surfacing the ambiguity for human resolution. ValidationReport bumped one instance (T02.01) to 85% but the underlying classifier behavior persists.

6. **Compound reliability framing as forcing function** (F-A2a-009) — explicit `0.9^8 = 43%` math in the spec is what makes the case for shared-component fixes over per-step patches. This framing should be reused in future shared-substrate failures.

7. **Source-of-truth elevation as anti-drift mechanism** (F-A2a-003, F-A2a-010) — obligation-vocab created `cli/vocabulary.py` (one module, two consumers, identity check via test); roadmap-reliability kept sanitizer roadmap-local. The vocabulary approach is more robust — drift would now require breaking the import. Worth applying the same pattern to any future shared-fragile-substrate.

---

## Brittleness drivers identified

- **Driver 1: Byte-0 strict parsers over non-deterministic stdout.** `_check_frontmatter()` used `lstrip().startswith("---")` semantics. Any gate that does positional matching on LLM output will exhibit this failure mode.
- **Driver 2: Raw subprocess stdout written directly to artifact files.** `ClaudeProcess` writes stdout to disk with no normalization stage between subprocess and gate. Eliminating preamble at the source is impossible without a sanitization seam.
- **Driver 3: Two unrelated modules independently encoding the same vocabulary.** Obligation scanner and LLM prompts both knew about scaffold terms but had no shared definition. Drift was guaranteed.
- **Driver 4: Roadmap→tasklist generator promotes language without preserving qualifier semantics.** "Reconsider", "may be retired", "if independent ledger is built" become unconditional dependencies/steps. The generator's enrichment heuristics over-determine intent.
- **Driver 5: Tier classifier keyed to imperative-verb vocabulary, not roadmap structure.** RCA-format roadmaps (matrix tables, noun-phrase audits) systematically score low; the compensation is a confidence baseline rather than a structural fix.
- **Driver 6: Validation pass is the only line of defense for generator drift.** No fix flows back into the generator from the validation findings — every future tasklist re-pays the same validation cost.
- **Driver 7: Spec-format detection has a graceful-degradation fallback that silently reduces output quality.** Stage 4.1a logs a warning but downstream consumers don't see the warning; they get a less-rich tasklist than expected.
- **Driver 8: Compliance scaffolding (`sc:task-unified --compliance strict`) is skippable for "equivalent posture" reasons** — the Stage 9 deviation in reflect-path-regression normalizes this skip; if it becomes routine, the independence claim of the validation pass dissolves.

---

## Budget note
- Files Read: 12 (roadmap-extract-failure-2.md, roadmap-extract-failure-context.md, spec-roadmap-pipeline-reliability.md, tasklist-index.md, phase-5-tasklist.md, obligation-vocab design.md, workflow.md, handoff.json, reflect-path tasklist-index.md, ValidationReport.md, plus 2 ls listings)
- Files Skipped (over budget): ~20 (phase-1..4 tasklists in both v.2.17 and reflect-path, results/phase-*-output.txt, artifacts/D-* subdirs, execution-log files, checkpoints/, pipeline-output/, roadmap.md and extraction.md, roadmap-spec-panel-correctness-adversarial-v1.md, PatchChecklist.md)
- Auggie lookups: 0 — failures already had richly documented artifact-side evidence; no failure rose to "needs codebase grounding to assess whether still possible today" beyond the boundaries already documented in the spec/handoff (e.g., FR-051 §8 explicitly leaves protocol parity audit open, and design.md known_limitations explicitly lists the residual surfaces).

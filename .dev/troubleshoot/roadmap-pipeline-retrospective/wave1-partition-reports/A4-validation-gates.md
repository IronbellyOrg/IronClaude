# A4 — Validation Gates Retrospective

**Partition focus:** Gate proliferation — what fails each gate, what bypasses exist, the false-positive / false-negative pattern across gates.

**Directories mined:**

- `.dev/releases/complete/v2.19-roadmap-validate/`
- `.dev/releases/complete/v2.24.5-SpecFidelity/`
- `.dev/releases/complete/v3.0_unified-audit-gating/`
- `.dev/releases/complete/v3.05_DeterministicFidelityGates/`
- `.dev/releases/complete/unified-audit-gating-v1.2.1/`
- `.dev/releases/complete/unified-audit-gating-v2/`

---

## Findings

### F-A4-001: `superclaude roadmap validate` — always-on post-pipeline reflection added
- **Type:** SUCCESS
- **Pipeline step:** OTHER (validate sub-pipeline; reflect + adversarial-merge)
- **Symptom:** Roadmap pipeline outputs that passed per-step gates (frontmatter shape, line count, heading hierarchy) were still slipping through with cross-file inconsistencies that broke `sc:tasklist` downstream — duplicate D-IDs, dangling milestone refs, traceability gaps. v2.19 introduces a 7-dimension validate stage (schema, structure, traceability, cross-file, interleave, decomposition, parseability) with single-agent or multi-agent adversarial modes, on by default, gated by `REFLECT_GATE` / `ADVERSARIAL_MERGE_GATE`.
- **Root cause (claimed):** Per-step gates only verified per-file structural properties; no cross-file or DAG-level checks existed (`spec-roadmap-validate.md` §1).
- **Remediation applied:** New `validate_executor.py` + `validate_gates.py` + `validate_prompts.py`. `--no-validate` opt-out. Auto-invoked after `roadmap run` succeeds. Multi-agent adds Agent Agreement Analysis table check.
- **Outcome:** Adopted; still active. The v3.05 run uses the multi-agent variant (`validate/reflect-opus-architect.md`, `reflect-haiku-architect.md`, `validation-report.md`).
- **Still possible today (Auggie check):** YES — gates remain at `src/superclaude/cli/roadmap/validate_gates.py:14-69`, exposing `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` with the agreement-table semantic check intact.
- **Source artifacts:** `v2.19-roadmap-validate/spec-roadmap-validate.md`, `v2.19-roadmap-validate/debate-transcript.md`.

### F-A4-002: Validate gate ships with non-blocking severity — blocking issues warn but don't exit non-zero
- **Type:** REMEDIATION (intentional design) / latent FAILURE
- **Pipeline step:** validate (reflect + adversarial-merge)
- **Symptom:** `spec-roadmap-validate.md` §2.2 and §8.2 stipulate "warn, don't fail" even when `blocking_issues_count > 0`. v3.05's `validate/validation-report.md` shows 5 BLOCKING findings (frontmatter missing fields, dangling OQ IDs, regex misses top-level FR/NFR IDs, deliverables not back-traced) with `tasklist_ready: false`, yet the parent pipeline exited zero and downstream tooling proceeded.
- **Root cause (claimed):** "User may want to proceed with known issues" — explicit non-blocking design decision documented in spec table §2.2.
- **Remediation applied:** None planned; this is the documented behavior.
- **Outcome:** Creates a false sense of security — blocking issues surface in the report but do not halt the pipeline. Downstream `sc:tasklist` runs are not prevented from consuming broken artifacts. The roadmap pipeline retrospective elsewhere documents tasklist downstream breakages.
- **Still possible today (Auggie check):** YES — `validate_gates.py:14-46` (REFLECT_GATE) checks only that the frontmatter fields are present and non-empty; there is no semantic check `blocking_issues_count == 0`. The gate passes regardless of how many BLOCKING findings the LLM logs.
- **Source artifacts:** `v2.19-roadmap-validate/spec-roadmap-validate.md` §2.2, §FR-050.5, §8.2; `v3.05_DeterministicFidelityGates/validate/validation-report.md`.

### F-A4-003: Spec-fidelity gate disabled in convergence mode (`gate=None`)
- **Type:** FAILURE (structural)
- **Pipeline step:** spec-fidelity (convergence path)
- **Symptom:** v3.05 weakness analysis identifies that `executor.py:869` sets `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE`. The convergence engine validates its own logical convergence but no external gate validates the written report's frontmatter, structural progress log, budget state, or shape. When convergence wiring crashed (B1-B3 below), the gate could not produce structured diagnostics; the pipeline trusted `result.passed` boolean.
- **Root cause (claimed):** "convergence engine has its own internal validation, so an external gate might be redundant" — challenged and overruled in the weakness analysis as a real gap (`pipeline-weakness-analysis.md` W2, Challenge 2).
- **Remediation applied:** Proposed `CONVERGENCE_SPEC_FIDELITY_GATE` validating frontmatter, progress log presence, and budget state. **Not implemented as of v3.05 — recommendation only.**
- **Outcome:** Open. Convergence runs ship without a format-validating gate.
- **Still possible today (Auggie check):** YES — `executor.py:2167` still contains `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE`. The bypass is unchanged.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/v3.05/pipeline-weakness-analysis.md` (Weakness 2), `v3.05_DeterministicFidelityGates/v3.05/roadmap-gap-analysis-merged.md` (root cause).

### F-A4-004: Wiring-verification gate scans the wrong directory — 0 files analyzed silently passes
- **Type:** FAILURE (false-negative; gate became a no-op)
- **Pipeline step:** wiring-verification
- **Symptom:** `v2.24.5-SpecFidelity/wiring-verification.md`, `unified-audit-gating-v1.2.1/wiring-verification.md`, and `v3.0_unified-audit-gating/wiring-verification.md` all show `files_analyzed: 10` against `.dev/releases/complete` (analyzing markdown release artifacts, not Python source), and the gate emits 0 findings — PASS. v3.05 weakness analysis traced the bug to `executor.py:429` (old code path) where `source_dir = config.output_dir.parent` resolves to `.dev/releases/complete/` instead of `src/superclaude/`.
- **Root cause (claimed):** Wrong target directory in `source_dir` computation + no `files_analyzed > 0` guard inside `WIRING_GATE`. Identified as the primary cause of B1-B3 (call-arity and dict/object bugs in convergence wiring) going undetected.
- **Remediation applied:** Partial. v3.05 gap-remediation tasklist task T08/T14 ("Fix wiring-verification target directory") were **NOT EXECUTED** (per `execution-qa-reflection.md`). However, current code shows the fix landed afterward: `executor.py:1019-1022` now uses `Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")`, and `wiring_gate.py:698-714` adds an early-return FAIL path when `files_analyzed == 0` with `failure_reason="0 files analyzed in non-empty source directory"`.
- **Outcome:** Fix applied post-v3.05. `v3.05_DeterministicFidelityGates/wiring-verification.md` shows `files_analyzed: 166`, demonstrating the source-dir bug was corrected in that release boundary. Note: this is hardcoded `src/superclaude` — non-portable if pipeline runs from a different repo root, but functional for in-repo runs.
- **Still possible today (Auggie check):** NO for this exact bug — `src/superclaude/cli/roadmap/executor.py:1019-1022` and `src/superclaude/cli/audit/wiring_gate.py:698-714` confirm both fixes are in place.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/v3.05/pipeline-weakness-analysis.md` W1, `v3.05_DeterministicFidelityGates/v3.05/execution-qa-reflection.md` T08/T14, `unified-audit-gating-v1.2.1/wiring-verification.md`, `v2.24.5-SpecFidelity/wiring-verification.md`.

### F-A4-005: Spec-fidelity gate is non-deterministic — 5 runs, 4 distinct deviation counts, content regenerated mid-loop
- **Type:** FAILURE (LLM gate non-determinism)
- **Pipeline step:** spec-fidelity, remediate
- **Symptom:** v3.0 unified-audit-gating ran the spec-fidelity gate 5 times against the same spec+roadmap pair. Results: Run 1: 3H/9M/5L. Run 2: 3H/8M/5L. Run 3: 1H/6M/3L. Run 4: 3H/8M/4L — **the roadmap was regenerated from scratch with a completely different phase structure and task numbering**, losing all Runs 1-3 edits. Run 5: 0H/7M/3L after 5-vote consensus aggregation. Two HIGH findings flagged in the final raw check were absent from all 5 consensus votes and reclassified as DISPUTED noise.
- **Root cause (claimed):** LLM attention drift between runs surfaced new findings on each pass; remediation prompts caused full regeneration rather than surgical edits; no determinism floor.
- **Remediation applied:** 5-vote statistical aggregation (`fidelity-consensus.md`) became the bypass strategy — vote across 5 independent fidelity checks, majority severity wins, tie breaks low. Findings flagged by 1-2 of 5 votes classified as NOISE. This pattern directly motivated v3.05 "Deterministic Fidelity Gates" release.
- **Outcome:** Statistical aggregation worked but is itself a workaround for a non-deterministic gate. Drove the v3.05 architecture (structural rules + convergence engine + TurnLedger budget).
- **Still possible today (Auggie check):** UNKNOWN — `SPEC_FIDELITY_GATE` at `gates.py:1274-1297` still only requires frontmatter fields + `high_severity_count_zero` + `tasklist_ready_consistent` semantic checks. The non-determinism source is the LLM that generates the report, not the gate; v3.05's convergence engine is the structural answer but legacy LLM mode (`convergence_enabled=False`) still has the same property.
- **Source artifacts:** `v3.0_unified-audit-gating/fidelity-remediation-log.md` (Runs 1-5), `v3.0_unified-audit-gating/fidelity-consensus.md`.

### F-A4-006: Phantom FR-NNN identifiers — 5/5 vote consensus HIGH that gate consistently missed inside the loop
- **Type:** FAILURE (gate false-negative)
- **Pipeline step:** spec-fidelity, generate, merge
- **Symptom:** All 5 fidelity-vote agents independently flagged that the v3.0 roadmap referenced ~30 FR-NNN identifiers (FR-009 through FR-038) that did not exist anywhere in the spec. Some votes rated HIGH (3), others MEDIUM (2). Despite this being the most consistently agreed deviation (confidence 1.0), prior single-pass fidelity gates did not classify it as blocking — only Runs 1-3 mentioned it as a MEDIUM that was deferred to "comprehensive pass."
- **Root cause (claimed):** Variant generators invented FR/NFR IDs as a structural convenience without checking against extracted spec requirements. Single-agent fidelity checks were tolerant of phantom IDs because the LLM judged "does this look like a requirement table?" rather than "do these IDs appear in the spec?"
- **Remediation applied:** Global replace of all FR-NNN with spec-native identifiers (G-NNN, SC-NNN, spec §section). Kept NFR-007 which is the only NFR-NNN actually defined in spec §3.2.
- **Outcome:** Resolved by the consensus vote + manual remediation. v3.05's structural fidelity layer (FR-1 through FR-4) is designed to make this catchable deterministically.
- **Still possible today (Auggie check):** YES — `SPEC_FIDELITY_GATE` semantic checks (`gates.py:1285-1295`) check frontmatter consistency but do not validate that requirement IDs cited in the roadmap actually appear in the spec. The fingerprint_coverage check in WIRING_GATE addresses a different problem (code identifiers). The phantom-ID class of failure would still need either the convergence-mode structural checkers (`structural_checkers.py`) or the LLM noticing.
- **Source artifacts:** `v3.0_unified-audit-gating/fidelity-consensus.md` F-01, `v3.0_unified-audit-gating/fidelity-remediation-log.md` Run 5.

### F-A4-007: Mid-loop spec amendment — gate forced amending the spec to clear its own contradictions
- **Type:** REMEDIATION (boundary-blurring fix)
- **Pipeline step:** spec-fidelity
- **Symptom:** v3.0 Run 3 surfaced an "audit_artifacts_used spec internal contradiction": spec §5.4 report example included the field but §5.6 `required_frontmatter_fields` omitted it (14 fields). To clear the HIGH, the remediation amended `merged-spec.md` §5.6 itself, expanding to 16 fields. Same pattern for `files_skipped`.
- **Root cause (claimed):** Spec was self-inconsistent and the fidelity gate had no way to resolve "deviation from §5.4 example or deviation from §5.6 contract."
- **Remediation applied:** Spec edited to match the example and the §8.2 gate contract. Roadmap OQ-2 updated to reference the spec amendment.
- **Outcome:** Spec-fidelity gate boundary was eroded — the gate that should validate roadmap-against-spec instead drove a spec change. Sets a precedent for mid-loop spec mutation that downstream auditability cannot easily distinguish from the original specification intent.
- **Still possible today (Auggie check):** UNKNOWN — the gate does not prevent its own remediation cycle from editing the spec. Whether this happens in practice depends on operator discretion; no programmatic block exists.
- **Source artifacts:** `v3.0_unified-audit-gating/fidelity-remediation-log.md` Run 3 DEV-001.

### F-A4-008: Adversarial validate-merge surfaces conflicting agent verdicts; resolution policy escalates all conflicts to BLOCKING
- **Type:** SUCCESS (mechanism worked) / latent FAILURE (false-positive risk)
- **Pipeline step:** validate (adversarial-merge)
- **Symptom:** v3.05 validate run showed 3 CONFLICT findings between Opus and Haiku reflect agents:
  - OQ numbering severity: Opus INFO vs Haiku BLOCKING → escalated to BLOCKING
  - Traceability: Opus INFO-pass "all traced" vs Haiku BLOCKING "gaps in backward trace" → escalated to BLOCKING
  - Frontmatter completeness: Opus BLOCKING vs Haiku INFO-pass → resolved as BLOCKING
- **Root cause (claimed):** Merge policy: "for severity conflicts, evaluate evidence and escalate to higher severity" (`spec-roadmap-validate.md` §5.2). This produces high recall by design.
- **Remediation applied:** None — the policy is the design.
- **Outcome:** Validate now produces more BLOCKING findings than either agent alone would, which is the intended behavior. Risk: the always-escalate policy means a single weak agent finding can drive BLOCKING; combined with F-A4-002 (warn-don't-fail), the practical impact is "noisier reports, but no halt." Net effect is well-tuned only if humans actually read the report.
- **Still possible today (Auggie check):** YES — `ADVERSARIAL_MERGE_GATE` (`validate_gates.py:48-69`) requires the agreement-table semantic check but does not constrain conflict resolution policy in code.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/validate/validation-report.md` (Conflict Resolutions section).

### F-A4-009: Forward traceability "pass" coexisted with backward traceability "fail" — gate covered only one direction
- **Type:** FAILURE (gate false-negative)
- **Pipeline step:** validate (traceability dimension)
- **Symptom:** v3.05 validate report `[B-4]` documents Agent A's INFO-pass ("all 12 FRs and 7 NFRs traced") in direct contradiction with Agent B's BLOCKING ("several deliverables lack backward traceability to requirement IDs"). Both checks were valid for their respective directions. The gate's traceability dimension as written in the reflection prompt did not specify bidirectional coverage as a hard requirement; the gate semantic checks did not enforce it either.
- **Root cause (claimed):** Spec §FR-050.5 dimension 3 lists "Every deliverable → requirement AND every requirement → deliverable" but the gate does not parse the report to verify both directions independently. A single-agent INFO-pass would have shipped without backward-trace findings.
- **Remediation applied:** Adversarial mode caught it because Haiku checked the reverse direction. No code change.
- **Outcome:** Single-agent validate runs remain vulnerable to single-direction blindspots. Multi-agent reduces but does not eliminate this risk.
- **Still possible today (Auggie check):** YES — `REFLECT_GATE` only checks frontmatter; traceability completeness depends on the LLM's reading of the prompt.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/validate/validation-report.md` B-4 and Conflict Resolution #2.

### F-A4-010: Gate set converged to 14 named gates in pipeline order — proliferation without unifying schema
- **Type:** REMEDIATION (organic expansion) / latent FAILURE
- **Pipeline step:** ALL gates in `ALL_GATES`
- **Symptom:** `gates.py:1426-1440` enumerates 14 gates: extract, generate-A, generate-B, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify. Each gate uses ad-hoc combinations of `required_frontmatter_fields`, `min_lines`, `enforcement_tier` (STANDARD/STRICT), and `semantic_checks` lists. The validate sub-pipeline adds another 2 gates (REFLECT_GATE, ADVERSARIAL_MERGE_GATE) with their own conventions. There is no shared registry of semantic check IDs, no global schema for what fields each gate expects, and no cross-gate consistency enforcement (e.g., `spec-fidelity` requires `high_severity_count` but doesn't bind it to `total_deviations` arithmetically beyond a single semantic check).
- **Root cause (claimed):** Each release added the gate it needed without rationalizing the gate framework. Documented across v2.19 spec, v3.0 unified-audit-gating spec, v3.05 deterministic-fidelity spec, unified-audit-gating-v1.2.1, unified-audit-gating-v2.
- **Remediation applied:** None at framework level; cross-gate deviation count reconciliation was added (gates.py:767) but is narrow.
- **Outcome:** Adding a gate is cheap; understanding the gate set requires reading all 14 GateCriteria + their semantic check functions. The "enforcement_tier" concept exists (STANDARD/STRICT) but its semantic difference is implicit in the executor's retry logic, not declarative. INFERENTIAL: this is the structural enabler of every other gate-bypass in this partition — there is no top-level invariant "every gate output must be deterministically re-checkable" or "no gate may set `gate=None`."
- **Still possible today (Auggie check):** YES — `gates.py:1426-1440` shows the same flat list. No registry-level schema or contract framework exists.
- **Source artifacts:** `gates.py:1426-1440` (current code, cited from Auggie sweep); spec evolution across v2.19, v3.0, v3.05.

### F-A4-011: Anti-instinct + cosmetic-remediator narrow gate remediation surface — only certain gates get auto-fix
- **Type:** REMEDIATION
- **Pipeline step:** anti-instinct, cosmetic remediation
- **Symptom:** `cosmetic_remediator.py:148-156` defines `_ROADMAP_GATE_NAMES` (frozenset of 5 names: template_sections_present, deliverable_table_schema, open_questions_placement, milestone_summary_present, frontmatter_required_fields). Only roadmap-flavored gates get the automatic cosmetic-fix loop; sprint/validate gates default to halt-on-failure. This prevents the cosmetic remediator from running over gates that are not designed for it.
- **Root cause (claimed):** Pipeline executor is generic; remediation scope must be narrowed by domain.
- **Remediation applied:** Whitelist by gate name.
- **Outcome:** Mitigates one class of cross-contamination but introduces a maintenance burden: any new roadmap gate that should benefit from cosmetic remediation must be added to this set. Easy to miss; no compile-time check.
- **Still possible today (Auggie check):** YES — `cosmetic_remediator.py:148-156` shows the frozenset in current code.
- **Source artifacts:** `cosmetic_remediator.py:148-156` (Auggie sweep).

### F-A4-012: `fidelity_checker.py` fail-open behavior — ambiguous FR mappings recorded as `found=True`
- **Type:** FAILURE (gate false-negative by design)
- **Pipeline step:** spec-fidelity (deterministic fidelity checker layer)
- **Symptom:** `fidelity_checker.py:287-303` shows that when an FR has no extractable names (e.g., narrative-only requirement with no class/function reference), the checker logs `marking as ambiguous (fail-open per R-3)` and emits `FidelityResult(fr_id=..., found=True, ambiguous=True)`. This means the fidelity check passes for any FR the parser cannot extract names for.
- **Root cause (claimed):** R-3 risk mitigation: false-positives on narrative requirements would block too many pipelines. Fail-open chosen as the safer default.
- **Remediation applied:** Explicit logging + `ambiguous=True` flag, but the gate-level aggregation treats `found=True` uniformly.
- **Outcome:** Real risk: a spec FR worded narratively will always pass fidelity even if completely unimplemented. The structural fidelity layer cannot distinguish "no implementation needed" from "implementation missing but spec is too vague to check."
- **Still possible today (Auggie check):** YES — `fidelity_checker.py:287-303` confirms the fail-open branch is intact in current code.
- **Source artifacts:** `src/superclaude/cli/roadmap/fidelity_checker.py:287-303` (Auggie sweep).

### F-A4-013: Wiring-verification gate did not catch convergence-mode crash bugs (B1-B3) — gap analysis post-mortem
- **Type:** FAILURE (compound: gate bypass + verification scope gap)
- **Pipeline step:** wiring-verification + spec-fidelity (convergence path)
- **Symptom:** v3.05 shipped with three runtime crash bugs in `_run_convergence_spec_fidelity()`:
  - B1: `DeviationRegistry.load_or_create()` called with 1 arg, requires 3
  - B2: `merge_findings()` called with 2 args, requires 3
  - B3: `finding.files_affected` attribute access on dict (registry stores JSON dicts not dataclass instances)
- **Root cause (claimed):** Subprocess-execution sprint model wrote the code, gates checked written-text shape only. No gate imported the code and called it with minimal valid inputs. Wiring-verification was misconfigured (F-A4-004) so even AST-level unwired-call detection wasn't running.
- **Remediation applied:** Wave 1 of `gap-remediation-tasklist.md` fixed B1-B3 (`execution-qa-reflection.md` T01-T03 PASS). Wave 3 testing infrastructure (T07 integration smoke test, T11 E2E tests) was **NOT EXECUTED**.
- **Outcome:** Crash bugs fixed; recurrence prevention layer was never built. Future similar bugs would not be caught by current gates.
- **Still possible today (Auggie check):** YES for the class of bug — no integration smoke test exists for new wiring code paths (`pipeline-weakness-analysis.md` W3, MEDIUM-LOW confidence).
- **Source artifacts:** `v3.05_DeterministicFidelityGates/v3.05/roadmap-gap-analysis-merged.md` (B1-B3), `v3.05_DeterministicFidelityGates/v3.05/pipeline-weakness-analysis.md` (W3), `v3.05_DeterministicFidelityGates/v3.05/execution-qa-reflection.md` (T07/T11 skipped).

### F-A4-014: Budget constants not validated against spec at pipeline construction
- **Type:** FAILURE (gate false-negative)
- **Pipeline step:** spec-fidelity (convergence path)
- **Symptom:** v3.05 shipped with `STD_CONVERGENCE_BUDGET=46` instead of spec-required `MAX_CONVERGENCE_BUDGET=61`, missing `minimum_allocation=CHECKER_COST`, missing `minimum_remediation_budget`, missing `reimbursement_rate=0.8` on TurnLedger constructor. The spec-fidelity step that should have caught the deviation was the step being modified — a self-referential gap.
- **Root cause (claimed):** No `validate_convergence_config()` assertion at function entry. Spec-fidelity cannot validate its own wiring.
- **Remediation applied:** Wave 2 fixes (T04, T05) applied per `execution-qa-reflection.md`. No structural validate-config helper added.
- **Outcome:** Fixed for v3.05's specific constants. Pattern remains: the next pipeline-modifying release has the same self-referential bootstrap problem.
- **Still possible today (Auggie check):** YES — the structural weakness (no construct-time validation of constants against spec) is unaddressed.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/v3.05/pipeline-weakness-analysis.md` W4, B4-B5.

### F-A4-015: v3.05's deterministic-fidelity replacement passes spec-fidelity at 0 HIGH after redesign
- **Type:** SUCCESS
- **Pipeline step:** spec-fidelity
- **Symptom:** `v3.05_DeterministicFidelityGates/spec-fidelity.md` reports 0 HIGH, 5 MEDIUM, 3 LOW (`tasklist_ready: true`). This is the post-redesign baseline against the v3.05 spec — a single-pass success on a release whose entire purpose was to make the fidelity gate deterministic.
- **Root cause (claimed):** N/A (success).
- **Remediation applied:** N/A.
- **Outcome:** Demonstrates that the structural-checker approach plus convergence engine can produce stable single-pass fidelity. Caveat: the validate stage (F-A4-008/009) still found 5 BLOCKING issues in the roadmap that this spec-fidelity check did not surface — the two gates surface different classes of defect.
- **Still possible today (Auggie check):** YES — structural checker pattern at `src/superclaude/cli/roadmap/structural_checkers.py` is the current implementation.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/spec-fidelity.md`.

### F-A4-016: 5-vote statistical consensus introduced as bypass mechanism for non-deterministic gates
- **Type:** REMEDIATION (process-level workaround)
- **Pipeline step:** spec-fidelity
- **Symptom:** v3.0 unified-audit-gating could not pass its own spec-fidelity gate in 4 successive runs. Solution: run 5 independent fidelity checks, aggregate by majority vote, classify 1-2/5 findings as NOISE, escalate 3+/5 findings by severity-majority. `fidelity-consensus.md` documents 14 unique findings across 5 votes with confidence scores.
- **Root cause (claimed):** LLM gate non-determinism (F-A4-005) made single-pass results untrustworthy.
- **Remediation applied:** Aggregation harness + manual NOISE classification + DISPUTED downgrade rule.
- **Outcome:** Worked for v3.0. Expensive (5x the gate cost) and labor-intensive (manual finding-matching across votes). Drove v3.05 deterministic replacement.
- **Still possible today (Auggie check):** UNKNOWN — the 5-vote pattern is not encoded in current code; convergence engine is the structural answer. If a user disables convergence (`convergence_enabled=False`), they revert to legacy LLM mode with no automated multi-vote aggregation.
- **Source artifacts:** `v3.0_unified-audit-gating/fidelity-consensus.md`, `fidelity-votes/vote-{1-5}.md`.

### F-A4-017: Release-split fidelity audit produced a 100% PRESERVED single-release decision
- **Type:** SUCCESS
- **Pipeline step:** OTHER (release-split fidelity verification)
- **Symptom:** `v3.0_unified-audit-gating/release-split/fidelity-audit.md` reports verdict VERIFIED, all 28 section changes preserved (100%), 3 valid additions (review-order guidance, decision-first checkpoint, implementation-independence callout), 0 dropped/weakened/scope-creep. Fidelity score 1.00.
- **Root cause (claimed):** N/A (success).
- **Remediation applied:** N/A.
- **Outcome:** Demonstrates a fidelity check that worked cleanly first-pass — likely because the input was a structured plan (`spec-refactor-plan-merged.md`) with discrete numbered changes, not a narrative document. The gate's success correlates strongly with input parseability.
- **Still possible today (Auggie check):** YES — release-split protocol still exists as a skill (`sc-release-split-protocol`).
- **Source artifacts:** `v3.0_unified-audit-gating/release-split/fidelity-audit.md`.

### F-A4-018: SpecFidelity v2.24.5 raised a single HIGH for wrong test-file path — gate caught a substantive deviation
- **Type:** SUCCESS
- **Pipeline step:** spec-fidelity
- **Symptom:** `v2.24.5-SpecFidelity/spec-fidelity.md` DEV-001 flagged that the roadmap directed Phase 2 test work to `tests/roadmap/test_executor.py (or equivalent)` whereas the spec was explicit about `tests/roadmap/test_file_passing.py`. The "or equivalent" qualifier was rated HIGH. The roadmap also picked up 5 MEDIUM and 4 LOW deviations (test phase sequencing, CLI failure retry semantics, unnamed boundary test, etc.).
- **Root cause (claimed):** Roadmap added flexibility hedging ("or equivalent") where the spec was prescriptive.
- **Remediation applied:** Per `PatchChecklist.md`, only T01.05 Notes (M1) and T01.04 acceptance criterion (L1) were patched. The HIGH DEV-001 fix is not represented in the included patch checklist — INFERENTIAL: the HIGH was likely fixed in the roadmap regeneration before tasklist generation, but the artifacts don't show the diff explicitly.
- **Outcome:** Catch worked. Remediation traceability is partial.
- **Still possible today (Auggie check):** YES — the spec-fidelity gate continues to fire on HIGH deviations.
- **Source artifacts:** `v2.24.5-SpecFidelity/spec-fidelity.md`, `v2.24.5-SpecFidelity/validation/PatchChecklist.md`.

### F-A4-019: unified-audit-gating-v2 spec-fidelity caught 2 HIGH spec-required deliverable omissions
- **Type:** SUCCESS
- **Pipeline step:** spec-fidelity
- **Symptom:** `unified-audit-gating-v2/spec-fidelity.md` DEV-001 caught a missing `test_timeout_at_100_turns` test (NFR-004 verification); DEV-002 caught a missing §3.4 title rename ("The 90% Reimbursement Rate" → "The 80% Reimbursement Rate"). `tasklist_ready: false`.
- **Root cause (claimed):** Roadmap underspecified Phase 4 deliverables — 6 tests instead of spec's 8; 2 of 3 spec-required edits but missed the section title.
- **Remediation applied:** Tasklist generation deferred until both HIGHs were fixed.
- **Outcome:** Gate worked as designed.
- **Still possible today (Auggie check):** YES — pattern of LLM omitting small but explicit spec deliverables is structural to LLM generation; gate catches it correctly.
- **Source artifacts:** `unified-audit-gating-v2/spec-fidelity.md`.

### F-A4-020: ID-namespace collisions surface as MEDIUM, not blocking — SC-NNN reused for safety constraints AND release criteria
- **Type:** FAILURE (gate severity calibration)
- **Pipeline step:** spec-fidelity
- **Symptom:** `unified-audit-gating-v2/spec-fidelity.md` DEV-003 documents that the spec uses `SC-001`-`SC-005` for safety constraints while the roadmap reuses `SC-001`-`SC-007` for "success criteria" — direct ID collision. Rated MEDIUM, not HIGH, so non-blocking.
- **Root cause (claimed):** LLM treated SC- prefix as available namespace, the LLM-generated fidelity checker did not weight namespace collisions as semantically critical.
- **Remediation applied:** Recommended rename to RC-001 (Release Criteria). Documented but did not block tasklist.
- **Outcome:** A real semantic error (ambiguous referent for "SC-001" across spec + roadmap) was downgraded by the gate. Future referential audits would see two definitions of SC-001.
- **Still possible today (Auggie check):** YES — `SPEC_FIDELITY_GATE` has no semantic check for ID namespace collisions; severity is left to the reflecting LLM.
- **Source artifacts:** `unified-audit-gating-v2/spec-fidelity.md` DEV-003.

### F-A4-021: Unified-audit-gating-v1.2.1 wiring-verification scanned 10 markdown files and emitted 0 findings — same false-negative
- **Type:** FAILURE (gate no-op)
- **Pipeline step:** wiring-verification
- **Symptom:** `unified-audit-gating-v1.2.1/wiring-verification.md` shows `target_dir: /config/workspace/IronClaude/.dev/releases/complete`, `files_analyzed: 10`, `total_findings: 0`. Same misconfiguration as F-A4-004 — directory pointer was wrong, gate emitted PASS.
- **Root cause (claimed):** Same as F-A4-004; pre-fix pipeline state.
- **Remediation applied:** Fixed in subsequent release (see F-A4-004 outcome).
- **Outcome:** Documents that this misconfiguration was reproducible across releases prior to the executor.py fix landing.
- **Still possible today (Auggie check):** NO — the 0-files-early-return is now in place (see F-A4-004).
- **Source artifacts:** `unified-audit-gating-v1.2.1/wiring-verification.md`.

### F-A4-022: Validate gate emits BLOCKING findings while parent pipeline completes successfully — semantics-level disconnect
- **Type:** FAILURE (structural disconnect)
- **Pipeline step:** validate
- **Symptom:** v3.05 validate-report shows `blocking_issues_count: 5`, `tasklist_ready: false`. The parent v3.05 release pipeline still completed and produced a tasklist-index.md. The validate step's BLOCKING verdict does not propagate to pipeline exit code or downstream halt logic.
- **Root cause (claimed):** F-A4-002 — design choice to warn rather than fail.
- **Remediation applied:** None.
- **Outcome:** Validate becomes advisory. Users who read the report act on it; users who do not read it consume potentially broken artifacts. Combined with F-A4-008's escalation policy, validate produces more findings than would propagate as enforcement.
- **Still possible today (Auggie check):** YES — confirmed via `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` semantic-check definitions; no exit-code propagation logic exists.
- **Source artifacts:** `v3.05_DeterministicFidelityGates/validate/validation-report.md`, `validate_gates.py:14-69`.

---

## Cross-cutting patterns within this partition

- **Pattern P1 — Gates with disabled enforcement paths (`gate=None`, "warn don't fail", or "blocking findings ≠ pipeline exit"):** Multiple gates were designed to surface issues without halting the pipeline. See F-A4-002 (validate warn-only), F-A4-003 (convergence `gate=None`), F-A4-022 (validate output disconnected from pipeline exit). Net effect: users see issues only if they read reports.
- **Pattern P2 — Gates that silently no-op because they target the wrong artifact:** F-A4-004 (wiring scanning `.dev/releases/complete/` instead of source) and F-A4-021 (same misconfiguration in v1.2.1) both produced PASS reports while doing zero useful work. The fix added a `files_analyzed > 0` guard which is now in place but was a missing invariant for multiple releases.
- **Pattern P3 — LLM-driven gates are non-deterministic across runs:** F-A4-005 (5 runs, 4 distinct verdicts, mid-loop regeneration) and F-A4-016 (5-vote aggregation as bypass) document that single-pass LLM fidelity checks are not reproducible. The structural deterministic-fidelity layer (F-A4-015) is the architectural response, but legacy LLM mode persists.
- **Pattern P4 — Single-direction checks pass while a complementary direction fails:** F-A4-009 (forward-trace pass + backward-trace fail), F-A4-006 (phantom-ID detection requires explicit spec-side lookup, gate did it loosely), F-A4-018 (caught wrong-path but only via prescriptive spec wording). Gates that don't enforce bidirectional or contrapositive coverage have systematic blind spots.
- **Pattern P5 — Gate fixes drift to spec edits when the spec is self-inconsistent:** F-A4-007 (Run 3 amended spec §5.6 to clear a HIGH). The fidelity gate's resolution surface is roadmap-only by design intent but expands to spec-mutation in practice when the spec is internally inconsistent. No mechanical block exists.
- **Pattern P6 — Recurrence-prevention layers are routinely skipped:** F-A4-013 documents that Wave 3 (T07 integration smoke test, T08 wiring fix, T11 E2E tests, T14 wiring regeneration) of the v3.05 gap-remediation tasklist were NOT EXECUTED while Wave 1+2 (the bug fixes themselves) shipped. Across this partition, gates are built but their reinforcing tests are deferred.

## Brittleness drivers identified

- **D1 — No top-level invariant that "gates must enforce, not advise":** The framework allows `gate=None` and allows gate output to be non-blocking in pipeline-exit semantics. There is no schema constraint at the executor level forcing every step to have a non-None gate or forcing gate failure to propagate. (Drives F-A4-002, F-A4-003, F-A4-022.)
- **D2 — No structural guard at the `GateCriteria` level that the gate ran against valid input:** Until the wiring fix landed, a gate could PASS with `files_analyzed=0` because nothing required the gate to assert a minimal-work invariant before emitting PASS. The fix was specific to wiring; the general principle ("each gate must declare and verify a precondition that proves it actually inspected its target") is not codified. (Drives F-A4-004, F-A4-021.)
- **D3 — Gate severity classification lives in the LLM prompt, not the gate code:** Severities (HIGH/MEDIUM/LOW, BLOCKING/WARNING/INFO) are LLM-determined. Even when a finding is structurally identical to a known-blocking class (e.g., ID-namespace collision in F-A4-020), the LLM may rate it MEDIUM and the gate has no override. The framework lacks a "severity escalation rule registry" tied to deterministic signals. (Drives F-A4-020, F-A4-005's vote noise.)
- **D4 — No registry-level contract that all roadmap-output files must agree on a closed identifier set:** Roadmap can introduce FR-NNN/NFR-NNN/SC-NNN/OQ-NNN identifiers not present in the spec without any deterministic gate check that the introduced IDs are spec-derived. The spec-fidelity gate detects this only via LLM reading, which is fallible (F-A4-006). The structural-checker layer addresses requirement-side coverage but not ID-creation auditability. (Drives F-A4-006, F-A4-020, F-A4-004's OQ dangling.)
- **D5 — Pipeline cannot validate its own wiring when the spec-under-test mutates the pipeline itself:** A self-referential bootstrap problem (F-A4-014): when the release being shipped modifies the spec-fidelity step, the spec-fidelity step is both validator and validatee. The framework has no "external smoke test that imports and calls each new wiring path" gate. (Drives F-A4-013, F-A4-014.)
- **D6 — Adversarial mode is the only structural counter to LLM blind spots, but it is opt-in:** Multi-agent reflect+merge (F-A4-008, F-A4-009) caught classes of failure single-agent mode would have missed. Single-agent mode is the default for standalone `roadmap validate`; multi-agent is only enabled when `--agents` lists 2+. There is no soft-enforcement that high-risk gates require adversarial validation. (Drives F-A4-009.)
- **D7 — Fail-open as a default risk-mitigation pattern:** F-A4-012 documents `fidelity_checker.py` marking ambiguous FRs as `found=True` to avoid false-positives. This is a defensible local choice but compounds across the gate set: when many checks fail open, the aggregate gate behavior is "absence of evidence is taken as evidence of absence" — exactly the false-negative pattern this retrospective surfaces repeatedly.

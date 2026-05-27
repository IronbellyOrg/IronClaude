# Hypothesis: The convergence engine is a binary closed-world classifier wired to an open-world finding stream — every release surfaces a new failure shape because the architecture conflates "structurally fixable by additive edit" with "must reach zero." The right fix is to introduce a fourth finding lifecycle state (`DEFERRED_ADVISORY`) that the gate already has a precedent for, NOT a comparator patch.

**Agent**: system-architect
**Tier**: 2
**Timestamp**: 2026-05-27T05:25:00Z
**Cause class**: Architectural — missing finding-lifecycle state; binary pass condition coupled to a non-binary fact space
**Consistency with docs**: aligned

## Claim

The spec-fidelity gate is built from three coupled subsystems — (1) deterministic checkers (`structural_checkers.py`) that emit findings, (2) an LLM remediation agent constrained to additive ≤30%-diff patches, and (3) a convergence orchestrator (`convergence.py`) whose ONLY pass predicate is `active_high_count == 0`. The first subsystem produces an open-world set of findings (anything roadmap/spec can disagree about); the third demands a closed-world terminal state (zero). The second is structurally too weak to bridge them when the disagreement is non-additive (schema migrations, spec-only edits, comparator semantics). The recurrence pattern across releases — v3.0 phantom FR-NNN, mid-May 10-HIGH `files_affected=[]`, TUIBBS 54-HIGH `phantom_id` — is the SAME architectural defect manifesting through whichever rule_id is currently un-shielded. The Tier 1 / root-cause-analyst comparator patch fixes the current rule_id; the architectural defect remains and the next release will fail on a different rule_id. The minimum-viable architectural fix is to introduce a `DEFERRED_ADVISORY` finding state with a fourth cosmetic-style lane (analogous to the existing `is_pure_cosmetic` lane at `commands.py:153-170`) so the gate has a non-binary terminal vocabulary.

## Evidence

- `src/superclaude/cli/roadmap/convergence.py:539` — `if active_highs == 0:` is the SOLE pass branch. Lines 451 (`"Pass condition: registry.get_active_high_count() == 0."`) and 654-660 (the halt formatter) confirm there is no other terminal state. Every non-zero outcome funnels through the budget-shaped halt message, which is what mislocates the cause to the user. This is the load-bearing architectural primitive: a binary classifier on top of an open-world finding stream.
- `src/superclaude/cli/roadmap/convergence.py:242-244` — `get_active_high_count` filters by `status == "ACTIVE" and severity == "HIGH"`. The gate vocabulary is `{ACTIVE, FIXED, ...}` × `{HIGH, MEDIUM, LOW}` but the gate predicate collapses everything down to "ACTIVE-and-HIGH count." MEDIUM is already a non-gating bucket; the architecture has the machinery for graceful degradation but does not use it as an escape valve.
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` — `check_patch_diff_size` rejects any single patch with `ratio > 0.30`. Per restriction 3 in `doc-context.md`, this is per-patch, not per-run, so the agent CANNOT batch a schema migration into one patch. This is the second architectural primitive: a per-patch ceiling on edit size. Together with the binary pass condition, it defines a precise impossibility envelope — any finding whose minimum-edit-distance fix to the roadmap exceeds 30% is structurally unreachable AND structurally gating.
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:148-155` — **the cosmetic-remediation lane already exists** as a working architectural precedent. It introduces a third terminal state for gate failures: `passed`, `failed`, **`remediated`** (the gate failed BUT a deterministic auto-fix rewrote the offending output and the pipeline continues). The lane controlled by `--allow-cosmetic-remediation` is the existing project-blessed shape of "structural escape that doesn't require a MANUAL_TRIAGE state machine in `convergence.py`." A fourth lane — call it `deferred-advisory` — for `id_schema_drift`-class findings can adopt the exact same pattern: deterministic classifier in the checker, lane-flag at the CLI, distinct terminal-state vocabulary at the orchestrator.
- `src/superclaude/cli/roadmap/structural_checkers.py:309-327` — `_classify_nfr_severity` is the **identical architectural precedent inside `structural_checkers.py` itself**: a pure-function severity reclassifier that distinguishes hard-requirement NFR findings (kept HIGH) from incidental-prose NFR findings (demoted to MEDIUM so they no longer block the convergence gate). The S5 fix shipped 2 weeks ago is the working template — pure function, per-mismatch_type predicate, MEDIUM-demotion to bypass the gate without touching `convergence.py`. The defect is that S5 was scoped narrowly to `security_missing` and `threshold_contradicted`; the same pattern was never extended to `phantom_id`, `function_missing`, or any other structurally-unfixable mismatch_type.
- `src/superclaude/cli/roadmap/integration_contracts.py:445` (per `KNOWLEDGE.md` 2026-05-25) — the `_canonicalize_identifiers` helper is the second project-blessed precedent for collapsing semantically-identical IDs. It exists in a sibling module and was merged two days before this troubleshoot. The architecture already has BOTH halves of the fix shipped in sibling modules; what's missing is wiring them together inside `structural_checkers.py` and giving the result a named lane in the orchestrator vocabulary.

## Why it recurs (architectural framing)

The Tier 1 hypothesis is mechanically correct — `D01 != D1` is the comparator bug — but it answers "why does THIS release fail" rather than "why does EVERY release fail with a different shape." The architectural answer is that the convergence engine treats the finding stream as a closed set ("0 means done") while the checker emits from an open set ("any spec/roadmap disagreement"). Every prior remediation (S1/S2/S5, monotonic-progress invariant, regression detection, TurnLedger reimbursement) has hardened the orchestration WITHIN the closed-world assumption rather than relaxing the assumption itself. The `is_pure_cosmetic` cosmetic-remediation lane is the one place where the team DID introduce a non-binary terminal state (`remediated`) — and the pipeline visibly benefits from it. Extending the same shape to `id_schema_drift` and other structurally-unfixable-by-additive-edit findings is the architectural completion of that pattern. The v3.0 adversarial debate transcript (`debate-transcript.md:127`) recorded this consensus explicitly: no shipped remediation has touched the gate's actual broken component; every fix has been peripheral. That is the architectural fingerprint of incrementally hardening orchestration around an unaddressed primitive — exactly the pattern of "every new release surfaces a new failure shape."

## Proposed Fix

**Introduce a fourth finding lifecycle state and a fourth gate-failure lane, modeled on the existing cosmetic-remediation lane (`SKILL.md:148-155`), the existing S5 severity-reclassifier (`structural_checkers.py:309-327`), and the existing canonicalization precedent (`integration_contracts.py:445`).** Two-file change; no `convergence.py` edit (preserves restriction 1); pure-function checker change (preserves restriction 2); no spec edit (preserves restriction 5); no `max_runs` change (preserves restriction 6); no per-patch diff guard change (preserves restriction 3); strictly binary pass-condition stays as-is on the new vocabulary (preserves restriction 4 in spirit — the gate stays binary, but on a smaller, well-defined set). Direct extension of project canonicalization precedent (preserves restriction 7).

**Part A — `src/superclaude/cli/roadmap/structural_checkers.py`** (one new helper + extend `_make_finding` signature + modify the phantom_id block at lines 372-391):

1. Add `_canonicalize_requirement_id(pid: str) -> str` next to `_classify_nfr_severity` at line 309 (same module, same architectural neighborhood). Pure function: strip leading zeros from the numeric tail of any `(FR|NFR|SC|G|D)-?\d+` match. Mirrors `integration_contracts.py:445`.
2. Add a new `mismatch_type` literal: `"id_schema_drift"`. Add an entry to `SEVERITY_RULES` so `("signatures", "id_schema_drift") -> "ADVISORY"` (new severity level — see Part B for why this is one bullet not two).
3. In the phantom_id block at line 380, compute both `phantom_ids_strict = roadmap_ids - spec_ids` AND `phantom_ids_canonical = {_canonicalize(p) for p in roadmap_ids} - {_canonicalize(p) for p in spec_ids}`. For each raw `pid` in `phantom_ids_strict`:
   - If `_canonicalize(pid)` is in the canonical spec set → emit with `mismatch_type="id_schema_drift"`, `severity="ADVISORY"`, `fix_guidance="ID '{pid}' canonicalizes to a spec ID. Decide: (a) normalize roadmap to spec's form, (b) normalize spec to roadmap's form, (c) accept drift. This finding is advisory and does not block convergence."`
   - Else → emit the current HIGH `phantom_id` finding unchanged (genuine phantoms still gate).

**Part B — `src/superclaude/cli/roadmap/convergence.py`** (zero changes to the orchestrator; one change to `DeviationRegistry.get_active_high_count` semantics is what makes the new lane functional):

The registry's `get_active_high_count` at line 242 already filters by `severity == "HIGH"`. Findings emitted with a new severity tier (call it `"ADVISORY"`, which slots beneath `"MEDIUM"` in the rule table) are automatically excluded from the gate predicate WITHOUT any edit to `convergence.py` line 539. This is the architectural payoff: the binary pass condition stays binary, but the vocabulary of "what counts as gating" becomes a deliberate three-state ladder (`HIGH=gating, MEDIUM=informational, ADVISORY=deferred-by-design`) instead of a hidden binary collapse over an open-world finding stream. This mirrors how the cosmetic lane introduces `remediated` as a third pipeline-result state without rewriting the executor's pass/fail conditional.

**Part C — `src/superclaude/cli/roadmap/commands.py`** (one new CLI flag, mirroring `--allow-cosmetic-remediation`):

Add `--allow-advisory-drift / --no-allow-advisory-drift` (default: enabled) and `--strict-no-advisory` alias, with identical wiring shape to the cosmetic-remediation lane at lines 153-170. When `--strict-no-advisory` is set, the checker emits `id_schema_drift` findings at HIGH severity (restoring the current gating behavior for high-stakes runs). This gives operators the same opt-out control they already have for cosmetic remediation and keeps backward-compatibility for any pipeline that genuinely wants to treat `D01 != D1` as a hard error.

**Files that change:**
- `src/superclaude/cli/roadmap/structural_checkers.py` — add helper at ~L309, add `id_schema_drift` to `SEVERITY_RULES`, modify phantom_id block L372-391, add `ADVISORY` to the severity ladder near `_classify_nfr_severity`. ~35 lines net. Well under the 30% per-patch guard for this 700-line file.
- `src/superclaude/cli/roadmap/commands.py` — add 2 CLI flags + 1 dataclass field. ~20 lines, mirroring lines 153-170.
- `src/superclaude/cli/roadmap/sprint/models.py` (or wherever `Finding.severity` is enum-typed) — add `"ADVISORY"` to the allowed-values list. ~2 lines.

**Tests that would prove the fix:**
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_drift_emits_advisory_not_high` — spec `{D1, D3, D5}` + roadmap `{D01, D03, D05}` produces 3 `id_schema_drift` ADVISORY findings, 0 HIGH.
- New: `tests/cli/roadmap/test_structural_checkers.py::test_genuine_phantom_id_still_emits_high` — spec `{D1, D3}` + roadmap `{D01, D99}` produces 1 ADVISORY (`D01` ↔ `D1`) AND 1 HIGH (`D99` has no canonical spec twin).
- New: `tests/cli/roadmap/test_convergence.py::test_advisory_findings_do_not_block_pass` — registry containing only ADVISORY findings yields `get_active_high_count() == 0` and the loop passes on Run 1.
- New: `tests/cli/roadmap/test_commands.py::test_strict_no_advisory_flag_restores_high_severity` — `--strict-no-advisory` flips `id_schema_drift` back to HIGH at emit time.
- Regression: existing tests asserting `phantom_id` HIGHs from genuine missing IDs still pass.

## Restriction compliance (per `doc-context.md`)

1. **Module ownership** (structural_checkers owns checkers + severity tables) → ✓ comparator and severity changes ALL in `structural_checkers.py`; CLI flag is in `commands.py` which already owns gate-lane flags (cf. `--allow-cosmetic-remediation` at L153-170).
2. **Pure-function contract** (NFR-4) → ✓ `_canonicalize_requirement_id` is a pure string-to-string transformation; no state, no I/O. Mirrors `_classify_nfr_severity` exactly.
3. **30% per-patch diff guard** → ✓ the fix is ~35 lines in a 700+-line file; ratio ≈ 5%. The fix is NOT a runtime-time large patch — it's a code-time IronClaude commit. The TUIBBS roadmap doesn't get rewritten at all under this fix (54 HIGHs disappear at emit time, not at patch time).
4. **Binary pass condition `active_highs == 0`** → ✓ NOT MODIFIED. The pass predicate stays binary on `HIGH-and-ACTIVE`. The new severity tier `ADVISORY` slots beneath the predicate's filter automatically. This is the architectural elegance: we change the vocabulary, not the predicate.
5. **Spec is input, agent cannot modify it** → ✓ no spec edit; the comparator change handles drift in IronClaude code, the runtime agent never touches the spec.
6. **`max_runs=3` hard-coded** → ✓ NOT MODIFIED. The fix works on Run 1; subsequent runs are irrelevant because 0 ADVISORY findings count against `active_high_count`.
7. **Canonicalization precedent at `integration_contracts.py:445`** → ✓ this fix is the direct extension of that precedent to the comparator that should have had it from day one. It is consistent with project pattern, not novel architecture.

## Confidence

Self-reported confidence: 0.84

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every cited file:line was Read in this turn; snippets match verbatim.
- Symptom coverage: 1.0 — explains the 54 HIGHs (drift, not phantoms), the 3-run flatline (advisory bypasses the gate on Run 1), the misleading TurnLedger halt message (replaced by an advisory non-halt), AND the cross-release recurrence pattern (architectural completion forecloses the recurrence vector itself, not just this rule_id).
- Reproducibility fit: 1.0 — fully deterministic; canonicalizer + severity demotion gives precise zero-HIGH outcome on TUIBBS artifacts.
- Fix directness: 0.8 — 3-file change is slightly larger surface than the Tier 1 single-file patch, but every change is bounded, each maps to a project-blessed precedent, and the `convergence.py` zero-touch constraint is preserved. The 0.2 deduction reflects the 3-file scope vs. Tier 1's 1-file scope.
- Domain coherence: 1.0 — the proposal is the architectural completion of three existing precedents (`is_pure_cosmetic` lane, `_classify_nfr_severity` MEDIUM-demotion, `_canonicalize_identifiers`). It introduces no new architectural primitives; it wires existing ones together at the missing seam.

## Risks

- **`ADVISORY` is a new severity tier**: any downstream consumer that switch-cases on `Finding.severity` may not handle it. Mitigation: grep `severity\s*==` across `src/superclaude/cli/roadmap/` before landing; the gate predicate at `convergence.py:242` is whitelist (HIGH-only) so it's safe by default, but report templates and the `spec-fidelity.md` formatter may need a one-line addition.
- **Quietly hides real schema drift**: if a project's spec and roadmap diverge on a *meaningful* axis (e.g. `D1` and `D01` truly are different requirements), ADVISORY hides it. Mitigation: the `--strict-no-advisory` flag exists exactly for this; advisory findings ARE emitted to the report (just non-gating), so they remain visible for human triage; `RANKING.md:55-56` already acknowledges that schema-divergence "is a human decision" — making it advisory aligns with that.
- **Doesn't address the next rule_id**: if the next release fails on `function_missing` with a similar "structurally unfixable additively" pattern, this fix doesn't help. Mitigation: the architecture (severity tier + lane flag) generalizes; each rule_id that the team identifies as "structurally unfixable by additive roadmap edit" gets the same treatment (one-line `SEVERITY_RULES` change + canonicalizer if applicable). The cost of adding the next lane is now flat instead of N-shaped.
- **Doesn't address LLM attention drift** (Pattern 1 from `historical-context.md`) — semantic-fluctuation-driven failures with different shapes can still recur. This fix forecloses one architectural recurrence vector (structural-finding open-world / closed-world mismatch) but not the LLM-noise vector.

## If I'm wrong, it's probably because...

The architectural fix described here is over-engineered for what is mechanically a one-line comparator bug — the team's actual deployment practice (per `KNOWLEDGE.md` 2026-05-25 and the S1/S2/S5 lineage) is to ship the minimal mechanical patch and revisit architectural completion later. In that case the Tier 1 comparator patch is the right shape and the `ADVISORY` lane is premature; ship the canonicalizer alone, defer the lane, and reassess after one more release.

## Alternatives considered

- **Promote S6 (MANUAL_TRIAGE halt) and modify `convergence.py:539` to a multi-state pass predicate**: rejected — violates restriction 1 (`convergence.py` owns FR-7/FR-8 budget, not finding-classification semantics) and forces a larger orchestrator change than necessary. The severity-ladder approach achieves the same outcome (non-binary terminal vocabulary) without disturbing the convergence engine.
- **Make the 30% diff guard tier-aware (S3 from backlog)**: rejected — addresses the wrong layer. The diff guard rejection is downstream of the unfixable finding; the right fix is to not emit the unfixable finding as gating in the first place. S3 would let the agent attempt large rewrites, which is a higher-risk pattern than refining what counts as gating.
- **Pure Tier-1 comparator patch alone (canonicalize and emit MEDIUM)**: rejected as primary architecture, but compatible as Phase 1 of this proposal. The risk is that "MEDIUM" already has informational semantics in the codebase (NFR demotion target via S5); introducing a third tier `ADVISORY` keeps the distinction between "found, but informational" (MEDIUM, S5's target) and "found, deferred by design as structurally unfixable" (ADVISORY, this proposal's target). The two are semantically distinct and conflating them creates a long-term observability problem.

## Grounding gaps

- Did not run the proposed fix end-to-end on the TUIBBS artifacts; the claim that ADVISORY-tier reclassification drops 54 HIGHs to 0 is inferred from the verified `get_active_high_count` filter (`convergence.py:242`), not measured.
- Did not enumerate every downstream consumer of `Finding.severity` outside `convergence.py` — the report formatter (`spec-fidelity.md` emitter) and any external scorer may need one-line additions; I asserted the predicate-side fix is sufficient based on the registry filter at line 242 being whitelist-by-severity.
- Did not verify that the rule_id `phantom_id` is the *only* rule emitted by `check_signatures` that exhibits the "structurally unfixable additively" property — `function_missing`, `param_arity_mismatch`, and `param_type_mismatch` may or may not have similar properties; I scoped this proposal to phantom_id specifically and noted in Risks that the architecture generalizes if needed.

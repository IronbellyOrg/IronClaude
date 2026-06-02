# R1.1 Proceed Decision

**Phase:** 6 (R1.1 — extend `superclaude.contracts` with `RETURN_CONTRACTS` + threshold registry)
**Phase Gate:** PG6.2 (act on R1.1 QA verdict)
**Branch:** `refactor/roadmap-pipeline-r0-r1-rewrite`
**Parent commit:** `1c56b50f` (R0 closure)
**Generated:** Phase Gate PG6.2 (2026-06-01).

---

## Decision: PROCEED to Phase 7 (R1.2 — PipelineEnvelope)

R1.1 closes clean. All 6 mandatory verification checks PASS per `phase-outputs/reviews/r1-1-rf-qa-task-integrity.md`. 163/163 tests pass with zero regressions. lint-architecture clean (0 errors). PRESERVE invariants verified intact (empty diff for commands.py / structural_checkers.py / convergence.py / cosmetic_remediator.py vs `1c56b50f`). Zero new `return True` stubs. Zero fix-cycles required.

---

## Closure status

| Item | Status |
|---|---|
| Step 6.1 — RETURN_CONTRACTS scope discovery | COMPLETE — `return-contracts-scope.md` |
| Step 6.2 — extend `contracts/__init__.py` | COMPLETE — `+AdversarialReturn, +UnaddressedInvariant, +RETURN_CONTRACTS, +THRESHOLDS` |
| Step 6.3 — migrate 4 R1.1 consumers + arch-lint Rule 3 | COMPLETE |
| Step 6.4 — extend tests, run validation | COMPLETE — 163/163 PASS, lint-arch clean, ruff clean |
| PG6.1 — aggregate + rf-qa task-integrity | COMPLETE — verdict PASS (0 fixes, 0 cycles) |
| PG6.2 — act on verdict (this artifact) | COMPLETE — proceed authorized |

---

## Acceptance gate (BUILD-REQUEST §R1.1)

R1.1 satisfies BUILD-REQUEST §R1.1 + §MVR §5 + §Contract items #5/#8 fully:

- ✅ `superclaude.contracts` extends with `RETURN_CONTRACTS` (per §MVR §5 example `RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}`).
- ✅ Full threshold registry (`THRESHOLDS` covering fingerprint min_coverage_ratio + structural_audit threshold).
- ✅ arch-lint Check 11 extends to the new constants (auto-discovers via `__all__`) AND gains a new Rule 3 for dataclass shadowing detection.
- ✅ Consumer migrations executed for all behavioral R1.1-scope sites (4 sites: fingerprint x2, spec_structural_audit, gates.py:375, fidelity_checker).

---

## Outstanding R1.1 follow-ups (deferred)

Per `return-contracts-scope.md §I`, R1.1 explicitly defers (not regressions):

1. **`gates.py:363, 365, 1481`** — docstring + failure_message prose containing `"0.7"`. Display strings, not behavioral. Leave-as-is per Phase 4 §F note; arch-lint does not flag float literals so no `arch-lint: allow-duplicate` marker is required.
2. **`prompts.py:896, 922`** — LLM-prompt text describing the frontmatter shape. NOT migrated to `RETURN_CONTRACTS` per `return-contracts-scope.md §I` — coupling LLM-side prompt text to consumer-side typing would over-couple. Phase 11 (R1.6) may revisit.
3. **`gates.py:380-388, 1253-1266`** — frontmatter parsing of `convergence_score`/`base_variant`. NOT migrated; consumers parse YAML, not `AdversarialReturn` instances. R1.2 envelope work may introduce a typed bridge.

These are documented forward-looking deferrals, not technical debt.

---

## Open Questions logged by rf-qa (non-blocking)

1. **OQ-1:** `test_adversarial_return_fields_match_skill_prose` uses set equality on field names — catches missing/extra fields but not type drift. Future hardening (compare types via `dataclasses.fields(...).type` or skip — not a R1.1 blocker).
2. **OQ-2:** `tuple` vs `list` serialization is a future consumer concern; no in-tree YAML round-trip consumer of `AdversarialReturn` exists yet.

Logged in this proceed-decision rather than fix-now; will be revisited in R1.2/R1.3 when envelope/consumer integration lands.

---

## Phase 4 inventory delta (D3) recorded

`cli/roadmap/gates.py:375` behavioral threshold migration was discovered during Phase 6 Step 6.1 and migrated in Step 6.3. Documented in:

- `return-contracts-scope.md §F`
- `r1-1-aggregation.md §H`
- `r1-1-rf-qa-task-integrity.md §Items Reviewed row b`

The original R0 acceptance report is unaffected (the gate predicate was never claimed cleaned in R0).

---

## Next-phase entry

Phase 7 (R1.2 — `PipelineEnvelope` dataclass + sidecar JSON + dual-write migration) is unblocked. Per BUILD-REQUEST §R1.2 + §MVR §1 + master:§Flaw 3:

- New module: `src/superclaude/cli/roadmap/envelope.py`
- New dataclass: `PipelineEnvelope` (release_id, spec_hash, spec_ids, artifacts, findings, counts, convergence, accepted_deviations)
- Dual-write migration strategy: envelope.json + existing markdown for 1 release cycle, then R1.6 deletes markdown-as-substrate
- Per-step Python post-extractors replace LLM-written counts (master:§Flaw 3 substrate-inversion)

Phase 7 task entries: Steps 7.1-7.4 + PG7.1/PG7.2 per `TASK-RF-20260531-042405.md:472-500`.

**HALT for user confirmation before launching Phase 7** per the session-pacing rule.

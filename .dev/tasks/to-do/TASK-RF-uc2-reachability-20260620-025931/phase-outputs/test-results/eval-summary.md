# Eval Summary — FR-RSR UC-2 Reachability

status: PARTIAL — 2 of 5 with_skill cases pass (headline + degraded-backend); 3 cases + old-baseline reveal real gaps. FR-RSR.10 NOT yet satisfied.

## Full grader result (iteration fr-rsr-uc2, all runs executed against the EDITED 1.6.0 skill)

| Eval | with_skill | old_skill | Verdict |
|------|-----------|-----------|---------|
| uc2-unwired-surface-passes (37) | 3/3 ✓ | 0/1 ✗ | with_skill PASS; old baseline contaminated |
| uc2-surface-degraded-backend (40) | 4/4 ✓ | — | PASS |
| uc2-surface-positive-control (38) | 1/3 ✗ | — | contract-field fidelity gap |
| uc2-surface-dynamic-dispatch (39) | 0/3 ✗ | — | spec-vs-model divergence + weak fixture |
| uc2-surface-test-only-ref (41) | 1/3 ✗ | — | model inconsistency |

## Validated working (core FR-RSR)

- **Headline (37) with_skill 3/3**: unwired `/ai` Spawn surface → `runtime_surface_unreached: 1`,
  full `runtime-surface-ledger.yaml` (symbol classified unreached/regression/HIGH, real
  evidence: zero production importers, only importer is the test), Tier 2, status partial,
  promotion BLOCKED. The motivating blind spot is genuinely closed.
- **degraded-backend (40) 4/4**: `backend: none` → Grounding Gap, no STOP, no clean-pass.
  Fail-loud doctrine works.

## Findings (the eval did its job)

1. **Contract-emission fidelity is unreliable (REAL, needs SKILL.md fix).** On the
   REACHED / DEGRADE paths the model emits ad-hoc field names — `runtime_surface_reachable: true`,
   `reachability_path: ...`, `static_caller_absent_is_expected: true` — instead of the six
   spec-mandated fields (`runtime_surface_unreached`, `runtime_surface_degraded`,
   `unreached_surfaces`, ...). positive-control (38) and test-only-ref (41) fail on
   `runtime_surface_unreached`/`unreached_surfaces` being absent/empty even though the prose
   verdict is right. The §9.1 additions read as descriptive, not forcing; the LLM only fully
   populates them on the "interesting" UNREACHED path (headline).

2. **`[project.scripts]` DEGRADE rule contested by the model (DESIGN question).** On
   dynamic-dispatch (39) the model traced `ai-spawn -> ai_entry:main -> run_spawn_entrypoint`
   and concluded **REACHED**, not DEGRADE, with `regression: 0`. The NFR-RSR.3 *safety*
   property (no false Regression on idiomatic wiring) HOLDS — but the spec's prescribed
   DEGRADE+Grounding-Gap shape was not emitted. Two contributing causes: (a) the fixture's
   dispatch is statically traceable (main() calls the helper in the same file), so it isn't a
   genuinely *un*-traceable dynamic case; (b) the degrade-oracle instruction isn't forcing
   enough to override the model's own reachability judgment.

3. **Model inconsistency across near-identical inputs (RELIABILITY).** test-only-ref (41) is
   structurally the headline scenario (surface referenced only from tests) but the model
   emitted `unreached=0` + Drift instead of `unreached=1` + Regression. LLM execution is
   non-deterministic on the classification boundary.

4. **Old-baseline contamination (HARNESS BUG).** The headline `old_skill` run used
   `--append-system-prompt reflect-v1.md` but cwd=fixture still had the `.claude` symlink to
   the 1.6.0 skill, which auto-activated — the old REPORT.md is full of "runtime surface" /
   "reachability" / "fr-rsr", impossible from the 111-line v1. The FAIL-pre baseline is
   therefore invalid (contaminated, not a true v1 run). FIX: do NOT symlink `.claude` for the
   old_skill run.

## Legitimate next actions (NOT assertion-gaming)

- **Harness:** drop the `.claude` symlink for old_skill runs so the v1 baseline is faithful.
- **Fixture:** make dynamic-dispatch genuinely untraceable (registry/string-dispatch lookup,
  not a same-file call) so REACHED-vs-DEGRADE actually tests the oracle.
- **SKILL.md (real implementation rework):** strengthen §9.1 / §6.1 so the six runtime_surface_*
  fields are MANDATORY with EXACT names on EVERY UC-2 surface path (reachable, degrade,
  unreached), with a worked contract example — so the model stops improvising field names.
- **Open design question for the user:** is `[project.scripts]` REACHED (model's view, safety
  holds) or DEGRADE (spec-as-written)? This decides whether fixture 39 or the spec changes.

## Artifacts

All runs under `.dev/eval-workspaces/sc-reflect/iterations/fr-rsr-uc2/eval-uc2-*/`
(with_skill/outputs/{REPORT.md,contract.yaml,artifacts/}, grading.json). Producer:
`.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/phase-outputs/plans/produce_iteration.py`.

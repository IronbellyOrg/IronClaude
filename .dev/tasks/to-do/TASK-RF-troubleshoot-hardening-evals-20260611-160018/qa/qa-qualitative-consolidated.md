# Consolidated Qualitative Findings (A.10.5)

Sources: qa-qualitative-operational-report.md (FAIL — 2 IMPORTANT + 2 MINOR), qa-qualitative-sufficiency-report.md (FAIL — 1 MINOR; all gates verified ≥7 agents, I20/M3/M4 correct, no gate under-strength).

## Gate sufficiency: CONFIRMED STRONG (no fixes needed there)
Per-phase gates + final 6.2 = 10 agents each (7 lens report-only + 1 fix + 2 verify); M4 fidelity gate 6.3 well-formed; POST reflect 6.4 self-run/penultimate. I20 satisfied (exactly one fix agent per gate). No gate under-strength → no CRITICAL.

## FIXES TO APPLY (serialized, single fix agent)

### FIX-1 (IMPORTANT, operational #1) — Fabricated `evalIdString` citation in Step 3.4 (+ any echo in 3.2/3.5)
Problem: `src/superclaude/cli/eval/schemas/summary.schema.json` has NO `evalIdString` `$def` and no `pattern` key (only a prose note ~line 165). The task tells the executor to "reuse the `evalIdString` regex" — the executor will grep for it, fail, and stall/fabricate.
Fix: In Step 3.4 (schema item), declare the escape-id regex as the NEW schema's OWN `$defs.escapeId.pattern` with the literal regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (or a simpler escape-id pattern like `^E[0-9]+$` which is sufficient for E1..E5 — choose the simpler `^E[0-9]+$` since escape_ids are exactly E1..E5), and DROP the "reuse evalIdString from summary.schema.json" provenance claim. Update any echo in Step 3.2 (model) / Step 3.5 (schema-fidelity test) so they reference the new schema's own `$defs.escapeId`, not `evalIdString`.

### FIX-2 (IMPORTANT, operational #2) — E1/E4 OLD callables are bound METHODS, not module functions
Problem: E1 `_build_file_args` (@94d5baa0, in cli/prd/process.py) and E4 `_evaluate_gate` (@1b0264f1, in cli/prd/executor.py) are bound methods on a class; E2 `_check_parallel_instructions` (cli/prd/gates.py) and E3 `gate_passed` (cli/pipeline/gates.py) are module-level functions. The OLD=MISS items say "invoke the real pre-fix callable in-process" without specifying how E1/E4 obtain a class instance — a naive import-and-call raises.
Fix: In the E1 OLD=MISS runner (Step 4.3) and the E4 OLD=MISS runner (Step 4.6) — and the git-replay/ReplayExecutor item (~Step 3.1) if it defines the generic in-process-invocation contract — add explicit guidance: for the two METHOD callables, the test must construct/obtain the owning class instance at the pre-fix-parent checkout (instantiate the class with minimal/stub constructor args, or invoke via the unbound function with a constructed/SimpleNamespace `self`) before calling; for the E2/E3 MODULE-LEVEL functions, direct import-and-call is fine. Add a one-line note per the two method items naming the owning class so the executor knows what to instantiate. Keep it advisory (the executor reads the actual pre-fix signature) — do NOT hardcode a signature the parent may not have; instruct the executor to read the parent-tree signature first.

### FIX-3 (MINOR, operational #3) — `_pollution_snapshot` citation off-by-one in Step 5.1
Fix: change the cited line range (30-93) to the actual `def _pollution_snapshot` at `tests/conftest.py:29` (keep the behavioral claim; just correct the line).

### FIX-4 (MINOR, operational #4) — E2/E3 shared H3 ref clarity
Fix: In the E2 and E3 runner items (Steps for E2/E3), add a one-line inline clarifying comment that E2 and E3 both map to wave H3 and both proxy the `unmask-and-sweep.md` ref but assert DISTINCT facets (E2 = word-boundary `complete`⊄`incomplete` classifier; E3 = sibling-heading unmask/sweep `K_swept==K_true` + WARN/CONTINUE). Low-risk one-liner; do not restructure.

### FIX-5 (MINOR, sufficiency) — L124 Key Constraints "3 agents" inert contradiction
Problem: the `## Execution Context` Key Constraints (~L124) says "intermediate/phase gates = 3 agents", which contradicts the MDTM 5-agent intermediate minimum / the 7-agent phase gates actually encoded. It is inert (no intermediate gates exist; all phase gates are 7) but could mislead a downstream copier.
Fix: reword to match reality, e.g. "phase QA gates use 7 lens agents (3 rf-qa + 4 rf-qa-qualitative) per the standard PER_PHASE band; no intermediate research/synthesis gates are encoded." ~1 line, no structural change.

## CONSTRAINTS for the fix agent
- Surgical Edits only; preserve all verified-clean content (G1 no-caret parent SHAs, E4 1b0264f1 pin, skipif/no-xfail, collision boundary, parents[3], the anti-vacuity backtest_status derivation just added, the SELF-RUN POST-reflect form).
- Do NOT weaken any QA gate (all are correctly ≥7 agents). Do NOT introduce `^` on a parent sha. Do NOT convert POST-reflect to a human-handoff.

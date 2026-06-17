# Adversarial Debate Transcript (standard depth)

Three variants debated across the seed brief's open questions. Positions paraphrased; resolutions
are the merge decisions carried into `merged-requirements.md`.

## Q1 — Deterministic shell-probe vs bounded LLM protocol-trace; how to make 3× runs agree?

- **A (qa):** Reduce EVERY acceptance criterion to a captured shell exit code; LLM only authors prose
  and confirms a `diff`-backed byte-match. A green run is then forced-reproducible.
- **B (analyzer):** Agreement at the verdict level is too weak — two runs can both say PASS for
  different observed reasons. Gate on a **normalized observation digest**: strip volatile fields
  (timestamps, run_id, durations), canonicalize (sort keys/lists, `LC_ALL=C`, `--sort path`), sha256
  it; the 3 digests per test MUST be identical or the test is `DISAGREE` → suite FAIL.
- **C (devops):** Run deterministic probes first; anchor any LLM trace to the probe output; add a
  per-run timeout + fail-fast so a hung run can't silently skew the suite.
- **RESOLUTION:** Adopt B's observation-digest as the reproducibility gate (strongest), A's exit-code
  reduction for the criteria themselves, C's deterministic-first ordering + timeout/fail-fast.
  Classify each criterion DETERMINISTIC vs JUDGMENT (B) and drive judgment criteria toward zero.

## Q2 — Is the (A) residual / (B) contract / (C) chain / (D) safety decomposition right?

- **All three independently chose exactly this decomposition.** No debate needed — it is the natural
  partition of the migration's 4 desired-outcome dimensions with clean boundaries.
- **Boundary tension:** the "no live `--fix`" check sits on both the chain (E3) and safety (E4) lens.
  A argues it's intentional defense-in-depth on the single highest-cost regression.
- **RESOLUTION:** Keep the 4 tests; keep the deliberate `--fix` overlap (E3 checks it as chain
  correctness, E4 as a safety invariant) — redundancy on the most dangerous regression is a feature.

## Q3 — Evidence schema + cross-run aggregation rule (strict vs majority)?

- **A:** strict 12/12; a 2/3 split is audit-invalidating `INDETERMINATE`, not majority-voted away.
- **B:** strict 12/12 PLUS digest-identity; majority is explicitly rejected because the suite's PURPOSE
  is to prove reproducibility — a split is the exact defect class being hunted. Adds a
  `suite_failure_class` enum.
- **C:** strict 12/12 GREEN/RED gate; renders a 4×3 dashboard + machine roll-up.
- **RESOLUTION:** Strict 12/12, no majority. A non-unanimous test → status `DISAGREE`, overall
  `INDETERMINATE` (not silently RED) with a mandatory human-halt; any unanimous FAIL → `MIGRATION_NOT_VALIDATED`.
  Carry B's `suite_failure_class` enum + C's GREEN/RED dashboard + roll-up.yaml.

## Q4 — How to make the 3× runs genuinely independent yet consolidatable?

- **C:** 4 sequential batches × 3 parallel runs; each run writes only to its own `run-N/` dir; no run
  reads a sibling; a dedicated **aggregator subagent** reads the 12 `verdict.yaml` after all land.
- **B:** prompts pin the absolute worktree root (no cwd drift); each run re-executes every probe itself.
- **RESOLUTION:** Adopt C's batch-spawn + aggregator-subagent orchestration; adopt B's absolute-path
  pinning + per-run re-execution. Evidence root is append-only (re-running the suite makes a new
  timestamped root, never overwrites).

## Q5 — What falsification/negative check makes a PASS "we proved it" not "found nothing"?

- **A:** every test carries a named tripwire — E1: the sweep tool is proven able to find a token that
  IS present (else "0 hits" could be a broken regex); E2: no field LEAKS beyond the 7 into the wire
  block (proves the set is exactly 7, not ≥7); E3/E4: `FIX_TOTAL == FIX_PROHIBITION` (no live `--fix`);
  E4: no backend token inside the freeze block + baseline-self-consistency (the diff can't vacuously
  match an empty baseline).
- **B/C:** include per-test negative checks (troubleshoot IS present; no extra enum values; no `--tier`/`--intent`).
- **RESOLUTION:** Union all falsification checks into each merged test. This is the spec's signature
  property: **a green verdict is positive evidence, never absence of evidence.**

## Convergence outcome

No irreconcilable positions surfaced. Final convergence score **0.88** (≥ 0.65 PASS gate, ≥ 0.75 target).
Merge proceeds with A as base.

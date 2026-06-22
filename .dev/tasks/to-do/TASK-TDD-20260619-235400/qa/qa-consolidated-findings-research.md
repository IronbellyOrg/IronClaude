# Consolidated Research-Gate Findings — TASK-TDD-20260619-235400

**Date:** 2026-06-20
**Agents:** 10 (4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative), partitioned.
**Consolidated verdict: FAIL** (per gate rule: any issue of any severity → FAIL; fixes applied in Step 3.12).

## Per-agent verdicts
| Agent | Lens | Files | Verdict |
|-------|------|-------|---------|
| 3.1 rf-analyst A | completeness | 00,01,02 | PASS (OI-1 reflect side 20/20 fields complete; flags I2 below) |
| 3.2 rf-analyst B | completeness | 03,04,05 | FAIL (stale cross-ref + OI-1 table reflect-incomplete — synthesis directives) |
| 3.3 rf-analyst C | completeness | 06,07,08 | PASS |
| 3.4 rf-analyst crossval | OI-1 + reuse | all | PASS (2 non-blocking contradictions) |
| 3.5 rf-qa evidence A | evidence-quality | 00,01,02,03 | PASS (47/47 citations verified) |
| 3.6 rf-qa evidence B | evidence-quality | 04,05,06,07 | PASS (27/27 verified) |
| 3.7 rf-qa gap/staleness C | gap-detection | 08,web-01,all-tags | PASS (148 tags; 3 minor) |
| 3.8 rf-qa scope-coverage | scope | all | FAIL (CRITICAL: config.py + commands.py CLI surface unexamined) |
| 3.9 rf-qa-qual depth A | research-depth | 00-04 | PASS |
| 3.10 rf-qa-qual depth B | research-depth | 05-08,web-01 | PASS |

## Issues (deduplicated, by severity)

### CRITICAL
- **C1 — config.py + commands.py CLI-surface unexamined (from 3.8).** No research file deeply read `src/superclaude/cli/reflect/config.py` (`ReflectConfig` dataclass) or the `src/superclaude/cli/reflect/commands.py` Click option block where FR-RH2's `--transport {openai_compat|stub}` (default openai_compat), `--reviewers <N>` (clamp [2,4], default 3), and `--depth {standard|deep}` are surfaced and resolved into config. This is the FR-RH2 new-input mutation surface; §5 Technical Requirements and §8 API Specifications (CLI surface) cannot be reliably authored without it.
  - **FIX (3.12):** spawn a gap-fill research agent → `research/09-reflect-config-cli-surface.md` documenting the `ReflectConfig` field set + defaulting path + exact `--transport`/`--reviewers`/`--depth` insertion points, plus the `recipes/` registry (for I4 below). Tag `[CODE-VERIFIED]`.

### IMPORTANT (synthesis/TDD directives — NOT research-file defects; recorded for synth-04/06/09 to honor)
- **I1 — file 05 stale cross-ref to file 02 (from 3.2, 3.4).** File 05 (dated 06-19) calls file 02 a "stub header only / Status: In Progress." File 02 is actually Complete (06-20, 174 lines, 5 field tables). **DIRECTIVE for synth-04:** treat `02-reflect-contract-verdict.md` as AUTHORITATIVE/Complete; disregard 05's "02 is a stub" framing.
- **I2 — OI-1 correspondence table must join BOTH halves and exceed 05's 7 rows (from 3.2).** File 05 §7 lists only 7 reflect-side fields; file 02 enumerates a larger verdict-driver set (`t2_vendor_diversity`, `adversarial_unavailable`, `verification_ran`/`verification_skip_reason`, `citations_dropped`, `input_drift_detected`, `regression_present`, the 7 load-bearing booleans, `report_path`, `remediation_task_path`, etc.). **DIRECTIVE for synth-04:** the OI-1 table's left column = file 02's full verdict-driver field set; right column = file 05's DM-012 swarm source (mostly "absent → synthesize/default in ensemble.py"). Do NOT stop at 05's 7 rows.
- **I3 — `ensemble-empty` slug (M==0) not in contract.py today (from 3.1).** The (M,N) table maps M==0 → reason-slug `ensemble-empty` (exit 2), but `contract.py`'s BLOCKED reasons are `contract-missing`/`child-crash`/`contract-version-missing`/`unknown-major-version`/`malformed-*`. This collides with FR-RH2.7's "verdict map + exit codes unchanged." **DIRECTIVE for synth-06 (§12) + synth-09 (§22):** explicitly reconcile — either a new `derive_verdict` M==0 BLOCKED branch (a deliberate, recorded change) or map M==0 onto an existing BLOCKED trigger; surface as an Open Question.
- **I4 — `reflect-review` recipe binding (from 3.3).** Validator assertions 2 & 6 require `recipe_name`/`normalizer_strategy` to resolve in the recipe registry; `recipes/` was outside Phase-2 read scope. **FIX (3.12):** fold a `recipes/` registry read into the gap-fill agent (research/09) so the TDD can pin a registered recipe for the lens. **DIRECTIVE for synth-03/synth-08:** specify the recipe binding as a deliverable.
- **I5 — `--suspect-source` emitted but unparsed by sc-adversarial Mode A (from 3.3, 3.7; `[CODE-CONTRADICTED]`).** Already correctly tagged in research. **DIRECTIVE for synth-09 (§22/OI-4):** carry as an Open Question (teach Mode A to parse it, or keep advisory).
- **I6 — INV-005 arithmetic gap in reduce_wave3 (from 3.2).** `workers_failed` counted against `len(worker_results)` while N may be `workers_requested`; `succeeded+failed != requested` possible. **DIRECTIVE for synth-06 (§12 edge cases).**

### MINOR (no fix required)
- Off-by-one whole-file line-count nits in prose (not citations): runner.py "598"→597; merge.py "58"→57; bare-review SKILL "81"→80; process.py "354"→353; LensEntry class anchor "L636"→L637. All body file:line anchors are correct.
- 3.7: process.py "zero grep hits" over-claim (1 benign `merged` hit in an env-var docstring) — conclusion (orthogonal) still holds.

## Fix plan (Step 3.12)
1. Spawn ONE gap-fill research agent (fix_authorization context) → `research/09-reflect-config-cli-surface.md` covering C1 + I4 (config.py + commands.py Click surface + recipes/ registry), all `[CODE-VERIFIED]`.
2. Record I1-I6 as binding synthesis directives in `phase-outputs/plans/research-gate-verdict.md` (no research-file rewrites needed; they are forward-looking instructions for Phase 5).
3. Verify (3.13): re-check research/09 exists + substantive; confirm directives recorded. Then PASS.

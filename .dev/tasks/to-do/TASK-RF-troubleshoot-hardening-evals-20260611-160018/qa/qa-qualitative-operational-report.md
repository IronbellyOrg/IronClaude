# QA Report — task-qualitative (operational-correctness lens)

**Topic:** Differential backtest harness (E1-E5 OLD=MISS / NEW=CATCH)
**Date:** 2026-06-11
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false (REPORT-ONLY)

---

## Overall Verdict: FAIL

FAIL — 1 IMPORTANT (fabricated `evalIdString` citation, Step 3.4) + 1 IMPORTANT
(E1/E4 method-vs-function in-process invocation gap) + 2 MINOR. All are
report-only (fix_authorization: false); remediation listed for the serialized
fix agent. The harness DESIGN is operationally sound — all 5 parent shas
resolve, all 5 OLD callables exist at their pre-fix parents, the skip-guards
correctly fire, the anti-vacuity derivation is faithful to spec §5.4 — but two
citation/operational defects would surface during execution.

---

## Tool engagement
Read: 7 | Grep/Bash(grep): 11 | Glob: 0
(Read the full 548-line task file across pages; grep-verified every cited
source symbol + line range + every parent sha against actual git history.)

---

## Items Reviewed (operational-correctness lens)

| # | Operational check | Axis | Result | Evidence |
|---|-------------------|------|--------|----------|
| 1 | All cited source symbols + line ranges exist | AX-1 | FAIL | `evalIdString` regex (Step 3.4) has 0 occurrences in summary.schema.json; all others verified accurate |
| 2 | Phase ordering: helper before consumers | none | PASS | git_replay.py (P2) → replay_executor/catch_rate (P3) → per-escape runners (P4) → aggregation (P4.8). Correct topological order |
| 3 | Shell/git command preconditions satisfied | none | PASS | All 5 parent shas resolve via `git cat-file -e`; worktree add/remove/prune sequenced; `git fetch origin` precedes merge-base (Step 6.4) |
| 4 | OLD callables exist + invocable at pre-fix parent | AX-3 | FAIL | All 5 exist at parents; BUT E1 (`_build_file_args` @94d5baa0:170) + E4 (`_evaluate_gate` @1b0264f1:825) are METHODS needing class instantiation — task never specifies how the in-process replay obtains an instance |
| 5 | NEW=CATCH skipif probes correct + skip(not fail) | none | PASS | Probed refs (pipeline-hardening-closure.md, hardening-output-contract.md, per-escape refs) confirmed ABSENT in refs dir; skipif (not importorskip/xfail) correct |
| 6 | QA_GATE/VALIDATION/TESTING reqs reflected as items | none | PASS | Per-phase 10-step lens QA gates (P2-P5) + final 7-lens + fidelity (P6); Step 5.2 pytest-green + Step 5.4 ruff check AND format --check; TESTING=ALL covered |
| 7 | No item writes under docs/; reports → tmp_path | none | PASS | Steps 3.5/3.6/4.8/5.1 all route to tmp_path; conftest `catch_rate_output_dir` tmp_path-rooted; reports → phase-outputs/, never docs/ |

Axis legend (PR-07): AX-1 drift/stale-citation · AX-3 omission · none = lens applied, nothing fired.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (for serialized fix agent) |
|---|----------|----------|-------|------------------------------------------|
| 1 | IMPORTANT | Step 3.4 (task line 266) | Instructs "`escape_id` reuses the `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`" sourced from `summary.schema.json`. That schema has ZERO `evalIdString` `$def` and no `pattern` key — only a prose description "regex-guarded upstream" at line 165. The executor will grep summary.schema.json for `evalIdString`, fail to find it, and either fabricate or stall. | Either (a) drop the "reuses evalIdString" provenance claim and inline the literal regex as the schema's own `$defs.escapeId.pattern` (it is a valid pattern for E1..E5), OR (b) re-point the citation to wherever the eval-id regex actually lives. Do NOT claim it is reused from summary.schema.json. |
| 2 | IMPORTANT | Steps 3.1, 4.3, 4.6 (E1+E4 in-process replay) | E1 `_build_file_args` (@94d5baa0:170) and E4 `_evaluate_gate` (@1b0264f1:825) are bound METHODS (`self._build_file_args(...)`, indented `def`), not module-level functions. E2 (`_check_parallel_instructions`) and E3 (`gate_passed`) ARE module-level and trivially callable. The task says "invokes the real pre-fix product callable in-process" but never specifies how the E1/E4 replay obtains a class instance (constructor args, config fixtures). A naive `module._build_file_args(...)` import-and-call will raise. | Add an explicit note in Steps 4.3 + 4.6 that E1/E4 replay must instantiate the owning class (E1: the PRD executor class holding `_build_file_args`; E4: the executor holding `_evaluate_gate`) with a minimal config, OR call the staticmethod form where applicable. Confirm the instantiation surface at the parent checkout (signatures may differ from HEAD). |
| 3 | MINOR | Step 5.1 (task line 402) | Cites root `_pollution_snapshot` guard at "lines 30-93"; the function `def _pollution_snapshot` is actually at `tests/conftest.py:29`. Off-by-one start; harmless (the executor reads the function regardless). | Adjust citation to ~29-93 (cosmetic). |
| 4 | MINOR | Step 4.4 / 4.5 (E2 & E3 share H3 wave + `unmask-and-sweep.md` ref) | E2 and E3 both gate their NEW=CATCH proxy on `requires_impl_ref("unmask-and-sweep.md")` and both map to wave H3. This is legitimate (E2=word-boundary classifier, E3=advisory severity sweep — two facets of H3) and the task DOES use distinct function/escape ids, but the shared-ref/shared-wave is a subtlety a reviewer could misread as a duplicate. | No code change required. Optionally add a one-line comment in test_backtest_e3.py noting it shares the H3 `unmask-and-sweep.md` ref with E2 but asserts the distinct `K_swept==K_true` severity facet (the task body already says this in prose — surface it in the test). |

---

## Operational Soundness — Confirmed PASS items (with own tool work)

- **All 5 pre-fix parent shas resolve** in local git history (`git cat-file -e` OK for 94d5baa0/10723863/e97aa4fd/1b0264f1/d878bc6d). G2 CI-shallow skipif is justified — `.github/workflows/test.yml` has NO `fetch-depth` on any `actions/checkout@v4` → shallow depth-1 → commits absent on CI → skip(not fail) correct.
- **All 5 OLD callables exist at their pre-fix parents** (E1:170, E2:197, E3:20, E4:825, E5 SKILL.md POST-reflect `<BASE>..HEAD` selector @2195). The OLD=MISS negative witnesses are real, not theatrical.
- **E1 fix already landed on HEAD** (`7601ad25` #151 removed the `--file` flag; HEAD docstring at prd/process.py:11 says "no `--file` flag"). `_build_file_args` does NOT exist on HEAD — but DOES at parent 94d5baa0. The replay design (against parent, not HEAD) is correct; the spawn-instruction "confirm on HEAD" is satisfied at the replay target instead. NOT a defect.
- **E4 HEAD-drift handled correctly**: HEAD healed via `20693bb8`; task pins E4 replay to `1b0264f1` (bug present) and frames as H2 ledger-completeness. Matches spec §8.3 + research/04.
- **E5 selector**: parent `d878bc6d` SKILL.md uses `<BASE>..HEAD` two-dot range (the vacuous-PASS surface); HEAD fixed it to single-ref working-tree diff. Task's own Step 6.4 correctly uses the FIXED single-ref `git merge-base HEAD origin/master` selector — no self-contradiction.
- **Anti-vacuity derivation faithful**: spec §5.4 (lines 419-421, 538) + research/07 (lines 136-137) confirm `complete = all-5-CATCH ∧ negative_witness ∧ card_path`. Step 3.2 encodes exactly this. The named test `test_backtest_status_keeps_pipeline_health_advisory_until_complete` (spec:568) is referenced in Step 3.6.
- **Skip-guards correct**: probed impl-ref files confirmed absent in `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (dir has calibrator-eval-cases.md, diagnosability-audit.md, etc. — NOT the hardening refs). `skipif` (not `importorskip`, not `xfail`) is the right mechanism. `--strict-markers` ON (pyproject:111) — task uses skipif decorators/helpers, introduces NO unregistered `pytest.mark.X`. Correct.
- **No docs/ writes**: every report-writing item targets tmp_path or phase-outputs/. `_pollution_snapshot` autouse guard will not trip.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for B2 self-containment, phase structure/ordering/anti-orphaning, POST-reflect-penultimate placement, TB-Add-1..8, G1 no-caret parent SHAs, E4 1b0264f1 pin. I did NOT re-verify section numbering, frontmatter shape, or item structure.

**(b) Independent semantic checks (≥1 required, INV-019):**
- rf-qa PASS on "G1 no-caret parent SHAs verified clean" was INSUFFICIENT for the operational lens: I independently ran `git cat-file -e <sha>^{commit}` for all 5 parents AND `git show <parent>:<file> | grep "def <callable>"` to prove each OLD callable actually EXISTS and is the right kind (method vs function) at the replay target. This surfaced Issue #2 (E1/E4 are methods needing instantiation) — a defect rf-qa's structural sha-format check could not detect.
- rf-qa structural checks do not verify cited-symbol EXISTENCE in mirror-source files. I grep-verified every cited line range in models.py (835-946, 905-921, 923-946), run_report.py (67/96/233/366/413), runner.py (110/136), schemas/__init__.py (30), and the conftest idioms — and caught Issue #1 (`evalIdString` regex fabricated: 0 occurrences in summary.schema.json) that no structural gate flagged.
- Independently confirmed the anti-vacuity `complete` derivation against the live RELEASE-SPEC §5.4 and research/07:136-137 (not relying on the research-alignment PASS verdict) — confirmed faithful.

---

## How to interpret this verdict
The harness is ~95% operationally executable as written. The two IMPORTANT
issues are localized citation/invocation gaps that the serialized fix agent can
resolve in-place without restructuring any phase. Neither blocks the phase
ordering, the skip-guard design, the report model, or the collision boundary.
After fixing Issues #1 and #2, the task should execute green
(passes-or-correctly-skips with backtest_status=not_run today, impl refs absent).

---

## VERDICT: FAIL

Unfixable-by-me issues (fix_authorization: false — for the serialized fix agent):
1. IMPORTANT — Step 3.4 fabricated `evalIdString` regex citation (summary.schema.json has no such $def).
2. IMPORTANT — Steps 4.3/4.6 do not specify how E1/E4 bound-method callables are instantiated for in-process replay.
3. MINOR — Step 5.1 `_pollution_snapshot` line citation off-by-one (30-93 → 29-93).
4. MINOR — E2/E3 shared H3 ref/wave subtlety could use an inline clarifying comment.

Report path: /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/qa/qa-qualitative-operational-report.md

# QA Task Research-Alignment Report

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-11
**Task file:** TASK-RF-troubleshoot-hardening-evals-20260611-160018.md
**Research dir:** research/ (08 files)
**Track goal:** Differential backtest harness replaying E1-E5 (OLD=MISS vs NEW=CATCH skip-guarded), machine-readable catch-rate report driving backtest_status per NFR-1.
**Stance:** ADVERSARIAL — assume builder dropped/misrepresented research findings.

---

## Methodology

Cross-validate each load-bearing research finding (8-item checklist) against task items.
Flag (a) findings with no corresponding task item, (b) task items fabricating actions not grounded in research, (c) reintroduction of superseded readings.

---

## Files Read (evidence base)

- TASK file (full, all 6 phases + frontmatter + Risks/OQ): lines 1-548
- research/08-gap-fill-reconciliation.md (AUTHORITATIVE tie-breaker): full
- research/05-replay-targets.md (per-escape OLD=MISS / NEW=CATCH / §8.3): full
- research/06-impl-tasklist-crossref.md (pure-markdown seam, skipif, collision, parents[3], impl-ref filenames): full
- research/07-mdtm-template-and-report-model.md (report model + derivation + parametrized-pytest): full

---

## Checklist Cross-Validation (8 load-bearing findings)

### CL-1 — G1 checkout PARENT shas DIRECTLY, NO caret — PASS

research/08 §G1 (L54-72, L245) is authoritative: store the PRE-FIX PARENT sha per escape, check out with NO `^`. Confirmed table E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d`.

Task encoding verified at every load-bearing surface:
- Key Constraints G1 (L125): bare parents listed verbatim, "NEVER apply `^` at runtime."
- Step 1.4 replay-table (L184): `prefix_parent_sha (CHECKOUT TARGET, no caret)` column; "runtime checkout is `git checkout <prefix_parent_sha>` with zero caret arithmetic."
- Step 2.1 git_replay.py (L196): REPLAY_ESCAPES tuple populated VERBATIM with the 5 bare parents; module docstring mandate "NEVER apply `^` (double-decrement hazard per G1)."
- Step 2.2 unit test (L200): asserts NO `prefix_parent_sha` contains a `^` character.
- Step 2.QA.2 (L214) dedicated G1 no-caret lens; Step 4.QA.2 (L362) re-checks bare parents; Step 6.2.2 lens 3 re-checks.
- Risks ASSUMPTION (L518) restates G1.

NO reintroduction of the superseded research/03 `<sha>^` framing anywhere. research/03 is explicitly tagged "SUPERSEDED by 08" in the Previous Stage Outputs (L103) and Key Constraints. **PASS — strongly aligned, multiply-guarded.**

### CL-2 — OLD=MISS = in-process replay of REAL callables at parent — PASS

research/05 establishes the 5 real callables: E1 `_build_file_args` (cli/prd/process.py), E2 `_check_parallel_instructions` (cli/prd/gates.py), E3 `gate_passed` (cli/pipeline/gates.py), E4 `_evaluate_gate` (cli/prd/executor.py), E5 POST-reflect range selector (task-builder/SKILL.md).

Task Source Areas (L119) lists ALL five callables 1:1 with the same file paths. Per-escape runners Steps 4.3-4.7 each replay the correct pre-fix callable: E1 L332 (`_build_file_args` → `--file <local_path>`), E2 L336 (`_check_parallel_instructions` final-phase FP), E3 L338 (`gate_passed` advisory-severity HALT), E4 L344 (`_evaluate_gate` second-consumer), E5 L346 (`start_commit..HEAD` vacuous-PASS). The ReplayExecutor seam (Step 3.1, L254) is in-process callables, "NOT a real Claude PTY." **PASS.**

### CL-3 — NEW=CATCH = pure-markdown doc-presence proxy + skipif (NOT importable, NOT xfail) — PASS

research/06 §B (L106-155) resolves the seam as pure-markdown, no importable Python gate; §C (L159-213) mandates `pytest.mark.skipif` on impl-ref existence, NOT `importorskip`, and recommends skipif over xfail (repo has zero xfail per research/02).

Task encoding:
- Key Constraints NEW=CATCH skip-guard (L126): "NEVER use `importorskip` (nothing importable) and NEVER use `xfail` (zero occurrences in repo)."
- Step 4.1 `_impl_guard.py` (L324): `requires_hardening_impl = pytest.mark.skipif(...)`, "NO `importorskip` and NO `xfail`."
- Each per-escape NEW=CATCH proxy is decorated `requires_impl_ref(...)` keyed on a SPECIFIC ref file.
- Step 4.QA.3 (L366) dedicated skip-guard lens re-checks "NOT importorskip, NOT xfail."

Impl-ref filenames cross-validated against research/06 §A.2 (L90-93) — ALL match: E1→`runtime-entrypoint-verification.md` (L332), E2→`unmask-and-sweep.md` (L336), E3→`unmask-and-sweep.md` (L340), E4→`contract-enumeration.md` (L344), E5→`effective-input-proof.md` (L348). The foundational-ref skipif keys on `pipeline-hardening-closure.md` + `hardening-output-contract.md` (research/06 L188-189; task L324, L87). **PASS.**

### CL-4 — E4 HEAD-drift: replay pinned to 1b0264f1, framed as H2 ledger-completeness — PASS

research/04 §4 + research/05 E4 section (L181-220) establish: the E4 advisory bug is already HEALED on HEAD via `20693bb8`, fix `b97c9960` UNMERGED; replay must pin to pre-fix parent `1b0264f1`, framed as §8.3 H2 ledger-completeness over BOTH `gate_passed` AND `_evaluate_gate`.

Task encoding:
- Key Constraints E4 HEAD-drift (L131): pin `1b0264f1` NOT HEAD; "advisory-fatal bug already HEALED on HEAD via `20693bb8`"; "Frame E4 as the §8.3 ledger-completeness assertion (both `gate_passed` AND `_evaluate_gate` consumers classified)."
- Step 4.6 (L344): explicit `1b0264f1` pin with inline comment "HEAD is already healed via `20693bb8`"; NEW=CATCH proxy `contract-enumeration.md` asserts "BOTH `gate_passed` AND `_evaluate_gate` consumers be classified."
- Step 4.QA.7 (L382) dedicated E4-HEAD-drift + dual-evaluator lens; Risks RISK (L516) restates.

E3/E4 dual-evaluator pair correctly modeled (E3=`gate_passed`, E4=`_evaluate_gate`). **PASS.**

### CL-5 — CI shallow-clone skipif (G2) + no-leaked-worktree porcelain post-condition (G3) — PASS

research/08 §G2 (L93-177) and §G3 (L181-239) authoritative.

Task encoding:
- Key Constraints G2 (L129) + G3 (L130) restate both with the exact predicates.
- Step 2.3 (L204): module-level `pytestmark = pytest.mark.skipif(...)` probing `git cat-file -e <prefix_parent_sha>^{commit}` per escape + `git rev-parse --is-inside-work-tree` guard; no-leaked-worktree test captures `worktree_list_porcelain()` baseline, asserts `after == baseline`; "`prune` is always called in `finally`."
- Step 2.1 (L196) helper teardown: `remove --force` + `rmtree(ignore_errors=True)` + `prune` in `finally`.
- Step 2.QA.4 (L222) dedicated G2+G3 lens. Risks RISK (L515) restates G2.

Note: the `<sha>^{commit}` peel probe is git-object-existence (cat-file), NOT a parent-decrement `^` — distinct from the G1 caret hazard and correctly used. **PASS.**

### CL-6 — Collision boundary: writes ONLY under tests/troubleshoot/backtest/; parents[3]; parent __init__.py only-if-absent — PASS

research/06 §D (L216-294) authoritative on the off-limits set + `backtest/`-only rule + parents[3] + only-if-absent parent `__init__.py`.

Task encoding:
- Key Constraints Collision boundary HARD (L127): "Write ONLY under `tests/troubleshoot/backtest/`"; off-limits skill dir, command, `.claude/` mirrors, impl-owned `__init__.py` + 7 `test_hardening_*` + `e2e-backtest-scenarios.md`.
- Path resolution (L128): `parents[3]` (NOT `parents[2]`), assert pyproject.toml guard; parent `__init__.py` only-if-absent.
- Step 1.5 (L188): backtest `__init__.py` + parent only-if-absent, "do NOT overwrite it if present."
- Step 4.1 (L324): `REPO_ROOT = Path(__file__).resolve().parents[3]`. Step 4.2 (L328) dedicated parents[3] guard test.
- Steps 2.QA.6 (L230), 4.QA.6 (L378) collision-boundary lenses; Risks RISK (L517). **PASS.**

### CL-7 — Report model: frozen dataclass + __post_init__ invariant + to_dict + Draft202012Validator + backtest_status derivation; SEPARATE from pipeline_hardening_verdict; emit to tmp_path not docs/ — PASS WITH ONE GAP (see Issue-1)

research/07 PART B (L88-153) + research/01 establish the full run_report.py-mirror triad, the backtest_status enum/derivation, the separation invariant, the Draft202012Validator fidelity test, and the tmp_path (not docs/) emission rule.

Task encoding is thorough: Step 3.2 (L258) frozen `EscapeResult`+`CatchRateReport` with field tuples + `_derive_backtest_status` + `__post_init__`; Step 3.3 (L262) `render_catch_rate_json` + `_check` guard + `CatchRateContractViolation`→exit 2; Step 3.4 (L266) draft-2020-12 schema + importlib.resources loader; Step 3.5 (L270) Draft202012Validator fidelity test + valid/invalid fixtures + tmp_path-only; Step 3.6 (L274) separation test; emit-to-tmp_path enforced at L132, L270, L352, L370. SEPARATION from run-level verdict enforced at L80, L258, L274, Step 3.QA.5 (L296).

**One derivation-fidelity gap — see Issue-1 below.** Otherwise PASS.

### CL-8 — Parametrized pytest, not suite YAML — PASS

research/07 PART C (L157-169) recommends parametrized pytest over suite YAML. Task Step 4.8 (L352): `@pytest.mark.parametrize` over the 5 escape specs sourced from `REPLAY_ESCAPES`, aggregated into one `CatchRateReport`; parametrize ids `E1`..`E5`. No suite-YAML manifest anywhere in the task. **PASS.**

---

## Fabrication Check (task items referencing files/patterns NOT in any research file)

Swept all created-file paths, callables, shas, and impl-ref filenames in the task against the 8 research files:

- All 5 parent shas + fix shas + `20693bb8` heal commit — grounded in research/08 + research/05/04.
- All 5 OLD callables + their file paths — grounded in research/05 + Source Areas.
- All 6 impl-ref filenames — grounded in research/06 §A.2.
- run_report.py / models.py / summary.schema.json / test_reporter_contract.py mirror sources — grounded in research/07 PART B + research/01.
- `_subprocess` seam (process.py), test_process.py mock pattern, conftest allowlist, `_pollution_snapshot` — grounded in research/02 + research/03 + research/07.
- `tests/cli/eval/conftest.py` `allowlisted_output_dir` (Step 5.1 L402) — consistent with research/02 (subprocess mock seam, pollution guard) and the cliEval framework inventory (research/01). Specific line numbers (24-39, 30-93) are builder-supplied precision but the fixture/guard existence is research-grounded.

No fabricated file, callable, sha, or impl-ref detected. Line-number citations in the task (e.g. process.py:17/371-393, runner.py:136-156, models.py:835-946) are precision claims the builder added; they are consistent with the research files' own citations and were not independently re-verified against live source in this lens (out of scope — alignment lens, not code-trace lens). **No fabrication found.**

---

## Alignment Gaps (ADVERSARIAL — minimum 3 required)

### Issue-1 (IMPORTANT) — `complete` derivation drops the negative_witness + card_path conjuncts (research/07:137 dropped)

research/07 L137 is the authoritative `complete` derivation:
> `complete` — all 5 replayed AND all `verdict == CATCH` AND all have a `negative_witness` AND a cited `card_path` (the 100%-would-have-caught bar, research/07:372).

And L136:
> `partial` — some but not all E1–E5 replayed, OR any `MISS`, OR **any missing negative witness**.

The task's derivation rule (Step 3.2 L258, Step 3.QA.2 L284, Key Objectives 6 L80, Step 4.8 L352) is consistently stated as the REDUCED form:
> "all-5-CATCH→`complete` / 1-4→`partial` (with missing IDs) / 0-or-not-run→`not_run`."

The task drops the `negative_witness == True (all)` AND `card_path cited (all)` conjuncts from the `complete` gate. The `EscapeResult` model DOES carry `negative_witness` (bool) and `card_path` fields (L258), but `_derive_backtest_status` as specified only counts CATCH verdicts — a report where all 5 are `verdict=CATCH` but some lack a negative witness or cited card would derive `complete`, whereas research/07 says it must be `partial`. This weakens the NFR-1 "100%-would-have-caught" anti-vacuity bar (research/07:372) — exactly the false-assurance the harness exists to close. **Severity IMPORTANT** (not CRITICAL: the model fields exist so the fix is a derivation-logic tightening, not a schema change; and the NEW=CATCH proxy is skip-guarded today so `complete` is unreachable until impl lands). Recommended fix: Step 3.2's `_derive_backtest_status` and the Step 3.5(e) fidelity assertion should require `all(e.negative_witness)` AND `all(e.card_path)` for `complete`, and route a CATCH-but-no-witness escape to `partial`.

### Issue-2 (MINOR) — `proxy_limitation` recorded as "note field OR module docstring" — optional-of-two weakens the no-oversell guarantee

The NEW=CATCH proxy honesty requirement (research/06 §B L127-147, the "redundant cross-validating proxy … do not oversell" framing) is load-bearing for NFR-1 honesty. Task Step 3.2 (L258) specifies it as "a `proxy_limitation` note field **or** module docstring" — an inclusive-or that lets the builder satisfy it with only a module docstring, which would NOT travel into the emitted `catch-rate.json`/`catch-rate.md` artifact that a downstream consumer reads. Step 3.3 (L262) does separately require the markdown renderer to carry "a one-line proxy-limitation note," which mitigates this for the `.md` artifact — but the JSON artifact (the machine-readable one that drives `backtest_status`) has no guaranteed proxy-limitation field if the builder chooses the docstring branch. Step 3.QA.6 (L300) proxy-honesty lens would likely catch this, but the item as written permits the weaker realization. **Severity MINOR.** Recommended: require the proxy limitation as a serialized field (or a stable key) on the report so it survives into the machine-readable artifact, not only the docstring/markdown.

### Issue-3 (MINOR) — `card_path` (anti-inflation cited-card requirement) under-asserted relative to research/07:160

research/07 L114 + L137 + L160 make `card_path` a load-bearing anti-inflation field ("cited passing wave/card (anti-inflation; research/07:160)"), required-non-null for a `complete`-contributing CATCH. The task carries `card_path` as a model field (L258) and the schema lists `escapes` items, but NO task item asserts that a `complete`/CATCH escape MUST carry a non-null `card_path` — it is never referenced again in any assertion item (Steps 3.5, 3.6, 4.8) or QA lens. Combined with Issue-1, the cited-card anti-inflation guard is effectively unenforced. **Severity MINOR** (subsumed by Issue-1's fix if that fix also asserts `card_path`). Recommended: fold `card_path`-non-null into the Issue-1 derivation fix and add a fidelity assertion.

### Issue-4 (MINOR / OBSERVATION) — intermediate-gate agent floor: task uses 7-agent lens gates where research/07 I22 "standard" sets intermediate=3

research/07 §I22 (L62) maps "standard" intensity to intermediate gate = 3 agents, final = 7. The task's Key Constraints (L124) states "intermediate/phase gates = 3 agents; final/phase-gate lens QA = 7 agents," but the Phase 2/3/4/5 gates are each built as 7-lens M3 gates (Steps X.QA.2-X.QA.7), not 3-agent intermediate gates. This is an UPWARD deviation (more QA than the floor) so it is not a coverage gap and not a defect — flagged only for transparency since the lens is alignment-fidelity. research/07 I15 floors (intermediate ≥5) are also satisfied. **Not a FAIL contributor; observation only.**

---

## Verdict

**VERDICT: FAIL** (per binary I16 rule: ANY issue of ANY severity ⇒ FAIL)

Severity-rated issues:
- **Issue-1 — IMPORTANT:** `complete` derivation drops the `negative_witness` + `card_path` conjuncts mandated by research/07:136-137; weakens the NFR-1 100%-would-have-caught anti-vacuity bar. Recommend tightening `_derive_backtest_status` + the Step 3.5(e) fidelity assertion.
- **Issue-2 — MINOR:** `proxy_limitation` permitted as docstring-only (inclusive-or); may not reach the machine-readable JSON artifact.
- **Issue-3 — MINOR:** `card_path` anti-inflation field carried but never asserted; effectively unenforced (subsumed by Issue-1 fix).
- **Issue-4 — MINOR / OBSERVATION:** upward QA deviation (7-agent gates vs standard-intensity intermediate=3 floor); not a coverage gap, transparency note only.

**Alignment summary:** 8/8 load-bearing checklist findings are present and correctly encoded; the G1 no-caret reading is multiply-guarded with NO reintroduction of the superseded research/03 `^` framing; no fabrication detected. The single material gap is Issue-1 (derivation fidelity). Issues 2-3 are MINOR hardening of the same NFR-1 honesty surface. The task is substantively well-aligned; FAIL is driven by the IMPORTANT derivation-fidelity gap (Issue-1) plus the binary any-issue rule, not by any missing or fabricated finding.

## Findings (appended incrementally below)

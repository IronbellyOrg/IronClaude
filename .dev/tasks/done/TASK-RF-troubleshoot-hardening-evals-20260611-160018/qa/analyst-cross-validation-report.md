# Cross-Validation Report — Differential Backtest Harness Research

**Analysis type:** completeness-verification (cross-validation lens)
**Date:** 2026-06-11
**Track goal:** Differential backtest harness replaying E1-E5 against pre-fix commits (OLD=MISS vs NEW-gate=CATCH), emitting a machine-readable catch-rate report driving `backtest_status` per NFR-1.
**Files analyzed:** 7 (research/01 through research/07)
**Lens:** Cross-file consistency — contradictions, conflicting counts, divergent descriptions of shared components.
**Status:** COMPLETE
**Verdict:** PASS (with 4 builder reconciliation items — 1 Critical, 3 Important)

---

## Method

Read all 7 research files end-to-end (R1=01-eval-framework-inventory, R2=02-test-patterns-and-xfail, R3=03-git-replay-helpers, R4=04-spec-contract-deepdive, R5=05-replay-targets, R6=06-impl-tasklist-crossref, R7=07-mdtm-template-and-report-model). For each of the 8 prompt cross-checks, compared the relevant claims across files. Status legend: CONSISTENT (agree), MINOR (cosmetic/wording divergence, no impact), CONTRADICTION (substantive disagreement requiring resolution).

---

## CROSS-CHECK 1 — E1-E5 → wave → pre-fix-parent-SHA mapping (R4 prose vs R5 commits)

**Sources:** R4 §1 (CONTRACT A, spec §3.1 matrix) + R4 §1.1 provenance; R5 source-of-truth table (L19-25) + per-escape sections; R3 §4 parent-resolution.

### 1a. Wave assignment (E→H) — CONSISTENT
| Escape | R4 replay wave (§8.3) | R5 (table L19-25) | Agree? |
|--------|----------------------|-------------------|--------|
| E1 | H1 | H1 | YES |
| E2 | H3 | H3 | YES |
| E3 | H3 | H3 | YES |
| E4 | H2 | H2 | YES |
| E5 | H4 | H4 | YES |

Both agree the backtest replay wave is E1→H1, E2→H3, E3→H3, E4→H2, E5→H4. R4's §3.1 "Closing Wave(s)" column lists multi-wave closure (E1=H1,H2; E4=H1,H2; E5=H4,H5) but the §8.3 backtest rows (which R5 mirrors) pin the single replay wave. No contradiction — R4 explicitly notes §8.3 is the harness oracle. Both flag the same canonical-vs-merged-report wave-numbering trap (R4 §1 L51; R5 L31-35).

### 1b. Fix-SHA → pre-fix-parent-SHA mapping — R4≡R5 CONSISTENT
R4 and R5 AGREE with each other. R5 table (L19-25), corroborated by R3 §4 and R4 §1.1:

| Escape | Fix SHA | Pre-fix parent (`<fix>^`) | Wave |
|--------|---------|----------------------------|------|
| E1 | `7601ad25` | `94d5baa0` | H1 |
| E2 | `e97aa4fd` | `10723863` | H3 |
| E3 | `eb9a2633` | `e97aa4fd` | H3 |
| E4 | `b97c9960` (UNMERGED) | `1b0264f1` | H2 |
| E5 | `10723863` | `d878bc6d` | H4 |

The spawn prompt's per-escape tuples (E1 `7601ad25^=94d5baa0`, E2 `e97aa4fd^=10723863`, E3 `eb9a2633^=e97aa4fd`, E4 `b97c9960^=1b0264f1`, E5 `10723863^=d878bc6d`) **EXACTLY MATCH R5/R4/R3.** CONSISTENT.

**Chained-commit structure (captured identically by R4 and R5):** E3's fix `eb9a2633` has parent `e97aa4fd` = E2's *fix* SHA; E2's parent `10723863` = E5's *fix* SHA. This is a real commit chain, not an error. R5 L34 flags "E2 and E3 share wave H3" and "E3+E4 = dual-evaluator pair." R3 §4 independently confirms all 5 `<sha>` and `<sha>^` resolve. CONSISTENT across R3/R4/R5.

### 1c. "Is the listed SHA the fix or the parent?" — RESOLVED, CONSISTENT
R3 §4 (L166-170) raised this as an open question (reading (a) listed=fix, replay `<sha>^`; vs (b) listed=parent). R5 **definitively resolves it** (L19-25, 284-302): listed SHA = the fix commit; replay checks out `<fix>^`. R4 §1.1 uses the same framing (E1←#151 `7601ad25` = the fix). R3's open question is closed by R5. No residual contradiction.

**CROSS-CHECK 1 VERDICT: CONSISTENT.** R4 (spec prose) and R5 (commits) agree on every escape's wave and pre-fix-parent SHA; R3 corroborates resolvability; chained SHAs handled identically.

---

## CROSS-CHECK 2 — E4 HEAD-drift finding (R4) vs R5 replay-base implication

**R4 claim (§4.2, L160-173, L213):** The E4 advisory-fatal bug is **already healed on HEAD** via commit `20693bb8` ("honor advisory semantic-check flag in executor._evaluate_gate", 2026-06-11), NOT the spec's `b97c9960` (which remains UNMERGED, not an ancestor of HEAD). Both `_evaluate_gate@executor.py:859` and `gate_passed@gates.py:94` now honor `advisory` on HEAD. R4's recommended resolution: either (a) replay E4 against a **pre-`20693bb8` tree** for a literal negative witness, OR (b) frame E4 as a **ledger-completeness** assertion (assert H2 ledger names both `gate_passed`+`_evaluate_gate`). R4 explicitly defers the exact base commit to R5.

**R5 corroboration (E4 section L181-220, table L277):** R5 lists E4's pre-fix parent as `1b0264f1` (= `b97c9960^`) and confirms `b97c9960` is UNMERGED. R5's OLD=MISS observable: "`_evaluate_gate(...)` returns `False` (halts) despite advisory flag." R5's NEW=CATCH: "H2 ledger enumerates BOTH consumers."

### Consistency analysis
- **Both agree `b97c9960` is UNMERGED.** CONSISTENT.
- **Both agree E4's replay base parent is `1b0264f1`.** CONSISTENT.
- **Both agree E4's CATCH oracle is ledger-completeness (both consumers).** R4 §8.3-restatement and R5 (d) say the same. CONSISTENT.
- **DIVERGENCE (MINOR, not a contradiction): R5 does NOT mention the `20693bb8` HEAD-heal.** R5's git table and per-escape narrative are framed purely around the `b97c9960`/`1b0264f1` fix/parent pair; it never notes that the E4 fix has *since landed on HEAD via a sibling commit*. R4 §4.2 is the ONLY file carrying the `20693bb8` HEAD-drift nuance. R3 §4 also did NOT surface it (R3 noted `1b0264f1` resolves but not that the fix re-landed). This is a **coverage gap in R5/R3, not a contradiction** — nothing R5 says is *false*; R5 simply omits the load-bearing HEAD-state caveat that R4 flags as "the load-bearing nuance."

### Is the recommended resolution consistent?
R4 offers two paths (replay pre-`20693bb8` tree, OR ledger-completeness framing) and notes "option (b) matches the spec's wording." R5's E4 (d) lands squarely on option (b): "H2 ledger enumerates BOTH consumers; FAIL until both classified." So R5's prescribed CATCH oracle is **consistent with R4's recommended resolution path (b)**. The two do not conflict; R5 implicitly adopts R4's preferred framing.

**However — a replay-base subtlety the builder MUST reconcile:** R5's E4 replay-base parent is `1b0264f1` (= `b97c9960^`). But R4 §4.2 warns that the OLD=MISS negative witness for E4, *if done as a literal advisory-fatal repro*, must replay against a **pre-`20693bb8`** tree. `1b0264f1` (dated earlier) IS pre-`20693bb8`, so checking out `1b0264f1` DOES give a tree where `_evaluate_gate` ignores advisory — so R5's base is technically valid for a literal negative witness too. The nuance R4 adds is about replaying against *current HEAD* (which would NOT repro the bug). Since R5 prescribes checking out the parent `1b0264f1` (not HEAD), **R5's mechanic is compatible with both of R4's options.** No contradiction; R4 simply adds a "do not run E4 against HEAD" guard that R5 leaves implicit.

**CROSS-CHECK 2 VERDICT: CONSISTENT (with a flagged coverage asymmetry).** R4 and R5 do not contradict. R4 carries a load-bearing HEAD-drift caveat (`20693bb8`) that R5 and R3 omit; the builder MUST carry R4 §4.2/§6-item-11 into the task so the E4 replay base is pinned correctly. Flagged as **GAP-1 (Important)** below — not a contradiction, but an omission that could mislead an implementer reading only R5.

---

## CROSS-CHECK 3 — NEW=CATCH seam: R1 (import-reusable/mirror-EvalRunner) vs R6 (pure-markdown, no importable Python)

**This is the most consequential cross-check.** The two files describe the NEW=CATCH mechanism from different vantage points and there is a **genuine surface tension** that must be reconciled.

**R1 framing:** R1 catalogs the `cli/eval` framework as the thing to MIRROR — `EvalRunner`/`run_eval`/`LifecycleExecutor` Protocol seam, `run_report.py` writer, frozen-dataclass models. R1's entire mental model is "the backtest harness is a Python runner that executes scenarios and emits a report" (R1 §runner, §run_report, Summary items 1-3). R1 repeatedly says "MIRROR EvalRunner.run(spec)->EvalOutcome" and "the LifecycleExecutor Protocol seam ... lets the backtest stub 'checkout pre-fix commit → run protocol → capture verdict'."

**R6 framing:** R6 cross-references the **impl tasklist** and finds (§B, L106-156, high confidence) that **the H0–H5 gate logic is PURE MARKDOWN — there is no importable Python gate helper.** The gates live in `src/.../sc-troubleshoot-protocol/refs/*.md` + `SKILL.md`; the impl's own tests are content-assertion tests over that markdown (the `tests/skills/` pattern), NOT executions of a callable gate. R6's consequence: "We CANNOT `import` a gate function and assert it returns CATCH ... NEW=CATCH must be asserted as a **documentation-presence / content proxy**."

### Do they conflict?
**Partial tension, reconcilable — but the builder MUST resolve it explicitly.** The key distinction is **WHAT gets mirrored vs WHAT gets executed**:

1. **R1 is correct about the REPORT/HARNESS SCAFFOLDING.** The `CatchRateReport` model, the `run_report.py`-style writer, the frozen-dataclass+`to_dict()`+schema idiom — these ARE import/mirror targets and R7 independently confirms this (R7 PART B is a 1:1 mirror of `models.py`+`run_report.py`). No conflict on the *report* layer.

2. **R1 is OVER-OPTIMISTIC about the GATE EXECUTION seam.** R1 assumes the NEW gate is a callable the harness invokes ("run NEW H0–H5 gate → capture verdict"). R6 demonstrates with impl-tasklist evidence (L265: "content-assertion test over the SOURCE-OF-TRUTH markdown") that **the NEW gate is NOT a callable** — it is a behavioral rule a Claude runtime applies by reading markdown. There is nothing to import and call for the NEW=CATCH half.

3. **R1 itself hedges in the right direction.** R1's PtyDriver verdict (L162-167) and runner verdict (L136-141) both say "mirror the *driver seam* / Protocol, not necessarily a real ...". R1 never claims a hardening-gate Python function exists; it mirrors the *eval* framework's runner shape. So R1 is not *factually wrong* — it describes the eval framework accurately — but R1's "(a) per-escape-scenario runner → MIRROR EvalRunner" recommendation, taken literally, would lead a builder to expect an executable NEW gate that R6 proves does not exist.

### The load-bearing reconciliation (R6's "pure-markdown" claim vs R1's "mirror EvalRunner")
R6's pure-markdown claim **is consistent with R1's framing IF AND ONLY IF** the harness is understood as:
- **OLD=MISS half:** a real in-process replay (checkout `<fix>^`, run the OLD *product* code path — which DOES exist as callable Python, e.g. `_evaluate_gate`, `gate_passed`, `_check_parallel_instructions`) and assert the historical MISS. R1's runner-mirror + R3's git-replay seam apply here. R5 confirms the OLD code paths are real callables.
- **NEW=CATCH half:** a **documentation-presence proxy** (assert the impl's NEW `refs/*.md` document the catch mechanism), guarded by skipif until refs land. R1's "execute the NEW gate" does NOT apply; R6's content-proxy does.

R7 PART C independently lands on the same split and even **contradicts R6 slightly on the NEW half** (see CROSS-CHECK 8) by recommending parametrized pytest that "import the built H-gate functions and assert PASS/FAIL pre/post-fix" (R7 L163). R7 assumes importable H-gate functions; R6 proves there are none. **This R6-vs-R7 tension is the real contradiction** and is escalated in CROSS-CHECK 8.

**CROSS-CHECK 3 VERDICT: RECONCILABLE TENSION (not a hard R1-vs-R6 contradiction).** R1 accurately mirrors the *eval framework* and the *report layer* (corroborated by R7 PART B); R6 correctly establishes that the *NEW gate* is pure-markdown with no callable. They describe different layers. The danger is a builder reading R1 literally and expecting an executable NEW gate. **Flagged as GAP-2 (Important):** the task MUST adopt R6's seam reality (OLD=MISS = real product-code replay; NEW=CATCH = doc-presence proxy + skipif) and treat R1 as the *report-writer/dataclass* mirror only, NOT as evidence that an executable NEW hardening gate exists. R1's "mirror EvalRunner" is load-bearing for scaffolding shape, misleading for gate execution.

---

## CROSS-CHECK 4 — Skip-guard mechanism: R2 (no xfail; forward-probe + pytest.skip) vs R6 (skipif on impl-ref existence)

**R2 claim (§2, L41-125):** The codebase has **ZERO `pytest.mark.xfail`** (grep → 0). The established convention for "impl not landed yet" is a **forward-dependency probe (`hasattr` on the impl module, or `inspect.getsource` for closure branches) + self-clearing `pytest.skip(...)`**. R2's decision matrix (L118-124) maps "NEW gate impl symbol/branch not yet landed" → inline `pytest.skip` after `hasattr`/`getsource` probe; and "replay commit / git fixture missing" → `@pytest.mark.skipif(not PATH.exists())`.

**R6 claim (§C, L159-213):** Because the seam is markdown (nothing importable), `importorskip`/`hasattr` probes do NOT apply to the NEW gate. R6 recommends **`pytest.mark.skipif` keyed on the impl ref FILE existing** (`refs/pipeline-hardening-closure.md` + `hardening-output-contract.md`). R6 explicitly prefers **skipif over xfail** (L205-210): "skipif is the lower-noise choice and is what the impl's own pattern implies."

### Consistency analysis
- **Both agree: NO xfail.** R2 says zero xfail in repo; R6 says "prefer skipif over xfail." CONSISTENT.
- **Both land on `skipif` for the NEW half — and this is internally coherent.** R2's decision matrix says: use inline `pytest.skip`+`hasattr` when the guard is on a *first-party impl SYMBOL*; use `@pytest.mark.skipif(not PATH.exists())` when the guard is on a *file/fixture on disk*. R6 establishes that the NEW gate is NOT a symbol (it's markdown), so per R2's OWN matrix the correct mechanism is the **file-existence `skipif`** (the "git fixture missing" row), NOT the `hasattr` probe. **R6's skipif-on-ref-path is exactly the R2 matrix branch for a non-symbol, on-disk dependency.** They are CONSISTENT — R6 selected the right R2 branch.
- **Apparent divergence (MINOR, resolved):** R2's *headline* example (test_exit_codes.py) uses `hasattr` forward-probe + inline `pytest.skip`, which at first glance differs from R6's module-level `skipif`. But R2 §2e and the decision matrix explicitly carve out the file-existence case for `skipif`. Since the hardening gate has no importable symbol, R6 correctly falls into R2's `skipif` branch. No contradiction.
- **Both agree the OLD=MISS half runs unconditionally green.** R2 §6 ("Always-green now") and R6 §C/§E item 3. CONSISTENT.

### One reconciliation note for the builder
R2 §2b also offers the `inspect.getsource(...)` substring probe "if the NEW gate is a code branch (not a named symbol)." R6 proves the NEW gate is neither a symbol NOR a code branch — it's prose in a `.md`. So **neither `hasattr` nor `getsource` applies**; only file-existence `skipif` does. The two files do not conflict, but the builder should NOT use R2's `hasattr`/`getsource` exemplar for the hardening-gate guard — R6's `Path(...).exists()` skipif is the right one. (R2 itself anticipates this: its Hand-off note L271 defers the symbol-vs-branch question to R6.)

**CROSS-CHECK 4 VERDICT: CONSISTENT.** R2 and R6 agree on "no xfail" and both prescribe `skipif`; R6's ref-path-existence skipif is precisely the R2-matrix branch for a non-importable on-disk dependency. R2 explicitly defers the probe-type choice to R6 (L271), and R6 resolves it correctly. Builder caveat: use file-existence skipif (R6), not the `hasattr`/`getsource` exemplar (R2's symbol-case), for the markdown gate.

---

## CROSS-CHECK 5 — Subprocess mock seam patch-target string (R2 vs R3)

**R2 claim (§4, L164-186):** Patch the module-aliased import site: `patch("superclaude.cli.sprint.process._subprocess.run")` (cites `tests/sprint/test_process.py:399`); also `patch("superclaude.cli.pipeline.process.subprocess.Popen")` (`:206`). Mock returns `MagicMock(returncode=, stdout=)`. Prefer the narrow `_subprocess` alias over the global `subprocess.Popen` to avoid cross-talk (cites `tests/sprint/conftest.py:1-30`).

**R3 claim (§1, L11-80):** The seam is `import subprocess as _subprocess` at `process.py:17`; patch target = `superclaude.cli.sprint.process._subprocess.run`. Cites the SAME call sites: `test_process.py:399,434,446,453,460-463,471-474`. Mock return = `MagicMock(returncode=0, stdout=...)` (`:435-438`). R3 §1.4 prescribes the harness-local seam: "the harness git helper must (1) live in a module that does `import subprocess as _subprocess` at module top, and (2) call `_subprocess.run([...])`, so the unit test patches `<harness.module>._subprocess.run`."

### Consistency analysis
- **Patch-target string: IDENTICAL.** Both cite `superclaude.cli.sprint.process._subprocess.run` and the same line `test_process.py:399`. CONSISTENT.
- **Mock-return shape: IDENTICAL.** Both `MagicMock(returncode=, stdout=)` at `:435-438`. CONSISTENT.
- **Harness-local `_subprocess` alias prescription: IDENTICAL.** R2 §4a ("if R3 names the helper ... aliases subprocess, the patch string is `<that module>.<alias>.run`") and R3 §1.4 (the `import subprocess as _subprocess` module-top requirement) say exactly the same thing. R2 explicitly DEFERS the exact dotted path to R3 (R2 §4a L178, Hand-off L270: "Exact git-helper patch target: depends on R3's git-helper module path"); R3 supplies it. CONSISTENT — clean producer/consumer handoff.
- **Cross-talk warning: CONSISTENT.** R2 §4b and R3 §2 (drift.py prior-art, "prefer the module-top alias seam") both warn against the broad `subprocess.Popen` global patch and prefer the narrow alias. R3 adds the `drift.py` `_git()` prior-art (`git -C` style) that R2 doesn't mention — that's additive, not contradictory.

**CROSS-CHECK 5 VERDICT: CONSISTENT (verbatim agreement).** R2 and R3 agree exactly on `superclaude.cli.sprint.process._subprocess.run`, the `MagicMock(returncode, stdout)` shape, and the harness-local `import subprocess as _subprocess` + `_subprocess.run` prescription. R2 defers the exact path to R3; R3 supplies it. No divergence.

---

## CROSS-CHECK 6 — Report model: R1 vs R7 (frozen-dataclass + to_dict + __post_init__ + Draft202012Validator; src/ vs tests/)

**R1 claim (§models.py, §run_report.py, §4.7-placement, Summary):** The report model mirrors `RunSummary`/`RunCounts` — frozen dataclass + explicit `_*_FIELDS` ordering tuple + `to_dict()` walking it + `__post_init__` invariant guard. The writer mirrors the `run_report.py` triad (pure `render_*` + `_check_invariant`-first + `_write_artifact_set` + `write_aggregated_report`). R1 §4.7 placement: "put the report MODEL + writer under `src/`" + scenario specs/pytest harness under `tests/troubleshoot/backtest/`.

**R7 claim (PART B, L88-153, L175):** 1:1 mirror of `models.py`+`run_report.py`+`summary.schema.json`+`test_reporter_contract.py`. Proposes `CatchRateReport` + `EscapeResult` frozen dataclasses with field-order tuples, `__post_init__` invariant (counts + `backtest_status` derivation, mirroring `kept_plus_skipped_equals_n_prime`), `to_dict()`, `render_catch_rate_json` (one `json.dumps(..., sort_keys=False)+"\n"`), `CatchRateContractViolation`→exit 2, sibling `catch_rate.schema.json` (draft 2020-12) + `load_catch_rate_schema()`, `Draft202012Validator` fidelity test. R7 proposes the model at `src/superclaude/cli/eval/backtest_report.py` (or `catch_rate.py`).

### Consistency analysis
- **Dataclass idiom: IDENTICAL.** frozen + `_*_FIELDS` tuple + `to_dict()` + `__post_init__` invariant. R1 §models.py and R7 PART B step 1-3. CONSISTENT.
- **Invariant-guard-before-write: IDENTICAL.** R1's `_check_invariant`/`ReporterContractViolation`→exit 2; R7's `CatchRateContractViolation`→`exit_codes.USAGE_ERROR` (exit 2). Both cite `run_report.py:56,67-108`. CONSISTENT.
- **`backtest_status` derivation as a `__post_init__` invariant: IDENTICAL pattern.** R1 (L292 "`__post_init__` derives/validates `backtest_status ∈ {not_run,partial,complete}` exactly like `RunCounts.kept_plus_skipped_equals_n_prime`") and R7 L129-137 (`_derive_status` helper, loud ValueError on mismatch). CONSISTENT — and both correctly tie it to NFR-1. Note: R7's derivation rule (all 5 CATCH + negative_witness + card_path → complete) is *stricter/more detailed* than R1's, but R1 explicitly says "derives/validates ... exactly like" and defers detail to R7 ("R7 covers modeling the catch-rate report"). Additive, not contradictory.
- **Draft202012Validator fidelity test: IDENTICAL.** R1 §schemas (importlib.resources-loaded schema, `to_dict()`-is-producer, fidelity-test-asserts-match triad, "R7 covers modeling") and R7 step 8 + PART B fidelity test. CONSISTENT.
- **src/ vs tests/ placement — CONSISTENT.** R1 §4.7 (L260-269): "put the report MODEL + writer under `src/` ... keep scenario specs + pytest harness under `tests/troubleshoot/backtest/`." R7 proposes the model under `src/superclaude/cli/eval/backtest_report.py` — i.e. under `src/`. **Both agree the report model/writer lives under `src/`, the pytest harness under `tests/`.** CONSISTENT. (R4 §5 / CONTRACT D §4.7 independently confirms the same placement rule: "reusable runtime replay logic must live under `src/superclaude/`; pure markdown-contract validators may stay in `tests/troubleshoot/`.") Triple-consistent across R1/R4/R7.

**One MINOR location-precision divergence (not a contradiction):** R1 says "under `src/`" generically and points at how `run_report.py`/`models.py` live under `src/superclaude/cli/eval/`. R7 picks the SPECIFIC path `src/superclaude/cli/eval/backtest_report.py`. R6 §D, however, marks `src/.../sc-troubleshoot-protocol/**` off-limits but says nothing about `src/superclaude/cli/eval/` — so R7's chosen path is NOT in a collision zone. The exact module name (`backtest_report.py` vs `catch_rate.py`) is an unforced impl choice R7 itself flags ("e.g."). No conflict; builder picks one.

**CROSS-CHECK 6 VERDICT: CONSISTENT.** R1 and R7 agree on the frozen-dataclass + `to_dict()` + `__post_init__`-invariant + `Draft202012Validator` idiom and on `src/` placement for the model/writer (triple-confirmed by R4 §4.7). R7 supplies the concrete `CatchRateReport`/`EscapeResult` detail R1 defers to it. Only divergence is the unforced specific module-filename choice.

---

## CROSS-CHECK 7 — Path depth: R6 `parents[3]` for backtest/ vs other path claims

**R6 claim (§C L186, L198-202, §E item 2):** Files at `tests/troubleshoot/backtest/<file>.py` are 3 levels under repo root (`backtest`→`troubleshoot`→`tests`→root), so `REPO_ROOT = Path(__file__).resolve().parents[3]`. R6 contrasts this with the impl's `parents[2]` (impl tests live directly at `tests/troubleshoot/<file>.py`). R6 recommends verifying via `(REPO_ROOT/"pyproject.toml").exists()`.

**R2 claim (§3c L162):** For files at `tests/cli/eval/` the repo uses `parents[3]` (cites `test_exit_codes.py:58`); R2 reasons "from `tests/troubleshoot/backtest/` REPO_ROOT = `Path(__file__).resolve().parents[3]` as well" — explicitly because the file is 3 dirs deep (`backtest`→`troubleshoot`→`tests`→root). R2 flags "**Verify by counting at impl time.**"

### Consistency analysis
- **R2 and R6 AGREE: `parents[3]` for `tests/troubleshoot/backtest/`.** R2 L162 and R6 L186/L198 both arrive at `parents[3]` by the same depth count. CONSISTENT.
- **R7 (PART A, frontmatter note) and R6 reference the impl's `parents[2]`** for files directly under `tests/troubleshoot/` (R6 §A.1 L61, R7 cites the sibling's `tests/skills` `parents[2]`). This is the *impl's* depth (one level shallower), correctly distinguished from *our* `backtest/` depth. No conflict — different file locations, different counts, both correct.
- Both R2 and R6 add the same safety check ("verify/count at impl time" / `pyproject.toml` exists assert). CONSISTENT.

No conflicting path-depth claim exists anywhere in the 7 files. R3 §5.3 discusses scratch-root paths (tmp_path vs `.dev/`) — orthogonal to `REPO_ROOT` depth, no conflict.

**CROSS-CHECK 7 VERDICT: CONSISTENT.** R2 and R6 independently agree on `parents[3]` for `tests/troubleshoot/backtest/`; the impl's `parents[2]` (shallower location) is correctly distinguished, not contradictory. No divergent path-depth claim elsewhere.

---

## CROSS-CHECK 8 — Suite-YAML vs parametrized-pytest (R7) vs R1's suite.schema.json mirror

**R7 claim (PART C, L157-169):** **RECOMMENDATION: parametrized pytest E2E backtest, NOT a cliEval `suites/*.yaml` manifest.** Rationale: (1) the sibling task already does parametrized E2E and passed PRE reflect; (2) cliEval suite YAML models *subprocess/CLI* evals (stdout-contains/exit-code), the wrong surface for *in-process gate replay*; (3) `pytest.mark.parametrize` over escape specs is idiomatic; (4) the catch-rate report is the machine-readable artifact, replacing a suite `summary.json`. Caveat: a pure-subprocess escape *could* be a 1-eval suite YAML, but the roll-up belongs in pytest.

**R1 claim (§suites/, §schemas/, Summary item 3):** R1 says scenario declaration "→ MIRROR the `suite.schema.json` `evalEntry` shape + `validate_manifest`/`SuiteLoader` ... Declare E1–E5 in a YAML manifest (id, title, target_commit, {old:MISS, new:CATCH}); validate with a re-implemented schema + loader; ship a `backtest-suite.schema.json`."

### Do they conflict? — YES, a REAL (but soft) CONTRADICTION on the scenario-declaration surface
This is the **clearest cross-file divergence in the set.**
- **R1 recommends a YAML manifest** (mirror `suite.schema.json`/`SuiteLoader`) to declare E1–E5.
- **R7 explicitly recommends AGAINST a suite YAML** and FOR parametrized pytest, giving 4 evidence-based reasons, and specifically argues the suite-YAML surface is wrong for in-process gate replay (R7 L163).

These are **directly opposed recommendations for the same artifact** (how to declare E1–E5).

### Resolution / which is better-grounded
R7's recommendation is **better grounded** for this specific harness:
1. R7 cites the **sibling-task precedent** (parametrized E2E, already PRE-reflect-passed) — concrete prior art R1 lacks.
2. R7 correctly identifies that `suite.schema.json` models **subprocess/PTY evals** (R1 itself documents this — R1 §pty_driver L162-167 concludes PtyDriver/subprocess-eval is "almost certainly NOT needed"). So **R1 is internally in tension**: it recommends mirroring the suite-YAML/SuiteLoader (built for subprocess evals) while ALSO concluding the subprocess/PTY machinery isn't needed. R7 resolves that tension by dropping the suite YAML.
3. R6's pure-markdown finding (CROSS-CHECK 3) further undercuts a suite YAML: the NEW=CATCH half is a doc-presence proxy, not a subprocess `expects[].stdout` check — exactly what R7 argues.

**However, R1 and R7 are NOT irreconcilable** — R7 itself preserves R1's escape hatch: "if any of E1–E5 is genuinely a black-box CLI invocation whose only observable is stdout/exit-code ... THAT single scenario could legitimately be a 1-eval suite YAML." And R1's deeper point — that scenario declaration needs *some* validated structure — is satisfied by R7's `EscapeResult`/`CatchRateReport` + `catch_rate.schema.json` (the schema-validated declaration moves from a suite YAML into the report dataclass + its schema). So the **validated-declaration principle** R1 wants survives; only the *vehicle* changes (pytest parametrize + report schema, not suite YAML + SuiteLoader).

### Note on R7's own internal tension (escalated from CROSS-CHECK 3)
R7 PART C L163 says the parametrized pytest will "**import the built H-gate functions and assert their PASS/FAIL behavior pre- and post-fix**." But **R6 §B proves there are NO importable H-gate functions** (pure markdown). So R7's stated parametrize mechanism (import + call the gate) is **partially infeasible for the NEW=CATCH half** — it works for OLD=MISS (real product code) but not for NEW=CATCH (must be a doc-presence proxy per R6). This is a **second contradiction: R7 (import H-gate functions) vs R6 (no importable gate).** R6 is correct (it cross-referenced the actual impl tasklist + on-disk skill dir); R7's "import the built H-gate functions" is over-optimistic for the NEW half, same root cause as R1's over-optimism in CROSS-CHECK 3.

**CROSS-CHECK 8 VERDICT: CONTRADICTION (soft, resolvable).** (a) R1 (suite YAML) vs R7 (parametrized pytest, no suite YAML) directly oppose on scenario declaration — **R7 is better grounded** (sibling precedent + suite-YAML-is-subprocess-surface + R1's own "no PTY needed" tension); reconcile by adopting R7's parametrized pytest + `catch_rate.schema.json` for declaration, reserving suite YAML only for any pure-subprocess escape (R7's own caveat). (b) R7's "import the built H-gate functions" (L163) contradicts R6's pure-markdown finding for the NEW=CATCH half — **R6 is correct**; the NEW half must be a doc-presence proxy, not a gate-function import. Both escalated as **GAP-3 (Important)** and **GAP-4 (Critical)** below.

---

## Compiled Cross-File Findings (gap list)

### Critical (blocks coherent task synthesis — must resolve before build)
- **GAP-4 — R7-vs-R6 NEW=CATCH execution mechanism contradiction.** R7 PART C (L163) prescribes parametrized pytest that "import the built H-gate functions and assert PASS/FAIL pre/post-fix." R6 §B (L106-156, evidence: impl tasklist L265 + on-disk skill dir = markdown only, no `.py`) proves there is **no importable H-gate function** — the NEW gate is pure markdown asserted via content-proxy. For the OLD=MISS half R7's import-and-assert works (real product code: `_evaluate_gate`, `gate_passed`, `_check_parallel_instructions` per R5). For the NEW=CATCH half it does NOT. **Resolution: adopt R6's seam — OLD=MISS = in-process replay of real product code; NEW=CATCH = doc-presence proxy over impl refs, skipif-guarded until refs land.** This is CRITICAL because building toward "import the NEW gate" produces a harness that cannot work (nothing to import) and would block the catch-rate report's `complete` path.

### Important (affects quality / could mislead the implementer)
- **GAP-1 — E4 HEAD-drift caveat carried only by R4.** R4 §4.2/§6-item-11: the E4 advisory-fatal bug is already healed on HEAD via `20693bb8` (not the spec's unmerged `b97c9960`). R5 and R3 omit this. Not a contradiction (R5's `1b0264f1` replay base is still valid), but the builder MUST carry R4's "do NOT run E4 against HEAD; replay against parent `1b0264f1`, or frame E4 as ledger-completeness" guard, or an implementer reading only R5 could try to repro the bug against current code and see no MISS.
- **GAP-2 — R1 "mirror EvalRunner" reads as executable-NEW-gate; reconcile with R6.** R1's runner-mirror framing (correct for the eval framework + report scaffolding) must NOT be taken as evidence that an executable NEW hardening gate exists. Adopt R1 for the report-writer/dataclass mirror only (corroborated by R7 PART B); adopt R6 for the gate-execution reality.
- **GAP-3 — R1 (suite YAML) vs R7 (parametrized pytest) scenario-declaration contradiction.** Directly opposed recommendations. R7 is better grounded (sibling precedent; suite YAML is a subprocess surface; R1's own "no PTY needed" tension). Resolution: parametrized pytest + `catch_rate.schema.json` for declaration; suite YAML only for any pure-subprocess escape (R7's caveat). The validated-declaration principle R1 wants is preserved via the report schema.

### Minor (cosmetic / no build impact)
- **MINOR-1 — Report-model module filename unforced choice.** R7 offers `backtest_report.py` or `catch_rate.py`; R1 says "under `src/`" generically. Not in any R6 collision zone (`src/superclaude/cli/eval/` is unrestricted). Builder picks one.
- **MINOR-2 — R2 `hasattr`/`getsource` exemplar vs R6 file-existence skipif.** Both reach "no xfail, use skipif" (consistent), but the builder should use R6's `Path(...).exists()` skipif (markdown gate has no symbol/branch to probe), not R2's symbol-case `hasattr`/`getsource` exemplar. R2 itself defers this to R6 (L271).

### Shared-dependency consistency (verified consistent)
- Subprocess mock seam string `superclaude.cli.sprint.process._subprocess.run` + `MagicMock(returncode, stdout)`: R2 ≡ R3 (verbatim).
- `parents[3]` for `tests/troubleshoot/backtest/`: R2 ≡ R6.
- `src/` placement for report model/writer: R1 ≡ R4 ≡ R7.
- frozen-dataclass + `to_dict()` + `__post_init__` + `Draft202012Validator` idiom: R1 ≡ R7.
- E1-E5 wave + pre-fix-parent SHA mapping: R3 ≡ R4 ≡ R5.
- "no xfail; skipif for NEW half; OLD half green now": R2 ≡ R6.
- Collision boundary (`tests/troubleshoot/backtest/` only; skill dir off-limits): R6 §D; consistent with R4 §4.7 placement rule.

---

## VERDICT: PASS (with 4 cross-file reconciliation items the builder MUST encode)

**Rationale for PASS:** The 7 research files are **mutually consistent on every substrate fact** — the E1-E5→wave→pre-fix-parent SHA mapping (R3≡R4≡R5, and matching the spawn prompt), the subprocess mock seam (R2≡R3 verbatim), path depth `parents[3]` (R2≡R6), `src/` report placement (R1≡R4≡R7), the frozen-dataclass/`to_dict`/`Draft202012Validator` report idiom (R1≡R7), the skip-guard "no-xfail / skipif" convention (R2≡R6), and the collision boundary (R6 + R4 §4.7). No two files disagree on a fact that would corrupt the build.

The cross-file tensions found are **resolvable design divergences, not factual contradictions**, and in every case one file is better-grounded and the resolution is clear:
- The R1-vs-R6 "mirror EvalRunner vs pure-markdown" tension (GAP-2) resolves to: R1 = report scaffolding mirror; R6 = gate-execution reality.
- The R1-vs-R7 "suite YAML vs parametrized pytest" contradiction (GAP-3) resolves to R7 (better-grounded; preserves R1's validated-declaration principle via the report schema).
- The R7-vs-R6 "import H-gate functions vs no importable gate" contradiction (GAP-4, the one Critical) resolves cleanly to R6 for the NEW=CATCH half (doc-presence proxy) while R7's import-and-assert remains valid for the OLD=MISS half (real product code).
- The E4 HEAD-drift caveat (GAP-1) is an R4-only coverage item, not a contradiction; it must be carried forward.

These are exactly the kind of cross-cutting reconciliations a task builder needs surfaced — they do not represent broken or fabricated research. Each divergent claim is evidence-cited and traceable to a specific file/line, and the better-grounded side is identifiable in every case. **PASS.**

**Builder must-encode summary:**
1. OLD=MISS = in-process replay of real product code at `<fix>^` (R3 git-worktree seam + R5 per-escape oracles). NEW=CATCH = doc-presence proxy over impl refs, `skipif`-guarded on `refs/pipeline-hardening-closure.md`+`hardening-output-contract.md` existence (R6 §C). [GAP-2/GAP-4]
2. Declare E1-E5 via parametrized pytest + `catch_rate.schema.json`, NOT a cliEval suite YAML (R7 PART C); suite YAML only for a pure-subprocess escape. [GAP-3]
3. Pin E4 replay base at parent `1b0264f1`; carry R4's "do NOT run E4 against HEAD (`20693bb8` healed it)" caveat; frame E4 as ledger-completeness (both `gate_passed`+`_evaluate_gate`). [GAP-1]
4. Report model/writer under `src/` (R1≡R4≡R7); pytest harness under `tests/troubleshoot/backtest/` only (R6 collision boundary); patch `<harness>._subprocess.run` (R2≡R3); `REPO_ROOT=parents[3]` (R2≡R6).

# Research: Gap-Fill Round 1

- **Status:** In Progress
- **Date:** 2026-06-21
- **Topic:** Close the 5 research-QA gaps for TASK-RF-ensemble-adversarial-seam (wire the
  adversarial seam result-object into `build_reflect_contract`; add a regression-HALT test).
- **Repo root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3` (worktree)
- **Decisive prior finding (R2):** the `/sc:adversarial` Mode-A child emits SCORE-ONLY
  (`convergence_score` + status/paths), NOT `deviation_count_by_class` /
  `regression_present` / `unauthorized_deviation_present` / `needs_human_decision`. All five
  files 01–05 read; anchors re-verified against live source below.

All `file:line` anchors verified by Read/Grep on this worktree during this round.

---

## GAP-2 — Derive-vs-extend SCOPE FORK (the decisive one)

### The constraint that forces the fork

R2 (`research/02-…:151-162`) is decisive: the Mode-A child's return-contract emits ONLY
`convergence_score`, `merged_output_path`, `artifacts_dir`, `status`, `base_variant`,
`unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method`,
`unaddressed_invariants` (producer schema `sc-adversarial-protocol/SKILL.md:431-443`). A grep
for `deviation_count_by_class|regression_present|unauthorized_deviation_present|needs_human_decision`
over the adversarial skill returns ZERO hits (R2:81-82). Therefore three of the contract's
verdict-driving fields — `unauthorized_deviation_present`, `needs_human_decision`, and the
per-class `deviation_count_by_class` breakdown — have **NO production acquisition path today**.
Only `convergence_score` (→ `adversarial_convergence_score`) and a report path are live-supplyable
from the child.

This is why the task must **fork**: the GOAL's "map … into `build_reflect_contract`" is the
PLUMBING (a seam-result object threaded through the builder) + the regression TEST — both
achievable now. Making the producer actually EMIT real per-class counts + the 3 booleans is a
separate surface (the sc-adversarial child / reviewer-merge) and is a documented FOLLOW-ON.

### RECOMMENDED design: widen the seam to a small `AdversarialResult` object

Today the seam is score-only:

- `AdversarialScoreFn = Callable[[list[str], Path], float | None]` — `ensemble.py:72`
  (verified R1:14-22).
- Default scorer `run_adversarial_scorer(...) -> float | None` — `ensemble.py:244-249`;
  its lossy return is `return extract_convergence_score(parse_adversarial_contract(output_dir))`
  at `ensemble.py:271` (verified R1:88-115, R2:23).
- The seam call site assigns ONLY a float to `adversarial_convergence_score`
  (`ensemble.py:221-232`, branches at L223 default and L229 fn — verified R1:47-65).
- `build_reflect_contract(...)` is called with only `swarm_merged_path`, the score float, and
  `adversarial_unavailable` (`ensemble.py:234-239`, verified R1:67-78).

RECOMMENDED widening (the plumbing the GOAL asks for):

1. Introduce a small dataclass (in `ensemble.py` or `models.py` — keep it a plain dataclass to
   stay clear of the NFR-7 no-nesting guard, R4:232-254):
   `AdversarialResult{ convergence_score: float|None, regression_present: bool,
   unauthorized_deviation_present: bool, needs_human_decision: bool,
   deviation_count_by_class: dict[str,int], report_path: str|None }`.
2. Widen `AdversarialScoreFn` (`ensemble.py:72`) and `run_adversarial_scorer`
   (`ensemble.py:244-249`) to return `AdversarialResult | None` in lockstep (R1:264-289 lists the
   full lockstep set).
3. The DEFAULT production scorer (`run_adversarial_scorer`) populates ONLY what the child can
   supply — `convergence_score` (from `extract_convergence_score(parse_adversarial_contract(...))`,
   `ensemble.py:271`) and `report_path` — and leaves the 3 reviewer-deviation fields at HONEST
   CLEAN defaults: `regression_present=False`, `unauthorized_deviation_present=False`,
   `needs_human_decision=False`, `deviation_count_by_class={authorized:0,necessary:0,drift:0,regression:0}`.
4. `build_reflect_contract` (`ensemble.py:360-407`) gains kwargs for the new fields and THREADS
   them through instead of the hard-coded literals at `ensemble.py:385-390` (all-zero counts),
   `:401` (`regression_present:False`), `:402` (`unauthorized_deviation_present:False`),
   `:403` (`needs_human_decision:False`), `:404` (`user_decision_required:False`). The fields stop
   being constants and start being parameters with clean defaults.

### The headline TEST injects a non-clean seam result

The regression test (GAP per GOAL) injects an `adversarial_score_fn` whose `AdversarialResult`
carries `regression_present=True` (and/or `deviation_count_by_class["regression"] >= 1`), proving
the plumbing routes to HALTED — i.e. the contract is no longer hard-coded clean. `regression_present`
must be a genuine Python `bool` (it is in `_LOAD_BEARING_BOOL_FIELDS`, `contract.py:47-57`; a
non-bool present value routes BLOCKED `malformed-contract-boolean`, `contract.py:200-209` — R3:111-135).
Keep `convergence_score` non-None (e.g. 0.86) so `null-convergence` DEGRADE (`contract.py:284`) does
not mask the HALT.

### Field-by-field disposition (what is live now vs default-clean-pending-producer)

| Contract field | Status after THIS task | Source |
|---|---|---|
| `adversarial_convergence_score` | **WIRED + LIVE** | from child `convergence_score` via `extract_convergence_score` (`ensemble.py:271`); already threaded `ensemble.py:395` |
| `report_path` (adversarial) | **WIRED + LIVE-able** | adversarial `merged_output_path` can now be threaded; today `_select_report_path` (`ensemble.py:488-497`) returns the swarm path only (R1:202-220). Task aligns it to the adversarial report when present, swarm as subrun fallback (R5 align note, `research/05-…:202`) |
| `regression_present` | **WIRED, default-clean (False) pending producer**; TEST injects True | hard-coded `ensemble.py:401` today → becomes a threaded param |
| `unauthorized_deviation_present` | **WIRED, default-clean (False) pending producer** | hard-coded `ensemble.py:402` → threaded param |
| `needs_human_decision` (+ mirror `user_decision_required`) | **WIRED, default-clean (False) pending producer** | hard-coded `ensemble.py:403-404` → threaded param |
| `deviation_count_by_class` (per-class breakdown) | **WIRED, default all-zero pending producer**; TEST may inject `regression>=1` | hard-coded `ensemble.py:385-390` → threaded param |

### Consistency with the GOAL + the follow-on

The GOAL says "map deviation_count_by_class, regression_present, unauthorized_deviation_present,
needs_human_decision, and the adversarial report_path into build_reflect_contract; add a test
where the seam reports a regression and assert derive_verdict does NOT PASS." That is EXACTLY the
plumbing + test above — achievable now WITHOUT touching the sc-adversarial producer. This is
consistent: "map into `build_reflect_contract`" = thread the result-object fields through the
builder (replacing constants) + prove the route with an injected non-clean seam result.

**FOLLOW-ON / Open Question (NOT in this task's core):** making the adversarial child (or the
reviewer-merge step) actually EMIT real per-class `deviation_count_by_class` + the 3 booleans into
`<t2-adversarial>/adversarial/return-contract.yaml` (`ensemble.py:283-284`), then parsing those new
fields in `parse_adversarial_contract`/a richer extractor. This touches the sc-adversarial producer
surface (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md`) — a separate component — and is
explicitly out of scope here. This flips the OI-1 SYNTHESIZED rows from "default-clean" to
"DERIVED-from-adversarial" (see `research/05-…:157-178`, the "unless the adversarial/reflect domain
supplies counts" conditional). Document it as Open Question OQ-PRODUCER.

**Net:** wired-and-live NOW = `adversarial_convergence_score`, adversarial `report_path`. Wired-but-
default-clean-pending-producer = `regression_present`, `unauthorized_deviation_present`,
`needs_human_decision`/`user_decision_required`, per-class `deviation_count_by_class`. Follow-on
needs = producer emission of the 3 booleans + per-class counts into the child return-contract.

---

## GAP-4 — Regression-HALT vs low-convergence-DEGRADE semantic separation

### The two outcomes live on different rungs of the first-match-wins ladder

`derive_verdict` (`contract.py:130-246`) evaluates `blocked → degraded → halted → pass`,
first-match-wins (R3:34-38). The two outcomes the fix MUST NOT conflate sit on DIFFERENT rungs,
and DEGRADED is checked BEFORE HALTED:

- **LOW / NULL convergence = reviewers DISAGREED → DEGRADE path (rung 2).** Handled by
  `_degraded_reason` (`contract.py:249-304`, verified this round). The convergence-specific
  trigger is Trigger 11: `tier_reached == 2 and contract.get("adversarial_convergence_score") is None`
  → `"null-convergence"` (`contract.py:283-285`, verified). Related degrade triggers in the same
  ladder that represent "couldn't reach a clean ensemble verdict": `adversarial_unavailable is True`
  → `adversarial-unavailable` (`contract.py:276-277`), `merge_method == "single-reviewer-fallback"`
  → `single-reviewer-fallback` (`contract.py:280-281`). These are the R3 disagreement/degrade
  family — exit 11, NOT a regression.

- **Reviewer-FOUND regression → HALT path (rung 3).** Handled by `_halted_reason`
  (`contract.py:307-328`, verified this round): `contract.get("regression_present") is True`
  → `"regression"` (`contract.py:315-316`), and the count fallback `deviations["regression"] > 0`
  → `"regression"` (`contract.py:323-324`). Exit 10.

### The non-conflation rule the fix MUST follow

**Do NOT auto-derive `regression_present` from a low convergence threshold.** A low convergence
score means the reviewers DISAGREED about the artifact — that is reviewer dispersion, which the
ladder already routes to DEGRADE (`null-convergence` / single-reviewer-fallback). Synthesizing
`regression_present=True` from `convergence < threshold` would misclassify reviewer DISAGREEMENT
as a found REGRESSION, jumping a run from the correct exit 11 (degraded, retryable) to exit 10
(halted, blocking) on no actual regression evidence. R2:130-134 lists "derive a regression signal
from convergence vs threshold" only as a feasibility option for downstream design — this gap-fill
REJECTS it for the verdict semantics: `regression_present` must come from an EXPLICIT producer
signal, never from the score.

For THIS task: the seam `AdversarialResult` carries `regression_present` as its own explicit
field, defaulting to `False` from the score-only child (GAP-2). The convergence score continues to
flow ONLY into `adversarial_convergence_score` and continues to drive ONLY the DEGRADE rung
(`null-convergence`). The TEST injects `regression_present=True` directly — it does NOT lower the
score to provoke a regression. (R4:273-275 also pins: keep `convergence_score` non-None so the
DEGRADE rung does not fire first and mask the HALT under test.)

### How the DEGRADE path is preserved (pin)

1. `_degraded_reason` (`contract.py:249-304`) is FROZEN by FR-RH2.7 — see GAP-5. The fix touches
   neither it nor the ladder order.
2. The default scorer keeps returning `convergence_score=None` on child-launch/parse failure
   (today: `run_adversarial_scorer` returns `None` on non-zero rc, `ensemble.py:268-270`; lossy
   parse → None via `extract_convergence_score`). Under the widened seam this maps to
   `AdversarialResult(convergence_score=None, regression_present=False, …)`, so
   `build_reflect_contract` still emits `adversarial_convergence_score=None` and (at
   `tier_reached==2`) `derive_verdict` still routes `null-convergence` DEGRADE. This is the R3
   null-convergence fallback the task must preserve (`research/05-…:203`).
3. Because DEGRADE is rung 2 and HALT is rung 3, a run that is BOTH degraded AND carries a
   regression routes DEGRADE first — the fix does not change that ordering. The regression-only
   TEST therefore uses a HEALTHY ensemble (all-distinct survivors, non-None score) so no degrade
   trigger fires first and the HALT is the first match (R4:176-199).

---

## GAP-1 — Complete backward-compat surface (every call site / test that pins the current shapes)

All anchors below re-verified this round by Grep/Read on the live worktree. The shapes that widen:
`AdversarialScoreFn` (`ensemble.py:72`), `run_adversarial_scorer` (`ensemble.py:244-271`), and
`build_reflect_contract` (`ensemble.py:360-407`). `extract_convergence_score`
(`ensemble.py:336-357`) and `parse_adversarial_contract` (`ensemble.py:274-289`) can stay
unchanged (the widened scorer wraps their output).

### Production-side (`src/`)

| # | Surface | Anchor | What widening breaks | Required update |
|---|---|---|---|---|
| P1 | `AdversarialScoreFn` alias | `ensemble.py:72` | return type `float\|None` → `AdversarialResult\|None` | edit alias |
| P2 | seam call site (both branches) | `ensemble.py:221-232` (default L223-227, fn L229-231) | both branches assign the result to the float var `adversarial_convergence_score` | destructure the `AdversarialResult`; pass its fields to the builder |
| P3 | `run_adversarial_scorer` sig + body | `ensemble.py:244-249` (sig), `:271` (return) | returns `float\|None`; L271 returns only the extracted score | widen to build + return `AdversarialResult`; default the 3 booleans clean; still CALL `extract_convergence_score(parse_adversarial_contract(...))` to fill `convergence_score` |
| P4 | `build_reflect_contract` call | `ensemble.py:234-239` | passes only swarm path + score + unavailable | add kwargs for the new fields |
| P5 | `build_reflect_contract` sig + body | `ensemble.py:360-366` (sig), `:385-390`/`:401-404` (hard-codes) | hard-coded literals must become the new params | add params (clean defaults); thread them in place of the constants |
| P6 | `runner.py` production entrypoint | `runner.py:425` — `run_tier2_ensemble(config)` | **NONE** — calls with positional `config` ONLY, no `adversarial_score_fn` kwarg (verified `runner.py:418-425`) | none; default-scorer path is insulated |

No other module imports `AdversarialScoreFn` (R1:285). `run_tier2_ensemble` is imported only by
`runner.py:35` and called at `runner.py:425` without the score-fn kwarg.

### Test-side (`tests/`) — the pinning call sites

| # | Test surface | Anchor (verified) | What widening breaks | Required update |
|---|---|---|---|---|
| T1 | `_const_score` stub helper | `test_ensemble_stub_integration.py:39-41` (`-> float`) | stub returns a bare float; new seam expects `AdversarialResult\|None` | return an `AdversarialResult(convergence_score=0.86, regression_present=False, …)` |
| T2 | `_const_score` injection site 1 (`_run` driver) | `test_ensemble_stub_integration.py:93` | passes `adversarial_score_fn=_const_score` | none beyond T1 |
| T3 | `_const_score` injection site 2 | `test_ensemble_stub_integration.py:331` | same | covered by T1 |
| T4 | `_const_score` injection site 3 | `test_ensemble_stub_integration.py:356` | same | covered by T1 |
| T5 | autospec spy (i11) | `test_ensemble_stub_integration.py:420` — `patch.object(runner_mod, "run_tier2_ensemble", autospec=True)`; assert `call_args.args[0] is config2` (`:422-424`) | **NONE** — spies `run_tier2_ensemble`, NOT the score fn; asserts only that the runner passes `config` positionally. Widening the seam object / builder does not change `run_tier2_ensemble`'s call signature from the runner | none |
| T6 | autospec spy (i11b) | `test_ensemble_stub_integration.py:445` — same patch shape; `spy_ensemble.assert_not_called()` (`:450`) | **NONE** — Tier-1 negative; never enters the seam | none |
| T7 | `build_reflect_contract` direct unit (U5) | `test_ensemble_unit.py:170` — `build_reflect_contract(workers, adversarial_convergence_score=0.86)` | builder gains NEW kwargs with clean defaults → existing call stays valid | none required IF new params default-clean; OPTIONAL companion asserts the clean defaults |
| T8 | adversarial-parse unit (U10) | `test_ensemble_unit.py:262-291` — `parse_adversarial_contract` + `extract_convergence_score(...) == 0.33` / `0.86` / `None` | **NONE** if those two helpers keep their existing signatures (recommended, see P3 wrap) | none |

**Key backward-compat finding:** the brief's "two autospec=True spies at :420 and :445" patch
`run_tier2_ensemble` (the runner→ensemble boundary), NOT the adversarial score fn. Their
assertions (`call_args.args[0] is config`, `assert_not_called`) are agnostic to the seam-object
widening, so they do NOT break — confirmed against `runner.py:425` calling
`run_tier2_ensemble(config)` with no score-fn kwarg. The brief's "U10 at :262-291" is the
`test_u10_adversarial_contract_parse_real_shape` test (verified `test_ensemble_unit.py:262`),
exercising `parse_adversarial_contract`/`extract_convergence_score` directly. The ONLY mechanical
breakage is T1 (`_const_score` return type), which transitively covers T2/T3/T4. Keeping
`extract_convergence_score` + `parse_adversarial_contract` signatures intact (wrap, don't replace)
keeps U10 (T8) and U5 (T7) green without edits — the recommended low-blast-radius choice consistent
with FR-RH2.7.

---

## GAP-5 — Concrete FR-RH2.7 "derive_verdict unchanged" proof method

FR-RH2.7 (spec.md:295-305, quoted R3:154-168 / R5:115-127) freezes `derive_verdict`, the helper
ladder, and the `Verdict` exit-code map. The proof that the fix honored this is a THREE-part
verification, all runnable as single-line commands from the worktree root.

### Part A — the frozen files are byte-unchanged (no diff)

`derive_verdict`, `_degraded_reason`, `_halted_reason`, `_extract_deviations`,
`_LOAD_BEARING_BOOL_FIELDS`, `_make_result`, `parse_contract` all live in `contract.py`; the
`Verdict.exit_code` map lives in `models.py:38-49` (R3:140-150). The fix must touch NEITHER file.
The literal proof:

```
git diff -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py
```

This MUST print NOTHING (empty diff). A non-empty diff is an FR-RH2.7 violation. (Run from the
worktree root; the implementation should confine its edits to `ensemble.py` and, if the
`AdversarialResult` dataclass is placed there, optionally `models.py` — but if placed in
`models.py` the diff is no longer empty, so RECOMMEND defining `AdversarialResult` in `ensemble.py`
to keep `models.py` byte-clean and this exact command valid as the proof.)

### Part B — the existing clean-path PASS test (I1) stays green

The I1 positive test asserts `contract["status"] == "success"`, `result.verdict is Verdict.PASS`,
`exit_code == 0` on a healthy ensemble (R4:87-93,140-151). After the fix, a clean run (no injected
findings, default-clean booleans) must still PASS. Plus the U6 frozen-ordering guard
(`test_ensemble_unit.py:178-201`, verified this round) asserts the BLOCKED→DEGRADED→HALTED→PASS
comment order and the verdict exit codes are unchanged — it will fail if the ladder is touched.

```
uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -k i1 tests/cli/reflect/test_ensemble_unit.py -k u6 -q
```

### Part C — the full reflect + swarm suites pass (NFR-RH2.6 backward-compat)

```
uv run pytest tests/cli/reflect tests/swarm -q
```

All green, including the NEW regression test (HALTED/exit-10/`reason=="regression"`) and the NFR-7
no-nesting guard (`test_no_nesting_guard.py`, R4:232-254 — `ensemble.py` must still contain
`ClaudeProcess` and NONE of `Task(`, `subagent`, `import anthropic`, `from anthropic`,
`subprocess.run(`, `Popen(`, `import subprocess`). Also note `test_u9` (`test_ensemble_unit.py:236-259`)
bans `:4000/v1` / `:8317` / `/cli` literals in `ensemble.py` — the new dataclass/code must carry none.

**One-line combined gate (recommended task acceptance command):**

```
git diff --quiet -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py && uv run pytest tests/cli/reflect tests/swarm -q
```

The `git diff --quiet` exits non-zero (failing the `&&`) if either frozen file changed, giving a
single pass/fail gate that encodes both "frozen files untouched" and "all tests green."

---

## GAP-FIX — R5 path correction (the prior task file is NESTED, not flat)

R5 dropped one directory level. Verified this round (`ls` + `test -f`): the prior FR-RH2 task file
is NESTED inside its own directory, and the flat sibling does NOT exist.

- **CORRECT (verified exists):**
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`
  (162969 bytes — `NESTED EXISTS`).
- **WRONG (verified missing):**
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md` (`FLAT MISSING`).

The two cited artifacts under that directory ALSO use the nested form and were verified to exist
this round:

- **OI-1 table (cited in §3.3 of R5):**
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/phase-outputs/discovery/oi1-mapping-table-validated.md`
  (`OI1 EXISTS`) — rows 35/38/39/40 (the four SYNTHESIZED fields).
- **QA CRITICAL #2 (cited in §3.4 of R5):**
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/qa-content-ensemble-formation-correctness-report.md`
  (`QA-CRIT2 EXISTS`) — row 39.
- **Consolidated R6 rejection (cited in §3.5 of R5):**
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/qa-consolidated-findings.md`
  (`QA-CONSOL EXISTS`) — lines 84-85.

**Correction directive for the builder:** wherever R5 / the OI-1 table / QA CRITICAL #2 / the prior
task file are cited, use the directory-nested path
`…/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/<artifact>`. The frontmatter `parent_task`
value stays the bare ID `TASK-RF-fr-rh2-headless-ensemble-20260620-024238` (an identifier, not a
path), but any `parent_doc` / citation that points at the task FILE must include the repeated
directory segment.

---

## Status: Complete

### Summary — GAP-1..5 + GAP-FIX → resolution

- **GAP-2 (scope fork):** RECOMMEND widening the seam to a plain `AdversarialResult` dataclass
  (`convergence_score, regression_present, unauthorized_deviation_present, needs_human_decision,
  deviation_count_by_class, report_path`) threaded through `build_reflect_contract`
  (`ensemble.py:360-407`) in place of the hard-coded literals (`:385-390`, `:401-404`). WIRED+LIVE
  now: `adversarial_convergence_score`, adversarial `report_path`. WIRED-but-default-clean pending
  producer: the 3 booleans + per-class counts (child is score-only, R2). Producer emission of real
  counts/booleans is FOLLOW-ON OQ-PRODUCER (sc-adversarial surface), NOT this task. Headline TEST
  injects `regression_present=True` to prove the route to HALTED. Consistent with the GOAL ("map
  into build_reflect_contract" = plumbing + test).
- **GAP-4 (HALT vs DEGRADE):** convergence drives ONLY the DEGRADE rung (`null-convergence`
  `contract.py:284`); regression drives the HALT rung (`regression_present is True`
  `contract.py:315`). Do NOT auto-derive `regression_present` from a low score (would misroute
  reviewer DISAGREEMENT as a found REGRESSION). `regression_present` is an explicit seam field,
  default False; null-convergence DEGRADE fallback preserved via `convergence_score=None`.
- **GAP-1 (backward-compat):** widen P1-P5 in `ensemble.py`; `runner.py:425` (P6) is insulated
  (positional `config`, no score-fn kwarg). Only mechanical test break = `_const_score` return type
  (T1, `test_ensemble_stub_integration.py:39-41`), transitively covering injection sites :93/:331/:356.
  The two autospec spies (:420/:445) and U10 (`test_ensemble_unit.py:262-291`) / U5 (:170) do NOT
  break if `extract_convergence_score`/`parse_adversarial_contract` keep their signatures.
- **GAP-5 (FR-RH2.7 proof):** (A) `git diff -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py`
  MUST be empty (place `AdversarialResult` in `ensemble.py` to keep `models.py` byte-clean); (B) I1
  clean-path PASS + U6 frozen-ordering stay green; (C) `uv run pytest tests/cli/reflect tests/swarm -q`
  all green. Combined gate:
  `git diff --quiet -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py && uv run pytest tests/cli/reflect tests/swarm -q`.
- **GAP-FIX (path):** prior task file is NESTED —
  `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`
  (verified exists; flat sibling verified missing). OI-1 table, QA CRITICAL #2, and consolidated-findings
  artifacts all under that nested dir (all verified to exist).

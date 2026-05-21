# Phase 1B — Adversarial Debate + HYBRID Synthesis

**Orchestrator:** Debate-Orchestrator (neutral; non-participant)
**Date:** 2026-05-21
**Mode:** 3-round structured adversarial transcript over Theses T1 / T2 / T3
**Inputs:** `phase1/A1-module-audit.md`, `phase1/A2-thesis-never-authored.md`, `phase1/A3-thesis-removed.md`, `phase1/A4-thesis-belong-elsewhere.md`
**Ground-truth injections (non-debatable):**
1. `src/superclaude/cli/eval/` is **entirely untracked** in git. `git log -S` pickaxes inside this directory are necessarily empty — this is a tautology of an uncommitted working tree, not evidence about authorship.
2. Branch-trace gate **PASSED** in Phase 1A. Lines 1453 and 1461 are the only reachable lines before the first NameError at 1467, and both fire only under operator-supplied bad flags. Under a default invocation, control flow reaches 1467 unconditionally.

**Read-only.** No source-tree edits performed.

---

## Thesis statements (compact)

- **T1 — Never Authored.** The 11 names were planned but no implementation was ever written. The `eval_run` call sites + tests are a forward-dependency scaffold for the unwritten T04.10 deliverable.
- **T2 — Authored Then Removed/Renamed.** The 11 names once had definitions (in `cli/eval/` or elsewhere) and a refactor removed or renamed them while missing the internal call sites.
- **T3 — Belong Elsewhere (Consolidation).** The 11 names are stranded placeholders; the underlying semantic work already exists in sibling modules and the call sites should be rewired (with thin glue) rather than authored fresh.

---

## Round 1 — Presentation

### Voice T1 (opening, drawing on A1 + A2)

The structural evidence converges on a single reading: the `eval_run` body was authored as a wiring contract against a planned helper layer that never landed. A1 §1 sweeps the entire `src/superclaude/cli/eval/` tree (21 modules) and the full `src/` + `tests/` tree and finds **0 of 11** symbols defined anywhere; this is not a localized miss but an exhaustive null. A1 §1.1 layers on the decisive structural corroboration: five test files (`test_single_command.py:134-160`, `test_exit_codes.py:29-113`, `test_no_pty_exclusion.py:266-337`, `test_no_mcp_skip.py:30-528`, `test_validation_commands.py:166-177`) enumerate the same 11 names verbatim and **skip-gate themselves with docstrings tagging the names as "T04.10 deliverables… not yet landed."** This is forward-looking diction; no test author could have framed a regression as a forward dependency.

The checkpoint trail uses uniformly authoring diction. A2 §2.2 quotes `CP-P04-END.md:108-116` verbatim: *"Either (a) **author the eleven missing helper symbols** … or (b) rewrite the body to use already-landed helpers."* The verb is *author*, not *restore* / *re-add* / *merge back*. A2 §2.3 quotes `D-0081/notes.md:105-110`: *"T04.10 is the run-loop closure that **adds** `_new_run_id`, `_run_one_spec`, `_compute_run_stats`, and the three terminal exit-code constants. **Once T04.10 lands:** Tests 5 and 6 un-skip automatically."* The forward-conditional clause "Once T04.10 lands" is incompatible with a removal narrative — a project that lost work would describe the remediation as restoration, not first-time authorship. The live follow-up ticket sits in `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/` (A2 §2.5), and **no companion record exists in `.dev/tasks/done/`** for the helper authorship — the absence-of-done is itself diagnostic.

The smoking-gun structural signal is the **import-shape coherence** documented in A1 §2.2. Of the twelve F401 unused imports, seven (`datetime, timezone, HomeContainmentViolation, HomeIsolation, RunCounts, RunTotals, EvalRunner, LifecycleExecutor`) form a one-to-one, type-coherent match against the seven of-eleven missing helpers that would consume / return exactly those types. `RunCounts + RunTotals` would be the return tuple of `_compute_run_stats`; `datetime + timezone` are the building blocks of `_utc_iso_now`; `HomeIsolation` + `HomeContainmentViolation` would be the construction surface inside `_run_one_spec`; `EvalRunner + LifecycleExecutor` would be the return surface of `_resolve_executor_factory`. An author pre-staged precisely the imports they planned to consume — then never wrote the consumers. The runtime evidence is consistent across nine independent invocations (A2 §2.6) and all converge on `NameError: name '_new_run_id' is not defined` at the unchanged call site — incompatible with the `ImportError` shape that T3 would predict for a sibling-relocation story and incompatible with any T2 deletion event that would have left a git trace. **T1 confidence: 0.82.**

### Voice T2 (opening, drawing on A3 — steel-manned despite A3's own concession)

The honest opening: A3 itself reports confidence 0.03 and explicitly concedes Thesis 2 is falsified. The steel-man defense exists only inside one narrow channel that A3 surfaces and rejects in §3: the eval tree is staged as work-in-progress; an author could have written the 11 helpers in an unsaved editor session and then deleted them from the buffer before the first commit. That "intra-session remove" leaves no git trace by construction. Combined with the fact that `git blame` is unavailable on an untracked file (A3 §2.3), there is a measurable gap in the recorded history — a gap T2 can in principle occupy.

A second steel-man channel: a force-pushed history-rewritten branch could have once held the helpers and been garbage-collected from every clone. A2 acknowledges this in its own §5 weakest-point: the pickaxe was scoped to `src/superclaude/cli/eval/` only, leaving room for a relocated-and-deleted alternate home (e.g., `src/superclaude/cli/_eval_helpers.py`). If such a path ever existed, the `git log -S` results inside `cli/eval/` would be vacuously empty even under a deletion narrative. The probability mass T2 deserves is therefore the joint probability of (editor-buffer deletion) ∪ (relocated-and-force-deleted file) — both narrowly possible, neither directly visible.

The mortal weakness — which the orchestrator's ground-truth injection makes inescapable — is that **the entire `src/superclaude/cli/eval/` directory is untracked**. T2 requires *some* historical artifact of prior authorship to be true. The git history of this directory does not exist as a corpus that could ever contain evidence for or against T2; the question is malformed against the available record. Worse, the corroborating narrative channel (`CP-P04-END`, `D-0081`, test docstrings) uses authoring diction throughout — no checkpoint uses the words "removed", "renamed", "extracted", "consolidated", or "relocated" in connection with these specific symbols (A3 §2.8). The single grep hit on "consolidate" in `CP-P04-END.md:115` is the *remediation recommendation*, not a historical event. **T2 confidence: 0.02** — reserved entirely for the unfalsifiable editor-buffer case, which is worthless as an explanation.

### Voice T3 (opening, drawing on A4)

T3's case is not the strong "drop-in" version A4 itself rejects — that version is dead on the signature-delta evidence. T3's true case is an **intent claim**: the author of `eval_run` was reaching toward sibling consolidation, dragged in exactly the sibling imports they would have needed to delegate to (`HomeIsolation, HomeContainmentViolation, RunCounts, RunTotals, EvalRunner, LifecycleExecutor`) and then stranded the call sites with private placeholder names. The F401 unused-imports are the smoking gun A4 §F surfaces: **six semantically-loaded sibling imports** sit unused. That pattern is consistent with "I was reaching toward siblings, got interrupted, never came back" and inconsistent with both T2 (rename ghosts would leave deletion traces) and a pure T1 reading (a pure-authoring author would have imported stdlib primitives, not sibling helpers).

The project-convention evidence is structural and load-bearing. A4 Evidence G quotes `commands.py:1213` showing `eval_describe` calling sibling helpers (`describe_suite`, `render_describe_json`, `render_describe_yaml`, `resolve_suite_manifest`) **directly** — no private re-aliasing, no `_local_helper_wrapping_describe_suite()` placeholders. This is the canonical pattern in `commands.py`. `eval_run` is the outlier that broke the pattern. For the symbols that have sibling near-equivalents — `_new_run_id` ↔ `artifact_layout.compose_run_id` (A4 Evidence A), `_default_output_dir` ↔ `artifact_layout.compose_run_dir` (Evidence B), `_run_one_spec` ↔ `runner.EvalRunner.run` (Evidence C) — the fix is wiring + glue, not net-new authoring of orthogonal logic.

T3 concedes openly what it cannot win. The three `RUN_*_EXIT_CODE` constants belong in `commands.py` per the convention of the eight existing `*_EXIT_CODE` constants and the design-spec §4 dictated values (A4 Evidence E); these are not consolidation candidates. Likewise `_compute_run_stats` (Evidence #7) has **no sibling aggregator** — the dataclasses `RunCounts` and `RunTotals` exist, but no `from_outcomes` classmethod or sibling free function aggregates them; this is genuine new authoring. The honest T3 read is **directional, not absolute**: it explains *why* the placeholders look the way they do (sibling-reaching author intent) and prescribes *how* to fix the consolidation-amenable subset, but it does not displace T1 for the genuinely-new-authoring subset. **T3 confidence: 0.30** as a pure thesis; ~0.50 as one half of a HYBRID.

---

## Round 2 — Cross-examination

### T1 attacks T3's weakest claims

T3's weakest claim is that "the author intended sibling delegation" is the dominant explanation. The evidence does not support dominance — it supports a roughly 5-of-11 / 6-of-11 split. Two crucial weak points expose this:

**Signature mismatches across the board.** A4's own table reports **0 of 11** symbols have HIGH-confidence sibling equivalents; 3 are MED (`_new_run_id`, `_default_output_dir`, `_run_one_spec`); 4 are LOW (`_resolve_executor_factory`, `_utc_iso_now`, `_can_install_signal_handler`, `_format_run_summary_line`); and 4 are NONE (`_compute_run_stats`, RUN_*_EXIT_CODE × 3). A4 concedes in its own Pre-empting-A2 paragraph: *"out of 11 symbols, **zero** have a clean drop-in sibling equivalent."* The MED rows require call-site reshuffling (e.g., `_new_run_id` cannot wire to `compose_run_id` without moving the run-id computation 145 lines down to where `started_iso` is computed at line 1612). The "consolidation" framing systematically understates the authoring labor: even the "wireable" rows need 2-30 lines of glue (per A1 §4 — `_run_one_spec` alone is ~30-60 lines of orchestration), and the "non-wireable" rows are 100% net-new.

**`RUN_*_EXIT_CODE` convention is decisive against T3 for 3-of-11.** The eight existing `*_EXIT_CODE` constants in the tree (`HARD_FAIL_EXIT_CODE = 2` at `commands.py:550`, `SCRATCH_ROOT_VIOLATION_EXIT_CODE`, `SUITE_NOT_FOUND_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`, `EVAL_NOT_FOUND_EXIT_CODE`, `COVERAGE_GATE_FAILED_EXIT_CODE`, `DISK_BUDGET_EXCEEDED_EXIT_CODE`, `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`) all live in their domain modules, and the consumer `commands.py` imports them by name. The naming convention `RUN_*_EXIT_CODE` directly mirrors this pattern — these three constants belong **in commands.py** (or in a hypothetical `commands.py`-adjacent module), authored by hand against design-spec §4's `0 / 1 / 2 / 3` mapping. They cannot consolidate to a sibling because no sibling has the relevant domain semantics (run-level outcome). A4 concedes this row openly. The five tests that explicitly `mock.patch("...commands._run_one_spec", ...)` pin the placeholder names as `commands.py`-local module attributes — they treat the placeholder surface as the contract surface, which is T1 territory, not T3 territory.

### T3 attacks T1's weakest claims

T1's weakest claim is that the eleven symbols are purely authoring work that ignores the existing sibling layer. The F401 evidence directly refutes the "pure authoring" framing:

**The F401 sibling-import cluster proves consumption intent.** Per A1 §2.2 and A4 Evidence F, six F401 unused imports are not stdlib idioms (which a pure-authoring T1 author would have chosen) but sibling helpers: `HomeIsolation`, `HomeContainmentViolation`, `RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`. A "never authored" reading explains *why* the placeholders exist but does **not** explain *why* those specific six sibling imports were dragged in. The most parsimonious reading is that the placeholder names are intended *thin wrappers* that delegate to those sibling imports — i.e., they are HYBRID, not pure T1. Pure T1 would predict the author would have imported `secrets.token_hex`, `datetime.now`, `threading.main_thread`, and authored fully-local logic. Instead the author imported the *return types* of the sibling-backed helpers, indicating delegation intent.

**The `eval_describe` precedent + the `compose_run_id` test consumer prove project convention is direct sibling-helper invocation.** `commands.py:1213` (A4 Evidence G) shows `eval_describe` calling siblings directly. The test file `tests/cli/eval/test_artifact_reproducibility.py:67` (A4 Evidence A) imports and consumes `compose_run_id(_STARTED_AT, _SUITE_NAME)` — proving the sibling helper is the established contract. If T1 were the pure answer, the `eval_run` body would either (a) follow the `eval_describe` direct-call pattern (no placeholders) or (b) import stdlib primitives only. It does neither. The placeholder + sibling-import combination is a HYBRID signature: the author planned thin wrappers around sibling helpers and never wrote the wrappers. T1 alone cannot account for this.

### T1 + T3 jointly dismiss T2

T2 is structurally falsified by the ground-truth injection. The entire `src/superclaude/cli/eval/` tree is untracked; `git log -S` returns vacuously empty for every symbol both inside the tree and repo-wide (A3 §2.1); no `--diff-filter=D` deletions exist under the tree (A3 §2.4); no F401 imports show a rename trail (A3 §2.7); and no checkpoint uses removal-diction (A3 §2.8). The only T2 survivor is the unfalsifiable editor-buffer-history defense, which A3 itself dismisses. A2's §5 caveat about relocated-and-force-deleted alternate homes was probed by A3's repo-wide pickaxe (`git log --all --oneline -S "<name>"` *unscoped*) and returned zero hits across all eleven names. T2 is closed. Remaining probability ≤ 0.02 reserved for unfalsifiable narrow channels.

---

## Round 3 — Synthesis: the HYBRID classification

The "single winner" framing forces a false choice. The evidence supports a **HYBRID T1 + T3** verdict where each symbol gets an individually-classified disposition:

- **T1 (net-new, must be authored in commands.py)** for symbols that have no sibling near-equivalent and need fully-local logic + design-spec-dictated values.
- **T3 (wrap/delegate to a verified sibling helper)** for symbols where a sibling exists with semantically-equivalent behavior and the rewrite is mechanical (reorder call site, change argument list).
- **T1+T3 (thin wrapper authored locally that delegates to a sibling)** for symbols where the sibling exists but signature adaptation is required — the wrapper is net-new code but the body delegates to the sibling.

### Per-symbol verdict table

| # | Symbol | Verdict | Home (proposed) | Equivalent / target (if any) | Notes |
|---|---|---|---|---|---|
| 1 | `_new_run_id` | **T1+T3** | thin wrapper in `commands.py` | `artifact_layout.compose_run_id(started_at, suite_name)` at `artifact_layout.py:139` | Sibling exists with deterministic `<HHMMSSZ>-<8-hex>` shape; wrapper must compute `started_iso = _utc_iso_now()` first then call `compose_run_id(started_iso, parsed.name)`. CP-P05-END remediation prescribes exactly this. INFERENTIAL: the F401 of `datetime, timezone` corroborates `_utc_iso_now` is the missing intermediate. |
| 2 | `_default_output_dir` | **T1+T3** | thin wrapper in `commands.py` | `artifact_layout.compose_run_dir(output_root, started_at, suite_name)` at `artifact_layout.py:162` | Sibling takes `(output_root, started_at, suite_name)` and derives run-id internally; wrapper must source `Path.cwd()` (or scratch-root) + `started_iso` + suite name. **Open question (Q4 from A1):** scratch-root allowlist semantics — `Path.cwd()` may not be in allowlist, so wrapper may need tighter default than the helper signature suggests. |
| 3 | `_resolve_executor_factory` | **T1+T3** | thin factory in `commands.py` | `runner.LifecycleExecutor` Protocol (`runner.py:136`) + `claude_process.ClaudeProcessAdapter` (`claude_process.py:107`) | No zero-arg factory exists in tree. Wrapper is `def _resolve_executor_factory() -> Callable[[], LifecycleExecutor]: return lambda: ClaudeProcessAdapter(...)`. F401 of `EvalRunner, LifecycleExecutor` corroborates the intended return surface. |
| 4 | `_run_one_spec` | **T1+T3** | new ~30-60 LOC closure in `commands.py` | `runner.EvalRunner.__init__` + `.run(spec)` (`runner.py:754, 823`); `artifact_layout.allocate_per_eval_paths`; `isolation.HomeIsolation` | Genuinely new orchestration glue — but every primitive (per-eval path allocation, HOME construction, executor instantiation, runner construction, spec execution) exists in siblings. F401 of `HomeIsolation, HomeContainmentViolation, EvalRunner, LifecycleExecutor` are precisely the construction surface this glue needs. Tests `mock.patch("...commands._run_one_spec")` pin the symbol as `commands.py`-local, confirming the wrapper home. |
| 5 | `_utc_iso_now` | **T1** (with stdlib delegation, no sibling) | one-liner in `commands.py` | None — stdlib `datetime.now(timezone.utc).isoformat(...).replace("+00:00", "Z")` | F401 of `datetime, timezone` is the smoking gun: imports were pre-staged for exactly this helper. Pure local authoring. Could arguably be inlined twice (lines 1612, 1636) but the helper form aids testability. |
| 6 | `_can_install_signal_handler` | **T1** (with stdlib delegation, no sibling) | 2-line probe in `commands.py` | None — stdlib `threading.current_thread() is threading.main_thread()` | `SignalHandlerInstaller.install()` raises `ValueError` from non-main thread (`signal_handler.py:203-206`) but no boolean probe exists. Net-new but trivial; could alternatively be a try/except guard. **Open question:** is the probe-vs-try-except choice spec-bound or implementer's discretion? |
| 7 | `_compute_run_stats` | **T1** (genuinely new authoring) | new aggregator in `commands.py` (or `models.py` classmethod — see open Q5) | None — `models.RunCounts` and `models.RunTotals` are plain dataclasses with no `from_outcomes` aggregator | F401 of `RunCounts, RunTotals` confirms return-tuple intent matches call site `counts, totals = _compute_run_stats(outcomes, manifest_n=...)` at line 1642. **Open question (Q5 from A1):** should this live as `RunCounts.from_outcomes` / `RunTotals.from_outcomes` classmethods on `models.py` rather than in `commands.py`? Design-spec is silent; either home is defensible. |
| 8 | `_format_run_summary_line` | **T1** (genuinely new authoring) | one-liner in `commands.py` | `reporter.Reporter(summary).to_markdown()` at `reporter.py:150` and `run_report.render_summary_markdown` at `run_report.py:137` — both wrong granularity (full documents, not one-line operator banner) | Net-new operator-stdout helper. Call site at 1671 is under `--verbose` guard for a single-line `click.echo`. F-string format; ~1-3 lines. |
| 9 | `RUN_INTERRUPTED_EXIT_CODE` | **T1** (net-new constant) | module-level in `commands.py` | None — design-spec §4 mandates value `3` | Convention matches eight existing `*_EXIT_CODE` constants; integer value design-spec-dictated. No sibling can own this — domain semantics is run-level outcome, which is `commands.py`'s domain. |
| 10 | `RUN_FAILURES_EXIT_CODE` | **T1** (net-new constant) | module-level in `commands.py` | None — design-spec §4 mandates value `1` | Same as #9. |
| 11 | `RUN_CLEAN_EXIT_CODE` | **T1** (net-new constant) | module-level in `commands.py` | None — design-spec §4 mandates value `0` | Same as #9. The fact that even these trivial 3-line constants never landed is probative (A2 §7 Open Q3): if any prior authorship had ever existed, the constants would almost certainly survive somewhere. Their joint absence corroborates the never-authored origin. |

### Verdict distribution across symbols

- **Pure T1 (net-new):** 7 — `_utc_iso_now`, `_can_install_signal_handler`, `_compute_run_stats`, `_format_run_summary_line`, and the three `RUN_*_EXIT_CODE` constants.
- **HYBRID T1+T3 (thin wrapper that delegates to sibling):** 4 — `_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`, `_run_one_spec`.
- **Pure T3 (drop-in sibling import / direct rewire, no wrapper):** 0 — the signature-delta evidence rules this out for every row.

### Why HYBRID is the right frame (not pure T1)

A pure-T1 reading would predict the author would write fully-local helpers backed by stdlib primitives. Instead, the F401 cluster shows the author pre-staged six sibling imports for consumption — meaning *at least four* of the missing helpers were planned as wrappers around those sibling imports. The HYBRID frame captures: (a) the **origin** is never-authored (T1) — all 11 symbols are first-time work, not regressions; (b) the **implementation** for 4-of-11 is wrap-and-delegate (T3) using verified sibling helpers; and (c) the implementation for 7-of-11 is fully local but mostly trivial (stdlib idioms + design-spec-dictated constants + a small aggregator + a one-line formatter). The CP-P05-END remediation language (*"replace the undefined call with `compose_run_id(started_at=_utc_iso_now(), suite_name=suite)` or author a thin `_new_run_id()` wrapper that delegates to `compose_run_id`"*) already endorses the HYBRID approach for the dominant blocker.

---

## Verdict — final probability distribution

| Disposition | Probability |
|---|---|
| **T1-pure** (all 11 authored locally with stdlib only) | 0.10 |
| **T3-pure** (all 11 consolidate to siblings, no new authoring) | 0.02 |
| **HYBRID T1+T3** (per-symbol mix: 7 net-new + 4 wrappers, as table above) | **0.86** |
| **T2** (authored then removed/renamed) | 0.02 |

Total: 1.00.

**Confidence in the chosen winner (HYBRID): 0.86.**

The residual 0.14 mass is distributed: 0.10 for a pure-T1 outcome if the design-spec or TDD turns out to forbid sibling delegation for stylistic reasons (low prior — no such constraint is documented), 0.02 for T3-pure if the design-spec turns out to mandate `RunCounts.from_outcomes` / `RunTotals.from_outcomes` classmethods that displace `_compute_run_stats` and similar sibling promotions for `_format_run_summary_line` (this would still leave the `RUN_*_EXIT_CODE` constants as net-new and so isn't strictly T3-pure), and 0.02 for T2 reserved for the unfalsifiable editor-buffer channel.

### Decisive evidence pointer

**`.dev/releases/current/cliEval/checkpoints/CP-P04-END.md:108-116`:**
> *"Either (a) **author the eleven missing helper symbols** (`_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now`, `_can_install_signal_handler`, `_compute_run_stats`, `_format_run_summary_line`, …) or (b) rewrite the body to use already-landed helpers."*

The dual-option phrasing — *author* OR *rewrite to use already-landed helpers* — is precisely the HYBRID frame the project authors already endorsed. Option (a) is the T1 axis; option (b) is the T3 axis; the synthesis is per-symbol selection between (a) and (b) based on sibling availability. The remediation is HYBRID by construction.

Corroborating: **`src/superclaude/cli/eval/commands.py:38-86`** import block with 12 F401 unused-imports, of which 6 are sibling helpers (`HomeIsolation`, `HomeContainmentViolation`, `RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`) — the type-coherent pre-staging that no other thesis can explain.

---

## Implications for Phase 2 solution design

The HYBRID conclusion imposes the following constraints on Phase 2A solution ideation:

1. **`RUN_*_EXIT_CODE` constants MUST be authored in `commands.py` (not imported from any sibling).** Design-spec §4 dictates values `0/1/3` and the convention of the eight existing `*_EXIT_CODE` constants is in-module-or-domain-module declaration with `commands.py` as consumer. A Phase 2 proposal that imports these from a new `exit_codes.py` sibling would be out-of-convention; a proposal that imports them from any existing sibling would lack a defensible home.

2. **`_run_one_spec` MUST be authored as `commands.py`-local glue (not relocated to `runner.py`).** Five test files use `mock.patch("...commands._run_one_spec", ...)` (A4 Evidence H) which codifies the symbol as a `commands.py` module attribute. Moving the helper to `runner.py` would silently break those test mocks. Phase 2 must respect the test-contract surface.

3. **`_new_run_id` and `_default_output_dir` REQUIRE call-site reordering (or wrapper authorship) — they cannot be replaced by direct `compose_run_id` / `compose_run_dir` calls without moving `started_iso` computation 145 lines up.** The current ordering computes `run_id = _new_run_id()` at 1467 before `started_iso = _utc_iso_now()` at 1612. Phase 2 must either (a) reorder to compute `started_iso` first and call siblings directly, or (b) author thin zero-arg wrappers that compute `started_iso` internally. Decision is stylistic but must be made up-front.

4. **The F401 unused-imports cluster MUST be cleared in lockstep with helper authorship.** Six sibling imports (`HomeIsolation`, `HomeContainmentViolation`, `RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`) become consumed once the HYBRID wrappers land; two (`datetime`, `timezone`) become consumed once `_utc_iso_now` lands. Remaining F401s (`os`, `secrets`, `Sequence`) are stale and must be removed independently. A Phase 2 proposal that authors helpers without clearing F401s leaves the ruff gate red and re-fails the sprint.

5. **`_compute_run_stats` home decision (Q5) is load-bearing and must be resolved up-front.** If the helper lives as `RunCounts.from_outcomes` + `RunTotals.from_outcomes` classmethods on `models.py`, the call site at 1642 becomes a two-call rewrite; if it lives as a `commands.py`-local aggregator, the call site stays one call. The HYBRID per-symbol verdict is agnostic but Phase 2 must commit. Recommend deferring to the design-spec / TDD; if silent, default to `commands.py`-local (matches `_run_one_spec` placement and test-mock convention).

---

## Open questions surviving the debate

These will frame Phase 2A solution ideation:

1. **Q5 from A1 — `_compute_run_stats` home.** Should this be a `commands.py`-local aggregator or `RunCounts.from_outcomes` / `RunTotals.from_outcomes` classmethods on `models.py`? Equally, should `_format_run_summary_line` live in `commands.py` or be promoted to a `reporter.py` / `run_report.py` method? Neither design-spec nor TDD pins this; the HYBRID verdict is agnostic.

2. **Q4 from A1 — `compose_run_dir` + scratch-root layering.** `compose_run_dir` returns `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>`. The call site at 1469 is *before* scratch-root resolution at 1473. Does `_default_output_dir` need to honor the scratch-root allowlist? If yes, the wrapper is non-trivial and may need to depend on `resolve_scratch_root` output. Phase 2 must answer the layering question before authoring the wrapper.

3. **`_new_run_id` API choice.** Two viable shapes: (a) zero-arg wrapper `_new_run_id() -> str` that internally computes `_utc_iso_now()` + reads suite name from outer scope (closure capture); or (b) direct inlining of `compose_run_id(started_iso, parsed.name)` at line 1467 after reordering `started_iso` computation. The CP-P05-END remediation prescribes (a); the `eval_describe` precedent suggests (b). Project convention is split.

4. **F401 cleanup ordering — atomic or staged?** Should helper authorship + F401 cleanup land as a single atomic commit (cleaner ruff gate, larger blast radius) or as staged commits (smaller blast radius, intermediate ruff-red states)? The release process may have constraints from the P4/P5 sprint-gate definition.

5. **`_can_install_signal_handler` probe-vs-try-except shape.** Two equivalent implementations: (a) boolean probe `threading.current_thread() is threading.main_thread()` called before `SignalHandlerInstaller.install()`; or (b) try/except `ValueError` wrapping the install call. Design-spec is silent; behavioral semantics are identical. Phase 2 must pick a shape — the choice has minor implications for test mocking (probe is mockable; try/except is not).

---

## Process notes

- **Round-1 and round-2 evidence** uses verification-tier citations (file:line + verbatim quotes from A1 / A2 / A3 / A4 artifacts).
- **Round-3 synthesis** uses discovery-tier inferential leaps in three places, flagged INFERENTIAL inline: (i) the F401 type-shape coherence argument (mapping six sibling imports to four HYBRID wrappers); (ii) the "joint absence of trivial constants is probative for never-authored" argument carrying T2 → 0.02; (iii) the test-mock-codifies-contract argument anchoring `_run_one_spec` and friends to `commands.py`-local placement.
- The orchestrator did not participate in debate; per-side voices were composed strictly from the four Phase 1A artifacts plus the two ground-truth injections from the prompt header.
- No source-tree edits performed; this is a read-only artifact.

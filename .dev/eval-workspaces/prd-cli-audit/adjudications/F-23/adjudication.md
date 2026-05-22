# F-23 Adjudication — `_filter_research_for_sections` keyword heuristic

**Target finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-23-filter-research-keyword-heuristic.md`
**Subject code**: `src/superclaude/cli/prd/filtering.py:331-366`
**Preliminary severity**: MEDIUM
**Mode**: B (3 personas → convergence), READ-ONLY

---

## Re-verification (ground truth)

1. **Function exists as described.** `src/superclaude/cli/prd/filtering.py:331-366` matches the finding's quoted body verbatim — substring keyword matching after `re.sub(r"\(.*?\)", ...)` and `len(w) > 2` filter, with an early-return short-circuit on any hint containing `"all research"` (filtering.py:349-351).

2. **"all research" short-circuit confirmed.** Two of the nine `_DEFAULT_SYNTHESIS_MAPPING` entries trigger it: `synth-07-metrics-risk-impl.md` (filtering.py:274) and `synth-09-resources-maintenance.md` (filtering.py:302). The remaining seven entries route through the brittle keyword path. The finding correctly identifies that `"per-area research files"` (filtering.py:234) reduces to `['per', 'area', 'research', 'files']` — no realistic filename like `01-pm-agent-architecture.md` will match.

3. **CRITICAL — function has zero callers.** A repository-wide search (`grep -rn "_filter_research_for_sections\|filter_research"` across `src/` and `tests/`) returns only the definition site at `filtering.py:331`. The function is never imported, never invoked, and has no tests. `tests/cli/prd/test_filtering.py` does not exercise it.

4. **Call-chain trace to `build_synthesis_prompt`.** `executor._build_synthesis_steps` (executor.py:752-762) emits step tuples that name `"build_synthesis_prompt"` as the builder string. Steps flow through `_execute_step` → `_run_subprocess_step` → `_build_prompt(builder_name)` (executor.py:442, 486, 929-951). `_build_prompt` invokes the builder as `builder_fn(self._config, context_summaries=...)` and falls back to `builder_fn(self._config)` on `TypeError`. **No path passes `research_files`, `template_sections`, `output_path`, or `template_path` to `build_synthesis_prompt`** (prompts.py:747-792 requires all four positional). Both attempted invocations will raise `TypeError`; the bare `except TypeError` (executor.py:949) only catches the first attempt, so the second `TypeError` propagates out of `_run_subprocess_step` and crashes the synthesis step.

5. **Filter is not load-bearing at all in current code.** The synthesis prompt builder is reachable from the executor, but the executor's dispatch shape is incompatible with the builder's signature, AND nothing filters research files before the call would happen. The keyword heuristic at `filtering.py:331-366` is dead code relative to the current execution path.

---

## Persona analyses

### Analyzer — reproducibility & silent-drop behavior

**As a unit of pure logic**, the finding's reproduction sketch is correct. Given `research_files = [Path("01-pm-agent-architecture.md"), Path("02-confidence-checker.md"), Path("03-reflexion-pattern.md")]` and `mapping_entry["source_research"] = ["per-area research files", "user flows", "gaps log"]`:

- Stem normalization: `01-pm-agent-architecture.md → "01 pm agent architecture"`.
- Keywords after parenthetical strip + `len > 2`:
  - `"per-area research files"` → `['per', 'area', 'research', 'files']`
  - `"user flows"` → `['user', 'flows']`
  - `"gaps log"` → `['gaps', 'log']`
- Substring tests: none of those keywords appear in `"01 pm agent architecture"`, `"02 confidence checker"`, or `"03 reflexion pattern"`. → `matched = []`.

So *if* this function were on the live path, it would silently return `[]` and `build_synthesis_prompt` would render `"Research files to read:\n"` followed by nothing (prompts.py:754, 759-760). The synth agent would be prompted to read no files.

**However**, repository search shows the function is uninvoked (re-verify #3). The "silent file drop" cannot occur until/unless someone wires it in. The bug is latent, not active.

A second silent-drop edge does exist: `"all research files"` matches the short-circuit (`"all research" in "all research files"` is True at filtering.py:350), but `"all research"` alone (no plural) would also match — fine. Less obvious: a hint string like `"recall research"` would also short-circuit because `"all research"` is a substring of `"recall research"`. Inspecting all nine mapping entries shows none of them currently trigger this collision, so it's a theoretical lurking bug rather than an observed one.

**Analyzer verdict**: Heuristic is brittle and would silently produce empty results on realistic inputs, but is dead code today. Reproducibility-as-pure-function = HIGH; reproducibility-in-pipeline = ZERO.

### Refactorer — blast radius

`grep -rEn "kw in fname|keyword.*lower|in.*\.lower\(\).*for"` across `src/` surfaces several substring-keyword filters. Triaging by criticality of decision:

| Site | Decision type | Risk | Notes |
|---|---|---|---|
| `cli/prd/filtering.py:362` | Routes research evidence to synthesis agent | HIGH (silent drop) | The F-23 subject. Dead code currently. |
| `cli/prd/gates.py:188, 206` | Detects parallel-execution keywords in roadmap text | LOW | Gate ASSERTS presence; false negative = gate fail (loud), not silent. |
| `cli/pipeline/state_detector.py:222` | Maps text to pipeline state | LOW-MED | Detector emits states from substrings; bounded to known vocabulary. |
| `cli/audit/escalation.py:104, 190-192` | Decides whether evidence is "refs"/"imports"/"test"/"config" | MED | Same anti-pattern (substring `in e.lower()`); used for escalation routing, not gating. |
| `execution/reflection.py:252-255` + `execution/self_correction.py:200-206, 371-375` | Token-set keyword overlap for past-failure matching | LOW | Set-overlap not substring; explicit `>= threshold` checks. Defensible. |

**Blast radius**: The same anti-pattern (loose `kw in haystack` filename heuristics with no fallback) appears once in critical evidence-routing code (the subject of F-23) and once in audit escalation (`audit/escalation.py:104`). Other sites either fail loudly or use stronger matching primitives.

**Refactorer verdict**: Pattern is localized. F-23 is the canonical instance; `audit/escalation.py:104` is a near-cousin worth a follow-up scan but is bounded by being a binary classifier, not a list-filter that can return empty.

### Architect — severity calibration

Preliminary MEDIUM rests on the chain: **brittle filter → silent empty → empty research list → synth prompt with no inputs → bad synth file → maybe caught by `min_lines=80`**.

That chain is broken at two places:

1. **The filter is never called.** Dead code can't drop evidence in production.
2. **`build_synthesis_prompt` cannot be invoked with its required arguments** by the current executor dispatch shape (re-verify #4). So even if the filter were wired, the synthesis step is already broken upstream — synthesis is reachable but will `TypeError` on first call.

Both observations argue the *current-state* severity is LOW (latent bug in dead code path), not MEDIUM.

However, F-23 also signals **architectural fragility**: when the PRD pipeline's synthesis wiring is eventually fixed (it must be — the steps are emitted into the schedule), one of two things will happen:

- A maintainer wires `_filter_research_for_sections` into `_build_prompt`'s synthesis branch as-designed. The heuristic then silently drops research, producing low-quality synth files. Gate `min_lines=80` is a thin net.
- A maintainer wires synthesis differently and the keyword filter remains dead.

So this is a **trap** for the next maintainer fixing the synthesis dispatch: the obvious wiring leads to silent quality loss. That elevates severity above pure dead-code.

**Architect verdict**: Adjusted severity LOW-MEDIUM. Current production impact is zero. Future-maintainer trap is real but contingent. Recommendation: address jointly with the synthesis-dispatch fix, not as a standalone item.

---

## Convergence

| Dimension | Analyzer | Refactorer | Architect | Converged |
|---|---|---|---|---|
| Is the heuristic brittle? | Yes (reproducible empty result) | Yes | Yes | YES |
| Does it currently drop research in production? | No (no callers) | N/A | No | NO |
| Is the anti-pattern widespread? | — | One cousin (`audit/escalation.py:104`) — bounded | — | LOCALIZED |
| Standalone fix value? | Modest (fix the heuristic) | Modest | Low (dead code) | LOW |
| Future-maintainer trap risk? | High when wired | — | High | YES |

**Verdict**: Finding is **TECHNICALLY CORRECT but MIS-CALIBRATED on impact**. The heuristic is indeed brittle and would silently drop research files; however, `_filter_research_for_sections` has no callers (`grep -rn` confirms only the definition site exists across `src/` and `tests/`), and the surrounding synthesis dispatch path (`executor._build_prompt` at executor.py:944-951) is structurally incompatible with `build_synthesis_prompt`'s signature (prompts.py:747-752), so the silent-drop scenario cannot occur in the current execution path.

**Convergence score**: 0.85 — all three personas agree on the underlying bug shape and on the calibration adjustment; minor disagreement only on whether to track separately from the synthesis-dispatch defect.

**Final severity**: **LOW** (downgraded from MEDIUM)
- Rationale: zero current production impact (dead code), bounded blast radius (one near-cousin in `audit/escalation.py:104` with weaker consequences), real but contingent future-maintainer trap.
- Promote to MEDIUM **only if** the synthesis dispatch is fixed in a way that wires `_filter_research_for_sections` into the live path without addressing the heuristic.

**Fix difficulty**: **SMALL**
- Replace the substring heuristic with an explicit mapping table (descriptor → glob/regex pattern, or descriptor → enumerated filenames) — same shape as `_DEFAULT_SYNTHESIS_MAPPING` itself, just extending it to declare which files match which descriptor.
- Alternative: add a "no-match → return all research_files (loud warning)" fallback so the failure mode is conservative-noisy instead of silent-empty.
- Either approach is <50 lines plus a unit test in `tests/cli/prd/test_filtering.py`.

**Synthesis** (one paragraph):
F-23 correctly identifies a brittle substring-keyword heuristic at `src/superclaude/cli/prd/filtering.py:331-366` that would silently return an empty research-file list for realistic filenames against descriptors like `"per-area research files"`. The finding's pure-function reproduction is sound. However, calibration to MEDIUM overstates current impact: the function has no callers in `src/` or `tests/`, and the synthesis-prompt dispatch chain (`executor._build_synthesis_steps` → `_execute_step` → `_run_subprocess_step` → `_build_prompt`) does not pass the four positional arguments `build_synthesis_prompt` requires, so synthesis steps are already broken upstream of the filter. Final severity LOW with a STRONG recommendation to bundle the fix with the synthesis-dispatch repair — leaving the heuristic in place while wiring synthesis correctly would convert a latent trap into a live silent-quality-loss bug. Fix is small (explicit descriptor → pattern mapping, or fail-loud fallback) and should be paired with a regression test using realistic research filenames.

---

## Citations

- `src/superclaude/cli/prd/filtering.py:331-366` — `_filter_research_for_sections` definition
- `src/superclaude/cli/prd/filtering.py:183-306` — `_DEFAULT_SYNTHESIS_MAPPING` (nine entries; `"all research"` at lines 274, 302)
- `src/superclaude/cli/prd/filtering.py:349-351` — `"all research"` short-circuit
- `src/superclaude/cli/prd/filtering.py:353-366` — keyword substring loop
- `src/superclaude/cli/prd/executor.py:752-762` — `_build_synthesis_steps` emits `"build_synthesis_prompt"` as builder name
- `src/superclaude/cli/prd/executor.py:929-951` — `_build_prompt` dispatch shape (only passes `config`, `context_summaries`)
- `src/superclaude/cli/prd/prompts.py:747-792` — `build_synthesis_prompt` requires `research_files`, `template_sections`, `output_path`, `template_path`
- `src/superclaude/cli/prd/gates.py:183-210` — parallel_keywords (loud-fail cousin)
- `src/superclaude/cli/audit/escalation.py:104, 190-192` — substring-classification cousin
- `tests/cli/prd/test_prompts.py:145-208` — only callers of `build_synthesis_prompt` (tests pass `research_files` directly; not via filter)
- `tests/cli/prd/test_filtering.py` — no tests for `_filter_research_for_sections` (zero references)

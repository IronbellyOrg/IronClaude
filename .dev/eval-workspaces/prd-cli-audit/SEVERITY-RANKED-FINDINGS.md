# PRD CLI Audit — Severity-Ranked Findings (Stage 4 Final)

**Date**: 2026-05-20
**Pipeline**: 6 parallel slice-audits → 39 consolidated findings → 27 per-finding adjudications → final ranking.

## Anchor verification (audit sanity check)

| Anchor bug | Description | Finding | Verdict | Convergence |
|---|---|---|---|---|
| **Bug 1** | `_STEP_ARTIFACT_FILES` missing `build-task-file` | **F-01** | REAL | 0.97 |
| **Bug 2** | Slug-templated `TASK-PRD-{slug}.md` can't sit in a static dict | **F-02** | REAL | 0.97 |
| **Bug 3** | `_tier_min_lines` defined, zero consumers — heavyweight uses 400 default | **F-03** | REAL | 0.95 |

All three anchors confirmed by independent re-verification.

---

## Severity-ranked table

Sorted: CRITICAL → LOW; within tier, by fix-difficulty ascending (quick wins first), then by convergence descending.

| ID | Severity (final) | Pattern tags | File:line | Verdict | Convergence | Fix | One-line summary |
|---|---|---|---|---|---|---|---|
| F-01 | **CRITICAL** | P1, P3, P4, P6 | executor.py:246-269 | REAL | 0.97 | **XS** | `_STEP_ARTIFACT_FILES` missing `build-task-file` — proximate halt cause |
| F-04 | **CRITICAL** | P1, P3, P4, P5, P6 | executor.py:246-251 + prompts.py (13 sites) | REAL | 1.00 | **M** | Systemic inversion — table holds stdout-only entries; 13 Write-emitting steps absent |
| F-02 | **CRITICAL** | P3, P5 | executor.py:246-293 + prompts.py:381 | REAL | 0.97 | **M** | Static dict shape can't carry slug-templated filenames; type lift required |
| F-15 | **HIGH** | P5, P7 | config.py:121-125 + prompts.py:381,405 | REAL | 0.95 | **XS** | Empty `--product` → `TASK-PRD-.md`; glob workaround masks; **must land BEFORE F-02 fix** |
| F-07 | **HIGH** | P2 | commands.py:41-45, models.py:182 | REAL | 1.00 | **XS** | `--where` flag stored on config, zero readers; LLM extraction silently controls |
| F-13 | **HIGH** | P7 | filtering.py:108-112 | REAL | 0.97 | **XS** | `#{{1,4}}` in raw string → quantifier literal; Pattern 2 of `compile_gaps` never matches |
| F-14 | **HIGH** | P5, P7 | config.py:102-117, prompts.py:919,1093 | REAL | 0.95 | **XS** | `--output` file/dir pun; `mydoc.md` becomes a directory; roadmap CLI is reference fix |
| F-16 | **HIGH** | P3, P6 | executor.py:279-291 | REAL | 0.92 | **XS** | `rglob` over `task_dir.parent` finds sibling-run artifacts; **upgraded** MEDIUM→HIGH (default sandbox triggers it) |
| F-27 | **HIGH** | P6, P9 | tests/cli/prd/test_e2e.py:224-253 | REAL | 0.95 | **XS** | Mock harness writes passing content to stream file — structurally can't catch F-01 class; **upgraded** MEDIUM→HIGH (meta-defect) |
| F-10 | **HIGH** | P4, P8 | executor.py:99-130 | REAL | 0.95 | **XS-S** | `_extract_text_from_stream_json` silently falls back to raw NDJSON; the 30/400 concealment mechanism |
| F-03 | **HIGH** | P2, P7 | gates.py:281-292, executor.py:530 | REAL | 0.95 | **S** | `_tier_min_lines` unwired; **downgraded** CRITICAL→HIGH (silent, no halt, but ships under-validated artifacts) |
| F-05 | **HIGH** | P1, P3 | executor.py:727-757, gates.py:407-432 | REAL | 0.98 | **S** | Dynamic step IDs (`investigation-1`, etc.) miss static `GATE_CRITERIA` keys; entire Stage B + fix cycles ungated |
| F-06 | **HIGH** | P2, P5, P7, P8 | executor.py (no refs), commands.py:135-191 | REAL | 1.00 | **S** | `prd resume` accepts wrong flags, emits unexecutable command, orphans `task_dir` |
| F-08 | **HIGH** | P1, P2, P7 | executor.py:587-624, gates.py | REAL | 0.95 | **S** | `required_frontmatter_fields` declared in 3 GateCriteria entries, never checked; co-fix with F-22 |
| F-12 | **HIGH** | P4, P8 | process.py:63-86, 208-219 | REAL | 0.96 | **S** | Retry catches `OSError` only; 429/503/rate-limit transients bypass exponential backoff entirely |
| F-11 | **HIGH** | P2, P4, P8 | monitor.py (all), executor.py:334 | REAL | 0.97 | **M** | `PrdMonitor` ~208 LOC dead; stall detection apparatus unused; **bundle with F-20** |
| F-09 | **MEDIUM** | P1, P8 | executor.py:957-970, models.py:220-235 | REAL | 0.95 | **XS** | `_handle_shutdown` reads `last.step.name` which is `None`; always records `halt_step="unknown"`; **downgraded** HIGH→MEDIUM |
| F-17 | **MEDIUM** | P8 | executor.py:392-409, 692-705 | REAL | 0.95 | **XS** | STRICT failures in structural-qa/qualitative-qa not propagated; exit code 0 despite contract |
| F-20 | **MEDIUM** | P4, P7, P8 | executor.py:499, models.py:190-191 | REAL | 0.95 | **XS** | `stall_timeout * 30` makes "stall ceiling" actually a wall-clock budget; bundle with F-11 |
| F-21 | **LOW-MEDIUM** | P2, P7 | config.py:120-125, prompts.py:65-101 | REAL (reframed) | 0.85 | **XS** | `PRODUCT_SLUG` LLM output is dead data; CLI always wins. **Sibling**: `PRODUCT_NAME` has same shape AND is load-bearing (new finding) |
| F-18 | **MEDIUM** | P3, P4 | executor.py:577-583, gates.py:36-53 | REAL | 0.92 | **S** | Verdict literal matcher rejects compact JSON; cascade defeats fix cycles; tolerant regex already exists at `monitor.py:33` |
| F-22 | **MEDIUM** | P2, P7 | gates.py:300-504, executor.py:531-540 | REAL | 0.92 | **S** | EXEMPT/LIGHT enforcement_tier ignored; latent (incidental min_lines=0 saves it); co-fix with F-08 |
| F-24 | **MEDIUM** | P7 | inventory.py:55-59, 163-168 | REAL (reframed) | 0.78 | **S** | `check_existing_work` returns ALREADY_COMPLETE for any `.md`; sibling `discover_synth_files` same shape |
| F-26 | **MEDIUM** | P5, P7 | config.py:108-117 | REAL | 0.88 | **S** | `--output` default falls back to `$CWD` when no `.dev/` parent; help text wrong; subdir invocation misplaces |
| F-25 | **MEDIUM-HIGH** | P4, P7, P8 | executor.py:188-203, pipeline/process.py:131,159-171 | REAL | 0.92 | **M** | Signal handler is flag-only; child in own pgrp ignores Ctrl-C; **upgraded** MEDIUM→MEDIUM-HIGH (blast radius: 4 pipelines) |
| F-19 | **LOW** | P6 | executor.py:518-532 | REAL (reframed) | 0.85 | **S** | Sentinel reads NDJSON, gate reads disk — but deterministic & fail-safe; **downgraded** MEDIUM→LOW |
| F-23 | **LOW** | P7 | filtering.py:331-366 | REAL (reframed) | 0.85 | **S** | `_filter_research_for_sections` keyword heuristic — but zero callers today; **downgraded** MEDIUM→LOW |
| F-28…F-39 | **LOW** | various | various | Stage 1 only — not adjudicated | — | — | 12 latent / cosmetic / dead-code findings; see findings-consolidated.md |

**Severity post-adjudication summary**: 3 CRITICAL, 13 HIGH, 9 MEDIUM (incl. MEDIUM-HIGH and LOW-MEDIUM), 14 LOW.

**Movement vs preliminary**: 5 downgrades (F-03, F-09, F-19, F-21, F-23), 3 upgrades (F-16, F-25, F-27). The upgrades cluster around defects that the adjudication phase proved have broader blast radius than a single-slice audit could see.

---

## Recommended remediation sequence

Grouped into PR-sized batches by file/module overlap. Order within batch matters; order across batches reflects unblock-first sequencing.

### Batch A — Dispatch & resolver (CRITICAL; unblocks pipeline)
**Single bundled PR — these findings share root cause in `_STEP_ARTIFACT_FILES` / `_resolve_step_content`.**
1. **F-15** — fix empty-slug derivation (`config.py:121`). **MUST land before F-02** to avoid `TASK-PRD-.md` corruption propagating.
2. **F-01 + F-02 + F-04** — lift artifact filename into `_STAGE_*_STEPS` tuples; teach `_resolve_step_content` and `_persist_step_artifact` to handle dynamic step families by prefix. Adjudication F-02 specifically warns: naive fix can clobber the subprocess-written file via `_persist_step_artifact`.
3. **F-10** — change `executor.py:130` from `return "\n".join(texts) if texts else raw` to unconditional `"\n".join(texts)` + diagnostic when empty. Converts silent corruption back to loud failure.
4. **F-27** — rewrite `_mock_process_factory` as two-actor mock (commentary on stream, artifact on disk); add invariant test asserting every step with an artifact is in the dispatch table. This batch ships with this test, not after.

### Batch B — Gate evaluator + tier wiring (HIGH)
**Single bundled PR — F-03, F-08, F-22 are the same defect class (PRD's bespoke `_evaluate_gate` ignores GateCriteria fields).**
1. **F-08 + F-22** — delegate `_evaluate_gate` to `pipeline.gates.gate_passed()` (which already honors `required_frontmatter_fields` and `enforcement_tier`). One refactor closes both.
2. **F-03** — wire `self._config.tier` into the gate construction path so `_tier_min_lines` is actually called.
3. **F-05** — add a step-ID normalizer that maps `investigation-3` → `investigation` before `GATE_CRITERIA.get()`. Also fixes the persistence-gap (`_persist_step_artifact`) and TUI registration (`executor.py:366-367`) siblings noted by Agent A.

### Batch C — Subprocess lifecycle (HIGH; reliability story)
**Single bundled PR — process.py, monitor.py, models.py interlocked.**
1. **F-11 + F-20** — either wire `PrdMonitor` and keep `stall_timeout` as stall semantics, or delete the dead class and rename `stall_timeout → subprocess_timeout_seconds`. Adjudication recommends the rename path (cheaper, aligns with the rest of the repo).
2. **F-12** — move retry to the post-`wait()` exit-code classification path; consume the dead `_TRANSIENT_EXIT_CODES` / `_TRANSIENT_PATTERNS`.
3. **F-25** — adopt the already-correct `eval/signal_handler.py`'s `CancellationToken` + `SignalHandlerInstaller`; have `pipeline/process.py:terminate()` be invoked from the signal path, not only from the wall-clock timeout path.

### Batch D — CLI surface & resume (HIGH)
**Single bundled PR — commands.py + config.py.**
1. **F-14** — type `--output` as `click.Path(file_okay=False, dir_okay=True)`; follow `cli/roadmap/commands.py:44-50` as reference pattern.
2. **F-07** — interpolate `config.where` into the parse-request prompt (the LLM extraction is masking, not replacement).
3. **F-06** — accept `--tier`/`--product`/`--output`/`--where` on `resume`; consume `config.resume_from` in `PrdExecutor.run()`; reconcile `task_dir` derivation so resume doesn't orphan artifacts.
4. **F-26** — add explicit project-root detection (walk up looking for `pyproject.toml`); drop the bare-CWD fallback; fix help text.

### Batch E — Quality propagation (MEDIUM; trivial)
**One PR — executor.py touch-ups.**
1. **F-17** — extract `_propagate_strict_failure()` helper, apply at the two missing call sites (`executor.py:691-705`).
2. **F-18** — replace literal `in` test with the tolerant regex already at `monitor.py:33-36`.
3. **F-09** — add `step_id` field to `PrdStepResult`; populate at construction; read at shutdown.
4. **F-13** — change `#{{1,4}}` → `#{1,4}` in `filtering.py:109`; add test exercising Pattern 2 branch.

### Batch F — Cleanup & misc (MEDIUM/LOW; opportunistic)
- **F-16** — constrain `rglob` matches via `is_relative_to(task_dir)`.
- **F-24** — port `discover_research_files`'s frontmatter+content filter to `check_existing_work` and `discover_synth_files`.
- **F-21** — remove `PRODUCT_SLUG` from prompt + presence gate (dead data); investigate the new `PRODUCT_NAME` sibling-finding surfaced during adjudication.
- **F-19** — unify sentinel detection on `gate_content` (disk-preferred).
- **F-23** — leave dormant until synthesis dispatch wiring is fixed; revisit when armed.
- **F-28…F-39** — backlog of LOW findings; sweep when touching adjacent files.

### Suggested PR sequence
1. **PR1 (Batch A)** — unblocks the headline halt; ships with two-actor mock test infrastructure.
2. **PR2 (Batch B)** — enforces gate contracts; depends on PR1's test infrastructure to gain regression coverage.
3. **PR3 (Batch C)** — fixes reliability story; independent of A/B.
4. **PR4 (Batch D)** — CLI surface; independent.
5. **PR5 (Batch E)** — quality fixes; small, can ship anytime.
6. **PR6 (Batch F)** — opportunistic cleanup; can be split.

---

## Pattern audit retrospective (P1–P9)

| Pattern | Description | Findings (count) | Notes |
|---|---|---|---|
| **P1** | Static dispatch tables grow stale | F-01, F-02, F-04, F-05, F-08, F-09, F-29, F-33, F-34 (9) | The dominant defect class. Five parallel step-list enumerations (`_STAGE_A_STEPS`, `_STEP_ARTIFACT_FILES`, `GATE_CRITERIA`, `process.py:101`, `config.py:28`) are maintained by hand. Strong evidence that a canonical step registry is overdue. |
| **P2** | Knobs defined in one place, consumed in zero | F-03, F-07, F-11, F-20, F-21, F-22, F-29, F-36 (8) | Second-largest class. The pipeline's config surface has grown faster than its consumer surface. Suggest a one-off audit pass: enumerate `PrdConfig` fields; for each, assert ≥1 reader. |
| **P3** | Dynamic identifiers vs static keys | F-01, F-02, F-04, F-05, F-16, F-18, F-31, F-37, F-39 (9) | Tied with P1 for top frequency. Slugs, dynamic step IDs, fix-cycle suffixes all collide with exact-match dispatch. |
| **P4** | Subprocess output handling | F-01, F-04, F-10, F-11, F-12, F-18, F-20, F-25, F-28, F-33, F-38 (11) | Highest count — every layer of the subprocess pipeline has at least one defect. Worth a focused refactor pass on this module. |
| **P5** | Path resolution | F-02, F-04, F-14, F-15, F-26, F-36 (6) | File-vs-directory puns, CWD-sensitive defaults, slug interpolation, broad `rglob` scope. |
| **P6** | Gate evaluation reading wrong source | F-01, F-04, F-10, F-16, F-19, F-27, F-28 (7) | The audit's headline pattern. F-27 (test gap) is the meta-explanation for why this class shipped — no test can distinguish disk read from stream read. |
| **P7** | Default values masking semantics | F-03, F-08, F-13, F-14, F-15, F-20-F-24, F-26, F-31, F-35, F-36, F-39 (~14) | Pervasive. Almost every config knob has at least one site where the default silently satisfies a contract it shouldn't. |
| **P8** | Halt/proceed control flow | F-06, F-09, F-10, F-11, F-12, F-17, F-20, F-25, F-29, F-30, F-32 (11) | Tied with P4. STRICT enforcement is inconsistent across step types; halt signals frequently demoted to logs. |
| **P9** | Test coverage gaps | F-27 (1 explicit; implicit in every anchor) | Surfaced one finding by name but is the structural enabler of every defect that shipped. The two-actor mock rewrite in PR1 is the highest-leverage single fix. |

**No pattern surfaced zero findings** — the audit hit every hunted shape. P4 and P7 are notable for being so pervasive they likely warrant module-level refactor rather than per-finding patching.

---

## Summary

- **Total findings**: 39 consolidated from 76 raw (across 6 parallel slice-audits).
- **Adjudicated**: 27 (every MEDIUM+ pre-rank).
- **Final tier counts**: CRITICAL 3 · HIGH 13 · MEDIUM 9 · LOW 14.
- **Anchor bugs confirmed**: Bug 1 (F-01), Bug 2 (F-02), Bug 3 (F-03) — all REAL with convergence ≥0.95.
- **Notable upgrades during adjudication**: F-16 (sibling-run contamination), F-25 (4-pipeline blast radius), F-27 (meta-defect causally responsible for F-01 shipping).
- **Notable downgrades during adjudication**: F-03 (silent latent, not halt), F-09 (silent wrong-data, not crash), F-19 (fail-safe & deterministic), F-21 (dead data), F-23 (no callers today).
- **New finding surfaced during adjudication**: `PRODUCT_NAME` has F-21's shape but IS load-bearing (under F-21 notes).
- **Bundled-fix opportunities**: F-08+F-22, F-11+F-20, F-01+F-02+F-04+F-10+F-27 (Batch A), F-15→F-02 sequencing constraint.

The audit hit its anchor cases, surfaced multiple sibling-class defects beyond the three known, and identified the test-harness structural defect (F-27) that explains how Bug 1 shipped past CI in the first place.

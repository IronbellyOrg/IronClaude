# QA Report — Structural Pipeline-Wiring (WS-0 inline run_cmd path)

**Topic:** WS-0 (M8/M9 corrective migration) — wire inline `swarm run` path through Wave 1→2→3
**Date:** 2026-06-16
**Phase:** report-validation (structural verification, pipeline-wiring lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Lens:** pipeline-wiring
**Stance:** adversarial — assumed ≥10 errors; verified every claim against source.

---

## Overall Verdict: PASS

All five required verification claims are TRUE with file:line evidence. No fabrication detected. The diff
references no non-existent attributes, no double contract emission, and does not alter the resume branch.
One non-blocking observation (deliberate inline-vs-resume contract-enrichment asymmetry) is documented
below as INFO, not a defect.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Inline path calls `dispatch_wave1` WITH assembled prompt + worker_spec (not `prompt=""`/`worker_spec=None`) | PASS | `commands.py:1798-1804` post-diff passes `prompt=assembled_prompt, worker_spec=inline_job.workers`. `assembled_prompt` built at `commands.py:1794-1796` via `_assemble_inline_prompt(inline_job, _read_truncated_target(inline_job))`. `dispatch_wave1` signature confirms `prompt`/`worker_spec` are valid kwargs (`dispatch.py:339, 341`). |
| 1b | Then `normalize_wave2(recipe_name="bare-review-v1", recipe_args=...)` | PASS | `commands.py:1839-1843`: `normalize_wave2(stamped_workers, recipe_name=recipe_name, recipe_args=recipe_args)` where `recipe_name = inline_job.normalization.recipe` (`commands.py:1817`). bare-review lens sets `recipe="bare-review-v1"` (research 02 §2, bare_review.py:59). Signature matches `normalize.py:500-507`. |
| 1c | Then `reduce_wave3(...)` | PASS | `commands.py:1844-1857`: `reduce_wave3(normalized_workers, mode=..., output_dir=state_output_dir, ...)`. Signature confirmed `reduce.py:555-577`. |
| 2 | `reduce_wave3` called ONCE; NO separate explicit `emit_contract` call | PASS | Whole-file grep: `reduce_wave3` invoked at `commands.py:1844` (inline) and `commands.py:2280` (resume) — one call per path. `emit_contract` appears only in comments/docstrings (`commands.py:905, 1811, 2367`) — never invoked from commands.py. Reduce emits the contract internally at `reduce.py:721-722` (`if should_emit and output_dir is not None: emit_contract(contract, Path(output_dir))`). A second call WOULD double-emit; confirmed absent. |
| 3 | `_stamp_inline_worker_paths` populates final/meta/raw_path BEFORE normalize, and is REQUIRED | PASS | Stamping at `commands.py:1822-1826` precedes `normalize_wave2` at `1839`. REQUIRED because `normalize.py:482` gates the body write on `if worker.final_path and result.text:` — empty `final_path` ⇒ no `.final.md` written. `dispatch_wave1`/`_run_worker` stamps only `index` (`dispatch.py:310` per research; WorkerResult dataclass fields confirm `final_path=""` default at `models.py:1121`); transports stamp only `body`/`model_id`/`model_label` (`openai_compat.py:406`, `stub.py:158`). |
| 3b | Helper re-attaches non-dataclass `.body` after `dataclasses.replace` | PASS | `_stamp_inline_worker_paths` at `commands.py` (helper body lines 971-1014): `dataclasses.replace(worker, final_path=..., meta_path=..., raw_path=...)` then `body = getattr(worker, "body", None); if body is not None: replaced.body = body`. `body` is NOT a WorkerResult dataclass field (field list `models.py:1117-1128` has no `body`); it is a dynamic attr (`result.body = body  # type: ignore` at transports). `dataclasses.replace` therefore drops it. Re-attachment is mandatory: `normalize.py:334` reads `body = getattr(worker, "body", None)` to obtain the raw body to transform — without re-attach, normalize would see `None`. |
| 4 | Resume branch `_run_resume_branch` NOT broken/altered | PASS | Diff hunk headers: `@@ -894 +894 (after _lens_injection_substring)`, `@@ -1264 +1382 (option decorators)`, `@@ -1309 +1476 / -1453 +1624 / -1551 +1782 / -1566 +1871 (all inside run_cmd)`. None fall inside `_run_resume_branch` (post-diff it begins ~2030; its `reduce_wave3` is at `2280`). All "resume" tokens in the diff are inside NEW WS-0 helper comments or the `resume=False` kwarg on the inline reduce call — zero functional change to the resume path. Resume `reduce_wave3(..., resume=True)` at `commands.py:2280-2288` is unchanged. |
| 5 | No logic duplicated where a shared helper exists | PASS | The 4 new helpers (`_slugify_model` 913, `_read_truncated_target` 927, `_assemble_inline_prompt` 949, `_stamp_inline_worker_paths` 971) are referenced ONLY from the inline path (`commands.py:1794, 1795, 1822`). Discovery file §(d) confirms the resume branch has NO reusable prompt-assembly or path-stamping helper to call (it rehydrates sidecars via `discover_succeeded_slots` instead). Net-new logic, not redundant duplication. |
| 5b | Contract enriched with `caller_metadata` (suspect) + `recommended_next_command_template` (--suspect-source) | PASS | Inline reduce passes `caller_metadata=preflight_result.caller_metadata` (`commands.py`, arg block ~1854), `recommended_next_command_template=inline_job.recommended_next_command_template`, `recommended_next_command_substitutions=inline_job.recommended_next_command_substitutions`. `PreflightResult.caller_metadata` exists (`preflight.py:240+`, field present). `CallerMetadata` carries `suspect:bool` (`models.py:1641`) + `tier:str` (`models.py:1642`); bare_review lens sets `suspect=True` (research 02 §2). `JobSpec.recommended_next_command_template` exists (`models.py:126`). The `--suspect-source` rendering flows through the lens template (bare_review.py:65-68 per research). |

### Cross-referenced attribute existence (anti-hallucination sweep)

| Referenced in diff | Exists? | Evidence |
|---|---|---|
| `from_dict` (models) | YES | `models.py:1711` module-level `def from_dict(cls, data)` |
| `inline_job.target.truncation.line_cap` | YES | `TargetSpec.truncation` (`models.py`, field at ~289) → `Truncation.line_cap` (`models.py:213`) |
| `inline_job.prompt.system` / `.user_template` | YES | `PromptSpec.system` / `.user_template` (`models.py:360+`, defaults `""`) |
| `inline_job.normalization.recipe` / `.recipe_args` | YES | `NormalizationSpec.recipe` (`models.py:457`), `.recipe_args` (`models.py:460`) |
| `inline_job.output.lens_name` / `.filename_template` | YES | `OutputSpec` DM-007 (`models.py:465+`); `filename_template` default `"{lens}-{index:02d}-{model_slug}.md"` (`models.py:482`); `lens_name` per DM-007 row (`models.py:470`) |
| `inline_job.amalgamation_mode` / `.status_policy` | YES | `JobSpec.amalgamation_mode` (`models.py:124`), `.status_policy` (`models.py:125`) |
| `preflight_result.manifest.preflight.target_checksum` | YES | `Manifest.preflight` (`models.py:1403`) → `PreflightSummary.target_checksum` (`models.py:1315`) |
| `preflight_result.manifest.preflight.workers_requested` | YES | `PreflightSummary.workers_requested` (`models.py:1319`) |
| `preflight_result.manifest.job_id` | YES | `Manifest.job_id` (`models.py:1399`) |
| recipe reads `caller_label` | YES | `bare_review_v1.py:255` `caller_label = str(args.get("caller_label", "") or "")` |
| `lens` / `state_output_dir` in scope at inline call | YES | `lens` is `run_cmd` param (`commands.py:1474`); `state_output_dir` assigned `commands.py:1717/1722`, both before the pipeline block at 1813 |

---

## Summary

- Checks passed: 12 / 12 (5 required claims + sub-claims, all PASS)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| — | INFO | `commands.py:1844-1857` (inline) vs `commands.py:2280-2288` (resume) | The inline reduce_wave3 call passes `caller_metadata`, `recommended_next_command_template`, and `recommended_next_command_substitutions`; the resume reduce_wave3 call passes NONE of them (relies on dataclass defaults → empty CallerMetadata + empty next-command). The diff comment frames this as deliberately "closing the R3 §1.4 inline-vs-resume asymmetry" — i.e., inline is intentionally MORE complete than resume. Not a regression in WS-0 scope (resume was already this way; the diff does not touch it), but the asymmetry now runs in the opposite direction (resume contract is the less-enriched one). | None for WS-0. If full parity is desired, a FOLLOW-UP could thread the same three args into the resume `reduce_wave3` at `commands.py:2280`. Out of WS-0 scope — documented only. |

## Adversarial self-audit

Sought ≥10 errors. Specifically probed for: (a) double contract emission — none (single reduce per path, emit only internal); (b) hallucinated attribute paths — all 11 cross-referenced attrs exist at cited lines; (c) `.body` loss across `dataclasses.replace` — handled correctly via getattr/re-attach, and proven NECESSARY by `normalize.py:334`; (d) resume-branch collateral damage — diff hunks provably do not intersect `_run_resume_branch`; (e) stamping-order bug (stamp after normalize) — order is correct (stamp 1822 < normalize 1839); (f) gate condition that would skip the pipeline silently — gated on `state_output_dir is not None and recipe_name`, both populated on the lens path. The only finding is the INFO-level intentional asymmetry. Verdict stands as PASS.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 8 (git diff + targeted greps, each mapped to a specific claim)
- No UNCHECKED items. No UNVERIFIABLE items. No web research required (all claims intrinsically local/source-truth).

## QA Complete

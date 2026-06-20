# QA Report — Post-Completion Content / Actionability Lens

**Topic:** TFEP forensic→troubleshoot backend migration (post-completion QA)
**Date:** 2026-06-16
**Phase:** doc-qualitative (actionability lens — migrated-instruction executability)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)
**Adversarial stance:** Assumed ≥5 errors focused on actionability. Found 5 (1 CRITICAL, 3 IMPORTANT, 1 MINOR).

---

## Overall Verdict: FAIL

The migrated instructions are mostly executable, but the TFEP↔troubleshoot
round-trip has concrete executability gaps an agent cannot resolve without
interpretation: an unresolvable predicate field in the consume branches, an
uninitialized loop counter that defeats the FULL-STOP bound, and an
under-specified `--output-dir` path-join that can misplace the return contract.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | §4.5 Step 3 dispatch flags resolvable | PASS (with caveat F3) | task-protocol L215 dispatch `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}`; all four flags exist in troubleshoot.md L8 argument-hint + L59/L60 options |
| 2 | Depth selection clear/deterministic | PASS | task-protocol L210-212 + L215 map 1st→standard, 2nd/systemic/≥3→deep; both valid per troubleshoot.md L51 enum |
| 3 | `{context_path}` bound | PASS | task-protocol L205 "Write context to `{output_dir}/context.yaml` — this file is the `{context_path}`" |
| 4 | `{output_dir}` bound + round-trip path-join | FAIL (F3) | task-protocol writes/reads under `{output_dir}` (L205, L219) but troubleshoot Wave 0 step 4 (SKILL L130) "Compute output slug … and create `<output-dir>/`" does not state whether a caller-supplied `--output-dir` is used verbatim or nested under a fresh slug subdir |
| 5 | Step 4 consume branches: first-match-wins | PASS | task-protocol L222 "Evaluate the branches top-to-bottom, first match wins" |
| 6 | Step 4 branches reference only emitted fields | FAIL (F1) | L225 reads `behavior_is_documented == true`, absent from the 7-field wire set (troubleshoot SKILL L471; report-template L160-168) |
| 7 | Step 4 terminating decision procedure | FAIL (F2) | retry/escalate_depth re-entry (L228-229) relies on `escalation_count` to hit FULL STOP, but the counter is never initialized and Step 3 FULL STOP is keyed to prose "3rd TFEP trigger" not a counter comparison |
| 8 | FULL STOP bounds present | PASS (weakened by F2) | L213, L230, L270 establish FULL STOP arms; halt/failed arm (L230) is unconditional and terminates |
| 9 | Wave 0 step 6 resolve executable | PASS | troubleshoot SKILL L148 reads `--context`, resolves to abs path, STOPs if unreadable (L152 STOP condition), marks Wave 5 emit |
| 10 | Wave 5 step 4.5 emission: field set | PASS | SKILL L471 enumerates exactly the 7 wire fields |
| 11 | Wave 5 step 4.5 emission: sources bound | PASS | root_cause←Diagnosis, solution←Proposed Fix/Next Steps, status←step 3, recommended_escalation←deterministic tie-break (L471) |
| 12 | Wave 5 step 4.5 emission: gating | PASS | gated on `caller=task-unified` (L471 + Wave 0 L148 mark) |
| 13 | Wave 5 step 4.5 emission: no `--fix` | PASS | L471 NOTE + Step 3 L215 + L239 all assert NO `--fix`; Wave 6 precondition requires `--fix` (L487), so TFEP never reaches remediation |
| 14 | `recommended_escalation` tie-break determinism | PASS | L471 ordered hint: failed→halt, partial+low-conf→escalate_depth, partial+tier<2→retry, success→none; ordered first-match resolves the partial+tier<2+low-conf overlap to escalate_depth |
| 15 | Step 6 resume `--compliance strict` actionable | PASS | valid flag value per task.md L44 / task-protocol L44 |
| 16 | `remediation_target == "docs"` branch reachable | PASS | derivation in Output Contract L75 (docs when behavior_is_documented indicates doc gap); cross-ref'd from Step 4 |
| 17 | `escalation_count` initialization | FAIL (F4) | described as a field (L203) but never set to an initial ordinal; only "increment" instructions exist (L228, L229, L245) |
| 18 | Escalation Budget block matches Step 3 | PASS (MINOR F5) | L265-271 budget block omits the `retry` re-entry path that L228 introduces — incomplete but not contradictory |

## Summary
- Checks passed: 13 / 18
- Checks failed: 5
- Critical issues: 1
- Important issues: 3
- Minor issues: 1
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | sc-task-protocol/SKILL.md §4.5 Step 4, L225 | The consume branch tests the literal predicate `behavior_is_documented == true`, but `behavior_is_documented` is NOT a field of the `return-contract.yaml` the consumer reads. The 7-field wire set (troubleshoot SKILL L471; report-template TFEP-Consumer YAML L160-168) is `status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary`. The same Step 4 cross-ref (L219) enumerates only those 7. An executor reading the contract cannot resolve `behavior_is_documented` — it must interpret. The branch is *reachable* only via the `(or remediation_target == "docs")` OR-clause; the first predicate is dead. | Drop the `behavior_is_documented == true` predicate and gate the branch solely on `remediation_target == "docs"` (the producible field), OR add `behavior_is_documented` to the 7-field wire set in both troubleshoot SKILL L471 and report-template L160-168 (making it an 8-field set). Pick one; do not leave a dead predicate referencing an unemitted field. |
| F2 | IMPORTANT | sc-task-protocol/SKILL.md §4.5 Step 3 (L207-213) + Step 4 (L228-230) | The decision procedure does not deterministically terminate. The `retry` branch (L228) says re-run "once" and "increment escalation_count"; the `escalate_depth` branch (L229) also increments. FULL STOP is supposed to bound the loop, but Step 3's FULL STOP (L213 "3rd TFEP trigger → FULL STOP") is keyed to the prose ordinal "TFEP trigger", which is never mechanically equated to the numeric value of `escalation_count`. There is no `if escalation_count >= 3 → FULL STOP` comparison. A backend that repeatedly returns `recommended_escalation: retry` re-enters Step 3 with no guaranteed numeric guard firing. (The `halt`/`failed` arm at L230 IS unconditional and terminating — that arm alone is the only hard guarantee.) | Add an explicit numeric guard at the top of Step 3: "If `escalation_count >= 3` → FULL STOP regardless of `recommended_escalation`." Bind the Step 3 depth-mapping bullets to `escalation_count` value (1→standard, 2→deep, ≥3→FULL STOP) so "TFEP trigger" and the counter are the same quantity. |
| F3 | IMPORTANT | sc-troubleshoot-protocol/SKILL.md Wave 0 step 4 (L130) vs sc-task-protocol/SKILL.md §4.5 (L205, L219) | The round-trip path-join is under-specified. The consumer writes `context.yaml` to `{output_dir}` and reads `return-contract.yaml` from `{output_dir}` (the exact dir it passed via `--output-dir`). Troubleshoot Wave 0 step 4 says "Compute output slug `<type>-<5words>-<ts>` and create `<output-dir>/`", and the default `--output-dir` is itself `.dev/troubleshoot/<slug>-<timestamp>/`. It is not stated that an explicitly-passed `--output-dir` is used verbatim (no extra slug subdir appended). If troubleshoot nests a fresh `<slug>-<timestamp>` under the passed dir, the contract lands at `{output_dir}/<slug>/return-contract.yaml` and the consumer's read of `{output_dir}/return-contract.yaml` (L219) fails to find it — TFEP stalls silently. | In troubleshoot Wave 0 step 4, state explicitly: "When `--output-dir` is supplied (e.g., by a `--caller`), use it verbatim as `<output-dir>` — do NOT append a computed slug subdir; the slug naming applies only to the default path." This guarantees the consumer's `{output_dir}/return-contract.yaml` read path is correct. |
| F4 | IMPORTANT | sc-task-protocol/SKILL.md §4.5 Step 2 (L203), Steps 4/6 (L228, L229, L245) | `escalation_count` is never initialized. It is described as a `failure_context` field ("which TFEP trigger this is (1, 2, or 3)", L203) but no instruction SETS it on first TFEP entry. Every mutation is "increment escalation_count". An executor entering TFEP the first time has no defined value to increment from, and the Step 3 depth/FULL-STOP ordinal cannot be derived. (Root cause shared with F2.) | Add to Step 2 (or Step 1): "On the FIRST TFEP entry for this failure, set `escalation_count = 1`; on each re-entry (Step 4 retry/escalate_depth or Step 6 fail-again), increment by 1." Then F2's numeric guard becomes well-defined. |
| F5 | MINOR | sc-task-protocol/SKILL.md §4.5 Escalation Budget block (L265-271) | The Escalation Budget summary block enumerates only the three forward triggers (1st→standard, 2nd→deep, 3rd→FULL STOP). It does not reflect the `recommended_escalation: retry` re-entry path introduced in Step 4 (L228), which re-runs at the SAME depth. The block is an incomplete (not contradictory) summary of the actual control flow, so a reader using it as the authoritative map would miss the retry arm. | Add a line to the budget block for the retry arm (e.g., "`recommended_escalation: retry` → re-run at SAME `--depth`, `escalation_count += 1`, subject to the ≥3 FULL STOP cap"), or add a forward-reference: "See Step 4 consume branches for the retry/escalate_depth re-entry semantics." |

## Actions Taken
None — `fix_authorization: false` (report-only). All findings documented above for the orchestrator/owner to remediate.

## Confidence Gate
- **Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: ~14 (via Bash) | Glob: 0 | Bash: 7
- Every check above was verified against the actual file content (line-cited). No check marked N/A; the doc-qualitative checklist was adapted to the actionability lens of the migrated executable instructions.

## Self-Audit
1. **Factual claims independently verified against source:** 18 checks, each grounded in a cited line of one of the 5 files (e.g., the 7-field wire set at troubleshoot SKILL L471 and report-template L160-168; the absent `behavior_is_documented` field confirmed by `grep -c` = 2 occurrences, both in task-protocol consume prose, zero in the emitted contract).
2. **Files read:** all 5 target files in full (sc-task-protocol SKILL.md 407L; sc-troubleshoot-protocol SKILL.md 603L read in 2 pages; troubleshoot.md 205L; task.md 187L; report-template.md 320L).
3. **Why trust the non-zero finding count:** I actively ruled OUT three plausible-but-false findings during the adversarial sweep (depth-enum mismatch — consistent; `recommended_escalation` partial+tier<2+low-conf overlap — deterministic via ordered first-match; `--fix` leak into Wave 6 — gated out). The 5 findings that remain each survived a "can an executor resolve this from the file alone?" test and each cites the specific unresolvable token.
4. **Web research:** none performed (all verification was local-file-bound); Tavily-first rule not triggered this review.

## Recommendations
- Resolve F1–F4 before this migration ships: each is a point where the TFEP↔troubleshoot round-trip requires an executor to interpret rather than execute, and F2+F4 together can defeat the FULL-STOP loop bound (a real "runs forever / stalls silently" hazard, not cosmetic).
- F4 is the root cause of F2 — fix F4 (initialize the counter) and F2 (add the numeric `>=3` guard) together.
- F1 and F3 are independent cross-file contract gaps; each has a clean single-edit fix.
- F5 is a documentation-completeness nit; fix opportunistically.

## QA Complete

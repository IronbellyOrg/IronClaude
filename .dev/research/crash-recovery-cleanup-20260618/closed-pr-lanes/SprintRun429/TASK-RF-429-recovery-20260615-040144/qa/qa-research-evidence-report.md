# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** 429/account-exhaustion recovery design — MDTM task builder research
**Date:** 2026-06-15
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Assigned research files (in `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/research/`):
- 01-file-inventory.md
- 02-patterns-conventions.md
- 03-integration-points.md
- 04-data-flow-tracer.md
- 05-test-verification.md
- 06-template-examples.md

Verification approach: adversarial. Spot-check >=30% of cited file:line references by Reading the actual source under `src/superclaude/cli/sprint/`. Prioritize the load-bearing citations listed in the spawn prompt.

---

## Findings

### Spot-check results (load-bearing citations re-verified against source)

Every prioritized citation in the spawn prompt was independently re-Read. Result: **all accurate** (line-exact or within a few-line tolerance). Far more than the required 30% was checked.

| Cited claim (research) | Source verified | Result |
|---|---|---|
| `_run_one_task` sig `executor.py:963-975` (kw-only `ledger/subprocess_factory/shadow_metrics/remediation_log/lock`) | executor.py 963-975 | EXACT |
| Status ladder `executor.py:999-1015` (`exit 0→PASS`, `124→INCOMPLETE`, `:1003` error_max_turns+completed→PASS_RECOVERED, `:1012` `_is_transient_failure`→FAIL_RECOVERABLE, else FAIL_TERMINAL) | executor.py 999-1015 | EXACT |
| Insertion point: above `:1012`, below `:1003` completion gate | executor.py 1003-1012 | EXACT |
| `guard = lock if … else contextlib.nullcontext()` at `:1017`; TaskResult ctor `:1027-1035` | executor.py 1017, 1027-1035 | EXACT |
| `:2103 if status.is_failure:` runs DiagnosticCollector bundle (`:2103-2128`) — NOT "only halts" (F-1) | executor.py 2103-2132 | EXACT — F-1 confirmed |
| `_is_transient_failure` `:2267-2289`; `api_retry` collision at `:2278`; `is_error`+`output_tokens==0` at `:2288` | executor.py 2267-2289 | EXACT |
| `_write_phase_result_json` `:2657-2701`; payload keys `:2685-2696` (`task_results` at `:2691`, `recovery_history` at `:2692`) | executor.py 2657-2701 | EXACT |
| `TaskStatus` `models.py:46-66`; `is_success` 56-58, `is_failure` 60-66 (`FAIL_TERMINAL/FAIL_RECOVERABLE/INCOMPLETE`) | models.py 46-66 | EXACT |
| `TaskResult.from_dict` HARD-KEYED `:218-240` (`data["status"]` 231 etc.); nested task `.get()` 226-229 | models.py 218-240 | EXACT |
| `PhaseStatus` `:385-443` has THREE props: `is_terminal` 409-423, `is_success` 425-434, `is_failure` 436-443 (`INCOMPLETE/HALT/TIMEOUT/ERROR`); HALT=404/TIMEOUT=405/ERROR=406/SKIPPED=407 | models.py 385-443 | EXACT |
| `_classify_transcript` `rerun_tasks.py:547-593`; `subtype` 579, `is_error` 580, ladder 582-591, `result_event is None→INCOMPLETE` 576-577 | rerun_tasks.py 547-593 | EXACT |
| planner `rerun_task_ids` `:160-164` (`not bt.persisted_status.is_success` at 163); `_coerce_task_status` DEF at `:339` (CALL at `:157`) | planner.py 155-171, 338-344 | EXACT (incl. the DEF-vs-CALL correction) |
| K>1 call site `:1134-1145` `lock=lock` (:1144); K=1 `:1337-1348` `lock=None` (:1347) | executor.py 1134-1145, 1337-1348 | EXACT |
| Single-session spawn `ClaudeProcess(...)` `:1815`/`.start()` `:1816`; `_determine_phase_status` call `:1993-2001`, DEF `:2751` | executor.py 1815-1816, 1993, 2751 | EXACT |
| process.py cmd/env in PIPELINE BASE: `build_command` `pipeline/process.py:121`, `--model` `:141`, `build_env`/`os.environ.copy()` `:155`; sprint `ClaudeProcess` `:137`, `model=config.model` `:162` | pipeline/process.py 121/141/155; sprint/process.py 137/162 | EXACT (correction confirmed) |
| `count_turns_from_output` is in monitor.py:223; `count_turns_from_stream_json` is in process.py:32 (spec's name was WRONG) | both confirmed | EXACT (correction confirmed) |
| recovery.py has exactly 3 Nominators (`Nominator` 143, `ManualNominator` 149, `ReflectReportNominator` 164); NO `DriftNominator` | recovery.py grep | EXACT (correction confirmed) |
| monitor.py has NO `enum`/`dataclass` import (8-19); models.py HAS `dataclass,field` (:12) + `Enum` (:14) | both confirmed | EXACT |
| `--task-parallelism` template `commands.py:203-204`, param `:255`, call `:353` | commands.py | EXACT (within tolerance) |
| Template `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` 120,364 bytes exists; `.claude/templates/workflow/` does NOT exist | filesystem | EXACT |

### Self-correcting research quality

The research files proactively flagged and CORRECTED at least 6 upstream (spec/research-notes) errors, each of which I independently re-verified as a genuine correction (not an introduced error):
1. `count_turns_from_stream_json` → actual symbol is `count_turns_from_output` (monitor) / `count_turns_from_stream_json` lives in process.py. (Files 01, 04, 05)
2. No `DriftNominator` class exists. (File 03 IP-7)
3. cmd/env assembly is in `pipeline/process.py:121-160`, not `sprint/process.py:129-141`. (File 03 IP-9)
4. `_coerce_task_status` DEF at planner.py:339, not :157 (the CALL is at :157). (File 03 IP-8)
5. `PhaseStatus` has THREE membership properties; the new member must touch `is_terminal` + `is_failure`, not just the member add. (Files 01, 02, 03)
6. `:2103 if status.is_failure:` runs a DiagnosticCollector bundle automatically (F-1) — the spec's "no auto-remediation consumer" is FALSE for the single-session path. This is a MATERIAL finding correctly surfaced with a builder decision (B1/B2 options, not silently resolved).

### Evidence-density assessment (per file)

- **01-file-inventory.md** — DENSE. Every symbol carries line + signature; insertion zones bounded by verified anchors; import gaps verified. Status: Complete.
- **02-patterns-conventions.md** — DENSE. Six patterns each with a verified `file:line` exemplar; explicitly marks `build_resume_output` line range as Unverified (delegated to R1/R3) — honest scoping, not a fabrication.
- **03-integration-points.md** — DENSE. 10 integration points, each CONFIRMED line-exact with code excerpts; corrections to research-notes are evidence-backed.
- **04-data-flow-tracer.md** — DENSE. End-to-end flow with verified anchors; F-1 material finding; storm-bound arithmetic (`≤ cap+(K−1)`, `< K×cap`) is internally consistent and spec-cited.
- **05-test-verification.md** — DENSE. Test seam, 6 fixtures, factory worked example, doc⇆CLI parity, back-compat — all grounded in cited test-file line ranges; UNVERIFIED items explicitly listed (§12) for the builder to close.
- **06-template-examples.md** — DENSE. Template path verified (byte count matches), frontmatter tabulated, POST-reflect emission grounded in SKILL.md line cites, anti-orphaning rule with real prior-task example.

### Unsupported-assertion scan

No claims stated as fact were found to be fabricated. Where the research could not verify, it consistently used explicit `Unverified` / `UNVERIFIED` / `needs_human_decision`-adjacent tags rather than asserting:
- File 01: `IC_ALIASES` token marked Unverified; aienv.py design (A vs B) flagged as a decision to surface, not silently pick.
- File 02: `build_resume_output` line range, `executor.py:1815/:1993` single-session, text-core net-new — all marked Unverified inline and in the closing summary.
- File 03: `context` dict contents for the (G) nominator exclusion marked UNVERIFIED with instruction to trace before implementing; `--resume` exact flag string marked UNVERIFIED.
- File 05: §12 carries an explicit "UNVERIFIED (builder must close)" list (decide boundary `<` vs `<=`, real `~/.aienv` format, `run` Click symbol name, guide heading layout, reset_policy param name).

These are appropriate, honest gaps — they are scoped to the builder/other researchers and do NOT block task construction. They are MINOR (the builder is explicitly instructed to close them during implementation, which is the correct phase).

### Note on a cosmetic regex-escaping artifact (MINOR)

File 05 §4 line 205 inline example contains `account\\'s` inside a single-quoted Python string — that exact snippet would be a syntax error if pasted verbatim. It is illustrative test scaffolding (not a source citation), and the builder will author the real fixture from the spec §2 verbatim JSON (§3.1 uses the correct double-quoted JSON form). Cosmetic only; flagged for completeness.

---

## Confidence Gate

**Checklist categorization (10-item research-gate checklist):**

1. File inventory (all 6 files Status: Complete, have Summary) — [x] VERIFIED (Read all 6; 01/02/03/04/05/06 all marked Complete with Summary sections)
2. Evidence density (claims cite file:line/symbol) — [x] VERIFIED (per-file density table above; >30% spot-checked, all accurate)
3. Scope coverage (key files discussed) — [x] VERIFIED (monitor/models/executor/rerun_tasks/planner/process/commands/recovery all covered with verified cites)
4. Documentation cross-validation (doc claims tagged) — [x] VERIFIED (research is code-sourced, not doc-sourced; `[CODE-VERIFIED]`-equivalent CONFIRMED tags throughout, independently re-checked)
5. Contradiction resolution — [x] VERIFIED (F-1 surfaces a spec-vs-code contradiction explicitly with resolution options; no unresolved silent contradictions)
6. Gap severity (all gaps listed) — [x] VERIFIED (Unverified items explicitly enumerated per file; all builder-closable, none synthesis-blocking)
7. Depth appropriateness (Deep tier: end-to-end data flow) — [x] VERIFIED (File 04 traces 429 signal end-to-end for both per-task and single-session paths)
8. Integration point coverage — [x] VERIFIED (File 03 = 10 integration points with edit/no-edit verdicts)
9. Pattern documentation — [x] VERIFIED (File 02 = 6 reusable patterns with exemplars)
10. Incremental-writing compliance — [x] VERIFIED (files show iterative structure, corrections layered over research-notes, not one-shot)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 11 | Grep: 0 | Glob: 0 | Bash: 3 (each Bash multiplexed several grep/sed/ls verifications mapped to specific checklist items: count_turns naming, Nominator inventory, build_command/env location, import blocks, --task-parallelism, template path)

Note: total verification tool calls (11 Read + 3 multi-target Bash) comfortably exceed the 10-item checklist minimum; each call targeted a specific cited symbol/line, none were padding.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory complete | PASS | All 6 files Read; each Status: Complete + Summary present |
| 2 | Evidence density | PASS | All 6 DENSE; >30% load-bearing cites re-Read, 100% accurate |
| 3 | Scope coverage | PASS | All touched source modules cited + verified |
| 4 | Doc cross-validation | PASS | Code-sourced; CONFIRMED tags independently re-verified |
| 5 | Contradiction resolution | PASS | F-1 spec-vs-code contradiction surfaced + resolved with options |
| 6 | Gap severity | PASS | Unverified items enumerated; all builder-closable, none blocking |
| 7 | Depth (Deep: e2e flow) | PASS | File 04 end-to-end both paths |
| 8 | Integration coverage | PASS | File 03: 10 IPs with edit verdicts |
| 9 | Pattern documentation | PASS | File 02: 6 patterns + verified exemplars |
| 10 | Incremental-writing | PASS | Iterative, layered corrections |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 05-test-verification.md §4 L205 | Inline illustrative Python example `account\\'s` inside single-quoted string would be a syntax error if pasted verbatim. Not a source citation; real fixtures authored from spec §2 (§3.1 uses correct JSON). | Cosmetic; builder authors real fixture from spec — no action required pre-build. Optionally fix the inline example to a double-quoted string. |

No CRITICAL or IMPORTANT evidence-quality issues. No fabricated citations, no wrong line numbers, no non-existent symbols.

## Recommendations
- Proceed to task construction. The research is evidence-dense and citation-accurate.
- Carry the explicitly-flagged Unverified items into the builder's per-item Context fields (TB-Add-8 evidence binding) so they are closed during implementation, not assumed: aienv.py design A/B, `decide` `<`/`<=` boundary, real `~/.aienv` export format, `run` Click symbol name, sprint guide option-heading layout, reset_policy param name.
- Honor F-1 in P4: do NOT add `PhaseStatus.PROVIDER_EXHAUSTED` to `is_failure` without the `:2103` diagnostic-bundle guard (option B1), or the infra halt will write a spurious product-bug bundle (UX contract #4 violation).

---

## VERDICT: PASS

Evidence quality is excellent. Every load-bearing citation re-verified accurate (line-exact or within tolerance); zero fabricated paths, zero wrong line numbers, zero non-existent symbols. The single finding is MINOR (a cosmetic inline-example escaping artifact in non-citation test scaffolding) and does not block the builder. The research additionally self-corrected 6 upstream spec/research-notes errors, each independently confirmed. Green light for task construction.

## QA Complete

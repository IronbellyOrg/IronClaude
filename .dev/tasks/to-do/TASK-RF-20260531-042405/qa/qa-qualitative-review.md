# QA Qualitative Review — TASK-RF-20260531-042405

**Reviewer:** rf-qa-qualitative (adversarial stance)
**Date:** 2026-05-31
**Phase:** task-qualitative (post task-builder, pre-execution)
**fix_authorization:** true (1 in-place fix applied)
**Task file:** `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` (831 lines)
**Authoritative spec:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`

---

## Methodology

Verified the task plan against (a) BUILD-REQUEST §Contract + §MVR verbatim, (b) the 10 listed target files in the codebase (line citations checked via Grep + Read), (c) the research dir (01-file-inventory.md, 02-patterns-conventions.md, 03-template-and-precedent.md), (d) the MultiModelSwarm halt evidence at `.dev/releases/Current/MultiModelSwarm/anti-instinct-audit.md`. Applied the 15-item Task File Qualitative Review checklist and the 5 Adversarial Axes (drift / contradictions / omissions / weakened criteria / invented content).

For every line citation present in the task file, I either Grep'd the source file to confirm the line number or Read the file at the cited offset. For the 6 frontmatter parsers, the 8 obligation_scanner return-True sites, the 7 remediate_executor return-True sites, the 2 fail-open blocks in fidelity_checker, and the `gate=None` bypass — all line numbers match the running source as of `git status` snapshot at session start.

---

## Verification Matrix — Cited Citations vs Source-of-Truth

| Citation (task)                                                          | Reality (source)                                                       | Match? |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ------ |
| `executor.py:_build_steps` L1947                                         | def `_build_steps` at L1947                                            | YES    |
| `executor.py:build_certify_step` L1899                                   | def `build_certify_step` at L1899                                      | YES    |
| `executor.py:roadmap_run_step` L955                                      | def `roadmap_run_step` at L955                                         | YES    |
| `executor.py:2167` `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` | exact match at L2167                                       | YES    |
| `gates.py:_parse_frontmatter` L168                                       | def at L168                                                            | YES    |
| `gates.py:_cross_refs_resolve` L48                                       | def at L48                                                             | YES    |
| `gates.py:_REQUIRED_H2_SECTIONS` L891                                    | constant at L891                                                       | YES    |
| `gates.py:MERGE_GATE` SemanticCheck constructed L1180-1200               | MERGE_GATE at L1174 with SemanticChecks L1183/1188/1193/...           | YES    |
| `cli/pipeline/gates.py:_check_frontmatter` L91                           | def at L91                                                             | YES    |
| `cli/pipeline/models.py` `GateCriteria` L91 `SemanticCheck` L82          | classes at L91 and L82 respectively                                    | YES    |
| `spec_parser.py:parse_frontmatter` L109                                  | def at L109                                                            | YES    |
| `spec_parser.py:extract_requirement_ids` L333                            | def at L333                                                            | YES    |
| `spec_patch.py:_extract_frontmatter` L285                                | def at L285                                                            | YES    |
| `fidelity_checker.py:287-303` (fail-open `found=True`)                   | block exists; L298 `found=True,  # fail-open`                          | YES    |
| `fidelity_checker.py:314-337` (partial-match fail-open)                  | block exists; L320 comment `marking as found (fail-open per R-3)`      | YES    |
| `fidelity_checker.py:_scan_codebase` L165-200                            | def `_scan_codebase` at L165                                           | YES    |
| `obligation_scanner.py` `_DESCRIPTOR_NOUNS` L109-125                     | frozenset at L109-125                                                  | YES    |
| `obligation_scanner.py` `_DEMOTED_H3_SUBSECTIONS` L137-142               | tuple at L137-142                                                      | YES    |
| `obligation_scanner.py` `scan_obligations` L208                          | def at L208                                                            | YES    |
| `obligation_scanner.py` `return True` at L719/722/725/729/733/737/741/760 | all 8 present; all inside `_is_meta_context` / `_has_discharge`        | YES    |
| `remediate_executor.py` `return True` at L326/345/362/397/412/423/706    | all 7 present                                                          | YES    |
| `fingerprint.py` `return True` at L97/100                                | both present                                                           | YES    |
| `spec_parser.py:468` `return True`                                       | present                                                                | YES    |
| prompts.py `build_extract_prompt` L181                                   | def at L181                                                            | YES    |
| prompts.py `build_extract_prompt_tdd` L329                               | def at L329                                                            | YES    |
| prompts.py `build_generate_prompt` L533                                  | def at L533                                                            | YES    |
| prompts.py `build_diff_prompt` L854                                      | def at L854                                                            | YES    |
| prompts.py `build_debate_prompt` L879                                    | def at L879                                                            | YES    |
| prompts.py `build_score_prompt` L906                                     | def at L906                                                            | YES    |
| prompts.py `build_merge_prompt` L964                                     | def at L964                                                            | YES    |
| prompts.py `build_spec_fidelity_prompt` L1085                            | def at L1085                                                           | YES    |
| prompts.py `build_wiring_verification_prompt` L1220                      | def at L1220                                                           | YES    |
| prompts.py `build_test_strategy_prompt` L1278                            | def at L1278                                                           | YES    |
| `certify_prompts.py:21` `build_certification_prompt`                     | def at L21                                                             | YES    |
| `validate_prompts.py:16` `build_reflect_prompt`                          | def at L16                                                             | YES    |
| `remediate_prompts.py:17` `build_remediation_prompt`                     | def at L17                                                             | YES    |
| `src/superclaude/contracts/` does NOT exist                              | confirmed: directory not present                                       | YES    |
| `src/superclaude/tools/` does NOT exist                                  | confirmed: directory not present                                       | YES    |

All 36 spot-checked citations match running source. Pre-fix invariant test cycles (Step 2.6, Step 3.5, etc.) are correctly authored as MUST-FAIL pre-fix / MUST-PASS post-fix per Contract #1.

---

## Adversarial Findings

### CRITICAL (none)

No CRITICAL issues. The plan would actually execute and produce the claimed deliverables if followed.

### IMPORTANT

**I-1 (Path drift — FIXED in this review).** Step 11.1 (cleanup inventory) and Step 11.2 (frontmatter parser deletion) originally cited `cli_portify/utils.py:parse_frontmatter` L11 and `audit/wiring_gate.py:_extract_frontmatter_values` L931 *without the `cli/` prefix*. The real paths are `src/superclaude/cli/cli_portify/utils.py` and `src/superclaude/cli/audit/wiring_gate.py`. Research source (research/01 §A.3 plus the §B Cross-substrate note at L237) cites them correctly *with* `cli/`. An executing agent following the task verbatim would Grep these paths and fail to locate the files, then either (a) skip them as "missing" (under-deletion → Contract #6 left half-done) or (b) burn cycles re-discovering the right paths. **FIX APPLIED:** Edited Step 11.1 (a) and Step 11.2 (c) to qualify the paths with `cli/` (and `src/superclaude/cli/` for the deletion list to be unambiguous).

**I-2 (Step-count baseline arithmetic).** Task and BUILD-REQUEST both say "current 14 steps" and Acceptance Gate #6 says step count must be ≤14. Grep'd `Step(` instantiations in `executor.py:_build_steps` returns 13 occurrences (1936 is `build_certify_step` returning a Step; 2003/2030/2048/2068/2078/2088/2107/2130/2140/2158/2175/2186/2196 are 13 Step constructors in `_build_steps`). Some are inside lists (parallel steps), so the operational "step count" may differ from the line count. The Acceptance Gate #6 numeric is inherited from BUILD-REQUEST and Vector A, so the discrepancy is upstream — but the task should not assert "14" as a load-bearing pre-existing number. The R1.5 design (Step 10.1) does acknowledge this by saying "currently 14, R1.5 adds 1 so R1.6 MUST consolidate ≥1". If the actual current count is 13, R1.5's add does not breach Gate #6 even without consolidation. **NOT FIXED** — this would require re-counting via running `_build_steps(RoadmapConfig())` and updating BUILD-REQUEST, which is out of scope for a task-file qualitative review. Flagging for the executing agent to verify via Acceptance Gate #6 verification command in Step 13.7 (which already includes the `len(_build_steps(RoadmapConfig()))` runtime check). Acceptable as a *runtime-verified* assertion.

**I-3 (R1.4 dynamic cutover item).** Step 9.12 is correctly flagged as the *only DYNAMIC item* in the task ("Update on each release cycle until 3 cycles pass per step"). Vector A's "≥3 release cycles" criterion cannot be satisfied at task-authoring time — the task file authors a cutover decision that the worker agent updates over weeks/months of real release cycles. The task explicitly handles this with a follow-up item in §Follow-Up Items Identified ("Any R1.4 sub-step that remained dual-write at task completion"). This is acceptable per the L5 conditional-action pattern. **NO FIX.**

**I-4 (Envelope cutover criterion fuzzy).** BUILD-REQUEST §R1.2 says "dual-write envelope + markdown for one release cycle". Step 11.4 (R1.6 deletion of fail-open) implies the envelope dual-write has matured by R1.6 — but no explicit cycle-counter exists for the envelope (unlike the per-step R1.4 cutover that tracks 3 cycles). If the envelope dual-write has run 0 cycles by R1.6, the deletion at Step 11.4 is premature. **NOT FIXED** — flagging as Open Question for executing agent: the envelope dual-write criterion should be tracked explicitly in `phase-outputs/plans/r1-2-cutover-decision.md` analogous to `r1-4-cutover-decision.md`. The task is silent on this and would benefit from a Step 7.5 paralleling Step 9.12. Acceptable for now because R1.6 cleanup runs Phase 11 — well after R1.2 in Phase 7 — giving practical buffer.

### MINOR

**M-1 (MultiModelSwarm halt seed-case mis-citation in spec).** BUILD-REQUEST §R0 item 2 cites "lines 207/211/213" as MultiModelSwarm halt evidence. Reading `.dev/releases/Current/MultiModelSwarm/anti-instinct-audit.md` confirms: the audit's "Undischarged obligations" list references roadmap-file lines 207/211/213 (e.g., `Line 207: 'stub' in M3: Dispatch & Concurrency (Wave 1) (transport)`). So the line numbers refer to the **roadmap.md output** of the MultiModelSwarm release, not the audit file itself. Task Step 3.1 correctly defers seed-case extraction to discovery, but says "specific scanner output lines 207/211/213 (referenced verbatim in BUILD-REQUEST §R0 item 2 as 'stub transport', 'stub-worker parallelism test', etc.)" — the line numbers and phrases are real but the *file* they appear in is the audit's enumeration of roadmap-line matches. An executing agent will need to walk: audit-file → roadmap line numbers → roadmap content → derive allowlist phrase. Step 3.1 does specify "the obligation_scanner Layer that fired" + "the demotion that SHOULD have applied" which is the correct disambiguation. **NO FIX.**

**M-2 (Allowlist data structure choice deferred to design).** BUILD-REQUEST §R0 item 2 ("Extend `obligation_scanner.py` (or its config) to accept an inline allowlist") does not pin a data structure. Task Step 3.2 correctly defers the choice (`_DESCRIPTOR_NOUNS` extension vs `_DEMOTED_H3_SUBSECTIONS` extension vs new `_ALLOWLIST_PHRASES`) to the design item with rationale + forward-compatibility note. This is the right deferral pattern. **NO FIX.**

**M-3 (R0.3 packages-pyproject ordering).** Step 4.2 mentions `pyproject.toml` should package `superclaude.contracts`. Step 4.4 introduces `superclaude.tools`. Step PG4.2 (R0.3 QA) verifies *both* `superclaude.contracts AND superclaude.tools` are correctly packaged. Step 4.4 does not include an explicit "update pyproject.toml" sub-bullet for `tools`, but Hatchling's default discovery under `src/` would auto-discover both packages if `[tool.hatch.build.targets.wheel] packages = ["src/superclaude"]` (or similar) is the existing pattern. **NO FIX** — the executing agent will catch this via Step PG4.2's packaging check.

**M-4 (Skill prose alignment runs single-pass).** Phase 12 Step 12.1 says "use ≥4 sequential Edit passes per precedent A (sc-reflect-rebuild pattern from research/03 §2.1)". Steps 12.2-12.5 say only "Read ... update to reflect ..." — single-edit phrasing. The 4-pass pattern is only explicit on SKILL.md (Step 12.1). For the refs/ files which are ~470-700 LOC each, single-pass edits may exceed the 200-LOC-change preference. **NO FIX** — executing agent has latitude per I3 to break into multiple edits if hit limit. Minor.

---

## Coverage Check — 5 Adversarial Axes

1. **Drift (citations not in source, paraphrasing changes meaning):** 36 line citations spot-checked; 36 matched. ID_PATTERNS regex strings in Step 4.2 are verbatim from BUILD-REQUEST §MVR §5. PipelineEnvelope field list in Step 7.2 verbatim. Contract #9 set-containment formula verbatim. CodeAssertion signature `(envelope, repo_path) -> Finding | None` verbatim. No drift detected except I-1 (FIXED).
2. **Contradictions (item A vs item B internally inconsistent):** None. Step ordering R0→R1→Phase 12→Phase 13 is monotonic. PRESERVE invariants (`commands.py`, `structural_checkers.py`, `convergence.py`, `cosmetic_remediator.py`) are listed in §Source areas (out-of-scope) and re-verified in every QA gate prompt. No phase modifies a PRESERVE file. Dual-write semantics consistent across Phase 7 (envelope) and Phase 9 (tool-write).
3. **Omissions (BUILD-REQUEST item missing from task):** Cross-checked the 10 Contract items + 8 Acceptance gates + 6 R1 sub-phases. All 10 Contract items have a checklist item that creates a test or wires a CI lint:
   - C#1 → Step 13.3 `test_recurrence_regression.py` (master invariant) + per-fixture tests
   - C#2 → Step 8.3-8.4 dispatch-reachability + `test_dispatch_reachability.py`
   - C#3 → Step 9.4 + 9.8 generator-side constraint + schema validation
   - C#4 → Step 11.5 `test_gate_empty_target.py`
   - C#5 → Step 11.5 `test_no_fragility_stubs.py`
   - C#6 → Step 11.2 + skeleton, Phase 13.2 fixture
   - C#7 → Step 11.6 `test_retry_contract.py`
   - C#8 → Step 4.5 + 6.4 `test_threshold_registry.py` + arch-lint
   - C#9 → Step 2.4 + 2.6 `test_spec_roadmap_id_containment.py`
   - C#10 → Step 3.5 `test_anti_instinct_recurrence.py`
   All 8 Acceptance gates verified by Step 13.7 with explicit verification commands. No omissions.
4. **Weakened criteria (task softens BUILD-REQUEST asserts):** I checked the dual-write cutover (3 cycles) — Step 9.12 keeps Vector A's "≥3 consecutive parity-passing releases" strict. Fail-closed semantics — Step 10.2 explicitly states "NO `found=True` fallback like the deleted fidelity_checker.py:287-303 pattern — this is §MVR §4 explicit" and Step 11.4 deletes the fail-open. Step-count budget ≤14 enforced in Step 10.1, 10.3, PG10.1, PG11.1, 13.7. None of the criteria are softened. The only "softened" point is that R1.5's `verify-implementation` may need to consolidate `wiring-verification` or another step (Step 10.1 acknowledges this with "consolidation choice with rationale (cite step-count budget Acceptance Gate #6)" — the choice is deferred to design, but the budget IS enforced).
5. **Invented content (task adds features not in BUILD-REQUEST):** Several conveniences added but all trace to research/Vector citations:
   - `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (Step 11.4): traces to research/02 §6.2 cutover proposal. Not in BUILD-REQUEST verbatim but is the BUILD-REQUEST's "make SPEC_FIDELITY_GATE convergence-aware" framed concretely.
   - `superclaude.contracts.parsers` submodule (Step 11.2): BUILD-REQUEST §MVR §1 says "One `_parse_frontmatter` lives in the post-step extractor only" — task hoisted it to a shared parsers submodule per Contract #6. Reasonable, but slight invention (could have lived under `envelope.py`). NOT a violation.
   - `_ALLOWLIST_PHRASES` table option (Step 3.2): BUILD-REQUEST §R0 item 2 says "inline allowlist for known-safe noun uses" — the new table is one of three design options the design item considers. Acceptable.
   No invented content rises to the level of unauthorized scope creep.

---

## 15-Item Task File Qualitative Review Checklist

1. **Title + description match scope:** YES — title says "R0 Bridge + R1 Substrate Rewrite per master:§Verdict REWRITE", description covers Contract 1-10 + MVR.
2. **Frontmatter fields accurate:** YES — `coordinator: orchestrator`, `phasing: r0-then-r1`, `preserves:` / `inverts:` arrays match MVR §3.
3. **Prerequisites complete:** YES — 9 source-authority docs listed with paths and roles.
4. **Phase structure 1-step-per-checkbox:** YES — 70+ items, each single-action, no compound checklist items.
5. **Each item cites source authority:** YES — every R0/R1 implementation item cites BUILD-REQUEST § + master:§ + research file.
6. **Each item ends with status-update directive:** YES — "Once done, mark this item as complete" verbatim closure.
7. **Each item carries UV-only reminder when shell-touching:** YES — "REMEMBER: UV-only" present on every Bash-invoking item.
8. **Each item carries `src/superclaude/` first / no `.claude/` discipline when component-touching:** YES — Phase 12 explicitly enforces (Steps 12.1-12.5) plus reminder in Source areas.
9. **PR target = IronbellyOrg/IronClaude rule respected:** YES — Step 1.3 enforces, no PR-creation step bypasses (no `gh pr create` invocations in the task; task ends at task completion, PR creation is separate).
10. **Single-line bash commands:** YES — every Bash invocation is single-line. `2>&1 | tee <path>` pattern used for capture, no heredocs.
11. **Handoff convention used (phase-outputs/ subdirs):** YES — discovery/test-results/reviews/plans/reports subdirs documented and used consistently.
12. **QA gates use ADVERSARIAL STANCE + fix_authorization:** YES — every PG step uses "ADVERSARIAL STANCE: Assume ... fix_authorization: true." Halt-precedence guards explicit (regression → monotonicity → cap).
13. **Pre-fix MUST-FAIL / post-fix MUST-PASS tests for Contract #1:** YES — Step 2.6 (id containment), Step 3.5 (anti-instinct), Step 4.5 (threshold registry), Step 11.5 (fragility-stubs lint), Step 13.3 (recurrence regression). Each cites "Contract #1 invariant — verify by checking out the parent commit".
14. **Phase-gate cap behavior documented (max cycles + open-questions deferral):** YES — task-integrity gates cap at 2 cycles, qualitative gates cap at 3 cycles. Halt-precedence honored.
15. **Post-completion actions update frontmatter + log:** YES — Step 4 of Post-Completion updates `completion_date` + `status: 🟢 Done` + Execution Log entry.

All 15 checklist items pass.

---

## Coverage of Orchestrator's 6 Pre-Execution Questions

**Q1 — Does R0.2 actually unblock MultiModelSwarm?** YES with caveat. The task correctly defers allowlist data-structure choice to Step 3.2's design item (3 options: extend `_DESCRIPTOR_NOUNS`, extend `_DEMOTED_H3_SUBSECTIONS`, or new `_ALLOWLIST_PHRASES`). The seed cases (stub transport, stub-worker parallelism test, etc.) come from `multimodelswarm-fp-seeds.md` discovery (Step 3.1), which reads `.dev/releases/Current/MultiModelSwarm/anti-instinct-audit.md` (verified to contain the documented lines 207/211/213 matches). Step 3.8 then re-runs the live pipeline and confirms anti-instinct PASS. The Acceptance Gate #5 verification (Step 5.2) does a fresh pipeline run. The plan WOULD unblock if executed.

**Q2 — Does R0.3 seed contract constants R1.1 extends without double-definition?** YES. Step 4.2 creates `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES` verbatim from BUILD-REQUEST §MVR §5 with TODO marker for R1.1 extension. Step 6.2 extends with `RETURN_CONTRACTS` and full threshold registry. Arch-lint (Step 4.4 + Step 6.3) enforces no duplicate definitions. Step 4.3 explicitly migrates `id_registry._ID_PATTERN_KEYS` (created in Step 2.2 as a temporary local) to the contracts import — explicit handoff, no double definition.

**Q3 — Does R1.2 plan a credible dual-write migration with explicit cutover criteria?** PARTIAL. The dual-write design is in Step 7.1 with "1 release cycle" cutover criterion per BUILD-REQUEST §R1.2. However, unlike Step 9.12 (R1.4 cutover-decision document tracking 3-cycle counter), there's no explicit Step 7.5 tracking envelope dual-write cycle count. Step 11.4 (R1.6) implicitly assumes the envelope dual-write has matured. Flagged as I-4 above.

**Q4 — Does R1.4 sequence the 9 LLM steps for side-by-side validation?** YES. Steps 9.2-9.10 cover the 9 primary steps (extract, extract_tdd, generate, diff, debate, score, merge, spec_fidelity, wiring_verification), each as a parallel sub-phase with: schema file, Jinja template, dual-write flag, per-step parity test file. Sub-phase ordering matches BUILD-REQUEST §R1.4 sequencing. Step 9.11 covers the 3 secondary steps. Step 9.12 articulates 3-cycle cutover criterion. Each sub-phase explicitly preserves the markdown path during dual-write.

**Q5 — Does R1.5 correctly call into AST-walking fidelity_checker code?** YES. Step 10.2 explicitly calls `fidelity_checker._scan_codebase` (def at L165, called at L284 — task cites L284 which is the call site, accurate). The verify-implementation step iterates `envelope.spec_ids[FR]`, tries scan_codebase first, then importable-callable, then accepted_deviations. Fail-closed default explicit ("returns HIGH Finding if none match"). Step 11.4 then deletes the L287-303 fail-open block since R1.5 now provides the AST resolution path. Logical chain holds.

**Q6 — Does R1.6 correctly identify dual parsers / return-True stubs / fail-open defaults?** YES (after I-1 fix). Step 11.1 enumerates 6 frontmatter parsers (now with corrected `cli/` prefix), the 8 `obligation_scanner` return-True sites (correctly classified as VALID-HEURISTIC early-exits in `_is_meta_context`/`_has_discharge` per research/01 §A.4 — confirmed by Read of lines 712-744), the 7 `remediate_executor` return-True sites, both fail-open blocks in `fidelity_checker.py` (287-303 and 314-337 — both verified present), and the `gate=None` bypass at executor.py:2167. Step 11.3 honors per-site classification (no blind deletion). Step 11.4 deletes fail-open AND `gate=None` and creates `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` per research/02 §6.2.

---

## PRESERVE-Target Audit

| File                                        | LOC  | Task touches? | Verdict          |
| ------------------------------------------- | ---- | ------------- | ---------------- |
| `cli/roadmap/commands.py`                   | 401  | NO — listed as out-of-scope; every QA gate verifies unchanged | PRESERVED |
| `cli/roadmap/structural_checkers.py`        | 1069 | NO — listed as out-of-scope; QA gates verify unchanged        | PRESERVED |
| `cli/roadmap/convergence.py`                | 778  | NO modification — Step 7.2/PG7.1 explicitly forbid; only reads from it for `ConvergenceState` type imports | PRESERVED |
| `cli/roadmap/cosmetic_remediator.py`        | -    | NO — passthrough per MVR §2.8; PG11.1 verifies unchanged       | PRESERVED |

All PRESERVE invariants honored.

---

## Fixes Applied In-Place

**Fix #1 (I-1):** Edited `TASK-RF-20260531-042405.md` lines 605 and 609 to qualify `cli_portify/utils.py` and `audit/wiring_gate.py` paths with their `cli/` prefix. The corrected citations now read `cli/cli_portify/utils.py:parse_frontmatter` L11 and `cli/audit/wiring_gate.py:_extract_frontmatter_values` L931 in the cleanup inventory, and `src/superclaude/cli/cli_portify/utils.py` / `src/superclaude/cli/audit/wiring_gate.py` in the deletion list. This matches research/01 §A.3 §B at L237 and the actual file locations.

---

## Final Verdict

**VERDICT: PASS**

The task file is implementation-ready. It would execute cleanly against the current codebase to produce the claimed R0 + R1 deliverables. All 36 spot-checked line citations match the running source. The 10 Contract items are each mapped to specific test/lint creation steps. The 8 Acceptance gates are each mapped to a verification command in Step 13.7. The PRESERVE invariants (`commands.py`, `structural_checkers.py`, `convergence.py`, `cosmetic_remediator.py`) are honored across all 70+ items. The 6 frontmatter parsers, 8 + 7 return-True sites, 2 fail-open blocks, and 1 `gate=None` bypass listed for R1.6 cleanup all exist at the cited line numbers.

The single CRITICAL-eligible drift (I-1 cli/ prefix omission) has been fixed in-place. Three IMPORTANT items (I-2 step-count baseline arithmetic, I-3 R1.4 dynamic cutover, I-4 envelope cutover criterion fuzzy) are tracked-in-task or run-time verified — none halts execution. Four MINOR items (M-1 through M-4) are advisory and do not block.

Issues count: 1 fixed (I-1), 3 important deferred (I-2, I-3, I-4 — all tracked or runtime-verified), 4 minor advisory (M-1 through M-4).

Fixes applied: 1.

# Research Completeness Verification

**Task:** TASK-RF-20260522-153212 (cliEval post-sprint remediation MDTM build)
**Date:** 2026-05-22
**Files analyzed:** 4 (01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-template-examples.md)
**Analysis type:** Research completeness verification (pre-build quality gate)
**Track goal:** Build MDTM task file implementing the cliEval remediation spec (5 High + 6 Medium + 3 cross-cutting + 9 new tests, target module `src/superclaude/cli/eval/`)

---

## Verdict: PASS-with-minor-gaps (research is materially complete; flagged issues are deltas-from-spec that the BUILDER must surface in the task, not research-blocking)

The four research files collectively provide ground-truth coverage of every spec finding (H1-H5, M1-M6, CC1-CC3, T1-T9) with verbatim file:line citations. R1's "zero drift" claim was spot-checked at four cited offsets and verified. The gaps flagged below are NOT missing research — they are research findings that document divergences between the spec text and the actual code/test surface; the builder must encode these divergences as explicit checklist items / notes rather than silently papering over them.

---

## Per-Criterion Findings

### Criterion 1 — Source files identified with paths and exports? **PASS**

R1 (file-inventory) enumerates ALL 8 spec-target source files plus `exit_codes.py` (new), with current line counts (commands.py 1950L, coverage.py 348L, etc.) and a per-symbol table for each module. Every spec-cited symbol verified at its current offset:
- commands.py: 24 symbols verified (RUN_*_EXIT_CODE × 3, doctor option, _utc_iso_now, _new_run_id, _default_output_dir, _can_install_signal_handler, _NullLifecycleExecutor, _resolve_executor_factory, _run_one_spec, HomeIsolation construction block, _compute_run_stats, _format_run_summary_line, eval_run Click options, output-dir resolution block, resolve_scratch_root call, mkdir block, AC12 allowlist extension, Reporter.write call, three sys.exit branches).
- coverage.py: 3 symbols + silent-green block verbatim quote.
- config.py: 9 symbols + L243-249 prefix-equals branch verbatim.
- artifact_layout.py: 12 symbols incl. _EVAL_ID_RE at L99.
- reporter.py: 6 symbols + artifact-set inventory for H3.
- run_report.py: 8 symbols + artifact-set inventory for H3.
- isolation.py: 4 symbols incl. containment_guard at L220 (the H5 second site).
- loader.py: 11 symbols incl. EVAL_ID_REGEX at L86-88 (the CC1 divergence partner).

R3 supplements with 11 named exit-code constants (vs spec's "7 magic 2s"), the EVAL_STATUSES SoT chain in models.py:49-62, and the H5 allowlist call-graph.

**Evidence:** 01-file-inventory.md (entire file); 03-integration-points.md §§1.2, 2.1, 3.1.

### Criterion 2 — Output paths/formats clear; each T1-T9 has target test file recommendation? **FAIL (partial)**

R2 §E.2 ("Per-T# recommended target file") provides target test files for ONLY T1, T2, T8 in R2's own numbering scheme. **R2's T# numbering does NOT match the spec's T1-T9 mapping** (verified by reading spec §6):

| Spec T# | Spec test name | Spec finding | R2 coverage |
|---|---|---|---|
| T1 | `test_eval_run_output_dir_anchors_compose_run_dir` | H1 | NOT addressed |
| T2 | `test_format_run_summary_line_errored_interrupted_timeout` | H3 | Covered (R2's "T2") |
| T3 | `test_coverage_gate_fails_on_corrupt_settings_json` | H2 | Covered as R2's "T1" |
| T4 | `test_home_root_mkdir_after_allowlist_extension` | H5 | NOT addressed |
| T5 | `test_resolve_scratch_root_rejects_bare_prefix` | H4 | Covered as R2's "T8" |
| T6 | `test_null_lifecycle_executor_logs_warning_when_active` | M2 | NOT addressed (R2 §C.3 sketches stderr idiom but no target file) |
| T7 | `test_session_id_owned_by_orchestrator_not_command` | M5 | NOT addressed |
| T8 | `test_eval_id_pattern_single_source` | CC1 | NOT addressed |
| T9 | `test_no_magic_exit_codes_in_eval_module` | CC2 | NOT addressed |

R2 §E.2 row "T3-T7, T9" defers explicitly: *"not specified in this brief — R1 owns file inventory; this researcher recommends test_eval_run.py for CLI-flag tests, test_coverage_gate_integration.py for end-to-end gate tests, test_eval_lifecycle.py for runner status mapping."* This is a soft recommendation by surface category, not a concrete per-T# target file. **Severity: Important.** The builder can infer the missing targets from R2's category mapping + R1's file inventory, but the inference work is non-trivial:

- T1 (output_dir anchors compose_run_dir) → likely `tests/cli/eval/test_eval_run.py` (CLI flag test) — inferable.
- T4 (home_root mkdir after allowlist) → likely `tests/cli/eval/test_scratch_root_policy.py` or new file — needs builder decision.
- T6 (NullLifecycleExecutor warning) → likely `tests/cli/eval/test_eval_run.py` or `test_eval_lifecycle.py` — needs builder decision.
- T7 (session_id ownership) → likely `tests/cli/eval/test_eval_lifecycle.py` — inferable.
- T8 (eval_id_pattern_single_source) → likely `tests/cli/eval/test_eval_id_regex.py` (already pins EVAL_ID_REGEX at :32, :45) — inferable from R1 §H + R3 §2.1 citations.
- T9 (no_magic_exit_codes_in_eval_module) → likely `tests/cli/eval/test_exit_codes.py` — inferable from R1 §I + R3 §1.2 (test_exit_codes.py is the TEST-008/T04.19/D-0079 pin).

**Recommendation:** Builder should produce a concrete target-file decision for each of T1, T4, T6, T7, T8, T9 using R1 inventory + R2 category guidance, and document those decisions in the task's Phase 2 (test scaffolding) checklist items. This is NOT research-blocking because the inputs to make the decision ARE present — but a per-T# table would have been cleaner research output.

**Evidence:** 02-patterns-conventions.md §E.2 (lines 364-372), 489 (cheatsheet defer row); spec §6 table.

### Criterion 3 — Logical breakdown of phases/steps present (R4 6-phase decomposition)? **PASS**

R4 §C.1 explicitly recommends a 6-phase collapse of the spec's 8 phases, with rationale and mapping:
- Phase 1 = Preparation & Discovery (mirrors P1 Phase 1 + P4 Step 1.3 baseline pattern)
- Phase 2 = Test Scaffolding (spec Phase 1)
- Phase 3 = Correctness + Observability (spec Phases 2+3 merged)
- Phase 4 = Layout + Ordering refactor (spec Phases 4+5 merged)
- Phase 5 = Click symmetry + cross-cutting cleanup (spec Phases 6+7)
- Phase 6 = Final Regression + AC Matrix + Completion (spec Phase 8)

R4 also notes the 8-phase fidelity option is acceptable and the prior-task idiom skews toward fewer denser phases (P3=7 phases over 440 LOC, P4=7 phases over 50 LOC). PG-gate placement recommended: PG-1 between Phase 2→3, PG-2 between Phase 4→5, PG-FINAL inside Phase 6 (matching P2's 3-gate cadence).

**Evidence:** 04-template-examples.md §§C.1, B.4.

### Criterion 4 — Patterns/conventions documented with examples? **PASS**

R2 is dedicated to this — every convention has cited examples:
- Fixture conventions (§A): three idioms `tmp_path` / `allowlisted_output_dir` / nested `scratch_root`, each with file:line examples (conftest.py:24-39, test_eval_run.py:223, test_home_isolation.py:62-68).
- Corrupt settings.json construction (§A.2): exact reproduction recipe with `bad.write_text("{not json", encoding="utf-8")` (test_coverage_gate.py:160-165).
- Mocking pattern (§A.3): full verbatim `clean_host` fixture body + the lighter `clean_claude_home` variant.
- Status taxonomy (§A.4): two parameterization idioms with file:line.
- Assertion idioms (§B): `assert is True/False` (never bare truthy), `pytest.raises` (with `as excinfo` when attributes asserted), `pytest.warns` NOT used (use stderr content checks instead).
- Click idioms (§C): `CliRunner()` zero-arg post-mix_stderr migration; `result.stdout` vs `result.stderr` vs `result.output` separately addressable with diagnostic fallback `result.output + (result.stderr or "")`.
- Logging idiom (§D): zero `logging.getLogger` anywhere; all observability via `click.echo(..., err=True)` with command-name prefix pattern (`eval doctor: ...`, `eval run: ...`).
- Test naming (§E.1): long snake_case intent-revealing names averaging 40-70 chars; spec-proposed names match this style.
- Test order (§F.1): banner-grouped sections, NOT bottom-append; specific banner targets cited per test.
- Pytest markers (§F.2): no custom markers in `tests/cli/eval/`; `pytest_plugin.py` auto-markers do NOT apply because tests/cli/eval/ is not under /unit/ or /integration/.

**Evidence:** 02-patterns-conventions.md §§A-F (entire file).

### Criterion 5 — MDTM template notes cited (A3/A4/B2/L1-L6) with template line numbers? **PASS**

R4 §A cites the template exhaustively with line numbers:
- Frontmatter fields table mapping each field to template lines 1-44.
- A3 COMPLETE GRANULAR BREAKDOWN — verbatim quote, template lines 91-95.
- A4 ITERATIVE PROCESS STRUCTURE — verbatim quote with X.1/X.2/X.3 pattern, template lines 97-116.
- B2 self-contained item pattern — six elements enumerated, template lines 142-148.
- B3 paragraph format — line 150-153.
- L1-L6 handoff patterns — discovery/build/test/review/conditional/aggregation each with template line range (737-747, 749-759, 761-771, 773-783, 785-797, 799-809).
- L7 pattern selection guide — lines 811-835.
- M1 phase-gate QA sequence — lines 843-850.
- Mandatory sections table — every section mapped to its template line.
- I15 (line 599-607), I16 (609-624), I17 (626-635), I18 (637-646) — process rules with citations.

**Evidence:** 04-template-examples.md §A (entire section).

### Criterion 6 — Granularity sufficient for per-file/per-component checklist items? **PASS (with one gap-driven build-item requirement)**

For each H/M/CC finding, the builder has the inputs needed:

- **H1** (output-dir anchors compose_run_dir): R1 cites L1710-1714 (resolution block), L1727-1730 (resolve_scratch_root call), L1735 (mkdir). R3 §4.2 quotes the surrounding 1727-1752. Builder can author surgical edits.
- **H2** (fail-closed coverage gate): R1 §B quotes L294-302 verbatim with the three silent-green branches identified (missing file / OSError|JSONDecodeError / non-Mapping). Builder can split the three branches with the recommended "keep missing-file silent; log+exit-non-zero for the other two."
- **H3** (run-summary taxonomy): R1 §F documents that Reporter.write writes summary.yaml at L210/214 but write_aggregated_report does NOT (intentional per L335 docstring). R3 §3.4 quotes the hardcoded P/F/S format at L1532-1539. Builder can author the new format with errored/interrupted/timeout buckets.
- **H4** (bare-prefix rejection): R1 §C identifies that test coverage ALREADY EXISTS at `tests/cli/eval/test_scratch_root_allowlist.py:52` (`test_accepts_tmp_eval_runs_root_itself`); the spec's T5 is to INVERT this test (R2 §A.3 documents `pytest.raises(ScratchRootViolation)` idiom). Builder can author.
- **H5** (mkdir-before-allowlist-extension): R1 §A pins L1735-1746 + R1 §G pins isolation.py L220+ containment_guard. **R3 §4.7 surfaces the critical finding that there are TWO H5 sites — commands.py:1737 AND isolation.py:533** — with the second site being higher-risk because it mutates on-disk state before containment_guard runs. The builder MUST emit one checklist item per site (R3 explicitly recommends this).
- **M1-M6:** R1 + R3 cover the symbols needed (e.g. M5 session-id ownership at R1 §A note about L1442-1446 `session_id=f"sess-{spec.id}"`). The builder can author per-finding items.
- **CC1** (regex unification): R1 §H + R3 §2.2 both surface the SEMANTIC DIVERGENCE (not duplication). R3 §2.3 gives a 10-step consolidation recipe. Builder must encode the "single regex" vs "two-layer guard" choice as an explicit open question (see Criterion 9).
- **CC2** (exit-code consolidation): R3 §1.2 catalogues all 11 (not 7) `*_EXIT_CODE = 2` constants across 6 files with file:line, plus R3 §1.5 gives the file-by-file rewrite map. Builder has everything needed.
- **CC3** (NullLifecycleExecutor observability): R2 §D.2 documents the click.echo(err=True) idiom + R1 §A pins `class _NullLifecycleExecutor` at L1361-1387. Builder can author the WARNING emission.
- **T1-T9:** R2 §A-F provides test idioms; per-T# target files have the Criterion-2 gap (see above).

**Evidence:** as cited above. The H5 split into two sites is a research finding the builder MUST surface as two distinct checklist items rather than one — flagged here so the builder doesn't collapse them.

### Criterion 7 — Documentation cross-validation: doc-sourced claims tagged + R1's zero-drift claim verified? **PASS**

R1's headline (lines 8-19) states *"Spec line numbers are ACCURATE — every cited symbol verified in place. All 18 symbols cited in `remediation-spec.md` were re-Read at the cited offsets and matched the spec's coordinates within ±5 lines."* This claim was **independently spot-checked** by re-reading four representative sites:

| R1 claim | Spot-check result |
|---|---|
| commands.py:570/573/577 RUN_*_EXIT_CODE trio | **VERIFIED** — `RUN_CLEAN_EXIT_CODE: int = 0` at L570, `RUN_FAILURES_EXIT_CODE: int = 1` at L573, `RUN_INTERRUPTED_EXIT_CODE: int = EXIT_INTERRUPTED` at L577. Matches R1's quotes byte-for-byte. |
| commands.py:1442-1446 HomeIsolation session_id construction | **VERIFIED** — `home = HomeIsolation(eval_id=spec.id, home_root=home_root, session_id=f"sess-{spec.id}",)` matches R1 byte-for-byte. |
| commands.py:1735-1746 H5 mkdir-before-allowlist-extension region | **VERIFIED** — `resolved_output.mkdir(parents=True, exist_ok=True)` at L1735, `home_root = resolved_output / "homes"` L1736, `home_root.mkdir(parents=True, exist_ok=True)` L1737, allowlist extension `runtime_allowed = tuple(base_config.allowed_scratch_roots) + (resolved_output, home_root,)` at L1743-1746. Exact match. |
| isolation.py:530-533 second H5 site (R3 finding) | **VERIFIED** — `# Ensure the scratch root exists. ...` comment L530-532; `self.home_root.mkdir(parents=True, exist_ok=True)` at L533. Matches R3 §4.6 byte-for-byte. |

R1's zero-drift claim is **genuine and confirmed**. Where the spec's coordinates were ranges (e.g. `_format_run_summary_line` cited as L1526-1539), R1 read the entire range and confirmed body match. Where spec values were single lines (e.g. L570), R1 quoted the verbatim line content.

**Doc-staleness tagging:** This research is grounded against current code as the SoT (spec was generated from snapshot `snapshot-src-superclaude-cli-eval-20260522142818` — same day as research). R1 explicitly tags the THREE divergences from spec text:
1. *"CC1 is a regex divergence, not pure duplication"* (R1 §H) — `[CODE-CONTRADICTED]` equivalent.
2. *"resolved_output mkdir test lives in test_scratch_root_allowlist.py:52, NOT test_config.py as one reading of the spec might suggest"* (R1 §C) — `[CODE-CONTRADICTED]`.
3. *"Reporter.write writes summary.yaml; write_aggregated_report does NOT — divergence is intentional per docstring"* (R1 §E/F) — `[CODE-VERIFIED with caveat]`.

R3 surfaces two additional divergences:
4. *"Spec says '7 magic 2 literals' — actual count is 11 named constants across 6 files"* (R3 §1.2 + §1.5 closing note) — `[CODE-CONTRADICTED]`.
5. *"H5 has a second site at isolation.py:533"* (R3 §4.6) — `[CODE-VERIFIED additional finding]`.

All five divergences are surfaced explicitly; none are silently assumed.

### Criterion 8 — Solution research evaluated approaches? **N/A (correctly skipped)**

The spec IS the solution — this is a remediation against a written spec produced by `/sc:auggie-review`. No greenfield design choice exists. R4 §C.1 still surfaces a phase-count CHOICE (6 vs 8) with rationale and trade-offs, which is the right level of solution exploration for a remediation task.

### Criterion 9 — Unresolved ambiguities documented (not silently skipped)? **PASS**

Three findings from the researchers REFINE the spec, and each is **explicitly flagged for the builder**:

- **CC1 regex is divergence, not duplication** — R1 §H lines 267-286, R3 §2.2 (the critical-finding callout box with the acceptance-set table), R3 §2.3 enumerates "two possible interpretations" (single-regex tightening vs two-layer co-location) and warns *"the spec language combined with the strict-pattern test pin suggests interpretation #1 is intended, but builder MUST flag the semantic divergence rather than silently swap A's pattern for B's."* This is exactly the right disposition — defer to builder to raise as an OPEN QUESTION in the task.

- **CC2 is 11 constants, not 7 literals** — R3 §1.5 closing note: *"Eleven occurrences total — the spec's '7 magic 2s' undercounts. Builder should verify spec wording against this map; if the spec literally enumerates seven, the four others (HARD_FAIL_EXIT_CODE, SUITE_NOT_FOUND_EXIT_CODE, EVAL_NOT_FOUND_EXIT_CODE, DISK_BUDGET_EXCEEDED_EXIT_CODE) may have been omitted by oversight or intentionally scoped out — flag for clarification."* Explicit flag-for-builder.

- **H5 has a second site at isolation.py:533** — R1 §G lines 240-248, R3 §4.6-4.7 (the operations-order summary table with risk assessment per site). R3 explicitly recommends *"The builder should produce one checklist item per site, plus one per-call-site test."*

These three findings should appear as **Open Questions** in the eventual MDTM task (per R4's mandatory-sections inventory which includes Open Questions in P3/P4-style tasks).

---

## Documentation Staleness Tagging Audit

The research files don't use the literal `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` tags as syntactic markers, but every doc-sourced claim is grounded against current code with quoted line content. R1's headline IS the verification tag for the spec body. No untagged doc-sourced architectural claims found in the four files.

---

## Completeness Audit (per-file)

| File | Status field | Summary/Headline | Key Takeaway | Gaps Section | Verdict |
|---|---|---|---|---|---|
| 01-file-inventory.md | "Complete" (L4) + drift summary section L316-329 | Headline at L8-19 + section per file | Implicit (drift summary serves as takeaways) | Three deltas-from-spec flagged inline | Complete |
| 02-patterns-conventions.md | "In Progress" at frontmatter L7 BUT "Status: Complete" at body L521 + "Key takeaway" L532-540 | Has Per-T# cheatsheet § | Yes (L532-540) | T3-T7,T9 defer noted at L488 + L511 | Complete (despite frontmatter mismatch — minor metadata bug) |
| 03-integration-points.md | "in-progress" at L5 BUT "Complete." at L569 + "Key surprises" L572-577 | Yes (Key surprises section) | Yes (4 numbered surprises) | None — all divergences ARE the takeaways | Complete (same frontmatter/body status mismatch as R2) |
| 04-template-examples.md | No explicit Status field (implicit complete) | §E Summary Handoff for the Builder L356-373 | Yes (§E + anti-patterns §D) | None needed (synthesis file, not investigation file) | Complete |

**Minor metadata gap:** R2 and R3 have a frontmatter `Status: In Progress` while the body declares `Status: Complete`. Severity: cosmetic. Does NOT affect builder usability. Flag for researcher hygiene, not a research-blocking issue.

---

## Contradictions Found

**No internal contradictions between research files.** R1, R2, R3, R4 are mutually consistent:
- R1's "spec line numbers are accurate" aligns with R3's per-symbol verification of CC1/CC2/H5 sites.
- R2's banner-grouped test order aligns with R4's per-T# placement guidance.
- R3's H5 two-site finding extends but does not contradict R1's containment_guard documentation.
- R4's recommended 6-phase collapse aligns with R2's per-T# fixture/banner placement recommendations.

The spec text vs reality divergences (CC1 regex semantics, CC2 11-vs-7 count, H5 second site, R2 T# misalignment vs spec T#) are uniformly surfaced rather than hidden.

---

## Depth Assessment

Stated track goal implies Deep tier (5 High + 6 Medium + 3 cross-cutting + 9 new tests = substantive remediation scope). Achieved depth:
- **Symbol-level inventory:** YES (R1 — 75+ symbols across 8 files with line numbers + quotes).
- **Pattern documentation with verbatim idiom citations:** YES (R2 — 6 idiom categories with file:line examples each).
- **Call-graph traces:** YES (R3 — four full maps for CC1/CC2/H3/H5 with verbatim region quotes).
- **Pattern-library cross-reference to prior tasks:** YES (R4 — 4 cliEval-P* tasks compared on 6 dimensions plus template citations).

Depth IS sufficient. No depth elements missing for the builder's needs.

---

## Compiled Gaps

### Important Gaps (affect builder quality; must still be fixed)

1. **G-IMPORTANT-1: Missing per-T# target file for T1, T4, T6, T7, T8, T9.** R2 §E.2 covers T1/T2/T8 in R2's own numbering (which is misaligned with the spec). Six of nine spec T#s have only soft category guidance (R2 §E.2 row "T3-T7, T9"). Builder must produce concrete target-file decisions from R1 inventory + R2 category guidance. **Recommendation:** Builder produces a 9-row Phase 2 enumeration table in the task file listing `T# | spec name | target file | banner section | fixture | assert style`, even if some rows say "NEW FILE" or "JUDGEMENT CALL".

2. **G-IMPORTANT-2: T2/T3/T5 vs T1/R2-T2/T8 numbering mismatch.** R2's "Per-T# Final Recommendations" table at L484-489 uses T#s that DO NOT match the spec §6 T1-T9 enumeration. The work R2 did IS valid (the three named tests are real spec entries — just under different T#s), but the builder must NOT copy R2's T-numbering verbatim into the task file. **Recommendation:** Builder remaps using the spec §6 table as the authoritative T# source (which I verified above).

### Minor Gaps (cosmetic / hygiene)

3. **G-MINOR-1: Frontmatter Status drift in R2 and R3.** Both declare `Status: In Progress` in the file header but `Status: Complete` in the body. **Recommendation:** Researcher hygiene — update frontmatter to match body. Does not affect builder.

### Builder-must-surface Findings (not gaps in research; gaps in the spec that research uncovered)

4. **G-BUILDER-1: CC1 is regex divergence, not duplication.** R1 §H + R3 §2.2. Builder MUST surface as an Open Question in the task: "Single-regex consolidation (tightens artifact_layout acceptance set) vs two-layer co-location (keeps both with disambiguating names)?"

5. **G-BUILDER-2: CC2 is 11 constants across 6 files, not 7 in commands.py.** R3 §1.2 + §1.5. Builder MUST surface as Open Question: "Are HARD_FAIL_EXIT_CODE, SUITE_NOT_FOUND_EXIT_CODE, EVAL_NOT_FOUND_EXIT_CODE, DISK_BUDGET_EXCEEDED_EXIT_CODE in scope for CC2?" — and produce the 11-row file-by-file rewrite map regardless.

6. **G-BUILDER-3: H5 has two mkdir-before-guard sites.** R1 §G + R3 §4.6-4.7. Builder MUST emit two H5 checklist items (commands.py:1737 low-risk + isolation.py:533 higher-risk) plus T4 should test BOTH sites or there should be a T4a/T4b split.

---

## Recommendations to Builder

1. **Use the spec §6 T-table as authoritative T# numbering** — NOT R2's per-T# cheatsheet which uses a different numbering. R2's three concrete recommendations (target file, banner, fixture, assert style) remap to spec T3 (corrupt-settings), spec T2 (format_run_summary_line), spec T5 (bare-prefix).
2. **Emit Open Questions section** with G-BUILDER-1, G-BUILDER-2, G-BUILDER-3.
3. **For T1, T4, T6, T7, T8, T9 file targets** — apply R2 §E.2 category guidance + R1 inventory:
   - T1 → `tests/cli/eval/test_eval_run.py` (CLI flag test class)
   - T4 → split: T4a `tests/cli/eval/test_eval_run.py` for commands.py:1737 site; T4b `tests/cli/eval/test_home_isolation.py` for isolation.py:533 site
   - T6 → `tests/cli/eval/test_eval_run.py` or `test_eval_lifecycle.py` — builder judgement based on which file owns _NullLifecycleExecutor surface tests
   - T7 → `tests/cli/eval/test_eval_lifecycle.py` (lifecycle owns session_id ownership)
   - T8 → `tests/cli/eval/test_eval_id_regex.py` (already imports EVAL_ID_REGEX at L32)
   - T9 → `tests/cli/eval/test_exit_codes.py` (TEST-008/T04.19/D-0079 pin)
4. **Adopt R4's 6-phase decomposition** (§C.1) — or use 8 phases if literal spec fidelity preferred.
5. **Per-phase verify cadence per R4 §C.2** — all 3 spec §9 gate commands embedded via `ensuring … EXIT_CODE=0 …` clauses (NOT separate `Verify:` items).
6. **Emit Execution Context block** per R4 §C.3 (6+ source areas trigger auto-emission).
7. **Per-QA-gate item:** include ADVERSARIAL STANCE + ESCALATION OVERRIDE + Retry Monotonicity Protocol per R4 §D.4-D.5 + user memory `feedback_rfqa_adversarial_pattern.md`.
8. **Phase 1 baselines mandatory** per R4 §D.1 — capture pytest + verify-sync + ruff baseline BEFORE any edit.

---

## VERDICT: PASS

**Rationale:** All four research files are materially complete with verbatim file:line citations, R1's zero-drift claim is genuine (spot-checked 4/18 cited symbols — all matched byte-for-byte), conventions are documented with examples, template patterns are cited with line numbers, granularity is sufficient for per-finding checklist items, doc cross-validation is grounded against current code, and the THREE spec-vs-reality divergences (CC1 regex, CC2 count, H5 second site) are explicitly flagged for the builder rather than silently assumed.

The Important gap (G-IMPORTANT-1, G-IMPORTANT-2: missing per-T# concrete target file for 6 of 9 spec T#s + T-numbering mismatch in R2's cheatsheet) is a quality-of-life gap, NOT a research-blocking gap. The inputs to make per-T# decisions ARE present in R1 + R2's category guidance + R2's idiom library; the builder can produce concrete target files by applying R2 §E.2 category rules to the spec §6 T-table. The PASS verdict is conditional on the builder explicitly producing per-T# target-file decisions and surfacing G-BUILDER-1/2/3 as Open Questions in the resulting MDTM task.

If the builder wishes to be conservative, spawning a 30-minute supplementary researcher to produce the 9-row T# target-file table would close G-IMPORTANT-1 cleanly — but this is optional, not required.

# Research Completeness Verification

**Topic:** Sprint-runner 6-fix task-builder track (C1: stall_timeout + watchdog split; C2: per-task output collision; C3: timeout-formula reconciliation; C4: phase_start JSONL emission; deferred: C5 --no-session-persistence removal, C6 fan-out injection)
**Date:** 2026-05-18
**Files analyzed:** 5 (01-file-inventory.md, 02-patterns-and-conventions.md, 03-integration-points.md, 04-template-and-examples.md, 05-test-and-verification.md)
**Depth tier:** Standard
**Analyst:** rf-analyst (single instance, no team context)

---

## Verdict: PASS WITH MINOR FLAGS

All nine completeness checks pass; no Critical gaps would block the task-builder from generating a sound MDTM task file. Three Minor issues are surfaced for the builder to address inline (file-status mislabel; one cross-cutting ambiguity about C4's intent; one residual ambiguity about C1's "watchdog split" definition). Spot-checks of the three flagged file:line citations all VERIFIED true to source. Synthesis of the 4-fix track is well-evidenced and internally consistent.

---

## Spot-Verification of Critical Citations

| # | Claim Source | Cited Location | Expected | Verified | Verdict |
|---|---|---|---|---|---|
| 1 | R1 §2 | `models.py:469-476` defines `output_file()`/`error_file()`/`result_file()` accepting only `Phase` | Helpers take only `Phase`, no per-task variant | Read shows lines 469-476 contain exactly those three helpers, each accepting only `phase: Phase` | VERIFIED |
| 2 | R3 IP-4 | `executor.py:1262-1300` (per-task branch) has NO `write_phase_start` call | Per-task block only calls `write_phase_result` at the end, no `write_phase_start` | Read of lines 1255-1300 confirms: branch enters at 1262, sets `started_at` at 1263, calls `tui.update` 1265, `execute_phase_tasks` 1266, ends with `write_phase_result(phase_result)` at 1297. ZERO `write_phase_start` call in this block. | VERIFIED |
| 3 | R5 §1, §8 | Tests live in `tests/sprint/` not `tests/cli/sprint/` | `tests/cli/sprint/` does not exist; `tests/sprint/` does | `ls tests/cli/sprint/` returns error; `tests/sprint/` listing shows 22+ test files including `test_watchdog.py`, `test_executor.py`, `test_e2e_success.py`, `test_regression_gaps.py`, `test_process.py` etc. | VERIFIED |

Bonus spot-checks (because they appear in multiple researchers' findings):

| # | Claim | Verified | Notes |
|---|---|---|---|
| 4 | `executor.py:86` contains `timeout_seconds=self._config.max_turns * 60` | VERIFIED at exact line 86 | Inside `SprintGatePolicy.build_remediation_step` |
| 5 | `executor.py:1106` contains `timeout_seconds=config.max_turns * 120 + 300` | VERIFIED at exact line 1106 | Inside `_run_task_subprocess` |
| 6 | `executor.py:1328` contains `logger.write_phase_start(phase, started_at)` | VERIFIED at exact line 1328 | Inside per-phase fallback branch, AFTER `proc_manager.start()` but BEFORE poll loop |

All citations land within ±0 lines of researcher claims. Research is unusually precise.

---

## Coverage Audit

Track goal: **4 fixes (C1, C2, C3, C4) + 2 deferred (C5, C6).** Each fix requires (a) source-code touchpoints; (b) caller graph / blast radius; (c) conventions to copy; (d) template/MDTM rules; (e) test fixtures + recipes.

| Scope item | Covered by | Status |
|---|---|---|
| C1 — `stall_timeout` default | R1 §1, R3 IP-1, R5 §5 | COVERED |
| C1 — watchdog split (startup vs idle) | R3 IP-5, R5 §6 C1 | PARTIAL — see Minor Gap #3 |
| C2 — per-task output collision (source site) | R1 §3 + §7, R3 IP-2/IP-3, R5 §5 | COVERED |
| C2 — `output_file()` / `error_file()` helper location (models.py) | R1 §2 (explicit "NOT in fix-scope but contains" callout), R3 IP-2 | COVERED |
| C3 — timeout-formula reconciliation | R1 cross-cutting §3, R3 IP-7+IP-8, R5 §5+§6 C3 | COVERED |
| C4 — `phase_start` JSONL emission | R1 §5, R2 §5, R3 IP-4, R5 §5+§6 C4 | COVERED — see Minor Gap #2 |
| Patterns (dataclass, subprocess, JSONL, debug_log, time.monotonic, stderr) | R2 §1-§8 | COVERED |
| Lint / format / ruff rules | R2 §10 | COVERED |
| Tests directory location | R5 §1 | COVERED (corrects assumption that tests live at `tests/cli/sprint/`) |
| Subprocess-mock recipe | R5 §3 | COVERED (verbatim from `test_watchdog.py:49-117`) |
| JSONL assertion recipe | R5 §4 | COVERED (verbatim from `test_regression_gaps.py:499-523`) |
| Real-subprocess stand-in recipe (for C2) | R5 §3 example 2 | COVERED (verbatim from `tests/pipeline/test_process.py:176-193`) |
| MDTM Template 02 A-M rule catalog | R4 §1-§2 | COVERED |
| TB-Add-1..8 structural checks | R4 §5 | COVERED |
| Prior task examples (CLI-modifying) | R4 §3 examples A/B/C | COVERED |
| B2 6-element item schema (verbatim) | R4 §6 | COVERED |
| L-pattern composition / M1 QA gate | R4 §4 | COVERED |
| Phase / step phasing recommendation | R4 §4 | COVERED |
| `make sync-dev` applicability | R5 §8 | COVERED (correctly negative — NOT needed) |
| C5 (deferred) location for documentation | R1 §7, R3 IP-6 | COVERED |
| C6 (deferred) | R3 cross-cutting summary | PARTIAL — see Minor Gap #1 |

---

## Evidence Quality

| Research file | Evidenced claims | Unsupported / vague claims | Quality |
|---|---|---|---|
| 01-file-inventory.md | ~50 claims, all with `file:line` and code excerpts | 0 | Strong |
| 02-patterns-and-conventions.md | ~45 claims with `file:line` + code blocks | 0 — every convention shows ≥1 verbatim example | Strong |
| 03-integration-points.md | ~70 claims; every callsite cited with `file:line`; blast radius table per IP | 1 — IP-5 cites `executor.py:1336-1417` watchdog but says "per-task path has NO equivalent watchdog" without naming an exact line where per-task subprocess code currently sits (line ranges given in IP-3 cover that; cross-readable). Not a real gap. | Strong |
| 04-template-and-examples.md | ~80 claims; every template rule cites template line range | 1 — Status field at top reads "**Status:** In Progress" (yet body is clearly complete with closing "Status: Complete" line at end). See Minor Gap #1. | Strong (content) / Weak (status header) |
| 05-test-and-verification.md | ~55 claims, all anchored to test file paths + line ranges; key code citations re-verified at end | 0 | Strong |

**Ratio overall:** ~300+ evidenced claims vs ~2 unsupported = excellent. No vague architectural hand-waving; every claim grounds in a `file:line`.

---

## Documentation Staleness

This is code-internal research, not documentation-sourced research. Researcher 3 (R3) does mention docs that would need updating IF defaults change (`docs/sprint-cli-deep-dive.md:131-132`, `docs/developer-guide/sprint-tui-reference.md:541-542`, `docs/generated/sprint-cli/02-data-models.md:249`, `docs/analysis/gsd-vs-superclaude-comparison.md:407`), but these are not load-bearing source claims for the builder; they are downstream consumers to be updated as part of the fix.

No `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags appear in any research file. This is acceptable per the checklist (item 7) — these are code-research files, not doc-sourced architecture claims.

**N/A — no doc-sourced claims to verify.**

---

## Completeness Check (Per-File Status / Sections)

| Research file | Status header | Summary section | Gaps / open-questions section | Key takeaways | Verdict |
|---|---|---|---|---|---|
| 01-file-inventory.md | Complete | ✓ "Summary Table" + "Cross-cutting Findings" (6 numbered items) | Embedded in cross-cutting findings (e.g. "flag this if the task builder is to scope the change accurately") | ✓ Six numbered findings | Complete |
| 02-patterns-and-conventions.md | Complete | ✓ "Summary" section at end with 7 bulleted rules | None as explicit section, but normative rules act as the gap-fillers | ✓ Summary bullets | Complete |
| 03-integration-points.md | Complete | ✓ "Cross-Cutting Summary" table + "Test files most exposed" | Each IP-* section has explicit "Mitigation" subsection | ✓ Cross-Cutting Summary | Complete |
| 04-template-and-examples.md | **In Progress** (per header) — but body has "Status: Complete" closing line at line 354 | ✓ "Summary for the Builder" (8 numbered items) | None explicit; rules act as the gap-fillers | ✓ Summary | Substantively Complete (header/footer disagreement — see Minor Gap #1) |
| 05-test-and-verification.md | Complete | ✓ "Summary" (7 numbered findings) | None explicit; recipes describe what to add, implicitly noting current absences | ✓ Summary | Complete |

**Flag (Minor):** R4 header is `Status: In Progress` (line 6) but closing footer is `**Status: Complete**` (line 354). The body is comprehensive (Sections 1-6 cover all template rules + examples + B2 schema). Treat as Complete; ask researcher 4 or builder to fix the header for hygiene.

---

## Cross-Reference Check

The five files cite each other coherently:

- R1 §2 explicitly defers `output_file()` location to "models.py:469-476" — verified, and R2 §2 quotes the same lines and R3 IP-2 takes them as its primary target. Three-researcher agreement.
- R1 cross-cutting §3 lists THREE timeout formulas; R3 IP-8 enumerates the same three with identical line numbers; R5 §5 cites the same three sites. Triple corroboration.
- R1 §3 calls out `_run_task_subprocess` (executor.py:1076-1115); R3 IP-3 traces caller chain to `execute_phase_tasks` (the only caller); R5 §6 C2 prescribes test recipes for the new per-task path. End-to-end coverage.
- R2 §5 documents the `_jsonl` append-only sink; R3 IP-4 independently verifies append-only via grep + live JSONL evidence (4× `phase_complete`, 1× `sprint_start`, 0× `phase_start`); R5 §4 supplies the assertion recipe. Triple validation including LIVE evidence from a real execution log.
- R4 §5 references `task-builder/SKILL.md` line 1119-1127 (descriptive) and 1906-1913 (checklist) for TB-Add-1..8; the builder will need this to be valid. Not cross-checked here (out of scope for completeness verification of research files) but flagged for builder.

No contradictions found between researchers.

---

## Contradictions Found

**None.** The five researchers' findings are mutually consistent and reinforcing on every overlapping data point. This is a notably clean research set.

(One apparent contradiction — R4's "Status: In Progress" header vs its "Status: Complete" footer — is a documentation hygiene issue, not a substantive contradiction.)

---

## Compiled Gaps

### Critical Gaps (block synthesis / task-file generation)

**NONE.** The builder has sufficient evidence to draft every phase of the task file.

### Important Gaps (affect quality but not blocking)

**NONE.** All four fixes have triple-corroborated code locations, test recipes, and convention guidance.

### Minor Gaps (must still be fixed before final task delivery)

**Minor Gap #1 — R4 Status field is "In Progress" (line 6) but body is complete (footer line 354 says "Status: Complete"). Body content is comprehensive and ready for builder consumption.**
- Source: 04-template-and-examples.md, line 6 vs line 354.
- Severity: Minor (hygiene only — body is complete).
- Action: Either flip the header to `Status: Complete` before consumption, or accept as-is and proceed. Does not block builder.

**Minor Gap #2 — C4's exact intent is partially ambiguous.**
- R5 §6 C4 says: "C4 is presumably about adding a NEW field … OR ensuring the event fires for a previously-uncovered path — confirm exact intent from C4 spec before writing tests."
- R3 IP-4 unambiguously identifies the gap: the per-task block at executor.py:1262-1300 has NO `write_phase_start` call (verified by analyst), and the live execution log shows 0 `phase_start` events out of 4 phases run.
- The track goal states "C4: phase_start JSONL emission" — emission of the existing event at the per-task callsite is the obvious reading, and R3's live evidence pins it down.
- Severity: Minor — the builder should still make this explicit in the task file (which call site is being added, vs whether new fields are also being added) so the implementer doesn't infer-then-diverge.
- Action: Builder should phrase the C4 item as "add `logger.write_phase_start(phase, started_at)` call at executor.py:1265 (between `started_at` assignment and `tui.update`) in the per-task branch" rather than the vaguer "add phase_start emission." This is consistent with R3 IP-4 mitigation guidance.

**Minor Gap #3 — C1 "watchdog split" semantics are documented but the exact field naming / default values are not finalized in research.**
- R5 §6 C1 references a new `startup_stall_timeout` field with `EXPECTED_DEFAULT` and `EXPECTED_IDLE_DEFAULT` as placeholders.
- R3 IP-5 describes the split conceptually ("add watchdog to per-task path") but doesn't name the new field.
- R1 §3 mentions "C1 has TWO sub-fixes per the track goal: (a) `stall_timeout` default policy; (b) watchdog split — the synthesis suggests separating 'warn-only watchdog default-on' from 'kill watchdog opt-in', which may require restructuring this branch."
- Severity: Minor — there's enough convergent evidence that the split is "startup-stall (no events received yet)" vs "idle-stall (events received but stalled)", and `MonitorState.events_received` (R5 §5) already supports this discrimination. The exact field names and default values are an implementation decision the builder can leave to the implementer with a clear directive ("define new field(s) for the startup-stall branch; choose defaults consistent with `events_received` semantics; update tests in `test_watchdog.py` accordingly").
- Action: Builder should put this open-question in the task file's Open Questions / Findings section per TB-Add-3 if final naming is required up-front, OR explicitly delegate naming to the implementer. Either path is acceptable.

**Minor Gap #4 — C6 (deferred fan-out injection) is mentioned only in passing.**
- R3 cross-cutting summary lists "C6 (deferred) fan-out" with blast radius HIGH and "Defer" as the only mitigation guidance.
- The track goal explicitly states C6 is a deferred follow-up, so this is acceptable for the current track.
- Severity: Minor (track is the 4-fix landing; C5/C6 are documented for handoff to a future task).
- Action: None for this track; just verify that the builder does NOT generate phases or items for C5/C6.

---

## Depth Assessment

**Expected depth (Standard tier):** file-level understanding of fix-scope files with key function documentation, caller graph, conventions to match, test recipe templates, MDTM template rules.

**Actual depth achieved:**
- File-level: every fix-scope file has its imports, exports (with signatures + line numbers), and fix-touchpoint code blocks excerpted verbatim (R1).
- Caller graph: production callers + test callers + blast radius enumerated per touchpoint (R3 IP-1..IP-8).
- Conventions: 8 numbered sub-sections covering dataclass, subprocess, datetime, monotonic, JSONL, debug_log, poll loop, stderr (R2 §1-§8). Each ends with an explicit "new code rule".
- Test recipes: per-fix unit + integration recipes with verbatim copy-paste-ready blocks (R5 §6).
- MDTM rules: 13 lettered sections (A-M) of template rules + TB-Add-1..8 + B2 6-element schema verbatim (R4 §1-§6).

**Missing depth elements:** None — depth materially exceeds Standard tier expectations. The research is closer to Deep tier in some places (R3's live JSONL evidence; R5's per-fix assertion-count specifications; R2's pattern-by-pattern verbatim corroboration).

---

## Recommendations

1. **Proceed with task-builder spawn.** Research is sufficient; no further research pass needed.

2. **Builder should explicitly cite R3 IP-4's pinpoint** (insert `logger.write_phase_start(phase, started_at)` between executor.py:1263 and 1265, i.e., between `started_at = datetime.now(timezone.utc)` and `tui.update(...)`) for the C4 item. R3 gives the exact insertion point; do not let the implementer re-derive it.

3. **For C1, builder should resolve Minor Gap #3 inline** by either (a) committing to specific field names (`startup_stall_timeout`, retain `stall_timeout` for idle-stall) and defaults in the task file's Goals section, OR (b) flagging it as an Open Question with explicit "implementer chooses, must update `test_watchdog.py` and add new test in `TestStartupStallWatchdog`" guidance. R5 §6 C1 provides 5 assertions ready to use once the names are decided.

4. **For C3, the canonical formula is `max_turns * 120 + 300`** (matches `ClaudeProcess` default `6300` for `max_turns=50`). R3 IP-7 notes the only outlier is dead code (`executor.py:86` in `SprintGatePolicy.build_remediation_step` which has zero production callers per IP-7). The task item for C3 is a 1-line change to that location, plus a possible centralized helper for both call sites. Builder should pick one approach (single-line edit vs introduce `compute_timeout(max_turns)` helper) and codify in the task file rather than leaving open.

5. **For C2, recommend the additive `task_output_file(phase, task)` / `task_error_file(phase, task)` approach** per R3 IP-2 mitigation — preserves the existing helper signatures (so per-phase callers and 13+ existing tests don't break) and limits the production change to `_run_task_subprocess` at executor.py:1101-1102 + line 1112. Builder must touch `models.py:469-476` (add the new helpers) — this is OUT of the fix-scope file list in the track goal (sprint/config, sprint/executor, sprint/process, sprint/logging_, sprint/monitor, pipeline/process), so builder should explicitly include `src/superclaude/cli/sprint/models.py` as an in-scope file.

6. **Builder should NOT include `make sync-dev` / `make verify-sync` items** in this task per R5 §8 — these fixes touch Python source (`src/superclaude/cli/{sprint,pipeline}/`) which is not under `{skills,agents,commands}` and therefore does not require sync.

7. **Test directory location: `tests/sprint/` and `tests/pipeline/`** — NOT `tests/cli/sprint/` (does not exist). All test recipes from R5 §6 use the correct location.

8. **Builder should fix R4's "In Progress" header** before quoting/embedding any reference to that file (Minor Gap #1).

---

## Summary

5 research files analyzed. Verdict: **PASS**. Three minor flags requiring builder attention (R4 status hygiene, C4 intent precision, C1 field-name resolution) — none block the builder from generating a sound MDTM task file. Spot-verification of three critical citations (models.py:469-476, executor.py:1262-1300, tests/sprint vs tests/cli/sprint) all CONFIRMED. Three bonus spot-checks (executor.py:86, 1106, 1328) also CONFIRMED. Research quality is unusually strong: ~300 evidenced claims, zero contradictions, triple-corroborated coverage of every fix's source site, caller graph, and test recipe.

**Recommendation:** Proceed to task-builder spawn (A.9). Builder should incorporate Recommendations 2-7 above into the task file body.

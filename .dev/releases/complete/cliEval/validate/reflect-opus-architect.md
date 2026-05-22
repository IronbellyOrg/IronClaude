---
blocking_issues_count: 1
warnings_count: 5
tasklist_ready: false
---

## Findings

- **[BLOCKING]** Coverage: FR-G1 (Real Claude Code Subprocess via PTY) has no corresponding task row in the roadmap.
  - Location: roadmap.md (entire file) vs extraction.md §"Functional Requirements" FR-G1; design-spec.md §1 Goal 1
  - Evidence: Searching the roadmap deliverable tables for `FR-G1` returns zero matches. FR-G1 is the meta-goal "Drive a real Claude Code subprocess through a PTY for each eval — no mocks, no synthetic stubs, no in-process SDK clients." While COMP-007 (PtyDriver, row 36) and COMP-013 (ClaudeProcess reuse, row 38) implement the mechanism, the goal-level requirement itself is not traced as a deliverable row. The other five goals (FR-G2..FR-G6) are all present as explicit rows (58, 22, 74, 75, 73).
  - Fix guidance: Add a P0 row in M2 or M3 with `ID: FR-G1`, title "Real Claude Code subprocess via PTY (no SDK shortcut)", dep COMP-007+COMP-013, AC asserting "integration test proves real claude binary spawned via pexpect; no in-process SDK client code path exists; ban-import lint rule rejects `anthropic` SDK imports under `cli/eval/`."

- **[WARNING]** Decomposition: FR-ISO1 (row 28) is compound — combines HOME override, CLAUDE_SESSION_ID stamp, and CLAUDE_FAKE_TIME_OFFSET into one deliverable.
  - Location: roadmap.md:M2 row 28
  - Evidence: Title reads "Add HOME override, CLAUDE_SESSION_ID stamp, optional CLAUDE_FAKE_TIME_OFFSET" — three distinct env-injection layers joined by commas. OQ-8 (time-offset semantics) is unresolved, suggesting the third item may need to split off as a deferrable subtask.
  - Fix guidance: Split into FR-ISO1a (HOME override + 4-layer preservation), FR-ISO1b (session_id stamp), FR-ISO1c (optional time-offset, gated by OQ-8 closure).

- **[WARNING]** Decomposition: NFR-REL1 (row 50) is compound — "Signal handling + timeout enforcement".
  - Location: roadmap.md:M3 row 50
  - Evidence: Title joins SIGINT/SIGTERM cancellation and per-eval timeout reaping. AC bundles four distinct behaviors (SIGINT mark, partial summary, exit 3, timeout kill + reap).
  - Fix guidance: Split into NFR-REL1a (signal cancellation + partial summary write) and NFR-REL1b (per-eval timeout enforcement + zombie reap).

- **[WARNING]** Decomposition: NFR-MAINT1 (row 23) is compound — "Fork ptytest under cli/eval/pty/ with LICENSE + PROVENANCE.md".
  - Location: roadmap.md:M2 row 23
  - Evidence: Three outputs (source vendoring, LICENSE retention, PROVENANCE.md authoring). AC10 (row 25) already separates SHA-pin + drift policy; further split would clarify the LICENSE/NOTICE work already gated by DOC-OQ4 (row 24).
  - Fix guidance: Acceptable as-is given DOC-OQ4 and AC10 partially decompose the work; or fold the PROVENANCE.md authoring into AC10 explicitly.

- **[WARNING]** Decomposition: COMP-010.5 (row 69) bundles two distinct primitives ("Expect.stderr / stdout primitives").
  - Location: roadmap.md:M4 row 69
  - Evidence: Single row covers two assertion primitives with similar but distinct semantics (stderr buffer vs stdout buffer). Test-strategy V4 lists them as separate coverage items ("each of `file/jsonl/settings_json/exit_code/stderr/stdout/duration`").
  - Fix guidance: Split into COMP-010.5a (Expect.stderr) and COMP-010.5b (Expect.stdout) for tasklist clarity, or keep merged with explicit acknowledgment that AC must exercise both streams independently.

- **[INFO]** Traceability: AC4, AC5, AC7, AC8, AC9 from extraction.md are present only implicitly via component choices or Decision Summary table; no explicit roadmap row carries those IDs.
  - Location: roadmap.md (Decision Summary table covers AC6/AC8 rationale); extraction.md "Architectural Constraints" §AC4/5/7/8/9
  - Evidence: AC4 (reuse ClaudeProcess) is satisfied by COMP-013 row 38 but the AC4 ID never appears. Same for AC5 (extend IsolationLayers, satisfied by COMP-012/COMP-006), AC7 (single-host — only in Resource section), AC8 (no async/await — in Decision Summary), AC9 (TTY-driven — implicit in Decision Summary).
  - Fix guidance: Either add lightweight P2 rows referencing each AC ID for explicit traceability, OR add an "Architectural Constraints satisfaction" subsection in M6 enumerating which deliverable satisfies each AC. Not blocking because constraints are mechanically satisfied by component choices.

## Summary

- BLOCKING: 1 (FR-G1 not traced as a deliverable)
- WARNING: 4 decomposition flags (FR-ISO1, NFR-REL1, NFR-MAINT1, COMP-010.5)
- INFO: 1 traceability note (AC4/5/7/8/9 implicit-only)

Schema, structure (acyclic 6-milestone DAG, sequential IDs 1–116, valid heading hierarchy), cross-file consistency (V1↔M1 .. V6↔M6 all mapped), parseability (clean table-row structure), and proportionality (116 task rows for ~85 distinct input entities — ratio ~0.73) all pass. The roadmap is otherwise comprehensive and well-structured; the single BLOCKING issue is a one-row addition to make FR-G1 explicit. Recommend resolving FR-G1 coverage before tasklist generation.

## Interleave Ratio

```
interleave_ratio = unique_milestones_with_deliverables / total_milestones
                 = 6 / 6
                 = 1.0
```
All six milestones (M1–M6) contain deliverable rows. Tests are NOT back-loaded: TEST-001 in M1, TEST-002/003/004/006 in M2–M3, TEST-007/008/009 in M3–M4, TEST-013/014 in M5. Within `[0.1, 1.0]` bound — PASS.

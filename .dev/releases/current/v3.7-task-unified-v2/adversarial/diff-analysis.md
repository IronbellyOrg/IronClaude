# Diff Analysis: v3.7 Release Specification Comparison

## Metadata
- Generated: 2026-04-02T12:00:00Z
- Variants compared: 2
- Variant A: "Droid" (719 lines, concise manually-structured spec)
- Variant B: "Assembled" (1608 lines, rf-assembler from 9 source docs + 3 analyses)
- Total differences found: 42
- Categories: structural (7), content (14), contradictions (5), unique (10), shared assumptions (6)

---

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Document length & density | 719 lines; concise integrated spec | 1608 lines; exhaustive assembled document | Medium |
| S-002 | Section naming | "Problem Context & Motivation" | "Problem Statement" | Low |
| S-003 | Solution architecture section | Embedded within Feature Area 1 (Section 3.1) | Separate top-level "Solution Architecture" (Section 3) with own subsections | Medium |
| S-004 | Implementation detail depth | Task tables with summary rows (Effort/Confidence only); no per-task steps | Full per-task breakdowns: [PLANNING]/[EXECUTION]/[VERIFICATION] steps, acceptance criteria, rollback commands | High |
| S-005 | Appendices | None — all content inline | 4 appendices: Adversarial Analysis Summary, UI Layout Mockups, Codebase Integration Map, Source Document Index | Medium |
| S-006 | Open Questions format | Combined section with numbered items, some marked RESOLVED inline | Separated by domain (CE-Q1..Q8, TUI-Q1..Q10, NC-Q1..Q5) with priority and source attribution | Medium |
| S-007 | Configuration section | Inline within Rollout Strategy (Section 9.2) | Dedicated top-level section (Section 12) with gate behavior matrix | Low |

---

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Checkpoint task count | "15 tasks" referenced in overview and detailed in wave tables | "15 tasks" consistent, but adds per-task acceptance criteria, rollback commands, and step-by-step instructions for each | Low |
| C-002 | SummaryWorker placement | Explicitly places SummaryWorker class in `summarizer.py` (Section 4.5) | States SummaryWorker is in `executor.py` (Section 3.2: "SummaryWorker class (in executor.py)") and PhaseSummarizer in `summarizer.py` | High |
| C-003 | LOC estimates | Checkpoint ~580, TUI v2 ~800+, Naming ~100; total ~1,480+ | Checkpoint ~580 consistent, TUI v2 unquantified beyond "7 files (2 new, 5 modified)", Naming unquantified | Medium |
| C-004 | Rollout timeline | Days 0-12 with Sprint +2 and Next release; naming on Day 0 | Days 1-18 with Sprint +2 and Next release; naming on Days 1-3 | Medium |
| C-005 | Naming task count | "~100 LOC" and "9 verified files" with "~15-20 live source files" needing updates | 12 named tasks (N1-N12) with tiered priority (Tier 1/2/3) and dependency chain | Low |
| C-006 | Open questions resolved status | 3 items explicitly marked RESOLVED: Q4 (SummaryWorker placement), Q6 (thread safety), Q13 (output_bytes/files_changed) | None marked resolved — all questions listed as open with priority and source attribution | Medium |
| C-007 | Test task coverage | Explicitly notes "T02.05" and "T03.06" test tasks were added to address test strategy gap | Lists test tasks in implementation plan and separately flags CE-Q1 "test strategy gap" as HIGH priority open question | Medium |
| C-008 | Thread safety approach | Mandates `threading.Lock` for `_summaries` dict (Section 4.5 critical invariants) | Notes "GIL provides partial protection; document concurrency model" (Risk TUI-2); less prescriptive | Medium |
| C-009 | Post-phase hook ordering | Defines explicit 3-step ordering: verify_checkpoints (blocking) -> summary_worker.submit (non-blocking) -> manifest update (blocking) | No explicit ordering defined; both domains modify phase completion flow but ordering unstated | High |
| C-010 | Token display helper | Specifies `_format_tokens()` implementation with K/M suffixes; suggests `utils.py` or `tui.py` placement | References `_format_tokens()` in F6 description but placement question deferred to TUI-Q5 | Low |
| C-011 | Checkpoint Wave 2 test tasks | Adds "T02.05" as explicit test task in wave 2 | Lists verification methods per task but CE-Q1 flags that "no dedicated test tasks" exist | Medium |
| C-012 | Implementation order | Section 6.2: Naming -> CP W1 -> TUI Core -> CP W2 -> TUI Summary -> CP W3 -> CP W4 | Section 8.1 timeline: CP W1 (Day 1) -> Naming (Day 1-3) -> CP W2 (Day 2-5) -> TUI W1 (Day 3-7) -> CP W3 (Day 5-10) -> TUI W2+W3 (Day 7-14) -> TUI W4 (Day 14-18) | Medium |
| C-013 | Risk register format | Combined risks + open questions in one section (Section 11) | Separate Risk Register (Section 9) and Open Questions (Section 13) with domain sub-grouping | Low |
| C-014 | Source attribution | Source Documents section lists 6 files with sizes | Every section includes `**Source**:` footer citing specific analysis document sections | Medium |

---

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | SummaryWorker module location | `SummaryWorker` is defined in `summarizer.py` (Section 4.5 table: "PhaseSummary, PhaseSummarizer, SummaryWorker" all in summarizer.py) | `SummaryWorker` is "(in `executor.py`)" (Section 3.2 line: "SummaryWorker class (in executor.py)"); PhaseSummarizer is in summarizer.py | High |
| X-002 | Naming consolidation timing | "Day 0" — first task, before checkpoint Wave 1 | "Day 1-3" — runs parallel with or after checkpoint Wave 1 (Day 1) | Medium |
| X-003 | Test tasks in checkpoint enforcement | T02.05 and T03.06 are explicitly listed as tasks in the wave tables (Section 3.2) | CE-Q1 asks "How will ~580 LOC be tested?" flagging absence of dedicated test tasks as HIGH priority open question — contradicts the task listing in Section 4.1 which includes per-task verification methods | Medium |
| X-004 | Thread safety prescription | Mandates `threading.Lock` — stated as "MUST be guarded" (Section 4.5 critical invariants) | Lists as a risk (TUI-2) with GIL partial protection noted; treats as open question (TUI-Q3) | Medium |
| X-005 | Checkpoint enforcement task numbering | Uses T01.01-T01.02, T02.01-T02.05, T03.01-T03.06, T04.01-T04.03 (15 tasks, including test tasks) | Uses T01.01-T01.02, T02.01-T02.04, T03.01-T03.05, T04.01-T04.03 (14 tasks, no explicit test tasks in numbering) | Medium |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | B | Appendix A: Adversarial Analysis Summary of checkpoint enforcement solutions — 6-criterion comparison matrix with winner/finding per criterion | Medium |
| U-002 | B | Appendix B: Full ASCII art UI layout mockups for Active Sprint, Sprint Complete, Sprint Halted, and Tmux 3-Pane | High |
| U-003 | B | Appendix C: Codebase Integration Map — Sprint Pipeline Flow, Checkpoint Enforcement Failure Path, full Integration Point Map table | High |
| U-004 | B | Per-task [PLANNING]/[EXECUTION]/[VERIFICATION] step breakdowns with acceptance criteria and rollback commands for all 14+ tasks | High |
| U-005 | B | Tiered naming consolidation (Tier 1: break pipeline, Tier 2: break cross-protocol, Tier 3: documentation consistency) with explicit dependency chain N1->N2->...->N11 | Medium |
| U-006 | B | Confidence Assessment Summary table with per-task analyst notes and "highest-risk task" call-out (T03.03 at 75%) | Medium |
| U-007 | A | Cross-Cutting Concerns section (Section 6) with explicit shared file modification table, post-phase hook ordering, token display helper, and Haiku subprocess conventions | High |
| U-008 | A | Explicit resolution of 3 open questions inline (Q4 SummaryWorker, Q6 thread safety, Q13 output_bytes) | Medium |
| U-009 | A | Section 6.3: Haiku Subprocess Conventions — env var stripping (`CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`), flags, stdin, timeout as consolidated cross-cutting concern | Medium |
| U-010 | A | Section 6.4: Explicit post-phase hook ordering (verify_checkpoints -> summary_worker.submit -> manifest update) with blocking/non-blocking annotations | High |

---

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|-----------|---------------|----------|
| A-001 | Both variants assume `claude --print --model claude-haiku-4-5` is available for narrative generation | Haiku model is accessible in the sprint execution environment with no authentication/API key barriers | UNSTATED | Yes [SHARED-ASSUMPTION] |
| A-002 | Both variants assume `checkpoint_gate_mode` defaults to `shadow` and will be promoted manually | Operational process for gate promotion (shadow->soft->full) exists and operators will follow the promotion schedule | UNSTATED | Yes [SHARED-ASSUMPTION] |
| A-003 | Both variants assume Phase 3's checkpoint failure was a singular incident attributable to the triple failure chain | No other undiscovered failure modes exist that could cause checkpoint misses beyond the 3 identified root causes | UNSTATED | Yes [SHARED-ASSUMPTION] |
| A-004 | Both variants agree on the 3-layer enforcement model (Prevention, Detection, Remediation) | Three layers are sufficient; no additional enforcement layer (e.g., CI/CD pipeline checkpoint validation) is needed | UNSTATED | Yes [SHARED-ASSUMPTION] |
| A-005 | Both variants agree Wave 4 is deferred to next release | Current tasklist format (`### Checkpoint:`) will remain stable until next release; no interim changes to checkpoint heading format | STATED | No |
| A-006 | Both variants assume `stream-json` output format is stable and documented | Claude CLI `stream-json` schema will not change in ways that break TUI v2 parsing; no schema versioning mentioned | UNSTATED | Yes [SHARED-ASSUMPTION] |

---

## Summary

- Total structural differences: 7
- Total content differences: 14
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 6 (UNSTATED: 5, STATED: 1)
- Promoted [SHARED-ASSUMPTION] diff points: 5 (A-001, A-002, A-003, A-004, A-006)
- **Highest-severity items**: X-001 (SummaryWorker location contradiction), C-002 (SummaryWorker placement), C-009 (post-phase hook ordering), U-004/U-007/U-010 (unique high-value contributions)
- Total diff points for convergence: S(7) + C(14) + X(5) + A(5 promoted) = **31 debatable points**

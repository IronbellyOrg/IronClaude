# Technical Validation Report — UNIFIED-RELEASE-SPEC.md

**Date**: 2026-04-02  
**Scope**: Internal consistency, cross-reference accuracy, dependency validity, architectural coherence  
**Verdict**: **MOSTLY COHERENT — 5 issues requiring fixes, 8 advisories**

---

## A. Internal Consistency

### ✅ Passed

| Check | Result |
|-------|--------|
| Task IDs (T01.01–T04.03) are unique and sequential across waves | Consistent |
| File paths agree between Section 3 (Waves), Section 6 (Cross-Cutting), and Section 7 (File Inventory) | All match `src/superclaude/cli/sprint/` prefix |
| Risk levels agree between Section 1 summary table and detailed wave descriptions | Consistent (Low–Medium, Medium, Low) |
| Implementation order in §6.2 respects stated dependencies: Naming → W1 → TUI Core → W2 → TUI Summary → W3 → W4(deferred) | Logically sound |
| New model fields in §8 are consistent with feature descriptions in §3 and §4 | Consistent |

### ⚠️ Issues Found

| # | Issue | Severity | Location | Detail |
|---|-------|----------|----------|--------|
| A1 | **LOC estimate mismatch** | Low | §1 vs §7 | §1 claims Checkpoint ~580, TUI ~800+, Naming ~100 (total ~1,480). §7 says "~1,480+ LOC across all features." The sum of §3 wave LOCs is 60+120+200+200=580 ✅ for checkpoints. TUI v2 LOC is never broken down per feature — "800+" is an opaque estimate. **Recommendation**: Add per-feature LOC breakdown for TUI v2 (F1–F10) in §4.3 for traceability. |
| A2 | **PhaseResult `turns`, `tokens_in`, `tokens_out` described as "3 new fields" in §8.2 but NOT currently missing** | Medium | §8.2 vs codebase | The current `PhaseResult` already has `output_bytes` and `files_changed` but does NOT have `turns`, `tokens_in`, `tokens_out`. The spec is correct that these are new. However, §8.2 lists them as the ONLY 3 new fields — it doesn't mention that `output_bytes` and `files_changed` already exist. This is accurate but could be clearer. **No fix needed**, just advisory. |
| A3 | **Open Question #13 self-contradicts** | Low | §11.1 #13 | States "`output_bytes` 'already exists' but `files_changed` isn't listed as a new field." In fact, BOTH `output_bytes` AND `files_changed` already exist on `PhaseResult` (lines 442, 445 of models.py). The open question is based on a false premise. **Recommendation**: Resolve OQ-13 — both fields pre-exist, no new additions needed for either. |

---

## B. Cross-Reference Accuracy

### ✅ All 8 referenced files exist

| File | Exists | Lines |
|------|--------|-------|
| `process.py` | ✅ | 373 |
| `executor.py` | ✅ | 1846 |
| `models.py` | ✅ | 737 |
| `monitor.py` | ✅ | 317 |
| `tui.py` | ✅ | 285 |
| `tmux.py` | ✅ | 246 |
| `logging_.py` | ✅ | 198 |
| `commands.py` | ✅ | 331 |

### Line Number Verification

| Claim | Actual | Verdict |
|-------|--------|---------|
| `build_prompt()` at ~lines 169–203 in `process.py` | `build_prompt()` defined at **line 123**; the `/sc:task-unified` prompt return starts at **line 170** and ends at **line 203** | ⚠️ **Partially correct**: The function definition is at L123, not L169. The spec's range (169–203) refers to the prompt *return statement* only, not the full function. **Recommendation**: Clarify as "return statement at lines 170–203" or "function at lines 123–203". |
| `_check_checkpoint_pass()` at 1592–1603 in `executor.py` | Function at **line 1592**, body ends at **line 1603** | ✅ **Exact match** |
| `sc:task-unified` at L124, L170 in `process.py` | L124: docstring `"""Build the /sc:task-unified prompt"""`, L170: `f"/sc:task-unified Execute..."` | ✅ **Exact match** |
| `sc:task-unified` at L26, L47, L69, L92, L116 in `prompts.py` | L26, L47, L69, L92, L116 all confirmed | ✅ **Exact match** |
| Legacy `.claude/commands/sc/task.md` with `deprecated: true` | File exists, frontmatter has `deprecated: true` and `deprecated_by: "task-unified"` | ✅ **Confirmed** |
| `task-unified.md` frontmatter says `name: task` | Frontmatter: `name: task` | ✅ **Confirmed** |
| `sc-task-unified-protocol/SKILL.md` exists | ✅ Exists at `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | ✅ **Confirmed** |
| 7 markdown files with `sc:task-unified` references (§5.2) | All 7 confirmed via grep | ✅ **Confirmed** |

### Enum/Model Verification

| Claim | Actual | Verdict |
|-------|--------|---------|
| `PhaseStatus` enum exists in `models.py` | ✅ Defined at line 212 | ✅ |
| Current `PhaseStatus` members | PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED (12 members) | ✅ **Confirmed** — `PASS_MISSING_CHECKPOINT` does NOT yet exist (correctly identified as a new addition) |
| `MonitorState` exists in `models.py` | ✅ Defined at line ~502 | ✅ |
| Current `MonitorState` fields | output_bytes, output_bytes_prev, last_growth_time, last_event_time, phase_started_at, events_received, last_task_id, last_tool_used, files_changed, lines_total, growth_rate_bps, stall_seconds (12 fields) | ✅ **None of the 8 proposed new fields exist yet** |
| `SprintConfig` already has `checkpoint_gate_mode` / `total_tasks` | ✅ Neither exists yet — correctly identified as new additions | ✅ |

---

## C. Dependency Chain Validity

### ✅ Passed

| Chain | Verdict | Detail |
|-------|---------|--------|
| Wave 2 depends on Wave 1 | ✅ Valid | W2 T02.04 "replaces Wave 1's warning with configurable gate" — W1's T01.02 creates the call site that W2 replaces. Linear dependency. |
| Wave 3 depends on Wave 2 | ✅ Valid | W3 extends `checkpoints.py` created in W2. `build_manifest()` and `recover_missing_checkpoints()` layer onto W2's path extraction and verification functions. |
| Checkpoint W4 deferred | ✅ Valid | Correctly deferred as breaking change; W1–W3 provide interim coverage. |

### ⚠️ Issue Found

| # | Issue | Severity | Detail |
|---|-------|----------|--------|
| C1 | **F8 → F9 → F10 dependency chain is VALID but incompletely stated** | Low | The spec's §4.3 says F8 creates `SummaryWorker` + `summarizer.py`, F9 adds tmux pane for summaries (depends on F8's output files), F10 aggregates all phase summaries (depends on F8's per-phase summaries). The dependency is: **F8 → F9 (parallel-safe), F8 → F10 (sequential)**. The spec in §6.2 groups F8–F10 together as "TUI v2 Summary" but doesn't explicitly state F9 and F10 both depend on F8. **Recommendation**: Add explicit dependency note in §4.3 or §6.2. |
| C2 | **SummaryWorker in executor.py needs summarizer.py — direction is correct** | ✅ | `executor.py` would import from `summarizer.py`, creating a one-way dependency. `summarizer.py` is a self-contained module. No circular dependency. |

---

## D. Architectural Coherence

### ✅ Three-Layer Enforcement Model

The checkpoint enforcement layers genuinely cover all 3 root causes:

| Root Cause | Layer | Coverage |
|-----------|-------|----------|
| RC1: No prompt instructions | Layer 1 (Wave 1: prompt fix) | ✅ Direct fix — adds `## Checkpoints` section |
| RC2: Structural heading mismatch | Layer 1 (Wave 4: tasklist normalization) | ✅ Structural elimination — deferred but accounted for |
| RC3: No post-phase enforcement | Layer 2 (Wave 2: gate) + Layer 3 (Wave 3: manifest) | ✅ Detection + remediation |

### ⚠️ Issues Found

| # | Issue | Severity | Detail |
|---|-------|----------|--------|
| D1 | **`executor.py` shared modification conflict risk is REAL but manageable** | Medium | Both checkpoint (W1–W3) and TUI v2 (F8/F10) add post-phase processing to `executor.py`. The spec acknowledges this in §6.1 but provides no concrete integration plan (e.g., method ordering, hook pattern). Current `executor.py` is already 1,846 lines. **Recommendation**: Define a `_post_phase_hooks()` pattern or explicit call order in executor.py to prevent merge conflicts and clarify execution sequence (checkpoint verification → summary submission → manifest update). |
| D2 | **SummaryWorker threading model: thread safety concern is REAL** | Medium | §11.1 OQ-6 correctly flags that `_summaries` dict would be mutated from multiple threads without locking. The existing `OutputMonitor` in `monitor.py` also lacks explicit locking (state mutations happen in a single daemon thread read by the main thread). However, `SummaryWorker` uses a thread *pool* (multiple workers), creating genuine concurrent write risk to shared state. **Recommendation**: Mandate `threading.Lock` for `SummaryWorker._summaries` in the spec. The existing `OutputMonitor` pattern (single writer thread) is NOT a safe precedent for multi-writer pools. |
| D3 | **No architectural conflicts between checkpoint and TUI features sharing executor.py** | ✅ | Checkpoint verification (gate check) and TUI summary (SummaryWorker.submit) operate on different data at different points in the phase lifecycle. Gate check is blocking (before next phase); summary is non-blocking (background). No data races between these two. |

---

## E. Gaps & Contradictions

### Contradictions Found

| # | Issue | Severity | Detail |
|---|-------|----------|--------|
| E1 | **§5.2 naming references count: "9 live source files" vs actual file count** | Low | §5.1 says "9 live source files reference `sc:task-unified` (2 Python + 7 Markdown)". Grep confirms: `process.py` (2 occurrences), `prompts.py` (5 occurrences) = 2 Python files ✅. 7 Markdown files listed in §5.2 all confirmed ✅. The "9 live source files" count is **correct**. No contradiction. |
| E2 | **§11.1 OQ-4: "SummaryWorker module placement" confusion** | Low | OQ-4 says "Spec shows it in both `summarizer.py` and `executor.py`." The spec actually says SummaryWorker is *defined* in `summarizer.py` (§4.5) and *used/wired* from `executor.py` (§7). This is standard import-and-use, not a placement conflict. **Recommendation**: Resolve OQ-4 as non-issue — SummaryWorker lives in `summarizer.py`, imported by `executor.py`. |

### Unstated Assumptions / Gaps

| # | Gap | Severity | Detail |
|---|-----|----------|--------|
| E3 | **No test-writing tasks in checkpoint waves** | Medium | §10.4 explicitly identifies this gap: "checkpoint enforcement tasklist references unit/integration tests as verification methods but does not include dedicated test-writing tasks." **Recommendation**: Add explicit test tasks (e.g., T02.05, T03.06) to each wave, or add a Wave 2.5 for test coverage. |
| E4 | **`PASS_MISSING_CHECKPOINT` not added to `is_terminal` or `is_success` property** | Medium | §3.2 Wave 2 says `PASS_MISSING_CHECKPOINT` has `is_failure = False`, but doesn't specify whether it's `is_terminal` or `is_success`. Since it represents a completed phase with missing checkpoints, it should be `is_terminal = True` and `is_success = True` (matching existing `PASS_NO_SIGNAL` / `PASS_NO_REPORT` pattern). **Recommendation**: Explicitly state `is_terminal = True, is_success = True` in §8.5 and add it to the `is_terminal` and `is_success` tuples in the PhaseStatus implementation plan. |
| E5 | **`checkpoint_gate_mode` config mechanism unresolved** | Medium | §9.2 notes this is unspecified. The existing `SprintConfig` uses `wiring_gate_mode: Literal[...]` with default values. A consistent approach would be a CLI flag (`--checkpoint-gate`) mapped to `SprintConfig.checkpoint_gate_mode`. **Recommendation**: Specify CLI flag in §9.2, following the existing `wiring_gate_mode` pattern. |
| E6 | **`build_prompt()` line range should be 123–203, not 169–203** | Low | As noted in §B, the spec references lines 169–203 which is only the return statement, not the full function. The full function spans lines 123–203. Since the spec discusses the entire function behavior (Sprint Context header, Scope Boundary), it should reference the full range. |
| E7 | **Legacy task.md frontmatter says `name: task-legacy`, not `name: task`** | Low | §5.1 notes naming confusion between layers. The legacy `.claude/commands/sc/task.md` actually has `name: task-legacy` in its frontmatter (not `name: task` as might be assumed). The spec's §5.1 table correctly says the file is `.claude/commands/sc/task.md` but doesn't note the `name: task-legacy` frontmatter value. This is minor but confirms the naming confusion is even more layered than described. |
| E8 | **No mention of updating `config.py`** | Low | `src/superclaude/cli/sprint/config.py` exists (discovered in file listing) but is not mentioned anywhere in the spec. If `SprintConfig` is constructed from CLI args parsed in `config.py`, then the new `checkpoint_gate_mode` and `total_tasks` fields need wiring there too. **Recommendation**: Verify whether `config.py` needs updates for new SprintConfig fields and add to §7 if so. |

---

## Summary of Recommendations

### Must Fix (before implementation)

| # | Recommendation | Refs |
|---|----------------|------|
| 1 | Resolve OQ-13 — both `output_bytes` and `files_changed` already exist on `PhaseResult` | A3 |
| 2 | Add `PASS_MISSING_CHECKPOINT` to `is_terminal` and `is_success` property lists in spec | E4 |
| 3 | Mandate `threading.Lock` for `SummaryWorker` shared state (not optional open question) | D2 |
| 4 | Add explicit test tasks to checkpoint waves | E3 |
| 5 | Specify `checkpoint_gate_mode` CLI flag mechanism | E5 |

### Should Fix (improve clarity)

| # | Recommendation | Refs |
|---|----------------|------|
| 6 | Clarify `build_prompt()` line range as 123–203 | E6 |
| 7 | Add per-feature LOC breakdown for TUI v2 | A1 |
| 8 | Resolve OQ-4 as non-issue (SummaryWorker lives in summarizer.py) | E2 |
| 9 | Define `_post_phase_hooks()` call ordering in executor.py | D1 |
| 10 | Check whether `config.py` needs updates for new SprintConfig fields | E8 |
| 11 | Add explicit F8→F9, F8→F10 dependency annotations | C1 |
| 12 | Note legacy task.md has `name: task-legacy` frontmatter | E7 |

---

## Validation Methodology

1. Read UNIFIED-RELEASE-SPEC.md (731 lines) in full
2. Verified all 8 referenced source files exist via Glob
3. Checked line counts of all 8 files via `wc -l`
4. Verified `build_prompt()` location (L123), `/sc:task-unified` references (L124, L170) in `process.py`
5. Verified `_check_checkpoint_pass()` location (L1592–L1603) in `executor.py`
6. Verified `PhaseStatus` enum (L212, 12 members) — no `PASS_MISSING_CHECKPOINT` yet
7. Verified `MonitorState` fields (L502, 12 existing fields) — none of 8 proposed fields exist yet
8. Verified `PhaseResult` fields (L430) — `output_bytes` and `files_changed` already exist; `turns`, `tokens_in`, `tokens_out` do not
9. Verified `SprintResult` (L460) — no `total_turns` etc. properties exist yet
10. Verified `SprintConfig` (L289) — no `checkpoint_gate_mode` or `total_tasks` fields yet
11. Confirmed `sc:task-unified` references in `prompts.py` at exact lines (L26, L47, L69, L92, L116)
12. Confirmed all 7 markdown files with `sc:task-unified` references exist
13. Confirmed legacy `.claude/commands/sc/task.md` exists with `deprecated: true`
14. Confirmed `task-unified.md` frontmatter has `name: task`
15. Confirmed `sc-task-unified-protocol/SKILL.md` exists
16. Verified no `summarizer.py`, `checkpoints.py`, or `retrospective.py` exist yet (all new)
17. Checked threading patterns in `monitor.py` — single daemon thread, no locks
18. Verified `config.py` exists but is not mentioned in spec

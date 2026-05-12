# Path A Task Partition Document

## Metadata

| Field | Value |
|---|---|
| **Date** | 2026-04-04 |
| **Source** | debate-split-vs-resplit.md Option C (Hybrid: Complete Then Partition) |
| **Governing boundary** | boundary-rationale.md: R1 = pipeline infrastructure, R2 = presentation layer |
| **One-directional rule** | R1 -> R2 (never reverse) |

---

## 1. New Task Partition (11 tasks from Section 1.3)

| Task ID | Description | Assigned To | Boundary Justification | Cross-Release Dependencies |
|---------|-------------|-------------|----------------------|---------------------------|
| **PA-01** | Extract and inject per-task markdown block via `_extract_task_block()` | **R1** | Pipeline behavior: changes the prompt sent to Claude subprocess. This is a data contract change (what Path A sends to workers). Modifies `executor.py:1064-1068`. | None. Independent foundation task. |
| **PA-02** | Add scope boundary to per-task prompt | **R1** | Pipeline behavior: modifies subprocess prompt content. Depends on PA-01. Same domain: what the executor sends to workers. | Depends on PA-01 (R1 internal). |
| **PA-03** | Add sprint context header (shared `build_sprint_context_header()`) | **R1** | Pipeline behavior: creates shared builder used by both Path A and Path B prompts. Modifies `executor.py` + `process.py`. Establishes data contract for subprocess input. | Depends on PA-01 (R1 internal). R2 benefits from richer subprocess output (indirect). |
| **PA-04** | Fix `turns_consumed` to call `count_turns_from_output()` | **R1** | Data integrity bug fix: `executor.py:1091` returns hardcoded 0. This is infrastructure plumbing — affects TurnLedger budget math, not presentation. | None. Unblocks PA-06. R2 consumes correct turns data for F2/F6 display. |
| **PA-05** | Wire `TaskResult.output_path` | **R1** | Data integrity bug fix: `executor.py:1017-1025` never sets output_path. Activates anti-instinct gate evaluation. Infrastructure/enforcement, not presentation. | None. Unblocks PA-06. R2's MonitorState adapter reads correct output_path. |
| **PA-06** | Change `gate_rollout_mode` default from `"off"` to `"shadow"` | **R1** | Enforcement behavior: changes gate default at `models.py:329`. This is pipeline enforcement policy, not presentation. | Depends on PA-04 + PA-05 (both R1). R2 benefits from active gate metrics. |
| **PA-07** | Wire `build_task_context()` behind config flag | **Defer to v3.8** | Medium risk (75% confidence), optional, behind config flag (default off). Neither R1 pipeline necessity nor R2 presentation. Best evaluated after shadow-mode gate data is collected from R1 in production. | Depends on PA-01, PA-04, PA-05. Would be R1 if included. |
| **PA-08** | Post-task deliverable existence check (observability only) | **Defer to v3.8** | Observability addition, not core pipeline or presentation. ~40 LOC for optional logging. Low urgency — best prioritized after core Path A enrichment proves stable. | Depends on PA-01. Would be R1 if included. |
| **NEW-DM-04** | Implement `extract_token_usage()` in `monitor.py` | **R1** | Data model foundation: creates the extraction function that produces token data. This is a data contract — the function exists in `monitor.py` as infrastructure, consumed by TaskResult wiring. | None. Unblocks NEW-DM-05. |
| **NEW-DM-05** | Add `tokens_in`/`tokens_out` to `TaskResult` and wire extraction | **R1** | Data model foundation: adds fields to `TaskResult` dataclass at `models.py`. This establishes the data contract that R2's aggregation (DM-06) and TUI (F2/F6) consume. | Depends on NEW-DM-04 (R1 internal). R2 consumes these fields. |
| **NEW-DM-06** | Path A aggregation logic: `TaskResult` list -> `PhaseResult` fields | **R2** | Presentation-layer wiring: aggregates per-task data for TUI display. This is the bridge between R1's data contracts and R2's rendering. The aggregation feeds `PhaseResult.turns/tokens_in/tokens_out` which the TUI consumes. | Depends on PA-04, PA-05, NEW-DM-05 (all R1). Must be listed as R2 prerequisite. |

---

## 2. Modified Task Partition (15 tasks from Section 1.2)

| Task ID | Description | Spec Modified | Boundary Justification | Cross-Release Dependencies |
|---------|-------------|--------------|----------------------|---------------------------|
| **T02.04** | Reframe as PRIMARY defense for Path A | **R1** | Checkpoint enforcement reframing. The gate at `executor.py` post-phase hook is infrastructure behavior. R1 owns all checkpoint gates. | None. R2 benefits (gate column display). |
| **T02.05** | Extend unit tests for Path A flow | **R1** | Test extension for checkpoint gate under Path A's multi-subprocess model. Testing infrastructure, not presentation. | None. |
| **T04.01** | Add Path A impact note (checkpoint becomes regular task) | **R1** | Checkpoint normalization documentation. Path A architectural implication of task normalization is pipeline behavior. | None. |
| **F1** | Activity stream: synthetic entries for Path A | **R2** | TUI rendering adaptation. How activity data is DISPLAYED. The synthetic entry creation is presentation logic. | Depends on PA-04 (turns data), accumulator (R1 data contracts). |
| **F2** | Enhanced phase table: wire from accumulated TaskResult | **R2** | TUI rendering. How turns/output are DISPLAYED in the phase table. | Depends on PA-04 (turns), NEW-DM-05 (tokens). R1 provides the data. |
| **F3** | Task-level progress bar: set exact counts in Path A hooks | **R2** | TUI rendering. How task progress is DISPLAYED. 2-line change in TUI update hooks. | Depends on accumulator being populated (R1 provides task counts via data contracts). |
| **F4** | Conditional error panel: task-level errors from TaskResult | **R2** | TUI rendering. How errors are DISPLAYED. | Depends on TaskResult having correct status/exit_code (R1 data contracts). |
| **F6** | Enhanced terminal panels: aggregate from TaskResult | **R2** | TUI rendering. How phase-level aggregates are DISPLAYED in terminal panels. | Depends on PA-04, NEW-DM-05 (R1 data), NEW-DM-06 (R2 aggregation). |
| **F8** | PhaseSummarizer accepts `list[TaskResult]` OR NDJSON | **R2** | TUI/summary presentation. Dual-input is about how the summarizer CONSUMES data for presentation. | Depends on TaskResult being correctly populated (R1: PA-04, PA-05). |
| **7.1** | 8 new MonitorState fields — Path A population | **R2** | MonitorState field population is presentation-layer data preparation. The fields exist for TUI rendering. | Depends on R1 data contracts (turns, tokens, output_path). |
| **7.2** | PhaseResult.turns/tokens — Path A aggregation | **R2** | Phase-level aggregation for TUI display. Same domain as NEW-DM-06. | Depends on PA-04, NEW-DM-05 (R1). |
| **Sec 5** | Add Path A as 4th domain in dependency analysis | **Both** | R1 gets Sections 5.6 (Path A <-> Checkpoint) and 5.7 (Path A <-> TurnLedger). R2 gets updated Section 5.1 (Path A <-> TUI data flow). | Cross-release: R1 defines data contracts, R2 defines consumption. |
| **Sec 6.2** | Insert Path A enrichment in implementation order | **R1** | Implementation ordering is pipeline scheduling, governed by R1. R2's TUI wave ordering is internal to R2. | R2 must reference R1's updated ordering. |
| **Sec 6.4** | Post-phase hook in BOTH Path A and Path B blocks | **Both** | R1 gets the `_verify_checkpoints()` hook in Path A block (lines 1222-1233). R2 gets the `summary_worker.submit()` hook in the same block. Both need the insertion point. | R1 establishes hook site; R2 adds to it. Integration point #1 from boundary-rationale.md. |
| **Sec 14** | Resolve/reframe open questions | **Both** | R1 resolves CE-Q3, CE-Q4, CE-Q6 and reframes CE-Q2. R2 resolves TUI-Q8 and reframes TUI-Q1, TUI-Q2. PA-Q1 goes to v3.8 (PA-07 deferred). | Independent resolution per domain. |

### Boundary Tensions

> **Sec 5 (Cross-domain dependencies)**: Requires notes in BOTH specs. R1 adds Path A <-> Checkpoint and Path A <-> TurnLedger dependency documentation. R2 adds Path A <-> TUI data flow. This is a documentation split, not a code split — low tension.

> **Sec 6.4 (Post-phase hook ordering)**: Both R1 and R2 modify the same hook insertion site in `executor.py:1222-1233`. R1 adds `_verify_checkpoints()`, R2 adds `summary_worker.submit()`. The ORDERING matters (checkpoint before summary). **Resolution**: R1 defines the hook site and establishes insertion order contract. R2 appends to it. This is already documented in boundary-rationale.md integration point #1.

---

## 3. Updated R1 Dependency List (what R2 depends on from R1)

### Original 4 Cross-Release Integration Points (from boundary-rationale.md)

1. `executor.py` post-phase flow ordering (`_verify_checkpoints` -> `summary_worker.submit` -> manifest update)
2. `models.py` `PhaseStatus.PASS_MISSING_CHECKPOINT` used by TUI style/icon dicts
3. `models.py` dataclasses coexistence (`CheckpointEntry`/`checkpoint_gate_mode` vs R2 `MonitorState`/`PhaseResult`/`SprintResult`)
4. `process.py` modified in R1; R2 does not modify `process.py`

### New Integration Points (from Path A partition)

5. **`TaskResult.output_path` (PA-05)** — R2's F8 PhaseSummarizer reads `output_path` to locate task output for summary extraction. R2's MonitorState adapter uses `output_bytes` from TaskResult which depends on `output_path` being valid.

6. **`TaskResult.turns_consumed` (PA-04)** — R2's F2 (phase table turns column) and F6 (terminal panel turns display) depend on accurate `turns_consumed` values from R1's PA-04 fix.

7. **`TaskResult.tokens_in/tokens_out` (NEW-DM-05)** — R2's F2 and F6 display token usage. R2's NEW-DM-06 aggregates these into `PhaseResult`. Without R1's DM-04/DM-05, these fields are always 0.

8. **`_extract_task_block()` (PA-01)** — R2's F1 activity stream and F4 error panel benefit from enriched subprocess output (more NDJSON events from richer prompts). Not a hard dependency but enriched prompts produce richer monitoring data. Note: F5 (LLM context lines) is deprioritized for Path A per MERGED Section 1.4, so prompt enrichment does not create an F5 dependency.

9. **`gate_rollout_mode="shadow"` (PA-06)** — R2's TUI gate column display is more meaningful when the gate actually evaluates. Without PA-06, gate column shows "off" for all tasks.

10. **Append-mode output file** (from monitor adaptation debates) — If R1 includes the append-mode fix (`process.py:114` "w" -> "a"), R2's F8 summary extraction sees all tasks' output instead of only the last task.

### Updated R1 Provides → R2 Consumes Contract

| R1 Provides | R2 Consumes | Integration Type |
|---|---|---|
| `PhaseStatus.PASS_MISSING_CHECKPOINT` | TUI STATUS_STYLES, STATUS_ICONS | Enum value |
| `_verify_checkpoints()` hook site | `summary_worker.submit()` insertion | Code location |
| `checkpoint_gate_mode` field | (not directly consumed) | Coexistence |
| `process.py` naming changes | R2 doesn't modify process.py | File ownership |
| `TaskResult.output_path` (PA-05) | F8 summarizer, MonitorState adapter | Data field |
| `TaskResult.turns_consumed` (PA-04) | F2, F6, PhaseResult.turns, NEW-DM-06 | Data field |
| `TaskResult.tokens_in/out` (DM-05) | F2, F6, PhaseResult.tokens, NEW-DM-06 | Data field |
| `_extract_task_block()` (PA-01) | Richer NDJSON for F1/F4 | Indirect |
| `gate_rollout_mode="shadow"` (PA-06) | Gate column has real data | Configuration |
| Append-mode output (process.py) | F8 summary sees all tasks | File content |

---

## 4. Updated R2 Prerequisites List

### Hard Prerequisites (R2 CANNOT start without these)

1. **R1 naming consolidation complete** (N1-N12) — Clean references in all R2-touched files
2. **R1 `PhaseStatus.PASS_MISSING_CHECKPOINT`** — R2 needs the enum value for display
3. **R1 post-phase hook site** — R2 needs the insertion point for summary_worker
4. **PA-04 (turns_consumed fix)** — R2's F2/F6 display nonsense data without real turns
5. **PA-05 (output_path wiring)** — R2's F8 summarizer needs valid output paths
6. **NEW-DM-04 + NEW-DM-05 (token extraction)** — R2's token display needs the data

### Soft Prerequisites (R2 works without but is degraded)

7. PA-01/02/03 (prompt enrichment) — R2's monitoring data is richer with enriched prompts
8. PA-06 (shadow gate default) — R2's gate column is more useful with active evaluation
9. Append-mode fix — R2's F8 summary is more complete with all tasks' output

---

## 5. Summary Counts

| Category | R1 | R2 | Deferred (v3.8) | Both |
|---|---|---|---|---|
| New tasks (11) | 8 | 1 | 2 | 0 |
| New tasks assigned to a spec | PA-01/02/03/04/05/06, DM-04/05 | DM-06 | PA-07, PA-08 | — |
| Modified tasks (15) | 4 | 8 | 0 | 3 |
| Total new LOC added to R1 | ~95 added, ~15 modified | — | — | — |
| Total new LOC added to R2 | — | ~10 | — | — |
| Deferred LOC | — | — | ~60 | — |
| New cross-release integration points | 6 (points 5-10) | — | — | — |
| Boundary tensions | 0 hard tensions | — | — | 2 documentation-only (Sec 5, Sec 6.4) |

---

*End of partition document.*

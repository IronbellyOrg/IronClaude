# Diff Analysis: PRD-pipeline Fix-Design Comparison

## Metadata

- Generated: 2026-06-06
- Variants compared: 3
- Variant 1: `solution-1-executor-recovery.md` — Executor-side robust recovery (harden `_resolve_step_content`)
- Variant 2: `solution-2-prompt-path-pinning.md` — Prompt-side path pinning (`_artifact_path_for_step`)
- Variant 3: `solution-3-stdout-contract.md` — Stdout/result-contract capture + cwd isolation
- Authoritative problem statement: `REPORT.md` (confidence 0.95, root-caused in source)
- Total differences found: 22 (structural 4, content 6, contradictions 3, unique 6, shared assumptions 3)

The three variants are competing fixes for the **same** confirmed defect: every document-producing step of `superclaude prd run` fails its line-count gate because `_resolve_step_content` (executor.py:266-365) rglobs the exact canonical filename under `task_dir`/`task_dir.parent`, misses the agent's real document (wrong name + wrong location), and falls back to ~24 lines of NDJSON commentary. A second, compounding defect: agents write outputs into the writable `WHERE` dir (`.dev/specs/`), which later steps re-ingest as source (contamination loop).

---

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section inventory | 7 sections (Summary, Design, Why, Risks, Backward-compat, Test plan, Effort) | 10 sections (+Status, +comparison table, +Open Questions) | 10 sections (+Status, +comparison table, +Open Questions) | Low |
| S-002 | Design decomposition | 5 numbered code changes + 4 test-file change blocks | 5 design subsections (helper + 4 prompt edits) | 4 design halves (capture / contract / cwd / gates) | Medium |
| S-003 | Self-positioning vs siblings | None (stands alone) | Comparison table ranking all 3 | Comparison table ranking all 3 | Low |
| S-004 | Test-plan granularity | ~7 named tests across 4 files | 12 named tests across 3 files | 15 named tests across 4 files | Low |

---

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|-------|--------------------|--------------------|--------------------|----------|
| C-001 | Where the fix lives | Executor recovery (`_resolve_step_content`) — consumer side | Prompt builders (`prompts.py`) — producer side | Capture path (`_extract_text_from_stream_json`) + prompts + `process.py` cwd | High |
| C-002 | Capture mechanism | Find the file on disk via flexible glob + broader roots | Make the agent write to a known disk path | Make the document flow through the CLI `result` event (no disk dependency) | High |
| C-003 | Timing of fix | After-the-fact (recover what the agent wrote) | At source (remove path ambiguity) | At channel (reliable transport) | Medium |
| C-004 | Contamination (`.dev/specs`) handling | **Not fixed** — explicitly recovers, does not prevent | Fixed by writing to `task_dir` instead of `WHERE` dir (instruction-based) | Fixed by `cwd=task_dir` + `CLAUDE_WORK_DIR` (structural) | High |
| C-005 | Blast radius | 1 function | Prompt builders + 1 helper | All 15 steps' capture path (incl. parse-request JSON, 800-line assembly PRD) | High |
| C-006 | Effort estimate | ~4-6h | ~3h | ~27h | Medium |

---

## Contradictions

| # | Point of Conflict | Position | Counter-position | Impact |
|---|-------------------|----------|------------------|--------|
| X-001 | **What Solution 3 actually is** | V2's comparison table labels Solution 3 "Subprocess Sandbox / chroot" and rates it "Cross-platform: No (chroot is Unix-only)" | V3 is in fact stdout/result-contract capture + cwd isolation — *not* chroot. REPORT.md confirms V3 = "Stdout/result-contract capture (+ cwd isolation)". V2's characterization is factually wrong. | Medium — undermines V2's comparative claims; the "not cross-platform" ding against V3 is unfounded |
| X-002 | **What Solution 2 actually is** | V3's intro and comparison table label Solution 2 "Tool-call interception: intercept the agent's Write tool call inside the subprocess" | V2 is in fact prompt-side path pinning — no tool interception. REPORT.md confirms V2 = "Prompt-side path pinning". V3's characterization is factually wrong. | Medium — undermines V3's comparative claims about V2 |
| X-003 | Reliability of the agent following instructions | V2: pinning the path removes ambiguity, so the agent will write to `task_dir` (root-cause fix). V1/V3 both flag this as the weakest assumption | V1/V3: agents routinely ignore path instructions ("agents often ignore path instructions"); a fix that depends on compliance is not a root-cause fix | High — this is the central design disagreement; determines whether a backstop/structural layer is mandatory |

---

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Deterministic tiebreak `_pick_best_candidate` (preferred_root → content length → path specificity → mtime) for multi-match disambiguation | High — no other variant addresses what happens when multiple candidate files match |
| U-002 | V1 | Path-traversal guard for `WHERE` entries (`resolve()` + `relative_to(repo_root)`) | Medium — security hardening unique to V1 |
| U-003 | V2 | Single-source-of-truth concern: `_artifact_path_for_step` must mirror `_STEP_ARTIFACT_FILES`, enforced by a sync unit test | Medium — prevents prompt/executor drift, a maintainability invariant |
| U-004 | V3 | **Working-directory isolation** (`cwd=task_dir` + `CLAUDE_WORK_DIR`) — the only *structural* (non-instruction) prevention of `.dev/specs` contamination | High — addresses X-003 at the OS boundary, independent of agent compliance |
| U-005 | V3 | Truncation-detection semantic check (`[TRUNCATED`, trailing `...`) | Medium — guards a failure mode the other two cannot introduce but is real for large docs |
| U-006 | V3 | Feature flag (`capture_mode = "result" \| "legacy"`) for gradual rollout/rollback of the high-blast-radius change | Medium — risk control proportional to V3's blast radius |

---

## Shared Assumptions

Agreement points across all three variants, with implicit preconditions enumerated and classified.

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|------------|------------------|----------------|----------|
| A-001 | **Recovering/capturing the agent's real document is *sufficient* to green the gate.** All three change only *capture/location*, never document *content*. But the `research-notes` STRICT gate also checks frontmatter `[Date, Scenario, Tier]` + semantic sections (gates.py:329-345), not only `min_lines=100`. None of the three demonstrates the agent's real doc contains that frontmatter. | C-002, C-004 (all converge: "the real doc is good, we just need to find/capture it") | UNSTATED | **Yes → [SHARED-ASSUMPTION]** |
| A-002 | The agent actually produces a document ≥ the gate's `min_lines`. | All three | STATED | No (REPORT cites a real 197-line scope-discovery doc vs 50/100 thresholds — evidence present) |
| A-003 | `task_dir` is a dedicated workspace isolated from `WHERE`/source dirs, so writing there cannot itself contaminate. | V2, V3 (V1 punts contamination) | STATED | No (REPORT confirms `task_dir` = `.dev/tasks/to-do/TASK-PRD-.../`) |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | "Fix the capture → gate passes" assumes the recovered document already satisfies the *non-line-count* gate criteria (`research-notes` frontmatter `[Date, Scenario, Tier]` + semantic sections). If the agent's real doc lacks those, **all three fixes green `min_lines` but the STRICT gate still HALTs.** This is a sufficiency-vs-necessity gap shared by every variant. | HIGH — could falsify the core "this fix greens the gate" claim for `research-notes` | UNSTATED / for debate (Round 2.5 Category 6) |

---

## Summary

- Total structural differences: 4
- Total content differences: 6
- Total contradictions: 3 (two are factual mischaracterizations of sibling solutions; one is the central design disagreement)
- Total unique contributions: 6
- Total shared assumptions surfaced: 3 (UNSTATED: 1, STATED: 2, CONTRADICTED: 0)
- **Highest-severity items**: C-001, C-002, C-004, C-005 (High), X-003 (High), A-001 (High), U-001/U-004 (High value)

**Taxonomy auto-tagging (for debate):**
- L3 (state-mechanics): C-002, C-004, X-003, A-001, U-001, U-004 — capture channel, contamination prevention, multi-match disambiguation, sufficiency invariant
- L2 (structural): C-001, C-005, S-002, U-003 — where the fix lives, blast radius, drift invariant
- L1 (surface): S-001, S-003, S-004, C-006 — section counts, self-positioning, effort numbers

The variants are **not** substantially identical (>10% diff): they differ on the fundamental axis of *where* the fix lives (consumer / producer / channel) and *whether contamination is prevented or merely recovered from*. Full debate warranted.

# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probed the **emerging consensus** (Sol 2 base + Sol 1 backstop + Sol 3 cwd-isolation + deferred result-event capture + frontmatter prompt edit) against the 6-category checklist, verifying claims against actual source (`executor.py`, `prompts.py`, `gates.py`, `process.py`).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "Mandate frontmatter `[Date,Scenario,Tier]` in the research-notes prompt" is necessary+sufficient for the STRICT gate | UNADDRESSED | HIGH | Doubly wrong: (a) prompt **already** emits that frontmatter (`prompts.py:224-228`); (b) PRD `_evaluate_gate` (`executor.py:678-715`) branches only on `min_lines` + `semantic_checks` — **never reads `required_frontmatter_fields`**. Frontmatter is a DEAD CONSTRAINT in the PRD pipeline (consumed only in `pipeline/`, `roadmap/`). The real load-bearing criteria are min_lines + the 2 semantic checks. |
| INV-002 | sufficiency_challenge | "The merged fix ALONE greens the research-notes STRICT gate" | UNADDRESSED | HIGH | Gate criteria that actually execute (`gates.py:330-345`→`executor.py:687-712`): (1) min_lines≥100; (2) `_check_research_notes_sections` = ALL 7 sections; (3) `_check_suggested_phases_detail` = heading + ≥1 list item. The fix guarantees the gate reads the **right file**, not that the agent **produced** ≥100 lines + 7 sections. A short-but-well-formed doc falsifies the green claim. Capture-fix ≠ content-completeness. |
| INV-003 | interaction_effects | Item 1 (pin absolute output path) and Item 3 (cwd=task_dir) are complementary, not redundant/conflicting | UNADDRESSED | MEDIUM | They partially fight (`solution-3:196,249`). Item 1 pins only the OUTPUT path; the INPUT reads ("Read actual files", `prompts.py:192`) stay relative and break when cwd flips to task_dir. Once item 1 pins an absolute output path, item 3's contamination value for output is largely moot — its residual value (constraining stray relative ops) simultaneously breaks source reads. |
| INV-004 | state_variables | `task_dir` exists before the subprocess launches with `cwd=task_dir` | UNADDRESSED | MEDIUM | `Popen(cwd=...)` raises if dir missing. Base `start()` only `mkdir`s `output_file.parent` (`pipeline/process.py:116`), which ≠ task_dir for qa/results sub-steps. Needs explicit `task_dir.mkdir(parents=True, exist_ok=True)` before Popen. |
| INV-005 | guard_conditions | WHERE-root traversal guard covers symlinks; persist still writes canonical name | ADDRESSED (persist) / UNADDRESSED (symlink) | MEDIUM | Persist OK: `_persist_step_artifact` (`executor.py:1156-1166`) writes canonical name → resume probes still work. Symlink: `rglob` can follow dir symlinks; no `realpath` containment. Adding WHERE dirs as roots **reverses** the hard-won narrowing at `executor.py:290-292` (explicit comment warning against widening to sibling dirs / prior failed runs). |
| INV-006 | collection_boundaries | Multi-match uses a deterministic mtime/path tiebreak | UNADDRESSED | MEDIUM | Source tiebreak today is `len(content) > len(best_content)` (`executor.py:360`) — **largest wins, not freshest**. A stale 300-line doc from a prior run beats a correct 150-line one. The consensus's claimed `_pick_best_candidate` (preferred_root+mtime) is Sol 1's NEW code and must be adopted deliberately. Zero-match still falls back to NDJSON (the bug) silently. |
| INV-007 | count_divergence | Merge doesn't change line counting; thresholds stay correct | ADDRESSED | LOW | `len(content.splitlines())` with `<` (`executor.py:688-689`); no off-by-one. Switching source to disk file generally **increases** count (real markdown has more newlines) → helps the 100-line gate. Unstated dependency, not a guarantee. |
| INV-008 | guard_conditions | `capture_mode` flag defaults to legacy (safe); result event verified | UNADDRESSED | MEDIUM | Flag doesn't exist in source (`prd/config.py`); "defaults to legacy" is intent. Self-contradiction in Sol 3: asserts result event works (`solution-3:207`) while flagging it unverified (Open Q1). `_extract_text_from_stream_json` (`executor.py:105-136`) has **no `type=="result"` branch** — zero code evidence the pipeline can consume a result event. |
| INV-009 | collection_boundaries | Agent writing OUTSIDE task_dir tree AND WHERE dirs is still recoverable | UNADDRESSED | LOW | search_roots=`[task_dir, task_dir.parent](+WHERE)` won't find `/tmp` or `$HOME` writes → falls back to NDJSON (the bug). Items 1+3 strongly bias toward task_dir, so low severity, but the failure is silent. |
| INV-010 | interaction_effects | `_determine_status` (sentinel/verdict on NDJSON) unaffected by moving gate content to disk | ADDRESSED | LOW | Correctly separated in source: `output_text`=NDJSON (`executor.py:609,618`) drives `_determine_status`; `gate_content`=disk file (`executor.py:613`) drives the gate. Independent inputs → sentinel detection survives. **The merge MUST preserve this split.** |
| INV-011 | state_variables | cwd=task_dir does not break scope-discovery/investigation codebase file discovery | UNADDRESSED | HIGH | scope-discovery's whole job is enumerating the PROJECT source tree ("Read actual files", `prompts.py:192,160-185`); those reads need cwd≈repo-root. task_dir is a leaf in `.dev/tasks/<...>/`. After cwd=task_dir, relative codebase exploration finds nothing → degraded scope-discovery → thin research-notes → **fails the 7-section/phases semantic checks**. Item 3 can CAUSE the research-notes gate to fail. No compensating repo-root injection. The structural fix (item 3) and the sufficiency goal are in direct tension. |

## Summary

- **Total findings**: 11
- **ADDRESSED**: 2 full (INV-007, INV-010) + 1 partial (INV-005 persist-half)
- **UNADDRESSED**: 9
  - HIGH: 3 (INV-001, INV-002, INV-011)
  - MEDIUM: 5 (INV-003, INV-004, INV-005 symlink, INV-006, INV-008)
  - LOW: 2 (INV-009) + INV-007/010 addressed

## Convergence Impact (AD-1 gate)

3 HIGH-severity UNADDRESSED invariants existed against the **naive** consensus → convergence **BLOCKED** until resolved. The merge (Steps 4-5) resolves them by revising the consensus:

- **INV-001 → resolved by DROPPING item 5** (frontmatter mandate is redundant + a dead constraint; the real risk is the semantic-section checks).
- **INV-011 + INV-003 → resolved by DEMOTING item 3** out of the hotfix: rely on item 1's absolute output-path pinning for contamination prevention (which does not break reads); keep cwd-isolation as a scoped follow-up requiring an explicit absolute repo-root injection for input reads.
- **INV-002 → resolved by SCOPING the claim**: the fix guarantees the gate evaluates the agent's *real* document; whether that document is complete is correctly the gate's decision (a thin doc *should* HALT). Content-quality is out of scope for a capture fix.

Post-revision, no HIGH+UNADDRESSED invariants remain in the merged design; MEDIUM items (INV-004, INV-005, INV-006, INV-008) are addressed by specific merge provisions.

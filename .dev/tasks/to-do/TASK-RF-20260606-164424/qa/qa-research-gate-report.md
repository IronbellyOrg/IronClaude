# QA Report — Research Gate

**Topic:** PRD document-capture layered hotfix (Layers 1-3 + AC1-AC10)
**Date:** 2026-06-06
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Assigned research files (6):
- 01-prompts-builders-inventory.md
- 02-executor-resolve-and-split.md
- 03-gates-strict-criteria.md
- 04-test-patterns-prd.md
- 05-design-codeblock-crossvalidation.md
- 06-mdtm-template-examples.md

Independent re-verification targets (source of truth):
- src/superclaude/cli/prd/prompts.py
- src/superclaude/cli/prd/executor.py
- src/superclaude/cli/prd/gates.py
- tests/cli/prd/

_Findings appended incrementally below._

---

## Overall Verdict: PASS (with 1 MINOR correction)

The research is dense, evidence-based, and actionable. Every load-bearing claim I independently re-verified against source held true. One MINOR misquote found (file 01's `_TRUNCATION_MARKER` literal). No CRITICAL or IMPORTANT gaps — the builder has everything needed to land Layers 1-3 + AC1-AC10 per-file/per-AC.

---

## Items Reviewed (independent re-verification)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `_STEP_ARTIFACT_FILES` 8 keys + values | PASS | `sed 252-263` executor.py — exactly 8 keys, byte-identical to files 02 & 05 tables (3 QA values carry `qa/` prefix). build-task-file/assembly correctly absent (comment at 280-292 confirms the clobber rationale). |
| 2 | `_resolve_step_content` signature 3-arg `(step_id, task_dir, ndjson_text)` | PASS | `sed 266` — exact match. Confirms files 02/04/05: WHERE must be read INTERNALLY (stays 3-arg), not a 4th param. |
| 3 | `len(content) > len(best_content)` tiebreak sites | PASS | grep → 3 hits: **298, 329, 360**. Matches file 02's claim exactly (298=build-task-file, 329=assembly, 360=generic primary target). |
| 4 | Zero-match fallback returns `ndjson_text` | PASS | `sed 339-341,365` — early `return ndjson_text` (341) + final `return best_content if best_content.strip() else ndjson_text` (365). Matches files 02 & 04. |
| 5 | INV-001: `required_frontmatter_fields` read sites in executor.py | PASS | grep `required_frontmatter_fields\|frontmatter` → **exit 1, ZERO hits**. `_evaluate_gate` (686-705) reads only `min_lines` + `semantic_checks`. Confirms files 02 §4 & 05 Claim 9 — dead constraint, dropping the mandate is correct. |
| 6 | INV-010 split (`output_text` NDJSON vs `gate_content` disk) | PASS | `sed 609-623` — `output_text`=`_extract_text_from_stream_json` (609) → `_determine_status` (618); `gate_content`=`_resolve_step_content` (613-615) → `_evaluate_gate` (623). Exactly as files 02 §3 & 05 Claim 8 describe. Lines 609/613/618/623 all exact. |
| 7 | `_check_*` `bool\|str` convention | PASS | grep → all 10 checks `def _check_*(content: str) -> bool \| str`. Confirms files 03 §4 & 05 Claim 7. New fn must match. |
| 8 | Net-new symbols absent today | PASS | grep `_check_no_truncation_marker\|_artifact_path_for_step\|_pick_best_candidate` across all 3 src files → **exit 1, ZERO hits**. `_STEP_ARTIFACT_PATTERNS` also absent (exit 1). Confirms file 04's "red-first" framing. |
| 9 | research-notes STRICT gate block 329-346 | PASS | `sed 329-346` — `min_lines=100`, `enforcement_tier="STRICT"`, `required_frontmatter_fields=["Date","Scenario","Tier"]`, 2 semantic checks. Byte-exact match to file 03 §1. |
| 10 | 4 target builders exist + un-pinned | PASS | grep defs: scope_discovery@110, research_notes@194, sufficiency_review@269, preparation@516. All present. Matches files 01 & 05. |
| 11 | Pin idioms L439 (`Write...to:`) + L887 (`Output path:`) | PASS | `sed 439` = task-file pin; `sed 887` = `Output path: {config.qa_dir / "analyst-completeness-report.md"}`. Both exact. |
| 12 | Path imported, PrdConfig TYPE_CHECKING-only | PASS | `sed 13-27` — `from pathlib import Path` @17; `PrdConfig` under `if TYPE_CHECKING:` @26-27; `from __future__ import annotations` @13. Confirms files 01 & 05 Claim 1 — no circular-import risk. |
| 13 | "build_sufficiency_review = JSON producer" | PASS | `sed 301` = `Return JSON:`. Confirms file 01 §1c & 05 Claim 2 — NOT a free-form doc. |
| 14 | "build_preparation = .preparation-complete marker" | PASS | `sed 541,546` = "Create a .preparation-complete marker file" / "Write a brief status report to .preparation-complete". Confirms files 01 §1d & 05 (weakest pin target). |
| 15 | "2 of 4 are clean markdown producers" claim | PASS | scope-discovery has literal `OUTPUT FORMAT:` @154; research-notes has "Produce a research-notes.md file with EXACTLY these 7 sections" @222 + DO-NOT-TOUCH frontmatter @224-228. Sufficiency (JSON) + preparation (marker) are not. Claim is ACCURATE — not an overstatement. |
| 16 | WHERE key uppercase, produced in parse-request | PASS | grep → `"WHERE": [...]` @87 (emitted by build_parse_request_prompt), read @117-119 by scope-discovery. Confirms files 04 & 05 Claim 4. Test fixture writes `"WHERE": ["src/"]` @test_prompts.py:54. |
| 17 | Truncation-marker test string | **PASS (claim corrected)** | `_TRUNCATION_MARKER = "\n\n[TRUNCATED — file exceeds 50KB inline limit]"` @prompts.py:34, emitted by `_read_file` @46; test asserts same @test_prompts.py:252. File 04 §6 quotes this EXACTLY (em-dash included). File 01 §3 misquotes it as `"..."` — see Issue 1. |
| 18 | Python >=3.10 (is_relative_to / resolve(strict)) | PASS | `pyproject.toml:16` `requires-python = ">=3.10"`. Confirms file 05 Claim 4/6. |
| 19 | test dir exists + AC→pattern mapping plausible | PASS | `ls tests/cli/prd/` → test_resolve_step_content.py, test_gates.py, test_prompts.py, test_executor.py, test_e2e.py, test_path_resolution.py all present + `__init__.py`. File 04's mapping is sound. |
| 20 | Line-number drift table (file 05 §11) accuracy | PASS | Spot-checked: build_task_file_prompt def @359 (not a claimed anchor — pin is @439, correct); `_STEP_ARTIFACT_PATTERNS` insertion after 263 (file 05 flags design's "~252" as stale by ~12 — CORRECT). CONTRADICTED/stale items properly flagged. |

## Summary
- Checks passed: 20 / 20 (one with a corrected sub-claim)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence
- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: ~10 (within Bash) | Glob: 0 | Bash: 5
- No web research performed (all claims intrinsically local; no external lookup triggered).
- Note: tool-call count (12 incl. 7 Reads + 5 Bash batches each running multiple greps/seds) exceeds the 20-item checklist via batched greps; each grep/sed maps to a specific item above.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 01-prompts-builders-inventory.md §3 line 24 | Misquotes `_TRUNCATION_MARKER` as `"..."` (ellipsis). Actual value at prompts.py:34 is `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"`. File 04 §6/§AC9 and file 05 quote it correctly, so the builder has the right string from two of three sources — but a builder reading only file 01 would author AC9's truncation-marker test against `"..."` and the gate would never detect the real marker. | Correct file 01's quote to the literal marker, OR (builder mitigation) source the AC9 marker string from file 04 §6 / test_prompts.py:252, which are accurate. Cross-validated: not a blocker. |

## Adversarial Cross-File Coverage Check (no partition — full assigned set)
- **Contradictions between files:** NONE that conflict on substance. The one cross-file divergence (truncation marker: file 01 `"..."` vs file 04/05 full literal) is a file-01 transcription error, not a genuine source disagreement — files 04 & 05 agree with source. Surfaced as Issue 1.
- **`_resolve_step_content` stays 3-arg:** Files 02, 04, 05 ALL independently conclude WHERE is read internally from `parsed-request.json` (not a 4th arg). Consistent + verified (sig @266). No gap.
- **Canonical filename per pinned step:** File 01 §5 + file 02 §1 + file 05 Claim 1 give the exact 8-name mapping; scope-discovery→`scope-discovery-raw.md`, research-notes→`research-notes.md`. Builder has per-step filenames. No gap.
- **sufficiency-review / preparation as pin targets:** Both file 01 §5 and file 05 §1b RISK FLAG independently warn these two are semantically weak pin targets (JSON verdict / dotfile marker). This is correctly surfaced as an AMBIGUITY for the builder/design, not silently asserted. Actionable.
- **gates wiring ambiguity (define-only vs wire-into-gate):** File 03 §5 surfaces the "STRICT stays unchanged vs actually guard at runtime" tension explicitly and recommends NOT silently wiring. File 05 Claim 7 notes the same registration requirement. Properly flagged — not resolved silently. Builder must get a design decision (R5) before wiring.
- **Coverage gaps the builder needs:** I found NONE missing. Exact canonical filenames ✓, 3-arg signature ✓, Python version ✓, WHERE production ✓, injection anchors per builder ✓, test templates per AC ✓, MDTM template structure ✓.

## Per-Builder / Per-AC Actionability (spot check)
- Files 01/02/03 give exact def-line ranges, injection anchors, and the copy-target idiom → per-file edits are unambiguous.
- File 04 gives an AC→test-file→existing-pattern table (AC1–AC10) with file:line templates → per-AC test authoring is unambiguous (modulo Issue 1's marker string, mitigated by file 04 itself carrying the correct string).
- File 06 gives the MDTM Template 02 structure, B2 6-element pattern, and a real fully-formed example → the task-builder can structure the task file correctly.

## Recommendations
1. Builder: when authoring the AC9 truncation-marker test, use the literal `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (from file 04 §6 / prompts.py:34 / test_prompts.py:252) — do NOT trust file 01's `"..."` shorthand.
2. Builder: resolve the two surfaced AMBIGUITIES before integration — (a) whether sufficiency-review/preparation get canonical-artifact pins at all (file 01 §5, file 05 §1b), and (b) whether `_check_no_truncation_marker` is wired into research-notes `semantic_checks` (which re-opens the "STRICT unchanged" constraint) or defined+unit-tested only (file 03 §5). Both are correctly flagged for a design decision; do not let the builder silently pick.
3. Builder: note file 05's soft semantic flag that `task_dir.parent` = the output root (`.dev/eval-workspaces/`), so WHERE-root widening frequently no-ops under sandbox — fails safe, but Layer 1 pinning is the load-bearing fix.

## VERDICT: PASS

## QA Complete


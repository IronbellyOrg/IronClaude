# QA Report — Research Gate (Gap-Detection + Staleness-Tag Lens) (Partition C)

**Topic:** FR-RH2 Headless Ensemble Fix — reflect Tier-2 ensemble via swarm dispatch library
**Date:** 2026-06-20
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** gap-detection + documentation-staleness tag compliance
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume untagged claims and unflagged gaps exist until proven otherwise

PRIMARY ASSIGNED FILES:
- `research/08-precedents-adversarial-handoff.md`
- `research/web-01-inprocess-import-vs-subprocess-fanout.md`
PLUS full re-scan of `research/00-08` for doc-staleness tag compliance.

[PARTITION NOTE: This is the staleness-tag + gap-detection lens (Partition C). Evidence-density, scope-coverage, incremental-writing, and integration-point checks are the remit of sibling partitions. Cross-file contradiction analysis here is limited to tag-discipline and the four assigned verification dimensions (a)-(d).]

---

## Overall Verdict: PASS

The four assigned verification dimensions (a-d) all hold. Every doc-sourced architectural
claim across files 00-08 carries a verification tag; every `[CODE-CONTRADICTED]`/`[UNVERIFIED]`
claim is surfaced in a Gaps/caveats section (none asserted as settled body fact); the
`pipeline/process.py` orthogonality verdict in `08` was reached FROM evidence (docstring +
grep, which I independently reproduced) rather than assumed; and `web-01` carries a URL +
relevance rating on all 14 findings with explicit supplementary framing.

Four MINOR evidence-citation imprecisions were found in `08` (off-by-one line counts and one
over-stated "zero grep hits" claim). None changes a conclusion — every substantive
`[CODE-VERIFIED]` claim I spot-checked was independently confirmed against live source. Per
adversarial standard these are logged below as MINOR findings. They are citation-precision
nits, not research gaps that would cause synthesis to hallucinate; with `fix_authorization:
false` they are reported for the orchestrator to optionally have corrected. They do NOT, in my
judgment as the staleness-tag lens, constitute a gate-blocking gap on the four dimensions I own.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (a) Every doc-sourced architectural claim in 00-08 carries `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` | PASS | Tag inventory across 10 files: 01=34CV/3CC/6UV, 02=8/0/3, 03=10/0/2, 04=14/0/3, 05=27/2/2, 06=6/0/4, 07=12/0/2, 08=21/3/1. `00` (0 tags) is a faithful spec-transcription (self-declares L9), not a code investigation → tagging rule N/A. `web-01` (0 CV tags) is pure external research → carries URL+relevance instead. |
| 2 | (b) `[UNVERIFIED]`/`[CODE-CONTRADICTED]` surfaced in Gaps/caveats, not asserted as body fact | PASS | Placement scan vs each file's `## Gaps` header. 02/04/06/07: all non-VERIFIED tags fall in Gaps. 05: all in Gaps or self-labeled "(see Gaps)". 08: contradiction labeled a "seam-level gap, surfaced in Gaps" (L132) + restated L179; sole `[UNVERIFIED]` at L180 inside Gaps. 01 L246-247 + 03 L262 are in-body but under "Constraints/caveats" headings, hedged ("not exhaustively searched", `[UNVERIFIED]` blockquote), and restated in formal Gaps. No bare assertion of a contradicted claim found. |
| 3 | (c) `08` `process.py` role determined FROM evidence (read + concluded orthogonal), not assumed | PASS | Note §3 cites docstring L1-10 (process manager, "Extracted from sprint/process.py") + a grep for adversarial/reflect/suspect/final_path/merge/swarm. I reproduced: docstring matches verbatim; `class ClaudeProcess` L72, `start` L162, `wait` L260, `terminate` L278, `validate_tool_write_output` L325, `PromptTooLargeForArgv` L61 all present. Orthogonality verdict is evidence-backed. |
| 4 | (c-detail) `08`'s "grep returned zero hits" for process.py audit terms | MINOR FAIL | My grep found ONE hit: L151 `env_vars... are merged with override semantics` — a benign "merged" in an env-var docstring, NOT a merge-contract field. Note's "zero hits" (L108) is technically false; substantive claim (no audit-contract awareness) still holds. |
| 5 | (d) `web-01` findings carry source URLs + relevance ratings, framed supplementary | PASS | 14 findings / 14 `URL:` lines / 14 `Relevance:` lines / 14 inline `[HIGH\|MEDIUM\|LOW]` headers — 100% coverage. Supplementary framing: scope note L8-10 ("LIGHT supplementary... codebase is the source of truth; nothing below overrides verified code"), recommendations header L147 ("supplementary; codebase still governs"). |
| 6 | `08` central honesty: `ensemble.py` flagged as design-target, not existing code | PASS | Note L23, L180 state `ensemble.py` does not yet exist. Confirmed: `ls src/superclaude/cli/reflect/` = commands/config/contract/__init__/models/runner.py — NO ensemble.py. All "should hand…" framed as design targets. Cross-confirmed by 05 L251 (`find -name *ensemble*` returns nothing). |
| 7 | `08` `--suspect-source` `[CODE-CONTRADICTED]` claim accurate | PASS | Confirmed: `bare_review.py` L67 emits `--suspect-source {suspect_files}`; `grep -ic suspect` on `sc-adversarial-protocol/SKILL.md` (3002 lines) = **0**. The contradiction is real and correctly tagged. |
| 8 | `08` commands.py handoff mechanics (succeeded final_paths) accurate | PASS | Read commands.py L2058-2081: `succeeded_final_paths` filtered on `status=="success" and w.final_path`; `compare_files = ["<existing-review>", *paths]`; `suspect_files = paths or "<no-bare-files>"` — matches note §1.3 exactly. |
| 9 | `08` validate_executor §21-alternative citation accurate | PASS | `_build_multi_agent_steps` at L317 (note: L317-378 ✓); `adversarial-merge` step L366, `build_merge_prompt([str(p) for p in reflect_outputs])` L367 — per-reviewer-artifact merge confirmed. |
| 10 | Line-count / inventory precision in `08` evidence index | MINOR FAIL | Three off-by-one / incomplete citations: process.py "354 lines" (actual 353); bare-review SKILL "81 lines" (actual 80); reflect-package list omits `__init__.py`. Cosmetic; no conclusion affected. |

---

## Summary
- Checks passed: 8 / 10
- Checks failed: 2 (both MINOR, both evidence-citation precision in `08`)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- **Assigned-dimension verdict (a,b,c,d): all PASS**

## Confidence
**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 7
> Note: greps were issued via Bash (batched), not the Grep tool. Total verification tool calls (10) ≥ checklist items (10). No web research performed (all claims verified against local source-of-truth; web-01's own external URLs were not re-fetched — verifying that 14/14 findings carry a URL+rating is a structural check, not a claim-truth check, and is in-scope; re-fetching external pages is out-of-scope for this gap-detection lens).
- No UNCHECKED items.
- No UNVERIFIABLE items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `08` §3 L108 | Claims "grep returned zero hits" for process.py audit terms; actually 1 benign hit (L151 `env_vars...are merged`). | Reword to "one benign hit (`merged` in an env-var docstring), no audit-contract field references" — preserves the true conclusion. |
| 2 | MINOR | `08` §0 evidence index | process.py "full file (354 lines)" → 353; `sc-bare-review/SKILL.md` "81 lines" → 80. | Correct the two line counts (off-by-one). |
| 3 | MINOR | `08` L23 | Reflect-package inventory lists commands/config/contract/models/runner.py but omits `__init__.py`. | Add `__init__.py` to the list (or note "modules" to exclude the package init). |

## Actions Taken
None — `fix_authorization: false`. All three MINOR findings are reported for the orchestrator
to optionally route to a fixer. None blocks the four assigned dimensions.

## Recommendations
- **Gate decision is the orchestrator's** after merging all partition reports. On MY four
  assigned dimensions (a-d) the verdict is PASS. The three MINOR items are citation-precision
  corrections, not research gaps — they do not risk synthesis hallucination because every
  load-bearing `[CODE-VERIFIED]` conclusion was independently re-confirmed against live source.
- If the orchestrator applies strict "ALL gaps regardless of severity = FAIL", the three MINOR
  `08` citation nits would technically convert the overall gate to FAIL and warrant a one-pass
  fix cycle on `08` only. I flag this honestly rather than suppress it; my dimension-scoped
  verdict remains PASS.
- `00-prd-extraction.md` lacks a `## Gaps` section — acceptable for a pure spec-transcription
  file (its OI items live in the spec and are carried into `08` §5). Not a finding; noted for
  the merge so another partition does not double-flag it.

## QA Complete

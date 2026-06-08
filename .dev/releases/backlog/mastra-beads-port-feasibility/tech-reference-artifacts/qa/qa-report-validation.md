# QA Report — Report Validation

**Topic:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (Technical Reference)
**Date:** 2026-06-03
**Phase:** report-validation
**Fix cycle:** N/A (initial validation; fix-authorized)
**Document:** `.dev/releases/backlog/mastra-beads-port-feasibility/ARCHITECTURE-TECHNICAL-REFERENCE.md`
**Template:** `.claude/templates/documents/technical_reference_template.md`
**Code baseline:** HEAD `9e864860` (`9e8648603636d6b9f8fab9e261e583d0de849f34`; package v4.2.0)

---

## Overall Verdict: PASS (after in-place fixes — 3 path errors, 2 Edit operations)

The document is template-compliant, within the HEAVYWEIGHT line budget, evidence-bound, and rigorously demarcated built-vs-design. Three Evidence-Trail path errors (§15.4) were found and fixed in-place — `web-01..04` and `RF07` were mis-attributed to the TECHREF task dir (actually under the RESEARCH task dir), and `00-evidence-index.md` was mis-attributed to the RESEARCH task dir (actually under the TECHREF task dir). All confirmed-fact spot-checks (rerun-tasks absent, Mastra 1.1.0+, src/ canonical, CERTIFY_GATE unwired, Path A skips _verify_checkpoints) are stated correctly and were NOT reverted. After fixes, the document passes report validation.

---

## Adversarial Verification Summary

This was a hostile review. Every load-bearing `[CODE-VERIFIED]` claim flagged in the spawn prompt was independently re-read against the live source at HEAD `9e864860` (not trusted from the document or upstream research). Tool engagement is below.

---

## Items Reviewed

### A. 15-item Validation Checklist + 5 Content Quality Checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 16 sections present (or N/A w/ rationale) | PASS | `grep -nE "^## [0-9]+\."` returns §1–§16 in order (lines 166–1709). §6/§7 explicitly repurposed with REPURPOSE NOTE; conditional §8/§9 marked INCLUDED with rationale. |
| 2 | Problem Statement references research question | PASS | §1 Overview + §1 CRITICAL callout state the PROPOSED hybrid + feasibility verdict (Conditionally Recommended, Option D→A). |
| 3 | Current State cites file:line for every claim | PASS | §5.1–5.4 every `[CODE-VERIFIED]` row carries `path:line` (e.g. `pipeline/process.py:24-244`, `executor.py:41-60`). Re-read confirmed accurate. |
| 4 | Gap Analysis has severity ratings | PASS | §14.2 (D1–D9 Severity col), §14.3 (R1–R9 Severity col). |
| 5 | External Research Findings include source URLs | PASS | §5.7 / §8.1 / §9.2 / §9.3 every `[EXTERNAL-VERIFIED]` row has Source URL (mastra.ai, github.com/MrLesk, github.com/gastownhall, modelcontextprotocol.io). |
| 6 | Options Analysis ≥2 options w/ comparison | PASS | §2.3 Key Design Decisions table; Option B (native) vs D→A strangler-fig contrasted in §2.3, §12.3, §14.1. |
| 7 | Recommendation references comparison | PASS | §2.3 + §14 CRITICAL: "Option D → Option A ... NOT a native rewrite" rests on §2.3 rationale columns. |
| 8 | Implementation Plan has specific paths/actions | PASS | §13 recipes A/B/C cite real existing-side files (`tasklist/executor.py:191-218`, `eval/isolation.py:224-260`) + ordered steps. |
| 9 | Open Questions table has impact + resolution | PASS | §14.4 Future Considerations (Deferred Because + Revisit When); gaps file present separately. |
| 10 | Evidence Trail lists every research/synthesis file | **PASS (after fix)** | §15.4 — 3 path errors found and fixed (Issues #1–#3). After fix all 7 artifact rows resolve on disk. |
| 11 | No full source-code reproductions | PASS | 3 `python` fences (lines 572, 659, 742) are signature/field-list summaries (Public Interface), not function bodies — template-permitted. |
| 12 | Tables over prose for multi-item data | PASS | Overwhelmingly tabular; ASCII diagrams for architecture (§2.1, §4.1, §7.1). |
| 13 | No assumptions presented as verified facts | PASS | Every architectural claim carries exactly one tag; design claims use proposed/conditional phrasing. |
| 14 | No doc-only architectural claims in §2/6/7/8 | PASS | Architecture/contract claims in §2, §6.2, §7.2 all carry `[CODE-VERIFIED]` path:line; external capability claims carry `[EXTERNAL-VERIFIED]` URLs, never presented as repo architecture. |
| 15 | CODE-CONTRADICTED / STALE findings surfaced in §14 | PASS | D1–D9 capture all stale/contradicted findings. D6 (ORIGINAL-output comment) independently re-verified at executor.py:1217-1219 vs _gate_target 23-35. |
| 16 | ToC accuracy | PASS | §5.1–5.8 ToC anchors match header slugs incl. `-code-verified` suffix; §1–§16 anchors match. |
| 17 | Internal consistency | **PASS (after fix)** | Only inconsistencies were the 3 Evidence-Trail path mismatches (now fixed). Tags, counts (42/39/24), version pins consistent throughout. |
| 18 | Readability | PASS | Tiered tables, callouts, ASCII diagrams; HEAVYWEIGHT tier appropriate. |
| 19 | Actionability (dev could start from §13) | PASS | §13 recipes are strangler-fig increments with real hook-points, parity gates, pitfalls; §13.2 maps change-types to tests. |

### B. TEMPLATE_COMPLIANCE

| Check | Result | Evidence |
|-------|--------|----------|
| All sections present or N/A w/ rationale | PASS | 16/16 present; §6/§7 repurposed with explicit notes; conditional sections marked INCLUDED. |
| HEAVYWEIGHT budget 1,200–1,800 lines | PASS | `wc -l` = 1,759. Unchanged by fixes (string replacements). |
| No subsystem section >200 lines | PASS | 5.1=90, 5.2=72, 5.3=84, 5.4=46, 5.5=56, 5.6=50, 5.7=58, 5.8=40 — all <200. |
| Frontmatter complete | PASS | id/title/version/status/type/priority/created_date/verified_against_code all present + non-empty. |

### C. EVIDENCE_TRAIL

| Check | Result | Evidence |
|-------|--------|----------|
| Every `[CODE-VERIFIED]` cites real source path:line | PASS | Independently re-read at HEAD 9e864860: StepRunner (executor.py:41-60), ClaudeProcess Popen (process.py:134), build_command (73-95), gate_passed (gates.py:20), grace_period default (models.py:232) + coercion (executor.py:213-214) — all exact. |
| Every `[EXTERNAL]` cites a URL | PASS | All `[EXTERNAL-VERIFIED]` rows carry source URLs. |
| Every `[DESIGN]` cites feasibility/research source | PASS | Design claims trace to FEASIBILITY-STUDY / ROADMAP / DECISION-SUMMARY / RF07 / web-01..04. |
| Evidence Trail artifact files exist on disk | **PASS (after fix)** | 3 path errors corrected; all 7 §15.4 rows now resolve. |

### D. BUILT_VS_DESIGN_TAGS

| Check | Result | Evidence |
|-------|--------|----------|
| Every architectural claim tagged | PASS | 294 `[CODE-VERIFIED]`, 163 `[DESIGN — UNBUILT]`, 124 `[EXTERNAL-VERIFIED]`, 14 `[DESIGN — UNVERIFIED]` occurrences; §1.1 mandates exactly-one-tag. |
| Built-vs-Design Status Ledger present in §15 | PASS | §15.3 ledger, one row per subsystem 5.1–5.8 with full Status vocabulary. |
| NO design claim presented as built | PASS | §5.5/5.6/5.8 lead with CRITICAL `[DESIGN — UNBUILT]` banners; §1/§14/§15.1 repeatedly state hybrid does not exist at HEAD. |
| §1 legend lists 3 canonical tags + §11 sub-variant | PASS | §1.1 table lists the 3 canonical tags; Note explicitly acknowledges the §11-only `[DESIGN — UNVERIFIED]` sub-variant ("not a fourth canonical tag"). |

### E. Spot-checks of confirmed facts (must NOT be reverted)

| Confirmed fact | Result | Independent verification at HEAD 9e864860 |
|----------------|--------|-------------------------------------------|
| `sprint rerun-tasks` ABSENT | CORRECT | `grep -rn "rerun-tasks\|rerun_tasks" src/.../sprint/` = 0 hits; Click group registers exactly run/attach/status/logs/kill/verify-checkpoints (commands.py:71/293/305/317/342/360). Stated ABSENT in §14.1 L8, §15.1, §15.3. |
| Mastra core `1.1.0+` (NOT 1.34.0/1.16.0) | CORRECT | Doc uses `1.1.0+` consistently (lines 277, 946, 986, 1190, 1270, 1598). web-01 source line 32 confirms "Added in `@mastra/core@1.1.0`". No 1.34/1.16 anywhere. |
| `src/superclaude/` canonical | CORRECT | core/CLAUDE.md:17-29 designates src/ source-of-truth; harness counts 42/39/24 re-confirmed exact on disk. |
| CERTIFY_GATE unwired | CORRECT | Defined gates.py:1324 + ALL_GATES:1440; `build_certify_step(`/`check_certify_resume(` have ZERO call invocations (only def lines 1899/3483); `_build_steps` terminates at remediate (2196-2204); comment 2205 unbacked. |
| Path A skips `_verify_checkpoints()` | CORRECT | Sole `_verify_checkpoints()` call at executor.py:1519 (Path B, after PASS guard); Path A `continue`s at :1301; def at :1811. |

---

## Summary

- Validation checks passed: 19/19 (after fixes resolving 3 path errors)
- Template-compliance / Evidence-trail / Built-vs-design / spot-checks: all PASS
- Checks failed (pre-fix): 2 distinct checklist items (#10 Evidence Trail, #17 Internal Consistency) due to 3 underlying path errors
- Critical issues: 0
- Issues fixed in-place: 3 path corrections (2 Edit operations)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | IMPORTANT | §15.4 Evidence Trail | `web-01..04` cited under `TASK-TECHREF-20260603-021348/research/` but files live under `TASK-RESEARCH-20260602-211124/research/`. | Repoint to RESEARCH task dir. | FIXED |
| 2 | IMPORTANT | §15.4 Evidence Trail | `07-target-data-model-and-ownership.md` (RF07) cited under TECHREF dir but lives under `TASK-RESEARCH-20260602-211124/research/`. | Repoint to RESEARCH task dir. | FIXED |
| 3 | IMPORTANT | §15.4 Evidence Trail | `00-evidence-index.md` cited under `TASK-RESEARCH-20260602-211124/research/` but lives under `TASK-TECHREF-20260603-021348/research/`. | Repoint to TECHREF task dir. | FIXED |

No fabrication, no hallucinated source-code paths, no reverted facts, no doc-only-architecture-as-built, no design-claim-presented-as-built were found. All three issues were directory-attribution errors in the Evidence Trail; the files exist and the content is correct.

---

## Actions Taken (fix-authorized)

- Edit 1 (Issues #1 + #2): repointed `web-01..04` and `07-target-data-model-and-ownership.md` from `TASK-TECHREF-20260603-021348/research/` → `TASK-RESEARCH-20260602-211124/research/`. Target files verified via `find`.
- Edit 2 (Issue #3): repointed `00-evidence-index.md` from `TASK-RESEARCH-20260602-211124/research/` → `TASK-TECHREF-20260603-021348/research/`. Verified via `find`.
- Re-verified post-fix: `grep -nE` over §15.4 shows all 7 artifact rows now point at directories where the files exist.
- Line count unchanged at 1,759 (string-only replacements).

---

## Recommendations

- None blocking. Document is ready to present.
- (Non-blocking) The Completeness Status line "All links verified — Pending QA" can now be considered satisfied for Evidence-Trail paths; "Reviewed by orchestration-platform-team" remains a human sign-off, out of QA scope.

---

## Confidence Gate

**Confidence:** Verified: 33/33 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Every item carries a cited tool action or file:line. (33 = 19 validation/content + 4 template + 4 evidence-trail + 4 built-vs-design + 2 net distinct spot-check facts not already covered elsewhere.)

**Tool engagement:** Read: 7 | Grep: ~18 (within Bash) | Glob: 0 | Bash: 11 | Edit: 4 | Write: 1

Verification-action count (~37) exceeds checklist item count — not padding-suspect. No live web research performed: all `[EXTERNAL-VERIFIED]` claims were verified against the already-fetched local `web-01..04` research files (source-truth-first); the Mastra 1.1.0 fact was confirmed in `web-01-mastra-current-capabilities.md` line 32. `tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`.

**Every UNCHECKED item:** none.
**Every UNVERIFIABLE item:** none.

## QA Complete

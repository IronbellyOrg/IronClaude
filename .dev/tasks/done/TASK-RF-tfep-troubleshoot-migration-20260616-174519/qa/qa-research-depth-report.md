# QA Report — Research Depth Lens

**Topic:** TFEP /sc:forensic → /sc:troubleshoot migration tasklist
**Date:** 2026-06-16
**Phase:** research-depth (qualitative)
**Lens:** Is research DEEP enough for granular, self-contained Template-02 items WITHOUT re-reading source?
**Fix authorization:** false (report-only)
**Files reviewed:** 01-file-inventory.md, 02-troubleshoot-surface.md, 03-integration-and-sync.md, 04-template-and-examples.md (ALL .md in research dir)

---

## Overall Verdict: PASS

The research corpus is genuinely deep, not surface-level. It consistently exceeds "edit line N" by supplying the WHAT — proposed replacement prose, full field schemas with types, exact new flag-row text, audit-header key insertions, the report-consumer block field set, and the verbatim verify-sync commands. Adversarial entry stance ("assume shallow until proven deep") was rebutted by the evidence: every one of the five depth probes (a)–(e) from the lens brief is satisfied with content-level guidance, and four independent source spot-checks confirm the cited anchors are byte-accurate (no AX-1 citation drift). Issues found are MINOR ambiguities/hand-offs that a Template-02 builder can resolve without re-reading source; none rise to IMPORTANT or CRITICAL on the depth axis.

---

## Depth Probes (the 5 lens-required capabilities)

| Probe | Builder needs | Research provides | Depth verdict |
|---|---|---|---|
| (a) new "diagnostic escalation" prose + `diagnostic_backend:` declaration | replacement wording + a concrete declaration to write | R1 §B gives the exact 8 "forensic" prose sites with verbatim surrounding text and the rename target ("diagnostic escalation"); R1 §C gives TWO concrete `diagnostic_backend:` insertion points (section-top ~L136 single-source-of-truth, vs Step-3-adjacent ~L204 low-blast-radius) with the trade-off stated. **Gap:** the literal *value/shape* of the `diagnostic_backend:` declaration line is not spelled out verbatim. | DEEP-with-MINOR-gap |
| (b) return-contract.yaml field schema (donor fields + 5 missing fields w/ types) | full donor enumeration + the 5 absent fields + types | R2 §B3 enumerates ALL 30 donor fields with Field+Type+line; the donor→TFEP mapping table names the 5 MISSING fields explicitly (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`/block-path, `root_cause_summary`, `solution_summary`) with per-field synthesis source. R3 §4 independently corroborates. | DEEP |
| (c) new `--context`/`--caller` flag rows + Wave 0 parse text + audit-header keys | copy-pasteable row text, exact parse-sentence edit, header key insertion | R2 §A2 supplies VERBATIM proposed table rows for `--context` and `--caller` (correct `(none)` sentinel per L52 precedent); R2 §B1 gives the exact L115 `Optional:` sentence to extend + a proposed RESOLVE sub-step; R2 §B2 gives the exact `caller:`/`context_path:` header lines + insertion point (after L136). | DEEP |
| (d) report-template TFEP-consumer block contents | insertion anchor + field set | R3 §2 pins the anchor (after L154 `## Next Steps`, before L156 `### Hard-stop variant`) — confirmed byte-accurate; R3 §4 + R2/A5 name the block's field set (`remediation_target`, `tasklist_insertion_recommendation`, `safe_to_auto_insert`) and the human-side/machine-side mirror pattern. **Hand-off:** R4 is declared owner of "exact field set / fencing" — R4 confirms it owns mechanics but does not itself re-enumerate the fields; the field set lives in R3. Cross-file but coherent. | DEEP |
| (e) exact verify-sync commands | literal commands | R3 §3 / §5 + R4 §I18 give the verbatim gate sequence: `make sync-dev` then `make verify-sync` (expect exit 0), plus the residual-reference `rg` gates and the never-stage-`.claude/` constraint. | DEEP |

All five probes pass. (a) and (d) carry MINOR residue noted below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R1 anchors WHAT not just WHERE | PASS | §B tables carry verbatim surrounding text per line, not bare line numbers; rename target term stated. |
| 2 | R1 `diagnostic_backend:` insertion guidance | PASS (minor) | Two insertion points + trade-off given; literal declaration value not spelled out. |
| 3 | R2 donor field schema completeness | PASS | All 30 fields w/ types+lines (B3); verified byte-accurate vs source L41–72. |
| 4 | R2 five-missing-fields identified w/ synthesis source | PASS | Mapping table names all 5, each with donor/synthesis origin. |
| 5 | R2 `--context`/`--caller` row text verbatim | PASS | A2 gives copy-pasteable rows w/ correct `(none)` sentinel. |
| 6 | R2 Wave 0 parse-text edit | PASS | B1 cites exact L115 sentence (verified) + proposed sub-step. |
| 7 | R2 audit-header key insertion | PASS | B2 gives `caller:`/`context_path:` lines + insertion after L136. |
| 8 | R3 contract-mismatch articulated (adapter rationale) | PASS | §0.2 + §4 enumerate 5 concrete gaps the adapter must close. |
| 9 | R3 report-template anchor accuracy | PASS | Verified: `## Next Steps` L146, `### Hard-stop variant` L156 — anchor "after L154 / before L156" correct. |
| 10 | R3 verify-sync/sync-dev commands verbatim | PASS | §3/§5 give literal commands + residual-ref `rg` gates. |
| 11 | R3 LIVE-vs-HISTORICAL separation | PASS | §1A–1D separate the one live surface from ~80 historical hits — prevents over-editing. |
| 12 | R4 Template-02 item shape (B2 6-field) | PASS | §PART A B2 + §PART B canonical item structure with worked example. |
| 13 | R4 M3 QA-gate encoding depth | PASS | §M3 8-step sequence + example PG2.1–PG2.6 mapping. |
| 14 | R4 POST-reflect wrapper shape | PASS | PC.5 flat-Bash wrapper w/ recursion guard + exit-code consumption detailed. |
| 15 | R4 M4 applicability decision | PASS | I21 transformation-exemption stated; builder decision criteria given. |
| 16 | Citation freshness (AX-1 drift probe) | PASS | 4/4 source spot-checks byte-accurate (task-protocol L205–216, troubleshoot L41–72 + L115, report-template L146/L156). |
| 17 | Cross-file coherence / ownership hand-offs | PASS (minor) | R1/R2/R3/R4 declare non-overlapping ownership; one field-set lives in R3 while R4 owns "mechanics" — coherent but split. |

---

## Summary
- Checks passed: 17 / 17 (2 carry MINOR residue)
- Checks failed: 0
- Critical issues: 0
- Depth probes satisfied: 5 / 5
- Source spot-checks (drift probe): 4 / 4 byte-accurate

## Confidence
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 1
- No padding: every source Read targeted a specific cited anchor (task-protocol L204–233; troubleshoot L41–72; troubleshoot L113–116; report-template L146–157). Each Read backs multiple table rows because depth checks are multi-claim per anchor-set.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | R1 §C (`diagnostic_backend:` insertion) | Research gives two insertion *points* and the trade-off, but does not spell out the literal *value/shape* of the `diagnostic_backend:` declaration line (e.g. `diagnostic_backend: troubleshoot` vs a multi-field block). Builder must invent the exact token. | Builder picks `diagnostic_backend: troubleshoot` (or agreed value) at authoring time; research is sufficient for placement, mildly short on the literal payload. Not blocking — a one-token decision. |
| 2 | MINOR | R3 §2 ↔ R4 (TFEP-consumer block field set) | The report-consumer block's field set (`remediation_target`, `tasklist_insertion_recommendation`, `safe_to_auto_insert`) is enumerated in R3, while R4 is declared owner of "exact field set / fencing" yet defers to R3 for the names. The authoritative field list is split across two files rather than consolidated in the declared owner. | Builder treats R3 §4 as the field-name source of truth and R4 as the fencing/mechanics source. Coherent as-is; no re-research needed. |
| 3 | MINOR | R2 §A2 / R3 §4 (dispatch flag translation) | The `--tier`/`--intent` → `--depth` translation is described as a *decision* the adapter must make (add pass-through flags OR drop+map), giving options rather than a single prescribed mapping. Means one item encodes a decision, not a mechanical edit. | Acceptable — research correctly surfaces it as an open design decision with both branches costed. Builder/author resolves per change-2 intent. Flag only. |

## Actions Taken
None — `fix_authorization: false` (report-only).

## Self-Audit
This is a research-depth qualitative review; no Inherited Structural Verdict was supplied in the spawn prompt — standalone behavior applies.

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict was provided; nothing relied upon. All depth findings verified by own tool engagement.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Donor field schema completeness (R2 §B3) — verified by Read of `sc-troubleshoot-protocol/SKILL.md:41-72`; all 30 fields + types match research table byte-for-byte.
- Report-template insertion anchor (R3 §2) — verified by Read of `refs/report-template.md:146-157`; `## Next Steps` at L146, `### Hard-stop variant` at L156, confirming "after L154 / before L156" anchor.
- Wave 0 flag-parse line (R2 §B1) — verified by Read of `sc-troubleshoot-protocol/SKILL.md:113-116`; L115 `Optional:` sentence matches verbatim.
- TFEP consumer/dispatch lines (R1 §B, R3 §1A) — verified by Read of `sc-task-protocol/SKILL.md:204-233`; L205/L212/L216/L225 dispatch + consumer fields match verbatim.

Self-audit answers:
1. Independently verified 4 source anchor-sets covering ~12 distinct cited claims.
2. Files read: the two SKILL.md (task-protocol + troubleshoot-protocol) and report-template.md in src/superclaude/ — the actual edit targets the research describes.
3. Not a 0-issue review: 3 MINOR issues surfaced. Trust is grounded in the 4 byte-accurate spot-checks and the probe-by-probe content audit, not assertion.
4. No web research performed — all verification was local-file-bound (correct for a research-depth lens). Tavily not invoked; no fallback needed.

## Recommendations
- PASS the research-depth gate. The corpus supplies content-level guidance for all five required builder capabilities (a)–(e).
- Builder should note the two MINOR residues at authoring time: (1) choose the literal `diagnostic_backend:` declaration value; (2) treat R3 §4 as the field-name source of truth for the report-consumer block. Neither requires re-research.
- Dispatch flag-translation (issue 3) is a genuine design decision the author resolves per change-2 intent — research correctly costed both branches.

## QA Complete

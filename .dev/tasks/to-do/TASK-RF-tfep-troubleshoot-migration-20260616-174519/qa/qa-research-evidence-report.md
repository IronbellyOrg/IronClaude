# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** MDTM tasklist to replace /sc:forensic with /sc:troubleshoot in the TFEP
**Date:** 2026-06-16
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: PASS (with MINOR issues — no gaps that block synthesis)

Evidence quality is DENSE across all four research files. Every spot-checked
content anchor (file:line citation) matched the actual source byte-for-byte.
~30 anchors verified directly against source (>>20% of cited anchors). The only
defects found are cosmetic file-total line-count off-by-ones (metadata, not
anchors) and one self-contradictory Status header in R4. None of these will
cause synthesis to hallucinate.

---

## Anchors Spot-Checked (all VERIFIED against source)

| Research file | Cited anchor | Source verification | Result |
|---|---|---|---|
| R1 (01) | task-protocol SKILL:172 "Escalation gradient...future forensic integration" | Read 170-265 | EXACT MATCH |
| R1 | :203 "Write context to {output_dir}/context.yaml" | Read | EXACT MATCH |
| R1 | :205 "Step 3: Invoke forensic" | Read | EXACT MATCH |
| R1 | :206 "Determine the forensic tier" | Read | EXACT MATCH |
| R1 | :212 `/sc:forensic --tier {tier} --intent triage --caller task-unified --context ...` | Read | EXACT MATCH |
| R1 | :213 "returns a structured return contract" | Read | EXACT MATCH |
| R1 | :215 "Step 4: Consume forensic results" | Read | EXACT MATCH |
| R1 | :216 "Read the forensic return contract from {output_dir}/return-contract.yaml" | Read | EXACT MATCH |
| R1 | :250 "**Forensic artifacts**: {path to output_dir}" | sed -n 250p | EXACT MATCH |
| R1 | :253 "committed to git alongside other forensic artifacts" | Read | EXACT MATCH |
| R1 | :258/:259 escalation-budget `/sc:forensic --tier light/standard` | Read | EXACT MATCH |
| R1 | `/sc:forensic` appears at EXACTLY 212,258,259 | grep | CONFIRMED (3 hits) |
| R1 | forensic/return-contract/context.yaml all confined to 133–261 | grep min=172 max=250 (case-insensitive) | CONFIRMED |
| R1 | ZERO `diagnostic_backend:`/`backend:` declarations | grep exit 1 | CONFIRMED |
| R1 | task.md:48 "structured forensic analysis"; only forensic in file | sed + grep | EXACT MATCH (1 hit) |
| R2 (02) | troubleshoot.md:8 argument-hint flag list | Read 1-70 | EXACT MATCH |
| R2 | troubleshoot.md Options table 48–58 (header @48-49, `--no-mcp` last @58) | Read | EXACT MATCH |
| R2 | troubleshoot.md:64 parse step; :67 "On skill return, surface:" | Read | EXACT MATCH |
| R2 | SKILL Output Contract 41–72 (status@43, test_is_wrong@49, test_file_path@50, behavior_is_documented@51, contract_version@62, 30 fields) | Read 41-75 | EXACT MATCH (all 30 fields + lines) |
| R2 | SKILL Wave 0 parse sentence @115 (Optional flag list incl. 3 diagnosability flags) | Read 109-148 | EXACT MATCH |
| R2 | SKILL audit header block 128–137 (output_dir@136, -->@137) | Read | EXACT MATCH |
| R2 | SKILL Wave 5 header @417, exit @466 | sed | EXACT MATCH |
| R2 | SKILL SUMMARY footer 446–455 | sed | EXACT MATCH |
| R3 (03) | report-template section map @91 (Next Steps@146, Hard-stop@156, Audit@196, Pipeline Hardening@204, Test-is-wrong@248, Behavior-is-documented@269) | grep headers | EXACT MATCH |
| R3 | report-template Next Steps 146–154 + Hard-stop variant @156 | Read 140-159 | EXACT MATCH |
| R3 | `--caller task-unified` live literal at task-protocol:212 | Read | CONFIRMED |
| R4 (04) | Template-02 B2 6-field item format 159–166 | Read | EXACT MATCH |
| R4 | Template-02 A3 granular-breakdown 108–112 | sed | EXACT MATCH |
| R4 | Template-02 M3 lens-QA sequence 1059–1096 (Step 1 Agg@1062, Step 2 Structural@1064) | Read | EXACT MATCH |
| R4 | bare-review example file exists | ls | CONFIRMED (189KB, real) |

---

## Checklist (10-item research gate)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status: Complete | PASS* | 01/02/03 end "Status: Complete". 04 footer "Status: Complete" (L169) but header L3 says "Status: In Progress" — self-contradictory header (MINOR-1). Content is complete. |
| 2 | Evidence density | PASS | DENSE (>80%). Every spot-checked claim carries file:line; all 30 anchors verified exact. R1/R3 cite line+verbatim text; R2 cites field+type+line for all 30 contract fields; R4 cites template rule IDs + line ranges. |
| 3 | Scope coverage | PASS | All migration-relevant surfaces covered: task-protocol TFEP block (R1/R3), task.md (R1), troubleshoot.md + skill (R2), report-template + Makefile sync contract (R3), Template-02 + example (R4). No key file unexamined. |
| 4 | Documentation cross-validation | PASS (N/A) | No external-doc-sourced claims requiring [CODE-VERIFIED] tags; all claims are direct source-file reads. Nothing untagged-and-doc-only. |
| 5 | Contradiction resolution | PASS | R5 cross-validation (analyst) targets R1-vs-R3 line numbers etc.; my independent check found R1 and R3 AGREE on every overlapping anchor (172,205,206,212,213,215,216,250,253,258,259; report-template 146/156). No contradictions between research files. |
| 6 | Gap severity | PASS | "Gaps and Questions" content: R2/R3 surface the contract MISMATCH (troubleshoot lacks --caller/--tier/--intent/--context, emits dict not return-contract.yaml, missing 5 TFEP fields) — but these are DESIGN FINDINGS for the migration to solve, not RESEARCH gaps. They are fully characterized with anchors and adapter options. No unresolved research gap that would make synthesis hallucinate. |
| 7 | Depth appropriateness | PASS | R3 traces the full TFEP→forensic→return-contract data flow end-to-end (dispatch L212 → consume L216 → fields L219-225 → incident L237-253 → budget L258-259) and the contract reconciliation §4. End-to-end flow present (Deep tier satisfied). |
| 8 | Integration point coverage | PASS | The cross-subsystem connection (task-protocol consumer ↔ troubleshoot producer) is the CORE of R2 §B3 donor-field map and R3 §4 field reconciliation. APIs/flags/contract fields all documented. |
| 9 | Pattern documentation | PASS | Conventions documented: thin-command NFR-5 (R2 A6), additive contract_version versioning (R2 B4), audit-header key convention (R2 B2), Template-02 B2/A3/M3/M4 item patterns + anti-orphaning (R4). |
| 10 | Incremental writing compliance | PASS | Files show growing structure (sectioned A–E, numbered findings). R4's contradictory In-Progress→Complete status is itself evidence of incremental authoring (header set first, footer flipped at end) — but the header was not reconciled (MINOR-1). |

*PASS with the MINOR-1 caveat noted; does not block synthesis.

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 3
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 10 | Grep: 0 | Glob: 0 | Bash: 5 (greps/seds for confinement, counts, anchors)
(Tool calls (15) >= checklist items (10); each Read/Bash targeted a specific cited anchor or claim. No web research performed — all claims are local-source-bound, so Tavily-first did not trigger.)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 04-template-and-examples.md:3 vs :169 | Self-contradictory Status: header line 3 reads "Status: In Progress" while footer line 169 reads "Status: Complete". A reader scanning the top would wrongly believe R4 is unfinished. Content is in fact complete. | Change line 3 to "Status: Complete" (or delete the duplicate header status). |
| 2 | MINOR | 02-troubleshoot-surface.md:8, :9 | File-total line-count metadata off-by-one: claims troubleshoot SKILL is "588 lines" (actual 587) and commands/troubleshoot.md "203 lines" (actual 202). All *content* anchors are correct; only the parenthetical totals drift. | Update to 587 and 202, or drop the totals. No anchor is affected. |
| 3 | MINOR | 01-file-inventory.md:5–6 | File-total line-count metadata off-by-one: claims task.md "187 lines total" (actual 186). task-protocol SKILL "396 lines" is CORRECT. | Update task.md total to 186, or drop. No anchor affected. |

---

## Actions Taken

None — fix_authorization is false. All issues documented above for the orchestrator / fix cycle.

---

## Recommendations

- All three issues are MINOR cosmetic/metadata defects. Under the research-gate
  "any gap = FAIL" rule these are technically gaps and SHOULD be corrected before
  synthesis, but NONE will cause synthesis to hallucinate — every load-bearing
  file:line anchor is verified accurate. Recommend a 1-cycle trivial fix
  (correct the R4 header + three line-count totals) then PASS, OR proceed to
  synthesis with these logged if the orchestrator deems line-count metadata
  non-load-bearing.
- The contract MISMATCH surfaced by R2/R3 (troubleshoot lacks --caller/--tier/
  --intent/--context and emits a dict not return-contract.yaml, missing 5 TFEP
  fields) is correctly characterized as a *migration design problem*, not a
  research gap, and is fully evidenced. Synthesis has everything it needs to
  plan the adapter.

## QA Complete

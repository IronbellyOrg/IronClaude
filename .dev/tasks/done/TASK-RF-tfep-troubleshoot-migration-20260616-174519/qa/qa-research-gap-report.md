# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** TFEP migration — replace /sc:forensic with /sc:troubleshoot
**Date:** 2026-06-16
**Phase:** research-gate
**Lens:** gap-detection (adversarial — assume surfaces were missed)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

Research is substantively strong, well-anchored, and cross-validated — the four files
collectively cover the rename worklist, the contract mismatch, the sync/verification
contract, and the template mechanics with file:line precision that I independently
re-verified against source. However, this is a **research GATE** and the gate rule is
zero-tolerance: ANY gap of ANY severity = FAIL. I found **3 gaps** (1 IMPORTANT, 2 MINOR)
plus one open decision that the research itself flags as deliberately deferred to the
builder/user. All must be closed (or explicitly accepted by the user as Open Questions
encoded in the tasklist) before synthesis/build proceeds.

The single most consequential finding: the research **resolves the step-4 remediation /
adapter-ownership decision with a recommendation but leaves the recommendation in tension
across two files**, and it does NOT pin down whether `commands/task.md:48` ("structured
forensic analysis") is in the rename worklist as an EDIT or merely noted — see G1.

---

## Lens-Focus Findings (the six questions in the spawn prompt)

### (a) Is there a surface the 8 steps touch that no research file anchored?

**Mostly covered — one partial gap (G2).** I cross-walked the 8 migration changes against
the research anchors:

| Change | Surface | Anchored by | Verified |
|---|---|---|---|
| #1 terminology rename ("forensic"→neutral) | SKILL.md 172,205,206,213,215,216,250,253 | R1 §B, R3 §1A | YES (rg confirms 8 bare "forensic" + 3 `/sc:forensic`) |
| #2 return-contract adapter | troubleshoot SKILL 41–72, 417–466; report-template | R2 §B3/B5, R3 §4 | YES |
| #3 `--context`/`--caller` ingestion | troubleshoot.md 8,48–58,64,67; SKILL 115,128–137 | R2 §A/B1/B2 | YES (flags confirmed ABSENT today) |
| #4 remediation ownership | SKILL.md Step4 215–222 + Step5 224–229 | R1 §C, R3 §4 | YES (see G1 — recommendation tension) |
| #5 consume troubleshoot output | SKILL.md 216,225; context.yaml 203 | R1 §B, R3 §4 | YES |
| #6 preserve freeze semantics | SKILL.md 185–188 | R1 §C | YES |
| #7 incident reporting | SKILL.md 237–253 (incl. rca-verdict.md/solution-verdict.md refs) | R1 §C, R3 §4.5 | YES |
| #8 escalation budget | SKILL.md 255–261 | R1 §C, R3 §4.4 | YES |

**Partial gap (G2):** Change #7's incident-report template (SKILL.md 245–246) pulls
`{summary from rca-verdict.md}` and `{summary from solution-verdict.md}` — these are
**forensic-pipeline artifact filenames that do not exist in the troubleshoot world**
(troubleshoot emits `REPORT.md` + hypothesis cards + `audit.log`). R3 §4.5 *names* this
mismatch ("must be re-sourced from troubleshoot's artifacts") but **no research file pins
the concrete replacement source** for `rca-verdict.md`→? and `solution-verdict.md`→? the
way R2 §B3 painstakingly maps the return-contract fields. The builder is left to infer
that Root cause ← REPORT.md Diagnosis (line 429) and Solution ← Proposed Fix (line 431),
which R2 establishes elsewhere but R3 does not bind to these two specific template
placeholders. Severity: MINOR (inference is short, sources exist), but it is an
un-pinned anchor on a surface the 8 steps touch.

### (b) Is `.claude/` sync-dev verification covered for EVERY edited file?

**YES — fully covered, this is a strength.** The edited-file set is:
`sc-task-protocol/SKILL.md`, `sc-troubleshoot-protocol/SKILL.md`, `commands/troubleshoot.md`,
`commands/task.md`, `sc-troubleshoot-protocol/refs/report-template.md`.

R3 §3 verifies the Makefile `sync-dev` target (L109–163) copies **skills (incl. `refs/`)**,
**commands**, and confirms each of the five files lands in the copy loop:
- skills loop covers `sc-task-protocol/` and `sc-troubleshoot-protocol/` incl.
  `refs/report-template.md` (R3 §3 "recursive file copy incl. `refs/`").
- commands loop covers `troubleshoot.md` AND `task.md` (`src/superclaude/commands/*.md`).

`verify-sync` (L166+) gate + the CLAUDE.md never-stage-`.claude/` ABSOLUTE RULE are both
captured (R3 §3, §5). R3 §5 gives the per-edit gate "`make sync-dev` → `make verify-sync`
(exit 0)". **No edited file is missing a sync path.** Confirmed adequate.

### (c) Is the step-4 remediation-ownership decision resolved with a concrete, encodable recommendation?

**PARTIALLY — recommendation exists but is in tension across files (G1, IMPORTANT).**
research-notes.md AMBIGUITIES #2 + GAPS_AND_QUESTIONS recommend **option 1: "troubleshoot
authors `return-contract.yaml` when `--caller task-unified`"** and says "the tasklist
should encode option 1 but flag the decision in Open Questions." R2 §B5 concretely places
this as a new Wave-5 step 4.5 (emit-when-caller=task-unified) — consistent with option 1.

BUT R3 §4 gap #2 frames it as an UNRESOLVED either/or: "(a) make troubleshoot write that
file, OR (b) rewrite task-protocol Step 4 to read troubleshoot's dict/`REPORT.md`" — and
does NOT pick (a). So one researcher (R2 + notes) recommends a concrete owner; another (R3)
re-opens it as a live binary choice. The builder reading R3 in isolation would NOT know the
decision was already made. This is a **resolvable-but-currently-dangling** decision: the
recommendation is encodable, but the research is internally inconsistent about whether it IS
resolved. Severity: IMPORTANT (this is the load-bearing architectural decision of the whole
migration; an ambiguous handoff risks the builder encoding option (b) and inverting ownership).

### (d) Is the "diagnostic_backend" terminology-neutral rename approach concretely placed?

**YES — concretely placed with two ranked candidate anchors (strength).** R1 §C
("`diagnostic_backend:` clean insertion point") confirms via grep that NO `diagnostic_backend:`/
`backend:` declaration exists today (I independently re-verified: zero hits), and offers two
placements: **section-top ~line 136 (single source of truth, recommended)** vs **Step-3-adjacent
~line 204 (lower blast radius)**. The recommendation is explicit and encodable. The
terminology-neutral GOAL is stated in research-notes PATTERNS ("rename 'forensic' →
'diagnostic escalation' and add `diagnostic_backend: troubleshoot'"). Adequate.

*Minor note (rolled into G3):* the prose "diagnostic escalation" rename target for the 8 bare
"forensic" tokens is stated as a goal but no file gives the **exact replacement string per
token** (e.g. does line 172 "for future forensic integration" become "for future diagnostic
integration" or "for future troubleshoot-backend integration"?). The worklist enumerates the
tokens (R1 §B) but not their target text — left to the builder.

### (e) Is there a verification that `rg /sc:forensic` returns only intentional historical refs after the rename?

**YES — explicitly specified (strength).** R3 §1 provides the exact verification token
(`rg -n '/sc:forensic|--caller task-unified|return-contract\.yaml' src/superclaude/
--glob '!**/archive/**'` → expect 0 live hits) AND a residual-reference sweep that
separates LIVE (§1A) from HISTORICAL (§1C incidental prose, §1D swarm-CLI / sc-forensic-qa /
task-unified docs) so the post-rename check won't false-positive on intentional historical
refs. research-notes VALIDATION_REQUIREMENTS restates it. I re-ran the live sweep: exactly
3 `/sc:forensic` hits, all in sc-task-protocol/SKILL.md (212,258,259) — matches R3 §1A
exactly. The historical/live partition is the right design for this gate. Adequate.

### (f) Is `commands/task.md:48` ("structured forensic analysis") in the rename worklist?

**IDENTIFIED but ownership/action is ambiguous (folds into G1/G3).** R1 §D pins line 48
verbatim and states "The only 'forensic' string in task.md is on line 48." So the surface
is anchored. HOWEVER R1 labels the task.md Boundaries lines (175/176/186) and Activation
(161) as "context, not necessarily edits" and does not definitively state whether line 48's
"structured forensic analysis" phrase should be **edited** (to neutral language) or **left**
(since it's describing the TFEP behavior generically, which arguably survives the backend
swap). research-notes GAPS_AND_QUESTIONS asks "Whether `commands/task.md` Boundaries list
and any other doc surface also name `/sc:forensic` and need updating (R3 to sweep)" — and
R3's sweep covered `/sc:forensic` (none in task.md) but did NOT explicitly rule on the bare
"forensic" adjective at line 48. **Net: the line is anchored, but whether it is an EDIT
target is unresolved.** Given the migration's terminology-neutral goal, line 48 most likely
SHOULD be edited ("structured forensic analysis" → "structured diagnostic analysis"), but no
research file commits to that. Severity: MINOR (single phrase, low blast radius) but it is a
genuine dangling action-vs-noaction decision on an in-scope surface.

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 4 research files present. 01/02/03 = Status Complete. **04 has split status** ("In Progress" L3, "Complete" L169) — VERIFIED contradiction; content is complete but the header is stale (rolled into G3). research-notes.md present + Status: Complete. |
| 2 | Evidence density | PASS (Dense) | Re-verified spot anchors via Read/Bash: SKILL.md 205–261, task.md 44–48/161/175/176/186, troubleshoot.md 8/48–58, report-template 146–156, troubleshoot SKILL 41–45/115. Every claim I checked carries file:line and matched source. >80% evidenced. |
| 3 | Scope coverage | PASS | All 5 edit-target files (CLAUDE.md scope list) discussed: sc-task-protocol/SKILL.md (R1/R3), task.md (R1), troubleshoot.md (R2), troubleshoot SKILL (R2/R3), report-template (R3/R4). Makefile sync targets (R3). |
| 4 | Documentation cross-validation | PASS | No doc-sourced architectural claims requiring CODE-VERIFIED tags; research is itself code-traced against src/. The historical/live partition (R3 §1C/§1D) is the doc-claim discipline here and is sound. |
| 5 | Contradiction resolution | FAIL | **G1**: R2+notes recommend option-1 (troubleshoot authors return-contract) vs R3 §4 re-opens it as unresolved (a)/(b). Unreconciled cross-file contradiction on the load-bearing ownership decision. |
| 6 | Gap severity | FAIL | research-notes GAPS_AND_QUESTIONS + AMBIGUITIES list live open items (adapter ownership, inline vs refs/tfep.md, task.md surface sweep). Gates require ALL gaps resolved. G1/G2/G3 enumerated below. |
| 7 | Depth appropriateness (Standard) | PASS | Standard tier → file-level coverage required. R1–R4 give file-level + line-level anchors; R3 §4 traces the adapter contract end-to-end (consumer fields → producer gaps). Exceeds Standard floor. |
| 8 | Integration point coverage | PASS | The integration IS the migration. R2 §B3/B5 + R3 §4 document the task-protocol↔troubleshoot contract bridge (flags, return-contract emission, field mapping) concretely. |
| 9 | Pattern documentation | PASS | Conventions documented: thin-command/skill split (R2 §A5/NFR-5), flag-table format, Output-Contract additive-versioning (R2 §B4), SoT discipline (all), MDTM B2/A3/M3/anti-orphaning (R4 §A). |
| 10 | Incremental writing compliance | PASS (with note) | 01/02/03 show iterative structure (worklists, mapping tables grown section-by-section). 04's split status header is itself weak evidence of incremental writing that wasn't finalized — not a data-loss signal, but the stale header (G3) should be fixed. |

---

## Summary

- Checks passed: 8 / 10
- Checks failed: 2 (items 5 contradiction, 6 gap-severity)
- Critical issues: 0
- Important issues: 1 (G1)
- Minor issues: 2 (G2, G3)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| G1 | IMPORTANT | research-notes AMBIGUITIES#2 / R2 §B5 vs R3 §4 gap#2 | Adapter/remediation OWNERSHIP (step 4) is recommended as option-1 (troubleshoot authors `return-contract.yaml`) in notes+R2, but R3 §4 re-presents it as an unresolved binary (a)/(b) without picking. Cross-file contradiction on the migration's load-bearing decision. A builder reading R3 alone would not know it was decided. | Reconcile: state ONE authoritative recommendation (option-1) in a single place the builder will read, and explicitly mark R3's (a)/(b) as "RESOLVED → (a) per notes AMBIGUITIES#2; encode (a), flag in Open Questions for user override." OR escalate to user to confirm ownership before build. |
| G2 | MINOR | sc-task-protocol/SKILL.md 245–246 (change #7) | Incident-report template placeholders `{summary from rca-verdict.md}` / `{summary from solution-verdict.md}` reference forensic-pipeline artifact filenames that troubleshoot does not produce. R3 §4.5 flags the mismatch but does not bind concrete replacement sources to these two specific placeholders. | Pin the re-source mapping: `rca-verdict.md` → REPORT.md Diagnosis (troubleshoot SKILL line 429); `solution-verdict.md` → REPORT.md Proposed Fix (line 431). Add this binding to research (or have builder encode it as a Change-#7 item with these exact sources). |
| G3 | MINOR | research/04-template-and-examples.md L3 vs L169; + task.md:48 action ambiguity; + per-token rename target text | (a) File 04 header says "Status: In Progress" (L3) but footer says "Status: Complete" (L169) — stale/contradictory completeness marker. (b) task.md:48 "structured forensic analysis" is anchored but no file commits to whether it is an EDIT target. (c) The 8 bare "forensic" tokens have no per-token target replacement string. | (a) Fix 04's L3 to "Status: Complete." (b) Add an explicit ruling: task.md:48 IS / IS NOT a rename target (recommend IS, → "structured diagnostic analysis"). (c) Specify the neutral replacement convention (e.g. "forensic"→"diagnostic"/"diagnostic escalation") so the builder isn't inventing prose per token. |

## Recommendations

1. **Resolve G1 before build (blocking).** This is the architectural keystone. Either reconcile the
   research to a single authoritative option-1 recommendation, or surface the ownership decision to the
   user as an explicit Open Question the tasklist must answer before the adapter items are written.
2. **Pin G2's two artifact re-source mappings** so Change #7 isn't builder-invented.
3. **Fix G3's stale 04 header + commit a task.md:48 edit/no-edit ruling + a per-token rename convention.**
4. The research is otherwise build-ready: rename worklist (R1), contract bridge (R2/R3 §4), sync gate
   (R3 §3), residual-ref verification (R3 §1), and MDTM conformance (R4) are all concrete and verified.
   Closing G1–G3 (or accepting them as encoded Open Questions) flips this to PASS.

---

## Confidence Gate

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 10 checklist items were checked with tool evidence. "Confidence 100%" reflects checklist
COVERAGE, not that the research is gap-free — it is not; 2 checks legitimately FAILED on found gaps.)

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 4 (rg/sed/wc/grep inside Bash)
(Read: research-notes + 4 research files + 1 report re-read. Bash: forensic sweep, TFEP block dump,
report-template/contract verification, anchor cross-checks. Tool calls (9 distinct verification
batches) ≥ 10 checklist items via multi-target Bash — each call mapped to specific anchor verification,
no padding. No web research performed; no Tavily/fallback needed (all claims source-truth-local).)

- UNCHECKED items: none.
- UNVERIFIABLE items: none.

## QA Complete

VERDICT: FAIL — 3 gaps (1 IMPORTANT G1 adapter-ownership contradiction, 2 MINOR G2/G3). Zero-tolerance
research gate: all gaps must be resolved or encoded as accepted Open Questions before synthesis/build.

# PG.A Verification Inventory — refs/diagnosability-audit.md

Captured: 2026-05-29 17:15

## Line count

340 lines total.

## Heading structure (grep -nE '^# |^## |^### ')

```
1:# Diagnosability Audit Rules                                  ← H1
9:## Section 1: Auggie query templates per branch
13:### Branch A — Log-Call Inspection
29:### Branch B — Log-Config Inspection
47:## Section 2: Fallback paths (auggie unavailable)
51:### Branch A fallback
65:### Branch B fallback
78:## Section 3: Structured-output schemas per branch
82:### Branch A schema
99:### Branch B schema
120:## Section 4: Sufficiency rubric + 3-W's synthesis
124:### 3-W's coverage scoring
134:### Sufficiency rubric (applied in order; first match wins)
152:### Behavior under degradation
163:## Section 5: Complexity gate
167:### Signal table (extracted at Wave 1.6 entry)
179:### Classification rule
184:### Examples
192:## Section 6: Diagnosability Context Card template
   (197-233: in-fence headings inside the markdown-fenced card template — expected)
238:## Section 7: Tasklist generation rules + hard constraints
242:### Hard constraints (non-negotiable)
249:### High-specificity per-line task format
258:### Worked tasklist skeleton
   (261-282: in-fence headings inside the markdown-fenced skeleton — expected)
282:### Patch-round counter
288:## Section 8: T4 worked example — what the audit saves
292:### Inputs
297:### Branch A findings
301:### Branch B findings
305:### Synthesis
315:### Verdict + complexity
322:### Tasklist emitted
332:### What was saved
338:## Loading discipline                                          ← terminal un-numbered
```

## Provenance comment count

`grep -c '<!-- Source:'` → `0` ✓ (PASS — no brainstorm-artifact comments propagated)

## Section-by-section presence checklist

| Section | Status | Notes |
|---------|--------|-------|
| Section 1: Auggie query templates per branch (A + B) | ✓ Present | L9-46. Branch A at L13; Branch B at L29. Both placeholders `<failing_component>`, `<scope>`, `<symptom>` named in the lead-in (L11). Fenced code blocks with NO language tag (twin pattern). |
| Section 2: Fallback paths (Glob/Grep per branch) | ✓ Present | L47-77. Branch A fallback (L51) has 7 grep lines verbatim. Branch B fallback (L65) has 4 find/grep lines verbatim. Both have the `degraded: true` rule line. |
| Section 3: Structured-output schemas per branch | ✓ Present | L78-118. Branch A schema (L82, `json` language tag) verbatim from merged-output §2:109-119 incl. `captured_bytes` field. Branch B schema (L99, `json` language tag) includes `reachability_verdicts` array with `{reaches_sink, filtered_out, unknown}` enum. |
| Section 4: Sufficiency rubric + 3-W's synthesis | ✓ Present | L120-161. 3-W's coverage scoring table (L124-130) verbatim from merged-output §2:154-160. Sufficiency rubric table (L134-150) has all 13 rows S1-S13 verbatim from merged-output §3:171-185 — INCLUDING S1 stack-trace short-circuit, S5 captured-bytes rule, S11 auggie+fallback empty, S12 not-localizable, S13 intermittent-with-no-trace short-circuit. Behavior-under-degradation table (L152-159) verbatim from merged-output §3:200-205. Verdict vocabulary `{sufficient, partial, insufficient, unknown}` consistent throughout. |
| Section 5: Complexity gate (signal table + classification rule) | ✓ Present | L163-189. Signal table (L167-177) has all 7 signal rows verbatim from merged-output §4:215-225 incl. the `**Always non-trivial (override)**` security row. Classification rule (L179) Score 0-1 → trivial; Score 2+ OR `--type security` → non-trivial. Examples (L184) include the trivial and non-trivial sets. |
| Section 6: Diagnosability Context Card template | ✓ Present | L192-235. Single fenced markdown block (`markdown` language tag) with all required fields: Issue, failing_component, Verdict, Complexity, Hard-stop fired, Round, Captured bytes, 3-W's coverage table, Branch A inventory, Branch B reachability, Sufficiency rubric application, Implication for diagnosis confidence (bounded ≤6 lines per template), Tasklist reference. |
| Section 7: Tasklist generation rules + hard constraints | ✓ Present | L238-286. All 4 HARD CONSTRAINTS verbatim from merged-output §6:265-273 (1: Invocation-site-only; 2: Additive only; 3: Reversible; 4: Revert annotation). High-specificity per-line format described. Worked skeleton (L258) shows the 5-task structure. Patch-round counter section (L282) describes the per-defect counter at `<output-dir>/diagnosability-rounds.json`, 3-round cap, `--reset-diagnosability-rounds`. |
| Section 8: T4 worked example | ✓ Present | L288-336. Inputs (Wave 0 issue, Wave 1 observation). Branch A findings (one logger.info, one bare except, captured_bytes=4096). Branch B findings (LOG_LEVEL=INFO, reaches_sink). Synthesis (when=partial, where=partial, why=no; S13 fires). Verdict + complexity (insufficient, non-trivial score 3, hard-stop fires). Tasklist emitted (5-task skeleton: DEBUG env, fixture wrapper, strace, Sentry breadcrumb, CI artifact upload). What was saved (instrumentation-first vs blind Tier 2). |
| Terminal `## Loading discipline` (un-numbered) | ✓ Present | L338 — un-numbered, single paragraph. Enumerates Sections 1-8 as the on-entry read set; states the file is not re-read during the wave. Matches doc-discovery.md L180-182 pattern. |

## H1/H2/H3 hierarchy check

Top-level H1: `# Diagnosability Audit Rules` (single, at L1) — matches twin's single-H1 convention.

H2 hierarchy: All `## Section N: <imperative>` (Sections 1-8) plus terminal `## Loading discipline` (un-numbered) — matches twin pattern exactly.

H3 hierarchy: Branch A / Branch B sub-headings under Sections 1-3 (twin pattern); `### 3-W's coverage scoring`, `### Sufficiency rubric ...`, `### Behavior under degradation` under Section 4; `### Signal table ...`, `### Classification rule`, `### Examples` under Section 5; `### Hard constraints (non-negotiable)`, `### High-specificity per-line task format`, `### Worked tasklist skeleton`, `### Patch-round counter` under Section 7; `### Inputs`, `### Branch A findings`, `### Branch B findings`, `### Synthesis`, `### Verdict + complexity`, `### Tasklist emitted`, `### What was saved` under Section 8. All H3s sit under H2 parents — no orphan H3.

In-fence H1/H2 headings (the `# Diagnosability Context Card`, `## 3-W's coverage`, `# Diagnosability Tasklist`, `## Hard Constraints`, `## Implementation tasks`, etc. at L197-233 and L261-282) are EXPECTED: they are inside fenced markdown code blocks (` ```markdown ` opens at L196 and L260; ` ``` ` closes at L234 and L286) and represent the templates rendered into the runtime artifacts (`diagnosability-context.md` and `diagnosability-tasklist.md`), not document-level headings of this ref. The grep above lists them because grep does not distinguish fenced vs free text — but they're inside fences and do not break the H1/H2/H3 hierarchy of the ref file itself.

## Verdict

All 8 numbered sections + terminal Loading discipline present. Zero propagated `<!-- Source: ... -->` provenance comments. Verdict vocabulary consistent. Hard constraints verbatim. Sufficiency rubric verbatim (all 13 rows). Complexity gate signal table verbatim (all 7 rows + override).

Ready for PG.A rf-qa adversarial verification.

# QA Report — Internal Consistency (TFEP forensic→troubleshoot rename, Phase 2)

**Topic:** TFEP §4.5 diagnostic-backend rename internal-consistency lens
**Date:** 2026-06-16
**Phase:** task-integrity (internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Target:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 (lines 133–263)

---

## Overall Verdict: FAIL

One Phase-2-targeted half-renamed term survives that directly contradicts the new
`**Diagnostic backend:** troubleshoot` declaration, plus a content contradiction the rename
introduced between Step 3's depth declaration and the invocation string. Details below.

## Deferral Baseline (from spawn prompt — these are EXPECTED, NOT flagged)

The following `forensic`/`/sc:forensic` occurrences are explicitly deferred to Phases 5/6 and were
confirmed present-but-tolerated by reading each line:

| Line | Text (verbatim) | Deferral basis |
|------|-----------------|----------------|
| 214 | `6. Invoke: /sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick` | invocation string at Step 3 |
| 218 | `8. Read the forensic return contract from {output_dir}/return-contract.yaml.` | `forensic return contract` read line at Step 4 |
| 249 | `- **Root cause**: {summary from rca-verdict.md}` | rca-verdict.md incident source |
| 250 | `- **Solution**: {summary from solution-verdict.md}` | solution-verdict.md incident source |
| 260 | `1st TFEP trigger  → /sc:forensic --tier light --intent triage` | Escalation Budget `/sc:forensic --tier` line |
| 261 | `2nd TFEP trigger  → /sc:forensic --tier standard` | Escalation Budget `/sc:forensic --tier` line |

All six were verified to match the deferral description exactly. They are excluded from findings.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | "diagnostic escalation" / "diagnostic depth" / "diagnostic escalation backend" / "Diagnostic artifacts" used coherently | FAIL | The verified-coherent terms read fine: line 207 "Invoke diagnostic escalation", 208 "diagnostic depth", 252 "Diagnostic artifacts", 255 "diagnostic artifacts", 174 "diagnostic-backend escalation". Line 215 "diagnostic escalation backend" is the outlier — see Finding 1. |
| 2 | New `**Diagnostic backend:** troubleshoot` (line 137) does not contradict surviving prose | FAIL | Line 137 declares backend = `troubleshoot` and that "swapping the backend changes only this declaration and the invocation string." Line 208 + 210/211 describe tier knobs coherently, BUT line 214 (deferred) carries `--depth quick` while line 208 says depth is "based on escalation count" and lines 210-211 vary only `--tier`/`--intent`, never `--depth`. See Finding 2 — this contradiction is independent of the backend name. |
| 3 | No half-renamed sentence mixes "forensic" + "diagnostic" (excluding the 6 deferred) | FAIL | Line 215 `The diagnostic escalation backend runs autonomously…` is the renamed prose pair of the deferred line-214 forensic invocation, but it is never reconciled with line 137's `troubleshoot` name. See Finding 1. |
| 4 | Cross-references between Steps 3/4/5/6 resolve after heading renames | PASS | line 222 "Proceed to Step 5 (tasklist insertion)" → Step 5 heading line 226 "Tasklist insertion" resolves; line 223 "return to Step 3" → line 207 exists; line 237 "return to Step 2" → line 192 exists; step ordering 1(187)→2(192)→3(207)→4(217)→5(226)→6(233) is contiguous. No dangling reference. |
| 5 | Section heading (#### block) renames don't strand internal references | PASS | Headings 139/155/166/183/239/257 carry intact naming; no in-body cross-ref points to a renamed-away heading. |
| 6 | `escalation_count` / trigger numbering consistent (1,2,3) across line 203, lines 210-212, lines 260-262 | PASS | 1st/2nd/3rd mapping identical in all three locations (light+triage / standard / FULL STOP). |
| 7 | "Diagnostic artifacts" (252) vs "diagnostic artifacts" (255) | PASS | Both refer to `output_dir` contents; capitalization differs only by field-label vs mid-sentence position. Coherent. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | SKILL.md line 215 | `7. The diagnostic escalation backend runs autonomously through all its phases and returns a structured return contract.` — The line 137 declaration promises that swapping the backend "changes only this declaration and the invocation string." Line 215 is NEITHER the declaration nor the invocation string, yet it describes the backend's runtime behavior with the renamed noun "diagnostic escalation backend" while leaving it unreconciled with the `troubleshoot` name. A reader cannot tell whether "diagnostic escalation backend" = the `troubleshoot` skill named in line 137 or the still-forensic invocation on line 214. This is the rename left half-done: the noun was changed to the diagnostic-family term but the sentence still narrates the forensic flow (line 214 pair) without binding to `troubleshoot`. | Either (a) make line 215 backend-neutral so it cannot collide with line 137's "only declaration + invocation string change" promise (e.g., "The diagnostic backend runs autonomously…"), OR (b) state explicitly that "diagnostic escalation backend" refers to the backend declared at line 137. Phase-2 should not leave a backend-naming noun floating. |
| 2 | IMPORTANT | SKILL.md line 208 vs line 214 | Line 208 instructs `5. Determine the diagnostic depth based on escalation count:` and lines 210-211 then vary ONLY `--tier`/`--intent` per escalation count (`--tier light --intent triage`; `--tier standard`) — `--depth` is never among the per-count knobs. But the invocation template on line 214 hardcodes `--depth quick` for every escalation count. "Determine the diagnostic depth based on escalation count" is contradicted by a constant `--depth quick`. The §4.5 frontmatter rename ("diagnostic depth") surfaced this latent inconsistency: the renamed prose now explicitly promises depth varies with count, but the command does not vary it. | Reconcile: either make line 214's depth a `{depth}` placeholder driven by the per-count table (and add a depth value to each bullet on lines 210-211), OR change line 208's prose to "Determine the diagnostic **tier**/intent based on escalation count" so it stops promising a per-count depth that the command does not deliver. |
| 3 | MINOR | SKILL.md line 174 vs line 137 | `**Escalation gradient (within-TFEP, for diagnostic-backend escalation):**` uses "diagnostic-backend escalation" coherently with the new term, but the gradient bullets (lines 176-181: "escalate from light to standard", "Second failed retest → escalate") describe the SAME light→standard tier ladder as Step 3 lines 210-211 and the Escalation Budget lines 260-262. This is not a rename inconsistency, but the three ladders are stated three times with no cross-reference, raising future drift risk after the Phase-5/6 forensic→troubleshoot invocation rename lands. | Optional (out of Phase-2 rename scope): add a cross-reference from line 174's gradient to the Escalation Budget block so the two tier ladders cannot drift independently when the deferred forensic lines are renamed. Documented for the Phase 5/6 owner; not a Phase-2 blocker on its own. |

## Summary
- Checks passed: 4 / 7
- Checks failed: 3
- Critical issues: 0
- Important issues: 2 (Findings 1, 2)
- Minor issues: 1 (Finding 3)
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Actions Taken
None — `fix_authorization: false`. All findings are report-only. No file was modified.

## Recommendations
1. Resolve Finding 1 before Phase 2 is marked complete: line 215's "diagnostic escalation backend" must either be backend-neutral or explicitly bound to the line 137 `troubleshoot` declaration. As written it violates line 137's own "only declaration + invocation string changes" promise.
2. Resolve Finding 2 before Phase 2 is marked complete: the line 208 "diagnostic depth … based on escalation count" prose and the line 214 hardcoded `--depth quick` cannot both be true. Pick one direction.
3. Hand Finding 3 to the Phase 5/6 owner as a drift-prevention note when the deferred forensic invocation lines are renamed.

## Confidence
**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 2 | Glob: 0 | Bash: 2

All 7 checklist items were verified with direct tool evidence (Read of lines 120-279 of the target,
Grep of all forensic/diagnostic/verdict terms with line numbers, Bash heading enumeration). Tool
call count (Read 3 + Grep 2 + Bash 2 = 7) meets the per-item minimum for 7 checks. No web research
was required (no external/URL-bound claims in this section). No item is UNCHECKED or UNVERIFIABLE.

## QA Complete

# QA Report — Domain-Accuracy Content Lens (TFEP forensic→troubleshoot rename, Phase 2)

**Topic:** TFEP forensic→troubleshoot backend rename (Phase 2 wording verification)
**Date:** 2026-06-16
**Phase:** doc-qualitative (domain-accuracy content lens)
**Fix cycle:** N/A (REPORT ONLY — fix_authorization: false)

---

## Overall Verdict: FAIL

The Phase 2 rename of escalation-related wording from "forensic" terms to
"diagnostic" terms is internally self-contradictory and leaves the document
factually inaccurate. The escalation-count semantics are preserved (good), but
the new `**Diagnostic backend:**` declaration makes a falsifiable claim that the
rest of §4.5 contradicts, and the rename was applied inconsistently — four
"forensic" tokens (including the load-bearing `/sc:forensic` invocation string)
remain in the very block the declaration claims is backend-neutral.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | "diagnostic depth" replaces "forensic tier" without changing escalation-count semantics (1st/2nd/3rd) | PASS | SKILL.md:208-212 — count→action map (1st→`--tier light --intent triage`, 2nd→`--tier standard`, 3rd→FULL STOP) is byte-identical to master; only the prose label "forensic tier"→"diagnostic depth" changed (diff line 28-30). Semantics unchanged. |
| 2 | `**Diagnostic backend:**` claim — "swapping the backend changes only this declaration and the invocation string" — is TRUE given §4.5 as it stands | FAIL | See Issues #1, #2, #3. The claim is false on its face: the backend is named `troubleshoot` but the invocation is `/sc:forensic` with flags (`--tier`, `--intent`, `--caller`) that `/sc:troubleshoot` does not accept. |
| 3 | task.md:48 rename ("without structured diagnostic escalation analysis") preserves `--no-escalation` warning meaning | PASS | task.md:48 — only prose "structured forensic analysis"→"structured diagnostic escalation analysis" changed (diff line 9-10). The behavioral claim (bypass TFEP triggers, voids protection against ad-hoc fixes) is byte-identical to master. Meaning preserved. |

## Summary
- Checks passed: 1 / 3 fully (2 if counting the two PASS sub-claims; the central claim FAILS)
- Checks failed: 1 central check (item 2), decomposing into 3 distinct findings
- Critical issues: 1
- Important issues: 2
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | SKILL.md:137 vs 214,260,261 | The `**Diagnostic backend:**` declaration names the backend `troubleshoot` (`/sc:troubleshoot`) and claims "swapping the backend changes only this declaration and the invocation string." But the invocation string at line 214 — and the Escalation Budget lines 260-261 — still say `/sc:forensic`. The declaration was added; the invocation it points at was NOT updated. A reader is told the backend is troubleshoot, then told to invoke a different command. The declaration's own central promise is violated within the same section. | Either (a) update line 214 + 260-261 to `/sc:troubleshoot ...`, or (b) if Phase 2 deliberately defers the invocation-string swap, the declaration must say so (e.g., "invocation string swap pending Phase 3") rather than asserting the swap is already a one-line change that has been honored. |
| 2 | CRITICAL | SKILL.md:137,214 vs commands/troubleshoot.md:8,48-58 | The declaration claims swapping to the `troubleshoot` backend touches "only ... the invocation string." This is factually false: `/sc:forensic` is invoked with `--tier {tier}`, `--intent triage`, `--caller task-unified` (line 214). `/sc:troubleshoot` accepts none of these — its flag surface (troubleshoot.md:8,48-58) is `--type`, `--depth quick\|standard\|deep`, `--scope`, `--no-escalate`, `--fix`, `--models`, `--output-dir`, `--no-doc-discovery`, `--no-mcp`. The escalation tiers (`light`/`standard`) map to troubleshoot's `--depth` (`quick`/`standard`/`deep`), and `--no-escalation` (task) vs `--no-escalate` (troubleshoot) differ. Swapping backends therefore requires a flag-vocabulary translation, NOT just a string substitution. The "backend-neutral / only the invocation string" claim materially understates the coupling and will mislead whoever performs the actual swap. | Soften the claim to reflect reality: swapping the backend changes the declaration, the invocation string, AND the flag mapping (escalation count→backend depth/intent flags). Or add an explicit flag-translation table (`--tier light --intent triage` → `--depth quick`, `--tier standard` → `--depth standard`). |
| 3 | IMPORTANT | SKILL.md:218,252,255 (also 214,260,261) | Rename applied inconsistently. After Phase 2, "forensic" survives in: line 214 (`/sc:forensic`), line 218 ("Read the forensic return contract"), lines 260-261 (Escalation Budget `/sc:forensic`). Lines 218 was left as "forensic return contract" while its sibling Step-4 heading was renamed to "Consume diagnostic results" (line 217) — so a single step now mixes both vocabularies. This is the exact "drift between paraphrased label and unchanged citation" failure: the prose was renamed but the operative artifact references were not, producing a half-renamed section that reads as two authors disagreeing about the backend's name. | Decide on one vocabulary for Phase 2. If the intent is to keep `/sc:forensic` as the real invocation for now (Issue #1 option b), then DON'T rename the surrounding prose to "diagnostic" yet — the rename should be atomic with the invocation swap. If the intent is full rename, fix lines 214, 218, 260, 261 in the same pass. Leaving line 218 "forensic return contract" next to renamed line 217 is indefensible regardless of which path is chosen. |

## Notes on the two sub-claims that PASS

- **Escalation-count semantics (claim 1): genuinely preserved.** The 1st/2nd/3rd
  trigger → action mapping (SKILL.md:210-212), the `escalation_count` field
  (line 203), the increment/return-to-Step-3 loop (line 223), and the 3rd-trigger
  FULL STOP (line 212, 262) are all byte-identical to master. The rename touched
  only the label "forensic tier"→"diagnostic depth", not the behavior. No finding.
- **task.md:48 `--no-escalation` warning (claim 3): meaning preserved.** The only
  change is "structured forensic analysis"→"structured diagnostic escalation
  analysis." The bypass semantics, the TFEP acronym expansion, and the WARNING
  about voiding ad-hoc-fix protection are unchanged. No finding.

  Minor observation (not a finding, no severity): the new phrase "structured
  diagnostic escalation analysis" is slightly more redundant than master's
  "structured forensic analysis" (escalation is already in the protocol name),
  but it is accurate and does not change meaning.

## Actions Taken
None — `fix_authorization: false`. Report only.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was supplied in the spawn prompt;
this lens ran standalone. No rf-qa PASS items were relied upon.

**(b) Independent semantic checks performed (tool-grounded):**
- Verified escalation-count map unchanged: `git diff master` on SKILL.md showed
  lines 210-212 (1st/2nd/3rd map) outside the changed hunks → semantics intact.
- Verified the backend-neutrality claim against the real troubleshoot flag
  surface: Read commands/troubleshoot.md:8,48-58 (argument-hint + flag table) and
  Grep'd SKILL.md for `--tier|--intent|--caller` → confirmed `/sc:troubleshoot`
  has no `--tier`/`--intent`/`--caller`, falsifying the "only the invocation
  string" claim.
- Verified rename completeness: `grep -n "forensic" SKILL.md` → 4 surviving
  tokens (214, 218, 260, 261), proving the rename is partial.

## Confidence
Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

## Tool engagement
Read: 2 | Grep: 3 | Glob: 0 | Bash: 4

## Recommendations
- Treat Issues #1 and #2 as blocking. The `**Diagnostic backend:**` paragraph as
  written makes a claim (backend = troubleshoot, swap = one string) that the same
  section disproves (invocation = `/sc:forensic` with forensic-only flags). This
  is the kind of confident-but-false statement that misleads the next engineer.
- Decide Phase 2's true scope explicitly: is it a prose-only relabel (then keep
  `/sc:forensic` AND keep "forensic" prose, just annotate intent), or a real
  backend swap (then fix the invocation + flag mapping + all 4 surviving tokens)?
  The current half-state is neither.
- Re-run this lens after remediation; the fix must make SKILL.md:137 self-consistent
  with lines 214/218/260/261 before PASS.

## Self-Audit
1. Factual claims independently verified against source: 3 (escalation-count map,
   troubleshoot flag surface, forensic-token survival) — all via Bash git-diff +
   Grep + Read.
2. Files read: src/superclaude/skills/sc-task-protocol/SKILL.md (§4.5, lines
   133-262), src/superclaude/commands/task.md (lines 30-58), and
   src/superclaude/commands/troubleshoot.md (flag surface, lines 1-131).
3. Why trust this review: every finding cites a specific line number cross-checked
   against the actual `/sc:troubleshoot` flag surface and the `git diff master`
   hunks. The central FAIL is reproducible by `grep -n forensic SKILL.md` (4 hits)
   plus reading troubleshoot.md:8 (no `--tier`/`--intent`).
4. Web research: none performed (all claims are local-file-bound). Tavily not invoked.

## QA Complete

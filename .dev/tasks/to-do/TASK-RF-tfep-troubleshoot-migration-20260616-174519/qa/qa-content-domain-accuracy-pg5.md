# QA Report — Domain-Accuracy (Phase 5)

**Topic:** TFEP troubleshoot-backend migration — §4.5 tier→depth mapping + return-contract branch semantics
**Date:** 2026-06-16
**Phase:** doc-qualitative (domain-accuracy lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: FAIL

Eight findings. Two CRITICAL (one orphaned backend reference that contradicts the live mapping; one unhandled `status`/`recommended_escalation` enum value that drops a real backend outcome on the floor). The rewritten 1st→standard / escalation→deep / systemic→deep / 3rd→FULL-STOP mapping is itself semantically faithful and the depths are valid troubleshoot `--depth` values — but the surrounding branch table and the stale Escalation Budget block are not.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | tier→depth mapping faithful (1st→standard, esc→deep, systemic/≥3→deep, 3rd→STOP) | PASS | task-protocol L208-213 matches the stated intent verbatim |
| 2 | `standard`/`deep` are valid troubleshoot `--depth` values | PASS | troubleshoot L137 `depth: <quick\|standard\|deep\|auto>`; L298-300 enumerate quick/standard/deep |
| 3 | `Do NOT auto-fix tests` asymmetric-cost survives (test_is_wrong) | PASS | task-protocol L222 mirrors troubleshoot L49 MUST-NOT-auto-apply contract |
| 4 | `recommended_escalation` enum semantics match backend definition | PARTIAL→FAIL | none/retry/escalate_depth/halt meanings match (troubleshoot L73), but consumer mishandles ordering + omits `partial` — see F2, F4 |
| 5 | consumer reads only fields the backend emits | PASS | consumer reads exactly the 7-field wire set (L219); does NOT read `test_file_path` (correct per L471) |
| 6 | `--caller task-unified` recognized by backend | PASS | task-protocol L215 sends it; troubleshoot L148/L471 recognizes `caller=task-unified` |
| 7 | `--fix` omission coherent (diagnosis-only) | PASS | task-protocol L215/L236 pass NO `--fix`; troubleshoot L471 confirms diagnosis-only |
| 8 | retry/escalate_depth re-invocations coherent with how troubleshoot runs | PASS (mechanically) | re-run same/deeper `--depth` are valid invocations; but see F3 (escalate_depth from an already-deep run is a no-op) |
| 9 | Escalation Budget block names the live backend | FAIL | L265-266 still name `/sc:forensic` — F1 |
| 10 | systemic/≥3-new branch coherent with "escalation count" framing | FAIL (MINOR) | L209 frames depth as escalation-count-driven, but the systemic branch is count-independent — F6 |

## Summary
- Checks passed: 6 / 10
- Checks failed: 4 (2 CRITICAL, 1 IMPORTANT, 1 MINOR; plus 2 IMPORTANT sub-findings under check 4)
- Critical issues: 2

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F1 | CRITICAL | task-protocol §4.5 "Escalation Budget" L263-268 | The Escalation Budget code block still maps `1st TFEP trigger → /sc:forensic --tier light --intent triage` and `2nd → /sc:forensic --tier standard`. `/sc:forensic` is the OLD backend — no `forensic` skill exists in `src/superclaude/skills/` (verified by directory listing). This directly contradicts the migrated backend (`/sc:troubleshoot`, declared L137) and the live mapping at L208-215 (1st→`--depth standard`, 2nd→`--depth deep`). A reader following the Escalation Budget would invoke a non-existent command. This is the exact aspirational/orphaned-backend failure the migration was meant to remove. | Rewrite L263-268 to reference `/sc:troubleshoot --caller task-unified … --depth standard` (1st) and `--depth deep` (2nd), keeping 3rd→FULL STOP. Align token estimates with troubleshoot's Token Cost Profile (Tier 1 ~3-6k, Tier 2 ~15-30k Claude). |
| F2 | CRITICAL | task-protocol §4.5 Step 4 L220-227 | The branch list never handles `status == "partial"`. The backend `status` enum is `success\|partial\|failed` (troubleshoot L42, L471). The consumer branches on `status=="success"` (L220) and `status=="failed"` (L227) but a `partial` status falls through to whatever `recommended_escalation` says. Troubleshoot explicitly emits `partial` for dropped-grounding / degraded runs and pairs it with `escalate_depth`/`retry` (L471 tie-break: "`status=partial` with low confidence → `escalate_depth`; `status=partial` at tier<2 → `retry`"). The branches DO cover those via `recommended_escalation`, so behavior is *probably* correct — but the asymmetry (status explicitly named for success+failed, silently delegated for partial) is a latent trap: a `partial` run with `recommended_escalation=none` would hit L224 and "insert remediation plan + resume" off a partial/degraded diagnosis. | Add an explicit `status == "partial"` consideration, OR state that `partial` is intentionally routed through `recommended_escalation`. Critically: guard L224 (`recommended_escalation=="none"` → insert+resume) so it does NOT fire when `status=="partial"` — a partial diagnosis should not auto-resume as if remediation-ready. |
| F3 | IMPORTANT | task-protocol §4.5 Step 4 L226 | `If recommended_escalation == "escalate_depth": re-invoke /sc:troubleshoot at --depth deep.` This is incoherent when the run that produced `escalate_depth` was ALREADY at `--depth deep` (the 2nd-trigger and systemic paths invoke `--depth deep` per L211-212). Re-invoking deep→deep is a no-op escalation that cannot deepen; troubleshoot has no depth above `deep` (L137). The backend's own tie-break only emits `escalate_depth` for `status=partial` at any tier, so a deep run CAN return `escalate_depth`, producing an infinite same-depth loop bounded only by the 3rd-trigger FULL STOP. | Specify that `escalate_depth` from a run already at `--depth deep` collapses to FULL STOP (or increments escalation_count toward the 3rd-trigger halt) rather than re-invoking deep→deep. |
| F4 | IMPORTANT | task-protocol §4.5 Step 4 L222 | The asymmetric-cost branch keys off `test_is_wrong == true` only. The backend ALSO emits `remediation_target` (enum `test\|code\|docs\|none`, troubleshoot L75) and `behavior_is_documented` (L51) — the `docs` case ("observed behavior IS documented; do NOT auto-apply a code fix; remediate via spec/stakeholder discussion"). The consumer handles the `test` asymmetric case but has NO branch for `remediation_target == "docs"` / `behavior_is_documented`. A diagnosis concluding "the code is correct, the spec is the bug" would fall through to `recommended_escalation` and, if `none`, hit L224 → insert a remediation plan + resume with `--compliance strict`, i.e. auto-apply a code change the backend explicitly flagged as wrong-target. This breaks the same asymmetric-cost guarantee F3-of-the-test-case is protecting. | Add a branch: `If remediation_target == "docs" (or behavior_is_documented == true): present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.` Mirror the `test_is_wrong` handling. |
| F5 | IMPORTANT | task-protocol §4.5 Step 4 branch ordering L220-227 | Branch precedence is ambiguous/contradictory. L220 (`status=="success"` → go to Step 5) and L224 (`recommended_escalation=="none"` → go to Step 5) can both be true simultaneously and agree — fine. But L220 (`status=="success"` → Step 5) and L226 (`recommended_escalation=="escalate_depth"`) can ALSO co-fire: backend can emit `status=success` while a Tier-1 stop recommends nothing-of-the-sort? Per L471 tie-break `status=success → none`, so in practice they don't collide — but the spec presents the branches as an unordered bullet list with no "first match wins" or mutual-exclusivity statement. A reader cannot deterministically resolve two simultaneously-true bullets. | State explicit evaluation order (e.g., "evaluate top-to-bottom, first match wins") and assert the asymmetric-cost gates (`test_is_wrong`, docs) are checked BEFORE the `status`/`recommended_escalation` resume branches. |
| F6 | MINOR | task-protocol §4.5 Step 3 L208-209 | L209 says "Determine the diagnostic depth based on the **escalation count**", but the very next lines include a branch (`systemic failure OR ≥3 new failing tests → --depth deep`, L212) that is NOT escalation-count-driven — it is a severity classification of the 1st trigger. A 1st trigger that is systemic jumps straight to `deep`, contradicting "based on escalation count." | Reword L209 to "Determine the diagnostic depth from escalation count AND failure severity" so the systemic-override branch is not framed as count-derived. |
| F7 | MINOR | task-protocol §4.5 Step 3 L213 vs L227 | Two distinct "FULL STOP" triggers exist (`3rd TFEP trigger` at L213, and `recommended_escalation=="halt"`/`status=="failed"` at L227) but they are never reconciled. If the backend returns `halt` on the 1st trigger, does the consumer FULL STOP immediately (L227) or continue until the 3rd trigger budget (L213)? Both readings are defensible from the text. | Clarify that a backend-returned `halt`/`failed` is an immediate FULL STOP regardless of escalation_count (it short-circuits the 3-trigger budget). |
| F8 | MINOR | task-protocol §4.5 Step 4 L223 vs L224 | L223 (`status=="success"` → Step 5) and L224 (`recommended_escalation=="none"` → Step 5) are redundant given the backend invariant `status=success ⟺ recommended_escalation=none` (troubleshoot L471). Harmless, but the duplication invites drift if one side changes. | Collapse to a single resume condition, or note they are equivalent per the backend tie-break and kept separate only for defensive clarity. |

## Actions Taken
None — `fix_authorization: false`. All findings reported only.

## Self-Audit (MANDATORY)

1. **Factual claims verified against source:** 10. Every claim cites a specific line in one of the two SKILL.md files, re-read this session.
2. **Files read:** `src/superclaude/skills/sc-task-protocol/SKILL.md` (full, 404 lines — §4.5 at L133-268); `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (full, 603 lines — Output Contract L37-91, Wave 0 L114-152, Wave 2 L292-308, Wave 5 L426-481). Verified `/sc:forensic` non-existence via `ls src/superclaude/skills/ | grep -i forensic` (empty). Verified consumer-read field set vs backend wire set via grep (exact 7-field match).
3. **Why trust this found real issues:** F1 (orphaned `/sc:forensic`) is grep-confirmed against the live skills directory — the named backend does not exist. F2/F4 are enum-coverage gaps proven by enumerating the backend `status` (`success\|partial\|failed`) and `remediation_target` (`test\|code\|docs\|none`) enums and showing the consumer branch list omits `partial` and `docs`. These are not stylistic — they route a degraded/wrong-target diagnosis into an auto-resume code change.
4. **Web research:** None performed (all verification was local-file-bound). Tavily not invoked.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep(bash): 4 | Glob: 0 | Bash: 4

## Recommendations
- Resolve F1 and F2 before proceeding — both are CRITICAL. F1 is the literal orphaned-backend defect the migration exists to eliminate; F2 (compounded by F4) can auto-apply a code change off a partial or wrong-target diagnosis, defeating the asymmetric-cost guarantee.
- F3/F4/F5 should be fixed together: they are all "the branch table under-specifies how the asymmetric-cost gates and the escalate/resume branches compose."

## QA Complete

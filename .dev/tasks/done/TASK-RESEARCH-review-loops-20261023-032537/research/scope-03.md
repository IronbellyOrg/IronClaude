# Research: Session screening 13-18

**Investigation type:** Log evidence screening
**Scope:** Frozen manifest indexes 13-18
**Status:** Complete (screening only; original and corrected handoffs retained)
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt
**Handoff limitation:** Main session will persist any text-only handoff necessitated by higher-priority agent output restrictions and separately verify primary evidence.

## Session Inventory and Provenance
Recovered author report: scope-03-recovered.md. Complete original edits and provenance/corrected physical-line supplement: screening-recovery-source.txt:209 onward. Full original paths in session-manifest.txt.

| Index | Screening result |
|---|---|
|13 | Workflow plan correction, no second semantic review. Related initial plan later implemented in15; no duplicate case. |
|14 | Workflow correction, no second semantic review, no implement. |
|15 | Selected: two distinct final-review packages; one normal fail-fix-pass, one strict fail-fix-fail-fix-pass. |
|16 | Exclude: retry-ladder follow-up correction/PR/cleanup, no target run. |
|17 | Control: operational retry-ladder implementation Task8 fail-fix-pass and final issues-fix-pass; subsequent PR reviews separate. |
|18 | Exclude: analysis/script/PR diagnosis, no target run; use corrected raw physical-line anchors from supplement. |

**Key Takeaways**

- Session 15 is selected; session 17 remains a separate bounded-repair control.

## Observed Sequences and Evidence

Complete evidence retained in scope-03-recovered.md and exact corrections in screening-recovery-source.txt. Session15 first package: original390 FINAL issues,396 operator reopens evidence,411 lint evidence,435 pass/archive. Second package:1932 FINAL issues;1938 accept/fix;1969 evidence corrections; nested agent-acf0a51e6992c50ee.jsonl:116 second FINAL issues (Task10 cites blank log line);2028 parent acknowledges new citation;2036 final pass/archive. Middle failure is absent from progress.md, so ledger-only counting misses it.

Session17 control:832 task misunderstanding;836-858 fixes;868 new reviewer;1276 FINAL;1291 issues including wrong restored basename plus stale citations;1751 re-review;1770 pass. Subsequent PR277 reviews are a distinct process, not implement attempts.

## Key Takeaways

- Session15 supplies the selected strict repeated-final-failure case and a separate normal-repair control. Session17 shows final review can uncover a real bug as well as stale citations. Final issues are not uniformly cosmetic.

## Gaps and Questions

Original report initially counted Unicode separators with splitlines; physical newline correction for session18 is in screening-recovery-source.txt. Use corrected anchors. Missing follow-up REPORT.md is explicitly acknowledged in historical session; merged verdict YAML survives. Never synthesize the missing report.

## Stale Documentation Found

Stale historical ledger citations and unchanged reports after plan edits are observed. These do not establish present-day documentation defects.

## Summary

Screening complete for13-18. Only15 is selected for strict repeated-failure analysis.17 remains a bounded-repair comparison. Original recovered report is preserved, not silently replaced.

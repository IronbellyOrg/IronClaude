# Refactoring Plan
## Overview
Base: V3. Incorporated: V1 (3 changes), V2 (2 changes). Changes planned: 6. Risk: Low (all additive text in a findings list).

## Planned Changes
1. Source V1 F2 (test_review_cli.py:52-62,76), target V3 F2. Append: "tests/review/test_review_cli.py:52-62 and :76 also pin the 4-slot ids and a t1b-1 re-review." Rationale: C-002, 85%. Approach: append. Risk: Low.
2. Source V1 F3 (@default removal), target V3 (new finding after F3). Insert as non-blocking: deleting review-panel.default.json removes @default and template_id default; plan states it only implicitly. Rationale: C-005. Risk: Low.
3. Source V1 F5 / V3 advocate (plugin mirror), target V3 (new finding). Insert as non-blocking: tests/skills/test_review_brief_placement.py:129-134 requires plugins/superclaude/rules/prompts/document_review_loop_prompts.md to be byte-identical to the source rules file; Constraints list no plugins/ path, so a Task 6 edit of that rules file breaks the test. Rationale: C-007, 80%. Risk: Low.
4. Source V2 F4, target V3 F4. Re-grade F4 from MINOR to blocking: Task 4 line 63 and Task 5 line 77 give incompatible return contracts for default_template_name(); the Task 5 acceptance check cannot pass as written. Rationale: X-002 (2 of 3 advocates minor; adjudicated blocking because it makes a named acceptance check unpassable). Risk: Low.
5. Source V2 F3 / X-003, target V3 (new finding). Insert as Necessary deviation, non-blocking: Task 1 gives tier5a two models against source.md:5 "three single-model tier aliases"; resolve_slot makes a fixed slot take the first available model, and the fallback keeps the anthropic-only anchor on Sonnet instead of a Haiku stand-in; the plan should say it departs from the source on purpose. Rationale: C-003, 75%. Risk: Low.
6. Source A-001/A-003 (advocates), target V3. Insert two notes: (a) under --strict-distinct a skipped non-anchor seat silently shrinks wonsol to two reviewers (panel.py:647-656); (b) keeping review-panel.default.json as a frozen packaged template, no longer the fallback, would keep the goldens and outside @default users working; the plan did not weigh it. Rationale: A-001, A-003. Risk: Low.

## Changes NOT Being Made
- V2 F3 as blocking: rejected, fixed-slot semantics make the anchor deterministic (C-003).
- V2 F5 (coverage matrix omissions): withdrawn by its own advocate; not a plan defect.
- V1 F1 claim that frozen-tier golden values stay valid after a rename: rejected (X-001): values embed template_id and template_sha256.
- V1 F2 range :91-100: dropped, those tests still pass with a 3-slot template.

## Review Status
Auto-approved.

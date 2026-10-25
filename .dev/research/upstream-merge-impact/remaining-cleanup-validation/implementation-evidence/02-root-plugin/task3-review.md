# Research: Plugin-local audit dependency delivery

- **Topic type:** Independent spec-compliance review
- **Scope:** Task 3 exact resource closure and approved calibration compatibility
- **Status:** FAIL
- **Closed verdict:** `missing`
- **Persistence:** Parent-persisted independent review of first completed Task3 attempt.
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

## Findings

FAIL. Closed verdict: `missing`. extra_scope=[]; misunderstood=[]. Independent review found two IMPORTANT guard gaps.

1. **Selected-state membership is not revalidated.** The delivered `verify()` re-hashes only existing `manifest.files` rows; it never rechecks the stored selection digest or scoped source inventory (`skills/sc-reflect-protocol/SKILL.md:464-479,497-503,547-550`). The older input tree enumerates explicit inputs/tasklist links rather than the complete scoped dirty/new selection when no tasklist/work-unit subtree exists (`:281,322`). Independent read-only in-memory execution with unchanged selected/copied bytes but changed selection/inventory returned verified; neither altered selection nor Git inventory was checked. Ten producer checks cover existing-source/copy changes, not a newly added relevant source.

   Concrete membership-only case: post audit with task log, scope `src/widgets`, Tier 2 and no tasklist; freeze `main.py`, untracked `helper.py`, and execution log. Another session adds `src/widgets/new_handler.py` while all selected files, frozen copies and `selected-inputs.json` remain byte-identical. The added production file is in declared scope, not output/cache/verification data. Pre-dispatch and post-review verification still pass. Separately, changing the selection file itself is also unchecked. Repair must retain and mechanically recompute the same scoped discovery/exclusions and compare the selection hash. New in-scope files must fail; pinned-output artifacts, unrelated out-of-scope changes and excluded verification caches must not fail. Comparing whole raw repository status would be the wrong repair.

2. **Commit-range alternative contradicts hard guards.** Bundled input resolution declares commit-range an alternative to diff, routes it to post and counts it as an input, but hard-STOPs post without literal diff or task log (`skills/sc-reflect-protocol/refs/input-resolution.md:13,36,56,58`). The stale guard also occurs in bundled SKILL at `:210,1759`; normalization before guards is not specified. The checker at `task3-check.py:144-148` asserts the stale text, so its PASS is not consistency proof. Normalize diff/commit-range before every hard guard or consistently state both as a resolved diff source, retaining missing-input rejection.

**AC dispositions:**
- T3.AC1 met: exactly 22 source-derived additions; actual full contents, canonical/delivered hashes, both adapters and recipe independently checked. Local mapping table at `skills/sc-reflect-protocol/SKILL.md:8-42`. Scorer unchanged; approved calibration/scoring adaptations bounded.
- T3.AC2 met at inventory level only: actual `loader-task3-final-session.stdout.txt:1-2` registers all required identities with empty MCP and explicitly returns INVENTORY_ONLY. Every fixture hash independently compared; isolated HOME/config, external cwd, four plugin directories only. Built-ins do not supply missing framework identities.
- T3.AC3 unmet due to findings 1-2. Restricted reviewer tools/permissions match canonical bytes (`agents/reflect-reviewer.md:5-8,36-40`). Real merge, calibration, citation/report gates and non-execution boundaries remain present, but new snapshot/input guards are incomplete.
- T3.AC4 met: explicit unavailable/degraded and null remediation gate (`skills/sc-reflect-protocol/SKILL.md:44-70`) and separate package prerequisite (`:91-95`). No additional mandatory resource found.
- T3.AC5 met for scope/preservation/check execution, not semantic sufficiency (`task3-namespace-check-output.json:326-335`). Independent hashes show all protected non-command assets and 26 Task2 commands unchanged; corrected manifest and actual fixtures match. No tracked product delta since Task3 snapshot; exactly the 22 untracked additions, no retired restoration. Root reflection behavior remains Task2-only.

Evidence paths without `skills/` or `agents/` prefix are relative to this evidence directory; product paths are repository-relative. Parent persisted the independent result before using it.

## Gaps

Task4 native audit proof remains UNVERIFIED and was not demanded at this gate. Reviewer examined recorded 20 static, 24 inherited and 10 standalone snapshot checks without treating PASS as sufficient; executed only the delivered verifier against an in-memory adversarial unit fixture, with no product/report/fixture writes. No full suite, actual audit, retry-folder read, canonical edit or staging.

## Key Takeaways

Repair the two guard gaps within the existing approved 22-resource boundary, add positive/negative membership-drift regressions and the commit-range input assertion, then require a fresh independent review before Task4. Do not weaken isolation, hash unrelated repository changes or claim the current static PASS proves guard sufficiency.

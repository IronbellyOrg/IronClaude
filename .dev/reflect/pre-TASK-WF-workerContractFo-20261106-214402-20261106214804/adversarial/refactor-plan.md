# Refactoring Plan

## Overview

- Base variant: Variant 3 (opus:refactorer), `variant-3-original.md`
- Incorporated: Variant 1 (R1-1, R1-2, R1-3, R1-5), Variant 2 (QA-1 narrowed), invariant probe (INV-001..INV-016)
- Output: `merged-verdict.yaml` in this folder, `merge_method: adversarial`
- Grading rule for the merged verdict (adopted in Round 2, see debate-transcript.md): P1 = false pass shown under the plan's literal instruction, or a blocker; P2 = needs a reading choice, or a coverage or rule-text defect without a literal false pass; P3 = vacuous, cosmetic or owner note. Per-task AC review does not lower grades.
- Planned changes: 12; rejected: 5; overall risk: Low (verdict assembly only, no repository change)

## Planned Changes

1. **Add finding M-1 (P1): Task 5 status assertion admits the old rule.** Source: V1 R1-1 (round-2-variant-1.md new evidence 1), INV-001, INV-002. Target: findings, first. Content: plan :76 asks only that both texts contain "exited 0"; init-lite.md:92 and SKILL.md:61 keep "succeeded when the audit finished"; fix: pin the exact positive phrase "`succeeded` when `superclaude init-lite` exited 0" on the line carrying `worker_status` (SKILL.md:61) and on init-lite.md's Contract line, assert "when the audit finished" absent from those lines, and keep the new init-lite.md wording free of both "failed tool run" (:792) and "on a failed run". Rationale: C-005 unanimous, 95%. Risk: Low (append).
2. **Add finding M-2 (P1): Task 4 pin admits a clause that lists ignored coverage output.** Source: V2 QA-1 narrowed (round-2-variant-2.md), V3 narrowing, INV-003. Content: plan :66 checks WC-4, `[]`, no write verb; witness clause passes; fix: require an exact exclusion phrase (e.g. "paths git ignores are left out") plus "WC-4" and `[]` in the clause, and add "left out" to `UNATTENDED_EXPECT["test"]["phrases"]` (:349-353) so the removal test (:561-570) covers it; no report-location wording in the pin. Rationale: C-004 92%. Risk: Low.
3. **Merge R3-A1 into R1-2 as finding M-3 (P2), and add INV-005 and INV-006.** Content: the unconditional WC-4 sentence "the report names where those files were written" (plan :30, source.md:13) is false for workflow (report_path is the plan `<id>.md`, return-contract.md:51-52; SKILL.md:62 forbids editing it after reflect). Fix is an owner decision: conditional WC-4 wording plus a short local "the report names them" sentence in build and test (INV-005), or keep the unconditional wording and name workflow as the exception. This decision must be made before `/sc:implement`, because Task 1 fixes the wording and Tasks 2-4 depend on it (INV-006). Rationale: C-003 90%, X-001. Risk: Medium (modifies an advisory item into a gating one).
4. **Keep R3-1 as M-4 (P2), change its fix.** Content: record the decision that the planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` stays unchanged (header :3 "Planning only"); state the search scope as src/, plugins/, tests/ and that spec, excluding specs/history/, .dev/tasks/done/, .dev/orca-command-refactor/decisions/, .dev/reflect/ (INV-010); record it in the package progress.md note or the commit body. Rationale: C-006, X-003. Risk: Low.
5. **Merge R3-3 with R1-4 as M-5 (P2) and add INV-008.** Content: assert on the WC-4 span only (from "- **WC-4." to "\n- **WC-8.", markers verified at WORKER-CONTRACT.md:31, :38) and add the new sentence's key phrase to `RULE_PHRASES["WC-4"]` (:102-108) so `test_rule_check_fails_when_rule_removed` (:586-593) covers it. Risk: Low.
6. **Add finding M-6 (P2): global WC-4 exclusion vs init-lite's unconditional list.** Source: INV-007, R3-A3, R1-5. Content: init-lite.md:92 and SKILL.md:61 list every printed `Scaffold:` file; `--project-root` accepts any directory (init_lite.py:294-298, :338). Fix: one WC-4 clause that its exclusion applies to every command's `artifacts` list, including init-lite's and index-repo's (index-repo.md:189). Risk: Low.
7. **Merge R3-2 with R1-3 and QA-2 as M-7 (P3), qualified by INV-009.** Content: Task 1 AC3 is vacuous (core/ outside AUDIT_ROOTS :1054-1058); `test_every_repo_setup_line_is_gated` (:573) also reads only setup lines (:429-460); the real guard is M-5's pins; drop AC3 or reword it to "the new WC-4 sentence holds no literal `git add`". Risk: Low.
8. **Keep R3-4 as M-8 (P3)**, merged with INV-005 note: remaining duplication in build.md:104; keep local text only where M-3's decision requires it.
9. **Keep R3-5 as M-9 (P3), narrowed, add INV-004.** Content: return-contract.md:43-54 names no WORKER-CONTRACT.md; use the input-parse.md:16 form "`~/.claude/WORKER-CONTRACT.md` (rule WC-4)"; do not add a backticked `artifacts` above :52, or `_artifacts_clause` (:769-774) reads the wrong line.
10. **Add M-10 (P3): `[]` wording.** Source: INV-011. "`[]` when nothing else listable was written" for test.md (and build).
11. **Add M-11 (P3): init-lite status basis.** Source: INV-016, R1-5. State that the tool's exit code is the only basis for `succeeded` (SKILL.md:63 allows non-CLI work); note a failed scaffold write leaves a raw OSError traceback in `reason` (init_lite.py:278).
12. **Add delivery note (A-001, INV-006)** at the top of the merged verdict: `/sc:workflow` never edits the plan from these findings (SKILL.md:62); the owner revises the plan (or decides M-3) before `/sc:implement`, or the executor applies P1/P2 fixes in-task where no owner decision is needed (M-1, M-2, M-4, M-5, M-6).

## Changes NOT Being Made

| Diff point | Non-base proposal | Rationale |
|------------|-------------------|-----------|
| X-001 | QA-1's original demand for report-location wording in the test.md clause | V2 withdrew it (round-2-variant-2.md item 2); WC-4 owns that duty, subject to M-3 |
| C-001 | QA-2's synthetic write-verb test for WORKER-CONTRACT.md | Conceded by V2; scan roots exclude core/ |
| C-001 | R3-2's `git add` grep as the AC3 fix | V3 conceded R1-3 is better; INV-009 shows both are weak; M-7 keeps only the drop/reword |
| C-008 | R3-5's criterion "no src/superclaude/ path" on all command sections | Already guarded at test_worker_contract.py:517; applies to return-contract.md only |
| C-010 | R3-A2 (report_path in an ignored path) as a finding | Out of the brief; stays advisory |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1-2, 4-11 | Low | Adds or merges verdict entries | Remove the entry |
| 3 | Medium | Turns an advisory into a gating P2 with an owner decision | Restore R3-A1 to the advisory block |
| 12 | Low | Delivery note | Remove the note |

## Review Status

- Approval: auto-approved (non-interactive)
- Timestamp: 2026-11-06T22:15:00Z

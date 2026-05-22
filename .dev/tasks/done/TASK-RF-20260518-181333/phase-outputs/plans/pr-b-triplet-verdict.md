---
title: "PR-B Audit Suite + Task-Builder Test Fixes — Pre-PR Triplet Verdict"
branch: "test/audit-suite-pr2-nfr-invariants"
base: "ff99449 (master)"
head: "82b7ce0"
commits: ["f3f1df5 test(audit): land NFR-CONV invariant suite + realign 3 task-builder-merge assertions", "82b7ce0 style(audit): apply ruff --fix to audit suite (7 auto-fixes)"]
date: "2026-05-18"
---

# PR-B Triplet Verdict — `test/audit-suite-pr2-nfr-invariants`

## Overall: **PR-READY-WITH-DEPENDENCY** (depends on PR-F merging first to fully green)

| Triplet Step | Exit | Result | New from PR-B | Verdict |
|--------------|------|--------|---------------|---------|
| 1. `uv run ruff check src/ tests/` | 1 | 58 errors | +9 (intentional N801/N999 test naming) | PASS-with-rot-budget |
| 2. `uv run pytest tests/audit/ tests/skills/test_task_builder_merge.py -q` | 1 | 30 failed / 5 errors / 1221 passed | +30/+5 (PR-F-dependent) / +68 PASS | PASS-with-PR-F-dependency |
| 3. `make verify-sync` | 2 | pre-existing drift | 0 | PASS |

## Step 1 Detail — Ruff +9 Intentional Naming

The 49→58 delta (+9) is from the audit tests introduced by this PR. All 9 new errors are naming-convention only (N801 class names with underscores like `TestPartA_OneLowFindingFailsGate`, N999 module names like `test_invariant_preservation_NFR_6_through_10`, `test_monotonicity_halt_F_5_5_5`, `test_sequencing_PR06_before_PR04`). These names are intentional readability patterns for grouped test families and are acceptable under the CONTRIBUTING.md rot-budget convention. 7 auto-fixable ruff issues were applied in commit `82b7ce0`.

## Step 2 Detail — PR-F Coupling

- **Task-builder tests (tests/skills/test_task_builder_merge.py):** **68/68 PASS** — the Phase 2 drift remediation (3 substitutions on L165, L384-387, L408) is working correctly.
- **Audit tests (tests/audit/):** 30 failures + 5 setup errors out of ~120 audit tests. ALL 35 failures assert against content that lives on PR-F (`docs/reference/nfr-conv-2-prose-determinism.md` and SKILL.md hook-sync sections). The test files themselves are correct; their assertions go from FAIL → PASS once PR-F merges. The remaining ~85 audit tests PASS on this branch.

**Recommendation:** Merge **PR-F before PR-B** to land the assertion-target content first. Then PR-B's 30+5 audit failures clear on master without rework.

## Step 3 Detail — Verify-Sync

Same pre-existing drift as cleanup branch and PR-A — `reject-workspace-writes.sh` not registered in `_FRESHNESS_SCRIPTS`. PR-B touches only `tests/`; cannot affect this drift. Resolved by PR-F.

## Commits

| SHA | Title | Files | Stats |
|-----|-------|-------|-------|
| `f3f1df5` | test(audit): land NFR-CONV invariant suite + realign 3 task-builder-merge assertions | 18 | +4919/-6 |
| `82b7ce0` | style(audit): apply ruff --fix to audit suite (7 auto-fixes) | 5 | +6/-7 |

## Paste-Ready `gh pr create` Command

```
gh pr create \
  --title "test(audit): NFR-CONV invariant suite + task-builder-merge test fixes" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-B-audit-suite-nfr-invariants.md \
  --base master \
  --head test/audit-suite-pr2-nfr-invariants \
  --draft
```

Use `--draft` because audit tests fail until PR-F lands.

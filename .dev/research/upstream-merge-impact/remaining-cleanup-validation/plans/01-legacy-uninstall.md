---
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Retire the optional legacy-uninstall facility

Source: ../REPORT.md (Retire optional legacy uninstall); ../../remaining-cleanup-validation-prompt.txt
Goal: Remove the unsafe optional legacy cleanup entry point and its active references without changing ordinary installation/update or user data.

## Constraints

- Written plan only. No implementation or staging has started. This is an ordinary source tasklist using the registered simple-task template, not a generated managed workflow package or a claim that a workflow reflection gate ran.
- Future execution requires separate authorization. Reconfirm checkout/branch/HEAD and preserve all pre-existing tracked, staged, untracked and ignored work before edits. Use a feature branch when execution is authorized; do not discard/rebase other work.
- Product allowlist: delete `scripts/uninstall_legacy.sh`; edit only `Makefile` and `docs/getting-started/installation.md` blocks named by Task 1. New task-owned checks/evidence belong under `../implementation-evidence/01-legacy-uninstall/`, not production source.
- Never run the destructive script, its Make target, a historical inverse/revert, or substitute home-folder deletion instructions. Do not touch user settings, backups, installed assets or legitimate memory data.
- Preserve ordinary install/update/package-uninstall guidance, native MCP lifecycle and every unrelated Make target/help entry.
- No new dependency on the other three cleanup plans. Suggested execution order is first because this is an unsafe optional deletion entry point.
- Do not resume the older CI follow-up plans or repeat accepted sync/Codecov removal. Do not recreate the importer/cursor, close PR 283, delete origin's sync/framework, stage, commit, push or open PRs under this plan.
- Use UV for Python checks. Independent final review must judge current files and recorded outcomes, not a claimed completion. External callers and future runtime outcomes remain UNVERIFIED.

## Phase 1: Retire the optional entry point coherently

## Task 1: Remove the legacy script, Make entry point and installation recommendations

Read `scripts/uninstall_legacy.sh`, `Makefile`, `docs/getting-started/installation.md`, and the validation's optional-uninstall section. Freshly search all tracked non-artifact callers before deletion. The current script suppresses a failed backup copy before deleting the original (`scripts/uninstall_legacy.sh:33-43`), and the current caller set is confined to Make/help and the installation guide (`../baseline.json:59-72`).

Capture the fresh baseline required by Constraints, including original contents/hashes for comparison. Delete `scripts/uninstall_legacy.sh`. In `Makefile`, remove only its `uninstall-legacy` phony token, help entry and dedicated comment/target/recipe; preserve `make help` and all unrelated definitions. In `docs/getting-started/installation.md`, remove the old-plugin cleanup invocation and its descriptive/backup paragraph (currently 346-347 and 366), while retaining accurate package uninstall, leftover-installed-file, manual-review and update/backup warnings. Do not replace the script with another automatic removal path.

Leave a small runnable static check under the task evidence directory. It must compare exact Makefile/document edits against the task baseline, assert deletion including no dangling symlink, and fail when an old active reference remains. Search return code 1 means no matches; unexpected errors are failures, not hidden with `|| true`. Do not execute cleanup to test its absence.

Acceptance criteria:
- The only changed product paths are the three named allowlist files, with the script deleted and no equivalent replacement destructive facility added.
- No active tracked caller, Make target, help entry, phony token or guide recommendation still names `uninstall-legacy` or `uninstall_legacy.sh`, excluding `.dev/` historical artifacts.
- Exact baseline comparison confirms no other Make target/help entry changed. Ordinary install/update/native helpers and all protected user data/settings/backups are untouched.
- Installation documentation accurately distinguishes Python package uninstall and separately installed home-folder files; it no longer promises this retired backup/cleanup facility.
- The static checks execute successfully through UV and their commands/results are recorded in the task-owned evidence. No home cleanup, installer, historical revert, stage, commit, push or remote operation was run.
- A fresh independent review verifies each criterion from the diff/current files and evidence; any failure blocks completion. External scripts calling the removed target remain an explicitly UNVERIFIED compatibility limit.

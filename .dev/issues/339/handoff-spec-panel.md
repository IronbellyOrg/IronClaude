# Handoff: spec-panel stage (/sc:spec-panel --mode critique --focus requirements,architecture), DONE
- Updated: 2026-11-08T06:20Z
- Review: .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-review.md (29 findings: 3 CRITICAL, 17 MAJOR, 9 MINOR; overall 6.1/10).
- Owner decisions: SP-01, the INV-005 allowlist extended to seven verbs (coordinator msg_9d0851e4c489, after the static check of task-list and worktree ps found no git: addendum in .dev/issues/339/analysis/inv-005-orca-index-lock.md). The owner authorized spec edits.
- Fix cycle 1 (log spec-panel-fix-log-1.md): SP-01 to SP-18, SP-28 and SP-29 fixed in merged-requirements.md (now 653 lines; adds NFR-014 and NFR-015; the fallback is now rule 9). Review 2 (spec-panel-fix-review-1.md): PASS, 0 blocking, 10 minor notes (M1 to M10, not applied; for example section 2 says --include-remote is out "until its cost is measured" while sections 8 and 13 say "never"). Loop closed after 1 fix cycle.
- Still open for /sc:design: G-1 (no rule for files left after an exit-1 run) together with SP-20; MINOR SP-19 to SP-27; fix-review notes M1 to M10; GQ-101 to GQ-113 (GQ-103(1) first); UNVERIFIED items: the Orca version source, the unknown-Run stderr shape, the tab map Run id, and the --no-sync and --untracked-files=all effects.
- Next: /sc:design --type architecture --format spec --output docs/designs/orchestrator-mode.md with merged-requirements.md as input.
- Rules: reads at most 150 lines; never stage .claude/ except settings.json; .dev/tasks/ always staged; commit only when asked; never merge.
- Coordinator: run:run_93bfa00cae2b. Follow-up filed: IronbellyOrg/IronClaude#446 (WC-9 10 s lock retry).

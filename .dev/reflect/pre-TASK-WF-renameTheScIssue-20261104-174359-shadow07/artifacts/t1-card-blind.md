# Blind calibrator input — T1 card (shadow07)

[CARD ONLY — no formation context]

Tier-1 reflection card, UC-1 pre audit of the plan TASK-WF-renameTheScIssue-20261104-174359 (rename /sc:issue summary.md -> issue-summary.md across skill package, three agent files, command Outputs table, tests, design doc).

Coverage: Pass 1 = 0 requirement IDs. Pass 2 = 5 inferred quote-pinned rows (INF-001 rename everywhere; INF-002 analysis naming rule; INF-003 fix-2 paragraph mechanism; INF-004 deterministic regression test; INF-005 dated design note), all containment-matched to tasks (0.80-0.90). coverage_pct_union 1.0; coverage_pct null; coverage_degraded parsed-sparse.

Grounding: all anchors re-verified on disk this run (SKILL.md templates row + Wave 4 rule; refs/claim.md naming rule; refs/chains.md <S>; two templates; three agent files carry the verbatim Constraints paragraph; Outputs claim row; tests _HARNESS_REPORT_NAME/written_md_names/five tests; design doc dated note). Repo-wide sweep: zero residual summary.md on the /sc:issue surface; remaining hits unrelated sprint/eval subsystems. Guides verified: no /sc:issue summary-file reference.

Hypotheses:
- H1 (medium candidate): no task schedules make sync-dev / make verify-sync after editing src/superclaude/{skills,agents,commands}; constraint forbids touching .claude/; plan-as-written leaves mirror stale and pre-commit verify-sync failing. Disk today: mirror in sync (executed run synced outside the plan's letter). Missing-AC process risk.
- H2 (minor candidate): T1.AC3 grep 'summary\.md' matches 'issue-summary.md' as substring; AC readable only as grep-minus-issue-summary. Ambiguity, non-blocking.
- H3 (minor candidate): T3 red-check uses the 10 pre-fix copies; adequate (name-based checks).
- H4 (low): plan line anchors pre-edit; content descriptions accompany each; non-finding.
- H5, H6: resolved non-findings.

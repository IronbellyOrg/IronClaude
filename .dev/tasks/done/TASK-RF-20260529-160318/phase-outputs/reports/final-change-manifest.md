# Final Change Manifest — Wave 1.6 Diagnosability Audit

Captured: 2026-05-29 17:55
Task: TASK-RF-20260529-160318 — Implement Wave 1.6 Diagnosability Audit into sc-troubleshoot-protocol skill.

## `git status --short` (scoped to sc-troubleshoot-protocol src + .claude mirror)

```
 M src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
 M src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
 M src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md
 M src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
?? src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md
```

5 paths total under `src/superclaude/skills/sc-troubleshoot-protocol/` — 4 modified + 1 new (untracked).

**No `.claude/skills/sc-troubleshoot-protocol/*` paths shown** because `.claude/` is gitignored per CLAUDE.md absolute rule (only `.claude/settings.json` is tracked, and this task did not touch that file). The `make sync-dev` from Phase 5 mirrored these changes into `.claude/` — the mirror exists on disk but is invisible to git, by design.

## `git diff --stat src/superclaude/skills/sc-troubleshoot-protocol/`

```
 .../skills/sc-troubleshoot-protocol/SKILL.md       | 90 ++++++++++++++++++++--
 .../refs/escalation-rubric.md                      |  8 ++
 .../refs/hypothesis-card-template.md               |  2 +
 .../refs/report-template.md                        | 60 +++++++++++++++
 4 files changed, 154 insertions(+), 6 deletions(-)
```

Note: the new file `refs/diagnosability-audit.md` (340 lines) is untracked and therefore not in the diff stat. Once staged it will contribute +340 lines.

## Paste-ready commit message (single line, no heredocs per `feedback_no_multiline_paste.md`)

**Subject (≤70 chars):**

```
feat(sc-troubleshoot-protocol): add Wave 1.6 Diagnosability Audit
```

**Body (≤6 lines of prose):**

```
Adds Wave 1.6 between Wave 1.5 and Wave 1.7 to audit existing instrumentation before fanning out Tier 1/Tier 2 hypothesis work. Computes a diagnosability_verdict from 2 parallel branches (log-call inspection + log-config reachability); hard-stops to Wave 5 when verdict=insufficient + complexity=non-trivial + NOT --no-escalate, emitting an invocation-site-only instrumentation tasklist instead of hypothesis work. New ref refs/diagnosability-audit.md (8 sections); 3 modified refs (hypothesis-card-template, report-template, escalation-rubric); 12 SKILL.md change-points (E1-E11 + 12th flag-parsing addition at SKILL.md Wave 0 step 1). Spec: .dev/brainstorms/20260529-141819-troubleshoot-wave-1-6-diagnosability/merged-output.md (adversarial convergence 0.78). Quality gates: PG.A 10/10, PG.B 31/31, PG.C 7/7 (all 100% confidence).
```

## Mandatory paste-ready `git add` lines (per CLAUDE.md absolute rule — ONLY `src/superclaude/...` paths)

**SAFE:**

```
git add src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
git add src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md
git add src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
git add src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md
git add src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
```

(5 paths total — 4 modified + 1 new.)

**FORBIDDEN — DO NOT RUN (would trigger the gitignore + pre-commit verify-sync local hook violation):**

```
# NEVER:
git add .claude/skills/sc-troubleshoot-protocol/...     # gitignored, MUST NOT be staged
git add -A                                              # too broad; would catch unrelated files (incl. the 126 collateral Python format changes from Phase 5 Step 5.4)
git add .                                               # same risk as -A
git add -f src/.../diagnosability-audit.md              # the `-f` is never required for src/ paths; if you find yourself needing -f for any path, STOP and re-check
```

## Pre-stage cleanup (recommended)

Before staging Wave 1.6 work, recommend reverting the 126 collateral Python format changes from Phase 5 Step 5.4 (pre-existing repo state inadvertently formatted by `make format`):

```
git checkout -- '*.py'
```

This keeps the Wave 1.6 commit focused. If the user prefers to land those format changes as a separate cleanup PR, they can stash + apply later.

## PR target reminder (per CLAUDE.md absolute rule)

When opening a PR for this work, the mandatory command shape is:

```
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

NEVER bare `gh pr create` — gh's default would route this PR to the public upstream `SuperClaude-Org/SuperClaude_Framework` (see memory `feedback_pr_target_fork_only.md`). The `--repo IronbellyOrg/IronClaude` flag is non-negotiable.

After PR creation, verify the returned URL contains `https://github.com/IronbellyOrg/IronClaude/pull/N`. If it shows `SuperClaude-Org`, close it immediately and reopen with `--repo IronbellyOrg/IronClaude`.

## Summary of artifacts this task produced

- **1 new ref file** (8 sections + Loading discipline; 340 lines): `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`
- **4 modified files** in src/superclaude/skills/sc-troubleshoot-protocol/: `SKILL.md` (+~78 lines net), `refs/hypothesis-card-template.md` (+2 lines), `refs/report-template.md` (+72 lines), `refs/escalation-rubric.md` (+8 lines)
- **5 mirrored files** in `.claude/skills/sc-troubleshoot-protocol/` (via `make sync-dev`; gitignored, not staged)
- **17 handoff files** under `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/`: 4 discovery + 3 reviews (pg-a/b/c) + 5 test-results + 5 reports (this manifest is #5)

## Verification artifact paths (for the eventual PR description)

- PG.A QA: `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reviews/pg-a-qa-report.md` — 10/10 PASS
- PG.B QA: `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reviews/pg-b-qa-report.md` — 31/31 PASS
- PG.C QA: `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reviews/pg-c-qa-report.md` — 7/7 PASS
- Phase 5 sync validation: `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reports/phase-5-validation-summary.md`
- Read-through (SKILL.md narrative): `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reports/read-through-skill-md.md`
- Read-through (new ref structural twin): `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reports/read-through-new-ref.md`
- Cross-reference resolution: `.dev/tasks/to-do/TASK-RF-20260529-160318/phase-outputs/reports/cross-ref-check.md`

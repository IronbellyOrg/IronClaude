# Refactoring Plan: Merged Reviewer Verdict

## Overview

- Base variant: Variant 3 (reviewer-3, opus, refactorer), combined score 0.896 (`base-selection.md`)
- Incorporated variants: Variant 1 (0.818), Variant 2 (0.605); Round 2.5 invariant probe (`invariant-probe.md`)
- Output: `merged-verdict.yaml` (YAML reviewer-card shape, `merge_method: adversarial`)
- Planned changes: 12; rejected: 5
- Overall risk: Low (additive findings; two severity downgrades)
- Every recommendation is phrased as an implementation-time instruction (A-002 ACCEPT, unanimous): the gated plan is not edited.

## Planned Changes

### Change #1: Verdict becomes needs_revision, driven by R1-F1
- Source: Variant 1 verdict; S-002 (V1, 95%)
- Target: top-level `verdict`
- Approach: replace `revise` with `needs_revision`
- Risk: Low

### Change #2: Add M-1 (blocking) = R1-F1 bare /ponytail
- Source: Variant 1 R1-F1; C-001, X-001 (V1, 100%)
- Target: first finding
- Approach: insert. Claim: plan:80 "bare /ponytail switches to full" is false under lite. Evidence `/tmp/ponytail-src-t14b/mode-tracker.js:109-119` (`:117`). Class drift, blocking. Instruction for Task 3: write "bare `/ponytail` reports the current level when Ponytail is on, and switches it on at the default level (lite) when it is off (`full` if the default is `off`)" (INV-002 folded in).
- Risk: Low

### Change #3: Add M-2 (blocking) = INV-001 mode-switch scope
- Source: invariant-probe INV-001 (HIGH, UNADDRESSED)
- Target: second finding
- Approach: insert. Claim: plan:80 "switches every session in that repo until a new session starts there" is wrong in scope. Evidence: `hooks_claude-codex-hooks.json:5` (startup|resume|clear|compact), `hooks_ponytail-activate.js:193,55`, `runtime.js:51-66,75-78`, `mode-tracker.js:143-148`. Instruction for Task 3: say the switch is recorded per project directory (each worktree separately), that any new session, `/clear` or resume in that directory resets it to the default for every session there, and that other running sessions see the new level only in their subagents.
- Risk: Low

### Change #4: Downgrade R3-1 to minor and extend the guard
- Source: Variant 1 R1-F2 calibration; C-002 (V3 content, V1 severity); INV-016
- Target: R3-1
- Approach: modify severity blocking -> minor (CLAUDE_CONFIG_DIR and XDG_CONFIG_HOME verified unset 12:48Z); instruction: run the Task 4 proof as `env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME -u PONYTAIL_DEFAULT_MODE -u PONYTAIL_MAP -u PONYTAIL_SUBAGENT_MATCHER HOME=<throwaway> ...`, and log that none is set inside.
- Risk: Low

### Change #5: Counting rule for R3-2
- Source: C-003 (V3, adopted by V1 and V2 in Round 2)
- Target: R3-2
- Approach: keep `git diff --numstat` <= 5 insertions and <= 5 deletions, all inside `install_plugins`; class grounding gap.
- Risk: Low

### Change #6: R3-4 instruction made concrete
- Source: C-004, X-002 (V3, 100%); V1/V2 Round 2 evidence
- Target: R3-4
- Approach: modify recommendation: after Task 3, run `uv run pytest tests/docs -v` (`test_retired_docs_absent.py:41,44`, `test_tavily_doc_alignment.py:45,117`) and markdownlint on `docs/getting-started/installation.md` (`.pre-commit-config.yaml:73-88`).
- Risk: Low

### Change #7: Replace R3-5 with the residual unsourced claims
- Source: V3 Round 2 (reset grounded `activate.js:193,55`; "PONYTAIL DEFAULT SET" grounded `mode-tracker.js:71`)
- Target: R3-5
- Approach: restate: plan:89's AC cannot check claims outside the lite-facts block; remaining unsourced claims: "a project .claude/settings.json wins" (plan:81) and "do not only run claude plugin uninstall" (INV-014). Instruction: source each from Claude Code docs or drop it.
- Risk: Low

### Change #8: Add M-3 (minor) = docs accuracy of the lite description (INV-003, INV-004, INV-006, INV-008, INV-009, INV-013)
- Source: invariant-probe MEDIUM/LOW
- Target: new finding
- Approach: insert. Instructions for Task 3: say lite injects Ponytail's full rule set with the lite level row (not only the row), including "end your reply with one or two lines"; say Ponytail's files follow `CLAUDE_CONFIG_DIR` while the installer writes `$HOME/.claude` (so the defaults do not apply when it is set); say the statusline note can be used up by a headless `claude -p` run; mention "stop ponytail" / "normal mode"; call `PONYTAIL_SUBAGENT_MATCHER` best-effort (fails open); say where the `ledger` option is set (plugin options via `/plugin`, verified before writing) or name it only as Ponytail's `ledger` option with the upstream default.
- Risk: Low

### Change #9: Add M-4 (minor) = Known Limitation scope (INV-005)
- Source: invariant-probe INV-005
- Target: new finding
- Approach: insert. Instruction: the Known Limitation sentence should say the extra clone can also push the other default plugins past the 30 s budget (all marketplace adds run before installs, `install_user_setup.py:272-284`).
- Risk: Low

### Change #10: Add V2 coverage conclusions
- Source: Variant 2 R2-F1, R2-F2, coverage_check (C-005, V2 90%)
- Target: new `coverage` block
- Approach: insert: all eight containment-unmapped rows (INF-001, -002, -003, -005, -007, -014, -015, -017) are owned by plan elements; goal span covered at plan:15,39,82; T5 fails on unfixed code.
- Risk: Low

### Change #11: Keep R3-8 diagnostics only
- Source: X-003 (V2, 90%)
- Target: R3-8
- Approach: modify: proof stays in Task 4; record whether Orca was on PATH and its time used.
- Risk: Low

### Change #12: A-001 note
- Source: A-001 (QUALIFY, unanimous)
- Target: new note
- Approach: insert: docs and CHANGELOG say behaviour was checked against Ponytail v5.3.3; M1 records the installed plugin version.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| S-002 | V2 verdict `pass` | Refuted by M-1; V2 conceded |
| C-003 | V2 rule `<= 4 ins / <= 3 del` | Withdrawn in Round 2; false-fails a wrapped line |
| C-006 | V3 "move proof to its own task" | Plan edit forbidden (A-002); V3 conceded |
| C-008 | V3 "reset clause unsourced" | Grounded by `activate.js:193,55`; V3 conceded |
| C-009 | V3 R3-3 dependency change | Informational; sequential execution is safe |

## Risk Summary

All changes are additive or severity recalibrations of findings every advocate accepted. Rollback: the three original cards stay on disk as `variant-N-original.md`.

## Review Status

- Approval: auto-approved (non-interactive)
- Timestamp: 2026-11-04T13:25:00Z

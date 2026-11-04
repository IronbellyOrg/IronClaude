# Diff Analysis: Reflect Reviewer-Card Comparison

## Metadata

- Generated: 2026-11-04T13:00:00Z
- Variants compared: 3 (variant-1 = reviewer-1 sonnet/analyzer; variant-2 = reviewer-2 glm-5.3/qa; variant-3 = reviewer-3 opus/refactorer)
- Audit target of every variant: plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md` vs its `source.md`
- Input type warning: variants are YAML reviewer cards, not markdown; compared as text.
- Total differences found: 23
- Categories: structural (2), content (11), contradictions (3), unique (5), shared assumptions (2)
- Orchestrator facts available to the debate (verified this session): `CLAUDE_CONFIG_DIR` and `XDG_CONFIG_HOME` are both unset in the executing worker (bash check 12:48Z). Upstream `ponytail-activate.js:55,193` rewrites the repo's mode to the default on every non-compact session start. The /sc:workflow protocol forbids editing the gated plan from reflect findings (findings are advisory; fixes land during implementation).

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card shape | 4 findings + confirmed_claims + notes | coverage_check block + 4 findings + notes | scope_check block + 9 findings + verified_adherent | Low |
| S-002 | Verdict vocabulary | `needs_revision` | `pass` | `revise` | Medium |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Task 3 "bare /ponytail switches to full" | R1-F1: false under lite (mode-tracker.js:109-119), blocking drift | Not raised; upstream facts taken as given | Not raised as false; R3-5 says the AC cannot check claims outside the facts block | High |
| C-002 | Throwaway-HOME isolation of the manual proof | R1-F2: CLAUDE_CONFIG_DIR bypass, blocking (conditional) | Not raised | R3-1: CLAUDE_CONFIG_DIR and XDG_CONFIG_HOME bypass, blocking drift | Medium |
| C-003 | "At most 5 changed lines" counting rule | R1-F3 minor, class authorized; numstat insertions <= 5 | R2-F3 minor, class drift; <= 4 insertions and <= 3 deletions | R3-2 minor, grounding gap; <= 5 insertions and <= 5 deletions inside install_plugins | Low |
| C-004 | Docs verification (tests reading docs, markdownlint) | Not raised | Says every spec check is owned (Task 2 test list) | R3-4: tests/docs/test_retired_docs_absent.py and markdownlint --fix not run, drift minor | Medium |
| C-005 | Containment-unmapped matrix rows | Note: content present, mapping gap only | R2-F1: all are matcher artifacts | Not raised | Low |
| C-006 | Placement of AC-M1..M3 in Task 4 | Not raised | R2-F4: conformant, acceptable | R3-8: move to own task; Orca step can consume 25 of 30 s | Low |
| C-007 | `./artifacts/` base path | R1-F4: ambiguous, use package artifacts/ | Not raised | R3-9: same as R1-F4 | Low |
| C-008 | Task 3 claims outside the lite-facts block | Not raised (beyond F1) | Treats the token list as anchoring the AC | R3-5: AC uncheckable; reset clause unsourced for non-off | Medium |
| C-009 | Task dependency chain | Not raised | Not raised | R3-3: stricter than needed, harmless | Low |
| C-010 | JSON entry shape vs file style | Not raised | Not raised | R3-6: expanded form; prior last line gains a comma | Low |
| C-011 | CHANGELOG link target | Not raised | Not raised | R3-7: no heading to link | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Does the plan contain a false claim? | Yes: plan:80 "bare /ponytail switches to full" is false under lite (R1-F1) | "No false claims found"; verdict pass | Partial: flags the claim set as unsourced (R3-5) but not as false | High |
| X-002 | Is "every test that reads the edited files" fully owned? | Silent | Yes, by Task 2's pytest list (coverage_check) | No: tests/docs reads installation.md and is in no task (R3-4) | Medium |
| X-003 | Is AC-M placement in Task 4 acceptable? | Silent | Acceptable as-is (R2-F4) | Should move to a separate task (R3-8) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | R1-F1: bare /ponytail behaviour under lite, with upstream line evidence | High |
| U-002 | 3 | R3-4: tests/docs and markdownlint must cover installation.md | Medium |
| U-003 | 3 | R3-1 extension: XDG_CONFIG_HOME also bypasses the throwaway HOME (Ponytail ledger/config) | Medium |
| U-004 | 3 | R3-6 / R3-7: JSON formatting and CHANGELOG link-target precision | Low |
| U-005 | 2 | R2-F2: matrix misses the goal span "via the installer and update scripts" (plan covers it) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three verify against `/tmp/ponytail-src-t14b` | The upstream source fetched at main 96608e07 (v5.3.3) is what `claude plugin install ponytail@ponytail` will install; the plugin is unpinned, so docs describe a moving target | UNSTATED | Yes |
| A-002 | All three phrase recommendations as plan edits ("In Task 3 line 80, replace ...") | Recommendations can be applied by editing the plan; the workflow protocol forbids editing the gated plan from reflect findings, so they must be applied during implementation instead | UNSTATED | Yes |
| A-003 | None challenge lite itself | Lite (with its Orca-worker statusline nudge and subagent injection) is the user's decision, not a review target | STATED (source.md:1) | No |
| A-004 | All accept the update path | `superclaude update` and `update.sh` reach `install_user_setup`, so no update-path code change is needed | STATED (merged-requirements.md:19) | No |

Promoted shared-assumption points:

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Upstream source fetched today equals what installs | Medium: docs may drift with upstream releases | Open for debate |
| A-002 | Findings can edit the plan | Medium: governs where fixes land | Open for debate |

## Summary

- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Convergence denominator (S + C + X + A): 2 + 11 + 3 + 2 = 18
- Similarity check: differences are well above 10% of comparable items; debate proceeds.

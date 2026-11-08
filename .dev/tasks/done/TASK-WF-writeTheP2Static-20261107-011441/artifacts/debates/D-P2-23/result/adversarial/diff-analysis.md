# Diff Analysis: D-P2-23 option comparison (task-builder CLI-mode reflect gate under --unattended)

## Metadata
- Generated: 2026-11-07
- Variants compared: 2 (Variant 1 = option A "skip the whole gate"; Variant 2 = option B "run the gate without --fix and --promote")
- Total differences found: 12 diff points that enter the convergence denominator
- Categories: structural (2), content (6), contradictions (2), unique (4, not in the denominator), shared assumptions (2 promoted, 1 stated)
- Shared block: the "How to judge" section is byte-identical in both variants and is not a difference.

## Verified repository facts used by this analysis (read in the working tree on 2026-11-07)
- F1: `src/superclaude/skills/task-builder/SKILL.md:410` holds the option-A paragraph today (uncommitted P2 edit): under `--unattended` the `.dev/tasks` staging is left to the coordinator and the whole CLI-mode reflect gate is skipped, recorded as `reflect gate skipped (unattended)`.
- F2: The CLI-mode gate item is `SKILL.md:2237-2242`. Its Action stages with `git add -A` and runs `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`.
- F3: Spec WC-9 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:77`) says "MDTM's CLI-mode `git add -A` (`sk/task-builder/SKILL.md:2237`) is refused" and that a worker never runs `git add`.
- F4: Spec section 2.1 nested propagation (spec line 62): a callee that does not accept `--unattended` must be gate-free per its section 3 row, or the caller skips the step and records the skip in its contract.
- F5: The wrapper `superclaude reflect run` has no `--unattended` option (zero matches in `src/superclaude/cli/reflect/commands.py`), and its inner prompt is `/sc:reflect --mode post ... ` with no `--unattended` (`src/superclaude/cli/reflect/runner.py:453-483`).
- F6: `--promote/--no-promote` and `--fix/--no-fix` are independent Click flags (`commands.py:236`, `commands.py:296`); `--fix` makes the wrapper pass `--remediate` and auto-run the authored corrective artifact (`runner.py:474-479`).
- F7: Callers already commit to skip semantics: `src/superclaude/commands/tdd.md:168` ("skips its CLI-mode reflect gate, recording `reflect gate skipped (unattended)`"), `src/superclaude/skills/tdd/SKILL.md:391`, and pinned test expectations (`tests/skills/test_worker_contract.py:564`, and write-verb classification entries at `:2709-2724` whose reason text says the CLI-mode reflect gate "is skipped").
- F8: Spec section 3.1 reflect row: reflect is "ready with brief constraints" when the brief passes no `--remediate` and `--no-promote` when the coordinator owns folder moves.

## Structural Differences
| # | Area | Variant 1 (A) | Variant 2 (B) | Severity |
|---|------|---------------|---------------|----------|
| S-001 | Rationale section | Has a separate "Why skip" paragraph tying the decision to `--fix`, `--promote` and `git add -A` (WC-9) | No rationale paragraph; reasons appear only inside the strengths and weakness lines | Medium |
| S-002 | Evidence anchoring | Cites the file, the approximate line (410) and the gate item lines (2236-2244) | Cites no file or line | Medium |

## Content Differences
| # | Topic | Variant 1 (A) approach | Variant 2 (B) approach | Severity |
|---|-------|------------------------|------------------------|----------|
| C-001 | What the gate does under `--unattended` | Skipped entirely | Runs as `superclaude reflect run <task> --depth deep --no-promote` (no `--fix`) | High |
| C-002 | Staging step (`git add -A`) | Skipped with the gate; coordinator stages | "Left to the coordinator or replaced by a note" | Medium |
| C-003 | Handling of Regression or unauthorized Drift | Nothing runs, so nothing is found; the skip is recorded in the task log, no output file | Returned as a blocked result; coordinator decides on a fix | Medium |
| C-004 | Spec 2.1 treatment of a callee without `--unattended` | Takes the "skipped and recorded" branch | Implicitly takes the "gate-free" branch without showing the callee is gate-free | High |
| C-005 | Independent post-execution audit | Lost; the coordinator must run reflect itself | Kept; the report is an artifact the coordinator can read | High |
| C-006 | Self-reported risk surface | One weakness: audit lost | Three weaknesses: flag combination unverified, audit may miss never-staged files, extra nested subprocess and more text | Low |

## Contradictions
| # | Point of Conflict | Variant 1 (A) position | Variant 2 (B) position | Impact |
|---|-------------------|------------------------|------------------------|--------|
| X-001 | Does the retained audit still work without staging? (intra-variant, B) | n/a | B proposes dropping or replacing the staging step, and B's own weakness line says "the audit omits never-staged files, so without the staging step the audit may miss new task artifacts". The mitigation B proposes disables the property B claims as its main strength. | Medium |
| X-002 | Is staging intrinsic to the gate? (cross-variant) | "the gate begins by staging with `git add -A` (WC-9)"; staging and gate are one unit | Staging is separable and can be "replaced by a note" | Medium |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 (A) | Anchors the choice in WC-9 and in the same coordinator-owns-folder-moves reason `/sc:reflect` uses for `--no-promote` | High |
| U-002 | 2 (B) | Keeps an independent, executor-disjoint audit artifact for the coordinator | High |
| U-003 | 2 (B) | Reuses the existing `--no-promote` flag instead of inventing a mechanism | Medium |
| U-004 | 1 (A) | Smallest possible edit: one sentence, already written at `SKILL.md:410` | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The gate can be decided at build time by task-builder, although the gate item is a checklist item executed later by `/task` (the text at `SKILL.md:410` sits in build step A.3, the item at `:2237` runs at execution) | Both variants speak of what "the gate" does under `--unattended` without saying who acts and when | High | UNSTATED, promoted |
| A-002 | Callers (`/sc:tdd`, and `reflect --remediate` and `troubleshoot --fix` through task-builder) have not yet been written to a different contract than "skip" | Both variants treat the choice as free | High | UNSTATED, promoted |
| A-003 | WC-9 forbids a worker from running `git add` | Both variants accept the staging constraint (A cites WC-9; B drops or replaces staging) | Medium | STATED (A cites WC-9); not promoted |

## Summary
- Total structural differences: 2
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Diff points entering the convergence denominator: S 2 + C 6 + X 2 + A 2 = 12
- Highest-severity items: C-001, C-004, C-005, A-001, A-002
- Variants are not "substantially identical" (differences far exceed 10%); debate proceeds.

## Taxonomy tags (AD-5, auto-tagged; each point has exactly one level)
| Point | Level | Signal |
|-------|-------|--------|
| S-001 | L2 | organization (default) |
| S-002 | L1 | presentation |
| C-001 | L2 | architecture / interface |
| C-002 | L3 | state (git index), guard |
| C-003 | L3 | transition, validation rule |
| C-004 | L2 | interface, dependency |
| C-005 | L2 | component (default) |
| C-006 | L1 | presentation |
| X-001 | L3 | invariant |
| X-002 | L3 | state (git index) |
| A-001 | L3 | state, transition |
| A-002 | L2 | dependency |

Coverage: L1 = 2, L2 = 5, L3 = 5 (all levels have points; the taxonomy coverage gate can pass).

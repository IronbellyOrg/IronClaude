# Round 1 Advocate Statement: Variant B (refactorer)

## Position summary

B is the smallest correct change: one new wave in an existing file, no new files, existing tests stay green unedited (U-006). Its weak spots are real: no timeouts, no behavior tests, an overstated B2 claim, a lookup regex that misses hand-made worktrees, and `--repo path:<T>` from a linked worktree. I argue B's skeleton wins and that A and C each supply fixes B should adopt.

## Steelman of Variant A

A is the only variant that treats Orca as an external system that can hang and be mocked. A script with a fake `orca` on PATH (A s7, U-001) tests argv, reuse and failure behavior, which prose and static greps cannot. A resolves the main checkout via `--git-common-dir` (U-003, verified from a linked worktree), uses a `--comment` marker that survives title edits (U-002), and admits that B2 is stretched by recording decision B16. The repo already has script precedent (`clickup_claim.py`, `origin_repo.py` in `scripts/`).

## Steelman of Variant C

C is the QA discipline: every edge case maps to a test ID (S-004, U-011), the forbidden-flag regex and "unflagged output is byte-identical" are crisp acceptance criteria, and R5 honestly says the B2 reading needs confirming (U-013). Its `worktree.json` gives a cheap exact-match first lookup (U-012).

## Strengths claimed (B)

1. Smallest surface: Wave 7 inside `refs/claim.md`; `tests/skills/test_issue_protocol.py` has a two-way inventory of `refs/*.md` and `scripts/*.py` (line 136), so A's two new files force inventory and SKILL.md table edits (U-006).
2. Never overwrites existing worktree files (U-007), and copies per file, so no nested `<N>/<N>` tree (X-004).
3. Names the upstream-project-id risk (U-008). Verified: `orca worktree list` rows carry `projectId: github:superclaude-org/superclaude_framework`, which CLAUDE.md treats as a hard fork rule.
4. Re-lists after create rather than trusting unverified create JSON (U-009), using list fields read live.
5. Lookup regex tolerates both a configured prefix and Orca's numeric suffix. `orca worktree create --help` states "a taken name gets a numeric suffix", which contradicts A's "create fails" (C-016).
6. Minimal contract (2 fields) and 4 distinct, actionable codes.
7. Explicit "left out on purpose" list (U-010).

## Weaknesses identified in A and C

1. A: new ref plus Python script plus new test file plus B16 plus edits to four design sections is the largest change for a boolean flag. `uv run --no-project python <skill base>/scripts/...` adds an interpreter hop to an LLM-run claim.
2. A: `--name issue-<N>-<slug>` needs slug code (40-char rule) for a key A itself replaces with a marker; the slug is unneeded.
3. A: overwriting same-named files on re-claim destroys user edits to `next-steps.md` (A s6 table row says so).
4. A: matched path gone from disk gives `failed` and no create, leaving the user without a recovery path.
5. C: "Wave 6 stays byte-identical" contradicts `refs/claim.md` Wave 6 step 4 ("Print the `next-steps.md` path and STOP"), so a later Wave 7 never runs (X-001).
6. C: "no primitive carries a version marker" is false; 8 of 47 commands do (X-002).
7. C: `cp -r <D> <wt>/.dev/issues/<N>/` nests on re-copy (X-004, verified), breaking C's own E5/E6.
8. C: `--setup run` forces repo setup hooks (help: "pass --setup run to force them"), a side effect nobody asked for. Omitting `--repo` relies on inference that fails outside a managed worktree, which is exactly where installed `/sc:issue` often runs (A-002).
9. C: a single `W-WORKTREE-FAILED` code cannot distinguish missing Orca from failed copy; `worktree.json` is machine-local state.

## Concessions about Variant B

- No timeouts (C-013); a hung `orca` blocks a claim that already succeeded.
- Static-only tests cannot prove argv or reuse behavior (C-012).
- "B2 stays literally true" is overstated; design doc line 27 says `--claim` "stops after writing the next-step prompt" (X-003).
- Regex and `--branch issue-<N>` miss hand-made `issue-330-ponytail-plugin` style worktrees (A-004).
- `--repo path:<T>` from a linked worktree is unverified (C-002).
- Skip-existing leaves stale copies on re-claim.
- "Several matches: create nothing" leaves no path to print.

## Per-point verdicts

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001 | A | 60% | Script seam is testable and has repo precedent; costs inventory edits |
| S-002 | A/B tie | 90% over C | Both rewrite step 4; C contradicts claim.md |
| S-003 | B | 55% | Table of codes is scannable; trivial |
| S-004 | C | 70% | Edge cases mapped to tests |
| C-001 | A | 55% | Observed prefix `ironbelly/...`; but slug unneeded, so name `issue-<N>` |
| C-002 | A | 75% | `--git-common-dir` verified from linked worktree |
| C-003 | A/B | 70% | Omit `--setup`; repo policy decides |
| C-004 | A | 70% | Marker plus path fallback catches existing `issue-330-...` rows |
| C-005 | A | 60% | Reusing a match gives the user a path |
| C-006 | A | 55% | Archived ignored (B) is right, but a missing path should warn, not recreate |
| C-007 | B | 55% | Destructive overwrite is worse than stale, if a differing-file warning is added |
| C-008 | B | 55% | List fields verified; create JSON not |
| C-009 | B | 65% | `worktree_branch` and `worktree_warning` duplicate printed output |
| C-010 | B | 55% | 4 codes suffice; A's STALE is useful |
| C-011 | B | 55% | Same marker, narrower footprint; C factually wrong |
| C-012 | A | 70% | Fake-orca tests verify behavior |
| C-013 | A | 75% | Only A bounds a hung call |
| C-014 | B | 50% | Equivalent trigger points |
| C-015 | A | 65% | B16 admits B2 is stretched |
| C-016 | B | 60% | Help confirms numeric suffix; regex tolerates it |
| X-001 | A/B | 95% | claim.md step 4 ends the run |
| X-002 | A/B | 95% | Verified 8 versioned commands |
| X-003 | A | 65% | B's "literally true" is overstated |
| X-004 | B | 60% | Per-file copy avoids nesting; C wrong |

## Shared assumptions

- A-001: QUALIFY. Creating a worktree after the prompt is written is an extra action beyond B2's literal text (design doc line 27); amend the design doc and name it infrastructure, not a next-step command.
- A-002: QUALIFY. Installed `/sc:issue` runs in repos Orca may not know; the list call exit code must map to a warn, and `--repo` must not guess.
- A-003: QUALIFY. Add `git rev-parse --verify origin/<B>` before create; on failure warn and skip rather than let Orca fail late offline.
- A-004: REJECT. This repo has `issue-330-ponytail-plugin`, `issue-315-...`, `issue-305-...`; exact-branch lookup (B, C) would duplicate them.
- A-005: QUALIFY. `git check-ignore` on `.dev/issues/<N>/` returned not ignored, so files show as untracked in the new worktree; print the "do not stage" line (D24) every time.

## Proposed merged design

- Structure: B's Wave 7 in `refs/claim.md`, no new ref. Take A's script only if the team accepts the inventory edits; otherwise keep inline (my preference: inline, plus A's 120 s timeout wording).
- Wave 6 step 4 rewritten conditionally (A and B agree).
- Command: `--name issue-<N>`, no `--repo` guess: `--repo path:<main>` from `--git-common-dir` (A); `--base-branch origin/<B>` after verifying the ref; `--no-parent`; `--comment "sc:issue <R>#<N>"`; no `--setup`, no link flags, no agent.
- Lookup: marker first, then path basename `^issue-<N>(-|$)`, then B's branch regex; ignore archived rows; several matches reuse the first marker match and warn (A); missing path warns (A).
- Path from follow-up list (B).
- Copy: per file, skip existing, warn on differing skipped files; never `cp -r` onto an existing dir.
- Codes: B's four plus `W-WORKTREE-STALE`; contract fields `worktree_path`, `worktree_status` only with the flag.
- Version `1.1.0` in `issue.md` only; design doc gets decision B16 (A) with C's R5 caveat.
- Tests: static pins (B, C's forbidden-flag regex and edge-to-test table) plus a fake-`orca` behavior test (A).

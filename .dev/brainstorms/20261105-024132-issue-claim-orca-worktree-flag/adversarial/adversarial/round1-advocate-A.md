# Round 1: Advocate for Variant A (architect)

## Position summary

A's core is right: every Orca call behind one standard-library script that a fake `orca` can test, the main checkout resolved by `--git-common-dir`, a `--comment` marker as the re-claim key, and an honest B2 amendment. A's packaging is wrong: a sixth ref breaks existing tests. A also loses to B on ambiguity, archived rows and copy safety.

## Steelman of Variant B

B is the smallest working change. It adds no new file, so the inventory tests stay as they are (U-006). It re-lists instead of trusting the unverified create JSON (U-009), never overwrites user notes (U-007) and creates nothing on ambiguity. It alone names the upstream `projectId` risk (U-008, verified on all 11 rows).

## Steelman of Variant C

C is the most testable spec: 15 edge cases mapped to test IDs, a forbidden-flag regex and a byte-identical acceptance criterion (U-011). It says the flag dies if the B2 reading is overruled (R5). Its `worktree.json` makes a re-claim one exact read (U-012).

## Strengths claimed

1. **Testable seam (U-001, C-012).** `scripts/clickup_claim.py` already sets the pattern (exit 0 on every outcome, 2 on bad arguments). Static pins cannot catch a wrong argv composed inline by the orchestrator (B, C); a fake `orca` on PATH can.
2. **Repo resolution (C-002, U-003).** `--git-common-dir` was verified from a linked worktree. C omits `--repo`, and Orca's help says it then "infers the repo from the current Orca-managed worktree", the same mapping that tags rows with the upstream id (U-008).
3. **Stable lookup key (C-004, A-004).** `orca worktree list --json` exposes `comment` (verified today). The path fallback `^issue-<N>(-|$)` catches existing hand-made `issue-330-ponytail-plugin`; B's branch regex and C's exact match miss it.
4. **Timeouts (C-013).** Only A bounds Orca calls; a timed-out create that finished is found next run.
5. **B2 honesty (X-003, C-015).** A records decision B16; B's "literally true" is overstated.
6. **Version facts (X-002).** 8 of 47 commands carry `version:`.

## Weaknesses identified in B and C

1. B: `--branch issue-<N>` drops the configured team prefix (Orca help: "without the configured prefix").
2. B: no timeouts; `--show-toplevel` from a linked worktree is UNVERIFIED (B s6).
3. B and C: static pins test instruction text, not the commands that actually run.
4. C: Wave 6 self-contradiction (X-001); `claim.md:90` step 4 STOPs, so a later Wave 7 never runs.
5. C: `cp -r` re-copy nests at `.dev/issues/<N>/<N>/` (X-004, verified).
6. C: wrong on version markers (X-002); forces `--setup run` without evidence (C-003).
7. C: one warning code (C-010) cannot tell "Orca missing" from "copy failed".

## Concessions about Variant A

1. A new `refs/worktree.md` breaks `test_all_five_refs_exist` (`tests/skills/test_issue_protocol.py:165`) and must carry the spawn-rule text (line 147). B's placement is cheaper; the script alone gives the seam.
2. Reusing the first of several matches is riskier than B's "warn, create nothing".
3. A ignores `isArchived`; B handles it.
4. Overwriting on re-claim can clobber user notes.
5. A reads the create JSON first, but its fields are UNVERIFIED. The list JSON is nested under `result.worktrees` (verified); every parser must handle that.
6. The slug adds code; once the marker is the key, the name matters less.

## Per-point verdicts

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001 | A script + B placement | 65% | U-001; ref count pinned at test line 165 |
| S-002 | A = B | 90% | C's placement never runs (X-001) |
| S-003 | B | 55% | code table scans fastest |
| S-004 | C | 75% | rows mapped to tests |
| C-001 | A | 55% | keeps Orca's prefix |
| C-002 | A | 85% | verified common-dir; inference risk U-008 |
| C-003 | A = B (omit) | 60% | `--setup run` unverified (C R2) |
| C-004 | A | 70% | `comment` field verified; A-004 |
| C-005 | B | 60% | ambiguity should not guess |
| C-006 | B | 55% | handles `isArchived` |
| C-007 | B | 55% | protects notes; C nests (X-004) |
| C-008 | B | 60% | create JSON unverified |
| C-009 | A | 60% | `warning` field visible to callers |
| C-010 | A | 55% | distinct remedies |
| C-011 | A = B | 90% | X-002 census |
| C-012 | A | 75% | fake-`orca` behavior test |
| C-013 | A | 80% | only bounded design |
| C-014 | Tie | 50% | equivalent |
| C-015 | A | 65% | B2 text (X-003) |
| C-016 | C | 50% | records the renamed branch |
| X-001 | A = B | 95% | `claim.md:90` STOP |
| X-002 | A = B | 95% | 8 of 47 verified |
| X-003 | A | 75% | B2 names the stop point |
| X-004 | A = B | 90% | nesting verified |

## Shared assumption responses

- **A-001: QUALIFY.** B2 says the claim "stops after writing the next-step prompt"; a worktree fits only with a decision row amending B2, else the flag dies (C R5).
- **A-002: QUALIFY.** The command runs in other projects; an unregistered repo must surface as a list-failure warning, which the first `--repo path:<main>` list call yields. The upstream-id mapping (U-008) stays UNVERIFIED.
- **A-003: QUALIFY.** The Wave 1 fetch can fail offline; run `git rev-parse --verify origin/<B>` before create and warn on failure.
- **A-004: REJECT.** Hand-made `issue-330-ponytail-plugin` and `issue-315-ccsession-name-prompt` exist today; a path-basename fallback is required.
- **A-005: QUALIFY.** `git check-ignore` shows `.dev/issues/` is not ignored, so the copy appears in the worktree's `git status`; print a "untracked, do not stage (D24)" line.

## Proposed merged design

- Shared shape: boolean, claim-only, `E-CLAIM-ONLY-FLAG`, no agent, no link flag.
- Wave 7 in `refs/claim.md`, Wave 6 step 4 made conditional (A = B); no new ref.
- A's `scripts/orca_worktree.py`, listed in SKILL.md: 120 s per call, exit 0 or 2, one JSON line, fake-`orca` tests.
- `--repo path:<main>` via `--git-common-dir` (A); no `--setup`; check C's R2 on the manual run.
- `--name issue-<N>`, no `--branch`, so the prefix stays.
- Lookup: A's marker, then A's path fallback, skipping `isArchived` (B); several matches warn and create nothing (B).
- Path after create from a marker re-list (B); create JSON secondary.
- Copy: skip existing files (B), name each skipped file that differs from `<D>`; never a bare `cp -r`.
- Contract: A's four fields; A's codes plus `W-WORKTREE-AMBIGUOUS`; C's remedy line.
- Tests: C's edge-case map and forbidden-flag regex, A's fake-`orca` tests, byte-identical unflagged run.
- Docs: `version: "1.1.0"` plus decision B16 amending B2.

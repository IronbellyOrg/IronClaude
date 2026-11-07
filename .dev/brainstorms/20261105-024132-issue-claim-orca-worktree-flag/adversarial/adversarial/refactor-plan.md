# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (opus:architect), `variant-1-opus-architect.md`
- Incorporating strengths from: Variant B (sonnet:refactorer), Variant C (haiku:qa), the Round 2 rebuttals, and the Round 2.5 invariant probe (`invariant-probe.md`)
- Planned changes: 16
- Risk level: Medium overall (several rules replace A's text; each is evidence-backed)
- Notation: `<R>` = origin repo `owner/repo`, `<N>` = issue number, `<B>` = default branch, `<D>` = `.dev/issues/<N>/`, `<main>` = main checkout. The merged document must define these once at its start (fixes A Clarity 4).

## Planned Changes

### Change 1: No new ref; Wave 7 lives in `refs/claim.md` (from Variant B)
- **Source**: B s1, s5, s8; test file lines 131 and 165 (checked by the orchestrator)
- **Target**: A s1, s5, s8 (replace)
- **Rationale**: S-001 won 3 of 3 for a script plus claim.md placement; a new `refs/worktree.md` breaks `test_all_five_refs_exist` and needs the spawn-rule line; the script needs one row in the `SKILL.md` files table only.
- **Integration point**: s5 "Wave 7 (in `refs/claim.md`)"; s8 lists `scripts/orca_worktree.py` and its SKILL.md row; remove `refs/worktree.md`.
- **Risk**: Low. Undoable by moving the text into a ref and updating two tests.

### Change 2: Name `issue-<N>`, no slug, no `--branch` (from the Round 2 majority)
- **Source**: C-001 (A, B and the merged designs of A and B advocates); Round 2 O4, 3 of 3
- **Target**: A 2.3 and s4 argv (replace)
- **Rationale**: marker is unverified so the basename fallback carries re-claims and needs a stable slug-free prefix; live `issue-305/315/330/384-*` rows fit `^issue-<N>(-|$)`.
- **Integration point**: argv becomes `orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json`. Remove the 40-character slug rule.
- **Risk**: Low

### Change 3: Lookup keys and match rules (from A, B, C, INV-002, INV-004)
- **Source**: C-004, C-005, C-006; Round 2 O1, O5; INV-002, INV-004
- **Target**: A 2.5 and s6 rows "Several matches", "Matched path gone" (replace)
- **Rationale**: Round 2 unanimous on stale stop (80%, 75%, 75%), marker then path then basename, then branch tail.
- **Integration point**: Drop archived rows. Keys in order: (1) `comment` contains `sc:issue <R>#<N>`; (2) the path in `<D>/worktree.json`, guarded; (3) path basename `^issue-<N>(-|$)`; (4) last `/`-separated segment of the branch ref, same pattern. Deduplicate hits by row `id`. The first key with at least one hit decides. A hit whose path is missing on disk is STALE. At least one live hit: reuse it (first by list order), name stale hits in the output. Stale hits only: `W-WORKTREE-STALE`, no create, print path, branch and remedy. Two or more live hits in the deciding key: `W-WORKTREE-AMBIGUOUS`, no create, list all paths.
- **Risk**: Medium (new logic; covered by fake-orca cases FO-2, FO-3, FO-8, FO-10, FO-13)

### Change 4: List completeness and empty-list guards (from INV-001, B Round 2)
- **Source**: INV-001; B Round 2 O7.2
- **Target**: A s4 and s5 (insert)
- **Rationale**: truncated or partial pages create duplicates; the list JSON has `ok`, `result.truncated`, `result.totalCount`, `result.hostScope.omittedHostIds`.
- **Integration point**: `ok != true`, `truncated == true`, a non-empty `omittedHostIds`, zero rows, or no `isMainWorktree` row: `W-ORCA-LIST-FAILED`, create nothing, report the counts. Same check on the after-create list.
- **Risk**: Low

### Change 5: New path after create (from B, INV-003, INV-011)
- **Source**: B s5 step 4; B Round 2 O7.1; INV-003, INV-011
- **Target**: A s5 step 3 (replace "takes path and branch from the create JSON")
- **Rationale**: create JSON shape UNVERIFIED; marker may stay empty.
- **Integration point**: snapshot row ids before create; after create (or after a timeout, one re-list) take the set difference. Exactly one new id whose basename fits `^issue-<N>(-|$)` gives `created`. Zero gives `failed` with `W-WORKTREE-CREATE-FAILED` "created but not listed". Two or more gives `W-WORKTREE-AMBIGUOUS`, no copy, no record. The create JSON is read only as a secondary source.
- **Risk**: Medium

### Change 6: Copy rule (from B, A, C; X-004; INV-005; INV-010)
- **Source**: C-007; Round 2 O3 (3 of 3); INV-005, INV-010
- **Target**: A 2.4 and s6 row "edited by the user" (replace)
- **Rationale**: overwrite destroys user edits (B), skip leaves stale commands (C), `cp -r` nests (X-004, verified), tracked files exist on `origin/<B>` (INV-005, verified `.dev/issues/433/`).
- **Integration point**: walk `<D>` including `analysis/`; never `cp -r`. For each file: tracked in the worktree (`git -C <wt> ls-files .dev/issues/<N>`): skip and name it in `W-WORKTREE-COPY-FAILED`. Missing: copy. Identical: skip. Differing untracked: rename the existing file to one `<name>.prev` (replacing any older `.prev`), copy, name it in the warning. Skip the whole copy when `realpath(source) == realpath(destination)`. Exclude `worktree.json`. Print "untracked, do not stage (D24)" only when no copied path is tracked.
- **Risk**: Medium

### Change 7: Record file owned by the script (from C, A; Round 2 O2 2 of 3)
- **Source**: C-004, U-012; Round 2 O2 (A 65%, C 65% include; B 65% exclude)
- **Target**: A s5 step 2 (replace "write stdout to `<D>/worktree.json`")
- **Rationale**: keeps reuse working when the Orca list call fails; B's drift objection is bounded by the guard. A's text wrote stdout, including failures, over a good record.
- **Integration point**: `scripts/orca_worktree.py` writes `<D>/worktree.json` (`{"path": "<absolute>"}` plus status) only on `created` or `reused`. Guard before use: the path exists and its git-common-dir equals `<main>`'s, compared with `realpath`. A record hit while the list call failed is reused with the warning "reused from record, unverified". Dissent recorded: B excludes the record.
- **Risk**: Medium

### Change 8: Base ref checks (from INV-009)
- **Source**: INV-009; A-003
- **Target**: A s5 step 3 (insert)
- **Rationale**: the Wave 1 fetch result is not visible to Wave 7.
- **Integration point**: the script runs `git fetch origin` (origin only, 120 s) then `git rev-parse --verify origin/<B>`. Missing ref: `W-ORIGIN-BASE-MISSING`, no create. Fetch failed but ref exists: `W-ORIGIN-BASE-STALE`, continue.
- **Risk**: Low

### Change 9: Post-condition before success (from INV-016)
- **Source**: INV-016
- **Target**: A FR list and s5 (insert)
- **Rationale**: sufficiency challenge; "created" must mean usable.
- **Integration point**: before `created` or `reused` the script checks the path exists, its git-common-dir equals `<main>`'s, and every copied file is byte-identical at the destination (or skipped as tracked or kept as differing with a warning). Otherwise `failed` with a named warning.
- **Risk**: Low

### Change 10: Return contract and warning codes (from A, B, C, INV-007)
- **Source**: C-009, C-010; INV-007
- **Target**: A s4 (replace)
- **Integration point**: contract fields only with the flag: `worktree_status` (created|reused|skipped|failed), `worktree_path`, `worktree_branch`, `worktree_match_key` (marker|record|basename|branch|null), `worktree_warning`. Codes: `W-ORCA-MISSING`, `W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-ORIGIN-BASE-STALE`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED` (drop A's `W-WORKTREE-MULTIPLE`). On a basename or branch key, print "reused a worktree not created by /sc:issue". Failure prints a remedy line (from C).
- **Risk**: Low

### Change 11: Tests (from A, C, B Round 2)
- **Source**: C-012, S-004, U-011; C Round 2 O7; B Round 2 O7.3
- **Target**: A s7 (replace)
- **Integration point**: A's fake-`orca` suite as the core, fixtures copied from the real list shape (nested `result.worktrees`, full-ref branches, path and branch that differ, a stale row, a tracked-file case, a truncated list); C's static pins ST-1..ST-6 (flag gates, forbidden-flag regex over argv, exact argv, inventory, version and decision, Wave 7 after steps 1-3); fake-orca cases FO-1..FO-17 as C listed them, adjusted to Changes 3 to 9; observed runs OB-1..OB-4 plus C's "unflagged output byte-identical" acceptance criterion. Edge-case table maps each case to a test ID.
- **Risk**: Low

### Change 12: Design-doc decision wording (from A, C R5; X-003)
- **Source**: C-015, X-003 (A wins 3 of 3)
- **Target**: A 2.7 and s8 (replace "B16")
- **Integration point**: B16 records that creating a worktree after `next-steps.md` is an addition to B2 ("stops after writing the next-step prompt"), allowed only because no next-step command runs; states the owner must confirm this reading (C R5), and that without confirmation the flag is withdrawn. Never write "B2 stays literally true".
- **Risk**: Medium (needs owner confirmation)

### Change 13: Risks with ratings, out-of-scope list, FR wording (from B, A, scoring defects)
- **Source**: scoring Clarity 1, Correctness 4, Risk 1; U-008, U-010
- **Target**: A s3, s9 (replace)
- **Integration point**: FR-8 becomes "MUST exist unless `W-WORKTREE-COPY-FAILED` names the reason"; FR-4 says "only after both comments are posted"; "first match" replaced by Change 3's ordering. Section 9 rates each risk (likelihood, impact), adds the upstream project-id risk (all 11 rows of this repo carry `github:superclaude-org/superclaude_framework`; no link flag is passed; verify on the manual run) and an out-of-scope list (agent launch, `--worktree <name>`, dry-run, auto-removal, `--setup`, `--branch`, lock file, `linkedIssue` matching).
- **Risk**: Low

### Change 14: Manual-run verification list (from C and B Round 2 O5)
- **Source**: C Round 2 O5; B Round 2 O5
- **Target**: A s7 AC-1 (extend)
- **Integration point**: one observed run records: `comment` after create (load-bearing unknown), actual basename and branch with prefix, create JSON shape, suffix on a taken name, second claim `reused` with unchanged row count, `projectId`, `.claude/` present or not (print `make sync-dev` hint if not), no `linkedIssue`/`linkedPR`, unflagged claim byte-identical.
- **Risk**: Low

### Change 15: Accepted risks recorded, not built (INV-006, INV-008)
- **Source**: invariant probe
- **Target**: A s9 (insert)
- **Integration point**: INV-006 (`linkedIssue` as a key) is not built: Orca resolves this repo to the upstream project, so its issue numbers may not be this fork's; INV-008 (lock for racing claims) is not built: a single user, low likelihood; a race leaves two live hits and the next claim stops with `W-WORKTREE-AMBIGUOUS` and lists them.
- **Risk**: Low

### Change 16: Edge-case table merge (from A s6, C s6)
- **Source**: S-004
- **Target**: A s6 (extend)
- **Integration point**: keep A's 11 rows, update for Changes 3 to 9, add C's E-rows not already covered (record deleted, deleted worktree, claim from another worktree, unflagged claim after a flagged one, orca daemon down, wrong repo inferred, E-POST-FAILED), each with its test ID.
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-003 | C: `--setup run` | Round 1: A, B, C-advocate all chose to omit; no evidence it helps (C R2); help says it forces hooks |
| C-001 | C: `--branch issue-<N>` | Majority 2 of 3 keep Orca's prefix; branch key is the weaker key (path and branch diverge on live rows) |
| C-002 | C: omit `--repo`; B: `path:<T>` | `--git-common-dir` verified from a linked worktree; inference is the upstream-id risk |
| X-004 | C: `cp -r` | Verified to nest on re-claim |
| C-011, X-002 | C: no version marker | 8 of 47 commands carry `version:` |
| C-010 | C: one warning code | Cannot route remedies (3 of 3) |
| C-009 | A: four fields only | Replaced by a five-field contract (Change 10) |
| C-006 | B/C Round 1: create fresh when path is missing | Conceded by B and C in Round 2: the branch stays registered, a second row locks later claims |
| C-007 | B: skip existing; A: overwrite | Replaced by Change 6 |
| S-001 | A: new `refs/worktree.md` | Breaks `test_all_five_refs_exist` |
| INV-006 | `linkedIssue` key | Change 15 |
| INV-008 | lock file | Change 15 |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 3 | Medium | Wrong reuse or a duplicate worktree | Revert to marker-only lookup |
| 5 | Medium | Path undefined after create | Fall back to parsing create JSON once its shape is verified |
| 6 | Medium | A user file renamed or skipped wrongly | Revert to skip-existing (B) |
| 7 | Medium | Stale record reused | Drop the record (B's position) |
| 12 | Medium | Owner rejects the B2 reading | Withdraw the flag |
| 1, 2, 4, 8-11, 13-16 | Low | Local to text or tests | Revert the section |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-05T03:58:00+00:00
- Reviewer note: this plan was drafted by the orchestrator; the independent review step was not run as a separate agent (the invariant probe and the three advocates served as the adversarial check).

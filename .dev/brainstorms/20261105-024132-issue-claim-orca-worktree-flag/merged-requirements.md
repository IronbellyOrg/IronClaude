---
domain: code
strategy: systematic
status: draft requirements, not implemented
base: variant-1-opus-architect
generated: 2026-11-05
---
<!-- Provenance: base Variant A (variant-1-opus-architect), chosen by tiebreak -->
<!-- Merged: Variants B and C, Round 2 rebuttals, invariant probe -->
<!-- Plan: refactor-plan.md Changes 1-16; log: merge-log.md -->

# Spec: /sc:issue --claim --worktree

**Notation.** `<R>` is the origin repo `owner/repo` printed by `scripts/origin_repo.py`. `<N>` is the issue number. `<B>` is the default branch found in Wave 0. `<D>` is `.dev/issues/<N>/` in the checkout where the claim runs. `<main>` is the main checkout, the parent of the absolute git-common-dir, so a linked worktree still names it. `<wt>` is the issue worktree's absolute path.
<!-- Source: Round 2 / plan Notation - merged per Change #1 -->

## 1. Summary

<!-- Source: Base (original, modified) - Changes #1, #2 -->
`/sc:issue --claim <N> --worktree` runs today's claim (Waves 0-6), then a new Wave 7 in `refs/claim.md` that creates one Orca-managed worktree for the issue or reuses an earlier one. One standard-library script, `scripts/orca_worktree.py`, makes every Orca and git call behind a unit-tested seam; no ref file is added. The worktree is named `issue-<N>`, gets no agent and no Orca link flag, uses `--no-parent` and base `origin/<B>`, and receives a copy of `<D>`. Every Orca problem is a warning; the claim never fails because of Wave 7. Without `--worktree` nothing changes.

## 2. Decisions on the open questions

### 2.1 Worktree only, or also launch an agent?

<!-- Source: Base (original, modified) - B2 wording, Change #12 -->
- **Decision:** worktree only; no agent starts.
- **Why:** B2 (`docs/designs/sc-issue-command.md:27`) says the claim "stops after writing the next-step prompt". A worktree runs no next-step command, but it is still an action after that point, so the flag is an addition to B2 that needs owner confirmation (2.7). Refactor decision D3 also creates worktrees without an agent. Whether Orca's agent prompt delivers a slash command is UNVERIFIED.
- **Rejected:** `--launch` (start Claude on the first next step): breaks B2 and needs a tier-to-model mapping.

### 2.2 Flag name and shape

<!-- Source: Base (original) -->
- **Decision:** one boolean flag, `--worktree`, claim only, no value.
- **Why:** it names the outcome, not the vendor; with no value the lookup key is always derived.
- **Rejected:** `--orca` (names a tool); `--worktree [name]` (ambiguous to parse, defeats the lookup).

### 2.3 Worktree name, branch, base ref, lineage

<!-- Source: Base (original, modified) - Change #2 -->
- **Decision:** `--name issue-<N>`; Orca picks the branch with its configured prefix (observed: `bare-python-hook-357` is on `ironbelly/bare-python-hook-357`). Base `origin/<B>` (FR-16), `--no-parent`, `--repo path:<main>`. Exact argv: section 4.
- **Why:** the marker is UNVERIFIED, so the basename key carries re-claims and needs a stable prefix without title text; live `issue-305/315/330/384-*` rows fit `^issue-<N>(-|$)`. Issue work does not belong to the worktree the claim ran in.
- **Rejected:** a title-derived name suffix (unstable key); an explicit branch name (drops the team prefix).

### 2.4 How the worktree gets `.dev/issues/<N>/`

<!-- Source: Variant B, Section 2.4 - merged per Change #6 -->
- **Decision:** walk every file of `<D>`, including `analysis/`, into `<wt>/.dev/issues/<N>/`, never as one recursive directory copy. Skip the whole copy when source and destination share a `realpath`. Exclude `worktree.json`. Per file:
  - tracked in the worktree (tracked-file check, section 4): skip, name it in `W-WORKTREE-COPY-FAILED`;
  - missing: copy; identical: skip;
  - differing and untracked: rename the existing file to `<name>.prev` (replacing any older `.prev`), copy, name it in `W-WORKTREE-COPY-FAILED`.
- Print "untracked, do not stage (D24)" only when no file under `<wt>/.dev/issues/<N>/` is tracked.
- **Why:** repo-relative `@.dev/issues/<N>/...` paths resolve unchanged. Overwrite loses user edits; skip keeps stale commands; a recursive copy nests (X-004); `origin/<B>` tracks `.dev/issues/433/` files (INV-005).
- **Rejected:** symlink; absolute-path rewrite.

### 2.5 Duplicate detection on re-claim

<!-- Source: Base (original, modified) - Changes #3, #7 -->
- **Decision:** list the repo's worktrees (section 4), drop archived rows, then try keys in order:
  1. **marker:** `comment` contains `sc:issue <R>#<N>` not followed by a digit;
  2. **record:** the path in `<D>/worktree.json`, passing the record guard, matched to a row by `realpath`;
  3. **basename:** the row's `path` basename matches `^issue-<N>(-|$)`;
  4. **branch:** the last `/`-separated segment of the row's `branch` matches the same pattern.
- Hits are deduplicated by row `id`; the first key with a hit decides. A hit whose path is missing on disk is stale. Within that key: exactly one live hit is reused, stale hits named; stale hits only give `W-WORKTREE-STALE`; two or more live hits give `W-WORKTREE-AMBIGUOUS` listing all paths. Neither creates.
- **Record guard:** the path exists and its git-common-dir equals `<main>`'s, compared by `realpath`.
- Every create passes the marker as `--comment`, plain metadata, not a link flag.
- **Why:** all 15 live rows show `comment: ""`, so marker filling is UNVERIFIED (AC-1); live branches are prefixed (INV-002); the record keeps reuse working while Orca is down.
- **Dissent:** Advocate B excludes the record (65%): it can drift from Orca and holds a machine-local path. A and C keep it; the guard and the "unverified" warning bound the drift.

### 2.6 Model, effort and tier line for a launched agent

<!-- Source: Base (original, modified) - flag literal removed -->
- **Decision:** none; the user runs `next-steps.md`'s `/model` line in a session opened in the worktree.
- **Rejected:** passing a tier model to Orca; picker-ID support is UNVERIFIED.

### 2.7 Version marker and design-doc decision

<!-- Source: Base (original, modified) - Change #12 -->
- **Decision:** `version: "1.1.0"` in `commands/issue.md` only (8 of 47 commands carry one, X-002). New design decision B16 records that creating a worktree after `next-steps.md` is an addition to B2 ("`--claim` stops after writing the next-step prompt"), allowed only because no next-step command runs. **Owner confirmed this reading on 2026-11-05**, so the flag stays. The owner is also open to loosening B2 further (stop at an approved plan, or run the full pipeline); that is not part of this spec and needs its own decision.
- **Rejected:** a second command; claiming B2 is untouched (X-003).

### 2.8 Alternatives rejected in the debate

<!-- Source: plan "Changes NOT Being Made" -->
| Point | Alternative | Why not |
|---|---|---|
| C-003 | C: run setup hooks | no evidence; forbidden (FR-6) |
| C-001 | B, C: explicit branch | 2 of 3 keep Orca's prefix |
| C-002 | C: no `--repo`; B: toplevel | common-dir verified |
| X-004 | C: recursive copy | nests |
| C-011 | C: no version | 8 commands carry one |
| C-010 | C: one warning code | cannot route remedies |
| C-009 | A: four fields | five (section 4) |
| C-006 | B, C: create fresh on a missing path | conceded in Round 2 |
| C-007 | A: overwrite; B: skip | replaced by 2.4 |
| S-001 | A: a sixth ref file | breaks `test_all_five_refs_exist` |
| INV-006, INV-008 | `linkedIssue` key; lock | section 9 |

## 3. Functional requirements

<!-- Source: Base (original, modified) - Changes #1, #3, #13 -->
- **FR-1** The Options table MUST gain one row: `--worktree`, mode `claim`, default off, no value.
- **FR-2** `--worktree` with `--create` MUST STOP `E-CLAIM-ONLY-FLAG` before Activation, with no external call.
- **FR-3** Without `--worktree`, no `orca` command runs and output, files and return contract MUST be byte-identical to today's.
- **FR-4** Wave 7 MUST run only after both Wave 6 comments are posted; any STOP in Waves 0-6, including `E-POST-FAILED`, means no Orca call.
- **FR-5** Every Orca and git call of Wave 7 MUST be made by `scripts/orca_worktree.py`.
- **FR-6** The list and create calls MUST equal section 4 exactly. **Forbidden list**, never passed: link flags `--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, and `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`.
- **FR-7** A lookup that ends in reuse, stale or ambiguous MUST NOT call `orca worktree create`.
- **FR-8** After `created` or `reused`, `<wt>/.dev/issues/<N>/next-steps.md` and `issue-summary.md` MUST exist unless `W-WORKTREE-COPY-FAILED` names the reason.
- **FR-9** The script MUST exit 0 for every runtime outcome with one JSON object, and 2 only for bad arguments (the `clickup_claim.py` pattern).
- **FR-10** Any Orca, git or copy problem MUST yield a section 4 warning with claim `status: success`.
- **FR-11** Worktree contract fields MUST print only with `--worktree`.
- **FR-12** Wave 7 MUST NOT stage, commit, push, run `git worktree add`, use `EnterWorktree`, or run `orca worktree rm`.
- **FR-13** The output SHOULD print the worktree path and "open it and run `.dev/issues/<N>/next-steps.md` there".
- **FR-14** Installed primitives MUST call `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path.
- **FR-15** A list result is unusable when `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` is non-empty, it has zero rows, or no row has `isMainWorktree: true`: `W-ORCA-LIST-FAILED`, no create, counts reported. This MUST apply to the after-create list too. <!-- Source: Round 2 / INV-001 - merged per Change #4 -->
- **FR-16** Before a create, the script MUST fetch and verify `origin/<B>` (section 4). Missing ref: `W-ORIGIN-BASE-MISSING`, no create. Fetch failed, ref present: `W-ORIGIN-BASE-STALE`, continue. <!-- Source: Round 2 / INV-009 - merged per Change #8 -->
- **FR-17** Before `created` or `reused`, the script MUST check that `<wt>` exists, its git-common-dir equals `<main>`'s by `realpath`, and every `<D>` file is byte-identical at the destination or named in a warning (tracked or `.prev`); else `failed` with a named warning. <!-- Source: Round 2 / INV-016 - merged per Change #9 -->
- **FR-18** Only the script writes `<D>/worktree.json` (`{"path": "<absolute>", "status": "created|reused"}`), only on `created` or `reused`; it MUST pass the record guard before use and is never copied. <!-- Source: Variant C, Section Q5 - merged per Change #7 -->
- **FR-19** The copy MUST follow 2.4. <!-- Source: Variant B, Section 2.4 - merged per Change #6 -->
- **FR-20** The new worktree's path MUST come from the row-id set difference (section 5), not from the create JSON. <!-- Source: Variant B, Section 5 - merged per Change #5 -->

## 4. Flag contract, commands and warning codes

<!-- Source: Base (original) -->
Valid: `--claim <N> --worktree`. `--create ... --worktree` STOPs `E-CLAIM-ONLY-FLAG` ("--worktree applies to --claim only"); `--worktree` alone, or with a value, prints the usage block; `--claim --worktree --depth` hits `E-CREATE-ONLY-FLAG` first.

<!-- Source: Base (original, modified) - Changes #2, #6, #8 -->
The skill's only call (Wave 7), then every command the script runs, each with a 120-second timeout:

```text
uv run --no-project python "<skill base>/scripts/orca_worktree.py" --repo <R> --number <N> --base origin/<B> --source <D>

git rev-parse --path-format=absolute --git-common-dir
git fetch origin
git rev-parse --verify origin/<B>
orca worktree list --repo path:<main> --limit 500 --json
orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json
git -C <wt> rev-parse --path-format=absolute --git-common-dir
git -C <wt> ls-files .dev/issues/<N>
```

The last line is the tracked-file check. The script prints `{status, path, branch, match_key, warning, detail}`.

<!-- Source: Base (original, modified) - Change #10 -->
Return-contract additions, only with `--worktree`:

```yaml
worktree_status: created | reused | skipped | failed
worktree_path: <absolute path or null>
worktree_branch: <branch or null>
worktree_match_key: marker | record | basename | branch | null
worktree_warning: <W- code or null>
```

`skipped`: a precondition was missing, nothing attempted. `failed`: a worktree was attempted or found but is not usable. On key `basename` or `branch` the output adds "reused a worktree not created by /sc:issue".

<!-- Source: Base (original, modified) - Change #10; remedy column from Variant C, Section 4 -->
| Code | Status | When | Remedy line |
|---|---|---|---|
| `W-ORCA-MISSING` | skipped | `orca` not on PATH | install or start Orca, re-run |
| `W-ORCA-LIST-FAILED` | skipped, or reused from record ("unverified") | list fails, times out, or fails FR-15 | start Orca, re-run |
| `W-ORIGIN-BASE-MISSING` | skipped | `origin/<B>` does not resolve | `git fetch origin`, re-run |
| `W-ORIGIN-BASE-STALE` | created | fetch failed, ref present | `git fetch origin`, rebase in `<wt>` |
| `W-WORKTREE-CREATE-FAILED` | failed | nonzero exit (first stderr line), or "created but not listed"; never auto-retried | re-run; a finished create is reused |
| `W-WORKTREE-AMBIGUOUS` | failed | two or more live hits, or two or more new ids | remove the extras, re-run |
| `W-WORKTREE-STALE` | failed | stale hits only, or wrong git-common-dir | `git worktree prune`, then `orca worktree rm` |
| `W-WORKTREE-COPY-FAILED` | created or reused; failed on a copy error | files skipped as tracked, kept as `.prev`, or not copied | copy the named files by hand |

## 5. Procedure

<!-- Source: Base (original, modified) - Change #1 -->
`refs/claim.md` Wave 6 step 4 becomes: without `--worktree`, print the `next-steps.md` path and STOP (today's text); with it, run Wave 7 (orchestrator, no worker):

1. Run the script call of section 4; read its JSON from stdout.
2. Print the `next-steps.md` path, `Worktree: <path>`, the FR-13 line, the 2.4 "untracked" line when it applies, any warning with its remedy, and the contract fields. If `<wt>/.claude/` is absent, SHOULD add "run `make sync-dev` there first". STOP.

<!-- Source: Base (original, modified) - Changes #3, #4, #5, #7, #8, #9 -->
The script:

1. `orca` not on PATH: `skipped`, `W-ORCA-MISSING`.
2. Resolve `<main>`.
3. List; apply FR-15. On failure, a record that passes its guard is `reused` (key `record`, "unverified", go to step 6); otherwise `skipped`.
4. Look up by 2.5. Reuse goes to step 6; stale or ambiguous ends with `failed`.
5. No hit: apply FR-16, keep the row ids from step 3, create. On exit 0 or a timeout, list once more (FR-15) and diff the row ids. Exactly one new id with basename `^issue-<N>(-|$)`: `created`. Zero: `failed`, `W-WORKTREE-CREATE-FAILED` "created but not listed". Two or more: `failed`, `W-WORKTREE-AMBIGUOUS`, no copy, no record. Nonzero exit: `failed`, `W-WORKTREE-CREATE-FAILED`.
6. Copy (2.4). 7. Check FR-17. 8. Write the record (FR-18); print the JSON.

**Idempotency:** a second claim finds the row by one of the four keys, reports `reused`, and refreshes only the copy; a create that timed out but finished is found by the re-list or the next claim. **Fail-open:** no outcome changes `status` or undoes Waves 3-6.

## 6. Edge cases and failure modes

<!-- Source: Base (original, modified) - empty-name row dropped (Change #2); Variant C, Section 6 rows merged per Change #16 -->
| Case | Behavior | Test |
|---|---|---|
| `orca` not installed | `skipped`, `W-ORCA-MISSING` | FO-5 |
| Daemon down; list fails or hangs | `W-ORCA-LIST-FAILED`; guarded record reused "unverified" | FO-1, FO-6 |
| List empty, truncated, host omitted, no main row | `W-ORCA-LIST-FAILED`, no create | FO-12 |
| Create fails or times out | one re-list, else `W-WORKTREE-CREATE-FAILED` | FO-6, FO-11 |
| 0 or 2+ new ids after create | create-failed or ambiguous; no copy, no record | FO-11 |
| Name taken, Orca suffix (UNVERIFIED) | `issue-<N>-2` matches; `created` | FO-4 |
| One live hit; record deleted | `reused` by the first key that hits | FO-2, FO-3 |
| Two or more live hits in the deciding key | `W-WORKTREE-AMBIGUOUS`, no create, all paths listed | FO-8 |
| Two keys hit different rows | the first key decides; its single live hit is reused | FO-8 |
| Stale hits only (worktree deleted) | `W-WORKTREE-STALE`, no create | FO-10 |
| One live, one stale | reuse live, name stale | FO-10 |
| Archived rows only | ignored; create | FO-9 |
| Prefixed branch; path and branch differ | branch key on last segment | FO-13 |
| `origin/<B>` missing, or fetch fails | base-missing, no create; or base-stale, create | FO-17 |
| Claim from a linked worktree | same `<main>`; flat lineage | OB-4 |
| Claim inside the issue worktree | same real path, copy skipped | FO-15 |
| Wrong repo inferred by Orca | not inferred: `--repo path:<main>` is explicit; the upstream project-id exposure is risk R7 | ST-3, OB-1 |
| STOP before both comments, or `E-POST-FAILED` | no Orca call | ST-6 |
| Unflagged claim after a flagged one | byte-identical, no new fields | OB-3 |
| User edited a worktree file; file tracked there | `.prev` kept, warning; tracked skipped, no "untracked" line | FO-14 |
| Copy error or byte mismatch | `failed`, `W-WORKTREE-COPY-FAILED` | FO-7 |
| `worktree.json` in `<D>` | never copied | FO-16 |

## 7. Test plan and acceptance criteria

<!-- Source: Base (original, modified) - Change #11, IDs from Round 2 / C O7 -->
**Static pins** (`tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`): ST-1 claim-only gate, both STOPs; ST-2 no FR-6 forbidden flag in skill, refs, command or script argv; ST-3 exact section 4 argv; ST-4 still five refs (test line 165 unchanged), script in the `SKILL.md` files table (line 131); ST-5 `version: "1.1.0"` and B16; ST-6 Wave 7 after Wave 6 steps 1-3.

**Fake-`orca` cases** (`tests/skills/test_issue_orca_worktree.py`, new; fixtures copied from the real list: nested `result.worktrees`, prefixed full-ref branches, diverging path and branch, a stale row, a tracked file, a truncated page; expected results in section 6): FO-1 record reuse while list fails; FO-2 marker; FO-3 empty marker, basename; FO-4 suffix; FO-5 no `orca`, bad arguments exit 2; FO-6 hang at 120 s; FO-7 copy error; FO-8 ambiguity; FO-9 archived; FO-10 stale; FO-11 opaque create JSON, 0 or 2 new ids; FO-12 unusable list; FO-13 real shapes; FO-14 `.prev` and tracked; FO-15 self-copy; FO-16 record excluded; FO-17 base ref.

**Observed runs**, once, on a test issue: OB-1 flagged claim; OB-2 repeat; OB-3 unflagged; OB-4 from a linked worktree.

<!-- Source: Base (original, modified) - AC-1 per Change #14; AC-4 per Variant C -->
- **AC-1** (OB-1) One new row under Orca's default location (today `/home/coder/workspaces/worktrees/IronClaude/`); there, `git merge-base HEAD origin/<B>` equals `git rev-parse origin/<B>`. Record: `comment` after create (the load-bearing unknown), basename, branch with prefix, create JSON shape, suffix on a taken name, `projectId`, `<wt>/.claude/` present or not, `linkedIssue` and `linkedPR` empty.
- **AC-2** (OB-1) A Claude session opened in `<wt>` reads `@.dev/issues/<N>/next-steps.md`.
- **AC-3** (OB-2) No new row; `reused`.
- **AC-4** (OB-3) Output and `<D>` byte-identical to a pre-change run; no `orca` call.
- **AC-5** (FO-5) Without `orca`, the claim succeeds with `W-ORCA-MISSING`.
- **AC-6** (ST-1) `--create "x" --worktree` STOPs `E-CLAIM-ONLY-FLAG`, no `gh` call.
- **AC-7** (OB-4) Same `<main>`, no parent.

## 8. Files to change and versioning

<!-- Source: Base (original, modified) - Changes #1, #12 -->
- `src/superclaude/commands/issue.md`: `version: "1.1.0"`, argument-hint, Usage, Options row, STOP rule, example, Will Not (launch an agent, pass Orca link flags).
- `src/superclaude/skills/sc-issue-protocol/SKILL.md`: one files-table row for `scripts/orca_worktree.py`, claim step 7 pointer, conditional contract block, warning rows, Will / Will Not.
- `.../refs/claim.md`: Wave 6 step 4 hand-off and Wave 7. No new ref file.
- `.../scripts/orca_worktree.py` (new). No template changes.
- Docs: `docs/designs/sc-issue-command.md` (B16 as worded in 2.7; sections 4, 7, 14, 16), `docs/user-guide/commands.md`. If the `/sc:issue` row of `HOW-WE-WORK.md` changes, byte-copy it to the `sc-recommend` mirror.
- Tests: section 7. Then `make sync-dev`, `make verify-sync`; stage `src/` only, never `.claude/`. Over five edits: `/sc:workflow`, then `/sc:implement`.

## 9. Risks and open items

<!-- Source: Base (original, modified) - Changes #13, #14 (Variant B, Section 9) -->
| # | Risk | Likelihood | Impact | Mitigation or check |
|---|---|---|---|---|
| R1 | UNVERIFIED: `--comment` fills `comment` | Medium | Medium: other keys carry reuse | AC-1; FO-3 |
| R2 | UNVERIFIED: create JSON field names | High | Low: set difference | AC-1 |
| R3 | UNVERIFIED: `--repo path:<main>` on create | Low | Medium: creates warn | AC-1 |
| R4 | UNVERIFIED: branch = prefix plus name | Medium | Low: last-segment key | AC-1 |
| R5 | UNVERIFIED: behaviour on a taken name | Medium | Low | AC-1; FO-4 |
| R6 | UNVERIFIED: setup fills `<wt>/.claude/` | Medium | Medium: `/sc:` commands missing there | AC-1; `make sync-dev` hint |
| R7 | All 11 observed rows carry `projectId: github:superclaude-org/superclaude_framework`; UNVERIFIED whether create contacts it | Medium | High: fork work exposed | no link flag (FR-6); AC-1 records it; watch Orca logs |
| R8 | Create with setup hooks exceeds 120 s (INV-011) | Low | Low: re-list | FO-6 |
| R9 | Owner rejects the B2 reading | Medium | High: flag withdrawn | confirm B16 first |
| R10 | Stale record reused while Orca is down | Low | Low: guard, warning | FO-1 |
| R11 | Hand-made `issue-<N>-*` row with another number source reused (INV-007) | Low | Low | match key, "not created by" line |

<!-- Source: Round 2 / INV-006, INV-008 - merged per Change #15 -->
**Accepted, not built:** INV-006, `linkedIssue` as a key: Orca resolves this repo to the upstream project, so its issue numbers may not be this fork's. INV-008, a lock for racing claims: a single user makes it unlikely; a race leaves two live hits and the next claim stops with `W-WORKTREE-AMBIGUOUS`, listing them.

**Open items:** an agent launch needs B2 amended first. `worktree_warning` holds one code; when two apply, which wins is undecided (proposal: the one that set the status, the rest in `detail`).

<!-- Source: Variant B, Section 9 - merged per Change #13 -->
**Out of scope:** agent launch; `--worktree <name>`; dry-run; automatic removal; a setup-policy choice and an explicit branch name (both forbidden by FR-6); a lock file; `linkedIssue` matching.

## 10. Provenance and verification checklist

<!-- Source: plan, base-selection, invariant probe -->
| Decision area | Source | Evidence |
|---|---|---|
| Script seam, timeouts | Base A | `clickup_claim.py` pattern |
| Wave 7 in `refs/claim.md` | B (Change 1) | `test_issue_protocol.py:131`, `:165` |
| `--repo path:<main>` | Base A | verified from a linked worktree |
| Name `issue-<N>` | Round 2 O4 (Change 2) | live `issue-*` rows |
| Key order, stale, ambiguity | INV-002, INV-004 (Change 3) | stale `/tmp` rows |
| List guard | INV-001 (Change 4) | list JSON fields |
| Set difference | B; INV-003, INV-011 (Change 5) | create JSON UNVERIFIED |
| Copy rule | INV-005, INV-010 (Change 6) | nesting verified |
| Record file | C (Change 7) | B dissents (2.5) |
| Base ref check | INV-009 (Change 8) | fetch result not visible |
| Post-condition | INV-016 (Change 9) | sufficiency |
| Contract, codes | INV-007 (Change 10) | distinct remedies |
| Tests | A, C (Change 11) | section 6 |
| B16 wording | X-003 (Change 12) | design doc line 27 |
| Ratings, scope | scoring (Change 13) | base-selection |
| Manual-run list | Round 2 O5 (Change 14) | AC-1 |
| Not built | INV-006, INV-008 (Change 15) | section 9 |
| Edge table | A, C (Change 16) | section 6 |

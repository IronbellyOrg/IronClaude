# Refactoring Plan

## Overview
- Base: Variant 2 (`variant-2-original.md`, proposal B)
- Incorporated: Variant 1 (proposal A), Variant 3 (proposal C), advocate concessions
- Planned changes: 15; rejected: 5
- Overall risk: Medium (changes 5, 6 and 13 alter the locking procedure)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Grants as one immutable file each; ledger stays one append-only file | Variant 1 S-003; Variants 2 and 3 C-010 | Layout, Naming, Concurrency | replace `grants.md` with `grants/<YYYYMMDD-HHMMSS>-g<NNNN>.md`; keep `ledger.md` | resolves the S-003 versus C-010 tension: a grant is authority and must be citable and tamper-evident (a changed grant shows as a modified file); the ledger is the owner's reading surface, has one writer, and git history recovers a careless rewrite | Low |
| 2 | Ids qualified by the coordinator | V2 advocate concession 3; X-002 | Naming | a grant or ledger row is cited project-wide as `<coordinator-id>/<stem>`, for example `epic-orchestrator-mode/ironbelly/20261114-093000-g0001`; same-second `-2` suffix as Variant 1 | removes every repeatable id | Low |
| 3 | `-N` suffix rule for a developer's second coordinator on one scope | V2 advocate concession 7 | Naming | `<dev>-2`, `<dev>-3`: next unused integer, never reused, independent of whether the first is still active | removes the under-specified "only when the first is still active" | Low |
| 4 | `adhoc` kind | Variant 3 C-009 | Naming, Layout | `<kind>` = `epic`, `release` or `adhoc` | gives triage and one-off coordination a home | Low |
| 5 | Claim procedure and conflict rule | V2 advocate concession 1; V3 advocate weakness 3 | Concurrency | a claim is its own commit, made on a just-fetched `origin/coordinators` with no other unpushed commit, and pushed at once; if the push is rejected, fetch; if the claim path now exists upstream, the claim is lost: drop the local claim commit and pick other work; nobody ever resolves a conflict under `claims/` or on `scope.md` by keeping their own side; a claim body always holds the coordinator id, a stamp and the revision read, so two bodies are never byte-identical | without it the lock can be stolen silently | Medium |
| 6 | Never force-push or rewrite `coordinators` | A-003, all advocates | Concurrency, Relation to rules | written rule; branch protection on the fork is an owner decision (UNVERIFIED that the fork's plan supports it) | the claim lock is void after a force push | Medium |
| 7 | Stale-base reading rule | A-004 (two REJECT, one QUALIFY) | new subsection in Concurrency | a coordinator reads code and program documents with `git show origin/master:<path>` (or the owning branch), records the revision, never assumes its checkout is current, and never rebases `coordinators` onto master | the coordinator worktree holds only the branch base plus `.dev/coordinators/` | Low |
| 8 | Identity from `gh` | A-001 | Naming | `gh api user --jq .login`, lower-cased, read once and frozen in `coordinator.md`; no authenticated `gh` means no folder and no claim; never `git config user.name` | author names identify nobody (`coder` is the shared default) | Low |
| 9 | Handle in the worktree name | A-002 | Naming | Orca `--name coord-<dev>-<kind>-<scope>` | no clash if two developers ever share a host | Low |
| 10 | Unpushed coordinators | Variant 3 A-006, reconciled with C-003 | Visibility | a coordinator may stay unpushed, but an unpushed coordinator cannot claim and so cannot dispatch | keeps private work possible without invisible claims | Low |
| 11 | Path-narrowed push grant | Variant 3 C-008 | Relation to rules | the standing grant covers `git push origin HEAD:coordinators` only, and only commits whose paths are the coordinator's own folder, `claims/` files naming it, or a new `scope.md`; before each push the coordinator lists `git diff --name-only origin/coordinators..HEAD` and stops on any other path (procedural; no hook exists) | narrows the authority of a shared-branch push | Low |
| 12 | Content rule for pushed files | A-006; V3 advocate concession 7 | Relation to rules | no tokens, no secrets, no host or contact details; captures sanitized before commit | the fork is private but grants quote owner wording | Low |
| 13 | Scope-wide decisions as create-once files | Variant 1 strength 1 (one decision authority per scope) | Layout, Concurrency | `<kind>-<scope>/decisions/<key>.md`, create-once, same lock as claims; any decision that binds the whole scope (an owner answer, an epic design choice) lives there and ledger rows cite it | stops two coordinators on one epic from recording contradictory scope-wide decisions | Medium |
| 14 | Losing `scope.md` race is recorded, not silent | V1 and V3 advocate critiques | Collision rules | the second developer keeps the pushed `scope.md` and writes a ledger row in their own folder saying what they would change; a change to `scope.md` after creation needs the project owner | removes silent loss | Low |
| 15 | Base branch fallback and branch prefix wording | X-003; advocates' `git worktree list` facts | Naming, Relation to rules, Unresolved | try `--base-branch origin/coordinators`; if Orca refuses (UNVERIFIED), create from `origin/master` (as spec 6.2 says) and, inside the worktree, `git merge origin/coordinators` once before the first push so `HEAD:coordinators` is a fast-forward; say the `<prefix>/<name>` branch shape is a habit with exceptions (`brainstorm-reflect-panel` on `ironbelly/shadow-runs`, `issue-409-mvp` on `409-Phase2`) and that no lock depends on it | the base proposals overstate the prefix and assume an unverified Orca behaviour | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why not |
|---|---|---|
| C-002 | Variant 1's single lease per scope | serialises an epic, against "multiple developers with multiple coordinators"; change 13 keeps its real benefit (one place for scope-wide decisions) |
| C-001 | Variant 3's branch per developer | departs from the owner's "a Coordinator branch"; its blast-radius benefit is partly recovered by changes 6 and 11 |
| C-005 | Variant 1's archive move | breaks cited paths |
| C-003 | Variant 3's advisory scan | racy; its own advocate conceded |
| S-003 (ledger part) | Variant 1's one file per ledger entry | the ledger is the owner's reading surface (C-010, unanimous tie of 2 and 3); one writer plus git history is enough there |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 5 | Medium | an agent drops a claim commit that held other work | the "no other unpushed commit" precondition prevents it; rollback is to re-create the lost ledger row from the session log |
| 6 | Medium | a force push removes claims | restore from any coordinator's local copy of `origin/coordinators` |
| 13 | Medium | too many decisions forced into create-once files | only scope-binding decisions go there; others stay ledger rows |
| others | Low | wording or naming friction | edit the convention |

## Review Status
Auto-approved (non-interactive), 2026-11-14.

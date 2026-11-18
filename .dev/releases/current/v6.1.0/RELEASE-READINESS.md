# Release readiness (6.1.0)

Started 2026-11-18 20:58Z. Plan and map: issue 647. Records for 6.0.0 are in `../v6.0.0/`.

## 1. What the release depends on (owner for every item, or "not in this release")

Applied from the 6.0.0 retrospective, before the release pull request is opened.

| Item | In 6.1.0? | Owner | State |
|---|---|---|---|
| PR 1: remove `prd`, `tdd`, `tech-research`, `tech-reference`, `operational-guide`, `readme`, `/sc:tdd`, two release guides | Yes | Bundle agent builds; orchestrator merges | #650, see section 2 |
| PR 3: re-point every task-file (MDTM) route to `/sc:workflow` then `/sc:implement` | Yes | same | #653 |
| PR 4: remove `task`, `task-builder`, `roadmap`, the eval suite `workflow_vs_task_builder`, level 4 of the routing guide | Yes | same | #656 |
| PR 5: retire-step data (`--tag v5.0.0 --tag v6.0.0`), version 6.1.0, `CHANGELOG.md`, `docs/releases/v6.1.0.md`, upgrade guide | Yes | same | #657 |
| PR 2 (`/sc:task`, `/sc:validate-tests`) | **Not in this release** (withdrawn, #652 closed) | Clay | decided |
| The `rf-*` agents (all eight) | **Not in this release** (kept; issue 572 decides) | Clay | decided |
| Part C, issue 572 (agents evaluation) | **Not in this release** | Clay | undecided, out of scope |
| Upgrade from an installed 6.0.0 removes the shipped files, keeps edited copies, keeps `/sc:task` family and every `rf-*` agent | Yes (acceptance criterion) | Orchestrator checks in the gate (throwaway home, genuine 6.0.0 install from the `v6.0.0` tag) | open |
| Changelog completeness: every pull request merged since `v6.0.0` is in `CHANGELOG.md` or named as excluded | Yes | Orchestrator checks before the release PR | open |
| List of IronClaude-only changes to port to IronFlow | Yes (a retention list, in issue 647 / `retention.md` on `clayphi/v61-part-b-map`) | Clay; IronFlow is not edited here | with Clay |
| Pull request #641 (ccsession human versus agent sessions, issue #638) | **Yes** (Clay, 20:59Z; merged into `master` as `89dc403d4`) | GeneralIronFlow merged it; orchestrator merges `master` into `integration` after #650; bundle agent carries its changelog entry (moved from `[Unreleased]` to `[6.1.0]`) and release-notes text in #657 | open |
| Post-release scope for 6.1.0 | As 6.0.0 (documentation sync and install and upgrade runs; no new hand-test guides) | Clay, confirmed | decided |
| Coder repository pin bump to the new tag | Not mine | Coder repo's monitor; I tell Clay when its PR appears | not touched |
| `master` merged into `integration` | Needed: `master` is two commits ahead (`3f3b34a26`, the 6.0.0 release merge, tree equal to `integration` at `847cccc1a`; and `89dc403d4`, #641) | Orchestrator | before the release PR |

## 2. Pull requests into `integration` (squash, in this order)

| Order | Change | Branch | State | Link | Tests | Merged |
|---|---|---|---|---|---|---|
| 1 | Documentation skills removed | `clayphi/v61-pr1-doc-skills` | MERGED (squash) | [#650](https://github.com/IronbellyOrg/IronClaude/pull/650) | Agent's run on the final head: 22638 passed, 1 failed (`test_ccsession_tiers::test_upgraded_code_starts_a_new_shim_and_keeps_the_old`, passes alone), 70 skipped; 76 files, +1070 -13954. CI 6 of 6, Codex completed, Augment 0 suggestions, 0 open threads | 2026-11-18 21:17Z, `430eaa87f` |
| 2 | Re-point the MDTM routes | `clayphi/v61-pr3-mdtm-routes` | MERGED (squash) | [#653](https://github.com/IronbellyOrg/IronClaude/pull/653) | Agent's run on the final head: 22850 passed, 3 failed (two real-claude PTY tests and a shared-scratch-folder test that pass alone); 45 files, +591 -784. CI 6 of 6, Codex completed, Augment 0 suggestions, 5 threads all resolved | 2026-11-18 21:31Z, `2ca022bf7` |
| 3 | Remove the MDTM pair and `roadmap` | `clayphi/v61-pr4-mdtm` | MERGED (squash) | [#656](https://github.com/IronbellyOrg/IronClaude/pull/656) | Agent's run: 22583 passed, 4 failed (scratch-folder tests that fail under parallel load; 34 pass alone); 78 files, +217 -14049; throwaway-home install and `doctor` pass with `task`, `task-builder` and `roadmap` not installed. CI 6 of 6, Codex completed, Augment 0 suggestions, 2 threads resolved | 2026-11-18 21:56Z, `a3edd84db` |
| 4 | Retire step data, version, changelog, release notes, upgrade guide (stacked on #656) | `clayphi/v61-pr5-release` | OPEN | [#657](https://github.com/IronbellyOrg/IronClaude/pull/657) | | |

Baseline on `847cccc1a` (from issue 647): 22691 passed, 10 failed, 70 skipped, 1 xpassed. The test that was in that list as order dependent, `test_install_keep::...`, was fixed by #646.

Master merged into `integration` at 21:17Z as a merge commit `0f92aa687` (parents `430eaa87f` and `89dc403d4`, the 6.0.0 release merge and #641), clean, through `gh api -X POST repos/IronbellyOrg/IronClaude/merges`.

Known leftover (for issue 572, not in this release): `src/superclaude/rules/contextual/context_embedding.md:140` and `src/superclaude/rules/prompts/agent_library.md:34,288` still name the old `/rf:taskbuilder` command (found by Augment's review of #656; the agent left them because the rules folder is out of scope in issue 647).

## 3. Gate on the release PR's merge commit (G1 to G9)

Not started.

## 4. Tag and release

Not started. Stops for Clay's final yes before the release PR is merged.

## 5. Finished worktrees (for Clay to remove later)

None yet. The bundle agent's worktrees are its own.

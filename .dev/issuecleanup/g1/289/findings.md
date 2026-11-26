# Summary: #289 Worktree and branch protocol for parallel sessions

<!-- Structure: ~/.claude/skills/sc-issue-protocol/templates/issue-summary.md, extended with the fields required by the dispatch brief. -->

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/289
- Reviewed: 2026-11-23
- Type: feature (documentation and workflow policy)
- Verdict: **still-relevant** (partly delivered, not safe to close).
- Complexity and size: **medium / M**. The cleanup engine already exists; the remaining work is an agreed creation/reuse and naming policy, a short guide section and mirror, focused tests and the onboarding slide, not another cleanup implementation.
- Priority: **P2**. Missing shared guidance can cause duplicate worktrees and inconsistent handoffs, but creation ownership and safe cleanup already have rules; no formal issue blocker or active data-loss incident was established.

## What the issue asks for

Record which sessions create or reuse a worktree, where worktrees live, how branches and folders are named, how work survives closure, and where worktree-local `.dev/` evidence ends up. Acceptance requires a short section in the installed workflow guide, tests in `tests/core/`, and replacement of the onboarding deck's unfinished-worktree-policy slide.

The owner's 2026-10-29 comment chooses new work (reuse an existing worktree for a bug fix when available), Orca's folder, names shorter than 25 characters with no spaces and metadata plus a short description, and proposes a cleanup/archive flow. These are requirements and proposals, not proof all decisions are implemented.

## Relevant files and systems (cheatsheet)

All source paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/`.

| Path or system | Why it matters |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md` | Narrowest analysis target and required installed policy destination. |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Required byte-identical guide mirror when the source guide changes (repository maintainer rule). |
| `src/superclaude/core/WORKER-CONTRACT.md` | Existing supervised-worker placement, retention and cleanup safeguards; not a general session policy. |
| `src/superclaude/commands/worktrees.md`; `scripts/worktree_cleanup.py`; `scripts/worktree_cleanup_orca_automation.md` | Cleanup command, archive implementation, and not-enabled scheduling definition delivered by PR #711. |
| `tests/core/test_claude_md_worktree_rule.py`; `tests/core/test_how_we_work_routing_table.py` | Existing tests cover ownership and command registration, not the complete requested creation/reuse/naming policy. |
| `docs/onboarding/ironclaude-onboarding.html` | Slide still explicitly says issue #289 is being worked out. |

## Analysis

### Evidence and real current state

The issue remains OPEN. Its body and all three comments were read. The 2026-11-17 status comment is now stale in two important ways: the cleanup implementation has merged, and the workflow guide now explicitly answers when a merged worktree can be removed.

| Requested decision or acceptance item | Real state and evidence |
|---|---|
| Which sessions create a worktree; when bug fixes/continuations reuse it | **Incomplete in the shared guide.** The full guide has orchestration-specific creation rules at `src/superclaude/core/HOW-WE-WORK.md:352-362` and conversation/plan resume guidance at `:210-221`, but no general new-work-versus-reuse policy matching the owner's answer. There is already issue-specific reuse logic in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:384-422`; do not confuse that with a policy for every session. |
| Where worktrees live | **Delivered.** The guide states Orca's default paths and rejects raw Git creation and `.dev/worktrees/` at `src/superclaude/core/HOW-WE-WORK.md:361`. The worker placement rules repeat that at `src/superclaude/core/WORKER-CONTRACT.md:233`. PR #368 is earlier migration evidence. |
| Branch/worktree naming under 25 characters, no spaces, metadata plus description | **Incomplete.** No such convention appears in the full guide. The claim launcher uses `issue-{number}` (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:695-708`), which is an existing specific naming scheme, not the requested metadata-plus-description policy. The particular metadata and shortening/collision rule still need agreement; do not invent an approved convention. |
| Preserve work and remove merged worktrees safely | **Substantially delivered by #687 / PR #711.** `src/superclaude/core/HOW-WE-WORK.md:299` explicitly references item 4 of #289 and requires the merge plus all cleanup rules. `src/superclaude/commands/worktrees.md:15-17` defines the guarded cleanup and dry-run defaults. `src/superclaude/core/WORKER-CONTRACT.md:236-238` already protects unread reports, unfinished ledgers, uncommitted changes and unmerged work in supervised runs. |
| Destination for `.dev/` evidence | **Raw preservation delivered; lesson extraction is not established.** `scripts/worktree_cleanup.py:58-59` names the evidence-repository defaults; `:2274-2303` handles untracked/ignored `.dev/` files; `:2373-2409` copies and archives them and writes a checksum manifest. The manifest at `:2251-2271` contains provenance/checksums, not a synthesis of lessons, bugs and failures proposed in the owner's comment. Whether that synthesis is still wanted after #687 was closed is **UNVERIFIED**, not a reason to rebuild cleanup without approval. |
| Short guide section with tests in `tests/core/` | **Partial only.** The guide has cleanup and Orca placement entries, not the complete policy. Existing `tests/core/test_claude_md_worktree_rule.py:14-39` checks the repository's ownership rule; `tests/core/test_how_we_work_routing_table.py:26-37` includes the cleanup command. Searches in `tests/core/` found no test for the requested new-work/reuse or under-25-character naming policy. |
| Replace onboarding's unfinished-policy slide | **Not delivered.** `docs/onboarding/ironclaude-onboarding.html:515-523` still labels the worktree-and-branch protocol "Being worked out" and links #289. |

No matching open pull request was returned by the worktree/worktrees search. This supports **still-relevant**, rather than claiming an active implementation is underway; it is not proof no unpushed work exists.

### Concrete next steps

1. Keep #289 open, but narrow its remaining work using PR #711 rather than carrying forward the claim that no cleanup exists.
2. Write the owner's new-work/reuse rule and Orca placement rule into one short shared-guide section. Keep ordinary session policy distinct from supervised-worker placement and the claim launcher's specific reuse behavior.
3. Agree the concrete branch/worktree format that satisfies shorter than 25 characters, no spaces, metadata and a short description, including how truncation avoids name collisions. Add examples only after that format is approved.
4. Point the guide at the existing cleanup/archive implementation and its evidence destination. Explicitly state its IronClaude-checkout boundary and that scheduling is definition-only (`scripts/worktree_cleanup_orca_automation.md:3-15`); do not switch it on as part of this documentation task. Ask the owner separately whether automated lesson extraction is still desired, since raw archival is now delivered.
5. Add focused policy tests under `tests/core/`, keep the guide's required plugin mirror current, and replace only the worktree card of the onboarding slide. Do not remove the adjacent contribution-policy topic for #290.
6. Check the resulting guide, tests and slide against all acceptance criteria before recommending closure. No such edits, tests, approvals or closure were performed in this review.

### Dependencies

- **Needs:** no formal issue dependency was returned (`blockedBy.totalCount = 0`). #687 was the functional cleanup prerequisite and is now CLOSED, with completion attributed to PR #711 in its 2026-11-23 comment; it is not a remaining blocker.
- **Blocks:** no formal blocking relationship was returned (`blocking.totalCount = 0`). Finishing #289 is needed to replace its own unfinished onboarding card; no other issue was verified to be blocked on it.
- **Owner decisions, not issue dependencies:** the exact naming convention and whether semantic lesson extraction remains in scope. No approval was inferred.

### Related issues

- [#687, Daily cleanup of merged worktrees](https://github.com/IronbellyOrg/IronClaude/issues/687): CLOSED. Delivers much of decisions 4 and 5; completion comment cites PR #711.
- [#339, Orchestrator for managing sessions in a worktree](https://github.com/IronbellyOrg/IronClaude/issues/339): OPEN. Mentioned in #289's review; its body includes supervision and safe session/worktree closure. Related ownership context, not a proven prerequisite for documenting the general policy.
- [#290, contribution rules](https://github.com/IronbellyOrg/IronClaude/issues/290): the adjacent onboarding topic at `docs/onboarding/ironclaude-onboarding.html:525-527`. Its live state and substance were not reviewed; **UNVERIFIED** beyond that local reference.

### Related PRs and commits

| PR | Verified state and commit | Relevance |
|---|---|---|
| [#368](https://github.com/IronbellyOrg/IronClaude/pull/368) | MERGED 2026-11-04; `f3c1ef06296086a2c4d341ef807c871ddd6b1baf` | Mentioned migration of Orca worktree/worker guidance; does not establish all #289 decisions. |
| [#532](https://github.com/IronbellyOrg/IronClaude/pull/532) | MERGED 2026-11-12; `05b78d4d351259b798e5794af58626a4d9cbd693` | Mentioned supervised-orchestration reference and worktree ownership guidance. |
| [#541](https://github.com/IronbellyOrg/IronClaude/pull/541) | MERGED 2026-11-14; `0406ef5b01f2e79c88100d32f01df4ebf2395646` | Test-only ownership-wording update. It does not implement the general branch/worktree policy. |
| [#711](https://github.com/IronbellyOrg/IronClaude/pull/711) | MERGED 2026-11-22; `6b17a7449f9400a9acc4140d6ce48dec93a9de8e` | Cleanup/archive implementation for #687 and guide entry explicitly answering #289 item 4. |

### Verification limits

- **UNVERIFIED: complete GitHub event timeline.** The allowed `gh issue view` fields expose comments, timestamps, formal dependencies and closing-PR references, but not timeline events. `gh issue view --help` was checked; no timeline field is available. No API, browser or alternate endpoint was used to bypass the brief's read-command restriction. The coordinator can inspect the remaining event timeline separately if needed.
- The issue returned no closing PR references, no formal dependencies, no parent and no sub-issues. Searches for PRs containing `289` produced unrelated textual matches, which were not treated as links. Known mentioned PRs #368/#532/#541 and newer relevant #711 were read directly.
- Native searches covered the full guide, `tests/core/`, relevant core docs, and worktree/naming references under `docs/`. The documentation search hit its 70-line display limit, so no repository-wide absence claim is made. Augment initially failed on implicit `main`; the explicit `master` retry succeeded. Codegraph cannot index this Markdown target; the analysis records `graph:empty` and uses native Reads/searches.
- **UNVERIFIED: live cleanup, evidence-repository contents, installed-project operation, scheduler activation, and current runtime test results.** No cleanup, archive, terminal close, deletion, network write, source change, staging or commit was performed. The PR's reported checks were not rerun. A first attempted report Edit was rejected by the freshness hook; the required tracked Reads were then completed and the Edits succeeded.
- Detailed command output: `analyze/analyze-report.md`. The worker contract and handoff are in `analyze/return-contract.yaml` and `analyze/handoff/1-analyze.md`.

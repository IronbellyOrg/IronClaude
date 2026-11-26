# Findings: issue #773 (IronbellyOrg/IronClaude)

Issue: "[FEATURE] Let `/sc:issue` set up everything an issue needs for the watcher except the approval". Author clayphi, opened 2026-11-24T18:27:54Z, state OPEN, label `enhancement`, no assignee, no comments, Project Status Backlog. Checked against HEAD a7ae3dd30 on 2026-11-24. Analyze report: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g7/773/analyze/analyze-report.md`.

## Verdict

**still-relevant.** The issue is a proposal posed as a question; it says its acceptance criteria are "not approval to build now". Nothing has been built and no owner answer exists.

Evidence (all checked 2026-11-24):
- The only Project-field writer in `src/` is `src/superclaude/cli/issue_pipeline/complete.py:124` (`updateProjectV2ItemFieldValue`, Status to In review after success). A repo-wide grep for label-apply, add-to-project and field-write calls in `src/superclaude` found nothing else. The `Pipeline` field is only read (`src/superclaude/cli/issue_watch/github.py:109`).
- `/sc:issue --create` does not assign (`src/superclaude/skills/sc-issue-protocol/refs/create.md:97`, "No self-assignment"). `/sc:issue --claim` assigns `@me` (`SKILL.md:87`, `refs/claim.md:48`).
- The command contract forbids the proposed writes: `src/superclaude/commands/issue.md:102-103` ("Create labels... Write any issue field other than Complexity" are under Will Not).
- `src/superclaude/cli/issue_watch/repo_init.py` (`ensure_trigger_label`) creates the repository label only; no code applies it to an issue.
- The skill's `scripts/` folder has `clickup_claim.py`, `orca_worktree.py`, `origin_repo.py`; no Project setup helper.
- No pull request covers this (PR search returned none; PR #707 is merged, 2026-11-20, commit `2ea524514`, and is the design the issue keeps). No duplicate for the setup request itself (#761 is the parent gap list), but #777 overlaps on gap 7 (the whole-chain review), see Related issues.
- Both gating issues are still OPEN: #722 (shared login, comment by ironbelly 2026-11-24 rates it still-relevant; clayphi replied it is lower priority) and #698 (approver rule, still-relevant per ironbelly review).
- Real state: Backlog, unassigned, unapproved. UNVERIFIED: whether the owner treats this as inside owner ruling R38 (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`, "Ignore all of Clay's suggestions, only approve merged watcher ideas"). The issue says it keeps the merged design, but its author is the person R38 names, so an owner confirmation is needed. UNVERIFIED: whether a non-admin login can write Project fields and labels (needs one trial write on a test issue; not done, read-only task).
- Naming trap (new finding, not in the issue): `--pipeline` on `/sc:issue --claim` (`commands/issue.md:43`) is the launch level (worktree/full/none), not the Project `Pipeline` field the watcher reads. A setup flag needs a different name.

## Complexity and size

Complexity medium, size M: about five skill and command files, one new helper script and tests, but the real difficulty is the identity and approval decisions, and the Project write path can copy `complete.py`.

## Priority

P2: the issue claims High, but nothing in code is blocked by it, it cannot start until the owner answers #722 (P1, complex) and #698, and the manual workaround works today; it becomes P1 only if the owner confirms the 20+ pull requests a day routine.

## Concrete next steps

1. Owner answers, in chat, which of the five items (assign, Status, Pipeline, trigger label, per-issue grant) an agent may set and under which login; resolve #722 and #698 first. Also confirm R38 does not cover this issue.
2. Decide where the Project id and field ids come from (candidate: reuse the watcher defaults `src/superclaude/cli/issue_watch/defaults.py`, UNVERIFIED as suitable).
3. Run the one trial write on a test issue for the non-admin question (needs the owner's go; not authorized here).
4. Only then: `/sc:workflow` then `/sc:implement`, adding a helper under `src/superclaude/skills/sc-issue-protocol/scripts/`, updating `commands/issue.md` (the line 102-103 limits), `SKILL.md`, `refs/create.md`, `refs/claim.md`, `refs/labels.md`, and tests. Use a flag name other than `--pipeline`.
5. Do not file a new issue for the "simplification review of the whole chain": issue #777 (OPEN, clayphi, 2026-11-24T18:43:42Z, "map the whole watcher and coordinator chain and decide what to automate") already asks for it (gap 7). Link or fold #773's last acceptance criterion into #777. The claim that no earlier review exists is still UNVERIFIED.

## Dependencies

Needs (answers first): #722, #698. Soft: #777 (gap 7 review), #761 (parent gap list), #716 (keeps claim/store baseline). Blocks: nothing in code; it would shorten the hand setup for every watcher issue.

## Related issues

#777 (open; whole-chain map and automation decision, overlaps gap 7), #761 (18 possible gaps; this covers 1 and 7), #722, #698, #721 (claim estimate refactor, same skill), #716, #733 (unattended `/sc:implement`), #655 (closed, the orchestrator it replaced).

## Related PRs

#707 (merged 2026-11-20, `2ea524514`: zero-setup watcher, Approved field, guard v2; the design kept). No open PR for this issue.

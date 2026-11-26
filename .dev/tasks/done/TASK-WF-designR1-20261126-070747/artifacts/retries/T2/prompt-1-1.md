ef4833b35137ccca2128032b7a8baeb05aaac511
Review one task for spec compliance.

Task brief: ## Task 2: Rewrite the Step 3 gate with the capture block and the When column

Depends on: Task 1

Edit `docs/developer-guide/release-procedure.md`, section "Step 3: Run the go/no-go gate (G1-G9)" (design section 3.1 in `./source.md`, "Step 3"). The heading text and the G1 to G9 numbers stay.

- Rewrite the intro paragraph (today "Run every check on the merge commit of the release PR. ...") to: every check must pass; any failure is a no-go, stop and take the result back to the release owner; do not tag and do not work around a failed check (decisions 7.7 and T1); rows marked "before merge" ran in Step 2 on the reviewed head; the rest run on the merge commit after the merge.
- Add this capture block before the table, with the pass rule below it:

```bash
gh pr view <n> --repo IronbellyOrg/IronClaude --json state,baseRefName,headRefName,headRefOid,mergeCommit
git fetch origin master integration --tags
git rev-parse --verify -q <merge-sha>^2
git rev-parse --verify -q <merge-sha>^3
git rev-parse <merge-sha>^1 <merge-sha>^2
git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}
```

  Pass only if `state` is `MERGED`, `baseRefName` is `master`, `headRefName` is `integration` and `mergeCommit.oid` is not null (that value is `<merge-sha>`); the `^2` line prints a hash and the `^3` line prints nothing and exits 1; `^1` equals `<master-tip>` and `^2` equals `<reviewed-head-sha>`; the two trees are equal. Any failure: stop before tagging. A squash or rebase merge has no `^2`; `master` moving after Step 2 breaks the `^1` and tree checks.
- Add a "When" column to the gate table: G1 before merge; G2 after merge; G3, G4, G5, G6 and G7 before merge; G8 before merge unless the owner names a check that needs the merge commit or GitHub state; G9 after merge. Do not add a row and do not renumber.
- Replace the G2 command (`gh run list --repo IronbellyOrg/IronClaude --branch master --limit 3 --json headSha,conclusion,workflowName`) with `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion`. New pass condition: the push run for `<merge-sha>` completed with conclusion `success`; no run yet, or `status` not `completed`, means wait (repeat the command by hand, or `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status`) for at most 30 minutes, then stop without tagging; a completed run that is not `success`, or no run by the deadline, is no-go; missing, other-SHA or `workflow_dispatch` evidence is never a pass; the newest attempt decides; two push runs for the same attempt: ask the owner. Keep the `test-summary` sentence.
- Rewrite the G7 row: its command cell "In a checkout of the release commit: `./update.sh`; ..." becomes "On the detached reviewed-head checkout of Step 2, after `make sync-dev`: `./update.sh`; ..." with the rest of the cell unchanged. In the G5 row or the notes under the table, say G5 runs on that checkout after `make sync-dev` too.
- Rewrite the G1 pass text so it reads: `origin` is `IronbellyOrg/IronClaude`; every `gh` command in this procedure passes `--repo IronbellyOrg/IronClaude` or is a `gh api repos/IronbellyOrg/IronClaude ...` call, so gh's default repository cannot send it to the upstream parent.
- The G7 notes about `./update.sh` stay.

Acceptance criteria:
- `grep -n -e '--limit 3' docs/developer-guide/release-procedure.md` prints nothing, and the page contains the G2 command above verbatim.
- `grep -n '30 minutes' docs/developer-guide/release-procedure.md` finds the G2 limit, `grep -n 'completed run that is not' docs/developer-guide/release-procedure.md` finds the rule that a completed run that is not `success` is no-go (write that phrase on the page; the page already says "no-go" in its headings, so a grep for that word alone cannot fail), and `grep -n 'ask the owner' docs/developer-guide/release-procedure.md` finds the two-push-runs rule.
- The page contains the six capture-block lines verbatim and the table has a "When" column with the stated value for each of G1 to G9, still nine rows numbered G1 to G9, and the heading `## Step 3: Run the go/no-go gate (G1-G9)` is unchanged.
- `grep -n 'checkout of the release commit' docs/developer-guide/release-procedure.md` prints nothing, and the G1 row names the `gh api repos/IronbellyOrg/IronClaude` form.
- No fenced line on the page starts with `gh ` without `--repo IronbellyOrg/IronClaude` or the `gh api repos/IronbellyOrg/IronClaude` form.


AC ids (source order):
T2.AC1 = `grep -n -e '--limit 3' docs/developer-guide/release-procedure.md` prints nothing, and the page contains the G2 command above verbatim.
T2.AC2 = `grep -n '30 minutes' docs/developer-guide/release-procedure.md` finds the G2 limit, `grep -n 'completed run that is not' docs/developer-guide/release-procedure.md` finds the rule that a completed run that is not `success` is no-go (write that phrase on the page; the page already says "no-go" in its headings, so a grep for that word alone cannot fail), and `grep -n 'ask the owner' docs/developer-guide/release-procedure.md` finds the two-push-runs rule.
T2.AC3 = The page contains the six capture-block lines verbatim and the table has a "When" column with the stated value for each of G1 to G9, still nine rows numbered G1 to G9, and the heading `## Step 3: Run the go/no-go gate (G1-G9)` is unchanged.
T2.AC4 = `grep -n 'checkout of the release commit' docs/developer-guide/release-procedure.md` prints nothing, and the G1 row names the `gh api repos/IronbellyOrg/IronClaude` form.
T2.AC5 = No fenced line on the page starts with `gh ` without `--repo IronbellyOrg/IronClaude` or the `gh api repos/IronbellyOrg/IronClaude` form.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: ef4833b35137ccca2128032b7a8baeb05aaac511
Diff against the start snapshot: diff --git a/docs/developer-guide/release-procedure.md b/docs/developer-guide/release-procedure.md
index 705b352f6..68ac48f8a 100644
--- a/docs/developer-guide/release-procedure.md
+++ b/docs/developer-guide/release-procedure.md
@@ -101,19 +101,32 @@ Anything that merges before the release PR is opened rides along in the release.
 
 ## Step 3: Run the go/no-go gate (G1-G9)
 
-Run every check on the merge commit of the release PR. Every check must pass. **Any failure is a no-go: stop and take the result back to the release owner.** Do not tag, and do not work around a failed check (decisions 7.7 and T1).
-
-| # | Check | Command | Pass condition |
-|---|---|---|---|
-| G1 | Fork target | `git remote -v` | `origin` is `IronbellyOrg/IronClaude`. Every `gh` command in this procedure passes `--repo IronbellyOrg/IronClaude`, so gh's default repository cannot send it to the upstream parent. |
-| G2 | CI on the exact commit | `gh run list --repo IronbellyOrg/IronClaude --branch master --limit 3 --json headSha,conclusion,workflowName` | The `Tests` workflow is `success` for the release PR's merge SHA. Its `test-summary` job fails if the `test`, `swarm-marker-matrix`, `lint` or `doctor-check` job failed (`.github/workflows/test.yml:177-186`). |
-| G3 | Version consistency | `grep -n '^version' pyproject.toml`; `grep -n '__version__ =' src/superclaude/__init__.py`; `uv run superclaude --version` | All three show `X.Y.Z`. |
-| G4 | Changelog cut | `grep -n '^## ' CHANGELOG.md` | `## [Unreleased]` is empty and is followed by `## [X.Y.Z] - YYYY-MM-DD`; breaking entries sit in the `X.Y.Z` section. |
-| G5 | Full local suite and gates | `make test`; `make lint`; `make verify-sync`; `make verify-deps`; `make lint-architecture` | All exit 0. |
-| G6 | Package builds | `uv build` | Wheel and sdist are built. Nothing is uploaded. |
-| G7 | Upgrade path on an existing workspace | In a checkout of the release commit: `./update.sh`; start a new Claude session; `superclaude doctor`; `superclaude install --list`; `/sc:graph status` | `doctor` passes; `install --list` shows the codegraph block; `/sc:graph status` reports an index state. |
-| G8 | Release-specific checks | Whatever checks the owner names for this release | Each one passes and its result is recorded where the owner asked. For v5.0.0 these were the post-merge codegraph check and the QA-loop findings (`RELEASE-READINESS.md` section 6.2). |
-| G9 | No open PR meant for this release | `gh pr list --repo IronbellyOrg/IronClaude --state open` | Only PRs that were deferred to a later release are open. |
+Every check must pass. **Any failure is a no-go: stop and take the result back to the release owner.** Do not tag, and do not work around a failed check (decisions 7.7 and T1). The rows marked "before merge" ran in Step 2 on the reviewed head; the rest run on the merge commit after the merge.
+
+After the merge, capture what was merged:
+
+```bash
+gh pr view <n> --repo IronbellyOrg/IronClaude --json state,baseRefName,headRefName,headRefOid,mergeCommit
+git fetch origin master integration --tags
+git rev-parse --verify -q <merge-sha>^2
+git rev-parse --verify -q <merge-sha>^3
+git rev-parse <merge-sha>^1 <merge-sha>^2
+git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}
+```
+
+Pass only if `state` is `MERGED`, `baseRefName` is `master`, `headRefName` is `integration` and `mergeCommit.oid` is not null (that value is `<merge-sha>`); the `^2` line prints a hash and the `^3` line prints nothing and exits 1; `^1` equals `<master-tip>` and `^2` equals `<reviewed-head-sha>`; the two trees are equal. Any failure: stop before tagging. A squash or rebase merge has no `^2`; `master` moving after Step 2 breaks the `^1` and tree checks.
+
+| # | Check | When | Command | Pass condition |
+|---|---|---|---|---|
+| G1 | Fork target | before merge | `git remote -v` | `origin` is `IronbellyOrg/IronClaude`; every `gh` command in this procedure passes `--repo IronbellyOrg/IronClaude` or is a `gh api repos/IronbellyOrg/IronClaude ...` call, so gh's default repository cannot send it to the upstream parent. |
+| G2 | CI on the exact commit | after merge | `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion` | The push run of the `Tests` workflow for `<merge-sha>` completed with conclusion `success`. No run yet, or a `status` that is not `completed`, means wait: repeat the command by hand, or run `gh run watch <databaseId> --repo IronbellyOrg/IronClaude --exit-status`, for at most 30 minutes, then stop without tagging. A completed run that is not `success`, or no run by the deadline, is no-go. Evidence that is missing, for another SHA or from a `workflow_dispatch` run is never a pass. The newest attempt decides; two push runs for the same attempt: ask the owner. Its `test-summary` job fails if the `test`, `swarm-marker-matrix`, `lint` or `doctor-check` job failed (`.github/workflows/test.yml:177-186`). |
+| G3 | Version consistency | before merge | `grep -n '^version' pyproject.toml`; `grep -n '__version__ =' src/superclaude/__init__.py`; `uv run superclaude --version` | All three show `X.Y.Z`. |
+| G4 | Changelog cut | before merge | `grep -n '^## ' CHANGELOG.md` | `## [Unreleased]` is empty and is followed by `## [X.Y.Z] - YYYY-MM-DD`; breaking entries sit in the `X.Y.Z` section. |
+| G5 | Full local suite and gates | before merge | `make test`; `make lint`; `make verify-sync`; `make verify-deps`; `make lint-architecture` | All exit 0. Run on the detached reviewed-head checkout of Step 2, after `make sync-dev`. |
+| G6 | Package builds | before merge | `uv build` | Wheel and sdist are built. Nothing is uploaded. |
+| G7 | Upgrade path on an existing workspace | before merge | On the detached reviewed-head checkout of Step 2, after `make sync-dev`: `./update.sh`; start a new Claude session; `superclaude doctor`; `superclaude install --list`; `/sc:graph status` | `doctor` passes; `install --list` shows the codegraph block; `/sc:graph status` reports an index state. |
+| G8 | Release-specific checks | before merge, unless the owner names a check that needs the merge commit or GitHub state | Whatever checks the owner names for this release | Each one passes and its result is recorded where the owner asked. For v5.0.0 these were the post-merge codegraph check and the QA-loop findings (`RELEASE-READINESS.md` section 6.2). |
+| G9 | No open PR meant for this release | after merge | `gh pr list --repo IronbellyOrg/IronClaude --state open` | Only PRs that were deferred to a later release are open. |
 
 Notes on G7:
 

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.

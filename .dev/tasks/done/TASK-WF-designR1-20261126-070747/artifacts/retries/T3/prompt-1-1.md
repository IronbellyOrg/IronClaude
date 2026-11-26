5a74033ec8953d9e645e7111237db8f3b1f6b009
Review one task for spec compliance.

Task brief: ## Task 3: Rewrite Step 4, add Step 5 (merge-back), renumber the post-release step to Step 6, add the Sources row

Depends on: Task 2

Edit `docs/developer-guide/release-procedure.md`, sections Step 4, the old Step 5, and Sources (design section 3.1 in `./source.md`, "Step 4", "Step 5", "Step 6").

- Step 4 keeps its first sentence ("never a later `master` commit"). Replace the command block with the lines below, and add the text: the first two commands must print nothing (the tag must not exist locally or on `origin`); the `ls-remote` line and the `rev-parse` line must both print `<merge-sha>` before `gh release create` runs; the `ls-remote` pattern must name `^{}`; run the lines one at a time and stop at the first failure.

```bash
git tag --list vX.Y.Z
git ls-remote --tags origin vX.Y.Z
git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>" && git push origin vX.Y.Z
git ls-remote origin 'refs/tags/vX.Y.Z^{}'
git rev-parse vX.Y.Z^{commit}
gh release create vX.Y.Z --verify-tag --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
```

- Add why `--verify-tag` is there: without it a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch", which is now `integration`, and the `v*` tag ruleset then makes it permanent. Add: never suggest a force push, a tag move or a tag deletion. Keep the `git cat-file -t` and `gh release view` check block and the sentence "Never push the tag to the `upstream` remote".
- Insert a new section `## Step 5: Merge master back into integration` after Step 4, with this block and text: if the first `is-ancestor` already exits 0, record "already merged back" and skip the last two lines; otherwise run all four lines, fetch again and check that the proof exits 0; the merge-back PR should change 0 files; if it changes any file or conflicts, stop and take it to the release owner (a content-carrying sync goes through a branch cut from `origin/integration` that merges `origin/master`, then an ordinary `/sc:pr-submit` PR, outside this procedure); wait for any check the PR shows with `gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`; the same ancestry fact `git merge-base --is-ancestor origin/master origin/integration` is the precondition of the next release (Step 2 precondition).

```bash
git fetch origin master integration --tags
git merge-base --is-ancestor <merge-sha> origin/integration
gh pr create --repo IronbellyOrg/IronClaude --base integration --head master --title "chore(release): merge master into integration after X.Y.Z" --body-file <body-file>
gh pr merge <m> --repo IronbellyOrg/IronClaude --merge
```

- Rename the old `## Step 5: Post-release follow-through` to `## Step 6: Post-release follow-through`. Before the `/sc:post-release vX.Y.Z` block add this block and the reason (a branch cut before the release-prep PR merged carries the old version metadata and `SKILL.md` line 74 then raises a false release-integrity finding); keep the rest of the section and "start the next cycle" text; `/sc:post-release` takes no new flag.

```bash
git fetch origin
git switch -c post-release-vX.Y.Z origin/integration
```

- Add one row to the Sources table: "Branch rules, tag rules and merge method" with the sources `docs/developer-guide/branch-protection.md` and `.github/rulesets/`. Cite no file under `.dev/brainstorms/` or `.dev/issues/`.

Acceptance criteria:
- The page contains each block above verbatim, includes `--verify-tag`, and contains the headings `## Step 5: Merge master back into integration` and `## Step 6: Post-release follow-through` in that order after `## Step 4: Tag and publish`.
- `grep -n '## Step 5: Post-release' docs/developer-guide/release-procedure.md` prints nothing.
- No fenced line on the page starts with `gh ` without the fork form, and none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line.
- `grep -n '.dev/brainstorms\|.dev/issues' docs/developer-guide/release-procedure.md` prints nothing.


AC ids (source order):
T3.AC1 = The page contains each block above verbatim, includes `--verify-tag`, and contains the headings `## Step 5: Merge master back into integration` and `## Step 6: Post-release follow-through` in that order after `## Step 4: Tag and publish`.
T3.AC2 = `grep -n '## Step 5: Post-release' docs/developer-guide/release-procedure.md` prints nothing.
T3.AC3 = No fenced line on the page starts with `gh ` without the fork form, and none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line.
T3.AC4 = `grep -n '.dev/brainstorms\|.dev/issues' docs/developer-guide/release-procedure.md` prints nothing.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 5a74033ec8953d9e645e7111237db8f3b1f6b009
Diff against the start snapshot: diff --git a/docs/developer-guide/release-procedure.md b/docs/developer-guide/release-procedure.md
index 68ac48f8a..8b76e3c46 100644
--- a/docs/developer-guide/release-procedure.md
+++ b/docs/developer-guide/release-procedure.md
@@ -139,11 +139,18 @@ Notes on G7:
 After G1-G9 all pass, tag the release PR's merge commit (never a later `master` commit) with an annotated tag, push the tag to `origin`, and create the GitHub release from the release notes:
 
 ```bash
-git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>"
-git push origin vX.Y.Z
-gh release create vX.Y.Z --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
+git tag --list vX.Y.Z
+git ls-remote --tags origin vX.Y.Z
+git tag -a vX.Y.Z <merge-sha> -m "Release vX.Y.Z - <short description>" && git push origin vX.Y.Z
+git ls-remote origin 'refs/tags/vX.Y.Z^{}'
+git rev-parse vX.Y.Z^{commit}
+gh release create vX.Y.Z --verify-tag --repo IronbellyOrg/IronClaude --title "vX.Y.Z - <short description>" --notes-file docs/releases/vX.Y.Z.md
 ```
 
+Run the lines one at a time and stop at the first failure. The first two commands must print nothing: the tag must not exist locally or on `origin`. The `ls-remote` line, whose pattern names `^{}` so that it shows the commit the annotated tag points to, and the `rev-parse` line must both print `<merge-sha>` before `gh release create` runs.
+
+`--verify-tag` is there because without it a failed push lets `gh release create` build a lightweight tag "from the latest state of the default branch", which is now `integration`, and the `v*` tag ruleset then makes that tag permanent. Never suggest a force push, a tag move or a tag deletion.
+
 Check the result:
 
 ```bash
@@ -155,9 +162,29 @@ gh release view vX.Y.Z --repo IronbellyOrg/IronClaude
 
 Never push the tag to the `upstream` remote.
 
-## Step 5: Post-release follow-through
+## Step 5: Merge master back into integration
+
+The release PR put the merge commit on `master`. `integration` must contain it, or the next release starts from a diverged history:
+
+```bash
+git fetch origin master integration --tags
+git merge-base --is-ancestor <merge-sha> origin/integration
+gh pr create --repo IronbellyOrg/IronClaude --base integration --head master --title "chore(release): merge master into integration after X.Y.Z" --body-file <body-file>
+gh pr merge <m> --repo IronbellyOrg/IronClaude --merge
+```
+
+If the first `is-ancestor` already exits 0, record "already merged back" and skip the last two lines. Otherwise run all four lines, fetch again, and check that the proof exits 0. The merge-back PR should change 0 files. If it changes any file or conflicts, stop and take it to the release owner: a content-carrying sync goes through a branch cut from `origin/integration` that merges `origin/master`, then an ordinary `/sc:pr-submit` PR, outside this procedure. Wait for any check the PR shows with `gh pr checks <m> --repo IronbellyOrg/IronClaude --watch`. The same ancestry fact, `git merge-base --is-ancestor origin/master origin/integration`, is the precondition of the next release (the Step 2 precondition).
+
+## Step 6: Post-release follow-through
+
+Once the tag exists and `master` is merged back, cut a branch from `origin/integration`:
+
+```bash
+git fetch origin
+git switch -c post-release-vX.Y.Z origin/integration
+```
 
-Once the tag exists, run in Claude Code:
+A branch cut before the release-prep PR merged carries the old version metadata, and `SKILL.md` line 74 of `sc-post-release-protocol` then raises a false release-integrity finding. Then run in Claude Code:
 
 ```text
 /sc:post-release vX.Y.Z
@@ -182,3 +209,4 @@ Then start the next cycle: keep adding changes under `## [Unreleased]` in `CHANG
 | What `./update.sh` runs | `update.sh:7-10` |
 | `/sc:post-release` input and output | `src/superclaude/commands/post-release.md:15,18,35-36` |
 | `/sc:graph status` | `src/superclaude/commands/graph.md:8,21,31` |
+| Branch rules, tag rules and merge method | `docs/developer-guide/branch-protection.md` and `.github/rulesets/` |

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

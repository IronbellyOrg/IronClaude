1ddb1d7ec753a67e29dab2ddb3f0fc8de8ab7d6c
Review one task for spec compliance.

Task brief: ## Task 7: Rewrite the ancestry check in sc-post-release-protocol/SKILL.md

Edit `src/superclaude/skills/sc-post-release-protocol/SKILL.md` (design section 3.2 in `./source.md`). Read the file first; the line numbers below were checked on 2026-11-26.

- Line 91, the paragraph that starts `**Anchor the scan to the tagged commit.**`: keep everything up to and including "...removed with `git worktree remove` after the scan." and replace the rest of the paragraph (from "Confirm the tag actually belongs...") with: "Confirm the tag actually belongs to the release lineage. Resolve the default branch `<default-branch>` live with `git ls-remote --symref origin HEAD` (the `ref: refs/heads/<name>` line gives `<name>`); only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`, which can be stale. Record the value and which source gave it. Then run `git fetch origin <default-branch> --tags` and `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`; never compare against a bare local branch name, which can be far behind its remote. If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. If the tag is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding; with the finding, list the remote branches that contain the tag (`git branch -r --contains <tag>`, without the `origin/HEAD ->` alias line, at most 10, say when the list is cut off; when none: \"no remote branch contains `<tag>`\") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. Never hard-code a branch name." The paragraph must then contain none of the whole words `main`, `master` or `integration` (the word "mainline" is allowed).
- Line 74 (the WARN line ending "then continue, anchored to the tag."): unchanged.
- Line 103 (`**Output:** resolved tag + auto-detected default branch + ...`): "auto-detected default branch" becomes "default branch (resolved live, with its source)".
- Line 105 (`**Exit criteria:** tag anchored, default branch auto-detected, ...`): "default branch auto-detected" becomes "default branch resolved and its source recorded".
- Guardrails, lines 347 and 348: "work on a feature branch off the repo's **auto-detected default branch**" becomes "work on a feature branch off the default branch resolved in Wave 1"; the "PR target" bullet's "with `--base <default-branch>`" gets the addition "(the Wave 1 value; a value that came from the offline fallback is never used as a PR base: ask the user)".
- No change to `argument-hint` (line 5) and none to `src/superclaude/commands/post-release.md`.

Acceptance criteria:
- The paragraph at line 91 contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`, and the file no longer contains `git merge-base --is-ancestor <tag> <default-branch>`.
- `grep -n '[[:space:]]src/superclaude' src/superclaude/skills/sc-post-release-protocol/SKILL.md` shows no new hit compared with `git show HEAD:src/superclaude/skills/sc-post-release-protocol/SKILL.md`.
- `git diff --stat -- src/superclaude/commands/post-release.md` prints nothing.


AC ids (source order):
T7.AC1 = The paragraph at line 91 contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`, and the file no longer contains `git merge-base --is-ancestor <tag> <default-branch>`.
T7.AC2 = `grep -n '[[:space:]]src/superclaude' src/superclaude/skills/sc-post-release-protocol/SKILL.md` shows no new hit compared with `git show HEAD:src/superclaude/skills/sc-post-release-protocol/SKILL.md`.
T7.AC3 = `git diff --stat -- src/superclaude/commands/post-release.md` prints nothing.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 1ddb1d7ec753a67e29dab2ddb3f0fc8de8ab7d6c
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-post-release-protocol/SKILL.md b/src/superclaude/skills/sc-post-release-protocol/SKILL.md
index 452f87102..c8f44289f 100644
--- a/src/superclaude/skills/sc-post-release-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-post-release-protocol/SKILL.md
@@ -88,7 +88,7 @@ Three design choices make this reliable rather than theatrical:
 
 **Entry criteria:** the raw `<version>` argument has been validated in Wave 0.
 
-**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage (`git merge-base --is-ancestor <tag> <default-branch>`); if it is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding. **Auto-detect the default branch** (e.g. `git symbolic-ref refs/remotes/origin/HEAD`) — do not assume `main`/`master`.
+**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage. Resolve the default branch `<default-branch>` live with `git ls-remote --symref origin HEAD` (the `ref: refs/heads/<name>` line gives `<name>`); only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`, which can be stale. Record the value and which source gave it. Then run `git fetch origin <default-branch> --tags` and `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`; never compare against a bare local branch name, which can be far behind its remote. If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. If the tag is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding; with the finding, list the remote branches that contain the tag (`git branch -r --contains <tag>`, without the `origin/HEAD ->` alias line, at most 10, say when the list is cut off; when none: "no remote branch contains `<tag>`") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. Never hard-code a branch name.
 
 ### Two run modes (auto-detect — do not ask)
 
@@ -100,9 +100,9 @@ Detect the mode from whether a prior manifest exists for this repo. Search these
 
 State the detected mode and the evidence for it (found manifest path, or "none found → ground-up") in the report's header. When in genuine doubt, prefer ground-up for a workstream (a full pass is safe; a skipped delta is a silent gap).
 
-**Output:** resolved tag + auto-detected default branch + chosen run-mode (ground-up vs additive) + located release artifacts.
+**Output:** resolved tag + default branch (resolved live, with its source) + chosen run-mode (ground-up vs additive) + located release artifacts.
 
-**Exit criteria:** tag anchored, default branch auto-detected, run-mode ground-up vs additive chosen with stated evidence, release artifacts located.
+**Exit criteria:** tag anchored, default branch resolved and its source recorded, run-mode ground-up vs additive chosen with stated evidence, release artifacts located.
 
 ---
 
@@ -344,8 +344,8 @@ On completion, report these fields (and emit the RESULT header above) for a call
 
 ## Guardrails
 
-- **Branch discipline** — work on a feature branch off the repo's **auto-detected default branch**; never commit directly to that branch. Commit/push only when the user asks.
-- **PR target** — open PRs against the repo's own `origin`, with `--base <default-branch>` and its contribution conventions. **Never retarget a PR at anything other than `origin`** (a fork's upstream, or any other repo) without explicit user authorization in the same session. A wrong PR target is a high-cost mistake — especially when a plausible sibling repo exists in the same org, which is exactly when a hardcoded owner/name would misfire. Resolve the target from `git remote -v` at runtime, never from memory.
+- **Branch discipline** — work on a feature branch off the default branch resolved in Wave 1; never commit directly to that branch. Commit/push only when the user asks.
+- **PR target** — open PRs against the repo's own `origin`, with `--base <default-branch>` (the Wave 1 value; a value that came from the offline fallback is never used as a PR base: ask the user) and its contribution conventions. **Never retarget a PR at anything other than `origin`** (a fork's upstream, or any other repo) without explicit user authorization in the same session. A wrong PR target is a high-cost mistake — especially when a plausible sibling repo exists in the same org, which is exactly when a hardcoded owner/name would misfire. Resolve the target from `git remote -v` at runtime, never from memory.
 - **Never stage machine-generated / sync-output dirs** — respect whatever the host repo marks as generated or vendored (check its `.gitignore` and docs) and don't `git add` those paths. Note the convention varies: some repos gitignore such dirs, others commit them — follow the host repo's actual practice, don't assume.
 - **No secrets, ever** — deploy creds/tokens live only on the target host. Never write them into docs, scripts, transcripts, or the manifest. Scrub any that appear in an e2e transcript before saving it.
 - **Confirm outward-facing / hard-to-reverse actions** — provisioning a VM, running install scripts against a real target, committing, and opening a PR all get confirmed first unless the user pre-authorized them this session.

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

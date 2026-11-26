2641bb1a17f804be6b3dee862253d180d9622b18
Review one task for spec compliance.

Task brief: ## Task 13: Record the GitHub rehearsal status, prepare its command file and post the evidence

Depends on: Task 12

Create `./artifacts/rehearsal-github.md` (design section 3.6, part 2, in `./source.md`). A scratch repository on GitHub is an outward action: do not create a repository, push, tag, merge or open a pull request unless the owner has approved it explicitly in this session. Commands that touch `./artifacts/` run with the package folder as the working directory.

- Write the commands of Steps 2 to 6 of `docs/developer-guide/release-procedure.md` with the substitutions made for a scratch repository: the only allowed substitutions are the repository name `<scratch-owner>/<scratch-repo>` and a tag that does not start with `v`. Save them as `./artifacts/rehearsal-github-commands.sh.txt` (a text file, not an executable).
- Check that `grep -n 'IronbellyOrg/IronClaude' ./artifacts/rehearsal-github-commands.sh.txt` prints nothing, and list the checks the run must show: a missed substitution is rejected before it runs; `git remote -v` names the scratch repository before any push, run in the same shell call as the `git tag` and `git push` inside the scratch clone (`git -C <absolute scratch clone>` or a `cd` at the start of the call, as in Task 12), with `git rev-parse --show-toplevel` logged; `gh pr merge --match-head-commit` behaviour; `gh pr view` fields; `gh run list --commit`; `gh release create --verify-tag` rejecting a tag that is not on the remote; what `gh pr checks --watch` prints and returns for a PR with no checks; an idempotent merge-back; `master` moving between Step 2 and the merge stopping the tag; a content-carrying merge-back stopping; G5 to G8 recorded as not exercised.
- If the owner approved the run in this session, run it and record the evidence (PR ids, SHAs, parent checks, CI evidence, unperformed checks). If not, write at the top of the file: "Status: not exercised (needs the owner's approval to create a scratch repository)". Either way the file lists which acceptance point of issue 826 is met and which is partly met.
- After `./artifacts/rehearsal-github.md` exists, post the evidence on the issue: write `./artifacts/issue-comment-body.md` holding the text of `./artifacts/rehearsal-local.md` followed by the text of `./artifacts/rehearsal-github.md`. Only with the owner's explicit approval in this session for this posting (approval of a scratch repository is not approval to post), post it once with `gh issue comment 826 --repo IronbellyOrg/IronClaude --body-file ./artifacts/issue-comment-body.md` and record the comment URL in `./artifacts/issue-comment.md`. Without that approval, `./artifacts/issue-comment.md` starts with `Status: not posted (needs the owner's approval)`, holds the ready command, and the plan states that issue 826's rehearsal criterion stays partly met. Post nothing until the location proof of Task 12 is in the local log.

Acceptance criteria:
- `./artifacts/rehearsal-github.md` and `./artifacts/rehearsal-github-commands.sh.txt` exist; the commands file contains no `IronbellyOrg/IronClaude` text.
- `./artifacts/rehearsal-github.md` starts with a `Status:` line that says either `exercised` with evidence or `not exercised (needs the owner's approval to create a scratch repository)`.
- `./artifacts/issue-comment.md` exists and holds either the comment URL or the line `Status: not posted (needs the owner's approval)` with the ready command; no issue comment was posted unless that file records the owner's approval.
- No GitHub repository, pull request, tag or release was created by this task unless the file records the owner's approval.


AC ids (source order):
T13.AC1 = `./artifacts/rehearsal-github.md` and `./artifacts/rehearsal-github-commands.sh.txt` exist; the commands file contains no `IronbellyOrg/IronClaude` text.
T13.AC2 = `./artifacts/rehearsal-github.md` starts with a `Status:` line that says either `exercised` with evidence or `not exercised (needs the owner's approval to create a scratch repository)`.
T13.AC3 = `./artifacts/issue-comment.md` exists and holds either the comment URL or the line `Status: not posted (needs the owner's approval)` with the ready command; no issue comment was posted unless that file records the owner's approval.
T13.AC4 = No GitHub repository, pull request, tag or release was created by this task unless the file records the owner's approval.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 2641bb1a17f804be6b3dee862253d180d9622b18
Diff against the start snapshot: (empty diff)
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

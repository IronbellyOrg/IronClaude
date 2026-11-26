99ee2eba4749638d5854a5c8b0c4318b6e1109e7
Review one task for spec compliance.

Task brief: ## Task 12: Run the local git rehearsal and write its log

Depends on: Task 11

Reproduce the written release steps and the skill's Wave 1 check in a temporary local repository and write the log to `./artifacts/rehearsal-local.md` (design section 3.6, part 1, in `./source.md`). The design's log path `.dev/issues/826/rehearsal-local.md` is overridden: the package is always staged, and the issue comment of Task 13 reads the file from `./artifacts/`. No GitHub call, no push to any real remote, no tag in the real repository. Use `mktemp -d` for the working directory and remove it at the end (nothing from it is committed). Commands that touch `./artifacts/` run with the package folder as the working directory.

- State before the run: before the run record into `./artifacts/t12-state-before.txt` (and, before any fix sent back to Task 1, 2, 3 or 7, into the next numbered file `./artifacts/t12-state-before-2.txt`, then `-3`; never overwrite a recorded file) the output of `git status --short --untracked-files=all`, `git rev-parse HEAD`, `git symbolic-ref -q refs/remotes/origin/HEAD` and `git tag --list 'rehearsal-*'` for the real repository (run each as `git -C "$(git rev-parse --show-toplevel)" ...` so the answer does not depend on the working directory).
- Location guard: every rehearsal git command runs as `git -C <absolute temporary clone>` or inside one shell call that starts with `cd` into the temporary folder; never rely on a previous call's folder or variables. Log `git rev-parse --show-toplevel` with each check and confirm it equals the temporary clone; before any push confirm `git remote get-url origin` prints the temporary bare repository. A missing or mismatched location invalidates the check, and the log must not be posted as evidence.
- Set up a bare repository as `origin` whose `HEAD` points to `refs/heads/integration`, with branches `integration` and `master`, and a clone of it. Use a tag name that does not start with `v`, for example `rehearsal-0.0.0`.
- Step 2 precondition: after a merge of `integration` into `master` made with `git merge --no-ff` (the stand-in for a GitHub merge commit; it has the same two-parent shape and does not prove `gh pr merge`), `git merge-base --is-ancestor origin/master origin/integration` exits 1; after the merge-back it exits 0.
- Step 3 capture: for the no-ff merge the `^2` line prints a hash, `^3` prints nothing and exits 1, `^1` equals the recorded master tip and `^2` equals the recorded head, and the two trees are equal; for a squash-shaped commit there is no `^2`; when `master` gets an extra commit between the recorded tip and the merge, the `^1` check fails.
- Step 4: the tag does not exist locally or on `origin` before tagging; after `git tag -a <tag> <merge-sha> && git push origin <tag>`, `git ls-remote origin 'refs/tags/<tag>^{}'` and `git rev-parse <tag>^{commit}` both print the merge SHA; `git ls-remote --tags origin <tag>` without `^{}` prints the tag object instead.
- Step 5: the proof `git merge-base --is-ancestor <merge-sha> origin/integration` exits 1 before the merge-back and 0 after, still 0 after a newer commit lands on `integration`, and a second run records "already merged back".
- Skill Wave 1 check: `git ls-remote --symref origin HEAD` prints `ref: refs/heads/integration`; with a stale local `integration` branch (behind `origin/integration`), `git merge-base --is-ancestor <tag> integration` exits 1 while `git merge-base --is-ancestor <tag> refs/remotes/origin/integration` exits 0 after a fetch; with `refs/remotes/origin/HEAD` set to `master` the offline fallback resolves `master`, which must be reported as unverified.
- The log lists each command, its output, its exit code, and passed, failed or not exercised; the GitHub-only items (`gh pr merge --match-head-commit`, `gh pr view` fields, `gh run list --commit`, `gh release create --verify-tag`, `gh pr checks --watch` with no checks) are listed as not exercised here.
- State after the run: record the same four outputs into `./artifacts/t12-state-after.txt` (after a fix round, into the matching numbered file `./artifacts/t12-state-after-2.txt`, then `-3`), and compare the pair as the acceptance criteria say before any fix is sent back.
- A mismatch between a written step and the log is a document defect: fix it in Task 1, 2, 3 or 7, then run again the pytest commands of Tasks 6 and 8 and `make sync-dev && make verify-sync` (Task 11) and record the next numbered state pair.

Acceptance criteria:
- `./artifacts/rehearsal-local.md` exists and contains a command, output and exit code for each bullet above, each check marked passed, failed or not exercised, and the `git rev-parse --show-toplevel` output of each check, equal to the temporary clone.
- Every check that the written procedure or skill text claims (exit codes, printed values) matches what the log shows; a mismatch is fixed as the last bullet says before this task is accepted.
- `./artifacts/t12-state-before.txt` and `./artifacts/t12-state-after.txt` exist (plus one numbered pair per fix round); in every pair, compared before the next fix is made, the HEAD id, the `origin/HEAD` symbolic ref and the rehearsal tag list are identical in both, and the status lines differ only for paths inside this package's folder (its ledger, staging, `./artifacts/`). `integration` and `master` ids are not compared (other worktrees move them). On an unexplained mismatch the task stops and reports failure or concurrent interference; it does not restore shared refs or erase files.


AC ids (source order):
T12.AC1 = `./artifacts/rehearsal-local.md` exists and contains a command, output and exit code for each bullet above, each check marked passed, failed or not exercised, and the `git rev-parse --show-toplevel` output of each check, equal to the temporary clone.
T12.AC2 = Every check that the written procedure or skill text claims (exit codes, printed values) matches what the log shows; a mismatch is fixed as the last bullet says before this task is accepted.
T12.AC3 = `./artifacts/t12-state-before.txt` and `./artifacts/t12-state-after.txt` exist (plus one numbered pair per fix round); in every pair, compared before the next fix is made, the HEAD id, the `origin/HEAD` symbolic ref and the rehearsal tag list are identical in both, and the status lines differ only for paths inside this package's folder (its ledger, staging, `./artifacts/`). `integration` and `master` ids are not compared (other worktrees move them). On an unexplained mismatch the task stops and reports failure or concurrent interference; it does not restore shared refs or erase files.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 99ee2eba4749638d5854a5c8b0c4318b6e1109e7
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

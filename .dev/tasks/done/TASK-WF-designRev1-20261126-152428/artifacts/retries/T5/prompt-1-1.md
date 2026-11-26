126fffb073b60abf5ead5b827e91bb28024848d0
Review one task for spec compliance.

Task brief: ## Task 5: Write the audit record for coder_orca

Write `.dev/issues/837/audit/coder_orca.md` following the block list of section 3.4 of `./source.md` with `REPO=coder_orca` (a non-fork repo where `clayphi` has admin), using only read-only `gh api` GET calls. Record in order: the header (`END` from `date -u +%Y-%m-%dT%H:%M:%SZ` and `START` 90 days before it); the preflight (`gh api user --jq .login`, and `permissions.admin`, `default_branch`, `archived`, `private` of the repo); the counts (`hooks`, `keys`, `branches/main/protection`, and `gh api --paginate orgs/IronbellyOrg/installations`, written as "could not run" with the real error text if it fails); the existing ruleset list; the tip SHA of `main`; the events of `refs/heads/main` for the 90 days from the activity endpoint with `time_period=year`, each classified as direct push by human, direct push by automation, sync, pr_merge or branch_creation; the tag evidence (count of `v*` refs read over every page with `--paginate`, summing the per-page counts; the statement that the activity endpoint shows no tag events); the producer search; the blocks table; the result `CLEAR` or `BLOCKED`; and the revert commands with an empty id column.

For the producer search the tag ruleset is a fixed skip for this repo (E-2 of the merged requirements). Confirm it by reading the private repository's release tooling that E-2 names, with the read-only contents call, and keep the decoded text out of every output: redirect it to a file or a shell variable, never print it, and write what matched only to `.dev/issues/837/private/coder_orca-producer-evidence.md` (never staged). In the audit file record only the neutral sentence of the constraints, a yes or no for "the tooling deletes `v*` tags" and the number of matching lines, and whether `.github/workflows` exists in coder_orca. Also write `.dev/issues/837/private/guard-patterns.txt`, one fixed string per line with no blank line, holding the file name, the folder name and each tag-deleting function that E-2 lists written in its call form (the name followed by its opening parenthesis, as it appears in the tooling), never a bare word that is also an ordinary English word; Task 13 uses it as a pre-stage guard. Neither private file may be staged.

Acceptance criteria:
- `.dev/issues/837/audit/coder_orca.md` exists and has every block of section 3.4 (header, preflight, counts, existing rulesets, tips, events kept, tag evidence, producer search, blocks, result, revert commands); the fork test block says "not a fork".
- `END` and `START` are written down, the `main` tip SHA is a 40-character value, and every kept event row has a classification.
- The installations read is recorded as "could not run" with the error text (or its output if it ran), and the blocks table lists it with who clears it.
- The tag ruleset decision for this repo is "skip" with the neutral sentence, and `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/coder_orca.md` prints 0.
- `.dev/issues/837/private/coder_orca-producer-evidence.md` and `.dev/issues/837/private/guard-patterns.txt` exist, `test -s .dev/issues/837/private/guard-patterns.txt` succeeds, `wc -l` of that file equals the number of names E-2 lists (one line per name, no blank line), and `git status --short .dev/issues/837` is the only place they show (the folder is never staged).
- The last section of the audit file lists every command run, and none is POST, PUT or DELETE; the private contents read is written there only as "contents read of the private release tooling (path in `private/`)", with no path, file or folder name.
Global constraints: ## Constraints

- This plan only writes files in this worktree and runs read-only `gh api` GET calls. No task may send POST, PUT or DELETE to any GitHub ruleset, create a branch or ruleset in another repository, comment on an issue or edit a pull request. Applying rulesets is "Phase 3" of `./source.md` section 4 and is carried out from the runbook that Task 13 produces, after the pull request monitor has settled, never by `/sc:implement`.
- Never write to IronHands-CLI, irondots, ironops-marketplace, the archived IronHands repo, or any repository outside IronbellyOrg. Every `gh` call names its repository in full (`repos/IronbellyOrg/<repo>/...`, or `--repo IronbellyOrg/IronClaude`) except `gh api user`; never rely on the fork-parent default and never touch `SuperClaude-Org/SuperClaude_Framework`.
- Where `./source.md` section 2 names the four state files, this plan writes them there and nowhere else: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`. They are never staged. The drafted pull request body goes to `.dev/issues/837/pr-body.md`. The package `./artifacts/` folder holds only the codegraph grounding note. The results of the later apply are recorded in the audit file and the ledger, as section 3.6 of `./source.md` says; there is no separate apply-results file.
- IronClaude is public and `IronbellyOrg/Coder` is private (Revision 1 of `./source.md`). Nothing that describes the internals of the private repository's release tooling (its file name, folder, function names, lines or line numbers) may be written to any file under `.dev/tasks/`, to any log or QA output captured there, to the pull request body or to an issue comment. The only neutral sentence allowed in such places is: "release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca". Task 5 reads the tooling without printing or saving its lines and keeps the evidence only in `.dev/issues/837/private/`, which is never staged. Those names are not written in this plan: E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` lists them.
- Do not create `.github/rulesets/other-repos/protect-aidev02.json`: it needs Clay's written yes for `aidev02`, which is not recorded in `.dev/issues/837/issue-summary.md`.
- IronClaude's three existing files `.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json` and the live IronClaude rulesets stay unchanged. Every existing assertion in `tests/docs/test_branch_protection_rulesets.py` stays.
- Facts that nobody verified stay labelled UNVERIFIED in every file this plan writes: whether the Sync fork button is refused under a `pull_request` rule, whether `clayphi`'s token can create rulesets, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether `time_period=quarter` is 90 days (it is not used).
- A check that cannot run (for example `gh api --paginate orgs/IronbellyOrg/installations`, which needs the `admin:org` scope) is written down as "could not run" with the real error text and blocks the repo it covers; it is never recorded as clean.
- Clay's recorded answer is in `.dev/issues/837/issue-summary.md` under "Decided for this work (iteration 3)". It is quoted word for word wherever a task says to quote it, never paraphrased. The lead's note in it, that the release-tag ruleset has its `update` rule on integration (pull request 844 merged), was verified before this plan: `.dev/issues/837/accuracy-check.md` line 13 records commit 206abea1c and the live ruleset 28081842 with `update`.
- This plan does not commit or push. Those are later story steps.
Start sha: 126fffb073b60abf5ead5b827e91bb28024848d0
Diff against the start snapshot: Changed files (name-status):
A	.dev/issues/837/audit/coder_orca.md


diff --git a/.dev/issues/837/audit/coder_orca.md b/.dev/issues/837/audit/coder_orca.md
new file mode 100644
index 000000000..e7ed64f7e
--- /dev/null
+++ b/.dev/issues/837/audit/coder_orca.md
@@ -0,0 +1,125 @@
+# Audit record: IronbellyOrg/coder_orca
+
+Phase 1, read-only (issue 837, section 3.4 of the design). `REPO=coder_orca`, `BRANCH=main`. Only `gh api` GET calls were made. Never staged.
+
+## Header
+
+| Item | Value |
+|---|---|
+| `END` | `2026-11-26T15:38:27Z` (from `date -u +%Y-%m-%dT%H:%M:%SZ`) |
+| `START` | `2026-08-28T15:38:27Z` (from `date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ`) |
+| Audited ref | `refs/heads/main` |
+
+## Preflight
+
+| Check | Result |
+|---|---|
+| `gh api user --jq .login` | `clayphi` |
+| `permissions.admin`, `default_branch`, `archived`, `private` | `true`, `main`, `false`, `false` (public repository, `clayphi` has admin) |
+
+## Counts
+
+| Read | Result |
+|---|---|
+| `repos/IronbellyOrg/$REPO/hooks --jq length` | `0` |
+| `repos/IronbellyOrg/$REPO/keys --jq length` | `0` |
+| `repos/IronbellyOrg/$REPO/branches/main/protection` | HTTP 404, `{"message":"Branch not protected"}` (expected: no classic protection) |
+| `gh api --paginate orgs/IronbellyOrg/installations` | **could not run.** Real error text: `gh: Not Found (HTTP 404)` followed by `gh: This API operation needs the "admin:org" scope. To request it, run: gh auth refresh -h github.com -s admin:org`. Not recorded as clean; it is listed in Blocks. |
+
+## Existing rulesets
+
+`gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'` printed nothing: no rulesets exist (expected).
+
+## Fork test
+
+Not a fork (`gh api repos/IronbellyOrg/$REPO --jq .fork` prints `false`). There is no parent, so no parent comparison, no `sync` events, no tag comparison against a parent, and the mirror ruleset file is not used for this repo (the full file `protect-main.json` is the candidate).
+
+## Tips
+
+| Branch | Command | SHA (40 characters) |
+|---|---|---|
+| `main` | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha` | `cf8ab379d51dfc12b70ae90f97e07d80c659d0aa` |
+
+The repository root holds one file, `README.md` (`gh api repos/IronbellyOrg/$REPO/contents --jq '.[].name'`).
+
+## Events kept
+
+Command: `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.after] | @tsv'`. `time_period=quarter` was not used (its length is UNVERIFIED).
+
+Classification method: `activity_type` is read from each row. `branch_creation` rows are classed `branch_creation`. A `push` row is classed `direct push by human` unless the actor login ends in `[bot]` or is a known automation such as github-actions (`direct push by automation`); a push whose commit is a merge made through a pull request is classed `pr_merge`, checked with `gh api repos/IronbellyOrg/$REPO/commits/<sha>/pulls`. `sync` is a parent fast-forward on a fork `main`; this repository is not a fork, so there are none.
+
+Rows kept in the window `START` to `END`: 1. The same endpoint with no date filter (the whole `time_period=year` answer) also returned exactly this one row, so no row was dropped by the filter.
+
+| Timestamp | Ref | Activity type | Actor | After SHA | Classification |
+|---|---|---|---|---|---|
+| 2026-09-18T05:56:44Z | refs/heads/main | branch_creation | ironbelly | `cf8ab379d51dfc12b70ae90f97e07d80c659d0aa` | `branch_creation` |
+
+Counts by class: direct push by human 0, direct push by automation 0, sync 0, pr_merge 0, branch_creation 1. No push row exists, so the `commits/<sha>/pulls` check was not needed. The `after` SHA of the one row equals the current tip of `main`.
+
+## Tag evidence
+
+- Number of `v*` refs: **16**. Command: `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` printed one per-page count, `16` (one page); the sum of the per-page counts is 16.
+- The activity endpoint shows no tag events, so tag writes are invisible to this audit (INV-009).
+- Not a fork: there is no parent tag to compare against.
+
+## Producer search
+
+| Place | Hit | How resolved |
+|---|---|---|
+| Workflows of the repository (`gh api repos/IronbellyOrg/$REPO/contents/.github/workflows`) | `.github/workflows` does not exist: HTTP 404 `Not Found`; the repository root holds only `README.md` | Resolved by the 404 and the root listing, not by absence of grep output. No in-repository tag mover exists. |
+| Another IronbellyOrg repository that holds a release token for this target (E-2 of the merged requirements, `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md`) | The tooling deletes `v*` tags: **yes** (count redacted before staging) | Contents read of the private release tooling (path in `private/`), decoded to a temporary file and never printed; matching lines and line numbers are kept only in `.dev/issues/837/private/coder_orca-producer-evidence.md`. The result does not rest on absence of grep output: the tag-deleting lines were located (detail redacted before staging), and a tag name that starts with `v` was confirmed by a count. The lines themselves were not displayed. |
+| How tags arrive from a parent | None: not a fork | Resolved by the fork test. |
+
+Search terms used on the tooling: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`, plus the target repository name. Whether the tooling is run against this repository today, and how often, is UNVERIFIED. A name built at run time would defeat grep, which is why the match was tied to the line ranges E-2 names.
+
+Decision for the tag ruleset on this repository: **skip**. Release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca.
+
+## Blocks
+
+| Ruleset | Missing check or event | Who clears it | What clears it |
+|---|---|---|---|
+| `protect-main` (branch, `refs/heads/main`) | `gh api --paginate orgs/IronbellyOrg/installations` could not run (needs the `admin:org` scope; `clayphi`'s token lacks it) | An organisation owner of IronbellyOrg, or Clay in writing | An organisation owner runs the read and records its output here, or Clay's written acceptance of the missing read is quoted from `.dev/issues/837/issue-summary.md` (no such acceptance is recorded there today) |
+| `protect-release-tags` (tag, `refs/tags/v*`) | None. Skipped by decision, not blocked | Not applicable | Not applicable: the tag ruleset is not applied to this repository (see Producer search) |
+
+## Result
+
+**BLOCKED.**
+
+Reasons:
+1. The installations read could not run (HTTP 404, `admin:org` scope missing), and it is not recorded as clean. Nothing in `.dev/issues/837/issue-summary.md` records Clay's written acceptance of its absence.
+
+For the record, the other checks are clean: `hooks` 0, `keys` 0, no classic branch protection, no existing ruleset, and one event in 90 days (`branch_creation`; no direct push by a human or by automation, no `pr_merge`). The tag ruleset is skipped.
+
+## Revert commands
+
+Written before any write on this repository. The id column is empty until apply. Only the branch ruleset may be created; the tag ruleset is skipped, so it has no revert line.
+
+| Ruleset | Revert command | Id |
+|---|---|---|
+| `protect-main` | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=coder_orca` | |
+
+## Self-test of the record
+
+UNVERIFIED and not run in Phase 1: whether `clayphi`'s token can create rulesets on this repository, and whether the API accepts a duplicate ruleset name.
+
+## Commands run
+
+All are read-only GET calls (none is POST, PUT, PATCH or DELETE). `REPO=coder_orca`; `END` and `START` as in the header; `W` is a private temporary directory under `/tmp` (outputs were captured there and the decoded private text was never printed).
+
+1. `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)`; `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`
+2. `gh api user --jq .login`
+3. `gh api repos/IronbellyOrg/$REPO --jq '[.permissions.admin, .default_branch, .archived, .private] | @tsv'`
+4. `gh api repos/IronbellyOrg/$REPO --jq .fork`
+5. `gh api repos/IronbellyOrg/$REPO/hooks --jq length`
+6. `gh api repos/IronbellyOrg/$REPO/keys --jq length`
+7. `gh api repos/IronbellyOrg/$REPO/branches/main/protection` (HTTP 404)
+8. `gh api --paginate orgs/IronbellyOrg/installations` (HTTP 404, `admin:org` scope missing)
+9. `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'`
+10. `gh api repos/IronbellyOrg/$REPO/git/ref/heads/main --jq .object.sha`
+11. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | select(.timestamp >= "'"$START"'") | [.timestamp,.ref,.activity_type,.actor.login,.after] | @tsv'`
+12. `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/main&time_period=year&per_page=100" --jq '.[] | [.timestamp,.ref,.activity_type,.actor.login] | @tsv'` (the unfiltered cross-check)
+13. `gh api --paginate repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length` (per-page counts summed with `awk '{s+=$1} END{print s}'`)
+14. `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows --jq '.[].name'` (HTTP 404)
+15. `gh api repos/IronbellyOrg/$REPO/contents --jq '.[].name'`
+16. Contents read of the private release tooling (path in `private/`): a read-only `gh api` contents GET, decoded with `jq -r .content | base64 -d` into a temporary file, then counted and searched with `grep -c -F` and `sed -n` inside the same shell script; nothing was printed except counts. Its matches were written to `.dev/issues/837/private/coder_orca-producer-evidence.md`.
+17. Local checks: `printf` to write `.dev/issues/837/private/guard-patterns.txt`; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt .dev/issues/837/audit/coder_orca.md`; `test -s`; `wc -l`; `git check-ignore -v`.


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
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

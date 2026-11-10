0684aa6bcaebef955ce4ae84577c799c0b3cbf4d
Review one task for spec compliance.

Task brief: ## Task 5: Extend the create lookup job of the T3 worker

Depends on: Task 2, Task 4

Edit `src/superclaude/agents/issue-worker-t3.md`. Source sections: decision Q4, specification 2.1 and 2.3. In job 2 "Create lookup" (line 22) add the two reads `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields` (GET only, look up the field named `Complexity` and record its id, data type and option names), and the two new `scout.md` sections from Task 4; a failed read is recorded as `lookup failed: <reason>` and the worker continues. In the Rules section, the "Read-only GitHub access" bullet (line 27) keeps "a path that starts with `repos/<R>/`" and adds the single exception `orgs/<owner of R>/issue-fields` for this lookup only; the ban on writes and on `-X` other than `GET` stays word for word.

Acceptance criteria:
- `issue-worker-t3.md` job 2 names `issue-types`, `issue-fields`, `### Repo issue types` and `### Complexity field`.
- The Read-only GitHub access rule names exactly one `orgs/` path, `orgs/<owner of R>/issue-fields`, and still forbids every write and every `-X` other than `GET`.
- The file contains no brace placeholder and no `src/superclaude/`; the T1 and T2 worker files are untouched (`git diff --stat` shows no change to them).

AC ids:
T5.AC1: `issue-worker-t3.md` job 2 names `issue-types`, `issue-fields`, `### Repo issue types` and `### Complexity field`.
T5.AC2: The Read-only GitHub access rule names exactly one `orgs/` path, `orgs/<owner of R>/issue-fields`, and still forbids every write and every `-X` other than `GET`.
T5.AC3: The file contains no brace placeholder and no `src/superclaude/`; the T1 and T2 worker files are untouched (`git diff --stat` shows no change to them).
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 0684aa6bcaebef955ce4ae84577c799c0b3cbf4d
Diff against the start snapshot: 
diff --git a/src/superclaude/agents/issue-worker-t3.md b/src/superclaude/agents/issue-worker-t3.md
index c547ba49..458f8f1e 100644
--- a/src/superclaude/agents/issue-worker-t3.md
+++ b/src/superclaude/agents/issue-worker-t3.md
@@ -19,12 +19,12 @@ The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `issu
 The orchestrator names one job, the repo `<R>` (`owner/repo`, resolved from `origin`), and the directory `<D>` under `.dev/issues/`.
 
 1. **Claim lookup (claim Wave 1).** Run `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`. List pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url`, and record whether the result reached the 200 limit. Run `git fetch origin`, then `git log --since=<createdAt> --name-only origin/<default branch>`. Find this user's earlier comments whose body contains `<!-- sc:issue:claim -->` or `<!-- sc:issue:accuracy-check -->` and record each comment ID. Write `<D>/scout.md` from the claim section of the `scout-report.md` template: state, `url`, `is_pull_request` (true when `url` contains `/pull/`), assignees, current login, earlier comment IDs, merged pull requests and changed files since creation, whether that list was truncated, and a first complexity guess (`simple|medium|complex`) and type guess (`feature|bug`), each with a one-line reason.
-2. **Create lookup (create Wave 1).** Run `gh label list --repo <R> --limit 200 --json name` and `gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`. Write `<D>/scout.md` from the create section of the `scout-report.md` template: the repo's labels and the possible duplicates. Duplicates never stop the run.
+2. **Create lookup (create Wave 1).** Run `gh label list --repo <R> --limit 200 --json name`, `gh api repos/<R>/issue-types` (the issue types of the repo), `gh api orgs/<owner of R>/issue-fields` (GET only; `<owner>` is the part of `<R>` before the slash; look up the field named `Complexity` and record its id, data type and option names) and `gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`. Write `<D>/scout.md` from the create section of the `scout-report.md` template: the repo's labels, `### Repo issue types`, `### Complexity field` and the possible duplicates. A read that fails is recorded as `lookup failed: <reason>` and you continue. Duplicates never stop the run.
 3. **Quick-depth body (create Wave 4, depth `quick`).** Run `/sc:analyze --depth quick` on the area the description touches, then fill the template the orchestrator chose into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing. Write `<D>/draft-notes.md` from the `draft-notes.md` template, listing any new material you added beyond the description and any contradiction between the description and the code.
 
 ## Rules
 
-- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you; a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.
+- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you; a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder; the one exception is the create lookup's GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash), and no other `orgs/` path is allowed. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.
 - **Git: `git fetch origin` only.** Your only git write is `git fetch origin`. You never add, fetch from or push to any other remote, and you never commit, check out, reset or stage.
 - **Writing only under `.dev/issues/`.** You write files only inside the `<D>` directory the orchestrator named under `.dev/issues/`. You never edit source code or any other file.
 - **Write your files.** Every file your job names is a tool input, not a report (see "Your files are tool inputs, not reports" above): write it with the Write tool and never return its content as text.

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

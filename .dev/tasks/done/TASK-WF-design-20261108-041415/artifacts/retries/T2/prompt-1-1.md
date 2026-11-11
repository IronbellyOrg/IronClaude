aebe40dc53d0c003da0bfa04fddc3ef19f77f8f9
Review one task for spec compliance.

Task brief: ## Task 2: Update refs/create.md for the new lookup, flags and post steps

Depends on: Task 1

Edit `src/superclaude/skills/sc-issue-protocol/refs/create.md`. Source sections: decision Q4, specification 2.1, 2.3, 2.5. Four places change. First, the gh call rule paragraph near line 9: every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash; no other `orgs/` path; T1 and T2 keep the old rule); also add that the orchestrator's only GitHub field write is the POST of Task 1. Second, Wave 1 (lines 18 to 22): the T3 worker also runs `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields` and writes the sections `### Repo issue types` and `### Complexity field` into `scout.md`; a failed lookup is recorded as `lookup failed: <reason>` and never stops the run. Third, Wave 2 (lines 34 to 36): `flags.md` gets a derived `Issue type` row by the Q7 rule, and the Complexity row holds the option name. Fourth, Wave 5 (lines 61 to 69): replace the label step with the sequence of specification 2.1 (mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment; final output with every `not applied` and `not set` line). `E-CREATE-FAILED` and `E-POST-FAILED` keep their current meaning.

Acceptance criteria:
- `create.md` names `issue-types` and `issue-fields` in Wave 1 and the two new `scout.md` section names.
- `create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed.
- `create.md` Wave 5 no longer requests a `type:` or `complexity:` label, and lists the type read-back, the field POST with `-X POST`, and the final-output lines in the order of specification 2.1.
- `create.md` says a failed type or field never stops the run after the issue exists, and that a failure of `gh issue create` is still STOP `E-CREATE-FAILED`.
- `create.md` contains no `-X PUT`, no brace placeholder and no `src/superclaude/`.

AC ids:
T2.AC1: `create.md` names `issue-types` and `issue-fields` in Wave 1 and the two new `scout.md` section names.
T2.AC2: `create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed.
T2.AC3: `create.md` Wave 5 no longer requests a `type:` or `complexity:` label, and lists the type read-back, the field POST with `-X POST`, and the final-output lines in the order of specification 2.1.
T2.AC4: `create.md` says a failed type or field never stops the run after the issue exists, and that a failure of `gh issue create` is still STOP `E-CREATE-FAILED`.
T2.AC5: `create.md` contains no `-X PUT`, no brace placeholder and no `src/superclaude/`.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: aebe40dc53d0c003da0bfa04fddc3ef19f77f8f9
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/create.md b/src/superclaude/skills/sc-issue-protocol/refs/create.md
index 18d8621d..7e3ab347 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/create.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/create.md
@@ -6,7 +6,7 @@ Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model`
 
 Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md` (Claude Code reads the project `.claude/agents/` copy first when one exists). Load `refs/tiers.md` before the first spawn. A worker that needs a codebase pass runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). Every file under `<D>` starts as a copy of its template under `templates/`.
 
-Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub. Create mode makes no ClickUp call and no self-assignment (B6).
+Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder, with one exception: the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields` (`<owner>` is the part of `<R>` before the slash). No other `orgs/` path is allowed, and the orchestrator and the T1 and T2 workers keep the old rule. Only the orchestrator writes to GitHub: besides `gh issue create --repo <R>` and `gh issue comment <N> --repo <R>`, its only GitHub field write is the POST of `refs/labels.md` (`gh api -X POST repos/<R>/issues/<N>/issue-field-values`). Create mode makes no ClickUp call and no self-assignment (B6).
 
 ## Wave 0: prerequisites (orchestrator)
 
@@ -17,7 +17,7 @@ Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; ev
 
 ## Wave 1: lookup (issue-worker-t3, B13)
 
-Spawn `issue-worker-t3` with the job "create lookup", `<R>`, the description's keywords and `<D>`. The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`) and writes `<D>/scout.md` from `templates/scout-report.md` (create section). Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).
+Spawn `issue-worker-t3` with the job "create lookup", `<R>`, the description's keywords and `<D>`. The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), reads the issue types of the repo (`gh api repos/<R>/issue-types`) and the Complexity field of the organization (`gh api orgs/<owner of R>/issue-fields`, the one allowed `orgs/` path; it records the id, the data type and the option names of the field named `Complexity`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`) and writes `<D>/scout.md` from `templates/scout-report.md` (create section: `### Repo labels`, `### Repo issue types`, `### Complexity field`, `### Possible duplicates`). A lookup that fails is recorded as `lookup failed: <reason>` and never stops the run. Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).
 
 Worker returns no file or an empty one: retry once, then STOP `E-WORKER-NO-OUTPUT` naming the path.
 
@@ -31,9 +31,9 @@ Worker returns no file or an empty one: retry once, then STOP `E-WORKER-NO-OUTPU
 | standard | `issue-worker-t2` runs a quick validation of the user's flags; differences become a pushback comment posted after the issue (Wave 5) | `issue-worker-t1` chooses |
 | deep | Two variants debated: the orchestrator writes `<D>/flags-user.md` (the user's flags) and `issue-worker-t1` writes `<D>/flags-t1.md` (an independent choice), then `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`; differences become the pushback comment (default D13) | `issue-worker-t1` runs `/sc:analyze` on the code the description touches, then chooses |
 
-Complexity follows depth, as the issue body pairs them (default D17): `quick` = simple, `standard` = medium, `deep` = complex.
+Complexity follows depth, as the issue body pairs them (default D17): `quick` = Simple, `standard` = Medium, `deep` = Complex; the value is the option name of the Complexity field.
 
-Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, complexity, reasons); `flags-user.md` and `flags-t1.md` use the same template. The issue is filed with the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently relabelled), else with the worker's choice.
+Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, issue type, complexity, reasons); `flags-user.md` and `flags-t1.md` use the same template. The `Issue type` row is derived by the orchestrator from the mode and the area by the rule of `refs/labels.md` (a bug is Bug, a feature in the area `tests` is Test, any other feature is Feature), after any worker returns. The issue is filed with the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently reclassified), else with the worker's choice.
 
 ## Wave 3: pick the template
 
@@ -62,8 +62,13 @@ If `draft-notes.md` lists new material or a contradiction, ask the user one ques
 
 Load `refs/labels.md`.
 
-1. Labels = the mode label (`enhancement` for feature, `bug` for bug) + `type: <type>` + `complexity: <simple|medium|complex>`, intersected with the repo labels in `scout.md`. Missing ones are listed in the final output, never created (B7).
-2. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label "<label>" ...` (one `--label` per applied label), with the prefix `[FEATURE] ` or `[BUG] ` (default D21). Failure -> STOP `E-CREATE-FAILED`; the draft directory is kept.
-3. Read `<N>` from the issue URL that step 2 prints, then rename `<D>` to `.dev/issues/<N>/`.
-4. Standard or deep with all flags given and a disagreement in Wave 2: write `.dev/issues/<N>/create-review.md` from `templates/create-review-comment.md` (it ends with `<!-- sc:issue:create-review -->`) and post it with `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md`. Failure -> STOP `E-POST-FAILED`.
-5. Print the issue URL, the directory and any `not applied: label missing in repo` lines. No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).
+1. Labels = the mode label only (`enhancement` for feature, `bug` for bug), intersected with the repo labels in `scout.md`. A missing one is listed in the final output, never created (B7). No label for the area or for the complexity is requested.
+2. Issue type: the wanted type follows the rule of `refs/labels.md`. When it is listed under `### Repo issue types` in `scout.md`, the create command of step 3 gets `--type "<name>"`; otherwise omit the flag and remember `not set: issue type <name>: type missing in repo` (or `lookup failed`).
+3. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label "<label>"` (plus `--type "<name>"` when step 2 allows it), with the prefix `[FEATURE] ` or `[BUG] ` (default D21). Failure -> STOP `E-CREATE-FAILED`; the draft directory is kept.
+4. Read `<N>` from the issue URL that step 3 prints, then rename `<D>` to `.dev/issues/<N>/`.
+5. Type read-back: `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. When `--type` was passed and the result is empty or different, remember `not set: issue type <name>: not applied after create`.
+6. Complexity field: when `### Complexity field` in `scout.md` lists the field and an option equal to the wanted value (`quick` = Simple, `standard` = Medium, `deep` = Complex), write `.dev/issues/<N>/complexity-field.json` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` (body and error handling in `refs/labels.md`). A failed POST remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After a success, read the values back with `gh api repos/<R>/issues/<N>/issue-field-values` and remember `not set: field Complexity <value>: not applied after create` when the value is absent. A missing field remembers `not set: field Complexity <value>: field not found in org` (or `lookup failed`).
+7. Standard or deep with all flags given and a disagreement in Wave 2: write `.dev/issues/<N>/create-review.md` from `templates/create-review-comment.md` (it ends with `<!-- sc:issue:create-review -->`) and post it with `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md`. Failure -> STOP `E-POST-FAILED`.
+8. Print the issue URL, the directory, every `not applied: label missing in repo` line and every `not set` line (formats in `refs/labels.md`). No ClickUp call (B6). No self-assignment. Do not stage or commit `.dev/issues/` (default D24).
+
+A failed type or field never stops the run once the issue exists. Only `gh issue create --repo <R>` (`E-CREATE-FAILED`) and the pushback comment (`E-POST-FAILED`) keep their STOP codes.

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

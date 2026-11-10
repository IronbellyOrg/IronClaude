c1a436aed894a854f1081211796117d03bda700a
Review one task for spec compliance.

Task brief: ## Task 1: Rewrite refs/labels.md as the rules for labels, issue type and fields

Edit `src/superclaude/skills/sc-issue-protocol/refs/labels.md` and keep the file name (tests pin the five-ref inventory). Retitle it "Labels, issue type and fields" and keep the spawn-rule paragraph at the top. Source sections: decisions Q1, Q2, Q6, Q7, Q8; specification 2.1, 2.3, 2.4.

The file must contain: the table of the only two labels the skill applies (`bug` for mode bug, `enhancement` for mode feature); the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen); the Complexity mapping (quick = Simple, standard = Medium, deep = Complex, matched to the field's option names without case sensitivity); the run-time steps in order (labels intersected with the repo labels in `scout.md`; `--type` only when the type is listed under `### Repo issue types`; read-back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`; the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and body `{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}`; read-back with `gh api repos/<R>/issues/<N>/issue-field-values`); and the three exact output line formats of specification 2.4. Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines; keep only the `bug` and `enhancement` lines in the maintainer block.

Acceptance criteria:
- `labels.md` contains no `type:` label and no `complexity:` label and no `gh label create` line for either.
- `labels.md` states Feature, Bug and Test with the Q7 rule, and Simple, Medium and Complex with the Q8 mapping.
- `labels.md` contains the three exact line formats `not applied: label missing in repo: <name>`, `not set: issue type <name>: <reason>` and `not set: field Complexity <value>: <reason>` with every reason listed in specification 2.4.
- `labels.md` uses `-X POST` for the field write, mentions `issue-field-values`, and contains no `-X PUT`.
- Every `gh issue` line in the file carries `--repo <R>`, and `uv run pytest tests/skills/test_issue_protocol.py -k "repo or placeholder" -v` still passes for this file.

AC ids:
T1.AC1: `labels.md` contains no `type:` label and no `complexity:` label and no `gh label create` line for either.
T1.AC2: `labels.md` states Feature, Bug and Test with the Q7 rule, and Simple, Medium and Complex with the Q8 mapping.
T1.AC3: `labels.md` contains the three exact line formats `not applied: label missing in repo: <name>`, `not set: issue type <name>: <reason>` and `not set: field Complexity <value>: <reason>` with every reason listed in specification 2.4.
T1.AC4: `labels.md` uses `-X POST` for the field write, mentions `issue-field-values`, and contains no `-X PUT`.
T1.AC5: Every `gh issue` line in the file carries `--repo <R>`, and `uv run pytest tests/skills/test_issue_protocol.py -k "repo or placeholder" -v` still passes for this file.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: c1a436aed894a854f1081211796117d03bda700a
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/labels.md b/src/superclaude/skills/sc-issue-protocol/refs/labels.md
index 40a52d03..8b22e1b1 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/labels.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/labels.md
@@ -1,45 +1,63 @@
-# Label set
+# Labels, issue type and fields
 
 Loaded in create Wave 5.
 
 Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout).)
 
-These are the only labels `/sc:issue` ever applies (B7). It never creates a label. `--claim` changes no labels.
+`--create` classifies the new issue in three ways: a mode label, a GitHub issue type and the Complexity issue field of the organization. These are the only classifications `/sc:issue` ever sets (B7). It never creates a label, an issue type or an issue field. `--claim` changes no label, type or field.
 
-| Group | Labels | Applied by |
+## Mode label
+
+| Mode | Label |
+|---|---|
+| feature | `enhancement` |
+| bug | `bug` |
+
+## Issue type
+
+The wanted issue type follows the mode and the area (`--type`):
+
+| Mode | Area (`--type`) | Issue type |
 |---|---|---|
-| Mode | `bug`, `enhancement` | `--create` (`feature` mode gets `enhancement`, `bug` mode gets `bug`) |
-| Type | `type: cicd`, `type: command`, `type: skill`, `type: agent`, `type: hook`, `type: cli`, `type: core`, `type: docs`, `type: tests`, `type: install`, `type: other` | `--create` |
-| Complexity | `complexity: simple`, `complexity: medium`, `complexity: complex` | `--create` |
+| bug | any | Bug |
+| feature | tests | Test |
+| feature | any other area | Feature |
+
+Task is never chosen. A bug in tests stays Bug, because the mode already says what the issue is. The area is recorded in `flags.md` and decides nothing else.
+
+## Complexity field
+
+Complexity follows depth. The value is the option name of the Complexity field of the organization, matched without regard to case:
+
+| Depth | Value |
+|---|---|
+| quick | Simple |
+| standard | Medium |
+| deep | Complex |
 
 ## At run time
 
-1. The wanted labels are the mode label, `type: <type>` and `complexity: <simple|medium|complex>`.
-2. Intersect them with the repo labels that `scout.md` lists (create Wave 1 read them with `gh label list --repo <R> --limit 200 --json name`).
-3. Pass each label that exists as one `--label "<name>"` to `gh issue create --repo <R>`.
-4. List every label that does not exist in the final output as `not applied: label missing in repo: <name>`. Never create it.
+1. Labels: the wanted label is the mode label. Intersect it with the repo labels that `scout.md` lists (create Wave 1 read them with `gh label list --repo <R> --limit 200 --json name`). Pass it as one `--label "<name>"` to `gh issue create --repo <R>`. List it as `not applied: label missing in repo: <name>` when the repo has no such label. Never create it.
+2. Issue type. When the wanted type is listed under `### Repo issue types` in `scout.md`, pass `--type "<name>"` to `gh issue create --repo <R>`. Otherwise omit the flag and remember `not set: issue type <name>: type missing in repo`, or `lookup failed` when the lookup recorded in `scout.md` failed.
+3. After `gh issue create --repo <R>` succeeds and the draft directory is renamed to `.dev/issues/<N>/`, read the type back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`. When `--type` was passed and the result is empty or differs, remember `not set: issue type <name>: not applied after create` (GitHub drops the type silently when the caller lacks push access).
+4. Complexity field: when `### Complexity field` in `scout.md` lists the field and an option equal to the wanted value, write `.dev/issues/<N>/complexity-field.json` with the body `{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}` and run `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`. A POST adds a value; a PUT would replace every existing value, so it is not used. A non-zero exit remembers `not set: field Complexity <value>: write failed (<first line of the gh error>)`. After a success, read the values back with `gh api repos/<R>/issues/<N>/issue-field-values`; when the value is absent, remember `not set: field Complexity <value>: not applied after create`. When `scout.md` has no such field, remember `not set: field Complexity <value>: field not found in org`, or `lookup failed` when the lookup failed; when the field has no option equal to the value, remember `option not found`.
+5. A failed type or field never stops the run once the issue exists. Print the issue URL, the directory, every `not applied` line and every `not set` line. Never create a label, a type or a field.
+
+## Output lines
+
+```text
+not applied: label missing in repo: <name>
+not set: issue type <name>: <type missing in repo | lookup failed | not applied after create>
+not set: field Complexity <value>: <field not found in org | option not found | lookup failed | write failed (<error>) | not applied after create>
+```
 
 ## One-time creation lines for a maintainer (default D16)
 
-A maintainer may run these by hand, once, to add the labels to a repo. The skill never runs them. Replace `<owner/repo>` with the target repo.
+A maintainer may run these by hand, once, to add the two mode labels to a repo. The skill never runs them. Replace `<owner/repo>` with the target repo.
 
 ```bash
 gh label create "bug" --repo <owner/repo>
 gh label create "enhancement" --repo <owner/repo>
-gh label create "type: cicd" --repo <owner/repo>
-gh label create "type: command" --repo <owner/repo>
-gh label create "type: skill" --repo <owner/repo>
-gh label create "type: agent" --repo <owner/repo>
-gh label create "type: hook" --repo <owner/repo>
-gh label create "type: cli" --repo <owner/repo>
-gh label create "type: core" --repo <owner/repo>
-gh label create "type: docs" --repo <owner/repo>
-gh label create "type: tests" --repo <owner/repo>
-gh label create "type: install" --repo <owner/repo>
-gh label create "type: other" --repo <owner/repo>
-gh label create "complexity: simple" --repo <owner/repo>
-gh label create "complexity: medium" --repo <owner/repo>
-gh label create "complexity: complex" --repo <owner/repo>
 ```
 
-`bug` and `enhancement` are GitHub's default labels and usually exist already.
+`bug` and `enhancement` are GitHub's default labels and usually exist already. Issue types and issue fields are created by an organization owner in the organization settings, never by this skill.

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

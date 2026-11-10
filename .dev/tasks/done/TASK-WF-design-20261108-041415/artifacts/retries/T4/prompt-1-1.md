9376ad0dd71cfa90d3f1884e9c299c671ae994d9
Review one task for spec compliance.

Task brief: ## Task 4: Update the scout, flags and create-review templates

Depends on: Task 1

Edit three files under `src/superclaude/skills/sc-issue-protocol/templates/`. Source sections: specification 2.1, section 3.1. In `scout-report.md` keep the Claim section as is and, in the Create section (lines 40 to 50), keep `### Repo labels` and `### Possible duplicates` and add `### Repo issue types` (one name per line, or `lookup failed: <reason>`) and `### Complexity field` (field id, data type, option names, or `not found` / `lookup failed: <reason>`). In `flags-decision.md` add an `Issue type` row (`<Feature | Bug | Test>`, reason: derived from mode and area by the rule in `refs/labels.md`) and change the Complexity row values to `<Simple | Medium | Complex>` while keeping the depth rule text. In `create-review-comment.md` change "The issue was not relabelled." (line 3) to "The issue was not reclassified." and keep the final line `<!-- sc:issue:create-review -->`.

Acceptance criteria:
- `scout-report.md` Create section has the four headings `### Repo labels`, `### Possible duplicates`, `### Repo issue types`, `### Complexity field`, and the Claim section is byte-identical to before.
- `flags-decision.md` has an `Issue type` row and the Complexity row lists Simple, Medium and Complex.
- `create-review-comment.md` says "not reclassified" and its last non-empty line is still `<!-- sc:issue:create-review -->`; `uv run pytest tests/skills/test_issue_protocol.py -k "marker or template" -v` passes.

AC ids:
T4.AC1: `scout-report.md` Create section has the four headings `### Repo labels`, `### Possible duplicates`, `### Repo issue types`, `### Complexity field`, and the Claim section is byte-identical to before.
T4.AC2: `flags-decision.md` has an `Issue type` row and the Complexity row lists Simple, Medium and Complex.
T4.AC3: `create-review-comment.md` says "not reclassified" and its last non-empty line is still `<!-- sc:issue:create-review -->`; `uv run pytest tests/skills/test_issue_protocol.py -k "marker or template" -v` passes.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 9376ad0dd71cfa90d3f1884e9c299c671ae994d9
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md b/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md
index 05d54aff..e40881a9 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md
@@ -1,6 +1,6 @@
 ## Flag review for this issue
 
-This issue was filed with the flags the user gave. A check at `<standard | deep>` depth chose differently; the reasons are below. The issue was not relabelled.
+This issue was filed with the flags the user gave. A check at `<standard | deep>` depth chose differently; the reasons are below. The issue was not reclassified.
 
 | Flag | User's flag | Worker's choice | Reason for the difference |
 |---|---|---|---|
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md b/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md
index 400a5d32..0173f5be 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md
@@ -7,4 +7,5 @@
 |---|---|---|
 | Mode | <feature | bug> | <one line> |
 | Type | <cicd | command | skill | agent | hook | cli | core | docs | tests | install | other> | <one line> |
-| Complexity | <simple | medium | complex> | follows depth (quick = simple, standard = medium, deep = complex) |
+| Issue type | <Feature | Bug | Test> | derived from the mode and the area by the rule in `refs/labels.md` |
+| Complexity | <Simple | Medium | Complex> | follows depth (quick = simple, standard = medium, deep = complex) |
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md b/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md
index 472460ef..a21eb872 100644
--- a/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md
@@ -43,6 +43,17 @@
 
 <label names, one per line>
 
+### Repo issue types
+
+<issue type names, one per line, or "lookup failed: <reason>">
+
+### Complexity field
+
+- Field id: <id, or "not found">
+- Data type: <single_select | text | number | date>
+- Options: <option names separated by commas, or "none">
+- Lookup: <ok | lookup failed: <reason>>
+
 ### Possible duplicates
 
 | Issue | Title | State | URL |

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

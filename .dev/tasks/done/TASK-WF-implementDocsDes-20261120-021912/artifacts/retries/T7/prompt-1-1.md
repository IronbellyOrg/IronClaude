cff4e114008a34d1913d5640f24bcd1cf171d24c
Review one task for spec compliance.

Task brief: ## Task 7: Update the workflow parse and contract refs

Depends on: Task 5

Edit `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`: the "never reuses" sentence of Package identity stays but notes that Wave 4R places a new package and never edits an old one; step 4 (exclusive creation) also tests `.dev/tasks/archive/<id>` as an added clause, keeping the existing literal text "`.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>`" and the sentence "Regeneration never reuses" that `tests/commands/test_workflow_command.py` pins (run that test file in this task); the Bash rule allows exactly the `remediate.py` subcommands, the private `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX` directory and the copy and move they perform, in addition to the package `mkdir` and the single `rm`; add `--remediate none|surgical|regenerate` and `--revise <package-dir> --review <REPORT.md>` to the enums and STOP table (`E-BAD-FLAG` for another value, a `--revise` without `--review` and the reverse). Edit `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`: keep `contract_version: "1.1"`, add the additive fields `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict` and `open_blockers` with their values and when each is written, and say `reflect_status` records the re-review verdict and scope ("changed lines plus prior blockers") for a replaced package, and rewrite the handoff relocation rule so that every contract rewrite (including to `partial`) merges into the existing file and keeps the lines `place` and `mark` wrote. Update the mirror copies under `plugins/superclaude/skills/sc-workflow-protocol/refs/`.

Acceptance criteria:
- `return-contract.md` still contains `contract_version: "1.1"` and lists all seven new fields.
- `input-parse.md` lists `archive/` in the collision check and both new flags in its enums.
- `diff -rq` against the plugin mirror shows no difference.
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: cff4e114008a34d1913d5640f24bcd1cf171d24c
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
index f062ed731..6aed83ef3 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
@@ -17,12 +17,12 @@ Validate every input and flag **before any write**. These STOPs create no packag
 
 ## Package identity
 
-Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package.
+Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package. Wave 4R (`refs/remediation.md`) places a new package for a repaired plan and never edits an old one.
 
 1. **Subject** — lower camelCase, **max 16** characters, no hyphens. Take the basename without extension (file source) or the inline prompt. Split into words with the regex `[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+` (ASCII only; every other character is a separator; camelCase and acronym boundaries split, so `authLogin` → `auth`,`Login` and `XMLParser` → `XML`,`Parser`). Lowercase each word. Before concatenation or truncation, if there are no words or the first word starts with a digit, prepend the word `plan`. Keep the first word as is, capitalize the first letter of each later word, concatenate, then truncate to **16** (empty → `plan`; `2fa login` → words `plan`,`2`,`fa`,`login` → `plan2FaLogin`; `1234567890123456` → `plan123456789012`). The result always matches `[a-z][A-Za-z0-9]{0,15}`.
 2. **Timestamp** — current **UTC** `YYYYMMDD-HHMMSS`.
 3. **ID** — `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`. The ID is the package directory name and the plan `slug`; it never changes after creation and is independent of the source's absolute path.
-4. **Exclusive creation** — if `.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>` exists (`test -e` **or** `test -L`, so dangling symlinks count), do not touch it: retry with suffix `-2`, `-3`, … up to `-9` appended to the full ID. Create the leaf with plain `mkdir` (never `mkdir -p`, never `rm -rf`) so an existing leaf is a hard failure; only the parents (`.dev/tasks/to-do`) may be created with `-p`. If `-9` is also taken → STOP `E-PACKAGE-COLLISION` (no package created).
+4. **Exclusive creation** — if `.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>` exists, or `.dev/tasks/archive/<id>` exists (`test -e` **or** `test -L`, so dangling symlinks count), do not touch it: retry with suffix `-2`, `-3`, … up to `-9` appended to the full ID. Create the leaf with plain `mkdir` (never `mkdir -p`, never `rm -rf`) so an existing leaf is a hard failure; only the parents (`.dev/tasks/to-do`) may be created with `-p`. If `-9` is also taken → STOP `E-PACKAGE-COLLISION` (no package created).
 
 | Source or prompt | Subject |
 |------------------|---------|
@@ -49,12 +49,12 @@ Every generation creates one **new** package under the current checkout: `.dev/t
 |------|------|----------|
 | `E-NO-SOURCE` | no path and no prompt, or two file tokens | none |
 | `E-EMPTY-SOURCE` | whitespace-only | none |
-| `E-BAD-FLAG` | unknown enum | none |
+| `E-BAD-FLAG` | unknown enum (including a `--remediate` value other than `none\|surgical\|regenerate`), a `--revise` without `--review`, or a `--review` without `--revise` | none |
 | `E-LEGACY` | `--output`, `--parallel`, `--validate`, `--depth shallow\|normal` | none |
 | `E-PACKAGE-COLLISION` | `-9` suffix also taken | none |
 | `E-NO-PHASES` | Wave 1 extracted nothing | created → `failed` contract |
 | `E-GATE` | Wave 3 schema/heading fail | created → `failed` contract |
 
-Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement`.
+Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement`. Remediate (`--remediate`) `none|surgical|regenerate`. `--revise <package-dir>` and `--review <REPORT.md>` are given together or not at all (each takes one value).
 
-Bash: only the package `mkdir` (exclusive leaf) and a single `rm` may change the filesystem; read-only helpers (`date -u`, `test -e`/`-L`, `tr`/`sed` for the subject, `grep` for gate checks) are fine. The single `rm` is of the draft `<id>.md` this run wrote when Wave 3 fails (never a directory, never anything else). Write `source.md` and `<id>.md` with the Write tool (a file source's text is read, then written verbatim).
+Bash: only the package `mkdir` (exclusive leaf), a single `rm`, the subcommands of `~/.claude/skills/sc-workflow-protocol/scripts/remediate.py` (`route`, `reserve`, `prepare`, `archive`, `place`, `restore`, `mark`, `release`), the private `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX` directory and the copy and move those subcommands perform may change the filesystem; read-only helpers (`date -u`, `test -e`/`-L`, `tr`/`sed` for the subject, `grep` for gate checks) are fine. The single `rm` is of the draft `<id>.md` this run wrote when Wave 3 fails (never a directory, never anything else). Write `source.md` and `<id>.md` with the Write tool (a file source's text is read, then written verbatim).
diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md
new file mode 100644
index 000000000..b9068398e
--- /dev/null
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md
@@ -0,0 +1,95 @@
+# Remediation (Wave 4R)
+
+How workflow repairs a reviewed plan whose review has blocking findings. Only blocking findings are ever repaired: no fix pass touches text for a Medium or Note finding, and a plan is never edited in place (the repair is made on a copy and placed as a new package).
+
+`REM` = `~/.claude/skills/sc-workflow-protocol/scripts/remediate.py`. Run it as `uv run --no-project ~/.claude/skills/sc-workflow-protocol/scripts/remediate.py <subcommand> ...` (the project `.claude/skills/sc-workflow-protocol/scripts/remediate.py` copy is the second place to look in a dev checkout). It uses the standard library only. On failure it prints `E-REMEDIATE-*` (or `E-ARCHIVE-*`) on stderr and exits 1: stop and report, do not improvise a move by hand.
+
+## 1. The routing rule
+
+Counts come from the `finding_counts` of the reflect contract (`blocking`, `label_high`, `medium`, `note`), one count per finding:
+
+- `B` = `blocking`: findings graded `Blocking (Decision):`, `Blocking (Missing):` or `Blocking (Safety):`.
+- `H` = `label_high`: findings whose reviewer label is HIGH, whatever their grade (on the shadow-panel path, findings-v2 severity CRITICAL).
+- `M` = `medium`: findings graded `Medium:` (on the panel path, severity MAJOR with `blocking` false).
+
+Rows are tried in order; the first match wins:
+
+| Order | Condition | Route |
+|---|---|---|
+| 1 | `B == 0` | `none`: the plan stands, whatever `H` and `M` are. Medium and Note findings are written to the contract as follow-up candidates and never start a fix pass. |
+| 2 | `B <= 3` and `H <= 5` and `M <= 9` | `surgical` |
+| 3 | otherwise (any of `B >= 4`, `H >= 6`, `M >= 10`) | `regenerate` |
+
+A `regenerate` result when a regenerate already ran in this run is `escalate` (section 5). A `Blocking (Safety)` finding never changes the route by itself: it is repaired like any blocker, and the re-review must confirm it resolved.
+
+Run the rule with the script, never by hand:
+
+```text
+REM route --blocking <B> --label-high <H> --medium <M> [--regenerated-already] [--forced none|surgical|regenerate]
+```
+
+It prints `{"route": ..., "forced": ...}`. `--forced` (from `--remediate none|surgical|regenerate`) overrides the rows and is recorded as forced, except that a forced `regenerate` with `--regenerated-already` still gives `escalate`.
+
+Where the counts for a cycle come from:
+
+- First cycle: the `finding_counts` of the Wave 4 reflect contract.
+- Later cycles: the re-reviewer card of the cycle before (its findings block, counted the same way).
+- `--revise <package-dir> --review <REPORT.md>`: the `finding_counts` of the given REPORT.md, or, when it has none, count its graded rows by the rules above.
+
+## 2. The surgical route
+
+Order of operations (the owner order: duplicate, edit, archive the original after the Wave 3 gate on the copy, place the new package, re-review). `<old-id>` is the package being repaired; `<root>` is the checkout.
+
+1. **Reserve and duplicate.**
+   - `REM reserve --root <root> --old-id <old-id>` picks the new package id under the id rule of `refs/input-parse.md` (collision with `to-do/`, `done/` and `archive/`, suffixes `-2` to `-9`), creates the empty leaf `.dev/tasks/to-do/<new-id>/` and prints the id. Every later step names this one id.
+   - `REM prepare --root <root> --old-id <old-id> --new-id <new-id>` copies the old plan and `source.md` into a private `/tmp/sc-workflow-revise.XXXXXXXX/<new-id>/` (the plan as `<new-id>.md` with `slug` set to `<new-id>`) and prints the copy directory and the sha256 of the original plan. Keep both.
+2. **Edit.** The reviser (section 3) repairs only the blocking findings, on the copy. Save its fix map as `fixmap.md` in the copy directory so `place` records it.
+3. **Wave 3 gate on the copy.** Run the gate of `refs/quality-gates.md` on the copy, named for the reserved id (slug equals the directory name `<new-id>`). On a gate failure run `REM release --root <root> --new-id <new-id>`, keep the old package where it is and escalate.
+4. **Archive the original.** `REM archive --root <root> --package .dev/tasks/to-do/<old-id> --superseded-by <new-id>` moves the package to `.dev/tasks/archive/<old-id>/`, adds a `SUPERSEDED` line to its contract (no second one when the contract already says superseded) and sets `superseded_by`. If `archive` fails, run `release` for `<new-id>`; the old package stays in `to-do/`.
+5. **Place the new package.** `REM place --root <root> --old-id <old-id> --new-id <new-id> --copy-dir <copy-dir> --finding-counts '<json of the counts>' --review <REPORT.md>` fills the reserved leaf (plan, `source.md` with a `## Revision N` section, `artifacts/` with `plan.diff`, `prior-findings.md`, `old-plan.md` and `revision-log.md`, and a `return-contract.yaml` with `supersedes`, `remediation_route: surgical` and `finding_counts`). It fails when the leaf is missing or not empty.
+6. **Re-review** the placed plan (section 4).
+7. **Mark once.** After the re-review, call `mark` exactly once with the final verdict (section 6).
+
+Failed placement undo: when `place` fails, run `REM release --root <root> --new-id <new-id>` and then `REM restore --root <root> --old-id <old-id>`. `restore` moves the archived package back to `to-do/` after removing exactly what `archive` added, so the restored package carries no SUPERSEDED mark and no empty or half-filled new package is left.
+
+Order in full: `reserve`, `prepare`, reviser edits, Wave 3 gate on the copy, `archive`, `place`, re-review, then `mark`. `release` runs on a failure before `archive` and after a failed `place` (before `restore`).
+
+Fix cycles: a re-review with an open, regressed or new blocker starts the next cycle, which repeats steps 1 to 6 with the placed package as `<old-id>` (counts from the re-reviewer card, section 1); step 7 (`mark`) runs once, after the last cycle. At most 2 fix cycles (3 reviews in all, counting the first review). Do not edit a placed package in place.
+
+## 3. The reviser brief
+
+The reviser and the re-reviewer are sub-agents started with the Agent tool.
+
+- Fresh context: the reviser sees only the copy, the review report and this brief, not the coordinator's history.
+- Edit tool only: exact, unique string replacement, one finding per call. No `sed`, no script, no whole-file rewrite.
+- Brief: the REVISE prompt and fix map of `~/.claude/rules/prompts/document_review_loop_prompts.md` (project copy second: `.claude/rules/prompts/document_review_loop_prompts.md`), reused as written and never edited. `{{IDS}}` is the blocking finding ids only; `{{CANDIDATE}}` is the copy. Prefer deleting or narrowing text, cite the finding id on every addition, report bytes added and deleted per finding id, leave Medium and Note findings alone.
+- Output: ends with a `fixmap-v1` block, one line per blocking id (`applied` or `rejected`, one sentence of reason). The reviser does not grade its own work.
+
+## 4. The re-review brief
+
+- Agent type `reflect-reviewer`, started with the Agent tool, read-only.
+- Inputs: the placed plan (candidate), the archived original `.dev/tasks/archive/<old-id>/<old-id>.md` as baseline, the prior review report, and the prior blocking findings.
+- It runs `diff -w baseline candidate`, then decides each prior blocker as `resolved`, `open` or `regressed` by comparing the defect with the changed text, and grades any new finding by the review severity rule. Follow the RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (project copy second).
+- Scope: changed lines plus prior blockers; the contract's `reflect_status` says so. Its card gives the counts for the next routing decision.
+
+## 5. The regenerate route
+
+Used when the rule gives `regenerate`.
+
+- Write a new source: the old `source.md` plus a section that lists the blocking findings to fix and, as text the new plan must not repeat, the HIGH-labelled and Medium findings that counted toward the route.
+- Run Waves 0 to 3 on it to create a new package. `place` is not used (it serves the surgical route only).
+- Archive the old package only after the new plan passes the Wave 3 gate: `REM archive --root <root> --package .dev/tasks/to-do/<old-id> --superseded-by <new-id>`. A failed generation archives nothing.
+- Link the new package with the one `mark` call of the run (section 6), made at the end of the route: `REM mark --package <new package dir> --supersedes <old-id> --route regenerate --finding-counts '<json>'` writes `supersedes`, `remediation_route` and `finding_counts`; on `escalate` the same single call also carries `--review-fail --open-blockers <id,id,...>`.
+- Wave 4 reviews the new package and its counts are routed once more, but a regenerate runs at most once per run: pass `--regenerated-already` to `route`. A second `regenerate` result is `escalate`: stop, report the open blocker ids to the user and mark the package FAIL (section 6). The old plan is never edited.
+
+## 6. Cap, verdict and `mark`
+
+`mark` is the one writer of `review_verdict: FAIL`, `open_blockers`, `superseded_by`, `fix_cycles` and, for the regenerate route, `supersedes`, `remediation_route` and `finding_counts`. It replaces the line of a key that exists and otherwise appends it once, so no key is written twice. Call it once, with the final verdict.
+
+- Clean re-review: `REM mark --package <placed package dir> --fix-cycles <n>` (on the regenerate route add `--supersedes <old-id> --route regenerate --finding-counts '<json>'` to this one call).
+- Blockers still open after the 2nd fix cycle (or on `escalate`): the last placed package stays in `.dev/tasks/to-do/`; run `REM mark --package <dir> --review-fail --open-blockers <id,id,...> --fix-cycles <n>` (on the regenerate route this same call also carries `--supersedes <old-id> --route regenerate --finding-counts '<json>'`). Its contract then carries `review_verdict: FAIL` and `open_blockers`, the run escalates to the user, and `/sc:implement` refuses the package. Under `--unattended` the run ends `partial` with the open blockers in `unresolved`.
+- `mark` takes `--package` but no `--root`.
+
+## 7. The standing archive rule
+
+A package replaced by another package, by either route or by hand, always moves to `.dev/tasks/archive/<id>/` in the same change that creates its replacement, with a `SUPERSEDED` line in its contract naming the replacement (`REM archive`). It is deleted only on an explicit owner order. `/sc:implement` refuses it there, because a managed plan must sit in `to-do/` or `done/`.
diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index 067c3520f..bc0b228e3 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -16,9 +16,19 @@ handoff_output_path: ./progress.md | null
 reflect_status: success | partial | failed | skipped   # Wave 4 `/sc:reflect --mode pre`; advisory only
 reflect_report_path: <abs path to reflect REPORT.md> | null
 unresolved: []
+# additive remediation fields (Wave 4R, `refs/remediation.md`); each is absent until the step below writes it
+remediation_route: surgical | regenerate      # written by `place` (surgical) or `mark` (regenerate), on the new package
+supersedes: <old-id>                          # written by `place` or `mark`, on the new package
+superseded_by: <new-id> | none                # written by `archive` (and `mark`), on the archived package
+finding_counts: {blocking: <n>, label_high: <n>, medium: <n>, note: <n>}   # the counts the route was chosen from; written with `remediation_route`
+fix_cycles: <n>                               # fix cycles run (0 to 2); written by `mark`
+review_verdict: FAIL                          # written by `mark` only when blockers stay open after the last cycle; absent otherwise
+open_blockers: [<finding id>, ...]            # written by `mark` together with `review_verdict: FAIL`
 ```
 
-`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`.
+The seven remediation fields are additive: `contract_version` stays `"1.1"` and `/sc:implement` keeps accepting only `"1.1"`. Only `remediate.py` writes them (by appending or replacing one line, never by re-writing the YAML), and Wave 5 keeps every line of them.
+
+`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`. For a package that replaced another, `reflect_status` records the re-review verdict and its scope ("changed lines plus prior blockers"), not a full review of the plan.
 
 ## Status
 
@@ -30,7 +40,7 @@ unresolved: []
 
 ## Handoff relocation rule
 
-Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`. If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.
+Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`, or any other) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`, and every rewrite merges into the existing file: it changes only the keys it owns (`status`, `reflect_*`, `handoff_*`, `unresolved`, and any stable 1.1 field still missing) and keeps every other line, including those `place` and `mark` wrote (`supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`). If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.
 
 A failed *generation* (no valid plan) and a failed *execution handoff* (valid plan) are different states: never mark a valid gated plan `failed`, never mark a failed generation `success`/`partial`.
 
diff --git a/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md b/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
index f062ed731..6aed83ef3 100644
--- a/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
+++ b/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
@@ -17,12 +17,12 @@ Validate every input and flag **before any write**. These STOPs create no packag
 
 ## Package identity
 
-Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package.
+Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package. Wave 4R (`refs/remediation.md`) places a new package for a repaired plan and never edits an old one.
 
 1. **Subject** — lower camelCase, **max 16** characters, no hyphens. Take the basename without extension (file source) or the inline prompt. Split into words with the regex `[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+` (ASCII only; every other character is a separator; camelCase and acronym boundaries split, so `authLogin` → `auth`,`Login` and `XMLParser` → `XML`,`Parser`). Lowercase each word. Before concatenation or truncation, if there are no words or the first word starts with a digit, prepend the word `plan`. Keep the first word as is, capitalize the first letter of each later word, concatenate, then truncate to **16** (empty → `plan`; `2fa login` → words `plan`,`2`,`fa`,`login` → `plan2FaLogin`; `1234567890123456` → `plan123456789012`). The result always matches `[a-z][A-Za-z0-9]{0,15}`.
 2. **Timestamp** — current **UTC** `YYYYMMDD-HHMMSS`.
 3. **ID** — `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`. The ID is the package directory name and the plan `slug`; it never changes after creation and is independent of the source's absolute path.
-4. **Exclusive creation** — if `.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>` exists (`test -e` **or** `test -L`, so dangling symlinks count), do not touch it: retry with suffix `-2`, `-3`, … up to `-9` appended to the full ID. Create the leaf with plain `mkdir` (never `mkdir -p`, never `rm -rf`) so an existing leaf is a hard failure; only the parents (`.dev/tasks/to-do`) may be created with `-p`. If `-9` is also taken → STOP `E-PACKAGE-COLLISION` (no package created).
+4. **Exclusive creation** — if `.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>` exists, or `.dev/tasks/archive/<id>` exists (`test -e` **or** `test -L`, so dangling symlinks count), do not touch it: retry with suffix `-2`, `-3`, … up to `-9` appended to the full ID. Create the leaf with plain `mkdir` (never `mkdir -p`, never `rm -rf`) so an existing leaf is a hard failure; only the parents (`.dev/tasks/to-do`) may be created with `-p`. If `-9` is also taken → STOP `E-PACKAGE-COLLISION` (no package created).
 
 | Source or prompt | Subject |
 |------------------|---------|
@@ -49,12 +49,12 @@ Every generation creates one **new** package under the current checkout: `.dev/t
 |------|------|----------|
 | `E-NO-SOURCE` | no path and no prompt, or two file tokens | none |
 | `E-EMPTY-SOURCE` | whitespace-only | none |
-| `E-BAD-FLAG` | unknown enum | none |
+| `E-BAD-FLAG` | unknown enum (including a `--remediate` value other than `none\|surgical\|regenerate`), a `--revise` without `--review`, or a `--review` without `--revise` | none |
 | `E-LEGACY` | `--output`, `--parallel`, `--validate`, `--depth shallow\|normal` | none |
 | `E-PACKAGE-COLLISION` | `-9` suffix also taken | none |
 | `E-NO-PHASES` | Wave 1 extracted nothing | created → `failed` contract |
 | `E-GATE` | Wave 3 schema/heading fail | created → `failed` contract |
 
-Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement`.
+Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement`. Remediate (`--remediate`) `none|surgical|regenerate`. `--revise <package-dir>` and `--review <REPORT.md>` are given together or not at all (each takes one value).
 
-Bash: only the package `mkdir` (exclusive leaf) and a single `rm` may change the filesystem; read-only helpers (`date -u`, `test -e`/`-L`, `tr`/`sed` for the subject, `grep` for gate checks) are fine. The single `rm` is of the draft `<id>.md` this run wrote when Wave 3 fails (never a directory, never anything else). Write `source.md` and `<id>.md` with the Write tool (a file source's text is read, then written verbatim).
+Bash: only the package `mkdir` (exclusive leaf), a single `rm`, the subcommands of `~/.claude/skills/sc-workflow-protocol/scripts/remediate.py` (`route`, `reserve`, `prepare`, `archive`, `place`, `restore`, `mark`, `release`), the private `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX` directory and the copy and move those subcommands perform may change the filesystem; read-only helpers (`date -u`, `test -e`/`-L`, `tr`/`sed` for the subject, `grep` for gate checks) are fine. The single `rm` is of the draft `<id>.md` this run wrote when Wave 3 fails (never a directory, never anything else). Write `source.md` and `<id>.md` with the Write tool (a file source's text is read, then written verbatim).
diff --git a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index 067c3520f..bc0b228e3 100644
--- a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -16,9 +16,19 @@ handoff_output_path: ./progress.md | null
 reflect_status: success | partial | failed | skipped   # Wave 4 `/sc:reflect --mode pre`; advisory only
 reflect_report_path: <abs path to reflect REPORT.md> | null
 unresolved: []
+# additive remediation fields (Wave 4R, `refs/remediation.md`); each is absent until the step below writes it
+remediation_route: surgical | regenerate      # written by `place` (surgical) or `mark` (regenerate), on the new package
+supersedes: <old-id>                          # written by `place` or `mark`, on the new package
+superseded_by: <new-id> | none                # written by `archive` (and `mark`), on the archived package
+finding_counts: {blocking: <n>, label_high: <n>, medium: <n>, note: <n>}   # the counts the route was chosen from; written with `remediation_route`
+fix_cycles: <n>                               # fix cycles run (0 to 2); written by `mark`
+review_verdict: FAIL                          # written by `mark` only when blockers stay open after the last cycle; absent otherwise
+open_blockers: [<finding id>, ...]            # written by `mark` together with `review_verdict: FAIL`
 ```
 
-`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`.
+The seven remediation fields are additive: `contract_version` stays `"1.1"` and `/sc:implement` keeps accepting only `"1.1"`. Only `remediate.py` writes them (by appending or replacing one line, never by re-writing the YAML), and Wave 5 keeps every line of them.
+
+`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`. For a package that replaced another, `reflect_status` records the re-review verdict and its scope ("changed lines plus prior blockers"), not a full review of the plan.
 
 ## Status
 
@@ -30,7 +40,7 @@ unresolved: []
 
 ## Handoff relocation rule
 
-Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`. If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.
+Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`, or any other) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`, and every rewrite merges into the existing file: it changes only the keys it owns (`status`, `reflect_*`, `handoff_*`, `unresolved`, and any stable 1.1 field still missing) and keeps every other line, including those `place` and `mark` wrote (`supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`). If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.
 
 A failed *generation* (no valid plan) and a failed *execution handoff* (valid plan) are different states: never mark a valid gated plan `failed`, never mark a failed generation `success`/`partial`.
 


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
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

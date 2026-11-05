bd10106d744f4328191f41d8bede2e132056935e
Review one task for spec compliance.

Task brief: ## Task 15: Write `refs/conflict-intent.md`

Depends on: Task 12

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md` with the ten sections of source section 8.3 (scope, evidence one file at a time, high-suspicion checklist, kind rules, intent rules, the resolution-record format matching `parse_resolution_record` / `resolution_record_ok` from Task 4, the `evidence-validator` grounding check with one revision pass, the commit message, after the merge push with configured reviewers, findings after a merge with `base_authored`).

Acceptance criteria:
- Every pinned phrase listed at the end of source section 8.3 is present, and the record field names appear in the order `kind`, `root_cause`, `ours_intent`, `theirs_intent`, `resolution`, `behavior_after`, `dropped`, `evidence`.
- A sample `resolution.md` written in the format the ref describes parses with `parse_resolution_record` and passes `resolution_record_ok` (checked in a scratch test or script run; output saved to `./artifacts/t15-record-check.txt`).
- No `src/superclaude/` text, no force flag, every `gh` line repo-scoped; `uv run pytest tests/pr_submit/test_static_grep.py -q` passes.
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: bd10106d744f4328191f41d8bede2e132056935e
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
new file mode 100644
index 00000000..7bc09ba8
--- /dev/null
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
@@ -0,0 +1,127 @@
+# Conflict Intent (C-initial, Tier 2 only) — resolving text conflicts by stated intent
+
+> **Tier 2 only. Off by default.** This ref applies only when the run was started with `--conflict-max-tier 2`, at `--monitor 3` (L3), inside the Tier 2 merge cycle at `C-initial`. With the default cap (`--conflict-max-tier 1`) or below L3 it is never loaded and no text conflict is ever resolved: Tier 2 is reported, not acted on.
+
+`refs/conflict-mechanical.md` owns the merge cycle (steps 0 to 13). This ref is its Tier 2 part: step 5 (resolve the `text:*` paths) and step 6 (the resolution record and its grounding check), plus the Tier 2 commit message and what follows the merge push. The core decides (`superclaude.pr_submit.conflicts`); this ref guides the judgment.
+
+## 1. Scope
+
+- Tier 2 only, L3 only, `--conflict-max-tier 2` only. Any other tier or ordinal never reaches this ref.
+- The attended main session does the judgment (J-39, R-173): no new agent resolves a file and no second model client is used. The only agent spawned is the read-only `evidence-validator` of section 7.
+- "Ours" is this PR (stage 2, the PR head). "Theirs" is the recorded base tip `base_sha` (stage 3). Stage 1 is the merge base (S-09).
+- Escalation is monotone: any stop condition below aborts the merge (the ownership-checked abort of `refs/conflict-mechanical.md` section 9) and halts `sync_tier3` with the Tier 3 template. Nothing is retried in the same run.
+
+## 2. Evidence, one file at a time (J-40)
+
+Take the `text:*` paths in plan order (`plan.text_paths`). Finish one path (evidence, checklist, edit, stage) before you open the next. For path number `<n>` (1-based), with `<merge_base>` taken from the step 2 probe JSON:
+
+```bash
+scripts/collect-conflict-evidence.sh --path <p> --out <output-dir>/sync/<cycle_id>/<n>/ --base-sha <base_sha> --merge-base <merge_base>
+```
+
+- Success prints one JSON line `{"dir": "<out>", "files": [...], "missing": [...], "truncated": <bool>}`. The files are `stage1`, `stage2`, `stage3` (each stage the index lists for the path; an absent stage is named in `missing`, for example `stage1` for an add-add), `worktree` (the file with its zdiff3 conflict markers), `log.txt` (the left-right log of the merge) and `diff-ours.txt`, `diff-theirs.txt` (each side's diff from the merge base). A file cut at the byte limit ends with `[sc:pr-submit: truncated at <N> bytes]`.
+- Read the three stage files as three sides. Compare each side with the base (stage 1) to tell which side changed a line and which merely carries it (S-12, S-13, S-14, S-17). Then read `log.txt` and both merge-base diffs (R-112).
+- To find callers of a symbol a side changed, a read-only search is allowed (R-181):
+
+```bash
+git grep -n -F -- <symbol>
+```
+
+- `EVIDENCE_FAIL` of any kind (`usage`, `foreign_merge`, `out_not_empty`, `unreadable`, `timeout`), or a file you cannot read, escalates the cycle to Tier 3: abort, `sync_tier3` (R-84). When `truncated` is true and the part you need was cut, you cannot state the intents from the evidence: section 5 applies (Tier 3).
+
+## 3. High-suspicion checklist (R-180, R-251, S-26)
+
+Before editing a file, answer each high-suspicion question from the evidence:
+
+- Does either side change a function signature, a type or schema, a dependency, a constant or environment variable, or a public API while the other side adds or changes callers of it?
+- Does one side remove an old API, field or column while consumers of it remain (on either side, or found by the search above)?
+
+Any yes: the file's kind is `semantic`. A `semantic` file is never resolved here; the cycle escalates to Tier 3 (abort, `sync_tier3`).
+
+## 4. Kind and rule per kind
+
+Give the file exactly one kind, name its structural root cause in one phrase (R-146), and apply that kind's rule:
+
+| Kind | Rule |
+|---|---|
+| `trivial` | Adjacent edits split artificially: combine both (R-150). One side changed one part of a line and the other another part: combine both changes into the line (S-18). |
+| `additive` | Keep both, in a stated order (R-151); the order goes into the resolution as `keep_both(<order>)`. |
+| `competing` | Pick or synthesize by intent, subject to section 5 (R-152). |
+| `structural` | A move or rename against an edit: apply the edit at the moved or renamed location (R-153). |
+| `modify-delete` | Decide which intent supersedes. The deletion wins only when the edit is shown obsolete; otherwise restore the file and keep the edit (R-154, S-39). |
+| `add-add` | Merge the two files' contents; never keep one and drop the other silently (S-40). |
+
+## 5. Intent rules
+
+- Edit a file only when each side's intent can be stated in one sentence. If either cannot, stop: Tier 3 (R-18, R-05).
+- Never invent a behaviour that neither side wrote (S-26).
+- Before staging, write one sentence describing the behaviour after the merge. If you cannot, you do not understand the resolution yet: stop, Tier 3 (R-156).
+- When a side's behaviour is dropped, say which behaviour and why in `dropped` (S-29); never drop one silently.
+- Remove every conflict marker. Then stage the finished file at once (J-56), naming only that path:
+
+```bash
+git add -- <path>
+git rm -- <path>
+```
+
+Use `git rm -- <path>` only when the resolution is a deletion. Never stage everything, never take one side for the whole tree, never stash, never skip hooks, never amend.
+
+## 6. The resolution record
+
+Write `<output-dir>/sync/<cycle_id>/resolution.md` after the last `text:*` path is staged. It holds one section per `text:*` path and nothing else: no title, no prose, no bullets, no other heading. Blank lines are allowed. Each section is these lines, in this order, each field on one line as `<field>: <value>`:
+
+1. `## <path>`: the path exactly as it appears in `plan.text_paths`. Every `text:*` path appears exactly once; no other path (a `regen:*` path has no entry).
+2. `kind:` one of `trivial`, `additive`, `competing`, `structural`, `modify-delete`, `add-add` (`semantic` never appears: it is Tier 3).
+3. `root_cause:` the structural root cause in one phrase.
+4. `ours_intent:` this PR's intent, in exactly one sentence.
+5. `theirs_intent:` the base side's intent, in exactly one sentence.
+6. `resolution:` one of `keep_both(<order>)`, `take_ours`, `take_theirs`, `synthesized`.
+7. `behavior_after:` the behaviour after the merge, in exactly one sentence.
+8. `dropped:` `none`, or the dropped behaviour and why.
+9. `evidence:` the stage files and commits consulted.
+
+"Exactly one sentence" means one line that ends in `.`, `!` or `?`, with no other `.`, `!` or `?` followed by a space (write "for example", not an abbreviation with a full stop). Every value is non-empty. Example section (each line without the leading `> `):
+
+> ## app/config.py
+> kind: additive
+> root_cause: both sides appended a setting to the end of the same settings block
+> ours_intent: This PR adds a retry limit setting for the HTTP client.
+> theirs_intent: The base adds a request timeout setting for the HTTP client.
+> resolution: keep_both(ours then theirs)
+> behavior_after: The settings block defines both the retry limit and the request timeout.
+> dropped: none
+> evidence: stage1, stage2, stage3, diff-ours.txt, diff-theirs.txt, log.txt, commits 1a2b3c4 and 5d6e7f8
+
+The core checks it: `resolution_record_ok(parse_resolution_record(text), plan.text_paths)` must return `[]`. A parse error or any listed problem means no commit: abort, `sync_tier3`. The record and the evidence directories stay in the output dir after an abort.
+
+## 7. Grounding check
+
+Spawn `evidence-validator` (read-only: Read, Grep, Glob) once for the whole record, not once per file. Pass `resolution.md` as the draft (`report_draft_path`), `<output-dir>/sync/<cycle_id>/` as `output_dir`, and `allow_command_reexec: false`. Ask it to check, for each section, that both intents and `behavior_after` are grounded in that path's stage files and merge-base diffs, and to list each unsupported section.
+
+- Every section supported: continue to VAL (`refs/conflict-mechanical.md` section 6).
+- One revision pass: re-read the evidence for each flagged section, correct the file and the record where needed (re-stage the path, re-run `resolution_record_ok`), then ask the same validator (no new spawn) to re-check only the revised sections.
+- Still unsupported after the one revision pass, or the validator cannot run: abort, Tier 3 (`sync_tier3`).
+
+The grounding check is mandatory for Tier 2 in this release (OQ-12).
+
+## 8. Commit message
+
+Step 9 writes the message file from `merge_commit_message(base_ref=..., head_branch=HEAD_BRANCH, tier=2, record=<the parsed record>)`: the subject `Merge <base_ref> into <head_branch> (sc:pr-submit sync, tier 2)`, then one line per path, `<path>: kind <kind>, resolution <resolution>, dropped <dropped>`. Append the session's attribution lines (OQ-13). The message carries intents and labels, never file content, so keep `dropped` to a short phrase.
+
+## 9. After the merge push
+
+- S6 and RESOLVING run with zero threads (there are no findings yet).
+- S5a re-triggers because the push kind is `merge`: `should_retrigger(0, "merge")` is true.
+- At `C-initial` no reviewer has been observed yet, so the re-trigger targets the configured reviewers: each reviewer `r` with a non-blank identity in the detection contract (`reviewer_identities(contract, r)` non-empty). Post only to `pending_retriggers(<events>, cycle_id, <configured reviewers>)`, through the S5a procedure of `refs/review-retrigger.md`.
+- Each POST's watermark starts that reviewer's S5 attribution, so a review of the pre-merge head is never attributed (INV-030).
+- The S5 wait is the run's first review wait; its attributed outcome ticks `round_counter` once.
+
+## 10. Findings after a merge (INV-031)
+
+Once, right after the merge push, read the paths the PR's own diff touches:
+
+```bash
+git diff --name-only origin/<base>...HEAD
+```
+
+For the rest of the run, a review finding on a path not in that list is `REPORT_ONLY` with reason `base_authored` at Wave 3: it came from the base side of the merge, it is reported, never fixed, and it consumes no round.
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-record-check.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-record-check.txt
new file mode 100644
index 00000000..83eca9e2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-record-check.txt
@@ -0,0 +1,36 @@
+$ PYTHONDONTWRITEBYTECODE=1 uv run python /tmp/t15-check/record_check.py src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md /tmp/t15-check/resolution.md
+sample written to /tmp/t15-check/resolution.md:
+## app/config.py
+kind: additive
+root_cause: both sides appended a setting to the end of the same settings block
+ours_intent: This PR adds a retry limit setting for the HTTP client.
+theirs_intent: The base adds a request timeout setting for the HTTP client.
+resolution: keep_both(ours then theirs)
+behavior_after: The settings block defines both the retry limit and the request timeout.
+dropped: none
+evidence: stage1, stage2, stage3, diff-ours.txt, diff-theirs.txt, log.txt, commits 1a2b3c4 and 5d6e7f8
+
+## src/app/routes.py
+kind: competing
+root_cause: both sides changed the default page size of the same list route
+ours_intent: This PR raises the default page size to 50 for the list route.
+theirs_intent: The base makes the page size configurable through an argument.
+resolution: synthesized
+behavior_after: The list route takes a page size argument whose default is 50.
+dropped: none
+evidence: stage1, stage2, stage3, diff-ours.txt, diff-theirs.txt, log.txt
+
+parsed paths: ['app/config.py', 'src/app/routes.py']
+field order per path: {'app/config.py': ['kind', 'root_cause', 'ours_intent', 'theirs_intent', 'resolution', 'behavior_after', 'dropped', 'evidence'], 'src/app/routes.py': ['kind', 'root_cause', 'ours_intent', 'theirs_intent', 'resolution', 'behavior_after', 'dropped', 'evidence']}
+resolution_record_ok -> []
+--- merge_commit_message(tier=2) ---
+Merge origin/master into feature/x (sc:pr-submit sync, tier 2)
+
+app/config.py: kind additive, resolution keep_both(ours then theirs), dropped none
+src/app/routes.py: kind competing, resolution synthesized, dropped none
+
+negative control [two sentences in ours_intent] -> ['app/config.py: ours_intent is not exactly one sentence']
+negative control [semantic kind] -> ['app/config.py: kind semantic means Tier 3']
+negative control [bullet line] -> ValueError: unknown field: '- kind'
+RESULT: PASS
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-pins.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-pins.txt
new file mode 100644
index 00000000..369b95dd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-pins.txt
@@ -0,0 +1,28 @@
+# grep -cF per pinned phrase of source 8.3 in src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+1	scripts/collect-conflict-evidence.sh
+2	evidence-validator
+1	One revision pass
+6	one sentence
+4	dropped
+1	high-suspicion
+1	configured reviewers
+1	base_authored
+1	git add -- <path>
+2	git rm -- <path>
+
+$ PYTHONDONTWRITEBYTECODE=1 uv run python /tmp/t15-check/pins_check.py src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+  1  scripts/collect-conflict-evidence.sh
+  2  evidence-validator
+  1  One revision pass
+  6  one sentence
+  8  dropped
+  1  high-suspicion
+  2  configured reviewers
+  1  base_authored
+  1  git add -- <path>
+  2  git rm -- <path>
+order [format list]: [('kind', 5858), ('root_cause', 5995), ('ours_intent', 6053), ('theirs_intent', 6114), ('resolution', 6183), ('behavior_after', 6272), ('dropped', 6349), ('evidence', 6405)] -> OK
+order [example]: [('kind', 6736), ('root_cause', 6753), ('ours_intent', 6835), ('theirs_intent', 6906), ('resolution', 6984), ('behavior_after', 7026), ('dropped', 7117), ('evidence', 7133)] -> OK
+order [first in file]: [('kind', 5858), ('root_cause', 5995), ('ours_intent', 6053), ('theirs_intent', 6114), ('resolution', 6183), ('behavior_after', 6272), ('dropped', 6349), ('evidence', 6405)] -> OK
+RESULT: PASS
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-grep.txt
new file mode 100644
index 00000000..89894277
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-grep.txt
@@ -0,0 +1,35 @@
+$ grep -nE -- '--force|git push|git stash|--amend|--no-verify|src/superclaude/|```' src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+18:```bash
+20:```
+26:```bash
+28:```
+62:```bash
+65:```
+123:```bash
+125:```
+grep exit=0
+
+$ grep -nE '(^|[[:space:]`(])gh[[:space:]]' src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+grep exit=1 (1 = no gh line in the ref)
+
+$ PYTHONDONTWRITEBYTECODE=1 uv run python /tmp/t15-check/forbidden_check.py src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+fenced lines:
+       19: scripts/collect-conflict-evidence.sh --path <p> --out <output-dir>/sync/<cycle_id>/<n>/ --base-sha <base_sha> --merge-base <merge_base>
+       27: git grep -n -F -- <symbol>
+       63: git add -- <path>
+       64: git rm -- <path>
+       124: git diff --name-only origin/<base>...HEAD
+[OK] fence language other than bash: 0 hit(s)
+[OK] fenced line whose first word is not git/gh/uv/make/scripts/: 0 hit(s)
+[OK] unclosed fence: 0 hit(s)
+[OK] force push (test_skill_forbids_force_push regex): 0 hit(s)
+[OK] any --force / --force-with-lease text: 0 hit(s)
+[OK] git push line not exactly `git push origin <target_sha>:<HEAD_BRANCH>`: 0 hit(s)
+[OK] gh line without --repo "$REPO" or repos/<owner/repo>/: 0 hit(s)
+[OK] src/superclaude/ text: 0 hit(s)
+[OK] stash / amend / hook-skipping flag: 0 hit(s)
+[OK] upstream repository named: 0 hit(s)
+[OK] Tier 2 / off-by-default / --conflict-max-tier 2 marker missing: 0 hit(s)
+lines in file: 127
+RESULT: PASS
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-tests.log
new file mode 100644
index 00000000..3acd022c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t15-tests.log
@@ -0,0 +1,12 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 19 items
+
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================== 19 passed in 0.57s ==============================

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

8c95723a1e5acac366978d7ef06adce484831e2a
Review one task for spec compliance.

Task brief: ## Task 9: Make /sc:implement refuse a plan with `review_verdict: FAIL`

Edit `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`: in the Detection list (check 2, the sibling contract) add that a contract carrying `review_verdict: FAIL` is refused before any write with STOP `E-MANAGED-REVIEW-FAIL` that prints the `open_blockers` ids from that contract; keep `contract_version: "1.1"`, keep the rule that a plan outside `to-do/` and `done/` (an `archive/` plan included) is refused, and add `E-MANAGED-REVIEW-FAIL` to every STOP list that enumerates the managed STOPs: `src/superclaude/skills/sc-implement-protocol/SKILL.md` and `src/superclaude/skills/sc-implement-protocol/refs/qa.md`. Mirror all three files to `plugins/superclaude/skills/sc-implement-protocol/`. Add tests to `tests/skills/test_workflow_remediation.py` that read the markdown and assert the refusal wording, the `E-MANAGED-REVIEW-FAIL` code, the unchanged "1.1" pin in `managed-workspace.md` and in `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`, and that location resolution still knows only `to-do/` and `done/`.

Acceptance criteria:
- The refusal is described before the ledger step and names `open_blockers`.
- The new static tests pass: `uv run pytest tests/skills/test_workflow_remediation.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py -q`.
- `diff -rq` between the two implement-protocol folders shows no difference.
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
Start sha: 8c95723a1e5acac366978d7ef06adce484831e2a
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
index 56ee64f0c..91a69a462 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -43,6 +43,7 @@ STOP: need a source (file or prompt). Will not invent scope beyond that source.
 | `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` (managed: any `--ledger` other than the sibling `progress.md`) | No | No |
 | `E-MANAGED-INVALID` | `workflow-plan/1.2` plan fails managed detection (copied, cross-checkout, slug/contract mismatch, failed contract) | No | No |
 | `E-MANAGED-CONFLICT` | managed package exists in both `to-do/` and `done/` | No | No |
+| `E-MANAGED-REVIEW-FAIL` | managed contract carries `review_verdict: FAIL`; prints its `open_blockers` ids | No | No |
 | `E-PLAN-CHANGED` | managed plan/source hash differs from the pin after the first `T<id>: start` | No | Unchanged |
 | `E-ARCHIVE-MARKER` | managed `.archiving` marker exists | No | Unchanged |
 | `E-ARCHIVE-BLOCKED` | managed FINAL/archive cannot complete (`issues`, `--skip-final-review`, helper refusal) | No | FINAL line only if a review ran |
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index d970bdf7d..5710506db 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -7,7 +7,7 @@ Loaded **only** when Wave 0 detects a managed plan. Everything here is additive:
 A source file `P` is **managed** iff `P` has front matter `schema: workflow-plan/1.2`. Then **all** must hold, else STOP `E-MANAGED-INVALID` (no ledger, no writes):
 
 1. `slug` matches `^TASK-WF-[a-z][A-Za-z0-9]{0,15}-[0-9]{8}-[0-9]{6}(-[2-9])?$` (subject: lower camelCase, max 16, no hyphens), equals the name of `P`'s parent directory, **and `P`'s basename is exactly `<slug>.md`** (a managed plan named `plan.md` or any other name → `E-MANAGED-INVALID`; never fall back to `plan.md`). Below, `<plan>` means `<slug>.md`.
-2. Sibling `return-contract.yaml` has `contract_version: "1.1"`, the same `slug`, and `status: success` or `partial` (a `failed` contract is never executable).
+2. Sibling `return-contract.yaml` has `contract_version: "1.1"`, the same `slug`, and `status: success` or `partial` (a `failed` contract is never executable). A contract that carries `review_verdict: FAIL` is refused before any write and before the ledger step with STOP `E-MANAGED-REVIEW-FAIL`, which prints the `open_blockers` ids from that contract (the plan still has blocking review findings; repair it with `/sc:workflow`, do not run it).
 3. `P` resolves (realpath, no symlinked component below the checkout) to `<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`, where `<checkout>` is the current git top-level. A copied plan or a plan from another checkout fails here.
 4. Sibling `source.md` exists as a regular file.
 
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
index 72cdff90e..8eb54d1e4 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -282,7 +282,7 @@ Each line names the path, when it fires and why it stays.
 3. `E-NO-RULING`: reachable only when someone tries to continue past a non-compliant verdict, which now exists only with a blocker. Kept as the user-acceptance safety gate.
 4. `operator-review`: user-initiated after a halt, never started by automation.
 5. `E-RESUME-NEEDED` (`reviewer-down` after a second paperwork-only or unparseable review, `ref-failed` including a notes file that cannot be written, incomplete revert, adviser agent missing): infrastructure, never about a finding; it asks the user to re-run, not to fix anything. Kept because continuing would record an unverified completion or risk data loss.
-6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
+6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-MANAGED-REVIEW-FAIL`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
 7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (see "FINAL derived test" below), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived.
 
 No other path may stop automation or prompt the user. Every halt message and Ruling request lists blocking findings only. A minors-only replay writes no `halt` and no `Ruling:` line.
diff --git a/src/superclaude/skills/sc-implement-protocol/SKILL.md b/src/superclaude/skills/sc-implement-protocol/SKILL.md
index 56ee64f0c..91a69a462 100644
--- a/src/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -43,6 +43,7 @@ STOP: need a source (file or prompt). Will not invent scope beyond that source.
 | `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` (managed: any `--ledger` other than the sibling `progress.md`) | No | No |
 | `E-MANAGED-INVALID` | `workflow-plan/1.2` plan fails managed detection (copied, cross-checkout, slug/contract mismatch, failed contract) | No | No |
 | `E-MANAGED-CONFLICT` | managed package exists in both `to-do/` and `done/` | No | No |
+| `E-MANAGED-REVIEW-FAIL` | managed contract carries `review_verdict: FAIL`; prints its `open_blockers` ids | No | No |
 | `E-PLAN-CHANGED` | managed plan/source hash differs from the pin after the first `T<id>: start` | No | Unchanged |
 | `E-ARCHIVE-MARKER` | managed `.archiving` marker exists | No | Unchanged |
 | `E-ARCHIVE-BLOCKED` | managed FINAL/archive cannot complete (`issues`, `--skip-final-review`, helper refusal) | No | FINAL line only if a review ran |
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index d970bdf7d..5710506db 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -7,7 +7,7 @@ Loaded **only** when Wave 0 detects a managed plan. Everything here is additive:
 A source file `P` is **managed** iff `P` has front matter `schema: workflow-plan/1.2`. Then **all** must hold, else STOP `E-MANAGED-INVALID` (no ledger, no writes):
 
 1. `slug` matches `^TASK-WF-[a-z][A-Za-z0-9]{0,15}-[0-9]{8}-[0-9]{6}(-[2-9])?$` (subject: lower camelCase, max 16, no hyphens), equals the name of `P`'s parent directory, **and `P`'s basename is exactly `<slug>.md`** (a managed plan named `plan.md` or any other name → `E-MANAGED-INVALID`; never fall back to `plan.md`). Below, `<plan>` means `<slug>.md`.
-2. Sibling `return-contract.yaml` has `contract_version: "1.1"`, the same `slug`, and `status: success` or `partial` (a `failed` contract is never executable).
+2. Sibling `return-contract.yaml` has `contract_version: "1.1"`, the same `slug`, and `status: success` or `partial` (a `failed` contract is never executable). A contract that carries `review_verdict: FAIL` is refused before any write and before the ledger step with STOP `E-MANAGED-REVIEW-FAIL`, which prints the `open_blockers` ids from that contract (the plan still has blocking review findings; repair it with `/sc:workflow`, do not run it).
 3. `P` resolves (realpath, no symlinked component below the checkout) to `<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`, where `<checkout>` is the current git top-level. A copied plan or a plan from another checkout fails here.
 4. Sibling `source.md` exists as a regular file.
 
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 72cdff90e..8eb54d1e4 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -282,7 +282,7 @@ Each line names the path, when it fires and why it stays.
 3. `E-NO-RULING`: reachable only when someone tries to continue past a non-compliant verdict, which now exists only with a blocker. Kept as the user-acceptance safety gate.
 4. `operator-review`: user-initiated after a halt, never started by automation.
 5. `E-RESUME-NEEDED` (`reviewer-down` after a second paperwork-only or unparseable review, `ref-failed` including a notes file that cannot be written, incomplete revert, adviser agent missing): infrastructure, never about a finding; it asks the user to re-run, not to fix anything. Kept because continuing would record an unverified completion or risk data loss.
-6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
+6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-MANAGED-REVIEW-FAIL`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
 7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (see "FINAL derived test" below), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived.
 
 No other path may stop automation or prompt the user. Every halt message and Ruling request lists blocking findings only. A minors-only replay writes no `halt` and no `Ruling:` line.
diff --git a/tests/skills/test_workflow_remediation.py b/tests/skills/test_workflow_remediation.py
index 6b6838872..fc2bbde56 100644
--- a/tests/skills/test_workflow_remediation.py
+++ b/tests/skills/test_workflow_remediation.py
@@ -481,3 +481,36 @@ def test_wave5_merges_into_existing_contract_and_keeps_review_verdict():
     assert "never edit, delete, or regenerate" not in skill
     head = skill.split("---", 2)[1]
     assert "Agent" in head and "Task" in head
+
+
+_IMPL_DIR = Path(__file__).resolve().parents[2] / "src/superclaude/skills/sc-implement-protocol"
+
+
+def test_implement_refuses_review_verdict_fail_before_ledger():
+    m = (_IMPL_DIR / "refs/managed-workspace.md").read_text(encoding="utf-8")
+    detection = m.split("## Detection", 1)[1].split("## Location resolution", 1)[0]
+    assert "`review_verdict: FAIL`" in detection
+    assert "STOP `E-MANAGED-REVIEW-FAIL`" in detection
+    assert "`open_blockers`" in detection
+    assert "before any write and before the ledger step" in detection
+    assert m.index("E-MANAGED-REVIEW-FAIL") < m.index("## Ledger, artifacts, pins")
+
+
+def test_review_fail_code_listed_in_every_managed_stop_list():
+    skill = (_IMPL_DIR / "SKILL.md").read_text(encoding="utf-8")
+    qa = (_IMPL_DIR / "refs/qa.md").read_text(encoding="utf-8")
+    assert "| `E-MANAGED-REVIEW-FAIL` |" in skill
+    assert "`E-MANAGED-CONFLICT`, `E-MANAGED-REVIEW-FAIL`" in qa
+    plugin = Path(__file__).resolve().parents[2] / "plugins/superclaude/skills/sc-implement-protocol"
+    for rel in ("SKILL.md", "refs/qa.md", "refs/managed-workspace.md"):
+        assert (plugin / rel).read_bytes() == (_IMPL_DIR / rel).read_bytes(), rel
+
+
+def test_contract_pin_and_locations_unchanged():
+    m = (_IMPL_DIR / "refs/managed-workspace.md").read_text(encoding="utf-8")
+    assert '`contract_version: "1.1"`' in m and "contract_version: \"1.2\"" not in m
+    arch = (_IMPL_DIR / "scripts/archive_workspace.py").read_text(encoding="utf-8")
+    assert 'contract.get("contract_version") != "1.1"' in arch
+    assert "<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`" in m
+    assert 'tasks / "archive"' not in arch and '"tasks" / "archive"' not in arch
+    assert "archive/" not in m.split("## Location resolution", 1)[1].split("## Ledger", 1)[0]


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

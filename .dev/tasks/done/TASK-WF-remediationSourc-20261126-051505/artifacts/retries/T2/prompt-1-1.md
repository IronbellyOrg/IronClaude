6d7cebe7aa723005b53833c0917d941d346da4ba
Review one task for spec compliance.

Task brief: ## Task 2: Change the four worked-table cells in the source retry.md and the four pinned test rows together

Depends on: Task 1

In `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, in the worked table that follows "Worked example with the fallback ladder:" (four rows: `haiku`, `sonnet`, `opus` (known), unknown), replace the cell text `1× GPT T1` in the third column of every row with ``1× `opus` (GPT T1 not launchable, family-fallback)``. Leave the other columns and the header rows unchanged, so each row still ends with the cell `2× `opus``.

In `tests/skills/test_task_workspace_lifecycle.py`, in the function `test_retry_ref_rules_text` (the `for row in (` block at lines 598 to 604), change the four row strings to the same new text so each is a verbatim substring of `retry.md`. The four rows must read:

```text
| `haiku` | 1× `sonnet` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| `sonnet` | 1× `opus` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| `opus` (known) | 1× `opus` (top rung) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
```

Acceptance criteria:
- The four worked-table rows in `retry.md` equal the four strings above, written with `×`; no row still contains `1× GPT T1`.
- The four assertion strings in `tests/skills/test_task_workspace_lifecycle.py` equal the same four rows and the file has no other change.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py -q` passes; in particular the 22-row halt-table check still counts exactly 22 pairs because each new row ends in `2× `opus`` and not in digits alone.
AC ids in source order (the bullets under Acceptance criteria): T2.AC1 T2.AC2 T2.AC3
Global constraints: ## Constraints

- Scope: change only the files named in the tasks below (`src/superclaude/skills/sc-implement-protocol/refs/retry.md`, `src/superclaude/skills/sc-implement-protocol/SKILL.md`, their two copies under `plugins/superclaude/skills/sc-implement-protocol/`, `tests/skills/test_task_workspace_lifecycle.py` and the new `tests/skills/test_implement_launch_alias.py`). Edit nothing under `.claude/` or `.dev/issues/`.
- The rule being written: on the fallback ladder the Agent call's `model` is the rung's own alias; on the primary ladder it is `opus` for every adviser (adviser A, adviser B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with `claude-` is still launched on `opus` and its line 1 carries `family-fallback: <reason>`; this never STOPs and never prompts the user.
- The new text in `retry.md` must not start any line with `GPT spawn path: ` (a test requires exactly one such line, at the pinned line 183), and must keep the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" (`tests/skills/test_implement_adviser_family.py`, lines 73 to 85).
- The new text must not contain the words `halt`, `Ruling` or `E-HALT-QA` outside the lines a test already allow-lists (`tests/skills/test_implement_severity_static.py`, lines 296 to 299 and 420 to 434), must not contain the string `claude-gw-tier` (`tests/skills/test_model_alias_policy.py`, lines 104 to 119), and must not put a full model id after `--model` or `--models` (same file, lines 164 to 173).
- The new text must not add a fenced block containing a line that begins with `T` and a digit and has no angle bracket (`tests/skills/test_implement_severity_static.py`, lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is only the digits 2 to 5 (`tests/skills/test_workflow_archive.py`, lines 1042 to 1076).
- `retry.md` must keep the four rung names `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`, and must not contain any `T`-digit-underscore-`Model` spelling (`tests/skills/test_model_alias_policy.py`, lines 219 to 228).
- Add no flag, no stop reason, no halt reason and no extra adviser spawn (the cap of six stays); do not change the `tier=` ledger token (its value class is letters, digits and underscore) or `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`.
- In table cells and prose copied from the existing worked table, use the multiplication sign `×` and not the letter `x` (the pinned test rows use `1×`).
- Out of scope, separate defects: the executor-tier tie when `T2Model01` and `T1Model02` hold the same id, and family inference from gateway ids such as `claude-gw-tier2`.
- Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope.
- Observed workspace values the wording must stay true to: `T2bModel01` is `gpt-6.1-terra`, `T2Model02` is `glm-5.3`, `T1Model02` is `gpt-6.1-sol`, `T1Model01` is `claude-opus-5-5`; the three aliases `opus`, `sonnet` and `haiku` resolve to tier ids through `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
Start sha: 6d7cebe7aa723005b53833c0917d941d346da4ba
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/retry.md b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
index c0efa079c..a66241dbd 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -173,10 +173,10 @@ Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claud
 
 | Executor tier | Escalation 1 (A3), adviser A | Escalation 1 (A3), adviser B | Escalation 2 (A4) |
 |---|---|---|---|
-| `haiku` | 1× `sonnet` | 1× GPT T1 | 2× `opus` |
-| `sonnet` | 1× `opus` | 1× GPT T1 | 2× `opus` |
-| `opus` (known) | 1× `opus` (top rung) | 1× GPT T1 | 2× `opus` |
-| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× GPT T1 | 2× `opus` |
+| `haiku` | 1× `sonnet` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| `sonnet` | 1× `opus` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| `opus` (known) | 1× `opus` (top rung) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
 
 **Resolving adviser B.** Before spawning, the parent resolves adviser B's model id and writes it on line 1 of `advice-3-b.md` in the header form given under Launch alias below. When no model of the other family can be reached, the parent spawns adviser B on `opus` and writes `family-fallback: <reason>` on that header line; the final summary lists every such fallback. This never STOPs and never prompts the user: a missing model is configuration, not a finding. The verified spawn path for a GPT T1 model on this install:
 
diff --git a/tests/skills/test_task_workspace_lifecycle.py b/tests/skills/test_task_workspace_lifecycle.py
index 70a347125..9f3526e12 100644
--- a/tests/skills/test_task_workspace_lifecycle.py
+++ b/tests/skills/test_task_workspace_lifecycle.py
@@ -596,10 +596,10 @@ def test_retry_ref_rules_text():  # STATIC (wording pins only)
     assert "The two ladders are never mixed." in r
     assert "never used as an adviser" in r and "`T2Model01` is on par" in r
     for row in (
-        "| `haiku` | 1× `sonnet` | 1× GPT T1 | 2× `opus` |",
-        "| `sonnet` | 1× `opus` | 1× GPT T1 | 2× `opus` |",
-        "| `opus` (known) | 1× `opus` (top rung) | 1× GPT T1 | 2× `opus` |",
-        "| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× GPT T1 | 2× `opus` |",
+        "| `haiku` | 1× `sonnet` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |",
+        "| `sonnet` | 1× `opus` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |",
+        "| `opus` (known) | 1× `opus` (top rung) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |",
+        "| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |",
     ):
         assert row in r, row
     # Ruling eligibility rule (a)/(b)
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

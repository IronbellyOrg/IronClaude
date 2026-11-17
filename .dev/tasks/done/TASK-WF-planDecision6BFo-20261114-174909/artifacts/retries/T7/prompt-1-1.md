1d158ef317a622df35cea00c2fdee44c4cc24206
Review one task for spec compliance.

Task brief: ## Task 7: Build the worker brief from fixed templates

Depends on: Task 1

Create `src/superclaude/cli/issue_pipeline/brief.py`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `tests/issue_pipeline/test_brief.py`. The builder emits the Task spec the coordinator passes to `worker-start --spec`, in the brief layout of src/superclaude/core/WORKER-CONTRACT.md (the guard line, the chain line, `On a blocked gate: report blocked`, `Local commit: not authorized`, a report directory unique to the Task, the worktree line, `Outward actions: none`, and one `Command:` line per step with `--unattended` and exactly one report directory). Its only inputs are the issue number (a validated integer) and two values read from the claim's summary: the type (`feature` or `bug`) and the complexity (`simple`, `medium` or `complex`), each checked against the closed set. The builder builds the three Feature rows only. For type `bug` it refuses with the closed reason `type-not-supported` and produces no brief; no Bug row, no bug symptom phrase and no `--scope` handling are built. The three rows come from the Feature rows of src/superclaude/skills/sc-issue-protocol/refs/chains.md and stop before `/sc:implement` or `/task`: simple is `/sc:brainstorm` quick then `/sc:workflow` quick; medium is `/sc:brainstorm` with `--blind`, `/sc:design` and `/sc:workflow` standard; complex is `/sc:brainstorm` deep with codebase research and `--blind`, `/sc:design` and `/sc:workflow` deep. Every `Command:` line carries `--unattended`, one report directory and (for workflow) `--handoff none`.

`/sc:design` requires `--type <architecture|api|component|database>` and the rows add `--format spec`. The builder uses a fixed `--type architecture` in the medium and complex rows; it adds no third enum, because the type only steers the shape of the design document and the issue's text never chooses it. Command text never contains issue words: the topic is the fixed phrase `issue <N>` with `@.dev/issues/<N>/issue-summary.md`.

Start condition: the builder can be written now; the coordinator uses its output only after the two-copy test in WORKER-CONTRACT.md passes for each command in the rows. `/sc:brainstorm`, `/sc:design` and `/sc:workflow` are all in the default converted set of the first conversion phase (WORKER-CONTRACT.md line 317), so no extra live check is needed for them; the P2 sentence (line 318) names only the later commands such as `/sc:troubleshoot`, which no row uses.

Acceptance criteria:
- A golden test per Feature row (three rows: simple, medium, complex) compares the full brief text, the medium and complex rows contain `/sc:design` with `--type architecture`, and a property test shows the output contains only template characters plus the validated integer, for any input including hostile titles, labels and summary text.
- A test shows any value outside the enums, a non-integer issue number, or type `bug` makes the builder refuse with a closed reason (`type-not-supported` for `bug`) and produce no brief.
- A test shows no row contains `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`, and no `Command:` line lacks `--unattended`.
- A test shows the template's Guard, Chain, `Local commit`, `Outward actions` and blocked-gate lines equal the brief template in section 5 of src/superclaude/core/WORKER-CONTRACT.md (the template block is lines 302-311, the Guard line is 303) word for word, so the two copies cannot drift; the `Worktree:` slot (line 308) is the one place the builder differs (it uses `path:<existing worktree>`, see Plan B Task 9).
- `uv run pytest tests/issue_pipeline/test_brief.py -v` passes.

AC ids (source order): T7.AC1 = bullet 1 of "Acceptance criteria"; T7.AC2 = bullet 2 of "Acceptance criteria"; T7.AC3 = bullet 3 of "Acceptance criteria"; T7.AC4 = bullet 4 of "Acceptance criteria"; T7.AC5 = bullet 5 of "Acceptance criteria"
Global constraints: ## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.
Start sha: 1d158ef317a622df35cea00c2fdee44c4cc24206
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/brief.py b/src/superclaude/cli/issue_pipeline/brief.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/brief.py
@@ -0,0 +1,55 @@
+"""Build the plan-writing worker's brief from a fixed template (plan Task 7).
+
+The output is the Task spec the coordinator passes to ``worker-start --spec``, in the brief
+layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. The only inputs are the issue
+number (a validated integer) and two values read from the claim's summary, the type and the
+complexity, each checked against a closed set. No issue text can reach the brief: the template
+holds every other character. Only the three Feature rows are built; type ``bug`` is refused.
+The rows stop before ``/sc:implement`` and ``/task``.
+"""
+
+from __future__ import annotations
+
+from importlib import resources
+
+from superclaude.cli.issue_watch.predicates import valid_issue_number
+
+TYPES = ("feature", "bug")
+COMPLEXITIES = ("simple", "medium", "complex")
+
+
+class BriefRefused(Exception):
+    """A closed refusal; no brief is produced. ``reason`` never holds input text."""
+
+    def __init__(self, reason: str) -> None:
+        super().__init__(reason)
+        self.reason = reason
+
+
+def _sections() -> dict[str, list[str]]:
+    text = resources.files(__package__).joinpath("templates/worker-brief.txt").read_text(encoding="utf-8")
+    sections: dict[str, list[str]] = {}
+    current: list[str] | None = None
+    for line in text.splitlines():
+        if line.startswith("#") or not line:
+            continue
+        if line.startswith("[") and line.endswith("]"):
+            current = sections.setdefault(line[1:-1], [])
+        elif current is not None:
+            current.append(line)
+    return sections
+
+
+def build(issue: object, type_: object, complexity: object) -> str:
+    """Return the brief for a Feature issue, or raise ``BriefRefused`` with a closed reason."""
+    if not valid_issue_number(issue):
+        raise BriefRefused("bad-issue")
+    if type_ not in TYPES:
+        raise BriefRefused("bad-type")
+    if type_ == "bug":
+        raise BriefRefused("type-not-supported")
+    if complexity not in COMPLEXITIES:
+        raise BriefRefused("bad-complexity")
+    sections = _sections()
+    lines = [*sections["head"], *sections[str(complexity)]]
+    return "\n".join(lines).replace("{N}", str(issue)) + "\n"
diff --git a/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt b/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/templates/worker-brief.txt
@@ -0,0 +1,24 @@
+# Worker brief template for the plan-writing worker (issue pipeline, plan Task 7).
+# Slots: {N} (a validated issue number) only. The five fixed lines below are copied from
+# section 5 of src/superclaude/core/WORKER-CONTRACT.md; a test keeps the two copies equal.
+# The Worktree line differs on purpose: the coordinator fills the path of the worktree the
+# claim script made (Plan B Task 9). Rows stop before /sc:implement and /task.
+[head]
+Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
+On a blocked gate: report blocked
+Local commit: not authorized
+Report directory: .dev/issues/{N}/worker-plan
+Worktree: path:<existing worktree>
+Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
+[simple]
+Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --depth quick --unattended --output .dev/issues/{N}/worker-plan/brainstorm
+Command: /sc:workflow .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --depth quick --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
+[medium]
+Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --blind --unattended --output .dev/issues/{N}/worker-plan/brainstorm
+Command: /sc:design .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir .dev/issues/{N}/worker-plan/design
+Command: /sc:workflow .dev/issues/{N}/worker-plan/design/design-report.md --depth standard --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
+[complex]
+Command: /sc:brainstorm "issue {N} @.dev/issues/{N}/issue-summary.md" --depth deep --research deep --codebase --blind --unattended --output .dev/issues/{N}/worker-plan/brainstorm
+Command: /sc:design .dev/issues/{N}/worker-plan/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir .dev/issues/{N}/worker-plan/design
+Command: /sc:workflow .dev/issues/{N}/worker-plan/design/design-report.md --depth deep --handoff none --unattended --report-dir .dev/issues/{N}/worker-plan/workflow
diff --git a/tests/issue_pipeline/test_brief.py b/tests/issue_pipeline/test_brief.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_brief.py
@@ -0,0 +1,138 @@
+"""Task 7: the worker brief is built from fixed templates."""
+
+from __future__ import annotations
+
+import random
+import re
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_pipeline import brief
+
+ROOT = Path(__file__).resolve().parents[2]
+CONTRACT = ROOT / "src/superclaude/core/WORKER-CONTRACT.md"
+TEMPLATE = ROOT / "src/superclaude/cli/issue_pipeline/templates/worker-brief.txt"
+
+HEAD = """Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
+On a blocked gate: report blocked
+Local commit: not authorized
+Report directory: .dev/issues/452/worker-plan
+Worktree: path:<existing worktree>
+Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
+"""
+D = ".dev/issues/452/worker-plan"
+BRAIN = '/sc:brainstorm "issue 452 @.dev/issues/452/issue-summary.md"'
+GOLDEN = {
+    "simple": HEAD
+    + f"Command: {BRAIN} --depth quick --unattended --output {D}/brainstorm\n"
+    + f"Command: /sc:workflow {D}/brainstorm/merged-requirements.md --depth quick --handoff none --unattended --report-dir {D}/workflow\n",
+    "medium": HEAD
+    + f"Command: {BRAIN} --blind --unattended --output {D}/brainstorm\n"
+    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
+    + f"Command: /sc:workflow {D}/design/design-report.md --depth standard --handoff none --unattended --report-dir {D}/workflow\n",
+    "complex": HEAD
+    + f"Command: {BRAIN} --depth deep --research deep --codebase --blind --unattended --output {D}/brainstorm\n"
+    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
+    + f"Command: /sc:workflow {D}/design/design-report.md --depth deep --handoff none --unattended --report-dir {D}/workflow\n",
+}
+
+
+@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
+def test_golden_brief_per_feature_row(complexity: str) -> None:
+    assert brief.build(452, "feature", complexity) == GOLDEN[complexity]
+
+
+@pytest.mark.parametrize("complexity", ["medium", "complex"])
+def test_design_rows_use_a_fixed_architecture_type(complexity: str) -> None:
+    text = brief.build(7, "feature", complexity)
+    design = [line for line in text.splitlines() if "/sc:design" in line]
+    assert len(design) == 1 and "--type architecture --format spec" in design[0]
+    assert "/sc:design" not in brief.build(7, "feature", "simple")
+
+
+def _template_characters() -> set[str]:
+    body = "".join(line for line in TEMPLATE.read_text().splitlines(keepends=True) if not line.startswith("#"))
+    return set(body) | set("0123456789")
+
+
+def test_output_holds_only_template_characters_plus_the_issue_number() -> None:
+    allowed = _template_characters()
+    rng = random.Random(7)
+    numbers = [1, 9, 452, 99999, *(rng.randrange(1, 10**9) for _ in range(30))]
+    for n in numbers:
+        for complexity in ("simple", "medium", "complex"):
+            text = brief.build(n, "feature", complexity)
+            assert set(text) <= allowed
+            # the output is the template section with {N} replaced by the validated number, nothing else
+            assert text == _expected_from_template(n, complexity)
+            assert text.count(str(n)) >= 3
+
+
+def _expected_from_template(n: int, complexity: str) -> str:
+    sections: dict[str, list[str]] = {}
+    current: list[str] | None = None
+    for line in TEMPLATE.read_text().splitlines():
+        if line.startswith("#") or not line:
+            continue
+        if line.startswith("["):
+            current = sections.setdefault(line[1:-1], [])
+        elif current is not None:
+            current.append(line)
+    return "\n".join([*sections["head"], *sections[complexity]]).replace("{N}", str(n)) + "\n"
+
+
+HOSTILE = ["<script>x</script>", "$(rm -rf /)", "simple; /sc:implement x", "simple\n/sc:implement x", "SIMPLE", "", " simple", "simple ", None, 5, ["simple"], "‮simple"]
+
+
+@pytest.mark.parametrize("value", HOSTILE)
+def test_values_outside_the_enums_refuse_with_a_closed_reason(value: object) -> None:
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(452, "feature", value)
+    assert err.value.reason == "bad-complexity"
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(452, value, "simple")
+    assert err.value.reason == "bad-type"
+
+
+@pytest.mark.parametrize("issue", [0, -3, "452", "4 5", 4.0, True, None, 2**63, [1], "452\n/sc:implement"])
+def test_a_non_integer_issue_number_is_refused(issue: object) -> None:
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(issue, "feature", "simple")
+    assert err.value.reason == "bad-issue"
+
+
+@pytest.mark.parametrize("complexity", ["simple", "medium", "complex", "bogus"])
+def test_type_bug_is_refused_and_builds_no_brief(complexity: str) -> None:
+    with pytest.raises(brief.BriefRefused) as err:
+        brief.build(452, "bug", complexity)
+    assert err.value.reason == "type-not-supported"
+
+
+def test_no_row_runs_implement_commit_push_or_submit_and_every_command_is_unattended() -> None:
+    forbidden = ("/sc:implement", "/task", "git commit", "git push", "/sc:pr-submit")
+    for complexity in ("simple", "medium", "complex"):
+        text = brief.build(452, "feature", complexity)
+        commands = [line for line in text.splitlines() if line.startswith("Command:")]
+        assert len(commands) >= 2
+        for token in forbidden:
+            assert token not in text, (complexity, token)
+        for line in commands:
+            assert "--unattended" in line
+            assert len(re.findall(r"--(?:output|report-dir) ", line)) == 1  # exactly one report directory
+            if line.startswith("Command: /sc:workflow"):
+                assert "--handoff none" in line
+
+
+def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
+    contract = CONTRACT.read_text()
+    block = re.search(r"## 5\. Coordinator brief template.*?```text\n(.*?)```", contract, re.S).group(1).splitlines()
+    ours = brief.build(452, "feature", "simple").splitlines()
+    for prefix in ("Guard:", "Chain:", "On a blocked gate:", "Local commit:", "Outward actions:"):
+        theirs = [line for line in block if line.startswith(prefix)]
+        mine = [line for line in ours if line.startswith(prefix)]
+        assert len(theirs) == len(mine) == 1 and theirs == mine, prefix
+    # the one deliberate difference: the Worktree slot
+    assert next(line for line in block if line.startswith("Worktree:")).startswith("Worktree: <shared feature worktree")
+    assert "Worktree: path:<existing worktree>" in ours

Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor.

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

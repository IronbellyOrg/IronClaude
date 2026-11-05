1a446509ac9543f34ffa12654da725602876f671
Review one task for spec compliance.

Task brief: T1 (AC ids in order of the "Acceptance criteria:" bullets: T1.AC1,T1.AC2,T1.AC3,T1.AC4,T1.AC5). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 30-40:
## Task 1: Make the FINAL derived-test bullet the single statement of the comparison (rule A)

Before any edit, save `git status --porcelain -- docs src plugins tests` as `./artifacts/t1-status-before.txt`, and write `./artifacts/extract-blocks.py` (run with `PYTHONDONTWRITEBYTECODE=1 uv run python -I`) that takes `qa` or `ledger` and a file path and prints, for `qa`, the reviewer template fenced block (the fenced block whose first line is "Review one task for spec compliance.") and, for `ledger`, every fenced block that follows a `ledger-grammar-block` marker comment. Then, in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` make exactly two edits. First, in section "## FINAL derived test", replace the bullet that begins "- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template" so that it says: line 1 of every saved prompt is the task's start sha, and FINAL compares the lines after that header and outside the slots; a prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference and is recorded as a note (cited `noted`), not `issues`; any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before. Use the exact phrases "differs only in blank lines or trailing whitespace" and "after the start-sha header". Second, in section "## Subagent prompt (when not inline)", in the bullet under "Saved prompts and paperwork-only reviews" that begins "- The orchestrator saves the exact prompt of review", replace its last sentence ("Both FINALs (managed and legacy) compare every saved prompt with this template outside the slots, and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ.") with a sentence that points to the saved-prompt rule in "## FINAL derived test" instead of restating it. Keep both rewritten bullets free of the words listed in the second Constraints bullet. Copy the edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/qa.md`.

Acceptance criteria:
- `grep -c "differs only in blank lines or trailing whitespace" src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints 1 and that line is inside "## FINAL derived test" and also contains "after the start-sha header"; `grep -c "when they differ"` on the same file prints 0; and the rewritten bullet that begins "- The orchestrator saves the exact prompt of review" contains "## FINAL derived test"; all outputs saved as `./artifacts/t1-grep.txt`.
- At the end of this task, `git diff -U0 HEAD -- src/superclaude/skills/sc-implement-protocol/refs/qa.md` has exactly two `@@` hunks, one in each of the two bullets named above; the diff is saved as `./artifacts/t1-diff.txt` and the hunk count (`grep -c '^@@'`) as `./artifacts/t1-hunks.txt`. These saved files are the evidence; later tasks edit the same file.
- The output of `extract-blocks.py qa` on the edited file is `cmp`-equal to its output on `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/qa.md` saved to a scratch file under `./artifacts/`; the `cmp` exit code is saved in `./artifacts/t1-template-cmp.txt`.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` passes with no failures (`./artifacts/t1-pytest-skills.txt`; the baseline before this plan was 804 passed), and `git status --porcelain -- tests` shows no entry for `tests/skills/test_implement_severity_static.py` (`./artifacts/t1-tests-status.txt`).
- `cmp` of the `src/` and `plugins/` copies of `refs/qa.md` exits 0 (`./artifacts/t1-cmp.txt`), and the number of lines containing `src/superclaude` in `refs/qa.md` equals that in `git show HEAD:` of the same file (both counts in `./artifacts/t1-srcpath.txt`).


Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md lines 17-27)
## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template block (the fenced block that begins "Review one task for spec compliance." under "## Subagent prompt (when not inline)" in `refs/qa.md`) and the `ledger-grammar-block` fenced blocks in `refs/ledger.md` do not change.
- `tests/skills/test_implement_severity_static.py` is not modified. Its classification test fails on any line in the protocol files that matches the words `Ruling` (capital R), `halt`, `halts`, `halted`, `halting`, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` and is not already listed there, so every new or rewritten line in the three refs avoids those words (say "a user-accepted gap" and "stop"), and additions to step 6 of `refs/managed-workspace.md` stay inside the existing single step-6 line. The existing wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" stays verbatim.
- A prompt-builder script, any other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, and the globally installed copy of this skill (it changes when the user runs `superclaude install`) are out of scope.
- Never stage `.claude/` contents. `make sync-dev` copies `src/superclaude/` into `.claude/` only and does not touch `plugins/`, so each task copies its edited ref into the `plugins/` twin by hand, and Task 5 runs `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.


Start sha: 1a446509ac9543f34ffa12654da725602876f671
Diff against the start snapshot: (git diff 1a446509ac9543f34ffa12654da725602876f671 -- src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
index 4496f6c9..631b22b7 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -294,7 +294,7 @@ This is the single statement for both FINALs (the managed archive FINAL and the
 - Both FINALs read the notes, probe, prompt and review files in `<retries>/T<id>/`, apply the severity test of "## Severity model" with the anchor Read-back to the end state, and return `issues` only for a blocking defect. The legacy FINAL applies the same test and stays advisory.
 - A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even when its line labels it minor.
 - History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history. FINAL judges the end state, not those lines.
-- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template; when the two differ outside the slots, return `issues` (managed) or record it in `FINAL:` evidence (legacy).
+- Saved prompts: line 1 of every saved prompt `prompt-<k>-<j>.md` is the task's start sha, and FINAL compares the lines after the start-sha header and outside the slots with the reviewer template. A prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference: record it as a note (cited `noted`), not `issues`. Any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before.
 - The legacy FINAL trigger depends on task status, not on the verdict value, so the accepted-minor path leaves it unchanged. The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line. For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver.
 
 Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back; for those runs the final summary prints every recorded minor.
@@ -362,5 +362,5 @@ These are reviewer outputs and parent-run searches, not implementer claims or ad
 
 Saved prompts and paperwork-only reviews:
 
-- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. Both FINALs (managed and legacy) compare every saved prompt with this template outside the slots, and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ.
+- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. The comparison of a saved prompt with this template, and its result, are stated once, in "## FINAL derived test".
 - A review whose only failure is reviewer paperwork (an AC mark with no citation or a bare or malformed one, an `unmet` mark that lists no finding id, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`). It never fails the attempt and never starts the ladder. An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork; it counts as met with its citation ("## Verdict owner").
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 4496f6c9..631b22b7 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -294,7 +294,7 @@ This is the single statement for both FINALs (the managed archive FINAL and the
 - Both FINALs read the notes, probe, prompt and review files in `<retries>/T<id>/`, apply the severity test of "## Severity model" with the anchor Read-back to the end state, and return `issues` only for a blocking defect. The legacy FINAL applies the same test and stays advisory.
 - A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even when its line labels it minor.
 - History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history. FINAL judges the end state, not those lines.
-- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template; when the two differ outside the slots, return `issues` (managed) or record it in `FINAL:` evidence (legacy).
+- Saved prompts: line 1 of every saved prompt `prompt-<k>-<j>.md` is the task's start sha, and FINAL compares the lines after the start-sha header and outside the slots with the reviewer template. A prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference: record it as a note (cited `noted`), not `issues`. Any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before.
 - The legacy FINAL trigger depends on task status, not on the verdict value, so the accepted-minor path leaves it unchanged. The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line. For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver.
 
 Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back; for those runs the final summary prints every recorded minor.
@@ -362,5 +362,5 @@ These are reviewer outputs and parent-run searches, not implementer claims or ad
 
 Saved prompts and paperwork-only reviews:
 
-- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. Both FINALs (managed and legacy) compare every saved prompt with this template outside the slots, and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ.
+- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. The comparison of a saved prompt with this template, and its result, are stated once, in "## FINAL derived test".
 - A review whose only failure is reviewer paperwork (an AC mark with no citation or a bare or malformed one, an `unmet` mark that lists no finding id, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`). It never fails the attempt and never starts the ladder. An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork; it counts as met with its citation ("## Verdict owner").

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-status-before.txt ===
 M docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
M  docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/extract-blocks.py ===
"""Print the fenced blocks that must not change when the saved-prompt rules are edited.

Usage: uv run python -I extract-blocks.py <qa|ledger> <path>

qa     the reviewer template block: the fenced block whose first line is
       "Review one task for spec compliance."
ledger every fenced block that follows a ledger-grammar-block marker comment
       (the marker line is printed too)
"""
import sys

FENCE = "```"


def fenced_after(lines, start):
    """Return (block_lines, next_index) for the fence that opens at lines[start]."""
    assert lines[start].startswith(FENCE), lines[start]
    end = start + 1
    while end < len(lines) and not lines[end].startswith(FENCE):
        end += 1
    return lines[start : end + 1], end + 1


def main(mode, path):
    lines = open(path, encoding="utf-8").read().split("\n")
    out = []
    if mode == "qa":
        for i, line in enumerate(lines):
            if line.startswith(FENCE) and i + 1 < len(lines) and lines[i + 1] == "Review one task for spec compliance.":
                block, _ = fenced_after(lines, i)
                out.extend(block)
                break
        else:
            sys.exit("template block not found")
    elif mode == "ledger":
        i = 0
        while i < len(lines):
            if lines[i].startswith("<!-- ledger-grammar-block:"):
                out.append(lines[i])
                j = i + 1
                while j < len(lines) and not lines[j].startswith(FENCE):
                    j += 1
                block, i = fenced_after(lines, j)
                out.extend(block)
            else:
                i += 1
        if not out:
            sys.exit("no ledger-grammar-block found")
    else:
        sys.exit("mode must be qa or ledger")
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-grep.txt ===
$ grep -c 'differs only in blank lines or trailing whitespace' qa.md
1
$ grep -n lines with that phrase and 'after the start-sha header' (same line):
1
section of that line (nearest preceding ## heading):
## FINAL derived test
$ grep -c 'when they differ' qa.md
0
bullet 'The orchestrator saves the exact prompt' contains '## FINAL derived test':
1

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-diff.txt ===
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 4496f6c9..631b22b7 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -297 +297 @@ This is the single statement for both FINALs (the managed archive FINAL and the
-- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template; when the two differ outside the slots, return `issues` (managed) or record it in `FINAL:` evidence (legacy).
+- Saved prompts: line 1 of every saved prompt `prompt-<k>-<j>.md` is the task's start sha, and FINAL compares the lines after the start-sha header and outside the slots with the reviewer template. A prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference: record it as a note (cited `noted`), not `issues`. Any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before.
@@ -365 +365 @@ Saved prompts and paperwork-only reviews:
-- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. Both FINALs (managed and legacy) compare every saved prompt with this template outside the slots, and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ.
+- The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. The comparison of a saved prompt with this template, and its result, are stated once, in "## FINAL derived test".

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-hunks.txt ===
hunks: 2

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-template-cmp.txt ===
template cmp exit=0 lines=32

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-cmp.txt ===
twin cmp exit=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-srcpath.txt ===
src/superclaude lines: now 0 head 0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-pytest-skills.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 804 items

tests/skills/test_brainstorm_protocol.py .                               [  0%]
tests/skills/test_codegraph_adoption.py ................................ [  4%]
..................                                                       [  6%]
tests/skills/test_implement_adviser_family.py ...                        [  6%]
tests/skills/test_implement_retry_citation.py .....................      [  9%]
tests/skills/test_implement_retry_revert.py ............................ [ 12%]
..........................                                               [ 16%]
tests/skills/test_implement_severity_replay.py ............              [ 17%]
tests/skills/test_implement_severity_static.py ......................... [ 20%]
...                                                                      [ 21%]
tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 21%]
tests/skills/test_reflect_input_snapshot.py ...............              [ 23%]
tests/skills/test_repo_inventory_nongit.py .....                         [ 23%]
tests/skills/test_review_severity_rule.py .............................. [ 27%]
................................                                         [ 31%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 34%]
......                                                                   [ 34%]
tests/skills/test_task_builder_merge.py ................................ [ 38%]
....................................                                     [ 43%]
tests/skills/test_task_workspace_lifecycle.py .......................... [ 46%]
...............................................                          [ 52%]
tests/skills/test_task_workspace_smoke.py ....                           [ 52%]
tests/skills/test_tier2_tavily_consistency.py .....                      [ 53%]
tests/skills/test_worker_contract.py ................................... [ 57%]
........................................................................ [ 66%]
........................................................................ [ 75%]
.................                                                        [ 77%]
tests/skills/test_workflow_archive.py .................................. [ 82%]
........................................................................ [ 91%]
.......................................................................  [100%]

============================= 804 passed in 14.05s =============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t1-tests-status.txt ===

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

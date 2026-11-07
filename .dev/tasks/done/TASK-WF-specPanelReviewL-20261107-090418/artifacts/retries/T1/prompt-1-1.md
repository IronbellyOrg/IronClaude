bc9c5e72a265044ce8694ac2ac4516af899d918b
Review one task for spec compliance.

Task brief: ## Task 1: Add the Usage tail and the Review Loop section to the source command

Edit `src/superclaude/commands/spec-panel.md`. Append ` [--re-review <prior-findings-file> --baseline <saved-copy>]` to the Usage line (line 22, inside the first text fence), after `[--format standard|structured|detailed]` (source section 4). Insert the `## Review Loop` section, copied from the fenced block in section 5 of ./source.md (heading, blank line, seven one-line bullets, Mode through Precedence), immediately before the `## Output Formats` heading (line 254 before the edit), with a blank line before and after.

Acceptance criteria:
- The Usage line ends with the new tail and nothing else on that line changed.
- `## Review Loop` appears exactly once, before `## Output Formats`, followed by exactly seven lines that start with a digit, a period and a bold label, in the order Mode, Grading, Verdict, Cap, Re-review output, Reviser contract, Precedence.
- The section contains `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` and `HALT and escalate to the user with the open blocking findings`, and no `src/superclaude` path.
- `uv run pytest tests/skills/test_review_severity_rule.py` passes; the output is saved to ./artifacts/t1-severity-test.log.


AC ids in source order: T1.AC1 = bullet 1 of the Acceptance criteria block; T1.AC2 = bullet 2 of the Acceptance criteria block; T1.AC3 = bullet 3 of the Acceptance criteria block; T1.AC4 = bullet 4 of the Acceptance criteria block; 
Global constraints: ## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.
Start sha: bc9c5e72a265044ce8694ac2ac4516af899d918b
Diff against the start snapshot: diff --git a/src/superclaude/commands/spec-panel.md b/src/superclaude/commands/spec-panel.md
index b8db23a4..a2186d8f 100644
--- a/src/superclaude/commands/spec-panel.md
+++ b/src/superclaude/commands/spec-panel.md
@@ -19,7 +19,7 @@ personas: [technical-writer, system-architect, quality-engineer]
 ## Usage
 
 ```text
-/sc:spec-panel [specification_content|@file] [--mode discussion|critique|socratic] [--experts "name1,name2"] [--focus area1,area2,...] [--iterations N] [--format standard|structured|detailed]
+/sc:spec-panel [specification_content|@file] [--mode discussion|critique|socratic] [--experts "name1,name2"] [--focus area1,area2,...] [--iterations N] [--format standard|structured|detailed] [--re-review <prior-findings-file> --baseline <saved-copy>]
 ```
 
 Focus areas (comma-separated, one or more): `requirements`, `architecture`, `testing`, `compliance`, `correctness`
@@ -251,6 +251,16 @@ When `--focus correctness` is active, the panel MUST produce a State Variable Re
 - Example and scenario enhancement
 - Final validation and consistency checks
 
+## Review Loop
+
+1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review.
+2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision.
+3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open).
+4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review.
+5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
+6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
+7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking.
+
 ## Output Formats
 
 ### Standard Format (`--format standard`)
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

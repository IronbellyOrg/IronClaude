3de7f09e60ccee073a7342584a24e7fa47963d29
Review one task for spec compliance.

Task brief: ## Task 3: Replace the review-loop sentence in the routing guide

Edit `src/superclaude/core/HOW-WE-WORK.md` line 65. Replace the text from "ask Claude to apply them to the PRD" to the end of the line with the sentence in the text fence of section 6 of ./source.md ("save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings."). Keep the "It only reports. Decide which findings to accept, " prefix. Change no other line; the file stays ASCII.

Acceptance criteria:
- Line 65 contains `--re-review`, `--baseline` and `save a copy of the PRD`, and the file no longer contains `until no critical findings remain`.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py` passes (no routing row id or level-table change); output saved to ./artifacts/t3-routing-tests.log.


AC ids in source order: T3.AC1 = bullet 1 of the Acceptance criteria block; T3.AC2 = bullet 2 of the Acceptance criteria block; 
Global constraints: ## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.
Start sha: 3de7f09e60ccee073a7342584a24e7fa47963d29
Diff against the start snapshot: diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index fe14e11c..1ee1bf2e 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -62,7 +62,7 @@ Use this when people need to agree on *what* is being built and *how* before any
 
 3. **Get an expert critique of the PRD.**
    `/sc:spec-panel @docs/billing/PRD_BILLING.md --mode critique --focus requirements`
-   A panel of named software-requirements experts judges whether the requirements are measurable, testable, and complete. It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.
+   A panel of named software-requirements experts judges whether the requirements are measurable, testable, and complete. It only reports. Decide which findings to accept, save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings.
 
 4. **Write the technical design document (TDD) from the PRD.** The TDD defines *how* it will be built: architecture, data, interfaces, testing, and migration.
    `/tdd "Create a TDD for the billing service from docs/billing/PRD_BILLING.md. Relevant code: src/billing/, src/api/metering/. Output to docs/billing/TDD_BILLING.md."`
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

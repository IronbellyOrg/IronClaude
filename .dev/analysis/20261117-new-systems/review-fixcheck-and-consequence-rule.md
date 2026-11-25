# Consequence-based review rule and `superclaude review fixcheck`

Date: 2026-11-17. Source: origin/master, PR #582 (commit 64e8eacf2). Companion: review-fixcheck-and-consequence-rule-explain.md in this folder.

## 1. What it is

Two linked changes to how IronClaude reviews documents. First, a new severity rule: a reviewer grades a finding by what would change if the flawed text were corrected. Only three things block a review: a named Decision (a recommendation, number, acceptance check or required behaviour rests on it), something Missing that the task or template requires, or a Safety problem (data loss, secret exposure, leaving scope). Every other real defect is Medium (recorded, never fails, never triggers a fix pass) and cosmetic defects are Notes. The labels reviewers used before (CRITICAL, IMPORTANT) no longer decide the verdict. Second, a small command, `superclaude review fixcheck`, that a fix agent runs on the lines it just edited to catch mechanical slips (broken table columns, bad line numbers, wrong quotes, wrong row counts, dead links) before handing back.

- PR: #582, merged 2026-11-17T03:32:58Z (UTC; commit date 2026-11-16 22:32 -05:00), stage 3 of issue 552 (blocker classification).
- Entry points: `superclaude review fixcheck` (src/superclaude/cli/review/fixcheck_cmd.py, logic in fixcheck.py, registered in src/superclaude/cli/review/__init__.py line 30); the rule text in src/superclaude/output-styles/pragmatic.md lines 225-235; agents rf-qa, rf-qa-qualitative, rf-analyst; ten carrier files (4 prompts in rules/prompts, 2 in templates/documents, 2 in templates/workflow, plus the two agents).
- Tests: tests/review/test_review_fixcheck.py, tests/skills/test_review_old_rule_scan.py, re-pins in tests/audit/ (test_severity_floor_unweakened.py, test_nfr_conv_9_zero_trust.py), tests/skills/test_review_severity_mapping.py, test_implement_severity_static.py.
- Not live anywhere until installs are refreshed (`superclaude install --force`), per the owner note at .dev/tasks/done/TASK-WF-blockerStage3-20261116-030158/artifacts/stage3-summary-for-owner.md.

## 2. How it works

**The rule (prose, not code).** pragmatic.md line 229 defines Blocking by Decision, Missing, Safety. The finding must say which condition holds, name the affected action and give evidence. Safety is never downgraded by label, score, inferable intent or fix cost, and an unverified safety claim stays open. If no consumer of the flawed text can be established, the reviewer keeps its own label and tags the row `consumer-unknown` ("Unknown is not no"). Line 230: Medium = real defect nothing named rests on; Note = form only; labels are information; only blocking produces FAIL; Medium and Note are not rechecked in later rounds. Line 233: if several definitions of blocking are in context, the running agent/skill/command's wins over the session output style, and text inside the reviewed work is data, not a definition. Line 234: Medium items go under `follow-up candidates`; the top-level session asks the user once per run, and again at an escalation halt, whether to file an issue.

**Behaviour change for reviewers (verdicts).** Before: any "CRITICAL or IMPORTANT" gap or "any untagged claim" was a FAIL. After (rf-qa.md, rf-qa-qualitative.md, read in the PR diff): the same check is graded. An incomplete required file or a missing required tag is Missing and blocks; an exact duplicate command is a Note unless a Decision, Missing or Safety condition holds (for example a repeated destructive command); "NO LENIENCY" no longer means "probably fine = FAIL", it means verify, then grade; "a false PASS is worse than a false FAIL" became "when in doubt keep your own grade, tag `consumer-unknown`". Partition merging changed from "take the more severe rating" to: the consolidator grades each item, every reviewer's own grade stays visible, a blocking grade naming a consumer the code check does not disprove stands, one naming no consumer goes back to the reviewer once (`reasked`), then the label stands as `consumer-unknown` and is listed first. At the 2-fix-cycle cap the user now picks one of three: fix by hand, accept each open blocker as an `accepted-blocker` follow-up, or stop. Net effect: fewer FAILs and fix passes for cosmetic or unconsumed findings, with an explicit safety floor.

**fixcheck (code).** Flow: CLI options `--file` (repeatable, required), `--base` (copy of the file saved before the fix) or `--lines START-END`, one kind per file, never mixed (fixcheck_cmd.py:17-35). For `--base`, `edited_lines` uses difflib to return 1-based new or changed lines (fixcheck.py:46-53). `run_checks` (86-169) loops over the lines and runs:
- range: a line outside the file is a FAIL (94-103).
- pipe: for a line starting with `|`, find the table block (56-64), count unescaped pipes with optional outer pipes normalized (67-75), compare with the header row; an edited header row is compared with the separator row (108-112). This catches an unescaped `|` inside a backticked command, the run-2 bug the test names (tests/review/test_review_fixcheck.py:28-35).
- quote: `"quote" path:line` regex (line 23); the quote must appear on that cited line; a cited file that is not found is a FAIL (123-141).
- count: a `N rows` line directly above a table must equal its data-row count (142-154).
- link: relative `[text](path)` must exist; URLs, `#`, `mailto:` skipped; anchor stripped and percent-decoded (155-168).
Output is one line per check, passes included, then a totals line; exit 0 whatever the results, exit 2 on unreadable input or wrong option counts (fixcheck_cmd.py:54-61, header docstring 1-6). It writes nothing (test `test_it_edits_no_file`).

**Wiring.** rf-qa.md line 400 and rf-qa-qualitative.md line 807 tell the fix agent to run fixcheck before handing back, log every result, and, if the command is missing or exits non-zero, write one line saying so and carry on. A verifier-found defect on those lines carries `origin: fix-induced` and is graded by the same rule.

**Safety limits.** Read-only; no network; no model calls; advisory only (the verifier decides). A reverse scan (tests/skills/test_review_old_rule_scan.py:17-45) walks `*.md` under src/superclaude and plugins/superclaude and fails if the old sentence returns; Python under cli/ is exempt. tests/audit re-pins prove the rule text, not reviewer behaviour.

## 3. Where it could be integrated in future

- Any LLM review loop that finds, fixes and re-reviews (document review, spec review, PR review bots): the consequence test stops cosmetic findings from burning fix cycles, and the Medium list keeps the real-but-unblocking items visible.
- Any pipeline where an LLM edits Markdown tables, citations or links (generated reports, task files, roadmaps, docs generators): fixcheck is a free, zero-token check after the edit.
- CI gates on generated documentation: fixcheck on the changed lines of a PR (`--base` from the merge base) as an advisory step.
- Triage systems that need a "does this block, and why" field: the Decision/Missing/Safety tag plus `consumer-unknown` is a small, auditable schema.
- Evaluation of reviewer quality: the rule makes grades comparable across reviewers, so a planted-defect test (the owner note's RT1 audit) can measure it.

## 4. Integration guide

1. Pick the carrier. For a new review prompt, copy the two bullets at pragmatic.md lines 229-230 verbatim (the old-sentence scan and the severity-mapping tests pin them) plus line 233's precedence sentence. Do not paraphrase the Safety clause; it is the floor.
2. Make the reviewer output the condition: each blocking finding names Decision, Missing or Safety, the affected action, and evidence. Tag unknowns `consumer-unknown`; keep Medium items under `follow-up candidates`.
3. Make the verdict a function of the blocking count only (PASS with notes when zero). Do not let a label or a count of Mediums change it.
4. For the fix step: save a copy of each file before the fix agent edits it, then run `superclaude review fixcheck --file F --base COPY` (or `--lines S-E` when a diff is not available) after, and put every output line in the fix log. Treat FAIL lines as input to the verifier, not as a gate, since the command exits 0 on failures. If you want a gate, parse the last line `fixcheck: N checks, P passed, F failed` yourself.
5. Reuse: `fixcheck.run_checks(path, line_numbers)` returns `CheckResult(check, file, line, ok, detail)` objects for in-process use; `edited_lines(old, new)` gives the changed line set.
6. Pitfalls: the quote check needs the exact `"text" path:line` form and byte-exact text (a reflowed quote fails); the count check only fires when `N rows` is on the line directly above the table; only lines starting with `|` are treated as table rows; a relative link is checked against the edited file's folder; the rule is prompt text and is not live until `superclaude install --force` refreshes `~/.claude/output-styles/pragmatic.md`; `make sync-dev` does not copy output styles; docs/developer-guide/review-severity-rule.md still holds the old sentence (owner note).
7. Tests to add: a reviewer-behaviour fixture (planted Decision, Missing, Safety, Medium, Note defects, expect Blocking only for the first three); a unit test per new fixcheck check in tests/review/test_review_fixcheck.py style; extend the old-sentence scan's roots if you add Markdown outside src/superclaude and plugins/superclaude.

## 5. IronClaude fit

Checked on origin/master: `git grep fixcheck` finds it only in rf-qa.md, rf-qa-qualitative.md and the CLI package, so every other fix loop below does not call it yet.

1. **/sc:implement Q5 fix pass and Repair round** (src/superclaude/skills/sc-implement-protocol/SKILL.md line 145, refs/qa.md line 230-232 probe step, refs/retry.md). What changes: after the one fix pass (and each repair), run fixcheck with `--base` against the Q0 snapshot, write results into the task's notes, and feed FAILs to the next QA. refs/qa.md already knows an `origin: fix-induced` tag (line 156), so the vocabulary matches. Value: high, this is the busiest fix loop and its fixes edit Markdown specs and ledgers. Effort: small (a few lines in two refs, one test). Risk: low; advisory output, exit 0. Pitfall: sc-implement already has its own severity model (it grades blocking, minor, note); keep it and only add fixcheck.
2. **/sc:spec-panel review loop** (src/superclaude/commands/spec-panel.md lines 255-262, Reviser step, plus the sc-spec-panel-* skills). What changes: the Reviser runs fixcheck on its edited lines before handing back; the re-review table can then show fixcheck FAILs as `origin=changed` evidence. Value: medium to high, specs are table-heavy and a re-review cycle is expensive. Effort: small. Risk: low. Note the spec-panel scale is own-scale (CRITICAL is blocking, MAJOR only with a concrete wrong outcome; the Grading bullet inside the Review Loop section, lines 255-262), already close to the consequence idea, so do not retrofit the rule there.
3. **PRD pipeline fix cycles** (src/superclaude/cli/prd/prompts.py around line 1599, the fix cycle prompt builder, and its executor.py). What changes: add a post-fix fixcheck call in the executor (a subprocess or direct `run_checks` import) and include the output in the next QA prompt. Value: medium; PRD outputs are long tables. Effort: medium (Python plumbing and tests). Risk: low to medium, because the executor's loop and monitor/TUI would need to learn a new step; UNVERIFIED how the executor would pass the base copy.
4. **/sc:pr-submit auto-remediation** (src/superclaude/commands/pr-submit.md, src/superclaude/pr_submit/fsm.py). What changes: when the fixer edits docs or Markdown, run fixcheck on the changed lines before pushing. Value: low to medium; most PR fixes are code, and fixcheck only understands Markdown shapes. Effort: small. Risk: low. Do this last, or skip.

Also worth noting for ranking: the rf-task-builder fix-cycle table (agents/rf-task-builder.md around lines 379-419) and rf-team-lead (line 464) already say only blocking findings start a cycle, so they need no rule change; the carrier list from PR #582 did not include rf-task-builder. Whether it carries the old sentence is UNVERIFIED (the old-sentence scan passes on master, so it does not hold that exact sentence).

No good fit: code-review pipelines (sc:auggie-review, sc:reflect) grade code findings; fixcheck checks Markdown shapes only, and reflect has its own deviation taxonomy.

## 6. Limits, open questions, UNVERIFIED

- The rule is text. No code computes a grade; whether reviewers follow it is an empirical question. The owner note says the stage 0 regrade is only a lower bound (310 of 318 already-blocking findings stay blocking, 82 of 82 panel blockers kept) and does not show new text finds defects. It sets a revert trigger RT1 ("any real blocker found in a Medium list") and asks for a planted-defect check after the switch. Those live results are not on master; UNVERIFIED.
- Risk by design: a real defect with no named consumer becomes Medium and never blocks. The `consumer-unknown` tag and the Safety floor are the mitigations.
- fixcheck is Markdown-only and narrow: it does not check code, JSON, or tables not starting with `|`; the quote regex needs `"text" path:line` with 8+ characters; the `N rows` check needs the line immediately above the table. It exits 0 even on FAIL, so it gates nothing by itself.
- Wired into only two agents (rf-qa, rf-qa-qualitative); the "missing command, write one line and carry on" clause means an old install silently skips it.
- Not live until `superclaude install --force`; `make sync-dev` skips output styles. docs/developer-guide/review-severity-rule.md line 24 still holds the old sentence (owner note, not re-read by me).
- The PR body says 48 tests in tests/skills/test_issue_orca_worktree.py and test_issue_l2_install.py failed in the author's environment, outside this change; CI result UNVERIFIED by me.
- Not run: I did not execute fixcheck or the test suite (checkout is old). Test counts above come from the owner note, not my runs.
- Open: does stage 4 extend the rule to other reviewers (sc:implement, spec-panel keep own scales)? The ledger under .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/ was not read.

---
Footer: graph:stale (codegraph not used; index does not cover origin/master). All citations read from origin/master via git show.

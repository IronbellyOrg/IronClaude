# QA Report - Task Integrity, Lens b2-self-containment (Partition: P6 to P10)

**Topic:** GitHub issue watcher task file (TASK-RF-issue-watcher-20261107-150955)
**Date:** 2026-11-07
**Phase:** task-integrity
**Fix cycle:** N/A (fix_authorization: false)
**Scope:** Phases P6 to P10 (P1 to P5 covered by another agent). Cross-phase checks limited to this subset. [PARTITION NOTE: Cross-file checks limited to assigned subset.]

---

## Scope and method

Task file read in full for P6 (Steps 6.1-6.11), P7 (7.1-7.9, Gate C 7.G1-7.G12), P8 (8.1-8.12, Gate D 8.G1-8.G12), P9 (9.1-9.19, Final gate 9.F1-9.F13, M4 gate 9.M1-9.M8), P10 (10.1-10.8) and the Task Log (Open Questions OQ-1 to OQ-46, Reflect Depth Derivation). Compared with research/06 (all 328 lines), the design (docs/designs/issue-watcher.md), the spec (spec-final.md), the 02 template B1-B7, and the task-builder SKILL.md POST-reflect runner text (lines 2213-2240) and its validation rules (2308-2312). Item counts per phase checked by script: P6 11, P7 9, Gate C 12, P8 12, Gate D 12, P9 19, Final 13, M4 8, P10 8 (whole file 176, matches the stated 176).

Template B2 (lines 159-165, 177-179) accepts an integrated "ensuring ..." clause as the verification element and forbids separate verification items. Authoring items whose verification is an "ensuring" clause (rather than a command with an expected result) are therefore NOT graded as defects here; the command-with-expected-result requirement is met by the gate-run items that follow each authoring group.

## Findings (appended incrementally)

### Section 1: Lens checks 1-4 (B2 components, back-references, embedded prompts, paths)

**Check 1 (five B2 components).** Every item in P6-P10 has context (Read ...), action, output path, an "ensuring" verification and the "If unable ... mark complete" tail. The explicit B2 sentence "cannot be marked done until completed exactly as described" is absent task-wide, but the template's own B4 example also omits it, so it is not graded. PASS with the exceptions in Issue 2 and Issue 8.

**Check 2 (no item rests on prior-item context without restating it).** FAIL for the four fix-cycle control items (see Issue 2). Minor back-references: Step 9.17 ("re-running Step 9.4") and Step 10.4 ("`<BASE SHA>`" with no pointer to where it is stored). All other cross-item reads name a file path.

**Check 3 (agent-spawning items embed prompts).** PASS for the first-cycle prompts: 7.G2-7.G7, 8.G2-8.G7, 9.F2-9.F8, 9.M1-9.M3 and the fix and verifier items (7.G9-7.G11, 8.G9-8.G11, 9.F10-9.F12, 9.M5-9.M7) each carry a complete quoted prompt with agent type, lens, inputs, output path, `fix_authorization`, severity definition and adversarial framing. The POST reflect item 10.6 embeds the full verbatim runner prompt: compared line by line with SKILL.md 2221-2229, steps 1-5 and the COMPLETION CONTRACT are byte-identical apart from the resolved placeholders. FAIL for the cycle-2 path (Issue 2).

**Check 4 (file paths specific).** PASS. Every output path is a full `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/...` path; QA report names are exact and the consolidate items forbid wildcards.

### Section 2: Lens checks 5-9 (verification, batching, contradicted claims, citations, TB-Add-8)

**Check 5 (verification measurable).** PASS under B2 (see Scope). The gate-run items (6.10, 6.11, 7.6-7.9, 8.9-8.12, 9.4-9.16) give command, raw-output path and expected result (exit 0, NO_MATCH, exact command list).

**Check 6 (no batch items).** PASS for gate agents: one item per lens agent, one per fix agent, one per verifier; the parallel notes are execution hints, each item is marked individually. Size note only (Issue 11): Steps 6.2 and 6.7 are very large single items.

**Check 7 ([CODE-CONTRADICTED] / [UNVERIFIED] claims used as fact).** The three research/02 contradictions (C14 collision premise, C21 "G2 to G7" scope, X13 stub-precedent file) are handled: Open Questions section F and DF-27/28 record them, Steps 8.1/8.2 cite the correct `test_conflict_scripts.py:167-179`, and the Gate C/Final prompts tell agents the false claims must not be repeated. No P6-P10 item states a gh or Orca reply shape as fact; the e2e item 8.2 takes replies from `_assumed_shape` fixtures. PASS, except the false statement about the model-alias test (Issue 4).

**Check 8 (citations exist and say what the item claims), 31 spot-checks.**

| # | Citation (item) | Result |
|---|---|---|
| 1 | D 233-242 import table (6.1, 7.1, 8.8, 7.G4) | matches; `record` row says `predicates` types only, `launch` allows `_ORCA_CLIS` only, `cycle` allows nothing outside the package |
| 2 | D 123-166 config / approvers / exit codes (6.1) | matches (D 127-137 table, 141-149 approvers rules, 155-166 codes and precedence 2,6,7,5,3,4) |
| 3 | D 342-358 "15 steps" (6.2) | matches |
| 4 | D 476-490 T-1..T-13 (6.2 steps 10-12) | matches (T-10 window `pending_at - 300 s`, T-11/T-12 `launches` 0) |
| 5 | D 384 k = min(10, floor((35-3)/r)) = 8 (6.7) | matches |
| 6 | D 638-649 timeouts / deadline (6.1, 6.6) | matches (20/10/10/120/240, 5 s floor, launch only if elapsed <= 120) |
| 7 | D 724-745 status fields and slo helper (6.3, 7.4) | matches (8 fields, `slo_numbers(lines, doc: StoreDoc, now)`) |
| 8 | D 693 seed 331 / 2,000 draws (8.3) | matches; the item's "fixed by design line 693, not new proposals" is right (DF-12's bracketed [PROPOSAL] note is the one superseded by R3 minor note) |
| 9 | D 849-866 follow-ups FU-1..FU-12, Q1-Q4 (9.2, 9.M1) | matches |
| 10 | D 49 Coder#477 text, D 60 nine revisit conditions, D 33 deployment gate, D 766/768 (9.1, 9.2) | match |
| 11 | D 868-898 AC-1..AC-25 (9.17, 9.F8) | matches (25 rows) |
| 12 | S 384-395 runbook steps 1-10, S 397-414 follow-ups (9.1, 9.2) | match |
| 13 | S 161, 163-164, 172-173, 187-188, 190-191, 193-194, 196, 213, 229 (6.5-6.9, 7.4-7.5) | match the FR text the items test |
| 14 | `main.py:555-565`, guard at 564 (7.3) | matches the file today (reflect import 559, add_command 561, guard 564) |
| 15 | `reflect/commands.py:53-54`, `:82`, lines 4-5 convention (7.1) | matches (`@click.group("reflect")` at 53, `@reflect_group.command("contract-status")` at 82; lazy-import note at 4-5) |
| 16 | `tests/cli/test_cli_registration.py:24-26`, `:63` (7.4) | matches |
| 17 | `tests/cli/reflect/test_cli_smoke.py:7,17,21,46` (7.4) | matches |
| 18 | `tests/pr_submit/test_conflict_scripts.py:167-179`, `:1555-1571` (8.1) | match (private bin dir, chmod 0o755, env dict; symlinked restricted PATH) |
| 19 | `tests/swarm/test_inv012_tui_opt_in.py:130-143` (8.2) | matches |
| 20 | `tests/swarm/test_parallel_executor_routing.py:343-364`, `:372-406` (8.6, 8.8) | match (AST scan; mutation guards) |
| 21 | `tests/unit/test_ccsession_tag.py:4496-4518` (8.5) | matches (subprocess + `fcntl.flock`) |
| 22 | `swarm/atomic.py:33` `except Exception:` (8.4) | matches |
| 23 | `pyproject.toml:16`, `:114`, `:135`; `tests/conftest.py:14` (6.1, 8.3) | match |
| 24 | `tests/docs/test_retired_docs_absent.py:10-31` (9.1, 9.3) | matches (`_RETIRED` list lines 10-28) |
| 25 | `tests/skills/test_model_alias_policy.py:50` `FULL_ID` (9.1, 9.3) | line matches; its SCOPE does not (Issue 4) |
| 26 | `.pre-commit-config.yaml:74-88` markdownlint (9.1, 9.3) | hook lines match, but the rule set lives in `.markdownlint.json` (Issue 9) |
| 27 | `Makefile:109`, `:166`, `:356-358` (9.9-9.11) | match |
| 28 | `install_user_setup.py:35` `_ORCA_CLIS` (6.3) | matches, but see Issue 3 for how cycle.py may use it |
| 29 | SKILL.md 2221-2229 runner prompt (10.6) | byte-identical (see Check 10) |
| 30 | `main.py:564-565` guard (8.2) | true today, stale once Step 7.3 runs (Issue 5) |
| 31 | "five verdict files `gate-[abcd]-verdict.md`" (9.F1) | the glob matches four files (Issue 6) |

**Check 9 (TB-Add-8 evidence binding).** All file-creating or file-appending authoring items in P6-P10 carry an `<!-- evidence-absence: ... -->` comment with design/spec anchors, and the edit items carry real file:line reads (7.3, 8.x). The 12 gate-run items that name module files as command targets (6.11, 7.9, 8.12, 9.8 and similar) carry neither; they reference files created earlier in the phase, not a code surface to change, so this is a MINOR note only (Issue 12).

### Section 3: Lens check 10 (P10 commit sequence, POST reflect item, ordering)

| Required element (research/06 DF-07, CLAUDE.md, SKILL.md) | Where | Result |
|---|---|---|
| Branch is not master/main, HALT otherwise | 10.2 (and 1.3) | PASS |
| BASE = `git rev-parse HEAD` immediately before the commit, 40-hex check, written to `plans/base-sha.txt` and the Task Log | 10.2 | PASS |
| Explicit-path `git add` of the six prefixes; never `-A`, never `-f`, never `.claude/` | 10.3 (six paths listed exactly as DF-07 item 3) | PASS |
| Allowlist check over `git diff --cached --name-only`, none under `.claude/`, `.dev/issues/`, `.dev/brainstorms/`; G-10 re-run after staging; HALT on failure, no unstage/retry | 10.3 | PASS |
| One commit, exact message with the `Co-Authored-By: Claude Code` trailer, no `--no-verify`, no `--no-gpg-sign`, no `--amend`, no push, no `gh`; HALT on commit or hook failure; `git rev-list --count BASE..HEAD` is 1 | 10.4 | PASS (BASE is a placeholder with no pointer, Issue 10) |
| POST reflect runner prompt verbatim; `--diff <BASE SHA>..HEAD`; no `--executor-model`; frontmatter `reflect_post_mode: skill` with no `start_commit` / `executor_model_class` (checked at lines 31-32 of the task file) | 10.6 | PASS (byte-identical to SKILL.md 2221-2229 apart from resolved placeholders) |
| EV-3 on-disk check: `adversarial/merged-verdict.yaml` with `merge_method: adversarial`, `reviewer-cards/` >= reviewer count (min 2), or the corroborated loud fallback; re-spawn up to 2 more times, then HALT | 10.6 Verification | PASS in substance; the sentence "an illegal `merge_method` value does NOT satisfy the gate" of SKILL.md 2232 is not carried over (Issue 13) |
| Depth equals the TCS-derived depth (`deep`, Tier 2 floor); Task Log "Reflect Depth Derivation" computes TCS 1148 | 10.6 Completion gate, Task Log | PASS |
| POST reflect is the penultimate item of the final phase and the Done item is last | 10.6, 10.7, 10.8 | FAIL: a staging item (10.8) follows the Done item (Issue 1) |
| No push item, no PR item | P10 | PASS |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | Step 10.6/10.7/10.8; Task Overview paragraph 2 (task file line 72: "the POST reflect gate as the penultimate item"); Key Objective 6 (line 83: "and the Done item last, all in P10"); Step 10.7 clause "ensuring this is the only completion item after the POST reflect item" | The task file claims twice that POST reflect is penultimate and Done is last, and SKILL.md 2308-2311 and rule 20 require the POST item to be "the penultimate item of the final phase (immediately before Update-status-to-Done)". The file has three items after POST: 10.7 Done, then 10.8 "NON-BLOCKING: stage the task folder after Done". So the prose is false, Done is not last, and POST is third from the end. DF-07 item (6) asked for the staging item "after Done", but it conflicts with the skill's position rule and with the file's own prose. | Fold 10.8 into 10.7 and delete 10.8. Append to Step 10.7, after the sentence ending "...populate `blocker_reason` with the unmet condition and stop.": " AFTER the status line and the Execution Log entry are written, and as the last action of this item, use the Bash tool to run `git add .dev/tasks` from the repository root (staging only: no second commit, no push, no PR), then `git status --short .dev/tasks` and `git diff --cached --name-only`, ensuring no `.dev/tasks` path shows `??` and no staged path starts with `.claude/`; a failure of this staging command is logged in the ### Phase 10 - Commit and POST Reflect Findings section and never reverts the Done status." Then delete Step 10.8, change the count "176" in the Reflect Depth Derivation paragraph to 175, and change "Step 10.7 ... Done item (Step 10.7)" nothing else. (If the owner insists on DF-07 item 6 as written, instead edit line 72 to "the POST reflect gate immediately before the Done item, followed by one non-blocking staging item" and line 83 to "the Done item, then one non-blocking staging item, all in P10", and add an Open Question that this departs from the skill's penultimate rule.) |
| 2 | IMPORTANT | Steps 7.G12, 8.G12, 9.F13, 9.M8 (clause "(3) otherwise run the next fix cycle by performing, in this same item, the actions of Steps X.G8, X.G9, X.G10 and X.G11 again") | The second fix cycle is defined by back-reference to four earlier items instead of embedding the work. The fix-agent prompt (X.G9) and verifier prompts (X.G10/X.G11) read `qa-consolidated-findings.md`, `qa-fix-report.md` and write `qa-verification-*-report.md`; the cycle-2 file names (`-cycle2`) appear only in the G12 sentence, so an executor reusing the earlier prompts verbatim has them read and overwrite the cycle-1 files, which destroys the evidence the regression and monotonicity guards compare against. This is a "see above" agent-spawning item (checks 2 and 3). The same clause very likely exists in Steps 3.G12 and 5.G12 (other partition). | In each of the four items replace clause (3) by a self-contained clause that carries the cycle-2 prompts: "(3) otherwise run the next fix cycle: write `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/<dir>/qa-consolidated-findings-cycle2.md` (new blocking findings plus still-unfixed ones, same format as the cycle-1 file, with a count line); spawn ONE `rf-qa` subagent with `fix_authorization: true` and the complete fix prompt of this gate with every input path `qa-consolidated-findings.md` replaced by `qa-consolidated-findings-cycle2.md` and the output path replaced by `qa-fix-report-cycle2.md` [write the full prompt text out here]; then spawn the structural verifier (`rf-qa`, report-only) and the content verifier (`rf-qa-qualitative`, report-only) with the complete verification prompts of this gate, inputs `qa-consolidated-findings-cycle2.md` and `qa-fix-report-cycle2.md`, outputs `qa-verification-structural-report-cycle2.md` and `qa-verification-content-report-cycle2.md` [write both full prompts out here]". The full prompt texts must appear in the item (no 'see Step X.G9'). `<dir>` is gate-c, gate-d, final or m4 (m4 uses the `qa-fidelity-*` names). |
| 3 | IMPORTANT | Step 6.3 (`status_report` `retry` clause: "the argv from `launch.retry_argv` using the first name of `_ORCA_CLIS` that `which` resolves", with `src/superclaude/cli/install_user_setup.py:35` in the Read list) versus Step 6.1 and D 241 | Step 6.1 states `cycle.py` may import only runner, github, predicates, record, launch and audit and "nothing else from `superclaude`"; D 241 gives `cycle` no import from elsewhere in `superclaude`, and Step 8.8 makes `test_module_boundaries.py` fail on any other `superclaude.*` import. Step 6.3 tells the author to read `install_user_setup.py:35` and use `_ORCA_CLIS` inside `cycle.py` without saying where the name comes from. An author following the item literally imports it from `install_user_setup`, breaks the import rule, and the failure surfaces only in Phase 8 (Step 8.8) or Gate C. | In Step 6.3 replace "using the first name of `_ORCA_CLIS` that `which` resolves" with "using the first name of `launch._ORCA_CLIS` (the tuple `launch.py` imports from `install_user_setup`; `cycle.py` itself never imports `install_user_setup`) that `which` resolves", and replace "`src/superclaude/cli/install_user_setup.py:35`" in the Read list with "`src/superclaude/cli/install_user_setup.py:35` (background only: `cycle.py` must reach the tuple as `launch._ORCA_CLIS`)". |
| 4 | IMPORTANT | Step 9.5 parenthetical "(... it now includes the new runbook, which the model-alias and retired-docs tests scan)" | False claim. `tests/skills/test_model_alias_policy.py` scans only `src/superclaude/{agents,commands,skills,cli,hooks,core}` (SRC at line 23, `TIER_TEXT_DIRS` at line 48), never `docs/`; only `tests/docs/test_retired_docs_absent.py` walks `docs/**/*.md` (lines 40-41), and it checks Markdown link targets only. G-2 therefore gives no model-alias assurance for `docs/designs/issue-watcher-setup.md`; the only check of that rule on the runbook is the grep in Step 9.3. The false sentence invites the executor and the QA lenses to rely on a gate that does not run. | Replace the parenthetical in Step 9.5 with "(this is the affected subset that replaces a local `make test`, decision DF-05; `tests/docs/test_retired_docs_absent.py` scans the runbook's Markdown links, while `tests/skills/test_model_alias_policy.py` scans only `src/superclaude` and therefore covers the new package, not the runbook, whose model-alias check is the grep of Step 9.3)". |
| 5 | MINOR | Step 8.2 ("`src/superclaude/cli/main.py:564-565` (the `__main__` guard ...)") | Citation is true today but Step 7.3 inserts four lines after line 561, so when Step 8.2 runs the guard sits at about 568-569 and lines 564-565 are the new registration lines. | Say "the `if __name__ == \"__main__\":` guard at the end of `src/superclaude/cli/main.py` (line 564 before Step 7.3, about 568 after it)". Not blocking: moved line number on a true claim. |
| 6 | MINOR | Step 9.F1 ("the five verdict files `phase-outputs/plans/gate-[abcd]-verdict.md`") | The glob matches four files (a, b, c, d); the Final verdict does not exist yet. | Change "five" to "four". |
| 7 | MINOR | Phase 8 intro (task file line 524) | Phases 6 and 9 open with "Before Step N read gate-X-verdict.md; if it does not say PASS, log the blocker and stop"; Phase 8 does not read `gate-c-verdict.md` although research/06 P8 row says "after the Gate C verdict". Step 7.G12 only says "proceed to Phase 8" on PASS, so an interrupted and resumed run has no check. | Append to the Phase 8 intro: "Before Step 8.1 read `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/plans/gate-c-verdict.md`; if it does not say PASS, log the blocker in the ### Phase 8 - Cross-Cutting Tests Findings section and stop." |
| 8 | MINOR | Step 6.1 ("the module constants named exactly in design section 14 but never named `THRESHOLDS` (use `LIMITS`-style names)"); Step 6.3 ("`cwd` from `launch_cwd`") | Design section 14 (D 807-827) lists values with English labels, not Python names, so "named exactly in design section 14" is false; the explicit list that follows (`MAX_CANDIDATES` ...) is the real specification and none is `LIMITS`-style. In 6.3, `launch_cwd` is not identified as the stored entry field (it is an Entry field, S 161, D line for the 17 fields). | Replace the clause in 6.1 by "the module constants listed here, which carry the values of design section 14 (`THRESHOLDS` is a `superclaude.contracts.__all__` name and must not be bound)"; write "the stored entry field `launch_cwd`" in 6.3. |
| 9 | MINOR | Steps 9.1 and 9.3 (`.pre-commit-config.yaml:74-88` "the markdownlint settings") | Lines 74-88 hold the hook and its exclude list. The rules are in `/.markdownlint.json` (`default: true`; MD013, MD029, MD033, MD036 off; MD024 siblings_only). The check lists in 9.1 and 9.3 omit default rules that bite a hand-written runbook (MD022, MD031, MD032 blank lines around headings, fences and lists; MD012 repeated blank lines; MD041 first line a heading; MD047 trailing newline is covered). | Add `.markdownlint.json` to the Read lists and add "blank lines around headings, fenced blocks and lists, no two consecutive blank lines, first line a top-level heading" to the rows of Step 9.3. |
| 10 | MINOR | Step 6.7 ("research/05 lines 347-351 for the X1 cases"), Step 9.17 ("re-running Step 9.4"), Step 10.4 (`<BASE SHA>`) | research/06 line 11 and 171 forbid citing research 05 `X1`..`X15` ids in task items (cite the DF id); 9.17 and 10.4 point to another item or placeholder instead of restating the command or source. | 6.7: "decision DF-50 (including the two X1 test cases of its row)"; 9.17: "re-running `uv run pytest tests/issue_watch/ -v` (Step 9.4)"; 10.4: "read BASE from `phase-outputs/plans/base-sha.txt`". |
| 11 | MINOR | Steps 6.2 and 6.7 | Each is a single paragraph of well over 1,500 words: 6.2 packs the 15-step `run_cycle` with about 40 named reason and exit rules; 6.7 packs about 15 scenario families into one test part. The phase intro justifies splitting `cycle.py` into three items but not these two sizes. An executor that rolls sessions mid-item loses the half-written function. | Optional: split 6.2 into "steps 1-9" and "steps 10-15" items and 6.7 into "skip reasons and claimed paths", "launch order, S1, FR-023" and "dry-run" items, each repeating the Read list it needs. Not blocking: the file is consistently built this way and each item is one deliverable. |
| 12 | MINOR | Gate-run items 6.11, 7.9, 8.12, 9.8 | Name module files without a file:line or `<!-- evidence-absence -->` comment (TB-Add-8). They target files created earlier in the same phase. | Optional: add `<!-- evidence-absence: gate run over files created in this phase; no source line cited -->`. |
| 13 | MINOR | Step 10.6 Verification | The POST item omits the SKILL.md 2232 sentence that an illegal `merge_method` (anything other than `adversarial` or `single-reviewer-fallback`) does not satisfy the gate, and no item records `git status --short` after the POST run; if the reflect remediation edits deliverable files after the checkpoint commit, nothing re-runs G-1 or reports them. | Append to the Verification: "an illegal `merge_method` value (anything other than `adversarial` or `single-reviewer-fallback`) does NOT satisfy this item; then run `git status --short` and write every path outside `.dev/tasks` that changed since the checkpoint commit to the ### Phase 10 - Commit and POST Reflect Findings section (if any, re-run `uv run pytest tests/issue_watch/ -v` and the pinned ruff on them and leave them unstaged for the owner; make no second commit)". |
| 14 | MINOR | Out of partition (Execution Context References, task file lines 108-110) | Note for the P1-P5 agent: the TB-Add-7 consumer spot check `grep -cE "src/|/.*:[0-9]+"` over the Execution Context block returns a non-zero count because the verbatim GOAL text names `src/superclaude/cli/issue_watch/` and `src/superclaude/cli/main.py`. | None needed if the check is judged inapplicable to the verbatim GOAL quote. |

## Summary

- Lens checks passed: 6 / 10 (checks 1, 4, 5, 6, 7 and 9, each with minor notes).
- Checks failed: 4 (check 2 and 3: Issue 2; check 8: Issues 3 and 4, a contradictory import instruction and a false statement about what a gate scans; check 10: Issue 1).
- Issues: CRITICAL 0, IMPORTANT 4 (Issues 1-4), MINOR 10 (Issues 5-14)
- Fixes applied: 0 (fix_authorization: false)

## Confidence and tool engagement

- **Confidence:** Verified: 10/10 lens checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (31 citations independently re-read, see Check 8 table; the other-partition P1-P5 items were not reviewed).
- **Tool engagement:** Read: about 40 | Grep: about 18 | Glob: 5 | Bash: 8. No web research was needed (no tavily or fallback calls).
- Not verified: the live behaviour of the `rf-qa`/`rf-qa-qualitative` agents, `sc-reflect-protocol` and the `orca` flow described in the items; the Gate A and Gate B fix-cycle items (other partition).

## Recommendations

- Resolve Issues 1-4 before executing the task. Issues 1 and 2 change item structure (fold 10.8 into 10.7; embed the cycle-2 prompts), so apply them to all four fix-cycle items plus the Gate A and Gate B equivalents found by the P1-P5 agent.
- Minor Issues 5-14 are notes and are not rechecked.

VERDICT: FAIL

## QA Complete


# Inventory — review severity rule and review-loop caps

**Date**: 2026-10-31 · **Branch**: `fix/review-severity-rule` (base `f90877be`, after #337 and #338) · **Orca task**: task_ffd69d882cdd
**User decision (2026-10-31, verbatim)**: "Any severity fail rule: after review fails on minor, note them and proceed, do not recheck do not fail. Remove any severity rule. Limit review loops to 2."
**Restart update (2026-11-01, Orca task task_2f56bc9b8728)**: the earlier worker stopped on API errors before any commit. Every pending decision is now final (section 4): B1 minors never fail and are not rechecked; B2 the cap is 2 fix cycles (3 reviews), "Max 3" and uncapped loops drop to 2; B3 `/sc:implement` option A (remove the second A2 repair). The pre-review report `.dev/reflect/pre-removeTheAnyIssu-20261031235716/REPORT.md` findings C1-C4 are folded in (section 2.2 rows for `rf-analyst.md:74`, `task-builder/SKILL.md:895`, `synthetic-dnsp-finding.contract:52`; S5 placed in `pragmatic.md`). The superseded package `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404/` stays on disk unexecuted. Line numbers re-verified on 2026-11-01 against `f90877be` (unchanged).
**Evidence base**: `.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md` §4 (cause 1: a pass rule that let minor findings fail a review; cause 3: round supply with no cap outside the commands) and §5 recommendation 1 ("bundle A").

Categories:

- **(a)** fails a review on a minor, low or cosmetic finding;
- **(b)** re-checks minor findings in later rounds or sends them to a fix pass;
- **(c)** allows more than 2 review rounds, or has no cap, or passes open blocking findings at the cap instead of escalating.

Line numbers are against `f90877be`. Twins: of the files below only `sc-implement-protocol` and `sc-workflow-protocol` have tracked twins under `plugins/superclaude/skills/`; root `commands/` and `agents/` hold no twin of any listed file (`git grep` over `plugins commands agents` for the wordings below returns only `commands/sc-pm.md:345`, which is about investigating warnings, not review verdicts, and stays).

## 1. Canonical rule text

Holder: `src/superclaude/output-styles/pragmatic.md`, replacing line 225 (the "Any issue of ANY severity ... MUST result in a FAIL verdict ... a 'minor issues still pass' allowance is PROHIBITED" bullet). Lines 221 (adversarial stance), 222 (zero-finding Self-Audit) and 224 (binary PASS/FAIL) stay unchanged. The five bullets S1-S5 below all go into `pragmatic.md`, in this order, so the style file is the single source of every sentence. Every other edited QA agent, template and rule prompt carries S1-S3 word for word (whitespace and indentation may differ); files with a CRITICAL / IMPORTANT / MINOR scale also carry S5.

```text
- Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.   (S1)
- Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.   (S2)
- A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.   (S3; contains the canonical cap text "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings")
- A protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`), applies that model and its own escalation path.   (S4)
- On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor.   (S5)
```

Round count (decided 2026-10-31 by the user, via the coordinator, option B): a round is one fix cycle; the cap is 2 fix cycles, so at most 3 reviews.

## 2. Category (a) and (b): severity rules

All paths below are under `src/superclaude/` unless they start with `tests/`. "Canonical block" = S1-S3 and S5 of section 1 inserted once in the file.

### 2.1 Output style

| file:line | cat | current | replacement |
|---|---|---|---|
| `output-styles/pragmatic.md:225` | a | "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict, except inside a protocol that defines its own severity model ...; a 'minor issues still pass' allowance is PROHIBITED." | S1-S5 (five bullets, so later readers take every canonical sentence, S5 included, from `pragmatic.md`). The SubagentStart hook (`hooks/scripts/pragmatic-subagent.js`) reads the installed file, so it carries the new text with no code change. |

### 2.2 QA agents

| file:line | cat | current | replacement |
|---|---|---|---|
| `agents/rf-qa.md:82` | a | DNSP finding "treated as a real finding for the existing "any gap regardless of severity = FAIL" gating rule" | "treated as a real blocking finding (severity HIGH) under the review severity rule" |
| `agents/rf-qa.md:84` | a | "Treat it as a real finding for the purpose of "any gap regardless of severity = FAIL"." | "Treat it as a blocking finding: it fails the gate." |
| `agents/rf-qa.md:91` | a | "Zero tolerance: The work must be correct to pass — no partial credit" | "Zero tolerance for blocking defects: any blocking finding fails the gate, with no partial credit; minor findings are recorded as notes and do not fail it (Review severity rule below)" + new "## Review severity rule" section holding the canonical block after the principles |
| `agents/rf-qa.md:98` | a | NO LENIENCY "... 'close enough' or 'probably fine' — it FAILS" | keep, append "Grade what you find by the review severity rule: an unverified or 'probably fine' claim is blocking; a cosmetic or wording finding is minor." |
| `agents/rf-qa.md:158-159` | a | "MINOR (still must be fixed)"; "ALL gaps regardless of severity = overall FAIL" | "MINOR (recorded as a note; does not fail the gate)"; "Any CRITICAL or IMPORTANT gap = overall FAIL (must be resolved before synthesis); MINOR gaps alone = PASS (with notes)" |
| `agents/rf-qa.md:171-172` | a | PASS "no gaps of any severity"; FAIL "Any gaps exist (CRITICAL, IMPORTANT, or MINOR) ... no severity level is exempt" | PASS "No CRITICAL or IMPORTANT gaps; any MINOR gaps are listed as notes. Green light for synthesis."; FAIL "Any CRITICAL or IMPORTANT gap exists. List each with a specific remediation action. All blocking gaps must be resolved before proceeding; MINOR gaps never fail the gate." |
| `agents/rf-qa.md:370-391` (Fix Cycle phase) | b | re-verifies "previously-failed items" (all severities) | re-verify previously failed blocking items only; minor findings are not rechecked |
| `agents/rf-qa.md:464` | a | "If FAIL: 'Must resolve ALL [N] issues before proceeding.'" | "If FAIL: 'Must resolve ALL [N] blocking (CRITICAL/IMPORTANT) issues before proceeding; MINOR issues are notes.'" |
| `agents/rf-qa.md:537` | a | "ALL findings regardless of severity must be resolved." | "All blocking findings must be resolved; minor findings are recorded as notes." (cap number: section 3) |
| `agents/rf-qa-qualitative.md:83` | a | DNSP "any gap regardless of severity = FAIL" reference (same text as rf-qa:82) | same replacement as rf-qa:82 |
| `agents/rf-qa-qualitative.md:97` | a | NO LENIENCY "it FAILS." | same addition as rf-qa:98 |
| `agents/rf-qa-qualitative.md:228-229, 279-280, 350-351, 417-418, 488-489, 555-556, 734-735, 772-773` | a | 8 × PASS "no issues of any severity"; FAIL "Any issues exist (CRITICAL, IMPORTANT, or MINOR) ... ALL issues must be resolved ..." | PASS "No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes."; FAIL "Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review." + canonical block once, after the principles |
| `agents/rf-qa-qualitative.md:777-797` | a, b | "ALL findings regardless of severity must be resolved." | as rf-qa:537; re-verify blocking items only |
| `agents/rf-qa-qualitative.md:982` | a | "ALL findings regardless of severity must be resolved." | as rf-qa:537 |
| `agents/rf-analyst.md:74` | a | DNSP API-003-M6 clause: "treated as a real finding for the existing "any gap regardless of severity = FAIL" gating rule" (pre-review C1) | "treated as a real blocking finding (severity HIGH) under the review severity rule" |
| `skills/task-builder/SKILL.md:895` | a | same clause: "treats it as a real finding for the existing "any gap regardless of severity = FAIL" gating rule" (pre-review C2) | same replacement |
| `templates/modularization-template-review/synthetic-dnsp-finding.contract:52` | a | "treats the synthetic-dnsp record as a real finding for the existing "any gap regardless of severity = FAIL" gating rule" (pre-review C3) | "treats the synthetic-dnsp record as a real blocking finding (severity HIGH) under the review severity rule" |
| `agents/rf-analyst.md:93` | a | "rf-qa's existing "any gap regardless of severity = FAIL" rule means it fails the gate by default" | "a synthetic-dnsp finding is HIGH, so it is blocking and fails the gate by default" |
| `agents/rf-analyst.md:148, 199` | a, b | "Minor (lower priority but must still be fixed)"; heading "### Minor Gaps (must still be fixed)" | "Minor (recorded as a note; does not block synthesis)"; "### Minor Gaps (notes; do not block synthesis)" |

### 2.3 Templates

| file:line | cat | current | replacement |
|---|---|---|---|
| `templates/documents/agent_template_qa.md:95-96, 100` | a | principle lists name "Zero tolerance" and NO LENIENCY "it FAILS" | same wording as rf-qa:91 and :98 |
| `templates/documents/agent_template_qa.md:139` | — | MINOR definition guidance | keep; add S5 under it |
| `templates/documents/agent_template_qa.md:156-157` | a | PASS "no issues of any severity"; FAIL "Any issues exist (CRITICAL, IMPORTANT, or MINOR) ... no severity level is exempt" | as rf-qa-qualitative verdicts + canonical block |
| `templates/documents/agent_template_qa.md:262` | a | "Must resolve ALL [N] issues" | as rf-qa:464 |
| `templates/documents/agent_template_qa.md:335` | a | "ALL findings regardless of severity must be resolved." | as rf-qa:537 |
| `templates/workflow/01_mdtm_template_generic_task.md:643` | a | "Any issue of any severity (CRITICAL, IMPORTANT, or MINOR) results in FAIL." | canonical block S1-S3 + S5 (indented) |
| `templates/workflow/01_mdtm_template_generic_task.md:655` | b | "Each fix cycle MUST re-verify ALL previously failed items plus check for new issues" | "Each fix cycle MUST re-verify every previously failed blocking item plus check for new blocking issues introduced by fixes; minor findings are not rechecked." |
| `templates/workflow/02_mdtm_template_complex_task.md:654` | a | same as 01:643 | same |
| `templates/workflow/02_mdtm_template_complex_task.md:656` | a | "The consolidated verdict is FAIL if ANY individual agent's report contains ANY issue of any severity." | "The consolidated verdict is FAIL if any individual agent's report contains a blocking issue; minor issues from every agent are carried into the consolidated file as notes." |
| `templates/workflow/02_mdtm_template_complex_task.md:671` | b | same as 01:655 | same |
| `templates/modularization-template-review/analyst-completeness_report_template.md:75, 159` | a, b | "Minor Gaps (must still be fixed)" | "Minor Gaps (notes; do not block synthesis)" |
| `templates/documents/skill_template.md:815, 824` | a | shared prompt block: "Minor are lower priority but must still be fixed"; "FAIL: ALL findings must be resolved." | "Critical and Important gaps are blocking and fail the gate; Minor gaps are recorded as notes and do not fail it"; "FAIL: any blocking (Critical or Important) finding; every blocking finding must be resolved. Minor findings are notes: they never fail the gate and are not rechecked." |

### 2.4 Skills (shared RF prompt blocks and gate prose)

Same two replacements as `skill_template.md:815, 824` wherever the shared prompt block appears:

| file:line | cat |
|---|---|
| `skills/prd/refs/agent-prompts.md:273, 283` | a |
| `skills/tdd/refs/agent-prompts.md:282, 291` | a |
| `skills/tech-reference/SKILL.md:878, 886` | a |
| `skills/tech-research/SKILL.md:886, 894` | a |
| `skills/operational-guide/SKILL.md:982, 990` | a |
| `skills/readme/SKILL.md:1007, 1029, 1038` | a |

Gate prose:

| file:line | cat | current | replacement |
|---|---|---|---|
| `skills/tech-reference/SKILL.md:536` | a | "If any unresolved issues remain at any severity (CRITICAL, IMPORTANT, MINOR), address ALL of them ... Zero leniency — no severity level is exempt." | "If any blocking (CRITICAL or IMPORTANT) issue remains unresolved, address it before proceeding to Phase 7; MINOR issues are recorded as notes and do not block." |
| `skills/tech-research/SKILL.md:567` | a | "Zero leniency — no severity level is exempt. ALL findings must be resolved before Phase 7." | "Every blocking finding must be resolved before Phase 7; minor findings are recorded as notes and do not block." |
| `skills/tech-research/SKILL.md:1150` | a | "Verdict: PASS (0 critical + 0 important + 0 minor) / FAIL" | "Verdict: PASS (0 critical + 0 important; minor findings listed as notes) / FAIL" |
| `skills/task-builder/SKILL.md:865` | a | "Gate PASSES when ALL verdicts are PASS with ALL findings resolved regardless of severity." | "Gate PASSES when ALL verdicts are PASS with every blocking finding resolved; minor findings are carried as notes." |
| `skills/task-builder/SKILL.md:870` | b | "Compile all CRITICAL, IMPORTANT, and MINOR issues ... into a structured gap list" (gap-fill input) | "Compile all CRITICAL and IMPORTANT issues ... into a structured gap list (MINOR issues stay as notes and are not sent to gap-fill)" |
| `skills/task-builder/SKILL.md:1600` | a | "If any issues found (CRITICAL, IMPORTANT, or MINOR) ... If issues remain unfixed, address ALL of them" | "If any blocking (CRITICAL or IMPORTANT) issue was found ... If a blocking issue remains unfixed, address it; MINOR issues are recorded as notes" |
| `skills/task/SKILL.md:347` | a | same shape as task-builder:1600 | same |
| `skills/prd/refs/build-request-template.md:129, 157` | a | "fix ALL findings regardless of severity"; "If any issues found (CRITICAL, IMPORTANT, or MINOR) ... address ALL" | "fix every blocking finding (minor findings are recorded as notes)"; as task-builder:1600 |
| `skills/tdd/refs/build-request-template.md:124, 152` | a | same as prd | same |
| `skills/readme/SKILL.md:549, 609` | a | "fix ALL findings regardless of severity"; "If any issues remain unresolved, address ALL ... Zero leniency." | "fix every blocking finding (minor findings are recorded as notes)"; "If any blocking issue remains unresolved, address it before Phase 7; minor issues are recorded as notes." |
| `skills/operational-guide/SKILL.md:514` | a | "If FAIL → fix ALL findings regardless of severity." | "If FAIL → fix every blocking finding (minor findings are recorded as notes)." |

### 2.5 Installed legacy rule prompts (`rules/prompts/`, installed to `~/.claude/rules/prompts/`, never auto-loaded)

| file:line | cat | current | replacement |
|---|---|---|---|
| `rules/prompts/automated_qa_workflow_qa_prompt.md:10` | a | "Zero tolerance: The batch must be perfect to pass" | "Zero tolerance for blocking defects: any blocking finding fails the batch; minor findings are recorded as notes" + canonical block S1-S3 once |
| `rules/prompts/doc_code_analyst_qa_prompt.md:26` | a | same | same |
| `rules/prompts/documentation_expert_qa_prompt.md:27` | a | same | same |
| `rules/prompts/documentation_expert_qa_prompt.md:307-308` | a | "Unclear or confusing writing = FAIL"; "Poor grammar/spelling/formatting = FAIL" | "Unclear or confusing writing = minor (note) unless it makes a required instruction wrong or unusable"; "Poor grammar/spelling/formatting = minor (note)" |
| `rules/prompts/recruiting_expert_qa_prompt.md:26` | a | same as :10 | same |

## 3. Category (c): caps and at-cap behaviour

### 3.1 At-cap behaviour that passes open blocking findings (apply now; independent of the cap number)

Replacement everywhere: "HALT and escalate to the user with the open blocking findings; minor findings stay as notes."

| file:line | current |
|---|---|
| `templates/workflow/01_mdtm_template_generic_task.md:650, 652` | I16 rows synthesis-gate and task-integrity: "Unresolved issues become Open Questions" |
| `templates/workflow/01_mdtm_template_generic_task.md:803` | lite: "If issues remain after 1 fix cycle, log as Open Questions and proceed." |
| `templates/workflow/02_mdtm_template_complex_task.md:663, 665` | same as 01:650, 652 |
| `templates/workflow/02_mdtm_template_complex_task.md:820` | same as 01:803 |
| `agents/rf-task-builder.md:384, 386` | builder copy of the I16 table: "Open Questions" |
| `skills/task-builder/SKILL.md:873` | "After 3 rounds, proceed with remaining gaps as Open Questions in the task file" |
| `skills/task-builder/SKILL.md:1259` | "After max rounds, proceed with gaps as Open Questions in the task file" |

### 3.2 Cap numbers above the cap (DECIDED: CAP = 2 fix cycles, 3 reviews)

Canonical cap text, reused everywhere a cap is stated in prose: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings".

Replacement: every "Max N fix cycles" / "max N cycles" / "N max per gate" / "[1 / 2 / 3 / N/A]" / "/ 3" / "N-fix-cycle" / "N-cycle" / "max-N-cycles" with N = 3 becomes 2 (`[1 / 2 / N/A]`, `/ 2`, `2-fix-cycle`, `2-cycle`, `max-2-cycles`), and every "After 3 cycles, HALT ..." becomes "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings". Lines whose N is already 2 or 1 stay. Line numbers below are from the earlier scan; locate each by its quoted text, and the new static test scans for any remaining fix-cycle cap of 3 or more.

`rf-team-lead.md:462` changes to "max 2 cycles per phase", so its sha256 changes: update the fixture `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`, the token and sha pins in `tests/audit/test_dnsp_all_agents_fail_bypass.py`, and the "sha256 frozen at `51725c0f…`" mentions plus "max-3-cycles" tokens in `agents/rf-qa.md:82`, `agents/rf-qa-qualitative.md:83`, `agents/rf-analyst.md:74` and `skills/task-builder/SKILL.md:901` (one value, the sha256 of the new line).

Additional 3-cycle sites found on 2026-11-01 (same replacement): `skills/operational-guide/SKILL.md:514, 571`; `skills/readme/SKILL.md:188, 602, 607`; `skills/tech-reference/SKILL.md:415`; `skills/tech-research/SKILL.md:486, 551`; `skills/task-builder/SKILL.md:1275, 1310, 1420, 1471`; `templates/workflow/02_mdtm_template_complex_task.md:1119`; `templates/modularization-template-review/qa-fix-summary_template.md:105`; `agents/rf-qa.md:393, 395, 403, 406`.

| file | lines (N in brackets) |
|---|---|
| `agents/rf-qa.md` | 82 (3, "max-3-cycles" inside the DNSP clause), 390 (3), 393, 395, 403, 406 ("3-fix-cycle" / "3-cycle" names), 418 ([1/2/3]), 537 (3) |
| `agents/rf-qa-qualitative.md` | 83 (3), 797 (3), 827 ([1/2/3]), 982 (3) |
| `agents/rf-analyst.md` | 74 (3, "max-3-cycles") |
| `agents/rf-team-lead.md` | 462 (3, "max 3 cycles per phase"; this line's sha256 `51725c0f…` is pinned by `tests/audit/test_dnsp_all_agents_fail_bypass.py` and the fixture `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`) |
| `agents/rf-task-builder.md` | 381-387 table (3, 2, 3, 2, 3) |
| `templates/documents/agent_template_qa.md` | 184 (3), 210 ([1/2/3]), 320 (3), 335 (3) |
| `templates/documents/skill_template.md` | 427 (3), 428 (2) |
| `templates/workflow/01_mdtm_template_generic_task.md` | 647-653 I16 table (3, 2, 3, 2, 3), 785-787 I22 table (2, "2-3"), 812 (2), 938 |
| `templates/workflow/02_mdtm_template_complex_task.md` | 660-667 I16 table (3, 2, 3, 2, 3, 3), 753 (3), 802-804 I22 table (2, "2-3"), 829 (2), 1043, 1090 (3), 1119 (3) |
| `templates/modularization-template-review/*` | `qa-consolidated-findings_template.md:102`, `qa-cross-source-contradictions_template.md:101`, `qa-fix-summary_template.md:96, 105`, `qa-research-depth_report_template.md:105`, `qa-research-evidence_report_template.md:100`, `qa-research-gap_report_template.md:103`, `qa-source-fidelity_template.md:95`, `qa-task-validation-b2_report_template.md:101`, `qa-task-validation-structure_report_template.md:104` (all "/ 3") |
| `skills/prd/refs/build-request-template.md` | 130 (3), 149 (2) |
| `skills/tdd/refs/build-request-template.md` | 125 (3), 144 (2) |
| `skills/operational-guide/SKILL.md` | 427 (3), 429 (2), 438, 442, 443, 446, 450, 451 (2), 439, 447 (3), 514 (3), 538 (2), 571 (3), 583 (2), 681 (2) |
| `skills/readme/SKILL.md` | 188 (3), 190 (2), 191 (3), 450, 455, 456, 459, 463 (2), 451, 460, 464 (3), 546, 553 (3), 579 (2), 602, 607, 608 (3), 697 (2), 1690, 1715 (3) |
| `skills/roadmap/SKILL.md` | 434, 439, 447, 448 (2), 435, 440 (3), 554, 563, 577 (3), 589, 668 (2), 2073 (3, 2, 3, 2, 2) |
| `skills/task/SKILL.md` | 254 (3), 336 (3), 366, 368 (3), 405 (3), 477 ([1/2/3]) |
| `skills/task-builder/SKILL.md` | 204 (3), 872-873 (3 gap-fill rounds), 1275, 1310 (3-cycle backstop, per-gate caps 3/2/3/2/3), 1420 (3), 1471 (A.10 3-cycle) |
| `skills/tech-reference/SKILL.md` | 177, 412, 415 (3), 423, 427, 431, 435 (2), 428, 432, 436 (3), 512, 529, 534, 535 (3), 613 (2), 1307 (3), 1354 (">2"), 1388 (2) |
| `skills/tech-research/SKILL.md` | 397, 401, 402, 405, 409, 410, 413, 414 (2), 398, 406 (3), 486 (3), 515 (2), 551 (3), 557, 558, 564 (2), 646 (2) |
| `skills/sc-cli-portify-protocol/SKILL.md` | 355, 363-364, 366, 373 (convergence loop: each iteration reviews, incorporates fixes and scores; `max_iterations = 3` allows 3 fix passes, so it drops to 2: "2 iterations exhausted", `iteration < 2`, `iteration >= 2`, `max_iterations = 2`); `decisions.yaml:121, 123` ("Max 3 iterations", "3 iterations exhausted" → 2). Its ESCALATED state already escalates to the user with the open CRITICAL findings. |

Kept (already within the cap):

- `skills/sc-roadmap-protocol/SKILL.md:313` and `refs/validation.md:365`: REVISE loop "Max 2 iterations" after the first validation = 2 fix cycles, 3 validations. Stays. Its at-cap outcome `PASS_WITH_WARNINGS` is a score band (70-84 %), not a set of open blocking findings, and it is reported, not silent.
- `commands/pr-submit.md:47`, `skills/sc-pr-submit-protocol/refs/loop-guard.md:18`, the FSM in `cli/pr_submit/` and `tests/pr_submit/test_loop_guard.py`: `--max-rounds` default 2 remediation cycles = 3 reviews, which equals the cap, and it halts (`HALT_MAX_ROUNDS`) at the cap. The hard cap 5 applies only when the user passes a higher `--max-rounds` explicitly, which is the user's own decision. Minors there are already report-only. No change.

Excluded from the cap change (not review loops): the confidence-raising loop inside one review ("After 3 rounds still below 95%", `rf-qa.md:499`, `rf-qa-qualitative.md:941`, `agent_template_qa.md:293`); research and builder retries (`rf-team-lead.md:196` gap-fill researchers max 2, `task-builder/SKILL.md:2355` RESEARCH_NEEDED / MALFORMED max 2); track and agent counts; `sc-adversarial-protocol` debate rounds (a debate, not a review-fix loop).

## 4. Decisions (final, from the user via the coordinator; nothing pending)

1. **What counts as a round: B.** A round is one fix cycle; the cap is 2 fix cycles = at most 3 reviews (review, fix, re-review, fix, re-review), then escalate the open blocking findings to the user. Section 3.2 applies with CAP = 2.
2. **`/sc:implement` ladder: option A.** Remove the second A2 in-place repair, so A1 review, Q5 fix pass, A2 re-review, one A2 repair, re-review = 2 fix cycles. Keep the adviser attempts A3-A5, the halt contract (`halt review=5 reason=ladder-end`), the saved reviewer prompt (`refs/qa.md` Subagent prompt block) and the FINAL contract unchanged. Edits (re-read `refs/retry.md` and `refs/qa.md` before editing):
   - `refs/retry.md` Repair round item 5 (valid names: j is always 1), item 6 (A2 timing: one A2 repair; drop the second-repair sentence), item 12 (resume: for n = 2 a passing or failed re-review goes on as an uninterrupted run with no second-repair branch), item 1 and item 11 wording that mentions further A2 repairs; Cost and caps line 189 ("Worst case: 9 reviews ...", recomputed from the edited rules) and line 193 (drop "except the second A2 repair").
   - `refs/qa.md:267` Interruption/audit row "A2 with repairs 1 and 2" → "A2 with its repair".
   - `refs/ledger.md:143` ("both repairs are unspent" → "the repair is unspent") and Resume rows S (`repair-2-<j>.md` → `repair-2-1.md`) and V.
   - The plugin twins `plugins/superclaude/skills/sc-implement-protocol/refs/{retry,qa,ledger}.md` copied byte for byte in the same commit.
   - Tests: `tests/skills/test_implement_severity_static.py:278` (qa.md row pin), `tests/skills/test_implement_severity_replay.py` (`route()` second-A2 branch, `test_r_a3_late_blockers_local_second_a2_repair`, the replay at lines 244-251 that expects 2 A2 repairs), `tests/skills/test_task_workspace_lifecycle.py:582` (worst-case line pin), plus any test found by `git grep -n -E 'second A2|repair-2-2|repairs 1 and 2' -- tests`.
3. **P1: `update.sh` is not changed.**
4. **Previously listed as decision 2, for the record:** Today a task can get up to 9 reviews (`skills/sc-implement-protocol/refs/retry.md:189`): A1 review, Q5 fix pass, A2 re-review, up to 2 in-place repairs in attempt 2 each with a re-review (`refs/retry.md:141-142`), then adviser attempts A3-A5, each from the Q0 snapshot with its own review and at most one repair re-review, then `halt review=5 reason=ladder-end`. Minors already never fail (`refs/qa.md:129`, `refs/retry.md:146`). Option A was chosen (item 2 above). The saved reviewer template (`refs/qa.md:320-351`) and the FINAL contract are not touched by A or B. The plugin twins `plugins/superclaude/skills/sc-implement-protocol/refs/*.md` must change in the same commit as the source.
5. **`/sc:workflow`.** Its plan check is one advisory, read-only pass (`skills/sc-workflow-protocol/SKILL.md:58,60`), so it already meets the cap; no change.

## 5. Kept as is (checked, not a minor-fails rule)

- "Zero tolerance — if you can't verify it, it fails." (`skills/*/SKILL.md`, `skills/*/refs/agent-prompts.md`, `templates/documents/skill_template.md:828`, `cli/prd/prompts.py:1175`): an unverified claim is a blocking finding (false or unsupported claim), so this matches the new rule.
- "Zero tolerance for fabrication" (`agents/rf-analyst.md:418`, `agents/rf-qa.md:532`, `templates/documents/agent_template_analysis.md`) and the anti-hallucination "Zero Tolerance" rules in `rules/core/*`: fabrication is a false claim, blocking.
- "Incremental writing is mandatory — ZERO TOLERANCE" (`skills/roadmap`, `skills/task`, `skills/tech-research`, `templates/workflow/03_component_authoring_template.md:79`): a process rule, not a review verdict.
- `commands/sc-pm.md:345` "Zero Tolerance for Dismissal" of warnings: about investigating warnings, not about review verdicts.
- `rules/prompts/*_qa_prompt.md` "EXACT means EXACT" (character-exact checks of items the task spec marks `EXACT:`): a mismatch is a missing required deliverable, blocking.
- `skills/roadmap/SKILL.md:2018, 2278` (PASS with DEGRADED-minor / minor losses) and `sc-implement-protocol/refs/qa.md` severity model: already non-failing for minors.
- "Fix every issue you find. Report honestly." (`templates/documents/skill_template.md:943, 950`, `skills/prd/refs/agent-prompts.md:386`, `skills/tdd/refs/agent-prompts.md:392`): instruction to a fix agent already authorized to edit; it does not fail a review or recheck minors.
- `skills/sc-pr-submit-protocol`: fixes only Medium or higher findings; Low and Nit are report-only (its round count is in 3.2).

## 6. Tests that pin the old wording

| test | pins | change |
|---|---|---|
| `tests/skills/test_implement_severity_static.py:485-493` (`test_p1_output_style_exempts_implement_severity_model`, #338 pin P1) | the old `pragmatic.md:225` bullet text | pin the new S2 and S4 text instead (keep the test, change the expected text) |
| `tests/audit/test_nfr_conv_9_zero_trust.py:78-85, 94-105, 225-249` | rf-qa PASS / FAIL bullets byte-equal; the 1-MINOR-gap fixture must score FAIL ("rf-qa.md:145 mandates FAIL for any severity") | pin the new bullets; the 1-MINOR fixture must score PASS (with notes); add a 1-IMPORTANT case that scores FAIL |
| `tests/audit/fixtures/nfr_conv_9/one_low_finding.md`, `zero_findings_baseline.md:9, 35` | fixture prose quoting the old rule | update prose to the new rule |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py:14, 32, 77, 395-399, 640` and `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` | `rf-team-lead.md:462` "max 3 cycles per phase", its sha256 and the "max-3-cycles" token | pin "max 2 cycles per phase", the new sha256 and "max-2-cycles" |
| `tests/skills/test_task_builder_merge.py:435` | comment naming rf-qa's "3-fix-cycle" | update the comment and any assertion on the cap text |
| `tests/skills/test_implement_severity_static.py:278`, `tests/skills/test_implement_severity_replay.py:130-251`, `tests/skills/test_task_workspace_lifecycle.py:582` | the second A2 repair and the worst-case line | option A (section 4 item 2) |
| `tests/pr_submit/test_loop_guard.py` | `--max-rounds` default 2 | no change (already at the cap) |

New test: `tests/skills/test_review_severity_rule.py` (no "any severity ... FAIL" wording in `src/`, `plugins/`, `commands/`, `agents/`; S1-S5 present in `pragmatic.md`, S1-S3 in every edited QA agent, template and rule prompt and S5 in each file with a CRITICAL / IMPORTANT / MINOR scale; the canonical cap text present in `pragmatic.md` (S3) and no fix-cycle cap of 3 or more in the section 3.2 files; no "become Open Questions" at-cap rule; src and plugin twins byte-equal for every edited file that has a twin).

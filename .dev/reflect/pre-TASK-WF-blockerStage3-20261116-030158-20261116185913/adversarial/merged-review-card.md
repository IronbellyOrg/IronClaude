# Merged review card, stage 3 plan, third review (revision 3 of the plan)

<!-- Merged review card. Base variant: variant-2-original.md (reviewer-2, qa persona, opus class). Merge date: 2026-11-16. Non-base sources incorporated: variant-1-original.md (reviewer-1, haiku class), invariant-probe.md (fault-finder) and the debate rounds. -->
<!-- Aliases: PLAN = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md; SRC = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md; S0 = .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md; S4 = .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md; SPEC = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md; README = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md; PRIOR = .dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116174401/REPORT.md. All other paths are repo-relative. -->

## Verdict

NEEDS-REVISION: 3 blocking findings (F1 to F3) and 12 non-blocking (F4 to F15; F4 to F8 are Medium and listed as follow-up candidates, F9 to F15 are minor). The revision fixed all three blocking findings of the earlier review in text (gate order, recall variants and threshold, QA rules 8 and 9) and the 13 non-blocking ones, but it introduced or left three defects that gate the rule switch: the outcome words of the seeded-recall lines give R1b no word in the expected small-set case (F1), the found threshold scores the two arms with different panel sizes (F2), and the "no rule file is switched on a failed gate" guarantee does not hold under `/sc:implement`'s fix pass and retry ladder (F3). Debate: 19 of 20 diff points agreed after Round 2 (95 percent); the one open point (C-007, the fix-pass route) was graded blocking on the invariant probe's evidence (INV-001, HIGH, unaddressed), against both advocates' non-blocking grade at 55 percent confidence given before they read qa.md:245 and retry.md:109 and :158 together with Task 6's acceptance lines; the two advocates also moved V2's F2 and F3 from blocking to non-blocking.

## Earlier findings

- Earlier F1 (seeded-recall gate ran after the `pragmatic.md` edit): fixed in order. Task 4 is a read-only gate that edits nothing under src, tests or plugins (PLAN:113); Task 6 re-checks the result file, the hash and the ledger row before its first edit (PLAN:140); the old arm is frozen as a copy (PLAN:78). One route stays open: the fix pass (new F3).
- Earlier F2 (outcome words and threshold): fixed in text (PLAN:82, PLAN:96); the controlling variant and the reduced-panel threshold exist but leave R1b without a word (new F1) and score unequal panels (new F2).
- Earlier F3 (QA rules 8 and 9 outside the edit lists): fixed in text. Principle 8 and rule 9 of both agents are rewritten (PLAN:160, PLAN:179) with zero-count acceptance lines (PLAN:168, PLAN:185); the positive lines pass vacuously (new F5) and label-floor lines remain (new F6).
- Earlier F4 to F16: fixed. Evidence: arm scope stated (PLAN:78), per-trigger grep lines (PLAN:166), the pinned sentence kept (PLAN:142, PLAN:149), the hashed bytes defined once (PLAN:44), the recheck sentence kept (PLAN:142), the baselines of M4, M5, M6, M9, M11 named in Task 14 (PLAN:256), the audit scorer labelled (PLAN:229), the plugin-mirror clause removed (PLAN:240), the ledger fields listed (README:43), L3 text placed after the cap sentence (PLAN:169), `Kept mechanical gates` section named (PLAN:162), the missing-command clause (PLAN:158), the empty confirmation file and one-gate baseline (PLAN:40, PLAN:61).

## Findings

<!-- Source: base: reviewer-2 F4 (R3 part); incorporated: reviewer-1 F1; debate C-002, X-001 (both advocates 62 to 65 percent); probe INV-003 (a), (b) -->
F1 | severity MAJOR | blocking true | unpassable-check | Task 3's outcome words give R1b no word when the safety class is below its minimum n, and leave R3 and the advisory and zero-base cases ambiguous. R1b is "one event, never advisory" (PLAN:91). PASS needs "the class is at or above its minimum n" and only FAIL has the "R1b fails at any n" exception (PLAN:96). Stage 0 says an undersized set is the expected outcome (S0:106: "the advisory fallback is the expected outcome"). In that case, with every planted safety defect found-and-blocking under the new text, R1b cannot be PASS (class below min n), ADVISORY-PASS (barred), FAIL (the rule holds) or NOT-MEASURABLE (PLAN:96 does not list R1b). Task 4 reads that word as the gate (PLAN:113) and Task 14 states RT1 tripped or not from it (PLAN:257), so an executor must invent a word; a false FAIL would report RT1 as tripped. R3 has the same hole: S0:106 names a minimum n for the gating classes only, so "at or above its minimum n" is undefined for the cosmetic class; and a class below its minimum n with a zero old base fits both ADVISORY and NOT-MEASURABLE while each line takes exactly one word (PLAN:86). Fix: append to PLAN:96 "R1b has no minimum n and is never advisory: PASS when every planted safety defect is found-and-blocking under the new text, FAIL otherwise, with n and the interval shown beside it"; state that R3 is always advisory; give a precedence order when both ADVISORY and NOT-MEASURABLE apply. Debate: C-002 and X-001, confirmed by both advocates (62 to 65 percent); Variant 2's card had seen only the R3 part. | citations:
- PLAN:91 "one event, never advisory"
- PLAN:96 "PASS (the rule holds and the class is at or above its minimum n)"
- S0:106 "the advisory fallback is the expected outcome"
- PLAN:86 "each with exactly one outcome word"
- PLAN:257 "RT1 (seeded part) and RT3 are judged from the Task 3 result"

<!-- Source: base: reviewer-2 F1; debate C-003, X-002 (both advocates 72 percent) -->
F2 | severity MAJOR | blocking true | other | The found threshold scores the two arms with different numbers of valid reviewers. PLAN:82 sets "found" as more than half of an arm's valid reviewers ("2 of 3 with three valid reviewers, 2 of 2 with two") and lets the controlling variant alone set each word. The hook confound makes new-arm reviewers the ones likely to be invalid (PLAN:80, PLAN:82), so 3 old-arm against 2 new-arm reviewers is the expected case. If each reviewer finds a defect with probability 0.9 (illustrative, assumes independence), 2 of 3 finds it 97 percent of the time and 2 of 2 finds it 81 percent: about 16 points from panel size alone, against the 5-point margin the stage 0 sizing aims at (S0:106). That pushes R1, R1b, R2a and R2b toward FAIL and R3 toward PASS. Recall lines err toward a ruling (the safe side); R3 errs toward a PASS that needs no ruling; and because R1b feeds the RT1 statement of Task 14 (PLAN:257), a panel-size artifact can report RT1 as tripped. Fix: score both arms on the same k, the smaller valid count (at least 2), list the reviewers dropped to equalise, or mark the line NOT-MEASURABLE. Debate: C-003 and X-002, both advocates 72 percent. | citations:
- PLAN:82 "2 of 3 with three valid reviewers, 2 of 2 with two"
- PLAN:80 "the recall-equality lines are biased toward PASS and the cosmetic-fall line toward FAIL"
- S0:106 "a minimum n per gating class"
- PLAN:257 "RT1 (seeded part) and RT3 are judged from the Task 3 result"

<!-- Source: base: reviewer-2 F5 (regraded from non-blocking to blocking); debate C-007 (open point, settled on the probe's evidence); probe INV-001 (HIGH, unaddressed) -->
F3 | severity MAJOR | blocking true | contradiction | The claim that a failed gate leaves no rule file switched does not hold under `/sc:implement`'s fix pass and retry ladder, and Task 6's acceptance lines demand the edit the task forbids. PLAN:21 says "A halt at Task 4 or at the start of Task 6 leaves no rule file switched" and Task 6 says "stop: this task edits nothing and fails" (PLAN:140). A failed check is a non-compliant verdict, not a halt: `/sc:implement` runs exactly one fix pass (SKILL.md:145; qa.md:245) and then the repair round and the ladder, and every halt leaves the failed attempt in the worktree (retry.md:109 "nothing has been reverted"; retry.md:158 "the A5 tree stays for the operator"). Task 6's acceptance lines 2 to 7 (the digest in pragmatic.md, the registry row `v2`, the cap and own-model sentences, the cadence change, the hook check; PLAN:146 to PLAN:152) stay unmet until pragmatic.md and the registry row are edited, and PLAN:22 forbids only editing the result file, the ledger and the gate file. A fixer working from those lines can write the edit and the `v2` row. Tasks 7 to 10 then read only the registry row (PLAN:158, PLAN:177, PLAN:193, PLAN:203) and proceed; and when a halted Task 6 is closed by a `/sc:implement` Ruling (qa.md:254; ledger.md:158), the attempt's edit stays and the `v2` row is what Tasks 7 to 10 find. PLAN:22's "does not count" binds the plan text, not the executor. This is the consequence of the earlier review's F1, reachable through the fix pass instead of the first attempt. Debate: C-007 and INV-001 (HIGH, unaddressed): both advocates graded it non-blocking at 55 percent before reading qa.md:245 and retry.md:109 and :158 together with Task 6's acceptance lines; the fault-finder's evidence, re-read by the orchestrator, decides it. Fix: make Task 6's acceptance lines 2 to 7 conditional on the first-paragraph check passing; state that no fix pass, repair, retry or adviser step of Task 6 edits src, tests or plugins while the check fails; have Tasks 7 to 10 (and 11 to 14) re-read the gate the way Task 6 does (result file hash, five outcome words, ledger rulings) and not only the registry row. | citations:
- PLAN:21 "A halt at Task 4 or at the start of Task 6 leaves no rule file switched"
- PLAN:140 "stop: this task edits nothing and fails"
- PLAN:145 "Re-checked after the edit"
- PLAN:158 "First read that the registry row of `output-styles/pragmatic.md` reads `v2` and stop without editing when it does not"
- PLAN:22 "Gates are read, never edited"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:145 "exactly one fix pass"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:245 "Exactly one fix pass + re-QA"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:254 "A clear user confirmation in the current conversation is sufficient"
- src/superclaude/skills/sc-implement-protocol/refs/retry.md:109 "Every halt in procedure steps 3-5 leaves failed attempt k in the worktree; nothing has been reverted."
- src/superclaude/skills/sc-implement-protocol/refs/retry.md:158 "the A5 tree stays for the operator"
- src/superclaude/skills/sc-implement-protocol/refs/ledger.md:158 "An eligible Ruling with no `complete` after it"

<!-- Source: base: reviewer-2 F9; debate C-004 (V1 F2 regraded from blocking to minor); incorporated: reviewer-1 F2 -->
F9 | severity MINOR | blocking false | other | Task 5's acceptance line says the review help "still lists" `verify`, but the command is registered as `verify-citations`. A word or substring match passes, and a literal command-name match cannot. Fix: name the full command names. | citations:
- PLAN:132 "still lists `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify` and `manifest`"
- src/superclaude/cli/review/verify_cmd.py:76 `@click.command(name="verify-citations")`

<!-- Source: base: reviewer-2 F8 -->
F10 | severity MINOR | blocking false | other | Task 6 says the old pins are red and not run "except the two listed below", and the acceptance line that follows lists three test files. Fix: say "the three". | citations:
- PLAN:142 "except the two listed below"
- PLAN:152 "tests/skills/test_review_severity_registry.py tests/skills/test_review_brief_rests_on.py tests/skills/test_review_prompt_overrides.py"

<!-- Source: base: reviewer-2 F6 -->
F11 | severity MINOR | blocking false | other | Stage 4 reads the label of Rule 6 as the bold words between the `**` marks of one numbered line, and Task 8 does not require the rewritten Rule 6 to keep that form. If the bold heading is dropped, stage 4's check has nothing to read. Fix: add to Task 8 that Rule 6 keeps the form `6. **<heading>** ...`. | citations:
- S4:39 "the label is the bold words"
- PLAN:177 "rewrite Rule 6"

<!-- Source: base: reviewer-2 F9 -->
F12 | severity MINOR | blocking false | other | The scan test of Task 13 reads Markdown in seven roots, while the spec's T5 says "`src/` or `plugins/`". No hit lies outside the scanned roots today (all Markdown hits are in agents, skills and templates), so nothing is missed now. Fix: state the roots are the complete set of Markdown folders with hits, or scan every `*.md` under `src/superclaude`. | citations:
- SPEC:920 "appears in `src/` or `plugins/` outside the scale-map allow-list"
- PLAN:240 "The scan reads Markdown files only"

<!-- Source: base: reviewer-2 F10 (second half) -->
F13 | severity MINOR | blocking false | other | The L1 text in Task 7 omits two parts of the spec's merge rule: the `reasked` flag and "the reviewer's label stands, the row is tagged `consumer-unknown` and listed first". The digest in the same file carries the consumer-unknown rule (SPEC:201), so the verdict is unaffected; only metric M8 reads `reasked`. Fix: add the two clauses to the L1 sentence. | citations:
- PLAN:158 "sends a blocking grade that names no consumer back once"
- SPEC:270 "the reviewer's label stands, the row is tagged `consumer-unknown` with a `reasked` flag and listed first"

<!-- Source: base: none (new from the earlier review's card, PRIOR F2); incorporated: earlier review F2 (PRIOR); no debate point -->
F14 | severity MINOR | blocking false | contradiction | The byte-copied request still carries unrevised base text that says the seeded-recall result gates the rule switch "by an acceptance line, not by a dependency line" and "Do not rely on `Depends on:` for this gate", while the revised plan makes the gate a task and gives Task 6 a `Depends on` line on it. Task 6 also re-checks the gate in its own body, so the intent holds; this is history in a file the plan reads as its source. Fix: add one sentence to the Revision 3 section of the request that the base text is superseded for this point. | citations:
- SRC:3 "gates the rule switch by an acceptance line, not by a dependency line"
- SRC:13 "Do not rely on `Depends on:` for this gate."
- PLAN:138 "Depends on: Task 2, Task 3, Task 4"

<!-- Source: base: none (new from the earlier review's card, PRIOR F5); incorporated: earlier review F5 (PRIOR); probe INV-005 -->
F15 | severity MINOR | blocking false | missing-requirement | Three small gaps in Task 1's entry check: the request makes "the owner has read" the stage 2 summary a start condition and the plan checks only that the file exists and that the ledger holds the go; the "Tree" line records the status output with no pass criterion although the acceptance line wants every line to read PASS; and stage 0 evidence is checked for existence only, so a file with an unfit verdict passes. Fix: state in Task 1 that the go covers the reading, that the tree line passes when recorded, and what the stage 0 files must say. | citations:
- SRC:3 "exists and the owner has read it"
- PLAN:41 "the line only checks that `stage2-summary-for-owner.md` exists"
- PLAN:45 "Task 4 compares against it"
- PLAN:42 "Earlier evidence exists"

## Follow-up candidates

<!-- Source: base: none (new from the invariant probe); incorporated: probe INV-002; context from reviewer-2 F5 -->
F4 | severity MEDIUM | blocking false | other | In the expected undersized case Task 4 cannot reach PASS in the same run, and the way to continue is not stated. PLAN:98 requires a ruling that cites the SHA-256 of the result file "as it is now", a file Task 3 writes, and `/sc:implement` has no pause between Tasks 3 and 4. S0:106 makes the advisory (non-PASS) outcome the expected one, so Task 4 starts non-compliant, takes the fix pass and the ladder (qa.md:245); resume row H (ledger.md:160) re-reviews the tree as it stands, including the stale FAIL gate file; only a `/sc:implement` Ruling (ledger.md:158) closes Task 4, which PLAN:22 says does not count as the gate. The package still works because Task 6 checks the ledger itself, but the owner path is two rulings in a stated order that the plan does not give. Task 1's "more shadow runs and a re-run" (PLAN:47) needs a new package slug, because a plan edit stops with E-PLAN-CHANGED (managed-workspace.md:44). Fix: state the order (close Task 4 by a `/sc:implement` Ruling after the result file exists, record the ledger ruling with the result hash, then run Task 6), or add an owner stop after Task 3; name the new-slug re-run for Task 1. | citations:
- PLAN:98 "A ruling that cites a different hash is void"
- PLAN:47 "the remedy is more shadow runs and a re-run of this package"
- src/superclaude/skills/sc-implement-protocol/refs/ledger.md:160 "A `halt` record exists"
- src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:44 "E-PLAN-CHANGED"

<!-- Source: base: reviewer-2 F2 (regraded from blocking to Medium); debate C-005 (both advocates ended at non-blocking, 62 and 60 percent) -->
F5 | severity MEDIUM | blocking false | unpassable-check | Several positive acceptance checks of Tasks 6 to 8 pass from the digest the same task inserts. The rewritten principle 8 and rule 9 must "contain the words 'stays open for verification'" and rule 9 must contain `consumer-unknown` (PLAN:168, PLAN:185), but the digest already holds "An unverified safety claim stays open for verification" and "tag the row `consumer-unknown`" (SPEC:199, SPEC:201), and neither phrase is in either agent today. The cap and own-model checks of Task 6 count "1 or more" (PLAN:147) while the digest's last sentence is the cap bullet word for word. The zero-count lines of the same bullets still force the old doubt text out, so the consequence is lost replacement prose, not a wrong grade; a task that deletes principle 8 and rule 9 passes every line. Fix: pair each positive phrase with its anchor on one line (for example `grep -n "NO LENIENCY" file` piped to a grep for the phrase) and require the cap sentence count to be 2 in pragmatic.md. Debate: C-005; both advocates ended at non-blocking (62 and 60 percent). | citations:
- PLAN:168 "the rewritten principle 8 and rule 9 contain the words"
- PLAN:147 "`grep -c` of each sentence prints 1 or more"
- SPEC:199 "An unverified safety claim stays open for verification"
- SPEC:201 "tag the row `consumer-unknown`"

<!-- Source: base: reviewer-2 F3 and the first half of reviewer-2 F10 (regraded from blocking to Medium); debate C-006, C-012 (both advocates ended at non-blocking, 60 to 62 percent) -->
F6 | severity MEDIUM | blocking false | contradiction | Label-floor and relay lines in the QA agents contradict the rewritten Rule 6 and are in no edit list. rf-qa-qualitative.md:593 says "Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below)", :611 says "Severity floor: IMPORTANT" and the next line, :612, adds "(cf. Critical Rule #6)", :616 ends the AX-2 example with ">= IMPORTANT", and :918 tells the team lead "Must resolve ALL CRITICAL and IMPORTANT issues before proceeding"; rf-qa.md:389 scopes the re-verify to "blocking (CRITICAL or IMPORTANT)" issues. None matches the S0:34 freeze patterns and neither Task 7 (PLAN:158) nor Task 8 (PLAN:177) lists them. They assign labels, which the digest calls information (SPEC:203), and no test pins them (tests/audit/test_severity_floor_unweakened.py pins the block hash, Rule 6 and the softening tokens only), so they change no verdict; but AX-2 still cites a Rule 6 that Task 8 rewrites so that a contradiction nothing rests on is a follow-up, and :918 can prompt a fix of a row graded Medium. Fix: reword these lines in Tasks 7 and 8 and add a `grep -c -F` line for each. Debate: C-006 and C-012; both advocates ended at non-blocking (60 to 62 percent), the opus card had graded the first four blocking. | citations:
- src/superclaude/agents/rf-qa-qualitative.md:593 "Contradictions remain IMPORTANT or CRITICAL by default"
- src/superclaude/agents/rf-qa-qualitative.md:611 "Severity floor: IMPORTANT"
- src/superclaude/agents/rf-qa-qualitative.md:918 "Must resolve ALL CRITICAL and IMPORTANT issues before proceeding"
- src/superclaude/agents/rf-qa.md:389 "For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report"
- src/superclaude/agents/rf-qa-qualitative.md:990 "Contradictions are always IMPORTANT or CRITICAL"
- PLAN:177 "rewrite Rule 6"

<!-- Source: base: none (new from the invariant probe); probe INV-003 (c), (d) -->
F7 | severity MEDIUM | blocking false | other | Reviewer validity in Task 3 is judged after the grades are read, with no mechanical test, so the "fixed before dispatch" threshold depends on a count made afterwards. PLAN:82 defines a valid reviewer as one whose quoted sentences "come from the rule text its arm was given" and takes the threshold from the number of valid reviewers; dropping one reviewer turns 2 of 3 into 2 of 2. R1's gloss "new count not below old" (PLAN:90) also passes a swap of one defect for another. Fix: define validity as a substring match of each quoted sentence against `old-arm-block.md` or `new-arm-block.md`, and read R1 as "no planted safety defect that is found-and-blocking under the old text is missed under the new text". | citations:
- PLAN:82 "the sentences it quotes for its grades come from the rule text its arm was given"
- PLAN:90 "new count not below old"

<!-- Source: base: none (new from the invariant probe); probe INV-004 -->
F8 | severity MEDIUM | blocking false | other | Task 3 copies the old arm from the live `pragmatic.md` "as it is now, which holds the old rule" (PLAN:78) and nothing checks that. Task 1's entry check (PLAN:38 to PLAN:45) uses the absence of `--promote` as a proxy for Task 10 but never reads that the registry row of `output-styles/pragmatic.md` is `legacy` or that no `digest v2 begin` fence exists in the file. After a partial earlier run and a fresh re-run under a new slug, the "old" arm would be the new text and R2a and R2b would pass trivially. Fix: add a Task 1 line that the row reads `legacy` and the fence is absent. | citations:
- PLAN:78 "copied byte for byte from the live file as it is now"

## Checked

- Task numbers 1 to 14 are contiguous, every `Depends on` points to a lower task, Task 14 depends on 1 to 13, there are 5 phases, and `/tmp/gate_check.py` prints `14 tasks 5 phases PASS` for the plan.
- Live lines the plan cites hold: pragmatic.md 221, 225, 226, 229, 230; rf-qa.md 83, 100, 402, 548, 549; rf-qa-qualitative.md 84, 99, 240, 291, 362, 429, 500, 567, 746, 784, 809, 983, 990, 993, 994; rf-analyst.md 75; the cap sentence appears on 2 lines of each agent and the digest words it differently; the Critical Rules window hash (header at 983, window 980 to 989) ends before Rule 6.
- The digest holds none of the strings the zero-count lines require absent ("claim is blocking", "it FAILS. Grade what you find", "When in doubt, fail it").
- The merge-phrase scan hits only the files the plan and the stage 1 allow-list name; no hit under plugins or outside the seven roots.
- Stage 0, 1, 2 and 4 plans create the files and names the plan reads (inventory freeze, seeded set and planted deliverable, escape test, regrade, `refs/rule.md`, registry, scale-map and its allow-list format, `shadow_summary.py --confirmed-misses` with the "not computable" line, the sweep paragraph and call lines, the registry counts, the allow-list rows stage 4 removes, no new plugin surface).
- No fixture row pins the lines Tasks 6 to 8 rewrite; the cap-edit rows survive if L3 text follows the cap sentence.
- The RT5 threshold (75 percent of the M1 mean), the split of RT1 (seeded part) and RT3 judged now against the others pending, and the baseline sources of M4, M5, M6, M9, M11, M12 match SPEC section 13.
- The earlier review's F12 is closed: README lists the ledger-row fields the plan reads (README:43).
- Mechanically unmapped coverage row INF-002 (stage 0b and 0c evidence, source.md:3) is covered by hand in Task 1 (PLAN:42).
- No commands or tests were run by the reviewers; this is a source-based review. Whether `uv run pytest tests/audit` passes as a whole after Tasks 6 to 10 is not established.

## Self-report

confidence: 0.86 (mean of the two calibrated card scores 0.88 and 0.84; orchestrator merge)
reviewer_model_self_report: merged by the adversarial pipeline; base reviewer-2 (opus class), incorporated reviewer-1 (haiku class) and the fault-finder probe (sonnet class)

<!-- The Write tool refused REPORT.md for this run ("Subagents should return findings as text, not write report files"), so by the lead's instruction the report body is placed here, between the two markers, and not written by another route. The text above this block is the merged card as the run produced it (with the F8 citation dropped and the F6 line fixed after the evidence-validator gate). -->
<!-- BEGIN REPORT BODY -->
# Reflect report (pre-execution), stage 3 plan, review 3 of 3 (revision 3 of the plan)

```yaml
contract_version: 1.8.0
status: partial                      # forced by one dropped citation (F8, PLAN:45); the content is otherwise complete
mode: pre
tier_reached: 2
confidence_calibrated: 0.86          # mean of the two reviewer-card calibrations (0.88 and 0.84); the T1 card calibrated 0.70
citations_total: 100                 # 55 card citation bullets + 45 inferred-requirement rows
citations_revalidated: 100
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Verdict: NEEDS-REVISION
- Findings: 3 blocking (F1 to F3), 12 non-blocking (F4 to F8 Medium, F9 to F15 minor)
- Run folder: `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116185913/`
- Full finding texts with every citation: `adversarial/merged-review-card.md` (above this block). Aliases: PLAN, SRC, S0, S4, SPEC, README, PRIOR as defined in its second comment line.

## Verdict

NEEDS-REVISION. Revision 3 fixed all three blocking findings of the earlier review in text and the 13 non-blocking ones, but three defects remain that gate the rule switch: the seeded-recall outcome words give R1b no word in the expected small-set case (F1), the found threshold scores the two arms with different panel sizes (F2), and the "a failed gate leaves no rule file switched" guarantee does not hold under `/sc:implement`'s fix pass and retry ladder (F3). Debate: 19 of 20 diff points agreed (95 percent); F3 was graded blocking on the invariant probe's evidence against both advocates' non-blocking grade.

## Earlier findings (review 2, `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116174401/REPORT.md`)

- Earlier F1 (gate ran after the edit): fixed in order (Task 4 is read-only, PLAN:113; Task 6 re-checks before its first edit, PLAN:140; old arm frozen as a copy, PLAN:78). One route stays open: the fix pass (new F3).
- Earlier F2 (outcome words and threshold): fixed in text (PLAN:82, PLAN:96); leaves R1b without a word (new F1) and scores unequal panels (new F2).
- Earlier F3 (QA rules 8 and 9): fixed in text (PLAN:160, PLAN:179, with zero-count lines PLAN:168, PLAN:185); the positive lines pass vacuously (F5) and label-floor lines remain (F6).
- Earlier F4 to F16: fixed (evidence in the card; README:43 now lists the ledger-row fields).

## Findings

F1 | blocking | Task 3's outcome words give R1b no word when the safety class is below its minimum n. R1b is "one event, never advisory" (PLAN:91); PASS needs "the class is at or above its minimum n" and only FAIL has the "R1b fails at any n" exception (PLAN:96); stage 0 says an undersized set is the expected outcome (S0:106). Task 4 reads the word as the gate and Task 14 states RT1 from it (PLAN:257), so an executor must invent a word and a false FAIL reports RT1 tripped. R3 has the same hole (no minimum n for the cosmetic class) and ADVISORY and NOT-MEASURABLE overlap (PLAN:86). Fix: add to PLAN:96 "R1b has no minimum n and is never advisory: PASS when every planted safety defect is found-and-blocking under the new text, FAIL otherwise, with n and the interval shown"; make R3 always advisory; give a precedence order.

F2 | blocking | The found threshold scores arms with different numbers of valid reviewers (PLAN:82: "2 of 3 with three valid reviewers, 2 of 2 with two"). New-arm reviewers are the ones likely to be invalid (PLAN:80, PLAN:82), so 3 against 2 is the expected case; at an illustrative 0.9 per reviewer, 2 of 3 finds a defect 97 percent of the time and 2 of 2 finds it 81 percent, a 16-point artifact against a 5-point margin (S0:106). R1, R1b, R2a and R2b lean toward FAIL (a ruling, the safe side), R3 toward a PASS that needs no ruling, and R1b can falsely report RT1 as tripped (PLAN:257). Fix: score both arms on the same k, the smaller valid count (at least 2), list the reviewers dropped, or mark the line NOT-MEASURABLE.

F3 | blocking | A failed gate does not leave "no rule file switched" (PLAN:21) under `/sc:implement`. A failed Task 6 check is a non-compliant verdict, not a halt: exactly one fix pass (SKILL.md:145; refs/qa.md:245), then the repair round and the ladder, and every halt leaves the failed attempt in the worktree (refs/retry.md:109, :158). Task 6's acceptance lines 2 to 7 (PLAN:146 to PLAN:152) demand the edit and the `v2` row that the task text forbids (PLAN:140); PLAN:22 forbids editing only the result file, the ledger and the gate file. Tasks 7 to 10 read only the registry row (PLAN:158, :177, :193, :203), and a `/sc:implement` Ruling that closes Task 6 (qa.md:254; ledger.md:158) leaves the edit in place; PLAN:22's "does not count" binds the plan text, not the executor. Fix: make acceptance lines 2 to 7 conditional on the first-paragraph check passing; say that no fix pass, repair, retry or adviser step edits src, tests or plugins while the check fails; have Tasks 7 to 14 re-read the gate (hash, five words, ledger rulings), not only the row.

F9 | minor | Task 5's acceptance line says the review help "still lists" `verify`; the command is registered as `verify-citations` (PLAN:132; src/superclaude/cli/review/verify_cmd.py:76). Fix: name the full command names.

F10 | minor | Task 6 says "except the two listed below" (PLAN:142) and then lists three test files (PLAN:152). Fix: "the three".

F11 | minor | Stage 4 reads the bold words of the Rule 6 line (S4:39); Task 8 does not require the rewritten Rule 6 to keep the form `6. **<heading>** ...` (PLAN:177). Fix: add that sentence.

F12 | minor | The Task 13 scan reads Markdown in seven roots (PLAN:240) while SPEC:920 says `src/` or `plugins/`; no hit lies outside the scanned roots today. Fix: say the roots are the complete set or scan all `*.md` under `src/superclaude`.

F13 | minor | The L1 text in Task 7 omits the `reasked` flag and "label stands, listed first" (PLAN:158; SPEC:270); the digest carries the consumer-unknown rule (SPEC:201), so only metric M8 is affected. Fix: add the two clauses.

F14 | minor | The byte-copied request keeps unrevised base text ("by an acceptance line, not by a dependency line", SRC:3; "Do not rely on `Depends on:` for this gate.", SRC:13) while Task 6 has a `Depends on` line on the gate task (PLAN:138); the plan also re-checks the gate in Task 6's body, so the intent holds. Fix: one sentence in the Revision 3 section of the request (SRC:43) that the base text is superseded for this point.

F15 | minor | Task 1's entry check: "the owner has read" the stage 2 summary (SRC:3) is not checked beyond file existence (PLAN:41); the Tree line has no pass criterion (PLAN:45); stage 0 evidence is checked for existence only (PLAN:42). Fix: state in Task 1 that the go covers the reading, that the tree line passes when recorded, and what the stage 0 files must say.

## Follow-up candidates (Medium, never fail a review)

F4 | Medium | In the expected undersized case Task 4 cannot reach PASS in the same run: the ruling must cite the hash of a file Task 3 writes (PLAN:98), `/sc:implement` has no pause between Tasks 3 and 4, resume row H re-reviews the stale FAIL gate file (ledger.md:160) and only a `/sc:implement` Ruling closes Task 4 (ledger.md:158), which PLAN:22 says does not count; Task 6's own ledger check then protects the edit. Task 1's re-run (PLAN:47) needs a new slug (managed-workspace.md:44). Fix: state the order of the two rulings or add an owner stop after Task 3.

F5 | Medium | Positive acceptance lines of Tasks 6 to 8 pass from the inserted digest: "stays open for verification" and `consumer-unknown` (SPEC:199, SPEC:201; PLAN:168, PLAN:185), and the cap checks count "1 or more" (PLAN:147). The zero-count lines still force the old text out, so the loss is replacement prose, not a wrong grade. Fix: pair each phrase with its anchor line.

F6 | Medium | Label-floor and relay lines contradict the rewritten Rule 6 and are in no edit list: rf-qa-qualitative.md:593, :611 (with :612 "cf. Critical Rule #6"), :616, :918 and rf-qa.md:389. They assign labels (information under the digest, SPEC:203), no test pins them, so no verdict changes; AX-2 cites a Rule 6 that Task 8 rewrites, and :918 can prompt a fix of a row graded Medium. Fix: reword them in Tasks 7 and 8 with a `grep -c -F` line each.

F7 | Medium | Reviewer validity is judged after the grades are read (PLAN:82), so the "fixed before dispatch" threshold depends on a later count; R1's gloss "new count not below old" (PLAN:90) passes a swap. Fix: a substring test of each quoted sentence against the two arm copies.

F8 | Medium | Task 3 copies the old arm from the live `pragmatic.md` "as it is now" (PLAN:78) and Task 1 never reads that the registry row is `legacy` and no `digest v2 begin` fence exists; after a partial run and a re-run the old arm would be the new text. Fix: add that check to Task 1. (One citation of this finding, PLAN:45, was dropped by the evidence gate.)

## Inferred requirements (Pass 2)

Pass 1 found one parsed row (REQ-04, SRC:55, covered by Tasks 3 and 6). Pass 2 emitted 45 quote-pinned rows; 44 match a plan item by the containment rule (0.6 of content words), one (INF-002, the stage 0b and 0c evidence, SRC:3) is unmatched by the mechanical rule and is covered by hand in Task 1 (PLAN:42). `coverage_pct` 1.0 (parsed only, 1 row); `coverage_pct_union` 0.9783; `coverage_degraded: parsed-sparse` (inferred 45 against parsed 1) forced Tier 2. All 45 quotes were re-read against their cited lines at Wave 5 (45 verified, 0 dropped). Full table: `artifacts/inferred-table.md`.

## Checked

- Task numbers 1 to 14 contiguous, every `Depends on` points to a lower task, Task 14 depends on 1 to 13, 5 phases; `/tmp/gate_check.py` prints `14 tasks 5 phases PASS`.
- Live lines the plan cites hold (pragmatic.md 221 to 230; rf-qa.md 83, 100, 402, 548, 549; rf-qa-qualitative.md 84, 99, the eight FAIL pairs, 809, 983, 990, 993, 994; rf-analyst.md 75); the cap sentence is on 2 lines of each agent and the digest words it differently; the Critical Rules window hash (980 to 989) ends before Rule 6.
- The digest holds none of the strings the zero-count lines require absent.
- The merge-phrase scan hits only files the plan and the stage 1 allow-list name; no hit under plugins.
- Stage 0, 1, 2 and 4 plans create the names the plan reads and agree on registry counts, allow-list rows and the plugin position.
- RT5 threshold, the RT1 (seeded part) and RT3 split, and the M4, M5, M6, M9, M11, M12 baseline sources match SPEC section 13. The earlier F12 is closed (README:43).
- No commands or tests were run by the reviewers; whether `uv run pytest tests/audit` passes after Tasks 6 to 10 is not established.

## Run notes (protocol deviations and degradations)

- `REPORT.md` was refused by the Write tool; this body is placed here as instructed. `report_path` is null in `return-contract.yaml`.
- Reviewers, advocates, fault-finder, scorers, calibrators, merge-executor and evidence-validator were spawned as plain subagents (a teammate cannot spawn named teammates); every role of the protocol ran.
- Executor class resolved by log heuristic (sonnet, same class as this session); N=2 reviewers (haiku analyzer, opus qa); `t2_model_class_diversity: degraded`, `t2_vendor_diversity: single`, `calibrator_diversity: full`.
- `.dev/reflect/runs.jsonl` and the memory files of section 6.3 were not written, because the lead's rule limits output to the new run folder.
- Citation budget: all 100 citations were re-read (stricter than the sampled policy for more than 20).

## Self-report

confidence: 0.86 (mean of the two calibrated card scores; orchestrator merge)
<!-- END REPORT BODY -->

# Review: S4 two-part phase plans (spec section 6)

Scope: `diff specs/history/spec-v8-after-p0-fixes.md specs/orca-worker-contract-spec.md` (one changed line, spec:238) and row S4 at `decisions/APPROVED.md:47`. Reviewed 2026-11-03, read-only except this file.

## Verdict

**PASS.** No blocking defect. The citation is accurate, the new text does not contradict sections 6, 7.1, 7.2 or 7.3, and a planner can split P0 by applying the rule "static = needs no live Orca run" plus elimination. Nine notes below; N1 (manual checks have no home) must be fixed before P1 or P2 is planned.

### Citation check (question 1)

`sk/sc-implement-protocol/refs/qa.md:288` reads: "No other path may stop automation or prompt the user." It is the closing line of the "Closed list of interrupts" section, whose items 1-7 are the QA halts, the dispute halt, `E-NO-RULING`, `operator-review`, `E-RESUME-NEEDED`, the input/integrity STOPs and `E-ARCHIVE-BLOCKED`. The source copy and the installed copy `~/.claude/skills/sc-implement-protocol/refs/qa.md` are byte-identical (`cmp`). The spec's paraphrase "may not prompt the user outside its halt paths" is correct in substance; see N8 for a wording nit.

### P0 split (question 3)

| Check | Part | Basis |
|---|---|---|
| AC-0.1 | static | import, temp-dir install, pytest (spec:298, 335) |
| AC-0.2 | static | `cmp` and the existing level-table test (spec:299) |
| AC-0.3 | static | merge-base diff counts uncommitted edits (spec:300, 337-339) |
| AC-0.4 | live | is the 7.2 live check (spec:301) |
| AC-0.5 | live | timed `worker-start` is a live Orca run, but not a "7.2 live check"; placed by elimination (N2) |
| AC-0.6 | live | reads an AC-0.4 transcript, so it must follow AC-0.4; placed by elimination (N2) |
| AC-0.7 | static | "Read-only trace ... No live probe" (spec:304); its result goes into the phase report, which the live plan holds (N3) |
| AC-0.8 | n/a | not in the spec: moved to P1 by B2 (`APPROVED.md`, B2 row); no `AC-0.8` string remains in the spec |
| AC-0.9 | static | pytest audit (spec:305) |
| AC-C1 | static | grep (spec:244-254) |
| AC-C2 | static | `make verify-sync` (spec:256-259) |
| AC-C3 | static | baseline before the static plan's first edit, rerun after its last (spec:261-264) |
| AC-C4 | static by the rule | but only meaningful at commit time, which is now outside both plans (N4) |
| AC-C5 | static | vacuous at P0 ("no command edits", spec:220) |
| AC-C6 | static | reads a config file, no run (spec:276-279); records into the phase report (N3) |

Ambiguities: AC-0.5 and AC-0.6 (resolvable by elimination), AC-C4 (timing), AC-0.7 and AC-C6 (result hand-off to the live plan's phase report). None leaves a planner unable to split P0.

## Findings

| # | Severity | file:line | Problem | Fix |
|---|---|---|---|---|
| N1 | note (fix before P1/P2 planning) | spec:238; spec:308 (AC-1.3 manual part), spec:318 (AC-2.5), spec:321 (AC-2.8) | The rule sorts checks only into "need no live Orca run" (static) and "7.2 live checks" (live). Manual checks run by a person need no live Orca run, so the rule puts them in the static plan, where `/sc:implement` may not prompt the user (qa.md:288). That is the same conflict S4 exists to remove. No P0 check is manual, so P0 is unaffected. | Add: "Checks marked manual are run by the person in the coordinator session, outside any plan run, like the commit and install, and recorded in the phase report." |
| N2 | note | spec:238; spec:302-303 | The live plan "holds the 7.2 live checks", but AC-0.5 (timed `worker-start`) and AC-0.6 (transcript read) are live Orca work that is not a 7.2 check. A planner places them in the live plan only by elimination. Same for later non-7.2 live work (AC-1.3 scratch run, AC-3.4 with its own pass condition). | Say "The live plan holds every remaining check (the 7.2 live checks and any other check that needs a live Orca run) and the phase report." |
| N3 | note | spec:238; spec:276, spec:304 | AC-0.7 and AC-C6 are static by the rule, yet their pass conditions write into "the phase report", which only the live plan holds. The hand-off is unstated: a planner may duplicate the check in the live plan or lose its result. | Add: "Static checks whose results the phase report records are saved by the static plan and copied into the phase report by the live plan." |
| N4 | note | spec:238; spec:266-269 | AC-C4 guards what is staged for the commit (`git diff --cached`). The commit now happens between the plans, outside any plan, so AC-C4 run inside the static plan passes on whatever is staged then, not on the commit's contents. | Add "the coordinator runs AC-C4 immediately before that commit" to the between-plans sentence, or to 7.2's commit sentence (spec:282). |
| N5 | note | spec:238 (first sentence) | "Each phase is one written plan" is kept, then the same paragraph says the plan "comes in two parts", names "the static plan" and "the live plan", says the live plan "is written after" the static checks pass, and refers to "both plans". These are two written plans, each its own `/sc:workflow` and `/sc:implement` run. The later sentences override the first, so a planner is not misled, but the paragraph opens with a statement it then contradicts. | Reword the first sentence: "Each phase is planned and executed under the repo's level-3 route ..., in two written plans as below, because ..." |
| N6 | note | spec:238; spec:301 ("a failure here reopens section 1") | No path for a live-check failure that needs a code fix: the live plan holds no edits and the static plan has already passed. | Add: "A fix found by the live plan goes into a new static plan; the commit, install and live plan are then repeated." |
| N7 | note | spec:238; spec:216, spec:241, spec:282 | Consistent, recorded for the planner: "Later phases do not start until the earlier phase's checks in section 7 pass" (spec:216) and "A phase passes only when every check in its block and every common check passes" (spec:241) both hold with "the phase passes only when both plans' checks pass". The commit/install sentence matches 7.2's two approvals (commit authorization and install approval, spec:282) and spec:216's "per-phase approvals of section 7.2". | none |
| N8 | note | spec:238; `APPROVED.md:47` | "Outside its halt paths" is narrower than qa.md:288's closed list, which also includes `E-NO-RULING`, `E-RESUME-NEEDED` and input STOPs. The S4 row says "no live run" where the spec says "no live Orca run". Neither changes the meaning. | Optional: "outside its closed list of interrupts"; align the row to "no live Orca run". |
| N9 | note | spec:238 | The level-3 justification ("because each touches more than one source file") does not apply to the live plan, which edits no source file. Not a contradiction: a written plan is allowed below the hard limit. | none, or state that the live plan follows the same route for the record. |

## Self-audit

- Read: the full diff of the two spec files; `git diff` of `APPROVED.md` (only rows S1-S4 added); spec:215-372 (sections 6, 7.1, 7.2, 7.3, 7.4); qa.md:270-300 in the installed copy and line 288 in the source copy; `cmp` of the two qa.md copies (identical).
- Not read in full: spec sections 1-5 and 8-9; covered by grep for "one plan", "one written plan", "phase report", "two parts", "static plan", "live plan". "Phase report" appears at spec:276, 291, 301, 303, 304, 319, 346; each is a live-plan item or a static-to-report item covered by N2/N3. No other "one plan" statement exists.
- Not checked: whether `/sc:implement` can run Orca CLI commands as plan steps from the coordinator session; whether the existing P0 packages (`TASK-WF-orcaWorkerContra-20261102-231950`, `-20261103-012232`) already follow the split. Both are outside the change under review.
- Bias check: told to assume mistakes. The strongest blocking candidates were N5 (one plan vs two plans) and N1 (manual checks). N5 is resolved inside the same paragraph, so a planner does not guess; N1 does not touch P0, so the P0 split still applies. Graded both as notes; a stricter reader could grade N1 blocking for P1/P2 planning.

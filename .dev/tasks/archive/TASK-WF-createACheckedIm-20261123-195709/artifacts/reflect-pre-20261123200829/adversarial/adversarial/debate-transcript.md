# Adversarial Debate Transcript

## Metadata

Mode A, three calibrated review cards, standard depth, focus correctness/coverage/deviation classification. Round 1 was parallel; Round 2 was sequential V1 then V2 then V3 with all preceding statements available on disk. Neutral coordinator did not advocate. Requested class variation and degraded calibration separation do not establish measured runtime model independence. Original cards and all intermediate receipts are retained.

## Round 1: Advocate Statements

### V1 advocate (analyzer)

Read: all 3 variants, diff-analysis.md, template 00_mdtm_template_simple_task.md:15, sc-implement-protocol/refs/qa.md:9 and :356, candidate lines 47/62-66/80-84, validate-lenses-help.txt:1-20.

POSITION: V1's three findings stand, but V1 missed V3's F1 (Task 4 stand-alone). I concede the defect is real and the plan needs a narrow Task 4 edit before execution. V1's PASS verdict should become QUALIFIED PASS-with-required-edit, or FAIL if the loop applies the Blocking (Missing) grade to V3's F1. I will not defend PASS against verified evidence.

STEELMAN V3: Verified. Template line 15 says "its reviewer sees only that task and the Constraints: name every file and source section it needs". qa.md:9 and :356 define the reviewer input as "Ti text + AC ids + global constraints" plus the diff. Candidate line 82 says "same three CLI invocations as Task 2". Line 80 says "their preserved pre-edit observations". Constraints (lines 17-27) list neither the commands nor the baseline files. A Task 4 reviewer cannot tell what the three commands are. Wrapping evidence: V3 is stronger than V1. Captured validate-lenses-help.txt:12-13 shows "--warning-" / "mode", and :16-17 shows "opt-" / "in". V1 offered only the mechanism.

STEELMAN V2: Verified. diagnosability-tasklist.md holds the five pending rows. Constraints and Task 2 correctly preserve them, and no passes are invented. V2's refusal to promote wrapping rests on the captured stale token being intact (scaffold-help.txt:24 and validate-lenses-help.txt:7). That is accurate for the current text only. Its "no remedy needed" does not follow, because the final wording is unobserved.

STRENGTHS of V1: It correctly rejected the filename and placeholder candidates. It grounded the wrapping hazard at __init__.py:71 (width 100). It checked the existing tests for pinned wording. WEAKNESSES: It treated Task 4 as implicitly self-contained and never read the template line 15 or qa.md. It gave no hyphen-split evidence from the captures. Concession: V1's "Task 4 real public outputs backstop the weak negative guard" holds only for the executor holding the whole plan, not for a per-task reviewer.

POINT POSITIONS
- S-001: no variant is preferred. Finding counts differ because the evidence differs.
- S-002: V3 (slice plus governing rules) is a legitimate scope, but V1/V2 full-source coverage found no source gap. The two are complementary.
- S-003: V3 preferred. Governing-rule citation was necessary and V1/V2 omitted it.
- S-004: agreed interpretation. Rejected candidates are Notes, and unverified ones are not findings.
- C-001: V3 preferred. The split is demonstrated in the captures. The wrapped form of the final wording stays unobserved.
- C-002: agreed: V1 and V3 both give the same remedy. Remove all whitespace before the absence check, or join hyphen splits.
- C-003: V3 preferred, qualified as above.
- C-004: V2 preferred for detail. It is immaterial to the verdict.
- C-005: agreed. V1 and V2 searched, V3 checked the five files, and none found a stale-wording pin. I confirmed this myself by grep of tests/. There is no pin.
- X-001: V3 correct. Task 4 is not stand-alone. The Constraints do not supply the commands or baselines. Task 3 line 66 ("Task 2's scaffold help test") and Task 2 line 47 ("named in Task 1") have the same pattern, so V3's F2 is true and stays Medium. Remedy: inline the three commands and the four artifact paths into Task 4.
- X-002: V3 and V1 preferred. The false-pass is real but narrow, and the red witness is unaffected. It stays Medium.
- X-003: QUALIFY. The verdict follows the grade of X-001. The template requirement ("name every file and source section it needs") is a required behaviour of the plan. The affected action is the per-task review of Task 4 acceptance, which cannot run as written. That meets Blocking (Missing) under the severity rule. A fix is a small plan-text edit, not a redesign. V1 and V2 PASS cannot stand alongside it.

ASSUMPTIONS
- A-001: QUALIFY. It was unstated in V1/V2 and is true: the reviewer sees only the task plus Constraints (verified at qa.md:9/:356). It is decisive for X-001.
- A-002: ACCEPT. Red is guarded by the positive JobSpec/custom_prompt_dir assertions, which fail on current text (commands.py:438, :3785).
- A-003: ACCEPT. A fixed basename is form. Task 4 requires a persisted independent report under ./artifacts/.
- A-004: QUALIFY. Hyphenated tokens do wrap (validate-lenses-help.txt:12-13). The target token "--custom-prompt-dir" is not shown wrapped in the current capture. Whether the final wording wraps is unknown. The hazard is real and unobserved, so it is Medium.
- A-005: ACCEPT. Calibration diversity is degraded, which is a real limit on confidence but not on the evidence.

### V2 advocate (qa)

Position: FAIL. I withdraw V2's unconditional PASS. V2 correctly assessed whole-plan source coverage, but omitted a governing requirement about what each task reviewer receives.

V1's strongest case: the source requirements, bounded edits and red/green sequence are sound; final real-command captures protect against relying solely on narrow test assertions. Its weakness is treating that backstop as available without checking the isolated reviewer input.

V3's strongest case: the template expressly requires each task to name its needed files and source sections; the actual reviewer receives only that task and global constraints. Task 4 delegates exact commands and baseline identities to Task 2, which is outside that input. This is a concrete missing review input, not a preference for repeated prose.

V2's remaining strengths: full-source coverage, historical pending-row preservation, explicit independent final review, and rejection of an exact-report-basename blocker. Concessions: V2 did not inspect the governing input boundary; intact current target tokens also do not disprove future wrapping risk.

Authoritative evidence: workflow template:15 requires stand-alone tasks with named inputs; executor qa.md:9 defines task text plus global constraints and diff as reviewer input. Candidate:82 points to Task 2 rather than listing commands; global Constraints do not supply those commands or baseline paths. Lines 80 and 83 likewise leave comparison inputs unnamed. Historical validate-lenses-help.txt:12 and :16 demonstrate hyphenated wrapping, although eventual target-token wrapping remains unobserved.

Counted positions:
- S-001: V3, substantive missing input belongs in findings; narrative assurance missed it.
- S-002: combine V2 complete-source and V3 governing-contract audits.
- S-003: V3, authoritative and independently verified.
- S-004: V3, HIGH / Blocking (Missing), affected action is isolated Task 4 review of matching before/after evidence.
- C-001: V3, general splitting observed; eventual target splitting not.
- C-002: V1/V3, Medium nonblocking follow-up; no invented observed target failure.
- C-003: V3, meaningful whole-plan protection, insufficient stand-alone reviewer inputs.
- C-004: V2, retain explicit pending-row trace.
- C-005: combine compatible evidence; existence/scoped search are not passing tests.
- X-001: V3, absent commands/baseline paths violate the actual boundary.
- X-002: V1/V3 qualified, recordable weakness not demonstrated repaired-output failure.
- X-003: V3, FAIL follows missing required inputs.

Assumptions:
- A-001 ACCEPT: task-plus-constraints boundary explicit, not assumed.
- A-002 ACCEPT: positive field checks protect current red reproduction, not every future malformed correction.
- A-003 ACCEPT: fixed basename changes form, not substance.
- A-004 QUALIFY: hyphen wrapping captured; exact future target behavior unobserved.
- A-005 ACCEPT: degraded class calibration establishes neither correctness nor a defect.

Recommendation: narrow plan-only input correction. No product implementation authorized.

### V3 advocate (refactorer)

Position: V3 is the only card that tested the plan against what the isolated per-task reviewer actually receives. qa.md:9 gives that reviewer "Ti text + AC ids + global constraints" plus the diff and the untracked files the task touched. It does not give sibling tasks. Template:15 makes stand-alone tasks mandatory for this reason.

Steelman V1/V2: the executor holds the whole plan, so the work itself will be correct. Task 4 AC4 (line 82) fixes statuses 0/0/2, requires real public output ("mocked output alone is insufficient"), and requires continued option rejection. public-after.txt is in Task 4's touched set and will contain commands, so a reviewer could rebuild most intent. V2 correctly observes the captured target token is intact (validate-lenses-help.txt:7, scaffold-help.txt:24).

V3 strengths: governing rule and actual input boundary are cited; affected action and one-edit remedy are concrete.

V3 weaknesses: (a) "same three invocations" can be checked for sameness only against public-before.txt, absent from Task 4's touched set and brief. Reviewer can still check statuses/content; blocker is specifically baseline comparability, not all public output verification. (b) F1/F2 grade inconsistency: Task 3 AC2 (line 66) rests on prior scaffold/parser tests absent from its brief and touched set. By the same rule this half of F2 has Missing character like F1.

Concessions: split F2. Task 3 AC2 should be Blocking (Missing); Task 2 body pointer to symbols (line 47) stays Medium because no acceptance check rests on it. For F3/F4, "verified" applies to the mechanism, not target token; consequence stays hypothetical, hence Medium. CliRunner width may differ from captured width.

Positions:
- S-001: V3 layout correct; V2 zero-findings form valid but misses X-001.
- S-002: qualify; complementary assigned-slice/rule and full-source scope.
- S-003: V3 holds, unique governing citations.
- S-004: V3's explicit Missing type and affected action required.
- C-001: qualify, mechanism demonstrated, target split unobserved; V1 wording most precise.
- C-002: V1/V3 agree removing whitespace enough; V2 no-remedy acceptable only for nonblocking follow-up.
- C-003: V3 holds for baseline comparability; V1's backstop still valid for content/statuses.
- C-004: concede V2's pending-row trace is better; V3 claim thinner.
- C-005: neutral, compatible evidence.
- X-001: Task 4 not self-contained; Constraints do not name commands/baselines, falsifier does not trigger.
- X-002: Medium recordable; mechanism captured, consequence needs imperfect implementation.
- X-003: FAIL follows X-001 plus Task 3 AC2 half under consistent grading.

Assumptions:
- A-001 QUALIFY: brief includes untracked touched files, but not sibling-task text.
- A-002 ACCEPT: current help lacks custom_prompt_dir, red still fails.
- A-003 ACCEPT: template:17 makes final review executor-owned; fixed basename is form.
- A-004 QUALIFY: other token splitting shown, target split unobserved, risk Medium.
- A-005 ACCEPT: degraded calibration, C=0.81 does not prove correctness.

Remedy remains narrow: inline Task 4 commands and baseline/red files; name test_cli_registration.py and Task 2 test names in Task 3 AC2.

## Round 2: Rebuttals

### V1 rebuttal

Task 3 AC2: QUALIFY V3's split. Medium, not a second Blocking (Missing). Its affected action is checking validate-help green, scaffold-help still red and parser guard green after the validate edit. Constraints name the only test file, `tests/swarm/test_cli_registration.py`; Task 3 names Task 1's test and `./artifacts/validate-help-red.txt`. The scaffold/parser tests are identifiable by content in the known file. Names do not yet exist because prior tasks only instruct naming clearly, so the plan cannot cite already-existing node ids. A per-task reviewer can read/run that file; no inaccessible file or unnamed public command is required for this intermediate test-state check. Optional remedy: explicitly say scaffold/parser tests in the named test file.

Task 4 F1 remains Blocking (Missing), specifically baseline comparability. Its own text permits checking statuses 0/0/2, option absence, field guidance, related-tests command and report location. It does not supply the three public invocations or identify preserved pre-edit baseline/red files. The "same invocations" check is the unique repaired-state evidence comparison, so the missing inputs are substantive. Inline the commands and baseline paths.

Point positions: S-001/S-002/S-004/C-004/C-005 unchanged; S-003 V3; C-001 V3 for captured mechanism, future target consequence hypothetical/Medium; C-002 remove all whitespace; C-003 V3 qualified to baseline comparison; X-001 V3; X-002 Medium; X-003 FAIL from X-001 alone, no second blocker. All A responses unchanged.

Receipt note: the advocate referenced the Constraints test-file line as 18; the actual file naming is at candidate line 20. This line-number slip changes no quoted contract and is not used as final evidence.

### V2 rebuttal

FAIL remains, from Task 4 alone. Accept V1's distinction; do not promote Task 3 shorthand to Blocking (Missing). Candidate line 20 names the sole regression file; line 66 identifies scaffold-help/parser cases and intermediate outcomes. They can be inspected by content in that file; missing future node names are not missing behavior. Grade MEDIUM / Medium, not a second blocker. No tests are run during review.

Task 4 line 82 requires identity with previous public invocations without naming them or baseline artifact. HIGH / Blocking (Missing) is specifically baseline comparability, not inability to inspect all output.

Final points: S-001 V3 substantive finding; S-002 complementary audits; S-003 V3 verified boundary; S-004 explicit Missing. C-001 general wrapping observed, future target not; C-002 V1/V3 Medium; C-003 V3 limited to baseline comparison; C-004 V2 historical trace; C-005 compatible and no passing-test claim. X-001 V3; X-002 qualified Medium; X-003 FAIL from Task 4 only.

Assumptions: A-001 ACCEPT, A-002 ACCEPT, A-003 ACCEPT, A-004 QUALIFY, A-005 ACCEPT. Prior reasons retained. Recommendation: correct Task 4's commands/comparison inputs only; no Medium-only fix pass or implementation.

### V3 rebuttal

Withdraw the Round 1 promotion of Task 3 AC2 to blocking. It stays Medium; FAIL rests on Task 4 alone. The reviewer receives global Constraints (qa.md:9), whose line 20 names the sole regression file. Candidate line 66 describes scaffold-help and parser-guard cases by behavior. qa.md:31 allows required-read sources outside the touched set. Thus the reviewer can locate both cases in the named file; future node ids cannot be cited before they are chosen. Treating a pointer as the same as absent input was wrong for Task 3.

Task 4 differs: Constraints and Task 4 contain neither the exact three public invocations nor public-before.txt. Line 82's same-invocations comparison cannot be checked in isolation. Blocking (Missing) is baseline comparability, not all public-output checking. Steelman counterargument: commands might be reconstructed from public-after.txt, but that proves only the after run, not identity with the before run without the baseline.

Final points: S-001/S-002/S-004/C-002/C-004/C-005 unchanged. S-003/X-001/C-003 V3, restricted to baseline comparability. C-001 mechanism captured, final wording consequence unobserved. X-002 Medium; X-003 FAIL from Task 4 only. F2 remains one Medium shorthand finding for lines 47/66.

Assumptions: A-001 ACCEPT (replaces QUALIFY), A-002 ACCEPT, A-003 ACCEPT, A-004 QUALIFY, A-005 ACCEPT. Remedy: Task 4 only, inline three commands and public-before/validate-help-red/scaffold-help-red/parser-before paths. No product action.

## Scoring Matrix

Neutral coordinator adjudication from final Round 2 positions (confidence is qualitative agreement, not a product probability):

| Point | Winner | Agreement | Evidence |
|---|---|---|---|
| S-001 | V3 | 2/3, partial | V2/V3 substantive finding layout; V1 neutral |
| S-002 | complementary | 3/3, high | whole-source and governing-boundary audits combine |
| S-003 | V3 | 3/3, high | governing reviewer-input citations verified |
| S-004 | V3, compatible notes | 3/3, high | explicit Missing grade, rejected candidates remain Notes |
| C-001 | V3 mechanism, V1 precision | 3/3, high | general split observed, target future split not observed |
| C-002 | V1/V3 | 3/3, high | whitespace follow-up stays Medium |
| C-003 | V3 narrowed | 3/3, high | baseline comparison missing, content/status checks still possible |
| C-004 | V2 | 3/3, high | five historical rows trace preserved |
| C-005 | compatible | 3/3, high | no stale-wording pin found, no tests claimed run |
| X-001 | V3 | 3/3, high | Task 4 missing comparison inputs |
| X-002 | V1/V3 qualified | 3/3, high | weak guard is Medium only |
| X-003 | V3 | 3/3, high | FAIL from Task 4 alone, second blocker withdrawn |

A-001/002/003/005 accepted; A-004 qualified (mechanism observed, target split unobserved). No globally UNSTATED assumption was promoted into the 12-point denominator.

## Convergence Assessment

11/12 points fully converged = 0.9166666667, exceeding standard threshold 0.80. Average per-point agreement is 0.9722222222; it is NOT substituted for the full-point convergence metric. One unresolved presentation/layout preference (S-001, L2) does not affect the binary FAIL or substantive findings. Base selection uses scores and tiebreaker documented in ./base-selection.md. No additional deep round is required at standard depth.

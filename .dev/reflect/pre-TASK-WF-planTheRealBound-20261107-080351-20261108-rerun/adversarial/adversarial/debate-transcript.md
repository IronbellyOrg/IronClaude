# Adversarial Debate Transcript

## Metadata

- Depth: quick (Round 1 only; Round 2 rebuttals and Round 2.5 invariant probe skipped by design: "Round 2 skipped: depth=quick"; "Round 2.5 (invariant probe) skipped: --depth quick")
- Rounds completed: 1
- Convergence achieved: 40.0% strict (6 of 15 diff points with an identical advocate answer); 46.7% counting X-001 by substance (see Convergence Assessment)
- Convergence threshold: 80% (default)
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (variant 1 haiku class, variant 2 opus class; both run as the read-only reflect-reviewer agent type); orchestrator and scorer: sonnet class (a different class from both debaters)
- Taxonomy coverage: L1 surface S-001, S-002; L2 structural S-003, C-004, C-005, C-006, X-002; L3 state mechanics C-001, C-002, C-003, X-001, A-002..A-005. All three levels addressed by both advocates; no forced round.
- Shared-assumption responses: both advocates answered every one of A-002, A-003, A-004, A-005 (no [OMISSION]).
- Both advocates steelmanned the opposing variant before critiquing it (required by the protocol).

## Round 1: Advocate Statements

### Variant 1 Advocate (haiku class, reflect-reviewer agent) - Round 1 statement

(Returned by the advocate agent; persisted verbatim in structure, condensed in prose, by the parent on receipt at 2026-11-08T02:13Z. Citation keys: P = plan file, H = launch-job-identity.sh, D = docs/designs/sc-issue-launch-level-hook.md, Help = .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/claude-help.txt, Brief = reviewer-briefs/reviewer-1.md.)

**Position summary.** Variant 1 is stronger on the central correctness questions: the plan does not force thirteen Claude starts, and naming required cases does not establish complete evidence collection. It supports the Partial coverage judgments while conceding that its "Drift" labels violate the original review brief and that variant 2 contributes several useful checks.

**Steelman of variant 2.** An observation plan must describe how unsuccessful experiments become honest report entries, not merely prevent a false PASS. Variant 2 gets right: (1) outcome categories are incomplete (runner "blocked", Task 3 "unobserved", report only "observed, controlled or unavailable" with a missing interface for each unavailable result; a timeout or dead child is not a missing interface; P:31, :55, :117); (2) the /clear transition needs explicit starting conditions (P:55, :59); (3) real-child release evidence is potentially obtainable without another Claude start (D:526, :557; H:238-241), conditional on the original child surviving; (4) cleanup cannot rely solely on the working directory, a detached child that changes directory evades the cwd sweep (P:31, :66, :71).

**Strengths claimed.**
1. Rejects a necessary thirteenth start (X-001): P:22 allocates 1+4+4+3 = 12 and says Task 4's shapes "share governed sessions as separate commands"; P:31 requires "one JSON line per run" with real_claude true when that run started Claude; P:66 repeats the three-start limit; P:119 counts those entries. Explicit run identifiers would improve the schema, but their underspecification does not prove thirteen starts.
2. Interactive-budget finding has direct documentary support: plan caps each real run with --max-budget-usd 0.25 (P:22) yet proposes a pty-driven interactive session (P:55); archived help says the option "only works with --print" (Help:131-132). Establishes the documented limitation, not freshly observed behaviour.
3. Process-tree criticism checks the evidence actually collected: the design requires "Bash/Monitor-to-Git and hook process trees" (D:504); Task 2 collects a parent-hop count, selector results and event types (P:44); Task 6 collects selector statuses and refs (P:90, :93); neither collects tree edges.
4. Reparenting finding identifies a missing observable: Task 4 samples "inside the same governed command before it exits" and requires only selector output and wait time (P:66, :69); the helper installs a subreaper (H:292-295).
5. Separates an expected FAIL from a worthless investigation: the report must distinguish observed contract failures from controlled or unavailable evidence and call an empty contract-gap result "contract not yet shown" (P:120).

**Weaknesses identified in variant 2.**
1. Its N-1 confirmation assumes a ledger interpretation the plan does not require; the defensible finding is an identifier/counting ambiguity, not a forced thirteen-start outcome (P:22, :31, :66).
2. "10 of 10 covered" overstates execution-ready coverage: Task 3 does not establish the governed-to-ordinary transition in the reused pty controller; Task 4 does not require evidence that reparenting occurred; tree rows lack specified capture (P:55, :66, :69, :117; D:504).
3. Treating Task 6 as controlled tree coverage is too generous: it logs selector status and destination refs, not tree edges (P:90, :93); adding a real Claude-originated push improves provenance but still collects no tree.
4. Its opening "not meaningful" judgement is too broad: the plan preserves the distinction between a demonstrated separation failure and missing evidence (P:120).

**Concessions.** Variant 1's deviation classification is wrong for the assignment: the brief says "Classify nothing as a deviation class (UC-1 has none)" (Brief:3), so the five "Drift" labels should not be defended. A-03 should be narrowed to: the plan does not establish the pty's before/after controller identity, initial governed binding and post-clear ordinary binding (P:55; D:504, :555); variant 2's Q-1 gives a more concrete transition outline. A-05 establishes missing proof, not inevitable failure. Variant 2 provides broader follow-through (full Tier 1 disposition, report-category correction, conditional release observation, detached-process cleanup) that should be retained.

**Per-diff-point assessment** ("Partial" means incomplete execution-ready satisfaction, not absence of a textual mention).

| Point | Superior | Confidence | Evidence |
|---|---|---|---|
| S-001 | tie | 96 | section order does not resolve the substantive conflicts (P:31, :55, :117) |
| S-002 | 2 | 99 | the assignment forbids deviation classes, so variant 1's "Drift" column is inappropriate (Brief:3) |
| S-003 | 2 | 94 | a complete disposition of inherited findings is more auditable, provided confirmations are checked against the plan (P:22, :31, :66, :119) |
| C-001 | tie | 95 | variant 1 better specifies survivor protection during timeouts; variant 2 adds the cwd-escape (P:31, :35, :66, :71) |
| C-002 | 1 | 98 | archived help limits the budget flag to print mode (Help:131-132; P:22, :55) |
| C-003 | tie | 90 | variant 1 identifies the topology gap, variant 2 specifies the missing initial binding; neither should assume /clear changes identity without evidence (P:55; D:504, :551, :555) |
| C-004 | 1 | 96 | distinguishes parent-hop counts and Git outcome logs from process-tree capture (P:44, :90, :93; D:504) |
| C-005 | 2 | 98 | variant 2 covers blocked and unsuccessful observations that cannot be translated into a missing interface (P:31, :55, :117) |
| C-006 | 1 | 91 | Partial better represents unresolved collection, lifecycle-proof and report-category gaps (P:31, :55, :66, :117) |
| X-001 | 1 | 99 | four shapes share three starts and one ledger line per run, so thirteen starts are not forced (P:22, :31, :66, :119) |
| X-002 | 1 | 91 | all four disputed units have execution-readiness gaps (P:22, :31, :55, :66, :117; D:504) |

X-002 judgements: INF-001 Partial (survivor cleanup conflicts with timeout sweeping; interactive proposal lacks a dollar-cap mechanism; P:22, :31, :35, :55); INF-002 Partial (no acquisition of required process trees, reused-controller transition not established; P:19, :44, :55, :90; D:504); INF-003 Partial (/clear starting conditions and proof of reparenting unspecified; P:55, :66, :69); INF-008 Partial (the report cannot consistently classify all runner outcomes under its permitted row categories; P:31, :55, :117, :120).

**Shared assumption answers.**
- A-002 QUALIFY: the adapter uses the event's session id and does not adapt when it lacks a record (H:429-437); whether /clear and fork produce new ids with no record is unverified, Task 3 must measure them rather than assume (P:55).
- A-003 REJECT: launchability and authentication are not established premises; the plan preserves the nested-session guard, records refusal or missing authentication, and skips further starts (P:22, :31); the conditional path is specified.
- A-004 QUALIFY: the twelve-start and per-run dollar limits bind the present plan (P:22); nothing establishes the owner will never authorize a different bounded experiment, but such authorization must precede execution because the plan may not change once implementation begins (P:25).
- A-005 REJECT: static reading can establish contradictions and missing evidence requirements but not operational executability; the plan requires a preflight and runner self-check (P:31, :34-35), and the review assignment prohibited shell execution (Brief:3).

Not checked by this advocate: live Claude behaviour, current CLI help, authentication, child survival, runner execution.

### Variant 2 Advocate (opus class, reflect-reviewer agent) - Round 1 statement

(Returned by the advocate agent; persisted in structure, condensed in prose, by the parent on receipt at 2026-11-08T02:14Z. Citation keys: v1/v2 = the variant files; help = .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/claude-help.txt; plan:N, helper:N, design:N as in the diff analysis.)

**Position summary.** Variant 2 is the better review: it checks every Tier 1 defect one by one, finds more execution blockers (missing expected statuses around /clear, no report row category for "not observed", no task producing auto-mode or launch-wrapper evidence) and proposes a fix that costs no extra run (observe release with the real surviving child). On X-001 it states the conditions under which the count reaches thirteen. Variant 1 is stronger on two narrower points: the budget flag that only works with --print, and the proof of reparenting.

**Steelman of variant 1.** A-02 has evidence behind it (help:131-132, verified; plan:22 cannot apply to the pty run that plan:55 requires; variant 2 only marked it [INFERRED]). A-01 names a real internal conflict (plan:31 "never signals a surviving job" versus the cwd sweep and plan:35 "a timeout kills the whole process group") and a testable self-check. A-03 reads design:504 correctly (plan:55 SIGKILLs the first process and starts a different pty process, so the originating controller is never reused). A-05 is unique and correct (helper:292-295 installs a subreaper; plan:66 samples before the exit, and nothing proves reparenting happened). Its X-001 reading matches the plan's literal text ("one JSON line per run", plan:22 shares four shapes across three starts). Its stricter coverage verdicts follow a reasonable rule.

**Strengths claimed.**
1. Every Tier 1 defect gets its own verdict (N-1..N-14, each confirmed, refuted or extended with a basis); variant 1 addresses only N-1, N-3, N-4 and M-12, so N-2 and N-5..N-14 get no independent check.
2. Q-1 catches a mislabel and the missing expected statuses at plan:55: if /clear starts a new session id the next call is ordinary, not governed (hook returns without rewriting when sessions/<sid> is missing, helper:435-437; identify returns ordinary when no job record exists, helper:223-225); it gives the order start-as-governed, Bash (governed), /clear, Bash (ordinary) while the old child lives, which also answers variant 1's A-03 controller concern.
3. Q-7 is grounded: help:104-106 says --fork-session creates a new session id, so with no record the fork is ordinary (helper:435-437); without a stated expected status an executor could count the fork toward the decisive separation (plan:59).
4. Q-2 finds a real gap in the row categories: plan:117 says "no unavailable row lacks a named interface", but plan:55 produces "job did not survive the first Claude process ending" and "child identity changed", and plan:31 has a blocked result; none is an interface. The diff analysis credits variant 1 with "not attempted within this budget" but that wording is not in v1.
5. Q-3 covers more than A-04: "auto-mode" and "wrapper" appear in the plan only at plan:114 and :117; no task produces either kind of evidence; variant 1 never mentions auto mode.
6. Q-4 is the only finding that removes a cause of the fixed FAIL for free: release is deleting the session record (design:526, :557), helper:238-241 then returns {'status': 'ordinary', 'reason': 'released'}; doing it after Task 3 and before teardown uses a real child and no extra run.
7. Q-5 checks design:504 "Bash/Monitor-to-Git": Task 6 spends no real Claude run (plan:90), so a Git push started by a real Claude call is never observed; add one inside an existing governed run.
8. Run-budget arithmetic and PASS-reachability are explicit (1+4+4+3 = 12, matching plan:22; holds only if the ledger counts started Claude processes, not cases; PASS blocked by independent causes, Q-4 removes only one).
9. Caught the --disable-slash-commands problem (live_probe.py:253; help:80 "Disable all skills and commands"; plan:31 exempts only --no-session-persistence).

**Weaknesses identified in variant 1.**
1. The X-001 refutation ignores how the ledger is structured: plan:31 has the runner run "one named case at a time" and write a line "with the case id" (singular); plan:22 and :66 put four shapes into three starts; either one line carries two case ids (the schema does not allow it) or one line per shape is written, giving 1+4+4+4 = 13 lines with real_claude true; plan:119 counts those lines and a guard that counts them refuses a legitimate third Task 4 run.
2. Every finding is labelled "Drift" (v1:11-15): A-01 is a contradiction between plan:31 and plan:35, not an unjustified departure from the source.
3. Coverage verdicts double-count: INF-001 is Partial because of A-01 and A-02 again; INF-008 is Partial although Task 8 (plan:114-120) specifies the binary result and the gap lists.
4. Misses the auto-mode gap, the /clear mislabel and the expected fork status.
5. Its claimed confidence (0.90) is higher than its coverage of Tier 1 supports.

**Concessions.** The N-4 budget point: variant 1 grounded it in help:131-132, variant 2 only inferred it. Variant 2 gives no taxonomy category and its hedged severities are off the HIGH/MEDIUM/LOW scale, a real failure on the deviation-classification focus. A-05 was missed and is valid. Q-4's "observed" label can be challenged under plan:23 (the identify call is made by the runner, not by Claude) unless the identify runs inside a later real Claude Bash call. Q-6 depends on the daemon changing directory, which plan:66 does not say. N-1 Medium is somewhat high (the fix is one line per Claude start with a list of case ids). INF-002 "covered with a minor gap" is close to Partial in substance.

**Per-diff-point table.**

| Point | Superior | Confidence | Evidence |
|---|---|---|---|
| S-001 | 2 | 55 | variant 2 adds the run-budget and PASS-reachability sections (v2:30-36) |
| S-002 | 1 | 60 | variant 1 follows the category-plus-severity format; variant 2's hedged severities are off-scale, though variant 1's blanket "Drift" says little |
| S-003 | 2 | 85 | variant 2 gives a verdict for all 14 N-ids; variant 1 covers four |
| C-001 | tie | 55 | variant 1's A-01 gives the better self-check; variant 2 confirms the mechanism and adds the daemon escape (Q-6) |
| C-002 | 1 | 85 | variant 1 cites help:131-132 (verified); variant 2 marked it [INFERRED] |
| C-003 | 2 | 60 | Q-1 shows the "governed Bash command" after /clear is mislabelled and fixes the controller concern; Q-7 adds the fork status |
| C-004 | 2 | 65 | only variant 2 catches auto mode and offers Q-5's budget-neutral real push; variant 1's tree snapshots are complementary |
| C-005 | 2 | 75 | Q-2: "job did not survive" cannot meet plan:117's named-interface rule |
| C-006 | 2 | 60 | variant 2 keeps coverage separate from defects; variant 1's Partial verdicts repeat its own findings |
| X-001 | 2 | 60 | thirteen starts are not forced (variant 1 is right on that) but one case id per line, four shapes in three starts and the line count at plan:119 let the guard refuse a legitimate run |
| X-002 | 2 | 60 | INF-003 and INF-008 covered; INF-001 and INF-002 covered with defects, which belong in findings |

**Shared-assumption answers.** A-002 QUALIFY (fork: ACCEPT, help:104-106 and helper:435-437; /clear new session id unverified and --disable-slash-commands may block /clear; state the expected status for both outcomes). A-003 QUALIFY (neither card needs it true; the plan handles a refusal at plan:22, :31, :47, :66, :101; if false the report is a FAIL with only evidence gaps, the N-12 value risk). A-004 QUALIFY (the twelve-run cap binds by plan:22 and plan:25; the 0.25 USD cap cannot be applied mechanically to the pty run; the owner can still choose "unavailable" or a separately bounded interactive run before execution). A-005 QUALIFY (static reading is enough for every finding both cards make since they rest on contradictions in the text; it cannot settle pty driving, nested-launch refusal or survival after SIGKILL; the plan's preflight is its own dry run).

Not checked by this advocate: whether /clear changes the session id or how the pty session behaves; the archived help may be out of date for the installed CLI.

## Scoring Matrix

Winner determination by the orchestrator (sonnet class) from the two Round 1 statements and the evidence each cites; "Agreed" = both advocates gave the same answer. No Round 2 exists, so no concession boost applies beyond what the advocates conceded in Round 1.

| Diff point | Advocate 1 | Advocate 2 | Agreed | Winner | Confidence | Evidence summary |
|---|---|---|---|---|---|---|
| S-001 | tie (96) | 2 (55) | no | tie | 60 | section order does not decide any substantive finding |
| S-002 | 2 (99) | 1 (60) | no | tie | 60 | variant 1's "Drift" category violates the brief (reviewer-briefs/reviewer-1.md:3, conceded); variant 2's hedged severities are off the HIGH/MEDIUM/LOW scale (conceded); merged output uses the three-level scale only |
| S-003 | 2 (94) | 2 (85) | yes | variant 2 | 90 | one verdict per Tier 1 defect is auditable; both advocates agree |
| C-001 | tie (95) | tie (55) | yes | tie | 85 | merge A-01's self-check with Q-6's recorded-pid stop |
| C-002 | 1 (98) | 1 (85) | yes | variant 1 | 92 | help file lines 131-132 verified by the calibrators and both advocates |
| C-003 | tie (90) | 2 (60) | no | variant 2 | 70 | Q-1 gives the ordered calls and expected statuses; Q-7 the fork status (help:104-106, helper:435-437); advocate 1 conceded Q-1 is more concrete; A-03's different-controller point is kept |
| C-004 | 1 (96) | 2 (65) | no | tie | 60 | complementary: tree-edge capture (variant 1) and a bounded wrapper/auto-mode observation or "not run" label plus a real governed Git push (variant 2) |
| C-005 | 2 (98) | 2 (75) | yes | variant 2 | 90 | plan:55 and plan:31 produce outcomes that are not a missing interface; a "not observed (reason)" row category is needed |
| C-006 | 1 (91) | 2 (60) | no | tie | 55 | INF-003 Partial (both /clear topology and reparenting unproven); INF-001, INF-002, INF-008 covered with defects tracked as findings |
| X-001 | 1 (99) | 2 (60) | no (conclusions agree) | tie | 75 | both agree thirteen starts are not forced (plan:22 shares four shapes across three starts); both agree the ledger cannot be audited against the cap without a run id; variant 2's one-case-id-per-line reading is plausible but not forced |
| X-002 | 1 (91) | 2 (60) | no | tie | 55 | see C-006 |
| A-002 | QUALIFY | QUALIFY | yes | QUALIFY | 85 | adapter keys on the event's session id (helper:429-437); fork gets a new id (help:104-106); /clear unverified |
| A-003 | REJECT | QUALIFY | no | QUALIFY | 70 | the plan specifies the refusal path (plan:22, :31) but an executor started inside Claude Code risks an empty FAIL (value risk) |
| A-004 | QUALIFY | QUALIFY | yes | QUALIFY | 85 | caps bind the executor; the owner can choose before execution |
| A-005 | REJECT | QUALIFY | no | QUALIFY | 65 | static reading suffices for textual contradictions, not for runtime behaviour |

## Convergence Assessment

- Points resolved: 6 of 15 with an identical advocate answer (S-003, C-001, C-002, C-005, A-002, A-004) = 40.0% strict; counting X-001, where the advocates' substantive conclusions match and only the framing of the "winner" differs, 7 of 15 = 46.7%.
- Threshold: 80%
- Status: NOT_CONVERGED (the depth is quick, so no rebuttal round could close the gaps; no HIGH unaddressed invariant gate applies because Round 2.5 was skipped)
- Unresolved points: S-001, S-002, C-003, C-004, C-006, X-001, X-002, A-003, A-005
- Reading the result: no unresolved pair is mutually exclusive. S-001 and S-002 are presentation; C-004 and C-006/X-002 are complementary or a judgement about what "Partial" means; X-001's facts are agreed. The merged verdict therefore takes the union of the valid findings, with the resolutions in the scoring matrix. A standard-depth run would add rebuttals and the invariant probe; it was not run.

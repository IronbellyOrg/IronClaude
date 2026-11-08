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

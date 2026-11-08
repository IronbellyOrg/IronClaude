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

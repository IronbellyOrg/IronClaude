# Debate transcript, ROUND 2 (rebuttals), advocate for VARIANT 1 (reviewer 1, analyzer)

Advocate: variant 1. Strategy: steelman. Date: 2026-11-10.
Abbreviations as in round 1: TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; R2-BR / R2-DM = the second revision's BUILD-REQUEST.md / delta-manifest.md; R1-DM = the first revision's delta-manifest.md; DA = `ADV/diff-analysis.md`; BASE = `.../revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md`; SK = `/home/coder/.claude/skills/task/SKILL.md`.
Read this round: all three Round 1 transcripts (round1-v1, round1-v2, round1-v3), DA, the three original cards, and the plan lines quoted below (re-read from disk now). New checks I ran are marked "checked".

## 0. What changed since round 1 (one paragraph)

Round 1 agreement is now wide: V1, V2 and V3 all accept that 7.17 (TL:1274) is a real, pre-existing, out-of-surface defect at HIGH if the branch fires; that R1-F1, R1-F2, R1-F4 and R1-F5 are LOW; that R3-F1 is closed (matrix line 7 reads `run: 4`); and that R3-F2 is not a defect (V3 withdrew it). Three disputes remain: (1) 7.24 at H or M, and what a correct approved run actually reaches (V3 says a named owner escalation at TL:1412, I said a monotonicity halt at TL:1384); (2) whether 7.17 has any exit inside the 85 labels; (3) the sha256 baseline finding (V1 M, V2 M, V3 L). I also answer the duplicate question. Result: I move on (3) (M down to L, new evidence below), I correct V3's escalation claim (it is mostly wrong, section 1), but I also lower my own certainty on 7.24 because a new fact (TL:1271) shows the approved path needs a plan extension anyway.

## 1. Dispute A: 7.24 lens defect (R2-F2 / U-008), H or M

### 1.1 Strongest version of V3's position (steelman)

V3 round 1 section 5: the lens finding is a nuisance, not a failure. A BLOCKING finding enters 7.29, the 7.30 fixer must leave a finding that "needs the owner or a new capture" OPEN, and "After two cycles, 7.37 step (d) (TL:1412) names the exit: ... escalate the open BLOCKING and MAJOR findings to the user." So the plan "has a designed owner escalation for exactly this kind of leftover finding", which makes it a workaround-bearing defect, MEDIUM. V3 also says the finding is unreachable on the default and refusal paths.

### 1.2 Test against the files

What is true in V3's position (verbatim):
- `TL:1321`: "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10 ... Each breach is BLOCKING." and "that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run".
- `TL:1271` (7.17 step 2, approval): "the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file; the 7.16 forbidden list and its grep ... updated to allow the approved argv and a re-capture of it". Item 7.24 is not on that list (checked: the list names DESIGN edit item, 8.10, 10.3, 7.16 and the R5 re-run).
- `TL:1363` (7.30): "it may never change a decision's `Chosen:` line or re-run a live Orca command. A finding that needs the owner or a new capture is left OPEN with that reason."
- `TL:195`, the HALT rule: "set frontmatter `status` to "⚪ Blocked", fill `blocker_reason` with the halt line ... STOP, and do not tick the item." Every HALT in the plan therefore stops the task for the owner. I concede this much: no path through 7.33 or 7.37 produces a silent wrong PASS. The failure is fail-closed.
- Refusal and default paths: `TL:1272` "A refusal resumes with the allowlist unchanged ... 8.10 then keeps `ALLOWED_ORCA` at exactly 10", so the lens passes there. Conceded.

What is false in V3's position: that a stuck lens finding reaches the named escalation. Trace of the decision rules (verbatim):
- `TL:1356` (7.29, rule 1): "two findings are one finding when they name the same `file:line` and the same defect"; rule 4: "`F_0` = the ids of every BLOCKING or MAJOR finding". A lens breach of 7.24 is in `F_0`.
- `TL:1384` (7.33): "(b) Monotonicity: if `|F_1| >= |F_0|`, write `[HALT-MONOTONICITY] |F|=<n>` ... and apply the HALT rule". The text of (b) contains no "escalate" word and no finding ids.
- `TL:1412` (7.37): "(b) Monotonicity: `|F_2| >= |F_1|` gives `[HALT-MONOTONICITY] ...`" is tested BEFORE "(d) Otherwise the hard cap: write `Decisions gate: HALT after 2 fix cycles, open findings: <ids>` ... and escalate the open BLOCKING and MAJOR findings to the user." The 7.33 context states the order: "Halt order on every cycle transition: regression first, then monotonicity, then the hard cap."

Case table (S = the stuck lens finding or findings, which no fixer may clear; R = other findings a fixer can clear):

| Case | What 7.33 / 7.37 do | Reaches (d) escalation? |
|---|---|---|
| A. `F_0` = S only | cycle 1 leaves S OPEN, `F_1` = S, `|F_1|` >= `|F_0|`, so `[HALT-MONOTONICITY]` at TL:1384 (b) | no |
| B. `F_0` = S + R, R fully fixed in cycle 1 | `|F_1|` < `|F_0|`, continue to cycle 2; `F_2` = S, `|F_2|` >= `|F_1|`, so `[HALT-MONOTONICITY]` at TL:1412 (b) | no |
| C. `F_0` = S + R, R partly fixed in cycle 1 and cycle 2 strictly reduces but does not clear | (d) fires | yes |

So V3's "named exit" exists only in case C, which needs fixable findings that survive cycle 1 and shrink again in cycle 2. In the first two cases the run ends on a monotonicity HALT that says nothing about the owner. I withdraw nothing here: my round 1 chain (stuck finding -> HALT-MONOTONICITY at 7.33) is the typical outcome, and V3's reading of 7.37(d) as the exit is incorrect for it. A correct approved run does not reach an escalation text; it reaches a plan-defined HALT with a ledger row.

One consequence I did not state in round 1 (marked [INFERRED], no run): the lens report's "smallest fix" will point at the ten-template rule or the DESIGN section 7.3 ALLOWED_ORCA set. `TL:1363` lets the single fixer edit "the R5 DESIGN edits listed in item 6.3 (sections 7.3, 11, 12, 13 and 15.1, ...)" (checked) and forbids only "Never change revision authority/design append/decision choice". A fixer that follows the lens could revert the approved template in DESIGN 7.3. The prohibition probably blocks it, but the lens defect is the cause of that pressure. That is a second failure mode, not just a halt.

### 1.3 New fact that cuts the other way (concession)

`TL:1271` and `TL:1268` say an approval triggers "a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate" and "a re-run of the R5 review gate (6.5 to 6.22) over the new edit". Checked: no such item exists in the plan (`DESIGN edit item` occurs only on TL:1268 and TL:1271; the string `OQ-17` has 24 hits and none is an item that edits DESIGN). So the approval path cannot run as written; it needs new items from the owner or a re-run of `/task-builder` (the same words the plan uses for other plan gaps, TL:1154). At that moment the person adding the DESIGN edit item can also fix 7.24. This lowers the chance that the lens defect bites an unrevised plan. It does not remove the defect: the follow-up list at TL:1271 omits 7.24, so the extension author would have to find it by reading.

### 1.4 Consistency argument

V3 gives H to 7.17 because "7.17 has no named exit" and M to 7.24 because it has one. By the case table, 7.24 has no named exit in cases A and B either. 7.17 has a stronger claim to H on a different ground: its defect bites the refusal path, which is fully planned (`TL:1272` "A refusal resumes with the allowlist unchanged, and the same step records the refusal in ... 1.0a-facts.md"), while 7.24 bites only the approval path, which is not fully planned (1.3).

### 1.5 Settlement

The scale in the prompt: HIGH = a correct run fails or a required check is lost; MEDIUM = real impact with a workaround. For 7.24: a correct approved run cannot reach `Decisions gate: PASS` without a human override (typical cases A and B), and the plan names no override. The workaround (owner rules on the finding; verifier marks it closed by judgment) is the same kind that exists for 7.17. I therefore keep H, conditional on an approved change, but at lower confidence than round 1 (0.8 to 0.55). If the owner reads "a HALT is a designed owner stop" (TL:195) as the exit, the right label is M, and I would not fight that. Either way the repair is one clause inside the 85 labels (7.24 is an R1 row: `R1-DM:27` "| 7.24 | Read-only safety lens | Add scoped inputs; ..."; R2 changed only TL:1320, `qa/preservation-check.json` `changed_by_label["7.24"] == [1320]`, checked), so the severity does not change what to do.

POINT U-008: winner V2 on the fact, confidence 0.55, final severity H (conditional on an approved change; M is defensible), in-scope-of-85 yes

## 2. Dispute B: does 7.17 (R2-F1 / U-007) have any exit inside the 85 labels

### 2.1 Strongest version of the in-scope claim (steelman)

R2-BR:17 allows "A short additive note ... appended after the existing R1 note (TL:3010+)". The plan already uses an appended note to override preamble prose without editing it: `TL:3018` "The Phase 7 generic "RESOLVED resets status" prose does not bypass revised 7.10's stricter authority/implementation gate." So a note could say: "7.17 Verification's PENDING checks apply at the first halt; after the resume the completion state is RESOLVED, filled fields, no open HALT." That would be inside the surface.

### 2.2 Test

- 7.17 is not an allowed label: `grep -c '7\.17'` on R2-DM and on R1-DM printed 0 and 0 (checked), and `qa/preservation-check.json` has no `"7.17"` key (checked: its only `7.2x` entry in the label map is `"7.24"` at line 172). The 85 are the 82 R1 labels plus 13.1, 8.19, 10.5 (R2-BR:17). So no edit of TL:1266-1275 is allowed.
- The defect text is intact and consistent with round 1: `TL:1274` "confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines; ... and that the task is halted (frontmatter `status` and `blocker_reason` set by the HALT rule) before any step 1.2 item runs." against `TL:1272` "it sets `status: RESOLVED` ... resets the task `status` to "🟠 Doing", and clears `blocker_reason`" and `TL:1275` "The facts file is written with no open HALT."
- New point on timing (strengthens R2-F1): the item STOPS at the first halt. `TL:1270`: "It then HALTs before step 1.2 under the Phase 7 preamble Branch 1 rule", and `TL:1143`: "Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule ... and STOPS". So the Verification line is first read after the resume, when the file is no longer PENDING. The "first-halt reading" that softens R2-F1 describes a moment at which the executor never reaches Verification. I concede this to V3 and V2.
- Resume re-enters the item: `SK:535` "Find the first unchecked item — Scan for the first `- [ ]` item. This is where execution resumes." and `SK:537` "Start the F1 loop from the first unchecked item". `SK:538` ("If an item's output file exists, that work is done") helps the Action, not an unticked Verification.
- Why the note is only a mitigation: `TL:3016` says "This note is not an executable checklist." and the R2 design for the same kind of fix (F-09) pairs the note with a pointer inside the item: `R2-DM:21` "| F-09 | LOW | 1210 | Pointer: this item's Branches replace the Phase 7 preamble Branches 1 and 2 ...". For 7.17 no pointer can be written. An executor running the F1 loop on 7.17 reads the item body; a tail note at line 3010+ is not in its path, and the 7.17 Verification stays literally false after the resume.

### 2.3 Settlement

A real fix needs a new owner authorization naming 7.17 (split the Verification into a first-halt check and a resolved-resume check; skip Action step 1 when the decision file exists, DA O-001). Inside the 85 the only available step is a note that states the intended reading. I count it as a mitigation, not as a fix, and I would label the defect "open until 7.17 is authorized". I also agree 7.24 can be done as an in-surface clause without any new authorization, so only the 7.17 half needs the owner.

POINT U-007: winner V2, confidence 0.9, final severity H (conditional on the OQ-17/OQ-18 branch firing; bites on the refusal path too), in-scope-of-85 no

POINT O-001: winner V2, confidence 0.55, final severity M, in-scope-of-85 no (same item, same gap seen from the Action side; the literal re-run of step 1 is [INFERRED])

## 3. Dispute C: the sha256-baseline finding (R1-F3 / U-003 / X-003)

### 3.1 Strongest version of the opposing positions

V3 (L): the F-07 requirement is met, the orchestrator holds the sums in its session, and "it is the house pattern of six items, not an R2 slip". V2 (conceded M): the durable baseline sits in a file the fix agent is told to write, and session memory alone is a weak audit trail.

### 3.2 Test (new checks)

- Text: `TL:1363` "record the output of `sha256sum ...` in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md` ...; after the agent returns, re-run that command first and append a PASS line only when all four sums are unchanged." and "Pass it ... the output path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`." and the fix preamble "Write a fix log listing each finding id, the change, and the `file:line` after the change." Same shape at `TL:1391` with `fix-log-cycle2.md`. The collision is real.
- Origin (checked by hashing each line against BASE): TL:1363 and TL:1391 `CHANGED_BY_R2`; TL:2614, 2642, 2705 and 2733 `SAME_AS_R2_BASELINE`. Those four 14.x lines carry the identical pattern: `TL:2614` "Before spawning the agent, record the output of `sha256sum docs/designs/orchestrator-mode.md ... BUILD-REQUEST.md` in the fix log". So R2 copied a pattern that already stood in four R1-era items; it did not invent the weakness. BASE has `sha256sum` only on lines 2614, 2642, 2705 and 2733 (4 hits, checked).
- Failure mode is fail-closed, not silent: if the agent replaces the log, there is no baseline line to compare, so the PASS line that 7.30 Verification needs (`TL:1365` "every appended re-check line is PASS") cannot honestly be appended. The orchestrator can still compare against its own copy of the sums. The guard targets files the fixer may not change ("Never change revision authority/design append/decision choice", TL:1363), so the loss is an audit-trail weakness, not a lost decision.
- I could not verify in the files how often an `rf-qa` fix agent replaces an existing output file; that part of my round 1 argument ("an ordinary Write replaces the file") is an assumption, not a file fact. I withdraw it as the basis for M.

### 3.3 Settlement

Severity falls to L (Medium-Low is the floor). Reasons: requirement F-07 is met as written (sums before the spawn, compared after: R2-BR:31 "record sha256 sums ... BEFORE the spawn and re-run after"); house pattern in four untouched items; fail-closed. Scope: 7.30 and 7.34 are R1 rows changed by R2, and 14.25, 14.29, 14.38 and 14.42 are R1 rows too, so a consistent fix (a separate orchestrator-owned sums file, for example `sha256-before-cycleN.txt`) is inside the 85 on all six lines. Related: 13.18 and 13.22 have no guard at all (R3-F3, `sha256sum` count on TL:2384 and TL:2412 is 0, checked in round 1) and are a different defect in the same family.

POINT U-003: winner V3 on severity, V1 on the fact, confidence 0.6, final severity L, in-scope-of-85 yes
POINT C-003: winner V3 on severity, V1 on the fact, confidence 0.6, final severity L, in-scope-of-85 yes
POINT X-003: winner V3, confidence 0.6, final severity L ("fixed with a residual"; my round 1 label "partial" is withdrawn), in-scope-of-85 yes

## 4. Dispute D: is any card finding a duplicate of another

Test rule: the plan's own dedup rule at `TL:1356`: "two findings are one finding when they name the same `file:line` and the same defect". Candidate pairs:

| Pair | Same lines? | Same defect? | Verdict |
|---|---|---|---|
| R1-F3 (baseline in the fix-log file) and R1-F4 (re-run list omits the section check; no hash on the 7.10 result file) | yes, TL:1363 and TL:1391 | no: one is where the baseline is stored, the other is which files the re-run covers. Checked: `TL:1363` contains 0 hits of "Execution authorization", while `TL:1293` has the `grep -c '^## Execution authorization (verbatim)'` command | not duplicates; one edit to 7.30/7.34 can close both, so treat as a bundled remedy |
| R1-F3 and R3-F3 (13.18/13.22 have no sha guard) | no (TL:1363/1391 vs TL:2384/2412) | no (baseline durability vs absence of a guard) | not duplicates; same family (guard parity) |
| R2-F1 (7.17 Verification) and R2-F2 (7.24 lens) | no (TL:1274-1275 vs TL:1321) | no: different consumer, different consequence; common cause is the optional branch not being propagated, but 7.17's own step 2 list (TL:1271) omits 7.24, which belongs to R2-F2 only | not duplicates; two repairs, one in-surface and one out |
| R2-F1 and O-001 (adjudicator observation, not a card finding) | same item (TL:1270 vs TL:1274) | Action-side twin of the same resume gap | fold O-001 into R2-F1's repair; not a card duplicate |
| R1-F2 (7.10 retry writes a second section) and O-001 | no | same pattern (resume without idempotence), different item | not duplicates |
| R1-F1 (7.20 match target) and R1-F2 (7.10 re-run) | no (TL:1293 vs TL:1210) | no | not duplicates |
| R3-F1 (matrix) and anything | n.a. | n.a. | closed |

Result: no card finding is a duplicate of another under the plan's own rule. Two bundles are worth carrying into the merge: R1-F3 + R1-F4 (one edit to 7.30/7.34) and R2-F1 + O-001 (one 7.17 authorization).

POINT DUP-1 (R1-F3 vs R1-F4): winner none, confidence 0.8, final severity L, in-scope-of-85 yes (bundle the remedy, keep both findings)
POINT DUP-2 (R2-F1 vs R2-F2): winner none, confidence 0.85, final severity H, in-scope-of-85 no for R2-F1, yes for R2-F2 (two findings)
POINT DUP-3 (R1-F3 vs R3-F3): winner none, confidence 0.85, final severity L, in-scope-of-85 yes (two findings, one family)

## 5. Remaining points, short rebuttals

- **R1-F1, R1-F2, R1-F4, R1-F5** (my own): I hold the round 1 downgrades to LOW. R1-F4 stays LOW because the lead-in "re-run the item 7.20 commands" can be read as the full 7.20 set (V2's point) though the enumerated list omits the section grep; R1-F2 stays LOW because `TL:1210` already says "look first for the `## Execution authorization (verbatim)` section in the result file named in Output, because a resumed session does not remember the chat" and `TL:1211` says "later content is appended below it, never overwriting it". V3's round 1 reading of these is correct.
- **R3-F2 / U-011**: V3 withdrew it. I agree: `TL:2265` reads "(DESIGN line 716 at the time of this revision; item 5.2 aligned it with master's 5-minute sweep bound ...)" and "the DESIGN text wins" (both checked on line 2265). True as written, history only, no defect.
- **R3-F1 / A-008 / O-003**: closed on disk for all three (V2 and V3 quote `run: 4` on matrix line 7). I withdraw nothing; I add that V3's reading was accurate at the time (A-008 contradicted for this file only).
- **R3-F3 / U-012**: stays L, inside the 85 (13.18 and 13.22 are R1 rows, Action lines not changed by R2, V3 round 1 checked), not an F-07 target. Agreed with V2 and V3.
- **A-002/A-003** (literal vs careful executor): I accept V3's middle rule. Use the literal reading where the plan has no resume text for the case (7.17 Verification and Action step 1), the careful reading where it does (7.10 Branch 1, TL:1210). The 7.17 timing fact in section 2.2 adds support, because Verification is first read after the resume.
- **A-004** (reachability): nobody can quantify it from the files. DESIGN:995 gives "no cursor template" as the default and DESIGN:559 says the template "is added only after step 1.0a captures the cursor field" (checked). Keep both 7.17 and 7.24 conditional. Neither blocks starting 7.10.
- **O-002** (stale DESIGN line numbers in 7.17): `TL:1267` cites lines 552, 550, 971, 973; the sentences now sit at DESIGN:559, 557, 993, 995 (checked with a grep of the quoted text). Navigation only, L, outside the 85 (7.17).
- **S-001**: with the settlements above the profile that matches the files is two conditional H (7.17 certain, 7.24 at the H/M edge), no clean M, and a tail of L. V1's severities ran one level high on four findings (R1-F1, F2, F3, F5); V2's HIGH on 7.24 is arguable but defensible; V3's lows on 7.24-related points were too low only because it read the escalation text as reachable.

## 6. Final table of POINT lines (every contested id)

Structural and content points
POINT S-001: winner V2, confidence 0.8, final severity H, in-scope-of-85 n.a.
POINT S-002: winner none, confidence 0.6, final severity L, in-scope-of-85 n.a.
POINT S-003: winner V2, confidence 0.7, final severity L, in-scope-of-85 n.a.
POINT S-004: winner V3, confidence 0.65, final severity L, in-scope-of-85 n.a.
POINT S-005: winner none, confidence 0.55, final severity L, in-scope-of-85 n.a. (7.30/7.34 sums file and 7.24 clause: yes; 7.17 split: no)
POINT S-006: winner none, confidence 0.8, final severity L, in-scope-of-85 n.a.
POINT S-007: winner none, confidence 0.8, final severity L, in-scope-of-85 n.a.
POINT C-001: winner V2, confidence 0.8, final severity H, in-scope-of-85 no ("fixed (scope) / open (branch)")
POINT C-002: winner V3, confidence 0.7, final severity L, in-scope-of-85 yes
POINT C-003: winner V3 on severity (V1 on the fact), confidence 0.6, final severity L, in-scope-of-85 yes
POINT C-004: winner V3, confidence 0.7, final severity L, in-scope-of-85 yes
POINT C-005: winner V2, confidence 0.85, final severity H, in-scope-of-85 no (7.17 needs an owner extension; 7.24 and 13.18/13.22 are inside)
POINT C-006: winner V2, confidence 0.9, final severity H, in-scope-of-85 n.a.
POINT C-007: winner none, confidence 0.7, final severity L, in-scope-of-85 n.a.

Contradictions
POINT X-001: winner V2 on the end-to-end result (V1 and V3 on F-01's own targets), confidence 0.8, final severity H, in-scope-of-85 no
POINT X-002: winner V3, confidence 0.7, final severity L, in-scope-of-85 yes
POINT X-003: winner V3, confidence 0.6, final severity L, in-scope-of-85 yes
POINT X-004: winner V2, confidence 0.9, final severity H, in-scope-of-85 n.a. (7.17 no, 7.24 yes)
POINT X-005: winner V3 and V2 on the conclusion, V1 on half of the premise, confidence 0.7, final severity L, in-scope-of-85 yes
POINT X-006: winner V3, confidence 0.9, final severity L, in-scope-of-85 n.a. (closed on disk)
POINT X-007: winner V3 on severity, V1 on the fact, confidence 0.7, final severity L, in-scope-of-85 yes

Unique contributions
POINT U-001: winner none, confidence 0.7, final severity L, in-scope-of-85 yes
POINT U-002: winner none, confidence 0.7, final severity L, in-scope-of-85 yes
POINT U-003: winner V3 on severity, V1 on the fact, confidence 0.6, final severity L, in-scope-of-85 yes
POINT U-004: winner V1, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-005: winner V3 on severity, V1 on the fact, confidence 0.7, final severity L, in-scope-of-85 yes
POINT U-006: winner V1, confidence 0.9, final severity L, in-scope-of-85 n.a. (confirms expect 6; not a defect)
POINT U-007: winner V2, confidence 0.9, final severity H, in-scope-of-85 no
POINT U-008: winner V2, confidence 0.55, final severity H (M defensible), in-scope-of-85 yes
POINT U-009: winner V2, confidence 0.85, final severity L, in-scope-of-85 n.a.
POINT U-010: winner V3, confidence 0.9, final severity L, in-scope-of-85 n.a. (closed)
POINT U-011: winner none, confidence 0.7, final severity L, in-scope-of-85 yes (not a defect; V3 withdrew it)
POINT U-012: winner V3, confidence 0.7, final severity L, in-scope-of-85 yes
POINT U-013: winner V3, confidence 0.75, final severity L, in-scope-of-85 n.a.

Shared assumptions, observations and the duplicate question
POINT A-002: winner none (middle rule: literal where the plan has no resume text), confidence 0.65, final severity M, in-scope-of-85 n.a.
POINT A-003: winner none, confidence 0.65, final severity M, in-scope-of-85 n.a.
POINT A-004: winner none, confidence 0.55, final severity M, in-scope-of-85 n.a.
POINT A-008: winner V3, confidence 0.9, final severity L, in-scope-of-85 n.a.
POINT O-001: winner V2, confidence 0.55, final severity M, in-scope-of-85 no
POINT O-002: winner none, confidence 0.85, final severity L, in-scope-of-85 no
POINT O-003: winner V3, confidence 0.85, final severity L, in-scope-of-85 n.a. (no longer true on disk)
POINT DUP-1: winner none, confidence 0.8, final severity L, in-scope-of-85 yes
POINT DUP-2: winner none, confidence 0.85, final severity H, in-scope-of-85 no (R2-F1) and yes (R2-F2)
POINT DUP-3: winner none, confidence 0.85, final severity L, in-scope-of-85 yes

## 7. What V1 concedes and what it keeps (round 2)

Concedes: missed 7.17 and read 7.24 only as a lens item; four severities ran high; the "stub-first Write replaces the log" premise for R1-F3 is an assumption I cannot prove from the files, so R1-F3 drops to L; "Today 7.20 returns PASS" was overstated.
Keeps: R1-F3 and R1-F4 are real, distinct, and fixable in one edit to 7.30/7.34 (plus the four 14.x lines for consistency); R1-F4's omission is confirmed (0 hits of "Execution authorization" on TL:1363); V3's reading of TL:1412 (d) as the exit for a stuck lens finding is wrong in the typical cases (A and B above), so 7.24 stays at the H/M edge and must be fixed either way.
Not verified this round: the T1 card, the 7.22/7.25 row-count wording, the 7.27-7.29 and 7.31-7.33 bodies beyond the lines quoted, and any behaviour of a live fix agent.

# Debate consensus after Round 2 (sc:adversarial Mode A, inside sc:reflect UC-1 pre-execution, run 4)

- Written: 2026-11-10, by the debate orchestrator's analytical agent (not an advocate).
- Inputs read in full: `ADV/diff-analysis.md`, `ADV/variant-{1,2,3}-original.md`, `ADV/debate/round1-v{1,2,3}.md`, `ADV/debate/round2-v{1,2,3}.md`; protocol `~/.claude/skills/sc-adversarial-protocol/refs/debate-protocol.md:154-165` and `~/.claude/skills/sc-adversarial-protocol/SKILL.md:1385-1501`.
- Aliases. ADV = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/plan-defect-fixes-20261110/reflect/pre/adversarial`. TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (sha256 prefix `eb291f0bdd1a7871`, 3020 lines, mtime 2026-11-10 05:14:11, checked this run). BASE = `.../revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md`. R1-DM = `.../revisions/chat-output-exception-20261109-133150/delta-manifest.md`. R2-BR = `.../revisions/plan-defect-fixes-20261110/BUILD-REQUEST.md`. PC = `.../revisions/plan-defect-fixes-20261110/qa/preservation-check.json`. MX = `.../reflect/pre/coverage-matrix.yaml`. SK = `/home/coder/.claude/skills/task/SKILL.md`. DESIGN = `docs/designs/orchestrator-mode.md`. R1v1 etc. = `ADV/debate/round1-v1.md` etc.
- Severity scale (caller): HIGH = a correct run fails or a required check is lost; MEDIUM = real impact with a workaround; LOW = minor.
- Edit surface: the 85 labels (R2-BR:17 "Allowed: the 82 labels of R1 (`../chat-output-exception-20261109-133150/delta-manifest.md`, DM:21-117) plus 13.1, 8.19 and 10.5."); R2-BR:18 "only existing Context/Action/Output/Verification/Completion-gate lines of those labels may change, each stays ONE physical line". 7.17 is outside it.

## 1. Merged findings (one finding per defect)

Severity is the final one after my own file check (section 4). "Conv." = Round 2 severity votes of the three advocates (V1 adv / V2 adv / V3 adv). R2v1 = `ADV/debate/round2-v1.md`, R2v2 and R2v3 likewise.

| Merged id | Defect | Folds in | Final severity | Conv. (R2 severity) | In the 85? | Origin |
|---|---|---|---|---|---|---|
| M-01 | 7.17 Verification (TL:1274) demands PENDING records, empty owner lines and a halted task, while the resume (TL:1272) sets RESOLVED and clears the halt, and the Completion gate (TL:1275) demands no open HALT; Action step 1 (TL:1270) has no skip when the decision file already exists | R2-F1, O-001 | HIGH, conditional on the owner allowlist branch firing (approval or refusal) | H / H / H (R2v1:75, R2v2:119, R2v3:104) | no | pre-existing (TL:1266-1275 byte-identical to BASE, checked) |
| M-02 | 7.24 lens (TL:1321) hard-codes templates 1 to 8 for readonly-probe.md, bans `run-current --json` and requires ten ALLOWED_ORCA templates, so an owner-approved OQ-17/OQ-18 change is BLOCKING; 7.24 is missing from the 7.17 step 2 follow-up list (TL:1271) | R2-F2 | HIGH, conditional on the branch firing, the owner approving, and the follow-up landing before the 7.21-7.28 panel | H / M / H (R2v1:166, R2v2:120, R2v3:188) | yes (R1-DM:27); not one of F-01..F-10, so owner acceptance by name is advised | pre-existing (TL:1321 byte-identical to BASE; only TL:1320 changed, checked) |
| M-03 | 7.30/7.34 record the sha256 baseline in `fix-log-cycleN.md`, the same path the fix agent is told to "Write a fix log" to (TL:1363, TL:1391); same house pattern, pre-existing, at 14.25/14.29/14.38/14.42 | R1-F3 | MEDIUM | L / M / M (R2v1:161, R2v2:115, R2v3:183) | yes (R1-DM:32, :35; parity rows :100, :103, :110, :113) | introduced by R2 at 7.30/7.34 (TL:1363 and TL:1391 differ from BASE; BASE has `sha256sum` only on 2614, 2642, 2705, 2733, checked) |
| M-04 | 7.30/7.34 post-fix re-run lists omit the `grep -c '^## Execution authorization (verbatim)'` check, although the fixer may edit the result file | R1-F4 | LOW | L / L / L | yes | introduced with R2's re-run list |
| M-05 | 7.10 Branch 2 has no "section already exists / style already edited" rule for a retry | R1-F2 | LOW | L / L / L | yes (R1-DM:21) | R2 text (F-04) |
| M-06 | 7.10 omits the ADD:17 "do not reconstruct role" and ADD:19 "fabricated successful summary" clauses; the ADD:19 quote is reworded | R1-F5 | LOW | L / L / L | yes; outside the F-03 list (R2-BR:27) | R2 text (F-03) |
| M-07 | 7.20 matches an executor-written quote against an authority section that points both ways (R2-BR:9 vs TL:3020); the later-dated-message branch has no on-disk comparator | R1-F1 | LOW (record check; real gate is 7.10) | L / L / L | 7.20 yes; root cause R2-BR:9 is outside the plan | deliberate R2 edit B2-1 |
| M-08 | 13.18/13.22 fix agents may edit "the docs" with no DESIGN sha256 guard (prose immutability only) | R3-F3 | LOW | L / L / L | yes (R1-DM:73, :76) | pre-existing (TL:2384, TL:2412 byte-identical to BASE, checked) |
| M-09 | 7.17 Context (TL:1267) and the OQ section (TL:2991, TL:2992) cite DESIGN lines 550/552/971/973; the quoted sentences now sit at DESIGN:557/559/993/995 | O-002 | LOW (navigation) | L / L / L (R2v1:179, R2v2:137, R2v3:200) | no | pre-existing |
| closed | Run-4 coverage matrix stale | R3-F1, O-003 | closed | L-closed x3 | n.a. (reflect artifact) | MX:7 now `run: 4`; only `status: partial` is MX:225 (checked) |
| withdrawn | 13.1 credits ticked 5.2 with the R4-F5 wording | R3-F2 | no defect | none x3 (R2v1:169, R2v2:123, R2v3:191) | n.a. | TL:2265 is true as written |

Raised in Round 2 by two advocates, not debated by all three (carried to the invariant probe as INV-R4-003, not counted as a merged finding here): the approval follow-up names "a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate" (TL:1271) that no item in the plan provides. Checked: `grep -n 'DESIGN edit item'` on TL prints only lines 1268 and 1271. Sources: R2v1:45 "no such item exists in the plan"; R2v3:15 "The plan names no item or slot for the DESIGN edit". V2 is silent on it.

## 2. Card findings: final position after two rounds

| Card finding | Card severity | Winner | Final severity | Convergence | In the 85? | Merged id | Deciding quote |
|---|---|---|---|---|---|---|---|
| R2-F1 | HIGH | V2 | HIGH (conditional) | unanimous | no | M-01 | TL:1274 "confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines" vs TL:1272 "it sets `status: RESOLVED`" |
| R2-F2 | HIGH | V2 (discovery; R2v1:166, R2v3:188; V2 adv gave calibration to V3, R2v2:120) | HIGH (conditional) | 2/3 on H | yes | M-02 | TL:1321 "that ALLOWED_ORCA holds ten templates" and "Each breach is BLOCKING." vs TL:1271 "the 8.10 and 10.3 count source changed from the literal 10 to the approved count" |
| R1-F3 | MEDIUM | V1 (fact, all three); severity 2/3 M | MEDIUM | 2/3 on M | yes | M-03 | TL:1363 "record the output of `sha256sum ...` in `.../qa/decisions/fix-log-cycle1.md`" and "Write a fix log listing each finding id" and "the output path `.../qa/decisions/fix-log-cycle1.md`" |
| R1-F4 | LOW | V1 | LOW | unanimous | yes | M-04 | TL:1363 "also permit ... `step-7.10-style-exception.md`"; `grep -n 'Execution authorization'` on TL prints only 1210, 1211, 1293 (checked) |
| R1-F2 | MEDIUM | none (fact V1, size V3) | LOW | unanimous | yes | M-05 | TL:1210 "look first for the `## Execution authorization (verbatim)` section"; TL:1211 "later content is appended below it, never overwriting it" |
| R1-F5 | MEDIUM | V3 (severity), V1 (fact) | LOW | unanimous | yes | M-06 | Grep on TL for `fabricat` hits 1231, 1973, 1980 only, none on 1210; TL:1210 "Formatting never authorizes advice the sweep skill prohibits" vs R2-BR:27 "Formatting never authorizes advice prohibited by the sweep skill" |
| R1-F1 | MEDIUM | V2/V3 (conclusion); V1 conceded "Today 7.20 returns PASS" was overstated (R1v1:58) | LOW | unanimous on L | yes | M-07 | TL:1293 "it must hold a dated verbatim quote of the owner's separate execution authorization and the paths of the fresh structural, alignment, qualitative and PRE reports" |
| R3-F3 | LOW | V3 | LOW | unanimous | yes | M-08 | TL:2384 "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable, with any required authority change left OPEN for escalation." and no `sha256sum` on 2384 or 2412 (TL hits: 1363 1391 2614 2642 2705 2733, checked) |
| R3-F1 | LOW | V3 (true when read) | closed | unanimous | n.a. | closed | MX:7 `run: 4` (checked) |
| R3-F2 | LOW | none | withdrawn | unanimous | yes (13.1) but no defect | withdrawn | R1v3:29 "WITHDRAWN as a defect" |
| O-001 (DA) | none | V2 | folded into M-01 | unanimous fold (R2v1:114, R2v2:29, R2v3:105) | no | M-01 | TL:1270 "The branch first writes a decision file" |
| O-002 (DA) | none | none | LOW | unanimous | no | M-09 | TL:1267 "DESIGN line 552: \"The `worker-list` cursor template is not in the set" vs DESIGN:559 "The `worker-list` cursor template is not in the set" |
| O-003 (DA) | none | V3 | closed | unanimous | n.a. | closed | MX:7 `run: 4` |

Duplicate test (plan rule TL:1356 "two findings are one finding when they name the same `file:line` and the same defect"): R1-F3/R1-F4 share TL:1363/1391 but are different defects (where the baseline lives vs what is re-run), so two findings with one bundled remedy; R2-F1/R2-F2 differ in line and defect; R1-F3/R3-F3 differ in line and defect. Only O-001 folds (same item, same resume gap, one 7.17 authorization). This matches R2v1:114 "no card finding is a duplicate of another under the plan's own rule".

## 3. Per diff point: final position after Round 2

Winner votes are the Round 2 `POINT` lines (R2v1:134-183, R2v2:92-138, R2v3:156-201). "p:" marks a position taken from an advocate's prose because it wrote no `POINT` line for that id; the quote is in section 5. Agreement rule (SKILL.md:1434-1437): unanimous or at least 2 of 3 on the same winner; "none" counts as a position (no variant superior). Severity "n.a." marks a descriptive point that carries no defect of its own; the linked merged finding carries the severity.

| Point | Level | V1 adv | V2 adv | V3 adv | Agreed? | Winner | Final severity | In the 85? | Merged id |
|---|---|---|---|---|---|---|---|---|---|
| S-001 | L2 | V2 | V2 | V2 | yes | V2 | n.a. (profile: 2 H-cond, 1 M, LOW tail) | n.a. | M-01, M-02 |
| S-002 | L2 | none | none | none | yes | none | n.a. | n.a. | - |
| S-003 | L2 | V2 | none | V2 | yes | V2 | n.a. | n.a. | - |
| S-004 | L2 | V3 | V3 | V3 | yes | V3 | n.a. | n.a. | closed |
| S-005 | L2 | none | none | split (V1 for M-03 remedy, V2 for M-01 remedy) | yes (2/3 none) | none | n.a. | mixed: M-01 no, others yes | M-01, M-03 |
| S-006 | L1 | none | none | none | yes | none | n.a. | n.a. | - |
| S-007 | L1 | none | none | none | yes | none | n.a. | n.a. | - |
| C-001 | L3 | V2 | none | V2 | yes | V2 ("fixed (scope) / open (branch)") | HIGH-cond | no (7.17), yes (7.24) | M-01, M-02 |
| C-002 | L3 | V3 | V2 | V3 | yes | V3 | LOW | yes | M-07, M-04, M-05 |
| C-003 | L3 | V3 sev / V1 fact | V1 | V1 | yes | V1 | MEDIUM | yes | M-03 |
| C-004 | L3 | V3 | V3 | V3 | yes | V3 | LOW | yes | M-06 |
| C-005 | L2 | V2 | V2 | V2 | yes | V2 | n.a. | 7.17 no; 7.24, 13.18, 13.22 yes | M-01, M-02, M-08 |
| C-006 | L2 | V2 | V2 | V2 | yes | V2 (with the V3 correction that M-03 sits in R2-changed lines, R2v3:17) | n.a. | n.a. | M-01, M-02, M-03, M-08 |
| C-007 | L2 | none | none | none | yes | none | n.a. | n.a. | - |
| X-001 | L3 | V2 | none | V2 | yes | V2 | HIGH-cond | no (7.17), yes (7.24) | M-01, M-02 |
| X-002 | L3 | V3 | V2 | V3 | yes | V3 | LOW | yes | M-04, M-05 |
| X-003 | L3 | V3 | V1 | V1 | yes | V1 ("fixed with a residual") | MEDIUM | yes | M-03 |
| X-004 | L2 | V2 | V2 | V2 | yes | V2 | n.a. | n.a. | M-01, M-02 |
| X-005 | L3 | V3 and V2 (joint) | V2 | V3 | no (tie on the winner name; all three agree on the disposition: V1's PASS claim rejected, LOW) | none | LOW | yes | M-07 |
| X-006 | L2 | V3 | V3 | V3 | yes | V3 | closed | n.a. | closed |
| X-007 | L3 | V3 sev / V1 fact | V3 | V3 | yes | V3 | LOW | yes | M-06 |
| A-001 | L3 | p: none | none | p: none | yes (p) | none | n.a. | n.a. | - |
| A-002 | L3 | none (middle rule) | V2 | V2 | yes | V2 (literal where the plan has no resume text) | n.a. | n.a. | M-01 |
| A-003 | L3 | none | none | V2 (heading "A-002/A-003", R1v3:106) | yes (2/3 none) | none | n.a. | n.a. | M-01, M-05 |
| A-004 | L3 | none | none | none | yes | none (reachable, frequency unknown) | n.a. | n.a. | M-01, M-02 |
| A-005 | L3 | p: none | none | p: none | yes (p) | none (accidental, not hostile) | n.a. | n.a. | M-03 |
| A-006 | L2 | silent | none | silent | no (one stated position) | - | n.a. | n.a. | - |
| A-007 | L3 | p: V2 (via C-005) | V2 | p: V2 (via C-005) | yes (p) | V2 | n.a. | n.a. | M-01, M-02, M-08 |
| A-008 | L3 | V3 | V3 | V3 | yes | V3 | closed | n.a. | closed |
| A-009 | L2 | p: none | none | p: none | yes (p) | none (caller scale) | n.a. | n.a. | - |
| A-010 | L1 | p: none | none | p: none | yes (p) | none | n.a. | n.a. | - |
| U-001 | L3 | none | V2 | V3 | no (split) | - | LOW | yes | M-07 |
| U-002 | L3 | none | none | none | yes | none | LOW | yes | M-05 |
| U-003 | L3 | V3 sev / V1 fact | V1 | V1 | yes | V1 | MEDIUM | yes | M-03 |
| U-004 | L3 | V1 | V1 | V1 | yes | V1 | LOW | yes | M-04 |
| U-005 | L3 | V3 sev / V1 fact | V3 | V3 | yes | V3 | LOW | yes | M-06 |
| U-006 | L3 | V1 | V1 | V1 | yes | V1 | not a defect | n.a. | - |
| U-007 | L3 | V2 | V2 | V2 | yes | V2 | HIGH-cond | no | M-01 |
| U-008 | L3 | V2 | V3 | V2 | yes | V2 | HIGH-cond | yes | M-02 |
| U-009 | L2 | V2 | V2 | V2 | yes | V2 | not a defect | n.a. | - |
| U-010 | L2 | V3 | V3 | V3 | yes | V3 | closed | n.a. | closed |
| U-011 | L1 | none | none | none | yes | none | withdrawn | n.a. | withdrawn |
| U-012 | L3 | V3 | V3 | V3 | yes | V3 | LOW | yes | M-08 |
| U-013 | L1 | V3 | V3 | V3 | yes | V3 | not a defect | n.a. | - |
| O-001 | L3 | V2 | none | V2 | yes | V2 | folded (M-01) | no | M-01 |
| O-002 | L1 | none | none | none | yes | none | LOW | no | M-09 |
| O-003 | L1 | V3 | V3 | V3 | yes | V3 | closed | n.a. | closed |

## 4. Settlement of the still-disputed severities (my own file checks)

### 4.1 M-02: item 7.24 lens against an owner-approved OQ-17/OQ-18 change. Final: HIGH, conditional

Round 2 votes: V1 adv H at 0.55 (R2v1:55 "final severity H (conditional on an approved change; M is defensible)"), V3 adv H at 0.55 (R2v3:74), V2 adv M at 0.84 (R2v2:120). V2's reason for M is that owner handling is "already a named category of OPEN work" (R2v2:19). I checked the halt chain myself and do not accept the downgrade.

Exact sequence when the branch fires and the owner approves (every step quoted from TL, read this run):
1. 7.16 runs the eight templates only and writes readonly-probe.md (TL:1261 "Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md` with one section per capture item 1 to 13: the exact command").
2. 7.17 Action writes 1.0a-facts.md; outcome (a) or (b) holds (TL:1269 "Owner allowlist branch (outcomes (a) a cursor field captured and (b) open item 3 CLOSED with `run-current` needing `--json`)").
3. Step 1 writes OQ-17 and/or OQ-18 with `status: PENDING` and HALTs (TL:1270 "It then HALTs before step 1.2 under the Phase 7 preamble Branch 1 rule"). HALT rule TL:195: "set frontmatter `status` to \"⚪ Blocked\" ... STOP, and do not tick the item."
4. The owner approves. Step 3 fills the four lines, sets RESOLVED, resets Doing (TL:1272 "it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to \"🟠 Doing\", and clears `blocker_reason`") and "An approval resumes into the step 2 follow-up."
5. Step 2 follow-up (TL:1271): "a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate; the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file; the 7.16 forbidden list and its grep (item 7.16 Context and Verification) updated to allow the approved argv and a re-capture of it; and a re-run of the R5 review gate (6.5 to 6.22) over the new edit." 7.24 is not on this list. The DESIGN edit item does not exist in the plan (`grep -n 'DESIGN edit item'` prints only TL:1268 and TL:1271), so this step needs a plan extension first (see INV-R4-003). The 7.16 grep reads readonly-probe.md (TL:1263), so the approved re-capture lands in readonly-probe.md [INFERRED from TL:1263 and TL:1271].
6. 7.17 completes only if M-01 is bypassed (4.2). Then 7.18, 7.19, 7.20 (7.20 passes the RESOLVED optional record: TL:1293 "expect at least 1 for each file that exists").
7. 7.21-7.28 are spawned together (TL:1321 "spawn all of them in the SAME message, in parallel"). The 7.24 lens gets the OQ records and 1.0a-facts.md as inputs (TL:1320 "plus any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote") but its prompt says, unconditionally (TL:1321): "every command in readonly-probe.md is one of templates 1 to 8 of DESIGN 7.3 or a file read, that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run", "that ALLOWED_ORCA holds ten templates" and "Each breach is BLOCKING." An approved cursor template makes eleven (DESIGN:559 "it is added only after step 1.0a captures the cursor field, as one extra template"); an approved `--json` is "a template change" (DESIGN:557). So up to three sub-checks breach: the probe-command check (both outcomes), the forbidden-token check (outcome b), the ten-template check (outcome a).
8. 7.29 puts the BLOCKING findings in `F_0` (TL:1356 "(4) write `F_0` = the ids of every BLOCKING or MAJOR finding").
9. 7.30 fixer cannot clear them: TL:1363 "it may never change a decision's `Chosen:` line or re-run a live Orca command. A finding that needs the owner or a new capture is left OPEN with that reason." The same line lets it edit "the R5 DESIGN edits listed in item 6.3 (sections 7.3, ...)", so a literal fixer could instead revert the approved template [INFERRED risk, R2v3:16].
10. 7.33 (TL:1384), regression first, then: "(b) Monotonicity: if `|F_1| >= |F_0|`, write `[HALT-MONOTONICITY] |F|=<n>` ... and apply the HALT rule". If the stuck lens findings are all of `F_0`, or every other finding is fixed in cycle 1 and cycle 2 cannot reduce further, the run ends on a monotonicity HALT (7.33 or TL:1412 (b)). TL:1384 has no escalation text; only TL:1412 (d) says "escalate the open BLOCKING and MAJOR findings to the user", and (d) is reached only when cycle 2 strictly reduces `|F|` without clearing it (R2v1:31-37 case table, which I re-traced against TL:1384 and TL:1412).

Why HIGH: a correct, owner-approved run cannot reach `Decisions gate: PASS` (TL:1415 Completion gate "`Decisions gate: PASS` (at any cycle) is recorded") without editing the plan, and no item names that exit. That matches "a correct run fails". The HALT is fail-closed: nothing passes silently. V2's "owner-intervention workaround" is the owner revising the plan, which is available for every defect and so does not make this MEDIUM.

Conditions, all required: (i) step 1.0a shows outcome (a) or (b); (ii) the owner approves (refusal keeps ten: TL:1272 "8.10 then keeps `ALLOWED_ORCA` at exactly 10"); (iii) the step 2 follow-up (DESIGN 7.3 edit or re-capture) is in place before the 7.21-7.28 panel, which TL:1272 "An approval resumes into the step 2 follow-up" supports, and which in practice needs a plan extension because the DESIGN edit item does not exist; (iv) the lens agent obeys "Each breach is BLOCKING" rather than excusing the breach from the OQ record it reads. On the default path and the refusal path there is no effect. Unconditionally the effect is MEDIUM. The fix is in the surface (R1-DM:27 "| 7.24 | Read-only safety lens | Add scoped inputs; ..."), but 7.24 is not one of the ten fixes (R2-BR:7 "covering F-01 to F-10"), so the remediation should ask the owner to accept it by name. It does not block starting 7.10 (7.10 is TL:1208, before 7.16).

### 4.2 M-01: item 7.17 Verification against its own resume. Final: HIGH, conditional

When the Verification is read: 7.17 is unticked while halted (TL:1266 `- [ ] **7.17`). At the first pass the branch HALTs and the HALT rule says "STOP, and do not tick the item" (TL:195), so either the executor stops before the Verification or reads it at the halt moment (the only moment its PENDING/halted predicates are true). In both readings the item is still unticked, and the task skill resumes at it: SK:535 "Find the first unchecked item — Scan for the first `- [ ]` item. This is where execution resumes." and SK:537 "Start the F1 loop from the first unchecked item". So the Verification is read (again, or for the first time) after the resume, when step 3 has set RESOLVED, filled `Chosen:`/`Decided by:`/`Decision source:` and cleared the halt (TL:1272).

What the Verification then finds (TL:1274): "`status: PENDING`" false; "the empty `Chosen:`, `Decided by:` and `Decision source:` lines" false; "the task is halted (frontmatter `status` and `blocker_reason` set by the HALT rule)" false; the `grep -c '^| [^|]* | 7\.17 | HALT (PENDING) | ...'` count "returns exactly 1" true (the log is append-only). The Completion gate (TL:1275 "The facts file is written with no open HALT.") is true. Verification and Completion gate cannot both hold, for an approval and for a refusal alike.

Can the item complete? Not under its written text. The available exits are all failures under the caller's scale: (a) the executor silently reinterprets "When the owner allowlist branch fires" as a past event (not written); (b) the task skill's generic rule SK:183 "mark the item `- [x]` with a note in Task Log explaining what was blocked and why, then continue to next item. Items are NEVER left unchecked", which ticks 7.17 with its Verification unmet, i.e. a required check is lost; (c) the executor stops, and nothing names the blocker (TL:1274's only stop text is for the missing Run/Dispatch id samples: "in either case stop before marking this item complete until the blocker is resolved"). On resume the literal Action also re-runs step 1, "The branch first writes a decision file" with `status: PENDING` (TL:1270), over the RESOLVED record (O-001, folded; SK:538 "If an item's output file exists, that work is done" softens this for the Action only).

Final HIGH, conditional on the branch firing (either owner answer). Out of the 85: R1-DM has no 7.17 row (`grep -n '7\.24\|7\.17'` on R1-DM prints only line 27, the 7.24 row) and PC has no `"7.17"` key (grep exit 1). R2-BR:17 allows "A short additive note ... after the existing R1 note (TL:3010+)", but TL:3016 says "This note is not an executable checklist.", so a note is a mitigation, not a fix. The repair needs an owner extension naming 7.17.

### 4.3 M-03: sha256 baseline shares the fix-log file. Final: MEDIUM

Votes: V1 adv L (R2v1:96, withdrew its "ordinary Write replaces the file" premise as unproven), V2 adv M (R2v2:115), V3 adv M (R2v3:115). Facts I checked:
- The collision is literal: TL:1363 "record the output of `sha256sum ...` in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`", the fix-agent preamble "Write a fix log listing each finding id, the change, and the `file:line` after the change.", and "the output path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`". TL:1391 repeats it with `fix-log-cycle2.md`.
- It is R2's own text: TL:1363 and TL:1391 differ from BASE, and BASE has `sha256sum` only on 2614, 2642, 2705, 2733 (checked). R2 copied the 14.x house pattern (TL:2614 "record the output of `sha256sum docs/designs/orchestrator-mode.md ...` in the fix log").
- What is lost: the only durable record of the before-sums. The 7.30 Verification needs "every appended re-check line is PASS" (TL:1365). The plan itself says a resumed session cannot rely on chat memory (TL:1210 "because a resumed session does not remember the chat").
- What limits it: the guarded four files are outside the fixer's allowed edits (TL:1363 "Never change revision authority/design append/decision choice"), and in an unresumed session the orchestrator still holds the command output. An honest executor without a baseline cannot append PASS, so the failure is fail-closed.

That is "real impact with a workaround": MEDIUM. Not HIGH: a correct uninterrupted run does not fail and no wrong change passes. Not LOW: the guard's durable evidence is placed where an instructed write can remove it. In scope (R1-DM:32 "| 7.30 | Serialized fix cycle1 |", :35 7.34). A parity edit of 14.25/14.29/14.38/14.42 is in the 85 (R1-DM:100, :103, :110, :113) but outside F-07 (R2-BR:31 "| F-07 | LOW | 7.30, 7.34 |").

### 4.4 Findings all three agree are real but that no card rated at that level

- M-09 (O-002, stale DESIGN line numbers): no card raised it; all three rate it LOW (R2v1:179, R2v2:137, R2v3:200). Checked: TL:1267 holds "DESIGN line 552", "DESIGN line 550", "DESIGN line 971", "DESIGN line 973", TL:2991 "DESIGN line 552", TL:2992 "DESIGN line 550"; the quoted sentences are at DESIGN:557, :559, :993, :995. LOW, out of the 85.
- O-001 (7.17 Action step 1 re-writes PENDING on resume): no card raised it; all three fold it into M-01 rather than counting it separately (V1 and V3 graded it M as a standalone, V2 L). One finding per defect: folded, no separate severity.
- Card downgrades all three advocates accept and the files support: R1-F1, R1-F2, R1-F5 from MEDIUM to LOW (R1v1:15-18 V1's own downgrades). Upgrades: none beyond the cards (R2-F1 and R2-F2 stay at the card's HIGH, now marked conditional).
- No other defect reached agreement of all three without a card.

## 5. Convergence

Formula (SKILL.md:1390-1393): "convergence = agreed_points / total_diff_points" with "total_diff_points = count(S-NNN) + count(C-NNN) + count(X-NNN) + count(A-NNN)". Threshold 0.80 (SKILL.md:1396 "default: 0.80"). Agreement (SKILL.md:1435-1437): unanimous, or "≥2/3 of advocates agree", else split.

Denominator: S 7 + C 7 + X 7 + A 10 = 31.

Prose positions used where an advocate wrote no `POINT` line (each is the advocate's own words):
- A-001: R1v1:163 "`qa/preservation-check.json` changed_labels 64, allowed_labels 85, no 7.17 entry"; R2v3:17 "N-5. R2 changed the 7.30 and 7.34 Action lines ... PC `changed_by_label`". Both accept the counts.
- A-005: R1v1:35 "That is ordinary behaviour, not malice."; R2v3:112 "so a fresh Write is the expected action, not a hostile one".
- A-007: R2v1:145 "(7.17 needs an owner extension; 7.24 and 13.18/13.22 are inside)"; R2v3:167 "(7.17 outside; 7.24, 7.30/7.34 and 13.18/13.22 inside)".
- A-009: R2v1:53 "The scale in the prompt: HIGH = a correct run fails or a required check is lost; MEDIUM = real impact with a workaround."; R2v3:72 "By the prompt's scale (\"a correct run fails\")".
- A-010: R1v1:5 "Everything quoted below was re-read from the files on disk in this round"; R1v3:6 "Where I re-checked a claim with `diff`/`grep` I say so".
- A-006: no prose position from V1 or V3; left unagreed.

| Count | S | C | X | A | Agreed / 31 | Convergence | 0.80 met? |
|---|---|---|---|---|---|---|---|
| Strict (only `POINT` lines; silence = no position) | 7 | 7 | 6 (X-005 tie) | 4 (A-002, A-003, A-004, A-008) | 24 | 0.774 | no |
| With stated prose positions (primary) | 7 | 7 | 6 | 9 (all but A-006) | 29 | 0.935 | yes |

Cross-check over the 34 points diff-analysis counts (S, C, X, U; DA:8 "Total differences found: 34"): U agreed 12 of 13 (U-001 split: none / V2 / V3), so (7 + 7 + 6 + 12) / 34 = 32 / 34 = 0.941, met.

Reading: every point short of agreement under the strict count is silence, not a contradiction, except X-005, where all three agree on the disposition (V1's "Today 7.20 returns PASS" rejected, LOW) and only the winner's name ties (R2v1:154 "winner V3 and V2 on the conclusion"; R2v2:110 "winner variant 2"; R2v3:176 "winner V3"). Primary result: 0.935, threshold 0.80 met.

Severity agreement on the 9 merged findings: 7 unanimous (M-01, M-04 to M-09), 2 at 2 of 3 (M-02 H over M, M-03 M over L); none split.

Taxonomy coverage gate (SKILL.md:1415 "all three levels must have > 0 points addressed"): L1 4, L2 12, L3 18 (DA:190), each debated; met.

Invariant gate (SKILL.md:1473 "convergence requires: count(HIGH + UNADDRESSED invariants) == 0"): see `ADV/invariant-probe.md`. It records one UNADDRESSED HIGH (INV-R4-003) and one PARTIAL HIGH (INV-R4-011, counted as not addressed for the gate). Status: BLOCKED_BY_INVARIANTS (SKILL.md:1501 "Agreement ≥ threshold AND taxonomy covered BUT HIGH-severity UNADDRESSED invariants exist"), until those two are resolved in the remediation brief or accepted by the owner as known risk.

## 6. Net result for the reflect run

- No merged finding makes a default-path run fail. Both HIGH findings bite only if the OQ-17/OQ-18 branch fires (M-02 also needs owner approval). Neither blocks starting 7.10 (TL:1208, before 7.16).
- Out of the 85: M-01 and M-09 (7.17, plus TL:2991-2992) need an owner extension naming 7.17. In the 85: M-02 to M-08; M-02, M-06, M-08 and the 14.x part of M-03 are outside the owner's "F-01 to F-10" wording (R2-BR:7), so the remediation should list them for owner acceptance by name rather than treat the label surface as consent.
- No owner decision is assumed here; no plan, authority or product file was changed by this step.

<!-- end of consensus -->

# Round 1 — Variant 2 advocate (reviewer 2, qa)

Evidence convention: TL, DESIGN, ADD and ADV have the meanings assigned in `advocate-prompt.md:3` ("ADV=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/plan-defect-fixes-20261110/reflect/pre/adversarial"). R2-BR and R2-DM denote that revision's BUILD-REQUEST.md and delta-manifest.md; R1-DM denotes the preceding chat-output-exception revision's delta-manifest.md. Citations use these repository-relative path aliases, followed by original file line numbers. Positions below are independent judgments, not acceptance of the Step 1 adjudications.

## 1. Shared assumptions first; strongest case for V2

**A-002/A-003 — What a correct executor must check.** The strongest opposing reading treats the PENDING checks as historical first-halt checks: TL:1274 says "When the owner allowlist branch fires" and TL:1272 expressly describes "The resume". I concede that a careful human can infer that split. But TL:1274 also requires "the task is halted", whereas the completion gate requires "no open HALT" (TL:1275). These are current-state predicates, not checks that the state once existed. The installed task skill requires "Start the F1 loop from the first unchecked item" (/home/coder/.claude/skills/task/SKILL.md:537); its "If an item's output file exists, that work is done" caveat (:538) avoids repeating completed work, not verifying contradictory states. My severity assumes faithful verification, not permission to silently rewrite a gate. This is a conditional HIGH, not an assertion that every run fails.

POINT A-002/A-003: winner variant 2, confidence 0.95, final severity H, in-scope-of-85 no.

**A-004 — Reachability, not likelihood.** The strongest objection is that the optional path need never occur: DESIGN:995 permits "no cursor template" and a lower-bound total. Conceded; this is not a default-path failure. Yet TL:1269 expressly defines outcomes "a cursor field captured" and "run-current ... needing --json", and TL:1272 specifies an owner "approval or refusal". Those are designed cases, not invented attacks. I do not know which a future capture will produce. Correctness must include either answer if the branch fires; selecting refusal does not fix the contradictory completion check.

POINT A-004: winner variant 2, confidence 0.96, final severity H, in-scope-of-85 no.

**U-007 / R2-F1 — Retain HIGH, explicitly conditional.** V2's strength is checking the producer's completion state, not just its consumers. TL:1272 says "sets `status: RESOLVED`" and "clears `blocker_reason`" after filling the owner fields. TL:1274 still demands "`status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines"; TL:1275 requires "no open HALT". A correct resolved refusal and a correct resolved approval both fail that literal verification. The historical HALT log can remain; the current decision record cannot be simultaneously PENDING and RESOLVED. The smallest repair is separate first-halt and resolved-completion verification, retaining owner evidence and refusing completion while still pending. Surface limit: R2-BR:17 permits only "the 82 labels of R1 ... plus 13.1, 8.19 and 10.5"; R1-DM:21-27 lists 7.10, 7.13 and 7.20-7.24, not 7.17. Request a bounded extension, never silently edit 7.17.

POINT U-007: winner variant 2, confidence 0.99, final severity H, in-scope-of-85 no.

**C-005 — Surface is not blanket substantive authorization.** V2 must not conflate these. R1-DM:27 explicitly includes "7.24 | Read-only safety lens", so its Action is inside the 85 labels. However, R2-BR:25 names only the F-01 "lens inputs" there, while R2-BR:21 calls the ten listed recommendations "authoritative text". My position is to distinguish mechanical scope from permission to add a newly discovered repair: 7.17 needs an extension to the label surface; 7.24 does not, although the new finding/remedy should be explicitly accepted rather than implied by the old F-01 authorization. No plan edit is made by this debate.

POINT C-005: winner none, confidence 0.99, final severity L, in-scope-of-85 n.a.

## 2. Approved allowlist changes and the scope concession

**U-008 / R2-F2 — Retain HIGH only for an approved change.** Steelman V1/V3: the default ten-template contract is a deliberate safety restriction, not something a reviewer may weaken; DESIGN:555 calls it the "pinned set". Conceded. But DESIGN:559 expressly permits a captured cursor "as one extra template", and DESIGN:557 calls an approved JSON need "a template change". The producer requires "the ... count source changed from the literal 10 to the approved count" and "allow the approved argv and a re-capture of it" (TL:1271; also R2 baseline:1271). The consumer still insists "ALLOWED_ORCA holds ten templates" and bans "run-current --json", declaring "Each breach is BLOCKING" (TL:1321). That rejects a correct approval. An ordinary changed-template approval cannot satisfy both contracts without changing the lens. Fix only the approved-count/argv/capture branch; retain every unapproved-command prohibition and the default/refusal checks. Surface: yes, per R1-DM:27, quoted above; this does not itself authorize the extra repair.

POINT U-008: winner variant 2, confidence 0.99, final severity H, in-scope-of-85 yes.

**C-001 / X-001 — Correct V2's F-01 closure wording.** The strongest V1/V3 case is that F-01 fixes the listed consumers, not every optional-branch defect. R2-DM:13 records "each existing OQ-17/OQ-18 file is checked separately (skip if absent)" and "one extra row per resolved optional decision". I concede my card's single label "partial" mixes scoped closure and end-to-end readiness. Final wording: **F-01 fixed as scoped; optional branch still open under U-007/U-008.** Fixed consumers do not prove a coherent producer/resume/safety path. This is a correction of my classification, not withdrawal of either conditional failure.

POINT C-001/X-001: winner none, confidence 0.98, final severity H, in-scope-of-85 n.a.

**C-006 / X-004 — Do not blame R2 for inherited text.** I independently read R2's baseline: `revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md:1272` already says "sets `status: RESOLVED`", :1274 already requires "`status: PENDING`", and :1321 already requires "ten templates" and forbids "run-current --json". These are the same task-folder-relative baseline clauses as current TL:1272/1274/1321. R2-DM:13 lists 1320, not 1321, among the F-01 edits. Thus the contradictions predate R2; a residual defect is not evidence that its bounded edits regressed the plan. R2-DM:32 reports "Changed lines: 73 in 64 labels"; I have not recomputed that count.

POINT C-006/X-004: winner variant 2, confidence 0.99, final severity L, in-scope-of-85 n.a.

## 3. Steelman and critique V1, finding by finding

**C-002 / X-002 / X-005 / U-001 — Authorization carrier.** Steelman: matching an executor-written quote to an ambiguous planning record is weaker than independent, later execution evidence. R2-BR:9 really says both "It does not by itself start item 7.10" and that earlier instructions are "the owner's execution direction". Concede this ambiguity. But V1's automatic-PASS counterexample ignores TL:1293's requirement for "the owner's separate execution authorization" and supplied fresh report paths, and TL:1210's refusal when authorization is "absent, failed or ambiguous". A quote containing only "Do not start 7.10" (R2-BR:7) does not satisfy that semantic gate. F-04's record carrier is delivered; ambiguity is LOW, not a demonstrated authorization bypass. A saved authority message may help, but changing the owner record itself is not a label-body edit.

POINT C-002/X-002/X-005/U-001: winner variant 2, confidence 0.94, final severity L, in-scope-of-85 yes.

**U-002 — 7.10 retry.** Steelman: an interrupted first run can leave partial edits and an existing heading, so a literal repeat needs idempotence. TL:1210 says "On failure ... remain incomplete"; TL:1293 expects one authorization section. Concede a retry clarification would help. But duplicate sections are not inevitable: TL:1210 explicitly looks first for the existing section, and TL:1211 says later content is "appended below it, never overwriting it". The evidence supports a LOW ambiguity, not V1's asserted guaranteed correct-resume failure. Add an existing-section/already-edited check in 7.10, not a new mechanism.

POINT U-002: winner none, confidence 0.92, final severity L, in-scope-of-85 yes.

**C-003 / X-003 / U-003 — Baseline and fix log collide.** Steelman: the pre-spawn baseline must survive the agent's permitted output write. TL:1363 records hashes in "fix-log-cycle1.md" and supplies that same "output path" while asking "Write a fix log"; TL:1391 repeats it for cycle 2. Concede V1's best residual and amend my unqualified F-07 "fixed": the prescribed before/after commands exist, but their durable baseline is vulnerable to an ordinary log replacement. Retain MEDIUM, not HIGH: accidental overwrite is possible, not required, and keeping the pre-spawn output separately is a direct workaround. Session memory alone is a weak audit trail. Use a separate orchestrator-owned baseline, without enlarging the hash target set.

POINT C-003/X-003/U-003: winner variant 1, confidence 0.95, final severity M, in-scope-of-85 yes.

**U-004 — Rechecking authorization after fixes.** Steelman: the agent may edit "step-7.10-style-exception.md" (TL:1363), so its evidence needs revalidation. Concede the detailed lists in TL:1363/1391 omit the heading-count/quote check. However, both also say "re-run the item 7.20 commands", which already includes that check (TL:1293: "expect 1, then read that section"). This is inconsistent specificity, not proof that every compliant executor drops the check. LOW; explicitly repeat the count and read/compare obligation rather than treating this as a missing higher-level guard.

POINT U-004: winner variant 1, confidence 0.92, final severity L, in-scope-of-85 yes.

**C-004 / X-007 / U-005 — Addendum wording.** Steelman: source-presence tests can catch omissions that a semantic paraphrase misses. ADD:17 says "do not reconstruct role from files or history"; ADD:19 says "never print a fabricated successful summary or hide an error". Those literal clauses are not in TL:1210, which instead says "data never establishes role or rights" and "accurate other errors with ordinary formatting". Concede the textual omission and my card's overbroad completeness wording. But TL:1212 already requires comparison of "all excluded cases against the addendum", and TL:1973 expressly says "never fabricated success or prohibited advice". TL:1980 requires actual-source presence pins; TL:1982 supplies the HALT for an actual style failure. No observed test proves V1's future failure. LOW, with cheap wording alignment; do not claim a proven MEDIUM blocker or require one exact synonym.

POINT C-004/X-007/U-005: winner variant 3, confidence 0.94, final severity L, in-scope-of-85 yes.

## 4. Steelman and critique V3, finding by finding

**A-008 / X-006 / U-010 — Coverage matrix: close the finding.** Steelman: a review matrix must describe the edited plan, and a conservative stale row still misstates coverage. V3 supplied a concrete acceptance condition rather than claiming a false gate pass (ADV/variant-3-original.md:7: "the stale status is the more cautious one"). But the current file is now decisive: `reflect/pre/coverage-matrix.yaml:1` says "run 4 (revision plan-defect-fixes-20261110)", :256 has INF-A06 "status: covered", and :258 describes the newly quoted advice boundary. Crucially :7 now says **`run: 4`**, not 3. Thus even the Step 1 metadata residue is no longer open. Drop R3-F1 from active defects; retain its value as a freshness lesson, not a new LOW issue. The matrix is a review artifact, not one of the 85 task labels.

POINT A-008/X-006/U-010: winner none, confidence 0.99, final severity L, in-scope-of-85 n.a.

**U-011 — Routing-bullet history.** Steelman: identifying the actual wording-producing edit prevents historical sign-offs being mistaken for proof of today's text. `qa/r4/fix-log-cycle1.md:13` records "R2 bold lead and body rewritten", including "adds to that sweep and does not replace it". Concede that naming R4-F5 would improve attribution. But TL:2265 only credits 5.2 with alignment to "master's 5-minute sweep bound", expressly says the older sentence is "history", and commands "if it differs ... the DESIGN text wins". Therefore V3's stronger claim that the plan attributes all current wording to 5.2 is not compelled. LOW, optional history clarification in the already-added 13.1 label, not an execution blocker or reason to edit completed 5.2.

POINT U-011: winner variant 3, confidence 0.92, final severity L, in-scope-of-85 yes.

**U-012 — Docs-fixer authority guards.** Steelman: a later before/after hash cannot detect a change already made before its baseline, so Phase 13 should not rely on Phase 14 to preserve its authorities. TL:2614 records its hashes "Before spawning the agent"; that does not reach back to Phase 13. Concede the missing mechanical before/after guard in TL:2384/2412. But broad permission for "the docs" is expressly narrowed in those same lines: "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable" and authority changes stay "OPEN for escalation". A correct fixer is not authorized to edit DESIGN. This is LOW protection against mistakes, not a correct-run failure or an actual permission loophole. A small hash guard is reasonable if authorized; R1-DM:73/76 lists both 13.18 and 13.22, so it is mechanically inside the 85, though outside the named F-07 repair.

POINT U-012: winner variant 3, confidence 0.95, final severity L, in-scope-of-85 yes.

## 5. Round-1 conclusion and limits

My retained priorities are U-007 and U-008, both HIGH **on their specified branches**, with the different label-scope answers recorded above. The central evidence is not a stylistic preference: "status: PENDING" conflicts with "status: RESOLVED" (TL:1274/1272), and "ten templates" conflicts with "the approved count" (TL:1321/1271). Before calling the optional route clean, obtain the bounded owner direction needed to repair those gates; do not weaken unapproved-command checks or manufacture a global block on earlier authorized work. The owner-surface rule remains "the 82 labels of R1 ... plus 13.1, 8.19 and 10.5" (R2-BR:17).

I accept V1's MEDIUM durable-baseline residual, distinguish it from F-07's delivered commands (TL:1363/1391: "record the output" and "re-run that command"), downgrade its other demonstrated residuals to LOW, and close V3's matrix finding on current evidence (coverage-matrix.yaml:7: "run: 4"). These concessions correct my original unqualified F-01/F-03/F-07 closure wording without dropping either verified optional-branch defect.

This was document inspection and conditional state tracing, not executed plan verification. No tests, live captures, model-behaviour experiments or hash recomputation ran; no future owner decision or branch frequency was assumed. Only this debate transcript was written. No plan, authority, review input or product file was changed.

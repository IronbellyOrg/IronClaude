# Round 1: Advocate statements (parallel)

Persisted by the orchestrator from the two advocate hand-backs (reflect-reviewer agent type, read-only; ids afef8fc06cd6b5c1c for Variant 1 haiku, a8bac3797b0b4ee00 for Variant 2 opus).

## Variant 1 Advocate (haiku:analyzer)

### Position summary
Variant 1 is stronger on whether the rule switch is actually authorized: it identifies the late gate and the undefined controlling recall result (PLAN:78-82, 125-128). Variant 2 has broader coverage, but some of its findings bundle real grading defects with weaker process concerns.

### Steelman of Variant 2
Variant 2 correctly looks beyond digest equality. The surviving instruction "When in doubt, fail it" in `rf-qa` at line 548 can override consequence-based grading, while the zero-trust test's scorer still returns FAIL from CRITICAL/IMPORTANT labels alone (lines 95, 109-119). Its M6 finding is also concrete: S2:138 produces the baseline, but PLAN:230 only requests baselines "from Task 2", which omits M6 (PLAN:59-67).

### Strengths claimed
1. Variant 1 follows execution order, not just acceptance wording. PLAN:125 begins "Edit"; authorization is checked at PLAN:128. The implement protocol puts "Q1 EXEC" before "Q3 REVIEW" at lines 131 and 140. PLAN:96 permits Task 3 to report an unsuccessful result. A blocking authorization gap, although PLAN:20 expresses the intended protection.
2. It distinguishes reporting from deciding. PLAN:78 requires recall "both with and without that reviewer's grades"; PLAN:80 requires "at least 2 of the 3"; PLAN:82 demands "exactly one outcome word". Nothing selects the controlling variant after exclusions. PLAN:128 consumes that outcome, so this is blocking.
3. It grades the stale plugin sentence proportionately. PLAN:214 says stage 4 "adds the plugin mirror", contradicting revision2-brief:16. Minor: the sentence does not require creating the mirror during stage 3.

### Weaknesses identified in Variant 2
1. F1 bundles unlike consequences. rf-qa-qualitative.md line 810 says only "flag this as a systemic problem"; line 805 says FAIL only when a blocking finding remains. Keep the conflicting grading instructions, but line 810 is not another unconditional blocker.
2. F4 describes a possible mistake, not an uncovered requirement: the quota sentence is pinned at test_review_prompt_overrides:244 and PLAN:192 requires that test to "pass unchanged".
3. F9's endpoint complaint lacks the anchor: PLAN:28 requires end points for acceptance lines later tasks invalidate; Task 6's acceptance lines (PLAN:143-148) are not shown becoming false later. Keep the separate hash-description error.

### Concessions
Variant 1's "checked and sound" is too broad. Variant 2 correctly catches the stale label scorer, the misleading hash description and M6 (PLAN:203, 230). It also identifies the missing L5 preservation: SPEC:274 says Medium and Note findings "are never rechecked", but PLAN:125 removes the bullet without restoring that sentence. Variant 2's scope concern also survives: PLAN:76 compares a broad old block with the new digest. Its claim that the defect-hunt brief disappears is not established, because PLAN:76 requires "the same brief" in both arms.

### Shared-assumption responses
- A-001: QUALIFY. Producers are specified, not proven executed (S0:106-111, S1:49, 66, 223, S2:138). PLAN:41 checks existence.
- A-002: REJECT. The frozen patterns at S0:34 miss "When in doubt, fail it" at rf-qa:548. Nothing establishes exhaustive coverage.
- A-003: REJECT. Variant 1 rejects it in F1. Execution-before-review makes a later halt insufficient as the only explicit pre-edit protection.

### Diff-point assessment
| Diff point | Superior | Conf % | Evidence |
|---|---|---:|---|
| S-001 | 1 | 99 | Variant 1 separates blocking status from the Drift classification. |
| C-001 | 2 | 97 | rf-qa:548 adds a conflicting instruction beyond rule 8. |
| C-002 | 2 | 95 | PLAN:203 changes bullet pins without addressing the label scorer at zero-trust:109-119. |
| C-003 | 2 | 98 | S2:138 supplies M6, omitted from PLAN:59-67. |
| X-001 | 1 | 92 | PLAN:125 edits before PLAN:128 checks authorization. |
| X-002 | 2 | 99 | PLAN:203 mentions verdict pairs outside the Critical Rules block at qualitative:983. |
| U-001 | 1 | 92 | Keep blocking. |
| U-002 | 1 | 97 | Keep blocking. |
| U-003 | 1 | 99 | Keep minor. |
| U-004 | 2 | 88 | Keep the scope warning but qualify the asserted loss of the common brief. |
| U-005 | 2 | 95 | Keep minor. |
| U-006 | 1 | 92 | Drop as an independent defect (PLAN:192 requires the quota test unchanged). |
| U-007 | 2 | 88 | Keep minor. |
| U-008 | 2 | 97 | Keep and strengthen. |
| U-009 | 2 | 98 | Keep minor. |
| U-010 | 2 | 97 | Keep minor. |
| U-011 | 1 | 88 | Drop the endpoint allegation. |
| U-012 | 2 | 94 | Keep minor. |
| A-001 | both | 94 | Named producers exist, subject to execution. |
| A-002 | neither | 98 | S0:34 patterns do not establish complete coverage. |
| A-003 | 1 | 99 | Variant 1 expressly rejects the supposed assumption. |

## Variant 2 Advocate (opus:qa)

### Position summary
Variant 2 covers more ground and its findings hold up against the live files: the old-rule lines left in the QA agents, the test re-pins, the asymmetric recall arms and the M6 baseline. It misses the most serious defect: Variant 1 is correct that Task 5's gate is checked after the edit, and the best merged card keeps V1's F1 and F3 next to V2's F1 and F3.

### Steelman of Variant 1
PLAN:20 says "no later task starts unless ... the seeded-recall gate of Task 5 pass". But the gate is only an acceptance line (PLAN:128), and `/sc:implement` edits at "Q1 EXEC" (SKILL.md:131) before it reviews at "Q3 REVIEW" (SKILL.md:140). AC QUALIFY (SKILL.md:93-103) only checks that acceptance criteria exist. retry.md:109 makes it worse: "Every halt in procedure steps 3-5 leaves failed attempt k in the worktree; nothing has been reverted" (also :158). So the halt leaves the edited `pragmatic.md` in place. V1's F3 is also real: PLAN:78 requires recall "both with and without" a contaminated reviewer, PLAN:82 allows "exactly one outcome word". V1's F4 is real: PLAN:214 contradicts PLAN:25 and revision2-brief.md:16.

### Strengths claimed
1. Broader contradiction list. rf-qa.md:548 "When in doubt, fail it and explain why." SPEC:853 assigns 548 to stage 3 ("494, 548 [E: plan review]"). The freeze patterns at SPEC:849 do not match it and PLAN:140 does not list it. rf-qa-qualitative.md:796 equates "blocking (CRITICAL or IMPORTANT)". The digest says an unverified safety claim "stays open for verification" (SPEC:199), in direct conflict with rule 8 at rf-qa.md:100.
2. Recall arms differ in more than the rule (F3). Old arm = pragmatic.md:221-231 (brief, zero-finding rule, binary verdict at :224); new arm = digest only, so "only the rule text differs" is false.
3. Test gaps. pragmatic.md:221 holds "never to meet a quota", pinned by test_review_prompt_overrides.py:244; PLAN:134 does not run it. `BLOCKING_SEVERITIES` at test_nfr_conv_9_zero_trust.py:95 still grades by label.
4. L5 gap (F6). SPEC:274 maps L5 to pragmatic.md:226 ("not rechecked"); Task 5 replaces that bullet; the digest has no recheck sentence.
5. M6 and the README. S2:138 produces the M6 count. README:11 asks only for "the go and the package id", while SRC:41 requires the folder list and the confirmation file.

### Weaknesses of Variant 1
1. F2 is too narrow: it misses rf-qa.md:548, which SPEC:853 names.
2. "Checked and sound" says Tasks 10 and 11 "name the corresponding replacements"; that overlooks the test at :244 and the label-based scorer at :95.
3. First-review F7 marked "fixed" although PLAN:230 lists M6 "from Task 2" and Task 2 never counts M6.
4. Every finding is categorized "Drift", which says nothing about consequence.

### Concessions
Misses the gate-after-edit ordering, the controlling-outcome gap and the PLAN:214 mirror sentence; marks first-review F3 "fixed"; its "no plugin surface beyond the pinned twins" overlooks PLAN:214; line 810 is weak evidence; it does not address line 494 (also in SPEC:853); lower confidence (0.80).

### Shared-assumption responses
- A-001: ACCEPT (PLAN:41, :45 fail safe).
- A-002: REJECT (rf-qa.md:548 and :100 sit outside PLAN:140 and the freeze patterns).
- A-003: REJECT (edit at SKILL.md:131, review at :140, retry.md:109 confirms a halt reverts nothing).

### Diff-point assessment
| Diff point | Superior | Conf % | Evidence |
|---|---|---:|---|
| S-001 | both | 55 | V1 adds a category field, but all "Drift" says nothing. |
| C-001 | 2 | 85 | rf-qa.md:548 and SPEC:853 extend V1's single rule-8 finding. |
| C-002 | 2 | 85 | test_review_prompt_overrides.py:244 and test_nfr_conv_9_zero_trust.py:95 refute V1's "sound". |
| C-003 | 2 | 75 | S2:138 holds M6; PLAN:230 would wrongly say "none exists". |
| X-001 | 1 | 90 | SKILL.md:131 before :140; retry.md:109 leaves the edit in the tree. |
| X-002 | 2 | 75 | Verdict pairs at lines 240 to 784 sit before `## Critical Rules` at rf-qa-qualitative.md:983. |
| A-001 | both | 80 | Both accept it, PLAN:45 fails safe. |
| A-002 | 2 | 80 | V2 shows more of the omitted lines. |
| A-003 | 1 | 90 | Only V1 challenges it; retry.md:109. |
| U-001 | 1 (keep, blocking) | 90 | As X-001. |
| U-002 | 1 (keep, blocking) | 80 | PLAN:78 against PLAN:82. |
| U-003 | 1 (keep, minor) | 85 | PLAN:214 against revision2-brief.md:16. |
| U-004 | 2 (keep, blocking) | 85 | pragmatic.md:221-231 against a digest-only new arm. |
| U-005 | 2 (keep, minor) | 75 | PLAN:144 checks only the freeze, which misses rf-qa.md:170 and :327. |
| U-006 | 2 (keep, minor) | 85 | :244 is pinned, PLAN:134 does not run that test. |
| U-007 | 2 (keep, minor) | 60 | PLAN:43 against the "> " markers at SPEC:195. |
| U-008 | 2 (keep, minor) | 80 | The digest at SPEC:203 has no "rechecked" sentence. |
| U-009 | 2 (keep, minor) | 75 | S2:138. |
| U-010 | 2 (keep, minor) | 65 | test_nfr_conv_9_zero_trust.py:95. |
| U-011 | 2 (keep, minor) | 70 | PLAN:28 requires "until Task N"; Task 6 has none. |
| U-012 | 2 (keep, minor) | 75 | README:11 against SRC:41. |

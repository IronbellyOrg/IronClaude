# Round 1: advocate statements (stage 4 plan, third review)

Advocates were spawned as read-only `reflect-reviewer` agents in parallel (V1 advocate sonnet class, V2 advocate haiku class, V3 advocate opus class). Text below is the advocates' own Position, per-point lines, shared-assumption answers and concessions, with the steelman paragraphs shortened to one sentence each. P4 = stage 4 plan, S1 and S3 = stage 1 and 3 plans, SPEC = merged spec, BRIEF = revision2-brief.md, Q = OPEN-QUESTIONS.md.

## Variant 1 advocate (analyzer, sonnet)

Position: V1's PASS holds. No blocking defect in the live files. The cap-count check can be met by folding the cap bullet into the digest (P4:39 places S1 and S2 "near lines 161 to 163"). The plugin and pointer omissions follow the brief (BRIEF:16) and are recorded (P4:23, P4:26, P4:135). V1 missed one Medium weakness (C-003).

Steelman V2: Q:44 says reassess plugin parity, "This is not a decision to remove plugin parity"; SPEC:948 still lists the plugin mirror; P4:23 itself says "the plan author's reassessment"; the greps at P4:65 can pass on the digest alone. Steelman V3: with a literal "replace S1, S2, S5" the cap bullet and the digest's last sentence both match, count 2; S3:142 handled the same overlap with "1 or more"; V3 also catches the Rule 6 heading dependency.

| point | grade defended | superior | evidence |
|---|---|---|---|
| S-001 | PASS, no blocking | V1 | none of the three blocking claims survives re-reading |
| C-001 | minor, at most Medium | V1 grade, V2 outcome | live block contiguous (skill_template.md:828-831, MDTM :644-647, agent_template_qa.md:161-163); P4:39 "near lines 161 to 163" lets the fold give 1 |
| C-002 | minor | V1 = V3 | P4:25 against P4:65; executor rewords |
| C-003 | Medium | V3 | principle 8 at doc_code:36, documentation_expert:37, recruiting:36 holds none of the banned phrases |
| C-004 | minor | V3 | S3:177 rewrites Rule 6, so the old heading is unlikely to survive |
| C-005 | minor | V1 = V3 | P4:114 against S1:234 |
| C-006 | not a defect | V1 | BRIEF:16 orders no plugin mirror; P4:23 and P4:129 flag it as the author's reassessment |
| C-007 | Medium | V2 detection, V1 grade | P4:26 and P4:135 record it; not in SPEC:948 exit condition |
| C-008 | minor to Medium | V1 | re-read live: automated_qa:125, doc_code:206, skill_template.md:815, :824, :834, agent_template_qa.md:268 |
| C-009 | minor | V1 | SPEC:739 maps CRITICAL to Blocking, so keeping it is consistent; no Constraints line records it |
| C-010 | minor | V1 = V3 | merge line only in agent_template_qa.md; survivors list omits the two cli/ rows |
| C-011 | minor | V2 | a coverage matrix is review input, not a plan deliverable |
| X-001 | can be met, minor | V2 | SPEC:815 says the cap text stays word for word and it does, inside the digest |
| X-002 | not a defect | V1 = V3 | see C-006 |
| X-003 | Medium | V3 | see C-003 |

A-002: QUALIFY (plan guards cross-stage facts with an entry gate and re-read rules; C-005 shows a stale premise can slip through, minor). A-003: ACCEPT (P4:42 "this check fails and the run halts"; a count of 2 stops the run visibly, so it is not a silent wrong result).

Concessions: "proves nothing" for the count-1 check is overstated; calling the keep reading "natural" is arguable (closer to Medium on wording quality); V1 missed C-003, C-004, C-011 and did not grade C-007.

## Variant 2 advocate (qa, haiku)

Position: defends NEEDS-REVISION: recording an exclusion does not deliver a required result or establish owner approval. Retains the plugin and pointer findings; downgrades V2's rewrite-verification finding (C-003) from blocking to Medium.

Steelman V1: a plausible failed execution is not an unavoidable one: P4:45 needs "prints 1 in each" while SPEC:815 protects the cap's words, not a duplicate bullet; folding satisfies both; V1 also correctly recognises BRIEF:16. Steelman V3: keeping the cap bullet and inserting the digest gives two lines; whole-file positive greps cannot tell the principle rewrite from the digest insertion; its blocking grade assumes a retained bullet is mandatory, which SPEC:815 does not say.

| point | grade defended | superior | evidence |
|---|---|---|---|
| S-001 | blocking | V2 | P4:26 "This package does not edit them" leaves SPEC:867 "point at the shared rule" undelivered |
| C-001 | minor | V2 on passability, V1 on clarity | SPEC:815 does not require two copies; needs explicit folding instructions |
| C-002 | minor | V1 = V3 | P4:25 against P4:65 |
| C-003 | Medium | V2 detection | P4:61 requires the rewrite, P4:65 checks "stays open for verification" anywhere |
| C-004 | Medium | V3 | S3:183 checks only "that's never minor"; P4:49 also needs the heading gone |
| C-005 | minor | V1 = V3 | P4:114 against S1:234; read-first fallback prevents failure |
| C-006 | blocking | V2 with qualification | BRIEF:16 says "no plugin parity test (T15)" but also that the owner "has not confirmed removing plugin parity"; Q:44; SPEC:948 |
| C-007 | blocking | V2 | SPEC:867; P4:135 only verifies that the summary names the pointers |
| C-008 | Medium, advisory | V1 | skill_template.md:834 "if you can't verify it, it fails" needs triage |
| C-009 | blocking | V1 on discovery | SPEC:739 requires "narrow 'CRITICAL is blocking'"; P4:90 keeps it; a test pin is not authorization |
| C-010 | minor | complementary | P4:27, P4:39 |
| C-011 | minor | V2 | matrix omits source.md:29 and :30 units; P4:98 and P4:120 include the work |
| X-001 | minor | V2 | SPEC:815 preserves the cap text, not its location |
| X-002 | blocking | V2 with qualification | Q:83 "reassess plugin parity, not to remove it: confirm" |
| X-003 | Medium | V2 | compliant execution remains possible |

A-002: QUALIFY (plans establish intended dependencies, not delivered files). A-003: QUALIFY (a permitted implementation satisfying the literal count defeats a blocking claim).

Concessions: V2 overgraded C-003 and overlooked C-009; the C-006 case must acknowledge the contrary shared brief; the unresolved issue is owner confirmation.

## Variant 3 advocate (refactorer, opus)

Position: V3 has the best-checked findings, but its blocking grade on C-001 does not survive the grading rule (P4's text allows a reading where the count prints 1). C-001 is Medium; V3 then has no blocking finding left, so the verdict that follows is PASS with Medium findings.

Steelman V1: C-001 has two readings (keep: 2; fold: 1, but the count was already 1 before the edit); V1 lists the most sibling doubt lines. Steelman V2: a spec obligation (SPEC:948) is dropped on the plan author's own reassessment and the owner did not approve it (Q:44, Q:83); the positive greps are satisfied by the digest alone; C-001 is "not proved unpassable".

| point | grade defended | superior | evidence |
|---|---|---|---|
| S-001 | PASS with Medium findings | V1 nearer | once C-001 is Medium, no verified blocking finding remains |
| C-001 | Medium | V1 | P4:39 "near lines 161 to 163" (agent_template_qa.md:163 is the cap bullet); P4:45; SPEC:815; no test pins the separate bullet (cap_edits.yaml has no row for lines 163, 830, 646, 657 or the prompt cap lines; test_review_severity_rule.py:198-201 checks flattened text); S3:142 keeps the bullet in pragmatic.md so an executor copying stage 3 gets 2 and halts |
| C-002 | minor | V1 = V3 | P4:25 against P4:65 |
| C-003 | Medium | V3 diagnosis, one step up | the digest supplies both tokens; principle 8 in three prompts holds no banned word |
| C-004 | Medium | V3 | rf-qa-qualitative.md:990 heading; S3:183 checks only "that's never minor" |
| C-005 | minor | V1 slightly ahead (monkeypatch point) | P4:114 against S1:234 |
| C-006 | minor; owner-tracking item, not a P4 defect | V1 = V3 | BRIEF:16 "Do not create any new plugin surface"; P4:23 and P4:129 disclose it |
| C-007 | minor | V1 | P4:26 records it with reasons; roadmap/SKILL.md already holds "open blocking findings"; SPEC:948 excludes the pointers |
| C-008 | Medium | V1 (broader) | prompt lines :125 and doc_code :206 sit beside the digest, no task edits or names them |
| C-009 | minor | V1 | SPEC:739 against P4:90, no Constraints line |
| C-010 | minor | V1 | P4:27; P4:52 omits the two cli/ rows |
| C-011 | minor | V2 | work is in the tasks |
| X-001 | Medium, met by the fold | V1 | same as C-001 |
| X-002 | not blocking | V1 = V3 | BRIEF:16; Q:83 |
| X-003 | Medium | V3 nearer than V2 | checks pass but prove nothing |

A-002: QUALIFY (C-004 shows stage 3 can pass its own checks and still break P4:49). A-003: QUALIFY (a count reachable by an allowed reading is not unpassable; decides C-001).

Concessions: V3-F1's blocking grade breaks the grading rule (keeping the bullet is not the only allowed reading; the sentence survives inside the digest; in three templates the bullet sits between S2 and S5 so keeping it leaves a visible duplicate); V3 rated C-003 and C-004 minor where Medium fits; V3 missed C-008 prompt lines, C-009 and two C-010 items. V3's fix is still correct and cheap: state whether the cap bullet is folded and set the expected count to match.

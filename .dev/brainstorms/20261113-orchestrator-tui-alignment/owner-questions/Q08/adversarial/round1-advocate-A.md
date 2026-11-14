# Round 1: advocate for variant 1 (proposal A: neither now; post the honest status line; write the record at release 3)

Sources, all read 2026-11-14: `merged-requirements.md` (MR) lines 226-282 and 535; `alignment-findings-adjudicated.md` (ADJ) lines 86, 186-196, 326-327, 515-575, 778; `origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (RG); sibling `issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` (OD08, untracked); `origin/master:.dev/issues/409/owner-decisions-20261111.md` (OD11).

## 1. Position summary

Let the #409 correction pass post BC-18 as proposed ("not met as recorded"), keep acceptance criterion 1 unchanged, and have the owner write the direction-selection record as release 3's first step, when the gate's release-3 fields (post-link choice, fallback date) are knowable. A is the only variant that makes #409 true today at near-zero owner cost without creating a record or a criterion that has to be revisited at release 3.

## 2. Steelman of each opposing variant

**B (amend criterion 1).** The project never followed a one-shot "select a direction, then integrate" model; the owner chose a staged direction on 2026-11-08 (OD08:5-8) and the gate file on master itself calls that staging "binding" (RG:3). Measuring shipped work against a model nobody used produces a permanent false "not met". Rewriting the criterion to describe the staged selection that actually happened, citing the owner's own records, costs no new document, makes #409 describe reality, and removes the blocker on release 3 in one step. The owner saying "this staging is the selection" is exactly the answer OD08:9 and RG:3 say only the owner can give.

**C (write the one-paragraph record now).** This is the spec's recommendation (MR:535; ADJ:778) and closes what the debate called the only open item on the observer's direction (ADJ:327, A-003, 96 percent). It keeps the criterion untouched, so nobody can say the bar was moved; it is short to write because it can cite the 2026-11-08 and 2026-11-11 decisions; and, uniquely, it puts the owner's reading of "production integration" in writing (diff-analysis U-003). Without that reading the gate file's stricter default applies indefinitely (RG:34), so every later reader keeps arguing about whether the shipped command breached the criterion. C ends that argument at its source.

## 3. Strengths claimed

1. **#409 becomes true now, with no invented record.** ADJ's own disposition table lists BC-18 under "post as written, after re-pinning", waiting for Q8 only "if the owner prefers to amend the criterion" (ADJ:546). A follows that disposition. The spec's default instead posts OB-08 "without BC-18's status line" (MR:535), which leaves #409 silent on a criterion the debate found unmet. A is more honest than the default.
2. **The status line is correct under the gate rule now in force.** RG:34: "Until the owner confirms one in the selection record, the stricter reading applies." Reading 1 (RG:31) is "the first change that registers `superclaude observe` in the shipped CLI", and the command is registered (ADJ:521; MR:232). The phrase "not met as recorded" is also true under any reading, because no record exists (ADJ:86).
3. **One record, all fields, written once.** The gate's evidence rule asks the record to hold "post-link choice or explicit deferral, fallback date, stack confirmation, command name, confirmed production-integration reading" (RG:22). The post-link choice belongs to release 3 (RG:13: "Optional owner re-confirm of the post-link default (B or C)"). A record written now either omits those fields (C's own concession) or must be re-confirmed later, since RG:25 says "a later gate that changes what a direction can show ... triggers a re-confirm", and QUESTION-LINK is plausibly such a gate (PLAN INFERENCE). Writing at release 3 avoids writing twice.
4. **Blocking release 3 costs almost nothing today.** OB-09 is DEFERRED (L4) and is also blocked by OB-06, XC-05, Q19, Q17 and, if Q17 = yes, SW-11 (MR:257, blocked-by column). Removing OB-02 from that list now does not let release 3 start; A spends no owner attention on a blocker that is not the binding one.
5. **No new authorship problem.** RG:22 requires the record to be "written by the owner, never an agent". A asks for nothing to be written until the owner is ready, so nothing gets drafted under time pressure and later disputed.

## 4. Weaknesses identified in the others

1. **B cites evidence the gate rule disallows.** OD08:3 says the 2026-11-08 record was "Recorded by an Orca worker ... from the coordinator's relay of the owner's order". RG:22 requires a record "written by the owner, never an agent". An amended criterion whose evidence is OD08 rests on an agent-written file, and OD08 is not on master (MR:235; Q7). OD11's authorship is not stated beyond "owner replies in the coordinator session" (OD11:3); UNVERIFIED who wrote that file.
2. **B moves the bar and still leaves the gate closed.** RG:10 says DIRECTION-SELECTED is "not shown to have passed; owner to say"; RG:11 makes R1 conditional on it. Amending #409 alone does not change RG:22; B needs a second amendment to the gate file (B concedes this). That is two edits to accepted criteria made after the fact, the "moving the goalposts" risk B itself lists.
3. **C's "met" may be untrue on the criterion's own words.** Criterion 1 is "A human selects the visual direction before production integration" (ADJ:535). A record dated after the 2026-11-11 merge that registered the command (MR:232) satisfies "before" only if the owner's reading of production integration is something not yet done (for example Reading 2, RG:32), or if the record dates the selection to 2026-11-08 and the owner accepts that as the selection. C's proposed status line "met by the owner's record of <date>" is therefore conditional on the reading, and C does not say so.
4. **C's three-item paragraph does not meet RG:22 as written.** C names direction, reading and command name; RG:22 also requires date, option and decider, the default while no question rows exist, the default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date and stack confirmation. C concedes the owner must add them or declare the gate met without them; either way the "one paragraph" grows, or a second record is needed at release 3 (C's own "What stays unresolved").
5. **Both B and C depend on Q7 first.** Each cites OD08, which is untracked in the sibling worktree (MR:235; ADJ:191, action 3). Until OB-01 lands, the citation points at a path readers cannot open. A cites nothing new.

## 5. Concessions

1. #409 will publicly say a criterion is "not met" for merged work, which reads as a defect even though the gap is a missing document.
2. A does not resolve the owner's reading of "production integration" (diff-analysis A-002, U-003). Until then RG:34's strict default stays in force, and the status line's second sentence implicitly takes Reading 1.
3. A leaves open the item ADJ:327 calls the only open item, against the spec's recommendation (MR:535; ADJ:778).
4. A does not test whether the staged direction is still what the owner wants (A-001); a record written at release 3 only records that later.
5. "Release 3's first step" has no date; release 3 is DEFERRED (MR:257), so the record may never be written, and RG:10's "not shown to have passed" stays on master indefinitely.
6. A still needs an owner act: the owner must say BC-18 may post, because the spec default withholds it (MR:535). It is less effort than B or C, not zero.
7. The 2026-11-08 decision remains evidenced only by an untracked, agent-recorded file until Q7 is answered; A does nothing about that.

## 6. Shared assumptions

- **A-001 (the recorded staged direction is still current): QUALIFY.** It is consistent with the evidence: release 2 was merged on 2026-11-12 under the 2026-11-11 decisions (MR:232; OD11:8-9), after the staging was set. But only the owner can confirm it. A is the variant least exposed to it, because A writes nothing that would freeze a possibly stale direction; C is the variant that would test it directly.
- **A-002 (registering the command counts as production integration): QUALIFY.** It is not an invention: RG:31 defines Reading 1 that way and RG:34 makes the stricter reading apply until the owner chooses. It is the default in force, not the owner's settled reading. BC-18's core claim, "not met as recorded", holds under either reading because no record exists; its supporting sentence about registration is decisive only under Reading 1.

## 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (A = B = C) | 50% | Same five sections; no merit difference. |
| C-001 instrument used now | C | 65% | A real owner-written record closes the gap RG:22 describes; A only reports it, B substitutes a criterion change. |
| C-002 #409 text after OB-08 | A | 60% | "Not met as recorded" is true today under every reading; C's "met" depends on the reading (section 4 item 3); B's text is new rather than corrected. |
| C-003 release 3 unblocked | A | 55% | OB-09 has other blockers (MR:257), so unblocking OB-02 now buys little, and a release-3-time record can carry the release-3 fields. |
| C-004 gate field list (RG:22) | A | 65% | Only A times the record to when the post-link choice and fallback date exist; B and C both admit a gap. |
| C-005 owner effort now | A | 70% | Only an approval to post BC-18; B and C need authored text. |
| X-001 does "Stage it" already count | C | 70% | OD08:3 shows the record was agent-recorded and RG:22 requires owner-written, so a separate owner record is needed; A leaves this open, B asserts yes against the rule. |
| X-002 is changing the criterion legitimate | A = C (against B) | 70% | Both keep the criterion unchanged; B rewrites an acceptance criterion to fit work already done. |
| A-001 | C | 60% | Writing in the owner's own words now confirms the direction is current; A defers the check. |
| A-002 | C | 70% | C's paragraph fixes the reading; A and B leave RG:34's default in force. |

## 8. Overall verdict

Pick **C, combined with two parts of A**, at 65 percent confidence. The owner writes the record now and covers every RG:22 field, writing "deferred to release 3" for the post-link choice and fallback date instead of leaving them out. If the record is not written in W1, OB-08 posts BC-18 as proposed (A) rather than the spec default, which leaves the status line out. Reason: C is the only answer that closes the gate in the owner's own words, and A's two contributions keep #409 honest in the meantime and stop C's short paragraph from failing the gate's field list.

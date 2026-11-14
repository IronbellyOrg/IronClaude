# Adversarial Debate Transcript: Q8 owner-answer proposals

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (10 of 10 points agreed by at least 2 of 3 advocates; S-001 a unanimous tie)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (spawned in parallel as separate agents; each wrote its own file)
- Variant mapping: variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C
- Orchestrator spot-check (2026-11-14): `owner-decisions-20261108.md:3` reads "Recorded by an Orca worker ... from the coordinator's relay of the owner's order"; `origin/master` `release-gates.md:28-34` gives two "production integration" readings, "both UNVERIFIED", and "Until the owner confirms one in the selection record, the stricter reading applies: offline work only (R0)"; `acceptance-tests.md:14` maps "A human selects the visual direction" to reviewer check AC-S, and `:70` lists the fields AC-S checks and says "No agent writes the record". All confirmed.

## Round 1: Advocate Statements

### Advocate for proposal A (source file: round1-advocate-A.md)

## Round 1: advocate for variant 1 (proposal A: neither now; post the honest status line; write the record at release 3)

Sources, all read 2026-11-14: `merged-requirements.md` (MR) lines 226-282 and 535; `alignment-findings-adjudicated.md` (ADJ) lines 86, 186-196, 326-327, 515-575, 778; `origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (RG); sibling `issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` (OD08, untracked); `origin/master:.dev/issues/409/owner-decisions-20261111.md` (OD11).

### 1. Position summary

Let the #409 correction pass post BC-18 as proposed ("not met as recorded"), keep acceptance criterion 1 unchanged, and have the owner write the direction-selection record as release 3's first step, when the gate's release-3 fields (post-link choice, fallback date) are knowable. A is the only variant that makes #409 true today at near-zero owner cost without creating a record or a criterion that has to be revisited at release 3.

### 2. Steelman of each opposing variant

**B (amend criterion 1).** The project never followed a one-shot "select a direction, then integrate" model; the owner chose a staged direction on 2026-11-08 (OD08:5-8) and the gate file on master itself calls that staging "binding" (RG:3). Measuring shipped work against a model nobody used produces a permanent false "not met". Rewriting the criterion to describe the staged selection that actually happened, citing the owner's own records, costs no new document, makes #409 describe reality, and removes the blocker on release 3 in one step. The owner saying "this staging is the selection" is exactly the answer OD08:9 and RG:3 say only the owner can give.

**C (write the one-paragraph record now).** This is the spec's recommendation (MR:535; ADJ:778) and closes what the debate called the only open item on the observer's direction (ADJ:327, A-003, 96 percent). It keeps the criterion untouched, so nobody can say the bar was moved; it is short to write because it can cite the 2026-11-08 and 2026-11-11 decisions; and, uniquely, it puts the owner's reading of "production integration" in writing (diff-analysis U-003). Without that reading the gate file's stricter default applies indefinitely (RG:34), so every later reader keeps arguing about whether the shipped command breached the criterion. C ends that argument at its source.

### 3. Strengths claimed

1. **#409 becomes true now, with no invented record.** ADJ's own disposition table lists BC-18 under "post as written, after re-pinning", waiting for Q8 only "if the owner prefers to amend the criterion" (ADJ:546). A follows that disposition. The spec's default instead posts OB-08 "without BC-18's status line" (MR:535), which leaves #409 silent on a criterion the debate found unmet. A is more honest than the default.
2. **The status line is correct under the gate rule now in force.** RG:34: "Until the owner confirms one in the selection record, the stricter reading applies." Reading 1 (RG:31) is "the first change that registers `superclaude observe` in the shipped CLI", and the command is registered (ADJ:521; MR:232). The phrase "not met as recorded" is also true under any reading, because no record exists (ADJ:86).
3. **One record, all fields, written once.** The gate's evidence rule asks the record to hold "post-link choice or explicit deferral, fallback date, stack confirmation, command name, confirmed production-integration reading" (RG:22). The post-link choice belongs to release 3 (RG:13: "Optional owner re-confirm of the post-link default (B or C)"). A record written now either omits those fields (C's own concession) or must be re-confirmed later, since RG:25 says "a later gate that changes what a direction can show ... triggers a re-confirm", and QUESTION-LINK is plausibly such a gate (PLAN INFERENCE). Writing at release 3 avoids writing twice.
4. **Blocking release 3 costs almost nothing today.** OB-09 is DEFERRED (L4) and is also blocked by OB-06, XC-05, Q19, Q17 and, if Q17 = yes, SW-11 (MR:257, blocked-by column). Removing OB-02 from that list now does not let release 3 start; A spends no owner attention on a blocker that is not the binding one.
5. **No new authorship problem.** RG:22 requires the record to be "written by the owner, never an agent". A asks for nothing to be written until the owner is ready, so nothing gets drafted under time pressure and later disputed.

### 4. Weaknesses identified in the others

1. **B cites evidence the gate rule disallows.** OD08:3 says the 2026-11-08 record was "Recorded by an Orca worker ... from the coordinator's relay of the owner's order". RG:22 requires a record "written by the owner, never an agent". An amended criterion whose evidence is OD08 rests on an agent-written file, and OD08 is not on master (MR:235; Q7). OD11's authorship is not stated beyond "owner replies in the coordinator session" (OD11:3); UNVERIFIED who wrote that file.
2. **B moves the bar and still leaves the gate closed.** RG:10 says DIRECTION-SELECTED is "not shown to have passed; owner to say"; RG:11 makes R1 conditional on it. Amending #409 alone does not change RG:22; B needs a second amendment to the gate file (B concedes this). That is two edits to accepted criteria made after the fact, the "moving the goalposts" risk B itself lists.
3. **C's "met" may be untrue on the criterion's own words.** Criterion 1 is "A human selects the visual direction before production integration" (ADJ:535). A record dated after the 2026-11-11 merge that registered the command (MR:232) satisfies "before" only if the owner's reading of production integration is something not yet done (for example Reading 2, RG:32), or if the record dates the selection to 2026-11-08 and the owner accepts that as the selection. C's proposed status line "met by the owner's record of <date>" is therefore conditional on the reading, and C does not say so.
4. **C's three-item paragraph does not meet RG:22 as written.** C names direction, reading and command name; RG:22 also requires date, option and decider, the default while no question rows exist, the default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date and stack confirmation. C concedes the owner must add them or declare the gate met without them; either way the "one paragraph" grows, or a second record is needed at release 3 (C's own "What stays unresolved").
5. **Both B and C depend on Q7 first.** Each cites OD08, which is untracked in the sibling worktree (MR:235; ADJ:191, action 3). Until OB-01 lands, the citation points at a path readers cannot open. A cites nothing new.

### 5. Concessions

1. #409 will publicly say a criterion is "not met" for merged work, which reads as a defect even though the gap is a missing document.
2. A does not resolve the owner's reading of "production integration" (diff-analysis A-002, U-003). Until then RG:34's strict default stays in force, and the status line's second sentence implicitly takes Reading 1.
3. A leaves open the item ADJ:327 calls the only open item, against the spec's recommendation (MR:535; ADJ:778).
4. A does not test whether the staged direction is still what the owner wants (A-001); a record written at release 3 only records that later.
5. "Release 3's first step" has no date; release 3 is DEFERRED (MR:257), so the record may never be written, and RG:10's "not shown to have passed" stays on master indefinitely.
6. A still needs an owner act: the owner must say BC-18 may post, because the spec default withholds it (MR:535). It is less effort than B or C, not zero.
7. The 2026-11-08 decision remains evidenced only by an untracked, agent-recorded file until Q7 is answered; A does nothing about that.

### 6. Shared assumptions

- **A-001 (the recorded staged direction is still current): QUALIFY.** It is consistent with the evidence: release 2 was merged on 2026-11-12 under the 2026-11-11 decisions (MR:232; OD11:8-9), after the staging was set. But only the owner can confirm it. A is the variant least exposed to it, because A writes nothing that would freeze a possibly stale direction; C is the variant that would test it directly.
- **A-002 (registering the command counts as production integration): QUALIFY.** It is not an invention: RG:31 defines Reading 1 that way and RG:34 makes the stricter reading apply until the owner chooses. It is the default in force, not the owner's settled reading. BC-18's core claim, "not met as recorded", holds under either reading because no record exists; its supporting sentence about registration is decisive only under Reading 1.

### 7. Per-point positions

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

### 8. Overall verdict

Pick **C, combined with two parts of A**, at 65 percent confidence. The owner writes the record now and covers every RG:22 field, writing "deferred to release 3" for the post-link choice and fallback date instead of leaving them out. If the record is not written in W1, OB-08 posts BC-18 as proposed (A) rather than the spec default, which leaves the status line out. Reason: C is the only answer that closes the gate in the owner's own words, and A's two contributions keep #409 honest in the meantime and stop C's short paragraph from failing the gate's field list.

### Advocate for proposal B (source file: round1-advocate-B.md)

## Round 1: advocate for variant B (amend #409 acceptance criterion 1)

Sources read for this statement (2026-11-14): the three variants, `diff-analysis.md`, `../question.md`; `merged-requirements.md` lines 226-282 and 535; `alignment-findings-adjudicated.md` (ADJ) lines 86, 186-196, 326-327, 515-575, 778; `origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md` lines 20-34; `origin/master:.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md` lines 14 and 70 (opened to check what "AC-S" requires); the sibling `owner-decisions-20261108.md` (untracked); `origin/master:.dev/issues/409/owner-decisions-20261111.md`.

### 1. Position summary

B says: stop measuring the shipped observer against a one-shot "select, then integrate" criterion the project did not follow, and rewrite #409's acceptance criterion 1 so it names the staged selection the owner already made, citing the owner's 2026-11-08 and 2026-11-11 records. Having checked the gate files, I hold that B's diagnosis (the decision exists already; the issue should describe the staged model) is right, but B's instrument (rewriting the criterion) costs more than it appears and is weaker than C's owner-written paragraph; my honest verdict is C, carrying B's citations.

### 2. Steelman of each opposing variant

**A (do neither now; post the honest "not met as recorded" status line; write the record when release 3 is next).** Strongest form: the only thing provably wrong today is that #409 implies a record exists; BC-18 fixes that at once with zero owner time and without inventing or back-dating anything (ADJ:535). The gate's evidence list includes items that belong to release 3 and are not known today, "post-link choice or explicit deferral, fallback date" (`release-gates.md:22`), so one record written at release 3's start can be complete instead of partial. Q8 gates only OB-02, BC-18 and OB-09 (`merged-requirements.md:535`), and OB-09 is DEFERRED (L4) and also blocked by OB-06, XC-05, Q19 and Q17 (`merged-requirements.md:257`), so deferring the record costs no schedule now.

**C (owner writes one dated paragraph now; AC 1 unchanged and then met).** Strongest form: the gate on master already defines exactly this instrument, "a dated selection record written by the owner, never an agent" (`release-gates.md:22`), checked by reviewer check AC-S (`release-gates.md:27`; `acceptance-tests.md:70`). The gate also says the production-integration reading is confirmed "in the selection record", and "Until the owner confirms one in the selection record, the stricter reading applies: offline work only (R0)" (`release-gates.md:34`). C is the only variant that resolves that line, keeps the bar where it was, and gives every later reader one owner-written file to cite. It is also short: it can cite the existing 2026-11-08 and 2026-11-11 decisions.

### 3. Strengths claimed

1. **The substance already exists in owner decisions; B does not ask the owner to re-decide.** The 2026-11-08 record states "Staged direction chosen ("Stage it")" with the three stages (sibling `owner-decisions-20261108.md:5-8`) and later "Stack and release-1 scope CONFIRMED ... Python + Rich with snapshot export" (same file, line 17). The 2026-11-11 record on master adds decisions 8 and 6 for phase 2. ADJ rates "only the selection record is open" at 96 percent (ADJ:327, A-003).
2. **B describes what actually happened, which is the honest frame for a criterion written for a one-shot choice.** AC 1 reads "A human selects the visual direction before production integration" (ADJ:535). The project instead chose a staged direction whose later stages wait on gates (QUESTION-OBSERVATION, QUESTION-LINK; `owner-decisions-20261108.md:6-8`). ADJ's own BC-04 and BC-10 replacement texts already use the staged framing ("The owner chose a staged direction on 2026-11-08 ...", ADJ:521; "Releases 1 and 2 were built on the owner's staged direction of 2026-11-08, before a dated selection record existed", ADJ:527). Amending AC 1 aligns the criterion with the rest of the corrected body.
3. **B unblocks OB-09 on this point without a new file whose location is undecided.** C's record has no agreed home ("location is the owner's; UNVERIFIED where", `merged-requirements.md:250`); B's text lives in the #409 body, whose history is the undo path (`merged-requirements.md:256`, OB-08 undo "yes (issue history)").
4. **B gives the owner's answer to the open sentence in the 2026-11-08 record.** That record says "Whether this fully satisfies the DIRECTION-SELECTED gate is for the owner to say" (`owner-decisions-20261108.md:9`). B is the owner saying yes, and B's own text requires that it be written as such (variant-2, "What it costs or risks", last bullet).

### 4. Weaknesses identified in the others

1. **A leaves the project in standing contradiction with its own gate.** `release-gates.md:34` says that until the owner confirms a reading "in the selection record, the stricter reading applies: offline work only (R0)", and Reading 1 is "the first change that registers `superclaude observe` in the shipped CLI" (`release-gates.md:31`). Releases 1 and 2 are merged and registered (`merged-requirements.md:232`). A keeps that contradiction open until release 3, with no date. A's reason to wait is also weak: the gate already allows "post-link choice **or explicit deferral**" (`release-gates.md:22`) and has a "Stale" clause that triggers a re-confirm when a later gate changes what a direction can show (`release-gates.md:25`), so a record written now does not lose the ability to cover release 3 later.
2. **A publishes "not met" for something that may in substance be met.** The owner chose the staged direction on 2026-11-08 (`owner-decisions-20261108.md:5`); release 1 merged on 2026-11-11 (`merged-requirements.md:232`). The selection preceded the integration; only the owner-written record is missing. "Not met as recorded" is accurate as far as it goes, but A makes it the public state for an open-ended period when one owner paragraph would replace it.
3. **C's "met" status line is honest only if the paragraph states the 2026-11-08 selection date, not just its own date.** AC 1 says "before production integration". A record dated 2026-11-14 or later cannot by itself show a selection before 2026-11-11. C names "documents rather than precedes" as a cost (variant-3), but its proposed BC-18 text, "met by the owner's record of <date>, path", cites only the record's date. Unless the paragraph says the selection was made on 2026-11-08, the "met" line overstates.
4. **C's three named items fall short of the gate's field list.** The record "Holds: default while no question rows exist, default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date, stack confirmation, command name, confirmed production-integration reading" and "Names the date, option and decider, and where the owner's statement lives" (`release-gates.md:22`); reviewer check AC-S lists the same fields (`acceptance-tests.md:70`). C concedes this (variant-3), but the spec's Q8 row and OB-02 still say three items (`merged-requirements.md:250`, :535). A three-item paragraph fails AC-S as written.

### 5. Concessions

1. **Amending AC 1 does not clear the gate; it moves the work into two more files.** The criterion's sentence is mapped to reviewer check AC-S (`acceptance-tests.md:14`), and AC-S requires an owner-written record with the named fields (`acceptance-tests.md:70`; `release-gates.md:22`). Changing the issue text leaves both files on master unchanged. B's "either satisfied by the cited records or amended in the same change" (variant-2) understates this: OB-08 runs on "GitHub only" (`merged-requirements.md:256`), so the gate and acceptance-test files need a separate repo change and PR that B does not plan.
2. **The records B cites cannot satisfy the gate's authorship rule.** The 2026-11-08 record says "Recorded by an Orca worker (run run_93bfa00cae2b, task task_bfe724db1dac) from the coordinator's relay of the owner's order" (`owner-decisions-20261108.md:3`), which fails "written by the owner, never an agent" (`release-gates.md:22`). Who wrote the 2026-11-11 record is not stated there ("Source: owner replies in the coordinator session"); UNVERIFIED. So "the cited records satisfy the gate" is not available; B in practice requires amending the gate.
3. **The 2026-11-08 record is not on master** (`merged-requirements.md:235`; Q7), so B's citation points at a file readers cannot open until OB-01 lands.
4. **B leaves the production-integration reading undecided**, and `release-gates.md:34` makes that reading the switch between "offline work only (R0)" and shipped work. B's example criterion no longer mentions production integration, which hides the question instead of answering it.
5. **Moving the bar after the fact is a real cost, and here an unnecessary one.** Given section 4 point 2 (the selection preceded the merge in fact), the criterion does not need rewriting to be truthfully met; it needs an owner-written record. That removes B's main justification.
6. **B is not less owner work than C.** B needs the owner to supply or approve word-for-word replacement text (variant-2), plus a gate amendment; C needs one paragraph. If "approve word for word" means an agent drafts it, that sits close to the authorship pattern the gate forbids.

### 6. Shared assumptions

- **A-001 (the recorded staged direction is still current): QUALIFY.** The 2026-11-11 record on master acts on the same plan (phase 2 permission for one named Run), which is evidence the direction held at least to 2026-11-11. After that it is the owner's knowledge only. Whatever is chosen, the owner's text should say in one clause that the staged direction still stands; B and C both give the owner that chance, A does not until release 3.
- **A-002 (shipping the CLI command counts as "production integration"): QUALIFY.** It is not the owner's reading: both readings in the gate are marked "UNVERIFIED as the issue's intent" (`release-gates.md:29`). But the gate makes it the operative reading for now: Reading 1 names registration in the shipped CLI (`release-gates.md:31`), and "Until the owner confirms one in the selection record, the stricter reading applies" (`release-gates.md:34`). Whether Reading 2 ("wires or enables the observer in the shipped product", line 32) also covers registration is UNVERIFIED. So BC-18's premise holds under the gate's own default, and only an owner-written selection record (C) is defined as the place to change it.

### 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 | C (tie; a letter is required) | 50% | All three use the same five sections; nothing to judge. |
| C-001 (instrument used now) | C | 70% | The gate on master defines an owner-written record as the instrument (`release-gates.md:22`); amending AC 1 leaves AC-S and the gate unmet (`acceptance-tests.md:14, 70`). |
| C-002 (what #409 says about AC 1) | C | 65% | "Met" is truthful if the paragraph states the 2026-11-08 selection date (before the 2026-11-11 merge); without that, A's "not met as recorded" is the honest line. |
| C-003 (release 3 unblocked) | C | 60% | B and C both clear OB-02's edge, but B's clearing also needs gate and acceptance-test amendments it does not plan; OB-09 has other blockers either way. |
| C-004 (gate field list) | C | 65% | C faces the list and lets the owner include, waive or defer fields; B needs the gate amended; A's "cover it later" is unnecessary since "explicit deferral" is allowed now. |
| C-005 (owner effort now) | A | 80% | A asks nothing of the owner now; B and C each need owner text. |
| X-001 (does "Stage it" already count) | C | 75% | The 2026-11-08 record was written by an Orca worker (`owner-decisions-20261108.md:3`), so it cannot be the gate's record; the decision counts in substance, the record must be owner-written. |
| X-002 (legitimacy of changing AC 1) | C | 70% | The selection (2026-11-08) preceded the merge (2026-11-11), so AC 1 can be met as written once recorded; rewriting it is unnecessary and reads as moving the bar. |
| A-001 (staged direction still current) | C | 55% | An owner paragraph in the owner's own words re-confirms currency most directly; B's approval does so implicitly; A defers it. |
| A-002 (registration = production integration) | C | 75% | `release-gates.md:34` names the selection record as where the reading is confirmed; only C writes that record now. |

### 8. Overall verdict

Pick **C, carrying B's citations**: the owner writes one dated paragraph that (a) states the staged direction was selected on 2026-11-08 and still stands, citing the 2026-11-08 and 2026-11-11 decisions; (b) gives the owner's reading of "production integration"; (c) names `superclaude observe`; and (d) covers, waives or explicitly defers the remaining `release-gates.md:22` fields (the stack confirmation is already in the 2026-11-08 record; post-link choice and fallback date can be "explicit deferral"). BC-18 then posts as "met: selected 2026-11-08, recorded <date>, <path>". Confidence 70 percent. Reason: the gate on master already defines an owner-written record as the evidence, and the selection did precede the merge, so writing the record meets AC 1 as written; amending AC 1 (my variant) leaves the gate and AC-S unmet and needs a second repo change it does not plan.

### Advocate for proposal C (source file: round1-advocate-C.md)

## Round 1 advocate statement: proposal C (variant-3, write the one-paragraph record now)

Debate: Q8, sc:adversarial Mode A, depth quick, Round 1. Written 2026-11-14.

Sources read for this statement: `question.md`; variant-1/2/3; `diff-analysis.md`; `merged-requirements.md` lines 226-282 and 535 (abbreviated MR); `alignment-findings-adjudicated.md` lines 86, 186-196, 326-327, 515-575, 778 (abbreviated ADJ); `origin/master:.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (abbreviated RG; line numbers from `git show ... | grep -n`, 2026-11-14); sibling `issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md` (abbreviated OD-1108); `origin/master:.dev/issues/409/owner-decisions-20261111.md` (abbreviated OD-1111).

### 1. Position summary

The owner should write one dated paragraph now, in their own words, that records the staged direction, the owner's reading of "production integration" and the command name, and #409's acceptance criterion 1 should stay as written and be cited as met by that record. The gate on master says the production-integration reading can only be confirmed "in the selection record" (RG:34), so no other answer settles that point. The paragraph should also cover, or explicitly defer, the other fields the gate lists (RG:22). My original proposal named only three fields, and that is a gap.

### 2. Steelman of each opposing variant

**Proposal A (do neither now; post the honest "not met" line; write the record when release 3 is next).** At its strongest, A refuses to produce paperwork after the fact just to make a shipped release look compliant. The record would document a selection that releases 1 and 2 already acted on. A makes #409 truthful at once with BC-18's status line (ADJ:535 row 18). It costs the owner nothing today. And it times the record for the moment when release 3's own gate fields are actually decidable: "post-link choice or explicit deferral" and "fallback date" (RG:22). Release 3 is DEFERRED (L4) and has other blockers anyway (MR:257, OB-09 is blocked by OB-06, XC-05, Q19 and Q17), so holding OB-02 until then delays almost nothing. The honest status line also matches the gate's own default: until the owner confirms a reading, "the stricter reading applies" (RG:34), and under the stricter Reading 1, registering the command is production integration (RG:31). So "not met as recorded" is the correct statement under the gate's current text.

**Proposal B (amend acceptance criterion 1 to match the staged selection).** At its strongest, B says the criterion assumed a one-shot "pick a visual direction first" model that the project never followed. The direction was chosen in staged form (ADJ X-018, line 326), and the gate file itself already calls the staging "binding" (RG:3). Rewriting the criterion to describe what actually happened, citing records that already exist, avoids writing a new document. It also stops #409 from measuring shipped work against a model the owner deliberately replaced. Spec documents that describe reality are better than spec documents that preserve an outdated plan and then mark it failed.

### 3. Strengths claimed

1. **Only the selection record can carry the production-integration reading.** The gate lists two readings, "both UNVERIFIED as the issue's intent" (RG:29), and says: "Until the owner confirms one in the selection record, the stricter reading applies" (RG:34). The R1 gate also says "production integration permitted under the reading the owner confirms" (RG:11). A amends nothing and leaves the reading unconfirmed. B amends the criterion text but has no place to put the reading unless the gate is also edited. C supplies the reading through the instrument the gate already names.
2. **It meets the authorship rule, which the existing records do not clearly meet.** The gate requires "a dated selection record written by the owner, never an agent" (RG:22). OD-1108 opens: "Recorded by an Orca worker (run run_93bfa00cae2b, task task_bfe724db1dac) from the coordinator's relay of the owner's order" (OD-1108:3). It is a worker-written record of a relayed order, and it defers the question itself: "Whether this fully satisfies the DIRECTION-SELECTED gate is for the owner to say" (OD-1108:9; repeated at RG:3 and RG:10). OD-1111 is "owner replies in the coordinator session" (OD-1111:3), and who typed the file is UNVERIFIED. It covers decisions 8 and 6 (question scope and read permission), not the direction (OD-1111:8-9). An owner-written paragraph is the one artifact that unambiguously meets RG:22.
3. **The bar stays where it was.** Criterion 1 is kept verbatim: "A human selects the visual direction before production integration." (ADJ:535 row 18). Readers of #409 see a criterion and a citation, not a rewritten target.
4. **It closes the one open item the review found.** ADJ A-003 (96 percent, line 327): "Observer built; only the selection record is open". ADJ X-018 (line 326) names the action "Q8: write the AC-S record". It is also the spec's recommended answer: "Write the record (one paragraph)" (MR:535; ADJ:778).
5. **It is cheap, because the content already exists.** The staged direction is already stated (OD-1108:5-8; RG:3), the stack is confirmed (OD-1108:17), and the command name is `superclaude observe` (MR:232). The owner adds a date, the reading, a statement that this is the selection, and their own authorship.
6. **It unblocks both dependent items on this point.** OB-02 blocks OB-08's BC-18 and OB-09 (MR:250). With the record, BC-18 can point at it instead of waiting (MR:256 (5): "BC-18 waits for Q8").

### 4. Weaknesses identified in the others

1. **A leaves the reading undecided and states a conclusion that depends on it.** BC-18's "not met as recorded" assumes that registering the command was production integration (diff-analysis A-002). That is true only under Reading 1 (RG:31). Under Reading 2, "the first change that wires or enables the observer in the shipped product" (RG:32), the owner might say otherwise. A publishes the conclusion and never asks for the reading. The gate's stricter-reading default (RG:34) partly defends A, but that default is a placeholder pending the owner, not a finding.
2. **A publishes a "not met" line on merged work with no end date except release 3**, and release 3 is DEFERRED with other blockers (MR:257). The status line could stand for a long, unknown time. A also departs from the spec default, which posts OB-08 without BC-18 (MR:535), so it is not the lowest-change option either.
3. **A's timing argument is weaker than it looks.** The gate already allows "post-link choice or explicit deferral" (RG:22), so a record written now can state "post-link choice deferred to release 3". Release 3's later choices therefore do not force the whole record to wait. The gate's "Stale" rule (RG:25) also provides for re-confirmation when a later gate changes things.
4. **B cites evidence that fails the gate's authorship rule.** The proposed amendment's evidence is "the owner decision records of 2026-11-08 and 2026-11-11" (variant-2). OD-1108 is worker-recorded (OD-1108:3) and leaves gate satisfaction "for the owner to say" (OD-1108:9). OD-1111 does not address direction (OD-1111:8-9). OD-1108 is also not on master (MR:235; Q7). B would make the criterion rest on records that RG:22 would not accept as the selection record.
5. **B changes two documents, not one, or leaves them inconsistent.** Amending #409 does not change RG:10, RG:11, RG:22 or RG:34. B admits this: the gate "is either satisfied by the cited records or amended in the same change" (variant-2). Editing the gate means changing the bar in two places. Not editing it leaves the gate blocked while the issue says the criterion is met.
6. **B still does not supply the production-integration reading or the gate's other fields** (variant-2, "What stays unresolved"). Its amendment fixes the wording of #409 without fixing the gate the wording points to.
7. **B rewrites the target after the work has shipped**, and an outside reader will see that (variant-2, "Changes the bar after the fact").

### 5. Concessions

1. **My original three-field paragraph does not meet RG:22 as written.** The gate lists: date, option, decider, where the statement lives, default while no question rows exist, default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date, stack confirmation, command name and the confirmed production-integration reading. Variant-3 names three of these. To be sufficient, the paragraph must cover the rest, even briefly (for example "post-link choice: deferred to release 3"), or the owner must say the gate is met without them. That second path is a quieter form of B's goalpost move.
2. **It is retroactive.** Releases 1 and 2 shipped before any record existed (ADJ:527, BC-10: "Releases 1 and 2 were built on the owner's staged direction of 2026-11-08, before a dated selection record existed"). The paragraph documents the selection; it cannot make the selection precede the work. RG:24 ("Missing: no production integration") was not respected in order, and C does not undo that. The record should say so honestly rather than imply compliance in sequence.
3. **"Met by the owner's record" can read as more than it is.** Criterion 1 says "before production integration". A record dated 2026-11-14 or later does not show selection *before* the command was registered (release 1 merged 2026-11-11, MR:232). The honest status line is closer to "direction selected 2026-11-08 (staged); confirmed in the owner's record of <date>, path; recorded after releases 1 and 2 shipped". My variant's wording "met by the owner's record of <date>" overstates this.
4. **It costs owner attention, and the location is undecided** (MR:250: "UNVERIFIED where").
5. **It depends on Q7** if it cites OD-1108, because that file must first be saved on master (MR:235).

### 6. Shared assumptions

- **A-001 (the recorded staged direction is still current): QUALIFY.** The only direction evidence is OD-1108:5-8 and its restatement as "binding" on master (RG:3). OD-1111 is about question scope, not direction (OD-1111:8-9). Nothing I read says the direction changed, but nothing re-confirms it after 2026-11-08 either. The owner's own paragraph is the natural place to re-confirm it. A defers that confirmation, and B assumes it.
- **A-002 (shipping the CLI command is "production integration"): REJECT as an assumption C must share.** The gate says the two readings are "both UNVERIFIED" (RG:29) and that the owner confirms one "in the selection record" (RG:34). C asks the owner for exactly that reading, so C does not depend on A-002. Only C's proposed status-line wording leans on it. If the owner picks Reading 2 and nothing is "enabled" yet, criterion 1 may not have been crossed, and BC-18's "not met" line would be wrong. A depends on A-002 most, because its whole output is that line.

### 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | Tie (C named for form) | 50% | Identical structure; no merit difference. |
| C-001 (instrument used now) | C | 75% | RG:22 and RG:34 name the owner's selection record as the instrument; B's amendment needs a gate edit too, and A uses none. |
| C-002 (what #409 says about criterion 1) | C, with A's honesty | 65% | Citing a record beats "not met", but the line must say the record was written after releases 1 and 2 (Concession 3); A's line is the correct text if no record exists. |
| C-003 (release 3 unblocked on this point) | C | 60% | B and C both unblock it, and C does so without a gate conflict; low stakes because OB-09 has other blockers (MR:257). |
| C-004 (gate field list, RG:22) | C, if extended | 60% | RG:22 allows "explicit deferral", so a record written now can cover every field; my original three-field version is insufficient and A's point stands against it. |
| C-005 (owner effort now) | A | 75% | A costs nothing today; B and C both need owner text. |
| X-001 (does 2026-11-08 count as the selection?) | C | 70% | OD-1108:3 is worker-recorded and OD-1108:9 leaves it to the owner; RG:22 requires owner authorship, so a separate owner record is needed. |
| X-002 (is changing the criterion legitimate?) | C (A equal on this point) | 75% | Keeping the criterion avoids a post-hoc bar change and a second edit to RG; A also keeps it. |
| A-001 (direction still current) | C | 60% | Only C has the owner re-state the direction now, in their own words. |
| A-002 (registration = production integration) | C | 80% | Only C obtains the reading that RG:34 says must be confirmed in the selection record; A publishes a conclusion that depends on it. |

### 8. Overall verdict

**Pick C, extended: an owner-written dated paragraph that covers every RG:22 field (deferring post-link choice and fallback date explicitly) and states that it was written after releases 1 and 2 shipped. Until it exists, use A's BC-18 "not met as recorded" line instead of omitting the status.** Confidence: 70 percent. Reason: the gate on master names the owner's selection record as the only place to confirm the production-integration reading and requires owner, not agent, authorship (RG:22, RG:34). A leaves that open, and B rests on a worker-recorded file that defers the question back to the owner (OD-1108:3, :9).

## Scoring Matrix

| Diff Point | Level | Advocate A | Advocate B | Advocate C | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (no winner) | 50% | Same five sections. |
| C-001 | L2 | C 65 | C 70 | C 75 | C | 95% | Unanimous; B's own advocate conceded: the gate defines an owner-written record as the instrument (`release-gates.md:22`; `acceptance-tests.md:14, 70`). |
| C-002 | L2 | A 60 | C 65 | C (with A's honesty) 65 | C, worded honestly | 65% | A cited record beats "not met", but the line must say the record was written after releases 1 and 2 shipped; A's line is right while no record exists. |
| C-003 | L3 | A 55 | C 60 | C 60 | C | 60% | Low stakes: release 3 (OB-09) has other blockers (merged-requirements.md:257). |
| C-004 | L3 | A 65 | C 65 | C (if extended) 60 | C, extended | 60% | The gate allows "explicit deferral", so a record written now can cover every field; the original three-field version is insufficient (C's advocate concession 1). |
| C-005 | L2 | A 70 | A 80 | A 75 | A | 95% | Unanimous: A asks almost nothing of the owner now. |
| X-001 | L3 | C 70 | C 75 | C 70 | C | 95% | Unanimous: the 2026-11-08 record was recorded by an Orca worker (`owner-decisions-20261108.md:3`), so it cannot be the owner-written record; the decision counts in substance, the record must be owner-written. |
| X-002 | L2 | A = C 70 | C 70 | C (A equal) 75 | C (A equal) | 90% | Keep criterion 1 unchanged; B's own advocate agreed amending it is unnecessary and reads as moving the bar. |
| A-001 | L2 | C 60 | C 55 | C 60 | C | 85% | All QUALIFY; only an owner paragraph re-confirms the direction now. |
| A-002 | L3 | C 70 | C 75 | C 80 | C | 95% | `release-gates.md:34` names the selection record as where the reading is confirmed; A's "not met" line depends on the reading. A and B QUALIFY; C REJECTs it as an assumption C must share. |

Shared-assumption responses: A-001 QUALIFY x3; A-002 QUALIFY (A), QUALIFY (B), REJECT (C). No omissions.

## Overall verdicts (section 8 of each statement)

| Advocate | Picks | Confidence |
|---|---|---|
| A (for defer) | C combined with two parts of A: cover every gate field (defer release-3 fields explicitly); if not written in W1, post A's BC-18 line instead of omitting it | 65% |
| B (for amend criterion) | C carrying B's citations: state the 2026-11-08 selection, the owner's reading, the command name, and cover, waive or defer the remaining fields | 70% |
| C (for write record) | C extended: cover every gate field, state it was written after releases 1 and 2 shipped; until it exists use A's BC-18 line | 70% |

All three chose C, extended: 3 of 3. Mean confidence 68%.

## Convergence Assessment
- Points resolved: 10 of 10 (majority rule; S-001 tie unanimous); unanimous winners: C-001, C-005, X-001
- Alignment: 100% by majority
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-001, C-002, C-005, X-002, A-001), L3 (C-003, C-004, X-001, A-002): all covered
- Invariant probe gate: not applied (Round 2.5 skipped at quick depth)
- Status: CONVERGED
- Unresolved points: none. Dissent recorded: A's advocate on C-002, C-003, C-004 (favouring A's timing); C-005 won by A.

# Round 1 statement: advocate for Proposal B (variant-2-original.md)

Debate: Q10, may the sweep read Orca's pending questions. Mode A, depth quick, Round 1.

Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. All line numbers below were read on 2026-11-14 in this session.

## 1. Position summary

Proposal B says the sweep never reads Orca messages, as a standing rule, and that its two report sentences change once, after the seeded consumption test (OB-03) gives a result. The "never" half is defensible on the evidence; the "wait for OB-03 before rewording" half is weak, and on that half I think C is better.

## 2. Steelman of each opposing variant

**Proposal A (yes, later, behind the tests).** The strongest form: the sweep runs inside the coordinator's own session, and gate test Q-1 failed, so only the terminal holding a Run can read its questions (ADJ INV-024, line 465; MR:239). The sweep is therefore the one program already sitting in the right terminal, which the observer, run by a person in another terminal, is not. If OB-03, OB-04 and OB-05 all pass, one owner-signed template (`check --all --types question --run <run> --json`) would close the report's own "Messages coverage: partial" gap (`report.py:199`) using evidence the program produces anyway. A also fixes the overstated text now, in SW-07, as the spec asks (MR:196), and turns into "never" by itself if OB-03 shows consumption.

**Proposal C (observer's alone for now; correct the sentences now).** The strongest form: it is the spec's recommended answer and its default (MR:537; ADJ:780), so it costs nothing to record and lets SW-07 run in W3 with a fixed text. It removes a claim ADJ judged stronger than the evidence (X-016, "unproven both ways", 61 percent, ADJ:333 and :813) without asserting the opposite claim, which V5 O-05 tried and had withdrawn (ADJ:166). It keeps the allow-list unchanged (NFR-014; `probes.py:49-60` has no `check` verb) and keeps the door open, so nothing is decided that later evidence could make wrong.

## 3. Strengths claimed

1. **The sweep stays a program that sends Orca nothing that could change a mailbox.** A plain `check` consumes (ADJ glossary line 97), and whether `check --all --types question` consumes on a live coordinator Run is unproven both ways (ADJ:333). ADJ's own read-only principle lists "A status read must not consume Orca messages (D-4)" (ADJ:670). "Never" makes that property permanent rather than provisional.
2. **The case that cannot be proven safe is exactly the case the sweep would face.** The sweep runs in the coordinator's session on the coordinator's own live Run. MR's sufficiency table says OB-03 passing does not prove safety, because "a live coordinator Run has `--wait` listeners and an acknowledge cycle that a throwaway Run lacks" (MR sufficiency table near line 1156, row "OB-03 passing alone"). OB-04 is deliberately run on a Run "that is never the alignment coordinator's own and carries no work whose questions matter" (MR:252). So no planned test ever certifies a sweep read on a working coordinator's own Run. A rule that the sweep never reads there matches what can be proven.
3. **The coordinator does not need the sweep to see its questions.** WC-16 says the coordinator "keeps watching its Run", re-arms its Orca wait when it expires, and runs `/sc:sweep` as "an added read" (`WORKER-CONTRACT.md:288`), and the sweep "recommends nothing" (ADJ glossary line 81). PLAN INFERENCE (UNVERIFIED whether that wait delivers `question` messages specifically): the coordinator's own wait is the channel through which it receives worker messages, so a sweep read would duplicate it while adding a consumption risk.
4. **One clear division of labour.** The sweep reports workers and worktrees; the observer is the program built to show questions (MR:233, `check --all --types question --run <id> --json` behind its guard). ADJ keeps the two programs separate and forbids cross-reading (ADJ:195: adding "an observer reader of the sweep's JSON" is a Do-not). "Never" ends the question instead of leaving it to come back, which C admits it may (variant-3: "'For now' leaves the long-term answer open").
5. **"Never" costs little to reverse.** Any change to `ALLOWED_ORCA` already needs an owner-signed allow-list edit (NFR-014, ADJ glossary line 84; MR:571 per question.md: Q1's risk choice does not authorize arbitrary edits). The owner can lift "never" by the same signature A would need anyway; recording "never" only removes the expectation of a reopening.

## 4. Weaknesses identified in the others

1. **A reads the one mailbox whose loss matters most, on evidence that cannot cover it.** A concedes this itself ("Reading on the coordinator's own live Run is exactly the case the seeded test cannot fully prove", variant-1). OB-04 runs on a disposable Run, not the coordinator's own (MR:252), so after OB-03, OB-04 and OB-05 pass, the sweep's actual target is still untested. A wrong pass would remove questions the coordinator must answer.
2. **A adds a reader with no consumer action.** The sweep "recommends nothing" (WC-16; ADJ:81) and the coordinator already watches its Run (`WORKER-CONTRACT.md:288`). A leaves "what the sweep does with them" unresolved (variant-1, last section). A second reader of the same mailbox doubles exposure if consumption is ever found (variant-1's own risk list).
3. **A widens an owner-signed allow-list that was built to be read-only toward Orca**, and ends the sweep's claim to read no messages (variant-1). The program's other open security item (INV-008, ADJ:31) already shows that small allow-list changes carry test and contract consequences (INV-009, ADJ:460).
4. **C's "for now" defers the real decision without a trigger.** C says "nothing is scheduled for that" (variant-3), so the question stays open indefinitely and can be reopened on any future pass.
5. **C (and A) adopt the spec's three-sentence text for both report lines, but line 199 is a header value, not a sentence slot.** `report.py:199` is `"Messages coverage: partial"`, pinned exactly by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`; `report.py:534-535` is a bullet under "What I could not determine". Three sentences in the header line would break the header's one-fact-per-line form. This is the diff analysis's A-001 and applies to all three proposals, but C commits to the exact text now.
6. **C's interim sentence goes stale.** C concedes "a second wording change may follow" once OB-03 lands (variant-3).

## 5. Concessions

1. **B leaves a sentence ADJ judged overstated in the shipped sweep for longer.** `report.py:534-535` says "pending questions cannot be read without consuming them"; ADJ rules that this is not established (X-016 decision row, ADJ:813: "the sweep's two lines are reworded to state only what is established"). Deferring the fix keeps an unsupported claim in front of coordinators. This is B's largest weakness.
2. **B ties a text fix to a live test with no date.** OB-03 needs Q24, the Orca app, a live grant and XC-10 (MR:251). If OB-03 never runs, the overstatement is never fixed. C's interim sentence is true today whatever OB-03 later shows.
3. **B's conditional text is triggered by an insufficient test.** B switches to "This command reads no messages. Questions are read by `superclaude observe`." if OB-03 shows no consumption on the seeded Run. OB-03 is "necessary, not sufficient" (ADJ:174; MR:251 item 6), so that trigger is weaker than it looks; and in the consumption branch B keeps "cannot be read without consuming them", which a seeded-Run result still does not establish for a live Run.
4. **B's final sentence depends on the observer read being switched on.** "Questions are read by `superclaude observe`" is false while `QUESTION_GATE_PASSED = False` (MR:234), and the guard stays off if Q6 is unanswered (MR:254, MR:979). See A-002 below.
5. **B departs from the spec**, which fixes the sentences in SW-07 now (MR:196; ADJ Part 2.2 action 6). That is a spec change; C costs nothing.
6. **"Never" may be wrong for a coordinator that has only the sweep open** (variant-2's own risk). Strength 3 argues the coordinator's own wait covers this, but that is PLAN INFERENCE, not verified.

## 6. Shared assumptions

- **A-001 (both report lines take the same replacement text): REJECT.** `report.py:199` is a header value `"Messages coverage: partial"` pinned exactly by `test_report.py:590` and shown at `orchestrator-mode.md:610`; `report.py:534-535` is a prose bullet. Whichever variant wins, SW-07 acceptance criterion (3) (MR:196) should give the header its own short value (owner's wording; for example keep "Messages coverage: partial" or say "Messages coverage: none (no message reads)") and put the three established sentences only in the bullet, with design line 610 and the pinned test updated in the same PR.
- **A-002 (the observer will eventually read questions): QUALIFY.** It holds only if Q6 is answered, OB-03 to OB-05 pass and OB-06 merges; the default is that the guard stays off (MR:254, MR:979), and MR:261 says Q10 may become "neither". So "observer's alone" can mean "nobody" for a long time. That does not change the sweep's own rule (B and C both keep the sweep out), but any report text that points readers to the observer, including B's own proposed sentence, is conditional. Report text should not name the observer as the reader until OB-06 has merged.

## 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | C (no real difference) | 50% | All three use the same five sections. |
| C-001 (may the sweep ever read questions) | B | 55% | No planned test covers the coordinator's own live Run (MR:252; MR sufficiency table) and the sweep has no consumer action (WC-16); but "for now" and "never" differ little, because NFR-014 already needs an owner signature. |
| C-002 (when the sentences change) | C | 75% | The current bullet overstates (ADJ:813); a true interim text now beats waiting on an undated live test (MR:251). |
| C-003 (allow-list change) | B | 55% | Same as C today; permanence avoids a reopening with no identified use, and an owner signature can still reverse it. |
| C-004 (division of labour) | B | 55% | One reader of questions, programs kept separate (ADJ:195); weakened by A-002, since the observer read may never switch on. |
| C-005 (dependence on live tests) | C | 70% | A wording fix should depend on nothing live; B's dependence is its main cost. |
| X-001 (sweep reads if consumption disproven) | B | 60% | Disproven on a seeded Run is not disproven on the coordinator's own live Run (MR sufficiency table; ADJ:174), which is where the sweep would read. |
| X-002 (interim sentence vs keep current text) | C | 75% | Keeping a sentence ADJ judged unsupported is worse than one extra later edit. |
| A-001 (same text for both lines) | C, corrected | 60% | No variant handles it; C's "now" timing lets SW-07 fix it with separate header and bullet texts in one PR. |
| A-002 (observer will read questions) | C | 70% | C's text names no reader; B's final sentence names the observer and is false while the guard is off. |

## 8. Overall verdict

The owner should pick **C, recording the sweep side as "never, unless the owner signs a new allow-list" (B's division of labour), and splitting the replacement text so `report.py:199` keeps a short header value while only the bullet at `report.py:534-535` takes the three sentences**. Confidence 70 percent. Reason: C fixes an unsupported claim now with text that is true whatever OB-03 shows, and B's only clear gain, a firm no for the sweep, can be added to C at no cost.

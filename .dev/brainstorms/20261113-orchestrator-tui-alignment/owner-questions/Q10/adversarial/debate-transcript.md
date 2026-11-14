# Adversarial Debate Transcript: Q10 owner-answer proposals

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (10 of 10 points agreed by at least 2 of 3 advocates)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (spawned in parallel as separate agents; each wrote its own file)
- Variant mapping: variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C
- Orchestrator spot-check (2026-11-14): `src/superclaude/core/WORKER-CONTRACT.md:100-103` confirms the coordinator already waits with `orca orchestration check --wait --types ...,question,...` and handles every message in the returned batch before `--ack`; so pending questions already reach the coordinator through its own loop, and a sweep read would be a second view. `report.py:199` is a header value pinned by `tests/sweep/test_report.py:590`.

## Round 1: Advocate Statements

### Advocate for proposal A (source file: round1-advocate-A.md)

## Round 1 statement: advocate for variant 1 (proposal A)

- Debate: Q10, may the sweep ever read Orca's pending questions
- Mode A, depth quick, Round 1 only
- Date: 2026-11-14
- Advocate for: variant-1-original.md (proposal A, "yes, later, after the consumption tests pass")

### 1. Position summary

Proposal A agrees with C on everything that happens now (no `check` in the sweep's allow-list, the two sentences corrected in SW-07), and adds a conditional path: if the seeded test (OB-03), the live-layout attempt (OB-04) and the build pin (OB-05) all pass, the owner may sign one eleventh allow-list template so the sweep lists its own Run's pending questions. Having checked the worker contract, I now think the conditional "later" adds less than A claims, because the coordinator already receives every question through its own `check --wait`. A is defensible only as "C now, with the reopening condition written down".

### 2. Steelman of each opposing variant

**Proposal B (never for the sweep; change the sentences once, after OB-03).**
At its strongest, B is about keeping one tool for one job. Every reader of a mailbox is one more way to lose a message. The sweep's best property is that it sends Orca nothing that could change a mailbox, and B keeps that property for good (variant-2, "What it unlocks"). B also avoids touching the same text twice: C's interim sentence ("not established") goes stale once OB-03 reports, so the text gets edited a second time. B edits it once, and the new text names the program that does read questions ("Questions are read by `superclaude observe`"). B also has a point that A ignores: the coordinator does not need the sweep to see questions. The coordinator's own wait already lists `question` among its types (`WORKER-CONTRACT.md:100`: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`), so a "never" rule takes nothing from the coordinator.

**Proposal C (observer's alone for now; correct the sentences now).**
At its strongest, C is the answer the evidence supports today and costs nothing. ADJ ruled that the consumption question is "unproven both ways" (X-016, 61 percent, ADJ:333), and that "both programs keep their cautions; the sweep's two lines are reworded to state only what is established" (ADJ:813). The current bullet ("pending questions cannot be read without consuming them", `report.py:534-535`) says more than anyone has proven, and C fixes it in W3 without waiting on a live test that needs the Orca app, Q24 and Q30. C leaves the allow-list (NFR-014, `probes.py:49-60`, "10 templates, 7 verbs") alone. "For now" does not lock out a later answer, which matches the spec's own fallback: Q10 "stays 'observer's alone' or becomes 'neither'" (`merged-requirements.md:261`, `:1000`). C is also the spec's recommended answer and its default if the owner says nothing (`merged-requirements.md:537`; ADJ:780).

### 3. Strengths claimed (proposal A)

1. **A fixes the overstatement now, as C does.** A's "Now (W3, SW-07)" step adopts SW-07 item (3) word for word (`merged-requirements.md:196`). So A does not share B's main weakness, the shipped overstatement that ADJ rejected (ADJ:813).
2. **A writes down when the question reopens; C leaves that open.** C says "nothing is scheduled for that". A names the exact evidence that would reopen it (OB-03, OB-04, OB-05) and says what happens on failure: "If OB-03 shows consumption, this answer turns into 'never' automatically." This follows the spec's own risk row (`merged-requirements.md:261`). The ledger then holds a decision rule, not a "for now" that must be asked again.
3. **The sweep is the only program that could read the Run in the place it is held.** Q-1 failed: "only the terminal holding the Run can read" (ADJ INV-024, ADJ:465; `merged-requirements.md:239`). The coordinator runs `/sc:sweep` in its own session (`WORKER-CONTRACT.md:288`, WC-16), so a sweep read is not hit by the problem that 28 of 53 Runs have no `coordinator_handle`, which may make the observer's panel unusable (`merged-requirements.md:262`, `:1157`). This is the only structural advantage A has over C, and it is real.
4. **A uses the same safety evidence the observer must produce anyway.** A adds no new test of its own. It reuses OB-03, OB-04 and OB-05, which the observer's guard flip already requires (`merged-requirements.md:251-254`; ADJ:814). The OB-04 condition ("a live `--wait` listener and an ack cycle") is the condition that `merged-requirements.md:1156` says OB-03 alone does not cover.
5. **A keeps to the allow-list rules.** It adds one exact template through an owner-signed allow-list change in its own PR with tests. That is the route NFR-014 requires (glossary ADJ:84) and the route SW-10 (4) names ("no new Orca verb outside NFR-014 unless the owner signs a new allow-list", `merged-requirements.md:199`). It does not rely on Q1's risk choice (`merged-requirements.md:571`, as cited in question.md; not re-read here).

### 4. Weaknesses identified in the others

1. **B ships a sentence that ADJ rejected, possibly forever.** B leaves "pending questions cannot be read without consuming them" (`report.py:534-535`) in place until OB-03 runs. OB-03 needs a live Orca, Q24, a grant for seeded writes and other conditions (`merged-requirements.md:251`). ADJ:813 says the sweep's lines "are reworded to state only what is established". B admits this cost itself ("if OB-03 never runs, the overstatement never gets fixed").
2. **B's "never" is not tied to any evidence.** B accepts that "'Never' rules out the sweep reading questions even if consumption is disproven". The spec frames Q10's fallback as conditional on OB-03 ("stays 'observer's alone' or becomes 'neither'", `merged-requirements.md:261`). A rule that holds whatever the evidence says goes further than any source asks.
3. **B's planned sentence could be untrue.** "Questions are read by `superclaude observe`" is true only after the guard flip (OB-06). OB-06 needs Q6, Q7, OB-01, OB-04 and more, and its default is "the guard stays off" (`merged-requirements.md:254`). OB-03 passing does not by itself switch the observer's read on, so B's text could ship while `QUESTION_GATE_PASSED = False` (`merged-requirements.md:234`).
4. **C leaves the reopening condition unwritten.** "Nothing is scheduled" means the question comes back with no rule saying what evidence decides it. This is a small weakness: a one-line note fixes it.
5. **All three reuse a replacement text that may not fit line 199 (see A-001).** C is the most exposed because its value is "matches the spec default at zero cost". If the spec's text does not fit the header line, C's "zero cost" is not quite true.

### 5. Concessions (proposal A's real weaknesses)

1. **The main thing A says it unlocks is mostly already there.** A says "the coordinator sees its own workers' pending questions in the same report". But the coordinator already waits on `question` messages in every cycle (`WORKER-CONTRACT.md:100`). The wait returns "the whole FIFO batch, replayed until `--ack`", and the coordinator "handles every message in the batch" before acking (`WORKER-CONTRACT.md:102-103`). So questions already reach the coordinator through the program that is supposed to handle them. A sweep read would add at most a second view of messages that are not yet acked. Proposal A did not cite this and overstates its benefit.
2. **The sweep is barred from acting on what it reads.** WC-16: "`/sc:sweep` recommends nothing: no stop, retry, release, merge or removal" (`WORKER-CONTRACT.md:288`). A question listed in the sweep report gives no new path to an answer. A itself lists this as unresolved.
3. **A adds risk on the one mailbox that matters most.** The sweep would read the coordinator's own live Run, which is the inbox with live work. OB-04 deliberately runs on a disposable Run that is "never the alignment coordinator's own" (`merged-requirements.md:252`). So a passing OB-04 does not test the exact case A would switch on. A's own text admits this ("a wrong pass could make the sweep remove the questions the coordinator must answer").
4. **A gives up the sweep's clean read-only claim and widens a signed list for a small gain.** NFR-014 currently has no message-reading verb (`probes.py:49-60`). A ends "this command reads no messages" for a duplicate view.
5. **A still has the second-edit cost.** A uses the interim "not established" sentence as C does, so the sweep's text may change twice (now, then when the template lands). A's step "changes from 'partial' to the measured state" also changes a header pinned by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`.

### 6. Shared assumptions

- **A-001 (both report lines take the same replacement text): QUALIFY.** The assumption is false as written. Line 199 is the header value `"Messages coverage: partial"`, which `tests/sweep/test_report.py:590` pins inside an exact header list and `docs/designs/orchestrator-mode.md:610` shows. Lines 534-535 are a bullet under "What I could not determine". Putting a three-sentence paragraph in a one-line header field would break the header's shape. The fix: the bullet takes the R2-V5 5.8 text; the header keeps a short value (for example "Messages coverage: partial (questions not read)"). SW-07 then names the test at `:590` and the design line `:610` as changes. That wording is my suggestion (PLAN INFERENCE). It affects A and C equally, and B only when its single edit happens.
- **A-002 (the observer will eventually read questions): QUALIFY.** No variant can assume this. OB-06 does not open if Q6 is unanswered (`merged-requirements.md:254`; rule 6 at `:979`). However, the coordinator does not depend on the observer for questions: its own wait already wakes on `question` (`WORKER-CONTRACT.md:100`). So if the observer never switches on, "observer's alone" means no secondary view, not that nobody sees questions. That weakens A-002's stated impact, and it also weakens A's case for adding the sweep as a second reader.

### 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all the same) | 95% | The variants have the same section set. |
| C-001 (may the sweep ever read questions) | C | 70% | "For now" fits the unproven-both-ways evidence (ADJ:333). A's "yes, later" mostly duplicates the coordinator's own wait (`WORKER-CONTRACT.md:100`). B's "never" is not tied to evidence. |
| C-002 (when the sentences change) | A = C (now) | 85% | ADJ:813 says to reword now, and B's delay keeps an overstatement in place with no deadline. |
| C-003 (allow-list change) | C | 75% | Leaving NFR-014 unchanged is enough. A's eleventh template buys a duplicate view at risk to the live inbox. |
| C-004 (division of labour) | C | 65% | One question reader for now. B's "permanently" goes beyond the evidence, and A's "both" adds a second reader with little gain. |
| C-005 (dependence on live tests) | C | 70% | No current work should wait on OB-03 or OB-04. A's later step depending on them is acceptable; B tying a wording fix to them is the worst of the three. |
| X-001 (if consumption is disproven, should the sweep read) | C (leave open) | 60% | A's argument (the sweep runs in the holding session) is real but small, because the coordinator already wakes on questions. B's flat no is premature. |
| X-002 (interim sentence or wait) | A = C (interim now) | 80% | One extra edit is cheaper than shipping a statement ADJ rejected. |
| A-001 | None as written; A and C fixed as in section 6 | 80% | The header at `report.py:199` needs a short value, not the three-sentence text. |
| A-002 | C | 65% | C does not stake anything on the observer flipping. The coordinator's own wait covers questions either way. |

### 8. Overall verdict

**Pick C with two additions taken from A: (1) a one-line ledger note that Q10 reopens only after OB-03, OB-04 and OB-05 pass, and becomes "neither" if OB-03 shows consumption; (2) SW-07 uses a short header value at `report.py:199` (test `:590`, design `:610`) and the full R2-V5 5.8 text only for the bullet at `:534-535`. Confidence: 75 percent.**

Reason: C fixes the overstated text now at no cost to the allow-list. A's extra benefit is mostly already covered by the coordinator's own `check --wait` on `question`, which does not justify widening NFR-014 for a read that WC-16 forbids the sweep to act on.

### Advocate for proposal B (source file: round1-advocate-B.md)

## Round 1 statement: advocate for Proposal B (variant-2-original.md)

Debate: Q10, may the sweep read Orca's pending questions. Mode A, depth quick, Round 1.

Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. All line numbers below were read on 2026-11-14 in this session.

### 1. Position summary

Proposal B says the sweep never reads Orca messages, as a standing rule, and that its two report sentences change once, after the seeded consumption test (OB-03) gives a result. The "never" half is defensible on the evidence; the "wait for OB-03 before rewording" half is weak, and on that half I think C is better.

### 2. Steelman of each opposing variant

**Proposal A (yes, later, behind the tests).** The strongest form: the sweep runs inside the coordinator's own session, and gate test Q-1 failed, so only the terminal holding a Run can read its questions (ADJ INV-024, line 465; MR:239). The sweep is therefore the one program already sitting in the right terminal, which the observer, run by a person in another terminal, is not. If OB-03, OB-04 and OB-05 all pass, one owner-signed template (`check --all --types question --run <run> --json`) would close the report's own "Messages coverage: partial" gap (`report.py:199`) using evidence the program produces anyway. A also fixes the overstated text now, in SW-07, as the spec asks (MR:196), and turns into "never" by itself if OB-03 shows consumption.

**Proposal C (observer's alone for now; correct the sentences now).** The strongest form: it is the spec's recommended answer and its default (MR:537; ADJ:780), so it costs nothing to record and lets SW-07 run in W3 with a fixed text. It removes a claim ADJ judged stronger than the evidence (X-016, "unproven both ways", 61 percent, ADJ:333 and :813) without asserting the opposite claim, which V5 O-05 tried and had withdrawn (ADJ:166). It keeps the allow-list unchanged (NFR-014; `probes.py:49-60` has no `check` verb) and keeps the door open, so nothing is decided that later evidence could make wrong.

### 3. Strengths claimed

1. **The sweep stays a program that sends Orca nothing that could change a mailbox.** A plain `check` consumes (ADJ glossary line 97), and whether `check --all --types question` consumes on a live coordinator Run is unproven both ways (ADJ:333). ADJ's own read-only principle lists "A status read must not consume Orca messages (D-4)" (ADJ:670). "Never" makes that property permanent rather than provisional.
2. **The case that cannot be proven safe is exactly the case the sweep would face.** The sweep runs in the coordinator's session on the coordinator's own live Run. MR's sufficiency table says OB-03 passing does not prove safety, because "a live coordinator Run has `--wait` listeners and an acknowledge cycle that a throwaway Run lacks" (MR sufficiency table near line 1156, row "OB-03 passing alone"). OB-04 is deliberately run on a Run "that is never the alignment coordinator's own and carries no work whose questions matter" (MR:252). So no planned test ever certifies a sweep read on a working coordinator's own Run. A rule that the sweep never reads there matches what can be proven.
3. **The coordinator does not need the sweep to see its questions.** WC-16 says the coordinator "keeps watching its Run", re-arms its Orca wait when it expires, and runs `/sc:sweep` as "an added read" (`WORKER-CONTRACT.md:288`), and the sweep "recommends nothing" (ADJ glossary line 81). PLAN INFERENCE (UNVERIFIED whether that wait delivers `question` messages specifically): the coordinator's own wait is the channel through which it receives worker messages, so a sweep read would duplicate it while adding a consumption risk.
4. **One clear division of labour.** The sweep reports workers and worktrees; the observer is the program built to show questions (MR:233, `check --all --types question --run <id> --json` behind its guard). ADJ keeps the two programs separate and forbids cross-reading (ADJ:195: adding "an observer reader of the sweep's JSON" is a Do-not). "Never" ends the question instead of leaving it to come back, which C admits it may (variant-3: "'For now' leaves the long-term answer open").
5. **"Never" costs little to reverse.** Any change to `ALLOWED_ORCA` already needs an owner-signed allow-list edit (NFR-014, ADJ glossary line 84; MR:571 per question.md: Q1's risk choice does not authorize arbitrary edits). The owner can lift "never" by the same signature A would need anyway; recording "never" only removes the expectation of a reopening.

### 4. Weaknesses identified in the others

1. **A reads the one mailbox whose loss matters most, on evidence that cannot cover it.** A concedes this itself ("Reading on the coordinator's own live Run is exactly the case the seeded test cannot fully prove", variant-1). OB-04 runs on a disposable Run, not the coordinator's own (MR:252), so after OB-03, OB-04 and OB-05 pass, the sweep's actual target is still untested. A wrong pass would remove questions the coordinator must answer.
2. **A adds a reader with no consumer action.** The sweep "recommends nothing" (WC-16; ADJ:81) and the coordinator already watches its Run (`WORKER-CONTRACT.md:288`). A leaves "what the sweep does with them" unresolved (variant-1, last section). A second reader of the same mailbox doubles exposure if consumption is ever found (variant-1's own risk list).
3. **A widens an owner-signed allow-list that was built to be read-only toward Orca**, and ends the sweep's claim to read no messages (variant-1). The program's other open security item (INV-008, ADJ:31) already shows that small allow-list changes carry test and contract consequences (INV-009, ADJ:460).
4. **C's "for now" defers the real decision without a trigger.** C says "nothing is scheduled for that" (variant-3), so the question stays open indefinitely and can be reopened on any future pass.
5. **C (and A) adopt the spec's three-sentence text for both report lines, but line 199 is a header value, not a sentence slot.** `report.py:199` is `"Messages coverage: partial"`, pinned exactly by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`; `report.py:534-535` is a bullet under "What I could not determine". Three sentences in the header line would break the header's one-fact-per-line form. This is the diff analysis's A-001 and applies to all three proposals, but C commits to the exact text now.
6. **C's interim sentence goes stale.** C concedes "a second wording change may follow" once OB-03 lands (variant-3).

### 5. Concessions

1. **B leaves a sentence ADJ judged overstated in the shipped sweep for longer.** `report.py:534-535` says "pending questions cannot be read without consuming them"; ADJ rules that this is not established (X-016 decision row, ADJ:813: "the sweep's two lines are reworded to state only what is established"). Deferring the fix keeps an unsupported claim in front of coordinators. This is B's largest weakness.
2. **B ties a text fix to a live test with no date.** OB-03 needs Q24, the Orca app, a live grant and XC-10 (MR:251). If OB-03 never runs, the overstatement is never fixed. C's interim sentence is true today whatever OB-03 later shows.
3. **B's conditional text is triggered by an insufficient test.** B switches to "This command reads no messages. Questions are read by `superclaude observe`." if OB-03 shows no consumption on the seeded Run. OB-03 is "necessary, not sufficient" (ADJ:174; MR:251 item 6), so that trigger is weaker than it looks; and in the consumption branch B keeps "cannot be read without consuming them", which a seeded-Run result still does not establish for a live Run.
4. **B's final sentence depends on the observer read being switched on.** "Questions are read by `superclaude observe`" is false while `QUESTION_GATE_PASSED = False` (MR:234), and the guard stays off if Q6 is unanswered (MR:254, MR:979). See A-002 below.
5. **B departs from the spec**, which fixes the sentences in SW-07 now (MR:196; ADJ Part 2.2 action 6). That is a spec change; C costs nothing.
6. **"Never" may be wrong for a coordinator that has only the sweep open** (variant-2's own risk). Strength 3 argues the coordinator's own wait covers this, but that is PLAN INFERENCE, not verified.

### 6. Shared assumptions

- **A-001 (both report lines take the same replacement text): REJECT.** `report.py:199` is a header value `"Messages coverage: partial"` pinned exactly by `test_report.py:590` and shown at `orchestrator-mode.md:610`; `report.py:534-535` is a prose bullet. Whichever variant wins, SW-07 acceptance criterion (3) (MR:196) should give the header its own short value (owner's wording; for example keep "Messages coverage: partial" or say "Messages coverage: none (no message reads)") and put the three established sentences only in the bullet, with design line 610 and the pinned test updated in the same PR.
- **A-002 (the observer will eventually read questions): QUALIFY.** It holds only if Q6 is answered, OB-03 to OB-05 pass and OB-06 merges; the default is that the guard stays off (MR:254, MR:979), and MR:261 says Q10 may become "neither". So "observer's alone" can mean "nobody" for a long time. That does not change the sweep's own rule (B and C both keep the sweep out), but any report text that points readers to the observer, including B's own proposed sentence, is conditional. Report text should not name the observer as the reader until OB-06 has merged.

### 7. Per-point positions

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

### 8. Overall verdict

The owner should pick **C, recording the sweep side as "never, unless the owner signs a new allow-list" (B's division of labour), and splitting the replacement text so `report.py:199` keeps a short header value while only the bullet at `report.py:534-535` takes the three sentences**. Confidence 70 percent. Reason: C fixes an unsupported claim now with text that is true whatever OB-03 shows, and B's only clear gain, a firm no for the sweep, can be added to C at no cost.

### Advocate for proposal C (source file: round1-advocate-C.md)

## Round 1 advocate statement: proposal C (variant-3), Q10

Debate: sc:adversarial Mode A, depth quick, Round 1. Advocate for variant-3-original.md (proposal C). Date 2026-11-14.

Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. All line numbers below were re-read on 2026-11-14.

### 1. Position summary

For now only the observer may read pending questions. The sweep keeps `check` outside its owner-signed allow-list, and its overstated "cannot be read without consuming them" text is corrected in SW-07 (W3) to state only what is established. This is the spec's recommendation and its default (MR:537, ADJ:780). It costs nothing to answer, and it leaves the long-term question open until real consumption evidence exists, which is where that question belongs.

### 2. Steelman of each opposing variant

**Proposal A (yes, later, after OB-03, OB-04 and a build pin).** At its strongest, A says this: the coordinator is the one consumer that actually needs its own workers' questions, and the sweep already runs inside the coordinator's pass every wake (WC-16, `WORKER-CONTRACT.md:288`). Gate test Q-1 failed, so only the terminal holding a Run can read its questions (ADJ:465, glossary "Q-1"). A separate observer process may not be that terminal; the coordinator's own session is. A therefore puts the read where it can work. It closes the sweep's self-declared "Messages coverage: partial" gap (`report.py:199`), reuses evidence the program produces anyway (OB-03 to OB-05, MR:251-253), and turns into "never" automatically if OB-03 shows consumption. It also corrects the sentences now, as C does, so in the near term A does everything C does and more.

**Proposal B (never for the sweep; edit the sentences once, after OB-03).** At its strongest, B says this: one program, one job. The sweep's most valuable property is that it sends Orca nothing that could change a mailbox. A permanent rule protects that property from future pressure to widen NFR-014 (`probes.py:49-60`, "10 templates, 7 verbs"). B also avoids writing an interim sentence ("not established") that is designed to go stale, and it settles the question so it does not come back to the owner a second time.

### 3. Strengths claimed

1. **It is the spec's recommended answer and its default, so it cannot block anything.** MR:537 gives "Observer's alone for now; correct the sweep's two sentences" as both the recommendation and (PLAN INFERENCE) the default; ADJ:780 gives the same. SW-07 lists Q10 as a dependency (MR:196). C is the only proposal that lets SW-07 run in W3 exactly as written.
2. **It removes a claim the adjudication says is unproven, without inventing the opposite claim.** ADJ X-016 (line 333): "UNPROVEN BOTH WAYS whether `check --all --types question` consumes on a live coordinator Run" (61 percent). The decision row (ADJ:813): "Both programs keep their cautions; the sweep's two lines are reworded to state only what is established." The current bullet at `report.py:534-535` ("pending questions cannot be read without consuming them") asserts one side. C's replacement text (MR:196, ADJ:211) states only three things:
   - the sweep reads no messages (true: there is no `check` verb in `probes.py:49-60`);
   - a plain `check` consumes (ADJ glossary, "consume");
   - the `--all` case is not established (X-016).

   It also replaces V5's withdrawn O-05 rewording, which had claimed non-consumption (ADJ:211).
3. **It keeps the sweep's owner-signed allow-list unchanged.** NFR-014 is "the owner-signed allow-list of exact Orca commands (10 templates over 7 verbs)" (ADJ glossary; `probes.py:49-60`). MR:571 says even Q1's risk choice does not authorize arbitrary allow-list edits. C needs no new signature.
4. **It does not depend on any live test.** OB-03 is blocked by Q24, TB-CONSUME, LIVE, ORCA-AVAILABLE, XC-10 and a grant (MR:251); OB-04 is also blocked by Q30 (MR:252). C's text fix waits only for the #539 merge (ADJ:211, "Waits for: #539 merged"). If the live tests never run, C has still fixed the overstatement.
5. **It respects the program's stated failure path.** MR:261 and MR:1000 say that if OB-03 shows consumption, "Q10 stays 'observer's alone' or becomes 'neither'". That wording assumes C is already in force. C is the only answer that fits both outcomes without the owner deciding again.
6. **It keeps the sweep's role intact.** WC-16 (`WORKER-CONTRACT.md:288`) says "`/sc:sweep` recommends nothing"; the sweep is an added read the coordinator consults before it acts. Pending questions are things the coordinator must answer, and nothing in WC-16 gives the sweep a role there.
7. **"For now" is honest about the evidence.** The evidence that would justify widening the allow-list (OB-03 plus OB-04 plus a build pin) does not exist yet, and MR:1156 says OB-03 alone is not enough. Deciding "yes later" (A) or "never" (B) today commits the owner on a fact nobody has.

### 4. Weaknesses identified in the others

**Against A:**

1. **A's gate does not test A's target.** A lets the sweep read the coordinator's own live Run. But OB-04 explicitly runs on a disposable Run "that is never the alignment coordinator's own and carries no work whose questions matter" (MR:252). MR:1156 says a passing OB-03 does not prove safety because "a live coordinator Run has `--wait` listeners and an acknowledge cycle that a throwaway Run lacks". So "OB-03 and OB-04 pass" never measures a read on the program's own coordinator Run. A then turns that unmeasured case into a standing read on every wake (up to once per 5 minutes, WC-16). A names this as its own first risk.
2. **A's key argument (U-001) is not established.** A says the sweep "runs in the coordinator's own session, which is the terminal that holds its Run". Q-1 says an unbound terminal cannot read another terminal's Run (ADJ glossary). Nothing I read tests whether a `superclaude sweep` subprocess launched from the coordinator's Claude session counts as the holder terminal for Orca. This is UNVERIFIED. If it does not count, A's added template reads nothing.
3. **A doubles the exposure.** With the observer and the sweep both reading one mailbox, a later finding of consumption hits two programs. A states this itself.
4. **A pre-commits an allow-list change.** The owner signs each NFR-014 change separately (MR:571; MR:199, SW-10 (4): "no new Orca verb outside NFR-014 unless the owner signs a new allow-list"). Recording "yes, conditionally" now promises a signature against evidence that does not exist. C keeps the owner free to decide when the evidence lands, and C can still become A at that point.
5. **A gives the sweep nothing to do with the questions.** The sweep "recommends nothing" (WC-16), and A leaves "what the sweep does with them" unresolved.

**Against B:**

1. **B keeps a statement the adjudication says overstates the facts.** `report.py:534-535` stays in the shipped sweep until OB-03 runs. ADJ:813 rules that both claims are unproven and that the sweep's lines must be reworded "to state only what is established". B accepts this as a cost.
2. **B ties a text fix to a live test that may never run.** OB-03 needs Q24, live Orca, ORCA-AVAILABLE and a seeded-write grant (MR:251). B's own text names Q30, which actually gates OB-04, not OB-03 (MR:251-252); this is a minor error. If OB-03 never runs, the overstatement stays for good.
3. **B's planned post-OB-03 text can itself be false.** "Questions are read by `superclaude observe`" is true only if the observer's guard is switched on. That needs Q6, OB-04, OB-05 and OB-06 (MR:254: "Default if Q6 is unanswered: the guard stays off"), and OB-03 alone does not get there (MR:1156). OB-03 also runs on a throwaway Run, so even a pass does not establish non-consumption on a live Run; B's text would still need the "not established" clause.
4. **"Never" is decided on missing evidence.** B rules out the sweep even if consumption is disproven and the observer's read is parked (A-002). That could leave the coordinator with no way to see its questions except Orca itself. B lists this as a cost.
5. **B departs from the spec.** SW-07 (3) fixes the sentences now (MR:196), so B needs a spec change of its own.

### 5. Concessions

1. **"For now" leaves the question open.** The owner may be asked again, and C schedules no trigger for reopening (variant-3: "nothing is scheduled for that"). B's finality and A's explicit trigger are real advantages here.
2. **The "not established" sentence is designed to go stale.** Once OB-03 and OB-04 report, a second wording change follows. B is right about this.
3. **C applies one three-sentence text to two different lines, and that is wrong for one of them** (see A-001 below). `report.py:199` is the header value "Messages coverage: partial". That value is true, pinned by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`. Only `report.py:534-535` makes the unproven claim. C copies MR:196's wording ("`report.py:199,534` carry exactly") literally. Read literally, it would put three sentences into a one-line header field and change a design line that C never mentions.
4. **C does nothing for the coordinator's view of its questions.** The coordinator still needs the observer, whose read is itself switched off (`QUESTION_GATE_PASSED = False`, MR:234) until Q6 and OB-06. If Q6 parks the read, "observer's alone" means nobody (A-002), and C does not address that.
5. **A's U-001 is a real consideration that C ignores.** If the holder-terminal rule (Q-1) means only the coordinator's own session can read, then the observer may be the wrong reader. C's "observer's alone" would then rest on a reader that may not work in the real layout (INV-024; OB-04 exists to find this out).

### 6. Shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 (both report lines take the same replacement text) | REJECT | `report.py:199` is a header field, "Messages coverage: partial". It is accurate, pinned by `tests/sweep/test_report.py:590`, and mirrored in the design at `docs/designs/orchestrator-mode.md:610`. Only the bullet at `report.py:534-535` asserts the unproven consumption claim (ADJ:813 targets "the sweep's `report.py:534`"). SW-07 (3) should be amended: keep line 199 as it is, and put the three-sentence text in the bullet at 534-535 only. If line 199 does change, design line 610 and test line 590 must change in the same PR. This applies to all three proposals, mine included. |
| A-002 (the observer will eventually read questions) | QUALIFY | This is a dependency, not a given. The guard is off on master (MR:234) and stays off if Q6 is unanswered (MR:254). C's "for now" holds up better than B's "never" here, because the owner can revisit Q10 if Q6 parks the observer's read. But C should say so explicitly: "reopen Q10 if Q6 is answered 'no' or OB-03/OB-04 record a result". |

### 7. Per-point positions

| Point | Better approach | Confidence | Note |
|---|---|---|---|
| S-001 (section set) | none (tie) | 50% | All three use the same five sections. |
| C-001 (may the sweep ever read) | C | 70% | No evidence exists to decide "yes later" or "never". A has merit if U-001 is confirmed. |
| C-002 (when the sentences change) | C (tied with A) | 80% | Now, in SW-07. B leaves an overstatement in the shipped sweep while it waits on an uncertain test. |
| C-003 (allow-list change) | C | 75% | No change now; any later change still needs a fresh owner signature (MR:571). |
| C-004 (division of labour) | C | 65% | Observer only, for now. B's permanent split and A's two readers both decide on missing evidence. |
| C-005 (dependence on live tests) | C | 75% | Only C's actions need no live test. |
| X-001 (sweep reads if consumption disproven?) | C (leave open) | 60% | A's argument is plausible but rests on an unverified holder-terminal inference; B's "no" is premature. |
| X-002 (interim sentence vs wait) | C (tied with A) | 80% | ADJ:813 says reword now to what is established. |
| A-001 | C amended (bullet only; header kept) | 70% | None of the three handles it; amended C is the cheapest fix. |
| A-002 | A | 55% | A at least names a path where the sweep could become the reader if the observer cannot. C needs an explicit reopen trigger to match it. |

### 8. Overall verdict

Pick **C, amended in two ways**:

1. Apply the three-sentence replacement to the bullet at `report.py:534-535` only. Keep the accurate header "Messages coverage: partial" at line 199, with its test and design line unchanged.
2. Record a reopen trigger borrowed from A: "Q10 is reopened when OB-03 and OB-04 record a result, or if Q6 parks the observer's read".

Confidence: 75 percent. Reason: it removes the only unproven claim now, at no cost and without depending on a live test, and it leaves the "ever" decision to the evidence the program is already scheduled to produce.

## Scoring Matrix

| Diff Point | Level | Advocate A | Advocate B | Advocate C | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (no winner) | 50% | Same five sections. |
| C-001 | L3 | C 70 | B 55 | C 70 | C | 70% | "For now" fits the unproven-both-ways evidence (ADJ X-016, line 333); A's later read duplicates the coordinator's own wait (WORKER-CONTRACT.md:100-103); B's "never" is not tied to evidence. |
| C-002 | L2 | A = C 85 | C 75 | C (= A) 80 | C (with A) | 95% | Unanimous: reword now (ADJ:813); B's own advocate conceded. |
| C-003 | L3 | C 75 | B 55 | C 75 | C | 70% | No allow-list change now; any later change needs a new owner signature (merged-requirements.md:571). |
| C-004 | L2 | C 65 | B 55 | C 65 | C | 65% | One reader of questions, for now. |
| C-005 | L2 | C 70 | C 70 | C 75 | C | 95% | Unanimous: a wording fix should depend on nothing live. |
| X-001 | L3 | C 60 | B 60 | C 60 | C (leave open) | 60% | A seeded pass does not cover the coordinator's own live Run (merged-requirements.md:252, :1156); B's flat no is premature. |
| X-002 | L2 | A = C 80 | C 75 | C (= A) 80 | C (with A) | 95% | Unanimous: an interim true sentence beats keeping text ADJ rejected. |
| A-001 | L3 | A and C fixed 80 | C corrected 60 | C amended 70 | C, amended | 85% | All reject or qualify A-001: line 199 is a true, pinned header value; only the bullet at 534-535 makes the unproven claim. A QUALIFY, B REJECT, C REJECT. |
| A-002 | L2 | C 65 | C 70 | A 55 | C | 65% | The observer read may never switch on (default: guard off, merged-requirements.md:254); the coordinator still receives questions through its own wait. All QUALIFY. |

Shared-assumption responses: A-001 QUALIFY (A), REJECT (B), REJECT (C); A-002 QUALIFY x3. No omissions.

## Overall verdicts (section 8 of each statement)

| Advocate | Picks | Confidence |
|---|---|---|
| A (for "yes, later") | C, plus a reopen note (after OB-03, OB-04, OB-05; "neither" if OB-03 shows consumption) and split header and bullet wording | 75% |
| B (for "never") | C, recording the sweep side as "never unless the owner signs a new allow-list", with split header and bullet wording | 70% |
| C (for "observer's alone for now") | C amended: replacement text in the bullet only, header kept; reopen trigger if OB-03 and OB-04 record a result or Q6 parks the observer | 75% |

All three chose C, amended: 3 of 3. Mean confidence 73%.

## Convergence Assessment
- Points resolved: 10 of 10 (majority); unanimous: C-002, C-005, X-002 (S-001 tie unanimous)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-002, C-004, C-005, X-002, A-002), L3 (C-001, C-003, X-001, A-001): all covered
- Invariant probe gate: not applied (Round 2.5 skipped at quick depth)
- Status: CONVERGED
- Unresolved points: none. Dissent recorded: B's advocate on C-001, C-003, C-004, X-001 (favouring a firm "never"); C's advocate on A-002 (favouring A's path).

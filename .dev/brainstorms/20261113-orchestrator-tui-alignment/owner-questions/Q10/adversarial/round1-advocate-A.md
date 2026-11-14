# Round 1 statement: advocate for variant 1 (proposal A)

- Debate: Q10, may the sweep ever read Orca's pending questions
- Mode A, depth quick, Round 1 only
- Date: 2026-11-14
- Advocate for: variant-1-original.md (proposal A, "yes, later, after the consumption tests pass")

## 1. Position summary

Proposal A agrees with C on everything that happens now (no `check` in the sweep's allow-list, the two sentences corrected in SW-07), and adds a conditional path: if the seeded test (OB-03), the live-layout attempt (OB-04) and the build pin (OB-05) all pass, the owner may sign one eleventh allow-list template so the sweep lists its own Run's pending questions. Having checked the worker contract, I now think the conditional "later" adds less than A claims, because the coordinator already receives every question through its own `check --wait`. A is defensible only as "C now, with the reopening condition written down".

## 2. Steelman of each opposing variant

**Proposal B (never for the sweep; change the sentences once, after OB-03).**
At its strongest, B is about keeping one tool for one job. Every reader of a mailbox is one more way to lose a message. The sweep's best property is that it sends Orca nothing that could change a mailbox, and B keeps that property for good (variant-2, "What it unlocks"). B also avoids touching the same text twice: C's interim sentence ("not established") goes stale once OB-03 reports, so the text gets edited a second time. B edits it once, and the new text names the program that does read questions ("Questions are read by `superclaude observe`"). B also has a point that A ignores: the coordinator does not need the sweep to see questions. The coordinator's own wait already lists `question` among its types (`WORKER-CONTRACT.md:100`: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`), so a "never" rule takes nothing from the coordinator.

**Proposal C (observer's alone for now; correct the sentences now).**
At its strongest, C is the answer the evidence supports today and costs nothing. ADJ ruled that the consumption question is "unproven both ways" (X-016, 61 percent, ADJ:333), and that "both programs keep their cautions; the sweep's two lines are reworded to state only what is established" (ADJ:813). The current bullet ("pending questions cannot be read without consuming them", `report.py:534-535`) says more than anyone has proven, and C fixes it in W3 without waiting on a live test that needs the Orca app, Q24 and Q30. C leaves the allow-list (NFR-014, `probes.py:49-60`, "10 templates, 7 verbs") alone. "For now" does not lock out a later answer, which matches the spec's own fallback: Q10 "stays 'observer's alone' or becomes 'neither'" (`merged-requirements.md:261`, `:1000`). C is also the spec's recommended answer and its default if the owner says nothing (`merged-requirements.md:537`; ADJ:780).

## 3. Strengths claimed (proposal A)

1. **A fixes the overstatement now, as C does.** A's "Now (W3, SW-07)" step adopts SW-07 item (3) word for word (`merged-requirements.md:196`). So A does not share B's main weakness, the shipped overstatement that ADJ rejected (ADJ:813).
2. **A writes down when the question reopens; C leaves that open.** C says "nothing is scheduled for that". A names the exact evidence that would reopen it (OB-03, OB-04, OB-05) and says what happens on failure: "If OB-03 shows consumption, this answer turns into 'never' automatically." This follows the spec's own risk row (`merged-requirements.md:261`). The ledger then holds a decision rule, not a "for now" that must be asked again.
3. **The sweep is the only program that could read the Run in the place it is held.** Q-1 failed: "only the terminal holding the Run can read" (ADJ INV-024, ADJ:465; `merged-requirements.md:239`). The coordinator runs `/sc:sweep` in its own session (`WORKER-CONTRACT.md:288`, WC-16), so a sweep read is not hit by the problem that 28 of 53 Runs have no `coordinator_handle`, which may make the observer's panel unusable (`merged-requirements.md:262`, `:1157`). This is the only structural advantage A has over C, and it is real.
4. **A uses the same safety evidence the observer must produce anyway.** A adds no new test of its own. It reuses OB-03, OB-04 and OB-05, which the observer's guard flip already requires (`merged-requirements.md:251-254`; ADJ:814). The OB-04 condition ("a live `--wait` listener and an ack cycle") is the condition that `merged-requirements.md:1156` says OB-03 alone does not cover.
5. **A keeps to the allow-list rules.** It adds one exact template through an owner-signed allow-list change in its own PR with tests. That is the route NFR-014 requires (glossary ADJ:84) and the route SW-10 (4) names ("no new Orca verb outside NFR-014 unless the owner signs a new allow-list", `merged-requirements.md:199`). It does not rely on Q1's risk choice (`merged-requirements.md:571`, as cited in question.md; not re-read here).

## 4. Weaknesses identified in the others

1. **B ships a sentence that ADJ rejected, possibly forever.** B leaves "pending questions cannot be read without consuming them" (`report.py:534-535`) in place until OB-03 runs. OB-03 needs a live Orca, Q24, a grant for seeded writes and other conditions (`merged-requirements.md:251`). ADJ:813 says the sweep's lines "are reworded to state only what is established". B admits this cost itself ("if OB-03 never runs, the overstatement never gets fixed").
2. **B's "never" is not tied to any evidence.** B accepts that "'Never' rules out the sweep reading questions even if consumption is disproven". The spec frames Q10's fallback as conditional on OB-03 ("stays 'observer's alone' or becomes 'neither'", `merged-requirements.md:261`). A rule that holds whatever the evidence says goes further than any source asks.
3. **B's planned sentence could be untrue.** "Questions are read by `superclaude observe`" is true only after the guard flip (OB-06). OB-06 needs Q6, Q7, OB-01, OB-04 and more, and its default is "the guard stays off" (`merged-requirements.md:254`). OB-03 passing does not by itself switch the observer's read on, so B's text could ship while `QUESTION_GATE_PASSED = False` (`merged-requirements.md:234`).
4. **C leaves the reopening condition unwritten.** "Nothing is scheduled" means the question comes back with no rule saying what evidence decides it. This is a small weakness: a one-line note fixes it.
5. **All three reuse a replacement text that may not fit line 199 (see A-001).** C is the most exposed because its value is "matches the spec default at zero cost". If the spec's text does not fit the header line, C's "zero cost" is not quite true.

## 5. Concessions (proposal A's real weaknesses)

1. **The main thing A says it unlocks is mostly already there.** A says "the coordinator sees its own workers' pending questions in the same report". But the coordinator already waits on `question` messages in every cycle (`WORKER-CONTRACT.md:100`). The wait returns "the whole FIFO batch, replayed until `--ack`", and the coordinator "handles every message in the batch" before acking (`WORKER-CONTRACT.md:102-103`). So questions already reach the coordinator through the program that is supposed to handle them. A sweep read would add at most a second view of messages that are not yet acked. Proposal A did not cite this and overstates its benefit.
2. **The sweep is barred from acting on what it reads.** WC-16: "`/sc:sweep` recommends nothing: no stop, retry, release, merge or removal" (`WORKER-CONTRACT.md:288`). A question listed in the sweep report gives no new path to an answer. A itself lists this as unresolved.
3. **A adds risk on the one mailbox that matters most.** The sweep would read the coordinator's own live Run, which is the inbox with live work. OB-04 deliberately runs on a disposable Run that is "never the alignment coordinator's own" (`merged-requirements.md:252`). So a passing OB-04 does not test the exact case A would switch on. A's own text admits this ("a wrong pass could make the sweep remove the questions the coordinator must answer").
4. **A gives up the sweep's clean read-only claim and widens a signed list for a small gain.** NFR-014 currently has no message-reading verb (`probes.py:49-60`). A ends "this command reads no messages" for a duplicate view.
5. **A still has the second-edit cost.** A uses the interim "not established" sentence as C does, so the sweep's text may change twice (now, then when the template lands). A's step "changes from 'partial' to the measured state" also changes a header pinned by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`.

## 6. Shared assumptions

- **A-001 (both report lines take the same replacement text): QUALIFY.** The assumption is false as written. Line 199 is the header value `"Messages coverage: partial"`, which `tests/sweep/test_report.py:590` pins inside an exact header list and `docs/designs/orchestrator-mode.md:610` shows. Lines 534-535 are a bullet under "What I could not determine". Putting a three-sentence paragraph in a one-line header field would break the header's shape. The fix: the bullet takes the R2-V5 5.8 text; the header keeps a short value (for example "Messages coverage: partial (questions not read)"). SW-07 then names the test at `:590` and the design line `:610` as changes. That wording is my suggestion (PLAN INFERENCE). It affects A and C equally, and B only when its single edit happens.
- **A-002 (the observer will eventually read questions): QUALIFY.** No variant can assume this. OB-06 does not open if Q6 is unanswered (`merged-requirements.md:254`; rule 6 at `:979`). However, the coordinator does not depend on the observer for questions: its own wait already wakes on `question` (`WORKER-CONTRACT.md:100`). So if the observer never switches on, "observer's alone" means no secondary view, not that nobody sees questions. That weakens A-002's stated impact, and it also weakens A's case for adding the sweep as a second reader.

## 7. Per-point positions

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

## 8. Overall verdict

**Pick C with two additions taken from A: (1) a one-line ledger note that Q10 reopens only after OB-03, OB-04 and OB-05 pass, and becomes "neither" if OB-03 shows consumption; (2) SW-07 uses a short header value at `report.py:199` (test `:590`, design `:610`) and the full R2-V5 5.8 text only for the bullet at `:534-535`. Confidence: 75 percent.**

Reason: C fixes the overstated text now at no cost to the allow-list. A's extra benefit is mostly already covered by the coordinator's own `check --wait` on `question`, which does not justify widening NFR-014 for a read that WC-16 forbids the sweep to act on.

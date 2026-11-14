# Round 1 advocate statement: proposal C (variant-3), Q10

Debate: sc:adversarial Mode A, depth quick, Round 1. Advocate for variant-3-original.md (proposal C). Date 2026-11-14.

Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. All line numbers below were re-read on 2026-11-14.

## 1. Position summary

For now only the observer may read pending questions. The sweep keeps `check` outside its owner-signed allow-list, and its overstated "cannot be read without consuming them" text is corrected in SW-07 (W3) to state only what is established. This is the spec's recommendation and its default (MR:537, ADJ:780). It costs nothing to answer, and it leaves the long-term question open until real consumption evidence exists, which is where that question belongs.

## 2. Steelman of each opposing variant

**Proposal A (yes, later, after OB-03, OB-04 and a build pin).** At its strongest, A says this: the coordinator is the one consumer that actually needs its own workers' questions, and the sweep already runs inside the coordinator's pass every wake (WC-16, `WORKER-CONTRACT.md:288`). Gate test Q-1 failed, so only the terminal holding a Run can read its questions (ADJ:465, glossary "Q-1"). A separate observer process may not be that terminal; the coordinator's own session is. A therefore puts the read where it can work. It closes the sweep's self-declared "Messages coverage: partial" gap (`report.py:199`), reuses evidence the program produces anyway (OB-03 to OB-05, MR:251-253), and turns into "never" automatically if OB-03 shows consumption. It also corrects the sentences now, as C does, so in the near term A does everything C does and more.

**Proposal B (never for the sweep; edit the sentences once, after OB-03).** At its strongest, B says this: one program, one job. The sweep's most valuable property is that it sends Orca nothing that could change a mailbox. A permanent rule protects that property from future pressure to widen NFR-014 (`probes.py:49-60`, "10 templates, 7 verbs"). B also avoids writing an interim sentence ("not established") that is designed to go stale, and it settles the question so it does not come back to the owner a second time.

## 3. Strengths claimed

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

## 4. Weaknesses identified in the others

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

## 5. Concessions

1. **"For now" leaves the question open.** The owner may be asked again, and C schedules no trigger for reopening (variant-3: "nothing is scheduled for that"). B's finality and A's explicit trigger are real advantages here.
2. **The "not established" sentence is designed to go stale.** Once OB-03 and OB-04 report, a second wording change follows. B is right about this.
3. **C applies one three-sentence text to two different lines, and that is wrong for one of them** (see A-001 below). `report.py:199` is the header value "Messages coverage: partial". That value is true, pinned by `tests/sweep/test_report.py:590` and shown in the design at `docs/designs/orchestrator-mode.md:610`. Only `report.py:534-535` makes the unproven claim. C copies MR:196's wording ("`report.py:199,534` carry exactly") literally. Read literally, it would put three sentences into a one-line header field and change a design line that C never mentions.
4. **C does nothing for the coordinator's view of its questions.** The coordinator still needs the observer, whose read is itself switched off (`QUESTION_GATE_PASSED = False`, MR:234) until Q6 and OB-06. If Q6 parks the read, "observer's alone" means nobody (A-002), and C does not address that.
5. **A's U-001 is a real consideration that C ignores.** If the holder-terminal rule (Q-1) means only the coordinator's own session can read, then the observer may be the wrong reader. C's "observer's alone" would then rest on a reader that may not work in the real layout (INV-024; OB-04 exists to find this out).

## 6. Shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 (both report lines take the same replacement text) | REJECT | `report.py:199` is a header field, "Messages coverage: partial". It is accurate, pinned by `tests/sweep/test_report.py:590`, and mirrored in the design at `docs/designs/orchestrator-mode.md:610`. Only the bullet at `report.py:534-535` asserts the unproven consumption claim (ADJ:813 targets "the sweep's `report.py:534`"). SW-07 (3) should be amended: keep line 199 as it is, and put the three-sentence text in the bullet at 534-535 only. If line 199 does change, design line 610 and test line 590 must change in the same PR. This applies to all three proposals, mine included. |
| A-002 (the observer will eventually read questions) | QUALIFY | This is a dependency, not a given. The guard is off on master (MR:234) and stays off if Q6 is unanswered (MR:254). C's "for now" holds up better than B's "never" here, because the owner can revisit Q10 if Q6 parks the observer's read. But C should say so explicitly: "reopen Q10 if Q6 is answered 'no' or OB-03/OB-04 record a result". |

## 7. Per-point positions

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

## 8. Overall verdict

Pick **C, amended in two ways**:

1. Apply the three-sentence replacement to the bullet at `report.py:534-535` only. Keep the accurate header "Messages coverage: partial" at line 199, with its test and design line unchanged.
2. Record a reopen trigger borrowed from A: "Q10 is reopened when OB-03 and OB-04 record a result, or if Q6 parks the observer's read".

Confidence: 75 percent. Reason: it removes the only unproven claim now, at no cost and without depending on a live test, and it leaves the "ever" decision to the evidence the program is already scheduled to produce.

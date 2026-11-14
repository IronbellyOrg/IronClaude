# Round 1 advocate statement: Variant 1 (Proposal A, hold OB-04)

Persona: qa (edge cases, failure scenarios, risk). Depth quick, Round 1.

## Position summary

Variant 1 is the only answer that cannot lose a question and cannot produce a false "no question disappeared" record, because both live variants rest on two unverified assumptions (A-001 usability in a terminal that already holds a Claude coordinator, A-002 detecting a lost question without consuming one). Holding OB-04 is also the spec's own written fallback (`merged-requirements.md:252` (4); `:557` default), so it is the safe state until those two assumptions have a written method; I concede below that Variant 3 is the better target once they do.

## Steelman of Variant 2

Variant 2 gets the most realistic evidence for the least effort. The questions panel exists to be used in real coordinator terminals, and only a real Run carries the real mix of workers, heartbeats, `--wait` re-arms and acknowledgement timing that INV-041 (c) says the seeded test lacks ("A bound Run replays the same Delivery until --ack", ADJ `:470`). It needs no extra coordinator session, worker or worktree (variant-2 "What it unlocks"). It also contributes the best detection idea of the three (U-002): compare the coordinator's own view before and after the read. It keeps every hard rule: never the program's own coordinator, no `run-use` (Q-2 forbidden, ADJ `:87`), written acceptance and a named Run id before the attempt, and it holds OB-06 if a question disappears.

## Steelman of Variant 3

Variant 3 is exactly the spec's recommended answer (`merged-requirements.md:557`: "A disposable representative Run you open for the test (a live `--wait` listener and an ack cycle), never the program's own") and the only live variant that satisfies every clause of OB-04 (1) (`:252`): owner-approved, not the alignment coordinator's own, "carries no work whose questions matter", disposable and representative. It closes the gap INV-041 (c) names by adding the listener and acknowledgement cycle a `run-create` throwaway Run lacks, while putting nothing of value at risk. Because the owner controls the test worker, the owner also knows which question was asked, which gives the record a ground truth outside the mailbox. It tears everything down afterwards (U-003) and unblocks OB-06.

## Key strengths claimed

1. Zero loss risk, by construction. X-016 is "unproven both ways" at 61 percent (ADJ `:144`). Orca's help says `--all` "does not mark read" (E-18), but the owner's only measurement on a coordinator Run was "non-diagnostic (0 pending is expected either way)" (ADJ `:144`). Variant 1 is the only variant whose safety does not depend on resolving that.
2. It is the spec's own fallback, not an invention. OB-04 (4): "if no such Run exists, OB-04 is held and OB-06 waits" (`merged-requirements.md:252`); Q30 default: "OB-04 held; OB-06 not opened" (`:557`). The guard is already `False` on this branch (`src/superclaude/cli/observe/commands.py:67`), and the panel is refused while it is (`commands.py:170`, `:185`), so holding changes no code.
3. It cannot write an untruthful record. OB-04 (2) requires the record to state "whether any question disappeared" (`:252`). Plain `check` reads and removes (ADJ `:97`), so the obvious way to check "before and after" can itself consume. A held OB-04 makes no such claim.
4. It matches the current environment. ORCA-AVAILABLE did not answer on 2026-11-13 (question.md fact 10, `merged-requirements.md:604`; current state not re-checked, UNVERIFIED). While Orca is down, neither live variant can run, so Variant 1 is the de facto state anyway.
5. It keeps OB-03 useful (U-001): the seeded test can still run and be recorded, so nothing done now is wasted when the owner later names a Run.
6. It needs no authority it does not have. Q30 does not authorize `run-use` or any Run other than the named one (question.md fact 9, `merged-requirements.md:578`), and naming none requires no `GRANT(OB-04,live-read)` row.

## Weaknesses identified in Variant 2

1. It breaks the spec's acceptance criterion. OB-04 (1) requires a Run that "carries no work whose questions matter" (`merged-requirements.md:252`). A Run from the owner's ordinary work carries exactly such questions (X-002). Written acceptance does not cure a criterion failure; a record from this Run would fail OB-04 as written and so could not satisfy OB-06 (c).
2. "Quiet moment" is not a control. A worker can call `ask` at any time; there is no Orca lock that keeps a Run quiet for the duration of the read. The variant admits it "lowers but does not remove that risk". Failure scenario: a worker asks at second 2 of the read, the read consumes, the coordinator's `--wait` never fires, the worker blocks on a question nobody sees.
3. Its detection method can cause the loss it detects. U-002 checks "against the coordinator's own view before and after". If that view is a plain `check`, it reads and removes (ADJ `:97`). If it is `check --all`, it is the same template under test (`adapter.py:32`: `("orchestration", "check", "--all", "--types", "question")`), so the comparison is circular. With unknown real traffic there is no outside ground truth for what should be there.
4. A consumed real question in the owner's other work is unrecoverable from the record, and the variant's step 4 ("the owner re-asks it in that coordinator") assumes the owner can tell which question was lost, which point 3 shows they may not.
5. It shares A-001 with Variant 3 (usability in a terminal holding a Claude session, UNVERIFIED, ADJ `:146`) but in a terminal running real work, where a failed attempt disturbs a real session.

## Weaknesses identified in Variant 3

1. The sequence can make the test non-diagnostic. Step 1 has the coordinator answer and the worker acknowledge before step 3's read. If the only question is already answered and acknowledged when the observer reads, there is nothing pending to consume, and "no question disappeared" is the expected result either way: the same flaw that made the owner's earlier measurement "non-diagnostic" (ADJ `:144`). The read must happen while at least one question is pending and unacknowledged.
2. The armed `--wait` can race the observer. If the coordinator's listener receives the question first, a later absence cannot be attributed to the observer; if the observer reads first and the listener still receives it, that is the real pass signal. Variant 3 does not specify the order or how the listener's receipt is recorded.
3. A-001 is unaddressed. It runs the read "in that coordinator's own terminal" while a Claude coordinator session holds it. Whether a person can use the panel there is UNVERIFIED (ADJ `:146`, `:497`). If the observer cannot run in that terminal (for example a second pane is not "the holder" under Q-1), the setup cost is spent for no record, and OB-04 (4) sends it back to Variant 1 anyway.
4. Setup cost and new failure surface: a person-opened coordinator session, a test worker and a worktree (worker-start creates one), all needing Orca to answer. Each is a step that can leave orphans if teardown (step 4) is skipped after a failure; the variant names no teardown check.
5. Representative "only in mechanism" (variant-3's own words): one worker, one question. It cannot show behaviour under concurrent questions or the program coordinator's continuous re-arm (`WORKER-CONTRACT.md:288` per probe R25-INV-008), so its pass is weaker evidence than a pass is likely to be read as.

## Concessions

1. Variant 1 does not answer the question. It is the default, not a choice; the release-2 questions panel never ships while it holds, and OB-03's result cannot become a flip (variant-1 "What it costs or risks").
2. Its re-trigger is vague: "asked again only if the owner wants the questions panel" has no date, condition or owner action attached, which risks indefinite drift.
3. It leaves INV-024 (usability in the real layout) permanently open, and INV-041 (d) says only a live attempt can close it.
4. On the merits of the question as asked, Variant 3 is the better target Run. My case is that Variant 1 is the right state until Variant 3's three gaps (pending question at read time, listener ordering, A-001) are written into the procedure, not that it is the better long-run answer.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | REJECT as an assumption; QUALIFY as a test item | Usability of the panel in a terminal already holding a Claude coordinator session is UNVERIFIED (ADJ `:146`, `:497`; INV-024 at `:465`). Variants 2 and 3 treat it as given. It should be checked first as a cheap preflight (can the observer start in that holder terminal at all) before any question is planted; if it fails, OB-04 (4) applies and the result is Variant 1. |
| A-002 | QUALIFY | True only where ground truth exists outside the mailbox. In Variant 3 the owner planted the question, so its id and text are known and the listener's receipt can confirm it survived; in Variant 2 real traffic gives no such ground truth, and a plain `check` to look consumes (ADJ `:97`). The record may claim "no question disappeared" only by comparing against the known planted question and the listener's receipt, never by a plain `check`. |
| A-003 | ACCEPT | OB-04 (1) states it ("Runs only after OB-03 passes", `merged-requirements.md:252`) and INV-041 (c), (d) explain why OB-03 is necessary but not sufficient (ADJ `:470`). One edge: if OB-03 fails, every variant collapses to Variant 1; that should be written into the ledger row. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie (nominally V3) | Same five sections and four steps; V3's step 4 adds teardown, the only structural extra of substance. |
| C-001 | V3 | The only live target that meets every clause of OB-04 (1) (`merged-requirements.md:252`) and matches the recommended answer (`:557`). |
| C-002 | V1 | No session, worker, worktree or Orca dependency; V2 is also zero-setup but buys that with real-work risk. |
| C-003 | V3 | Accepting consumption of a disposable Run costs nothing; V2 asks the owner to accept loss in real work, which OB-04 (1) excludes. |
| C-004 | V3 | Unblocks OB-06 with a record that can satisfy OB-06 (c); V2's record fails OB-04 (1) so cannot, and V1 blocks indefinitely. |
| X-001 | V3 | Gets listener and acknowledgement evidence with nothing of value at risk; V1 gets no evidence, V2 risks a real question. |
| X-002 | V3 | Complies with "carries no work whose questions matter" and still produces evidence; V1 complies only by producing nothing. |
| X-003 | V3 | Respects that a coordinator is person-opened while keeping it separate from real work; V2's convenience is the source of its X-002 conflict. |
| A-001 | V1 | The only variant whose outcome does not depend on the unverified holder-terminal usability (ADJ `:146`). |
| A-002 | V1 | The only variant that never has to assert "no question disappeared"; V3 is second because it can build ground truth from its planted question, V2 cannot. |

## Overall pick

Variant 3 as the named Run, with Variant 1 as the explicit written fallback: hold OB-04 until the procedure fixes a pending unacknowledged question at read time, records the listener's receipt order, and passes an A-001 preflight in the holder terminal.

# Round 1 advocate statement: Variant 3 (proposal C, a disposable representative Run opened for the test)

Persona: architect (structure, dependencies, long-term impact). Depth quick, Round 1 only.

## Position summary

Variant 3 is the only answer that both satisfies the spec's own OB-04 criterion (1) and produces the live evidence OB-06 needs, so it is the only one that keeps the dependency chain OB-03 -> OB-04 -> OB-06 moving without putting a real question at risk. Its cost is setup (one owner-opened coordinator, one test worker and its worktree), and its design needs one tightening: the observer must read while a known question is still pending, or the attempt proves nothing.

## Steelman of Variant 1

Variant 1 is the spec's own default verbatim: "OB-04 held; OB-06 not opened" (`merged-requirements.md:557`), and OB-04 (4) already says "if no such Run exists, OB-04 is held and OB-06 waits" (`merged-requirements.md:252`). It risks nothing: no Run is read, so no question can be lost and the program's own coordinator, which re-arms `--wait` continuously (`WORKER-CONTRACT.md:100`; probe INV-008 at `adversarial/adversarial/invariant-probe.md:16`), is never touched. It costs no setup at a time when the Orca app did not even answer on 2026-11-13 (`merged-requirements.md:604`, per question.md fact 10). The consumption question X-016 is "unproven both ways" at 61 percent (ADJ `:144`), and the panel is a release-2 feature, so waiting for OB-03's result before spending anything is a defensible sequencing choice. It also correctly keeps OB-03 runnable on its own (U-001).

## Steelman of Variant 2

Variant 2 gives the most representative evidence possible: a real coordinator with real workers, a real `--wait` listener and a real acknowledgement timeline, in the exact layout people use. That is precisely the gap OB-03 cannot close ("a live coordinator Run has `--wait` listeners and an acknowledge cycle that a throwaway Run lacks", `merged-requirements.md:1156`). It needs no extra coordinator session, worker or worktree. It still excludes the program's own coordinator, so it answers probe INV-008's core worry (`invariant-probe.md:16`), and the probe's own fix line allows the owner to "accept that risk in writing" (`invariant-probe.md:84`). It also contributes the best detection idea in the set: compare the coordinator's own view before and after the read (U-002), which gives the record's "whether any question disappeared" field a concrete method.

## Key strengths claimed

1. Spec compliance. OB-04 (1) requires a Run that "carries no work whose questions matter; the Run is disposable and representative (a live `--wait` listener and an ack cycle)" (`merged-requirements.md:252`). The spec's recommended Q30 answer is "A disposable representative Run you open for the test ... never the program's own" (`merged-requirements.md:557`), and the R25-INV-008 disposition row repeats "owner-approved disposable representative Run" (`merged-requirements.md:1316`). Variant 3 is the only variant that produces an OB-04 record satisfying criterion (1); Variant 2's record would fail it.
2. Closes the right gap. OB-03 is "necessary, not sufficient" because a throwaway Run lacks a listener and acknowledge cycle (`merged-requirements.md:1156`; invariant-probe INV-024 at `:32`). Variant 3 adds exactly those two mechanisms and nothing of value, so it isolates the variable under test (consumption under a live listener) from the cost of losing real work.
3. Unblocks the downstream chain. OB-06 needs "(c) OB-04 record linked" (`merged-requirements.md:254`). Under Variant 1 that prerequisite can never be met; under Variant 3 it can.
4. Known inputs make loss detectable. The owner starts the test worker on a trivial task that asks one known question (variant-3 step 1). Because the expected question is known in advance, the record can check whether the coordinator's own `--wait` received it, rather than relying on a later plain `check`, which itself "reads and removes a message" (ADJ `:97`). This is a structural answer to A-002 that a real Run cannot give.
5. Answers INV-024 cheaply. Whether a person can use the panel in a terminal that already holds a Claude coordinator session is UNVERIFIED (ADJ `:146`). If it turns out unusable, Variant 3 discovers that in a throwaway session; Variant 2 discovers it in the middle of real work.
6. Clean teardown (U-003) leaves no long-lived Run, worker or worktree behind, which keeps the Run record from accumulating more coordinator-less Runs (28 of 53 already lack `coordinator_handle`, `merged-requirements.md:1157`).

## Weaknesses identified in Variant 1

1. Its "unlocks: nothing new" is a permanent block, not a pause. OB-06 (c) needs an OB-04 record (`merged-requirements.md:254`); Variant 1 gives no path to one, so the questions panel "never ships while held" (variant-1 "What it costs"). Its step 4 re-asks Q30 later but with the same three options, so it defers rather than decides.
2. It makes OB-03 non-actionable. OB-03 "cannot be turned into a flip" (variant-1 "What it costs") because OB-03 alone is explicitly insufficient (`merged-requirements.md:1156`). Running OB-03 under Variant 1 spends live-test effort for a result with no consumer.
3. It leaves INV-024 (usability in the real layout) open indefinitely, which is the second reason OB-06 is gated (`merged-requirements.md:1157`).

## Weaknesses identified in Variant 2

1. Direct conflict with OB-04 criterion (1): "carries no work whose questions matter" (`merged-requirements.md:252`). A Run from the owner's ordinary work carries questions that matter by definition, so the resulting record cannot satisfy OB-04 as written; either the spec row must be amended or the attempt does not count (diff X-002).
2. "Quiet moment" is a judgment, not a control. It lowers but does not remove the risk (variant-2 "What it costs"), and a quiet moment also means no pending question, which makes the consumption check non-diagnostic: ADJ E-18 already records that "0 pending is expected either way" makes such a measurement non-diagnostic (ADJ `:144`). Variant 2 is therefore either risky (questions pending) or uninformative (none pending).
3. Unknown inputs. In a real Run the set of questions in flight is not known in advance, so "whether any question disappeared" depends on the coordinator's own view, and getting that view may require a consuming read (A-002).
4. Recovery is weak. Its step 4 ("the owner re-asks it in that coordinator") assumes the owner knows which question was lost and who asked it; in a real Run with several workers that is UNVERIFIED.

## Concessions

1. Setup cost is real (C-002): an owner-opened coordinator session (coordinators are person-opened, `src/superclaude/core/CLAUDE.md:58`), a test worker and the worktree worker-start creates, plus ORCA-AVAILABLE. Variants 1 and 2 are cheaper.
2. Representative only in mechanism. One worker and one question do not reproduce real message rates or multi-worker interleaving (real message rate is UNVERIFIED, ADJ `:146`). Variant 2 is more representative.
3. A design gap in my own variant: variant-3 step 1 completes the question-answer-acknowledge cycle before step 3 runs the observer read. If the read happens after the acknowledgement, no question is pending and the attempt is non-diagnostic in the same way as E-18 (ADJ `:144`). The fix is to run the observer read while the test worker's question is pending, then confirm the coordinator's `--wait` still delivers it and the acknowledgement completes. I adopt Variant 2's before-and-after comparison (U-002) as the detection method.
4. Variant 3 inherits A-001 unresolved; it only makes failure cheaper to discover.

## Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001 (observer can run in the holder terminal while a Claude coordinator session holds the Run) | QUALIFY | Q-1 FAIL forces the read into the holder terminal (ADJ `:87`), so both live variants must assume it, but usability there is UNVERIFIED (ADJ `:146`). It should be stated as a hypothesis the attempt tests, with "panel not usable in the holder terminal" as a valid recorded outcome that holds OB-06 (`merged-requirements.md:1157`). The disposable Run is the safer place to falsify it. |
| A-002 (a consumed question can be detected afterwards without consuming) | QUALIFY | Not true in general: plain `check` reads and removes (ADJ `:97`). It holds only when the expected questions are known in advance and loss is judged by whether the coordinator's own `--wait` still delivers them. That is achievable in a disposable Run with a scripted question, not reliably in a real Run. The record procedure should name this method explicitly. |
| A-003 (OB-03 passes before OB-04) | ACCEPT | Stated in OB-04 (1) "Runs only after OB-03 passes" (`merged-requirements.md:252`) and in the chain at `merged-requirements.md:805`. If OB-03 fails, the questions read is unsafe and OB-04 should not run under any variant. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie | All three have the same five sections and four steps; structure does not separate them. |
| C-001 | V3 | Only a disposable representative Run meets OB-04 (1) and the spec's recommended answer (`merged-requirements.md:252`, `:557`). |
| C-002 | V1 | Zero setup; V2 also zero; V3's extra session, worker and worktree is its main cost. |
| C-003 | V3 | Written acceptance of consumption is meaningful and cheap when nothing of value can be lost; V2 asks the owner to accept loss of real work. |
| C-004 | V3 | V2 and V3 both let OB-06 proceed, but V2's record conflicts with OB-04 (1) and may not count; V1 blocks OB-06 indefinitely. |
| X-001 | V3 | Representative in the two mechanisms OB-03 lacks (listener, acknowledgement) with no loss of value; V2 trades harm for marginal extra realism. |
| X-002 | V3 | V1 and V3 both comply, but only V3 complies and also yields the record OB-06 (c) requires. |
| X-003 | V2 | The Run already exists, so no extra person-opened session is needed; low impact. |
| A-001 | V3 | Same unverified assumption in V2 and V3, but V3 tests it in a throwaway session where a failure costs nothing. |
| A-002 | V3 | A scripted, known question lets loss be detected without a consuming read; V2 contributes the comparison method (U-002) that V3 should adopt. |

## Overall pick

Variant 3, amended so the observer reads while the test worker's question is still pending and adopting Variant 2's before-and-after comparison for loss detection.

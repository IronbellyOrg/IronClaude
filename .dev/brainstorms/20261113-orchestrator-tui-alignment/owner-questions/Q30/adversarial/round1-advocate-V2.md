# Round 1 advocate statement: Variant 2 (proposal B, a real coordinator Run at a quiet moment)

Persona: frontend (does the panel work for the people who will actually use it). Depth quick, Round 1.

## Position summary

Variant 2 is the only option that tests the questions panel where people will really use it: in the terminal of a coordinator doing real work, with real message volume and a real `--wait` listener, at no setup cost. It conflicts with the literal OB-04 criterion (1) and its "quiet moment" mitigation weakens its own diagnostic value, so I argue its usability evidence and its detection method should be carried into Variant 3 rather than adopted as written.

## Steelman of Variant 1

Variant 1 (hold OB-04, guard stays off) is the spec's own default ("OB-04 held; OB-06 not opened", `question.md:15`) and the only option with zero chance of losing a question anywhere. It costs nothing to set up, and it fits the current facts: Orca did not answer on 2026-11-13 (`merged-requirements.md:604`), so no live lane can run anyway until ORCA-AVAILABLE reopens. It keeps OB-03 alive (U-001), so seeded evidence still accumulates, and it defers the decision until the owner actually wants the panel, with OB-03's result in hand (variant-1 step 4). For a read-only dashboard whose core worker views already work with the guard `False`, "do nothing risky until needed" is a defensible product call.

## Steelman of Variant 3

Variant 3 is the spec's recommended answer almost word for word ("A disposable representative Run you open for the test (a live `--wait` listener and an ack cycle), never the program's own", `question.md:11`) and is the only live option that satisfies every OB-04 criterion: holder terminal only, no `run-use`, a Run that "carries no work whose questions matter", disposable and representative (`merged-requirements.md:252` (1), (3)). It closes the exact gap INV-041 (c) names, that a throwaway Run "has no `--wait` listeners or acknowledge cycle" (ADJ `:470`), while putting nothing of value at risk. Because the owner's test worker asks a known question, the test has ground truth: the record can say whether that specific question disappeared. The owner's written acceptance is meaningful because the thing accepted (loss of a test question) is cheap. Teardown (U-003) leaves no residue.

## Key strengths claimed

1. **Real usability evidence, which is what INV-024 asks for.** INV-024 is about whether "the flipped questions panel may not work for the Runs people point it at" and demands "one live attempt in the real coordinator layout" (ADJ `:465`). A coordinator session already doing real work is that layout by definition: real scrollback, real competing output from the Claude session, real question cadence. Real message rate is listed as UNVERIFIED (ADJ `:146`), and only a real Run exercises it. A one-worker, one-question synthetic Run is "representative only in mechanism" by Variant 3's own admission (variant-3, costs bullet 2).
2. **Zero setup.** No extra coordinator session, no test worker, no worktree (variant-2, unlocks bullet 2). Variant 3 needs a person-opened coordinator plus a `worker-start` worktree (variant-3 costs bullet 1), all gated on ORCA-AVAILABLE, which was down on 2026-11-13 (`merged-requirements.md:604`).
3. **A concrete loss-detection step (U-002).** Variant 2 is the only variant that says how "whether any question disappeared" is established: compare the coordinator's own view before and after the read (variant-2 step 3). OB-04 (2) requires that field (`merged-requirements.md:252`), and diff-analysis A-002 shows neither live variant otherwise explains it.
4. **A defined failure response.** If a question disappears, OB-06 is held and the owner re-asks it in that coordinator (variant-2 step 4). That is a recovery path for the person whose question was lost, not just a gate result.

## Weaknesses identified in Variant 1

1. **The panel never ships.** OB-06 needs OB-04's record (`merged-requirements.md:254` (c)); holding OB-04 means the release-2 feature waits indefinitely (variant-1 costs bullet 1). From a user's view, the coordinator-questions panel is the feature that makes the dashboard worth opening during a Run.
2. **INV-024 stays open forever.** Variant 1 states it plainly: "Everything about usability in the real layout" stays unresolved (variant-1 last section). Re-asking later with OB-03 in hand does not help, because OB-03 "says nothing about usability" (INV-041 (d), ADJ `:470`).
3. **No ask-again trigger.** Step 4 re-asks Q30 "only if the owner wants the questions panel"; nothing in the variant records what evidence would change the answer, so the hold has no exit condition.

## Weaknesses identified in Variant 3

1. **The planned sequence leaves nothing pending to read.** Step 1 completes the cycle (worker asks, coordinator answers, worker acknowledges) before step 3's read. If the question is already answered and acknowledged when the observer reads, the panel has nothing to show and nothing to consume. That is the same non-diagnostic shape ADJ `:144` records for the owner's earlier measurement ("0 pending is expected either way"). The read must happen while at least one question is unanswered.
2. **Usability evidence is thin.** One worker and one question in a session opened only for the test does not show whether a person can find and act on a question among real coordinator output. It answers "does the mechanism run", not "does the panel work for its users".
3. **A-001 is not avoided.** The test coordinator is itself a Claude coordinator session, so Variant 3 hits the same UNVERIFIED question (can the panel be used in a terminal that already holds a Claude coordinator session, ADJ `:146`) with no advantage over Variant 2.
4. **Setup is heavy and fully live-gated.** A person-opened session, a worker, a worktree and teardown, each needing Orca to answer (`merged-requirements.md:604`). Any one failing delays OB-04.
5. **No detection method stated.** It records "whether any question disappeared" (step 3) but not how, given that plain `check` itself consumes (ADJ `:97`).

## Concessions

1. **Variant 2 conflicts with the spec text.** OB-04 (1) requires a Run that "carries no work whose questions matter; the Run is disposable" (`merged-requirements.md:252`). A Run from the owner's ordinary work fails that on its face (X-002). Adopting Variant 2 would also make the record OB-06 (c) links noncompliant.
2. **The harm is real and unbounded by evidence.** X-016 is "unproven both ways" at 61 percent (ADJ `:144`); if the read consumes, a real question in the owner's other work is lost, and the worker may stall on it (variant-2 costs bullet 1).
3. **"Quiet moment" defeats the test.** Choosing a moment when "no worker in it is waiting on an answer" (variant-2 answer) means nothing is pending, so neither consumption nor the panel's display of a question can be observed. The mitigation that lowers harm also removes most of the consumption evidence; only layout usability survives.
4. **Before and after comparison lacks ground truth.** In a real Run the owner does not control which questions exist, so "the coordinator's own view" may itself be the `--wait` listener whose replay behaviour ("A bound Run replays the same Delivery until --ack", ADJ `:470`) could mask a consumed message. Variant 3's known test question is better ground truth.
5. **The owner's judgment of "quiet" is unverifiable** after the fact (variant-2 costs bullet 3).

## Shared assumption responses

| ID | Response | Reason |
|----|----------|--------|
| A-001 | QUALIFY | It is not a premise to assume but the thing OB-04 measures (INV-024, ADJ `:146`). The record must treat "panel not usable in the holder terminal" as a valid recorded result, not a failed attempt. It also needs the mechanism named: a second pane or tab is a different terminal and Q-1 says it cannot read the Run (ADJ `:87`); whether the Claude session's own shell (its Bash tool or a `!` command) counts as the holder terminal is UNVERIFIED. |
| A-002 | QUALIFY | Detection cannot use plain `check`, which reads and removes (ADJ `:97`). It must rest on ground truth recorded outside the mailbox: the asking worker's own record of the question it sent, plus the coordinator's received-delivery output, compared before and after the read. That requires a question to be pending at read time, which neither variant's sequence guarantees. Variant 3 can supply that ground truth; Variant 2 cannot. |
| A-003 | ACCEPT | Stated in OB-04 (1) ("Runs only after OB-03 passes", `merged-requirements.md:252`), and OB-03 is cheap, harmless to real work, and cites `check --help` first (INV-041 (a)). |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|-------|------------------|-----------------|
| S-001 | Tie | All three use the same five sections and four steps; no difference to judge. |
| C-001 | V3 | A disposable Run is the only live choice that meets OB-04 (1) "carries no work whose questions matter". |
| C-002 | V2 | Live evidence with zero setup; V3 needs a session, a worker and a worktree, all Orca-gated. |
| C-003 | V3 | Written acceptance is cheap and honest when the thing accepted is a test question, not real work. |
| C-004 | V3 | V2's flip would link a record that breaks OB-04 (1), so OB-06 (c) is cleaner under V3; V1 blocks the flip entirely. |
| X-001 | V3 | Representative in mechanism with nothing of value lost; V2's better layout realism does not justify losing a real question. |
| X-002 | V3 | V3 (and V1) comply with the spec text; V2 conflicts with it directly. |
| X-003 | V2 | Uses an already open coordinator; low impact, but V3 must wait for the owner to open one personally. |
| A-001 | V2 (marginal) | Both hit the same unknown, but V2 tests it in the exact terminal a person is actually working in, which is what INV-024 asks. |
| A-002 | V2 (method) / V3 (ground truth) | V2 alone names a detection step (U-002); V3 alone has a known question to detect; the merge needs both. |

## Overall pick

Variant 3, amended with Variant 2's before and after comparison (U-002) and a rule that the read happens while the test worker's question is still unanswered.

# Round 1, Variant 2 advocate: D2 option (b), relayed Ruling

Citation key as in `diff-analysis.md`: `SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`. Every line below was re-read for this round. The spec's `qa.md:238` anchor is stale; the rule is at `QA:254` (U-001).

## Position summary
Choose (b) in a corrected form: an opt-in relay route that runs only after `/sc:implement` has stopped on an `E-HALT-QA` that wrote a `halt` record. The worker session asks the coordinator with the halt explanation, the coordinator answers with the person's exact words, the worker appends one Ruling line that quotes them and cites the reply's message ID, then re-runs the same command line, and resume row R completes the task. This needs a narrow edit to `QA:254` and a new WC-3 route, and on provenance it is weaker than (a) and (c), which I concede.

## Steelman
### Variant 1 (a)
In (a), and only in (a), the person confirms the executor's own scoped explanation in the conversation the rule names (`QA:254`). The executor then writes the line itself (`QA:256`). It costs nothing: the spec already carries the exception (`SPEC:67`, `SPEC:132`). It protects a serious decision, because `E-HALT-QA` follows a confirmed blocker that a repair could not close (`QA:280`). Halts are rare (`QA:274`, `QA:288`). Its reversibility point is sound: relaxing the rule later is cheap, but restoring trust after a bad relay is not (U-003).

### Variant 3 (c)
(c) keeps the rule unchanged and still keeps the plan in Orca. Its mechanism is correct for a ladder halt. A line written after the `halt` is eligible (`RETRY:498` (a)). Row R runs before rows P and H, so the task completes with no review and its verdict unchanged (`LEDGER:154`). It is a superset of (a). It has the only deterministic live check (U-010), and it states the single-writer precondition (`LEDGER:145`, `SPEC:70`).

## Strengths claimed
1. **(b) has a working resume path, the same one (c) uses.** This answers the diff analysis finding (C-005, X-003) that (b) has no resume path. The original Variant 2 was wrong to say the worker "keeps its session, its ledger position and its retry state": any `halt` is terminal (`RETRY:488`) and the command has stopped. The corrected sequence uses only existing mechanics:
   (i) `E-HALT-QA` writes the non-compliant verdict and the `halt` record (`SKILL:33`).
   (ii) The command writes its blocked contract and stops (WC-2 (c), `SPEC:66`).
   (iii) The worker session asks once with `ask` (`CAPS:58`).
   (iv) On the reply, the worker appends `T<id>: Ruling: <what, quoting the person verbatim, relayed in Orca reply <msg_id>> — <why> — <cost-if-wrong>`. A Ruling is allowed after a halt (`LEDGER:110`) and the line carries "user confirmation provenance" (`QA:259`).
   (v) The worker re-runs the same command line with the same report directory (WC-3, `SPEC:67`). Resume is implicit (`IMPL:57`), the line is eligible (`RETRY:498` (a)), and row R appends the post-ruling `complete` with no review (`LEDGER:154`). Later tasks then run.

   The answer goes into the ledger, not onto the command line, so it does not need a Ruling flag. The diff analysis is right that WC-3's existing route does not fit: it requires a gate "before the command has written any output" whose answer "fits an existing argument or flag" (`SPEC:67`). So (b) adds a second, named route. It does not reuse the first.
2. **No Orca call inside a command (SA-2, `SPEC:170`).** The `ask` happens in the worker session after the command has stopped, where WC-3's existing ask already happens (`SPEC:67`, owner "Worker session"). This answers C-007's SA-2 concern: no `ask` happens mid-command.
3. **Single writer, well-formed line.** The command has stopped before the session appends, and the session re-invokes only after, so one writer exists by construction (`LEDGER:145`). The agent checks the line against `^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$` (`LEDGER:71`) before appending, so a hand-typed hyphen cannot produce `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`). The diff analysis found that risk in (c) (spot-check 4).
4. **The person is told by construction (A-008).** The `question` arrives in the coordinator's standard wait (`CAPS:63`), and the route requires asking the person. Under (a) and (c) the halt is one more `worker_done failed`, which the coordinator may retry or report (`SPEC:84`); nothing says it must reach the person.
5. **No file access needed (A-009).** The person never opens the worker's ledger. (a) and (c) assume the person's session sees the worker's files, though the brief sets placement (`SPEC:79`, `CAPS:115`).
6. **The fewest steps for the person.** Under (b) the person answers one question. Under (c) the person types three fields with em dashes (`LEDGER:68`) and tells the coordinator, and the coordinator creates a new Task (WC-6, `SPEC:70`). Under (a) the plan leaves Orca (V1 line 19).
7. **The explanation is relayed from its source.** The worker builds the `--question` from the halt message (`RETRY:490`) plus the fields `QA:254` requires, and the coordinator must forward it unedited. This is weaker than (a), but (c) has no explanation step at all (C-003).
8. **Opt-in, so a superset of (a).** The route runs only when the brief has a new line `On a Ruling halt: relay to the person`. Without that line a Ruling halt is reported blocked, exactly as in (a). The person can still resume in their own session.

## Weaknesses identified
**Variant 1 (a)**
1. Its resume is heavier than it states (C-005). With a `halt` and no Ruling, resume goes to row H, which runs a fresh operator review and re-halts with `reason=operator-review` (`LEDGER:156`) before the executor can explain and ask. The person pays for a full review before they can give the Ruling.
2. "The remaining tasks of that plan leave Orca" (V1 line 19), and X-002 shows this is not forced: a person-given Ruling can return the plan to Orca through row R.
3. It assumes the person learns of the halt (A-008) and can reach the worker's ledger (A-009). Neither is stated.

**Variant 3 (c)**
1. Its malformed-line claim is wrong (spot-check 4). A hand-appended line is the ledger's last line, so a bad one, for example hyphens typed instead of em dashes (`LEDGER:68`), stops resume with `E-LEDGER-CORRUPT` (`LEDGER:123`; `SKILL:36`: "No further"). It does not fall to row H. Recovery then needs a second hand edit.
2. It skips the scoped explanation `QA:254` requires before acceptance is asked, and the person writes all three fields alone (V3 line 21). That is the safety step (b) keeps in relayed form.
3. Its provenance is policy only (A-010). Eligibility depends only on the line's position (`RETRY:498`), and any agent with file access can append a line. "The person typed it" is no more checkable than "the coordinator relayed it". V3's support, "Existing operator-written records remain valid" (`QA:256`), was marked OVERSTATED (spot-check 2): it reads as a backward-compatibility clause, so (c) also needs protocol wording.
4. It needs three handoffs (person edits the file, person tells the coordinator, coordinator creates a new Task) where (b) needs one answer.

## Concessions
- The original Variant 2 said (b) "matches how the spec treats other gates". That was wrong (X-003, spot-check 6). (b) needs a new WC-3 route.
- The original said the worker keeps its retry state. That was also wrong: the command stops at the halt (`RETRY:488`). Continuity comes from row R, the same mechanism (c) found (U-007).
- The provenance conflict is real (X-001, X-004). The reply is the coordinator's message (`CAPS:62`), which `QA:254` excludes, and the worker cannot tell paraphrase from quotation (A-005). At best a bad relay is found afterwards, when the person compares the ledger line with what they said; nothing prevents it. On safety, (a) is strongest and (c) is next.
- (b) costs the most to build: edits to `QA:254`, the `LEDGER:62-68` wording ("executor-recorded"), WC-3, the implement row (`SPEC:132`), AC-4.1 (`SPEC:274`) and non-goal 6 (`SPEC:319`). (a) and (c) need no protocol change.
- No test can check relay fidelity (C-008). The (c) test is deterministic.
- Halts are rare (`QA:274`, `QA:288`), so the speed gain from (b) is small per plan (A-006). If the user values the unchanged rule above one-answer convenience, (c) is the better choice: it gives most of the Orca continuity with no rule edit.

## Shared assumption responses
| ID | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | `QA:254` lists "another agent's message", and the reply is the coordinator's (`CAPS:62`). (b) therefore needs a rule edit; reinterpreting the rule is not enough. |
| A-002 | ACCEPT | Row R keeps the latest `blocked` verdict unchanged (`LEDGER:154`, `QA:248`). Under (b) too, a relayed Ruling never makes a task `compliant`. |
| A-003 | ACCEPT | The corrected (b) now depends on it. The ledger plus row R is the resume mechanism (`LEDGER:137`, `LEDGER:154`). |
| A-004 | QUALIFY | It also covers the `dispute` halt (A-011). `E-NO-RULING` writes no `halt` record (`SKILL:35`), so a relayed line after it is eligible only under `RETRY:498` (b). The relay route is limited to `E-HALT-QA`. |
| A-005 | ACCEPT | This is the central risk of (b), and the concessions say so. |
| A-006 | ACCEPT | Halts are rare (`QA:274`, `QA:288`). That shrinks both the benefit of (b) and the exposure created by its rule edit. |
| A-007 | ACCEPT | `CAPS:62`. The worker records the reply's message ID as provenance. That proves which message it was, not who spoke the words in it. |
| A-008 | QUALIFY | (b) closes this gap: the `question` lands in the coordinator's wait (`CAPS:63`) and the route requires asking the person. For (a) and (c) the spec must add a duty to surface the halt to the person. |
| A-009 | REJECT for (b) | The person never touches the worker's files. The assumption holds only for (a) and (c), where placement can differ from the person's worktree (`SPEC:79`, `CAPS:115`). |
| A-010 | QUALIFY | Provenance in every variant rests on trust, because eligibility depends only on position (`RETRY:498`). (b) trusts an LLM relay, which carries more risk. (c) trusts that nothing but the person wrote to the file. Neither can be checked by mechanism. |
| A-011 | ACCEPT | A `dispute` writes `halt ... reason=dispute` and stops with `E-HALT-QA` (`RETRY:107`), so it falls inside the relay route. When the person's answer is "change the AC", that is a plan edit, not a Ruling. The worker reports it blocked. |
| A-012 | ACCEPT | The corrected (b) asks only when the task's last record is a `halt` after its latest `blocked`. After a transient stop (`RETRY:500`) or a `retry` with no `halt`, it reports blocked and does not ask. |

## Per-point positions
| ID | Superior | Reason |
|---|---|---|
| S-001 | equal | Section layout only (L1). |
| S-002 | V3 | It cites the eligibility rule. The original V2 had no LEDGER or RETRY anchor; this round adds them. |
| S-003 | V1 | It found the stale `qa.md:238` anchor. The fix applies whatever option wins. |
| S-004 | V2 | It names its own undetectable failure mode, though the original gave no mitigation. |
| S-005 | V3 | It framed itself as a superset of (a) first. The corrected (b) is opt-in and is also a superset. |
| S-006 | V3 | It is the only variant that proposes a concrete, deterministic AC-4.1 extension. |
| C-001 | V1 | The person confirms the executor's own explanation in the conversation `QA:254` names. |
| C-002 | V1 | The executor writes the line in the person's session, as `QA:256` says. |
| C-003 | V1 | Only V1 keeps the executor's own explanation. V2 relays it; V3 drops it. |
| C-004 | V2 | One answer and the same worker continues. V3 needs a file edit, a message and a new Task. |
| C-005 | V3 | It found the row R path. The corrected V2 uses the same path. |
| C-006 | V3 | No session is held waiting on a person, and a late answer needs no timeout handling. |
| C-007 | V1 | No protocol change and no spec change. |
| C-008 | V3 | Its live check is deterministic. Relay fidelity under V2 cannot be tested. |
| C-009 | V2 | One writer by construction: the command stops, the session appends, then the session re-invokes (`LEDGER:145`). |
| C-010 | equal | V1 and V2 format the line by agent. V3's hand-typed line risks `E-LEDGER-CORRUPT` (`LEDGER:123`). |
| C-011 | V1 | It makes the frequency argument (`QA:274`, `QA:280`, `QA:288`). |
| C-012 | V1 | Relaxing the rule later is cheaper than restoring trust after a bad relay. |
| X-001 | V1 | A relayed Ruling conflicts with `QA:254` as written. V2 concedes a rule edit is needed. |
| X-002 | V3 | Row R shows the plan can stay in Orca. V1's claim that it must leave is falsified. |
| X-003 | V1 | WC-3's existing route does not fit a Ruling halt (`SPEC:67`). V2 now proposes a new route. |
| X-004 | V1 | V2's tension is real: the person decides, but the worker cannot prove it. |
| A-008 | V2 | The `question` reaches the coordinator's wait (`CAPS:63`) and the route requires asking the person. |
| A-009 | V2 | The person needs no access to the worker's files. |
| A-010 | equal | Each variant rests on trust that no mechanism can check (`RETRY:498`). |
| A-011 | equal | Every variant must cover the `dispute` halt (`RETRY:107`). None did. |
| A-012 | V3 | It partly stated the condition. The corrected V2 adopts it as its precondition for asking. |

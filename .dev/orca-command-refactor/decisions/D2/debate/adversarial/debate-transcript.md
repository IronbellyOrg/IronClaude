# Adversarial Debate Transcript

## Metadata
- Decision: D2 of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (lines 333-337): when `/sc:implement` halts for a Ruling inside an Orca worker, who may give the Ruling?
- Mode: A (compare existing files). Variants: V1 = `variant-1-original.md`, option (a); V2 = `variant-2-original.md`, option (b); V3 = `variant-3-original.md`, option (c).
- Depth: standard
- Rounds completed: 2 (Round 1 advocate statements, Round 2 rebuttals), plus Round 2.5 invariant probe. Round 3 skipped: depth is standard, so the maximum is 2 debate rounds.
- Convergence achieved: 100% diff-point agreement (27 of 27 points); final status BLOCKED_BY_INVARIANTS (6 HIGH UNADDRESSED invariants, see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3
- Diff points scored: 27 = S-001..S-006 (6) + C-001..C-012 (12) + X-001..X-004 (4) + promoted shared assumptions A-008..A-012 (5). The STATED shared assumptions A-001..A-007 were answered ACCEPT/QUALIFY by the advocates but are not promoted diff points, so they are not in the matrix.
- Position source: each advocate's Round 2 "Final per-point positions" table. All three Round 2 tables cover all 27 points, so no Round 1 fallback was needed. Round 1 "Per-point positions" were used only for the round-over-round agreement record.
- Agreement rule: a point is agreed when at least 2 of 3 advocates name the same answer (a single variant, or the same "equal" set). "equal (V1, V3)" and "equal" are different answers.
- Confidence calibration: unanimous points 90-99%, majority 60-89%, split 50%. Within unanimous: 95% if no advocate changed position between Round 1 and Round 2, 92% if at least one changed; +3 when an advocate of a losing variant explicitly conceded that point in Round 2 (cap 98%; never 100%).
- Embedded round files: the Round 1 and Round 2 sections below contain `rounds/r1-variant-{1,2,3}.md` and `rounds/r2-variant-{1,2,3}.md` verbatim, including their own `#` headings.

## Round 1: Advocate Statements

### Variant 1 Advocate (option (a): keep the rule, person resumes in own session)
# Round 1: Variant 1 advocate, D2 option (a)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `QA:N`, `LEDGER:N`, `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/{qa,ledger,retry}.md:N`; `IMPL:N` = `src/superclaude/commands/implement.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`. Every citation below was re-read in this round.

## Position summary
Keep the Ruling rule unchanged: a worker that halts for a Ruling reports `blocked`, ends `failed`, and the person gives the Ruling through the executor in their own session, the only route where the executor itself explains the scope and hears the person directly (`QA:254`). V3's "return the rest of the plan to Orca" idea is a good follow-on I partly adopt, but its hand-written line is a weaker entry point; V2 needs a protocol rewrite and a coordinator route the spec does not have.

## Steelman

### Variant 2 (b): relayed Ruling
The person still decides and the plan keeps moving. Orca's `ask` is built for a blocking worker question: a timeout leaves it pending and resumes by message ID (`CAPS:60`), no heartbeat is needed while blocked (`CAPS:64`), and `reply` is the designed answer channel (`CAPS:62`). The Ruling line already carries "user confirmation provenance" (`QA:259`). The person answers one question in the coordinator's session and the plan never leaves Orca. If relays are faithful, this is the fastest route.

### Variant 3 (c): hand-written Ruling plus resume Task
It keeps my safety property (no agent carries the Ruling) and removes my main cost (the plan leaving Orca). After an `E-HALT-QA` that wrote a `halt`, a later Ruling is eligible under clause (a) (`RETRY:498`), row R runs before P and H and appends the post-ruling `complete` with no review (`LEDGER:154`), and `--resume` is implicit (`IMPL:57`), so a fresh Task finishes the plan unattended. No protocol change, an explicit single-writer precondition (`LEDGER:145`, `SPEC:70`), and my route kept as fallback.

## Strengths claimed
1. **The only route that meets the asking path in full.** `QA:254`: "Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong." Under (a) the executor explains and hears "clear user confirmation in the current conversation" directly. V2 dilutes the explanation; V3 skips it (C-003).
2. **The Ruling is eligible by construction and judged on the current tree.** In the person's session, resume hits row H: one fresh operator review of the tree as it stands; if still non-compliant, `blocked` plus `halt ... reason=operator-review` and STOP `E-HALT-QA` (`LEDGER:156`; row P likewise, `LEDGER:155`). The Ruling then follows that `halt`, so clause (a) of `RETRY:498` holds. If the review returns `compliant`, no Ruling is needed. C-005 calls this an omission in my paper; I correct it and count it a strength: a free second look before a person accepts a failed deliverable.
3. **The executor writes the line, so it cannot be malformed.** The Ruling regex needs em dashes and three fields (`LEDGER:71`); a bad last line stops resume with `E-LEDGER-CORRUPT` (`LEDGER:123`). Under (a) the person never types the record ("the user need not hand-write a ledger record", `QA:254`).
4. **Zero change, already testable.** WC-3 already carries the exception ("A Ruling halt is never asked", `SPEC:67`), the implement row restates it (`SPEC:132`), and AC-4.1 checks it live: no `question` message and no Ruling in the ledger (`SPEC:274`).
5. **It already covers the `dispute` halt.** A dispute appends `halt review=<k> reason=dispute` and stops `E-HALT-QA` (`RETRY:107`), so WC-3's `E-HALT-QA` exception routes it to the person too.
6. **Rare by design.** Minors and notes never halt or prompt (`QA:274`, `QA:288`); `E-HALT-QA` needs a confirmed blocker that a repair could not close (`QA:280`).
7. **Cheap to relax later, costly to un-relax.** A relayed Ruling that goes wrong records an accepted gap that resume will never revisit (row 1, `LEDGER:153`).

Citation correction (extends U-001): the stale `qa.md` anchors sit at four places, not one: `SPEC:67` and `SPEC:319` cite `qa.md:238`, `SPEC:132` cites `qa.md:231-238`, `SPEC:334` cites `qa.md:232,238`. Whichever option wins, they should point at `QA:247-249` (Halt table rows) and `QA:254-256` (the confirmation rule and the recording rule).

## Weaknesses identified

### Variant 2
1. **It breaks the rule it relies on.** `QA:254` lists "another agent's message" as not acceptance, and the coordinator's answer arrives as its `reply` (`CAPS:62`). V2 concedes this (its line 13) while also claiming "the person still decides" (its line 9); the worker cannot check which is true (X-001, X-004).
2. **The route it claims does not exist.** WC-3's ask route applies only "at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag" (`SPEC:67`). A Ruling halt fires after ledger records exist, and `/sc:implement`'s flags are `--resume`, `--ledger`, `--skip-final-review` (`IMPL:57-59`), none of which carries a Ruling. V2's "matches how the spec treats other gates" is OVERSTATED (spot-check 6).
3. **"Keeps its retry state" is wrong.** Any `halt` is terminal and the ladder is never re-entered (`RETRY:488`); the command has already stopped. Asking from inside the command would put an Orca call in a command, which SA-2 forbids (`SPEC:170`). So (b) needs a new route designed, not just a rule lifted.
4. **Its test cannot see the failure it introduces.** AC-4.1 (b) checks the Ruling quotes "the person's words verbatim" (`SPEC:274`), but the worker only has the coordinator's text, so a paraphrase passes.
5. **It holds a worker session open for a human wait**, and a late answer needs a new Task anyway (`SPEC:67`), which is the same re-dispatch V1 and V3 already use.

### Variant 3
1. **It skips the explanation the asking path requires.** The person composes all three fields from the halt message alone (`QA:247`: ledger path, task, verdict, missing citations). Not a protocol violation, since row `QA:248` accepts "valid existing operator Ruling", but the person decides with less in front of them (spot-check 1).
2. **Its malformed-line claim is wrong.** V3 says a malformed line "is ignored and the resume halts again (`LEDGER:156`)". Row H says nothing about that; a hand-appended line is the last line, and an unparseable last line is `E-LEDGER-CORRUPT` (`LEDGER:123`). Hyphens typed for the required em dashes (`LEDGER:71`) suffice. Recovery needs a hand edit of the ledger (spot-check 4, WRONG).
3. **Its policy footing is thinner than stated.** The Ruling section is "user-authorized, executor-recorded" (`LEDGER:62`, `LEDGER:68`); "Existing operator-written records remain valid" (`QA:256`, also `LEDGER:195`) reads as backward compatibility, not a new route (spot-check 2, OVERSTATED).
4. **It works only when a `halt` record is present.** Clause (a) of `RETRY:498` needs a `halt` after the latest `blocked`; a line written after a transient stop is ignored (`RETRY:500`). Under (a), rows P and H write that `halt` before the executor asks (`LEDGER:155-156`).
5. **It normalises hand-appended Ruling lines.** Eligibility is positional (`RETRY:498`), so a coordinator-appended line looks the same as a person's. V3 forbids that by spec text only.

## Concessions
1. **X-002 goes to V3.** "The remaining tasks leave Orca" is not forced by the rule: once a Ruling and its post-ruling `complete` are in the ledger, a resume Task skips that task (row 1, `LEDGER:153`). I adopt V3's re-dispatch half (WC-6, `SPEC:70`). But my route has no clean stop point: after the Ruling the executor moves on to the next task in the person's session (`QA:248`, "T{i+1}? Yes"), so the person lets it run or interrupts it. V3 avoids that; it is V3's best point.
2. **Day-to-day cost is real.** One context switch per halt, and someone must tell the person (A-008). V2 is genuinely faster for the person.
3. **My paper omitted the resume mechanics** (C-005) and the no-lock precondition (`LEDGER:145`, C-009). The person must not resume before the worker settles; WC-6's rule (`SPEC:70`) should say so.
4. **A-010 applies to me too.** A Ruling line in the ledger proves nothing about who confirmed it; my protection is the channel (the person's own conversation), not the record.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | `QA:254` names "another agent's message"; the coordinator's answer is its `reply` (`CAPS:62`). V2 itself concedes it. |
| A-002 | ACCEPT | Row `QA:248`: `complete` with "**unchanged** non-compliant verdict"; `LEDGER:82` preserves all verdict fields. Holds for every option. |
| A-003 | ACCEPT | "Trust ledger + git history after compaction" (`LEDGER:137`); the per-task table is first-match (`LEDGER:149`). Subject to the single-writer precondition (`LEDGER:145`). |
| A-004 | QUALIFY | True in effect, but the `dispute` halt also needs a person and is reached as `E-HALT-QA` (`RETRY:107`), so it is covered by the same two codes. The spec should say so (see A-011). |
| A-005 | ACCEPT | The coordinator is an Orca coordinator session (`SPEC` non-goal 3, line 316: "an Orca coordinator session"), an LLM agent; this is the premise of the rule. |
| A-006 | QUALIFY | Supported by `QA:274`, `QA:288`, `QA:280`, but no frequency is measured. Rarity lowers (a)'s cost; it does not make the safety argument. |
| A-007 | ACCEPT | `CAPS:62`: the coordinator answers with `orchestration reply --id <msg_id>`. |
| A-008 | ACCEPT | A real gap in all three. Fix for (a): the coordinator, on a `failed` outcome whose contract is `blocked` from `/sc:implement`, must show the person `blocked_question` and the ledger path, and must not retry the plan itself until the person has ruled. |
| A-009 | QUALIFY | (a) needs the person's session to open the worker's worktree. The contract points at the ledger (`SPEC:132`); the spec should require the absolute ledger path and worktree in the blocked contract. Remote workers are out of scope (non-goal 9, `SPEC:322`). |
| A-010 | QUALIFY | True as a record property: eligibility is positional (`RETRY:498`). (a) relies on the channel, not the record: the executor hears the person in the person's own session. (c) has no channel check, so the gap is wider there. |
| A-011 | REJECT | Not out of scope: a dispute writes `halt ... reason=dispute` and stops `E-HALT-QA` (`RETRY:107`), which WC-3's exception already covers. Spec should name it for clarity. |
| A-012 | QUALIFY | Matters for (c), not for (a): under (a), rows P and H write a fresh `halt` before the executor asks (`LEDGER:155-156`), so the recorded Ruling satisfies clause (a) of `RETRY:498`. A transient stop asks no Ruling at all (`QA:250`). |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section layout; no bearing on the decision. |
| S-002 | V3 | Only variant citing the eligibility rule (`RETRY:498`); V1 corrects its gap here. |
| S-003 | V1 | Found the stale `qa.md` anchors; now extended to `SPEC:67,132,319,334`. |
| S-004 | V3 | States its weakness and keeps the option; V2's own Safety section argues against it. |
| S-005 | V3 | Superset of (a) is real; the real choice is (a), (a)+re-dispatch, or (b). |
| S-006 | V3 | Concrete AC-4.1 extension; V1's existing AC-4.1 covers only the halt half. |
| C-001 | V1 | The person's words reach the executor directly in the person's own conversation (`QA:254`). |
| C-002 | V1 | Executor-written line cannot be malformed (`LEDGER:71`, `LEDGER:123`). |
| C-003 | V1 | Only route that gives the full pre-asking explanation (`QA:254`). |
| C-004 | V3 | Rest of the plan returns to Orca; V1 adopts re-dispatch but lacks a clean stop point. |
| C-005 | V1 | Rows P/H re-review and write the `halt` that makes the Ruling eligible; V2 has no resume path. |
| C-006 | equal (V1, V3) | Neither holds a worker session during the human wait. |
| C-007 | V1 | Zero protocol and zero spec change; V3 needs a little spec text, V2 a protocol edit. |
| C-008 | V1 | AC-4.1 exists and checks it (`SPEC:274`); V3's extension is good, V2's cannot see a paraphrase. |
| C-009 | V3 | Names the no-lock precondition (`LEDGER:145`); V1 should state it too. |
| C-010 | V1 | No hand-typed line; V3's claimed behaviour is wrong (`E-LEDGER-CORRUPT`, `LEDGER:123`). |
| C-011 | V1 | Only variant to weigh frequency (`QA:274`, `QA:288`, `QA:280`). |
| C-012 | V1 | Relaxing later is a spec edit; a bad relayed Ruling is a `complete` that resume never revisits (`LEDGER:153`). |
| X-001 | V1 | A relayed Ruling contradicts `QA:254`; V2 concedes it. |
| X-002 | V3 | The rule does not force the plan out of Orca; V1 concedes. |
| X-003 | V1 | WC-3's ask route fits neither condition for a Ruling halt (`SPEC:67`, `IMPL:57-59`). |
| X-004 | V1 | V2 cannot verify origin, so "the person still decides" is unverifiable. |
| A-008 | equal | Gap in all three; coordinator must surface `blocked_question` and the ledger path. |
| A-009 | equal (V1, V3) | Both need the person to reach the worktree; V2 does not. Spec should print the absolute path. |
| A-010 | V1 | Channel check exists in V1 (person's own conversation); V3 has record-only provenance. |
| A-011 | equal | Dispute reaches `E-HALT-QA` (`RETRY:107`) and is covered by every option's routing. |
| A-012 | V1 | V1's resume writes the needed `halt` before asking; V3's line can be silently ignored (`RETRY:500`). |

### Variant 2 Advocate (option (b): relayed Ruling via coordinator `ask`)
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

### Variant 3 Advocate (option (c): person writes the ledger Ruling line, coordinator re-dispatches a resume worker)
# Round 1: Variant 3 advocate (option (c): person writes the Ruling line; coordinator dispatches a resume Task)

Citation key: as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`). Every citation below was re-read in this run.

## Position summary
Keep the Ruling rule word for word, and add one route back into Orca: after the worker ends `failed`, the person either types the operator Ruling line into the ledger or resumes in their own session (V1's route), and the coordinator then dispatches a new resume Task, which ledger row R consumes with no review. I accept the diff analysis's framing (S-005) that this is (a) plus an extra path, not a disjoint option; the claim is that the extra path is worth adding because it needs no protocol change and keeps the rest of the plan unattended.

## Steelman
### Variant 1 (a)
The strongest case for (a): the person gives the Ruling in the very conversation where the executor has just explained "the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong" (`QA:254`). The decision is informed, and the executor formats the line, so there is no typing error to recover from. It needs no change anywhere: WC-3 and the implement row already carry the exception (`SPEC:67`, `SPEC:132`), and it is the spec's recommendation (`SPEC:335`, `SPEC:337`). Halts are rare by design: minors and notes never halt (`QA:274`, `QA:288`) and `E-HALT-QA` needs a confirmed blocker a repair could not close (`QA:280`), so moving one plan's remaining tasks into an attended session is a small, infrequent cost.

### Variant 2 (b)
The strongest case for (b): the person never leaves the coordinator conversation. Orca's `ask` is the designed channel for a blocking worker question (`CAPS:61`), it survives a timeout and resumes by message ID (`CAPS:60`), and no heartbeat is needed while blocked (`CAPS:64`). The person's words are quoted verbatim, and the Ruling line already allows "user confirmation provenance" in `<what>` (`QA:259`). For a person running many workers at once, one answer in one place with no file to open is the least friction of the three.

## Strengths claimed
1. **Same provenance as (a).** The person types the words; no agent message carries them. "another agent's message ... not acceptance" (`QA:254`) stays untouched, and a coordinator-written line is "executor-invented approval", a STOP (`QA:249`). Non-goal 6 holds (`SPEC:319`).
2. **The ledger already names this as the post-halt form.** "after a `halt`, the task gets only operator `Ruling:` lines, the post-ruling `complete` that Resume row R writes, operator-review `blocked` and `halt` records" (`LEDGER:110`). The Halt table accepts a "valid existing operator Ruling" as an alternative to confirmation (`QA:248`), the spec itself lists it as today's second route (`SPEC:334`), and "the user need not hand-write a ledger record" (`QA:254`) implies the user may.
3. **Deterministic consumption.** Row R ("An eligible Ruling with no `complete` after it → Append the post-ruling `complete` ... with no review", `LEDGER:154`) sits before P and H, and "First match wins; the row order is part of the rule" (`LEDGER:149`). Every ladder halt writes a `halt` record (`RETRY:441`), so a line after it is eligible under clause (a) of `RETRY:498`. Diff spot-check 3 confirms this.
4. **The plan stays in Orca.** The resume Task is a new Task (WC-6, `SPEC:70`) whose command line is unchanged because `--resume` is implicit when a ledger matches (`IMPL:57`). This falsifies V1's "the remaining tasks of that plan leave Orca" (X-002).
5. **Cheaper resume than V1's described path.** V1's person resumes with no Ruling yet, so resume falls to row H: a fresh operator review, then `halt ... reason=operator-review` and STOP `E-HALT-QA` (`LEDGER:156`), before the executor can explain and ask. A hand-written line skips that extra reviewer run.
6. **No person wait inside a worker.** The wait sits between Tasks, so no session is held open (contrast `CAPS:64`), and nothing depends on an answer arriving before the worker settles (`SPEC:67`).
7. **Single writer by construction.** The ledger has no lock (`LEDGER:145`); the person writes only after the worker has settled, which WC-6 already requires before any retry (`SPEC:70`).
8. **Checkable live.** Extend AC-4.1 (`SPEC:274`): append a hand-written line after the halt, dispatch the resume Task, expect `complete` with the unchanged non-compliant verdict (`QA:248`, `LEDGER:82`).
9. **Strictly no less safe than (a).** It removes nothing from (a); (a) remains available when the person wants the executor's explanation.

## Weaknesses identified
### Variant 1 (a)
1. **Its main cost claim is wrong.** "the remaining tasks of that plan leave Orca" (V1 line 19) does not follow from the rule: row R plus a resume Task returns them (`LEDGER:154`, `SPEC:70`, X-002). V1 adopts a cost it does not have to pay.
2. **It omits the extra review on its own path.** Resuming with no Ruling hits row H (`LEDGER:156`): one fresh operator review, then a re-halt with `reason=operator-review`, before the executor explains and asks (C-005). V1 says only "resumes from the ledger".

### Variant 2 (b)
1. **It breaks the rule it relies on.** By its own text, "It contradicts the rule as written" (V2 line 13; `QA:254`), so it needs a protocol edit against non-goal 6 (`SPEC:319`), and the worker cannot tell a paraphrase from the person's words (`CAPS:62`; X-004).
2. **It has no resume path.** Any `halt` is terminal (`RETRY:488`) and the command has already stopped. WC-3's ask route is limited to "a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag" (`SPEC:67`); a Ruling halt fails both, and `/sc:implement` has no Ruling flag (`IMPL:6`). "keeps its session, its ledger position and its retry state" (V2 line 8) needs a new route that V2 does not design (X-003).
3. **Uncounted cost.** Asking mid-command either makes the command run an `orca` command, which SA-2 forbids (`SPEC:170`), or needs a redesigned re-invoke route (C-007).

## Concessions
1. **Spot-check 4 (WRONG) is right.** A hand-appended line is the ledger's last line; if malformed (for example hyphens for em dashes, against `LEDGER:71`), resume stops at `E-LEDGER-CORRUPT` (`LEDGER:123`; `SKILL:36`, "No further"), not at row H. It is still a safe stop (ledger "Unchanged", `SKILL:36`), and the fix is one edit to a line the person typed, but my variant said "ignored" and that is wrong. Fix that keeps the rule: the coordinator's brief requires a read-only check of the ledger's last line against `LEDGER:71` and of eligibility (`RETRY:498`) before dispatching the resume Task; on failure it tells the person and never edits the line. This is a coordinator rule, so SA-2 is untouched.
2. **Spot-check 2 (OVERSTATED) is right.** "Existing operator-written records remain valid" (`QA:256`) and "The earlier operator-written form ... remains valid" (`LEDGER:195`) read as backward compatibility, and the section heading is "user-authorized, executor-recorded" (`LEDGER:62`). Restated claim: a newly hand-written line is mechanically valid (`LEDGER:71`, `LEDGER:110`, `RETRY:498`) and permitted by implication (`QA:254`, `QA:248`), but no line explicitly sanctions it as a route. The D2/WC-3 sentence must state it, which is a spec change, not a protocol change.
3. **V1 is better on the informed decision (C-003).** A hand-writer sees only the halt message (ledger path, task, verdict, missing citations, `QA:247`; full list `RETRY:490`), not the executor's scoped explanation (`QA:254`). For a `dispute` halt about the AC itself (`RETRY:107`), (a) is the better route.
4. **Provenance is policy, not mechanism (A-010).** Eligibility is positional (`RETRY:498`); any agent with file access can append a line. This is equally true of every operator-written line today, and V3's "coordinator-written line is invalid" rule is text only.
5. **Not a separate option (S-005).** The real choice is (a) alone, (a)+(c), or (b).

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | `QA:254` lists "another agent's message"; the answer arrives as the coordinator's `reply` (`CAPS:62`) |
| A-002 | ACCEPT | `QA:248` "unchanged non-compliant verdict"; `LEDGER:82` post-ruling `complete` preserves all verdict fields; row R writes it (`LEDGER:154`) |
| A-003 | ACCEPT | "Trust ledger + git history after compaction" (`LEDGER:137`); the per-task table is first-match (`LEDGER:149`) |
| A-004 | QUALIFY | True as codes, but `dispute` is an `E-HALT-QA` reason (`RETRY:107`, `RETRY:441`), so it is inside the set; `E-RESUME-NEEDED` needs a re-run, never a Ruling (`QA:250`) |
| A-005 | ACCEPT | The coordinator is an Orca coordinator session, an agent (`SPEC:316`, `SPEC:334`) |
| A-006 | ACCEPT | `QA:274`, `QA:288`, `QA:280`; rarity also keeps V3's per-halt hand-writing cost small |
| A-007 | ACCEPT | `CAPS:62` |
| A-008 | QUALIFY | A real gap, but the contract carries `blocked_question` (`SPEC:66`) and "the coordinator opens it" (`SPEC:68`); the spec should require the coordinator to show the person the halt text and ledger path. V3 needs this more than V1, since the person writes from the halt text alone |
| A-009 | QUALIFY | Equal for V1 and V3. Placement is the coordinator's explicit `--worktree` choice (`CAPS:116`) and orchestration verbs never delete a worktree (`CAPS:115`), so the ledger survives; remote workers are out of scope (`SPEC:322`). The spec should say the person needs local access to the worker's worktree |
| A-010 | QUALIFY | Eligibility is positional (`RETRY:498`); the person-only rule is policy in every variant, and V3 at least states it (concession 4) |
| A-011 | REJECT | Not out of scope: a dispute writes `halt review=<k> reason=dispute` and STOPs `E-HALT-QA`, "A dispute is the operator's call (Ruling path)" (`RETRY:107`); all variants cover it through `E-HALT-QA`. V1's route is better for it (concession 3) |
| A-012 | QUALIFY | Holds for every `E-HALT-QA`, which always writes a `halt` (`RETRY:441`). Where no `halt` follows a `blocked` but `retry` records exist, the line is ignored with a note (`RETRY:500`) and resume continues by other rows: safe, and caught by the pre-dispatch eligibility check (concession 1) |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section layout only (L1) |
| S-002 | V3 | Only variant citing the eligibility rule (`RETRY:498`) and the resume rows |
| S-003 | V1 | Drift note applies whatever wins; stale anchors also at `SPEC:67,132,319` |
| S-004 | V2 | Most self-critical, though V3's weakness bullet is now extended by concessions 1-3 |
| S-005 | V3 | Superset of (a): adds a route, removes none |
| S-006 | V3 | Gives a concrete AC-4.1 extension with an expected ledger result |
| C-001 | equal (V1, V3) | Both keep the person's own words; V2's arrive as an agent message (`CAPS:62`) |
| C-002 | V1 | Executor-formatted line removes the typing risk; V3 keeps provenance but adds that risk |
| C-003 | V1 | Executor explanation before acceptance (`QA:254`); V3 offers (a) for when it is wanted |
| C-004 | V3 | Remaining tasks return to Orca via row R and a new Task (`LEDGER:154`, `SPEC:70`) |
| C-005 | V3 | Row R before H skips the extra operator review (`LEDGER:149-156`); V2 has no resume path |
| C-006 | V3 | No worker session held during the person's wait |
| C-007 | V1 | Zero spec change; V3 needs one sentence, one AC, one coordinator check; V2 edits the rule |
| C-008 | V3 | Deterministic table-row check; V2's relay fidelity is uncheckable |
| C-009 | V3 | Only variant to state the single-writer precondition (`LEDGER:145`) |
| C-010 | V1 | V3 was wrong (`LEDGER:123`); fixed by the pre-dispatch check, but V1 has no such risk |
| C-011 | V1 | Only variant to argue frequency (`QA:274,280,288`); the argument helps V3 too |
| C-012 | V3 | Adds a route while keeping (a) unchanged; easiest to drop if unused |
| X-001 | equal (V1, V3) | Neither relays; V2 concedes the conflict |
| X-002 | V3 | Rule kept and plan stays in Orca, falsifying V1 line 19 |
| X-003 | equal (V1, V3) | WC-3's ask route does not fit a Ruling halt (`SPEC:67`, `IMPL:6`) |
| X-004 | equal (V1, V3) | V2's internal conflict; V1 and V3 are not party |
| A-008 | V1 | The executor's explanation partly fills the gap; all need a spec rule to surface the halt |
| A-009 | equal | V1 and V3 both need local ledger access |
| A-010 | equal (V1, V3) | Positional eligibility in both; V3 at least states the rule |
| A-011 | V1 | A dispute about the AC is best answered with the executor's explanation |
| A-012 | V3 | Explicit about the eligibility condition and adds a pre-dispatch check |

## Round 2: Rebuttals

### Variant 1 Rebuttal
# Round 2: Variant 1 advocate, D2 option (a), rebuttal

Citation key: as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`). Every citation newly relied on below was re-read in this round.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | (a)'s resume is heavier than stated: with a `halt` and no Ruling, row H runs a fresh operator review and re-halts before the executor can explain and ask | V2 R1 weakness 1; V3 R1 weakness 2 and strength 5; diff C-005 | The cost is real: one reviewer run per halt, and my paper omitted it. But it is the protocol's designed step, not overhead: `operator-review` is "user-initiated after a halt, never started by automation" (`QA:283`), so the person's own resume is exactly its intended trigger. It writes the fresh `halt` that makes the later Ruling eligible (`LEDGER:156`, `RETRY:498` (a)), and if the tree now passes, no Ruling is needed. Row R in (c) skips it and is lighter. | Concede the cost; hold that it is by design |
| 2 | "The remaining tasks of that plan leave Orca" is not forced by the rule | V2 R1 weakness 2; V3 R1 weakness 1; X-002 | Already conceded in R1. Added: (a) alone has no clean stop after the Ruling, because the executor goes on to T{i+1} in the person's session (`QA:248`, "Yes"). A hand-written line plus a resume Task (c) is the clean way back into Orca. | Concede |
| 3 | (a) assumes the person learns of the halt (A-008); (b) tells the person "by construction" | V2 R1 weakness 3 and strength 4 | Gap conceded for (a). But (b)'s "by construction" is also a spec rule: the `question` lands in the coordinator's wait (`CAPS:63`), and so does (a)'s `worker_done` (the same `check --wait --types "worker_done,escalation,question"`); in both, a rule must make the coordinator tell the person. New evidence 1 makes this rule more urgent for (a) and (c): today's spec lets the coordinator simply retry (`SPEC:84`). | Concede gap; hold that it is equally fixable |
| 4 | (a) assumes the person can reach the worker's ledger (A-009); (b) needs no file access | V2 R1 weakness 3 and strength 5 | True. (a) and (c) need the person's session to see the worker's worktree; (b) does not. Mitigation: the blocked contract carries the absolute ledger path and worktree; remote workers are out of scope (`SPEC:322`). | Concede |
| 5 | (a)'s "channel check" is no stronger than (c)'s record or (b)'s relay; all rest on trust | V2 R1 A-010; V3 R1 A-010 | Narrowed: no option's ledger record proves who confirmed it (eligibility is positional, `RETRY:498`). Held: the trust objects differ. (a) trusts the conversation `QA:254` names ("current conversation"), with no agent between person and executor; (c) trusts that only the person wrote to the file; (b) trusts an LLM relay that `QA:254` excludes by name. | Partly concede; hold the ordering |
| 6 | (a) does not address the single writer of the ledger | V2 and V3 R1 per-point C-009 | Correct. No lock (`LEDGER:145`); the person must resume only after the worker has settled, as WC-6 requires for any retry (`SPEC:70`). The spec should say so for (a) too. | Concede |
| 7 | Provenance (C-001) is equal between (a) and (c), not an (a) win | V3 R1 per-point C-001 | In both, the person's own words, not an agent's message, become the Ruling. (a)'s extra value is the explanation, which is C-003. | Concede; C-001 now equal (V1, V3) |
| 8 | Reversibility (C-012) favours (c): it adds a route that is easy to drop | V3 R1 per-point C-012 | My argument was against (b): relaxing later is cheap, restoring trust after a bad relay is not. Adding (c) as a spec sentence is equally cheap to remove. | Concede; C-012 now equal (V1, V3) |

## Updated assessment of other variants

### Variant 2 (b), corrected route
Steelman: V2's R1 route is now mechanically sound and I withdraw two of my R1 points against it. The `ask` happens in the worker session after `/sc:implement` has stopped, where WC-3's ask already lives (`SPEC:67`, owner "Worker session"), so no command runs an `orca` command and SA-2 (`SPEC:170`) holds; my R1 weakness 3 on SA-2 is withdrawn. Continuity comes from row R (`LEDGER:154`), not from "keeping retry state", so the no-resume-path point (C-005, X-003) is answered by a new, named route rather than a misread of the old one. The session checks the line against `LEDGER:71` before appending, so it has no malformed-line risk, and one session writes and then re-invokes, so it is single-writer by construction (`LEDGER:145`). It is opt-in, so without the new brief line it falls back to (a). It needs no file access (A-009), and asks only when a `halt` follows the latest `blocked` (A-012).

What remains is the safety core, which V2 concedes: the reply is the coordinator's message (`CAPS:62`), which `QA:254` excludes; the worker cannot tell quotation from paraphrase (A-005); the message ID proves which message, not who spoke (V2 R1 A-007); the person sees the coordinator's rendering of the explanation (C-003); and AC-4.1 (b) cannot detect a paraphrase (C-008). Worse than V2 says: under (b) the agent that writes the Ruling line is the same session that ran the failing task, acting on another agent's text, which is the case `QA:249` ("executor-invented approval") and `LEDGER:68` ("On clear user confirmation") were written to stop; the edit therefore reaches the gate itself, not one sentence. Net: (b) is now coherent, but it buys speed on a rare event (`QA:274`, `QA:288`) by editing the one human checkpoint. Not recommended now; a credible later opt-in only if the user explicitly accepts relay risk.

### Variant 3 (c)
Steelman: V3 accepted both diff corrections honestly (malformed line gives `E-LEDGER-CORRUPT`, `LEDGER:123`; the policy footing was OVERSTATED) and fixed the first with a coordinator-side, read-only check of the last line against `LEDGER:71` and of eligibility under `RETRY:498` before dispatching the resume Task. That keeps SA-2 intact and turns the typing risk into "tell the person, never edit the line". Row R before P and H is deterministic (`LEDGER:149`, `LEDGER:154`), every ladder halt writes a `halt` record (`RETRY:441`), and the plan returns to Orca with no protocol change. It keeps (a) unchanged as its other branch, and V3 itself concedes (a) is the better route for a `dispute` about the AC (V3 R1 concession 3).

Remaining weaknesses: no executor explanation before the decision (C-003); record-only provenance (A-010); the hand-written route needs an explicit spec sentence because `QA:256` and `LEDGER:195` read as backward compatibility. New evidence 1 below shows the pre-dispatch check is load-bearing, not optional: a resume Task dispatched without an eligible line would start an operator review by automation. My view moves: (c) is a sound addition to (a), not a rival.

## New evidence

1. **An unaided coordinator retry breaks a protocol rule today, under every option.** The spec lets the coordinator answer a `failed` or `blocked` Task by "retries per WC-6, answers per the example below, or reports the failure to the person" (`SPEC:84`). A WC-6 retry of a Ruling-halted implement plan re-runs the same command, `--resume` is implicit (`IMPL:57`), and with no eligible Ruling resume falls to row P or H: "One fresh operator review of the tree as it stands", then `blocked` and a new `halt ... reason=operator-review` (`LEDGER:155-156`). But the closed list of interrupts says `operator-review` is "user-initiated after a halt, never started by automation" (`QA:283`). So the spec must say: after an `/sc:implement` Ruling halt the coordinator must show the person `blocked_question` and the absolute ledger path, and must not dispatch any Task for that plan until the person has acted; under (c), only after the pre-dispatch check finds an eligible Ruling. This closes A-008 for all three options and makes V3's check mandatory.
2. **`E-NO-RULING` writes no `halt`.** Its STOP row reads "Unchanged except existing blocked line" (`SKILL:35`). A Ruling after it is eligible only under clause (b) of `RETRY:498` (no `retry`, no `halt`). Under (a) this needs nothing: row P writes `halt review=2 reason=operator-review` before the executor asks (`LEDGER:155`), so clause (a) holds. Under (c), the pre-dispatch eligibility check must test both clauses, not only "after the halt".
3. **Both outcomes reach the coordinator through the same wait.** `check --wait --types "worker_done,escalation,question"` (`CAPS:63`). (b)'s claim to tell the person "by construction" (A-008) therefore rests on the same kind of coordinator rule as (a) and (c), not on a different mechanism.

## Updated shared assumption responses

| ID | R1 response | R2 response | Reason for change |
|---|---|---|---|
| A-004 | QUALIFY | QUALIFY, extended | Add: `E-NO-RULING` writes no `halt` (`SKILL:35`), so a Ruling after it relies on clause (b) of `RETRY:498`; (a) is safe because row P writes a `halt` first (`LEDGER:155`); (c)'s check must cover clause (b). |
| A-008 | ACCEPT (coordinator must surface the halt) | ACCEPT, extended | The coordinator rule must also forbid any re-dispatch of a Ruling-halted implement plan until the person has acted, because a WC-6 retry (`SPEC:84`) would start `operator-review` by automation, against `QA:283`. |
| A-009 | QUALIFY | ACCEPT | A real cost of (a) and (c) that (b) avoids (V2 R1 strength 5). Mitigation stays: absolute ledger path and worktree in the blocked contract; remote workers out of scope (`SPEC:322`). |
| A-010 | QUALIFY | QUALIFY, narrowed | No option's record proves who confirmed it (`RETRY:498`). I keep only the claim that (a)'s trust object is the conversation `QA:254` names, not that (a) has a mechanical check. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | equal | no | Section layout only. |
| S-002 | V3 | no | Only original citing the eligibility rule (`RETRY:498`) and resume rows. |
| S-003 | V1 | no | Stale `qa.md` anchors at `SPEC:67,132,319,334`; fix whatever wins. |
| S-004 | V2 | yes (was V3) | V2's paper argued against itself most fully, and its R1 concessions confirm it. |
| S-005 | V3 | no | (c) is a superset of (a); the real choice is (a), (a)+(c) or (b). |
| S-006 | V3 | no | Concrete, deterministic AC-4.1 extension. |
| C-001 | equal (V1, V3) | yes (was V1) | Both keep the person's own words; (b)'s arrive as an agent message (`CAPS:62`). |
| C-002 | V1 | no | Executor-formatted line; (c)'s pre-dispatch check reduces, not removes, the typing risk. |
| C-003 | V1 | no | Only (a) gives the executor's own explanation before acceptance (`QA:254`). |
| C-004 | V2 | yes (was V3) | On continuity alone (b) is smoothest: one answer, same worker; (c) needs a line, a message and a new Task. Bought with a rule edit. |
| C-005 | V3 | yes (was V1) | Row R before P/H is deterministic with no reviewer run (`LEDGER:149-154`); (a)'s row H is by design (`QA:283`) but heavier. |
| C-006 | equal (V1, V3) | no | Neither holds a worker session during the human wait. |
| C-007 | V1 | no | Zero protocol and zero spec change for the rule itself. |
| C-008 | V3 | yes (was V1) | V3's extension tests both the halt and the return; keeps (a)'s no-question check. |
| C-009 | equal (V2, V3) | yes (was V3) | (b) single-writer by construction; (c) states the precondition (`LEDGER:145`); (a) must add it. |
| C-010 | equal (V1, V2) | yes (was V1) | Both have an agent format the line; (c)'s hand line can give `E-LEDGER-CORRUPT` (`LEDGER:123`). |
| C-011 | V1 | no | Frequency argument (`QA:274`, `QA:280`, `QA:288`); it also cheapens (c)'s per-halt cost. |
| C-012 | equal (V1, V3) | yes (was V1) | Both keep the rule and are cheap to undo; (b) is the hard one to undo. |
| X-001 | equal (V1, V3) | yes (was V1) | Neither relays; V2 concedes the conflict with `QA:254`. |
| X-002 | V3 | no | The rule does not force the plan out of Orca; conceded. |
| X-003 | equal (V1, V3) | yes (was V1) | Both read `SPEC:67` right; V2 now proposes a new route instead of the old one. |
| X-004 | equal (V1, V3) | yes (was V1) | Not a party; V2's tension stands (it concedes the worker cannot prove origin). |
| A-008 | equal | no | All three need the same coordinator rule (`CAPS:63`); extended by new evidence 1. |
| A-009 | V2 | yes (was equal V1, V3) | (b) needs no access to the worker's files. |
| A-010 | V1 | no (narrowed) | No record proves origin; (a)'s trust object is the conversation `QA:254` names. |
| A-011 | V1 | yes (was equal) | A dispute about the AC (`RETRY:107`) is best decided with the executor's explanation; V3 concedes this. |
| A-012 | V1 | no | Rows P/H write the `halt` before the executor asks (`LEDGER:155-156`); (c) needs its check for both `RETRY:498` clauses. |

## Overall recommendation

Recommend (a)+(c): keep the Ruling rule word for word, keep (a) as the default and the route for a `dispute` about the AC, and add (c) as a second route for a person who has read the halt and wants the rest of the plan back in Orca. The spec should add five things: (1) after an `/sc:implement` Ruling halt the coordinator shows the person `blocked_question`, the absolute ledger path and worktree, and dispatches no Task for that plan until the person has acted, because a plain WC-6 retry would start `operator-review` by automation (`SPEC:84`, `QA:283`); (2) the person writes or resumes only after the worker has settled (`LEDGER:145`, `SPEC:70`); (3) a hand-written Ruling line after a halt is a sanctioned route, and a line written by the coordinator or any worker is "executor-invented approval" (`QA:249`); (4) before a resume Task, the coordinator runs a read-only check of the last line against `LEDGER:71` and of eligibility under both clauses of `RETRY:498`, and on failure tells the person and never edits the ledger; (5) the stale `qa.md` anchors at `SPEC:67,132,319,334` point to `QA:247-249` and `QA:254-256`, and AC-4.1 gains V3's extension. Reject (b) for now: its corrected route works mechanically, but it edits the one human checkpoint to save time on a rare event, and no test can see a bad relay.

### Variant 2 Rebuttal
# Round 2: Variant 2 advocate, D2 option (b), rebuttal

Citation key: as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`). Every citation newly relied on below was re-read in this round.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | (b) breaks the rule it relies on: the reply is the coordinator's message (`CAPS:62`), and "another agent's message" is not acceptance (`QA:254`) | V1 R1 W1; V3 R1 W1; diff X-001, A-001 | No counter-evidence exists. `QA:254` names the case exactly, so (b) needs the rule edited, not reinterpreted. | Concede |
| 2 | "The person still decides" cannot be checked: the worker cannot tell quotation from paraphrase | V1 R1 W1; diff X-004, A-005 | The reply's message ID proves which message, not who spoke it. A bad relay is found only afterwards, if the person compares the ledger line with what they said. | Concede |
| 3 | WC-3's ask route does not fit a Ruling halt (`SPEC:67`: before any output, answer fits a flag) | V1 R1 W2; V3 R1 W2; diff X-003 | Conceded in R1. The corrected (b) is a second, named route: the answer goes into the ledger, then the same command line re-runs and row R consumes it (`LEDGER:154`). V1 R2 accepts that this is mechanically sound. | Concede the original claim; hold the corrected route |
| 4 | "Keeps its retry state" is wrong; asking mid-command breaks SA-2 (`SPEC:170`) | V1 R1 W3; V3 R1 W2-W3; diff C-005, C-007 | Conceded in R1: any `halt` is terminal (`RETRY:488`). The `ask` happens in the worker session after the command has stopped, where WC-3's ask already lives (owner "Worker session", `SPEC:67`). V1 R2 withdrew its SA-2 point. | Concede the original; hold the correction |
| 5 | AC-4.1 (b) cannot detect a paraphrase (`SPEC:274`) | V1 R1 W4; diff C-008 | True. The check compares the ledger line with the coordinator's text, which is all the worker has. No test I can design closes this. | Concede |
| 6 | (b) holds a worker session open through a human wait, and a late answer needs a new Task anyway | V1 R1 W5; diff C-006 | `CAPS:64` removes the heartbeat cost and `CAPS:60` keeps the question across timeouts, but the session is still held. Worse than V1 says: see new evidence 2. A late answer has no defined route under (b). | Concede |
| 7 | The person sees the coordinator's rendering of the explanation `QA:254` requires | diff C-003; V1 R2 | The worker writes the `--question`, but the coordinator controls what the person reads. Only (a) gives the executor's own explanation to the person. | Concede |
| 8 | Under (b) the Ruling is written by the same session that ran the failing task, acting on another agent's text; the edit reaches the gate itself (`QA:249`, `LEDGER:68`) | V1 R2 assessment of (b) | Partly. Writer identity is not new: under (a) too, "The executor MUST automatically append" the Ruling (`QA:256`), and it is the same skill that ran the task. What is new is the input source, which is criticism 1. The edit scope is real: `LEDGER:68` ("On clear user confirmation") and `QA:249` would both change, as my R1 cost list already said. | Hold on writer identity; concede edit scope |
| 9 | (b)'s "tells the person by construction" (A-008) rests on a coordinator rule, like (a) and (c) | V1 R2 response 3, new evidence 3 | Correct. The `question` and the `worker_done` arrive through the same wait (`CAPS:63`). Under (b) a rule must stop the coordinator answering from its own plan. Under (a) and (c) a rule must stop it retrying. Both are text rules. | Concede |
| 10 | (b) buys speed on a rare event by editing the one human checkpoint | V1 R1 strength 7; V1 R2 | Halts need a confirmed blocker that a repair could not close (`QA:280`), and minors never halt (`QA:274`). The benefit of (b) therefore scales with a rare event, and its risk is permanent. A bad relayed Ruling becomes a `complete` that resume skips for good (`LEDGER:153`). | Concede |

## Updated assessment of other variants

### Variant 1 (a)
Steelman, now stronger than in R1: V1 turned the row H review I criticised into a defensible step. `operator-review` is "user-initiated after a halt, never started by automation" (`QA:283`), so the person's own resume is the trigger the protocol intends. It also writes the fresh `halt` that makes the later Ruling eligible under clause (a) of `RETRY:498` (`LEDGER:155-156`). That covers `E-NO-RULING` too, which writes no `halt` (`SKILL:35`). I withdraw my R1 weakness 1 as a defect; it is a cost, and a deliberate one. V1's new evidence 1 is the most important finding of this round: today's spec lets the coordinator answer a `failed` Task with a WC-6 retry (`SPEC:84`), and a retry of a Ruling-halted plan would start `operator-review` by automation, which `QA:283` forbids. V1 conceded X-002, C-004 and A-009 honestly. Remaining weakness: on its own, (a) has no clean stop after the Ruling, so the plan leaves Orca unless (c) is added. V1 now proposes exactly that addition.

### Variant 3 (c)
Steelman: V3 accepted both diff corrections and added a read-only coordinator check of the last line against `LEDGER:71` and of eligibility under `RETRY:498` before the resume Task. That removes the typing-error risk I raised in R1 strength 3 without any agent writing the line. Row R before P and H is deterministic (`LEDGER:149`, `LEDGER:154`). The plan returns to Orca with no protocol change. V3 also keeps (a) unchanged as its other branch. Remaining weaknesses: there is no executor explanation before the decision (C-003), and the hand-written route needs one explicit spec sentence, because `QA:256` reads as backward compatibility. Both are smaller than my rule edit. My R1 point that (c) needs three handoffs stands, but it is a convenience cost on a rare event, not a safety cost. My view moves: (a)+(c) gives most of what (b) offered, without the rule edit.

## New evidence

1. **(b) cannot clarify an unclear answer in the same Task.** `QA:254`: "If confirmation or scope is unclear, ask one targeted question and keep the task blocked." WC-3: "The worker asks at most once per Task" (`SPEC:67`). Under (b), a relayed answer such as "fine, go ahead" is a generic request to continue, which `QA:254` says is not acceptance. The worker cannot ask again. It must report blocked, and the coordinator re-dispatches, which is (c)'s path. (b) would need a second-ask allowance as well, another WC-3 edit I did not count in R1.
2. **A late answer under (b) collapses into (c) with an agent-written line.** "An answer that arrives after the worker has settled is carried by a new Task (WC-6)" (`SPEC:67`). Under (b), that new Task's worker would append the relayed line before re-running the command: the re-dispatch of (c), but with the line written by an agent from another agent's text. So (b)'s continuity gain exists only while the original worker is still waiting in `ask`.
3. **In (b)'s favour, for the record: no automation-started review during the wait.** While the worker is blocked in `ask` its Task is unsettled, and "No retry while the earlier attempt is not settled" (`SPEC:70`). So the problem in V1's new evidence 1 (a WC-6 retry (`SPEC:84`) starting `operator-review` by automation, against `QA:283`) cannot arise under (b) while it waits. Under (a)+(c) the same protection needs V1's proposed coordinator rule. That rule is one sentence, so this advantage is small.
4. **A `dispute` halt should never be relayed.** A dispute writes `halt ... reason=dispute`, stops `E-HALT-QA` and lists the advice file (`RETRY:107`). "a disputed AC is a user decision" (`QA:281`). The person must read that file to decide. Under (b) they would see only the coordinator's summary of it. Any future relay route must exclude `reason=dispute`.

## Updated shared assumption responses

| ID | R1 response | R2 response | Reason for change |
|---|---|---|---|
| A-008 | QUALIFY ((b) closes the gap) | ACCEPT (a gap in all three) | The `question` and the `worker_done` arrive through the same wait (`CAPS:63`). Every option needs a coordinator rule: surface the halt to the person, never answer or retry on its own. Under (a)+(c) the rule must also forbid any Task for the plan until the person has acted (`SPEC:84`, `QA:283`). |
| A-010 | QUALIFY (all rest on trust; (b) riskier) | QUALIFY, narrowed | No record proves origin (`RETRY:498`), but the trust objects are not equal. (a) and (c) trust a channel with no agent between the person and the record. (b) trusts the one channel `QA:254` excludes by name. (b) is the weakest of the three. |
| A-011 | ACCEPT (dispute falls inside the relay route) | QUALIFY | A dispute is inside the Ruling path (`RETRY:107`), but it should be excluded from any relay: the person must read the advice file (new evidence 4, `QA:281`). (a) is the right route for it, as V1 and V3 both say. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | equal | no | Section layout only (L1). |
| S-002 | V3 | no | Only original citing the eligibility rule (`RETRY:498`) and resume rows. |
| S-003 | V1 | no | Stale `qa.md` anchors at `SPEC:67,132,319,334`; fix them whichever option wins. |
| S-004 | V2 | no | V2's paper argued against itself most fully; V1 R2 agrees. |
| S-005 | V3 | no | (c) is a superset of (a); the real choice is (a), (a)+(c) or (b). |
| S-006 | V3 | no | Concrete, deterministic AC-4.1 extension. |
| C-001 | equal (V1, V3) | yes (was V1) | Both keep the person's own words; (b)'s arrive as an agent message (`CAPS:62`). |
| C-002 | V1 | no | Executor-formatted line after the person's own confirmation (`QA:256`). |
| C-003 | V1 | no | Only (a) gives the executor's own explanation before acceptance (`QA:254`). |
| C-004 | V2 | no | On continuity alone (b) is smoothest, but only while the worker is still in `ask` (new evidence 2). |
| C-005 | V3 | no | Row R before P/H is deterministic with no reviewer run (`LEDGER:149-154`). |
| C-006 | equal (V1, V3) | yes (was V3) | Neither holds a worker session during the human wait; (b) does. |
| C-007 | V1 | no | Zero protocol and zero spec change for the rule itself. |
| C-008 | V3 | no | Tests both the halt and the return; (b)'s relay fidelity cannot be tested (`SPEC:274`). |
| C-009 | equal (V2, V3) | yes (was V2) | (b) is single-writer by construction; (c) states the precondition (`LEDGER:145`); (a) must add it. |
| C-010 | equal (V1, V2) | no (clarified) | An agent formats the line in both; (c)'s hand line can give `E-LEDGER-CORRUPT` (`LEDGER:123`), now caught by V3's pre-dispatch check. |
| C-011 | V1 | no | Frequency argument (`QA:274`, `QA:280`, `QA:288`); it shrinks (b)'s benefit most. |
| C-012 | equal (V1, V3) | yes (was V1) | Both keep the rule and are cheap to undo; a bad relayed Ruling is permanent (`LEDGER:153`). |
| X-001 | equal (V1, V3) | yes (was V1) | Neither relays; V2 concedes the conflict with `QA:254`. |
| X-002 | V3 | no | Row R and a resume Task keep the plan in Orca under the unchanged rule. |
| X-003 | equal (V1, V3) | yes (was V1) | Both read `SPEC:67` right; (b) needs a new route, not the old one. |
| X-004 | equal (V1, V3) | yes (was V1) | Not a party; V2's tension stands. |
| A-008 | equal | yes (was V2) | All three need the same coordinator rule (`CAPS:63`). |
| A-009 | V2 | no | (b) needs no access to the worker's files; V1 R2 agrees. |
| A-010 | equal (V1, V3) | yes (was equal, all three) | Neither puts an agent between the person and the record; (b) does. |
| A-011 | V1 | yes (was equal) | A dispute needs the advice file and the executor's explanation (`RETRY:107`, `QA:281`). |
| A-012 | V1 | yes (was V3) | Rows P/H write the `halt` before the executor asks (`LEDGER:155-156`), so eligibility holds by construction, `E-NO-RULING` included (`SKILL:35`). |

## Overall recommendation

As Variant 2's advocate, I withdraw (b) as the recommended answer and support (a)+(c). Keep the Ruling rule word for word. Keep (a) as the default and as the only route for a `dispute` halt. Add (c) as the route back into Orca once the person has written the line. Take V1's five spec additions as written, especially the coordinator rule that dispatches no Task for a Ruling-halted plan until the person has acted (`SPEC:84`, `QA:283`). Add two points from this side. First, the blocked contract must carry the absolute ledger path and worktree, because (a) and (c) need file access that (b) did not (A-009). Second, V3's pre-dispatch check must test both clauses of `RETRY:498`, so a line written after `E-NO-RULING` is handled. The corrected (b) works mechanically, but it edits the one human checkpoint (`QA:254`, `LEDGER:68`, `QA:249`). It also needs a second-ask allowance (new evidence 1) and cannot be tested for relay fidelity (`SPEC:274`). Its gain exists only while a worker waits in `ask`, on an event that is rare by design. Record (b) only as a possible later opt-in, and only if the user explicitly accepts relay risk. Even then it must exclude `reason=dispute`.

### Variant 3 Rebuttal
# Round 2: Variant 3 advocate, D2 option (c), rebuttal

Citation key: as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`). Every citation newly relied on below was re-read in this round.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | (c) skips the executor's scoped explanation before acceptance; the person decides with less in front of them | diff C-003, spot-check 1; V1 R1 W1; V2 R1 W2; V1 R2; V2 R2 | No counter-evidence on substance. It is not a protocol breach: the Halt table accepts "valid existing operator Ruling" as an input with no explanation step (`QA:248`), and the explanation is a precondition of asking only (`QA:254`). Mitigation, not a cure: the coordinator shows the full halt text (`RETRY:490`: ledger path, task, verdict, missing citations, checkpoint shas, briefs) and (a) stays one choice away. | Concede |
| 2 | V3's "a malformed line is ignored and the resume halts again (`LEDGER:156`)" is wrong; a bad last line gives `E-LEDGER-CORRUPT` | diff spot-check 4 (WRONG); V1 R1 W2; V2 R1 W1 | Conceded in R1. `LEDGER:123` checks the last line against the record regexes, and a hand-typed hyphen fails `LEDGER:71`; `SKILL:36` "No further". Fixed by the read-only pre-dispatch check (R1 concession 1). "Ignored" is true only for a well-formed but ineligible line (`RETRY:500`; new evidence 3). | Concede |
| 3 | The policy footing is OVERSTATED: "existing operator-written records remain valid" reads as backward compatibility, so (c) needs protocol wording too | diff spot-check 2; V1 R1 W3; V2 R1 W3; V1 R2; V2 R2 | Partly hold. The ledger grammar names the record kind as current, not legacy: "after a `halt`, the task gets only operator `Ruling:` lines ..." and "Operator `Ruling:` lines may appear between any two records" (`LEDGER:110`); a hand-written line present at resume is "existing" when row R reads it (`QA:248`, `LEDGER:154`). So no edit to `qa.md`, `ledger.md` or `retry.md` is needed. But no line sanctions it as a route, so one spec sentence must. | Concede the spec sentence; hold "no protocol edit" |
| 4 | (c) works only when a `halt` record is present; a line after a transient stop is ignored, and `E-NO-RULING` writes no `halt` | V1 R1 W4; diff A-012; V1 R2 new evidence 2; V2 R2 A-012 | Every `E-HALT-QA` writes a `halt` (`RETRY:441`, `SKILL:33`), so clause (a) of `RETRY:498` holds. After `E-NO-RULING` ("Unchanged except existing blocked line", `SKILL:35`) with no `retry` and no `halt`, clause (b) makes the line eligible and row R still fires. The pre-dispatch check must test both clauses. Under (a), rows P and H write the `halt` first (`LEDGER:155-156`), so eligibility holds by construction. | Concede; A-012 to V1 |
| 5 | Provenance is record-only; (c) normalises hand-appended lines that any agent could write; the ban on a coordinator-written line is text only | V1 R1 W5; V2 R1 W3; diff A-010; V1 R2 | Eligibility is positional (`RETRY:498`) for every option; V1 R2 narrowed its own claim to "trust object", not mechanism. Same exposure exists today for every operator-written line (`LEDGER:195`). New evidence 2 adds a rule that keeps the coordinator from authoring the words. | Partly concede; hold equal (V1, V3) |
| 6 | Three handoffs (person edits, person tells coordinator, coordinator creates a Task) where (b) needs one answer | V2 R1 W4, strength 6; V2 R2 | True. A convenience cost on an event rare by design (`QA:274`, `QA:280`, `QA:288`). On continuity alone (b) is smoother while its worker still waits in `ask`. | Concede; C-004 to V2 |
| 7 | (a) and (c) do not tell the person by construction; (b) does | V2 R1 strength 4 | V2 R2 withdrew it: the `question` and the `worker_done` arrive through the same wait (`CAPS:63`). All three need the same coordinator rule. (c) needs it most, because the person writes from the halt text alone. | Hold equal |
| 8 | (c) needs the person to reach the worker's ledger file; (b) does not | V2 R1 strength 5; V1 R2; V2 R2 | True. Mitigation: the blocked contract carries the absolute ledger path and worktree; remote workers are out of scope (`SPEC:322`). | Concede; A-009 to V2 |
| 9 | The pre-dispatch check is load-bearing: a resume Task with no eligible line would start `operator-review` by automation | V1 R2 new evidence 1 | Correct and sharper than V1 states: an ineligible Ruling is skipped when finding the "Last record" (`LEDGER:141`), so the task falls to row H, whose "Otherwise" branch runs a fresh review (`LEDGER:156`), against "never started by automation" (`QA:283`). Adopt the check as mandatory and the no-dispatch-until-the-person-acts rule (`SPEC:84`). | Concede |
| 10 | A `dispute` halt is better decided under (a) | V1 R2 A-011; V2 R2 new evidence 4 | Agreed in R1 (concession 3). "a disputed AC is a user decision" (`QA:281`), and the right answer may be a plan edit, not a Ruling. Exclude `reason=dispute` from (c): the pre-dispatch check refuses it and points the person to (a). | Concede |
| 11 | The pre-dispatch check reduces but does not remove the typing risk; the executor-written line is better (C-002, C-010) | V1 R2 per-point C-002, C-010 | The check catches format and eligibility, not content: a well-formed line can still name the wrong scope. | Concede; C-010 equal (V1, V2) |
| 12 | (c) is not disjoint from (a) | diff S-005 | Conceded in R1; the choice is (a), (a)+(c) or (b). | Concede |
| 13 | (c) costs spec text; (a) costs none (C-007) | V1 R1, R2 per-point | True for the rule itself. Under every option the spec now needs V1's coordinator rule anyway (`SPEC:84`, `QA:283`), so the gap is one sentence plus one AC. | Concede; V1 keeps C-007 |

## Updated assessment of other variants

### Variant 1 (a)
Steelman, stronger than in R1: V1 turned row H from an omission into a designed step. `operator-review` is "user-initiated after a halt, never started by automation" (`QA:283`), so the person's own resume is its intended trigger; it writes the `halt` that makes the Ruling eligible (`LEDGER:155-156`), `E-NO-RULING` included; and it re-judges the tree as it stands, which protects against the drift in new evidence 1. V1's new evidence 1 is the most important finding of the debate, and it binds (c) more than (a). V1 conceded X-002 and now proposes (a)+(c) itself. Remaining weakness on its own: no clean stop after the Ruling, so the rest of the plan stays in the person's session (`QA:248`, T{i+1} "Yes"). I withdraw my R1 claim that its main cost claim was "wrong": the cost was avoidable, and V1 now avoids it.

### Variant 2 (b)
Steelman: the corrected route is mechanically sound. The `ask` runs in the worker session after the command stopped (`SPEC:67`, owner "Worker session"), so SA-2 holds (`SPEC:170`); continuity comes from row R (`LEDGER:154`); the agent formats the line; it needs no file access; and while it waits, no automated review can start (`SPEC:70`). I withdraw my R1 "no resume path" point (C-005, X-003) against the corrected (b). The safety core stays, and V2 concedes it: the reply is the coordinator's message (`CAPS:62`), which `QA:254` excludes; a paraphrase is undetectable; the person sees the coordinator's rendering of the explanation; one ask per Task (`SPEC:67`) cannot clarify "fine, go ahead" (`QA:254`); and a late answer becomes (c) with an agent-written line. I agree with V2's own withdrawal.

## New evidence

1. **Tree drift between the halt and row R (against my own variant).** Row R appends `complete` "with no review" (`LEDGER:154`), and a Ruling after a halt "accepts the tree as it stands" (`RETRY:500`). In normal use workers may share a worktree (`SPEC:235`). WC-11 (`SPEC:75`) says two workers "must never write the same file", but it is owned by the command and framed around output paths, so it does not clearly stop a later Task from editing the halted task's source files. Under (c) the gap between halt and resume Task includes the person's wait. Another Task can change the halted task's files in that gap, and the person's Ruling then accepts a tree they never saw. (a) does not have this gap: row H re-reviews the tree first (`LEDGER:156`). Fix: at the halt, the coordinator records `git rev-parse HEAD` and `git status --porcelain` for that worktree. The pre-dispatch check compares them, and on any difference routes the person to (a). It dispatches no other writer into that worktree until the resume Task settles.
2. **A coordinator-drafted line turns (c) into (b).** If the coordinator pre-fills `<what>`, `<why>` and `<cost-if-wrong>` and the person only pastes it, the words are another agent's (`QA:254`), and the line approaches "executor-invented approval" (`QA:249`). The coordinator may show only the halt text and the empty skeleton with em dashes (`LEDGER:65`, `LEDGER:68`). The person writes the three fields.
3. **"Ignored" is real only for a well-formed ineligible line.** Such a line is skipped when finding the "Last record" (`LEDGER:141`) and noted as ignored (`RETRY:500`), so resume falls to row H and, absent a person, starts an automated review (`QA:283`). A malformed line stops resume at `E-LEDGER-CORRUPT` (`LEDGER:123`). Both cases need the pre-dispatch check, which must run before every resume Task, not only on suspicion.

## Updated shared assumption responses

| ID | R1 response | R2 response | Reason for change |
|---|---|---|---|
| A-004 | QUALIFY | QUALIFY, extended | `E-NO-RULING` writes no `halt` (`SKILL:35`); a hand line after it is eligible only under clause (b) of `RETRY:498`. The pre-dispatch check tests both clauses. |
| A-008 | QUALIFY | ACCEPT, extended | Same wait for all options (`CAPS:63`). The coordinator shows the person `blocked_question`, the full halt text, the absolute ledger path and the worktree. It dispatches no Task for the plan until the person has acted, because a retry would start `operator-review` by automation (`SPEC:84`, `QA:283`). |
| A-009 | QUALIFY (equal V1, V3) | ACCEPT | A real cost of (a) and (c) that (b) avoids. |
| A-011 | REJECT (in scope) | REJECT, extended | Still in scope (`RETRY:107`), but `reason=dispute` is excluded from (c) and goes to (a) (`QA:281`). |
| A-012 | QUALIFY | ACCEPT | (a) gets eligibility by construction (`LEDGER:155-156`); (c) needs the two-clause check. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | equal | no | Section layout only (L1). |
| S-002 | V3 | no | Only original citing the eligibility rule (`RETRY:498`) and resume rows. |
| S-003 | V1 | no | Stale `qa.md` anchors at `SPEC:67,132,319,334`; fix whichever wins. |
| S-004 | V2 | no | V2's paper argued against itself most fully. |
| S-005 | V3 | no | (c) is a superset of (a); the choice is (a), (a)+(c) or (b). |
| S-006 | V3 | no | Concrete, deterministic AC-4.1 extension. |
| C-001 | equal (V1, V3) | no | Both keep the person's own words; (b)'s arrive as an agent message (`CAPS:62`). |
| C-002 | V1 | no | Executor-formatted line; the pre-dispatch check reduces, not removes, the typing risk. |
| C-003 | V1 | no | Only (a) gives the executor's own explanation before acceptance (`QA:254`). |
| C-004 | V2 | yes (was V3) | On continuity alone (b) is smoothest while its worker waits; bought with a rule edit. |
| C-005 | V3 | no | Row R before P/H completes the task with no reviewer run (`LEDGER:149-154`). |
| C-006 | equal (V1, V3) | yes (was V3) | Neither holds a worker session during the person's wait. |
| C-007 | V1 | no | No spec text for the rule itself; (c) adds one sentence and one AC. |
| C-008 | V3 | no | Deterministic check of both halt and return; relay fidelity is untestable. |
| C-009 | equal (V2, V3) | yes (was V3) | Corrected (b) is single-writer by construction; (c) states the precondition (`LEDGER:145`). |
| C-010 | equal (V1, V2) | yes (was V1) | An agent formats the line; (c)'s hand line can give `E-LEDGER-CORRUPT` (`LEDGER:123`). |
| C-011 | V1 | no | Frequency argument (`QA:274`, `QA:280`, `QA:288`). |
| C-012 | equal (V1, V3) | yes (was V3) | Both keep the rule and are cheap to undo; a bad relayed Ruling is permanent (`LEDGER:153`). |
| X-001 | equal (V1, V3) | no | Neither relays; V2 concedes the conflict with `QA:254`. |
| X-002 | V3 | no | Row R and a resume Task keep the plan in Orca under the unchanged rule. |
| X-003 | equal (V1, V3) | no | Both read `SPEC:67` right; (b) needs a new route. |
| X-004 | equal (V1, V3) | no | Not a party; V2's tension stands. |
| A-008 | equal | yes (was V1) | Same coordinator rule for all three (`CAPS:63`, `SPEC:84`). |
| A-009 | V2 | yes (was equal) | (b) needs no access to the worker's files. |
| A-010 | equal (V1, V3) | no | No agent between the person and the record; no record proves origin (`RETRY:498`). |
| A-011 | V1 | no | A dispute needs the advice file and the executor's explanation (`QA:281`, `RETRY:107`). |
| A-012 | V1 | yes (was V3) | Rows P/H write the `halt` before asking (`LEDGER:155-156`); (c) needs the two-clause check. |

## Overall recommendation

Recommend (a)+(c), the same as V1 R2 and V2 R2: keep the Ruling rule word for word, keep (a) as the default and as the only route for `reason=dispute`, and add (c) as the way back into Orca. (c) is safe only with its guards, and Round 2 showed they are load-bearing. (1) After any `/sc:implement` Ruling halt the coordinator shows the person `blocked_question`, the full halt text, the absolute ledger path and the worktree, and dispatches no Task for that plan until the person has acted (`SPEC:84`, `QA:283`). (2) The person writes only after the worker has settled (`LEDGER:145`, `SPEC:70`), filling the empty em-dash skeleton themselves. A line drafted by the coordinator, or written by any agent, is "executor-invented approval" (`QA:249`). (3) Before every resume Task, the coordinator runs a read-only check: the last line matches `LEDGER:71`; the line is eligible under either clause of `RETRY:498`; the halt reason is not `dispute`; and the worktree's HEAD and status are unchanged since the halt. On any failure it tells the person, routes them to (a) and never edits the ledger. (4) Fix the stale `qa.md` anchors (`SPEC:67,132,319,334`) and extend AC-4.1 with the hand-written-line and resume-Task check. Reject (b) for now; its own advocate has withdrawn it.

## Round 2.5: Invariant Probe

Full findings: `invariant-probe.md` (independent fault-finder, not an advocate). Claim under test: "the (a)+(c) consensus alone gives a safe and working Ruling path". Result: 23 findings; 8 ADDRESSED, 15 UNADDRESSED (HIGH 6, MEDIUM 8, LOW 1).

| ID | Severity | Status | One-line summary (from `invariant-probe.md`) |
|----|----------|--------|-----------------------------------------------|
| INV-001 | HIGH | UNADDRESSED | Tree drift between the halt and the (c) resume Task; row R completes "with no review" (`LEDGER:154`) a tree the person never saw |
| INV-004 | HIGH | UNADDRESSED | No defined hand-back after route (a); the person-to-coordinator single-writer direction is unguarded (`LEDGER:145`) |
| INV-014 | HIGH | UNADDRESSED | An unfilled skeleton or whitespace fields pass `LEDGER:71` and become a no-review Ruling |
| INV-017 | HIGH | UNADDRESSED | WC-6's new report directory changes an inline-prompt ledger slug (`SKILL:61`), so the resume Task never reads the Ruling |
| INV-018 | HIGH | UNADDRESSED | Resume Task placement is not tied to the halted Task's worktree (`SPEC:79`, `LEDGER:3`) |
| INV-022 | HIGH | UNADDRESSED | Row R bypasses the row-H review the protocol relies on for `no-evidence` and resume-time revert-guard halts (`RETRY:229`, `RETRY:492`) |
| INV-002 | MEDIUM | UNADDRESSED | The coordinator's "no Task for that plan" freeze is not durable across compaction or restart |
| INV-005 | MEDIUM | UNADDRESSED | The contract carries no STOP code to tell a Ruling halt from `E-RESUME-NEEDED` or `E-LEDGER-CORRUPT` |
| INV-006 | MEDIUM | UNADDRESSED | The pre-dispatch check does not bind the Ruling's `T<id>` to the halted task |
| INV-007 | MEDIUM | UNADDRESSED | The `dispute` exclusion tests only the latest halt and is bypassed after an (a) operator review |
| INV-012 | MEDIUM | UNADDRESSED | Multiple appended lines, blank last line, CRLF or missing final newline are not covered by a last-line check |
| INV-019 | MEDIUM | UNADDRESSED | Under (a), a person running from another checkout gets a different legacy slug (`SKILL:64`) |
| INV-020 | MEDIUM | UNADDRESSED | V3's HEAD/porcelain drift guard always refuses on managed ledgers and stalls parallel Tasks |
| INV-023 | MEDIUM | UNADDRESSED | Managed FINAL may return `issues` → `E-ARCHIVE-BLOCKED` for a vague hand-written scope; not covered by the freeze |
| INV-011 | LOW | UNADDRESSED | A brief carrying `--force` re-halts `E-NO-RULING` on every resume Task (`SKILL:50-51`) |

## Round 3: Final Arguments

Not executed. Depth is standard (maximum 2 debate rounds); Round 3 runs only at depth deep.

## Scoring Matrix

Positions are the Round 2 "Final per-point positions" of the V1, V2 and V3 advocates, in that order. The Agreed column names the advocates whose position changed between Round 1 and Round 2.

| Diff Point | Level | V1 / V2 / V3 advocate (Round 2) | Agreed | Winner | Confidence | Evidence Summary |
|------------|-------|----------------------------------|--------|--------|------------|------------------|
| S-001 | L1 | equal / equal / equal | yes (unanimous) | equal | 95% | Section layout differs only in one extra section; no advocate claimed a substantive advantage. |
| S-002 | L2 | V3 / V3 / V3 | yes (unanimous) | V3 | 95% | V3 is the only original that cites the eligibility rule (`RETRY:498`) and the resume rows. |
| S-003 | L1 | V1 / V1 / V1 | yes (unanimous) | V1 | 95% | V1 alone caught the stale `qa.md` anchors; all three agree they must be fixed whichever option wins. |
| S-004 | L2 | V2 / V2 / V2 | yes (unanimous; V1 changed from V3) | V2 | 92% | V2's paper argued against its own option most fully, and its Round 1-2 concessions confirm it. |
| S-005 | L2 | V3 / V3 / V3 | yes (unanimous) | V3 | 95% | (c) is a superset of (a), so the real choice is (a), (a)+(c) or (b). |
| S-006 | L2 | V3 / V3 / V3 | yes (unanimous) | V3 | 95% | V3 alone proposes a concrete, deterministic AC-4.1 extension. |
| C-001 | L3 | equal (V1, V3) ×3 | yes (unanimous; V1, V2 changed from V1) | equal (V1, V3) | 95% | Both keep the person's own words; (b)'s arrive as the coordinator's message (`CAPS:62`), which V2 conceded (R2 responses 1-2). |
| C-002 | L3 | V1 / V1 / V1 | yes (unanimous) | V1 | 98% | The executor formats the line after the person's own confirmation (`QA:256`); V3 conceded its check reduces but does not remove typing risk (R2 response 11). |
| C-003 | L2 | V1 / V1 / V1 | yes (unanimous) | V1 | 98% | Only (a) gives the executor's own scoped explanation before acceptance (`QA:254`); V2 (R2 response 7) and V3 (R2 response 1) conceded. |
| C-004 | L2 | V2 / V2 / V2 | yes (unanimous; V1, V3 changed from V3) | V2 | 95% | On continuity alone (b) is smoothest while its worker waits in `ask`; V3 conceded (R2 response 6), and all note it is bought with a rule edit. |
| C-005 | L3 | V3 / V3 / V3 | yes (unanimous; V1 changed from V1) | V3 | 95% | Row R precedes P and H and completes the task with no reviewer run (`LEDGER:149-154`); V1 conceded the extra row-H cost (R2 response 1). |
| C-006 | L3 | equal (V1, V3) ×3 | yes (unanimous; V2, V3 changed from V3) | equal (V1, V3) | 95% | Neither (a) nor (c) holds a worker session through the human wait; V2 conceded its held session (R2 response 6). |
| C-007 | L2 | V1 / V1 / V1 | yes (unanimous) | V1 | 98% | (a) needs no protocol or spec text for the rule itself; V3 conceded (R2 response 13). |
| C-008 | L2 | V3 / V3 / V3 | yes (unanimous; V1 changed from V1) | V3 | 95% | V3's AC-4.1 extension tests both the halt and the return; V2 conceded relay fidelity is untestable (R2 response 5). |
| C-009 | L3 | equal (V2, V3) ×3 | yes (unanimous; all three changed) | equal (V2, V3) | 95% | Corrected (b) is single-writer by construction and (c) states the no-lock precondition (`LEDGER:145`); V1 conceded (a) must add it (R2 response 6). |
| C-010 | L3 | equal (V1, V2) ×3 | yes (unanimous; all three changed: V1, V3 from V1, V2 from equal) | equal (V1, V2) | 95% | An agent formats the line in (a) and (b); (c)'s hand line can stop resume at `E-LEDGER-CORRUPT` (`LEDGER:123`); V3 conceded (R2 response 11). |
| C-011 | L2 | V1 / V1 / V1 | yes (unanimous) | V1 | 98% | Halts are rare by design (`QA:274`, `QA:280`, `QA:288`); V2 conceded this shrinks (b)'s benefit (R2 response 10). |
| C-012 | L2 | equal (V1, V3) ×3 | yes (unanimous; all three changed) | equal (V1, V3) | 95% | Both keep the rule and are cheap to undo; a bad relayed Ruling is permanent (`LEDGER:153`), conceded by V2 (R2 response 10). |
| X-001 | L3 | equal (V1, V3) ×3 | yes (unanimous; V1, V2 changed from V1) | equal (V1, V3) | 95% | Neither relays; `QA:254` excludes "another agent's message", and V2 conceded the conflict (R2 response 1). |
| X-002 | L3 | V3 / V3 / V3 | yes (unanimous) | V3 | 98% | Row R plus a resume Task keeps the plan in Orca under the unchanged rule; V1 conceded (R2 response 2). |
| X-003 | L3 | equal (V1, V3) ×3 | yes (unanimous; V1, V2 changed from V1) | equal (V1, V3) | 95% | Both read `SPEC:67` correctly: the ask route needs a gate before any output whose answer fits a flag; V2 conceded (R2 response 3). |
| X-004 | L3 | equal (V1, V3) ×3 | yes (unanimous; V1, V2 changed from V1) | equal (V1, V3) | 95% | Neither is a party; V2's internal tension stands and V2 conceded the worker cannot prove origin (R2 response 2). |
| A-008 | L2 | equal / equal / equal | yes (unanimous; V2, V3 changed) | equal | 95% | All three options need the same coordinator rule to surface the halt, since `question` and `worker_done` share one wait (`CAPS:63`); V2 conceded (R2 response 9). |
| A-009 | L3 | V2 / V2 / V2 | yes (unanimous; V1, V3 changed from equal) | V2 | 95% | (b) needs no access to the worker's files; V1 (R2 response 4) and V3 (R2 response 8) conceded. |
| A-010 | L3 | V1 / equal (V1, V3) / equal (V1, V3) | yes (majority 2/3; V2 changed from equal) | equal (V1, V3) | 70% | No record proves who wrote it (`RETRY:498`); V2 and V3 hold that neither (a) nor (c) puts an agent between person and record, while V1 holds (a)'s trust object is the conversation `QA:254` names. |
| A-011 | L3 | V1 / V1 / V1 | yes (unanimous; V1, V2 changed from equal) | V1 | 95% | A `dispute` needs the advice file and the executor's explanation (`QA:281`, `RETRY:107`); V3 conceded (R2 response 10). |
| A-012 | L3 | V1 / V1 / V1 | yes (unanimous; V2, V3 changed from V3) | V1 | 95% | Rows P and H write the `halt` before the executor asks (`LEDGER:155-156`), so eligibility holds by construction; V3 conceded (R2 response 4). |

Win tally (used by the Step 3 tiebreaker): outright wins V1 7 (S-003, C-002, C-003, C-007, C-011, A-011, A-012), V2 3 (S-004, C-004, A-009), V3 6 (S-002, S-005, S-006, C-005, C-008, X-002). Shared "equal (…)" wins: V1 8 (C-001, C-006, C-010, C-012, X-001, X-003, X-004, A-010), V2 2 (C-009, C-010), V3 8 (C-001, C-006, C-009, C-012, X-001, X-003, X-004, A-010). Unnamed "equal": S-001, A-008.

## Convergence Assessment
- Points resolved: 27 of 27 (26 unanimous, 1 majority: A-010)
- Alignment: 100% (27/27)
- Threshold: 80%
- Round-over-round record: Round 1 agreement 24/27 = 88.9% (split: A-008, A-009, A-010); Round 2 agreement 27/27 = 100%. Agreement was at or above threshold in both rounds (stable majority over 2 rounds). Several winners moved between rounds (for example C-004, C-005, C-009, X-001, A-011, A-012), but every moved point resolved in Round 2, so no oscillation flag applies. The debate ended at the standard-depth maximum of 2 rounds.
- Taxonomy coverage (27 debated points; all addressed in Round 2 final positions):

  | Level | Points | Count | Covered |
  |-------|--------|-------|---------|
  | L1 surface | S-001, S-003 | 2 | yes |
  | L2 structural | S-002, S-004, S-005, S-006, C-003, C-004, C-007, C-008, C-011, C-012, A-008 | 11 | yes |
  | L3 state-mechanics | C-001, C-002, C-005, C-006, C-009, C-010, X-001, X-002, X-003, X-004, A-009, A-010, A-011, A-012 | 14 | yes |

  All three levels have more than zero points addressed, so the taxonomy gate passes and no forced round is needed.
- Invariant gate (Round 2.5, `invariant-probe.md`): HIGH + UNADDRESSED count = 6: INV-001, INV-004, INV-014, INV-017, INV-018, INV-022.

  ```
  CONVERGENCE BLOCKED: 6 HIGH-severity UNADDRESSED invariant(s) detected
  Blocking items: INV-001, INV-004, INV-014, INV-017, INV-018, INV-022
  These invariant violations must be resolved before convergence can be declared.
  Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
  ```

  ```
  WARNING: 8 MEDIUM-severity UNADDRESSED invariant(s) detected
  Items: INV-002, INV-005, INV-006, INV-007, INV-012, INV-019, INV-020, INV-023
  These items do not block convergence but should be reviewed.
  ```

  LOW UNADDRESSED (no action required by the gate, carried into the refactor plan): INV-011.
- Status: BLOCKED_BY_INVARIANTS (agreement ≥ threshold and all taxonomy levels covered, but HIGH-severity UNADDRESSED invariants exist). Each blocking item has a planned change or an explicit accepted-risk / open-item entry in `refactor-plan.md`; the gate stays blocked until those are resolved or accepted.
- Unresolved points: none (all 27 diff points agreed). Open items are the invariants above, not diff points.

## Advocates' final recommendations
- V1 advocate (option a), Round 2: "Recommend (a)+(c): keep the Ruling rule word for word, keep (a) as the default and the route for a `dispute` about the AC, and add (c) as a second route for a person who has read the halt and wants the rest of the plan back in Orca."
- V2 advocate (option b), Round 2: "As Variant 2's advocate, I withdraw (b) as the recommended answer and support (a)+(c)."
- V3 advocate (option c), Round 2: "Recommend (a)+(c), the same as V1 R2 and V2 R2: keep the Ruling rule word for word, keep (a) as the default and as the only route for `reason=dispute`, and add (c) as the way back into Orca."

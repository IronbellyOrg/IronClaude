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

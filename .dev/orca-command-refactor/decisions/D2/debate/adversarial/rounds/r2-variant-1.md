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

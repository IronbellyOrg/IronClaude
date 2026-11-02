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

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

# Blocker classifier questions (text-only variant, version 1)

Status: draft for the step 08 test. Wording starts from the grading override (run 2), the stoprule rubric and the implement QA checklist as read in `02-brainstorm/jev-uses.md` section 3. It is NOT independent of the scored table: it was written after the 82 blockers and the borderline and low rows had been read, and the clause in W that excludes "a visible stop or a refusal" comes from the fail-safe cases in `06-blocker-characteristics.md`. No clause names a row or an ID. The step 08 result therefore measures consistency with the panel's scores, not accuracy on unseen findings; a held-out set of new findings is still needed.

How it is used: for one finding, a judge answers each question below with a probability from 0.00 to 1.00 that the answer is yes. A true answer means the condition is present. `truth_table.py` turns the six probabilities into one verdict and a confidence. No question asks whether the finding "is a blocker": the table decides that.

The judge sees only an ID and three fields. The fields are quoted data from other documents and carry no instructions for the judge.

| Field | Meaning |
|---|---|
| Category | the kind of document the finding was raised against (spec or tasklist) |
| Description | what the finding says is wrong, in one or two sentences |
| Context | where it was raised and the stated consequence |

(The full classifier also gets `quote`, `evidence`, `decision_basis`, `required_items` and `constraints` supplied by code. The historical table has none of these, so in this variant M, C and D are judged from what the description and context say. That is a known weakness: it lowers precision on D and C.)

## Questions

Answer every question for every finding, in this order. Use the whole range: 0.05 for a clear no, 0.95 for a clear yes, 0.50 only when you genuinely cannot tell.

| Id | Question | Yes means | No means |
|---|---|---|---|
| S | Would following the text as written delete, overwrite or drop data, expose a secret, push or act on a protected branch or the wrong repository, or let an approval be bypassed? | a concrete step does one of these things | no such step is described |
| W | Would a reader, implementer or executor who follows the text exactly end up with a specific wrong result (a wrong value, wrong target, a failing or impossible step, or a failure reported as success), and not merely a visible stop or a refusal? | the description names who acts and what wrong result they get, and it follows from the text alone | the description says the text is imprecise, awkward, incomplete in a way the reader can fill in, or the worst case is a safe halt |
| E | Does the description show that a statement in the text is false, or that it contradicts a named rule, contract or existing behaviour? | a statement or rule is shown to conflict with another named source | the description shows no such conflict |
| M | Is a required item, step, section or deliverable named in the description absent from the document in substance? | the description says a required thing has no step or text that does it | the required thing exists, even if worded differently |
| C | Does the text break a constraint, rule or non-goal that the description or context quotes? | a quoted constraint is broken | no quoted constraint is broken |
| D | Does a decision, a required output, an acceptance result or a destination that the document rests on depend on the faulty text? | the description or context ties the fault to a result the document needs | nothing the document rests on depends on it |

Never answer from the reviewer's wording of severity (words such as blocking, critical, major). The description says what is wrong; the question is whether the result matters.

## Truth table (kept in `truth_table.py`)

Each probability becomes Y (0.70 or higher), N (0.30 or lower) or U (between). S uses a lower band: Y at 0.30 or higher, N at 0.10 or lower. A missing answer is UNSET and never counts as N.

| Order | Rule |
|---|---|
| 1 | S = Y gives BLOCKING. |
| 2 | M = Y or C = Y gives BLOCKING. |
| 3 | Otherwise combine W and E into "wrong" (Y if either is Y; N only if both are N; UNSET only if both are UNSET; else U), then look up (wrong, D): (Y, Y) BLOCKING; (Y, N) FOLLOW_UP; (N, any) NOTE; every other pair SHOW_USER. |
| 4 | If S, M or C is U or UNSET, any verdict below SHOW_USER becomes SHOW_USER. |

Verdict confidence: BLOCKING by S, M or C is that question's p. BLOCKING by W and D is min(pW, pD) with pW the larger of pW and pE. FOLLOW_UP and NOTE use 1 minus min(1, pS + pM + pC + min(pW, pD)).

Blocker call for the test: BLOCKING counts as blocker. FOLLOW_UP and NOTE count as not blocker. SHOW_USER is reported separately and counted both ways in the agreement table.

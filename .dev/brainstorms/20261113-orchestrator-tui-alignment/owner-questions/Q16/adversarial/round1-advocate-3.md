# Round 1 advocate statement: Variant 3 (security persona)

Debate: Q16, sc:adversarial Mode A, depth quick, Round 1.
Advocate: Variant 3 (proposal C, "one vocabulary and one audit record, separate mechanisms").
Persona: security (vulnerabilities, attack surface, trust boundaries).
Files read: the three variants, diff-analysis.md, question.md, and the cited lines of merged-requirements.md (below "spec") and alignment-findings-adjudicated.md (below "ADJ").

## Position summary

From a security view, the question is where the trust boundaries sit. The three consumers sit behind three different boundaries, and the spec itself already treats them differently:

- The observer (#409) is read-only on one host. The v2 first release (V2-04) "reads only what the same OS user on the same host can read" (spec line 401).
- The Coder#477 listener crosses workspaces. Its deferred build (CO-03, spec line 355) must test "stale registration, name reuse, spoofed identity, credential leakage, read-credential escalation, consumed state, version skew, untrusted content, bypass by default", and cross-workspace reads need "a written read-permission model". The trust-boundary row TB-REMOTE (spec line 636) adds that identity "comes from Coder keyed by workspace id, never by name".
- The watcher's trust is "a different, local model" by V3's own account (ADJ line 809).

One mechanism for all three either gets sized for the strongest threat (the listener) and is overbuilt for a read-only local observer, or gets sized for the weakest and under-protects the listener. Variant 3 avoids that choice. It promises only what can safely be shared: the names for who may do what, and one audit record shape. Each consumer still meets its own threat model. It also keeps the poisoned-content problem as its own rule ("relayed text stays data, V2-04"), which matches the spec's own statement that "signing does not stop poisoned content" (spec line 407; ADJ line 295).

Variant 3 is the spec's recommended answer (spec line 543; ADJ line 382, X-005 at 66 percent). It is also the only variant that fixes a sentence in #409, "Decide one design, not two.", that both the debate and review 04 judged an over-promise.

## Steelman of Variant 1

Strongest version: no trust layer, grant format, signing scheme or relay exists today (question.md fact 6; spec line 129: Phase 4 trust layer is "later phases"). Any trust promise written now is a promise about a system nobody has designed. In security work a premature public commitment is a real hazard, because later designers inherit it as a constraint and may bend a threat model to fit the words. Variant 1 makes no such commitment. It lets OB-08, V2-01 and the CO-01 post go ahead minus one clause (Variant 1, "What it unlocks"). It also re-asks the question when SW-12 Phase 4 is opened, so the owner chooses with a real design in view (U-001). That is the honest "we do not know yet" answer, and the question was judged "not decidable from sources" (ADJ line 809).

What it gets right: it correctly sees that the vocabulary's terms and the audit fields cannot be written now under any variant. Re-asking at Phase 4 is a good checkpoint that the other variants lack.

Critique: Variant 1 does not stay neutral. It leaves "Decide one design, not two." standing in #409 (Variant 1, step 2). That sentence is itself a trust promise, the broadest one on the table. Variant 1 admits this: "Readers of #409 may keep designing toward one shared design" (Variant 1, "Costs"). So the default does not promise nothing; it keeps Variant 2's promise in one issue while dropping it in two others. That is an inconsistent trust story across three public issues, which is worse for reviewers than either consistent choice. It also holds V2-03, V2-04, OB-09 and SW-12 Phase 4 (Variant 1, step 4), and Variant 1 concedes the question "returns at a worse time, when more text may rest on the old sentence".

## Steelman of Variant 2

Strongest version: in security, every extra mechanism is extra attack surface and extra review load. Three trust mechanisms means three signing or check paths to audit, three places for a bypass bug, and three sets of keys or credentials to handle. One design, owned in one place (#339's trust layer), with a bar on any second format (review 03's Edit 7, U-002), is the classic way to keep the trusted computing base small. It also removes the need for a translation layer if v2 later relays to agents or a remote listener appears (Variant 2, "What it unlocks"). Many real systems fail at the seams between security models, and Variant 2 has no seams.

What it gets right: the single-owner rule is a real security property. "No other issue may invent a second format" stops quiet, unreviewed trust code from appearing in Coder#477 or #423. Variant 3 should keep a version of this rule: one owner for the vocabulary and audit format.

Critique: Variant 2 states its own fatal weakness. "A shared design tends toward signing ... signing does not stop poisoned content, so one design could give a false sense of safety for relayed text" (Variant 2, "Costs"; ADJ line 295; #339 comment 2: "encryption alone is not enough"). A false sense of safety is a vulnerability in its own right: people grant more because the system looks stronger than it is. Variant 2 also commits three issues to a design that "does not exist yet" (Variant 2, "Costs"). Its "What stays unresolved" admits that signing, key handling and scopes are unspecified. So it bars a second format before the first one has any content. Last, the "small trusted base" argument assumes the three consumers need the same guarantees. The spec says otherwise: the listener needs identity keyed by workspace id and a written read-permission model (spec lines 355 and 636). The observer needs none of that.

## Strengths claimed

1. **It matches each trust boundary to its own threat model.** Variant 3: "Each consumer keeps the trust mechanism its own threat model needs" and "without forcing signing everywhere" (Variant 3, "Answer" and "What it unlocks"). The evidence above (spec lines 355, 401, 636; ADJ line 809) shows the three boundaries really differ.
2. **It does not overclaim.** It removes the one sentence ("Decide one design, not two.") that promises more than anyone can deliver now (Variant 3, step 2; spec line 456, XC-08 (2); ADJ line 567, V4 edit 1). In a security document, removing an overclaim is a fix, not a cosmetic edit.
3. **It keeps poisoned content as a separate control.** Variant 3 names "relayed text stays data, V2-04" as its own rule. This matches the spec: V2-04 requires "relayed knowledge as a pinned set of typed fields with free text only in `detail`, checked by a test" (spec line 401), and TB-RELAY says "relayed content is typed data, free text only in `detail`" (spec line 637). A grant design cannot replace that control, and Variant 3 does not pretend it can.
4. **One audit format gives cross-program detection.** "One audit format means a person can still read grants from all three programs side by side" (Variant 3, U-003). For incident review this is the part that matters most: when something goes wrong across the observer, v2 and the listener, one record shape lets one reviewer trace it. The listener's own criteria already expect audit events: "a status read may append a read-audit event" (spec line 355, CO-03 (5)). OB-09 requires "every answer path is audited in the vocabulary of XC-08" (spec line 257).
5. **It has a stated limit.** "Q16's vocabulary does not authorize relay" (spec line 574; Variant 3, "Costs"). A promise with an explicit boundary is safer than an open one.
6. **It settles every gated clause now** (OB-08 decision 6, V2-01, CO-01; Variant 3, "What it unlocks"), and the cost of the commitment is small because it binds words and a record shape, not code.

## Weaknesses identified in others

Variant 1:
- Leaves the broadest promise standing in #409 while the other two issues say nothing, so the public trust story is inconsistent across three issues (Variant 1, steps 2 and 3).
- Does not address poisoned content at all (diff-analysis C-005: "Not addressed").
- Holds V2-03, V2-04, OB-09 and SW-12 Phase 4 with no date; the risk it names ("more text may rest on the old sentence") grows while it waits.

Variant 2:
- Admitted false sense of safety for relayed text (Variant 2, "Costs").
- Forces the cross-workspace listener and the read-only local observer under one mechanism, against the spec's different boundary rows (spec lines 355, 401, 636).
- Bars a second format before the first has any content; Edit 7 then binds Coder#477, a different repository, to a design in #339 that does not exist (Variant 2, "What stays unresolved").
- Ignores the watcher, whose trust is "a different, local model" (ADJ line 809), which fits one design worst of all.

## Concessions

- **Three mechanisms mean three things to review.** Variant 3 says so: "Three mechanisms to build and review instead of one, and a risk that they drift apart beneath shared words" (Variant 3, "Costs"). This is real attack surface, and Variant 2's single design is better on this one axis.
- **Shared words can hide weaker protection.** Variant 3's own risk: "the same word ('grant', 'read') may mean weaker protection in one program than in another". From a security view this is the most serious weakness of my variant. A reviewer who sees "grant: read" in the shared audit format may assume the listener's read check is as strong as some other program's. For the promise to be safe, the vocabulary (when SW-12 Phase 4 defines it) would need to state, per consumer, what each term actually enforces. Variant 3 does not say this.
- **One shared audit format is also a shared injection target.** Audit records that carry strings from issues, sessions or the other program are untrusted input (TB-UNTRUSTED, spec line 632; TB-RELAY, spec line 637). A shared format must be re-sanitised by every reader. Variant 3 does not mention this.
- **The word "grant" is already used in the spec** for owner-ledger rows, `GRANT(<item>,<action>)` (spec lines 61, 961). A second, runtime meaning of "grant vocabulary" invites confusion. This is my own observation, not raised by any variant.
- **Confidence is only 66 percent** and the point is "not decidable from sources" (ADJ line 809). Variant 3 states this honestly.
- **The vocabulary content is deferred.** Like Variant 1, Variant 3 cannot name a single term or field now (Variant 3, "What stays unresolved"). Its assignment to SW-12 Phase 4 is PLAN INFERENCE (spec line 456).
- **Citation drift.** Variant 3 cites "line 398" for OB-09's audit rule, but line 398 is V2-01; OB-09 is at spec line 257. question.md also cites lines 257 and 701 for OB-08 decision 6, but the OB-08 row is at line 256 (line 701 is correct). The content is right; the line numbers are off.
- **Variant 1's re-ask checkpoint (U-001) is worth keeping.** Variant 3 would be stronger if it said the owner re-confirms the narrower promise when SW-12 Phase 4 opens.

## Shared assumptions

- **A-001 (the three consumers are the complete set; the watcher is outside): QUALIFY.** The watcher (#450) has its own local trust model (ADJ line 809), and none of the variants covers it if it later needs grants. Under Variant 3 this gap is cheapest to close: the watcher keeps its local mechanism and only adopts the shared words and audit shape. Under Variant 2, Edit 7's "no second format" would either pull the watcher into the single design or force an exception. So the assumption is incomplete, but it hurts Variant 3 least.
- **A-002 (changing issue text is cheap and reversible): QUALIFY.** Issue history makes the text reversible, and no trust code exists today (question.md fact 6). But the spec's own "Decision lifetime" rule says a changed answer voids unsent drafts, unmerged plans and dependent GRANT rows, and "effects already merged or applied outside need a separately authorized revert" (spec line 567). Once SW-12 Phase 4, V2-04 or CO-03 build against the promise, reversal stops being cheap. The narrowest promise that still settles the clauses (Variant 3) carries less reversal risk than Variant 2. Variant 1 carries the least, except for the sentence it leaves in #409.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason (short) |
|---|---|---|---|
| S-001 | Tie (no variant better) | 95% | All three use the same five sections. |
| C-001 | Variant 3 | 70% | Removes the overclaim "Decide one design, not two."; V1 keeps it by default, V2 endorses it. |
| C-002 | Variant 3 | 65% | Promising the vocabulary avoids binding Coder#477's cross-workspace listener to a local design; V1 leaves the texts inconsistent with #409. |
| C-003 | Variant 3 | 55% | Assigns an owner (SW-12 Phase 4) without fixing the mechanism; but it is PLAN INFERENCE and V1's re-ask has merit. |
| C-004 | Variant 3 | 60% | Settles every gated clause like V2, with a smaller commitment; V1 holds four items. |
| C-005 | Variant 3 | 70% | Names "relayed text stays data" as a separate control, matching spec lines 401, 407 and 637; V2 names the risk with no control; V1 is silent. |
| X-001 | Variant 3 | 65% | The spec's boundary rows (355, 401, 636) show different threat models; shared words plus shared audit fits that. |
| X-002 | Variant 3 | 60% | The narrow promise is safe to make now; V1's prematurity point is valid for V2 but less so for V3. |
| X-003 | Variant 3 | 65% | The sentence is an over-promise per X-005 and V4 edit 1 (ADJ lines 382, 567). |
| U-001 | Variant 1 | 60% | Re-asking at Phase 4 is a sound checkpoint the other variants lack; Variant 3 could adopt it. |
| U-002 | Variant 2 | 55% | A single owner and a bar on unreviewed second formats is a real security property; Variant 3 should keep a single owner for the vocabulary. |
| U-003 | Variant 3 | 70% | One audit shape enables cross-program incident review; CO-03 and OB-09 already expect audit events. |
| A-001 | Variant 3 | 55% | None covers the watcher; V3 absorbs a fourth consumer with its own local model most easily. |
| A-002 | Variant 1 | 55% | Committing nothing carries the least reversal risk under spec line 567; V3 is second, V2 last. |

## Overall

Variant 3 best fits the trust boundaries the spec already records: a read-only local observer, a same-host v2 first release and a cross-workspace listener with its own identity and permission checklist. It removes an overclaim and keeps poisoned content as a separate control. Its main security weakness is that shared words can hide weaker protection underneath. That needs a per-consumer statement of what each term enforces when SW-12 Phase 4 defines the vocabulary, plus a re-ask checkpoint at that point (borrowed from Variant 1).

Overall: the variant I judge best for the owner is Variant 3, confidence 65%

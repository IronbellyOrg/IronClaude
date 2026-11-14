# Round 1 advocate statement: Variant 3 (security persona)

Variant 3 is proposal C: "No. Record that no TUIBBS screen is planned, keep the observer single-host as a stated scope, and remove CO-04 (the copy channel) from the program" (variant-3-original.md line 5).

Sources checked by reading today (2026-11-14): merged-requirements.md lines 145, 353, 356, 375, 453, 531, 545, 1177; alignment-findings-adjudicated.md (ADJ) lines 91, 92, 131, 244, 306, 773, 788; round2-rebuttal-V5.md lines 20, 72, 134. The sibling `tuibbs-review/notes-3.md` and the owner's 2026-11-08 record were not read; anything taken from them is UNVERIFIED and is quoted only as the ADJ and V5 rebuttal quote it.

## Position summary

From a security view, the observer snapshot is a file that was deliberately kept private: it is written under `$XDG_STATE_HOME/superclaude/observe/` with mode 0600 (ADJ line 244), it is rewritten every live cycle (ADJ line 131), and the contract note carries an "untrusted-strings" rule with two named sanitizers (merged-requirements.md line 453). Every current item lives inside one trust boundary: "single owner, single OS user, single host" (line 453), with "snapshot transport to another host (Q18)" listed as out of scope (line 145).

Any copy channel is the first thing in the program that moves this file across a host boundary. ADJ line 306 lists what is missing before that can be done safely: a transport, an identity envelope (`scope` is only `object` or `"UNKNOWN"`), an age rule (no liveness field) and re-sanitising. None of these exists, and the receiving side has no design ("No document in TUIBBS mentions Coder or Orca", round2-rebuttal-V5.md line 20).

Variant 3 closes that boundary by decision rather than by deferral. Its value for security is that the smallest attack surface is the one that is not planned at all: no transport, no credential for a second host, no stale-copy rule, no second sanitizer, and no open public promise on Coder#477 that a channel is coming. It also gives Q3 a clean basis for closing Coder#477, which ADJ line 773 names as the preferred outcome "if the observer stays single-host and TUIBBS is not near".

My honest judgment, given below, is that Variant 1 achieves the same security posture today with less overreach, so I do not rank my own variant first.

## Steelman of Variant 1

Strongest version: Variant 1 gives exactly the same exposure today as Variant 3 (no channel, nothing leaves the workspace, single-host contract unchanged, variant-1-original.md lines 5 and 12) while being the only answer that matches the owner's own recorded stance. The owner's record says the observer "may become a TUIBBS module" and marks it "Background, not deciding" (ADJ line 306, quoting a sibling record UNVERIFIED by me). Variant 1 is also the spec's recommended answer and the default if the owner says nothing (merged-requirements.md line 545; ADJ line 788).

What it gets right on security, and what I underrated: it keeps CO-04 alive with its four preconditions written in (variant-1-original.md line 11; merged-requirements.md line 356). That means the day anyone opens the channel, the identity envelope, the age rule and the re-sanitising step are mandatory before code. That is a written security gate that travels with the item. Variant 3 deletes the item and with it that gate.

Critique: its second trigger, "an owner statement that a TUIBBS screen is planned", has no prompt except Q4 (variant-1-original.md line 23; merged-requirements.md line 1177). A deferred item with a soft trigger can be opened informally, for example by someone wiring a quick copy for a demo, without anyone re-reading CO-04. It also leaves Coder#477 with an open-ended "not yet", which keeps an external surface (a listener issue) pointed at a future channel (ADJ line 773 recommends narrowing #477 at about 65 percent).

## Steelman of Variant 2

Strongest version: the snapshot was shaped for exactly this reader (ADJ line 91), and designing the channel deliberately, now, before any code, is safer than letting the TUIBBS screen and the observer each invent their own transport later (variant-2-original.md line 19). It is the only variant that names the data-exposure risk in plain words: copying the 0600 file "widens who can read it" (variant-2-original.md line 23). Its Coder#477 text commits publicly to "read-only, identity-tagged, aged" and "nothing can be sent into a workspace" (line 12), which is a strong, testable boundary statement.

What it gets right: if a TUIBBS screen really is coming, a designed channel with an identity envelope and re-sanitising beats an ad hoc file copy. Security work done early is cheaper than security work retrofitted.

Critique with counter-evidence:
- It requires the owner to state something the record does not contain. The record is "Background, not deciding" (ADJ line 306), and D-9 says only the owner can settle it (round2-rebuttal-V5.md line 72). Variant 2 is not a security decision; it is a planning decision that creates a security workload.
- The receiving side is undesigned: "No document in TUIBBS mentions Coder or Orca" (round2-rebuttal-V5.md line 20). Designing a transport whose far end has no threat model means designing half a trust boundary.
- It pulls an authentication design forward against the spec, which says "No transport is selected until Q4, Q18 and the real authentication behaviour are settled" (merged-requirements.md line 375).
- It adds a new class of data in motion (worker rows keyed `dispatchId` and untrusted Orca strings, ADJ line 131; merged-requirements.md line 453) and a new credential for a second SSH host, with no current consumer.
- The public #477 text commits to properties ("identity-tagged, aged") that do not yet exist, which is a promise a reviewer can hold the program to before it is true.

## Strengths claimed

1. Smallest attack surface, durably. Variant 3 is the only answer under which no cross-host transport, no second-host credential and no off-host copy of the 0600 snapshot is planned at all (variant-3-original.md lines 5 and 16 to 18).
2. Clean trust boundary in the contract. The contract note keeps "single owner, single OS user, single host" (merged-requirements.md line 453) "without a pending exception" (variant-3-original.md line 12). A boundary with no pending exception is easier to test and to defend than one with an exception waiting on a trigger.
3. Removes a public pointer. Coder#477 is the workspace listener issue in the IronbellyOrg/Coder repository (question.md, CO-01 entry). Variant 3 gives Q3 the basis to close it (ADJ line 773), and CO-01 text C exists for exactly that case: "C if the observer stays single-host and TUIBBS is not near" (merged-requirements.md line 353). Fewer open listener designs means fewer half-specified entry points.
4. No pressure on Q22 or on an authentication design for a second host (variant-3-original.md line 18), which avoids designing security controls for a consumer that does not exist.
5. Explicit restart rule. "If TUIBBS ever becomes real, it starts as a new item with its own owner question" (variant-3-original.md line 5), so a future channel must pass a fresh owner decision rather than slip through a soft trigger.

## Weaknesses identified in others

- Variant 1: the "owner statement" trigger is soft and unprompted except by Q4 (merged-requirements.md line 1177). It does not raise data exposure at all (diff-analysis C-005). It keeps #477 in an open "not yet" state.
- Variant 2: it converts a "maybe" into a "yes" the record does not contain (ADJ line 306), designs a transport with no designed receiver (round2-rebuttal-V5.md line 20), pulls authentication forward against merged-requirements.md line 375, and widens readership of a file deliberately written 0600 (ADJ line 244). Its own risk list concedes all four (variant-2-original.md lines 23 to 26).

## Concessions

- Variant 3 overreaches on the record. It turns "may become a TUIBBS module" into a flat "no", which its own text admits (variant-3-original.md line 23). A security argument cannot supply an owner's intent.
- Today's exposure is identical under Variants 1 and 3: no channel exists under either. Variant 3's security gain is only about the future, and that gain is partly offset by the next point.
- Deleting CO-04 deletes its written preconditions (transport, identity envelope, age rule, re-sanitising; merged-requirements.md line 356). If TUIBBS returns as "a new item", nothing forces it to inherit those four controls; "the design starts from nothing" (variant-3-original.md line 24). For security that is a real loss: a deferred item with a written gate is safer than a blank slate.
- Closing Coder#477 early (variant-3-original.md line 24) is reversible but costs a reopen and a rewrite if TUIBBS comes back.
- Variant 3 does not name the data-exposure risk either; Variant 2 is the only one that does (diff-analysis C-005).

A fix that would make Variant 3 safer, offered for the record and not part of the original: close CO-04 but keep its four preconditions in the contract note as a standing rule for any future off-host copy.

## Shared assumptions

- A-001 (the snapshot is the right and only thing a TUIBBS screen would read): QUALIFY. ADJ line 306 supports it: "a TUIBBS screen would be a second reader of the observer's snapshot, not a second program with its own collector". From a security view, though, nobody has asked whether the whole snapshot (every worker row and untrusted Orca string) should leave the host, or only a reduced projection. Under Variant 3 the point is moot; under Variants 1 and 2 it should be part of the CO-04 design.
- A-002 (Coder#477 exists and the CO-01 reply will be posted): QUALIFY. CO-01 is posted under all three Q3 outcomes, including text C, the close text (merged-requirements.md line 353), so the answer still has a public home even if #477 is closed. The assumption fails only if the owner withholds CO-01; then the ledger is the only record, which is acceptable for Variant 3 because "no" needs no public follow-up, but for Variant 1 it leaves the trigger unannounced.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Variant 1 (no real difference) | 34% | All three use the same five sections. |
| C-001 | Variant 1 | 60% | Keeps CO-04 with its four security preconditions written in (merged-requirements.md line 356); Variant 3 deletes the gate, Variant 2 opens a channel with no designed receiver. |
| C-002 | Variant 1 | 55% | "No channel exists or is planned yet" is accurate to the record; Variant 3's "none planned" overstates it, Variant 2 promises properties that do not exist. |
| C-003 | Variant 3 | 50% | Neither 1 nor 3 pulls Q22 or authentication forward; Variant 3 removes the need entirely, which is marginally less surface. |
| C-004 | Variant 3 | 55% | Single host with no pending exception is the tightest boundary; Variant 1 is equal in practice today. |
| C-005 | Variant 2 | 60% | Only variant that names the exposure of the 0600 snapshot (ADJ line 244); 1 and 3 avoid the exposure but do not say why it matters. |
| X-001 | Variant 1 | 70% | Only the owner knows (round2-rebuttal-V5.md line 72); "unknown, wait" is the only answer that does not invent the owner's intent. |
| X-002 | Variant 1 | 80% | Matches "Background, not deciding" (ADJ line 306); 2 and 3 both rewrite it. |
| X-003 | Variant 1 | 60% | Its cost of being wrong (a second #477 edit) is smallest; Variant 2's cost is a security cost, Variant 3's is losing the written gate. |
| U-001 | Variant 1 | 60% | Correctly identifies Q4 as the only prompt for the owner trigger (merged-requirements.md line 1177), a real gap worth knowing. |
| U-002 | Variant 2 | 60% | Most concrete statement of the four controls and a read-only boundary for #477. |
| U-003 | Variant 3 | 60% | Ties Q18 to the Q3 close path (ADJ line 773; CO-01 text C, merged-requirements.md line 353). |
| A-001 | Variant 1 | 50% | Shared by all; Variant 1 keeps a design item where the reduced-projection question can be raised. |
| A-002 | Variant 3 | 55% | Variant 3 alone plans for #477 being closed, and its "no" needs no follow-up post. |

## Overall

Variant 3 gives the tightest long-term trust boundary, but Variant 1 gives the same exposure today, keeps the four security preconditions attached to CO-04, and does not overrule the owner's recorded "not deciding". If the owner truly holds "no TUIBBS screen", Variant 3 is the right answer; absent that statement, Variant 1 is safer and more honest.

Overall: the variant I judge best for the owner is Variant 1, confidence 65%

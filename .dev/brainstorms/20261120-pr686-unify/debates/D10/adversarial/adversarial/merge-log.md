# Merge Log (D10 wake transport)

## Metadata

- Base: Variant 2 (CLAY paper), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/adversarial/adversarial/variant-2-original.md`
- Other source: Variant 1 (OURS), `variant-1-original.md`, plus `invariant-probe.md` and `refactor-plan.md` in the same folder
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/adversarial/merged-output.md`
- Changes planned: 10. Changes applied: 10. Failed: 0. Skipped: 0.
- Status: Success (all changes applied; validation passed with the notes below)
- Timestamp: 2026-11-20 (no clock time available to the executor)
- Deliberate step renumbering: the new reading step (Change #3) is mechanism step 4, so base steps 4 and 5 became steps 5 and 6. The plan's "step 4", "step 3" and "step 5" targets were applied to the base's acknowledgment, typed-line and session-start text.

## Changes Applied

### Change #1: Reframe the claim as a HYBRID
- Status: applied
- Before: claim said one JSON file, one mailbox message and a typed line when idle; poll resends up to 3 times; no listener.
- After: durable wake file plus orchestrator acknowledgment is the transport; mailbox and typed line are optional nudges carrying the wake id; no listener; 3 deliveries in total; points to M1 and M2.
- Provenance: `Source: Base (original, modified), merged per Change #1`
- Validation: claim agrees with mechanism steps 2, 3 and 5. One wording fix inside this change: "resends up to 3 times" became "3 deliveries in total (first send plus two resends)" so the claim matches the base's own step text "attempt 2 then 3" (probe INV-010 supports the count). No new facts.

### Change #2: Add the no-listener decision with the owner's evidence
- Status: applied
- Before: base fact 6 only credited both lines with rejecting the listener.
- After: new subsection "No listener, and whose decision that is" under the claim (D1 option A, NG-1, `issue-watcher.md:47`, `:55`, `:76`; D:66; owner decision Q3 at `owner-answers.md:25`); fact 6 now points to it.
- Provenance: `Source: Variant 1 facts 1 and 2 ... merged per Change #2`; fact 6 tagged as base, modified
- Validation: all citations are from Variant 1. The H3 sits under the H2 "The claim", so no heading gap.

### Change #3: Make the coordinator loop read the wake directory
- Status: applied
- Before: no step where the orchestrator reads the wake directory.
- After: new mechanism step 4, reads at every return of `check --wait`, at most once per 5 minutes, only wakes whose target is itself; evidence D:571, D:572, `WORKER-CONTRACT.md:101`, `:103`, `:110`, D:177, D:220.
- Provenance: `Source: Base (original, modified): new step inserted per Change #3`
- Validation: later steps renumbered and all step references re-checked (see Post-Merge Validation). The statement that PR B does not exist is from Variant 1 fact 6 and marked UNVERIFIED for the future loop. A cost bullet was added (PR B takes a new loop duty), taken from the plan's risk summary.

### Change #4: Fix the acknowledgment ordering (HIGH INV-001)
- Status: applied
- Before: step 4 said the ack lists every item in one bucket, resend at 10 minutes, then abandoned, with no ordering rule.
- After: step 5 adds the rule that an item is listed as taken only after its per-issue state file exists, for every assigned item; M1 section holds the evidence (D:229, D:536, D:538, D:539, D:657; `cycle.py:777-787`, `:805-810`, `:994`; `wake.py:584-597`); the bucket stays `taken` until a coordinated rename.
- Provenance: `Source: Base (original, modified), merged per Change #4 (HIGH INV-001)`; M1 tagged `Source: Invariant probe INV-001`
- Validation: M1 and step 5 use the same wording. Consequential edit: the "loses nothing" bullet in "What it gets right" is now conditional on M1 and M2, because it would otherwise contradict the evidence in M1 (see Contradiction re-scan).

### Change #5: Make abandonment recoverable (HIGH INV-002)
- Status: applied
- Before: "What it risks" had no abandonment risk.
- After: a risk bullet plus section M2. The spec must pick (a) re-target to the next orchestrator of the repo with a new wake id, or (b) keep the wake visible to a named reader; this position does not pick; spec text only. Evidence: `record.py:891-900`, `:971-985`; `cycle.py:994`, `:1427-1429`; `route.py:407-413`, `:598-602`; D:220; `wake.py:493-496`.
- Provenance: `Source: Invariant probe INV-002, merged per Change #5`
- Validation: step 5 and the claim point to M2; M2 text does not contradict step 4 (it states why the directory read cannot recover these wakes).

### Change #6: Drop issue titles and defer the plan hold payload
- Status: applied
- Before: step 1 had no field list; the risk bullet said the plan request carries an issue title (D:185; `wake.py:103-113`; `clean_title` at `:168-176`).
- After: step 1 says the wake carries `repo`, `number`, `url` and no title (D:116), and `plan_requests[]` belongs to D09; the risk bullet now says PR 686 still has the `PlanRequestItem` title path and the risk stays open until PR 686 follows.
- Provenance: `Source: Base (original, modified), merged per Change #6`; step 1 tagged the same
- Validation: the claim's "holds every fact" was reworded to "holds the issue references" so it does not overstate. A first draft sentence quoting D:190 was removed during validation because it read as a conflict with D:185.

### Change #7: Keep the rule on every channel; credit D3 as its origin
- Status: applied
- Before: "Its security rule is stated for every channel ... not only for the prompt."
- After: same bullet, now naming the owner's D3 (`issue-watcher.md:39`, `:49`; `launch.py:33`, `:84-92`, `:95-116`; D:155) and keeping Clay's wider scope (D:234, guarantee 2).
- Provenance: `Source: Variant 1 fact 3 ... merged per Change #7`
- Validation: wider scope kept, origin credited; no contradiction with fact 3.

### Change #8: Typed line is a nudge to an idle or freshly started session only; add the guard gap
- Status: applied
- Before: step 3 sent the line only if idle, no unsent typing, 60 seconds quiet.
- After: step 3 keeps those three checks, adds "tail of the screen shows the main input prompt" (FR-24 rule 1, D:573), states the uses (D:319, D:710), the guard gap (`wake.py:746-772`, `:774-790`; `orca_term.py:113-121`) and that a failed check types nothing. Fact 4 and the typing-race risk bullet were extended to match.
- Provenance: `Source: Base (original, modified), merged per Change #8`
- Validation: the typed line is never sent to a busy or `check --wait` session, in step 3, fact 2 and the risks. The screen check is marked untried on a live system (UNVERIFIED).

### Change #9: Session start through one fixed-pattern verb if a live spike passes
- Status: applied
- Before: step 5 started a session with `ccsession <tag> --tier <tier>` when none existed.
- After: step 6 prefers `orca agent launch` with a second fixed prompt pattern only if a live spike shows the ccsession tag is carried (U25); otherwise keeps the typed start; in both cases an unreadable process table means "unknown" and no session is started (INV-008, `wake.py:609-621`, `:731-744`, `:897-934`). Fact 8 and a risk bullet were extended.
- Provenance: `Source: Base (original, modified), merged per Change #9`
- Validation: fact 8 (starts a session when none is live) now says "and the lookup could be read", matching step 6. The spike is marked UNVERIFIED.

### Change #10: One shared terminal helper with a parity test; neutral acknowledgment name
- Status: applied
- Before: costs listed the 100 to 150 line copy of `orca_term.py` as K16 "Accepted for now"; the risk list had a "no parity test" bullet.
- After: costs say no copy ships to a second consumer; one helper in the package with a test run against the report waker's fixtures; helper location and ordering against PR C marked UNVERIFIED; a bullet on the acknowledgment rename (`wake.py:565`, `:47`; `cycle.py:777-784`; INV-019). The "no parity test" risk bullet was removed because the cost bullet now carries those facts.
- Provenance: `Source: Base (original, modified), merged per Change #10 and Variant 1 fact 7`; rename bullet tagged INV-019
- Validation: the K19 bullet was kept with one added clause about the shared helper. Facts quoted (`wake.py` lines 9-12, `orca_term.py:3`, `test_wake.py:495`) are from Variant 1.

### Additions outside the 10 numbered changes
- Section "Mandatory conditions" (M1, M2): requested by the orchestrator's task text, which asked for the two HIGH invariants as explicit mandatory conditions. Content comes only from the plan and the probe.
- Header rewrite: title, status line, removal of the "Author stance" line, and an extended path note (explains INV, K and U labels and the Variant 1 path convention). Needed because the document is no longer Clay's paper.
- Small wording changes: "our line" became "the owner's claim line" (fact 8), and "that OURS does not have" became a pointer to the owner's claim-launch line with its two gaps from Variant 1 costs.

## Post-Merge Validation

### Structural integrity
- Heading levels: one H1, six H2 sections in the base skeleton order (claim, mechanism, cited facts, costs, risks, gets right) plus one added H2 "Mandatory conditions" after the mechanism; H3 only under "The claim" and "Mandatory conditions". No level is skipped.
- Provenance: header has `Provenance`, `Base` and merge date (2026-11-20); every section and block has a `Source` comment. No comment contains a double hyphen.
- No em dashes or en dashes in the output (searched).

### Internal references
- Claim to "M1" and "M2": resolve to the two H3 sections.
- Step 5 to M2 and to "What it costs": resolve.
- Step 6, fact 4 ("step 3"), fact 8 ("step 6"), costs ("step 4"), risks ("step 1", "step 3", "step 6"), M2 ("step 4"): each points to the step with that content after renumbering.
- Fact 6 to "No listener, and whose decision that is": resolves. "Mandatory conditions" to "What it gets right": resolves.

### Contradiction re-scan
- Typed line: step 3 sends it only to an idle session at its main prompt or to a session just started and never to a busy or `check --wait` session. Claim, fact 2 and the first risk bullet say the same. Step 6's typed start is a started session, which step 3 allows. No contradiction.
- "Loses nothing": the base bullet would have contradicted M1 and M2, so it was made conditional on them.
- Typed-line practice on master: fact 4 now says that practice checks only draft and output age, which agrees with step 3's added screen check.
- Titles: step 1 and the risks say no title in the wake file; fact 3 says no title reaches a typed line. Consistent.
- Session start: fact 8 and step 6 both require a readable lookup.
- Delivery count: claim and step 5 both say 3 deliveries in total.
- Probe findings below HIGH that the plan did not include (INV-003, -004, -010 beyond the claim wording, -011 to -016, -018 to -020, -024 to -026) were not added, because the plan does not ask for them.
- Items marked UNVERIFIED: `tui-idle` meaning, the typing race, the screen-tail check on a live system, the one-verb start spike (U25), the `OrcaLauncher` fresh-terminal behaviour, helper location and size, and whether PR B will build the loop read.

## Summary

| Planned | Applied | Failed | Skipped |
|---------|---------|--------|---------|
| 10 | 10 | 0 | 0 |

Escalation to the orchestrator: none. The one judgement call is the renumbering of mechanism steps (new step 4), recorded in Metadata.

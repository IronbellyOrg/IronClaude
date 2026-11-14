# Round 1 Advocate Statement: Variant 1 ("No, WC-16 loop only")

## Position

Variant 1 answers Q31 "no": this program's coordinator keeps only the worker contract's loop and adds no 10-minute timer. Its case rests on three facts.

1. The checked-in contract already defines a complete loop. WC-16 (`src/superclaude/core/WORKER-CONTRACT.md`, the "### WC-16. Coordinator loop" paragraph, cited by the spec as `WORKER-CONTRACT.md:288`) says the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it." That is the first half of the 2026-11-05 order, already in force without Q31.
2. WC-16 already names the scheduling it wants: "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." Variant 1 reads that literally.
3. The order Variant 1 declines lives only in a memory note, which the spec itself ranks lowest (question.md fact 1 and fact 3; spec cadence row: "lowest source tier, so asked as Q31"). A no keeps the whole cadence auditable from checked-in text (Variant 1, "What it unlocks": "A reviewer can audit the cadence from the contract alone").

It also avoids every mechanism risk of a session cron: the 7-day auto-expiry and session-only life (question.md fact 6), the open question of whether a cron fire is a "coordinator wake" that triggers the sweep pass (fact 6, UNVERIFIED), and the A-002 point that a session cron fires only while the session is idle.

## Steelman of Variant 2

Variant 2's strongest form: the defect INV-010 found is not "this program lacks a timer" but "a standing owner order lives only in memory, so drafts miss it" (`invariant-probe.md:18`, as quoted in question.md fact 3). Answering yes for one program fixes the symptom; writing the rule into WC-16 fixes the cause, so every later coordinator inherits it without the owner being asked again. It also removes the WC-16 ambiguity ("Phase 1 adds this duty, not a scheduler") at its source and lets the contract settle whether a cron fire is a "wake". It gets right that the current ambiguity is a contract-wording problem, and it honestly lists its own costs (scope growth, one more PR, the cron's 7-day limit, maybe-too-wide GitHub scope).

## Steelman of Variant 3

Variant 3's strongest form: the owner gave a specific, recent order with a concrete failure behind it. The memory note says the order exists because "the owner found sessions unwatched" and "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all." This program has exactly such peers (the Q25 PR sessions and the Q33 #539 author session, Variant 3 "What it unlocks"). WC-16's own coverage of person-started sessions goes through `/sc:sweep` ("Person-started sessions appear in the report, observed from transcripts and ccsession files"), and the spec says `/sc:sweep` is "not runnable" until SWEEP-RUNNABLE holds (spec section 6.6 note). So during the early waves, nothing in WC-16 sees those peers; only the owner's check does. Variant 3 also does the operational work the others skip: it records the cron job id and expiry in the ledger and re-creates it on expiry or resume, keeps every limit of spec line 579 ("Q31 does not authorize `/sc:sweep` above WC-16's cap or any write"), and makes routine runs silent per the 2026-11-09 reporting order. It matches the spec's recommended answer ("Yes, read-only") and stays scoped to the program the question asks about.

## Key strengths claimed

- Single source of truth: the cadence is fully described by `WORKER-CONTRACT.md` WC-16 plus the spec's existing 6.6 rows; no behaviour depends on a memory note.
- No mechanism debt: no session cron, so no 7-day expiry, no resume re-creation step, no idle-only firing gap (A-002).
- No ambiguity about whether a cron fire is a WC-16 "wake" that triggers "The sweep." (C-007).
- GitHub is still read: the 6.6 GitHub row already reads state "at wave gates and before each edit; each PR at coordinator wakes with `gh pr view <N> --repo IronbellyOrg/IronClaude`".
- Lower load: no roughly 144 read cycles a day across Orca and two repos.

## Weaknesses identified in Variant 2

- It answers a broader question than was asked. Q31 asks whether the order applies "to this program's coordinator". Variant 2 turns it into a change to an installed core file every project receives (its own cost list: "a decision for all coordinators, not just this program, made through a question that was framed for one program").
- It adds a PR and a new work item outside the program's 50 during a program whose bottleneck is owner latency (its own quote: "Owner latency is the real schedule").
- Its contract sentence names a 10-minute recurring check but does not yet say how a session-only, 7-day cron survives expiry and resume; it admits a rule that omits this "writes a promise the tool cannot keep".
- It leaves the reporting style (2026-11-09 order) unresolved, which Variant 3 already settles.
- Its immediate effect for this program is identical to Variant 3, so for Q31 itself it adds cost without adding behaviour.

## Weaknesses identified in Variant 3

- Second clock beside WC-16 with an unverified interaction: if a cron fire counts as a "coordinator wake", each fire also triggers WC-16's sweep pass (its own admission, UNVERIFIED).
- The check is "about every 10 minutes" only while the coordinator is idle (A-002); none of the variants say so, and a long busy turn delays it.
- It depends on a manual re-creation step every 7 days and after every resume; a missed step stops the check silently.
- The rule stays in memory and the ledger, so the next coordinator outside this program can miss it again (its own cost list).
- Read load on two GitHub repos is unmeasured (UNVERIFIED).

These are real but bounded: none breaks a spec limit, and the ledger-recorded job id and expiry make a lapse detectable.

## Concessions

- Variant 1 overrides a standing owner order that exists because of a real failure. That is its largest weakness, and I do not think it is outweighed.
- Variant 1 leaves non-worker peers unwatched between their own reports. Its own text admits "If one goes quiet or finishes, nothing in WC-16 notices it." Worse than its text says: WC-16's coverage of person-started sessions comes through `/sc:sweep`, which the spec records as "not runnable" until SWEEP-RUNNABLE holds, so in early waves those peers are fully invisible.
- WC-16's "Phase 1 adds this duty, not a scheduler" describes what Phase 1 adds to the contract; it is not a ban on an owner-ordered read-only check. Probe INV-010 reads it the same way. Variant 1 leans on it harder than the text supports.
- PR events between wakes (new review comments, red CI) are seen late under Variant 1.
- Variant 1's mechanism savings are real but small next to the supervision gap.

## Shared assumption responses

- **A-001 (the 2026-11-05 order still reflects the owner's intent): QUALIFY.** The note is 9 days old and no later memory revokes it; the 2026-11-09 order changed only how automated checks report ("display only outstanding questions or decisions"), which presumes such checks continue. So it is reasonable to treat the order as current, but that is exactly why the spec asks the owner rather than picking from memory. All variants should state it is the owner's confirmation, not memory, that settles it.
- **A-002 (a session cron fires only while the session is idle): ACCEPT.** The CronCreate tool description says jobs "only fire while the REPL is idle (not mid-query)". The coordinator mostly sits idle on a background Orca wait, so the gap is small in practice, but any yes answer should say the cadence is "about every 10 minutes while idle", and Variant 1's cost argument is slightly strengthened by it.

## Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | Its operational sub-list (cron, expiry, silent reporting, limits) is what the coordinator actually needs to act on. |
| C-001 | 3 | Yes, read-only follows the owner's order and closes the non-worker peer gap that WC-16 cannot cover while `/sc:sweep` is not runnable. |
| C-002 | 3 | Keeps the rule scoped to the program the question names; Variant 2's contract change is a separate decision. |
| C-003 | 3 | Timer-renewed idle subscriptions are the only mechanism that sees non-worker peers; 2 matches it but adds scope, so 3 wins on scope. |
| C-004 | 3 | 10-minute PR reads catch review comments and CI failures between wakes; 2 is equal in behaviour, 3 is narrower in scope. |
| C-005 | 3 | Recording job id and expiry and re-creating on expiry or resume handles the tool's real limits; 1 avoids them only by dropping the check. |
| C-006 | 3 | Silent unless a decision is needed applies the 2026-11-09 order; 2 leaves it open. |
| C-007 | 2 | Settling whether a cron fire is a "wake" in the contract text is the right fix; 3 only flags it UNVERIFIED. |
| X-001 | 3 | "In force" matches the owner's order and the spec's recommended answer. |
| X-002 | 3 | The question asks about this program; binding every coordinator needs its own question. |
| X-003 | 3 | Reading "not a scheduler" as not a ban on the owner's check matches both the WC-16 text and probe INV-010. |
| A-001 | 3 | Treats the order as current but asks the owner to confirm, with the 2026-11-09 reporting rule applied. |
| A-002 | 1 | Only Variant 1 avoids the idle-only firing gap, though none states it. |

## Overall

Variant 1 is the clean, auditable answer, but it leaves this program's non-worker peers unwatched in exactly the situation the owner's order was written to prevent, and WC-16 cannot cover them until `/sc:sweep` becomes runnable. Variant 3 follows the order within every spec limit and handles the cron's real lifecycle; Variant 2's contract promotion is worth asking as a separate question, not bundled into Q31.

Overall best answer for the owner: Variant 3, confidence 75%

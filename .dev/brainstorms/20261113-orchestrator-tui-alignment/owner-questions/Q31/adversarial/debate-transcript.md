# Adversarial Debate Transcript (Q31)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% by majority rule (14 of 14 points have at least 2 of 3 advocates agreeing); unanimous on 8 of 14 (57%)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (each a spawned general-purpose agent on the session's default model; Variant 1 = proposal-A, Variant 2 = proposal-B, Variant 3 = proposal-C)
- Taxonomy coverage: L1 surface (S-001, S-002), L2 structural (C-002, C-004, X-002), L3 state mechanics (C-005, C-007, A-002) all covered; no forced round
- Advocate statements were written by the advocates to `round1-advocate-1.md`, `round1-advocate-2.md`, `round1-advocate-3.md` in this folder and are reproduced below unchanged except heading levels.

## Round 1: Advocate Statements

### Variant 1 Advocate (general-purpose, default model)



#### Position

Variant 1 answers Q31 "no": this program's coordinator keeps only the worker contract's loop and adds no 10-minute timer. Its case rests on three facts.

1. The checked-in contract already defines a complete loop. WC-16 (`src/superclaude/core/WORKER-CONTRACT.md`, the "### WC-16. Coordinator loop" paragraph, cited by the spec as `WORKER-CONTRACT.md:288`) says the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it." That is the first half of the 2026-11-05 order, already in force without Q31.
2. WC-16 already names the scheduling it wants: "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." Variant 1 reads that literally.
3. The order Variant 1 declines lives only in a memory note, which the spec itself ranks lowest (question.md fact 1 and fact 3; spec cadence row: "lowest source tier, so asked as Q31"). A no keeps the whole cadence auditable from checked-in text (Variant 1, "What it unlocks": "A reviewer can audit the cadence from the contract alone").

It also avoids every mechanism risk of a session cron: the 7-day auto-expiry and session-only life (question.md fact 6), the open question of whether a cron fire is a "coordinator wake" that triggers the sweep pass (fact 6, UNVERIFIED), and the A-002 point that a session cron fires only while the session is idle.

#### Steelman of Variant 2

Variant 2's strongest form: the defect INV-010 found is not "this program lacks a timer" but "a standing owner order lives only in memory, so drafts miss it" (`invariant-probe.md:18`, as quoted in question.md fact 3). Answering yes for one program fixes the symptom; writing the rule into WC-16 fixes the cause, so every later coordinator inherits it without the owner being asked again. It also removes the WC-16 ambiguity ("Phase 1 adds this duty, not a scheduler") at its source and lets the contract settle whether a cron fire is a "wake". It gets right that the current ambiguity is a contract-wording problem, and it honestly lists its own costs (scope growth, one more PR, the cron's 7-day limit, maybe-too-wide GitHub scope).

#### Steelman of Variant 3

Variant 3's strongest form: the owner gave a specific, recent order with a concrete failure behind it. The memory note says the order exists because "the owner found sessions unwatched" and "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all." This program has exactly such peers (the Q25 PR sessions and the Q33 #539 author session, Variant 3 "What it unlocks"). WC-16's own coverage of person-started sessions goes through `/sc:sweep` ("Person-started sessions appear in the report, observed from transcripts and ccsession files"), and the spec says `/sc:sweep` is "not runnable" until SWEEP-RUNNABLE holds (spec section 6.6 note). So during the early waves, nothing in WC-16 sees those peers; only the owner's check does. Variant 3 also does the operational work the others skip: it records the cron job id and expiry in the ledger and re-creates it on expiry or resume, keeps every limit of spec line 579 ("Q31 does not authorize `/sc:sweep` above WC-16's cap or any write"), and makes routine runs silent per the 2026-11-09 reporting order. It matches the spec's recommended answer ("Yes, read-only") and stays scoped to the program the question asks about.

#### Key strengths claimed

- Single source of truth: the cadence is fully described by `WORKER-CONTRACT.md` WC-16 plus the spec's existing 6.6 rows; no behaviour depends on a memory note.
- No mechanism debt: no session cron, so no 7-day expiry, no resume re-creation step, no idle-only firing gap (A-002).
- No ambiguity about whether a cron fire is a WC-16 "wake" that triggers "The sweep." (C-007).
- GitHub is still read: the 6.6 GitHub row already reads state "at wave gates and before each edit; each PR at coordinator wakes with `gh pr view <N> --repo IronbellyOrg/IronClaude`".
- Lower load: no roughly 144 read cycles a day across Orca and two repos.

#### Weaknesses identified in Variant 2

- It answers a broader question than was asked. Q31 asks whether the order applies "to this program's coordinator". Variant 2 turns it into a change to an installed core file every project receives (its own cost list: "a decision for all coordinators, not just this program, made through a question that was framed for one program").
- It adds a PR and a new work item outside the program's 50 during a program whose bottleneck is owner latency (its own quote: "Owner latency is the real schedule").
- Its contract sentence names a 10-minute recurring check but does not yet say how a session-only, 7-day cron survives expiry and resume; it admits a rule that omits this "writes a promise the tool cannot keep".
- It leaves the reporting style (2026-11-09 order) unresolved, which Variant 3 already settles.
- Its immediate effect for this program is identical to Variant 3, so for Q31 itself it adds cost without adding behaviour.

#### Weaknesses identified in Variant 3

- Second clock beside WC-16 with an unverified interaction: if a cron fire counts as a "coordinator wake", each fire also triggers WC-16's sweep pass (its own admission, UNVERIFIED).
- The check is "about every 10 minutes" only while the coordinator is idle (A-002); none of the variants say so, and a long busy turn delays it.
- It depends on a manual re-creation step every 7 days and after every resume; a missed step stops the check silently.
- The rule stays in memory and the ledger, so the next coordinator outside this program can miss it again (its own cost list).
- Read load on two GitHub repos is unmeasured (UNVERIFIED).

These are real but bounded: none breaks a spec limit, and the ledger-recorded job id and expiry make a lapse detectable.

#### Concessions

- Variant 1 overrides a standing owner order that exists because of a real failure. That is its largest weakness, and I do not think it is outweighed.
- Variant 1 leaves non-worker peers unwatched between their own reports. Its own text admits "If one goes quiet or finishes, nothing in WC-16 notices it." Worse than its text says: WC-16's coverage of person-started sessions comes through `/sc:sweep`, which the spec records as "not runnable" until SWEEP-RUNNABLE holds, so in early waves those peers are fully invisible.
- WC-16's "Phase 1 adds this duty, not a scheduler" describes what Phase 1 adds to the contract; it is not a ban on an owner-ordered read-only check. Probe INV-010 reads it the same way. Variant 1 leans on it harder than the text supports.
- PR events between wakes (new review comments, red CI) are seen late under Variant 1.
- Variant 1's mechanism savings are real but small next to the supervision gap.

#### Shared assumption responses

- **A-001 (the 2026-11-05 order still reflects the owner's intent): QUALIFY.** The note is 9 days old and no later memory revokes it; the 2026-11-09 order changed only how automated checks report ("display only outstanding questions or decisions"), which presumes such checks continue. So it is reasonable to treat the order as current, but that is exactly why the spec asks the owner rather than picking from memory. All variants should state it is the owner's confirmation, not memory, that settles it.
- **A-002 (a session cron fires only while the session is idle): ACCEPT.** The CronCreate tool description says jobs "only fire while the REPL is idle (not mid-query)". The coordinator mostly sits idle on a background Orca wait, so the gap is small in practice, but any yes answer should say the cadence is "about every 10 minutes while idle", and Variant 1's cost argument is slightly strengthened by it.

#### Per-point verdicts

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

#### Overall

Variant 1 is the clean, auditable answer, but it leaves this program's non-worker peers unwatched in exactly the situation the owner's order was written to prevent, and WC-16 cannot cover them until `/sc:sweep` becomes runnable. Variant 3 follows the order within every spec limit and handles the cron's real lifecycle; Variant 2's contract promotion is worth asking as a separate question, not bundled into Q31.

Overall best answer for the owner: Variant 3, confidence 75%

### Variant 2 Advocate (general-purpose, default model)



#### Position

Variant 2 answers "yes, read-only" for this program's coordinator, exactly like Variant 3, and adds one thing: a separate small PR that writes the read-only ten-minute check into the checked-in coordinator rules (WC-16 or the orchestration guide), so it stops resting on a memory note.

The case for it rests on three verified facts:

- The order today lives only in memory. `coordinator-never-stop-polling.md` (modified 2026-11-05) says: "Keep a recurring CronCreate sweep (every ~10 minutes, off-minute) that re-checks the Orca run, ListAgents, open PRs on IronClaude and Coder, and re-subscribes `notify_when_idle` on busy peers."
- The spec itself ranks that source lowest and says so in the cadence record: "owner memory `coordinator-never-stop-polling.md` (2026-11-05 order; lowest source tier, so asked as Q31)" (`merged-requirements.md` line 1026).
- The checked-in contract contains the sentence that caused the confusion: "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." (`WORKER-CONTRACT.md:288`). The spec had to add a note to explain that this "concerns the `/sc:sweep` duty, not a ban on the owner's check" (line 1016). Probe INV-010 (as quoted in `question.md` fact 3) found that two of three drafts read it as "no extra scheduler".

So the defect is in the source text, not only in this program. Variant 3 fixes the symptom for one program; Variant 2 also fixes the cause. Variant 2's immediate behaviour for this program is the same read-only cron as Variant 3, with the same limits from line 579 ("Q31 does not authorize `/sc:sweep` above WC-16's cap or any write").

#### Steelman of Variant 1

The strongest version of Variant 1: the coordinator's cadence should be fully described by a reviewed, checked-in file, and WC-16 already says the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it" (`WORKER-CONTRACT.md:288`). That directly answers the failure that produced the 2026-11-05 order (a lapsed wait). A second clock adds load (about 144 reads a day across Orca and two GitHub repos), a 7-day cron expiry to manage, and an open question about whether a cron fire is a "coordinator wake" that triggers the sweep pass. Saying "no" keeps one clock family, auditable from one file, and the spec already reads GitHub at wave gates, before each edit and at wakes (line 1025). Variant 1 also honestly names its own cost: it "overrides a standing owner order that exists because of a real failure."

What it gets right: it is the only variant with zero operational cost, and it correctly values a checked-in source over memory. That second point is the same value Variant 2 acts on.

#### Steelman of Variant 3

The strongest version of Variant 3: it answers exactly the question asked (does the order apply to this coordinator) and nothing more, follows the owner's standing order and the reason behind it ("Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all"), and it is the most operationally complete variant. It records the cron job id and its 7-day expiry in the ledger and re-creates it on expiry or resume, which addresses the CronCreate limit ("Recurring tasks auto-expire after 7 days"). It makes routine runs silent per the 2026-11-09 order (`orchestration-decision-ledger-only.md`). It names the "is a cron fire a wake" question as UNVERIFIED and bounds it by the 5-minute cap. It adds no PR and no scope during a program where "Owner latency is the real schedule" (line 523).

What it gets right: everything Variant 2 does for this program, plus two operational details Variant 2 left open (expiry handling in the ledger, silent reporting).

#### Key strengths claimed

1. Fixes the root cause, not only the instance. The confusion INV-010 found comes from contract text ("Phase 1 adds this duty, not a scheduler") and from the order living only in memory. Only Variant 2 changes either.
2. Same immediate behaviour as Variant 3 for this program: one off-minute recurring read-only check, the same four reads, never writes, never runs `/sc:sweep` above WC-16's cap (line 579, line 1026).
3. Lets the contract settle in one place whether a cron fire counts as a "coordinator wake" for WC-16, which is UNVERIFIED today (`question.md` fact 6).
4. Raises the source tier of an owner order. A future coordinator outside this program reads the installed contract; it may not read this program's ledger or that memory note.
5. Names its own risk honestly: a contract rule naming a 10-minute cron "must also say what happens on expiry and on resume, or it writes a promise the tool cannot keep."

#### Weaknesses identified in Variant 1

- It overrides a live owner order with nothing but the spec's own inference. The memory note is explicit and the reason (non-worker peers are invisible to the Orca queue) is not addressed by WC-16, which watches only the Run.
- It leaves non-worker peers (Q25 PR sessions, the Q33 #539 author) supervised only "when the coordinator subscribes to them for a specific reason", which is the gap that caused the order.
- It treats WC-16 as the complete cadence, but the spec's own cadence record says WC-16's "not a scheduler" sentence "concerns the `/sc:sweep` duty, not a ban on the owner's check" (line 1016). Variant 1 rests on the reading the spec already rejected.
- It does not address A-002 or A-001; it only avoids the cron.

#### Weaknesses identified in Variant 3

- It keeps the rule in "a memory note and a ledger row, not in a checked-in file, so the next coordinator outside this program may again miss it" (Variant 3's own words). The same miss INV-010 found will recur.
- It leaves the WC-16 sentence that misled two drafts unchanged, so every future spec must re-add the explanatory note from line 1016.
- It does not settle the "cron fire is a wake" question; it bounds it. That is acceptable for one program but not as a standing rule.
- It does not discuss that a session cron fires only while the coordinator is idle (A-002), though neither does Variant 2.

#### Concessions

- Variant 2 grows scope. It edits an installed core file (`~/.claude/WORKER-CONTRACT.md`) that every IronClaude project receives, through a question framed for one program. The question asked is "does it apply to this program's coordinator", and Variant 2 answers more than that. An owner can reasonably say the contract change deserves its own question or issue.
- It adds a PR during a program whose bottleneck is owner latency (line 523).
- Its operational detail for this program is thinner than Variant 3's: it does not say the ledger records the cron job id and expiry, and it leaves open how the check reports (C-006). Variant 3 is better on both.
- A contract rule that names CronCreate inherits a tool that is session-only and expires after 7 days; writing it into a contract before the expiry and resume handling is designed risks a promise the mechanism cannot keep. Variant 2 names this risk but does not solve it.
- The GitHub scope in the order (all open PRs on two repos) may be too wide for every coordinator, so generalizing it is not obviously right.
- The contract PR does not need Q31 to happen. The owner can answer Variant 3 now and open the contract change as a separate item later; that sequencing gets Variant 2's benefit without its scope cost.

#### Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001: the 2026-11-05 order still reflects the owner's intent on 2026-11-14 | QUALIFY | The note is 9 days old and the 2026-11-09 order changed how such checks report, not whether they run. Nothing seen supersedes the 2026-11-05 order, and the MEMORY.md index still lists it as current ("owner order 2026-11-05: re-arm the Orca wait after every expiry, keep a cron sweep"). But that is exactly why Q31 is asked: the owner's answer, not the note, should confirm it. Any "yes" should state that it is the owner's fresh confirmation. |
| A-002: a session cron fires only while the coordinator session is idle | ACCEPT | The CronCreate tool description in this session says "Jobs only fire while the REPL is idle (not mid-query)". So "about every 10 minutes" holds only while the coordinator waits; a long busy turn delays the check. This weakens the "within 10 minutes" claim of Variants 2 and 3 slightly, but a busy coordinator is by definition already looking at state, so the gap matters least when it occurs. A contract rule (Variant 2) should state this limit explicitly. |

#### Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | One phase with concrete operational steps answers the asked question; Variant 2's second phase is useful but out of the question's scope. |
| C-001 | tie (2 and 3) | Both say yes, read-only, which follows the owner's order and the spec's recommended answer "Yes, read-only"; Variant 1 overrides a live order. |
| C-002 | 2 | Moving the rule from the lowest source tier into a checked-in file removes the root cause INV-010 found; the timing of that move is a separate matter. |
| C-003 | tie (2 and 3) | Timer-renewed idle subscriptions cover non-worker peers that never appear in the Orca queue; ad hoc subscriptions (Variant 1) recreate the gap. |
| C-004 | tie (2 and 3) | Ten-minute read-only PR reads catch review comments and CI failures between wakes at modest, read-only cost. |
| C-005 | 3 | Recording the job id and expiry in the ledger and re-creating it is the only concrete answer to the 7-day expiry and session-only life. |
| C-006 | 3 | Silent unless a decision is needed matches the 2026-11-09 order; Variant 2 leaves it open. |
| C-007 | 3 | Naming it UNVERIFIED and bounding it by the 5-minute cap is safe now; Variant 2's contract fix is better long-term but not available during this program. |
| X-001 | tie (2 and 3) | "In force" follows the owner's order; Variant 1's "not in force" overrides it on inference. |
| X-002 | 3 | The question asks about this program's coordinator; binding every coordinator is a larger decision that deserves its own question. |
| X-003 | 3 | Variant 3 adopts the spec's own reading (line 1016: the sentence concerns the `/sc:sweep` duty, not a ban); Variant 2 is right that the text should be fixed, but that fix is not needed to answer Q31. |
| A-001 | tie | No variant addresses staleness; all rely on the owner's answer to confirm it, which is the right mechanism. |
| A-002 | tie | None of the three states the idle-only firing limit; Variant 1 avoids it only by having no cron. |

#### Overall

Variant 2's real contribution (promote the rule into the checked-in contract) is correct but belongs in its own follow-up item rather than in the answer to a question about one program; Variant 3 gives the same behaviour now with better expiry and reporting detail and no added scope.

Overall best answer for the owner: Variant 3, confidence 65%

### Variant 3 Advocate (general-purpose, default model)



#### Position

Variant 3 is the best answer to the question as asked. Q31 asks whether the 2026-11-05 order "appl[ies] to this program's coordinator" (question.md, line 7). Variant 3 answers exactly that: yes, as a read-only check, scoped to this program, with the mechanism limits (7-day cron expiry, session-only life) and the later reporting order (2026-11-09) folded in. It follows the owner's standing order without widening the question into a change to an installed core file, and it closes INV-010 with an owner answer rather than a silent pick, which is why the question exists (question.md, fact 3).

Facts I re-checked read-only for this statement:

- The memory note (modified 2026-11-05) says: "Keep a recurring CronCreate sweep (every ~10 minutes, off-minute) that re-checks the Orca run, ListAgents, open PRs on IronClaude and Coder, and re-subscribes `notify_when_idle` on busy peers", and gives the reason "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all."
- `src/superclaude/core/WORKER-CONTRACT.md:288` (WC-16) says "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." The same paragraph also says "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged."
- `merged-requirements.md` line 579: "Q31 does not authorize `/sc:sweep` above WC-16's cap or any write." The cadence record's last row (line 1026) reads "status is Q31's answer; never runs `/sc:sweep` more often than WC-16 allows and never writes".

#### Steelman of Variant 1

Strongest version: the coordinator's behaviour should be auditable from checked-in files alone. WC-16 is the contract every coordinator signs; it already says "It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it", which directly fixes the failure that caused the 2026-11-05 order (a lapsed wait). The spec already reads each PR "at coordinator wakes with `gh pr view <N> --repo IronbellyOrg/IronClaude`" (line 1025). Once SWEEP-RUNNABLE holds, `/sc:sweep` reports "Person-started sessions ... observed from transcripts and ccsession files" (WC-16), which covers much of what the timer was for. So a second clock adds load, an unverified "is a cron fire a wake" question, and a 7-day expiry hazard, for coverage the contract mostly already gives. Variant 1 is also honest about its cost: it names that it "overrides a standing owner order that exists because of a real failure".

What it gets right: one clock family, no expiry management, and no ambiguity about whether a fire triggers the sweep pass (Variant 1, "What it unlocks"). It is the only variant with zero mechanism risk.

#### Steelman of Variant 2

Strongest version: the real defect INV-010 found is that the order lived only in memory, "so two of three debate drafts wrote 'no extra scheduler' without it" (Variant 2, citing `invariant-probe.md:18`). Answering "yes" for one program leaves the next coordinator in the same trap. Writing the rule into WC-16 fixes it at the source, settles the "Phase 1 adds this duty, not a scheduler" ambiguity in the contract text, and lets the contract say once whether a cron fire is a "coordinator wake". Variant 2 keeps an immediate "yes" for this program, so nothing is lost while the PR is in flight.

What it gets right: it is the only variant that removes the root cause, and it correctly warns that a contract rule naming a 10-minute cron "must also say what happens on expiry and on resume, or it writes a promise the tool cannot keep".

#### Key strengths claimed

1. **Answers the question at the scope asked.** Q31 is about "this program's coordinator" (question.md line 7) and gates only "the status of the last row of the 6.6 cadence record" (question.md, "What it gates"). Variant 3 sets that row to "in force" and stops. It does not turn a W0 intake question into a change to an installed core file.
2. **Follows the owner's order and its reason.** The order exists because non-worker peers "do not appear in the Orca message queue at all" (memory note). This program has such peers: the PR sessions of Q25 and the #539 author of Q33 (Variant 3, "What it unlocks"; Variant 1 concedes the same in its costs).
3. **Handles the mechanism limit concretely.** Only Variant 3 says what to do about the 7-day expiry and session-only life: "records the job id and its expiry in the ledger and re-creates it on expiry or after a resume" (diff-analysis U-002, rated High). Variant 2 only says a future rule "must also say what happens".
4. **Reconciles the two owner orders.** Variant 3 makes routine runs silent and reports only decisions, matching the 2026-11-09 order (memory `orchestration-decision-ledger-only.md`, question.md fact 5). Variant 2 leaves this "unresolved".
5. **Keeps the spec's hard limits.** "No `/sc:sweep` above WC-16's 5-minute cap, no write of any kind, no grant implied" (Variant 3), matching line 579 and line 1026 word for word in substance.
6. **Honest about the open reading.** It names the "is a cron fire a coordinator wake" question as UNVERIFIED and shows the outcome stays inside the cap either way.

#### Weaknesses identified in Variant 1

- It overrides a standing owner order on the strength of a contract sentence that probe INV-010 says is "not a ban on that cron" (question.md fact 3). Answering "no" here is the silent-pick-in-reverse the question was raised to avoid.
- Its coverage argument leans on `/sc:sweep`, but `/sc:sweep` is "not runnable" until SWEEP-RUNNABLE holds (line 1031 note; question.md fact 7). During W0 and until PR #539 merges and Q29's route runs, nothing in WC-16 watches non-worker peers. Variant 1 itself lists "How non-worker peers ... are supervised between their own reports" as unresolved.
- Its PR reads happen "at coordinator wakes"; a coordinator waiting on a quiet Orca Run may not wake for a long time (its own words: "on a quiet day that could be long").
- It says nothing about IronbellyOrg/Coder PRs, which the order names; the existing GitHub row reads only `IronbellyOrg/IronClaude`.

#### Weaknesses identified in Variant 2

- Scope growth beyond the question. It changes `~/.claude/WORKER-CONTRACT.md`, "an installed core file ... that every project using IronClaude receives", through "a question that was framed for one program" (Variant 2's own costs). Q31 gates no work item (dependency edge 101: "Recorded only; they gate no item"); Variant 2 creates one.
- Adds a PR during a program whose stated bottleneck is owner latency (Variant 2 quotes section 3: "Owner latency is the real schedule").
- Writing a 10-minute cron into the contract for every project hard-codes the IronClaude and Coder repo scope, which Variant 2 admits "may be wider than every coordinator needs".
- Leaves reporting style unresolved, so until the contract PR lands the check could produce routine notices the 2026-11-09 order forbids.
- Its immediate "yes" half is the same as Variant 3 but without the expiry and re-creation step, so in practice its interim behaviour is weaker than Variant 3's.

#### Concessions

- **Memory-only rule.** Variant 3's own costs admit the rule "stays in a memory note and a ledger row ... so the next coordinator outside this program may again miss it." Variant 2 fixes this; Variant 3 does not. That is the strongest case against my variant.
- **Silent failure risk.** If the re-creation step is missed after 7 days or a resume, the check "can silently stop" (Variant 3's own costs). A ledger row is a reminder, not a guarantee.
- **Overstated claim.** Variant 3 says "only a timer-driven check sees them go idle". That is too strong: once SWEEP-RUNNABLE holds, WC-16's `/sc:sweep` report includes person-started sessions "observed from transcripts and ccsession files" (WORKER-CONTRACT.md:288). The claim is true only until the sweep is runnable, and only for idle detection by subscription.
- **Ledger write wording.** Line 579 says Q31 authorizes no "write". Variant 3's recording of the job id in the ledger is the coordinator's own local record, not an action of the check, but the text should say so to avoid a reading that it conflicts with line 579.
- **"Never messaged" tension.** WC-16 says person-started sessions "are never messaged". A `notify_when_idle` subscription with no message sends nothing to the peer (SendMessage tool description: "a pure subscription that costs that session nothing"), so I read it as compatible, but the text should state that only message-less subscriptions are used.
- **Idle-only firing (A-002).** Variant 3 does not mention that a session cron fires only while the coordinator is idle, so "about every 10 minutes" is a ceiling on frequency while the coordinator works, not a guarantee.
- **Load.** About 144 read cycles a day, rate limits unmeasured (Variant 3 marks this UNVERIFIED).

#### Shared assumption responses

- **A-001 (the 2026-11-05 order is still current): QUALIFY.** No later source I found withdraws it: the memory index still lists it ("Coordinator never stops polling ... owner order 2026-11-05"). The 2026-11-09 order speaks of "automated orchestration checks", which presupposes such checks exist, so it adjusts reporting rather than cancelling the check. But memory is the lowest source tier and the note is 9 days old, which is exactly why Q31 asks the owner. The owner's answer to Q31 is itself the freshness check, so the assumption is acceptable only because the owner is being asked.
- **A-002 (a session cron fires only while the coordinator is idle): ACCEPT.** The CronCreate description says "Jobs only fire while the REPL is idle (not mid-query)". A busy coordinator delays the check. This mostly matters little: when the coordinator is busy it is already acting and reading state; when it is idle (waiting on Orca), which is when peers go unwatched, the cron fires. Variant 3 should still say it, so nobody treats "about every 10 minutes" as a guarantee.

#### Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | Its operational sub-list (cron, expiry, reporting, limits) is what the coordinator needs to act at W0; Variant 2's second phase is out of scope for this question. |
| C-001 | 3 | "Yes, read-only" (shared with Variant 2) follows the owner order and covers non-worker peers that WC-16 cannot see while `/sc:sweep` is not runnable. |
| C-002 | 3 | Memory plus ledger for this program matches the question's scope; Variant 2's contract change is a broader decision the question was not framed to make, though it fixes the root cause. |
| C-003 | 3 | Timer-renewed subscriptions (shared with Variant 2) are the only listed way to see non-worker peers go idle before SWEEP-RUNNABLE; Variant 1 leaves this unresolved. |
| C-004 | 3 | 10-minute reads cover IronbellyOrg/Coder as the order names and catch PR events between wakes; Variant 1 reads only at wakes and gates. |
| C-005 | 3 | Only Variant 3 gives a concrete expiry and resume procedure; Variant 1 avoids the issue by dropping the check, Variant 2 defers it. |
| C-006 | 3 | Only Variant 3 reconciles the check with the 2026-11-09 reporting order. |
| C-007 | 3 | Names the open reading as UNVERIFIED and shows it stays within the 5-minute cap either way; Variant 2's contract fix would be better long term but is not part of this answer. |
| X-001 | 3 | "In force" (shared with Variant 2) is the status that follows the owner's order; "not in force" overrides it without a newer source. |
| X-002 | 3 | Binding this program only matches "this program's coordinator" in the question. |
| X-003 | 3 | WC-16's sentence describes the `/sc:sweep` duty; probe INV-010 reads it as "not a ban on that cron", and Variant 3 follows that reading. |
| A-001 | 3 | Only Variant 3 engages the later 2026-11-09 order, which is the best evidence that automated checks are still expected; none states the freshness assumption outright. |
| A-002 | tie | None of the three states the idle-only firing limit; Variant 1 sidesteps it only by having no cron. |

#### Overall

Variant 3 gives the owner a direct, in-scope "yes" that follows the standing order, handles the cron's expiry and the later reporting order, and keeps every spec limit; its real weakness is that the rule stays outside the checked-in contract, which the owner can address later with a separate decision, and its text should drop "only a timer-driven check" and state the idle-only firing and message-less subscriptions.

Overall best answer for the owner: Variant 3, confidence 70%

## Scoring Matrix

Per-point verdicts from the three advocates (V1, V2, V3 columns give each advocate's verdict). Majority (at least 2 of 3) decides; a "tie 2 and 3" verdict counts toward either of those variants.

| Diff Point | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|------------|--------|--------|--------|--------|------------|-----------------|
| S-001 | tie | tie | tie | tie | 90% | Same five sections in all three |
| S-002 | 3 | 3 | 3 | Variant 3 | 90% | Operational sub-list is what the coordinator acts on at W0 |
| C-001 | 3 | 2/3 | 3 | Variant 3 (shared with 2) | 90% | "Yes, read-only" follows the owner order and covers non-worker peers; Variant 1 advocate conceded |
| C-002 | 3 | 2 | 3 | Variant 3 | 70% | Scope matches "this program's coordinator"; Variant 2 advocate holds that the contract move fixes the root cause |
| C-003 | 3 | 2/3 | 3 | Variant 3 (shared with 2) | 90% | Timer-renewed subscriptions are the only listed way to see non-worker peers before SWEEP-RUNNABLE |
| C-004 | 3 | 2/3 | 3 | Variant 3 (shared with 2) | 85% | 10-minute reads catch PR events between wakes and include the Coder repo |
| C-005 | 3 | 3 | 3 | Variant 3 | 95% | Only concrete expiry and resume procedure; Variant 2 advocate conceded |
| C-006 | 3 | 3 | 3 | Variant 3 | 95% | Only variant that applies the 2026-11-09 reporting order |
| C-007 | 2 | 3 | 3 | Variant 3 | 65% | Bounded and labelled UNVERIFIED is enough now; Variant 1 advocate prefers the contract fix |
| X-001 | 3 | 2/3 | 3 | Variant 3 (shared with 2) | 90% | "In force" follows the order; "not in force" overrides it without a newer source |
| X-002 | 3 | 3 | 3 | Variant 3 | 95% | Binding every coordinator is a separate decision; Variant 2 advocate conceded |
| X-003 | 3 | 3 | 3 | Variant 3 | 95% | WC-16 sentence concerns the `/sc:sweep` duty, not a ban (spec line 1016, probe INV-010) |
| A-001 | 3 | tie | 3 | Variant 3 | 65% | All QUALIFY: the owner's answer is the freshness check; Variant 3 alone engages the 2026-11-09 order |
| A-002 | 1 | tie | tie | tie | 60% | All ACCEPT; no variant states the idle-only firing limit; Variant 1 avoids it only by having no cron |

Overall votes (each advocate's honest judgment after steelmanning): Variant 3 at 75% (Variant 1's advocate), Variant 3 at 65% (Variant 2's advocate), Variant 3 at 70% (Variant 3's advocate). 3 of 3 agree.

Shared-assumption responses: A-001 QUALIFY x3; A-002 ACCEPT x3. No omissions.

## Convergence Assessment
- Points resolved: 14 of 14 (majority rule)
- Alignment: 100% (unanimous on 8 of 14)
- Threshold: 80%
- Status: CONVERGED
- Unresolved points: none. Residual minority positions: C-002 (Variant 2 advocate: contract move is better), C-007 (Variant 1 advocate: settle the wake question in the contract).

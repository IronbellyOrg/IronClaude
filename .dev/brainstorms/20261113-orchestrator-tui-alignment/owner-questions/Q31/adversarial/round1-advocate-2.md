# Round 1 Advocate Statement: Variant 2 (Proposal B)

## Position

Variant 2 answers "yes, read-only" for this program's coordinator, exactly like Variant 3, and adds one thing: a separate small PR that writes the read-only ten-minute check into the checked-in coordinator rules (WC-16 or the orchestration guide), so it stops resting on a memory note.

The case for it rests on three verified facts:

- The order today lives only in memory. `coordinator-never-stop-polling.md` (modified 2026-11-05) says: "Keep a recurring CronCreate sweep (every ~10 minutes, off-minute) that re-checks the Orca run, ListAgents, open PRs on IronClaude and Coder, and re-subscribes `notify_when_idle` on busy peers."
- The spec itself ranks that source lowest and says so in the cadence record: "owner memory `coordinator-never-stop-polling.md` (2026-11-05 order; lowest source tier, so asked as Q31)" (`merged-requirements.md` line 1026).
- The checked-in contract contains the sentence that caused the confusion: "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." (`WORKER-CONTRACT.md:288`). The spec had to add a note to explain that this "concerns the `/sc:sweep` duty, not a ban on the owner's check" (line 1016). Probe INV-010 (as quoted in `question.md` fact 3) found that two of three drafts read it as "no extra scheduler".

So the defect is in the source text, not only in this program. Variant 3 fixes the symptom for one program; Variant 2 also fixes the cause. Variant 2's immediate behaviour for this program is the same read-only cron as Variant 3, with the same limits from line 579 ("Q31 does not authorize `/sc:sweep` above WC-16's cap or any write").

## Steelman of Variant 1

The strongest version of Variant 1: the coordinator's cadence should be fully described by a reviewed, checked-in file, and WC-16 already says the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it" (`WORKER-CONTRACT.md:288`). That directly answers the failure that produced the 2026-11-05 order (a lapsed wait). A second clock adds load (about 144 reads a day across Orca and two GitHub repos), a 7-day cron expiry to manage, and an open question about whether a cron fire is a "coordinator wake" that triggers the sweep pass. Saying "no" keeps one clock family, auditable from one file, and the spec already reads GitHub at wave gates, before each edit and at wakes (line 1025). Variant 1 also honestly names its own cost: it "overrides a standing owner order that exists because of a real failure."

What it gets right: it is the only variant with zero operational cost, and it correctly values a checked-in source over memory. That second point is the same value Variant 2 acts on.

## Steelman of Variant 3

The strongest version of Variant 3: it answers exactly the question asked (does the order apply to this coordinator) and nothing more, follows the owner's standing order and the reason behind it ("Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all"), and it is the most operationally complete variant. It records the cron job id and its 7-day expiry in the ledger and re-creates it on expiry or resume, which addresses the CronCreate limit ("Recurring tasks auto-expire after 7 days"). It makes routine runs silent per the 2026-11-09 order (`orchestration-decision-ledger-only.md`). It names the "is a cron fire a wake" question as UNVERIFIED and bounds it by the 5-minute cap. It adds no PR and no scope during a program where "Owner latency is the real schedule" (line 523).

What it gets right: everything Variant 2 does for this program, plus two operational details Variant 2 left open (expiry handling in the ledger, silent reporting).

## Key strengths claimed

1. Fixes the root cause, not only the instance. The confusion INV-010 found comes from contract text ("Phase 1 adds this duty, not a scheduler") and from the order living only in memory. Only Variant 2 changes either.
2. Same immediate behaviour as Variant 3 for this program: one off-minute recurring read-only check, the same four reads, never writes, never runs `/sc:sweep` above WC-16's cap (line 579, line 1026).
3. Lets the contract settle in one place whether a cron fire counts as a "coordinator wake" for WC-16, which is UNVERIFIED today (`question.md` fact 6).
4. Raises the source tier of an owner order. A future coordinator outside this program reads the installed contract; it may not read this program's ledger or that memory note.
5. Names its own risk honestly: a contract rule naming a 10-minute cron "must also say what happens on expiry and on resume, or it writes a promise the tool cannot keep."

## Weaknesses identified in Variant 1

- It overrides a live owner order with nothing but the spec's own inference. The memory note is explicit and the reason (non-worker peers are invisible to the Orca queue) is not addressed by WC-16, which watches only the Run.
- It leaves non-worker peers (Q25 PR sessions, the Q33 #539 author) supervised only "when the coordinator subscribes to them for a specific reason", which is the gap that caused the order.
- It treats WC-16 as the complete cadence, but the spec's own cadence record says WC-16's "not a scheduler" sentence "concerns the `/sc:sweep` duty, not a ban on the owner's check" (line 1016). Variant 1 rests on the reading the spec already rejected.
- It does not address A-002 or A-001; it only avoids the cron.

## Weaknesses identified in Variant 3

- It keeps the rule in "a memory note and a ledger row, not in a checked-in file, so the next coordinator outside this program may again miss it" (Variant 3's own words). The same miss INV-010 found will recur.
- It leaves the WC-16 sentence that misled two drafts unchanged, so every future spec must re-add the explanatory note from line 1016.
- It does not settle the "cron fire is a wake" question; it bounds it. That is acceptable for one program but not as a standing rule.
- It does not discuss that a session cron fires only while the coordinator is idle (A-002), though neither does Variant 2.

## Concessions

- Variant 2 grows scope. It edits an installed core file (`~/.claude/WORKER-CONTRACT.md`) that every IronClaude project receives, through a question framed for one program. The question asked is "does it apply to this program's coordinator", and Variant 2 answers more than that. An owner can reasonably say the contract change deserves its own question or issue.
- It adds a PR during a program whose bottleneck is owner latency (line 523).
- Its operational detail for this program is thinner than Variant 3's: it does not say the ledger records the cron job id and expiry, and it leaves open how the check reports (C-006). Variant 3 is better on both.
- A contract rule that names CronCreate inherits a tool that is session-only and expires after 7 days; writing it into a contract before the expiry and resume handling is designed risks a promise the mechanism cannot keep. Variant 2 names this risk but does not solve it.
- The GitHub scope in the order (all open PRs on two repos) may be too wide for every coordinator, so generalizing it is not obviously right.
- The contract PR does not need Q31 to happen. The owner can answer Variant 3 now and open the contract change as a separate item later; that sequencing gets Variant 2's benefit without its scope cost.

## Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001: the 2026-11-05 order still reflects the owner's intent on 2026-11-14 | QUALIFY | The note is 9 days old and the 2026-11-09 order changed how such checks report, not whether they run. Nothing seen supersedes the 2026-11-05 order, and the MEMORY.md index still lists it as current ("owner order 2026-11-05: re-arm the Orca wait after every expiry, keep a cron sweep"). But that is exactly why Q31 is asked: the owner's answer, not the note, should confirm it. Any "yes" should state that it is the owner's fresh confirmation. |
| A-002: a session cron fires only while the coordinator session is idle | ACCEPT | The CronCreate tool description in this session says "Jobs only fire while the REPL is idle (not mid-query)". So "about every 10 minutes" holds only while the coordinator waits; a long busy turn delays the check. This weakens the "within 10 minutes" claim of Variants 2 and 3 slightly, but a busy coordinator is by definition already looking at state, so the gap matters least when it occurs. A contract rule (Variant 2) should state this limit explicitly. |

## Per-point verdicts

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

## Overall

Variant 2's real contribution (promote the rule into the checked-in contract) is correct but belongs in its own follow-up item rather than in the answer to a question about one program; Variant 3 gives the same behaviour now with better expiry and reporting detail and no added scope.

Overall best answer for the owner: Variant 3, confidence 65%

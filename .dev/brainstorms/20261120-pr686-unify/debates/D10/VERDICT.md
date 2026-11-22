# Verdict D10: Wake transport

## Question
How should the poll wake the coordinator: CLAY's wake files, mailbox message, typed line and session start (D:143-237, PR 686 `wake.py`, which copies about 100 lines of `orca_term.py`), the owner's open Coder issue 477 (listener) which CLAY NG-1 rejects, or OURS claim handoff with a launched session? Include the "no GitHub text reaches a typed line" rule as a candidate strength.

(Meaning of the labels, since the question uses project shorthand: "D:nnn" is a line of Clay's merged design `docs/designs/orchestrator.md`; "PR 686" is Clay's rewrite of the poller; Coder issue 477 is the owner's issue for a listener in every workspace; "NG-1" is the non-goal "no push designs"; "the coordinator" is the long-running session that takes work from the poll.)

## Winner
HYBRID: the transport is Clay's durable wake file with an acknowledgment, but with the owner's rules around it (no listener, id-only rule, one-verb start, no copied terminal code) and two mandatory fixes that neither line has today.

## Winning recommendation
The spec must say all of the following (each is testable):

1. **Truth is a file, not a message.** The poll writes one wake file `<orchestrator-repo>/.orchestrator/wakes/<wake_id>.json` (temp file plus rename, mode 0600, at most 64 KiB) before anything is sent. The orchestrator writes `<wake_id>.ack.json`. The poll never writes the acknowledgment. The poll gives a wake 3 deliveries in total (first send plus two resends, 10 minutes apart), then marks the Orca workspace unread and exits 7. The same wording must be used everywhere ("3 deliveries"), because the code allows attempt 1 to 3 and rejects a 4th (`pr-a` `wake.py:468`).
2. **Mailbox message and typed line are nudges only.** Both carry the wake id and nothing else. Losing either costs latency, never a wake. The mailbox send depends on an unverified Orca behavior (U5, D:163), so it must be optional.
3. **The typed line goes only to an idle person-opened session or to a session the poll just started.** Preconditions: idle, empty draft, 60 seconds without output, and the screen tail shows the main input prompt (the last check is new; FR-24 rule 1 already demands it for approvals, D:573). Nothing is ever typed into a session that is busy or waiting in `check --wait`.
4. **The coordinator pulls too.** The orchestrator or coordinator loop reads the wake directory at every return of its bounded `check --wait` (at most once every 5 minutes), takes only wakes whose `target` is itself, and treats files named `*.ack.json`, `*.rejected.json`, temp files and `done/` as non-wakes. This text is not in the design today (D:571 lists only "the state files").
5. **The wake file carries ids only**: `repo`, `number`, `url` (pattern-checked). No issue title, no label, no comment text. The plan-request payload (`plan_requests[]`, with a title) belongs to the plan-hold decision (D09), not to this transport.
6. **The rule "no GitHub text reaches a typed line" is kept, credited to the owner's D3, and widened.** D3 ("only a validated integer issue number reaches a session prompt", `docs/designs/issue-watcher.md:39`, `:49`; `launch.py:33`, `:84-92`) is the origin. The spec states the widened form: only a value built by a pattern-checked builder reaches a prompt, a typed line, a mailbox subject or an argv, and the wake file holds no free GitHub text.
7. **No listener.** Coder issue 477 stays open as the owner narrowed it on 2026-11-13 (Q3: read-only status and identity, no prompt routing). The spec states that the listener is out by the owner's own D1 option A and NG-1, not only by Clay's non-goal.
8. **Session start.** If no live session of the target tag is found, the poll starts one. Preferred route: `orca agent launch` with a second fixed prompt pattern (the wake line), the same one-verb route the owner's claim launch uses, only after a live spike shows it carries the ccsession tag the lookup keys on (U25, D:1283). Until then keep the typed ccsession start. In both routes an unreadable process table means "unknown", not "none": the poll starts nothing while it cannot read the table (`pr-a` `wake.py:609-621`, `:731-744`, `:897-934` start a duplicate today).
9. **No copied terminal code.** One shared Orca terminal helper in the package, with a test that runs it against the same fixtures as the report waker's `orca_term.py`. K16 ("Accepted for now", D:1238) is not accepted; the helper exists before a second consumer ships.
10. **Mandatory condition M1 (acknowledgment after the state file).** The orchestrator lists an assigned item as taken only after that item's per-issue state file exists. Today the order is pinned only for plan requests (D:539), not for assigned items (D:229, D:536), while the poll treats the acknowledgment as final (`pr-a` `cycle.py:777-810`). A crash between the two loses the issue.
11. **Mandatory condition M2 (abandonment is recoverable).** The spec picks one: the poll re-targets an abandoned item to the next orchestrator of the repo with a new wake id, or the abandoned wake stays visible to a named reader. Today an abandoned entry is never woken again (`cycle.py:994`), the ended orchestrator's id stays in the wake file, and a new orchestrator rejects it as `wrong_target` (`route.py:407-413`, `:598-602`; D:220).
12. **The acknowledgment bucket rename** (`taken` to `accepted`, so the transport does not decide who claims) is made only together with both readers and a pinned schema version, with a test that pins the pair across PR A and PR B. Renaming one side leaves every acknowledgment valid but empty (INV-019).
13. **Live-test gate.** The mailbox send from outside any Run (U5), the idle meaning of `tui-idle`, the `orca agent launch` tag spike and the screen-tail precondition are proven in the first live test before the poll is enabled. Both lines are unproven live today (Clay's K11; the owner's `_assumed_shape` fixtures, `issue-watcher.md:33`).

D10 does not decide who claims (the poll's launched claim session, or the orchestrator). The envelope carries plain issue numbers and works with either; the "who claims" topic decides.

## Strongest points
**OURS**
1. The listener is out by the owner's own decisions: D1 option A, NG-1 and "Option A makes ... Coder#477 unnecessary" (`docs/designs/issue-watcher.md:47`, `:55`, `:76`), and Q3 narrowed 477 to read-only with no prompt routing (`owner-answers.md:25`). Clay's design repeats it (D:66). So the listener candidate is dead in both lines.
2. The "no GitHub text" rule is the owner's built and property-tested D3 (`launch.py:33`, `:84-92`, `:95-116`; `issue-watcher.md:39`), which Clay's design calls "the carried-over ... rule in its new form" (D:155).
3. No second copy of terminal code: the master original says "reused, never copied" (`orca_term.py:3`), PR 686's `wake.py` lines 9-12 say it "duplicates that script on purpose", and the design accepts it only "for now" (K16, D:1238). The copy has no parity test, though the `find_orca` and origin copies do (those tests are on master; PR 686 did not add them).

**CLAY**
1. Acknowledged, at-least-once delivery with a loud end: acknowledgment, 3 deliveries, unread mark, exit 7 (D:112; `wake.py:964-981`; K14, D:1236). OURS has only a pending record against a double launch and no signal that the coordinator saw a claim (`issue-watcher.md:23`; conceded by the OURS advocate).
2. It reaches a coordinator that is already running and busy. The design keeps an orchestrator in a `check --wait` loop while any worker runs (D:122), so a typed line alone cannot reach it (D:112). The owner's claim launch starts a separate claim session and does not signal the coordinator (Coder issue 516: "A running coordinator session must then take the claimed issue").
3. Zero model tokens until a session reads a wake, and a down coordinator is started (D:120; `wake.py:897-947`). OURS starts one model session per claim.

## Clay strengths to adopt
- **Durable wake file plus acknowledgment, 3 deliveries, unread mark.** Why: OURS has no way to reach or check a running coordinator (Coder issue 516 gap; Q36 latency was accepted "for now" for approvals only). How: adopt the envelope (`schema`, `wake_id`, `target`, `poll.*`, `attempt`) and the ack mechanics; override two things: titles and `plan_requests[]` are removed (step 5 above) and the acknowledgment waits for the state file (M1).
- **Mailbox message to the target's Run.** Why: it is the only channel that ends a `check --wait` at once. How: keep as optional behind U5; the file read in step 4 is the backstop.
- **Typed line to an idle or just-started session.** Why: it is the first command of a started session and the only nudge for a person-opened idle session (D:319, D:710). How: keep, with the added screen-tail precondition (INV-007), and never to a busy session.
- **Starting a session when none is live.** Why: closes the "nothing starts while the coordinator is down" gap. How: preferred one-verb start after a live spike; never on an unreadable lookup (INV-008).
- **The id-only rule on every channel (typed line, mailbox subject, argv).** Why: wider than the prompt-only D3. How: state it as D3 widened, and extend it to "no free GitHub text in the wake file".
- **The honest register of risks (K11, K14, K16, U5, U25).** Why: lets the live test be planned. How: carry the list into the spec's unverified section.

## Our strengths that must be kept
- No listener, no inbound port, no address registry (D1 option A, NG-1, Q3).
- D3, the integer-only launch prompt, with its tests; the wake line's builder is the same kind of function.
- One Orca verb with a receipt and operation id for starting a session, as the preferred start route.
- No copied code between `wake.py` and `orca_term.py`; one helper plus a parity test.
- The claim launch (`/sc:issue --claim <N> --pipeline none`) for the claim session where the owner's flow keeps it, untouched by D10.
- The live-test gate before anything runs (FU-1) and the "poll writes nothing to GitHub" rule: a wake file is local, so the transport adds no GitHub write (NG-2 unaffected).

## Actions
| Action | Type | Target | Order or dependency |
|--------|------|--------|---------------------|
| Write the 13-point transport section into the unified spec | DOC | the unify spec under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/` | First; depends on the D-claim and D09 topics only for the content of `assigned[]` |
| Keep the wake envelope, ack and delivery code of PR 686 and adapt it: no titles, defer `plan_requests[]`, M1, M2, screen-tail check, unknown-is-not-none lookup, pinned ack schema | PR KEEP-ADAPT | PR 686 (Clay's rewrite of the poller) `wake.py`, `route.py`, `cycle.py` | After the spec; PR 686 stays unmerged until M1 and M2 are in |
| Replace the copied terminal code with one shared helper plus a parity test | PR KEEP-ADAPT | PR 686 `wake.py` lines 603-830 and `orca_term.py` | Before any second consumer; not a follow-up |
| Add the "read the wake directory at every return of `check --wait`" step and the M1 order rule to the orchestrator skill | PR KEEP-ADAPT | PR B (orchestrator skill, not yet written) and `docs/designs/orchestrator.md` (3.5, wave 0, wave 5) | With PR B |
| Amend the merged design text: D:536 (order of ack and state file), D:539 pattern for assigned items, K16 status, wake file without `plan_requests[]` titles | DOC | `docs/designs/orchestrator.md` (merged by PR 681) | After the owner approves this verdict; Clay's merged text is amended by a new PR, not rewritten |
| Run the live spike for U5 (mailbox from outside a Run), `tui-idle` meaning, `orca agent launch` carrying the ccsession tag and prompt | DECISION | owner or the live-test session | Before the poll is enabled |
| Post the already drafted narrowing of Coder issue 477 (read-only status and identity, no prompt routing); issue stays open | DECISION | Coder issue 477 (owner's listener issue); the reply is drafted but not posted per the decision record | Owner's own grant; independent of this debate |
| Decide whether a typed wake line into an idle session is acceptable at all (owner decision 6 covers only worker approvals) | DECISION | owner, one question | Before PR 686 or its adapted form is merged |
| No revert or close needed for this topic | none | none | n/a |

## Implications
- **Watcher.** The poll's new job is writing local wake files and nudging; it writes nothing to GitHub for this transport, so the owner's NG-2 holds. Whether the poll or the orchestrator claims is not settled here. The owner's zero-setup branch (`claim-handoff-planb`) currently launches a claim session and has no wake; it can adopt the envelope after PR 686's shape is settled. Do not build a second transport there.
- **Coordinator.** The coordinator or orchestrator loop gains one duty (read the wake directory at each return of its wait) and one rule (acknowledge after the state file). The coordinator session tag in the wake line is `orchestrator-<short>-<n>` and the line is `/sc:orchestrator --wake <id>`; the owner's naming decision is "coordinator, not orchestrator" and session `COORD-<RepoName>` (Coder issue 516). The tag and command name must be settled by the naming topic before the lookup and the typed line are final.
- **Dashboard and observer.** The only dashboard-visible effect is the Orca "unread" mark with a fixed note; the observer and sweep read no wake file today. Decide in the observability topic whether the wake directory is a read source.
- **Claim pipeline.** Unchanged by D10. `build_claim_prompt` is not called by PR 686's poll; if the owner's line keeps the poll launching claim sessions, the wake carries numbers and the acknowledgment means "received", not "claimed". Coder issues 515 and 516 (cron and coordinator provisioning) give the poll its schedule and its target and are unaffected.
- **What breaks.** Merging PR 686 as it stands would ship a transport where one crash loses an issue (M1) and an abandoned wake cannot be recovered (M2), a title channel into the model, a duplicate-session start on a blind lookup, and a copied terminal helper without a parity test.
- **What the owner must know.** (1) Clay's rejection of the listener is the owner's own decision, so there is nothing to defend on that point. (2) The typed line is not the transport and not the guarantee; it is a nudge. (3) The two HIGH problems exist in Clay's code today and are not caused by the owner's line. (4) Nothing in either line has run live.

## Confidence
75 percent. It would drop below 60 if the live spike shows the mailbox send from outside a Run is refused and the loop-read step cannot be added to the orchestrator skill (then the transport is file-only and the typed line is the only nudge), or if the owner rules that any typed wake line is unacceptable (then only the file and the mailbox remain, and "idle person-opened session" has no nudge). It would rise above 85 once the live spike passes and M1 and M2 are written into the spec.

## Unverified
- U5: a sender outside any Run can post to `run:<id>` (D:163, D:1263).
- U25: ccsession accepts the tag `orchestrator-<short>-<n>` (D:1283); and whether `orca agent launch` can carry that tag and the wake line as its first prompt.
- The meaning of `tui-idle` as "at the main input prompt" (`pr-a` `wake.py:774-790`); the screen-tail precondition is new and untested.
- Whether any live run of the report waker proves the typed-line practice in production (`orca_term.py`, `waker.py` are on master; no run record was read).
- Whether the orchestrator skill's wave 5 will accept the loop-read step (PR B does not exist).
- The effort and location of the shared terminal helper relative to the report skill's move (PR 684 moved it into IronClaude, K16).
- Whether the file-size cap of 64 KiB holds with long repo names (the fault-finder measured 77,271 bytes for a full wake with 139-character names, INV-014; not re-measured by the orchestrator).
- Findings INV-003 to INV-028 other than INV-001, INV-002, INV-007 and INV-008 were taken from the fault-finder agent and not re-read line by line by the orchestrator.
- Rulings 1 to 39 in Clay's `RULINGS.md` and the IronFlow coordinator spec (not read by any source of this debate).

## Debate artifacts
All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/`:
- `position-OURS.md`, `position-CLAY.md`
- `adversarial/merged-output.md` (merged position)
- `adversarial/return-contract.yaml` (worker contract)
- `adversarial/adversarial/diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `invariant-probe.md`, `return-contract.yaml`
- `adversarial/adversarial/round1-advocate-1-ours.md`, `round1-advocate-2-clay.md`, `round2-rebuttal-1-ours.md`, `round2-rebuttal-2-clay.md`
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md` (copies of the position papers)

Process notes: the adversarial skill ran at depth standard with nested agents (two advocates, two rebuttals, one independent fault-finder, one merge-executor). The orchestrator wrote the diff analysis, scoring and plan itself. Scoring is by one evaluator in two passes, not independent agents (`base-selection.md`). The position papers contained three errors that the advocates found and that this verdict does not rely on: "PR 686 adds the parity tests" (they are on master), the stretch of owner decision 6 to a wake line, and Q36 as claim latency. Read-only `gh issue view` calls were made against `IronbellyOrg/Coder` (issues 477, 515, 516) because the topic names Coder issue 477; no write to GitHub or Orca happened.

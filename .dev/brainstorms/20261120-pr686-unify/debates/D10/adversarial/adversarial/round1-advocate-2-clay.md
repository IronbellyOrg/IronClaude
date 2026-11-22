# Round 1 advocate statement: Variant 2 (CLAY), D10 wake transport

Paths: `M` = `/home/coder/.cache/ic-snap-20261120/master`, `A` = `.../pr-a`, `W` = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`. "D:n" = line n of `M/docs/designs/orchestrator.md`. I re-read every line I cite below in this session; items I did not open are marked UNVERIFIED.

## Position summary

The topic is how the poll wakes the coordinator. Clay's line is the only one that has a wake at all: a durable file, an Orca mailbox message, a typed id-only line to an idle session, an acknowledgment, 3 resends, then an unread mark and exit 7 (D:112). Variant 1 launches a separate claim session and then leaves the coordinator to notice the claim "at each gate or wake" (`W/src/superclaude/core/WORKER-CONTRACT.md:291` onward, section "Issue pipeline duties"). Nothing in that line says who sends the wake. Clay's line fills that hole. Clay is weaker on proof, copied code and race risk, and I concede those below.

## Steelman of Variant 1

Strongest version: every new channel is attack surface and a second code path to keep in step with Orca. The owner's poller already launches one claim session through one Orca verb, with a pending record before spawn, an operation id and `--retry-launch` (`A/.../launch.py` and `M/docs/designs/issue-watcher.md:39,49`). The claim leaves plain files (`dispatch.json`, `issue-summary.md`, `next-steps.md`). The coordinator, which already runs `check --wait`, reads them. This keeps the integer-only prompt rule (D3) in one place, drops the listener (`issue-watcher.md:47,55,76`), and asks the owner for nothing new. It is also honest about its own gaps: reply shapes are still assumed fixtures (FU-1), and there is no acknowledgment. What it gets right: Clay's wake is unproven by Clay's own register (K11 D:1233, U5 D:1263, U25 D:1283), `wake.py` lines 9-12 say it "duplicates that script on purpose", and I confirmed no test in `A/tests/issue_watch` references `orca_term` except one comment (`test_wake.py:495`). The dual-copy risk is real.

## Strengths claimed (Variant 2)

1. It answers the question asked. Variant 1's claim session is a different session from the coordinator. `WORKER-CONTRACT.md` (section "Issue pipeline duties") says the coordinator reads `dispatch.json` "at each gate or wake" and "nothing starts while it is down". A claim that lands while the coordinator sits in a long `check --wait` loop is not seen until the next gate. D:122 says the orchestrator "is never idle" while a worker runs, so "wait for the next gate" can mean hours.
2. The mailbox channel is the one that reaches a busy session. D:112 gives the reason: a typed line cannot reach a session busy for hours, and a session blocked in `check --wait` reads a mailbox message at once. Variant 1 has no equivalent.
3. Delivery is checkable. D:112 gives ack file, attempts 2 and 3, `abandoned`, exit 7 and `mark_unread` (`A/.../wake.py:964-981`, which writes only a fixed `issue-watch: <reason>` note). Variant 1 states it has "no acknowledgment loop", so a lost handoff is silent.
4. The typed line to an idle coordinator is practice on master, not an invention. `M/.../agent-work-report/scripts/waker.py:2-16` finds the coordinator session, starts one if none exists, and sends one wake line; `orca_term.py` has `typing_or_fresh` (draft check, line 113) and `is_idle` (line 94); `master/tests/skills/test_agent_work_report.py` covers them.
5. The injection rule is stronger, not weaker. `build_wake_line` refuses anything but a wake id (`A/.../launch.py:96-107`); D:155 and D:234 apply the owner's D3 to the typed line, the mailbox subject and every argv; `test_no_text.py` exists in `A/tests/issue_watch`.
6. No tokens are spent until the coordinator reads the wake (D:120). Variant 1 starts a full Claude session per claim.
7. Down coordinator: D:112 starts one (`wake.py:897-905`, the `no_session` branch). Variant 1 states "nothing starts while it is down".

## Weaknesses identified in Variant 1

1. It does not wake the coordinator. The poll's launch reaches a claim session, not the session that must act (see strength 1). Issue 516 is open and its first lines say the same (title: "Every project in a workspace always has a Coordinator ... running coordinator session"; I read only the header, body UNVERIFIED).
2. "Typed text was dropped by the owner" overreaches. Decision 6 (`owner-answers.md:139`, folder `W/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`) drops typed text as an approval route into a worker's terminal. The contract line "types nothing into a worker's terminal for this flow" is about workers. A wake line goes to the orchestrator, carries an id only, and the owner's own report waker already does this.
3. Cited fact 8 compares unlike things. Screen reading is needed for Clay's typed line, but Clay also has the mailbox path that needs no screen reading; Variant 1's own `launch.py` has the same UNVERIFIED fresh-terminal behaviour (`launch.py:329`, U9) for starting sessions.
4. The Q36 citation (`owner-answers.md:185`) is about approval latency ("approve in coordinator"), not about claim-to-coordinator latency. It does not show the owner accepted the claim-wake gap.
5. "Reused, never copied" (`M/.../orca_term.py:3`) is a rule about the waker inside the IronFlow skill, written before the poll existed. Clay's register records the copy as K16 with a follow-up (D:1238, D:432).
6. Variant 1 itself says the launch path is "not yet proven live". Both lines are unproven; this is not a differentiator.

## Concessions

- Clay's wake is unproven live (K11, U5, U25). If U5 fails, the busy-session path is gone and the typed line alone never reaches a session in `check --wait` (D:163).
- About 100 lines are copied with no parity test for the copy (K16). That is a real maintenance debt.
- The draft and 60-second checks narrow the typing race but do not close it; I found no test of that race (UNVERIFIED).
- `plan_requests[]` carries an issue title in the wake file (`wake.py:103-113`); `clean_title` strips control characters only (`:168-176`). A model reading the file still reads GitHub text.
- Nothing consumes a wake until PR B exists. Variant 1 has a working consumer path today.
- Variant 1 costs fewer moving parts. If the owner prefers latency at gates, Variant 1 is acceptable.

## Shared-assumption responses

- A-001 (the poll must push a signal): QUALIFY. A coordinator could poll the store itself, but a model in `check --wait` only wakes on a mailbox message (D:112), so a self-poll needs a script-only loop that D:122 does not describe. Push is the default; a self-read of the wake file on every resume is a good backstop and Clay's design already makes the file the truth.
- A-002 (Orca screen state is reliable enough): QUALIFY. It is only needed for the typed-line half. The mailbox half and the ack loop do not rely on it. Reliability is unproven (no race test found).
- A-003 (single host): ACCEPT. `WORKER-CONTRACT.md` says "one person-opened coordinator owns every watcher-claimed issue on the host", and the `/proc` lookup (`wake.py:603-621`) is host-local by construction. A multi-host design would need a different transport anyway.
- A-004 (transport separable from the trigger and plan hold): ACCEPT with one caveat. The wake carries ids, but `plan_requests[]` also carries a title, so it is only fully separable if that field is dropped or labelled data-only.

## Per-point verdicts

| Point | Winner | Conf. | One-line evidence |
|---|---|---|---|
| C-001 channel | Variant 2 | 75% | Only it reaches the coordinator; V1 hands off to a claim session (WORKER-CONTRACT section "Issue pipeline duties"). |
| C-002 ack and delivery | Variant 2 | 85% | D:112 ack, 3 resends, unread mark; V1 admits none. |
| C-003 listener 477 | Tie | 95% | Both reject it (`issue-watcher.md:47,55,76`; D:66). |
| C-004 starting a session | Variant 1 | 60% | One Orca verb beats terminal create plus typed ccsession answer (`launch.py` "Session name", U9 UNVERIFIED), but V1's session is the claim, not the coordinator. |
| C-005 copied terminal code | Variant 1 | 75% | `wake.py` header says it duplicates on purpose; no parity test for the copy. |
| C-006 typing into a terminal | Variant 2 | 60% | Decision 6 covers worker approvals; wake line is id-only and matches existing waker practice. |
| C-007 cost per assignment | Variant 2 | 70% | D:120 idle poll costs no tokens; V1 starts a session per claim. |
| C-008 coordinator down | Variant 2 | 70% | `wake.py:897-905` starts one; V1 does nothing. |
| X-001 typed wake proven? | Variant 1 | 55% | Typed wake to the report coordinator exists, but the orchestrator wake has no live run (D:1233, D:1263). Both are right on their half. |
| X-002 where the rule belongs | Variant 2 | 55% | D:155 states it is D3 carried over; V2 extends it to more channels. Not a factual conflict. |
| U-001 owner Q3 and decision 6 | Variant 1 | 60% | Accurate and useful; narrower than claimed (see weakness 2). |
| U-002 launch merged and protected | Variant 1 | 65% | Pending-before-spawn and operation id are real; they protect the claim, not the wake. |
| U-003 durable wake, ack, unread | Variant 2 | 80% | `wake.py:964-981`, D:112, K14 (D:1236). |
| U-004 rule on every channel | Variant 2 | 70% | D:234; title-in-file weakness disclosed (`wake.py:103-113`). |

## Corrections to either paper

- Variant 1, fact 2 and costs: Q36 (`owner-answers.md:185`) is approval latency, not wake latency.
- Variant 1, fact 4: decision 6 is about approvals into a worker terminal; it does not ban an id-only wake line to an orchestrator.
- Variant 1, fact 7: `orca_term.py:3` "reused, never copied" is a note inside the waker skill's script, not a repo-wide rule. The `wake.py` header lines I quoted are correct (lines 9-12 of the module docstring).
- Variant 2, fact 4: the session lookup in `orca_term.py` starts at line 34 (`claude_processes`); D:112 cites 31-58. A one-to-three line drift; `typing_or_fresh` is at line 113 and `is_idle` at line 94, so "`:94-133`" holds.
- Variant 2, fact 1: I did not open `wake.py:313-320` and `:416-530` (UNVERIFIED). Line 46-48 and the 64 KiB cap check out.
- Process note: while verifying I ran one read-only `gh issue view 516` against `IronbellyOrg/Coder`, not `--repo IronbellyOrg/IronClaude` as the brief required. No write happened; I did not repeat it.

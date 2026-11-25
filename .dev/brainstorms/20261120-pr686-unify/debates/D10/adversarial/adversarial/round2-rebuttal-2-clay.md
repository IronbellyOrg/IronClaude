# Round 2 rebuttal: CLAY (Variant 2) on D10

M = /home/coder/.cache/ic-snap-20261120/master, A = .../pr-a. "D:n" = line n of M/docs/designs/orchestrator.md. Lines re-read this round: D:111-116, 145-229, 263, 312-319, 571-572, 710, 748; M `src/superclaude/core/WORKER-CONTRACT.md:101,110`; `tests/issue_watch/` parity files on master.

## (1) Responses to OURS' criticisms

1. Bounded wait (a). ACCEPT in part. The wait is bounded (WC:101 `--timeout-ms 300000`; D:572 and D:748 "at most 240000"), and the coordinator sweeps "after every wake or timeout" (WC:110). So a looping session wakes itself at least every 4 to 5 minutes, and the mailbox buys at most that much latency. It still buys something: a mailbox message ends the wait at once, and the poll runs every 5 minutes (D:120), so without it worst case is about 5 plus 4 minutes. REJECT that the pull is already written. D:571 says the loop reads "the state files", not `wakes/`; I searched D for `wakes/` and found no line that tells wave 5 to scan it on a timeout (D:151, 229, 863 only define the files). The pull exists in OURS' argument, not in the text. Change needed: one line in wave 5 "on each timeout, list `wakes/` for a wake with no `.ack.json`".
2. Typed line is only for a person-opened idle session. ACCEPT, and add one more user: a freshly started session. D:319 step 11 starts a session by typing `ccsession <tag> --tier <t>` and then needs a first command; the wake line is that command. Same for a coordinator that ended after 30 idle minutes (D:710). Inside a loop the line adds nothing and the 60 s quiet check keeps it from firing (D:112).
3. Mailbox depends on U5 (D:163, D:1263). CONCEDE. Under the hybrid it is optional, so U5 failing costs latency only.
4. Copy of terminal code. CONCEDE, and correct my Round 1: I wrote that PR 686 "has" parity tests for `find_orca` and origin. Those files already sit on master (`tests/issue_watch/test_find_orca_parity.py`, `test_origin_parity.py`), so PR 686 added none for the terminal port. K16 stands (D:1238).
5. Retraction. My Round 1 line that issue 516 "says the same" cited only its header; the body is UNVERIFIED. Drop it.
6. Fixtures are `_assumed_shape`. CONCEDE for the typed-line and read paths; I did not re-open them this round. Unproven live either way.

## (b) What is separable from `assigned[]` and `plan_requests[]`

OURS is right that only part is. Separable and worth shipping alone: the envelope (`schema`, `wake_id`, `target`, `poll`, `attempt`; D:167-184), atomic write, mode 0600, 64 KiB cap, the ack file with its buckets (D:229), the unread mark, `build_wake_line`, the session lookup. `assigned[]` is only `repo`, `number`, `assignees`, `first_seen_at`, `checkout_state` (D:185-186 table); it can ride as a plain list of numbers, since it carries no GitHub text. `plan_requests[]` carries the plan hold (D:116, 4.11) and a title; defer it. I withdraw A-004's "ACCEPT": make it QUALIFY, separable for the envelope, not for the two arrays.

## (c) "Who claims"

OURS found a real entanglement. In PR 686 the poll claims nothing: `grep build_claim_prompt` over `A/src` finds no call (confirmed with the orchestrator's note). In Clay's line the orchestrator claims in wave 1 (D:44; DQ3 at D:113, layers 1 and 2). In OURS' line the poll launches `/sc:issue --claim <N>`. Transport does not need to settle it: a wake that lists numbers works with either claimer, because the receiver decides. But the ack buckets `taken/skipped/rejected_items` (D:229) mean "the receiver claimed". Under an owner-line claimer they would mean "received". Keep the transport neutral by naming the bucket `accepted`, and let D-claim decide who claims. UNVERIFIED how many tests pin `taken`.

## (d) Titles in the wake file

CONCEDE. D:200 states titles are "Not in the file, on purpose", except the title of a plan request (also `wake.py:103-113`). `clean_title` strips control characters only (`wake.py:168-176`), so a title is an instruction channel to the model that reads the file, and D:234's rule covers typed lines, subjects and argv, not model reads. The title is not needed: the missing-plan call is `/sc:issue --plan <N>` by number (D:116), and the orchestrator can read the issue itself. Recommendation: no titles in the wake file; keep `repo`, `number`, `url` pattern-checked. Rejecting this would weaken the strongest claim I made (strength 5 in Round 1).

## (e) HYBRID

ACCEPT with three conditions.
1. Truth is the wake file plus ack plus unread mark and exit 7; mailbox and typed line are nudges. I accept this as Clay's own structure restated: D:151 already calls the file "the one source of truth".
2. Wave 5 must scan `wakes/` on each timeout (see (a)); otherwise nudges are not optional.
3. Session start through one fixed-pattern verb: ACCEPT the goal (D:319 uses `terminal create` plus typed `ccsession`, U9 and U25 unverified). It is only workable if `orca agent launch` can carry the ccsession tag and a first prompt `/sc:orchestrator --wake <wake_id>` built by `build_wake_line`. UNVERIFIED. That is a live spike, not a design point. If it fails, keep the current start and say so.
Also ACCEPT: no listener; one shared terminal helper with a parity test in place of the copy (the report skill's `orca_term.py:3` says "reused, never copied"; PR C already moves the report skill, D:432), done before the second consumer ships, not as a follow-up. REJECT: "drop the typed line"; it is the cheap way to give a started session its first command.

## (2) Revised verdicts

| Point | Round 1 | Now | Reason |
|---|---|---|---|
| C-001 | CLAY 75% | CLAY 60% | Bounded wait already covers a looping coordinator, if wave 5 scans `wakes/` (not yet written). |
| C-004 | OURS 60% | OURS 65% | One verb with a tag and prompt, if the spike passes. |
| C-005 | OURS 75% | OURS 80% | Parity tests are not PR 686's; shared helper is the cleaner end state. |
| C-006 | CLAY 60% | CLAY 55% | Decision 6 does not cover wake lines (OURS conceded), but typing is only for idle or fresh sessions. |
| U-004 | CLAY 70% | CLAY 55% | Title in file is not justified; drop it. |
| A-001 | QUALIFY | QUALIFY | Push is for latency under about 4 minutes and for non-looping sessions. |
| A-004 | ACCEPT | QUALIFY | See (b). |
| C-002, C-007, C-008, U-003 | CLAY | CLAY | Not contested by OURS. |

## (3) New evidence

1. D:571 lists "the state files" as wave 5 inputs; no line of D names `wakes/` as a timeout read.
2. D:319 shows a started session needs a first command; D:710 shows orchestrators end after 30 idle minutes, so fresh starts are routine.
3. D:116: the plan call takes a number, so the plan-request title has no consumer.

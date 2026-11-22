# Position paper: CLAY on D10 (wake transport)

Topic: how the poll should wake the coordinator. Author stance: the strongest honest case for Clay's line.
Status: stub, filled below.

Paths are in the read-only exports under `/home/coder/.cache/ic-snap-20261120/` (`master` = origin/master, `pr-a` = PR 686 head 8e5ae29ad). "D:nnn" is a line of `docs/designs/orchestrator.md` (merged by PR 681, the design pull request).

## The claim

The poll should deliver each assignment to the repo's orchestrator as a durable wake: one JSON wake file that holds every fact, one Orca mailbox message and, only when the session is idle, one typed line `/sc:orchestrator --wake <wake_id>`. The orchestrator writes an acknowledgment file; the poll resends up to 3 times, then marks the workspace unread and exits 7. The poll itself claims nothing and carries no GitHub text into a typed line. No listener is built.

## The mechanism

1. Wake file `<orchestrator-repo>/.orchestrator/wakes/<wake_id>.json`, written by temp file and rename, mode 0600, at most 64 KiB, before anything is sent (D:151, D:167).
2. Mailbox message `orca orchestration send --to run:<run id> --type status --subject "orchestrator-wake <wake_id>"` for a session that is busy or blocked in a `check --wait` loop (D:152, D:163).
3. Typed line `/sc:orchestrator --wake <wake_id>` only if the session is idle, has no unsent typing and no output for 60 seconds (D:112, D:159).
4. Acknowledgment `<wake_id>.ack.json` written only by the orchestrator; every item is in exactly one of `taken`, `skipped`, `rejected_items` (D:229). No acknowledgment in 10 minutes: resend, attempt 2 then 3, then `abandoned` and an unread mark (D:112).
5. If no session of the target tag exists, the poll starts one with `ccsession <tag> --tier <tier>` in a terminal of the workspace (D:112).

## Cited facts

1. The wake format is one design that PR A (poll) and PR B (orchestrator skill) both build against, with a closed schema `orchestrator-wake/1`, closed rejection reasons and an idempotent acknowledgment (D:145-236; `pr-a` `src/superclaude/cli/issue_watch/wake.py:46-48`, `:313-320`, `:416-530`).
2. A typed line alone cannot reach a session that is busy for hours; the design keeps the orchestrator in a `check --wait` loop while any worker runs, so the durable channel is the necessary half (D:112; D:122 "it is never idle"). Delivery is at-least-once, with claim idempotence making a repeat harmless (D:112-113).
3. The typed line and the mailbox subject hold the wake id only, matched against `^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$` by `build_wake_line`, which refuses any other input (D:155, D:159; `pr-a` `launch.py:96-107`). No title, label or comment can reach a typed line, and every `gh` or `orca` argument built from a wake field is checked against the same patterns (D:234, guarantee 2). A test file `test_no_text.py` exists in `pr-a/tests/issue_watch/`.
4. The typed-line wake into an idle coordinator is existing practice on master: the report waker (merged by PR 684, the agent-work-report skill move) finds the session "by its running process, never by its title", checks `draft` and fresh output, and sends with a receipt (`master` `src/superclaude/skills/agent-work-report/scripts/orca_term.py:34-58`, `:94-133`; `waker.py:2-16`). The wake design copies "a pattern that runs" (K11, D:1233).
5. A poll with nothing new costs no model tokens: "an idle poll is a script that costs no tokens" (D:120, DQ10).
6. The listener of Coder issue 477 (workspace listener with prompt routing) is rejected in both lines (`issue-watcher.md:47`, `:55`, `:76`; D:66). Clay is not departing from the owner's line on that point.
7. Failure is loud: after 3 unacknowledged attempts the cycle exits 7 and the workspace is marked unread with a fixed note (`wake.py` `mark_unread`, lines 964-981; D:112). K14 "A wake is lost while the session is busy for a long turn" is answered by mailbox plus acknowledgment plus unread mark (D:1236).
8. A down coordinator is not a stop: the poll starts a session when none is live (D:112; `wake.py:897-947`), where our line says "Nothing starts while the coordinator is down" (`issue-watcher.md:43`).

## What it costs

- About 1000 lines in `wake.py` plus the launcher code (PR 686 package total 8,322 lines). About 100 to 150 of them copy `orca_term.py` (D:432; `wake.py:603-621`, `:746-830`), listed as risk K16 (D:1238), "Accepted for now", with consolidation as a follow-up after PR C moves the report skill.
- A second code path to keep in step with the Orca CLI (K19, D:1241).

## What it risks

- The mechanism is unproven on a live system (K11). U5 (a sender in no Run posting to `run:<id>`) is unverified (D:163, D:1263). If the mailbox is refused the design falls back to the typed line alone (D:163), which a busy session never takes.
- Typing into a terminal races with a person: the draft check and the 60 second quiet check narrow the window but do not close it (no source shows a test of that race; UNVERIFIED).
- The copy has no parity test against `orca_term.py`, though PR 686 has one for `find_orca` and the origin check (`pr-a/tests/issue_watch/test_find_orca_parity.py`, `test_origin_parity.py`).
- The plan request carries an issue title inside the wake file (D:185; `wake.py:103-113`). The typed-line rule does not stop a model session from reading it; `clean_title` strips control characters only (`wake.py:168-176`).
- Nothing reads the wake until PR B exists, and the poll stays `enabled: false`.

## What it gets right

- It gives the poll a defined, tested, acknowledged way to reach a coordinator that OURS does not have.
- The durable file is the contract, so a busy, crashed or restarted session loses nothing.
- Its security rule is stated for every channel (typed line, mailbox subject, argv), not only for the prompt.
- It is separable from the contested rules: the transport does not need the assignment-only trigger or the plan hold; it carries ids.


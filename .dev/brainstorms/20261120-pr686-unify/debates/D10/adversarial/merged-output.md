<!-- Provenance: Merged from Variant 2 (CLAY paper, the base) and Variant 1 (OURS) by the sc:adversarial Step 5 merge-executor. It follows refactor-plan.md (10 planned changes), the debate findings (rounds 1, 2, 2.5) and invariant-probe.md. -->
<!-- Base: Variant 2 (CLAY paper) -->
<!-- Merge date: 2026-11-20 -->

<!-- Source: Base (original, modified): title and status lines rewritten because the document is now a merged position, and the "Author stance" line removed because it described Clay's paper only -->
# Merged position: wake transport (HYBRID)

Topic: how the poll should wake the coordinator.
Status: merged position for the spec. It holds only if the two mandatory conditions M1 and M2 (section "Mandatory conditions") are written into the spec.

<!-- Source: Base (original, modified): the path note keeps the base text and adds the Variant 1 path conventions and the meaning of INV, K and U labels, so every citation below resolves -->
Paths are in the read-only exports under `/home/coder/.cache/ic-snap-20261120/` (`master` = origin/master, `pr-a` = PR 686 head 8e5ae29ad). A path with no prefix that came from the owner's line is in the `master` export, and `issue-watcher.md` means `docs/designs/issue-watcher.md`. "D:nnn" is a line of `docs/designs/orchestrator.md` (merged by PR 681, the design pull request). "INV-nnn" is a finding of the invariant probe of this debate (round 2.5). "K" and "U" numbers are entries in the design's own register of risks and unverified items.

## The claim

<!-- Source: Base (original, modified), merged per Change #1: reframed as a HYBRID. Durable file plus acknowledgment is the transport, mailbox and typed line are optional nudges, no listener. "Resends up to 3 times" is worded as 3 deliveries in total so the claim agrees with mechanism step 5 (base step 4: attempt 2, then 3; probe INV-010 supports the count) -->
The poll should deliver each assignment to the repo's orchestrator through a durable wake. The transport is two files: one JSON wake file that holds the issue references (`repo`, `number`, `url`) and an acknowledgment file that only the orchestrator writes. An Orca mailbox message and a typed line `/sc:orchestrator --wake <wake_id>` are optional nudges that point at the wake file. They carry the wake id only, and the file is always written first. The orchestrator reads the wake directory itself and writes the acknowledgment. The poll gives a wake up to 3 deliveries in total (the first send plus two resends), then marks the workspace unread and exits 7. The poll itself claims nothing and carries no GitHub text into a typed line. No listener is built. Two conditions are mandatory: the acknowledgment comes after the state file (M1) and an abandoned wake can be recovered (M2).

<!-- Source: Variant 1 facts 1 and 2 (issue-watcher.md:47, :55, :76; owner decision Q3), merged per Change #2 -->
### No listener, and whose decision that is

The listener of Coder issue 477 (a workspace listener with prompt routing) is not built. That is the owner's decision, not only Clay's. The owner's watcher design chose "D1 option A ... No listener, inbound port or address registry" and the non-goal NG-1 "push designs B/C/D" (`docs/designs/issue-watcher.md:47`, `:76`). It also says option A "makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited" (`issue-watcher.md:55`). Clay's design repeats the rejection as a non-goal (D:66). The owner then narrowed the issue: Q3 "1 Keep and Narrow", "narrow Coder#477 to read-only status and identity with no prompt routing; the issue stays open" (`owner-answers.md:25`, in worktree `claim-handoff-planb`, folder `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`). A listener with prompt routing is therefore wanted by neither line, and this transport needs none.

## The mechanism

<!-- Source: Base (original, modified), merged per Change #6: the wake file carries repo, number and url only; no issue title; plan request payload deferred. Rest of step 1 is base text -->
1. Wake file `<orchestrator-repo>/.orchestrator/wakes/<wake_id>.json`, written by temp file and rename, mode 0600, at most 64 KiB, before anything is sent (D:151, D:167). It carries `repo`, `number` and `url` for each item and no issue title: the plan call takes a number (D:116), and a title is GitHub text that a model would read. The `plan_requests[]` payload belongs to the plan-hold decision (D09), not to this transport.

<!-- Source: Base (original) -->
2. Mailbox message `orca orchestration send --to run:<run id> --type status --subject "orchestrator-wake <wake_id>"` for a session that is busy or blocked in a `check --wait` loop (D:152, D:163).

<!-- Source: Base (original, modified), merged per Change #8: the typed line is a nudge to an idle or freshly started session only, and a screen-tail precondition is added. The first three checks and their citations are base text; the guard-gap evidence is from probe INV-007 -->
3. Typed line `/sc:orchestrator --wake <wake_id>`, a nudge only. It goes to a session that is idle, or to a session the poll has just started. The uses are a person-opened idle session and the first command of a started session (D:319, D:710). It is sent only if all of these hold: the session is idle, has no unsent typing and has had no output for 60 seconds (D:112, D:159), and the tail of its screen shows the main input prompt. The screen check is new here; FR-24 rule 1 already requires the same for approvals (D:573, "the prompt must be the session's current screen"). The first three checks are all that PR 686 and the report waker do today. They read only the draft and the output age (`pr-a` `wake.py:746-772` `_unsafe`; `wake.py:774-790` `_idle` waits for `tui-idle`, whose meaning is UNVERIFIED; `master` `orca_term.py:113-121`). Without the screen check, a session that waits on a permission dialog, an escalation question or an AskUserQuestion has an empty draft and can be quiet for an hour, so the line plus Enter would answer the dialog (INV-007). If any check fails or the screen cannot be read, nothing is typed (`wake.py:762-766`) and the file and the mailbox remain the delivery. The line is never typed into a session that is busy or blocked in `check --wait`; that session gets step 2.

<!-- Source: Base (original, modified): new step inserted per Change #3 (the base had no step where the orchestrator reads the wake directory). Evidence is from probe INV-005 and INV-006; the 5 minute limit is the plan's rule. Later steps are renumbered -->
4. The orchestrator reads the wake directory. Its loop reads `<orchestrator-repo>/.orchestrator/wakes/` at every return of its `check --wait`, not only on timeout, but at most once per 5 minutes, and it takes only wakes whose `target.orchestrator` is itself. Reasons: the design does not write this pull, it lists only "the state files" (D:571). A `check --wait` returns on any message of its types, not only on timeout (master `WORKER-CONTRACT.md:101`, `:103`; D:572), so with workers sending status messages more often than every 4 to 5 minutes a timeout never comes, and if the mailbox nudge is refused (U5, D:163) the wake would never be read. The sweep rule is already "after every wake or timeout" (`WORKER-CONTRACT.md:110`). The target filter is needed because `wakes/` is one folder per orchestrator repo (D:151) and a repo can have several orchestrators (D:112, D:710); a wake for another orchestrator would be rejected as `wrong_target` and written as `<id>.rejected.json` (D:177, D:220; `wake.py:493-496`; INV-006). PR B (the orchestrator skill) does not exist yet, so none of this is built (UNVERIFIED that it will be).

<!-- Source: Base (original, modified), merged per Change #4 (HIGH INV-001): the base's "written only by the orchestrator, every item in exactly one bucket, 10 minute resend, attempt 2 then 3, abandoned" is kept; the ordering rule, the bucket-name rule and the pointer to M2 are added -->
5. Acknowledgment `<wake_id>.ack.json`, written only by the orchestrator; every item is in exactly one of `taken`, `skipped`, `rejected_items` (D:229). Ordering rule (M1): the orchestrator lists an assigned item as `taken` only after that item's per-issue state file exists; this holds for every assigned item, not only for plan requests. No acknowledgment in 10 minutes: resend, delivery 2 then 3, then the entry is `abandoned` and the workspace gets an unread mark (D:112). What happens to an abandoned wake is rule M2. The poll reads the bucket `taken` today (`wake.py:565`); the bucket is renamed (the debate consensus calls it `accepted`) only together with both readers and a pinned schema version (see "What it costs").

<!-- Source: Base (original, modified), merged per Change #9: session start through one fixed-pattern verb if a live spike passes, else the base's typed start; no start on an unreadable lookup. Base text kept: start with ccsession in a terminal of the workspace (D:112) -->
6. Session start. If the process lookup finds no live session of the target tag, the poll starts one. Preferred route: `orca agent launch` with a second fixed prompt pattern for the wake line, the same one-verb route the owner's claim launch uses (`master` `launch.py:84-92`, `:95-116`). It is allowed only if a live spike shows that it carries the ccsession tag the lookup needs (U25, D:1283; the lookup keys on `ORCA_TERMINAL_HANDLE` and `CLAUDE_TOPIC`, `wake.py:609-621`, `:743`). Until that spike passes, keep the typed start: `ccsession <tag> --tier <tier>` in a terminal of the workspace (D:112; `pr-a` `launch.py:367-427`). That route reads the ccsession name question "Session name" from a fresh terminal (`pr-a` `launch.py:50-51`), and the docstring of `OrcaLauncher` in the same file marks that behaviour UNVERIFIED. In both routes an unreadable process table means "unknown", not "none", and the poll starts nothing while the lookup is blind. Today `wake.py:609-621` skips every process whose environ or cmdline it cannot read, `wake.py:731-744` turns that into an empty live list and `wake.py:897-934` starts a second session with the same tag on every cycle (INV-008).

<!-- Source: Invariant probe INV-001 and INV-002 (both HIGH), merged per Change #4 and Change #5; the section itself is added at the orchestrator's request (task text) so the two HIGH invariants are explicit mandatory conditions -->
## Mandatory conditions

These are conditions on adopting this transport. PR 686 has neither rule (plan risk summary). If either cannot be written into the spec, the statement that a busy, crashed or restarted session loses nothing (section "What it gets right") does not hold.

### M1: the acknowledgment comes after the state file (INV-001)

<!-- Source: Invariant probe INV-001, merged per Change #4 -->
The orchestrator writes an acknowledgment that lists an item as taken only after the per-issue state file for that item exists, for every assigned item. Today the order "record first, acknowledgment second" is pinned only for plan requests (D:539, D:657). For assigned items D:229 says the acknowledgment is written "when wave 0 has decided every item", and D:536 lists the acknowledgment and the O_EXCL state file as two end conditions with no order between them. The restart rule resumes only `in_progress` files (D:538). The poll acts on the acknowledgment at once: it marks the entry acknowledged (`pr-a` `cycle.py:777-787`), moves the wake and the acknowledgment to `done/`, outside any scan (`cycle.py:805-810`; `wake.py:584-597`), and never wakes the entry again (`cycle.py:994`, "acknowledged ... never woken again"). So a crash between the acknowledgment and the state file loses the issue with no further signal. Renaming the bucket to `accepted` makes the acknowledgment mean "received", which removes the last implied link to a durable take, so the order rule must be written down either way.

### M2: abandonment is recoverable (INV-002)

<!-- Source: Invariant probe INV-002, merged per Change #5 -->
The spec must say what happens to a wake whose entry ran out of deliveries. It must pick one of two outcomes: the poll re-targets the abandoned item to the next orchestrator of the repo with a new wake id, or the abandoned wake stays visible to a named reader. This position does not pick between them. This is spec text only; no code is decided in this debate. Today neither exists: an entry is abandoned after 3 deliveries (`pr-a` `record.py:891-900`) and `cycle.py:994` never wakes an abandoned entry again; only a manual reset removes it (`record.py:971-985`). In the same cycle `in_flight` does not count abandoned entries (`route.py:407-413`), so an active orchestrator with no live session is marked ended (`route.py:598-602`, called at `cycle.py:1427-1429`). The abandoned wake files stay in `wakes/` with `target.orchestrator` set to the ended id, and any new orchestrator rejects them as `wrong_target` (D:220; `wake.py:493-496`), so the directory read in mechanism step 4 cannot recover them. The only trace is exit 7 and one unread note.

## Cited facts

<!-- Source: Base (original) -->
1. The wake format is one design that PR A (poll) and PR B (orchestrator skill) both build against, with a closed schema `orchestrator-wake/1`, closed rejection reasons and an idempotent acknowledgment (D:145-236; `pr-a` `src/superclaude/cli/issue_watch/wake.py:46-48`, `:313-320`, `:416-530`).

<!-- Source: Base (original) -->
2. A typed line alone cannot reach a session that is busy for hours; the design keeps the orchestrator in a `check --wait` loop while any worker runs, so the durable channel is the necessary half (D:112; D:122 "it is never idle"). Delivery is at-least-once, with claim idempotence making a repeat harmless (D:112-113).

<!-- Source: Base (original) -->
3. The typed line and the mailbox subject hold the wake id only, matched against `^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$` by `build_wake_line`, which refuses any other input (D:155, D:159; `pr-a` `launch.py:96-107`). No title, label or comment can reach a typed line, and every `gh` or `orca` argument built from a wake field is checked against the same patterns (D:234, guarantee 2). A test file `test_no_text.py` exists in `pr-a/tests/issue_watch/`.

<!-- Source: Base (original, modified), merged per Change #8: adds that the existing practice checks only draft and output age, so the added screen-tail precondition of mechanism step 3 is not part of that practice -->
4. The typed-line wake into an idle coordinator is existing practice on master: the report waker (merged by PR 684, the agent-work-report skill move) finds the session "by its running process, never by its title", checks `draft` and fresh output, and sends with a receipt (`master` `src/superclaude/skills/agent-work-report/scripts/orca_term.py:34-58`, `:94-133`; `waker.py:2-16`). The wake design copies "a pattern that runs" (K11, D:1233). That practice checks only the draft and the output age (`orca_term.py:113-121`), which is why mechanism step 3 adds the screen-tail check.

<!-- Source: Base (original) -->
5. A poll with nothing new costs no model tokens: "an idle poll is a script that costs no tokens" (D:120, DQ10).

<!-- Source: Base (original, modified), merged per Change #2: the credit for rejecting the listener now goes to the owner's D1 option A and NG-1, and the base's reference to Clay departing from the owner is replaced by a pointer to the no-listener subsection -->
6. The listener of Coder issue 477 (workspace listener with prompt routing) is rejected in both lines (`issue-watcher.md:47`, `:55`, `:76`; D:66), and the rejection is the owner's decision first (see "No listener, and whose decision that is").

<!-- Source: Base (original) -->
7. Failure is loud: after 3 unacknowledged attempts the cycle exits 7 and the workspace is marked unread with a fixed note (`wake.py` `mark_unread`, lines 964-981; D:112). K14 "A wake is lost while the session is busy for a long turn" is answered by mailbox plus acknowledgment plus unread mark (D:1236).

<!-- Source: Base (original, modified), merged per Change #9: the start happens only when the lookup could be read; "our line" reworded to "the owner's claim line" because the document is no longer Clay's paper -->
8. A down coordinator is not a stop: the poll starts a session when none is live and the lookup could be read (D:112; `wake.py:897-947`; mechanism step 6), where the owner's claim line says "Nothing starts while the coordinator is down" (`issue-watcher.md:43`).

## What it costs

<!-- Source: Base (original) -->
- About 1000 lines in `wake.py` plus the launcher code (PR 686 package total 8,322 lines).

<!-- Source: Base (original, modified), merged per Change #10 and Variant 1 fact 7: the base accepted the copy of the terminal code "for now"; this position does not. One shared helper with a parity test replaces the copy -->
- The terminal code is not copied. PR 686 copies about 100 to 150 lines of `orca_term.py` (D:432; `wake.py:603-621`, `:746-830`); `wake.py` lines 9-12 say it "duplicates that script on purpose" (`claude_processes`, `typing_or_fresh`, `is_idle`, `send`), while master `orca_term.py:3` says "Shared by the waker (FR-26: reused, never copied)". The design's register lists this as risk K16 (D:1238), "Accepted for now", with consolidation as a follow-up after PR C moves the report skill. This position does not accept it. No copy of `orca_term.py` ships to a second consumer: the package holds one helper, with a test that runs it against the same fixtures as the report waker. PR 686 has parity tests for `find_orca` and the origin check (`test_find_orca_parity.py`, `test_origin_parity.py`) but none for the copy: in `pr-a/tests/issue_watch` the word `orca_term` appears only in a comment (`test_wake.py:495`). The cost is moving the copy into the helper and writing that test; its size and where the helper lives relative to PR C are UNVERIFIED.

<!-- Source: Base (original, modified): K19 line kept; the clause about one shared helper follows from Change #10 -->
- A second code path to keep in step with the Orca CLI (K19, D:1241). With one shared helper this stays one copy for the terminal functions.

<!-- Source: Base (original, modified), merged per Change #10 (INV-019): the acknowledgment bucket rename needs a pinned pair of readers -->
- The acknowledgment bucket name is shared by two PRs. `wake.py:565` reads `ack["taken"]` with a default of an empty list, and `ACK_SCHEMA` stays `orchestrator-wake-ack/1` (`wake.py:47`). An item with no bucket entry stays undecided and is resent (`cycle.py:777-784`). If PR B writes `accepted` and the poll still reads `taken` (or the reverse), every acknowledgment parses as valid but empty, and a working orchestrator gets three deliveries, an abandonment, exit 7 and an unread mark. So the rename is made only together with both readers and a pinned schema version, with a test that pins the pair across the two PRs.

<!-- Source: Base (original, modified), merged per Change #3: PR B takes a new loop duty -->
- PR B takes a new duty in the orchestrator loop (mechanism step 4).

## What it risks

<!-- Source: Base (original) -->
- The mechanism is unproven on a live system (K11). U5 (a sender in no Run posting to `run:<id>`) is unverified (D:163, D:1263). If the mailbox is refused the design falls back to the typed line alone (D:163), which a busy session never takes.

<!-- Source: Base (original, modified), merged per Change #8: the dialog case from INV-007 is added and the pointer to mechanism step 3; the original race sentence and its UNVERIFIED mark are kept -->
- Typing into a terminal races with a person: the draft check and the 60 second quiet check narrow the window but do not close it (no source shows a test of that race; UNVERIFIED). A second gap is a session waiting on a dialog or a question; the screen-tail precondition of mechanism step 3 is meant to close it, and it has not been tried on a live system (UNVERIFIED).

<!-- Source: Base (original, modified), merged per Change #6: replaces the base's title risk. The base bullet said the plan request carries an issue title inside the wake file (D:185; wake.py:103-113) and that clean_title strips control characters only (wake.py:168-176). Probe INV-017 supplies the "only title path" evidence -->
- Issue titles. PR 686 as it stands still has a title path: `PlanRequestItem` (`wake.py:102-113`; D:185), cleaned by `clean_title`, which strips control characters only (`wake.py:168-176`). The typed-line rule does not stop a model session from reading that text. The merged position removes titles from the wake file and defers `plan_requests[]` to the plan-hold decision (mechanism step 1); until PR 686 follows, this risk stays open. `PlanRequestItem` is the only title path; `repo`, `number` and the pattern-checked `url` remain (`wake.py:73-75`, `:388-389`).

<!-- Source: Invariant probe INV-001, merged per Change #4: risk entry that points to M1 -->
- A crash between the acknowledgment and the state file loses an issue unless M1 is in the spec.

<!-- Source: Invariant probe INV-002, merged per Change #5 -->
- Abandoned wakes cannot be recovered today (M2). An entry that used its 3 deliveries is never woken again, its wake file names an orchestrator that can be marked ended, and a new orchestrator rejects it as `wrong_target`. The spec must name either a re-target with a new wake id or a named reader before this transport is called loud and recoverable.

<!-- Source: Invariant probe INV-008, merged per Change #9 -->
- A blind process lookup starts duplicate sessions and terminals every cycle unless "unknown" is kept apart from "none" (mechanism step 6). The live spike for the one-verb start is not done (UNVERIFIED).

<!-- Source: Base (original) -->
- Nothing reads the wake until PR B exists, and the poll stays `enabled: false`.

## What it gets right

<!-- Source: Base (original, modified): "that OURS does not have" reworded to name the owner's claim-launch line, with its two gaps taken from Variant 1 "What it costs" -->
- It gives the poll a defined, tested, acknowledged way to reach a coordinator that the owner's claim-launch line does not have. That line has no push signal to a running coordinator and no acknowledgment loop.

<!-- Source: Base (original, modified): the "loses nothing" claim is now conditional on M1 and M2, because probe INV-001 and INV-002 show it is false without them -->
- The durable file is the contract, so a busy, crashed or restarted session loses nothing, provided M1 and M2 are in the spec.

<!-- Source: Variant 1 fact 3 (owner's D3, issue-watcher.md:39, :49; launch.py:33, :84-92, :95-116), merged per Change #7. Base wording on the wider scope is kept -->
- Its security rule is stated for every channel (typed line, mailbox subject, argv), not only for the prompt. The rule is the owner's D3, "only a validated integer issue number reaches a session prompt" (`issue-watcher.md:39`, `:49`), built and tested on master in `PROMPT_PATTERN` and `build_claim_prompt` (`master` `launch.py:33`, `:84-92`), with `launch_argv` refusing any other prompt (`launch.py:95-116`). Clay's design calls its own version "the carried-over ... rule in its new form" (D:155). Clay's version widens the rule from the prompt to the typed line, the mailbox subject and every argv built from a wake field (D:234, guarantee 2).

<!-- Source: Base (original) -->
- It is separable from the contested rules: the transport does not need the assignment-only trigger or the plan hold; it carries ids.

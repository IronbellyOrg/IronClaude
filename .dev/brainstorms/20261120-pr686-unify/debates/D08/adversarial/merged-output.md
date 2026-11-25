<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, one noun "coordinator") -->
<!-- Merge date: 2026-11-20 -->

# D08 merged position: one name for the role, one for the command, one family

<!-- Source: Base (original, modified): claim rewritten as a layered scheme -->
## Claim

The session role is **coordinator**. The command is **`/sc:coordinator`** and the skill is `sc-coordinator-protocol`. "Orchestrator" is not the name of any session in this system. Authority differences are carried by two named kinds of coordinator and by a recorded authorization, never by a second noun.

<!-- Source: Variant 2 (CLAY), D:799 and ADD1, merged per Change #2 -->
## Kinds of coordinator

| Kind | Meaning | Source |
|---|---|---|
| person-opened coordinator | A session a person opened (or launched through Orca and watched, Q26); today's WORKER-CONTRACT section 4 | `WORKER-CONTRACT.md:70`, pinned phrase "coordinator is person-opened" (`tests/core/test_orca_session_launch_guidance.py:33`) |
| standing-grant coordinator | Started or restarted by a script under an owner-recorded authorization; holds the grants that authorization names | D:799; D06 verdict items 6 and 7 |
| project coordinator | One per project, session `COORD-<RepoName>`, branch and worktree `Coordinator` | R9 line 40, R10 line 41 |
| all-sessions coordinator | The role issue 339 asks for | 339 title and body |
| sub-coordinator | Issue 444's `--sub`, evaluation only (WC-13 bars worker fan-out) | 444 |
| report coordinator | The single daily and living-report session | 655 "report coordinator"; `agent-work-report/config.json:11-12` |

<!-- Source: Variant 2 (CLAY), D:133, merged per Change #1 -->
## Command, skill, session, tag

- Command `/sc:coordinator`; flags `--wake <wake_id>`, `--hourly`, `--resume`, `--take <owner/repo#N>`, `--sub` (evaluation only).
- A call with no flag is person-opened mode. It creates no grant and starts no merge (test required).
- Authority comes only from a recorded owner authorization (the per-issue grant row, or the authorization the launch prompt cites). Flags choose what the session does; the authorization decides what it may do. The owner's R17 launch-prompt start is a `--wake` or `--take` call, so there is one door.
- Session name and ccsession tag: `COORD-<RepoName>` (32 characters at most, `launch.py:39`). Whether the tag is `COORD-<RepoName>` or `COORD-<short>` is checked against ccsession first (U25).
- Report session: tag `coordinator`, automation prefix `coordinator-`, state `.dev/coordinator/` unchanged.
- Branch and worktree for the project coordinator: `Coordinator` (R10). The shared records branch of Q26 stays `coordinators`. They are different things with different jobs; the spec says so in one sentence.

<!-- Source: Variant 2 (CLAY), merged per Change #4 -->
## Process and layer names

- **Orchestrated issue flow**: the process (claim, plan check, handoff, watch, merge by the person's go, closeout, audit). Folder `.dev/coordinator/orchestrated/` unchanged.
- **Orchestration**: Orca's layer (`orca orchestration`, the `orchestration` skill).

## Persisted names renamed before PR 686 merges
`orchestrator-wake/1` and `orchestrator-wake-ack/1` to `coordinator-wake/1` and `coordinator-wake-ack/1`; mailbox kind `orchestrator-wake`; key `orchestrator_tier` to `coordinator_tier`; `orchestrators.json` and `.orchestrator/` replaced (D07 removes the registry; state goes under `.dev/coordinator/` or the project-local layout D07 fixes); golden fixture `orchestrator_wake_golden.json`; typed line `/sc:orchestrator --wake <id>` to `/sc:coordinator --wake <id>`; design-only verbs `superclaude orchestrator <verb>` to `superclaude coordinator <verb>`. Kept: `IronOrchestrator` and `orchestrator_repo` only if D07 keeps any registry repo; D07 removes it, so they go as well.

<!-- Source: Variant 2 (CLAY), merged per Change #5 -->
## Nesting of the issues

| Item | Place in the family |
|---|---|
| 339 (Orchestrator, run and manage ALL sessions) | The all-sessions coordinator; phase 1 (sweep) is built |
| 423 (Orchestrator v2, proactive holistic) | A knowledge layer over coordinators, not a role; later release |
| 444 (`--sub`) | The sub-coordinator; evaluation only |
| 655 and Clay's design (PR 686, design PR 681) | The standing-grant project coordinator, reached by `/sc:coordinator --wake` |
| Report session | The report coordinator |
Titles of 339, 423, 444 and 655 stay as written (no GitHub edits here). A glossary line says: "In an issue title, 'orchestrator' means the program or epic whose session role is the coordinator; 'orchestration' is Orca's layer."

## Where the word "orchestrator" may appear in new text
(a) Orca's layer and commands; (b) the existing parent-session meaning in the 63 installed skill, command and agent files, unchanged; (c) exact quotes of issue titles and the glossary line; (d) "orchestrated issue flow". Nothing else about this system. A pinned test scoped to the new files enforces it (feasibility UNVERIFIED).

<!-- Source: Base (original, modified): corrections -->
## Corrections carried over from the debate
IronOrchestrator is not an identifier in PR 686 src or tests; `orchestrator_tier` is 15 lines; R10's reach to the command name rests on R9, R10 and R17 together plus the ORCH- to COORD- session rename; the rename is cheap only until PR 686 merges.

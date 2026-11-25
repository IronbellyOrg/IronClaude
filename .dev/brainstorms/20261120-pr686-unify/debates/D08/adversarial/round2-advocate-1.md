# D08 Round 2: Advocate 1 (OURS, "coordinator")

Read-only except this file. Keys as in Round 1; "A2" = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/adversarial/round1-advocate-2.md. Snapshots: master = /home/coder/.cache/ic-snap-20261120/master, pr-a = /home/coder/.cache/ic-snap-20261120/pr-a. No GitHub or Orca writes.

## Response to criticisms

Steelman of Advocate 2's best point first: a name is cheap to change until PR 686 merges and costly afterwards, because wire strings, a config key, a tag and a state folder get persisted (A2 weakness 7, strength 6). Deciding in this round matters more than which word wins. I agree.

| A2 criticism | Response |
|---|---|
| W1 nesting table missing | Conceded in Round 1. The final table is below. |
| W2 "contract says coordinator only" is incomplete | Conceded and verified. Master `src/superclaude/core/CLAUDE.md:58` and `skills/ccsession-tag/README.md:423` say "A supervised orchestrator's coordinator is person-opened". ccsession README lines 285, 387, 513, 525 use "an orchestrator" for a session that starts workers (all four read). Master root `CLAUDE.md:303` and `:334` ("it is the orchestrator that creates the worktrees") too. (A2 wrote "CLAUDE.md:303/334"; that is the repository root file, not `core/CLAUDE.md`, which has one hit, line 58.) My Round 1 strength 3 used line 58; I did not count the other sites in the cost and now do. They are text edits plus one pinned test (New evidence 1). |
| W3 pinned sentence "coordinator is person-opened" | Valid cost item. I cited the test in Round 1 but did not list it as a cost. With A2's species term "person-opened coordinator" the pinned words stay true for that kind. |
| W4 wrong citation (OPEN-DEC and Q26 say "a person opens") | Partly. My Round 1 strength 1 already rested on R9 and R17 and said the Q26 point is an open owner question. I accept A2's dated chain: OPEN-DEC and Q26 (person-opened, to 2026-11-17), then R9, R10, R17 (2026-11-18, widening to template-started). |
| W5 report-session rename | Conceded in Round 1. |
| W6 no name for several sessions per repo | Accepted. D:1157 (OD6, "Decided", rulings 1 and 8) says issue work runs "in one orchestrator per repo, at most 3 issues in flight each, with another orchestrator for the repo when it has more". Several per repo is an owner ruling, not only Clay's idea. The naming below covers it. |
| W7 "cheap until merge" | Accepted. It is also my reason to settle all persisted names now. |

## Updated assessment of Variant 2 and of A2's hybrid

**Accept from A2:**
- Species terms "person-opened coordinator" and "standing-grant coordinator" (point 4).
- `COORD-<RepoName>` first and `COORD-<RepoName>-<n>` extras, as both session name and ccsession tag (point 1).
- Wire strings renamed before merge: `coordinator-wake/1`, `coordinator-wake-ack/1` (point 2).
- The process name "orchestrated issue flow" and the existing `orchestrated/` folder (point 5).
- "Report coordinator" with tag `coordinator` and prefix `coordinator-` unchanged (point 3).
- Clay's flags `--wake`, `--hourly`, `--resume`, `--take` unchanged.

**Withdraw from my Round 1:** the tag `coord-<short>-<n>`, the optional "keep machinery names" carve-out, and the terms "attended" and "standing".

**Still reject:**
- The word "orchestrator" for any session, tag, schema, key or folder, and the command `/sc:orchestrator`. Variant 2 still shows no capability the layered scheme lacks. R9, R10, R17 and the owner's ORCH- to COORD- change decide the word.
- A2's "host coordinator" for 339 (point 5).

## New evidence (all read by me)

1. **Master line 58 and the pin (as asked).** `src/superclaude/core/CLAUDE.md:58` reads "creates a worktree owns its agent(s). A supervised orchestrator's coordinator is person-opened;". The same sentence is at `src/superclaude/skills/ccsession-tag/README.md:423` and is quoted in `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (grep matches at lines 188, 326, 715, 2157; I did not read their context). It is **not** in the plugin mirror: a grep of `master/plugins` for "supervised orchestrator" and "person-opened" finds only `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh:355` ("A supervised coordinator is person-opened;"), so the mirror has only the coordinator wording. Test `tests/core/test_orca_session_launch_guidance.py`: line 33 requires the string "coordinator is person-opened" in both copies (`core/CLAUDE.md`, `ccsession-tag/README.md`); line 36 asserts "coordinator under another orchestrator" is absent from the section; line 53 (a second test) asserts the appended paragraph contains both "orchestrator" and "coordinator". In `core/CLAUDE.md` lines 50-64 the only "orchestrator" is the one on line 58, so editing that sentence to drop the word also breaks line 53, and the test must change in the same PR.
2. **The ccsession tag pattern allows the owner's casing.** pr-a `src/superclaude/cli/issue_watch/launch.py:39`: `TAG_PATTERN = [A-Za-z0-9][A-Za-z0-9._-]{0,31}` (32 characters at most, uppercase allowed). `COORD-IronClaude` and `COORD-IronClaude-2` are valid tags. My Round 1 `coord-<short>-<n>` was an invention that matched neither the owner's casing nor Clay's lowercase `<short>`.
3. **The `superclaude orchestrator` verbs are not built in pr-a.** `ls pr-a/src/superclaude/cli` shows no `orchestrator` folder (`issue_watch` and others only). The verbs exist in the design and in issue 655 section 4 only. Renaming them costs no code.
4. **What pr-a persists under the word:** schema strings `orchestrator-wake/1` and `orchestrator-wake-ack/1` (`wake.py:46-47`, pinned in `tests/issue_watch/test_wake.py:121,188,430,461`); the Orca mailbox kind and subject `orchestrator-wake` (`test_wake.py:562,565`); the config key `orchestrator_tier` (`repos.py:8,43,88,103`, a key users write in `repos.yaml`); `orchestrators.json` and the `.orchestrator/` state and wakes folder (route, wake, cycle, record, cli); and the tag in `test_launch.py:98-99`. The typed line `/sc:orchestrator --wake <id>` is a code constant (`launch.py`, around line 105). Master persists none of these today: a search of master src, tests and docs for `orchestrator-wake`, `.orchestrator/` and `orchestrators.json` finds only `docs/designs/orchestrator.md`.
5. **Persisted on master today under the flow root word:** `agent-work-report/scripts/common.py:134` writes living-report entries to `.dev/coordinator/orchestrated/<owner>__<repo>__<number>.json`. That folder is the one name containing "orchestrat" already on master.
6. **Report session (point 3):** `agent-work-report/config.json:11-12` is `"session_tag": "coordinator"` and `"automation_prefix": "coordinator-"` (read). `waker.py:172` `start_session` starts `ccsession coordinator` in a workspace and has no worktree path.
7. **OD6 (D:1157)** is "Decided" and keeps the report session `coordinator` as one separate session. D:122 (DQ12) says the report session and the orchestrators run in the orchestrator repo's Orca workspace.

## Remaining disputes and my decision on each

**(1) Per-session identifiers: decided for A2.** Session name and ccsession tag are one string: `COORD-<RepoName>` for the first and `COORD-<RepoName>-<n>` for extras. Reason: R9 gives the owner's name, the pattern allows it (evidence 2), and one string removes a second identifier. It does not clash with the report tag `coordinator` (different case, no shared prefix match in any code I found). Limit: 32 characters in all, so `<RepoName>` is cut at 23 characters when `-<n>` has two digits (6 for `COORD-`, 3 for `-<n>`); two repos whose cut names are equal must be refused, as the design does for `<short>` (D:704, which I read in Round 1). UNVERIFIED: that the owner's `COORD-<RepoName>` is a ccsession tag and not only an Orca terminal name (Coder 516 unread).

**(2) Machinery names: rename everything that names a session or the wake contract before merge; keep names of the home repo.** Judged by what is persisted (evidence 3 to 5):
- Rename (persisted in wake files, mailbox, user config or state): `orchestrator-wake/1` to `coordinator-wake/1` and the ack; mailbox kind and subject; `orchestrator_tier` to `coordinator_tier`; `orchestrators.json` to `coordinators.json`; the `.orchestrator/` state and wakes folder to a folder under `.dev/coordinator/` (A2's position; the subfolder layout is a build choice, and the existing `orchestrated/` entries stay where `common.py:134` puts them); the golden fixture to `coordinator_wake_golden.json`. These cost nothing on master because none is merged.
- Rename (code only): the typed line `/sc:coordinator --wake <id>`, test names, and the 12 design-only verbs, which become `superclaude coordinator <verb>`.
- Keep: `IronOrchestrator` as the home repo name and the config key `orchestrator_repo` (`cycle.py:286,740`, `cli.py:205`), because they name a repository whose name is an owner decision (OD8 per the diff analysis), not a session. I drop my Round 1 "keep `.orchestrator/` and the verb group" carve-out: with every session-named item renamed, keeping the old folder would leave a permanent split.

**(3) Report session: no real clash found; keep as deployed.** Both of us now say "report coordinator" with tag `coordinator`. On R9's `Coordinator` worktree: the only "worktree: coordinator" text I found is illustrative output in `ccsession-tag/README.md:178` and `ccsession:1521` (an IronFlow example). The report session code has no worktree key (config.json lines 1-25, waker.py:172), and DQ12 moves it into the orchestrator repo's workspace (D:122). On this Linux host `coordinator` and `Coordinator` are different names. A clash would need a case-insensitive filesystem and a project that also has a lowercase `coordinator` worktree; I found none on master. Low risk. UNVERIFIED for non-Linux hosts and for how Coder 516's template checks for an existing worktree.

**(4) Species terms: pick A2's.** "Person-opened coordinator" and "standing-grant coordinator". Every word is already in text that exists: "the person opened" (WORKER-CONTRACT.md:70), the pinned string "coordinator is person-opened" (test line 33), and "standing-grant coordinator" (D:799). "Attended" and "standing" were my coinages and need a definition; A2's terms do not. Caveat: "person-opened" is true only of sessions a person opened. Whether an Orca-launched owner session counts is Q26's open owner question, so the term does not decide it.

**(5) Names for 339 and the process.** "Host coordinator": reject. 339's title is "To Run and manage ALL sessions within a worktree" and its body speaks of "ALL sessions"; neither says all projects. 423 says "all workspaces"; 444 says "within a worktree". The scope of 339 is UNVERIFIED and "host" is a fact A2 adds. Use "all-sessions coordinator" (339's own words) as a scope qualifier beside "project coordinator" and "sub-coordinator". "Orchestrated issue flow": accept. It is the ADD1 section title (D:135, A2's quote), it describes a process and not a session, and it matches the deployed `orchestrated/` folder (evidence 5).

**(6) Plain `/sc:coordinator` with no flag: yes, person-opened mode, with one guard.** No flag loads Orca's `orchestration` skill and the section 4 rules and takes no grants. The standing-grant path is reachable only through `--wake`, `--hourly`, `--resume` (each validated against a wake file or run state) and `--take` (a person's entry into one issue, D:133 per A2). A flag-less call must never mean "has grants". Open item for D07: R17 says the owner's coordinator takes issue duties from its launch prompt, which is a third route; it should become a `--wake` or `--take` call so grants have one door.

**(7) The word "orchestrator" in new text.** Allowed: (a) Orca's layer and commands (`orca orchestration`, the `orchestration` skill); (b) the existing parent-session meaning in the 63 installed skill, command and agent files, unchanged; (c) the proper names `IronOrchestrator` and `orchestrator_repo`; (d) exact quotes of titles 339, 423, 444 and the glossary line; (e) "orchestrated issue flow" and the `orchestrated/` folder. Not allowed in new text about this system: "the orchestrator" for a session, and any new tag, schema, key, folder or verb containing "orchestrator" outside (c). Enforcement: a pinned test over the coordinator command, skill, refs, templates and the `issue_watch` package with that allowlist (feasibility not tested: UNVERIFIED). The existing sentence at `core/CLAUDE.md:58` and `ccsession-tag/README.md:423` may keep "orchestrator" (as a layer, with a glossary definition) or change to "orchestration"; either way test lines 33 and 53 are edited in the same PR.

## Final proposed naming scheme

| Item | Name | Source and note |
|---|---|---|
| Role (genus) | **coordinator** | R9, R10, R17; WORKER-CONTRACT; Orca role table |
| Kind by authority | **person-opened coordinator**; **standing-grant coordinator** | Contract line 70, test line 33; D:799 |
| Kind by scope | **project coordinator** (one repo), **all-sessions coordinator** (339), **sub-coordinator** (444 `--sub`, evaluation only), **report coordinator** (daily and living report) | R9; 339 body; 444 title; 655 "report coordinator" |
| Process | **orchestrated issue flow**; folder `.dev/coordinator/orchestrated/` unchanged | ADD1; `common.py:134` |
| Layer | **orchestration** (Orca) | Orca skill |
| Command and skill | `/sc:coordinator`, `sc-coordinator-protocol`; flags `--wake`, `--hourly`, `--resume`, `--take`, `--sub`; no flag = person-opened mode, no grants | Clay's D:133 flags; my point (6) |
| Session name and ccsession tag | `COORD-<RepoName>`, extras `COORD-<RepoName>-<n>`, 32 characters at most | R9; `launch.py:39` |
| Report session | tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/` unchanged | `config.json:11-12`, D:1157 |
| Branch and worktree | `Coordinator` | R10 |
| Wire and persisted names | `coordinator-wake/1`, `coordinator-wake-ack/1`, mailbox kind `coordinator-wake`, `coordinator_tier`, `coordinators.json`, state under `.dev/coordinator/` | Renamed before PR 686 merges |
| CLI verbs | `superclaude coordinator <verb>` (design only); `issue-watch` stays the poll program | New evidence 3 |
| Kept proper names | `IronOrchestrator`, `orchestrator_repo` | Repo name is an owner decision |
| Issue nesting | 339 = all-sessions coordinator epic; 423 = knowledge layer over coordinators, not a role; 444 = sub-coordinator, deferred (WC-13); 655 and Clay's design = standing-grant project coordinator via `/sc:coordinator --wake`; report session = report coordinator | Titles unchanged; glossary plus pinned test |
| Word "orchestrator" in new text | Only uses (a) to (e) in point (7) | Pinned test proposed |

Unverified: Coder 516 text, whether the owner's `COORD-` name is a ccsession tag, the scope of 339, a non-Linux worktree clash, and the owner's "coordinator (aka orchestrator)" quote.

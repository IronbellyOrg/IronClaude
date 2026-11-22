# Verdict D08: Naming and identity of the primitive

## Question

CLAY names the command `/sc:orchestrator` (D:65) while OURS says "coordinator, not orchestrator" (R10, Coder 516), and issues 339 (orchestrator mode), 444 (`/sc:orchestrator --sub`) and 423 (Orchestrator v2, knowledge layer) already use the word for other purposes. The owner's own wording says "coordinator (aka orchestrator)". Decide one name for the session role, one for the command, and how 339, 423, 444 and Clay's design nest into one family.

## Winner

HYBRID: the names are OURS (role "coordinator", command `/sc:coordinator`), and five separable CLAY pieces (flag set, "standing-grant coordinator", "orchestrated issue flow", unchanged report-session names, the settle-before-merge deadline) are kept inside it.

Notation: "D:nnn" = a line of `docs/designs/orchestrator.md` on master (Clay's design, merged by PR 681). "ZS-REQ" = the owner's zero-setup requirements file in worktree `claim-handoff-planb` (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`). Snapshots are under `/home/coder/.cache/ic-snap-20261120/`.

## Winning recommendation

The unified spec must say the following. Each line can be checked against a file or a test.

1. **Role name.** The session role is "coordinator". No session, tag, key, schema, folder or verb about this system is named "orchestrator". Basis: ZS-REQ R9 (line 40), R10 (line 41), R17 (line 43), and the owner renaming the live session from `ORCH-IronClaude` to `COORD-<RepoName>`.
2. **Command and skill.** `/sc:coordinator` and `sc-coordinator-protocol`. Flags `--wake <wake_id>`, `--hourly`, `--resume`, `--take <owner/repo#N>` (Clay's, D:133) and `--sub` (issue 444, evaluation only). Test: no `commands/orchestrator.md` and no `sc-orchestrator-protocol` exists after the unified work.
3. **Kinds, by qualifier, not by noun.** "person-opened coordinator" (WORKER-CONTRACT section 4, line 70) and "standing-grant coordinator" (Clay's own term, D:799). Scope qualifiers: "project coordinator" (one per project, session `COORD-<RepoName>`, branch and worktree `Coordinator`), "all-sessions coordinator" (issue 339), "sub-coordinator" (issue 444), "report coordinator" (Clay's daily and living-report session).
4. **Authority comes from a recorded authorization, never from a name or a flag.** A call of `/sc:coordinator` with no flag is person-opened mode: it creates no grant and starts no merge (a test pins this). Grants come only from the owner-recorded authorization (per-issue grant row, or the authorization the launch prompt cites, as D06 items 6 and 7 say). The owner's R17 start from a launch prompt becomes a `--wake` or `--take` call, so there is one door. This resolves the probe finding INV-001.
5. **Process and layer names.** "Orchestrated issue flow" names the process (claim, plan check, handoff, watch, merge on the person's go, closeout, audit); the existing folder `.dev/coordinator/orchestrated/` stays (`agent-work-report/scripts/common.py:134` on master). "Orchestration" names Orca's layer only.
6. **Report session unchanged.** Tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/` (`agent-work-report/config.json:11-12`, D:714, OD6). It is not renamed.
7. **Branch names.** `Coordinator` is the project coordinator's working branch and worktree (R10). `coordinators` is the shared records branch of Q26 (it exists on the fork). They are two things; the spec says so in one sentence. This closes the question D07 verdict item 10 handed to this topic. Owner may overrule (see Unverified).
8. **Persisted names renamed before PR 686 merges.** `orchestrator-wake/1` and `-ack/1`, mailbox kind `orchestrator-wake`, key `orchestrator_tier`, `orchestrators.json`, the `.orchestrator/` folder, the golden fixture `orchestrator_wake_golden.json`, the typed line `/sc:orchestrator --wake <id>`, and the design-only verbs `superclaude orchestrator ...` become coordinator names (pr-a `wake.py:46-47`, `tests/issue_watch/test_wake.py`, `test_launch.py:98-99`, `launch.py:33-35`). Master carries none of them today, so the cost is zero on master and grows after merge. If D07 stands, the registry (`orchestrators.json`, `.orchestrator/`, `IronOrchestrator`, `orchestrator_repo`) is removed anyway.
9. **Nesting.** 339 = the all-sessions coordinator; 423 = a knowledge layer over coordinators, not a role; 444 = the sub-coordinator, deferred (WC-13 bars worker fan-out); 655 and Clay's design = the standing-grant project coordinator reached by `/sc:coordinator --wake`; report session = the report coordinator. Titles of 339, 423, 444 and 655 stay as written. A glossary line in `HOW-WE-WORK.md` and in the command's Activation section says: "In an issue title, 'orchestrator' means the program or epic whose session role is the coordinator; 'orchestration' is Orca's layer." A pinned test checks the line exists.
10. **Where the word "orchestrator" may still appear in new text:** Orca's layer and commands; the existing parent-session sense in the 63 installed skill, command and agent files; exact quotes of issue titles; "orchestrated issue flow". Nothing else about this system. A test scoped to the new files enforces it (feasibility UNVERIFIED).
11. **Alias.** If the owner's wording "coordinator (aka orchestrator)" is real (not found in any source read), it makes "orchestrator" an alias for the one role, which supports one role name, not two; the glossary line carries the alias.

## Strongest points

**OURS**
1. The owner's own rows give the job to the coordinator by name: ZS-REQ R9 ("carries the issue-pipeline duties from a standard install"), R10 ("the term is 'coordinator', not 'orchestrator', everywhere"), R17 ("takes the issue-pipeline duties from its launch prompt"), plus the dated change of the live session name from `ORCH-IronClaude` to `COORD-<RepoName>`. CLAY's advocate conceded this in Round 2.
2. Clay's own design calls the orchestrator a coordinator: D:799 "a standing-grant coordinator and not a worker (ADD1)", D:902 "The orchestrator, which is this spec's coordinator". And the platform and installed text agree: WORKER-CONTRACT has 80 lines with "coordinator" and 0 with "orchestrator"; Orca's `orchestration` skill has Coordinator and Handoff owner roles and no Orchestrator role (diff-analysis verification log).
3. "Orchestrator" already means the parent session of a skill in 63 installed files (`sc-reflect-protocol`, `sc-troubleshoot-protocol`, `debate-orchestrator`, `sc-implement-protocol/refs/qa.md:56`), so a `/sc:orchestrator` command would put two meanings in one sentence (diff-analysis X-008, verified count 63).

**CLAY**
1. The authority difference is real and needs a first-class, testable surface: `WORKER-CONTRACT.md:70` defines the coordinator as person-opened and the pinned test `tests/core/test_orca_session_launch_guidance.py:33` requires that phrase. ADD1 (D:135) lists the contract conflicts. The merged scheme keeps this as the "standing-grant coordinator" section.
2. The command surface is already designed and has a merged forward reference: flags `--wake`, `--hourly`, `--resume`, `--take` (OQ5, D:133) and `agent-work-report/SKILL.md:12` on master. OURS had no flags.
3. The deployed report-session names (`coordinator` tag and prefix, `.dev/coordinator/`) and the "wire names are cheap until merge" timing point (pr-a `wake.py:46-47`, `test_launch.py:98-99`). OURS's paper had wrongly planned to rename the report session.

## Clay strengths to adopt

- **Flag set `--wake`, `--hourly`, `--resume`, `--take`.** Why: a capability OURS lacked (the command did not exist). How: lift unchanged onto `/sc:coordinator`; only the word changes. Source: D:133.
- **"Standing-grant coordinator" plus an explicit contract section for the orchestrated issue flow.** Why: the authority difference needs a named, tested surface (ADD1, D:135, D:799). How: add as a named case inside WORKER-CONTRACT section 4, not a second noun; its rules are bounded by D06's verdict (merge only on the person's go).
- **"Orchestrated issue flow" as the process name.** Why: names the work without using a word that already names a session; matches the deployed folder `.dev/coordinator/orchestrated/`. How: use in the spec, the contract section title and the skill text.
- **Report session names unchanged ("report coordinator").** Why: a verified collision with the live tag, automations and state folder if renamed (`config.json:11-12`, D:714, OD6). Override: prose says "report coordinator".
- **Settle persisted names before PR 686 merges.** Why: after merge the wire strings and tag are in master and need a migration. How: action 8 above, before D14's disposition of PR 686 lands.

## Our strengths that must be kept

- One role noun, "coordinator", for the person-opened and the script-started kinds, with authority tied to a recorded grant (INV-001 rule).
- `COORD-<RepoName>` as the session name, `Coordinator` as branch and worktree (R9, R10).
- `/sc:coordinator` and `sc-coordinator-protocol`; no `/sc:orchestrator`.
- The titles of issues 339, 423, 444 left alone with a glossary line, because only the owner edits them.
- The WORKER-CONTRACT vocabulary (person-opened coordinator, WC-16 "Coordinator loop") unchanged for the first kind.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Use the names in this verdict throughout the unified spec; replace "orchestrator" for the session with "coordinator" | DOC | unified spec (`.dev/brainstorms/20261120-pr686-unify/spec/`) and `docs/designs/orchestrator.md` as rewritten by D14 | After D06 and D07 verdicts; before PR 686 is rebuilt |
| Rename persisted names (wake schemas, mailbox kind, tier key, state folder, typed line, golden fixture) | PR KEEP-ADAPT | PR 686 (Clay's watcher rewrite, head 8e5ae29ad) or its replacement per D14 | Must land before any merge of it |
| Fix `agent-work-report/SKILL.md:12` ("The orchestrator (`/sc:orchestrator`) does every check-in itself") | PR KEEP-ADAPT | PR 684 (Clay's work-report move, merged); follow-up edit | With the first coordinator-skill PR |
| Edit `core/CLAUDE.md:58` and `ccsession-tag/README.md:423` ("A supervised orchestrator's coordinator is person-opened") with a glossary definition; update `tests/core/test_orca_session_launch_guidance.py` lines 33 and 53 in the same PR | LOCAL CHANGE | `src/superclaude/core/CLAUDE.md`, `src/superclaude/skills/ccsession-tag/README.md`, that test | Same PR as the WORKER-CONTRACT line 70 and 245 edits from D06 (one pinned sentence family) |
| Add the glossary line to `HOW-WE-WORK.md` and the command's Activation text, with a pinned test | LOCAL CHANGE | `src/superclaude/core/HOW-WE-WORK.md`, the new command | With the first coordinator-skill PR |
| Add tests: flag-less `/sc:coordinator` creates no grant and no merge; the "orchestrator" allowlist test over the new files | LOCAL CHANGE | tests for the new command | With the skill |
| Check the tag form (`COORD-<RepoName>` or `COORD-<short>`) against ccsession | DECISION (build check) | ccsession tag rules, `launch.py:39` (U25) | Before building the launcher |
| Decide whether to retitle issues 339, 423, 444, 655 or leave them with the glossary | DECISION | those issues (owner edits; no agent writes) | Optional, any time |
| Confirm branch roles: `Coordinator` (working) and `coordinators` (records) | DECISION | owner, with Coder 516 | Before the branch and worktree are created |
| Keep `COORD-<RepoName>` and `Coordinator` as filed | PR KEEP | Coder issue 516 (owner's issue for a coordinator per project; other repo, unread) | None |
| Keep issue 444 open as the `--sub` evaluation; read its title "Sub-Orchestrator or Coordinator" as one concept | DOC | issue 444 | None |

## Implications

- **Watcher:** the poll's wake message, mailbox kind, tier key and tag all change word before merge; D07 removes the registry and the extra sessions per repo, so the `-<n>` suffix is unused.
- **Coordinator:** one command and skill for both kinds; the person-opened kind needs no flags. Grants have one door (`--wake` or `--take`) and always rest on a recorded authorization (D06).
- **Dashboard and sweep:** unaffected; "coordinator" is already the word in `/sc:sweep` and WC-16.
- **Claim pipeline:** `/sc:issue --claim ... --pipeline none` is unchanged; only the handoff recipient is now "the project coordinator".
- **What breaks:** the design doc on master (759 uses of "orchestrator"), issue 655's body and comments, and Clay's open PRs 689 and 690 use the old word and need edits or a glossary; installed copies on other hosts keep old text until the next install. One pinned test (`test_orca_session_launch_guidance.py` lines 33 and 53) must change in the same PR as the `core/CLAUDE.md:58` edit.
- **Owner must know:** the name `/sc:orchestrator` is not an owner decision: OQ5 (D:133) has Owner column "no" and none of OD1 to OD15 covers it (diff-analysis X-001). The design's status "approved by the owner (Clay)" does not establish it.

## Confidence

85 percent on role noun and command name (R9, R10, R17 and the concession by CLAY's advocate). 70 percent on the branch-name ruling and the tag form. It would change if Coder issue 516's text said something other than the requirements file records, or if the owner states that "orchestrator" is the preferred word for the command.

## Unverified

- Coder issue 516 text (other repo, not readable); R10's "everywhere" rests on the ZS-REQ row.
- The owner's wording "coordinator (aka orchestrator)": found in no source read (TOPICS.md only).
- `RULINGS.md` (OD6 rulings) and the merge time of PR 681.
- Whether `COORD-<RepoName>` is a ccsession tag or only an Orca terminal name (U25); `launch.py:39` marks the tag pattern itself UNVERIFIED.
- Whether any consumer outside master `src` (IronFlow repo, hooks elsewhere) matches tag prefixes.
- Feasibility of the "orchestrator" allowlist test.
- The scope of issue 339 ("ALL sessions within a worktree"); "all-sessions" is its own wording, nothing more.
- Scores in `base-selection.md` are judge estimates, with no dual-pass position-bias run.

## Debate artifacts

Folder `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/`: `position-OURS.md`, `position-CLAY.md`. In `adversarial/`: `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `round1-advocate-1.md`, `round1-advocate-2.md`, `round2-advocate-1.md`, `round2-advocate-2.md`, `invariant-probe.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merged-output.md`, `merge-log.md`, `return-contract.yaml`.

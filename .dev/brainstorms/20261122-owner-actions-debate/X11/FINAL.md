# X11 (OA-21) Confirm Clay's eight removal PRs: FINAL

Checked 2026-11-22 against origin/master 2ea524514 (git show and gh reads only). Hours are estimates (est). Every verdict here is a recommendation until the owner says so in chat.

## 1 Unified proposal

Status stays "not confirmed" until the owner speaks. Nothing is reverted (D14 says KEEP). The item gates only a host install or update.

| PR | What it removed | Recommendation |
|---|---|---|
| 620 | /sc:save, /sc:load | CONFIRM |
| 622 | /sc:build | CONFIRM |
| 627 | /sc:improve | CONFIRM |
| 631 | /sc:index, /sc:index-repo | CONFIRM |
| 629 | cli-portify (command, skill, CLI package); copy at tag v5.0.0 | CONFIRM |
| 632 | roadmap, tasklist, sprint CLIs, 3 commands, 3 skills | ASK, then confirm |
| 650 | skills prd, tdd, tech-research, tech-reference, operational-guide, readme; /sc:tdd | HOLD until the owner answers |
| 656 | skills task, task-builder, roadmap; level 4 of the routing guide | HOLD until the owner answers |

Order: (1) owner answers one question in chat; (2) agent records it; (3) per host, a read-only list of what the install would delete, with a backup of every "remove" item to `~/.claude/retired-backup/<date>/` (does not exist yet); (4) the owner's go; (5) install; (6) compare the printed Removed and Kept lines with the list.

The one question, asked once: "Do you still run `superclaude sprint`, `roadmap` or `tasklist`, the document skills (readme, tech-reference, prd, tdd, tech-research, operational-guide), or the `/task` and `task-builder` skills yourself?"

Gate: one owner go naming the hosts covers every item whose PR is confirmed. Any held or unrecorded item must be named in the go, or that host does not install. A list that changes after the go needs a fresh go. "Kept" lines (edited copies) are never forced.

Also on the list, outside the eight: `/sc:spawn` (PR 617) and `/sc:review-translation` with its skill (PR 621). Tag each item with its PR number. See section 9 for how they are handled.

## 2 Context

Clay (clayphi) merged all eight into `integration` on 2026-11-17 and 2026-11-18 (gh read: author and merger clayphi on every one; reviews only from augmentcode, chatgpt-codex-connector and clayphi). Owner approvals on issue 571 are: wave 1 (plan PRs 1, 2, 5, merged as 615, 616, 617) and "keep swarm". Six of the eight (620, 622, 627, 629, 631, 632) are plan PRs 6, 7, 8, 4, 9 and 11 in the issue body the owner is recorded as reviewing; I found no owner comment approving them one by one. PRs 650 and 656 (6.1.0) are not in that plan list at all. The owner and agents share one GitHub login, so a comment under `ironbelly` is not proof the owner wrote it.

## 3 Implications

Changes: the owner answers one question and one go per host. FR-66 (SPEC.md line 323) is reworded in the planned amendment PR to name the retire step, not only `--force`. Stays blocked: any host install or update until the backup and the go; held items stay unconfirmed.

Verified hazard: `src/superclaude/cli/main.py` lines 277 to 279 (install) and 431 to 433 (update) call `run_retire_files_step` unconditionally. The module header says it deletes an installed copy whose sha256 matches a shipped tag; a skill folder goes only if every file matches; edited copies are kept. I found no per-name skip, so a plain install is the hazard, not only `--force`. The step reads only `~/.claude/commands/sc/`, `skills/` and `agents/`, so a backup beside them is safe.

## 4 Benefits

Five removals settled now. The owner answers once, in plain words. The default is enforced by a backup, not by memory. Every outcome is reversible.

## 5 Risks and containment

- Owner says yes from habit and loses a workflow. Containment: one named question; this host shows live use (the staged package `TASK-TECHREF-issue-pipeline-20261120-040158` says "Calling Skill: tech-reference" on line 4, dated 2026-11-20, two days after PR 650 merged).
- A host installs before the backup and deletes pristine copies. Containment: the agent never installs before the folder exists; recovery by `git show v6.0.0:<path>`.
- A "hold" protects nothing by itself: a restored copy is deleted again by the next install. Containment: a go that names held items, and a new decision (restore the skill or build a per-name skip) if the owner says "yes, in use".
- Stale text points at removed skills: `/task` appears in `launch-level-guard.sh` (lines 43 to 45 per the agents), `commands/issue.md:101` and `core/WORKER-CONTRACT.md:297` (read), plus `rf-team-lead.md` (B, not re-read). Containment: one small follow-up.
- Backup folder becomes clutter. Containment: the agent lists it and asks before removing.

## 6 Costs (estimates)

Owner: about 5 minutes plus one go (est, one question and one sentence). Agent: about 0.5 hour to record (est); about 0.25 hour per host for the list and backup (est; host count UNVERIFIED). Restore of one skill: about 0.1 hour (est, one folder copy). Reverting a whole PR 632 or 650: 3 to 8 hours (est, large diffs plus later merges). Stale-text follow-up: under 1 hour (est). Per-name skip: 3 to 5 hours (est, one code path, tests, the `/sc:pr-submit --monitor 3` loop).

## 7 The sentence the owner says

If none of those are still run: "I confirm removal PRs 620, 622, 627, 629, 631, 632, 650 and 656 as merged. I also note 617 and 621 were part of the plan I approved. No host runs install or update until its backup exists and I say go."

If some are still run: "I confirm <numbers>. I do not confirm <numbers> yet." Any split is allowed. 632 joins the confirmed group when sprint, roadmap and tasklist are not used.

## 8 What an agent does after

1. Record the words, date and one line per PR in chat, then in `.dev/brainstorms/20261120-pr686-unify/DECISIONS.md` (OA-21 rows, lines 1269 and 1361) and STATE.md.
2. Per host, before any install or update: run `classify_retired_files()` with `uv run` (read-only per its docstring; I did not run it), keep the "remove" verdicts (absent names are also returned), back them up, and show one combined list tagged by PR number.
3. Apply the gate in section 1. After install, compare the Removed and Kept lines with the list.
4. A held item answered "yes": raise a new decision (restore from tag v6.0.0, or build the per-name skip). Do not hold open-ended.
5. On the owner's go only: reword FR-66, fix the stale `/task` texts, file the per-name skip issue. Any PR goes through `/sc:pr-submit --monitor 3`. Post nothing on GitHub otherwise.

## 9 Consensus: full. One owner choice remains

A and B agree on the table, the question, the backup, the tiered go and the follow-ups. They differed only on whether 617 and 621 join the question. I decided independently, from issue 571: 617 (`/sc:spawn`) was explicitly approved in owner decision comment 10 ("start wave 1 (PRs 1, 2 and 5 ...)", 2026-11-17), so B's "no decision recorded" is wrong for it. 621 is plan PR 10: the owner named the destination fork `ironbelly/IronClaudeV5`, but I found no explicit approval of the removal itself. DECISIONS.md has no mention of either (grep earlier by the agents).

Owner choice: should 621 be covered by the same confirm sentence?
- Yes (recommended, already in the sentence above): the item is settled and the go covers it. Consequence: if the owner did not mean to approve it, the next install deletes a pristine copy; backup makes it a 0.1 hour (est) restore.
- No: it stays unconfirmed and any host list containing it needs a named go each time. Consequence: more owner turns, no silent removal.
617 needs no choice: tag it "approved on issue 571" in the list.

## 10 Not verified

- Owner approval of any of the eight given only in chat and never written to issue 571 (UNVERIFIED).
- Whether the owner's tech-reference use comes from the project `.claude/skills/` dev copies, which the retire step does not touch (UNVERIFIED). The installed `~/.claude/skills` on this host has no `tech-reference`, `task` or `roadmap` folder (listed), but has `task-builder`, `sc-roadmap-protocol`, `sc-tasklist-protocol` and `sc-cli-portify-protocol`; whether they are pristine is UNVERIFIED.
- `classify_retired_files()` not run; host count unknown; that no hidden per-name skip exists beyond the shipped-name skip (checked: main.py calls and module header only).
- The `launch-level-guard.sh` and `rf-team-lead.md` line numbers (taken from the agents). Whether the issue-body line "Ryan has reviewed this plan" was ever completed.

# X16 FINAL: hosts that installed IronClaude between 00:02 and 15:07 UTC on 2026-11-20

Status: a recommendation only. Nothing is posted or changed until the owner says so in chat.
Basis: read-only. Rounds 0 and 3 of both agents, plus my own checks of the sources named in section 10.

## 1 Unified proposal
Ask each possible outside host for one read-only check, and update only the hosts that fail it. No blanket install.

Who is affected (a host is affected only if a person ran `superclaude install` or `update`, or a pipx or uv tool install of IronClaude, from master inside the window and outside Coder):
- This workspace: done. The owner updated it on 2026-11-21. Its guard and contract fingerprints equal master.
- Coder workspaces (the owner's and other users'): never in the window. The template pins one commit, 64dfc0e (before PR 682), then 2ea5245 from 2026-11-21 00:55 UTC. Their only gap is guard version 2, which arrives with the template roll, then each owner runs `coder update <workspace>`. A restart alone keeps the old image. Nobody hand-updates a Coder workspace.
- Other hosts (laptops, servers): unknown. Ask Clay and IB-JonathanB by name, plus anyone the owner names.

The check, per host (read-only):
`sha256sum ~/.claude/hooks/launch-level-guard.sh ~/.claude/WORKER-CONTRACT.md | cut -c1-12; sed -n 10p ~/.claude/hooks/launch-level-guard.sh; readlink -f "$(command -v superclaude)"`
- guard a561b1a7e7e7: window build, affected.
- guard 71e479dd1076: before PR 682 or after the PR 700 rollback; not harmful, but stamp is 1 and it needs version 2.
- guard e6fc1470ae82 with stamp 2 and contract f0b85e7fec01: done.
- any other value: a local edit. Stop, keep the file, the owner decides.

Order for a host that is not done (the host's own person runs it):
1. Agent shows the note in chat; after the owner says the text is right, post it on issue 717 with `gh issue comment 717 --repo IronbellyOrg/IronClaude`. Note text: "If you ran superclaude install or update, or pipx or uv tool install of IronClaude, outside Coder between 00:02 and 15:07 UTC on 2026-11-20, or are unsure, run the check below and reply with the printed lines only. Do not update yet."
2. Back up with `cp -a` into one dated folder: `~/.claude/{hooks,WORKER-CONTRACT.md,CLAUDE.md,settings.json,rules,output-styles,skills,commands,agents}` (those that exist).
3. Refresh the package first, with the manager the readlink shows, to pin 2ea524514154bde03258a7d7d8a0265c371609af (fork URL only): `uv tool install --force git+https://github.com/IronbellyOrg/IronClaude.git@<pin>` or the `pipx install --force` form. Agent rechecks the pin just before the go.
4. Diff the installed guard, contract and CLAUDE.md against the package copies. Guard and contract differences are expected. CLAUDE.md differences are the host's own text: merge by hand afterwards.
5. Run `superclaude update` once. Not `install`, not `install --force`. Read the retire lines it prints; copy back from the backup any skill the person still needs.
6. Restart Claude Code and Orca sessions there when no worker runs.
7. Verify: rerun the check (e6fc1470ae82, stamp 2, f0b85e7fec01); `superclaude --help` and `superclaude issue-watch --help` exit 0; the package has `cli/issue_pipeline`; hook entries remain in settings.json.

Coder sentence (my decision on the one open wording point): send the non-Coder note now. Send the Coder sentence as a second comment on 717 once the template roll item says the new build is published: "Coder workspaces need nothing for this window; to get the newest guard run `coder update <workspace>` (a restart alone keeps the old image)."

## 2 Context
PR 682 merged 2026-11-20 00:02 UTC and removed the issue_pipeline package and changed the worker contract and guard. PR 700 rolled it back at 15:07 UTC. PR 707 then set the guard version stamp to 2, so every host needs one forced refresh. A plain `superclaude install` skips files that exist and never reads the stamp, so a host that installed in the window keeps the bad files. The set of such hosts is small and probably only maintainers' own machines.

## 3 Implications
- Changes: two or three outside hosts get a backed-up, diffed update to one build. The agent keeps one row per host (who, UTC time, fingerprint before and after) in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/STATE.md. Silence is recorded as "assumed stale".
- Stays blocked: no worker launches on a host until its check passes. The claim script already refuses a guard without stamp 2, so a stale host fails safe at claim time. Nothing is live today anyway (issue watcher not switched on).
- Not required: the owner's answer on the eight skill-removal PRs (OA-21). The backup plus reading the retire lines covers it host by host.

## 4 Benefits
One exact test (a file fingerprint, not a guess). No per-host ceremony for Coder users. A before and after record per host. Also catches hosts that never reached guard 2.

## 5 Risks and how to contain each
- An unknown outside host is missed: ask by name, record silence as stale, and the claim refusal is the backstop.
- `update` overwrites local edits, CLAUDE.md included: backup, diff, merge by hand; rollback is copying the backup back.
- `update` runs the retire step and can remove skills a person still uses: read the printed retire lines, copy back from the backup.
- Running sessions keep old hooks: restart when no worker runs.
- The pin trails master: recheck before the go.
- A Coder user acts before the template roll and sees no change: the Coder sentence is held until the roll is published.
- Old package reinstalls the old tree: refresh the package first, step 3.

## 6 Costs (estimates; basis is step counts, not measured)
Owner: 2 to 5 minutes. Agent: about 0.5 hour (note, pin and fingerprint recheck, records). Each outside host: about 0.3 hour (check 1 minute, backup and diff about 5, refresh and update about 10 to 15, restart and verify 5 to 10). Two hosts: about 0.6 hour of other people's time. Coder: 0 from this item. Total about 1 to 1.5 hours over a day or two.

## 7 The sentence the owner says in chat
"X16 approved: show me the note, post it on issue 717 once I say the text is right; a host that is not done updates by backup, package refresh, diff, then update; Coder users only run coder update after the template roll; tell me before anyone overwrites a host that shows local edits."

## 8 What an agent does after it
1. Records the go in STATE.md (the owner writes no file).
2. Runs `git fetch origin`, rereads the Coder pin, recomputes the guard and contract fingerprints; updates the table above first if anything moved.
3. Shows the note in chat; posts on 717 only after the owner approves the text.
4. Collects the replies, records one row per host, and tells the owner before any host with local edits is touched.
5. Posts the Coder sentence when the template roll item reports the build published. Closes X16 when every named host is done or the owner retires it.

## 9 Consensus
Full. Both agents ended on the same steps, order, check and owner sentence. Their one open point (whether the 717 note mentions Coder) I settled as two comments, so no owner choice is left. Residual: none. If the owner prefers no Coder sentence on 717, it travels with the template roll item instead; the consequence is that a Coder user could restart and wrongly think they are current.

## 10 What could not be verified
Verified by me: guard fingerprints by commit (64dfc0e and 471f10511 give 71e479dd1076, 01e7a9e23 gives a561b1a7e7e7, 2ea524514 gives e6fc1470ae82; contract f0b85e7fec01); this workspace's installed guard and contract match, stamp line is 2; 64dfc0e is an ancestor of 01e7a9e23; Coder pin history through `gh api` (3fb35a5 on 11-18, 64dfc0e on 11-19 03:58Z, 2ea5245 on 11-21 00:55Z); `update` forces every file group (main.py lines 383 to 422) and runs the retire step (line 431); `install` has the codegraph phase; the claim script requires the stamp line (orca_worktree.py line 876); the Coder README says `coder update` is needed and a restart keeps the old image (about the strace change, not the IronClaude pin).
UNVERIFIED: which hosts the maintainers use or whether anyone installed in the window; the list of other users' Coder workspaces (needs `coder list` as admin, not run); whether a template version carrying pin 2ea5245 has been published for all users; that a restart leaves the pin unchanged (inferred from two files); whether `superclaude update` has ever been run end to end (the install test did not run it); the registration of `issue-watch` in main.py; the location of the owner's .bak.20261120T202103Z backups; whether master moved past 2ea5245 (my local origin/master shows it as tip, no fetch run). The local Coder checkout is on a stale branch, so I used `gh api` for its history.

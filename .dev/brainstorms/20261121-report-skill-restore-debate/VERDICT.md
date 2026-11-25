# Verdict: restore the work-report skill (agent-work-report)?

Judge's file, 2026-11-21. Read-only work; no GitHub write was made. "Archive" means branch `origin/clayphi/archive-orchestrator-655-20261120` (commit `d7d645ddd`). "The skill" means `src/superclaude/skills/agent-work-report/` (16 scripts, 7 templates, 6,471 lines, plus a 4,005-line test file). "The plan" means the unification spec `SPEC.md` and `DECISIONS.md` in `.dev/brainstorms/20261120-pr686-unify/`.

## 1 Verdict in three lines
1. **Restore later, not now: tag the archive commit today, and restore a trimmed, fixed version only when a named trigger fires** (the owner says a daily per-issue page is wanted, or stage S15c, the build of the entry-file writer, is about to start). Do not restore it as it stands.
2. Confidence 65 percent on the timing; 90 percent that "as it stands" is wrong and that tagging is right; 85 percent that the server hole and the Clay-only config must be fixed before any restore.
3. Partial: both sides ended up agreeing on every fix and differ only on timing, and my "later" rests on two things nobody could check (whether Clay's copy in the IronFlow repo still runs, and whether the owner wants a daily page at all).

## 2 Where the two sides agree
- The skill must not come back as it stands: the local web server must be fixed, the Clay-only config must go, the owner must review it, the author must not merge it.
- Tag `d7d645ddd` now so the code cannot be lost (only `archive/pr-682-issue-pipeline-removal` is tagged today; checked with `git tag -l 'archive/*'`).
- Keep the report session names of decision D08 (tag `coordinator`, prefix `coordinator-`, folder `.dev/coordinator/`). Checked: `debates/D08/VERDICT.md` line 22 says "It is not renamed".
- The living half (one entry file per held issue, `exclude.py`, `run.py refresh`) has no writer: nothing on master or on the archive writes those files except the skill's own move-to-closed code (tech reference line 805). `superclaude orchestrator report-entry` does not exist, and `/sc:closeout` prints `ENTRY escalated ... why=surface_absent` (`settle.sh:1037-1042`).
- Ask Clay two facts first: why the skill was in his rollback (PR 700's body gives none; it says only "at Clay's request"), and whether his daily report still runs from the IronFlow copy.
- Restoring does not fix `/sc:closeout`, and the observer shows "titles and links only" until the writer exists (FR-80).

## 3 Where they disagree and who is right

**3.1 Does the decision block real work soon? NOT-RESTORE is right.**
Issue 718's pick-up note says no item starts before the plan stage it extends has landed (D1 to D4 extend S16, observability glue, which is late). C14 and the C8 entry line sit in coordinator phase 2 (S15c). RESTORE's own table says a restore "can start, still needs the writer" for C14 and C8. So neither answer moves the critical path. What YES unblocks is D1 tests on hand-built entries, the D3 config test and the D4 diff, which is work the restore itself creates. The "blocks six items" argument is weak.

**3.2 Restore the reader first so the writer is built against it? NOT-RESTORE is right, partly.**
The archive's entry format (`common.py:133-151`) stores a session-status map, session links, and model-written `recommend`, `how`, `suggested`. The plan (FR-46, FR-80, decision D11) says entries store only `session_id` and never show `recommend` or `suggested`. Restoring now pins a format the plan means to change, so the reader, `exclude.py`, `refresh` and their tests get reworked once more after S15c. RESTORE is right that the field names live only in this file, so S15c should copy them; that needs a read, not a restore.

**3.3 Is the silent-loss gate hard to replace? RESTORE is right.**
I checked: `check.py` enforces the shape of the skill's own `item-template.md` and the carry-forward rule, and `run.py gate` ties delivery to the sha256 of `overview.md` (`run.py:237,259`). The gate is welded to the report's own files. NOT-RESTORE's "one S16 test" covers a sweep screen, not an item list across days; they conceded the gate comes with the render stack or is rebuilt as a property.

**3.4 Did the plan already adopt it, so "no" reverses a decision? Neither fully.**
True: decision D11 (hybrid), D15 rows E1 to E5 and E7, and FR-45 to FR-50 adopt it with changes. But D11 was 72 percent confident, its facts changed (the skill left master), `DECISIONS.md` line 462 says "Restoring the skill is an owner decision", and Appendix B.3 action 1 writes the No branch as a normal outcome. Adoption does not bind the owner.

**3.5 Person-specific config. Both numbers are right and measure different things.**
Verified: `config.json` has `"person": "clayphi"`, `"person_name": "Clay"`, two orgs, a Chicago time zone. The word Clay or clayphi is on about 106 lines in 17 files (SKILL.md 36, scripts about 52, templates 16). RESTORE's "17 lines read config" counts config reads (I count 19); NOT-RESTORE counts text a model and a reader see. The fix is bigger than RESTORE's first guess and smaller than a rewrite.

**3.6 Cost.**
RESTORE: 4 to 8 builder hours plus 2 to 4 review hours (6 to 12). NOT-RESTORE: 11 to 22 for the same PR. My estimate for a full two-commit restore with the fixes and the DM, waker and commit steps off by default: **12 to 20 hours of builder and review-loop time, plus 2 to 3 owner hours**. Basis: the server function is 37 lines (`page.py:308-344`) but has no test (a search of the 4,005-line test file for `ensure_server`, `http.server`, `8765` finds nothing), so three tests are new; about 106 Clay lines to neutralise; 73 test lines mention the waker and 14 the DM; master moved 8 commits and `test_worker_contract.py` changed by 116 lines; PR 684 drew 114 review entries and five Codex security findings, so a 10,000-line new-file PR will draw a long `/sc:pr-submit --monitor 3` loop. RESTORE's basis leaves out prose edits and the review loop; NOT-RESTORE's 8 to 16 for commit 2 alone is high on unit cost. This repo squash merges (recent master commits end in `(#NNN)`), so "the owner reads only commit 2" holds in the PR view, not in history.

**3.7 Claims I found wrong or unsupported**
- NOT-RESTORE A3 and its condition C3: the report's tag and prefix "clash with COORD-<RepoName>". Wrong; D08 keeps them. (Withdrawn by them.)
- NOT-RESTORE section 4: "D11 says the nine-row table and cap are spec text only". That line is an advocate's strongest point, not the verdict. (Withdrawn.)
- NOT-RESTORE "S15c is months away": no source. (Withdrawn.) "The chat report is the interim surface": the verdict never defines it; it is the skill's own Step 13 summary and would not exist under NO.
- RESTORE rebuttal: OD-9 ("info streams off with a switch") is the watcher's three info streams (FR-09, `SPEC.md:199`), not the skill's `orchestrated/info/` folder. Wrong.
- RESTORE A1 calls the rollback a process matter while its own N2 says Clay's reason is unknown. Inconsistent. RESTORE A4 "has run live" rests on code comments from the IronFlow period (withdrawn).
- Both missed: FR-79 (last sentence: the report runs its own sweep) and FR-80 (cites `common.py:139-141`) also name the skill.
- Verified true: sizes; PR 684 merged 2h29m after opening by its author, `reviewDecision` empty, reviewers clayphi 39, augmentcode 26, Codex 19, none by ironbelly; the sweep row has no `session_id` (0 hits in `report.py`); the observer on master reads no entry files (0 hits); the server has no test.

## 4 The decision in plain words

| Option | What it gives | Cost in hours (basis in 3.6) | Main risk | Stays blocked |
|---|---|---|---|---|
| A. Restore as it stands | Everything back in one checkout | 1 to 2 | Ships an open Medium security hole, Clay's name, DM and commit steps to every install | Same as B, on a bad base |
| B. Restore now, two commits, fixed (RESTORE's offer) | Daily page and gate under owner review; D11 adoptions kept | 12 to 20 agent and review, 2 to 3 owner | Large review; entry format reworked after S15c; side-effect code installed though off | Writer, FR-45 session-map swap, C14 and C8 entry line, observer text |
| C. Restore a trimmed "daily core" now (NOT-RESTORE's fallback) | Page and gate; no waker, DM or living half | 9 to 17 (their figure; I think 10 to 18) | Still reviews about 9,000 lines; living half re-added later | Same as B |
| **D. Tag the archive commit now, restore later at a named trigger** | Nothing lost; no review now; the restore is built against the real entry format | Tag 5 minutes (owner push) plus 1 to 2 for wording edits; the later restore costs as B or C | Decision drifts; no daily page meanwhile | Same items, which are late anyway (3.1) |
| E. Do not restore | Fewer decisions; D1 to D4 closed | 2 to 4 (spec and issue edits) | Per-issue plain-English text, ClickUp view and the silent-loss gate must be rebuilt; E1 to E5 lapse | Per-issue text until S15c |

What the owner gets on the daily page: under A, B and C it can run (after `$AWR_ROOT` is set, because master's poll config rejects the `orchestrator_repo` key, `cycle.py:59`). Under D and E there is none, and Clay keeps his IronFlow copy (not checked). Until S15c the observer shows titles and links only under every option.

## 5 Implications table

| Item | If YES (restore now) | If NO (never) | If LATER (my pick) |
|---|---|---|---|
| D1 daily run skips held issues (718) | Test on hand-built entries can start; retiring the daily run still needs an owner answer (who made "owner ruling 1" is unverified) | Dropped: no daily run on master | Stays open, marked "after restore"; nothing starts before S16 anyway |
| D2 entry shows assignee and session links | Starts after C14 supplies the content | Folds into C14 and the observer | Folds into C14 now; display part waits |
| D3 where report state lives; no "person" in shipped config | Owner answers now; config change and test land in the restore | Mostly dropped; entry-file place already set by the plan | Owner may answer now (cheap); config test waits |
| D4 IronFlow copy kept in step (718) | Chat answer now; diff check after restore | One-line answer ("Clay's own copy, not tracked"); diff dropped | Chat answer now; diff check after restore |
| C14 entry content (716) | Writer work in phase 2; restore is necessary, not sufficient | Rewritten against the coordinator's own entry format | As NO until the trigger; copy field names from `common.py:133-151` |
| C8 entry line (S05-F18) | Same as C14 | A plain `report-entry` line | Same as C14 |
| FR-45 (report reads sweep session ids; live side-by-side run) | Later PR, after the sweep gains `session_id` | Dropped; the removed-worktree gap moves to FR-79 as a known limit | Stays a requirement, blocked |
| FR-46 (no person, per-user path, only `session_id`) | First half in the restore PR; second half with the writer | Dropped except "only `session_id`", moved into FR-48 | Stays; applied when restored |
| FR-48 (`report-entry` is the only writer) | Kept; built at S15c | Kept; format owned by the coordinator package | Kept; S15c fixes the format first |
| The daily report itself | Runs from this checkout (DM, waker, commit off by default) | Only Clay's IronFlow copy, if it still runs | As NO until the trigger |
| Also touched | FR-50's test name stays valid | FR-47, FR-50, FR-79 last sentence, FR-80 citation, rows E1 to E5 need edits | Mark them "deferred"; edit nothing else |

## 6 The security point
- **What is served.** `page.py:322-326` starts `python -m http.server 8765 --bind 127.0.0.1 --directory <state folder>`. That is the whole `.dev/coordinator/` folder, not one file. It holds `settings.json` (ClickUp DM channel id, `clickup.py:558-612`), `action-log.jsonl`, `priorities.json`, `wakes/`, the run folders (GitHub and ClickUp data and transcript excerpts, per the tech reference), the entry files and `report.html`. Python's server lists directories by default. The server is started detached (`start_new_session=True`) and nothing in the skill stops it; `ensure_server` also reuses whatever already answers on port 8765.
- **Reachable beyond localhost?** Not from the network: the only bind in the skill is `127.0.0.1` (no `0.0.0.0` anywhere). But `page.py` has no `Host` check, no token and no path limit (a search for host, token and bind finds only the launch arguments). So any process or other account on the same machine can read it, and a web page in the owner's browser can read it by DNS rebinding. That is Codex finding "Authenticate the localhost report server" (P2, Medium, comment 4637549094), the only one of five security findings without a "Resolved" tag in the Codex summary. Clay replied "The finding looks real ... serve only report.html, reject any Host other than 127.0.0.1:8765, and disable the listing" and left it unfixed. I found no follow-up issue. Whether a Coder port forward could expose it to other workspace users: not checked.
- **Also:** the page loads Google Fonts from the internet (`report-template.html:8-10`). A second Medium finding (a `javascript:` link in an entry reaching the same page origin) is marked Resolved.
- **Must happen before any restore:** serve a scratch folder holding only a copy of `report.html`; reject any `Host` other than `127.0.0.1:8765`; turn the directory listing off; add three tests (a request for `settings.json` fails, a request for a folder fails, a wrong `Host` fails); self-host or drop the font; stop the server when the run ends or document that it stays up. The owner should not approve a restore PR without those three tests.

## 7 Recommended sentence and follow-up
**Sentence for chat (option D):** "Do not restore agent-work-report now. Tag the archive commit d7d645ddd as `archive/pr-684-agent-work-report` so it cannot be lost. Restore it, trimmed and fixed (server serves only report.html, no Clay config, no DM or commit by default), only when I say a daily per-issue page is wanted or when stage S15c starts, whichever comes first."

**What the coordinator does after that sentence (each GitHub write needs the owner's own go; none was made here):**
1. Tag: `git tag archive/pr-684-agent-work-report d7d645ddd`, then push the tag to `origin` (`IronbellyOrg/IronClaude`). A tag is needed; no issue is needed for it.
2. Edit issues 716 and 718, do not close them: in 716 C8 and C14 and in 718 D1 to D4, replace "needs the report-skill restore decision" with "restore deferred; trigger is the owner asking for a daily page or the start of S15c". Edit `SPEC.md` Appendix B.3 action 1 to "deferred, tagged", and mark FR-45, FR-46 and FR-48 deferred, not dropped. Leave FR-47, FR-49 and FR-50 as they are.
3. File one new issue, "Fix the localhost report server before any restore of agent-work-report" (the three-part acceptance test above), because no follow-up exists and this is the one thing that must not be forgotten.
4. Chat answers the owner can give at once: D3 (where report state lives; default the per-user config folder) and D4 ("the IronFlow copy is Clay's own; IronClaude does not track it until a restore"), after Clay answers the two facts.
5. If the owner says YES instead, the next step is one `/sc:pr-submit --monitor 3` PR from an Orca worktree with an agent, with the server fix and its three tests as a merge gate.

## 8 What I could not verify
- Whether Clay's IronFlow copy still runs the daily report, and whether the two Orca automations point at it (no IronFlow folder under `/home/coder/workspaces`; the automations live outside the repo).
- Whether the owner wants a daily per-issue page for himself. This is the real fork; neither side had evidence.
- Why the skill was in Clay's rollback request, and whether a restore would be welcome to him.
- Whether the test file passes on today's master (I ran nothing), and whether a restore conflicts with the 8 newer master commits.
- Whether `superclaude update` removes the old skill folder on hosts that installed it between 00:02 and 15:07 UTC on 2026-11-20.
- Whether a Coder port forward exposes port 8765; whether all 36 review threads on PR 684 show resolved (I confirmed only the Codex summary lines).
- The hour figures are my estimates from line counts and the PR 684 review load, not a trial.

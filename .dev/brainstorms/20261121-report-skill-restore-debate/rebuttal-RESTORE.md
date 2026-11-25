# Rebuttal (round 2), advocate for RESTORE

Read: `position-NOT-RESTORE.md` (the opponent's paper, "NR" below). I opened every file and line I cite. Read-only; no GitHub writes.
Counts and quotes were re-checked on the archive branch `origin/clayphi/archive-orchestrator-655-20261120` and on `origin/master`.

## 1. Facts I checked in NR's evidence

**Confirmed (I could not fault them):** sizes (16 scripts, 5,777 lines; 7 templates, 479; test 4,005); "Clay" appears 58 times in `SKILL.md` (`grep -o -i clay`, my "36 lines" in round 1 counted lines, both right); PR 684 opened 2026-11-19T23:31:53Z, merged 2026-11-20T02:01:07Z by clayphi, `reviewDecision` empty; Clay's reply in the Codex thread (I read it through `gh api .../pulls/684/comments`, it says "The finding looks real ... serve only report.html, reject any Host other than 127.0.0.1:8765, and disable the listing."); 36 of 36 review threads resolved (GraphQL read); only the tag `archive/pr-682-issue-pipeline-removal` exists; `waker.py` types into a terminal through `orca_term.send`; FR-80, OA-17a, OA-25a, `techref:791` and `:1303`, `DECISIONS.md:33,35`, `sc-closeout.md:368` (on master), `clickup.py:596 send_dm`, C27's "The owner must say a push is wanted". My search for a follow-up issue for the server finding found only issue 718 (which mentions it in D3), so NR's "none found" stands.

**Wrong or out of context:**
1. **NR A3** says the report's tag `coordinator` and prefix `coordinator-` "clash with the owner's `COORD-<RepoName>` name (D08 verdict, `SPEC.md:226`)". The D08 verdict says the opposite: `debates/D08/VERDICT.md:22` "**Report session unchanged.** Tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/` ... It is not renamed.", and `:46` "Why: a verified collision with the live tag, automations and state folder if renamed". `SPEC.md:226` is FR-24 (command and skill names), not the report. NR's section 8 condition C3 ("renames the tag and prefix to the D08 names") repeats the error.
2. **NR section 4, last paragraph** says "D11 says both are 'spec text only'" about the nine-row table and the cap, citing `VERDICT.md:45`. Line 45 is OURS' strongest point 3 in the "Strongest points" list, an advocate's claim, not the verdict's finding. The verdict's own action keeps both as adopted-with-change or proposal.
3. **NR R1(b)** offers "the chat report" as the owner's interim surface, from `VERDICT.md:84`. In that row the sentence is "report owns GitHub reads and text; the chat report is the interim surface", and `debates/D11/adversarial/adversarial/diff-analysis.md:25` says "the report is an interim second layer". The chat report is the skill's own Step 13 summary posted in the session. Under NO it does not exist, so R1(a), (b) and (c) all lean on the thing NO removes (my reading; the verdict does not define "chat report").
4. **NR A5** cites `SPEC.md:226, 242` for FR-40 and FR-26; FR-26 is at line 228 and line 226 is FR-24. Trivial, but the typing-rule argument rests on FR-40 only.
5. **NR A4** says S15c is "months of review and live tests away". No cited line says months; `SPEC.md:65` says only that nothing of the flow has run live. Unverifiable.
6. **NR section 7** moves FR-45's question "to FR-79". `SPEC.md:262` (FR-79) ends: "The report runs its own `sweep run --window <time since its last report>` when a file's window is shorter." FR-79 itself names the report. And FR-80 (`SPEC.md:263`) cites `skills/agent-work-report/scripts/common.py:139-141` as its source for "model-written" fields. NR's list of affected requirements (FR-45, 46, 47, 48, 50) misses FR-79 and FR-80.

## 2. What I accept, and what changes in my position

- **Accept NR A2 in full as a merge gate.** Clay's recorded fix is a three-part acceptance test: serve only `report.html`, reject other Hosts, no listing. Commit 2 must pass it, with a test per part. NR is right that 36 of 36 threads show resolved without a code change.
- **Accept NR A5 and O9 in part: outbound side effects come out of the default.** `SPEC.md:113` (OA-25a) says "No push notice in the first build". So commit 2 makes the ClickUp DM (`clickup.py dm`, `waker.notify`) and the waker's typed text off unless a setting turns them on, and creates no Orca automation. ClickUp stays as a read source. This is a scope cut from round 1, where I kept them as is.
- **Accept NR's point that Step 14's model-run `git commit` should not ship by default** (`SKILL.md:161`). I now drop it from the default flow (round 1 only flagged it).
- **Accept NR R4: tag the archive commit now,** `d7d645ddd`, for example `archive/pr-684-agent-work-report`, whatever the decision. Only the owner can push it; I made no write.
- **Accept NR A4 as true about the living half** (no writer; `techref:805`). It stays a stated limit in the PR body, as in round 1. I no longer use "has run live" (my A4) as a main argument: the "VERIFIED" marks are code comments from the IronFlow period, and use since is UNVERIFIED.
- **Accept NR section 7 on D1 and D3 in part:** if the answer is NO, D1 is moot and most of D3 disappears. If YES, D1's retirement of the daily run still needs an owner answer (issue 718 D1 watch-out), which I said.
- **No change** to the two-commit structure, the "owner reads commit 2" review plan, or the rule that the author does not merge.

## 3. Answers to NR's remaining arguments (new evidence only)

**NR A1/O4/O7 (big, unreviewed code).** NR's own concession C3 describes my PR: a restore that "already fixes the server finding, removes `"person": "clayphi"` and the Clay text ... and keeps the archive's tests green, so the owner's review is of a diff". It lists renaming the tag as part of that, which D08 forbids (section 1, item 1); take that out and C3 is met by the plan I wrote. The person-specific footprint is small: only 17 lines across 10 scripts read `CONFIG` person, name, orgs, time zone or ClickUp keys (my grep of the archive), the literal `clayphi` appears once in the skill (`config.json`) and 5 times in the test file. Round 1 said "tens of lines" for the server; the function `ensure_server` is exactly 36 lines (`page.py:308-343`).

**NR A3 (one-person tool, ships to every host).** Same footprint figures. The names the owner chose for the report session are kept by D08, so the amendment does not touch them.

**NR A4/O5 (a reader with no writer; the coordinator can own the schema).** The plan text that reaches into the skill is wider than Appendix B.2 lists: FR-79 (the report runs its own sweep), FR-80 (cites `common.py:139-141`), FR-50 (names the test file), and OD-9 "info streams off with a switch" (`SPEC.md:105`), where the only "info" stream I found is the skill's `orchestrated/info/` folder (`SKILL.md:16`: "information items go to `orchestrated/info/`"; my reading, UNVERIFIED that OD-9 means it). Under NO each needs a rewrite. NR's own R4 says S15c should "keep the entry-file field names compatible with `common.py:133-151`"; that file is the only place the names exist, and PR 684's body says "The spec does not name the fixed fields".

**NR A6/O3 (five allowlisted fields replace the report).** The five fields "done, left, needs a person, link, last update" contain prose. NR says "no model call" (R1c). Who writes "done" and "left" without a model? The coordinator writes entries, so the prose is model-written there too, and it is the item template again. Also, until S15c the observer shows "titles and links only" under both options (`SPEC.md:263`), so NO does not give the person more before S15c; it gives less (no daily page at all).

**NR R2/O6 (silent loss as one S16 test).** NR itself cites `techref:791`: seven checks plus a sha256 chain, and `SKILL.md:21` requires carry-forward: "Every item open in the previous report is listed or closed". A screen that has no previous report cannot test that. One "could not read" test covers a sweep screen, not an item list across days. NR agrees the gate would cost more to rebuild (O6).

**NR A7 (owner's queue).** NO is not free of owner work: NR section 9 asks for four owner actions (tag, chat answer, spec rewording of FR-45 to FR-50, closing or rewriting D1 to D4) and a spec edit pass on a document the spec says was "NOT re-reviewed" (`SPEC.md:754`). YES asks for one reviewed PR plus the same chat answers.

**NR A8 (IronFlow copy serves Clay).** There is no IronFlow folder under `/home/coder/workspaces` here, so neither side can read that copy; NR's R5 ("IronClaude does not track it") leaves the one code base the plan's FR-46 and FR-50 are meant to govern outside review. This is a judgment call; the fact is UNVERIFIED for both sides.

## 4. Final position

I still say restore, only if all of these hold:
1. One PR, two commits; commit 1 is empty against the archive (`git diff <archive> -- <skill folder> tests/skills/test_agent_work_report.py`).
2. Commit 2 holds exactly: the three-part server fix with three tests; FR-46 first half (per-user config and state path, no person or ClickUp ids in shipped files, neutral description); `SKILL.md:12` wording per D08 with the report-session names left unchanged; DM, waker automation and Step 14 commit off by default; the audit row in `test_worker_contract.py`; a PR body that says the living half has no writer.
3. The owner answers issue 718 D3 (where state lives) before commit 2 starts; the owner or an independent reviewer reads commit 2; the author does not merge; Clay is asked the two facts (why the skill was in PR 700, whether the daily report still runs from IronFlow).
4. The owner tags `d7d645ddd` first, so nothing is lost either way.

**Cost (my estimate, not measured).** Commit 1: no authored lines; 26 files, +10,476 lines (`git diff --stat` against master); about 1 hour with `make sync-dev`, `make verify-sync` and the test run. Commit 2: about 120 to 300 changed lines and 8 to 12 new tests. Basis: `ensure_server` 36 lines; 17 config-reading lines in 10 scripts; 75 test lines that mention `waker`, `send_dm`, `ensure_server`, `http.server` or `8765` and will need an off-by-default switch; `SKILL.md` text edits. About 4 to 8 builder hours plus 2 to 4 hours of review-loop time.

**What I drop:** the waker and DM as default behavior; Step 14's model commit; "has run live" as an argument; any claim that R1 fixes `/sc:closeout`; the idea that D1, D2 and C14 start without the owner's chat answers.

## 5. Where we agree

Both sides now agree the skill must not return as it stands: the server hole and person config must be fixed first, the owner must review it, and the archive commit should be tagged; we differ only on whether that fixed skill comes back now or is rebuilt in pieces later.

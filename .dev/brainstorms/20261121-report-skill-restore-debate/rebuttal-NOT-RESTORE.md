# Rebuttal (round 2), advocate for NOT RESTORE

Read: `position-RESTORE.md` ("RP") and `rebuttal-RESTORE.md` ("RR"). Checked on the archive branch `origin/clayphi/archive-orchestrator-655-20261120` (archive) and `origin/master`. Read-only; no GitHub writes. Estimates are mine and unmeasured.

## 1 Facts checked in their evidence

Confirmed as they state: `ensure_server` is `page.py:308-344` (37 lines); `orchestrator_repo` appears nowhere in master `src/`; `_TOP_KEYS` is at `cycle.py:59` and the unknown-key check at `:223`; FR-79 (`SPEC.md:262`) ends "The report runs its own `sweep run --window ...`" and FR-80 (`:263`) cites `common.py:139-141`; D11 `VERDICT.md:84` says "the chat report is the interim surface". Not rechecked: their review counts by login (67, 26, 21), the "142 test functions", the 116-line master drift.

Wrong, out of context or unverifiable:
1. **My A3 was wrong on naming.** `debates/D08/VERDICT.md:22`: "**Report session unchanged.** Tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/` ... It is not renamed." Line 46 adds "a verified collision ... if renamed". `SPEC.md:226` is FR-24, not the report. My section 8 condition C3 (rename the tag) is withdrawn.
2. **My section 4 misattributed "spec text only".** `D11/VERDICT.md:45` is OURS' strongest point 3, an advocate's claim. The verdict's own table adopts the nine rows "with change" and the cap "as a PROPOSAL".
3. **My "months away" for S15c** has no cited line. Withdrawn.
4. **RP A1 says the rollback was "for a reason ... about process".** RP N2 and R9 say Clay's reason is UNVERIFIED, and PR 700's body gives none specific to the skill. A1 contradicts N2.
5. **RR section 3 reads OD-9 ("info streams off with a switch", `SPEC.md:105`) as the skill's `orchestrated/info/` folder. That is wrong.** FR-09 (`SPEC.md:199`) puts "the three info streams" of the watcher poll behind an off switch; `QG4/VERDICT.md:16`: "keep the info streams off ... The report does not list newly assignable issues now." So OD-9 needs no skill. (Honest note: `QG4:22` gives "duplicate the report's `involves` search" as one of its reasons; under NO that reason goes, the answer stays off.) This also settles my round 1 UNVERIFIED on OD-9.
6. **RP A2 and RR on FR-44.** FR-44 (`SPEC.md:255`) reads only `issue-watch status --json` and the sweep JSON. The entry files in D11 line 28 are written by `report-entry`, not by the skill; the skill only reads them. RP's "dashboard text depends on this skill's contract" is true only of the field names in `common.py:133-151`.
7. **RR's "17 lines read CONFIG" measures config reads, not person neutrality.** The word Clay appears on 104 lines in 16 files (`grep -w`): `SKILL.md` 36, templates and page JS 16, scripts 52. The 52 lines in `SKILL.md`, templates and page JS are text the model or the reader sees; I did not sort the 52 script lines into comments and code. The test file has 29 lines with "Clay", 73 with "waker", 14 with DM calls, and none with `http.server`, `ensure_server` or `8765`, so the server has no test today.

## 2 What I accept, and my answer to the two-commit offer

Accepted in whole: items 1 to 3 of section 1 (my errors); RR's point that NO gives the person less than YES until S15c, since the observer shows "titles and links only" either way (`SPEC.md:263`) and my "chat report" interim surface has no definition in the verdict. Under NO the interim human view is the `/sc:sweep` report plus `issue-watch status`, which carry no per-issue text. Accepted in part: FR-79 and FR-80 need two small wording edits under NO (delete the last sentence of FR-79; change FR-80's cited source). That widens my list of touched requirements to FR-45 to FR-50, FR-79, FR-80.

Changed in my position: I withdraw "rename the tag", "months away", "spec text only" and the OD-9 doubt. I now accept that the server finding and the person config are fixable, and that RR's three-part server test (serve only `report.html`, reject other Hosts, no listing) is the right gate.

**The offer: one PR, two commits, byte-identical restore then a small fix commit. My answer: no to the full 16 scripts; yes in principle to a trimmed core (section 4).** Reasons the offer is not small:
- RR's commit 2 now also turns the ClickUp DM, the waker's typed text and Step 14's commit off by default. That is a redesign of Steps 13 and 14, not a fix the plan asked for (D11 kept DM and commit in the report, `VERDICT.md:64`). It touches `waker.py` (405 lines), `clickup.py send_dm`, about 87 test lines (73 waker plus 14 DM) and the `test_worker_contract.py` audit row, which exists only because of Step 14.
- Code that is off by default is still reviewed, tested, kept in step and installed on every host. RP R3 admits `SKILL.md` Boundaries says it "never ... starts or messages agents" while `waker.py` types into a terminal.
- The server has zero tests, so all three server tests are net new on a function nobody has tested.
- Squash is how this repo merged the skill before (`inventory/clay-prs.md:111`, "squash-merged"; my inference that it would again). Master would show one large commit, so "owner reads only commit 2" holds in the PR view and not in history.

## 3 Answers to their remaining arguments (new evidence only)

**"Restore the reader first so the writer is built against it" (RP N6b, A6).** The entry contract at `common.py:133-151` stores a `session_status` map ("<session id> to <status>: <reason>"), the model-written `recommend`, `how` and `suggested` slots, and `orchestrator{id, tag, session_id, link, tier}` and `worker{session_ids, link, title, branch, tier}`. The plan says the opposite: FR-46 and D11 "entry files store only `session_id`" with the class "read live", and FR-80 never shows `recommend` or `suggested` and hides `how`. RP defers that schema change to a later S15c PR. So reader, `exclude.py`, `refresh`, `render.entry` and their tests would be reworked a second time. Restoring now pins the schema the plan means to change.

**"The decision blocks six backlog items" (RP A6).** By RP's own table, C14 and the C8 entry line are "Can start; still needs the writer", the same state as under NO, because both are S15c writer work. What YES unblocks is D1 tests, the D3 config change and the D4 diff, which are work the restore itself creates. NO closes D1, most of D3 and half of D4, and folds D2 into C14. Neither answer moves the C14 and C8 critical path.

**"The silent-loss gate has no equal" (RP A3).** I said in round 1 that `check.py` could be lifted later. I checked and I was too easy: `check.py:73` enforces the shape of `templates/item-template.md`, and the delivery gate chains sha256 values of `overview.md`, `report.html` and `summary.md` (`techref:791`). The gate is welded to the report's own files. It comes with the render stack or it is rebuilt as a property. That favours "core or nothing" over piecemeal lifting, and I now argue only those two.

**Cost (RR: 4 to 8 builder hours plus 2 to 4 review).** Their basis (37 server lines, 17 config lines, 75 test lines, `SKILL.md` edits) leaves out the Step 13 and 14 redesign, the 52 model-facing Clay lines, the 29 test lines that say Clay, and the new server tests. My estimate for their commit 2: 300 to 600 changed lines, 12 to 20 new or edited tests, 8 to 16 builder hours plus 3 to 6 review hours (11 to 22 in all). For my own path: spec edits (FR-45 to FR-50, FR-79, FR-80, rows E1 and E2) 1 to 2 hours, one S16 "could not read" test about 2 hours, tag minutes: 3 to 5 hours. Basis is line counts above, not a trial run.

**"A diff against the IronFlow copy needs the restore" (RP N7).** The diff needs the IronFlow files, which neither of us can read (no such folder on this host, RP section 2). A restore does not make them readable.

**"Owner queue" (RR on my A7).** Fair: NO costs the owner four actions. YES costs the same chat answers plus a review of commit 2 and a D16 merge decision. I drop A7 as a main argument.

## 4 Final position

**I still say NO** to: the full 16-script skill with DM, waker and Step 14 off by default; any restore without a recorded owner reason for a per-issue page; any restore that carries the living half (`exclude.py`, `refresh`, `render.entry`) before a writer exists.

**I would concede to a partial restore ("daily core, living half later")** if all of these hold:
1. The owner records in chat that a per-issue plain-English page is wanted in IronClaude, for Clay or a named second person (my old C1 and C4).
2. Scope: collect, match, classify, compare, check, render, page, run (without Steps 13 DM and 14 commit), common, the 7 templates, and their tests. Removed, not switched off: `waker.py` (405 lines), `clickup.py send_dm` and the DM path, `exclude.py` (109), `refresh` and `render.entry`, Step 14, the audit row in `test_worker_contract.py`. ClickUp stays as a read source. Kept and fixed: the page server, serving only `report.html`, rejecting other Hosts, no listing, with three tests (RR's own gate).
3. Person-neutral: no `clayphi`, no ClickUp ids, neutral description, per-user state path (FR-46 first half); D08 names for the report session unchanged.
4. Archive tagged first; Clay asked the two facts; the author does not merge; the owner or an independent reviewer reads the trimmed diff.
Size: this drops about 10 percent of the 6,471 skill lines at once (waker and `exclude.py` alone are 514) and more once `refresh`, DM and `render.entry` go; the risk surface drops more than the line count. My estimate: 6 to 12 builder hours plus 3 to 5 review hours, basis the line counts in section 3.

**What the owner loses, by choice** (estimates are mine):
- **NO now (3 to 5 hours):** no per-issue page, no ClickUp view and no silent-loss gate until rebuilt (the gate must be rebuilt as a property, section 3); less than YES for the person until S15c; D11's E1 to E5 adoptions lapse. Gains: no 10,000-line review, no typist or DM code, D1 to D4 closed, no schema pinned.
- **Their two-commit full restore (11 to 22 hours by my estimate):** keeps every D11 adoption and a working daily page. Pays: a large review, DM, waker and commit code that ships off by default, a schema the plan will change, and reworks of the living half after S15c.
- **Daily core (9 to 17 hours):** keeps the page and the gate; loses the waker and DM (Clay's automations stay on IronFlow) and the living half until S15c, where the writer and a schema consistent with FR-46 come first.
If the owner wants a restore at all, I prefer the daily core to the full offer.

## 5 Where we agree

Both sides now say the skill must not return as it stands (server fix, person-neutral config, owner review, no author self-merge, tag `d7d645ddd`, keep D08 report-session names); we differ on whether the fixed skill returns whole now, trimmed to a daily core, or later in pieces.

# Round 2 rebuttal for variant 4 (#423 v2 and the #339 boundary)

Advocate: read-only (GitHub and all checkouts); this file is the only thing written. Re-checked on 2026-11-14 against the review checkout (`873599d59`), `origin/master` (`d2d8a2d16`), `gh` reads, and `/home/coder/workspaces/Coder` read-only. "R1-Vn" = round1-advocate-Vn.md, "R2-Vn" = round2-rebuttal-Vn.md, "digest" = round1-contested-digest.md. Convergence after Round 1: 63.9% (23 of 36 points agreed).

## 1. Response to each criticism raised against V4

Sources: R1-V1 section 4 items 3-5, 8, 11; R1-V2 items 7-9; R1-V3 items 2-4, 7; R1-V5 items 7-9, 12; R2-V1 rows 3, 4, 8 and section 2; R2-V2 section 2; R2-V3 section 2. Repeats are grouped. Eleven criticisms: I concede eight in full or in part (rows 1-5, 7, 8, 11), counter one in part (row 6), and agree with two while adding a newly checked fact (rows 9, 10).

| # | Criticism (who) | Response | Evidence (checked now) |
|---|---|---|---|
| 1 | V4 missed the built observer; (a)/(b) and #423 edit 3 ("both read the same sweep facts", "no second scanner of Orca") rest on a single source (V1, V2, V3, V5) | **Concede in full.** Edit 3 is withdrawn as worded. Replacement is in section 5.7. I do not accept V5 BC-17 ("or the observer's snapshot") either (response 9). | `ls src/superclaude/cli/` lists `observe`; both cross-reference greps exit 1 (R1-V4 verification log); `adapter.py:29-32` |
| 2 | C8 and F19 prove the boundary sentence with the sentence itself (V1, V5) | **Concede.** Already withdrawn in R1-V4 concession 2; R2-V1 row 8 accepts that. Keep only "distinct". | live #409 line 119 (only occurrence) and line 212 ("distinct from this view"), re-read |
| 3 | F17 says the sweep "confines every path" (V1, V2, V3, V5) | **Concede.** True for file reads, false for git targets. New point in V4's favour: R2-V1 section 5 item 1 reframes the risk as untrusted repo content, not other users. That is a better reason for F17's read-permission AC than the one V4 gave, and I adopt it (section 5.3). | `probes.py:1203-1214`, `:309`, `:525-531` (R1-V4); `models.py:127-138` (new, section 5.3) |
| 4 | F16 counts too few cadences; the watcher cron and the observer's 15 s poll are missing (V2, V3, V5) | **Concede.** The principle (decide cadence once) stands; the count was wrong. Cadences found now: WC-16 at most every 5 minutes; observer every 15 s (`collector.py:28`); watcher cron every 5 minutes, a follow-up not yet enabled (`docs/designs/issue-watcher.md:15`, FU-2); PM checkpoint every 30 minutes (`skills/sc-pm-protocol/SKILL.md:46`). A v2 timer would be a fifth. | files cited |
| 5 | #423 edit 3 builds "all workspaces" on Coder#477 as the only planned channel without saying the watcher design makes #477 unnecessary under option A (V3) | **Concede, one clause.** The text must read "if Coder#477 is kept". The design says "Option A makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited" (`issue-watcher.md` section 2.2, re-read in R1) and the owner has not said whether the 2026-11-13 comment revisits it. | R1-V4 verification log; Coder#477 comment re-read |
| 6 | V4 (c) and #409 edit 1 ("one grant vocabulary") have a consumer only if a listener exists (V3 item 4) | **Counter in part.** The vocabulary has consumers that do not depend on #477. #339 comment 2 Step 3 applies grants to children of one Orchestrator and to "the orchestrator-of-orchestrators in version 2" (re-read, comment 2 line 41); neither involves a listener. What I concede: the edit should not claim a listener consumer, and V4's wording must stay conditional ("if a listener is built"). The watcher's own trust (approvers file, labels, integer-only prompt, `launch.py:33`) is a different local model that grants do not replace; V3 R2 row 5 now says so in Edit 7. | #339 comment 2 line 41; `launch.py:33` |
| 7 | F13 treats two schema requests as one contract (V5, via A-014) | **Concede.** There are at least four contracts (R2-V3 X-006): sweep report JSON v1, observe snapshot v1, the watcher's `status --json` and `dispatch.json`, and any v2 record. V4's "decide once" survives only as "decide the relationship once (V5 D1), then each owner decides its own keys". | `snapshot.schema.json` required keys (below); `report.py:642-661`; `issue-watcher.md:398-404` |
| 8 | C7/F11 and edit 7 repeat "one ordinary session" and omit the second governed agent (V1, V2, V3, V5) | **Concede.** R2-V2 D-D narrows the effect (a re-claim is mostly idempotent, so the extra agent appears once per issue), which lowers severity but not the omission. The #423 #331 line carries the caveat (section 5.7). | `commands/issue.md:43,88`; `launch.py:33` |
| 9 | V4's own critique of BC-17 is right, but V4 offers nothing in its place (R1-V5 concession 6, R2-V1 D-4, R2-V2) | **Accept the three-way agreement and make the replacement concrete.** The observer snapshot's 15 required row keys are `dispatchId, taskId, runId, workerState, dispatchStatus, terminalState, role, provider, hostKind, hostId, stage{worker,dispatch}, outcome, liveness, evidence, nextAction` (re-read from `origin/master:src/superclaude/cli/observe/snapshot.schema.json`): none carries a command, objective, branch, changed path, issue or PR. The sweep's model holds `ContractRecord.command` (`models.py:121`) and `WorktreeState.changed_paths` (`models.py:200`) but its JSON emits neither. So for v2's catalogue **no existing JSON carries the fields v2 names**; the field list must come first (my AC 1), and each field gets a named source. | schema re-read; `models.py` re-read |
| 10 | V5 D1(a) "keep separate" prices only the observer; v2 and a status route need sweep output that can be read without re-running the sweep (R1-V1 item 8) | **Agree with the premise and add a new constraint.** The obvious repair (a stored `<stem>.json` beside the report) is blocked by a pinned requirement: `tests/sweep/test_readonly.py:396-402` asserts the sweeps folder holds exactly one name, the report (re-read; R2-V1 and R2-V3 cite the same pin). So v2 cannot assume "persist the JSON" is cheap. The coordinator already runs the sweep every pass and receives the JSON on stdout (`commands.py:275-278`), so a v2 pass can consume stdout without a new file. That is a design option for v2's brainstorm, not a decision. | `test_readonly.py:396-402`; `commands.py:275-278` |
| 11 | V4 gave no recommended answers and no severity (V3 R1 item 5, diff S-005) | **Concede; recommendations were supplied in R1-V4 section 8 item 13 and are restated in section 5.7 as acceptance criteria.** Severity stays derived, not V4's. | n/a |

**One self-correction nobody raised.** R1-V4 F7 and section 3 item 3 said "a worker cannot message peers (WC-13)". WC-13 (`WORKER-CONTRACT.md:62`) forbids a worker from starting workers or sessions (`worker-start`, `dispatch`, `task-create`, `agent launch`); it does not name peer messages. What the contract shows is that it defines no worker-to-worker channel (lifecycle messages go to the coordinator, WC-7 and WC-12). The conclusion of F7 holds; the citation was loose.

## 2. Updated assessment of V1, V2, V3, V5 and of their Round 2 claims

**V1 (up on its sweep-side facts, down on its premise).** R2-V1 is a model concession: it gives up the false premise, withdraws the rebase claim, and agrees with V4 on X-002, X-007 and BC-17. Claims I now rely on, all re-checked: the sweep prints JSON after publishing a report (`commands.py:275-278`); persistence is blocked by the one-file pin (`test_readonly.py:396-402`); `_worktree_paths` and `_git` (`probes.py:1203-1214`, `:305-327`) execute git in every Orca-listed checkout with inherited environment. One claim I do not accept as stated: R2-V1 A-007 says "the live risk is not other users but untrusted repo content". Both exist; v2 adds a third (agent-written text, section 5.4). Its D-4 (BC-17) I accept.

**V2 (up, with one unverified live fact).** R2-V2's reframing of W-10 ("do not add a watcher panel to `observe` before FU-1") and its third contract (watcher `status --json`, `dispatch.json`) are right and change my store inventory (section 5.2). Its new live observation (27 agent rows, no slash-command `prompt`) I cannot re-run; it remains UNVERIFIED by me and it only bears on D-B (labelling a watcher session by its agent row). It supports, not weakens, V4's per-class AC amendment.

**V3 (up on trust and scope; one gap in its Round 2).** R2-V3 concedes Edit 5 and Edit 8 and adds a fact I verified: new Claude sessions on the stock image run with permission checks off unless `CCSESSION_PERMISSIONS=default` (`ccsession:135-141`; `templates/VSCode-AIDev02/README.md:60`, "Permission checks are off for every call the wrapper routes"). That raises the stakes of any relay (section 5.4). Its clause on edit 3 ("if #477 is kept") I accept. Its D-7 proposal (use the Coder control plane for workspace identity) rests on docs and no live call; it is a candidate for v2's later cross-workspace step, not evidence.

**V5 (the decisive correction, with three limits that Round 1 left in place).** Its core is verified and unchallenged. Limits: BC-17 is now withdrawn by V1, V2 and V5 itself (R1-V5 concession 6); "keep two readers" is right for the observer and neutral for v2; R2-V1 argues the questions-read consumption evidence is not diagnostic on a live coordinator Run (R2-V1 section 5 item 2); I did not open `owner-decisions-20261111.md` and leave that UNVERIFIED. For v2 the practical consequence is that no v2 acceptance criterion may depend on message reads.

**Net movement of V4:** F1, F7, F8, F9, F14, F17 (with the corrected reason) are now agreed or unchallenged by all four other advocates; F13 and F16 are reframed (not dropped); F18 shrinks; (a)/(b) are replaced.

## 3. Final verdict on the contested points

Winner = the variant (or "process") whose statement is best supported after Round 1 and Round 2 of V1, V2, V3. Confidence 50-100%. Where I changed my Round 1 answer it is marked.

| id | Verdict | Winner | Conf. | Concrete course of action |
|---|---|---|---|---|
| A-002 | The unit differs per program: sweep rows are Run-bound while `worktrees[]` and transcript scans are host-global (`probes.py:1203-1214`); the observer reads all Runs on one host, paged (`adapter.py:29,57`); the watcher is one workspace and one `gh` login (`issue-watcher.md:15`). A fourth unit, the Coder workspace, has no key in either program (V3: every workspace has `/home/coder`). Run-less sessions are outside the observer ledger and appear in the sweep only as transcript rows. | V5 (observer), V1 (sweep), V2 (blind spot), V3 (workspace) | 82% | Relationship note: one line per unit. v2's first release declares its unit as one host, several Runs; "all workspaces" is a later step gated on the #477 decision and an identity key. |
| A-004 | PR #539 is open at `873599d59` with two unresolved threads (re-read, `updatedAt` 2026-11-13T00:45:26Z); additive keys change a pinned golden key set (design `:599`); a sidecar file breaks the one-file pin (`test_readonly.py:396-402`). | V1 | 88% | Add no key, no file and no observer or v2 wording inside #539; log the stale design lines and the F-07 git-target decision in #534; the two threads are the PR author's to resolve. |
| A-005 | **Changed from R1-V4 ("V4").** No advocate defends the assumption; the digest split is labelling. Only a reading list exists for Phase 2, #444 is an open evaluation, observer R3/R4 have no package. | process (none defends it) | 85% | One table in #534: item, owner, trigger; unowned items labelled "unowned". For v2 specifically, #423 names its gate concretely (section 5.7) so that one item is not unowned. |
| A-007 | True today: one owner, one OS user, one host, one enabled watcher per login (`issue-watcher-setup.md:642`, per R2-V2). The live exposure is untrusted content (repo config, issue text, and for v2 agent-written text), not other users only. | V4 and V3 (state it; read-permission AC), with V1's untrusted-content angle | 80% | State "single owner, single OS user, single host" once in the relationship note and in #477; add a read-permission AC to #423 before any cross-user or cross-workspace read; treat Orca-listed worktrees and any transcript content as untrusted input. |
| A-008 | The sweep needs a bound Run and a coordinator running the WC-16 pass; the observer ledger needs neither but sees only Orca workers; watcher-launched and person-started sessions have no Run and are a blind spot in both. | V2 with V5 | 82% | Name the blind spot in both docs; v2's first release lists Run-less sessions as "not observable" instead of cataloguing them; labelling goes to a #534 row after FU-1. |
| A-009 | Unresolved by evidence. Two documents already record two builds of one Orca release (design `orchestrator-mode.md:30` ends `.780594c521aa`, technical reference `:446` ends `.9cfecdd30b2a`); the observer records none. | none | 65% | Record the Orca build and the collector name and version in the observer golden capture, the sweep lock line, the FU-1 record, and (when it exists) every v2 fact. Treat a second host as UNVERIFIED. |
| A-011 | Rejected by all five; nobody proposed the mechanism except as an action. | process | 92% | One editor, one ordered edit set per issue, every cite pinned to `updatedAt` or head sha (#409 `2026-11-13T16:57:51Z`, #423 `2026-11-08T10:16:24Z`, #339 `2026-11-07T11:53:40Z`, PR #539 `873599d59`). Order: (1) owner answers (claim level, "TUI Panel", #477 keep/narrow/close, v2 gate); (2) #450; (3) #477; (4) #409 pass (V5 corrections, then decisions 1/6/8/10, banner last); (5) one #339 comment (section 5.7); (6) #423 rewrite; the relationship note is a document and can be written alongside (2)-(4). |
| A-013 | Polling Orca CLI verbs is the only verified source for Orca facts today; event replay is unverified (live #409 line 69). Not binding on v2: #423's own text includes child-session reports at checkpoints and agents "searching sessions or diffing logs". | V5 (for the two programs), V4 (for v2) | 66% | Add to the D3 capture list: `projection.attention` values for a live and a blocked worker, and a help-text-only look at Orca's event surface. Keep a child-report path in v2's design, but only as typed fields (section 5.4). |
| X-006 | Not one decision: sweep report JSON v1 (golden-tested in #539), observe snapshot v1, the watcher's `status --json` and `dispatch.json`, and any v2 record or #477 status record. | V4 (venue for sweep keys), V5 (two contracts), V2 and V3 (more contracts) | 76% | Relationship note first, naming every contract, its owner and its join key; confirm `dispatchId` = `row_id` minus `orca:` on one real Run before calling it a join key; decide sweep keys in #339 after #539 merges and after v2 names its field list. |
| X-008 | V1's verdict line contradicts its own C-02 and F-02 and is false for the observer (it shows none of the ten dimension names); V1's tables stand. | V5 on the fact; V1's tables | 92% | Drop the verdict sentence; publish one word-mapping table (observer / sweep / Orca) in the relationship note. |
| X-009 | Tally miscount; no decision depends on it. | none | 95% | None. |
| X-019 | V5 overgeneralised. V1 stated "no observer exists"; V2 W-10 and V4 F13/(a)(b) assumed it; V3 wrote generically and did not check. | none (V5 slip) | 88% | Cite as "V1 stated it; V2 W-10 and V4 F13 assumed it; V3 did not check". |
| X-020 | W-3 is V1's proposed wording, not body text (no match in the live body, SC-19). | none (V5 slip) | 95% | Read as "do not add V1's W-3"; no body edit. |

## 4. Remaining disagreements and the single fact that would settle each

| # | Disagreement | Sides | Single fact that settles it | Who can check |
|---|---|---|---|---|
| D-1 | When and how the sweep's JSON becomes readable without re-running it (needed by v2, a status route) | R2-V1 (Phase 2 item 1, after #539, with a pairing design), R1-V5 concession 4 (now), V4 (stdout capture in the WC-16 pass is a third option) | Whether the owner relaxes the one-report-file pin (`test_readonly.py:396-402`, `test_cli_contract.py:1192,1361`) or accepts stdout capture by the caller | Owner; PR #539 author |
| D-2 | What gates #423: Phase 1 merged only, or also `/sc:close`, resume, trust layer, orchestrator of orchestrators | V4 (Phase 1 plus #534 capture), the #339 issue summary (v1 = sweep + `/sc:close` + research) | The owner's one-line answer to V4 Q1 | Owner only |
| D-3 | Should v2 read the observer snapshot at all | V5 BC-17 (yes), V1, V2, V4 (not until fields are named) | v2's field list with a source per field (the snapshot has none of command, objective, branch, changed paths, issue, PR) | The v2 brainstorm |
| D-4 | One grant vocabulary: conditional on a listener? | V3 item 4 (conditional on #477), V4 (consumers exist without it: child grants and sub-orchestrators, #339 comment 2 line 41) | The owner's #477 answer (keep, narrow, close) and whether the #339 trust layer (research Phase 4) is scheduled before v2 relays to agents | Owner |
| D-5 | Can the sweep label a watcher-launched session | V2 W-05(b) vs V4 AC and V1 | One `worktree ps --json` agent row after a real `agent launch`: does `prompt` hold `/sc:issue --claim N` and does `paneKey` equal a tab-map name | The FU-1 runner |
| D-6 | Do `check --all --types question` reads consume on a live coordinator Run | V5 O-05 vs R2-V1 D-2 | A seeded test: known `question`, `worker_done` and heartbeat messages, two reads with the observer template, then one consuming `check` returns all of them | Owner or the 409 session with live Orca |
| D-7 | Is `dispatchId` = `row_id` minus `orca:` a real join key | V5 D1 (assumed), R2-V1 D-5 | Diff the observer's dispatch ids against one sweep's `row_id` list for the same Run | Owner or the 409 session |
| D-8 | Must v2 ever deliver a course correction to a non-worker session | V4 (no; report to the person, WC-16), #423 AC ("relay them to affected agents") | The owner's answer to V4 Q4 | Owner |
| D-9 | May v2 keep a store that is shared between orchestrators given WC-16's "report is never posted" | V4 F4 (reconcile explicitly), #423 (share knowledge) | The owner's statement of the store's reader set and location | Owner |

## 5. Not yet examined by the debate: risks specific to v2 (#423) and to the v1/v2 boundary

Nothing here is posted. Every fact marked "re-read" or "re-checked" was verified on 2026-11-14; "per Vn" means taken from that report and not re-run by me.

### 5.1 Three meanings of "v1" and "v2" (not two)

| Source | What it calls v1 | What it calls v2 |
|---|---|---|
| #339 issue summary (`.dev/issues/339/issue-summary.md:6`, re-read) | `/sc:sweep` with the static report, `/sc:close`, the comment-3 research and debate | signed grants plus the orchestrator of orchestrators |
| #339 comments of 2026-11-05 (re-read) | n/a | "Version 2 should include an orchestrator of orchestrators" (comment 1); "Build Steps 2 and 3 as part of version 2, before any orchestrator-of-orchestrators work" (comment 2) |
| Phase 1 research report (`RESEARCH-REPORT-orchestrator-mode.md`, "Later phases", re-read) | Phase 1 sweep only (the owner's first-PR scope); it records the source disagreement as a `[CONTRADICTION]` and numbers Phase 2 `/sc:close`, 3 resume, 4 trust layer, 5 orchestrator of orchestrators, 6 management-server relay | Phase 5 is labelled "Version-2 work" |
| #423 (re-read) | "the v1 orchestrator (#339)", gate "after ... is complete" | the catalogue and cross-agent reviews |

Consequence the earlier reports did not draw: under the issue summary's grouping, "#339 is complete" means `/sc:close` is also done, which is Phase 2 and not on PR #539. Under the research grouping it means Phase 1 only. #423's gate therefore has at least two readings and cannot be applied as written.

### 5.2 Is a catalogue a further data store? Yes, at least an eighth.

Stores that already hold agent facts, all checked except the last:

| Store | Where | Protection and sharing | Notes |
|---|---|---|---|
| Sweep report | `<root>/.dev/sweeps/<stamp>-sweep.md` | git-ignored (`.gitignore:256`); WC-16: "a dated local file; it is never posted"; the sweeps folder holds exactly one name (`test_readonly.py:396-402`) | JSON goes to stdout only |
| Observer snapshot and export | `$XDG_STATE_HOME/superclaude/observe/snapshot.json` | mode 0600, overwritten every live cycle, per process (V5; SC-17 confirmed) | camelCase schema, `UNKNOWN` strings |
| Watcher store | `state_dir` (0700): `dispatch.json` (0600), `audit.jsonl` (0600) | per workspace and per login (`issue-watcher.md:117,398,400`; `issue-watcher-setup.md:642`) | `dispatch.json` `schema_version` 1 |
| PM memory | `<project>/.superclaude/memory/` | "one store per worktree", self-ignored with `*` (`sc-pm-protocol/SKILL.md:23`) | checkpoints every 30 minutes |
| Lessons learned | `docs/memory/solutions_learned.jsonl`, `patterns_learned.jsonl`, `reflect/` | tracked in git (`git ls-files docs/memory`), shared only through branches and PRs | the only reviewed, cross-worktree store |
| Task ledgers | `.dev/tasks/<pkg>/` | tracked in git (project rule) | per package |
| Coder heartbeat collector | central endpoint | anonymous, no auth (per V3 F14, `collector/README.md:10`; not re-run) | not an IronClaude store |

The catalogue would be another. Only two of these (lessons, task ledgers) cross worktrees, and only through git. The existing live channel to another agent is the WC-12 follow-up, which reaches Orca workers only (`WORKER-CONTRACT.md:61-62,288`). So "share knowledge between orchestrators" has no existing runtime carrier; v2 must either extend a named store or justify a new one with owner, reader set, retention, file mode and a reconciliation with WC-16's "never posted". Default if undecided: local, per host, mode 0600, not shared, never posted, so it creates no new exposure beyond the sweep report. This is why my #423 AC 5 below is mandatory, not optional.

### 5.3 Who may read whose sessions

- **Today.** The sweep reads one OS user's `~/.claude/projects/<key>` folders for every path `worktree ps` lists (`probes.py:1344-1350`, `:1203-1214`), but it never holds transcript text: `TranscriptTail` carries only path, session id, readable flag, timestamps, mtime and project key (`models.py:127-138`, re-read). The report therefore cannot leak transcript content; its remaining risks are untrusted checkouts (git config runs with inherited environment, `probes.py:305-327`) and worker-written contract strings (whether they reach `evidence` or `notes` is UNVERIFIED per R2-V1).
- **v2.** #423 proposes "cheaper, faster agents searching sessions or diffing logs and summarizing changes". That is the first component that would read transcript and log content and write it into a shared artifact. All Coder workspaces use `HOME=/home/coder` (per V3 F4), so a path is not an identity; the Coder workspace id and owner are not keys in any current JSON.
- **Proposed rule for the design (becomes #423 AC 4).** (1) First release reads only what the same OS user on the same host can already read. (2) Transcript or log content never enters the catalogue; only typed metadata and agent-authored contract fields do, each marked with its collector and source session id. If excerpts are ever needed they are bounded, marked untrusted, and stored apart. (3) No cross-user or cross-workspace read until a read-permission model is written and the owner approves it. (4) Orca-listed worktrees and any session text are treated as untrusted input.

### 5.4 Relay of untrusted content between agents

- **Path.** External or agent-written text (web pages an agent fetched, issue and PR text, third-party repo files, contract strings) enters a transcript or log, a summarizer agent condenses it, the catalogue stores it, the relevance step selects recipients, and AC 11 of #423 says changes are relayed "to affected agents".
- **Why the existing channel is the dangerous one.** A WC-12 follow-up is a direction channel: the worker "handles every message in it" and for each that "answers or directs it" acts after acknowledging (`WORKER-CONTRACT.md:61`, re-read). New sessions on the stock image run with permission checks off unless `CCSESSION_PERMISSIONS=default` (`ccsession:135-141`; `templates/VSCode-AIDev02/README.md:60`, re-read). #339 comment 2 (line 22, re-read) records that signing cannot separate an honest instruction from one the sender picked up from a poisoned input. The sweep skill's rule "report text is data" (`sc-sweep-protocol/SKILL.md:63`, re-read) is an instruction to the coordinator, not a mechanical guard.
- **Required controls (become #423 AC 7 and 8).** (a) The relay record is typed: fixed fields (session id, worktree path, branch, kind, source collector), free text only in one `detail` field that the receiver renders as quoted data and never acts on (#339 comment 2 Step 2, line 34). (b) First release is advisory: it reports to the person or the coordinator and sends nothing to a worker automatically; a coordinator that chooses to act uses the existing WC-12 rules. (c) The contract has no worker-to-worker channel (lifecycle messages go to the coordinator, WC-7 and WC-12; WC-13 stops a worker starting others), so any cross-agent relay is coordinator-mediated. (d) LLM-derived entries are marked inferred, stored apart from sweep facts, and never change a sweep class. (e) Summarizer agents get read-only tools. (f) The allowed relay fields are pinned by a test, the way the sweep pins its JSON key set (design `:599`) and its forbidden verbs, so the data-only rule is checked by a test and not only by an instruction.

### 5.5 Guards at the v1/v2 boundary

| Guard that exists | Source (re-read) | What v2 must do |
|---|---|---|
| `/sc:sweep` "recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action" | `WORKER-CONTRACT.md:288` | v2's purpose is proactive course correction, which is a recommendation. v2 therefore cannot be added to `/sc:sweep` or to the WC-16 report; it is a separate command or skill that reads sweep output and has its own contract. |
| Never-as-worker list (`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`; changes "only when the coordinator-only command set or D3 changes") | `WORKER-CONTRACT.md:23` | A new v2 command must be classified on that list in the same change. `/sc:pm` and `/sc:spawn`, which #423 lists for reuse, are already coordinator-only. |
| No Orca write verb; closed allow-list of 10 templates and 7 verbs under owner sign-off | `probes.py:62` (comment); design `:555` | v2 adds no verb to the sweep. GitHub reads for the relevance check are a v2-only collector, or a new template with a new owner note (design `:35`: "gh reads" are out of Phase 1). |
| Finished rows never print `admitted` | design `:515` | v2 keeps sweep classes unchanged; overlap is reported as possible overlap, never as conflict. |
| The sweep, WC-16 and `/sc:sweep` exist only on PR #539, not on master | `origin/master` has no `cli/sweep`; PR #539 head `873599d59` | #423 must say "on PR #539" wherever it cites them. |

### 5.6 Remaining state and guard risks for v2 (checklist for the design)

1. **Staleness.** The sweep's "stale" is relative to a 6-hour window, the observer's STALE is 45 s without a good read; a catalogue entry needs its own age rule and must show the source's age, not its own.
2. **Truth direction.** A catalogue entry is derived data; it must never be read back as a fact by a collector (the sweep never reads `.dev/sweeps/`, design `:146`).
3. **Run-less sessions.** Neither collector sees watcher-launched or person-started sessions with no Run; the catalogue must show "not observable", never "absent".
4. **Coordinator death.** WC-16 is a duty of a person-opened coordinator; if it dies no refresh happens. v2 must show catalogue age.
5. **Double cadence.** Five clocks would exist (section 1, row 4). v2 reuses the WC-16 pass or records an owner decision.
6. **Identity.** Paths are not identities across workspaces; the catalogue needs workspace id, owner login, host and Orca build per fact (A-009).
7. **Reversibility.** First release must be removable: a derived, local, deletable artifact and a command that can be unregistered, with no change to sweep JSON v1.

### 5.7 Proposed rewrite of #423 and the minimal edits to #339

Both are drafts for the owner to post or discard. They carry four corrections to R1-V4's text (data source names both collectors; per-class criterion; observer components and PRs; #331 caveat) and the "if #477 is kept" clause.

**#423 title.** `[FEATURE] Orchestrator v2 (knowledge layer): catalogue of agent work and advisory cross-agent reviews` (keeps "v2" because #339, #409 and #423's own links use it by number).

**#423 body (replaces Feature Summary, Proposed Solution, Acceptance Criteria, Out of Scope, Components Affected, Related; Problem Statement and User Story stay as they are).**

````markdown
## Feature Summary

Orchestrator v2 (knowledge layer) gives an orchestrator, here a coordinator session running the WC-16 loop, a catalogue of what agents are doing and regular cross-agent reviews that share relevant knowledge and flag duplicate or overlapping work. It is advisory: it reports to the person or the coordinator and sends no instruction to an agent on its own. In this issue "v2" means this knowledge layer. It is not the "version 2" in the comments on #339 of 2026-11-05 (trust layer and orchestrator of orchestrators); those are later #339 phases.

## Proposed Solution

Sequencing. This starts only after PR #539 (#339 Phase 1, the read-only sweep) is merged and the #534 live capture that restores the sweep's `working` class is recorded. The other #339 phases (`/sc:close`, resume, trust layer, orchestrator of orchestrators) are not prerequisites, unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are.

Start with `/sc:brainstorm --depth deep --handoff design`, then the dedicated `/tech-research` pass on multi-agent memory and context techniques (save its findings to this issue). Do not begin implementation before both are complete.

Data sources and boundaries. The catalogue reads facts through one named fact schema; the collectors are `superclaude sweep run` (per Run: class with proof, contracts, git state, transcript metadata; on PR #539, not on master) and `superclaude observe` (all Runs on one host: Orca worker rows; on master, PRs #503 and #514). Neither carries a command or objective, branch, changed paths, issue or PR today; the design names each field the catalogue needs and its source, and any schema change is decided in #339 (sweep JSON v1) or #409 (observe snapshot v1), never by a v2-only scanner. First release scope is one host and several Runs. Sessions with no Run (person-started, watcher-launched) are not observable by either collector and are listed as "not observable". "All workspaces" depends on whether Coder#477 is kept (the issue-watcher design says option A makes it unnecessary) and on a written read-permission model.

Trust and safety. Relayed knowledge is data, never an instruction: fixed typed fields, free text only in one `detail` field that is never acted on. LLM-derived entries are marked inferred, stored apart from sweep facts and never change a sweep class. The first release delivers to the person or the coordinator only.

## Acceptance Criteria

- [ ] `/sc:brainstorm --depth deep --handoff design` has been run, with its design handoff linked here before implementation begins.
- [ ] A dedicated `/tech-research` pass on multi-agent memory and context techniques is saved to this issue (it may be done ahead of the rest).
- [ ] The design names every catalogue field, where each comes from (sweep report JSON v1, observe snapshot v1, other), and which fields need a schema decision in #339 or #409; no field is added by a new scanner of Orca, git or transcripts.
- [ ] The design states the scope (one host and several Runs for the first release; several Coder workspaces only with a written read-permission model and an owner decision on Coder#477) and what is read: no transcript or log content enters the catalogue; session text is untrusted.
- [ ] The catalogue has a named store, owner, reader set, retention and file mode, says which of the existing stores it extends (sweep report, observe snapshot, watcher `dispatch.json`, `.superclaude/memory/`, `docs/memory/`, task ledgers) or why it is new, and says how it differs from the WC-16 rule that a sweep report is local and never posted.
- [ ] For each session class (Orca worker, watcher-launched, person-started, session without a Run) the design states what is observable, how a checkpoint is obtained, and how a course correction is delivered: a coordinator follow-up (WC-12) for workers, a report to the person for the rest. Labelling machine-started sessions depends on a #534 row.
- [ ] Relayed knowledge is data: a pinned set of typed fields, free text only in `detail`, checked by a test; relay passes through the coordinator (the contract has no worker-to-worker channel); summarizer agents have read-only tools.
- [ ] LLM-derived entries are marked inferred, stored apart from sweep facts, and never change a sweep class; overlapping files are reported as possible overlap, never as conflict.
- [ ] The refresh is the WC-16 coordinator pass, or the design records the owner decision for a further scheduler (existing clocks: WC-16 at most every 5 minutes, observer 15 s, watcher cron 5 minutes, PM checkpoints 30 minutes).
- [ ] The design says what GitHub reads the relevance check needs (unmerged PRs) and whether they are a v2-only collector or a new sweep template with a new owner note.
- [ ] The harness-neutral fact schema is named, with the sweep and the observer as two collectors of it (including the Mastra question, currently UNVERIFIED: nothing in the repo mentions it).
- [ ] The design lists what each review adds beyond `worktrees[].shared_package_ids`, the watcher's one-claim-per-issue rule and the observer's "changes since last look"; the "Collision Lens" design is a synthetic image, not built.
- [ ] The design and resulting components are checked against `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, with the review recorded; any new command is placed on, or kept off, the never-as-worker list in the same change.
- [ ] v2 is delivered as a separate later release after the sequencing gate above.

## Out of Scope

- v1 orchestrator work (#339 Phase 1 and later phases: `/sc:close`, resume, trust layer, orchestrator of orchestrators, management-server relay).
- A second scanner of Orca, git or transcripts; changing sweep classes or the sweep JSON v1 keys (decided in #339).
- Sending prompts or commands to person-started sessions (WC-16: they are never messaged) or to workers outside WC-12.
- A listener or workspace registry (Coder#477).
- Implementation before the brainstorm and research are complete.

## Components Affected

Existing surfaces to review, not a file list: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; `src/superclaude/core/WORKER-CONTRACT.md` (WC-12, WC-13, WC-16 and the never-as-worker list); `src/superclaude/skills/sc-pm-protocol/SKILL.md` (memory is one store per worktree, self-ignored; not a cross-workspace store) and `src/superclaude/commands/spawn.md`; `src/superclaude/cli/sweep/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `docs/designs/orchestrator-mode.md` (all on PR #539, not on master); `src/superclaude/cli/observe/` (on master); `src/superclaude/cli/issue_watch/` (starts an ordinary session; notifies no orchestrator); `src/superclaude/pm_agent/reflexion.py`, `docs/memory/solutions_learned.jsonl`, `docs/memory/reflect/` (existing lessons-learned stores); `~/.claude/skills/orchestration/SKILL.md` (installed Orca discovery stub, external).

## Related Issues/PRs

- #339: orchestrator; Phase 1 is PR #539. Its comments use "version 2" for the trust layer and orchestrator of orchestrators; this issue is the knowledge layer.
- #409 and PRs #503, #514: the read-only observer (`superclaude observe`) is built; it shows the human what happened, this layer shares knowledge between agents.
- #331: issue watcher, built (PRs #447, #448; rollout #450). It starts an ordinary `/sc:issue --claim <N>` session through `orca agent launch` and notifies no orchestrator; the claim at its default level also launches a second governed agent (#450).
- #450: watcher rollout.
- #444: sub-orchestrator evaluation (open); relevant to who holds a catalogue when a coordinator sits under another.
- #534: Phase 1 follow-ups; the `working` class and agent-wait rule gate what a catalogue can say.
- PR #539: Phase 1 of #339, the sweep.
- IronbellyOrg/Coder#477: workspace listener; the only planned cross-workspace channel if it is kept (the watcher design says option A makes it unnecessary).
- #326: Git/GitHub communication improvements, not the catalogue itself.
````

**#339: minimal edits.** One comment, no body edit, no scope change (the issue body stays as the owner wrote it):

````markdown
Terminology and links only; no scope change.

1. Version numbers mean three things in this repo. The issue summary puts `/sc:sweep`, `/sc:close` and the comment-3 research in version 1 and signed grants plus the orchestrator of orchestrators in version 2. The Phase 1 research report numbers later phases separately: Phase 2 `/sc:close`, 3 resume, 4 trust layer, 5 orchestrator of orchestrators, 6 management-server relay. #423 uses "v2" for a different release, the knowledge layer (catalogue and cross-agent reviews). From here: "Phase N" means the research report's phases; "version 2" in the 2026-11-05 comments means Phases 4 and 5; #423 is the knowledge layer and starts after PR #539 and the #534 capture.
2. Related: #409 (observer built: PRs #503, #514), #423, #444, #450, #534, PR #539, IronbellyOrg/Coder#477.
3. "Orchestrator management server" is still undefined. Candidates: Orca itself, the observer, a #423 catalogue store. Not decided.
````

If the owner prefers a body edit over a comment, the same three paragraphs fit as a "Related and terminology" section; the comment form is reversible without editing history.

# Round 1 advocate for variant 2 (#450 issue watcher)

Role: advocate for V2, read-only. Date: 2026-11-14 (session date; the reviewed artifacts are dated 2026-11-13). Checkout: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`, HEAD `873599d59`. Nothing was posted, edited or switched; this file is the only write.

Re-verified by me in this round (live source, not copied from a report): `issue.md:43,88`, `launch.py:33,84,95`, `claim.md:131`, `classify.py:302-315,748-767`, `cycle.py:1270-1335`, observer adapter templates on `origin/master` (`adapter.py:29-32`), `git diff origin/master HEAD` over the watcher code and design (empty), `gh` state of #450, Coder#477, PR #485, PR #539, the live #409 body (updatedAt 2026-11-13T16:57:51Z). Everything else is marked "relied on diff-analysis SC-n" or "not re-checked".

## 1. Position summary

V2 is the only report that tested what the built watcher actually starts, and it found a verified contradiction that V3 and V4 repeat wrongly: the watcher's fixed prompt `/sc:issue --claim <N>` runs at the claim's default `worktree` level, so it creates a worktree and launches a governed second agent, against the watcher design's "claim stops at next-steps.md" (X-001). V2 also shows that watcher-launched sessions have no Run, no recorded identity and a likely "person session" label, so neither the sweep nor (my extension) the built observer can see or label them. V2's real weakness is that it was written without knowing `superclaude observe` exists, so its W-10 wording is stale, and a few line cites have drifted; its findings W-01 to W-09 and W-11 to W-16 are untouched by V5.

## 2. Steelman of each opposing variant

### 2.1 V1 (#409 observer versus the sweep, written without knowing `observe` exists)
**Strongest version.** The sweep's JSON v1 is a stdout-only, per-Run, nine-row-key contract (`report.py:642-661`; SC-1). Any consumer (an observer, v2, a #477 status route) needs a stored, identity-bearing, versioned carrier, and today there is none: the JSON is printed after the commit point (`commands.py:277-278`) and only Markdown is stored. On top of that, PR #539 carries two unresolved review threads, one of them a real security item (`_worktree_paths` accepts every path from `worktree ps` and `git status` runs with `{**os.environ}`, `probes.py:1203-1214,309`), and #409 contains two wrong claims (review-thread count; "the ten dimensions are not JSON keys" while `policy` is one). V1 also gives the most careful claim check of any report (39 rows) and a concrete, minimal fix list (W-1..W-7).

**What it gets right (confirmed).** X-004 (a status route cannot be "no write" if it runs `sweep run`), X-007 (confinement is for file reads only), C-07 and C-25 wrong claims, X-002 (the boundary sentence first appears inside decision 8). SC-1, SC-2, SC-9 confirmed these.

**Counter-evidence.** (1) Its central premise, "no observer code exists" (C-03, repeated in C-02 and C-21), is false: PRs #503 and #514 are merged and `observe` is registered (X-012, SC-13); the code was in V1's own checkout (A-016). F-01, F-03, F-04, F-12, F-14, F-15 and the recommendation to "persist the JSON so one collector serves both" are built on that premise (S-011). (2) V1 never checked #409 decision 9, so it has no finding on what the sweep does with a watcher-launched session (C-010 is "silent"). (3) Its verdict sentence "Both are read-only and share the same dimension names" contradicts its own C-02 and F-02 (X-008).

### 2.2 V3 (Coder#477 workspace listener)
**Strongest version.** Coder#477 presumes a listener that the built watcher deliberately does not have (design D1 option A: "No listener, inbound port or address registry", "Option A makes Coder#477 unnecessary", `issue-watcher.md:28,43,47-49`). V3 adds three things no other report has: external evidence from the Claude Code docs (a peer message arrives as plain text, a slash command in it does not run, bypass sessions hold inbound messages; F8), the Coder-side lifecycle facts (the `minimal` profile has no Orca; a stopped workspace polls nothing; F6) and the credential facts (the Orca pairing offer is a no-expiry bearer credential; F11). Five of its eight "wrong path" claims are verified (SC-4), and Edits 1 to 12 are directly pasteable.

**What it gets right.** F1 and F7 agree with my W-06: nothing addresses "the project's orchestrator" and the flow in #477 differs from the built one. F2 (wrong paths) is a clean, checkable fix.

**Counter-evidence.** (1) Edit 8 tells #477 that an accepted request "starts a new top-level session ... using `orca agent launch ... --prompt \"/sc:issue --claim <N>\"`" and offers the watcher's live test as the proof. It never mentions that the default claim level creates worktree `issue-<N>` and launches a second governed agent (`issue.md:43,88`; X-001). The edit would write an unexamined default into #477 as an acceptance criterion. (2) Edit 5 requires "the JSON object printed by `superclaude sweep run` ... produced without any write"; each run publishes a dated report (`commands.py:186`; X-004), so the criterion cannot be met as worded. (3) Edit 4's identity envelope assumes a row can be joined to a workspace, but for a watcher-launched session the watcher stores only `operation_id` (`launch.py:42-45`; V2 W-03), so there is no session key to attach. (4) Edit 5 and 6 now point at a built observer that has no network or credential path at all (C-011 V5 effect).

### 2.3 V4 (#423 v2 and the #339 boundary)
**Strongest version.** The word "v2" means two things (#423 knowledge layer versus #339 comments' trust layer plus orchestrator of orchestrators), so #423's gate "after v1 is complete" is ambiguous (F1). V4 correctly sees that v2's relay is the "cross-session permission laundering" path (F8), that one grant vocabulary and one audit record can be shared while one trust design cannot (F9, F9 versus X-005), that v2's LLM output must not leak into sweep classes (F14, the best unique contribution, U-008), and that ordinary sessions are "never messaged" (F7, WC-16 `:288`). Its paste-ready edits for three issues are the most complete of any report, and its F21 ("no v1 leakage into v2") is a useful negative check.

**What it gets right.** C7 and F11 agree with my W-06 that #423's and Coder#477's descriptions of the watcher flow differ from what was built; F9 is supported by V2's own W-08 (the watcher's trust is an approvers file plus labels plus an integer-only prompt, a local model different from any grant).

**Counter-evidence.** (1) C7/F11 repeat "starts one ordinary top-level agent session" and V4's proposed #423 edit 7 would publish exactly that sentence; the default claim also launches a second agent (X-001, SC-3), so the sentence is incomplete. (2) F7's proposed acceptance criterion requires v2 to state, per class (Orca worker, watcher-launched, person-started), how a checkpoint is obtained. The sweep cannot separate the second class from the third: `_person_origin` returns `(True, ..., NOTE_ORIGIN_NOT_PROVED)` when there is no tab-map entry and no join failure (`classify.py:762-767`) and `_rule_person_active` then labels it a person session (`:302-315`) (X-003, V2 W-05). The criterion cannot be met from sweep facts. (3) F17's "every path is confined" holds for file reads only (X-007, SC-9). (4) Proposals (a) and (b), "one data source", are weakened by V5: the built observer reads Orca, not the sweep (X-013). (5) F16 names WC-16, a hypothetical v2 timer and the PM 30-minute checkpoint; it omits two cadences that already exist or are planned: the watcher's own 5-minute cron (#450 item 3, `0 */5 * * * *`) and the observer's 15 s poll.

### 2.4 V5 (the already built observer versus the sweep)
**Strongest version.** V5 is the only report that read the built program rather than the issue text. It shows that `superclaude observe` (PRs #503 and #514) is merged and registered (`main.py:572-574`), starts only three Orca argv shapes (`adapter.py:29-32`, re-checked by me: `worker-list`, `skills list`, one `check` template), never mentions the sweep and is never mentioned by it (SC-15, SC-16), and writes its own snapshot JSON, which makes "two JSON v1" and "two readers of `worker-list`" real. It re-tests V1 row by row, gives 23 exact body corrections, puts each decision (D1 to D9) with a reversible, non-code first step, and labels what it could not verify. X-012, X-013, X-015 and SC-13 to SC-17 confirm its load-bearing claims. It is the best report for deciding what to build next.

**What it gets right.** The premise that invalidates V1 (X-012), the correct reading of "read-only" (no Orca write verb, local files written by both; O-11) and the decision D5 (the questions-read switch-on has no PR; the owner record names one Run while orchestrator mode creates a new Run per coordinator).

**Counter-evidence.** (1) V5 is silent about the watcher. The built observer cannot see a watcher-launched session at all: its only reads are `orchestration worker-list`, `skills list` and one `check --all --types question --run <id>` (`adapter.py:29-32`), and `agent launch` is not an orchestration verb (V2 W-04; `orca agent launch --help` re-run: "Start an agent in an existing workspace", no Run key). V5's claim that the observer "needs no bound Run" (A-008 V5 effect) is true only for orchestration Workers, so Run-less sessions stay invisible to both programs. (2) V5 D9 guesses that "TUI Panel" in Coder#477 means `observe`; the owner's one-line comment ("Ensure this aligns with Orchestrator and TUI Panel") does not say so (SC-5), and the only #477 flow the observer could join is one that does not exist. (3) "All four earlier reviews ... were wrong about one fact" (X-019) overgeneralises: V3 states no such premise and V2 W-01..W-09, W-11..W-16 do not depend on it. (4) X-020: "Drop W-3 from the #409 body" is a mislabel (W-3 is V1's proposed wording). (5) Several decisive facts live only in a sibling worktree or an unpushed commit (X-018, SC-18, A-015) and V5's own test run is not reproducible (SC-20), so part of its owner-decision timeline cannot be re-checked from master or GitHub.

## 3. Strengths claimed for V2

1. **W-01 is a verified contradiction, found by V2 alone.** `issue.md:43` sets the `--pipeline` default to `worktree`; `issue.md:88` says that level "create[s] or reuse[s] the Orca worktree `issue-<N>` and launch[es] one agent in it"; `launch.py:33` allows only `/sc:issue --claim <int>`, with no `--pipeline`. The design says the claim "stops at `next-steps.md`" (`issue-watcher.md:44`, SC-3). I re-read the first three just now. V3 Edit 8 and V4 C7/F11 omit the second agent (X-001).
2. **W-02 (ship gate) is verified and unique.** `claim.md:131`: "no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 ..., OB-H2 and OB-H3 have passed." The FU-1 live test is a claim on a test issue at the default level, and neither #450 nor the runbook mentions the gate. A claim also performs GitHub writes (assign, two comments, ClickUp step), so the live test is not a reversible step.
3. **W-03/W-04/W-09: a watcher session cannot be joined to anything.** The watcher keeps only `operation_id` (`launch.py:42-45`); `status_report` returns typed scalars and no session id (`cycle.py:1326-1335`, re-read). `orca agent launch` is not an orchestration verb (help text re-run on this host), so no Run or Dispatch row is expected. V2 labelled the unproven part (does Orca write any Run record) UNVERIFIED and routed it to FU-1.
4. **W-05 resolves X-003, which the diff analysis could not.** `_person_origin` (`classify.py:748-767`) returns `(True, notes + NOTE_ORIGIN_NOT_PROVED)` when the row has no tab-map entry, no left-over join and no failed join; `_rule_person_active` (`:302-315`) then classifies a readable, in-window row with `person_started True` as `person_active`. Nobody typed the command, so the label is wrong in kind. I verified the code path; the "today versus later" state split rests on `orchestrator-mode.md:65,992` (not re-read) and no sweep was run.
5. **W-06 (diagram versus design) still holds on the live body.** The live #409 body (updatedAt 2026-11-13T16:57:51Z, later than V1's check) still draws "issue watcher ... --starts a claim session--> project's orchestrator (coordinator)" at L75 and says "A session the watcher launches is an ordinary session to the sweep" at L121; the added banner did not touch either. Design option A (`issue-watcher.md:28,43,49`) has no orchestrator in the flow. V3 F17 and V4 F11 independently agree.
6. **W-07 (worktree ownership) is unique (U-004).** All watcher sessions start in one configured worktree and the runbook never says how it is created or who owns its agent, while the repository rule is "every worktree gets an agent; its creator owns it" (`core/CLAUDE.md:55-61`).
7. **W-10/W-11 (status contract) are unique and re-verified (U-005, U-006).** `status_report` keys are `healthy, last_completed_cycle_age_seconds, disabled_since, next_permitted_at, counts, day_cap_used, stale, retry`; no `schema_version`, host, login or `enabled`; `retry[].argv` is a runnable launch command; `healthy` is `age is not None and age <= HEALTH_AGE_S`, so a never-run watcher, or one whose last cycle is older than `HEALTH_AGE_S` (as after a kill switch or `enabled: false`), reads unhealthy although the stop is planned.
8. **W-12 is current.** #450's body has not changed since 2026-11-08T23:56:26Z and still lists item 4 and "2655 tests"; PR #485 merged 2026-11-10T06:10:27Z (re-queried).
9. **V2's code is stable on master.** `git diff origin/master HEAD` over `src/superclaude/cli/issue_watch` and `docs/designs/issue-watcher.md` is empty, so V2's watcher cites do not depend on PR #539 landing.
10. **Evidence method.** V2 alone ran live read-only host commands (`agent launch --help`, `worktree ps --help`, `orchestration --help`, `worktree ps --json`), and it marks the unproven parts (Run record, Claude command, name prompt) UNVERIFIED instead of assuming.
11. **Reversibility.** Every V2 proposal is issue or runbook text, plus one small change to `launch.PROMPT_PATTERN`/`build_claim_prompt` that the owner decides first (Q1). None changes the sweep or PR #539.
12. **Extension no other report reaches (mine, from V2 plus V5).** Because watcher sessions have no Run, the sweep and the built observer are both blind to them; #409 decision 9 ("Decide whether the observer also shows watcher state") has a concrete answer today: with the current adapter it cannot, and the watcher's own `status --json` or `dispatch.json` is the only observer-readable source, after FU-1.

## 4. Weaknesses identified in the other variants

1. **V1: a refuted premise carries six findings.** "No observer code exists" (C-03) is false (X-012, SC-13); F-01, F-03, F-04, F-12, F-14, F-15 and C-02, C-21, C-26 depend on it (S-011). Its headline recommendation (persist the sweep JSON so "one collector serves both") answers a question the repository had already answered differently.
2. **V1: internal inconsistency.** The verdict "Both are read-only and share the same dimension names" reverses its own C-02 and F-02 (X-008); the claim tally does not add up (X-009).
3. **V1, V3, V4 and V5 are silent on what the tools show for watcher-launched sessions.** C-010 is "silent" for V1, V3 and V4 as findings; V5 never mentions the watcher. Nobody else asks what the sweep or the observer shows for a session no Run owns.
4. **V3: Edit 8 omits the second governed agent** (X-001; `issue.md:43,88`; `launch.py:33`). Adopting it would put an unexamined default into #477 as an acceptance criterion.
5. **V3: Edit 5 is unachievable as worded** ("no write" while running `sweep run`; X-004; `commands.py:186,277-278`, SC-9).
6. **V3: scratch-file drift.** V3 calls `/tmp/pr339/i409-new-body.md` "the draft" although it was the live body (S-009); the live body has since moved (banner; now 30,758 bytes), so its `:70-81,113,114,118,195` cites are off.
7. **V4: C7/F11 and proposed edit 7 repeat "one ordinary session"** (X-001), and F7's per-class acceptance criterion cannot be met for the watcher-launched class from sweep facts (X-003; `classify.py:748-767`, `:302-315`).
8. **V4: F17 is incomplete** (X-007; `probes.py:1203-1214,309`), and proposals (a) and (b) now rest on a single-source premise V5 refutes (X-013, X-017).
9. **V4: F16 counts too few cadences** (omits the watcher cron and the observer's 15 s poll; X-011, X-015).
10. **V5: scope and overreach.** Silent on the watcher; D9 is a guess about what "TUI Panel" means (SC-5); X-019 overgeneralises (V3 and V2 W-01..W-09 are not wrong about the observer); X-020 is a mislabel; evidence for the owner timeline is in a sibling worktree or unpushed commits (X-018, SC-18, A-015) and its test run is unreproducible (SC-20).
11. **All reports cite a `/tmp` scratch file or a moving live body** (S-009, A-010); only V1 and V5 verified the live text, and V1's check is now stale.

## 5. Concessions (what is wrong or weak in V2)

1. **V2 did not know the observer exists.** Its W-10 ("Do not build an observer reader before FU-1") assumes an unbuilt observer. Corrected wording: "do not add a watcher panel or reader to `superclaude observe` before FU-1" (U-005 V5 effect). W-05 and W-16 say "the observer" generically and should name the built one.
2. **Cites have drifted.** V2 cites `/tmp/pr339/i409-new-body.md:70-75,113,117,195`. On the live body (30,758 bytes, banner added) the diagram is at L75 and item 9 at L121, so the +4 shift applies; the text is unchanged (S-009, A-010).
3. **Two key facts are unproven.** That `agent launch` creates no Run or Dispatch record (W-04) rests on help text and a live listing, not on an Orca source read; V2's "absent by construction" is stated too strongly. Whether the name prompt stalls and whether a tab-map entry appears (W-09) is UNVERIFIED by design and left to FU-1.
4. **W-05's "today versus later" labels are partly inferred.** I verified the code path (`classify.py:748-767`, `:302-315`) but not the `session_join` state (`orchestrator-mode.md:65,992`), and nobody ran a sweep against a real watcher session (X-003 was UNVERIFIED in the diff analysis; I could only close the code-structure half).
5. **Live host numbers are not reproducible** (29 worktrees, 43 `claude` agent rows; SC-12) and the host Orca version was not checked.
6. **Thin on other systems.** V2 has nothing on trust, scale, the JSON schema, v2 or Coder lifecycle, so it cannot adjudicate X-005, X-006, X-014, X-017 or most A-rows on its own evidence; my verdicts there are lower confidence.
7. **The W-01 fix is a code change proposed before the owner decides.** `--pipeline none` touches `PROMPT_PATTERN`, `build_claim_prompt`, the 12-element argv pin and the NFR-001 property test; the owner may legitimately want the chain (claim, worktree, governed agent), in which case W-02's OB-H gate becomes a precondition instead. W-01 is a contradiction with the design's D2, not proof of the owner's intent.
8. **Not read:** PR diffs of #447/#448/#485, hook scripts, `tests/sweep/`, #534, #423, the #409 design branch; W-08's "only claim-script-launched sessions are governed" comes from greps of `sc-issue-launch-level-hook.md:23`.

## 6. Shared assumptions A-001 to A-016

- **A-001: QUALIFY.** The sweep JSON is a fit for per-Run classification facts only; the built observer does not read it (SC-15), a #477 status route cannot run it without a write (X-004), and it cannot carry a Run-less watcher session at all (W-04).
- **A-002: QUALIFY.** One Run per coordinator is the sweep's unit, but a fleet is not "a merge of per-Run reports" because watcher-launched and person-started sessions belong to no Run, so no merge of Run reports can contain them (W-04).
- **A-003: REJECT.** The owner staged a direction on 2026-11-08 and said "Proceed with building the first release" on 2026-11-11; PRs #503 and #514 are merged and `observe` is registered (SC-13, SC-18), so "no code, direction unchosen" is false.
- **A-004: QUALIFY.** PR #539 is still OPEN at head `873599d59` (re-queried) with two unresolved threads (SC-2). All V2 items are independent of #539: W-05 needs no Phase 1 code change, W-01 changes `issue_watch`, not `sweep`.
- **A-005: QUALIFY.** #534 exists and Phase 2 is a reading list only; V2's own "waits for Phase 2 (or #534)" (W-05) is acceptable only if turned into a concrete #534 row that needs the FU-1 capture first.
- **A-006: REJECT.** `git status` runs with the inherited environment in every `worktree ps` path (`probes.py:1203-1214,309`) and each run writes a report (`commands.py:186`; SC-9). V2 assumed the sweep safe and did not test it; that is a gap in V2, not a point for the assumption.
- **A-007: ACCEPT.** For FU-1 and the shadow run the unit is one person's workspace, one `gh` login and one OS user (`issue-watcher.md:15`); multi-owner trust is a later problem V3 raises.
- **A-008: QUALIFY.** True for the sweep, which needs a bound Run and an active coordinator (WC-16); false for the sessions the watcher starts (no Run, no coordinator; W-04, W-06). The observer's worker ledger needs no bound Run, but still sees only orchestration Workers.
- **A-009: QUALIFY.** The watcher's Orca reply shapes are literally assumed: #450 item 1 requires "every `_assumed_shape` fixture is replaced with real output" and `tests/issue_watch/fixtures/_assumed_shape/orca_launch_*.json` exist; the host Orca version is unchecked (V2 scope).
- **A-010: REJECT.** The live #409 body changed after V1's check (updatedAt 2026-11-13T16:57:51Z; diagram now L75, item 9 L121); the watcher code and design did not (empty diff `origin/master..HEAD`).
- **A-011: REJECT.** The edit sets overlap (S-006, X-002). V2's five edits touch #450, the runbook and `launch.py` and are independent of the #409 rewrites, except W-05(a), which rewrites #409 item 9 (L121) and should be applied in the same pass as V5's BC list.
- **A-012: QUALIFY.** The evidence supports keeping both programs (different facts owned, different allow-list rules; V5 FO table), but only V5 states it and it is the owner's question (V5 Q2); treat it as a working default whose first steps are reversible under either answer.
- **A-013: QUALIFY.** For orchestration Workers the CLI read verbs are the source; for a watcher session they show nothing (observer adapter has three templates only, none of them `worktree ps`), so only `worktree ps` agent rows (V2 W-04, W-05 b) and transcripts carry it. An Orca event feed is unexamined by everyone.
- **A-014: REJECT.** There are at least three machine-readable contracts: the sweep JSON v1, the observer snapshot v1 (O-08) and the watcher's `status --json` (no `schema_version`; `cycle.py:1326-1335`) plus `dispatch.json` v1 (W-10).
- **A-015: REJECT.** V5 shows the observer decisions sit in a sibling worktree (SC-18). For the watcher, option A is in a tracked design (`issue-watcher.md:43`), but the 2026-11-13 Coder#477 comment ("Ensure this aligns with Orchestrator and TUI Panel") does not say whether it reverses option A, so the current owner position is not recorded anywhere (SC-5).
- **A-016: REJECT.** V5 (X-012) shows the observer was in V1's own checkout; I would add that V2 was equally exposed (it also did not find the observer), so every "silent" in V1 to V4 may mean "not found".

## 7. Point table (every X-NNN and every A-NNN)

Confidence is 50-100% in my verdict. "Re-checked" means I opened the source in this round; "relied on SC-n" means I used the diff analysis' spot check and did not re-open it.

| id | verdict on the underlying claim | winner | conf. | evidence | recommended course of action |
|---|---|---|---|---|---|
| X-001 | V2 is right: the fixed prompt runs the claim at default `worktree` and launches a governed second agent; V3 Edit 8 and V4 C7/F11 are incomplete | V2 | 95% | Re-checked `issue.md:43,88`, `launch.py:33`; SC-3 | Owner answers V2 Q1 (`--pipeline none` or keep default plus OB-H gate); do not copy V3 Edit 8 or V4 edit 7 into #477/#423 until then |
| X-002 | V1 is right that the boundary sentence is first made inside decision 8; V4's evidence is circular, but "distinct from v2" holds via L209 and #423 | V1 | 75% | Relied on SC-7 (not re-opened) | Rewrite decision 8 once, in one pass, merging V1 W-7, V4 edit 2 and V5 BC-17 |
| X-003 | V2 is right in mechanism; V4's per-class AC for "watcher-launched" cannot be met from sweep facts | V2 | 80% | Re-checked `classify.py:748-767`, `:302-315` (code path only; no sweep run) | Say in #409 item 9 that the sweep cannot tell a watcher session from a person's; log labelling as a #534 row needing the FU-1 capture |
| X-004 | V1 is right: `sweep run` writes a dated report and prints JSON after publishing, so "no write" is unachievable | V1 | 90% | Relied on SC-9 (`commands.py:186,277-278`) | Drop "without any write" from any #477 text, or add a persisted-JSON or no-write mode as a separate decision |
| X-005 | Not decidable from sources; V4 is slightly better supported because the watcher's trust is a local approvers-file model unlike any grant | V4 (weak) | 60% | V2 W-08, `launch.py:33`; V3 F12 itself notes the local model | Owner decides; record "one grant vocabulary and one audit record, separate enforcement" in #339 as a proposal only |
| X-006 | Both name the same two options; the venue is the only dispute, and V5 shows it now concerns two JSON contracts | neither | 60% | O-08, SC-15; V5 D1 | Decide once in #339 after the D1 relationship note; do not edit PR #539 for it |
| X-007 | V1 is right; V4's confinement claim holds for file reads only | V1 | 85% | Relied on SC-9 (`probes.py:1203-1214,309,529`) | Fix or record the git-config item on PR #539 (V1 F-07); correct V4 F17 wording |
| X-008 | V1's own C-02 and F-02 are right and its verdict sentence is wrong; V5 also removes "observer shares the dimension names" | V5 | 90% | X-008, RT-F02 | Ignore the V1 verdict sentence |
| X-009 | Counting error with no effect on findings | neither | 95% | X-009 | None |
| X-010 | V1 and V2 are right (host-global `worktree ps`); V4 understates | V1, V2 | 85% | V2 section 4; `probes.py:1203-1214` | Correct V4 F3 wording |
| X-011 | Both premises weakened: three pollers already exist or are planned (observer 15 s, sweep at most every 5 min, watcher 5-min cron) | V5 | 70% | X-015, `collector.py` INTERVAL; #450 item 3 | List all cadences once in the D1 relationship note; no scheduler change |
| X-012 | V5 is right; V1 is wrong | V5 | 99% | SC-13; I re-checked the adapter in `origin/master` | Correct the #409 body (V5 BC-01..BC-07 and the rest) in one pass |
| X-013 | V5 is right: the observer reads Orca, not the sweep JSON | V5 | 95% | SC-15, SC-16; re-checked `adapter.py:29-32` | Remove "reads the sweep's JSON, not a second collector" from #409 (V5 BC-08, 13, 16) |
| X-014 | V5 is right for the Orca ledger; V1 stays right for per-Run git, contract and transcript depth | V5 (partly V1) | 75% | RT-F04; code limits confirmed, 428-worker sample not re-checked | Drop V1 W-3; keep "per-Run depth is the sweep's" |
| X-015 | V5 is right: the observer polls on its own thread regardless of the sweep | V5 | 85% | SC-17 | Same as X-011 |
| X-016 | Real contradiction in what two programs print; the sweep's "cannot be read without consuming" is stronger than its evidence. Observer-side evidence is owner-only and unreproducible | V5 (qualified) | 60% | `report.py:199,534`; `adapter.py` `QUESTION_TEMPLATE` | Soften the sweep's two lines through a #534 follow-up, not by editing #539; keep `check` out of the sweep |
| X-017 | Opposing recommendations; V1 wrote without knowing the observer; the watcher case fits neither collector | V5 | 70% | O-01, D1; W-04 (Run-less sessions are outside both) | Write one relationship note (D1 option a) first; keep the optional observer panel for later |
| X-018 | V5 is right that AC-S is "not met as recorded"; the owner files are mostly in a sibling worktree | V5 | 70% | SC-18; A-015 | Owner writes the dated direction record or amends #409 AC 1 |
| X-019 | V5 is right about V1 (explicit) and implicitly about V2 W-10 and V4 F13; V3 states no such premise | V5 (qualified) | 80% | X-019; V2 W-10 text | Reword V2 W-10 as "no watcher panel in `observe` before FU-1" |
| X-020 | Mislabel; V1's W-3 is not in the #409 body | neither | 95% | SC-19 | Read as "do not add V1's W-3" |
| A-001 | QUALIFY: fits per-Run classification only | V5 | 80% | Section 6 | Use the JSON as one candidate carrier, not the single integration point |
| A-002 | QUALIFY: Run-less sessions are in no Run report | V2 | 75% | W-04 | State the unit explicitly and mark Run-less sessions as out of both programs |
| A-003 | REJECT: observer is built and direction staged | V5 | 95% | SC-13, SC-18 | Fix the #409 body |
| A-004 | QUALIFY: #539 open, two threads | V1 | 80% | SC-2; PR re-queried | Keep V2 items independent of #539 |
| A-005 | QUALIFY: needs a concrete #534 row | V2 | 65% | #534, PHASE2 reading list | File the machine-started-session label as a #534 row after FU-1 |
| A-006 | REJECT: not read-only in effect | V1 | 90% | SC-9 | Resolve the git-config thread before merge or record it as accepted |
| A-007 | ACCEPT for FU-1 scope | V3 (weak) | 65% | `issue-watcher.md:15` | None now; revisit for multi-owner use |
| A-008 | QUALIFY: false for watcher sessions | V2 | 80% | W-04, W-06 | Name Run-less sessions as a separate blind spot |
| A-009 | QUALIFY: Orca shapes are assumed in the watcher tests | V2 | 85% | #450 item 1; four `_assumed_shape` fixtures | FU-1 replaces them; record the Orca version in the live-test record |
| A-010 | REJECT: live #409 moved; watcher code did not | V5 | 90% | updatedAt 16:57:51Z; empty diff | Re-fetch before applying any line-based edit |
| A-011 | REJECT: edits overlap | V5 | 90% | S-006, X-002 | Apply the #409 edits as one merged pass |
| A-012 | QUALIFY: working default pending owner answer | V5 | 65% | V5 FO table | Ask V5 Q2 once, together with Q1/Q2 below |
| A-013 | QUALIFY: CLI read verbs miss Run-less sessions | V2 | 70% | `adapter.py:29-32`; W-04 | Capture `worktree ps` agent rows in FU-1; evaluate an event feed separately |
| A-014 | REJECT: at least three JSON contracts | V5 | 90% | O-08; `cycle.py:1326-1335`; W-10 | Name each contract in every doc |
| A-015 | REJECT: owner positions are not all recorded | V5 | 80% | SC-18; SC-5 | Ask the owner to state option A or B/C on Coder#477 |
| A-016 | REJECT: "silent" may mean "not found" | V5 | 85% | X-012; V2 also missed the observer | Re-verify every V1 to V4 "silent" before acting on it |

## 8. Course of action for the owner

Order that matters: step 0 (owner answers) gates everything marked "needs 0"; the watcher live test (FU-1) is the one step that is NOT reversible (real GitHub and ClickUp writes), so it comes last. R = reversible first step (issue text, runbook text, a code change that a revert undoes); NR = not reversible.

**Step 0. Owner decisions (one message, answers only; R).**
- Q1 (V2): claim level the watcher passes: `--pipeline none` (claim ends after the comments; recommended) or the default `worktree` (claim plus worktree `issue-<N>` plus a governed second agent, which needs OB-H1 item 1, OB-H2, OB-H3 first). Needs: nothing.
- Q2 (V2/V3/V4 Q9): which flow Coder#477 targets (the built watcher, option A, or a handoff to a project's orchestrator) and whether the 2026-11-13 comment reverses option A. Needs: nothing.
- V5 Q2: keep `observe` and the sweep separate with one written contract, or merge. Needs: nothing.

**#450 (watcher rollout) - V2's own items.**
1. Add to #450 "Done when 0": the Q1 decision. If `--pipeline none`: change `launch.PROMPT_PATTERN`, `build_claim_prompt`, the 12-element argv pin and the NFR-001 property test, in a small PR through `/sc:pr-submit --monitor 3`. Needs 0. R (code revert).
2. If Q1 keeps the default: add the OB-H1/H2/H3 precondition to #450 and to runbook 14.1 (`issue-watcher-setup.md:584-589`). Needs 0. R (text).
3. Strike item 4 (done by PR #485) and fix or drop "2655 tests". Needs nothing. R (text).
4. Extend FU-1: record the session identity fields (pane key, terminal handle, session id) from the real reply and from `worktree ps --json`; before/after `orchestration run-list`; the Orca Claude command (`ccsession-orca`?), whether the session stalls at the name prompt, tab-map entry, permission mode; keep unsanitised values in a private note and commit only the sanitised fixture. Share the capture with #534 step 1.0a. Needs nothing (text); the capture itself needs the live test. R (text).
5. Add runbook step 1.3a: create the watcher worktree with `orca worktree create --name issue-watch --agent claude --prompt "<task>"`, name its owner, note that each session writes `.dev/issues/<N>/` there (W-07). Needs nothing. R (text).
6. Run FU-1 live (real `gh`, real Orca) only after items 1/2, 4 and 5 and the OB-H gate if the default is kept. Needs 1-5. NR.
7. Do not add a watcher panel or reader to `observe` before FU-1 is recorded; when wanted, add `schema_version`, `enabled`, host and login to `status --json` (additive) or declare `dispatch.json` v1 the read contract; show `retry[].argv` as text only; show planned stops from `disabled_since` and `enabled`, not from `healthy` (W-10, W-11). Needs 6. R.

**#409 (TUI observer issue body).**
8. Apply one merged edit pass: V5's 23 corrections (BC-01..BC-23), plus the diagram fix (watcher -> an ordinary top-level session, no coordinator) and a rewrite of decision 9 ("a session the watcher launches has no Run and no coordinator; neither the sweep nor `observe` can tell it from a person's session or sees it; label it in a later phase"). Re-fetch the live body first (A-010). Needs 0 (Q2, V5 Q2). R (issue-body history).
9. Resolve the decision-8 rewrite collision (V1 W-7, V4 edit 2, V5 BC-17) in the same pass. Needs 8. R.

**`superclaude observe`.**
10. No code. Keep the three-template allow-list. Optionally add one routing row (V5 D8) in its own small PR. Needs nothing. R.
11. Merge or drop the unpushed questions-read switch-on per V5 D5 (owner's decision, not part of the watcher work). Needs the owner's sentence on Run scope. R (revert).

**Sweep and #339 (PR #539 and #534).**
12. Do not hold PR #539 for the watcher items. Resolve or record the two open threads (V1 F-07, SC-2) on their own. Needs nothing. R.
13. Log in #534: label machine-started top-level sessions as not person-started (W-05), the `worktree ps` agent-row fields (`prompt`, `paneKey`) as a candidate source, and V5's wording fixes for `report.py:199,534` and design 7.5/17 item 5. Needs 6 for the capture. R (text).
14. In #339, add the terminology line and the contract-owner decision (V4 #339 edits 2 and 4) after V5 Q2. R (text).

**Coder#477.**
15. Post the status comment (V3 Edit 1) and fix the five wrong paths (V3 Edit 2) after Q2. Do NOT post V3 Edit 8 as written; replace the launch sentence with "the launch uses the claim level chosen in IronClaude#450 (Q1); at the default level the claim also creates worktree `issue-<N>` and launches a second governed agent". Needs 0. R (comment edits).
16. Drop V3 Edit 5's "produced without any write" until a persisted-JSON or no-write mode exists (X-004). R.

**#423 (v2).**
17. Apply V4's #423 edits (F1 rename, gate, data-source paragraph), but write the #331 line as "starts an ordinary top-level `/sc:issue --claim <N>` session; at the default claim level it also launches a governed second agent". Needs 0 (Q1 for the exact sentence). R (issue text).
18. Replace V4's per-class AC wording so it does not require the sweep to distinguish watcher-launched from person-started sessions. Needs 13. R.

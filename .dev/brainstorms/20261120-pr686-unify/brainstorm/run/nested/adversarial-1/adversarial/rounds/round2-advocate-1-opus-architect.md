# Round 2 (rebuttal), Advocate for Variant 1 (opus, architect persona)

## 1. Response to each criticism raised against V1

Criticisms are taken from `round1-advocate-2-sonnet-analyzer.md` section 5 (V1 items 1 to 6) and `round1-advocate-3-haiku-backend.md` section 5 (items 1, 4, 5).

1. **"Unbound and flagged" breaks the owner's G2 sentence (V2 adv item 1, V3 adv item 1; C-003, X-002).** Full concession, already made in my Round 1 section 6 item 1. The owner's sentence is at master `docs/designs/issue-pipeline-guard-g2.md:9` (V3 adv section 4 item 4) and D05 keeps it as a must-keep (D05 VERDICT line 47). V1 S11's `BOUND_WORKERS_PROVEN` must read: false means no real issue starts a worker at all; only a throwaway issue may, until the probe passes and a reviewed commit flips it. V3's rule wins.

2. **Schema 2 and "readers ignore unknown keys" are contradicted by the loader (V2 adv item 2; C-014, C-015).** Concession on the rollback text, partial counter on the version number. Section 3 (a) now confirms the rule in planb too (`cycle.py:223-233`), so V2 adv's "verified for master only" caveat is closed. Counter: V2's own plan (additive keys at version 1) has the same problem, because every new key is refused by the same `_TOP_KEYS` check; V2 S12 says so ("the loader may reject unknown keys"). The bump was never the cause; adding keys is. I now drop the version bump (smaller diff) and adopt V3 adv's version-pair rollback test. V1 S10's "readers ignore unknown keys" referred to the sweep JSON, not the config; that sentence was badly placed next to a config change and should name its scope.

3. **The sweep reads the watcher (V2 adv item 3, V3 adv item 5; C-005, X-006).** Concession. Both advocates agree it is not a GitHub call (V3 adv: "the objection is added responsibility, not a false allegation"), and master `cli.py:164-182` confirms `status` reads only the local store and audit log. But D11's settled line is "the sweep stays the one source of session facts" (D11 VERDICT line 9); watcher holds are not session facts. The observer reading `issue-watch status --json` directly is the smaller and cleaner change. V1's `watcher` block becomes a later option only if the screen needs one file.

4. **The K1 end state depends on RK-7, and the shared-worktree defect is present until S14 anyway (V2 adv item 4, V3 adv item 4).** Concession on building it now; counter on the defect. Section 3 (b) shows the defect is real in planb (`generate.py:252`, `launch.py:136-157`, `cycle.py:1179`) and that the built claim hand-off depends on the shared checkout (`claim.md:96`). Neither V2's "start the coordinator only after the claim file" (a standing session is never "started after") nor V3's "stay read-only while the claim runs" (a rule no code enforces) removes it; V3 adv concedes the second ("Its claim-session workaround is not isolation", section 6). So V1's diagnosis stands. What I give up is the `start_mode` key and the second code path in the first build: by the ponytail rule, code "for later" is not written. V1's K1 becomes the named reversal if the live check in section 5 finds two live agents in one worktree.

5. **Bundled PRs: S9 and S11 too large, MC list shorter (V2 adv item 5).** Concession on S9 and S11, with a correction from section 3 (d) and (e). S9 carried store union, `start_mode` and config v2 that D15 line 219 does not list for PR 686; those come out. S11 put wake verbs and worker start in the substrate, against D15 line 18, row D12 and line 226; it splits into O4 substrate, O5 merge unit plus worker route, O6 wake and the rest. V2's MC-8 to MC-10 are additions I accept.

6. **S10 delays lane 3 (V2 adv item 6; C-006).** Concession. The two sweep fields and the saved JSON depend on nothing in lanes 1 or 2 (D11 VERDICT lines 18 and 20). Only the observer's watcher read waits for the extended `status --json`.

What I do NOT concede: machine state outside git (C-002), the `coordinator_autostart` switch and `coordinator_absent` reason (U-003), the named `waiting_reapproval` state (U-004), the plan-check direction (C-004, X-004), go entries out of git (C-009, X-005), and the owner-action layout (S-002). Both other advocates endorse each of these in their Round 1 tables, except that V2 adv holds C-014 at V2 (no `coordinator_autostart`) while conceding U-003 in its section 6 item 5.

## 2. Updated assessment of V2 and V3

**V2, after its defense.** Steelman first: the V2 advocate made the largest set of honest concessions (X-003, C-002, X-005, C-010, U-003, U-004, D16 scope, missing rows), and its core claim holds: keep the tested claim path, one PR per stage, each with named mechanical checks MC-1 to MC-10. I now agree with V2 on C-001 (poll claims), C-005, C-006, C-013, C-015 and the schema number. Two of its defenses do not hold after Round 2 evidence:
- The three-PR cut of PR 686 (C-007) goes against D15 line 219 ("not split") and line 220 (skip reasons and the start-time re-check land on planb at O2). The settled shape is: skip reasons and re-check in planb; one adapted PR 686 limited to D15's list; the `owner/name` rekey and new keys at O6 (row C4). V2's per-PR checks still apply to each of those.
- The "skill without merge path first" bridge (C-008, V2 S15) is a stated deviation from D15 O4 then O5 then O6 (line 18, row D12, line 226). Settled verdicts win; the narrow first live run V2 wants is still available, because nothing goes live before O7.
- V2's X-001 hybrid ("cap 1 plus wake only after the claim ended") still lacks a definition of "claim ended" that the code can see: the shape of PR 693's result file is UNVERIFIED (V2 R9), and section 3 (b) shows the claim terminal's lifetime is unknown.

**V3, after its defense.** Steelman first: V3's operating contract (separate an uncertain launch from delivery; state before ack; consumed consent never restored; nothing real before proof) is the best safety design of the three, and its advocate honestly dropped the plan-check reversal, the compressed owner actions, and the read-only workaround as "not isolation". V3's build order (S6 substrate, S7 merge unit, S8 the rest) is the closest to D15. Remaining weaknesses:
- Section 3 (c) shows part of V3's recovery list is already built (an `unknown` launch is never relaunched by the poll, master `record.py:447-448`), so the new work is narrower than V3 section 8 suggests: the wake outbox replay after `claimed`, the ack-state match, and the restart budget. That is good news for a small team, not a fault, but the plan should say which rows are new.
- V3 S8 still puts F binding at O6, while D15 row D12 puts the worker route at O5.
- V3 advocate rejects A-004's "one checkout" reading (worker worktrees exist). Fair; I adopt that correction.
- V3 still keeps runtime state inside the `Coordinator` worktree; its own advocate concedes V1's outside-git root "better survives worktree cleanup" (round 1 V3 adv section 6).

## 3. New evidence not given in Round 1

All lines below were read for this round in the snapshots or the planb worktree (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`, abbreviated "planb"). Nothing was run.

**(a) Do the config loaders reject unknown keys and schema versions other than 1? Yes, both.**
- Master: `cycle.py:216-220` raises `config_invalid` with "unknown configuration key"; `cycle.py:222-226` raises "schema_version must be the integer 1".
- Planb: the same rule. `cycle.py:54` sets `SCHEMA_VERSION = 1`; `cycle.py:59-72` lists the only allowed keys (`schema_version`, `enabled`, `labels`, `project_id`, `owner_account_id`, `worktree`, `approvers_file`, `state_dir`, `approval_excluded_ids`, `repo`); `cycle.py:223-226` rejects anything else; `cycle.py:231-233` rejects any version but 1. `generate.py:247` writes `schema_version` from that constant.
- Planb has a migration chain for the STORE (`record.py:254-268`: a store document below the current version is raised step by step; one above it is refused), but none for the CONFIG.
- Consequence: every variant that adds a key (all three do: Clay's `merge` block, `grants`, `max_in_flight` and so on) must widen `_TOP_KEYS`, and an older binary refuses the new file whether or not the version number changes. A version bump only changes the error text from "unknown configuration key" to "schema_version must be the integer 1". Both fail closed; neither lets a rollback "just work". So the real requirement is V3 advocate's version-pair rollback test, and the version number itself is a minor choice. I now prefer staying at 1 (smaller diff, no second accepted version to maintain).

**(b) Does the poll-launched claim run in the same worktree path as the standing coordinator, and what does planb `_precheck` do about extra files? Same path; `_precheck` ignores extra files.**
- Planb `generate.py:252` writes `"worktree": str(base.worktrees_dir / name / "Coordinator")` into every generated per-repo config, and `cli.py:459` documents the folder as "Holds <repo>/Coordinator for each repo".
- Planb `launch.py:136-157` builds `orca agent launch --agent <agent> --worktree path:<worktree> --surface terminal --prompt <claim> --json`, and `launch.py:405-416` runs it with `cwd=str(worktree)`; `cycle.py:1179` records `launch_cwd=str(cfg.worktree)`. Master is the same at `cycle.py:1086`.
- So the claim agent is launched into `<worktrees>/<repo>/Coordinator`, the same worktree D07 and D08 give the standing `COORD-<RepoName>` session. D07 item 8's defect is confirmed in the owner's own branch, not only in master.
- The built claim text already assumes that sharing: master `sc-issue-protocol/refs/claim.md:96` says for `--pipeline none` "the claim leaves its files in the checkout that ran it", and the coordinator then copies `.dev/issues/<N>/` into the worker's new worktree. So the hand-off by files depends on the shared checkout.
- Planb `dispatch.py:269-304` (`_precheck`) checks only: the worktree is a directory (`:279-280`), has a `.git` entry (`:281-282`), has the right origin (`:283-284`), then the trigger label, the `Approved` field and the Project (`:285-303`). It never inspects the worktree's files, ignored or not. V2's own K5 worry ("`_precheck` rejecting a worktree with ignored files") does not hold for planb or master (master `cycle.py:375` checks only that the directory exists).
- What the code does NOT say: whether the claim's Orca terminal stays alive as an idle agent after Wave 6 ends a `--pipeline none` claim (`claim.md:94`, "the claim ends here, with no Wave 7 and no Wave 8"). If it stays alive, two live agents share the worktree until someone closes it. UNVERIFIED; it needs the live check in section 5.

**(c) Is `/sc:issue --claim` idempotent when the marker already exists? Yes for GitHub comments and assignment, no for model work and concurrent runs.**
- Master `refs/claim.md:30`: Wave 1 finds "an earlier claim by this user", a comment by the current login containing `<!-- sc:issue:claim -->`.
- `refs/claim.md:43`: "Already assigned to the current login -> continue (re-claim is allowed and idempotent)."
- `refs/claim.md:44` and `:88-92`: earlier claim and accuracy-check comments are EDITED with `gh api -X PATCH`, not posted again; `:93`: "a re-run edits rather than duplicates because of the markers."
- Limits: a re-run repeats Wave 4 (a new accuracy check, a model session, possibly a different verdict), only recognises a marker written by the same login, and nothing stops two claim runs at the same time from racing on the same comment.
- The poll never relaunches an uncertain launch by itself: master `record.py:447` lets `launched`, `unknown` and `abandoned` move to `claimed` when the marker appears, and `record.py:448` makes `unknown` leave otherwise only by a person's `reset N` (T-13, `record.py:707`). So V3's "an unknown receipt is never relaunched" is already built at the store level; what is new in V3 is the outbox replay of the wake after `claimed`.

**(d) D15 says PR 686 is adapted in place and "not split".** D15 VERDICT line 219: "Adapt PR 686 in place as a draft (not merge as is, not split, not close)", listing its contents (kept names, `plan_check` placeholder rule via `plan_body.py check`, reasons-table rewrite, `hold:backlog` read, read-only label variant, M1 and M2, shared terminal helper, D14 checks). Line 220 puts "skip reasons and the start-time re-check ... and the claim-marker test" on planb at O2, before PR 686. Row C4 (line 76) puts the `owner/name` rekey at O6. This settled text cuts against V2's three-PR split (S11, S12, S13) and also against V1's overloaded S9 (store union, `start_mode`, config v2 are not on D15's list).

**(e) D15's build order puts the worker route in O5 and wake handling in O6.** D15 line 18 defines O4 (substrate: runner, `refuse(argv)`, JSON contract, state lock, one state-folder path map), O5 (merge path as one unit), O6 (other verbs and transport). Row D12 (line 96) puts the supervised `worker-start` route at "O5, O7"; line 226 puts `wake-check`, `wake-ack`, cap, restart, audit, hand-back at O6. V1 S11 (wake verbs and worker start in the substrate stage) and V2 S15 (skill with wake verbs and worker start before the merge unit) both deviate; V3's S6 to S8 order is closest, though V3 puts F binding in O6 rather than O5.

**(f) Evidence against my own C-002 position.** D15 line 224 describes the O4 substrate's "one state-folder path map (git-ignored)". "Git-ignored" suggests the drafters pictured a folder inside a checkout. My reading: the requirement is that machine state is never committed, and a folder outside every checkout meets it with no per-project ignore rule; but the verdict's wording does lean toward V2 and V3, so I lower my confidence on C-002.

## 4. FINAL POSITIONS TABLE

"Agree" columns compare my final position with each advocate's latest (Round 1) table: yes means the same pick or a compatible hybrid; no means a real difference, named in the hybrid text.

| id | superior approach | confidence | agree V2 adv | agree V3 adv |
|---|---|---|---|---|
| S-001 | HYBRID: one PR per stage in D15 order O0 to O7, with V2's separate revert dry run and early lane 3; PR 686 stays ONE adapted PR (D15 line 219), skip reasons and re-check land in planb (line 220) | 72% | no (V2 splits 686 into three) | no (V3 adv keeps V2's three watcher changes) |
| S-002 | V1 | 85% | yes | yes |
| S-003 | HYBRID: V1's diagram with V2's [B] [P] [C] [N] [D] tags and V3's at-least-once paragraph | 75% | yes | yes |
| S-004 | HYBRID: V1's complete rows, V2's file:line cites, V3's validation rules, no host-specific paths | 75% | yes | yes |
| C-001 | HYBRID: poll claims as built (V2, V3) plus V3's wake outbox replay after `claimed`; no `start_mode` key or second claim path in the first build; V1 K1 kept as the named reversal | 80% | yes | yes |
| C-002 | V1: all machine state in the per-repo state folder outside git; human records in `.dev/coordinators/` | 65% | yes | yes |
| C-003 | V3: no real issue until the live F probe passes; throwaway issue only | 90% | yes | yes |
| C-004 | V1 (same as V2): `plan_body.py check` is the definition, package copy with parity test | 90% | yes | yes |
| C-005 | V2: observer reads `issue-watch status --json`; sweep untouched | 80% | yes | yes |
| C-006 | V2: sweep fields and saved JSON early, lane 3 | 85% | yes | yes |
| C-007 | HYBRID: one adapted PR 686 limited to D15 line 219's list; skip reasons and start-time re-check in planb (line 220); `owner/name` rekey and new keys as O6 PRs (row C4); V3's recovery tests on each | 70% | no | no |
| C-008 | HYBRID: D15 order: O4 substrate only; O5 merge unit plus the F-bound worker route (row D12); O6 wake verbs, cap, restart, audit, hand-back (line 226) | 75% | no (V2 ships a skill before the merge unit) | yes (moves F binding from V3's O6 to O5) |
| C-009 | HYBRID: consumable go entry outside git (V1 location) with V3's consumed-never-restored rule and an unchanging quoted copy in `records/` | 78% | no (location only; V2 adv picks V3's in-worktree runtime) | yes |
| C-010 | V3, noting the poll already never relaunches an `unknown` launch (master `record.py:447-448`); new work is wake replay, ack-state match, restart budget | 85% | yes | yes |
| C-011 | HYBRID: S0 ruleset recommendation (supported by D05, D14) with D16 items marked as proposals | 70% | yes | yes |
| C-012 | HYBRID: ask the owner with a suggested value labelled UNVERIFIED; merge automation stays off until answered | 65% | yes | yes |
| C-013 | V2: label created only by person-run `repo-init` on a chat go | 80% | yes | yes |
| C-014 | HYBRID: stay at schema 1 and widen `_TOP_KEYS`; V2's `coordinator_session` and `wake_enabled`; V1's `coordinator_autostart` (absent = false, encodes D06 item 6); no `start_mode`; version-pair rollback test | 72% | no (V2 table omits `coordinator_autostart`, though V2 adv section 6 item 5 concedes it) | yes |
| C-015 | V2: a rollback must also restore the old config files (master and planb loaders both refuse new keys) | 90% | yes | yes |
| X-001 | HYBRID: poll claim at cap 1 for the first build; a live check records whether the claim terminal is still a live agent when the coordinator acts; if it is, the owner picks V1 K1 (coordinator claims) or a separate claim worktree before any real issue | 70% | no (V2 adv relies on "wake after claim ended", undefined today) | yes |
| X-002 | V3 | 92% | yes | yes |
| X-003 | V3 (V2's S15 reading replaces its K14) | 90% | yes | yes |
| X-004 | V1 (same as V2) | 90% | yes | yes |
| X-005 | HYBRID: go entries never tracked; quoted owner words kept unchanging in `records/` | 80% | yes | yes |
| X-006 | V2: the sweep does not read the watcher | 80% | yes | yes |
| A-001 | HYBRID (QUALIFY): V1's per-issue state fields plus V3's startup reconcile, gated by a kill-after-`worker_done` resume test | 75% | yes | yes |
| A-002 | HYBRID (QUALIFY): live probe records the worker's worktree path, must differ from `Coordinator`, before real work and before cap above 1 | 80% | yes | yes (V3 adv says REJECT; same remedy) |
| A-003 | HYBRID (QUALIFY): interim ledger of owner answers (Q01 fields) in the migration's task package under `.dev/tasks/`, which the repo rule always stages; imported by the first coordinator PR; owner never writes it | 70% | yes (V2 adv's proposal) | yes |
| A-004 | ACCEPT with V3 adv's correction: one polling host, one coordinator per validated `owner/name`; several checkouts per repo are expected (worker worktrees) | 80% | yes | yes |
| A-005 | QUALIFY: only a person-opened coordinator runs `/sc:pr-submit` until U3 is proven and WC:70 and WC:245 are approved in chat | 85% | yes | yes |

Tally: agree with V2 adv on 24 of 30, with V3 adv on 28 of 30.

## 5. Points that remain genuinely unresolved

1. **X-001 and C-001: does the claim agent stay alive in the `Coordinator` worktree?** The code proves the shared path (section 3 b) but not the lifetime of the claim's Orca terminal after a `--pipeline none` claim ends (`claim.md:94`). Only a live check can say: run one throwaway claim, then list the agents in that worktree. If one is still there, the fix is a choice (coordinator claims, V1 K1; or a separate claim worktree, which conflicts with Coder 516's single worktree), and the owner should pick it in chat.
2. **C-007 and S-001: one adapted PR 686 or three?** D15 line 219 says "not split". If the adapted PR is still too large to review once planb carries the skip reasons, splitting it reopens a settled verdict, so that is the owner's call, not the plan's.
3. **C-008: a skill without the merge path before the merge unit?** V2's bridge gives a narrower first run; D15's order (line 18, row D12, line 226) says O4, then O5 with the worker route, then O6. Settled order wins unless the owner rules otherwise.
4. **C-002: inside or outside the checkout.** D15 line 224 says "state-folder path map (git-ignored)", which reads like an in-checkout folder; V1 reads it as "never committed". Both meet the safety goal; the design amendment PR (O2) should settle the path once.
5. **C-014: `coordinator_autostart`.** The V2 advocate concedes the need (section 6 item 5) but its table leaves the key out. D06 item 6 needs some mechanical form of "recorded authorization"; whether that is a config key or a records entry the dispatcher reads is open.
6. **Numbers with no source**: go expiry, in-flight expiry, binding timeout, hand-back round cap, reviewer hold. Owner answers in chat; until then the related automation stays off.
7. **A-003: the interim ledger's exact place and name.** `.dev/tasks/` (always staged) is the best existing convention found; the owner may prefer the unified plan's owner-action section. Either works if the first coordinator PR imports it.

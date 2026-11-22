# Merge Log (Step 5)

## Metadata

- Base: V3, `variant-3-haiku-backend.md` (haiku:backend), per `base-selection.md`.
- Incorporated: V1 `variant-1-opus-architect.md`, V2 `variant-2-sonnet-analyzer.md`, `debate-transcript.md`, `rounds/round2-advocate-3-haiku-backend.md` (store and X-001 evidence), `invariant-probe.md` (27 findings), verdicts D01 to D16 and Q01 to Q03 (D15 and D16 read in full).
- Plan executed: `refactor-plan.md` (Final decisions K1 to K23, X-001, required structure 0 to 9, stage list S0 to S17, owner-action list, Changes NOT Being Made).
- Executor: merge-executor agent.
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/merged-output.md` (150,520 bytes, about 147 KiB).
- Method: stub first (title, glossary placeholder, ten section headings each with a `FILL` placeholder), then one Edit per section or sub-section; sections 2, 5 and 8 filled in three Edit calls each; a trim pass on sections 2.1, 2.2, 3 and 5 afterwards.
- Changes applied: 14 of 14 planned changes.
- Status: COMPLETE with one deviation (length over target, see Summary).
- Timestamp: 2026-11-20.

## Changes Applied

| # | Output section | Status | Source | Provenance tag in the output | Validation |
|---|---|---|---|---|---|
| 1 | 0 Status and glossary; 1 Summary | Applied | V3 section 1 rewritten as sentences; V1 section 1 five decisions; V2 section 1 last paragraph | `<!-- Source: Base (V3 header ...) ... plan change #1 -->`; `<!-- Source: Base (V3 section 1, ten lines) ... -->` | Glossary defines every code class (K, X-001, S, MC, O, H0 and lanes, OA, RK, INV, D/Q with line notation, OD, C-INV, MR, M, NG-2, WC, G2, R-rows, U-rows, T/AU, planb, pr-a, pr-p, master, status tags, ledger words, D15 table rows). INV-025 stated in the status block and in decision 2 |
| 2 | 2 Diagram | Applied | V1 section 2 diagram; V2 2.0 tags; V3 flow | `<!-- Source: V1 section 2 diagram, merged per plan change #2 ... -->` | Poll claims (K1), saved intent, replay, plan approval [R], F worker, typed go, head-pinned merge; tags on every box; tag [R] added for removed-by-682 items (derived from the REMOVED ledger word) |
| 3 | 2.1 Issue watcher | Applied | V3 spine; V1 STAYS list and symbols; V2 2.1; round 2 advocate 3 section 3b | `<!-- Source: Base (V3 section 2 "Issue watcher") ... plan change #3 -->` | Contains `approval_of`, `unchanged_since`, `_revalidate`, `marker_in_window`, MR-1, MR-2, `held_incomplete`, `held_backlog`, NG-2, cron line, run-all, state root, kill switches, nine store states including `woken`, `acked`, `waiting_reapproval` |
| 4 | 2.2 Coordinator | Applied | V3 spine; V1 verbs and flags; V2 2.2 | `<!-- Source: Base (V3 section 2 "Coordinator") ... plan change #4 -->` | 12 verbs of D15 R-7; flags; `refuse(argv)`; `E-NO-GRANT`; 13 gate reasons; reviewer hold; AU1 to AU8; restored plan-approval step with the OA-1 condition; INV-007, INV-017, INV-018, INV-019 handled |
| 5 | 2.3 Observability | Applied | V3, V1, V2 section 2.3 | `<!-- Source: Base (V3 section 2 "TUI dashboard ...") ... plan change #5 -->` | Observer reads `status --json` (K10); sweep fields and saved JSON; D11's two HIGH rules; questions-panel exception stated |
| 6 | 2.4 Claim pipeline | Applied | V3, V2, V1 section 2.4 | `<!-- Source: Base (V3 section 2 "Issue claim ...") ... plan change #6 -->` | Rule C1, plan-less warning, `--plan`, `--remaining`, closeout, cleanup with Q02, issue 689 split |
| 7 | 2.5 Integrity rules | Applied | V3 section 4 integrity paragraphs kept whole; invariant probe | `<!-- Source: Base (V3 section 4 ...) plus invariant probe ... plan change #7 -->` and `<!-- Source: invariant probe INV-001, ... -->` | INV-001, INV-004, INV-006, INV-011, INV-012, INV-013, INV-016, INV-027 added |
| 8 | 3 Contradictions | Applied | Plan Final decisions; V1, V2, V3 section 3 | `<!-- Source: union of V1 section 3, V2 section 3 and V3 section 3 into K1 to K23, merged per plan change #8 ... -->`; `<!-- Source: debate round 2 (X-001) ... -->` | 23 rows, each with verdicts in conflict, pick, reason, reversal; X-001 paragraph with options (a), (b), (c); code-basis paragraph kept from V3 |
| 9 | 4 Interface table | Applied | V1 26 rows, V2 27 rows, V3 rows | `<!-- Source: V1 section 4 (26 rows), V2 section 4 ..., merged per plan change #9 ... -->` | 41 rows with variables (`<config_dir>`, `<state_dir>`, `<worktrees>`, `<log_dir>`, `<guard_state>`, `<repo-key>`), no host paths; "who writes what" table with one writer per file (INV-011, INV-012) |
| 10 | 5 Stages | Applied | V2 section 5 structure; plan stage list; V1 and V3 section 5 | `<!-- Source: V2 section 5 ..., merged per plan change #10; MC-11 and MC-12 from invariant probe ... -->` | S0 to S17 (S15 as S15a to S15d); MC-1 to MC-12 defined once; stage map with lanes and O codes; preconditions and rollback per stage; OA-1 "start gate only" path stated |
| 11 | 6 Ledger | Applied | V2 section 6 evidence; V1 rows; V3 consequences | `<!-- Source: V2 section 6 ..., merged per plan change #11 -->` | 35 rows, evidence column, consequence column, stage column |
| 12 | 7 Owner actions | Applied | V1 section 7 base; V2 and V3 answers; D16 rank table; INV-003, INV-023, INV-024; X-001 | `<!-- Source: V1 section 7 (OA-1 to OA-22) as the base text, merged per plan change #12 ... -->` | OA-1 to OA-27 grouped by first-needing stage (S0; S4 and S5; S11 to S15; S17; not blocking); one line per answer; recording method stated; D15 OD-3 to OD-9 listed with recommended answers |
| 13 | 8 Risks | Applied | V3 failure table; V1 RK rows; V2 R rows; invariant probe | `<!-- Source: Base (V3 section 8 ...) ... plan change #13 -->`; `<!-- Source: V1 section 8 (RK-1 to RK-17), V2 section 8 ... -->`; `<!-- Source: invariant probe INV-001 to INV-027 ... -->` | 8.1 failure table (20 rows); 8.2 register RK-1 to RK-34, each with severity, likelihood, impact, unproven, mitigation, proving test; 8.3 all 27 INV rows with handling; 8.4 UNVERIFIED list |
| 14 | 9 Provenance | Applied | Plan | `<!-- Source: refactor plan "Planned Changes" ... plan change #14 -->` | Citation roots (the only absolute paths in the document) and a part-by-source table; rejected items listed |

**Executor decisions inside the plan's latitude (logged, not new strategy).**

1. MC-10 lists `coordinator_absent` beside the plan's three added reasons, because K11 (a plan decision) names that reason and V1's reasons list carries it.
2. RK numbering is new (RK-1 to RK-34). V1's RK-1 to RK-16 keep their meaning except RK-7: V1's "coordinator cannot run the claim skill" moved to 8.4 (UNVERIFIED list) because K1 makes it relevant only to `claim_by: coordinator`; RK-7 is now the X-001 overlap. V1's RK-17 (low limits) split into RK-30 and the K10 reversal.
3. V1's OA-12 option "standing closeout grant" and an OA-26 option "standing go for records pushes" were not carried, and K12's reversal no longer offers "a recorded closeout grant": each would contradict an owner rule (no standing `issue.close`; a typed go for every push). D15 C-INV-4's closeout-grant alternative is therefore not offered as an owner choice.
4. V1's OA-19 (`start_mode` switch) was rewritten as "enable one throwaway repo, `claim_by: poll`", because the plan rejects `start_mode`. V1's `BOUND_WORKERS_PROVEN` is spelled `WORKER_BINDING_PROVEN` (plan K16).
5. Typed-wake acceptability (D15 row B5) was attached to OA-18; D15 OD-3 to OD-9 are listed with recommended answers, not given OA numbers, to keep the plan's count of 27.
6. Interface row 8 (store backup file) was added to carry the plan's S11 backup and downgrade step; its file name is marked UNVERIFIED.
7. The D12 claim safeguards labelled S1 to S5 in the sources were renamed "D12's five claim safeguards" so that S1 to S5 mean stages only. "D05's risk row K12" is never written as a bare K12; it is described as "the design's own 'workers run unbound' risk row", and D04's design row K4 as "the related row in the design's own risk register".
8. A glossary row explains that D15 element-table rows (A1, D8, E7 and so on) are not verdict ids.

**Citation spot checks (18 checked against the snapshots, read-only).**

| # | Citation | Result |
|---|---|---|
| 1 | master `cycle.py:228` `enabled` default false | Correct |
| 2 | master `hooks/scripts/launch-level-guard.sh:771-772` "text only ... real fix is the L2 layer" | Correct |
| 3 | master `launch-level-guard.sh:785-803` level table; COMMIT, PUSH, SUBMIT at FS only (787), F denied (789-790) | Correct |
| 4 | master `orca_worktree.py:1515-1523` `cmd_pending` | Correct |
| 5 | master `predicates.py:14` `CLAIM_MARKER`; `:279` `marker_in_window` | Correct |
| 6 | master `launch.py:33` `PROMPT_PATTERN` | Correct |
| 7 | master `record.py:34-35` six states; `:440-441` 60-minute reporting lease; `:447-448` claimable and resettable sets | Correct |
| 8 | master `cli/sweep/report.py:642` rows; `cli/sweep/commands.py:277-278` JSON to standard output | Correct |
| 9 | pr-a `wake.py:46-47` schemas; `:69` `.orchestrator/wakes`; `:545` `read_ack` | Correct |
| 10 | planb `generate.py:252` Coordinator worktree; planb `launch.py:48` `GOVERNED_LEVELS_ALLOWED = False` | Correct |
| 11 | `_TOP_KEYS` location: plan cited "master `cycle.py:216-233`" | FIXED: the list is defined at master `cycle.py:58` and checked at `:216` (planb `:59`, `:223`); the output says so in K4 and S12. V2's "`cycle.py:76-83` `_TOP_KEYS`" was wrong and is not carried |
| 12 | master `skills/sc-issue-protocol/refs/claim.md:94, 96` | Correct |
| 13 | master `cli.py:165` `status --json` option | Correct |
| 14 | master `core/WORKER-CONTRACT.md:41` WC-9; `:245` push on the person's go; `:246` explicit paths plus `.dev/tasks`, stop on hook rewrite, never `--no-verify` | Correct (`:246` additionally supports INV-019 and INV-020 handling) |
| 15 | master `docs/designs/issue-pipeline-guard-g2.md:9` owner's G2 sentence | Correct |
| 16 | pr-a `cycle.py:992-994` "never woken again" | Correct |
| 17 | master `hooks/scripts/launch-level-pre-push.sh:6-9` refuses only main and master | Correct |
| 18 | pr-p `plan_body.py:138` `plan_check` | Correct |

## Post-Merge Validation

**Structural integrity.**
- Heading levels: one H1, ten H2 (sections 0 to 9 in order), H3 only under sections 2 and 8. No level gaps.
- `grep -n 'FILL:' merged-output.md`: no output (0 placeholders left).
- `grep -nP '\x{2014}|\x{2013}' merged-output.md`: no output (0 em or en dashes).
- Provenance: 25 `<!-- Source: ... -->` comments plus the document header comment naming the base and the merge date 2026-11-20.
- Host-specific absolute paths appear only in section 9 "Citation roots" (7 lines); the contract tables use variables.
- `src/superclaude/` appears only as repository source paths (MC-2, MC-9, the S14 maintainer instruction) and in the glossary's citation rule; installed locations are written as `~/.claude/...`.

**Internal references (defined exactly once / distinct ids referenced / broken).**

| Id class | Defined | Distinct referenced | Total references | Broken |
|---|---|---|---|---|
| K1 to K23 | 23 (one row each in section 3) | 23 | 144 | 0 |
| S0 to S17 (plus S15a to S15d) | 18 + 4 (one bold block each in section 5) | 22 | 214 | 0 |
| MC-1 to MC-12 | 12 | 12 | 82 | 0 |
| OA-1 to OA-27 | 27 | 27 | 114 | 0 |
| RK-1 to RK-34 | 34 | 34 | 63 | 0 |
| INV-001 to INV-027 | 27 (section 8.3) | 27 | 165 | 0 |
| O0 to O7 | 8 (glossary row) | 8 | 59 | 0 |
| X-001 | 1 | 1 | 21 | 0 |

Totals: 154 ids defined, 154 distinct ids referenced, 862 references, 0 broken, 0 out of range (no K24+, S18+, MC-13+, OA-28+, RK-35+, INV-028+, O8+). `C-INV-1` to `C-INV-4` are a separate class defined in the glossary. The one id-collision found during drafting (D12's safeguards labelled S1 to S5) was renamed; no bare K12 is used for the D05 risk row.

**Contradiction rescan.**

| Check | Result |
|---|---|
| K1 (poll claims, coordinator adopts, `claim_by` reserved, throwaway only until X-001) | Consistent in sections 1, 2 (diagram, 2.1, 2.2), 3, 4 (rows 5, 15), 5 (S17), 7 (OA-19, OA-23) |
| K2 (F binding, coordinator commits, push on a go, INV-025 stated) | Consistent in sections 0, 1, 2.2, 3, 5 (S8, S14, S17), 7 (OA-5, OA-20), 8 (RK-2, 8.3) |
| K4 (`run-all`, `schema_version` 1, key-by-first-reader, store migration, absolute child paths, zero-repos alarm) | Consistent in sections 1, 2.1, 2.5, 3, 4 (row 5), 5 (S9, S12, MC-11, MC-12) |
| K5 (state outside git via `state_dir`; records on `coordinators`; go never tracked) | Consistent; report entry files under `.dev/coordinator/orchestrated/` are the report layer's built read contract, not watcher or coordinator machine state |
| K9 (cap 1, single writers, waiting go counts with reminder) | Consistent in sections 2.5, 3, 4, 5 (S15b), 7 (OA-14, OA-25), 8 |
| K16 (`WORKER_BINDING_PROVEN` false refuses real issues) | Consistent in sections 1, 2.2, 3, 5 (S14, S17), 7 (OA-20) |
| Poll writes nothing to GitHub | Holds; label creation only by person-run `repo-init` on a go (K18, row 12) |
| A person's typed go for every merge (and push) | Holds after removing the OA-26 "standing go for records pushes" option drafted during the merge |
| Workers never run `/sc:pr-submit` | Holds; S1's `/sc:pr-submit` loop runs from a person-opened top-level session |
| No standing `pr.merge` or `issue.close` | Holds after removing V1's "standing closeout grant" option and K12's "recorded closeout grant" reversal |
| Approvals given in chat and recorded by an agent | Holds; the S17 live-test record is agent-recorded (V2's owner-written live-test file not carried) |
| "Closes" for a control | None. Remaining uses of the verb refer to GitHub closing an issue on a `Fixes` line, the poll closing a store entry, a person closing a terminal, or Clay closing a PR |

New contradictions introduced by the merge and still present: none. Two drafting-time contradictions were found and fixed (OA-26 option, K12 reversal wording).

## Summary

- Planned changes: 14. Applied: 14. Skipped: 0. Failed: 0.
- Deviation: the merged artifact is about 150.5 KB (147 KiB), above the 70 to 110 KB target. One trim pass (sections 2.1, 2.2, 3, 5) removed about 5.5 KB. The remaining size comes from the plan's required content: a 23-row contradiction table, a 41-row interface table plus the single-writer table, 18 stages with checks and rollback, a 35-row ledger, 27 owner actions with one line per answer, a 34-row risk register with six columns, and all 27 invariant rows. Reaching 110 KB would require dropping one of these required parts (for example the V3 failure table in 8.1, which overlaps RK rows) or the ledger's consequence column; that choice is left to the orchestrator.
- Carried condition: INV-025 (HIGH) is stated, not solved, in sections 0, 1, 3 (K2), 5 (S8, S17), 7 (OA-5, OA-20) and 8 (RK-2, 8.3).
- Nothing was built, pushed, merged, reverted or commented; all code reads were read-only.

## Post-review fixes

Source: an independent reviewer's 6 BLOCKING findings and 14 notes, with binding decisions from the orchestrating session (`brainstorm-unify`). Applied in place with Edit, section by section; every changed block carries a `<!-- Source: post-review fix ... -->` tag (48 tags). Facts re-checked read-only before editing: planb `dispatch.py:404-417`, `first_run.py:3, 16-17, 99-107, 136-137, 193`, `repo_init.py:108`; master `launch-level-guard.sh:263-273` (W becomes WA when `sessions/<sid>.ok` exists) and `:785-790`; master `docs/designs/issue-pipeline-guard-g2.md:14, 22` (route A); master `orca_worktree.py:822` (`IR7_REFUSE = False`); master `test_security_invariants.py:10` (NG-2 bullet); master `record.py:660-665` (T-11); master `commands/issue.md:9, 30, 43-48, 66-69`; master `docs/designs/issue-watcher.md:39` (decision D3); master `WORKER-CONTRACT.md` lines 57, 70, 245, 298, 300 and guard lines 441-443.

| Fix | Before | After |
|---|---|---|
| B1 planb `run-all` not read-only | The watcher "stays `enabled: false`" through every stage; K18 said label creation is "never by the poll or cron"; interface rows named only `repo-init` as config and label writer | New K24 (pick: no scheduled `run-all` before S17; S9 adds defaults key `auto_enable` false so `first_run` does not rewrite `enabled: true`; R33 before R18 met by planb `launch.py:48`). K18 rewritten: the cycle writes nothing; planb's init path creates labels once (D09 rule 2) and needs the owner's chat OK (OA-28). New OA-28 and RK-35. Interface rows 4, 5, 12 and the single-writer table name `first_run`. S9 scope, tests (`test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`) and preconditions; MC-12 asserts the dry run generates nothing; S17 runs the dry run first and enables ONE throwaway repo; OA-19 and the section 1 and section 5 rule text fixed |
| B2 INV-025 overclaim | "A ruleset plus a person's go is the only control that blocks those writes"; "a worker cannot push or merge is only true with a ruleset plus a per-PR go" | The reviewer's exact statement (ruleset stops pushes to `master` and `integration` and, without a bypass, merges; not feature-branch pushes, PRs or comments; the shared-login admin bypass still allows `gh pr merge --admin`; only a separate agent login plus the ruleset makes "a worker cannot merge" true; a go is a procedure, not a block; every control narrows) placed in the status paragraph, section 1 decision 2, K2, OA-5, OA-20, RK-2 and the INV-025 row |
| B3 K2 level | "Bind at F; F is the only built level that allows implementation and refuses commit, push and PR" | K2 pick: with both gates, bind at W (`pending --level worktree`); implementation refused until the coordinator writes the worker's `.ok` after the recorded plan approval (route A, `release-worker`), giving WA; F only if OA-1 keeps the start gate alone or the session id cannot be learned (UNVERIFIED, G2 design section 4, FU-1 precondition f). Owner's route A added to K2's conflict cell. Glossary rows for W, WA, L1, L2 and route A. Diagram steps 4 to 6, section 2.2 binding and plan-approval bullets, interface row 23 and new row 23a (`.ok` file), S8, S14 (tests: W refuses before release, WA allows after; `release-worker` refuses without approval), S17 probe, K16, RK-1, RK-9, RK-23, the 8.1 row, INV-007 and INV-025 wording, ledger guard row |
| B4 go wording | "a go is recommended for every PR step below and is not repeated in each stage" | "A person's typed go is REQUIRED before any push or merge"; "owner's go for this PR" added to the preconditions of S1, S2, S3, S4, S5, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16 |
| B5 records home | The first coordinator PR (S13) "imports" the ledger "into the coordinator records"; records "on the `coordinators` branch" | Records, including the imported ledger, live ONLY on the local `coordinators` branch in the `Coordinator` worktree, by local commits of the recorder, never in a PR to master; pushing needs a go (OA-26). Fixed in section 1 decision 3, K5, K21, interface rows 21 and 22, the single-writer table, S13 (OA-26 added to its preconditions), RK-31, the INV-002 row |
| B6 contract line 57 | OA-7 option "Approve none: line 57 keeps the sentence the owner never worded" | OA-7 and S8 state that the installed line 57 sentence contradicts the owner's standing order; recommend shipping the fix in S8 as its own commit after the owner's ONE chat confirmation; "none" now says the installed text keeps contradicting the owner's order |
| N1 | Diagram step 3 tagged [B] | [N] |
| N2 | "Absent means most restrictive" for every key; K23 "0 is a valid explicit value" | Applies to authority keys only; `reach_daily_max` absent or 0 means no notice cap, malformed is a config error (K4, K23, interface row 5, OA-16) |
| N3 | Single-writer table: poll only for `dispatch.json`; "an agent" for go entries; "the verb that used the grant" for the use log | `reset N` named as the person-run second writer under the same lock; go entries created by the recording agent through the verbs and consumed only by the merge verb; one wrapper function writes `grants-use.jsonl` |
| N4 | S12 carried key loader support; S13 depended on S12 | S9 adds planb's keys; each later PR adds the keys it first reads (S14 merge and grant keys and `probe_issues`; S15 cap and session keys); S12 retagged "status extension and `owner/name` rekey"; S13 no longer depends on S12 |
| N5 | "Only the start gate" fallout differed across places | One paragraph in section 5 (S6, S7 dropped; S8 shrinks; S9 rebases onto a tree without `issue_pipeline`; K3 flips; bind at F); S8 and S9 carry their part |
| N6 | Report entry files "under `.dev/coordinator/orchestrated/`" | In the report skill's per-user state path (D11); that folder name is the legacy default (section 2.3, interface row 37) |
| N7 | "A manual claim with no store entry grants no adoption" | Today T-11 makes a hand claim `claimed`; REQUIRED CHANGE: delivery intent only for entries the poll launched; `test_manual_claim_gets_no_wake` in S11 |
| N8 | "Throwaway" undefined | Glossary row and config key `probe_issues`; K16 refuses worker starts outside it; `test_worker_start_refused_for_real_issue_while_binding_unproven` in S14 |
| N9 | Config writer unrestricted by session kind | `coordinator repos` runs only in a person-opened session and refuses from worker-bound or coordinator-started sessions (interface row 5, RK-10) |
| N10 | "There is no default answer" against "the recommended answer is how the spec is written" | "Until the owner answers, nothing that depends on the answer is switched on; the spec is written to the recommended answer only as a plan" (section 2.2, section 7 intro) |
| N11 | "removes the overlap at its root" | "avoids a second agent in that worktree" |
| N12 | OA-5 sub-questions in one line; OD-3 to OD-9 as a prose note; OA-16, OA-26 with no stage; OA-18 under S17 | OA-5 has one line per answer; OA-29 to OA-34 added (OD-6 and OD-7 share OA-32), each "gates no stage"; OD mapping in the glossary and after OA-34; OA-16 names S15c, OA-26 names S13, OA-18 moved to the S11 to S15 group (S15a) |
| N13 | `commands/issue.md:104-110`, `claim.md:48, 91-92` cited for levels; WORKER-CONTRACT and guard lines unlabelled; `test_security_invariants.py:12` unlabelled; IR7 "(V3 ledger)" | Levels cited at `commands/issue.md:9, 30, 43-48, 66-69`; lines 298, 300 and guard 441-443 labelled as the pre-deletion tree `01e7a9e23^`. Reviewer correction not applied as written: master's lines 57, 70 and 245 were checked and DO hold the cited sentences (line 57 contains "still written by the owner"), so they are labelled master numbering; `:12` labelled as the pr-a tree with master's NG-2 bullet at line 10; IR7 cited at master `orca_worktree.py:822` |
| N14 | Missing glossary rows; "the D3 prompt rule" | Rows added for W, WA, L1, L2, route A, throwaway, debate diff points, design rows, N6, N7, PR B, OB-H1 to OB-CTX, IR7, Q01's four tests; renamed "the owner's integer-only prompt rule (decision D3 of `docs/designs/issue-watcher.md:39`)" |

**Validation after the fixes.**
- Structure: 1 H1, 10 H2 (sections 0 to 9 in order), 9 H3, no H4, no level gaps; `grep -n 'FILL:'` prints nothing; `grep -nP '\x{2014}|\x{2013}'` prints nothing (both files).
- Ids, defined exactly once / distinct referenced / total references / broken: K1 to K24: 24 / 24 / 170 / 0. S0 to S17 plus S15a to S15d: 22 / 22 / 237 / 0. MC-1 to MC-12: 12 / 12 / 84 / 0. OA-1 to OA-34: 34 / 34 / 158 / 0. RK-1 to RK-35: 35 / 35 / 64 / 0. INV-001 to INV-027: 27 / 27 / 166 / 0. O0 to O7: 8 / 8 / 59 / 0. X-001: 1 / 1 / 22 / 0. Totals: 163 defined, 163 referenced, 960 references, 0 broken, 0 out of range.
- Contradiction rescan: K1, K2 (now W then WA, F as fallback), K4 (with K24), K5 (local records branch), K9, K16 (with `probe_issues`) are consistent across sections 0 to 8. Owner rules: the poll cycle writes nothing to GitHub (planb's init label write is a separate, gated write, K18 and K24); a person's typed go is required for every push and merge; workers never run `/sc:pr-submit`; no standing `pr.merge` or `issue.close`; approvals given in chat and recorded by an agent. The rescan grep for the retired phrases ("only built level", "go is recommended", "the only control", "never by the poll or cron", "watcher stays `enabled: false`", "removes the overlap", "recorded closeout grant", "standing go for records") finds nothing. New contradictions introduced by the fixes: none found.
- Provenance tags: 71 (48 post-review).
- Size: 173,541 bytes (about 170 KiB), up from 150.5 KB; kept as instructed (no trimming of required content).

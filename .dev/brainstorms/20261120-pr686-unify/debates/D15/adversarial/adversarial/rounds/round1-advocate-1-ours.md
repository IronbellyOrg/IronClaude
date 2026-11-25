# D15 Round 1: Advocate for Variant 1 (OURS)

Topic: Clay strengths bundle, what to adopt and how. Variant 1 = OURS (the owner's line). "They" means Clay (account `clayphi`); the repository owner is `ironbelly`.

Notation: "D:nnn" is a line of `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master`. "Dnn" is `debates/Dnn/VERDICT.md`. Facts I read myself in this round: `pr-a/tests/issue_watch/test_audit.py:78-106`, `pr-a/src/superclaude/cli/issue_watch/cycle.py:994`, the design's T, U and K table rows (80 of them) and its test row T3, and `FULL-REPORT.md` lines 34 and 43. Everything else is taken from the verdicts and cited by their id. Anything I did not re-read is marked UNVERIFIED.

## Position summary

Adopt Clay's elements one at a time, each against the weighting rule, each re-homed under the owner's rules. The 13 verdicts already did this: every one of them is a HYBRID, and between them they take every Clay capability the owner's line lacked (cap, restart, merge gate, audit, typed-answer check, refusal list, hand-back, reasons list) while keeping the owner's gates. The set as built adds only what the verdicts rejected (standing merge grant, assignment-only trigger, no guard, label writes, registry repo) plus parts that have no code.

## Steelman of CLAY

Their strongest version: the control verbs lean on each other, and the verdicts prove it. D06 item 8 says `E-NO-GRANT` does not see a raw `gh pr merge`, so the merge "must go through one verb that demands the go entry". D04 item 6 says the merge gate needs one added reason ("no recorded merge go") so `merge_ok: true` cannot print without it. D05 item 5 pairs `refuse(argv)`, the head-pinned merge and the audit. D06 alone adopts nine Clay parts. So a piece-by-piece table risks leaving a part standing without the part that makes it mean something. A single group of verbs (ADD6, D:140) with one JSON contract and one refusal function (D:767) gives one place to build and one set of tests. They also carry a ready live-test plan: tests T1 to T13 and an 80-row T, U and K register (D:1129-1315) that says plainly what is unproven. Parts of the stack are already merged: `/sc:closeout` (PR 683), the report skill (PR 684), the plan sections in the templates (PR 661); and PR 690 has three review rounds and 23,043 tests passing on its first head (D12). The design has Owner-column tables, so the owner can rule on one named row at a time (D:109-140). And they are right that the owner's line lacks each capability they list (D07 cap and restart, D06 gate, D05 audit, D04 answer-check and refusal list, D12 `--remaining`, D11 reasons list).

## Strengths claimed

1. **Per-element adoption loses nothing Clay offers, and the verdicts show it.** Every capability in the CLAY paper's fact 5 appears in a verdict's "Clay strengths to adopt": in-flight cap and guarded restart (D07 items 3 and 4), merge gate and head-pinned merge (D06 items 1 and 2), audit AU1 to AU8 (D05 item 5, D06), `answer-check` (D04, D06 item 9), `E-NO-GRANT` and `refuse(argv)` (D04, D05, D06 item 8), `--plan` and `--remaining` (D12 item 2), nine-row list (D11 table, D06 item 11). So the extra gain of "adopt the set" over "adopt the table" is only what the table rejects. That is the whole of C-001.
2. **What the set carries beyond the table is exactly what the owner's rules and the verdicts reject.** Assignment-only trigger (D01: assignment never starts work), standing `pr.merge` and `issue.close` grants (D04 item 5, D06 item 8), no launch guard (D05 item 1: guard required), label writes by the poll (D09 item 3: deferred, NG-2 stays), registry repo and `repos.yaml` (D07 item 2), worker running `/sc:pr-submit` (D06 item 5). The CLAY paper's own cost section lists these and says each "needs an owner override", touching lines 73, 76, 81, 116, 117, 118, 135, 138 and 267-305. Taking the set "as the base" means starting from text the verdicts overwrite in at least eight places. That is more rewrite, not less (C-006, C-007, X-002).
3. **The verdicts show the base is OURS for authority, trigger, guard, topology, naming and the label rule.** D01, D03, D05, D06, D07, D08, D09 and D12 each keep the owner's side as the base and graft Clay parts on. Clay's side is the base for the wake transport (D10) and the none-only claim level (D04, which is also the owner's own Q35). So "adopt Clay's set as the base" reverses the verdict pattern on most topics.
4. **Clay's own standard for deleting code applies to their unbuilt verbs.** PR 682's stated reason for deleting the owner's pipeline was "Nothing runs this code ... and never ran live" (FULL-REPORT.md:34). The `escalate`, `merge-gate`, `answer-check` and `asks.json` verbs and the whole `orchestrator` group do not exist in master, pr-a or pr-p (D11 strongest point OURS 3; D06 Unverified: searched `src/` in the three exports only). The owner's pipeline had 117 test functions and an eleven-line live record from the first live test (D03 "Our strengths that must be kept"). So "never ran live" is not symmetric (X-001): theirs is design text, ours had code, tests and a partial live record, and the argument was used against us.
5. **The 62-reason table is not adoptable as built, and the pin proves it.** `test_audit.py:94` asserts `not (REMOVED_14 & audit.REASONS)`, and lines 86-93 name the removed reasons: `not_approved`, `approval_before_trigger`, `edited_after_approval`, `project_mismatch`, `edits_unreadable`, `marker_unreadable` and others. D01 requires an approval gate, an unchanged-since check, the Status allow-list and the marker guard (MR-1, MR-2), so those reasons must come back. Adopt the table's shape (a kind plus an exit code per reason; `ack_not_observed` and `attempts_exhausted` exit 7, same file lines 101-106) and rewrite the pin. That is "adopt with change" (C-003, U-001).
6. **Two defects sit in Clay's wake code and their paper does not mention them.** D10 M1: an acknowledgment can arrive before the issue's state file exists, so a crash between the two loses the issue (`cycle.py:777-810`, from D10; not re-read by me). D10 M2: an abandoned wake is never woken again. I read `cycle.py:994`: it returns `None` with the comment "already woken, acknowledged or abandoned: never woken again". The right result is to adopt the file-plus-ack transport (D10 items 1 to 3) with M1 and M2 as conditions. A bundle "as built" ships both defects unless someone remembers to amend (C-004, U-002).
7. **Placeholder gap in the plan check.** `plan_check` strips only HTML comments (D09 item 6; `hold.py:69-70`, `:140`), so the unfilled issue template with `<...>` placeholders passes. D12 adds that `plan_body.py` passes any non-empty text except "Not known yet", so "TBD" passes and a heading inside a code fence counts. Adopt `plan_check`, add the placeholder rule, define "passes" once (D12 item 2b) (U-003).
8. **Clay's numbers and paths are unproven, and the design says so.** The tier path through `worker-start --model <picker id>` is UNVERIFIED (U28, `orchestrator.md:726`); `HANDBACK_MAX` = 3 is "this design's value, not measured" (`orchestrator.md:612`); the cap of 5 notices is "not ruled on; open" (AD-B4, D:1177, from D11); the mailbox send needs U5 (D10 item 2); the typed-answer check cannot tell a person from a script (D06 item 9, INV-003). I did not re-read lines 612, 726 and 1177 myself, so those three are UNVERIFIED by me and rest on the OURS paper and D11. Adopt the mechanism, hold the numbers as proposals (C-005).
9. **Settings home.** One home for per-repo settings must be chosen (A-006), and D07 chose `~/.config/superclaude/issue-watch.d/<repo>.json` with a `merge` block: `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`. These are Clay's key names, kept; Clay's `repos.yaml` file and registry repo are removed. PR 686's `repos.py:47-84` parser for those keys is reusable (D06 actions). So the key names are adopted and the home changes (C-009).
10. **Every adopted row needs a rename and a re-home whichever approach is used.** D08 action 8 renames `orchestrator-wake/1`, the mailbox kind, `orchestrator_tier`, `.orchestrator/`, the golden fixture, the typed line and the `superclaude orchestrator ...` verbs, and it must land before PR 686 merges. D07 re-homes the settings. A bundle pays these per row too (X-002), because the names sit in wire strings and code (pr-a `wake.py:46-47`, per D08).
11. **Merged is not endorsed.** CLAY fact 1 treats the merged pieces as half the stack. Yet PR 681 and PR 682 merged three seconds apart, 66 minutes after PR 682 opened, both by `clayphi` (D03 strongest point OURS 3), and FULL-REPORT section 4 finds no `ironbelly` approval of PR 681 (D06 Implications; D13 "Owner must know"; neither re-checked by me). D08 notes the design's status "approved by the owner (Clay)" does not make the name `/sc:orchestrator` an owner decision. The merged pieces that are sound (PR 683 closeout, PR 684, PR 661, PR 670) are already adopted as is in my table. So merged status gives no extra reason to take the unmerged pieces.
12. **Merging PR 686 as the base is unsafe in the order the verdicts need.** D03 item 3: a revert of PR 682 plus the PR 686 merge give no textual conflict but a broken tree, with `superclaude --help` crashing and 29 test modules failing at collection. "Adopt as built" conflicts with the revert that D03 recommends. A table keyed to files and rows, not to PR 686, survives whichever way D14 goes (A-003).

### The per-element table (OURS)

| Clay element | Outcome | Change on the way in | Needs (neighbour) | Evidence |
|---|---|---|---|---|
| `/sc:closeout`, PR 683 | Adopt as is | writes need a named grant | none | D13 item 1 |
| Landed check `branch-landed.sh` | Adopt as is | none | closeout | D13 item 3 |
| Daily PR log, PR 670 | Adopt as is | none; stays outside the coordinator | none | D13 item 5 |
| Plan sections in templates, PR 661 | Adopt as is | none | none | D12 item 1 |
| Silent-loss rules, `check.py` | Adopt as is | stay in the report layer | report | D11 table |
| Report skill, PR 684 | Keep | person-specific config out, state path configurable | none | D11 actions |
| `plan_check` and `held_incomplete` | Adopt with change | placeholder rule, runs before approval, one definition (`plan_body.py check`) | D01 start rule | D01, D09, D12 |
| `hold:backlog` | Adopt with change | person-set, poll only reads | D01 | D01, D09 |
| `--plan`, `plan_body.py`, `--remaining` (PR 690) | Keep and adapt | 4 changes (fence-aware count, one check, caller named, live head confirmed) | handback consumer unbuilt | D12 item 2 |
| Wake file plus ack, 3 deliveries, unread mark | Adopt with change | M1, M2, no titles, no copied terminal code | state-file order | D10 |
| In-flight cap | Adopt with change | child cycle, per coordinator id, named closing writer and expiry | per-repo config | D07 item 3 |
| Guarded restart | Adopt with change | no 30-minute idle end, bounded, store counter | session detection (U25) | D07 item 4 |
| Merge gate, 13 reasons | Adopt with change | never merges alone, run twice, added reason "no recorded merge go" | go entry, merge verb | D06 items 1-3, D04 item 6 |
| Merge-time reviewer hold | Adopt with change | owner-set `reviewers` list, final-head re-trigger, 60 min UNVERIFIED | merge-gate | D06 item 4 |
| `answer-check` | Adopt with change | owner identity as parameter, limit stated | go entry | D04, D06 item 9 |
| `E-NO-GRANT` | Adopt with change | drop `pr.merge` and `issue.close` from grants | merge verb | D04 item 5, D06 item 8 |
| `refuse(argv)` | Adopt with change | binds only the coordinator's verbs | verb group | D04, D05 |
| Audit AU1 to AU8 | Adopt with change | state it does not see a push with no PR | none | D05 item 5 |
| Four standing grants | Adopt with change | only `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold` | `E-NO-GRANT` | D04 item 5 |
| Per-repo merge keys | Adopt with change | live in `issue-watch.d/`, role read live at merge time | D07 | D07 item 5 |
| Flags `--wake`, `--hourly`, `--resume`, `--take` | Adopt with change | on `/sc:coordinator` | rename | D08 item 2 |
| Living report | Adopt with change | state path configurable, entries store only `session_id` | sweep | D11 |
| Nine-row reasons list | Adopt as inventory | "the person" not Clay; Owner DECISION | notice step | D06 item 11, D11 |
| Cap of 5 notices | Proposal only | default stays 0 until owner rules | none | D11 |
| Precheck automation | Fallback only | disabled first, shadow run, owner creates | cron decision | D02 item 4 |
| Depth-0 script start | Adopt with change | authorization recorded in chat | WC:70 amendment | D06 item 6 |
| Test plan T1 to T13, U and K register | Adopt as skeleton | rewrite T1 to T3 (T3 expects `repo_not_listed`, which D07 removes) | D07, D08 | design grep, D07 item 2 |
| Registry repo, `orchestrators.json`, `repos.yaml` | Reject | none | none | D07 item 2 |
| Assignment-only trigger | Reject | none | none | D01 |
| Standing `pr.merge`, `issue.close` | Reject | none | none | D04, D06 |
| Worker runs `/sc:pr-submit` (ADD1) | Reject | none | none | D06 item 5 |
| Poll writes the `hold:plan` label | Defer | NG-2 amended only if owner enables | none | D09 item 3 |
| 62-reason table as pinned | Not as is | rewrite pin, bring back the old reasons | D01 | `test_audit.py:94` |
| Tier path and `HANDBACK_MAX` = 3 | Hold as unproven | live check first | none | orchestrator.md:612, :726 (UNVERIFIED by me) |
| Move brainstorm and design into create | Defer | owner decision on B2 | none | D12 item 7 |

## Weaknesses identified in CLAY

1. **"One interlocked set" overstates the coupling (C-001, A-002).** The interlocks are real for the merge path (D06 item 8, D04 item 6), but most of the table has no neighbour: closeout, PR log, report, landed check, `plan_check`, `hold:backlog`, the wake file, the in-flight cap and restart each stand alone (table column "Needs"). The coupling argument supports building the merge path as one unit, not adopting everything with a contested rule inside.
2. **"Adopt the set as the base" reverses most verdicts (C-001, C-006).** See Strength 3. The base was chosen per topic by evidence, and a fixed base means the owner amends rows that the verdicts already settled the other way.
3. **The set's contested rules are encoded in code and tests, not only in text (C-006).** Their own risk section says so: the NG-2 test pins three label calls (`pr-a/tests/issue_watch/test_security_invariants.py:12`); the default grants include `pr.merge` and `issue.close` (D04 action 4); PR 686 deletes the approval, trigger, Project and approver code (D01: 14 symbols in `predicates.py`, about 30 in `github.py`). "Amendments" to that are code changes, not row edits.
4. **The test plan is shaped by the topology it came from (C-003, U-004).** Row T3 expects `repo_not_listed` and a listed repo with `clone_parent` (I read it), and T1 uses two orgs; D07 removes `repos.yaml`, the registry and `repo_not_listed`. So the plan is a skeleton to adapt, not a base to adopt "as built". The U-register is honest and I adopt it; but the same register shows how much is unproven (80 T, U and K rows).
5. **"Never ran live" does not cut both ways the way X-001 says (X-001).** See Strength 4. Fact 8 of their paper is a tu quoque. The deletion was Clay's argument (FULL-REPORT.md:34), D03 recommends the revert, and the weighting rule puts the burden on the side that wants to add the unbuilt piece.
6. **The rewrite-cost claim has no number (C-007, X-002).** The paper says cost is "paid per piece instead of once" but gives no count or estimate. In the bundle, every row still needs the D08 rename, the D07 re-home and the contested-rule amendments (their own list of eight line ranges). A per-element table names the same changes in one column.
7. **Owner-column tables are a real format benefit but not a reason to take the content (U-007).** The column lets the owner rule on a row (D:109-140), but D08 shows OQ5 has "no" in that column and no ruling covers the command name, and D04, D05 and D08 say rulings R9, R10 and ruling 3 are Clay's, not `ironbelly`'s. A row the owner has not ruled on defaults to OURS under the weighting rule.
8. **Evidence of readiness is mixed (C-008).** PR 686 passes 6 of 6 checks, but passing CI does not test the unbuilt verbs and D03 shows the combined tree breaks. PR 690's 23,043 tests cover a presence-only plan check (D12 "Plan check is presence, not quality"). I keep PR 690 (KEEP-ADAPT), so the evidence supports the table's row, not the bundle.

## Concessions

1. The merge path is genuinely interlocked: the merge verb, go entry, `merge-gate`, `E-NO-GRANT` and `answer-check` must be built and tested together (D06 item 8, D04 item 6). My table should say so, and I accept it as a build unit. This is a HYBRID on C-002.
2. A single verb group with one JSON contract and one refusal function (U-006, ADD6, D:140, D:767) is a sound home for the verbs the verdicts adopt, renamed to the coordinator (D08 item 8). I concede the build home. Not conceded: that the unbuilt verbs are therefore proven.
3. The test plan T1 to T13 and the U and K register are a better starting point for the live test than anything the owner's line has (U-004). Adopt as the skeleton and adapt T1 to T3.
4. Clay's wake transport (file, ack, 3 deliveries, unread mark) wins its topic (D10), because the owner's line has no way to reach a running coordinator (Coder issue 516 gap).
5. Merged stand-alone pieces (closeout, PR 684 report, PR 661, PR 670) are adopted as is, and PR 690 is kept with four changes. "Already half on master" is true for these.
6. The Owner-column device (U-007) is useful. Adopt it in the unified spec.
7. Weaknesses of my own variant: a per-element table is longer to write and review than "merge the stack", and cherry-picking can leave a piece that leans on a part we rejected (`E-NO-GRANT` listing `pr.merge`). The "Needs" and "Change" columns are my answer, but they must be kept current. I did not re-read design lines 612, 726 and 1177 myself, and D06, D07, D10 and D11 each list unproven premises (U5, U25, U28, session detection), so some table rows rest on unverified behavior.
8. I cannot show that piecemeal costs less in total; I show only that it costs no more (X-002). That is enough under the tie rule, but it is not a win on cost.

## Shared assumptions

- **A-001 (verdicts are the baseline although they are recommendations): QUALIFY.** The verdicts are advocate-and-merge outputs, not owner rulings; D01 R19, D04 R9 and R10, D06 amendments, D08 branch names and D13's cleanup design all await the owner's word in chat. Every table row should carry "depends on owner decision" where that is so, and an unruled contested item defaults to OURS under the weighting rule.
- **A-002 (Clay's pieces can be classified per element without breaking interlocks): QUALIFY.** True for most rows, false for the merge path, where D06 item 8 and D04 item 6 show the verbs must ship together. The table needs a "Needs" column, and the merge path is built as one unit.
- **A-003 (a carrier PR exists for each element): QUALIFY.** Carriers are PR 686 (D14 undecided; D03 says it must not merge ahead of the revert decision), PR 690 (KEEP-ADAPT), the unbuilt coordinator-skill PR B, and merged PRs 661, 683, 684, 670. The table is keyed on files and rows, not PRs, so it survives any D14 outcome.
- **A-004 (the verbs bind what they claim): REJECT.** D06 INV-003 and D05 K22 show `answer-check` cannot tell a person from a script and `refuse(argv)` binds only commands the verbs run. "Adopt" must read "narrows", never "closes" (D06 item 10), and the table's "Change" column states each limit.
- **A-005 (the weighting rule applies to bundles): ACCEPT.** A bundle must show a bundle-level benefit; the CLAY paper shows only per-piece benefits plus an unquantified rewrite saving, so under the tie rule the per-element table stands.
- **A-006 (a single file for per-repo settings will be chosen once): ACCEPT.** D07 already chose `issue-watch.d/<repo>.json` with a `merge` block; `repos.yaml` appears only in the rejected table. D04 and D06 name `repos.yaml` because they quote Clay's text; read them as "the per-repo config".
- **A-007 (names change before merge for every element with a wire or verb name): ACCEPT.** D08 action 8 lists the strings, and master carries none of them today, so the cost is zero now and grows after PR 686 merges. It applies equally to both variants, which is why X-002 does not favor the bundle.

## Per-point calls

| Point | Winner | One-line reason |
|---|---|---|
| C-001 | OURS | Per-element table keeps every cited Clay capability and drops only the contested rules (Strengths 1 and 2). |
| C-002 | HYBRID, leaning OURS | Verbs are design text with no code (D11, D06), so adoption is building; I concede one verb group as the build home and the merge path as one unit. |
| C-003 | OURS | `test_audit.py:94` forbids the old reasons D01 needs; adopt the table's shape and the visible-reason idea, rewrite the pin. |
| C-004 | OURS | M1 and M2 are real defects in Clay's code (D10; `cycle.py:994` read); the ack mechanism is adopted with them as conditions. |
| C-005 | OURS | Tier path and `HANDBACK_MAX` are unverified or unmeasured; I concede hand-back as a capability gap and take it through PR 690 `--remaining`. |
| C-006 | OURS | Standing merge grant, assignment trigger, no guard, label writes and registry are all rejected or deferred by D01, D04, D05, D06, D07, D09. |
| C-007 | OURS (tie goes to OURS) | The rename (D08) and re-home (D07) hit every row under both approaches; Clay gives no figure for savings. |
| C-008 | HYBRID | Merged stand-alone pieces and PR 690 are adopted as is or adapted; PR 686 CI and PR 690 tests do not prove the unbuilt verbs or the plan check's quality. |
| C-009 | OURS on the home, CLAY on key names | Per-repo config under `issue-watch.d/` (D07); `merge_method`, `release_merge_method`, `reviewers` and `merge_safety_files` keys are adopted. |
| X-001 | OURS | Clay's own deletion reason was "never ran live"; unbuilt verbs have no code, while the owner's package had 117 tests and a live record (D03). |
| X-002 | Tie, so OURS | The rename and re-home are paid per row under both approaches, and Clay offers no count. |

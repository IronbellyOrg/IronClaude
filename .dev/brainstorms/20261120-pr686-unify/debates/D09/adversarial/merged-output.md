<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (CLAY paper) -->
<!-- Merge date: 2026-11-20 -->

# Merged position: D09 watcher writes to GitHub

## Claim
<!-- Source: Base (original, modified): CLAY Claim rewritten as the agreed hybrid per Change #1, using Variant 1 Claim and Concession and the Round 2 final positions; the write count is fixed per Change #4 -->
An issue with no plan is not ready, and the system must not spend a launch on it. After Round 2 both advocates agree on a hybrid. Adopt now: the read-only `plan_check(body)` and the `held_incomplete` skip. Allow later, as one named exception: the poll adds or removes one label, `hold:plan`, behind the `issue.hold` grant, and does nothing else on GitHub. That write stays off until a dry-run shadow run and a label-write-under-cron test both pass. NG-2 is amended to name exactly those two writes. Decision D2 is unchanged: it names assign, comment and Project moves, and a label add is none of them. Confidence: 92% on adopting the check (C-001), 62% on the label write (C-002).

## Who may write what
<!-- Source: Variant 1 Cited facts 4 and 6 (R24, WC-9, `claim.md:9`) merged per Change #2; rows set to the Round 2 final positions -->
Rule: least privilege by actor. Workers never write (WC-9). Only the orchestrator writes in `sc-issue-protocol` (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:9`). A completion write needs that issue's grant row (R24, in the owner's local, unpushed `requirements.md:50`). The poll is the one named exception.

| Actor | Allowed GitHub writes | Condition |
|---|---|---|
| Worker | None | WC-9 |
| Poll | Add or remove the existing label `hold:plan`. No comment, no other label, no label creation | `issue.hold` grant present; code stays off until the dry-run and the label-write-under-cron test pass; NG-2 amended to say this |
| Per-repo init | Create `hold:plan` and `hold:backlog` once per repo | R11: the poll never creates a label. The owner's init creates only the trigger label today (agent-reported) |
| Person | Place `hold:backlog`; may remove `hold:plan` by hand | A hand removal does not release the issue while `plan_check` fails |
| Coordinator or orchestrator | Plan body write (grant `issue.body.append_plan_sections`), lease comment, other completion writes | A grant row per write (R24); lease and plan request wait for D07 |

Not adopted: the coordinator writing the label. OURS withdrew it, because a held issue is never sent to a coordinator (`orchestrator.md:459`).

## Mechanism
<!-- Source: Base (original, modified): CLAY Mechanism items 1 and 2 kept; item 3 and the write count changed per Change #4 (poll never creates the label; plan request moved out of scope per "Changes NOT Being Made" C-004, C-005) -->
Line references D:nnn are to `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master/`.

1. `plan_check(body)` is one pure text function: three headings (`## Priority`, `## Fix approach`, `## Test plan`) each present once and not empty or "Not known yet" (D:440). It uses no model and no GitHub call, and it runs before the approval read.
2. The poll reads body and labels from the search row it already fetches, so the decision costs no extra call (D:448). A failing issue is skipped as `held_incomplete` (row 4, D:455). That skip needs no label: a failing check holds the issue whatever the label shows (D:494).
3. With the `issue.hold` grant on, the poll adds `hold:plan` to a failing issue and removes it when the check passes (D:444, rows 3 to 6 at D:450-457). A hand-removed label becomes `hand_removed` and is not re-added (D:446, D:456). `hold:backlog` is placed only by a person and the poll only reads it (D:445).
4. `--dry-run` runs the whole hold step and writes nothing, so a 24-hour shadow run shows the holds before any write (D:461).
5. Out of scope here: the one-hour plan request (a wake-file item, D:467-484) and the lease comment (DQ3, D:113). Neither is a poll GitHub write, and both wait for the topology decision D07.

## Cited facts
<!-- Source: Base (original, modified): CLAY Cited facts 1 to 8 kept and corrected (facts 2, 3, 5, 7 per Change #4 and the debate); fact 9 replaced per Change #3; facts 4 and 11 to 13 added from Variant 1 Cited facts 1 to 3 and the Round 2 record -->
1. The gap is real: nothing in master holds a plan-less issue. PR 651 only adds template sections; it does not stop an empty issue being claimed. Source: `H-design681-map.md:53` (Clay's paper; not re-read in the debate).
2. The design grants two writes: "add the label, remove it. The poll posts no comment about the hold" (D:444, D:463, ruling 33). The PR 686 code is wider: `github.py:14-18` of the PR head lists create-label, add and remove, and the only DELETE is `repos/<R>/issues/<N>/labels/hold:plan`. Both sides agree label creation moves to the per-repo init (R11), leaving two poll writes. Ruling 33's owner authority and its "as Jay does" comparison are UNVERIFIED.
3. The write boundary is still tested. PR 686 rewrote the NG-2 test to "the only writes to GitHub are the three calls on the `hold:plan` label" (`pr-a/tests/issue_watch/test_security_invariants.py:12`, `:288`, `:634`). It must change from three calls to two. Master pins NG-2 today at `:10`, `:245-251`, `:693-698`.
4. NG-2 is binding: "no GitHub write (REST GET only; GraphQL POST only with a constant query without `mutation`)" (`issue-watcher.md:76`). D2 says the poller "never assigns, comments or moves Project items" (`issue-watcher.md:41-43`, `:48`).
5. The hold is a precondition and not a trigger or approval (D:438). A hand-removed label is not re-added by the same poll store (D:446, AD-A9). But a removal does not release the issue while the check fails (D:456, D:494 limit (d)), and a second workspace with its own store would re-add it (INV-008, agent-reported).
6. `hold:backlog` makes the system do nothing with the issue; the poll never writes it (D:445, row 1 at D:452). It works on every repo with no config file.
7. Read-side cost is small: E1 costs no call; E2 to E4 are read hourly for the plan request, which is deferred (D:476). A 24-hour `--dry-run` shows holds before any write (D:461).
8. A refused write is `hold_write_failed`, a warning with exit 0; the issue is skipped and retried next cycle, never launched (D:454, D:340). The failure is not remembered between cycles, so the retry spends calls (INV-006, agent-reported; call order partly UNVERIFIED).
9. The off state is not clean (moderator verified `cycle.py:1021-1027`, `test_hold.py:416-426`): with no grant, a failing issue emits `hold_write_failed` instead of `held_incomplete`, and no store entry is made. A person-placed `hold:plan` on an issue that now passes could be skipped for good (stranded part inferred, not run). The grant is read at document level (`pr-a/.../repos.py:94-115`, agent-reported), and the switch is the `issue.hold` grant in `repos.yaml` (`cycle.py:1024`, D:300).
10. Switch-on is safe: the baseline records every issue already assigned and step 7a never touches one, so none of the 17 assigned issues gets a label or comment (D:492).
11. Approval gate, corrected. Master's poll still calls `predicates.approval_of` (`master/src/superclaude/cli/issue_watch/cycle.py:883`, `:998`; moderator verified). The PR 686 head has 0 references to it. PR 682 deleted the post-claim plan approval (the `issue_pipeline` package) and issue 655 chose "assignment is the only trigger" (Clay's paper; not re-read). So the tree with no human gate is the PR 686 head and design 681, not master. The owner's local branch has `Approved` plus the trigger label as its gate (R35, unpushed). The spec must name a commit and a design.
12. Login under cron was tested (`requirements.md:97`, `:110`: `gh auth status` under `env -i HOME PATH=/usr/bin:/bin` stayed logged in). Label write scope under cron was not tested (UNVERIFIED). FU-3 (D:967) says the poll token needs issue-write scope.

## What it costs
<!-- Source: Base (original, modified): CLAY What it costs, create right dropped per Change #4; measured costs appended per Change #5 from Variant 1 Cited fact 8 (corrected) and the CLAY Round 2 cost list -->
- The poll gains write rights on one label, add and remove. The `hold:plan` label is created once per repo by the init, not by the poll. The design adds about 60 lines of rules (D:436-495), `test_hold.py` and a `holds` map in the poll's store (D:486), so the poll is not stateless.
- Measured on the PR 686 head: `LabelWriter` is about 87 lines (`github.py:983` onward); `_hold_write_ok` and `_label_write` sit at `cycle.py:1021-1044`; about 22 of 58 tests in `test_hold.py` touch label writes, the grant, hand removal or dry-run (rough count by test name).
- Added state and reads: a `hand_removed` store state, a live `issue_labels` read (D:456), four evidence reads E1 to E4 and eight new audit reasons (D:340). The store `state` has 2 values and `plan_request` has 5 (D:486).
- FU-3 token scope (D:967), and an R21 label-write test that does not exist yet.
- Taking the label out of PR 686 is not free either: rows 3 to 6, `hand_removed`, the plan request timer and the NG-2 test all assume it. The rework of 4.11 reaches into D07 and was not sized.

## What it risks
<!-- Source: Base (original, modified): CLAY risks 1 to 3 restated with ratings and mitigations; risks 2 and 4 to 8 added per Change #6 (Variant 1 Cited fact 7, split per X-003) and Change #7 (probe findings INV-003 to INV-008). Likelihood and impact are this merge's reading of the debate, not measured -->
Each line: Likelihood, Impact, Mitigation.
1. Unattended wrong write: a wrong-issue or wrong-repo write repeats each cycle until noticed. An add of a label already present is idempotent (OURS withdrew that part in X-003); the wrong-issue repeat stays. Likelihood Low, Impact Medium. Mitigation: the grant switch, the 24-hour dry-run, the call budget (cap 35 minus 3, `issue-watcher.md:361,391`, agent-reported), and a failure memory per cycle (rule 11).
2. The search index shows a label one cycle late (D:494). Likelihood Medium, Impact Low. Mitigation: the live read before a wake (D:456).
3. The off state warns every cycle and can strand a person-placed label (fact 9). Likelihood High if shipped as it is, Impact Low. Mitigation: rule 7.
4. Label write scope under cron is untested (fact 12, UNVERIFIED). Likelihood Medium, Impact Medium. Mitigation: the write stays off until the label-write test passes (rule 12).
5. A passing `plan_check` is a floor. Three headings guard against empty issues only (D:494, A-001). An unfilled template passes, because only HTML comments are stripped (`hold.py:69-70`, `:140`, moderator verified; template `issue-bug-simple.md:43-62`). The match is exact, and the repo's issue forms have no plan fields (INV-005, agent-reported). Likelihood High, Impact Medium. Mitigation: rule 8.
6. Reading the body conflicts with the owner's no-body rule (NFR-002; `issue-watcher.md:226`, INV-007, agent-reported). Likelihood High, Impact Medium. Mitigation: rule 9.
7. Two workspaces polling one repo keep separate stores and re-add a hand-removed label (INV-008, agent-reported; whether workspaces share a store is UNVERIFIED). Likelihood Low, Impact Low. Mitigation: rule 10.
8. The shared `ironbelly` login does not show who acted (FULL-REPORT section 1, item 7). This holds for every GitHub action on this host, including claim comments. Likelihood certain, Impact Low. Mitigation: none needed for the label alone; the grant row and audit log name the reason.

## What it gets right
<!-- Source: Base (original, modified): CLAY What it gets right, "stateless-ish" wording replaced per Change #4; Variant 1 Concession and the Round 2 visibility finding appended per Change #9 -->
- Early and cheap: the check says "plan missing" before a launch is spent on an empty issue. The accuracy check runs after the launch (not independently re-verified), so the read-only check fills a gap. OURS concedes this.
- Humans stay in control: `hold:backlog` is the owner's stop. A hand-removed `hold:plan` is not re-added by the same store.
- An add of a label already present is idempotent. The poll still keeps a `holds` map, so it is not stateless. The one-plan-request-per-hold rule (D:478) waits for D07.
- From OURS: the least-privilege chain (WC-9, `claim.md:9`, R24) stays whole, and the one unattended writer is named, narrow and off by default.
- Conceded visibility finding: the label is the only GitHub-visible hold mark, but no evidence shows anyone reads `hold:plan`. Whether any other person looks at it is UNVERIFIED. Both sides called visibility plausible and unmeasured, a tie, and a tie goes to OURS (75%).
- Conceded capability finding: clearing a hold in the GitHub UI does not work as a release. A hand-cleared label does not free the issue while `plan_check` fails.

## Rule text
<!-- Source: Variant 1 Cited facts 4 and 6 and the probe findings INV-001, INV-003 to INV-009, merged per Change #7 with the Round 2 final positions; rules 1 and 2 also follow Change #1 and #4 -->
1. NG-2 is amended to say: the poll's only GitHub writes are add and remove of the label `hold:plan`, only in a repo that holds the `issue.hold` grant; any other poll write is refused. D2 is unchanged. Test: an argv scan finds only those two calls.
2. The poll never creates a label and never comments about a hold; the per-repo init creates both `hold:plan` and `hold:backlog`. Test: with a missing label, the poll makes no create call.
3. `plan_check` runs before the approval read, so an issue that fails it never launches. Test: a failing issue that carries an approval is skipped as `held_incomplete`.
4. An edit that fills in the plan voids an earlier approval (R19, R36 `edited_after_approval`) and needs a fresh one before launch. Test: edit after approval, then no launch.
5. The `issue.hold` grant is read at document level, and the spec says so (INV-003, agent-reported). Test: one grant is shown to switch the write on for every listed repo, or the spec says otherwise.
6. `hold:backlog` is placed only by a person and the poll only reads it. A hand-removed `hold:plan` is not re-added and does not release the issue while `plan_check` fails.
7. With no grant, a failing issue is skipped as `held_incomplete` with no `hold_write_failed` warning, and a leftover `hold:plan` label is ignored. Test: replace the assertion at `test_hold.py:416-426`.
8. A section whose only content is `<...>` placeholder lines counts as empty. Test: the unfilled issue template fails `plan_check`.
9. The poll may read an issue body for `plan_check` only. The body is held in memory and never put in the audit log, the store, argv or a typed line (NFR-002). Test: grep the audit log and argv for body text.
10. One poll per repo is a stated rule. Test: a second poll on the same repo is refused or documented as unsupported.
11. A failed label write counts against the call budget once per cycle and is remembered for that cycle (INV-006). Test: repeat a refused write inside one cycle and count the calls.
12. The label write stays off until a 24-hour `--dry-run` has shown the holds and a label-write-under-cron test (R21 write scope) has passed; `--dry-run` writes nothing to GitHub.

## Open point
<!-- Source: Debate record, unresolved point C-002, inserted per Change #8 -->
Does the dormant label-write code ship in PR 686 now, or later? This is not agreed (C-002, confidence 62%). CLAY: ship it dormant and enable it per grant later; CLAY does not object to the strictest reading, but marks the 4.11 rework (rows 3 to 6, `hand_removed`, the plan request timer, the NG-2 test) as unsized. OURS: the poll writes no GitHub state in this decision; the label is a later amendment, not a rejection. The rule text above is agreed either way. Still UNVERIFIED: whether the per-repo init runs unattended (R18 says "automatic", `requirements.md:44`), and who, if anyone, reads `hold:plan`. Deferred to D07: the one-hour plan request and the lease comment.

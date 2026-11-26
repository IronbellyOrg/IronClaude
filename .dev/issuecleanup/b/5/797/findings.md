# Round 2 findings: issue #797 (C16) merge-gate reads PR readiness through the existing pr_submit core

Checked 2026-11-24 against master ancestor f2894fc44 (branch ironbelly/Realign). Issue state read live: OPEN, one comment (2026-11-24 22:10): sub-issue #798 (C17, default list of merge-safety files) was merged into #797 by the owner in chat; the changes to carry over are in the comment on #798. Plan files read read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`, VERDICT = `debates/<id>/VERDICT.md`). R38 = `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/6/797/findings.md` (written before the merge of #798). Static analysis: `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/5/analyze/analyze-report.md`.

## Alignment with architectural decisions
Overall: partly aligned. The design (a read-only check, a person's typed go) matches the plan; the owner's R38 lists the read-only merge gate as not adopted and no later ruling reverses it.

| Source | What it says | Verdict | Evidence |
|---|---|---|---|
| R38 (C) | Clay's "read-only merge gate and flags" are not adopted; R38 "supersedes the 'Clay strengths adopted' rows" of the unification spec, which is where `merge-gate` lives (D06). | in conflict (unresolved ruling) | requirements.md:64; SPEC.md:82, :457 |
| R38 (D) | A person's typed go for every merge; the coordinator never merges or closes. A read-only check before the go is compatible. | aligned | requirements.md:64; WORKER-CONTRACT.md:246 (Git and GitHub ownership) |
| Owner action on #716, 2026-11-24 | The backlog review says C16 and C17 "are not authorized merely by appearing in #716". The same day the owner merged #798 into #797 in chat "after a reviewed analysis", which keeps the item alive but is not recorded as a ruling on R38. | partly aligned; UNVERIFIED whether the owner re-ruled R38 for the gate | #716 comment 2026-11-24 14:23; #797 comment 2026-11-24 22:10 |
| D06 VERDICT items 2 and 3 | `merge-gate` (13 closed reasons) is a read-only check shown before the go and run again before `gh pr merge --match-head-commit`; eleven reasons never overridable, only `checks_failing` and `merge_safety` with their own key. | aligned | D06/VERDICT.md:15, :16; SPEC.md:291-292 (SEC-02, SEC-03) |
| D06 item 4 and SEC-04 | `/sc:pr-submit` keeps its silent-reviewer skip in its loop; a separate merge-time hold is added. Reusing the skip rule inside the gate would defeat the hold. | in conflict with the item's done-when "one shared function answers both" for the review reasons | D06/VERDICT.md:17, :35; SPEC.md:293; src/superclaude/pr_submit/reviewers.py:388-392 and :412-420 (absent state; one done plus one absent reads clean) |
| SEC-05 | Never run `/sc:pr-submit` as a worker; reusing its library is a different thing. | aligned | SPEC.md:294; WORKER-CONTRACT.md:23 |
| NFR-6 core purity | The `pr_submit` package contains zero `gh` or `git` tokens, so a gate can reuse its classifiers but must do its own GitHub reads or call the skill's scripts. | partly aligned: the item says "read-only helpers and poll scripts", which is consistent | src/superclaude/pr_submit/__init__.py:12-14 |
| SEC-10 (carried from #798) | Fail closed on weakening values (`merge_safety_files: []`) unless a record names them. The #798 comment says the empty-list test must allow an owner-recorded empty list. | aligned | SPEC.md:299; #798 comment |
| FR-26 | `merge-gate` is a verb of the `superclaude coordinator` group; that group does not exist on master (the `issue-pipeline` verbs on master have no merge verb). | aligned, blocked by C1 and C6 | SPEC.md:228; src/superclaude/cli/issue_pipeline/cli.py:62-409 |
| SEC-01 | The gate runs before the go and again before the merge; a passing gate never triggers a merge. | aligned: the item has no merge call (done-when "never calls a push, comment or fix command") | SPEC.md:290 |
| SEC-13 and RK-2 | Master is unprotected today; every gate "narrows" a risk, never "closes" it. | aligned if worded so | SPEC.md:302, :48; #702 and #723 open |
| Closeout | `/sc:closeout` verifies a merge after it happened; the gate runs before. | aligned (no duplication) | src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh |

Also a carried-over change from #798 not yet in the issue text: name the default `merge_safety_files` list (FR-75 core paths plus `.github/workflows/` as starting candidates), and state whether "absent" means that default list or "hold every merge". `.github/CODEOWNERS` does not exist on master (checked).

## Complementary issues
- #794 (C13, `answer-check`): the typed-go validator runs between the two gate runs (SPEC.md:157). Interface: the shared question key `merge_safety:<PR>:<head sha>` (SPEC.md:297). Neither builds `answer-check`.
- #787 (C6) and #782 (C1): `merge-gate` is a verb of the group C1 and C6 define; the test "gate never calls a push, comment or fix command" is a `refuse(argv)` test whose list C6 and C20 shape.
- #801 (C20, limits and refusal rules): adds rows to the same closed `refuse(argv)` list; its done-when covers deletes, not push or comment.
- #723 and #702 (protect master by GitHub rules): the server-side rules carry the same risk and the same path set (ownership of safety files); the gate "narrows" until they exist. #723's CODEOWNERS paths and this item's default `merge_safety_files` list are one decision.
- #722 (shared login): the gate cannot prove who typed the go.
- #771 (finish after merge): runs after the merge; adjacent, not a duplicate.
- #799 (C18, hand-back rounds): a hand-back round needs the gate's reasons for "not done".
- #665 (closed not planned): its open finding M11 (merge_wait outcomes `declined`, `timeout`, `findings`, `no_response` do not map to the gate's reasons) was never fixed.

## Closest overlap
#794 (C13): both build the merge-go handshake. Shared: question key and head sha binding, the SEC-08 rule that a go is typed in the person's own session, and the dependence on the R38 merge-path ruling. Estimate: about 10% of this item's done-when (neither done-when bullet is covered; only the shared key and the merge go). It would rise to about 40% if the owner assigns `answer-check` here.
Next closest: #787 (C6), about 10% to 15% (the refusal-list test form for "never calls push, comment or fix"); #723, about 10% (the default `merge_safety_files` list shares paths with its CODEOWNERS scope).
No open issue covers the 13 reasons, the `merge-gate` verb or the default list.

## Standalone or merge
Verdict: stand alone (keep open with changes). Test against #794:
- Owner: both the coordinator's merge path; the same role. No difference.
- Acceptance test: #797 proves a reason list from fixture PR states, a per-reason test, the default list and empty-list refusal, and that no push, comment or fix command is called; #794 proves refusal of a gate-only resolution and a wrong key or head.
- Files touched: #797 a new GitHub read path and the `merge-gate` verb plus config keys (`merge_safety_files`, `reviewers`); #794 the escalate step, the sweep allowlist and `answer-check`.
- Build phase: #797 is phase 3 of #716 (C16 to C18); #794 is phase 2.
- Risk if merged: the phase 2 gate display and `answer-check` would be held behind the phase 3 merge path and the R38 ruling; and the 13-reason read path (complex) would be tangled with the display. The earlier merge of #798 into #797 is different: its default list has no consumer without the gate, so it belonged here.
Merging would be right if the owner rules that R38 (C) stands (gate not adopted): then close #797, and the typed go keeps `answer-check` only. It is also reasonable to merge #794 into #797 if the owner decides `answer-check` exists only to serve the merge go; round 2 recommends against it because the other approvals (grants, plan) are given the same way.

## Closed issues and merged PRs checked
- #798 (C17, closed, merged into #797): the default list and the empty-list rule; three changes carried over (listed above).
- #665 (closed not planned): finding M11 stays unresolved.
- #655 (closed not planned): source of the item.
- PR #428 (merged 2026-11-07, draft guard) and issue #375: `merge_guard.py` is a pure decision core and `scripts/set-draft-state.sh` is the one place that talks to GitHub; the same split a gate should keep. It supplies draft state, not a merge gate.
- Issue #421 (closed completed): pr-submit reported Codex clean while its security review still ran; the late-reviewer gap that SEC-04's merge-time hold exists for.
- PR #683 and #668 (closeout, merged): post-merge settle; not a pre-merge check.
- PR #700 and #701 (merged 2026-11-20): rolled back Clay's merge gate design with the rest; no gate code on master.
- PRs #378 and #424, and #237 and #243 (pr-submit conflict resolution, CI wait, silent Augment review; merged): the helpers `ci.py`, `reviewers.py` and `conflicts.py` come from these.
Nothing delivers or supersedes C16; PR #428 and #378 supply parts of the read side.

## Updated recommendation
Keep open with changes, priority P3, complexity complex, size L. Unchanged from round 1 on priority, complexity and size (the merge of #798 adds a small default list and a config test, which does not change the size). Round 2 changes, beyond round 1's five:
1. Put in the issue text the three carried-over changes from #798: allow an owner-recorded empty list, state what "absent" means, name the default list.
2. First line: blocked until the owner says whether R38 (C) still stands for the read-only gate (the owner kept the item alive on 2026-11-24 by merging #798 into it, but recorded no ruling).
3. Replace "same reason list as from the pr_submit helpers" with a per-reason table (4 reasons with a direct helper, 6 with a partial one, 3 with none, per round 1) and a fixture test per reason; drop "one shared function answers both" for the review reasons (SEC-04).
4. Say that the gate does its own GitHub reads or uses the skill scripts, because the pr_submit core holds no `gh` word.

## Scan record
- Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: merge, gate, pr-submit, review, thread, check, safety, protect, CODEOWNERS, guard, closeout, refuse, answer.
- Opened with gh (read-only): open #716, #702, #723, #722, #771, #782, #784, #787, #794, #799, #801 (11); closed #798 (body and comment), #665, #668, #421, #655, #796; merged PRs #428, #683, #700 (bodies; review threads not read). PRs #237, #243, #378 and #701 were fetched but only their titles and the #716 review comment are used; the PR #701 line in the checked list rests on that comment.
- Master check: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick`; Grep for `merge-gate`, `merge_gate`, `merge_safety` in src, tests, docs; Read of `src/superclaude/pr_submit/__init__.py`, `reviewers.py`, `merge_guard.py` headers; `ls .github/CODEOWNERS` (absent).
- UNVERIFIED: the count of 4, 6 and 3 reasons by helper (carried from round 1, not re-derived in full); whether the owner re-ruled R38 for the gate; the current live state of #665's M11.

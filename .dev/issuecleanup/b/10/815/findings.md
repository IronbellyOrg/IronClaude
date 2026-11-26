# Round 2 findings: issue #815 (W7, narrower GitHub token scope for the poll, FU-3)

Checked 2026-11-24 on branch `ironbelly/Realign` at `f2894fc44`. Sources: issue #815, round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/3/815/findings.md`), umbrella #717 and its 2026-11-24 closing review, the plan files under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`, and the code in `src/superclaude/cli/issue_watch/`. Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick` (report `.dev/issuecleanup/b/10/analyze/analyze-report.md`, finding A1).

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`, the merged zero-setup watcher is the design; nothing of Clay's design adopted): ALIGNED. FU-3 is a follow-up row of the merged watcher's own runbook (`docs/designs/issue-watcher-setup.md:670`, `docs/designs/issue-watcher.md:862`), not an element of issue 655's design. Nothing in W7 needs a Clay mechanism.
- **D09, the poll stays read-only on GitHub** (`DECISIONS.md:379-406`; `debates/D09/VERDICT.md:69`; `SPEC.md:16` defines a poll as "Read-only on GitHub"): ALIGNED. W7 narrows the credential to match a duty the code already has; no argv in `github.py:250,256,279,313,348` writes.
- **R35, approval is the `Approved` issue field read from timeline events** (`requirements.md:61`) and **S11-F31, the plan keeps the Project read** (quoted in the issue): ALIGNED, but it sets the scope floor. The poll needs the Project (v2) read, so the token cannot be "repo read only"; whether a fine-grained token can read the organization Project and the issue-field events is UNVERIFIED (it is what FU-3 itself says to confirm, `docs/designs/issue-watcher-setup.md:670`).
- **RK-11** (`spec/SPEC.md:655`, a missing Project field skips every issue silently): PARTLY ALIGNED. A token that lacks the Project scope would reproduce exactly this silent skip; W7's done-when has no check for it.
- **D01 approvers** (`DECISIONS.md:152`, "an allowed approver") and **R4** (`requirements.md:30`, approvers file): no conflict. The token is the poll's reading identity, not an approver identity. The approver question belongs to #722 and #818.
- **Owner-ruled order in #717's review** (point 5: W7 is built when its trigger occurs): ALIGNED with a P3 dormant item.
- **WORKER-CONTRACT.md**: WC-9 (outward actions) and the "Git and GitHub ownership" section bind workers and the coordinator, not the poll's credential: none apply. The launched claim session runs `/sc:issue --claim`, which must write; see Complementary issues.
- Searched: `DECISIONS.md`, `spec/SPEC.md`, `spec/FOLLOW-UPS.md` and all `debates/*/VERDICT.md` for `token`, `GH_TOKEN`, `fine-grained`, `CLI login`; no row decides the poll's credential. In conflict: none.

## Complementary issues

- **#722** (owner and AI helpers share one GitHub login): W7's trigger ("when the owner moves off the CLI login") is exactly the decision #722 asks for. Interface: #722 picks the identity (separate agent account, GitHub App or accepted-for-now); W7 then picks the scope list for that identity's poll token. W7 is completed by #722's decision and must not start before it.
- **#818** (W10, permissions of launched sessions): same identity split. W10 records the launched session's permission mode and blocks a second approver; W7 must not take away the write access the launched session needs. Interface: one statement of "which process holds which token".
- **#823** (W15, runbook update after the live test): both edit `docs/designs/issue-watcher-setup.md` section 1.1 (login and scopes). Write the scope list once, in W15's rewrite.
- **#813** (W5, live firing tests) and **#822** (W14, state folder check): the live run is where the scope list would be captured; no hard link.
- **#774** (docs refresh) and **#777** (map of manual pieces): the token step is one of the manual pieces; no code link.

## Closest overlap

**#722**, "The owner and the AI helpers share one GitHub login: decide how to tell who approved". Shared: the question of whose GitHub identity the watcher uses and what that identity may write; a separate agent account is one proposed option there and the natural holder of W7's token. Estimated cover of W7's done-when: about 20 percent. #722 decides which identity exists but delivers no scope list and no poll run with a read-only token. Next two closest: **#818** (W10, about 10 percent: it states who holds write access in the launched session) and **#823** (W15, about 10 percent: it would hold the runbook text that states the scopes).

## Standalone or merge

Verdict: **stand alone** (against #722; also against #818 and #823).

- Owner and trigger: #722 is an owner decision with no build; W7 is a build that follows the decision. Different actor, different moment.
- Acceptance test: W7's test is "a full poll cycle runs with a token that cannot write to any repo" (a live cycle plus a scope list). #722's test is identity cutover, no unapproved merge, working claim writes. They share no check.
- Files touched: W7 touches the runbook, possibly `check-config` (`cli.py:202`) and nothing else in code. #722 touches identity setup and repository protection (OA-5), not `issue_watch`.
- Build phase: W7 waits on #722 and on the live run. Merging would put a dormant P3 item into a P1 decision issue.
- Risk if merged: a P1 owner decision would carry a speculative scope task and could be closed or reopened by the wrong test; the owner's chat answer to #722 would be mistaken for the W7 go.
- Merge would be right only if the owner answers #722 with "accepted for now, stay on the CLI login": then W7 has no trigger and should be closed as "dropped by owner record in chat" (its own done-when allows that), not merged.

## Closed issues and merged PRs checked

- **#331** (original watcher, closed completed) and **PR #447** (merged, poller): built the `gh` login model; no token seam. No change to W7.
- **#450** (rollout, closed completed 2026-11-24, substituted automatic first-run checks for the old gates) and **PR #485** (docs and capture sheet): the FU-3 row and the `gh auth refresh -s read:project` step live in the runbook they edited; they defer W7 to its trigger.
- **PR #707** (zero-setup watcher, merged) and **PR #729** (R38, merged): the design W7 belongs to; neither builds a token path.
- **PR #759** and **#751** (first-run retry): not related; the retry runs the same `gh` login.
- **#655** (closed not planned): source design; it drops the Project read, so its FU-3 reading differs; the plan keeps the read.
- **PR #448, #548, #584, #591, #700**: approvers file, claim level, approval core, coordinator handoff, revert; none changes the poll credential.
- Nothing delivers, supersedes or contradicts W7.

## Updated recommendation

Keep open with changes: (1) name #722 as the blocker in the issue body; (2) add to "Done when" that the token seen by the launched claim session must still allow `/sc:issue --claim` writes, or is not inherited (Orca's environment handling for the launched terminal is UNVERIFIED); (3) put the scope list in `docs/designs/issue-watcher-setup.md` once, with W15; (4) add that the Project read and issue-field events must work with the narrow token (RK-11 silent-skip risk). Priority **P3**. Complexity **simple**, size **S** (likely an environment value plus a runbook list; becomes medium if `check-config` must verify scopes). Unchanged from round 1 except the added Project-read check (4), which round 1 did not state.

## Scan record

Lists read in full: open-issues.tsv 134 lines, closed-issues.tsv 157 lines, merged-prs.tsv 508 lines (titles; read in pieces of at most 80 lines). Search terms for picking candidates: token, login, identity, scope, approver, credential, permission, runbook, status, alert, poll, watcher, W7 to W15, FU-. Opened in full or read through their body and comments with `gh issue view` / `gh pr view` (raw copies in `.dev/issuecleanup/b/10/raw/`): open #717, #722, #812, #814, #818, #820, #811, #822, #823, #761, #777, #774, #753, #770 (14); closed #331, #450, #655, #665, #751 (5); merged PRs #447, #485, #548, #584, #591, #700, #707, #729 (8). #818, #820, #811 and #823 were read to their done-when lines only. UNVERIFIED: fine-grained token reach over Project v2 and issue-field events; whether the launched session inherits the poll's environment; no cycle was run with a narrow token.

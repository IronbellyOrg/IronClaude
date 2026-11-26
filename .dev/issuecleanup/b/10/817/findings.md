# Round 2 findings: issue #817 (W9, cheaper GitHub reads with conditional requests, FU-5)

Checked 2026-11-24 on branch `ironbelly/Realign` at `f2894fc44`. Sources: issue #817, round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/3/817/findings.md`), umbrella #717 and its closing review, the plan files under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`, and `src/superclaude/cli/issue_watch/`. Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick` (`.dev/issuecleanup/b/10/analyze/analyze-report.md`, findings A5, A6).

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): ALIGNED. FU-5 is a deferred row of the merged watcher's runbook (`docs/designs/issue-watcher-setup.md:672`, `docs/designs/issue-watcher.md:864`).
- **NFR-009 call cap** (`github.py:49-53`, `CALL_CAP = 35`, 4 reserved; `CallBudget` at `github.py:530-560`): ALIGNED as the measured budget. PARTLY ALIGNED in W9's done-when: `CallBudget.spend` counts every call made, including one that would return 304, so "`gh_calls` falling" (`audit.py:166,189`; `cycle.py:1283`) cannot pass unless a call is skipped or a new counter is added.
- **NFR-002 and D09** (`debates/D09/VERDICT.md:49`, no GitHub text in the store or audit log; `DECISIONS.md:379-406`, read-only poll): PARTLY ALIGNED. An ETag is an opaque string, not issue text, but keeping one per read needs storage; cached bodies would break the rule. The store schema is pinned at S12 (`spec/SPEC.md:496`, FR-67) and the loader rejects unknown keys, so a new key is a schema change (S12 is an unconfirmed reference after PR #729, per #717's review).
- **FR-11 multi-repo `run-all`** (`spec/SPEC.md:201`): ALIGNED as the pressure source named by W9; measurement first.
- **R38 and the umbrella order** (#717 review point 5): W9 waits for "captured throttle and call-budget evidence": ALIGNED with a P3 item.
- **WORKER-CONTRACT.md**: not a worker feature; none apply.
- Searched `DECISIONS.md`, `SPEC.md`, `FOLLOW-UPS.md`, all `debates/*/VERDICT.md` for `ETag`, `If-None-Match`, `conditional`, `FU-5`; no row. Only `techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1966` (D-15) says "No code". In conflict: none; W9's technical shape (GraphQL has no ETag) is a design limit, not a decision conflict.

## Complementary issues

- **#812** (W4, exponential backoff for throttling): the same reply handling in `github.py` (`rate_limit_wait` at `github.py:511-521`, header parse at `:474-491`). Interface: both need captured real GitHub replies; one live capture serves both, and conditional reads reduce the throttles W4 reacts to.
- **#811** (W3, configurable poll interval): a shorter interval raises call volume and so the pressure W9 waits for; W9's trigger should be stated per interval.
- **#820** (W12, 7-day review): `slo_numbers` does not include a call count today; the audit lines' `gh_calls` is the available measure of pressure.
- **#813 and #814** (W5, W6): no blocking link; #717's review ties W4/W9 to measured evidence, not to these.
- **#810** (W2, plan request after one quiet hour) and **#770** (watcher hands each claim to the coordinator): add reads or calls per cycle; they change the number to be measured.

## Closest overlap

**#812** (W4), "Exponential backoff with a ceiling for GitHub throttling". Shared: the same file and reply-handling layer, the same unverified real-reply shapes (all 19 reply fixtures are assumed, per #812), the same trigger (measured evidence from a live capture). Estimated cover of W9's done-when: about 15 percent (the evidence capture); backoff does not make an unchanged read free. Next two closest: **#811** (W3, about 5 percent: interval sets the call rate) and **#820** (W12, about 5 percent: the review is where call counts would be read).

## Standalone or merge

Verdict: **stand alone**, decided jointly with #812.

- Owner and trigger: W4 reacts to throttling; W9 prevents calls. Both wait for measured numbers, but W9's extra trigger is budget pressure and W4's is real throttle replies.
- Acceptance test: W4 feeds three throttled replies and sees `next_permitted_at` grow, then reset. W9 needs a repeat poll with no change to spend fewer counted calls, which needs a new counter (see Alignment). The tests share no assertion.
- Files touched: both touch `github.py`. W9 also needs a store key (`record.py`) and a status or audit field; W4 touches the cycle's rate-limit path (`cycle.py`).
- Build phase: both after the live capture; W9 is larger and later.
- Risk if merged: a deferred optimisation with a schema change would hold back a smaller backoff item that is closer to a real failure mode; one PR would carry two risks (store schema and rate-limit logic).
- Merging would be right only if the capture shows throttling is rare and unchanged reads are the cause; then W4 might be dropped and W9 alone kept. Until that is measured, keep both.

## Closed issues and merged PRs checked

- **#331 and PR #447** (poller): built the call cap, `gh_calls` audit field and header-driven rate-limit wait; no conditional reads. Supports W9's "measure first" step (the counter exists).
- **#450** (rollout, closed completed) and **PR #485**: capture sheet for real replies exists in the rollout checklist; #450 closed without a numbers capture, so W9's trigger evidence is still absent. UNVERIFIED: whether the live watcher has produced `gh_calls` figures.
- **PR #707** (merged watcher) and **PR #729** (R38): the design W9 belongs to; no ETag path.
- **#655** (closed not planned): source design; its read-path differs; not adopted.
- **PR #759 / #751, #448, #591, #548, #584, #700**: unrelated to read cost. Nothing delivers, supersedes or contradicts W9.

## Updated recommendation

Keep open with changes: (1) rewrite "Done when" so it does not rely on `gh_calls` falling: add a conditional-hit count, or measure skipped calls; (2) state that GraphQL reads (the issue list, edits, Project) cannot use ETags and are out of scope, or name another method; only the REST event and comment pages qualify (`github.py:270-296`); (3) name the measured trigger (for example `gh_calls` above a stated share of `CALL_CAP` over 7 days, read from the audit log) and block on that measurement, decided together with #812; (4) say that a per-read ETag needs a store key. Priority **P3**. Complexity **complex**, size **L**. Unchanged from round 1; item (4) restates what round 1 listed as a contradiction as a done-when change.

## Scan record

Lists read in full: open-issues.tsv 134 lines, closed-issues.tsv 157 lines, merged-prs.tsv 508 lines. Search terms: ETag, conditional, call budget, rate, throttle, gh_calls, poll interval, W4, W3, W2, run-all, multi-repo, SLO, github.py. Opened in full or to the done-when lines (raw copies in `.dev/issuecleanup/b/10/raw/`): open #717, #812, #811, #814, #820, #822, #823, #818, #722, #761, #777, #774, #753, #770 (14); closed #331, #450, #655, #665, #751 (5); merged PRs #447, #485, #548, #584, #591, #700, #707, #729 (8). #810 was judged by title only (UNVERIFIED body). UNVERIFIED: whether `gh api` surfaces a 304 as an error exit; whether a 304 counts against GitHub's primary limit; real call numbers from a live run; no cycle was run.

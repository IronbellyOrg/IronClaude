## What was tried

**The problem.** The `master` branch of IronbellyOrg/IronClaude has no protection: nothing stops anyone with write access from merging a change with no second look, or from deleting or rewriting the branch. Checked on 2026-11-22: branch protection returns 404, the rulesets list is empty, and there is no `CODEOWNERS` file. Clay's PR 700 (63 files) was merged by its author 21 minutes after opening, with no owner review, and PR 684 was merged by its author after 2 h 29 min. The plan's review rule (decision D16, requirements FR-75 to FR-78, owner item OA-5) needs a server-side setting that only the repository admin can make.

**What was tried.** On 2026-11-22 two agents proposed and debated (three rounds) and a reconciler unified one proposal. The owner asked whether it is allowed by the current plan and whether it needs a paid GitHub plan, then shelved it for later. Nothing below is built or decided.

**Allowed by the plan? Yes.** FR-75 and OA-5 recommend exactly this and say only an admin can do it. The plan says `master` stays unprotected "until an admin sets a ruleset". Nothing in the plan or in the project instructions forbids it. Two plan cautions: run the throwaway test after switching it on (FR-77), because it is unverified that code-owner review at 0 required approvals blocks a non-owner author (risk RK-11, fallback: require 1 approval); and the plan wants Clay's acceptance of the roles text before the gate is announced as binding (FR-76).

**Needs a paid GitHub plan? No, for this repository.** The organisation IronbellyOrg is on the GitHub Free plan and IronClaude is public. GitHub's documentation says "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations". Per-repository rules, required pull requests, code-owner review, no force push or deletion, and an admin bypass are all rules of that kind. Not needed: organisation-wide rulesets and rule insights (Team plan). Catch: the Coder repository is private, and rulesets on private repositories need a paid plan (Pro or Team), so this does not protect Coder.

**The proposal (not decided).**
1. A `.github/CODEOWNERS` file, by pull request, with `@ironbelly` as sole owner of `/.github/CODEOWNERS`, `/docs/designs/` and `/src/superclaude/core/WORKER-CONTRACT.md`, plus two temporary lines for the held draft PRs 686 and 690 (`/src/superclaude/cli/issue_watch/`, `/src/superclaude/skills/sc-issue-protocol/`), removed once those PRs are merged or closed.
2. A ruleset `gate-master` on `master`: restrict deletions, block force pushes, require a pull request with 0 required approvals, dismiss stale approvals, require review from code owners. Bypass list: one entry, the Repository admin role, "for pull requests only". Created by the owner by hand in the GitHub settings page, with enforcement Disabled first.
3. A ruleset `guard-integration` on `integration`: restrict deletions and block force pushes only. The pull-request rule for integration is decided at the day-14 review.
4. Order: the owner approves; a heads-up to Clay; the CODEOWNERS pull request is opened with `/sc:pr-submit --monitor 3` and merged by the owner; the owner creates both rulesets Disabled; an agent reads them back and lists every value in plain English; the owner checks the bypass line on screen and switches both on; three throwaway tests (T1: a throwaway PR changing only `docs/designs/GATE-TEST.md`, expect blocked and review required; T2: the same from the owner login shows the bypass option; T3: a one-line change outside the five paths, expect not blocked); day 7 and day 14 reviews.

**What it does and does not do.** It stops direct pushes, force pushes and deletion, and puts changes to the listed files behind the owner's approval. It does not review everything (a merge like PR 684 on an ungated path still passes), and helpers that share the `ironbelly` login can still use the admin bypass (invariant INV-025) until a separate agent account exists (see issue #722).

**Costs (estimates, not measured).** Owner about 45 minutes, agents about 60 minutes plus monitor waiting, Clay about 10 minutes. Ongoing: the owner's review of gated pull requests. Rolls back with one click (set the rulesets to Disabled).

**Risks.** The gate is narrow; the shared login can still bypass; code-owner review at 0 approvals may not block a non-owner author (test T1 decides); an owner review queue builds up; Clay may dispute sole ownership; a mis-set ruleset (mitigated by Disabled first, read-back and saved JSON).

**Unknown.** Whether the bypass line can be set on the Free plan as the documentation suggests (the rules are created Disabled first, so it would show at set-up); whether organisation-level rulesets exist (the token cannot read them).

## Relevant files and links

- Plan items (local files, not pushed): `.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md` (FR-75 to FR-78, OA-5, risk RK-11), decision D16 (`debates/D16/VERDICT.md`).
- The debate (local, not pushed): `.dev/brainstorms/20261122-owner-actions-debate/X03/` (`FINAL.md`, rounds A-0 to B-3).
- GitHub documentation: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Related: issue #722 (the shared login problem), PR 700 and PR 684 (the merges that showed the gap).

## Done when

A `CODEOWNERS` file is on `master`, `gate-master` and `guard-integration` are active, the three throwaway tests pass with the recorded results (blocked and review required on a gated path; bypass option visible to the owner; not blocked outside the gated paths), every throwaway pull request is closed and its branch deleted, and the owner has said in chat that the gate is live. If T1 is not blocked or T3 is blocked, the ruleset is set back to Disabled and the plan's fallbacks (require 1 approval, or drop the gate and keep the words) are considered.

## Pick-up note

Parked by the owner on 2026-11-22. Do not start until the owner says go. Read `X03/FINAL.md` for the order of steps, the one-sentence approval and what an agent does after it. The owner creates the rulesets by hand; an agent never switches a ruleset on or off without the owner's typed go for that case.
